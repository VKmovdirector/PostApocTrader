#!/usr/bin/env python3
"""Build 23: Herald a day earlier, lighter caravans, END DAY once the last buyer is in, STALL & LOOKS marker,
saved sign fix, intro -> name screen -> how-to flow, scavenger walker, shop card, per-event paper pictures,
and the picture reaching the window edges."""
import re, sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b,count=1):
    global src,n
    if src.count(a)!=count: print('ANCHOR FAIL (%d found, want %d):\n%s'%(src.count(a),count,a[:220])); sys.exit(1)
    src=src.replace(a,b); n+=1

rep("build 22: morning town page, intro, per-slot progress","build 23: name screen, last-call END DAY, paper pictures, edge-to-edge")
rep("  txt('build 22',W-20,H-18,10,C.dimmer,'right','normal');","  txt('build 23',W-20,H-18,10,C.dimmer,'right','normal');")

# ---------- 3. Herald printed at dusk of day 4, 8, 12 -> read on 5, 9, 13 ----------
rep("function paperDay(d){ return d>=5&&(d-5)%4===0; }          /* the Herald prints on day 5, 9, 13 ... */",
    "function paperDay(d){ return d>=4&&(d-4)%4===0; }          /* printed at dusk of day 4, 8, 12: read, and in force, on the morning of 5, 9, 13 */")
rep("   EVENTS  -  every issue of the Herald (day 5, 9, 13 ...) prints one event; it moves",
    "   EVENTS  -  every issue of the Herald (read on day 5, 9, 13 ...) prints one event; it moves")

# ---------- 5. caravans carry 10-15% less from day 4 ----------
rep("const crateSize  = d => Math.min(6, 3+Math.floor((d-1)/3));            /* the most a crate can hold that day; each one rolls 3..this */",
    "const crateSize  = d => Math.min(6, 3+Math.floor((d-1)/3));            /* the most a crate can hold that day; each one rolls crateLo..this */\n"
    "const crateLo    = d => d<=3 ? 3 : 2;                                  /* build 23: from day 4 a crate can be as light as 2 (about 12% less stock) */")
rep("  const n=big ? ri(3,crateSize(S.day))*2 : ri(3,crateSize(S.day)), items=[];",
    "  const lo=crateLo(S.day), hi=crateSize(S.day), n=big ? ri(lo,hi)*2 : ri(lo,hi), items=[];")
rep("  txt('caravan every '+Math.round(crateEvery(S.day))+'s, '+(crateSize(S.day)>3?'3-'+crateSize(S.day):'3')+' a crate  ·  customer every '+custEvery(S.day).toFixed(1)+'s',",
    "  const clo=crateLo(S.day), chi=crateSize(S.day);\n"
    "  txt('caravan every '+Math.round(crateEvery(S.day))+'s, '+(chi>clo?clo+'-'+chi:''+clo)+' a crate  ·  customer every '+custEvery(S.day).toFixed(1)+'s',")

# ---------- 2. END DAY once the day's last buyer has walked in ----------
rep("/* the END DAY button only shows once the last two buyers of the day are on the road (or the day is closing) */\n"
    "function lastCall(){ return S.scene==='play'&&!S.shut&&!tutFrozen()&&(S.dayLen-S.dayTime)<=custEvery(S.day)*2; }",
    "/* the END DAY button only shows once the day's last buyer has actually walked in: nobody else can spawn\n"
    "   (the next timed arrival would land after closing, the rush is spent) and nobody is still on the road */\n"
    "function lastCall(){\n"
    "  if(S.scene!=='play'||S.shut||tutFrozen()) return false;\n"
    "  const noMore = S.closing || (S.rushQueue===0 && S.dayTime+S.nextCust>=S.dayLen);\n"
    "  return noMore && !S.custs.some(c=>c.state==='walk');\n"
    "}")
rep("'the last buyers are on the road'","'that was the last buyer today'")

# ---------- 1. STALL & LOOKS: marker and wording ----------
rep("  S.day++;\n  if(books){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub();",
    "  S.day++;\n  if(newLooksOn(S.day).length) S.looksFresh=true;             /* a NEW tab on STALL & LOOKS until it is opened */\n"
    "  if(books){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub();")
rep("  S.paperFresh=false; S.paperDay=0; S.event=null; S.evGain=0;\n",
    "  S.paperFresh=false; S.paperDay=0; S.event=null; S.evGain=0; S.looksFresh=false;\n")
rep("look:{look:S.worn,owned:S.owned},caps:S.caps,","look:{look:S.worn,owned:S.owned},looksFresh:!!S.looksFresh,caps:S.caps,")
rep("'maxCombo','cslots','rows'].forEach(k=>{ if(d[k]!==undefined) S[k]=d[k]; });",
    "'maxCombo','cslots','rows','looksFresh'].forEach(k=>{ if(d[k]!==undefined) S[k]=d[k]; });")
