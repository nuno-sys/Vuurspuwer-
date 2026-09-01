/* Aanvraagformulier → echte e-mail, via Resend (https://resend.com).
 *
 * Draait als Cloudflare Pages Function op POST /api/contact en verstuurt
 * twee mails: de aanvraag naar Nuno (met reply-to van de aanvrager) en
 * een bevestiging in huisstijl naar de aanvrager, met een kopie van wat
 * er is ingevuld en de belofte binnen 24 uur te reageren.
 *
 * Vereist één geheim in het Pages-project (Settings → Variables and
 * Secrets): RESEND_API_KEY. Optioneel kunnen MAIL_FROM en MAIL_TO de
 * standaardadressen hieronder overschrijven.
 */

import { stuurConcept } from "../../assistent/concept.js";

const SITE = "https://vuurspuwer.com";
const DEFAULT_TO = "nuno@vuurspuwer.com";
const DEFAULT_FROM = "Vuurspuwer Nuno <boekingen@vuurspuwer.com>";
const WHATSAPP = "https://wa.me/31620020723";

const FIELDS = [
  ["naam", "Naam", 120],
  ["email", "E-mail", 254],
  ["telefoon", "Telefoon", 40],
  ["datum", "Datum evenement", 40],
  ["act", "Show", 60],
  ["locatie", "Locatie", 160],
  ["ruimte", "Binnen of buiten", 20],
  ["bericht", "Bericht", 4000],
];

/* De bevestiging aan de aanvrager gaat mee in de taal van de pagina
   waarop het formulier stond; de aanvraag zelf blijft Nederlands. */
const T9N = {
  nl: {
    labels: { naam: "Naam", email: "E-mail", telefoon: "Telefoon", datum: "Datum evenement",
              act: "Show", locatie: "Locatie", ruimte: "Binnen of buiten", bericht: "Bericht" },
    subject: (n) => `Bedankt ${n} — je aanvraag bij Vuurspuwer Nuno is ontvangen \u{1F525}`,
    pre: (n) => `Bedankt ${n} — je aanvraag is in goede orde ontvangen. Ik reageer binnen 24 uur.`,
    tagline: "VUURSPUWER · FAKIR · MENTALIST",
    hi: (n) => `Bedankt, ${n}! \u{1F525}`,
    bodyA: "Je aanvraag is in goede orde ontvangen. Ik bekijk hem persoonlijk en je hoort",
    bodyB: "binnen 24 uur", bodyC: "van mij of je datum nog vrij is, met een vrijblijvende offerte op maat.",
    recap: "Dit heb je ingevuld",
    wa_btn: "Spoedvraag? App direct via WhatsApp",
    wa_txt: (n) => `Hallo Nuno, ik heb net een aanvraag gestuurd (${n}). Ik heb een spoedvraag:`,
    foot: "Vuurspuwer Nuno · Nederland, België & internationaal",
    plain: (n) => `Bedankt ${n}! Je aanvraag is in goede orde ontvangen; ik reageer binnen 24 uur.`,
  },
  en: {
    labels: { naam: "Name", email: "Email", telefoon: "Phone", datum: "Event date",
              act: "Show", locatie: "Location", ruimte: "Indoors or outdoors", bericht: "Message" },
    subject: (n) => `Thank you ${n} — your request to Fire Breather Nuno has been received \u{1F525}`,
    pre: (n) => `Thank you ${n} — your request has been received. I'll reply within 24 hours.`,
    tagline: "FIRE BREATHER · FAKIR · MENTALIST",
    hi: (n) => `Thank you, ${n}! \u{1F525}`,
    bodyA: "Your request has been received. I'll review it personally and you'll hear",
    bodyB: "within 24 hours", bodyC: "whether your date is still free, with a free tailored quote.",
    recap: "What you submitted",
    wa_btn: "Urgent question? WhatsApp me directly",
    wa_txt: (n) => `Hello Nuno, I just sent a request (${n}). I have an urgent question:`,
    foot: "Fire Breather Nuno · Netherlands, Belgium & international",
    plain: (n) => `Thank you ${n}! Your request has been received; I'll reply within 24 hours.`,
  },
  de: {
    labels: { naam: "Name", email: "E-Mail", telefoon: "Telefon", datum: "Datum der Veranstaltung",
              act: "Show", locatie: "Ort", ruimte: "Drinnen oder draußen", bericht: "Nachricht" },
    subject: (n) => `Danke ${n} — Ihre Anfrage bei Feuerspucker Nuno ist eingegangen \u{1F525}`,
    pre: (n) => `Danke ${n} — Ihre Anfrage ist gut angekommen. Ich antworte innerhalb von 24 Stunden.`,
    tagline: "FEUERSPUCKER · FAKIR · MENTALIST",
    hi: (n) => `Vielen Dank, ${n}! \u{1F525}`,
    bodyA: "Ihre Anfrage ist gut angekommen. Ich sehe sie mir persönlich an und Sie hören",
    bodyB: "innerhalb von 24 Stunden", bodyC: "ob Ihr Termin noch frei ist — mit einem kostenlosen Angebot nach Maß.",
    recap: "Ihre Angaben",
    wa_btn: "Dringende Frage? Direkt per WhatsApp",
    wa_txt: (n) => `Hallo Nuno, ich habe gerade eine Anfrage gesendet (${n}). Ich habe eine dringende Frage:`,
    foot: "Feuerspucker Nuno · Niederlande, Belgien & international",
    plain: (n) => `Vielen Dank ${n}! Ihre Anfrage ist eingegangen; ich antworte innerhalb von 24 Stunden.`,
  },
  fr: {
    labels: { naam: "Nom", email: "E-mail", telefoon: "Téléphone", datum: "Date de l'événement",
              act: "Spectacle", locatie: "Lieu", ruimte: "Intérieur ou extérieur", bericht: "Message" },
    subject: (n) => `Merci ${n} — votre demande à Nuno a bien été reçue \u{1F525}`,
    pre: (n) => `Merci ${n} — votre demande a bien été reçue. Je réponds sous 24 heures.`,
    tagline: "CRACHEUR DE FEU · FAKIR · MENTALISTE",
    hi: (n) => `Merci, ${n} ! \u{1F525}`,
    bodyA: "Votre demande a bien été reçue. Je l'examine personnellement et vous saurez",
    bodyB: "sous 24 heures", bodyC: "si votre date est encore libre, avec un devis gratuit sur mesure.",
    recap: "Votre demande",
    wa_btn: "Question urgente ? WhatsApp direct",
    wa_txt: (n) => `Bonjour Nuno, je viens d'envoyer une demande (${n}). J'ai une question urgente :`,
    foot: "Cracheur de feu Nuno · Pays-Bas, Belgique & international",
    plain: (n) => `Merci ${n} ! Votre demande a bien été reçue ; je réponds sous 24 heures.`,
  },
};

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function clean(data) {
  const out = {};
  for (const [key, , max] of FIELDS) {
    out[key] = String(data[key] ?? "").replace(/\s+/g, " ").trim().slice(0, max);
  }
  // het bericht mag zijn regeleinden houden
  out.bericht = String(data.bericht ?? "").trim().slice(0, 4000);
  return out;
}

