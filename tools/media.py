#!/usr/bin/env python3
"""Zet de aangeleverde foto's om naar webformaten die snel laden.

Uit /media komen de originelen; hier gaan ze eruit als WebP op twee
breedtes, zodat de browser de kleinste kan kiezen die past.
"""
import os, shutil
from PIL import Image

SRC = "media"
DST = "assets/media"
WIDTHS = (1600, 900)

# bronbestand -> naam op de site, met de alt-tekst die erbij hoort
PLAN = {
    "vuurspuwer.jpg":
        ("festival", "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein"),
    "w=850.jpg":
        ("vuurshow", "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe"),
    "Wat-Is-De-Ideale-Kijkafstand-Voor-Het-Publiek-Het-Complete-Antwoord-door-Vuurspuwer-Nuno-vuurspuwer-Nuno.webp":
        ("vuurbal", "Meters hoge vuurbal tegen een zwarte nachtlucht"),
    "download.jpeg":
        ("themafeest", "Vuurspuwer bij een vintage bus tijdens een themafeest"),
    "Entertainer+Inhuren+Mentalist+Nuno.jpg":
        ("mentalist", "Nuno op het podium van een lege theaterzaal"),
    "Vuurspuwen+-+vuurspuwer+huren-640w.webp":
        ("schemering", "Vuurspuwen in de schemering, vlam breed uitwaaierend"),
    "Vuurshow-boeken-nuno.webp":
        ("workshop", "Vuurspuwer blaast een grote vuurbal tegen de avondlucht vanaf een balustrade"),
    "reptielenshow boeken.webp":
        ("reptiel", "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow"),
    "fakirshow-huren.jpg":
        ("fakirshow", "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer"),
    "spijkerbed-fakirshow-nuno.webp":
        ("spijkerbed", "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht"),
    "Vuurspuwer-huren-Nuno.webp":
        ("avondvuur", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
    "Kan-Ik-Vuurspuwer-Nuno-Boeken-Voor-Mijn-Bruiloft-Het-Complete-Antwoord-door-Vuurspuwer-Nuno-119283961_791034501663066_5861792144018564535_n.jpg.webp":
        ("bruiloft", "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels"),
}
# stond er al: de fakiract
KEEP = {"work-2.webp": ("fakir", "Fakiract: Nuno onder het gewicht van een staande toeschouwer")}

def variants(im, name, made, dst):
    """Schrijft alleen breedtes die kleiner zijn dan het origineel."""
    w0, h0 = im.size
    ws = [w for w in WIDTHS if w < w0] or []
    ws.append(min(w0, max(WIDTHS)))
    for w in sorted(set(ws)):
        out = im if w == w0 else im.resize((w, round(h0 * w / w0)), Image.LANCZOS)
        f = os.path.join(dst, f"{name}-{w}.webp")
        out.save(f, "WEBP", quality=82, method=6)
        made.append((f, os.path.getsize(f), out.size))


def main():
    os.makedirs(DST, exist_ok=True)
    made = []
    for src, (name, alt) in PLAN.items():
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            print("  ontbreekt:", src); continue
        variants(Image.open(p).convert("RGB"), name, made, DST)
    for src, (name, alt) in KEEP.items():
        p = os.path.join(DST, src)
        if not os.path.exists(p): continue
        variants(Image.open(p).convert("RGB"), name, made, DST)

    # omslag voor blogberichten: donker, alleen vuur en silhouet
    cover = Image.open(os.path.join(
        SRC, "Wat-Is-De-Ideale-Kijkafstand-Voor-Het-Publiek-Het-Complete-Antwoord-"
             "door-Vuurspuwer-Nuno-vuurspuwer-Nuno.webp")).convert("RGB")
    c = cover.resize((1200, round(cover.height * 1200 / cover.width)), Image.LANCZOS)
    c.save(os.path.join(DST, "post-cover.webp"), "WEBP", quality=84, method=6)
    c.save(os.path.join(DST, "post-cover.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    made.append((os.path.join(DST, "post-cover.webp"),
                 os.path.getsize(os.path.join(DST, "post-cover.webp")), c.size))

    for f, s, d in sorted(made):
        print(f"  {f:44s} {d[0]:>5}x{d[1]:<5} {s/1024:6.0f} kB")

if __name__ == "__main__":
    main()
