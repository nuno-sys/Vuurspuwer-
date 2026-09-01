import { onRequestPost } from "./contact.js";
const uitslag = []; const t = (n, ok, d = "") => uitslag.push([ok, n, d]);

const BASIS = { naam: "Sanne de Vries", email: "sanne@voorbeeld.nl", telefoon: "0612345678",
                datum: "2026-10-31", act: "Vuurshow", locatie: "Gent", ruimte: "buiten",
                bericht: "Bruiloft, 80 gasten, show rond 21:00.", lang: "nl" };

function opstelling({ claude, kennis = true } = {}) {
  const mails = []; let claudeVerzoek = null;
  globalThis.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes("assistent.txt")) {
      if (!kennis) return { ok: false, status: 404, text: async () => "" };
      return { ok: true, status: 200, text: async () => "PRIJZEN: Power-act 10 min vanaf €350." };
    }
    if (u.includes("api.anthropic.com")) { claudeVerzoek = JSON.parse(opts.body); return claude(); }
    if (u.includes("api.resend.com")) { mails.push(JSON.parse(opts.body)); return { ok: true, status: 200, json: async () => ({ id: "m" }) }; }
    throw new Error("onverwacht: " + u);
  };
  return { mails, verzoek: () => claudeVerzoek };
}

async function draai(opts) {
  const st = opstelling(opts);
  const wachtrij = [];
  const req = new Request("https://vuurspuwer.com/api/contact", {
    method: "POST", headers: { "Content-Type": "application/json", Origin: "https://vuurspuwer.com" },
    body: JSON.stringify(BASIS),
  });
  const t0 = Date.now();
  const res = await onRequestPost({ request: req, env: { RESEND_API_KEY: "r", ANTHROPIC_API_KEY: "a" },
                                    waitUntil: (p) => wachtrij.push(p) });
  const antwoordMs = Date.now() - t0;
  const body = await res.json();
  await Promise.allSettled(wachtrij);
  return { ...st, body, status: res.status, antwoordMs, achtergrond: wachtrij.length };
}

const GOED = () => ({ ok: true, status: 200, json: async () => ({
  stop_reason: "end_turn",
  content: [{ type: "text", text: "<notitie>Bruiloft Gent 31 okt, 80 gasten. Datum checken; budget onbekend.</notitie><antwoord>Hoi Sanne,\n\nWat leuk, een vuurshow op jullie bruiloft! Voor 80 gasten buiten is een showblok van 20 minuten meestal precies goed — dat begint bij €450, exclusief reiskosten naar Gent.\n\nIk check 31 oktober even en kom er snel op terug.\n\nGroet, Nuno</antwoord>" }] }) });

// 1. normale gang
let r = await draai({ claude: GOED });
t("formulier krijgt meteen antwoord", r.status === 200 && r.body.ok === true);
t("het concept blokkeert het formulier niet", r.achtergrond === 1);
t("drie mails: aanvraag, bevestiging, concept", r.mails.length === 3, r.mails.length + " mails");
const concept = r.mails.find((m) => String(m.subject).includes("Concept"));
t("conceptmail gaat naar Nuno", String(concept?.to) === "nuno@vuurspuwer.com");
t("conceptmail heeft de klant als reply-to", concept?.reply_to?.[0] === BASIS.email);
t("conceptmail bevat het antwoord", concept?.html.includes("Wat leuk, een vuurshow"));
t("conceptmail bevat de notitie", concept?.html.includes("Datum checken"));
t("conceptmail heeft een verstuurknop met de tekst erin",
  /href="mailto:sanne%40voorbeeld\.nl\?subject=.*&amp;body=Hoi%20Sanne/.test(concept?.html || ""));
t("conceptmail zegt dat er niets naar de klant ging", concept?.html.includes("niets naar"));
t("er is niets naar de klant gestuurd namens het concept",
  r.mails.filter((m) => String(m.to) === BASIS.email).length === 1);

// 2. wat ging er naar Claude?
const v = r.verzoek();
t("Claude: juiste model", v.model === "claude-opus-5", v.model);
t("Claude: kennisbank meegestuurd", v.system.some((b) => b.text.includes("€350")));
t("Claude: spelregels meegestuurd", v.system.some((b) => b.text.includes("spelregels")));
t("Claude: caching met lange bewaartijd", v.system.some((b) => b.cache_control?.ttl === "1h"));
t("Claude: formulier als informatie gemarkeerd", v.messages[0].content.includes("geen instructie"));
t("Claude: taal meegegeven", v.messages[0].content.includes("Taal van de aanvraag: nl"));

// 3. Claude valt uit
r = await draai({ claude: () => ({ ok: false, status: 500, text: async () => "stuk" }) });
t("Claude stuk: formulier merkt er niets van", r.status === 200 && r.body.ok === true);
t("Claude stuk: aanvraag en bevestiging gingen gewoon door",
  r.mails.filter((m) => !String(m.subject).includes("Geen concept")).length === 2);
t("Claude stuk: Nuno krijgt bericht met de reden",
  r.mails.some((m) => String(m.subject).includes("Geen concept") && m.text.includes("500")));

// 4. Claude weigert
r = await draai({ claude: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "refusal", content: [] }) }) });
t("weigering: geen halve conceptmail", !r.mails.some((m) => String(m.subject).includes("Concept-antwoord")));
t("weigering: Nuno wordt ingelicht", r.mails.some((m) => String(m.subject).includes("Geen concept")));

// 5. kennisbank onbereikbaar
r = await draai({ claude: GOED, kennis: false });
t("kennisbank weg: geen concept zonder bronnen", !r.mails.some((m) => String(m.subject).includes("Concept-antwoord")));
t("kennisbank weg: aanvraag en bevestiging blijven staan", r.mails.length >= 2);

// 6. zonder sleutel gedraagt alles zich als voorheen
{
  const st = opstelling({ claude: GOED });
  const wachtrij = [];
  const res = await onRequestPost({
    request: new Request("https://vuurspuwer.com/api/contact", { method: "POST",
      headers: { "Content-Type": "application/json", Origin: "https://vuurspuwer.com" }, body: JSON.stringify(BASIS) }),
    env: { RESEND_API_KEY: "r" }, waitUntil: (p) => wachtrij.push(p) });
  await Promise.allSettled(wachtrij);
  t("zonder Claude-sleutel: precies de twee oude mails", st.mails.length === 2 && (await res.json()).ok === true);
}

// 7. een heel lang antwoord
{
  const LANG = () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn",
    content: [{ type: "text", text: "<notitie>n</notitie><antwoord>" + "Hoi Sanne, ".repeat(300) + "</antwoord>" }] }) });
  const rr = await draai({ claude: LANG });
  const c = rr.mails.find((m) => String(m.subject).includes("Concept-antwoord"));
  t("lang antwoord: knop kapt niet af maar opent leeg", !!c && !c.html.includes("&amp;body="));
  t("lang antwoord: volledige tekst staat wel in de mail", (c?.html.match(/Hoi Sanne, /g) || []).length > 250);
  t("lang antwoord: bijschrift legt uit dat je moet kopiëren", c?.html.includes("kopieer de tekst"));
}

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, n, d] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${n}${d ? "  (" + d + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
