import sys
SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
D="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/"
def patch(path, reps):
    s=open(path).read()
    for a,b in reps:
        assert a in s, (path[-24:], a[:60])
        s=s.replace(a,b,1)
    open(path,'w').write(s)

# ---------- crafting module changes: applied to the module source and to both built files
MOD=[
 ("n:'Scrap',     c:2","n:'Scrap',     c:16"),("n:'Timber',    c:4","n:'Timber',    c:32"),("n:'Cloth',     c:2","n:'Cloth',     c:16"),
 ("n:'Herbs',     c:4","n:'Herbs',     c:32"),("n:'Grain',     c:2","n:'Grain',     c:16"),("n:'Glass',     c:4","n:'Glass',     c:32"),
 ("n:'Chem',      c:6","n:'Chem',      c:48"),("n:'Wire',      c:8","n:'Wire',      c:64"),
 ("n:'Fine Parts',c:18, day:3","n:'Fine Parts',c:1000, day:5"),("n:'Relic Core',c:48,day:5","n:'Relic Core',c:2000,day:10"),
 ("{n:'EPIC',     m:5,   col:'#a173c8', day:3}","{n:'EPIC',     m:5,   col:'#a173c8', day:5}"),
 ("{n:'LEGENDARY',m:12,  col:'#e8b13c', day:5}","{n:'LEGENDARY',m:12,  col:'#e8b13c', day:10}"),
 ("  const cats=activeCats(), tw=Math.floor","  const cats=activeCats().filter(c=>c!=='junk'), tw=Math.floor"),      # no junk at the bench
 ("Drop anything on SCRAP to get half its materials back.","Drop anything on SCRAP - or CONTROL-click it - to get half its materials back."),
 ("function rarFrame(q,item,inset){","""function wsScrapAt(x,y){
  for(let i=0;i<17;i++) if(S.tray[i]&&inRect(x,y,trayRect(i))){ const it=S.tray[i]; S.tray[i]=null; scrapItem(it); return true; }
  if(S.anvil&&inRect(x,y,anvilRect())){ const it=S.anvil; S.anvil=null; scrapItem(it); return true; }
  for(let i=0;i<S.shelves.length;i++) for(let j=0;j<4;j++){ const e=S.shelves[i].slots[j];
    if(e&&inRect(x,y,wsSlotRect(i,j))){ S.shelves[i].slots[j]=null; scrapItem(e.item); return true; } }
  return false;
}
function rarFrame(q,item,inset){"""),
]
for p in [SP+"/craft2.js", D+"index.html"]:
    patch(p, MOD)
patch(SP+"/pc2.py",[
 ("if(S.scene==='workshop'){ if(workTutClick()) return; wsPick(p.x,p.y); }","if(S.scene==='workshop'){ if(workTutClick()) return; if(ev.ctrlKey||ev.button===2){ wsScrapAt(p.x,p.y); return; } wsPick(p.x,p.y); }"),
 ("    rep(\"  S.day=1; S.caps=40;\",\"  S.day=1; S.caps=80;\")","    rep(\"  S.day=1; S.caps=40;\",\"  S.day=1; S.caps=500;\")\n    rep(\"  const cats=activeCats().filter(c=>t.wants.indexOf(c)>=0);\",\"  const cats=activeCats().filter(c=>t.wants.indexOf(c)>=0&&(DEMO.caravans||c!=='junk'));\")\n    rep(\"cv.addEventListener('pointerdown',ev=>{\",\"cv.addEventListener('contextmenu',ev=>ev.preventDefault());\\ncv.addEventListener('pointerdown',ev=>{\")"),
])

