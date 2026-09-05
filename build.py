#!/usr/bin/env python3
"""Bouwt de statische site uit de WordPress-export.

Leest de export, kiest de 20 stadspagina's, de blogposts en de vaste
pagina's, en schrijft voor elk een map met een index.html in het ontwerp
van de homepage. Webadressen blijven exact zoals ze nu zijn.
"""
import base64, hashlib, html, json, os, re, shutil, sys, unicodedata
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser

import pages_content as PC
import i18n as I
import matrix as MX
import occasions as OCC
import occasions_i18n as OCCI

# gelegenheid-pagina's registreren: slugs voor hreflang, vertalingen
# in de taalbouw (de NL-versies worden verderop apart gebouwd)
I.SLUGS.update(OCC.SLUGS)
import glossary as GL
I.SLUGS.update(GL.SLUGS)
I.PAGES["en"].update(OCCI.EN)
I.PAGES["de"].update(OCCI.DE)
I.PAGES["fr"].update(OCCI.FR)

TODAY = date.today().isoformat()
MONTHS_NL = ["", "januari", "februari", "maart", "april", "mei", "juni", "juli",
             "augustus", "september", "oktober", "november", "december"]
TODAY_NL = f"{date.today().day} {MONTHS_NL[date.today().month]} {date.today().year}"

MONTHS_LOC = {
 "nl": MONTHS_NL,
 "en": ["", "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"],
 "de": ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
        "August", "September", "Oktober", "November", "Dezember"],
 "fr": ["", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"],
}

def nl_datum(iso, lang="nl"):
    """'2026-08-31' -> '31 augustus 2026' (of de vorm van de gekozen taal)"""
    try:
        j, m, d = iso.split("-")
        maand = MONTHS_LOC.get(lang, MONTHS_NL)[int(m)]
        return f"{int(d)}. {maand} {j}" if lang == "de" else f"{int(d)} {maand} {j}"
    except Exception:
        return iso

# de bouwdatum in elke taal — plaatshouders die write() omzet
TODAY_LOC = {l: nl_datum(str(date.today()), l) for l in ("nl", "en", "de", "fr")}

XML  = "nunovuurspuwer-vuurshowsampfakirshowenworkshops.WordPress.2026-08-30.xml"
OUT  = "dist"
SITE = "https://vuurspuwer.com"
NS = {'wp': 'http://wordpress.org/export/1.2/',
      'content': 'http://purl.org/rss/1.0/modules/content/'}

CITIES = [
    "vuurspuwer-boeken-in-amsterdam", "vuurspuwer-boeken-in-rotterdam",
    "vuurspuwer-boeken-in-den-haag", "vuurspuwer-boeken-in-utrecht",
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
    "vuurspuwer-boeken-in-den-haag": "Den Haag", "vuurspuwer-boeken-in-utrecht": "Utrecht",
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

# ------------------------------------------- slugs met een cijfer erachter
# WordPress plakt "-2" achter een slug als die al bezet is. Voor vier
# pagina's is dat cijfer het enige wat er van de botsing overbleef: de
# botsende pagina is allang weg, of was een verdwaalde stadspagina (de
# slug van het vuurspuwers-artikel was van "Vuurspuwer Ede", die van het
# verrassingsfeestje van "Vuurspuwer As"). Zo'n adres heeft geen reden
# om het cijfer te houden: lelijk voor de bezoeker, en Google leest het
# als "de tweede van twee". De pagina verhuist naar het schone adres, het
# oude adres wordt een 301 (zie _redirects), en de botsende oude pagina
# — die tot nu toe naar de homepage stuurde — is geen apart adres meer.
_HERNOEMD = {
    "vuurspuwer-boeken-in-utrecht-2": "vuurspuwer-boeken-in-utrecht",
    "de-betekenis-en-geschiedenis-van-vuurspuwers-2":
        "de-betekenis-en-geschiedenis-van-vuurspuwers",
    "zo-organiseer-je-een-geslaagd-verrassingsfeestje-2":
        "zo-organiseer-je-een-geslaagd-verrassingsfeestje",
    "vuurspuwer-boeken-voor-een-bedrijfsfeest-de-ultieme-spectaculaire-ervaring-2":
        "vuurspuwer-boeken-voor-een-bedrijfsfeest-de-ultieme-spectaculaire-ervaring",
}
for _oud, _nieuw in _HERNOEMD.items():
    if _oud in pages:
        pages[_nieuw] = {**pages.pop(_oud), "slug": _nieuw}

# In 21 artikelen stonden nog oude adressen (een hotmail-adres en twee
# adressen van vroegere sites) als contactadres. Het enige adres dat
# gelezen wordt is nuno@vuurspuwer.com — daar komen de aanvragen binnen
# en van daaruit gaan de bevestigingen. Overal hetzelfde adres dus.
_OUDE_MAIL = ("nuno@hotmail.nl", "contact@mentalistnuno.nl", "contact@fakir-show.nl")
for _pg in pages.values():
    for _m in _OUDE_MAIL:
        if _m in _pg["body"]:
            _pg["body"] = _pg["body"].replace(_m, "nuno@vuurspuwer.com")

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
                           for f in ("site.css", "site.js", "ga.js", "zoek.js"))).hexdigest()[:10]

GTAG = f'<script src="/assets/ga.js?v={VER}" defer></script>'
# zelf gehoste fonts: alleen de twee gezichten die boven de vouw staan
# vooraf laden; de @font-face-regels zitten in site.css zelf.
FONTS    = ('<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin.woff2" crossorigin>'
            '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/instrument-latin.woff2" crossorigin>'
            '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/jetbrains-latin.woff2" crossorigin>')

def esc(t): return html.escape(t or "", quote=True)

_DATUM_LBL = {
 "nl": {"pub": "Gepubliceerd", "mod": "bijgewerkt"},
 "en": {"pub": "Published",    "mod": "updated"},
 "de": {"pub": "Veröffentlicht", "mod": "aktualisiert"},
 "fr": {"pub": "Publié",       "mod": "mis à jour"},
}

OG_LOCALE = {"nl": "nl_NL", "en": "en_GB", "de": "de_DE", "fr": "fr_BE"}

def og_image_for(iu):
    """De gebrandede 1200x630-deelafbeelding die bij een kopfoto hoort."""
    m = re.match(r"/assets/media/([a-z0-9-]+?)(?:-\d+)?\.(?:webp|jpg)$", iu or "")
    base = m.group(1) if m else ""
    if base and os.path.exists(f"assets/media/og-{base}.jpg"):
        return f"/assets/media/og-{base}.jpg"
    return "/assets/media/og-festival.jpg"

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

# ------------------------------------------------------------- AVIF
# Naast elke WebP-foto komt een AVIF-variant (±30% kleiner bij gelijke
# kwaliteit). In de pagina's wordt elke <img> die volledig in AVIF
# beschikbaar is in een <picture> gewikkeld: moderne browsers laden AVIF,
# de rest valt terug op WebP. De og-*-deelplaatjes blijven JPG/WebP,
# want social-scrapers begrijpen AVIF niet altijd.
_AVIF_OK = set()

def gen_avif():
    from PIL import Image
    made = 0
    for f in sorted(os.listdir("assets/media")):
        if not f.endswith(".webp") or f.startswith("og-"):
            continue
        src = f"assets/media/{f}"
        dst = src[:-5] + ".avif"
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            Image.open(src).save(dst, "AVIF", quality=50)
            os.utime(dst)
            made += 1
        # alleen gebruiken als AVIF ook echt kleiner is dan de WebP
        if os.path.getsize(dst) < os.path.getsize(src):
            _AVIF_OK.add("/" + dst)
    if made:
        print(f"  {made} AVIF-varianten aangemaakt")

def _avif_set(cand):
    """'url w, url w' -> zelfde lijst in AVIF, of None als iets ontbreekt."""
    out = []
    for e in cand.split(","):
        parts = e.split()
        if not parts: return None
        u = parts[0]
        if not (u.startswith("/assets/media/") and u.endswith(".webp")):
            return None
        a = u[:-5] + ".avif"
        if a not in _AVIF_OK: return None
        out.append(" ".join([a] + parts[1:]))
    return ", ".join(out)

def _avifize(doc):
    def img_repl(m):
        tag = m.group(0)
        srcset = re.search(r'srcset="([^"]+)"', tag)
        src = re.search(r'src="([^"]+)"', tag)
        cand = srcset.group(1) if srcset else (src.group(1) if src else None)
        if not cand: return tag
        av = _avif_set(cand)
        if not av: return tag
        sizes = re.search(r'sizes="([^"]+)"', tag)
        s_attr = f' sizes="{sizes.group(1)}"' if sizes else ""
        return (f'<picture><source type="image/avif" srcset="{av}"{s_attr}>'
                f'{tag}</picture>')
    doc = re.sub(r"<img [^>]*>", img_repl, doc)
    def pre_repl(m):
        tag = m.group(0)
        if "image/avif" in tag: return tag
        iss = re.search(r'imagesrcset="([^"]+)"', tag)
        href = re.search(r'href="([^"]+)"', tag)
        av = _avif_set(iss.group(1) if iss else (href.group(1) if href else ""))
        if not av: return tag
        if iss:
            tag = tag.replace(f'imagesrcset="{iss.group(1)}"',
                              f'imagesrcset="{av}"')
        else:
            tag = tag.replace(">", f' imagesrcset="{av}">')
        return tag.replace(">", ' type="image/avif">')
    return re.sub(r'<link rel="preload" as="image"[^>]*>', pre_repl, doc)

def crumbs(items):
    li = "".join(
        f'<li><a href="{esc(u)}">{esc(n)}</a></li>' if u else f'<li><span aria-current="page">{esc(n)}</span></li>'
        for n, u in items)
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": k + 1, "name": n,
                                 **({"item": SITE + u} if u else {})}
                                for k, (n, u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Kruimelpad"><ol>{li}</ol></nav>', data

# Google toont reviewsterren en prijzen alleen bij bepaalde typen; Service
# hoort daar niet bij. Daarom krijgt elke pagina met een Service ook een
# Product-knoop (sterren + vanafprijs) en draagt elke pagina het volledige
# LocalBusiness-blok, zodat beide rich results overal gedetecteerd worden.
_RATING_LD = {"@type": "AggregateRating", "ratingValue": "4.9",
              "reviewCount": "136", "bestRating": "5", "worstRating": "1"}
_OFFER_TXT = {
    "nl": "Prijzen van €350 tot €1500, afhankelijk van show en duur. Vrijblijvende offerte op maat.",
    "en": "Prices from €350 to €1500, depending on show and duration. Free tailored quote.",
    "de": "Preise von 350 € bis 1500 €, je nach Show und Dauer. Kostenloses Angebot nach Maß.",
    "fr": "Prix de 350 € à 1500 €, selon le spectacle et la durée. Devis gratuit sur mesure.",
}
# De entiteitsblokken (bedrijf, persoon) staan op élke pagina, dus ook op
# de Engelse, Duitse en Franse. Tot nu toe stonden ze daar in het
# Nederlands: "Vuurspuwer, fakir en mentalist voor bedrijfsfeesten" in de
# structured data van een Engelse pagina. Zoekmachines lezen dat mee, en
# een pagina die zegt Engels te zijn hoort ook Engelse structured data te
# dragen. De namen, adressen en id's blijven gelijk; alleen de
# beschrijvende velden volgen de taal van de pagina.
_LD_I18N = {
 "nl": {"biz": "Vuurspuwer, fakir en mentalist voor bedrijfsfeesten, festivals, bruiloften en themafeesten in Nederland en België.",
        "nl": "Nederland", "be": "België", "de": "Deutschland",
        "job": "Vuurspuwer, fakir, mentalist en reptielenshow-artiest",
        "pers": "Professioneel vuurspuwer en fakir met 17 jaar ervaring, bekend van SBS6, RTL, VTM en optredens voor o.a. Walibi, Julianatoren en IKEA.",
        "cap": "Portret van vuurspuwer Nuno",
        "kent": ["Vuurspuwen", "Fakirshow", "Mentalisme", "Reptielenshow", "Workshop vuurspuwen", "Veiligheid bij vuurshows"]},
 "en": {"biz": "Fire breather, fakir and mentalist for corporate events, festivals, weddings and theme parties in the Netherlands and Belgium.",
        "nl": "Netherlands", "be": "Belgium", "de": "Germany",
        "job": "Fire breather, fakir, mentalist and reptile show artist",
        "pers": "Professional fire breather and fakir with 17 years of experience, known from SBS6, RTL, VTM and performances for Walibi, Julianatoren and IKEA, among others.",
        "cap": "Portrait of fire breather Nuno",
        "kent": ["Fire breathing", "Fakir show", "Mentalism", "Reptile show", "Fire-breathing workshop", "Fire show safety"]},
 "de": {"biz": "Feuerspucker, Fakir und Mentalist für Firmenfeiern, Festivals, Hochzeiten und Mottopartys in den Niederlanden und Belgien.",
        "nl": "Niederlande", "be": "Belgien", "de": "Deutschland",
        "job": "Feuerspucker, Fakir, Mentalist und Reptilienshow-Künstler",
        "pers": "Professioneller Feuerspucker und Fakir mit 17 Jahren Erfahrung, bekannt aus SBS6, RTL, VTM und Auftritten u. a. für Walibi, Julianatoren und IKEA.",
        "cap": "Porträt von Feuerspucker Nuno",
        "kent": ["Feuerspucken", "Fakirshow", "Mentalismus", "Reptilienshow", "Feuerspucker-Workshop", "Sicherheit bei Feuershows"]},
 "fr": {"biz": "Cracheur de feu, fakir et mentaliste pour fêtes d'entreprise, festivals, mariages et fêtes à thème aux Pays-Bas et en Belgique.",
        "nl": "Pays-Bas", "be": "Belgique", "de": "Allemagne",
        "job": "Cracheur de feu, fakir, mentaliste et artiste de spectacle de reptiles",
        "pers": "Cracheur de feu et fakir professionnel avec 17 ans d'expérience, connu de SBS6, RTL, VTM et de prestations pour Walibi, Julianatoren et IKEA, entre autres.",
        "cap": "Portrait du cracheur de feu Nuno",
        "kent": ["Cracher du feu", "Spectacle de fakir", "Mentalisme", "Spectacle de reptiles", "Atelier cracheur de feu", "Sécurité des spectacles de feu"]},
}
def _land(lang, code):
    return {"@type": "Country", "name": _LD_I18N[lang][code]}

_BUSINESS_LD = {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "EntertainmentBusiness"],
    "@id": f"{SITE}/#business",
    "name": "Vuurspuwer Nuno", "legalName": "Nuno Art",
    "url": f"{SITE}/",
    "description": ("Vuurspuwer, fakir en mentalist voor bedrijfsfeesten, festivals, "
                    "bruiloften en themafeesten in Nederland en België."),
    "telephone": "+31620020723", "email": "nuno@vuurspuwer.com",
    "priceRange": "€€",
    "image": [f"{SITE}/assets/media/festival-1600.webp",
              f"{SITE}/assets/media/vuurbal-1333.webp",
              f"{SITE}/assets/media/fakir-1080.webp"],
    "logo": {"@type": "ImageObject",
             "url": f"{SITE}/assets/media/logo-mail.png",
             "width": 560, "height": 153},
    "address": {"@type": "PostalAddress", "postalCode": "3703 BM",
                "addressLocality": "Zeist", "addressRegion": "Utrecht",
                "addressCountry": "NL"},
    "areaServed": [{"@type": "Country", "name": "Nederland"},
                   {"@type": "Country", "name": "België"}],
    "knowsLanguage": ["nl", "en", "de", "fr"],
    "sameAs": ["https://www.facebook.com/show.nuno",
               "https://www.instagram.com/officialnuno",
               "https://x.com/mentalist_nuno",
               "https://entertainershow.com/artiest/vuurspuwer-nuno/"],
    "aggregateRating": _RATING_LD,
}

def business_ld(lang="nl"):
    T = _LD_I18N[lang]
    return {**_BUSINESS_LD, "description": T["biz"],
            "areaServed": [_land(lang, "nl"), _land(lang, "be")]}

# De auteur/artiest als volwaardige entiteit op élke pagina (E-E-A-T):
# zoekmachines koppelen zo alle artikelen en shows aan één herkenbaar
# persoon met gezicht, ervaring en socials.
_PERSON_LD = {
    "@context": "https://schema.org", "@type": "Person",
    "@id": f"{SITE}/#nuno", "name": "Nuno",
    "alternateName": "Vuurspuwer Nuno",
    "jobTitle": "Vuurspuwer, fakir, mentalist en reptielenshow-artiest",
    "description": ("Professioneel vuurspuwer en fakir met 17 jaar ervaring, "
                    "bekend van SBS6, RTL, VTM en optredens voor o.a. Walibi, "
                    "Julianatoren en IKEA."),
    "image": {"@type": "ImageObject",
              "url": f"{SITE}/assets/media/nuno-avatar.webp",
              "width": 288, "height": 288,
              "caption": "Portret van vuurspuwer Nuno"},
    "url": f"{SITE}/over-nuno/",
    "sameAs": ["https://www.facebook.com/show.nuno",
               "https://www.instagram.com/officialnuno",
               "https://x.com/mentalist_nuno",
               "https://entertainershow.com/artiest/vuurspuwer-nuno/"],
    "worksFor": {"@id": f"{SITE}/#business"},
    "knowsAbout": ["Vuurspuwen", "Fakirshow", "Mentalisme",
                   "Reptielenshow", "Workshop vuurspuwen",
                   "Veiligheid bij vuurshows"],
    "knowsLanguage": ["nl", "en", "de", "fr"],
    "hasCredential": {"@type": "EducationalOccupationalCredential",
                      "credentialCategory": "certification",
                      "name": "Gecertificeerd vuurspuwer en fakir"},
}

def person_ld(lang="nl"):
    T = _LD_I18N[lang]
    return {**_PERSON_LD, "jobTitle": T["job"], "description": T["pers"],
            "image": {**_PERSON_LD["image"], "caption": T["cap"]},
            "url": SITE + I.url_of(lang, "over-nuno"),
            "knowsAbout": T["kent"]}

# Google Afbeeldingen: elke foto draagt maker, licentie en de pagina waar
# gebruiksrecht aangevraagd kan worden (Search Console-suggesties).
_IMG_META = {
    "creator": {"@type": "Person", "@id": f"{SITE}/#nuno", "name": "Nuno"},
    "creditText": "Vuurspuwer Nuno",
    "copyrightNotice": "© Vuurspuwer Nuno",
    "license": f"{SITE}/disclaimer-voorwaarden/",
    "acquireLicensePage": f"{SITE}/contact-3/",
}
def _license_images(g):
    if isinstance(g, dict):
        t = g.get("@type")
        if "ImageObject" in (t if isinstance(t, list) else [t]):
            for k, v in _IMG_META.items(): g.setdefault(k, v)
        for v in g.values(): _license_images(v)
    elif isinstance(g, list):
        for v in g: _license_images(v)

def _augment_rich_results(graph, lang, page_desc=None, page_img=None, page_url=None,
                          page_words=0):
    def types(g):
        t = g.get("@type")
        return t if isinstance(t, list) else [t]
    extra = []
    for g in graph:
        if not isinstance(g, dict): continue
        if "WebPage" in types(g) and page_words > 150:
            g.setdefault("wordCount", page_words)
            g.setdefault("timeRequired", f"PT{max(1, round(page_words / 220))}M")
        if "FAQPage" in types(g):
            if page_url: g.setdefault("@id", page_url + "#faq")
            g.setdefault("inLanguage", I.HTML_LANG[lang])
        if "Service" in types(g):
            offers = dict(g.pop("offers", None) or
                          {"@type": "AggregateOffer", "priceCurrency": "EUR",
                           "lowPrice": "350", "description": _OFFER_TXT[lang]})
            g.pop("aggregateRating", None)
            offers.setdefault("highPrice", "1500")
            offers.setdefault("offerCount", "6")
            offers.setdefault("availability", "https://schema.org/InStock")
            if g.get("url"): offers.setdefault("url", g["url"])
            pid = (g.get("@id") or (g.get("url", "") + "#service")).replace("#service", "#product")
            prod = {"@context": "https://schema.org", "@type": "Product",
                    "@id": pid, "name": g.get("name"),
                    "description": g.get("description") or page_desc,
                    "brand": {"@type": "Brand", "name": "Vuurspuwer Nuno"},
                    "offers": offers, "aggregateRating": _RATING_LD}
            img = g.get("image") or page_img
            if img: prod["image"] = img
            if g.get("inLanguage"): prod["inLanguage"] = g["inLanguage"]
            extra.append(prod)
    if not any(isinstance(g, dict) and
               ("LocalBusiness" in types(g) or "EntertainmentBusiness" in types(g))
               for g in graph):
        extra.append(business_ld(lang))
    if not any(isinstance(g, dict) and "Person" in types(g) for g in graph):
        extra.append(person_ld(lang))
    graph.extend(extra)
    _license_images(graph)
    # het bedrijf en de producten (sterren, prijzen) als eerste blokken in de
    # head, zodat zoekmachines ze zo vroeg mogelijk lezen
    def _prio(g):
        ts = types(g) if isinstance(g, dict) else []
        if "LocalBusiness" in ts or "EntertainmentBusiness" in ts: return 0
        if "Product" in ts: return 1
        return 2
    graph.sort(key=_prio)

# --------------------------------------------- meertalige chrome en helpers
# vertaalde kop- en voetstukken: de NL-blokken uit index.html met de
# menulinks, labels en teksten omgezet per taal. Alles wat geen eigen
# vertaling heeft, blijft gewoon naar de NL-pagina wijzen.
_FOOTER_LABELS = {
 "en": {">Reptielenshow<": ">Reptile show<", ">Workshop vuurspuwen<": ">Fire-breathing workshop<",
        ">Mentalisme<": ">Mentalism<", ">Themafeesten<": ">Theme parties<",
        ">Over Nuno<": ">About Nuno<", ">Prijzen<": ">Prices<", "💍 Vuurshows per gelegenheid": "💍 Fire shows by occasion", "📍 Vuurspuwer per stad": "📍 Fire breather by city", "🎃 Halloween per stad": "🎃 Halloween by city", "⚔️ Fakirshow per stad": "⚔️ Fakir show by city", "💨 Workshop per stad": "💨 Workshop by city", ">Bruiloften<": ">Weddings<", ">Bedrijfsfeesten<": ">Corporate events<", ">🎄 Kerst &amp; nieuwjaar<": ">🎄 Christmas &amp; New Year<", ">Beoordelingen<": ">Reviews<", ">Locaties<": ">Locations<",
        ">Aanvraagformulier<": ">Request form<", ">Algemene voorwaarden<": ">Terms &amp; conditions<",
        ">Privacybeleid<": ">Privacy policy<", "<h2>Shows</h2>": "<h2>Shows</h2>",
        "<h2>Site</h2>": "<h2>Site</h2>", "<h2>Contact</h2>": "<h2>Contact</h2>",
        ">Foto&rsquo;s<": ">Photos<", ">Video&rsquo;s<": ">Videos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Certified fire breather &amp; fakir",
        "17 jaar podiumervaring": "17 years of stage experience",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Permits &amp; safety distances arranged",
        "4.9/5 uit 136 reviews": "4.9/5 from 136 reviews",
        'aria-label="Zekerheden"': 'aria-label="Guarantees"',
        ">Bekend van<": ">As seen on<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Known from these channels and productions"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo act by fire breather Nuno: kneeling, he breathes a fireball while a dancer with large red wings stands behind him"',
        '&#128293; Vuurspuwer &middot; Vuurspuwer Nuno boeken via EntertainerShow.com': '&#128293; Fire breather &middot; Book Vuurspuwer Nuno via EntertainerShow.com',
        '>Boek nu &rarr;<': '>Book now &rarr;<',
        'Het Europese entertainmentnetwerk &middot; rechtstreeks boeken, zonder commissie': 'The European entertainment network &middot; book direct, no commission',
        '<span class="vh">(opent in een nieuw tabblad)</span>': '<span class="vh">(opens in a new tab)</span>',
        "Vuurspuwer, fakir en mentalist. Boekbaar in Nederland, Belgi&euml; en daarbuiten.": 'Fire breather, fakir and mentalist. Available in the Netherlands, Belgium and beyond.',
        "Nederland, Belgi&euml; &amp; internationaal": "Netherlands, Belgium &amp; international"},
 "de": {">Reptielenshow<": ">Reptilienshow<", ">Workshop vuurspuwen<": ">Feuerspucker-Workshop<",
        ">Mentalisme<": ">Mentalismus<", ">Themafeesten<": ">Mottopartys<",
        ">Over Nuno<": ">Über Nuno<", ">Prijzen<": ">Preise<", "💍 Vuurshows per gelegenheid": "💍 Feuershows nach Anlass", "📍 Vuurspuwer per stad": "📍 Feuerspucker nach Stadt", "🎃 Halloween per stad": "🎃 Halloween nach Stadt", "⚔️ Fakirshow per stad": "⚔️ Fakirshow nach Stadt", "💨 Workshop per stad": "💨 Workshop nach Stadt", ">Bruiloften<": ">Hochzeiten<", ">Bedrijfsfeesten<": ">Firmenfeiern<", ">🎄 Kerst &amp; nieuwjaar<": ">🎄 Weihnachten &amp; Silvester<", ">Beoordelingen<": ">Bewertungen<", ">Locaties<": ">Standorte<",
        ">Aanvraagformulier<": ">Anfrageformular<", ">Algemene voorwaarden<": ">AGB<",
        ">Privacybeleid<": ">Datenschutz<", "<h2>Shows</h2>": "<h2>Shows</h2>",
        "<h2>Site</h2>": "<h2>Website</h2>", "<h2>Contact</h2>": "<h2>Kontakt</h2>",
        ">Foto&rsquo;s<": ">Fotos<", ">Video&rsquo;s<": ">Videos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Zertifizierter Feuerspucker &amp; Fakir",
        "17 jaar podiumervaring": "17 Jahre B&uuml;hnenerfahrung",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Genehmigungen &amp; Sicherheitsabst&auml;nde geregelt",
        "4.9/5 uit 136 reviews": "4,9/5 aus 136 Bewertungen",
        'aria-label="Zekerheden"': 'aria-label="Garantien"',
        ">Bekend van<": ">Bekannt aus<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Bekannt aus diesen Sendern und Produktionen"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo-Act von Feuerspucker Nuno: kniend spuckt er einen Feuerball, w&auml;hrend eine T&auml;nzerin mit gro&szlig;en roten Fl&uuml;geln hinter ihm steht"',
        '&#128293; Vuurspuwer &middot; Vuurspuwer Nuno boeken via EntertainerShow.com': '&#128293; Feuerspucker &middot; Vuurspuwer Nuno buchen &uuml;ber EntertainerShow.com',
        '>Boek nu &rarr;<': '>Jetzt buchen &rarr;<',
        'Het Europese entertainmentnetwerk &middot; rechtstreeks boeken, zonder commissie': 'Das europ&auml;ische Entertainment-Netzwerk &middot; direkt buchen, ohne Provision',
        '<span class="vh">(opent in een nieuw tabblad)</span>': '<span class="vh">(&ouml;ffnet in neuem Tab)</span>',
        "Vuurspuwer, fakir en mentalist. Boekbaar in Nederland, Belgi&euml; en daarbuiten.": 'Feuerspucker, Fakir und Mentalist. Buchbar in den Niederlanden, Belgien und dar&uuml;ber hinaus.',
        "Nederland, Belgi&euml; &amp; internationaal": "Niederlande, Belgien &amp; international"},
 "fr": {">Reptielenshow<": ">Spectacle de reptiles<", ">Workshop vuurspuwen<": ">Atelier cracheur de feu<",
        ">Mentalisme<": ">Mentalisme<", ">Themafeesten<": ">Fêtes à thème<",
        ">Over Nuno<": ">À propos de Nuno<", ">Prijzen<": ">Tarifs<", "💍 Vuurshows per gelegenheid": "💍 Spectacles de feu par occasion", "📍 Vuurspuwer per stad": "📍 Cracheur de feu par ville", "🎃 Halloween per stad": "🎃 Halloween par ville", "⚔️ Fakirshow per stad": "⚔️ Spectacle de fakir par ville", "💨 Workshop per stad": "💨 Atelier par ville", ">Bruiloften<": ">Mariages<", ">Bedrijfsfeesten<": ">Fêtes d'entreprise<", ">🎄 Kerst &amp; nieuwjaar<": ">🎄 Noël &amp; Nouvel An<", ">Beoordelingen<": ">Avis<", ">Locaties<": ">Villes<",
        ">Aanvraagformulier<": ">Formulaire de demande<", ">Algemene voorwaarden<": ">Conditions générales<",
        ">Privacybeleid<": ">Confidentialité<", "<h2>Shows</h2>": "<h2>Spectacles</h2>",
        "<h2>Site</h2>": "<h2>Site</h2>", "<h2>Contact</h2>": "<h2>Contact</h2>",
        ">Foto&rsquo;s<": ">Photos<", ">Video&rsquo;s<": ">Vidéos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Cracheur de feu &amp; fakir certifié",
        "17 jaar podiumervaring": "17 ans d'expérience scénique",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Autorisations &amp; distances de sécurité gérées",
        "4.9/5 uit 136 reviews": "4,9/5 sur 136 avis",
        'aria-label="Zekerheden"': 'aria-label="Garanties"',
        ">Bekend van<": ">Vu sur<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Vu sur ces chaînes et productions"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo du cracheur de feu Nuno : à genoux, il crache une boule de feu tandis qu\'une danseuse aux grandes ailes rouges se tient derrière lui"',
        '&#128293; Vuurspuwer &middot; Vuurspuwer Nuno boeken via EntertainerShow.com': '&#128293; Cracheur de feu &middot; R&eacute;server Vuurspuwer Nuno via EntertainerShow.com',
        '>Boek nu &rarr;<': '>R&eacute;server &rarr;<',
        'Het Europese entertainmentnetwerk &middot; rechtstreeks boeken, zonder commissie': 'Le r&eacute;seau europ&eacute;en du divertissement &middot; r&eacute;servation directe, sans commission',
        '<span class="vh">(opent in een nieuw tabblad)</span>': '<span class="vh">(ouvre dans un nouvel onglet)</span>',
        "Vuurspuwer, fakir en mentalist. Boekbaar in Nederland, Belgi&euml; en daarbuiten.": 'Cracheur de feu, fakir et mentaliste. Disponible aux Pays-Bas, en Belgique et au-del&agrave;.',
        "Nederland, Belgi&euml; &amp; internationaal": "Pays-Bas, Belgique &amp; international"},
}
_WA_TEXT = {
 "en": "Hello%20Nuno%2C%20I%20have%20a%20question%20about%20a%20booking",
 "de": "Hallo%20Nuno%2C%20ich%20habe%20eine%20Frage%20zu%20einer%20Buchung",
 "fr": "Bonjour%20Nuno%2C%20j%27ai%20une%20question%20concernant%20une%20r%C3%A9servation",
}
_CHAT_ARIA = {"en": "Chat with Nuno", "de": "Mit Nuno chatten", "fr": "Discuter avec Nuno"}
_CHAT_CTA  = {"en": "Chat with Nuno", "de": "Mit Nuno chatten", "fr": "Discuter avec Nuno"}
_SLUIT     = {"en": "Close", "de": "Schlie&szlig;en", "fr": "Fermer"}
_WA_ARIA = {"en": "Chat with Nuno on WhatsApp", "de": "Mit Nuno auf WhatsApp chatten",
            "fr": "Discuter avec Nuno sur WhatsApp"}
