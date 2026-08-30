"""Eigen inhoud voor de video's-pagina, de drie showpagina's en de
Halloween-pagina. De teksten komen van de live site en zijn opgeschoond
en licht aangescherpt; de webadressen blijven exact gelijk."""

SITE = "https://vuurspuwer.com"

# ------------------------------------------------------------------ video's
VIDEOS = [
    ("reel-1.mp4", "reel-1-poster.webp", "PT19S",
     "Vuurshow op locatie",
     "Vuurspuwer Nuno tijdens een vuurshow op locatie: vuurspuwen, vuurjongleren en body fire."),
    ("reel-2.mp4", "reel-2-poster.webp", "PT58S",
     "Acts & fakirwerk",
     "Compilatie van vuur- en fakiracts van Vuurspuwer Nuno op festivals en bedrijfsfeesten."),
    ("showreel.mp4", "reel-poster.jpg", "PT13S",
     "Showreel",
     "Korte showreel van vuurspuwer en fakir Nuno."),
    ("hero-portrait.mp4", "vuurbal-900.webp", "PT5S",
     "Vuurbal in close-up",
     "Meters hoge vuurbal van vuurspuwer Nuno, gefilmd van dichtbij."),
]

def videos_body():
    tiles = []
    for i, (src, poster, _, cap, alt) in enumerate(VIDEOS):
        ratio = ' data-ratio="9/16"' if "portrait" in src else ""
        tiles.append(f'''<figure class="reel rise"{ratio}>
        <video muted loop playsinline preload="none" poster="/assets/media/{poster}"
               data-src="/assets/media/{src}" aria-label="{alt}"></video>
        <button class="reel__play" type="button" aria-label="Video afspelen: {cap}">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <figcaption class="reel__hud"><span>{cap}</span><span class="reel__time"></span></figcaption>
      </figure>''')
    return ('<p>Vuurshows, fakiracts en vuurspuwen in beweging: een greep uit de '
            'optredens van de afgelopen jaren. Klik op een video om hem af te spelen '
            '&mdash; of bekijk ook <a href="/fotos/">alle foto&rsquo;s</a> en '
            '<a href="/#boeken">vraag direct een offerte aan</a>.</p>'
            '<div class="reels reels--page">' + "".join(tiles) + "</div>")

def videos_schema():
    return {"@context": "https://schema.org", "@type": "VideoGallery",
            "name": "Video's van Vuurspuwer Nuno",
            "url": f"{SITE}/videos/",
            "about": {"@id": f"{SITE}/#business"},
            "video": [{"@type": "VideoObject",
                       "name": f"{cap} — Vuurspuwer Nuno",
                       "description": alt,
                       "contentUrl": f"{SITE}/assets/media/{src}",
                       "thumbnailUrl": f"{SITE}/assets/media/{poster}",
                       "uploadDate": "2026-08-30", "duration": dur,
                       "publisher": {"@id": f"{SITE}/#business"}}
                      for src, poster, dur, cap, alt in VIDEOS]}

# -------------------------------------------------------------- showpagina's
# hulpstukje: een rij fotos onder het artikel
def _fotorij(items):
    tiles = "".join(
        f'<a href="/assets/media/{full}" data-lightbox data-cap="{cap}">'
        f'<img src="/assets/media/{thumb}" width="{w}" height="{h}" loading="lazy" '
        f'decoding="async" alt="{alt}"></a>'
        for thumb, full, w, h, cap, alt in items)
    return f'<h2>Foto’s uit de show</h2><div class="fgrid">{tiles}</div>'

