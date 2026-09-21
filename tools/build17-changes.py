SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/index.html"
s=open(f).read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b,1)
rep("build 16 (pixel art, workbench, map, achievements, transport)","build 17 (pixel art, workbench, map, achievements, transport, town hub)")
i=s.index("function drawShop(){"); j=s.index("function drawLookPreview(")
s=s[:i]+open(SP+"/hub.js").read()+s[j:]
# key caps: big and on the left, in the Fixer cards...
rep("  if(keyTag){ plate(cx+cw-24,cy+6,18,16,'#2a2012',col); txt(keyTag,cx+cw-15,cy+14,10,col,'center'); }",
    "  if(keyTag){ plate(cx+7,cy+42,30,26,'#0d0a08',col); txt(keyTag,cx+22,cy+55,15,col,'center'); txt('KEY',cx+22,cy+76,7,C.dimmer,'center'); }")
rep("  for(let k=0;k<max;k++){ g.fillStyle=k<lvl?col:'#3a3228'; g.fillRect(cx+10,cy+42+k*8,8,5); }",
    "  for(let k=0;k<max;k++){ g.fillStyle=k<lvl?col:'#3a3228'; if(keyTag) g.fillRect(cx+cw-16-k*10,cy+8,7,5); else g.fillRect(cx+10,cy+42+k*8,8,5); }")
# ...and on the rail during the day
rep("    blit(perkIcon(a.id,ready?a.col:'#6b5a45'),r.x+10,r.y+10,3);\n    plate(r.x+r.w-22,r.y+3,19,15,'#2a2012',a.col);\n    txt(a.key,r.x+r.w-12,r.y+10,10,a.col,'center');",
    "    plate(r.x+4,r.y+9,24,26,'#0d0a08',ready?a.col:'#6b5a45');\n    txt(a.key,r.x+16,r.y+22,15,ready?a.col:'#8a7a62','center');\n    blit(perkIcon(a.id,ready?a.col:'#6b5a45'),r.x+33,r.y+10,3);")
assert s.count("r.x+r.w-12,r.y+r.h-13")==3
s=s.replace("r.x+r.w-12,r.y+r.h-13","r.x+r.w-25,r.y+r.h/2")
rep("'OPEN TOMORROW · DAY '+(S.day+1),()=>{dropTries();S.editName=false;nextDay();},C.gold,13);","'OPEN THE STALL · DAY '+(S.fresh?S.day:S.day+1),()=>{dropTries();S.editName=false;hubOpenDay();},C.gold,12);")
# every road leads back to town
rep("               else { S.scene='shop'; S.sceneT=0; } },","               else toHub(); },")
rep("CRAFT.demo?(has?'OPEN THE STALL':'OPEN WITH NOTHING TO SELL'):'BACK TO THE FIXER',","CRAFT.demo?(has?'OPEN THE STALL':'OPEN WITH NOTHING TO SELL'):'BACK TO TOWN',")
rep("  button(px0+pw-150,py0+18,120,38,'BACK',()=>{S.scene='shop';S.sceneT=0;},C.gold,13);","  button(px0+pw-150,py0+18,120,38,'BACK',()=>toHub(),C.gold,13);")
rep("  if(ev.key==='Escape'&&S.scene==='transport'){ S.scene='shop'; ev.preventDefault(); return; }","  if(ev.key==='Escape'&&(S.scene==='transport'||S.scene==='shop'||S.scene==='ledger')){ toHub(); ev.preventDefault(); return; }")
rep("'BACK TO THE FIXER',()=>{dropTries();S.editName=false;S.scene='shop';},C.dim,12);","'BACK TO TOWN',()=>{dropTries();S.editName=false;toHub();},C.dim,12);")
rep("'CLOSE THE BOOKS',()=>{S.scene='shop';},C.gold,14);","'CLOSE THE BOOKS',()=>toHub(),C.gold,14);")
rep("function afterPaper(){ S.scene=(S.day%5===0&&S.history.length)?'ledger':'shop'; S.sceneT=0; }","function afterPaper(){ S.scene=(S.day%5===0&&S.history.length)?'ledger':'hub'; S.sceneT=0; }")
rep("  else if(S.scene==='shop') drawShop();","  else if(S.scene==='hub') drawHub();\n  else if(S.scene==='shop') drawShop();")
rep("    txt(S.scene==='shop'?'THE FIXER':","    txt(S.scene==='hub'?'DUSTWELL':S.scene==='shop'?'THE FIXER':")
# a run now opens on the town page too
rep("  S.shelves=[]; makeShelves(); startDay();\n}","  S.shelves=[]; makeShelves(); startDay();\n  S.fresh=true; S.scene='hub'; S.sceneT=0;          /* day 1 starts from the town page like every other */\n}")
open(f,'w').write(s); print('ok')
