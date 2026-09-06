// Test: het cache- en header-contract van de site, zoals Cloudflare Pages
// het uit _headers toepast. Draai lokaal tegen `wrangler pages dev dist`
// of tegen de live site:
//   node tests/headers.mjs http://127.0.0.1:8789
//   node tests/headers.mjs https://vuurspuwer.com
// Controleert: documenten kort met stale-while-revalidate, assets een jaar
// immutable (en NIET de HTML-cache erbij), 404 niet cachebaar, en de
// beveiligings-/preload-headers aanwezig.
const BASE = process.argv[2] || 'http://127.0.0.1:8789';
let fout = 0;
const eis = (naam, ok, detail = '') => { console.log(`${ok ? '  ok ' : ' FOUT'}  ${naam}${detail ? '  — ' + detail : ''}`); if (!ok) fout++; };

async function kop(pad) {
  const r = await fetch(BASE + pad, { method: 'GET', redirect: 'manual', headers: { 'Accept-Encoding': 'br, gzip' } });
  const h = {}; r.headers.forEach((v, k) => h[k] = v);
  return { status: r.status, h };
}

// 1. Document (HTML): korte cache met stale-while-revalidate + Link-preloads
{
  const { status, h } = await kop('/');
  const cc = h['cache-control'] || '';
  eis('home status 200', status === 200, String(status));
  eis('home HTML-cache = max-age=60 + swr', /max-age=60/.test(cc) && /stale-while-revalidate=86400/.test(cc), cc);
  eis('home HTML-cache NIET immutable/jaar', !/immutable/.test(cc) && !/31536000/.test(cc), cc);
  eis('home heeft Link-preload (Early Hints)', /rel=preload/.test(h['link'] || ''), (h['link'] || '').slice(0, 60));
  eis('home HSTS met preload', /preload/.test(h['strict-transport-security'] || ''), h['strict-transport-security'] || '');
  eis('home X-Content-Type-Options nosniff', (h['x-content-type-options'] || '') === 'nosniff');
}
// 2. Een /pad/-document (stad): zelfde contract
{
  const { status, h } = await kop('/vuurspuwer-boeken-in-amsterdam/');
  const cc = h['cache-control'] || '';
  eis('stad status 200', status === 200, String(status));
  eis('stad HTML-cache = max-age=60 + swr', /max-age=60/.test(cc) && /stale-while-revalidate/.test(cc), cc);
  eis('stad NIET immutable', !/immutable/.test(cc), cc);
}
// 3. Asset: een jaar immutable, en GEEN HTML-cache eroverheen
{
  const { h } = await kop('/assets/site.css');
  const cc = h['cache-control'] || '';
  eis('asset = 1 jaar immutable', /max-age=31536000/.test(cc) && /immutable/.test(cc), cc);
  eis('asset NIET de HTML-cache (max-age=60) erbij', !/max-age=60/.test(cc), cc);
}
// 4. Font: idem
{
  const { h } = await kop('/assets/fonts/archivo-latin.woff2');
  eis('font = 1 jaar immutable', /immutable/.test(h['cache-control'] || ''), h['cache-control'] || '');
}
// 5. sw.js: no-cache (moet altijd verversen)
{
  const { h } = await kop('/sw.js');
  eis('sw.js = no-cache', /no-cache/.test(h['cache-control'] || ''), h['cache-control'] || '');
}
// 6. 404: niet cachebaar
{
  const { status, h } = await kop('/deze-pagina-bestaat-niet-xyz/');
  const cc = h['cache-control'] || '';
  eis('404 status', status === 404, String(status));
  eis('404 niet-cachebaar (no-store/no-cache/max-age=0)', /no-store|no-cache|max-age=0/.test(cc) || cc === '', cc);
}
console.log(`\n${fout ? 'FOUT: ' + fout + ' controle(s) mislukt' : 'alle header-controles ok'}`);
process.exit(fout ? 1 : 0);
