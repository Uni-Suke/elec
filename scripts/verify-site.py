"""Validate the built static site, curriculum links, and numerical examples."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,math,re
root=Path(__file__).resolve().parents[1]
dist=root/'dist'
errors=[]
class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.refs=[];self.ids=set();self.h1=0;self.title=False;self.lang=False;self.description=False;self.missing_alt=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:
   if a['id'] in self.ids: errors.append('Duplicate HTML id: '+a['id'])
   self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if tag=='html':self.lang=a.get('lang')=='ja'
  if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
  if tag=='img' and not a.get('alt'):self.missing_alt+=1
  for key in ('href','src'):
   if a.get(key):self.refs.append(a[key])
pages={}
for f in dist.rglob('*.html'):
 p=Page();p.feed(f.read_text());pages[f.resolve()]=p
 if p.h1!=1:errors.append(f'{f.relative_to(dist)}: expected one h1, got {p.h1}')
 if not p.title or not p.lang or not p.description or p.missing_alt:errors.append(f'{f.relative_to(dist)}: missing document metadata / image alt')
links=0
for f,p in pages.items():
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  target=(dist/path.lstrip('/')) if path.startswith('/') else (f.parent/path if path else f)
  if target.is_dir():target=target/'index.html'
  elif not target.suffix and not target.exists():target=target/'index.html'
  target=target.resolve();links+=1
  if not target.exists():errors.append(f'{f.relative_to(dist)} -> missing {ref}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{f.relative_to(dist)} -> missing anchor {ref}')
index=json.loads((dist/'search-index.json').read_text())
lessons={}
orders=set()
for f in (root/'src/content/lessons').glob('*.md'):
 data=next((e for e in index if e['id']==f.stem),None)
 if data is None:
  errors.append(f'Missing content index entry: {f.stem}');continue
 body=data['body']
 lessons[f.stem]=data
 key=(data['category'],data['order'])
 if key in orders:errors.append(f'Duplicate curriculum order: {key}')
 orders.add(key)
 if len(body)<500:errors.append(f'{f.stem}: article too short')
 if not data['quiz']['question'] or not data['quiz']['answer']:errors.append(f'{f.stem}: missing quiz')
 if data['category']=='experiments':
  for section in ['目的','必要な部品','回路','手順','予想結果','測定結果','うまくいかない']:
   if section not in body:errors.append(f'{f.stem}: missing {section}')
 if f.stem.startswith('design-') and f.stem!='design-process':
  if '<details>' not in body or '要求仕様' not in body or '部品選定とデータシート' not in body:errors.append(f'{f.stem}: missing design structure')
for id,d in lessons.items():
 for related in d['related']:
  if related not in lessons:errors.append(f'{id}: unknown related {related}')
if len(index)!=len(lessons):errors.append('Search index does not include every lesson')
if any(not e['body'] for e in index):errors.append('Search index missing article body')
for term in ['MOSFET','ヒューズ','Hi-Z','キルヒホッフ','BOM','JFET','ファンクションジェネレータ','ADC','デカップリング']:
 if not any(term in (e['title']+e['body']) for e in index):errors.append('Missing searchable topic: '+term)
# Independently recompute the core examples and their boundary conditions.
checks={
 'LED nominal mA':(1000*(5-2)/620,4.84,.01),
 'LED worst-case mA':(1000*(5.25-1.8)/(620*.99),5.62,.01),
 'LED resistor worst W':((5.25-1.8)**2/(620*.99),.0194,.0001),
 'Divider loaded V':(5*5000/(10000+5000),1.667,.001),
 'RC cutoff Hz':(1/(2*math.pi*1000*100e-9),1591.55,.01),
 'RC gain 10 kHz':(1/math.sqrt(1+(10000/(1/(2*math.pi*1000*100e-9)))**2),.157,.001),
 'RC cutoff 1.58k min Hz':(1/(2*math.pi*(1580*1.01+50)*100e-9*1.1),879,1),
 'RC cutoff 1.58k max Hz':(1/(2*math.pi*1580*.99*100e-9*.9),1131,1),
 'BJT bias Ic mA':(100*(1.5625-.7)/(6875+101*1000)*1000,.800,.001),
 'LDO worst loss W':((13.2-3.3)*.3,2.97,.001),
 'ADC input LSB mV':(3.3/4096/3*1000,.269,.001),
 'PWM resistor average W':(.5*5**2/100,.125,.0001),
}
for name,(actual,expected,tol) in checks.items():
 if abs(actual-expected)>tol:errors.append(f'{name}: {actual} != {expected}')
counts={}
for d in lessons.values():counts[d['category']]=counts.get(d['category'],0)+1
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(pages)} HTML pages; {links} internal links/assets/anchors; {len(lessons)} articles; {len(index)} full-text search entries; {len(checks)} calculation checks.')
print('Curriculum:',json.dumps(counts,ensure_ascii=False))
print('SVG diagrams:',len(list((dist/'diagrams').glob('*.svg'))))
