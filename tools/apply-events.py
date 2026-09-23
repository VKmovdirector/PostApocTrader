SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/events-demo.html"
s=open(f).read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b,1)
s=s.replace("'rustrations.","'rustrations.events.")            # the rig keeps its own saves, options and achievements
rep("<title>Rust &amp; Rations</title>","<title>Rust &amp; Rations - events test</title>")
rep("/* ================================================================\n   WALKTHROUGHS",open(SP+"/events.js").read()+"\n/* ================================================================\n   WALKTHROUGHS")
# price
rep("*(it.crafted?CRAFT.mult:1);\n","*(it.crafted?CRAFT.mult:1)*evMult(it.cat);\n")
# when the paper prints
rep("function paperDay(d){ return d>=5&&(d-5)%4===0; }","function paperDay(d){ return EVDEMO.everyNight ? d>=1 : (d>=5&&(d-5)%4===0); }")
rep("function afterReport(){ if(paperDay(S.day)){ S.scene='paper'; S.sceneT=0; } else afterPaper(); }","function afterReport(){ if(paperDay(S.day)){ rollEvent(); S.scene='paper'; S.sceneT=0; } else afterPaper(); }")
# bookkeeping: what the event was worth
rep("  S.cr.soldR[drag.item.r||0]++;","  { const em=evMult(drag.item.cat); if(em!==1) S.evGain=(S.evGain||0)+(price-Math.round(price/em)); }\n  S.cr.soldR[drag.item.r||0]++;")
rep("  const share=Math.round(price/list.length);","  { const em=evMult(list[0].item.cat); if(em!==1) S.evGain=(S.evGain||0)+(price-Math.round(price/em)); }\n  const share=Math.round(price/list.length);")
rep("  S.dayMis=0; S.dayFiled=0;","  S.dayMis=0; S.dayFiled=0; S.evGain=0;")
rep("  if(rp.mats>0) rows.push(","  { const e=evToday(); if(e) rows.push(['Herald: '+CATS[e.cat].name+' '+evPct(e),(S.evGain>=0?'+':'')+(S.evGain||0)+'c']); }\n  if(rp.mats>0) rows.push(")
rep("  S.shelves=[]; makeShelves(); startDay();","  S.event=null; S.evGain=0;\n  S.shelves=[]; makeShelves(); startDay();")
# the day itself: intro card, banner, shelf badge
rep("  if(S.day===3) txt('NEW: bulk orders","  { const e=evToday(); if(e){ const up=e.m>1; plate(x+40,y+196,w-80,50,up?'#1e2a18':'#2a1a16',up?C.green:C.red);\n      txt('TODAY: '+CATS[e.cat].name+' PRICES '+evPct(e),W/2,y+212,15,up?C.green:C.red,'center');\n      txt(e.h.join(' ')+'  ·  the Herald',W/2,y+233,10,C.dim,'center','normal'); } }\n  if(S.day===3) txt('NEW: bulk orders")
rep("    txt(cat.name,r.x+22,r.y+SHELF_HEAD/2,16,cat.col);","    txt(cat.name,r.x+22,r.y+SHELF_HEAD/2,16,cat.col);\n    { const e=evToday(); if(e&&e.cat===sh.cat){ const up=e.m>1, tx3=r.x+30+txtw(cat.name,16), tw3=txtw(evPct(e),11)+12;\n        g.fillStyle=up?C.green:C.red; g.fillRect(tx3,r.y+4,tw3,15); txt(evPct(e),tx3+tw3/2,r.y+12,11,'#14100c','center'); } }")
# town page reminder
rep("  txt('DUSTWELL',x+30,y+36,28,C.gold);","  txt('DUSTWELL',x+30,y+36,28,C.gold);\n  { const e=evTomorrow(); if(e){ const up=e.m>1; txt('TOMORROW: '+CATS[e.cat].name+' '+evPct(e)+'  ·  '+e.h.join(' '),x+w-30,y+62,12,up?C.green:C.red,'right'); } }")
# the newspaper
i=s.index("  txt('MEDS PRICES',tx2,y+134,30,INK,'left');"); j=s.index("  g.fillStyle=FADE; g.fillRect(x+30,y+372,w-60,1);")
s=s[:i]+"""  const ev=S.event||EVENTS[0];
  blit(EV_SPR[ev.type],tx2+tw2-34,y+112,4);
  txt(ev.type.toUpperCase(),tx2,y+114,10,FADE,'left','normal');
  txt(ev.h[0],tx2,y+142,28,INK,'left');
  txt(ev.h[1],tx2,y+174,28,INK,'left');
  g.fillStyle=INK; g.fillRect(tx2,y+192,tw2,2);
  let py2=wrapText(ev.b,tx2,y+212,tw2,16,11,INK);
  wrapText(ev.q,tx2,py2+22,tw2,16,11,FADE);
  { const up=ev.m>1;                                  /* the part the trader actually needs */
    g.fillStyle=INK; g.fillRect(tx2,y+318,tw2,44); g.fillStyle='#d8cdb4'; g.fillRect(tx2+3,y+321,tw2-6,38);
    txt('TOMORROW',tx2+12,y+340,10,FADE,'left','normal');
    txt(CATS[ev.cat].name+' PRICES '+(up?'UP ':'DOWN ')+evPct(ev),tx2+tw2-12,y+340,15,INK,'right'); }
"""+s[j:]
rep("""  const cols=[['RAIDERS SEEN NORTH','Three trucks, no colours flown.'],
              ['WATER TOWER HOLDS','Council votes to patch it again.'],
              ['ASH PLUM GLUT','Growers say the crop came early.']];""","  const cols=(S.event&&S.event.fill)||EV_FILL.slice(0,3);")
# save / load carry the event
rep("rig:S.rig,history:S.history,","rig:S.rig,event:S.event,history:S.history,")
rep("['day','caps','hire','actOwn','wb','wbDay','unl','mats','rig','history',","['day','caps','hire','actOwn','wb','wbDay','unl','mats','rig','event','history',")
# title: say what this is, and the test switch
rep("  txt('a trading post at the edge of the dust',lx,ly+78,15,'#d8c8a8','center','normal');","  txt('EVENTS TEST  ·  the Herald moves one price for one day',lx,ly+78,14,'#8fd0ee','center','normal');")
rep("  txt('build 19',W-20,H-18,10,C.dimmer,'right','normal');","  button(W/2-210,560,420,40,'HERALD PRINTS: '+(EVDEMO.everyNight?'EVERY NIGHT  (test)':'DAY 5, 9, 13...  (as in the game)'),()=>{EVDEMO.everyNight=!EVDEMO.everyNight;},EVDEMO.everyNight?C.green:C.dim,11);\n  txt('events test rig',W-20,H-18,10,C.dimmer,'right','normal');")
open(f,'w').write(s); print('ok')
