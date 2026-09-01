(() => {
  "use strict";

  const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const COARSE  = window.matchMedia("(pointer: coarse)").matches;
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp  = (a, b, t) => a + (b - a) * t;

  /* --------------------------------------------------------------
     Shared scroll state — one rAF loop drives everything
     -------------------------------------------------------------- */
  const S = {
    y: 0,          /* scrollY                       */
    vel: 0,        /* smoothed scroll velocity 0..1 */
    heat: 0.55,    /* flame intensity               */
    mx: 0.5,       /* pointer, normalised           */
    my: 0.5
  };

  /* ==============================================================
     1. Flame — WebGL. This is the page's only light source.
     ============================================================== */
  const VERT = `
    attribute vec2 p;
    void main(){ gl_Position = vec4(p, 0.0, 1.0); }
  `;

  const FRAG = `
    precision highp float;
    uniform vec2  uRes;
    uniform float uTime;
    uniform float uHeat;
    uniform float uLean;
    uniform float uGain;

    float hash(vec2 p){
      p = fract(p * vec2(123.34, 456.21));
      p += dot(p, p + 45.32);
      return fract(p.x * p.y);
    }
    float noise(vec2 p){
      vec2 i = floor(p), f = fract(p);
      f = f * f * (3.0 - 2.0 * f);
      float a = hash(i);
      float b = hash(i + vec2(1.0, 0.0));
      float c = hash(i + vec2(0.0, 1.0));
      float d = hash(i + vec2(1.0, 1.0));
      return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
    }
    float fbm(vec2 p){
      float v = 0.0, a = 0.5;
      for (int i = 0; i < 5; i++){
        v += a * noise(p);
        p *= 2.03;
        a *= 0.5;
      }
      return v;
    }

    void main(){
      vec2 uv = gl_FragCoord.xy / uRes.xy;
      float aspect = uRes.x / uRes.y;
      vec2 p = vec2(uv.x * aspect, uv.y);

      float t = uTime * 0.42;

      /* rising, domain-warped smoke field */
      vec2 q = vec2(p.x * 1.35, p.y * 0.95 - t);
      float warp = fbm(q * 1.9 + vec2(0.0, -t * 1.35));
      float n = fbm(q * 3.1 + warp * 1.15);

      /* the plume leans toward the pointer, like a draught in the room */
      float cx = uv.x - 0.5 + uLean * 0.12 * (1.0 - uv.y);
      float spread = mix(0.62, 1.5, uv.y);
      float plume = exp(-pow(abs(cx) / spread, 2.2) * 3.4);

      /* hot at the floor, gone by the top of the layer */
      float rise = pow(1.0 - uv.y, 1.35);

      float f = n * rise * mix(0.35, 1.0, plume);
      f = pow(f, 1.55) * (2.15 + uHeat * 1.9) * uGain;

      /* licks of flame that break away from the body */
      float tongue = fbm(q * 5.4 + warp * 1.3) * rise * plume;
      f += pow(tongue, 2.15) * (1.35 + uHeat * 1.2);

      vec3 col = vec3(0.0);
      col += vec3(0.42, 0.05, 0.01) * smoothstep(0.10, 0.48, f);
      col += vec3(1.00, 0.30, 0.02) * smoothstep(0.30, 0.80, f);
      col += vec3(1.00, 0.69, 0.16) * smoothstep(0.58, 1.05, f);
      col += vec3(1.00, 0.95, 0.82) * smoothstep(0.88, 1.35, f);

      /* cold night bleeding in at the edges so the heat reads hotter */
      col += vec3(0.03, 0.07, 0.13) * (1.0 - plume) * rise * 0.5
             * (1.0 - smoothstep(0.04, 0.30, f));

      float a = clamp(f * 1.35, 0.0, 1.0);
      a *= smoothstep(0.0, 0.16, 1.0 - uv.y);

      gl_FragColor = vec4(col, a);
    }
  `;

  function initFlame(){
    const cv = $("#flame");
    if (!cv || REDUCED) return null;

    const gl = cv.getContext("webgl", {
      alpha: true, premultipliedAlpha: false, antialias: false, depth: false
    }) || cv.getContext("experimental-webgl");
    if (!gl) { cv.style.display = "none"; return null; }

    const compile = (type, src) => {
      const sh = gl.createShader(type);
      gl.shaderSource(sh, src);
      gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
        console.warn(gl.getShaderInfoLog(sh));
        return null;
      }
      return sh;
    };

    const vs = compile(gl.VERTEX_SHADER, VERT);
    const fs = compile(gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) { cv.style.display = "none"; return null; }

    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { cv.style.display = "none"; return null; }
    gl.useProgram(prog);

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, "p");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    const uRes  = gl.getUniformLocation(prog, "uRes");
    const uTime = gl.getUniformLocation(prog, "uTime");
    const uHeat = gl.getUniformLocation(prog, "uHeat");
    const uLean = gl.getUniformLocation(prog, "uLean");
    const uGain = gl.getUniformLocation(prog, "uGain");

    function resize(){
      const dpr = clamp(window.devicePixelRatio || 1, 1, innerWidth < 700 ? 1.2 : 1.6);
      const w = Math.round(cv.clientWidth  * dpr);
      const h = Math.round(cv.clientHeight * dpr);
      if (cv.width !== w || cv.height !== h) {
        cv.width = w; cv.height = h;
        gl.viewport(0, 0, w, h);
      }
      gl.uniform2f(uRes, cv.width, cv.height);
    }
    resize();
    addEventListener("resize", resize, { passive: true });

    return function draw(t){
      resize();
      gl.uniform1f(uTime, t);
      gl.uniform1f(uHeat, S.heat);
      gl.uniform1f(uLean, (S.mx - 0.5) * 2);
      /* a narrow viewport is all plume and no dark edge — pull it back */
      gl.uniform1f(uGain, innerWidth < 760 ? 0.74 : 1.0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    };
  }

  /* ==============================================================
     2. Embers — 2D canvas, sparse and slow
     ============================================================== */
  function initEmbers(){
    const cv = $("#embers");
    if (!cv || REDUCED) return null;
    const ctx = cv.getContext("2d");
    let dpr = 1, parts = [];

    function size(){
      dpr = clamp(window.devicePixelRatio || 1, 1, 2);
      cv.width  = Math.round(innerWidth  * dpr);
      cv.height = Math.round(innerHeight * dpr);
    }
    function spawn(seed){
      return {
        x: Math.random() * innerWidth,
        y: seed ? Math.random() * innerHeight : innerHeight + 20,
        r: 0.6 + Math.random() * 1.9,
        v: 0.25 + Math.random() * 0.85,
        sway: 0.4 + Math.random() * 1.4,
        phase: Math.random() * Math.PI * 2,
        life: 0,
        max: 320 + Math.random() * 520,
        hot: Math.random()
      };
    }
    function reset(){
      size();
      const n = innerWidth < 760 ? 26 : 62;
      parts = Array.from({ length: n }, () => spawn(true));
    }
    reset();
    addEventListener("resize", reset, { passive: true });

    return function draw(t){
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, innerWidth, innerHeight);
      ctx.globalCompositeOperation = "lighter";

      const push = 0.6 + S.heat * 1.5;
      for (const p of parts) {
        p.life++;
        p.y -= p.v * push;
        p.x += Math.sin(t * 0.6 + p.phase) * p.sway * 0.35;
        if (p.life > p.max || p.y < -30) Object.assign(p, spawn(false));

        const k = 1 - p.life / p.max;
        const a = Math.sin(Math.PI * k) * 0.85;
        const col = p.hot > 0.72 ? "255,243,214" : p.hot > 0.34 ? "255,176,32" : "255,77,10";

        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 5);
        g.addColorStop(0,   "rgba(" + col + "," + (a * 0.95).toFixed(3) + ")");
        g.addColorStop(0.4, "rgba(" + col + "," + (a * 0.28).toFixed(3) + ")");
        g.addColorStop(1,   "rgba(" + col + ",0)");
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 5, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalCompositeOperation = "source-over";
    };
  }

  /* ==============================================================
     3. Master loop
     ============================================================== */
  const drawFlame  = initFlame();
  const drawEmbers = initEmbers();

  let last = S.y = window.scrollY || 0;
  let rawVel = 0, running = true, t0 = performance.now();

  const burn = $("#burn");
  const stage = $(".stage");

  function frame(now){
    if (!running) return;
    const t = (now - t0) / 1000;

    /* scroll + velocity */
    const y = window.scrollY || 0;
    rawVel = lerp(rawVel, clamp(Math.abs(y - last) / 42, 0, 1), 0.14);
    S.vel = rawVel;
    last = y;
    S.y = y;

    /* the fire is tallest at the top of the page, and flares when you move */
    const heroFade = 1 - clamp(y / (innerHeight * 0.9), 0, 1);
    S.heat = lerp(S.heat, Math.min(0.28 + heroFade * 0.52 + S.vel * 0.32, 1.02), 0.08);

    /* on the hero the fire stands tall; past it, it settles into a floor */
    if (stage) stage.style.setProperty("--sh", (heroFade * (innerWidth < 760 ? 5 : 10)).toFixed(2) + "%");

    /* de sfeerlagen (vlam + vonken) op 30 fps: visueel gelijk, maar
       het scheelt de helft van het tekenwerk op de hoofdthread */
    S.tick = (S.tick || 0) ^ 1;
    if (S.tick) {
      if (drawFlame)  drawFlame(t);
      if (drawEmbers) drawEmbers(t);
    }
    burnFrame();
    galleryFrame();

    if (burn) {
      const doc = document.documentElement;
      const max = doc.scrollHeight - innerHeight;
      burn.style.width = (max > 0 ? clamp(y / max, 0, 1) * 100 : 0).toFixed(2) + "%";
    }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { running = false; }
    else { running = true; t0 = performance.now() - 1000; requestAnimationFrame(frame); }
  });

  addEventListener("pointermove", (e) => {
    S.mx = e.clientX / innerWidth;
    S.my = e.clientY / innerHeight;
  }, { passive: true });

  /* ==============================================================
     4. Ignition — the mark burns in the middle of a black screen while
     the counter runs to 100. Then the site fades up behind it and the
     mark flies to its place in the header, cooling on the way and
     burning a trail as it goes. When it lands, the fire front sweeps up
     the hero and the page starts lighting itself.
     ============================================================== */
  (function ignition(){
    const wrap  = $("#ignition"), bar = $("#ignBar"), pct = $("#ignPct"),
          meter = $("#ignMeter"), flyer = $("#ignFlyer"),
          navMark = $("#navLogo"),
          brand = $(".nav__brand");

    /* Eerste bezoek met de cookievraag: de intro houdt zich in en het merk
       boven in het menu blijft donker. Het brandende logo van de kaart
       vliegt er straks zelf naartoe (ga.js) — één vlucht, geen twee. */
    const vraagt = document.documentElement.classList.contains("cookie-vraag");

    if (!wrap || !flyer) { if (brand && !vraagt) brand.classList.add("is-landed"); start(); return; }

    /* De volledige vuurshow-intro (logo, teller, vlucht naar het menu)
       hoort bij de homepage en speelt daar bij elk bezoek. Onderliggende
       pagina's openen direct met alleen de korte vuurveeg — dat houdt de
       gemeten laadtijd daar razendsnel. */
    const full = location.pathname === "/";

    if (!full || vraagt) {
      /* een tik wachten zodat het hele script eerst geladen is;
         daarna direct openen met alleen de korte vuurveeg */
      setTimeout(() => {
        if (brand && !vraagt) brand.classList.add("is-landed");
        wrap.classList.add("is-open");
        start();
        sweep();
        wrap.classList.add("is-out");
        setTimeout(() => wrap.remove(), 620);
      }, 0);
      return;
    }

    document.body.classList.add("is-locked");

    let p = 0, ready = false, flown = false;

    Promise.all([
      document.fonts ? document.fonts.ready : Promise.resolve(),
      new Promise((res) => {
        if (document.readyState === "complete") res();
        else addEventListener("load", res, { once: true });
      })
    ]).then(() => setTimeout(() => { ready = true; }, 80));

    const tick = setInterval(() => {
      p = Math.min(p + Math.random() * 14 + 10, ready ? 100 : 94);
      if (bar) bar.style.setProperty("--p", p.toFixed(0) + "%");
      if (pct) pct.textContent = String(Math.floor(p));
      if (p >= 100) { clearInterval(tick); fly(); }
    }, 50);

    /* Two movements, deliberately separate. First the wordmark catches
       from the left, letter by letter, with the fire front travelling
       across it. Only once it is fully alight does it set off. */
    function fly(){
      if (flown) return;
      flown = true;

      document.body.classList.remove("is-locked");
      start();
      if (meter) meter.classList.add("is-done");

      if (REDUCED) {
        flyer.style.setProperty("--reveal", "1");
        land();
        return;
      }

      const REVEAL = 1000;
      const t0 = performance.now();
      flyer.style.setProperty("--edge", "1");

      (function catchFire(now){
        const k = clamp((now - t0) / REVEAL, 0, 1);
        const e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        flyer.style.setProperty("--reveal", e.toFixed(4));
        if (k < 1) requestAnimationFrame(catchFire);
        else {
          flyer.style.setProperty("--reveal", "1");
          flyer.style.setProperty("--edge", "0");
          setTimeout(depart, 220);
        }
      })(t0);
    }

    function depart(){
      const from = flyer.getBoundingClientRect();
      const to   = navMark && navMark.getBoundingClientRect();

      if (!to || !to.width || !flyer.animate) { land(); return; }

      const dx = (to.left + to.width  / 2) - (from.left + from.width  / 2);
      const dy = (to.top  + to.height / 2) - (from.top  + from.height / 2);
      const sc = to.width / from.width;

      setTimeout(() => wrap.classList.add("is-open"), 300);

      const anim = flyer.animate([
        { transform: "translate(0,0) scale(1)",
          filter: "drop-shadow(0 0 46px rgba(255,90,10,.6))" },
        { transform: "translate(" + (dx * 0.38).toFixed(1) + "px," + (dy * 0.64).toFixed(1) + "px) scale(" + (sc + (1 - sc) * 0.44).toFixed(3) + ")",
          filter: "drop-shadow(0 0 24px rgba(255,90,10,.4))", offset: 0.56 },
        { transform: "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + sc.toFixed(3) + ")",
          filter: "drop-shadow(0 0 2px rgba(255,90,10,0))" }
      ], { duration: 1000, easing: "cubic-bezier(.58,0,.16,1)", fill: "forwards" });

      anim.finished.then(land, land);
    }

    function land(){
      if (brand) brand.classList.add("is-landed");
      wrap.classList.add("is-out");
      sweep();
      setTimeout(() => wrap.remove(), 620);
    }

  })();

  /* ==============================================================
     5. Chrome — sticky nav and the fullscreen menu
     ============================================================== */
  (function chrome(){
    const nav = $("#nav"), burger = $("#burger"), menu = $("#menu");

    const onScroll = () => nav && nav.classList.toggle("is-stuck", (window.scrollY || 0) > 24);
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    if (!burger || !menu) return;

    const links = $$("a", menu);
    links.forEach((a, i) => { a.style.transitionDelay = (0.08 + i * 0.06) + "s"; });

    const setOpen = (open) => {
      menu.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
      const btxt = burger.querySelector(".burger__txt");
      if (btxt) btxt.textContent = open
        ? (burger.dataset.txtOpen || "Sluit")
        : (burger.dataset.txtClosed || "Menu");
      document.body.classList.toggle("is-locked", open);
    };

    burger.addEventListener("click", () => setOpen(burger.getAttribute("aria-expanded") !== "true"));
    links.forEach((a) => a.addEventListener("click", () => setOpen(false)));
    addEventListener("keydown", (e) => { if (e.key === "Escape") setOpen(false); });
  })();

  /* ==============================================================
     6. The burn — every piece of this page starts black and is set
     alight from below. A fire front sits low in the viewport; anything
     that rises past it catches, burns up through itself and settles
     into its own colour. Nothing ever un-burns, so what you have read
     stays readable.
     ============================================================== */
  const TEXT_SEL = [
    ".hero__title span", ".lede", ".eyebrow", ".bay__title",
    ".manifesto [data-split] .w", ".prose p",
    ".act__name", ".act__desc",
    ".show__name", ".show__desc", ".show__cta",
    ".case h2", ".case .prose p",
    ".geo__col h3", ".geo__more",
    ".faq__item summary", ".faq__item p",
    ".gal__head .eyebrow", ".gal__hint", ".hero__trust", ".reel__note",
    ".spec__val", ".spec__key",
    ".tvlist li", ".safety dt", ".safety dd",
    ".rating__num", ".rating__meta", ".rating__todo",
    ".page__title", ".crumbs li", ".prose--page > *", ".citylist a",
    ".contact__line span", ".contact__line b", ".form__note", ".field > span",
    ".reel__hud span",
    ".scrollcue span", ".readout div",
    ".ticker__group span",
    ".foot__word", ".foot__bar span"
  ].join(",");

  /* plates in the gallery burn on their own clock (the sideways
     scroll), so they are not registered here */
  const BLOCK_SEL = ".reel, .show__shot";
  /* de sociale links in de voet doen niet mee met het inbrand-effect:
     hun rustkleur moet altijd volledig contrast houden (toegankelijkheid) */
  const FADE_SEL  = ".btn, .chip, .stars, .rating__score, .spec, .safety > div, .book, .field input, .field select, .field textarea, .scrollcue i, .status";

  const burners = [];

  function register(){
    if (REDUCED) return;
    burners.length = 0;
    const add = (sel, cls) => {
      $$(sel).forEach((el) => {
        el.classList.add(cls);
        burners.push({ el, burn: 0, abs: 0, spec: el.matches(".spec") });
      });
    };
    add(TEXT_SEL,  "b-t");
    add(BLOCK_SEL, "b-b");
    add(FADE_SEL,  "b-f");
    measure();
  }

  /* Positions are measured once and read from memory after that, so the
     frame loop never touches layout. */
  function measure(){
    const sy = window.scrollY || 0;
    for (const it of burners) it.abs = it.el.getBoundingClientRect().top + sy;
  }

  /* Two ways the fire arrives, and they are not the same motion.

     On load it climbs: a line rises from the bottom of the screen to
     above the top, and each thing catches as the line reaches it, so
     the hero lights from the ground up.

     After that the line is parked low in the viewport and the page
     moves instead: anything scrolling up through it catches on the way.
     Either way the light comes from below. */
  const REST = 0.86, BAND = 0.24;
  let sweepFrom = 0, endAt = 0, phase = "hold";

  function sweep(){
    sweepFrom = performance.now();
    phase = "sweep";
  }

  function burnFrame(){
    if (phase === "hold" || !burners.length) return;

    const vh = innerHeight, sy = window.scrollY || 0, band = vh * BAND;
    const climbing = phase === "sweep";

    let line = 0;
    if (climbing) {
      const k = clamp((performance.now() - sweepFrom) / 1500, 0, 1);
      const eased = k * k * (3 - 2 * k);          /* even, readable climb */
      line = vh * (1.06 - eased * 1.5);
      if (k >= 1) phase = "scroll";
    }
    /* At the very bottom nothing can rise any further, so whatever is
       still under the line would sit there for ever. Raise the line
       instead of snapping it, so the footer burns in like the rest. */
    const atEnd = (sy + vh) >= (document.documentElement.scrollHeight - 4);
    if (atEnd) { if (!endAt) endAt = performance.now(); } else { endAt = 0; }
    const lift = endAt ? clamp((performance.now() - endAt) / 700, 0, 1) * vh * 0.42 : 0;
    const trigger = vh * REST + lift;

    for (let i = 0; i < burners.length; i++) {
      const it = burners[i];
      if (it.burn >= 1) continue;

      const top = it.abs - sy;
      /* while the line is still climbing, everything under the fold
         waits its turn */
      if (climbing && top > vh) continue;

      const t = climbing
        ? clamp((top - line) / band, 0, 1)
        : clamp((trigger - top) / band, 0, 1);
      if (t <= it.burn + 0.002) continue;

      it.burn = t;
      it.el.style.setProperty("--burn", t.toFixed(3));
      it.el.style.setProperty("--glow", Math.sin(Math.PI * t).toFixed(3));

      if (t >= 1) {
        it.el.classList.remove("burning");
        it.el.classList.add("burnt");
      } else if (!it.el.classList.contains("burning")) {
        it.el.classList.add("burning");
      }
      if (it.spec && t > 0.45) countUp(it.el);
    }
  }

  let remeasure;
  addEventListener("resize", () => {
    clearTimeout(remeasure);
    remeasure = setTimeout(measure, 180);
  }, { passive: true });

  /* ==============================================================
     7. Manifesto — split into words so the fire climbs it line by line
     ============================================================== */
  function splitManifesto(){
    const el = $("[data-split]");
    if (!el || el.dataset.done) return;
    el.dataset.done = "1";

    const words = el.textContent.trim().split(/\s+/);
    el.textContent = "";
    words.forEach((w, i) => {
      const sp = document.createElement("span");
      sp.className = "w";
      sp.textContent = w;
      if (/vuur|hitte|ademen|carri/i.test(w)) sp.classList.add("hot");
      el.appendChild(sp);
      if (i < words.length - 1) el.appendChild(document.createTextNode(" "));
    });
  }

  /* ==============================================================
     8. Spec counters
     ============================================================== */
  function countUp(scope){
    const el = $(".spec__val", scope);
    if (!el || el.dataset.ran) return;
    el.dataset.ran = "1";

    const target = parseFloat(el.dataset.count || "0");
    const dec = parseInt(el.dataset.dec || "0", 10);
    if (REDUCED || target === 0) {
      el.firstChild.nodeValue = target.toFixed(dec);
      return;
    }
    const dur = 1200, t1 = performance.now();
    (function step(now){
      const k = clamp((now - t1) / dur, 0, 1);
      const eased = 1 - Math.pow(1 - k, 3);
      el.firstChild.nodeValue = (target * eased).toFixed(dec);
      if (k < 1) requestAnimationFrame(step);
    })(t1);
  }

  /* ==============================================================
     9b. Gallery — vertical scroll drives the strip sideways

     The rail around the sticky viewport gets extra height equal to
     the hidden width of the track. Scrolling through that height
     translates the track to the left, so the photos ride past —
     revealing left to right — and each burns in from below as it
     enters. When the last one has passed the rail ends and the
     page continues downward on its own.
     ============================================================== */
  const gal = { rail: null, track: null, bar: null, max: 0, plates: [] };

  function sizeGallery(){
    if (!gal.rail) return;
    const vw = gal.rail.clientWidth;
    gal.max = Math.max(0, gal.track.scrollWidth - vw);
    /* one viewport to stand in, plus the sideways distance */
    gal.rail.style.height = (innerHeight + gal.max) + "px";
  }

  function galleryFrame(){
    if (!gal.rail || !gal.max) return;
    const top = gal.rail.getBoundingClientRect().top;
    const p = clamp(-top / gal.max, 0, 1);
    const x = p * gal.max;
    gal.track.style.transform = "translateX(" + (-x) + "px)";
    if (gal.bar) gal.bar.style.width = (p * 100).toFixed(2) + "%";

    /* each plate catches fire as it comes in from the right */
    const vw = gal.rail.clientWidth;
    for (const it of gal.plates) {
      if (it.burn >= 1) continue;
      const left = it.left - x;
      const t = clamp((vw * 0.92 - left) / (it.w * 0.7), 0, 1);
      if (t <= it.burn + 0.002) continue;
      it.burn = t;
      it.el.style.setProperty("--burn", t.toFixed(3));
      it.el.style.setProperty("--glow", Math.sin(Math.PI * t).toFixed(3));
      if (t >= 1) it.el.classList.remove("burning");
      else if (!it.el.classList.contains("burning")) it.el.classList.add("burning");
    }
  }

  function initGallery(){
    const sec = $("#werk");
    if (!sec) return;

    if (REDUCED) {
      /* no choreography: a plain strip you swipe yourself */
      sec.classList.add("gal--flat");
      return;
    }

    gal.rail  = $("#galRail");
    gal.track = $("#galTrack");
    gal.bar   = $("#galBar");
    if (!gal.rail || !gal.track) return;

    sizeGallery();
    gal.plates = $$(".plate", gal.track).map((el) => ({
      el, burn: 0, left: el.offsetLeft, w: el.offsetWidth || 1
    }));
  }

  function resizeGallery(){
    if (!gal.rail) return;
    sizeGallery();
    for (const it of gal.plates) {
      it.left = it.el.offsetLeft;
      it.w = it.el.offsetWidth || 1;
    }
  }

  /* ==============================================================
     10. Video slots — reveal only when footage genuinely plays
     ============================================================== */
  /* Footage that suits the screen. A portrait clip blown up across a
     desktop hero looks soft, so each shape gets its own file and the
     other one is never downloaded. Missing file, no harm: the flame
     carries the hero on its own. */
  const HERO_VIDEO = {
    /* The portrait clip is shown at its own shape in the hero panel on wide
       screens and as the backdrop on phones, so it is never stretched.
       Point `panel` at a wide master if one is ever shot for it. */
    portrait: "/assets/media/hero-portrait.mp4",
    panel:    null
  };

  function initVideo(){
    const hero = $("#heroVideo");
    if (hero) {
      const live = () => hero.classList.add("is-live");
      hero.addEventListener("playing", live);
      hero.addEventListener("loadeddata", () => { if (hero.readyState >= 2) live(); });

      const src = innerWidth >= 980
        ? (HERO_VIDEO.panel || HERO_VIDEO.portrait)
        : HERO_VIDEO.portrait;
      if (src) {
        /* mobiel is streng over autoplay: expliciet gedempt en
           autoplay aan vóór het laden, anders weigert iOS soms */
        hero.muted = true;
        hero.defaultMuted = true;
        hero.autoplay = true;
        hero.setAttribute("muted", "");
        hero.src = src;
        hero.preload = "auto";
        hero.load();
        const tryPlay = () => {
          const p = hero.play();
          if (p && p.catch) p.catch(() => {});
        };
        tryPlay();
        hero.addEventListener("loadeddata", tryPlay, { once: true });
        /* energiebesparing/databesparing blokkeert stille autoplay
           tot de eerste aanraking — dan alsnog starten */
        const kick = () => { if (hero.paused) tryPlay(); };
        ["touchstart", "pointerdown", "scroll"].forEach((ev) =>
          addEventListener(ev, kick, { once: true, passive: true }));
        document.addEventListener("visibilitychange", () => {
          if (!document.hidden && hero.paused) tryPlay();
        });
      }
    }

    /* The two supplied showreel clips. Each starts on its own play
       button, loads its file only then (or when it scrolls into view),
       and pauses itself the moment it leaves the screen. One at a
       time: starting one silences the other. */
    const reels = $$(".reel");
    const players = [];

    reels.forEach((fig) => {
      const vid = $("video", fig), btn = $(".reel__play", fig),
            time = $(".reel__time", fig);
      if (!vid || !btn) return;
      players.push(vid);

      const arm = () => {
        if (vid.src) return;
        /* dezelfde autoplay-eisen als de herovideo: expliciet gedempt
           en inline, anders weigeren telefoons het stille afspelen */
        vid.muted = true;
        vid.defaultMuted = true;
        vid.playsInline = true;
        vid.setAttribute("muted", "");
        vid.src = vid.dataset.src || "";
        vid.preload = "auto";
        vid.load();
        vid.addEventListener("canplay", () => {
          if (fig.classList.contains("in-view") && vid.paused) {
            vid.play().catch(() => {});
          }
        }, { once: true });
      };

      btn.addEventListener("click", () => {
        arm();
        if (vid.paused) {
          for (const other of players) if (other !== vid) other.pause();
          vid.play().catch(() => {});
        } else {
          vid.pause();
        }
      });

      vid.addEventListener("play",  () => fig.classList.add("is-playing"));
      vid.addEventListener("pause", () => fig.classList.remove("is-playing"));

      vid.addEventListener("timeupdate", () => {
        if (!time || !isFinite(vid.duration)) return;
        const sec = Math.floor(vid.currentTime);
        time.textContent = String(Math.floor(sec / 60)).padStart(2, "0") + ":" +
                           String(sec % 60).padStart(2, "0");
      });

      /* De posterframe staat in data-poster in plaats van poster, want een
         poster= wordt door de preload-scanner meteen opgehaald — ook met
         preload="none", ook ver onder de vouw, en juist in het venster
         waarin de stylesheet om bandbreedte vecht. Anderhalf scherm
         voorsprong is ruim genoeg: de zwaarste poster is 37 KB en dus
         binnen voordat de reel in beeld komt. Tot dan staat er hetzelfde
         asgrijs als nu tijdens het laden. */
      if (vid.dataset.poster) {
        const posterWacht = new IntersectionObserver((es) => {
          if (!es.some((e) => e.isIntersecting)) return;
          vid.poster = vid.dataset.poster;
          posterWacht.disconnect();
        }, { rootMargin: "800px 0px", threshold: 0 });
        posterWacht.observe(fig);
      }

      new IntersectionObserver((es) => {
        for (const e of es) {
          fig.classList.toggle("in-view", e.isIntersecting);
          if (e.isIntersecting) { arm(); vid.play().catch(() => {}); }
          else vid.pause();
        }
      }, { threshold: 0.3 }).observe(fig);
    });

    /* mobiel vangnet: weigert de browser stille autoplay (bijv. bij
       energiebesparing), probeer het bij elke aanraking opnieuw voor
       de reels die in beeld staan */
    const kickReels = () => {
      for (const vid of players) {
        const r = vid.getBoundingClientRect();
        if (r.top < innerHeight && r.bottom > 0 && vid.paused && vid.src) {
          vid.play().catch(() => {});
        }
      }
    };
    ["touchstart", "pointerdown"].forEach((ev) =>
      addEventListener(ev, kickReels, { passive: true }));
  }

  /* ==============================================================
     12. Booking form  /* ==============================================================
     12. Booking form
     ============================================================== */
  /* ==============================================================
     11b. Offerte-wizard: drie stappen naar een prijsindicatie, met
     één klik door naar WhatsApp (voor-ingevuld) of het formulier
     ============================================================== */
  function initWizard(){
    const wiz = $("[data-wiz]");
    if (!wiz) return;
    const send = (n, p) => { try { if (window.gtag) window.gtag("event", n, p || {}); } catch (e) {} };
    const steps = $$(".wiz__step", wiz);
    const dots = $$(".wiz__dots li", wiz);
    const state = { occ: "", pkg: "", min: 0, max: 0 };
    const show = (n) => {
      steps.forEach((s) => { s.hidden = s.dataset.step !== String(n); });
      dots.forEach((d, i) => d.classList.toggle("is-on", i < n));
      wiz.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };
    $$(".wiz__chip:not(.wiz__chip--pkg)", wiz).forEach((b) =>
      b.addEventListener("click", () => {
        state.occ = b.dataset.occ;
        $$(".wiz__chip:not(.wiz__chip--pkg)", wiz).forEach((x) => x.classList.toggle("is-sel", x === b));
        send("wizard_step", { step: 1, occasion: state.occ });
        show(2);
      }));
    $$(".wiz__chip--pkg", wiz).forEach((b) =>
      b.addEventListener("click", () => {
        state.pkg = b.dataset.pkg;
        state.min = +b.dataset.min; state.max = +b.dataset.max;
        $$(".wiz__chip--pkg", wiz).forEach((x) => x.classList.toggle("is-sel", x === b));
      }));
    $$("[data-wiz-back]", wiz).forEach((b) =>
      b.addEventListener("click", () =>
        show(b.closest(".wiz__step").dataset.step === "3" ? 2 : 1)));
    const dateEl = $("[data-wiz-date]", wiz), placeEl = $("[data-wiz-place]", wiz);
    const fmtDate = (v) => {
      if (!v) return wiz.dataset.noDate;
      const p = v.split("-");
      return p[2] + "-" + p[1] + "-" + p[0];
    };
    const waBtn = $("[data-wiz-wa]", wiz), formBtn = $("[data-wiz-form]", wiz);
    $("[data-wiz-go]", wiz).addEventListener("click", () => {
      if (!state.pkg) ($(".wiz__chip--pop", wiz) || $(".wiz__chip--pkg", wiz)).click();
      const price = "€" + state.min + " – €" + state.max;
      const parts = [state.occ, state.pkg, fmtDate(dateEl.value)];
      const place = placeEl.value.trim();
      if (place) parts.push(place);
      $("[data-wiz-pick]", wiz).textContent = parts.join("  ·  ");
      $("[data-wiz-price]", wiz).textContent = price;
      const msg = wiz.dataset.waMsg
        .replace("{pkg}", state.pkg).replace("{occ}", state.occ)
        .replace("{date}", fmtDate(dateEl.value))
        .replace("{place}", place || wiz.dataset.noPlace);
      waBtn.href = "https://wa.me/31620020723?text=" + encodeURIComponent(msg);
      const fmsg = wiz.dataset.formMsg
        .replace("{occ}", state.occ).replace("{pkg}", state.pkg).replace("{price}", price);
      formBtn.dataset.d = dateEl.value || "";
      formBtn.dataset.pl = place;
      formBtn.dataset.m = fmsg;
      formBtn.href = wiz.dataset.contact + "?wiz=1"
        + "&m=" + encodeURIComponent(fmsg)
        + (dateEl.value ? "&d=" + encodeURIComponent(dateEl.value) : "")
        + (place ? "&pl=" + encodeURIComponent(place) : "");
      send("wizard_quote", { occasion: state.occ, package: state.pkg,
                             value: state.min, currency: "EUR" });
      show(3);
    });
    waBtn.addEventListener("click", () =>
      send("wizard_whatsapp", { occasion: state.occ, package: state.pkg }));
    formBtn.addEventListener("click", (e) => {
      send("wizard_form", { occasion: state.occ, package: state.pkg });
      /* staat het boekingsformulier op deze pagina? Dan direct invullen
         en ernaartoe scrollen in plaats van navigeren */
      const form = $("#bookForm");
      if (!form) return;
      e.preventDefault();
      if (formBtn.dataset.d && form.datum) form.datum.value = formBtn.dataset.d;
      if (formBtn.dataset.pl && form.locatie && form.locatie.tagName === "INPUT") {
        form.locatie.value = formBtn.dataset.pl;
      }
      if (formBtn.dataset.m && form.bericht && !form.bericht.value) {
        form.bericht.value = formBtn.dataset.m;
      }
      form.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  }

  function initForm(){
    const form = $("#bookForm"), status = $("#formStatus");
    if (!form || !status) return;

    /* voor-invulling vanuit de offerte-wizard op een andere pagina */
    try {
      const q = new URLSearchParams(location.search);
      if (q.get("wiz")) {
        if (q.get("d") && form.datum) form.datum.value = q.get("d");
        if (q.get("pl") && form.locatie && form.locatie.tagName === "INPUT") {
          form.locatie.value = q.get("pl");
        }
        if (q.get("m") && form.bericht && !form.bericht.value) form.bericht.value = q.get("m");
        setTimeout(() => form.scrollIntoView({ block: "center" }), 150);
      }
    } catch (e) {}

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const naam = String(data.get("naam") || "").trim();
      const mail = String(data.get("email") || "").trim();

      status.hidden = false;

      if (!naam || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)) {
        status.textContent = form.dataset.msgInvalid ||
          "Vul je naam en een geldig e-mailadres in, dan kan ik reageren.";
        (naam ? form.querySelector('[name="email"]') : form.querySelector('[name="naam"]')).focus();
        return;
      }

      const payload = {};
      for (const [k, v] of data.entries()) payload[k] = String(v);

      const knop = form.querySelector('button[type="submit"]');
      if (knop) knop.disabled = true;
      status.textContent = form.dataset.msgBusy || "Versturen…";

      try {
        const r = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const uit = await r.json().catch(() => ({}));
        if (!r.ok || !uit.ok) throw new Error("send");

        /* Alleen een bevestigingsmail beloven als hij ook echt verstuurd
           is. Ging dat mis, dan is de aanvraag wel binnen (en krijgt Nuno
           daar apart bericht van), maar dan zeggen we niets wat niet klopt. */
        status.innerHTML = uit.confirmed === false
          ? (form.dataset.msgOkNc ||
             "\u{1F525} Gelukt &mdash; je aanvraag is verstuurd! Ik reageer persoonlijk <b>binnen 24 uur</b>.")
          : (form.dataset.msgOk ||
             ("\u{1F525} Gelukt &mdash; je aanvraag is verstuurd! Je ontvangt direct " +
              "een bevestiging per e-mail en ik reageer <b>binnen 24 uur</b>."));
        form.reset();
      } catch {
        /* vangnet: lukt het versturen niet (offline, of de mailfunctie is
           nog niet geconfigureerd), dan staat de aanvraag klaar als mail */
        const body = [
          "Naam: " + naam,
          "E-mail: " + mail,
          (payload.telefoon ? "Telefoon: " + payload.telefoon : null),
          "Datum: " + (payload.datum || "-"),
          "Act: " + (payload.act || "-"),
          "Locatie: " + (payload.locatie || "-"),
          "Ruimte: " + (payload.ruimte || "-"),
          "", String(payload.bericht || "")
        ].filter((l) => l !== null).join("\n");

        const mailHref = "mailto:nuno@vuurspuwer.com?subject=" +
          encodeURIComponent("Aanvraag " + naam) + "&body=" + encodeURIComponent(body);
        const waHref = "https://wa.me/31620020723?text=" + encodeURIComponent(body);
        status.innerHTML = form.dataset.msgFail
          ? form.dataset.msgFail +
            ' <a href="' + mailHref + '">E-mail →</a> &middot; ' +
            '<a href="' + waHref + '" rel="noopener">WhatsApp →</a>'
          : "Versturen lukte net niet &mdash; " +
            '<a href="' + mailHref + '">stuur je aanvraag via je eigen mailprogramma</a> of ' +
            '<a href="' + waHref + '" rel="noopener">app hem via WhatsApp</a>.';
      } finally {
        if (knop) knop.disabled = false;
      }
    });
  }

  /* ==============================================================
     13. Fit the wordmark to the page — measured, not guessed, so
     "VUURSPUWER" spans the full width at every viewport
     ============================================================== */
  function fitWord(box, measured, cap){
    if (!box || !measured) return;

    box.style.fontSize = "10px";
    const avail = box.clientWidth;
    if (!avail) { box.style.fontSize = ""; return; }

    box.style.fontSize = "200px";
    const natural = measured.scrollWidth;
    if (!natural) { box.style.fontSize = ""; return; }

    box.style.fontSize = Math.min(cap, Math.floor(200 * avail / natural)) + "px";
  }

  function fitHero(){
    const h1 = $(".hero__title");
    if (h1) fitWord(h1, h1.firstElementChild, 300);

    const foot = $(".foot__word");
    if (foot) fitWord(foot, foot, 340);
  }

  /* ==============================================================
     14. Go
     ============================================================== */
  function start(){
    if (start.done) return;
    start.done = true;

    /* Wat hier boven staat bepaalt hoe de eerste verf eruitziet en moet
       dus vóór die verf klaar zijn: splitManifesto en fitHero zetten de
       koppen goed, initGallery geeft de rail zijn hoogte, en register()
       zet alle brandbare elementen op zwart. Zou register() later komen,
       dan flitst de tekst eerst zichtbaar voordat hij dooft. */
    splitManifesto();
    fitHero();
    initGallery();
    register();
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => { fitHero(); measure(); });
    }

    /* De rest is bedrading: videospelers, formulier, wizard, lichtbak,
       de WhatsApp-knop en het jaartal. Niets daarvan bepaalt hoe het
       eerste beeld eruitziet, dus laten we de browser eerst verven en
       doen we dit een frame later. Sinds de stylesheet en de fonts
       eerder binnen zijn, viel deze taak precies over het verfmoment
       heen en schoof de eerste verf een kwart seconde op. */
    if (typeof requestAnimationFrame === "function") {
      requestAnimationFrame(() => setTimeout(bedrading, 0));
    } else {
      bedrading();
    }
  }

  function bedrading(){
    if (bedrading.done) return;
    bedrading.done = true;
    initVideo();
    initForm();
    initWizard();

    const yr = $("#year");
    if (yr) yr.textContent = String(new Date().getFullYear());

    /* WhatsApp-knop: online tijdens de echte openingstijden
       (ma t/m za, 9:00-18:00, Nederlandse tijd), anders eerlijk
       "reageert snel" met een gedoofde stip */
    /* WhatsApp is er altijd: groene stip aan, status op Online */
    const wa = $(".wa");
    if (wa) {
      wa.classList.add("is-online");
      const st = $("#waStatus");
      if (st) st.textContent = wa.dataset.online || "Online";
    }

    /* photo grid: every picture opens full-size in a lightbox,
       with arrows and the keyboard doing what you expect */
    const shots = $$("[data-lightbox]");
    if (shots.length) {
      const box = document.createElement("div");
      box.className = "lightbox";
      box.setAttribute("role", "dialog");
      box.setAttribute("aria-modal", "true");
      box.setAttribute("aria-label", "Fotoweergave");
      box.innerHTML =
        '<button class="lightbox__close" aria-label="Sluiten">&#10005;</button>' +
        '<button class="lightbox__prev" aria-label="Vorige foto">&#8592;</button>' +
        '<img alt="">' +
        '<button class="lightbox__next" aria-label="Volgende foto">&#8594;</button>';
      document.body.appendChild(box);
      const big = $("img", box);
      let cur = 0, opener = null;

      const show = (i) => {
        cur = (i + shots.length) % shots.length;
        const a = shots[cur];
        big.src = a.getAttribute("href");
        big.alt = $("img", a) ? $("img", a).alt : "";
      };
      const open = (i, src) => {
        opener = src || null;
        show(i);
        box.classList.add("is-open");
        document.body.classList.add("is-locked");
        $(".lightbox__close", box).focus();
      };
      const close = () => {
        box.classList.remove("is-open");
        document.body.classList.remove("is-locked");
        big.src = "";
        if (opener) opener.focus();
      };

      shots.forEach((a, i) => a.addEventListener("click", (e) => {
        e.preventDefault();
        open(i, a);
      }));
      $(".lightbox__close", box).addEventListener("click", close);
      $(".lightbox__prev", box).addEventListener("click", () => show(cur - 1));
      $(".lightbox__next", box).addEventListener("click", () => show(cur + 1));
      box.addEventListener("click", (e) => { if (e.target === box) close(); });
      addEventListener("keydown", (e) => {
        if (!box.classList.contains("is-open")) return;
        if (e.key === "Escape") close();
        if (e.key === "ArrowLeft") show(cur - 1);
        if (e.key === "ArrowRight") show(cur + 1);
      });
    }

    /* article images that have not moved over yet would show as broken
       icons; hide them until the uploads folder is in place */
    $$(".prose img, .lede-img img").forEach((img) => {
      img.addEventListener("error", () => {
        const fig = img.closest("figure");
        (fig || img).remove();
        measure();
      });
    });

    /* de hero en de galerij opnieuw opmeten als het venster van vorm verandert */
    addEventListener("resize", () => {
      fitHero();
      measure();
      resizeGallery();
    }, { passive: true });
  }

  /* safety net: if the loader never resolves, run anyway */
  setTimeout(start, 4200);
})();

