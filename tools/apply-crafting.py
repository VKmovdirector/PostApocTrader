import sys
SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
D="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/"
SHARED14=[['  const it=entry.item, v=(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m;', '  const it=entry.item, v=(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m*(it.crafted?CRAFT.mult:1);'], ['    let v=0; d.bundle.forEach(b=> v+=Math.max(1,Math.round(b.item.v*0.25)));', '    let v=0; d.bundle.forEach(b=> v+=scrapValue(b.item));'], ['    const v=Math.max(1,Math.round(d.item.v*0.25));', '    const v=scrapValue(d.item);'], ['    const v=Math.max(1,Math.round(B.drag.item.v*0.25));', '    const v=scrapValue(B.drag.item);'], ['    else { S.caps+=Math.max(1,Math.round(B.drag.item.v*0.25)); B.scrapped++; }', '    else { S.caps+=scrapValue(B.drag.item); B.scrapped++; }'], ["((d.item.r?RAR[d.item.r].n+' ':'')+d.item.n+' ('+d.item.v+'c)');", "((d.item.crafted?'HAND-MADE ':'')+(d.item.r?RAR[d.item.r].n+' ':'')+d.item.n+' ('+d.item.v+'c)');"]]
mode=sys.argv[1]            # demo | main
demo = mode=='demo'
s=open(D+"v11b-before-workbench.html").read()
def rep(a,b,cnt=1):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b,cnt)
mod=open(SP+"/craft2.js").read().replace("%%CFG%%","{demo:true, mult:8}" if demo else "{demo:false, price:1000, mult:8}")
rep("/* ================================================================\n   WALKTHROUGHS","%%CRAFT%%/* ================================================================\n   WALKTHROUGHS")
s=s.replace("%%CRAFT%%",mod+"\n")
# ---- shared: price, bookkeeping, scenes, input, rarity on the trading screen
rep("  return Math.max(1, Math.round(0.5*patter*entry.item.v*src*wantM","  const it=entry.item, v=(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m;\n  return Math.max(1, Math.round(0.5*patter*v*src*wantM")
rep("    S.shelves.push({cat: old[i]? old[i].cat : cats[i%cats.length], slots:[null,null,null,null]});","    S.shelves.push({cat: old[i]? old[i].cat : cats[i%cats.length], slots: (S.wb&&old[i])? old[i].slots : [null,null,null,null]});   /* with a workbench, stock keeps overnight */")
rep("  addCombo(); TUT.hag=drag.haggle||0;\n  c.state='served'","  addCombo(); TUT.hag=drag.haggle||0;\n  S.cr.soldR[drag.item.r||0]++;\n  if((drag.item.r||0)>purseR(c)){ S.cr.capped++; const rr=custRect(c.row); float(rr.x+170,rr.y+104,'PURSE TOO SMALL - PAID AS '+RAR[purseR(c)].n,C.red,12); }\n  c.state='served'")
rep("  if(S.scene!=='play'||S.paused) return;\n\n  if(tutFrozen())","  if(S.scene==='workshop'){ S.cr.wsTime+=dt; workTutTick(dt); }\n  if(S.scene!=='play'||S.paused) return;\n\n  if(tutFrozen())")
rep("spilled:S.spilled,combo:S.dayCombo,before:S.caps,after:S.caps-rent-wage};","spilled:S.spilled,combo:S.dayCombo,before:S.caps,after:S.caps-rent-wage,mats:S.cr.daySpent};\n  S.cr.daySpent=0;")
rep("  rows.push(['Rent','-'+rp.rent+'c']);","  if(rp.mats>0) rows.push(['Materials (already paid)',rp.mats+'c']);\n  rows.push(['Rent','-'+rp.rent+'c']);")
rep("  else if(S.scene==='gameover') drawGameOver();","  else if(S.scene==='workshop') drawWorkshop();\n  else if(S.scene==='summary') drawSummary();\n  else if(S.scene==='gameover') drawGameOver();")
rep("S.scene==='paper'?'THE PAPER':","S.scene==='paper'?'THE PAPER':S.scene==='workshop'?'THE WORKBENCH':S.scene==='summary'?'RESULTS':")
rep("    tryPick(p.x,p.y,ev.shiftKey);\n  }\n});","    tryPick(p.x,p.y,ev.shiftKey);\n  }\n  if(S.scene==='workshop'){ if(workTutClick()) return; if(ev.ctrlKey||ev.button===2){ wsScrapAt(p.x,p.y); return; } wsPick(p.x,p.y); }\n});")
rep("  const p=toDesign(ev); MX=p.x; MY=p.y;\n  if(S.drag){","  const p=toDesign(ev); MX=p.x; MY=p.y;\n  if(S.wd){ S.wd.x=p.x; S.wd.y=p.y; }\n  if(S.drag){")
rep("window.addEventListener('pointerup',ev=>{ const p=toDesign(ev); if(S.drag) resolveDrop(p.x,p.y); });","window.addEventListener('pointerup',ev=>{ const p=toDesign(ev); if(S.wd) wsDrop(p.x,p.y); if(S.drag) resolveDrop(p.x,p.y); });")
rep("        const sc=itemScale(q.w,q.h), showName=q.h>=64;","        const sc=itemScale(q.w,q.h), showName=q.h>=64;\n        rarFrame({x:q.x,y:q.y,w:q.w,h:q.h-4},e.item);")
rep("      const showName=q.w>=84;","      rarFrame(q,e.item);\n      const showName=q.w>=84;")
rep("  const nm = d.bundle ? (d.bundle.length+' x '+CATS[d.item.cat].name) : (d.item.n+' ('+d.item.v+'c)');","  const nm = d.bundle ? (d.bundle.length+' x '+CATS[d.item.cat].name) : ((d.item.r?RAR[d.item.r].n+' ':'')+d.item.n+' ('+d.item.v+'c)');")
rep("      txt(price+'c',x+r.w-60,y+(big?26:22),big?22:17,C.gold,'center');","      txt(price+'c',x+r.w-60,y+(big?26:22),big?22:17,C.gold,'center');\n      if((S.drag.item.r||0)>purseR(c)) txt('PAYS AS '+RAR[purseR(c)].n,x+r.w-60,y+(big?56:44),9,C.red,'center');")
rep("    if(isBulk){\n      const bw3=","    if(S.wb){ const pr=purseR(c), nx=x+(big?84:62)+txtw(c.type.n,big?16:13)+10;      /* purse pips: the richest tier they pay for */\n      for(let p=1;p<=3;p++){ g.fillStyle=p<=pr?RAR[p].col:'#3a3228'; g.fillRect(nx+(p-1)*9,y+(big?12:10),6,6); } }\n    if(isBulk){\n      const bw3=")
for _a,_b in SHARED14:
    rep(_a,_b)
