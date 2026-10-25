#!/usr/bin/env python3
"""Build a public, attributed photo library from Wikimedia Commons only.
Do not include any private project document, enterprise formulas or raw macro-plan.
"""
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import json,re,time,html,io,sys
from PIL import Image,ImageOps

BASE=Path(__file__).resolve().parents[1]
SITE=BASE/"index.html"
JS=(BASE/"fotos-catalogo.js").read_text(encoding="utf-8")
data=json.loads(re.search(r"const DATA=(\[.*?\]);\nlet active=",SITE.read_text(encoding="utf-8"),re.S).group(1))
m=re.search(r"const topics=(\{.*?\});\nconst memo=",JS,re.S)
if not m: raise RuntimeError("Missing public Wikimedia search topics.")
dict_text=re.sub(r'(?m)(\b[a-z_]+):',r'"\1":',m.group(1))
topics=json.loads(dict_text)
output=BASE/"assets"/"fotos"
output.mkdir(parents=True,exist_ok=True)
catalog=[]
success=0
def slug(s):
 s=s.lower()
 import unicodedata
 s=''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
 return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:100]
def ask(url):
 request=Request(url,headers={"User-Agent":"EcorecycleOpenEducationalGallery/1.0 (contact: fundacionecopiensaevolution@gmail.com)","Accept":"application/json"})
 with urlopen(request,timeout=30) as f: return f.read()
def search_photo(term):
 opts={"action":"query","generator":"search","gsrsearch":term,"gsrnamespace":6,"gsrlimit":12,"prop":"imageinfo","iiprop":"url|mime|extmetadata","iiurlwidth":900,"format":"json"}
 r=json.loads(ask("https://commons.wikimedia.org/w/api.php?"+urlencode(opts)))
 pages=sorted((r.get("query") or {}).get("pages",{}).values(),key=lambda x:x.get("index",999))
 for item in pages:
  info=(item.get("imageinfo") or [None])[0]
  if not info or info.get("mime")!="image/jpeg":continue
  ex=info.get("extmetadata") or {}
  license=html.unescape((ex.get("LicenseShortName") or {}).get("value",""))
  if not re.search(r'CC0|Public domain|CC BY|CC-BY',license,re.I):continue
  return {"thumb":info.get("thumburl") or info.get("url"),"source":info.get("descriptionurl") or "", "license":license, "creator":re.sub("<[^>]+>","",(ex.get("Artist") or {}).get("value","")), "title":item.get("title","")}
 return None
for cat in data:
 sec=cat["id"];terms=topics.get(sec,[])
 for ix,sub in enumerate(cat["b"]):
  term=terms[ix] if ix<len(terms) else sub[0]+" recycling"
  name=slug(sub[0])
  dest=output/sec/(name+".jpg");dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():
   catalog.append({"material":sec,"subbase":sub[0],"filename":str(dest.relative_to(BASE)),"cached":True})
   continue
  try:
   item=search_photo(term)
   if not item:continue
   raw=ask(item["thumb"])
   im=Image.open(io.BytesIO(raw)).convert("RGB")
   if im.width<260 or im.height<170:continue
   # Full canvas visible; cropped only for consistent card covers.
   im=ImageOps.fit(im,(768,480),Image.Resampling.LANCZOS,centering=(.5,.5))
   im.save(dest,"JPEG",quality=81,optimize=True,progressive=True)
   catalog.append({"material":sec,"subbase":sub[0],"filename":str(dest.relative_to(BASE)),"source":item["source"],"license":item["license"],"creator":item["creator"],"original_title":item["title"],"query":term})
   success+=1
   print("PHOTO",sec,sub[0],flush=True)
  except Exception as err:print("SKIP",sec,sub[0],str(err)[:100],file=sys.stderr,flush=True)
  time.sleep(.35)
(output/"creditos.json").write_text(json.dumps({"nota":"Fotografías externas ilustrativas; no documentan operaciones propias de la Fundación.","fuentes":catalog},ensure_ascii=False,indent=2),encoding="utf-8")
print("DONE saved",success,"total",len(catalog))
