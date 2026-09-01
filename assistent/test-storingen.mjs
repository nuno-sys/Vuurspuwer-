/* De sorteerstap en de storingsroutes. Een klantmail mag nooit blijven liggen,
   en gewone post mag nooit een concept opleveren. */
import { generateKeyPairSync } from "node:crypto";
const { privateKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const SA = JSON.stringify({ client_email: "a@b.iam.gserviceaccount.com",
                            private_key: privateKey.export({ type: "pkcs8", format: "pem" }) });
const b64u = (s) => Buffer.from(s, "utf-8").toString("base64url");
const uitslag = []; const t = (n, ok, d = "") => uitslag.push([ok, n, d]);
const LABELS = { "Boekingen/Concept klaar": "L_KLAAR", "Boekingen/Nagekeken worden": "L_FOUT", "vs-gezien": "L_GEZIEN" };

function opstelling({ koppen = [], soort = "JA", schrijf, tekst = "Wat kost een vuurshow?" }) {
  const staat = { concepten: 0, labels: [], claude: 0 };
  const cache = new Map();
  globalThis.caches = { default: { match: async (k) => (cache.has(k) ? new Response(cache.get(k)) : null),
                                   put: async (k, v) => { cache.set(k, await v.text()); } } };
  globalThis.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes("oauth2")) return { ok: true, json: async () => ({ access_token: "T" }) };
    if (u.includes("assistent.txt")) return { ok: true, text: async () => "PRIJZEN" };
    if (u.includes("/labels") && !opts.method)
      return { ok: true, json: async () => ({ labels: Object.entries(LABELS).map(([name, id]) => ({ id, name })) }) };
    if (u.includes("/messages?")) {
      const q = decodeURIComponent(u.split("q=")[1] || "");
      if (q.includes("in%3Asent") || q.includes("in:sent")) return { ok: true, json: async () => ({ messages: [] }) };
      return { ok: true, json: async () => ({ messages: [{ id: "m1" }] }) };
    }
    if (u.includes("/messages/m1?")) return { ok: true, json: async () => ({
      id: "m1", threadId: "t1", snippet: "s",
      payload: { mimeType: "text/plain", body: { data: b64u(tekst) },
        headers: [{ name: "From", value: "klant@voorbeeld.nl" }, { name: "Subject", value: "Vraag" },
                  { name: "Message-ID", value: "<x@y>" }, ...koppen] } }) };
    if (u.includes("/drafts")) { staat.concepten++; return { ok: true, json: async () => ({ id: "d" }) }; }
    if (u.includes("/modify")) { staat.labels.push(JSON.parse(opts.body)); return { ok: true, json: async () => ({}) }; }
    if (u.includes("anthropic")) {
      staat.claude++;
      const v = JSON.parse(opts.body);
      if (v.max_tokens <= 200) return { ok: true, status: 200, json: async () => ({ stop_reason: "end_turn", content: [{ type: "text", text: soort }] }) };
      return schrijf();
    }
    throw new Error("onverwacht: " + u);
  };
  return staat;
}
const GOED = () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn",
  content: [{ type: "text", text: "<notitie>n</notitie><antwoord>a</antwoord>" }] }) });

const mod = await import("./src/index.js");
const env = { GOOGLE_SA_JSON: SA, MAILBOX: "nuno@vuurspuwer.com", ANTHROPIC_API_KEY: "k", TEST_SLEUTEL: "s" };
const draai = async (o) => { const s = opstelling(o); const r = await (await mod.default.fetch(new Request("https://x/?sleutel=s"), env)).json(); return { ...s, r }; };

// sorteren
let s = await draai({ soort: "NEE", schrijf: () => { throw new Error("had niet mogen schrijven"); } });
t("geen boekingsvraag: geen concept", s.concepten === 0 && s.r.boekingen === 0);
t("geen boekingsvraag: alleen stil gemerkt, geen zichtbaar label",
  s.labels[0]?.addLabelIds?.length === 1 && s.labels[0].addLabelIds[0] === "L_GEZIEN");
t("geen boekingsvraag: één Claude-aanroep, niet twee", s.claude === 1);

// nieuwsbrief: helemaal geen Claude
s = await draai({ koppen: [{ name: "List-Unsubscribe", value: "<mailto:uit@x.nl>" }],
                  schrijf: () => { throw new Error("nee"); } });
t("nieuwsbrief: overgeslagen zonder Claude te vragen", s.claude === 0 && s.concepten === 0);
t("nieuwsbrief: stil gemerkt", s.labels[0]?.addLabelIds?.[0] === "L_GEZIEN");

// automatische afzender
s = await draai({ koppen: [{ name: "From", value: "no-reply@dienst.nl" }], schrijf: () => { throw new Error("nee"); } });
t("no-reply-afzender: overgeslagen zonder Claude", s.claude === 0);

// eigen post
s = await draai({ koppen: [{ name: "From", value: "Nuno <nuno@vuurspuwer.com>" }], schrijf: () => { throw new Error("nee"); } });
t("eigen verzonden mail: overgeslagen zonder Claude", s.claude === 0);

// storingen bij het schrijven
s = await draai({ schrijf: () => ({ ok: false, status: 500, text: async () => "kapot" }) });
t("schrijven mislukt: geen half concept", s.concepten === 0);
t("schrijven mislukt: naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.includes("L_FOUT"));
t("schrijven mislukt: ook stil gemerkt zodat hij niet blijft rondgaan", s.labels[0]?.addLabelIds?.includes("L_GEZIEN"));

s = await draai({ schrijf: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "refusal", content: [] }) }) });
t("weigering: naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.includes("L_FOUT") && s.concepten === 0);

s = await draai({ schrijf: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn", content: [{ type: "text", text: "geen tags" }] }) }) });
t("onbruikbaar antwoord: naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.includes("L_FOUT") && s.concepten === 0);

// sorteerstap zelf valt uit
s = await draai({ soort: null, schrijf: GOED });
globalThis.fetch = (orig => async (u, o) => (String(u).includes("anthropic") && JSON.parse(o.body).max_tokens <= 200)
  ? { ok: false, status: 503, text: async () => "weg" } : orig(u, o))(globalThis.fetch);
s = await (async () => { const st = opstelling({ soort: "JA", schrijf: GOED });
  globalThis.fetch = (orig => async (u, o) => (String(u).includes("anthropic") && JSON.parse(o.body).max_tokens <= 200)
    ? { ok: false, status: 503, text: async () => "weg" } : orig(u, o))(globalThis.fetch);
  const r = await (await mod.default.fetch(new Request("https://x/?sleutel=s"), env)).json();
  return { ...st, r }; })();
t("sorteren mislukt: mail gaat naar 'nagekeken worden', niet stilzwijgend weg",
  s.labels[0]?.addLabelIds?.includes("L_FOUT"));

// normale gang
s = await draai({ soort: "JA", schrijf: GOED });
t("boekingsvraag: concept gemaakt en beide labels gezet",
  s.concepten === 1 && s.labels[0]?.addLabelIds?.includes("L_KLAAR") && s.labels[0].addLabelIds.includes("L_GEZIEN"));

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, n, d] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${n}${d ? "  (" + d + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
