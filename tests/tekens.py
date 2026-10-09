#!/usr/bin/env python3
"""Vreemde tekens in de gebouwde site.

Aanleiding: bij een herschrijving in oktober 2026 slopen twee Cyrillische
letters in het woord 'hindoeïstisch'. Voor een lezer lijkt dat een typefout;
voor een zoekmachine is het een ander woord. Deze test laat de bouw omvallen
zodra er in dist een letter uit een schrift staat dat de site niet gebruikt
(Cyrillisch, Grieks, Hebreeuws, Arabisch buiten het ene citaat op de
fakir-pagina, Devanagari, CJK). HTML-entities voor letters (&euml;) zijn op deze site een
bewuste keuze en tellen niet als fout.
"""
import os, re, sys
DIST = os.path.join(os.path.dirname(__file__), "..", "dist")
VREEMD = re.compile(r"[Ͱ-ϿЀ-ӿ֐-׿ऀ-ॿ぀-ヿ一-鿿]")
# het Arabische woord faqīr op de fakir-pagina is bewust
TOEGESTAAN = {"betekenis-en-geschiedenis-van-fakir": re.compile(r"[؀-ۿ]")}
fouten = 0
for root, _, files in os.walk(DIST):
    for f in files:
        if not f.endswith((".html", ".txt", ".xml", ".json")): continue
        p = os.path.join(root, f)
        try: s = open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            print(f"  ✖ geen geldige UTF-8: {p}"); fouten += 1; continue
        slug = os.path.relpath(root, DIST).replace(os.sep, "/")
        for m in VREEMD.finditer(s):
            ctx = s[max(0, m.start()-30):m.end()+30].replace("\n", " ")
            print(f"  ✖ {slug}: vreemd teken U+{ord(m.group(0)):04X} in …{ctx}…"); fouten += 1; break
        # llms-full.txt neemt de fakir-pagina in platte tekst over, dus ook het woord
        if slug not in TOEGESTAAN and not (slug == "." and f == "llms-full.txt"):
            m = re.search(r"[؀-ۿ]", s)
            if m:
                print(f"  ✖ {slug}: Arabisch schrift buiten de fakir-pagina"); fouten += 1
print(f"tekens: {'in orde' if not fouten else str(fouten) + ' fout(en)'}")
sys.exit(1 if fouten else 0)
