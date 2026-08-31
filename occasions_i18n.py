# -*- coding: utf-8 -*-
"""Vertaalde gelegenheid-pagina's (en/de/fr)."""

_OFFER = lambda lo, hi, n, desc: {"@type": "AggregateOffer", "priceCurrency": "EUR",
                                  "lowPrice": lo, "highPrice": hi, "offerCount": n,
                                  "description": desc}

EN = {

"vuurshow-bruiloft": {
 "title": "A fire show at your wedding",
 "seo_title": "\U0001F49B Wedding Fire Show | Romantic Alternative to Fireworks — from €450",
 "seo_desc": "A fire show at your wedding? A romantic 20-minute show at the first dance or evening opening — often allowed where fireworks are banned. 4.9/5 from 136 reviews. From €450.",
 "eyebrow": "Weddings",
 "img": ("/assets/media/bruiloft-1080.webp", "Duo fire act at a wedding: Nuno with a dancer with large red wings"),
 "body": """
<p><strong>A fire show at your wedding is the moment guests talk about for years: towering flames at the first dance or a spectacular opening of the evening party. Best of all: a fire show is often allowed exactly where fireworks are banned.</strong></p>
<h2>Why fire fits a wedding perfectly</h2>
<p>Fireworks are prohibited at most wedding venues in the Netherlands and Belgium. A professional fire show delivers the same wow moment — up close, personal and choreographed to your music. Nuno matches the act to your first dance and coordinates safety directly with the venue, so you have nothing to arrange.</p>
<h2>On your day</h2>
<ul>
<li><strong>The evening opening</strong> — a 20-minute show block full of fire breathing, fire juggling and body fire.</li>
<li><strong>At the first dance</strong> — flames and sparks framing your opening dance; a gift for your photographer.</li>
<li><strong>Duo with a fire dancer</strong> — extra romance and theatre, as in the photo above.</li>
<li><strong>Indoors or bad weather?</strong> — Nuno switches to <a href="/en/fakir-show/">the fakir show</a> or mentalism: just as unforgettable, without open fire.</li>
</ul>
<h2>What does it cost?</h2>
<p>The 20-minute wedding show block starts at <strong>€450</strong>; a 10-minute power act from <strong>€350</strong> — equipment, safe fuels, set-up and venue coordination included. See <a href="/en/fire-breather-prices/">all prices</a> or <a href="/en/contact/">check your wedding date</a> — you'll hear within 24 hours. With <a href="/en/about-nuno/">17 years of experience</a> and <a href="/en/reviews/">4.9/5 from 136 reviews</a>, Nuno performs across the Netherlands and Belgium.</p>
""",
 "faq": [
  ("How much does a wedding fire show cost?",
   "The popular 20-minute show block starts at €450 excluding travel; a 10-minute power act from €350. You always receive one all-in quote."),
  ("Is a fire show allowed where fireworks are banned?",
   "Usually yes: a fire act falls under the venue's own rules, not fireworks law. Nuno coordinates permits and safety distances directly with the venue."),
  ("Can the show accompany our first dance?",
   "Yes — the choreography is matched to your song, in consultation with your DJ or band."),
  ("What if it rains or the show must move indoors?",
   "Light rain is fine outdoors. Indoors without open fire, Nuno switches to the fakir show or mentalism — the spectacle stays."),
 ],
 "service": {"name": "Wedding fire show", "type": "Fire show",
   "desc": "Romantic fire show for weddings: evening opening or first dance, solo or duo with a fire dancer. Often allowed where fireworks are banned. From €450.",
   "offers": _OFFER("350", "750", "3", "Power act 10 min from €350, show block 20 min from €450, duo show from €700.")},
},

"vuurshow-bedrijfsfeest": {
 "title": "A fire show at your corporate event",
 "seo_title": "\U0001F525 Corporate Event Fire Show | Wow-factor Entertainment — from €450",
 "seo_desc": "Entertainment for your corporate event or staff party? A professional fire show as opening or grand finale impresses staff and clients alike. As seen on TV. From €450, quote within 24 hours.",
 "eyebrow": "Corporate events",
 "img": ("/assets/media/themafeest-1080.webp", "Fire breather Nuno at a corporate party in the evening"),
 "body": """
<p><strong>A company party people still talk about on Monday morning? A professional fire show as opening or grand finale gives your staff party, client event or anniversary exactly that wow moment — polished, safe and representative.</strong></p>
<h2>Why event managers book Nuno</h2>
<p>At a corporate event, reliability matters as much as spectacle. Nuno arrives with sharp costumes, clear communication and a show timed to the minute — 10, 20 or 30 minutes. With TV appearances for <a href="/en/about-nuno/">SBS6, RTL and VTM</a> and <a href="/en/reviews/">4.9/5 from 136 reviews</a>, you know what you're booking.</p>
<h2>Formats that work</h2>
<ul>
<li><strong>The opening</strong> — a 10-minute power act that sets the energy (from €350).</li>
<li><strong>The grand finale</strong> — a 20-minute show block just before the DJ or band (from €450).</li>
<li><strong>Team building</strong> — the team learns to breathe fire in the <a href="/en/fire-breathing-workshop/">workshop</a>.</li>
<li><strong>Indoor venue?</strong> — the <a href="/en/fakir-show/">fakir show</a> or mentalism deliver the spectacle without open fire.</li>
</ul>
<h2>Budget and booking</h2>
<p>Shows range from €350 to €1500 — see <a href="/en/fire-breather-prices/">all prices</a>. Invoicing with proper VAT specification. Send your date and venue via the <a href="/en/contact/">request form</a>: a quote within 24 hours. December party? Book early — those dates fill first.</p>
""",
 "faq": [
  ("How much does a corporate fire show cost?",
   "An opening act of 10 minutes from €350, a full 20-minute show block from €450, complete evening programmes up to €1500 — always one all-in quote, invoiced properly."),
  ("Is a fire show representative enough for clients and management?",
   "Yes — sharp costumes, professional communication and a choreographed show. Nuno has performed on national TV and for brands across the Benelux."),
  ("Can it take place at an office site or indoors?",
   "Outdoors almost always, including car parks and roof terraces; indoors when the venue and fire brigade allow it. Otherwise Nuno switches to acts without open fire."),
  ("Can we combine the show with a workshop?",
   "Certainly — a popular staff-party combo: the show as spectacle, then colleagues learn fire breathing under supervision. Ask for the combination rate."),
 ],
 "service": {"name": "Corporate event fire show", "type": "Fire show",
   "desc": "Professional fire show for corporate events, staff parties and client events: opening, grand finale or team-building workshop. As seen on TV. From €450, invoiced.",
   "offers": _OFFER("350", "1500", "4", "Opening 10 min from €350, show block 20 min from €450, full show from €595, evening programme up to €1500.")},
},

"vuurshow-verjaardag": {
 "title": "A fire show for a birthday or anniversary",
 "seo_title": "\U0001F389 Birthday Fire Show | Spectacle in Your Own Garden — from €350",
 "seo_desc": "Make a birthday or anniversary unforgettable: book a fire show at home — 10 to 20 minutes of spectacle in the garden or driveway. From €350, across the Netherlands and Belgium.",
 "eyebrow": "Birthdays & anniversaries",
 "img": ("/assets/media/avondvuur-1080.webp", "Fire breather Nuno blows an enormous fireball at dusk"),
 "body": """
<p><strong>For the birthday of someone who has everything, a 50th in the garden or a wedding anniversary: a fire show at home is the gift nobody sees coming — and nobody ever forgets.</strong></p>
<h2>Spectacle in your own garden</h2>
<p>A fire show needs surprisingly little space: a garden, driveway or the green in front of the house is often enough. Nuno assesses the spot in advance (a photo via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> usually suffices), brings everything himself and leaves the place tidy.</p>
<h2>Popular formulas</h2>
<ul>
<li><strong>The surprise act (10 min, from €350)</strong> — the birthday person knows nothing; suddenly there's a fire breather in the garden.</li>
<li><strong>The party block (20 min, from €450)</strong> — a full mini-show with fire breathing, juggling and interaction.</li>
<li><strong>With fakir elements</strong> — does the birthday person dare to stand on the <a href="/en/fakir-show/">bed of nails</a>?</li>
</ul>
<h2>When and where</h2>
<p>Fire looks best at dusk — around ten in summer, from five in winter. Nuno performs across the Netherlands and Belgium; see <a href="/en/fire-breather-prices/">all prices</a> or <a href="/en/contact/">check your date</a> — an answer within 24 hours. Prefer no fire? The <a href="/en/about-nuno/">reptile show or mentalism</a> are equally strong surprises.</p>
""",
 "faq": [
  ("How much does a birthday fire show cost?",
   "The 10-minute surprise act from €350, the full 20-minute party block from €450 — excluding travel, always with one all-in quote."),
  ("How much garden space is needed?",
   "Less than you think: a free circle of a few metres without overhanging branches usually suffices. Send a garden photo via WhatsApp and you'll hear straight away."),
  ("Can it be a complete surprise?",
   "Yes — the most popular formula. Everything is arranged quietly with the organiser; the birthday person sees Nuno only when the first fireball goes up."),
  ("Is it safe with children and elderly guests?",
   "Yes: fully certified, safe show fuels and a clear safety zone from which everyone can see everything perfectly."),
 ],
 "service": {"name": "Birthday and anniversary fire show", "type": "Fire show",
   "desc": "Fire show at home for birthdays and anniversaries: 10-minute surprise act or 20-minute party block in the garden. From €350, across the Netherlands and Belgium.",
   "offers": _OFFER("350", "750", "3", "Surprise act 10 min from €350, party block 20 min from €450, with fakir interaction from €595.")},
},

"vuurshow-festival": {
 "title": "Book a fire show for your festival",
 "seo_title": "\U0001F3AA Festival Fire Show | Up to 5 Sets a Day — Walibi Experience",
 "seo_desc": "A fire act for your festival or public event? Nuno plays up to 5 sets of 20 minutes a day, knows festival production from the Walibi Fright Nights and delivers a tight rider. €950–€1500 all-in.",
 "eyebrow": "Festivals & events",
 "img": ("/assets/media/festival-1600.webp", "Fire breather Nuno blows a fireball on a festival square for a large crowd"),
 "body": """
<p><strong>For festivals, fire is the ultimate crowd-puller: visible from afar, photogenic on every phone. Nuno runs festival programmes of up to five 20-minute sets a day — with the routine of the Walibi Fright Nights and festival Emporium.</strong></p>
<h2>Built for festival production</h2>
<p>Festivals demand tight set times, fast changeovers and safe work with a moving crowd. Nuno delivers a clear technical rider (playing circle, safety zone, coordination with production) and fits his sets to your schedule — daytime acts included, with fakir elements pulling crowds before dark.</p>
<h2>The festival package</h2>
<ul>
<li><strong>Up to 5 × 20 minutes a day</strong> — spread over afternoon and evening, €950–€1500 all-in.</li>
<li><strong>Roaming acts</strong> — short surprise moments across the site between sets.</li>
<li><strong>Halloween productions</strong> — a complete <a href="/en/halloween/">Halloween programme</a>, known from the Fright Nights.</li>
<li><strong>Multi-day or recurring</strong> — ask for multi-day rates.</li>
</ul>
<h2>Booking</h2>
<p>Festival summer and October fill far ahead. Send your dates and number of sets via the <a href="/en/contact/">request form</a> — a quote with rider within 24 hours. See <a href="/en/fire-breather-prices/">all prices</a>, the <a href="/en/videos/">showreels</a> and <a href="/en/reviews/">organisers' reviews</a>.</p>
""",
 "faq": [
  ("What does a festival fire act cost?",
   "The festival package with up to five 20-minute sets costs €950 to €1500 all-in, depending on sets and travel. A single set starts at €450."),
  ("What is in the technical rider?",
   "A free playing circle with safety zone, agreement on surface and crowd barriers where needed. No stage or power required; music coordination with the DJ is possible."),
  ("Does a fire show work in daylight?",
   "Yes — by day the fireballs and fakir elements pull the crowds; from dusk the full fire spectacle joins in."),
  ("How are permits handled on an event site?",
   "Nuno works within the organiser's event permit and supplies the required details on the act, fuels and safety measures on request."),
 ],
 "service": {"name": "Festival fire show", "type": "Fire show",
   "desc": "Festival package: up to five 20-minute fire sets a day, roaming acts and fakir option. Experienced at Walibi Fright Nights and Emporium. €950–€1500 all-in.",
   "offers": _OFFER("450", "1500", "3", "Single festival set from €450, day package up to 5×20 min €950–€1500, multi-day on request.")},
},

"vrijgezellenfeest": {
 "title": "Bachelor party: fire-breathing workshop",
 "seo_title": "\U0001F525 Bachelor Party Activity | Fire-Breathing Workshop — Nothing More Original",
 "seo_desc": "Looking for an original bachelor(ette) party activity? Learn fire breathing with the whole group under professional guidance — photos of everyone's first fireball included. From €350.",
 "eyebrow": "Bachelor parties",
 "img": ("/assets/media/workshop-1125.webp", "Workshop participant blows a large fireball against the evening sky"),
 "body": """
<p><strong>Another go-kart day? Or give the groom or bride a story that will be told at the wedding itself: the whole group learns fire breathing under professional guidance — with photos of everyone's first fireball as proof.</strong></p>
<h2>How the workshop works</h2>
<p>Safety first: fuels, technique and protection. Then practising without fire, and whoever is ready blows their first real fireball under Nuno's direct supervision. The workshop lasts one to two hours and ends — of course — with the bachelor setting the biggest fireball of the day.</p>
<h2>Why this is THE bachelor party</h2>
<ul>
<li><strong>Nothing more original</strong> — nobody in the group has done this before.</li>
<li><strong>For every group</strong> — 4 to 20 people; whoever doesn't dare, takes the photos.</li>
<li><strong>Anywhere in NL & BE</strong> — Nuno brings all materials to your city; only some open outdoor space is needed.</li>
<li><strong>Combine with a show</strong> — first watch <a href="/en/fire-show/">how it's really done</a>, then try it yourself.</li>
</ul>
<h2>Prices and booking</h2>
<p>The workshop starts at <strong>€350</strong> per group, materials and guidance included — see <a href="/en/fire-breathing-workshop/">the workshop page</a> and <a href="/en/fire-breather-prices/">all prices</a>. Weekend dates fill fast: <a href="/en/contact/">check your date</a> or send a <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>. One firm rule: participants stay sober until after the workshop — the drinks come later.</p>
""",
 "faq": [
  ("What does a bachelor party fire workshop cost?",
   "From €350 per group, including materials, fuels and guidance, excluding travel. A combo with a mini fire show beforehand is possible."),
  ("How big can the group be?",
   "Four to about twenty people works best; larger groups are split into rounds so everyone gets personal guidance."),
  ("Isn't it dangerous?",
   "Under professional guidance it is very doable: technique without fire first, then step by step. One hard rule: you take part sober — drinks come afterwards."),
  ("Do we get photos?",
   "Yes — every participant's first fireball is captured. Legendary material for the group chat and the wedding speech."),
 ],
 "service": {"name": "Bachelor party fire-breathing workshop", "type": "Fire-breathing workshop",
   "desc": "Original bachelor(ette) activity: the whole group learns fire breathing under professional guidance, photos included. From €350, across the Netherlands and Belgium.",
   "offers": _OFFER("350", "750", "2", "Workshop from €350 per group; combo with mini fire show on request.")},
},

"vuurwerk-alternatief": {
 "title": "Fireworks banned? Book a fire show",
 "seo_title": "\U0001F386 Alternative to Fireworks | A Fire Show: Allowed and Just as Spectacular",
 "seo_desc": "Fireworks banned at your venue or municipality? A professional fire show delivers the same spectacle — closer, quieter, without permit stress. THE alternative for weddings and events.",
 "eyebrow": "Fireworks alternative",
 "img": ("/assets/media/vuurbal-1333.webp", "Towering fireball against a black night sky above fire breather Nuno"),
 "body": """
<p><strong>More and more municipalities in the Netherlands and Belgium restrict or ban consumer fireworks, and most venues never allowed them. The good news: there is an alternative that is at least as spectacular — and usually simply permitted.</strong></p>
<h2>Why a fire show is often allowed where fireworks are not</h2>
<p>Fireworks fall under strict launch rules and permits; a professional fire act falls under the venue's own event rules and works with controlled fire at eye level — no bangs, no projectiles, no debris. Nuno coordinates with the venue in advance and keeps the prescribed safety distances.</p>
<h2>Fire show versus fireworks</h2>
<ul>
<li><strong>Up close</strong> — guests stand metres from towering fireballs.</li>
<li><strong>Quieter</strong> — no bangs: suitable for residential areas, campsites and pets nearby.</li>
<li><strong>Longer</strong> — not thirty seconds of sparkle but a 10–30 minute show on your music.</li>
<li><strong>Weatherproof</strong> — a fire show goes ahead in wind and light rain.</li>
</ul>
<h2>For which moments</h2>
<p>Popular at <a href="/en/fire-show-wedding/">weddings</a> (a grand finale instead of fireworks), <a href="/en/christmas-new-year-entertainment/">New Year's Eve and receptions</a>, <a href="/en/fire-show-corporate-event/">corporate events</a> and public events that cannot get a fireworks permit. A closing show costs between €350 and €595 — see <a href="/en/fire-breather-prices/">all prices</a> or <a href="/en/contact/">request a quote</a>; an answer within 24 hours.</p>
""",
 "faq": [
  ("Is a fire show really allowed where fireworks are banned?",
   "Usually yes: a professional fire act falls under the venue's or event's rules, not fireworks law. Nuno coordinates this directly with the venue in advance."),
  ("Is it as spectacular as fireworks?",
   "Different and closer: towering fireballs metres away, on music and with interaction — guests experience it more intensely than fireworks a hundred metres up."),
  ("What does it cost?",
   "Between €350 and €595 for a 10–30 minute closing show — usually far cheaper than professional display fireworks including the permit process."),
  ("Does it work for New Year's Eve?",
   "Especially then: a countdown show to midnight is the perfect replacement for fireworks — do book December well ahead."),
 ],
 "service": {"name": "Fire show as fireworks alternative", "type": "Fire show",
   "desc": "Spectacular, permitted alternative to fireworks at weddings, New Year's Eve and events: a 10–30 minute fire show, quieter, closer, without permit stress. From €350.",
   "offers": _OFFER("350", "750", "3", "Closing act 10 min from €350, show block 20 min from €450, full finale 30 min from €595.")},
},

"kerst-nieuwjaar-entertainment": {
 "title": "Christmas party & New Year entertainment",
 "seo_title": "\U0001F384 Christmas & New Year Entertainment | A Fire Show in the Winter Dark",
 "seo_desc": "Entertainment for your Christmas party, staff event or New Year's reception? In the dark winter months a fire show reaches full effect. December fills early — book in time. From €450.",
 "eyebrow": "Christmas & New Year",
 "img": ("/assets/media/schemering-640.webp", "Fire breathing in the early winter dusk, the flame fanning out wide"),
 "body": """
<p><strong>December is the best month for fire: dark by five o'clock, guests outside by the fire baskets — and then Nuno opens the evening with towering flames. For Christmas parties, staff events and New Year receptions, a fire show is the winter spectacle par excellence.</strong></p>
<h2>Why fire and winter belong together</h2>
<p>In summer a fire show waits until after ten; in December the full effect starts in the late afternoon. The heat of the flames, sparks against the winter sky, guests with mulled wine at a safe distance — and snow or light rain is no problem for a professional act.</p>
<h2>For every December party</h2>
<ul>
<li><strong>The Christmas party</strong> — a 20-minute show block as the highlight of the <a href="/en/fire-show-corporate-event/">company evening</a>, from €450.</li>
<li><strong>The New Year reception</strong> — open the year with fire: a powerful 10-minute act, from €350.</li>
<li><strong>New Year's Eve</strong> — the countdown show as an <a href="/en/fireworks-alternative/">alternative to fireworks</a>.</li>
<li><strong>Indoors as well</strong> — the <a href="/en/fakir-show/">fakir show</a> or mentalism inside, fire outside as the highlight.</li>
</ul>
<h2>December fills first</h2>
<p>The Thursdays and Fridays of December are booked earliest every year — companies plan in September and October. <a href="/en/contact/">Check your date now</a>; an answer within 24 hours. All packages are in the <a href="/en/fire-breather-prices/">price overview</a>.</p>
""",
 "faq": [
  ("What does Christmas or New Year entertainment cost?",
   "An opening act of 10 minutes from €350, the full 20-minute show block from €450 — companies receive one all-in quote, properly invoiced."),
  ("Does a fire show work in cold, rain or snow?",
   "Yes — cold and light precipitation are no problem; in the dark the show only gets more spectacular. Only in storm is an alternative arranged."),
  ("How early should we book a December party?",
   "The Thursday and Friday evenings of December are largely full by early autumn. Book before October if possible."),
  ("Is it suitable as a fireworks replacement on New Year's Eve?",
   "Yes — the countdown show to midnight is quieter, safer and more personal than fireworks, and usually permitted."),
 ],
 "service": {"name": "Christmas and New Year fire show", "type": "Fire show",
   "desc": "Winter spectacle for Christmas parties, staff events, New Year receptions and New Year's Eve: a fire show in the early winter dark, also as a fireworks alternative. From €450.",
   "offers": _OFFER("350", "1500", "4", "New Year act 10 min from €350, Christmas show block 20 min from €450, full show from €595, multiple sets up to €1500.")},
},
}