/* ================================================================
   Deelknop en mini-chat — los blok, draait na het hoofdscript.
   Alles viertalig op basis van de paginataal, zonder extra verzoeken.
   ================================================================ */
(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var lang = (document.documentElement.lang || "nl").slice(0, 2);

  var T = {
    nl: { share: "Deel deze pagina", native: "Delen…", mail: "E-mail", sms: "SMS",
          groet: ["Goedenacht", "Goedemorgen", "Goedemiddag", "Goedenavond"],
          msg: " 🔥 Brandende vraag? Stel hem hier gerust — ik reageer snel.",
          cta: "Chat met Nuno", status: "Online",
          prefill: "Hallo Nuno! Ik heb een vraag over " },
    en: { share: "Share this page", native: "Share…", mail: "Email", sms: "SMS",
          groet: ["Good night", "Good morning", "Good afternoon", "Good evening"],
          msg: " 🔥 Burning question? Ask away — I reply quickly.",
          cta: "Chat with Nuno", status: "Online",
          prefill: "Hello Nuno! I have a question about " },
    de: { share: "Diese Seite teilen", native: "Teilen…", mail: "E-Mail", sms: "SMS",
          groet: ["Gute Nacht", "Guten Morgen", "Guten Tag", "Guten Abend"],
          msg: " 🔥 Eine brennende Frage? Fragen Sie mich einfach — ich antworte schnell.",
          cta: "Mit Nuno chatten", status: "Online",
          prefill: "Hallo Nuno! Ich habe eine Frage zu " },
    fr: { share: "Partager cette page", native: "Partager…", mail: "E-mail", sms: "SMS",
          groet: ["Bonsoir", "Bonjour", "Bonjour", "Bonsoir"],
          msg: " 🔥 Une question brûlante ? Posez-la ici — je réponds vite.",
          cta: "Chatter avec Nuno", status: "En ligne",
          prefill: "Bonjour Nuno ! J'ai une question concernant " },
  };
  var L = T[lang] || T.nl;

  /* ------------------------------------------------ deelknop links */
  var share = $("#share"), btn = $("#shareBtn"), panel = $("#sharePanel");
  if (share && btn && panel) {
    var url = location.href.split("#")[0];
    var title = document.title;
    var enc = encodeURIComponent;
    btn.setAttribute("aria-label", L.share);
    var items = panel.querySelectorAll(".share__item");
    items.forEach(function (a) {
      var k = a.dataset.share, span = a.querySelector("span");
      if (k === "native") {
        span.textContent = L.native;
        if (navigator.share) {
          a.hidden = false;
          a.addEventListener("click", function (e) {
            e.preventDefault();
            navigator.share({ title: title, url: url }).catch(function () {});
            close();
          });
        }
      }
      else if (k === "fb")   a.href = "https://www.facebook.com/sharer/sharer.php?u=" + enc(url);
      else if (k === "msgr") a.href = "fb-messenger://share/?link=" + enc(url);
      else if (k === "wa")   a.href = "https://wa.me/?text=" + enc(title + " " + url);
      else if (k === "mail") { a.href = "mailto:?subject=" + enc(title) + "&body=" + enc(url); span.textContent = L.mail; }
      else if (k === "sms")  { a.href = "sms:?&body=" + enc(title + " " + url); span.textContent = L.sms; }
    });
    var close = function () { panel.hidden = true; btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function () {
      var open = panel.hidden;
      panel.hidden = !open;
      btn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) {
      if (!share.contains(e.target)) close();
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }

  /* ------------------------------------------- mini-chat bij de wa */
  var card = $("#chatCard"), msg = $("#chatMsg"),
      cta = $("#chatCta"), ctaTxt = $("#chatCtaTxt"), status = $("#chatStatus");
  if (!card || !msg) return;

  if (ctaTxt) ctaTxt.textContent = L.cta;
  if (status) status.textContent = L.status;
  if (cta) cta.href = "https://wa.me/31620020723?text=" +
      encodeURIComponent(L.prefill + "…");

  var shown = false;
  function greeting() {
    var h = new Date().getHours();
    var deel = h < 6 ? 0 : h < 12 ? 1 : h < 18 ? 2 : 3;
    return L.groet[deel] + "!" + L.msg;
  }
  function openChat(withTyping) {
    if (shown) { card.hidden = false; requestAnimationFrame(function(){ card.classList.add("is-in"); }); return; }
    shown = true;
    card.hidden = false;
    requestAnimationFrame(function () { card.classList.add("is-in"); });
    var text = greeting();
    if (!withTyping) { msg.textContent = text; return; }
    /* even "typen", dan het bericht letter voor letter */
    setTimeout(function () {
      msg.textContent = "";
      var i = 0;
      (function tick() {
        msg.textContent = text.slice(0, ++i);
        if (i < text.length) setTimeout(tick, 18);
      })();
    }, 1300);
  }
  function closeChat() {
    card.classList.remove("is-in");
    setTimeout(function () { card.hidden = true; }, 450);
    try { sessionStorage.setItem("chatweg", "1"); } catch (e) {}
  }
  var closeBtn = $("#chatClose");
  if (closeBtn) closeBtn.addEventListener("click", closeChat);

  /* na 12 seconden vanzelf openen — één keer per sessie */
  var auto = true;
  try { auto = !sessionStorage.getItem("chatweg"); } catch (e) {}
  if (auto) {
    var arm = function () { setTimeout(function () { if (card.hidden) openChat(true); }, 12000); };
    if (document.readyState === "complete") arm();
    else addEventListener("load", arm, { once: true });
  }
})();

/* Halloween-countdown: telt af naar 31 oktober, schakelt zelf door
   naar volgend jaar en toont op de dag zelf een live-melding. */
(function () {
  var box = document.getElementById("hwBox");
  if (!box) return;
  var els = {};
  box.querySelectorAll("[data-hw]").forEach(function (e) { els[e.dataset.hw] = e; });
  function target() {
    var now = new Date(), y = now.getFullYear();
    if (now > new Date(y, 10, 1)) y += 1;           /* na 1 november: volgend jaar */
    return { y: y, t: new Date(y, 9, 31, 20, 0, 0) };
  }
  function pad(n) { return n < 10 ? "0" + n : "" + n; }
  function tick() {
    var tg = target(), now = new Date(), ms = tg.t - now;
    if (els.y) els.y.textContent = tg.y;
    if (ms <= 0) {                                   /* 31 oktober zelf */
      if (!box.classList.contains("hw--live")) {
        box.classList.add("hw--live");
        var p = document.createElement("p");
        p.className = "hw__live";
        p.textContent = box.dataset.live || "";
        box.querySelector(".hw__timer").after(p);
      }
      return;
    }
    var s = Math.floor(ms / 1000);
    if (els.d) els.d.textContent = Math.floor(s / 86400);
    if (els.h) els.h.textContent = pad(Math.floor(s / 3600) % 24);
    if (els.m) els.m.textContent = pad(Math.floor(s / 60) % 60);
    if (els.s) els.s.textContent = pad(s % 60);
  }
  tick();
  setInterval(tick, 1000);
})();

/* GA4-conversietracking: elke klik die richting een boeking gaat wordt
   als event gemeten. gtag buffert in de dataLayer, dus ook kliks vóór
   het laden van het script gaan niet verloren. */
(function () {
  function send(name, params) {
    try { if (window.gtag) window.gtag("event", name, params || {}); } catch (e) {}
  }
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a,button") : null;
    if (!a) return;
    var h = a.href || "";
    var txt = (a.textContent || "").trim().slice(0, 60);
    if (h.indexOf("tel:") === 0)            send("phone_call",     { link_url: h, link_text: txt });
    else if (h.indexOf("wa.me") > -1)       send("whatsapp_click", { link_url: h, link_text: txt });
    else if (h.indexOf("mailto:") === 0)    send("email_click",    { link_url: h });
    else if (a.id === "chatCta")            send("chat_cta_click", {});
    else if (a.id === "shareBtn")           send("share_open",     {});
    else if (a.closest && a.closest("#sharePanel"))
                                            send("share", { method: a.dataset.share || "link" });
    else if (a.closest && a.closest(".pstrip"))
                                            send("prices_click", { page_path: location.pathname });
    else if (a.closest && a.closest(".hw")) send("halloween_cta",  {});
  }, { capture: true, passive: true });

  /* formulier verstuurd = belangrijkste conversie */
  var form = document.getElementById("bookForm");
  if (form) form.addEventListener("submit", function () {
    send("generate_lead", { form_id: "bookForm", page_path: location.pathname });
  });

  /* mini-chat geopend (één keer per paginaweergave) */
  var card = document.getElementById("chatCard"), chatSeen = false;
  if (card && window.MutationObserver) {
    new MutationObserver(function () {
      if (!card.hidden && !chatSeen) { chatSeen = true; send("chat_open", {}); }
    }).observe(card, { attributes: true, attributeFilter: ["hidden"] });
  }
})();

