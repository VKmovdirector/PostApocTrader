#!/usr/bin/env python3
"""Build 26: robo-hand lvl 2 files two, ADAPTABILITY passive, cut scenes before day 9 and day 15, streak reset at dusk,
materials -15%, Strider parts -25%, the day's last buyer wants something in stock, actives generalised to ACTIVES.length."""
import re, sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b,count=1):
    global src,n
    if src.count(a)!=count: print('ANCHOR FAIL (%d found, want %d):\n%s'%(src.count(a),count,a[:200])); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("build 25: music loop, 20% fewer goods off the road","build 26: cut scenes, adaptability, robo-hand lvl 2, last buyer wants stock")
rep("  txt('build 25',W-20,H-18,10,C.dimmer,'right','normal');","  txt('build 26',W-20,H-18,10,C.dimmer,'right','normal');")

# ---- actives: no more hard-coded six ----
rep("S.actOwn=[false,false,false,false,false,false];\nS.actCd=[0,0,0,0,0,0]; S.handT=0; S.signalT=0;",
    "S.actOwn=ACTIVES.map(()=>false);\nS.actCd=ACTIVES.map(()=>0); S.handT=0; S.signalT=0;")
rep("  S.actOwn=[false,false,false,false,false,false]; S.actCd=[0,0,0,0,0,0]; S.steadyT=0;","  S.actOwn=ACTIVES.map(()=>false); S.actCd=ACTIVES.map(()=>0); S.steadyT=0;")
rep("  S.actCd=[0,0,0,0,0,0]; S.steadyT=0; S.patterT=0; S.handT=0; S.signalT=0;\n  S.crateDue=0;","  S.actCd=ACTIVES.map(()=>0); S.steadyT=0; S.patterT=0; S.handT=0; S.signalT=0;\n  S.crateDue=0;")
rep("  for(let i=0;i<6;i++) if(S.actCd[i]>0) S.actCd[i]=Math.max(0,S.actCd[i]-dt);","  for(let i=0;i<ACTIVES.length;i++) if(S.actCd[i]>0) S.actCd[i]=Math.max(0,S.actCd[i]-dt);")
rep("ev.key>='1'&&ev.key<='6'){ fireActive(+ev.key-1);","ev.key>='1'&&ev.key<=String(ACTIVES.length)){ fireActive(+ev.key-1);")
rep("let TIP=null, RAILPOS=[null,null,null,null,null,null], RAILAY=252;","let TIP=null, RAILPOS=ACTIVES.map(()=>null), RAILAY=252;")
rep("  TIP=null; RAILPOS=[null,null,null,null,null,null];","  TIP=null; RAILPOS=ACTIVES.map(()=>null);")

# ---- 2. robo-hand level 2 files two at once ----
rep("  {id:'drone', n:'SORTING ROBO-HAND', d:'a rusted arm that files for you every 9s', max:2, cost:[275,400]},",
    "  {id:'drone', n:'SORTING ROBO-HAND', d:'a rusted arm that files a piece every 9s · lvl 2 files two', max:2, cost:[275,400]},")
rep("""    S.droneT-=dt*S.up.drone;
    if(S.droneT<=0){
      S.droneT=9;
      for(let i=0;i<S.cslots;i++){
        const e=S.counter[i];
        if(e&&!e.arriving){
          const f=freeShelfSlot(e.item.cat);
          if(f){
            const from=counterSlotRect(i), to=shelfSlotRect(f.i,f.j);
            S.counter[i]=null;
            S.shelves[f.i].slots[f.j]={item:e.item,misfiled:false,arriving:1,anim:0};
            flyer(e.item,from.x+from.w/2,from.y+from.h/2,to.x+to.w/2,to.y+to.h/2,0.5,70,()=>{
              const sl=S.shelves[f.i].slots[f.j]; if(sl){ sl.arriving=0; sl.anim=1; } Snd.tick();
            });
          }
          break;
        }
      }""",
"""    S.droneT-=dt;
    if(S.droneT<=0){
      S.droneT=9; let filed=0;                                           /* level 2: two pieces per pass */
      for(let i=0;i<S.cslots&&filed<S.up.drone;i++){
        const e=S.counter[i];
        if(e&&!e.arriving){
          const f=freeShelfSlot(e.item.cat);
          if(f){
            const from=counterSlotRect(i), to=shelfSlotRect(f.i,f.j);
            S.counter[i]=null; filed++;
            S.shelves[f.i].slots[f.j]={item:e.item,misfiled:false,arriving:1,anim:0};
            flyer(e.item,from.x+from.w/2,from.y+from.h/2,to.x+to.w/2,to.y+to.h/2,0.5+filed*0.08,70,()=>{
              const sl=S.shelves[f.i].slots[f.j]; if(sl){ sl.arriving=0; sl.anim=1; } Snd.tick();
            });
          }
        }
      }""")

