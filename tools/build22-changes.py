#!/usr/bin/env python3
"""Build 22: per-slot achievements+look, exact bulk counts, no pause button, END DAY under the queue,
three-town map, town page = next morning (sunrise city, door icons, NEW AT THE FIXER at the bottom),
bigger bottom-aligned perk rail, NES-style intro."""
import re, sys
P='index.html'
src=open(P).read()
n=0
def rep(a,b,count=1):
    global src,n
    if src.count(a)!=count:
        print('ANCHOR FAIL (%d found, want %d):\n%s'%(src.count(a),count,a[:200])); sys.exit(1)
    src=src.replace(a,b); n+=1

# ---------- header ----------
rep("RUST & RATIONS  -  build 19 (pixel art) - build 21: Herald events",
    "RUST & RATIONS  -  build 19 (pixel art) - build 22: morning town page, intro, per-slot progress")

# ---------- 1. achievements and the look live in the save slot ----------
rep("try{ const sv=JSON.parse(localStorage.getItem('rustrations.ach')||'null'); if(sv){ Object.assign(AST,sv.st||{}); ACH_GOT=sv.got||{}; } }catch(e){}\n"
    "function achSave(){ try{ localStorage.setItem('rustrations.ach',JSON.stringify({st:AST,got:ACH_GOT})); }catch(e){} }",
    "try{ localStorage.removeItem('rustrations.ach'); localStorage.removeItem('rustrations.look'); }catch(e){}   /* build 22: both live in the save slot now */\n"
    "function achSave(){ saveGame(); }\n"
    "function achReset(){ Object.keys(AST).forEach(k=>delete AST[k]); ACH_GOT={}; TOASTS=[]; }   /* a new game starts from nothing */")
rep("function saveLook(){ try{ localStorage.setItem('rustrations.look',JSON.stringify({look:S.worn,owned:S.owned})); }catch(e){} }\n"
    "(function(){ try{ const r=localStorage.getItem('rustrations.look');\n"
    "  if(r){ const d=JSON.parse(r);\n"
    "    if(d.look) Object.assign(S.look,d.look);\n"
    "    if(d.owned) Object.assign(S.owned,d.owned);\n"
    "    S.worn=Object.assign({},S.look); } }catch(e){} })();",
    "const LOOK_DEFAULT=Object.assign({},S.look);\n"
    "function saveLook(){ saveGame(); }                        /* the look belongs to the save slot */\n"
    "function lookReset(){ S.look=Object.assign({},LOOK_DEFAULT); S.worn=Object.assign({},S.look);\n"
    "  S.owned={}; LOOKCATS.forEach(k=>LOOKS[k].forEach(o=>{ if(o.cost===0) S.owned[k+':'+o.id]=1; })); S.editName=false; invalidateLook(); }")
rep("  const d={v:1,t:Date.now(),day:S.day,",
    "  const d={v:2,t:Date.now(),day:S.day,ach:{st:AST,got:ACH_GOT},look:{look:S.worn,owned:S.owned},")
rep("  Object.assign(S.up,d.up||{}); while(S.actOwn.length<ACTIVES.length) S.actOwn.push(false);",
    "  if(!(d.v>=2)&&d.day!==undefined) S.day=d.day+1;         /* build 21 saves stored the finished day; the town page is now the next morning */\n"
    "  achReset(); if(d.ach){ Object.assign(AST,d.ach.st||{}); ACH_GOT=d.ach.got||{}; }\n"
    "  lookReset(); if(d.look){ Object.assign(S.look,d.look.look||{}); Object.assign(S.owned,d.look.owned||{}); S.worn=Object.assign({},S.look); invalidateLook(); }\n"
    "  Object.assign(S.up,d.up||{}); while(S.actOwn.length<ACTIVES.length) S.actOwn.push(false);")
rep("function beginRun(){                                   /* OK on the how-to card: straight into day 1 and its lesson */\n"
    "  startRun();",
    "function beginRun(){                                   /* after the intro: straight into day 1 and its lesson */\n"
    "  achReset(); lookReset(); startRun();")
rep("  txt('build 19',W-20,H-18,10,C.dimmer,'right','normal');\n"
    "  txt('achievements '+achCount()+'/'+ACH.length+'  ·  best run: day '+S.best.day,20,H-18,10,C.dimmer,'left','normal');",
    "  txt('build 22',W-20,H-18,10,C.dimmer,'right','normal');\n"
    "  txt('best run: day '+S.best.day,20,H-18,10,C.dimmer,'left','normal');")
rep("      txt(perks+' perks'+(d.wb?'  ·  workbench':'')+'  ·  strider '+Object.values(d.rig||{}).filter(Boolean).length+'/4',x+cw/2,y+166,10,C.dim,'center','normal');\n"
    "      txt('saved '+new Date(d.t).toLocaleDateString()+'  '+new Date(d.t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}),x+cw/2,y+188,9,C.dimmer,'center','normal');",
    "      txt(perks+' perks'+(d.wb?'  ·  workbench':'')+'  ·  strider '+Object.values(d.rig||{}).filter(Boolean).length+'/4',x+cw/2,y+166,10,C.dim,'center','normal');\n"
    "      txt(Object.keys((d.ach&&d.ach.got)||{}).length+'/'+ACH.length+' achievements',x+cw/2,y+184,10,C.dim,'center','normal');\n"
    "      txt('saved '+new Date(d.t).toLocaleDateString()+'  '+new Date(d.t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}),x+cw/2,y+204,9,C.dimmer,'center','normal');")

