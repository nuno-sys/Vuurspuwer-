/* Google Analytics (G-VBKVM99CPB) achter een toestemmingsdrempel.

   Zonder toestemming gebeurt er niets: geen gtag.js, geen cookies, geen
   verzoek naar Google. Events worden hoogstens in een lokale dataLayer
   gezet — dat is enkel geheugen in de tab en verlaat het apparaat niet.
   Pas als de bezoeker op "meet maar mee" klikt wordt het echte script
   geladen; de gebufferde events gaan dan alsnog in één keer mee.

   Weigert de bezoeker, dan slaan we alleen die keuze op en laadt er
   nooit iets. De keuze is onderaan de site altijd te herzien. */
(function () {
  var ID = "G-VBKVM99CPB";
  var SLEUTEL = "vsCookies";        /* "ja" | "nee" */

  /* ====================================================================
     TIJDELIJK — analytics voor iedereen, cookiebanner uit.
     Reden: even echt verkeer kunnen zien in Google Analytics. Zolang dit
     "true" is laadt GA meteen voor elke bezoeker en verschijnt de
     toestemmingskaart niet. Zet terug op "false" om de nette
     toestemmingsdrempel te herstellen (dan blokkeert "Liever niet" GA weer).
     ==================================================================== */
  var ALTIJD = true;

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  function keuze() {
    try { return localStorage.getItem(SLEUTEL); } catch (e) { return null; }
  }
  function bewaar(v) {
    try { localStorage.setItem(SLEUTEL, v); } catch (e) {}
  }

  var HTML = document.documentElement;
  var TRAAG = false;
  try { TRAAG = matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) {}

  /* Staat de vraag nog open, dan houdt de intro zich in: het merk boven
     in het menu blijft donker tot het logo van de kaart er landt. Dit
     script staat voor site.js, dus de vlag staat er op tijd. */
  if (!ALTIJD && keuze() === null) HTML.classList.add("cookie-vraag");

  function merk() {
    return document.getElementById("navLogo") ||
           document.querySelector(".nav__brand .logo");
  }
  /* het merk staat op zijn plek: zichtbaar maken en de vlag intrekken */
  function geland() {
    var b = document.querySelector(".nav__brand");
    if (b) { b.classList.remove("is-vliegend"); b.classList.add("is-landed"); }
    HTML.classList.remove("cookie-vraag");
  }

  /* ---------------------------------------------- Analytics starten */
  var gestart = false, geladen = false;
  function start() {
    if (gestart) return;
    gestart = true;
    gtag("js", new Date());
    gtag("config", ID, { transport_type: "beacon", anonymize_ip: true });

    function laad() {
      if (geladen) return;
      geladen = true;
      var s = document.createElement("script");
      s.async = true;
      s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
      document.head.appendChild(s);
    }
    /* net als voorheen buiten het kritieke pad houden */
    if (document.readyState === "complete") setTimeout(laad, 250);
    else addEventListener("load", function () { setTimeout(laad, 250); });
    ["pointerdown", "keydown", "touchstart", "scroll"].forEach(function (ev) {
      addEventListener(ev, laad, { once: true, passive: true });
    });
    addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") laad();
    });
  }

  /* ------------------------------------------------- de keuzekaart */
  function kaart() { return document.getElementById("cookie"); }

  var bezig = false;                  /* er vliegt een logo: niet nog eens */

  /* na de eerstvolgende geverfde frame */
  function straks(fn) {
    if (typeof requestAnimationFrame !== "function") { fn(); return; }
    requestAnimationFrame(function () { requestAnimationFrame(fn); });
  }

  /* De kaart is beeldvullend met een backdrop-filter en geanimeerde
     verlopen; hem tonen kost een dure compositie. Valt die vóór het
     eerste beeld, dan schuift het eerste beeld op — gemeten ~130ms op
     een trage telefoon. Dus: eerst de pagina laten verschijnen, dan de
     kaart. De bezoeker ziet hem nog steeds meteen, maar nu ópkomend
     over een pagina die er al staat in plaats van over een zwart vlak. */
  function naEersteVerf(fn) {
    var gedaan = false;
    function eenmaal() { if (!gedaan) { gedaan = true; straks(fn); } }
    var vangnet = setTimeout(eenmaal, 2500);
    try {
      var po = new PerformanceObserver(function (l) {
        for (var i = 0; i < l.getEntries().length; i++) {
          if (l.getEntries()[i].name === "first-contentful-paint") {
            po.disconnect(); clearTimeout(vangnet); eenmaal(); return;
          }
        }
      });
      po.observe({ type: "paint", buffered: true });
    } catch (e) { clearTimeout(vangnet); eenmaal(); }
  }

  function toon() {
    var k = kaart();
    if (!k) { geland(); return; }     /* geen kaart: merk niet in het donker laten */
    k.classList.remove("is-weg");
    k.hidden = false;
    HTML.classList.add("cookie-open");
    var ja = document.getElementById("cookieJa");
    if (ja) setTimeout(function () { try { ja.focus(); } catch (e) {} }, 60);
  }

  function sluit() {
    var k = kaart();
    if (k) { k.hidden = true; k.classList.remove("is-weg"); }
    HTML.classList.remove("cookie-open");
  }

  function antwoord(v) {
    if (bezig) return;
    bezig = true;
    bewaar(v);
    if (v === "ja") start();
    /* Het sein voor site.js: nu pas vat de pagina vlam. Zolang de kaart
       er lag had inbranden geen zin — er lag een doek van 94% overheen. */
    try { document.dispatchEvent(new CustomEvent("vuur:keuze", { detail: v })); }
    catch (e) {
      try {
        var ev = document.createEvent("Event");
        ev.initEvent("vuur:keuze", true, false);
        document.dispatchEvent(ev);
      } catch (e2) {}
    }
    vlieg();
  }

  /* Bij een keuze dooft de kaart en maakt hij een kopie van het merk los.
     Die vliegt op gemiddelde snelheid naar zijn echte plek boven in het
     menu — op mobiel en desktop naar dezelfde gemeten plek — en koelt
     onderweg af. Precies daar licht het echte merk op, zodat er geen
     sprongetje te zien is. Lukt de vlucht niet (geen animatie-API,
     minder beweging, geen doel), dan landt het merk meteen. */
  function vlieg() {
    var k = kaart();
    var bron = k && k.querySelector(".cookie__vlam");
    var doel = merk();
    var brand = document.querySelector(".nav__brand");

    if (!k || k.hidden || !bron || !doel || TRAAG || !bron.animate) {
      sluit(); geland(); bezig = false; return;
    }

    if (brand) { brand.classList.remove("is-landed"); brand.classList.add("is-vliegend"); }

    var a = bron.getBoundingClientRect();
    var b = doel.getBoundingClientRect();
    if (!a.width || !b.width) { sluit(); geland(); bezig = false; return; }

    var vlieger = bron.cloneNode(true);
    vlieger.className = bron.className + " cookie__vlieger";
    vlieger.setAttribute("aria-hidden", "true");
    vlieger.style.left = a.left + "px";
    vlieger.style.top = a.top + "px";
    vlieger.style.width = a.width + "px";
    vlieger.style.setProperty("--logo-w", a.width + "px");
    document.body.appendChild(vlieger);

    k.classList.add("is-weg");
    HTML.classList.remove("cookie-open");

    var dx = (b.left + b.width / 2) - (a.left + a.width / 2);
    var dy = (b.top + b.height / 2) - (a.top + a.height / 2);
    var sc = b.width / a.width;

    var vlucht = vlieger.animate([
      { transform: "translate(0,0) scale(1)",
        filter: "drop-shadow(0 2px 14px rgba(255,110,20,.9)) drop-shadow(0 -8px 30px rgba(255,60,0,.55))" },
      { transform: "translate(" + (dx * 0.34).toFixed(1) + "px," + (dy * 0.62).toFixed(1) + "px) scale(" + (sc + (1 - sc) * 0.46).toFixed(3) + ")",
        filter: "drop-shadow(0 1px 11px rgba(255,120,20,.5))",
        offset: 0.56 },
      { transform: "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px) scale(" + sc.toFixed(3) + ")",
        filter: "drop-shadow(0 0 2px rgba(255,90,10,0))" }
    ], { duration: 1050, easing: "cubic-bezier(.58,0,.16,1)", fill: "forwards" });

    function neer() {
      geland();
      sluit();
      vlieger.style.transition = "opacity .4s linear";
      vlieger.style.opacity = "0";
      setTimeout(function () {
        if (vlieger.parentNode) vlieger.parentNode.removeChild(vlieger);
      }, 460);
      bezig = false;
    }
    if (vlucht.finished) vlucht.finished.then(neer, neer);
    else vlucht.onfinish = neer;
    setTimeout(function () { if (bezig) neer(); }, 1600);   /* vangnet */
  }

  function koppel() {
    var k = kaart();
    if (!k) return;
    var ja = document.getElementById("cookieJa");
    var nee = document.getElementById("cookieNee");
    if (ja) ja.addEventListener("click", function () { antwoord("ja"); });
    if (nee) nee.addEventListener("click", function () { antwoord("nee"); });

    /* Escape geldt als weigeren: geen keuze mag nooit toestemming betekenen */
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !k.hidden && !bezig) antwoord("nee");
    });
    /* de aandacht binnen de kaart houden zolang hij openstaat */
    k.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var f = k.querySelectorAll("button, a[href]");
      if (!f.length) return;
      var eerste = f[0], laatste = f[f.length - 1];
      if (e.shiftKey && document.activeElement === eerste) { laatste.focus(); e.preventDefault(); }
      else if (!e.shiftKey && document.activeElement === laatste) { eerste.focus(); e.preventDefault(); }
    });

    /* opnieuw kiezen vanuit de voettekst */
    var herzie = document.querySelectorAll("[data-cookie-herzie]");
    for (var i = 0; i < herzie.length; i++) {
      herzie[i].addEventListener("click", function (e) {
        e.preventDefault();
        toon();
      });
    }
  }

  function begin() {
    if (ALTIJD) {                     /* TIJDELIJK: meteen meten, geen banner */
      HTML.classList.remove("cookie-vraag");
      start();
      return;
    }
    koppel();
    var v = keuze();
    if (v === "ja") start();
    else if (v !== "nee") naEersteVerf(toon);   /* nog geen keuze: vragen */
    else HTML.classList.remove("cookie-vraag");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", begin);
  } else {
    begin();
  }
})();
