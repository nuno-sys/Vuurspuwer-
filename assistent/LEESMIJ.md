# Conceptantwoord bij een formulieraanvraag

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

## Later

In de map `assistent/` staat ook een Gmail-versie die conceptantwoorden maakt
op mail die rechtstreeks bij je binnenkomt, plus de opzet voor agenda en
Moneybird. Die staat uit tot je zover bent; hij vraagt een Google-serviceaccount.