# ---- 3. ADAPTABILITY ----
rep("  {id:'guard', n:'HIRED GUN',      d:'raiders never rob you',         max:1, cost:[230]}\n];",
    "  {id:'guard', n:'HIRED GUN',      d:'raiders never rob you',         max:1, cost:[230]},\n"
    "  {id:'adapt', n:'ADAPTABILITY',   d:'on Herald days 5%/10% of caravan goods lean to what is dear, away from what is cheap', max:2, cost:[800,1600]}\n];")
rep(" shelf:['kkkkkkkk','k......k','kkkkkkkk','k.k..k.k','kkkkkkkk','k..k...k','kkkkkkkk','........'],",
    " shelf:['kkkkkkkk','k......k','kkkkkkkk','k.k..k.k','kkkkkkkk','k..k...k','kkkkkkkk','........'],\n"
    " adapt:['...k....','..kkk...','.k.k.k..','...k....','....k...','..k.k.k.','...kkk..','....k...'],")
rep("function rollItem(){\n  const it=pick(BYCAT[pick(activeCats())]), x=Math.random();",
    "/* ADAPTABILITY: on a Herald day the road leans: 5 (10) of every 100 pieces move toward the kind whose price is up,\n"
    "   or away from the kind whose price is down (a 25% share becomes 30%, or 20%) */\n"
    "function rollCat(){\n"
    "  const cats=activeCats(), e=evToday(), L=S.up.adapt||0;\n"
    "  if(e&&L){ if(e.m>1){ if(Math.random()<0.0667*L) return e.cat; }\n"
    "            else if(Math.random()<0.2*L) return pick(cats.filter(c=>c!==e.cat)); }\n"
    "  return pick(cats);\n"
    "}\n"
    "function rollItem(){\n  const it=pick(BYCAT[rollCat()]), x=Math.random();")

