const V = "vs-74a6ae2ddb";
const CORE = [
  "/", "/assets/site.css?v=74a6ae2ddb", "/assets/site.js?v=74a6ae2ddb",
  "/assets/fonts/archivo-latin.woff2", "/assets/fonts/instrument-latin.woff2",
  "/assets/fonts/jetbrains-latin.woff2"
];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/")) return;
  if (url.pathname.startsWith("/assets/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      if (hit) return hit;
      const res = await fetch(e.request);
      if (res.ok) c.put(e.request, res.clone());
      return res;
    }));
    return;
  }
  if (e.request.mode === "navigate" || url.pathname.endsWith("/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      const net = fetch(e.request).then((res) => {
        if (res.ok) c.put(e.request, res.clone());
        return res;
      }).catch(() => hit || c.match("/"));
      return hit || net;
    }));
  }
});
