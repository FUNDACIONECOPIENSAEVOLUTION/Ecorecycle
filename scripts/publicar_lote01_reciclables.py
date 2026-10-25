#!/usr/bin/env python3
"""Convierte exactamente diez imágenes originales de IA en fotos locales sin marcas recreadas.
Solo publica la zona central del material: no se reutiliza ningún logo sintético ni cinta rotulada.
Mantiene fuera del repositorio el documento macro empresarial.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps
from io import BytesIO
import base64, json, os, sys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'scripts'/'lote01_reciclables_blobs.json'
BASE=ROOT/'assets'/'biblioteca'/'reciclables-secos'
TOKEN=os.environ.get('GITHUB_TOKEN')
assert TOKEN, 'No se recibió token temporal de GitHub Actions'
spec=json.loads(SRC.read_text('utf-8'))
assert len(spec['imagenes'])==10, 'El paquete debe contener exactamente diez imágenes'
assert len({e['archivo'] for e in spec['imagenes']})==10, 'Nombres duplicados'

def read_github_blob(sha):
    url='https://api.github.com/repos/FUNDACIONECOPIENSAEVOLUTION/Ecorecycle/git/blobs/'+sha
    req=Request(url,headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','User-Agent':'Ecorecycle-Assets/1.0'})
    with urlopen(req,timeout=45) as response:
        blob=json.loads(response.read())
    assert blob.get('encoding')=='base64'
    return base64.b64decode(blob['content'])

photos=[]
for i,item in enumerate(spec['imagenes'],1):
    raw=read_github_blob(item['blob_sha'])
    source=Image.open(BytesIO(raw)).convert('RGB')
    W,H=source.size
    # Recorte revisado: excluye insignias/logos generados en esquinas y pie decorativo.
    area=source.crop((round(W*.23),round(H*.28),round(W*.77),round(H*.78)))
    area=ImageOps.fit(area,(810,540),Image.Resampling.LANCZOS)
    relative=item['archivo']
    assert relative.startswith('assets/biblioteca/reciclables-secos/'),relative
    output=ROOT/relative
    output.parent.mkdir(parents=True,exist_ok=True)
    area.save(output,'JPEG',quality=89,optimize=True,progressive=True)
    photos.append({
      'numero':i,'nombre':item['nombre'],'tipo':item['tipo'],'archivo':relative,
      'alt':item['alt'],'licencia':'Creación original con IA para catálogo ECORECYCLE',
      'autor':'Fundación Ecopiensa Evolution / ilustración generada con IA',
      'procedencia':'ilustración IA, no fotografía de instalaciones propias',
      'origen':'Paquete 01 — Reciclables secos I',
      'sin_logotipo_generado':True,
      'derechos':'Imagen generada para el proyecto, no se incorpora material fotográfico externo'
    })
    print(f"OK {i:02d} {item['tipo']}: {item['nombre']} → {relative}",flush=True)
BASE.mkdir(parents=True,exist_ok=True)
(BASE/'manifest.json').write_text(json.dumps({
 'lote':'01','linea':'Material reciclable','version':'1.0',
 'aviso':'Recreaciones con IA; no constituyen evidencia de operaciones, instalaciones o productos disponibles.',
 'imagenes':photos},ensure_ascii=False,indent=2),encoding='utf-8')
print('Publicados',len(photos),'archivos locales',flush=True)
