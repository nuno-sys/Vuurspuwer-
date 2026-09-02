/* Client-side zoekmachine voor de statische site.
   Leest /zoekindex.json (per taal opgebouwd tijdens de build), filtert
   op titel/beschrijving/adres en toont gerangschikte resultaten. Werkt
   zonder server; de voettekst-zoekbalk stuurt gewoon via GET hierheen. */
(function () {
  "use strict";
  var cfg = document.getElementById("zoekData");
  if (!cfg) return;

  var lang     = cfg.getAttribute("data-lang") || "nl";
  var indexUrl = cfg.getAttribute("data-index") || "/zoekindex.json";
  var pageUrl  = cfg.getAttribute("data-url") || location.pathname;
  var M = {
    typ:     cfg.getAttribute("data-msg-typ")   || "",
    none:    cfg.getAttribute("data-msg-none")  || "Niets gevonden voor",
    count:   cfg.getAttribute("data-msg-count") || "resultaten voor",
    one:     cfg.getAttribute("data-msg-one")   || "resultaat voor",
    loading: cfg.getAttribute("data-msg-loading") || "Zoeken…"
  };

  var form   = document.getElementById("zoekForm");
  var input  = document.getElementById("zoekIn");
  var status = document.getElementById("zoekStatus");
  var out    = document.getElementById("zoekResultaten");
  var idx = null, klaar = false;

  function qUit() {
    var m = /[?&]q=([^&]*)/.exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, " ")) : "";
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function norm(s) {
    return String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function markeer(text, toks) {
    var s = esc(text);
    for (var i = 0; i < toks.length; i++) {
      if (!toks[i]) continue;
      var re = new RegExp("(" + toks[i].replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
      s = s.replace(re, "<mark>$1</mark>");
    }
    return s;
  }

  function toon(q) {
    q = (q || "").trim();
    if (input && input.value !== q) input.value = q;
    if (!q) { out.innerHTML = ""; status.textContent = M.typ; return; }
    if (!idx) { status.textContent = M.loading; return; }

    var toks = norm(q).split(/\s+/).filter(Boolean);
    var res = [];
    for (var i = 0; i < idx.length; i++) {
      var d = idx[i], t = norm(d.t), de = norm(d.d), u = norm(d.u);
      var score = 0, hits = 0;
      for (var j = 0; j < toks.length; j++) {
        var tok = toks[j], f = 0;
        if (t.indexOf(tok) >= 0) { f += 10; if (t.indexOf(tok) === 0) f += 5; }
        if (de.indexOf(tok) >= 0) f += 3;
        if (u.indexOf(tok) >= 0) f += 2;
        if (f > 0) { hits++; score += f; }
      }
      if (hits > 0) {
        if (hits === toks.length) score += 25;  // alle woorden gevonden
        res.push({ d: d, s: score });
      }
    }
    res.sort(function (a, b) { return b.s - a.s; });
    res = res.slice(0, 50);

    if (!res.length) {
      out.innerHTML = "";
      status.textContent = M.none + " “" + q + "”.";
      return;
    }
    status.textContent = res.length + " " + (res.length === 1 ? M.one : M.count) + " “" + q + "”.";
    var html = "";
    for (var k = 0; k < res.length; k++) {
      var r = res[k].d;
      html += '<li class="zres"><a href="' + esc(r.u) + '">'
        + '<span class="zres__t">' + markeer(r.t, toks) + "</span>"
        + '<span class="zres__u">' + esc(r.u) + "</span>"
        + (r.d ? '<span class="zres__d">' + markeer(r.d, toks) + "</span>" : "")
        + "</a></li>";
    }
    out.innerHTML = html;
  }

  var q0 = qUit();
  if (input) input.value = q0;
  status.textContent = q0 ? M.loading : M.typ;

  fetch(indexUrl, { credentials: "omit" })
    .then(function (r) { return r.json(); })
    .then(function (j) { idx = (j && j[lang]) || []; klaar = true; toon(input ? input.value : q0); })
    .catch(function () { status.textContent = M.none + " “" + (input ? input.value : q0) + "”."; });

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = input ? input.value.trim() : "";
      var nu = pageUrl + (q ? "?q=" + encodeURIComponent(q) : "");
      if (history.replaceState) history.replaceState(null, "", nu);
      toon(q);
    });
    if (input) input.addEventListener("input", function () { if (klaar) toon(input.value); });
  }
})();