/* Service worker: assets en bezochte pagina's uit de lokale cache —
   vervolgkliks en herhaalbezoek zijn onmiddellijk, offline werkt de
   site als brochure. Registratie buiten het kritieke pad. */
if ("serviceWorker" in navigator) {
  addEventListener("load", function () {
    setTimeout(function () {
      /* register() slaat de update-controle over als er binnen 24 uur al
         een is geweest, dus een nieuwe versie bereikt een terugkerende
         bezoeker anders dagenlang niet. update() forceert de controle;
         dat kost één voorwaardelijk verzoek van een halve KB. */
      navigator.serviceWorker.register("/sw.js")
        .then(function (r) { if (r && r.update) r.update(); })
        .catch(function () {});
    }, 600);
  });
}

/* Core Web Vitals van echte bezoekers naar GA4: LCP, CLS en INP per
   paginaweergave, verstuurd zodra de bezoeker de pagina verlaat. */
(function () {
  if (!("PerformanceObserver" in window)) return;
  var lcp = 0, cls = 0, inp = 0, sent = false;
  try {
    new PerformanceObserver(function (l) {
      var es = l.getEntries();
      if (es.length) lcp = es[es.length - 1].startTime;
    }).observe({ type: "largest-contentful-paint", buffered: true });
  } catch (e) {}
  try {
    new PerformanceObserver(function (l) {
      l.getEntries().forEach(function (en) {
        if (!en.hadRecentInput) cls += en.value;
      });
    }).observe({ type: "layout-shift", buffered: true });
  } catch (e) {}
  try {
    new PerformanceObserver(function (l) {
      l.getEntries().forEach(function (en) {
        if (en.duration > inp) inp = en.duration;
      });
    }).observe({ type: "event", durationThreshold: 40, buffered: true });
  } catch (e) {}
  addEventListener("visibilitychange", function () {
    if (document.visibilityState !== "hidden" || sent || !window.gtag) return;
    sent = true;
    gtag("event", "web_vitals", {
      metric_lcp: Math.round(lcp),
      metric_cls: Math.round(cls * 1000) / 1000,
      metric_inp: Math.round(inp),
      page_path: location.pathname,
      non_interaction: true
    });
  });
})();

