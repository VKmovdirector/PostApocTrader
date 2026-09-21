SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/index.html"
s=open(f).read()
def rep(a,b,cnt=1):
    global s
    assert a in s, a[:70]
    s=s.replace(a,b) if cnt==0 else s.replace(a,b,cnt)
rep("build 15 (pixel art, workbench, map, achievements)","build 16 (pixel art, workbench, map, achievements, transport)")
# 1 difficulty flat from day 10, random crate size
rep("const custEvery  = d => d===1? 7.0 : Math.max(2.7, 6.6-0.34*(d-1));","const custEvery  = d => d===1? 7.0 : Math.max(3.54, 6.6-0.34*(d-1));   /* flat from day 10 */")
rep("const crateEvery = d => Math.max(7.5, 14-0.6*(d-1));","const crateEvery = d => Math.max(8.6, 14-0.6*(d-1));                  /* flat from day 10 */")
rep("const crateSize  = d => Math.min(6, 3+Math.floor((d-1)/3));","const crateSize  = d => Math.min(6, 3+Math.floor((d-1)/3));            /* the most a crate can hold that day; each one rolls 3..this */")
rep("  const n=crateSize(S.day), items=[];","  const n=ri(3,crateSize(S.day)), items=[];")
rep("  txt('caravan every '+Math.round(crateEvery(S.day))+'s  ·  customer every '","  txt('caravan every '+Math.round(crateEvery(S.day))+'s, '+(crateSize(S.day)>3?'3-'+crateSize(S.day):'3')+' a crate  ·  customer every '")
# 2 sign
rep("{id:'sign',  n:'PAINTED SIGN',   d:'+15% on every sale',            max:3, cost:[155,245,350]},","{id:'sign',  n:'PAINTED SIGN',   d:'+5% on every sale per level',   max:3, cost:[150,400,800]},")
rep("sign:1+0.15*S.up.sign,","sign:1+0.05*S.up.sign,")
# 3 signal fire
rep("  why:'for when you need a second pair of hands'}\n];","  why:'for when you need a second pair of hands'},\n {key:6,id:'signal',n:'SIGNAL FIRE',    cd:60, cost:800, col:'#f08a4a',\n  d:'light the beacon: caravans hurry in 10% faster for 20s',\n  why:'for when the shelves are running dry'}\n];\nconst SIGNAL_BOOST=0.10, SIGNAL_TIME=20;")
rep("S.actOwn=[false,false,false,false,false];\nS.actCd=[0,0,0,0,0]; S.handT=0;","S.actOwn=[false,false,false,false,false,false];\nS.actCd=[0,0,0,0,0,0]; S.handT=0; S.signalT=0;")
rep("  S.actOwn=[false,false,false,false,false]; S.actCd=[0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0;","  S.actOwn=[false,false,false,false,false,false]; S.actCd=[0,0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0; S.signalT=0; S.rig={};")
rep("  S.actCd=[0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0;\n","  S.actCd=[0,0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0; S.signalT=0;\n")
rep("  for(let i=0;i<5;i++) if(S.actCd[i]>0)","  for(let i=0;i<6;i++) if(S.actCd[i]>0)")
rep("ev.key>='1'&&ev.key<='5'){","ev.key>='1'&&ev.key<='6'){")
rep("let TIP=null, RAILPOS=[null,null,null,null,null], RAILAY=252;","let TIP=null, RAILPOS=[null,null,null,null,null,null], RAILAY=252;")
rep("  TIP=null; RAILPOS=[null,null,null,null,null];","  TIP=null; RAILPOS=[null,null,null,null,null,null];")
rep("  txt('1-5',RAIL.x+RAIL.w-8,y-12,10,C.dimmer,'right');","  txt('1-6',RAIL.x+RAIL.w-8,y-12,10,C.dimmer,'right');")
rep("    S.nextCrate-=dt;\n","    S.nextCrate-=dt*(S.signalT>0?1+SIGNAL_BOOST:1);\n")
rep("  S.patterT=Math.max(0,S.patterT-dt);\n","  S.patterT=Math.max(0,S.patterT-dt);\n  if(S.scene==='play'&&!S.paused) S.signalT=Math.max(0,S.signalT-dt);\n")
rep("  } else if(a.id==='hire'){","  } else if(a.id==='signal'){\n    S.signalT=SIGNAL_TIME;\n  } else if(a.id==='hire'){")
rep("  } else if(S.steadyT>0){\n    plate(RAIL.x+6,sy,RAIL.w-12,26,'#1e2a18','#7fb74f');\n    txt('STEADY '+S.steadyT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#a8d98a','center');\n  }","  } else if(S.steadyT>0){\n    plate(RAIL.x+6,sy,RAIL.w-12,26,'#1e2a18','#7fb74f');\n    txt('STEADY '+S.steadyT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#a8d98a','center');\n  } else if(S.signalT>0){\n    plate(RAIL.x+6,sy,RAIL.w-12,26,'#33200f','#f08a4a');\n    txt('SIGNAL '+S.signalT.toFixed(1)+'s',RAIL.x+RAIL.w/2,sy+13,11,'#f8b888','center');\n  }")
rep(" back: ['kkkkkkkk',"," signal:['...k....','..kk....','..kkk.k.','.kkkkkk.','.kk.kkk.','.kk..kk.','..kkkk..','kkkkkkkk'],\n back: ['kkkkkkkk',")
rep("    if(a.id==='hire') return;                      /* sold from her own card above, it has levels */","    if(a.id==='hire'||a.id==='signal') return;     /* these two have their own cards in the grid above */")
rep("  txt('ACTIVE  ·  press the key',x+30,y+318,12,'#a173c8');","  { const si=ACTIVES.findIndex(q=>q.id==='signal'), a=ACTIVES[si], cx=x+30+2*(cw+gap), cy=y+100+(ch+gap), own=S.actOwn[si], afford=!own&&S.caps>=a.cost;\n    shopCard(cx,cy,cw,ch,a.id,a.col,a.n,a.d,own?1:0,1,own?null:a.cost,afford,\n      ()=>{ S.caps-=a.cost; S.actOwn[si]=true; Snd.coin(4); flash(a.col,0.2); AST.perks=n0('perks')+1; if(S.actOwn.every(Boolean)) AST.allActive=1; achCheck(); },''+a.key);\n    txt('ACTIVE · '+a.cd+'s rest',cx+10,cy+ch-12,9,C.dimmer,'left','normal'); }\n  txt('ACTIVE  ·  press the key',x+30,y+318,12,'#a173c8');")
rep("{id:'actives', n:'FIVE FINGERS',      d:'Own all five active perks in one run.',","{id:'actives', n:'EVERY TRICK',       d:'Own every active perk in one run.',    ")
# 4 transport
rep("/* ================================================================\n   WALKTHROUGHS",open(SP+"/rig.js").read()+"\n/* ================================================================\n   WALKTHROUGHS")
rep("""  button(x+30,y+h-58,196,44,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,11);
  button(x+236,y+h-58,150,44,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,11);""","""  button(x+30,y+h-58,168,44,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,10);
  button(x+206,y+h-58,120,44,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,10);
  button(x+548,y+h-58,160,44,'TRANSPORT '+rigCount()+'/'+RIG.length,()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',10);""")
