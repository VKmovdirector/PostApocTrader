#!/usr/bin/env python3
"""Build 24: Transport locked to day 15, bulk lesson gives exactly what it asks, caravans back-to-back carry 3,
no purse line on the town page, refining follows the recipe calendar, every craft yields one, the counter shows
in the workshop."""
import re, sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("build 23: name screen, last-call END DAY, paper pictures, edge-to-edge","build 24: workshop counter, one-per-craft, Transport from day 15")
rep("  txt('build 23',W-20,H-18,10,C.dimmer,'right','normal');","  txt('build 24',W-20,H-18,10,C.dimmer,'right','normal');")

# 1. TRANSPORT opens on day 15
rep("const RIG=[","const RIG_DAY=15;                                     /* the yard opens on day 15 */\nconst RIG=[")
rep("  door(lx,by+(bh+gp)*2,bw,bh,'TRANSPORT '+rigCount()+'/'+RIG.length,()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',13,'rig');",
    "  if(S.day>=RIG_DAY){ door(lx,by+(bh+gp)*2,bw,bh,'TRANSPORT',()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',13,'rig'); if(S.day===RIG_DAY) newTab(lx,by+(bh+gp)*2,bw,bh); }\n"
    "  else { const ty=by+(bh+gp)*2; plate(lx,ty,bw,bh,'#15110d','#33291f'); blit(hubIcon('rig',C.dimmer),lx+12,ty+bh/2-8,2);\n"
    "    txt('TRANSPORT',lx+bw/2,ty+bh/2-6,13,C.dimmer,'center'); txt('opens on day '+RIG_DAY,lx+bw/2,ty+bh/2+13,9,C.dimmer,'center','normal'); }")
rep("    if(S.day===2) notes.push(['NEW AT THE FIXER: perks and active skills are for sale',C.gold,'#231c10']);",
    "    if(S.day===2) notes.push(['NEW AT THE FIXER: perks and active skills are for sale',C.gold,'#231c10']);\n"
    "    if(S.day===RIG_DAY) notes.push(['NEW: TRANSPORT is open - the Strider parts are for sale','#c8a070','#221a12']);")

# 2. the bulk lesson stocks exactly three and keeps nothing back afterwards
rep("""    S.shelves[row].slots=[0,1,2,3].map((z,j)=>{
      const it=pick(BYCAT[cat]);
      TUT.gave.push({i:row,j:j,item:it});
      return {item:it,misfiled:false,arriving:0,anim:0};
    });""",
"""    /* three meds on the shelf, counting any the player already has: the order is for three, so nothing is left over */
    const sl=S.shelves[row].slots; let have=sl.filter(e=>e&&e.item.cat===cat).length;
    for(let j=0;j<4&&have<3;j++){ if(sl[j]&&sl[j].item.cat===cat) continue;
      const it=pick(BYCAT[cat]); sl[j]={item:it,misfiled:false,arriving:0,anim:0}; TUT.gave.push({i:row,j:j,item:it}); have++; }""")
rep("""  /* take back whatever the lesson put out and the player did not use */
  TUT.gave.forEach(g=>{""",
"""  /* the day-1 props (worthless cans, a sample) are cleared away; the day-3 meds are real stock and stay */
  if(id==='basics') TUT.gave.forEach(g=>{""")

# 3. caravans on each other's heels carry three at most; the big one waits its turn
rep("function spawnCrate(big){\n  const lo=crateLo(S.day), hi=crateSize(S.day), n=big ? ri(lo,hi)*2 : ri(lo,hi), items=[];",
    "const CRATE_GAP=15;                                   /* seconds: a caravan this soon after the last one is a light one */\n"
    "function sinceCrate(){ return S.dayTime-(S.lastCrateT===undefined?-99:S.lastCrateT); }\n"
    "function spawnCrate(big){\n  const lo=crateLo(S.day), hi=crateSize(S.day); let n=big ? ri(lo,hi)*2 : ri(lo,hi); const items=[];\n"
    "  if(!big&&sinceCrate()<CRATE_GAP) n=Math.min(n,3);\n  S.lastCrateT=S.dayTime;")
