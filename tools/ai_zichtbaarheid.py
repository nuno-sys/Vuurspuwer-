#!/usr/bin/env python3
"""AI-zichtbaarheidsmeter voor vuurspuwer.com.

Stelt een vaste set vragen - zoals klanten ze stellen, in vier talen en voor
vier markten - aan AI-assistenten met webzoeken aan, en legt per antwoord vast:
  * genoemd:    staat Nuno / Vuurspuwer Nuno / vuurspuwer.com in het antwoord?
  * geciteerd:  is een pagina van vuurspuwer.com als bron aangehaald?
  * welke andere domeinen wél als bron zijn aangehaald (de concurrentie).

Dit is geen trucje om verkeer te "halen": AI-assistenten noemen een bedrijf als
hun zoekindex en hun bronnen het noemen. Deze meter laat zien waar dat al zo is,
waar niet, en welke sites in plaats daarvan worden aangehaald. Dat is de basis
om gericht te verbeteren, en om te zien of het werkt.

Aanbieders (elk draait alleen als de sleutel als omgevingsvariabele bestaat):
  anthropic   ANTHROPIC_API_KEY   Claude, met de server-side webzoektool
  openai      OPENAI_API_KEY      Responses API met de webzoektool
  gemini      GEMINI_API_KEY      Gemini API met Grounding with Google Search
  perplexity  PERPLEXITY_API_KEY  Agent API met webzoeken (perplexity/sonar)
Modellen zijn per aanbieder te overschrijven met ANTHROPIC_MODEL, OPENAI_MODEL,
GEMINI_MODEL en PERPLEXITY_MODEL.

Gebruik:
  python3 tools/ai_zichtbaarheid.py               meting + rapport
  python3 tools/ai_zichtbaarheid.py --rapport     alleen het rapport opnieuw maken
  python3 tools/ai_zichtbaarheid.py --zelftest    verwerking testen zonder API
  python3 tools/ai_zichtbaarheid.py --max 3       alleen de eerste 3 vragen
  python3 tools/ai_zichtbaarheid.py --toegang     live: mogen en kunnen AI-crawlers erbij?
Uitvoer: ai-zichtbaarheid/metingen/<datum>.json, ai-zichtbaarheid/toegang.json
en ai-zichtbaarheid/RAPPORT.md
"""
import argparse, collections, datetime, json, os, re, sys, time
import urllib.error, urllib.parse, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HIER, "..", "ai-zichtbaarheid")
METINGEN = os.path.join(MAP, "metingen")
DOEL_DOMEIN = "vuurspuwer.com"
# "Nuno" alleen telt mee: alle vragen gaan over vuur-, fakir- of mentalisme-acts,
# dus een Nuno in het antwoord is vrijwel zeker hij
GENOEMD_RX = re.compile(r"vuurspuwer\.com|vuurspuwer\s+nuno|\bnuno\b", re.I)

# (id, taal, land, vraag) - land is de ISO-code die als locatie wordt meegegeven
VRAGEN = [
 ("nl-bruiloft-utrecht", "nl", "NL", "Ik zoek een vuurspuwer voor mijn bruiloft in de buurt van Utrecht. Wie kun je aanraden?"),
 ("nl-prijs", "nl", "NL", "Wat kost het om een vuurspuwer in te huren in Nederland?"),
 ("nl-fakirshow", "nl", "NL", "Welke fakirshow kan ik boeken voor een bedrijfsfeest in Nederland?"),
 ("nl-mentalist", "nl", "NL", "Ik wil een mentalist boeken voor een personeelsfeest. Welke mentalisten in Nederland zijn goed?"),
 ("nl-vuurwerk-alternatief", "nl", "NL", "Wat is een goed alternatief voor vuurwerk op een bruiloft of bedrijfsfeest?"),
 ("nl-workshop", "nl", "NL", "Waar kan ik met mijn team een workshop vuurspuwen doen als teambuilding?"),
 ("nl-amsterdam", "nl", "NL", "Vuurshow boeken in Amsterdam: welke vuurartiesten zijn er?"),
 ("nl-entertainer", "nl", "NL", "Welke entertainer kan ik inhuren voor een themafeest zoals 1001 nacht?"),
 ("nl-maastricht", "nl", "NL", "vuurspuwer inhuren Maastricht"),
 ("nl-vlammenshow", "nl", "NL", "vlammenshow huren voor een verjaardag"),
 ("be-antwerpen", "nl", "BE", "Ik zoek een vuurspuwer voor een bedrijfsevent in Antwerpen. Wie raad je aan?"),
 ("be-tentfeest", "nl", "BE", "Vuurshow voor een tentfeest in West-Vlaanderen, wie kan dat?"),
 ("fr-liege", "fr", "BE", "Je cherche un cracheur de feu pour un mariage à Liège. Qui me conseillez-vous ?"),
 ("fr-bruxelles", "fr", "BE", "Spectacle de feu à Bruxelles pour une soirée d'entreprise : quels artistes ?"),
 ("fr-luxembourg", "fr", "LU", "Cracheur de feu au Luxembourg pour un mariage, qui contacter ?"),
 ("de-aachen", "de", "DE", "Feuerspucker für eine Hochzeit in Aachen buchen – wen empfiehlst du?"),
 ("de-duesseldorf", "de", "DE", "Feuershow mieten in Düsseldorf für eine Firmenfeier"),
 ("de-luxemburg", "de", "LU", "Feuerspucker in Luxemburg buchen"),
 ("en-nl", "en", "NL", "I want to hire a fire breather for a wedding in the Netherlands. Who do you recommend?"),
 ("en-be", "en", "BE", "Fakir show or mentalist for a corporate event in Belgium - who can I book?"),
]