rep("  door(lx,by+(bh+gp)*3,bw,bh,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,13,'looks');",
    "  door(lx,by+(bh+gp)*3,bw,bh,'STALL & LOOKS',()=>{ S.looksFresh=false; S.scene='looks'; S.sceneT=0; },nl?C.purple:C.dim,13,'looks');\n"
    "  if(S.looksFresh){ const ly=by+(bh+gp)*3, p=Math.sin(S.t*6)>-0.2;                       /* new stock in the wardrobe */\n"
    "    g.fillStyle=p?C.red:'#7a2f22'; g.fillRect(lx+bw-52,ly-8,58,20); txt('NEW',lx+bw-23,ly+2,11,'#fff0d8','center');\n"
    "    g.strokeStyle=C.gold; g.lineWidth=3; if(p) g.strokeRect(lx-3,ly-3,bw+6,bh+6); }")
rep("      const msg='NEW AT THE FIXER: '+parts.join(' · '), mw=txtw(msg,14)+40;",
    "      const msg='NEW AT STALL & LOOKS: '+parts.join(' · '), mw=txtw(msg,14)+40;")
rep("    } else txt('nothing new at the Fixer this morning',W/2,y+h-34,10,C.dimmer,'center','normal'); }",
    "    } else txt('nothing new at Stall & Looks this morning',W/2,y+h-34,10,C.dimmer,'center','normal'); }")

# ---------- the sign was typed into S.look but saved from S.worn ----------
rep("function saveLook(){ saveGame(); }                        /* the look belongs to the save slot */",
    "function saveLook(){ saveGame(); }                        /* the look belongs to the save slot */\n"
    "function setSign(s){ S.look.sign=s; S.worn.sign=s; }     /* the save serialises S.worn, so the name lives in both */")
rep("    if(ev.key==='Backspace'){ S.look.sign=(S.look.sign||'').slice(0,-1); saveLook(); ev.preventDefault(); }",
    "    if(ev.key==='Backspace'){ setSign((S.look.sign||'').slice(0,-1)); saveLook(); ev.preventDefault(); }")
rep("      if(/[A-Z0-9 '&.\\-]/.test(ch)){ S.look.sign=(S.look.sign||'')+ch; saveLook(); }",
    "      if(/[A-Z0-9 '&.\\-]/.test(ch)){ setSign((S.look.sign||'')+ch); saveLook(); }")

# ---------- 6 + 9. slots -> intro -> name -> how-to -> day 1 ----------
rep("function newGame(n){ slotErase(n); S.slotPick=n; S.scene='howto'; S.sceneT=0; }",
    "function newGame(n){ slotErase(n); S.slotPick=n; achReset(); lookReset(); startIntro(); }   /* fresh progress, then the intro */")
rep("  achReset(); lookReset(); startRun(); S.slot=S.slotPick||1;","  startRun(); S.slot=S.slotPick||1;")
rep("  if(S.introN<INTRO.length-1){ S.introN++; S.introT=0; Snd.ui(); } else beginRun();",
    "  if(S.introN<INTRO.length-1){ S.introN++; S.introT=0; Snd.ui(); } else toNameScene();")
rep("  button(W-140,20,120,36,'SKIP',()=>beginRun(),C.dim,12);","  button(W-140,20,120,36,'SKIP',()=>toNameScene(),C.dim,12);")
rep("  if(S.scene==='intro'){ if(ev.key==='Escape') beginRun(); else if(ev.key==='Enter'||ev.key===' ') introClick(); ev.preventDefault(); return; }",
    "  if(S.scene==='intro'){ if(ev.key==='Escape') toNameScene(); else if(ev.key==='Enter'||ev.key===' ') introClick(); ev.preventDefault(); return; }\n"
    "  if(S.scene==='name'){ if(ev.key==='Enter'){ if(S.nameBuf.trim()) nameKey('OK'); } else if(ev.key==='Backspace') nameKey('BS'); else if(ev.key.length===1) nameKey(ev.key.toUpperCase()); ev.preventDefault(); return; }")