# ---------- 2. a bulk order takes exactly what was asked ----------
rep("  if(!w||w.kind!=='bundle'||list.length<w.n) return false;",
    "  if(!w||w.kind!=='bundle'||list.length!==w.n) return false;      /* exactly the number asked: four is not three */")
rep("      const prog=bundleProgress(c), done=prog>=c.want.n;",
    "      const prog=bundleProgress(c), done=prog===c.want.n, over=prog>c.want.n;")
rep("        plate(wb.x+wb.w-pw-4,wb.y+4,pw,wb.h-8,done?'#2e3a1e':'#2a2012',done?C.green:'#c08a2a');\n"
    "        txt(prog+'/'+c.want.n,wb.x+wb.w-pw/2-4,wb.y+wb.h/2,big?16:13,done?C.green:C.gold,'center');",
    "        plate(wb.x+wb.w-pw-4,wb.y+4,pw,wb.h-8,done?'#2e3a1e':(over?'#3a1e1a':'#2a2012'),done?C.green:(over?C.red:'#c08a2a'));\n"
    "        txt(prog+'/'+c.want.n,wb.x+wb.w-pw/2-4,wb.y+wb.h/2,big?16:13,done?C.green:(over?C.red:C.gold),'center');")
rep("    if(c.want.kind==='bundle'){ c.line='I said '+c.want.n+' of them.';",
    "    if(c.want.kind==='bundle'){ c.line=d.bundle.length>c.want.n?('I said '+c.want.n+', not '+d.bundle.length+'.'):('I said '+c.want.n+' of them.');")
rep("  if(TUT.step===1){ if(bundleProgress(c)>=c.want.n){ TUT.step=2; TUT.t=0; } return; }",
    "  if(TUT.step===1){ if(bundleProgress(c)===c.want.n){ TUT.step=2; TUT.t=0; } return; }")

# ---------- 3+4. no pause button; END DAY appears under the queue for the last two buyers ----------
rep("  if(S.scene==='play'){\n"
    "    button(1100,8,76,42,S.paused?'RESUME':'PAUSE',()=>{S.paused=!S.paused;},C.dim,S.paused?10:13);\n"
    "    button(1182,8,90,42,'END DAY',()=>{ if(S.scene==='play') shutUpShop(); },C.red,12);\n"
    "  } else {",
    "  if(S.scene==='play'){                                   /* no pause button: esc opens the menu */\n"
    "    keycap(1186,13,50,32,'ESC',C.dim,'rest',false); txt('MENU',1258,29,10,C.dimmer,'center');\n"
    "  } else {")
rep("function shutUpShop(){\n  S.closing=true;",
    "/* the END DAY button only shows once the last two buyers of the day are on the road (or the day is closing) */\n"
    "function lastCall(){ return S.scene==='play'&&!S.shut&&!tutFrozen()&&(S.dayLen-S.dayTime)<=custEvery(S.day)*2; }\n"
    "function shutUpShop(){\n  S.closing=true; S.shut=true;")
rep("  S.combo=0; S.closing=false; S.overtime=0;\n  S.catEarn={};",
    "  S.combo=0; S.closing=false; S.overtime=0; S.shut=false;\n  S.catEarn={};")
rep("             hr.x+12,hr.y+52,hr.w-24,16,11,C.ink);\n    return;\n  }\n  const ce=crateEvery(S.day), tleft=Math.max(0,S.nextCrate);",
    "             hr.x+12,hr.y+52,hr.w-24,16,11,C.ink);\n    return;\n  }\n"
    "  if(lastCall()){                                          /* the day's last buyers: the END DAY button sits right under the queue */\n"
    "    const on=Math.sin(S.t*5)>0;\n"
    "    txt(S.closing?'CLOSING TIME':'LAST CALL',hr.x+12,hr.y+15,11,C.red);\n"
    "    txt(S.closing?'nobody else is coming':'the last buyers are on the road',hr.x+hr.w-12,hr.y+15,10,C.dim,'right','normal');\n"
    "    button(hr.x+12,hr.y+30,hr.w-24,54,'END DAY',()=>shutUpShop(),on?'#ff7a5c':C.red,20);\n"
    "    return;\n  }\n"
    "  const ce=crateEvery(S.day), tleft=Math.max(0,S.nextCrate);")

# ---------- 5. three towns ----------
rep("   THE MAP  -  five towns in the barrens. Only Dustwell is open yet;",
    "   THE MAP  -  three towns in the barrens. Only Dustwell is open yet;")
rep(""" {id:'cinder',  n:'CINDER GAP',  x:236,y:98,  road:'5 days east',
  d:'A mountain pass held by raiders who found that tolls pay better than raids. Short tempers.', wants:'arms, and quickly'},
 {id:'meridian',n:'OLD MERIDIAN',x:180,y:152, road:'4 days south-east',
  d:'The drowned city. Scavengers haul machines out of towers that lean a little further every year.', wants:'tech, and sells it cheap'},
 {id:'lastpump',n:'LAST PUMP',   x:286,y:40,  road:'9 days, the end of the road',
  d:'The only deep pump left working. Rich, thirsty, and a long way from anywhere.', wants:'the finest goods you can make'}
];
const ROUTES=[[0,1],[0,3],[1,2],[3,2],[2,4]];""",
""" {id:'cinder',  n:'CINDER GAP',  x:236,y:98,  road:'5 days east, past the salt',
  d:'A mountain pass held by raiders who found that tolls pay better than raids. Short tempers.', wants:'arms, and quickly'}
];
const ROUTES=[[0,1],[1,2]];""")
rep("""  /* the drowned city */
  for(let i=0;i<16;i++){ const bx=166+rnd2()*34, bh=5+rnd2()*12; px(bx,160-bh,3+rnd2()*3,bh,'#5a5148'); px(bx,160-bh,1,bh,'#7a7064'); }
  px(160,158,50,4,'#6f8a8a'); px(164,161,40,2,'#57706f');
""","")
rep("    if(tn.id==='lastpump'){ px(tx-10,ty-8,1,10,'#3a3129'); px(tx-13,ty-9,7,1,'#3a3129'); }\n","")
rep("  txt('five towns, one road  ·  only Dustwell is open to you so far',W/2,56,10,C.dim,'center','normal');",
    "  txt('three towns, one road  ·  only Dustwell is open to you so far',W/2,56,10,C.dim,'center','normal');")
