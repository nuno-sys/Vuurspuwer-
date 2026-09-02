const V = "vs-5d7d8767af";
/* "/" staat hier bewust NIET in: die haalde de homepage op bij het eerste
   bezoek aan elke willekeurige pagina, ook als de bezoeker er nooit heen
   ging. Hij komt vanzelf in de cache zodra iemand hem opvraagt. */
const CORE = [
  "/assets/site.css?v=5d7d8767af", "/assets/site.js?v=5d7d8767af",
  "/assets/fonts/archivo-latin.woff2", "/assets/fonts/instrument-latin.woff2",
  "/assets/fonts/jetbrains-latin.woff2"
];
const OFFLINE = "/offline/";
const VERS = 600000;              /* 10 minuten; daarna eerst het netwerk */
const STEMPEL = "x-sw-at";

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V)
    .then((c) => Promise.all(CORE.map((u) => c.add(u).catch(() => {}))))
    .then(() => caches.open(V).then((c) => c.add(OFFLINE).catch(() => {})))
    .then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    /* zonder navigationPreload staat de netwerkfetch bij elke navigatie te
       wachten tot de worker is opgestart - op een koude telefoon 50-250ms */
    if (self.registration.navigationPreload) {
      try { await self.registration.navigationPreload.enable(); } catch (x) {}
    }
    const ks = await caches.keys();
    await Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* een gecachede kopie krijgt een tijdstempel mee, zodat we later weten
   of hij nog vers genoeg is om zonder netwerk te serveren */
function metStempel(res) {
  const h = new Headers(res.headers);
  h.set(STEMPEL, String(Date.now()));
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
}
function vers(res) {
  const t = res && res.headers.get(STEMPEL);
  return !!t && (Date.now() - Number(t)) < VERS;
}

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/")) return;
  /* video's laten we volledig met rust: de browser vraagt ze met Range op,
     krijgt 206 terug, en de Cache API weigert 206 - dat leverde bij elke
     mediarequest een stille afwijzing op, plus een omweg om niets */
  if (/\.(mp4|webm|mov|m4v)$/.test(url.pathname)) return;

  if (url.pathname.startsWith("/assets/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      if (hit) return hit;
      const res = await fetch(e.request);
      if (res.status === 200) { try { await c.put(e.request, res.clone()); } catch (x) {} }
      return res;
    }));
    return;
  }

  if (e.request.mode === "navigate" || url.pathname.endsWith("/")) {
    e.respondWith((async () => {
      const c = await caches.open(V);
      const hit = await c.match(e.request);
      /* de browser is al begonnen met ophalen (navigationPreload); dat
         antwoord gebruiken scheelt een tweede verzoek om hetzelfde */
      const haal = (async () => {
        let res = null;
        try { res = await e.preloadResponse; } catch (x) {}
        if (!res) res = await fetch(e.request);
        if (res && res.status === 200) {
          try { await c.put(e.request, metStempel(res.clone())); } catch (x) {}
        }
        return res;
      })();
      if (hit && vers(hit)) { haal.catch(() => {}); return hit; }
      try { return await haal; } catch (x) { return hit || (await c.match(OFFLINE)) || Response.error(); }
    })());
  }
});
