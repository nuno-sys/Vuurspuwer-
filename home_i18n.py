"""Volledige vertaling van de homepage (index.html) naar EN/DE/FR.

De sleutels zijn de exacte NL-tekstfragmenten uit index.html (inclusief
HTML-entiteiten en, waar nodig, omliggende markup als anker zodat korte
woorden nergens per ongeluk elders vervangen worden). apply() vervangt
de fragmenten van lang naar kort, zodat langere zinnen altijd vóór hun
deelwoorden aan de beurt komen."""

# kop-metadata per taal, in dezelfde klikstijl als de NL-homepage
HEAD = {
 "en": {
  "title": "🔥 Hire a Fire Breather? Fire Show &amp; Fakir Show | Nuno",
  "desc": "🔥 The Benelux&#x27; top fire breather, seen on SBS6, RTL 4 &amp; VTM ★ 4.9/5 (136 reviews) ✓ Fire shows, fakir shows, mentalism &amp; workshops ✓ €350–€1500 ✓ Quote within 24h.",
  "kw": "hire fire breather, book fire show, fakir show, mentalist, fire breathing workshop, event entertainment, Netherlands, Belgium",
 },
 "de": {
  "title": "🔥 Feuerspucker buchen? Feuershow &amp; Fakirshow | Nuno",
  "desc": "🔥 Der Top-Feuerspucker der Benelux, bekannt aus SBS6, RTL 4 &amp; VTM ★ 4,9/5 (136 Bewertungen) ✓ Feuershow, Fakirshow, Mentalismus &amp; Workshops ✓ 350–1500 € ✓ Angebot in 24 h.",
  "kw": "Feuerspucker buchen, Feuershow buchen, Fakirshow, Mentalist, Workshop Feuerspucken, Event-Entertainment, Niederlande, Belgien",
 },
 "fr": {
  "title": "🔥 Engager un Cracheur de Feu ? Spectacle de Feu | Nuno",
  "desc": "🔥 Le meilleur cracheur de feu du Benelux, vu sur SBS6, RTL 4 &amp; VTM ★ 4,9/5 (136 avis) ✓ Spectacles de feu, fakir, mentalisme &amp; ateliers ✓ 350–1500 € ✓ Devis sous 24 h.",
  "kw": "engager cracheur de feu, réserver spectacle de feu, spectacle fakir, mentaliste, atelier cracheur de feu, animation événement, Pays-Bas, Belgique",
 },
}

