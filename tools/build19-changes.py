SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/index.html"
s=open(f).read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b,1)
rep("build 18 (pixel art, workbench, map, achievements, transport, town hub)","build 19 (pixel art; title screen, save slots, ESC menu)")
rep("/* ================================================================\n   WALKTHROUGHS",open(SP+"/menu.js").read()+"\n/* ================================================================\n   WALKTHROUGHS")
rep("  scene:'menu', t:0, sceneT:0,","  scene:'title', t:0, sceneT:0,")
rep("    gn.gain.exponentialRampToValueAtTime(vol||0.07,t+0.012);","    gn.gain.exponentialRampToValueAtTime((vol||0.07)*(this.vol||1),t+0.012);")
rep("function shake(a){ S.shake=Math.max(S.shake,a); }","function shake(a){ if(typeof OPT!=='undefined'&&!OPT.shake) return; S.shake=Math.max(S.shake,a); }")
rep("  S.fresh=true; S.scene='hub'; S.sceneT=0;          /* day 1 starts from the town page like every other */","  S.fresh=false; S.esc=false; S.paused=false;       /* a new run goes straight into day 1 (see beginRun) */")
rep("  if(S.day===1&&!TUT.done.basics) startLesson('basics');\n  else if(S.day===BULK_DAY&&!TUT.done.bulk) startLesson('bulk');","  if(!OPT.tutorials){ TUT.done.basics=true; TUT.done.bulk=true; }\n  if(S.day===1&&!TUT.done.basics) startLesson('basics');\n  else if(S.day===BULK_DAY&&!TUT.done.bulk) startLesson('bulk');")
rep("  if(!WT.done){\n    WT.on=true;","  if(!WT.done&&OPT.tutorials){\n    WT.on=true;")
rep("function toHub(){ S.scene='hub'; S.sceneT=0; }","function toHub(){ S.scene='hub'; S.sceneT=0; saveGame(); }          /* every arrival in town is a save */")
rep("function afterPaper(){ S.scene=(S.day%5===0&&S.history.length)?'ledger':'hub'; S.sceneT=0; }","function afterPaper(){ if(S.day%5===0&&S.history.length){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub(); }")
# the how-to card: OK only
i=s.index("  button(W/2-160,y+h-136,154,38,'THE MAP'"); j=s.index("  txt('best so far: day '")
s=s[:i]+"  button(W/2-160,y+h-96,320,58,'OK',()=>beginRun(),C.gold,22);\n"+s[j:]
rep("  if(S.scene==='menu') drawMenu();","  if(S.scene==='title') drawTitle();\n  else if(S.scene==='slots') drawSlots();\n  else if(S.scene==='howto') drawMenu();\n  else if(S.scene==='options') drawOptions();\n  else if(S.scene==='settings') drawSettings();\n  else if(S.scene==='bye') drawBye();")
rep("  else if(S.scene==='play'&&S.paused) drawPaused();\n  if(S.scene!=='menu'&&S.scene!=='gameover'&&S.scene!=='ach'&&S.scene!=='map') drawHUD();\n  drawToasts(1/60);",
    "  if(['title','slots','howto','options','settings','bye','gameover','ach','map'].indexOf(S.scene)<0) drawHUD();\n  if(escOpen()) drawEscMenu();\n  drawToasts(1/60);")
rep("  if(ev.key==='m'||ev.key==='M') Snd.on=!Snd.on;\n  if(ev.key==='Escape'||ev.key===' '){ if(S.scene==='play'){ S.paused=!S.paused; ev.preventDefault(); } }",
    "  if(ev.key==='m'||ev.key==='M'){ OPT.sound=!OPT.sound; optSave(); }\n  if(ev.key==='Escape'&&(S.scene==='options'||S.scene==='settings')){ closePage(); ev.preventDefault(); return; }\n  if(ev.key==='Escape'&&S.scene==='slots'){ S.slotArm=0; S.scene=S.backScene||'title'; ev.preventDefault(); return; }\n  if(ev.key==='Escape'&&S.scene==='hub'){ S.esc=!S.esc; ev.preventDefault(); return; }\n  if(ev.key==='Escape'||ev.key===' '){ if(S.scene==='play'){ S.paused=!S.paused; ev.preventDefault(); } }")
rep("  if(S.deadReason) button(W/2-120,y+h-70,240,50,'THAT IS THAT',()=>{S.scene='gameover';S.sceneT=0;},C.red,16);" if "  if(S.deadReason) button(W/2-120" in s else "  else if(S.deadReason) button(W/2-120,y+h-70,240,50,'THAT IS THAT',()=>{S.scene='gameover';S.sceneT=0;},C.red,16);",
    "  else if(S.deadReason) button(W/2-120,y+h-70,240,50,'THAT IS THAT',()=>{ slotErase(S.slot); S.scene='gameover';S.sceneT=0;},C.red,16);")
rep("  button(W/2-130,y+h-78,260,50,'TRY AGAIN',()=>startRun(),C.gold,17);","  button(W/2-270,y+h-78,260,50,'TRY AGAIN',()=>{ const n=S.slot; startRun(); S.slot=n; S.scene='play'; },C.gold,17);\n  button(W/2+10,y+h-78,260,50,'MAIN MENU',()=>toTitle(),C.dim,15);")
open(f,'w').write(s); print('ok')