_BRAND_ARIA = {"en": "Fire breather Nuno, to the homepage", "de": "Feuerspucker Nuno, zur Startseite",
               "fr": "Cracheur de feu Nuno, vers l'accueil"}
_CALL_ARIA = {"en": "Call Nuno on +31 6 200 207 23", "de": "Nuno anrufen unter +31 6 200 207 23",
              "fr": "Appeler Nuno au +31 6 200 207 23"}
_CALL_NOW = {"en": ">Call now<", "de": ">Jetzt anrufen<", "fr": ">Appeler<"}
_PRICES_LBL = {"en": "Prices", "de": "Preise", "fr": "Tarifs"}

SITEMAP_IMG = {}   # pad -> [volledige afbeeldings-urls] voor de image-sitemap

# ------------------------------------------------- cookiekeuze per taal
# De beeldvullende toestemmingskaart staat in index.html en komt via de
# FOOTER-chunk op elke pagina terecht; hier de vertalingen ervan.
_COOKIE_LBL = {
 "en": {
  ">🍪 Even eerlijk<": ">🍪 Let's be honest<",
  "Wij spuwen vuur,<br><em>geen rook</em>": "We breathe fire,<br><em>not smoke</em>",
  "Deze site meet alleen anoniem hoeveel mensen langskomen en\n    welke shows ze bekijken &mdash; zodat Nuno weet waar hij op moet inzetten.\n    Geen advertenties, geen doorverkoop, geen gedoe.":
  "This site only measures anonymously how many people drop by and which shows they look at &mdash; so Nuno knows what to focus on. No ads, no reselling, no nonsense.",
  "Liever niet? Ook prima. Dan meten we\n    niets en werkt alles gewoon door. Je kunt je keuze altijd wijzigen onderaan de site.":
  "Rather not? That's fine too. Then we measure nothing and everything keeps working. You can change your choice at any time at the bottom of the site.",
  ">Prima, meet maar mee<": ">Sure, count me in<",
  ">Liever niet<": ">Rather not<",
  ">Lees het privacybeleid<": ">Read the privacy policy<",
  ">Cookievoorkeur<": ">Cookie preference<",
 },
 "de": {
  ">🍪 Even eerlijk<": ">🍪 Mal ehrlich<",
  "Wij spuwen vuur,<br><em>geen rook</em>": "Wir spucken Feuer,<br><em>keinen Rauch</em>",
  "Deze site meet alleen anoniem hoeveel mensen langskomen en\n    welke shows ze bekijken &mdash; zodat Nuno weet waar hij op moet inzetten.\n    Geen advertenties, geen doorverkoop, geen gedoe.":
  "Diese Seite misst nur anonym, wie viele Menschen vorbeischauen und welche Shows sie ansehen &mdash; damit Nuno weiß, worauf er setzen soll. Keine Werbung, kein Weiterverkauf, kein Theater.",
  "Liever niet? Ook prima. Dan meten we\n    niets en werkt alles gewoon door. Je kunt je keuze altijd wijzigen onderaan de site.":
  "Lieber nicht? Auch gut. Dann messen wir nichts und alles funktioniert weiterhin. Ihre Wahl können Sie unten auf der Seite jederzeit ändern.",
  ">Prima, meet maar mee<": ">Passt, messt ruhig<",
  ">Liever niet<": ">Lieber nicht<",
  ">Lees het privacybeleid<": ">Datenschutzerklärung lesen<",
  ">Cookievoorkeur<": ">Cookie-Einstellung<",
 },
 "fr": {
  ">🍪 Even eerlijk<": ">🍪 Soyons honnêtes<",
  "Wij spuwen vuur,<br><em>geen rook</em>": "Nous crachons du feu,<br><em>pas de la fumée</em>",
  "Deze site meet alleen anoniem hoeveel mensen langskomen en\n    welke shows ze bekijken &mdash; zodat Nuno weet waar hij op moet inzetten.\n    Geen advertenties, geen doorverkoop, geen gedoe.":
  "Ce site mesure uniquement de façon anonyme combien de personnes passent et quels spectacles elles regardent &mdash; pour que Nuno sache où concentrer ses efforts. Pas de publicité, pas de revente, pas d'histoires.",
  "Liever niet? Ook prima. Dan meten we\n    niets en werkt alles gewoon door. Je kunt je keuze altijd wijzigen onderaan de site.":
  "Vous préférez pas ? Aucun souci. Nous ne mesurons rien et tout continue de fonctionner. Vous pouvez modifier votre choix à tout moment en bas du site.",
  ">Prima, meet maar mee<": ">D'accord, mesurez<",
  ">Liever niet<": ">Plutôt pas<",
  ">Lees het privacybeleid<": ">Lire la politique de confidentialité<",
  ">Cookievoorkeur<": ">Préférence cookies<",
 },
}

_CHROME_CACHE = {}
# ------------------------------------------------------------------ zoeken
# Een echte client-side zoekmachine: /zoekindex.json wordt tijdens de build
# per taal gevuld, /assets/zoek.js filtert en rangschikt. De voettekst-
# zoekbalk stuurt via GET naar de zoekpagina; die pagina zelf zoekt live.
_ZOEK = {
 "nl": {"url": "/zoeken/", "h1": "Zoeken",
        "seo_title": "Zoeken \u2014 Vuurspuwer Nuno",
        "seo_desc": "Zoek snel op vuurspuwer.com: shows, steden, prijzen, blog en veelgestelde vragen.",
        "eyebrow": "Zoeken", "aria": "Zoeken op de site", "ph": "Zoek op de site\u2026",
        "btn": "Zoeken",
        "intro": "Waar ben je naar op zoek? Typ een woord \u2014 bijvoorbeeld een stad, een showtype of \u2018prijzen\u2019.",
        "typ": "Typ hierboven een zoekterm om te beginnen.",
        "none": "Niets gevonden voor", "count": "resultaten voor",
        "one": "resultaat voor", "loading": "Zoeken\u2026"},
 "en": {"url": "/en/search/", "h1": "Search",
        "seo_title": "Search \u2014 Fire Breather Nuno",
        "seo_desc": "Search fire-breather Nuno\u2019s site: shows, cities, prices, blog and frequently asked questions.",
        "eyebrow": "Search", "aria": "Search the site", "ph": "Search the site\u2026",
        "btn": "Search",
        "intro": "What are you looking for? Type a word \u2014 a city, a show type, or \u2018prices\u2019.",
        "typ": "Type a search term above to begin.",
        "none": "No results for", "count": "results for",
        "one": "result for", "loading": "Searching\u2026"},
 "de": {"url": "/de/suche/", "h1": "Suche",
        "seo_title": "Suche \u2014 Feuerspucker Nuno",
        "seo_desc": "Durchsuchen Sie die Website von Feuerspucker Nuno: Shows, St\u00e4dte, Preise, Blog und h\u00e4ufige Fragen.",
        "eyebrow": "Suche", "aria": "Website durchsuchen", "ph": "Website durchsuchen\u2026",
        "btn": "Suchen",
        "intro": "Wonach suchen Sie? Geben Sie ein Wort ein \u2014 eine Stadt, eine Showart oder \u201ePreise\u201c.",
        "typ": "Geben Sie oben einen Suchbegriff ein.",
        "none": "Nichts gefunden f\u00fcr", "count": "Ergebnisse f\u00fcr",
        "one": "Ergebnis f\u00fcr", "loading": "Suchen\u2026"},
 "fr": {"url": "/fr/recherche/", "h1": "Recherche",
        "seo_title": "Recherche \u2014 Cracheur de feu Nuno",
        "seo_desc": "Recherchez sur le site du cracheur de feu Nuno\u00a0: spectacles, villes, tarifs, blog et questions fr\u00e9quentes.",
        "eyebrow": "Recherche", "aria": "Rechercher sur le site", "ph": "Rechercher sur le site\u2026",
        "btn": "Rechercher",
        "intro": "Que cherchez-vous\u00a0? Tapez un mot \u2014 une ville, un type de spectacle ou \u00ab\u00a0tarifs\u00a0\u00bb.",
        "typ": "Saisissez un terme de recherche ci-dessus.",
        "none": "Aucun r\u00e9sultat pour", "count": "r\u00e9sultats pour",
        "one": "r\u00e9sultat pour", "loading": "Recherche\u2026"},
}

def localize_doc(d, lang):
    """Past alle taalvervangingen (labels, links, WhatsApp) toe op een stuk
    HTML — gebruikt voor de header/footer-chunks én voor de volledige
    homepage-klonen per taal."""
    if lang == "nl":
        return d
    L = I.UI[lang]; M = L["menu"]
    # ankers die naar de (taal)homepage wijzen, vóór de generieke '/'-regel
    d = d.replace('href="/#', f'href="/{lang}/#')
    # paginalinks naar de vertaalde tegenhangers
    for nl_slug in I.SLUGS:
        if nl_slug == "": continue
        d = d.replace(f'href="/{nl_slug}/"', f'href="{I.url_of(lang, nl_slug)}"')
    d = d.replace('href="/"', f'href="/{lang}/"')
    # zichtbare labels
    lbl = {">Home<": f'>{M["home"]}<', ">Foto's<": f'>{M["fotos"]}<', ">Video's<": f'>{M["videos"]}<',
           ">Vuurshow<": f'>{M["vuurshow"]}<', ">Workshop<": f'>{M["workshop"]}<',
           ">Fakirshow<": f'>{M["fakirshow"]}<', ">Contact<": f'>{M["contact"]}<',
           ">Reviews<": f'>{M["reviews"]}<',
           ">Offerte aanvragen<": f'>{L["offerte"]}<',
           ">Bel direct<": _CALL_NOW[lang],
           ">&#128182; Prijzen<": f'>&#128182; {_PRICES_LBL[lang]}<',
           '<span class="burger__txt">Menu</span>': f'<span class="burger__txt">{L["menu_btn"]}</span>',
           'aria-label="Vuurspuwer Nuno, naar de homepagina"': f'aria-label="{_BRAND_ARIA[lang]}"',
           'aria-label="4.9 · 136 reviews — lees de beoordelingen"': f'aria-label="{L["stars_label"]}"',
           '4.9 &middot; 136 reviews': L["stars_txt"].replace("·", "&middot;"),
           'aria-label="Bel Nuno op +31 6 200 207 23"': f'aria-label="{_CALL_ARIA[lang]}"',
           'aria-label="Wissel tussen donkere en lichte weergave"':
           {"en": 'aria-label="Switch between dark and light mode"',
            "de": 'aria-label="Zwischen dunklem und hellem Modus wechseln"',
            "fr": 'aria-label="Basculer entre mode sombre et clair"'}[lang],
           'aria-label="Menu openen"': f'aria-label="{L["menu_btn"]}"',
           '>Naar de inhoud<': f'>{L["skip"]}<',
           'aria-label="Chat met Nuno"': f'aria-label="{_CHAT_ARIA[lang]}"',
           '<span id="chatCtaTxt">Chat met Nuno</span>': f'<span id="chatCtaTxt">{_CHAT_CTA[lang]}</span>',
           'class="chat__close" id="chatClose" aria-label="Sluiten"': f'class="chat__close" id="chatClose" aria-label="{_SLUIT[lang]}"',
           'data-i18n-open="Menu"': "",
           }
    for a, b in lbl.items(): d = d.replace(a, b)
    # de burger wisselt open/dicht-tekst via data-attributen
    d = d.replace('<button class="burger"',
                  f'<button class="burger" data-txt-open="{L["close_btn"]}" data-txt-closed="{L["menu_btn"]}"')
    for a, b in _FOOTER_LABELS[lang].items(): d = d.replace(a, b)
    for a, b in _COOKIE_LBL[lang].items(): d = d.replace(a, b)
    # WhatsApp-knop: taalversie van tekst, label en statuswoorden
    d = d.replace("Hallo%20Nuno%2C%20ik%20heb%20een%20vraag%20over%20een%20boeking", _WA_TEXT[lang])
    d = d.replace('aria-label="Chat met Nuno op WhatsApp"', f'aria-label="{_WA_ARIA[lang]}"')
    d = d.replace('<a class="wa" ', f'<a class="wa" data-online="{L["wa_status_on"]}" data-offline="{L["wa_status_off"]}" ')
    d = d.replace('>Online</b>', f'>{L["wa_status_on"]}</b>')
    # voettekst-zoekbalk in de taal van de pagina
    Z = _ZOEK[lang]
    d = d.replace('>Zoeken op de site<', f'>{esc(Z["aria"])}<')
    d = d.replace('aria-label="Zoeken op de site"', f'aria-label="{esc(Z["aria"])}"')
    d = d.replace('placeholder="Zoek op de site&hellip;"', f'placeholder="{esc(Z["ph"])}"')
    d = d.replace('>Zoeken</button>', f'>{esc(Z["btn"])}</button>')
    d = d.replace('action="/zoeken/"', f'action="{Z["url"]}"')
    # sitelinks-zoekvak (SearchAction) naar de taalversie van de zoekpagina
    d = d.replace("https://vuurspuwer.com/zoeken/?q=",
                  f"https://vuurspuwer.com{Z['url']}?q=")
    return d

def chrome(lang):
    """(header, footer) voor een taal; NL is het origineel."""
    if lang == "nl":
        return HEADER, FOOTER
    if lang not in _CHROME_CACHE:
        _CHROME_CACHE[lang] = (localize_doc(HEADER, lang), localize_doc(FOOTER, lang))
    return _CHROME_CACHE[lang]

def alternates_for(nl_slug):
    return {l: I.url_of(l, nl_slug) for l in ("nl", "en", "de", "fr")}

def regio_alternates(nl_city):
    """hreflang voor een NL-stadspagina met een Duitse of Franse versie."""
    for lang, mapping in I.REGIO_SLUGS.items():
        if nl_city in mapping:
            return {"nl": f"/{nl_city}/", lang: f"/{lang}/{mapping[nl_city]}/"}
    return None

def lang_row(lang, alternates):
    """De taalkeuze in de footer: linkt naar déze pagina in elke taal."""
    parts = []
    for l in ("nl", "en", "de", "fr"):
        href = (alternates or {}).get(l) or ("/" if l == "nl" else f"/{l}/")
        name = I.LANG_NAMES[l]
        if l == lang:
            parts.append(f'<b aria-current="true">{name}</b>')
        else:
            parts.append(f'<a href="{href}" hreflang="{l}" lang="{l}">{name}</a>')
    return ('<div class="foot__langs">\U0001F310 ' + " &middot; ".join(parts) + "</div>")

# Inhoudsopgave met ankers op elke lange pagina: Google kan dan
# "Ga naar sectie"-springlinks onder het zoekresultaat tonen.
_TOC_TITLE = {"nl": "Op deze pagina", "en": "On this page",
              "de": "Auf dieser Seite", "fr": "Sur cette page"}
def _hid(text, used):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "sectie"
    h = t; n = 2
    while h in used: h = f"{t}-{n}"; n += 1
    used.add(h)
    return h

def _add_toc(body, lang):
    used, heads = set(), []
    def repl(m):
        label = m.group(1)
        text = html.unescape(re.sub(r"<[^>]+>", "", label)).strip()
        hid = _hid(text, used)
        heads.append((hid, text))
        return f'<h2 id="{hid}">{label}</h2>'
    new = re.sub(r"<h2>(.*?)</h2>", repl, body, flags=re.S)
    if len(heads) < 3: return body
    items = "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in heads)
    toc = (f'<nav class="toc" aria-label="{_TOC_TITLE[lang]}">'
           f'<p class="toc__t">{_TOC_TITLE[lang]}</p><ul>{items}</ul></nav>')
    pos = new.find("<h2")
    return new[:pos] + toc + new[pos:] if pos > -1 else new

# Instant-navigatie: direct na de eerste paginalading worden de vier
# belangrijkste vervolgpagina's alvast opgehaald, en elke interne link
# wordt bij hover/touch al gepre-renderd (Speculation Rules, Chrome/Edge).
# De speculatieregels stonden per pagina met eigen URL's in de HTML, maar het
# Content-Security-Policy van de site blokkeerde ze stilzwijgend ("Refused to
# apply inline speculation rules") - ze hebben dus nooit gewerkt. Nu zijn ze op
# elke pagina identiek, zodat er precies EEN hash is; die zetten we hieronder in
# de CSP. Daarmee werken ze wel, zonder de policy op te rekken.
_OK_NC = ("\U0001F525 Gelukt \u2014 je aanvraag is verstuurd! "
          "Ik reageer persoonlijk <b>binnen 24 uur</b>.")


def spec_rules(lang=None, zelf=None):
    return ('<script type="speculationrules">'
            + json.dumps(spec_regels_json(), separators=(",", ":")) + "</script>")


def spec_regels_json():
    intern = [{"href_matches": "/*"},
              {"not": {"href_matches": "/api/*"}},
              {"not": {"href_matches": "/assets/*"}}]
    return {
        # alles wat de bezoeker aanwijst wordt alvast opgehaald - niets
        # wordt blind vooruit geladen, dus geen concurrentie met de pagina
        # die hij nu aan het lezen is
        "prefetch": [{"where": {"and": intern}, "eagerness": "moderate"}],
        # prerender voert de hele pagina uit, inclusief scripts en beelden.
        # Dat mag voor de navigatie en de boekknoppen bij hover, maar niet
        # voor de 102 stedenlinks in de voettekst - daar wacht
        # "conservative" tot de bezoeker de muisknop indrukt.
        "prerender": [
            {"where": {"and": [{"selector_matches": ".nav a, .menu a, .btn"}] + intern[1:]},
             "eagerness": "moderate"},
            {"where": {"and": intern}, "eagerness": "conservative"},
        ],
    }


# ---------------------------------------------- foto-strip halverwege
# Dezelfde galerijplaten als op de homepage, als horizontale scroll-strip
# na ±25% van de inhoud: bezoekers zien de shows, de foto's tellen mee in
# de image-sitemap per pagina en de meest relevante foto staat vooraan.
_MIDGAL_IMGS = [
 ("bruiloft",   "bruiloft-480.webp",   "bruiloft-1080.webp",   480, 541, ("bruiloft", "trouw", "wedding", "hochzeit", "mariage")),
 ("festival",   "festival-480.webp",   "festival-1600.webp",   480, 481, ("festival",)),
 ("vuurbal",    "vuurbal-480.webp",    "vuurbal-1333.webp",    480, 720, ("halloween", "vuurwerk", "firework", "feuerwerk", "artifice", "kerst", "silvester", "nieuwjaar", "new-year", "noel")),
 ("themafeest", "themafeest-480.webp", "themafeest-1080.webp", 480, 600, ("bedrijfsfeest", "corporate", "firmenfeier", "entreprise", "themafeest")),
 ("workshop",   "workshop-480.webp",   "workshop-1125.webp",   480, 603, ("workshop", "vrijgezell", "bachelor", "junggesell", "evjf", "atelier")),
 ("fakir",      "fakir-480.webp",      "fakir-1080.webp",      480, 599, ("fakir", "spijker")),
 ("avondvuur",  "avondvuur-480.webp",  "avondvuur-1080.webp",  480, 476, ("verjaardag", "birthday", "geburtstag", "anniversaire", "jubil")),
 ("reptiel",    "reptiel-480.webp",    "reptiel-960.webp",     480, 447, ("reptiel", "slang", "reptile")),
 ("vuurzee",    "vuurzee-480.webp",    "vuurzee-1234.webp",    480, 479, ("vuurwerk", "firework", "feuerwerk", "artifice", "halloween", "kerst", "nieuwjaar", "silvester", "noel", "new-year")),
 ("straatfakir", "straatfakir-480.webp", "straatfakir-1081.webp", 480, 320, ("fakir", "spijker", "entertainer")),
 ("glasact",    "glasact-480.webp",    "glasact-1600.webp",    480, 320, ("fakir", "glas", "spijker", "mentalis")),
 ("podium",     "podium-480.webp",     "podium-1024.webp",     480, 353, ("festival", "concert")),
 ("vuurhart",   "vuurhart-480.webp",   "vuurhart-998.webp",    480, 600, ("bruiloft", "trouw", "huwelijk", "wedding", "hochzeit", "mariage", "verjaardag", "jubileum")),
 ("cirque",     "cirque-480.webp",     "cirque-1080.webp",     480, 710, ("themafeest", "festival", "fakir", "vrijgezell")),
 ("spijkersandwich", "spijkersandwich-480.webp", "spijkersandwich-1125.webp", 480, 476, ("fakir", "spijker", "halloween")),
 ("themafakir", "themafakir-480.webp", "themafakir-1056.webp", 480, 931, ("themafeest", "bedrijfsfeest", "corporate", "firmen", "entreprise", "fakir")),
 ("familiefest", "familiefest-480.webp", "familiefest-640.webp", 480, 965, ("festival", "kinderfeest", "verjaardag", "familie")),
 ("galavuur",   "galavuur-480.webp",   "galavuur-1080.webp",   480, 853, ("bruiloft", "trouw", "huwelijk", "wedding", "hochzeit", "mariage", "gala", "jubileum", "kerst")),
 ("zonsondergang", "zonsondergang-480.webp", "zonsondergang-1152.webp", 480, 853, ("bruiloft", "festival", "verjaardag", "zomer")),
 ("nachtvuur",  "nachtvuur-480.webp",  "nachtvuur-960.webp",   480, 480, ("nieuwjaar", "silvester", "kerst", "noel", "new-year", "halloween")),
 ("terrasvuur", "terrasvuur-480.webp", "terrasvuur-582.webp",  480, 792, ("bedrijfsfeest", "personeelsfeest", "zakelijk", "corporate", "firmen", "entreprise")),
 ("portret",    "portret-480.webp",    "portret-1080.webp",    480, 600, ("mentalis", "entertainer", "hypno")),
]
_MIDGAL_ALT = {
 "bruiloft":   {"nl": "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels",
                "en": "Duo act at a wedding: fire breather Nuno with a dancer with red wings",
                "de": "Duo-Act auf einer Hochzeit: Feuerspucker Nuno mit Tänzerin mit roten Flügeln",
                "fr": "Duo à un mariage : le cracheur de feu Nuno avec une danseuse aux ailes rouges"},
 "festival":   {"nl": "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek",
                "en": "Fire breather Nuno blows a fireball on a festival square for a large crowd",
                "de": "Feuerspucker Nuno spuckt einen Feuerball auf einem Festivalplatz vor großem Publikum",
                "fr": "Le cracheur de feu Nuno souffle une boule de feu devant une grande foule de festival"},
 "vuurbal":    {"nl": "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer",
                "en": "Towering fireball against a black night sky above the fire breather",
                "de": "Meterhoher Feuerball vor schwarzem Nachthimmel über dem Feuerspucker",
                "fr": "Immense boule de feu contre un ciel nocturne au-dessus du cracheur de feu"},
 "themafeest": {"nl": "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond",
                "en": "Fire breather next to a vintage bus during an evening theme party",
                "de": "Feuerspucker neben einem Oldtimer-Bus bei einer abendlichen Mottoparty",
                "fr": "Cracheur de feu près d'un bus vintage lors d'une soirée à thème"},
 "workshop":   {"nl": "Workshopdeelnemer blaast een grote vuurbal tegen de avondlucht",
                "en": "Workshop participant blows a large fireball against the evening sky",
                "de": "Workshop-Teilnehmer bläst einen großen Feuerball gegen den Abendhimmel",
                "fr": "Participant à l'atelier soufflant une grande boule de feu au crépuscule"},
 "fakir":      {"nl": "Fakiract: Nuno draagt het gewicht van een staande toeschouwer",
                "en": "Fakir act: Nuno bears the weight of a standing spectator",
                "de": "Fakir-Act: Nuno trägt das Gewicht eines stehenden Zuschauers",
                "fr": "Numéro de fakir : Nuno porte le poids d'un spectateur debout"},
 "avondvuur":  {"nl": "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering",
                "en": "Fire breather Nuno blows an enormous fireball at dusk",
                "de": "Feuerspucker Nuno spuckt einen riesigen Feuerball in der Abenddämmerung",
                "fr": "Le cracheur de feu Nuno souffle une énorme boule de feu au crépuscule"},
 "reptiel":    {"nl": "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow",
                "en": "Nuno with a boa constrictor around his arm during the reptile show",
                "de": "Nuno mit einer Boa constrictor um den Arm während der Reptilienshow",
                "fr": "Nuno avec un boa constricteur autour du bras pendant le spectacle de reptiles"},
 "vuurzee":     {"nl": "Vuurspuwer Nuno blaast een enorme vuurzee met vonkenregen in een uitgaansstraat bij nacht",
                "en": "Fire breather Nuno blowing an enormous sea of fire with a rain of sparks in a nightlife street",
                "de": "Feuerspucker Nuno bläst ein riesiges Feuermeer mit Funkenregen in einer Ausgehstraße bei Nacht",
                "fr": "Le cracheur de feu Nuno souffle une immense mer de feu avec pluie d'étincelles dans une rue animée"},
 "straatfakir": {"nl": "Fakiract op straat: twee toeschouwers staan op Nuno terwijl hij op het spijkerbed ligt",
                "en": "Fakir act in the street: two spectators standing on Nuno while he lies on the bed of nails",
                "de": "Fakir-Act auf der Straße: zwei Zuschauer stehen auf Nuno, während er auf dem Nagelbrett liegt",
                "fr": "Numéro de fakir dans la rue : deux spectateurs debout sur Nuno allongé sur la planche à clous"},
 "glasact":     {"nl": "Nuno steunt met zijn handen in de glasscherven tijdens een theatershow",
                "en": "Nuno resting his hands in broken glass during a theatre show",
                "de": "Nuno stützt sich während einer Theatershow mit den Händen in Glasscherben",
                "fr": "Nuno prend appui les mains dans les tessons de verre pendant un spectacle en salle"},
 "podium":      {"nl": "Nuno op het festivalpodium met vuur boven een juichende festivalmenigte",
                "en": "Nuno on the festival stage with fire above a cheering festival crowd",
                "de": "Nuno auf der Festivalbühne mit Feuer über einer jubelnden Menge",
                "fr": "Nuno sur la scène du festival, du feu au-dessus d'une foule en liesse"},
 "vuurhart":    {"nl": "Vuurspuwer Nuno blaast een vuurbal in de vorm van een hart tegen de zomerlucht",
                "en": "Fire breather Nuno blowing a heart-shaped fireball against the summer sky",
                "de": "Feuerspucker Nuno bläst einen herzförmigen Feuerball in den Sommerhimmel",
                "fr": "Le cracheur de feu Nuno souffle une boule de feu en forme de cœur dans le ciel d'été"},
 "cirque":      {"nl": "Toeschouwer staat op het spijkerbed op Nuno tijdens een spectaculaire circusavond met confetti",
                "en": "Spectator standing on the bed of nails on Nuno during a spectacular circus night with confetti",
                "de": "Zuschauerin steht auf dem Nagelbrett auf Nuno während einer spektakulären Zirkusnacht mit Konfetti",
                "fr": "Spectatrice debout sur la planche à clous posée sur Nuno lors d'une soirée cirque spectaculaire"},
 "spijkersandwich": {"nl": "Fakiract in de club: Nuno ligt tussen twee spijkerbedden terwijl een toeschouwer er bovenop staat",
                "en": "Fakir act in the club: Nuno lying between two beds of nails while a spectator stands on top",
                "de": "Fakir-Act im Club: Nuno liegt zwischen zwei Nagelbrettern, während ein Zuschauer darauf steht",
                "fr": "Numéro de fakir en club : Nuno allongé entre deux planches à clous, un spectateur debout dessus"},
 "themafakir":  {"nl": "Gast staat op het spijkerbord op Nuno tijdens een Aziatisch themafeest, geholpen door twee dames in kimono",
                "en": "Guest standing on the nail board on Nuno during an Asian theme party, helped by two ladies in kimono",
                "de": "Gast steht auf dem Nagelbrett auf Nuno bei einer asiatischen Mottoparty, gestützt von zwei Damen im Kimono",
                "fr": "Une invitée debout sur la planche à clous posée sur Nuno lors d'une soirée à thème asiatique"},
 "familiefest": {"nl": "Vuurspuwer Nuno in rood circusjasje blaast een vuurbal boven het publiek op een zomers familiefestival",
                "en": "Fire breather Nuno in a red circus jacket blowing a fireball above the crowd at a summer family festival",
                "de": "Feuerspucker Nuno in roter Zirkusjacke bläst einen Feuerball über dem Publikum eines Familienfestivals",
                "fr": "Le cracheur de feu Nuno en veste de cirque rouge souffle une boule de feu au-dessus du public d'un festival familial"},
 "galavuur":    {"nl": "In wit gala-kostuum blaast Nuno een metershoge vuurzuil tussen bloemen en kaarsen op een chique feest",
                "en": "In a white gala suit, Nuno blows a towering column of fire between flowers and candles at an elegant party",
                "de": "Im weißen Gala-Anzug bläst Nuno eine meterhohe Feuersäule zwischen Blumen und Kerzen auf einem edlen Fest",
                "fr": "En costume de gala blanc, Nuno souffle une colonne de feu immense entre fleurs et bougies lors d'une fête chic"},
 "zonsondergang": {"nl": "Vuurspuwer Nuno in glitterjasje blaast een vuurbal over het water bij zonsondergang voor publiek",
                "en": "Fire breather Nuno in a glitter jacket blowing a fireball over the water at sunset for an audience",
                "de": "Feuerspucker Nuno in Glitzerjacke bläst bei Sonnenuntergang einen Feuerball über das Wasser",
                "fr": "Le cracheur de feu Nuno en veste pailletée souffle une boule de feu au-dessus de l'eau au coucher du soleil"},
 "nachtvuur":   {"nl": "Vuurspuwer Nuno blaast met twee fakkels een grote vuurbal recht omhoog in de nacht",
                "en": "Fire breather Nuno with two torches blowing a large fireball straight up into the night",
                "de": "Feuerspucker Nuno bläst mit zwei Fackeln einen großen Feuerball senkrecht in die Nacht",
                "fr": "Le cracheur de feu Nuno, deux torches en main, souffle une grande boule de feu droit dans la nuit"},
 "terrasvuur":  {"nl": "Geknield blaast vuurspuwer Nuno een lange vlam over het terras, zelfs in de regen",
                "en": "Kneeling, fire breather Nuno blows a long flame across the terrace, even in the rain",
                "de": "Kniend bläst Feuerspucker Nuno eine lange Flamme über die Terrasse, sogar im Regen",
                "fr": "À genoux, le cracheur de feu Nuno souffle une longue flamme sur la terrasse, même sous la pluie"},
 "portret":     {"nl": "Portret van vuurspuwer en mentalist Nuno met hoed in paars-rood stagelicht",
                "en": "Portrait of fire breather and mentalist Nuno with hat in purple-red stage light",
                "de": "Porträt von Feuerspucker und Mentalist Nuno mit Hut im violett-roten Bühnenlicht",
                "fr": "Portrait du cracheur de feu et mentaliste Nuno, chapeau vissé, dans une lumière de scène pourpre"},
}
_MIDGAL_HEAD = {"nl": "Zo ziet het eruit — foto's uit de shows",
                "en": "What it looks like — photos from the shows",
                "de": "So sieht es aus — Fotos aus den Shows",
                "fr": "Aperçu en images — photos des spectacles"}
