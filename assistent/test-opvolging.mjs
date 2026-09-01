/* De opvolging: wachttijd, opslag, de dagelijkse ronde en de storingsroutes. */
import { wachtDagen, isRijp } from "./opvolging.js";
import { onRequestGet } from "../functions/api/opvolging.js";
import { onRequestPost as contact } from "../functions/api/contact.js";

const uitslag = []; const t = (n, ok, d = "") => uitslag.push([ok, n, d]);
const DAG = 86400000;
const NU = Date.parse("2026-09-01T08:00:00Z");
const overDagen = (n) => new Date(NU + n * DAG).toISOString().slice(0, 10);

/* ---------------------------------------------- wanneer duw je? */
t("evenement over een week: na 2 dagen", wachtDagen(overDagen(7), NU) === 2);
t("evenement over 6 weken: na 3 dagen", wachtDagen(overDagen(42), NU) === 3);
t("evenement over een jaar: na 5 dagen", wachtDagen(overDagen(365), NU) === 5);
t("geen datum ingevuld: na 4 dagen", wachtDagen("", NU) === 4);
t("datum al voorbij: na 2 dagen", wachtDagen(overDagen(-3), NU) === 2);
t("nog te vers: nog niet duwen",
  !isRijp({ datum: overDagen(365), ontvangen: NU - 2 * DAG }, NU));
t("lang genoeg stil: wel duwen",
  isRijp({ datum: overDagen(365), ontvangen: NU - 6 * DAG }, NU));
t("bruiloft volgende week is na 2 dagen al rijp",
  isRijp({ datum: overDagen(7), ontvangen: NU - 2 * DAG }, NU));

/* ---------------------------------------------- nagebootste KV */
function maakKV(inhoud = {}) {
  const m = new Map(Object.entries(inhoud));
  return {
    _m: m,
    list: async ({ prefix }) => ({ keys: [...m.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })) }),
    get: async (k) => m.get(k) ?? null,
    put: async (k, v) => { m.set(k, v); },
    delete: async (k) => { m.delete(k); },
  };
}

function net({ claude, mails }) {
  globalThis.fetch = async (url, opts = {}) => {
    const u = String(url);
    if (u.includes("assistent.txt")) return { ok: true, text: async () => "PRIJZEN" };
    if (u.includes("anthropic")) return claude();
    if (u.includes("resend")) { mails.push(JSON.parse(opts.body)); return { ok: true, json: async () => ({ id: "m" }) }; }
    throw new Error("onverwacht: " + u);
  };
}
const DUWTJE = () => ({ ok: true, status: 200, json: async () => ({ stop_reason: "end_turn",
  content: [{ type: "text", text: "<notitie>Bruiloft over 3 weken, de moeite waard.</notitie><antwoord>Hoi Sanne,\n\nIk hoorde nog niets van je — is de vuurshow nog actueel? Laat maar weten, dan houd ik de datum even vrij.\n\nGroet, Nuno</antwoord>" }] }) });

const RIJ = { naam: "Sanne de Vries", email: "sanne@voorbeeld.nl", datum: overDagen(20),
              act: "Vuurshow", locatie: "Gent", bericht: "Bruiloft, 80 gasten", lang: "nl",
              ontvangen: NU - 4 * DAG };
const ENV = (kv, extra = {}) => ({ OPVOLG: kv, OPVOLG_SLEUTEL: "S", ANTHROPIC_API_KEY: "a",
                                   RESEND_API_KEY: "r", ...extra });
const roep = (env, sleutel = "S") =>
  onRequestGet({ request: new Request("https://vuurspuwer.com/api/opvolging?sleutel=" + sleutel), env });

