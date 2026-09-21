/* ================================================================
   CRAFTING TEST  -  materials, recipes, rarity, the morning workshop
   ================================================================ */
const CRAFT=%%CFG%%;
const DEMO={caravans:!CRAFT.demo, days:7};
const RAR=[
  {n:'COMMON',   m:1,   col:'#a08e74', day:1},
  {n:'RARE',     m:2.2, col:'#5f9fd0', day:1},
  {n:'EPIC',     m:6,   col:'#a173c8', day:5},
  {n:'LEGENDARY',m:16,  col:'#e8b13c', day:10}
];
const MATS=[
  {id:'scrap', n:'Scrap',     c:16, pal:{a:'#8a8178',b:'#b8aea0'}, px:['..kkkk..','.kabbak.','kabaabak','kaakkaak','kaakkaak','kabaabak','.kaaaak.','..kkkk..']},
  {id:'timber',n:'Timber',    c:32, pal:{a:'#7a5738',b:'#a87c4f'}, px:['........','kkkkkkkk','kbbbbbbk','kaaaaaak','kbbabbak','kaaaaaak','kkkkkkkk','........']},
  {id:'cloth', n:'Cloth',     c:16, pal:{a:'#c9b48f',b:'#efe3cb'}, px:['.kkkkkk.','kbbbbbbk','kabababk','kbbbbbbk','kabababk','kbbbbbbk','kaaaaaak','.kkkkkk.']},
  {id:'herbs', n:'Herbs',     c:32, pal:{a:'#4f8a3c',b:'#7fb74f'}, px:['....kk..','...kbbk.','.kkkbbak','kbbkbak.','kbbakak.','.kaakk..','..kkak..','....k...']},
  {id:'grain', n:'Grain',     c:16, pal:{a:'#b8923c',b:'#e8c86a'}, px:['..kkkk..','..kaak..','.kkkkkk.','kbbbbbak','kbabbaak','kbbbbaak','kaaaaaak','.kkkkkk.']},
  {id:'glass', n:'Glass',     c:32, pal:{a:'#6fb8d8',b:'#c8ecf8'}, px:['...kk...','..kbbk..','..kbak..','.kbbaak.','kbbaaaak','kbaaaaak','kaaaaaak','.kkkkkk.']},
  {id:'chem',  n:'Chem',      c:48, pal:{a:'#a173c8',b:'#d8b8f0'}, px:['..kkkk..','...kk...','...kk...','..kbbk..','.kbbbak.','kbaaaaak','kaaaaaak','.kkkkkk.']},
  {id:'wire',  n:'Wire',      c:64, pal:{a:'#c8703a',b:'#f0a868'}, px:['.kkkkkk.','kbbbbbbk','k.kkkk.k','kbbbbbbk','k.kkkk.k','kaaaaaak','k.kkkk.k','.kkkkkk.']},
  {id:'fine',  n:'Fine Parts',c:144, unlock:1000, day:5, pal:{a:'#a173c8',b:'#e0c8f4'}, px:['.k.kk.k.','kbkbbkbk','.kbaabk.','kba..abk','kba..abk','.kbaabk.','kakaakak','.k.kk.k.']},
  {id:'relic', n:'Relic Core',c:384, unlock:2000,day:10, pal:{a:'#e8b13c',b:'#fff0b0'}, px:['...kk...','..kbbk..','.kbbbak.','kbbbaaak','kabaaaak','.kaaaak.','..kaak..','...kk...']}
];
const MATBY={}; MATS.forEach(m=>{ MATBY[m.id]=m; m.spr=spriteFrom(m.px,Object.assign({k:'#1a1410'},m.pal)); });
/* item id -> [material A, material B, workbench-day the recipe opens, how many one craft yields]
   Goods sell at about half their value, so the cheap ones come out in pairs or they would never pay. */
const RECIPES={
  pipegun:['scrap','timber',1,1], bandage:['cloth','herbs',1,2], beans:['grain','glass',1,2], board:['cloth','wire',1,2],
  cans:['grain','scrap',2,2],     shells:['scrap','chem',2,2],
  stimpak:['glass','chem',3,1],   water:['glass','cloth',3,1],
  cell:['wire','scrap',4,1],      tape:['cloth','cloth',4,2],
  knife:['scrap','cloth',5,1],    mutfruit:['grain','grain',5,2],
  radaway:['herbs','glass',6,1],  terminal:['wire','glass',6,1], scrap:['scrap','scrap',6,2]
};
ITEMS.forEach(it=>{ it.r=0; it.base=it; });
const VARIANT={};
/* rarity and "made at the bench" are variants of the same item id, so every drag / sell / want path is untouched.
   Hand-made goods are worth CRAFT.mult times a caravan piece of the same tier. */
