#!/usr/bin/env python3
"""Bouwt de statische site uit de WordPress-export.

Leest de export, kiest de 20 stadspagina's, de blogposts en de vaste
pagina's, en schrijft voor elk een map met een index.html in het ontwerp
van de homepage. Webadressen blijven exact zoals ze nu zijn.
"""
import html, json, os, re, shutil, sys
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser

import pages_content as PC

TODAY = date.today().isoformat()
MONTHS_NL = ["", "januari", "februari", "maart", "april", "mei", "juni", "juli",
             "augustus", "september", "oktober", "november", "december"]
TODAY_NL = f"{date.today().day} {MONTHS_NL[date.today().month]} {date.today().year}"

XML  = "nunovuurspuwer-vuurshowsampfakirshowenworkshops.WordPress.2026-08-30.xml"
OUT  = "dist"
SITE = "https://vuurspuwer.com"
NS = {'wp': 'http://wordpress.org/export/1.2/',
      'content': 'http://purl.org/rss/1.0/modules/content/'}

CITIES = [
    "vuurspuwer-boeken-in-amsterdam", "vuurspuwer-boeken-in-rotterdam",
    "vuurspuwer-boeken-in-den-haag", "vuurspuwer-boeken-in-utrecht-2",
    "vuurspuwer-boeken-in-eindhoven", "vuurspuwer-boeken-in-groningen",
    "vuurspuwer-boeken-in-tilburg", "vuurspuwer-boeken-in-breda",
    "vuurspuwer-boeken-in-antwerpen", "vuurspuwer-boeken-in-gent",
    "vuurspuwer-boeken-in-brussel", "vuurspuwer-boeken-in-brugge",
    "vuurspuwer-boeken-in-leuven", "vuurspuwer-boeken-in-liege",
    "vuurspuwer-boeken-in-mechelen",
    "spectaculaire-vuurspuwer-aachen-maak-uw-evenement-in-de-keizerstad-onvergetelijk",
    "vuurspuwer-inhuren-in-krefeld-een-vlammend-spektakel-voor-uw-event",
    "vuurspuwer-monchengladbach-spectaculaire-vuurshows-net-over-de-grens",
    "vuurspuwer-inhuren-in-kaldenkirchen-spectaculair-entertainment-in-de-grensregio",
    "vuurspuwer-inhuren-in-kleve-breng-vurige-magie-naar-de-grensregio",
]
CITY_LABEL = {
    "vuurspuwer-boeken-in-amsterdam": "Amsterdam", "vuurspuwer-boeken-in-rotterdam": "Rotterdam",
    "vuurspuwer-boeken-in-den-haag": "Den Haag", "vuurspuwer-boeken-in-utrecht-2": "Utrecht",
    "vuurspuwer-boeken-in-eindhoven": "Eindhoven", "vuurspuwer-boeken-in-groningen": "Groningen",
    "vuurspuwer-boeken-in-tilburg": "Tilburg", "vuurspuwer-boeken-in-breda": "Breda",
    "vuurspuwer-boeken-in-antwerpen": "Antwerpen", "vuurspuwer-boeken-in-gent": "Gent",
    "vuurspuwer-boeken-in-brussel": "Brussel", "vuurspuwer-boeken-in-brugge": "Brugge",
    "vuurspuwer-boeken-in-leuven": "Leuven", "vuurspuwer-boeken-in-liege": "Luik",
    "vuurspuwer-boeken-in-mechelen": "Mechelen",
    "spectaculaire-vuurspuwer-aachen-maak-uw-evenement-in-de-keizerstad-onvergetelijk": "Aachen",
    "vuurspuwer-inhuren-in-krefeld-een-vlammend-spektakel-voor-uw-event": "Krefeld",
    "vuurspuwer-monchengladbach-spectaculaire-vuurshows-net-over-de-grens": "Mönchengladbach",
    "vuurspuwer-inhuren-in-kaldenkirchen-spectaculair-entertainment-in-de-grensregio": "Kaldenkirchen",
    "vuurspuwer-inhuren-in-kleve-breng-vurige-magie-naar-de-grensregio": "Kleve",
}
# pagina's die blijven bestaan naast de shows op de homepage
KEEP_PAGES = ["over-nuno", "contact-3", "beoordelingen", "disclaimer-voorwaarden",
              "privacybeleid", "fotos", "videos", "blog",
              "locaties-vuurshows-nederland-belgie", "entertainer-huren",
              "vuurspuwer-inhuren", "fakir-show-inhuren", "reptielenhow",
              "workshop-vuurspuwen", "entertainer-huren-voor-bedrijfsfeest"]