rep("b:'The monthly haul from Old Meridian never arrived.", "b:'The monthly haul from the east never arrived.")

# ---------- 6. the town page is the next morning ----------
rep("function afterPaper(){ if(S.day%5===0&&S.history.length){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub(); }\n"
    "/* the Herald is delivered, not shoved in your face: it waits behind a button on the town page */\n"
    "function afterReport(){ if(paperDay(S.day)){ rollEvent(); S.paperFresh=true; S.paperDay=S.day; } afterPaper(); }",
    "/* the Herald is delivered, not shoved in your face: it waits behind a button on the town page.\n"
    "   Closing the dusk report moves the calendar on: the town page is the NEXT MORNING, so S.day is the day about to be traded. */\n"
    "function afterReport(){\n"
    "  if(paperDay(S.day)){ rollEvent(); S.paperFresh=true; S.paperDay=S.day; }\n"
    "  const books=S.day%5===0&&S.history.length;\n"
    "  S.day++;\n"
    "  if(books){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub();\n"
    "}")
rep("function nextDay(){ S.day++; startDay(); }",
    "function nextDay(){ startDay(); }                        /* the day number already moved on when dusk closed */")
rep("function hubOpenDay(){ if(S.fresh){ S.fresh=false; S.scene='dayintro'; S.sceneT=0; } else nextDay(); }",
    "function hubOpenDay(){ S.fresh=false; startDay(); }")
rep("function effDay(){ return CRAFT.demo ? S.day : S.day+1; }",
    "function effDay(){ return S.day; }                        /* the town page already is the trading day */")
rep("  S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day+1;", "  S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day;")
rep("  { const e=S.paperFresh?null:evTomorrow(); if(e){ const up=e.m>1; txt('TOMORROW: '+CATS[e.cat].name+' '+evPct(e)+'  ·  '+e.h.join(' '),x+w-30,y+62,12,up?C.green:C.red,'right'); } }\n"
    "  txt(S.fresh?'before your first day':('the night after day '+S.day),x+30,y+64,12,C.dim,'left','normal');\n"
    "  txt('purse '+S.caps+'c   ·   rent '+(S.fresh?'tonight ':'tomorrow ')+rentFor(S.fresh?S.day:S.day+1)+'c',x+w-30,y+36,14,C.ink,'right');",
    "  { const e=S.paperFresh?null:evToday(); if(e){ const up=e.m>1; txt('TODAY: '+CATS[e.cat].name+' '+evPct(e)+'  ·  '+e.h.join(' '),x+w-30,y+62,12,up?C.green:C.red,'right'); } }\n"
    "  txt('morning of day '+S.day,x+30,y+64,12,C.dim,'left','normal');\n"
    "  txt('purse '+S.caps+'c   ·   rent tonight '+rentFor(S.day)+'c',x+w-30,y+36,14,C.ink,'right');")
rep("  button(W/2-230,iy+ih+28,460,62,'OPEN THE STALL  ·  DAY '+(S.fresh?S.day:S.day+1),()=>hubOpenDay(),C.gold,18);\n}",
    "  button(W/2-230,iy+ih+28,460,62,'OPEN THE STALL  ·  DAY '+S.day,()=>hubOpenDay(),C.gold,18);\n"
    "  { const nl=newLooksOn(S.day);                            /* what came in overnight, at the foot of the page */\n"
    "    if(nl.length){\n"
    "      const kinds={hat:'costume',face:'costume',coat:'colour',awning:'colour',lantern:'colour',flag:'colour',pattern:'texture',wall:'texture'}, cnt={};\n"
    "      nl.forEach(t=>{ const k=kinds[t.cat]||'thing'; cnt[k]=(cnt[k]||0)+1; });\n"
    "      const parts=Object.keys(cnt).map(k=>cnt[k]+' '+k+(cnt[k]>1?'s':''));\n"
    "      const msg='NEW AT THE FIXER: '+parts.join(' · '), mw=txtw(msg,14)+40;\n"
    "      plate(W/2-mw/2,y+h-52,mw,36,'#1d1520',C.purple);\n"
    "      txt(msg,W/2,y+h-34,14,C.purple,'center');\n"
    "    } else txt('nothing new at the Fixer this morning',W/2,y+h-34,10,C.dimmer,'center','normal'); }\n}")
rep("  button(x+24,y+510,296,44,'OPEN THE STALL · DAY '+(S.fresh?S.day:S.day+1),()=>{dropTries();S.editName=false;hubOpenDay();},C.gold,12);",
    "  button(x+24,y+510,296,44,'OPEN THE STALL · DAY '+S.day,()=>{dropTries();S.editName=false;hubOpenDay();},C.gold,12);")
rep("  { const up=ev.m>1, stale=ev.day<=S.day;               /* the part the trader actually needs */",
    "  { const up=ev.m>1, stale=ev.day<S.day;                /* the part the trader actually needs; read in the morning it says TODAY */")
