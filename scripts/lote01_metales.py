from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
from PIL import Image, ImageOps
import json,re,html,io,time

root=Path(__file__).resolve().parents[1]
destroot=root/'assets/biblioteca/metales'
specs=[
('subbases','Aluminio','aluminio.jpg','aluminium cans scrap metal','alum,can'),
('subbases','Cobre','cobre.jpg','copper wire scrap metal','copper,wire,cobre'),
('subbases','Hierro y acero','hierro-y-acero.jpg','steel iron beams scrap','steel,iron,beam'),
('subbases','Acero inoxidable','acero-inoxidable.jpg','stainless steel metal scrap','stainless,steel'),
('subbases','Bronce, latón y otros','bronce-laton-y-otros.jpg','brass fittings metal scrap','brass,bronze,fitting'),
('productos','Latas compactadas','latas-compactadas.jpg','crushed aluminum beverage cans','alum,can'),
('productos','Lingotes industriales','lingotes-industriales.jpg','aluminium metal ingots','ingot,alum'),
('productos','Perfiles de aluminio','perfiles-de-aluminio.jpg','aluminium extrusion profile','extrusion,alum,profile'),
('productos','Cable separado','cable-separado.jpg','copper wire coil metal','copper,wire,cable'),
('productos','Cobre clasificado','cobre-clasificado.jpg','copper scrap metal pieces','copper,cobre'),
]
CURATED={"Aluminio":"Aluminium for recycling.jpg","Cobre":"Copper wires.JPG","Hierro y acero":"Steel beams stacked beside a building in a construction yard.jpg","Acero inoxidable":"Steel Scrap Compacted.JPG","Bronce, latón y otros":"Close-up of brass plumbing valves with red handles in a home installation.jpg","Latas compactadas":"Compressed aluminium cans.jpg","Lingotes industriales":"Ingots.JPG","Perfiles de aluminio":"Novacel aluminium profiles protection.jpg","Cable separado":"Large coil.jpg","Cobre clasificado":"Alambre de cobre.JPG"}
def get(url):
 req=Request(url,headers={'User-Agent':'EcorecycleReferenceGallery/1.0 (fundacionecopiensaevolution@gmail.com)'})
 with urlopen(req,timeout=35) as r:return r.read()
def plain(v):return re.sub('<[^>]*>','',html.unescape(v))
previous={}
mf=destroot/'manifest.json'
if mf.exists():
 try:previous={(v['tipo'],v['nombre']):v for v in json.loads(mf.read_text('utf-8')).get('imagenes',[])}
 except Exception:pass
records=[]
for idx,(kind,label,filename,query,required) in enumerate(specs,1):
 target=destroot/kind/filename
 target.parent.mkdir(parents=True,exist_ok=True)
 if label in CURATED:
  try:
   p={'action':'query','titles':'File:'+CURATED[label],'prop':'imageinfo','iiprop':'url|mime|size|extmetadata','iiurlwidth':900,'format':'json'}
   pages=json.loads(get('https://commons.wikimedia.org/w/api.php?'+urlencode(p))).get('query',{}).get('pages',{})
   info=next(iter(pages.values())).get('imageinfo',[None])[0]
   if info and info.get('mime')=='image/jpeg':
    meta=info.get('extmetadata',{})
    lic=plain(meta.get('LicenseShortName',{}).get('value',''))
    if re.search(r'CC BY|CC-BY|CC0|Public domain',lic,re.I):
     im=Image.open(io.BytesIO(get(info.get('thumburl') or info['url']))).convert('RGB')
     im=ImageOps.fit(im,(900,560),Image.Resampling.LANCZOS)
     im.save(target,'JPEG',quality=83,optimize=True,progressive=True)
     rec={'numero':idx,'tipo':kind,'nombre':label,'archivo':str(target.relative_to(root)),'fuente':info.get('descriptionurl',''),'licencia':lic,'autor':plain(meta.get('Artist',{}).get('value','')),'titulo':'File:'+CURATED[label],'origen':'Foto externa seleccionada por correspondencia de material'}
     records.append(rec);print('CURADA',label,rec['titulo'],flush=True)
     continue
  except Exception as e:print('NO CURADA',label,str(e)[:120],flush=True)
 if target.exists() and (kind,label) in previous:
  records.append(previous[(kind,label)]);continue
 success=None
 terms=required.split(',')
 for q in [query,query.split(' scrap')[0],label+' recycling',query.split(' ')[0]]:
  params={'action':'query','generator':'search','gsrsearch':q,'gsrnamespace':6,'gsrlimit':35,'prop':'imageinfo','iiprop':'url|mime|size|extmetadata','iiurlwidth':900,'format':'json'}
  try:
   pages=json.loads(get('https://commons.wikimedia.org/w/api.php?'+urlencode(params))).get('query',{}).get('pages',{})
  except Exception as e:print('Error',q,str(e)[:100]);continue
  for page in sorted(pages.values(),key=lambda o:o.get('index',999)):
   info=(page.get('imageinfo') or [None])[0]
   if not info or info.get('mime')!='image/jpeg':continue
   title=page.get('title','').lower()
   if not any(x in title for x in terms):continue
   if info.get('width',0)<300 or info.get('height',0)<190:continue
   meta=info.get('extmetadata',{})
   license=plain(meta.get('LicenseShortName',{}).get('value',''))
   if not re.search(r'CC BY|CC-BY|CC0|Public domain',license,re.I):continue
   try:
    im=Image.open(io.BytesIO(get(info.get('thumburl') or info['url']))).convert('RGB')
    im=ImageOps.fit(im,(900,560),Image.Resampling.LANCZOS)
    im.save(target,'JPEG',quality=82,optimize=True,progressive=True)
    success={'numero':idx,'tipo':kind,'nombre':label,'archivo':str(target.relative_to(root)),'fuente':info.get('descriptionurl',''),'licencia':license,'autor':plain(meta.get('Artist',{}).get('value','')),'titulo':page.get('title',''),'origen':'Foto de referencia externa, no evidencia institucional'}
    break
   except Exception as e:print('No se pudo procesar',label,str(e)[:90])
  if success:break
 if success:print('OK',label,success['titulo'],flush=True)
 else:
  success={'numero':idx,'tipo':kind,'nombre':label,'archivo':'','estado':'Foto específica pendiente'}
  print('PENDIENTE',label,flush=True)
 records.append(success)
 time.sleep(.2)
destroot.mkdir(parents=True,exist_ok=True)
mf.write_text(json.dumps({'lote':1,'material':'Metales','imagenes':records},ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',sum(bool(x['archivo']) for x in records),'de 10')
