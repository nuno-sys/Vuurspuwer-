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

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  function keuze() {
    try { return localStorage.getItem(SLEUTEL); } catch (e) { return null; }
  }
  function bewaar(v) {
    try { localStorage.setItem(SLEUTEL, v); } catch (e) {}
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

  function toon() {
    var k = kaart();
    if (!k) return;
    k.hidden = false;
    document.documentElement.classList.add("cookie-open");
    var ja = document.getElementById("cookieJa");
    if (ja) setTimeout(function () { try { ja.focus(); } catch (e) {} }, 60);
  }

  function sluit() {
    var k = kaart();
    if (k) k.hidden = true;
    document.documentElement.classList.remove("cookie-open");
  }

  function antwoord(v) {
    bewaar(v);
    sluit();
    if (v === "ja") start();
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
      if (e.key === "Escape" && !k.hidden) antwoord("nee");
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
    koppel();
    var v = keuze();
    if (v === "ja") start();
    else if (v !== "nee") toon();     /* nog geen keuze: vragen */
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", begin);
  } else {
    begin();
  }
})();
