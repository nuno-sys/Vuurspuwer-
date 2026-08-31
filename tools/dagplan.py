#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dagelijkse indexeermotor voor vuurspuwer.com — het masterplan.

Elke dag kiest dit script de tien belangrijkste adressen van dat moment en
meldt ze aan bij elke zoekmachine die dat toestaat. De keuze is niet
willekeurig maar berekend uit drie factoren:

  1. BASISGEWICHT  — hoe belangrijk is de pagina voor boekingen?
     (homepage en prijzen zwaarder dan een oud blogbericht)
  2. SEIZOEN       — Halloween telt in september/oktober veel zwaarder,
     kerst en nieuwjaar in november/december, bruiloften in het voorjaar,
     festivals in de zomer. Zo staat de juiste pagina vooraan wanneer er
     ook echt op gezocht wordt.
  3. WACHTTIJD     — hoe langer een pagina niet is aangemeld, hoe hoger hij
     stijgt. Daardoor komt op termijn de héle site aan de beurt zonder dat
     dezelfde pagina's elkaar verdringen.

Wat er per dag gebeurt:
  • IndexNow   — volautomatisch (Bing, DuckDuckGo, Yandex, Seznam, Naver).
  • Bing API   — volautomatisch zodra het geheim BING_API_KEY is ingesteld.
  • Sitemaps   — opnieuw aangemeld bij Bing.
  • Google     — Google heeft géén open aanmeld-API voor gewone pagina's
    (de Indexing API is officieel alleen voor vacatures en livestreams;
    misbruik riskeert je toegang). Daarom schrijft dit script dagplan.md
    met tien kant-en-klare Search Console-links: aanklikken, op
    'Indexering aanvragen' drukken, klaar in twee minuten.

Gebruik:  python3 tools/dagplan.py            (dagplan maken + aanmelden)
          python3 tools/dagplan.py --dry-run  (alleen tonen, niets versturen)
