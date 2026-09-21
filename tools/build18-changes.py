f="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/index.html"
s=open(f).read()
def rep(a,b):
    global s
    assert a in s, a[:70]; s=s.replace(a,b,1)
rep("build 17 (pixel art, workbench, map, achievements, transport, town hub)","build 18 (pixel art, workbench, map, achievements, transport, town hub)")
# ---------------- key caps
rep("function shopCard(","""/* A keyboard key, seen a little from above. state: 'ready' | 'rest' | 'off';  down = pressed this instant */
function keycap(x,y,w,h,label,col,state,down){
  x=Math.round(x); y=Math.round(y);
  const live=state==='ready', top=live?'#ddd2ba':(state==='rest'?'#8f8776':'#5e584d'),
        hi=live?'#f6eed8':(state==='rest'?'#a59c89':'#6e675b'), side=live?'#9c9078':(state==='rest'?'#5f594c':'#403c34'),
        ink=live?'#1a1410':(state==='rest'?'#2e2a23':'#2a2722'), lift=down?0:3;
  g.fillStyle='#0a0806'; g.fillRect(x,y+2,w,h);                                  /* shadow / base */
  g.fillStyle='#2a251d'; g.fillRect(x+1,y+1,w-2,h);                              /* outline */
  g.fillStyle=side; g.fillRect(x+2,y+2,w-4,h-2);                                 /* side wall */
  const tx=x+3, ty=y+2+(3-lift), tw=w-6, th=h-7;                                 /* raised top face */
  g.fillStyle=top; g.fillRect(tx,ty,tw,th);
  g.fillStyle=hi;  g.fillRect(tx,ty,tw,1); g.fillRect(tx,ty,1,th);
  g.fillStyle=side; g.fillRect(tx,ty+th-1,tw,1); g.fillRect(tx+tw-1,ty,1,th);
  g.fillStyle='#2a251d'; g.fillRect(tx,ty,1,1); g.fillRect(tx+tw-1,ty,1,1); g.fillRect(tx,ty+th-1,1,1); g.fillRect(tx+tw-1,ty+th-1,1,1);   /* rounded corners */
  txt(label,tx+tw/2,ty+th/2-1,Math.round(h*0.5),ink,'center');
  g.fillStyle=live?col:side; g.fillRect(tx+4,ty+th-4,tw-8,2);                     /* the perk's colour, like a painted legend */
}
function shopCard(""")
rep("  if(keyTag){ plate(cx+7,cy+42,30,26,'#0d0a08',col); txt(keyTag,cx+22,cy+55,15,col,'center'); txt('KEY',cx+22,cy+76,7,C.dimmer,'center'); }",
    "  if(keyTag){ keycap(cx+6,cy+40,32,30,keyTag,col,(lvl>0||afford)?'ready':'off',false); txt('KEY',cx+22,cy+78,7,C.dimmer,'center'); }")
rep("    plate(r.x+4,r.y+9,24,26,'#0d0a08',ready?a.col:'#6b5a45');\n    txt(a.key,r.x+16,r.y+22,15,ready?a.col:'#8a7a62','center');",
    "    keycap(r.x+3,r.y+8,27,28,''+a.key,a.col,ready?'ready':'rest',(S.keyFx&&S.keyFx[i]>0));")
rep("  S.actCd[i]=a.cd; achInc('actUsed');","  S.actCd[i]=a.cd; achInc('actUsed'); (S.keyFx=S.keyFx||[])[i]=0.16;")
rep("  S.patterT=Math.max(0,S.patterT-dt);\n","  S.patterT=Math.max(0,S.patterT-dt);\n  if(S.keyFx) for(let k=0;k<S.keyFx.length;k++) if(S.keyFx[k]>0) S.keyFx[k]-=dt;\n")
# ---------------- caravans: single file, one BIG one at half-time
rep("""function spawnCrate(){
  const n=ri(3,crateSize(S.day)), items=[];""","""/* Only ever one caravan in the yard. big = the half-time load: a double roll in a bigger crate. */
function spawnCrate(big){
  const n=big ? ri(3,crateSize(S.day))*2 : ri(3,crateSize(S.day)), items=[];""")
rep("  S.crates.push({x:-150,y:cb.y-4,t:0,items:items,state:'in'});","  S.crates.push({x:-170,y:cb.y-(big?14:4),t:0,items:items,state:'in',big:!!big,n:n});")
rep("    if(S.nextCrate<=0){ S.nextCrate=crateEvery(S.day); spawnCrate(); }","    if(S.nextCrate<=0){ S.nextCrate=crateEvery(S.day); S.crateDue=(S.crateDue||0)+1; }     /* due - but it waits its turn */")
rep("    spawnCrate(); spawnCrate();\n    S.banner={text:'CARAVAN ROLLS IN',sub:'two crates and a crowd',t:0,dur:3.2};","    S.bigDue=true;\n    S.banner={text:'BIG CARAVAN',sub:'a full load and a crowd',t:0,dur:3.2};")
rep("  for(let i=S.crates.length-1;i>=0;i--){\n    const cr=S.crates[i]; cr.t+=dt;","  if(!S.crates.length&&!S.closing&&!tutFrozen()){\n    if(S.bigDue){ S.bigDue=false; spawnCrate(true); }\n    else if(S.crateDue>0){ S.crateDue--; spawnCrate(false); }\n  }\n  for(let i=S.crates.length-1;i>=0;i--){\n    const cr=S.crates[i]; cr.t+=dt;")
rep("  S.nextCrate=1.4; S.nextCust=","  S.crateDue=0; S.bigDue=false; S.keyFx=[];\n  S.nextCrate=1.4; S.nextCust=")
rep("""    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(x-2,y+42,60,5);
    g.fillStyle=C.wood; g.fillRect(x,y,56,42);
    g.fillStyle=C.woodHi; g.fillRect(x,y,56,4); g.fillStyle=C.woodDk; g.fillRect(x,y+20,56,4);
    g.fillStyle='#2a1f14'; g.fillRect(x,y+38,56,4);
    txt('CARAVAN',x+28,y+31,11,'#c9b48f','center');""","""    const cw2=cr.big?84:56, ch2=cr.big?52:42;
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(x-2,y+ch2,cw2+4,5);
    g.fillStyle=C.wood; g.fillRect(x,y,cw2,ch2);
    g.fillStyle=C.woodHi; g.fillRect(x,y,cw2,4); g.fillStyle=cr.big?C.gold:C.woodDk; g.fillRect(x,y+Math.round(ch2*0.48),cw2,4);
    g.fillStyle='#2a1f14'; g.fillRect(x,y+ch2-4,cw2,4);
    if(cr.big){ g.fillStyle=C.gold; g.fillRect(x,y,3,ch2); g.fillRect(x+cw2-3,y,3,ch2); }
    txt(cr.big?'BIG CARAVAN':'CARAVAN',x+cw2/2,y+(cr.big?14:12),cr.big?10:9,cr.big?'#f6d874':'#c9b48f','center');
    txt('x'+cr.items.length,x+cw2/2,y+ch2-13,cr.big?16:13,'#efe3cb','center');       /* how much is still aboard */""")
rep("  txt(S.closing?'closed':'in '+Math.ceil(tleft)+'s',hr.x+hr.w-12,hr.y+15,11,C.dimmer,'right','normal');","  txt(S.closing?'closed':(S.crates.length?'unloading...':((S.crateDue>0||S.bigDue)?'at the gate':'in '+Math.ceil(tleft)+'s')),hr.x+hr.w-12,hr.y+15,11,S.crates.length?C.gold:C.dimmer,'right','normal');")
open(f,'w').write(s); print('ok')
