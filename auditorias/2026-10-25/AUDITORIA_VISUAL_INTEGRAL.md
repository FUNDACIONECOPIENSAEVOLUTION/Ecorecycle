# AUDITORÍA VISUAL INTEGRAL · 25 de octubre de 2026

**Objeto:** contrastar los organigramas y los archivos de imagen de la Fundación Ecopiensa Evolution con su repositorio público ECORECYCLE. **No se publica documentación interna del proyecto macro**.

## Confirmaciones técnicas

- GitHub `main` contiene las páginas `index.html`, `ecoaldeas.html`, `ecoaldeas-propuestas.html`, `ecocia.html`, `ecotiendas.html`, `biblioteca-visual.html`.
- Existen **13 organigramas vectoriales SVG** en `organigramas/` y usan figuritas/emoji en los nodos, no fotos individuales.
- **70 archivos de imagen** están presentes en 7 bibliotecas de diez ilustraciones/fotos: ECOALDEAS (20), ECO-CIA (10), eco-tiendas (10), orgánicos (10), reciclables secos (10), metales (10). Sus siete manifiestos apuntan a los archivos existentes.
- Adicionalmente, **67 fotografías externas** de subbases tienen metadatos de procedencia, autor y licencia en `assets/fotos/creditos.json`. Su uso está sujeto a atribución suficiente y, sobre todo, **correspondencia visual correcta**. No se confunden con fotografías institucionales reales.
- El inventario general de materiales tiene **13 bases/categorías**, **68 subbases** y **272 posiciones de productos/aplicaciones**: **353 posiciones**.
- De las 353 posiciones: **13 bases no tienen imagen propia**, **67 de 68 subbases enlazan a una imagen local**, **21 de 272 productos/aplicaciones enlazan a imágenes**, pero solo **20 archivos diferentes** cubren esas 21 posiciones (biocarbón aparece en dos subbases). Por tanto hay **265 posiciones sin imagen y 1 imagen reiterada en dos nodos**.
- Estas cifras son **inventario técnico**, NO aprobación de calidad o exactitud fotográfica.

## Problemas verificables

1. **Dos imágenes dentro del mismo proceso.** El script `scripts/publicar_ecoaldeas_paquete02.py` hace dos pegados por tarjeta (`im.paste(crop(left...))` y `im.paste(crop(right...))`). Es contrario a una sola imagen clara por proceso.
2. **Recortes de una misma infografía** en `scripts/publicar_ecoaldeas_paquete01.py`: diez tarjetas derivan de cuatro composiciones generales. Se requiere crear escenas independientes para evitar confusión de animales, edificaciones y texturas.
3. **Orgánicos derivados de un catálogo conjunto.** Las diez ilustraciones están presentes, pero requieren rehacerse como escenas independientes de buena resolución cuando se haga la corrección visual.
4. **SVG sin fotografías.** La página permite visualizar fotos en tarjetas HTML, pero los organigramas SVG siguen utilizando emojis; la exportación dinámica de `index.html` también los incrusta.
5. **Base sin foto independiente.** `fotos-catalogo.js` muestra la foto de la primera subbase como imagen de la base principal. Es la repetición que hay que eliminar.
6. **Productos fuera de tres líneas quedan pendientes:** `productFor()` resuelve únicamente reciclables, metales y orgánicos. Hay que sustituirlo por un mapa de imágenes por `linea + subbase + producto` para todos los materiales.
7. **Imágenes con manchas o puntos negros:** incidencia reportada en la web. No se puede asignar honestamente un número exacto de fotos afectadas usando solo manifiestos y código; exige inspección de cada archivo a tamaño real y revisión del render responsive.
8. **Recorte excesivo:** las tarjetas usan `object-fit:cover` incluso cuando la imagen contiene explicaciones; para diagramas usar `contain` y reservar `cover` para fotos horizontales generadas con composición apropiada.
9. **Números de paquete visibles:** la biblioteca pública aún presenta encabezados con "Paquete 01/02". El nombre público debe ser solamente el tema; los códigos de grupos quedan en el plan interno.
10. **No mezclar funciones:** ECOALDEAS = parcelas/fincas, autoconsumo y procesos complementarios; ECO-CIA = centro independiente, circular si así se diseña, que recibe excedentes; eco-tiendas = comercialización.
11. **Derechos de imagen:** las 67 referencias tienen metadatos (sin campos vacíos de procedencia, autor o licencia) pero la interfaz debe exponer crédito/licencia y cumplir las condiciones pertinentes sin convertir las fotos en enlaces de salida.

