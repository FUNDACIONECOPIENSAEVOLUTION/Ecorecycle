#!/usr/bin/env python3
"""Auditoría pública ECORECYCLE: inventario por nodo y lista de creación.
Nunca incluir archivos del proyecto macro ni datos internos.
"""
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone
import json, csv, re

root=Path(__file__).resolve().parents[1]
main=(root/"index.html").read_text(encoding="utf-8")
data=json.loads(re.search(r"const DATA=(\[.*?\]);\nlet active=",main,re.S).group(1))
def read_manifest(rel):
 p=root/rel
 if p.is_file():
  try:return json.loads(p.read_text(encoding="utf-8")).get("imagenes",[])
  except Exception:return []
 return []
credits=[]
f=root/"assets/fotos/creditos.json"
if f.exists():credits=json.loads(f.read_text(encoding="utf-8")).get("fuentes",[])
rpack=read_manifest("assets/biblioteca/reciclables-secos/manifest.json")
mpack=read_manifest("assets/biblioteca/metales/manifest.json")
opack=read_manifest("assets/biblioteca/organicos/manifest.json")
river=read_manifest("assets/biblioteca/rio/manifest.json")
source_files={p.as_posix().removeprefix(root.as_posix()+"/") for p in root.rglob("*") if p.is_file()}
rows=[]
def clean(s):return str(s).rstrip("*").strip()
def actual(path):return bool(path and path in source_files and (root/path).stat().st_size>1024)
def add(branch,cat,sub,name,typ,ref=None,quality="pendiente",source=""):
 path=ref or ""
 status="VINCULADA_REVISAR" if actual(path) else ("ARCHIVO_FALTANTE" if path else "PENDIENTE_CREAR")
 rows.append({"linea":branch,"categoria":cat,"subbase":sub,"nombre":name,"tipo":typ,
   "estado":status,"imagen":path,"origen":source,"control_calidad":quality,
   "derechos":"pendiente" if not path else ("referencia de tercero con licencia documentada" if source=="Wikimedia Commons" else "ilustración con IA, uso público sujeto a condiciones aplicables")})
for mat in data:
 id=mat["id"]
 cat=mat["n"]
 base=f"assets/biblioteca/bases/{id}.jpg"
 add("MATERIALES",cat,"",cat,"base",base if base in source_files else "","pendiente" if base not in source_files else "visual por revisar")
 for sub in mat["b"]:
  subname=sub[0]
  if id=="reciclables":
   rec=next((x for x in rpack if x.get("tipo")=="subbases" and clean(x.get("nombre"))==clean(subname)),None)
  elif id=="metales":
   rec=next((x for x in mpack if x.get("tipo")=="subbases" and clean(x.get("nombre"))==clean(subname)),None)
  else:
   rec=next((x for x in credits if x.get("material")==id and clean(x.get("subbase"))==clean(subname)),None)
  path=rec.get("archivo",rec.get("filename","")) if rec else ""
  src="Wikimedia Commons" if rec and rec in credits else "IA" if path else ""
  add("MATERIALES",cat,subname,subname,"subbase",path,"referencia por revisar" if path else "pendiente",src)
  for p in sub[2]:
   product=clean(p)
   x=None
   if id=="reciclables":x=next((x for x in rpack if x.get("tipo")=="productos" and clean(x.get("nombre"))==product),None)
   elif id=="metales":x=next((x for x in mpack if x.get("tipo")=="productos" and clean(x.get("nombre"))==product),None)
   elif id=="organicos":x=next((x for x in opack if clean(x.get("nombre"))==product),None)
   elif id=="rio":x=next((x for x in river if clean(x.get("nombre"))==product and clean(x.get("subbase"))==clean(subname)),None)
   path=x.get("archivo","") if x else ""
   add("MATERIALES",cat,subname,product,"producto",path,
     "hiperrealismo editorial pendiente de aprobación" if id=="rio" and path else "ilustración/pertinencia por revisar" if path else "pendiente","IA" if path else "")
for mat,manifests,typ in [
 ("ECOALDEAS",["assets/biblioteca/ecoaldeas/paquete-01/manifest.json","assets/biblioteca/ecoaldeas/paquete-02/manifest.json"],"módulo/proceso"),
 ("ECO-CIA",["assets/biblioteca/ecocia/manifest.json"],"módulo"),
 ("ECO-TIENDAS",["assets/biblioteca/ecotiendas/manifest.json"],"módulo"),
]:
 for m in manifests:
  for item in read_manifest(m):
   add(mat,mat,"",item.get("nombre",""),typ,item.get("archivo",""),
   "borrador visual: recorte de infografía" if mat!="ECOALDEAS" else "ilustración conceptual; revisión específica pendiente","IA")
for item in [
 ("ECOALDEAS","Infografía de sistema diversificado","assets/organigramas/ecoaldeas-sistema-diversificado.jpg"),
 ("ECO-CIA","Referencia arquitectónica","assets/organigramas/ecocia-referencia-institucional.jpg"),
]:
 add(item[0],item[0],"",item[1],"organigrama",item[2],"ilustración a revisar","IA")
for cat in data:
 path=f"organigramas/{cat['id']}.svg"
 add("ORGANIGRAMAS","Diagrama de materiales","",cat["n"],"organigrama",path,"diagrama SVG con símbolos; pendiente de enriquecer con fotos","diagrama")
for page in ("ecoaldeas-propuestas.html","ecoaldeas.html","ecocia.html","ecotiendas.html","biblioteca-visual.html"):
 assert (root/page).exists(),f"Falta página {page}"
