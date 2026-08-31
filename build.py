#!/usr/bin/env python3
"""Bouwt de statische site uit de WordPress-export.

Leest de export, kiest de 20 stadspagina's, de blogposts en de vaste
pagina's, en schrijft voor elk een map met een index.html in het ontwerp
van de homepage. Webadressen blijven exact zoals ze nu zijn.
"""
import html, json, os, re, shutil, sys, unicodedata
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser

import pages_content as PC
import i18n as I
import matrix as MX

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
            '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/instrument-latin.woff2" crossorigin>'
            '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/jetbrains-latin.woff2" crossorigin>')

def esc(t): return html.escape(t or "", quote=True)

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
              "reviewCount": "134", "bestRating": "5", "worstRating": "1"}
_OFFER_TXT = {
    "nl": "Prijzen van €350 tot €1500, afhankelijk van show en duur. Vrijblijvende offerte op maat.",
    "en": "Prices from €350 to €1500, depending on show and duration. Free tailored quote.",
    "de": "Preise von 350 € bis 1500 €, je nach Show und Dauer. Kostenloses Angebot nach Maß.",
    "fr": "Prix de 350 € à 1500 €, selon le spectacle et la durée. Devis gratuit sur mesure.",
}
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
    "sameAs": ["https://www.facebook.com/show.nuno",
               "https://www.instagram.com/officialnuno",
               "https://x.com/mentalist_nuno"],
    "aggregateRating": _RATING_LD,
}

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

