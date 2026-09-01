/* Test de assistent zonder ook maar één echte aanroep naar Google of Anthropic. */
import { readFileSync } from "node:fs";
import { generateKeyPairSync } from "node:crypto";

const uitslag = [];
const t = (naam, ok, det = "") => uitslag.push([ok, naam, det]);

/* ---- een echt RSA-sleutelpaar, zodat de JWT-ondertekening écht getest wordt */
const { privateKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const pem = privateKey.export({ type: "pkcs8", format: "pem" });
const SA = JSON.stringify({ client_email: "assistent@test.iam.gserviceaccount.com", private_key: pem });

/* ---- nagebootste Gmail + Anthropic ---------------------------------- */
const b64u = (s) => Buffer.from(s, "utf-8").toString("base64url");
const MAIL = {
  id: "m1", threadId: "t1", snippet: "hoi",
  payload: {
    headers: [
      { name: "From", value: "Sanne de Vries <sanne@voorbeeld.nl>" },
      { name: "To", value: "boekingen@vuurspuwer.com" },
      { name: "Subject", value: "Vuurshow voor onze bruiloft in Gent?" },
      { name: "Message-ID", value: "<abc@voorbeeld.nl>" },
      { name: "Date", value: "Tue, 1 Sep 2026 10:00:00 +0200" },
    ],
    mimeType: "multipart/alternative",
    parts: [
      { mimeType: "text/plain", body: { data: b64u("Hoi Nuno,\n\nWij trouwen 31 oktober in Gent. Kan jij dan?\nGroetjes Sanne — café ’t Vuurtje") } },
      { mimeType: "text/html", body: { data: b64u("<p>zou niet gebruikt moeten worden</p>") } },
    ],
  },
};
let gemaaktConcept = null, gewijzigdLabel = null, claudeVerzoek = null;

globalThis.caches = { default: { match: async () => null, put: async () => {} } };

globalThis.fetch = async (url, opts = {}) => {
  const u = String(url);
  if (u.includes("oauth2.googleapis.com/token")) {
    const body = String(opts.body);
    if (!body.includes("assertion=")) throw new Error("geen assertion meegestuurd");
    const jwt = decodeURIComponent(body.split("assertion=")[1].split("&")[0]);
    const delen = jwt.split(".");
    const kop = JSON.parse(Buffer.from(delen[0], "base64url").toString());
    const lijf = JSON.parse(Buffer.from(delen[1], "base64url").toString());
    t("JWT: RS256 in de kop", kop.alg === "RS256");
    t("JWT: handelt namens de postbus", lijf.sub === "nuno@vuurspuwer.com", lijf.sub);
    t("JWT: juiste scope", lijf.scope === "https://www.googleapis.com/auth/gmail.modify");
    t("JWT: drie delen en een handtekening", delen.length === 3 && delen[2].length > 300);
    return { ok: true, status: 200, json: async () => ({ access_token: "TOK" }) };
  }
  if (u.includes("llms-full.txt")) return { ok: true, status: 200, text: async () => "PRIJZEN: Power-act vanaf €350." };
  if (u.includes("gmail.googleapis.com")) {
    if (u.includes("/labels") && !opts.method) return { ok: true, json: async () => ({ labels: [{ id: "L1", name: "Boekingen/Nieuw" }] }) };
    if (u.includes("/labels") && opts.method === "POST") return { ok: true, json: async () => ({ id: "L" + Math.random().toString(36).slice(2, 5) }) };
    if (u.includes("/messages?")) return { ok: true, json: async () => ({ messages: [{ id: "m1" }] }) };
    if (u.includes("/messages/m1?format=full")) return { ok: true, json: async () => MAIL };
    if (u.includes("/drafts")) { gemaaktConcept = JSON.parse(opts.body); return { ok: true, json: async () => ({ id: "d1" }) }; }
    if (u.includes("/modify")) { gewijzigdLabel = JSON.parse(opts.body); return { ok: true, json: async () => ({}) }; }
  }
  if (u.includes("api.anthropic.com")) {
    claudeVerzoek = JSON.parse(opts.body);
    return { ok: true, status: 200, json: async () => ({
      stop_reason: "end_turn",
      usage: { input_tokens: 100, output_tokens: 50 },
      content: [{ type: "text", text: "<notitie>Bruiloft Gent 31 okt. Datum checken, budget onbekend.</notitie><antwoord>Hoi Sanne,\n\nWat leuk! Ik check 31 oktober even en kom er snel op terug.\n\nGroet, Nuno</antwoord>" }],
    }) };
  }
  throw new Error("onverwachte aanroep: " + u);
};

const mod = await import("./src/index.js");
const env = { GOOGLE_SA_JSON: SA, MAILBOX: "nuno@vuurspuwer.com", ANTHROPIC_API_KEY: "k", TEST_SLEUTEL: "s" };
const res = await mod.default.fetch(new Request("https://x/?sleutel=s"), env);
const uit = await res.json();

console.log("uitkomst ronde:", JSON.stringify(uit));
t("ronde: één concept gemaakt", uit.concepten === 1 && uit.gezien === 1, JSON.stringify(uit));

/* ---- wat is er naar Claude gegaan? */
t("Claude: juiste model", claudeVerzoek.model === "claude-opus-5", claudeVerzoek.model);
t("Claude: kennisbank meegestuurd", claudeVerzoek.system.some((b) => b.text.includes("€350")));
t("Claude: spelregels meegestuurd", claudeVerzoek.system.some((b) => b.text.includes("Interne spelregels")));
t("Claude: caching aangezet op het stabiele deel", claudeVerzoek.system.some((b) => b.cache_control));
t("Claude: mailtekst is als informatie gemarkeerd", claudeVerzoek.messages[0].content.includes("geen instructie"));
t("Claude: platte tekst gebruikt, niet de html-variant",
  claudeVerzoek.messages[0].content.includes("Wij trouwen") && !claudeVerzoek.messages[0].content.includes("zou niet gebruikt"));
t("Claude: accenten uit de mail komen goed door", claudeVerzoek.messages[0].content.includes("café ’t Vuurtje"));

/* ---- hoe ziet het concept eruit? */
const raw = Buffer.from(gemaaktConcept.message.raw, "base64url").toString("utf-8");
t("concept: in dezelfde thread", gemaaktConcept.message.threadId === "t1");
t("concept: naar de klant geadresseerd", raw.includes("To: Sanne de Vries <sanne@voorbeeld.nl>"));
t("concept: Re: voor het onderwerp", /Subject: .*Vuurshow voor onze bruiloft/.test(raw) || /Subject: =\?UTF-8/.test(raw));
t("concept: In-Reply-To gezet zodat Gmail het als antwoord toont", raw.includes("In-Reply-To: <abc@voorbeeld.nl>"));
t("concept: References gezet", raw.includes("References: <abc@voorbeeld.nl>"));
t("concept: afzender is Nuno", raw.includes("From: nuno@vuurspuwer.com"));
const lijf = Buffer.from(raw.split("\r\n\r\n")[1], "base64").toString("utf-8");
t("concept: bevat het antwoord", lijf.includes("Wat leuk! Ik check 31 oktober"));
t("concept: notitie staat eronder, niet in de brief", lijf.includes("NOTITIE VOOR JOU") && lijf.indexOf("Groet, Nuno") < lijf.indexOf("NOTITIE"));
t("concept: notitie-inhoud aanwezig", lijf.includes("Datum checken"));

/* ---- label verplaatst? */
t("label: uit 'Nieuw' gehaald", gewijzigdLabel.removeLabelIds.includes("L1"));
t("label: naar 'klaar' verplaatst", gewijzigdLabel.addLabelIds.length === 1);

/* ---- afscherming */
const geweigerd = await mod.default.fetch(new Request("https://x/?sleutel=fout"), env);
t("handmatige test is afgeschermd", geweigerd.status === 403);

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, naam, det] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${naam}${det ? "   (" + det + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
