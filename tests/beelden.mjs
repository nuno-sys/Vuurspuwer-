// Test: geen enkel beeld is kapot. Laadt de belangrijkste pagina's op
// mobiel en desktop, scrollt alles in beeld (lazy-loading) en eist dat
// elke <img> met een bron echt gedecodeerd is (naturalWidth > 0).
// Gebruik:  node tests/beelden.mjs [basis-url]   (standaard http://127.0.0.1:8429)
import { chromium } from 'playwright';
import fs from 'node:fs';
const LOG = process.env.BEELDEN_LOG;
const zeg = (m) => { console.log(m); if (LOG) fs.appendFileSync(LOG, m + '\n'); };
const BASE = process.argv[2] || 'http://127.0.0.1:8429';
const PADEN = ['/', '/wat-kost-een-vuurspuwer/', '/beoordelingen/', '/contact-3/', '/fotos/',
  '/vuurspuwer-boeken-in-amsterdam/', '/artiesten-boeken-tips/', '/blog/', '/en/', '/de/', '/fr/', '/zoeken/'];
const chrome = await chromium.launch({ executablePath: process.env.CHROME_PATH_PW || undefined, args: ['--no-sandbox'] });
let fouten = 0, totaal = 0;
for (const [w, h, m] of [[390, 844, true], [1440, 950, false]]) {
  const ctx = await chrome.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: m ? 2 : 1, isMobile: m });
  for (const pad of PADEN) {
    const p = await ctx.newPage();
    const jsFouten = []; p.on('pageerror', e => jsFouten.push(e.message));
    await p.goto(BASE + pad, { waitUntil: 'load' });
    await p.click('#cookieJa').catch(() => {});
    for (let y = 0; y < 40000; y += h * 0.8) {           // alles in beeld brengen
      const tot = await p.evaluate(() => document.documentElement.scrollHeight);
      if (y > tot) break;
      await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(90);
    }
    await p.waitForTimeout(600);
    const r = await p.evaluate(async () => {
      const imgs = [...document.images].filter(i => i.currentSrc || i.src);
      await Promise.all(imgs.map(i => i.decode().catch(() => {})));
      return { n: imgs.length, kapot: imgs.filter(i => !(i.naturalWidth > 0)).map(i => (i.currentSrc || i.src).slice(-70)) };
    });
    totaal += r.n; fouten += r.kapot.length + jsFouten.length;
    zeg(`${m ? 'mobiel ' : 'desktop'} ${pad.padEnd(34)} ${String(r.n).padStart(3)} beelden ${r.kapot.length ? 'KAPOT: ' + r.kapot.join(', ') : 'ok'}${jsFouten.length ? '  JS-FOUT: ' + jsFouten[0] : ''}`);
    await p.close();
  }
  await ctx.close();
}
await chrome.close();
zeg(`\n${totaal} beelden gecontroleerd, ${fouten} fout(en)`);
process.exit(fouten ? 1 : 0);