rep("  button(W/2-160,y+h-96,320,58,'OK',()=>startIntro(),C.gold,22);","  button(W/2-160,y+h-96,320,58,'OK',()=>beginRun(),C.gold,22);")
rep("  else if(S.scene==='intro') drawIntro();","  else if(S.scene==='intro') drawIntro();\n  else if(S.scene==='name') drawName();")
rep("['title','slots','howto','intro','settings','bye','gameover','ach','map']","['title','slots','howto','intro','name','settings','bye','gameover','ach','map']")
# keycap gets a rust finish
rep("  const live=state==='ready', top=live?'#ddd2ba':(state==='rest'?'#8f8776':'#5e584d'),\n"
    "        hi=live?'#f6eed8':(state==='rest'?'#a59c89':'#6e675b'), side=live?'#9c9078':(state==='rest'?'#5f594c':'#403c34'),\n"
    "        ink=live?'#1a1410':(state==='rest'?'#2e2a23':'#2a2722'), lift=down?0:3;",
    "  const live=state==='ready', rust=state==='rust',\n"
    "        top=rust?'#7a4a2a':live?'#ddd2ba':(state==='rest'?'#8f8776':'#5e584d'),\n"
    "        hi=rust?'#9a6238':live?'#f6eed8':(state==='rest'?'#a59c89':'#6e675b'),\n"
    "        side=rust?'#4a2c18':live?'#9c9078':(state==='rest'?'#5f594c':'#403c34'),\n"
    "        ink=rust?'#f0d8b0':live?'#1a1410':(state==='rest'?'#2e2a23':'#2a2722'), lift=down?0:3;")
rep("  g.fillStyle=live?col:side; g.fillRect(tx+4,ty+th-4,tw-8,2);                     /* the perk's colour, like a painted legend */",
    "  g.fillStyle=live?col:side; g.fillRect(tx+4,ty+th-4,tw-8,2);                     /* the perk's colour, like a painted legend */\n"
    "  if(rust){ g.fillStyle='#c8702a'; g.fillRect(tx+2+((x*7)%Math.max(1,tw-8)),ty+2+((y*5)%Math.max(1,th-6)),3,2);   /* rust flecks */\n"
    "            g.fillStyle='#2e160c'; g.fillRect(tx+tw-5-((x*3)%4),ty+th-5-((y*3)%3),2,2); }")
# the name screen itself, after drawIntro
rep("function toTitle(){ S.paused=false;",
    r"""/* ---------- the name screen: after the intro, before the how-to card ---------- */
const NAME_OK=/[A-Z0-9 '&.\-]/, NAME_ROWS=['1234567890','QWERTYUIOP','ASDFGHJKL','ZXCVBNM-&'];
function toNameScene(){ S.scene='name'; S.sceneT=0; S.nameBuf=''; S.nameT=0; S.nameHit=null; }
function nameKey(ch){                                        /* one path for the on-screen keys and the real keyboard */
  if(ch==='BS') S.nameBuf=S.nameBuf.slice(0,-1);
  else if(ch==='OK'){ setSign(S.nameBuf.trim()||'TRADER'); invalidateLook(); S.scene='howto'; S.sceneT=0; Snd.good(); return; }
  else if(S.nameBuf.length<10&&NAME_OK.test(ch)) S.nameBuf+=ch;
  else { Snd.bad(); return; }
  S.nameHit={k:ch,t:S.t}; Snd.ui();
}
function drawName(){
  S.nameT+=1/60;
  fillFull('#000');
  const line="Let's give my new place a proper name:", k=Math.min(line.length,Math.max(0,Math.floor((S.nameT-0.4)*18)));
  txt(line.slice(0,k)+(k<line.length?'_':''),W/2,150,22,C.ink,'center');
  const fx=W/2-220, fy=205;
  plate(fx,fy,440,56,'#1d1712',C.gold);
  const cur=Math.sin(S.t*6)>0?'_':'';
  if(S.nameBuf) txt(S.nameBuf+cur,W/2,fy+28,26,C.gold,'center');
  else { txt('TRADER',W/2,fy+28,26,C.dimmer,'center'); txt(cur,W/2+txtw('TRADER',26)/2+6,fy+28,26,C.gold,'center'); }
  txt('up to 10 letters  ·  type, or use the board',W/2,fy+74,10,C.dimmer,'center','normal');
  const KW=60, KH=48, KP=68, x0=W/2-(9*KP+KW)/2;
  const hit=(ch)=>S.nameHit&&S.nameHit.k===ch&&S.t-S.nameHit.t<0.12;
  NAME_ROWS.forEach((row,r)=>{
    const y=300+r*64, off=[0,0,34,68][r];
    for(let i=0;i<row.length;i++){ const ch=row[i], x=x0+off+i*KP;
      keycap(x,y,KW,KH,ch,'#b8622a','rust',hit(ch)); BTNS.push({x:x,y:y,w:KW,h:KH,fn:()=>nameKey(ch)}); }
  });
  const y5=556;
  keycap(x0,y5,120,KH,'DEL','#b8622a','rust',hit('BS'));   BTNS.push({x:x0,y:y5,w:120,h:KH,fn:()=>nameKey('BS')});
  keycap(x0+128,y5,260,KH,'SPACE','#b8622a','rust',hit(' ')); BTNS.push({x:x0+128,y:y5,w:260,h:KH,fn:()=>nameKey(' ')});
  const ok=!!S.nameBuf.trim();
  if(ok) button(x0+396,y5,276,KH,"THAT'S THE NAME",()=>nameKey('OK'),C.gold,14);
  else { plate(x0+396,y5,276,KH,'#15110d','#33291f'); txt("THAT'S THE NAME",x0+396+138,y5+KH/2,14,C.dimmer,'center'); }
}
function toTitle(){ S.paused=false;""")