rep("    if(S.bigDue){ S.bigDue=false; spawnCrate(true); }\n    else if(S.crateDue>0){ S.crateDue--; spawnCrate(false); }",
    "    if(S.bigDue){ if(sinceCrate()>=CRATE_GAP){ S.bigDue=false; spawnCrate(true); } }   /* the big load never lands on the heels of another */\n"
    "    else if(S.crateDue>0){ S.crateDue--; spawnCrate(false); }")
rep("  S.crateDue=0; S.bigDue=false; S.keyFx=[];","  S.crateDue=0; S.bigDue=false; S.lastCrateT=-99; S.keyFx=[];")

# 4. no purse / rent line on the town page (the HUD has them)
rep("  txt('purse '+S.caps+'c   ·   rent tonight '+rentFor(S.day)+'c',x+w-30,y+36,14,C.ink,'right');\n","")

# 5. refining follows the recipe calendar
rep("  if(r>3) return 'max';\n  if(craftDay()<RAR[r].day) return 'day';",
    "  if(r>3) return 'max';\n  if(!recipeOpen(item.base||item)) return 'recipe';         /* what you cannot make yet you cannot refine yet */\n  if(craftDay()<RAR[r].day) return 'day';")
rep("  else if(st==='max') txt('LEGENDARY. Nothing finer.',ix,a.y+20,13,RAR[3].col);\n  else {",
    "  else if(st==='max') txt('LEGENDARY. Nothing finer.',ix,a.y+20,13,RAR[3].col);\n"
    "  else if(st==='recipe'){ const dd=RECIPES[(S.anvil.base||S.anvil).id][2]-craftDay();\n"
    "    txt('NOT YET',ix,a.y+10,14,C.dimmer); wrapText('You cannot refine what you cannot make. This recipe opens in '+dd+' day'+(dd>1?'s':'')+'.',ix,a.y+32,iw,16,10,C.dim); }\n"
    "  else {")

# 6. every craft yields one
s0=src.index("const RECIPES={"); s1=src.index("};",s0)
block=src[s0:s1]; block2=re.sub(r",(\d)\]",",1]",block); assert block2!=block
src=src[:s0]+block2+src[s1:]; n+=1
rep("/* item id -> [material A, material B, workbench-day the recipe opens, how many one craft yields]\n   Goods sell at about half their value, so the cheap ones come out in pairs or they would never pay. */",
    "/* item id -> [material A, material B, workbench-day the recipe opens, how many one craft yields (one, since build 24)] */")

# 7. the counter shows under the shelves in the workshop
rep("function wsShelfRect(i){ return {x:WS.sh.x+12,y:WS.sh.y+44+i*132,w:WS.sh.w-24,h:126}; }",
    "function wsShelfRect(i){ return {x:WS.sh.x+12,y:WS.sh.y+44+i*110,w:WS.sh.w-24,h:104}; }\n"
    "function wsCounterRect(){ return {x:WS.sh.x+12,y:WS.sh.y+44+4*110+2,w:WS.sh.w-24,h:88}; }\n"
    "function wsCounterSlot(j){ const r=wsCounterRect(), k=S.cslots, sw=Math.floor((r.w-(k-1)*6)/k); return {x:r.x+j*(sw+6),y:r.y+22,w:sw,h:r.h-22}; }")
rep("  if(S.anvil&&inRect(x,y,anvilRect())){ S.wd={item:S.anvil,from:{k:'anvil'},x:x,y:y}; S.anvil=null; Snd.ui(); return; }\n  for(let i=0;i<S.shelves.length;i++){",
    "  if(S.anvil&&inRect(x,y,anvilRect())){ S.wd={item:S.anvil,from:{k:'anvil'},x:x,y:y}; S.anvil=null; Snd.ui(); return; }\n"
    "  for(let j=0;j<S.cslots;j++){ const e=S.counter[j]; if(e&&inRect(x,y,wsCounterSlot(j))){ S.wd={item:e.item,from:{k:'counter',i:j},x:x,y:y}; S.counter[j]=null; Snd.ui(); return; } }\n"
    "  for(let i=0;i<S.shelves.length;i++){")
