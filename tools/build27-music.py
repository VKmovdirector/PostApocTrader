#!/usr/bin/env python3
"""Build 27: the tape - an 83 s loop cut from the user's track, embedded as AAC; MUSIC in settings cycles OFF / CHIP LOOP / DUST TAPE."""
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("build 26: cut scenes, adaptability, robo-hand lvl 2, last buyer wants stock","build 27: Quick Trade in the game, the tape")
rep("  txt('build 26',W-20,H-18,10,C.dimmer,'right','normal');","  txt('build 27',W-20,H-18,10,C.dimmer,'right','normal');")
rep("const OPT={sound:true, vol:2, shake:true, tutorials:true, music:true};",
    "const OPT={sound:true, vol:2, shake:true, tutorials:true, music:'tape'};      /* music: 'off' | 'chip' (the made-up loop) | 'tape' (the recorded track) */")
rep("try{ Object.assign(OPT,JSON.parse(localStorage.getItem('rustrations.opts')||'{}')); }catch(e){}",
    "try{ Object.assign(OPT,JSON.parse(localStorage.getItem('rustrations.opts')||'{}')); }catch(e){}\n"
    "if(OPT.music===true) OPT.music='tape'; else if(OPT.music===false) OPT.music='off';   /* build 25 saved a yes/no */")
# the Music object: modes
rep("  on:false, ctx:null, master:null, lead:null, next:0, step:0, timer:null, chordOn:null,",
    "  on:false, cur:'off', ctx:null, master:null, lead:null, next:0, step:0, timer:null, chordOn:null, buf:null, src:null, loading:false,")
rep("  vol(){ return 0.16*(Snd.vol||1); },\n"
    "  apply(){\n"
    "    const want=!!(OPT.music&&OPT.sound&&Snd.ctx);\n"
    "    if(want&&!this.on) this.start();\n"
    "    else if(!want&&this.on) this.stop();\n"
    "    else if(this.on&&this.master) this.master.gain.setTargetAtTime(this.vol(),this.ctx.currentTime,0.1);\n"
    "  },\n"
    "  start(){\n"
    "    const c=Snd.ctx; if(!c) return; this.ctx=c; this.on=true;\n"
    "    this.master=c.createGain(); this.master.gain.setValueAtTime(0.0001,c.currentTime);\n"
    "    this.master.gain.exponentialRampToValueAtTime(this.vol(),c.currentTime+2); this.master.connect(c.destination);\n",
    "  vol(){ return (this.cur==='tape'?0.30:0.16)*(Snd.vol||1); },\n"
    "  apply(){\n"
    "    const want=(OPT.sound&&Snd.ctx)?(OPT.music||'off'):'off';\n"
    "    if(want!==this.cur){ if(this.on) this.stop(); if(want!=='off') this.start(want); this.cur=want; }\n"
    "    else if(this.on&&this.master) this.master.gain.setTargetAtTime(this.vol(),this.ctx.currentTime,0.1);\n"
    "  },\n"
    "  start(kind){\n"
    "    const c=Snd.ctx; if(!c) return; this.ctx=c; this.on=true; this.cur=kind;\n"
    "    this.master=c.createGain(); this.master.gain.setValueAtTime(0.0001,c.currentTime);\n"
    "    this.master.gain.exponentialRampToValueAtTime(this.vol(),c.currentTime+2); this.master.connect(c.destination);\n"
    "    if(kind==='tape'){ this.startTape(); return; }\n")
rep("  stop(){\n    this.on=false; clearInterval(this.timer); this.timer=null;",
    "  /* the tape: decoded once, then a looping buffer source - no gap at the seam */\n"
    "  startTape(){\n"
    "    const c=this.ctx, m=this.master, go=()=>{ if(!this.on||this.cur!=='tape'||this.master!==m) return;\n"
    "      const s=c.createBufferSource(); s.buffer=this.buf; s.loop=true; s.connect(m); s.start(); this.src=s; };\n"
    "    if(this.buf){ go(); return; }\n"
    "    if(this.loading||typeof MUSIC_TRACK==='undefined') return; this.loading=true;\n"
    "    fetch(MUSIC_TRACK).then(r=>r.arrayBuffer()).then(b=>c.decodeAudioData(b)).then(buf=>{ this.buf=buf; this.loading=false; go(); }).catch(()=>{ this.loading=false; });\n"
    "  },\n"
    "  stop(){\n    this.on=false; this.cur='off'; clearInterval(this.timer); this.timer=null;\n"
    "    if(this.src){ try{ this.src.stop(this.ctx.currentTime+1); }catch(e){} this.src=null; }")
rep("  toggleRow(p.x,r(1),p.w,'MUSIC',OPT.music?'ON':'OFF',()=>{ OPT.music=!OPT.music; optSave(); },'a slow loop under the day');",
    "  toggleRow(p.x,r(1),p.w,'MUSIC',{off:'OFF',chip:'CHIP LOOP',tape:'DUST TAPE'}[OPT.music]||'OFF',()=>{ OPT.music={off:'chip',chip:'tape',tape:'off'}[OPT.music]||'chip'; optSave(); },'the tape is the recorded track; the chip loop is made on the spot');")
# the tape itself, as its own script block before the game script
b64=open('audio/dust-tape-loop.b64').read().strip()
rep('<body><canvas id="c"></canvas>\n<script>',
    '<body><canvas id="c"></canvas>\n<script>/* the tape: an 83 s loop, AAC in an MP4 box, decoded once on the first click */\nconst MUSIC_TRACK="data:audio/mp4;base64,'+b64+'";</script>\n<script>')
open(P,'w').write(src); print('applied',n,'size',len(src))
