# AI-zichtbaarheid van vuurspuwer.com

Gemaakt door `tools/ai_zichtbaarheid.py`. Per vraag: ★ = vuurspuwer.com geciteerd als bron, ✓ = Nuno genoemd zonder bronvermelding, ○ = een pagina van vuurspuwer.com is wel opgehaald maar niet aangehaald (de eerste stap), · = niet genoemd, – = niet gemeten of fout.

## Kunnen AI-crawlers de site lezen? (live gecontroleerd op 2026-10-09)

Geen problemen gevonden: robots.txt laat alle zoek- en antwoordcrawlers toe, de site weigert hun user-agent niet, en llms.txt, llms-full.txt en de sitemap zijn bereikbaar.

| crawler | voor | robots.txt | site |
|---|---|---|---|
| OAI-SearchBot | ChatGPT zoeken | toegestaan | doorgelaten |
| ChatGPT-User | ChatGPT opent een pagina | toegestaan | doorgelaten |
| PerplexityBot | Perplexity zoeken | toegestaan | doorgelaten |
| Perplexity-User | Perplexity opent een pagina | toegestaan | doorgelaten |
| Claude-SearchBot | Claude zoeken | toegestaan | doorgelaten |
| Claude-User | Claude opent een pagina | toegestaan | doorgelaten |
| Googlebot | Google, AI Overviews en Gemini | toegestaan | doorgelaten |
| Bingbot | Bing, Copilot en deels ChatGPT | toegestaan | doorgelaten |
| Applebot | Apple / Siri | toegestaan | doorgelaten |
| Google-Extended | Gemini-training (geen zoekverkeer) | toegestaan | – |
| GPTBot | OpenAI-training (geen zoekverkeer) | toegestaan | doorgelaten |
| ClaudeBot | Anthropic-training (geen zoekverkeer) | toegestaan | doorgelaten |

*Site* test alleen de user-agent vanaf een GitHub-server; de echte crawlers komen van hun eigen adressen. Een weigering is dus een probleem, 'doorgelaten' is een goede aanwijzing maar geen garantie.

Nog geen metingen. Zet minstens één API-sleutel als GitHub-geheim (zie de uitleg in `tools/ai_zichtbaarheid.py`) en start de Action *AI-zichtbaarheid*.

