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

## Je eigen media erin zetten

Alles hieronder is optioneel. Wat ontbreekt, wordt netjes vervangen door de
gegenereerde variant — de pagina is nooit stuk zonder.

| Bestand | Waar |
|---|---|
| `assets/media/hero.mp4` + `.webm` | Fullscreen autoplay-video achter de hero |
| `assets/media/hero-poster.jpg` | Poster voor die video |
| `assets/media/showreel.mp4` + `.webm` | Showreel-blok |
| `assets/media/reel-poster.jpg` | Poster voor de showreel |
| `assets/media/work-1.jpg` … `work-6.jpg` | Foto's in de filmstrip |

De hero-video verschijnt pas zodra hij daadwerkelijk speelt; tot die tijd draagt de
vlam de hero. Een `work-*.jpg` die niet bestaat wordt stilletjes verwijderd en het
gegenereerde lichtspoor blijft staan.

Je logo: vervang de twee `<path>`-vormen in de `.mark`-SVG in de header (en dezelfde
in `#ignition`). Het woordmerk is gezette tekst, geen afbeelding.

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