_MIDGAL_SKIP = {"", "blog", "404", "en", "de", "fr",
                "fotos", "videos", "contact-3", "beoordelingen",
                "disclaimer-voorwaarden", "privacybeleid"}
for _s in ("fotos", "videos", "contact-3", "beoordelingen"):
    for _l in ("en", "de", "fr"):
        _MIDGAL_SKIP.add(f"{_l}/{I.SLUGS[_s][_l]}")

def midgal(lang, slug):
    s = slug.lower()
    order = sorted(range(len(_MIDGAL_IMGS)),
                   key=lambda i: (0 if any(k in s for k in _MIDGAL_IMGS[i][5]) else 1, i))
    tiles, fulls = [], []
    for i in order:
        base, thumb, full, w, h, _k = _MIDGAL_IMGS[i]
        alt = _MIDGAL_ALT[base][lang]
        ss = srcset_of(f"/assets/media/{thumb}")
        ss_attr = f' srcset="{ss}" sizes="(max-width:700px) 62vw, 300px"' if ss else ""
        tiles.append(
            f'<figure class="plate"><a href="/assets/media/{full}" data-lightbox>'
            f'<img src="/assets/media/{thumb}"{ss_attr} width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="{esc(alt)}"></a></figure>')
        fulls.append(f"{SITE}/assets/media/{full}")
    head = _MIDGAL_HEAD[lang]
    html_out = (f'<aside class="midgal" aria-label="{esc(head)}">'
                f'<p class="midgal__eyebrow">📸 {esc(head)}</p>'
                f'<div class="midgal__track">{"".join(tiles)}</div></aside>')
    return html_out, fulls[:8]

# ------------------------------------------------- video-strip
# Twee showreels verderop in de inhoud: eerst het vuur, als uitsmijter de
# metershoge vuurbal in portret. Zelfde .reel-mechaniek als de homepage:
# het bestand laadt pas (data-src) zodra de video in beeld schuift en
# speelt dan gedempt vanzelf af; uit beeld pauzeert hij zichzelf.
_VIDGAL = [
    ("reel-1.mp4", "reel-1-poster.webp", "reel-1-poster-640.webp",
     "PT19S", 640, 480, ""),
    ("hero-portrait.mp4", "vuurbal-900.webp", "vuurbal-640.webp",
     "PT5S", 730, 1022, " reel--tall"),
]
_VIDGAL_TXT = {
 "nl": {"head": "De show in beweging", "play": "Video afspelen",
        "cc": "Geen gesproken tekst",
        "names": ("Vuurshow op locatie", "Vuurbal in close-up"),
        "descs": ("Vuurspuwer Nuno tijdens een vuurshow op locatie: vuurspuwen, vuurjongleren en body fire.",
                  "Meters hoge vuurbal van vuurspuwer Nuno, gefilmd van dichtbij.")},
 "en": {"head": "The show in motion", "play": "Play video",
        "cc": "No spoken text",
        "names": ("Fire show on location", "Fireball in close-up"),
        "descs": ("Fire breather Nuno during a fire show on location: fire breathing, fire juggling and body fire.",
                  "Towering fireball by fire breather Nuno, filmed up close.")},
 "de": {"head": "Die Show in Bewegung", "play": "Video abspielen",
        "cc": "Kein gesprochener Text",
        "names": ("Feuershow vor Ort", "Feuerball in Nahaufnahme"),
        "descs": ("Feuerspucker Nuno während einer Feuershow vor Ort: Feuerspucken, Feuerjonglage und Body Fire.",
                  "Meterhoher Feuerball von Feuerspucker Nuno, aus nächster Nähe gefilmt.")},
 "fr": {"head": "Le spectacle en mouvement", "play": "Lire la vidéo",
        "cc": "Pas de texte parlé",
        "names": ("Spectacle de feu sur place", "Boule de feu en gros plan"),
        "descs": ("Le cracheur de feu Nuno pendant un spectacle de feu sur place : crachage de feu, jonglerie enflammée et body fire.",
                  "Immense boule de feu du cracheur de feu Nuno, filmée de près.")},
}

def vidgal(lang, page_url):
    """De strip zelf plus de bijbehorende VideoObject-blokken."""
    t = _VIDGAL_TXT[lang]
    tiles, ld = [], []
    for i, (src, poster, small, dur, w, h, cls) in enumerate(_VIDGAL):
        name, desc = t["names"][i], t["descs"][i]
        ratio = "" if cls else ' data-ratio="4/3"'
        tiles.append(f'''<figure class="reel{cls}"{ratio}>
        <video muted loop playsinline preload="none" data-poster="/assets/media/{small}"
               data-src="/assets/media/{src}" aria-label="{esc(desc)}"><track kind="captions" src="/assets/media/stil.vtt" srclang="nl" label="{esc(t["cc"])}"></video>
        <button class="reel__play" type="button" aria-label="{esc(t["play"])}: {esc(name)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <figcaption class="reel__hud"><span>{esc(name)}</span><span class="reel__time"></span></figcaption>
      </figure>''')
        ld.append({"@context": "https://schema.org", "@type": "VideoObject",
                   "@id": f"{page_url}#showreel-{i + 1}",
                   "name": f"{name} — Vuurspuwer Nuno", "description": desc,
                   "contentUrl": f"{SITE}/assets/media/{src}",
                   "thumbnailUrl": f"{SITE}/assets/media/{poster}",
                   "uploadDate": "2026-08-30", "duration": dur,
                   "width": w, "height": h,
                   "inLanguage": I.HTML_LANG[lang],
                   "publisher": {"@id": f"{SITE}/#business"}})
    head = t["head"]
    html_out = (f'<aside class="vidgal" aria-label="{esc(head)}"><div class="vidgal__inner">'
                f'<p class="vidgal__eyebrow">🎬 {esc(head)}</p>'
                f'<div class="vidgal__track">{"".join(tiles)}</div></div></aside>')
    return html_out, ld

def _insert_two(body, first, second):
    """`first` (fotostrip) na ±25% van de tekst, `second` (videostrip) na
    ±62% — met minstens één blok ertussen, zodat de twee stroken nooit
    direct op elkaar volgen. Geeft (body, is-de-videostrip-geplaatst) terug.

    Pagina's met een eigen indeling (zoals het vuur-woordenboek) bepalen de
    plek zelf met <!--STRIP1--> en <!--STRIP2-->-markeringen, zodat de
    stroken nooit binnen een grid of kaart belanden."""
    if "<!--STRIP1-->" in body:
        body = body.replace("<!--STRIP1-->", first, 1)
        vid = "<!--STRIP2-->" in body and bool(second)
        body = body.replace("<!--STRIP2-->", second if vid else "", 1)
        return body, vid
    parts = re.split(r"(</p>|</ul>|</ol>|</table>|</blockquote>)", body)
    chunks = [parts[i] + parts[i + 1] for i in range(0, len(parts) - 1, 2)]
    if len(parts) % 2:
        chunks.append(parts[-1])
    if len(chunks) < 3:
        return body + first, False
    text_len = lambda c: len(re.sub(r"<[^>]+>", "", c))
    total = sum(text_len(c) for c in chunks) or 1
    def pick(frac, lo):
        cum = 0
        for idx in range(len(chunks) - 1):
            cum += text_len(chunks[idx])
            if cum >= total * frac and idx >= lo:
                return idx
        return None
    i1 = pick(0.25, 1)
    if i1 is None:
        return body + first, False
    i2 = pick(0.62, i1 + 2) if second else None
    out = []
    for idx, c in enumerate(chunks):
        out.append(c)
        if idx == i1:
            out.append(first)
        if idx == i2:
            out.append(second)
    return "".join(out), i2 is not None

def _insert_mid(body, snippet, frac=0.25):
    parts = re.split(r"(</p>|</ul>|</ol>|</table>|</blockquote>)", body)
    chunks = []
    for i in range(0, len(parts) - 1, 2):
        chunks.append(parts[i] + parts[i + 1])
    if len(parts) % 2:
        chunks.append(parts[-1])
    if len(chunks) < 3:
        return body + snippet
    text_len = lambda c: len(re.sub(r"<[^>]+>", "", c))
    total = sum(text_len(c) for c in chunks)
    cum = 0
    for idx, c in enumerate(chunks[:-1]):
        cum += text_len(c)
        if cum >= total * frac and idx >= 1:
            return "".join(chunks[:idx + 1]) + snippet + "".join(chunks[idx + 1:])
    return body + snippet

# ------------------------------------------------- offerte-wizard
# Drie stappen naar een indicatieprijs: gelegenheid -> pakket + datum en
# plaats -> prijsindicatie met één klik naar WhatsApp (voor-ingevuld
# bericht) of het offerteformulier. Volledig client-side, dus geen
# milliseconde laadtijd; site.js verzorgt de interactie en GA4-events.
_WIZ = {
 "nl": {"eyebrow": "💶 Offerte-wizard", "title": "Weet in <em>30 seconden</em> je prijs",
        "sub": "Drie klikken en je ziet direct een eerlijke prijsindicatie — en of je datum nog vrij is.",
        "q1": "Wat vieren jullie?", "q2": "Welke show past erbij?",
        "date": "Datum (optioneel)", "place": "Plaats", "place_ph": "Bijv. Utrecht of Antwerpen",
        "back": "‹ Terug", "next": "Bekijk mijn prijs ›",
        "res_head": "Jouw prijsindicatie", "res_note": "Inclusief professioneel materiaal, verzekering en afstemming met de locatie. Reistijd wordt transparant in de offerte opgenomen.",
        "res_trust": "★ 4,9/5 uit 136 reviews · Binnen 24 uur een offerte op maat",
        "wa_btn": "Check datum via WhatsApp", "form_btn": "Vraag offerte aan",
        "popular": "Meest gekozen", "no_date": "datum in overleg", "no_place": "onze regio",
        "wa_msg": "Hallo Nuno! Ik zoek een {pkg} voor een {occ} op {date} in {place}. Is die datum nog vrij?",
        "form_msg": "{occ} — {pkg}. Indicatie uit de prijswizard: {price}.",
        "occs": [("💍", "Bruiloft"), ("🏢", "Bedrijfsfeest"), ("🎉", "Verjaardag"),
                 ("🎪", "Festival"), ("🎃", "Halloween"), ("🥂", "Vrijgezellenfeest"),
                 ("✨", "Iets anders")],
        "pkgs": [("⚡", "Power-act", "10 minuten vol spektakel", 350, 450, 0),
                 ("🔥", "Volledige vuurshow", "±20 minuten — de populairste keuze", 450, 750, 1),
                 ("🎪", "Festival-pakket", "meerdere sets tot 5×20 minuten", 750, 1500, 0),
                 ("💨", "Workshop vuurspuwen", "zelf leren vuurspuwen met de groep", 350, 650, 0),
                 ("🧠", "Advies van Nuno", "nog geen idee — denk met me mee", 350, 1500, 0)]},
 "en": {"eyebrow": "💶 Quote wizard", "title": "Know your price in <em>30 seconds</em>",
        "sub": "Three clicks and you instantly see an honest price indication — and whether your date is still free.",
        "q1": "What are you celebrating?", "q2": "Which show fits best?",
        "date": "Date (optional)", "place": "Town or city", "place_ph": "E.g. Amsterdam or Antwerp",
        "back": "‹ Back", "next": "Show my price ›",
        "res_head": "Your price indication", "res_note": "Including professional equipment, insurance and coordination with the venue. Travel time is included transparently in the quote.",
        "res_trust": "★ 4.9/5 from 136 reviews · Tailored quote within 24 hours",
        "wa_btn": "Check the date on WhatsApp", "form_btn": "Request a quote",
        "popular": "Most chosen", "no_date": "date to be agreed", "no_place": "our region",
        "wa_msg": "Hello Nuno! I'm looking for a {pkg} for a {occ} on {date} in {place}. Is that date still available?",
        "form_msg": "{occ} — {pkg}. Indication from the price wizard: {price}.",
        "occs": [("💍", "Wedding"), ("🏢", "Corporate event"), ("🎉", "Birthday"),
                 ("🎪", "Festival"), ("🎃", "Halloween"), ("🥂", "Bachelor party"),
                 ("✨", "Something else")],
        "pkgs": [("⚡", "Power act", "10 minutes of pure spectacle", 350, 450, 0),
                 ("🔥", "Full fire show", "±20 minutes — the most popular choice", 450, 750, 1),
                 ("🎪", "Festival package", "multiple sets up to 5×20 minutes", 750, 1500, 0),
                 ("💨", "Fire-breathing workshop", "learn to breathe fire with your group", 350, 650, 0),
                 ("🧠", "Nuno's advice", "no idea yet — let's think together", 350, 1500, 0)]},
 "de": {"eyebrow": "💶 Angebots-Assistent", "title": "In <em>30 Sekunden</em> zum Preis",
        "sub": "Drei Klicks und Sie sehen sofort eine ehrliche Preisindikation — und ob Ihr Termin noch frei ist.",
        "q1": "Was feiern Sie?", "q2": "Welche Show passt?",
        "date": "Datum (optional)", "place": "Ort", "place_ph": "Z. B. Köln oder Aachen",
        "back": "‹ Zurück", "next": "Preis anzeigen ›",
        "res_head": "Ihre Preisindikation", "res_note": "Inklusive professionellem Material, Versicherung und Abstimmung mit der Location. Die Anfahrt wird transparent im Angebot ausgewiesen.",
        "res_trust": "★ 4,9/5 aus 136 Bewertungen · Maßgeschneidertes Angebot in 24 h",
        "wa_btn": "Termin per WhatsApp prüfen", "form_btn": "Angebot anfordern",
        "popular": "Am häufigsten gewählt", "no_date": "Termin nach Absprache", "no_place": "unserer Region",
        "wa_msg": "Hallo Nuno! Ich suche eine {pkg} für eine {occ} am {date} in {place}. Ist der Termin noch frei?",
        "form_msg": "{occ} — {pkg}. Indikation aus dem Preis-Assistenten: {price}.",
        "occs": [("💍", "Hochzeit"), ("🏢", "Firmenfeier"), ("🎉", "Geburtstag"),
                 ("🎪", "Festival"), ("🎃", "Halloween"), ("🥂", "Junggesellenabschied"),
                 ("✨", "Etwas anderes")],
        "pkgs": [("⚡", "Power-Act", "10 Minuten volles Spektakel", 350, 450, 0),
                 ("🔥", "Komplette Feuershow", "±20 Minuten — die beliebteste Wahl", 450, 750, 1),
                 ("🎪", "Festival-Paket", "mehrere Sets bis 5×20 Minuten", 750, 1500, 0),
                 ("💨", "Workshop Feuerspucken", "selbst Feuerspucken lernen", 350, 650, 0),
                 ("🧠", "Nunos Rat", "noch keine Idee — gemeinsam überlegen", 350, 1500, 0)]},
 "fr": {"eyebrow": "💶 Assistant devis", "title": "Votre prix en <em>30 secondes</em>",
        "sub": "Trois clics et vous voyez immédiatement une indication de prix honnête — et si votre date est encore libre.",
        "q1": "Que fêtez-vous ?", "q2": "Quel spectacle convient ?",
        "date": "Date (facultatif)", "place": "Ville", "place_ph": "P. ex. Bruxelles ou Liège",
        "back": "‹ Retour", "next": "Voir mon prix ›",
        "res_head": "Votre indication de prix", "res_note": "Matériel professionnel, assurance et coordination avec le lieu inclus. Le déplacement est indiqué de façon transparente dans le devis.",
        "res_trust": "★ 4,9/5 sur 136 avis · Devis sur mesure sous 24 h",
        "wa_btn": "Vérifier la date sur WhatsApp", "form_btn": "Demander un devis",
        "popular": "Le plus choisi", "no_date": "date à convenir", "no_place": "notre région",
        "wa_msg": "Bonjour Nuno ! Je cherche un {pkg} pour un {occ} le {date} à {place}. Cette date est-elle encore libre ?",
        "form_msg": "{occ} — {pkg}. Indication de l'assistant prix : {price}.",
        "occs": [("💍", "Mariage"), ("🏢", "Fête d'entreprise"), ("🎉", "Anniversaire"),
                 ("🎪", "Festival"), ("🎃", "Halloween"), ("🥂", "Enterrement de vie de célibataire"),
                 ("✨", "Autre chose")],
        "pkgs": [("⚡", "Power-act", "10 minutes de pur spectacle", 350, 450, 0),
                 ("🔥", "Spectacle de feu complet", "±20 minutes — le choix le plus populaire", 450, 750, 1),
                 ("🎪", "Formule festival", "plusieurs sets jusqu'à 5×20 minutes", 750, 1500, 0),
                 ("💨", "Atelier cracheur de feu", "apprenez à cracher le feu en groupe", 350, 650, 0),
                 ("🧠", "Conseil de Nuno", "pas encore d'idée — réfléchissons ensemble", 350, 1500, 0)]},
}

def wizard(lang):
    W = _WIZ[lang]
    occ_chips = "".join(
        f'<button type="button" class="wiz__chip" data-occ="{esc(nm)}">{e} {esc(nm)}</button>'
        for e, nm in W["occs"])
    pkg_chips = "".join(
        f'<button type="button" class="wiz__chip wiz__chip--pkg{" wiz__chip--pop" if pop else ""}" '
        f'data-pkg="{esc(nm)}" data-min="{lo}" data-max="{hi}">'
        + (f'<span class="wiz__pop">{esc(W["popular"])}</span>' if pop else "")
        + f'<b>{e} {esc(nm)}</b><small>{esc(sub)}</small>'
        f'<span class="wiz__range">€{lo}–€{hi}</span></button>'
        for e, nm, sub, lo, hi, pop in W["pkgs"])
    return f'''<section class="wrap bay wiz" id="prijswizard" aria-label="{esc(W["res_head"])}">
    <div class="bay__head"><p class="eyebrow eyebrow--dim rise">{W["eyebrow"]}</p>
    <h2 class="bay__title rise" data-delay="1">{W["title"]}</h2>
    <p class="lede rise" data-delay="2">{esc(W["sub"])}</p></div>
    <div class="wiz__card rise" data-delay="2" data-wiz
         data-contact="{I.url_of(lang, "contact-3")}"
         data-wa-msg="{esc(W["wa_msg"])}" data-form-msg="{esc(W["form_msg"])}"
         data-no-date="{esc(W["no_date"])}" data-no-place="{esc(W["no_place"])}">
      <ol class="wiz__dots" aria-hidden="true"><li class="is-on"></li><li></li><li></li></ol>
      <div class="wiz__step" data-step="1">
        <p class="wiz__q">{esc(W["q1"])}</p>
        <div class="wiz__chips">{occ_chips}</div>
      </div>
      <div class="wiz__step" data-step="2" hidden>
        <p class="wiz__q">{esc(W["q2"])}</p>
        <div class="wiz__chips wiz__chips--pkg">{pkg_chips}</div>
        <div class="wiz__fields">
          <label class="field"><span>{esc(W["date"])}</span><input type="date" data-wiz-date></label>
          <label class="field"><span>{esc(W["place"])}</span><input type="text" data-wiz-place placeholder="{esc(W["place_ph"])}"></label>
        </div>
        <div class="wiz__nav">
          <button type="button" class="wiz__back" data-wiz-back>{esc(W["back"])}</button>
          <button type="button" class="btn" data-wiz-go><span class="btn__dot"></span>{esc(W["next"])}</button>
        </div>
      </div>
      <div class="wiz__step" data-step="3" hidden>
        <p class="wiz__q">{esc(W["res_head"])}</p>
        <p class="wiz__pick" data-wiz-pick></p>
        <p class="wiz__price" data-wiz-price></p>
        <p class="wiz__note">{esc(W["res_note"])}</p>
        <p class="wiz__trust">{esc(W["res_trust"])}</p>
        <div class="wiz__cta">
          <a class="btn wiz__wa" data-wiz-wa href="https://wa.me/31620020723" rel="noopener">{esc(W["wa_btn"])}</a>
          <a class="btn btn--ghost" data-wiz-form href="{I.url_of(lang, "contact-3")}">{esc(W["form_btn"])}</a>
        </div>
        <div class="wiz__nav"><button type="button" class="wiz__back" data-wiz-back>{esc(W["back"])}</button></div>
      </div>
    </div>
  </section>'''

# ------------------------------------------------- SERP-optimalisatie
# Elke <title> en meta-beschrijving wordt een klikmagneet: passende emoji
# vooraan, de belangrijkste zoekwoorden binnen de zichtbare lengte
# (titel ±62 tekens, beschrijving ±158), sterren en vinkjes met de USP's,
# en gegarandeerd uniek over alle 261 pagina's. De H1 op de pagina zelf
# behoudt de volledige, lange zoekwoordenrijke titel.
_SERP_EMOJI = [
    ("🎬", ("video",)),
    ("📸", ("foto", "photo")),
    ("⭐", ("beoordeling", "review", "bewertung", "avis")),
    ("🎃", ("halloween", "griezel", "spook", "horror", "fright")),
    ("💍", ("bruiloft", "trouw", "huwelijk", "wedding", "hochzeit", "mariage")),
    ("🎄", ("kerst", "nieuwjaar", "silvester", "noel", "noël", "christmas", "oud-en-nieuw", "new-year", "neujahr")),
    ("🎆", ("vuurwerk", "firework", "feuerwerk", "artifice")),
    ("💨", ("workshop", "leren-vuurspuwen", "atelier", "cursus")),
    ("⚔️", ("fakir", "spijker", "zwaard", "glasscherven", "nagelbrett", "planche")),
    ("🧠", ("mentalis", "hypno", "gedachte")),
    ("🐍", ("reptiel", "slang", "reptile")),
    ("🛡️", ("veilig", "vergunning", "brandweer", "risico")),
    ("💶", ("kost", "prijs", "prijzen", "tarief", "budget", "goedkoop", "preis", "prix", "price")),
    ("🎉", ("verjaardag", "jubileum", "vrijgezell", "birthday", "geburtstag", "anniversaire", "kinderfeest", "themafeest")),
    ("🏢", ("bedrijfsfeest", "personeelsfeest", "zakelijk", "corporate", "firmen", "entreprise", "teambuilding", "beurs", "bedrijfsuitje")),
    ("🎩", ("entertainer", "artiest", "act")),
]
def _serp_emoji(s):
    s = s.lower()
    for e, keys in _SERP_EMOJI:
        if any(k in s for k in keys):
            return e
    return "🔥"

def _has_emoji(s):
    return any(ord(c) > 0x2300 for c in s)

# terugkerende, niets toevoegende staarten uit de oude WordPress-titels
_TITLE_JUNK = re.compile(
    r"\s*[-–—:|]\s*(het complete antwoord( door vuurspuwer nuno)?|"
    r"de ultieme spectaculaire ervaring|de ultieme gids( voor .*)?|"
    r"\[jouw bedrijfsnaam\])\s*$", re.I)

def _fit_title(t, limit=62):
    t = re.sub(r"\s*\|\s*\[jouw bedrijfsnaam\]", "", t, flags=re.I)
    while True:
        t2 = _TITLE_JUNK.sub("", t).strip()
        if t2 == t: break
        t = t2
    if len(t) <= limit: return t
    for tail in (" | Vuurspuwer Nuno", " — Vuurspuwer Nuno", " – Vuurspuwer Nuno",
                 " | Nuno", " — Nuno", " – Nuno"):
        if t.endswith(tail) and len(t) - len(tail) >= 28:
            t = t[:-len(tail)]
            if len(t) <= limit: return t
    while len(t) > limit:
        idx = max(t.rfind(" | "), t.rfind(" — "), t.rfind(" – "))
        if idx < 25: break
        t = t[:idx].rstrip()
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0].rstrip(" ,.:;–—|-&")
    return t

_RATING_TXT = {"nl": "★ 4,9/5 (136 reviews)", "en": "★ 4.9/5 (136 reviews)",
               "de": "★ 4,9/5 (136 Bewertungen)", "fr": "★ 4,9/5 (136 avis)"}
_SEEN_TITLES = {}

