"""De reptielenshow in het Engels, Duits en Frans.

De Nederlandse pagina /reptielenhow/ haalde in de Search Console-export over
zes maanden 17 klikken op 419 vertoningen (positie 9,3) en de oude Duitse
versie /de/Reptilienshow/ zelfs 10,3% doorklik op positie 11,4 — de hoogste
van de hele site. Die Duitse pagina was in september meegegaan in de
samenvoeging naar /de/feuershow/, wat de zoekvraag niet beantwoordt.
Hier staat hij terug, samen met een Engelse en Franse versie, want dit is een
echte act van Nuno en geen stadspagina: hij hoort in alle vier de talen.
"""

SLUGS = {
    "reptielenhow": {"en": "reptile-show", "de": "reptilienshow",
                     "fr": "spectacle-de-reptiles"},
}

_FOTOS = {
    "en": [("reptiel-900.webp", "reptiel-960.webp", 900, 838,
            "Reptile show with a boa constrictor",
            "Nuno with a boa constrictor around his arm during the reptile show"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124,
            "Fakir act with glass and weight",
            "Fakir act: Nuno bearing the weight of a standing spectator")],
    "de": [("reptiel-900.webp", "reptiel-960.webp", 900, 838,
            "Reptilienshow mit Boa constrictor",
            "Nuno mit einer Boa constrictor um den Arm während der Reptilienshow"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124,
            "Fakir-Akt mit Glas und Gewicht",
            "Fakir-Akt: Nuno trägt das Gewicht eines stehenden Zuschauers")],
    "fr": [("reptiel-900.webp", "reptiel-960.webp", 900, 838,
            "Spectacle de reptiles avec un boa constrictor",
            "Nuno avec un boa constrictor autour du bras pendant le spectacle de reptiles"),
           ("fakir-900.webp", "fakir-1080.webp", 900, 1124,
            "Numéro de fakir avec verre et poids",
            "Numéro de fakir : Nuno supporte le poids d'un spectateur debout")],
}

EN = {"reptielenhow": {
 "title": "Reptile show: meet a boa constrictor up close",
 "seo_title": "\U0001F40D Book a Reptile Show – Snakes & Tarantulas | Nuno",
 "seo_desc": "Book a reptile show with snakes, tarantulas and other reptiles. An indoor act with no open fire, safe for all ages. Quote within 24 hours.",
 "eyebrow": "Reptile show",
 "img": ("/assets/media/reptiel-900.webp",
         "Nuno with a boa constrictor around his arm during the reptile show"),
 "body": """
<p><strong>A reptile show brings animals most guests have only ever seen behind glass right into the room. Snakes, tarantulas and other reptiles, introduced one by one, with every guest free to come as close as they dare. No open fire, so it works indoors — in halls, restaurants, museums and offices where a fire show is not allowed.</strong></p>
<h2>What happens during a reptile show</h2>
<p>Nuno moves through the room with the animals rather than performing on a stage. Each animal is introduced: what it is, where it lives, how it moves, what is true about it and what is myth. Guests who want to can touch or hold an animal; guests who would rather watch from a distance simply watch. That choice is the heart of the act — the people who are most afraid at the start are often the ones holding a snake by the end of the evening.</p>
<h2>Which animals come along</h2>
<p>Several species of snake, tarantulas and other reptiles. Which animals travel to your event depends on your audience and the venue: the selection for a children's party is different from the one for a corporate evening. Nuno discusses this with you beforehand.</p>
<h2>Safety</h2>
<p>Everything happens under the supervision of an experienced handler. Touching and holding is always voluntary, never a surprise. The animals travel in their own transport boxes and are only out of them during the act. The show suits all ages.</p>
<h2>Indoors, and in any season</h2>
<p>The reptile show is an indoor act by nature. It needs no outdoor space, no clearance height and no fire safety zone, which makes it the obvious choice when the venue rules out open fire, or when the weather does. It also runs just as well in winter as in summer.</p>
<h2>Combining it with the fire show</h2>
<p>A popular pairing: the reptile show as a walkabout among the guests during the reception or dinner, and the <a href="/en/fire-show/">fire show</a> outside to close the evening. That way there is something happening all night. A <a href="/en/fakir-show/">fakir show</a> or mentalism can slot in between.</p>
<h2>Booking a reptile show</h2>
<p>A reptile show costs between €350 and €1500, depending on the length and the number of blocks. Travel and materials are included. Send your date and location through the <a href="/en/contact/">contact form</a> and you will have a quote within 24 hours. Nuno performs across the Netherlands, Belgium and the German border region.</p>
""",
 "faq": [("Which animals come to the reptile show?",
          "Several species of snake, tarantulas and other reptiles. Exactly which animals come along depends on your audience and the venue; the selection for a children's party differs from the one for a corporate event."),
         ("Is the reptile show safe, also for children?",
          "Yes. Everything happens under the supervision of an experienced handler. Touching and holding is always voluntary — guests who are nervous at first are often the last to give it a try anyway. The show suits all ages."),
         ("What does a reptile show cost?",
          "A reptile show costs between €350 and €1500, depending on the length and the number of blocks. Travel and materials are included. Request a quote and you will have a price within 24 hours."),
         ("Can the reptile show be held indoors?",
          "Yes, it is an indoor act by nature. There is no open fire, so it works in halls, restaurants, museums and offices where a fire show is not permitted."),
         ("Can the reptile show be combined with a fire show?",
          "Certainly, and it is a popular combination. The reptile show works well as a walkabout among the guests, after which the fire show closes the evening outside.")],
 "service": {"name": "Reptile show", "type": "Educational Reptile Show",
             "desc": "Educational and interactive reptile show with snakes, tarantulas and other reptiles. An indoor act without open fire, suitable for all ages."},
 "fotos": _FOTOS["en"],
}}