rep("    txt(stale?('DAY '+ev.day):'TOMORROW',tx2+12,y+340,10,FADE,'left','normal');",
    "    txt(stale?('DAY '+ev.day):'TODAY',tx2+12,y+340,10,FADE,'left','normal');")
# NEW AT THE FIXER leaves the day card
rep("""  const nl=newLooksOn(S.day);
  if(nl.length){
    const kinds={hat:'costume',face:'costume',coat:'colour',awning:'colour',lantern:'colour',flag:'colour',pattern:'texture',wall:'texture'};
    const cnt={};
    nl.forEach(t=>{ const k=kinds[t.cat]||'thing'; cnt[k]=(cnt[k]||0)+1; });
    const parts=Object.keys(cnt).map(k=>cnt[k]+' '+k+(cnt[k]>1?'s':''));
    txt('NEW AT THE FIXER: '+parts.join(' · '),W/2,y+200,14,C.purple,'center');
  }
  txt('purse '+S.caps+'c',W/2,y+228,13,C.dim,'center','normal');""",
"""  txt('purse '+S.caps+'c',W/2,y+228,13,C.dim,'center','normal');""")

# sunrise over the town + a dusk version for the intro
rep("let CITY_IMG=null;\nfunction buildCity(){\n"
    "  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');\n"
    "  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };\n"
    "  ['#2a2238','#3d2c40','#5a3644','#7d4440','#a85c3a','#cf7c3a','#e39a48'].forEach((col,i)=>px(0,i*8,Wc,9,col));\n"
    "  for(let dy=-13;dy<=13;dy++){ const w=Math.floor(Math.sqrt(169-dy*dy)); px(104-w,40+dy,w*2+1,1,dy<-4?'#f6d08a':'#f0b060'); }",
    "let CITY_IMG=null, CITY_DUSK=null;\n"
    "/* mode 'dawn' (the town page: every visit is the next morning) or 'dusk' (the intro) */\n"
    "function buildCity(mode){\n"
    "  const dawn=mode!=='dusk';\n"
    "  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');\n"
    "  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };\n"
    "  (dawn?['#2c2a4e','#4a3a62','#7a4a5c','#b06a50','#dc9458','#f2bc70','#fbe0a0']:['#2a2238','#3d2c40','#5a3644','#7d4440','#a85c3a','#cf7c3a','#e39a48']).forEach((col,i)=>px(0,i*8,Wc,9,col));\n"
    "  if(dawn){                                                   /* the sun coming up behind the wall, rays fanning out */\n"
    "    for(let r=0;r<9;r++){ const a=-Math.PI*0.95+r*(Math.PI*0.9/8); for(let k=18;k<80;k+=2) px(104+Math.cos(a)*k,58+Math.sin(a)*k,2,1,'rgba(255,240,190,0.35)'); }\n"
    "    for(let dy=-17;dy<=0;dy++){ const w=Math.floor(Math.sqrt(289-dy*dy)); px(104-w,58+dy,w*2+1,1,dy<-9?'#fff4c8':'#ffd884'); }\n"
    "    [[20,16],[27,13],[34,17],[118,20],[124,18]].forEach(b=>{ px(b[0],b[1],1,1,'#3a2a3a'); px(b[0]+1,b[1]-1,1,1,'#3a2a3a'); px(b[0]+2,b[1],1,1,'#3a2a3a'); });\n"
    "  } else for(let dy=-13;dy<=13;dy++){ const w=Math.floor(Math.sqrt(169-dy*dy)); px(104-w,40+dy,w*2+1,1,dy<-4?'#f6d08a':'#f0b060'); }")
rep("    for(let wy=top+4;wy<58;wy+=5) for(let wx=bx+2;wx<bx+w-2;wx+=3) if(rn()<0.16) px(wx,wy,1,2,'#f0c060');",
    "    for(let wy=top+4;wy<58;wy+=5) for(let wx=bx+2;wx<bx+w-2;wx+=3) if(rn()<0.16) px(wx,wy,1,2,dawn?'#4a3a4a':'#f0c060');   /* lamps are out by morning */")
rep("  [[64,57],[85,57]].forEach(l=>{ px(l[0],l[1],2,2,'#f6d874'); px(l[0]-1,l[1]-1,4,1,'#1d1620'); });",
    "  [[64,57],[85,57]].forEach(l=>{ px(l[0],l[1],2,2,dawn?'#6a5a4a':'#f6d874'); px(l[0]-1,l[1]-1,4,1,'#1d1620'); });")
rep("  if(!CITY_IMG) CITY_IMG=buildCity();\n"
    "  const iw=600, ih=320, ix=W/2-iw/2, iy=y+96;\n"
    "  plate(ix-6,iy-6,iw+12,ih+12,'#0d0a08','#5c4a37');\n"
    "  g.imageSmoothingEnabled=false; g.drawImage(CITY_IMG,ix,iy,iw,ih);\n"
    "  [[64,57],[85,57]].forEach((l,i)=>{ const p=0.5+Math.sin(S.t*3+i*2)*0.25; const gx=ix+l[0]*4+4, gy=iy+l[1]*4+4, gr=g.createRadialGradient(gx,gy,2,gx,gy,40);\n"
    "    gr.addColorStop(0,'rgba(246,216,116,'+(0.5*p)+')'); gr.addColorStop(1,'rgba(246,216,116,0)'); g.fillStyle=gr; g.fillRect(gx-40,gy-40,80,80); });",
    "  if(!CITY_IMG) CITY_IMG=buildCity('dawn');\n"
    "  const iw=600, ih=320, ix=W/2-iw/2, iy=y+96;\n"
    "  plate(ix-6,iy-6,iw+12,ih+12,'#0d0a08','#5c4a37');\n"
    "  g.imageSmoothingEnabled=false; g.drawImage(CITY_IMG,ix,iy,iw,ih);\n"
    "  { const p=0.6+Math.sin(S.t*1.2)*0.2, gx=ix+104*4+2, gy=iy+58*4, gr=g.createRadialGradient(gx,gy,10,gx,gy,150);   /* the sun's glow breathes */\n"
    "    gr.addColorStop(0,'rgba(255,236,170,'+(0.45*p)+')'); gr.addColorStop(1,'rgba(255,200,120,0)'); g.fillStyle=gr; g.fillRect(gx-150,gy-150,300,300); }")

