SP="/private/tmp/claude-501/-Users-volodymyrk-Documents-AI-Content-System/a701e449-2e9f-43fb-8246-20623e9b794c/scratchpad"
D="/Users/volodymyrk/Documents/AI Content System/wasteland-trader/"
def patch(path, reps):
    s=open(path).read()
    for a,b in reps:
        assert a in s, (path[-20:], a[:60])
        s=s.replace(a,b,1)
    open(path,'w').write(s)
MOD=[
 ("{n:'EPIC',     m:5,   col:","{n:'EPIC',     m:6,   col:"),("{n:'LEGENDARY',m:12,  col:","{n:'LEGENDARY',m:16,  col:"),
 ("n:'Fine Parts',c:1000, day:5","n:'Fine Parts',c:144, unlock:1000, day:5"),("n:'Relic Core',c:2000,day:10","n:'Relic Core',c:384, unlock:2000,day:10"),
 ("""function rar(item,r){
  const b=item.base||item; if(!r) return b;
  const k=b.id+r;
  if(!VARIANT[k]) VARIANT[k]=Object.assign({},b,{r:r,base:b,v:Math.round(b.v*RAR[r].m)});
  return VARIANT[k];
}""","""/* rarity and "made at the bench" are variants of the same item id, so every drag / sell / want path is untouched.
   Hand-made goods are worth CRAFT.mult times a caravan piece of the same tier. */
function rar(item,r,crafted){
  const b=item.base||item; r=r||0;
  if(crafted===undefined) crafted=!!item.crafted;
  if(!r&&!crafted) return b;
  const k=b.id+r+(crafted?'c':'');
  if(!VARIANT[k]) VARIANT[k]=Object.assign({},b,{r:r,base:b,crafted:crafted,v:Math.round(b.v*RAR[r].m*(crafted?CRAFT.mult:1))});
  return VARIANT[k];
}
/* the barrel pays for the object, not for the craftsmanship - or scrapping fresh work would turn a profit */
function scrapValue(item){ return Math.max(1,Math.round((item.base||item).v*RAR[item.r||0].m*0.25)); }
function unlockMat(m){
  if(S.unl[m.id]||S.caps<m.unlock){ Snd.bad(); return; }
  S.caps-=m.unlock; S.unl[m.id]=true; S.cr.spent+=m.unlock; Snd.coin(6); flash(m.pal.a,0.2);
}"""),
 ("  S.cr={spent:0,","  S.unl={fine:false,relic:false};\n  S.cr={spent:0,"),
 ("  if(m.day&&craftDay()<m.day) return;\n  const cost=m.c*n;","  if((m.day&&craftDay()<m.day)||(m.unlock&&!S.unl[m.id])) return;\n  const cost=m.c*n;"),
 ("  for(let k=0;k<n;k++){ const free=S.tray.indexOf(null); S.tray[free]=it;","  for(let k=0;k<n;k++){ const free=S.tray.indexOf(null); S.tray[free]=rar(it,0,true);"),
 ("  if(craftDay()<RAR[r].day) return 'day';\n  return billMissing","  if(craftDay()<RAR[r].day) return 'day';\n  { const ub=upgradeBill(item); for(const k in ub) if(MATBY[k].unlock&&!S.unl[k]) return 'lock'; }\n  return billMissing"),
 ("  if(!item||!item.r) return;\n  const c=RAR[item.r].col, k=inset||2;\n  g.fillStyle=rgba(c,0.16);","  if(!item||(!item.r&&!item.crafted)) return;\n  const c=item.r?RAR[item.r].col:'#c9a978', k=inset||2;\n  if(item.crafted){ g.fillStyle=c; g.fillRect(q.x+q.w-k-9,q.y+q.h-k-4,7,2); g.fillRect(q.x+q.w-k-4,q.y+q.h-k-9,2,7); }   /* maker's notch */\n  g.fillStyle=rgba(c,item.r?0.16:0.07);"),
 ("    txt(m.c+'c each',mk.x+60,y+38,10,C.dim,'left','normal');","    if(m.unlock&&!S.unl[m.id]){\n      txt('pay once: '+m.unlock+'c',mk.x+60,y+38,10,C.dim,'left','normal');\n      button(mk.x+178,y+12,96,32,'UNLOCK',()=>unlockMat(m),S.caps>=m.unlock?C.gold:C.dimmer,11); return; }\n    txt(m.c+'c each',mk.x+60,y+38,10,C.dim,'left','normal');"),
 ("    txt('sells about '+Math.round(it.v*0.5)+'c each',","    txt('sells about '+Math.round(it.v*0.5*CRAFT.mult)+'c each',"),
 ("    else button(wb.x+14,a.y+a.h+10,wb.w-28,32,st==='ok'?","    else if(st==='lock') txt('UNLOCK '+(S.unl.fine?'RELIC CORE':'FINE PARTS')+' AT THE MARKET FIRST',wb.x+wb.w/2,a.y+a.h+26,11,C.gold,'center');\n    else button(wb.x+14,a.y+a.h+10,wb.w-28,32,st==='ok'?"),
 ("    const nm=(S.wd.item.r?RAR[S.wd.item.r].n+' ':'')+S.wd.item.n+'  '+S.wd.item.v,","    const nm=(S.wd.item.crafted?'HAND-MADE ':'')+(S.wd.item.r?RAR[S.wd.item.r].n+' ':'')+S.wd.item.n+'  '+S.wd.item.v,"),
]
SHARED=[   # lines that live in the base game, identical in both builds
 ("  const it=entry.item, v=(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m;","  const it=entry.item, v=(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m*(it.crafted?CRAFT.mult:1);"),
 ("    let v=0; d.bundle.forEach(b=> v+=Math.max(1,Math.round(b.item.v*0.25)));","    let v=0; d.bundle.forEach(b=> v+=scrapValue(b.item));"),
 ("    const v=Math.max(1,Math.round(d.item.v*0.25));","    const v=scrapValue(d.item);"),
 ("    const v=Math.max(1,Math.round(B.drag.item.v*0.25));","    const v=scrapValue(B.drag.item);"),
 ("    else { S.caps+=Math.max(1,Math.round(B.drag.item.v*0.25)); B.scrapped++; }","    else { S.caps+=scrapValue(B.drag.item); B.scrapped++; }"),
 ("((d.item.r?RAR[d.item.r].n+' ':'')+d.item.n+' ('+d.item.v+'c)');","((d.item.crafted?'HAND-MADE ':'')+(d.item.r?RAR[d.item.r].n+' ':'')+d.item.n+' ('+d.item.v+'c)');"),
]
patch(SP+"/craft2.js", MOD)
patch(D+"index.html", MOD+SHARED+[
 ("const CRAFT={demo:false, price:1000};","const CRAFT={demo:false, price:1000, mult:8};"),
 ("function scrapValue(item){ return Math.max(1,Math.round(item.v*0.25)); }\n",""),
 ("RUST & RATIONS  -  build 13 (pixel art, workbench)","RUST & RATIONS  -  build 14 (pixel art, workbench)"),
])
# the demo generator: config + the shared edits, expressed against the text pc2 itself produces
s=open(SP+"/pc2.py").read()
s=s.replace('"{demo:true}" if demo else "{demo:false, price:1000}"','"{demo:true, mult:8}" if demo else "{demo:false, price:1000, mult:8}"')
hook="if demo:\n    rep(\"<title>"
assert hook in s
extra="for _a,_b in SHARED14:\n    rep(_a,_b)\n"
s=s.replace(hook, extra+hook,1)
s=s.replace("mode=sys.argv[1]","SHARED14="+repr([list(p) for p in SHARED])+"\nmode=sys.argv[1]",1)
s=s.replace("(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m;\\n  return","(it.base||it).v*RAR[Math.min(it.r||0,purseR(cust))].m;\\n  return")   # unchanged: SHARED14 rewrites it afterwards
open(SP+"/pc2.py","w").write(s)
print("ok")