if demo:
    rep("<title>Rust &amp; Rations</title>","<title>Rust &amp; Rations - crafting test</title>")
    s=s.replace("rustrations.best","rustrations.craft.best")
    rep("function spawnCrate(){","function spawnCrate(){\n  if(!DEMO.caravans) return;")
    rep("    want = Math.random()<0.35 ? {kind:'item',item:pick(BYCAT[cat]),cat:cat} : {kind:'cat',cat:cat};","    const oi=DEMO.caravans?BYCAT[cat]:openItems(cat);\n    want = (oi.length&&Math.random()<0.35) ? {kind:'item',item:pick(oi),cat:cat} : {kind:'cat',cat:cat};")
    rep("item:(Math.random()<0.3?pick(BYCAT[cat]):null),n:n};","item:((Math.random()<0.3&&(DEMO.caravans||openItems(cat).length))?pick(DEMO.caravans?BYCAT[cat]:openItems(cat)):null),n:n};")
    rep("  S.day=1; S.caps=40;","  S.day=1; S.caps=500;")
    rep("  const cats=activeCats().filter(c=>t.wants.indexOf(c)>=0);","  const cats=activeCats().filter(c=>t.wants.indexOf(c)>=0&&(DEMO.caravans||c!=='junk'));")
    rep("cv.addEventListener('pointerdown',ev=>{","cv.addEventListener('contextmenu',ev=>ev.preventDefault());\ncv.addEventListener('pointerdown',ev=>{")
    rep("  TUT.done={};\n  UPGRADES","  TUT.done={basics:1,bulk:1};      /* the stall lessons assume caravans; the workbench has its own */\n  craftReset();\n  UPGRADES")
    rep("S.scene='dayintro'; S.sceneT=0; S.tut=S.day===1?1:0;","S.scene='dayintro'; S.sceneT=0; S.tut=(S.day===1&&DEMO.caravans)?1:0;")
    rep("  if(tutFrozen()){ TUT.t+=dt; lessonStep(); }","  if(S.back.length&&!S.closing){ S.backT-=dt; const fs=freeCounterSlot();\n    if(S.backT<=0&&fs>=0){ S.counter[fs]={item:S.back.shift(),arriving:0,anim:1,misfiled:false}; S.backT=1.6; Snd.drop(); } }\n  if(tutFrozen()){ TUT.t+=dt; lessonStep(); }")
    rep("function startDay(){\n  S.counter=new Array(8).fill(null);","function startDay(){\n  if(S.tray){ const left=(S.counter||[]).filter(e=>e).map(e=>e.item).concat(S.back||[]); S.back=[];\n    left.forEach(it=>{ const k=S.tray.indexOf(null); if(k>=0) S.tray[k]=it; }); }\n  S.counter=new Array(8).fill(null);")
    rep("         ()=>{S.scene='play';S.sceneT=0;say(pick(['Another day.','Let\\'s trade.','Dust\\'s up. Open.']));},C.gold,17);","         ()=>enterWorkshop(),C.gold,17);")
    rep("'RAISE THE SHUTTER',","'TO THE WORKBENCH',")
    rep("  txt('caravan every '+Math.round(crateEvery(S.day))+'s  ·  customer every '+custEvery(S.day).toFixed(1)+'s',","  txt((DEMO.caravans?'caravan every '+Math.round(crateEvery(S.day))+'s':'no caravans - you sell what you make')+'  ·  customer every '+custEvery(S.day).toFixed(1)+'s',")
    rep("  if(S.day===2) txt('NEW: junk crates start arriving.',W/2,y+146,14,CATS.junk.col,'center');","  const newRec=ITEMS.filter(it=>RECIPES[it.id][2]===S.day).map(it=>it.n), newTier=RAR.find(r=>r.day===S.day&&r.m>2.2);\n  txt('NEW RECIPES: '+(newRec.join(', ')||'none')+(newTier?'   ·   '+newTier.n+' WORK OPENS':''),W/2,y+262,12,'#8fd0ee','center');\n  if(S.day===2) txt('NEW: junk buyers come to town.',W/2,y+146,14,CATS.junk.col,'center');")
    rep("  else button(W/2-150,y+h-70,300,50,'CLOSE FOR THE DAY',()=>{S.scene='paper';S.sceneT=0;},C.gold,15);","  else button(W/2-150,y+h-70,300,50,S.day>=DEMO.days?'SEE THE RESULTS':'CLOSE FOR THE DAY',()=>{ if(S.day>=DEMO.days){S.scene='summary';S.sceneT=0;} else nextDay(); },C.gold,15);")
    rep("  txt('NEXT CARAVAN',hr.x+12,hr.y+15,11,C.dim);","  txt(DEMO.caravans?'NEXT CARAVAN':('BACK STOCK  '+S.back.length+' LEFT'),hr.x+12,hr.y+15,11,(!DEMO.caravans&&S.back.length)?C.gold:C.dim);")
    rep("  txt(S.closing?'closed':'in '+Math.ceil(tleft)+'s',hr.x+hr.w-12,hr.y+15,11,C.dimmer,'right','normal');\n  bar(hr.x+12,hr.y+25,hr.w-24,11,S.closing?0:1-tleft/ce,C.gold);","  if(DEMO.caravans){\n  txt(S.closing?'closed':'in '+Math.ceil(tleft)+'s',hr.x+hr.w-12,hr.y+15,11,C.dimmer,'right','normal');\n  bar(hr.x+12,hr.y+25,hr.w-24,11,S.closing?0:1-tleft/ce,C.gold);\n  } else bar(hr.x+12,hr.y+25,hr.w-24,11,Math.min(1,S.back.length/17),C.gold);")
    rep("  txt('UNSORTED - THE COUNTER',cb.x+6,cb.y+11,15,C.dim);","  txt(DEMO.caravans?'UNSORTED - THE COUNTER':'FROM THE BACK ROOM - FILE IT',cb.x+6,cb.y+11,15,C.dim);")
    i=s.index("  const rows=[\n    ['THE CARAVAN DUMPS LOOT"); j=s.index("  let yy=y+142;")
    s=s[:i]+"""  const rows=[
    ['EVERY MORNING STARTS AT THE WORKBENCH','Buy materials, click a recipe, and the goods land in your tray.'],
    ['REFINE IT ON THE ANVIL','Extra materials lift it: common, rare, epic, legendary. No luck involved.'],
    ['STOCK THE SHELVES, THEN OPEN','Unshelved goods follow as back stock. Unsold stock waits for tomorrow.'],
    ['MIND THE BUYER\\'S PURSE','The pips by a name show the richest tier they pay for. Above it, they pay their cap.'],
    ['RENT IS STILL DUE EVERY NIGHT','Seven days. Materials come out of the same purse.']
  ];
"""+s[j:]
    rep("  txt('a trading post at the edge of the dust',W/2,y+92,14,C.dim,'center','normal');","  txt('CRAFTING TEST  ·  a separate rig',W/2,y+92,13,'#8fd0ee','center','normal');")
    rep("  button(W/2-160,y+h-86,320,54,'OPEN THE STALL',()=>startRun(),C.gold,20);","  button(W/2-160,y+h-132,320,34,'CARAVANS: '+(DEMO.caravans?'ON  (free loot as well)':'OFF  (crafted stock only)'),()=>{DEMO.caravans=!DEMO.caravans;},DEMO.caravans?C.green:C.dim,11);\n  button(W/2-160,y+h-86,320,54,'START THE TEST',()=>startRun(),C.gold,20);")
    out="crafting-demo.html"