function rowsHtml(d, labels) {
  const rows = [];
  for (const [key] of FIELDS) {
    const label = labels[key];
    if (!d[key]) continue;
    const value = key === "bericht"
      ? esc(d[key]).replace(/\n/g, "<br>")
      : esc(d[key]);
    rows.push(
      `<tr><td style="padding:9px 14px 9px 0;font-family:'Courier New',monospace;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:#8A7A6D;vertical-align:top;white-space:nowrap;">${label}</td>` +
      `<td style="padding:9px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#FFF3D6;">${value}</td></tr>`);
  }
  return rows.join("");
}

/* Bevestiging voor de aanvrager: zwart, het logo in het midden, de
   kopie van de aanvraag en onderaan de WhatsApp-knop voor spoed. */
function confirmationHtml(d, t) {
  return `<!doctype html>
<html lang="nl">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Je aanvraag is ontvangen</title></head>
<body style="margin:0;padding:0;background-color:#050302;">
<div style="display:none;max-height:0;overflow:hidden;">${esc(t.pre(d.naam))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#050302;">
<tr><td align="center" style="padding:36px 16px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
    <tr><td align="center" style="padding:8px 0 28px;">
      <img src="${SITE}/assets/media/logo-mail.png" width="220" alt="NUNO" style="display:block;width:220px;max-width:60%;height:auto;border:0;">
      <div style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:3px;color:#8A7A6D;padding-top:10px;">${t.tagline.replace(/·/g, "&middot;")}</div>
    </td></tr>
    <tr><td style="background-color:#0A0705;border:1px solid #2e2113;border-radius:14px;padding:30px 28px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:22px;line-height:1.25;font-weight:bold;color:#FFB020;padding-bottom:14px;">${esc(t.hi(d.naam))}</td></tr>
        <tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#C6B29E;padding-bottom:8px;">
          ${esc(t.bodyA)}
          <strong style="color:#FFF3D6;">${esc(t.bodyB)}</strong> ${esc(t.bodyC)}
        </td></tr>
        <tr><td style="padding:18px 0 6px;font-family:'Courier New',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#FFB020;">${esc(t.recap)}</td></tr>
        <tr><td style="border-top:1px solid #2e2113;padding-top:6px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rowsHtml(d, t.labels)}</table>
        </td></tr>
        <tr><td align="center" style="padding:26px 0 6px;">
          <a href="${WHATSAPP}?text=${encodeURIComponent(t.wa_txt(d.naam))}"
             style="display:inline-block;background-color:#FFB020;background-image:linear-gradient(96deg,#FF4D0A,#FFB020 30%,#FFF3D6 52%,#FFB020 74%,#FF4D0A);color:#170800;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;text-decoration:none;padding:13px 26px;border-radius:999px;">
            &#128172;&nbsp; ${esc(t.wa_btn)}
          </a>
        </td></tr>
      </table>
    </td></tr>
    <tr><td align="center" style="padding:24px 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.8;color:#8A7A6D;">
      ${t.foot.replace(/·/g, "&middot;")}<br>
      <a href="${SITE}/" style="color:#FFB020;text-decoration:none;">vuurspuwer.com</a> &middot;
      <a href="tel:+31620020723" style="color:#FFB020;text-decoration:none;">+31 6 200 207 23</a> &middot;
      <a href="mailto:${DEFAULT_TO}" style="color:#FFB020;text-decoration:none;">${DEFAULT_TO}</a>
    </td></tr>
  </table>
</td></tr>
</table>
</body>
</html>`;
}