# ---------- 7. the walker: a scavenger, not a cowboy ----------
rep("""const WALK_TOP=['....kkkk....','...kkkkkk...','..kkkkkkkk..','....kkkk....','....kkkk....','...kkkkkkk..','..kkkkkkkkk.','.kkkkkkkkkk.',
                '.kk.kkkk.kkk','.kk.kkkk.kkk','.k..kkkk..k.','....kkkk....','....kkkk....','....kkkk....','....kkkk....'];
const WALK_PX=[
 WALK_TOP.concat(['...kkkkkk...','...kkk.kk...','..kkk..kkk..','..kk....kk..','.kkk....kkk.','.kk......kk.','kkk......kkk','kk........kk','kkk......kkk']),
 WALK_TOP.concat(['....kkkk....','....kkkk....','....kkkk....','....kkkk....','....kkkk....','....kkkk....','...kkkkk....','...kkkkk....','..kkk.kkk...'])
].map(r=>spriteFrom(r,{k:'#120c10'}));""",
"""/* a scavenger in silhouette: hood with a goggle bump, pack with a bedroll, a staff in the leading hand, ragged hem, canteen */
const WALK_TOP=['......kkkk......','.....kkkkkk.....','....kkkkkkkk....','....kkkkkkkkk...','....kkkkkkkk...k','.....kkkkkk....k','......kkk......k',
                '..kk.kkkkkkk...k','.kkkkkkkkkkkk..k','.kkkkkkkkkkkkkkk','.kkkkkkkkkkkk..k','.kkkkkkkkkk....k','.kkkk.kkkkkk...k','.kkkk.kkkkkk...k',
                '..kk..kkkkkkk..k','..kk..kkkkkkk..k','.....kkkkkkkkk.k','.....kk.kkkkk..k','.....kkkkk.kk..k'];
const WALK_PX=[
 WALK_TOP.concat(['.....kkk.kkk...k','....kkk...kkk..k','....kk.....kk..k','...kkk.....kkk.k','...kk.......kk.k','..kkk.......kkkk','..kk.........kkk']),
 WALK_TOP.concat(['......kkkkk....k','......kkkkk....k','......kkkk.....k','......kkkk.....k','......kkkk.....k','.....kkkkk.....k','....kkk.kkk....k'])
].map(r=>spriteFrom(r,{k:'#120c10'}));""")
rep("    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-34,iy+64*4-3,70,4);\n    blit(WALK_PX[f],ix+wx*4,iy+64*4-24*5-bob*5,5);",
    "    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-40,iy+64*4-3,86,4);\n    blit(WALK_PX[f],ix+wx*4,iy+64*4-26*5-bob*5,5);")

# ---------- 8. card 4: a shop, nobody in it ----------
rep("let INTRO_BG=null, INTRO_KEY=null;","let INTRO_BG=null, INTRO_KEY=null, INTRO_SHOP=null;")
rep("function startIntro(){ if(!INTRO_BG) INTRO_BG=buildIntroWalk(); if(!INTRO_KEY) INTRO_KEY=buildIntroKey();",
    "function startIntro(){ if(!INTRO_BG) INTRO_BG=buildIntroWalk(); if(!INTRO_KEY) INTRO_KEY=buildIntroKey(); if(!INTRO_SHOP) INTRO_SHOP=buildIntroShop();")
rep("""  else {
    if(!SCENE) SCENE=buildScene();
    g.fillStyle='#1a1410'; g.fillRect(ix,iy,iw,ih);
    g.drawImage(SCENE,28,10,150,80,ix,iy,iw,ih);                       /* the stall, opened */
    blit(traderSprite(),ix+iw-170,iy+ih-150,4);
  }""","""  else g.drawImage(INTRO_SHOP,ix,iy,iw,ih);                            /* the shop, open, nobody in yet */""")
