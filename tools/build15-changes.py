SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/index.html"
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    assert a in s, a[:70]
    if cnt==0: s=s.replace(a,b)
    else: s=s.replace(a,b,cnt)
rep("RUST & RATIONS  -  build 14 (pixel art, workbench)","RUST & RATIONS  -  build 15 (pixel art, workbench, map, achievements)")
rep("/* ================================================================\n   WALKTHROUGHS",open(SP+"/achmap.js").read()+"\n/* ================================================================\n   WALKTHROUGHS")
# ---- hooks
rep("  S.cr.soldR[drag.item.r||0]++;","  S.cr.soldR[drag.item.r||0]++;\n  AST.sold=n0('sold')+1; AST.earned=n0('earned')+price; AST.maxSale=Math.max(n0('maxSale'),price);\n  if(drag.src==='counter') AST.counterSales=n0('counterSales')+1;\n  if(c.want.kind==='item') AST.exact=n0('exact')+1;\n  if((drag.haggle||0)>=priceMults().haggleMax-0.001) AST.maxHag=n0('maxHag')+1;\n  (AST.types=AST.types||{})[c.type.id]=1; achCheck();")
rep("  S.caps+=price; S.earned+=price; S.sold++; S.bulkSold++;","  S.caps+=price; S.earned+=price; S.sold+=list.length; S.bulkSold++;       /* a bulk order counts every piece as sold */\n  AST.sold=n0('sold')+list.length; AST.earned=n0('earned')+price; AST.maxSale=Math.max(n0('maxSale'),price);\n  AST.bulk=n0('bulk')+1; if(list.length>=4) AST.bulk4=1; (AST.types=AST.types||{})[c.type.id]=1; achCheck();")
rep("  S.combo++; S.maxCombo=Math.max(S.maxCombo,S.combo); S.dayCombo=Math.max(S.dayCombo,S.combo);","  S.combo++; S.maxCombo=Math.max(S.maxCombo,S.combo); S.dayCombo=Math.max(S.dayCombo,S.combo);\n  if(S.combo>n0('bestStreak')) achMax('bestStreak',S.combo);")
rep("  if(mis){\n    breakCombo();","  if(mis){ S.dayMis=(S.dayMis||0)+1; achInc('misfiled'); } else { S.dayFiled=(S.dayFiled||0)+1; achInc('filed'); }\n  if(mis){\n    breakCombo();")
rep("    S.spilled++; S.combo=0;","    S.spilled++; S.combo=0; achInc('spilled');")
rep("S.scrapN=(S.scrapN||0)+1;","S.scrapN=(S.scrapN||0)+1; achInc('scrapped');",0)
rep("          float(c.x+260,c.y+26,'TOO GREEDY',C.red,22);","          float(c.x+260,c.y+26,'TOO GREEDY',C.red,22); achInc('snaps');")
rep("  S.caps-=rent+wage;\n","  S.caps-=rent+wage;\n  AST.bestDay=Math.max(n0('bestDay'),S.day); AST.bestTake=Math.max(n0('bestTake'),S.earned);\n  if(S.sold>=8&&S.angry===0) AST.noWalkDay=1;\n  if((S.dayFiled||0)>=10&&!S.dayMis&&!S.spilled) AST.spotlessDay=1;\n  if(S.caps>=0){ AST.bestPurse=Math.max(n0('bestPurse'),S.caps); if(S.caps<10) AST.whisker=1; }\n  achCheck();\n")
rep("  S.dayTime=0; S.dayLen=dayLenFor(S.day);","  S.dayMis=0; S.dayFiled=0;\n  S.dayTime=0; S.dayLen=dayLenFor(S.day);")
rep("      button(W/2+6,y+h-76,244,52,'KEEP THEM',()=>afterReport(),C.gold,14);","      button(W/2+6,y+h-76,244,52,'KEEP THEM',()=>{ achInc('kept'); afterReport(); },C.gold,14);")
rep("()=>{ scrapLeftovers(); S.deadReason=null; },C.gold,12);","()=>{ scrapLeftovers(); S.deadReason=null; achInc('fireSale'); },C.gold,12);")
rep("  if(u.id==='drone') TRADER_KEY='';","  if(u.id==='drone') TRADER_KEY='';\n  AST.perks=n0('perks')+1; if(UPGRADES.every(q=>S.up[q.id]>=q.max)) AST.allPassive=1; achCheck();")
rep("      ()=>{ S.caps-=a.cost; S.actOwn[i]=true; Snd.coin(4); flash(a.col,0.2); },''+a.key);","      ()=>{ S.caps-=a.cost; S.actOwn[i]=true; Snd.coin(4); flash(a.col,0.2); AST.perks=n0('perks')+1; if(S.actOwn.every(Boolean)) AST.allActive=1; achCheck(); },''+a.key);")
rep("      ()=>{ S.caps-=nx.fee; S.hire.lvl=nx.lvl; S.actOwn[4]=true; Snd.coin(4); flash('#8fd0ee',0.2); }, '5');","      ()=>{ S.caps-=nx.fee; S.hire.lvl=nx.lvl; S.actOwn[4]=true; Snd.coin(4); flash('#8fd0ee',0.2); AST.perks=n0('perks')+1; AST.hired=1; if(S.actOwn.every(Boolean)) AST.allActive=1; achCheck(); }, '5');")
rep("  S.actCd[i]=a.cd;\n  Snd.good(); flash(a.col,0.18);","  S.actCd[i]=a.cd; achInc('actUsed');\n  Snd.good(); flash(a.col,0.18);")
rep("  saveLook(); Snd.coin(4); flash(C.gold,0.2);","  saveLook(); Snd.coin(4); flash(C.gold,0.2); achInc('looks');")
rep("      S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day+1;","      S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day+1; achInc('bench');")
rep("S.tray[free]=rar(it,0,true); S.cr.crafted++;","S.tray[free]=rar(it,0,true); AST.crafted=n0('crafted')+1; S.cr.crafted++;")
rep("  S.anvil=rar(S.anvil,S.anvil.r+1); S.cr.up[S.anvil.r]++;","  S.anvil=rar(S.anvil,S.anvil.r+1); S.cr.up[S.anvil.r]++;\n  if(S.anvil.r===3) AST.madeLeg=1; achCheck();")
# ---- scenes
rep("  else if(S.scene==='workshop') drawWorkshop();","  else if(S.scene==='ach') drawAchievements();\n  else if(S.scene==='map') drawMap();\n  else if(S.scene==='workshop') drawWorkshop();")
rep("  if(S.scene!=='menu'&&S.scene!=='gameover') drawHUD();","  if(S.scene!=='menu'&&S.scene!=='gameover'&&S.scene!=='ach'&&S.scene!=='map') drawHUD();\n  drawToasts(1/60);")
# menu: tighter rows, two page buttons
rep("    yy+=62;\n  });\n  button(W/2-160,y+h-86,320,54,'OPEN THE STALL',()=>startRun(),C.gold,20);","    yy+=54;\n  });\n  button(W/2-160,y+h-136,154,38,'THE MAP',()=>openPage('map'),'#8fd0ee',12);\n  button(W/2+6,y+h-136,154,38,'ACHIEVEMENTS '+achCount()+'/'+ACH.length,()=>openPage('ach'),C.gold,10);\n  button(W/2-160,y+h-86,320,54,'OPEN THE STALL',()=>startRun(),C.gold,20);")
rep("  txt('space or esc to resume  ·  m mutes',W/2,H/2+20,14,C.dim,'center','normal');","  txt('space or esc to resume  ·  m mutes',W/2,H/2+20,14,C.dim,'center','normal');\n  button(W/2-170,H/2+54,164,40,'THE MAP',()=>openPage('map'),'#8fd0ee',12);\n  button(W/2+6,H/2+54,164,40,'ACHIEVEMENTS',()=>openPage('ach'),C.gold,11);")
open(f,'w').write(s); print('ok')
