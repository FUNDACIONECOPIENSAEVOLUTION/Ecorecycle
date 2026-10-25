#!/usr/bin/env python3
"""Crea descargas verificadas de las galerías institucionales públicas (sin documentos reservados)."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json
root=Path(__file__).resolve().parents[1]
out=root/'descargas';out.mkdir(exist_ok=True)
for category in ['ecocia','ecotiendas','organicos']:
    path=root/'assets'/'biblioteca'/category
    d=json.loads((path/'manifest.json').read_text('utf8'))
    images=d['imagenes']
    assert len(images)==10
    names=[x['nombre'] for x in images]
    assert len(set(names))==10
    zipname='GALERIA_'+category.upper()+'_10_IMAGENES.zip'
    with ZipFile(out/zipname,'w',ZIP_DEFLATED,compresslevel=8) as z:
        for x in images:
            file=root/x['archivo']
            assert file.is_file() and file.stat().st_size>14000,file
            z.write(file,arcname=file.name)
        z.write(path/'manifest.json',arcname='manifest.json')
        z.writestr('LEAME.txt','Imágenes ilustrativas de Fundación Ecopiensa Evolution. Archivo para difusión, no evidencia de instalaciones actuales. El logotipo institucional se muestra por separado en la página web.\n')
    with ZipFile(out/zipname) as z:
        assert z.testzip() is None
        assert len([p for p in z.namelist() if p.endswith('.jpg')])==10
    print('ZIP confirmado',zipname,(out/zipname).stat().st_size)