# ---- 4+5. cut scenes: the intro machinery becomes a reel player ----
rep("""const INTRO=[
 {text:'DUSTWELL. THE EDGE OF THE DUST.'},
 {text:"It's a new dawn..."},
 {text:'And a new beginning for me...'},
 {text:'Time to trade goods!'}
];""",
r"""const INTRO=[
 {text:'DUSTWELL. THE EDGE OF THE DUST.', gold:true, draw:(ix,iy,iw,ih)=>g.drawImage(CITY_DUSK,ix,iy,iw,ih)},
 {text:"It's a new dawn...", draw:(ix,iy,iw,ih)=>{
    g.drawImage(INTRO_BG,ix,iy,iw,ih);
    const wx=14+Math.min(84,S.introT*7), f=Math.floor(S.introT*4)%2, bob=f?0:1;   /* a figure walks toward the light */
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-40,iy+64*4-3,86,4);
    blit(WALK_PX[f],ix+wx*4,iy+64*4-26*5-bob*5,5); }},
 {text:'And a new beginning for me...', draw:(ix,iy,iw,ih)=>g.drawImage(INTRO_KEY,ix,iy,iw,ih)},
 {text:'Time to trade goods!', draw:(ix,iy,iw,ih)=>g.drawImage(INTRO_SHOP,ix,iy,iw,ih)}
];
/* two more reels: the morning of day 9 and the morning of day 15 */
const REEL9=[
 {text:'I need to focus on unlocking the workbench to make more money...', img:'bench'},
 {text:'A mighty storm is coming in 15 days...', img:'storm', flash:true},
 {text:'The town will probably be buried under sand and dust.', img:'buried'}
];
const REEL15=[
 {text:'I will be moving to another town on day 26...', img:'road'},
 {text:'For this I need to build myself a suitable transport...', img:'strider'},
 {text:"That's my main focus now!", img:'focus'}
];
const REEL_IMG={};
function reelImg(k){ if(!REEL_IMG[k]) REEL_IMG[k]=REEL_BUILD[k](); return REEL_IMG[k]; }
function playReel(cards,end){ S.reel=cards; S.reelEnd=end; S.scene='intro'; S.sceneT=0; S.introN=0; S.introT=0; }
function reelCanvas(){ const c=makeCanvas(150,80), x=c.getContext('2d'); const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  let sd=17; const rn=()=>{ sd=(sd*1103515245+12345)&0x7fffffff; return sd/0x7fffffff; }; return {c,x,px,rn}; }
const REEL_BUILD={
  bench(){ const {c,px,rn}=reelCanvas();                            /* a dim back room, the bench under one lamp */
    ['#0e0a08','#14100c','#1a1410','#211a14'].forEach((col,i)=>px(0,i*20,150,21,col));
    for(let k=0;k<150;k+=9) px(k,0,1,58,'#120d0a');                                            /* wall planks */
    px(10,14,52,3,'#4a3a2a'); px(10,17,52,1,'#2a1e14');                                        /* a shelf of jars */
    [[14,'#6fb8d8'],[24,'#a173c8'],[34,'#7fb74f'],[44,'#e8b13c']].forEach(j=>{ px(j[0],6,7,8,j[1]); px(j[0]+1,5,5,1,'#3a3228'); px(j[0]+2,8,1,4,'rgba(255,255,255,0.35)'); });
    px(74,0,1,18,'#2a2422'); px(66,18,17,5,'#3a3228'); px(69,23,11,3,'#f8e0a0');                /* the lamp */
    for(let r=1;r<=9;r++) px(74-r*4,26+r*3.6,r*8,3.6,'rgba(255,220,140,'+(0.06)+')');           /* its cone */
    px(20,50,110,6,'#6b4a30'); px(20,50,110,1,'#8a6a45'); px(24,56,6,24,'#4a3220'); px(120,56,6,24,'#4a3220');   /* the bench */
    px(58,36,24,14,'#3a3a3a'); px(54,40,32,6,'#4a4a4a'); px(50,42,8,3,'#4a4a4a'); px(58,36,24,1,'#6a6a6a');       /* anvil */
    px(96,40,3,10,'#6b4a30'); px(93,36,9,5,'#5a5a5a'); px(93,36,9,1,'#8a8a8a');                                 /* hammer */
    px(34,42,6,8,'#6fb8d8'); px(35,40,4,2,'#3a3228'); px(36,44,1,4,'rgba(255,255,255,0.4)');                     /* a bottle */
    px(110,44,10,6,'#c8703a'); px(111,45,8,1,'#f0a868'); px(111,48,8,1,'#f0a868');                              /* wire coil */
    px(0,80-18,150,18,'#151008'); for(let k=0;k<12;k++) px(rn()*150,64+rn()*14,5+rn()*8,1,'#1f1810');
    return c; },
  storm(){ const {c,px,rn}=reelCanvas();                           /* a wall of dust rolling in from the east */
    ['#a97a4a','#b98550','#c9955a','#d6a468','#e0b478','#e8c48a','#d9ad6c'].forEach((col,i)=>px(0,i*8,150,9,col));
    px(0,56,150,24,'#8a6a42'); for(let k=0;k<24;k++) px(rn()*150,58+rn()*20,8+rn()*14,1,k%2?'#a08050':'#6e5434');
    /* the storm: a towering brown-black front curving over, right half */
    for(let xx=60;xx<150;xx++){ const t=(xx-60)/90, top=Math.max(0,34-t*44), col=t<0.25?'#6b4a30':t<0.5?'#4a3220':t<0.75?'#33221a':'#231810'; px(xx,top,1,80-top,col); }
    for(let i=0;i<70;i++){ const sx=62+rn()*88, sy=rn()*80, w=3+rn()*9; px(sx,sy,w,1,i%3?'#5a3e28':'#2a1c12'); }   /* churn */
    for(let i=0;i<26;i++) px(30+rn()*40,10+rn()*60,2+rn()*6,1,'#9a7a52');                                          /* grit flying ahead */
    /* lightning */
    [[96,4],[124,12]].forEach(l=>{ let lx=l[0], ly=l[1]; for(let k=0;k<9;k++){ px(lx,ly,1,4,'#fff2c0'); lx+=(k%2?-2:2); ly+=4; } });
    /* the town, small, at the left */
    [[6,48,6],[14,44,5],[22,50,4],[30,46,7]].forEach(b=>{ px(b[0],b[1],b[2],56-b[1],'#4a3428'); }); px(0,54,44,3,'#3a2a20');
    return c; },
  buried(){ const {c,px,rn}=reelCanvas();                          /* the town under the dunes: only the tops show */
    ['#c9a46a','#d4b078','#dcbb84','#e3c48e','#e8cc98','#ecd2a0','#efd6a6'].forEach((col,i)=>px(0,i*8,150,9,col));
    for(let i=0;i<60;i++) px(rn()*150,rn()*50,1,1,'rgba(90,70,40,0.35)');                                        /* dust haze */
    [[12,30,11],[30,22,9],[47,36,13],[70,18,8],[84,28,10],[118,34,12],[134,24,9]].forEach(t=>{ const top=60-t[1]; px(t[0],top,t[2],60-top,'#3a2e30'); px(t[0],top,2,60-top,'#4a3a3e');
      for(let wy=top+4;wy<52;wy+=5) for(let wx=t[0]+2;wx<t[0]+t[2]-2;wx+=3) if(rn()<0.2) px(wx,wy,1,2,'#2a2024'); });
    px(59,30,10,7,'#241a26'); px(60,37,1,14,'#241a26'); px(67,37,1,14,'#241a26');                                /* water tower */
    /* the dunes over everything */
    for(let xx=0;xx<150;xx++){ const y=48+Math.sin(xx*0.09)*6+Math.sin(xx*0.031+1)*5; px(xx,y,1,80-y,'#d8b374'); px(xx,y,1,1,'#f0d49a'); }
    for(let xx=0;xx<150;xx++){ const y=62+Math.sin(xx*0.06+2)*4; px(xx,y,1,80-y,'#c9a061'); px(xx,y,1,1,'#e6c184'); }
    for(let k=0;k<30;k++) px(rn()*150,50+rn()*28,4+rn()*10,1,k%2?'#e2c085':'#b8925a');
    px(100,44,1,16,'#3a2a22'); px(96,44,10,4,'#5a4030'); px(97,45,8,1,'#8a6a45');                                /* a sign, going under */
    return c; },
  road(){ const {c,px,rn}=reelCanvas();                            /* the road out, a town on the skyline */
    ['#2c2a4e','#4a3a62','#7a4a5c','#b06a50','#dc9458','#f2bc70','#fbe0a0'].forEach((col,i)=>px(0,i*8,150,9,col));
    for(let dy=-8;dy<=0;dy++){ const w=Math.floor(Math.sqrt(64-dy*dy)); px(96-w,52+dy,w*2+1,1,'#fff0c0'); }
    let fx=60; while(fx<130){ const w=2+rn()*5, h=3+rn()*8; px(fx,52-h,w,h,'#3a2a3c'); fx+=w+1; }               /* the far town */
    px(84,40,1,12,'#3a2a3c'); px(82,38,5,2,'#3a2a3c'); px(86,30,2,8,'rgba(60,44,60,0.5)');                       /* a chimney, smoke */
    px(0,52,150,28,'#5a4432'); for(let k=0;k<20;k++) px(rn()*150,54+rn()*24,6+rn()*12,1,k%2?'#6e5640':'#3f2f22');
    for(let y=52;y<80;y++){ const t=(y-52)/28, hw=1+t*40; px(96-hw,y,hw*2,1,'#7a6048'); if(y%4===0) px(96-1,y,2,2,'#a08868'); }   /* the road */
    px(14,36,2,30,'#3a2a22'); px(16,38,22,7,'#6b4a30'); px(16,38,22,1,'#8a6a45'); px(33,39,5,5,'#6b4a30'); px(18,40,16,1,'#f2dfb4'); px(18,42,12,1,'#f2dfb4');   /* signpost with an arrow board */
    px(120,60,4,7,'#8a7a5a'); px(121,58,2,2,'#a89a7a');                                                        /* milestone */
    return c; },
  strider(){ const {c,x,px,rn}=reelCanvas();                       /* the yard: the walker still a blueprint */
    ['#1c1a3a','#33284e','#5a3a58','#8a4a52','#c06a48','#e8985a','#f8c878'].forEach((col,i)=>px(0,i*8,150,9,col));
    px(0,56,150,24,'#2e2420'); for(let k=0;k<18;k++) px(rn()*150,58+rn()*20,6+rn()*12,1,k%2?'#3e3028':'#1e1612');
    px(0,54,150,2,'#1d1620'); for(let k=0;k<150;k+=6) px(k,52,3,2,'#1d1620');                                    /* the wall behind */
    const saved=S.rig; S.rig={}; const sc=striderCanvas(); S.rig=saved;
    x.imageSmoothingEnabled=false; x.drawImage(sc,0,0,176,100,26,2,106,60);
    px(112,48,14,10,'#6b4a30'); px(112,48,14,1,'#8a6a45'); px(114,44,10,4,'#5a5a5a'); px(116,42,3,3,'#8a8a8a');  /* a crate of parts */
    px(10,50,12,4,'#8a8a8a'); px(8,48,4,8,'#8a8a8a'); px(22,49,3,6,'#8a8a8a');                                    /* a wrench */
    return c; },
  focus(){ const {c,px,rn}=reelCanvas();                           /* close: the gear, the wrench, the sparks */
    ['#0e0a08','#14100c','#1a1410','#211a14'].forEach((col,i)=>px(0,i*20,150,21,col));
    const gx=64, gy=42, R=26;
    for(let a=0;a<360;a+=1){ const r=(Math.floor(a/22.5)%2?R:R-5); for(let k=8;k<=r;k++) px(gx+Math.cos(a*Math.PI/180)*k,gy+Math.sin(a*Math.PI/180)*k,1,1,'#6a5a48'); }
    for(let a=0;a<360;a+=4) px(gx+Math.cos(a*Math.PI/180)*6,gy+Math.sin(a*Math.PI/180)*6,1,1,'#3a3028');
    for(let a=0;a<360;a+=2) px(gx+Math.cos(a*Math.PI/180)*(R-8),gy+Math.sin(a*Math.PI/180)*(R-8),1,1,'#8a7a62');
    [[70,30],[84,44],[54,52],[76,58]].forEach(p=>{ px(p[0],p[1],3,2,'#8a4a22'); px(p[0]+1,p[1]+1,2,1,'#b06030'); });   /* rust */
    for(let k=0;k<50;k++) px(90+k*1.1,64-k*0.7,3,3,'#9a9a9a'); px(136,20,12,10,'#9a9a9a'); px(140,23,6,4,'#1a1410'); px(92,60,10,10,'#8a8a8a');   /* the wrench */
    for(let k=0;k<50;k++) px(90+k*1.1,63-k*0.7,3,1,'#c8c8c8');
    for(let i=0;i<16;i++){ const sx=96+rn()*20, sy=52+rn()*14; px(sx,sy,2,1,i%2?'#ffe08a':'#ff9a3c'); px(sx+rn()*6-3,sy-rn()*8,1,1,'#fff0b0'); }   /* sparks */
    for(let r=1;r<=8;r++) px(100-r*3,58-r*3,r*6,r*6,'rgba(255,190,90,0.03)');
    return c; }
};""")
rep("function startIntro(){ if(!INTRO_BG) INTRO_BG=buildIntroWalk(); if(!INTRO_KEY) INTRO_KEY=buildIntroKey(); if(!INTRO_SHOP) INTRO_SHOP=buildIntroShop(); if(!CITY_DUSK) CITY_DUSK=buildCity('dusk');\n"
    "  S.scene='intro'; S.sceneT=0; S.introN=0; S.introT=0; }\n"
    "function introTyped(){ const s=INTRO[S.introN].text; return Math.min(s.length,Math.max(0,Math.floor((S.introT-0.7)*18))); }\n"
    "function introClick(){\n"
    "  const s=INTRO[S.introN].text;\n"
    "  if(introTyped()<s.length){ S.introT=99; return; }          /* first click finishes the line */\n"
    "  if(S.introN<INTRO.length-1){ S.introN++; S.introT=0; Snd.ui(); } else toNameScene();\n"
    "}",
    "function startIntro(){ if(!INTRO_BG) INTRO_BG=buildIntroWalk(); if(!INTRO_KEY) INTRO_KEY=buildIntroKey(); if(!INTRO_SHOP) INTRO_SHOP=buildIntroShop(); if(!CITY_DUSK) CITY_DUSK=buildCity('dusk');\n"
    "  playReel(INTRO,toNameScene); }\n"
    "function introTyped(){ const s=S.reel[S.introN].text; return Math.min(s.length,Math.max(0,Math.floor((S.introT-0.7)*18))); }\n"
    "function introClick(){\n"
    "  const s=S.reel[S.introN].text;\n"
    "  if(introTyped()<s.length){ S.introT=99; return; }          /* first click finishes the line */\n"
    "  if(S.introN<S.reel.length-1){ S.introN++; S.introT=0; Snd.ui(); } else S.reelEnd();\n"
    "}")