SHOW_PAGES = {
 "vuurspuwer-inhuren": {
  "title": "Vuurspuwer inhuren: boek de meest spectaculaire vuurshow van Nederland & België",
  "seo_title": "\U0001F525 Vuurspuwer Inhuren – Meest Spectaculaire Vuurshow NL & BE",
  "seo_desc": "Vuurspuwer inhuren in Nederland of België? Nuno is dé meest gevraagde vuurartiest van de Benelux. Adembenemende shows voor elk evenement. Vraag vandaag nog offerte aan!",
  "eyebrow": "Vuurshow",
  "img": ("/assets/media/avondvuur-1080.webp", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
  "body": """
<p>Zoekt u niet zomaar entertainment, maar een act die uw gasten letterlijk ademloos achterlaat? Een openingsshow of afsluiter waar nog jaren over gesproken wordt? Welkom in de wereld van Nuno.</p>
<p>Als een van de meest gevraagde en ervaren vuurartiesten en fakirs van de Benelux tilt Nuno elk evenement naar een ongekend niveau. Met <a href="/over-nuno/" title="meer dan 15 jaar internationale ervaring">meer dan 15 jaar internationale ervaring</a>, spectaculaire tv-optredens en een absolute focus op veiligheid levert Nuno geen standaard vuurspuw-act, maar een high-end visueel meesterwerk &mdash; <a href="/locaties-vuurshows-nederland-belgie/" title="aangepast aan uw locatie">aangepast aan uw locatie</a>.</p>
<p>Klaar om de vonk te laten overslaan? Lees verder of vraag direct een vrijblijvende offerte aan. Meer weten over wat een vuurspuwer doet? Lees <a href="https://nl.wikipedia.org/wiki/Vuurspuwen" rel="noopener">deze pagina op Wikipedia</a>.</p>

<h2>Waarom eventplanners exclusief kiezen voor vuurartiest Nuno</h2>
<p>Bij het werken met vuur is er geen ruimte voor fouten of amateurisme. Eventplanners, bruidsparen en festivalorganisatoren kiezen voor Nuno vanwege de ijzersterke combinatie van artistieke perfectie en strikte professionaliteit.</p>
<h3>\U0001F525 Visueel spektakel van wereldklasse</h3>
<ul>
<li><strong>Visueel spektakel</strong> &mdash; geen simpele vlammetjes, maar metershoge vuurwolken, vuurjongleren en indrukwekkende choreografie&euml;n op muziek.</li>
<li><strong>100% veilig &amp; gecertificeerd</strong> &mdash; veiligheid staat op &eacute;&eacute;n: professioneel materiaal, veilige vloeistoffen en alle vergunningseisen en afstanden.</li>
<li><strong>High-end uitstraling</strong> &mdash; strakke kostuums, professionele houding en stipte communicatie. Perfect voor zakelijke evenementen.</li>
<li><strong>Flexibel inzetbaar</strong> &mdash; een podium in Amsterdam, een kasteeltuin in Antwerpen of een intieme oprit: de show wordt aangepast aan uw locatie. Benieuwd naar de mogelijkheden? Neem <a href="/contact-3/">contact</a> op.</li>
</ul>

<h2>Onze vuurshows: een explosie van entertainment</h2>
<p>Een vuurshow van Nuno is maatwerk. Wij bieden verschillende formats die passen bij de dynamiek van uw evenement:</p>
<ul>
<li><strong>De Power-Act (5&ndash;10 min)</strong> &mdash; een korte, explosieve show. Ideaal als openingsact of spectaculaire afsluiter om het energieniveau naar een hoogtepunt te brengen.</li>
<li><strong>De Volledige Vuurshow (20&ndash;30 min)</strong> &mdash; een opbouwende show met fakir-elementen, lichaamsvuur, vuurspuwen en interactie met het publiek.</li>
<li><strong>Duo Shows</strong> &mdash; voor extra impact kan Nuno geboekt worden samen met een vrouwelijke vuurartiest of danseres.</li>
</ul>
<p>Binnen (indien de locatie het toelaat) of buiten: wij zorgen voor de wow-factor.</p>

<h2>Ook mogelijk: interactieve workshops vuurspuwen</h2>
<p>Wilt u niet alleen kijken, maar ook doen? Nuno biedt unieke <a href="/workshop-vuurspuwen/" title="workshops vuurspuwen">workshops vuurspuwen</a> aan. Een origineel idee voor teambuilding, vrijgezellenfeesten of avontuurlijke bedrijfsuitjes.</p>
<ul>
<li>Verleg uw grenzen en vergroot het zelfvertrouwen van het team.</li>
<li>Leer de basisprincipes van vuurmanipulatie.</li>
<li>Veilige technieken onder strikte professionele begeleiding.</li>
</ul>

<h2>Voor welke evenementen is Nuno geschikt?</h2>
<ul>
<li>\U0001F389 <strong>Jubilea &amp; priv&eacute;feesten</strong> &mdash; exclusief entertainment gewoon bij u in de tuin of op locatie.</li>
<li>\U0001F3E2 <strong>Bedrijfsfeesten</strong> &mdash; indruk maken op klanten of personeel met een krachtige opening.</li>
<li>\U0001F48D <strong>Bruiloften</strong> &mdash; een romantische vuurshow als alternatief voor vuurwerk (vaak w&eacute;l toegestaan waar vuurwerk verboden is!).</li>
<li>\U0001F3AA <strong>Festivals &amp; evenementen</strong> &mdash; een visuele trekpleister die perfect werkt op social media. Bekijk ook de <a href="/locaties-vuurshows-nederland-belgie/">locaties in Nederland en Belgi&euml;</a>.</li>
</ul>

<h2>Klaar om uw evenement in vuur en vlam te zetten?</h2>
<p>Wacht niet te lang met het vastleggen van uw datum: de agenda van Nuno loopt snel vol, zeker in het hoogseizoen. <a href="/#boeken">Check beschikbaarheid &amp; prijzen</a>, bel <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> of app via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
""",
  "faq": [
   ("Is een vuurshow veilig op mijn locatie?",
    "Ja, veiligheid is prioriteit nummer één. Nuno werkt volgens strikte veiligheidsprotocollen, gebruikt professionele vloeistoffen en materialen, en past de show aan op de beschikbare ruimte en locatie (zowel binnen als buiten)."),
   ("Wat kost het inhuren van een vuurspuwer?",
    "De prijs is afhankelijk van het type show, de duur en de locatie. Omdat elke show maatwerk is, kunt u het beste direct een vrijblijvende offerte aanvragen voor een prijsopgave op maat."),
   ("Kan de vuurshow ook binnen plaatsvinden?",
    "Ja, mits de locatie voldoet aan bepaalde veiligheidseisen (zoals plafondhoogte en ventilatie). Nuno heeft speciale acts ontwikkeld die veilig binnen uitgevoerd kunnen worden, bijvoorbeeld met lichaamsvuur en fakir-technieken."),
   ("In welke regio's treedt Vuurspuwer Nuno op?",
    "Nuno verzorgt optredens door heel Nederland en België. Van Amsterdam en Rotterdam tot Antwerpen en Brussel. Reiskosten worden berekend in de offerte."),
  ],
  "service": {"name": "Vuurshow", "type": "Fire Show / Vuurperformance",
              "desc": "Spectaculaire vuurshow met vuurspuwen, vuurjongleren en indrukwekkende effecten. Professioneel, veilig en geschikt voor bedrijfsfeesten, bruiloften en festivals."},
  "fotos": [("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Vuurbal in de avondschemering", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
            ("festival-900.webp", "festival-1600.webp", 900, 902, "Complete vuurshow op een festival", "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek"),
            ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Vuurshow bij daglicht", "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe")],
 },

 "fakir-show-inhuren": {
  "title": "Fakir show: heerser over angst en pijn",
  "seo_title": "\U0001F525 Fakir Show Inhuren – Sensationele Act van Nuno de Fakir",
  "seo_desc": "Fakir show inhuren voor uw evenement? Nuno de Fakir beheerst angst en pijn als geen ander. Een onvergetelijke act die uw publiek doet huiveren. Boek nu!",
  "eyebrow": "Fakirshow",
  "img": ("/assets/media/fakirshow-640.webp", "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer"),
  "body": """
<p>Sta versteld van de diverse kunsten van de <strong>fakirshow</strong>! Bent u op zoek naar een originele en sensationele act voor uw evenement? <a href="/over-nuno/" title="Nuno de Fakir, meester in zijn vak">Nuno de Fakir, meester in zijn vak</a>, biedt een onvergetelijke ervaring. Boek een fakirshow die uw publiek zal doen huiveren.</p>

<h2>Wat kunt u verwachten van een fakirshow?</h2>
<p>De fakirshow is een spectaculaire voorstelling vol adembenemende acts. Nuno loopt over glas, trotseert spijkerbedden en demonstreert indrukwekkende zwaardkunsten. Vuurspuwen, een klassieker, mag natuurlijk niet ontbreken! Het publiek wordt actief betrokken bij de show &mdash; bijvoorbeeld door op de fakir te staan terwijl hij op een spijkerbed ligt (altijd onder begeleiding). De duur van de show varieert van 15 tot 60 minuten, afgestemd op uw wensen.</p>
<p>Wilt u de fakirshow combineren met andere acts? Dat kan! Denk aan <a href="/vuurspuwer-inhuren/">vuurspuwen</a> of een <a href="/reptielenhow/">reptielenshow</a>. Wij denken graag met u mee om een unieke ervaring te cre&euml;ren.</p>

<h2>Locaties voor een fakirshow</h2>
<p>De fakirshow is geschikt voor vrijwel elke locatie, van podia tot straatoptredens. Met jarenlange ervaring weet Nuno op elke plek een fantastische show neer te zetten. De show kan worden aangepast aan uw wensen: langer, korter, of zonder vuurspuwen. Meerdere optredens achter elkaar zijn ook mogelijk (maximaal 4). Bekijk de <a href="/locaties-vuurshows-nederland-belgie/" title="geschikt voor vrijwel elke locatie">locaties in Nederland en Belgi&euml;</a>.</p>

<h2>Thema's voor de fakirshow</h2>
<p>De acts van de fakirshow passen perfect bij evenementen met thema's als 1001-nacht, Oosters, sprookjes, magie of carnaval. Wij staan open voor uw idee&euml;n en wensen om de show perfect aan te laten sluiten bij uw evenement. Meer over het fenomeen 'fakir' leest u op <a href="https://nl.wikipedia.org/wiki/Fakir" rel="noopener">Wikipedia</a>.</p>

<h2>Waarom kiezen voor de fakirshow van Vuurspuwer.com?</h2>
<ul>
<li>Professionele en ervaren artiest</li>
<li>Combineerbaar met andere acts van Vuurspuwer.com</li>
<li>Een act vol spanning, sensatie en verwondering</li>
</ul>

<h2>Hoe kan ik een fakirshow boeken?</h2>
<p>Vul het <a href="/contact-3/">contactformulier</a> in en wij nemen binnen 24 uur contact met u op. Na een kort gesprek ontvangt u een gratis en vrijblijvende offerte op maat. Klaar om uw publiek te verrassen en te verbazen? Neem vandaag nog contact op!</p>
""",
  "faq": [],
  "service": {"name": "Fakirshow", "type": "Fakir Performance",
              "desc": "Spannende fakirshow met klassieke acts zoals spijkerbed, glaslopen en extreme demonstraties, veilig uitgevoerd met ervaring en discipline."},
  "fotos": [("fakirshow-640.webp", "fakirshow-640.webp", 640, 1351, "Fakirshow in het theater", "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer"),
            ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Het spijkerbord van dichtbij", "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht"),
            ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Glas en gewicht", "Fakiract: Nuno draagt het gewicht van een staande toeschouwer")],
 },

 "reptielenhow": {
  "title": "Reptielenshow: een onvergetelijke ervaring voor uw evenement",
  "seo_title": "Reptielenshow Boeken – Unieke Act voor Uw Evenement",
  "seo_desc": "Boek de reptielenshow van Nuno voor een onvergetelijke ervaring op uw feest of evenement. Fascinerende reptielen, professioneel verzorgd. Vraag vrijblijvend offerte aan!",
  "eyebrow": "Reptielenshow",
  "img": ("/assets/media/reptiel-960.webp", "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow"),
  "body": """
<p>Bent u op zoek naar een unieke en spannende act voor uw feest, evenement of opening? De <strong>reptielenshow</strong> van Vuurspuwer.com, verzorgd door <a href="/over-nuno/" title="ervaren professional Nuno">Nuno</a>, is een tropische verrassing die uw gasten niet snel zullen vergeten! Overwin uw angsten en maak kennis met fascinerende reptielen.</p>

<h2>Wat kunt u verwachten van onze reptielenshow?</h2>
<p>Onze dynamische reptielenworkshop biedt een interactieve kennismaking met verschillende soorten slangen, vogelspinnen en andere 'griezelige' reptielen. Onder begeleiding van een ervaren professional leren uw gasten op een leuke en veilige manier hun angsten te overwinnen. Stel je voor: uw gasten zitten gezellig aan tafel of lopen ontspannen rond, en plotseling worden ze op een leuke manier geconfronteerd met slangen, spinnen, schorpioenen en een leguaan!</p>
<p>Als uw gasten het leuk vinden om een schorpioen aan te raken of een slang even op de schouder te hebben, is dat geen probleem. Ook spinnen mogen, indien gewenst, vastgehouden worden. Uiteraard gebeurt dit alles onder strikt toezicht en met respect voor de dieren.</p>

<h2>Educatie en entertainment hand in hand</h2>
<p>Tijdens de <strong>slangenshow</strong> worden vragen over de dieren educatief en enthousiast beantwoord. Uw gasten zullen versteld staan van de interessante feiten en weetjes die ze leren. En als kers op de taart krijgen ze na afloop een foto mee als herinnering aan deze bijzondere ervaring!</p>

<h2>Reptielenshow op maat</h2>
<p>Of u nu een slang wilt huren voor een fotoshoot of ge&iuml;nteresseerd bent in een complete reptielenshow: bij Vuurspuwer.com zijn de mogelijkheden bespreekbaar. We passen de act graag aan uw wensen en de aard van uw evenement aan. Wilt u bijvoorbeeld een spectaculaire combinatie met een <a href="/vuurspuwer-inhuren/">vurige vuurspuwer-act</a>? Neem <a href="/contact-3/">contact</a> met ons op om de mogelijkheden te bespreken.</p>

<h2>Een onvergetelijke binnenkomst</h2>
<p>Wilt u een onvergetelijke binnenkomst cre&euml;ren voor uw feest, evenement of opening, waar uw gasten nog lang over napraten? Dan is een reptielenshow de perfecte act! Een unieke en verrassende manier om de aandacht te trekken en een onvergetelijke indruk achter te laten.</p>

<h2>Meer informatie over reptielen</h2>
<p>Wilt u meer weten over de fascinerende wereld van reptielen? Bezoek de <a href="https://nl.wikipedia.org/wiki/Reptielen" rel="noopener nofollow">Wikipedia-pagina over reptielen</a> &mdash; of bekijk de <a href="/">homepagina</a> van Vuurspuwer.com.</p>
""",
  "faq": [],
  "service": {"name": "Reptielenshow", "type": "Educational Reptile Show",
              "desc": "Educatieve en interactieve reptielenshow met exotische dieren. Geschikt voor families, scholen en events: veilig, gecontroleerd en boeiend."},
  "fotos": [("reptiel-900.webp", "reptiel-960.webp", 900, 838, "Boa constrictor tijdens de show", "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow")],
 },

 "halloween": {
  "title": "Halloween vuurshow & horror-fakir boeken",
  "seo_title": "\U0001F383 Halloween Vuurshow & Horror-Fakir Boeken | NL & BE – vanaf €395",
  "seo_desc": "Halloween-act boeken? Duivelse vuurshows, horror-fakirshow en scare-acts — bekend van Walibi Fright Nights. Heel NL & BE, vanaf €395. Oktober loopt vol: boek nu!",
  "eyebrow": "\U0001F383 Oktober · beperkt beschikbaar",
  "img": ("/assets/media/vuurbal-1333.webp", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
  "body": """
<p>Bekend van de <strong>Halloween Fright Nights van Walibi Holland</strong>. Duivelse vuurshows, scare-acts en een horror-fakir die uw gasten laat huiveren &mdash; in heel Nederland en Belgi&euml;.</p>

<h2>Halloween is het seizoen van vuur</h2>
<p>Geen feest past zo perfect bij vuur en duisternis als Halloween. Nuno transformeert voor de gelegenheid tot demon, duivel of horror-fakir: vlammen die uit het donker opdoemen, een spijkerbed-act bij fakkellicht, scare-momenten tussen het publiek en mentalisme dat net iets t&eacute; goed gedachten leest. Elk element wordt afgestemd op uw thema en doelgroep &mdash; van gezinsvriendelijk griezelen tot volwassen horror.</p>
<p>Met optredens op de Halloween Fright Nights van Walibi Holland op zijn cv weet Nuno precies hoe je een grote menigte laat gillen &eacute;n applaudisseren. Maar ook op een spooktocht van de scouting, een horrornacht in de kroeg of een Halloween-bedrijfsfeest maakt hij het verschil.</p>

<h2>Halloween-acts op een rij</h2>
<ul>
<li>\U0001F608 <strong>Duivelse vuurshow</strong> &mdash; vlammen, vonken en vuurzuilen in horror-styling (vanaf &euro;395)</li>
<li>\U0001F5E1️ <strong>Horror-fakirshow</strong> &mdash; spijkerbed, glas en zwaarden in griezelgrime (vanaf &euro;450)</li>
<li>\U0001F441️ <strong>Duister mentalisme</strong> &mdash; gedachten lezen met een onheilspellend randje</li>
<li>\U0001F525 <strong>Complete Halloween-productie</strong> &mdash; meerdere acts verspreid over de avond (vanaf &euro;750)</li>
</ul>

<h2>Vroeg boeken loont</h2>
<p>De weekenden rond 31 oktober zijn elk jaar als eerste vol. Boek bij voorkeur v&oacute;&oacute;r september om zeker te zijn van uw datum; last-minute kan soms, maar de keuze is dan beperkt. <a href="/#boeken">Check direct de beschikbaarheid</a> of app via <a href="https://wa.me/31620020723?text=Hallo%20Nuno%2C%20is%20mijn%20Halloween-datum%20nog%20vrij%3F" rel="noopener">WhatsApp</a>.</p>
""",
  "faq": [
   ("Wat kost een Halloween vuurshow of horror-act?",
    "Halloween-acts boekt u vanaf €395 (vuurshow) of €450 (horror-fakirshow). Een complete Halloween-avondproductie met meerdere acts is mogelijk vanaf €750. Oktober-data zijn beperkt — vroeg boeken loont."),
   ("Welke Halloween-acts zijn er mogelijk?",
    "Duivelse vuurshows, een horror-fakir op spijkerbed en glas, scare-acts tussen het publiek, griezelig mentalisme en combinaties daarvan. Kostuum en grime worden volledig op uw thema afgestemd — van klassieke horror tot demonisch."),
   ("Heeft Nuno ervaring met grote Halloween-events?",
    "Ja. Nuno stond onder meer op de Halloween Fright Nights van Walibi Holland, één van de grootste Halloween-events van de Benelux, naast talloze spooktochten, horrornachten en themafeesten."),
   ("Hoe vroeg moet ik boeken voor Halloween?",
    "De weekenden rond 31 oktober zijn elk jaar als eerste vol. Boek bij voorkeur vóór september om zeker te zijn van uw datum; last-minute kan soms, maar de keuze is dan beperkt."),
  ],
  "service": {"name": "Halloween entertainment", "type": "Halloween entertainment",
              "desc": "Halloween vuurshows, horror-fakiracts en scare-entertainment voor Fright Nights, spooktochten en themafeesten in Nederland en België.",
              "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                         "lowPrice": "395", "highPrice": "1800",
                         "description": "Vanaf-prijs, exclusief reiskosten. Vrijblijvende offerte op maat."}},
  "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal tijdens een nachtshow", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
            ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Horror-fakir: het spijkerbord", "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht"),
            ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Vuur bij het themafeest", "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond")],
 },
}

def show_schema(slug, page):
    svc = page["service"]
    out = [{"@context": "https://schema.org", "@type": "Service",
            "@id": f"{SITE}/{slug}/#service",
            "name": svc["name"], "serviceType": svc["type"],
            "description": svc["desc"], "url": f"{SITE}/{slug}/",
            "image": SITE + page["img"][0],
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Country", "name": "Nederland"},
                           {"@type": "Country", "name": "België"}],
            **({"offers": svc["offers"]} if "offers" in svc else {})}]
    if page["faq"]:
        out.append({"@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [{"@type": "Question", "name": q,
                                    "acceptedAnswer": {"@type": "Answer", "text": a}}
                                   for q, a in page["faq"]]})
    return out

def show_faq_html(page):
    if not page["faq"]:
        return ""
    items = "".join(
        f'<details class="faq__item"><summary>{q}</summary>'
        f'<p>{a}</p></details>' for q, a in page["faq"])
    return ('<section class="wrap bay" aria-label="Veelgestelde vragen">'
            '<div class="bay__head"><p class="eyebrow eyebrow--dim rise">Veelgestelde vragen</p>'
            '<h2 class="bay__title rise" data-delay="1">Eerst even <em>zeker weten</em></h2></div>'
            f'<div class="faq">{items}</div></section>')
