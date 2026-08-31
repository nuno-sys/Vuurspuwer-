"""Het Vuur-woordenboek: één kennisbank-pagina per taal die alle termen
uit de vuur- en fakirwereld uitlegt, met DefinedTerm-schema zodat Google
en AI-zoekers elke definitie los kunnen oppakken.

Links in definities staan als [[nl-slug|ankertekst]] en worden per taal
naar de juiste vertaalde pagina herschreven."""
import re
import i18n as I

SITE = "https://vuurspuwer.com"

SLUGS = {"vuur-woordenboek": {"en": "fire-glossary", "de": "feuer-glossar",
                              "fr": "glossaire-du-feu"}}

META = {
 "nl": {
  "title": "Vuur-woordenboek: alle termen uit de vuurshow-wereld uitgelegd",
  "seo_title": "📖 Vuur-woordenboek | Alle Vuurshow-termen Uitgelegd",
  "seo_desc": "📖 Wat is poi? Wat doet een fakir? Vuurhappen of vuurspuwen? Alle termen uit de vuurshow-wereld uitgelegd door vuurspuwer Nuno ★ 4,9/5 ✓ Hét naslagwerk van NL & BE.",
  "eyebrow": "📖 Kennisbank",
  "kw": "vuur woordenboek, vuurshow termen, wat is poi, wat is een fakir, vuurspuwen betekenis, vuurhappen, body fire, vuurstaf, fakirshow uitleg",
  "set_name": "Vuur-woordenboek van Vuurspuwer Nuno",
  "intro": ("<p>Wat is het verschil tussen <strong>vuurhappen en vuurspuwen</strong>? "
            "Wat doet een <strong>fakir</strong> precies, en wat zijn <strong>poi</strong>? "
            "In dit woordenboek legt vuurspuwer en fakir Nuno — met [[over-nuno|17 jaar podiumervaring]] — "
            "alle termen uit de vuur- en showwereld uit. Handig als je een [[vuurspuwer-inhuren|vuurshow wilt boeken]] "
            "en precies wilt weten wat er op jouw feest te zien is, of als je gewoon nieuwsgierig bent "
            "naar dit eeuwenoude vak.</p>"),
  "groups": [("Vuurtechnieken van A tot Z",
              ["vuurspuwen", "vuurhappen", "poi", "vuurstaf", "vuurwaaiers",
               "vuurketting", "vuurjongleren", "bodyfire"]),
             ("Fakir, mentalisme en meer",
              ["fakir", "spijkerbed", "glaslopen", "mentalisme", "reptielenshow"]),
             ("Productie en veiligheid",
              ["vuurshow", "kevlar", "showbrandstof", "veiligheidsafstand",
               "workshop", "pyro"])],
 },
 "en": {
  "title": "Fire glossary: every term from the fire show world explained",
  "seo_title": "📖 Fire Glossary | Every Fire Show Term Explained",
  "seo_desc": "📖 What is poi? What does a fakir do? Fire eating or fire breathing? Every fire show term explained by fire breather Nuno ★ 4.9/5 ✓ The reference for NL & BE.",
  "eyebrow": "📖 Knowledge base",
  "kw": "fire glossary, fire show terms, what is poi, what is a fakir, fire breathing meaning, fire eating, body fire, fire staff, fakir show explained",
  "set_name": "Fire glossary by fire breather Nuno",
  "intro": ("<p>What is the difference between <strong>fire eating and fire breathing</strong>? "
            "What exactly does a <strong>fakir</strong> do, and what are <strong>poi</strong>? "
            "In this glossary, fire breather and fakir Nuno — with [[over-nuno|17 years of stage experience]] — "
            "explains every term from the world of fire and performance. Useful when you want to "
            "[[vuurspuwer-inhuren|book a fire show]] and know exactly what your guests will see, "
            "or when you are simply curious about this age-old craft.</p>"),
  "groups": [("Fire techniques from A to Z",
              ["vuurspuwen", "vuurhappen", "poi", "vuurstaf", "vuurwaaiers",
               "vuurketting", "vuurjongleren", "bodyfire"]),
             ("Fakir, mentalism and more",
              ["fakir", "spijkerbed", "glaslopen", "mentalisme", "reptielenshow"]),
             ("Production and safety",
              ["vuurshow", "kevlar", "showbrandstof", "veiligheidsafstand",
               "workshop", "pyro"])],
 },
 "de": {
  "title": "Feuer-Glossar: alle Begriffe aus der Feuershow-Welt erklärt",
  "seo_title": "📖 Feuer-Glossar | Alle Feuershow-Begriffe erklärt",
  "seo_desc": "📖 Was ist Poi? Was macht ein Fakir? Feuerschlucken oder Feuerspucken? Alle Begriffe der Feuershow-Welt, erklärt von Feuerspucker Nuno ★ 4,9/5 ✓ Das Nachschlagewerk.",
  "eyebrow": "📖 Wissensbasis",
  "kw": "Feuer Glossar, Feuershow Begriffe, was ist Poi, was ist ein Fakir, Feuerspucken Bedeutung, Feuerschlucken, Body Fire, Feuerstab, Fakirshow erklärt",
  "set_name": "Feuer-Glossar von Feuerspucker Nuno",
  "intro": ("<p>Was ist der Unterschied zwischen <strong>Feuerschlucken und Feuerspucken</strong>? "
            "Was genau macht ein <strong>Fakir</strong>, und was sind <strong>Poi</strong>? "
            "In diesem Glossar erklärt Feuerspucker und Fakir Nuno — mit [[over-nuno|17 Jahren Bühnenerfahrung]] — "
            "alle Begriffe aus der Welt des Feuers. Praktisch, wenn Sie eine "
            "[[vuurspuwer-inhuren|Feuershow buchen]] möchten und genau wissen wollen, was Ihre Gäste "
            "erwartet — oder wenn Sie einfach neugierig auf dieses uralte Handwerk sind.</p>"),
  "groups": [("Feuertechniken von A bis Z",
              ["vuurspuwen", "vuurhappen", "poi", "vuurstaf", "vuurwaaiers",
               "vuurketting", "vuurjongleren", "bodyfire"]),
             ("Fakir, Mentalismus und mehr",
              ["fakir", "spijkerbed", "glaslopen", "mentalisme", "reptielenshow"]),
             ("Produktion und Sicherheit",
              ["vuurshow", "kevlar", "showbrandstof", "veiligheidsafstand",
               "workshop", "pyro"])],
 },
 "fr": {
  "title": "Glossaire du feu : tous les termes du spectacle de feu expliqués",
  "seo_title": "📖 Glossaire du Feu | Tous les Termes de Spectacle Expliqués",
  "seo_desc": "📖 C'est quoi le poi ? Que fait un fakir ? Mangeur ou cracheur de feu ? Tous les termes du spectacle de feu expliqués par Nuno ★ 4,9/5 ✓ La référence NL & BE.",
  "eyebrow": "📖 Base de connaissances",
  "kw": "glossaire du feu, termes spectacle de feu, c'est quoi le poi, qu'est-ce qu'un fakir, cracheur de feu signification, mangeur de feu, body fire, bâton de feu",
  "set_name": "Glossaire du feu du cracheur de feu Nuno",
  "intro": ("<p>Quelle est la différence entre <strong>manger le feu et cracher le feu</strong> ? "
            "Que fait exactement un <strong>fakir</strong>, et que sont les <strong>poi</strong> ? "
            "Dans ce glossaire, le cracheur de feu et fakir Nuno — fort de [[over-nuno|17 ans d'expérience scénique]] — "
            "explique tous les termes du monde du feu. Utile si vous voulez "
            "[[vuurspuwer-inhuren|réserver un spectacle de feu]] et savoir exactement ce que vos invités "
            "verront — ou si ce métier ancestral vous intrigue tout simplement.</p>"),
  "groups": [("Techniques de feu de A à Z",
              ["vuurspuwen", "vuurhappen", "poi", "vuurstaf", "vuurwaaiers",
               "vuurketting", "vuurjongleren", "bodyfire"]),
             ("Fakir, mentalisme et plus",
              ["fakir", "spijkerbed", "glaslopen", "mentalisme", "reptielenshow"]),
             ("Production et sécurité",
              ["vuurshow", "kevlar", "showbrandstof", "veiligheidsafstand",
               "workshop", "pyro"])],
 },
}

