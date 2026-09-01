/* De storingsroutes: wat gebeurt er als het misgaat? Een aanvraag mag nooit
   stilzwijgend blijven liggen. */
import { generateKeyPairSync } from "node:crypto";
const { privateKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const SA = JSON.stringify({ client_email: "a@b.iam.gserviceaccount.com",
                            private_key: privateKey.export({ type: "pkcs8", format: "pem" }) });
const b64u = (s) => Buffer.from(s, "utf-8").toString("base64url");
const uitslag = []; const t = (n, ok, d = "") => uitslag.push([ok, n, d]);
globalThis.caches = { default: { match: async () => null, put: async () => {} } };

const LABELS = { "Boekingen/Nieuw": "L_NIEUW", "Boekingen/Concept klaar": "L_KLAAR",
                 "Boekingen/Nagekeken worden": "L_FOUT" };

function opstelling({ van = "klant@voorbeeld.nl", claude }) {
  const staat = { concepten: 0, labels: [] };
  globalThis.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes("oauth2")) return { ok: true, json: async () => ({ access_token: "T" }) };
    if (u.includes("llms-full")) return { ok: true, text: async () => "PRIJZEN" };
    if (u.includes("/labels") && !opts.method)
      return { ok: true, json: async () => ({ labels: Object.entries(LABELS).map(([name, id]) => ({ id, name })) }) };
    if (u.includes("/messages?")) return { ok: true, json: async () => ({ messages: [{ id: "m1" }] }) };
    if (u.includes("/messages/m1?format=full")) return { ok: true, json: async () => ({
      id: "m1", threadId: "t1", snippet: "s",
      payload: { mimeType: "text/plain", body: { data: b64u("Hoi, wat kost een show?") },
                 headers: [{ name: "From", value: van }, { name: "Subject", value: "Vraag" },
                           { name: "Message-ID", value: "<x@y>" }] } }) };
    if (u.includes("/drafts")) { staat.concepten++; return { ok: true, json: async () => ({ id: "d" }) }; }
    if (u.includes("/modify")) { staat.labels.push(JSON.parse(opts.body)); return { ok: true, json: async () => ({}) }; }
    if (u.includes("anthropic")) return claude();
    throw new Error("onverwacht: " + u);
  };
  return staat;
}

const mod = await import("./src/index.js");
const env = { GOOGLE_SA_JSON: SA, MAILBOX: "nuno@vuurspuwer.com", ANTHROPIC_API_KEY: "k", TEST_SLEUTEL: "s" };
const draai = async (opts) => {
  const staat = opstelling(opts);
  const r = await (await mod.default.fetch(new Request("https://x/?sleutel=s"), env)).json();
  return { ...staat, r };
};

// 1. Claude valt uit
let s = await draai({ claude: () => ({ ok: false, status: 500, text: async () => "kapot" }) });
t("Claude uitgevallen: geen concept gemaakt", s.concepten === 0);
t("Claude uitgevallen: mail naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.[0] === "L_FOUT");
t("Claude uitgevallen: mail niet in 'Nieuw' blijven hangen", s.labels[0]?.removeLabelIds?.[0] === "L_NIEUW");
t("Claude uitgevallen: ronde meldt 0 concepten", s.r.concepten === 0 && s.r.gezien === 1);

// 2. Claude weigert
s = await draai({ claude: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "refusal", content: [] }) }) });
t("weigering: geen concept", s.concepten === 0);
t("weigering: naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.[0] === "L_FOUT");

// 3. Claude geeft onbruikbare vorm terug
s = await draai({ claude: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn", content: [{ type: "text", text: "zomaar wat tekst zonder tags" }] }) }) });
t("geen antwoord-tags: geen half concept in de inbox", s.concepten === 0);
t("geen antwoord-tags: naar 'nagekeken worden'", s.labels[0]?.addLabelIds?.[0] === "L_FOUT");

// 4. mail van Nuno zelf (bijv. zijn eigen verzonden antwoord)
s = await draai({ van: "Nuno <nuno@vuurspuwer.com>",
                  claude: () => { throw new Error("Claude had niet aangeroepen mogen worden"); } });
t("eigen mail: overgeslagen zonder Claude aan te roepen", s.concepten === 0 && s.r.concepten === 0);
t("eigen mail: netjes uit 'Nieuw' gehaald", s.labels[0]?.removeLabelIds?.[0] === "L_NIEUW");

// 5. gewoon goed
s = await draai({ claude: () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn",
    content: [{ type: "text", text: "<notitie>n</notitie><antwoord>a</antwoord>" }] }) }) });
t("normale gang: concept gemaakt en label verplaatst", s.concepten === 1 && s.labels[0]?.addLabelIds?.[0] === "L_KLAAR");

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, n, d] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${n}${d ? "  (" + d + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
