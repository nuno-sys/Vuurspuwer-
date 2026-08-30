#!/usr/bin/env python3
"""Maakt de gebrandede deelafbeeldingen (og-*.jpg, 1200x630) en de
volledige icon-set voor Apple en Android."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

M = "assets/media"
LOGO = Image.open(os.path.join(M, "logo-mail.png")).convert("RGBA")

# basisfoto per paginatype -> og-<naam>.jpg
SOURCES = {
    "festival":   "festival-1600.webp",
    "avondvuur":  "avondvuur-1080.webp",
    "vuurbal":    "vuurbal-1333.webp",
    "vuurshow":   "vuurshow-850.webp",
    "workshop":   "workshop-1125.webp",
    "fakirshow":  "fakirshow-640.webp",
    "themafeest": "themafeest-1080.webp",
    "mentalist":  "mentalist-1371.webp",
    "reptiel":    "reptiel-960.webp",
    "post-cover": "post-cover.webp",
    "reel-1-poster": "reel-1-poster.webp",
}

def og_image(name, src):
    im = Image.open(os.path.join(M, src)).convert("RGB")
    # naar 1200x630: cover-crop rond het midden, iets naar boven
    tw, th = 1200, 630
    scale = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = max(0, round((im.height - th) * 0.38))
    im = im.crop((x, y, x + tw, y + th))
    im = ImageEnhance.Brightness(im).enhance(0.92)

    # donker verloop onderaan zodat het logo altijd leesbaar is
    grad = Image.new("L", (1, th))
    for j in range(th):
        k = max(0, (j / th - 0.45)) / 0.55
        grad.putpixel((0, j), int(200 * (k ** 1.4)))
    overlay = Image.new("RGB", (tw, th), (5, 3, 2))
    im = Image.composite(overlay, im, grad.resize((tw, th)))

    # het logo met gloed, linksonder, plus de sterrenregel
    lw = 340
    lh = round(LOGO.height * lw / LOGO.width)
    logo = LOGO.resize((lw, lh), Image.LANCZOS)
    glow = Image.new("RGBA", (lw + 80, lh + 80), (0, 0, 0, 0))
    glow.paste(logo, (40, 40), logo)
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    px, py = 56, th - lh - 64
    im.paste(Image.new("RGB", glow.size, (255, 90, 10)), (px - 40, py - 40), glow.split()[3].point(lambda a: a // 3))
    im.paste(logo, (px, py), logo)

    d = ImageDraw.Draw(im)
    # sterren + 4.9 als kleine gouden badge onder het logo
    sy = py + lh + 14
    for s in range(5):
        cx = px + 8 + s * 26
        d.polygon([(cx, sy), (cx + 4, sy + 8), (cx + 12, sy + 9), (cx + 6, sy + 15),
                   (cx + 8, sy + 24), (cx, sy + 19), (cx - 8, sy + 24), (cx - 6, sy + 15),
                   (cx - 12, sy + 9), (cx - 4, sy + 8)], fill=(255, 176, 32))
    out = os.path.join(M, f"og-{name}.jpg")
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  og-{name}.jpg  {os.path.getsize(out)//1024} KiB")

for name, src in SOURCES.items():
    og_image(name, src)

# ---------------------------------------------------------------- iconen
def flame_icon(size, pad_ratio=0.0, rounded=True):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if rounded:
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size * 14 // 64, fill=(10, 7, 5, 255))
    else:
        d.rectangle([0, 0, size, size], fill=(10, 7, 5, 255))
    pad = size * pad_ratio
    s = (size - 2 * pad) / 64
    ox = oy = pad
    def drop(cx, top, bottom, w, col):
        cx, top, bottom, w = ox + cx * s, oy + top * s, oy + bottom * s, w * s
        d.polygon([(cx, top), (cx + w, (top + bottom) / 2 + w * .4), (cx, bottom),
                   (cx - w, (top + bottom) / 2 + w * .4)], fill=col)
        d.ellipse([cx - w, (top + bottom) / 2 - w * .2, cx + w, bottom], fill=col)
    drop(32, 8, 52, 15, (255, 77, 10, 255))
    drop(32, 20, 51, 10, (255, 176, 32, 255))
    drop(31.5, 33, 49, 5.5, (255, 243, 214, 235))
    return im

flame_icon(192).save("assets/icon-192.png")
flame_icon(512).save("assets/icon-512.png")
# maskable: het vuurteken in de veilige zone, vlak zwart tot de rand
flame_icon(512, pad_ratio=0.12, rounded=False).save("assets/icon-maskable-512.png")
print("  iconen: 192, 512, maskable-512")
