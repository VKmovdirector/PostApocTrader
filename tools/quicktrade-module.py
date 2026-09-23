#!/usr/bin/env python3
"""Quick Trade demo: index.html + a 7th active, QUICK TRADE (key 7): swap one plain piece for any other, paying the difference.
Own saves (rustrations.qt.*), the skill owned from the start, 600c to begin."""
import sys
SRC='index.html'; DST='quicktrade-demo.html'
src=open(SRC).read(); n=0
def rep(a,b,count=1):
    global src,n
    if src.count(a)!=count: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("<title>Rust &amp; Rations</title>","<title>Rust &amp; Rations - quick trade demo</title>")
rep("  txt('build 26',W-20,H-18,10,C.dimmer,'right','normal');","  txt('QUICK TRADE DEMO · key 7 is yours from the start · 600c',W-20,H-18,10,'#e0d060','right','normal');")
rep("function slotKey(n){ return 'rustrations.slot'+n; }","function slotKey(n){ return 'rustrations.qt.slot'+n; }")
rep("  why:'for when the shelves are running dry'}\n];",
    "  why:'for when the shelves are running dry'},\n"
    " {key:7,id:'swap',  n:'QUICK TRADE',    cd:45, cost:900, col:'#e0d060',\n"
    "  d:'swap one plain piece on a shelf or the counter for any other, paying the difference in price',\n"
    "  why:'for when a buyer wants what you do not have'}\n];")
rep(" signal:['...k....','..kk....','..kkk.k.','.kkkkkk.','.kk.kkk.','.kk..kk.','..kkkk..','kkkkkkkk'],",
    " signal:['...k....','..kk....','..kkk.k.','.kkkkkk.','.kk.kkk.','.kk..kk.','..kkkk..','kkkkkkkk'],\n"
    " swap:  ['..k.....','.kkkkkk.','k.k....k','.kk....k','.......k','k....kk.','k....k.k','.kkkkkk.'],")
rep("  const a=ACTIVES[i];\n  S.actCd[i]=a.cd; achInc('actUsed');",
    "  const a=ACTIVES[i];\n"
    "  if(a.id==='swap'){ S.qt={phase:'pick'}; Snd.ui(); say('What should it be instead?'); return; }   /* the cooldown starts when the swap is made */\n"
    "  S.actCd[i]=a.cd; achInc('actUsed');")
rep("  S.actOwn=ACTIVES.map(()=>false); S.actCd=ACTIVES.map(()=>0); S.steadyT=0;",
    "  S.actOwn=ACTIVES.map(()=>false); S.actOwn[ACTIVES.length-1]=true; S.actCd=ACTIVES.map(()=>0); S.steadyT=0;")
rep("  S.day=1; S.caps=40;","  S.day=1; S.caps=600;")
rep("  S.crateDue=0; S.bigDue=false; S.crateRest=0; S.keyFx=[];","  S.crateDue=0; S.bigDue=false; S.crateRest=0; S.keyFx=[]; S.qt=null;")
rep("  if(S.scene!=='play'||S.paused) return;\n","  if(S.scene!=='play'||S.paused||S.qt) return;                      /* the day waits while a quick trade is chosen */\n")
rep("    if(lessonClick()) return;","    if(S.qt){ qtClick(p.x,p.y); return; }\n    if(lessonClick()) return;")
rep("window.addEventListener('keydown',ev=>{\n","window.addEventListener('keydown',ev=>{\n  if(S.qt&&ev.key==='Escape'){ S.qt=null; Snd.drop(); ev.preventDefault(); return; }\n")
rep("drawPerkRail(); drawEffects(); drawBanner(); drawDrag(); drawBot(); drawLesson(); drawPerkTip();",
    "drawPerkRail(); drawEffects(); drawBanner(); drawDrag(); drawBot(); drawLesson(); drawPerkTip(); drawQuickTrade();")