## Doce casos de correspondencia incorrecta identificados desde las fuentes

1. **Material reciclable · Papel** — El archivo de origen identificado es cartón; la web usa un archivo local preferente, pero la referencia equivocada permanece.
2. **Material orgánico · Podas y jardinería** — La fotografía documenta una sierra en un museo, no residuos de poda.
3. **Escombros y RCD · Cerámicos y tejas** — La fotografía corresponde a una pieza arqueológica romana, no a RCD cerámico.
4. **Escombros y RCD · Asfalto recuperado** — El título identifica una calle; no acredita pavimento fresado recuperado.
5. **Cartón y papel · Papel mixto** — El título identifica un triciclo de transporte, no papel mixto.
6. **Llantas usadas · Granulado de caucho** — El material identificado es TPV; no demuestra granulado de llanta.
7. **Llantas usadas · Polvo de caucho** — La fotografía se refiere a fabricación de neumáticos, no al polvo recuperado.
8. **Llantas usadas · Pirólisis industrial** — La fotografía es de un hallazgo arqueológico, no de un proceso de pirólisis.
9. **Aceites usados · Grasas alimentarias** — Archivo titulado 'The slave of grease', sin evidencia de residuos grasos alimentarios.
10. **Residuos electrónicos RAEE · Equipos recuperables** — Fotografía de una demostración de artes marciales, no de RAEE recuperable.
11. **Residuos electrónicos RAEE · Carcasas plásticas** — Fotografía de un banco de jardín, no de carcasas de aparatos.
12. **Residuos electrónicos RAEE · Baterías y pantallas** — Archivo de conservación energética, no separación de baterías y pantallas.

Los títulos de fuente permiten descartar estos usos; el resto de fotografías debe revisarse una por una antes de aprobación definitiva.

## Cantidad de trabajo visual

| Concepto | Pendiente |
|---|---:|
| Posiciones de materiales sin imagen | 265 |
| Una imagen de biocarbón repetida para dos subbases | 1 |
| Rehacer escenas internas de ECOALDEAS | 10 |
| Rehacer escenas generales de ECOALDEAS | 10 |
| Rehacer productos orgánicos recortados | 10 |
| Sustituir referencias claramente incorrectas | 12 |
| **Total de producción/sustitución planificada** | **308** |

**31 grupos internos**, a máximo diez imágenes por grupo: 30 grupos de diez y uno final de 8. Cifra preliminar: futuras correcciones estéticas, nuevos módulos o decisiones de reutilización legítima pueden modificarla.

## Qué imágenes siguen pendientes de subir

Las **cuatro láminas PNG históricas** de `ECOALDEAS_PROPUESTAS/01_red_territorial.png`, `02_plan_maestro.png`, `03_unidad_familiar.png`, `04_cadena_circular.png` fueron producidas en la conversación, pero **no aparecen como esos cuatro archivos en el árbol público**. La página de propuestas usa cuatro ilustraciones alternativas `assets/biblioteca/ecoaldeas/fuentes/*.jpg`, una por pestaña; no debe decirse que son las cuatro PNG originales. Asimismo, distintas infografías con nombres locales del chat no figuran como archivos autónomos en GitHub. Se consideran **materiales fuente en revisión** y no incrementan automáticamente las 70 imágenes de biblioteca.

## Criterios de aprobación antes de subir un lote

- Un solo sujeto/proceso inequívoco y correctamente identificado por nombre.
- Imagen individual sin manchas negras, bordes extraños, texto IA defectuoso, círculos superpuestos ni collage doble.
- No incrustar número de paquete ni sello o logo generado; usar el **logo original** desde la web.
- Alternativa textual, etapa del flujo, destino de producto y advertencias técnicas coherentes.
- Imagen local WebP/JPG/PNG, sin dependencia de enlaces externos; clic abre un visor interno.
- Registro en un manifiesto único por nodo; verificar archivo, imagen, título y ubicación en web.
- Móvil y PC con imagen nítida, sin `object-fit:cover` que recorte contenido explicativo.
- Las imágenes de actividades propuestas se marcan como **ilustraciones IA** y no pruebas de producción instalada.

Consulta [el inventario completo](./INVENTARIO_NODOS_2026-10-25.csv) y [los 31 grupos internos](./PLAN_GRUPOS_IMAGENES_2026-10-25.json).
