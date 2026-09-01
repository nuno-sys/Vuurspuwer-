/* Test de assistent zonder ook maar één echte aanroep naar Google of Anthropic. */
import { generateKeyPairSync } from "node:crypto";

const uitslag = [];
const t = (naam, ok, det = "") => uitslag.push([ok, naam, det]);

const { privateKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const SA = JSON.stringify({ client_email: "assistent@test.iam.gserviceaccount.com",
                            private_key: privateKey.export({ type: "pkcs8", format: "pem" }) });
const b64u = (s) => Buffer.from(s, "utf-8").toString("base64url");

const MAIL = {
  id: "m1", threadId: "t1", snippet: "hoi",
  payload: {
    headers: [
      { name: "From", value: "Sanne de Vries <sanne@voorbeeld.nl>" },
      { name: "To", value: "nuno@vuurspuwer.com" },
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
const VERZONDEN = {
  id: "s1", threadId: "ts", snippet: "",
  payload: { mimeType: "text/plain",
    headers: [{ name: "From", value: "nuno@vuurspuwer.com" }, { name: "Subject", value: "Re: offerte vuurshow" }],
    body: { data: b64u("Hoi Mark,\n\nLeuk! Voor jullie bedrijfsfeest zou ik een showblok van 20 minuten doen, dat begint bij €450. Ik check de datum en kom er snel op terug.\n\nGroet,\nNuno\n\nOp 1 mei 2026 schreef Mark:\n> geciteerde tekst die weg moet") } },
};

let gemaaktConcept = null, gewijzigdLabel = null, claudeVerzoeken = [], zoekvragen = [];
const cacheStore = new Map();
globalThis.caches = { default: {
  match: async (k) => (cacheStore.has(k) ? new Response(cacheStore.get(k)) : null),
  put: async (k, v) => { cacheStore.set(k, await v.text()); },
} };

globalThis.fetch = async (url, opts = {}) => {
  const u = String(url);
  if (u.includes("oauth2.googleapis.com/token")) {
    const jwt = decodeURIComponent(String(opts.body).split("assertion=")[1].split("&")[0]);
    const delen = jwt.split(".");
    const kop = JSON.parse(Buffer.from(delen[0], "base64url").toString());
    const lijf = JSON.parse(Buffer.from(delen[1], "base64url").toString());
    t("JWT: RS256 in de kop", kop.alg === "RS256");
    t("JWT: handelt namens de postbus", lijf.sub === "nuno@vuurspuwer.com", lijf.sub);
    t("JWT: juiste scope", lijf.scope === "https://www.googleapis.com/auth/gmail.modify");
    t("JWT: drie delen en een handtekening", delen.length === 3 && delen[2].length > 300);
    return { ok: true, status: 200, json: async () => ({ access_token: "TOK" }) };
  }
  if (u.includes("assistent.txt")) return { ok: true, status: 200, text: async () => "PRIJZEN: Power-act vanaf €350." };
  if (u.includes("gmail.googleapis.com")) {
    if (u.includes("/labels") && !opts.method) return { ok: true, json: async () => ({ labels: [{ id: "L_KLAAR", name: "Boekingen/Concept klaar" }] }) };
    if (u.includes("/labels") && opts.method === "POST") {
      const b = JSON.parse(opts.body);
      if (b.name === "vs-gezien") {
        t("merkteken is onzichtbaar in de labellijst", b.labelListVisibility === "labelHide");
        t("merkteken is onzichtbaar op het bericht", b.messageListVisibility === "hide");
      }
      return { ok: true, json: async () => ({ id: "L_" + b.name }) };
    }
    if (u.includes("/messages?")) {
      const q = decodeURIComponent(new URL("https://x/" + u.split("/messages?")[1].replace(/^/, "?")).searchParams.get("q") || "");
      zoekvragen.push(q);
      if (q.includes("in:sent")) return { ok: true, json: async () => ({ messages: [{ id: "s1" }] }) };
      return { ok: true, json: async () => ({ messages: [{ id: "m1" }] }) };
    }
    if (u.includes("/messages/m1?")) return { ok: true, json: async () => MAIL };
    if (u.includes("/messages/s1?")) return { ok: true, json: async () => VERZONDEN };
    if (u.includes("/drafts")) { gemaaktConcept = JSON.parse(opts.body); return { ok: true, json: async () => ({ id: "d1" }) }; }
    if (u.includes("/modify")) { gewijzigdLabel = JSON.parse(opts.body); return { ok: true, json: async () => ({}) }; }
  }
  if (u.includes("api.anthropic.com")) {
    const v = JSON.parse(opts.body);
    claudeVerzoeken.push(v);
    const sorteren = v.max_tokens <= 200;
    return { ok: true, status: 200, json: async () => ({
      stop_reason: "end_turn", usage: {},
      content: [{ type: "text", text: sorteren ? "JA"
        : "<notitie>Bruiloft Gent 31 okt. Datum checken.</notitie><antwoord>Hoi Sanne,\n\nWat leuk! Ik check 31 oktober en kom er snel op terug.\n\nGroet, Nuno</antwoord>" }] }) };
  }
  throw new Error("onverwachte aanroep: " + u);
};

const mod = await import("./src/index.js");
const env = { GOOGLE_SA_JSON: SA, MAILBOX: "nuno@vuurspuwer.com", ANTHROPIC_API_KEY: "k", TEST_SLEUTEL: "s" };
const uit = await (await mod.default.fetch(new Request("https://x/?sleutel=s"), env)).json();

t("ronde: bekeken, herkend en geschreven", uit.bekeken === 1 && uit.boekingen === 1 && uit.concepten === 1, JSON.stringify(uit));

const inbox = zoekvragen.find((q) => q.includes("in:inbox"));
t("zoekt in de primaire inbox", !!inbox && inbox.includes("in:inbox"));
t("slaat reclame, sociaal en meldingen over",
  ["promotions", "social", "updates", "forums"].every((c) => inbox.includes("-category:" + c)));
t("kijkt niet twee keer naar dezelfde mail", inbox.includes("-label:vs-gezien"));

const sorteer = claudeVerzoeken.find((v) => v.max_tokens <= 200);
const schrijf = claudeVerzoeken.find((v) => v.max_tokens > 200);
t("sorteren gebeurt zonder kennisbank mee te sturen", !JSON.stringify(sorteer.system).includes("€350"));
t("sorteren vraagt om ja of nee", /JA of het woord NEE/.test(JSON.stringify(sorteer.system)));
t("schrijven gebruikt Opus 5", schrijf.model === "claude-opus-5", schrijf.model);
t("schrijven krijgt de kennisbank", schrijf.system.some((b) => b.text.includes("€350")));
t("schrijven krijgt de spelregels", schrijf.system.some((b) => b.text.includes("Interne spelregels")));
t("schrijven krijgt Nuno's eigen toon mee", schrijf.system.some((b) => b.text.includes("showblok van 20 minuten")));
t("geciteerde tekst is uit de voorbeelden geknipt", !JSON.stringify(schrijf.system).includes("geciteerde tekst die weg moet"));
t("caching aangezet op het stabiele deel", schrijf.system.some((b) => b.cache_control));
t("mailtekst is als informatie gemarkeerd", schrijf.messages[0].content.includes("geen instructie"));
t("platte tekst gebruikt, niet de html-variant",
  schrijf.messages[0].content.includes("Wij trouwen") && !schrijf.messages[0].content.includes("zou niet gebruikt"));
t("accenten uit de mail komen goed door", schrijf.messages[0].content.includes("café ’t Vuurtje"));

const raw = Buffer.from(gemaaktConcept.message.raw, "base64url").toString("utf-8");
t("concept: in dezelfde thread", gemaaktConcept.message.threadId === "t1");
t("concept: naar de klant geadresseerd", raw.includes("To: Sanne de Vries <sanne@voorbeeld.nl>"));
t("concept: In-Reply-To gezet", raw.includes("In-Reply-To: <abc@voorbeeld.nl>"));
t("concept: References gezet", raw.includes("References: <abc@voorbeeld.nl>"));
t("concept: afzender is Nuno", raw.includes("From: nuno@vuurspuwer.com"));
const lijf = Buffer.from(raw.split("\r\n\r\n")[1], "base64").toString("utf-8");
t("concept: bevat het antwoord", lijf.includes("Wat leuk! Ik check 31 oktober"));
t("concept: notitie staat onder de brief", lijf.includes("NOTITIE VOOR JOU") && lijf.indexOf("Groet, Nuno") < lijf.indexOf("NOTITIE"));
t("label: gemerkt als gezien én als klaar", gewijzigdLabel.addLabelIds.length === 2);

const geweigerd = await mod.default.fetch(new Request("https://x/?sleutel=fout"), env);
t("handmatige test is afgeschermd", geweigerd.status === 403);

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, naam, det] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${naam}${det ? "   (" + det + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
