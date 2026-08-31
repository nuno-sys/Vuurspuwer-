#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Master-indexeerscript voor vuurspuwer.com.

Wat het doet:
  1. Haalt de live sitemap op en meldt ALLE adressen in één keer aan bij
     IndexNow (api.indexnow.org) — die verdeelt de melding zelf over Bing,
     DuckDuckGo, Yandex, Seznam en Naver. Bing voedt ook ChatGPT-search.
  2. Controleert dat sitemap, feed, llms.txt en robots.txt live bereikbaar
     zijn en de IndexNow-sleutel klopt.
  3. Schrijft gsc-plan.txt: een dag-voor-dag plan (10 URL's per dag, de
     limiet van Search Console) om de belangrijkste pagina's handmatig bij
     Google aan te melden — het enige deel dat Google niet automatisch
     aanneemt.

Gebruik:  python3 tools/indexeer.py
(Draait ook automatisch: de GitHub Action doet stap 1 bij elke push naar
main én elke maandagochtend.)
"""
import json, re, sys, urllib.request

SITE = "https://vuurspuwer.com"
KEY = "031a0a94dea279b0f3c9d84a5f39a7be"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "vuurspuwer-indexeer/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")

def main():
    print("── 1. Bereikbaarheid controleren")
    ok = True
    for pad in ("/sitemap.xml", "/feed.xml", "/llms.txt", "/robots.txt", f"/{KEY}.txt"):
        try:
            st, body = fetch(SITE + pad)
            extra = ""
            if pad.endswith(f"{KEY}.txt") and body.strip() != KEY:
                extra = "  ⚠ sleutelbestand klopt niet!"; ok = False
            print(f"   {st} {SITE}{pad}{extra}")
        except Exception as e:
            print(f"   ✗ {SITE}{pad}: {e}"); ok = False
    if not ok:
        print("   Los eerst de fouten hierboven op."); sys.exit(1)

    print("── 2. Sitemap inlezen")
    _, sm = fetch(SITE + "/sitemap.xml")
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    urls = [u for u in urls if "/assets/" not in u]
    prios = dict(re.findall(r"<loc>(.*?)</loc>.*?<priority>(.*?)</priority>", sm))
    print(f"   {len(urls)} pagina-adressen gevonden")

    print("── 3. IndexNow: alles aanmelden (Bing/DuckDuckGo/Yandex/Seznam/Naver)")
    payload = json.dumps({"host": "vuurspuwer.com", "key": KEY,
                          "keyLocation": f"{SITE}/{KEY}.txt",
                          "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"   ✓ IndexNow antwoordde {r.status} — {len(urls)} URL's aangemeld")
    except Exception as e:
        print(f"   ✗ IndexNow-melding mislukt: {e}")

    print("── 4. Google-dagplan schrijven (gsc-plan.txt)")
    def rang(u):
        p = float(prios.get(u, "0.5"))
        pad = u.replace(SITE, "")
        boost = 0.05 if pad.count("/") <= 2 else 0
        return -(p + boost)
    top = sorted(urls, key=rang)
    dagen = [top[i:i+10] for i in range(0, min(len(top), 140), 10)]
    with open("gsc-plan.txt", "w", encoding="utf-8") as f:
        f.write("GOOGLE SEARCH CONSOLE — DAGPLAN\n"
                "================================\n"
                "Google accepteert ±10 handmatige indexeringsverzoeken per dag.\n"
                "Doe elke dag één blokje: URL-inspectie → URL plakken →\n"
                "'Indexering aanvragen'. Belangrijkste pagina's eerst.\n\n")
        for i, blok in enumerate(dagen, 1):
            f.write(f"── Dag {i} ──\n" + "\n".join(blok) + "\n\n")
    print(f"   ✓ gsc-plan.txt: {len(dagen)} dagen × 10 URL's, belangrijkste eerst")
    print("\nKlaar. Bing & co zijn automatisch gepind; het Google-deel staat in gsc-plan.txt.")

if __name__ == "__main__":
    main()
