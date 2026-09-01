# -*- coding: utf-8 -*-
"""Gelegenheid-pagina's: bruiloft, bedrijfsfeest, verjaardag, festival,
vrijgezellenfeest, plus de decembermachine (vuurwerk-alternatief en
kerst/nieuwjaar). Nederlands hier; en/de/fr in occasions_i18n."""

SLUGS = {
    "vuurshow-bruiloft":       {"en": "fire-show-wedding",        "de": "feuershow-hochzeit",       "fr": "spectacle-de-feu-mariage"},
    "vuurshow-bedrijfsfeest":  {"en": "fire-show-corporate-event","de": "feuershow-firmenfeier",    "fr": "spectacle-de-feu-entreprise"},
    "vuurshow-verjaardag":     {"en": "fire-show-birthday",       "de": "feuershow-geburtstag",     "fr": "spectacle-de-feu-anniversaire"},
    "vuurshow-festival":       {"en": "fire-show-festival",       "de": "feuershow-festival",       "fr": "spectacle-de-feu-festival"},
    "vrijgezellenfeest":       {"en": "bachelor-party-activity",  "de": "junggesellenabschied",     "fr": "evjf-evg-activite"},
    "vuurwerk-alternatief":    {"en": "fireworks-alternative",    "de": "feuerwerk-alternative",    "fr": "alternative-feu-artifice"},
    "kerst-nieuwjaar-entertainment": {"en": "christmas-new-year-entertainment", "de": "weihnachtsfeier-silvester-show", "fr": "spectacle-noel-nouvel-an"},
}

_OFFER = lambda lo, hi, n, desc: {"@type": "AggregateOffer", "priceCurrency": "EUR",
                                  "lowPrice": lo, "highPrice": hi, "offerCount": n,
                                  "description": desc}