/* De aanvraag zelf, voor Nuno: zelfde stijl, alle velden op een rij. */
function requestHtml(d) {
  return `<!doctype html>
<html lang="nl">
<head><meta charset="utf-8"><title>Nieuwe aanvraag</title></head>
<body style="margin:0;padding:0;background-color:#050302;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#050302;">
<tr><td align="center" style="padding:32px 16px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
    <tr><td align="center" style="padding:0 0 22px;">
      <img src="${SITE}/assets/media/logo-mail.png" width="170" alt="NUNO" style="display:block;width:170px;height:auto;border:0;">
    </td></tr>
    <tr><td style="background-color:#0A0705;border:1px solid #2e2113;border-radius:14px;padding:26px 28px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:19px;font-weight:bold;color:#FFB020;padding-bottom:12px;">&#128293; Nieuwe aanvraag via vuurspuwer.com</td></tr>
        <tr><td style="border-top:1px solid #2e2113;padding-top:6px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rowsHtml(d, T9N.nl.labels)}</table>
        </td></tr>
        <tr><td style="padding-top:16px;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#8A7A6D;">
          Beantwoord deze mail om ${esc(d.naam)} direct te mailen (reply-to staat goed).
        </td></tr>
      </table>
    </td></tr>
  </table>
</td></tr>
</table>
</body>
</html>`;
}

function textVersion(d, intro, labels) {
  const lines = [intro, ""];
  for (const [key] of FIELDS) {
    if (d[key]) lines.push(`${labels[key]}: ${d[key]}`);
  }
  return lines.join("\n");
}

const wacht = (ms) => new Promise((r) => setTimeout(r, ms));

/* Resend staat twee verzoeken per seconde toe. Twee mails direct achter
   elkaar (de aanvraag naar Nuno, dan de bevestiging naar de aanvrager)
   liepen daar tegenaan: de eerste ging door, de tweede kreeg 429 en werd
   stil weggegooid. Vandaar: opnieuw proberen bij 429 en bij tijdelijke
   serverfouten, met oplopende pauze. */