# meerdere unieke zoekwoorden per pagina (Google negeert de keywords-meta,
# maar Bing-familie en AI-zoekers lezen hem wél mee)
_KW_TOPIC = {
 "🎃": "halloween show boeken, halloween entertainment, griezelact",
 "💍": "vuurshow bruiloft, entertainment bruiloft, trouwfeest act",
 "🎄": "kerst entertainment, nieuwjaarsshow, winterevent act",
 "🎆": "vuurwerk alternatief, vuurshow buiten",
 "💨": "workshop vuurspuwen, teambuilding activiteit, vrijgezellenfeest workshop",
 "⚔️": "fakirshow boeken, spijkerbed act, fakir inhuren",
 "🧠": "mentalist boeken, mentalisme show",
 "🐍": "reptielenshow, slangenshow boeken",
 "🛡️": "vuurshow veiligheid, vergunning vuurshow",
 "💶": "vuurspuwer prijs, vuurshow kosten, offerte vuurshow",
 "🎉": "feest entertainment, verjaardag artiest, themafeest act",
 "🏢": "bedrijfsfeest entertainment, personeelsfeest act, zakelijk evenement artiest",
 "🎬": "vuurshow video, showreel vuurspuwer",
 "📸": "vuurshow foto's, vuurspuwer afbeeldingen",
 "⭐": "reviews vuurspuwer, beoordelingen vuurshow",
 "🎩": "entertainer boeken, artiest inhuren",
 "🔥": "vuurshow boeken, vuuract, vuurartiest",
}
_KW_GENERIC = {
 "en": "hire fire breather, book fire show, fakir show, event entertainment, Netherlands, Belgium",
 "de": "Feuerspucker buchen, Feuershow buchen, Fakirshow, Event-Entertainment, Niederlande, Belgien",
 "fr": "engager cracheur de feu, spectacle de feu, spectacle fakir, animation événement, Pays-Bas, Belgique",
}
def _serp_kw(p, kind, emo, lang="nl"):
    parts = []
    if p.get("keywords"): parts.append(p["keywords"])
    if lang != "nl":
        # de onderwerpstabel hieronder is Nederlands; een anderstalige pagina
        # krijgt zijn eigen zoekwoorden of anders de algemene set in zijn taal
        parts.append(_KW_GENERIC[lang])
        seen, out = set(), []
        for part in parts:
            for kw in [k.strip() for k in part.split(",")]:
                if kw and kw.lower() not in seen:
                    seen.add(kw.lower()); out.append(kw)
        return ", ".join(out)
    parts.append(_KW_TOPIC.get(emo, _KW_TOPIC["🔥"]))
    if kind == "city" and p.get("slug") in CITY_LABEL:
        c = CITY_LABEL[p["slug"]]
        parts.append(f"vuurspuwer {c}, vuurshow {c}, entertainment {c}")
    parts.append("vuurspuwer inhuren, vuurspuwer boeken, Nederland, België")
    seen, out = set(), []
    for kw in ", ".join(parts).split(", "):
        k = kw.strip()
        if k and k.lower() not in seen:
            seen.add(k.lower()); out.append(k)
    return ", ".join(out)

def _serp(title, desc, p, kind, lang):
    slug = p.get("slug", "")
    topic = f"{slug} {title}"
    emo = _serp_emoji(topic)
    # stadspagina's: de oude WordPress-marketingtitels volledig vervangen
    # door een strak, zoekwoordenrijk formaat per stad
    if kind == "city" and lang == "nl" and slug in CITY_LABEL:
        city = CITY_LABEL[slug]
        title = f"🔥 Vuurspuwer inhuren in {city} | Vuurshow vanaf €350"
        desc = (f"📍 Vuurspuwer Nuno in {city}: vuurshow, fakirshow & workshop "
                f"vuurspuwen ★ 4,9/5 (136 reviews) ✓ €350–€1500 ✓ Binnen 24 uur "
                f"een offerte voor jouw feest of event in {city}.")
    else:
        title = _fit_title(title)
        if not _has_emoji(title):
            title = f"{emo} {title}"
        if len(title) <= 48 and "nuno" not in title.lower():
            title += " | Nuno"
        # beschrijving: bestaande goede teksten houden maar inkorten en van
        # sterren voorzien; kale tekstfragmenten worden een echte advertentie
        crafted = p.get("seo_desc") or ""
        rating = _RATING_TXT[lang]
        if not crafted:
            kern = _fit_title(p.get("title", ""), 64)
            kern = re.sub(r"^[^\w€]+\s*", "", kern).rstrip("?.!")
            desc = (f"{emo} {kern}? Tips & antwoorden van vuurspuwer en fakir "
                    f"Nuno {rating} ✓ Shows van €350 tot €1500 in NL & BE "
                    f"✓ Binnen 24 uur offerte.")
        else:
            desc = crafted
            if "4,9" not in desc and "4.9" not in desc and len(desc) + len(rating) + 1 <= 156:
                desc = f"{desc.rstrip()} {rating}"
            if not _has_emoji(desc) and "★" not in desc and "✓" not in desc:
                desc = f"{emo} {desc}"
    if len(desc) > 160:
        desc = desc[:158].rsplit(" ", 1)[0].rstrip(" ,;:–—-") + "…"
    # uniek over de hele site: bij een botsing een onderscheidend achtervoegsel
    key = title.lower()
    if _SEEN_TITLES.get(key, slug) != slug:
        for extra in (" | Tips", " | Gids", " | Info", f" | {slug[-12:]}"):
            cand = _fit_title(f"{title}{extra}", 70)
            if cand.lower() not in _SEEN_TITLES:
                title = cand; key = title.lower(); break
    _SEEN_TITLES.setdefault(key, slug)
    return title, desc, _serp_kw(p, kind, emo, lang)

_ALT_GENERIEK = {
    "nl": "Vuurspuwer Nuno spuwt vuur tijdens een spectaculaire vuurshow op een evenement",
    "en": "Fire breather Nuno breathes fire during a spectacular fire show at an event",
    "de": "Feuerspucker Nuno spuckt Feuer w\u00e4hrend einer spektakul\u00e4ren Feuershow auf einer Veranstaltung",
    "fr": "Le cracheur de feu Nuno crache du feu lors d\u2019un spectacle de feu spectaculaire",
}

def render(p, kind, extra_schema=None, extra_html="", lang="nl", path=None, alternates=None):
    L = I.UI[lang]
    if not p.get("no_toc"):
        p = {**p, "body": _add_toc(p.get("body", ""), lang)}
    title = p["seo_title"] or f'{p["title"]} | Vuurspuwer Nuno'
    desc  = p["seo_desc"] or text_of(p["body"], 155)
    title, desc, meta_kw = _serp(title, desc, p, kind, lang)
    path  = path or (f'/{p["slug"]}/' if p["slug"] else "/")
    url   = SITE + path

    # foto-strip na ±25% en video-strip na ±62% van de inhoud (niet op
    # galerij-, contact- en indexpagina's, en nooit direct op elkaar),
    # plus registratie in de image-sitemap van deze pagina
    _vg_ld = []
    if (kind in ("page", "post", "city") and p["slug"] not in _MIDGAL_SKIP
            and len(p.get("body", "")) > 1500):
        _mg_html, _mg_fulls = midgal(lang, p["slug"])
        _vg_html, _ld = vidgal(lang, url)
        _body, _vid_in = _insert_two(p["body"], _mg_html, _vg_html)
        p = {**p, "body": _body}
        SITEMAP_IMG[path] = list(dict.fromkeys(SITEMAP_IMG.get(path, []) + _mg_fulls))
        if _vid_in:
            _vg_ld = _ld
    home  = "/" if lang == "nl" else f"/{lang}/"
    trail = [(L["crumb_home"], home)]
    if kind == "post":   trail.append(("Blog", "/blog/"))
    elif kind == "city" and lang == "nl":
        trail.append(("Locaties", "/locaties-vuurshows-nederland-belgie/"))
    trail.append((p["title"], None))
    crumb_html, crumb_data = crumbs(trail)

    # hreflang-verwijzingen tussen de taalversies van deze pagina
    hreflang = ""
    if alternates:
        for l in ("nl", "en", "de", "fr"):
            if l in alternates:
                hreflang += f'<link rel="alternate" hreflang="{l}" href="{SITE}{alternates[l]}">\n'
        hreflang += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alternates["nl"]}">'
    HDR, FTR = chrome(lang)
    FTR = FTR.replace('<div class="foot__bar">', lang_row(lang, alternates) + '\n  <div class="foot__bar">')

    # een korte eigen intro: de eerste alinea, tenzij die de titel herhaalt
    # (of de pagina er expliciet géén wil, zoals de contactpagina)
    if "intro" in p:
        intro = p["intro"]
    else:
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
        # de alt van een hergebruikte foto mag geen andere plaats noemen dan
        # de pagina zelf (de festivalfoto droeg "Ternat" mee uit WordPress)
        if kind == "city" and p["slug"] in CITY_LABEL:
            ia = f"Vuurspuwer Nuno spuwt een vuurbal tijdens een vuurshow \u2013 boekbaar in {CITY_LABEL[p['slug']]} en omgeving"
        elif ia and "Ternat" in ia and "ternat" not in p["slug"].lower():
            ia = _ALT_GENERIEK.get(lang, _ALT_GENERIEK["nl"])
        p = {**p, "img": (iu, ia)}

    # elk blogbericht draagt dezelfde omslag: donker, alleen Nuno en de vlam
    if kind == "post":
        p = {**p, "img": ("/assets/media/post-cover.webp",
                          "Vuurspuwer Nuno met een metershoge vuurbal tegen een zwarte nachtlucht")}

    # De kop van elke pagina: de uitgelichte foto beeldvullend, tot achter
    # het menu, en nooit bijgesneden — de foto zelf past er volledig in
    # (contain), met dezelfde foto wazig als decor eromheen (cover).
    eyebrow = p.get("eyebrow") or ("Vuurshow op locatie" if kind == "city" and lang == "nl"
                                   else "Blog" if kind == "post" else L["eyebrow_default"])
    # Zichtbare datum: alleen waar hij de lezer iets zegt — bij artikelen
    # (hoe actueel is dit?) en bij pagina's die op actualiteit drijven, zoals
    # de prijzen. De 'bijgewerkt'-datum is een plaatshouder die write() door
    # de echte grootboekdatum vervangt, zodat zichtbaar en schema gelijk zijn.
    datumregel = ""
    if kind == "post" or p.get("toon_datum"):
        L_DAT = _DATUM_LBL[lang]
        pub = p.get("date") or ""
        delen = []
        if pub and kind == "post":
            delen.append(f'<time datetime="{pub}">{L_DAT["pub"]} {nl_datum(pub, lang)}</time>')
        delen.append(f'<time datetime="{TODAY}">{L_DAT["mod"]} {TODAY_LOC[lang]}</time>')
        datumregel = f'<p class="pdate">{" · ".join(delen)}</p>'

    preload = ""
    if p.get("img"):
        iu, ia = p["img"]
        if iu.startswith("/"):
            SITEMAP_IMG[path] = list(dict.fromkeys([SITE + iu] + SITEMAP_IMG.get(path, [])))
        ss = srcset_of(iu)
        ss_attr = f' srcset="{ss}" sizes="100vw"' if ss else ""
        pre_ss = f' imagesrcset="{ss}" imagesizes="100vw"' if ss else ""
        preload = f'<link rel="preload" as="image" href="{esc(iu)}"{pre_ss} fetchpriority="high">'
        hero = f'''<header class="phero">
    <img class="phero__bg" src="{esc(iu)}"{ss_attr} alt="" aria-hidden="true" fetchpriority="high" decoding="async">
    <img class="phero__img" src="{esc(iu)}"{ss_attr} alt="{esc(ia)}" fetchpriority="high" decoding="async">
    <div class="phero__veil" aria-hidden="true"></div>
    <div class="phero__body wrap">
      {crumb_html}
      <p class="eyebrow">{esc(eyebrow)}</p>
      <h1 class="page__title">{esc(p["title"])}</h1>
      {datumregel}
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

    # Google Afbeeldingen: elke foto op deze pagina krijgt een eigen
    # ImageObject met een unieke naam op basis van de paginatitel, plus
    # licentie-info (via _license_images). De kopfoto wordt gemarkeerd
    # als representativeOfPage.
    _pg_ld = []
    if (kind in ("page", "post", "city") and p["slug"] not in _MIDGAL_SKIP
            and SITEMAP_IMG.get(path)):
        _pg_ld = [page_images_ld(lang, url, p["title"], SITEMAP_IMG[path])]

    graph = [crumb_data]
    if kind == "post":
        _wc = len(re.findall(r"\w+", text_of(p["body"])))
        graph.append({"@context": "https://schema.org", "@type": "BlogPosting",
                      "headline": p["title"], "datePublished": p["date"],
                      "dateModified": TODAY,
                      "description": desc, "mainEntityOfPage": url,
                      "wordCount": _wc,
                      "timeRequired": f"PT{max(1, round(_wc / 220))}M",
                      **({"image": (SITE + p["img"][0] if p["img"][0].startswith("/") else p["img"][0])} if p.get("img") else {}),
                      "author": {"@type": "Person", "name": "Nuno",
                                 "@id": f"{SITE}/#nuno",
                                 "url": f"{SITE}/over-nuno/"},
                      **({"articleSection": p["cat_label"]} if p.get("cat_label") else {}),
                      **({"keywords": p["keywords"]} if p.get("keywords") else {}),
                      "publisher": {"@id": f"{SITE}/#business"}})
    if extra_schema:
        graph.extend(extra_schema) if isinstance(extra_schema, list) else graph.append(extra_schema)
    graph.extend(_vg_ld)
    graph.extend(_pg_ld)
    _augment_rich_results(graph, lang, page_desc=desc, page_url=url,
        page_img=(SITE + p["img"][0]) if p.get("img") and p["img"][0].startswith("/") else None,
        page_words=len(re.findall(r"\w+", text_of(p["body"]))))
    ogv = ""
    if p.get("og_video"):
        vu, vw, vh = p["og_video"]
        ogv = (f'<meta property="og:video" content="{SITE}{vu}">\n'
               f'<meta property="og:video:secure_url" content="{SITE}{vu}">\n'
               '<meta property="og:video:type" content="video/mp4">\n'
               f'<meta property="og:video:width" content="{vw}">\n'
               f'<meta property="og:video:height" content="{vh}">')
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>' for g in graph)

    doc = f'''<!doctype html>
<html lang="{I.HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0A0705">
<meta name="color-scheme" content="dark">
<meta name="application-name" content="Vuurspuwer Nuno">
<meta name="apple-mobile-web-app-title" content="Vuurspuwer Nuno">
<meta name="msapplication-TileColor" content="#0A0705">
<style>html{{background:#0A0705;color-scheme:dark}}html[data-theme="light"]{{background:#FAF4E9;color-scheme:light}}</style>
<script>try{{if(localStorage.vsTheme==="light")document.documentElement.setAttribute("data-theme","light")}}catch(e){{}}</script>
<link rel="mask-icon" href="/assets/pinned-tab.svg" color="#FFB020">
<link rel="preconnect" href="https://www.googletagmanager.com">
{GTAG}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(meta_kw)}">
{'<meta name="robots" content="noindex,follow">' if p.get("noindex") else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'}
<meta name="author" content="Nuno (Vuurspuwer Nuno)">
<link rel="canonical" href="{url}">
{hreflang}
<meta property="og:type" content="{'article' if kind == 'post' else 'website'}">
<meta property="og:site_name" content="Vuurspuwer Nuno">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE + og_image_for(p["img"][0] if p.get("img") else "")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(p["img"][1] if p.get("img") else "Vuurspuwer Nuno")}">
<meta name="twitter:card" content="summary_large_image">
{ogv}
<link rel="alternate" type="application/rss+xml" title="Blog — Vuurspuwer Nuno" href="/feed.xml">
<link rel="sitemap" type="application/xml" title="Sitemap" href="/sitemap.xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/icon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v={VER}">
{preload}
{ld}
{spec_rules(lang)}
</head>
<body>
<div class="readbar" aria-hidden="true"></div>
<a class="skip" href="#top">{L.get("skip", "Naar de inhoud")}</a>
{IGNITION}{STAGE}{HDR}
<main class="shell" id="top">
  {hero}

  <div class="wrap bay">
    <div class="prose prose--page">
{p["body"]}
    </div>
  </div>
{extra_html}
  <section class="wrap bay cta">
    <h2 class="bay__title">{L["cta_title"]}</h2>
    <p class="lede">{L["cta_lede"]}</p>
    <div class="hero__actions">
      <a class="btn" href="tel:+31620020723"><span class="btn__dot"></span>+31 6 200 207 23</a>
      <a class="btn btn--ghost" href="https://wa.me/31620020723">{L["cta_whatsapp"]}</a>
      <a class="btn btn--ghost" href="{I.url_of(lang, "contact-3")}">{L["cta_form"]}</a>
    </div>
  </section>
</main>
{FTR}
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''
    if lang != "nl":
        for _a, _b in _CHROME_LANG[lang].items():
            doc = doc.replace(_a, _b)
    return doc

# ----------------------------------------------------- eerlijke lastmod
# Google negeert <lastmod> zodra het onbetrouwbaar blijkt — en tot nu toe
# stempelde elke build álle pagina's op "vandaag". Daarom een grootboek
# (lastmod.json, meegecommit): per pagina een vingerafdruk van de inhoud
# (zonder vluchtige delen zoals ?v=-versies en datums); de datum schuift
# alleen op wanneer de inhoud écht verandert. Sitemap-lastmod en
# dateModified van artikelen volgen dit grootboek.
_LEDGER_F = "lastmod.json"
try:
    _LEDGER = json.load(open(_LEDGER_F, encoding="utf-8"))
except Exception:
    _LEDGER = {}
_WRITTEN_PATHS = set()
# de datums zoals ze vóór deze build in het grootboek stonden, om achteraf
# te kunnen zien hoeveel er daadwerkelijk verschoven
_LEDGER_VOOR = {p: v.get("d") for p, v in _LEDGER.items()}
# Zichtbare datums in élke taal van de site, ook de Duitse vorm met punt
# ("2. September 2026"). Tot nu toe werd alleen de Nederlandse vorm
# gefilterd, waardoor elke Engelse, Duitse en Franse pagina met een
# "bijgewerkt op"-regel bij elke bouw een nieuwe vingerafdruk kreeg — en
# dus elke dag een nieuwe lastmod, zonder dat er iets veranderd was.
_ALLE_MAANDEN = sorted({m for l in MONTHS_LOC.values() for m in l[1:] if m}, key=len, reverse=True)
_NL_DATUM = r"\d{1,2}\.? (?:" + "|".join(map(re.escape, _ALLE_MAANDEN)) + r") \d{4}"
# Wat hier uit gefilterd wordt telt niet als inhoudswijziging. Naast de
# assethash en datums hoort daar ook de laadplumbing bij: speculatieregels,
# het poster-attribuut van een video en de sitebrede blokken in de
# voettekst (het linkoverzicht, de partnerkaart) en de sameAs-lijst met
# profielen zeggen niets over wat er op de pagina zelf staat. Een lastmod
# die daarop verspringt is een leugen tegen Google — en die vertrouwt
# lastmod sitebreed of helemaal niet.
_VOLATILE = re.compile(
    r"<script type=\"speculationrules\">.*?</script>"
    r"|<nav class=\"fseo\".*?</nav>"
    r"|<!--PARTNER-->.*?</a>\n\n  "
    r"|\"sameAs\": \[[^\]]*\]"
    r"|\bdata-poster=\"[^\"]*\"|\bposter=\"[^\"]*\""
    r"|\?v=[0-9a-f]+|\d{4}-\d{2}-\d{2}|" + _NL_DATUM, re.S)

# Wat telt als "de pagina is veranderd"? De inhoud in <main>, en dan zonder
# de dingen die niet van deze pagina zíjn: de fotostrips en videostrips
# (decor dat overal gelijk is), de "lees ook"-lijst en de broodkruimels
# (navigatie die verschuift zodra er ergens anders een artikel bijkomt of
# verdwijnt) en de doelen van links (een link die voortaan rechtstreeks
# naar zijn eindadres wijst, is geen nieuwe tekst). Header, voettekst,
# chatkaart en cookiekaart staan buiten <main> en tellen dus nooit mee —
# een vertaalde voettekstregel is geen reden om 60 pagina's als
# "vandaag gewijzigd" aan te bieden. Google vertrouwt lastmod sitebreed
# of helemaal niet, dus dit moet precies zijn.
_MAIN   = re.compile(r"<main\b.*?</main>", re.S)
_DECOR  = re.compile(r"<aside\b.*?</aside>"
                     r"|<section class=\"wrap bay relposts\"[^>]*>.*?</section>"
                     r"|<nav class=\"crumbs\".*?</nav>"
                     # het gedeelde FAQ-blok onder artikelen: per rubriek hetzelfde,
                     # dus geen inhoud van de pagina zelf
                     r"|<section class=\"wrap bay\" aria-label=\"Veelgestelde vragen\">.*?</section>"
                     r"|\bhref=\"[^\"]*\""
                     # toegankelijkheidslabels, ondertitelingstaal en verborgen
                     # formuliervelden: geen inhoud, wel tekst die per taal wisselt
                     r"|\b(?:aria-label|srclang|label)=\"[^\"]*\""
                     r"|<input type=\"hidden\"[^>]*>", re.S)
def _basis(doc):
    m = _MAIN.search(doc)
    kern = m.group(0) if m else doc
    return _VOLATILE.sub("", _DECOR.sub("", kern))

def _lastmod(path, doc):
    _WRITTEN_PATHS.add(path)
    h = hashlib.sha1(_basis(doc).encode("utf-8")).hexdigest()[:16]
    old = _LEDGER.get(path)
    if old and old.get("h") == h:
        return old["d"]
    _LEDGER[path] = {"h": h, "d": TODAY}
    return TODAY

# ------------------------------------------- contextuele links naar buiten
# Het eigen artiestenprofiel op EntertainerShow staat als kaart in de
# voettekst, maar een link telt pas echt mee als hij ergens in een zin
# hoort. Daarom drie stuks, met de hand geplaatst, elk op de plek waar de
# lezer er iets aan heeft: wie is Nuno, wat kost een artiest, en hoe boek
# je er een. Meer zou een patroon worden in plaats van een aanbeveling.
#
# De ankerzin staat maar op één pagina op de hele site. Verandert die tekst
# ooit, dan valt de bouw om in plaats van dat de link stilletjes verdwijnt.
_ES_URL = "https://entertainershow.com/artiest/vuurspuwer-nuno/"

def _es(tekst):
    return f'<a href="{_ES_URL}" target="_blank" rel="noopener">{tekst}</a>'

_ES_LINKS = {
 # Over Nuno: wie hij is en waar hij nog meer te vinden is.
 "over-nuno": (
   "ik breng een niveau van professionaliteit en spektakel dat wordt erkend.",
   "ik breng een niveau van professionaliteit en spektakel dat wordt erkend. "
   "Ook buiten deze site ben ik te vinden: op "
   + _es("mijn profiel als vuurspuwer op EntertainerShow")
   + ", het Europese entertainmentnetwerk, ziet u wat ik speel en boekt u "
     "rechtstreeks bij mij."),
 # Gids over artiesten boeken: precies het onderwerp van de link.
 "artiesten-boeken-tips": (
   "De kosten kunnen variëren afhankelijk van de populariteit, de reisafstand "
   "en de duur van het optreden.",
   "De kosten kunnen variëren afhankelijk van de populariteit, de reisafstand "
   "en de duur van het optreden. Let ook op de route waarlangs je boekt: via een "
   "bemiddelingsbureau komt er meestal een commissie bovenop de gage, terwijl je "
   "op een netwerk als "
   + _es("EntertainerShow, waar je artiesten rechtstreeks boekt")
   + ", met de artiest zelf schakelt en die opslag wegvalt."),
 # Prijzenpagina: wie prijzen vergelijkt, wil weten wat er bovenop komt.
 "wat-kost-een-vuurspuwer": (
   "van een enkele fakkel tot complete producties.",
   "van een enkele fakkel tot complete producties. Bij een bemiddelingsbureau "
   "komt daar vaak nog een commissie bovenop; via deze site of via "
   + _es("het artiestenprofiel van Nuno op EntertainerShow")
   + " boek je rechtstreeks en betaal je die opslag niet."),
}

def _contextlinks(slug, doc):
    """De met de hand gekozen link in de lopende tekst van één pagina."""
    paar = _ES_LINKS.get(slug)
    if not paar:
        return doc
    anker, met = paar
    n = doc.count(anker)
    if n != 1:
        raise SystemExit(
            f"  ✖ contextlink {slug}: ankerzin {n}x gevonden, verwacht 1x.\n"
            "    De tekst van die pagina is gewijzigd; werk de zin bij in _ES_LINKS.")
    return doc.replace(anker, met, 1)

def write(slug, doc):
    doc = _contextlinks(slug, doc)
    doc = _avifize(doc)
    path = f"/{slug}/" if slug else "/"
    mod = _lastmod(path, doc)
    doc = doc.replace(f'"dateModified": "{TODAY}"', f'"dateModified": "{mod}"')
    if mod != TODAY:                       # zichtbare datum meeschuiven
        doc = doc.replace(f'<time datetime="{TODAY}">', f'<time datetime="{mod}">')
        for _l, _vandaag in TODAY_LOC.items():
            doc = doc.replace(_vandaag, nl_datum(mod, _l))
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)