# door icons
rep("function drawHub(){\n  dim(0.8);",
    "const HUB_PX={\n"
    " fixer:['.....kk.','....kkkk','....kk.k','...kkkk.','..kkk...','.kkk....','kkk.....','kk......'],\n"
    " bench:['..kkkk..','..kkkkk.','..kkkkk.','..kkkk..','....k...','....k...','....k...','....k...'],\n"
    " rig:  ['..kkkk..','.kkkkkk.','.kk..kk.','kkkkkkkk','k.k..k.k','k.k..k.k','k.k..k.k','.k....k.'],\n"
    " looks:['...kk...','..kkkk..','..kkkk..','..kkkk..','kkkkkkkk','kkkkkkkk','........','........'],\n"
    " book: ['kkkkkkkk','k..kk..k','k..kk..k','k..kk..k','k..kk..k','k..kk..k','kkkkkkkk','...kk...'],\n"
    " map:  ['...k....','..kkk...','.k.k.k..','kkkkkkk.','.k.k.k..','..kkk...','...k....','........'],\n"
    " ach:  ['kkkkkkkk','k.kkkk.k','k.kkkk.k','.kkkkkk.','..kkkk..','...kk...','..kkkk..','.kkkkkk.'],\n"
    " paper:['kkkkkkk.','k.....k.','k.kk..k.','k.kk.kk.','k....kkk','k.kkk.kk','k.....kk','kkkkkkkk']\n"
    "};\n"
    "const HUB_SPR={};\n"
    "function hubIcon(id,col){ const k=id+col; if(!HUB_SPR[k]) HUB_SPR[k]=spriteFrom(HUB_PX[id],{k:col}); return HUB_SPR[k]; }\n"
    "/* a town door: a button with its icon on the left */\n"
    "function door(x,y,w,h,label,fn,col,size,icon){ button(x,y,w,h,label,fn,col,size); blit(hubIcon(icon,col),x+12,y+h/2-8,2); }\n"
    "function drawHub(){\n  dim(0.8);")
rep("  button(lx,by,bw,bh,'THE FIXER',()=>{S.scene='shop';S.sceneT=0;},C.gold,15);\n"
    "  button(lx,by+(bh+gp),bw,bh,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>buyBench(),canWb?'#8fd0ee':C.dimmer,S.wb?13:11);\n"
    "  button(lx,by+(bh+gp)*2,bw,bh,'TRANSPORT '+rigCount()+'/'+RIG.length,()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',13);\n"
    "  button(lx,by+(bh+gp)*3,bw,bh,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,13);\n"
    "  button(rx,by,bw,bh,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,13);\n"
    "  button(rx,by+(bh+gp),bw,bh,'THE MAP',()=>openPage('map'),'#8fd0ee',13);\n"
    "  button(rx,by+(bh+gp)*2,bw,bh,'ACHIEVEMENTS '+achCount()+'/'+ACH.length,()=>openPage('ach'),C.gold,10);\n"
    "  { const has=!!S.paperDay, fresh=!!S.paperFresh, hy=by+(bh+gp)*3;\n"
    "    if(has) button(rx,hy,bw,bh,'THE HERALD',()=>{ S.paperFresh=false; S.scene='paper'; S.sceneT=0; saveGame(); },fresh?C.gold:C.dim,13);\n"
    "    else { plate(rx,hy,bw,bh,'#15110d','#33291f'); txt('THE HERALD',rx+bw/2,hy+bh/2-6,13,C.dimmer,'center'); txt('no paper yet',rx+bw/2,hy+bh/2+13,9,C.dimmer,'center','normal'); }",
    "  door(lx,by,bw,bh,'THE FIXER',()=>{S.scene='shop';S.sceneT=0;},C.gold,15,'fixer');\n"
    "  door(lx,by+(bh+gp),bw,bh,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>buyBench(),canWb?'#8fd0ee':C.dimmer,S.wb?13:11,'bench');\n"
    "  door(lx,by+(bh+gp)*2,bw,bh,'TRANSPORT '+rigCount()+'/'+RIG.length,()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',13,'rig');\n"
    "  door(lx,by+(bh+gp)*3,bw,bh,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,13,'looks');\n"
    "  door(rx,by,bw,bh,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,13,'book');\n"
    "  door(rx,by+(bh+gp),bw,bh,'THE MAP',()=>openPage('map'),'#8fd0ee',13,'map');\n"
    "  door(rx,by+(bh+gp)*2,bw,bh,'ACHIEVEMENTS '+achCount()+'/'+ACH.length,()=>openPage('ach'),C.gold,10,'ach');\n"
    "  { const has=!!S.paperDay, fresh=!!S.paperFresh, hy=by+(bh+gp)*3;\n"
    "    if(has) door(rx,hy,bw,bh,'THE HERALD',()=>{ S.paperFresh=false; S.scene='paper'; S.sceneT=0; saveGame(); },fresh?C.gold:C.dim,13,'paper');\n"
    "    else { plate(rx,hy,bw,bh,'#15110d','#33291f'); blit(hubIcon('paper',C.dimmer),rx+12,hy+bh/2-8,2); txt('THE HERALD',rx+bw/2,hy+bh/2-6,13,C.dimmer,'center'); txt('no paper yet',rx+bw/2,hy+bh/2+13,9,C.dimmer,'center','normal'); }")

