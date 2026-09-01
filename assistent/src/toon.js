/* Nuno's eigen toon, geleerd uit zijn verzonden mail.
 *
 * Beter dan voorbeelden met de hand invullen: hij hoeft niets bij te houden
 * en de assistent blijft meeleren als zijn manier van schrijven verandert.
 *
 * Er wordt gericht gezocht op boekingswoorden, dus privémail en post aan de
 * boekhouder blijven buiten beeld. */

import { zoekBerichten, haalBericht } from "./google.js";

const ZOEK =
  "in:sent newer_than:365d " +
  "(vuurshow OR vuurspuwer OR fakir OR fakirshow OR offerte OR optreden OR " +
  "boeking OR workshop OR showblok OR reiskosten OR mentalist)";
const HOEVEEL = 10;
const CACHE_URL = "https://assistent.intern/toonvoorbeelden";

/* Alles wegknippen wat geciteerd is: het antwoord van Nuno staat bovenaan,
   daaronder staat de mail van de klant en die kennen we al. */
function alleenEigenTekst(t) {
  const regels = t.split("\n");
  const uit = [];
  for (const r of regels) {
    if (/^\s*>/.test(r)) break;
    if (/^\s*(Op|On)\s.{5,60}\s(schreef|wrote)\s*:?\s*$/i.test(r)) break;
    if (/^\s*-{2,}\s*(Oorspronkelijk bericht|Original Message)/i.test(r)) break;
    if (/^\s*Van:\s/i.test(r) && uit.length > 2) break;
    uit.push(r);
  }
  return uit.join("\n").replace(/\n{3,}/g, "\n\n").trim();
}

export async function toonvoorbeelden(token, cache) {
  const gecached = await cache.match(CACHE_URL);
  if (gecached) return gecached.text();

  let tekst = "";
  try {
    const gevonden = await zoekBerichten(token, ZOEK, HOEVEEL);
    const stukken = [];
    for (const { id } of gevonden) {
      const m = await haalBericht(token, id);
      const eigen = alleenEigenTekst(m.tekst);
      /* te kort is een "prima, tot dan"; te lang is meestal een doorgestuurde
         draad waar weinig van te leren valt */
      if (eigen.length < 120 || eigen.length > 2000) continue;
      stukken.push(`--- antwoord van Nuno (${m.onderwerp}) ---\n${eigen}`);
      if (stukken.length >= 6) break;
    }
    tekst = stukken.join("\n\n");
  } catch (e) {
    console.error("toonvoorbeelden ophalen mislukt:", String(e).slice(0, 200));
  }

  /* een dag bewaren: zijn toon verandert niet per uur, en dit scheelt tien
     Gmail-verzoeken per ronde */
  await cache.put(CACHE_URL, new Response(tekst, {
    headers: { "Cache-Control": "max-age=86400", "Content-Type": "text/plain" },
  }));
  return tekst;
}
