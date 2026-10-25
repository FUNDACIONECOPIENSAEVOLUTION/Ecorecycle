from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'assets/biblioteca/rio/manifest.json'
items=json.loads(manifest.read_text(encoding='utf8'))['imagenes']
assert len(items)==10
dest=ROOT/'descargas/APLICACIONES_MATERIAL_DE_RIO.zip'
dest.parent.mkdir(parents=True,exist_ok=True)
with ZipFile(dest,'w',ZIP_DEFLATED,compresslevel=8) as z:
    z.write(manifest,arcname='manifest.json')
    for i in items:
        p=ROOT/i['archivo']
        assert p.is_file() and p.stat().st_size>10000,p
        sub=i['subbase'].replace('¾','tres_cuartos').replace('½','medio').replace(' ','_').replace('/','_')
        z.write(p,arcname=sub+'/'+p.name)
    z.writestr('LEAME.txt','Fundación Ecopiensa Evolution / ECORECYCLE. Diez recreaciones hiperrealistas generadas con IA. Solo representan productos y aplicaciones propuestos, no obras de la Fundación. No usar como evidencia técnica o certificación. Logo oficial no modificado.\n')
with ZipFile(dest) as z:
    assert z.testzip() is None
    assert sum(s.lower().endswith('.jpg') for s in z.namelist())==10
print('ZIP_VERIFICADO',dest.stat().st_size, len(items))
