#!/usr/bin/env python3
import hashlib,html,json,re,subprocess
from pathlib import Path
out=Path('brand-footer-evidence');out.mkdir(exist_ok=True)
def guard(name,expected):
    b=Path(name).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected,'Source changed: '+name
guard('index.html','6dc37847b68fbcfc500324647afa622148b3ed46')
guard('build.py','985fc49f9ff0801d1a9d313f8d5b93c8c996192a')
guard('assets/site.css','32ca77385691c65b879e41eae042ec522a1cf2cc')
guard('dist/assets/site.css','3a0fea6500bd4474af5fc18a37b47e9b818964c0')
COPY={
 'nl':['Andere websites van Nuno Art','Naast deze website ontwikkelt Nuno Art ook andere online projecten. Elk heeft een eigen onderwerp en doelgroep.'],
 'en':['Other Nuno Art websites','Alongside this website, Nuno Art develops other online projects, each with its own focus and audience.'],
 'de':['Weitere Websites von Nuno Art','Neben dieser Website entwickelt Nuno Art weitere Onlineprojekte, jeweils mit eigenem Schwerpunkt und eigener Zielgruppe.'],
 'fr':['Autres sites de Nuno Art','En complément de ce site, Nuno Art développe d’autres projets en ligne, chacun avec son propre thème et son public.']}
module='"""Native ownership disclosure used by the existing page builder."""\nimport html,re\nCOPY = '+repr(COPY)+r'''
def render(lang):
    title,intro=COPY.get(lang,COPY['en'])
    links=''.join('<li><a href="https://'+host+'/" rel="nofollow">'+label+'</a></li>' for host,label in [('euroacts.com','EuroActs'),('astronivo.com','AstroNivo'),('eurozena.com','EuroZena')])
    return '<details class="brand-projects" data-brand-projects><summary>'+html.escape(title)+'</summary><p>'+html.escape(intro)+'</p><ul>'+links+'</ul></details>'
def localize(doc):
    if 'data-brand-projects' not in doc:return doc
    language=re.search(r'<html\b[^>]*\blang="([^"]+)"',doc,re.I)
    lang=language.group(1).split('-')[0] if language else 'nl'
    return re.sub(r'<details class="brand-projects" data-brand-projects>.*?</details>',lambda _:render(lang),doc,flags=re.S)
'''
assert not Path('brand_projects.py').exists()
Path('brand_projects.py').write_text(module)
namespace={};exec(compile(module,'brand_projects.py','exec'),namespace)
render,localize=namespace['render'],namespace['localize']
changed=[];rows=[]
names=['index.html']+subprocess.check_output(['git','ls-files','dist'],text=True).splitlines()
for name in names:
    p=Path(name)
    if p.suffix!='.html':continue
    old=p.read_text();matches=list(re.finditer(r'<nav class="foot__network"[^>]*>.*?</nav>',old,re.S))
    if not matches:continue
    assert len(matches)==1,(name,'ambiguous footer')
    match=matches[0]
    for host in ['euroacts.com','eurozena.com','astronivo.com']:
        assert match.group().count('href="https://'+host+'/"')==1,(name,host)
    lang=re.search(r'<html\b[^>]*\blang="([^"]+)"',old,re.I).group(1).split('-')[0]
    assert lang in COPY,(name,lang)
    addition=render(lang)
    new=old[:match.start()]+addition+old[match.end():]
    assert new.replace(addition,match.group(),1)==old,'Non-footer difference'
    new,n=re.subn(r'(/assets/site\.css\?v=[a-zA-Z0-9._-]+)(?=["\'])',r'\1&amp;brands=1',new)
    assert n<=2,(name,'unexpected stylesheet inventory')
    p.write_text(new);changed.append(name)
    rows.append({'path':name,'lang':lang,'old_sha256':hashlib.sha256(old.encode()).hexdigest(),'footer_links':3,'rel':'nofollow'})
assert len(rows)>=187 and all('dist/'+l+'/index.html' in changed for l in ['en','de','fr'])
p=Path('build.py');before=p.read_text();needle='def write(slug, doc):\n'
assert before.count(needle)==1
p.write_text(before.replace(needle,needle+'    from brand_projects import localize as localize_brand_projects\n    doc = localize_brand_projects(doc)\n'))
changed+=['build.py','brand_projects.py']
CSS='''
/* Secondary ownership information: accessible without JavaScript. */
footer .brand-projects{display:block;max-inline-size:44ch;min-inline-size:0;margin-block:8px 0;margin-inline-end:auto;text-align:start;font-size:12px;line-height:1.7;color:var(--ink-dim)}
footer .foot__bar>.brand-projects{flex-basis:100%}
footer .brand-projects>summary{display:list-item;list-style:disclosure-closed inside;cursor:pointer;min-block-size:36px;padding:6px 0;font:inherit;color:inherit}
footer .brand-projects[open]>summary{list-style-type:disclosure-open}
footer .brand-projects>summary:focus-visible{outline:2px solid currentColor;outline-offset:3px}
footer .brand-projects p{margin:8px 0 10px;font:inherit;color:inherit}
footer .brand-projects ul{list-style:none;margin:0;padding:0}
footer .brand-projects li{display:block;margin:0;padding:0}
footer .brand-projects a{display:inline-block;min-block-size:28px;padding:2px 0;font:inherit;color:inherit;text-decoration:underline;text-underline-offset:3px}
'''
for name in ['assets/site.css','dist/assets/site.css']:
    p=Path(name);before=p.read_text();assert '.brand-projects' not in before;p.write_text(before+CSS);changed.append(name)
for lang in COPY:
    test='<html lang="'+lang+'"><footer>'+render('nl')+'</footer>'
    actual=localize(test)
    assert html.escape(COPY[lang][0]) in actual and actual.count('rel="nofollow"')==3
    assert ' open' not in actual and '<script' not in actual
compile(Path('build.py').read_text(),'build.py','exec')
(out/'scope.json').write_text(json.dumps({'pages':len(rows),'languages':list(COPY),'files':changed,'rows':rows,'native_details':True,'only_footer_and_stylesheet_version_changed':True},ensure_ascii=False,indent=2)+'\n')
(out/'paths.json').write_text(json.dumps(changed))
(out/'change.patch').write_text(subprocess.check_output(['git','diff','--','index.html','build.py','assets/site.css'],text=True))
print(json.dumps({'validated_pages':len(rows),'localized_languages':len(COPY)}))