rep("  button(x+396,y+h-58,250,44,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>{","  button(x+334,y+h-58,206,44,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>{")
rep("    },canWb?'#8fd0ee':C.dimmer,11);\n  if(!S.wb&&inRect(MX,MY,{x:x+396,y:y+h-58,w:250,h:44})){","    },canWb?'#8fd0ee':C.dimmer,10);\n  if(!S.wb&&inRect(MX,MY,{x:x+334,y:y+h-58,w:206,h:44})){")
rep("  button(x+656,y+h-58,254,44,'TOMORROW · DAY '+(S.day+1),()=>nextDay(),C.gold,13);","  button(x+716,y+h-58,194,44,'TOMORROW · DAY '+(S.day+1),()=>nextDay(),C.gold,10);")
rep("  else if(S.scene==='map') drawMap();","  else if(S.scene==='map') drawMap();\n  else if(S.scene==='transport') drawTransport();")
rep("S.scene==='workshop'?'THE WORKBENCH':","S.scene==='workshop'?'THE WORKBENCH':S.scene==='transport'?'THE YARD':")
rep("  if(ev.key==='Escape'&&(S.scene==='map'||S.scene==='ach')){ closePage(); ev.preventDefault(); return; }","  if(ev.key==='Escape'&&(S.scene==='map'||S.scene==='ach')){ closePage(); ev.preventDefault(); return; }\n  if(ev.key==='Escape'&&S.scene==='transport'){ S.scene='shop'; ev.preventDefault(); return; }")
# map: strider progress, and the first leg lights up when she can walk
rep("  txt('N',100,52,12,'#2a1f14','center');","  txt('N',100,52,12,'#2a1f14','center');\n  { const rc=(S.rig?rigCount():0), ok=S.rig&&rigDone(); plate(W-330,20,166,40,'#1a1410',ok?C.gold:'#5c4a37'); txt('STRIDER '+rc+'/'+RIG.length,W-247,40,12,ok?C.gold:C.dim,'center');\n    if(ok&&Math.sin(S.t*5)>-0.3){ const a=TOWNS[0], b=TOWNS[1]; g.strokeStyle=C.gold; g.lineWidth=4; g.setLineDash([14,10]); g.beginPath(); g.moveTo(a.x*4,a.y*4); g.lineTo(b.x*4,b.y*4); g.stroke(); g.setLineDash([]); } }")
rep("  txt(tn.home?'YOU ARE HERE':'THE ROAD IS NOT OPEN YET',bx+bw-16,by+22,10,tn.home?C.green:C.dimmer,'right');","  { const reach=!tn.home&&tn.id==='saltpan'&&S.rig&&rigDone();\n    txt(tn.home?'YOU ARE HERE':(reach?'THE STRIDER CAN REACH IT · LATER BUILD':'THE ROAD IS NOT OPEN YET'),bx+bw-16,by+22,10,tn.home?C.green:(reach?C.gold:C.dimmer),'right'); }")
open(f,'w').write(s); print('ok')
