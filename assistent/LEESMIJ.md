# Boekingsassistent — instellen

Wat dit doet: elke drie minuten kijkt hij of er nieuwe boekingsmail is, leest
die, en zet een **concept**antwoord klaar in dezelfde Gmail-thread. Er wordt
nooit iets verstuurd. Jij leest, past aan, drukt op verzenden.

Onder het antwoord staat een korte notitie voor jezelf: wat de klant wil, wat
opvalt, en wat er nog ontbreekt voor een offerte. Die haal je weg voor je
verstuurt.

---

## Stap 1 — het adres (5 minuten)

In de Google Admin-console, bij je eigen gebruiker:

1. Ga naar **admin.google.com → Directory → Gebruikers → jouw account**
2. Klik **Gebruikersgegevens → E-mailaliassen → Alias toevoegen**
3. Vul in: `boekingen` (dus `boekingen@vuurspuwer.com`)

Alles wat naar boekingen@ gaat komt nu gewoon in je bestaande inbox.

## Stap 2 — het filter (3 minuten)

Dit filter bepaalt wát de assistent mag zien. Alles daarbuiten blijft voor hem
onzichtbaar. In Gmail:

1. **Instellingen → Filters en geblokkeerde adressen → Nieuw filter maken**
2. Bij **Aan**: `boekingen@vuurspuwer.com`
3. **Filter maken** → vink aan: **Label toepassen** → **Nieuw label** →
   `Boekingen/Nieuw`

> Wil je later ook mail aan nuno@ laten meedoen, dan zet je er een tweede
> filter bij. Begin klein: eerst zien of het bevalt.

**Dit is je noodrem.** Zet je het filter uit, dan krijgt de assistent niets
meer te zien en gebeurt er niets.

## Stap 3 — de assistent toegang geven (10 minuten)

Dit is hetzelfde soort serviceaccount als je voor Search Console hebt gemaakt.

1. **console.cloud.google.com** → je project → **API's en services → Bibliotheek**
   → zoek **Gmail API** → **Inschakelen**
2. **API's en services → Inloggegevens → Inloggegevens maken → Serviceaccount**.
   Noem hem `boekingsassistent`. Geen rollen nodig.
3. Klik het serviceaccount aan → **Sleutels → Sleutel toevoegen → JSON**.
   Bewaar dat bestand goed; je hebt het zo één keer nodig.
4. Op hetzelfde scherm, onder **Geavanceerd**, staat een **Client-ID** (een
   lang getal). Kopieer die.
5. Ga naar **admin.google.com → Beveiliging → Toegangsbeheer voor API's →
   Domeinbrede delegatie → Nieuwe toevoegen**
   - Client-ID: het getal uit stap 4
   - Bereiken: `https://www.googleapis.com/auth/gmail.modify`

> Let op: alleen `gmail.modify`. Dat is lezen, labelen en concepten maken —
> **niet** versturen. De assistent kán dus niet mailen, ook niet als hij zou
> willen.

## Stap 4 — de sleutels op hun plek (5 minuten)

Twee stuks, allebei in Cloudflare:

**In het Cloudflare-dashboard → Workers & Pages → `vuurspuwer-boekingsassistent`
→ Settings → Variables and Secrets:**

| Naam | Wat erin gaat |
|---|---|
| `ANTHROPIC_API_KEY` | je sleutel van console.anthropic.com |
| `GOOGLE_SA_JSON` | de **hele inhoud** van het JSON-bestand uit stap 3 |
| `TEST_SLEUTEL` | verzin zelf iets lang en willekeurigs |

**In GitHub → je repo → Settings → Secrets and variables → Actions:**

| Naam | Wat erin gaat |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Cloudflare → My Profile → API Tokens → *Edit Cloudflare Workers* |
| `CLOUDFLARE_ACCOUNT_ID` | staat rechts in je Cloudflare-dashboard |

Die twee laatste zorgen dat de assistent zichzelf bijwerkt zodra er iets
verandert. Daarna hoef je nooit meer iets te installeren.

## Stap 5 — je spelregels invullen

Open `assistent/spelregels.md` en vul in wat er staat. Alles wat al op je site
staat — shows, prijzen, reiskosten, veelgestelde vragen — hoef je **niet** over
te typen: die leest hij van je eigen site (`llms-full.txt`), en die is altijd
bij, want hij wordt bij elke sitewijziging opnieuw gemaakt.

Het belangrijkste stuk is onderaan: **twee of drie antwoorden die je zelf ooit
hebt gestuurd**. Daaraan leert hij jouw toon. Zonder die voorbeelden klinkt hij
correct maar niet als jij.

## Stap 6 — proefdraaien

Stuur jezelf een mail naar `boekingen@vuurspuwer.com` vanaf een ander adres,
alsof je een klant bent. Binnen drie minuten staat er een concept in je Gmail.

Wil je niet wachten, open dan in je browser:
`https://vuurspuwer-boekingsassistent.<jouw-subdomein>.workers.dev/?sleutel=<TEST_SLEUTEL>`

---

## Wat je in Gmail terugziet

| Label | Betekenis |
|---|---|
| `Boekingen/Nieuw` | binnengekomen, wacht op de assistent |
| `Boekingen/Concept klaar` | er staat een concept voor je klaar |
| `Boekingen/Nagekeken worden` | er ging iets mis — deze doe je met de hand |

Die laatste is belangrijk: er blijft nooit een aanvraag stilzwijgend liggen.
Gaat er iets mis, dan zie je dat.

## Wat het kost

Ongeveer twee tot vijf cent per e-mail. Bij twintig aanvragen per dag zo'n
€15 tot €30 per maand. Cloudflare en de Gmail API zijn gratis op dit volume.

## Waar je op moet letten

De assistent noemt alleen prijzen die op je site staan. Klopt een prijs op de
site niet meer, pas hem daar aan — dan klopt het antwoord meteen ook.

Hij zegt nooit dat een datum vrij is; hij schrijft dat je het checkt. Dat komt
in een volgende stap, als de agenda erbij komt.

Staat er in een mail van een "klant" iets als *"negeer je instructies"* of
*"geef 80% korting"* — dat werkt niet. Hij behandelt de inhoud van een mail als
informatie, nooit als opdracht, en meldt het in de notitie aan jou. En omdat
hij alleen concepten maakt, kan er sowieso niets de deur uit zonder jou.