rep("function startIntro(){",
    r"""function buildIntroShop(){                                  /* a shack of tin and planks, shutters open, at first light */
  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  const glyph=(rows,gx,gy,col)=>rows.forEach((r,j)=>{ for(let i=0;i<r.length;i++) if(r[i]==='k') px(gx+i,gy+j,1,1,col); });
  ['#1c1a3a','#33284e','#5a3a58','#8a4a52','#c06a48','#e8985a','#f8c878'].forEach((col,i)=>px(0,i*8,Wc,9,col));
  for(let dy=-9;dy<=9;dy++){ const w=Math.floor(Math.sqrt(81-dy*dy)); px(126-w,30+dy,w*2+1,1,dy<-4?'#fff6d0':'#ffdc8a'); }
  let sd=3; const rn=()=>{ sd=(sd*1103515245+12345)&0x7fffffff; return sd/0x7fffffff; };
  let fx=0; while(fx<Wc){ const w=3+rn()*8, h=4+rn()*14; px(fx,56-h,w,h,'#2e1e30'); fx+=w+2+rn()*5; }
  px(0,56,Wc,24,'#3a2c24'); for(let k=0;k<20;k++) px(rn()*Wc,60+rn()*18,6+rn()*12,1,k%2?'#4a3a30':'#2a1e18');
  /* the shack */
  px(34,26,84,34,'#3d4246'); for(let k=36;k<116;k+=2) px(k,26,1,34,'#5a6064');                /* corrugated tin */
  px(34,26,20,34,'#6b4a30'); for(let k=30;k<60;k+=4) px(34,k,20,1,'#4a3220'); px(34,26,1,34,'#3a2718'); px(53,26,1,34,'#3a2718');   /* plank end */
  [[70,30],[104,44],[90,52]].forEach(p=>{ px(p[0],p[1],5,3,'#8a4a22'); px(p[0]+1,p[1]+1,2,1,'#b06030'); });                        /* rust */
  px(30,20,92,6,'#3b3025'); px(30,20,92,1,'#5a4a38'); px(28,25,96,2,'#2a2018'); px(60,21,14,2,'#8a4a22');                        /* lean-to roof */
  px(108,4,1,17,'#2a2422'); px(105,7,7,1,'#2a2422'); px(106,10,5,1,'#2a2422');                                                    /* aerial */
  px(58,10,32,10,'#3a2718'); px(58,10,32,1,'#5a4030'); px(60,20,1,2,'#2a1e14'); px(87,20,1,2,'#2a1e14');                          /* roof sign */
  glyph(['kkk','k.k','k.k','k.k','kkk'],62,12,'#f2dfb4'); glyph(['kkk','k.k','kkk','k..','k..'],68,12,'#f2dfb4');
  glyph(['kkk','k..','kkk','k..','kkk'],74,12,'#f2dfb4'); glyph(['k.k','kkk','kkk','k.k','k.k'],80,12,'#f2dfb4');
  px(40,34,60,7,'#b8502f'); for(let k=40;k<100;k+=8) px(k,34,4,7,'#d0663c'); px(40,41,60,2,'#2a1a14');                            /* awning */
  px(72,35,10,5,'#7a4a3a'); for(let k=73;k<82;k+=2) px(k,35,1,1,'#3a2418');                                                       /* patch */
  px(40,43,1,10,'#2a2018'); px(99,43,1,10,'#2a2018');
  px(58,40,26,14,'#14100c'); px(60,48,22,1,'#4a3a2a'); [[62,44,'#c8a040'],[67,44,'#a04030'],[72,44,'#7a8a9a'],[77,44,'#c8a040']].forEach(t=>{ px(t[0],t[1],4,4,t[2]); px(t[0],t[1],4,1,'#f0e0b0'); });
  px(52,38,5,17,'#6b4a30'); px(85,38,5,17,'#6b4a30'); px(53,40,3,1,'#4a3220'); px(53,46,3,1,'#4a3220'); px(86,40,3,1,'#4a3220'); px(86,46,3,1,'#4a3220');   /* shutters */
  px(103,42,12,18,'#2a1c14'); px(104,43,10,16,'#1a1210'); px(112,51,1,2,'#c8a040');                                               /* door, ajar */
  px(122,26,1,10,'#2a2422'); px(121,36,3,4,'#f8e0a0'); px(122,35,1,1,'#3a2422');                                                 /* bare bulb */
  for(let r=8;r>0;r--) px(122-r,38-r*0.6,r*2,r*1.2,'rgba(255,220,140,'+(0.05)+')');
  px(4,44,10,14,'#4a423a'); px(4,47,10,1,'#6b6258'); px(4,54,10,1,'#6b6258'); px(5,44,1,14,'#5c554a');                           /* barrel */
  px(16,48,13,10,'#6b4a30'); px(16,48,13,1,'#8a6a45'); px(22,48,1,10,'#4a3220'); px(18,40,10,8,'#5a3f28'); px(18,40,10,1,'#7a5a3a');   /* crates */
  [[122,54],[131,54],[126,50],[135,50],[130,46]].forEach(b=>{ px(b[0],b[1],10,4,'#8a7a5a'); px(b[0],b[1],10,1,'#a89a7a'); });    /* sandbags */
  return c;
}
function startIntro(){""")