def _augment_rich_results(graph, lang, page_desc=None, page_img=None, page_url=None):
    def types(g):
        t = g.get("@type")
        return t if isinstance(t, list) else [t]
    extra = []
    for g in graph:
        if not isinstance(g, dict): continue
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
        extra.append(_BUSINESS_LD)
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
        ">Over Nuno<": ">About Nuno<", ">Prijzen<": ">Prices<", ">Beoordelingen<": ">Reviews<", ">Locaties<": ">Locations<",
        ">Aanvraagformulier<": ">Request form<", ">Algemene voorwaarden<": ">Terms &amp; conditions<",
        ">Privacybeleid<": ">Privacy policy<", "<h2>Shows</h2>": "<h2>Shows</h2>",
        "<h2>Site</h2>": "<h2>Site</h2>", "<h2>Contact</h2>": "<h2>Contact</h2>",
        ">Foto&rsquo;s<": ">Photos<", ">Video&rsquo;s<": ">Videos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Certified fire breather &amp; fakir",
        "17 jaar podiumervaring": "17 years of stage experience",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Permits &amp; safety distances arranged",
        "4.9/5 uit 134 reviews": "4.9/5 from 134 reviews",
        'aria-label="Zekerheden"': 'aria-label="Guarantees"',
        ">Bekend van<": ">As seen on<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Known from these channels and productions"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo act by fire breather Nuno: kneeling, he breathes a fireball while a dancer with large red wings stands behind him"',
        "Nederland, Belgi&euml; &amp; internationaal": "Netherlands, Belgium &amp; international"},
 "de": {">Reptielenshow<": ">Reptilienshow<", ">Workshop vuurspuwen<": ">Feuerspucker-Workshop<",
        ">Mentalisme<": ">Mentalismus<", ">Themafeesten<": ">Mottopartys<",
        ">Over Nuno<": ">Über Nuno<", ">Prijzen<": ">Preise<", ">Beoordelingen<": ">Bewertungen<", ">Locaties<": ">Standorte<",
        ">Aanvraagformulier<": ">Anfrageformular<", ">Algemene voorwaarden<": ">AGB<",
        ">Privacybeleid<": ">Datenschutz<", "<h2>Shows</h2>": "<h2>Shows</h2>",
        "<h2>Site</h2>": "<h2>Website</h2>", "<h2>Contact</h2>": "<h2>Kontakt</h2>",
        ">Foto&rsquo;s<": ">Fotos<", ">Video&rsquo;s<": ">Videos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Zertifizierter Feuerspucker &amp; Fakir",
        "17 jaar podiumervaring": "17 Jahre B&uuml;hnenerfahrung",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Genehmigungen &amp; Sicherheitsabst&auml;nde geregelt",
        "4.9/5 uit 134 reviews": "4,9/5 aus 134 Bewertungen",
        'aria-label="Zekerheden"': 'aria-label="Garantien"',
        ">Bekend van<": ">Bekannt aus<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Bekannt aus diesen Sendern und Produktionen"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo-Act von Feuerspucker Nuno: kniend spuckt er einen Feuerball, w&auml;hrend eine T&auml;nzerin mit gro&szlig;en roten Fl&uuml;geln hinter ihm steht"',
        "Nederland, Belgi&euml; &amp; internationaal": "Niederlande, Belgien &amp; international"},
 "fr": {">Reptielenshow<": ">Spectacle de reptiles<", ">Workshop vuurspuwen<": ">Atelier cracheur de feu<",
        ">Mentalisme<": ">Mentalisme<", ">Themafeesten<": ">Fêtes à thème<",
        ">Over Nuno<": ">À propos de Nuno<", ">Prijzen<": ">Tarifs<", ">Beoordelingen<": ">Avis<", ">Locaties<": ">Villes<",
        ">Aanvraagformulier<": ">Formulaire de demande<", ">Algemene voorwaarden<": ">Conditions générales<",
        ">Privacybeleid<": ">Confidentialité<", "<h2>Shows</h2>": "<h2>Spectacles</h2>",
        "<h2>Site</h2>": "<h2>Site</h2>", "<h2>Contact</h2>": "<h2>Contact</h2>",
        ">Foto&rsquo;s<": ">Photos<", ">Video&rsquo;s<": ">Vidéos<",
        "Gecertificeerd vuurspuwer &amp; fakir": "Cracheur de feu &amp; fakir certifié",
        "17 jaar podiumervaring": "17 ans d'expérience scénique",
        "Vergunningseisen &amp; veiligheidsafstanden geregeld": "Autorisations &amp; distances de sécurité gérées",
        "4.9/5 uit 134 reviews": "4,9/5 sur 134 avis",
        'aria-label="Zekerheden"': 'aria-label="Garanties"',
        ">Bekend van<": ">Vu sur<",
        'aria-label="Bekend van deze zenders en producties"': 'aria-label="Vu sur ces chaînes et productions"',
        'alt="Duo-act van vuurspuwer Nuno: geknield spuwt hij een vuurbal terwijl een danseres met grote rode vleugels achter hem staat"':
        'alt="Duo du cracheur de feu Nuno : à genoux, il crache une boule de feu tandis qu\'une danseuse aux grandes ailes rouges se tient derrière lui"',
        "Nederland, Belgi&euml; &amp; internationaal": "Pays-Bas, Belgique &amp; international"},
}
_WA_TEXT = {
 "en": "Hello%20Nuno%2C%20I%20have%20a%20question%20about%20a%20booking",
 "de": "Hallo%20Nuno%2C%20ich%20habe%20eine%20Frage%20zu%20einer%20Buchung",
 "fr": "Bonjour%20Nuno%2C%20j%27ai%20une%20question%20concernant%20une%20r%C3%A9servation",
}
_WA_ARIA = {"en": "Chat with Nuno on WhatsApp", "de": "Mit Nuno auf WhatsApp chatten",
            "fr": "Discuter avec Nuno sur WhatsApp"}
_BRAND_ARIA = {"en": "Fire breather Nuno, to the homepage", "de": "Feuerspucker Nuno, zur Startseite",
               "fr": "Cracheur de feu Nuno, vers l'accueil"}
_CALL_ARIA = {"en": "Call Nuno on +31 6 200 207 23", "de": "Nuno anrufen unter +31 6 200 207 23",
              "fr": "Appeler Nuno au +31 6 200 207 23"}