NL = {

"vuurshow-bruiloft": {
 "title": "Vuurshow op je bruiloft",
 "seo_title": "\U0001F49B Vuurshow Bruiloft | Romantisch Alternatief voor Vuurwerk — vanaf €450",
 "seo_desc": "Vuurshow op je bruiloft? Een romantische show van 20 minuten bij de eerste dans of avondopening — vaak wél toegestaan waar vuurwerk verboden is. 4,9/5 uit 136 reviews. Vanaf €450.",
 "eyebrow": "Bruiloften",
 "img": ("/assets/media/bruiloft-1080.webp", "Duo-vuuract op een bruiloft: Nuno met een danseres met grote rode vleugels"),
 "body": """
<p><strong>Een vuurshow op je bruiloft is hét moment waar gasten nog jaren over praten: metershoge vlammen bij de eerste dans, een vonkenregen bij het aansnijden van de taart of een spectaculaire opening van het avondfeest. En het mooiste: een vuurshow is vaak wél toegestaan op plekken waar vuurwerk verboden is.</strong></p>

<h2>Waarom een vuurshow perfect past bij een bruiloft</h2>
<p>Vuurwerk op een trouwlocatie is in Nederland en België bijna nergens meer toegestaan: vergunningen, buren, natuurgebieden. Een professionele vuurshow geeft hetzelfde wauw-moment — maar dan dichtbij, persoonlijk en op muziek die bij jullie past. Nuno stemt de choreografie af op jullie openingsdans of favoriete nummer, en overlegt vooraf met de locatie over de veiligheid, zodat jullie nergens omkijken naar hebben.</p>

<h2>Zo ziet het eruit op jullie dag</h2>
<ul>
<li><strong>De avondopening</strong> — gasten komen buiten, het licht dimt, en Nuno opent het feest met een showblok van 20 minuten vol vuurspuwen, vuurjongleren en body fire.</li>
<li><strong>Bij de eerste dans</strong> — vlammen en vonken omlijsten jullie openingsdans; samen met de <a href="/fotos/">fotograaf</a> levert dit de mooiste trouwfoto's op.</li>
<li><strong>Duo met danseres</strong> — voor extra romantiek en theater: Nuno samen met een vuurdanseres met vleugels, zoals op de foto hierboven.</li>
<li><strong>Binnen of slecht weer?</strong> — dan schakelt Nuno naar <a href="/entertainer-huren/">mentalisme</a> of de <a href="/fakir-show-inhuren/">fakirshow</a>: net zo onvergetelijk, zonder open vuur.</li>
</ul>

<h2>Wat kost een vuurshow op een bruiloft?</h2>
<p>Het populairste pakket voor bruiloften is het showblok van 20 minuten <strong>vanaf €450</strong>; een korte power-act van 10 minuten kan al <strong>vanaf €350</strong>. Alles is inbegrepen: materiaal, veilige showbrandstoffen, op- en afbouw en afstemming met de locatie. Bekijk het volledige <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a> of vraag direct een <a href="/contact-3/">offerte met jullie trouwdatum</a> aan — binnen 24 uur antwoord.</p>

<h2>Praktisch geregeld, zonder stress</h2>
<p>Nuno werkt volledig gecertificeerd, binnen de vergunningseisen van de locatie en met de voorgeschreven veiligheidsafstanden — hij stemt dit vóór jullie dag rechtstreeks met de trouwlocatie af. Met <a href="/over-nuno/">17 jaar ervaring</a> op bruiloften, festivals en tv weet hij precies hoe hij een dagplanning niet verstoort maar verrijkt. Van kasteeltuin tot strandpaviljoen: hij speelt door heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a> — bekijk bijvoorbeeld <a href="/vuurspuwer-boeken-in-amsterdam/">Amsterdam</a>, <a href="/vuurspuwer-boeken-in-utrecht-2/">Utrecht</a> of <a href="/locaties-vuurshows-nederland-belgie/">België</a>.</p>
""",
 "faq": [
  ("Wat kost een vuurshow op een bruiloft?",
   "Het showblok van 20 minuten — het populairste bruiloftspakket — kost vanaf €450, exclusief reiskosten. Een korte power-act van 10 minuten kan vanaf €350. Je ontvangt altijd één all-in offerte."),
  ("Mag een vuurshow op onze trouwlocatie, ook waar vuurwerk verboden is?",
   "Meestal wel: een vuurshow valt onder andere regels dan vuurwerk. Nuno werkt binnen de vergunningseisen van de locatie en stemt de veiligheidsafstanden vooraf rechtstreeks met de locatie af."),
  ("Kan de show tijdens de eerste dans?",
   "Ja, dat is zelfs een van de mooiste momenten: de choreografie wordt afgestemd op jullie openingsnummer, in overleg met de dj of band."),
  ("Wat als het regent of de show binnen moet?",
   "Buiten kan een vuurshow ook bij lichte regen. Moet het binnen en staat de locatie geen open vuur toe, dan schakelt Nuno naar mentalisme of de fakirshow — het spektakel blijft."),
  ("Hoe ver van tevoren moeten we boeken?",
   "Trouwseizoen (mei–september) en zaterdagen lopen het eerst vol. Boek bij voorkeur drie tot zes maanden vooruit; check je datum vrijblijvend via het formulier of WhatsApp."),
 ],
 "service": {"name": "Vuurshow op een bruiloft", "type": "Vuurshow",
   "desc": "Romantische vuurshow voor bruiloften: avondopening of eerste dans, solo of duo met danseres, 10–30 minuten. Vaak wél toegestaan waar vuurwerk verboden is. Vanaf €450.",
   "offers": _OFFER("350", "750", "3", "Power-act 10 min vanaf €350, showblok 20 min vanaf €450, duo-show met danseres vanaf €700.")},
 "fotos": [("bruiloft-900.webp", "bruiloft-1080.webp", 900, 1014, "Duo-act met danseres op een bruiloft", "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Vuurbal in de avondschemering", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
           ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Vuur in de avond", "Vuurspuwer bij een vintage bus tijdens een avondfeest")],
},

"vuurshow-bedrijfsfeest": {
 "title": "Vuurshow op je bedrijfsfeest",
 "seo_title": "\U0001F525 Vuurshow Bedrijfsfeest | Entertainment met Wow-factor — vanaf €450",
 "seo_desc": "Entertainment voor je bedrijfsfeest? Een professionele vuurshow als opening of grande finale maakt indruk op personeel én klanten. Bekend van SBS6, RTL en Walibi. Vanaf €450, offerte binnen 24 uur.",
 "eyebrow": "Bedrijfsfeesten",
 "img": ("/assets/media/themafeest-1080.webp", "Vuurspuwer Nuno bij een vintage bus tijdens een bedrijfsfeest in de avond"),
 "body": """
<p><strong>Een bedrijfsfeest dat het gesprek van de maandagochtend wordt? Een professionele vuurshow als opening of grande finale geeft je personeelsfeest, klantenevent of jubileum precies dat wauw-moment dat blijft hangen — strak, veilig en representatief.</strong></p>

<h2>Waarom eventmanagers voor Nuno kiezen</h2>
<p>Bij een zakelijk evenement telt niet alleen spektakel, maar ook uitstraling en betrouwbaarheid. Nuno komt met strak kostuum, professionele communicatie vooraf en een show die exact in het programma past — 10, 20 of 30 minuten, op de minuut. Met optredens voor <a href="/over-nuno/">SBS6, RTL, VTM en de Walibi Fright Nights</a> en een <a href="/beoordelingen/">4,9 uit 136 beoordelingen</a> weet je wat je in huis haalt.</p>

<h2>Formats die werken op zakelijke events</h2>
<ul>
<li><strong>De opening</strong> — een power-act van 10 minuten die het energieniveau direct op honderd zet (vanaf €350).</li>
<li><strong>De grande finale</strong> — een volledig showblok van 20 minuten als afsluiter, vlak voor de dj of band (vanaf €450).</li>
<li><strong>Teambuilding: workshop vuurspuwen</strong> — het team leert onder professionele begeleiding zelf vuurspuwen; dé <a href="/workshop-vuurspuwen/">teamactiviteit</a> waar nog jaren over gepraat wordt.</li>
<li><strong>Themafeest-totaalpakket</strong> — van 1001 Nacht tot Caribbean: <a href="/entertainer-huren-voor-bedrijfsfeest/">compleet thema-entertainment</a> met vuur als middelpunt.</li>
<li><strong>Binnen-locatie?</strong> — <a href="/entertainer-huren/">mentalisme</a> of de <a href="/fakir-show-inhuren/">fakirshow</a> brengen het spektakel zonder open vuur.</li>
</ul>

<h2>Van Zuidas tot industrieel erfgoed</h2>
<p>Industriële loodsen, kantoortuinen, parkeerdaken, strandclubs: bijna elke zakelijke locatie leent zich voor vuur — Nuno beoordeelt dit vooraf en regelt de afstemming met de locatie over vergunningseisen en veiligheidsafstanden. Hij speelt door heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>: van <a href="/vuurspuwer-boeken-in-amsterdam/">Amsterdam</a> en <a href="/vuurspuwer-boeken-in-rotterdam/">Rotterdam</a> tot <a href="/vuurspuwer-boeken-in-eindhoven/">Eindhoven</a> en <a href="/vuurspuwer-boeken-in-antwerpen/">Antwerpen</a>.</p>

<h2>Budget en offerte</h2>
<p>Shows kosten tussen de €350 en €1500, afhankelijk van duur en programma — zie het <a href="/wat-kost-een-vuurspuwer/">complete prijzenoverzicht</a>. Facturatie gaat netjes op rekening met duidelijke btw-specificatie (KvK 98164325). Stuur je datum en locatie via het <a href="/contact-3/">aanvraagformulier</a>: binnen 24 uur ligt er een offerte. December-feest? Bekijk dan ook het <a href="/kerst-nieuwjaar-entertainment/">kerst- en nieuwjaarsaanbod</a> en boek vroeg.</p>
""",
 "faq": [
  ("Wat kost een vuurshow op een bedrijfsfeest?",
   "Een openings-act van 10 minuten vanaf €350, een volledig showblok van 20 minuten vanaf €450 en een complete avondprogrammering tot €1500. Altijd één all-in offerte, netjes op factuur."),
  ("Is een vuurshow representatief genoeg voor klanten en directie?",
   "Ja — strakke kostuums, professionele communicatie en een gechoreografeerde show op muziek. Nuno stond op tv bij SBS6, RTL en VTM en werkt voor merken en events in heel de Benelux."),
  ("Kan het ook op een binnenlocatie of kantoorterrein?",
   "Buiten vrijwel altijd, ook op parkeerterreinen en daktuinen; binnen zodra de locatie en brandweer het toelaten. Anders schakelt Nuno naar mentalisme of de fakirshow zonder open vuur."),
  ("Hoe zit het met veiligheid en verzekering van gasten?",
   "Nuno is volledig gecertificeerd, gebruikt professionele showbrandstoffen en houdt de voorgeschreven veiligheidsafstanden aan; alles wordt vooraf met de locatie afgestemd."),
  ("Kunnen we show en workshop combineren?",
   "Zeker — populair op personeelsfeesten: eerst de show als spektakel, daarna leert een groep collega's onder begeleiding zelf vuurspuwen. Vraag naar het combitarief."),
 ],
 "service": {"name": "Vuurshow op een bedrijfsfeest", "type": "Vuurshow",
   "desc": "Professionele vuurshow voor bedrijfsfeesten, personeelsfeesten en klantevents: opening, grande finale of teambuilding-workshop. Bekend van tv. Vanaf €450, op factuur.",
   "offers": _OFFER("350", "1500", "4", "Opening 10 min vanaf €350, showblok 20 min vanaf €450, volledige show vanaf €595, avondprogramma tot €1500.")},
 "fotos": [("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Vuur op een bedrijfsfeest", "Vuurspuwer bij een vintage bus tijdens een bedrijfsfeest in de avond"),
           ("festival-900.webp", "festival-1600.webp", 900, 902, "Vuurshow voor groot publiek", "Vuurspuwer Nuno spuwt een vuurbal voor een groot publiek"),
           ("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Workshop vuurspuwen als teambuilding", "Vuurspuwer blaast een grote vuurbal tegen de avondlucht")],
},

"vuurshow-verjaardag": {
 "title": "Vuurshow op een verjaardag of jubileum",
 "seo_title": "\U0001F389 Vuurshow Verjaardag & Jubileum | Spektakel in je Eigen Tuin — vanaf €350",
 "seo_desc": "Een verjaardag, Abraham/Sarah of jubileum onvergetelijk maken? Boek een vuurshow aan huis: 10 tot 20 minuten spektakel in de tuin of op de oprit. Vanaf €350, heel NL & BE.",
 "eyebrow": "Verjaardagen & jubilea",
 "img": ("/assets/media/avondvuur-1080.webp", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
 "body": """
<p><strong>Voor de verjaardag van iemand die alles al heeft, een 50e met Abraham of Sarah in de tuin, of een huwelijksjubileum: een vuurshow aan huis is het cadeau dat niemand ziet aankomen — en niemand ooit vergeet.</strong></p>

<h2>Spektakel in je eigen tuin</h2>
<p>Voor een vuurshow is verrassend weinig ruimte nodig: een tuin, oprit of het grasveldje voor de deur is vaak al genoeg. Nuno beoordeelt de plek vooraf (een foto via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> volstaat meestal), neemt alles zelf mee en laat de plek netjes achter. De buren? Die staan gegarandeerd mee te kijken.</p>

<h2>Populaire formules</h2>
<ul>
<li><strong>De verrassingsact (10 min, vanaf €350)</strong> — de jarige weet van niets; ineens staat er een vuurspuwer in de tuin.</li>
<li><strong>Het feestblok (20 min, vanaf €450)</strong> — een volledige mini-show met vuurspuwen, vuurjongleren en interactie; perfect voor Abraham, Sarah en jubilea.</li>
<li><strong>Met fakir-elementen</strong> — durft de jarige op het <a href="/fakir-show-inhuren/">spijkerbed</a> te staan? Interactie waar iedereen bij wil zijn.</li>
<li><strong>Voor de durfals: mini-workshop</strong> — de gasten proberen het zelf onder begeleiding; kijk bij de <a href="/workshop-vuurspuwen/">workshop vuurspuwen</a>.</li>
</ul>

<h2>Wanneer en waar</h2>
<p>Een vuurshow komt het mooist uit in de schemering of het donker — in de zomer rond tien uur, in de winter al vanaf vijf uur. Nuno speelt door heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>; door de thuisbasis in Zeist zijn de reiskosten in het midden van het land het laagst. Bekijk <a href="/wat-kost-een-vuurspuwer/">alle prijzen</a> of <a href="/contact-3/">check direct je datum</a> — binnen 24 uur antwoord, vaak dezelfde dag.</p>

<h2>Ook leuk om te weten</h2>
<p>Kinderen kijken op veilige afstand hun ogen uit — en voor wie liever geen vuur wil: de <a href="/reptielenhow/">reptielenshow</a> met echte slangen of een <a href="/entertainer-huren/">mentalisme-act</a> in de woonkamer zijn net zulke sterke verrassingen. Lees de <a href="/beoordelingen/">ervaringen van jarigen en jubilarissen</a>: gemiddeld 4,9 uit 136 beoordelingen.</p>
""",
 "faq": [
  ("Wat kost een vuurshow op een verjaardag?",
   "De verrassingsact van 10 minuten kost vanaf €350, het volledige feestblok van 20 minuten vanaf €450 — exclusief reiskosten, altijd met één all-in offerte vooraf."),
  ("Hoeveel ruimte is er nodig in een tuin?",
   "Minder dan je denkt: een vrije cirkel van enkele meters zonder overhangende takken of parasols volstaat vaak al. Stuur een foto van de tuin via WhatsApp en je hoort direct of het kan."),
  ("Kan het ook als complete verrassing?",
   "Ja — dat is zelfs de populairste formule. Alles wordt vooraf stilletjes afgestemd met de organisator; de jarige ziet Nuno pas als de eerste vuurbal de lucht in gaat."),
  ("Is het veilig met kinderen en ouderen erbij?",
   "Ja. Nuno is volledig gecertificeerd, gebruikt veilige showbrandstoffen en zet vooraf een duidelijke veiligheidszone uit waar iedereen prima achter kan staan én alles kan zien."),
  ("Tot hoe laat kan een show in een woonwijk?",
   "Een vuurshow is relatief stil — geen knallen zoals vuurwerk — en kan daardoor prima 's avonds in een woonwijk. Nuno houdt rekening met de omgeving en adviseert over het beste tijdstip."),
 ],
 "service": {"name": "Vuurshow op een verjaardag of jubileum", "type": "Vuurshow",
   "desc": "Vuurshow aan huis voor verjaardagen, Abraham/Sarah en jubilea: verrassingsact van 10 minuten of feestblok van 20 minuten in de tuin. Vanaf €350, heel Nederland en België.",
   "offers": _OFFER("350", "750", "3", "Verrassingsact 10 min vanaf €350, feestblok 20 min vanaf €450, met fakir-interactie vanaf €595.")},
 "fotos": [("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Vuurbal in de schemering", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
           ("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal tijdens een avondshow", "Meters hoge vuurbal tegen een zwarte nachtlucht"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Fakir-interactie op een feest", "Close-up van de fakiract met het spijkerbord")],
},

"vuurshow-festival": {
 "title": "Vuurshow boeken voor je festival",
 "seo_title": "\U0001F3AA Vuurshow Festival Boeken | Tot 5 Sets per Dag — Walibi-ervaring",
 "seo_desc": "Vuuract voor je festival of evenement? Nuno speelt tot 5 sets van 20 minuten per dag, kent de festivalpraktijk van Walibi Fright Nights en Emporium en levert een strakke rider. €950–€1500 all-in.",
 "eyebrow": "Festivals & evenementen",
 "img": ("/assets/media/festival-1600.webp", "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek"),
 "body": """
<p><strong>Voor festivals en publieksevenementen is vuur de ultieme publiekstrekker: zichtbaar van ver, fotogeniek op elke telefoon en telkens weer een oploop. Nuno draait festivalprogramma's tot vijf sets van twintig minuten per dag — met de routine van Walibi Fright Nights en Emporium.</strong></p>

<h2>Gebouwd voor de festivalpraktijk</h2>
<p>Een festival vraagt iets anders dan een besloten feest: strakke settijden tussen de acts door, snelle op- en afbouw, veilig werken met publiek dat overal staat, en een act die óók overdag werkt. Nuno levert een duidelijke technische rider (benodigde ruimte, veiligheidszone, afstemming met de organisatie) en stemt de sets af op jullie blokkenschema — van festivalplein tot campingpodium.</p>

<h2>Het festivalpakket</h2>
<ul>
<li><strong>Tot 5 × 20 minuten per dag</strong> — verspreid over middag en avond, €950–€1500 all-in afhankelijk van het aantal sets.</li>
<li><strong>Roaming acts tussen het publiek</strong> — korte verrassingsmomenten op het terrein tussen de sets door.</li>
<li><strong>Combinatie met de <a href="/fakir-show-inhuren/">fakirshow</a></strong> — spijkerbed en glasscherven trekken overdag net zoveel publiek als vuur in het donker.</li>
<li><strong>Halloween- en themaproducties</strong> — voor oktober-events is er een compleet <a href="/halloween/">Halloween-programma</a>, bekend van de Fright Nights.</li>
<li><strong>Meerdaags of terugkerend</strong> — vaste act op je jaarlijkse festival? Vraag naar meerdaagse tarieven.</li>
</ul>

<h2>Bewezen op grote podia</h2>
<p>Van de <a href="/halloween/">Walibi Halloween Fright Nights</a> tot festival Emporium en optredens voor <a href="/over-nuno/">SBS6, RTL en VTM</a>: Nuno kent de dynamiek van grote producties — aanleveren wat de productieleiding nodig heeft, klaarstaan op de minuut en pieken als het publiek er staat. Bekijk de <a href="/videos/">showreels</a> en <a href="/fotos/">festivalfoto's</a>, of lees de <a href="/beoordelingen/">beoordelingen van organisatoren</a>.</p>

<h2>Boeken en beschikbaarheid</h2>
<p>Festivalzomer en oktober lopen ver vooruit vol. Stuur je data en het aantal gewenste sets via het <a href="/contact-3/">aanvraagformulier</a> — je ontvangt binnen 24 uur een offerte met rider. Alle pakketprijzen staan in het <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a>; Nuno speelt in heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>.</p>
""",
 "faq": [
  ("Wat kost een vuuract op een festival?",
   "Het festivalpakket met maximaal vijf sets van 20 minuten kost €950 tot €1500 all-in, afhankelijk van het aantal sets en de reisafstand. Eén set boeken kan vanaf €450."),
  ("Wat staat er in de technische rider?",
   "Een vrije speelcirkel met veiligheidszone, afstemming over de ondergrond en publieksbarrières waar nodig, en een afgesproken plek voor materiaal. Stroom en podium zijn niet vereist; muziekafstemming met de dj kan."),
  ("Werkt een vuurshow ook overdag?",
   "Ja — overdag zijn de vuurballen en de fakir-elementen (spijkerbed, glas) de publiekstrekkers; in de schemering en avond komt het volledige vuurspektakel erbij."),
  ("Hoe zit het met vergunningen op een evenemententerrein?",
   "Nuno werkt binnen de evenementenvergunning van de organisator en levert daarvoor op verzoek de benodigde gegevens over de act, brandstoffen en veiligheidsmaatregelen aan."),
  ("Kan Nuno meerdere dagen of jaarlijks terugkomen?",
   "Ja, meerdaagse festivals en jaarlijkse edities zijn juist ideaal; vraag naar de meerdaagse tarieven in de offerte."),
 ],
 "service": {"name": "Vuurshow op een festival", "type": "Vuurshow",
   "desc": "Festivalpakket: tot vijf vuursets van 20 minuten per dag, roaming acts en fakirshow-optie. Ervaring met Walibi Fright Nights en Emporium. €950–€1500 all-in.",
   "offers": _OFFER("450", "1500", "3", "Eén festivalset vanaf €450, dagpakket tot 5×20 min €950–€1500, meerdaags op aanvraag.")},
 "fotos": [("festival-900.webp", "festival-1600.webp", 900, 902, "Vuurshow op een festivalplein", "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Vuurshow bij daglicht", "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe"),
           ("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal in de nacht", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer")],
},

"vrijgezellenfeest": {
 "title": "Vrijgezellenfeest: workshop vuurspuwen",
 "seo_title": "\U0001F525 Vrijgezellenfeest Activiteit | Workshop Vuurspuwen — Origineler Bestaat Niet",
 "seo_desc": "Op zoek naar een originele vrijgezellenfeest-activiteit? Leer met de hele groep vuurspuwen onder professionele begeleiding. Inclusief foto's als bewijs. Vanaf €350, heel NL & BE.",
 "eyebrow": "Vrijgezellenfeesten",
 "img": ("/assets/media/workshop-1125.webp", "Workshop vuurspuwen: deelnemer blaast een grote vuurbal tegen de avondlucht"),
 "body": """
<p><strong>Nog een keer paintball of karten? Of geef je de bruidegom of bruid een verhaal dat op de bruiloft zelf verteld gaat worden: met de hele groep leren vuurspuwen, onder professionele begeleiding — mét foto's van ieders eerste vuurbal als bewijs.</strong></p>

<h2>Hoe de workshop werkt</h2>
<p>Eerst veiligheid: uitleg over de brandstoffen, de techniek en de bescherming. Dan oefenen zonder vuur, en wie er klaar voor is spuwt onder <a href="/over-nuno/">Nuno's</a> directe begeleiding zijn of haar eerste échte vuurbal. De workshop duurt één tot twee uur, past zich aan het lef van de groep aan en eindigt — uiteraard — met de vrijgezel die de grootste vuurbal van de dag neerzet. Iedereen gaat naar huis met spectaculaire foto's voor de groepsapp.</p>

<h2>Waarom dit hét vrijgezellenfeest is</h2>
<ul>
<li><strong>Origineler bestaat niet</strong> — niemand in de vriendengroep heeft dit al gedaan.</li>
<li><strong>Voor elke groep</strong> — van 4 tot 20 personen, mannen én vrouwen; wie niet durft, fotografeert.</li>
<li><strong>Overal in NL & BE</strong> — Nuno komt met alle materialen naar jullie stad of feestlocatie; alleen wat vrije buitenruimte is nodig. Bekijk bijvoorbeeld wat er mogelijk is in <a href="/vuurspuwer-boeken-in-amsterdam/">Amsterdam</a>, <a href="/vuurspuwer-boeken-in-rotterdam/">Rotterdam</a> of <a href="/vuurspuwer-boeken-in-antwerpen/">Antwerpen</a>.</li>
<li><strong>Combineer met een show</strong> — eerst kijken hoe het écht moet (<a href="/vuurspuwer-inhuren/">mini-vuurshow</a>), daarna zelf proberen.</li>
</ul>

<h2>Prijzen en boeken</h2>
<p>De workshop begint <strong>vanaf €350</strong> voor een groep, inclusief alle materialen, brandstoffen en begeleiding — bekijk het <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a> voor combi's met een show. Data in het weekend lopen snel vol: <a href="/contact-3/">check je datum</a> of stuur direct een appje via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>. Meer weten over de workshop zelf? Lees alles op de <a href="/workshop-vuurspuwen/">workshoppagina</a>.</p>

<h2>Veilig, ook na een biertje minder</h2>
<p>Duidelijke regel: vuurspuwen doe je nuchter — het drinken komt ná de workshop. Nuno is volledig gecertificeerd, gebruikt veilige showbrandstoffen en houdt de groep strak aan de veiligheidsinstructies, zodat het spannend blijft zonder ooit gevaarlijk te worden. Lees de <a href="/beoordelingen/">ervaringen van eerdere groepen</a>.</p>
""",
 "faq": [
  ("Wat kost een workshop vuurspuwen voor een vrijgezellenfeest?",
   "Vanaf €350 voor de groep, inclusief materialen, brandstoffen en begeleiding, exclusief reiskosten. Een combi met een mini-vuurshow vooraf is mogelijk; vraag naar het combitarief."),
  ("Hoe groot mag de groep zijn?",
   "Vier tot ongeveer twintig personen werkt het best. Bij grotere groepen wordt de workshop in rondes gedaan zodat iedereen persoonlijke begeleiding krijgt."),
  ("Is het niet gevaarlijk?",
   "Onder professionele begeleiding is het goed te doen: eerst techniek zonder vuur, dan stap voor stap opbouwen. Eén harde regel: deelnemen doe je nuchter — drinken komt na afloop."),
  ("Waar kan de workshop plaatsvinden?",
   "Overal met wat vrije buitenruimte: een veldje, parkeerplaats of het terrein van jullie feestlocatie. Nuno komt naar elke stad in Nederland en België en neemt alles mee."),
  ("Krijgen we foto's van de workshop?",
   "Ja — van elke deelnemer wordt de eerste vuurbal vastgelegd. Die foto's zijn legendarisch materiaal voor de groepsapp én de bruiloftsspeech."),
 ],
 "service": {"name": "Workshop vuurspuwen voor een vrijgezellenfeest", "type": "Workshop vuurspuwen",
   "desc": "Originele vrijgezellenfeest-activiteit: met de hele groep leren vuurspuwen onder professionele begeleiding, inclusief foto's. Vanaf €350, heel Nederland en België.",
   "offers": _OFFER("350", "750", "2", "Workshop vanaf €350 per groep; combi met mini-vuurshow op aanvraag.")},
 "fotos": [("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Deelnemer blaast zijn eerste vuurbal", "Workshopdeelnemer blaast een grote vuurbal tegen de avondlucht"),
           ("schemering-640.webp", "schemering-640.webp", 640, 423, "Vuurspuwen in de schemering", "Vuurspuwen in de schemering, de vlam waaiert breed uit"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "De vuurbal van de avond", "Vuurspuwer spuwt een enorme vuurbal in de avondschemering")],
},

"vuurwerk-alternatief": {
 "title": "Vuurwerk verboden? Boek een vuurshow",
 "seo_title": "\U0001F386 Alternatief voor Vuurwerk | Vuurshow: Wél Toegestaan, Net Zo Spectaculair",
 "seo_desc": "Vuurwerk verboden op je locatie of in je gemeente? Een professionele vuurshow geeft hetzelfde spektakel — dichterbij, stiller, zonder vergunningstress. Hét alternatief voor bruiloften en events.",
 "eyebrow": "Vuurwerk-alternatief",
 "img": ("/assets/media/vuurbal-1333.webp", "Meters hoge vuurbal tegen een zwarte nachtlucht boven vuurspuwer Nuno"),
 "body": """
<p><strong>Steeds meer gemeenten in Nederland en België beperken of verbieden consumentenvuurwerk, en op trouwlocaties, campings en in natuurgebieden mag het al jaren bijna nergens. Goed nieuws: er is een alternatief dat minstens zo spectaculair is — en vaak gewoon wél mag.</strong></p>

<h2>Waarom een vuurshow vaak wél kan waar vuurwerk niet mag</h2>
<p>Vuurwerk valt onder strenge afsteekregels en vergunningen; een professionele vuuract valt onder de evenementen- en locatieregels en werkt met gecontroleerd vuur op ooghoogte, zonder knallen en zonder projectielen. Nuno stemt de show vooraf af met de locatie, werkt binnen de vergunningseisen en houdt de voorgeschreven veiligheidsafstanden aan — geen afsteekvergunning-stress, geen vuurwerkafval, geen geschrokken huisdieren in de buurt.</p>

<h2>Vuurshow versus vuurwerk</h2>
<ul>
<li><strong>Dichtbij in plaats van ver weg</strong> — je gasten staan op enkele meters van metershoge vuurballen; elk telefoontje filmt mee.</li>
<li><strong>Stiller</strong> — geen knallen: geschikt voor woonwijken, campings, dieren in de buurt en gasten met kleine kinderen.</li>
<li><strong>Langer genieten</strong> — geen dertig seconden sterretjes, maar een show van 10 tot 30 minuten op jullie muziek.</li>
<li><strong>Persoonlijk</strong> — choreografie op de openingsdans, het jubileum-moment of de aftelling naar middernacht.</li>
<li><strong>Weerbestendig</strong> — een vuurshow kan bij wind en lichte regen waar siervuurwerk al lang is afgeblazen.</li>
</ul>

<h2>Voor welke momenten</h2>
<p>Het vuurwerk-alternatief is populair bij <a href="/vuurshow-bruiloft/">bruiloften</a> (grote finale in plaats van vuurwerk), <a href="/kerst-nieuwjaar-entertainment/">oud & nieuw en nieuwjaarsrecepties</a>, <a href="/vuurshow-bedrijfsfeest/">bedrijfsfeesten</a> en dorps- en stadsevenementen die geen vuurwerkvergunning krijgen. Ook op <a href="/vuurshow-festival/">festivals</a> vervangt een vuuract steeds vaker de traditionele afsluiter.</p>

<h2>Prijzen</h2>
<p>Een afsluitende vuurshow kost tussen de €350 (10 minuten) en €595 (volledige show van 30 minuten) — een fractie van professioneel siervuurwerk, zonder vergunningtraject. Bekijk het <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a> of <a href="/contact-3/">vraag een offerte aan</a> met je datum en locatie; binnen 24 uur antwoord. Nuno speelt in heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>.</p>
""",
 "faq": [
  ("Mag een vuurshow echt op plekken waar vuurwerk verboden is?",
   "Meestal wel: een professionele vuuract valt onder de regels van de locatie of het evenement, niet onder de vuurwerkregels. Nuno stemt dit vooraf rechtstreeks met de locatie of gemeente af."),
  ("Is een vuurshow net zo spectaculair als vuurwerk?",
   "Anders én dichterbij: metershoge vuurballen op enkele meters afstand, op muziek en met interactie. Gasten ervaren het intenser dan vuurwerk op honderd meter hoogte."),
  ("Wat kost een vuurshow als vuurwerk-alternatief?",
   "Tussen de €350 en €595 voor een afsluitshow van 10 tot 30 minuten — doorgaans aanzienlijk goedkoper dan professioneel siervuurwerk inclusief vergunningtraject."),
  ("Is het veilig voor gasten, kinderen en huisdieren?",
   "Ja: gecontroleerd vuur, professionele brandstoffen, een duidelijke veiligheidszone en geen knallen. Daardoor ook geschikt voor woonwijken en locaties met dieren in de buurt."),
  ("Werkt het ook met oud & nieuw?",
   "Juist dan: een aftelshow naar middernacht is de perfecte vervanging van de vuurwerkshow — boek december wel ruim op tijd."),
 ],
 "service": {"name": "Vuurshow als alternatief voor vuurwerk", "type": "Vuurshow",
   "desc": "Spectaculair en toegestaan alternatief voor vuurwerk op bruiloften, oud & nieuw en evenementen: vuurshow van 10-30 minuten, stiller, dichterbij en zonder vergunningstress. Vanaf €350.",
   "offers": _OFFER("350", "750", "3", "Afsluitshow 10 min vanaf €350, showblok 20 min vanaf €450, volledige finale 30 min vanaf €595.")},
 "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal in de nacht", "Meters hoge vuurbal tegen een zwarte nachtlucht"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Finale in de schemering", "Vuurspuwer spuwt een enorme vuurbal in de avondschemering"),
           ("festival-900.webp", "festival-1600.webp", 900, 902, "Publiek bij de vuurshow", "Vuurspuwer spuwt een vuurbal voor een groot publiek")],
},

"kerst-nieuwjaar-entertainment": {
 "title": "Entertainment voor kerstfeest & nieuwjaarsreceptie",
 "seo_title": "\U0001F384 Kerstfeest & Nieuwjaarsreceptie Entertainment | Vuurshow in de Winteravond",
 "seo_desc": "Entertainment voor je kerstborrel, personeelsfeest of nieuwjaarsreceptie? In de donkere wintermaanden komt een vuurshow maximaal tot zijn recht. December loopt vroeg vol — boek op tijd. Vanaf €450.",
 "eyebrow": "Kerst & nieuwjaar",
 "img": ("/assets/media/schemering-640.webp", "Vuurspuwen in de vroege winterschemering, de vlam waaiert breed uit"),
 "body": """
<p><strong>December is de mooiste maand voor vuur: om vijf uur is het al donker, gasten staan buiten bij de vuurkorven — en dan opent Nuno de avond met metershoge vlammen. Voor kerstborrels, personeelsfeesten en nieuwjaarsrecepties is een vuurshow het winterspektakel bij uitstek.</strong></p>

<h2>Waarom vuur en winter zo goed samengaan</h2>
<p>In de zomer moet een vuurshow wachten tot na tienen; in december is het al in de namiddag donker genoeg voor het volle effect. De warmte van de vlammen, de vonkenregens tegen de winterlucht, gasten met glühwein op veilige afstand: het is de sfeer waar december-feesten het van moeten hebben. En sneeuw of lichte regen? Geen probleem voor een professionele vuuract.</p>

<h2>Voor elk decemberfeest</h2>
<ul>
<li><strong>De kerstborrel of het personeelsfeest</strong> — een showblok van 20 minuten als hoogtepunt van de <a href="/vuurshow-bedrijfsfeest/">bedrijfsavond</a>, vanaf €450.</li>
<li><strong>De nieuwjaarsreceptie</strong> — open het jaar met vuur: een krachtige act van 10 minuten voor personeel of leden, vanaf €350.</li>
<li><strong>Oud & nieuw</strong> — de aftelshow naar middernacht als <a href="/vuurwerk-alternatief/">alternatief voor vuurwerk</a>, zonder knallen en vergunningstress.</li>
<li><strong>Winterse themafeesten</strong> — combineer met de <a href="/fakir-show-inhuren/">fakirshow</a> of <a href="/entertainer-huren/">mentalisme</a> voor het programma binnen, en vuur voor het moment buiten.</li>
<li><strong>Winter-events en kerstmarkten</strong> — meerdere korte sets per avond, zoals op <a href="/vuurshow-festival/">festivals</a>.</li>
</ul>

<h2>December loopt het vroegst vol</h2>
<p>De vrijdagen en donderdagen van december zijn elk jaar de eerste die volgeboekt raken — bedrijven plannen hun kerstfeest vaak al in september of oktober. Wil je zeker zijn van je datum, <a href="/contact-3/">check hem dan nu</a>; binnen 24 uur weet je of het kan, inclusief offerte. Alle pakketten en prijzen staan in het <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a>.</p>

<h2>Praktisch in de winter</h2>
<p>Een vuurshow heeft buiten maar weinig ruimte nodig — een terras, binnenplaats of parkeerterrein bij de feestlocatie volstaat vaak. Nuno is gecertificeerd, werkt binnen de vergunningseisen van de locatie en speelt door heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>; lees de <a href="/beoordelingen/">beoordelingen</a> van eerdere winterfeesten.</p>
""",
 "faq": [
  ("Wat kost entertainment voor een kerstfeest of nieuwjaarsreceptie?",
   "Een openingsact van 10 minuten vanaf €350, het volledige showblok van 20 minuten vanaf €450. Bedrijven ontvangen één all-in offerte op factuur."),
  ("Kan een vuurshow bij kou, regen of sneeuw?",
   "Ja — kou en lichte neerslag zijn geen probleem; de show wordt er in het donker alleen maar spectaculairder op. Alleen bij storm wordt in overleg een alternatief of nieuw moment gekozen."),
  ("Hoe vroeg moeten we ons decemberfeest boeken?",
   "De donderdag- en vrijdagavonden van december zijn elk jaar in de vroege herfst al grotendeels vol. Boek bij voorkeur vóór oktober; last-minute kan soms doordeweeks."),
  ("Is een vuurshow geschikt als vervanging van vuurwerk met oud & nieuw?",
   "Ja — de aftelshow naar middernacht is stiller, veiliger en persoonlijker dan vuurwerk, en meestal wél toegestaan. Zie ook de pagina over het vuurwerk-alternatief."),
  ("Kan er ook een programma binnen worden verzorgd?",
   "Zeker: mentalisme of de fakirshow voor het binnenprogramma, en het vuurspektakel buiten als hoogtepunt — een populaire wintercombinatie."),
 ],
 "service": {"name": "Vuurshow voor kerstfeest en nieuwjaarsreceptie", "type": "Vuurshow",
   "desc": "Winterspektakel voor kerstborrels, personeelsfeesten, nieuwjaarsrecepties en oud & nieuw: vuurshow in de vroege winteravond, ook als vuurwerk-alternatief. Vanaf €450.",
   "offers": _OFFER("350", "1500", "4", "Nieuwjaarsact 10 min vanaf €350, kerstshowblok 20 min vanaf €450, volledige show vanaf €595, meerdere sets tot €1500.")},
 "fotos": [("schemering-640.webp", "schemering-640.webp", 640, 423, "Vuur in de vroege schemering", "Vuurspuwen in de schemering, de vlam waaiert breed uit"),
           ("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal tegen de nachtlucht", "Meters hoge vuurbal tegen een zwarte nachtlucht"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Fakirshow voor het binnenprogramma", "Fakiract: Nuno draagt het gewicht van een staande toeschouwer")],
},
}
