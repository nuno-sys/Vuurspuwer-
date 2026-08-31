"""Vertalingen voor de meertalige site: Engels, Duits en Frans.

Nederlands is en blijft de hoofdtaal op de bestaande adressen; de
vertaalde pagina's leven onder /en/, /de/ en /fr/ met eigen nette slugs.
Alleen wat in het menu staat wordt vertaald (plus de Duitse en Franstalige
regiopagina's) — de blog en de NL-stadspagina's blijven Nederlands.
"""

SITE = "https://vuurspuwer.com"
LANGS = ("en", "de", "fr")
LANG_NAMES = {"nl": "Nederlands", "en": "English", "de": "Deutsch", "fr": "Français"}
HTML_LANG = {"nl": "nl", "en": "en", "de": "de", "fr": "fr"}

# NL-slug ("" = homepage) -> slug per taal (zonder taalvoorvoegsel)
SLUGS = {
    "": {"en": "", "de": "", "fr": ""},
    "fotos": {"en": "photos", "de": "fotos", "fr": "photos"},
    "videos": {"en": "videos", "de": "videos", "fr": "videos"},
    "vuurspuwer-inhuren": {"en": "fire-show", "de": "feuershow", "fr": "spectacle-de-feu"},
    "workshop-vuurspuwen": {"en": "fire-breathing-workshop", "de": "feuerspucker-workshop", "fr": "atelier-cracheur-de-feu"},
    "halloween": {"en": "halloween", "de": "halloween", "fr": "halloween"},
    "fakir-show-inhuren": {"en": "fakir-show", "de": "fakirshow", "fr": "spectacle-de-fakir"},
    "contact-3": {"en": "contact", "de": "kontakt", "fr": "contact"},
    "beoordelingen": {"en": "reviews", "de": "bewertungen", "fr": "avis"},
    "over-nuno": {"en": "about-nuno", "de": "ueber-nuno", "fr": "a-propos-de-nuno"},
}

# Duitse en Franstalige regiopagina's: NL-stadsslug -> vertaalde slug
REGIO_SLUGS = {
    "de": {
        "spectaculaire-vuurspuwer-aachen-maak-uw-evenement-in-de-keizerstad-onvergetelijk": "feuerspucker-aachen",
        "vuurspuwer-inhuren-in-krefeld-een-vlammend-spektakel-voor-uw-event": "feuerspucker-krefeld",
        "vuurspuwer-monchengladbach-spectaculaire-vuurshows-net-over-de-grens": "feuerspucker-moenchengladbach",
        "vuurspuwer-inhuren-in-kaldenkirchen-spectaculair-entertainment-in-de-grensregio": "feuerspucker-kaldenkirchen",
        "vuurspuwer-inhuren-in-kleve-breng-vurige-magie-naar-de-grensregio": "feuerspucker-kleve",
    },
    "fr": {
        "vuurspuwer-boeken-in-liege": "cracheur-de-feu-liege",
        "vuurspuwer-boeken-in-brussel": "cracheur-de-feu-bruxelles",
    },
}

def url_of(lang, slug):
    """Volledig pad van een pagina in een taal ('' = taal-homepage)."""
    if lang == "nl":
        return "/" if slug == "" else f"/{slug}/"
    loc = SLUGS.get(slug, {}).get(lang)
    if loc is None:
        return f"/{lang}/"
    return f"/{lang}/" if loc == "" else f"/{lang}/{loc}/"

# ------------------------------------------------------------------ chrome
# teksten in header, menu, footer, CTA-blok en formulier per taal;
# "nl" is de referentie zoals die nu in index.html staat.
UI = {
 "nl": {
    "menu": {"home": "Home", "fotos": "Foto's", "videos": "Video's",
             "vuurshow": "Vuurshow", "workshop": "Workshop",
             "halloween": "\U0001F383 Halloween", "fakirshow": "Fakirshow",
             "contact": "Contact", "reviews": "Reviews"},
    "offerte": "Offerte aanvragen",
    "stars_label": "4,9 van de 5 sterren uit 136 reviews — lees de beoordelingen",
    "stars_txt": "4.9 · 136 reviews",
    "menu_btn": "Menu", "close_btn": "Sluit",
    "cta_title": "Check je <em>datum</em>",
    "cta_lede": "Bel of app even, dan weet je binnen een minuut of het kan.",
    "cta_whatsapp": "WhatsApp direct", "cta_form": "Stuur een aanvraag",
    "crumb_home": "Home",
    "wa_status_on": "Online", "wa_status_off": "Reageert snel",
    "eyebrow_default": "Vuurspuwer Nuno",
 },
 "en": {
    "menu": {"home": "Home", "fotos": "Photos", "videos": "Videos",
             "vuurshow": "Fire show", "workshop": "Workshop",
             "halloween": "\U0001F383 Halloween", "fakirshow": "Fakir show",
             "contact": "Contact", "reviews": "Reviews"},
    "offerte": "Request a quote",
    "stars_label": "Rated 4.9 out of 5 from 136 reviews — read the reviews",
    "stars_txt": "4.9 · 136 reviews",
    "menu_btn": "Menu", "close_btn": "Close",
    "cta_title": "Check your <em>date</em>",
    "cta_lede": "Call or send a WhatsApp message — you'll know within a minute.",
    "cta_whatsapp": "WhatsApp directly", "cta_form": "Send a request",
    "crumb_home": "Home",
    "wa_status_on": "Online", "wa_status_off": "Replies quickly",
    "eyebrow_default": "Fire breather Nuno",
 },
 "de": {
    "menu": {"home": "Start", "fotos": "Fotos", "videos": "Videos",
             "vuurshow": "Feuershow", "workshop": "Workshop",
             "halloween": "\U0001F383 Halloween", "fakirshow": "Fakirshow",
             "contact": "Kontakt", "reviews": "Bewertungen"},
    "offerte": "Angebot anfordern",
    "stars_label": "4,9 von 5 Sternen aus 136 Bewertungen — Bewertungen lesen",
    "stars_txt": "4.9 · 136 Bewertungen",
    "menu_btn": "Menü", "close_btn": "Zu",
    "cta_title": "Termin <em>prüfen</em>",
    "cta_lede": "Rufen Sie an oder schreiben Sie per WhatsApp — in einer Minute wissen Sie Bescheid.",
    "cta_whatsapp": "Direkt per WhatsApp", "cta_form": "Anfrage senden",
    "crumb_home": "Start",
    "wa_status_on": "Online", "wa_status_off": "Antwortet schnell",
    "eyebrow_default": "Feuerspucker Nuno",
 },
 "fr": {
    "menu": {"home": "Accueil", "fotos": "Photos", "videos": "Vidéos",
             "vuurshow": "Spectacle de feu", "workshop": "Atelier",
             "halloween": "\U0001F383 Halloween", "fakirshow": "Fakir",
             "contact": "Contact", "reviews": "Avis"},
    "offerte": "Demander un devis",
    "stars_label": "Note de 4,9 sur 5 pour 136 avis — lire les avis",
    "stars_txt": "4.9 · 136 avis",
    "menu_btn": "Menu", "close_btn": "Fermer",
    "cta_title": "Vérifiez votre <em>date</em>",
    "cta_lede": "Appelez ou envoyez un message WhatsApp — réponse en une minute.",
    "cta_whatsapp": "WhatsApp direct", "cta_form": "Envoyer une demande",
    "crumb_home": "Accueil",
    "wa_status_on": "En ligne", "wa_status_off": "Répond vite",
    "eyebrow_default": "Cracheur de feu Nuno",
 },
}

# formulier-teksten (contactpagina en taal-homepages)
FORM = {
 "en": {
    "naam": "Name", "email": "Email", "tel": "Phone (optional)",
    "datum": "Event date", "show": "Which show?", "ruimte": "Indoors or outdoors",
    "opts_show": ["Not sure yet", "Fire show", "Fakir show", "Fire-breathing workshop",
                  "Reptile show", "Halloween act", "Mentalism", "Theme party / combination"],
    "opts_ruimte": ["Outdoors", "Indoors", "Both"],
    "locatie": "Location", "locatie_ph": "City or venue, e.g. Amsterdam",
    "bericht": "Tell us briefly about your event",
    "bericht_ph": "E.g. company party for 80 guests, show around 9 pm",
    "submit": "Send request",
    "note": "You'll receive an instant confirmation by email — and a personal reply within 24 hours.",
    "msg_busy": "Sending…",
    "msg_ok": "\U0001F525 Done — your request has been sent! You'll receive a confirmation by email and I'll reply <b>within 24 hours</b>.",
    "msg_fail": "Sending didn't work — email your request to nuno@vuurspuwer.com or send it via WhatsApp.",
    "msg_invalid": "Please fill in your name and a valid email address so I can reply.",
 },
 "de": {
    "naam": "Name", "email": "E-Mail", "tel": "Telefon (optional)",
    "datum": "Datum der Veranstaltung", "show": "Welche Show?", "ruimte": "Drinnen oder draußen",
    "opts_show": ["Weiß ich noch nicht", "Feuershow", "Fakirshow", "Feuerspucker-Workshop",
                  "Reptilienshow", "Halloween-Act", "Mentalismus", "Mottoparty / Kombination"],
    "opts_ruimte": ["Draußen", "Drinnen", "Beides"],
    "locatie": "Ort", "locatie_ph": "Stadt oder Location, z. B. Aachen",
    "bericht": "Erzählen Sie kurz von Ihrer Veranstaltung",
    "bericht_ph": "z. B. Firmenfeier mit 80 Gästen, Show gegen 21 Uhr",
    "submit": "Anfrage senden",
    "note": "Sie erhalten sofort eine Bestätigung per E-Mail — und innerhalb von 24 Stunden eine persönliche Antwort.",
    "msg_busy": "Wird gesendet…",
    "msg_ok": "\U0001F525 Geschafft — Ihre Anfrage ist unterwegs! Sie erhalten eine Bestätigung per E-Mail und ich antworte <b>innerhalb von 24 Stunden</b>.",
    "msg_fail": "Das Senden hat nicht geklappt — mailen Sie Ihre Anfrage an nuno@vuurspuwer.com oder schicken Sie sie per WhatsApp.",
    "msg_invalid": "Bitte Namen und eine gültige E-Mail-Adresse angeben, damit ich antworten kann.",
 },
 "fr": {
    "naam": "Nom", "email": "E-mail", "tel": "Téléphone (facultatif)",
    "datum": "Date de l'événement", "show": "Quel spectacle ?", "ruimte": "Intérieur ou extérieur",
    "opts_show": ["Je ne sais pas encore", "Spectacle de feu", "Spectacle de fakir", "Atelier cracheur de feu",
                  "Spectacle de reptiles", "Animation Halloween", "Mentalisme", "Soirée à thème / combinaison"],
    "opts_ruimte": ["Extérieur", "Intérieur", "Les deux"],
    "locatie": "Lieu", "locatie_ph": "Ville ou salle, p. ex. Liège",
    "bericht": "Parlez-nous brièvement de votre événement",
    "bericht_ph": "P. ex. fête d'entreprise de 80 personnes, spectacle vers 21 h",
    "submit": "Envoyer la demande",
    "note": "Vous recevez une confirmation immédiate par e-mail — et une réponse personnelle sous 24 heures.",
    "msg_busy": "Envoi en cours…",
    "msg_ok": "\U0001F525 C'est fait — votre demande est envoyée ! Vous recevez une confirmation par e-mail et je réponds <b>sous 24 heures</b>.",
    "msg_fail": "L'envoi n'a pas abouti — envoyez votre demande à nuno@vuurspuwer.com ou par WhatsApp.",
    "msg_invalid": "Merci d'indiquer votre nom et une adresse e-mail valide pour que je puisse répondre.",
 },
}

# ------------------------------------------------------------------ inhoud
# volledige pagina-inhoud per taal; de sleutel is de NL-slug.
PAGES = {"en": {}, "de": {}, "fr": {}}

