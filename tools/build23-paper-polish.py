#!/usr/bin/env python3
"""Build 23 polish: the weather backdrop follows the story, not just up/down."""
import sys
P='index.html'; src=open(P).read()
a="""  if(type==='weather'){
    if(up){ for(let i=0;i<9;i++){ const cx=rn()*96, cy=2+rn()*12, w=10+rn()*16; px(cx,cy,w,4,NP[5]); px(cx+2,cy+4,w-4,2,NP[4]); }
            for(let i=0;i<40;i++){ const sx=rn()*96, sy=6+rn()*30; px(sx,sy,1,4,NP[4]); px(sx-1,sy+4,1,2,NP[4]); } }
    else { for(let dy=-7;dy<=7;dy++){ const w=Math.floor(Math.sqrt(49-dy*dy)); px(70-w,12+dy,w*2+1,1,NP[0]); }
           for(let r=0;r<5;r++){ const a=-2.6+r*0.55; for(let k=10;k<30;k+=2) px(70+Math.cos(a)*k,12+Math.sin(a)*k,1,1,NP[0]); } }"""
b="""  if(type==='weather'){
    const id=ev?ev.id:'', stormy=id==='dust'||id==='acid', cold=id==='cold';      /* the sky follows the story */
    if(stormy){ for(let i=0;i<9;i++){ const cx=rn()*96, cy=2+rn()*12, w=10+rn()*16; px(cx,cy,w,4,NP[5]); px(cx+2,cy+4,w-4,2,NP[4]); }
            for(let i=0;i<40;i++){ const sx=rn()*96, sy=6+rn()*30; px(sx,sy,1,4,NP[4]); px(sx-1,sy+4,1,2,NP[4]); } }
    else if(cold){ for(let dy=-4;dy<=4;dy++){ const w=Math.floor(Math.sqrt(16-dy*dy)); px(74-w,10+dy,w*2+1,1,NP[1]); }
            for(let i=0;i<50;i++) px(rn()*96,2+rn()*36,1,1,NP[0]); }
    else { const R=up?9:7; for(let dy=-R;dy<=R;dy++){ const w=Math.floor(Math.sqrt(R*R-dy*dy)); px(70-w,12+dy,w*2+1,1,NP[0]); }
           for(let r=0;r<7;r++){ const a=-2.9+r*0.5; for(let k=R+3;k<34;k+=2) px(70+Math.cos(a)*k,12+Math.sin(a)*k,1,1,NP[0]); } }"""
if src.count(a)!=1: print('ANCHOR FAIL'); sys.exit(1)
src=src.replace(a,b); open(P,'w').write(src); print('applied')