rep("""  g.globalAlpha=fade; g.imageSmoothingEnabled=false;
  if(n===0) g.drawImage(CITY_DUSK,ix,iy,iw,ih);
  else if(n===1){
    g.drawImage(INTRO_BG,ix,iy,iw,ih);
    const wx=14+Math.min(84,S.introT*7), f=Math.floor(S.introT*4)%2, bob=f?0:1;   /* a figure walks toward the light */
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-40,iy+64*4-3,86,4);
    blit(WALK_PX[f],ix+wx*4,iy+64*4-26*5-bob*5,5);
  }
  else if(n===2) g.drawImage(INTRO_KEY,ix,iy,iw,ih);
  else g.drawImage(INTRO_SHOP,ix,iy,iw,ih);                            /* the shop, open, nobody in yet */
  g.globalAlpha=1;""",
"""  g.globalAlpha=fade; g.imageSmoothingEnabled=false;
  const card=S.reel[n];
  if(card.draw) card.draw(ix,iy,iw,ih); else g.drawImage(reelImg(card.img),ix,iy,iw,ih);
  if(card.flash&&Math.sin(S.t*7)>0.985){ g.fillStyle='rgba(255,240,200,0.35)'; g.fillRect(ix,iy,iw,ih); }   /* lightning */
  g.globalAlpha=1;""")
