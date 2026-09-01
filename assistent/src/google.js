/* Toegang tot Gmail namens nuno@vuurspuwer.com.
 *
 * We gebruiken een serviceaccount met domeinbrede delegatie, net als bij
 * Search Console. Voordeel boven een gewone OAuth-koppeling: er is geen
 * refresh-token dat kan verlopen en niemand hoeft ooit opnieuw ergens op
 * "toestaan" te klikken. Het serviceaccount tekent zelf een JWT en ruilt
 * die in voor een toegangstoken van een uur. */

const TOKEN_URL = "https://oauth2.googleapis.com/token";

function b64url(buf) {
  const bytes = buf instanceof ArrayBuffer ? new Uint8Array(buf) : buf;
  let s = "";
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function pemNaarBytes(pem) {
  const body = pem.replace(/-----[^-]+-----/g, "").replace(/\s+/g, "");
  const ruw = atob(body);
  const uit = new Uint8Array(ruw.length);
  for (let i = 0; i < ruw.length; i++) uit[i] = ruw.charCodeAt(i);
  return uit.buffer;
}

/* Toegangstoken ophalen. `namens` is het adres dat het serviceaccount mag
   nabootsen; `scopes` bepaalt wat het daarmee mag. */
export async function toegangstoken(saJson, namens, scopes) {
  const sa = typeof saJson === "string" ? JSON.parse(saJson) : saJson;
  const nu = Math.floor(Date.now() / 1000);
  const kop = b64url(new TextEncoder().encode(JSON.stringify({ alg: "RS256", typ: "JWT" })));
  const lijf = b64url(new TextEncoder().encode(JSON.stringify({
    iss: sa.client_email,
    sub: namens,                       // hierdoor handelt het namens Nuno
    scope: scopes.join(" "),
    aud: TOKEN_URL,
    iat: nu,
    exp: nu + 3600,
  })));
  const sleutel = await crypto.subtle.importKey(
    "pkcs8", pemNaarBytes(sa.private_key),
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["sign"]);
  const handtekening = await crypto.subtle.sign(
    "RSASSA-PKCS1-v1_5", sleutel, new TextEncoder().encode(`${kop}.${lijf}`));
  const jwt = `${kop}.${lijf}.${b64url(handtekening)}`;

  const r = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
      assertion: jwt,
    }),
  });
  if (!r.ok) throw new Error(`Google-token ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return (await r.json()).access_token;
}

/* ------------------------------------------------------------------ Gmail */

async function gmail(token, pad, opties = {}) {
  const r = await fetch(`https://gmail.googleapis.com/gmail/v1/users/me${pad}`, {
    ...opties,
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", ...(opties.headers || {}) },
  });
  if (!r.ok) throw new Error(`Gmail ${opties.method || "GET"} ${pad} -> ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return r.json();
}

export async function labelId(token, naam) {
  const { labels } = await gmail(token, "/labels");
  const gevonden = labels.find((l) => l.name === naam);
  if (gevonden) return gevonden.id;
  const nieuw = await gmail(token, "/labels", {
    method: "POST",
    body: JSON.stringify({ name: naam, labelListVisibility: "labelShow", messageListVisibility: "show" }),
  });
  return nieuw.id;
}

export async function zoekBerichten(token, vraag, max = 10) {
  const q = new URLSearchParams({ maxResults: String(max), q: vraag });
  const uit = await gmail(token, `/messages?${q}`);
  return uit.messages || [];
}

/* Een label dat Nuno nooit ziet: niet in de labellijst, niet op het bericht.
   We gebruiken het alleen om te onthouden wat we al bekeken hebben. */
export async function stilLabel(token, naam) {
  const { labels } = await gmail(token, "/labels");
  const bestaat = labels.find((l) => l.name === naam);
  if (bestaat) return bestaat.id;
  const nieuw = await gmail(token, "/labels", {
    method: "POST",
    body: JSON.stringify({ name: naam, labelListVisibility: "labelHide", messageListVisibility: "hide" }),
  });
  return nieuw.id;
}

/* Losse tekst uit een Gmail-bericht halen: het formaat is een boom van
   parts, en de leesbare tekst kan op elk niveau zitten. */
function tekstUit(part, diep = 0) {
  if (!part || diep > 12) return "";
  const mime = part.mimeType || "";
  if (mime === "text/plain" && part.body?.data) return decodeB64(part.body.data);
  if (part.parts) {
    /* multipart/alternative bevat dezelfde mail twee keer: als platte tekst
       en als html. Precies één daarvan nemen, anders staat alles dubbel in
       het verzoek aan Claude. Platte tekst heeft de voorkeur. */
    if (mime === "multipart/alternative") {
      const plat = part.parts.find((p) => (p.mimeType || "") === "text/plain");
      if (plat) { const uit = tekstUit(plat, diep + 1); if (uit) return uit; }
      const html = part.parts.find((p) => (p.mimeType || "").startsWith("text/html"));
      if (html) { const uit = tekstUit(html, diep + 1); if (uit) return uit; }
    }
    const stukken = part.parts.map((p) => tekstUit(p, diep + 1)).filter(Boolean);
    if (stukken.length) return stukken.join("\n");
  }
  if (mime === "text/html" && part.body?.data) {
    return decodeB64(part.body.data)
      .replace(/<style[\s\S]*?<\/style>/gi, "")
      .replace(/<script[\s\S]*?<\/script>/gi, "")
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<\/p>/gi, "\n\n")
      .replace(/<[^>]+>/g, " ")
      .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'")
      .replace(/[ \t]+/g, " ").replace(/\n{3,}/g, "\n\n").trim();
  }
  return "";
}

function decodeB64(d) {
  const s = d.replace(/-/g, "+").replace(/_/g, "/");
  const ruw = atob(s + "=".repeat((4 - (s.length % 4)) % 4));
  const bytes = new Uint8Array(ruw.length);
  for (let i = 0; i < ruw.length; i++) bytes[i] = ruw.charCodeAt(i);
  return new TextDecoder("utf-8").decode(bytes);
}

export async function haalBericht(token, id) {
  const m = await gmail(token, `/messages/${id}?format=full`);
  const kop = {};
  for (const h of m.payload?.headers || []) kop[h.name.toLowerCase()] = h.value;
  return {
    id: m.id,
    threadId: m.threadId,
    van: kop.from || "",
    aan: kop.to || "",
    onderwerp: kop.subject || "(geen onderwerp)",
    messageId: kop["message-id"] || "",
    references: kop.references || "",
    datum: kop.date || "",
    lijstpost: !!(kop["list-unsubscribe"] || kop["list-id"] || kop.precedence),
    auto: /auto-(generated|replied)|no-reply|noreply/i.test(
      (kop["auto-submitted"] || "") + " " + (kop.from || "")),
    tekst: (tekstUit(m.payload) || m.snippet || "").slice(0, 20000),
  };
}

/* Een concept in dezelfde thread. In-Reply-To en References zorgen dat
   Gmail het als antwoord in het bestaande gesprek toont. */
export async function maakConcept(token, bericht, antwoord, vanAdres) {
  const naar = bericht.van;
  const onderwerp = /^re:/i.test(bericht.onderwerp) ? bericht.onderwerp : `Re: ${bericht.onderwerp}`;
  const refs = [bericht.references, bericht.messageId].filter(Boolean).join(" ");
  const regels = [
    `From: ${vanAdres}`,
    `To: ${naar}`,
    `Subject: ${mimeKop(onderwerp)}`,
    bericht.messageId ? `In-Reply-To: ${bericht.messageId}` : null,
    refs ? `References: ${refs}` : null,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
    "",
    b64(antwoord),
  ].filter((r) => r !== null).join("\r\n");

  return gmail(token, "/drafts", {
    method: "POST",
    body: JSON.stringify({ message: { threadId: bericht.threadId, raw: b64url(new TextEncoder().encode(regels)) } }),
  });
}

/* koppen mogen alleen ascii bevatten; de rest gaat als RFC 2047 mee */
function mimeKop(s) {
  return /^[\x20-\x7E]*$/.test(s) ? s : `=?UTF-8?B?${b64(s)}?=`;
}
function b64(s) {
  const bytes = new TextEncoder().encode(s);
  let r = "";
  for (const b of bytes) r += String.fromCharCode(b);
  return btoa(r);
}

export async function verplaatsLabel(token, id, erbij, eraf) {
  return gmail(token, `/messages/${id}/modify`, {
    method: "POST",
    body: JSON.stringify({ addLabelIds: erbij, removeLabelIds: eraf }),
  });
}