_CALL_NOW = {"en": ">Call now<", "de": ">Jetzt anrufen<", "fr": ">Appeler<"}
_PRICES_LBL = {"en": "Prices", "de": "Preise", "fr": "Tarifs"}

SITEMAP_IMG = {}   # pad -> [volledige afbeeldings-urls] voor de image-sitemap

_CHROME_CACHE = {}
def chrome(lang):
    """(header, footer) voor een taal; NL is het origineel."""
    if lang == "nl":
        return HEADER, FOOTER
    if lang in _CHROME_CACHE:
        return _CHROME_CACHE[lang]
    L = I.UI[lang]; M = L["menu"]
    h, f = HEADER, FOOTER
    # paginalinks naar de vertaalde tegenhangers (header, menu én footer)
    for nl_slug in I.SLUGS:
        if nl_slug == "": continue
        h = h.replace(f'href="/{nl_slug}/"', f'href="{I.url_of(lang, nl_slug)}"')
        f = f.replace(f'href="/{nl_slug}/"', f'href="{I.url_of(lang, nl_slug)}"')
    h = h.replace('href="/"', f'href="/{lang}/"')
    h = h.replace('href="/#top"', f'href="/{lang}/"')
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
           'aria-label="4,9 van de 5 sterren uit 134 reviews — lees de beoordelingen"': f'aria-label="{L["stars_label"]}"',
           '4.9 &middot; 134 reviews': L["stars_txt"].replace("·", "&middot;"),
           'aria-label="Bel Nuno op +31 6 200 207 23"': f'aria-label="{_CALL_ARIA[lang]}"',
           'aria-label="Menu openen"': f'aria-label="{L["menu_btn"]}"',
           'data-i18n-open="Menu"': "",
           }
    for a, b in lbl.items(): h = h.replace(a, b)
    h = h.replace("Nederland, Belgi&euml; &amp; internationaal",
                  _FOOTER_LABELS[lang]["Nederland, Belgi&euml; &amp; internationaal"])
    # de burger wisselt open/dicht-tekst via data-attributen
    h = h.replace('<button class="burger"',
                  f'<button class="burger" data-txt-open="{L["close_btn"]}" data-txt-closed="{L["menu_btn"]}"')
    for a, b in _FOOTER_LABELS[lang].items(): f = f.replace(a, b)
    f = f.replace(">Vuurshow<", f'>{M["vuurshow"]}<')
    f = f.replace(">Fakirshow<", f'>{M["fakirshow"]}<')
    f = f.replace('href="/"', f'href="/{lang}/"')
    # WhatsApp-knop: taalversie van tekst, label en statuswoorden
    f = f.replace("Hallo%20Nuno%2C%20ik%20heb%20een%20vraag%20over%20een%20boeking", _WA_TEXT[lang])
    f = f.replace('aria-label="Chat met Nuno op WhatsApp"', f'aria-label="{_WA_ARIA[lang]}"')
    f = f.replace('<a class="wa" ', f'<a class="wa" data-online="{L["wa_status_on"]}" data-offline="{L["wa_status_off"]}" ')
    f = f.replace('>Online</b>', f'>{L["wa_status_on"]}</b>')
    _CHROME_CACHE[lang] = (h, f)
    return h, f

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
def spec_rules(lang):
    top = [I.url_of(lang, s) for s in
           ("contact-3", "wat-kost-een-vuurspuwer", "vuurspuwer-inhuren", "halloween")]
    rules = {
        "prefetch": [{"urls": top, "eagerness": "immediate"}],
        "prerender": [{"where": {"and": [
            {"href_matches": "/*"},
            {"not": {"href_matches": "/api/*"}},
            {"not": {"href_matches": "/assets/*"}}]},
            "eagerness": "moderate"}],
    }
    return ('<script type="speculationrules">'
            + json.dumps(rules, separators=(",", ":")) + "</script>")

