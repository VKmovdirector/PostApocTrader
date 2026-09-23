#!/usr/bin/env python3
"""Build 24b: a caravan rests after unloading, longer the heavier it was; nothing lands during the rest."""
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("const CRATE_GAP=15;                                   /* seconds: a caravan this soon after the last one is a light one */\n"
    "function sinceCrate(){ return S.dayTime-(S.lastCrateT===undefined?-99:S.lastCrateT); }\n"
    "function spawnCrate(big){\n  const lo=crateLo(S.day), hi=crateSize(S.day); let n=big ? ri(lo,hi)*2 : ri(lo,hi); const items=[];\n"
    "  if(!big&&sinceCrate()<CRATE_GAP) n=Math.min(n,3);\n  S.lastCrateT=S.dayTime;",
    "/* after a crate is unloaded the road rests: 2 s per piece, 6 s at least (3 pieces 6 s, 6 pieces 12 s, the big 12 pieces 24 s) */\n"
    "function crateRestFor(n){ return Math.max(6,2*n); }\n"
    "function crateResting(){ return S.dayTime<(S.crateRest||0); }\n"
    "function spawnCrate(big){\n  const lo=crateLo(S.day), hi=crateSize(S.day), n=big ? ri(lo,hi)*2 : ri(lo,hi), items=[];")
rep("    if(S.nextCrate<=0){ S.nextCrate=crateEvery(S.day); S.crateDue=(S.crateDue||0)+1; }     /* due - but it waits its turn */",
    "    if(S.nextCrate<=0){ S.nextCrate=crateEvery(S.day); S.crateDue=1; }                    /* due - but it waits its turn, and never queues up */")
rep("  if(!S.crates.length&&!S.closing&&!tutFrozen()){\n"
    "    if(S.bigDue){ if(sinceCrate()>=CRATE_GAP){ S.bigDue=false; spawnCrate(true); } }   /* the big load never lands on the heels of another */\n"
    "    else if(S.crateDue>0){ S.crateDue--; spawnCrate(false); }",
    "  if(!S.crates.length&&!S.closing&&!tutFrozen()&&!crateResting()){                 /* nothing lands while the road rests */\n"
    "    if(S.bigDue){ S.bigDue=false; spawnCrate(true); }\n"
    "    else if(S.crateDue>0){ S.crateDue--; spawnCrate(false); }")
rep("        else cr.state='out';","        else { cr.state='out'; S.crateRest=S.dayTime+crateRestFor(cr.n); }   /* unloaded: the rest starts now */")
rep("  S.crateDue=0; S.bigDue=false; S.lastCrateT=-99; S.keyFx=[];","  S.crateDue=0; S.bigDue=false; S.crateRest=0; S.keyFx=[];")
rep("  const ce=crateEvery(S.day), tleft=Math.max(0,S.nextCrate);\n"
    "  txt('NEXT CARAVAN',hr.x+12,hr.y+15,11,C.dim);\n"
    "  txt(S.closing?'closed':(S.crates.length?'unloading...':((S.crateDue>0||S.bigDue)?'at the gate':'in '+Math.ceil(tleft)+'s')),hr.x+hr.w-12,hr.y+15,11,S.crates.length?C.gold:C.dimmer,'right','normal');\n"
    "  bar(hr.x+12,hr.y+25,hr.w-24,11,S.closing?0:1-tleft/ce,C.gold);",
    "  const ce=crateEvery(S.day), rest=Math.max(0,(S.crateRest||0)-S.dayTime), due=S.crateDue>0||S.bigDue, tleft=due?rest:Math.max(0,S.nextCrate,rest);\n"
    "  txt('NEXT CARAVAN',hr.x+12,hr.y+15,11,C.dim);\n"
    "  txt(S.closing?'closed':(S.crates.length?'unloading...':(due?(rest>0?'on the road · '+Math.ceil(rest)+'s':'at the gate'):'in '+Math.ceil(tleft)+'s')),hr.x+hr.w-12,hr.y+15,11,S.crates.length?C.gold:C.dimmer,'right','normal');\n"
    "  bar(hr.x+12,hr.y+25,hr.w-24,11,S.closing?0:1-Math.min(1,tleft/ce),C.gold);")
open(P,'w').write(src); print('applied',n)
