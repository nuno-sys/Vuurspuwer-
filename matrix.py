"""De stad x show-matrix: voor elke stad in Nederland en Vlaanderen een
eigen pagina per show (fakirshow, workshop, Halloween). Elke pagina krijgt
een eigen stadskarakter, roterende tekstvarianten, een FAQ en een
Service-schema met de stad als werkgebied — geen twee pagina's gelijk."""

SITE = "https://vuurspuwer.com"

# stadssleutel -> (label, sfeerzin over locaties in die stad, NL-stadspagina)
CITIES = {
 "amsterdam":  ("Amsterdam", "van een rooftopbar aan het IJ tot een bedrijfsfeest op de Zuidas of een borrel in een pakhuis aan de gracht", "vuurspuwer-boeken-in-amsterdam"),
 "rotterdam":  ("Rotterdam", "van een loods op Katendrecht tot een dakterras met skyline-zicht of een festival in het Zuiderpark", "vuurspuwer-boeken-in-rotterdam"),
 "den-haag":   ("Den Haag", "van een strandpaviljoen op Scheveningen tot een statige zaal in het centrum of een bedrijfsfeest op de Binckhorst", "vuurspuwer-boeken-in-den-haag"),
 "utrecht":    ("Utrecht", "van een werfkelder aan de Oudegracht tot een evenementenhal in Leidsche Rijn — en Zeist ligt om de hoek, dus voorrijkosten vallen mee", "vuurspuwer-boeken-in-utrecht"),
 "eindhoven":  ("Eindhoven", "van Strijp-S tot het Ketelhuis: industriële locaties en vuur zijn een gouden combinatie", "vuurspuwer-boeken-in-eindhoven"),
 "groningen":  ("Groningen", "van de Grote Markt tot een feestzaal in de binnenstad of een studentenvereniging met lef", "vuurspuwer-boeken-in-groningen"),
 "tilburg":    ("Tilburg", "van de Spoorzone tot een festivalterrein of kroegenfeest — kermisstad Tilburg weet wat spektakel is", "vuurspuwer-boeken-in-tilburg"),
 "breda":      ("Breda", "van het Chassé-terrein tot een landgoed of tuinfeest onder de Grote Kerk", "vuurspuwer-boeken-in-breda"),
 "antwerpen":  ("Antwerpen", "van het Eilandje tot een kasteeltuin of magazijnfeest aan de Schelde", "vuurspuwer-boeken-in-antwerpen"),
 "gent":       ("Gent", "van de Graslei tot een loods in de Dampoort of een verlicht winterfeest", "vuurspuwer-boeken-in-gent"),
 "brussel":    ("Brussel", "van een zaal aan de Grote Markt tot een bedrijfsevent in de Europese wijk — tweetalige communicatie is vanzelfsprekend", "vuurspuwer-boeken-in-brussel"),
 "brugge":     ("Brugge", "tegen het decor van de middeleeuwse binnenstad wordt elke vuuract een sprookje", "vuurspuwer-boeken-in-brugge"),
 "leuven":     ("Leuven", "van het Ladeuzeplein tot een studentikoos feest of bedrijfsevent in de rand", "vuurspuwer-boeken-in-leuven"),
 "luik":       ("Luik", "van de Médiacité tot een feest aan de Maas — la Cité Ardente maakt haar naam waar", "vuurspuwer-boeken-in-liege"),
 "mechelen":   ("Mechelen", "van de Grote Markt onder Sint-Rombouts tot het Vrijbroekpark", "vuurspuwer-boeken-in-mechelen"),
}

# per show: url-voorvoegsel, hoofdpagina, kopfoto, teksten en FAQ
def _rot(key, opties):
    return opties[sum(map(ord, key)) % len(opties)]

