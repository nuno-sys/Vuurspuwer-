# -*- coding: utf-8 -*-
"""Nederlandstalige zoekwoordpagina's die nog geen eigen plek hadden.

Aanleiding: de Search Console-export van 13 juni – 12 september 2026 laat
zien dat de site wél goed scoort op de "vuurspuwer"-familie (positie 8–15)
maar nauwelijks bestaat op de even commerciële woorden "vuurshow",
"vuurshows" en "vlammenshow" (positie 27–53, samen ruim 1.500 vertoningen).
Het woord "vuurshow" stond 6.209 keer in de teksten maar geen enkele pagina
had het als hoofdonderwerp; "vlammenshow" kwam nergens voor.

Deze pagina's zijn bewust alléén Nederlands: "vlammenshow" is een
Nederlandse zoekterm zonder bruikbare tegenhanger in het Engels, Duits of
Frans. Ze krijgen daarom geen hreflang-verwijzingen naar taalversies die
niet bestaan.
"""

_OFFER = {"@type": "AggregateOffer", "priceCurrency": "EUR",
          "lowPrice": "350", "highPrice": "1500", "offerCount": "6",
          "description": "Van een power-act van 10 minuten vanaf €350 tot een "
                         "volledig avondprogramma tot €1500. Altijd één all-in "
                         "offerte, inclusief reis en materiaal."}