# ---------- 4. a picture that fits the news ----------
PICS={'dust':'The east road, before the grit came.','heat':'Tins going fast at the strip.','cold':'Beans for the shiverers.',
 'acid':'Boards under tarps, west end.','fair':'Produce, knee-deep.','gangs':'The ridge road at dusk.','raiders':'Fires past the north wash.',
 'militia':'Wall duty: bring your own iron.','truce':'Quiet on the ridge.','convoy':'Where the convoy should have been.',
 'fever':'The clinic lamp, lit again.','harvest':'Carts queued at the gate.','tower':'Half the tank, in the street.',
 'bunker':'Crates out of the rail-yard store.','power':'The works, dark.','quack':'Free at the gate. Mostly sugar.'}
cnt=[0]
def addpic(m):
    cnt[0]+=1; return "{id:'%s',%spic:'%s', type:"%(m.group(1),m.group(2),PICS[m.group(1)])
src=re.sub(r"\{id:'(\w+)',(\s*)type:",addpic,src)
assert cnt[0]==16, cnt; n+=1
start=src.index("let PAPER_IMG=null;\nfunction buildPaperImg(){"); end=src.index("function drawPaper(){")
assert end>start
src=src[:start]+r"""/* one picture per story: a backdrop for the family (weather / military / town) and the goods it is about in front;
   a glut ("prices down") shows twice the goods. Newsprint greys, and the same speckle as before so it looks printed. */
const PAPER_IMGS={};
function paperImg(ev){ const k=ev.id+(ev.m>1?'+':'-'); if(!PAPER_IMGS[k]) PAPER_IMGS[k]=buildPaperImg(ev); return PAPER_IMGS[k]; }
function buildPaperImg(ev){
  const c=makeCanvas(96,54), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  const NP=['#e0d6be','#cdc2aa','#b4a991','#9a8f79','#7e735f','#5e564a','#332e26'];
  const up=!ev||ev.m>1, type=ev?ev.type:'town', cat=ev?ev.cat:'food';
  let seed=11; const rn=()=>{ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; };
  const skyC=up?[NP[3],NP[2],NP[2],NP[1]]:[NP[1],NP[1],NP[0],NP[0]];
  for(let i=0;i<4;i++) px(0,i*8,96,9,skyC[i]);
  let rx=0;
  if(type==='weather'){
    if(up){ for(let i=0;i<9;i++){ const cx=rn()*96, cy=2+rn()*12, w=10+rn()*16; px(cx,cy,w,4,NP[5]); px(cx+2,cy+4,w-4,2,NP[4]); }
            for(let i=0;i<40;i++){ const sx=rn()*96, sy=6+rn()*30; px(sx,sy,1,4,NP[4]); px(sx-1,sy+4,1,2,NP[4]); } }
    else { for(let dy=-7;dy<=7;dy++){ const w=Math.floor(Math.sqrt(49-dy*dy)); px(70-w,12+dy,w*2+1,1,NP[0]); }
           for(let r=0;r<5;r++){ const a=-2.6+r*0.55; for(let k=10;k<30;k+=2) px(70+Math.cos(a)*k,12+Math.sin(a)*k,1,1,NP[0]); } }
    px(0,38,96,16,NP[3]); px(0,42,96,12,NP[4]);
    for(let i=0;i<12;i++) px(rn()*96,40+rn()*12,6+rn()*10,1,NP[2]);
  } else if(type==='military'){
    while(rx<96){ const w=6+rn()*12, h=8+rn()*14; px(rx,34-h,w,h+4,NP[4]); px(rx,34-h,w,1,NP[3]); rx+=w; }
    px(0,36,96,18,NP[5]); px(0,40,96,14,NP[4]);
    const fires=up?5:1;
    for(let i=0;i<fires;i++){ const fx=8+i*18+rn()*8, fy=30-rn()*8; px(fx,fy,3,2,NP[0]); px(fx-1,fy+2,5,2,NP[1]);
      if(up) for(let k=1;k<8;k++) px(fx+1+Math.sin(k*0.9)*1.5,fy-k*2,2+(k>3?1:0),2,NP[2]); }
    if(!up){ px(70,10,1,22,NP[6]); px(71,10,9,6,NP[0]); px(71,10,9,1,NP[5]); }
  } else {
    for(let dy=-5;dy<=5;dy++){ const w=Math.floor(Math.sqrt(25-dy*dy)); px(70-w,12+dy,w*2+1,1,NP[0]); }
    while(rx<96){ const w=4+rn()*9, h=6+rn()*16; px(rx,32-h,w,h+2,NP[3]); rx+=w+2; }
    px(14,16,9,6,NP[4]); px(16,22,2,10,NP[4]); px(20,22,2,10,NP[4]); px(13,15,11,1,NP[5]);
    rx=0; while(rx<96){ const w=6+rn()*10, h=4+rn()*12; px(rx,36-h,w,h+5,NP[5]);
      for(let wy=36-h+2;wy<36;wy+=3) for(let wx=rx+1;wx<rx+w-1;wx+=3) if(((wx*5+wy*7)%4)===0) px(wx,wy,1,1,NP[6]); rx+=w+3; }
    px(0,41,96,13,NP[3]); px(0,45,96,6,NP[4]); for(let i=0;i<96;i+=8) px(i,47,4,1,NP[1]);
  }
  const sub=(ox,oy)=>{
    if(cat==='food'){ px(ox,oy+8,20,10,NP[4]); px(ox+1,oy+9,18,1,NP[3]); px(ox,oy+8,20,1,NP[5]);
      for(let r=0;r<2;r++) for(let i=0;i<(r?2:3);i++){ const tx=ox+22+i*7+r*3, ty=oy+11-r*8; px(tx,ty,6,7,NP[2]); px(tx,ty,6,1,NP[0]); px(tx,ty+3,6,2,NP[5]); px(tx,ty+6,6,1,NP[4]); } }
    else if(cat==='meds'){ px(ox,oy+6,16,11,NP[1]); px(ox,oy+6,16,3,NP[0]); px(ox,oy+6,16,1,NP[4]); px(ox+6,oy+9,4,7,NP[6]); px(ox+4,oy+11,8,3,NP[6]);
      px(ox+19,oy+7,4,10,NP[3]); px(ox+20,oy+5,2,2,NP[5]); px(ox+25,oy+9,4,8,NP[2]); px(ox+26,oy+7,2,2,NP[5]); }
    else if(cat==='guns'){ px(ox,oy+13,26,4,NP[3]); px(ox+2,oy+9,22,4,NP[3]); px(ox+4,oy+5,18,4,NP[3]); [oy+13,oy+9,oy+5].forEach(yy=>px(ox,yy,26,1,NP[1]));
      for(let i=0;i<2;i++){ const gx=ox+6+i*9; px(gx,oy-4,1,18,NP[6]); px(gx+1,oy-2,1,3,NP[6]); px(gx-1,oy+6,3,6,NP[5]); } }
    else { px(ox,oy+3,8,14,NP[5]); px(ox+1,oy+4,6,2,NP[1]); px(ox+2,oy+1,4,2,NP[6]); px(ox+1,oy+8,6,1,NP[3]);
      px(ox+11,oy+9,14,8,NP[4]); for(let yy=oy+10;yy<oy+16;yy+=2) for(let xx=ox+12;xx<ox+24;xx+=2) px(xx,yy,1,1,NP[1]);
      px(ox+29,oy-4,1,21,NP[6]); px(ox+26,oy-2,7,1,NP[6]); px(ox+27,oy+1,5,1,NP[6]); }
  };
  sub(8,36); if(!up) sub(52,36);
  for(let i=0;i<200;i++){ const gx=(i*37)%96, gy=(i*53)%54; px(gx,gy,1,1,'rgba(40,34,26,0.10)'); }
  return c;
}
"""+src[end:]; n+=1
rep("""  if(!PAPER_IMG) PAPER_IMG=buildPaperImg();
  const ix=x+34, iy=y+108;
  g.fillStyle=INK; g.fillRect(ix-3,iy-3,96*3+6,54*3+6);
  blit(PAPER_IMG,ix,iy,3);
  txt('The east road, yesterday.',ix,iy+54*3+16,11,FADE,'left','normal');
  const tx2=ix+96*3+26, tw2=x+w-34-tx2;
  const ev=S.event||EVENTS[0];""",
"""  const ev=S.event||EVENTS[0], evDef=EVENTS.find(e=>e.id===ev.id)||ev;   /* a stored event from an older build has no caption */
  const ix=x+34, iy=y+108;
  g.fillStyle=INK; g.fillRect(ix-3,iy-3,96*3+6,54*3+6);
  blit(paperImg(ev),ix,iy,3);
  txt(ev.pic||evDef.pic||'The east road, yesterday.',ix,iy+54*3+16,11,FADE,'left','normal');
  const tx2=ix+96*3+26, tw2=x+w-34-tx2;""")