DE = {

"vuurshow-bruiloft": {
 "title": "Feuershow auf Ihrer Hochzeit",
 "seo_title": "\U0001F49B Feuershow Hochzeit | Romantische Feuerwerk-Alternative — ab 450 €",
 "seo_desc": "Feuershow auf der Hochzeit? Eine romantische 20-Minuten-Show zum Eröffnungstanz oder Abendauftakt — oft erlaubt, wo Feuerwerk verboten ist. 4,9/5 aus 136 Bewertungen. Ab 450 €.",
 "eyebrow": "Hochzeiten",
 "img": ("/assets/media/bruiloft-1080.webp", "Duo-Feueract auf einer Hochzeit: Nuno mit Tänzerin mit großen roten Flügeln"),
 "body": """
<p><strong>Eine Feuershow auf der Hochzeit ist der Moment, über den Gäste noch Jahre sprechen: meterhohe Flammen beim Eröffnungstanz oder ein spektakulärer Auftakt der Abendfeier. Das Beste: Eine Feuershow ist oft genau dort erlaubt, wo Feuerwerk verboten ist.</strong></p>
<h2>Warum Feuer perfekt zur Hochzeit passt</h2>
<p>Feuerwerk ist an den meisten Hochzeitslocations nicht mehr erlaubt. Eine professionelle Feuershow liefert denselben Wow-Moment — nah, persönlich und choreografiert auf Ihre Musik. Nuno stimmt den Act auf Ihren Eröffnungstanz ab und klärt die Sicherheit direkt mit der Location.</p>
<h2>An Ihrem Tag</h2>
<ul>
<li><strong>Der Abendauftakt</strong> — ein 20-Minuten-Showblock mit Feuerspucken, Feuerjonglage und Body Fire.</li>
<li><strong>Beim Eröffnungstanz</strong> — Flammen und Funken rahmen Ihren Tanz; ein Geschenk für den Fotografen.</li>
<li><strong>Duo mit Feuertänzerin</strong> — extra Romantik und Theater, wie auf dem Foto oben.</li>
<li><strong>Drinnen oder schlechtes Wetter?</strong> — dann wechselt Nuno zur <a href="/de/fakirshow/">Fakirshow</a> oder zum Mentalismus.</li>
</ul>
<h2>Was kostet das?</h2>
<p>Der 20-Minuten-Showblock beginnt bei <strong>450 €</strong>, ein 10-Minuten-Power-Act bei <strong>350 €</strong> — Material, sichere Brennstoffe, Auf- und Abbau inklusive. Alle Preise im <a href="/de/feuerspucker-kosten/">Preisüberblick</a>; <a href="/de/kontakt/">prüfen Sie Ihren Hochzeitstermin</a> — Antwort innerhalb von 24 Stunden. Mit <a href="/de/ueber-nuno/">17 Jahren Erfahrung</a> und <a href="/de/bewertungen/">4,9/5 aus 136 Bewertungen</a> spielt Nuno in NRW, der Grenzregion und den ganzen Niederlanden und Belgien.</p>
""",
 "faq": [
  ("Was kostet eine Feuershow auf der Hochzeit?",
   "Der beliebte 20-Minuten-Showblock ab 450 € zzgl. Anfahrt; ein 10-Minuten-Power-Act ab 350 €. Sie erhalten immer ein All-in-Angebot."),
  ("Ist eine Feuershow erlaubt, wo Feuerwerk verboten ist?",
   "Meistens ja: Ein Feueract fällt unter die Regeln der Location, nicht unter das Feuerwerksrecht. Nuno stimmt Genehmigungen und Sicherheitsabstände direkt mit der Location ab."),
  ("Kann die Show den Eröffnungstanz begleiten?",
   "Ja — die Choreografie wird auf Ihr Lied abgestimmt, in Absprache mit DJ oder Band."),
  ("Was passiert bei Regen?",
   "Leichter Regen ist draußen kein Problem. Drinnen ohne offenes Feuer wechselt Nuno zu Fakirshow oder Mentalismus."),
 ],
 "service": {"name": "Feuershow auf einer Hochzeit", "type": "Feuershow",
   "desc": "Romantische Feuershow für Hochzeiten: Abendauftakt oder Eröffnungstanz, solo oder als Duo mit Feuertänzerin. Oft erlaubt, wo Feuerwerk verboten ist. Ab 450 €.",
   "offers": _OFFER("350", "750", "3", "Power-Act 10 Min ab 350 €, Showblock 20 Min ab 450 €, Duo-Show ab 700 €.")},
},

"vuurshow-bedrijfsfeest": {
 "title": "Feuershow auf Ihrer Firmenfeier",
 "seo_title": "\U0001F525 Feuershow Firmenfeier | Entertainment mit Wow-Faktor — ab 450 €",
 "seo_desc": "Entertainment für Firmenfeier oder Betriebsfest? Eine professionelle Feuershow als Eröffnung oder Finale beeindruckt Mitarbeiter und Kunden. Bekannt aus dem TV. Ab 450 €, Angebot in 24 Stunden.",
 "eyebrow": "Firmenfeiern",
 "img": ("/assets/media/themafeest-1080.webp", "Feuerspucker Nuno bei einer Firmenfeier am Abend"),
 "body": """
<p><strong>Eine Firmenfeier, über die am Montagmorgen noch gesprochen wird? Eine professionelle Feuershow als Eröffnung oder großes Finale gibt Ihrem Betriebsfest, Kundenevent oder Jubiläum genau diesen Wow-Moment — souverän, sicher und repräsentativ.</strong></p>
<h2>Warum Eventmanager Nuno buchen</h2>
<p>Bei Firmenevents zählt Verlässlichkeit ebenso wie Spektakel: klare Kommunikation, elegante Kostüme, eine minutengenaue Show von 10, 20 oder 30 Minuten. Mit TV-Auftritten bei <a href="/de/ueber-nuno/">SBS6, RTL und VTM</a> und <a href="/de/bewertungen/">4,9/5 aus 136 Bewertungen</a> wissen Sie, wen Sie buchen.</p>
<h2>Formate, die funktionieren</h2>
<ul>
<li><strong>Die Eröffnung</strong> — ein 10-Minuten-Power-Act (ab 350 €).</li>
<li><strong>Das große Finale</strong> — ein 20-Minuten-Showblock direkt vor DJ oder Band (ab 450 €).</li>
<li><strong>Teambuilding</strong> — das Team lernt im <a href="/de/feuerspucker-workshop/">Workshop</a> selbst Feuerspucken.</li>
<li><strong>Indoor-Location?</strong> — die <a href="/de/fakirshow/">Fakirshow</a> oder Mentalismus liefern Spektakel ohne offenes Feuer.</li>
</ul>
<h2>Budget und Buchung</h2>
<p>Shows kosten 350 bis 1500 € — siehe <a href="/de/feuerspucker-kosten/">Preisüberblick</a>; Rechnung mit ordentlicher MwSt.-Ausweisung. Senden Sie Termin und Ort über das <a href="/de/kontakt/">Anfrageformular</a>: Angebot innerhalb von 24 Stunden. Weihnachtsfeier? Diese Termine sind zuerst weg — <a href="/de/weihnachtsfeier-silvester-show/">früh buchen</a>.</p>
""",
 "faq": [
  ("Was kostet eine Feuershow auf einer Firmenfeier?",
   "Eröffnungsact 10 Min ab 350 €, kompletter Showblock 20 Min ab 450 €, ganze Abendprogramme bis 1500 € — immer ein All-in-Angebot auf Rechnung."),
  ("Ist eine Feuershow repräsentativ genug für Kunden und Geschäftsleitung?",
   "Ja — elegante Kostüme, professionelle Abstimmung und eine choreografierte Show. Nuno stand im nationalen Fernsehen und spielt für Marken in der ganzen Benelux und NRW."),
  ("Geht das auch auf dem Firmengelände oder drinnen?",
   "Draußen fast immer, auch auf Parkplätzen und Dachterrassen; drinnen, sobald Location und Feuerwehr zustimmen. Sonst wechselt Nuno zu Acts ohne offenes Feuer."),
  ("Können wir Show und Workshop kombinieren?",
   "Gern — die beliebte Kombination: erst die Show, danach lernen Kollegen unter Anleitung selbst Feuerspucken. Fragen Sie nach dem Kombitarif."),
 ],
 "service": {"name": "Feuershow auf einer Firmenfeier", "type": "Feuershow",
   "desc": "Professionelle Feuershow für Firmenfeiern, Betriebsfeste und Kundenevents: Eröffnung, Finale oder Teambuilding-Workshop. Bekannt aus dem TV. Ab 450 €, auf Rechnung.",
   "offers": _OFFER("350", "1500", "4", "Eröffnung 10 Min ab 350 €, Showblock 20 Min ab 450 €, komplette Show ab 595 €, Abendprogramm bis 1500 €.")},
},

"vuurshow-verjaardag": {
 "title": "Feuershow zum Geburtstag oder Jubiläum",
 "seo_title": "\U0001F389 Feuershow Geburtstag | Spektakel im eigenen Garten — ab 350 €",
 "seo_desc": "Einen Geburtstag oder ein Jubiläum unvergesslich machen? Feuershow zu Hause: 10 bis 20 Minuten Spektakel im Garten oder in der Einfahrt. Ab 350 €, NRW, Grenzregion, NL & BE.",
 "eyebrow": "Geburtstage & Jubiläen",
 "img": ("/assets/media/avondvuur-1080.webp", "Feuerspucker Nuno spuckt einen riesigen Feuerball in der Abenddämmerung"),
 "body": """
<p><strong>Für den Geburtstag von jemandem, der schon alles hat, einen runden Geburtstag im Garten oder ein Ehejubiläum: Eine Feuershow zu Hause ist das Geschenk, das niemand kommen sieht — und niemand je vergisst.</strong></p>
<h2>Spektakel im eigenen Garten</h2>
<p>Eine Feuershow braucht überraschend wenig Platz: Garten, Einfahrt oder die Wiese vor dem Haus genügen oft. Nuno beurteilt den Ort vorab (ein Foto per <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> reicht meist), bringt alles mit und hinterlässt den Platz ordentlich.</p>
<h2>Beliebte Formeln</h2>
<ul>
<li><strong>Der Überraschungsact (10 Min, ab 350 €)</strong> — das Geburtstagskind weiß von nichts; plötzlich steht ein Feuerspucker im Garten.</li>
<li><strong>Der Festblock (20 Min, ab 450 €)</strong> — eine komplette Mini-Show mit Feuerspucken, Jonglage und Interaktion.</li>
<li><strong>Mit Fakir-Elementen</strong> — traut sich das Geburtstagskind auf das <a href="/de/fakirshow/">Nagelbett</a>?</li>
</ul>
<h2>Wann und wo</h2>
<p>Feuer wirkt am schönsten in der Dämmerung — im Sommer gegen zehn, im Winter ab fünf. Nuno spielt in NRW, der Grenzregion und den ganzen Niederlanden und Belgien; alle Preise im <a href="/de/feuerspucker-kosten/">Überblick</a>, Termin prüfen über das <a href="/de/kontakt/">Formular</a> — Antwort innerhalb von 24 Stunden.</p>
""",
 "faq": [
  ("Was kostet eine Feuershow zum Geburtstag?",
   "Der Überraschungsact von 10 Minuten ab 350 €, der komplette Festblock von 20 Minuten ab 450 € — zzgl. Anfahrt, immer mit All-in-Angebot vorab."),
  ("Wie viel Platz braucht es im Garten?",
   "Weniger als gedacht: ein freier Kreis von wenigen Metern ohne überhängende Äste genügt oft. Senden Sie ein Gartenfoto per WhatsApp."),
  ("Geht es als komplette Überraschung?",
   "Ja — die beliebteste Formel. Alles wird still mit dem Organisator abgestimmt; das Geburtstagskind sieht Nuno erst beim ersten Feuerball."),
  ("Ist es mit Kindern und älteren Gästen sicher?",
   "Ja: voll zertifiziert, sichere Showbrennstoffe und eine klare Sicherheitszone, aus der alle alles sehen."),
 ],
 "service": {"name": "Feuershow zum Geburtstag oder Jubiläum", "type": "Feuershow",
   "desc": "Feuershow zu Hause für Geburtstage und Jubiläen: Überraschungsact von 10 Minuten oder Festblock von 20 Minuten im Garten. Ab 350 €.",
   "offers": _OFFER("350", "750", "3", "Überraschungsact 10 Min ab 350 €, Festblock 20 Min ab 450 €, mit Fakir-Interaktion ab 595 €.")},
},

"vuurshow-festival": {
 "title": "Feuershow für Ihr Festival buchen",
 "seo_title": "\U0001F3AA Feuershow Festival | Bis zu 5 Sets pro Tag — Walibi-Erfahrung",
 "seo_desc": "Ein Feueract für Festival oder Publikumsevent? Nuno spielt bis zu 5 Sets à 20 Minuten pro Tag, kennt die Festivalpraxis der Walibi Fright Nights und liefert einen klaren Rider. 950–1500 € all-in.",
 "eyebrow": "Festivals & Events",
 "img": ("/assets/media/festival-1600.webp", "Feuerspucker Nuno spuckt einen Feuerball auf einem Festivalplatz vor großem Publikum"),
 "body": """
<p><strong>Auf Festivals ist Feuer der ultimative Publikumsmagnet: von weitem sichtbar, fotogen auf jedem Handy. Nuno spielt Festivalprogramme mit bis zu fünf Sets à zwanzig Minuten pro Tag — mit der Routine der Walibi Fright Nights und des Festivals Emporium.</strong></p>
<h2>Gemacht für die Festivalpraxis</h2>
<p>Festivals verlangen enge Setzeiten, schnelle Wechsel und sicheres Arbeiten mit Publikum. Nuno liefert einen klaren technischen Rider (Spielkreis, Sicherheitszone, Abstimmung mit der Produktion) und passt die Sets an Ihren Zeitplan an — auch tagsüber, mit Fakir-Elementen als Publikumsmagnet vor der Dunkelheit.</p>
<h2>Das Festivalpaket</h2>
<ul>
<li><strong>Bis zu 5 × 20 Minuten pro Tag</strong> — verteilt über Nachmittag und Abend, 950–1500 € all-in.</li>
<li><strong>Roaming-Acts</strong> — kurze Überraschungsmomente auf dem Gelände zwischen den Sets.</li>
<li><strong>Halloween-Produktionen</strong> — ein komplettes <a href="/de/halloween/">Halloween-Programm</a>, bekannt von den Fright Nights.</li>
<li><strong>Mehrtägig oder jährlich</strong> — fragen Sie nach Mehrtagestarifen.</li>
</ul>
<h2>Buchung</h2>
<p>Festivalsommer und Oktober sind früh ausgebucht. Senden Sie Termine und Setanzahl über das <a href="/de/kontakt/">Anfrageformular</a> — Angebot mit Rider innerhalb von 24 Stunden. Alle Preise im <a href="/de/feuerspucker-kosten/">Überblick</a>, dazu <a href="/de/videos/">Showreels</a> und <a href="/de/bewertungen/">Bewertungen von Veranstaltern</a>.</p>
""",
 "faq": [
  ("Was kostet ein Feueract auf einem Festival?",
   "Das Festivalpaket mit bis zu fünf Sets à 20 Minuten kostet 950 bis 1500 € all-in, je nach Setanzahl und Anfahrt. Ein einzelnes Set ab 450 €."),
  ("Was steht im technischen Rider?",
   "Ein freier Spielkreis mit Sicherheitszone, Abstimmung zu Untergrund und Absperrungen. Bühne und Strom sind nicht nötig; Musikabstimmung mit dem DJ ist möglich."),
  ("Funktioniert eine Feuershow auch bei Tageslicht?",
   "Ja — tagsüber ziehen Feuerbälle und Fakir-Elemente das Publikum; ab der Dämmerung kommt das volle Feuerspektakel dazu."),
  ("Wie laufen Genehmigungen auf dem Eventgelände?",
   "Nuno arbeitet innerhalb der Veranstaltungsgenehmigung des Organisators und liefert auf Wunsch alle nötigen Angaben zu Act, Brennstoffen und Sicherheitsmaßnahmen."),
 ],
 "service": {"name": "Feuershow auf einem Festival", "type": "Feuershow",
   "desc": "Festivalpaket: bis zu fünf Feuersets à 20 Minuten pro Tag, Roaming-Acts und Fakir-Option. Erfahrung von Walibi Fright Nights und Emporium. 950–1500 € all-in.",
   "offers": _OFFER("450", "1500", "3", "Einzelset ab 450 €, Tagespaket bis 5×20 Min 950–1500 €, mehrtägig auf Anfrage.")},
},

"vrijgezellenfeest": {
 "title": "Junggesellenabschied: Feuerspucker-Workshop",
 "seo_title": "\U0001F525 Junggesellenabschied Idee | Feuerspucker-Workshop — Origineller geht nicht",
 "seo_desc": "Eine originelle JGA-Aktivität gesucht? Lernen Sie mit der ganzen Gruppe Feuerspucken unter professioneller Anleitung — mit Fotos vom ersten Feuerball. Ab 350 €, NL, BE & Grenzregion.",
 "eyebrow": "Junggesellenabschiede",
 "img": ("/assets/media/workshop-1125.webp", "Workshop-Teilnehmer bläst einen großen Feuerball gegen den Abendhimmel"),
 "body": """
<p><strong>Noch einmal Kartfahren? Oder schenken Sie dem Bräutigam oder der Braut eine Geschichte, die auf der Hochzeit selbst erzählt wird: Die ganze Gruppe lernt Feuerspucken unter professioneller Anleitung — mit Fotos vom ersten Feuerball als Beweis.</strong></p>
<h2>So läuft der Workshop</h2>
<p>Zuerst Sicherheit: Brennstoffe, Technik, Schutz. Dann Üben ohne Feuer — und wer bereit ist, spuckt unter Nunos direkter Anleitung seinen ersten echten Feuerball. Der Workshop dauert ein bis zwei Stunden und endet natürlich damit, dass der Junggeselle den größten Feuerball des Tages setzt.</p>
<h2>Warum das DER Junggesellenabschied ist</h2>
<ul>
<li><strong>Origineller geht nicht</strong> — das hat noch niemand aus der Gruppe gemacht.</li>
<li><strong>Für jede Gruppe</strong> — 4 bis 20 Personen; wer sich nicht traut, fotografiert.</li>
<li><strong>Überall in NL, BE und der Grenzregion</strong> — Nuno bringt alles mit; nur etwas freie Außenfläche wird gebraucht.</li>
<li><strong>Mit Show kombinieren</strong> — erst sehen, <a href="/de/feuershow/">wie es richtig geht</a>, dann selbst probieren.</li>
</ul>
<h2>Preise und Buchung</h2>
<p>Der Workshop beginnt bei <strong>350 €</strong> pro Gruppe, Material und Anleitung inklusive — siehe <a href="/de/feuerspucker-workshop/">Workshopseite</a> und <a href="/de/feuerspucker-kosten/">Preisüberblick</a>. Wochenendtermine sind schnell weg: <a href="/de/kontakt/">Termin prüfen</a> oder direkt per <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>. Eine feste Regel: Teilgenommen wird nüchtern — getrunken wird danach.</p>
""",
 "faq": [
  ("Was kostet ein Feuerspucker-Workshop für einen JGA?",
   "Ab 350 € pro Gruppe, inklusive Material, Brennstoffen und Anleitung, zzgl. Anfahrt. Eine Kombination mit einer Mini-Feuershow vorab ist möglich."),
  ("Wie groß darf die Gruppe sein?",
   "Vier bis etwa zwanzig Personen; größere Gruppen werden in Runden aufgeteilt, damit jeder persönliche Anleitung bekommt."),
  ("Ist das nicht gefährlich?",
   "Unter professioneller Anleitung gut machbar: erst Technik ohne Feuer, dann Schritt für Schritt. Eine harte Regel: nüchtern teilnehmen — getrunken wird danach."),
  ("Bekommen wir Fotos?",
   "Ja — der erste Feuerball jedes Teilnehmers wird festgehalten. Legendäres Material für die Gruppe und die Hochzeitsrede."),
 ],
 "service": {"name": "Feuerspucker-Workshop für den Junggesellenabschied", "type": "Feuerspucker-Workshop",
   "desc": "Originelle JGA-Aktivität: Die ganze Gruppe lernt Feuerspucken unter professioneller Anleitung, Fotos inklusive. Ab 350 €.",
   "offers": _OFFER("350", "750", "2", "Workshop ab 350 € pro Gruppe; Kombination mit Mini-Feuershow auf Anfrage.")},
},

"vuurwerk-alternatief": {
 "title": "Feuerwerk verboten? Buchen Sie eine Feuershow",
 "seo_title": "\U0001F386 Feuerwerk-Alternative | Feuershow: erlaubt und genauso spektakulär",
 "seo_desc": "Feuerwerk an Ihrer Location oder in Ihrer Gemeinde verboten? Eine professionelle Feuershow liefert dasselbe Spektakel — näher, leiser, ohne Genehmigungsstress. DIE Alternative für Hochzeiten und Events.",
 "eyebrow": "Feuerwerk-Alternative",
 "img": ("/assets/media/vuurbal-1333.webp", "Meterhoher Feuerball vor schwarzem Nachthimmel über Feuerspucker Nuno"),
 "body": """
<p><strong>Immer mehr Gemeinden beschränken oder verbieten Feuerwerk, und an den meisten Locations war es nie erlaubt. Die gute Nachricht: Es gibt eine Alternative, die mindestens genauso spektakulär ist — und meist einfach erlaubt.</strong></p>
<h2>Warum eine Feuershow oft erlaubt ist, wo Feuerwerk nicht darf</h2>
<p>Feuerwerk unterliegt strengen Abbrennregeln und Genehmigungen; ein professioneller Feueract fällt unter die Regeln der Location und arbeitet mit kontrolliertem Feuer auf Augenhöhe — ohne Knall, ohne Projektile, ohne Müll. Nuno stimmt alles vorab mit der Location ab und hält die vorgeschriebenen Sicherheitsabstände ein.</p>
<h2>Feuershow gegen Feuerwerk</h2>
<ul>
<li><strong>Nah dran</strong> — Gäste stehen wenige Meter von meterhohen Feuerbällen.</li>
<li><strong>Leiser</strong> — kein Knallen: geeignet für Wohngebiete, Campingplätze und Tiere in der Nähe.</li>
<li><strong>Länger</strong> — keine dreißig Sekunden Funken, sondern eine Show von 10–30 Minuten auf Ihrer Musik.</li>
<li><strong>Wetterfest</strong> — eine Feuershow läuft auch bei Wind und leichtem Regen.</li>
</ul>
<h2>Für welche Momente</h2>
<p>Beliebt bei <a href="/de/feuershow-hochzeit/">Hochzeiten</a> (großes Finale statt Feuerwerk), <a href="/de/weihnachtsfeier-silvester-show/">Silvester und Neujahrsempfängen</a>, <a href="/de/feuershow-firmenfeier/">Firmenfeiern</a> und öffentlichen Events ohne Feuerwerksgenehmigung. Eine Abschluss-Show kostet 350 bis 595 € — siehe <a href="/de/feuerspucker-kosten/">Preise</a> oder <a href="/de/kontakt/">Angebot anfragen</a>; Antwort innerhalb von 24 Stunden.</p>
""",
 "faq": [
  ("Ist eine Feuershow wirklich erlaubt, wo Feuerwerk verboten ist?",
   "Meistens ja: Ein professioneller Feueract fällt unter die Regeln der Location oder des Events, nicht unter das Feuerwerksrecht. Nuno stimmt das vorab direkt ab."),
  ("Ist es so spektakulär wie Feuerwerk?",
   "Anders und näher: meterhohe Feuerbälle wenige Meter entfernt, auf Musik und mit Interaktion — intensiver als Feuerwerk in hundert Metern Höhe."),
  ("Was kostet es?",
   "Zwischen 350 und 595 € für eine Abschluss-Show von 10–30 Minuten — meist deutlich günstiger als professionelles Höhenfeuerwerk samt Genehmigungsverfahren."),
  ("Funktioniert das auch an Silvester?",
   "Gerade dann: Die Countdown-Show zu Mitternacht ist der perfekte Feuerwerksersatz — Dezember früh buchen."),
 ],
 "service": {"name": "Feuershow als Feuerwerk-Alternative", "type": "Feuershow",
   "desc": "Spektakuläre, erlaubte Alternative zum Feuerwerk bei Hochzeiten, Silvester und Events: Feuershow von 10–30 Minuten, leiser, näher, ohne Genehmigungsstress. Ab 350 €.",
   "offers": _OFFER("350", "750", "3", "Abschlussact 10 Min ab 350 €, Showblock 20 Min ab 450 €, großes Finale 30 Min ab 595 €.")},
},

"kerst-nieuwjaar-entertainment": {
 "title": "Show für Weihnachtsfeier & Silvester",
 "seo_title": "\U0001F384 Weihnachtsfeier & Silvester Show | Feuershow im Winterdunkel",
 "seo_desc": "Entertainment für Weihnachtsfeier, Betriebsfest oder Neujahrsempfang? In den dunklen Wintermonaten wirkt eine Feuershow maximal. Der Dezember ist früh ausgebucht. Ab 450 €.",
 "eyebrow": "Weihnachten & Silvester",
 "img": ("/assets/media/schemering-640.webp", "Feuerspucken in der frühen Winterdämmerung, die Flamme fächert breit auf"),
 "body": """
<p><strong>Der Dezember ist der schönste Monat für Feuer: Um fünf ist es dunkel, die Gäste stehen draußen an den Feuerkörben — und dann eröffnet Nuno den Abend mit meterhohen Flammen. Für Weihnachtsfeiern, Betriebsfeste und Neujahrsempfänge ist eine Feuershow das Winterspektakel schlechthin.</strong></p>
<h2>Warum Feuer und Winter zusammengehören</h2>
<p>Im Sommer wartet eine Feuershow bis nach zehn; im Dezember beginnt die volle Wirkung schon am späten Nachmittag. Die Wärme der Flammen, Funkenregen gegen den Winterhimmel, Gäste mit Glühwein in sicherem Abstand — und Schnee oder leichter Regen sind kein Problem.</p>
<h2>Für jedes Dezemberfest</h2>
<ul>
<li><strong>Die Weihnachtsfeier</strong> — ein 20-Minuten-Showblock als Höhepunkt der <a href="/de/feuershow-firmenfeier/">Firmenfeier</a>, ab 450 €.</li>
<li><strong>Der Neujahrsempfang</strong> — das Jahr mit Feuer eröffnen: ein starker 10-Minuten-Act ab 350 €.</li>
<li><strong>Silvester</strong> — die Countdown-Show als <a href="/de/feuerwerk-alternative/">Feuerwerk-Alternative</a>.</li>
<li><strong>Drinnen dazu</strong> — <a href="/de/fakirshow/">Fakirshow</a> oder Mentalismus im Saal, Feuer draußen als Höhepunkt.</li>
</ul>
<h2>Der Dezember ist zuerst weg</h2>
<p>Die Donnerstage und Freitage im Dezember sind jedes Jahr am frühesten ausgebucht — Firmen planen im September und Oktober. <a href="/de/kontakt/">Prüfen Sie jetzt Ihren Termin</a>; Antwort innerhalb von 24 Stunden. Alle Pakete im <a href="/de/feuerspucker-kosten/">Preisüberblick</a>.</p>
""",
 "faq": [
  ("Was kostet Entertainment für Weihnachtsfeier oder Neujahrsempfang?",
   "Ein Eröffnungsact von 10 Minuten ab 350 €, der komplette Showblock von 20 Minuten ab 450 € — Firmen erhalten ein All-in-Angebot auf Rechnung."),
  ("Funktioniert eine Feuershow bei Kälte, Regen oder Schnee?",
   "Ja — Kälte und leichter Niederschlag sind kein Problem; im Dunkeln wird die Show nur spektakulärer. Nur bei Sturm wird eine Alternative vereinbart."),
  ("Wie früh sollten wir das Dezemberfest buchen?",
   "Die Donnerstag- und Freitagabende im Dezember sind im Frühherbst weitgehend vergeben. Am besten vor Oktober buchen."),
  ("Eignet sich das als Feuerwerksersatz an Silvester?",
   "Ja — die Countdown-Show zu Mitternacht ist leiser, sicherer und persönlicher als Feuerwerk und meist erlaubt."),
 ],
 "service": {"name": "Feuershow für Weihnachtsfeier und Silvester", "type": "Feuershow",
   "desc": "Winterspektakel für Weihnachtsfeiern, Betriebsfeste, Neujahrsempfänge und Silvester: Feuershow im frühen Winterdunkel, auch als Feuerwerk-Alternative. Ab 450 €.",
   "offers": _OFFER("350", "1500", "4", "Neujahrsact 10 Min ab 350 €, Weihnachts-Showblock 20 Min ab 450 €, komplette Show ab 595 €, mehrere Sets bis 1500 €.")},
},
}