DE = {"reptielenhow": {
 "title": "Reptilienshow: einer Boa constrictor ganz nah",
 "seo_title": "\U0001F40D Reptilienshow buchen – Schlangen & Vogelspinnen | Nuno",
 "seo_desc": "Reptilienshow buchen mit Schlangen, Vogelspinnen und anderen Reptilien. Indoor-Act ohne offenes Feuer, sicher für jedes Alter. Angebot binnen 24 Stunden.",
 "eyebrow": "Reptilienshow",
 "img": ("/assets/media/reptiel-900.webp",
         "Nuno mit einer Boa constrictor um den Arm während der Reptilienshow"),
 "body": """
<p><strong>Eine Reptilienshow bringt Tiere in den Raum, die die meisten Gäste nur hinter Glas kennen. Schlangen, Vogelspinnen und andere Reptilien, eines nach dem anderen vorgestellt, und jeder Gäst darf so nah herankommen, wie er möchte. Kein offenes Feuer, also auch drinnen möglich — in Sälen, Restaurants, Museen und Büros, in denen eine Feuershow nicht erlaubt ist.</strong></p>
<h2>Was bei einer Reptilienshow passiert</h2>
<p>Nuno geht mit den Tieren durch den Raum, statt auf einer Bühne zu stehen. Jedes Tier wird vorgestellt: was es ist, wo es lebt, wie es sich bewegt, was stimmt und was Legende ist. Wer möchte, darf ein Tier anfassen oder halten; wer lieber aus der Entfernung zusieht, sieht zu. Genau diese Wahl macht den Act aus — wer am Anfang am meisten Respekt hat, hält am Ende des Abends oft als Letzter doch eine Schlange in der Hand.</p>
<h2>Welche Tiere mitkommen</h2>
<p>Mehrere Schlangenarten, Vogelspinnen und weitere Reptilien. Welche Tiere mitreisen, hängt vom Publikum und vom Ort ab: Für einen Kindergeburtstag ist die Auswahl eine andere als für eine Firmenfeier. Nuno bespricht das vorab mit Ihnen.</p>
<h2>Sicherheit</h2>
<p>Alles geschieht unter Aufsicht eines erfahrenen Profis. Anfassen und Halten ist immer freiwillig und nie eine Überraschung. Die Tiere reisen in eigenen Transportboxen und sind nur während des Acts draußen. Die Show ist für jedes Alter geeignet.</p>
<h2>Drinnen — und zu jeder Jahreszeit</h2>
<p>Die Reptilienshow ist von Natur aus ein Indoor-Act. Sie braucht keinen Außenbereich, keine freie Höhe und keine Sicherheitszone für Feuer. Damit ist sie die naheliegende Wahl, wenn die Location offenes Feuer ausschließt — oder das Wetter. Im Winter funktioniert sie genauso gut wie im Sommer.</p>
<h2>Kombination mit der Feuershow</h2>
<p>Eine beliebte Kombination: die Reptilienshow als Walkact zwischen den Gästen beim Empfang oder Essen, danach die <a href="/de/feuershow/">Feuershow</a> draußen zum Abschluss. So ist den ganzen Abend etwas los. Eine <a href="/de/fakirshow/">Fakirshow</a> oder Mentalismus passt gut dazwischen.</p>
<h2>Reptilienshow buchen</h2>
<p>Eine Reptilienshow kostet zwischen 350 € und 1500 €, je nach Dauer und Anzahl der Blöcke. Anfahrt und Material sind enthalten. Schicken Sie Datum und Ort über das <a href="/de/kontakt/">Kontaktformular</a>, und Sie haben binnen 24 Stunden ein Angebot. Nuno tritt in den Niederlanden, Belgien und der deutschen Grenzregion auf — unter anderem in <a href="/de/feuerspucker-aachen/">Aachen</a>, <a href="/de/feuerspucker-krefeld/">Krefeld</a> und <a href="/de/feuerspucker-moenchengladbach/">Mönchengladbach</a>.</p>
""",
 "faq": [("Welche Tiere kommen zur Reptilienshow mit?",
          "Mehrere Schlangenarten, Vogelspinnen und weitere Reptilien. Welche Tiere genau mitkommen, hängt vom Publikum und vom Ort ab; für einen Kindergeburtstag ist die Auswahl eine andere als für eine Firmenfeier."),
         ("Ist die Reptilienshow sicher, auch für Kinder?",
          "Ja. Alles geschieht unter Aufsicht eines erfahrenen Profis. Anfassen und Halten ist immer freiwillig — gerade Gäste, die anfangs Respekt haben, trauen sich am Ende oft doch. Die Show ist für jedes Alter geeignet."),
         ("Was kostet eine Reptilienshow?",
          "Eine Reptilienshow kostet zwischen 350 € und 1500 €, je nach Dauer und Anzahl der Blöcke. Anfahrt und Material sind im Preis enthalten. Fordern Sie ein Angebot an und Sie haben binnen 24 Stunden einen Preis."),
         ("Kann die Reptilienshow drinnen stattfinden?",
          "Ja, sie ist von Natur aus ein Indoor-Act. Es gibt kein offenes Feuer, also funktioniert sie in Sälen, Restaurants, Museen und Büros, in denen eine Feuershow nicht erlaubt ist."),
         ("Lässt sich die Reptilienshow mit einer Feuershow kombinieren?",
          "Ja, und das ist eine beliebte Kombination. Die Reptilienshow funktioniert gut als Walkact zwischen den Gästen, danach schließt die Feuershow den Abend draußen ab.")],
 "service": {"name": "Reptilienshow", "type": "Educational Reptile Show",
             "desc": "Lehrreiche und interaktive Reptilienshow mit Schlangen, Vogelspinnen und anderen Reptilien. Indoor-Act ohne offenes Feuer, für jedes Alter geeignet."},
 "fotos": _FOTOS["de"],
}}

