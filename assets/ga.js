/* Google Analytics (G-VBKVM99CPB), buiten het kritieke pad.
   Events worden meteen in de dataLayer gezet; het gtag.js-script zelf
   komt pas binnen als de pagina klaar is met laden, zodat het de
   eerste weergave nooit vertraagt. */
(function () {
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", "G-VBKVM99CPB", { transport_type: "beacon" });

  var loaded = false;
  function load() {
    if (loaded) return;
    loaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=G-VBKVM99CPB";
    document.head.appendChild(s);
  }
  if (document.readyState === "complete") {
    setTimeout(load, 250);
  } else {
    addEventListener("load", function () { setTimeout(load, 250); });
  }
  /* wie eerder interactie heeft, wordt meteen gemeten */
  ["pointerdown", "keydown", "touchstart", "scroll"].forEach(function (ev) {
    addEventListener(ev, load, { once: true, passive: true });
  });
  /* vertrekt de bezoeker vóór het laden, laad dan alsnog direct: de
     gebufferde dataLayer-events gaan dan via de beacon-transport mee */
  addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") load();
  });
})();