SHOWS = {
 "fakirshow": {
  "prefix": "fakirshow",
  "main": "/fakir-show-inhuren/",
  "main_txt": "de fakirshow",
  "img": ("/assets/media/fakirshow-640.webp", "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer"),
  "eyebrow": "Fakirshow op locatie",
  "title": "Fakirshow boeken in {stad}",
  "seo_title": "\U0001F525 Fakirshow Boeken in {stad} | Spijkerbed, Glas & Zwaarden — Nuno",
  "seo_desc": "Fakirshow boeken in {stad}? Nuno trotseert spijkerbed, glas en zwaarden — met het publiek als deel van de act. 4,9/5 uit 136 reviews. Offerte binnen 24 uur!",
  "intros": [
   "<p>Een act waar {stad} nog lang over napraat? Boek de <a href=\"{main}\">fakirshow</a> van Nuno: spijkerbed, glaslopen, zwaardkunsten en vuur — uitgevoerd met de precisie van zeventien jaar podiumervaring, en met uw publiek als deel van de show.</p>",
   "<p>Op zoek naar entertainment in {stad} dat verder gaat dan een bandje of dj? De <a href=\"{main}\">fakirshow</a> van Nuno laat gasten huiveren én juichen: spijkerbed, glas, zwaarden en vuur, gebracht met theatrale klasse en absolute veiligheid.</p>",
   "<p>Sommige shows kijk je, deze vóél je. Met de <a href=\"{main}\">fakirshow</a> haalt u een act naar {stad} die het publiek actief meemaakt: wie durft er op de fakir te staan terwijl hij op het spijkerbed ligt?</p>",
  ],
  "kern": """
<h2>Wat de fakirshow in {stad} inhoudt</h2>
<p>Nuno loopt over glasscherven, laat toeschouwers op zich staan terwijl hij op het spijkerbed ligt, demonstreert zwaardkunsten en sluit af met vuurspuwen. De show duurt 15 tot 60 minuten en past zich aan uw programma aan — als spektakelblok op het podium of dichtbij tussen de gasten. Perfect voor thema's als 1001-nacht, magie, circus of gewoon een avond die anders durft te zijn.</p>
<h2>Fakirshow op elke locatie in {stad}</h2>
<p>De fakirshow heeft geen vlammenzee nodig en kan daardoor vrijwel overal: {sfeer}. Binnen kan vrijwel altijd; buiten sowieso. Combineren met een <a href="/{stadpagina}/">vuurshow</a> of een <a href="/workshop-vuurspuwen-{key}/">workshop vuurspuwen</a> maakt er een complete showavond van.</p>
""",
  "faq": [
   ("Kan de fakirshow binnen in {stad}?",
    "Ja — de fakirshow is juist ideaal voor binnenlocaties: het spijkerbed, glaslopen en de zwaardacts hebben geen open vuur nodig. Alleen voor het vuurspuwen als finale is wat vrije hoogte of een buitenmoment nodig; zonder kan ook."),
   ("Hoe lang duurt een fakirshow?",
    "Van een compact spektakelblok van 15 minuten tot een volledige voorstelling van een uur, en maximaal vier optredens op één avond. De show wordt afgestemd op uw programma in {stad}."),
   ("Wat kost een fakirshow in {stad}?",
    "De prijs hangt af van duur en programma; reistijd naar {stad} wordt netjes in de offerte meegenomen. Vraag vrijblijvend een offerte aan — u hoort binnen 24 uur of uw datum vrij is."),
  ],
  "service": ("Fakirshow in {stad}", "Fakir Performance",
              "Fakirshow van Nuno in {stad}: spijkerbed, glaslopen, zwaardkunsten en vuurspuwen, veilig en theatraal gebracht voor feesten en evenementen."),
 },

 "workshop-vuurspuwen": {
  "prefix": "workshop-vuurspuwen",
  "main": "/workshop-vuurspuwen/",
  "main_txt": "de workshop vuurspuwen",
  "img": ("/assets/media/workshop-1125.webp", "Workshop vuurspuwen onder begeleiding van professioneel vuurspuwer Nuno"),
  "eyebrow": "Workshop op locatie",
  "title": "Workshop vuurspuwen in {stad}",
  "seo_title": "\U0001F525 Workshop Vuurspuwen in {stad} | Teambuilding & Vrijgezellen — Nuno",
  "seo_desc": "Workshop vuurspuwen in {stad}: leer zelf veilig vuurspuwen onder begeleiding van Nuno. Dé activiteit voor teambuilding en vrijgezellenfeesten. Offerte binnen 24 uur!",
  "intros": [
   "<p>Zelf een metershoge vuurbal de lucht in blazen, midden in {stad}? Tijdens de <a href=\"{main}\">workshop vuurspuwen</a> leert Nuno uw groep stap voor stap de kunst van het vuurspuwen — veilig, verantwoord en onvergetelijk.</p>",
   "<p>Teambuilding waar écht over gepraat wordt: geen escaperoom, maar leren vuurspuwen. Nuno komt met alle materialen naar {stad} en begeleidt uw groep van eerste uitleg tot de eerste eigen vuurbal.</p>",
   "<p>Voor de vrijgezel die alles al heeft, het team dat wel wat vuur kan gebruiken of de verjaardag die anders moet: de <a href=\"{main}\">workshop vuurspuwen</a> in {stad} verlegt letterlijk grenzen.</p>",
  ],
  "kern": """
<h2>Zo werkt de workshop in {stad}</h2>
<p>Eerst veiligheid: brandstoffen, beschermende kleding en techniek. Dan oefenen zonder vuur, en wie er klaar voor is spuwt onder Nuno's begeleiding zijn of haar eerste echte vuurbal — met foto's als bewijs. De workshop past zich aan het niveau van de groep aan, van complete beginners tot durfals die meer willen, en duurt één tot enkele uren.</p>
<h2>Locaties in en rond {stad}</h2>
<p>Nodig is vooral wat vrije buitenruimte: {sfeer}. Nuno neemt alle materialen mee. De workshop laat zich goed combineren met een <a href="/{stadpagina}/">vuurshow als opening of finale</a> — eerst kijken hoe het moet, dan zelf doen.</p>
""",
  "faq": [
   ("Is de workshop vuurspuwen in {stad} veilig?",
    "Ja. Veiligheid is het halve programma: eerst de juiste brandstoffen, kleding en techniek, dan pas vuur — stap voor stap onder professionele begeleiding van Nuno, met alle veiligheidsmaterialen erbij."),
   ("Voor welke groepen is de workshop geschikt?",
    "Voor iedereen vanaf 18 jaar: vrijgezellenfeesten, teambuilding, verjaardagen en verenigingen in en rond {stad}. Het programma wordt op maat van de groepsgrootte en het lef van de deelnemers gemaakt."),
   ("Wat hebben we nodig op onze locatie in {stad}?",
    "Vooral wat vrije buitenruimte zonder overkapping. Nuno neemt brandstoffen, fakkels en veiligheidsmaterialen mee en overlegt vooraf kort over de plek. Twijfelt u over uw locatie? Stuur hem gewoon mee met de aanvraag."),
  ],
  "service": ("Workshop vuurspuwen in {stad}", "Workshop / Teambuilding",
              "Workshop vuurspuwen van Nuno in {stad}: veilig leren vuurspuwen als teambuilding, vrijgezellenactiviteit of feestprogramma, met alle materialen inbegrepen."),
 },

 "halloween": {
  "prefix": "halloween",
  "main": "/halloween/",
  "main_txt": "de Halloween-acts",
  "img": ("/assets/media/vuurbal-1333.webp", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
  "eyebrow": "\U0001F383 Halloween in {stad}",
  "title": "Halloween vuurshow & horror-acts in {stad}",
  "seo_title": "\U0001F383 Halloween Vuurshow {stad} | Horror-Fakir & Scare-Acts — vanaf €350",
  "seo_desc": "Halloween-act boeken in {stad}? Duivelse vuurshows, horror-fakir en scare-acts van Nuno — bekend van Walibi's Fright Nights. Vanaf €350. Oktober loopt vol!",
  "intros": [
   "<p>Halloween in {stad} mag dit jaar wel wat heter. Nuno — bekend van de <strong>Halloween Fright Nights van Walibi Holland</strong> — komt met duivelse <a href=\"{main}\">vuurshows, een horror-fakir en scare-acts</a> die uw gasten laten gillen én applaudisseren.</p>",
   "<p>Een spooktocht, horrornacht of Halloween-bedrijfsfeest in {stad}? Met vlammen uit het donker, een spijkerbed bij fakkellicht en scare-momenten tussen het publiek maakt Nuno er een avond van die niemand vergeet — <a href=\"{main}\">bekijk alle Halloween-acts</a>.</p>",
   "<p>Vuur en duisternis horen bij elkaar, en nergens beter dan met Halloween. Nuno transformeert voor {stad} tot demon, duivel of horror-fakir — van gezinsvriendelijk griezelen tot volwassen horror, <a href=\"{main}\">afgestemd op uw thema</a>.</p>",
  ],
  "kern": """
<h2>Halloween-acts voor {stad}</h2>
<ul>
<li>\U0001F608 <strong>Duivelse vuurshow</strong> — vlammen, vonken en vuurzuilen in horror-styling (vanaf &euro;350)</li>
<li>\U0001F5E1️ <strong>Horror-fakirshow</strong> — spijkerbed, glas en zwaarden in griezelgrime (vanaf &euro;450)</li>
<li>\U0001F441️ <strong>Duister mentalisme</strong> — gedachten lezen met een onheilspellend randje</li>
<li>\U0001F525 <strong>Complete Halloween-productie</strong> — meerdere acts verspreid over de avond (vanaf &euro;750)</li>
</ul>
<h2>Van spooktocht tot bedrijfsfeest in {stad}</h2>
<p>Elke Halloween-locatie werkt: {sfeer}. Kostuum en grime worden op uw thema afgestemd; de intensiteit ook — een scoutinggroep krijgt een ander programma dan een horrornacht voor volwassenen. Rond 31 oktober zijn de weekenden elk jaar als eerste vol: wie {stad} zeker wil, boekt vóór september.</p>
""",
  "faq": [
   ("Wat kost een Halloween-act in {stad}?",
    "Vanaf €350 voor de duivelse vuurshow, vanaf €450 voor de horror-fakirshow en vanaf €750 voor een complete avondproductie met meerdere acts — plus reiskosten naar {stad}, netjes in de offerte."),
   ("Is de show geschikt voor ons publiek?",
    "Ja — de intensiteit wordt afgestemd: van gezinsvriendelijk griezelen bij een buurtfeest tot stevige horror voor een volwassen publiek. Kostuum, grime en interactie gaan mee in uw thema."),
   ("Hoe vroeg moeten we boeken voor Halloween in {stad}?",
    "De weekenden rond 31 oktober zijn elk jaar het eerst vergeven. Boek bij voorkeur vóór september; last-minute kan soms, maar de keuze in data en acts is dan beperkt."),
  ],
  "service": ("Halloween-entertainment in {stad}", "Halloween entertainment",
              "Halloween vuurshows, horror-fakiracts en scare-entertainment van Nuno in {stad}: voor spooktochten, horrornachten, themafeesten en bedrijfsfeesten."),
 },
}

def page_slug(show_key, city_key):
    return f"{SHOWS[show_key]['prefix']}-{city_key}"

def build_page(show_key, city_key):
    """(pagina-dict, extra_html, schema-lijst) voor één stad x show."""
    S = SHOWS[show_key]
    stad, sfeer, stadpagina = CITIES[city_key]
    slug = page_slug(show_key, city_key)
    f = lambda t: t.format(stad=stad, sfeer=sfeer, stadpagina=stadpagina,
                           key=city_key, main=S["main"])
    intro = _rot(slug, S["intros"])
    body = f(intro) + f(S["kern"])

    # dwarsverbanden: de andere shows in deze stad + buursteden met dezelfde show
    andere = [k for k in SHOWS if k != show_key]
    ook = "".join(
        f'<li><a href="/{page_slug(k, city_key)}/">{SHOWS[k]["title"].format(stad=stad)}</a></li>'
        for k in andere)
    ook += f'<li><a href="/{stadpagina}/">Vuurspuwer boeken in {stad}</a></li>'
    keys = list(CITIES)
    i = keys.index(city_key)
    buren = [keys[(i + n) % len(keys)] for n in range(1, 7)]
    buurt = "".join(
        f'<li><a href="/{page_slug(show_key, b)}/">{S["title"].format(stad=CITIES[b][0])}</a></li>'
        for b in buren)
    body += (f'<h2>Ook in {stad} en omgeving</h2>'
             f'<ul class="citylist">{ook}</ul>')
    extra_html = (f'<section class="wrap bay"><h2 class="bay__title">Ook in de <em>buurt</em></h2>'
                  f'<ul class="citylist">{buurt}</ul></section>')

    faq = [(q.format(stad=stad), a.format(stad=stad)) for q, a in S["faq"]]
    naam, styp, sdesc = (x.format(stad=stad) for x in S["service"])
    schema = [
        {"@context": "https://schema.org", "@type": "Service",
         "@id": f"{SITE}/{slug}/#service", "name": naam, "serviceType": styp,
         "description": sdesc, "url": f"{SITE}/{slug}/",
         "image": SITE + S["img"][0],
         "provider": {"@id": f"{SITE}/#business"},
         "areaServed": {"@type": "City", "name": stad}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in faq]},
    ]
    fq = "".join(f'<details class="faq__item"><summary>{q}</summary><p>{a}</p></details>'
                 for q, a in faq)
    extra_html += ('<section class="wrap bay" aria-label="Veelgestelde vragen">'
                   '<div class="bay__head"><p class="eyebrow eyebrow--dim rise">Veelgestelde vragen</p>'
                   f'<h2 class="bay__title rise" data-delay="1">Eerst even <em>zeker weten</em></h2></div>'
                   f'<div class="faq">{fq}</div></section>')
    p = {"slug": slug, "title": S["title"].format(stad=stad),
         "seo_title": S["seo_title"].format(stad=stad),
         "seo_desc": S["seo_desc"].format(stad=stad),
         "eyebrow": S["eyebrow"].format(stad=stad),
         "img": S["img"], "body": body}
    return p, extra_html, schema

def stad_dwarslinks(city_slug_nl):
    """Voor de bestaande NL-stadspagina: links naar de matrixpagina's."""
    for key, (stad, _, stadpagina) in CITIES.items():
        if stadpagina == city_slug_nl:
            links = "".join(
                f'<li><a href="/{page_slug(k, key)}/">{SHOWS[k]["title"].format(stad=stad)}</a></li>'
                for k in SHOWS)
            return (f'<section class="wrap bay"><h2 class="bay__title">Meer in <em>{stad}</em></h2>'
                    f'<ul class="citylist">{links}</ul></section>')
    return ""
