#!/usr/bin/env python3
"""Descargas completas de los paquetes ECOALDEAS 01 y 02, sin proyectos privados."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json
root=Path(__file__).resolve().parents[1]
out=root/'descargas';out.mkdir(exist_ok=True)
for no in ('01','02'):
 folder=root/'assets/biblioteca/ecoaldeas'/('paquete-'+no)
 manifest=folder/'manifest.json'
 info=json.loads(manifest.read_text(encoding='utf-8'))
 imgs=info['imagenes']
 assert len(imgs)==10 and len({x['nombre'] for x in imgs})==10
 output=out/('ECOALDEAS_PAQUETE_'+no+'_10_IMAGENES.zip')
 with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=8) as z:
  for x in imgs:
   file=root/x['archivo']
   assert file.exists() and file.stat().st_size>10000,x
   z.write(file,arcname=file.name)
  z.write(manifest,arcname='manifest.json')
  preview=folder/('VISTA_PREVIA_PAQUETE'+no+'.jpg')
  if not preview.exists():preview=folder/('VISTA_PREVIA_PAQUETE0'+no+'.jpg')
  if preview.exists():z.write(preview,arcname=preview.name)
  z.writestr('LEAME_PRIMERO.txt','Fundación Ecopiensa Evolution. ECOALDEAS Paquete '+no+'; 10 ilustraciones generadas con IA y alojadas en ECORECYCLE. El documento macro es privado y NO forma parte de esta descarga.\n')
 with ZipFile(output) as ver:
  assert ver.testzip() is None
  assert len([x for x in ver.namelist() if x.endswith('.jpg')])>=10
 print('ZIP',output.name,output.stat().st_size)