# Assets present but not necessarily integrated (sources, panel collages, historic logos, etc).
used={row["imagen"] for row in rows if row["imagen"]}
all_photo={p for p in source_files if p.lower().endswith((".jpg",".jpeg",".png",".webp",".svg"))}
unused=sorted(all_photo-used)
for p in unused:
 if "logo ecopiensa" in p: continue
 if p.startswith("assets/fotos/"):continue
 if p.startswith("assets/biblioteca/") or p.startswith("assets/organigramas/"):
  rows.append({"linea":"BANCO DE IMÁGENES","categoria":"Archivo existente sin nodo propio","subbase":"",
    "nombre":Path(p).stem.replace("_"," "),"tipo":"fuente/borrador","estado":"BANCO_SIN_ASIGNAR",
    "imagen":p,"origen":"archivo local","control_calidad":"revisar antes de asignar a un producto","derechos":"comprobar origen y licencia"})
primary=[x for x in rows if x["linea"]=="MATERIALES"]
missing=[x for x in primary if x["estado"]!="VINCULADA_REVISAR"]
pending=[x for x in missing if x["tipo"]!="organigrama"]
other=[x for x in rows if x["linea"]!="MATERIALES"]
# Planning: next groups by families, do not put group numbers in image filenames.
groups=[]
idx=1
for material in [x["n"] for x in data]:
 items=[x for x in pending if x["categoria"]==material]
 for n in range(0,len(items),10):
  chunk=items[n:n+10]
  groups.append({"grupo":"G"+str(idx).zfill(2),"familia":material,
   "cantidad":len(chunk),"imagenes":[{"nombre":x["nombre"],"subbase":x["subbase"],"tipo":x["tipo"],
    "archivo_recomendado":re.sub(r'[^a-z0-9]+','-',__import__('unicodedata').normalize('NFKD',x["nombre"].lower()).encode('ascii','ignore').decode()).strip('-')+".jpg"} for x in chunk]})
  idx+=1
now=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
report={"fecha_auditoria":now,"total_archivos_imagen":len(all_photo),
 "total_nodos_materiales":len(primary),
 "nodos_vinculados_con_imagen":sum(x["estado"]=="VINCULADA_REVISAR" for x in primary),
 "nodos_pendientes":len(pending),
 "organigramas_materiales":len(data),
 "banco_de_imagenes_no_asignadas":sum(x["estado"]=="BANCO_SIN_ASIGNAR" for x in rows),
 "grupos_pendientes":len(groups),
 "aviso":"La presencia de un JPG no verifica fidelidad fotográfica ni permisos definitivos; revisar manualmente cada activo.",
 "items":rows}
(root/"AUDITORIA_CATALOGO.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
with (root/"AUDITORIA_IMAGENES.csv").open("w",newline="",encoding="utf-8-sig") as fh:
 w=csv.DictWriter(fh,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
(root/"PLAN_PAQUETES_IMAGENES.json").write_text(json.dumps({"fecha":now,"grupos_pendientes":groups,
 "regla":"Crear diez imágenes por grupo, con nombre propio por producto; no incluir palabra paquete ni grupo en título/archivo."},ensure_ascii=False,indent=2),encoding="utf-8")
summary=Counter(x["estado"] for x in primary)
(root/"AUDITORIA_VISUAL.md").write_text(
f"""# Auditoría integral de imágenes — ECORECYCLE
Actualización: {now}. Se revisaron archivos, manifiestos y rutas del sitio; la pertinencia visual requiere inspección editorial adicional.

## Resumen
- Archivos gráficos localizados en GitHub: **{len(all_photo)}** (incluye organigramas, fuentes, recursos y logos).
- Nodos de materiales requeridos: **{len(primary)}** (13 bases, 68 subbases, 272 productos/aplicaciones).
- Nodos con archivo local y ruta de carga prevista: **{summary['VINCULADA_REVISAR']}**; son candidatos a revisión, **no aprobaciones de calidad**.
- Nodos sin imagen individual correcta: **{len(pending)}**.
- Diagramas de materiales: **{len(data)} SVG existentes**, todavía esquemáticos y no plenamente fotográficos.
- Archivos/fuentes de consulta sin nodo asignado: **{report['banco_de_imagenes_no_asignadas']}** (no se borran).
- Grupos previstos para completar nodos faltantes: **{len(groups)}** de hasta diez fotografías.
- ECOALDEAS y ECO-CIA son **proyectos distintos**: las ecoaldeas son fincas diversificadas, no un modelo circular de edificio; ECO-CIA recibe excedentes para acopio y transformación.

## Revisión visual pendiente
Las imágenes recortadas de infografías de ECO-CIA, ECO-TIENDAS y algunos productos orgánicos son **provisionales**. Las diez nuevas imágenes de río son más realistas, pero requieren comprobar escala, coherencia material y correspondencia técnica. Las fotos de Wikimedia requieren conservar atribución y licencia; el clic de la web se mantiene dentro del sitio.

## Próximos trabajos
- Ver lista completa por nodo en \`AUDITORIA_IMAGENES.csv\`.
- Grupos previstos en \`PLAN_PAQUETES_IMAGENES.json\`.
- Informes públicos navegables en \`auditoria.html\`.
- Cada archivo nuevo debe tener nombre descriptivo, ruta estable, texto alternativo y nota de procedencia. Mantener intacto \`logo ecopiensa (1).png\`.
- El macroproyecto privado no está incluido en esta auditoría.
""",encoding="utf-8")
print(json.dumps({k:v for k,v in report.items() if k!="items"},ensure_ascii=False))
