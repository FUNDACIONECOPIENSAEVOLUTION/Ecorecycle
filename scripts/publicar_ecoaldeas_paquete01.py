#!/usr/bin/env python3
"""Create ECOALDEAS Package 01, 10 themed original illustrations hosted in ECORECYCLE.
No external HTTP requests or third-party photos; labels remain in HTML.
Concept-only: no proof of built works. The internal macroproject must never be published.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/biblioteca/ecoaldeas/paquete-01"
SRC=ROOT/"assets/biblioteca/ecoaldeas/fuentes"
OUT.mkdir(parents=True,exist_ok=True)
SOURCES={"network":"red_familiar.jpg","farm":"finca_integral.jpg","flow":"red_excedentes.jpg","cycle":"granja_diversificada.jpg"}
spec=[
 ("01_parcelacion_colaborativa","Parcelación colaborativa","network",(78,280,680,640),"Varias parcelas campesinas con producciones complementarias"),
 ("02_finca_integral_sistematica","Finca integral sistemática","farm",(75,190,806,715),"Vivienda y varios módulos productivos en una misma finca"),
 ("03_huerta_hortalizas","Huerta y hortalizas","cycle",(210,395,465,590),"Diversidad de cultivos y hortalizas en camas agrícolas"),
 ("04_frutales_y_forrajes","Frutales y forrajes","network",(720,286,1030,555),"Árboles frutales y cultivos que complementan otras actividades"),
 ("05_avicultura_gallinas","Gallinas y pollos","cycle",(664,349,809,472),"Zona ilustrativa de gallinas y pollos de corral"),
 ("06_porcicultura","Porcicultura","cycle",(585,332,709,449),"Cerdos y estructura de producción pecuaria"),
 ("07_bovinos_y_caprinos","Bovinos y caprinos","farm",(565,438,820,660),"Ganado y producción de forraje, zona pecuaria"),
 ("08_acuicultura_peces","Piscicultura","cycle",(650,474,855,632),"Estanque de producción de peces y cuidado del agua"),
 ("09_compostaje_controlado","Tratamiento orgánico","cycle",(1088,420,1402,619),"Zona de tratamiento diferenciado de orgánicos y estiércoles"),
 ("10_autoconsumo_y_excedentes","Autoconsumo y excedentes","flow",(480,285,1018,585),"Alimentos para familias y excedentes entregados a ECO-CIA")
]
records=[]
for i,(slug,name,key,bbox,desc) in enumerate(spec,1):
    img=Image.open(SRC/SOURCES[key]).convert("RGB")
    assert img.width>=bbox[2] and img.height>=bbox[3],(slug,img.size,bbox)
    img=ImageOps.fit(img.crop(bbox),(960,600),Image.Resampling.LANCZOS)
    path=OUT/(slug+".jpg")
    ImageDraw.Draw(img).rectangle((1,1,958,598),outline="#a7cdb5",width=3)
    img.save(path,"JPEG",quality=87,optimize=True,progressive=True)
    records.append({
       "numero":i,"id":slug,"nombre":name,"descripcion":desc,
       "archivo":str(path.relative_to(ROOT)).replace("\\","/"),
       "tipo":"módulo","estado":"ilustración conceptual generada con IA",
       "derechos":"Fuente visual propia generada con IA. Sin fotografía de terceros.",
       "observacion":"No es fotografía de una instalación construida; validar detalle de implementación."
    })
(OUT/"manifest.json").write_text(json.dumps({
 "paquete":"ECOALDEAS-01","imagenes":records,
 "nota":"Imágenes originales temáticas sin enlaces externos ni logos generados. El logo oficial se aplica desde el archivo institucional."},ensure_ascii=False,indent=2),encoding="utf-8")
print("Creado paquete ECOALDEAS-01:",len(records),"archivos individuales")
