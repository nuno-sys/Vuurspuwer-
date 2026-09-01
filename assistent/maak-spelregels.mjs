/* spelregels.md -> src/spelregels.js
   Zo bewerkt Nuno gewoon markdown, en kan zowel de Worker als de test het
   inlezen zonder dat er een tweede versie van dezelfde tekst bestaat. */
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const hier = dirname(fileURLToPath(import.meta.url));
const tekst = readFileSync(join(hier, "spelregels.md"), "utf-8");
writeFileSync(join(hier, "src", "spelregels.js"),
  "/* Automatisch gemaakt uit spelregels.md — niet met de hand bewerken. */\n" +
  "export default " + JSON.stringify(tekst) + ";\n");
console.log(`spelregels.js gemaakt (${tekst.length} tekens)`);
