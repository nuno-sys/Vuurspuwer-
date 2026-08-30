# Vuurspuwer.com

Eén statische pagina, gebouwd om te draaien op **Cloudflare Pages**. Geen build-stap,
geen dependencies: `index.html` is de hele site.

## Wat het is

Een donkere, fullscreen site voor Vuurspuwer Nuno — vuurspuwer, fakir en mentalist. Er brandt een echte,
live-gerenderde vlam (WebGL) langs de onderrand van het scherm die feller wordt
naarmate je scrolt — de content stijgt uit het vuur omhoog. Alle beeld op de pagina
wordt gegenereerd in de browser: er zitten geen afbeeldingsbestanden in de repo.

- **Intro**: het merk brandt midden op zwart terwijl de teller naar 100 loopt.
  Daarna komt de site erachter omhoog en vliegt het merk naar zijn plek in de
  header — het dooft onderweg en brandt een vuurspoor. Dat spoor is de poi, dus
  de intro legt de interactie uit voordat de bezoeker iets aanraakt.
- **De brand**: niets op deze pagina verschijnt, alles vat vlam. Elk stuk tekst,
  elke kaart en elke foto staat eerst zwart op zwart. Een vuurlijn laag in beeld
  steekt aan wat er langs stijgt: de letters branden van onder naar boven door
  zichzelf heen en laten hun eigen kleur achter. Bij het laden klimt die lijn
  eenmalig door de hero omhoog; daarna staat hij stil en beweegt de pagina.
  Wat eenmaal gebrand is blijft leesbaar — er dooft nooit iets terug.
- WebGL fragment-shader voor de vlam (fbm-noise, domain warp), met een pointer-lean
- Canvas-2D vonkenlaag over de hele viewport
- Long-exposure lichtsporen als posterbeeld per act (cirkel, lemniscaat, spiraal, golf)
- Wordmark die zichzelf meet en exact op de paginabreedte past, op elk viewport
- Scroll-gedreven manifesto, tellers, sleepbare filmstrip, fullscreen mobiel menu
- Volledige `prefers-reduced-motion`-route: de vlam wordt dan een statisch verloop

## Media die er nu in zit

    assets/media/hero-portrait.mp4   730x1022, 5 s, stil — hero op telefoons
    assets/media/showreel.mp4        540x540, 13 s, met geluid — showreel
    assets/media/reel-poster.jpg     poster voor de showreel
    assets/media/work-1.jpg          vuurspuwen op een festivalplein
    assets/media/work-2.webp         fakirshow, spijkerbed
    assets/media/work-3.webp         vuurspuwen tegen zwarte achtergrond
    assets/brand/nuno.svg            het woordmerk, uit de PNG getraceerd
    assets/brand/nuno-logo-origineel.png   het aangeleverde origineel
    assets/brand/                    logo's van SBS6, RTL 4, VTM, Walibi,
                                     IKEA, Emporium en Julianatoren

## Het woordmerk

Het aangeleverde logo is een PNG van 292x80 in twee kleuren. Te klein om groot
in beeld te brengen, dus is de vorm getraceerd naar vector: de pixelrand is
gevolgd, vereenvoudigd en weer glad gemaakt, waarbij de drips onder de N en de
vlam aan de O bewaard zijn gebleven.

Die vector zit als data-URI in de CSS (`--logo-src` op `.logo`), niet als los
bestand. Dat scheelt een verzoek en werkt ook waar externe afbeeldingen
geblokkeerd zijn. `assets/brand/nuno.svg` blijft staan als bron, bijvoorbeeld
om er een favicon van te maken.

Het gebruikt geen eigen kleur meer: het masker wordt gevuld met het
vuurverloop van de site, met een langzame gloed die er in negen seconden
doorheen trekt. Het originele goud staat in
`assets/brand/nuno-logo-origineel.png` als je terug wilt.

Nog aan te leveren:

- **`assets/media/hero-landscape.mp4`** — een breed origineel voor de hero op
  desktop. De twee bestaande video's zijn social-crops (staand en vierkant) en
  worden wazig als je ze over 1440 px uitrekt. Zolang dit bestand ontbreekt
  staat `HERO_VIDEO.landscape` in `index.html` op `null` en draagt de vlam de
  hero; zet die regel op het pad zodra het bestand er is.
- Meer foto's voor de filmstrip: kaders 4 tot en met 6 tonen nu nog een
  getekend lichtspoor.

## Waar de inhoud vandaan komt

De teksten, cijfers en contactgegevens zijn opgehaald uit Nuno's eigen sites en
zijn boekingsprofiel via websearch — de sites zelf zijn vanuit de bouwomgeving niet
bereikbaar, dus foto's en het logo konden niet worden meegenomen.

| Op de pagina | Bron |
|---|---|
| 17 jaar, TV-credits (SBS6, RTL, VTM, Engeland, Uri Geller) | vuurspuwer.com/over-nuno |
| Shows en speelduren (Power-Act 5–10 min, Complete Vuurshow 20–30 min) | vuurspuwer.com, fakirshow.nl |
| Fakir, reptielen, mentalisme, workshop vuurspuwen | vuurspuwer.com/entertainer-huren |
| Veiligheid: certificering, vergunningseisen, veiligheidsafstanden | vuurspuwer.com/vuurspuwer-inhuren |
| 4,9 gemiddeld uit 134 beoordelingen | showbird.com — profiel Nuno |
| +31 6 200 207 23, ma–za 9:00–18:00 | vuurspuwer.com |
| contact@fakir-show.nl | nu-no.nl/contact |

**Nog controleren:** of `contact@fakir-show.nl` het adres is dat je op vuurspuwer.com
wilt tonen, en of het beoordelingscijfer nog klopt — dat loopt op.

## Wat er nog niet in zit

- **Je logo.** De vlam in de header is een tijdelijke SVG. Vervang de twee `<path>`-vormen
  in `.mark` (header) en in `#ignition`.
- **Je foto's.** Alle beeld is nu gegenereerd in de browser. Zet je eigen bestanden
  in `assets/media/` (zie tabel hierboven) en ze nemen het automatisch over.
- **Video.** Idem — hero en showreel hebben klaarstaande slots.

## Boekingsformulier

Het formulier is nog niet gekoppeld. Het valideert, en biedt daarna een `mailto:`-link
met de aanvraag erin. Zodra er een endpoint is: vervang het blok onder
`Demo build: nothing is sent anywhere` in `initForm()` door een `fetch()` naar dat
endpoint.

WhatsApp loopt nu via een directe `wa.me/31620020723`-link in de hero, de
contactkolom en onder het formulier — daar is geen backend voor nodig.

## Deployen naar Cloudflare Pages

Er valt niets te bouwen. In het Pages-project:

- **Build command**: leeg laten
- **Build output directory**: `/`

```
npx wrangler pages deploy . --project-name=vuurspuwer
```

`_headers` zet caching en een paar security-headers. Externe verzoeken beperken zich
tot Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`).

### Als er later een Worker bij komt

Voor bijvoorbeeld het boekingsformulier: zet een `functions/api/boeking.js` in de repo.
Pages pikt die map automatisch op als Pages Functions, zonder aparte Worker-deploy.