NL = {

# ---------------------------------------------------------------------------
"vuurshow-boeken": {
 "title": "Vuurshow boeken",
 "seo_title": "\U0001F525 Vuurshow boeken in NL & BE | Vanaf €350 | Vuurspuwer Nuno",
 "seo_desc": "Vuurshow boeken? Nuno verzorgt vuurshows in heel Nederland en België ★ 4,9/5 uit 136 reviews ✓ €350–€1500 ✓ binnen 24 uur een offerte op maat.",
 "eyebrow": "Vuurshows",
 "img": ("/assets/media/festival-1600.webp",
         "Vuurshow op een festivalplein: Nuno spuwt een metershoge vuurbal boven het publiek"),
 "body": """
<p><strong>Een vuurshow is het moment waarop iedereen zijn telefoon pakt. Metershoge vuurballen, draaiend vuur op muziek en een finale die je in je gezicht voelt. Vuurspuwer Nuno verzorgt vuurshows in heel Nederland en België — op festivals, bedrijfsfeesten, bruiloften en themafeesten — vanaf €350.</strong></p>

<h2>Wat is een vuurshow precies?</h2>
<p>Een vuurshow is een liveact waarin een professionele vuurartiest met open vuur werkt op muziek en licht. Bij Nuno bestaat een show uit een vaste opbouw: hij begint rustig met vuurjongleren zodat het publiek dichterbij komt, bouwt op via draaiend vuur en body fire, en eindigt met het vuurspuwen — de vuurballen die tot zes meter hoog reiken. Een show duurt tien tot dertig minuten, afhankelijk van wat je kiest.</p>
<p>Het verschil met <a href="/vuurwerk-alternatief/">vuurwerk</a> is dat een vuurshow van dichtbij gebeurt, met een artiest die contact maakt met het publiek. Daardoor mag het ook op plekken waar vuurwerk allang verboden is: binnenterreinen, natuurgebieden, stadscentra en locaties met buren.</p>

<h2>Drie vormen om uit te kiezen</h2>
<ul>
<li><strong>Power-act van 10 minuten — vanaf €350.</strong> Eén compact blok op het hoogtepunt van de avond. Populair als verrassing bij het aansnijden van de taart of als opening van het feest.</li>
<li><strong>Showblok van 20 minuten — vanaf €450.</strong> De volledige opbouw met jongleren, draaiend vuur en de vuurspuw-finale. Dit is wat de meeste opdrachtgevers boeken.</li>
<li><strong>Avondprogramma — tot €1500.</strong> Meerdere blokken verspreid over de avond, eventueel met een tweede artiest of een <a href="/fakir-show-inhuren/">fakirshow</a> ertussen, zodat er de hele avond iets te beleven valt.</li>
</ul>

<h2>Waar Nuno vuurshows verzorgt</h2>
<p>Nuno werkt vanuit Zeist en komt in heel Nederland en heel Vlaanderen en Wallonië. Reiskosten zitten altijd in de offerte, dus je krijgt één bedrag zonder verrassingen achteraf. Bekijk <a href="/locaties-vuurshows-nederland-belgie/">alle locaties</a> of ga direct naar de stad waar je feest is: <a href="/vuurspuwer-boeken-in-amsterdam/">Amsterdam</a>, <a href="/vuurspuwer-boeken-in-rotterdam/">Rotterdam</a>, <a href="/vuurspuwer-boeken-in-utrecht/">Utrecht</a>, <a href="/vuurspuwer-boeken-in-antwerpen/">Antwerpen</a>, <a href="/vuurspuwer-boeken-in-gent/">Gent</a> of <a href="/vuurspuwer-boeken-in-brussel/">Brussel</a>.</p>

<h2>Vuurshow per gelegenheid</h2>
<p>Elke gelegenheid vraagt een andere opbouw. Een <a href="/vuurshow-bruiloft/">vuurshow op een bruiloft</a> is romantisch en op maat gemaakt bij de eerste dans. Een <a href="/vuurshow-bedrijfsfeest/">vuurshow op een bedrijfsfeest</a> werkt als opening of grande finale en gaat netjes op factuur. Op een <a href="/vuurshow-festival/">festival</a> draait het om bereik en herhaling, en bij een <a href="/vuurshow-verjaardag/">verjaardag of jubileum</a> om de verrassing.</p>

<h2>Veiligheid is geen bijzaak</h2>
<p>Nuno werkt al zeventien jaar met vuur en is bekend van SBS6, RTL 4 en VTM. Hij komt altijd ruim voor aanvang, loopt de locatie door met de organisatie, bepaalt de veiligheidszone en heeft eigen blusmiddelen bij zich. Hij is verzekerd en werkt met een vloeistof die speciaal voor dit vak is bedoeld. Lees meer over <a href="/vuurspuwen-op-locatie-wat-zijn-de-veiligheidsvereisten-het-complete-antwoord-door-vuurspuwer-nuno/">de veiligheidsvereisten op locatie</a>.</p>

<h2>Wat kost een vuurshow?</h2>
<p>Een vuurshow kost tussen de €350 en €1500. Wat je betaalt hangt af van de lengte, het aantal blokken en de reisafstand. Je krijgt altijd één all-in bedrag, inclusief reis, materiaal en verzekering. Bekijk het <a href="/wat-kost-een-vuurspuwer/">complete prijzenoverzicht</a> of vraag meteen een <a href="/contact-3/">vrijblijvende offerte</a> aan — binnen 24 uur heb je antwoord.</p>
""",
 "faq": [
   ("Wat kost een vuurshow?",
    "Een vuurshow kost tussen de €350 en €1500. Een power-act van 10 minuten begint bij €350, het populaire showblok van 20 minuten bij €450, en een volledig avondprogramma met meerdere blokken loopt op tot €1500. Reiskosten, materiaal en verzekering zitten altijd in het bedrag, dus je krijgt één all-in offerte zonder verrassingen."),
   ("Hoe lang duurt een vuurshow?",
    "Tien tot dertig minuten. Tien minuten is een compacte power-act op het hoogtepunt van de avond; twintig minuten is de volledige show met jongleren, draaiend vuur en de vuurspuw-finale. Voor een avondprogramma worden meerdere blokken over de avond verdeeld, zodat het feest tussendoor gewoon doorloopt."),
   ("Mag een vuurshow overal?",
    "Bijna overal, en vaak juist wél op plekken waar vuurwerk verboden is. Een vuurshow valt onder andere regels dan vuurwerk. Nuno overlegt vooraf met de locatie, bepaalt de veiligheidszone en neemt eigen blusmiddelen mee. Alleen onder een laag afdak of bij zeer harde wind is open vuur soms niet verstandig; dan schakelt hij naar mentalisme of de fakirshow."),
   ("Kan een vuurshow binnen?",
    "Ja, mits er genoeg hoogte en ventilatie is. Nuno past de act aan de ruimte aan: binnen wordt er minder hoog gespoten en meer met jongleren en body fire gewerkt. Is de zaal echt te laag, dan is de fakirshow of mentalisme een volwaardig alternatief zonder open vuur."),
   ("Hoeveel ruimte is er nodig voor een vuurshow?",
    "Buiten ongeveer zes bij zes meter vrije vloer en zes meter vrije hoogte, met het publiek op een paar meter afstand. Binnen kan het krapper, maar hoogte blijft het belangrijkst. Nuno bekijkt de situatie vooraf en zegt eerlijk wat er wel en niet kan."),
   ("Hoe snel kan ik een vuurshow boeken?",
    "Vraag een offerte aan via het contactformulier of WhatsApp; binnen 24 uur heb je antwoord met een prijs op maat. Voor december en de festivalzomer is vroeg boeken verstandig — die data zijn het eerst vol."),
 ],
 "service": {
   "name": "Vuurshow boeken",
   "type": "Vuurshow",
   "desc": "Professionele vuurshow voor festivals, bedrijfsfeesten, bruiloften en themafeesten in heel Nederland en België. Van een power-act van 10 minuten tot een volledig avondprogramma. Vanaf €350.",
   "offers": _OFFER,
 },
 "fotos": [
   ["festival-900.webp", "festival-1600.webp", 900, 902,
    "Vuurshow op een festivalplein",
    "Vuurshow op een festival: Nuno spuwt een metershoge vuurbal boven het publiek"],
   ["avondvuur-900.webp", "avondvuur-1080.webp", 900, 893,
    "Vuurbal in de avondschemering",
    "Vuurshow in de avondschemering met een enorme vuurbal"],
   ["nachtvuur-900.webp", "nachtvuur-960.webp", 900, 900,
    "Draaiend vuur in het donker",
    "Vuurshow bij nacht: draaiend vuur tegen een zwarte lucht"],
 ],
},

# ---------------------------------------------------------------------------
"vlammenshow": {
 "title": "Vlammenshow",
 "seo_title": "\U0001F525 Vlammenshow huren | Vlammen & Vuur op je Feest | Vanaf €350",
 "seo_desc": "Vlammenshow huren voor je feest of evenement? Metershoge vlammen op muziek, binnen en buiten, in heel NL & BE ★ 4,9/5 uit 136 reviews ✓ vanaf €350.",
 "eyebrow": "Vlammenshow",
 "img": ("/assets/media/vuurzee-900.webp",
         "Vlammenshow: een zee van vlammen tijdens een optreden van Nuno"),
 "body": """
<p><strong>Een vlammenshow is precies wat het woord belooft: vlammen die de lucht in gaan, warmte die je op je gezicht voelt en een publiek dat een halve stap achteruit doet. Vuurspuwer Nuno verzorgt vlammenshows in heel Nederland en België, binnen en buiten, vanaf €350.</strong></p>

<h2>Wat is een vlammenshow?</h2>
<p>Vlammenshow, vuurshow en vuurspuwen worden door elkaar gebruikt, maar mensen die "vlammenshow" zoeken bedoelen meestal één ding: ze willen échte vlammen zien, groot en dichtbij. Dat is precies waar Nuno's act op gebouwd is. De vuurballen die hij spuwt reiken tot zes meter hoog, en in het donker kleuren ze het hele terrein oranje.</p>
<p>Een vlammenshow is geen <a href="/vuurwerk-alternatief/">vuurwerk</a>. Er is geen knal, geen vergunningstraject van weken en geen veiligheidszone van honderd meter. Er staat een artiest voor je neus die het vuur beheerst, op muziek, met timing. Daardoor kan het op plekken waar vuurwerk allang niet meer mag.</p>

<h2>Wat je ziet tijdens de show</h2>
<ul>
<li><strong>Vuurballen</strong> — de klassieker: metershoge vlammen die recht omhoog gaan, het moment waar alle foto's van gemaakt worden.</li>
<li><strong>Draaiend vuur</strong> — poi en staff die vuurcirkels in de lucht tekenen, strak op de muziek.</li>
<li><strong>Body fire</strong> — vlammen over armen en handen, van dichtbij, waar het publiek de warmte voelt.</li>
<li><strong>De finale</strong> — meerdere vuurballen achter elkaar, het punt waarop iedereen begint te klappen.</li>
</ul>

<h2>Binnen of buiten</h2>
<p>Buiten kan alles: daar heeft Nuno de hoogte om de grootste vlammen te maken. Binnen kan het ook, mits er genoeg hoogte en ventilatie is — dan verschuift het accent naar draaiend vuur en body fire, en blijven de vlammen lager maar net zo dichtbij. Nuno bekijkt de locatie vooraf en zegt eerlijk wat er wel en niet kan. Is open vuur echt geen optie, dan is de <a href="/fakir-show-inhuren/">fakirshow</a> met spijkerbed en glasact een volwaardig alternatief dat net zo hard binnenkomt.</p>

<h2>Voor welke feesten</h2>
<p>Een vlammenshow werkt overal waar je één onvergetelijk moment wilt: op een <a href="/vuurshow-bedrijfsfeest/">bedrijfsfeest</a> als opening of afsluiter, op een <a href="/vuurshow-bruiloft/">bruiloft</a> bij de avondopening, op een <a href="/vuurshow-festival/">festival</a> als publiekstrekker, en op een <a href="/vuurshow-verjaardag/">verjaardag of jubileum</a> als complete verrassing. Voor themafeesten sluit het naadloos aan bij middeleeuwen, 1001 nacht, Halloween en oud en nieuw.</p>

<h2>Wat kost een vlammenshow?</h2>
<p>Een vlammenshow kost tussen de €350 en €1500, afhankelijk van de lengte en het aantal blokken. Een korte krachtige act begint bij €350, het volledige showblok van twintig minuten bij €450. Reis, materiaal en verzekering zitten er altijd in. Bekijk het <a href="/wat-kost-een-vuurspuwer/">prijzenoverzicht</a> of vraag direct een <a href="/contact-3/">offerte</a> aan; binnen 24 uur heb je antwoord.</p>

<h2>Waarom Nuno</h2>
<p>Zeventien jaar ervaring, bekend van SBS6, RTL 4 en VTM, en 4,9 uit 5 op basis van 136 <a href="/beoordelingen/">beoordelingen</a>. Hij werkt in heel Nederland en België, komt ruim op tijd, regelt de veiligheid zelf en denkt mee over het moment in je programma waarop de show het hardst aankomt.</p>
""",
 "faq": [
   ("Wat is het verschil tussen een vlammenshow en een vuurshow?",
    "Er is geen inhoudelijk verschil: het zijn twee woorden voor dezelfde act. Mensen die „vlammenshow” zoeken willen meestal benadrukken dat ze grote, zichtbare vlammen willen — en dat is precies waar de show van Nuno op gebouwd is, met vuurballen tot zes meter hoog."),
   ("Wat kost een vlammenshow?",
    "Tussen de €350 en €1500. Een korte krachtige act van 10 minuten begint bij €350, het volledige showblok van 20 minuten bij €450, en een avondprogramma met meerdere blokken loopt op tot €1500. Reiskosten, materiaal en verzekering zitten altijd in het bedrag."),
   ("Kan een vlammenshow binnen?",
    "Ja, als er genoeg hoogte en ventilatie is. Binnen blijven de vlammen lager en verschuift het accent naar draaiend vuur en body fire. Nuno bekijkt de zaal vooraf. Kan open vuur echt niet, dan is de fakirshow met spijkerbed en glasact een volwaardig alternatief."),
   ("Is een vlammenshow gevaarlijk voor het publiek?",
    "Nee, mits het door een professional wordt gedaan. Nuno werkt met een veiligheidszone, eigen blusmiddelen en speciale showvloeistof, en is verzekerd. Het publiek staat op veilige afstand maar dichtbij genoeg om de warmte te voelen — dat is juist het effect."),
   ("Heb ik een vergunning nodig voor een vlammenshow?",
    "Meestal niet, en dat is het grote verschil met vuurwerk. Sommige gemeenten of locaties willen een melding vooraf. Nuno weet uit ervaring hoe dat per locatie werkt en helpt je op weg als er iets geregeld moet worden."),
   ("Hoeveel ruimte is er nodig?",
    "Buiten ongeveer zes bij zes meter vrije vloer en zes meter vrije hoogte. Binnen kan het krapper, maar vrije hoogte blijft het belangrijkst. Nuno stemt de act af op de ruimte die er is."),
 ],
 "service": {
   "name": "Vlammenshow huren",
   "type": "Vuurshow",
   "desc": "Vlammenshow met metershoge vuurballen, draaiend vuur en body fire, op muziek en op maat. Binnen en buiten, in heel Nederland en België. Vanaf €350.",
   "offers": _OFFER,
 },
 "fotos": [
   ["vuurzee-900.webp", "vuurzee-900.webp", 900, 899,
    "Een zee van vlammen tijdens de show",
    "Vlammenshow: een zee van vlammen tijdens een optreden van Nuno"],
   ["vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350,
    "Metershoge vuurbal",
    "Vlammenshow met een metershoge vuurbal tegen een donkere lucht"],
   ["schemering-640.webp", "schemering-640.webp", 640, 423,
    "Vlammen in de schemering",
    "Vlammenshow in de schemering"],
 ],
},

}
