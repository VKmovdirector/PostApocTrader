#!/usr/bin/env python3
"""Build 22 polish: a finer walking silhouette (12x24 at 5x) and outlines on the hand holding the key."""
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL', src.count(a), a[:120]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("""const WALK_PX=[
 ['...kk...','..kkkkk.','...kk...','..kkkk..','.kkkkkk.','.k.kk.k.','.k.kk.k.','...kk...','...kk...','..k..k..','.k....k.','k......k'],
 ['...kk...','..kkkkk.','...kk...','..kkkk..','.kkkkkk.','.k.kk.k.','.k.kk.k.','...kk...','...kk...','...kk...','...kk...','...kk...']
].map(r=>spriteFrom(r,{k:'#120c10'}));""",
"""const WALK_TOP=['....kkkk....','...kkkkkk...','..kkkkkkkk..','....kkkk....','....kkkk....','...kkkkkkk..','..kkkkkkkkk.','.kkkkkkkkkk.',
                '.kk.kkkk.kkk','.kk.kkkk.kkk','.k..kkkk..k.','....kkkk....','....kkkk....','....kkkk....','....kkkk....'];
const WALK_PX=[
 WALK_TOP.concat(['...kkkkkk...','...kkk.kk...','..kkk..kkk..','..kk....kk..','.kkk....kkk.','.kk......kk.','kkk......kkk','kk........kk','kkk......kkk']),
 WALK_TOP.concat(['....kkkk....','....kkkk....','....kkkk....','....kkkk....','....kkkk....','....kkkk....','...kkkkk....','...kkkkk....','..kkk.kkk...'])
].map(r=>spriteFrom(r,{k:'#120c10'}));""")
rep("""    const wx=18+Math.min(78,S.introT*7), f=Math.floor(S.introT*4)%2, bob=f?0:1;   /* a figure walks toward the light */
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-30,iy+62*4,58,3);
    blit(WALK_PX[f],ix+wx*4,iy+(64-12*2)*4-bob*4,8);""",
"""    const wx=14+Math.min(84,S.introT*7), f=Math.floor(S.introT*4)%2, bob=f?0:1;   /* a figure walks toward the light */
    g.fillStyle='rgba(0,0,0,0.35)'; g.fillRect(ix+wx*4-34,iy+64*4-3,70,4);
    blit(WALK_PX[f],ix+wx*4,iy+64*4-24*5-bob*5,5);""")
rep("""  px(52,34,44,34,'#d8ac7c'); px(52,34,44,4,'#e8c090'); px(52,64,44,4,'#b08458');      /* palm */""",
"""  px(51,33,46,36,'#6a4a34');                                                           /* outline */
  px(52,34,44,34,'#d8ac7c'); px(52,34,44,4,'#e8c090'); px(52,64,44,4,'#b08458');      /* palm */""")
rep("""  px(40,40,14,10,'#d8ac7c'); px(38,42,6,8,'#d8ac7c');""",
"""  px(39,39,16,12,'#6a4a34'); px(37,41,8,10,'#6a4a34');
  px(40,40,14,10,'#d8ac7c'); px(38,42,6,8,'#d8ac7c');""")
rep("""    px(f[0],f[1],fw,fh,'#d8ac7c'); px(f[0],f[1],fw,2,'#e8c090');""",
"""    px(f[0]-1,f[1]-1,fw+2,fh+2,'#6a4a34');
    px(f[0],f[1],fw,fh,'#d8ac7c'); px(f[0],f[1],fw,2,'#e8c090');""")
open(P,'w').write(src); print('applied',n)
