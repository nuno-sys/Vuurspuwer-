# Conceptantwoord bij een formulieraanvraag

> **Dit is wat er nu aan staat.** Verderop staat een Gmail-versie beschreven
> die ook je gewone inbox meeleest; die is gebouwd maar staat uit en vraagt
> een Google-serviceaccount. Je hoeft daar nu niets mee.

## Wat het doet

Iemand vult het formulier op de site in. Er gebeurt dan drie dingen:

1. De aanvraag komt bij jou binnen — zoals altijd.
2. De klant krijgt zijn bevestiging — zoals altijd.
3. **Nieuw:** je krijgt een tweede mail met een kant-en-klaar conceptantwoord,
   plus een korte notitie over wat opvalt en wat er nog ontbreekt voor een
   offerte. Onderin zit een knop die je mailprogramma opent met de tekst er al
   in.

Er gaat **niets** naar de klant behalve de bevestiging die er altijd al was.
Het concept is voor jou. Jij leest, past aan, verstuurt.

## Wat je moet doen

Eén ding: zet je Anthropic-sleutel in Cloudflare.

**Cloudflare-dashboard → Workers & Pages → je site → Settings → Variables and
Secrets → Add → Encrypt:**

| Naam | Waarde |
|---|---|
| `ANTHROPIC_API_KEY` | je sleutel van console.anthropic.com |

Dat is alles. Staat de sleutel er niet, dan werkt de site precies zoals nu —
twee mails, geen concept. Er gaat dus nooit iets stuk doordat je hem vergeet.

## Waar de kennis vandaan komt

Van je eigen site. `assistent.txt` wordt bij elke build gemaakt uit de
prijzenpagina, de showpagina's en de veelgestelde vragen. Daardoor kan er geen
prijs in een concept staan die niet op je site staat, en klopt alles meteen
zodra je een prijs aanpast.

Wat er **niet** op je site staat, zet je in `assistent/spelregels.md`: je toon,
je ondergrens, betaalvoorwaarden, wat je niet doet, wat je nodig hebt op
locatie. Dat bestand blijft privé — het staat niet op het web.

Het belangrijkste stuk staat onderaan dat bestand: **twee of drie antwoorden
die je zelf ooit hebt gestuurd**. Daaraan leert hij jouw toon. Zonder die
voorbeelden klinkt hij correct, maar niet als jij. Vul je niets in, dan werkt
het ook — hij schrijft dan neutraal en netjes.

Na het aanpassen van `spelregels.md`: `python3 build.py`, committen, pushen.

## Wat het kost

Ongeveer vijf cent per aanvraag.

## Waar je op moet letten

- Hij zegt nooit dat een datum vrij is, want hij ziet je agenda niet. Hij
  schrijft dat je het checkt.
- Bedragen zijn altijd een indicatie met een aanbod voor een offerte op maat.
- Staat er in het berichtveld iets als *"negeer je instructies"* of *"geef 80%
  korting"*, dan behandelt hij dat als informatie en meldt het in de notitie.
  Hij volgt het niet op. En omdat er sowieso alleen een concept naar jou gaat,
  kan er niets de deur uit zonder jou.
- Lukt het schrijven niet, dan krijg je een mail met de reden. De aanvraag en
  de bevestiging zijn dan gewoon verstuurd.

---

# De Gmail-versie — STAAT UIT

> Voor later. Hij is gebouwd en getest, maar wordt niet uitgerold: de
> GitHub-actie start alleen met de hand en er staat geen serviceaccount.
> Je hoeft hier niets voor te doen.

Hierboven ging over het formulier. Er staat ook een versie klaar die je
gewone **inbox** meeleest, zodat je ook niets mist als iemand rechtstreeks
naar nuno@ mailt in plaats van het formulier in te vullen.

## Hoe hij te werk gaat

Elke drie minuten kijkt hij naar je primaire inbox van de afgelopen week.
Per mail:

1. **Gratis overslaan.** Nieuwsbrieven (te herkennen aan de uitschrijflink),
   no-reply-afzenders en je eigen verzonden post gaan er meteen uit. Reclame,
   sociale post en meldingen sorteert Gmail zelf al weg en komen niet eens
   langs. Hier wordt Claude niet eens voor gevraagd.
2. **Sorteren.** Eén korte vraag: is dit iemand die mogelijk wil boeken?
   Bij nee gebeurt er niets — geen concept, geen zichtbaar label, niets. Je
   boekhouder en je verzekering blijven met rust.
3. **Schrijven.** Alleen bij ja komt er een concept in dezelfde thread.

Mail die hij bekeken heeft krijgt een onzichtbaar merkteken (`vs-gezien`),
zodat hij niet twee keer naar hetzelfde kijkt. Dat label zie je niet: het
staat niet in je labellijst en niet op je berichten.

## Hij leert je toon uit je eigen mail

Hij zoekt in je **verzonden items** op boekingswoorden — vuurshow, offerte,
optreden, workshop — en gebruikt je laatste antwoorden als voorbeeld van hoe
jij schrijft. Geciteerde tekst knipt hij eruit, dus alleen jouw eigen woorden
tellen mee. Privémail en post aan de boekhouder komen daar niet in voor.

Je hoeft dus zelf geen voorbeelden meer in `spelregels.md` te zetten. En hij
blijft meeleren: verandert jouw manier van schrijven, dan verandert hij mee.
De voorbeelden worden een dag bewaard, dus dit kost bijna niets.

## Wat je moet doen om hem aan te zetten

1. **Gmail API aanzetten** — console.cloud.google.com → je project →
   API's en services → Bibliotheek → *Gmail API* → Inschakelen
2. **Serviceaccount maken** — API's en services → Inloggegevens →
   Inloggegevens maken → Serviceaccount. Noem hem `boekingsassistent`,
   geen rollen nodig. Klik hem daarna aan → Sleutels → Sleutel toevoegen →
   JSON. Bewaar dat bestand.
3. **Client-ID kopiëren** — staat op datzelfde scherm onder Geavanceerd,
   een lang getal.
4. **Delegatie instellen** — admin.google.com → Beveiliging → Toegangsbeheer
   voor API's → Domeinbrede delegatie → Nieuwe toevoegen. Client-ID uit
   stap 3, en als bereik precies dit:
   `https://www.googleapis.com/auth/gmail.modify`

   > Alleen `gmail.modify`: lezen, labelen en concepten maken. **Geen
   > verzendrecht.** Hij kán niet mailen, ook niet als hij zou willen.

5. **Sleutels zetten.** In Cloudflare bij de Worker
   `vuurspuwer-boekingsassistent` → Settings → Variables and Secrets:
   `ANTHROPIC_API_KEY`, `GOOGLE_SA_JSON` (de hele inhoud van het
   JSON-bestand) en `TEST_SLEUTEL` (verzin zelf iets lang).
   In GitHub → Settings → Secrets → Actions: `CLOUDFLARE_API_TOKEN` en
   `CLOUDFLARE_ACCOUNT_ID`.
6. **Uitrollen.** GitHub → Actions → *Boekingsassistent uitrollen* → Run
   workflow. Daarna gaat het vanzelf bij elke wijziging.

## Wat je in Gmail terugziet

| Label | Betekenis |
|---|---|
| `Boekingen/Concept klaar` | er staat een concept voor je klaar |
| `Boekingen/Nagekeken worden` | er ging iets mis — deze doe je met de hand |

Meer niet. Alle andere post blijft onaangeroerd.

## Wat het kost

Sorteren kost een fractie van een cent per mail; alleen bij een echte
boekingsvraag komt er een antwoord van een paar cent achteraan. Bij dertig
mails per dag waarvan er vijf over boekingen gaan: ongeveer €10 per maand.

## De noodrem

Zet de Worker op pauze in het Cloudflare-dashboard, of verwijder de secret
`GOOGLE_SA_JSON`. Dan stopt hij onmiddellijk en blijft de rest van je site
gewoon werken.
