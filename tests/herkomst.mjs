// Herkomst van een aanvraag: welke bron leest functions/api/contact.js af
// uit de verwijzer en de utm-parameters? Vooral de AI-assistenten moeten
// goed gaan: gemini.google.com mag niet als "Google" tellen, en een site als
// claudette.nl niet als Claude. Draaien met: node tests/herkomst.mjs
import { readFileSync } from "node:fs";
const bron = readFileSync(new URL("../functions/api/contact.js", import.meta.url), "utf8");
const blok = bron.slice(bron.indexOf("const AI_BRONNEN"), bron.indexOf("function herkomstRegel"));
const bronNaam = new Function(blok + "\nreturn bronNaam;")();
const C = [
  ["https://chatgpt.com/", {}, "ChatGPT (AI-assistent)"],
  ["", {utm_source:"chatgpt.com"}, "ChatGPT (AI-assistent)"],
  ["https://chat.openai.com/c/123", {}, "ChatGPT (AI-assistent)"],
  ["https://www.perplexity.ai/search?q=x", {}, "Perplexity (AI-assistent)"],
  ["", {utm_source:"perplexity"}, "Perplexity (AI-assistent)"],
  ["https://gemini.google.com/app", {}, "Gemini (AI-assistent)"],
  ["https://copilot.microsoft.com/", {}, "Microsoft Copilot (AI-assistent)"],
  ["https://claude.ai/chat/abc", {}, "Claude (AI-assistent)"],
  ["https://chat.mistral.ai/chat", {}, "Mistral Le Chat (AI-assistent)"],
  ["https://www.google.com/", {}, "Google (organisch)"],
  ["https://www.google.nl/", {}, "Google (organisch)"],
  ["https://www.bing.com/", {}, "Bing"],
  ["", {utm_source:"google", utm_medium:"bedrijfsprofiel"}, "Google-bedrijfsprofiel"],
  ["", {}, "direct of app (getypt, bladwijzer, WhatsApp)"],
  ["https://vuurspuwer.com/fakir-show-inhuren/", {}, "eigen site"],
  ["https://www.instagram.com/", {}, "Instagram"],
  ["https://notgemini.example.com/", {}, "notgemini.example.com"],
  ["https://claudette.nl/", {}, "claudette.nl"],
  ["https://geminifestival.be/", {}, "geminifestival.be"],
  ["", {utm_source:"claude.ai"}, "Claude (AI-assistent)"],
  ["", {utm_source:"copilot.microsoft.com"}, "Microsoft Copilot (AI-assistent)"],
  ["", {utm_source:"newsletter", utm_medium:"email"}, "newsletter (email)"],
  ["https://www.bing.com/chat", {}, "Bing"],
];
let fout = 0;
for (const [v, u, verwacht] of C) {
  const r = bronNaam(v, u);
  const ok = r === verwacht; if (!ok) fout++;
  console.log((ok ? "ok  " : "FOUT") + "  " + (v || JSON.stringify(u)).padEnd(46) + " -> " + r + (ok ? "" : "   (verwacht: " + verwacht + ")"));
}
console.log(fout ? fout + " fout(en)" : "alle " + C.length + " gevallen goed");
process.exit(fout ? 1 : 0);