# ---------- 8. the perk rail: bigger, and it ends level with the counter ----------
rep("const RAIL={x:8,w:118,py:108};\n"
    "let TIP=null, RAILPOS=[null,null,null,null,null,null], RAILAY=252;\n"
    "function perkRailRect(i){ return RAILPOS[i]||{x:RAIL.x+6,y:RAILAY,w:RAIL.w-12,h:44}; }",
    "const RAIL={x:10,w:150};\n"
    "let TIP=null, RAILPOS=[null,null,null,null,null,null], RAILAY=252;\n"
    "function perkRailRect(i){ return RAILPOS[i]||{x:RAIL.x+6,y:RAILAY,w:RAIL.w-12,h:54}; }")
start=src.index("/* only what you actually own shows on the rail */\nfunction drawPerkRail(){")
end=src.index("function drawPerkTip(){")
cut=src[start:end]
assert end>start and cut.count("function ")==1, cut[:300]
new_rail = r"""/* only what you actually own shows on the rail. The rail hangs from the bottom: its last card
   sits level with the bottom of THE COUNTER, whatever you own. */
function drawPerkRail(){
  TIP=null; RAILPOS=[null,null,null,null,null,null];
  const live=S.scene==='play';
  const owned=UPGRADES.filter(u=>S.up[u.id]>0), acts=ACTIVES.filter((a,i)=>S.actOwn[i]);
  if(!owned.length&&!acts.length) return;
  const PW=40, PG=6, AH=54, AG=70;                                   /* passive tile / active card and its pitch */
  const cb=counterBlock(), bottom=cb.y+cb.h;
  const hPass=owned.length?22+Math.ceil(owned.length/3)*(PW+PG)+6:0;
  const hAct=acts.length?22+acts.length*AG:0;
  let y=bottom-hPass-hAct;
  RAILAY=y;
  if(S.patterT>0||S.steadyT>0||S.signalT>0){                          /* a running effect sits above the rail */
    const sy=y-34;
    if(S.patterT>0){ plate(RAIL.x+6,sy,RAIL.w-12,26,'#2a1e33','#a173c8'); txt('PATTER '+S.patterT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#c9a3e0','center'); }
    else if(S.steadyT>0){ plate(RAIL.x+6,sy,RAIL.w-12,26,'#1e2a18','#7fb74f'); txt('STEADY '+S.steadyT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#a8d98a','center'); }
    else { plate(RAIL.x+6,sy,RAIL.w-12,26,'#33200f','#f08a4a'); txt('SIGNAL '+S.signalT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#f8b888','center'); }
  }
  if(owned.length){
    txt('PASSIVE',RAIL.x+8,y+10,10,C.dim);
    owned.forEach((u,i)=>{
      const cx=RAIL.x+6+(i%3)*(PW+PG), cy=y+22+Math.floor(i/3)*(PW+PG), lv=S.up[u.id];
      plate(cx,cy,PW,PW,'#2a2218',C.gold);
      blit(perkIcon(u.id,C.gold),cx+8,cy+8,3);
      if(lv>1){ plate(cx+PW-15,cy+PW-15,15,15,'#2a2012',C.gold); txt(lv,cx+PW-7,cy+PW-7,9,C.gold,'center'); }
      if(live&&inRect(MX,MY,{x:cx,y:cy,w:PW,h:PW}))
        TIP={x:cx+PW+6,y:cy,title:u.n,body:u.d,col:C.gold,
             foot: lv>=u.max ? 'fully upgraded' : ('level '+lv+' of '+u.max+' · next '+u.cost[lv]+'c')};
    });
    y+=hPass;
  }
  if(!acts.length) return;
  txt('ACTIVE',RAIL.x+8,y+10,10,C.gold);
  txt('KEYS 1-6',RAIL.x+RAIL.w-8,y+10,9,C.dimmer,'right');
  let n=0;
  ACTIVES.forEach((a,i)=>{
    if(!S.actOwn[i]) return;
    const r={x:RAIL.x+6,y:y+22+n*AG,w:RAIL.w-12,h:AH};
    RAILPOS[i]=r; n++;
    const cd=S.actCd[i], ready=cd<=0, hov=inRect(MX,MY,r);
    plate(r.x,r.y,r.w,r.h, ready?(hov?'#3a2f1e':'#241d12'):'#141009', ready?a.col:'#4a3b2c');
    if(cd>0){
      g.globalAlpha=0.6; g.fillStyle='#0b0907';
      g.fillRect(r.x+3,r.y+3,r.w-6,Math.round((r.h-6)*(cd/a.cd))); g.globalAlpha=1;
    }
    keycap(r.x+4,r.y+9,34,36,''+a.key,a.col,ready?'ready':'rest',(S.keyFx&&S.keyFx[i]>0));
    blit(perkIcon(a.id,ready?a.col:'#6b5a45'),r.x+44,r.y+11,4);
    if(a.id==='hire'&&S.handT>0) txt(S.handT.toFixed(0)+'s',r.x+r.w-28,r.y+r.h/2,15,a.col,'center');
    else if(cd>0) txt(Math.ceil(cd)+'s',r.x+r.w-28,r.y+r.h/2,15,C.ink,'center');
    else txt('READY',r.x+r.w-28,r.y+r.h/2,9,a.col,'center');
    txt(a.n.split(' ').pop(),r.x+r.w/2,r.y+r.h+8,10,ready?a.col:C.dimmer,'center');
    if(live&&hov)
      TIP={x:r.x+r.w+10,y:r.y,title:a.n+(a.id==='hire'?' · LVL '+S.hire.lvl:''),body:a.id==='hire'?('KIT works the stall beside you for '+hired().dur+' seconds: files, sells and haggles.'):a.d,col:a.col,
           foot:'key '+a.key+' · '+a.cd+'s cooldown · '+(cd>0?(Math.ceil(cd)+'s to go'):'ready')};
    BTNS.push({x:r.x,y:r.y,w:r.w,h:r.h,fn:()=>fireActive(i)});
  });
}
"""
src=src[:start]+new_rail+src[end:]; n+=1

