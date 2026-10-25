(()=>{"use strict";
const topics={
rio:["crushed aggregate stones quarry","gravel stones","gravel construction aggregate","small gravel quarry","cement grout sand","coarse sand construction"],
reciclables:["corrugated cardboard recycling","paper recycling stacks","PET plastic bottles recycling","plastic HDPE containers recycling","scrap metal recycling"],
organicos:["fruit vegetable compost waste","garden waste leaves branches","cow manure compost agriculture","agricultural crop residue straw","kitchen food scraps compost","wastewater treatment sludge"],
rcd:["crushed concrete rubble","brick demolition waste","ceramic tile debris","soil aggregate construction","metal waste demolition","asphalt pavement milling"],
plasticos:["PET plastic bottles","HDPE plastic jerrycan","LDPE plastic wrap film","polypropylene plastic food containers","mixed recyclable plastics","polystyrene foam waste"],
papel_carton:["cardboard corrugated boxes stack","white paper stacks","waste paper recycling","old newspapers stack","Tetra Pak carton"],
metales:["aluminium beverage cans scrap","copper wire scrap metal","steel beams scrap metal","stainless steel scrap","brass bronze scrap recycling"],
madera:["wood pallets stacked","wood offcuts timber","sawdust woodworking","wood chips mulch","wood waste sorting"],
vidrio:["glass bottles recycling","clear glass cullet","green glass bottle recycling","brown amber glass bottles","broken mixed glass recycling"],
llantas:["used car tires stack","crumb rubber granules","black rubber powder","steel wire scrap tire","tire pyrolysis industrial reactor"],
aceites:["used cooking oil container","animal fat grease","used motor oil drums","oil filters automotive waste","contaminated oil containers"],
textiles:["second hand clothing reuse","cotton fabric scrap","denim jeans upcycle","polyester fabric scrap","mixed textile waste"],
raee:["refurbished computer laptops","electric cable copper scrap","electronic printed circuit board recycling","old computer plastic casing","rechargeable battery waste"]
};
const memo=new Map(),pending=[],seen=new WeakSet();let running=0;
const creditList=fetch("./assets/fotos/creditos.json").then(r=>r.ok?r.json():null).then(d=>d?.fuentes||[]).catch(()=>[]);
function slug(s){return s.toLowerCase().replaceAll("¾","tres-cuartos").replaceAll("½","medio").replaceAll("⅜","tres-octavos").normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,100);}
function localPhoto(img,local,query){
 img.addEventListener("error",()=>{pending.push([img,query]);pump();},{once:true});
 img.addEventListener("load",async()=>{img.classList.add("is-loaded");const credits=await creditList;
 const v=credits.find(x=>("./"+x.filename)===local);const a=img.closest("a");
 if(v&&a){a.href=v.source;a.target="_blank";a.rel="noopener noreferrer";a.title="Wikimedia Commons · "+v.original_title+" · "+v.license;}
 },{once:true});
 img.src=local;
}
const productPatterns=[
[/compost|bokashi|abono/i,"mature compost soil"],
[/humus|lombriz/i,"vermicompost earthworms"],
[/biogás|biodigest/i,"anaerobic biogas digester tanks"],
[/biocarbón|biochar/i,"biochar charcoal pieces"],
[/briqueta|pellet/i,"wood biomass briquettes pellets"],
[/hongo|seta/i,"oyster mushroom growing substrate"],
[/acolchado|astilla/i,"wood chips mulch"],
[/fertilizante|enmienda|suelo/i,"organic fertilizer soil bags"],
[/adoquín|loseta|piso/i,"concrete paving stones"],
[/bloque|ladrillo/i,"concrete construction blocks bricks"],
[/tubería|canal/i,"concrete drainage pipes"],
[/filamento|impresión 3D/i,"3d printing filament spool"],
[/prótesis/i,"3D printed prosthetic hand"],
[/madera plástica/i,"recycled plastic lumber"],
[/escoba|cerda/i,"plastic broom brush"],
[/mueble|silla|mesa/i,"outdoor furniture recycled"],
[/papel|cuaderno|libreta/i,"recycled paper notebook"],
[/caja|cartón|embalaje/i,"cardboard packaging boxes"],
[/vidrio|mosaico/i,"recycled glass mosaic"],
[/cobre|metal|acero|chatarra/i,"recycled scrap steel copper metal"],
[/llanta|caucho|tapete/i,"recycled rubber tile floor"],
[/biodiésel|aceite|jabón/i,"biodiesel used cooking oil"],
[/textil|ropa|bolso/i,"recycled textile clothing"],
[/electrón|computador|repuesto/i,"electronic recycling computers"],
[/vía|asfalto|carretera/i,"asphalt roadway construction"]
];
function searchTerm(product,cat,i){const hit=productPatterns.find(([re])=>re.test(product));return hit?hit[1]:(topics[cat]||[])[i]||cat+" recycling material"}
async function commons(query){
 const p=new URLSearchParams({action:"query",generator:"search",gsrsearch:query,gsrnamespace:"6",gsrlimit:"10",prop:"imageinfo",iiprop:"url|mime|extmetadata",iiurlwidth:"540",format:"json",origin:"*"});
 const r=await fetch("https://commons.wikimedia.org/w/api.php?"+p.toString());if(!r.ok)throw Error("Photo network unavailable");
 const j=await r.json();const a=Object.values(j.query?.pages||{}).sort((a,b)=>(a.index||0)-(b.index||0));
 for(const e of a){const ii=e.imageinfo?.[0];if(!ii||ii.mime!=="image/jpeg")continue;
 const lic=ii.extmetadata?.LicenseShortName?.value||"";if(!/(cc0|public domain|cc-by|cc by|CC BY|CC0)/i.test(lic))continue;
 if(ii.thumburl)return {src:ii.thumburl,page:ii.descriptionurl||ii.url,license:lic,name:e.title}}
 return null;
}
function put(img,query,local){
 if(!query||seen.has(img))return;seen.add(img);if(local){localPhoto(img,local,query)}else{pending.push([img,query]);pump()}
}
function pump(){while(running<3&&pending.length){const [img,q]=pending.shift();if(!img.isConnected)continue;running++;
 if(!memo.has(q))memo.set(q,commons(q).catch(()=>null));
 memo.get(q).then(v=>{if(!v||!img.isConnected)return;
 img.addEventListener("load",()=>img.classList.add("is-loaded"),{once:true});img.src=v.src;
 img.alt="Fotografía ilustrativa: "+q;
 const a=img.closest("a");if(a){a.href=v.page;a.target="_blank";a.rel="noopener noreferrer";a.title="Foto externa: "+v.name+" · licencia "+v.license;}
 img.title="Wikimedia Commons · "+v.name+" · "+v.license;
 }).finally(()=>{running--;pump()});
}}
function applyPhotos(){
 const cat=window.DATA?window.DATA.find(x=>x.id===window.active):null;
 const chosen=cat||((typeof DATA!=="undefined")?DATA.find(x=>x.id===active):null);if(!chosen)return;
 document.querySelectorAll(".item").forEach(card=>{
 const label=card.querySelector(".itemHead")?.textContent||"";
 const ix=chosen.b.findIndex(b=>b[0]===label);if(ix<0)return;
 const target=card.querySelector(".visual");if(target&&!target.querySelector(".eco-photo")){
  const a=document.createElement("a");a.className="eco-photo-link";a.setAttribute("aria-label","Abrir procedencia y licencia de la foto");
  const img=document.createElement("img");img.className="eco-photo";img.loading="lazy";
  a.appendChild(img);target.appendChild(a);put(img,(topics[chosen.id]||[])[ix]||label+" material recycling","./assets/fotos/"+chosen.id+"/"+slug(label)+".jpg");
 }
 card.querySelectorAll(".product").forEach((p,i)=>{if(p.querySelector(".eco-thumb"))return;
 const label=p.textContent.trim();const img=document.createElement("img");img.className="eco-thumb";
 img.alt="Referencia visual: "+label;img.loading="lazy";p.insertBefore(img,p.firstChild);
 put(img,searchTerm(label,chosen.id,i));
 });
 });
}
const prev=window.draw;if(typeof prev==="function"){window.draw=function(){prev();applyPhotos()};}
applyPhotos();
})();