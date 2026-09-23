#!/usr/bin/env python3
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("let CRATE_RATE=1.25;                                                    /* build 25: the road is 20% slower */",
    "let CRATE_RATE=1.0, CRATE_LOAD=0.8;                                     /* build 25: lighter crates (and a slower road if needed) - tuned by the bot */\n"
    "function crateLoad(d,n){ return Math.max(d<=3?3:2, Math.round(n*CRATE_LOAD)); }   /* what a crate really carries after the cut */")
rep("  const lo=crateLo(S.day), hi=crateSize(S.day), n=big ? ri(lo,hi)*2 : ri(lo,hi), items=[];",
    "  const lo=crateLo(S.day), hi=crateSize(S.day), n=crateLoad(S.day, big ? ri(lo,hi)*2 : ri(lo,hi)), items=[];")
rep("  const clo=crateLo(S.day), chi=crateSize(S.day);",
    "  const clo=crateLoad(S.day,crateLo(S.day)), chi=crateLoad(S.day,crateSize(S.day));")
open(P,'w').write(src); print('applied',n)
