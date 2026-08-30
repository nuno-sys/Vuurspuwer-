#!/usr/bin/env python3
"""Maakt kleinere varianten voor srcset en perst de zwaarste bestanden
verder aan, zodat telefoons nooit meer bytes laden dan het scherm toont."""
import os
from PIL import Image

M = "assets/media"

def variant(src, width, out, q=72):
    p = os.path.join(M, src)
    im = Image.open(p)
    if im.width <= width:
        im.save(os.path.join(M, out), "WEBP", quality=q, method=6)
    else:
        h = round(im.height * width / im.width)
        im.resize((width, h), Image.LANCZOS).save(os.path.join(M, out), "WEBP", quality=q, method=6)
    print(f"  {out}: {os.path.getsize(os.path.join(M, out))//1024} KiB")

def recompress(src, q):
    p = os.path.join(M, src)
    before = os.path.getsize(p)
    Image.open(p).save(p, "WEBP", quality=q, method=6)
    print(f"  {src}: {before//1024} -> {os.path.getsize(p)//1024} KiB")

# 480-breed voor alle rasterfoto's (shows, galerij, fotopagina)
GRID = ["vuurshow-850", "fakirshow-640", "reptiel-900", "workshop-900",
        "mentalist-900", "themafeest-900", "festival-900", "vuurbal-900",
        "fakir-900", "avondvuur-900", "spijkerbed-900", "bruiloft-900",
        "schemering-640"]
for b in GRID:
    variant(b + ".webp", 480, b.rsplit("-", 1)[0] + "-480.webp")

# videoposters: alleen een plaatshouder, hoeft nooit 960 breed te zijn
variant("reel-1-poster.webp", 640, "reel-1-poster-640.webp", q=68)
variant("reel-2-poster.webp", 640, "reel-2-poster-640.webp", q=68)
variant("vuurbal-900.webp", 640, "vuurbal-640.webp", q=70)

# blogomslag: kaartformaat + tussenmaat voor de paginakop
variant("post-cover.webp", 480, "post-cover-480.webp", q=70)
variant("post-cover.webp", 900, "post-cover-900.webp", q=74)

# de twee bestanden die Lighthouse als te zwaar aanmerkt
recompress("vuurshow-850.webp", 68)
recompress("fakirshow-640.webp", 68)
