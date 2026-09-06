#!/usr/bin/env python3
"""Geen kapotte beelden — statische, browserloze controle.

Loopt door elke gebouwde HTML-pagina in dist/, verzamelt elke beeld-URL uit
src én srcset (ook uit <source>), en eist dat elk lokaal /assets/-beeld op
schijf bestaat én echte pixelafmetingen heeft. Dat is precies wat
naturalWidth > 0 in de browser zou garanderen, maar zonder browser en dus
snel en betrouwbaar in CI. De browservariant staat in tests/beelden.mjs.

Gebruik:  python3 tests/beelden.py        (verwacht een verse dist/)
"""
import re, glob, os, sys
from PIL import Image

refs = set()
for f in glob.glob("dist/**/*.html", recursive=True):
    h = open(f, encoding="utf-8").read()
    for m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"', h):
        refs.add(m.group(1))
    for m in re.finditer(r'\bsrcset="([^"]+)"', h):
        for part in m.group(1).split(","):
            u = part.strip().split(" ")[0]
            if u:
                refs.add(u)

local = sorted(u for u in refs if u.startswith("/assets/"))
ontbreekt, kapot, ok, maten = [], [], 0, {}
for u in local:
    p = "dist" + u.split("?")[0]
    if not os.path.exists(p):
        ontbreekt.append(u); continue
    try:
        if p not in maten:
            with Image.open(p) as im:
                maten[p] = im.size
        w, hh = maten[p]
        if w > 0 and hh > 0:
            ok += 1
        else:
            kapot.append(u)
    except Exception as e:
        kapot.append(f"{u} ({e})")

print(f"{len(local)} unieke lokale beeld-URLs, {ok} in orde")
if ontbreekt:
    print(f"ONTBREEKT op schijf ({len(ontbreekt)}):"); [print("  ", u) for u in ontbreekt]
if kapot:
    print(f"KAPOT / 0px ({len(kapot)}):"); [print("  ", u) for u in kapot]
sys.exit(1 if (ontbreekt or kapot) else 0)
