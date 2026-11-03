// Worker-ingang voor vuurspuwer.com.
//
// De site zelf is statisch (./dist, zie wrangler.jsonc) en wordt door
// Cloudflare rechtstreeks geserveerd; alleen /api/* komt hier binnen
// (run_worker_first). De handlers zijn de bestaande Pages Functions in
// functions/api/ — ongewijzigd, dus dezelfde code werkt op Pages én als
// Worker. Zonder deze ingang draaide een Worker-deploy alleen de statische
// bestanden en bestonden /api/contact en /api/opvolging niet.
import * as contact from "../functions/api/contact.js";
import * as opvolging from "../functions/api/opvolging.js";

const ROUTES = { "/api/contact": contact, "/api/opvolging": opvolging };

export default {
  async fetch(request, env, ctx) {
    const pad = new URL(request.url).pathname.replace(/\/+$/, "");
    const mod = ROUTES[pad];
    if (!mod) return env.ASSETS.fetch(request);

    const m = request.method.toUpperCase();
    const handler = mod["onRequest" + m[0] + m.slice(1).toLowerCase()] || mod.onRequest;
    if (!handler) {
      const toegestaan = Object.keys(mod)
        .filter((k) => k.startsWith("onRequest") && k.length > 9)
        .map((k) => k.slice(9).toUpperCase());
      return new Response("Method Not Allowed", {
        status: 405,
        headers: { Allow: toegestaan.join(", ") },
      });
    }
    // dezelfde context die Pages Functions krijgen
    return handler({
      request,
      env,
      params: {},
      data: {},
      functionPath: pad,
      waitUntil: (p) => ctx.waitUntil(p),
      passThroughOnException: () => ctx.passThroughOnException(),
      next: () => env.ASSETS.fetch(request),
    });
  },
};