PAGES["en"]["vuurspuwer-inhuren"] = {
 "title": "Hire a fire breather: book the most spectacular fire show in the Netherlands & Belgium",
 "seo_title": "\U0001F525 Hire a Fire Breather – Spectacular Fire Show NL & BE | Nuno",
 "seo_desc": "Hire a professional fire breather in the Netherlands or Belgium. Nuno is the Benelux's most-booked fire artist. Breathtaking shows for any event. Request a free quote!",
 "eyebrow": "Fire show",
 "img": ("/assets/media/avondvuur-1080.webp", "Fire breather Nuno blowing a huge fireball into the evening sky"),
 "body": """
<p>Looking for more than just entertainment — an act that leaves your guests literally breathless? An opening or closing show people will talk about for years? Welcome to the world of Nuno.</p>
<p>As one of the most experienced and sought-after fire artists and fakirs in the Benelux, Nuno lifts every event to another level. With <a href="/en/about-nuno/" title="more than 15 years of international experience">more than 15 years of international experience</a>, spectacular TV appearances and an absolute focus on safety, Nuno delivers not a standard fire act but a high-end visual masterpiece — tailored to your venue.</p>
<h2>Why event planners choose fire artist Nuno</h2>
<ul>
<li><strong>World-class visual spectacle</strong> — no small flames, but towering clouds of fire, fire juggling and choreography set to music.</li>
<li><strong>100% safe &amp; certified</strong> — professional equipment, safe fuels, and full compliance with permits and safety distances.</li>
<li><strong>High-end presentation</strong> — sharp costumes, professional conduct and punctual communication. Perfect for corporate events.</li>
<li><strong>Flexible</strong> — a stage in Amsterdam, a castle garden in Antwerp or an intimate driveway: the show adapts to your location. Curious? <a href="/en/contact/">Get in touch</a>.</li>
</ul>
<h2>Our fire shows: an explosion of entertainment</h2>
<ul>
<li><strong>The Power Act (5–10 min)</strong> — a short, explosive show. Ideal as an opener or a spectacular finale.</li>
<li><strong>The Full Fire Show (20–30 min)</strong> — a building show with fakir elements, body fire, fire breathing and audience interaction.</li>
<li><strong>Duo shows</strong> — for extra impact, Nuno can be booked together with a female fire artist or dancer.</li>
</ul>
<p>Indoors (where the venue allows) or outdoors: we bring the wow factor.</p>
<h2>Also possible: interactive fire-breathing workshops</h2>
<p>Want to do more than watch? Nuno offers unique <a href="/en/fire-breathing-workshop/">fire-breathing workshops</a> — an original idea for team building, stag and hen parties or adventurous company outings.</p>
<h2>Which events suit Nuno?</h2>
<ul>
<li>\U0001F389 <strong>Anniversaries &amp; private parties</strong> — exclusive entertainment in your own garden or venue.</li>
<li>\U0001F3E2 <strong>Corporate events</strong> — impress clients or staff with a powerful opening.</li>
<li>\U0001F48D <strong>Weddings</strong> — a romantic fire show as an alternative to fireworks (often allowed where fireworks are not!).</li>
<li>\U0001F3AA <strong>Festivals &amp; events</strong> — a visual magnet that works brilliantly on social media.</li>
</ul>
<h2>Ready to set your event on fire?</h2>
<p>Don't wait too long to secure your date: Nuno's calendar fills up fast, especially in high season. <a href="/en/contact/">Check availability &amp; prices</a>, call <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> or message via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
""",
 "faq": [
  ("Is a fire show safe at my venue?",
   "Yes — safety is priority number one. Nuno works to strict safety protocols, uses professional fuels and equipment, and adapts the show to the available space, indoors or outdoors."),
  ("What does it cost to hire a fire breather?",
   "The price depends on the type of show, its duration and the location. Every show is tailor-made, so request a free quote for an exact price."),
  ("Can the fire show take place indoors?",
   "Yes, provided the venue meets certain safety requirements such as ceiling height and ventilation. Nuno has developed special acts that can be performed safely indoors, for example with body fire and fakir techniques."),
  ("Where does fire breather Nuno perform?",
   "Nuno performs throughout the Netherlands and Belgium — from Amsterdam and Rotterdam to Antwerp and Brussels — and internationally on request. Travel costs are included in the quote."),
 ],
 "service": {"name": "Fire show", "type": "Fire Show / Fire Performance",
             "desc": "Spectacular fire show with fire breathing, fire juggling and impressive effects. Professional, safe and suited to corporate events, weddings and festivals."},
 "fotos": [("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Fireball at dusk", "Fire breather Nuno blowing an enormous fireball at dusk"),
           ("festival-900.webp", "festival-1600.webp", 900, 902, "Full fire show at a festival", "Fire breather Nuno blowing a fireball over a festival crowd"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Daytime fire show", "Daytime fire show at a festival, audience watching from a few metres away")],
}

PAGES["en"]["fakir-show-inhuren"] = {
 "title": "Fakir show: master of fear and pain",
 "seo_title": "\U0001F525 Book a Fakir Show – Sensational Act by Nuno the Fakir",
 "seo_desc": "Book a fakir show for your event. Nuno the Fakir masters fear and pain like no other — an unforgettable act that will make your audience shiver. Book now!",
 "eyebrow": "Fakir show",
 "img": ("/assets/media/fakirshow-640.webp", "Fakir show in the theatre: Nuno on the bed of nails bearing the weight of a spectator"),
 "body": """
<p>Marvel at the many arts of the <strong>fakir show</strong>! Looking for an original, sensational act for your event? <a href="/en/about-nuno/" title="Nuno the Fakir, a master of his craft">Nuno the Fakir, a master of his craft</a>, offers an unforgettable experience that will make your audience shiver.</p>
<h2>What to expect from a fakir show</h2>
<p>The fakir show is a spectacular performance full of breathtaking acts. Nuno walks on glass, defies beds of nails and demonstrates impressive sword skills. Fire breathing — a classic — is naturally part of the show. The audience takes part too, for instance by standing on the fakir while he lies on a bed of nails (always under supervision). The show runs from 15 to 60 minutes, tailored to your wishes.</p>
<p>Want to combine the fakir show with other acts? Absolutely — think <a href="/en/fire-show/">fire breathing</a> or a reptile show. We are happy to create a unique experience with you.</p>
<h2>Venues for a fakir show</h2>
<p>The fakir show suits almost any location, from theatre stages to street performances. With years of experience, Nuno delivers a fantastic show anywhere. It can be adapted to your wishes: longer, shorter, or without fire breathing. Multiple performances in a row are possible too (up to 4).</p>
<h2>Themes</h2>
<p>The fakir acts fit perfectly with themes like 1001 Nights, Oriental, fairy tales, magic or carnival. We gladly adapt the show to match your event.</p>
<h2>Why choose Nuno's fakir show?</h2>
<ul>
<li>A professional, experienced performer</li>
<li>Combinable with Nuno's other acts</li>
<li>An act full of tension, sensation and wonder</li>
</ul>
<h2>How do I book a fakir show?</h2>
<p>Fill in the <a href="/en/contact/">contact form</a> and we'll get back to you within 24 hours with a free, no-obligation quote. Ready to amaze your audience? Get in touch today!</p>
""",
 "faq": [],
 "service": {"name": "Fakir show", "type": "Fakir Performance",
             "desc": "Thrilling fakir show with classic acts such as the bed of nails, glass walking and extreme demonstrations, performed safely with experience and discipline."},
 "fotos": [("fakirshow-640.webp", "fakirshow-640.webp", 640, 1351, "Fakir show in the theatre", "Fakir show in the theatre: Nuno on the bed of nails bearing the weight of a spectator"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "The bed of nails up close", "Close-up of the fakir act: Nuno balancing the nail board with chains on his face"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Glass and weight", "Fakir act: Nuno bearing the weight of a standing spectator")],
}

PAGES["en"]["workshop-vuurspuwen"] = {
 "title": "Fire-breathing workshop",
 "seo_title": "\U0001F525 Fire-Breathing Workshop | Learn Fire Breathing with Nuno",
 "seo_desc": "Fire-breathing workshop with professional guidance from Nuno. Ideal for team building, stag and hen parties or company events. Book your workshop now!",
 "eyebrow": "Workshop",
 "img": ("/assets/media/workshop-1125.webp", "Fire-breathing workshop under the guidance of professional fire breather Nuno"),
 "body": """
<h2>Fire-Breathing Workshop: Unleash the Fire in Yourself (and Your Team)!</h2>
<p>Ever dreamt of breathing fire? Want an unforgettable experience that is thrilling and instructive at the same time? Then the fire-breathing workshop by Nuno, the <a href="/en/about-nuno/">experienced fire breather and fakir</a> of Vuurspuwer.com, is exactly what you're looking for. Nuno teaches you the art of fire breathing and fire eating in a safe, responsible way. Do you dare?</p>
<h3>Why take a fire-breathing workshop?</h3>
<ul>
<li><strong>Stag &amp; hen parties:</strong> give the bride or groom a fiery start to married life!</li>
<li><strong>Birthdays:</strong> make your party unforgettable with a spectacular demonstration and workshop.</li>
<li><strong>Company events:</strong> surprise your colleagues with an original, challenging activity that strengthens team spirit.</li>
<li><strong>Clubs and groups:</strong> an evening full of tension, sensation and unforgettable moments.</li>
<li><strong>Team building:</strong> improve cooperation and trust within your team in a unique way.</li>
</ul>
<h3>Safety first!</h3>
<p>Safety always comes first. Nuno teaches you not only the techniques of fire breathing but everything about the safety measures: the right fuels, protective clothing and how to minimise risk. You'll feel comfortable and confident before you breathe your first flame.</p>
<h3>For beginners and advanced</h3>
<p>Whether you've never touched fire or already have some experience, the workshop suits everyone. Beginners are guided step by step, while advanced participants learn new techniques and tricks.</p>
<h3>Team building with fire</h3>
<p>Fire breathing demands cooperation, communication and trust — the perfect team-building activity. Learning it together forges a bond your team will never forget.</p>
<h3>A workshop tailored to you</h3>
<p>From a short demonstration to a full course: the workshop is adapted entirely to your wishes, on location in the Netherlands or Belgium. <a href="/en/contact/">Contact us</a> to discuss the options.</p>
<h3>Book your unforgettable fire experience now!</h3>
<p>Don't wait — plan your fire-breathing workshop with Nuno today and push your limits. <a href="/en/contact/">Get in touch</a> and make your event a fiery success!</p>
""",
 "faq": [
  ("Is the fire-breathing workshop safe?",
   "Yes. Safety always comes first: you first learn everything about the right fuels, protective clothing and minimising risk, then practise step by step under Nuno's professional supervision."),
  ("Who is the workshop suitable for?",
   "Anyone aged 18 or over, from complete beginners to advanced participants. The workshop adapts to the group's level — ideal for stag and hen parties, birthdays, company events and team building."),
  ("Where can the workshop take place?",
   "On location anywhere in the Netherlands or Belgium, provided there is enough open outdoor space. Nuno brings all materials."),
  ("What does a fire-breathing workshop cost?",
   "The price depends on group size, duration and location. Request a free quote — you'll receive a tailored proposal within 24 hours."),
 ],
 "service": {"name": "Fire-breathing workshop", "type": "Workshop / Team building",
             "desc": "Fire-breathing workshop with professional guidance from Nuno. Learn fire breathing and fire eating safely — ideal for team building, stag and hen parties and company events."},
 "fotos": [("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Fire breathing against the evening sky", "Fire breather blowing a large fireball against the evening sky from a balustrade"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Fireball at dusk", "Fire breather Nuno blowing an enormous fireball at dusk"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Daytime fire show", "Daytime fire show at a festival, audience watching from a few metres away")],
}

PAGES["en"]["halloween"] = {
 "title": "Book a Halloween fire show & horror fakir",
 "seo_title": "\U0001F383 Halloween Fire Show & Horror Fakir | NL & BE – from €350",
 "seo_desc": "Booking a Halloween act? Devilish fire shows, a horror fakir show and scare acts — known from Walibi Fright Nights. All of NL & BE, from €350. October fills up fast!",
 "eyebrow": "\U0001F383 October · limited availability",
 "img": ("/assets/media/vuurbal-1333.webp", "Towering fireball against a black night sky above the fire breather"),
 "body": """
<p>Known from the <strong>Halloween Fright Nights at Walibi Holland</strong>. Devilish fire shows, scare acts and a horror fakir that will make your guests shiver — throughout the Netherlands and Belgium.</p>
<h2>Halloween is the season of fire</h2>
<p>No celebration suits fire and darkness better than Halloween. For the occasion Nuno transforms into a demon, devil or horror fakir: flames looming out of the dark, a bed-of-nails act by torchlight, scare moments among the crowd and mentalism that reads minds a little too well. Every element is tuned to your theme and audience — from family-friendly spooky to adult horror.</p>
<p>With performances at Walibi Holland's Halloween Fright Nights on his CV, Nuno knows exactly how to make a big crowd scream and applaud. He makes the difference just as much at a scout's haunted trail, a horror night at the pub or a company Halloween party.</p>
<h2>Halloween acts at a glance</h2>
<ul>
<li>\U0001F608 <strong>Devilish fire show</strong> — flames, sparks and pillars of fire in horror styling (from €350)</li>
<li>\U0001F5E1️ <strong>Horror fakir show</strong> — bed of nails, glass and swords in creepy make-up (from €450)</li>
<li>\U0001F441️ <strong>Dark mentalism</strong> — mind reading with a sinister edge</li>
<li>\U0001F525 <strong>Complete Halloween production</strong> — several acts spread across the evening (from €750)</li>
</ul>
<h2>Book early</h2>
<p>The weekends around 31 October always sell out first. Book before September to be sure of your date; last-minute is sometimes possible, but choice is limited. <a href="/en/contact/">Check availability now</a> or message via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
""",
 "faq": [
  ("What does a Halloween fire show or horror act cost?",
   "Halloween acts start from €350 (fire show) or €450 (horror fakir show). A complete Halloween evening production with several acts is possible from €750. October dates are limited — booking early pays off."),
  ("Which Halloween acts are possible?",
   "Devilish fire shows, a horror fakir on the bed of nails and glass, scare acts among the crowd, creepy mentalism and combinations of these. Costume and make-up are fully matched to your theme."),
  ("Does Nuno have experience with large Halloween events?",
   "Yes. Nuno performed at Walibi Holland's Halloween Fright Nights, one of the biggest Halloween events in the Benelux, alongside countless haunted trails, horror nights and theme parties."),
  ("How early should I book for Halloween?",
   "The weekends around 31 October sell out first every year. Book before September to be sure of your date; last-minute is sometimes possible, but choice is then limited."),
 ],
 "service": {"name": "Halloween entertainment", "type": "Halloween entertainment",
             "desc": "Halloween fire shows, horror fakir acts and scare entertainment for fright nights, haunted trails and theme parties in the Netherlands and Belgium.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "3",
                        "description": "Starting price, excluding travel costs. Free tailored quote."}},
 "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Fireball during a night show", "Towering fireball against a black night sky above the fire breather"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Horror fakir: the nail board", "Close-up of the fakir act: Nuno balancing the nail board with chains on his face"),
           ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Fire at a theme party", "Fire breather next to a vintage bus during an evening theme party")],
}

PAGES["en"]["over-nuno"] = {
 "title": "About fire breather & fakir Nuno: 17 years of mastery",
 "seo_title": "\U0001F525 Fire Breather & Fakir Nuno | 17 Years of Mastery",
 "seo_desc": "Fire breather and fakir Nuno: 17 years of experience as an entertainer in the Netherlands and Belgium. Fire show, fakir show, mentalist and reptile show. Request a free quote!",
 "eyebrow": "About Nuno",
 "img": ("/assets/media/mentalist-1371.webp", "Nuno on the stage of a theatre"),
 "body": """
<p><strong>Fire breather and fakir Nuno has been one of the most experienced entertainers in the Netherlands and Belgium for more than 17 years. Fire breather, fakir, mentalist and reptile-show artist: Nuno combines craftsmanship with spectacle and leaves a lasting impression at every performance.</strong></p>
<h2>About Fire Breather &amp; Fakir Nuno: 17 Years of Mastery in Entertainment</h2>
<p>Welcome to a world of adrenaline, passion and pure magic. I'm Nuno, and for more than 17 years I've been pushing boundaries on stage. What began as a fascination with fire has grown into an international career as a professional <strong>fire breather</strong> and fakir. From spectacular fire shows at festivals to mysterious appearances in music videos and on national television: my goal is always to leave an unforgettable impression.</p>
<h2>From National TV Studios to International Stages</h2>
<p>My journey has taken me to places few people reach. With appearances for broadcasters such as SBS6, RTL and VTM, and productions in England, I've proven that entertainment is more than an act — it's craftsmanship. Whether it's an intimate wedding, a large corporate event or a dynamic festival set in the Netherlands or Belgium, I bring a level of professionalism and spectacle that gets recognised. Want an unforgettable event of your own? <a href="/en/contact/">Get in touch</a>.</p>
<h3>The Art of the Impossible</h3>
<p>As a fakir and mentalist, my work revolves around the power of mind over body. Pushing the pain threshold and mastering mental forces are central to my shows. My disciplines:</p>
<ul>
<li><strong>Fire mastery:</strong> towering flames and absolute precision.</li>
<li><strong>Fakir techniques:</strong> defying glass and beds of nails with total mental control.</li>
<li><strong>A passion for perfection:</strong> every show is 100% safe, professional and tuned to the venue.</li>
</ul>
<p>Entertainment is in my blood. The passion for the audience and the thrill of the impossible drive me to raise my acts ever higher. Booking Nuno means choosing almost two decades of experience, passion and a guaranteed wow factor.</p>
<h2>Experience the Power of Fire and Magic Yourself</h2>
<p>Ready to lift your event to an unprecedented level? Whether you want to book a <a href="/en/fire-show/"><strong>fire show</strong></a> for an opening, a <a href="/en/fakir-show/">fakir act</a> for a theme party or an interactive <a href="/en/fire-breathing-workshop/">workshop</a>: I'll gladly help turn your vision into reality.</p>
<p>Let's create something legendary together. <a href="/en/contact/">Request a free quote now!</a></p>
""",
 "faq": [],
 "service": None,
}

PAGES["en"]["fotos"] = {
 "title": "Photos of the shows",
 "seo_title": "Photos | Fire show, fakir show & reptile show | Fire breather Nuno",
 "seo_desc": "See photos of Nuno's fire shows, fakir shows, reptile show and workshops at festivals, corporate events and weddings across the Netherlands and Belgium.",
 "eyebrow": "Photos",
 "img": ("/assets/media/festival-1600.webp", "Fire breather Nuno blowing a fireball over a festival crowd"),
 "intro_html": ('<p>A selection from recent years: fire shows at festivals and corporate events, '
                'fakir shows in the theatre, the reptile show and performances at weddings and theme '
                'parties. Click a photo to view it full size &mdash; or '
                '<a href="/en/contact/">request a quote right away</a>.</p>'),
 "captions": {
    "festival":   ("Full fire show on a festival square", "Fire breather Nuno blowing a fireball on a festival square for a large crowd"),
    "vuurbal":    ("Fireball during a night show", "Towering fireball against a black night sky above the fire breather"),
    "avondvuur":  ("Fireball at dusk", "Fire breather Nuno blowing an enormous fireball at dusk"),
    "vuurshow":   ("Daytime fire show at a summer festival", "Daytime fire show at a festival, audience watching from a few metres away"),
    "workshop":   ("Fire breathing against the evening sky", "Fire breather blowing a large fireball against the evening sky from a balustrade"),
    "schemering": ("Fire breathing at twilight", "Fire breathing at twilight, the flame fanning out wide against a blue sky"),
    "themafeest": ("Theme party with fire by the vintage bus", "Fire breather next to a vintage bus during an evening theme party"),
    "bruiloft":   ("Duo act with dancer at a wedding", "Duo act at a wedding: fire breather Nuno with a dancer with red wings"),
    "fakirshow":  ("Fakir show in the theatre", "Fakir show in the theatre: Nuno on the bed of nails bearing the weight of a spectator"),
    "fakir":      ("Fakir act with glass and weight", "Fakir act: Nuno bearing the weight of a standing spectator"),
    "spijkerbed": ("The nail board up close", "Close-up of the fakir act: Nuno balancing the nail board with chains on his face"),
    "reptiel":    ("Reptile show with boa constrictor", "Nuno with a boa constrictor around his arm during the reptile show"),
    "vuurzee":     ("Sea of fire in the nightlife street", "Fire breather Nuno blowing an enormous sea of fire with a rain of sparks in a nightlife street at night"),
    "straatfakir": ("Street fakir show: the audience stands ON Nuno", "Fakir act in the street: two spectators standing on Nuno while he lies on the bed of nails"),
    "glasact":     ("Broken-glass act in the theatre", "Nuno resting his hands in broken glass during a theatre show"),
    "podium":      ("Festival stage for thousands", "Nuno on the festival stage with fire above a cheering festival crowd"),
    "mentalist":  ("Mentalist Nuno in the theatre", "Nuno on the stage of an empty theatre for a mentalism show"),
 },
 "gallery_name": "Photos of fire breather Nuno",
}

PAGES["en"]["videos"] = {
 "title": "Videos of the shows",
 "seo_title": "Videos | Fire show & fakir show in action | Fire breather Nuno",
 "seo_desc": "Watch videos of Nuno's fire shows, fakir acts and performances. Showreels from festivals, corporate events and shows across the Netherlands and Belgium.",
 "eyebrow": "Videos",
 "img": ("/assets/media/reel-1-poster.webp", "Fire breather Nuno during a fire show on location"),
 "intro_html": ('<p>Fire shows, fakir acts and fire breathing in motion: a selection from recent '
                'years. Click a video to play it &mdash; also see <a href="/en/photos/">all photos</a> '
                'or <a href="/en/contact/">request a quote</a>.</p>'),
 "vid_caps": [
    ("Fire show on location", "Fire breather Nuno during a fire show on location: fire breathing, fire juggling and body fire."),
    ("Acts & fakir work", "Compilation of Nuno's fire and fakir acts at festivals and corporate events."),
    ("Showreel", "Short showreel of fire breather and fakir Nuno."),
    ("Fireball in close-up", "Towering fireball by fire breather Nuno, filmed up close."),
 ],
 "gallery_name": "Videos of fire breather Nuno",
}

PAGES["en"]["contact-3"] = {
 "title": "Work with Nuno? Check your date",
 "seo_title": "\U0001F525 Contact | Book fire breather Nuno — reply within 24 hours",
 "seo_desc": "Booking a fire show, fakir show or workshop? Call, WhatsApp or email Nuno, or send the request form with your date and location. Free quote within 24 hours.",
 "eyebrow": "Contact",
 "img": ("/assets/media/themafeest-1080.webp", "Fire breather next to a vintage bus during an evening theme party"),
 "body": """
<p>Working with Nuno? Whether it's a <a href="/en/fire-show/">fire show</a>,
<a href="/en/fakir-show/">fakir show</a>, <a href="/en/fire-breathing-workshop/">fire-breathing
workshop</a> or a complete <a href="/en/halloween/">Halloween production</a>: tell us briefly
what you're celebrating, where and when &mdash; and you'll hear <strong>within 24 hours</strong>
whether your date is free, with a free tailored quote.</p>
""",
 "contact_labels": {"tel_head": "Phone — Mon–Sat, 9:00–18:00", "biz": "Landline / business",
                    "wa": "WhatsApp", "wa_link": "Send a message", "mail": "Email",
                    "area": "Service area", "area_val": "Netherlands, Belgium & international",
                    "note": "For a date within two weeks: calling or WhatsApp is faster than email."},
}

PAGES["en"]["beoordelingen"] = {
 "title": "4.9 out of 136 reviews",
 "seo_title": "⭐ Reviews Fire Breather Nuno — 4.9/5 from 136 reviews",
 "seo_desc": "Read what clients across the Netherlands and Belgium say about Nuno's fire shows and fakir shows. Average 4.9/5 from 136 Google reviews.",
 "eyebrow": "Reviews",
 "img": ("/assets/media/festival-1600.webp", "Fire breather Nuno blowing a fireball over a festival crowd"),
 "texts": {
    "based_on": "based on 136 reviews",
    "google_link": "View the Google profile ›",
    "intro": "Clients from all over the Netherlands and Belgium about Nuno's fire shows, fakir shows and workshops — from Amsterdam to Antwerp and from Groningen to Brussels. The reviews below are shown in their original language.",
    "outro_pre": "Want to read all reviews? See the full overview on ",
    "outro_link": "Nuno's Google profile",
    "outro_post": ". Want an experience like this yourself? ",
    "outro_cta": "Request a free quote",
 },
}

PAGES["en"][""] = {
 "title": "Fire breather Nuno — fire shows, fakir shows & workshops",
 "seo_title": "Fire Breather Nuno | Hire a Fire Show, Fakir Show & Workshop — NL & BE",
 "seo_desc": "Hire professional fire breather Nuno for your event in the Netherlands or Belgium. Fire shows, fakir shows, workshops and Halloween acts. Rated 4.9/5 — free quote within 24 hours.",
 "eyebrow": "Fire breather · fakir · mentalist",
 "img": ("/assets/media/festival-1600.webp", "Fire breather Nuno blowing a fireball over a festival crowd"),
 "home": {
   "intro": """
<p><strong>Seventeen years of fire, on national TV and stages across Europe.</strong> Nuno is one of
the most experienced fire artists of the Netherlands and Belgium: fire breather, fakir, mentalist
and reptile-show artist in one. Certified, fully insured, and rated
<a href="/en/reviews/">4.9 out of 5 from 136 Google reviews</a>.</p>
<p>From a five-minute explosive opener to a complete evening production: every show is tailor-made
for your venue and audience — corporate events, weddings, festivals and private parties, indoors
or outdoors, throughout the Netherlands, Belgium and beyond.</p>
""",
   "shows_head": "The shows",
   "cards": [
     ("vuurspuwer-inhuren", "vuurshow-850.webp", "Fire show", "Towering flames, fire juggling and choreography set to music — the showpiece for any event.", "Daytime fire show at a festival, audience watching from a few metres away"),
     ("fakir-show-inhuren", "fakirshow-640.webp", "Fakir show", "Bed of nails, glass walking and sword acts: tension and wonder from start to finish.", "Fakir show in the theatre: Nuno on the bed of nails bearing the weight of a spectator"),
     ("workshop-vuurspuwen", "workshop-900.webp", "Fire-breathing workshop", "Learn to breathe fire yourself, safely — the ultimate team building or party activity.", "Fire breather blowing a large fireball against the evening sky"),
     ("halloween", "vuurbal-900.webp", "\U0001F383 Halloween acts", "Devilish fire shows and a horror fakir, known from Walibi's Fright Nights. From €350.", "Towering fireball against a black night sky"),
     ("fotos", "festival-900.webp", "Photos", "See the shows in pictures: festivals, weddings, corporate events and theatre.", "Fire breather Nuno blowing a fireball on a festival square"),
     ("videos", "themafeest-900.webp", "Videos", "Showreels and clips of the fire and fakir acts in action.", "Fire breather next to a vintage bus during an evening theme party"),
   ],
   "why_head": "Why book Nuno?",
   "why": [
     ("Certified & insured", "Fully certified as a fire breather and fakir, with professional equipment, safe fuels and liability insurance."),
     ("Seen on TV", "SBS6, RTL, VTM, the Uri Geller show and productions in England."),
     ("4.9/5 from 136 reviews", "Clients across the Netherlands and Belgium rate the shows with top marks."),
     ("Tailor-made", "Every performance is adapted to your venue, theme and audience — indoors or outdoors."),
   ],
   "reviews_head": "What clients say",
   "reviews_link": "Read all 30 featured reviews ›",
   "cta_head": "Check your date",
   "cta_text": "Send the request form and you'll hear within 24 hours whether your date is free — or call or WhatsApp for an immediate answer.",
 },
 "faq": [
  ("Where does fire breather Nuno perform?",
   "Throughout the Netherlands and Belgium — from Amsterdam and Rotterdam to Antwerp and Brussels — and internationally on request. Travel costs are included in the quote."),
  ("What does a fire show cost?",
   "The price depends on the type of show, duration and location. Request a free quote and you'll receive a tailored proposal within 24 hours."),
  ("Is a fire show safe indoors?",
   "Yes, provided the venue meets safety requirements such as ceiling height and ventilation. Nuno has special indoor acts with body fire and fakir techniques."),
  ("How far in advance should I book?",
   "Popular dates — summer weekends, Halloween, New Year's Eve — fill up months ahead. Booking early guarantees your date; last-minute is sometimes possible."),
 ],
}

# ------------------------------------------------------------------ Duits
PAGES["de"]["vuurspuwer-inhuren"] = {
 "title": "Feuerspucker buchen: die spektakulärste Feuershow der Niederlande & Belgiens",
 "seo_title": "\U0001F525 Feuerspucker buchen – Spektakuläre Feuershow NL, BE & Grenzregion",
 "seo_desc": "Feuerspucker für Ihr Event buchen? Nuno ist der meistgebuchte Feuerkünstler der Benelux — auch in der deutschen Grenzregion. Atemberaubende Shows, kostenloses Angebot!",
 "eyebrow": "Feuershow",
 "img": ("/assets/media/avondvuur-1080.webp", "Feuerspucker Nuno bläst einen riesigen Feuerball in den Abendhimmel"),
 "body": """
<p>Sie suchen nicht einfach Unterhaltung, sondern einen Act, der Ihren Gästen buchstäblich den Atem raubt? Eine Eröffnungs- oder Abschlussshow, über die noch Jahre gesprochen wird? Willkommen in der Welt von Nuno.</p>
<p>Als einer der erfahrensten und gefragtesten Feuerkünstler und Fakire der Benelux hebt Nuno jede Veranstaltung auf ein neues Niveau. Mit <a href="/de/ueber-nuno/">über 15 Jahren internationaler Erfahrung</a>, spektakulären TV-Auftritten und absolutem Fokus auf Sicherheit liefert Nuno keinen Standard-Act, sondern ein visuelles Meisterwerk — maßgeschneidert für Ihre Location, auch in der deutschen Grenzregion von Aachen bis Kleve.</p>
<h2>Warum Eventplaner Feuerkünstler Nuno wählen</h2>
<ul>
<li><strong>Visuelles Spektakel auf Weltklasse-Niveau</strong> — keine kleinen Flämmchen, sondern meterhohe Feuerwolken, Feuerjonglage und Choreografien zur Musik.</li>
<li><strong>100 % sicher &amp; zertifiziert</strong> — professionelles Equipment, sichere Brennstoffe und Einhaltung aller Auflagen und Sicherheitsabstände.</li>
<li><strong>High-End-Auftreten</strong> — elegante Kostüme, professionelles Auftreten, pünktliche Kommunikation. Perfekt für Firmenevents.</li>
<li><strong>Flexibel einsetzbar</strong> — Bühne, Schlossgarten oder private Einfahrt: Die Show passt sich Ihrer Location an. Neugierig? <a href="/de/kontakt/">Nehmen Sie Kontakt auf</a>.</li>
</ul>
<h2>Unsere Feuershows: eine Explosion an Entertainment</h2>
<ul>
<li><strong>Der Power-Act (5–10 Min.)</strong> — kurz und explosiv. Ideal als Eröffnung oder spektakuläres Finale.</li>
<li><strong>Die komplette Feuershow (20–30 Min.)</strong> — eine sich steigernde Show mit Fakir-Elementen, Körperfeuer, Feuerspucken und Publikumsinteraktion.</li>
<li><strong>Duo-Shows</strong> — für noch mehr Wirkung ist Nuno auch gemeinsam mit einer Feuerkünstlerin oder Tänzerin buchbar.</li>
</ul>
<p>Drinnen (wo die Location es erlaubt) oder draußen: Wir sorgen für den Wow-Effekt.</p>
<h2>Ebenfalls möglich: interaktive Feuerspucker-Workshops</h2>
<p>Sie möchten nicht nur zuschauen? Nuno bietet einzigartige <a href="/de/feuerspucker-workshop/">Feuerspucker-Workshops</a> an — eine originelle Idee für Teambuilding, Junggesellenabschiede oder abenteuerlustige Betriebsausflüge.</p>
<h2>Für welche Veranstaltungen eignet sich Nuno?</h2>
<ul>
<li>\U0001F389 <strong>Jubiläen &amp; private Feiern</strong> — exklusives Entertainment direkt bei Ihnen im Garten oder vor Ort.</li>
<li>\U0001F3E2 <strong>Firmenfeiern</strong> — beeindrucken Sie Kunden und Mitarbeiter mit einer kraftvollen Eröffnung.</li>
<li>\U0001F48D <strong>Hochzeiten</strong> — eine romantische Feuershow als Alternative zum Feuerwerk (oft erlaubt, wo Feuerwerk verboten ist!).</li>
<li>\U0001F3AA <strong>Festivals &amp; Events</strong> — ein visueller Publikumsmagnet, der auch auf Social Media perfekt funktioniert.</li>
</ul>
<h2>Bereit, Ihr Event zu entflammen?</h2>
<p>Warten Sie nicht zu lange: Nunos Kalender füllt sich schnell, besonders in der Hochsaison. <a href="/de/kontakt/">Verfügbarkeit &amp; Preise prüfen</a>, anrufen unter <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> oder per <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> schreiben.</p>
""",
 "faq": [
  ("Ist eine Feuershow an meiner Location sicher?",
   "Ja — Sicherheit hat oberste Priorität. Nuno arbeitet nach strengen Sicherheitsprotokollen, verwendet professionelle Brennstoffe und Materialien und passt die Show an den verfügbaren Raum an, drinnen wie draußen."),
  ("Was kostet es, einen Feuerspucker zu buchen?",
   "Der Preis hängt von Showtyp, Dauer und Ort ab. Jede Show ist Maßarbeit — fordern Sie ein kostenloses Angebot an und Sie erhalten binnen 24 Stunden einen Vorschlag."),
  ("Kann die Feuershow auch drinnen stattfinden?",
   "Ja, sofern die Location bestimmte Anforderungen erfüllt (Deckenhöhe, Belüftung). Nuno hat spezielle Indoor-Acts mit Körperfeuer und Fakir-Techniken entwickelt."),
  ("Tritt Nuno auch in Deutschland auf?",
   "Ja — Nuno tritt in den gesamten Niederlanden, in Belgien und regelmäßig in der deutschen Grenzregion auf: Aachen, Krefeld, Mönchengladbach, Kleve und Umgebung. Anfahrtskosten werden im Angebot ausgewiesen."),
 ],
 "service": {"name": "Feuershow", "type": "Feuershow / Feuerperformance",
             "desc": "Spektakuläre Feuershow mit Feuerspucken, Feuerjonglage und beeindruckenden Effekten. Professionell, sicher und ideal für Firmenfeiern, Hochzeiten und Festivals."},
 "fotos": [("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Feuerball in der Abenddämmerung", "Feuerspucker Nuno bläst einen riesigen Feuerball in der Abenddämmerung"),
           ("festival-900.webp", "festival-1600.webp", 900, 902, "Komplette Feuershow auf einem Festival", "Feuerspucker Nuno bläst einen Feuerball über eine Festivalmenge"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Feuershow bei Tageslicht", "Feuershow am Tag auf einem Festival, das Publikum schaut aus wenigen Metern zu")],
}

PAGES["de"]["fakir-show-inhuren"] = {
 "title": "Fakirshow: Herrscher über Angst und Schmerz",
 "seo_title": "\U0001F525 Fakirshow buchen – Sensationeller Act von Nuno dem Fakir",
 "seo_desc": "Fakirshow für Ihre Veranstaltung buchen? Nuno der Fakir beherrscht Angst und Schmerz wie kein anderer. Ein unvergesslicher Act, der Ihr Publikum erschaudern lässt!",
 "eyebrow": "Fakirshow",
 "img": ("/assets/media/fakirshow-640.webp", "Fakirshow im Theater: Nuno auf dem Nagelbrett unter dem Gewicht eines Zuschauers"),
 "body": """
<p>Staunen Sie über die vielfältigen Künste der <strong>Fakirshow</strong>! Sie suchen einen originellen, sensationellen Act für Ihre Veranstaltung? <a href="/de/ueber-nuno/">Nuno der Fakir, ein Meister seines Fachs</a>, bietet ein unvergessliches Erlebnis, das Ihr Publikum erschaudern lässt.</p>
<h2>Was Sie von einer Fakirshow erwarten können</h2>
<p>Die Fakirshow ist eine spektakuläre Vorstellung voller atemberaubender Acts. Nuno läuft über Glas, trotzt Nagelbrettern und zeigt beeindruckende Schwertkünste. Feuerspucken — ein Klassiker — darf natürlich nicht fehlen! Das Publikum wird aktiv einbezogen, etwa indem jemand auf dem Fakir steht, während er auf dem Nagelbrett liegt (stets unter Anleitung). Die Show dauert 15 bis 60 Minuten, ganz nach Ihren Wünschen.</p>
<p>Sie möchten die Fakirshow mit anderen Acts kombinieren? Gern — etwa mit <a href="/de/feuershow/">Feuerspucken</a> oder einer Reptilienshow. Wir gestalten gemeinsam ein einzigartiges Erlebnis.</p>
<h2>Locations für eine Fakirshow</h2>
<p>Die Fakirshow eignet sich für nahezu jeden Ort, von der Theaterbühne bis zum Straßenauftritt. Mit jahrelanger Erfahrung liefert Nuno überall eine fantastische Show — länger, kürzer oder ohne Feuerspucken, ganz wie Sie wünschen. Auch mehrere Auftritte hintereinander sind möglich (maximal 4).</p>
<h2>Themen</h2>
<p>Die Acts passen perfekt zu Themen wie 1001 Nacht, Orient, Märchen, Magie oder Karneval. Wir stimmen die Show gern auf Ihre Veranstaltung ab.</p>
<h2>Warum die Fakirshow von Nuno?</h2>
<ul>
<li>Professioneller, erfahrener Künstler</li>
<li>Kombinierbar mit Nunos anderen Acts</li>
<li>Ein Act voller Spannung, Sensation und Staunen</li>
</ul>
<h2>Wie buche ich eine Fakirshow?</h2>
<p>Füllen Sie das <a href="/de/kontakt/">Kontaktformular</a> aus — Sie erhalten binnen 24 Stunden ein kostenloses, unverbindliches Angebot. Bereit, Ihr Publikum zu verblüffen? Melden Sie sich noch heute!</p>
""",
 "faq": [],
 "service": {"name": "Fakirshow", "type": "Fakir-Performance",
             "desc": "Spannende Fakirshow mit klassischen Acts wie Nagelbrett, Glaslaufen und extremen Demonstrationen — sicher ausgeführt mit Erfahrung und Disziplin."},
 "fotos": [("fakirshow-640.webp", "fakirshow-640.webp", 640, 1351, "Fakirshow im Theater", "Fakirshow im Theater: Nuno auf dem Nagelbrett unter dem Gewicht eines Zuschauers"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Das Nagelbrett aus der Nähe", "Nahaufnahme des Fakir-Acts: Nuno balanciert das Nagelbrett mit Ketten auf seinem Gesicht"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Glas und Gewicht", "Fakir-Act: Nuno trägt das Gewicht eines stehenden Zuschauers")],
}

PAGES["de"]["workshop-vuurspuwen"] = {
 "title": "Feuerspucker-Workshop",
 "seo_title": "\U0001F525 Feuerspucker-Workshop | Feuerspucken lernen mit Nuno",
 "seo_desc": "Feuerspucker-Workshop mit professioneller Anleitung von Nuno. Ideal für Teambuilding, Junggesellenabschied oder Firmenfeier. Jetzt Workshop buchen!",
 "eyebrow": "Workshop",
 "img": ("/assets/media/workshop-1125.webp", "Feuerspucker-Workshop unter Anleitung des professionellen Feuerspuckers Nuno"),
 "body": """
<h2>Feuerspucker-Workshop: Entfessle das Feuer in dir (und deinem Team)!</h2>
<p>Träumst du davon, Feuer zu spucken? Willst du ein unvergessliches Erlebnis, das spannend und lehrreich zugleich ist? Dann ist der Feuerspucker-Workshop von Nuno, dem <a href="/de/ueber-nuno/">erfahrenen Feuerspucker und Fakir</a> von Vuurspuwer.com, genau das Richtige. Nuno bringt dir die Kunst des Feuerspuckens und Feueressens sicher und verantwortungsvoll bei. Traust du dich?</p>
<h3>Warum einen Feuerspucker-Workshop machen?</h3>
<ul>
<li><strong>Junggesellenabschiede:</strong> ein feuriger Start ins Eheleben für Braut oder Bräutigam!</li>
<li><strong>Geburtstage:</strong> mach deine Feier mit einer spektakulären Vorführung plus Workshop unvergesslich.</li>
<li><strong>Firmenfeiern:</strong> überrasche deine Kollegen mit einer originellen Aktivität, die den Teamgeist stärkt.</li>
<li><strong>Vereine und Gruppen:</strong> ein Abend voller Spannung, Sensation und unvergesslicher Momente.</li>
<li><strong>Teambuilding:</strong> Zusammenarbeit und Vertrauen im Team auf einzigartige Weise stärken.</li>
</ul>
<h3>Sicherheit geht vor!</h3>
<p>Sicherheit steht immer an erster Stelle. Nuno vermittelt nicht nur die Technik, sondern alles über die Sicherheitsmaßnahmen: die richtigen Brennstoffe, Schutzkleidung und Risikominimierung. Du fühlst dich sicher, bevor du deine erste Flamme spuckst.</p>
<h3>Für Anfänger und Fortgeschrittene</h3>
<p>Ob du noch nie mit Feuer zu tun hattest oder schon Erfahrung mitbringst — der Workshop passt sich deinem Niveau an. Anfänger werden Schritt für Schritt begleitet, Fortgeschrittene lernen neue Techniken und Tricks.</p>
<h3>Teambuilding mit Feuer</h3>
<p>Feuerspucken erfordert Zusammenarbeit, Kommunikation und Vertrauen — die perfekte Teambuilding-Aktivität, die zusammenschweißt.</p>
<h3>Workshop nach Maß</h3>
<p>Von der kurzen Vorführung bis zum kompletten Kurs: Der Workshop wird vollständig an eure Wünsche angepasst — vor Ort in den Niederlanden, Belgien oder der deutschen Grenzregion. <a href="/de/kontakt/">Kontaktiert uns</a> für die Möglichkeiten.</p>
<h3>Buche jetzt dein unvergessliches Feuer-Erlebnis!</h3>
<p>Warte nicht länger und plane noch heute deinen Feuerspucker-Workshop mit Nuno. <a href="/de/kontakt/">Melde dich</a> und mach dein Event zu einem feurigen Erfolg!</p>
""",
 "faq": [
  ("Ist der Feuerspucker-Workshop sicher?",
   "Ja. Sicherheit steht immer an erster Stelle: Zuerst lernst du alles über die richtigen Brennstoffe, Schutzkleidung und Risikominimierung, dann übst du Schritt für Schritt unter Nunos professioneller Anleitung."),
  ("Für wen ist der Workshop geeignet?",
   "Für alle ab 18 Jahren, vom Anfänger bis zum Fortgeschrittenen. Der Workshop passt sich dem Niveau der Gruppe an — ideal für Junggesellenabschiede, Geburtstage, Firmenfeiern und Teambuilding."),
  ("Wo kann der Workshop stattfinden?",
   "Vor Ort in den Niederlanden, Belgien oder der deutschen Grenzregion, sofern draußen genug freier Platz vorhanden ist. Nuno bringt sämtliches Material mit."),
  ("Was kostet ein Feuerspucker-Workshop?",
   "Der Preis hängt von Gruppengröße, Dauer und Ort ab. Fordern Sie ein kostenloses Angebot an — Sie erhalten binnen 24 Stunden einen Vorschlag nach Maß."),
 ],
 "service": {"name": "Feuerspucker-Workshop", "type": "Workshop / Teambuilding",
             "desc": "Feuerspucker-Workshop mit professioneller Anleitung von Nuno. Sicher Feuerspucken und Feueressen lernen — ideal für Teambuilding, Junggesellenabschiede und Firmenfeiern."},
 "fotos": [("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Feuerspucken gegen den Abendhimmel", "Feuerspucker bläst einen großen Feuerball gegen den Abendhimmel"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Feuerball in der Abenddämmerung", "Feuerspucker Nuno bläst einen riesigen Feuerball in der Abenddämmerung"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Feuershow bei Tageslicht", "Feuershow am Tag auf einem Festival")],
}

PAGES["de"]["halloween"] = {
 "title": "Halloween-Feuershow & Horror-Fakir buchen",
 "seo_title": "\U0001F383 Halloween-Feuershow & Horror-Fakir | NL, BE & Grenzregion – ab 350 €",
 "seo_desc": "Halloween-Act buchen? Teuflische Feuershows, Horror-Fakirshow und Scare-Acts — bekannt von den Walibi Fright Nights. Ab 350 €. Der Oktober füllt sich schnell!",
 "eyebrow": "\U0001F383 Oktober · begrenzt verfügbar",
 "img": ("/assets/media/vuurbal-1333.webp", "Meterhoher Feuerball vor schwarzem Nachthimmel über dem Feuerspucker"),
 "body": """
<p>Bekannt von den <strong>Halloween Fright Nights im Walibi Holland</strong>. Teuflische Feuershows, Scare-Acts und ein Horror-Fakir, der Ihre Gäste erschaudern lässt — in den Niederlanden, Belgien und der deutschen Grenzregion.</p>
<h2>Halloween ist die Saison des Feuers</h2>
<p>Kein Fest passt so gut zu Feuer und Dunkelheit wie Halloween. Für diesen Anlass verwandelt sich Nuno in einen Dämon, Teufel oder Horror-Fakir: Flammen, die aus dem Dunkel auftauchen, ein Nagelbrett-Act im Fackelschein, Scare-Momente mitten im Publikum und Mentalismus, der Gedanken ein wenig zu gut liest. Jedes Element wird auf Ihr Thema und Ihre Zielgruppe abgestimmt — von familienfreundlichem Gruseln bis zu Horror für Erwachsene.</p>
<h2>Die Halloween-Acts im Überblick</h2>
<ul>
<li>\U0001F608 <strong>Teuflische Feuershow</strong> — Flammen, Funken und Feuersäulen im Horror-Styling (ab 350 €)</li>
<li>\U0001F5E1️ <strong>Horror-Fakirshow</strong> — Nagelbrett, Glas und Schwerter in Gruselmaske (ab 450 €)</li>
<li>\U0001F441️ <strong>Düsterer Mentalismus</strong> — Gedankenlesen mit unheimlichem Unterton</li>
<li>\U0001F525 <strong>Komplette Halloween-Produktion</strong> — mehrere Acts über den Abend verteilt (ab 750 €)</li>
</ul>
<h2>Früh buchen lohnt sich</h2>
<p>Die Wochenenden um den 31. Oktober sind jedes Jahr zuerst ausgebucht. Buchen Sie am besten vor September; last minute ist manchmal möglich, die Auswahl dann aber begrenzt. <a href="/de/kontakt/">Jetzt Verfügbarkeit prüfen</a> oder per <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a> schreiben.</p>
""",
 "faq": [
  ("Was kostet eine Halloween-Feuershow oder ein Horror-Act?",
   "Halloween-Acts buchen Sie ab 350 € (Feuershow) bzw. 450 € (Horror-Fakirshow). Eine komplette Halloween-Abendproduktion mit mehreren Acts ist ab 750 € möglich. Oktober-Termine sind begrenzt."),
  ("Welche Halloween-Acts sind möglich?",
   "Teuflische Feuershows, ein Horror-Fakir auf Nagelbrett und Glas, Scare-Acts im Publikum, unheimlicher Mentalismus und Kombinationen daraus. Kostüm und Maske werden komplett auf Ihr Thema abgestimmt."),
  ("Hat Nuno Erfahrung mit großen Halloween-Events?",
   "Ja. Nuno stand u. a. bei den Halloween Fright Nights im Walibi Holland auf der Bühne, einem der größten Halloween-Events der Benelux — neben unzähligen Gruseltouren, Horrornächten und Mottopartys."),
  ("Wie früh sollte ich für Halloween buchen?",
   "Die Wochenenden um den 31. Oktober sind jedes Jahr zuerst weg. Buchen Sie am besten vor September, um sich Ihren Termin zu sichern."),
 ],
 "service": {"name": "Halloween-Entertainment", "type": "Halloween-Entertainment",
             "desc": "Halloween-Feuershows, Horror-Fakir-Acts und Scare-Entertainment für Fright Nights, Gruseltouren und Mottopartys in den Niederlanden, Belgien und der Grenzregion.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "3",
                        "description": "Ab-Preis, zzgl. Anfahrt. Kostenloses Angebot nach Maß."}},
 "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Feuerball bei einer Nachtshow", "Meterhoher Feuerball vor schwarzem Nachthimmel über dem Feuerspucker"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Horror-Fakir: das Nagelbrett", "Nahaufnahme des Fakir-Acts: Nuno balanciert das Nagelbrett mit Ketten auf seinem Gesicht"),
           ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Feuer bei der Mottoparty", "Feuerspucker neben einem Oldtimer-Bus bei einer abendlichen Mottoparty")],
}

PAGES["de"]["over-nuno"] = {
 "title": "Über Feuerspucker & Fakir Nuno: 17 Jahre Meisterschaft",
 "seo_title": "\U0001F525 Feuerspucker & Fakir Nuno | 17 Jahre Meisterschaft",
 "seo_desc": "Feuerspucker und Fakir Nuno: 17 Jahre Erfahrung als Entertainer in den Niederlanden, Belgien und der Grenzregion. Feuershow, Fakirshow, Mentalist. Kostenloses Angebot!",
 "eyebrow": "Über Nuno",
 "img": ("/assets/media/mentalist-1371.webp", "Nuno auf der Bühne eines Theaters"),
 "body": """
<p><strong>Feuerspucker und Fakir Nuno gehört seit über 17 Jahren zu den erfahrensten Entertainern der Niederlande und Belgiens. Feuerspucker, Fakir, Mentalist und Reptilienshow-Künstler: Nuno verbindet Handwerkskunst mit Spektakel und hinterlässt bei jedem Auftritt einen bleibenden Eindruck.</strong></p>
<h2>Über Feuerspucker &amp; Fakir Nuno: 17 Jahre Meisterschaft im Entertainment</h2>
<p>Willkommen in einer Welt voller Adrenalin, Leidenschaft und purer Magie. Ich bin Nuno, und seit über 17 Jahren verschiebe ich Grenzen auf der Bühne. Was als Faszination für das Feuer begann, ist zu einer internationalen Karriere als professioneller <strong>Feuerspucker</strong> und Fakir geworden. Von spektakulären Feuershows auf Festivals bis zu mysteriösen Auftritten in Videoclips und im nationalen Fernsehen: Mein Ziel ist immer ein unvergesslicher Eindruck.</p>
<h2>Von nationalen TV-Studios auf internationale Bühnen</h2>
<p>Mein Weg hat mich an Orte geführt, die nur wenige erreichen. Mit Auftritten für Sender wie SBS6, RTL und VTM sowie Produktionen in England habe ich bewiesen: Entertainment ist mehr als ein Act — es ist Handwerkskunst. Ob intime Hochzeit, großes Firmenevent oder dynamisches Festival-Set: Ich bringe ein Niveau an Professionalität und Spektakel, das anerkannt wird. <a href="/de/kontakt/">Nehmen Sie Kontakt auf</a>.</p>
<h3>Die Kunst des Unmöglichen</h3>
<ul>
<li><strong>Feuermeisterschaft:</strong> meterhohe Flammen und höchste Präzision.</li>
<li><strong>Fakir-Techniken:</strong> Glas und Nagelbretter trotzen mit totaler mentaler Kontrolle.</li>
<li><strong>Leidenschaft für Perfektion:</strong> Jede Show ist 100 % sicher, professionell und auf die Location abgestimmt.</li>
</ul>
<p>Entertainment liegt mir im Blut. Die Leidenschaft fürs Publikum und der Kick des Unmöglichen treiben mich an, meine Acts immer weiter zu perfektionieren. Wer Nuno bucht, wählt fast zwei Jahrzehnte Erfahrung, Leidenschaft und den garantierten Wow-Effekt.</p>
<h2>Erleben Sie die Kraft von Feuer und Magie selbst</h2>
<p>Bereit, Ihr Event auf ein neues Niveau zu heben? Ob <a href="/de/feuershow/"><strong>Feuershow</strong></a> zur Eröffnung, <a href="/de/fakirshow/">Fakir-Act</a> für die Mottoparty oder interaktiver <a href="/de/feuerspucker-workshop/">Workshop</a>: Ich helfe gern, Ihre Vision Wirklichkeit werden zu lassen.</p>
<p>Lassen Sie uns gemeinsam etwas Legendäres schaffen. <a href="/de/kontakt/">Jetzt kostenloses Angebot anfordern!</a></p>
""",
 "faq": [],
 "service": None,
}

PAGES["de"]["fotos"] = {
 "title": "Fotos der Shows",
 "seo_title": "Fotos | Feuershow, Fakirshow & Reptilienshow | Feuerspucker Nuno",
 "seo_desc": "Fotos der Feuershows, Fakirshows, Reptilienshow und Workshops von Nuno auf Festivals, Firmenfeiern und Hochzeiten in den Niederlanden, Belgien und der Grenzregion.",
 "eyebrow": "Fotos",
 "img": ("/assets/media/festival-1600.webp", "Feuerspucker Nuno bläst einen Feuerball über eine Festivalmenge"),
 "intro_html": ('<p>Eine Auswahl aus den letzten Jahren: Feuershows auf Festivals und Firmenfeiern, '
                'Fakirshows im Theater, die Reptilienshow und Auftritte auf Hochzeiten und Mottopartys. '
                'Klicken Sie auf ein Foto für die Großansicht &mdash; oder '
                '<a href="/de/kontakt/">fordern Sie direkt ein Angebot an</a>.</p>'),
 "captions": {
    "festival":   ("Komplette Feuershow auf einem Festivalplatz", "Feuerspucker Nuno bläst einen Feuerball auf einem Festivalplatz vor großem Publikum"),
    "vuurbal":    ("Feuerball bei einer Nachtshow", "Meterhoher Feuerball vor schwarzem Nachthimmel über dem Feuerspucker"),
    "avondvuur":  ("Feuerball in der Abenddämmerung", "Feuerspucker Nuno bläst einen riesigen Feuerball in der Abenddämmerung"),
    "vuurshow":   ("Feuershow bei Tageslicht auf einem Sommerfestival", "Feuershow am Tag auf einem Festival, das Publikum schaut aus wenigen Metern zu"),
    "workshop":   ("Feuerspucken gegen den Abendhimmel", "Feuerspucker bläst einen großen Feuerball gegen den Abendhimmel von einer Balustrade"),
    "schemering": ("Feuerspucken in der Dämmerung", "Feuerspucken in der Dämmerung, die Flamme fächert breit vor blauem Himmel auf"),
    "themafeest": ("Mottoparty mit Feuer am Oldtimer-Bus", "Feuerspucker neben einem Oldtimer-Bus bei einer abendlichen Mottoparty"),
    "bruiloft":   ("Duo-Act mit Tänzerin auf einer Hochzeit", "Duo-Act auf einer Hochzeit: Feuerspucker Nuno mit Tänzerin mit roten Flügeln"),
    "fakirshow":  ("Fakirshow im Theater", "Fakirshow im Theater: Nuno auf dem Nagelbrett unter dem Gewicht eines Zuschauers"),
    "fakir":      ("Fakir-Act mit Glas und Gewicht", "Fakir-Act: Nuno trägt das Gewicht eines stehenden Zuschauers"),
    "spijkerbed": ("Das Nagelbrett aus der Nähe", "Nahaufnahme des Fakir-Acts: Nuno balanciert das Nagelbrett mit Ketten auf seinem Gesicht"),
    "reptiel":    ("Reptilienshow mit Boa constrictor", "Nuno mit einer Boa constrictor um den Arm während der Reptilienshow"),
    "vuurzee":     ("Feuermeer in der Ausgehstraße", "Feuerspucker Nuno bläst ein riesiges Feuermeer mit Funkenregen in einer Ausgehstraße bei Nacht"),
    "straatfakir": ("Fakirshow auf der Straße: das Publikum steht AUF Nuno", "Fakir-Act auf der Straße: zwei Zuschauer stehen auf Nuno, während er auf dem Nagelbrett liegt"),
    "glasact":     ("Glasscherben-Act im Theater", "Nuno stützt sich während einer Theatershow mit den Händen in Glasscherben"),
    "podium":      ("Festivalbühne vor Tausenden", "Nuno auf der Festivalbühne mit Feuer über einer jubelnden Menge"),
    "mentalist":  ("Mentalist Nuno im Theater", "Nuno auf der Bühne eines leeren Theaters für eine Mentalismus-Show"),
 },
 "gallery_name": "Fotos von Feuerspucker Nuno",
}

PAGES["de"]["videos"] = {
 "title": "Videos der Shows",
 "seo_title": "Videos | Feuershow & Fakirshow in Aktion | Feuerspucker Nuno",
 "seo_desc": "Videos der Feuershows, Fakir-Acts und Auftritte von Nuno. Showreels von Festivals, Firmenfeiern und Events in den Niederlanden, Belgien und der Grenzregion.",
 "eyebrow": "Videos",
 "img": ("/assets/media/reel-1-poster.webp", "Feuerspucker Nuno während einer Feuershow vor Ort"),
 "intro_html": ('<p>Feuershows, Fakir-Acts und Feuerspucken in Bewegung: eine Auswahl aus den '
                'letzten Jahren. Klicken Sie auf ein Video zum Abspielen &mdash; sehen Sie auch '
                '<a href="/de/fotos/">alle Fotos</a> oder <a href="/de/kontakt/">fordern Sie ein Angebot an</a>.</p>'),
 "vid_caps": [
    ("Feuershow vor Ort", "Feuerspucker Nuno bei einer Feuershow vor Ort: Feuerspucken, Feuerjonglage und Körperfeuer."),
    ("Acts & Fakirkunst", "Zusammenschnitt der Feuer- und Fakir-Acts von Nuno auf Festivals und Firmenfeiern."),
    ("Showreel", "Kurzes Showreel von Feuerspucker und Fakir Nuno."),
    ("Feuerball in Nahaufnahme", "Meterhoher Feuerball von Feuerspucker Nuno, aus der Nähe gefilmt."),
 ],
 "gallery_name": "Videos von Feuerspucker Nuno",
}

PAGES["de"]["contact-3"] = {
 "title": "Mit Nuno arbeiten? Termin prüfen",
 "seo_title": "\U0001F525 Kontakt | Feuerspucker Nuno buchen — Antwort binnen 24 Stunden",
 "seo_desc": "Feuershow, Fakirshow oder Workshop buchen? Rufen Sie an, schreiben Sie per WhatsApp oder senden Sie das Formular mit Datum und Ort. Kostenloses Angebot binnen 24 Stunden.",
 "eyebrow": "Kontakt",
 "img": ("/assets/media/themafeest-1080.webp", "Feuerspucker neben einem Oldtimer-Bus bei einer abendlichen Mottoparty"),
 "body": """
<p>Mit Nuno zusammenarbeiten? Ob <a href="/de/feuershow/">Feuershow</a>,
<a href="/de/fakirshow/">Fakirshow</a>, <a href="/de/feuerspucker-workshop/">Feuerspucker-Workshop</a>
oder eine komplette <a href="/de/halloween/">Halloween-Produktion</a>: Erzählen Sie kurz, was Sie
feiern, wo und wann &mdash; und Sie hören <strong>binnen 24 Stunden</strong>, ob Ihr Termin frei
ist, mit einem kostenlosen Angebot nach Maß.</p>
""",
 "contact_labels": {"tel_head": "Telefon — Mo–Sa, 9:00–18:00", "biz": "Festnetz / geschäftlich",
                    "wa": "WhatsApp", "wa_link": "Nachricht senden", "mail": "E-Mail",
                    "area": "Einsatzgebiet", "area_val": "Niederlande, Belgien, Grenzregion & international",
                    "note": "Für einen Termin innerhalb von zwei Wochen: Anruf oder WhatsApp geht schneller als E-Mail."},
}

PAGES["de"]["beoordelingen"] = {
 "title": "4,9 aus 136 Bewertungen",
 "seo_title": "⭐ Bewertungen Feuerspucker Nuno — 4,9/5 aus 136 Bewertungen",
 "seo_desc": "Lesen Sie, was Auftraggeber aus den Niederlanden und Belgien über die Feuershows und Fakirshows von Nuno sagen. Durchschnittlich 4,9/5 aus 136 Google-Bewertungen.",
 "eyebrow": "Bewertungen",
 "img": ("/assets/media/festival-1600.webp", "Feuerspucker Nuno bläst einen Feuerball über eine Festivalmenge"),
 "texts": {
    "based_on": "basierend auf 136 Bewertungen",
    "google_link": "Google-Profil ansehen ›",
    "intro": "Auftraggeber aus den gesamten Niederlanden und Belgien über die Feuershows, Fakirshows und Workshops von Nuno — von Amsterdam bis Antwerpen und von Groningen bis Brüssel. Die Bewertungen werden in der Originalsprache angezeigt.",
    "outro_pre": "Alle Bewertungen lesen? Die komplette Übersicht finden Sie im ",
    "outro_link": "Google-Profil von Nuno",
    "outro_post": ". Selbst so ein Erlebnis buchen? ",
    "outro_cta": "Kostenloses Angebot anfordern",
 },
}

PAGES["de"][""] = {
 "title": "Feuerspucker Nuno — Feuershows, Fakirshows & Workshops",
 "seo_title": "Feuerspucker Nuno | Feuershow, Fakirshow & Workshop buchen — NL, BE & Grenzregion",
 "seo_desc": "Buchen Sie den professionellen Feuerspucker Nuno für Ihr Event — Niederlande, Belgien und die deutsche Grenzregion. Feuershows, Fakirshows, Workshops. 4,9/5 — Angebot binnen 24 h.",
 "eyebrow": "Feuerspucker · Fakir · Mentalist",
 "img": ("/assets/media/festival-1600.webp", "Feuerspucker Nuno bläst einen Feuerball über eine Festivalmenge"),
 "home": {
   "intro": """
<p><strong>Siebzehn Jahre Feuer — im nationalen Fernsehen und auf Bühnen in ganz Europa.</strong>
Nuno gehört zu den erfahrensten Feuerkünstlern der Niederlande und Belgiens und tritt regelmäßig
in der deutschen Grenzregion auf: Feuerspucker, Fakir, Mentalist und Reptilienshow-Künstler in
einer Person. Zertifiziert, versichert und mit <a href="/de/bewertungen/">4,9 von 5 Sternen aus
136 Google-Bewertungen</a>.</p>
<p>Vom fünfminütigen explosiven Opener bis zur kompletten Abendproduktion: Jede Show ist Maßarbeit
für Ihre Location und Ihr Publikum — Firmenfeiern, Hochzeiten, Festivals und private Feste,
drinnen wie draußen, von Amsterdam bis Aachen.</p>
""",
   "shows_head": "Die Shows",
   "cards": [
     ("vuurspuwer-inhuren", "vuurshow-850.webp", "Feuershow", "Meterhohe Flammen, Feuerjonglage und Choreografien zur Musik — das Herzstück jedes Events.", "Feuershow am Tag auf einem Festival"),
     ("fakir-show-inhuren", "fakirshow-640.webp", "Fakirshow", "Nagelbrett, Glaslaufen und Schwert-Acts: Spannung und Staunen von Anfang bis Ende.", "Fakirshow im Theater: Nuno auf dem Nagelbrett"),
     ("workshop-vuurspuwen", "workshop-900.webp", "Feuerspucker-Workshop", "Selbst sicher Feuerspucken lernen — das ultimative Teambuilding.", "Feuerspucker bläst einen großen Feuerball gegen den Abendhimmel"),
     ("halloween", "vuurbal-900.webp", "\U0001F383 Halloween-Acts", "Teuflische Feuershows und ein Horror-Fakir, bekannt von den Walibi Fright Nights. Ab 350 €.", "Meterhoher Feuerball vor schwarzem Nachthimmel"),
     ("fotos", "festival-900.webp", "Fotos", "Die Shows in Bildern: Festivals, Hochzeiten, Firmenfeiern und Theater.", "Feuerspucker Nuno auf einem Festivalplatz"),
     ("videos", "themafeest-900.webp", "Videos", "Showreels und Clips der Feuer- und Fakir-Acts in Aktion.", "Feuerspucker neben einem Oldtimer-Bus"),
   ],
   "why_head": "Warum Nuno buchen?",
   "why": [
     ("Zertifiziert & versichert", "Vollständig zertifiziert als Feuerspucker und Fakir, mit professionellem Equipment, sicheren Brennstoffen und Haftpflichtversicherung."),
     ("Bekannt aus dem TV", "SBS6, RTL, VTM, die Uri-Geller-Show und Produktionen in England."),
     ("4,9/5 aus 136 Bewertungen", "Auftraggeber aus den Niederlanden und Belgien bewerten die Shows mit Bestnoten."),
     ("Maßarbeit", "Jeder Auftritt wird an Location, Thema und Publikum angepasst — drinnen wie draußen."),
   ],
   "reviews_head": "Das sagen Auftraggeber",
   "reviews_link": "Alle 30 ausgewählten Bewertungen lesen ›",
   "cta_head": "Termin prüfen",
   "cta_text": "Senden Sie das Anfrageformular und Sie hören binnen 24 Stunden, ob Ihr Termin frei ist — oder rufen Sie an bzw. schreiben Sie per WhatsApp für eine sofortige Antwort.",
 },
 "faq": [
  ("Wo tritt Feuerspucker Nuno auf?",
   "In den gesamten Niederlanden und Belgien sowie regelmäßig in der deutschen Grenzregion: Aachen, Krefeld, Mönchengladbach, Kleve und Umgebung. International auf Anfrage."),
  ("Was kostet eine Feuershow?",
   "Der Preis hängt von Showtyp, Dauer und Ort ab. Fordern Sie ein kostenloses Angebot an — Sie erhalten binnen 24 Stunden einen Vorschlag nach Maß."),
  ("Ist eine Feuershow drinnen sicher?",
   "Ja, sofern die Location Anforderungen wie Deckenhöhe und Belüftung erfüllt. Nuno hat spezielle Indoor-Acts mit Körperfeuer und Fakir-Techniken."),
  ("Wie früh sollte ich buchen?",
   "Beliebte Termine — Sommerwochenenden, Halloween, Silvester — sind Monate im Voraus vergeben. Früh buchen sichert den Termin; last minute ist manchmal möglich."),
 ],
}

# ------------------------------------------------------------------ Frans
PAGES["fr"]["vuurspuwer-inhuren"] = {
 "title": "Engager un cracheur de feu : le spectacle de feu le plus spectaculaire des Pays-Bas et de Belgique",
 "seo_title": "\U0001F525 Cracheur de Feu – Spectacle de Feu Spectaculaire | Belgique & Pays-Bas",
 "seo_desc": "Engager un cracheur de feu professionnel en Belgique ou aux Pays-Bas ? Nuno est l'artiste de feu le plus demandé du Benelux. Spectacles à couper le souffle. Devis gratuit !",
 "eyebrow": "Spectacle de feu",
 "img": ("/assets/media/avondvuur-1080.webp", "Le cracheur de feu Nuno soufflant une énorme boule de feu dans le ciel du soir"),
 "body": """
<p>Vous cherchez plus qu'un simple divertissement — un numéro qui laisse vos invités littéralement sans voix ? Un spectacle d'ouverture ou de clôture dont on parlera encore pendant des années ? Bienvenue dans l'univers de Nuno.</p>
<p>Artiste de feu et fakir parmi les plus expérimentés et les plus demandés du Benelux, Nuno élève chaque événement à un autre niveau. Avec <a href="/fr/a-propos-de-nuno/">plus de 15 ans d'expérience internationale</a>, des passages spectaculaires à la télévision et une priorité absolue à la sécurité, Nuno ne livre pas un numéro standard mais un chef-d'œuvre visuel haut de gamme — adapté à votre lieu, partout en Wallonie, à Bruxelles et aux Pays-Bas.</p>
<h2>Pourquoi les organisateurs choisissent l'artiste de feu Nuno</h2>
<ul>
<li><strong>Un spectacle visuel de classe mondiale</strong> — pas de petites flammes, mais des nuages de feu de plusieurs mètres, du jonglage enflammé et des chorégraphies en musique.</li>
<li><strong>100 % sûr &amp; certifié</strong> — matériel professionnel, combustibles sûrs et respect de toutes les autorisations et distances de sécurité.</li>
<li><strong>Une présentation haut de gamme</strong> — costumes soignés, attitude professionnelle et communication ponctuelle. Parfait pour les événements d'entreprise.</li>
<li><strong>Flexible</strong> — une scène à Bruxelles, un jardin de château à Liège ou une allée intime : le spectacle s'adapte à votre lieu. Curieux ? <a href="/fr/contact/">Contactez-nous</a>.</li>
</ul>
<h2>Nos spectacles de feu : une explosion de divertissement</h2>
<ul>
<li><strong>Le Power Act (5–10 min)</strong> — court et explosif. Idéal en ouverture ou en final spectaculaire.</li>
<li><strong>Le spectacle complet (20–30 min)</strong> — un show progressif avec éléments de fakir, feu corporel, crachage de feu et interaction avec le public.</li>
<li><strong>Les duos</strong> — pour encore plus d'impact, Nuno peut se produire avec une artiste de feu ou une danseuse.</li>
</ul>
<p>En intérieur (si le lieu le permet) ou en extérieur : l'effet wow est garanti.</p>
<h2>Également possible : ateliers interactifs de crachage de feu</h2>
<p>Envie de participer plutôt que de regarder ? Nuno propose des <a href="/fr/atelier-cracheur-de-feu/">ateliers cracheur de feu</a> uniques — une idée originale pour un team building, un enterrement de vie de garçon ou une sortie d'entreprise audacieuse.</p>
<h2>Pour quels événements ?</h2>
<ul>
<li>\U0001F389 <strong>Jubilés &amp; fêtes privées</strong> — un divertissement exclusif dans votre jardin ou sur votre lieu.</li>
<li>\U0001F3E2 <strong>Événements d'entreprise</strong> — impressionnez clients et collaborateurs avec une ouverture puissante.</li>
<li>\U0001F48D <strong>Mariages</strong> — un spectacle de feu romantique comme alternative au feu d'artifice (souvent autorisé là où les feux d'artifice sont interdits !).</li>
<li>\U0001F3AA <strong>Festivals &amp; événements</strong> — un aimant visuel qui fonctionne à merveille sur les réseaux sociaux.</li>
</ul>
<h2>Prêt à enflammer votre événement ?</h2>
<p>N'attendez pas trop longtemps pour réserver votre date : l'agenda de Nuno se remplit vite, surtout en haute saison. <a href="/fr/contact/">Vérifiez la disponibilité et les prix</a>, appelez le <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> ou envoyez un message <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
""",
 "faq": [
  ("Un spectacle de feu est-il sûr sur mon lieu ?",
   "Oui — la sécurité est la priorité numéro un. Nuno suit des protocoles stricts, utilise des combustibles et du matériel professionnels et adapte le spectacle à l'espace disponible, en intérieur comme en extérieur."),
  ("Combien coûte un cracheur de feu ?",
   "Le prix dépend du type de spectacle, de sa durée et du lieu. Chaque spectacle est du sur-mesure : demandez un devis gratuit et recevez une proposition sous 24 heures."),
  ("Le spectacle peut-il avoir lieu en intérieur ?",
   "Oui, à condition que le lieu réponde à certaines exigences (hauteur de plafond, ventilation). Nuno a développé des numéros d'intérieur avec feu corporel et techniques de fakir."),
  ("Où se produit le cracheur de feu Nuno ?",
   "Dans toute la Belgique — Bruxelles, Liège, la Wallonie et la Flandre — ainsi qu'aux Pays-Bas, et à l'international sur demande. Les frais de déplacement figurent dans le devis."),
 ],
 "service": {"name": "Spectacle de feu", "type": "Spectacle de feu / Performance de feu",
             "desc": "Spectacle de feu spectaculaire avec crachage de feu, jonglage enflammé et effets impressionnants. Professionnel, sûr et idéal pour événements d'entreprise, mariages et festivals."},
 "fotos": [("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Boule de feu au crépuscule", "Le cracheur de feu Nuno soufflant une énorme boule de feu au crépuscule"),
           ("festival-900.webp", "festival-1600.webp", 900, 902, "Spectacle de feu complet en festival", "Le cracheur de feu Nuno soufflant une boule de feu au-dessus d'une foule de festival"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Spectacle de feu en plein jour", "Spectacle de feu en plein jour lors d'un festival, le public à quelques mètres")],
}

PAGES["fr"]["fakir-show-inhuren"] = {
 "title": "Spectacle de fakir : maître de la peur et de la douleur",
 "seo_title": "\U0001F525 Spectacle de Fakir – Numéro Sensationnel de Nuno le Fakir",
 "seo_desc": "Réserver un spectacle de fakir pour votre événement ? Nuno le Fakir maîtrise la peur et la douleur comme personne — un numéro inoubliable qui fera frissonner votre public !",
 "eyebrow": "Spectacle de fakir",
 "img": ("/assets/media/fakirshow-640.webp", "Spectacle de fakir au théâtre : Nuno sur le lit de clous portant le poids d'un spectateur"),
 "body": """
<p>Émerveillez-vous devant les multiples arts du <strong>spectacle de fakir</strong> ! Vous cherchez un numéro original et sensationnel pour votre événement ? <a href="/fr/a-propos-de-nuno/">Nuno le Fakir, maître en son art</a>, offre une expérience inoubliable qui fera frissonner votre public.</p>
<h2>À quoi s'attendre ?</h2>
<p>Le spectacle de fakir est une représentation spectaculaire pleine de numéros à couper le souffle. Nuno marche sur du verre, défie les lits de clous et démontre d'impressionnants talents à l'épée. Le crachage de feu — un classique — est bien sûr de la partie ! Le public participe activement, par exemple en montant sur le fakir allongé sur son lit de clous (toujours sous supervision). Le spectacle dure de 15 à 60 minutes, selon vos souhaits.</p>
<p>Envie de combiner le spectacle de fakir avec d'autres numéros ? C'est possible — pensez au <a href="/fr/spectacle-de-feu/">crachage de feu</a> ou à un spectacle de reptiles. Nous créons volontiers une expérience unique avec vous.</p>
<h2>Les lieux</h2>
<p>Le spectacle de fakir convient à presque tous les lieux, de la scène de théâtre à la rue. Fort de longues années d'expérience, Nuno livre partout un spectacle fantastique — plus long, plus court ou sans crachage de feu, selon vos envies. Plusieurs représentations à la suite sont possibles (maximum 4).</p>
<h2>Les thèmes</h2>
<p>Les numéros s'accordent parfaitement aux thèmes comme les 1001 nuits, l'Orient, les contes, la magie ou le carnaval. Nous adaptons volontiers le spectacle à votre événement.</p>
<h2>Pourquoi choisir le spectacle de fakir de Nuno ?</h2>
<ul>
<li>Un artiste professionnel et expérimenté</li>
<li>Combinable avec les autres numéros de Nuno</li>
<li>Un numéro plein de tension, de sensation et d'émerveillement</li>
</ul>
<h2>Comment réserver ?</h2>
<p>Remplissez le <a href="/fr/contact/">formulaire de contact</a> et recevez sous 24 heures un devis gratuit et sans engagement. Prêt à éblouir votre public ? Contactez-nous dès aujourd'hui !</p>
""",
 "faq": [],
 "service": {"name": "Spectacle de fakir", "type": "Performance de fakir",
             "desc": "Spectacle de fakir palpitant avec des numéros classiques comme le lit de clous, la marche sur verre et des démonstrations extrêmes, exécutés en toute sécurité avec expérience et discipline."},
 "fotos": [("fakirshow-640.webp", "fakirshow-640.webp", 640, 1351, "Spectacle de fakir au théâtre", "Spectacle de fakir au théâtre : Nuno sur le lit de clous portant le poids d'un spectateur"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Le lit de clous de près", "Gros plan du numéro de fakir : Nuno en équilibre avec la planche à clous et des chaînes sur le visage"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124, "Verre et poids", "Numéro de fakir : Nuno portant le poids d'un spectateur debout")],
}

PAGES["fr"]["workshop-vuurspuwen"] = {
 "title": "Atelier cracheur de feu",
 "seo_title": "\U0001F525 Atelier Cracheur de Feu | Apprenez à Cracher le Feu avec Nuno",
 "seo_desc": "Atelier cracheur de feu avec l'encadrement professionnel de Nuno. Idéal pour un team building, un enterrement de vie de garçon ou une fête d'entreprise. Réservez !",
 "eyebrow": "Atelier",
 "img": ("/assets/media/workshop-1125.webp", "Atelier cracheur de feu sous la direction du cracheur de feu professionnel Nuno"),
 "body": """
<h2>Atelier Cracheur de Feu : libérez le feu en vous (et dans votre équipe) !</h2>
<p>Vous rêvez de cracher du feu ? Envie d'une expérience inoubliable, à la fois palpitante et instructive ? Alors l'atelier cracheur de feu de Nuno, le <a href="/fr/a-propos-de-nuno/">cracheur de feu et fakir expérimenté</a> de Vuurspuwer.com, est exactement ce qu'il vous faut. Nuno vous enseigne l'art de cracher et de manger le feu de manière sûre et responsable. Oserez-vous ?</p>
<h3>Pourquoi suivre un atelier cracheur de feu ?</h3>
<ul>
<li><strong>Enterrements de vie de garçon/fille :</strong> offrez aux futurs mariés un départ enflammé !</li>
<li><strong>Anniversaires :</strong> rendez votre fête inoubliable avec une démonstration spectaculaire suivie d'un atelier.</li>
<li><strong>Fêtes d'entreprise :</strong> surprenez vos collègues avec une activité originale qui renforce l'esprit d'équipe.</li>
<li><strong>Associations et groupes :</strong> une soirée pleine de tension, de sensations et de moments inoubliables.</li>
<li><strong>Team building :</strong> améliorez la coopération et la confiance au sein de votre équipe de façon unique.</li>
</ul>
<h3>La sécurité avant tout !</h3>
<p>La sécurité passe toujours en premier. Nuno vous enseigne non seulement les techniques, mais aussi tout ce qui concerne les mesures de sécurité : les bons combustibles, les vêtements de protection et la réduction des risques. Vous vous sentirez en confiance avant de cracher votre première flamme.</p>
<h3>Pour débutants et confirmés</h3>
<p>Que vous n'ayez jamais touché au feu ou que vous ayez déjà de l'expérience, l'atelier s'adapte à chacun. Les débutants sont guidés pas à pas, les confirmés apprennent de nouvelles techniques.</p>
<h3>Team building avec le feu</h3>
<p>Cracher le feu exige coopération, communication et confiance — l'activité de team building parfaite, qui soude une équipe pour longtemps.</p>
<h3>Un atelier sur mesure</h3>
<p>De la courte démonstration au cours complet : l'atelier s'adapte entièrement à vos souhaits, sur place en Belgique ou aux Pays-Bas. <a href="/fr/contact/">Contactez-nous</a> pour en discuter.</p>
<h3>Réservez votre expérience de feu inoubliable !</h3>
<p>N'attendez plus et planifiez dès aujourd'hui votre atelier cracheur de feu avec Nuno. <a href="/fr/contact/">Contactez-nous</a> et faites de votre événement un succès enflammé !</p>
""",
 "faq": [
  ("L'atelier cracheur de feu est-il sûr ?",
   "Oui. La sécurité passe toujours en premier : vous apprenez d'abord tout sur les bons combustibles, les vêtements de protection et la réduction des risques, puis vous pratiquez pas à pas sous l'encadrement professionnel de Nuno."),
  ("À qui s'adresse l'atelier ?",
   "À toute personne de 18 ans ou plus, du débutant complet au participant confirmé. L'atelier s'adapte au niveau du groupe — idéal pour enterrements de vie de garçon, anniversaires, fêtes d'entreprise et team building."),
  ("Où l'atelier peut-il avoir lieu ?",
   "Sur place partout en Belgique et aux Pays-Bas, à condition de disposer d'assez d'espace libre en extérieur. Nuno apporte tout le matériel."),
  ("Combien coûte un atelier cracheur de feu ?",
   "Le prix dépend de la taille du groupe, de la durée et du lieu. Demandez un devis gratuit — vous recevrez une proposition sur mesure sous 24 heures."),
 ],
 "service": {"name": "Atelier cracheur de feu", "type": "Atelier / Team building",
             "desc": "Atelier cracheur de feu avec encadrement professionnel de Nuno. Apprenez à cracher et manger le feu en toute sécurité — idéal pour team building, enterrements de vie de garçon et fêtes d'entreprise."},
 "fotos": [("workshop-900.webp", "workshop-1125.webp", 900, 1130, "Crachage de feu dans le ciel du soir", "Cracheur de feu soufflant une grande boule de feu dans le ciel du soir"),
           ("avondvuur-900.webp", "avondvuur-1080.webp", 900, 893, "Boule de feu au crépuscule", "Le cracheur de feu Nuno soufflant une énorme boule de feu au crépuscule"),
           ("vuurshow-850.webp", "vuurshow-850.webp", 850, 1024, "Spectacle de feu en plein jour", "Spectacle de feu en plein jour lors d'un festival")],
}

PAGES["fr"]["halloween"] = {
 "title": "Réserver un spectacle de feu Halloween & fakir d'horreur",
 "seo_title": "\U0001F383 Spectacle de Feu Halloween & Fakir d'Horreur | BE & NL – dès 350 €",
 "seo_desc": "Réserver une animation Halloween ? Spectacles de feu diaboliques, fakir d'horreur et scare acts — connu des Walibi Fright Nights. Dès 350 €. Octobre se remplit vite !",
 "eyebrow": "\U0001F383 Octobre · disponibilité limitée",
 "img": ("/assets/media/vuurbal-1333.webp", "Immense boule de feu contre un ciel nocturne noir au-dessus du cracheur de feu"),
 "body": """
<p>Connu des <strong>Halloween Fright Nights de Walibi Holland</strong>. Spectacles de feu diaboliques, scare acts et un fakir d'horreur qui fera frissonner vos invités — dans toute la Belgique et aux Pays-Bas.</p>
<h2>Halloween est la saison du feu</h2>
<p>Aucune fête ne s'accorde mieux au feu et à l'obscurité qu'Halloween. Pour l'occasion, Nuno se transforme en démon, diable ou fakir d'horreur : des flammes qui surgissent du noir, un numéro de lit de clous à la lueur des torches, des moments de frayeur au milieu du public et du mentalisme qui lit les pensées un peu trop bien. Chaque élément est adapté à votre thème et à votre public — du frisson familial à l'horreur pour adultes.</p>
<h2>Les animations Halloween en un coup d'œil</h2>
<ul>
<li>\U0001F608 <strong>Spectacle de feu diabolique</strong> — flammes, étincelles et colonnes de feu en style horreur (dès 350 €)</li>
<li>\U0001F5E1️ <strong>Fakir d'horreur</strong> — lit de clous, verre et épées en maquillage effrayant (dès 450 €)</li>
<li>\U0001F441️ <strong>Mentalisme sombre</strong> — lecture de pensées avec une touche sinistre</li>
<li>\U0001F525 <strong>Production Halloween complète</strong> — plusieurs numéros répartis sur la soirée (dès 750 €)</li>
</ul>
<h2>Réservez tôt</h2>
<p>Les week-ends autour du 31 octobre partent toujours en premier. Réservez de préférence avant septembre ; la dernière minute est parfois possible, mais le choix est alors limité. <a href="/fr/contact/">Vérifiez la disponibilité</a> ou envoyez un message <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
""",
 "faq": [
  ("Combien coûte un spectacle de feu ou une animation d'horreur pour Halloween ?",
   "Les animations Halloween démarrent à 350 € (spectacle de feu) ou 450 € (fakir d'horreur). Une production complète de soirée avec plusieurs numéros est possible dès 750 €. Les dates d'octobre sont limitées."),
  ("Quelles animations Halloween sont possibles ?",
   "Spectacles de feu diaboliques, un fakir d'horreur sur lit de clous et verre, des scare acts dans le public, du mentalisme inquiétant et leurs combinaisons. Costume et maquillage sont entièrement adaptés à votre thème."),
  ("Nuno a-t-il l'expérience des grands événements Halloween ?",
   "Oui. Nuno s'est produit aux Halloween Fright Nights de Walibi Holland, l'un des plus grands événements Halloween du Benelux, en plus d'innombrables parcours hantés, nuits d'horreur et fêtes à thème."),
  ("Quand réserver pour Halloween ?",
   "Les week-ends autour du 31 octobre partent chaque année en premier. Réservez avant septembre pour garantir votre date."),
 ],
 "service": {"name": "Animations Halloween", "type": "Divertissement Halloween",
             "desc": "Spectacles de feu Halloween, numéros de fakir d'horreur et scare entertainment pour fright nights, parcours hantés et fêtes à thème en Belgique et aux Pays-Bas.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "3",
                        "description": "Prix de départ, hors frais de déplacement. Devis gratuit sur mesure."}},
 "fotos": [("vuurbal-900.webp", "vuurbal-1333.webp", 900, 1350, "Boule de feu lors d'un spectacle nocturne", "Immense boule de feu contre un ciel nocturne noir au-dessus du cracheur de feu"),
           ("spijkerbed-900.webp", "spijkerbed-1242.webp", 900, 873, "Fakir d'horreur : la planche à clous", "Gros plan du numéro de fakir : Nuno en équilibre avec la planche à clous"),
           ("themafeest-900.webp", "themafeest-1080.webp", 900, 1125, "Feu à la fête à thème", "Cracheur de feu à côté d'un bus vintage lors d'une fête à thème en soirée")],
}

PAGES["fr"]["over-nuno"] = {
 "title": "À propos du cracheur de feu & fakir Nuno : 17 ans de maîtrise",
 "seo_title": "\U0001F525 Cracheur de Feu & Fakir Nuno | 17 Ans de Maîtrise",
 "seo_desc": "Cracheur de feu et fakir Nuno : 17 ans d'expérience comme artiste en Belgique et aux Pays-Bas. Spectacle de feu, fakir, mentaliste et spectacle de reptiles. Devis gratuit !",
 "eyebrow": "À propos de Nuno",
 "img": ("/assets/media/mentalist-1371.webp", "Nuno sur la scène d'un théâtre"),
 "body": """
<p><strong>Cracheur de feu et fakir, Nuno compte depuis plus de 17 ans parmi les artistes les plus expérimentés des Pays-Bas et de Belgique. Cracheur de feu, fakir, mentaliste et artiste de spectacle de reptiles : Nuno allie savoir-faire et spectacle et laisse une impression durable à chaque représentation.</strong></p>
<h2>À propos du Cracheur de Feu &amp; Fakir Nuno : 17 ans de maîtrise du divertissement</h2>
<p>Bienvenue dans un monde d'adrénaline, de passion et de pure magie. Je m'appelle Nuno et, depuis plus de 17 ans, je repousse les limites sur scène. Ce qui a commencé comme une fascination pour le feu est devenu une carrière internationale de <strong>cracheur de feu</strong> et fakir professionnel. Des spectacles de feu spectaculaires en festival aux apparitions mystérieuses dans des clips et à la télévision nationale : mon objectif est toujours de laisser une impression inoubliable.</p>
<h2>Des studios de télévision aux scènes internationales</h2>
<p>Mon parcours m'a mené là où peu de gens vont. Avec des passages pour des chaînes comme SBS6, RTL et VTM, et des productions en Angleterre, j'ai prouvé que le divertissement est plus qu'un numéro — c'est un artisanat. Mariage intime, grand événement d'entreprise ou set de festival dynamique : j'apporte un niveau de professionnalisme et de spectacle qui se remarque. <a href="/fr/contact/">Contactez-moi</a>.</p>
<h3>L'art de l'impossible</h3>
<ul>
<li><strong>Maîtrise du feu :</strong> des flammes de plusieurs mètres et une précision absolue.</li>
<li><strong>Techniques de fakir :</strong> défier le verre et les lits de clous avec un contrôle mental total.</li>
<li><strong>La passion de la perfection :</strong> chaque spectacle est 100 % sûr, professionnel et adapté au lieu.</li>
</ul>
<p>Le divertissement coule dans mes veines. La passion du public et le frisson de l'impossible me poussent à élever sans cesse mes numéros. Réserver Nuno, c'est choisir près de deux décennies d'expérience, de passion et un effet wow garanti.</p>
<h2>Vivez vous-même la puissance du feu et de la magie</h2>
<p>Prêt à hisser votre événement à un niveau inédit ? Que vous souhaitiez un <a href="/fr/spectacle-de-feu/"><strong>spectacle de feu</strong></a> pour une ouverture, un <a href="/fr/spectacle-de-fakir/">numéro de fakir</a> pour une fête à thème ou un <a href="/fr/atelier-cracheur-de-feu/">atelier</a> interactif : je vous aide volontiers à réaliser votre vision.</p>
<p>Créons ensemble quelque chose de légendaire. <a href="/fr/contact/">Demandez un devis gratuit !</a></p>
""",
 "faq": [],
 "service": None,
}

PAGES["fr"]["fotos"] = {
 "title": "Photos des spectacles",
 "seo_title": "Photos | Spectacle de feu, fakir & reptiles | Cracheur de feu Nuno",
 "seo_desc": "Découvrez les photos des spectacles de feu, de fakir, de reptiles et des ateliers de Nuno — festivals, événements d'entreprise et mariages en Belgique et aux Pays-Bas.",
 "eyebrow": "Photos",
 "img": ("/assets/media/festival-1600.webp", "Le cracheur de feu Nuno soufflant une boule de feu au-dessus d'une foule de festival"),
 "intro_html": ('<p>Une sélection des dernières années : spectacles de feu en festival et en '
                'entreprise, spectacles de fakir au théâtre, spectacle de reptiles et prestations '
                'lors de mariages et fêtes à thème. Cliquez sur une photo pour l\'agrandir &mdash; ou '
                '<a href="/fr/contact/">demandez directement un devis</a>.</p>'),
 "captions": {
    "festival":   ("Spectacle de feu complet sur une place de festival", "Le cracheur de feu Nuno soufflant une boule de feu sur une place de festival devant un large public"),
    "vuurbal":    ("Boule de feu lors d'un spectacle nocturne", "Immense boule de feu contre un ciel nocturne noir au-dessus du cracheur de feu"),
    "avondvuur":  ("Boule de feu au crépuscule", "Le cracheur de feu Nuno soufflant une énorme boule de feu au crépuscule"),
    "vuurshow":   ("Spectacle de feu en plein jour lors d'un festival d'été", "Spectacle de feu en plein jour lors d'un festival, le public à quelques mètres"),
    "workshop":   ("Crachage de feu dans le ciel du soir", "Cracheur de feu soufflant une grande boule de feu dans le ciel du soir depuis une balustrade"),
    "schemering": ("Crachage de feu au crépuscule", "Crachage de feu au crépuscule, la flamme s'évasant largement contre un ciel bleu"),
    "themafeest": ("Fête à thème avec feu près du bus vintage", "Cracheur de feu à côté d'un bus vintage lors d'une fête à thème en soirée"),
    "bruiloft":   ("Duo avec danseuse lors d'un mariage", "Duo lors d'un mariage : le cracheur de feu Nuno avec une danseuse aux ailes rouges"),
    "fakirshow":  ("Spectacle de fakir au théâtre", "Spectacle de fakir au théâtre : Nuno sur le lit de clous portant le poids d'un spectateur"),
    "fakir":      ("Numéro de fakir avec verre et poids", "Numéro de fakir : Nuno portant le poids d'un spectateur debout"),
    "spijkerbed": ("La planche à clous de près", "Gros plan du numéro de fakir : Nuno en équilibre avec la planche à clous et des chaînes sur le visage"),
    "reptiel":    ("Spectacle de reptiles avec boa constrictor", "Nuno avec un boa constrictor autour du bras pendant le spectacle de reptiles"),
    "vuurzee":     ("Mer de feu dans la rue animée", "Le cracheur de feu Nuno souffle une immense mer de feu avec pluie d'étincelles dans une rue animée la nuit"),
    "straatfakir": ("Spectacle de fakir dans la rue : le public debout SUR Nuno", "Numéro de fakir dans la rue : deux spectateurs debout sur Nuno allongé sur la planche à clous"),
    "glasact":     ("Numéro de verre brisé au théâtre", "Nuno prend appui les mains dans les tessons de verre pendant un spectacle en salle"),
    "podium":      ("Scène de festival devant des milliers", "Nuno sur la scène du festival, du feu au-dessus d'une foule en liesse"),
    "mentalist":  ("Le mentaliste Nuno au théâtre", "Nuno sur la scène d'un théâtre vide pour un spectacle de mentalisme"),
 },
 "gallery_name": "Photos du cracheur de feu Nuno",
}

PAGES["fr"]["videos"] = {
 "title": "Vidéos des spectacles",
 "seo_title": "Vidéos | Spectacle de feu & fakir en action | Cracheur de feu Nuno",
 "seo_desc": "Regardez les vidéos des spectacles de feu, des numéros de fakir et des prestations de Nuno. Showreels de festivals et d'événements en Belgique et aux Pays-Bas.",
 "eyebrow": "Vidéos",
 "img": ("/assets/media/reel-1-poster.webp", "Le cracheur de feu Nuno pendant un spectacle de feu sur site"),
 "intro_html": ('<p>Spectacles de feu, numéros de fakir et crachage de feu en mouvement : une '
                'sélection des dernières années. Cliquez sur une vidéo pour la lire &mdash; voyez '
                'aussi <a href="/fr/photos/">toutes les photos</a> ou '
                '<a href="/fr/contact/">demandez un devis</a>.</p>'),
 "vid_caps": [
    ("Spectacle de feu sur site", "Le cracheur de feu Nuno pendant un spectacle de feu sur site : crachage de feu, jonglage enflammé et feu corporel."),
    ("Numéros & art du fakir", "Compilation des numéros de feu et de fakir de Nuno en festivals et événements d'entreprise."),
    ("Showreel", "Court showreel du cracheur de feu et fakir Nuno."),
    ("Boule de feu en gros plan", "Immense boule de feu du cracheur de feu Nuno, filmée de près."),
 ],
 "gallery_name": "Vidéos du cracheur de feu Nuno",
}

PAGES["fr"]["contact-3"] = {
 "title": "Travailler avec Nuno ? Vérifiez votre date",
 "seo_title": "\U0001F525 Contact | Réserver le cracheur de feu Nuno — réponse sous 24 h",
 "seo_desc": "Réserver un spectacle de feu, de fakir ou un atelier ? Appelez, envoyez un WhatsApp ou le formulaire avec votre date et lieu. Devis gratuit sous 24 heures.",
 "eyebrow": "Contact",
 "img": ("/assets/media/themafeest-1080.webp", "Cracheur de feu à côté d'un bus vintage lors d'une fête à thème en soirée"),
 "body": """
<p>Travailler avec Nuno ? Qu'il s'agisse d'un <a href="/fr/spectacle-de-feu/">spectacle de feu</a>,
d'un <a href="/fr/spectacle-de-fakir/">spectacle de fakir</a>, d'un
<a href="/fr/atelier-cracheur-de-feu/">atelier cracheur de feu</a> ou d'une
<a href="/fr/halloween/">production Halloween</a> complète : dites-nous brièvement ce que vous
fêtez, où et quand &mdash; et vous saurez <strong>sous 24 heures</strong> si votre date est libre,
avec un devis gratuit sur mesure.</p>
""",
 "contact_labels": {"tel_head": "Téléphone — lun–sam, 9h–18h", "biz": "Fixe / professionnel",
                    "wa": "WhatsApp", "wa_link": "Envoyer un message", "mail": "E-mail",
                    "area": "Zone d'intervention", "area_val": "Belgique, Pays-Bas & international",
                    "note": "Pour une date dans les deux semaines : appeler ou WhatsApp va plus vite que l'e-mail."},
}

PAGES["fr"]["beoordelingen"] = {
 "title": "4,9 sur 136 avis",
 "seo_title": "⭐ Avis Cracheur de Feu Nuno — 4,9/5 sur 136 avis",
 "seo_desc": "Lisez ce que disent les clients de Belgique et des Pays-Bas des spectacles de feu et de fakir de Nuno. Moyenne de 4,9/5 sur 136 avis Google.",
 "eyebrow": "Avis",
 "img": ("/assets/media/festival-1600.webp", "Le cracheur de feu Nuno soufflant une boule de feu au-dessus d'une foule de festival"),
 "texts": {
    "based_on": "sur la base de 136 avis",
    "google_link": "Voir le profil Google ›",
    "intro": "Des clients de toute la Belgique et des Pays-Bas à propos des spectacles de feu, de fakir et des ateliers de Nuno — d'Amsterdam à Anvers et de Groningue à Bruxelles. Les avis ci-dessous sont affichés dans leur langue d'origine.",
    "outro_pre": "Envie de lire tous les avis ? Consultez l'aperçu complet sur ",
    "outro_link": "le profil Google de Nuno",
    "outro_post": ". Envie de vivre la même expérience ? ",
    "outro_cta": "Demandez un devis gratuit",
 },
}

PAGES["fr"][""] = {
 "title": "Cracheur de feu Nuno — spectacles de feu, fakir & ateliers",
 "seo_title": "Cracheur de Feu Nuno | Spectacle de Feu, Fakir & Atelier — Belgique & Pays-Bas",
 "seo_desc": "Engagez le cracheur de feu professionnel Nuno pour votre événement en Belgique ou aux Pays-Bas. Spectacles de feu, fakir, ateliers et animations Halloween. 4,9/5 — devis sous 24 h.",
 "eyebrow": "Cracheur de feu · fakir · mentaliste",
 "img": ("/assets/media/festival-1600.webp", "Le cracheur de feu Nuno soufflant une boule de feu au-dessus d'une foule de festival"),
 "home": {
   "intro": """
<p><strong>Dix-sept ans de feu, à la télévision nationale et sur les scènes de toute l'Europe.</strong>
Nuno est l'un des artistes de feu les plus expérimentés des Pays-Bas et de Belgique — il se produit
régulièrement à Bruxelles, à Liège et dans toute la Wallonie : cracheur de feu, fakir, mentaliste
et artiste de spectacle de reptiles en une seule personne. Certifié, assuré et noté
<a href="/fr/avis/">4,9 sur 5 pour 136 avis Google</a>.</p>
<p>De l'ouverture explosive de cinq minutes à la production complète d'une soirée : chaque
spectacle est du sur-mesure pour votre lieu et votre public — événements d'entreprise, mariages,
festivals et fêtes privées, en intérieur comme en extérieur.</p>
""",
   "shows_head": "Les spectacles",
   "cards": [
     ("vuurspuwer-inhuren", "vuurshow-850.webp", "Spectacle de feu", "Des flammes de plusieurs mètres, du jonglage enflammé et des chorégraphies en musique — la pièce maîtresse de tout événement.", "Spectacle de feu en plein jour lors d'un festival"),
     ("fakir-show-inhuren", "fakirshow-640.webp", "Spectacle de fakir", "Lit de clous, marche sur verre et numéros à l'épée : tension et émerveillement du début à la fin.", "Spectacle de fakir au théâtre : Nuno sur le lit de clous"),
     ("workshop-vuurspuwen", "workshop-900.webp", "Atelier cracheur de feu", "Apprenez vous-même à cracher le feu, en toute sécurité — le team building ultime.", "Cracheur de feu soufflant une grande boule de feu dans le ciel du soir"),
     ("halloween", "vuurbal-900.webp", "\U0001F383 Animations Halloween", "Spectacles de feu diaboliques et fakir d'horreur, connus des Fright Nights de Walibi. Dès 350 €.", "Immense boule de feu contre un ciel nocturne noir"),
     ("fotos", "festival-900.webp", "Photos", "Les spectacles en images : festivals, mariages, événements d'entreprise et théâtre.", "Le cracheur de feu Nuno sur une place de festival"),
     ("videos", "themafeest-900.webp", "Vidéos", "Showreels et extraits des numéros de feu et de fakir en action.", "Cracheur de feu à côté d'un bus vintage"),
   ],
   "why_head": "Pourquoi réserver Nuno ?",
   "why": [
     ("Certifié & assuré", "Entièrement certifié comme cracheur de feu et fakir, avec matériel professionnel, combustibles sûrs et assurance responsabilité civile."),
     ("Vu à la télévision", "SBS6, RTL, VTM, l'émission d'Uri Geller et des productions en Angleterre."),
     ("4,9/5 sur 136 avis", "Des clients de Belgique et des Pays-Bas notent les spectacles au plus haut niveau."),
     ("Sur mesure", "Chaque prestation est adaptée à votre lieu, votre thème et votre public — en intérieur comme en extérieur."),
   ],
   "reviews_head": "Ce que disent les clients",
   "reviews_link": "Lire les 30 avis sélectionnés ›",
   "cta_head": "Vérifiez votre date",
   "cta_text": "Envoyez le formulaire de demande et vous saurez sous 24 heures si votre date est libre — ou appelez / envoyez un WhatsApp pour une réponse immédiate.",
 },
 "faq": [
  ("Où se produit le cracheur de feu Nuno ?",
   "Dans toute la Belgique — Bruxelles, Liège, la Wallonie et la Flandre — et aux Pays-Bas, ainsi qu'à l'international sur demande. Les frais de déplacement figurent dans le devis."),
  ("Combien coûte un spectacle de feu ?",
   "Le prix dépend du type de spectacle, de la durée et du lieu. Demandez un devis gratuit et recevez une proposition sur mesure sous 24 heures."),
  ("Un spectacle de feu en intérieur est-il sûr ?",
   "Oui, à condition que le lieu réponde aux exigences de sécurité (hauteur de plafond, ventilation). Nuno propose des numéros d'intérieur spéciaux avec feu corporel et techniques de fakir."),
  ("Quand faut-il réserver ?",
   "Les dates populaires — week-ends d'été, Halloween, Nouvel An — partent des mois à l'avance. Réserver tôt garantit votre date ; la dernière minute est parfois possible."),
 ],
}

# --------------------------------------------------- regiopagina's DE en FR
# sleutel = NL-stadsslug; volledige eigen inhoud in de streektaal.
REGIO_PAGES = {"de": {}, "fr": {}}

def _de_stad(stad, extra, kenmerk):
    return f"""
<p>Sie planen eine Veranstaltung in <strong>{stad}</strong> und suchen einen Act, der wirklich in Erinnerung bleibt? Feuerspucker Nuno bringt seine spektakuläre Feuershow direkt zu Ihnen — aus dem nahen Zeist (NL) ist er schnell in der Grenzregion, oft sogar kurzfristig.</p>
<h2>Eine Feuershow in {stad}, die niemand vergisst</h2>
<p>{extra} Meterhohe Feuerwolken, Feuerjonglage, Körperfeuer und auf Wunsch Fakir-Elemente wie das Nagelbrett: Nuno stellt für jede Location in {stad} und Umgebung die passende Show zusammen — von der Firmenfeier über die Hochzeit bis zum Stadtfest, drinnen (wo erlaubt) wie draußen.</p>
<h2>Sicher, zertifiziert und professionell</h2>
<p>{kenmerk} Nuno arbeitet mit professionellem Equipment und sicheren Brennstoffen, hält alle Sicherheitsabstände ein und stimmt sich im Vorfeld mit Ihnen und ggf. der Location ab. Mit über 17 Jahren Erfahrung, TV-Auftritten (SBS6, RTL, VTM) und 4,9 von 5 Sternen aus 136 Google-Bewertungen buchen Sie Qualität ohne Risiko.</p>
<h2>Auch buchbar in {stad}</h2>
<ul>
<li><a href="/de/fakirshow/">Fakirshow</a> — Nagelbrett, Glaslaufen und Schwert-Acts</li>
<li><a href="/de/feuerspucker-workshop/">Feuerspucker-Workshop</a> — selbst sicher Feuerspucken lernen</li>
<li><a href="/de/halloween/">Halloween-Acts</a> — teuflische Feuershows und ein Horror-Fakir (ab 350 €)</li>
</ul>
<h2>Jetzt Termin für {stad} sichern</h2>
<p>Fragen Sie unverbindlich an: Sie erhalten <strong>binnen 24 Stunden</strong> Antwort mit einem kostenlosen Angebot nach Maß. <a href="/de/kontakt/">Zum Anfrageformular</a>, telefonisch unter <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> oder per <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
"""

REGIO_PAGES["de"]["spectaculaire-vuurspuwer-aachen-maak-uw-evenement-in-de-keizerstad-onvergetelijk"] = {
 "stad": "Aachen",
 "title": "Feuerspucker in Aachen buchen: Feuershow in der Kaiserstadt",
 "seo_title": "\U0001F525 Feuerspucker Aachen | Feuershow buchen — Angebot binnen 24 h",
 "seo_desc": "Feuerspucker in Aachen buchen? Nuno bringt seine spektakuläre Feuershow in die Kaiserstadt — Firmenfeiern, Hochzeiten und Stadtfeste. Kostenloses Angebot binnen 24 h!",
 "body": _de_stad("Aachen",
    "Ob auf dem Katschhof, in einer Eventlocation am Rand der Altstadt oder bei Ihnen im Garten: Vor der Kulisse der Kaiserstadt wirkt eine Feuershow doppelt magisch.",
    "Gerade in einer historischen Stadt wie Aachen zählt Sicherheit."),
}
REGIO_PAGES["de"]["vuurspuwer-inhuren-in-krefeld-een-vlammend-spektakel-voor-uw-event"] = {
 "stad": "Krefeld",
 "title": "Feuerspucker in Krefeld buchen: ein flammendes Spektakel",
 "seo_title": "\U0001F525 Feuerspucker Krefeld | Feuershow buchen — Angebot binnen 24 h",
 "seo_desc": "Feuerspucker in Krefeld buchen? Nuno liefert ein flammendes Spektakel für Ihr Event in der Samt- und Seidenstadt. Kostenloses Angebot binnen 24 Stunden!",
 "body": _de_stad("Krefeld",
    "Von der Firmenfeier in der Samt- und Seidenstadt bis zum Vereinsfest am Niederrhein: Eine Feuershow verwandelt jeden Abend in ein Ereignis.",
    "Auch bei Wind und Wetter am Niederrhein bleibt die Show kontrolliert und sicher."),
}
REGIO_PAGES["de"]["vuurspuwer-monchengladbach-spectaculaire-vuurshows-net-over-de-grens"] = {
 "stad": "Mönchengladbach",
 "title": "Feuerspucker in Mönchengladbach: spektakuläre Feuershows direkt hinter der Grenze",
 "seo_title": "\U0001F525 Feuerspucker Mönchengladbach | Feuershow buchen",
 "seo_desc": "Feuerspucker in Mönchengladbach buchen? Nuno kommt aus den nahen Niederlanden mit einer spektakulären Feuershow zu Ihrem Event. Kostenloses Angebot binnen 24 h!",
 "body": _de_stad("Mönchengladbach",
    "Von der Vitusstadt bis ins Umland: Nuno ist von der niederländischen Grenze aus in kürzester Zeit bei Ihnen — perfekt auch für spontanere Termine.",
    "Kurze Anfahrt, große Wirkung."),
}
REGIO_PAGES["de"]["vuurspuwer-inhuren-in-kaldenkirchen-spectaculair-entertainment-in-de-grensregio"] = {
 "stad": "Kaldenkirchen",
 "title": "Feuerspucker in Kaldenkirchen: spektakuläres Entertainment in der Grenzregion",
 "seo_title": "\U0001F525 Feuerspucker Kaldenkirchen & Nettetal | Feuershow buchen",
 "seo_desc": "Feuerspucker in Kaldenkirchen oder Nettetal buchen? Nuno wohnt praktisch um die Ecke — spektakuläre Feuershows für Feste in der Grenzregion. Angebot binnen 24 h!",
 "body": _de_stad("Kaldenkirchen",
    "Nettetal, Venlo-Umgebung, der ganze Grenzstrich: Für Nuno ist Kaldenkirchen praktisch um die Ecke — die Anfahrt bleibt klein, das Spektakel groß.",
    "Kurze Wege bedeuten flexible Zeiten und faire Preise."),
}
REGIO_PAGES["de"]["vuurspuwer-inhuren-in-kleve-breng-vurige-magie-naar-de-grensregio"] = {
 "stad": "Kleve",
 "title": "Feuerspucker in Kleve: feurige Magie für die Grenzregion",
 "seo_title": "\U0001F525 Feuerspucker Kleve | Feuershow buchen — Angebot binnen 24 h",
 "seo_desc": "Feuerspucker in Kleve buchen? Nuno bringt feurige Magie in die Schwanenstadt und die gesamte Grenzregion. Kostenloses Angebot binnen 24 Stunden!",
 "body": _de_stad("Kleve",
    "Von der Schwanenburg bis zum Festzelt im Umland: Eine Feuershow gibt jedem Fest in Kleve den magischen Höhepunkt.",
    "Vom Kinderfest bis zur Betriebsfeier wird die Show passend dosiert."),
}

def _fr_stad(stad, extra, kenmerk):
    return f"""
<p>Vous organisez un événement à <strong>{stad}</strong> et cherchez un numéro qui marquera vraiment les esprits ? Le cracheur de feu Nuno apporte son spectacle de feu spectaculaire jusque chez vous — depuis Zeist (Pays-Bas), il rejoint rapidement {stad}, souvent même en dernière minute.</p>
<h2>Un spectacle de feu à {stad} que personne n'oubliera</h2>
<p>{extra} Nuages de feu de plusieurs mètres, jonglage enflammé, feu corporel et, sur demande, des éléments de fakir comme le lit de clous : Nuno compose le spectacle adapté à chaque lieu à {stad} et dans les environs — fête d'entreprise, mariage ou fête de quartier, en intérieur (où c'est autorisé) comme en extérieur.</p>
<h2>Sûr, certifié et professionnel</h2>
<p>{kenmerk} Nuno travaille avec du matériel professionnel et des combustibles sûrs, respecte toutes les distances de sécurité et se concerte en amont avec vous et le lieu. Avec plus de 17 ans d'expérience, des passages télé (SBS6, RTL, VTM) et 4,9/5 sur 136 avis Google, vous réservez la qualité sans risque.</p>
<h2>Également réservable à {stad}</h2>
<ul>
<li><a href="/fr/spectacle-de-fakir/">Spectacle de fakir</a> — lit de clous, marche sur verre et numéros à l'épée</li>
<li><a href="/fr/atelier-cracheur-de-feu/">Atelier cracheur de feu</a> — apprenez vous-même à cracher le feu en toute sécurité</li>
<li><a href="/fr/halloween/">Animations Halloween</a> — spectacles de feu diaboliques et fakir d'horreur (dès 350 €)</li>
</ul>
<h2>Réservez votre date à {stad}</h2>
<p>Demandez sans engagement : vous recevez une réponse <strong>sous 24 heures</strong> avec un devis gratuit sur mesure. <a href="/fr/contact/">Vers le formulaire</a>, par téléphone au <a href="tel:+31620020723">+31&nbsp;6&nbsp;200&nbsp;207&nbsp;23</a> ou via <a href="https://wa.me/31620020723" rel="noopener">WhatsApp</a>.</p>
"""

REGIO_PAGES["fr"]["vuurspuwer-boeken-in-liege"] = {
 "stad": "Liège",
 "title": "Engager un cracheur de feu à Liège : un spectacle de feu inoubliable",
 "seo_title": "\U0001F525 Cracheur de Feu Liège | Réserver un Spectacle de Feu — devis sous 24 h",
 "seo_desc": "Engager un cracheur de feu à Liège ? Nuno apporte son spectacle de feu spectaculaire dans la Cité Ardente — fêtes d'entreprise, mariages et festivals. Devis gratuit sous 24 h !",
 "body": _fr_stad("Liège",
    "De la place Saint-Lambert aux salles des bords de Meuse : dans la Cité Ardente, un spectacle de feu porte doublement bien son nom.",
    "Dans une ville animée comme Liège, la sécurité est primordiale."),
}
REGIO_PAGES["fr"]["vuurspuwer-boeken-in-brussel"] = {
 "stad": "Bruxelles",
 "title": "Engager un cracheur de feu à Bruxelles : le feu au cœur de la capitale",
 "seo_title": "\U0001F525 Cracheur de Feu Bruxelles | Réserver un Spectacle de Feu — devis sous 24 h",
 "seo_desc": "Engager un cracheur de feu à Bruxelles ? Nuno se produit régulièrement dans la capitale — événements d'entreprise, mariages et festivals. Devis gratuit sous 24 heures !",
 "body": _fr_stad("Bruxelles",
    "Rooftop d'entreprise, salle de gala ou jardin privé à Uccle : Nuno se produit régulièrement dans la capitale et connaît les exigences des lieux bruxellois.",
    "Bilingue par nature : la communication se fait sans souci en français, néerlandais ou anglais."),
}

REGIO_IMG = {
 "de": ("/assets/media/avondvuur-1080.webp", "Feuerspucker Nuno bläst einen riesigen Feuerball in der Abenddämmerung"),
 "fr": ("/assets/media/avondvuur-1080.webp", "Le cracheur de feu Nuno soufflant une énorme boule de feu au crépuscule"),
}
REGIO_EYEBROW = {"de": "Feuershow vor Ort", "fr": "Spectacle de feu sur site"}
REGIO_SERVICE = {
 "de": lambda stad: {"name": f"Feuerspucker in {stad} buchen", "type": "Feuershow",
                     "desc": f"Spektakuläre Feuershow von Feuerspucker Nuno in {stad} und Umgebung: Feuerspucken, Feuerjonglage und Fakir-Acts für Firmenfeiern, Hochzeiten und Feste."},
 "fr": lambda stad: {"name": f"Cracheur de feu à {stad}", "type": "Spectacle de feu",
                     "desc": f"Spectacle de feu spectaculaire du cracheur de feu Nuno à {stad} et environs : crachage de feu, jonglage enflammé et numéros de fakir pour entreprises, mariages et fêtes."},
}

UI["nl"]["skip"] = "Naar de inhoud"
UI["en"]["skip"] = "Skip to content"
UI["de"]["skip"] = "Zum Inhalt"
UI["fr"]["skip"] = "Aller au contenu"

# ------------------------- extra regiopagina's zonder NL-tegenhanger
STANDALONE_REGIO = {
 "de": {
  "feuerspucker-duesseldorf": {
   "stad": "Düsseldorf",
   "title": "Feuerspucker in Düsseldorf buchen: Feuershow an Rhein und Kö",
   "seo_title": "\U0001F525 Feuerspucker Düsseldorf | Feuershow buchen — Angebot binnen 24 h",
   "seo_desc": "Feuerspucker in Düsseldorf buchen? Nuno bringt seine spektakuläre Feuershow an den Rhein — Firmenfeiern, Hochzeiten und Events. Kostenloses Angebot binnen 24 h!",
   "body": _de_stad("Düsseldorf",
      "Vom Rheinufer über die Altstadt bis zur Firmenfeier im Medienhafen: Düsseldorf liebt große Auftritte — und eine Feuershow ist der größte.",
      "Auch bei anspruchsvollen Locations am Rhein bleibt alles kontrolliert."),
  },
  "feuerspucker-duisburg": {
   "stad": "Duisburg",
   "title": "Feuerspucker in Duisburg buchen: Feuer im Ruhrgebiet",
   "seo_title": "\U0001F525 Feuerspucker Duisburg | Feuershow buchen — Angebot binnen 24 h",
   "seo_desc": "Feuerspucker in Duisburg buchen? Nuno bringt Feuershows in den Landschaftspark und das ganze westliche Ruhrgebiet. Kostenloses Angebot binnen 24 Stunden!",
   "body": _de_stad("Duisburg",
      "Der Landschaftspark Duisburg-Nord und Industriekulisse überhaupt sind wie gemacht für Feuer — kaum eine Region passt besser zu dieser Show.",
      "Industriegelände, Halle oder Vereinsheim: Die Show wird an den Ort angepasst."),
  },
 },
 "fr": {
  "cracheur-de-feu-namur": {
   "stad": "Namur",
   "title": "Engager un cracheur de feu à Namur : le feu au cœur de la Wallonie",
   "seo_title": "\U0001F525 Cracheur de Feu Namur | Spectacle de Feu en Wallonie — devis sous 24 h",
   "seo_desc": "Engager un cracheur de feu à Namur ? Nuno apporte son spectacle de feu au cœur de la Wallonie — fêtes d'entreprise, mariages et festivals. Devis gratuit sous 24 h !",
   "body": _fr_stad("Namur",
      "De la Citadelle aux bords de Meuse et de Sambre : la capitale wallonne offre des décors magnifiques pour un spectacle de feu.",
      "Capitale de la Wallonie ou village des environs : la show s'adapte au lieu."),
  },
  "cracheur-de-feu-charleroi": {
   "stad": "Charleroi",
   "title": "Engager un cracheur de feu à Charleroi : des flammes au Pays Noir",
   "seo_title": "\U0001F525 Cracheur de Feu Charleroi | Spectacle de Feu — devis sous 24 h",
   "seo_desc": "Engager un cracheur de feu à Charleroi ? Nuno enflamme le Pays Noir — fêtes d'entreprise, festivals et événements privés. Devis gratuit sous 24 heures !",
   "body": _fr_stad("Charleroi",
      "Du centre-ville aux friches industrielles réinventées : le décor du Pays Noir donne au feu une intensité unique.",
      "Sites industriels, salles ou plein air : tout est possible."),
  },
  "cracheur-de-feu-mons": {
   "stad": "Mons",
   "title": "Engager un cracheur de feu à Mons : le feu sur la Grand-Place",
   "seo_title": "\U0001F525 Cracheur de Feu Mons | Spectacle de Feu — devis sous 24 h",
   "seo_desc": "Engager un cracheur de feu à Mons ? Nuno se produit dans tout le Hainaut — fêtes d'entreprise, mariages, festivals et fêtes de ville. Devis gratuit sous 24 h !",
   "body": _fr_stad("Mons",
      "De la Grand-Place au beffroi : la cité du Doudou sait faire la fête, et un spectacle de feu s'y sent chez lui.",
      "Du Doudou aux fêtes privées : l'intensité s'adapte au public."),
  },
 },
}

# ------------------------------------------------------------- prijzenpagina
SLUGS["wat-kost-een-vuurspuwer"] = {"en": "fire-breather-prices",
                                    "de": "feuerspucker-kosten",
                                    "fr": "prix-cracheur-de-feu"}

PAGES["en"]["wat-kost-een-vuurspuwer"] = {
 "title": "How much does a fire breather cost?",
 "seo_title": "\U0001F4B6 Fire Breather Prices 2026 | From €350 — Transparent Packages",
 "seo_desc": "Hire a fire breather from €350. See all prices and packages: from a 10-minute power act to a full festival show (€350–€1500), including travel costs. Transparent and all-in.",
 "eyebrow": "Prices & packages",
 "img": ("/assets/media/avondvuur-1080.webp", "Fire breather Nuno blows an enormous fireball at dusk"),
 "body": """
<p><strong>Hiring fire breather Nuno costs between €350 and €1500, depending on show length and package. This page shows exactly what each show costs, what is included and how travel costs work — transparent, with no surprises.</strong></p>
<h2>Fire show prices 2026: package overview</h2>
<p>Across the market, "fire show" prices range from about €400 to well over €6000, because the term covers everything from a single torch act to full productions. Nuno works with clear packages and a starting price of €350:</p>
<table class="ptable">
<thead><tr><th>Package</th><th>Duration</th><th>Indication</th><th>Perfect for</th></tr></thead>
<tbody>
<tr><td><strong>Power act</strong></td><td>10 min</td><td>from €350</td><td>Opening or grand finale, product launch</td></tr>
<tr><td><strong>Show block</strong></td><td>20 min</td><td>from €450</td><td>Weddings, birthdays, anniversaries, company parties</td></tr>
<tr><td><strong>Full fire show</strong></td><td>30 min</td><td>from €595</td><td>Theme parties and galas, with fakir elements and interaction</td></tr>
<tr><td><strong>Festival package</strong></td><td>up to 5 × 20 min</td><td>€950 – €1500</td><td>Festivals and multi-day events, spread across the day or evening</td></tr>
</tbody>
</table>
<p><em>All amounts are indications excluding travel costs; you always receive a free tailored quote first, with one all-in total price.</em></p>
<h2>What is included?</h2>
<ul>
<li><strong>Everything for the show</strong> — professional equipment, safe show fuels, costumes, set-up and breakdown.</li>
<li><strong>Safety arranged</strong> — Nuno is fully certified and works within permit requirements and prescribed safety distances, coordinated with the venue in advance.</li>
<li><strong>Consultation and customisation</strong> — music, timing and programme are agreed beforehand so the show fits your event seamlessly.</li>
<li><strong>One point of contact</strong> — you book directly with the artist, without agency margins.</li>
</ul>
<h2>Travel costs</h2>
<p>Nuno travels from Zeist (Utrecht region) across the <a href="/en/">Netherlands and Belgium</a>. Travel costs are calculated per kilometre and always stated upfront in the quote — usually €25–€75 within the Netherlands, slightly more for Belgium. Further away or international? Also possible, on request.</p>
<h2>What determines the price?</h2>
<ul>
<li><strong>Duration and number of sets</strong> — one power act costs less than five show blocks on a festival day.</li>
<li><strong>Type of act</strong> — a <a href="/en/fire-show/">fire show</a>, <a href="/en/fakir-show/">fakir show</a> or combination; a mentalism act works indoors where fire is not allowed.</li>
<li><strong>Duo or solo</strong> — performing with a fire dancer makes the show bigger (and the budget slightly larger).</li>
<li><strong>Date and season</strong> — <a href="/en/halloween/">October (Halloween)</a> and December are peak months: booking early pays off.</li>
</ul>
<p>Not sure which package fits? Send your date and location via the <a href="/en/contact/">request form</a> — within 24 hours you will know whether the date is free, with a price proposal. Prefer direct contact? Call or WhatsApp <a href="https://wa.me/31620020723" rel="noopener">+31 6 200 207 23</a>. With <a href="/en/about-nuno/">17 years of experience</a> and <a href="/en/reviews/">4.9/5 from 136 reviews</a>, you know exactly what you are booking.</p>
""",
 "faq": [
  ("How much does a fire breather cost for a wedding or birthday?",
   "The 20-minute show block is the most popular for weddings, birthdays, anniversaries and company parties: from €450 excluding travel costs. A short 10-minute power act starts at €350."),
  ("What does a fire show at a festival cost?",
   "For festivals there is a package of up to five 20-minute sets spread across the day or evening: €950 to €1500 all-in, depending on the number of sets and travel distance."),
  ("Are there any additional costs?",
   "Only travel costs (per kilometre from Zeist, usually €25–€75 within the Netherlands). Equipment, fuels, set-up and coordination with the venue are included. The quote always shows one all-in total."),
  ("Why do fire show prices vary so much online?",
   "The term 'fire show' covers everything from a single artist with a torch to full productions with several performers — hence online prices from €400 to over €6000. Always check what is included; with Nuno it is in writing in the quote."),
  ("Can the show take place indoors, and does that cost extra?",
   "Indoors is possible whenever the venue and fire brigade allow it; otherwise Nuno switches to acts without open fire, such as mentalism or the fakir show. The package price stays the same."),
 ],
 "service": {"name": "Hire a fire breather (prices and packages)", "type": "Fire show",
             "desc": "Book a fire show from 10 minutes to 5×20 minutes: power act, show block for weddings and company parties, full fire show or festival package. Transparent prices from €350 to €1500.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "4",
                        "description": "Four packages: power act 10 min (from €350), show block 20 min (from €450), full show 30 min (from €595), festival package up to 5×20 min (€950–€1500)."}},
}

PAGES["de"]["wat-kost-een-vuurspuwer"] = {
 "title": "Was kostet ein Feuerspucker?",
 "seo_title": "\U0001F4B6 Feuerspucker Kosten 2026 | Ab 350 € — Transparente Pakete",
 "seo_desc": "Feuerspucker buchen ab 350 €. Alle Preise und Pakete: vom 10-Minuten-Power-Act bis zur kompletten Festivalshow (350–1500 €), inklusive Erklärung der Anfahrtskosten.",
 "eyebrow": "Preise & Pakete",
 "img": ("/assets/media/avondvuur-1080.webp", "Feuerspucker Nuno spuckt einen riesigen Feuerball in der Abenddämmerung"),
 "body": """
<p><strong>Einen Feuerspucker zu buchen kostet bei Nuno zwischen 350 und 1500 €, je nach Showdauer und Paket. Auf dieser Seite sehen Sie genau, was jede Show kostet, was enthalten ist und wie die Anfahrt berechnet wird — transparent und ohne Überraschungen.</strong></p>
<h2>Feuershow-Preise 2026: Pakete im Überblick</h2>
<p>Am Markt reichen die Preise für eine „Feuershow“ von etwa 400 bis weit über 6000 €, weil darunter alles verkauft wird — von der einzelnen Fackel bis zur Großproduktion. Nuno arbeitet mit klaren Paketen und einem Ab-Preis von 350 €:</p>
<table class="ptable">
<thead><tr><th>Paket</th><th>Dauer</th><th>Richtwert</th><th>Perfekt für</th></tr></thead>
<tbody>
<tr><td><strong>Power-Act</strong></td><td>10 Min</td><td>ab 350 €</td><td>Eröffnung oder großes Finale, Produktlaunch</td></tr>
<tr><td><strong>Showblock</strong></td><td>20 Min</td><td>ab 450 €</td><td>Hochzeiten, Geburtstage, Jubiläen, Firmenfeiern</td></tr>
<tr><td><strong>Komplette Feuershow</strong></td><td>30 Min</td><td>ab 595 €</td><td>Mottopartys und Galas, mit Fakir-Elementen und Interaktion</td></tr>
<tr><td><strong>Festivalpaket</strong></td><td>bis 5 × 20 Min</td><td>950 – 1500 €</td><td>Festivals und mehrtägige Events, über den Tag oder Abend verteilt</td></tr>
</tbody>
</table>
<p><em>Alle Beträge sind Richtwerte zzgl. Anfahrt; Sie erhalten immer zuerst ein kostenloses Angebot mit einem All-in-Gesamtpreis.</em></p>
<h2>Was ist im Preis enthalten?</h2>
<ul>
<li><strong>Alles für die Show</strong> — professionelles Material, sichere Showbrennstoffe, Kostüme, Auf- und Abbau.</li>
<li><strong>Sicherheit geregelt</strong> — Nuno arbeitet voll zertifiziert, innerhalb der Genehmigungsauflagen und mit den vorgeschriebenen Sicherheitsabständen.</li>
<li><strong>Abstimmung und Maßarbeit</strong> — Musik, Timing und Programm werden vorab abgestimmt.</li>
<li><strong>Ein Ansprechpartner</strong> — Sie buchen direkt beim Künstler, ohne Agenturmargen.</li>
</ul>
<h2>Anfahrtskosten</h2>
<p>Nuno reist von Zeist (Region Utrecht) nach <a href="/de/">NRW und in die gesamte Grenzregion</a>. Die Anfahrt wird pro Kilometer berechnet und steht immer vorab im Angebot — für NRW meist zwischen 50 und 100 €. Weiter weg? Auf Anfrage ebenfalls möglich.</p>
<h2>Wovon hängt der Preis ab?</h2>
<ul>
<li><strong>Dauer und Anzahl der Auftritte</strong> — ein Power-Act kostet weniger als fünf Showblöcke an einem Festivaltag.</li>
<li><strong>Art des Acts</strong> — eine <a href="/de/feuershow/">Feuershow</a>, <a href="/de/fakirshow/">Fakirshow</a> oder Kombination; Mentalismus funktioniert auch drinnen, wo Feuer nicht erlaubt ist.</li>
<li><strong>Duo oder solo</strong> — mit Feuertänzerin wird die Show größer.</li>
<li><strong>Termin und Saison</strong> — <a href="/de/halloween/">Oktober (Halloween)</a> und Dezember sind Spitzenmonate: früh buchen lohnt sich.</li>
</ul>
<p>Unsicher, welches Paket passt? Senden Sie Datum und Ort über das <a href="/de/kontakt/">Anfrageformular</a> — innerhalb von 24 Stunden wissen Sie, ob der Termin frei ist, inklusive Preisvorschlag. Mit <a href="/de/ueber-nuno/">17 Jahren Erfahrung</a> und <a href="/de/bewertungen/">4,9/5 aus 136 Bewertungen</a> wissen Sie genau, wen Sie buchen.</p>
""",
 "faq": [
  ("Was kostet ein Feuerspucker für eine Hochzeit oder einen Geburtstag?",
   "Der 20-Minuten-Showblock ist für Hochzeiten, Geburtstage, Jubiläen und Firmenfeiern am beliebtesten: ab 450 € zzgl. Anfahrt. Ein kurzer Power-Act von 10 Minuten beginnt bei 350 €."),
  ("Was kostet eine Feuershow auf einem Festival?",
   "Für Festivals gibt es ein Paket mit bis zu fünf Auftritten à 20 Minuten, über den Tag oder Abend verteilt: 950 bis 1500 € all-in, je nach Anzahl der Sets und Anfahrt."),
  ("Gibt es zusätzliche Kosten?",
   "Nur die Anfahrt (pro Kilometer ab Zeist, für NRW meist 50–100 €). Material, Brennstoffe, Auf- und Abbau und die Abstimmung mit der Location sind enthalten. Das Angebot zeigt immer einen All-in-Gesamtpreis."),
  ("Warum schwanken Feuershow-Preise online so stark?",
   "Unter „Feuershow“ wird alles verkauft — vom einzelnen Künstler mit Fackel bis zur Großproduktion; daher Preise von 400 bis über 6000 €. Prüfen Sie immer, was enthalten ist; bei Nuno steht es schwarz auf weiß im Angebot."),
  ("Kann die Show auch drinnen stattfinden, und kostet das extra?",
   "Drinnen geht, sobald Location und Feuerwehr es erlauben; andernfalls wechselt Nuno zu Acts ohne offenes Feuer wie Mentalismus oder Fakirshow. Am Paketpreis ändert das nichts."),
 ],
 "service": {"name": "Feuerspucker buchen (Preise und Pakete)", "type": "Feuershow",
             "desc": "Feuershow buchen von 10 Minuten bis 5×20 Minuten: Power-Act, Showblock für Hochzeiten und Firmenfeiern, komplette Feuershow oder Festivalpaket. Transparente Preise von 350 bis 1500 €.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "4",
                        "description": "Vier Pakete: Power-Act 10 Min (ab 350 €), Showblock 20 Min (ab 450 €), komplette Show 30 Min (ab 595 €), Festivalpaket bis 5×20 Min (950–1500 €)."}},
}

PAGES["fr"]["wat-kost-een-vuurspuwer"] = {
 "title": "Combien coûte un cracheur de feu ?",
 "seo_title": "\U0001F4B6 Prix Cracheur de Feu 2026 | Dès 350 € — Forfaits Transparents",
 "seo_desc": "Réserver un cracheur de feu dès 350 €. Tous les prix et forfaits : du power act de 10 minutes au spectacle complet de festival (350–1500 €), frais de déplacement expliqués.",
 "eyebrow": "Prix & forfaits",
 "img": ("/assets/media/avondvuur-1080.webp", "Le cracheur de feu Nuno souffle une énorme boule de feu au crépuscule"),
 "body": """
<p><strong>Réserver le cracheur de feu Nuno coûte entre 350 et 1500 €, selon la durée du spectacle et le forfait. Cette page montre exactement le prix de chaque spectacle, ce qui est inclus et comment fonctionnent les frais de déplacement — en toute transparence.</strong></p>
<h2>Prix des spectacles de feu 2026 : les forfaits</h2>
<p>Sur le marché, les prix d'un « spectacle de feu » vont d'environ 400 à plus de 6000 €, car ce terme recouvre tout — d'une simple torche à une production complète. Nuno travaille avec des forfaits clairs et un prix de départ de 350 € :</p>
<table class="ptable">
<thead><tr><th>Forfait</th><th>Durée</th><th>Indication</th><th>Parfait pour</th></tr></thead>
<tbody>
<tr><td><strong>Power act</strong></td><td>10 min</td><td>dès 350 €</td><td>Ouverture ou grand final, lancement de produit</td></tr>
<tr><td><strong>Bloc spectacle</strong></td><td>20 min</td><td>dès 450 €</td><td>Mariages, anniversaires, jubilés, fêtes d'entreprise</td></tr>
<tr><td><strong>Spectacle complet</strong></td><td>30 min</td><td>dès 595 €</td><td>Fêtes à thème et galas, avec éléments de fakir et interaction</td></tr>
<tr><td><strong>Forfait festival</strong></td><td>jusqu'à 5 × 20 min</td><td>950 – 1500 €</td><td>Festivals et événements sur plusieurs jours, répartis sur la journée ou la soirée</td></tr>
</tbody>
</table>
<p><em>Tous les montants sont indicatifs, hors frais de déplacement ; vous recevez toujours d'abord un devis gratuit sur mesure avec un prix total tout compris.</em></p>
<h2>Qu'est-ce qui est inclus ?</h2>
<ul>
<li><strong>Tout pour le spectacle</strong> — matériel professionnel, combustibles sûrs, costumes, montage et démontage.</li>
<li><strong>Sécurité assurée</strong> — Nuno est entièrement certifié et respecte les autorisations et distances de sécurité, en concertation avec le lieu.</li>
<li><strong>Concertation et sur-mesure</strong> — musique, timing et programme sont convenus à l'avance.</li>
<li><strong>Un seul interlocuteur</strong> — vous réservez directement auprès de l'artiste, sans marge d'agence.</li>
</ul>
<h2>Frais de déplacement</h2>
<p>Nuno se déplace depuis Zeist (région d'Utrecht) dans <a href="/fr/">toute la Belgique et les Pays-Bas</a>. Les frais sont calculés au kilomètre et toujours indiqués à l'avance dans le devis — pour la Belgique généralement entre 50 et 100 €.</p>
<h2>De quoi dépend le prix ?</h2>
<ul>
<li><strong>Durée et nombre de passages</strong> — un power act coûte moins que cinq blocs sur une journée de festival.</li>
<li><strong>Type de numéro</strong> — un <a href="/fr/spectacle-de-feu/">spectacle de feu</a>, un <a href="/fr/spectacle-de-fakir/">spectacle de fakir</a> ou une combinaison ; le mentalisme fonctionne aussi en intérieur.</li>
<li><strong>Duo ou solo</strong> — avec une danseuse de feu, le spectacle prend de l'ampleur.</li>
<li><strong>Date et saison</strong> — <a href="/fr/halloween/">octobre (Halloween)</a> et décembre sont les mois de pointe : réservez tôt.</li>
</ul>
<p>Vous hésitez sur le forfait ? Envoyez votre date et lieu via le <a href="/fr/contact/">formulaire</a> — sous 24 heures vous saurez si la date est libre, avec une proposition de prix. Avec <a href="/fr/a-propos-de-nuno/">17 ans d'expérience</a> et <a href="/fr/avis/">4,9/5 sur 136 avis</a>, vous savez exactement qui vous réservez.</p>
""",
 "faq": [
  ("Combien coûte un cracheur de feu pour un mariage ou un anniversaire ?",
   "Le bloc spectacle de 20 minutes est le plus populaire pour les mariages, anniversaires, jubilés et fêtes d'entreprise : dès 450 € hors déplacement. Un power act de 10 minutes commence à 350 €."),
  ("Combien coûte un spectacle de feu en festival ?",
   "Pour les festivals, il existe un forfait jusqu'à cinq passages de 20 minutes répartis sur la journée ou la soirée : 950 à 1500 € tout compris, selon le nombre de sets et la distance."),
  ("Y a-t-il des frais supplémentaires ?",
   "Uniquement les frais de déplacement (au kilomètre depuis Zeist, généralement 50–100 € pour la Belgique). Matériel, combustibles, montage et concertation avec le lieu sont inclus. Le devis affiche toujours un total tout compris."),
  ("Pourquoi les prix des spectacles de feu varient-ils autant en ligne ?",
   "Sous « spectacle de feu » on vend de tout — d'un artiste seul avec une torche à une production complète ; d'où des prix de 400 à plus de 6000 €. Vérifiez toujours ce qui est inclus ; chez Nuno, c'est écrit noir sur blanc dans le devis."),
  ("Le spectacle peut-il avoir lieu en intérieur, et cela coûte-t-il plus cher ?",
   "En intérieur, c'est possible dès que le lieu et les pompiers l'autorisent ; sinon Nuno passe à des numéros sans flamme comme le mentalisme ou le fakir. Le prix du forfait ne change pas."),
 ],
 "service": {"name": "Réserver un cracheur de feu (prix et forfaits)", "type": "Spectacle de feu",
             "desc": "Réservez un spectacle de feu de 10 minutes à 5×20 minutes : power act, bloc spectacle pour mariages et fêtes d'entreprise, spectacle complet ou forfait festival. Prix transparents de 350 à 1500 €.",
             "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                        "lowPrice": "350", "highPrice": "1500", "offerCount": "4",
                        "description": "Quatre forfaits : power act 10 min (dès 350 €), bloc 20 min (dès 450 €), spectacle complet 30 min (dès 595 €), forfait festival jusqu'à 5×20 min (950–1500 €)."}},
}