rep("  const s=INTRO[n].text, k=introTyped(), shown=s.slice(0,k), cur=(k<s.length||Math.sin(S.t*8)>0)?'_':' ';\n"
    "  txt(shown+cur,W/2,iy+ih+80,22,n===0?C.gold:C.ink,'center');\n"
    "  for(let i=0;i<INTRO.length;i++){ g.fillStyle=i===n?C.gold:'#3a3228'; g.fillRect(W/2-30+i*16,iy+ih+130,10,6); }\n"
    "  if(k>=s.length) txt('click to go on',W/2,iy+ih+170,11,C.dimmer,'center','normal');\n"
    "  button(W-140,20,120,36,'SKIP',()=>toNameScene(),C.dim,12);",
    "  const s=card.text, k=introTyped(), shown=s.slice(0,k), cur=(k<s.length||Math.sin(S.t*8)>0)?'_':' ';\n"
    "  txt(shown+cur,W/2,iy+ih+80,txtw(s,22)>W-80?16:22,card.gold?C.gold:C.ink,'center');\n"
    "  for(let i=0;i<S.reel.length;i++){ g.fillStyle=i===n?C.gold:'#3a3228'; g.fillRect(W/2-(S.reel.length*16)/2+i*16,iy+ih+130,10,6); }\n"
    "  if(k>=s.length) txt('click to go on',W/2,iy+ih+170,11,C.dimmer,'center','normal');\n"
    "  button(W-140,20,120,36,'SKIP',()=>S.reelEnd(),C.dim,12);")
