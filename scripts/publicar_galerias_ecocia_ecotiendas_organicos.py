#!/usr/bin/env python3
"""Organiza ilustraciones originales en imágenes locales con nombres de procesos, sin logo ficticio.
Cada archivo queda en su sección; el nombre del paquete solo figura en el manifiesto interno.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageEnhance
import json, math, random

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"assets/biblioteca"
SIZE=(960,600)
def save_crop(src, dest, focus=(.13,.19,.87,.81)):
    im=Image.open(src).convert("RGB")
    W,H=im.size
    rect=(int(focus[0]*W),int(focus[1]*H),int(focus[2]*W),int(focus[3]*H))
    im=ImageOps.fit(im.crop(rect),SIZE,method=Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True,exist_ok=True)
    im.save(dest,"JPEG",quality=87,optimize=True,progressive=True)
def manifest(folder,title,items,origin):
    d={"linea":title,"tipo":"Galería institucional ilustrativa","imagenes":[{"nombre":name,"archivo":str((folder/"imagenes"/(stem+".jpg")).relative_to(ROOT)).replace("\\","/"),
       "alt":"Ilustración conceptual de "+name,"origen":origin,"derechos":"Ilustración generada con IA para el proyecto, sin atribución de instalaciones reales"} for stem,name in items]}
    (folder/"manifest.json").write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding="utf8")
    return d
eco=[
("recepcion_y_pesaje","Recepción y pesaje"),
("inspeccion_y_clasificacion","Inspección y clasificación"),
("transformacion_agroindustrial","Transformación agroindustrial"),
("empaque_y_etiquetado","Empaque y etiquetado"),
("almacenamiento_seco","Almacenamiento seco"),
("refrigeracion_y_cadena_fria","Refrigeración y cadena fría"),
("distribucion_y_despacho","Distribución y despacho"),
("educacion_agroindustrial","Educación y servicios"),
("cargue_y_consolidacion","Cargue y consolidación de pedidos"),
("ruta_territorial","Ruta territorial de distribución")
]
shops=[
("eco_tienda_comunitaria","Eco-tienda comunitaria"),
("mercado_campesino","Mercado campesino"),
("feria_regional","Feria regional"),
("exhibicion_fresca","Exhibición de productos frescos"),
("exhibicion_transformados","Exhibición de productos transformados"),
("atencion_en_caja","Atención en caja"),
("pedidos_y_domicilios","Pedidos y domicilios"),
("degustacion_promocion","Degustación y promoción"),
("articulacion_comunitaria","Articulación comunitaria"),
("consumo_responsable","Consumo responsable")
]
for base_name, entries, title in [
("ecocia",eco,"ECO-CIA · Centro integral agroindustrial"),
("ecotiendas",shops,"Eco-tiendas · comercialización de excedentes")]:
 folder=BASE/base_name
 for stem,name in entries:
    save_crop(folder/"fuentes"/(stem+".jpg"),folder/"imagenes"/(stem+".jpg"))
    print("OK",base_name,name,flush=True)
 manifest(folder,title,entries,"Creación original con IA, recorte de la ilustración para eliminar rótulos/logos de referencia")

organic=[
("compost_estabilizado","Compost estabilizado",(0.032,.365,.335,.577)),
("humus_de_lombriz","Humus de lombriz",(0.344,.364,.665,.575)),
("enmiendas_de_suelo","Enmiendas de suelo",(0.030,.756,.332,.948)),
("acolchado_vegetal","Acolchado vegetal",(0.682,.755,.973,.945)),
("astillas","Astillas",(0.038,.174,.340,.364)),
("biocarbon","Biocarbón",(0.678,.590,.970,.765)),
("digestato_tratado","Digestato tratado",(0.675,.367,.970,.575)),
("fertilizante_formulado","Fertilizante formulado",(0.037,.580,.332,.765)),
("sustrato_para_hongos","Sustrato para hongos",(0.350,.584,.665,.768)),
("bokashi","Bokashi",(0.039,.370,.344,.575))
]
source=BASE/"organicos/fuentes/catalogo_organicos.jpg"
folder=BASE/"organicos"
for stem,name,crop in organic:
 dest=folder/"productos"/(stem+".jpg")
 save_crop(source,dest,crop)
 # A selected subset receives differentiated visualization representing its specific processed form.
 if stem in ("biocarbon","astillas","sustrato_para_hongos","digestato_tratado"):
    im=Image.open(dest).convert("RGB");draw=ImageDraw.Draw(im,"RGBA")
    if stem=="biocarbon":
      random.seed(14)
      for n in range(120):
       x=random.randint(35,900);y=random.randint(160,540);w=random.randint(10,32);h=random.randint(8,25)
       draw.polygon([(x,y),(x+w,y-5),(x+w+8,y+h),(x+3,y+h+5)],fill=(32,35,31,210),outline=(105,104,97,180))
    elif stem=="astillas":
      random.seed(55)
      for n in range(100):
       x=random.randint(30,900);y=random.randint(240,570);length=random.randint(10,45)
       draw.polygon([(x,y),(x+length,y-5),(x+length+5,y+8),(x+3,y+16)],fill=(170,112,57,190),outline=(105,75,34,110))
    elif stem=="sustrato_para_hongos":
      for x,y in [(205,290),(390,280),(600,333),(770,285)]:
       draw.ellipse((x-55,y-70,x+55,y-15),fill=(229,227,204,210),outline=(143,133,109,180),width=4)
       draw.rounded_rectangle((x-12,y-18,x+12,y+45),radius=7,fill=(215,212,188,210))
    else:
      draw.rounded_rectangle((290,235,650,490),radius=26,fill=(84,99,80,185),outline=(213,227,205,220),width=7)
      draw.ellipse((355,250,585,315),fill=(79,59,38,180))
    im.save(dest,"JPEG",quality=88,optimize=True)
 print("OK", "organicos",name,flush=True)
d={"linea":"Material orgánico · apoyo a ecoaldeas","tipo":"Productos derivados","imagenes":[{"nombre":name,"archivo":str((folder/"productos"/(stem+".jpg")).relative_to(ROOT)).replace("\\","/"),"alt":"Ilustración conceptual de "+name,
 "origen":"Ilustración original con IA; recorte y representación conceptual específica",
 "derechos":"Creación por IA sin fotografías externas",
 "nota":"Producto sujeto a estabilización, pruebas de calidad y requisitos aplicables antes de uso agrícola"} for stem,name,_ in organic]}
(folder/"manifest.json").write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf8")
for path,count in [(BASE/"ecocia",10),(BASE/"ecotiendas",10),(BASE/"organicos",10)]:
 m=json.loads((path/"manifest.json").read_text(encoding="utf8"))
 assert len(m["imagenes"])==count
 assert len({x["nombre"] for x in m["imagenes"]})==count
 for x in m["imagenes"]:
    file=ROOT/x["archivo"]
    assert file.exists() and file.stat().st_size>14000, file
print("VALIDACIÓN FINAL: 30 archivos individuales + 3 manifiestos")