# ---------- main game
MAIN=[
 # 1-3 prices
 ("cd:30, cost:240,","cd:30, cost:600,"),("cd:50, cost:320,","cd:50, cost:1000,"),("cd:60, cost:300,","cd:60, cost:1200,"),
 # 5 hired hand becomes the fifth active
 ("  why:'for when the shelves are bare'}\n];","  why:'for when the shelves are bare'},\n {key:5,id:'hire',  n:'HIRED HAND',     cd:40, cost:2000, col:'#8fd0ee',\n  d:'KIT works the stall beside you: files, sells and haggles for a few seconds',\n  why:'for when you need a second pair of hands'}\n];"),
 ("S.actOwn=[false,false,false,false];\nS.actCd=[0,0,0,0];","S.actOwn=[false,false,false,false,false];\nS.actCd=[0,0,0,0,0]; S.handT=0;"),
 ("  S.actOwn=[false,false,false,false]; S.actCd=[0,0,0,0]; S.steadyT=0; S.patterT=0;","  S.actOwn=[false,false,false,false,false]; S.actCd=[0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0; S.counter=[]; S.scrapN=0;"),
 ("  S.actCd=[0,0,0,0]; S.steadyT=0; S.patterT=0;\n  S.nextCrate","  S.actCd=[0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0;\n  S.nextCrate"),
 ("  for(let i=0;i<4;i++) if(S.actCd[i]>0) S.actCd[i]=Math.max(0,S.actCd[i]-dt);","  for(let i=0;i<5;i++) if(S.actCd[i]>0) S.actCd[i]=Math.max(0,S.actCd[i]-dt);"),
 ("ev.key>='1'&&ev.key<='4'){","ev.key>='1'&&ev.key<='5'){"),
 ("let TIP=null, RAILPOS=[null,null,null,null], RAILAY=252;","let TIP=null, RAILPOS=[null,null,null,null,null], RAILAY=252;"),
 ("  TIP=null; RAILPOS=[null,null,null,null];","  TIP=null; RAILPOS=[null,null,null,null,null];"),
 ("  txt('1-4',RAIL.x+RAIL.w-8,y-12,10,C.dimmer,'right');","  txt('1-5',RAIL.x+RAIL.w-8,y-12,10,C.dimmer,'right');"),
 ("function queueRows(){ return 3+(hand()?1:0); }","function queueRows(){ return 3; }"),
 ("function hand(){ return (S.hire.lvl>0&&S.hire.on!==false) ? HANDS[S.hire.lvl-1] : null; }","function hand(){ return (S.hire.lvl>0&&S.handT>0) ? HANDS[S.hire.lvl-1] : null; }      /* only while the active is running */"),
 ("  } else if(a.id==='patter'){\n    S.patterT=10;\n  } else {","  } else if(a.id==='patter'){\n    S.patterT=10;\n  } else if(a.id==='hire'){\n    const hh=hired(); S.handT=hh.dur; S.actCd[i]=a.cd+hh.dur;        /* the cooldown starts when she clocks off */\n    const hm=botHome(); BOT.x=hm.x; BOT.y=hm.y; botIdle(0.1);\n  } else {"),
 ("  S.patterT=Math.max(0,S.patterT-dt);\n","  S.patterT=Math.max(0,S.patterT-dt);\n  if(S.handT>0&&S.scene==='play'&&!S.paused){ S.handT-=dt; if(S.handT<=0){ S.handT=1e-6; botStrand(); S.handT=0; } }\n"),
 ("  const hd=hired();\n  if(S.day===HIRE_DAY&&!hd)","  const hd=null;                                   /* the hand is an active now: no wage, no morning toggle */\n  if(false)"),
 ("  ACTIVES.forEach((a,i)=>{\n    const cx=x+30+i*(cw+gap), cy=y+330;","  ACTIVES.forEach((a,i)=>{\n    if(a.id==='hire') return;                      /* sold from her own card above, it has levels */\n    const cx=x+30+i*(cw+gap), cy=y+330;"),
 ("    if(cd>0) txt(Math.ceil(cd)+'s',r.x+r.w-12,r.y+r.h-13,13,C.ink,'center');","    if(a.id==='hire'&&S.handT>0) txt(S.handT.toFixed(0)+'s',r.x+r.w-12,r.y+r.h-13,13,a.col,'center');\n    else if(cd>0) txt(Math.ceil(cd)+'s',r.x+r.w-12,r.y+r.h-13,13,C.ink,'center');"),
 ("      TIP={x:r.x+r.w+10,y:r.y,title:a.n,body:a.d,col:a.col,","      TIP={x:r.x+r.w+10,y:r.y,title:a.n+(a.id==='hire'?' · LVL '+S.hire.lvl:''),body:a.id==='hire'?('KIT works the stall beside you for '+hired().dur+' seconds: files, sells and haggles.'):a.d,col:a.col,"),
 # 8-9 caravans bring the odd refined piece
 ("function rollItem(){ return pick(BYCAT[pick(activeCats())]); }","function rollItem(){\n  const it=pick(BYCAT[pick(activeCats())]), x=Math.random();\n  if(S.day>15&&x<0.01) return rar(it,2);          /* 1% epic after day 15 */\n  if(S.day>10&&x<0.06) return rar(it,1);          /* 5% rare after day 10 */\n  return it;\n}"),
 ("    if(S.wb){ const pr=purseR(c),","    if(S.wb||S.day>10){ const pr=purseR(c),"),
 # 4 stock always survives the night; the dusk report asks what to do with it
 ("slots: (S.wb&&old[i])? old[i].slots : [null,null,null,null]});   /* with a workbench, stock keeps overnight */","slots: old[i]? old[i].slots : [null,null,null,null]});   /* stock keeps overnight unless scrapped at dusk */"),
 ("function startDay(){\n  S.counter=new Array(8).fill(null);","function startDay(){\n  { const keep=(S.counter||[]).filter(e=>e); keep.forEach(e=>{ e.arriving=0; e.anim=0; });\n    S.counter=keep.concat(new Array(8).fill(null)).slice(0,8); }\n  S.shelves.forEach(sh=>sh.slots.forEach(e=>{ if(e){ e.arriving=0; e.anim=0; } }));"),
 # 13 paper cadence
 ("  else button(W/2-150,y+h-70,300,50,'CLOSE FOR THE DAY',()=>{S.scene='paper';S.sceneT=0;},C.gold,15);","""  else {
    const lv=leftovers();
    if(lv.n){
      txt(lv.n+' GOODS LEFT ON THE STALL',W/2,y+h-96,11,C.dim,'center');
      button(W/2-250,y+h-76,244,52,'SCRAP THEM  +'+lv.v+'c',()=>{ scrapLeftovers(); afterReport(); },C.dim,12);
      button(W/2+6,y+h-76,244,52,'KEEP THEM',()=>afterReport(),C.gold,14);
    } else button(W/2-150,y+h-70,300,50,'CLOSE FOR THE DAY',()=>afterReport(),C.gold,15);
  }"""),
 ("  if(S.deadReason) button(W/2-120,y+h-70,240,50,'THAT IS THAT',()=>{S.scene='gameover';S.sceneT=0;},C.red,16);","""  if(S.deadReason&&S.caps+leftovers().v>=0){
    txt('THE UNSOLD STOCK WOULD COVER IT',W/2,y+h-96,11,C.gold,'center');
    button(W/2-190,y+h-76,380,52,'SCRAP IT ALL TO MAKE RENT  +'+leftovers().v+'c',()=>{ scrapLeftovers(); S.deadReason=null; },C.gold,12);
  }
  else if(S.deadReason) button(W/2-120,y+h-70,240,50,'THAT IS THAT',()=>{S.scene='gameover';S.sceneT=0;},C.red,16);"""),
 ("function drawReport(){","""function paperDay(d){ return d>=5&&(d-5)%4===0; }          /* the Herald prints on day 5, 9, 13 ... */
function afterPaper(){ S.scene=(S.day%5===0&&S.history.length)?'ledger':'shop'; S.sceneT=0; }
function afterReport(){ if(paperDay(S.day)){ S.scene='paper'; S.sceneT=0; } else afterPaper(); }
function scrapValue(item){ return Math.max(1,Math.round(item.v*0.25)); }
function leftovers(){
  let n=0,v=0;
  S.shelves.forEach(sh=>sh.slots.forEach(e=>{ if(e){ n++; v+=scrapValue(e.item); } }));
  (S.counter||[]).forEach(e=>{ if(e){ n++; v+=scrapValue(e.item); } });
  return {n:n,v:v};
}
function scrapLeftovers(){
  const lv=leftovers(); S.caps+=lv.v; if(S.endReport) S.endReport.after+=lv.v;
  S.shelves.forEach(sh=>sh.slots.fill(null)); S.counter.fill(null);
  Snd.coin(3); flash(C.gold,0.12);
}
/* CONTROL-click (or right-click) an item on the stall: straight into the scrap barrel */
function scrapAt(x,y){
  let item=null;
  const cj=counterSlotUnder(x,y);
  if(cj>=0&&S.counter[cj]&&!S.counter[cj].arriving){ item=S.counter[cj].item; S.counter[cj]=null; }
  if(!item){ const ss=shelfSlotUnder(x,y); const e=ss&&S.shelves[ss.i].slots[ss.j];
    if(e&&!e.arriving){ item=e.item; S.shelves[ss.i].slots[ss.j]=null; } }
  if(!item) return false;
  selClear();
  const v=scrapValue(item), tr=trashRect();
  S.caps+=v; S.scrapN=(S.scrapN||0)+1; breakCombo();
  flyer(item,x,y,tr.x+tr.w/2,tr.y+40,0.3,50,()=>{ burst(tr.x+tr.w/2,tr.y+40,'#6b5c48',10,120); });
  float(tr.x+tr.w/2,tr.y+10,'+'+v+'c SCRAP',C.dim,16); Snd.drop();
  return true;
}
function drawReport(){"""),
 ("  BTNS.push({x:bx,y:by,w:bw,h:bh,fn:()=>{\n    S.scene=(S.day%5===0&&S.history.length)?'ledger':'shop'; S.sceneT=0; }});","  BTNS.push({x:bx,y:by,w:bw,h:bh,fn:()=>afterPaper()});"),
 # 7 ctrl-click + lesson step
 ("cv.addEventListener('pointerdown',ev=>{","cv.addEventListener('contextmenu',ev=>ev.preventDefault());\ncv.addEventListener('pointerdown',ev=>{"),
 ("    if(lessonClick()) return;\n    tryPick(p.x,p.y,ev.shiftKey);","    if(lessonClick()) return;\n    if(ev.ctrlKey||ev.button===2){ scrapAt(p.x,p.y); return; }\n    tryPick(p.x,p.y,ev.shiftKey);"),
 ("if(S.scene==='workshop'){ if(workTutClick()) return; wsPick(p.x,p.y); }","if(S.scene==='workshop'){ if(workTutClick()) return; if(ev.ctrlKey||ev.button===2){ wsScrapAt(p.x,p.y); return; } wsPick(p.x,p.y); }"),
 ("    S.caps+=v; breakCombo();\n    const tr=trashRect();\n    float(tr.x+tr.w/2,tr.y+10,'+'+v+'c SCRAP',C.dim,16);","    S.caps+=v; breakCombo(); S.scrapN=(S.scrapN||0)+1;\n    const tr=trashRect();\n    float(tr.x+tr.w/2,tr.y+10,'+'+v+'c SCRAP',C.dim,16);"),
 ("  if(TUT.active==='basics') return TUT.step===0||TUT.step===4;","  if(TUT.active==='basics') return TUT.step===0||TUT.step===5;"),
 ("      if(S.sold>TUT.sold0){ TUT.step=4; TUT.t=0; }\n      else lessonEnsure({kind:'cat',cat:'meds'},'scavenger','Same again. Quick.',1);\n      return;\n    }\n    return;                                      /* step 4 waits for a click */","""      if(S.sold>TUT.sold0){ TUT.step=4; TUT.t=0; TUT.scr0=S.scrapN||0; }
      else lessonEnsure({kind:'cat',cat:'meds'},'scavenger','Same again. Quick.',1);
      return;
    }
    if(TUT.step===4){                            /* something worthless lands: get rid of it */
      if((S.scrapN||0)>TUT.scr0){ TUT.step=5; TUT.t=0; return; }
      if(!S.counter.some(e=>e&&e.lesson)&&!(S.drag&&S.drag.item.id==='cans')){
        S.shelves.forEach(sh=>sh.slots.forEach((e,j)=>{ if(e&&e.item.id==='cans') sh.slots[j]=null; }));
        const k=freeCounterSlot(); if(k>=0) S.counter[k]={item:ITEMBY.cans,arriving:0,anim:1,misfiled:false,lesson:true};
      }
      return;
    }
    return;                                      /* step 5 waits for a click */"""),
 ("  TUT.gave=[];\n  TUT.active=null; TUT.cust=null;","  TUT.gave=[];\n  S.counter.forEach((e,k)=>{ if(e&&e.lesson) S.counter[k]=null; });\n  TUT.active=null; TUT.cust=null;"),
 ("    else { head='THAT IS THE JOB';","    else if(step===4){ head='SCRAP WHAT YOU CANNOT SELL';\n      body='Tin cans, and no junk shelf today. Hold CONTROL and click them - or drag them to SCRAP IT. A jammed counter spills.'; }\n    else { head='THAT IS THE JOB';"),
 ("  const last = basics? step>=4 : step>=3;","  const last = basics? step>=5 : step>=3;"),
 ("    } else if(step===2||step===3){\n      S.shelves[TUT.row]","    } else if(step===4){\n      S.counter.forEach((e,k)=>{ if(e&&e.lesson){ const q=counterSlotRect(k); tutGlow({x:q.x,y:q.y,w:q.w,h:q.h}); } });\n      const tr=trashRect(); tutGlow({x:tr.x,y:tr.y,w:tr.w,h:tr.h});\n    } else if(step===2||step===3){\n      S.shelves[TUT.row]"),
]
patch(D+"index.html", MAIN)
print("patched")