rep("  if(S.scene==='intro'){ if(ev.key==='Escape') toNameScene(); else if","  if(S.scene==='intro'){ if(ev.key==='Escape') S.reelEnd(); else if")
rep("  if(S.day===2) S.fixerFresh=true;                             /* the first morning the Fixer can be visited */\n"
    "  if(books){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub();",
    "  if(S.day===2) S.fixerFresh=true;                             /* the first morning the Fixer can be visited */\n"
    "  const go=()=>{ if(books){ S.scene='ledger'; S.sceneT=0; saveGame(); } else toHub(); };\n"
    "  if(S.day===9) playReel(REEL9,go); else if(S.day===RIG_DAY) playReel(REEL15,go); else go();   /* a few frames of story on the way into town */")

# ---- 6. the streak dies at dusk ----
rep("  S.caps-=rent+wage;\n  AST.bestDay=","  S.caps-=rent+wage;\n  S.combo=0;                                              /* yesterday's streak is not today's */\n  AST.bestDay=")

# ---- 7. materials 15% cheaper ----
s0=src.index("const MATS=["); s1=src.index("];",s0); block=src[s0:s1]
block2=re.sub(r"c:(\d+),",lambda m:"c:%d,"%round(int(m.group(1))*0.85),block); assert block2!=block
src=src[:s0]+block2+src[s1:]; n+=1
# ---- 8. Strider parts 25% cheaper ----
for a,b in [("cost:3000","cost:2250"),("cost:4000","cost:3000"),("cost:2500, d:'Nobody","cost:1875, d:'Nobody"),("cost:2000, d:'An armoured","cost:1500, d:'An armoured")]: rep(a,b)