# ---------- 9. the intro: four cards, NES style ----------
rep("  button(W/2-160,y+h-96,320,58,'OK',()=>beginRun(),C.gold,22);",
    "  button(W/2-160,y+h-96,320,58,'OK',()=>startIntro(),C.gold,22);")
rep("function toTitle(){ S.paused=false;",
    r"""/* ---------- the intro: four cards on black, text typed under each, a click turns the page ---------- */
const INTRO=[
 {text:'DUSTWELL. THE EDGE OF THE DUST.'},
 {text:"It's a new dawn..."},
 {text:'And a new beginning for me...'},
 {text:'Time to trade goods!'}
];
let INTRO_BG=null, INTRO_KEY=null;
const WALK_PX=[
 ['...kk...','..kkkkk.','...kk...','..kkkk..','.kkkkkk.','.k.kk.k.','.k.kk.k.','...kk...','...kk...','..k..k..','.k....k.','k......k'],
 ['...kk...','..kkkkk.','...kk...','..kkkk..','.kkkkkk.','.k.kk.k.','.k.kk.k.','...kk...','...kk...','...kk...','...kk...','...kk...']
].map(r=>spriteFrom(r,{k:'#120c10'}));
function buildIntroWalk(){                                  /* the road at first light */
  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  ['#1c1a3a','#33284e','#5a3a58','#8a4a52','#c06a48','#e8985a','#f8c878'].forEach((col,i)=>px(0,i*8,Wc,9,col));
  for(let dy=-14;dy<=0;dy++){ const w=Math.floor(Math.sqrt(196-dy*dy)); px(100-w,56+dy,w*2+1,1,dy<-7?'#fff6d0':'#ffdc8a'); }
  let sd=5; const rn=()=>{ sd=(sd*1103515245+12345)&0x7fffffff; return sd/0x7fffffff; };
  let fx=0; while(fx<Wc){ const w=3+rn()*8, h=3+rn()*12; px(fx,56-h,w,h,'#2a1a2c'); fx+=w+2+rn()*6; }
  px(0,56,Wc,24,'#241a1c'); for(let k=0;k<26;k++) px(rn()*Wc,58+rn()*20,4+rn()*10,1,k%2?'#31242a':'#1a1214');
  px(0,64,Wc,1,'#3a2a2e');
  return c;
}
function buildIntroKey(){                                   /* a rusty key, close, in an open hand */
  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  ['#100c10','#181018','#241620','#30202a','#3c2a30','#4a3634','#5a4238','#6a4e3c'].forEach((col,i)=>px(0,i*10,Wc,11,col));
  /* sleeve, wrist, palm */
  px(96,54,54,26,'#3a2a20'); px(96,54,54,3,'#4e3a2c'); px(100,60,50,2,'#2a1c16');
  px(84,46,30,24,'#d2a476'); px(84,46,30,3,'#e2b888');                               /* wrist / heel of the hand */
  px(52,34,44,34,'#d8ac7c'); px(52,34,44,4,'#e8c090'); px(52,64,44,4,'#b08458');      /* palm */
  px(50,36,3,30,'#c0946a'); px(94,38,3,28,'#c0946a');
  /* thumb, up the left side */
  px(40,40,14,10,'#d8ac7c'); px(38,42,6,8,'#d8ac7c'); px(40,40,14,2,'#e8c090'); px(40,48,14,2,'#b08458'); px(44,44,6,2,'#c8987a');
  /* the key lies across the palm: bow on the left, teeth to the right */
  const R='#8a5a2a', R2='#b0783a', R3='#5a3818', R4='#c89058';
  for(let dy=-9;dy<=9;dy++){ const w=Math.floor(Math.sqrt(81-dy*dy)); px(28-w,42+dy,w*2+1,1,R); }
  for(let dy=-4;dy<=4;dy++){ const w=Math.floor(Math.sqrt(16-dy*dy)); px(28-w,42+dy,w*2+1,1,'#241a16'); }
  px(21,34,10,2,R2); px(20,49,12,2,R3); px(24,36,2,2,R4);
  px(36,40,58,5,R); px(36,40,58,1,R2); px(36,44,58,1,R3);                              /* shaft */
  px(84,45,4,7,R); px(90,45,4,10,R); px(78,45,3,5,R); px(84,45,4,1,R2); px(90,45,4,1,R2);   /* teeth */
  [[44,41],[58,42],[66,41],[74,43],[52,43]].forEach(p=>px(p[0],p[1],2,1,R4));           /* worn bright spots */
  [[48,42],[62,43],[80,41]].forEach(p=>px(p[0],p[1],3,2,'#6a4020'));                     /* rust */
  /* fingers curl over the shaft */
  [[54,44],[64,44],[74,44],[84,46]].forEach((f,i)=>{ const fw=9, fh=[22,24,22,18][i];
    px(f[0],f[1],fw,fh,'#d8ac7c'); px(f[0],f[1],fw,2,'#e8c090'); px(f[0],f[1]+fh-3,fw,3,'#b08458'); px(f[0]+fw-1,f[1],1,fh,'#b8906a');
    px(f[0]+2,f[1]+9,fw-4,1,'#c8987a'); });
  /* a little light on the key from the window */
  for(let i=0;i<40;i++) px(10+Math.random()*60,6+Math.random()*24,1,1,'rgba(255,230,180,0.25)');
  return c;
}
function startIntro(){ if(!INTRO_BG) INTRO_BG=buildIntroWalk(); if(!INTRO_KEY) INTRO_KEY=buildIntroKey(); if(!CITY_DUSK) CITY_DUSK=buildCity('dusk');
  S.scene='intro'; S.sceneT=0; S.introN=0; S.introT=0; }
function introTyped(){ const s=INTRO[S.introN].text; return Math.min(s.length,Math.max(0,Math.floor((S.introT-0.7)*18))); }
function introClick(){
  const s=INTRO[S.introN].text;
  if(introTyped()<s.length){ S.introT=99; return; }          /* first click finishes the line */
  if(S.introN<INTRO.length-1){ S.introN++; S.introT=0; Snd.ui(); } else beginRun();
}
function drawIntro(){
  S.introT+=1/60;
  g.fillStyle='#000'; g.fillRect(0,0,W,H);
  const n=S.introN, iw=600, ih=320, ix=W/2-iw/2, iy=96, fade=clamp(S.introT/0.7,0,1);
  g.globalAlpha=fade; g.imageSmoothingEnabled=false;
  if(n===0) g.drawImage(CITY_DUSK,ix,iy,iw,ih);
  else if(n===1){
    g.drawImage(INTRO_BG,ix,iy,iw,ih);
    const wx=18+Math.min(78,S.introT*7), f=Math.floor(S.introT*4)%2, bob=f?0:1;   /* a figure walks toward the light */
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-30,iy+62*4,58,3);
    blit(WALK_PX[f],ix+wx*4,iy+(64-12*2)*4-bob*4,8);
  }
  else if(n===2) g.drawImage(INTRO_KEY,ix,iy,iw,ih);
  else {
    if(!SCENE) SCENE=buildScene();
    g.fillStyle='#1a1410'; g.fillRect(ix,iy,iw,ih);
    g.drawImage(SCENE,28,10,150,80,ix,iy,iw,ih);                       /* the stall, opened */
    blit(traderSprite(),ix+iw-170,iy+ih-150,4);
  }
  g.globalAlpha=1;
  g.fillStyle='#2a221a'; g.fillRect(ix-4,iy-4,iw+8,4); g.fillRect(ix-4,iy+ih,iw+8,4); g.fillRect(ix-4,iy,4,ih); g.fillRect(ix+iw,iy,4,ih);
  const s=INTRO[n].text, k=introTyped(), shown=s.slice(0,k), cur=(k<s.length||Math.sin(S.t*8)>0)?'_':' ';
  txt(shown+cur,W/2,iy+ih+80,22,n===0?C.gold:C.ink,'center');
  for(let i=0;i<INTRO.length;i++){ g.fillStyle=i===n?C.gold:'#3a3228'; g.fillRect(W/2-30+i*16,iy+ih+130,10,6); }
  if(k>=s.length) txt('click to go on',W/2,iy+ih+170,11,C.dimmer,'center','normal');
  button(W-140,20,120,36,'SKIP',()=>beginRun(),C.dim,12);
}
function toTitle(){ S.paused=false;""")
rep("  else if(S.scene==='howto') drawMenu();",
    "  else if(S.scene==='howto') drawMenu();\n  else if(S.scene==='intro') drawIntro();")