# ------------------------------------------------- de fotopagina
# Eigen galerij in plaats van de oude WordPress-inhoud: alle foto's,
# klik opent de lightbox, en elke foto staat als ImageObject in de markup.
FOTOS = [
    ("galavuur",      "galavuur-900.webp",      "galavuur-1080.webp",     900, 1600,
     "Vuurzuil op een galafeest",
     "In wit gala-kostuum blaast Nuno een metershoge vuurzuil tussen bloemen en kaarsen op een chique feest"),
    ("zonsondergang", "zonsondergang-900.webp", "zonsondergang-1152.webp", 900, 1600,
     "Vuurbal boven het water bij zonsondergang",
     "Vuurspuwer Nuno in glitterjasje blaast een vuurbal over het water bij zonsondergang voor publiek"),
    ("nachtvuur",     "nachtvuur-900.webp",     "nachtvuur-960.webp",     900, 900,
     "Vuurbal boven de nachtelijke straat",
     "Vuurspuwer Nuno blaast met twee fakkels een grote vuurbal recht omhoog in de nacht"),
    ("terrasvuur",    "terrasvuur-480.webp",    "terrasvuur-582.webp",    480, 792,
     "Vuurshow op het terras in de regen",
     "Geknield blaast vuurspuwer Nuno een lange vlam over het terras, zelfs in de regen"),
    ("portret",       "portret-900.webp",       "portret-1080.webp",      900, 1124,
     "Portret in het stagelicht",
     "Portret van vuurspuwer en mentalist Nuno met hoed in paars-rood stagelicht"),
    ("vuurhart",        "vuurhart-900.webp",        "vuurhart-998.webp",        900, 1125,
     "Vuurbal in hartvorm",
     "Vuurspuwer Nuno blaast een vuurbal in de vorm van een hart tegen de zomerlucht"),
    ("cirque",          "cirque-900.webp",          "cirque-1080.webp",         900, 1332,
     "Circusavond: publiek op het spijkerbed",
     "Toeschouwer staat op het spijkerbed op Nuno tijdens een spectaculaire circusavond met confetti"),
    ("spijkersandwich", "spijkersandwich-900.webp", "spijkersandwich-1125.webp", 900, 892,
     "De spijker-sandwich in de nachtclub",
     "Fakiract in de club: Nuno ligt tussen twee spijkerbedden terwijl een toeschouwer er bovenop staat"),
    ("themafakir",      "themafakir-900.webp",      "themafakir-1056.webp",     900, 1745,
     "Fakiract op een themafeest",
     "Gast staat op het spijkerbord op Nuno tijdens een Aziatisch themafeest, geholpen door twee dames in kimono"),
    ("familiefest",     "familiefest-480.webp",     "familiefest-640.webp",     480, 965,
     "Vuurbal op het familiefestival",
     "Vuurspuwer Nuno in rood circusjasje blaast een vuurbal boven het publiek op een zomers familiefestival"),
    ("vuurzee",     "vuurzee-900.webp",     "vuurzee-1234.webp",     900, 899,
     "Vuurzee in de uitgaansstraat",
     "Vuurspuwer Nuno blaast een enorme vuurzee met vonkenregen in een uitgaansstraat bij nacht"),
    ("straatfakir", "straatfakir-900.webp", "straatfakir-1081.webp", 900, 599,
     "Fakirshow op straat: publiek staat óp Nuno",
     "Fakiract op straat: twee toeschouwers staan op Nuno terwijl hij op het spijkerbed ligt"),
    ("glasact",     "glasact-900.webp",     "glasact-1600.webp",     900, 600,
     "Glasscherven-act in het theater",
     "Nuno steunt met zijn handen in de glasscherven tijdens een theatershow"),
    ("podium",      "podium-900.webp",      "podium-1024.webp",      900, 662,
     "Festivalpodium voor duizenden",
     "Nuno op het festivalpodium met vuur boven een juichende festivalmenigte"),
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

# ------------------------------------------------- foto-meta per pagina
# Elke foto heeft een bijschrift en alt-tekst in vier talen (de
# galerijteksten); per pagina krijgt elke getoonde foto daarmee een eigen
# ImageObject met een unieke naam op basis van de paginatitel — zo leest
# Google Afbeeldingen context, licentie en maker bij álle foto's.
_IMG_CAPS = {}
for _k, _t, _full, _w, _h, _cap, _alt in FOTOS:
    _IMG_CAPS.setdefault(_k, {})["nl"] = (_cap, _alt)
for _l in ("en", "de", "fr"):
    for _k, (_cap, _alt) in I.PAGES[_l]["fotos"]["captions"].items():
        _IMG_CAPS.setdefault(_k, {})[_l] = (_cap, _alt)
_IMG_BY_URL = {}
for _k, _t, _full, _w, _h, _c, _a in FOTOS:
    _IMG_BY_URL[f"{SITE}/assets/media/{_full}"] = _k
for _k, _t, _full, _w, _h, _kw in _MIDGAL_IMGS:
    _IMG_BY_URL.setdefault(f"{SITE}/assets/media/{_full}", _k)

_PGAL_NAME = {"nl": "Foto's bij", "en": "Photos for",
              "de": "Fotos zu", "fr": "Photos pour"}

def _short_title(t, limit=48):
    t2 = re.split(r"\s*[|–—]\s*", t)[0].strip() or t
    if len(t2) > limit:
        t2 = t2[:limit].rsplit(" ", 1)[0].rstrip(" ,.:;-")
    return t2

def page_images_ld(lang, url, title, img_urls):
    kern = _short_title(title)
    items = []
    for n, iu in enumerate(img_urls[:15], 1):
        base = _IMG_BY_URL.get(iu)
        caps = _IMG_CAPS.get(base, {}) if base else {}
        pair = caps.get(lang) or caps.get("nl")
        if pair:
            naam = f"{pair[0]} — {kern}"
            alt = pair[1]
        else:
            naam = f"{kern} — Vuurspuwer Nuno"
            alt = kern
        node = {"@type": "ImageObject", "@id": f"{url}#foto-{n}",
                "name": naam,
                "description": alt,
                "contentUrl": iu, "url": iu,
                "inLanguage": I.HTML_LANG[lang]}
        if n == 1:
            node["representativeOfPage"] = True
        items.append(node)
    return {"@context": "https://schema.org", "@type": "ImageGallery",
            "@id": f"{url}#fotogalerij",
            "name": f"{_PGAL_NAME[lang]}: {kern}",
            "url": url, "inLanguage": I.HTML_LANG[lang],
            "about": {"@id": f"{SITE}/#business"},
            "image": items}

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

# -------------------------------------------- Halloween-thema en prijslinks
_HW = {
 "nl": dict(eyeb="Aftellen naar Halloween", d="dagen", h="uren", m="min", s="sec",
            sub="Oktober loopt elk jaar als eerste vol — zet je datum nu vast",
            cta="Check je Halloween-datum",
            live="🎃 Het is zover — laatste kans voor een boeking dit jaar!",
            cities="Halloween-act boeken per stad",
            cities_p="Nuno speelt in oktober door heel Nederland en België — van Fright Night tot spooktocht en themafeest. Kies je stad voor lokale informatie:"),
 "en": dict(eyeb="Countdown to Halloween", d="days", h="hours", m="min", s="sec",
            sub="October fills up first every year — lock in your date now",
            cta="Check your Halloween date",
            live="🎃 It's here — last chance to book this year!",
            cities="Book a Halloween act by city",
            cities_p="In October Nuno performs across the Netherlands and Belgium — from fright nights to haunted trails. Pick your city for local details:"),
 "de": dict(eyeb="Countdown bis Halloween", d="Tage", h="Std", m="Min", s="Sek",
            sub="Der Oktober ist jedes Jahr zuerst ausgebucht — sichern Sie sich jetzt Ihren Termin",
            cta="Halloween-Termin prüfen",
            live="🎃 Es ist so weit — letzte Chance für dieses Jahr!",
            cities="Halloween-Act nach Stadt buchen",
            cities_p="Im Oktober tritt Nuno in den ganzen Niederlanden und Belgien auf — von Fright Nights bis Gruseltouren. Wählen Sie Ihre Stadt:"),
 "fr": dict(eyeb="Compte à rebours d'Halloween", d="jours", h="heures", m="min", s="sec",
            sub="Octobre se remplit chaque année en premier — bloquez votre date maintenant",
            cta="Vérifier votre date d'Halloween",
            live="🎃 C'est le moment — dernière chance de réserver cette année !",
            cities="Réserver une animation Halloween par ville",
            cities_p="En octobre, Nuno se produit partout aux Pays-Bas et en Belgique — des fright nights aux parcours hantés. Choisissez votre ville :"),
}

def hw_top(lang):
    L = _HW[lang]
    cells = "".join(f'<span class="hw__cell"><b data-hw="{k}">–</b><i>{L[k]}</i></span>'
                    for k in ("d", "h", "m", "s"))
    return f'''<div class="hw" id="hwBox" data-live="{esc(L["live"])}">
<span class="hw__bat hw__bat--1" aria-hidden="true">🦇</span>
<span class="hw__bat hw__bat--2" aria-hidden="true">🦇</span>
<span class="hw__bat hw__bat--3" aria-hidden="true">👻</span>
<p class="hw__eyebrow">🎃 {esc(L["eyeb"])} <b data-hw="y">{TODAY[:4]}</b></p>
<div class="hw__timer" role="timer">{cells}</div>
<p class="hw__sub">{esc(L["sub"])}</p>
<a class="btn hw__cta" href="{I.url_of(lang, "contact-3")}"><span class="btn__dot"></span>{esc(L["cta"])}</a>
</div>'''

def hw_cities(lang):
    L = _HW[lang]
    links = "".join(f'<li><a href="/{_sp}/">🎃 {esc(n)}</a></li>'
                    for k, (n, _sf, _sp) in MX.CITIES.items())
    return (f'<section class="wrap bay hwcities"><h2 class="bay__title">{esc(L["cities"])}</h2>'
            f'<p class="hwcities__p">{esc(L["cities_p"])}</p>'
            f'<ul class="citylist">{links}</ul></section>')

# ------------------------------------------------- regio-dwarslinks (de/fr)
# De Duitse en Franse regiopagina's zonder Nederlandse tegenhanger
# (Düsseldorf, Duisburg, Namur, Charleroi, Mons) werden door niets gelinkt:
# ze stonden alleen in de sitemap. Een sitemap regelt ontdekking, interne
# links regelen prioriteit — dus krijgen alle regiopagina's van een taal
# hier een dwarsverwijzing naar elkaar.
_REGIO_KOP = {
 "de": ("Feuershow in Ihrer Stadt",
        "Nuno tritt regelmäßig im deutschen Grenzgebiet auf — wählen Sie Ihre Stadt."),
 "fr": ("Spectacle de feu dans votre ville",
        "Nuno se produit régulièrement en Belgique francophone — choisissez votre ville."),
 "en": ("Fire show in your region",
        "Nuno performs across the Netherlands, Belgium and the German border region."),
}
def regio_steden(lang):
    """[(stadsnaam, pad)] van álle regiopagina's van een taal."""
    uit = []
    for nl_city, R in I.REGIO_PAGES.get(lang, {}).items():
        uit.append((R["stad"], f"/{lang}/{I.REGIO_SLUGS[lang][nl_city]}/"))
    for loc, R in I.STANDALONE_REGIO.get(lang, {}).items():
        uit.append((R["stad"], f"/{lang}/{loc}/"))
    return sorted(uit)

def regio_links(lang, skip=None):
    if lang not in _REGIO_KOP:
        return ""
    steden = [(n, u) for n, u in regio_steden(lang) if u != skip]
    if not steden:
        return ""
    kop, sub = _REGIO_KOP[lang]
    li = "".join(f'<li><a href="{u}">📍 {esc(n)}</a></li>' for n, u in steden)
    return (f'<section class="wrap bay hwcities"><h2 class="bay__title">{esc(kop)}</h2>'
            f'<p class="hwcities__p">{esc(sub)}</p>'
            f'<ul class="citylist">{li}</ul></section>')

_PRIJS_STRIP = {
 "nl": ("Benieuwd naar de kosten?", "Bekijk alle prijzen & pakketten — vanaf €350"),
 "en": ("Curious about the cost?", "See all prices & packages — from €350"),
 "de": ("Neugierig auf die Kosten?", "Alle Preise & Pakete ansehen — ab 350 €"),
 "fr": ("Curieux du prix ?", "Voir tous les prix & forfaits — dès 350 €"),
}
def prijs_strip(lang):
    t, a = _PRIJS_STRIP[lang]
    return (f'<section class="wrap bay pstrip"><p>💶 <strong>{esc(t)}</strong> '
            f'<a href="{I.url_of(lang, "wat-kost-een-vuurspuwer")}">{esc(a)}</a></p></section>')

# het gelegenheden-linkweb: elke show- en gelegenheid-pagina verwijst naar
# de andere gelegenheden, zodat Google de structuur meteen begrijpt
_OCC_HEAD = {"nl": "Populair voor deze gelegenheden", "en": "Popular occasions",
             "de": "Beliebte Anlässe", "fr": "Occasions populaires"}
_OCC_LBL = {
 "vuurshow-bruiloft":       {"nl": "💍 Bruiloften", "en": "💍 Weddings", "de": "💍 Hochzeiten", "fr": "💍 Mariages"},
 "vuurshow-bedrijfsfeest":  {"nl": "🏢 Bedrijfsfeesten", "en": "🏢 Corporate events", "de": "🏢 Firmenfeiern", "fr": "🏢 Fêtes d'entreprise"},
 "vuurshow-verjaardag":     {"nl": "🎉 Verjaardagen & jubilea", "en": "🎉 Birthdays", "de": "🎉 Geburtstage", "fr": "🎉 Anniversaires"},
 "vuurshow-festival":       {"nl": "🎪 Festivals", "en": "🎪 Festivals", "de": "🎪 Festivals", "fr": "🎪 Festivals"},
 "vrijgezellenfeest":       {"nl": "🥂 Vrijgezellenfeesten", "en": "🥂 Bachelor parties", "de": "🥂 Junggesellenabschiede", "fr": "🥂 EVG & EVJF"},
 "vuurwerk-alternatief":    {"nl": "🎆 Vuurwerk-alternatief", "en": "🎆 Fireworks alternative", "de": "🎆 Feuerwerk-Alternative", "fr": "🎆 Alternative à l'artifice"},
 "kerst-nieuwjaar-entertainment": {"nl": "🎄 Kerst & nieuwjaar", "en": "🎄 Christmas & New Year", "de": "🎄 Weihnachten & Silvester", "fr": "🎄 Noël & Nouvel An"},
}
def occ_links(lang, skip=None):
    items = "".join(
        f'<li><a href="{I.url_of(lang, s)}">{lbl[lang]}</a></li>'
        for s, lbl in _OCC_LBL.items() if s != skip)
    return (f'<section class="wrap bay occlinks"><h2 class="bay__title">{esc(_OCC_HEAD[lang])}</h2>'
            f'<ul class="citylist">{items}</ul></section>')

# ---------------------------------------------- SEO-blok in de voettekst
# Alle pagina's gegroepeerd als uitklapbare blokken: zoekmachines lezen de
# inhoud van <details> ook dichtgeklapt, bezoekers klappen open wat ze nodig
# hebben. Gelegenheden-links worden per taal gelokaliseerd via de slugtabel.
# Het linkoverzicht onder in de voettekst (gelegenheden, steden,
# kennisbank) stond in alle talen in het Nederlands. De labels volgen nu
# de taal; de stadslinks wijzen nog naar de Nederlandse stadspagina's,
# want die bestaan alleen in het Nederlands.
_VUURSPUWER = {"en": "Fire breather", "de": "Feuerspucker", "fr": "Cracheur de feu"}
_STAD_I18N = {
 "Den Haag": {"en": "The Hague", "de": "Den Haag", "fr": "La Haye"},
 "Antwerpen": {"en": "Antwerp", "de": "Antwerpen", "fr": "Anvers"},
 "Gent": {"en": "Ghent", "de": "Gent", "fr": "Gand"},
 "Brussel": {"en": "Brussels", "de": "Brüssel", "fr": "Bruxelles"},
 "Brugge": {"en": "Bruges", "de": "Brügge", "fr": "Bruges"},
 "Leuven": {"en": "Leuven", "de": "Löwen", "fr": "Louvain"},
 "Luik": {"en": "Liège", "de": "Lüttich", "fr": "Liège"},
 "Mechelen": {"en": "Mechelen", "de": "Mecheln", "fr": "Malines"},
}
_FSEO_I18N = {
 "🎃 Halloween-acts": {"en": "🎃 Halloween acts", "de": "🎃 Halloween-Acts", "fr": "🎃 Spectacles d'Halloween"},
 "🎭 Themafeesten": {"en": "🎭 Theme parties", "de": "🎭 Mottopartys", "fr": "🎭 Fêtes à thème"},
 "💶 Prijzen & pakketten": {"en": "💶 Prices & packages", "de": "💶 Preise & Pakete", "fr": "💶 Tarifs & forfaits"},
 "📖 Vuur-woordenboek: alle termen uitgelegd": {"en": "📖 Fire glossary: every term explained", "de": "📖 Feuer-Glossar: alle Begriffe erklärt", "fr": "📖 Glossaire du feu : tous les termes expliqués"},
 "💶 Wat kost een vuurspuwer?": {"en": "💶 What does a fire breather cost?", "de": "💶 Was kostet ein Feuerspucker?", "fr": "💶 Combien coûte un cracheur de feu ?"},
 "📰 Blog & tips": {"en": "📰 Blog & tips", "de": "📰 Blog & Tipps", "fr": "📰 Blog & conseils"},
 "⭐ 136 beoordelingen": {"en": "⭐ 136 reviews", "de": "⭐ 136 Bewertungen", "fr": "⭐ 136 avis"},
 "📖 Kennisbank": {"en": "📖 Knowledge base", "de": "📖 Wissen", "fr": "📖 Base de connaissances"},
}
_CHROME_I18N = {
 'aria-label="Site wordt geladen"': {"en": "Site is loading", "de": "Seite wird geladen", "fr": "Chargement du site"},
 'aria-label="Hoofdmenu"': {"en": "Main menu", "de": "Hauptmenü", "fr": "Menu principal"},
 'aria-label="Mobiel menu"': {"en": "Mobile menu", "de": "Mobiles Menü", "fr": "Menu mobile"},
 'aria-label="Contact en voorwaarden"': {"en": "Contact and terms", "de": "Kontakt und Bedingungen", "fr": "Contact et conditions"},
 'aria-label="Deel deze pagina"': {"en": "Share this page", "de": "Diese Seite teilen", "fr": "Partager cette page"},
 'aria-label="Kruimelpad"': {"en": "Breadcrumb", "de": "Brotkrumen-Navigation", "fr": "Fil d'Ariane"},
 'aria-label="5 van de 5 sterren"': {"en": "5 out of 5 stars", "de": "5 von 5 Sternen", "fr": "5 étoiles sur 5"},
 'aria-label="Alle pagina\'s per onderwerp"': {"en": "All pages by topic", "de": "Alle Seiten nach Thema", "fr": "Toutes les pages par thème"},
}
_KVK = {"en": "Chamber of Commerce 98164325 &middot; VAT NL002416954B13",
        "de": "Handelsregister (KvK) 98164325 &middot; USt-IdNr. NL002416954B13",
        "fr": "Registre du commerce (KvK) 98164325 &middot; TVA NL002416954B13"}
_DELEN = {"en": "Share&hellip;", "de": "Teilen&hellip;", "fr": "Partager&hellip;"}
# Dezelfde labels zijn ook nodig ín de gegenereerde pagina's (broodkruimels,
# de laadmelding, videotracks, sterren): die staan niet in het footer-fragment
# maar worden per pagina opgebouwd. render() past deze tabel toe.
_CHROME_LANG = {"en": {}, "de": {}, "fr": {}}
for _l in ("en", "de", "fr"):
    _F = _FOOTER_LABELS[_l]
    _C = _CHROME_LANG[_l]
    for _k, _tr in _CHROME_I18N.items():
        _C[_k] = _k.split("=")[0] + f'="{_tr[_l]}"'
    _C['srclang="nl"'] = f'srclang="{_l}"'
    _C['<span id="chatStatus">Online</span>'] = f'<span id="chatStatus">{I.UI[_l]["wa_status_on"]}</span>'
    _C["KvK 98164325 &middot; btw NL002416954B13"] = _KVK[_l]
    _C["<span>Delen&hellip;</span>"] = f"<span>{_DELEN[_l]}</span>"
    for _nl, _tr in _FSEO_I18N.items():
        _C[f'>{esc(_nl)}<'] = f'>{esc(_tr[_l])}<'
    for _s, _lbl in _OCC_LBL.items():
        _F[f'>{esc(_lbl["nl"])}<'] = f'>{esc(_lbl[_l])}<'
    for _nl, _tr in _FSEO_I18N.items():
        _F[f'>{esc(_nl)}<'] = f'>{esc(_tr[_l])}<'
    for _n in CITY_LABEL.values():
        _F[f'>Vuurspuwer {esc(_n)}<'] = f'>{_VUURSPUWER[_l]} {esc(_STAD_I18N.get(_n, {}).get(_l, _n))}<'
    for _k, _tr in _CHROME_I18N.items():
        _F[_k] = _k.split("=")[0] + f'="{_tr[_l]}"'
    _F["KvK 98164325 &middot; btw NL002416954B13"] = _KVK[_l]
    _F["<span>Delen&hellip;</span>"] = f"<span>{_DELEN[_l]}</span>"
    _F['<span id="chatStatus">Online</span>'] = f'<span id="chatStatus">{I.UI[_l]["wa_status_on"]}</span>'
    _F['srclang="nl"'] = f'srclang="{_l}"'
_FOOTER_LABELS["fr"]['aria-label="Shows"'] = 'aria-label="Spectacles"'
_FOOTER_LABELS["de"]['aria-label="Site"'] = 'aria-label="Website"'
_FOOTER_LABELS["de"]['<span>E-mail</span>'] = '<span>E-Mail</span>'
_FOOTER_LABELS["de"]['>E-mail<'] = '>E-Mail<'
_FOOTER_LABELS["en"]['class="rating__num">4,9<'] = 'class="rating__num">4.9<'
_FOOTER_LABELS["en"]['class="rkop__cijfer">4,9<'] = 'class="rkop__cijfer">4.9<'
_CHROME_LANG["en"]['class="rating__num">4,9<'] = 'class="rating__num">4.9<'
_CHROME_LANG["en"]['class="rkop__cijfer">4,9<'] = 'class="rkop__cijfer">4.9<'
_CHROME_LANG["fr"]['aria-label="Shows"'] = 'aria-label="Spectacles"'
_CHROME_LANG["de"]['aria-label="Site"'] = 'aria-label="Website"'
# honeypot-label in het formulier: onzichtbaar, maar wel de taal van de pagina
_CHROME_LANG["fr"]['<span>Website</span><input type="text" name="website"'] = '<span>Site web</span><input type="text" name="website"'

def foot_seo():
    def grp(summary, links):
        lis = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in links)
        return (f'<details class="fseo__g"><summary>{esc(summary)}</summary>'
                f'<ul>{lis}</ul></details>')
    gel = [(lbl["nl"], I.url_of("nl", s)) for s, lbl in _OCC_LBL.items()]
    gel += [("🎃 Halloween-acts", "/halloween/"),
            ("🎭 Themafeesten", "/entertainer-huren-voor-bedrijfsfeest/"),
            ("💶 Prijzen & pakketten", "/wat-kost-een-vuurspuwer/")]
    # De drie lijsten "Halloween/Fakirshow/Workshop per stad" stonden hier
    # ook. Die pagina's zijn opgeheven; de stadspagina's dekken alle drie de
    # shows, dus één stadslijst is genoeg en de voettekst wordt er korter van.
    stad = [(f"Vuurspuwer {n}", f"/{s}/") for s, n in CITY_LABEL.items()]
    kennis = [("📖 Vuur-woordenboek: alle termen uitgelegd", "/vuur-woordenboek/"),
              ("💶 Wat kost een vuurspuwer?", "/wat-kost-een-vuurspuwer/"),
              ("📰 Blog & tips", "/blog/"),
              ("⭐ 136 beoordelingen", "/beoordelingen/")]
    return ('<nav class="fseo" aria-label="Alle pagina\'s per onderwerp">'
            + grp("💍 Vuurshows per gelegenheid", gel)
            + grp("📍 Vuurspuwer per stad", stad)
            + grp("📖 Kennisbank", kennis)
            + "</nav>")

FOOTER = FOOTER.replace("<!--FOOT:SEO-->", foot_seo())

# ------------------------------------------------------------------ bouwen
gen_avif()
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
    write(slug, render(p, "city", svc, near, alternates=regio_alternates(slug)))
    built.append(slug)

# blogcategorieën: elk artikel krijgt een rubriek (zichtbaar als label,
# in het schema als articleSection en op de blogpagina als groep)
_BLOG_CATS = [
 ("halloween",  "🎃 Halloween", ("halloween", "griezel", "spook", "horror", "fright")),
 ("bruiloften", "💍 Bruiloften", ("bruiloft", "trouw", "huwelijk")),
 ("zakelijk",   "🏢 Bedrijfsfeesten & events", ("bedrijfsfeest", "personeelsfeest", "zakelijk", "bedrijfsuitje", "teambuilding", "beurs", "evenement")),
 ("workshops",  "💨 Workshops", ("workshop", "leren-vuurspuwen", "zelf-vuurspuwen", "cursus")),
 ("acts",       "⚔️ Fakir, mentalisme & reptielen", ("fakir", "spijkerbed", "glas", "zwaard", "mentalis", "reptiel", "slang", "hypno")),
 ("feesten",    "🎉 Feesten & verjaardagen", ("verjaardag", "jubileum", "vrijgezell", "themafeest", "kinderfeest", "feestje")),
 ("veiligheid", "🛡 Veiligheid & vergunningen", ("veilig", "vergunning", "brandweer", "risico", "afstand")),
 ("prijzen",    "💶 Prijzen & boeken", ("kost", "prijs", "prijzen", "budget", "goedkoop", "offerte", "checklist", "boeken", "inhuren", "huren", "tips")),
 ("steden",     "📍 Steden & regio's", ("amsterdam", "rotterdam", "den-haag", "utrecht", "eindhoven", "antwerpen", "gent", "brussel", "groningen", "maastricht", "limburg", "brabant", "belgie", "duits", "regio", "locatie")),
]
_BLOG_FALLBACK = ("vuurshows", "🔥 Vuurshows & inspiratie")
def post_cat(bp):
    s = (bp["slug"] + " " + bp["title"]).lower()
    for cid, label, keys in _BLOG_CATS:
        if any(k in s for k in keys): return cid, label
    return _BLOG_FALLBACK

# elke blogpost eindigt met een boekings-CTA: van informatie naar aanvraag
_POST_CTA = """
<div class="postcta">
  <p class="postcta__t">🔥 Zelf een vuurshow, fakirshow of workshop boeken?</p>
  <p>Nuno speelt door heel Nederland en België — 4,9/5 uit 136 beoordelingen,
  prijzen van €350 tot €1500 en binnen 24 uur antwoord op je aanvraag.</p>
  <p class="postcta__row">
    <a class="btn" href="/contact-3/"><span class="btn__dot"></span>Check je datum</a>
    <a class="postcta__alt" href="/wat-kost-een-vuurspuwer/">Bekijk alle prijzen</a>
    <a class="postcta__alt" href="https://wa.me/31620020723?text=Hallo%20Nuno%2C%20ik%20heb%20een%20vraag%20over%20een%20boeking" rel="noopener">App direct via WhatsApp</a>
  </p>
</div>"""

# mini-FAQ onder elk artikel: per rubriek de drie vragen die lezers van
# zo'n artikel het vaakst stellen, mét FAQPage-schema (posts hebben verder
# geen FAQPage, dus dit botst nergens mee)
_POST_FAQ = {
 "halloween": [
  ("Wat kost een vuurshow met Halloween?",
   "Een Halloween-vuurshow boek je vanaf €350. De meeste opdrachtgevers kiezen een show van 15–20 minuten tussen €350 en €750, afhankelijk van locatie en gewenste acts. Halloween-avond is snel volgeboekt, dus reserveer op tijd."),
  ("Kan de vuurshow in Halloween-thema?",
   "Ja. Kostuum, muziek en acts worden afgestemd op het griezelthema: fakiracts, vuurspuwen en een spannende opbouw die perfect past bij een Halloween-feest, spooktocht of themapark-event."),
  ("Kan een vuurshow ook bij een spooktocht of buitenevenement?",
   "Zeker. Nuno speelt op pleinen, in tuinen en langs routes; een vrije buitenruimte van enkele meters is genoeg. Veiligheid en afstemming met de organisatie zijn altijd inbegrepen.")],
 "bruiloften": [
  ("Wat kost een vuurshow op een bruiloft?",
   "Een vuurshow op een bruiloft boek je vanaf €350; de meeste bruidsparen kiezen een show van 15–20 minuten tussen €350 en €750, inclusief afstemming met de locatie."),
  ("Wanneer plan je de vuurshow op de trouwdag?",
   "Meestal na het diner of als opening van het avondfeest, wanneer het net donker is — dan komt het vuur het mooist uit en staan alle gasten erbij."),
  ("Is een vuurshow veilig op onze trouwlocatie?",
   "Ja. Nuno stemt vooraf met de locatie af, houdt veilige afstanden aan en is volledig verzekerd. Ook op binnenplaatsen en strandlocaties is vaak meer mogelijk dan je denkt.")],
 "zakelijk": [
  ("Wat kost entertainment voor een bedrijfsfeest?",
   "Een vuurshow of fakirshow voor een bedrijfsfeest boek je tussen €350 en €1500, afhankelijk van duur, acts en locatie. Binnen 24 uur ontvang je een offerte op maat."),
  ("Is een vuurshow geschikt voor een zakelijk publiek?",
   "Absoluut: van personeelsfeest tot productlancering. Nuno stond op SBS6, RTL4 en VTM en speelde voor merken als IKEA en parken als Walibi — professioneel, spectaculair en veilig."),
  ("Regelt Nuno de veiligheid en eventuele vergunningen?",
   "Nuno stemt vooraf af met de locatie en waar nodig met gemeente of brandweer, houdt veilige afstanden aan en is volledig verzekerd. Jij hoeft alleen de datum te prikken.")],
 "workshops": [
  ("Wat kost een workshop vuurspuwen?",
   "Een workshop vuurspuwen boek je vanaf €350, afhankelijk van groepsgrootte en locatie. Ideaal voor vrijgezellenfeesten, teamuitjes en verjaardagen."),
  ("Is vuurspuwen leren veilig voor beginners?",
   "Ja. Je leert stap voor stap onder professionele begeleiding: eerst techniek en veiligheid, daarna pas echt vuur. Nuno werkt met de juiste brandstoffen en bescherming."),
  ("Voor welke groepen is de workshop geschikt?",
   "Voor vrijgezellenfeesten, bedrijfsuitjes, teambuilding en verenigingen. De workshop wordt aangepast aan het niveau en de wensen van de groep.")],
 "acts": [
  ("Welke acts doet Nuno naast vuurspuwen?",
   "Fakiracts (spijkerbed, glas lopen), mentalisme en een reptielenshow met slangen. Alles is te combineren tot één spectaculair programma."),
  ("Wat kost een fakirshow of mentalist?",
   "Een fakirshow of mentalist-act boek je vanaf €350; een uitgebreid programma met meerdere acts loopt tot €1500. Binnen 24 uur ontvang je een offerte."),
  ("Kan een show ook binnen plaatsvinden?",
   "Fakiracts, mentalisme en de reptielenshow kunnen prima binnen. Vuurspuwen gebeurt buiten of in hoge zalen, altijd na afstemming met de locatie.")],
 "feesten": [
  ("Wat kost een vuurshow op een verjaardag of feest?",
   "Een vuurshow op een feest boek je vanaf €350; de populairste keuze is een show van 15–20 minuten tussen €350 en €750, inclusief reistijd in de offerte."),
  ("Hoe lang duurt een show op een feest?",
   "Een show duurt 10 tot 20 minuten — precies lang genoeg om iedereen ademloos te houden. Voor grotere feesten zijn meerdere sets op een avond mogelijk."),
  ("Moet ik zelf iets regelen voor de show?",
   "Alleen een vrije buitenruimte van enkele meters. Nuno neemt alles mee, stemt af met de locatie en is volledig verzekerd.")],
 "veiligheid": [
  ("Is een professionele vuurshow veilig?",
   "Ja. Nuno werkt al meer dan 20 jaar met vaste veiligheidsafstanden, professionele brandstoffen en een volledige verzekering. Veiligheid is altijd stap één van de voorbereiding."),
  ("Is er een vergunning nodig voor een vuurshow?",
   "Voor de meeste privéfeesten niet. Bij grote of openbare evenementen kan een melding bij gemeente of brandweer nodig zijn — Nuno denkt mee en levert de benodigde informatie aan."),
  ("Is Nuno verzekerd?",
   "Ja, volledig. Locaties ontvangen op verzoek vooraf de verzekerings- en veiligheidsinformatie voor hun eigen administratie.")],
 "prijzen": [
  ("Wat kost een vuurspuwer?",
   "Een vuurspuwer boek je tussen €350 en €1500: vanaf €350 voor een korte show, tussen €450 en €750 voor de populairste 20 minuten en tot €1500 voor een volledig festivalprogramma."),
  ("Wat bepaalt de prijs van een vuurshow?",
   "De duur van de show, het aantal acts (vuur, fakir, mentalisme, reptielen), de reisafstand en de datum. In de offerte staat alles transparant op een rij."),
  ("Hoe snel krijg ik een offerte?",
   "Binnen 24 uur. Stuur de datum, locatie en het soort feest mee, dan krijg je direct een passend voorstel en weet je of je datum nog vrij is.")],
 "steden": [
  ("In welke regio's treedt Nuno op?",
   "In heel Nederland en België, en ook net over de grens in Duitsland en Frankrijk. Van Amsterdam tot Antwerpen en van Groningen tot Gent."),
  ("Worden er reiskosten gerekend?",
   "Reistijd wordt transparant in de offerte opgenomen, zodat je vooraf precies weet wat de show op jouw locatie kost — zonder verrassingen achteraf."),
  ("Hoe ver van tevoren moet ik boeken?",
   "Populaire data (zaterdagen, Halloween, december) zijn vaak 4–8 weken vooruit volgeboekt. Vroeg aanvragen loont; last-minute kan soms ook — vraag het gewoon.")],
 "vuurshows": [
  ("Wat kost het boeken van een vuurshow?",
   "Een vuurshow boek je tussen €350 en €1500, afhankelijk van duur en acts. De populairste show duurt 20 minuten en is geschikt voor bruiloften, verjaardagen en bedrijfsfeesten."),
  ("Hoe lang duurt een vuurshow?",
   "Van 10 tot 20 minuten per set; op festivals speelt Nuno tot vijf sets van 20 minuten verspreid over de dag of avond."),
  ("Waar kan een vuurshow plaatsvinden?",
   "Vrijwel overal met een vrije buitenruimte: tuinen, pleinen, festivalterreinen, stranden en binnenplaatsen. Nuno stemt de show af op jouw locatie.")],
}