def render(p, kind, extra_schema=None, extra_html="", lang="nl", path=None, alternates=None):
    L = I.UI[lang]
    p = {**p, "body": _add_toc(p.get("body", ""), lang)}
    title = p["seo_title"] or f'{p["title"]} | Vuurspuwer Nuno'
    desc  = p["seo_desc"] or text_of(p["body"], 155)
    path  = path or (f'/{p["slug"]}/' if p["slug"] else "/")
    url   = SITE + path
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
    preload = ""
    if p.get("img"):
        iu, ia = p["img"]
        if iu.startswith("/"): SITEMAP_IMG[path] = [SITE + iu]
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
    _augment_rich_results(graph, lang, page_desc=desc, page_url=url,
        page_img=(SITE + p["img"][0]) if p.get("img") and p["img"][0].startswith("/") else None)
    ogv = ""
    if p.get("og_video"):
        vu, vw, vh = p["og_video"]
        ogv = (f'<meta property="og:video" content="{SITE}{vu}">\n'
               f'<meta property="og:video:secure_url" content="{SITE}{vu}">\n'
               '<meta property="og:video:type" content="video/mp4">\n'
               f'<meta property="og:video:width" content="{vw}">\n'
               f'<meta property="og:video:height" content="{vh}">')
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(g, ensure_ascii=False)}</script>' for g in graph)

    return f'''<!doctype html>
<html lang="{I.HTML_LANG[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0A0705">
<meta name="color-scheme" content="dark">
<meta name="application-name" content="Vuurspuwer Nuno">
<meta name="apple-mobile-web-app-title" content="Vuurspuwer Nuno">
<meta name="msapplication-TileColor" content="#0A0705">
<style>html{{background:#0A0705;color-scheme:dark}}</style>
<link rel="mask-icon" href="/assets/pinned-tab.svg" color="#FFB020">
<link rel="preconnect" href="https://www.googletagmanager.com">
{GTAG}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
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
<link rel="icon" href="/favicon.ico" sizes="32x32">
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
    links = "".join(f'<li><a href="/halloween-{k}/">🎃 {esc(n)}</a></li>'
                    for k, (n, _sf, _sp) in MX.CITIES.items())
    return (f'<section class="wrap bay hwcities"><h2 class="bay__title">{esc(L["cities"])}</h2>'
            f'<p class="hwcities__p">{esc(L["cities_p"])}</p>'
            f'<ul class="citylist">{links}</ul></section>')

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

# ------------------------------------------------------------------ bouwen
if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT, exist_ok=True)
built, missing = [], []

for slug in CITIES:
    p = pages.get(slug)
    if not p: missing.append(slug); continue
    city = CITY_LABEL[slug]
    others = [(CITY_LABEL[s], s) for s in CITIES if s != slug][:8]
    near = (MX.stad_dwarslinks(slug)
            + '<section class="wrap bay"><h2 class="bay__title">Ook in de <em>buurt</em></h2>'
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

posts = [p for p in pages.values() if p["kind"] == "post"]
for p in posts:
    # workshop-vuurspuwen is in de export een bericht, maar leeft op de
    # site als volwaardige showpagina — die komt uit KEEP_PAGES.
    if p["slug"] in PC.SHOW_PAGES: continue
    write(p["slug"], render(p, "post")); built.append(p["slug"])

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
            p["body"] = hw_top("nl") + '<div class="hwpage">' + p["body"] + "</div>"
        extra = prijs_strip("nl") + PC.show_faq_html(sp)
        if sp["fotos"]:
            extra += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                      + PC._fotorij(sp["fotos"]) + "</div></section>")
        if slug == "halloween":
            extra += hw_cities("nl")
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
        p = {**p, "title": "4,9 uit 134 beoordelingen",
             "seo_title": "⭐ Reviews Vuurspuwer Nuno — 4.9/5 uit 134 beoordelingen",
             "seo_desc": "Lees beoordelingen van opdrachtgevers uit heel NL & BE over de vuurshows en fakirshows van Nuno. Gemiddeld 4.9/5 uit 134 reviews.",
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
extra += hw_cities("nl")
write("halloween", render(p, "page", PC.show_schema("halloween", hp), extra,
                          alternates=alternates_for("halloween")))
built.append("halloween")

# ------------------------------------- de stad x show-matrix (Nederlands)
for show_key in MX.SHOWS:
    for city_key in MX.CITIES:
        p, extra_html, schema = MX.build_page(show_key, city_key)
        write(p["slug"], render(p, "city", schema, extra_html))
        built.append(p["slug"])
print(f"  matrix: {len(MX.SHOWS) * len(MX.CITIES)} stad x show-pagina's")

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
                    "areaServed": [{"@type": "Country", "name": "Nederland"},
                                   {"@type": "Country", "name": "België"},
                                   {"@type": "Country", "name": "Deutschland"}],
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
          data-msg-fail="{esc(F["msg_fail"])}" data-msg-invalid="{esc(F["msg_invalid"])}">
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

def lang_reviews_body(lang):
    T = I.PAGES[lang]["beoordelingen"]["texts"]
    cards = "".join(
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
        <video muted loop playsinline preload="none" poster="/assets/media/{PC._poster(poster)}"
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
_pz = {"slug": "wat-kost-een-vuurspuwer", "title": PZ["title"],
       "seo_title": PZ["seo_title"], "seo_desc": PZ["seo_desc"],
       "img": PZ["img"], "eyebrow": PZ["eyebrow"], "date": TODAY,
       "body": PZ["body"]}
write("wat-kost-een-vuurspuwer",
      render(_pz, "page", PC.show_schema("wat-kost-een-vuurspuwer", PZ),
             PC.show_faq_html(PZ),
             alternates=alternates_for("wat-kost-een-vuurspuwer")))
built.append("wat-kost-een-vuurspuwer")

LANG_ALTS = {}   # pad -> alternates, voor de sitemap
for slug_nl in I.SLUGS:
    alts = alternates_for(slug_nl)
    for l, pth in alts.items():
        LANG_ALTS[pth] = alts

for lang in I.LANGS:
    for nl_slug, T in sorted(I.PAGES[lang].items()):
        path = I.url_of(lang, nl_slug)
        alts = alternates_for(nl_slug)
        out = path.strip("/")
        p = {"slug": out, "title": T["title"], "seo_title": T["seo_title"],
             "seo_desc": T["seo_desc"], "img": T["img"], "eyebrow": T["eyebrow"],
             "date": TODAY, "body": T.get("body", "")}
        extra_html, extra_ld = "", lang_schema(lang, path, T)
        if nl_slug == "":
            p["body"] = lang_home_body(lang)
            extra_html = lang_faq_html(lang, T.get("faq")) + lang_contact_form(lang)
        elif nl_slug == "fotos":
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
                           "workshop-vuurspuwen", "halloween"):
                extra_html = prijs_strip(lang) + extra_html
            if T.get("fotos"):
                extra_html += ('<section class="wrap bay"><div class="prose--page" style="max-width:none">'
                               + lang_fotorij(lang, T["fotos"]) + "</div></section>")
            if nl_slug == "halloween":
                p["body"] = hw_top(lang) + '<div class="hwpage">' + p["body"] + "</div>"
                extra_html += hw_cities(lang)
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
        write(f"{lang}/{loc}", render(p, "page", ld, "", lang=lang, path=path, alternates=alts))
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
        write(f"{lang}/{loc}", render(p, "page", ld, "", lang=lang, path=path))
        built.append(f"{lang}/{loc}")
print(f"  vertaalde pagina's: {sum(len(I.PAGES[l]) for l in I.LANGS)} + "
      f"{sum(len(I.REGIO_PAGES[l]) for l in I.REGIO_PAGES)} regiopagina's (en/de/fr)")

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

# sitemap — met xhtml-alternates voor alle taalversies
_TOP_PAGES = {"halloween", "wat-kost-een-vuurspuwer",
              "en/halloween", "de/halloween", "fr/halloween",
              "en/fire-breather-prices", "de/feuerspucker-kosten",
              "fr/prix-cracheur-de-feu"}
def _prio(s):
    if s in _TOP_PAGES: return "0.9"
    if s in CITIES: return "0.8"
    if s.split("/")[0] in I.LANGS: return "0.7"
    return "0.6"
urls = [("/", "1.0")] + [(f"/{s}/", _prio(s)) for s in sorted(kept)]
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
    "/assets/media/reptiel-960.webp")]
_VIDEOS = [
    ("Showreel Vuurspuwer Nuno - vuurshow op locatie",
     "Beelden van een vuurshow van Vuurspuwer Nuno: vuurspuwen, vuurjongleren en body fire.",
     "/assets/media/reel-1-poster.webp", "/assets/media/reel-1.mp4", 19),
    ("Showreel Vuurspuwer Nuno - acts en fakirwerk",
     "Compilatie van vuur- en fakiracts van Vuurspuwer Nuno op festivals en bedrijfsfeesten.",
     "/assets/media/reel-2-poster.webp", "/assets/media/reel-2.mp4", 58),
    ("Showreel Vuurspuwer Nuno",
     "Korte showreel van vuurspuwer en fakir Nuno.",
     "/assets/media/reel-poster.jpg", "/assets/media/showreel.mp4", 13),
    ("Vuurbal in close-up - Vuurspuwer Nuno",
     "Meters hoge vuurbal van vuurspuwer Nuno, gefilmd van dichtbij.",
     "/assets/media/vuurbal-900.webp", "/assets/media/hero-portrait.mp4", 5),
]
# de fotopagina's melden de complete galerij aan Google Afbeeldingen
_GALLERY = [f"{SITE}/assets/media/{full}" for _k, _t, full, _w, _h, _c, _a in FOTOS]
for _p in ("/fotos/", "/en/photos/", "/de/fotos/", "/fr/photos/"):
    SITEMAP_IMG[_p] = list(dict.fromkeys(SITEMAP_IMG.get(_p, []) + _GALLERY))

for pth, pr in urls:
    entry = f"  <url><loc>{SITE}{pth}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>"
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

> Professionele vuurspuwer, fakir, mentalist en reptielenshow-artiest met 17 jaar ervaring. Optredens in heel Nederland en België (en de Duitse grensregio), vanuit Zeist (NL). Beoordeeld met 4,9/5 uit 134 reviews. Prijzen van €350 tot €1500 per show. Bekend van SBS6, RTL 4, VTM, Uri Geller, Walibi Fright Nights, Julianatoren en Emporium. Volledig gecertificeerd.

Boekingen lopen via het aanvraagformulier of WhatsApp; reactie binnen 24 uur. De volledige site-inhoud in platte tekst staat in [llms-full.txt]({SITE}/llms-full.txt).

## Shows en diensten
- [Vuurshow]({SITE}/vuurspuwer-inhuren/): choreografie van vuurspuwen, vuurjongleren en body fire, 5–30 min, ook als duo met danseres
- [Fakirshow]({SITE}/fakir-show-inhuren/): spijkerbed, glaslopen en zwaarden, met het publiek als deel van de act
- [Workshop vuurspuwen]({SITE}/workshop-vuurspuwen/): zelf leren vuurspuwen — teambuilding, vrijgezellen- en bedrijfsfeesten
- [Halloween-acts]({SITE}/halloween/): duivelse vuurshows en horror-fakir, bekend van de Walibi Fright Nights
- [Reptielenshow]({SITE}/reptielenhow/): educatieve ontmoeting met exotische slangen
- [Mentalisme]({SITE}/entertainer-huren/): gedachtelezen en psychologische illusies, ook binnen inzetbaar
- [Themafeesten]({SITE}/entertainer-huren-voor-bedrijfsfeest/): complete themaproducties van 1001 Nacht tot Caribbean

## Prijzen en boeken
- [Prijzen en pakketten]({SITE}/wat-kost-een-vuurspuwer/): power-act 10 min vanaf €350, showblok 20 min vanaf €450, volledige show 30 min vanaf €595, festivalpakket tot 5×20 min €950–€1500
- [Contact en offerte]({SITE}/contact-3/): aanvraagformulier, antwoord binnen 24 uur
- [Beoordelingen]({SITE}/beoordelingen/): 4,9/5 uit 134 reviews van opdrachtgevers
- [Over Nuno]({SITE}/over-nuno/): 17 jaar ervaring, tv-optredens bij SBS6, RTL en VTM
- Telefoon/WhatsApp: +31 6 200 207 23 · E-mail: nuno@vuurspuwer.com · KvK 98164325

## Media
- [Foto's]({SITE}/fotos/): galerij met licenseerbare showfoto's
- [Video's]({SITE}/videos/): showreels van vuur- en fakiracts
- [Locaties]({SITE}/locaties-vuurshows-nederland-belgie/): alle steden in Nederland en België

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

parts.append("## Reviews van opdrachtgevers (4,9/5 uit 134 beoordelingen)\n\n" +
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
print(f"  llms.txt, llms-full.txt ({len(faq_md)} FAQ's, {len(PC.REVIEWS)} reviews) "
      "en IndexNow-sleutel geschreven")

# homepage en assets meenemen; ook daar de versie-stempel op css/js,
# de volledige hreflang-set en de taalkeuze in de footer
hp_doc = open("index.html", encoding="utf-8").read()
for a in ("assets/site.css", "assets/site.js", "assets/ga.js"):
    hp_doc = hp_doc.replace(f'"/{a}"', f'"/{a}?v={VER}"')
home_alts = alternates_for("")
hre = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{home_alts[l]}">\n'
              for l in ("nl", "en", "de", "fr"))
hp_doc = hp_doc.replace(
    '<link rel="alternate" hreflang="nl" href="https://vuurspuwer.com/">\n'
    '<link rel="alternate" hreflang="x-default" href="https://vuurspuwer.com/">',
    hre + '<link rel="alternate" hreflang="x-default" href="https://vuurspuwer.com/">')
hp_doc = hp_doc.replace('<div class="foot__bar">',
                        lang_row("nl", home_alts) + '\n  <div class="foot__bar">')
hp_doc = hp_doc.replace("</head>", spec_rules("nl") + "\n</head>", 1)
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
open(os.path.join(OUT, "_headers"), "w", encoding="utf-8").write(_hdrs)

# eigen 404-pagina in huisstijl (Cloudflare Pages pakt 404.html automatisch)
_p404 = {"slug": "404", "title": "Deze pagina is in rook opgegaan",
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
<li>⭐ <a href="/beoordelingen/">4,9/5 uit 134 beoordelingen</a></li>
<li>✉️ <a href="/contact-3/">Contact en offerte</a> — of app direct via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a></li>
</ul>"""}
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
    render(_p404, "page", path="/"))
print("  _headers met Early Hints en 404.html geschreven")

# service worker: assets cache-first (staan toch een jaar vast), pagina's
# stale-while-revalidate — herhaalbezoek en vervolgkliks zijn daarmee
# onmiddellijk, en de site werkt zelfs offline als brochure.
open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8").write("""\
const V = "vs-%s";
const CORE = [
  "/", "/assets/site.css?v=%s", "/assets/site.js?v=%s",
  "/assets/fonts/archivo-latin.woff2", "/assets/fonts/instrument-latin.woff2",
  "/assets/fonts/jetbrains-latin.woff2"
];
self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(V).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k !== V).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.startsWith("/api/")) return;
  if (url.pathname.startsWith("/assets/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      if (hit) return hit;
      const res = await fetch(e.request);
      if (res.ok) c.put(e.request, res.clone());
      return res;
    }));
    return;
  }
  if (e.request.mode === "navigate" || url.pathname.endsWith("/")) {
    e.respondWith(caches.open(V).then(async (c) => {
      const hit = await c.match(e.request);
      const net = fetch(e.request).then((res) => {
        if (res.ok) c.put(e.request, res.clone());
        return res;
      }).catch(() => hit || c.match("/"));
      return hit || net;
    }));
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
