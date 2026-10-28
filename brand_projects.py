"""Native ownership disclosure used by the existing page builder."""
import html,re
COPY = {'nl': ['Andere websites van Nuno Art', 'Naast deze website ontwikkelt Nuno Art ook andere online projecten. Elk heeft een eigen onderwerp en doelgroep.'], 'en': ['Other Nuno Art websites', 'Alongside this website, Nuno Art develops other online projects, each with its own focus and audience.'], 'de': ['Weitere Websites von Nuno Art', 'Neben dieser Website entwickelt Nuno Art weitere Onlineprojekte, jeweils mit eigenem Schwerpunkt und eigener Zielgruppe.'], 'fr': ['Autres sites de Nuno Art', 'En complément de ce site, Nuno Art développe d’autres projets en ligne, chacun avec son propre thème et son public.']}
def render(lang):
    title,intro=COPY.get(lang,COPY['en'])
    links=''.join('<li><a href="https://'+host+'/" rel="nofollow">'+label+'</a></li>' for host,label in [('euroacts.com','EuroActs'),('astronivo.com','AstroNivo'),('eurozena.com','EuroZena')])
    return '<details class="brand-projects" data-brand-projects><summary>'+html.escape(title)+'</summary><p>'+html.escape(intro)+'</p><ul>'+links+'</ul></details>'
def localize(doc):
    if 'data-brand-projects' not in doc:return doc
    language=re.search(r'<html\b[^>]*\blang="([^"]+)"',doc,re.I)
    lang=language.group(1).split('-')[0] if language else 'nl'
    return re.sub(r'<details class="brand-projects" data-brand-projects>.*?</details>',lambda _:render(lang),doc,flags=re.S)