# ---------------------------------------------------------------- opschonen
ALLOWED = {"p","h2","h3","h4","ul","ol","li","strong","em","b","i","a","br",
           "blockquote","figure","figcaption","img","table","thead","tbody","tr","th","td"}
KEEP_ATTR = {"a": {"href"}, "img": {"src", "alt", "width", "height"}}

class Clean(HTMLParser):
    """Houdt alleen betekenisvolle opmaak over en gooit thema-rommel weg."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip = [], [], 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "iframe"): self.skip += 1; return
        if self.skip or tag not in ALLOWED: return
        keep = KEEP_ATTR.get(tag, set())
        a = "".join(f' {k}="{html.escape(v or "", quote=True)}"' for k, v in attrs if k in keep)
        if tag == "img": a += ' loading="lazy" decoding="async"'
        self.out.append(f"<{tag}{a}>")
        if tag not in ("br", "img"): self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in ("script", "style", "iframe"):
            self.skip = max(0, self.skip - 1); return
        if self.skip or tag not in ALLOWED or tag in ("br", "img"): return
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f"</{t}>")
                if t == tag: break
    def handle_data(self, d):
        if not self.skip: self.out.append(html.escape(d, quote=False))
    def result(self):
        while self.stack: self.out.append(f"</{self.stack.pop()}>")
        return "".join(self.out)

def clean_html(raw):
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)          # Gutenberg-commentaar
    raw = re.sub(r"\[/?[a-z0-9_\-]+[^\]]*\]", "", raw, re.I)  # shortcodes
    # uploads verhuizen mee: zelfde pad, straks op Cloudflare zelf.
    # Tot de uploads-map er is verbergt site.js afbeeldingen die nog 404'en.
    raw = re.sub(r"https?://(?:www\.)?vuurspuwer\.com/wp-content/", "/wp-content/", raw)
    c = Clean(); c.feed(raw)
    out = c.result()
    out = re.sub(r"<p>\s*</p>", "", out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()

def text_of(h, limit=None):
    t = re.sub(r"<[^>]+>", " ", h)
    t = html.unescape(re.sub(r"\s+", " ", t)).strip()
    if not limit or len(t) <= limit: return t
    cut = t[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,.;:") + "\u2026"

print("export lezen…")
channel = ET.parse(XML).getroot().find("channel")
items = channel.findall("item")

def meta(i):
    d = {}
    for m in i.findall("wp:postmeta", namespaces=NS):
        k = m.findtext("wp:meta_key", namespaces=NS)
        if k: d[k] = m.findtext("wp:meta_value", namespaces=NS) or ""
    return d

# bijlage-id -> URL, zodat de uitgelichte afbeelding erbij komt
ATT = {}
for i in items:
    if i.findtext("wp:post_type", namespaces=NS) == "attachment":
        pid = i.findtext("wp:post_id", namespaces=NS)
        url = i.findtext("wp:attachment_url", namespaces=NS)
        alt = ""
        for m in i.findall("wp:postmeta", namespaces=NS):
            if m.findtext("wp:meta_key", namespaces=NS) == "_wp_attachment_image_alt":
                alt = m.findtext("wp:meta_value", namespaces=NS) or ""
        if pid and url: ATT[pid] = (url, alt or html.unescape((i.findtext("title") or "").strip()))

pages = {}
for i in items:
    if i.findtext("wp:status", namespaces=NS) != "publish": continue
    if i.findtext("wp:post_type", namespaces=NS) not in ("page", "post"): continue
    slug = re.sub(r"^https?://[^/]+/", "", i.findtext("link") or "").strip("/")
    if not slug: continue
    m = meta(i)
    pages[slug] = {
        "slug": slug,
        "kind": i.findtext("wp:post_type", namespaces=NS),
        "title": html.unescape((i.findtext("title") or "").strip()),
        "date": (i.findtext("wp:post_date", namespaces=NS) or "")[:10],
        "body": clean_html(i.findtext("content:encoded", namespaces=NS) or ""),
        "seo_title": html.unescape(m.get("_yoast_wpseo_title", "")).replace("%%sep%%", "|").replace("%%sitename%%", "Vuurspuwer Nuno").replace("%%title%%", html.unescape((i.findtext("title") or "").strip())).strip(),
        "seo_desc": html.unescape(m.get("_yoast_wpseo_metadesc", "")).strip(),
        "img": ATT.get(m.get("_thumbnail_id", "")),
    }
print(f"  {len(pages)} gepubliceerde pagina's in de export")
json.dump({"count": len(pages)}, open("/tmp/_pages.json", "w"))

# ------------------------------------------------------- gedeelde onderdelen
src = open("index.html", encoding="utf-8").read()
def chunk(a, b):
    i = src.index(a); j = src.index(b, i)
    return src[i:j]

IGNITION = chunk('<div id="ignition"', '<!-- ============================================================\n     Ambient stage')
STAGE    = chunk('<div class="stage" aria-hidden="true">', '<main class="shell"')
HEADER   = STAGE[STAGE.index('<header class="nav"'):]
STAGE    = STAGE[:STAGE.index('<header class="nav"')]
# op een onderliggende pagina wijzen de ankers terug naar de homepage
HEADER   = HEADER.replace('href="#', 'href="/#')
FOOTER   = chunk('<footer class="foot shell wrap">', '<script src="/assets/site.js"') 
# versie-stempel voor css/js: /assets/* staat een jaar immutable in de
# cache, dus elke wijziging krijgt een nieuw adres via ?v=…
import hashlib
VER = hashlib.md5(b"".join(open(f"assets/{f}", "rb").read()
                           for f in ("site.css", "site.js", "ga.js"))).hexdigest()[:10]

GTAG = f'<script src="/assets/ga.js?v={VER}" defer></script>'
# zelf gehoste fonts: alleen de twee gezichten die boven de vouw staan
# vooraf laden; de @font-face-regels zitten in site.css zelf.
FONTS    = ('<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin.woff2" crossorigin>'
            '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/instrument-latin.woff2" crossorigin>')

def esc(t): return html.escape(t or "", quote=True)

def srcset_of(iu):
    """Zoekt de -480/-640/-900/…-broertjes van een media-bestand op schijf
    en bouwt daar een srcset van, zodat telefoons de kleine variant laden."""
    m = re.match(r"/assets/media/([a-z0-9-]+?)-(\d+)\.webp$", iu or "")
    if iu == "/assets/media/post-cover.webp":
        return ("/assets/media/post-cover-480.webp 480w, "
                "/assets/media/post-cover-900.webp 900w, "
                "/assets/media/post-cover.webp 1200w")
    if not m: return ""
    base = m.group(1)
    cands = sorted(
        (int(mm.group(1)), f"/assets/media/{f}")
        for f in os.listdir("assets/media")
        if (mm := re.match(rf"{re.escape(base)}-(\d+)\.webp$", f)))
    if len(cands) < 2: return ""
    return ", ".join(f"{u} {w}w" for w, u in cands)

def crumbs(items):
    li = "".join(
        f'<li><a href="{esc(u)}">{esc(n)}</a></li>' if u else f'<li><span aria-current="page">{esc(n)}</span></li>'
        for n, u in items)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": k + 1, "name": n,
                                 **({"item": SITE + u} if u else {})}
                                for k, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Kruimelpad"><ol>{li}</ol></nav>', data

def render(p, kind, extra_schema=None, extra_html=""):
    title = p["seo_title"] or f'{p["title"]} | Vuurspuwer Nuno'
    desc  = p["seo_desc"] or text_of(p["body"], 155)
    url   = f'{SITE}/{p["slug"]}/'
    trail = [("Home", "/")]
    if kind == "post":   trail.append(("Blog", "/blog/"))
    elif kind == "city": trail.append(("Locaties", "/locaties-vuurshows-nederland-belgie/"))
    trail.append((p["title"], None))
    crumb_html, crumb_data = crumbs(trail)

    # een korte eigen intro: de eerste alinea, tenzij die de titel herhaalt
    first = re.search(r"<p>(.*?)</p>", p["body"], re.S)
    intro = text_of(first.group(1), 190) if first else ""
    if intro and intro.lower().startswith(p["title"][:24].lower()):
        intro = ""

    if p.get("img"):
        iu, ia = p["img"]
        iu = re.sub(r"https?://(?:www\.)?vuurspuwer\.com/wp-content/", "/wp-content/", iu)
        if iu.startswith("/wp-content/") and not os.path.exists(iu.lstrip("/")):
            fallbacks = ["/assets/media/festival-1600.webp",
                         "/assets/media/vuurbal-1333.webp",
                         "/assets/media/vuurshow-850.webp",
                         "/assets/media/themafeest-1080.webp"]
            iu = fallbacks[sum(map(ord, p["slug"])) % len(fallbacks)]
            ia = ia or "Vuurspuwer Nuno tijdens een vuurshow"
        p = {**p, "img": (iu, ia)}

    # elk blogbericht draagt dezelfde omslag: donker, alleen Nuno en de vlam
    if kind == "post":
        p = {**p, "img": ("/assets/media/post-cover.webp",
                          "Vuurspuwer Nuno met een metershoge vuurbal tegen een zwarte nachtlucht")}

    # De kop van elke pagina: de uitgelichte foto beeldvullend, tot achter
    # het menu, en nooit bijgesneden — de foto zelf past er volledig in
    # (contain), met dezelfde foto wazig als decor eromheen (cover).
    eyebrow = p.get("eyebrow") or ("Vuurshow op locatie" if kind == "city"
                                   else "Blog" if kind == "post" else "Vuurspuwer Nuno")
    preload = ""
    if p.get("img"):
        iu, ia = p["img"]
        ss = srcset_of(iu)
        ss_attr = f' srcset="{ss}" sizes="100vw"' if ss else ""
        pre_ss = f' imagesrcset="{ss}" imagesizes="100vw"' if ss else ""
        preload = f'<link rel="preload" as="image" href="{esc(iu)}"{pre_ss} fetchpriority="high">'
        hero = f'''<header class="phero">
    <div class="phero__bg" style="background-image:url('{esc(iu)}')" aria-hidden="true"></div>
    <img class="phero__img" src="{esc(iu)}"{ss_attr} alt="{esc(ia)}" fetchpriority="high" decoding="async">
    <div class="phero__veil" aria-hidden="true"></div>
    <div class="phero__body wrap">
      {crumb_html}
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h1 class="page__title">{esc(p["title"])}</h1>
      {f'<p class="lede">{esc(intro)}</p>' if intro else ''}
    </div>
  </header>'''
    else:
        hero = f'''<article class="page wrap">
    {crumb_html}
    <p class="eyebrow">{esc(eyebrow)}</p>
    <h1 class="page__title">{esc(p["title"])}</h1>
    {f'<p class="lede">{esc(intro)}</p>' if intro else ''}
  </article>'''

    graph = [crumb_data]
    if kind == "post":
        graph.append({"@context": "https://schema.org", "@type": "BlogPosting",
                      "headline": p["title"], "datePublished": p["date"],
                      "dateModified": TODAY,
                      "description": desc, "mainEntityOfPage": url,
                      **({"image": (SITE + p["img"][0] if p["img"][0].startswith("/") else p["img"][0])} if p.get("img") else {}),
                      "author": {"@type": "Person", "name": "Nuno", "@id": f"{SITE}/#nuno"},
                      "publisher": {"@id": f"{SITE}/#business"}})
    if extra_schema:
        graph.extend(extra_schema) if isinstance(extra_schema, list) else graph.append(extra_schema)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>' for g in graph)

    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0A0705">
{GTAG}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'article' if kind == 'post' else 'website'}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{(SITE + p["img"][0] if p["img"][0].startswith("/") else p["img"][0]) if p.get("img") else SITE + "/assets/media/festival-1600.webp"}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{preload}
{ld}
</head>
<body>
<a class="skip" href="#top">Naar de inhoud</a>
{IGNITION}{STAGE}{HEADER}
<main class="shell" id="top">
  {hero}

  <div class="wrap bay">
    <div class="prose prose--page">
{p["body"]}
    </div>
  </div>
{extra_html}
  <section class="wrap bay cta">
    <h2 class="bay__title">Check je <em>datum</em></h2>
    <p class="lede">Bel of app even, dan weet je binnen een minuut of het kan.</p>
    <div class="hero__actions">
      <a class="btn" href="tel:+31620020723"><span class="btn__dot"></span>+31 6 200 207 23</a>
      <a class="btn btn--ghost" href="https://wa.me/31620020723">WhatsApp direct</a>
      <a class="btn btn--ghost" href="/contact-3/">Stuur een aanvraag</a>
    </div>
  </section>
</main>
{FOOTER}
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''

def write(slug, doc):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)


# ------------------------------------------------- de fotopagina
# Eigen galerij in plaats van de oude WordPress-inhoud: alle foto's,
# klik opent de lightbox, en elke foto staat als ImageObject in de markup.
FOTOS = [
    ("festival",   "festival-900.webp",   "festival-1600.webp",  900, 902,
     "Complete vuurshow op een festivalplein",
     "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek"),
    ("vuurbal",    "vuurbal-900.webp",    "vuurbal-1333.webp",   900, 1350,
     "Vuurbal tijdens een nachtshow",
     "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
    ("avondvuur",  "avondvuur-900.webp",  "avondvuur-1080.webp", 900, 893,
     "Vuurbal in de avondschemering",
     "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
    ("vuurshow",   "vuurshow-850.webp",   "vuurshow-850.webp",   850, 1024,
     "Vuurshow bij daglicht op een zomerfestival",
     "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe"),
    ("workshop",   "workshop-900.webp",   "workshop-1125.webp",  900, 1130,
     "Vuurspuwen tegen de avondlucht",
     "Vuurspuwer blaast een grote vuurbal tegen de avondlucht vanaf een balustrade"),
    ("schemering", "schemering-640.webp", "schemering-640.webp", 640, 423,
     "Vuurspuwen in de schemering",
     "Vuurspuwen in de schemering, de vlam waaiert breed uit tegen een blauwe lucht"),
    ("themafeest", "themafeest-900.webp", "themafeest-1080.webp", 900, 1125,
     "Themafeest met vuur bij de vintage bus",
     "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond"),
    ("bruiloft",   "bruiloft-900.webp",   "bruiloft-1080.webp",  900, 1014,
     "Duo-act met danseres op een bruiloft",
     "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels"),
    ("fakirshow",  "fakirshow-640.webp",  "fakirshow-640.webp",  640, 1351,
     "Fakirshow in het theater",
     "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer"),
    ("fakir",      "fakir-900.webp",      "fakir-1080.webp",     900, 1124,
     "Fakiract met glas en gewicht",
     "Fakiract: Nuno draagt het gewicht van een staande toeschouwer"),
    ("spijkerbed", "spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873,
     "Het spijkerbord van dichtbij",
     "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht"),
    ("reptiel",    "reptiel-900.webp",    "reptiel-960.webp",    900, 838,
     "Reptielenshow met boa constrictor",
     "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow"),
    ("mentalist",  "mentalist-900.webp",  "mentalist-1371.webp", 900, 900,
     "Mentalist Nuno in het theater",
     "Nuno op het podium van een lege theaterzaal voor een mentalismeshow"),
]

def fotos_body():
    tiles = []
    for _, thumb, full, w, h, cap, alt in FOTOS:
        ss = srcset_of(f"/assets/media/{thumb}")
        ss_attr = f' srcset="{ss}" sizes="(max-width:760px) 46vw, 31vw"' if ss else ""
        tiles.append(
            f'<a href="/assets/media/{full}" data-lightbox data-cap="{esc(cap)}">'
            f'<img src="/assets/media/{thumb}"{ss_attr} width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="{esc(alt)}"></a>')
    return ('<p>Een greep uit de shows van de afgelopen jaren: vuurshows op festivals '
            'en bedrijfsfeesten, fakirshows in het theater, de reptielenshow en optredens '
            'op bruiloften en themafeesten. Klik op een foto om hem groot te bekijken &mdash; '
            'of <a href="/#boeken">vraag direct een offerte aan</a>.</p>'
            '<div class="fgrid">' + "".join(tiles) + "</div>")

def fotos_schema():
    return {"@context": "https://schema.org", "@type": "ImageGallery",
            "name": "Foto's van Vuurspuwer Nuno",
            "url": f"{SITE}/fotos/",
            "about": {"@id": f"{SITE}/#business"},
            "image": [{"@type": "ImageObject",
                       "contentUrl": f"{SITE}/assets/media/{full}",
                       "thumbnail": f"{SITE}/assets/media/{thumb}",
                       "name": cap, "description": alt,
                       "creditText": "Vuurspuwer Nuno",
                       "copyrightNotice": "\u00a9 Vuurspuwer Nuno"}
                      for _, thumb, full, _, _, cap, alt in FOTOS]}

# ------------------------------------------------------------------ bouwen
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
built, missing = [], []

for slug in CITIES:
    p = pages.get(slug)
    if not p: missing.append(slug); continue
    city = CITY_LABEL[slug]
    others = [(CITY_LABEL[s], s) for s in CITIES if s != slug][:8]
    near = ('<section class="wrap bay"><h2 class="bay__title">Ook in de <em>buurt</em></h2>'
            '<ul class="citylist">' +
            "".join(f'<li><a href="/{s}/">Vuurspuwer in {n}</a></li>' for n, s in others) +
            "</ul></section>")
    svc = {"@context": "https://schema.org", "@type": "Service",
           "name": f"Vuurspuwer inhuren in {city}", "serviceType": "Vuurshow",
           "provider": {"@id": f"{SITE}/#business"},
           "areaServed": {"@type": "City", "name": city},
           "url": f"{SITE}/{slug}/"}
    write(slug, render(p, "city", svc, near)); built.append(slug)

posts = [p for p in pages.values() if p["kind"] == "post"]
for p in posts:
    # workshop-vuurspuwen is in de export een bericht, maar leeft op de
    # site als volwaardige showpagina — die komt uit KEEP_PAGES.
    if p["slug"] in PC.SHOW_PAGES: continue
    write(p["slug"], render(p, "post")); built.append(p["slug"])

for slug in KEEP_PAGES:
    p = pages.get(slug)
    if not p: missing.append(slug); continue
    if slug == "videos":
        p = {**p, "title": "Video's van de shows",
             "seo_title": "Video's | Vuurshow & fakirshow in actie | Vuurspuwer Nuno",
             "seo_desc": "Bekijk video's van de vuurshows, fakiracts en optredens van Vuurspuwer Nuno. Showreels van festivals, bedrijfsfeesten en evenementen in Nederland en België.",
             "body": PC.videos_body(),
             "eyebrow": "Video's",
             "img": ("/assets/media/reel-1-poster.webp",
                     "Vuurspuwer Nuno tijdens een vuurshow op locatie")}
        write(slug, render(p, "page", PC.videos_schema()))
        built.append(slug); continue
    if slug in PC.SHOW_PAGES:
        sp = PC.SHOW_PAGES[slug]
        p = {**p, "title": sp["title"], "seo_title": sp["seo_title"],
             "seo_desc": sp["seo_desc"], "body": sp["body"], "img": sp["img"],
             "eyebrow": sp["eyebrow"]}
        extra = PC.show_faq_html(sp)
        if sp["fotos"]:
            extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                      + PC._fotorij(sp["fotos"]) + "</div></section>")
        write(slug, render(p, "page", PC.show_schema(slug, sp), extra))
        built.append(slug); continue
    if slug == "fotos":
        p = {**p, "title": "Foto's van de shows",
             "seo_title": "Foto's | Vuurshow, fakirshow & reptielenshow | Vuurspuwer Nuno",
             "seo_desc": "Bekijk foto's van de vuurshows, fakirshows, reptielenshow en workshops van Vuurspuwer Nuno op festivals, bedrijfsfeesten en bruiloften in Nederland en België.",
             "body": fotos_body(),
             "eyebrow": "Foto's",
             "img": ("/assets/media/festival-1600.webp",
                     "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein")}
        write(slug, render(p, "page", fotos_schema()))
        built.append(slug); continue
    if slug == "beoordelingen":
        p = {**p, "title": "4,9 uit 134 beoordelingen",
             "seo_title": "⭐ Reviews Vuurspuwer Nuno — 4.9/5 uit 134 beoordelingen",
             "seo_desc": "Lees beoordelingen van opdrachtgevers uit heel NL & BE over de vuurshows en fakirshows van Nuno. Gemiddeld 4.9/5 uit 134 reviews.",
             "body": PC.reviews_body(),
             "eyebrow": "Beoordelingen",
             "img": ("/assets/media/festival-1600.webp",
                     "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek")}
        write(slug, render(p, "page", PC.reviews_schema()))
        built.append(slug); continue
    if slug == "contact-3":
        p = {**p, "title": "Samenwerken met Nuno? Check je datum",
             "seo_title": "\U0001F525 Contact | Vuurspuwer Nuno boeken — binnen 24 uur antwoord",
             "seo_desc": "Vuurshow, fakirshow of workshop boeken? Bel, app of mail Nuno, of stuur het aanvraagformulier met datum en locatie. Binnen 24 uur een vrijblijvende offerte.",
             "body": PC.contact_body(),
             "eyebrow": "Contact",
             "img": ("/assets/media/themafeest-1080.webp",
                     "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond")}
        write(slug, render(p, "page", PC.contact_schema(), PC.CONTACT_FORM))
        built.append(slug); continue
    if slug == "blog":
        cards = []
        for bp in sorted(posts, key=lambda x: x["date"], reverse=True):
            if bp["slug"] in PC.SHOW_PAGES: continue
            excerpt = text_of(bp["body"], 150)
            cards.append(
                f'<article class="bcard"><a href="/{bp["slug"]}/">'
                f'<img src="/assets/media/post-cover-480.webp" '
                f'srcset="/assets/media/post-cover-480.webp 480w, /assets/media/post-cover-900.webp 900w" '
                f'sizes="(max-width:700px) 92vw, 340px" alt="" width="480" height="720" loading="lazy" decoding="async">'
                f'<h2>{esc(bp["title"])}</h2></a>'
                f'<p>{esc(excerpt)}</p>'
                f'<p class="bcard__meta"><time datetime="{TODAY}">Bijgewerkt op {TODAY_NL}</time></p>'
                f'</article>')
        blog_posts = [bp for bp in sorted(posts, key=lambda x: x["date"], reverse=True)
                      if bp["slug"] not in PC.SHOW_PAGES]
        blog_ld = [{"@context": "https://schema.org", "@type": "Blog",
                    "@id": f"{SITE}/blog/#blog", "url": f"{SITE}/blog/",
                    "name": "Blog van Vuurspuwer Nuno", "dateModified": TODAY,
                    "publisher": {"@id": f"{SITE}/#business"},
                    "blogPost": [{"@type": "BlogPosting",
                                  "headline": bp["title"],
                                  "url": f"{SITE}/{bp['slug']}/",
                                  "datePublished": bp["date"],
                                  "dateModified": TODAY}
                                 for bp in blog_posts]}]
        p = {**p, "title": "Blog: gidsen, tips & inspiratie",
             "seo_title": "\U0001F525 Blog | Gidsen & tips over vuurshows | Vuurspuwer Nuno",
             "seo_desc": "Gidsen en tips over vuurshows, fakirshows en entertainment boeken: prijzen, veiligheid, Halloween, bruiloften en bedrijfsfeesten. Door vuurspuwer Nuno.",
             "body": ('<p>Gidsen, tips en inspiratie uit de praktijk: wat kost een vuurshow, '
                      'waar let je op qua veiligheid, en hoe maak je van een bedrijfsfeest, '
                      'bruiloft of Halloween-avond iets onvergetelijks. Alle artikelen zijn '
                      f'bijgewerkt op {TODAY_NL}.</p><div class="bloglist">' + "".join(cards) + "</div>"),
             "eyebrow": "Blog",
             "img": ("/assets/media/post-cover.webp",
                     "Vuurspuwer Nuno met een metershoge vuurbal tegen een zwarte nachtlucht")}
        write(slug, render(p, "page", blog_ld))
        built.append(slug); continue
    write(slug, render(p, "page")); built.append(slug)

hp = PC.SHOW_PAGES["halloween"]
p = {"slug": "halloween", "kind": "page", "title": hp["title"],
     "date": "2026-08-30", "body": hp["body"],
     "seo_title": hp["seo_title"], "seo_desc": hp["seo_desc"], "img": hp["img"]}
extra = PC.show_faq_html(hp)
extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
          + PC._fotorij(hp["fotos"]) + "</div></section>")
write("halloween", render(p, "page", PC.show_schema("halloween", hp), extra))
built.append("halloween")

print(f"  {len(built)} pagina's gebouwd  ({len(CITIES)} steden, {len(posts)} blogposts)")
if missing: print("  niet gevonden:", ", ".join(missing))
json.dump(built, open("/tmp/_built.json", "w"))

# ------------------------------------------- doorverwijzingen en sitemap
kept = set(built)
lines = ["# oude adressen die blijven werken", "",
         # het kanonieke contactadres is /contact-3/ (zo heet het op de
         # live site); alle andere contact-varianten wijzen daarheen
         "/contact/  /contact-3/  301"]

# 1. dubbelingen naar het origineel zonder cijfer
for slug in pages:
    base = re.sub(r"-\d+$", "", slug)
    if base != slug and base in kept:
        lines.append(f"/{slug}/  /{base}/  301")
    elif base in ("contact", "contact-me") and slug not in kept:
        lines.append(f"/{slug}/  /contact-3/  301")

# 2. stadspagina's die niet meegaan, naar de locatiepagina
HUB = "/locaties-vuurshows-nederland-belgie/"
dropped = 0
for slug, p in pages.items():
    if slug in kept: continue
    if re.search(r"vuurspuw|vuurshow", slug) and re.search(r"boeken|inhuren|huren|in-", slug):
        lines.append(f"/{slug}/  {HUB}  301")
        dropped += 1

# 3. alles wat verder wegvalt naar de homepage, zodat niets een 404 wordt
rest = 0
for slug in pages:
    if slug in kept: continue
    if any(l.startswith(f"/{slug}/ ") or l.startswith(f"/{slug}/\t") for l in lines): continue
    if f"/{slug}/  {HUB}  301" in lines: continue
    lines.append(f"/{slug}/  /  301")
    rest += 1

open(os.path.join(OUT, "_redirects"), "w").write("\n".join(lines) + "\n")
print(f"  _redirects: {len(lines)-2} regels ({dropped} stadspagina's naar de hub, {rest} overig)")

# sitemap
urls = [(SITE + "/", "1.0")] + [(f"{SITE}/{s}/", "0.8" if s in CITIES else "0.6") for s in sorted(kept)]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, pr in urls:
    sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w").write(
    f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(f"  sitemap.xml: {len(urls)} adressen")

# homepage en assets meenemen; ook daar de versie-stempel op css/js
hp_doc = open("index.html", encoding="utf-8").read()
for a in ("assets/site.css", "assets/site.js", "assets/ga.js"):
    hp_doc = hp_doc.replace(f'"/{a}"', f'"/{a}?v={VER}"')
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(hp_doc)
shutil.copytree("assets", os.path.join(OUT, "assets"))

# css en js geminificeerd in dist; de bronbestanden blijven leesbaar
def _minify_css(t):
    # voorzichtig: alleen commentaar en overbodige witruimte, niets in strings
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = "\n".join(l.strip() for l in t.splitlines() if l.strip())
    t = re.sub(r"\n(?=[{}])", "", t)
    return t

p = os.path.join(OUT, "assets", "site.css")
_src = open(p).read()
open(p, "w").write(_minify_css(_src))
print(f"  site.css geminificeerd: {len(_src)//1024} -> {os.path.getsize(p)//1024} KiB")

try:
    import rjsmin
    for js in ("site.js", "ga.js"):
        p = os.path.join(OUT, "assets", js)
        _src = open(p).read()
        open(p, "w").write(rjsmin.jsmin(_src))
        print(f"  {js} geminificeerd: {len(_src)//1024} -> {os.path.getsize(p)//1024} KiB")
except ImportError:
    print("  rjsmin niet beschikbaar: js ongewijzigd gekopieerd")
shutil.copy("_headers", os.path.join(OUT, "_headers"))
shutil.copy("favicon.ico", os.path.join(OUT, "favicon.ico"))
shutil.copy("404.html", os.path.join(OUT, "404.html")) if os.path.exists("404.html") else None
print("  homepage en assets gekopieerd")
