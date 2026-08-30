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

function rowsHtml(d) {
  const rows = [];
  for (const [key, label] of FIELDS) {
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
function confirmationHtml(d) {
  return `<!doctype html>
<html lang="nl">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Je aanvraag is ontvangen</title></head>
<body style="margin:0;padding:0;background-color:#050302;">
<div style="display:none;max-height:0;overflow:hidden;">Bedankt ${esc(d.naam)} — je aanvraag is in goede orde ontvangen. Ik reageer binnen 24 uur.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#050302;">
<tr><td align="center" style="padding:36px 16px;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
    <tr><td align="center" style="padding:8px 0 28px;">
      <img src="${SITE}/assets/media/logo-mail.png" width="220" alt="NUNO" style="display:block;width:220px;max-width:60%;height:auto;border:0;">
      <div style="font-family:'Courier New',monospace;font-size:10px;letter-spacing:3px;color:#8A7A6D;padding-top:10px;">VUURSPUWER &middot; FAKIR &middot; MENTALIST</div>
    </td></tr>
    <tr><td style="background-color:#0A0705;border:1px solid #2e2113;border-radius:14px;padding:30px 28px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:22px;line-height:1.25;font-weight:bold;color:#FFB020;padding-bottom:14px;">Bedankt, ${esc(d.naam)}! &#128293;</td></tr>
        <tr><td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#C6B29E;padding-bottom:8px;">
          Je aanvraag is in goede orde ontvangen. Ik bekijk hem persoonlijk en je hoort
          <strong style="color:#FFF3D6;">binnen 24 uur</strong> van mij of je datum nog vrij is,
          met een vrijblijvende offerte op maat.
        </td></tr>
        <tr><td style="padding:18px 0 6px;font-family:'Courier New',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#FFB020;">Dit heb je ingevuld</td></tr>
        <tr><td style="border-top:1px solid #2e2113;padding-top:6px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rowsHtml(d)}</table>
        </td></tr>
        <tr><td align="center" style="padding:26px 0 6px;">
          <a href="${WHATSAPP}?text=${encodeURIComponent(`Hallo Nuno, ik heb net een aanvraag gestuurd (${d.naam}). Ik heb een spoedvraag:`)}"
             style="display:inline-block;background-color:#FFB020;background-image:linear-gradient(96deg,#FF4D0A,#FFB020 30%,#FFF3D6 52%,#FFB020 74%,#FF4D0A);color:#170800;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;text-decoration:none;padding:13px 26px;border-radius:999px;">
            &#128172;&nbsp; Spoedvraag? App direct via WhatsApp
          </a>
        </td></tr>
      </table>
    </td></tr>
    <tr><td align="center" style="padding:24px 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.8;color:#8A7A6D;">
      Vuurspuwer Nuno &middot; Nederland, Belgi&euml; &amp; internationaal<br>
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
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rowsHtml(d)}</table>
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

function textVersion(d, intro) {
  const lines = [intro, ""];
  for (const [key, label] of FIELDS) {
    if (d[key]) lines.push(`${label}: ${d[key]}`);
  }
  return lines.join("\n");
}

async function resend(key, payload) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { "Authorization": `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const detail = await r.text().catch(() => "");
    throw new Error(`Resend ${r.status}: ${detail.slice(0, 300)}`);
  }
  return r.json();
}

export async function onRequestPost({ request, env }) {
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
    text: textVersion(d, "Nieuwe aanvraag via vuurspuwer.com"),
  });

  // 2. de bevestiging naar de aanvrager; als die faalt is de aanvraag
  //    zelf al binnen, dus dan geven we alsnog "ok" terug
  let confirmed = true;
  try {
    await resend(key, {
      from,
      to: [d.email],
      reply_to: [to],
      subject: `Bedankt ${d.naam} — je aanvraag bij Vuurspuwer Nuno is ontvangen \u{1F525}`,
      html: confirmationHtml(d),
      text: textVersion(d,
        `Bedankt ${d.naam}! Je aanvraag is in goede orde ontvangen; ik reageer binnen 24 uur. ` +
        `Spoedvraag? App via ${WHATSAPP}. Dit heb je ingevuld:`),
    });
  } catch {
    confirmed = false;
  }

  return json(200, { ok: true, confirmed });
}