rep("  if(['title','slots','howto','settings','bye','gameover','ach','map'].indexOf(S.scene)<0) drawHUD();",
    "  if(['title','slots','howto','intro','settings','bye','gameover','ach','map'].indexOf(S.scene)<0) drawHUD();")
rep("  for(let i=BTNS.length-1;i>=0;i--){ const b=BTNS[i]; if(inRect(p.x,p.y,b)){ Snd.ui(); b.fn(); return; } }\n"
    "  if(S.scene==='play'&&!S.paused){",
    "  for(let i=BTNS.length-1;i>=0;i--){ const b=BTNS[i]; if(inRect(p.x,p.y,b)){ Snd.ui(); b.fn(); return; } }\n"
    "  if(S.scene==='intro'){ introClick(); return; }\n"
    "  if(S.scene==='play'&&!S.paused){")
rep("window.addEventListener('keydown',ev=>{\n"
    "  if(S.scene==='play'&&!S.paused&&ev.key>='1'&&ev.key<='6'){",
    "window.addEventListener('keydown',ev=>{\n"
    "  if(S.scene==='intro'){ if(ev.key==='Escape') beginRun(); else if(ev.key==='Enter'||ev.key===' ') introClick(); ev.preventDefault(); return; }\n"
    "  if(S.scene==='play'&&!S.paused&&ev.key>='1'&&ev.key<='6'){")

open(P,'w').write(src)
print('applied',n,'edits')