# ---- 9. the day's last buyer asks for something in stock ----
rep("function spawnCustomer(){\n  let freeRow;\n  for(let i=0;i<queueRows();i++) if(!S.custs.some(c=>c.row===i)){ freeRow=i; break; }\n  if(freeRow===undefined) return;",
    "function spawnCustomer(last){\n  let freeRow;\n  for(let i=0;i<queueRows();i++) if(!S.custs.some(c=>c.row===i)){ freeRow=i; break; }\n  if(freeRow===undefined) return;\n"
    "  if(last){                                                  /* the day's last buyer asks for a piece you actually have */\n"
    "    const stock=[]; S.shelves.forEach(sh=>sh.slots.forEach(e=>{ if(e&&!e.arriving) stock.push(e.item); })); (S.counter||[]).forEach(e=>{ if(e&&!e.arriving) stock.push(e.item); });\n"
    "    if(stock.length){ const it=pick(stock), b=it.base||it, cat=b.cat;\n"
    "      const pool=TYPES.filter(t=>t.tier<=tierFor(S.day)), fit=pool.filter(t=>t.wants.indexOf(cat)>=0), t=pick(fit.length?fit:pool), pm=patScale(S.day);\n"
    "      S.lastWantCat=cat;\n"
    "      S.custs.push({type:t,row:freeRow,want:{kind:'item',item:b,cat:cat},pat:t.pat*pm,patMax:t.pat*pm,\n"
    "        x:W+60,y:custRect(freeRow).y,state:'walk',st:0,bob:Math.random()*6,mood:0,line:pick(t.hello),lineT:2.8,shakeT:0,last:true});\n"
    "      return; } }")
rep("    if(S.nextCust<=0){ S.nextCust=custEvery(S.day)*rnd(0.8,1.2); spawnCustomer(); }",
    "    if(S.nextCust<=0){ S.nextCust=custEvery(S.day)*rnd(0.8,1.2); spawnCustomer(S.dayTime+S.nextCust>=S.dayLen); }   /* the last one of the day is told so */")
open(P,'w').write(src); print('applied',n)
