/* ECORECYCLE v1.4 — 100% imagenes locales, cero enlaces externos desde las fotografias. */
(()=>{
"use strict";
const base="./assets/biblioteca/reciclables-secos/";
const pending=[];
let packItems=[],metalItems=[],organicItems=[],publicCredits=[],booted=false;
const clean=s=>String(s||"").replace(/\*+$/,"").trim();
const slug=s=>clean(s).toLowerCase().replaceAll("¾","tres-cuartos").replaceAll("½","medio").replaceAll("⅜","tres-octavos")
 .normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
async function load(){
 try{const r=await fetch(base+"manifest.json",{cache:"no-cache"});if(r.ok)packItems=(await r.json()).imagenes||[];}catch(_){}
 try{const r=await fetch("./assets/fotos/creditos.json");if(r.ok)publicCredits=(await r.json()).fuentes||[];}catch(_){}
 try{const r=await fetch('./assets/biblioteca/metales/manifest.json');if(r.ok)metalItems=(await r.json()).imagenes||[];}catch(_){}
 try{const r=await fetch('./assets/biblioteca/organicos/manifest.json');if(r.ok)organicItems=(await r.json()).imagenes||[];}catch(_){}
 booted=true;paint();
}
function exactPack(group,name){
 if(active!=="reciclables")return null;
 const x=packItems.find(x=>x.tipo===group&&clean(x.nombre)===clean(name));
 return x?.archivo?{src:"./"+x.archivo,label:x.nombre,alt:x.alt||x.nombre,license:x.licencia||"Ilustracion original IA",credit:x.autor||"Fundación Ecopiensa Evolution",kind:"Imagen generada con IA, ilustrativa"}:null;
}
function localSub(group,name){
 const p=exactPack(group,name);if(p)return p;
 if(active==='metales'){const z=metalItems.find(x=>x.tipo===group&&clean(x.nombre)===clean(name)&&x.archivo);if(z)return {src:'./'+z.archivo,label:z.nombre,alt:z.nombre,license:z.licencia||'Ver créditos',credit:z.autor||'Wikimedia Commons',kind:'Fotografía de referencia local bajo licencia indicada'};}
 const x=publicCredits.find(x=>x.material===active&&clean(x.subbase)===clean(name));
 return x?.filename?{src:"./"+x.filename,label:name,alt:name,license:x.license||"Licencia no registrada",credit:x.creator||"Autor no registrado",kind:"Fotografia externa ilustrativa alojada localmente"}:null;
}
function productFor(name){
 const pack=exactPack("productos",name);if(pack)return pack;
 if(active==='organicos'){const item=organicItems.find(x=>clean(x.nombre)===clean(name));if(item)return {src:'./'+item.archivo,label:item.nombre,alt:item.alt||item.nombre,license:'Creación original generada con IA',credit:'Fundación Ecopiensa Evolution',kind:'Ilustración conceptual de producto orgánico; uso agrícola condicionado a calidad y normativa'};}
 if(active==='metales'){const z=metalItems.find(x=>x.tipo==='productos'&&clean(x.nombre)===clean(name)&&x.archivo);if(z)return {src:'./'+z.archivo,label:z.nombre,alt:z.nombre,license:z.licencia||'Ver créditos',credit:z.autor||'Wikimedia Commons',kind:'Fotografía de referencia local bajo licencia indicada'};}
 // Las siguientes entregas se resolveran mediante sus propios manifiestos, nunca por fotos de otro producto.
 return null;
}
function nodePhoto(source,label,variant){
 const slot=document.createElement("div");slot.className="local-image-slot "+variant;
 if(source?.src){
  const btn=document.createElement("button");btn.type="button";btn.className="local-photo-button";
  btn.setAttribute("aria-label","Ampliar imagen de "+label+" dentro de la página");
  const img=document.createElement("img");img.src=source.src;img.alt=source.alt||label;img.loading="lazy";
  img.addEventListener("error",()=>{btn.replaceWith(placeholder(label));},{once:true});
  btn.appendChild(img);btn.addEventListener("click",()=>openPreview(source,label));
  slot.appendChild(btn);
 }else slot.appendChild(placeholder(label));
 return slot;
}
function placeholder(name){
 const div=document.createElement("div");div.className="image-pending";div.setAttribute("role","status");
 div.textContent="Imagen pendiente";div.title="Pendiente de imagen individual: "+name;return div;
}
function buildDialog(){
 if(document.querySelector("#ecorecycle-viewer"))return;
 const dialog=document.createElement("dialog");dialog.id="ecorecycle-viewer";dialog.setAttribute("aria-label","Visor de imágenes ECORECYCLE");
 dialog.innerHTML='<div class="viewer-top"><strong id="viewer-title"></strong><button class="viewer-close" type="button" aria-label="Cerrar visor">Cerrar ×</button></div><img id="viewer-img" alt=""><div class="viewer-details" id="viewer-details"></div>';
 document.body.appendChild(dialog);
 dialog.querySelector(".viewer-close").addEventListener("click",()=>dialog.close());
 dialog.addEventListener("click",e=>{if(e.target===dialog)dialog.close();});
}
function openPreview(info,label){
 buildDialog();
 const d=document.querySelector("#ecorecycle-viewer");
 document.querySelector("#viewer-title").textContent=label;
 const im=document.querySelector("#viewer-img");im.src=info.src;im.alt=info.alt||label;
 document.querySelector("#viewer-details").textContent=info.kind+" · "+info.credit+" · "+info.license+" · Imagen ilustrativa, no certifica producción propia.";
 if(typeof d.showModal==="function")d.showModal();else d.setAttribute("open","");
}
function paint(){
 if(!booted||typeof DATA==="undefined"||typeof active==="undefined")return;
 const material=DATA.find(c=>c.id===active);if(!material)return;
 const cards=[...document.querySelectorAll("#cards .item")];
 for(const card of cards){
  const heading=card.querySelector(".itemHead"),name=heading?.textContent?.trim();
  if(!name)continue;
  const visual=card.querySelector(".visual");
  if(visual){visual.innerHTML="";visual.appendChild(nodePhoto(localSub("subbases",name),name,"subbase-photo"));}
  for(const product of card.querySelectorAll(".product")){
   const span=product.querySelector("span:last-child");
   if(!span)continue;
   const label=span.textContent.trim();
   for(const elem of [...product.children])if(elem!==span)elem.remove();
   product.insertBefore(nodePhoto(productFor(label),label,"producto-photo"),span);
  }
 }
 const icon=document.querySelector("#baseIcon");
 if(icon){
  icon.innerHTML="";
  // La foto de base se toma de la primera subbase adecuada, pero se etiqueta como ilustración general.
  const first=material.b[0]?.[0];
  icon.appendChild(nodePhoto(first?localSub("subbases",first):null,material.n,"base-photo"));
 }
}
const previous=window.draw;
if(typeof previous==="function"){window.draw=function(){previous();paint();};}
document.addEventListener("DOMContentLoaded",load,{once:true});
if(document.readyState!=="loading")load();
})();
