#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google Search Console-koppeling voor vuurspuwer.com.

WAT DIT WEL DOET
  • sitemap.xml officieel (her)indienen via de Search Console API — de
    geauthenticeerde opvolger van de ping die Google in 2023 schrapte.
  • Per pagina bij Google OPVRAGEN of hij geïndexeerd is, wanneer hij voor
    het laatst gecrawld is, welke URL Google als canoniek ziet en welke rich
    results hij herkent. Read-only.
  • Daarvan een rapport schrijven (gsc-rapport.md) dat precies laat zien
    wélke pagina's nog niet in Google staan en waarom.

WAT DIT NIET DOET — en waarom niet
  Er bestaat GEEN publieke Google-API om indexering aan te vragen. De knop
  "Indexering aanvragen" in Search Console heeft geen tegenhanger: het
  endpoint index:requestIndexing bestaat niet (404), terwijl index:inspect
  wel bestaat (401 zonder token). De Indexing API die het wél kan, is
  officieel uitsluitend voor vacatures (JobPosting) en livestreams
  (BroadcastEvent); deze site heeft geen van beide, en misbruik kost je de
  API-toegang. Dit script is dus een MEETLAT, geen motor: het vertelt je of
  je werk vrucht draagt en waar het vastloopt.

EENMALIGE INSTELLING (±20 minuten, zie ook de uitleg onderaan)
  1. Google Cloud Console → nieuw project.
  2. Search Console API aanzetten (NIET de Indexing API).
  3. Service-account maken, JSON-sleutel downloaden.
  4. Search Console → Instellingen → Gebruikers → het service-accountadres
     toevoegen met machtiging "Volledig" (bewust géén Eigenaar).
  5. De JSON als GitHub-secret GOOGLE_SA_JSON plakken.

GEBRUIK
  python3 tools/gsc.py --check              controleer toegang (doe dit eerst)
  python3 tools/gsc.py --sitemap            sitemap opnieuw indienen
  python3 tools/gsc.py --inspect [aantal]   pagina's opvragen (standaard 30)
  python3 tools/gsc.py --rapport            alleen het rapport herschrijven
"""
import base64, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date

SITE = "https://vuurspuwer.com"
PROPERTY = "sc-domain:vuurspuwer.com"
STATUS_FILE = "gsc-status.json"          # bewust NIET indexing-state.json:
RAPPORT_FILE = "gsc-rapport.md"          # dat bestand is de IndexNow-rotatieklok
TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://searchconsole.googleapis.com"
SCOPE = "https://www.googleapis.com/auth/webmasters"
PER_RONDE = 30          # ruim onder het dagquotum van 2000 per property

# --------------------------------------------------------------- auth
def _b64(raw):
    return base64.urlsafe_b64encode(raw).rstrip(b"=")

def _teken_rs256(bericht, private_key_pem):
    """RS256 met cryptography; valt terug op de openssl-opdracht."""
    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        sleutel = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
        return sleutel.sign(bericht, padding.PKCS1v15(), hashes.SHA256())
    except ImportError:
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f:
            f.write(private_key_pem); pad = f.name
        try:
            return subprocess.run(["openssl", "dgst", "-sha256", "-sign", pad],
                                  input=bericht, capture_output=True, check=True).stdout
        finally:
            os.unlink(pad)

def access_token():
    ruw = os.environ.get("GOOGLE_SA_JSON", "").strip()
    if not ruw:
        return None
    if not ruw.lstrip().startswith("{"):          # ook base64 toegestaan
        ruw = base64.b64decode(ruw).decode()
    sa = json.loads(ruw)
    nu = int(time.time())
    kop = _b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    lijf = _b64(json.dumps({"iss": sa["client_email"], "scope": SCOPE,
                            "aud": TOKEN_URL, "iat": nu, "exp": nu + 3600}).encode())
    hand = _teken_rs256(kop + b"." + lijf, sa["private_key"])
    jwt = kop + b"." + lijf + b"." + _b64(hand)
    data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt.decode()}).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["access_token"]

def api(pad, token, methode="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + pad, data=data, method=methode,
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            tekst = r.read().decode("utf-8", "replace")
            return r.status, (json.loads(tekst) if tekst.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, {"fout": e.read().decode("utf-8", "replace")[:400]}

# ------------------------------------------------------------- stappen
def controleer(token):
    st, body = api("/webmasters/v3/sites", token)
    print(f"── Toegang controleren  (HTTP {st})")
    if st != 200:
        print("   ✗", json.dumps(body)[:400])
        print("\n   Veelvoorkomend:")
        print("   403 accessNotConfigured → Search Console API staat niet aan in je project")
        print("   403 permissionDenied    → service-account nog niet als gebruiker in")
        print("                             Search Console toegevoegd (machtiging: Volledig)")
        return False
    namen = [s["siteUrl"] for s in body.get("siteEntry", [])]
    print(f"   ✓ toegang tot {len(namen)} property('s): {', '.join(namen) or '(geen)'}")
    if PROPERTY not in namen:
        print(f"   ⚠ {PROPERTY} zit er niet bij — gebruik exact een naam uit deze lijst")
        return False
    return True

def dien_sitemap_in(token):
    pad = (f"/webmasters/v3/sites/{urllib.parse.quote(PROPERTY, safe='')}"
           f"/sitemaps/{urllib.parse.quote(SITE + '/sitemap.xml', safe='')}")
    st, body = api(pad, token, methode="PUT")
    ok = st in (200, 204)
    print(f"── Sitemap indienen  (HTTP {st}) {'✓' if ok else '✗ ' + json.dumps(body)[:200]}")
    return ok

def inspecteer(token, urls):
    """Vraagt per adres Google's eigen indexeerstatus op."""
    uit = {}
    for i, u in enumerate(urls, 1):
        st, body = api("/v1/urlInspection/index:inspect", token, "POST",
                       {"inspectionUrl": u, "siteUrl": PROPERTY, "languageCode": "nl"})
        if st != 200:
            print(f"   {i:3}. {st} {u}  {json.dumps(body)[:120]}")
            if st in (403, 401):
                print("        → gestopt: dit is een toegangsprobleem, geen quotum")
                break
            if st == 429:
                print("        → quotum bereikt, morgen verder")
                break
            continue
        r = (body.get("inspectionResult") or {}).get("indexStatusResult") or {}
        uit[u] = {"verdict": r.get("verdict", "?"),
                  "dekking": r.get("coverageState", ""),
                  "gecrawld": (r.get("lastCrawlTime") or "")[:10],
                  "canoniek": r.get("googleCanonical", ""),
                  "verwijzers": len(r.get("referringUrls") or []),
                  "op": date.today().isoformat()}
        v = uit[u]
        print(f"   {i:3}. {v['verdict']:5} {v['dekking'][:38]:38} {u.replace(SITE,'') or '/'}")
    return uit