async function resend(key, payload, pogingen = 3) {
  let laatste = "";
  for (let i = 0; i < pogingen; i++) {
    if (i) await wacht(700 * i);
    let r;
    try {
      r = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { "Authorization": `Bearer ${key}`, "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      laatste = `netwerk: ${e && e.message ? e.message : e}`;
      continue;
    }
    if (r.ok) return r.json();
    const detail = await r.text().catch(() => "");
    laatste = `Resend ${r.status}: ${detail.slice(0, 300)}`;
    /* 4xx anders dan 429 is een echte afwijzing: opnieuw proberen helpt niet */
    if (r.status !== 429 && r.status < 500) break;
  }
  throw new Error(laatste || "onbekend");
}

export async function onRequestPost({ request, env, waitUntil }) {
  const json = (status, body) => new Response(JSON.stringify(body), {
    status, headers: { "Content-Type": "application/json" },
  });

  // alleen aanroepen vanaf de site zelf
  const origin = request.headers.get("Origin") || "";
  if (origin && !/^https:\/\/([a-z0-9-]+\.)*(vuurspuwer\.com|pages\.dev)$/.test(origin)) {
    return json(403, { ok: false, error: "origin" });
  }

  let data;
  try {
    const type = request.headers.get("Content-Type") || "";
    data = type.includes("json")
      ? await request.json()
      : Object.fromEntries((await request.formData()).entries());
  } catch {
    return json(400, { ok: false, error: "body" });
  }

  // honingpot: robots die het onzichtbare veld invullen krijgen "ok"
  if (String(data.website ?? "").trim() !== "") {
    return json(200, { ok: true });
  }

  const lang = ["nl", "en", "de", "fr"].includes(data.lang) ? data.lang : "nl";
  const t = T9N[lang];
  const d = clean(data);
  if (!d.naam || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) {
    return json(422, { ok: false, error: "velden" });
  }

  const key = env.RESEND_API_KEY;
  if (!key) {
    // nog niet geconfigureerd: de site valt terug op het mailto-pad
    return json(503, { ok: false, error: "config" });
  }
  const to = env.MAIL_TO || DEFAULT_TO;
  const from = env.MAIL_FROM || DEFAULT_FROM;

  // 1. de aanvraag naar Nuno — dit is de mail die er echt toe doet
  await resend(key, {
    from,
    to: [to],
    reply_to: [d.email],
    subject: `\u{1F525} Aanvraag van ${d.naam}${d.act && d.act !== "Weet ik nog niet" ? ` — ${d.act}` : ""}${d.datum ? ` op ${d.datum}` : ""}`,
    html: requestHtml(d),
    text: textVersion(d, "Nieuwe aanvraag via vuurspuwer.com", T9N.nl.labels),
  });

  // 2. de bevestiging naar de aanvrager. De aanvraag zelf is al binnen, dus
  //    dit mag de melding aan de bezoeker niet omgooien - maar stil laten
  //    mislukken mag ook niet: dan denkt de klant dat hij een bevestiging
  //    krijgt die nooit komt, en weet Nuno van niets.
  await wacht(600);                       // ruim binnen Resends 2/seconde
  let confirmed = true, reden = "";
  try {
    await resend(key, {
      from,
      to: [d.email],
      reply_to: [to],
      subject: t.subject(d.naam),
      html: confirmationHtml(d, t),
      text: textVersion(d, `${t.plain(d.naam)} WhatsApp: ${WHATSAPP}`, t.labels),
    });
  } catch (e) {
    confirmed = false;
    reden = String((e && e.message) || e).slice(0, 300);
    // Nuno moet het weten, anders wacht de klant op een mail die niet komt
    try {
      await wacht(600);
      await resend(key, {
        from,
        to: [to],
        reply_to: [d.email],
        subject: `\u{26A0} Bevestiging NIET verstuurd aan ${d.naam} <${d.email}>`,
        text: [
          `De aanvraag van ${d.naam} is binnengekomen, maar de automatische`,
          `bevestiging naar ${d.email} is niet verstuurd.`,
          ``,
          `Reden van de mailserver:`,
          reden,
          ``,
          `Beantwoord deze mail om ${d.naam} alsnog persoonlijk te bevestigen.`,
        ].join("\n"),
      }, 2);
    } catch { /* dan houdt het op; de aanvraag zelf is wel bezorgd */ }
  }

  // 3. de aanvraag onthouden voor de opvolging over een paar dagen. Zonder
  //    KV-koppeling gebeurt dit niet en werkt de rest gewoon door.
  if (env.OPVOLG) {
    try {
      await env.OPVOLG.put(
        `aanvraag:${Date.now()}:${Math.random().toString(36).slice(2, 8)}`,
        JSON.stringify({
          naam: d.naam, email: d.email, datum: d.datum, act: d.act,
          locatie: d.locatie, bericht: (d.bericht || "").slice(0, 600),
          lang, ontvangen: Date.now(),
        }),
        { expirationTtl: 60 * 24 * 3600 }     // na twee maanden vanzelf weg
      );
    } catch { /* opvolging is een extraatje; de aanvraag gaat voor */ }
  }

  // 4. het conceptantwoord voor Nuno. Dit gebeurt NA het antwoord aan de
  //    browser, zodat het formulier snel blijft en de aanvraag zelf nooit op
  //    Claude hoeft te wachten. Gaat het mis, dan is er niets verloren: de
  //    aanvraag ligt al bij Nuno en de klant heeft zijn bevestiging.
  if (env.ANTHROPIC_API_KEY && typeof waitUntil === "function") {
    waitUntil(
      stuurConcept(env, d, lang, from, to, resend, wacht).catch(async (e) => {
        try {
          await wacht(700);
          await resend(key, {
            from, to: [to], reply_to: [d.email],
            subject: `\u{26A0} Geen concept gelukt voor ${d.naam}`,
            text: [
              `De aanvraag van ${d.naam} is binnen, maar het conceptantwoord`,
              `kon niet worden geschreven.`, ``,
              `Reden: ${String((e && e.message) || e).slice(0, 300)}`, ``,
              `Beantwoord deze mail om ${d.naam} met de hand te antwoorden.`,
            ].join("\n"),
          }, 2);
        } catch { /* dan houdt het op; de aanvraag zelf is bezorgd */ }
      })
    );
  }

  return json(200, { ok: true, confirmed, reden });
}