# tid -> {lang: (emoji, naam, definitie)}
TERMS = {
 "vuurspuwen": {
  "nl": ("🔥", "Vuurspuwen (fire breathing)",
   "Bij vuurspuwen verstuift de artiest een fijne nevel brandstof over een brandende fakkel, waardoor een metershoge vuurbal ontstaat. Het is de meest spectaculaire techniek uit de [[vuurspuwer-inhuren|vuurshow]] — en een van de gevaarlijkste, die jarenlange training in ademtechniek, windinschatting en brandstofkeuze vereist. Vaak de grote finale van een optreden."),
  "en": ("🔥", "Fire breathing",
   "In fire breathing, the performer sprays a fine mist of fuel across a burning torch, creating a towering fireball. It is the most spectacular technique in a [[vuurspuwer-inhuren|fire show]] — and one of the most dangerous, requiring years of training in breath control, reading the wind and choosing the right fuel. Often the grand finale of a performance."),
  "de": ("🔥", "Feuerspucken (fire breathing)",
   "Beim Feuerspucken zerstäubt der Artist einen feinen Brennstoffnebel über eine brennende Fackel, wodurch ein meterhoher Feuerball entsteht. Es ist die spektakulärste Technik der [[vuurspuwer-inhuren|Feuershow]] — und eine der gefährlichsten, die jahrelanges Training in Atemtechnik, Windeinschätzung und Brennstoffwahl erfordert. Oft das große Finale eines Auftritts."),
  "fr": ("🔥", "Cracher le feu (fire breathing)",
   "En crachant le feu, l'artiste pulvérise une fine brume de combustible sur une torche enflammée, créant une immense boule de feu. C'est la technique la plus spectaculaire du [[vuurspuwer-inhuren|spectacle de feu]] — et l'une des plus dangereuses, exigeant des années d'entraînement au souffle, à la lecture du vent et au choix du combustible. Souvent le grand final d'une prestation.")},
 "vuurhappen": {
  "nl": ("👄", "Vuurhappen (fire eating)",
   "Bij vuurhappen dooft de artiest brandende fakkels in de mond: door de vlam de zuurstof te ontnemen gaat hij uit. Het wordt vaak verward met vuurspuwen, maar is precies het omgekeerde — vuurhappen dóóft vuur, vuurspuwen creëert het. Een serene, spannende act die het publiek van dichtbij kan volgen."),
  "en": ("👄", "Fire eating",
   "In fire eating, the performer extinguishes burning torches in the mouth: by cutting off the flame's oxygen, it goes out. It is often confused with fire breathing, but is exactly the opposite — fire eating extinguishes fire, fire breathing creates it. A serene, thrilling act the audience can watch up close."),
  "de": ("👄", "Feuerschlucken (fire eating)",
   "Beim Feuerschlucken löscht der Artist brennende Fackeln im Mund: Der Flamme wird der Sauerstoff entzogen, sodass sie erlischt. Es wird oft mit Feuerspucken verwechselt, ist aber genau das Gegenteil — Feuerschlucken löscht Feuer, Feuerspucken erzeugt es. Ein ruhiger, spannender Act, den das Publikum aus nächster Nähe verfolgen kann."),
  "fr": ("👄", "Manger le feu (fire eating)",
   "Le mangeur de feu éteint des torches enflammées dans sa bouche : privée d'oxygène, la flamme s'éteint. On le confond souvent avec le cracheur de feu, mais c'est exactement l'inverse — manger le feu l'éteint, le cracher le crée. Un numéro serein et captivant que le public peut suivre de très près.")},
 "poi": {
  "nl": ("🌀", "Poi",
   "Poi zijn twee gewichten aan kettingen of koorden die de artiest in cirkelende patronen om het lichaam slingert. De techniek komt oorspronkelijk van de Māori uit Nieuw-Zeeland; met brandende kevlar-lonten worden het hypnotiserende vuurcirkels. Een vast onderdeel van vrijwel elke professionele [[vuurspuwer-inhuren|vuurshow]]."),
  "en": ("🌀", "Poi",
   "Poi are two weights on chains or cords that the performer swings around the body in circular patterns. The technique originates from the Māori of New Zealand; with burning kevlar wicks they become hypnotic circles of fire. A staple of virtually every professional [[vuurspuwer-inhuren|fire show]]."),
  "de": ("🌀", "Poi",
   "Poi sind zwei Gewichte an Ketten oder Schnüren, die der Artist in kreisenden Mustern um den Körper schwingt. Die Technik stammt ursprünglich von den Māori aus Neuseeland; mit brennenden Kevlar-Dochten werden daraus hypnotisierende Feuerkreise. Fester Bestandteil fast jeder professionellen [[vuurspuwer-inhuren|Feuershow]]."),
  "fr": ("🌀", "Poi",
   "Les poi sont deux poids fixés à des chaînes ou cordes que l'artiste fait tournoyer autour du corps en motifs circulaires. La technique vient des Māori de Nouvelle-Zélande ; avec des mèches en kevlar enflammées, ils deviennent des cercles de feu hypnotiques. Un incontournable de presque tout [[vuurspuwer-inhuren|spectacle de feu]] professionnel.")},
 "vuurstaf": {
  "nl": ("🪄", "Vuurstaf (fire staff)",
   "Een staf met kevlar-wieken aan beide uiteinden. De artiest draait, gooit en rolt de staf over het lichaam ('contact staff'), waardoor doorlopende vuurlijnen ontstaan. Grote, vloeiende bewegingen die ook op afstand — bijvoorbeeld op een festivalpodium — prachtig zichtbaar zijn."),
  "en": ("🪄", "Fire staff",
   "A staff with kevlar wicks at both ends. The performer spins, throws and rolls the staff across the body ('contact staff'), creating continuous lines of fire. Large, flowing movements that read beautifully even from a distance — on a festival stage, for example."),
  "de": ("🪄", "Feuerstab (fire staff)",
   "Ein Stab mit Kevlar-Dochten an beiden Enden. Der Artist dreht, wirft und rollt den Stab über den Körper ('Contact Staff'), wodurch durchgehende Feuerlinien entstehen. Große, fließende Bewegungen, die auch aus der Ferne — etwa auf einer Festivalbühne — wunderschön wirken."),
  "fr": ("🪄", "Bâton de feu (fire staff)",
   "Un bâton muni de mèches en kevlar aux deux extrémités. L'artiste le fait tourner, le lance et le fait rouler sur le corps (« contact staff »), créant des lignes de feu continues. De grands mouvements fluides, magnifiques même de loin — sur une scène de festival par exemple.")},
 "vuurwaaiers": {
  "nl": ("🪭", "Vuurwaaiers (fire fans)",
   "Metalen waaiers met meerdere vlammen tegelijk, vaak gebruikt in danschoreografieën. Ze geven een elegante, bijna theatrale uitstraling — populair bij [[vuurshow-bruiloft|bruiloften]] en stijlvolle bedrijfsevents, waar sfeer belangrijker is dan spektakel alleen."),
  "en": ("🪭", "Fire fans",
   "Metal fans carrying several flames at once, often used in dance choreography. They create an elegant, almost theatrical look — popular at [[vuurshow-bruiloft|weddings]] and stylish corporate events, where atmosphere matters as much as spectacle."),
  "de": ("🪭", "Feuerfächer (fire fans)",
   "Metallfächer mit mehreren Flammen gleichzeitig, oft in Tanzchoreografien eingesetzt. Sie wirken elegant, fast theatralisch — beliebt bei [[vuurshow-bruiloft|Hochzeiten]] und stilvollen Firmenevents, wo Atmosphäre genauso zählt wie Spektakel."),
  "fr": ("🪭", "Éventails de feu (fire fans)",
   "Des éventails métalliques portant plusieurs flammes à la fois, souvent utilisés dans des chorégraphies dansées. Ils donnent un rendu élégant, presque théâtral — populaires aux [[vuurshow-bruiloft|mariages]] et aux événements d'entreprise raffinés, où l'ambiance compte autant que le spectacle.")},
 "vuurketting": {
  "nl": ("⛓️", "Vuurketting (fire chains)",
   "Kettingen met brandende kevlar-uiteinden, verwant aan poi maar langer en rauwer in beweging. De artiest laat ze zoevend om zich heen cirkelen; het metaal gloeit mee in het donker. Een techniek die kracht en controle combineert."),
  "en": ("⛓️", "Fire chains",
   "Chains with burning kevlar ends, related to poi but longer and rawer in movement. The performer sends them whirring in circles; the metal glows along in the dark. A technique that combines power with control."),
  "de": ("⛓️", "Feuerkette (fire chains)",
   "Ketten mit brennenden Kevlar-Enden, verwandt mit Poi, aber länger und roher in der Bewegung. Der Artist lässt sie surrend um sich kreisen; das Metall glüht im Dunkeln mit. Eine Technik, die Kraft und Kontrolle vereint."),
  "fr": ("⛓️", "Chaînes de feu (fire chains)",
   "Des chaînes aux extrémités en kevlar enflammées, proches des poi mais plus longues et plus brutes dans le mouvement. L'artiste les fait siffler en cercles autour de lui ; le métal rougeoie dans l'obscurité. Une technique qui allie puissance et contrôle.")},
 "vuurjongleren": {
  "nl": ("🤹", "Vuurjongleren",
   "Jongleren met brandende fakkels: dezelfde precisie als gewoon jongleren, maar elke misvangst telt. Vaak het interactieve, luchtige deel van een show — met vaart, humor en publiekscontact tussen de grotere vuuracts door."),
  "en": ("🤹", "Fire juggling",
   "Juggling with burning torches: the same precision as regular juggling, except every missed catch counts. Often the interactive, light-hearted part of a show — bringing pace, humour and audience contact between the bigger fire acts."),
  "de": ("🤹", "Feuerjonglage",
   "Jonglieren mit brennenden Fackeln: dieselbe Präzision wie beim normalen Jonglieren, nur zählt hier jeder Fehlgriff. Oft der interaktive, leichte Teil einer Show — mit Tempo, Humor und Publikumskontakt zwischen den größeren Feuer-Acts."),
  "fr": ("🤹", "Jonglerie enflammée",
   "Jongler avec des torches enflammées : la même précision que la jonglerie classique, sauf que chaque rattrapage manqué compte. Souvent la partie interactive et légère d'un spectacle — rythme, humour et contact avec le public entre les grands numéros de feu.")},
 "bodyfire": {
  "nl": ("💪", "Body fire",
   "Bij body fire laat de artiest vlammen kortstondig over de eigen huid lopen — armen, handen of tong. Het geheim zit in timing en techniek: de vlam beweegt continu en raakt de huid maar een fractie van een seconde. Alleen voor professionals; het staat garant voor ingehouden adem bij het publiek."),
  "en": ("💪", "Body fire",
   "In body fire, the performer lets flames travel briefly across the skin — arms, hands or tongue. The secret is timing and technique: the flame keeps moving and touches the skin for only a fraction of a second. Strictly for professionals; guaranteed to make the audience hold its breath."),
  "de": ("💪", "Body Fire",
   "Beim Body Fire lässt der Artist Flammen kurz über die eigene Haut laufen — Arme, Hände oder Zunge. Das Geheimnis liegt in Timing und Technik: Die Flamme bewegt sich ständig und berührt die Haut nur für den Bruchteil einer Sekunde. Nur für Profis — und garantiert für angehaltenen Atem im Publikum."),
  "fr": ("💪", "Body fire",
   "Avec le body fire, l'artiste laisse des flammes parcourir brièvement sa propre peau — bras, mains ou langue. Le secret : le timing et la technique, la flamme restant en mouvement et ne touchant la peau qu'une fraction de seconde. Réservé aux professionnels ; souffle coupé garanti dans le public.")},
 "fakir": {
  "nl": ("🎩", "Fakir",
   "Van het Arabische <em>faqīr</em> ('arme'); oorspronkelijk een rondtrekkende asceet, in de showwereld een artiest die extreme lichaamsbeheersing toont: het spijkerbed, glas lopen, gewichten dragen. Nuno combineert deze klassieke acts met vuur in zijn [[fakir-show-inhuren|fakirshow]] — spanning die je van dichtbij voelt."),
  "en": ("🎩", "Fakir",
   "From the Arabic <em>faqīr</em> ('poor one'); originally a wandering ascetic, in show business a performer demonstrating extreme body control: the bed of nails, glass walking, bearing weights. Nuno combines these classic acts with fire in his [[fakir-show-inhuren|fakir show]] — tension you can feel up close."),
  "de": ("🎩", "Fakir",
   "Vom arabischen <em>faqīr</em> („Armer“); ursprünglich ein umherziehender Asket, in der Showwelt ein Artist, der extreme Körperbeherrschung zeigt: Nagelbrett, Glaslaufen, Gewichte tragen. Nuno kombiniert diese klassischen Acts in seiner [[fakir-show-inhuren|Fakirshow]] mit Feuer — Spannung, die man aus nächster Nähe spürt."),
  "fr": ("🎩", "Fakir",
   "De l'arabe <em>faqīr</em> (« pauvre ») ; à l'origine un ascète itinérant, dans le monde du spectacle un artiste démontrant une maîtrise extrême du corps : planche à clous, marche sur verre, port de poids. Nuno combine ces numéros classiques avec le feu dans son [[fakir-show-inhuren|spectacle de fakir]] — une tension palpable de tout près.")},
 "spijkerbed": {
  "nl": ("🛏️", "Spijkerbed (bed of nails)",
   "Honderden spijkers waarover het lichaamsgewicht zich verdeelt: hoe meer punten, hoe minder druk per spijker — pure natuurkunde, maar het blijft indrukwekkend om te zien, zeker wanneer er ook nog een toeschouwer óp de fakir gaat staan. Het icoon van elke [[fakir-show-inhuren|fakirshow]]."),
  "en": ("🛏️", "Bed of nails",
   "Hundreds of nails across which the body weight is distributed: the more points, the less pressure per nail — pure physics, yet it remains striking to watch, especially when a spectator stands on top of the fakir. The icon of every [[fakir-show-inhuren|fakir show]]."),
  "de": ("🛏️", "Nagelbrett (bed of nails)",
   "Hunderte Nägel, über die sich das Körpergewicht verteilt: je mehr Punkte, desto weniger Druck pro Nagel — reine Physik, und doch beeindruckend anzusehen, besonders wenn sich zusätzlich ein Zuschauer auf den Fakir stellt. Das Wahrzeichen jeder [[fakir-show-inhuren|Fakirshow]]."),
  "fr": ("🛏️", "Planche à clous (bed of nails)",
   "Des centaines de clous sur lesquels le poids du corps se répartit : plus il y a de pointes, moins il y a de pression par clou — de la physique pure, mais toujours impressionnante à voir, surtout quand un spectateur monte sur le fakir. L'emblème de tout [[fakir-show-inhuren|spectacle de fakir]].")},
 "glaslopen": {
  "nl": ("🦶", "Glas lopen",
   "Blootsvoets over een bak glasscherven. De techniek draait om gewichtsverdeling, voetplaatsing en het lezen van de scherven — plus absoluut vertrouwen in de eigen voorbereiding. Een van de oudste fakirtradities, die het publiek stiller krijgt dan welke vuurbal ook."),
  "en": ("🦶", "Glass walking",
   "Barefoot across a bed of broken glass. The technique is about weight distribution, foot placement and reading the shards — plus absolute trust in one's own preparation. One of the oldest fakir traditions, and it silences an audience like no fireball can."),
  "de": ("🦶", "Glaslaufen",
   "Barfuß über ein Bett aus Glasscherben. Die Technik lebt von Gewichtsverteilung, Fußplatzierung und dem Lesen der Scherben — plus absolutem Vertrauen in die eigene Vorbereitung. Eine der ältesten Fakirtraditionen, die das Publikum stiller macht als jeder Feuerball."),
  "fr": ("🦶", "Marche sur verre",
   "Pieds nus sur un lit de tessons de verre. La technique repose sur la répartition du poids, le placement des pieds et la lecture des éclats — plus une confiance absolue dans sa préparation. L'une des plus anciennes traditions de fakir, qui fait taire un public mieux que n'importe quelle boule de feu.")},
 "mentalisme": {
  "nl": ("🧠", "Mentalisme",
   "Psychologische illusies: gedachten 'lezen', beslissingen sturen en voorspellingen die uitkomen. Geen bovennatuurlijke krachten, wel scherpe observatie, suggestie en jarenlange oefening. Omdat er geen vlam aan te pas komt, is mentalisme overal binnen inzetbaar — ideaal voor zalen waar vuur niet mag."),
  "en": ("🧠", "Mentalism",
   "Psychological illusions: 'reading' minds, steering decisions and predictions that come true. No supernatural powers — just sharp observation, suggestion and years of practice. Since no flame is involved, mentalism works in any indoor venue — ideal where fire is not allowed."),
  "de": ("🧠", "Mentalismus",
   "Psychologische Illusionen: Gedanken „lesen“, Entscheidungen lenken und Vorhersagen, die eintreffen. Keine übernatürlichen Kräfte, sondern scharfe Beobachtung, Suggestion und jahrelange Übung. Da keine Flamme im Spiel ist, funktioniert Mentalismus in jedem Innenraum — ideal, wo Feuer nicht erlaubt ist."),
  "fr": ("🧠", "Mentalisme",
   "Des illusions psychologiques : « lire » les pensées, orienter les décisions, des prédictions qui se réalisent. Aucun pouvoir surnaturel — de l'observation aiguisée, de la suggestion et des années de pratique. Sans flamme, le mentalisme s'invite dans n'importe quelle salle — idéal là où le feu est interdit.")},
 "reptielenshow": {
  "nl": ("🐍", "Reptielenshow",
   "Een educatieve, veilig begeleide ontmoeting met exotische slangen en reptielen, waarbij het publiek de dieren van dichtbij ziet — en soms mag aanraken. Perfect als publiekstrekker voor familiedagen, winkelcentra en themafeesten, en volledig zonder vuur."),
  "en": ("🐍", "Reptile show",
   "An educational, safely supervised encounter with exotic snakes and reptiles, where the audience sees the animals up close — and sometimes gets to touch them. Perfect as a crowd-puller for family days, shopping centres and theme parties, and entirely without fire."),
  "de": ("🐍", "Reptilienshow",
   "Eine lehrreiche, sicher begleitete Begegnung mit exotischen Schlangen und Reptilien, bei der das Publikum die Tiere aus nächster Nähe sieht — und manchmal berühren darf. Perfekt als Publikumsmagnet für Familientage, Einkaufszentren und Mottopartys, ganz ohne Feuer."),
  "fr": ("🐍", "Spectacle de reptiles",
   "Une rencontre éducative et encadrée en toute sécurité avec des serpents et reptiles exotiques, où le public voit les animaux de très près — et peut parfois les toucher. Parfait pour attirer les foules aux journées familiales, centres commerciaux et soirées à thème, entièrement sans feu.")},
 "vuurshow": {
  "nl": ("🎪", "Vuurshow (fire performance)",
   "De overkoepelende term: een gechoreografeerd optreden waarin technieken als vuurspuwen, poi, staf en body fire samenkomen op muziek. Een professionele [[vuurspuwer-inhuren|vuurshow]] duurt 10 tot 20 minuten per set en wordt opgebouwd naar één grote climax — bekijk ook [[wat-kost-een-vuurspuwer|wat een vuurshow kost]]."),
  "en": ("🎪", "Fire show (fire performance)",
   "The umbrella term: a choreographed performance in which techniques such as fire breathing, poi, staff and body fire come together to music. A professional [[vuurspuwer-inhuren|fire show]] lasts 10 to 20 minutes per set and builds towards one grand climax — see also [[wat-kost-een-vuurspuwer|what a fire show costs]]."),
  "de": ("🎪", "Feuershow (fire performance)",
   "Der Oberbegriff: ein choreografierter Auftritt, in dem Techniken wie Feuerspucken, Poi, Stab und Body Fire zur Musik zusammenkommen. Eine professionelle [[vuurspuwer-inhuren|Feuershow]] dauert 10 bis 20 Minuten pro Set und baut auf einen großen Höhepunkt hin — siehe auch [[wat-kost-een-vuurspuwer|was eine Feuershow kostet]]."),
  "fr": ("🎪", "Spectacle de feu (fire performance)",
   "Le terme générique : une prestation chorégraphiée où crachage de feu, poi, bâton et body fire se rejoignent en musique. Un [[vuurspuwer-inhuren|spectacle de feu]] professionnel dure 10 à 20 minutes par set et monte vers un grand final — voir aussi [[wat-kost-een-vuurspuwer|le prix d'un spectacle de feu]].")},
 "kevlar": {
  "nl": ("🧵", "Kevlar",
   "De hittebestendige aramidevezel waarvan de lonten van vrijwel alle vuurattributen zijn gemaakt. Kevlar zuigt de brandstof op en houdt de vlam vast zonder zelf snel te verbranden — de reden dat poi, staf en waaiers optreden na optreden meegaan."),
  "en": ("🧵", "Kevlar",
   "The heat-resistant aramid fibre from which the wicks of virtually all fire props are made. Kevlar soaks up the fuel and holds the flame without burning away itself — the reason poi, staffs and fans last performance after performance."),
  "de": ("🧵", "Kevlar",
   "Die hitzebeständige Aramidfaser, aus der die Dochte fast aller Feuerrequisiten bestehen. Kevlar saugt den Brennstoff auf und hält die Flamme, ohne selbst schnell zu verbrennen — der Grund, warum Poi, Stab und Fächer Auftritt für Auftritt halten."),
  "fr": ("🧵", "Kevlar",
   "La fibre aramide résistante à la chaleur dont sont faites les mèches de presque tous les accessoires de feu. Le kevlar absorbe le combustible et retient la flamme sans se consumer rapidement — la raison pour laquelle poi, bâtons et éventails durent spectacle après spectacle.")},
 "showbrandstof": {
  "nl": ("⛽", "Showbrandstof",
   "Professionele artiesten werken uitsluitend met speciale showbrandstoffen met een gecontroleerd vlampunt — nooit met benzine of spiritus. De juiste brandstof bepaalt de kleur, temperatuur en voorspelbaarheid van de vlam, en is de basis van elke veilige show. Ook in de [[workshop-vuurspuwen|workshop vuurspuwen]] leer je hier alles over."),
  "en": ("⛽", "Show fuel",
   "Professional performers work exclusively with special show fuels with a controlled flash point — never with petrol or methylated spirits. The right fuel determines the colour, temperature and predictability of the flame, and is the basis of every safe show. You learn all about it in the [[workshop-vuurspuwen|fire-breathing workshop]] too."),
  "de": ("⛽", "Show-Brennstoff",
   "Professionelle Artisten arbeiten ausschließlich mit speziellen Show-Brennstoffen mit kontrolliertem Flammpunkt — nie mit Benzin oder Spiritus. Der richtige Brennstoff bestimmt Farbe, Temperatur und Berechenbarkeit der Flamme und ist die Basis jeder sicheren Show. Auch im [[workshop-vuurspuwen|Workshop Feuerspucken]] lernen Sie alles darüber."),
  "fr": ("⛽", "Combustible de spectacle",
   "Les artistes professionnels travaillent exclusivement avec des combustibles de spectacle au point d'éclair contrôlé — jamais avec de l'essence ou de l'alcool à brûler. Le bon combustible détermine la couleur, la température et la prévisibilité de la flamme, et fonde la sécurité de chaque spectacle. On apprend tout cela aussi à l'[[workshop-vuurspuwen|atelier cracheur de feu]].")},
 "veiligheidsafstand": {
  "nl": ("📏", "Veiligheidsafstand",
   "De voorgeschreven vrije ruimte tussen artiest, publiek, bebouwing en aankleding. Hoeveel afstand nodig is hangt af van de acts en de wind; een professional stemt dit vooraf af met de locatie en — bij grotere evenementen — met gemeente of brandweer. Bij het [[contact-3|boeken]] wordt dit altijd voor je geregeld."),
  "en": ("📏", "Safety distance",
   "The prescribed clear space between performer, audience, buildings and decoration. How much distance is needed depends on the acts and the wind; a professional coordinates this in advance with the venue and — at larger events — with the municipality or fire brigade. When you [[contact-3|book]], this is always arranged for you."),
  "de": ("📏", "Sicherheitsabstand",
   "Der vorgeschriebene Freiraum zwischen Artist, Publikum, Bebauung und Dekoration. Wie viel Abstand nötig ist, hängt von den Acts und dem Wind ab; ein Profi stimmt das vorab mit der Location und — bei größeren Events — mit Gemeinde oder Feuerwehr ab. Bei der [[contact-3|Buchung]] wird das immer für Sie geregelt."),
  "fr": ("📏", "Distance de sécurité",
   "L'espace libre réglementaire entre l'artiste, le public, les bâtiments et la décoration. La distance nécessaire dépend des numéros et du vent ; un professionnel la coordonne à l'avance avec le lieu et — pour les grands événements — avec la commune ou les pompiers. Lors de la [[contact-3|réservation]], tout cela est réglé pour vous.")},
 "workshop": {
  "nl": ("💨", "Workshop vuurspuwen",
   "Zelf leren vuurspuwen onder begeleiding van een professional: eerst techniek en veiligheid, daarna pas echt vuur. Een populaire teambuilding- en vrijgezellenactiviteit — na afloop heeft iedereen zijn eigen vuurbal geblazen. Lees alles over de [[workshop-vuurspuwen|workshop vuurspuwen]]."),
  "en": ("💨", "Fire-breathing workshop",
   "Learning to breathe fire yourself under professional guidance: technique and safety first, real fire only after that. A popular team-building and bachelor-party activity — by the end, everyone has blown their own fireball. Read all about the [[workshop-vuurspuwen|fire-breathing workshop]]."),
  "de": ("💨", "Workshop Feuerspucken",
   "Selbst Feuerspucken lernen unter professioneller Anleitung: erst Technik und Sicherheit, dann erst echtes Feuer. Eine beliebte Teambuilding- und Junggesellen-Aktivität — am Ende hat jeder seinen eigenen Feuerball geblasen. Alles über den [[workshop-vuurspuwen|Workshop Feuerspucken]]."),
  "fr": ("💨", "Atelier cracheur de feu",
   "Apprendre soi-même à cracher le feu sous supervision professionnelle : d'abord la technique et la sécurité, ensuite seulement le vrai feu. Une activité de team building et d'enterrement de vie de célibataire très populaire — à la fin, chacun a soufflé sa propre boule de feu. Tout sur l'[[workshop-vuurspuwen|atelier cracheur de feu]].")},
 "pyro": {
  "nl": ("🎆", "Pyrotechniek vs. vuurshow",
   "Pyrotechniek is vuurwerk en technische effecten: aan strenge regels en vergunningen gebonden en op steeds meer plekken beperkt. Een vuurshow is een artiest met levende vlam — persoonlijker, flexibeler en op veel locaties wél mogelijk waar vuurwerk dat niet is. Daarom kiezen steeds meer organisatoren een [[vuurwerk-alternatief|vuurshow als vuurwerk-alternatief]]."),
  "en": ("🎆", "Pyrotechnics vs. fire show",
   "Pyrotechnics means fireworks and technical effects: bound by strict rules and permits, and restricted in more and more places. A fire show is an artist with a living flame — more personal, more flexible, and possible at many venues where fireworks are not. That is why more and more organisers choose a [[vuurwerk-alternatief|fire show as a fireworks alternative]]."),
  "de": ("🎆", "Pyrotechnik vs. Feuershow",
   "Pyrotechnik bedeutet Feuerwerk und technische Effekte: an strenge Regeln und Genehmigungen gebunden und an immer mehr Orten eingeschränkt. Eine Feuershow ist ein Artist mit lebendiger Flamme — persönlicher, flexibler und an vielen Orten möglich, wo Feuerwerk es nicht ist. Deshalb wählen immer mehr Veranstalter eine [[vuurwerk-alternatief|Feuershow als Feuerwerk-Alternative]]."),
  "fr": ("🎆", "Pyrotechnie vs. spectacle de feu",
   "La pyrotechnie, ce sont les feux d'artifice et effets techniques : soumise à des règles et autorisations strictes, et limitée dans de plus en plus d'endroits. Un spectacle de feu, c'est un artiste avec une flamme vivante — plus personnel, plus flexible, et possible dans bien des lieux où les feux d'artifice ne le sont pas. C'est pourquoi de plus en plus d'organisateurs choisissent un [[vuurwerk-alternatief|spectacle de feu comme alternative au feu d'artifice]].")},
}

