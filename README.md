# Vuurspuwer.com

Eén statische pagina, gebouwd om te draaien op **Cloudflare Pages**. Geen build-stap,
geen dependencies: `index.html` is de hele site.

## Wat het is

Een donkere, fullscreen entertainer-site voor een vuurspuwer. Er brandt een echte,
live-gerenderde vlam (WebGL) langs de onderrand van het scherm die feller wordt
naarmate je scrolt — de content stijgt uit het vuur omhoog. Alle beeld op de pagina
wordt gegenereerd in de browser: er zitten geen afbeeldingsbestanden in de repo.

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

## Nog te vervangen

Dit is een eerste opzet — de volgende inhoud is **placeholder** en moet nog met echte
gegevens worden ingevuld:

- Telefoonnummer (`+31 (0)00 000 0000`) en e-mailadres
- De drie reacties onder "Wat opdrachtgevers zeggen" — namen staan als `[Naam]`,
  `[Festival]`, `[Bedrijf]`, `[Locatie]`
- De vier showspecificaties (vlamhoogte, showtijd, opbouwtijd) — controleer of deze
  cijfers voor jouw show kloppen
- De acts, hun beschrijvingen en de chips (vuur/LED, binnen/buiten, speelduur)

## Boekingsformulier

Het formulier is nog niet gekoppeld. Het valideert, en biedt daarna een `mailto:`-link
met de aanvraag erin. Zodra er een endpoint is: vervang het blok onder
`Demo build: nothing is sent anywhere` in `initForm()` door een `fetch()` naar dat
endpoint.

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
