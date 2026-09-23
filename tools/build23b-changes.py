#!/usr/bin/env python3
"""Build 23b: no seam at the frame edge, the town page is a full-window page, THE FIXER marked NEW on day 2."""
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
# 1. the side strips slide 8px under the scene so no seam can show at a fractional scale
rep("  if(EXX>0){ g.drawImage(SCENE_EDGE,0,0,1,190,-EXX-16,0,EXX+16,H); g.drawImage(SCENE_EDGE,0,0,1,190,W,0,EXX+16,H); }",
    "  if(EXX>0){ g.drawImage(SCENE_EDGE,0,0,1,190,-EXX-16,0,EXX+24,H); g.drawImage(SCENE_EDGE,0,0,1,190,W-8,0,EXX+24,H); }   /* tucked 8px under the scene: no seam */")
# 2. the town page fills the window; nothing shows through
rep("function drawHub(){\n  dim(0.8);\n  const x=70,y=78,w=W-140,h=H-98;\n  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');",
    "function newTab(x,y,w,h){ const p=Math.sin(S.t*6)>-0.2;                                  /* the blinking NEW tab and gold frame on a door */\n"
    "  g.fillStyle=p?C.red:'#7a2f22'; g.fillRect(x+w-52,y-8,58,20); txt('NEW',x+w-23,y+2,11,'#fff0d8','center');\n"
    "  g.strokeStyle=C.gold; g.lineWidth=3; if(p) g.strokeRect(x-3,y-3,w+6,h+6); }\n"
    "function drawHub(){\n"
    "  { const r=fullRect(); plate(r.x,r.y,r.w,r.h,'#1a1410','#6b5540','#8a6f50'); }        /* a page of its own, edge to edge */\n"
    "  const x=70,y=78,w=W-140,h=H-98;")
# 3. THE FIXER is marked on the first morning it can be visited (day 2)
rep("  door(lx,by,bw,bh,'THE FIXER',()=>{S.scene='shop';S.sceneT=0;},C.gold,15,'fixer');",
    "  door(lx,by,bw,bh,'THE FIXER',()=>{ S.fixerFresh=false; S.scene='shop'; S.sceneT=0; },C.gold,15,'fixer');\n"
    "  if(S.fixerFresh) newTab(lx,by,bw,bh);")
rep("  if(S.looksFresh){ const ly=by+(bh+gp)*3, p=Math.sin(S.t*6)>-0.2;                       /* new stock in the wardrobe */\n"
    "    g.fillStyle=p?C.red:'#7a2f22'; g.fillRect(lx+bw-52,ly-8,58,20); txt('NEW',lx+bw-23,ly+2,11,'#fff0d8','center');\n"
    "    g.strokeStyle=C.gold; g.lineWidth=3; if(p) g.strokeRect(lx-3,ly-3,bw+6,bh+6); }",
    "  if(S.looksFresh) newTab(lx,by+(bh+gp)*3,bw,bh);                                          /* new stock in the wardrobe */")
rep("    if(fresh){ const p=Math.sin(S.t*6)>-0.2;                       /* a fresh paper is hard to miss */\n"
    "      g.fillStyle=p?C.red:'#7a2f22'; g.fillRect(rx+bw-52,hy-8,58,20); txt('NEW',rx+bw-23,hy+2,11,'#fff0d8','center');\n"
    "      g.strokeStyle=C.gold; g.lineWidth=3; if(p) g.strokeRect(rx-3,hy-3,bw+6,bh+6); }",
    "    if(fresh) newTab(rx,hy,bw,bh);                                 /* a fresh paper is hard to miss */")
rep("  if(newLooksOn(S.day).length) S.looksFresh=true;             /* a NEW tab on STALL & LOOKS until it is opened */",
    "  if(newLooksOn(S.day).length) S.looksFresh=true;             /* a NEW tab on STALL & LOOKS until it is opened */\n"
    "  if(S.day===2) S.fixerFresh=true;                             /* the first morning the Fixer can be visited */")
rep("S.evGain=0; S.looksFresh=false;\n","S.evGain=0; S.looksFresh=false; S.fixerFresh=false;\n")
rep("looksFresh:!!S.looksFresh,caps:S.caps,","looksFresh:!!S.looksFresh,fixerFresh:!!S.fixerFresh,caps:S.caps,")
rep("'cslots','rows','looksFresh'].forEach","'cslots','rows','looksFresh','fixerFresh'].forEach")
# the notices at the foot of the page: one line each, stacked
rep("""  { const nl=newLooksOn(S.day);                            /* what came in overnight, at the foot of the page */
    if(nl.length){
      const kinds={hat:'costume',face:'costume',coat:'colour',awning:'colour',lantern:'colour',flag:'colour',pattern:'texture',wall:'texture'}, cnt={};
      nl.forEach(t=>{ const k=kinds[t.cat]||'thing'; cnt[k]=(cnt[k]||0)+1; });
      const parts=Object.keys(cnt).map(k=>cnt[k]+' '+k+(cnt[k]>1?'s':''));
      const msg='NEW AT STALL & LOOKS: '+parts.join(' · '), mw=txtw(msg,14)+40;
      plate(W/2-mw/2,y+h-52,mw,36,'#1d1520',C.purple);
      txt(msg,W/2,y+h-34,14,C.purple,'center');
    } else txt('nothing new at Stall & Looks this morning',W/2,y+h-34,10,C.dimmer,'center','normal'); }""",
"""  { const notes=[];                                         /* what came in overnight, at the foot of the page */
    if(S.day===2) notes.push(['NEW AT THE FIXER: perks and active skills are for sale',C.gold,'#231c10']);
    const nl=newLooksOn(S.day);
    if(nl.length){
      const kinds={hat:'costume',face:'costume',coat:'colour',awning:'colour',lantern:'colour',flag:'colour',pattern:'texture',wall:'texture'}, cnt={};
      nl.forEach(t=>{ const k=kinds[t.cat]||'thing'; cnt[k]=(cnt[k]||0)+1; });
      const parts=Object.keys(cnt).map(k=>cnt[k]+' '+k+(cnt[k]>1?'s':''));
      notes.push(['NEW AT STALL & LOOKS: '+parts.join(' · '),C.purple,'#1d1520']);
    }
    notes.forEach((nt,i)=>{ const mw=txtw(nt[0],14)+40, ny=y+h-52-i*44; plate(W/2-mw/2,ny,mw,36,nt[2],nt[1]); txt(nt[0],W/2,ny+18,14,nt[1],'center'); });
    if(!notes.length) txt('nothing new in town this morning',W/2,y+h-34,10,C.dimmer,'center','normal'); }""")
open(P,'w').write(src); print('applied',n)