# ------------------------------------------------------------- rapport
def schrijf_rapport(status, totaal):
    gezien = status.get("paginas", {})
    per = {}
    for u, v in gezien.items():
        per.setdefault(v.get("dekking") or v.get("verdict") or "onbekend", []).append(u)
    geindexeerd = [u for u, v in gezien.items() if v.get("verdict") == "PASS"]
    r = [f"# Google-indexstatus — {date.today().isoformat()}", "",
         f"Opgevraagd: **{len(gezien)} van {totaal}** adressen uit de sitemap.",
         f"Daarvan staat Google-oordeel PASS op **{len(geindexeerd)}**.", "",
         "> Dit rapport is een meting, geen actie. Google kent geen API om",
         "> indexering aan te vragen; wat hier rood staat, los je op met betere",
         "> interne links, sterkere inhoud of het opruimen van omleidingen.", "",
         "## Naar status", "", "| Status | Aantal |", "|---|---|"]
    for k, v in sorted(per.items(), key=lambda t: -len(t[1])):
        r.append(f"| {k} | {len(v)} |")
    niet = [u for u, v in gezien.items() if v.get("verdict") != "PASS"]
    if niet:
        r += ["", f"## Nog niet geïndexeerd ({len(niet)})", "",
              "| Pagina | Status | Laatst gecrawld | Interne verwijzers |", "|---|---|---|---|"]
        for u in sorted(niet):
            v = gezien[u]
            r.append(f"| `{u.replace(SITE,'') or '/'}` | {v.get('dekking','')} | "
                     f"{v.get('gecrawld') or '—'} | {v.get('verwijzers', 0)} |")
    r += ["", f"_Laatste ronde: {status.get('laatste_ronde','—')}_", ""]
    open(RAPPORT_FILE, "w", encoding="utf-8").write("\n".join(r))

# ---------------------------------------------------------------- main
def lees_status():
    try:
        return json.load(open(STATUS_FILE, encoding="utf-8"))
    except Exception:
        return {"paginas": {}, "laatste_ronde": ""}

def sitemap_urls():
    import re
    pad = "dist/sitemap.xml"
    if not os.path.exists(pad):
        sys.exit("✗ dist/sitemap.xml ontbreekt — draai eerst: python3 build.py")
    return re.findall(r"<loc>(.*?)</loc>", open(pad, encoding="utf-8").read())

def main():
    argv = sys.argv[1:] or ["--check"]
    urls = sitemap_urls()
    status = lees_status()

    if "--rapport" in argv:
        schrijf_rapport(status, len(urls))
        print(f"✓ {RAPPORT_FILE} herschreven"); return

    token = access_token()
    if not token:
        print("GOOGLE_SA_JSON is niet ingesteld — Google-koppeling overgeslagen.")
        print("Zie de uitleg boven in dit bestand voor de eenmalige instelling.")
        return                      # géén foutcode: de rest van de dag draait door

    if not controleer(token):
        sys.exit(1)
    if "--check" in argv:
        return

    if "--sitemap" in argv:
        dien_sitemap_in(token)

    if "--inspect" in argv:
        n = PER_RONDE
        i = argv.index("--inspect")
        if i + 1 < len(argv) and argv[i + 1].isdigit():
            n = int(argv[i + 1])
        # eerst wat we nog nooit opvroegen, daarna wat het langst geleden is
        gezien = status.get("paginas", {})
        beurt = sorted(urls, key=lambda u: (gezien.get(u, {}).get("op", ""), u))[:n]
        print(f"── {len(beurt)} van {len(urls)} adressen opvragen bij Google")
        nieuw = inspecteer(token, beurt)
        status.setdefault("paginas", {}).update(nieuw)
        status["laatste_ronde"] = date.today().isoformat()
        json.dump(status, open(STATUS_FILE, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=0, sort_keys=True)
        schrijf_rapport(status, len(urls))
        pass_n = sum(1 for v in status["paginas"].values() if v.get("verdict") == "PASS")
        print(f"\n✓ {len(status['paginas'])}/{len(urls)} adressen gemeten, "
              f"{pass_n} met oordeel PASS — zie {RAPPORT_FILE}")

if __name__ == "__main__":
    main()