rep("/* ---------- the name screen: after the intro, before the how-to card ---------- */",
    r"""/* ================================================================
   QUICK TRADE (demo)  -  key 7: point at a plain piece, pick what it should be, pay the difference
   ================================================================ */
function qtPlain(it){ return !!it&&!(it.r||0)&&!it.crafted; }
function qtClick(x,y){
  if(S.qt.phase==='pick'){
    const ss=shelfSlotUnder(x,y);
    if(ss){ const e=S.shelves[ss.i].slots[ss.j]; if(e&&!e.arriving&&qtPlain(e.item)){ S.qt={phase:'choose',src:{k:'shelf',i:ss.i,j:ss.j,item:e.item}}; Snd.ui(); return; } }
    const cj=counterSlotUnder(x,y);
    if(cj>=0){ const e=S.counter[cj]; if(e&&!e.arriving&&qtPlain(e.item)){ S.qt={phase:'choose',src:{k:'counter',i:cj,item:e.item}}; Snd.ui(); return; } }
    S.qt=null; Snd.drop(); return;                                    /* nothing usable under the click: cancelled */
  }
  S.qt=null; Snd.drop();                                              /* a click off the board cancels */
}
function qtSwap(target){
  const s=S.qt.src, cost=Math.max(0,target.v-s.item.v);
  if(S.caps<cost){ Snd.bad(); flash(C.red,0.2); return; }
  S.caps-=cost; let q;
  if(s.k==='shelf'){ const sh=S.shelves[s.i]; sh.slots[s.j]={item:target,misfiled:sh.cat!==target.cat,arriving:0,anim:1}; q=shelfSlotRect(s.i,s.j); }
  else { S.counter[s.i]={item:target,arriving:0,anim:1,misfiled:false}; q=counterSlotRect(s.i); }
  burst(q.x+q.w/2,q.y+q.h/2,'#e0d060',16,180); float(q.x+q.w/2,q.y-2,cost?('-'+cost+'c'):'EVEN SWAP',cost?C.red:C.green,14);
  const i=ACTIVES.findIndex(a=>a.id==='swap'); S.actCd[i]=ACTIVES[i].cd; (S.keyFx=S.keyFx||[])[i]=0.16; achInc('actUsed');
  S.qt=null; Snd.coin(3); flash('#e0d060',0.18);
}
function drawQuickTrade(){
  if(!S.qt) return;
  if(S.qt.phase==='pick'){
    S.shelves.forEach((sh,i)=>sh.slots.forEach((e,j)=>{ if(e&&!e.arriving&&qtPlain(e.item)) tutGlow(shelfSlotRect(i,j)); }));
    for(let j=0;j<S.cslots;j++){ const e=S.counter[j]; if(e&&!e.arriving&&qtPlain(e.item)) tutGlow(counterSlotRect(j)); }
    plate(W/2-280,LO.panelL.y-82,560,56,'#1d1712','#e0d060');
    txt('QUICK TRADE: CLICK THE PIECE YOU WANT TO SWAP',W/2,LO.panelL.y-62,14,'#e0d060','center');
    txt('plain pieces only - not rare, epic or hand-made  ·  esc cancels  ·  the day waits',W/2,LO.panelL.y-42,10,C.dim,'center','normal');
    return;
  }
  dim(0.6);
  const s=S.qt.src, w=1060, h=420, x=W/2-w/2, y=H/2-h/2;
  plate(x,y,w,h,'#1a1410','#e0d060','#8a6f50');
  txt('QUICK TRADE',x+24,y+30,22,'#e0d060');
  txt('swap '+s.item.n.toUpperCase()+' ('+s.item.v+'c) for any plain piece  ·  you pay the difference  ·  purse '+S.caps+'c',x+w-24,y+30,11,C.dim,'right','normal');
  const cats=activeCats(), cw=(w-48-(cats.length-1)*12)/cats.length;
  cats.forEach((c,ci)=>{
    const cx=x+24+ci*(cw+12);
    plate(cx,y+52,cw,h-96,'#211a14','#4a3b2c'); blit(catBadge(c),cx+8,y+60,2); txt(CATS[c].name,cx+30,y+68,13,CATS[c].col);
    BYCAT[c].forEach((it,k)=>{
      const ry=y+88+k*46, r={x:cx+6,y:ry,w:cw-12,h:42}, cost=Math.max(0,it.v-s.item.v), same=it.id===s.item.id, can=!same&&S.caps>=cost, hov=can&&inRect(MX,MY,r);
      plate(r.x,r.y,r.w,r.h,hov?'#33281c':'#191310',same?'#33291f':(can?CATS[c].col:'#5a3a30'));
      drawItem(it,r.x+22,r.y+21,2);
      txt(fitText(it.n,r.w-112,11),r.x+44,r.y+14,11,same?C.dimmer:C.ink);
      txt(it.v+'c',r.x+44,r.y+31,9,C.dim,'left','normal');
      txt(same?'YOURS':(cost?'-'+cost+'c':'FREE'),r.x+r.w-8,r.y+21,12,same?C.dimmer:(can?(cost?C.gold:C.green):C.red),'right');
      if(can) BTNS.push({x:r.x,y:r.y,w:r.w,h:r.h,fn:()=>qtSwap(it)});
    });
  });
  button(x+w-150,y+h-40,126,30,'CANCEL',()=>{ S.qt=null; Snd.drop(); },C.dim,12);
  txt('a cheaper piece is a free swap; the money is not refunded  ·  the day waits while you choose',x+24,y+h-25,10,C.dimmer,'left','normal');
}
/* ---------- the name screen: after the intro, before the how-to card ---------- */""")
open(DST,'w').write(src); print('demo written',n)
