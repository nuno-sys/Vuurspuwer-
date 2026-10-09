#!/usr/bin/env python3
"""Sjabloontekst tussen stadspagina's.

De oude site had 358 stadspagina's met dezelfde tekst en een andere
plaatsnaam; daar is hij op 21 augustus 2026 op afgestraft. Deze test legt
alle stads- en regiopagina's per taal naast elkaar en meldt elke zin van
acht of meer woorden die letterlijk op twee pagina's staat. De vaste
onderdelen van de site (menu, voettekst, offerte-strook, FAQ-kop) tellen
niet mee: alleen de tekst binnen <main>.
"""
import os, re, sys, collections
DIST = os.path.join(os.path.dirname(__file__), "..", "dist")
SETS = {
 "nl": re.compile(r"^vuurspuwer-boeken-in-"),
 "de": re.compile(r"^de/feuerspucker-(?!kosten|workshop)"),
 "fr": re.compile(r"^fr/cracheur-de-feu-"),
}
def zinnen(html):
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S)
    t = m.group(1) if m else html
    t = re.sub(r"<(script|style|nav|aside|form|details)[^>]*>.*?</\1>", " ", t, flags=re.S)
    # de vaste blokken onder de tekst (offerte-wizard, prijsstrook, FAQ-kop,
    # fotorij, gelegenheidslinks) horen bij het ontwerp, niet bij de tekst
    t = re.sub(r'<section class="(?:wrap bay|bay wrap)[^"]*"[^>]*>.*?</section>', " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t)
    out = set()
    for z in re.split(r"(?<=[.!?])\s+", t):
        w = z.strip().split()
        if len(w) >= 8: out.add(" ".join(w).lower())
    return out
fouten = 0
for lang, rx in SETS.items():
    paginas = {}
    for root, _, files in os.walk(DIST):
        if "index.html" not in files: continue
        slug = os.path.relpath(root, DIST).replace(os.sep, "/")
        if rx.match(slug):
            paginas[slug] = zinnen(open(os.path.join(root, "index.html"), encoding="utf-8").read())
    waar = collections.defaultdict(set)
    for slug, zs in paginas.items():
        for z in zs: waar[z].add(slug)
    dubbel = {z: s for z, s in waar.items() if len(s) > 1}
    # een zin die op álle pagina's staat is geen bouwsteen maar hét sjabloon
    echt = dubbel
    print(f"{lang}: {len(paginas)} pagina's, {len(echt)} gedeelde zinnen")
    for z, s in sorted(echt.items(), key=lambda x: -len(x[1]))[:40]:
        print(f"  ✖ op {len(s)} pagina's: “{z[:110]}…”  ({', '.join(sorted(s))[:120]})")
    fouten += len(echt)
print(f"sjabloon: {'in orde' if not fouten else str(fouten) + ' gedeelde zin(nen)'}")
sys.exit(1 if fouten else 0)