else:
    rep("RUST & RATIONS  -  build 2 (pixel art)","RUST & RATIONS  -  build 12 (pixel art, workbench)")
    rep("  TUT.done={};\n  UPGRADES","  TUT.done={};\n  craftReset();\n  UPGRADES")
    rep("""  button(x+30,y+h-58,268,44,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,13);
  button(x+310,y+h-58,222,44,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,13);
  button(x+544,y+h-58,366,44,'OPEN TOMORROW · DAY '+(S.day+1),()=>nextDay(),C.gold,14);""","""  button(x+30,y+h-58,196,44,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,11);
  button(x+236,y+h-58,150,44,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,11);
  const canWb=S.wb||S.caps>=CRAFT.price;
  button(x+396,y+h-58,250,44,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>{
      if(S.wb){ enterWorkshop(); return; }
      if(S.caps<CRAFT.price){ Snd.bad(); return; }
      S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day+1; Snd.coin(6); flash('#8fd0ee',0.25); enterWorkshop();
    },canWb?'#8fd0ee':C.dimmer,11);
  if(!S.wb&&inRect(MX,MY,{x:x+396,y:y+h-58,w:250,h:44})){
    plate(x+336,y+h-150,370,84,'#14100c','#8fd0ee');
    txt('THE WORKBENCH',x+350,y+h-132,12,'#8fd0ee');
    wrapText('Buy materials, craft your own goods and refine them up to LEGENDARY. Shelf stock keeps overnight once you own it.',x+350,y+h-112,342,14,10,C.ink);
  }
  button(x+656,y+h-58,254,44,'TOMORROW · DAY '+(S.day+1),()=>nextDay(),C.gold,13);""")
    out="index.html"
open(D+out,'w').write(s); print(out,'ok',len(s))