SYSTEEM = ("Answer the user's question as a helpful assistant would, using web search. "
           "Name concrete performers or companies where you can, and cite your sources.")


# ------------------------------------------------------------------ hulpjes
def domein(url):
    try:
        h = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        return ""
    return h.lower().removeprefix("www.")

def _post(url, kop, lijf, timeout=180, pogingen=3):
    req = urllib.request.Request(url, data=json.dumps(lijf).encode(), method="POST",
                                 headers={"Content-Type": "application/json", **kop})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            # te druk of tijdelijk stuk: even wachten en opnieuw; al het andere is echt fout
            if e.code not in (429, 500, 502, 503, 504) or poging == pogingen - 1:
                raise
            time.sleep(10 * 2 ** poging)

def _uniek(lijst):
    return list(dict.fromkeys(x for x in lijst if x))


# ------------------------------------------------------------ verwerkers
# Elk ontleedt het ruwe antwoord van één aanbieder naar dezelfde vorm:
# {"tekst": str, "geciteerd": [urls/domeinen], "gelezen": [urls]}.
# Gescheiden van de aanroep, zodat --zelftest ze zonder API kan controleren.

def ontleed_anthropic(blokken):
    """blokken: response.content als lijst dicts (model_dump)."""
    tekst, geciteerd, gelezen = [], [], []
    for b in blokken:
        t = b.get("type")
        if t == "text":
            tekst.append(b.get("text") or "")
            for c in b.get("citations") or []:
                if c.get("url"): geciteerd.append(c["url"])
        elif t == "web_search_tool_result":
            inhoud = b.get("content")
            # bij een fout is content een object, bij succes een lijst
            if isinstance(inhoud, list):
                gelezen += [r.get("url") for r in inhoud if isinstance(r, dict)]
    return {"tekst": "".join(tekst), "geciteerd": _uniek(geciteerd), "gelezen": _uniek(gelezen)}

def ontleed_openai(antwoord):
    # output[] is een gemengde lijst (reasoning, web_search_call, message):
    # altijd op type filteren, nooit op positie
    tekst, geciteerd, gelezen, gezocht = [], [], [], False
    for item in antwoord.get("output") or []:
        if item.get("type") == "web_search_call":
            gezocht = gezocht or item.get("status") == "completed"
            gelezen += [b.get("url") for b in (item.get("action") or {}).get("sources") or []
                        if isinstance(b, dict)]
        if item.get("type") != "message": continue
        for c in item.get("content") or []:
            if c.get("type") != "output_text": continue
            tekst.append(c.get("text") or "")
            for a in c.get("annotations") or []:
                if a.get("type") == "url_citation" and a.get("url"):
                    geciteerd.append(a["url"])
    return {"tekst": "".join(tekst), "geciteerd": _uniek(geciteerd), "gelezen": _uniek(gelezen),
            "gezocht": gezocht}

