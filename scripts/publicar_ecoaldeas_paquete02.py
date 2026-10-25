#!/usr/bin/env python3
# Paquete 02 ECOALDEAS: imágenes derivadas de ilustraciones originales con IA.
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json
BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'assets/biblioteca/ecoaldeas/paquete-02';OUT.mkdir(parents=True,exist_ok=True)
SRC=BASE/'assets/biblioteca/ecoaldeas/fuentes'
A=Image.open(SRC/'paquete02_a.jpg').convert('RGB')
B=Image.open(SRC/'paquete02_b.jpg').convert('RGB')
P={'gallinas':(B,(9,627,297,852)),'cerdos':(B,(314,627,604,851)),
'bovinos':(B,(620,631,917,851)),'peces':(B,(928,629,1223,855)),
'biodig':(B,(1237,632,1528,857)),'vivienda':(B,(318,182,611,382)),
'hortalizas':(B,(618,181,918,381)),'aldea':(A,(4,181,414,404)),
'forrajes':(A,(1259,174,1533,402)),'porqui_biodig':(A,(465,470,961,704)),
'bovinos2':(A,(966,470,1529,705)),'compost':(A,(464,776,970,937)),
'mercado':(A,(982,773,1528,934)),'estanque':(A,(6,777,450,935))}
S=[
('01_gallinaza_recogida_segura','Gallinaza: recolección segura','gallinas','compost',['Separar gallinaza','Tratamiento controlado','Enmienda solo si es apta']),
('02_porquinaza_tratamiento','Porquinaza: tratamiento','cerdos','porqui_biodig',['Recolectar por separado','Tratar de forma autorizada','Gestionar digestato seguro']),
('03_estiercol_bovino_caprino','Estiércol bovino y caprino','bovinos','bovinos2',['Acopiar sin contaminar','Estabilizar o compostar','Uso agrícola validado']),
('04_compostaje_monitoreado','Compostaje monitoreado','compost','biodig',['Mezclar residuos aptos','Controlar temperatura','Madurar el compost']),
('05_compost_maduro_para_suelo','Compost maduro para suelo','compost','hortalizas',['Verificar madurez','Dosificar según el suelo','Mejorar el suelo agrícola']),
('06_forrajes_para_animales','Cultivo de forrajes','forrajes','bovinos',['Sembrar según el clima','Cosechar y conservar','Alimentación adecuada']),
('07_captacion_y_riego_protegido','Agua captada y riego protegido','vivienda','hortalizas',['Captación permitida','Almacenar agua segura','Riego eficiente']),
('08_estanque_calidad_del_agua','Estanque y calidad del agua','peces','estanque',['Monitorear parámetros','Proteger de vertimientos','Producción piscícola']),
('09_cosecha_para_autoconsumo','Cosecha para autoconsumo','hortalizas','mercado',['Cosechar y seleccionar','Reservar para la familia','Compartir en comunidad']),
('10_excedentes_para_ecocia','Excedentes hacia ECO-CIA','mercado','aldea',['Cubrir autoconsumo','Clasificar y registrar','Entregar a ECO-CIA'])]
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,b=False):return ImageFont.truetype(FB if b else F,size)
def crop(k,w,h):
 im,rect=P[k]
 return ImageOps.fit(im.crop(rect),(w,h),Image.Resampling.LANCZOS)
def write(p,i):
 key,name,left,right,steps=p
 im=Image.new('RGB',(1200,760),(248,252,248));d=ImageDraw.Draw(im)
 d.rounded_rectangle((12,12,1188,748),radius=27,fill='white',outline=(150,202,169),width=3)
 d.rounded_rectangle((12,12,1188,118),radius=25,fill=(7,92,54))
 d.rectangle((12,75,1188,118),fill=(7,92,54))
 d.ellipse((29,34,96,101),fill=(208,243,218))
 d.text((62,64),str(i),font=font(31,True),fill=(7,92,54),anchor='mm')
 sz=40
 while d.textbbox((0,0),name,font=font(sz,True))[2]>1030 and sz>27:sz-=1
 d.text((117,35),name,font=font(sz,True),fill='white')
 d.text((117,89),'ECOALDEAS  |  PAQUETE 02  |  PROCESOS CONECTADOS',font=font(14,True),fill=(210,243,218))
 im.paste(crop(left,792,423),(31,139));im.paste(crop(right,333,423),(836,139))
 d.rounded_rectangle((31,139,823,562),radius=7,outline=(155,205,175),width=2)
 d.rounded_rectangle((836,139,1169,562),radius=7,outline=(155,205,175),width=2)
 d.rounded_rectangle((31,581,1169,715),radius=15,fill=(238,248,240))
 for ix,step in enumerate(steps):
  x=57+ix*392
  d.ellipse((x,603,x+34,637),fill=(15,139,75));d.text((x+17,620),str(ix+1),font=font(18,True),fill='white',anchor='mm')
  words=step.split();line='';lines=[]
  for word in words:
   next=(line+' '+word).strip()
   if line and d.textbbox((0,0),next,font=font(22,True))[2]>296:
    lines.append(line);line=word
   else:line=next
  if line:lines.append(line)
  for t,w in enumerate(lines):d.text((x,648+27*t),w,font=font(22,True),fill=(23,66,44))
  if ix<2:d.polygon([(x+344,624),(x+360,635),(x+344,646)],fill=(9,126,69))
 d.text((33,728),'Ilustración conceptual IA  |  No representa instalaciones existentes  |  Logo oficial solo en la web',font=font(13),fill=(89,116,96))
 path=OUT/(key+'.jpg');im.save(path,'JPEG',quality=90,optimize=True,progressive=True)
 return {'numero':i,'id':key,'nombre':name,'archivo':str(path.relative_to(BASE)).replace('\\','/'),'pasos':steps,
 'descripcion':name+' — '+', '.join(steps),'tipo':'proceso interno ECOALDEAS',
 'origen':'Recreación editorial de material generado con IA','derechos':'Imagen original de IA, sin fotos de terceros',
 'nota':'Ilustración conceptual. El tratamiento de residuos requiere validación técnica.'}
rows=[write(p,i) for i,p in enumerate(S,1)]
(OUT/'manifest.json').write_text(json.dumps({'paquete':'ECOALDEAS-02','imagenes':rows,
 'aviso':'Las ecoaldeas son fincas diversificadas. ECO-CIA es centro independiente; no se aplica estiércol crudo a alimentos.'},ensure_ascii=False,indent=2),encoding='utf-8')
preview=Image.new('RGB',(2000,5*620+150),(239,250,242));pd=ImageDraw.Draw(preview)
pd.rectangle((0,0,2000,124),fill=(7,92,54))
pd.text((45,24),'ECOALDEAS | PAQUETE 02 | DIEZ PROCESOS',font=font(43,True),fill='white')
for ix,row in enumerate(rows):
 image=Image.open(BASE/row['archivo']);image.thumbnail((980,610))
 preview.paste(image,(10+ix%2*1000,145+ix//2*620))
preview.save(OUT/'VISTA_PREVIA_PAQUETE02.jpg',quality=88,optimize=True)
print('VERIFICADO',len(rows),'archivos en',OUT)