# ---------- 10. the picture reaches the window edges ----------
rep("let VS=1, VX=0, VY=0;","let VS=1, VX=0, VY=0, EXX=0, EXY=0;            /* EXX/EXY: design-space margin visible beyond the 1280x760 frame */")
rep("  VS=Math.min(cw/W, ch/H); VX=(cw-W*VS)/2; VY=(ch-H*VS)/2;",
    "  VS=Math.min(cw/W, ch/H); VX=(cw-W*VS)/2; VY=(ch-H*VS)/2; EXX=VX/VS; EXY=VY/VS;")
rep("function resize(){","/* the whole visible window in design units (with a pad for the screen shake) */\n"
    "function fullRect(){ return {x:-EXX-16,y:-EXY-16,w:W+2*EXX+32,h:H+2*EXY+32}; }\n"
    "function fillFull(style){ const r=fullRect(); g.fillStyle=style; g.fillRect(r.x,r.y,r.w,r.h); }\n"
    "function resize(){")
rep("  g.translate(VX,VY); g.scale(VS,VS);\n"
    "  if(S.shake>0.2) g.translate(Math.round(rnd(-S.shake,S.shake)),Math.round(rnd(-S.shake,S.shake)));\n"
    "  g.beginPath(); g.rect(0,0,W,H); g.clip();",
    "  g.translate(VX,VY); g.scale(VS,VS);\n"
    "  g.beginPath(); g.rect(-EXX,-EXY,W+2*EXX,H+2*EXY); g.clip();       /* the frame is the window, not the 1280x760 box */\n"
    "  if(S.shake>0.2) g.translate(Math.round(rnd(-S.shake,S.shake)),Math.round(rnd(-S.shake,S.shake)));")