def _post_faq(cid):
    qa = _POST_FAQ.get(cid) or _POST_FAQ["vuurshows"]
    items = "".join(
        f'<details class="faq__item"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in qa)
    html_out = ('<section class="wrap bay" aria-label="Veelgestelde vragen">'
                '<div class="bay__head"><p class="eyebrow eyebrow--dim rise">Veelgestelde vragen</p>'
                '<h2 class="bay__title rise" data-delay="1">Eerst even <em>zeker weten</em></h2></div>'
                f'<div class="faq">{items}</div></section>')
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in qa]}
    return html_out, ld

# "Lees ook": drie artikelen uit dezelfde rubriek (aangevuld met de
# nieuwste andere artikelen), als luxe kaarten mét ItemList-schema
def _related(cur, blogset):
    cid, _ = post_cat(cur)
    same = [bp for bp in blogset if bp["slug"] != cur["slug"] and post_cat(bp)[0] == cid]
    rest = [bp for bp in blogset if bp["slug"] != cur["slug"] and post_cat(bp)[0] != cid]
    pick = (same + rest)[:3]
    if not pick:
        return "", None
    cards, items, used = [], [], set()
    for pos, bp in enumerate(pick, 1):
        # elke kaart een eigen foto: bij een botsing doorschuiven
        gi = sum(map(ord, bp["slug"])) % len(_MIDGAL_IMGS)
        while gi in used:
            gi = (gi + 1) % len(_MIDGAL_IMGS)
        used.add(gi)
        base, thumb, _full, w, h, _k = _MIDGAL_IMGS[gi]
        alt = _MIDGAL_ALT[base]["nl"]
        _, lab = post_cat(bp)
        mins = max(1, round(len(re.findall(r"\w+", text_of(bp["body"]))) / 220))
        cards.append(
            f'<article class="relcard"><a href="/{bp["slug"]}/">'
            f'<span class="relcard__media"><img src="/assets/media/{thumb}" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="{esc(alt)}"></span>'
            f'<span class="relcard__body"><span class="relcard__cat">{lab}</span>'
            f'<span class="relcard__t">{esc(bp["title"])}</span>'
            f'<span class="relcard__meta">{mins} min lezen · Lees verder →</span></span>'
            f'</a></article>')
        items.append({"@type": "ListItem", "position": pos,
                      "url": f'{SITE}/{bp["slug"]}/', "name": bp["title"]})
    html_out = ('<section class="wrap bay relposts" aria-label="Gerelateerde artikelen">'
                '<div class="bay__head"><p class="eyebrow eyebrow--dim rise">Lees ook</p>'
                '<h2 class="bay__title rise" data-delay="1">Verder <em>lezen</em></h2></div>'
                f'<div class="relposts__grid">{"".join(cards)}</div></section>')
    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "name": "Gerelateerde artikelen", "itemListElement": items}
    return html_out, ld

# het auteursblok onder elk artikel: gezicht, ervaring en bewijs (E-E-A-T),
# met rel=author naar de over-pagina waar het volledige Person-schema leeft
_AUTHOR_BOX = """
<section class="wrap bay abio" aria-label="Over de auteur">
  <div class="abio__card rise">
    <img class="abio__pic" src="/assets/media/nuno-avatar.webp" width="288" height="288"
         loading="lazy" decoding="async" alt="Portret van vuurspuwer Nuno">
    <div class="abio__txt">
      <p class="abio__eyebrow">Geschreven door</p>
      <p class="abio__name">Nuno — vuurspuwer, fakir &amp; mentalist</p>
      <p class="abio__bio">17 jaar podiumervaring, bekend van SBS6, RTL&nbsp;4 en VTM en
      optredens voor o.a. Walibi, Julianatoren en IKEA. Nuno schrijft zelf over vuur,
      veiligheid en entertainment — rechtstreeks uit de praktijk van honderden shows
      in Nederland en België.</p>
      <p class="abio__links"><a rel="author" href="/over-nuno/">Meer over Nuno →</a>
      <span class="abio__stars">★ 4,9 · 136 reviews</span></p>
    </div>
  </div>
</section>"""

_ALLE_POSTS = [p for p in pages.values() if p["kind"] == "post"]
_POST_SLUGS = {p["slug"] for p in _ALLE_POSTS}

# Een bericht met een cijfer achter de slug waarvan het origineel óók op
# de site staat, is een tweeling: dezelfde titel, twee maanden later
# opnieuw geschreven en door WordPress naast het origineel gezet. Tot nu
# toe werden beide gebouwd, met elk een canonical naar zichzelf, terwijl
# het cijferadres tegelijk een 301 kreeg — twee pagina's die om dezelfde
# zoekopdracht concurreren. Nu komt er per paar precies één op de site,
# onder het schone adres. Wélke van de twee teksten dat wordt, staat in
# _BETERE_TEKST; de keuze is per paar gemaakt op leesbaarheid,
# zoekintentie en feiten.
def _tweeling_van(slug):
    base = re.sub(r"-\d+$", "", slug)
    if base != slug and (base in _POST_SLUGS or base in KEEP_PAGES):
        return base
    return None

posts = [p for p in _ALLE_POSTS if not _tweeling_van(p["slug"])]

# Per paar is door drie onafhankelijke lezers (lezer, zoekmachine, feiten)
# gekozen welke versie op het schone adres komt; tekst, titel en
# beschrijving apart. "-2" = de herschrijving van december 2023 overnemen,
# None = het origineel houden. Bij gelijkspel wint het origineel.
_BETERE_TEKST = {
    "artiesten-boeken-tips":                                   {"body": None, "title": None, "desc": "-2"},
    "betekenis-en-geschiedenis-van-fakir":                     {"body": "-2", "title": None, "desc": None},
    "checklist-voor-het-organiseren-van-een-feest":            {"body": "-2", "title": None, "desc": None},
    "fantastische-teambuilding-activiteiten-voor-bedrijven-de-beste-tips-en-trends":
                                                               {"body": "-2", "title": None, "desc": "-2"},
    "halloweenshow-boeken-2023":                               {"body": "-2", "title": "-2", "desc": None},
    "ideeen-en-tips-voor-het-leukste-kinderfeestje":           {"body": "-2", "title": "-2", "desc": "-2"},
    "tips-om-origineel-je-verjaardag-te-vieren":               {"body": "-2", "title": "-2", "desc": "-2"},
    "tips-voor-een-onvergetelijk-personeelsfeest":             {"body": None, "title": "-2", "desc": "-2"},
    "tips-voor-het-organiseren-van-uw-bedrijfsfeest":          {"body": "-2", "title": "-2", "desc": "-2"},
    "waar-kun-je-een-entertainer-inhuren":                     {"body": None, "title": "-2", "desc": "-2"},
    "wat-vieren-we-met-halloween-en-hoe-is-het-ontstaan":      {"body": None, "title": "-2", "desc": None},
}
# per pagina: verplichte correcties in de gekozen tekst (van, naar)
_TEKSTFIX = {
    "tips-voor-het-organiseren-van-uw-bedrijfsfeest": (
        # taalfout en misleidend anker in de herschrijving
        ('<a href="https://vuurspuwer.com/een-onvergetelijk-event-bij-martins-patershof-mechelen-be-entertainment-op-hoog-niveau/">origineel entertainment</a>',
         '<a href="/vuurshow-bedrijfsfeest/">originele act zoals een vuurshow</a>'),
        # registerbreuk: de rest van de tekst is in de u-vorm
        ("Meer informatie over fotografie vind je op", "Meer informatie over fotografie vindt u op"),
        # los emoji aan het eind van de metabeschrijving
        ("onvergetelijk entertainment! \u2709\ufe0f", "onvergetelijk entertainment!"),
    ),
}
# twee koppen kwamen in kleine letters uit WordPress ("artiesten boeken tips");
# de zoektitel was al goed, de H1 op de pagina niet
_TITEL = {
    "artiesten-boeken-tips": "Artiesten boeken: tips voor je evenement",
    "ideeen-en-tips-voor-het-leukste-kinderfeestje": "Ideeën en tips voor het leukste kinderfeestje",
}

_blogset = sorted((bp for bp in posts if bp["slug"] not in PC.SHOW_PAGES),
                  key=lambda x: x["date"], reverse=True)
for p in posts:
    # workshop-vuurspuwen is in de export een bericht, maar leeft op de
    # site als volwaardige showpagina — die komt uit KEEP_PAGES.
    if p["slug"] in PC.SHOW_PAGES: continue
    if p["slug"] in _BETERE_TEKST:
        _k = _BETERE_TEKST[p["slug"]]
        _bron = pages[p["slug"] + "-2"]
        if _k["body"]:
            p = {**p, "body": _bron["body"], "img": _bron["img"] or p["img"]}
        if _k["title"]:
            p = {**p, "title": _bron["title"], "seo_title": _bron["seo_title"] or p["seo_title"]}
        if _k["desc"] and _bron["seo_desc"]:
            p = {**p, "seo_desc": _bron["seo_desc"]}
    if p["slug"] in _TITEL:
        p = {**p, "title": _TITEL[p["slug"]]}
    for _van, _naar in _TEKSTFIX.get(p["slug"], ()):
        if not any(_van in p[_veld] for _veld in ("body", "seo_title", "title", "seo_desc")):
            raise SystemExit(f"  ✖ tekstfix {p['slug']}: {_van!r} niet gevonden")
        p = {**p, "body": p["body"].replace(_van, _naar),
             "title": p["title"].replace(_van, _naar),
             "seo_title": p["seo_title"].replace(_van, _naar),
             "seo_desc": p["seo_desc"].replace(_van, _naar)}
    _cid, _clabel = post_cat(p)
    _faq_html, _faq_ld = _post_faq(_cid)
    _rel_html, _rel_ld = _related(p, _blogset)
    p = {**p, "body": p["body"] + _POST_CTA,
         "eyebrow": _clabel,
         "cat_label": _clabel.split(" ", 1)[1],
         "keywords": f'{_clabel.split(" ", 1)[1]}, vuurshow, vuurspuwer, fakirshow, entertainment boeken'}
    _extra_ld = [_faq_ld] + ([_rel_ld] if _rel_ld else [])
    write(p["slug"], render(p, "post", _extra_ld, _AUTHOR_BOX + _faq_html + _rel_html))
    built.append(p["slug"])

for slug in KEEP_PAGES:
    p = pages.get(slug)
    if not p: missing.append(slug); continue
    # taalversies (en/de/fr) verwijzen naar elkaar via hreflang
    alts = alternates_for(slug) if slug in I.SLUGS else None
    if slug == "videos":
        p = {**p, "title": "Video's van de shows",
             "seo_title": "Video's | Vuurshow & fakirshow in actie | Vuurspuwer Nuno",
             "seo_desc": "Bekijk video's van de vuurshows, fakiracts en optredens van Vuurspuwer Nuno. Showreels van festivals, bedrijfsfeesten en evenementen in Nederland en België.",
             "body": PC.videos_body(),
             "eyebrow": "Video's",
             "og_video": ("/assets/media/showreel.mp4", 540, 540),
             "img": ("/assets/media/reel-1-poster.webp",
                     "Vuurspuwer Nuno tijdens een vuurshow op locatie")}
        write(slug, render(p, "page", PC.videos_schema(), alternates=alts))
        built.append(slug); continue
    if slug in PC.SHOW_PAGES:
        sp = PC.SHOW_PAGES[slug]
        p = {**p, "title": sp["title"], "seo_title": sp["seo_title"],
             "seo_desc": sp["seo_desc"], "body": sp["body"], "img": sp["img"],
             "eyebrow": sp["eyebrow"]}
        if slug == "halloween":
            p["toon_datum"] = True
            p["body"] = hw_top("nl") + '<div class="hwpage">' + p["body"] + "</div>"
        extra = wizard("nl") + prijs_strip("nl") + PC.show_faq_html(sp)
        if sp["fotos"]:
            extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                      + PC._fotorij(sp["fotos"]) + "</div></section>")
        if slug == "halloween":
            extra += hw_cities("nl")
        extra += occ_links("nl")
        write(slug, render(p, "page", PC.show_schema(slug, sp), extra, alternates=alts))
        built.append(slug); continue
    if slug == "fotos":
        p = {**p, "title": "Foto's van de shows",
             "seo_title": "Foto's | Vuurshow, fakirshow & reptielenshow | Vuurspuwer Nuno",
             "seo_desc": "Bekijk foto's van de vuurshows, fakirshows, reptielenshow en workshops van Vuurspuwer Nuno op festivals, bedrijfsfeesten en bruiloften in Nederland en België.",
             "body": fotos_body(),
             "eyebrow": "Foto's",
             "img": ("/assets/media/festival-1600.webp",
                     "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein")}
        write(slug, render(p, "page", fotos_schema(), alternates=alts))
        built.append(slug); continue
    if slug == "beoordelingen":
        p = {**p, "title": "4,9 uit 136 beoordelingen",
             "seo_title": "⭐ Reviews Vuurspuwer Nuno — 4.9/5 uit 136 beoordelingen",
             "seo_desc": "Lees beoordelingen van opdrachtgevers uit heel NL & BE over de vuurshows en fakirshows van Nuno. Gemiddeld 4.9/5 uit 136 reviews.",
             "body": PC.reviews_body(),
             "eyebrow": "Beoordelingen",
             "img": ("/assets/media/festival-1600.webp",
                     "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek")}
        write(slug, render(p, "page", PC.reviews_schema(), alternates=alts))
        built.append(slug); continue
    if slug == "contact-3":
        p = {**p, "title": "Samenwerken met Nuno? Check je datum",
             "seo_title": "\U0001F525 Contact | Vuurspuwer Nuno boeken — binnen 24 uur antwoord",
             "seo_desc": "Vuurshow, fakirshow of workshop boeken? Bel, app of mail Nuno, of stuur het aanvraagformulier met datum en locatie. Binnen 24 uur een vrijblijvende offerte.",
             "body": PC.contact_body(),
             "intro": "",  # geen tekst in de paginakop; de uitleg staat in de pagina zelf
             "eyebrow": "Contact",
             "img": ("/assets/media/themafeest-1080.webp",
                     "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond")}
        write(slug, render(p, "page", PC.contact_schema(), PC.CONTACT_FORM, alternates=alts))
        built.append(slug); continue
    if slug == "blog":
        blog_posts = [bp for bp in sorted(posts, key=lambda x: x["date"], reverse=True)
                      if bp["slug"] not in PC.SHOW_PAGES]
        # artikelen per rubriek, met filterchips bovenaan
        groups = {}
        for bp in blog_posts:
            cid, label = post_cat(bp)
            groups.setdefault(cid, (label, []))[1].append(bp)
        cat_order = [c[0] for c in _BLOG_CATS] + [_BLOG_FALLBACK[0]]
        def _bcard(bp):
            excerpt = text_of(bp["body"], 140)
            # de echte bijwerkdatum van dit artikel, niet de bouwdatum
            _bd = _LEDGER.get(f'/{bp["slug"]}/', {}).get("d", TODAY)
            return (
                f'<article class="bcard"><a href="/{bp["slug"]}/">'
                f'<img src="/assets/media/post-cover-480.webp" '
                f'srcset="/assets/media/post-cover-480.webp 480w, /assets/media/post-cover-900.webp 900w" '
                f'sizes="(max-width:700px) 92vw, 340px" '
                f'alt="{esc(bp["title"])} — vuurspuwer Nuno" '
                f'width="480" height="720" loading="lazy" decoding="async">'
                f'<h2>{esc(bp["title"])}</h2></a>'
                f'<p>{esc(excerpt)}</p>'
                f'<p class="bcard__meta"><time datetime="{_bd}">Bijgewerkt op {nl_datum(_bd)}</time></p>'
                f'</article>')
        chips, sections = [], []
        for cid in cat_order:
            if cid not in groups: continue
            label, bps = groups[cid]
            chips.append(f'<a class="bchip" href="#cat-{cid}">{esc(label)} <b>{len(bps)}</b></a>')
            sections.append(
                f'<section class="blogcat" id="cat-{cid}">'
                f'<h2 class="blogcat__t">{esc(label)}</h2>'
                f'<div class="bloglist">{"".join(_bcard(bp) for bp in bps)}</div></section>')
        cats_html = ('<nav class="bchips" aria-label="Rubrieken">' + "".join(chips) + "</nav>"
                     + "".join(sections))
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
                      'bruiloft of Halloween-avond iets onvergetelijks. Kies een rubriek of '
                      f'blader door alle {len(blog_posts)} artikelen — bijgewerkt op {TODAY_NL}.</p>'
                      + cats_html),
             "no_toc": True,
             "eyebrow": "Blog",
             "img": ("/assets/media/post-cover.webp",
                     "Vuurspuwer Nuno met een metershoge vuurbal tegen een zwarte nachtlucht")}
        write(slug, render(p, "page", blog_ld, alternates=alts))
        built.append(slug); continue
    write(slug, render(p, "page", alternates=alts)); built.append(slug)

hp = PC.SHOW_PAGES["halloween"]
p = {"slug": "halloween", "kind": "page", "title": hp["title"],
     "date": "2026-08-30", "eyebrow": hp.get("eyebrow", "Halloween"),
     "body": hw_top("nl") + '<div class="hwpage">' + hp["body"] + "</div>",
     "seo_title": hp["seo_title"], "seo_desc": hp["seo_desc"], "img": hp["img"]}
extra = prijs_strip("nl") + PC.show_faq_html(hp)
extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
          + PC._fotorij(hp["fotos"]) + "</div></section>")
extra += hw_cities("nl") + occ_links("nl")
write("halloween", render(p, "page", PC.show_schema("halloween", hp), extra,
                          alternates=alternates_for("halloween")))
built.append("halloween")

# ------------------------------------- de stad x show-matrix: opgeheven
# Deze 45 pagina's (15 steden x 3 shows) waren voor de helft letterlijk
# hetzelfde: gemeten 50 tot 54 procent identieke zinnen op zo'n 400 woorden.
# Dat is het patroon dat Google doorway pages noemt, en het oordeel daarover
# raakt niet alleen die pagina's maar de hele site.
#
# De vijftien echte stadspagina's blijven; die zijn uniek (3 procent overlap)
# en noemen fakirshow, workshop en Halloween allemaal. Elke matrixpagina
# leidt daarom naar de stadspagina van diezelfde stad: dat is het naaste
# equivalent, het houdt de bezoeker in zijn eigen stad, en het bundelt de
# waarde in de pagina die we willen laten winnen.
_MATRIX_OM = {}
for _sk in MX.SHOWS:
    for _ck, (_n, _sf, _stadpagina) in MX.CITIES.items():
        _MATRIX_OM[MX.page_slug(_sk, _ck)] = _stadpagina
print(f"  matrix opgeheven: {len(_MATRIX_OM)} dunne pagina's naar hun stadspagina")

# ------------------------------------------------- vertaalde pagina's
# Engels, Duits en Frans: alles wat in het menu staat, plus de Duitse
# en Franstalige regiopagina's. hreflang verbindt de taalversies.
FAQ_HEAD = {
 "nl": ("Veelgestelde vragen", "Eerst even <em>zeker weten</em>"),
 "en": ("Frequently asked questions", "Good to <em>know first</em>"),
 "de": ("Häufige Fragen", "Vorab <em>gut zu wissen</em>"),
 "fr": ("Questions fréquentes", "Bon à <em>savoir</em>"),
}
FOTORIJ_HEAD = {"en": "Photos from the show", "de": "Fotos aus der Show", "fr": "Photos du spectacle"}

def lang_faq_html(lang, faq):
    if not faq: return ""
    eye, tit = FAQ_HEAD[lang]
    items = "".join(f'<details class="faq__item"><summary>{q}</summary><p>{a}</p></details>'
                    for q, a in faq)
    return ('<section class="wrap bay">'
            f'<div class="bay__head"><p class="eyebrow eyebrow--dim rise">{eye}</p>'
            f'<h2 class="bay__title rise" data-delay="1">{tit}</h2></div>'
            f'<div class="faq">{items}</div></section>')

def lang_fotorij(lang, items):
    tiles = []
    for thumb, full, w, h, cap, alt in items:
        ss = PC._srcset(thumb)
        ss_attr = f' srcset="{ss}" sizes="(max-width:760px) 46vw, 31vw"' if ss else ""
        tiles.append(f'<a href="/assets/media/{full}" data-lightbox data-cap="{esc(cap)}">'
                     f'<img src="/assets/media/{thumb}"{ss_attr} width="{w}" height="{h}" loading="lazy" '
                     f'decoding="async" alt="{esc(alt)}"></a>')
    return f'<h2>{FOTORIJ_HEAD[lang]}</h2><div class="fgrid">{"".join(tiles)}</div>'

def lang_schema(lang, path, T, kind="page"):
    """WebPage + eventuele Service/FAQ met inLanguage voor een taalpagina."""
    url = SITE + path
    out = [{"@context": "https://schema.org", "@type": "WebPage",
            "@id": url + "#page", "url": url, "name": T["title"],
            "inLanguage": I.HTML_LANG[lang],
            "about": {"@id": f"{SITE}/#business"}}]
    svc = T.get("service")
    if svc:
        out.append({"@context": "https://schema.org", "@type": "Service",
                    "@id": url + "#service", "name": svc["name"],
                    "serviceType": svc["type"], "description": svc["desc"],
                    "url": url, "inLanguage": I.HTML_LANG[lang],
                    "image": SITE + T["img"][0],
                    "provider": {"@id": f"{SITE}/#business"},
                    "areaServed": [_land(lang, "nl"), _land(lang, "be"), _land(lang, "de")],
                    **({"offers": svc["offers"]} if "offers" in svc else {})})
    if T.get("faq"):
        out.append({"@context": "https://schema.org", "@type": "FAQPage",
                    "inLanguage": I.HTML_LANG[lang],
                    "mainEntity": [{"@type": "Question", "name": q,
                                    "acceptedAnswer": {"@type": "Answer", "text": a}}
                                   for q, a in T["faq"]]})
    return out

def lang_contact_form(lang):
    F = I.FORM[lang]
    C = I.PAGES[lang]["contact-3"]["contact_labels"]
    shows = "".join(f"<option>{o}</option>" for o in F["opts_show"])
    ruimte = "".join(f"<option>{o}</option>" for o in F["opts_ruimte"])
    return f'''
<section class="wrap bay" aria-label="{C["wa"]} / {C["mail"]}">
  <div class="book">
    <div class="contact rise">
      <div class="contact__line"><span class="eyebrow eyebrow--dim">{C["tel_head"]}</span>
        <b><a href="tel:+31620020723">+31 6 200 207 23</a></b></div>
      <div class="contact__line"><span class="eyebrow eyebrow--dim">{C["biz"]}</span>
        <b><a href="tel:+31852033547">+31 85 203 35 47</a></b></div>
      <div class="contact__line"><span class="eyebrow eyebrow--dim">{C["wa"]}</span>
        <b><a href="https://wa.me/31620020723" rel="noopener">{C["wa_link"]}</a></b></div>
      <div class="contact__line"><span class="eyebrow eyebrow--dim">{C["mail"]}</span>
        <b><a href="mailto:nuno@vuurspuwer.com">nuno@vuurspuwer.com</a></b></div>
      <div class="contact__line"><span class="eyebrow eyebrow--dim">{C["area"]}</span>
        <b>{C["area_val"]}</b></div>
      <p class="form__note">{C["note"]}</p>
    </div>
    <form class="form rise" data-delay="1" id="bookForm" novalidate
          data-msg-busy="{esc(F["msg_busy"])}" data-msg-ok="{esc(F["msg_ok"])}"
          data-msg-fail="{esc(F["msg_fail"])}" data-msg-invalid="{esc(F["msg_invalid"])}"
          data-msg-ok-nc="{esc(F.get("msg_ok_nc", _OK_NC))}">
      <input type="hidden" name="lang" value="{lang}">
      <div class="form__row">
        <label class="field"><span>{F["naam"]}</span><input type="text" name="naam" autocomplete="name" required></label>
        <label class="field"><span>{F["email"]}</span><input type="email" name="email" autocomplete="email" required></label>
      </div>
      <div class="form__row">
        <label class="field"><span>{F["tel"]}</span><input type="tel" name="telefoon" autocomplete="tel"></label>
        <label class="field"><span>{F["datum"]}</span><input type="date" name="datum"></label>
      </div>
      <div class="form__row">
        <label class="field"><span>{F["show"]}</span><select name="act">{shows}</select></label>
        <label class="field"><span>{F["ruimte"]}</span><select name="ruimte">{ruimte}</select></label>
      </div>
      <label class="field"><span>{F["locatie"]}</span><input type="text" name="locatie" placeholder="{esc(F["locatie_ph"])}"></label>
      <label class="field"><span>{F["bericht"]}</span><textarea name="bericht" rows="4" placeholder="{esc(F["bericht_ph"])}"></textarea></label>
      <label class="hp" aria-hidden="true"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <div class="status" id="formStatus" hidden role="status"></div>
      <div><button class="btn" type="submit"><span class="btn__dot"></span>{F["submit"]}</button></div>
      <p class="form__note">{F["note"]}</p>
    </form>
  </div>
</section>
'''

_REV_BADGE = {"en": "NEW", "de": "NEU", "fr": "NOUVEAU"}
_REV_AGO = {"en": "August 2026", "de": "August 2026", "fr": "août 2026"}
_REV_PROOF = {"en": "📸 Original from Google", "de": "📸 Original von Google",
              "fr": "📸 Original de Google"}
_REV_PROOF_ALT = {"en": "Original Google review by", "de": "Originale Google-Bewertung von",
                  "fr": "Avis Google original de"}

def lang_reviews_body(lang):
    T = I.PAGES[lang]["beoordelingen"]["texts"]
    cards = PC.new_review_cards(badge=_REV_BADGE[lang], ago=_REV_AGO[lang],
                                lang_attr=' lang="nl"',
                                proof=_REV_PROOF[lang],
                                proof_alt=_REV_PROOF_ALT[lang]) + "".join(
        f'<article class="rcard" lang="nl"><p class="rcard__stars" aria-label="5/5">★★★★★</p>'
        f'<blockquote><p>{t}</p></blockquote>'
        f'<footer class="rcard__who">{n} <span>&middot; {c}</span></footer></article>'
        for n, c, t in PC.REVIEWS)
    return f'''
<div class="rkop">
  <span class="rkop__cijfer">4,9</span>
  <div class="rkop__rechts">
    <span class="rkop__sterren" aria-hidden="true">★★★★★</span>
    <small>{T["based_on"]}</small>
    <a href="{PC.GOOGLE_PROFILE}" rel="noopener">{T["google_link"]}</a>
  </div>
</div>
<p>{T["intro"]}</p>
<div class="rgrid">{cards}</div>
<p>{T["outro_pre"]}<a href="{PC.GOOGLE_PROFILE}" rel="noopener">{T["outro_link"]}</a>{T["outro_post"]}<a href="{I.url_of(lang, "contact-3")}">{T["outro_cta"]}</a>.</p>
'''

def lang_fotos_body(lang):
    T = I.PAGES[lang]["fotos"]
    tiles = []
    for name, thumb, full, w, h, _, _ in FOTOS:
        cap, alt = T["captions"][name]
        ss = srcset_of(f"/assets/media/{thumb}")
        ss_attr = f' srcset="{ss}" sizes="(max-width:760px) 46vw, 31vw"' if ss else ""
        tiles.append(f'<a href="/assets/media/{full}" data-lightbox data-cap="{esc(cap)}">'
                     f'<img src="/assets/media/{thumb}"{ss_attr} width="{w}" height="{h}" '
                     f'loading="lazy" decoding="async" alt="{esc(alt)}"></a>')
    return T["intro_html"] + '<div class="fgrid">' + "".join(tiles) + "</div>"

def lang_videos_body(lang):
    T = I.PAGES[lang]["videos"]
    tiles = []
    for (src, poster, _, _, _), (cap, alt) in zip(PC.VIDEOS, T["vid_caps"]):
        ratio = ' data-ratio="9/16"' if "portrait" in src else ""
        tiles.append(f'''<figure class="reel rise"{ratio}>
        <video muted loop playsinline preload="none" data-poster="/assets/media/{PC._poster(poster)}"
               data-src="/assets/media/{src}" aria-label="{esc(alt)}"><track kind="captions" src="/assets/media/stil.vtt" srclang="nl" label="—"></video>
        <button class="reel__play" type="button" aria-label="{esc(cap)}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <figcaption class="reel__hud"><span>{esc(cap)}</span><span class="reel__time"></span></figcaption>
      </figure>''')
    return T["intro_html"] + '<div class="reels reels--page">' + "".join(tiles) + "</div>"