"""
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import date, datetime, timedelta

SITE = "https://vuurspuwer.com"
KEY = "031a0a94dea279b0f3c9d84a5f39a7be"
STATE_FILE = "indexing-state.json"
PLAN_FILE = "dagplan.md"
PER_DAG = 10
# een pagina komt pas na deze wachttijd opnieuw in aanmerking
RUSTDAGEN = 21

# ------------------------------------------------------------ basisgewicht
# hoe dichter bij een boeking, hoe hoger. 100 = homepage.
_BASIS = [
    (100, lambda s: s == ""),
    (95,  lambda s: s in ("wat-kost-een-vuurspuwer", "contact-3", "vuurspuwer-inhuren")),
    (90,  lambda s: s in ("halloween", "fakir-show-inhuren", "workshop-vuurspuwen",
                          "beoordelingen", "vuur-woordenboek")),
    (85,  lambda s: s.startswith(("vuurshow-", "vrijgezellenfeest", "vuurwerk-alternatief",
                                  "kerst-nieuwjaar-entertainment"))),
    (75,  lambda s: s.startswith("vuurspuwer-boeken-in-") or s == "locaties-vuurshows-nederland-belgie"),
    (70,  lambda s: s.split("/")[0] in ("en", "de", "fr")),
    (65,  lambda s: s.startswith(("halloween-", "fakirshow-", "workshop-vuurspuwen-"))),
    (60,  lambda s: s in ("fotos", "videos", "blog", "over-nuno")),
]
def basisgewicht(slug):
    for punten, test in _BASIS:
        try:
            if test(slug): return punten
        except Exception:
            pass
    return 40  # blogberichten en overige pagina's

# ---------------------------------------------------------------- seizoen
# (maand -> [(trefwoord, bonus), ...]) — trefwoord wordt in de slug gezocht
_SEIZOEN = {
    1:  [("nieuwjaar", 40), ("kerst", 15), ("bruiloft", 20), ("vrijgezell", 15)],
    2:  [("bruiloft", 30), ("vrijgezell", 20), ("bedrijfsfeest", 15)],
    3:  [("bruiloft", 35), ("festival", 20), ("vrijgezell", 20)],
    4:  [("bruiloft", 35), ("festival", 30), ("verjaardag", 15)],
    5:  [("festival", 35), ("bruiloft", 30), ("verjaardag", 15)],
    6:  [("festival", 40), ("bruiloft", 25), ("workshop", 15)],
    7:  [("festival", 40), ("verjaardag", 20), ("workshop", 15)],
    8:  [("festival", 30), ("halloween", 25), ("bedrijfsfeest", 20)],
    9:  [("halloween", 50), ("bedrijfsfeest", 25), ("festival", 15)],
    10: [("halloween", 60), ("bedrijfsfeest", 25), ("kerst", 15)],
    11: [("kerst", 50), ("nieuwjaar", 35), ("bedrijfsfeest", 30)],
    12: [("kerst", 55), ("nieuwjaar", 50), ("bedrijfsfeest", 25)],
}
# vertaalde slugs tellen mee voor hetzelfde thema
_THEMA_ALIAS = {
    "halloween":     ("halloween",),
    "kerst":         ("kerst", "christmas", "weihnacht", "noel", "noël"),
    "nieuwjaar":     ("nieuwjaar", "new-year", "silvester", "nouvel-an"),
    "bruiloft":      ("bruiloft", "wedding", "hochzeit", "mariage"),
    "festival":      ("festival",),
    "verjaardag":    ("verjaardag", "birthday", "geburtstag", "anniversaire"),
    "bedrijfsfeest": ("bedrijfsfeest", "corporate", "firmen", "entreprise"),
    "vrijgezell":    ("vrijgezell", "bachelor", "junggesell", "evjf"),
    "workshop":      ("workshop", "atelier"),
}
def seizoensbonus(slug, maand):
    s = slug.lower()
    bonus = 0
    for thema, punten in _SEIZOEN.get(maand, []):
        if any(a in s for a in _THEMA_ALIAS.get(thema, (thema,))):
            bonus = max(bonus, punten)
    return bonus

# ------------------------------------------------------------------ hulp
def lees_sitemap(pad="dist/sitemap.xml"):
    if not os.path.exists(pad):
        sys.exit(f"✗ {pad} niet gevonden — draai eerst: python3 build.py")
    xml = open(pad, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)

def slug_van(url):
    return url.replace(SITE, "").strip("/")

def lees_state():
    try:
        return json.load(open(STATE_FILE, encoding="utf-8"))
    except Exception:
        return {"laatst": {}, "historie": []}

def schrijf_state(state):
    state["historie"] = state["historie"][-90:]
    json.dump(state, open(STATE_FILE, "w", encoding="utf-8"),
              ensure_ascii=False, indent=0, sort_keys=True)

def kies_dagplan(urls, state, vandaag, aantal=PER_DAG):
    """Scoort alle adressen en geeft de beste `aantal` terug."""
    laatst = state.get("laatst", {})
    maand = vandaag.month
    gescoord = []
    for u in urls:
        s = slug_van(u)
        score = basisgewicht(s) + seizoensbonus(s, maand)
        vorige = laatst.get(u)
        if vorige:
            dagen = (vandaag - date.fromisoformat(vorige)).days
            if dagen < RUSTDAGEN:
                continue                       # nog in rust, sla over
            score += min(dagen - RUSTDAGEN, 60)  # hoe langer geleden, hoe hoger
        else:
            score += 60                        # nog nooit aangemeld: voorrang
        gescoord.append((score, u))
    if not gescoord:                            # alles in rust: neem de oudste
        gescoord = [(-(date.fromisoformat(laatst[u]).toordinal()), u)
                    for u in urls if u in laatst]
    gescoord.sort(key=lambda t: (-t[0], t[1]))
    return [u for _, u in gescoord[:aantal]]

# ------------------------------------------------------- aanmeldkanalen
def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode()
    hdr = {"Content-Type": "application/json; charset=utf-8"}
    hdr.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdr)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")[:200]

def naar_indexnow(urls):
    """Bing, DuckDuckGo, Yandex, Seznam en Naver in één melding."""
    payload = {"host": "vuurspuwer.com", "key": KEY,
               "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}
    st, body = post_json("https://api.indexnow.org/indexnow", payload)
    return f"IndexNow: {st} ({len(urls)} adressen)"

def naar_bing(urls):
    """Bing URL Submission API — alleen als het geheim is ingesteld."""
    api = os.environ.get("BING_API_KEY", "").strip()
    if not api:
        return "Bing API: overgeslagen (geen BING_API_KEY ingesteld)"
    ep = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={api}"
    st, body = post_json(ep, {"siteUrl": SITE, "urlList": urls})
    return f"Bing API: {st} ({len(urls)} adressen)"

def sitemaps_aanmelden(sitemaps):
    """Bing accepteert nog een sitemap-ping; Google stopte daar in 2023 mee."""
    uit = []
    for sm in sitemaps:
        doel = "https://www.bing.com/ping?sitemap=" + urllib.parse.quote(sm, safe="")
        try:
            with urllib.request.urlopen(doel, timeout=20) as r:
                uit.append(f"Bing sitemap-ping {r.status}: {sm}")
        except Exception as e:
            uit.append(f"Bing sitemap-ping mislukt ({e.__class__.__name__}): {sm}")
    return uit

# ------------------------------------------------------------- dagplan.md
def gsc_link(url):
    return ("https://search.google.com/search-console/inspect"
            f"?resource_id=sc-domain%3Avuurspuwer.com&id={urllib.parse.quote(url, safe='')}")

def schrijf_dagplan(urls, vandaag, meldingen):
    regels = [f"# Indexeer-dagplan {vandaag.isoformat()}", "",
              "Google kent géén open aanmeld-API voor gewone pagina's, dus deze tien",
              "adressen zijn met de hand aan te melden. Klik een link, druk op",
              "**Indexering aanvragen** — samen twee minuten werk per dag.", "",
              "| # | Pagina | Aanmelden bij Google |", "|---|---|---|"]
    for i, u in enumerate(urls, 1):
        naam = slug_van(u) or "homepage"
        regels.append(f"| {i} | `{naam}` | [openen in Search Console]({gsc_link(u)}) |")
    regels += ["", "## Automatisch verstuurd", ""]
    regels += [f"- {m}" for m in meldingen]
    regels += ["", f"_Volgende ronde: {(vandaag + timedelta(days=1)).isoformat()}_", ""]
    open(PLAN_FILE, "w", encoding="utf-8").write("\n".join(regels))

# ----------------------------------------------------------------- main
def main():
    dry = "--dry-run" in sys.argv
    vandaag = date.today()
    urls = lees_sitemap()
    state = lees_state()
    plan = kies_dagplan(urls, state, vandaag)

    print(f"── Dagplan {vandaag} — {len(plan)} van {len(urls)} adressen")
    for i, u in enumerate(plan, 1):
        s = slug_van(u)
        print(f"   {i:2}. {s or '(homepage)'}  "
              f"[basis {basisgewicht(s)} + seizoen {seizoensbonus(s, vandaag.month)}]")

    meldingen = []
    if dry:
        print("\n── --dry-run: niets verstuurd")
        meldingen = ["(dry-run, niets verstuurd)"]
    else:
        print("\n── Aanmelden")
        sitemaps = [f"{SITE}/sitemap.xml"]
        if os.path.exists("dist/sitemap-index.xml"):
            sitemaps.insert(0, f"{SITE}/sitemap-index.xml")
        for fn in (lambda: naar_indexnow(plan), lambda: naar_bing(plan)):
            try:
                m = fn()
            except Exception as e:
                m = f"{fn.__name__ if hasattr(fn,'__name__') else 'kanaal'} mislukt: {e}"
            print("  ", m); meldingen.append(m)
        for m in sitemaps_aanmelden(sitemaps):
            print("  ", m); meldingen.append(m)
        for u in plan:
            state.setdefault("laatst", {})[u] = vandaag.isoformat()
        state.setdefault("historie", []).append(
            {"datum": vandaag.isoformat(), "urls": plan})
        schrijf_state(state)

    schrijf_dagplan(plan, vandaag, meldingen)
    print(f"\n✓ {PLAN_FILE} geschreven — tien Search Console-links klaar om aan te klikken")
    aangemeld = len(state.get("laatst", {}))
    print(f"✓ dekking: {aangemeld}/{len(urls)} adressen ooit aangemeld")

if __name__ == "__main__":
    main()