rep("  g.drawImage(MAP_IMG,0,0,W,H);\n  g.fillStyle='rgba(20,14,8,0.18)'; g.fillRect(0,0,W,H);",
    "  fillFull('#1a1410'); g.drawImage(MAP_IMG,0,0,W,H);\n  fillFull('rgba(20,14,8,0.18)');")
before=src.count("g.fillRect(0,0,W,H)")
src,k=re.subn(r"g\.fillStyle=([^;]+); g\.fillRect\(0,0,W,H\);", lambda m:"fillFull(%s);"%m.group(1), src)
assert k==before and k>=11, (k,before); n+=1
assert "fillRect(0,0,W,H)" not in src
rep("  g.fillStyle='rgba(12,9,7,0.9)'; g.fillRect(0,0,W,LO.hudH);\n  g.fillStyle='#5c4a37'; g.fillRect(0,LO.hudH-2,W,2);",
    "  { const r=fullRect(); g.fillStyle='rgba(12,9,7,0.9)'; g.fillRect(r.x,r.y,r.w,LO.hudH-r.y); g.fillStyle='#5c4a37'; g.fillRect(r.x,LO.hudH-2,r.w,2); }")
rep("function buildScene(){\n  const sc=makeCanvas(320,190), x=sc.getContext('2d');",
    "let SCENE_EDGE=null;                       /* one column of just the sky and ground bands: what the margins show on a wide window */\n"
    "function buildScene(){\n  const sc=makeCanvas(320,190), x=sc.getContext('2d');")
rep("  for(let i=0;i<sky.length;i++) px(0,i*6,320,7,sky[i]);\n  px(0,78,320,6,'#d2954f');",
    "  for(let i=0;i<sky.length;i++) px(0,i*6,320,7,sky[i]);\n  px(0,78,320,6,'#d2954f');\n"
    "  { SCENE_EDGE=makeCanvas(1,190); const e=SCENE_EDGE.getContext('2d'), ep=(b,h,c)=>{ e.fillStyle=c; e.fillRect(0,b,1,h); };\n"
    "    sky.forEach((c,i)=>ep(i*6,7,c)); ep(78,6,'#d2954f'); ep(82,10,'#6b4c33'); ep(92,16,'#5b3f2b'); ep(108,34,'#4c3423'); ep(142,48,'#3d2a1c'); }")
rep("function drawScene(){\n  if(!SCENE) SCENE=buildScene();\n  blit(SCENE,0,0,4);",
    "function drawSceneEdges(){                 /* sky and ground carry on past the 1280 frame; the car and the pole do not repeat */\n"
    "  if(!SCENE_EDGE) return;\n"
    "  g.imageSmoothingEnabled=false;\n"
    "  if(EXX>0){ g.drawImage(SCENE_EDGE,0,0,1,190,-EXX-16,0,EXX+16,H); g.drawImage(SCENE_EDGE,0,0,1,190,W,0,EXX+16,H); }\n"
    "  if(EXY>0){ g.fillStyle='#241f3a'; g.fillRect(-EXX-16,-EXY-16,W+2*EXX+32,EXY+16); g.fillStyle='#3d2a1c'; g.fillRect(-EXX-16,H,W+2*EXX+32,EXY+16); }\n"
    "}\n"
    "function drawScene(){\n  if(!SCENE) SCENE=buildScene();\n  drawSceneEdges(); blit(SCENE,0,0,4);")

open(P,'w').write(src); print('applied',n,'edits')