/* Licht/donker-schakelaar: keuze onthouden, theme-color meebewegen. */
(function () {
  var btn = document.getElementById("themeBtn");
  var meta = document.querySelector('meta[name="theme-color"]');
  function apply(t, save) {
    if (t === "light") document.documentElement.setAttribute("data-theme", "light");
    else document.documentElement.removeAttribute("data-theme");
    if (meta) meta.setAttribute("content", t === "light" ? "#FAF4E9" : "#0A0705");
    if (btn) btn.setAttribute("aria-pressed", String(t === "light"));
    if (save) try { localStorage.vsTheme = t; } catch (e) {}
  }
  apply(document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark", false);
  if (btn) btn.addEventListener("click", function () {
    var t = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
    apply(t, true);
    try { if (window.gtag) gtag("event", "theme_toggle", { theme: t }); } catch (e) {}
  });
})();

/* Verse reviews: de "x geleden"-tijd wordt bij elk bezoek live
   uitgerekend in de taal van de pagina, en de NIEUW-badge dooft
   na 45 dagen vanzelf — de sectie blijft dus altijd eerlijk vers. */
(function () {
  var els = document.querySelectorAll("[data-rev-date]");
  if (!els.length) return;
  var lang = (document.documentElement.lang || "nl").slice(0, 2);
  var rtf;
  try { rtf = new Intl.RelativeTimeFormat(lang, { numeric: "auto" }); }
  catch (e) { return; }
  els.forEach(function (el) {
    var days = Math.floor((Date.now() - new Date(el.getAttribute("data-rev-date")).getTime()) / 864e5);
    if (isNaN(days) || days < 0) days = 0;
    if (el.hasAttribute("data-rev-new")) {
      if (days > 45) el.remove();
      return;
    }
    var txt;
    if (days < 7) txt = rtf.format(-days, "day");
    else if (days < 30) txt = rtf.format(-Math.round(days / 7), "week");
    else if (days < 365) txt = rtf.format(-Math.round(days / 30), "month");
    else txt = rtf.format(-Math.round(days / 365), "year");
    el.textContent = txt;
  });
})();