def lang_home_body(lang):
    T = I.PAGES[lang][""]; H = T["home"]
    cards = []
    for nl_slug, imgfile, name, desc, alt in H["cards"]:
        ss = srcset_of(f"/assets/media/{imgfile}")
        ss_attr = f' srcset="{ss}" sizes="(max-width:700px) 92vw, 340px"' if ss else ""
        cards.append(
            f'<article class="bcard"><a href="{I.url_of(lang, nl_slug)}">'
            f'<img src="/assets/media/{imgfile}"{ss_attr} alt="{esc(alt)}" width="480" height="480" '
            f'loading="lazy" decoding="async"><h2>{name}</h2></a><p>{desc}</p></article>')
    why = "".join(f'<article class="rcard"><p class="rcard__stars" aria-hidden="true">\U0001F525</p>'
                  f'<blockquote><p><strong>{t}</strong><br>{d}</p></blockquote></article>'
                  for t, d in H["why"])
    quotes = "".join(
        f'<article class="rcard" lang="nl"><p class="rcard__stars" aria-label="5/5">★★★★★</p>'
        f'<blockquote><p>&ldquo;{t}&rdquo;</p></blockquote>'
        f'<footer class="rcard__who">{n} <span>&middot; {c}</span></footer></article>'
        for n, c, t in PC.REVIEWS[:3])
    return (H["intro"]
            + f'<h2>{H["shows_head"]}</h2><div class="bloglist">{"".join(cards)}</div>'
            + f'<h2>{H["why_head"]}</h2><div class="rgrid">{why}</div>'
            + f'<h2>{H["reviews_head"]}</h2><div class="rgrid">{quotes}</div>'
            + f'<p><a href="{I.url_of(lang, "beoordelingen")}">{H["reviews_link"]}</a></p>'
            + f'<h2>{H["cta_head"]}</h2><p>{H["cta_text"]}</p>')

# de prijzenpagina: cornerstone zonder WXR-bron, dus synthetisch gebouwd
PZ = PC.PRIJZEN
_pz = {"slug": "wat-kost-een-vuurspuwer", "toon_datum": True, "title": PZ["title"],
       "seo_title": PZ["seo_title"], "seo_desc": PZ["seo_desc"],
       "img": PZ["img"], "eyebrow": PZ["eyebrow"], "date": TODAY,
       "body": PZ["body"]}
write("wat-kost-een-vuurspuwer",
      render(_pz, "page", PC.show_schema("wat-kost-een-vuurspuwer", PZ),
             wizard("nl") + PC.show_faq_html(PZ),
             alternates=alternates_for("wat-kost-een-vuurspuwer")))
built.append("wat-kost-een-vuurspuwer")

# gelegenheid-pagina's (NL): bruiloft, bedrijfsfeest, verjaardag, festival,
# vrijgezellenfeest, vuurwerk-alternatief en kerst/nieuwjaar
for _slug, OC in OCC.NL.items():
    _p = {"slug": _slug, "title": OC["title"], "seo_title": OC["seo_title"],
          "seo_desc": OC["seo_desc"], "img": OC["img"], "eyebrow": OC["eyebrow"],
          "date": TODAY, "body": OC["body"]}
    _extra = wizard("nl") + prijs_strip("nl") + PC.show_faq_html(OC)
    if OC.get("fotos"):
        _extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                   + PC._fotorij(OC["fotos"]) + "</div></section>")
    _extra += occ_links("nl", skip=_slug)
    write(_slug, render(_p, "page", PC.show_schema(_slug, OC), _extra,
                        alternates=alternates_for(_slug)))
    built.append(_slug)
print(f"  {len(OCC.NL)} gelegenheid-pagina's (nl) gebouwd")

# het Vuur-woordenboek: kennisbank met DefinedTerm-schema, in vier talen
for _gl in ("nl", "en", "de", "fr"):
    GM = GL.META[_gl]
    _gslug = "vuur-woordenboek" if _gl == "nl" else f'{_gl}/{GL.SLUGS["vuur-woordenboek"][_gl]}'
    _gpath = f"/{_gslug}/"
    _gbody, _gld = GL.build(_gl)
    _gp = {"slug": _gslug, "title": GM["title"], "seo_title": GM["seo_title"],
           "seo_desc": GM["seo_desc"], "eyebrow": GM["eyebrow"], "date": TODAY,
           "keywords": GM["kw"], "body": _gbody,
           "img": ("/assets/media/vuurbal-1333.webp", _MIDGAL_ALT["vuurbal"][_gl])}
    write(_gslug, render(_gp, "page", [_gld], occ_links(_gl),
                         lang=_gl, path=_gpath,
                         alternates=alternates_for("vuur-woordenboek")))
    built.append(_gslug)
print("  vuur-woordenboek gebouwd (nl/en/de/fr)")

LANG_ALTS = {}   # pad -> alternates, voor de sitemap
for slug_nl in I.SLUGS:
    alts = alternates_for(slug_nl)
    for l, pth in alts.items():
        LANG_ALTS[pth] = alts

for lang in I.LANGS:
    for nl_slug, T in sorted(I.PAGES[lang].items()):
        # de taal-homepages worden verderop gebouwd als volwaardige klonen
        # van de echte homepage (zelfde ontwerp, volledig vertaald)
        if nl_slug == "":
            continue
        path = I.url_of(lang, nl_slug)
        alts = alternates_for(nl_slug)
        out = path.strip("/")
        p = {"slug": out, "title": T["title"], "seo_title": T["seo_title"],
             "seo_desc": T["seo_desc"], "img": T["img"], "eyebrow": T["eyebrow"],
             "date": TODAY, "body": T.get("body", ""),
             # prijzen en Halloween drijven op actualiteit: daar zegt een
             # zichtbare bijwerkdatum de lezer iets
             "toon_datum": nl_slug in ("wat-kost-een-vuurspuwer", "halloween")}
        extra_html, extra_ld = "", lang_schema(lang, path, T)
        if nl_slug == "fotos":
            p["body"] = lang_fotos_body(lang)
            p["intro"] = ""
        elif nl_slug == "videos":
            p["body"] = lang_videos_body(lang)
            p["intro"] = ""
            p["og_video"] = ("/assets/media/showreel.mp4", 540, 540)
        elif nl_slug == "contact-3":
            p["intro"] = ""
            extra_html = lang_contact_form(lang)
        elif nl_slug == "beoordelingen":
            p["body"] = lang_reviews_body(lang)
            p["intro"] = ""
            extra_ld = extra_ld + PC.reviews_schema()
        else:
            extra_html = lang_faq_html(lang, T.get("faq"))
            if nl_slug in ("vuurspuwer-inhuren", "fakir-show-inhuren",
                           "workshop-vuurspuwen", "halloween") or nl_slug in OCC.SLUGS:
                extra_html = wizard(lang) + prijs_strip(lang) + extra_html
            elif nl_slug == "wat-kost-een-vuurspuwer":
                extra_html = wizard(lang) + extra_html
            if T.get("fotos"):
                extra_html += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                               + lang_fotorij(lang, T["fotos"]) + "</div></section>")
            if nl_slug == "halloween":
                p["body"] = hw_top(lang) + '<div class="hwpage">' + p["body"] + "</div>"
                extra_html += hw_cities(lang)
            if nl_slug in ("vuurshow-inhuren", "vuurspuwer-inhuren", "fakir-show-inhuren",
                           "workshop-vuurspuwen", "halloween") or nl_slug in OCC.SLUGS:
                extra_html += occ_links(lang, skip=nl_slug if nl_slug in OCC.SLUGS else None)
        write(out, render(p, "page", extra_ld, extra_html,
                          lang=lang, path=path, alternates=alts))
        built.append(out)
    # regiopagina's in de streektaal
    for nl_city, R in I.REGIO_PAGES.get(lang, {}).items():
        loc = I.REGIO_SLUGS[lang][nl_city]
        path = f"/{lang}/{loc}/"
        alts = {"nl": f"/{nl_city}/", lang: path}
        LANG_ALTS[path] = alts
        LANG_ALTS[f"/{nl_city}/"] = alts
        iu, ia = I.REGIO_IMG[lang]
        p = {"slug": f"{lang}/{loc}", "title": R["title"], "seo_title": R["seo_title"],
             "seo_desc": R["seo_desc"], "img": (iu, ia),
             "eyebrow": I.REGIO_EYEBROW[lang], "date": TODAY, "body": R["body"]}
        svc = I.REGIO_SERVICE[lang](R["stad"])
        ld = [{"@context": "https://schema.org", "@type": "Service",
               "@id": SITE + path + "#service", "name": svc["name"],
               "serviceType": svc["type"], "description": svc["desc"],
               "url": SITE + path, "inLanguage": I.HTML_LANG[lang],
               "provider": {"@id": f"{SITE}/#business"},
               "areaServed": {"@type": "City", "name": R["stad"]}}]
        write(f"{lang}/{loc}", render(p, "page", ld, regio_links(lang, skip=path),
                                      lang=lang, path=path, alternates=alts))
        built.append(f"{lang}/{loc}")
    # steden zonder NL-tegenhanger (Düsseldorf, Duisburg, Namur, Charleroi, Mons)
    for loc, R in I.STANDALONE_REGIO.get(lang, {}).items():
        path = f"/{lang}/{loc}/"
        iu, ia = I.REGIO_IMG[lang]
        p = {"slug": f"{lang}/{loc}", "title": R["title"], "seo_title": R["seo_title"],
             "seo_desc": R["seo_desc"], "img": (iu, ia),
             "eyebrow": I.REGIO_EYEBROW[lang], "date": TODAY, "body": R["body"]}
        svc = I.REGIO_SERVICE[lang](R["stad"])
        ld = [{"@context": "https://schema.org", "@type": "Service",
               "@id": SITE + path + "#service", "name": svc["name"],
               "serviceType": svc["type"], "description": svc["desc"],
               "url": SITE + path, "inLanguage": I.HTML_LANG[lang],
               "provider": {"@id": f"{SITE}/#business"},
               "areaServed": {"@type": "City", "name": R["stad"]}}]
        write(f"{lang}/{loc}", render(p, "page", ld, regio_links(lang, skip=path),
                                      lang=lang, path=path))
        built.append(f"{lang}/{loc}")
print(f"  vertaalde pagina's: {sum(len(I.PAGES[l]) for l in I.LANGS)} + "
      f"{sum(len(I.REGIO_PAGES[l]) for l in I.REGIO_PAGES)} regiopagina's (en/de/fr)")

print(f"  {len(built)} pagina's gebouwd  ({len(CITIES)} steden, {len(posts)} blogposts)")
if missing: print("  niet gevonden:", ", ".join(missing))
json.dump(built, open("/tmp/_built.json", "w"))

# ------------------------------------------- doorverwijzingen en sitemap
# ------------------------------------------------- de vier homepages
# De EN/DE/FR-homepages zijn volledige klonen van het NL-ontwerp: zelfde
# hero, galerij, showreels, reviews en boekingsformulier — volledig
# vertaald via home_i18n. Alle vier krijgen de offerte-wizard vlak vóór
# het boekingsblok. Dit gebeurt vóór de sitemap, zodat de lastmod-datums
# van de homepages meteen kloppen.
import home_i18n as HI
_HP_SRC = open("index.html", encoding="utf-8").read()
home_alts = alternates_for("")
_HRE_NL = ('<link rel="alternate" hreflang="nl" href="https://vuurspuwer.com/">\n'
           '<link rel="alternate" hreflang="x-default" href="https://vuurspuwer.com/">')
_HRE_ALL = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{home_alts[l]}">\n'
                   for l in ("nl", "en", "de", "fr")) + \
           '<link rel="alternate" hreflang="x-default" href="https://vuurspuwer.com/">'
_HP_TITLE = "<title>🔥 Vuurspuwer inhuren? Vuurshow &amp; Fakirshow | Nuno</title>"
_HP_DESC = '<meta name="description" content="🔥 Dé vuurspuwer van NL &amp; BE, bekend van SBS6, RTL 4 en VTM ★ 4,9/5 (136 reviews) ✓ Vuurshow, fakirshow, mentalisme &amp; workshops ✓ €350–€1500 ✓ Binnen 24 uur offerte.">'
_HP_KW = '<meta name="keywords" content="vuurspuwer inhuren, vuurspuwer boeken, vuurshow boeken, fakirshow, mentalist boeken, workshop vuurspuwen, entertainment bedrijfsfeest, artiest bruiloft, Nederland, België">'
_HP_OGT = '<meta property="og:title" content="🔥 Vuurspuwer inhuren? Vuurshow &amp; Fakirshow | Nuno">'
_HP_OGD = '<meta property="og:description" content="Dé vuurspuwer van NL &amp; BE, bekend van SBS6, RTL 4 en VTM ★ 4,9/5 (136 reviews). Vuurshow, fakirshow, mentalisme &amp; workshops — binnen 24 uur offerte.">'
_hp_missing = {}
for _hl in ("nl", "en", "de", "fr"):
    d = _HP_SRC
    if _hl != "nl":
        d = d.replace("<!--FOOT:SEO-->", foot_seo())
        # het verborgen taalveld van het formulier: anders krijgt een Engelse
        # aanvrager vanaf de Engelse homepage een Nederlandse bevestiging
        d = d.replace('name="lang" value="nl"', f'name="lang" value="{_hl}"')
        d = localize_doc(d, _hl)
        d, _miss = HI.apply(d, _hl)
        _hp_missing[_hl] = _miss
        H = HI.HEAD[_hl]
        d = d.replace('<html lang="nl">', f'<html lang="{I.HTML_LANG[_hl]}">', 1)
        d = d.replace(_HP_TITLE, f'<title>{H["title"]}</title>', 1)
        d = d.replace(_HP_DESC, f'<meta name="description" content="{H["desc"]}">', 1)
        d = d.replace(_HP_KW, f'<meta name="keywords" content="{H["kw"]}">', 1)
        d = d.replace(_HP_OGT, f'<meta property="og:title" content="{H["title"]}">', 1)
        d = d.replace(_HP_OGD, f'<meta property="og:description" content="{H["desc"]}">', 1)
        d = d.replace('<link rel="canonical" href="https://vuurspuwer.com/">',
                      f'<link rel="canonical" href="{SITE}/{_hl}/">', 1)
        d = d.replace('<meta property="og:url" content="https://vuurspuwer.com/">',
                      f'<meta property="og:url" content="{SITE}/{_hl}/">', 1)
        d = d.replace('content="nl_NL"', f'content="{OG_LOCALE[_hl]}"')
        d = d.replace('"inLanguage": "nl-NL"', f'"inLanguage": "{I.HTML_LANG[_hl]}"')
    # de offerte-wizard vlak vóór het boekingsblok, en voor de Duitse en
    # Franse versie ook de regiosteden — anders is dat de enige groep
    # pagina's die vanaf de homepage onbereikbaar blijft
    d = d.replace('<section class="bay wrap" id="boeken"',
                  regio_links(_hl) + wizard(_hl) + '\n\n  <section class="bay wrap" id="boeken"', 1)
    for _a in ("assets/site.css", "assets/site.js", "assets/ga.js"):
        d = d.replace(f'"/{_a}"', f'"/{_a}?v={VER}"')
    d = d.replace(_HRE_NL, _HRE_ALL, 1)
    d = d.replace('<div class="foot__bar">', lang_row(_hl, home_alts) + '\n  <div class="foot__bar">')
    d = d.replace("</head>", spec_rules(_hl) + "\n</head>", 1)
    d = d.replace("<!--FOOT:SEO-->", foot_seo())
    d = _avifize(d)
    _hp_path = "/" if _hl == "nl" else f"/{_hl}/"
    _lastmod(_hp_path, d)
    _hp_dir = OUT if _hl == "nl" else os.path.join(OUT, _hl)
    os.makedirs(_hp_dir, exist_ok=True)
    open(os.path.join(_hp_dir, "index.html"), "w", encoding="utf-8").write(d)
    if _hl != "nl":
        built.append(_hl)
print("  4 homepages gebouwd (nl/en/de/fr, zelfde ontwerp)")
for _hl, _miss in _hp_missing.items():
    if _miss:
        print(f"  ⚠ home_i18n {_hl}: {len(_miss)} fragmenten niet gevonden")
        for _m in _miss:
            print(f"      · {_m[:110]!r}")

# ------------------------------------------------- de vier zoekpagina's
# Volwaardige pagina's met het site-ontwerp; noindex (zoekresultaten horen
# niet in de index) maar wel bruikbaar en gekoppeld via de SearchAction.
def _zoek_pagina(lang):
    Z = _ZOEK[lang]
    url = Z["url"]
    out = url.strip("/")
    ui = (f'<section class="wrap bay zoekpg">'
          f'<form class="zoek__form" id="zoekForm" role="search" action="{url}" method="get">'
          f'<label class="vh" for="zoekIn">{esc(Z["aria"])}</label>'
          f'<input class="zoek__in" id="zoekIn" type="search" name="q" '
          f'placeholder="{esc(Z["ph"])}" autocomplete="off" enterkeyhint="search" '
          f'maxlength="80" autofocus>'
          f'<button type="submit">{esc(Z["btn"])}</button></form>'
          f'<p class="zoek__status" id="zoekStatus" role="status" aria-live="polite"></p>'
          f'<ul class="zoek__resultaten" id="zoekResultaten"></ul>'
          f'<span id="zoekData" hidden data-index="/zoekindex.json" '
          f'data-lang="{lang}" data-url="{url}" '
          f'data-msg-typ="{esc(Z["typ"])}" data-msg-none="{esc(Z["none"])}" '
          f'data-msg-count="{esc(Z["count"])}" data-msg-one="{esc(Z["one"])}" '
          f'data-msg-loading="{esc(Z["loading"])}"></span>'
          f'</section>'
          f'<script src="/assets/zoek.js?v={VER}" defer></script>')
    p = {"slug": out, "title": Z["h1"], "seo_title": Z["seo_title"],
         "seo_desc": Z["seo_desc"], "eyebrow": Z["eyebrow"], "date": TODAY,
         "body": f'<p>{Z["intro"]}</p>', "intro": "", "no_toc": True,
         "noindex": True,
         "img": ("/assets/media/schemering-640.webp",
                 "Vuurspuwer Nuno bij schemering")}
    write(out, render(p, "page", "", ui, lang=lang, path=url, alternates=None))

for _zl in ("nl", "en", "de", "fr"):
    _zoek_pagina(_zl)
print("  zoekpagina's gebouwd (nl/en/de/fr, noindex)")

# de zoekindex: elke geindexeerde pagina met titel, beschrijving en adres,
# gegroepeerd per taal, gelezen door /assets/zoek.js
import html as _html
_ZIDX = {"nl": [], "en": [], "de": [], "fr": []}
_ZTITEL = re.compile(r"<title>(.*?)</title>", re.S)
_ZDESC  = re.compile(r'<meta name="description" content="(.*?)"')
_ZLANG  = re.compile(r'<html lang="([a-z]{2})"')
for _root, _, _fs in os.walk(OUT):
    if "index.html" not in _fs: continue
    _doc = open(os.path.join(_root, "index.html"), encoding="utf-8").read()
    if "noindex" in _doc[:_doc.find("</head>")]: continue
    _lm = _ZLANG.search(_doc); _tl = (_lm.group(1) if _lm else "nl")
    if _tl not in _ZIDX: continue
    _rel = os.path.relpath(_root, OUT).replace(os.sep, "/")
    _u = "/" if _rel == "." else f"/{_rel}/"
    _tm = _ZTITEL.search(_doc); _dm = _ZDESC.search(_doc)
    if not _tm: continue
    _t = _html.unescape(_tm.group(1)).strip()
    for _suf in (" | Vuurspuwer Nuno", " | Nuno", " \u2014 Vuurspuwer Nuno"):
        if _t.endswith(_suf): _t = _t[: -len(_suf)]
    _d = _html.unescape(_dm.group(1)).strip() if _dm else ""
    _ZIDX[_tl].append({"u": _u, "t": _t, "d": _d})
for _tl in _ZIDX:
    _ZIDX[_tl].sort(key=lambda e: e["u"])