function rar(item,r,crafted){
  const b=item.base||item; r=r||0;
  if(crafted===undefined) crafted=!!item.crafted;
  if(!r&&!crafted) return b;
  const k=b.id+r+(crafted?'c':'');
  if(!VARIANT[k]) VARIANT[k]=Object.assign({},b,{r:r,base:b,crafted:crafted,v:Math.round(b.v*RAR[r].m*(crafted?CRAFT.mult:1))});
  return VARIANT[k];
}
/* the barrel pays for the object, not for the craftsmanship - or scrapping fresh work would turn a profit */
function scrapValue(item){ return Math.max(1,Math.round((item.base||item).v*RAR[item.r||0].m*0.25)); }
function unlockMat(m){
  if(S.unl[m.id]||S.caps<m.unlock){ Snd.bad(); return; }
  S.caps-=m.unlock; S.unl[m.id]=true; S.cr.spent+=m.unlock; Snd.coin(6); flash(m.pal.a,0.2);
}
/* demo: the workshop is this morning. main game: it is tonight, stocking for tomorrow, and the
   recipe / tier calendar counts from the day the bench was bought. */
function effDay(){ return CRAFT.demo ? S.day : S.day+1; }
function craftDay(){ return CRAFT.demo ? S.day : Math.max(1,effDay()-S.wbDay+1); }
function recipeOpen(it){ return craftDay()>=RECIPES[it.id][2]; }
function openItems(cat){ return BYCAT[cat].filter(recipeOpen); }
function purseR(c){ return clamp(c.type.tier,1,3); }            /* richest tier this customer pays full price for */
function billOf(list){ const o={}; list.forEach(p=>{ if(p[1]>0) o[p[0]]=(o[p[0]]||0)+p[1]; }); return o; }
function recipeBill(it){ const rc=RECIPES[it.id]; return billOf([[rc[0],1],[rc[1],1]]); }
function upgradeBill(item){
  const r=(item.r||0)+1, rc=RECIPES[item.base.id];
  return billOf([[rc[0],[0,2,3,4][r]],[rc[1],[0,1,3,4][r]],['fine',[0,0,1,2][r]],['relic',r===3?1:0]]);
}
function billCost(b){ let s=0; for(const k in b) s+=MATBY[k].c*b[k]; return s; }
function billMissing(b){ for(const k in b) if((S.mats[k]||0)<b[k]) return MATBY[k]; return null; }
function payBill(b){ for(const k in b) S.mats[k]-=b[k]; }
function billText(b){ return Object.keys(b).map(k=>(b[k]>1?b[k]+' ':'')+MATBY[k].n).join(' + '); }
function craftReset(){
  S.mats={}; MATS.forEach(m=>S.mats[m.id]=0);
  S.tray=new Array(17).fill(null); S.back=[]; S.backT=0; S.anvil=null; S.wd=null; S.wsTab='guns';
  S.wb=CRAFT.demo; S.wbDay=1; WT.on=false; WT.done=false;
  S.unl={fine:false,relic:false};
  S.cr={spent:0,daySpent:0,crafted:0,up:[0,0,0,0],soldR:[0,0,0,0],capped:0,wsTime:0,scrapped:0};
}
function buyMat(m,n){
  if((m.day&&craftDay()<m.day)||(m.unlock&&!S.unl[m.id])) return;
  const cost=m.c*n;
  if(S.caps<cost){ Snd.bad(); return; }
  S.caps-=cost; S.mats[m.id]+=n; S.cr.spent+=cost; S.cr.daySpent+=cost; Snd.coin(1);
}
function trayFree(){ let n=0; S.tray.forEach(x=>{ if(!x) n++; }); return n; }
function craft(it){
  const b=recipeBill(it), n=RECIPES[it.id][3];
  if(!recipeOpen(it)||billMissing(b)||trayFree()<n){ Snd.bad(); return false; }
  payBill(b);
  for(let k=0;k<n;k++){ const free=S.tray.indexOf(null); S.tray[free]=rar(it,0,true); S.cr.crafted++; S.cr.up[0]++;
    const q=trayRect(free); burst(q.x+q.w/2,q.y+q.h/2,CATS[it.cat].col,8,120); }
  Snd.good();
  return true;
}
/* scrapping hands back half of every material that went into the object (its share of a paired craft) */
function spentOn(item){
  const b=item.base||item, rc=RECIPES[b.id], o={};
  o[rc[0]]=(o[rc[0]]||0)+1/rc[3]; o[rc[1]]=(o[rc[1]]||0)+1/rc[3];
  let cur=b; for(let u=0;u<(item.r||0);u++){ const ub=upgradeBill(cur); for(const k in ub) o[k]=(o[k]||0)+ub[k]; cur=rar(cur,u+1); }
  return o;
}
function scrapYield(item){
  const sp=spentOn(item), o={}; let any=false;
  for(const k in sp){ const n=Math.floor(sp[k]/2); if(n>0){ o[k]=n; any=true; } }
  if(!any) o[RECIPES[(item.base||item).id][0]]=1;
  return o;
}
function scrapItem(item){
  const y=scrapYield(item); for(const k in y) S.mats[k]+=y[k];
  S.cr.scrapped++;
  const q=binRect(); dust(q.x+q.w/2,q.y+q.h/2,8); float(q.x+q.w/2,q.y-4,'+'+billText(y),C.dim,11); Snd.drop();
}
function canUpgrade(item){
  if(!item) return 'empty';
  const r=(item.r||0)+1;
  if(r>3) return 'max';
  if(craftDay()<RAR[r].day) return 'day';
  { const ub=upgradeBill(item); for(const k in ub) if(MATBY[k].unlock&&!S.unl[k]) return 'lock'; }
  return billMissing(upgradeBill(item)) ? 'short' : 'ok';
}
function doUpgrade(){
  if(canUpgrade(S.anvil)!=='ok'){ Snd.bad(); return false; }
  payBill(upgradeBill(S.anvil));
  S.anvil=rar(S.anvil,S.anvil.r+1); S.cr.up[S.anvil.r]++;
  const a=anvilRect(); burst(a.x+a.w/2,a.y+a.h/2,RAR[S.anvil.r].col,22,240);
  float(a.x+a.w/2,a.y-6,RAR[S.anvil.r].n+'!',RAR[S.anvil.r].col,20);
  flash(RAR[S.anvil.r].col,0.18); Snd.coin(4+S.anvil.r*2);
  return true;
}
/* ---------------- workshop layout ---------------- */
const WS={mk:{x:16,y:70,w:290,h:676}, wb:{x:318,y:70,w:440,h:676}, sh:{x:770,y:70,w:494,h:676}};
function anvilRect(){ return {x:WS.wb.x+18,y:WS.wb.y+330,w:96,h:96}; }
function trayRect(i){ return {x:WS.wb.x+16+(i%6)*69,y:WS.wb.y+512+Math.floor(i/6)*54,w:64,h:50}; }
function binRect(){ return trayRect(17); }
function wsShelfRect(i){ return {x:WS.sh.x+12,y:WS.sh.y+44+i*132,w:WS.sh.w-24,h:126}; }
function wsSlotRect(i,j){ const r=wsShelfRect(i), sw=Math.floor((r.w-18)/4); return {x:r.x+j*(sw+6),y:r.y+24,w:sw,h:r.h-24}; }
function wsStocked(){ return stockCount()>0; }
function wsStep(){
  let mats=0; for(const k in S.mats) mats+=S.mats[k];
  const goods=S.tray.some(x=>x)||!!S.anvil;
  if(wsStocked()&&!goods) return 4;
  if(goods) return 3;
  if(mats>=2) return 2;
  return 1;
}
function wsPick(x,y){
  for(let i=0;i<17;i++) if(S.tray[i]&&inRect(x,y,trayRect(i))){ S.wd={item:S.tray[i],from:{k:'tray',i:i},x:x,y:y}; S.tray[i]=null; Snd.pick(); return; }
  if(S.anvil&&inRect(x,y,anvilRect())){ S.wd={item:S.anvil,from:{k:'anvil'},x:x,y:y}; S.anvil=null; Snd.pick(); return; }
  for(let i=0;i<S.shelves.length;i++){
    const hr=wsShelfRect(i);
    if(inRect(x,y,{x:hr.x,y:hr.y,w:hr.w,h:22})&&!S.shelves[i].slots.some(s=>s)){
      const cats=activeCats(); S.shelves[i].cat=cats[(cats.indexOf(S.shelves[i].cat)+1)%cats.length]; Snd.ui(); return;
    }
    for(let j=0;j<4;j++){ const e=S.shelves[i].slots[j];
      if(e&&inRect(x,y,wsSlotRect(i,j))){ S.wd={item:e.item,from:{k:'shelf',i:i,j:j},x:x,y:y}; S.shelves[i].slots[j]=null; Snd.pick(); return; } }
  }
}
function wsPut(to,item){
  if(to.k==='tray') S.tray[to.i]=item;
  else if(to.k==='anvil') S.anvil=item;
  else { const sh=S.shelves[to.i]; sh.slots[to.j]={item:item,misfiled:sh.cat!==item.cat,arriving:0,anim:1}; }
}
function wsDrop(x,y){
  const d=S.wd; if(!d) return; S.wd=null;
  let to=null;
  if(inRect(x,y,anvilRect())&&!S.anvil) to={k:'anvil'};
  if(inRect(x,y,binRect())){ scrapItem(d.item); return; }
  for(let i=0;i<17&&!to;i++) if(!S.tray[i]&&inRect(x,y,trayRect(i))) to={k:'tray',i:i};
  for(let i=0;i<S.shelves.length&&!to;i++) for(let j=0;j<4&&!to;j++)
    if(!S.shelves[i].slots[j]&&inRect(x,y,wsSlotRect(i,j))) to={k:'shelf',i:i,j:j};
  if(!to){ wsPut(d.from,d.item); Snd.drop(); return; }
  wsPut(to,d.item);
  if(to.k==='shelf'){
    const q=wsSlotRect(to.i,to.j), mis=S.shelves[to.i].cat!==d.item.cat;
    float(q.x+q.w/2,q.y+8,mis?'WRONG SHELF x0.5':'STOCKED',mis?C.red:C.green,13); mis?Snd.bad():Snd.good();
  } else Snd.drop();
}
function wsScrapAt(x,y){
  for(let i=0;i<17;i++) if(S.tray[i]&&inRect(x,y,trayRect(i))){ const it=S.tray[i]; S.tray[i]=null; scrapItem(it); return true; }
  if(S.anvil&&inRect(x,y,anvilRect())){ const it=S.anvil; S.anvil=null; scrapItem(it); return true; }
  for(let i=0;i<S.shelves.length;i++) for(let j=0;j<4;j++){ const e=S.shelves[i].slots[j];
    if(e&&inRect(x,y,wsSlotRect(i,j))){ S.shelves[i].slots[j]=null; scrapItem(e.item); return true; } }
  return false;
}
function rarFrame(q,item,inset){
  if(!item||(!item.r&&!item.crafted)) return;
  const c=item.r?RAR[item.r].col:'#c9a978', k=inset||2;
  if(item.crafted){ g.fillStyle=c; g.fillRect(q.x+q.w-k-9,q.y+q.h-k-4,7,2); g.fillRect(q.x+q.w-k-4,q.y+q.h-k-9,2,7); }   /* maker's notch */
  g.fillStyle=rgba(c,item.r?0.16:0.07); g.fillRect(q.x+k,q.y+k,q.w-k*2,q.h-k*2);
  g.fillStyle=c;
  g.fillRect(q.x+k,q.y+k,q.w-k*2,2); g.fillRect(q.x+k,q.y+q.h-k-2,q.w-k*2,2);
  g.fillRect(q.x+k,q.y+k,2,q.h-k*2); g.fillRect(q.x+q.w-k-2,q.y+k,2,q.h-k*2);
  for(let p=0;p<item.r;p++) g.fillRect(q.x+k+5+p*7,q.y+k+5,5,5);
}
function wsCell(q,hot){
  g.fillStyle='#191310'; g.fillRect(q.x,q.y,q.w,q.h);
  g.fillStyle=hot?C.gold:'#33291f';
  g.fillRect(q.x,q.y,q.w,2); g.fillRect(q.x,q.y+q.h-2,q.w,2); g.fillRect(q.x,q.y,2,q.h); g.fillRect(q.x+q.w-2,q.y,2,q.h);
}
function wsGlow(p){
  const a=0.45+Math.sin(S.t*5)*0.3; g.globalAlpha=a; g.fillStyle=C.gold;
  g.fillRect(p.x-3,p.y-3,p.w+6,3); g.fillRect(p.x-3,p.y+p.h,p.w+6,3);
  g.fillRect(p.x-3,p.y,3,p.h); g.fillRect(p.x+p.w,p.y,3,p.h); g.globalAlpha=1;
}
function drawWorkshop(){
  dim(0.82);
  const step=wsStep(), mk=WS.mk, wb=WS.wb, sh=WS.sh;
  /* ---- material market ---- */
  plate(mk.x,mk.y,mk.w,mk.h,'#1a1410','#6b5540','#8a6f50');
  txt('MATERIAL MARKET',mk.x+14,mk.y+22,15,C.gold);
  txt('fixed prices',mk.x+mk.w-14,mk.y+22,10,C.dimmer,'right','normal');
  MATS.forEach((m,i)=>{
    const y=mk.y+44+i*62, locked=m.day&&craftDay()<m.day;
    plate(mk.x+8,y,mk.w-16,56,'#211a14',locked?'#33291f':'#4a3b2c');
    blit(m.spr,mk.x+18,y+12,4,locked?0.3:1);
    txt(m.n,mk.x+60,y+18,12,locked?C.dimmer:C.ink);
    if(locked){ txt(CRAFT.demo?('opens day '+m.day):('in '+(m.day-craftDay())+' day'+(m.day-craftDay()>1?'s':'')),mk.x+60,y+38,10,C.dimmer,'left','normal'); return; }
    if(m.unlock&&!S.unl[m.id]){
      txt('pay once: '+m.unlock+'c',mk.x+60,y+38,10,C.dim,'left','normal');
      button(mk.x+178,y+12,96,32,'UNLOCK',()=>unlockMat(m),S.caps>=m.unlock?C.gold:C.dimmer,11); return; }
    txt(m.c+'c each',mk.x+60,y+38,10,C.dim,'left','normal');
    txt('x'+S.mats[m.id],mk.x+170,y+38,14,S.mats[m.id]?C.gold:C.dimmer,'right');
    button(mk.x+178,y+12,44,32,'+1',()=>buyMat(m,1),S.caps>=m.c?C.gold:C.dimmer,12);
    button(mk.x+228,y+12,46,32,'+5',()=>buyMat(m,5),S.caps>=m.c*5?C.gold:C.dimmer,12);
  });
  /* ---- workbench ---- */
  plate(wb.x,wb.y,wb.w,wb.h,'#1a1410','#6b5540','#8a6f50');
  txt('WORKBENCH',wb.x+14,wb.y+22,15,C.gold);
  txt('click a recipe to make one',wb.x+wb.w-14,wb.y+22,10,C.dimmer,'right','normal');
  const cats=activeCats().filter(c=>c!=='junk'), tw=Math.floor((wb.w-24-(cats.length-1)*4)/cats.length);
  if(cats.indexOf(S.wsTab)<0) S.wsTab=cats[0];
  cats.forEach((c,i)=>{
    const tx=wb.x+12+i*(tw+4), on=S.wsTab===c;
    plate(tx,wb.y+40,tw,30,on?'#33281c':'#14100c',on?CATS[c].col:'#4a3b2c');
    txt(CATS[c].name,tx+tw/2,wb.y+55,11,on?CATS[c].col:C.dimmer,'center');
    BTNS.push({x:tx,y:wb.y+40,w:tw,h:30,fn:()=>{S.wsTab=c;}});
  });
  BYCAT[S.wsTab].forEach((it,i)=>{
    const y=wb.y+80+i*74, r={x:wb.x+12,y:y,w:wb.w-24,h:68}, open=recipeOpen(it), b=recipeBill(it);
    const yl=RECIPES[it.id][3], miss=open?billMissing(b):null, full=trayFree()<yl, ok=open&&!miss&&!full, hov=ok&&inRect(MX,MY,r);
    plate(r.x,r.y,r.w,r.h,hov?'#33281c':'#211a14',ok?CATS[it.cat].col:'#3a3228');
    drawItem(it,r.x+34,r.y+34,3,open?1:0.25);
    txt(it.n.toUpperCase()+(yl>1?'  x'+yl:''),r.x+70,r.y+20,13,open?C.ink:C.dimmer);
    if(!open){ const dd=RECIPES[it.id][2]-craftDay(); txt(CRAFT.demo?('recipe opens day '+RECIPES[it.id][2]):('recipe opens in '+dd+' day'+(dd>1?'s':'')),r.x+70,r.y+44,10,C.dimmer,'left','normal'); return; }
    txt(billText(b)+'  ·  '+billCost(b)+'c',r.x+70,r.y+40,10,C.dim,'left','normal');
    txt('sells about '+Math.round(it.v*0.5*CRAFT.mult)+'c each',r.x+70,r.y+56,9,C.dimmer,'left','normal');
    if(miss) txt('need '+miss.n,r.x+r.w-12,r.y+34,11,C.red,'right');
    else if(full) txt('tray full',r.x+r.w-12,r.y+34,11,C.red,'right');
    else { txt('CRAFT',r.x+r.w-12,r.y+34,13,CATS[it.cat].col,'right'); BTNS.push({x:r.x,y:r.y,w:r.w,h:r.h,fn:()=>craft(it)}); }
  });
  /* anvil */
  txt('REFINE',wb.x+14,wb.y+314,13,C.gold);
  txt('common > rare > epic > legendary',wb.x+wb.w-14,wb.y+314,10,C.dimmer,'right','normal');
  const a=anvilRect(), st=canUpgrade(S.anvil);
  wsCell(a,S.wd&&inRect(MX,MY,a)&&!S.anvil);
  if(S.anvil){ rarFrame(a,S.anvil,3); drawItem(S.anvil,a.x+a.w/2,a.y+a.h/2-4,4); txt(RAR[S.anvil.r].n,a.x+a.w/2,a.y+a.h-12,10,RAR[S.anvil.r].col,'center'); }
  else txt('drop here',a.x+a.w/2,a.y+a.h/2,10,C.dimmer,'center','normal');
  const ix=a.x+a.w+16, iw=wb.x+wb.w-14-ix;
  if(st==='empty') wrapText('Drag a finished object onto the anvil and pay extra materials to lift it a tier. Rich buyers pay for it; poor ones cannot.',ix,a.y+14,iw,16,10,C.dim);
  else if(st==='max') txt('LEGENDARY. Nothing finer.',ix,a.y+20,13,RAR[3].col);
  else {
    const nr=S.anvil.r+1, nb=upgradeBill(S.anvil), nv=rar(S.anvil,nr).v;
    txt('TO '+RAR[nr].n,ix,a.y+10,14,RAR[nr].col);
    txt('value '+S.anvil.v+' > '+nv,ix+iw,a.y+10,11,C.ink,'right');
    let yy=a.y+32;
    Object.keys(nb).forEach(k=>{ const have=S.mats[k]||0, okk=have>=nb[k];
      txt(nb[k]+' x '+MATBY[k].n,ix,yy,10,okk?C.ink:C.red,'left','normal');
      txt('have '+have,ix+iw,yy,10,okk?C.dim:C.red,'right','normal'); yy+=15; });
    if(st==='day') txt(RAR[nr].n+' WORK OPENS '+(CRAFT.demo?('DAY '+RAR[nr].day):('IN '+(RAR[nr].day-craftDay())+' DAYS')),wb.x+wb.w/2,a.y+a.h+26,11,C.dimmer,'center');
    else if(st==='lock') txt('UNLOCK '+(S.unl.fine?'RELIC CORE':'FINE PARTS')+' AT THE MARKET FIRST',wb.x+wb.w/2,a.y+a.h+26,11,C.gold,'center');
    else button(wb.x+14,a.y+a.h+10,wb.w-28,32,st==='ok'?('REFINE TO '+RAR[nr].n+'  ·  '+billCost(nb)+'c OF MATERIALS'):'NOT ENOUGH MATERIALS',()=>doUpgrade(),st==='ok'?RAR[nr].col:C.dimmer,11);
  }
  /* tray */
  txt('FINISHED GOODS',wb.x+14,wb.y+498,13,C.gold);
  txt(CRAFT.demo?'unshelved = back stock':'kept here until you shelve it',wb.x+wb.w-14,wb.y+498,9,C.dimmer,'right','normal');
  for(let i=0;i<17;i++){ const q=trayRect(i), it=S.tray[i];
    wsCell(q,S.wd&&!it&&inRect(MX,MY,q));
    if(it){ rarFrame(q,it); drawItem(it,q.x+q.w/2,q.y+q.h/2,2); } }
  { const q=binRect(), hot=S.wd&&inRect(MX,MY,q);
    plate(q.x,q.y,q.w,q.h,hot?'#3e2f22':'#211a14',hot?C.gold:'#4a3b2c');
    blit(BARREL_SPR,q.x+q.w/2-12,q.y+5,3); txt('SCRAP',q.x+q.w/2,q.y+q.h-9,9,hot?C.gold:C.dim,'center');
    if(hot){ const yt='BACK: '+billText(scrapYield(S.wd.item)), w3=txtw(yt,10,'normal')+16;
      plate(q.x+q.w-w3,q.y-26,w3,20,'#14100c',C.gold); txt(yt,q.x+q.w-w3/2,q.y-16,10,C.ink,'center','normal'); } }
  /* ---- shelves ---- */
  plate(sh.x,sh.y,sh.w,sh.h,'#1a1410','#6b5540','#8a6f50');
  txt('THE SHELVES',sh.x+14,sh.y+22,15,C.gold);
  txt('what is here at dawn is what you sell',sh.x+sh.w-14,sh.y+22,10,C.dimmer,'right','normal');
  S.shelves.forEach((s,i)=>{
    const r=wsShelfRect(i), cat=CATS[s.cat], good=S.wd&&S.wd.item.cat===s.cat, empty=!s.slots.some(e=>e);
    g.fillStyle=S.wd?(good?'rgba(127,183,79,0.16)':'rgba(200,80,58,0.10)'):'rgba(0,0,0,0.25)'; g.fillRect(r.x,r.y,r.w,22);
    blit(catBadge(s.cat),r.x+4,r.y+5,1.5); txt(cat.name,r.x+22,r.y+11,14,cat.col);
    if(empty) txt('click to relabel',r.x+r.w-6,r.y+11,10,C.dimmer,'right','normal');
    for(let j=0;j<4;j++){ const q=wsSlotRect(i,j), e=s.slots[j];
      wsCell(q,S.wd&&!e&&inRect(MX,MY,q));
      if(e){ rarFrame(q,e.item); drawItem(e.item,q.x+q.w/2,q.y+q.h/2-8,3);
        txt(fitText(e.item.n,q.w-8,9,'normal'),q.x+q.w/2,q.y+q.h-12,9,e.item.r?RAR[e.item.r].col:C.dim,'center','normal');
        if(e.misfiled){ g.fillStyle=C.red; g.fillRect(q.x+q.w-28,q.y+3,25,12); txt('MIS',q.x+q.w-15,q.y+9,10,'#1a1410','center'); } }
    }
  });
  const guide=[['1 · BUY MATERIALS','The market is on the left.'],['2 · CLICK A RECIPE','The workbench turns two materials into goods.'],
               ['3 · DRAG IT TO A SHELF','Or onto the anvil first, to refine it.'],['4 · STOCKED',CRAFT.demo?'Open the stall when you are ready.':'Head back when you are done.']][step-1];
  if(!WT.on){ txt(guide[0],sh.x+sh.w/2,sh.y+578,13,C.gold,'center'); txt(guide[1],sh.x+sh.w/2,sh.y+594,10,C.ink,'center','normal'); }
  txt('rent '+(CRAFT.demo?'tonight ':'tomorrow ')+rentFor(effDay())+'c  ·  spent on materials '+S.cr.daySpent+'c',sh.x+sh.w/2,sh.y+610,10,C.dim,'center','normal');
  const has=wsStocked()||S.tray.some(x=>x);
  button(sh.x+sh.w/2-150,sh.y+sh.h-56,300,46,CRAFT.demo?(has?'OPEN THE STALL':'OPEN WITH NOTHING TO SELL'):'BACK TO THE FIXER',
         ()=>{ if(S.wd){ wsPut(S.wd.from,S.wd.item); S.wd=null; } WT.on=false; WT.done=true;      /* one lesson, one starter kit */
               if(CRAFT.demo){ S.back=S.tray.filter(x=>x); S.tray.fill(null); S.backT=2.5; S.scene='play'; S.sceneT=0; say(pick(['Another day.','Let\'s trade.','Dust\'s up. Open.'])); }
               else { S.scene='shop'; S.sceneT=0; } },
         (has||!CRAFT.demo)?C.gold:C.dimmer,15);
  if(WT.on) drawWorkTut(); else
  wsGlow(step===1?mk:step===2?{x:wb.x+8,y:wb.y+36,w:wb.w-16,h:266}:step===3?sh:{x:sh.x+sh.w/2-150,y:sh.y+sh.h-56,w:300,h:46});
  drawEffects();
  if(S.wd){
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(Math.round(S.wd.x-20),Math.round(S.wd.y+24),40,5);
    drawItem(S.wd.item,S.wd.x,S.wd.y-4,3);
    const nm=(S.wd.item.crafted?'HAND-MADE ':'')+(S.wd.item.r?RAR[S.wd.item.r].n+' ':'')+S.wd.item.n+'  '+S.wd.item.v, w2=txtw(nm,10,'normal')+16;
    plate(S.wd.x-w2/2,S.wd.y+30,w2,20,'#14100c',S.wd.item.r?RAR[S.wd.item.r].col:'#4a3b2c');
    txt(nm,S.wd.x,S.wd.y+40,10,C.ink,'center','normal');
  }
}
/* ---------------- workbench walkthrough: first visit only ---------------- */
const WT={on:false,done:false,step:0,t:0,c0:0};
function enterWorkshop(){
  S.scene='workshop'; S.sceneT=0;
  if(!WT.done){
    WT.on=true; WT.step=0; WT.t=0; S.wsTab='guns';
    S.mats.scrap+=6; S.mats.timber+=4; S.mats.cloth+=2;           /* starter kit, so the lesson never stalls on an empty purse */
  }
}
function workTutWaiting(){ return WT.on&&(WT.step===0||WT.step===5)&&WT.t>0.4; }
function workTutClick(){
  if(!workTutWaiting()) return false;
  if(WT.step===0){ WT.step=1; WT.t=0; WT.c0=S.cr.crafted; S.wsTab='guns'; } else { WT.on=false; WT.done=true; }
  Snd.ui(); return true;
}
function workTutTick(dt){
  if(!WT.on) return; WT.t+=dt;
  const onShelf=S.shelves.some(sh=>sh.slots.some(e=>e&&e.item.r>0));
  if(WT.step===1&&S.cr.crafted>WT.c0){ WT.step=2; WT.t=0; }
  else if(WT.step===2&&S.anvil){ WT.step=3; WT.t=0; }
  else if(WT.step===3&&S.anvil&&S.anvil.r>0){ WT.step=4; WT.t=0; }
  else if(WT.step===4&&!S.anvil&&!S.wd&&WT.t>0.2){ WT.step=5; WT.t=0; }
  else if((WT.step===2||WT.step===3)&&!S.anvil&&!S.wd&&!S.tray.some(x=>x)&&WT.t>0.5){ WT.step=1; WT.c0=S.cr.crafted; WT.t=0; }   /* scrapped or shelved it early: make another */
}
function drawWorkTut(){
  const sh=WS.sh, wb=WS.wb, a=anvilRect();
  const T=[['THE WORKBENCH','Make your own stock instead of waiting on the road. There is a starter kit of scrap, timber and cloth on the house.'],
           ['1 · CLICK THE ZIP GUN RECIPE','Scrap + Timber. The finished gun drops into the tray below.'],
           ['2 · DRAG IT ONTO THE ANVIL','Pick the Zip Gun up from FINISHED GOODS and drop it on the anvil.'],
           ['3 · PRESS REFINE','Extra materials lift it from COMMON to RARE - worth more than double. No luck involved.'],
           ['4 · PUT IT ON A SHELF','Drag it to the ARMS shelf. Stock on a shelf is waiting for you when the stall opens.'],
           ['THAT IS THE CRAFT','Buy more on the left. Drop anything on SCRAP - or CONTROL-click it - to get half its materials back. The pips by a buyer\'s name show the richest tier they pay for - sell above it and they pay their cap.']][WT.step];
  const cr={x:sh.x+16,y:sh.y+322,w:sh.w-32,h:180};
  plate(cr.x,cr.y,cr.w,cr.h,'#241a0e',C.gold);
  txt(T[0],cr.x+16,cr.y+24,15,C.gold);
  wrapText(T[1],cr.x+16,cr.y+54,cr.w-32,18,11,C.ink);
  if(workTutWaiting()&&Math.sin(S.t*6)>-0.3) txt('click anywhere to carry on',cr.x+16,cr.y+cr.h-18,11,C.gold,'left','normal');
  button(cr.x+cr.w-84,cr.y+cr.h-34,72,24,'SKIP',()=>{WT.on=false;WT.done=true;},C.dim,10);
  const gl=[null,{x:wb.x+12,y:wb.y+80,w:wb.w-24,h:68},a,{x:wb.x+14,y:a.y+a.h+10,w:wb.w-28,h:32},wsShelfRect(Math.max(0,S.shelves.findIndex(s=>s.cat==='guns'))),null][WT.step];
  if(gl) wsGlow(gl);
}
function drawSummary(){
  dim(0.84);
  const w=760,h=560,x=W/2-w/2,y=104, c=S.cr;
  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');
  txt('CRAFTING TEST  ·  '+S.history.length+' DAYS',W/2,y+44,26,C.gold,'center');
  let te=0,tr=0; S.history.forEach(d=>{te+=d.earned;tr+=d.rent;});
  const rows=[['takings',te+'c'],['rent paid',tr+'c'],['spent on materials',c.spent+'c'],['net of rent and materials',(te-tr-c.spent)+'c'],
    ['purse now',S.caps+'c'],['objects crafted',c.crafted+''],
    ['refined to rare / epic / legendary',c.up[1]+' / '+c.up[2]+' / '+c.up[3]],
    ['sold common / rare / epic / legendary',c.soldR.join(' / ')],
    ['sales paid below their tier (purse too small)',c.capped+''],
    ['time in the workshop',Math.round(c.wsTime)+'s  ('+Math.round(c.wsTime/Math.max(1,S.history.length))+'s a morning)']];
  let yy=y+96; rows.forEach(r=>{ txt(r[0],x+50,yy,12,C.dim,'left','normal'); txt(r[1],x+w-50,yy,14,C.ink,'right'); yy+=32; });
  txt('day by day:  '+S.history.map(d=>'D'+d.day+' '+d.earned+'c').join('   '),W/2,yy+14,10,C.dim,'center','normal');
  button(W/2-150,y+h-70,300,50,'RUN IT AGAIN',()=>startRun(),C.gold,16);
}