FR = {"reptielenhow": {
 "title": "Spectacle de reptiles : un boa constrictor à portée de main",
 "seo_title": "\U0001F40D Réserver un spectacle de reptiles – serpents & mygales | Nuno",
 "seo_desc": "Réservez un spectacle de reptiles avec serpents, mygales et autres reptiles. Numéro d'intérieur sans feu, sûr à tout âge. Devis sous 24 heures.",
 "eyebrow": "Spectacle de reptiles",
 "img": ("/assets/media/reptiel-900.webp",
         "Nuno avec un boa constrictor autour du bras pendant le spectacle de reptiles"),
 "body": """
<p><strong>Un spectacle de reptiles fait entrer dans la salle des animaux que la plupart des invités n'ont jamais vus autrement que derrière une vitre. Serpents, mygales et autres reptiles, présentés un par un, chacun s'approchant autant qu'il le souhaite. Pas de feu, donc possible en intérieur — dans les salles, les restaurants, les musées et les bureaux où un spectacle de feu est interdit.</strong></p>
<h2>Comment se déroule un spectacle de reptiles</h2>
<p>Nuno circule dans la salle avec les animaux plutôt que de jouer sur une scène. Chaque animal est présenté : ce qu'il est, où il vit, comment il se déplace, ce qui est vrai et ce qui relève de la légende. Qui le souhaite peut toucher ou tenir un animal ; qui préfère regarder de loin regarde de loin. C'est ce choix qui fait tout le numéro — ceux qui hésitent le plus au début sont souvent les derniers à tenir un serpent en fin de soirée.</p>
<h2>Quels animaux se déplacent</h2>
<p>Plusieurs espèces de serpents, des mygales et d'autres reptiles. Le choix dépend du public et du lieu : la sélection pour un anniversaire d'enfant n'est pas celle d'une soirée d'entreprise. Nuno en discute avec vous à l'avance.</p>
<h2>Sécurité</h2>
<p>Tout se passe sous la supervision d'un professionnel expérimenté. Toucher et tenir reste toujours volontaire, jamais une surprise. Les animaux voyagent dans leurs propres caisses de transport et n'en sortent que pendant le numéro. Le spectacle convient à tous les âges.</p>
<h2>En intérieur, et en toute saison</h2>
<p>Le spectacle de reptiles est par nature un numéro d'intérieur. Il ne demande ni espace extérieur, ni hauteur libre, ni zone de sécurité pour le feu. C'est donc le choix évident quand le lieu exclut le feu — ou quand la météo s'en charge. Il fonctionne aussi bien en hiver qu'en été.</p>
<h2>En combinaison avec le spectacle de feu</h2>
<p>Une combinaison appréciée : le spectacle de reptiles en déambulation parmi les invités pendant l'accueil ou le repas, puis le <a href="/fr/spectacle-de-feu/">spectacle de feu</a> dehors pour clôturer la soirée. Il se passe ainsi quelque chose toute la soirée. Un <a href="/fr/spectacle-de-fakir/">spectacle de fakir</a> ou du mentalisme peut s'intercaler.</p>
<h2>Réserver un spectacle de reptiles</h2>
<p>Un spectacle de reptiles coûte entre 350 € et 1500 € selon la durée et le nombre de blocs. Déplacement et matériel sont compris. Envoyez votre date et votre lieu via le <a href="/fr/contact/">formulaire de contact</a> et vous recevrez un devis sous 24 heures. Nuno se déplace aux Pays-Bas, en Belgique — dont <a href="/fr/cracheur-de-feu-liege/">Liège</a>, <a href="/fr/cracheur-de-feu-bruxelles/">Bruxelles</a> et <a href="/fr/cracheur-de-feu-namur/">Namur</a> — et au Luxembourg.</p>
""",
 "faq": [("Quels animaux viennent au spectacle de reptiles ?",
          "Plusieurs espèces de serpents, des mygales et d'autres reptiles. Le choix exact dépend du public et du lieu ; la sélection pour un anniversaire d'enfant n'est pas celle d'une soirée d'entreprise."),
         ("Le spectacle de reptiles est-il sûr, même pour les enfants ?",
          "Oui. Tout se passe sous la supervision d'un professionnel expérimenté. Toucher et tenir reste toujours volontaire — ceux qui hésitent au début sont souvent les derniers à se lancer. Le spectacle convient à tous les âges."),
         ("Combien coûte un spectacle de reptiles ?",
          "Un spectacle de reptiles coûte entre 350 € et 1500 € selon la durée et le nombre de blocs. Déplacement et matériel sont compris. Demandez un devis et vous aurez un prix sous 24 heures."),
         ("Le spectacle de reptiles peut-il avoir lieu en intérieur ?",
          "Oui, c'est par nature un numéro d'intérieur. Il n'y a pas de feu, il fonctionne donc dans les salles, les restaurants, les musées et les bureaux où un spectacle de feu est interdit."),
         ("Peut-on combiner le spectacle de reptiles avec un spectacle de feu ?",
          "Oui, et c'est une combinaison appréciée. Le spectacle de reptiles fonctionne bien en déambulation parmi les invités, puis le spectacle de feu clôture la soirée dehors.")],
 "service": {"name": "Spectacle de reptiles", "type": "Educational Reptile Show",
             "desc": "Spectacle de reptiles éducatif et interactif avec serpents, mygales et autres reptiles. Numéro d'intérieur sans feu, adapté à tous les âges."},
 "fotos": _FOTOS["fr"],
}}