HOME = {
# ============================================================== ENGELS
 "en": {
  # --- hero ---
  "Meester van vuur &amp; magie": "Master of fire &amp; magic",
  ">Bekijk de shows<": ">See the shows<",

  # --- manifesto ---
  "Professionele <em>vuurspuwer</em> inhuren": "Hire a professional <em>fire breather</em>",
  "Oerkracht en artistieke perfectie in één act &mdash; en een plein dat stilvalt.":
  "Raw power and artistic perfection in one act &mdash; and a crowd that falls silent.",
  "Zoekt u entertainment dat de oerkracht van vuur combineert met artistieke perfectie? Nuno is de meester van vuur en magie in de Benelux. Als volledig gecertificeerd vuurspuwer, fakir en mentalist verandert hij bedrijfsfeesten, grootschalige festivals en exclusieve bruiloften in een onvergetelijke ervaring: visueel verbluffend en gegarandeerd veilig uitgevoerd.":
  "Looking for entertainment that combines the raw power of fire with artistic perfection? Nuno is the master of fire and magic in the Benelux. As a fully certified fire breather, fakir and mentalist he turns corporate events, large-scale festivals and exclusive weddings into an unforgettable experience: visually stunning and guaranteed to be performed safely.",
  "Onderweg optredens voor SBS6, RTL en VTM, producties in Engeland en een plek in de televisieshow van Uri Geller. Elke show wordt op de plek gebouwd: de ruimte, de wind, het moment in het programma en wat úw publiek op dat punt van de avond nodig heeft. Lees":
  "Along the way: appearances for SBS6, RTL and VTM, productions in England and a spot on Uri Geller&rsquo;s television show. Every show is built on location: the space, the wind, the moment in the programme and what your audience needs at that point of the evening. Read",
  ">meer over vuurspuwer en fakir Nuno<": ">more about fire breather and fakir Nuno<",

  # --- shows ---
  ">De shows<": ">The shows<",
  "Kies op <em>vlam</em>, ruimte en speelduur": "Choose by <em>flame</em>, space and duration",
  "Van een explosieve openingsact tot een complete avond entertainment. Elke show wordt op maat gemaakt voor uw thema, locatie en publiek.":
  "From an explosive opening act to a full evening of entertainment. Every show is tailor-made for your theme, venue and audience.",
  ">Echt vuur<": ">Real fire<",
  ">Binnen &amp; buiten<": ">Indoor &amp; outdoor<",
  ">Meesterlijke vuurshows<": ">Masterful fire shows<",
  "De visuele climax van uw evenement. Nuno bouwt een choreografie van metershoge vlammen en vonkenregens: vuurspuwen, vuurjongleren, vuurketting, vuurwaaiers en body fire. Volledig gecertificeerd en veilig uitgevoerd &mdash; event entertainment op het hoogste niveau.":
  "The visual climax of your event. Nuno builds a choreography of towering flames and cascades of sparks: fire breathing, fire juggling, fire chains, fire fans and body fire. Fully certified and safely performed &mdash; event entertainment at the highest level.",
  ">Bekijk de vuurshow<": ">See the fire show<",
  ">Glas &amp; spijkers<": ">Glass &amp; nails<",
  ">Op maat<": ">Tailor-made<",
  ">Mystieke fakirshows<": ">Mystical fakir shows<",
  "Een fascinerende reis naar de grenzen van de menselijke lichaamsbeheersing. Nuno trotseert het spijkerbed en loopt blootsvoets over glas. Een spannende, serene act die van dichtbij te volgen is en het publiek sprakeloos achterlaat.":
  "A fascinating journey to the limits of human body control. Nuno defies the bed of nails and walks barefoot over glass. A thrilling, serene act that can be followed up close and leaves the audience speechless.",
  ">Ontdek het mysterie<": ">Discover the mystery<",
  ">Geen vuur<": ">No fire<",
  ">Binnen<": ">Indoor<",
  ">Educatief<": ">Educational<",
  ">Sensationele reptielenshow<": ">Sensational reptile show<",
  "Sta oog in oog met de meest mysterieuze bewoners van onze planeet. Een educatieve, veilig begeleide en spannende ontmoeting met exotische slangen en reptielen. Perfect als publiekstrekker voor winkelcentra, familiedagen en themafeesten.":
  "Come face to face with the most mysterious inhabitants of our planet. An educational, safely supervised and exciting encounter with exotic snakes and reptiles. Perfect as a crowd-puller for shopping centres, family days and theme parties.",
  ">Bekijk de dieren<": ">Meet the animals<",
  ">Buiten<": ">Outdoor<",
  ">Groepen<": ">Groups<",
  ">Grensverleggende workshops<": ">Boundary-pushing workshops<",
  "Ervaar zelf de kracht van het vuur, onder strikte begeleiding van een meester. Een unieke teambuildingactiviteit voor bedrijfsuitjes, vrijgezellenfeesten en schoolkampen. Verleg uw eigen grenzen &mdash; veilig, met professioneel materiaal.":
  "Experience the power of fire yourself, under the strict guidance of a master. A unique team-building activity for company outings, bachelor parties and school camps. Push your own limits &mdash; safely, with professional equipment.",
  ">Boek uw workshop<": ">Book your workshop<",
  ">Interactief<": ">Interactive<",
  ">Verbijsterend mentalisme<": ">Baffling mentalism<",
  "Verlies uw grip op de realiteit. Nuno leest gedachten, stuurt beslissingen en verbijstert met psychologische illusies. Een interactieve show op maat, zonder vuur, die uw gasten nog lang zal laten discussiëren &mdash; ook in zalen waar geen vlam mag branden.":
  "Lose your grip on reality. Nuno reads minds, steers decisions and baffles with psychological illusions. An interactive tailor-made show, without fire, that will keep your guests debating for a long time &mdash; including venues where no flame is allowed.",
  ">Bekijk de acts<": ">See the acts<",
  ">Decor &amp; styling<": ">Décor &amp; styling<",
  ">Totaalbeleving<": ">Total experience<",
  ">Exclusieve themafeesten<": ">Exclusive theme parties<",
  "Van een mystieke 1001 Nacht tot een zenuwslopend Halloween of een zwoel Caribbean event. Wij verzorgen niet alleen perfect aansluitend entertainment, maar creëren complete decors en styling voor de ultieme totaalbeleving.":
  "From a mystical Arabian Nights to a nerve-racking Halloween or a sultry Caribbean event. We not only provide perfectly matching entertainment, but create complete sets and styling for the ultimate total experience.",
  ">Ontdek de mogelijkheden<": ">Discover the possibilities<",

  # --- showreel ---
  "Beelden, <em>geen filter</em>": "Footage, <em>no filter</em>",
  ">Vuurshow op locatie<": ">Fire show on location<",
  ">Acts &amp; fakirwerk<": ">Acts &amp; fakir work<",
  ">Vuurbal in close-up<": ">Fireball in close-up<",
  "Liever de volledige beeldbank? Bekijk": "Prefer the full media library? See",
  ">alle video&rsquo;s<": ">all videos<",
  "</a> of <a": "</a> or <a",
  ">alle foto&rsquo;s<": ">all photos<",

  # --- galerij ---
  ">Galerij<": ">Gallery<",
  "Vuur, <em>echt gebeurd</em>": "Fire, <em>for real</em>",
  "Scroll verder &mdash; de galerij schuift mee.": "Keep scrolling &mdash; the gallery moves with you.",
  ">Alle foto&rsquo;s<": ">All photos<",

  # --- cijfers ---
  'aria-label="In cijfers"': 'aria-label="In numbers"',
  ">jaar<": ">years<",
  ">Op het podium<": ">On stage<",
  ">Gemiddelde beoordeling<": ">Average rating<",
  ">Google-reviews<": ">Google reviews<",
  ">Langste vuurshow<": ">Longest fire show<",

  # --- maatwerk ---
  "Vuurshow op maat voor bedrijfsfeest, festival of bruiloft": "Tailor-made fire show for corporate events, festivals and weddings",
  "Nuno maakt vuurshows die aansluiten op uw thema, locatie en publiek. Een krachtige openingsact voor een zakelijk gala, een romantische climax voor een bruiloft of een energieke performance op een festival: elke show is een zorgvuldige, veilige mix van adembenemend vuurspuwen en spectaculaire stunts. Een onuitwisbare indruk is gegarandeerd.":
  "Nuno creates fire shows that match your theme, venue and audience. A powerful opening act for a corporate gala, a romantic climax for a wedding or an energetic performance at a festival: every show is a careful, safe mix of breathtaking fire breathing and spectacular stunts. An indelible impression is guaranteed.",
  "Gecertificeerde veiligheid en jarenlange ervaring": "Certified safety and years of experience",
  "Met een portfolio aan optredens op internationale festivals, prestigieuze zakelijke events en bekende tv-programma&rsquo;s staat de naam Nuno voor spektakel én professionaliteit. Hij is inzetbaar door heel Nederland en België en daarbuiten. Veiligheid en certificering staan bij elke vuuract op de eerste plaats: professioneel materiaal, veilige vloeistoffen en de voorgeschreven afstanden tot publiek en omgeving.":
  "With a portfolio of performances at international festivals, prestigious corporate events and well-known TV shows, the name Nuno stands for spectacle and professionalism alike. He performs throughout the Netherlands and Belgium and beyond. Safety and certification come first in every fire act: professional equipment, safe fuels and the prescribed distances from audience and surroundings.",
  "Meer dan vuur alleen: fakir, mentalisme en reptielen": "More than fire alone: fakir, mentalism and reptiles",
  "Nuno biedt als veelzijdig entertainer een breed scala aan acts. Verbaas uw gasten met een interactieve": "As a versatile entertainer, Nuno offers a wide range of acts. Amaze your guests with an interactive",
  ">mentalismeshow<": ">mentalism show<",
  "waarin gedachten worden gelezen en illusie realiteit wordt. Kies voor stalen zenuwen met een traditionele": "in which minds are read and illusion becomes reality. Opt for nerves of steel with a traditional",
  ">fakirshow<": ">fakir show<",
  "op glas en spijkers. Of bied een educatieve ervaring met de": "on glass and nails. Or offer an educational experience with the",
  ">reptielenshow<": ">reptile show<",
  ", waarbij het publiek oog in oog staat met exotische slangen. Voor elk evenement in Nederland en België: ervaring, veiligheid en pure wow-factor.":
  ", where the audience comes face to face with exotic snakes. For every event in the Netherlands and Belgium: experience, safety and pure wow factor.",
  ">Ontvang uw offerte op maat<": ">Receive your tailored quote<",
  ">Chat op WhatsApp<": ">Chat on WhatsApp<",

  # --- reviews ---
  ">Beoordelingen<": ">Reviews<",
  "4,9 uit <em>136 beoordelingen</em>": "4.9 from <em>136 reviews</em>",
  '&ldquo;Wil je een spectaculaire show met een flinke dosis humor, liters spanning en een portie &bdquo;drakenadem&rdquo; waar je wenkbrauwen spontaan van gaan krullen? Dan ben je bij Nuno aan het juiste adres! Een absolute knaller! Je gasten praten er dagen later nog over&hellip; met sterren in hun ogen &eacute;n waarschijnlijk een lichte rookgeur in hun kleding. 😂✨&rdquo;':
  '&ldquo;Looking for a spectacular show with a hefty dose of humour, litres of suspense and a portion of &ldquo;dragon&rsquo;s breath&rdquo; that will make your eyebrows curl? Then Nuno is the right address! An absolute banger! Your guests will still be talking about it days later&hellip; with stars in their eyes and probably a faint smell of smoke in their clothes. 😂✨&rdquo;',
  '&ldquo;Super leuke ervaring! Nuno neemt zijn hele publiek mee in een geweldige show vol grappen en echte spectaculaire stunts. Nooit verwacht om zelf nog eens vuur te mogen spuwen, heel erg bedankt voor de mooie ervaring!&rdquo;':
  '&ldquo;Super fun experience! Nuno takes his whole audience along in a great show full of jokes and truly spectacular stunts. Never expected to breathe fire myself one day — thank you so much for the wonderful experience!&rdquo;',
  '>NIEUW<':
  '>NEW<',
  'alt="Vuurspuwer Nuno blaast een enorme vuurzee met vonkenregen in een uitgaansstraat bij nacht"': 'alt="Fire breather Nuno blowing an enormous sea of fire with a rain of sparks in a nightlife street"',
  'alt="Fakiract op straat: twee toeschouwers staan op Nuno terwijl hij op het spijkerbed ligt"': 'alt="Fakir act in the street: two spectators standing on Nuno while he lies on the bed of nails"',
  'alt="Nuno steunt met zijn handen in de glasscherven tijdens een theatershow"': 'alt="Nuno resting his hands in broken glass during a theatre show"',
  'alt="Nuno op het festivalpodium met vuur boven een juichende festivalmenigte"': 'alt="Nuno on the festival stage with fire above a cheering festival crowd"',
  '&ldquo;Geweldige workshop gehad van Nuno. Veiligheid voor alles! Ik heb er ontzettend veel van geleerd. En een hele fijne middag gehad. Iemand zonder kapsones en passie voor zijn vak. Diepe buiging!&rdquo;': '&ldquo;Had a great workshop with Nuno. Safety first, always! I learned an awful lot and had a really lovely afternoon. Someone without any airs and with true passion for his craft. Deep bow!&rdquo;',
  'alt="Originele Google-review van Anton Fennema"': 'alt="Original Google review by Anton Fennema"',
  '&ldquo;Wij hadden een vuurspuw workshop geboekt voor een vrijgezellenfeest bij Nuno. Nuno weet er echt een feestje van te maken en we hebben dan ook een hele leuke workshop gehad. Aanrader!&rdquo;': '&ldquo;We booked a fire-breathing workshop with Nuno for a bachelor party. Nuno really knows how to turn it into a party, and we had a great workshop indeed. Highly recommended!&rdquo;',
  'alt="Originele Google-review van N. Beek"': 'alt="Original Google review by N. Beek"',
  '&ldquo;Aardige man, zorgt voor een spectaculaire show! Waar veel mensen naar blijven kijken en steeds meer willen zien! ☄️🔥💥&rdquo;': '&ldquo;Nice guy who puts on a spectacular show! One that people keep watching — and want to see more and more of! ☄️🔥💥&rdquo;',
  'alt="Originele Google-review van Lisanne"': 'alt="Original Google review by Lisanne"',
  '>📸 Origineel van Google<': '>📸 Original from Google<',
  'alt="Originele Google-review van EL Mul"': 'alt="Original Google review by EL Mul"',
  'alt="Originele Google-review van Henk Mulder"': 'alt="Original Google review by Henk Mulder"',
  '>augustus 2026<':
  '>August 2026<',
  "136 beoordelingen op Google &middot;": "136 reviews on Google &middot;",
  ">bekijk ze op Google<": ">see them on Google<",
  "Lees alle 30 uitgelichte reviews &rsaquo;": "Read all 30 featured reviews &rsaquo;",
  'aria-label="5 van de 5 sterren"': 'aria-label="5 out of 5 stars"',

  # --- zekerheid ---
  ">Zekerheid<": ">Assurance<",
  "Spektakel is het <em>makkelijke</em> deel": "Spectacle is the <em>easy</em> part",
  ">Bekend van<": ">As seen on<",
  ">De televisieshow van Uri Geller<": ">Uri Geller&rsquo;s television show<",
  ">Producties in Engeland<": ">Productions in England<",
  ">Veiligheid<": ">Safety<",
  ">Gecertificeerd<": ">Certified<",
  "Volledig gecertificeerd als vuurspuwer en fakir. Professioneel materiaal en veilige vloeistoffen.":
  "Fully certified as a fire breather and fakir. Professional equipment and safe fuels.",
  ">Vergunning en afstand<": ">Permits and distance<",
  "Ik werk binnen de vergunningseisen en houd de voorgeschreven veiligheidsafstanden tot publiek en omgeving aan.":
  "I work within permit requirements and keep the prescribed safety distances from audience and surroundings.",
  ">Binnen of buiten<": ">Indoors or outdoors<",
  "Buiten altijd. Binnen zodra de locatie het toelaat &mdash; en anders draaien we de avond op mentalisme of reptielen, zonder vlam.":
  "Outdoors always. Indoors whenever the venue allows it &mdash; and otherwise we run the evening on mentalism or reptiles, without a flame.",

  # --- werkgebied ---
  ">Werkgebied<": ">Service area<",
  "Internationaal inzetbaar, <em>lokaal</em> beschikbaar": "Internationally bookable, <em>locally</em> available",
  "Vanuit centraal Nederland verzorgen wij wekelijks shows door de hele Benelux en het Duitse grensgebied.":
  "From the centre of the Netherlands we perform shows every week throughout the Benelux and the German border region.",
  ">Nederland<": ">The Netherlands<",
  ">Den Haag<": ">The Hague<",
  ">Belgi&euml;<": ">Belgium<",
  ">Antwerpen<": ">Antwerp<",
  ">Gent<": ">Ghent<",
  ">Brussel<": ">Brussels<",
  ">Brugge<": ">Bruges<",
  ">Luik<": ">Liège<",
  ">Duits grensgebied<": ">German border region<",
  "Alle locaties &rsaquo;": "All locations &rsaquo;",

  # --- faq ---
  ">Veelgestelde vragen<": ">Frequently asked questions<",
  "Eerst even <em>zeker</em> weten": "First, let&rsquo;s be <em>sure</em>",
  "Is Nuno gecertificeerd als vuurspuwer?": "Is Nuno certified as a fire breather?",
  "Ja. Nuno is volledig gecertificeerd als vuurspuwer en fakir en werkt met professioneel materiaal en veilige vloeistoffen.":
  "Yes. Nuno is fully certified as a fire breather and fakir and works with professional equipment and safe fuels.",
  "Wat kost het om een vuurspuwer in te huren?": "How much does it cost to hire a fire breather?",
  "Shows kosten tussen de &euro;350 (power-act van 10 minuten) en &euro;1500 (festivalpakket tot 5&times;20 minuten), exclusief reiskosten. Bekijk het volledige overzicht op":
  "Shows cost between &euro;350 (10-minute power act) and &euro;1500 (festival package up to 5&times;20 minutes), excluding travel costs. See the full overview on",
  ">de prijzenpagina<": ">the prices page<",
  "of vraag direct een offerte op maat aan.": "or request a tailored quote right away.",
  "Hoe zit het met vergunningen en veiligheidsafstanden?": "What about permits and safety distances?",
  "Er wordt gewerkt binnen de vergunningseisen van de locatie, met de voorgeschreven veiligheidsafstanden tot publiek, bebouwing en aankleding. Nuno stemt dit vooraf met de organisatie af.":
  "Everything is done within the venue&rsquo;s permit requirements, with the prescribed safety distances from audience, buildings and decoration. Nuno coordinates this with the organisation in advance.",
  "Kan een vuurshow ook binnen?": "Can a fire show take place indoors?",
  "Buiten altijd, en binnen zodra de locatie en de brandweer het toelaten. Mag er geen vlam branden, dan draait de avond op mentalisme, de fakirshow of de reptielenshow.":
  "Outdoors always, and indoors whenever the venue and fire brigade allow it. If no flame is permitted, the evening runs on mentalism, the fakir show or the reptile show.",
  "In welke plaatsen treedt Vuurspuwer Nuno op?": "In which places does fire breather Nuno perform?",
  "Vanuit Zeist door heel Nederland en Belgi&euml;, inclusief het Duitse grensgebied. Denk aan Amsterdam, Rotterdam, Utrecht, Den Haag, Eindhoven, Antwerpen, Gent, Brussel, Aachen en Krefeld.":
  "From Zeist throughout the Netherlands and Belgium, including the German border region. Think Amsterdam, Rotterdam, Utrecht, The Hague, Eindhoven, Antwerp, Ghent, Brussels, Aachen and Krefeld.",
  "Hoe ver van tevoren moet ik boeken?": "How far in advance should I book?",
  "Voor een datum in het hoogseizoen is enkele weken tot maanden vooruit verstandig. Voor een aanvraag binnen twee weken kunt u het beste bellen of appen.":
  "For a date in high season, a few weeks to months ahead is wise. For a request within two weeks, calling or messaging works best.",

  # --- boeken ---
  ">Boeken<": ">Booking<",
  "Check je <em>datum</em>": "Check your <em>date</em>",
  "Telefoon &mdash; ma t/m za, 9:00&ndash;18:00": "Phone &mdash; Mon&ndash;Sat, 9:00&ndash;18:00",
  ">Vast / zakelijk<": ">Landline / business<",
  ">Stuur een bericht<": ">Send a message<",
  ">Mail<": ">Email<",
  "Nederland, Belgi&euml; &amp; internationaal": "Netherlands, Belgium &amp; international",
  "Voor een datum binnen twee weken: bel of app even, dan gaat het sneller dan mail.":
  "For a date within two weeks: call or message &mdash; it&rsquo;s faster than email.",
  ">Naam<": ">Name<",
  ">E-mail<": ">Email<",
  ">Datum<": ">Date<",
  ">Weet ik nog niet<": ">Not sure yet<",
  ">Vuurshow<": ">Fire show<",
  ">Fakirshow<": ">Fakir show<",
  ">Reptielenshow<": ">Reptile show<",
  ">Workshop vuurspuwen<": ">Fire-breathing workshop<",
  ">Mentalisme<": ">Mentalism<",
  ">Themafeest<": ">Theme party<",
  ">Locatie<": ">Location<",
  ">Allebei<": ">Both<",
  ">Vertel kort over het evenement<": ">Tell us briefly about the event<",
  ">Verstuur aanvraag<": ">Send request<",
  "Je ontvangt direct een bevestiging per e-mail &mdash; en binnen 24 uur een persoonlijke reactie.":
  "You&rsquo;ll receive an instant confirmation by email &mdash; and a personal reply within 24 hours.",
  'placeholder="Plaats of zaal, bijv. Utrecht of De Vereeniging"': 'placeholder="Town or venue, e.g. Utrecht or De Vereeniging"',
  'placeholder="Bijv. bedrijfsfeest voor 80 personen, show rond 21:00 uur"': 'placeholder="E.g. company party for 80 people, show around 9 pm"',

  # --- attributen (alt/aria) ---
  'aria-label="Geen gesproken tekst"': 'aria-label="No spoken text"',
  'label="Geen gesproken tekst"': 'label="No spoken text"',
  "Vuurspuwer Nuno spuwt een vuurbal boven het publiek tijdens een festival overdag": "Fire breather Nuno blows a fireball above the audience during a daytime festival",
  "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer": "Fakir show in the theatre: Nuno on the bed of nails under the weight of a spectator",
  "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow": "Nuno with a boa constrictor around his arm during the reptile show",
  "Vuurspuwer blaast een grote vuurbal tegen de avondlucht tijdens de workshop vuurspuwen": "Fire breather blows a large fireball against the evening sky during the fire-breathing workshop",
  "Mentalist Nuno op het podium van een lege theaterzaal": "Mentalist Nuno on the stage of an empty theatre",
  "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond": "Fire breather next to a vintage bus during an evening theme party",
  "Showreel: vuurshow op locatie": "Showreel: fire show on location",
  "Showreel vuurshow afspelen": "Play fire show showreel",
  "Showreel: acts en fakirwerk": "Showreel: acts and fakir work",
  "Showreel acts afspelen": "Play acts showreel",
  "Showreel van vuurspuwer Nuno": "Showreel of fire breather Nuno",
  "Showreel afspelen": "Play showreel",
  'aria-label="Vuurbal in close-up"': 'aria-label="Fireball in close-up"',
  "Vuurbal-video afspelen": "Play fireball video",
  "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek": "Fire breather Nuno blows a fireball on a festival square for a large crowd",
  "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer": "Towering fireball against a black night sky above the fire breather",
  "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe": "Daytime fire show at a festival, audience watching from a few metres away",
  "Fakiract: Nuno draagt het gewicht van een staande toeschouwer": "Fakir act: Nuno bears the weight of a standing spectator",
  "Nuno op het podium van een lege theaterzaal voor een mentalismeshow": "Nuno on the stage of an empty theatre for a mentalism show",
  "Vuurspuwen in de schemering, de vlam waaiert breed uit tegen een blauwe lucht": "Fire breathing at dusk, the flame fanning out wide against a blue sky",
  "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering": "Fire breather Nuno blows an enormous fireball at dusk",
  "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht": "Close-up of the fakir act: Nuno balances the nail board with chains on his face",
  "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels": "Duo act at a wedding: fire breather Nuno with a dancer with red wings",
 },

# ============================================================== DUITS
 "de": {
  "Meester van vuur &amp; magie": "Meister von Feuer &amp; Magie",
  ">Bekijk de shows<": ">Shows ansehen<",

  "Professionele <em>vuurspuwer</em> inhuren": "Professionellen <em>Feuerspucker</em> buchen",
  "Oerkracht en artistieke perfectie in één act &mdash; en een plein dat stilvalt.":
  "Urkraft und künstlerische Perfektion in einem Act &mdash; und ein Platz, der verstummt.",
  "Zoekt u entertainment dat de oerkracht van vuur combineert met artistieke perfectie? Nuno is de meester van vuur en magie in de Benelux. Als volledig gecertificeerd vuurspuwer, fakir en mentalist verandert hij bedrijfsfeesten, grootschalige festivals en exclusieve bruiloften in een onvergetelijke ervaring: visueel verbluffend en gegarandeerd veilig uitgevoerd.":
  "Suchen Sie Entertainment, das die Urkraft des Feuers mit künstlerischer Perfektion verbindet? Nuno ist der Meister von Feuer und Magie in den Benelux-Ländern. Als voll zertifizierter Feuerspucker, Fakir und Mentalist verwandelt er Firmenfeiern, große Festivals und exklusive Hochzeiten in ein unvergessliches Erlebnis: visuell atemberaubend und garantiert sicher ausgeführt.",
  "Onderweg optredens voor SBS6, RTL en VTM, producties in Engeland en een plek in de televisieshow van Uri Geller. Elke show wordt op de plek gebouwd: de ruimte, de wind, het moment in het programma en wat úw publiek op dat punt van de avond nodig heeft. Lees":
  "Unterwegs: Auftritte für SBS6, RTL und VTM, Produktionen in England und ein Platz in der Fernsehshow von Uri Geller. Jede Show wird vor Ort gebaut: der Raum, der Wind, der Moment im Programm und was Ihr Publikum an diesem Punkt des Abends braucht. Lesen Sie",
  ">meer over vuurspuwer en fakir Nuno<": ">mehr über Feuerspucker und Fakir Nuno<",

  ">De shows<": ">Die Shows<",
  "Kies op <em>vlam</em>, ruimte en speelduur": "Wählen Sie nach <em>Flamme</em>, Raum und Spieldauer",
  "Van een explosieve openingsact tot een complete avond entertainment. Elke show wordt op maat gemaakt voor uw thema, locatie en publiek.":
  "Vom explosiven Opening-Act bis zum kompletten Abendprogramm. Jede Show wird maßgeschneidert für Ihr Thema, Ihre Location und Ihr Publikum.",
  ">Echt vuur<": ">Echtes Feuer<",
  ">Binnen &amp; buiten<": ">Drinnen &amp; draußen<",
  ">Meesterlijke vuurshows<": ">Meisterhafte Feuershows<",
  "De visuele climax van uw evenement. Nuno bouwt een choreografie van metershoge vlammen en vonkenregens: vuurspuwen, vuurjongleren, vuurketting, vuurwaaiers en body fire. Volledig gecertificeerd en veilig uitgevoerd &mdash; event entertainment op het hoogste niveau.":
  "Der visuelle Höhepunkt Ihres Events. Nuno baut eine Choreografie aus meterhohen Flammen und Funkenregen: Feuerspucken, Feuerjonglage, Feuerkette, Feuerfächer und Body Fire. Voll zertifiziert und sicher ausgeführt &mdash; Event-Entertainment auf höchstem Niveau.",
  ">Bekijk de vuurshow<": ">Zur Feuershow<",
  ">Glas &amp; spijkers<": ">Glas &amp; Nägel<",
  ">Op maat<": ">Nach Maß<",
  ">Mystieke fakirshows<": ">Mystische Fakirshows<",
  "Een fascinerende reis naar de grenzen van de menselijke lichaamsbeheersing. Nuno trotseert het spijkerbed en loopt blootsvoets over glas. Een spannende, serene act die van dichtbij te volgen is en het publiek sprakeloos achterlaat.":
  "Eine faszinierende Reise an die Grenzen der menschlichen Körperbeherrschung. Nuno trotzt dem Nagelbrett und läuft barfuß über Glas. Ein spannender, ruhiger Act, der aus nächster Nähe zu verfolgen ist und das Publikum sprachlos zurücklässt.",
  ">Ontdek het mysterie<": ">Das Mysterium entdecken<",
  ">Geen vuur<": ">Ohne Feuer<",
  ">Binnen<": ">Drinnen<",
  ">Educatief<": ">Lehrreich<",
  ">Sensationele reptielenshow<": ">Sensationelle Reptilienshow<",
  "Sta oog in oog met de meest mysterieuze bewoners van onze planeet. Een educatieve, veilig begeleide en spannende ontmoeting met exotische slangen en reptielen. Perfect als publiekstrekker voor winkelcentra, familiedagen en themafeesten.":
  "Stehen Sie Auge in Auge mit den geheimnisvollsten Bewohnern unseres Planeten. Eine lehrreiche, sicher begleitete und spannende Begegnung mit exotischen Schlangen und Reptilien. Perfekt als Publikumsmagnet für Einkaufszentren, Familientage und Mottopartys.",
  ">Bekijk de dieren<": ">Zu den Tieren<",
  ">Buiten<": ">Draußen<",
  ">Groepen<": ">Gruppen<",
  ">Grensverleggende workshops<": ">Grenzerweiternde Workshops<",
  "Ervaar zelf de kracht van het vuur, onder strikte begeleiding van een meester. Een unieke teambuildingactiviteit voor bedrijfsuitjes, vrijgezellenfeesten en schoolkampen. Verleg uw eigen grenzen &mdash; veilig, met professioneel materiaal.":
  "Erleben Sie selbst die Kraft des Feuers, unter strenger Anleitung eines Meisters. Eine einzigartige Teambuilding-Aktivität für Firmenausflüge, Junggesellenabschiede und Schullager. Erweitern Sie Ihre Grenzen &mdash; sicher, mit professionellem Material.",
  ">Boek uw workshop<": ">Workshop buchen<",
  ">Interactief<": ">Interaktiv<",
  ">Verbijsterend mentalisme<": ">Verblüffender Mentalismus<",
  "Verlies uw grip op de realiteit. Nuno leest gedachten, stuurt beslissingen en verbijstert met psychologische illusies. Een interactieve show op maat, zonder vuur, die uw gasten nog lang zal laten discussiëren &mdash; ook in zalen waar geen vlam mag branden.":
  "Verlieren Sie den Halt an der Realität. Nuno liest Gedanken, lenkt Entscheidungen und verblüfft mit psychologischen Illusionen. Eine interaktive Show nach Maß, ohne Feuer, über die Ihre Gäste noch lange diskutieren werden &mdash; auch in Sälen, in denen keine Flamme brennen darf.",
  ">Bekijk de acts<": ">Zu den Acts<",
  ">Decor &amp; styling<": ">Dekor &amp; Styling<",
  ">Totaalbeleving<": ">Gesamterlebnis<",
  ">Exclusieve themafeesten<": ">Exklusive Mottopartys<",
  "Van een mystieke 1001 Nacht tot een zenuwslopend Halloween of een zwoel Caribbean event. Wij verzorgen niet alleen perfect aansluitend entertainment, maar creëren complete decors en styling voor de ultieme totaalbeleving.":
  "Von mystischem 1001-Nacht bis zu nervenaufreibendem Halloween oder einem heißen Caribbean-Event. Wir liefern nicht nur perfekt passendes Entertainment, sondern gestalten komplette Kulissen und Styling für das ultimative Gesamterlebnis.",
  ">Ontdek de mogelijkheden<": ">Möglichkeiten entdecken<",

  "Beelden, <em>geen filter</em>": "Bilder, <em>ohne Filter</em>",
  ">Vuurshow op locatie<": ">Feuershow vor Ort<",
  ">Acts &amp; fakirwerk<": ">Acts &amp; Fakirkunst<",
  ">Vuurbal in close-up<": ">Feuerball in Nahaufnahme<",
  "Liever de volledige beeldbank? Bekijk": "Lieber die ganze Bildergalerie? Sehen Sie",
  ">alle video&rsquo;s<": ">alle Videos<",
  "</a> of <a": "</a> oder <a",
  ">alle foto&rsquo;s<": ">alle Fotos<",

  ">Galerij<": ">Galerie<",
  "Vuur, <em>echt gebeurd</em>": "Feuer, <em>wirklich passiert</em>",
  "Scroll verder &mdash; de galerij schuift mee.": "Scrollen Sie weiter &mdash; die Galerie wandert mit.",
  ">Alle foto&rsquo;s<": ">Alle Fotos<",

  'aria-label="In cijfers"': 'aria-label="In Zahlen"',
  ">jaar<": ">Jahre<",
  ">Op het podium<": ">Auf der Bühne<",
  ">Gemiddelde beoordeling<": ">Durchschnittliche Bewertung<",
  ">Google-reviews<": ">Google-Bewertungen<",
  ">Langste vuurshow<": ">Längste Feuershow<",

  "Vuurshow op maat voor bedrijfsfeest, festival of bruiloft": "Feuershow nach Maß für Firmenfeier, Festival oder Hochzeit",
  "Nuno maakt vuurshows die aansluiten op uw thema, locatie en publiek. Een krachtige openingsact voor een zakelijk gala, een romantische climax voor een bruiloft of een energieke performance op een festival: elke show is een zorgvuldige, veilige mix van adembenemend vuurspuwen en spectaculaire stunts. Een onuitwisbare indruk is gegarandeerd.":
  "Nuno gestaltet Feuershows, die zu Ihrem Thema, Ihrer Location und Ihrem Publikum passen. Ein kraftvoller Opening-Act für eine Firmengala, ein romantischer Höhepunkt für eine Hochzeit oder eine energiegeladene Performance auf einem Festival: Jede Show ist eine sorgfältige, sichere Mischung aus atemberaubendem Feuerspucken und spektakulären Stunts. Ein unauslöschlicher Eindruck ist garantiert.",
  "Gecertificeerde veiligheid en jarenlange ervaring": "Zertifizierte Sicherheit und langjährige Erfahrung",
  "Met een portfolio aan optredens op internationale festivals, prestigieuze zakelijke events en bekende tv-programma&rsquo;s staat de naam Nuno voor spektakel én professionaliteit. Hij is inzetbaar door heel Nederland en België en daarbuiten. Veiligheid en certificering staan bij elke vuuract op de eerste plaats: professioneel materiaal, veilige vloeistoffen en de voorgeschreven afstanden tot publiek en omgeving.":
  "Mit einem Portfolio aus Auftritten auf internationalen Festivals, renommierten Firmenevents und bekannten TV-Programmen steht der Name Nuno für Spektakel und Professionalität. Er ist in den ganzen Niederlanden, Belgien und darüber hinaus buchbar. Sicherheit und Zertifizierung stehen bei jedem Feuer-Act an erster Stelle: professionelles Material, sichere Flüssigkeiten und die vorgeschriebenen Abstände zu Publikum und Umgebung.",
  "Meer dan vuur alleen: fakir, mentalisme en reptielen": "Mehr als nur Feuer: Fakir, Mentalismus und Reptilien",
  "Nuno biedt als veelzijdig entertainer een breed scala aan acts. Verbaas uw gasten met een interactieve": "Als vielseitiger Entertainer bietet Nuno eine breite Palette an Acts. Verblüffen Sie Ihre Gäste mit einer interaktiven",
  ">mentalismeshow<": ">Mentalismus-Show<",
  "waarin gedachten worden gelezen en illusie realiteit wordt. Kies voor stalen zenuwen met een traditionele": "bei der Gedanken gelesen werden und Illusion Realität wird. Wählen Sie Nerven aus Stahl mit einer traditionellen",
  ">fakirshow<": ">Fakirshow<",
  "op glas en spijkers. Of bied een educatieve ervaring met de": "auf Glas und Nägeln. Oder bieten Sie ein lehrreiches Erlebnis mit der",
  ">reptielenshow<": ">Reptilienshow<",
  ", waarbij het publiek oog in oog staat met exotische slangen. Voor elk evenement in Nederland en België: ervaring, veiligheid en pure wow-factor.":
  ", bei der das Publikum exotischen Schlangen Auge in Auge gegenübersteht. Für jedes Event in den Niederlanden und Belgien: Erfahrung, Sicherheit und purer Wow-Faktor.",
  ">Ontvang uw offerte op maat<": ">Ihr Angebot nach Maß erhalten<",
  ">Chat op WhatsApp<": ">Auf WhatsApp chatten<",

  ">Beoordelingen<": ">Bewertungen<",
  "4,9 uit <em>136 beoordelingen</em>": "4,9 aus <em>136 Bewertungen</em>",
  '&ldquo;Wil je een spectaculaire show met een flinke dosis humor, liters spanning en een portie &bdquo;drakenadem&rdquo; waar je wenkbrauwen spontaan van gaan krullen? Dan ben je bij Nuno aan het juiste adres! Een absolute knaller! Je gasten praten er dagen later nog over&hellip; met sterren in hun ogen &eacute;n waarschijnlijk een lichte rookgeur in hun kleding. 😂✨&rdquo;':
  '&ldquo;Suchst du eine spektakuläre Show mit einer kräftigen Portion Humor, literweise Spannung und einer Prise „Drachenatem“, von der sich deine Augenbrauen spontan kräuseln? Dann bist du bei Nuno an der richtigen Adresse! Ein absoluter Knaller! Deine Gäste reden noch Tage später darüber&hellip; mit Sternen in den Augen und wahrscheinlich einem leichten Rauchgeruch in der Kleidung. 😂✨&rdquo;',
  '&ldquo;Super leuke ervaring! Nuno neemt zijn hele publiek mee in een geweldige show vol grappen en echte spectaculaire stunts. Nooit verwacht om zelf nog eens vuur te mogen spuwen, heel erg bedankt voor de mooie ervaring!&rdquo;':
  '&ldquo;Super schöne Erfahrung! Nuno nimmt sein ganzes Publikum mit in eine großartige Show voller Witze und wirklich spektakulärer Stunts. Nie erwartet, selbst einmal Feuer spucken zu dürfen — vielen Dank für dieses schöne Erlebnis!&rdquo;',
  '>NIEUW<':
  '>NEU<',
  'alt="Vuurspuwer Nuno blaast een enorme vuurzee met vonkenregen in een uitgaansstraat bij nacht"': 'alt="Feuerspucker Nuno bläst ein riesiges Feuermeer mit Funkenregen in einer Ausgehstraße bei Nacht"',
  'alt="Fakiract op straat: twee toeschouwers staan op Nuno terwijl hij op het spijkerbed ligt"': 'alt="Fakir-Act auf der Straße: zwei Zuschauer stehen auf Nuno, während er auf dem Nagelbrett liegt"',
  'alt="Nuno steunt met zijn handen in de glasscherven tijdens een theatershow"': 'alt="Nuno stützt sich während einer Theatershow mit den Händen in Glasscherben"',
  'alt="Nuno op het festivalpodium met vuur boven een juichende festivalmenigte"': 'alt="Nuno auf der Festivalbühne mit Feuer über einer jubelnden Menge"',
  '&ldquo;Geweldige workshop gehad van Nuno. Veiligheid voor alles! Ik heb er ontzettend veel van geleerd. En een hele fijne middag gehad. Iemand zonder kapsones en passie voor zijn vak. Diepe buiging!&rdquo;': '&ldquo;Großartigen Workshop bei Nuno gehabt. Sicherheit geht vor! Ich habe unheimlich viel gelernt und einen sehr schönen Nachmittag gehabt. Jemand ohne Allüren und mit Leidenschaft für sein Fach. Tiefe Verbeugung!&rdquo;',
  'alt="Originele Google-review van Anton Fennema"': 'alt="Originale Google-Bewertung von Anton Fennema"',
  '&ldquo;Wij hadden een vuurspuw workshop geboekt voor een vrijgezellenfeest bij Nuno. Nuno weet er echt een feestje van te maken en we hebben dan ook een hele leuke workshop gehad. Aanrader!&rdquo;': '&ldquo;Wir hatten bei Nuno einen Feuerspuck-Workshop für einen Junggesellenabschied gebucht. Nuno weiß daraus wirklich ein Fest zu machen, und wir hatten einen richtig tollen Workshop. Sehr zu empfehlen!&rdquo;',
  'alt="Originele Google-review van N. Beek"': 'alt="Originale Google-Bewertung von N. Beek"',
  '&ldquo;Aardige man, zorgt voor een spectaculaire show! Waar veel mensen naar blijven kijken en steeds meer willen zien! ☄️🔥💥&rdquo;': '&ldquo;Netter Mann, der für eine spektakuläre Show sorgt! Bei der viele Leute dranbleiben — und immer mehr sehen wollen! ☄️🔥💥&rdquo;',
  'alt="Originele Google-review van Lisanne"': 'alt="Originale Google-Bewertung von Lisanne"',
  '>📸 Origineel van Google<': '>📸 Original von Google<',
  'alt="Originele Google-review van EL Mul"': 'alt="Originale Google-Bewertung von EL Mul"',
  'alt="Originele Google-review van Henk Mulder"': 'alt="Originale Google-Bewertung von Henk Mulder"',
  '>augustus 2026<':
  '>August 2026<',
  "136 beoordelingen op Google &middot;": "136 Bewertungen auf Google &middot;",
  ">bekijk ze op Google<": ">auf Google ansehen<",
  "Lees alle 30 uitgelichte reviews &rsaquo;": "Alle 30 ausgewählten Bewertungen lesen &rsaquo;",
  'aria-label="5 van de 5 sterren"': 'aria-label="5 von 5 Sternen"',

  ">Zekerheid<": ">Sicherheit &amp; Vertrauen<",
  "Spektakel is het <em>makkelijke</em> deel": "Spektakel ist der <em>einfache</em> Teil",
  ">Bekend van<": ">Bekannt aus<",
  ">De televisieshow van Uri Geller<": ">Der Fernsehshow von Uri Geller<",
  ">Producties in Engeland<": ">Produktionen in England<",
  ">Veiligheid<": ">Sicherheit<",
  ">Gecertificeerd<": ">Zertifiziert<",
  "Volledig gecertificeerd als vuurspuwer en fakir. Professioneel materiaal en veilige vloeistoffen.":
  "Voll zertifiziert als Feuerspucker und Fakir. Professionelles Material und sichere Flüssigkeiten.",
  ">Vergunning en afstand<": ">Genehmigung und Abstand<",
  "Ik werk binnen de vergunningseisen en houd de voorgeschreven veiligheidsafstanden tot publiek en omgeving aan.":
  "Ich arbeite im Rahmen der Genehmigungsauflagen und halte die vorgeschriebenen Sicherheitsabstände zu Publikum und Umgebung ein.",
  ">Binnen of buiten<": ">Drinnen oder draußen<",
  "Buiten altijd. Binnen zodra de locatie het toelaat &mdash; en anders draaien we de avond op mentalisme of reptielen, zonder vlam.":
  "Draußen immer. Drinnen, sobald die Location es zulässt &mdash; andernfalls gestalten wir den Abend mit Mentalismus oder Reptilien, ganz ohne Flamme.",

  ">Werkgebied<": ">Einsatzgebiet<",
  "Internationaal inzetbaar, <em>lokaal</em> beschikbaar": "International einsetzbar, <em>lokal</em> verfügbar",
  "Vanuit centraal Nederland verzorgen wij wekelijks shows door de hele Benelux en het Duitse grensgebied.":
  "Von der Mitte der Niederlande aus spielen wir wöchentlich Shows in den gesamten Benelux-Ländern und im deutschen Grenzgebiet.",
  ">Nederland<": ">Niederlande<",
  ">Belgi&euml;<": ">Belgien<",
  ">Brussel<": ">Brüssel<",
  ">Brugge<": ">Brügge<",
  ">Leuven<": ">Löwen<",
  ">Luik<": ">Lüttich<",
  ">Duits grensgebied<": ">Deutsches Grenzgebiet<",
  "Alle locaties &rsaquo;": "Alle Orte &rsaquo;",

  ">Veelgestelde vragen<": ">Häufige Fragen<",
  "Eerst even <em>zeker</em> weten": "Erst einmal <em>sicher</em> sein",
  "Is Nuno gecertificeerd als vuurspuwer?": "Ist Nuno als Feuerspucker zertifiziert?",
  "Ja. Nuno is volledig gecertificeerd als vuurspuwer en fakir en werkt met professioneel materiaal en veilige vloeistoffen.":
  "Ja. Nuno ist als Feuerspucker und Fakir voll zertifiziert und arbeitet mit professionellem Material und sicheren Flüssigkeiten.",
  "Wat kost het om een vuurspuwer in te huren?": "Was kostet es, einen Feuerspucker zu buchen?",
  "Shows kosten tussen de &euro;350 (power-act van 10 minuten) en &euro;1500 (festivalpakket tot 5&times;20 minuten), exclusief reiskosten. Bekijk het volledige overzicht op":
  "Shows kosten zwischen 350 &euro; (10-minütiger Power-Act) und 1500 &euro; (Festivalpaket bis 5&times;20 Minuten), zuzüglich Fahrtkosten. Die vollständige Übersicht finden Sie auf",
  ">de prijzenpagina<": ">der Preisseite<",
  "of vraag direct een offerte op maat aan.": "oder fordern Sie direkt ein Angebot nach Maß an.",
  "Hoe zit het met vergunningen en veiligheidsafstanden?": "Wie sieht es mit Genehmigungen und Sicherheitsabständen aus?",
  "Er wordt gewerkt binnen de vergunningseisen van de locatie, met de voorgeschreven veiligheidsafstanden tot publiek, bebouwing en aankleding. Nuno stemt dit vooraf met de organisatie af.":
  "Gearbeitet wird im Rahmen der Genehmigungsauflagen der Location, mit den vorgeschriebenen Sicherheitsabständen zu Publikum, Bebauung und Dekoration. Nuno stimmt dies vorab mit der Organisation ab.",
  "Kan een vuurshow ook binnen?": "Geht eine Feuershow auch drinnen?",
  "Buiten altijd, en binnen zodra de locatie en de brandweer het toelaten. Mag er geen vlam branden, dan draait de avond op mentalisme, de fakirshow of de reptielenshow.":
  "Draußen immer, und drinnen, sobald Location und Feuerwehr es erlauben. Darf keine Flamme brennen, läuft der Abend mit Mentalismus, der Fakirshow oder der Reptilienshow.",
  "In welke plaatsen treedt Vuurspuwer Nuno op?": "In welchen Orten tritt Feuerspucker Nuno auf?",
  "Vanuit Zeist door heel Nederland en Belgi&euml;, inclusief het Duitse grensgebied. Denk aan Amsterdam, Rotterdam, Utrecht, Den Haag, Eindhoven, Antwerpen, Gent, Brussel, Aachen en Krefeld.":
  "Von Zeist aus in den ganzen Niederlanden und Belgien, einschließlich des deutschen Grenzgebiets. Zum Beispiel Amsterdam, Rotterdam, Utrecht, Den Haag, Eindhoven, Antwerpen, Gent, Brüssel, Aachen und Krefeld.",
  "Hoe ver van tevoren moet ik boeken?": "Wie weit im Voraus sollte ich buchen?",
  "Voor een datum in het hoogseizoen is enkele weken tot maanden vooruit verstandig. Voor een aanvraag binnen twee weken kunt u het beste bellen of appen.":
  "Für einen Termin in der Hochsaison sind einige Wochen bis Monate Vorlauf ratsam. Für eine Anfrage innerhalb von zwei Wochen rufen Sie am besten an oder schreiben per WhatsApp.",

  ">Boeken<": ">Buchen<",
  "Check je <em>datum</em>": "Prüfen Sie Ihr <em>Datum</em>",
  "Telefoon &mdash; ma t/m za, 9:00&ndash;18:00": "Telefon &mdash; Mo&ndash;Sa, 9:00&ndash;18:00 Uhr",
  ">Vast / zakelijk<": ">Festnetz / geschäftlich<",
  ">Stuur een bericht<": ">Nachricht senden<",
  ">Mail<": ">E-Mail<",
  "Nederland, Belgi&euml; &amp; internationaal": "Niederlande, Belgien &amp; international",
  "Voor een datum binnen twee weken: bel of app even, dan gaat het sneller dan mail.":
  "Für einen Termin innerhalb von zwei Wochen: kurz anrufen oder per WhatsApp schreiben &mdash; das geht schneller als E-Mail.",
  ">Naam<": ">Name<",
  ">E-mail<": ">E-Mail<",
  ">Datum<": ">Datum<",
  ">Weet ik nog niet<": ">Weiß ich noch nicht<",
  ">Vuurshow<": ">Feuershow<",
  ">Fakirshow<": ">Fakirshow<",
  ">Reptielenshow<": ">Reptilienshow<",
  ">Workshop vuurspuwen<": ">Workshop Feuerspucken<",
  ">Mentalisme<": ">Mentalismus<",
  ">Themafeest<": ">Mottoparty<",
  ">Locatie<": ">Ort<",
  ">Allebei<": ">Beides<",
  ">Vertel kort over het evenement<": ">Erzählen Sie kurz vom Event<",
  ">Verstuur aanvraag<": ">Anfrage senden<",
  "Je ontvangt direct een bevestiging per e-mail &mdash; en binnen 24 uur een persoonlijke reactie.":
  "Sie erhalten sofort eine Bestätigung per E-Mail &mdash; und innerhalb von 24 Stunden eine persönliche Antwort.",
  'placeholder="Plaats of zaal, bijv. Utrecht of De Vereeniging"': 'placeholder="Ort oder Saal, z. B. Utrecht oder De Vereeniging"',
  'placeholder="Bijv. bedrijfsfeest voor 80 personen, show rond 21:00 uur"': 'placeholder="Z. B. Firmenfeier für 80 Personen, Show gegen 21 Uhr"',

  'aria-label="Geen gesproken tekst"': 'aria-label="Kein gesprochener Text"',
  'label="Geen gesproken tekst"': 'label="Kein gesprochener Text"',
  "Vuurspuwer Nuno spuwt een vuurbal boven het publiek tijdens een festival overdag": "Feuerspucker Nuno spuckt einen Feuerball über dem Publikum bei einem Festival am Tag",
  "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer": "Fakirshow im Theater: Nuno auf dem Nagelbrett unter dem Gewicht eines Zuschauers",
  "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow": "Nuno mit einer Boa constrictor um den Arm während der Reptilienshow",
  "Vuurspuwer blaast een grote vuurbal tegen de avondlucht tijdens de workshop vuurspuwen": "Feuerspucker bläst einen großen Feuerball gegen den Abendhimmel beim Workshop Feuerspucken",
  "Mentalist Nuno op het podium van een lege theaterzaal": "Mentalist Nuno auf der Bühne eines leeren Theatersaals",
  "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond": "Feuerspucker neben einem Oldtimer-Bus bei einer abendlichen Mottoparty",
  "Showreel: vuurshow op locatie": "Showreel: Feuershow vor Ort",
  "Showreel vuurshow afspelen": "Showreel Feuershow abspielen",
  "Showreel: acts en fakirwerk": "Showreel: Acts und Fakirkunst",
  "Showreel acts afspelen": "Showreel Acts abspielen",
  "Showreel van vuurspuwer Nuno": "Showreel von Feuerspucker Nuno",
  "Showreel afspelen": "Showreel abspielen",
  'aria-label="Vuurbal in close-up"': 'aria-label="Feuerball in Nahaufnahme"',
  "Vuurbal-video afspelen": "Feuerball-Video abspielen",
  "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek": "Feuerspucker Nuno spuckt einen Feuerball auf einem Festivalplatz vor großem Publikum",
  "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer": "Meterhoher Feuerball vor schwarzem Nachthimmel über dem Feuerspucker",
  "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe": "Feuershow am Tag auf einem Festival, das Publikum schaut aus wenigen Metern zu",
  "Fakiract: Nuno draagt het gewicht van een staande toeschouwer": "Fakir-Act: Nuno trägt das Gewicht eines stehenden Zuschauers",
  "Nuno op het podium van een lege theaterzaal voor een mentalismeshow": "Nuno auf der Bühne eines leeren Theatersaals für eine Mentalismus-Show",
  "Vuurspuwen in de schemering, de vlam waaiert breed uit tegen een blauwe lucht": "Feuerspucken in der Dämmerung, die Flamme fächert sich breit gegen einen blauen Himmel auf",
  "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering": "Feuerspucker Nuno spuckt einen riesigen Feuerball in der Abenddämmerung",
  "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht": "Nahaufnahme des Fakir-Acts: Nuno balanciert das Nagelbrett mit Ketten auf seinem Gesicht",
  "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels": "Duo-Act auf einer Hochzeit: Feuerspucker Nuno mit Tänzerin mit roten Flügeln",
 },

# ============================================================== FRANS
 "fr": {
  "Meester van vuur &amp; magie": "Maître du feu &amp; de la magie",
  ">Bekijk de shows<": ">Voir les spectacles<",

  "Professionele <em>vuurspuwer</em> inhuren": "Engager un <em>cracheur de feu</em> professionnel",
  "Oerkracht en artistieke perfectie in één act &mdash; en een plein dat stilvalt.":
  "Puissance brute et perfection artistique en un seul numéro &mdash; et une place qui retient son souffle.",
  "Zoekt u entertainment dat de oerkracht van vuur combineert met artistieke perfectie? Nuno is de meester van vuur en magie in de Benelux. Als volledig gecertificeerd vuurspuwer, fakir en mentalist verandert hij bedrijfsfeesten, grootschalige festivals en exclusieve bruiloften in een onvergetelijke ervaring: visueel verbluffend en gegarandeerd veilig uitgevoerd.":
  "Vous cherchez un divertissement qui allie la puissance brute du feu à la perfection artistique ? Nuno est le maître du feu et de la magie au Benelux. Cracheur de feu, fakir et mentaliste entièrement certifié, il transforme fêtes d'entreprise, grands festivals et mariages exclusifs en une expérience inoubliable : visuellement époustouflant et exécuté en toute sécurité.",
  "Onderweg optredens voor SBS6, RTL en VTM, producties in Engeland en een plek in de televisieshow van Uri Geller. Elke show wordt op de plek gebouwd: de ruimte, de wind, het moment in het programma en wat úw publiek op dat punt van de avond nodig heeft. Lees":
  "En chemin : des passages sur SBS6, RTL et VTM, des productions en Angleterre et une place dans l'émission télévisée d'Uri Geller. Chaque spectacle se construit sur place : l'espace, le vent, le moment du programme et ce dont votre public a besoin à ce point de la soirée. Lisez",
  ">meer over vuurspuwer en fakir Nuno<": ">plus sur le cracheur de feu et fakir Nuno<",

  ">De shows<": ">Les spectacles<",
  "Kies op <em>vlam</em>, ruimte en speelduur": "Choisissez selon la <em>flamme</em>, l'espace et la durée",
  "Van een explosieve openingsact tot een complete avond entertainment. Elke show wordt op maat gemaakt voor uw thema, locatie en publiek.":
  "D'un numéro d'ouverture explosif à une soirée complète de divertissement. Chaque spectacle est fait sur mesure pour votre thème, votre lieu et votre public.",
  ">Echt vuur<": ">Vrai feu<",
  ">Binnen &amp; buiten<": ">Intérieur &amp; extérieur<",
  ">Meesterlijke vuurshows<": ">Spectacles de feu magistraux<",
  "De visuele climax van uw evenement. Nuno bouwt een choreografie van metershoge vlammen en vonkenregens: vuurspuwen, vuurjongleren, vuurketting, vuurwaaiers en body fire. Volledig gecertificeerd en veilig uitgevoerd &mdash; event entertainment op het hoogste niveau.":
  "Le point culminant visuel de votre événement. Nuno construit une chorégraphie de flammes immenses et de pluies d'étincelles : crachage de feu, jonglerie enflammée, chaînes de feu, éventails de feu et body fire. Entièrement certifié et exécuté en toute sécurité &mdash; du divertissement événementiel au plus haut niveau.",
  ">Bekijk de vuurshow<": ">Voir le spectacle de feu<",
  ">Glas &amp; spijkers<": ">Verre &amp; clous<",
  ">Op maat<": ">Sur mesure<",
  ">Mystieke fakirshows<": ">Spectacles de fakir mystiques<",
  "Een fascinerende reis naar de grenzen van de menselijke lichaamsbeheersing. Nuno trotseert het spijkerbed en loopt blootsvoets over glas. Een spannende, serene act die van dichtbij te volgen is en het publiek sprakeloos achterlaat.":
  "Un voyage fascinant aux limites de la maîtrise du corps humain. Nuno défie la planche à clous et marche pieds nus sur le verre. Un numéro captivant et serein, à suivre de près, qui laisse le public sans voix.",
  ">Ontdek het mysterie<": ">Découvrir le mystère<",
  ">Geen vuur<": ">Sans feu<",
  ">Binnen<": ">Intérieur<",
  ">Educatief<": ">Éducatif<",
  ">Sensationele reptielenshow<": ">Spectacle de reptiles sensationnel<",
  "Sta oog in oog met de meest mysterieuze bewoners van onze planeet. Een educatieve, veilig begeleide en spannende ontmoeting met exotische slangen en reptielen. Perfect als publiekstrekker voor winkelcentra, familiedagen en themafeesten.":
  "Retrouvez-vous face aux habitants les plus mystérieux de notre planète. Une rencontre éducative, encadrée en toute sécurité et pleine de sensations avec des serpents et reptiles exotiques. Parfait pour attirer le public dans les centres commerciaux, journées familiales et soirées à thème.",
  ">Bekijk de dieren<": ">Voir les animaux<",
  ">Buiten<": ">Extérieur<",
  ">Groepen<": ">Groupes<",
  ">Grensverleggende workshops<": ">Ateliers hors du commun<",
  "Ervaar zelf de kracht van het vuur, onder strikte begeleiding van een meester. Een unieke teambuildingactiviteit voor bedrijfsuitjes, vrijgezellenfeesten en schoolkampen. Verleg uw eigen grenzen &mdash; veilig, met professioneel materiaal.":
  "Ressentez vous-même la puissance du feu, sous la stricte supervision d'un maître. Une activité de team building unique pour sorties d'entreprise, enterrements de vie de garçon et camps scolaires. Repoussez vos limites &mdash; en toute sécurité, avec du matériel professionnel.",
  ">Boek uw workshop<": ">Réserver votre atelier<",
  ">Interactief<": ">Interactif<",
  ">Verbijsterend mentalisme<": ">Mentalisme stupéfiant<",
  "Verlies uw grip op de realiteit. Nuno leest gedachten, stuurt beslissingen en verbijstert met psychologische illusies. Een interactieve show op maat, zonder vuur, die uw gasten nog lang zal laten discussiëren &mdash; ook in zalen waar geen vlam mag branden.":
  "Perdez prise avec la réalité. Nuno lit les pensées, oriente les décisions et stupéfie avec des illusions psychologiques. Un spectacle interactif sur mesure, sans feu, qui fera longtemps parler vos invités &mdash; même dans les salles où aucune flamme n'est autorisée.",
  ">Bekijk de acts<": ">Voir les numéros<",
  ">Decor &amp; styling<": ">Décor &amp; stylisme<",
  ">Totaalbeleving<": ">Expérience totale<",
  ">Exclusieve themafeesten<": ">Soirées à thème exclusives<",
  "Van een mystieke 1001 Nacht tot een zenuwslopend Halloween of een zwoel Caribbean event. Wij verzorgen niet alleen perfect aansluitend entertainment, maar creëren complete decors en styling voor de ultieme totaalbeleving.":
  "D'une mystique 1001 Nuits à un Halloween éprouvant ou un événement caribéen torride. Nous fournissons non seulement un divertissement parfaitement assorti, mais créons des décors complets et le stylisme pour l'expérience totale ultime.",
  ">Ontdek de mogelijkheden<": ">Découvrir les possibilités<",

  "Beelden, <em>geen filter</em>": "Des images, <em>sans filtre</em>",
  ">Vuurshow op locatie<": ">Spectacle de feu sur place<",
  ">Acts &amp; fakirwerk<": ">Numéros &amp; art du fakir<",
  ">Vuurbal in close-up<": ">Boule de feu en gros plan<",
  "Liever de volledige beeldbank? Bekijk": "Envie de toute la médiathèque ? Voir",
  ">alle video&rsquo;s<": ">toutes les vidéos<",
  "</a> of <a": "</a> ou <a",
  ">alle foto&rsquo;s<": ">toutes les photos<",

  ">Galerij<": ">Galerie<",
  "Vuur, <em>echt gebeurd</em>": "Du feu, <em>pour de vrai</em>",
  "Scroll verder &mdash; de galerij schuift mee.": "Continuez à défiler &mdash; la galerie vous suit.",
  ">Alle foto&rsquo;s<": ">Toutes les photos<",

  'aria-label="In cijfers"': 'aria-label="En chiffres"',
  ">jaar<": ">ans<",
  ">Op het podium<": ">Sur scène<",
  ">Gemiddelde beoordeling<": ">Note moyenne<",
  ">Google-reviews<": ">Avis Google<",
  ">Langste vuurshow<": ">Plus long spectacle de feu<",

  "Vuurshow op maat voor bedrijfsfeest, festival of bruiloft": "Spectacle de feu sur mesure pour fête d'entreprise, festival ou mariage",
  "Nuno maakt vuurshows die aansluiten op uw thema, locatie en publiek. Een krachtige openingsact voor een zakelijk gala, een romantische climax voor een bruiloft of een energieke performance op een festival: elke show is een zorgvuldige, veilige mix van adembenemend vuurspuwen en spectaculaire stunts. Een onuitwisbare indruk is gegarandeerd.":
  "Nuno crée des spectacles de feu qui s'accordent à votre thème, votre lieu et votre public. Un numéro d'ouverture puissant pour un gala d'entreprise, un point culminant romantique pour un mariage ou une performance énergique en festival : chaque spectacle est un mélange soigné et sûr de crachage de feu à couper le souffle et de cascades spectaculaires. Une impression indélébile est garantie.",
  "Gecertificeerde veiligheid en jarenlange ervaring": "Sécurité certifiée et des années d'expérience",
  "Met een portfolio aan optredens op internationale festivals, prestigieuze zakelijke events en bekende tv-programma&rsquo;s staat de naam Nuno voor spektakel én professionaliteit. Hij is inzetbaar door heel Nederland en België en daarbuiten. Veiligheid en certificering staan bij elke vuuract op de eerste plaats: professioneel materiaal, veilige vloeistoffen en de voorgeschreven afstanden tot publiek en omgeving.":
  "Avec un portfolio de prestations dans des festivals internationaux, des événements d'entreprise prestigieux et des émissions télévisées connues, le nom Nuno est synonyme de spectacle et de professionnalisme. Il se produit dans l'ensemble des Pays-Bas, en Belgique et au-delà. La sécurité et la certification passent en premier dans chaque numéro de feu : matériel professionnel, liquides sûrs et distances réglementaires par rapport au public et à l'environnement.",
  "Meer dan vuur alleen: fakir, mentalisme en reptielen": "Plus que du feu : fakir, mentalisme et reptiles",
  "Nuno biedt als veelzijdig entertainer een breed scala aan acts. Verbaas uw gasten met een interactieve": "Entertainer polyvalent, Nuno propose une large gamme de numéros. Étonnez vos invités avec un",
  ">mentalismeshow<": ">spectacle de mentalisme interactif<",
  "waarin gedachten worden gelezen en illusie realiteit wordt. Kies voor stalen zenuwen met een traditionele": "où les pensées sont lues et l'illusion devient réalité. Optez pour des nerfs d'acier avec un",
  ">fakirshow<": ">spectacle de fakir traditionnel<",
  "op glas en spijkers. Of bied een educatieve ervaring met de": "sur verre et clous. Ou offrez une expérience éducative avec le",
  ">reptielenshow<": ">spectacle de reptiles<",
  ", waarbij het publiek oog in oog staat met exotische slangen. Voor elk evenement in Nederland en België: ervaring, veiligheid en pure wow-factor.":
  ", où le public se retrouve face à des serpents exotiques. Pour chaque événement aux Pays-Bas et en Belgique : expérience, sécurité et pur effet wow.",
  ">Ontvang uw offerte op maat<": ">Recevez votre devis sur mesure<",
  ">Chat op WhatsApp<": ">Discuter sur WhatsApp<",

  ">Beoordelingen<": ">Avis<",
  "4,9 uit <em>136 beoordelingen</em>": "4,9 sur <em>136 avis</em>",
  '&ldquo;Wil je een spectaculaire show met een flinke dosis humor, liters spanning en een portie &bdquo;drakenadem&rdquo; waar je wenkbrauwen spontaan van gaan krullen? Dan ben je bij Nuno aan het juiste adres! Een absolute knaller! Je gasten praten er dagen later nog over&hellip; met sterren in hun ogen &eacute;n waarschijnlijk een lichte rookgeur in hun kleding. 😂✨&rdquo;':
  '&ldquo;Envie d&rsquo;un spectacle spectaculaire avec une bonne dose d&rsquo;humour, des litres de suspense et une portion de « souffle de dragon » à faire friser les sourcils ? Alors Nuno est la bonne adresse ! Un vrai carton ! Vos invités en parleront encore des jours plus tard&hellip; des étoiles dans les yeux et probablement une légère odeur de fumée dans les vêtements. 😂✨&rdquo;',
  '&ldquo;Super leuke ervaring! Nuno neemt zijn hele publiek mee in een geweldige show vol grappen en echte spectaculaire stunts. Nooit verwacht om zelf nog eens vuur te mogen spuwen, heel erg bedankt voor de mooie ervaring!&rdquo;':
  '&ldquo;Une expérience super sympa ! Nuno embarque tout son public dans un spectacle génial, plein d&rsquo;humour et de cascades vraiment spectaculaires. Jamais je n&rsquo;aurais pensé cracher du feu moi-même un jour — merci beaucoup pour cette belle expérience !&rdquo;',
  '>NIEUW<':
  '>NOUVEAU<',
  'alt="Vuurspuwer Nuno blaast een enorme vuurzee met vonkenregen in een uitgaansstraat bij nacht"': 'alt="Le cracheur de feu Nuno souffle une immense mer de feu avec pluie d&rsquo;étincelles dans une rue animée"',
  'alt="Fakiract op straat: twee toeschouwers staan op Nuno terwijl hij op het spijkerbed ligt"': 'alt="Numéro de fakir dans la rue : deux spectateurs debout sur Nuno allongé sur la planche à clous"',
  'alt="Nuno steunt met zijn handen in de glasscherven tijdens een theatershow"': 'alt="Nuno prend appui les mains dans les tessons de verre pendant un spectacle en salle"',
  'alt="Nuno op het festivalpodium met vuur boven een juichende festivalmenigte"': 'alt="Nuno sur la scène du festival, du feu au-dessus d&rsquo;une foule en liesse"',
  '&ldquo;Geweldige workshop gehad van Nuno. Veiligheid voor alles! Ik heb er ontzettend veel van geleerd. En een hele fijne middag gehad. Iemand zonder kapsones en passie voor zijn vak. Diepe buiging!&rdquo;': '&ldquo;Superbe atelier avec Nuno. La sécurité avant tout ! J&rsquo;y ai énormément appris et passé un très bel après-midi. Quelqu&rsquo;un sans prétention et passionné par son métier. Chapeau bas !&rdquo;',
  'alt="Originele Google-review van Anton Fennema"': 'alt="Avis Google original d&rsquo;Anton Fennema"',
  '&ldquo;Wij hadden een vuurspuw workshop geboekt voor een vrijgezellenfeest bij Nuno. Nuno weet er echt een feestje van te maken en we hebben dan ook een hele leuke workshop gehad. Aanrader!&rdquo;': '&ldquo;Nous avions réservé un atelier cracheur de feu chez Nuno pour un enterrement de vie de garçon. Nuno sait vraiment en faire une fête, et nous avons passé un atelier très sympa. À recommander !&rdquo;',
  'alt="Originele Google-review van N. Beek"': 'alt="Avis Google original de N. Beek"',
  '&ldquo;Aardige man, zorgt voor een spectaculaire show! Waar veel mensen naar blijven kijken en steeds meer willen zien! ☄️🔥💥&rdquo;': '&ldquo;Un homme sympathique qui offre un spectacle spectaculaire ! Que beaucoup de gens continuent de regarder — en voulant en voir toujours plus ! ☄️🔥💥&rdquo;',
  'alt="Originele Google-review van Lisanne"': 'alt="Avis Google original de Lisanne"',
  '>📸 Origineel van Google<': '>📸 Original de Google<',
  'alt="Originele Google-review van EL Mul"': 'alt="Avis Google original d&rsquo;EL Mul"',
  'alt="Originele Google-review van Henk Mulder"': 'alt="Avis Google original de Henk Mulder"',
  '>augustus 2026<':
  '>août 2026<',
  "136 beoordelingen op Google &middot;": "136 avis sur Google &middot;",
  ">bekijk ze op Google<": ">les voir sur Google<",
  "Lees alle 30 uitgelichte reviews &rsaquo;": "Lire les 30 avis sélectionnés &rsaquo;",
  'aria-label="5 van de 5 sterren"': 'aria-label="5 étoiles sur 5"',

  ">Zekerheid<": ">Garanties<",
  "Spektakel is het <em>makkelijke</em> deel": "Le spectacle, c'est la partie <em>facile</em>",
  ">Bekend van<": ">Vu sur<",
  ">De televisieshow van Uri Geller<": ">L'émission télévisée d'Uri Geller<",
  ">Producties in Engeland<": ">Des productions en Angleterre<",
  ">Veiligheid<": ">Sécurité<",
  ">Gecertificeerd<": ">Certifié<",
  "Volledig gecertificeerd als vuurspuwer en fakir. Professioneel materiaal en veilige vloeistoffen.":
  "Entièrement certifié comme cracheur de feu et fakir. Matériel professionnel et liquides sûrs.",
  ">Vergunning en afstand<": ">Autorisations et distances<",
  "Ik werk binnen de vergunningseisen en houd de voorgeschreven veiligheidsafstanden tot publiek en omgeving aan.":
  "Je travaille dans le cadre des exigences d'autorisation et respecte les distances de sécurité réglementaires par rapport au public et à l'environnement.",
  ">Binnen of buiten<": ">Intérieur ou extérieur<",
  "Buiten altijd. Binnen zodra de locatie het toelaat &mdash; en anders draaien we de avond op mentalisme of reptielen, zonder vlam.":
  "À l'extérieur, toujours. À l'intérieur dès que le lieu le permet &mdash; sinon la soirée se joue sur le mentalisme ou les reptiles, sans flamme.",

  ">Werkgebied<": ">Zone d'intervention<",
  "Internationaal inzetbaar, <em>lokaal</em> beschikbaar": "Mobilisable à l'international, disponible <em>localement</em>",
  "Vanuit centraal Nederland verzorgen wij wekelijks shows door de hele Benelux en het Duitse grensgebied.":
  "Depuis le centre des Pays-Bas, nous assurons chaque semaine des spectacles dans tout le Benelux et la région frontalière allemande.",
  ">Nederland<": ">Pays-Bas<",
  ">Den Haag<": ">La Haye<",
  ">Belgi&euml;<": ">Belgique<",
  ">Antwerpen<": ">Anvers<",
  ">Gent<": ">Gand<",
  ">Brussel<": ">Bruxelles<",
  ">Brugge<": ">Bruges<",
  ">Leuven<": ">Louvain<",
  ">Luik<": ">Liège<",
  ">Mechelen<": ">Malines<",
  ">Duits grensgebied<": ">Région frontalière allemande<",
  "Alle locaties &rsaquo;": "Tous les lieux &rsaquo;",

  ">Veelgestelde vragen<": ">Questions fréquentes<",
  "Eerst even <em>zeker</em> weten": "D'abord, en être <em>sûr</em>",
  "Is Nuno gecertificeerd als vuurspuwer?": "Nuno est-il certifié comme cracheur de feu ?",
  "Ja. Nuno is volledig gecertificeerd als vuurspuwer en fakir en werkt met professioneel materiaal en veilige vloeistoffen.":
  "Oui. Nuno est entièrement certifié comme cracheur de feu et fakir et travaille avec du matériel professionnel et des liquides sûrs.",
  "Wat kost het om een vuurspuwer in te huren?": "Combien coûte l'engagement d'un cracheur de feu ?",
  "Shows kosten tussen de &euro;350 (power-act van 10 minuten) en &euro;1500 (festivalpakket tot 5&times;20 minuten), exclusief reiskosten. Bekijk het volledige overzicht op":
  "Les spectacles coûtent entre 350 &euro; (power-act de 10 minutes) et 1500 &euro; (formule festival jusqu'à 5&times;20 minutes), hors frais de déplacement. Consultez l'aperçu complet sur",
  ">de prijzenpagina<": ">la page des tarifs<",
  "of vraag direct een offerte op maat aan.": "ou demandez directement un devis sur mesure.",
  "Hoe zit het met vergunningen en veiligheidsafstanden?": "Qu'en est-il des autorisations et des distances de sécurité ?",
  "Er wordt gewerkt binnen de vergunningseisen van de locatie, met de voorgeschreven veiligheidsafstanden tot publiek, bebouwing en aankleding. Nuno stemt dit vooraf met de organisatie af.":
  "Tout se déroule dans le cadre des exigences d'autorisation du lieu, avec les distances de sécurité réglementaires par rapport au public, aux bâtiments et à la décoration. Nuno coordonne cela au préalable avec l'organisation.",
  "Kan een vuurshow ook binnen?": "Un spectacle de feu est-il possible en intérieur ?",
  "Buiten altijd, en binnen zodra de locatie en de brandweer het toelaten. Mag er geen vlam branden, dan draait de avond op mentalisme, de fakirshow of de reptielenshow.":
  "À l'extérieur, toujours ; à l'intérieur dès que le lieu et les pompiers le permettent. Si aucune flamme n'est autorisée, la soirée se joue sur le mentalisme, le spectacle de fakir ou le spectacle de reptiles.",
  "In welke plaatsen treedt Vuurspuwer Nuno op?": "Dans quelles villes le cracheur de feu Nuno se produit-il ?",
  "Vanuit Zeist door heel Nederland en Belgi&euml;, inclusief het Duitse grensgebied. Denk aan Amsterdam, Rotterdam, Utrecht, Den Haag, Eindhoven, Antwerpen, Gent, Brussel, Aachen en Krefeld.":
  "Depuis Zeist, dans tous les Pays-Bas et en Belgique, y compris la région frontalière allemande. Pensez à Amsterdam, Rotterdam, Utrecht, La Haye, Eindhoven, Anvers, Gand, Bruxelles, Aix-la-Chapelle et Krefeld.",
  "Hoe ver van tevoren moet ik boeken?": "Combien de temps à l'avance faut-il réserver ?",
  "Voor een datum in het hoogseizoen is enkele weken tot maanden vooruit verstandig. Voor een aanvraag binnen twee weken kunt u het beste bellen of appen.":
  "Pour une date en haute saison, quelques semaines à quelques mois d'avance sont recommandés. Pour une demande sous deux semaines, mieux vaut appeler ou envoyer un message WhatsApp.",

  ">Boeken<": ">Réserver<",
  "Check je <em>datum</em>": "Vérifiez votre <em>date</em>",
  "Telefoon &mdash; ma t/m za, 9:00&ndash;18:00": "Téléphone &mdash; lun&ndash;sam, 9h00&ndash;18h00",
  ">Vast / zakelijk<": ">Fixe / professionnel<",
  ">Stuur een bericht<": ">Envoyer un message<",
  ">Mail<": ">E-mail<",
  "Nederland, Belgi&euml; &amp; internationaal": "Pays-Bas, Belgique &amp; international",
  "Voor een datum binnen twee weken: bel of app even, dan gaat het sneller dan mail.":
  "Pour une date sous deux semaines : appelez ou envoyez un message, c'est plus rapide que l'e-mail.",
  ">Naam<": ">Nom<",
  ">E-mail<": ">E-mail<",
  ">Datum<": ">Date<",
  ">Weet ik nog niet<": ">Je ne sais pas encore<",
  ">Vuurshow<": ">Spectacle de feu<",
  ">Fakirshow<": ">Spectacle de fakir<",
  ">Reptielenshow<": ">Spectacle de reptiles<",
  ">Workshop vuurspuwen<": ">Atelier cracheur de feu<",
  ">Mentalisme<": ">Mentalisme<",
  ">Themafeest<": ">Soirée à thème<",
  ">Locatie<": ">Lieu<",
  ">Allebei<": ">Les deux<",
  ">Vertel kort over het evenement<": ">Parlez-nous brièvement de l'événement<",
  ">Verstuur aanvraag<": ">Envoyer la demande<",
  "Je ontvangt direct een bevestiging per e-mail &mdash; en binnen 24 uur een persoonlijke reactie.":
  "Vous recevez immédiatement une confirmation par e-mail &mdash; et une réponse personnelle sous 24 heures.",
  'placeholder="Plaats of zaal, bijv. Utrecht of De Vereeniging"': 'placeholder="Ville ou salle, p. ex. Utrecht ou De Vereeniging"',
  'placeholder="Bijv. bedrijfsfeest voor 80 personen, show rond 21:00 uur"': 'placeholder="P. ex. fête d\'entreprise pour 80 personnes, spectacle vers 21h"',

  'aria-label="Geen gesproken tekst"': 'aria-label="Pas de texte parlé"',
  'label="Geen gesproken tekst"': 'label="Pas de texte parlé"',
  "Vuurspuwer Nuno spuwt een vuurbal boven het publiek tijdens een festival overdag": "Le cracheur de feu Nuno souffle une boule de feu au-dessus du public lors d'un festival en journée",
  "Fakirshow in het theater: Nuno op het spijkerbed onder het gewicht van een toeschouwer": "Spectacle de fakir au théâtre : Nuno sur la planche à clous sous le poids d'un spectateur",
  "Nuno met een boa constrictor om zijn arm tijdens de reptielenshow": "Nuno avec un boa constricteur autour du bras pendant le spectacle de reptiles",
  "Vuurspuwer blaast een grote vuurbal tegen de avondlucht tijdens de workshop vuurspuwen": "Le cracheur de feu souffle une grande boule de feu dans le ciel du soir pendant l'atelier",
  "Mentalist Nuno op het podium van een lege theaterzaal": "Le mentaliste Nuno sur la scène d'un théâtre vide",
  "Vuurspuwer bij een vintage bus tijdens een themafeest in de avond": "Cracheur de feu près d'un bus vintage lors d'une soirée à thème",
  "Showreel: vuurshow op locatie": "Showreel : spectacle de feu sur place",
  "Showreel vuurshow afspelen": "Lire le showreel du spectacle de feu",
  "Showreel: acts en fakirwerk": "Showreel : numéros et art du fakir",
  "Showreel acts afspelen": "Lire le showreel des numéros",
  "Showreel van vuurspuwer Nuno": "Showreel du cracheur de feu Nuno",
  "Showreel afspelen": "Lire le showreel",
  'aria-label="Vuurbal in close-up"': 'aria-label="Boule de feu en gros plan"',
  "Vuurbal-video afspelen": "Lire la vidéo de la boule de feu",
  "Vuurspuwer Nuno spuwt een vuurbal op een festivalplein voor een groot publiek": "Le cracheur de feu Nuno souffle une boule de feu devant une grande foule de festival",
  "Meters hoge vuurbal tegen een zwarte nachtlucht boven de vuurspuwer": "Immense boule de feu contre un ciel nocturne noir au-dessus du cracheur de feu",
  "Vuurshow overdag op een festival, publiek kijkt vanaf enkele meters toe": "Spectacle de feu en journée dans un festival, le public regarde à quelques mètres",
  "Fakiract: Nuno draagt het gewicht van een staande toeschouwer": "Numéro de fakir : Nuno porte le poids d'un spectateur debout",
  "Nuno op het podium van een lege theaterzaal voor een mentalismeshow": "Nuno sur la scène d'un théâtre vide pour un spectacle de mentalisme",
  "Vuurspuwen in de schemering, de vlam waaiert breed uit tegen een blauwe lucht": "Crachage de feu au crépuscule, la flamme s'évase largement contre un ciel bleu",
  "Vuurspuwer Nuno spuwt een enorme vuurbal in de avondschemering": "Le cracheur de feu Nuno souffle une énorme boule de feu au crépuscule",
  "Close-up van de fakiract: Nuno balanceert het spijkerbord met kettingen op zijn gezicht": "Gros plan du numéro de fakir : Nuno balance la planche à clous avec des chaînes sur son visage",
  "Duo-act op een bruiloft: vuurspuwer Nuno met danseres met rode vleugels": "Duo à un mariage : le cracheur de feu Nuno avec une danseuse aux ailes rouges",
 },
}

def apply(doc, lang):
    """Vervangt alle fragmenten (langste eerst) en meldt wat niet gevonden is."""
    missing = []
    for nl, tr in sorted(HOME[lang].items(), key=lambda kv: -len(kv[0])):
        if nl in doc:
            doc = doc.replace(nl, tr)
        else:
            missing.append(nl)
    return doc, missing