json.dump(_ZIDX, open(os.path.join(OUT, "zoekindex.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print(f"  zoekindex.json: {sum(len(v) for v in _ZIDX.values())} pagina's "
      f"(nl {len(_ZIDX['nl'])}, en {len(_ZIDX['en'])}, de {len(_ZIDX['de'])}, fr {len(_ZIDX['fr'])})")

kept = set(built)
lines = ["# oude adressen die blijven werken", "",
         # het kanonieke contactadres is /contact-3/ (zo heet het op de
         # live site); alle andere contact-varianten wijzen daarheen
         "/contact/  /contact-3/  301"]

# 1. dubbelingen naar het origineel zonder cijfer
# adressen die een 301 krijgen horen niet in de sitemap: Google zou ze
# aanbieden en dan als 'pagina met omleiding' terugmelden
_OMGELEID = set()
for slug in pages:
    base = re.sub(r"-\d+$", "", slug)
    if base != slug and base in kept:
        lines.append(f"/{slug}/  /{base}/  301")
        _OMGELEID.add(slug)
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

# 2b. de opgeheven matrixpagina's naar de stadspagina van dezelfde stad
for _van, _naar in _MATRIX_OM.items():
    lines.append(f"/{_van}/  /{_naar}/  301")
    _OMGELEID.add(_van)

# 3. alles wat verder wegvalt naar de homepage, zodat niets een 404 wordt
rest = 0
for slug in pages:
    if slug in kept: continue
    if any(l.startswith(f"/{slug}/ ") or l.startswith(f"/{slug}/\t") for l in lines): continue
    if f"/{slug}/  {HUB}  301" in lines: continue
    lines.append(f"/{slug}/  /  301")
    rest += 1

# 4. de hernoemde adressen: het oude cijferadres naar het schone
for _oud, _nieuw in _HERNOEMD.items():
    lines.append(f"/{_oud}/  /{_nieuw}/  301")
    _OMGELEID.add(_oud)

# 5. adressen waar blogteksten nog naar linken maar die al vóór de export
# verwijderd waren — 54 links naar 36 adressen die een 404 gaven. Vrijwel
# allemaal oude locatie-artikelen ("Magisch entertainment bij Kasteel X"):
# die gaan naar de locatiepagina, net als de opgeheven stadspagina's. De
# rest naar de pagina die het onderwerp nu draagt. De links in de teksten
# zelf worden verderop rechtstreeks gemaakt, dus de bezoeker merkt niets
# van de omleiding; die blijft voor wie van buiten komt. Nieuwe kapotte
# links laten de bouw omvallen (zie de controle bij de eindpas).
_VERDWENEN = {
    "/vuurspuwer-boeken-voor-evenement/":
        "/hoe-vuurspuwer-nuno-boeken-voor-evenementen-het-complete-antwoord-door-vuurspuwer-nuno/",
    "/vuurspuwer-boeken-voor-een-bedrijfsfeest/":
        "/vuurspuwer-boeken-voor-een-bedrijfsfeest-de-ultieme-spectaculaire-ervaring/",
    "/Vuurspuwer-boeken-voor-een-verjaardag-de-ultieme-spectaculaire-ervaring/":
        "/vuurspuwer-boeken-voor-een-verjaardag-de-ultieme-spectaculaire-ervaring/",
    "/wat-is-de-ideale-kijkafstand-voor-het-publiek-het-complete-antwoord-door-vuurspuwer-nuno/":
        "/vuurspuwer-inhuren/",
    "/zijn-fakirs-echte-magiers-of-illusionisten-het-complete-antwoord-door-vuurspuwer-nuno/":
        "/betekenis-en-geschiedenis-van-fakir/",
    "/bedrijfsfeest-organiseren-tips/": "/tips-voor-het-organiseren-van-uw-bedrijfsfeest/",
    "/vuurspuwer-inhuren-in-amersfoort/": HUB,
    "/entertainment/vuurspuwer-vuurshow/": "/vuurspuwer-inhuren/",
    "/offerte-aanvragen/": "/contact-3/",
}
_VENUE = re.compile(r"entertainment-bij-|event-bij-|feest-bij-|avond-bij-|avond-in-het-|"
                    r"evenement-bij-|spektakel-bij-|knokke-heist|kasteel|zalmhuis|vismijn|"
                    r"belfort|gravensteen|zuiderpershuis|nekkerhal|technopolis|patershof|"
                    r"faculty-club|3hoog|abdij-van-park|casino-van-sint-niklaas|salons-|"
                    r"crowne-plaza|hotel-metropole|kruisherenhotel|auberge-du-pecheur|river-woods")
_bestaat = lambda u: u == "/" or os.path.exists(os.path.join(OUT, u.strip("/"), "index.html"))
_HREF_ALL = re.compile(r'<a [^>]*href="(?:https?://vuurspuwer\.com)?(/[^"#?]*)(?:[#?][^"]*)?"')
_bekend = {l.split()[0] for l in lines if l.startswith("/")}
_dood = set()
for _root, _, _fs in os.walk(OUT):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        for _u in _HREF_ALL.findall(open(os.path.join(_root, _f), encoding="utf-8").read()):
            if _u.startswith(("/assets/", "/api/")) or "." in _u.rsplit("/", 1)[-1]: continue
            _uu = _u.rstrip("/") + "/"
            if not _bestaat(_uu) and _uu not in _bekend: _dood.add(_uu)
_onbekend = []
for _u in sorted(_dood):
    _doel = _VERDWENEN.get(_u) or (HUB if _VENUE.search(_u) else None)
    if not _doel: _onbekend.append(_u); continue
    lines.append(f"{_u}  {_doel}  301")
if _onbekend:
    raise SystemExit("  ✖ interne links naar adressen zonder pagina én zonder omleiding:\n    " + "\n    ".join(_onbekend))
print(f"  verdwenen adressen omgeleid: {len(_dood)} (waar blogteksten nog naar linkten)")

# Eén regel per bron (de eerste wint, zoals Cloudflare het ook leest) en
# geen kettingen: elke omleiding wijst meteen naar het eindadres. Een
# ketting kost de bezoeker een extra rondreis en Google telt hem als
# ruis; na een hernoeming ontstaan ze vanzelf, dus ze worden hier
# opgelost in plaats van gehoopt dat ze er niet zijn.
_RD, _uniek, _dubbel = {}, [], 0
for l in lines:
    p = l.split()
    if len(p) >= 2 and p[0].startswith("/"):
        if p[0] in _RD: _dubbel += 1; continue
        _RD[p[0]] = p[1]
    _uniek.append(l)
lines = _uniek
def _eind(doel):
    gezien = set()
    while doel in _RD:
        if doel in gezien: raise SystemExit(f"  ✖ omleidingslus bij {doel}")
        gezien.add(doel); doel = _RD[doel]
    return doel
_kettingen = 0
for i, l in enumerate(lines):
    p = l.split()
    if len(p) >= 2 and p[0].startswith("/") and p[1] in _RD:
        e = _eind(p[1])
        if e == p[0]: raise SystemExit(f"  ✖ omleiding naar zichzelf: {p[0]}")
        lines[i] = f"{p[0]}  {e}  {p[2] if len(p) > 2 else '301'}"
        _RD[p[0]] = e; _kettingen += 1
for _bron in _RD:
    if os.path.exists(os.path.join(OUT, _bron.strip("/"), "index.html")):
        raise SystemExit(f"  ✖ {_bron} is omgeleid én gebouwd — dat is een duplicaat")

open(os.path.join(OUT, "_redirects"), "w").write("\n".join(lines) + "\n")
print(f"  _redirects: {len(lines)-2} regels ({dropped} stadspagina's naar de hub, "
      f"{len(_MATRIX_OM)} matrixpagina's naar hun stad, {rest} overig; "
      f"{_dubbel} dubbele bronnen verwijderd, {_kettingen} kettingen opgelost)")

# sitemap — met xhtml-alternates voor alle taalversies
_TOP_PAGES = {"halloween", "wat-kost-een-vuurspuwer",
              "en/halloween", "de/halloween", "fr/halloween",
              "en/fire-breather-prices", "de/feuerspucker-kosten",
              "fr/prix-cracheur-de-feu",
              "vuur-woordenboek", "en/fire-glossary",
              "de/feuer-glossar", "fr/glossaire-du-feu"}
_TOP_PAGES |= set(OCC.SLUGS)
_TOP_PAGES |= {f"{l}/{OCC.SLUGS[s][l]}" for s in OCC.SLUGS for l in ("en", "de", "fr")}
def _prio(s):
    if s in _TOP_PAGES: return "0.9"
    if s in CITIES: return "0.8"
    if s.split("/")[0] in I.LANGS: return "0.7"
    return "0.6"
urls = [("/", "1.0")] + [(f"/{s}/", _prio(s)) for s in sorted(kept - _OMGELEID)]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
      'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" '
      'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">']

# de homepage draagt de volledige galerij en de showreels mee, zodat
# Google Afbeeldingen en Google Video's alles rechtstreeks vinden
SITEMAP_IMG["/"] = [SITE + u for u in (
    "/assets/media/vuurbal-1333.webp", "/assets/media/festival-1600.webp",
    "/assets/media/vuurshow-850.webp", "/assets/media/themafeest-1080.webp",
    "/assets/media/fakir-1080.webp", "/assets/media/mentalist-1371.webp",
    "/assets/media/schemering-640.webp", "/assets/media/avondvuur-1080.webp",
    "/assets/media/spijkerbed-1242.webp", "/assets/media/bruiloft-1080.webp",
    "/assets/media/reptiel-960.webp", "/assets/media/vuurzee-1234.webp",
    "/assets/media/straatfakir-1081.webp", "/assets/media/glasact-1600.webp",
    "/assets/media/podium-1024.webp", "/assets/media/vuurhart-998.webp",
    "/assets/media/cirque-1080.webp", "/assets/media/spijkersandwich-1125.webp",
    "/assets/media/themafakir-1056.webp", "/assets/media/familiefest-640.webp",
    "/assets/media/galavuur-1080.webp", "/assets/media/zonsondergang-1152.webp",
    "/assets/media/nachtvuur-960.webp", "/assets/media/terrasvuur-582.webp",
    "/assets/media/portret-1080.webp")]
_VIDEOS = [
    ("Showreel Vuurspuwer Nuno - vuurshow op locatie",
     "Beelden van een vuurshow van Vuurspuwer Nuno: vuurspuwen, vuurjongleren en body fire.",
     "/assets/media/reel-1-poster.webp", "/assets/media/reel-1.mp4", 19),
    ("Showreel Vuurspuwer Nuno - acts en fakirwerk",
     "Compilatie van vuur- en fakiracts van Vuurspuwer Nuno op festivals en bedrijfsfeesten.",
     "/assets/media/reel-2-poster.webp", "/assets/media/reel-2.mp4", 58),
    ("Showreel Vuurspuwer Nuno",
     "Korte showreel van vuurspuwer en fakir Nuno.",
     "/assets/media/reel-poster.webp", "/assets/media/showreel.mp4", 13),
    ("Vuurbal in close-up - Vuurspuwer Nuno",
     "Meters hoge vuurbal van vuurspuwer Nuno, gefilmd van dichtbij.",
     "/assets/media/vuurbal-900.webp", "/assets/media/hero-portrait.mp4", 5),
]
# de fotopagina's melden de complete galerij aan Google Afbeeldingen
_GALLERY = [f"{SITE}/assets/media/{full}" for _k, _t, full, _w, _h, _c, _a in FOTOS]
for _p in ("/fotos/", "/en/photos/", "/de/fotos/", "/fr/photos/"):
    SITEMAP_IMG[_p] = list(dict.fromkeys(SITEMAP_IMG.get(_p, []) + _GALLERY))

for pth, pr in urls:
    _mod = _LEDGER.get(pth, {}).get("d", TODAY)
    entry = f"  <url><loc>{SITE}{pth}</loc><lastmod>{_mod}</lastmod><priority>{pr}</priority>"
    for l, alt in sorted((LANG_ALTS.get(pth) or {}).items()):
        entry += f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{alt}"/>'
    for iu in SITEMAP_IMG.get(pth, []):
        entry += f"<image:image><image:loc>{iu}</image:loc></image:image>"
    if pth == "/":
        for vt, vd, vp, vc, vs in _VIDEOS:
            entry += ("<video:video>"
                      f"<video:thumbnail_loc>{SITE}{vp}</video:thumbnail_loc>"
                      f"<video:title>{esc(vt)}</video:title>"
                      f"<video:description>{esc(vd)}</video:description>"
                      f"<video:content_loc>{SITE}{vc}</video:content_loc>"
                      f"<video:duration>{vs}</video:duration>"
                      "</video:video>")
    sm.append(entry + "</url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"""# vuurspuwer.com — alles mag gecrawld worden, ook door AI-assistenten.
# Overzicht voor taalmodellen: {SITE}/llms.txt
# Volledige inhoud in platte tekst: {SITE}/llms-full.txt

User-agent: *
Allow: /

# AI-crawlers expliciet welkom (zoek-, antwoord- en assistentverkeer)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Gemini-Deep-Research
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: CCBot
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
print(f"  sitemap.xml: {len(urls)} adressen")

# IndexNow: het sleutelbestand moet op de site zelf staan
_inkey = open("indexnow-key.txt").read().strip()
open(os.path.join(OUT, f"{_inkey}.txt"), "w").write(_inkey)

# llms.txt: index voor AI-assistenten volgens llmstxt.org — een H1, een
# samenvatting en secties met echte markdown-links [titel](url): omschrijving
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(f"""# Vuurspuwer Nuno

> Professionele vuurspuwer, fakir, mentalist en reptielenshow-artiest met 17 jaar ervaring. Optredens in heel Nederland en België (en de Duitse grensregio), vanuit Zeist (NL). Beoordeeld met 4,9/5 uit 136 reviews. Prijzen van €350 tot €1500 per show. Bekend van SBS6, RTL 4, VTM, Uri Geller, Walibi Fright Nights, Julianatoren en Emporium. Volledig gecertificeerd.

Boekingen lopen via het aanvraagformulier of WhatsApp; reactie binnen 24 uur. De volledige site-inhoud in platte tekst staat in [llms-full.txt]({SITE}/llms-full.txt).

## Shows en diensten
- [Vuurshow]({SITE}/vuurspuwer-inhuren/): choreografie van vuurspuwen, vuurjongleren en body fire, 5–30 min, ook als duo met danseres
- [Fakirshow]({SITE}/fakir-show-inhuren/): spijkerbed, glaslopen en zwaarden, met het publiek als deel van de act
- [Workshop vuurspuwen]({SITE}/workshop-vuurspuwen/): zelf leren vuurspuwen — teambuilding, vrijgezellen- en bedrijfsfeesten
- [Halloween-acts]({SITE}/halloween/): duivelse vuurshows en horror-fakir, bekend van de Walibi Fright Nights
- [Reptielenshow]({SITE}/reptielenhow/): educatieve ontmoeting met exotische slangen
- [Mentalisme]({SITE}/entertainer-huren/): gedachtelezen en psychologische illusies, ook binnen inzetbaar
- [Themafeesten]({SITE}/entertainer-huren-voor-bedrijfsfeest/): complete themaproducties van 1001 Nacht tot Caribbean

## Gelegenheden
- [Bruiloften]({SITE}/vuurshow-bruiloft/): romantische vuurshow bij de eerste dans of avondopening, vaak toegestaan waar vuurwerk verboden is
- [Bedrijfsfeesten]({SITE}/vuurshow-bedrijfsfeest/): opening of grande finale voor personeelsfeesten en klantevents, op factuur
- [Verjaardagen en jubilea]({SITE}/vuurshow-verjaardag/): verrassingsact aan huis, in de tuin of op de oprit
- [Festivals]({SITE}/vuurshow-festival/): tot vijf sets van 20 minuten per dag, met technische rider
- [Vrijgezellenfeesten]({SITE}/vrijgezellenfeest/): workshop vuurspuwen met de hele groep
- [Vuurwerk-alternatief]({SITE}/vuurwerk-alternatief/): spektakel dat wél mag waar vuurwerk verboden is
- [Kerst en nieuwjaar]({SITE}/kerst-nieuwjaar-entertainment/): winterspektakel voor kerstborrels en oud & nieuw

## Prijzen en boeken
- [Prijzen en pakketten]({SITE}/wat-kost-een-vuurspuwer/): power-act 10 min vanaf €350, showblok 20 min vanaf €450, volledige show 30 min vanaf €595, festivalpakket tot 5×20 min €950–€1500
- [Contact en offerte]({SITE}/contact-3/): aanvraagformulier, antwoord binnen 24 uur
- [Beoordelingen]({SITE}/beoordelingen/): 4,9/5 uit 136 reviews van opdrachtgevers
- [Over Nuno]({SITE}/over-nuno/): 17 jaar ervaring, tv-optredens bij SBS6, RTL en VTM
- Telefoon/WhatsApp: +31 6 200 207 23 · E-mail: nuno@vuurspuwer.com · KvK 98164325

## Media
- [Foto's]({SITE}/fotos/): galerij met licenseerbare showfoto's
- [Video's]({SITE}/videos/): showreels van vuur- en fakiracts
- [Locaties]({SITE}/locaties-vuurshows-nederland-belgie/): alle steden in Nederland en België
- [Vuur-woordenboek]({SITE}/vuur-woordenboek/): 19 termen uit de vuur- en fakirwereld uitgelegd, van poi en body fire tot pyrotechniek — ook in het [Engels]({SITE}/en/fire-glossary/), [Duits]({SITE}/de/feuer-glossar/) en [Frans]({SITE}/fr/glossaire-du-feu/)

## Talen
- [Nederlands]({SITE}/): hoofdversie
- [English]({SITE}/en/): fire breather for hire in the Netherlands & Belgium
- [Deutsch]({SITE}/de/): Feuerspucker für NRW und die Grenzregion
- [Français]({SITE}/fr/): cracheur de feu pour la Belgique francophone

## Optional
- [Volledige inhoud (llms-full.txt)]({SITE}/llms-full.txt): alle pagina's, veelgestelde vragen en reviews in platte tekst
- [Sitemap]({SITE}/sitemap.xml): alle 229 pagina's met afbeeldingen en video's
- [Blog]({SITE}/blog/): artikelen over vuurshows, veiligheid en evenementen
""")

# llms-full.txt: de complete inhoud in platte tekst, zodat ChatGPT, Claude,
# Gemini en Perplexity de site in één bestand kunnen inlezen
import glob as _glob
import html as _htmllib
def _plain(fragment):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = _htmllib.unescape(t)
    return re.sub(r"\s+", " ", t).strip()

def _dist_main(pth):
    h = open(os.path.join(OUT, pth.strip("/"), "index.html"), encoding="utf-8").read()
    title = _plain(re.search(r"<title>(.*?)</title>", h, re.S).group(1))
    m = re.search(r"<main.*?</main>", h, re.S)
    return title, _plain(m.group(0) if m else "")

_FULL = ["vuurspuwer-inhuren", "fakir-show-inhuren", "workshop-vuurspuwen",
         "reptielenhow", "entertainer-huren", "entertainer-huren-voor-bedrijfsfeest",
         "halloween", "wat-kost-een-vuurspuwer", "over-nuno",
         "locaties-vuurshows-nederland-belgie", "contact-3"]
parts = ["# Vuurspuwer Nuno — volledige inhoud (vuurspuwer.com)\n",
         "> Automatisch gegenereerd uit de live site. Index: "
         f"{SITE}/llms.txt · Sitemap: {SITE}/sitemap.xml\n"]
for slug in _FULL:
    t, b = _dist_main(f"/{slug}/")
    parts.append(f"## {t}\nURL: {SITE}/{slug}/\n\n{b}\n")

# alle veelgestelde vragen van de hele site (alle talen), ontdubbeld
faq_seen, faq_md = set(), []
for f in ["index.html"] + sorted(_glob.glob(os.path.join(OUT, "**", "index.html"), recursive=True)):
    for mm in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                         open(f, encoding="utf-8").read(), re.S):
        try: d = json.loads(mm)
        except ValueError: continue
        nodes = d.get("@graph", [d]) if isinstance(d, dict) else (d if isinstance(d, list) else [d])
        for g in nodes:
            if not isinstance(g, dict): continue
            t = g.get("@type")
            if "FAQPage" not in (t if isinstance(t, list) else [t]): continue
            for q in g.get("mainEntity", []):
                qq = q.get("name"); aa = (q.get("acceptedAnswer") or {}).get("text")
                if qq and aa and qq not in faq_seen:
                    faq_seen.add(qq)
                    faq_md.append(f"**V: {qq}**\nA: {_plain(aa)}\n")
parts.append("## Veelgestelde vragen (alle pagina's en talen)\n\n" + "\n".join(faq_md))

parts.append("## Reviews van opdrachtgevers (4,9/5 uit 136 beoordelingen)\n\n" +
             "\n".join(f"- {n}: “{_plain(t)}”" for n, _, t in PC.REVIEWS))

parts.append("## Blogartikelen\n\n" +
             "\n".join(f"- [{p['title']}]({SITE}/{p['slug']}/)" for p in posts))

_city_paths = sorted(u for u, _ in urls if u.count("/") == 2 and
                     any(k in u for k in ("vuurspuwer-", "fakirshow-", "workshop-vuurspuwen-",
                                          "halloween-")))
parts.append("## Stedenpagina's (Nederland en België)\n\n" +
             "\n".join(f"- {SITE}{u}" for u in _city_paths))
open(os.path.join(OUT, "llms-full.txt"), "w", encoding="utf-8").write(
    "\n".join(parts) + "\n")

# spelregels.md -> spelregels.js, zodat de mailfunctie ze kan meebundelen.
# Ze staan bewust NIET in dist: dit zijn interne afspraken (ondergrens, wat
# Nuno niet doet, betaalvoorwaarden) en die horen niet op het web.
_sr_md = os.path.join("assistent", "spelregels.md")
if os.path.exists(_sr_md):
    _sr = open(_sr_md, encoding="utf-8").read()
    open(os.path.join("assistent", "spelregels.js"), "w", encoding="utf-8").write(
        "/* Automatisch gemaakt uit spelregels.md door build.py.\n"
        "   Bewerk spelregels.md, niet dit bestand. */\n"
        "export default " + json.dumps(_sr, ensure_ascii=False) + ";\n")

# assistent.txt: de beknopte versie waarmee de boekingsassistent werkt.
# llms-full.txt is 150 KB — dat elke aanvraag meesturen kost onnodig veel.
# Hier staat alleen wat je nodig hebt om een boekingsvraag te beantwoorden:
# de prijzenpagina voluit, elke show in het kort, en alle veelgestelde
# vragen. Het wordt bij elke build opnieuw gemaakt, dus het kan nooit uit de
# pas lopen met wat er op de site staat.
_ass = ["# Wat er op vuurspuwer.com staat \u2014 naslag voor het conceptantwoord\n",
        "> Automatisch gemaakt uit de live site. Noem nooit een prijs of\n"
        "> voorwaarde die hier niet in staat.\n"]
_pt, _pb = _dist_main("/wat-kost-een-vuurspuwer/")
_ass.append(f"## Prijzen en pakketten (volledig)\n\n{_pb}\n")
for slug in ("vuurspuwer-inhuren", "fakir-show-inhuren", "workshop-vuurspuwen",
             "reptielenhow", "entertainer-huren", "halloween",
             "entertainer-huren-voor-bedrijfsfeest"):
    _t, _b = _dist_main(f"/{slug}/")
    _ass.append(f"## {_t}\nURL: {SITE}/{slug}/\n\n{_b[:2200]}\n")
_al = "\n".join(_ass).lower()
_extra = [q for q in faq_md
          if q.split("**")[1][3:40].lower() not in _al][:40]
_ass.append("## Overige veelgestelde vragen\n\n" + "\n".join(_extra))
open(os.path.join(OUT, "assistent.txt"), "w", encoding="utf-8").write(
    "\n".join(_ass) + "\n")

print(f"  llms.txt, llms-full.txt ({len(faq_md)} FAQ's, {len(PC.REVIEWS)} reviews), "
      f"assistent.txt ({os.path.getsize(os.path.join(OUT, 'assistent.txt'))//1024} KiB) "
      "en IndexNow-sleutel geschreven")

# de vier homepages zijn hierboven al gebouwd (vóór de sitemap);
# hier alleen nog de assets meenemen
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
    for js in ("site.js", "ga.js", "zoek.js"):
        p = os.path.join(OUT, "assets", js)
        _src = open(p).read()
        open(p, "w").write(rjsmin.jsmin(_src))
        print(f"  {js} geminificeerd: {len(_src)//1024} -> {os.path.getsize(p)//1024} KiB")
except ImportError:
    print("  rjsmin niet beschikbaar: js ongewijzigd gekopieerd")
# _headers naar dist, met 103 Early Hints (Link-preloads) erin — het
# Cloudflare-equivalent van de oude LiteSpeed-serveroptimalisaties:
# de browser krijgt css en fonts al aangereikt vóór de HTML er is.
_hdrs = open("_headers", encoding="utf-8").read()
_early = ("/*\n"
          f"  Link: </assets/site.css?v={VER}>; rel=preload; as=style\n"
          "  Link: </assets/fonts/archivo-latin.woff2>; rel=preload; as=font; type=font/woff2; crossorigin\n"
          "  Link: </assets/fonts/instrument-latin.woff2>; rel=preload; as=font; type=font/woff2; crossorigin\n"
          "  Link: </assets/fonts/jetbrains-latin.woff2>; rel=preload; as=font; type=font/woff2; crossorigin\n")
_hdrs = _hdrs.replace("/*\n", _early, 1)
# De hash van het speculatieregel-blok in de CSP zetten, berekend uit de
# inhoud die we net gegenereerd hebben - zo kan hij nooit verlopen als de
# regels veranderen. 'inline-speculation-rules' alleen blijkt niet genoeg:
# Chrome eist alsnog een hash zodra de policy hashes bevat.
_spec_hash = "sha256-" + base64.b64encode(hashlib.sha256(
    (json.dumps(spec_regels_json(), separators=(",", ":"))).encode()).digest()).decode()
_hdrs = _hdrs.replace("'inline-speculation-rules'",
                      f"'inline-speculation-rules' '{_spec_hash}'", 1)
open(os.path.join(OUT, "_headers"), "w", encoding="utf-8").write(_hdrs)

# eigen 404-pagina in huisstijl (Cloudflare Pages pakt 404.html automatisch)
_p404 = {"slug": "404", "noindex": True,
         "title": "Deze pagina is in rook opgegaan",
         "seo_title": "404 — Pagina niet gevonden | Vuurspuwer Nuno",
         "seo_desc": "Deze pagina bestaat niet (meer). Bekijk de shows, prijzen en foto's van Vuurspuwer Nuno of neem contact op.",
         "eyebrow": "404", "date": TODAY,
         "img": ("/assets/media/vuurbal-1333.webp",
                 "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
         "body": """
<p><strong>De pagina die je zocht bestaat niet (meer) — maar het vuur brandt gewoon door.</strong> Waarschijnlijk is de pagina verhuisd of klopt het adres net niet.</p>
<p>Waar wil je heen?</p>
<ul>
<li>🔥 <a href="/vuurspuwer-inhuren/">Vuurshow boeken</a> of de <a href="/fakir-show-inhuren/">fakirshow</a> bekijken</li>
<li>💶 <a href="/wat-kost-een-vuurspuwer/">Prijzen en pakketten</a> — vanaf €350</li>
<li>🎃 <a href="/halloween/">Halloween-acts</a> voor oktober</li>
<li>📸 <a href="/fotos/">Foto's</a> en <a href="/videos/">video's</a> van de shows</li>
<li>⭐ <a href="/beoordelingen/">4,9/5 uit 136 beoordelingen</a></li>
<li>✉️ <a href="/contact-3/">Contact en offerte</a> — of app direct via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a></li>
</ul>"""}
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
    _avifize(render(_p404, "page", path="/")))

# offlinepagina: de service worker viel tot nu toe terug op de homepage
# onder het adres van de pagina die je zocht — verwarrend, en met "/" uit
# de precache ook niet meer beschikbaar. Nu een eigen pagina die eerlijk
# zegt wat er aan de hand is, met het telefoonnummer dat wél werkt.
_poff = {"slug": "offline", "noindex": True,
         "title": "Even geen verbinding",
         "seo_title": "Offline — Vuurspuwer Nuno",
         "seo_desc": "Je bent even offline. Zodra je weer verbinding hebt werkt de site gewoon door.",
         "eyebrow": "Offline", "date": TODAY,
         "img": ("/assets/media/vuurbal-1333.webp",
                 "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
         "body": """
<p><strong>Je hebt even geen verbinding.</strong> De pagina's die je al bezocht hebt staan nog in je telefoon en werken gewoon; de rest komt terug zodra je weer online bent.</p>
<p>Haast? Nuno is direct bereikbaar:</p>
<ul>
<li>📞 <a href="tel:+31620020723">06 20 02 07 23</a></li>
<li>💬 <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a></li>
<li>✉️ <a href="mailto:nuno@vuurspuwer.com">nuno@vuurspuwer.com</a></li>
</ul>"""}
os.makedirs(os.path.join(OUT, "offline"), exist_ok=True)
open(os.path.join(OUT, "offline", "index.html"), "w", encoding="utf-8").write(
    _avifize(render(_poff, "page", path="/")))
print("  _headers met Early Hints, 404.html en offlinepagina geschreven")

# service worker: assets cache-first (staan toch een jaar vast), pagina's
# stale-while-revalidate met een versheidsgrens — herhaalbezoek en
# vervolgkliks zijn onmiddellijk, maar niemand krijgt ooit prijzen of
# teksten van meer dan tien minuten oud te zien. Googlebot voert geen
# service worker uit, dus dit raakt indexering op geen enkele manier.
open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8").write("""\
const V = "vs-%s";
/* "/" staat hier bewust NIET in: die haalde de homepage op bij het eerste
   bezoek aan elke willekeurige pagina, ook als de bezoeker er nooit heen
   ging. Hij komt vanzelf in de cache zodra iemand hem opvraagt. */
const CORE = [
  "/assets/site.css?v=%s", "/assets/site.js?v=%s",
  "/assets/fonts/archivo-latin.woff2", "/assets/fonts/instrument-latin.woff2",
  "/assets/fonts/jetbrains-latin.woff2"
];
const OFFLINE = "/offline/";
const VERS = 600000;              /* 10 minuten; daarna eerst het netwerk */
const STEMPEL = "x-sw-at";

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V)
    .then((c) => Promise.all(CORE.map((u) => c.add(u).catch(() => {}))))
    .then(() => caches.open(V).then((c) => c.add(OFFLINE).catch(() => {})))
    .then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil((async () => {
    /* zonder navigationPreload staat de netwerkfetch bij elke navigatie te
       wachten tot de worker is opgestart - op een koude telefoon 50-250ms */
    if (self.registration.navigationPreload) {
      try { await self.registration.navigationPreload.enable(); } catch (x) {}
    }
    const ks = await caches.keys();
    await Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* een gecachede kopie krijgt een tijdstempel mee, zodat we later weten
   of hij nog vers genoeg is om zonder netwerk te serveren */
function metStempel(res) {
  const h = new Headers(res.headers);
  h.set(STEMPEL, String(Date.now()));
  return new Response(res.body, { status: res.status, statusText: res.statusText, headers: h });
}
function vers(res) {
  const t = res && res.headers.get(STEMPEL);
  return !!t && (Date.now() - Number(t)) < VERS;
}

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/")) return;
  /* video's laten we volledig met rust: de browser vraagt ze met Range op,
     krijgt 206 terug, en de Cache API weigert 206 - dat leverde bij elke
     mediarequest een stille afwijzing op, plus een omweg om niets */
  if (/\.(mp4|webm|mov|m4v)$/.test(url.pathname)) return;

  if (url.pathname.startsWith("/assets/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      if (hit) return hit;
      const res = await fetch(e.request);
      if (res.status === 200) { try { await c.put(e.request, res.clone()); } catch (x) {} }
      return res;
    }));
    return;
  }

  if (e.request.mode === "navigate" || url.pathname.endsWith("/")) {
    e.respondWith((async () => {
      const c = await caches.open(V);
      const hit = await c.match(e.request);
      /* de browser is al begonnen met ophalen (navigationPreload); dat
         antwoord gebruiken scheelt een tweede verzoek om hetzelfde */
      const haal = (async () => {
        let res = null;
        try { res = await e.preloadResponse; } catch (x) {}
        if (!res) res = await fetch(e.request);
        if (res && res.status === 200) {
          try { await c.put(e.request, metStempel(res.clone())); } catch (x) {}
        }
        return res;
      })();
      if (hit && vers(hit)) { haal.catch(() => {}); return hit; }
      try { return await haal; } catch (x) { return hit || (await c.match(OFFLINE)) || Response.error(); }
    })());
  }
});
""" % (VER, VER, VER))
print("  sw.js geschreven")

# RSS-feed van de blog: de twintig nieuwste artikelen
from datetime import datetime as _dt
def _rfc822(d):
    return _dt.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 10:00:00 +0000")
_feed_posts = sorted((bp for bp in posts if bp["slug"] not in PC.SHOW_PAGES),
                     key=lambda x: x["date"], reverse=True)[:20]
_items = "".join(f"""
  <item>
    <title>{esc(bp["title"])}</title>
    <link>{SITE}/{bp["slug"]}/</link>
    <guid isPermaLink="true">{SITE}/{bp["slug"]}/</guid>
    <pubDate>{_rfc822(bp["date"])}</pubDate>
    <description>{esc(text_of(bp["body"], 300))}</description>
  </item>""" for bp in _feed_posts)
open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Blog — Vuurspuwer Nuno</title>
  <link>{SITE}/blog/</link>
  <description>Artikelen over vuurshows, fakirshows, veiligheid en het boeken van entertainment in Nederland en België.</description>
  <language>nl</language>
  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>{_items}
</channel>
</rss>
""")
print(f"  feed.xml geschreven ({len(_feed_posts)} artikelen)")
shutil.copy("favicon.ico", os.path.join(OUT, "favicon.ico"))
shutil.copy("site.webmanifest", os.path.join(OUT, "site.webmanifest"))
print("  homepage en assets gekopieerd")

# ------------------------------------------ interne links rechtstreeks
# Elke interne link die op een omgeleid adres uitkwam, wijst nu meteen
# naar het eindadres. Er liepen er 235 via een 301: een extra rondreis
# voor de bezoeker, en voor Google een signaal dat de site zijn eigen
# adressen niet kent. De _redirects blijven staan voor links van buiten;
# de site zelf wijst rechtstreeks. Dit gebeurt ná het schrijven van de
# pagina's, want pas dan is bekend welke adressen omgeleid zijn — en het
# telt niet als inhoudswijziging voor lastmod, want dat is het niet.
_HREF = re.compile(r'href="(https?://vuurspuwer\.com)?(/[^"#?]*?)/?([#?][^"]*)?"')
_ABS_A = re.compile(r'(<a\b[^>]*?)href="https?://vuurspuwer\.com(/[^"]*)"')
_omgezet, _pag = 0, 0
for _root, _, _fs in os.walk(OUT):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _pth = os.path.join(_root, _f)
        _doc = open(_pth, encoding="utf-8").read()
        def _her(m):
            global _omgezet
            pad = m.group(2).rstrip("/") + "/"
            if pad.startswith("/assets/") or pad not in _RD: return m.group(0)
            _omgezet += 1
            return f'href="{m.group(1) or ""}{_RD[pad]}{m.group(3) or ""}"'
        _n = _HREF.sub(_her, _doc)
        # en een interne link hoort niet met het eigen domein ervoor: dat is
        # een erfenis van WordPress en telt in browsers en crawlers als een
        # absolute link naar een andere site — alleen in <a>, niet in
        # canonical/og/hreflang, want die moeten juist absoluut zijn
        _n = _ABS_A.sub(lambda m: m.group(1) + 'href="' + m.group(2) + '"', _n)
        if _n != _doc:
            open(_pth, "w", encoding="utf-8").write(_n); _pag += 1
print(f"  interne links rechtstreeks: {_omgezet} links op {_pag} pagina's wezen naar een omgeleid adres")
for _tf in ("llms.txt", "llms-full.txt", "assistent.txt", "feed.xml", "sitemap.xml"):
    _tp = os.path.join(OUT, _tf)
    if not os.path.exists(_tp): continue
    _tt = open(_tp, encoding="utf-8").read()
    _fout = [b for b in _RD if f"{SITE}{b}" in _tt or f'"{b}"' in _tt]
    if _fout:
        raise SystemExit(f"  ✖ {_tf} verwijst naar omgeleide adressen: {_fout[:5]}")

# ------------------------------------------------ alle foto's in WebP
# Elke zichtbare foto (img-src, srcset, poster) hoort WebP te zijn, met AVIF
# ernaast via <picture>. Uitzonderingen: deelafbeeldingen (og-*) en icoontjes
# blijven jpg/png omdat sociale platforms en iOS dat verwachten; het logo in
# het schema (logo-mail.png) is geen zichtbare foto. Breekt de build zodra er
# een jpg/png-foto insluipt.
_ATTR_IMG = re.compile(r'\b(?:src|srcset|data-poster|poster)="([^"]+)"', re.I)
_MAG_NIET_WEBP = ("og-", "/assets/icon", "apple-touch", "favicon", "maskable", "logo-mail")
_fout_img = set()
for _root, _, _fs in os.walk(OUT):
    for _f in _fs:
        if not _f.endswith(".html"): continue
        _h = open(os.path.join(_root, _f), encoding="utf-8").read()
        for _v in _ATTR_IMG.findall(_h):
            if re.search(r"\.(?:jpe?g|png|gif)(?:\s|,|$|\?)", _v, re.I) and not any(m in _v for m in _MAG_NIET_WEBP):
                _fout_img.add(_v[:90])
if _fout_img:
    raise SystemExit("  \u2716 foto's die geen WebP zijn (zet ze om of voeg een uitzondering toe):\n    " + "\n    ".join(sorted(_fout_img)[:12]))
print("  alle zichtbare foto's in WebP (+AVIF): gecontroleerd")

# grootboek bijwerken: alleen paden die deze build echt bestaan
_LEDGER = {p: v for p, v in _LEDGER.items() if p in _WRITTEN_PATHS}
json.dump(_LEDGER, open(_LEDGER_F, "w", encoding="utf-8"),
          ensure_ascii=False, indent=0, sort_keys=True)
_verschoven = sum(1 for p, v in _LEDGER.items()
                  if _LEDGER_VOOR.get(p) not in (None, v["d"]))
_nieuw = sum(1 for p in _LEDGER if p not in _LEDGER_VOOR)
print(f"  lastmod.json bijgewerkt ({len(_LEDGER)} pagina's: "
      f"{_verschoven} datums verschoven, {_nieuw} nieuw)")
if _verschoven > len(_LEDGER) // 2 and os.environ.get("LASTMOD_BULK") != "1":
    print("  ⚠ meer dan de helft van de lastmod-datums verschoof. Als dat niet de "
          "bedoeling was, push dit niet: Google vertrouwt lastmod alleen als hij "
          "klopt. Bewust? Draai: LASTMOD_BULK=1 python3 build.py")
