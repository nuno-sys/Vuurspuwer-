#!/usr/bin/env python3
"""Bouwt de statische site uit de WordPress-export.

Leest de export, kiest de 20 stadspagina's, de blogposts en de vaste
pagina's, en schrijft voor elk een map met een index.html in het ontwerp
van de homepage. Webadressen blijven exact zoals ze nu zijn.
"""
import html, json, os, re, shutil, sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

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
              "entertainer-huren-voor-bedrijfsfeest"]

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
GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VBKVM99CPB"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VBKVM99CPB');
</script>"""
FONTS    = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">'

def esc(t): return html.escape(t or "", quote=True)

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

    figure = ""
    if p.get("img"):
        iu, ia = p["img"]
        figure = (f'<figure class="lede-img wrap"><img src="{esc(iu)}" alt="{esc(ia)}" '
                  f'loading="lazy" decoding="async"></figure>')

    graph = [crumb_data]
    if kind == "post":
        graph.append({"@context": "https://schema.org", "@type": "BlogPosting",
                      "headline": p["title"], "datePublished": p["date"],
                      "description": desc, "mainEntityOfPage": url,
                      **({"image": (SITE + p["img"][0] if p["img"][0].startswith("/") else p["img"][0])} if p.get("img") else {}),
                      "author": {"@type": "Person", "name": "Nuno", "@id": f"{SITE}/#nuno"},
                      "publisher": {"@id": f"{SITE}/#business"}})
    if extra_schema: graph.append(extra_schema)
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
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#top">Naar de inhoud</a>
{IGNITION}{STAGE}{HEADER}
<main class="shell" id="top">
  <article class="page wrap">
    {crumb_html}
    <p class="eyebrow">{esc("Vuurshow op locatie" if kind == "city" else "Blog" if kind == "post" else "Vuurspuwer Nuno")}</p>
    <h1 class="page__title">{esc(p["title"])}</h1>
    {f'<p class="lede">{esc(intro)}</p>' if intro else ''}
  </article>

  {figure}
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
      <a class="btn btn--ghost" href="/#boeken">Stuur een aanvraag</a>
    </div>
  </section>
</main>
{FOOTER}
<script src="/assets/site.js" defer></script>
</body>
</html>
'''

def write(slug, doc):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)

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
    write(p["slug"], render(p, "post")); built.append(p["slug"])

for slug in KEEP_PAGES:
    p = pages.get(slug)
    if not p: missing.append(slug); continue
    write(slug, render(p, "page")); built.append(slug)

print(f"  {len(built)} pagina's gebouwd  ({len(CITIES)} steden, {len(posts)} blogposts)")
if missing: print("  niet gevonden:", ", ".join(missing))
json.dump(built, open("/tmp/_built.json", "w"))

# ------------------------------------------- doorverwijzingen en sitemap
kept = set(built)
lines = ["# oude adressen die blijven werken", ""]

# 1. dubbelingen naar het origineel zonder cijfer
for slug in pages:
    base = re.sub(r"-\d+$", "", slug)
    if base != slug and base in kept:
        lines.append(f"/{slug}/  /{base}/  301")

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
    sm.append(f"  <url><loc>{u}</loc><priority>{pr}</priority></url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w").write(
    f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(f"  sitemap.xml: {len(urls)} adressen")

# homepage en assets meenemen
shutil.copy("index.html", os.path.join(OUT, "index.html"))
shutil.copytree("assets", os.path.join(OUT, "assets"))
shutil.copy("_headers", os.path.join(OUT, "_headers"))
print("  homepage en assets gekopieerd")