def _gemini_domein(web):
    """Het echte domein van een Gemini-bron. web.uri is altijd een omleiding via
    vertexaisearch.cloud.google.com; in de praktijk staat het domein in
    web.title (geobserveerd gedrag, geen gedocumenteerd contract). Lukt dat
    niet, dan wordt de omleiding opgevraagd zonder haar te volgen en telt de
    Location-header (de werkwijze uit python-genai issue #1512)."""
    titel = (web.get("title") or "").strip().lower().removeprefix("www.")
    if re.fullmatch(r"([a-z0-9-]+\.)+[a-z]{2,}", titel):
        return "https://" + titel + "/"
    uri = web.get("uri") or ""
    if "grounding-api-redirect" not in uri:
        return uri
    if os.environ.get("AI_ZICHT_GEEN_NET"):
        return ""
    class _Stop(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    try:
        urllib.request.build_opener(_Stop).open(urllib.request.Request(uri, method="HEAD"), timeout=10)
    except urllib.error.HTTPError as e:
        return e.headers.get("Location") or ""
    except Exception:
        return ""
    return ""

def ontleed_gemini(antwoord):
    kand = (antwoord.get("candidates") or [{}])[0]
    # denkdelen (thought: true) horen niet bij het antwoord
    tekst = "".join(p.get("text", "") for p in (kand.get("content") or {}).get("parts") or []
                    if not p.get("thought"))
    meta = kand.get("groundingMetadata") or {}
    chunks = meta.get("groundingChunks") or []
    gebruikt = {i for s_ in meta.get("groundingSupports") or [] for i in s_.get("groundingChunkIndices") or []}
    gelezen, geciteerd = [], []
    for i, ch in enumerate(chunks):
        url = _gemini_domein(ch.get("web") or {})
        gelezen.append(url)
        # alleen een bron die in groundingSupports aan de tekst is gekoppeld,
        # is daadwerkelijk aangehaald; de rest is alleen opgehaald
        if i in gebruikt: geciteerd.append(url)
    return {"tekst": tekst, "geciteerd": _uniek(geciteerd), "gelezen": _uniek(gelezen),
            "gezocht": bool(meta.get("webSearchQueries") or chunks)}

def ontleed_perplexity(antwoord):
    """Agent API (/v1/agent): output[] met items 'message', 'search_results'
    en 'fetch_url_results'. Perplexity toont alle zoekresultaten als bronnenlijst
    bij het antwoord, dus die tellen als geciteerd; inline annotaties zijn vaak leeg."""
    tekst, geciteerd, gelezen, gezocht = [], [], [], False
    for it in antwoord.get("output") or []:
        t = it.get("type")
        if t == "message":
            for p in it.get("content") or []:
                if p.get("type") == "output_text":
                    tekst.append(p.get("text") or "")
                    geciteerd += [a.get("url") for a in p.get("annotations") or [] if a.get("url")]
        elif t == "search_results":
            gezocht = True
            urls = [r.get("url") for r in it.get("results") or [] if isinstance(r, dict)]
            geciteerd += urls; gelezen += urls
        elif t == "fetch_url_results":
            gelezen += [c.get("url") for c in it.get("contents") or [] if isinstance(c, dict)]
    return {"tekst": "".join(tekst), "geciteerd": _uniek(geciteerd),
            "gelezen": _uniek(gelezen + geciteerd), "gezocht": gezocht}


# -------------------------------------------------------------- aanroepen
def vraag_anthropic(vraag, land):
    # Officiële Anthropic Python-SDK (pip install anthropic); de sleutel komt
    # uit ANTHROPIC_API_KEY.
    import anthropic
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL") or "claude-opus-5-5"
    tools = [{"type": "web_search_20260209", "name": "web_search", "max_uses": 3,
              "user_location": {"type": "approximate", "country": land}}]
    berichten = [{"role": "user", "content": vraag}]
    alle = []
    for _ in range(4):   # een lange zoekbeurt kan pauzeren (pause_turn): hervatten
        r = client.beta.messages.create(
            model=model, max_tokens=4000, system=SYSTEEM, tools=tools,
            output_config={"effort": "medium"},
            # bij een weigering neemt de API zelf een ander model over
            betas=["server-side-fallback-2026-07-01"], fallbacks="default",
            messages=berichten)
        blokken = [b.model_dump() for b in r.content]
        alle += blokken
        if r.stop_reason != "pause_turn": break
        berichten = [{"role": "user", "content": vraag},
                     {"role": "assistant", "content": r.content}]
    if r.stop_reason == "refusal":
        raise RuntimeError("geweigerd")
    uit = ontleed_anthropic(alle)
    uit["model"] = r.model
    return uit

def vraag_openai(vraag, land):
    model = os.environ.get("OPENAI_MODEL") or "gpt-6-luna"
    a = _post("https://api.openai.com/v1/responses",
              {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
              {"model": model, "instructions": SYSTEEM, "input": vraag,
               # zonder land rekent de zoektool met de Verenigde Staten
               "tools": [{"type": "web_search",
                          "user_location": {"type": "approximate", "country": land}}],
               # anders beslist het model zelf of het zoekt, en dan meet je soms
               # een antwoord uit het geheugen in plaats van uit de zoekindex
               "tool_choice": "required", "max_tool_calls": 3,
               "include": ["web_search_call.action.sources"], "store": False})
    uit = ontleed_openai(a); uit["model"] = a.get("model", model)
    if not uit.get("gezocht"):
        raise RuntimeError("geen voltooide zoekopdracht in het antwoord; meting ongeldig")
    return uit

def vraag_gemini(vraag, land):
    # 2.5 is sinds 18 september 2026 beperkt tot bestaande gebruikers
    model = os.environ.get("GEMINI_MODEL") or "gemini-3.5-flash-lite"
    a = _post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
              {"x-goog-api-key": os.environ["GEMINI_API_KEY"]},
              {"systemInstruction": {"parts": [{"text": SYSTEEM}]},
               "contents": [{"role": "user", "parts": [{"text": vraag}]}],
               "tools": [{"google_search": {}}]})
    uit = ontleed_gemini(a); uit["model"] = a.get("modelVersion", model)
    if not uit.get("gezocht"):
        raise RuntimeError("Gemini heeft niet gezocht; meting ongeldig")
    return uit

def vraag_perplexity(vraag, land):
    # De oude Sonar-API (/chat/completions) wordt sinds 27 september 2026 niet
    # meer ondersteund; dit is de Agent API. Die weigert onbekende velden met
    # een 400, dus alleen velden uit de officiële SDK-typen.
    model = os.environ.get("PERPLEXITY_MODEL") or "perplexity/sonar"
    a = _post("https://api.perplexity.ai/v1/agent",
              {"Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"},
              {"model": model, "instructions": SYSTEEM, "input": vraag,
               "tools": [{"type": "web_search", "user_location": {"country": land}}],
               "max_output_tokens": 2000})
    # ook een mislukte run komt terug met HTTP 200
    if a.get("status") != "completed":
        raise RuntimeError(f"status {a.get('status')}: {str(a.get('error'))[:200]}")
    uit = ontleed_perplexity(a); uit["model"] = a.get("model", model)
    if not uit["gezocht"]:
        raise RuntimeError("Perplexity heeft niet gezocht; meting ongeldig")
    return uit

AANBIEDERS = {
    "anthropic": ("ANTHROPIC_API_KEY", "Claude", vraag_anthropic),
    "openai": ("OPENAI_API_KEY", "ChatGPT", vraag_openai),
    "gemini": ("GEMINI_API_KEY", "Gemini", vraag_gemini),
    "perplexity": ("PERPLEXITY_API_KEY", "Perplexity", vraag_perplexity),
}


# ----------------------------------------------------------------- meting
def _eigen(d):
    return d == DOEL_DOMEIN or d.endswith("." + DOEL_DOMEIN)

def beoordeel(uit):
    doms = [domein(u) for u in uit["geciteerd"]]
    return {
        "genoemd": bool(GENOEMD_RX.search(uit["tekst"])),
        "geciteerd": any(_eigen(d) for d in doms),
        "gelezen": any(_eigen(domein(u)) for u in uit.get("gelezen", [])),
        "andere_domeinen": _uniek(d for d in doms if d and not _eigen(d)),
    }

def meet(max_vragen=None, alleen=None):
    actief = {k: v for k, v in AANBIEDERS.items()
              if os.environ.get(v[0]) and (not alleen or k in alleen)}
    if not actief:
        print("Geen enkele API-sleutel gezet; niets te meten. Zie de uitleg bovenin dit bestand.")
        return None
    print("Aanbieders:", ", ".join(v[1] for v in actief.values()))
    rijen = []
    for vid, taal, land, vraag in VRAGEN[:max_vragen or None]:
        for sleutel, (_, naam, fn) in actief.items():
            rij = {"vraag": vid, "taal": taal, "land": land, "aanbieder": sleutel}
            try:
                uit = fn(vraag, land)
                rij.update(beoordeel(uit), model=uit.get("model"),
                           tekst=uit["tekst"][:3000], bronnen=uit["geciteerd"][:25])
            except urllib.error.HTTPError as e:
                rij["fout"] = f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}"
            except Exception as e:  # één mislukte vraag mag de meting niet stoppen
                rij["fout"] = f"{type(e).__name__}: {str(e)[:300]}"
            print(f"  {vid:24} {naam:11} {'fout' if 'fout' in rij else _teken(rij)}")
            rijen.append(rij)
            time.sleep(1)
    datum = datetime.date.today().isoformat()
    os.makedirs(METINGEN, exist_ok=True)
    pad = os.path.join(METINGEN, f"{datum}.json")
    json.dump({"datum": datum, "rijen": rijen}, open(pad, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("Meting opgeslagen:", os.path.relpath(pad))
    return pad


# ---------------------------------------------------------------- toegang
# Een assistent kan alleen citeren wat zijn crawler mag én kan ophalen.
# robots.txt komt uit build.py, maar Cloudflare kan er op de live site regels
# bij zetten (beheerde robots.txt) of AI-crawlers aan de rand weigeren; dat
# zie je alleen aan de live site. Deze controle kijkt daarom live.
SITE = "https://" + DOEL_DOMEIN
# (robots-token, voor wie, telt mee voor citaties in antwoorden)
AI_CRAWLERS = [
    ("OAI-SearchBot", "ChatGPT zoeken", True),
    ("ChatGPT-User", "ChatGPT opent een pagina", True),
    ("PerplexityBot", "Perplexity zoeken", True),
    ("Perplexity-User", "Perplexity opent een pagina", True),
    ("Claude-SearchBot", "Claude zoeken", True),
    ("Claude-User", "Claude opent een pagina", True),
    ("Googlebot", "Google, AI Overviews en Gemini", True),
    ("Bingbot", "Bing, Copilot en deels ChatGPT", True),
    ("Applebot", "Apple / Siri", True),
    ("DuckAssistBot", "DuckDuckGo AI-antwoorden", True),
    ("MistralAI-User", "Mistral opent een pagina", True),
    ("Google-Extended", "Gemini-training (geen zoekverkeer)", False),
    ("GPTBot", "OpenAI-training (geen zoekverkeer)", False),
    ("ClaudeBot", "Anthropic-training (geen zoekverkeer)", False),
]
TOEGANG_PADEN = ["/", "/vuurwerk-alternatief/", "/llms.txt"]
TOEGANG = os.path.join(MAP, "toegang.json")

def _haal(url, ua="Mozilla/5.0 (compatible; vuurspuwer-zichtbaarheidsmeter)"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers), r.read(200000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read(20000).decode("utf-8", "replace")

def beoordeel_robots(tekst):
    """Per crawler: mag hij de controlepaden ophalen volgens deze robots.txt?"""
    import urllib.robotparser
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(tekst.splitlines())
    return {tok: all(rp.can_fetch(tok, SITE + p) for p in TOEGANG_PADEN)
            for tok, _, _ in AI_CRAWLERS}

def _geweigerd(status, kop, lijf):
    kop = {k.lower(): v for k, v in kop.items()}
    # 402: Cloudflare pay per crawl
    return (status in (401, 402, 403, 429, 503) or kop.get("cf-mitigated") == "challenge"
            or "Just a moment..." in lijf[:5000])

def toegang():
    uit = {"datum": datetime.date.today().isoformat(), "waarschuwingen": []}
    w = uit["waarschuwingen"]
    status, _, robots = _haal(SITE + "/robots.txt")
    uit["robots_status"] = status
    if status != 200:
        w.append(f"robots.txt geeft HTTP {status}")
        robots = ""
    # Cloudflare zet zijn blok vóór de eigen robots.txt: "# BEGIN Cloudflare
    # Managed content" met Content-signal en Disallow-regels voor trainingsbots
    uit["robots_cloudflare"] = "Cloudflare Managed" in robots or "content-signal" in robots.lower()
    if uit["robots_cloudflare"]:
        w.append("Cloudflare voegt eigen regels toe aan robots.txt (beheerde robots.txt); "
                 "trainingsbots uitsluiten is prima, zoek- en antwoordcrawlers niet")
    uit["robots"] = beoordeel_robots(robots) if robots else {}
    for tok, voor, zoek in AI_CRAWLERS:
        if robots and not uit["robots"][tok] and zoek:
            w.append(f"robots.txt sluit {tok} uit ({voor})")
    # Met de user-agent van de crawler: weigert de rand (Cloudflare) hem?
    # Alleen een weigering zegt iets: de echte crawlers komen van hun eigen
    # IP-adressen, dus 'doorgelaten' hier is geen garantie voor hen.
    uit["rand"] = {}
    for tok, voor, zoek in AI_CRAWLERS:
        if tok == "Google-Extended":
            continue   # alleen een robots-token, geen eigen crawler
        ua = f"Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; {tok}/1.0)"
        try:
            st, kop, lijf = _haal(SITE + "/", ua)
            uit["rand"][tok] = {"status": st, "geweigerd": _geweigerd(st, kop, lijf)}
        except Exception as e:
            uit["rand"][tok] = {"status": None, "geweigerd": None, "fout": f"{type(e).__name__}: {e}"[:200]}
        if uit["rand"][tok]["geweigerd"] and zoek:
            w.append(f"de site weigert {tok} ({voor}) met HTTP {uit['rand'][tok]['status']}")
        time.sleep(0.5)
    for pad, soort in [("/llms.txt", "text/plain"), ("/llms-full.txt", "text/plain"),
                       ("/sitemap.xml", "xml")]:
        try:
            st, kop, _ = _haal(SITE + pad)
            ct = {k.lower(): v for k, v in kop.items()}.get("content-type", "")
        except Exception as e:
            st, ct = None, f"{type(e).__name__}"
        uit.setdefault("bestanden", {})[pad] = {"status": st, "type": ct}
        if st != 200 or soort not in ct:
            w.append(f"{pad} geeft HTTP {st} ({ct or 'geen type'})")
    os.makedirs(MAP, exist_ok=True)
    json.dump(uit, open(TOEGANG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Toegang:", "in orde" if not w else "")
    for x in w:
        print("  ⚠", x)
    return uit


# ---------------------------------------------------------------- rapport
def _teken(x):
    if not x or "fout" in x: return "–"
    return "★" if x["geciteerd"] else "✓" if x["genoemd"] else "○" if x.get("gelezen") else "·"

def rapport():
    bestanden = sorted(f for f in os.listdir(METINGEN) if f.endswith(".json")) if os.path.isdir(METINGEN) else []
    metingen = [json.load(open(os.path.join(METINGEN, f), encoding="utf-8")) for f in bestanden]
    r = ["# AI-zichtbaarheid van vuurspuwer.com", "",
         "Gemaakt door `tools/ai_zichtbaarheid.py`. Per vraag: ★ = vuurspuwer.com geciteerd als bron, "
         "✓ = Nuno genoemd zonder bronvermelding, ○ = een pagina van vuurspuwer.com is wel "
         "opgehaald maar niet aangehaald (de eerste stap), · = niet genoemd, – = niet gemeten of fout.", ""]
    if os.path.exists(TOEGANG):
        t = json.load(open(TOEGANG, encoding="utf-8"))
        r += [f"## Kunnen AI-crawlers de site lezen? (live gecontroleerd op {t['datum']})", ""]
        if t["waarschuwingen"]:
            r += [f"- ⚠ {x}" for x in t["waarschuwingen"]]
        else:
            r += ["Geen problemen gevonden: robots.txt laat alle zoek- en antwoordcrawlers toe, "
                  "de site weigert hun user-agent niet, en llms.txt, llms-full.txt en de sitemap zijn bereikbaar."]
        r += ["", "| crawler | voor | robots.txt | site |", "|---|---|---|---|"]
        for tok, voor, _ in AI_CRAWLERS:
            rb = t.get("robots", {}).get(tok)
            rd = t.get("rand", {}).get(tok)
            r.append(f"| {tok} | {voor} | {'–' if rb is None else 'toegestaan' if rb else 'uitgesloten'} | "
                     f"{'–' if not rd or rd.get('geweigerd') is None else 'geweigerd' if rd['geweigerd'] else 'doorgelaten'} |")
        r += ["", "*Site* test alleen de user-agent vanaf een GitHub-server; de echte crawlers "
              "komen van hun eigen adressen. Een weigering is dus een probleem, 'doorgelaten' "
              "is een goede aanwijzing maar geen garantie.", ""]
    if not metingen:
        r += ["Nog geen metingen. Zet minstens één API-sleutel als GitHub-geheim (zie de uitleg in "
              "`tools/ai_zichtbaarheid.py`) en start de Action *AI-zichtbaarheid*.", ""]
    else:
        r += ["## Verloop per aanbieder", "", "| datum | aanbieder | geciteerd | genoemd | opgehaald | metingen |",
              "|---|---|---|---|---|---|"]
        for m in metingen:
            per = collections.defaultdict(list)
            for x in m["rijen"]:
                if "fout" not in x: per[x["aanbieder"]].append(x)
            for a, xs in sorted(per.items()):
                n = len(xs)
                r.append(f"| {m['datum']} | {AANBIEDERS.get(a, ('', a))[1]} | "
                         f"{sum(x['geciteerd'] for x in xs)}/{n} | {sum(x['genoemd'] for x in xs)}/{n} | "
                         f"{sum(x.get('gelezen', False) or x['geciteerd'] for x in xs)}/{n} | {n} |")
        laatst = metingen[-1]
        aanb = sorted({x["aanbieder"] for x in laatst["rijen"]})
        idx = {(x["vraag"], x["aanbieder"]): x for x in laatst["rijen"]}
        r += ["", f"## Laatste meting ({laatst['datum']}) per vraag", "",
              "| vraag | " + " | ".join(AANBIEDERS.get(a, ('', a))[1] for a in aanb) + " |",
              "|---|" + "---|" * len(aanb)]
        for vid, taal, land, vraag in VRAGEN:
            cel = []
            for a in aanb:
                x = idx.get((vid, a))
                cel.append(_teken(x))
            r.append(f"| {vraag} ({land}) | " + " | ".join(cel) + " |")
        conc = collections.Counter(d for x in laatst["rijen"] if "fout" not in x for d in x.get("andere_domeinen", []))
        r += ["", "## Welke sites worden in plaats daarvan geciteerd", "",
              "Hier liggen de kansen: een vermelding op deze sites (een profiel, een recensie, een "
              "artikel) is wat AI-assistenten als bron gebruiken.", "",
              "| domein | aantal antwoorden |", "|---|---|"]
        r += [f"| {d} | {n} |" for d, n in conc.most_common(20)]
        fouten = [x for x in laatst["rijen"] if "fout" in x]
        if fouten:
            r += ["", "## Fouten in de laatste meting", ""]
            r += [f"- {x['aanbieder']} / {x['vraag']}: {x['fout'][:200]}" for x in fouten]
    open(os.path.join(MAP, "RAPPORT.md"), "w", encoding="utf-8").write("\n".join(r) + "\n")
    print("Rapport geschreven: ai-zichtbaarheid/RAPPORT.md")


# --------------------------------------------------------------- zelftest
def zelftest():
    """Controleert de verwerkers op antwoorden in de gedocumenteerde vorm."""
    fout = 0
    def eis(naam, uit, genoemd, geciteerd, anders=()):
        nonlocal fout
        b = beoordeel(uit)
        ok = (b["genoemd"] == genoemd and b["geciteerd"] == geciteerd
              and all(d in b["andere_domeinen"] for d in anders)
              and not any(d.endswith(DOEL_DOMEIN) for d in b["andere_domeinen"]))
        fout += not ok
        print(f"  {'ok  ' if ok else 'FOUT'} {naam}: {b}")
    eis("anthropic", ontleed_anthropic([
        {"type": "server_tool_use", "name": "web_search", "input": {"query": "vuurspuwer utrecht"}},
        {"type": "web_search_tool_result", "content": [
            {"type": "web_search_result", "url": "https://vuurspuwer.com/vuurspuwer-boeken-in-utrecht/", "title": "x"},
            {"type": "web_search_result", "url": "https://www.concurrent.nl/", "title": "y"}]},
        {"type": "text", "text": "Vuurspuwer Nuno uit Zeist ", "citations": [
            {"type": "web_search_result_location", "url": "https://vuurspuwer.com/over-nuno/", "title": "x", "cited_text": "..."}]},
        {"type": "text", "text": "of een ander bureau.", "citations": [
            {"type": "web_search_result_location", "url": "https://www.concurrent.nl/a", "title": "y", "cited_text": "..."}]},
    ]), True, True, ("concurrent.nl",))
    eis("anthropic-zoekfout", ontleed_anthropic([
        {"type": "web_search_tool_result", "content": {"type": "web_search_tool_result_error", "error_code": "max_uses_exceeded"}},
        {"type": "text", "text": "Ik vond geen artiesten."}]), False, False)
    eis("openai", ontleed_openai({"output": [
        {"type": "reasoning", "summary": []},
        {"type": "web_search_call", "status": "completed", "action": {"type": "search",
            "queries": ["vuurspuwer bruiloft"], "sources": [{"type": "url", "url": "https://vuurspuwer.com/vuurshow-bruiloft/"}]}},
        {"type": "message", "content": [{"type": "output_text", "text": "Je kunt Vuurspuwer Nuno boeken.",
            "annotations": [{"type": "url_citation", "url": "https://vuurspuwer.com/?utm_source=chatgpt.com", "title": "x"},
                            {"type": "url_citation", "url": "https://andere-artiest.be/", "title": "y"}]}]}]}),
        True, True, ("andere-artiest.be",))
    eis("gemini", ontleed_gemini({"candidates": [{"content": {"parts": [
            {"text": "Denk na over Nuno...", "thought": True},
            {"text": "Er zijn verschillende vuurspuwers."}]},
        "groundingMetadata": {"webSearchQueries": ["vuurspuwer aachen"], "groundingChunks": [
            {"web": {"uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AbC", "title": "vuurspuwer.com"}},
            {"web": {"uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/DeF", "title": "www.feuershow.de"}},
            {"web": {"uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/GhI", "title": "Een titel zonder domein"}}],
          "groundingSupports": [{"segment": {"startIndex": 0, "endIndex": 10}, "groundingChunkIndices": [0, 1]}]}}]}),
        False, True, ("feuershow.de",))
    g = ontleed_gemini({"candidates": [{"content": {"parts": [{"text": "x"}]},
        "groundingMetadata": {"groundingChunks": [
            {"web": {"uri": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/A", "title": "vuurspuwer.com"}}],
          "groundingSupports": []}}]})
    ok = not beoordeel(g)["geciteerd"] and beoordeel(g)["gelezen"]
    fout += not ok
    print(f"  {'ok  ' if ok else 'FOUT'} gemini-opgehaald-niet-geciteerd: {beoordeel(g)}")
    eis("perplexity", ontleed_perplexity({"status": "completed", "output": [
        {"type": "search_results", "queries": ["vuurspuwer"], "results": [
            {"id": 1, "url": "https://boekingsbureau.nl/vuur", "title": "z", "snippet": "..."}]},
        {"type": "message", "role": "assistant", "content": [
            {"type": "output_text", "text": "Probeer een lokaal bureau [1].", "annotations": []}]}]}),
        False, False, ("boekingsbureau.nl",))
    eis("perplexity-nuno", ontleed_perplexity({"status": "completed", "output": [
        {"type": "search_results", "results": [{"url": "https://www.vuurspuwer.com/vuurspuwer-inhuren-maastricht/"}]},
        {"type": "fetch_url_results", "contents": [{"url": "https://feuershow.de/x"}]},
        {"type": "message", "content": [{"type": "output_text", "text": "Vuurspuwer Nuno [web:1]."}]}]}),
        True, True)
    eis("niet-nuno", ontleed_perplexity({"output": [{"type": "message", "content": [
        {"type": "output_text", "text": "Nunes en Nunoz zijn bekend."}]}]}), False, False)
    rb = beoordeel_robots("User-agent: *\nAllow: /\n\nUser-agent: GPTBot\nDisallow: /\n"
                          "\nUser-agent: PerplexityBot\nDisallow: /llms.txt\n")
    ok = rb["OAI-SearchBot"] and not rb["GPTBot"] and not rb["PerplexityBot"] and rb["Claude-SearchBot"]
    fout += not ok
    print(f"  {'ok  ' if ok else 'FOUT'} robots: {rb}")
    eigen = open(os.path.join(HIER, "..", "dist", "robots.txt"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(HIER, "..", "dist", "robots.txt")) else None
    if eigen is not None:
        rb = beoordeel_robots(eigen)
        ok = all(rb.values())
        fout += not ok
        print(f"  {'ok  ' if ok else 'FOUT'} eigen robots.txt laat alle crawlers toe: {ok}")
    ok = _geweigerd(403, {}, "") and _geweigerd(402, {}, "") and _geweigerd(200, {"CF-Mitigated": "challenge"}, "") \
        and not _geweigerd(200, {}, "<html>")
    fout += not ok
    print(f"  {'ok  ' if ok else 'FOUT'} weigering herkennen")
    print("zelftest:", "in orde" if not fout else f"{fout} fout(en)")
    return fout


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rapport", action="store_true", help="alleen het rapport opnieuw maken")
    ap.add_argument("--zelftest", action="store_true", help="verwerking testen zonder API")
    ap.add_argument("--max", type=int, help="alleen de eerste N vragen")
    ap.add_argument("--aanbieders", help="komma-lijst, bv. anthropic,perplexity")
    ap.add_argument("--toegang", action="store_true", help="alleen live controleren of AI-crawlers erbij kunnen")
    a = ap.parse_args()
    if a.zelftest: sys.exit(1 if zelftest() else 0)
    if a.toegang:
        toegang(); rapport(); sys.exit(0)
    if not a.rapport:
        meet(a.max, set(a.aanbieders.split(",")) if a.aanbieders else None)
    rapport()