def _links(txt, lang):
    return re.sub(r"\[\[([a-z0-9-]+)\|([^\]]+)\]\]",
                  lambda m: f'<a href="{I.url_of(lang, m.group(1))}">{m.group(2)}</a>',
                  txt)

def build(lang):
    """(body-html, DefinedTermSet-schema) voor één taal."""
    M = META[lang]
    slug = "vuur-woordenboek" if lang == "nl" else f'{lang}/{SLUGS["vuur-woordenboek"][lang]}'
    url = f"{SITE}/{slug}/"
    set_id = url + "#woordenboek"
    parts = [_links(M["intro"], lang)]
    terms_ld = []
    # de foto- en videostrip komen tússen de groepen, nooit in de kaarten-grid
    strip_after = {0: "<!--STRIP1-->", 1: "<!--STRIP2-->"}
    for gi, (h2, tids) in enumerate(M["groups"]):
        parts.append(f"<h2>{h2}</h2>")
        parts.append('<div class="gloss">')
        for tid in tids:
            emoji, naam, defi = TERMS[tid][lang]
            parts.append(
                f'<section class="gloss__item" id="{tid}">'
                f'<h3 class="gloss__t">{emoji} {naam}</h3>'
                f"<p>{_links(defi, lang)}</p></section>")
            plain = re.sub(r"<[^>]+>", "", re.sub(r"\[\[[a-z0-9-]+\|([^\]]+)\]\]", r"\1", defi))
            terms_ld.append({"@type": "DefinedTerm", "@id": f"{url}#{tid}",
                             "name": re.sub(r"\s*\([^)]*\)$", "", naam),
                             "description": plain,
                             "url": f"{url}#{tid}",
                             "inDefinedTermSet": {"@id": set_id}})
        parts.append("</div>")
        if gi in strip_after:
            parts.append(strip_after[gi])
    ld = {"@context": "https://schema.org", "@type": "DefinedTermSet",
          "@id": set_id, "name": M["set_name"], "url": url,
          "inLanguage": I.HTML_LANG[lang],
          "about": {"@id": f"{SITE}/#business"},
          "hasDefinedTerm": terms_ld}
    return "\n".join(parts), ld
