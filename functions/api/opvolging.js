/* Dagelijks: wie wacht er nog op een antwoord?
 *
 * Wordt aangeroepen door de bestaande GitHub-actie die 's ochtends al draait.
 * Loopt de bewaarde aanvragen langs, en voor elke aanvraag die lang genoeg
 * stil is gebleven komt er één mail met een kant-en-klaar duwtje.
 *
 * Er gaat niets naar de klant. Eén mail per aanvraag, nooit meer.  */

import { stuurDuwtje, isRijp } from "../../assistent/opvolging.js";

const FROM = "Vuurspuwer Nuno <boekingen@vuurspuwer.com>";
const TO = "nuno@vuurspuwer.com";
const PER_KEER = 8;

const wacht = (ms) => new Promise((r) => setTimeout(r, ms));

async function resend(key, payload, pogingen = 3) {
  let laatste = "";
  for (let i = 0; i < pogingen; i++) {
    if (i) await wacht(700 * i);
    let r;
    try {
      r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch (e) { laatste = `netwerk: ${e && e.message}`; continue; }
    if (r.ok) return r.json();
    laatste = `Resend ${r.status}: ${(await r.text()).slice(0, 200)}`;
    if (r.status !== 429 && r.status < 500) break;
  }
  throw new Error(laatste || "onbekend");
}

async function ronde(env) {
  const nu = Date.now();
  const { keys } = await env.OPVOLG.list({ prefix: "aanvraag:", limit: 200 });
  let bekeken = 0, verstuurd = 0, mislukt = 0;

  for (const { name } of keys) {
    if (verstuurd >= PER_KEER) break;
    const ruw = await env.OPVOLG.get(name);
    if (!ruw) continue;
    let rij;
    try { rij = JSON.parse(ruw); } catch { await env.OPVOLG.delete(name); continue; }
    bekeken++;
    if (!isRijp(rij, nu)) continue;

    try {
      await stuurDuwtje(env, rij, nu, env.MAIL_FROM || FROM, env.MAIL_TO || TO, resend, wacht);
      verstuurd++;
      /* meteen weg: één duwtje per aanvraag, nooit twee */
      await env.OPVOLG.delete(name);
    } catch (e) {
      mislukt++;
      console.error("duwtje mislukt voor", rij.naam, String(e).slice(0, 200));
      /* na drie mislukte pogingen laten we hem gaan, anders blijft hij
         elke ochtend terugkomen */
      rij.pogingen = (rij.pogingen || 0) + 1;
      if (rij.pogingen >= 3) await env.OPVOLG.delete(name);
      else await env.OPVOLG.put(name, JSON.stringify(rij), { expirationTtl: 60 * 24 * 3600 });
    }
  }
  return { bekeken, verstuurd, mislukt };
}

async function draai(request, env) {
  const sleutel = request.headers.get("x-sleutel") ||
                  new URL(request.url).searchParams.get("sleutel");
  if (!env.OPVOLG_SLEUTEL || sleutel !== env.OPVOLG_SLEUTEL) {
    return new Response("nee", { status: 403 });
  }
  if (!env.OPVOLG) return Response.json({ fout: "geen KV-koppeling" }, { status: 503 });
  if (!env.ANTHROPIC_API_KEY || !env.RESEND_API_KEY) {
    return Response.json({ fout: "sleutels ontbreken" }, { status: 503 });
  }
  try {
    return Response.json(await ronde(env));
  } catch (e) {
    return Response.json({ fout: String(e).slice(0, 400) }, { status: 500 });
  }
}

export const onRequestPost = ({ request, env }) => draai(request, env);
export const onRequestGet = ({ request, env }) => draai(request, env);