rep("  else if(to.k==='anvil') S.anvil=item;\n  else {",
    "  else if(to.k==='anvil') S.anvil=item;\n  else if(to.k==='counter') S.counter[to.i]={item:item,arriving:0,anim:0,misfiled:false};\n  else {")
rep("  for(let i=0;i<17&&!to;i++) if(!S.tray[i]&&inRect(x,y,trayRect(i))) to={k:'tray',i:i};\n  for(let i=0;i<S.shelves.length&&!to;i++)",
    "  for(let i=0;i<17&&!to;i++) if(!S.tray[i]&&inRect(x,y,trayRect(i))) to={k:'tray',i:i};\n"
    "  for(let j=0;j<S.cslots&&!to;j++) if(!S.counter[j]&&inRect(x,y,wsCounterSlot(j))) to={k:'counter',i:j};\n"
    "  for(let i=0;i<S.shelves.length&&!to;i++)")
rep("  if(S.anvil&&inRect(x,y,anvilRect())){ const it=S.anvil; S.anvil=null; scrapItem(it); return true; }\n  for(let i=0;i<S.shelves.length;i++) for(let j=0;j<4;j++){ const e=S.shelves[i].slots[j];",
    "  if(S.anvil&&inRect(x,y,anvilRect())){ const it=S.anvil; S.anvil=null; scrapItem(it); return true; }\n"
    "  for(let j=0;j<S.cslots;j++){ const e=S.counter[j]; if(e&&inRect(x,y,wsCounterSlot(j))){ S.counter[j]=null; scrapItem(e.item); return true; } }\n"
    "  for(let i=0;i<S.shelves.length;i++) for(let j=0;j<4;j++){ const e=S.shelves[i].slots[j];")
rep("""  const guide=[['1 · BUY MATERIALS','The market is on the left.'],""",
"""  { const cr=wsCounterRect();                                   /* the unsorted counter, as it will be at dawn */
    g.fillStyle='rgba(0,0,0,0.25)'; g.fillRect(cr.x,cr.y,cr.w,22);
    txt('UNSORTED - THE COUNTER',cr.x+6,cr.y+11,13,C.dim);
    const cnt=(S.counter||[]).filter(Boolean).length; txt(cnt+'/'+S.cslots,cr.x+cr.w-6,cr.y+11,12,cnt?C.ink:C.dimmer,'right');
    for(let j=0;j<S.cslots;j++){ const q=wsCounterSlot(j), e=S.counter[j];
      wsCell(q,S.wd&&!e&&inRect(MX,MY,q));
      if(e){ rarFrame(q,e.item); drawItem(e.item,q.x+q.w/2,q.y+q.h/2-6,2); txt(fitText(e.item.n,q.w-6,8,'normal'),q.x+q.w/2,q.y+q.h-9,8,C.dim,'center','normal'); } } }
  const guide=[['1 · BUY MATERIALS','The market is on the left.'],""")
rep("  if(!WT.on){ txt(guide[0],sh.x+sh.w/2,sh.y+578,13,C.gold,'center'); txt(guide[1],sh.x+sh.w/2,sh.y+594,10,C.ink,'center','normal'); }\n"
    "  txt('rent '+(CRAFT.demo?'tonight ':'tomorrow ')+rentFor(effDay())+'c  ·  spent on materials '+S.cr.daySpent+'c',sh.x+sh.w/2,sh.y+610,10,C.dim,'center','normal');",
    "  if(!WT.on){ txt(guide[0],sh.x+sh.w/2,sh.y+584,13,C.gold,'center'); txt(guide[1],sh.x+sh.w/2,sh.y+598,10,C.ink,'center','normal'); }\n"
    "  txt('rent tonight '+rentFor(effDay())+'c  ·  spent on materials '+S.cr.daySpent+'c',sh.x+sh.w/2,sh.y+612,10,C.dim,'center','normal');")
open(P,'w').write(src); print('applied',n)