/* ---------------------------------------------- de dagelijkse ronde */
{
  const mails = []; net({ claude: DUWTJE, mails });
  const kv = maakKV({ "aanvraag:1:a": JSON.stringify(RIJ),
                      "aanvraag:2:b": JSON.stringify({ ...RIJ, naam: "Vers", ontvangen: NU - 1 * DAG }) });
  const uit = await (await roep(ENV(kv))).json();
  t("ronde: alleen de rijpe aanvraag krijgt een duwtje", uit.verstuurd === 1 && uit.bekeken === 2, JSON.stringify(uit));
  t("ronde: één mail, en die gaat naar Nuno", mails.length === 1 && String(mails[0].to) === "nuno@vuurspuwer.com");
  t("ronde: klant staat als reply-to", mails[0].reply_to?.[0] === "sanne@voorbeeld.nl");
  t("ronde: er gaat niets naar de klant", !mails.some((m) => String(m.to).includes("voorbeeld.nl")));
  t("ronde: het duwtje staat erin", mails[0].html.includes("is de vuurshow nog actueel"));
  t("ronde: de notitie staat erin", mails[0].html.includes("de moeite waard"));
  t("ronde: knop met de tekst er al in", /href="mailto:sanne%40voorbeeld\.nl\?subject=.*&amp;body=Hoi%20Sanne/.test(mails[0].html));
  t("ronde: aanvraag daarna weg, dus nooit een tweede duwtje", !kv._m.has("aanvraag:1:a"));
  t("ronde: de verse aanvraag blijft staan", kv._m.has("aanvraag:2:b"));
  t("ronde: mail noemt hoe lang het stil is", mails[0].html.includes("4 dagen geleden"));
}

/* ---------------------------------------------- storingen */
{
  const mails = []; net({ claude: () => ({ ok: false, status: 500, text: async () => "stuk" }), mails });
  const kv = maakKV({ "aanvraag:1:a": JSON.stringify(RIJ) });
  const uit = await (await roep(ENV(kv))).json();
  t("Claude stuk: geen mail, wel geteld", uit.mislukt === 1 && mails.length === 0);
  t("Claude stuk: aanvraag blijft staan voor morgen", kv._m.has("aanvraag:1:a"));
  t("Claude stuk: poging geteld", JSON.parse(kv._m.get("aanvraag:1:a")).pogingen === 1);
  for (let i = 0; i < 2; i++) await roep(ENV(kv));
  t("na drie mislukte ochtenden geeft hij het op", !kv._m.has("aanvraag:1:a"));
}
{
  const mails = []; net({ claude: DUWTJE, mails });
  const kv = maakKV({ "aanvraag:1:a": "geen geldige json" });
  const uit = await (await roep(ENV(kv))).json();
  t("kapotte opslag: overgeslagen en opgeruimd", uit.verstuurd === 0 && !kv._m.has("aanvraag:1:a"));
}

/* ---------------------------------------------- afscherming */
{
  net({ claude: DUWTJE, mails: [] });
  const kv = maakKV({});
  t("zonder sleutel geweigerd", (await roep(ENV(kv), "fout")).status === 403);
  t("zonder KV-koppeling nette melding",
    (await onRequestGet({ request: new Request("https://x/api/opvolging?sleutel=S"),
                          env: { OPVOLG_SLEUTEL: "S", ANTHROPIC_API_KEY: "a", RESEND_API_KEY: "r" } })).status === 503);
}

/* ---------------------------------------------- het formulier bewaart */
{
  const mails = []; net({ claude: DUWTJE, mails });
  const kv = maakKV({});
  const wachtrij = [];
  await contact({
    request: new Request("https://vuurspuwer.com/api/contact", { method: "POST",
      headers: { "Content-Type": "application/json", Origin: "https://vuurspuwer.com" },
      body: JSON.stringify({ naam: "Sanne", email: "sanne@voorbeeld.nl", datum: "2026-10-31",
                             act: "Vuurshow", locatie: "Gent", bericht: "x", lang: "nl" }) }),
    env: { RESEND_API_KEY: "r", OPVOLG: kv }, waitUntil: (p) => wachtrij.push(p) });
  await Promise.allSettled(wachtrij);
  const sleutels = [...kv._m.keys()];
  t("formulier bewaart de aanvraag voor opvolging", sleutels.length === 1 && sleutels[0].startsWith("aanvraag:"));
  const bewaard = JSON.parse(kv._m.get(sleutels[0]));
  t("bewaard: naam, adres, datum en taal", bewaard.naam === "Sanne" && bewaard.datum === "2026-10-31" && bewaard.lang === "nl");
  t("bewaard: met tijdstip", typeof bewaard.ontvangen === "number");
}
{
  const mails = []; net({ claude: DUWTJE, mails });
  const wachtrij = [];
  const res = await contact({
    request: new Request("https://vuurspuwer.com/api/contact", { method: "POST",
      headers: { "Content-Type": "application/json", Origin: "https://vuurspuwer.com" },
      body: JSON.stringify({ naam: "Sanne", email: "sanne@voorbeeld.nl", lang: "nl" }) }),
    env: { RESEND_API_KEY: "r" }, waitUntil: (p) => wachtrij.push(p) });
  await Promise.allSettled(wachtrij);
  t("zonder KV-koppeling werkt het formulier gewoon", res.status === 200 && (await res.json()).ok === true);
}

const fout = uitslag.filter(([ok]) => !ok);
for (const [ok, n, d] of uitslag) console.log(`${ok ? "  ok  " : "  FOUT"}  ${n}${d ? "  (" + d + ")" : ""}`);
console.log(`\n${uitslag.length - fout.length} van ${uitslag.length} controles geslaagd`);
if (fout.length) process.exitCode = 1;