FR = {

"vuurshow-bruiloft": {
 "title": "Un spectacle de feu à votre mariage",
 "seo_title": "\U0001F49B Spectacle de Feu Mariage | Alternative Romantique au Feu d'Artifice — dès 450 €",
 "seo_desc": "Un spectacle de feu à votre mariage ? Un show romantique de 20 minutes à la première danse ou en ouverture de soirée — souvent autorisé là où les feux d'artifice sont interdits. 4,9/5 sur 136 avis. Dès 450 €.",
 "eyebrow": "Mariages",
 "img": ("/assets/media/bruiloft-1080.webp", "Duo de feu à un mariage : Nuno avec une danseuse aux grandes ailes rouges"),
 "body": """
<p><strong>Un spectacle de feu à votre mariage, c'est le moment dont vos invités parleront pendant des années : des flammes immenses à la première danse ou une ouverture spectaculaire de la soirée. Le meilleur : un spectacle de feu est souvent autorisé exactement là où les feux d'artifice sont interdits.</strong></p>
<h2>Pourquoi le feu convient parfaitement à un mariage</h2>
<p>Les feux d'artifice sont interdits dans la plupart des lieux de réception en Belgique et aux Pays-Bas. Un spectacle de feu professionnel offre le même effet waouh — de près, personnel et chorégraphié sur votre musique. Nuno adapte le numéro à votre première danse et règle la sécurité directement avec le lieu.</p>
<h2>Le jour J</h2>
<ul>
<li><strong>L'ouverture de soirée</strong> — un bloc de 20 minutes de crachage de feu, jonglerie enflammée et body fire.</li>
<li><strong>À la première danse</strong> — flammes et étincelles encadrent votre danse ; un cadeau pour votre photographe.</li>
<li><strong>Duo avec danseuse de feu</strong> — plus de romantisme et de théâtre, comme sur la photo ci-dessus.</li>
<li><strong>En intérieur ou mauvais temps ?</strong> — Nuno passe au <a href="/fr/spectacle-de-fakir/">spectacle de fakir</a> ou au mentalisme.</li>
</ul>
<h2>Quel est le prix ?</h2>
<p>Le bloc mariage de 20 minutes commence à <strong>450 €</strong> ; un power act de 10 minutes dès <strong>350 €</strong> — matériel, combustibles sûrs, montage et concertation avec le lieu inclus. Voir <a href="/fr/prix-cracheur-de-feu/">tous les prix</a> ou <a href="/fr/contact/">vérifier votre date de mariage</a> — réponse sous 24 heures. Avec <a href="/fr/a-propos-de-nuno/">17 ans d'expérience</a> et <a href="/fr/avis/">4,9/5 sur 136 avis</a>, Nuno se produit dans toute la Belgique et les Pays-Bas.</p>
""",
 "faq": [
  ("Combien coûte un spectacle de feu à un mariage ?",
   "Le bloc de 20 minutes, le plus populaire, commence à 450 € hors déplacement ; un power act de 10 minutes dès 350 €. Vous recevez toujours un devis tout compris."),
  ("Un spectacle de feu est-il autorisé là où les feux d'artifice sont interdits ?",
   "Généralement oui : un numéro de feu relève des règles du lieu, pas de la législation sur les feux d'artifice. Nuno règle autorisations et distances de sécurité directement avec le lieu."),
  ("Le spectacle peut-il accompagner notre première danse ?",
   "Oui — la chorégraphie est calée sur votre chanson, en concertation avec le DJ ou le groupe."),
  ("Et s'il pleut ou si le spectacle doit se faire en intérieur ?",
   "Une pluie légère ne pose pas de problème dehors. En intérieur sans flamme, Nuno passe au fakir ou au mentalisme — le spectacle reste."),
 ],
 "service": {"name": "Spectacle de feu pour mariage", "type": "Spectacle de feu",
   "desc": "Spectacle de feu romantique pour mariages : ouverture de soirée ou première danse, solo ou duo avec danseuse. Souvent autorisé là où les feux d'artifice sont interdits. Dès 450 €.",
   "offers": _OFFER("350", "750", "3", "Power act 10 min dès 350 €, bloc 20 min dès 450 €, duo dès 700 €.")},
},

"vuurshow-bedrijfsfeest": {
 "title": "Un spectacle de feu à votre fête d'entreprise",
 "seo_title": "\U0001F525 Spectacle de Feu Entreprise | Animation à Effet Waouh — dès 450 €",
 "seo_desc": "Une animation pour votre fête d'entreprise ou soirée du personnel ? Un spectacle de feu professionnel en ouverture ou grand final impressionne collaborateurs et clients. Vu à la télé. Dès 450 €.",
 "eyebrow": "Fêtes d'entreprise",
 "img": ("/assets/media/themafeest-1080.webp", "Le cracheur de feu Nuno lors d'une fête d'entreprise en soirée"),
 "body": """
<p><strong>Une fête d'entreprise dont on parle encore le lundi matin ? Un spectacle de feu professionnel en ouverture ou en grand final donne à votre soirée du personnel, événement client ou jubilé exactement cet effet waouh — soigné, sûr et représentatif.</strong></p>
<h2>Pourquoi les organisateurs réservent Nuno</h2>
<p>Dans l'événementiel d'entreprise, la fiabilité compte autant que le spectacle : costumes élégants, communication claire et un show à la minute près — 10, 20 ou 30 minutes. Avec des passages télé chez <a href="/fr/a-propos-de-nuno/">SBS6, RTL et VTM</a> et <a href="/fr/avis/">4,9/5 sur 136 avis</a>, vous savez qui vous réservez.</p>
<h2>Des formats qui fonctionnent</h2>
<ul>
<li><strong>L'ouverture</strong> — un power act de 10 minutes (dès 350 €).</li>
<li><strong>Le grand final</strong> — un bloc de 20 minutes juste avant le DJ ou le groupe (dès 450 €).</li>
<li><strong>Team building</strong> — l'équipe apprend à cracher le feu à l'<a href="/fr/atelier-cracheur-de-feu/">atelier</a>.</li>
<li><strong>Lieu intérieur ?</strong> — le <a href="/fr/spectacle-de-fakir/">fakir</a> ou le mentalisme offrent le spectacle sans flamme.</li>
</ul>
<h2>Budget et réservation</h2>
<p>Les spectacles vont de 350 à 1500 € — voir <a href="/fr/prix-cracheur-de-feu/">tous les prix</a> ; facturation en bonne et due forme. Envoyez date et lieu via le <a href="/fr/contact/">formulaire</a> : devis sous 24 heures. Fête de décembre ? Ces dates partent en premier — <a href="/fr/spectacle-noel-nouvel-an/">réservez tôt</a>.</p>
""",
 "faq": [
  ("Combien coûte un spectacle de feu pour une fête d'entreprise ?",
   "Un act d'ouverture de 10 minutes dès 350 €, un bloc complet de 20 minutes dès 450 €, des programmes de soirée jusqu'à 1500 € — toujours un devis tout compris, facturé."),
  ("Est-ce assez représentatif pour des clients et la direction ?",
   "Oui — costumes élégants, communication professionnelle et show chorégraphié. Nuno est passé à la télévision nationale et travaille pour des marques dans tout le Benelux."),
  ("Est-ce possible sur un site d'entreprise ou en intérieur ?",
   "Dehors presque toujours, y compris parkings et toits-terrasses ; en intérieur dès que le lieu et les pompiers l'autorisent. Sinon Nuno passe aux numéros sans flamme."),
  ("Peut-on combiner spectacle et atelier ?",
   "Bien sûr — le combo populaire : d'abord le show, puis les collègues apprennent à cracher le feu sous encadrement. Demandez le tarif combiné."),
 ],
 "service": {"name": "Spectacle de feu pour fête d'entreprise", "type": "Spectacle de feu",
   "desc": "Spectacle de feu professionnel pour fêtes d'entreprise et événements clients : ouverture, grand final ou atelier team building. Vu à la télé. Dès 450 €, facturé.",
   "offers": _OFFER("350", "1500", "4", "Ouverture 10 min dès 350 €, bloc 20 min dès 450 €, spectacle complet dès 595 €, programme de soirée jusqu'à 1500 €.")},
},

"vuurshow-verjaardag": {
 "title": "Un spectacle de feu pour un anniversaire ou jubilé",
 "seo_title": "\U0001F389 Spectacle de Feu Anniversaire | Le Spectacle dans Votre Jardin — dès 350 €",
 "seo_desc": "Rendre un anniversaire ou un jubilé inoubliable ? Réservez un spectacle de feu à domicile : 10 à 20 minutes de spectacle dans le jardin. Dès 350 €, Belgique et Pays-Bas.",
 "eyebrow": "Anniversaires & jubilés",
 "img": ("/assets/media/avondvuur-1080.webp", "Le cracheur de feu Nuno souffle une énorme boule de feu au crépuscule"),
 "body": """
<p><strong>Pour l'anniversaire de quelqu'un qui a déjà tout, un 50e dans le jardin ou un jubilé de mariage : un spectacle de feu à domicile est le cadeau que personne ne voit venir — et que personne n'oublie.</strong></p>
<h2>Le spectacle dans votre propre jardin</h2>
<p>Un spectacle de feu demande étonnamment peu de place : un jardin, une allée ou la pelouse devant la maison suffisent souvent. Nuno évalue l'endroit à l'avance (une photo par <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> suffit), apporte tout et laisse les lieux impeccables.</p>
<h2>Formules populaires</h2>
<ul>
<li><strong>L'acte surprise (10 min, dès 350 €)</strong> — la personne fêtée ne sait rien ; soudain, un cracheur de feu dans le jardin.</li>
<li><strong>Le bloc de fête (20 min, dès 450 €)</strong> — un mini-spectacle complet avec crachage de feu, jonglerie et interaction.</li>
<li><strong>Avec éléments de fakir</strong> — la personne fêtée ose-t-elle monter sur le <a href="/fr/spectacle-de-fakir/">lit de clous</a> ?</li>
</ul>
<h2>Quand et où</h2>
<p>Le feu est le plus beau au crépuscule — vers vingt-deux heures en été, dès dix-sept heures en hiver. Nuno se produit dans toute la Belgique et les Pays-Bas ; voir <a href="/fr/prix-cracheur-de-feu/">tous les prix</a> ou <a href="/fr/contact/">vérifier votre date</a> — réponse sous 24 heures.</p>
""",
 "faq": [
  ("Combien coûte un spectacle de feu pour un anniversaire ?",
   "L'acte surprise de 10 minutes dès 350 €, le bloc de fête complet de 20 minutes dès 450 € — hors déplacement, toujours avec un devis tout compris."),
  ("Quelle place faut-il dans un jardin ?",
   "Moins qu'on ne pense : un cercle libre de quelques mètres sans branches suffit souvent. Envoyez une photo du jardin par WhatsApp."),
  ("Peut-on en faire une surprise totale ?",
   "Oui — la formule la plus populaire. Tout est réglé discrètement avec l'organisateur ; la personne fêtée ne voit Nuno qu'à la première boule de feu."),
  ("Est-ce sûr avec des enfants et des aînés ?",
   "Oui : entièrement certifié, combustibles sûrs et une zone de sécurité claire d'où tout le monde voit tout."),
 ],
 "service": {"name": "Spectacle de feu pour anniversaire ou jubilé", "type": "Spectacle de feu",
   "desc": "Spectacle de feu à domicile pour anniversaires et jubilés : acte surprise de 10 minutes ou bloc de fête de 20 minutes dans le jardin. Dès 350 €.",
   "offers": _OFFER("350", "750", "3", "Acte surprise 10 min dès 350 €, bloc de fête 20 min dès 450 €, avec interaction fakir dès 595 €.")},
},

"vuurshow-festival": {
 "title": "Réserver un spectacle de feu pour votre festival",
 "seo_title": "\U0001F3AA Spectacle de Feu Festival | Jusqu'à 5 Sets par Jour — Expérience Walibi",
 "seo_desc": "Un numéro de feu pour votre festival ou événement public ? Nuno joue jusqu'à 5 sets de 20 minutes par jour, connaît la production festival des Walibi Fright Nights et fournit un rider clair. 950–1500 € tout compris.",
 "eyebrow": "Festivals & événements",
 "img": ("/assets/media/festival-1600.webp", "Le cracheur de feu Nuno souffle une boule de feu sur une place de festival devant une grande foule"),
 "body": """
<p><strong>En festival, le feu est l'aimant à public ultime : visible de loin, photogénique sur chaque téléphone. Nuno joue des programmes de festival jusqu'à cinq sets de vingt minutes par jour — avec la routine des Walibi Fright Nights et du festival Emporium.</strong></p>
<h2>Fait pour la production de festival</h2>
<p>Un festival exige des horaires serrés, des changements rapides et un travail sûr avec une foule mouvante. Nuno fournit un rider technique clair (cercle de jeu, zone de sécurité, coordination avec la production) et cale ses sets sur votre programme — aussi en journée, avec les éléments de fakir comme aimant avant la nuit.</p>
<h2>Le forfait festival</h2>
<ul>
<li><strong>Jusqu'à 5 × 20 minutes par jour</strong> — répartis sur l'après-midi et la soirée, 950–1500 € tout compris.</li>
<li><strong>Numéros itinérants</strong> — de courts moments surprises sur le site entre les sets.</li>
<li><strong>Productions Halloween</strong> — un <a href="/fr/halloween/">programme Halloween complet</a>, connu des Fright Nights.</li>
<li><strong>Plusieurs jours ou récurrent</strong> — demandez les tarifs multi-jours.</li>
</ul>
<h2>Réservation</h2>
<p>L'été des festivals et octobre se remplissent longtemps à l'avance. Envoyez vos dates et le nombre de sets via le <a href="/fr/contact/">formulaire</a> — devis avec rider sous 24 heures. Voir <a href="/fr/prix-cracheur-de-feu/">tous les prix</a>, les <a href="/fr/videos/">showreels</a> et les <a href="/fr/avis/">avis d'organisateurs</a>.</p>
""",
 "faq": [
  ("Combien coûte un numéro de feu en festival ?",
   "Le forfait festival avec jusqu'à cinq sets de 20 minutes coûte 950 à 1500 € tout compris, selon le nombre de sets et la distance. Un set seul dès 450 €."),
  ("Que contient le rider technique ?",
   "Un cercle de jeu libre avec zone de sécurité, accord sur le sol et les barrières si nécessaire. Ni scène ni électricité requises ; coordination musicale avec le DJ possible."),
  ("Un spectacle de feu fonctionne-t-il en plein jour ?",
   "Oui — en journée, les boules de feu et les éléments de fakir attirent la foule ; dès le crépuscule, le spectacle complet s'y ajoute."),
  ("Comment gérer les autorisations sur un site d'événement ?",
   "Nuno travaille dans le cadre de l'autorisation de l'organisateur et fournit sur demande les informations nécessaires sur le numéro, les combustibles et les mesures de sécurité."),
 ],
 "service": {"name": "Spectacle de feu en festival", "type": "Spectacle de feu",
   "desc": "Forfait festival : jusqu'à cinq sets de feu de 20 minutes par jour, numéros itinérants et option fakir. Expérience Walibi Fright Nights et Emporium. 950–1500 € tout compris.",
   "offers": _OFFER("450", "1500", "3", "Set seul dès 450 €, forfait jour jusqu'à 5×20 min 950–1500 €, multi-jours sur demande.")},
},

"vrijgezellenfeest": {
 "title": "EVG/EVJF : atelier cracheur de feu",
 "seo_title": "\U0001F525 Activité EVG & EVJF | Atelier Cracheur de Feu — Rien de Plus Original",
 "seo_desc": "Une activité originale pour un enterrement de vie de garçon ou de jeune fille ? Apprenez à cracher le feu en groupe, sous encadrement professionnel — photos de la première boule de feu incluses. Dès 350 €.",
 "eyebrow": "EVG & EVJF",
 "img": ("/assets/media/workshop-1125.webp", "Participant à l'atelier soufflant une grande boule de feu contre le ciel du soir"),
 "body": """
<p><strong>Encore un karting ? Ou offrez au futur marié ou à la future mariée une histoire qui sera racontée au mariage lui-même : tout le groupe apprend à cracher le feu sous encadrement professionnel — avec les photos de la première boule de feu de chacun comme preuve.</strong></p>
<h2>Comment se déroule l'atelier</h2>
<p>La sécurité d'abord : combustibles, technique, protection. Puis on s'exerce sans feu, et qui est prêt souffle sa première vraie boule de feu sous la supervision directe de Nuno. L'atelier dure une à deux heures et se termine — bien sûr — par la plus grande boule de feu du jour, signée par le futur marié.</p>
<h2>Pourquoi c'est L'activité d'EVG</h2>
<ul>
<li><strong>Rien de plus original</strong> — personne du groupe ne l'a déjà fait.</li>
<li><strong>Pour chaque groupe</strong> — de 4 à 20 personnes ; qui n'ose pas, photographie.</li>
<li><strong>Partout en Belgique et aux Pays-Bas</strong> — Nuno apporte tout ; seul un peu d'espace extérieur est nécessaire.</li>
<li><strong>À combiner avec un show</strong> — d'abord voir <a href="/fr/spectacle-de-feu/">comment font les pros</a>, puis essayer soi-même.</li>
</ul>
<h2>Prix et réservation</h2>
<p>L'atelier commence à <strong>350 €</strong> par groupe, matériel et encadrement inclus — voir la <a href="/fr/atelier-cracheur-de-feu/">page atelier</a> et <a href="/fr/prix-cracheur-de-feu/">tous les prix</a>. Les week-ends partent vite : <a href="/fr/contact/">vérifiez votre date</a> ou envoyez un message <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>. Une règle ferme : on participe sobre — l'apéro vient après.</p>
""",
 "faq": [
  ("Combien coûte un atelier cracheur de feu pour un EVG ?",
   "Dès 350 € par groupe, matériel, combustibles et encadrement inclus, hors déplacement. Un combo avec un mini-spectacle avant est possible."),
  ("Quelle taille de groupe ?",
   "De quatre à une vingtaine de personnes ; les grands groupes sont répartis en tournées pour que chacun ait un encadrement personnel."),
  ("N'est-ce pas dangereux ?",
   "Sous encadrement professionnel, c'est tout à fait faisable : d'abord la technique sans feu, puis étape par étape. Une règle stricte : on participe sobre."),
  ("Recevons-nous des photos ?",
   "Oui — la première boule de feu de chaque participant est immortalisée. Un matériau légendaire pour le groupe et le discours de mariage."),
 ],
 "service": {"name": "Atelier cracheur de feu pour EVG/EVJF", "type": "Atelier cracheur de feu",
   "desc": "Activité EVG/EVJF originale : tout le groupe apprend à cracher le feu sous encadrement professionnel, photos incluses. Dès 350 €.",
   "offers": _OFFER("350", "750", "2", "Atelier dès 350 € par groupe ; combo avec mini-spectacle sur demande.")},
},

"vuurwerk-alternatief": {
 "title": "Feu d'artifice interdit ? Réservez un spectacle de feu",
 "seo_title": "\U0001F386 Alternative au Feu d'Artifice | Spectacle de Feu : Autorisé et Aussi Spectaculaire",
 "seo_desc": "Feu d'artifice interdit sur votre lieu ou dans votre commune ? Un spectacle de feu professionnel offre le même effet — plus près, plus silencieux, sans stress d'autorisation. L'alternative pour mariages et événements.",
 "eyebrow": "Alternative au feu d'artifice",
 "img": ("/assets/media/vuurbal-1333.webp", "Immense boule de feu contre un ciel nocturne au-dessus du cracheur de feu Nuno"),
 "body": """
<p><strong>De plus en plus de communes belges et néerlandaises limitent ou interdisent les feux d'artifice, et la plupart des lieux ne les ont jamais autorisés. La bonne nouvelle : il existe une alternative au moins aussi spectaculaire — et généralement simplement permise.</strong></p>
<h2>Pourquoi un spectacle de feu est souvent autorisé là où l'artifice ne l'est pas</h2>
<p>Les feux d'artifice relèvent de règles de tir strictes et d'autorisations ; un numéro de feu professionnel relève des règles du lieu et travaille avec un feu contrôlé à hauteur d'yeux — sans détonations, sans projectiles, sans déchets. Nuno règle tout à l'avance avec le lieu et respecte les distances de sécurité prescrites.</p>
<h2>Spectacle de feu contre feu d'artifice</h2>
<ul>
<li><strong>Tout près</strong> — vos invités sont à quelques mètres de boules de feu immenses.</li>
<li><strong>Plus silencieux</strong> — pas de détonations : adapté aux quartiers résidentiels, campings et animaux à proximité.</li>
<li><strong>Plus long</strong> — pas trente secondes d'étincelles mais un show de 10 à 30 minutes sur votre musique.</li>
<li><strong>Résistant à la météo</strong> — un spectacle de feu a lieu même par vent et pluie légère.</li>
</ul>
<h2>Pour quels moments</h2>
<p>Populaire aux <a href="/fr/spectacle-de-feu-mariage/">mariages</a> (grand final au lieu d'un feu d'artifice), au <a href="/fr/spectacle-noel-nouvel-an/">Nouvel An et aux réceptions</a>, aux <a href="/fr/spectacle-de-feu-entreprise/">fêtes d'entreprise</a> et aux événements publics sans autorisation d'artifice. Un show de clôture coûte 350 à 595 € — voir <a href="/fr/prix-cracheur-de-feu/">les prix</a> ou <a href="/fr/contact/">demander un devis</a> ; réponse sous 24 heures.</p>
""",
 "faq": [
  ("Un spectacle de feu est-il vraiment autorisé là où l'artifice est interdit ?",
   "Généralement oui : un numéro de feu professionnel relève des règles du lieu ou de l'événement, pas de la législation sur les artifices. Nuno le règle directement à l'avance."),
  ("Est-ce aussi spectaculaire qu'un feu d'artifice ?",
   "Différent et plus proche : des boules de feu immenses à quelques mètres, en musique et avec interaction — plus intense qu'un artifice à cent mètres d'altitude."),
  ("Combien cela coûte-t-il ?",
   "Entre 350 et 595 € pour un show de clôture de 10 à 30 minutes — généralement bien moins cher qu'un artifice professionnel avec sa procédure d'autorisation."),
  ("Cela fonctionne-t-il pour le réveillon du Nouvel An ?",
   "Justement : le compte à rebours vers minuit est le remplacement parfait de l'artifice — réservez décembre bien à l'avance."),
 ],
 "service": {"name": "Spectacle de feu comme alternative au feu d'artifice", "type": "Spectacle de feu",
   "desc": "Alternative spectaculaire et autorisée au feu d'artifice pour mariages, Nouvel An et événements : spectacle de feu de 10 à 30 minutes, plus silencieux, plus proche, sans stress d'autorisation. Dès 350 €.",
   "offers": _OFFER("350", "750", "3", "Acte de clôture 10 min dès 350 €, bloc 20 min dès 450 €, grand final 30 min dès 595 €.")},
},

"kerst-nieuwjaar-entertainment": {
 "title": "Spectacle pour Noël & Nouvel An",
 "seo_title": "\U0001F384 Spectacle Noël & Nouvel An | Un Show de Feu dans la Nuit d'Hiver",
 "seo_desc": "Une animation pour votre fête de Noël, soirée du personnel ou réception de Nouvel An ? Dans les mois sombres de l'hiver, un spectacle de feu atteint son plein effet. Décembre se remplit tôt. Dès 450 €.",
 "eyebrow": "Noël & Nouvel An",
 "img": ("/assets/media/schemering-640.webp", "Crachage de feu dans le crépuscule d'hiver, la flamme s'évase largement"),
 "body": """
<p><strong>Décembre est le plus beau mois pour le feu : il fait nuit à dix-sept heures, les invités sont dehors près des braseros — et Nuno ouvre la soirée avec des flammes immenses. Pour les fêtes de Noël, soirées du personnel et réceptions de Nouvel An, un spectacle de feu est le spectacle d'hiver par excellence.</strong></p>
<h2>Pourquoi le feu et l'hiver vont ensemble</h2>
<p>En été, un spectacle de feu attend vingt-deux heures ; en décembre, le plein effet commence dès la fin d'après-midi. La chaleur des flammes, les étincelles contre le ciel d'hiver, les invités au vin chaud à distance sûre — et la neige ou une pluie légère ne posent aucun problème.</p>
<h2>Pour chaque fête de décembre</h2>
<ul>
<li><strong>La fête de Noël</strong> — un bloc de 20 minutes comme point culminant de la <a href="/fr/spectacle-de-feu-entreprise/">soirée d'entreprise</a>, dès 450 €.</li>
<li><strong>La réception de Nouvel An</strong> — ouvrir l'année avec du feu : un act puissant de 10 minutes dès 350 €.</li>
<li><strong>Le réveillon</strong> — le compte à rebours comme <a href="/fr/alternative-feu-artifice/">alternative au feu d'artifice</a>.</li>
<li><strong>En intérieur aussi</strong> — le <a href="/fr/spectacle-de-fakir/">fakir</a> ou le mentalisme dans la salle, le feu dehors en apothéose.</li>
</ul>
<h2>Décembre part en premier</h2>
<p>Les jeudis et vendredis de décembre sont réservés les premiers chaque année — les entreprises planifient dès septembre. <a href="/fr/contact/">Vérifiez votre date maintenant</a> ; réponse sous 24 heures. Tous les forfaits dans <a href="/fr/prix-cracheur-de-feu/">l'aperçu des prix</a>.</p>
""",
 "faq": [
  ("Combien coûte une animation pour Noël ou le Nouvel An ?",
   "Un act d'ouverture de 10 minutes dès 350 €, le bloc complet de 20 minutes dès 450 € — les entreprises reçoivent un devis tout compris, facturé."),
  ("Un spectacle de feu fonctionne-t-il par froid, pluie ou neige ?",
   "Oui — le froid et les précipitations légères ne posent pas de problème ; dans l'obscurité, le show n'en est que plus spectaculaire. Seule la tempête impose une alternative."),
  ("Quand réserver la fête de décembre ?",
   "Les jeudis et vendredis soir de décembre sont largement pris dès le début de l'automne. Réservez de préférence avant octobre."),
  ("Convient-il comme remplacement de l'artifice au réveillon ?",
   "Oui — le compte à rebours vers minuit est plus silencieux, plus sûr et plus personnel que l'artifice, et généralement autorisé."),
 ],
 "service": {"name": "Spectacle de feu pour Noël et Nouvel An", "type": "Spectacle de feu",
   "desc": "Spectacle d'hiver pour fêtes de Noël, soirées du personnel, réceptions de Nouvel An et réveillon : show de feu dans la nuit d'hiver, aussi comme alternative à l'artifice. Dès 450 €.",
   "offers": _OFFER("350", "1500", "4", "Act de Nouvel An 10 min dès 350 €, bloc de Noël 20 min dès 450 €, spectacle complet dès 595 €, plusieurs sets jusqu'à 1500 €.")},
},
}
