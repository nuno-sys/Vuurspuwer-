"""Eigen inhoud voor de video's-pagina, de drie showpagina's en de
Halloween-pagina. De teksten komen van de live site en zijn opgeschoond
en licht aangescherpt; de webadressen blijven exact gelijk."""
import html as _html
import os, re

SITE = "https://vuurspuwer.com"

def _srcset(thumb):
    """srcset uit de kleinere broertjes (-480 enz.) van een media-bestand."""
    m = re.match(r"([a-z0-9-]+?)-(\d+)\.webp$", thumb)
    if not m: return ""
    base = m.group(1)
    cands = sorted(
        (int(mm.group(1)), f)
        for f in os.listdir("assets/media")
        if (mm := re.match(rf"{re.escape(base)}-(\d+)\.webp$", f)))
    if len(cands) < 2: return ""
    return ", ".join(f"/assets/media/{f} {w}w" for w, f in cands)

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

def _poster(poster):
    """De lichtere 640-variant van een poster, als die bestaat."""
    small = re.sub(r"\.(webp|jpg)$", r"-640.webp", poster)
    return small if os.path.exists(f"assets/media/{small}") else poster

def videos_body():
    tiles = []
    for i, (src, poster, _, cap, alt) in enumerate(VIDEOS):
        ratio = ' data-ratio="9/16"' if "portrait" in src else ""
        tiles.append(f'''<figure class="reel rise"{ratio}>
        <video muted loop playsinline preload="none" poster="/assets/media/{_poster(poster)}"
               data-src="/assets/media/{src}" aria-label="{alt}"><track kind="captions" src="/assets/media/stil.vtt" srclang="nl" label="Geen gesproken tekst"></video>
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
    tiles = []
    for thumb, full, w, h, cap, alt in items:
        ss = _srcset(thumb)
        ss_attr = f' srcset="{ss}" sizes="(max-width:760px) 46vw, 31vw"' if ss else ""
        tiles.append(
            f'<a href="/assets/media/{full}" data-lightbox data-cap="{cap}">'
            f'<img src="/assets/media/{thumb}"{ss_attr} width="{w}" height="{h}" loading="lazy" '
            f'decoding="async" alt="{alt}"></a>')
    return f'<h2>Foto’s uit de show</h2><div class="fgrid">{"".join(tiles)}</div>'

SHOW_PAGES = {
 "workshop-vuurspuwen": {
  "title": "Workshop vuurspuwen",
  "seo_title": "\U0001F525 Workshop Vuurspuwen | Leer Vuurspuwen met Nuno",
  "seo_desc": "Workshop vuurspuwen met professioneel begeleiding van Nuno. Ideaal voor teambuilding, vrijgezellenfeest of bedrijfsfeest. Boek nu uw workshop!",
  "eyebrow": "Workshop",
  "img": ("/assets/media/workshop-1125.webp", "Workshop vuurspuwen onder begeleiding van professioneel vuurspuwer Nuno"),
  "body": """
<h2>Workshop Vuurspuwen: Ontketen het Vuur in Jezelf (en je Team)!</h2>
<p>Droom je ervan om vuur te spuwen? Wil je een onvergetelijke ervaring beleven die tegelijkertijd spannend en leerzaam is? Dan is de workshop vuurspuwen van Nuno, de <a href="/over-nuno/" title="ervaren vuurspuwer en fakir">ervaren vuurspuwer en fakir</a> van Vuurspuwer.com, precies wat je zoekt! Nuno leert je op een veilige en verantwoorde manier de kunst van het vuurspuwen en vuurhappen. Durf jij het aan?</p>
<h3>Waarom een Workshop Vuurspuwen volgen?</h3>
<p>Een workshop vuurspuwen is meer dan alleen een spectaculaire activiteit. Het is een unieke ervaring die perfect is voor:</p>
<ul>
<li><strong>Vrijgezellenfeesten:</strong> geef de aanstaande bruidegom of bruid een vurige start van het huwelijk!</li>
<li><strong>Verjaardagen:</strong> maak je verjaardagsfeest onvergetelijk met een spectaculaire vuurspuwdemonstratie en workshop. Overweeg om een <a href="/vuurspuwer-boeken-voor-een-verjaardag-de-ultieme-spectaculaire-ervaring/">vuurspuwer te boeken voor een verjaardag</a> voor een extra speciale ervaring.</li>
<li><strong>Bedrijfsfeesten:</strong> verras je collega&rsquo;s met een originele en uitdagende activiteit die de teamgeest versterkt.</li>
<li><strong>Verenigingen en Chirogroepen:</strong> zorg voor een avond vol spanning, sensatie en onvergetelijke momenten.</li>
<li><strong>Teambuilding:</strong> verbeter de samenwerking en het vertrouwen binnen je team op een unieke en uitdagende manier.</li>
</ul>
<h3>Veiligheid staat voorop!</h3>
<p>Bij Vuurspuwer.com staat veiligheid altijd voorop. Nuno leert je niet alleen de technieken van het vuurspuwen, maar ook alles over de veiligheidsmaatregelen. Je leert over de juiste brandstoffen, de benodigde beschermende kleding en hoe je risico&rsquo;s kunt minimaliseren. Nuno zorgt ervoor dat je je comfortabel en zelfverzekerd voelt voordat je begint met vuurspuwen. Meer informatie over vuurspuwen vind je op <a href="https://nl.wikipedia.org/wiki/Vuurspuwen" rel="noopener">Wikipedia</a>.</p>
<h3>Voor Beginners en Gevorderden</h3>
<p>Of je nu nog nooit vuur hebt aangeraakt of al enige ervaring hebt, de workshop vuurspuwen is geschikt voor iedereen. Nuno past de workshop aan aan jouw niveau en wensen. Beginners worden stap voor stap begeleid, terwijl gevorderden nieuwe technieken en trucs leren om hun vaardigheden te verbeteren.</p>
<h3>Teambuilding met Vuur: Versterk de Band!</h3>
<p>Vuurspuwen is een perfecte teambuildingactiviteit. Het vereist samenwerking, communicatie en vertrouwen. Door samen te leren vuurspuwen, versterken collega&rsquo;s, vrienden of clubleden hun band en cre&euml;ren ze een onvergetelijke ervaring. Een <a href="/vuurspuwer-inhuren/">vuurspuwer inhuren</a> kan ook een geweldige manier zijn om de teamgeest te versterken.</p>
<h3>Maatwerk Workshop Vuurspuwen</h3>
<p>De workshop vuurspuwen kan volledig worden aangepast aan jouw specifieke wensen en behoeften. Of je nu een korte demonstratie wilt of een volledige cursus, Nuno staat klaar om aan je verwachtingen te voldoen. De workshop kan zowel op locatie als op een <a href="/locaties-vuurshows-nederland-belgie/" title="op een door jou gekozen externe locatie">door jou gekozen externe locatie</a> worden georganiseerd. Neem <a href="/contact-3/">contact</a> op om de mogelijkheden te bespreken.</p>
<h3>Boek nu jouw Onvergetelijke Vuurspuw Experience!</h3>
<p>Wacht niet langer en plan vandaag nog jouw onvergetelijke workshop vuurspuwen met Nuno! Ontdek de sensatie van vuurhappen en verleg je grenzen. Neem <a href="/contact-3/">contact</a> op met Nuno via Vuurspuwer.com en maak van jouw evenement een vurig succes!</p>
""",
  "faq": [
   ("Is de workshop vuurspuwen veilig?",
    "Ja. Veiligheid staat altijd voorop: je leert eerst alles over de juiste brandstoffen, beschermende kleding en het minimaliseren van risico's, en oefent stap voor stap onder professionele begeleiding van Nuno."),
   ("Voor wie is de workshop geschikt?",
    "Voor iedereen vanaf 18 jaar, van complete beginners tot gevorderden. De workshop wordt aangepast aan het niveau en de wensen van de groep — ideaal voor vrijgezellenfeesten, verjaardagen, bedrijfsfeesten en teambuilding."),
   ("Waar kan de workshop plaatsvinden?",
    "Zowel op locatie als op een door jou gekozen externe plek in Nederland of België, mits er buiten voldoende vrije ruimte is. Nuno neemt alle materialen mee."),
   ("Wat kost een workshop vuurspuwen?",
    "De prijs hangt af van de groepsgrootte, duur en locatie. Vraag vrijblijvend een offerte aan via het contactformulier, telefoon of WhatsApp — je ontvangt binnen 24 uur een voorstel op maat."),
  ],
  "service": {"name": "Workshop vuurspuwen", "type": "Workshop / Teambuilding",
              "desc": "Workshop vuurspuwen met professionele begeleiding van Nuno. Veilig leren vuurspuwen en vuurhappen — ideaal voor teambuilding, vrijgezellenfeesten en bedrijfsfeesten."},
  "fotos": [("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Vuurspuwen tegen de avondlucht", "Vuurspuwer blaast een grote vuurbal tegen de avondlucht vanaf een balustrade"),
            ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Vuurbal in de avondschemering", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
            ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Vuurshow bij daglicht", "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe")],
 },

 "over-nuno": {
  "title": "Over Vuurspuwer & Fakir Nuno: 17 jaar meesterschap",
  "seo_title": "\U0001F525 Vuurspuwer & Fakir Nuno | 17 Jaar Meesterschap",
  "seo_desc": "Vuurspuwer en fakir Nuno: 17 jaar ervaring als entertainer in Nederland en België. Vuurshow, fakirshow, mentalist én reptielenshow. Vraag vrijblijvend een offerte aan!",
  "eyebrow": "Over Nuno",
  "img": ("/assets/media/mentalist-1371.webp", "Nuno op het podium van een theaterzaal"),
  "body": """
<p><strong>Vuurspuwer en fakir Nuno is al meer dan 17 jaar een van de meest ervaren entertainers van Nederland en Belgi&euml;. Vuurspuwer, fakir, mentalist &eacute;n reptielenshow-artiest: Nuno combineert vakmanschap met spektakel en laat bij elk optreden een blijvende indruk achter.</strong></p>
<h2>Over Vuurspuwer &amp; Fakir Nuno: 17 Jaar Meesterschap in Entertainment</h2>
<p>Welkom in een wereld vol adrenaline, passie en pure magie. Ik ben Nuno, en al meer dan 17 jaar verleg ik grenzen op het podium. Wat begon als een fascinatie voor vuur, is uitgegroeid tot een internationale carri&egrave;re als professioneel <strong>vuurspuwer</strong> en fakir. Van spectaculaire <a href="https://nl.wikipedia.org/wiki/Vuurspuwen" rel="noopener">vuurshows</a> op festivals tot mysterieuze optredens in videoclips en op nationale televisie: mijn doel is altijd om een onvergetelijke indruk achter te laten.</p>
<h2>Van Nationale TV-Studio&rsquo;s tot Internationale Podia</h2>
<p>Mijn reis heeft mij op plekken gebracht waar weinigen komen. Met optredens voor zenders als SBS6, RTL, VTM en producties in Engeland, heb ik bewezen dat entertainment meer is dan een act; het is vakmanschap. Of het nu gaat om een intiem huwelijk, een grootschalig bedrijfsfeest of een dynamische festivalset in Nederland of Belgi&euml;, ik breng een niveau van professionaliteit en spektakel dat wordt erkend. Wilt u ook een onvergetelijk evenement? Neem dan <a href="/contact-3/">contact</a> op.</p>
<h3>Vuurspuwer Nuno: De Kunst van het Onmogelijke</h3>
<p>Als fakir en mentalist draait mijn werk om de kracht van de geest over het lichaam. Het verleggen van de pijngrens en het beheersen van mentale krachten staan centraal in mijn shows. Ik beheers verschillende disciplines:</p>
<ul>
<li><strong>Vuurmeesterschap:</strong> metershoge vlammen en uiterste precisie.</li>
<li><strong>Fakir-technieken:</strong> het trotseren van glas en spijkerbedden met totale mentale controle.</li>
<li><strong>Passie voor Perfectie:</strong> elke show is 100% veilig, professioneel en afgestemd op de locatie.</li>
</ul>
<p>Entertainment zit in mijn bloed. De passie voor het publiek en de kick van het onmogelijke drijven mij om mijn acts naar een hoger niveau te tillen. Als u Nuno wilt <a href="/vuurspuwer-inhuren/">inhuren</a>, kiest u voor bijna twee decennia aan ervaring, passie en de garantie op een &lsquo;WOW-factor&rsquo;.</p>
<h2>Beleef de Kracht van Vuur en Magie Zelf</h2>
<p>Bent u klaar om uw evenement naar een ongekend niveau te tillen? Of u nu een <a href="/vuurspuwer-inhuren/"><strong>vuurshow</strong></a> wilt boeken voor een opening, een <a href="/fakir-show-inhuren/">fakir-act</a> voor een themafeest of een interactieve <a href="/workshop-vuurspuwen/">workshop</a>: ik denk graag met u mee om uw visie werkelijkheid te maken.</p>
<p>Laten we samen iets legendarisch cre&euml;ren. <a href="/contact-3/">Vraag direct een vrijblijvende offerte aan!</a></p>
""",
  "faq": [],
  "service": None,
  "extra_ld": [{"@context": "https://schema.org", "@type": "AboutPage",
                "@id": f"{SITE}/over-nuno/#about",
                "url": f"{SITE}/over-nuno/",
                "name": "Over Vuurspuwer & Fakir Nuno",
                "mainEntity": {"@id": f"{SITE}/#nuno"},
                "about": {"@id": f"{SITE}/#business"}},
               {"@context": "https://schema.org", "@type": "Person",
                "@id": f"{SITE}/#nuno", "name": "Nuno",
                "alternateName": "Vuurspuwer Nuno",
                "jobTitle": "Vuurspuwer, fakir, mentalist en reptielenshow-artiest",
                "description": "Professioneel vuurspuwer en fakir met 17 jaar ervaring, bekend van SBS6, RTL, VTM en producties in Engeland.",
                "image": {"@type": "ImageObject",
                          "url": f"{SITE}/assets/media/nuno-avatar.webp",
                          "width": 288, "height": 288,
                          "caption": "Portret van vuurspuwer Nuno"},
                "url": f"{SITE}/over-nuno/",
                "sameAs": ["https://www.facebook.com/show.nuno",
                           "https://www.instagram.com/officialnuno",
                           "https://x.com/mentalist_nuno"],
                "worksFor": {"@id": f"{SITE}/#business"},
                "knowsAbout": ["Vuurspuwen", "Fakirshow", "Mentalisme", "Reptielenshow", "Workshop vuurspuwen"]}],
  "fotos": [("mentalist-900.webp", "mentalist-1371.webp", 900, 900, "Mentalist Nuno in het theater", "Nuno op het podium van een lege theaterzaal voor een mentalismeshow"),
            ("festival-900.webp", "festival-1600.webp", 900, 902, "Vuurshow op een festivalplein", "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek"),
            ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Fakiract met glas en gewicht", "Fakiract: Nuno draagt het gewicht van een staande toeschouwer")],
 },

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
  "seo_title": "\U0001F383 Halloween Vuurshow & Horror-Fakir Boeken | NL & BE – vanaf €350",
  "seo_desc": "Halloween-act boeken? Duivelse vuurshows, horror-fakirshow en scare-acts — bekend van Walibi Fright Nights. Heel NL & BE, vanaf €350. Oktober loopt vol: boek nu!",
  "eyebrow": "\U0001F383 Oktober · beperkt beschikbaar",
  "img": ("/assets/media/vuurbal-1333.webp", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
  "body": """
<p>Bekend van de <strong>Halloween Fright Nights van Walibi Holland</strong>. Duivelse vuurshows, scare-acts en een horror-fakir die uw gasten laat huiveren &mdash; in heel Nederland en Belgi&euml;.</p>

<h2>Halloween is het seizoen van vuur</h2>
<p>Geen feest past zo perfect bij vuur en duisternis als Halloween. Nuno transformeert voor de gelegenheid tot demon, duivel of horror-fakir: vlammen die uit het donker opdoemen, een spijkerbed-act bij fakkellicht, scare-momenten tussen het publiek en mentalisme dat net iets t&eacute; goed gedachten leest. Elk element wordt afgestemd op uw thema en doelgroep &mdash; van gezinsvriendelijk griezelen tot volwassen horror.</p>
<p>Met optredens op de Halloween Fright Nights van Walibi Holland op zijn cv weet Nuno precies hoe je een grote menigte laat gillen &eacute;n applaudisseren. Maar ook op een spooktocht van de scouting, een horrornacht in de kroeg of een Halloween-bedrijfsfeest maakt hij het verschil.</p>

<h2>Halloween-acts op een rij</h2>
<ul>
<li>\U0001F608 <strong>Duivelse vuurshow</strong> &mdash; vlammen, vonken en vuurzuilen in horror-styling (vanaf &euro;350)</li>
<li>\U0001F5E1️ <strong>Horror-fakirshow</strong> &mdash; spijkerbed, glas en zwaarden in griezelgrime (vanaf &euro;450)</li>
<li>\U0001F441️ <strong>Duister mentalisme</strong> &mdash; gedachten lezen met een onheilspellend randje</li>
<li>\U0001F525 <strong>Complete Halloween-productie</strong> &mdash; meerdere acts verspreid over de avond (vanaf &euro;750)</li>
</ul>

<h2>Vroeg boeken loont</h2>
<p>De weekenden rond 31 oktober zijn elk jaar als eerste vol. Boek bij voorkeur v&oacute;&oacute;r september om zeker te zijn van uw datum; last-minute kan soms, maar de keuze is dan beperkt. <a href="/#boeken">Check direct de beschikbaarheid</a> of app via <a href="https://wa.me/31620020723?text=Hallo%20Nuno%2C%20is%20mijn%20Halloween-datum%20nog%20vrij%3F" rel="noopener">WhatsApp</a>.</p>
""",
  "faq": [
   ("Wat kost een Halloween vuurshow of horror-act?",
    "Halloween-acts boekt u vanaf €350 (vuurshow) of €450 (horror-fakirshow). Een complete Halloween-avondproductie met meerdere acts is mogelijk vanaf €750. Oktober-data zijn beperkt — vroeg boeken loont."),
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
                         "lowPrice": "350", "highPrice": "1500", "offerCount": "3",
                         "description": "Vanaf-prijs, exclusief reiskosten. Vrijblijvende offerte op maat."}},
  "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Vuurbal tijdens een nachtshow", "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer"),
            ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Horror-fakir: het spijkerbord", "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht"),
            ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Vuur bij het themafeest", "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond")],
 },
}

def show_schema(slug, page):
    svc = page["service"]
    out = []
    if svc:
        out.append({"@context": "https://schema.org", "@type": "Service",
            "@id": f"{SITE}/{slug}/#service",
            "name": svc["name"], "serviceType": svc["type"],
            "description": svc["desc"], "url": f"{SITE}/{slug}/",
            "image": SITE + page["img"][0],
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "Country", "name": "Nederland"},
                           {"@type": "Country", "name": "België"}],
            **({"offers": svc["offers"]} if "offers" in svc else {})})
    if page.get("extra_ld"):
        out.extend(page["extra_ld"])
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

# ------------------------------------------------------------- beoordelingen
# De echte reviews van het Google-profiel, zoals aangeleverd van de
# live reviewspagina: 4,9 uit 136 beoordelingen, hieronder de 30 uitgelichte.
GOOGLE_PROFILE = "https://share.google/2S3Fcj7r3VXT3VtbB"
RATING = {"value": "4.9", "count": "136"}
REVIEWS = [
 ("Silke van Dam", "Amsterdam", "Wat een magisch optreden van Vuurspuwer Nuno in Amsterdam! Het vuurspuwen was professioneel en het publiek was muisstil van spanning. Een onvergetelijke avond."),
 ("Eva Smit", "Amsterdam", "Vuurspuwer Nuno leverde een hypnotiserende performance in Amsterdam. Van gevaarlijke stunts tot de spannende climax — ideaal voor feesten en events."),
 ("Bas van der Linden", "Antwerpen", "Wat een talent! Nuno's show in Antwerpen met perfect vuurspuwen en mystieke elementen was puur genot. 10/10!"),
 ("Stijn Claes", "Antwerpen", "Geweldige fakir- en vuurperformance van Nuno in Antwerpen. Elke stunt werd met precisie uitgevoerd. Topentertainment!"),
 ("Joke Vermeulen", "Utrecht", "Wat een talent! Nuno's show in Utrecht met indrukwekkend vuurspuwen en mystieke elementen was puur genot. 10/10!"),
 ("Nina Peters", "Utrecht", "Geweldige fakir- en vuurperformance van Nuno in Utrecht. Een mix van gevaar en schoonheid die ons betoverde. Topentertainment!"),
 ("Wim Verhoeven", "Gent", "Vuurspuwer Nuno maakte indruk met zijn opwindende fakirtrucs tijdens het event in Gent. Alles was perfect getimed en magisch. 5 sterren waard!"),
 ("Pieter van Dijk", "Gent", "Nuno leverde een adembenemende performance in Gent. Van lichaamskunsten tot de spannende climax — betoverend."),
 ("Nina Peters", "Tilburg", "Vuurspuwer Nuno maakte indruk met zijn intense circusachtige show tijdens het event in Tilburg. Perfect getimed en adembenemend. 5 sterren!"),
 ("Femke Hoekstra", "Tilburg", "Indrukwekkend en perfect was het optreden van Vuurspuwer Nuno in Tilburg. Een must-see voor avontuurlijke geesten!"),
 ("Joke Vermeulen", "Brussel", "Nuno maakte indruk met zijn verrassende lichaamskunsten tijdens het event in Brussel. De fakirshow was het hoogtepunt. 5 sterren waard!"),
 ("Sara Peeters", "Brussel", "Briljant optreden in Brussel met Nuno's perfecte fakirkunsten en vuuracts. Een unieke ervaring die ik niet snel vergeet."),
 ("Lien de Smet", "Eindhoven", "Vuurspuwer Nuno leverde een briljante performance in Eindhoven. Van stunts tot de spannende climax, alles was professioneel. Betoverend gedaan!"),
 ("Femke Hoekstra", "Eindhoven", "Nuno maakte indruk met zijn hypnotiserende fakirtrucs tijdens het event in Eindhoven. Alles was perfect getimed en indrukwekkend."),
 ("Femke Hoekstra", "Leuven", "Wat een opwindend optreden van Vuurspuwer Nuno in Leuven! Het publiek was muisstil van spanning. Echt een aanrader!"),
 ("Rik van den Berg", "Leuven", "Wat een talent! Nuno's show in Leuven met spannend vuurspuwen en mystieke elementen was puur genot. 10/10!"),
 ("Silke van Dam", "Groningen", "Wat een ongelooflijk optreden van Vuurspuwer Nuno in Groningen! De fakirtrucs waren spectaculair en het publiek was muisstil van spanning."),
 ("Tom Hendrikx", "Groningen", "Briljant optreden in Groningen met Nuno's fakirkunsten en vuuracts. Een unieke ervaring die ik niet snel vergeet."),
 ("Bram van der Velde", "Rotterdam", "Vuurspuwer Nuno maakte indruk met zijn verrassende circusachtige show tijdens het event in Rotterdam. Alles was perfect getimed. 5 sterren waard!"),
 ("Tom Hendrikx", "Rotterdam", "Wat een talent! Nuno's show in Rotterdam met ongelooflijk vuurspuwen en mystieke elementen was puur genot. 10/10!"),
 ("Lien de Smet", "Nijmegen", "Wat een talent! Nuno's show in Nijmegen met spectaculair vuurspuwen en mystieke elementen was puur genot. 10/10!"),
 ("Jeroen Claes", "Nijmegen", "Geweldige fakir- en vuurperformance van Nuno in Nijmegen. Een mix van gevaar en schoonheid die ons betoverde. Topentertainment!"),
 ("Mark de Groot", "Den Haag", "Vuurspuwer Nuno maakte indruk met zijn adembenemende circusachtige show tijdens het event in Den Haag. De fakirshow was het hoogtepunt."),
 ("Lotte de Boer", "Den Haag", "Nuno als Vuurspuwer in Den Haag was fantastisch. Professioneel en veilig, ondanks de risico's. Sterk aanbevolen!"),
 ("Stijn Claes", "Breda", "Nuno maakte indruk met zijn professionele mystieke performance tijdens het event in Breda. De fakirshow was het hoogtepunt. 5 sterren waard!"),
 ("Eva Smit", "Breda", "Incredibel! Nuno's vuurshow in Breda was creatief en vol adrenaline. Zijn beheersing over het vuur is indrukwekkend."),
 ("Annelies Dubois", "Almere", "Nuno maakte indruk met zijn professionele acts tijdens het event in Almere. Alles was perfect getimed en ongelooflijk. 5 sterren waard!"),
 ("Tessa van Wijk", "Almere", "Wat een talent! Nuno's show in Almere met ontzagwekkend vuurspuwen was puur genot. 10/10!"),
 ("Pieter van Dijk", "Apeldoorn", "Vuurspuwer Nuno leverde een magische performance in Apeldoorn. Van fakiracts tot de spannende climax — fascinerend gedaan!"),
 ("Silke van Dam", "Apeldoorn", "Nuno als Vuurspuwer in Apeldoorn was fantastisch. Professioneel en veilig, ondanks de risico's. Sterk aanbevolen!"),
]

# de allernieuwste Google-reviews: prominent bovenaan met een NIEUW-badge
# en een levende "x geleden"-tijd — site.js rekent die bij elk bezoek
# opnieuw uit, en laat de badge na 45 dagen vanzelf verdwijnen
NEW_REVIEWS = [
 ("EL Mul", "Local Guide", "2026-08-31", "review-elmul", (480, 543),
  "Wil je een spectaculaire show met een flinke dosis humor, liters spanning en een portie &bdquo;drakenadem&rdquo; waar je wenkbrauwen spontaan van gaan krullen? Dan ben je bij Nuno aan het juiste adres! Een absolute knaller! Je gasten praten er dagen later nog over&hellip; met sterren in hun ogen &eacute;n waarschijnlijk een lichte rookgeur in hun kleding. 😂✨"),
 ("Henk Mulder", "Local Guide", "2026-08-31", "review-henk", (480, 246),
  "Super leuke ervaring! Nuno neemt zijn hele publiek mee in een geweldige show vol grappen en echte spectaculaire stunts. Nooit verwacht om zelf nog eens vuur te mogen spuwen, heel erg bedankt voor de mooie ervaring!"),
 ("Lisanne", "Google", "2026-08-17", "review-lisanne", (480, 188),
  "Aardige man, zorgt voor een spectaculaire show! Waar veel mensen naar blijven kijken en steeds meer willen zien! ☄️🔥💥"),
]

def new_review_cards(badge="NIEUW", ago="augustus 2026", lang_attr="",
                     proof="📸 Origineel van Google", proof_alt="Originele Google-review van"):
    out = []
    for i, (n, meta, d, img, (iw, ih), t) in enumerate(NEW_REVIEWS):
        delay = f' data-delay="{i}"' if i else ""
        out.append(
            f'<article class="rcard rcard--new rise"{delay}{lang_attr}>'
            f'<p class="rcard__stars" aria-label="5 van de 5 sterren">★★★★★'
            f'<span class="rcard__new" data-rev-new data-rev-date="{d}">{badge}</span></p>'
            f'<blockquote><p>&ldquo;{t}&rdquo;</p></blockquote>'
            f'<footer class="rcard__who">{n} <span>&middot; {meta}</span>'
            f'<time class="rcard__ago" data-rev-date="{d}" datetime="{d}">{ago}</time></footer>'
            f'<a class="rcard__proof" href="/assets/media/{img}-900.webp" data-lightbox>'
            f'<img src="/assets/media/{img}-480.webp" '
            f'srcset="/assets/media/{img}-480.webp 480w, /assets/media/{img}-900.webp 900w" '
            f'sizes="(max-width:760px) 86vw, 350px" width="{iw}" height="{ih}" '
            f'loading="lazy" decoding="async" alt="{proof_alt} {n}">'
            f'<span class="rcard__prooftag">{proof}</span></a></article>')
    return "".join(out)

def reviews_body():
    cards = new_review_cards() + "".join(
        f'<article class="rcard"><p class="rcard__stars" aria-label="5 van de 5 sterren">'
        f'★★★★★</p><blockquote><p>{t}</p></blockquote>'
        f'<footer class="rcard__who">{n} <span>&middot; {c}</span></footer></article>'
        for n, c, t in REVIEWS)
    return f'''
<div class="rkop">
  <span class="rkop__cijfer">{RATING["value"].replace(".", ",")}</span>
  <div class="rkop__rechts">
    <span class="rkop__sterren" aria-hidden="true">★★★★★</span>
    <small>gebaseerd op {RATING["count"]} beoordelingen</small>
    <a href="{GOOGLE_PROFILE}" rel="noopener">Bekijk het Google-profiel &rsaquo;</a>
  </div>
</div>
<p>Opdrachtgevers uit heel Nederland en Belgi&euml; over de vuurshows, fakirshows en
workshops van Nuno &mdash; van Amsterdam tot Antwerpen en van Groningen tot Brussel.</p>
<div class="rgrid">{cards}</div>
<p>Alle beoordelingen lezen? Bekijk het volledige overzicht op het
<a href="{GOOGLE_PROFILE}" rel="noopener">Google-profiel van Vuurspuwer Nuno</a>.
Zelf zo&rsquo;n ervaring beleven? <a href="/contact-3/">Vraag een vrijblijvende offerte aan</a>.</p>
'''

def reviews_schema():
    return [{"@context": "https://schema.org", "@type": "LocalBusiness",
             "@id": f"{SITE}/#business",
             "name": "Vuurspuwer Nuno", "url": f"{SITE}/",
             "aggregateRating": {"@type": "AggregateRating",
                                 "ratingValue": RATING["value"],
                                 "reviewCount": RATING["count"],
                                 "bestRating": "5", "worstRating": "1"},
             "review": [{"@type": "Review",
                         "author": {"@type": "Person", "name": n},
                         "datePublished": d,
                         "reviewRating": {"@type": "Rating", "ratingValue": "5",
                                          "bestRating": "5"},
                         "reviewBody": _html.unescape(t),
                         "itemReviewed": {"@id": f"{SITE}/#business"}}
                        for n, _m, d, _img, _wh, t in NEW_REVIEWS]
                       + [{"@type": "Review",
                           "author": {"@type": "Person", "name": n},
                           "reviewRating": {"@type": "Rating", "ratingValue": "5",
                                            "bestRating": "5"},
                           "reviewBody": t,
                           "itemReviewed": {"@id": f"{SITE}/#business"}}
                          for n, _, t in REVIEWS]}]

# ------------------------------------------------------------------ contact
def contact_body():
    return '''
<p>Samenwerken met Nuno? Of het nu gaat om een <a href="/vuurspuwer-inhuren/">vuurshow</a>,
<a href="/fakir-show-inhuren/">fakirshow</a>, <a href="/workshop-vuurspuwen/">workshop
vuurspuwen</a>, <a href="/reptielenhow/">reptielenshow</a> of een complete
<a href="/halloween/">Halloween-productie</a>: vertel kort wat je viert, waar en wanneer
&mdash; dan hoor je <strong>binnen 24 uur</strong> of de datum vrij is, met een
vrijblijvende offerte op maat.</p>
'''

CONTACT_FORM = '''
<section class="wrap bay" aria-label="Direct contact en aanvraagformulier">
  <div class="book">
    <div class="contact rise">
      <div class="contact__line">
        <span class="eyebrow eyebrow--dim">Telefoon &mdash; ma t/m za, 9:00&ndash;18:00</span>
        <b><a href="tel:+31620020723">+31 6 200 207 23</a></b>
      </div>
      <div class="contact__line">
        <span class="eyebrow eyebrow--dim">Vast / zakelijk</span>
        <b><a href="tel:+31852033547">+31 85 203 35 47</a></b>
      </div>
      <div class="contact__line">
        <span class="eyebrow eyebrow--dim">WhatsApp</span>
        <b><a href="https://wa.me/31620020723?text=Hallo%20Nuno%2C%20is%20mijn%20datum%20nog%20vrij%3F" rel="noopener">Stuur een bericht</a></b>
      </div>
      <div class="contact__line">
        <span class="eyebrow eyebrow--dim">Mail</span>
        <b><a href="mailto:nuno@vuurspuwer.com">nuno@vuurspuwer.com</a></b>
      </div>
      <div class="contact__line">
        <span class="eyebrow eyebrow--dim">Werkgebied</span>
        <b>Nederland, Belgi&euml; &amp; internationaal</b>
      </div>
      <p class="form__note">Voor een datum binnen twee weken: bel of app even, dan gaat het sneller dan mail.</p>
    </div>

    <form class="form rise" data-delay="1" id="bookForm" novalidate>
      <input type="hidden" name="lang" value="nl">
      <div class="form__row">
        <label class="field"><span>Naam</span><input type="text" name="naam" autocomplete="name" required></label>
        <label class="field"><span>E-mail</span><input type="email" name="email" autocomplete="email" required></label>
      </div>
      <div class="form__row">
        <label class="field"><span>Telefoon (optioneel)</span><input type="tel" name="telefoon" autocomplete="tel"></label>
        <label class="field"><span>Datum van het evenement</span><input type="date" name="datum"></label>
      </div>
      <div class="form__row">
        <label class="field"><span>Welke show?</span>
          <select name="act">
            <option>Weet ik nog niet</option>
            <option>Vuurshow</option>
            <option>Fakirshow</option>
            <option>Workshop vuurspuwen</option>
            <option>Reptielenshow</option>
            <option>Halloween-act</option>
            <option>Mentalisme</option>
            <option>Themafeest / combinatie</option>
          </select>
        </label>
        <label class="field"><span>Binnen of buiten</span>
          <select name="ruimte">
            <option>Buiten</option>
            <option>Binnen</option>
            <option>Allebei</option>
          </select>
        </label>
      </div>
      <label class="field"><span>Locatie</span><input type="text" name="locatie" placeholder="Plaats of zaal, bijv. Utrecht of De Vereeniging"></label>
      <label class="field"><span>Vertel kort over het evenement</span><textarea name="bericht" rows="4" placeholder="Bijv. bedrijfsfeest voor 80 personen, show rond 21:00 uur"></textarea></label>
      <label class="hp" aria-hidden="true"><span>Website</span><input type="text" name="website" tabindex="-1" autocomplete="off"></label>

      <div class="status" id="formStatus" hidden role="status"></div>

      <div>
        <button class="btn" type="submit"><span class="btn__dot"></span>Verstuur aanvraag</button>
      </div>
      <p class="form__note">Je ontvangt direct een bevestiging per e-mail &mdash; en binnen 24 uur een persoonlijke reactie.</p>
    </form>
  </div>
</section>
'''

def contact_schema():
    return [{"@context": "https://schema.org", "@type": "ContactPage",
             "@id": f"{SITE}/contact-3/#contact",
             "url": f"{SITE}/contact-3/",
             "name": "Contact — Vuurspuwer Nuno",
             "about": {"@id": f"{SITE}/#business"},
             "mainEntity": {"@id": f"{SITE}/#business"}}]

# ------------------------------------------------------------- prijzenpagina
PRIJZEN = {
 "title": "Wat kost een vuurspuwer inhuren?",
 "seo_title": "\U0001F4B6 Wat Kost een Vuurspuwer Inhuren? Prijzen & Pakketten 2026",
 "seo_desc": "Vuurspuwer inhuren vanaf €350. Bekijk alle prijzen en pakketten: van 10 minuten power-act tot complete festivalshow (€350–€1500), incl. uitleg over reiskosten. Transparant en all-in.",
 "eyebrow": "Prijzen & pakketten",
 "img": ("/assets/media/avondvuur-1080.webp", "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering"),
 "body": """
<p><strong>Een vuurspuwer inhuren kost bij Nuno tussen de €350 en €1500, afhankelijk van de showduur en het pakket. Op deze pagina zie je precies wat elke show kost, wat er is inbegrepen en hoe reiskosten werken — transparant en zonder verrassingen.</strong></p>

<h2>Prijzen vuurshow 2026: overzicht per pakket</h2>
<p>In de markt lopen prijzen voor een "vuurshow" uiteen van zo'n €400 tot ruim €6000, omdat onder die naam van alles wordt verkocht — van een enkele fakkel tot complete producties. Nuno werkt met heldere pakketten en een vanafprijs van €350:</p>
<table class="ptable">
<thead><tr><th>Pakket</th><th>Duur</th><th>Indicatie</th><th>Perfect voor</th></tr></thead>
<tbody>
<tr><td><strong>Power-act</strong></td><td>10 min</td><td>vanaf €350</td><td>Opening of grande finale, productlancering</td></tr>
<tr><td><strong>Showblok</strong></td><td>20 min</td><td>vanaf €450</td><td>Bruiloften, verjaardagen, jubilea, bedrijfsfeesten</td></tr>
<tr><td><strong>Volledige vuurshow</strong></td><td>30 min</td><td>vanaf €595</td><td>Themafeesten en gala's, met fakir-elementen en interactie</td></tr>
<tr><td><strong>Festivalpakket</strong></td><td>tot 5 × 20 min</td><td>€950 – €1500</td><td>Festivals en meerdaagse evenementen, verspreid over de dag of avond</td></tr>
</tbody>
</table>
<p><em>Alle bedragen zijn indicaties exclusief reiskosten; je ontvangt altijd eerst een vrijblijvende offerte op maat met één all-in totaalprijs.</em></p>

<h2>Wat is er bij de prijs inbegrepen?</h2>
<ul>
<li><strong>Alles voor de show</strong> — professioneel materiaal, veilige showbrandstoffen, kostuums en op- en afbouw.</li>
<li><strong>Veiligheid geregeld</strong> — Nuno werkt volledig gecertificeerd, binnen de vergunningseisen en met de voorgeschreven veiligheidsafstanden; dit stemt hij vooraf met de locatie af.</li>
<li><strong>Overleg en maatwerk</strong> — vooraf afstemming over muziek, timing en het programma, zodat de show naadloos in jouw evenement past.</li>
<li><strong>Eén aanspreekpunt</strong> — je boekt rechtstreeks bij de artiest, zonder bureau-marges.</li>
</ul>

<h2>Reiskosten</h2>
<p>Nuno reist vanuit Zeist (regio Utrecht) door heel <a href="/locaties-vuurshows-nederland-belgie/">Nederland en België</a>. Reiskosten worden per kilometer berekend en staan altijd vooraf in de offerte — binnen Nederland meestal tussen de €25 en €75, voor België iets meer. Verder weg of internationaal? Ook dat kan, op aanvraag.</p>

<h2>Waarvan hangt de prijs af?</h2>
<ul>
<li><strong>Duur en aantal optredens</strong> — één power-act is voordeliger dan vijf showblokken op een festivaldag.</li>
<li><strong>Type act</strong> — een <a href="/vuurspuwer-inhuren/">vuurshow</a>, <a href="/fakir-show-inhuren/">fakirshow</a>, <a href="/reptielenhow/">reptielenshow</a> of combinatie; een <a href="/entertainer-huren/">mentalisme-act</a> kan ook binnen waar vuur niet mag.</li>
<li><strong>Duo of solo</strong> — samen met een vuurdanseres wordt de show groter (en het budget iets ruimer).</li>
<li><strong>Datum en seizoen</strong> — <a href="/halloween/">oktober (Halloween)</a> en december zijn topmaanden: vroeg boeken loont.</li>
<li><strong>Locatie</strong> — afstand en bijzondere wensen van de venue.</li>
</ul>

<h2>Voorbeelden uit de praktijk</h2>
<ul>
<li><strong>Bruiloft in Amsterdam</strong> — showblok van 20 minuten als avondopener: rond de €500 all-in.</li>
<li><strong>Bedrijfsfeest in Eindhoven</strong> — volledige vuurshow van 30 minuten met fakir-finale: rond de €650 all-in.</li>
<li><strong>Festival in Antwerpen</strong> — vier optredens van 20 minuten verspreid over de avond: rond de €1250 all-in.</li>
</ul>
<p>Twijfel je welk pakket past? Stuur je datum en locatie via het <a href="/contact-3/">aanvraagformulier</a> — binnen 24 uur weet je of de datum vrij is, mét prijsvoorstel. Liever direct contact? Bel of app <a href="https://wa.me/31620020723" rel="noopener">+31 6 200 207 23</a>.</p>

<h2>Waarom opdrachtgevers voor Nuno kiezen</h2>
<p>Met <a href="/over-nuno/">17 jaar ervaring</a>, tv-optredens bij SBS6, RTL en VTM, de Walibi Fright Nights op zijn naam en <a href="/beoordelingen/">een 4,9 uit 136 beoordelingen</a> weet je precies wat je in huis haalt. Bekijk de <a href="/fotos/">foto's</a> en <a href="/videos/">video's</a> voor een voorproefje.</p>
""",
 "faq": [
  ("Wat kost een vuurspuwer voor een bruiloft of verjaardag?",
   "Voor bruiloften, verjaardagen, jubilea en bedrijfsfeesten is het showblok van 20 minuten het populairst: vanaf €450, exclusief reiskosten. Een korte power-act van 10 minuten kan al vanaf €350."),
  ("Wat kost een vuurshow op een festival?",
   "Voor festivals is er een pakket tot vijf optredens van 20 minuten, verspreid over de dag of avond: €950 tot €1500 all-in, afhankelijk van het aantal sets en de reisafstand."),
  ("Zijn er nog bijkomende kosten?",
   "Alleen reiskosten (per kilometer vanaf Zeist, meestal €25–€75 binnen Nederland). Materiaal, brandstoffen, op- en afbouw en afstemming met de locatie zitten bij de prijs in. De offerte toont altijd één all-in totaalbedrag."),
  ("Waarom lopen prijzen van vuurshows online zo uiteen?",
   "Onder 'vuurshow' wordt van alles verkocht: van één artiest met een fakkel tot complete producties met meerdere performers — daardoor zie je online prijzen van €400 tot ruim €6000. Vraag daarom altijd na wat er precies is inbegrepen; bij Nuno staat dat zwart-op-wit in de offerte."),
  ("Is een aanbetaling nodig en hoe zit het met annuleren?",
   "De afspraken over betaling en annulering staan helder in de offerte en de algemene voorwaarden — geen kleine lettertjes. Een datum staat pas definitief vast na schriftelijke bevestiging."),
  ("Kan de show ook binnen, en kost dat extra?",
   "Binnen kan zodra de locatie en de brandweer het toelaten; anders schakelt Nuno naar acts zonder open vuur, zoals mentalisme of de fakirshow. Dat verandert niets aan de pakketprijs."),
 ],
 "service": {"name": "Vuurspuwer inhuren (prijzen en pakketten)", "type": "Vuurshow",
             "desc": "Vuurshow boeken van 10 tot 5×20 minuten: power-act, showblok voor bruiloften en bedrijfsfeesten, volledige vuurshow of festivalpakket. Transparante prijzen van €350 tot €1500.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "4",
                        "description": "Vier pakketten: power-act 10 min (vanaf €350), showblok 20 min (vanaf €450), volledige show 30 min (vanaf €595), festivalpakket tot 5×20 min (€950–€1500)."}},
 "fotos": [],
}
