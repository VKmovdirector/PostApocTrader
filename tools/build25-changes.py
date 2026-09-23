#!/usr/bin/env python3
"""Build 25: 20% fewer goods off the road (caravan timer), and a music loop with a MUSIC switch in settings."""
import sys
P='index.html'; src=open(P).read(); n=0
def rep(a,b):
    global src,n
    if src.count(a)!=1: print('ANCHOR FAIL',src.count(a),a[:160]); sys.exit(1)
    src=src.replace(a,b); n+=1
rep("build 24: workshop counter, one-per-craft, Transport from day 15","build 25: music loop, 20% fewer goods off the road")
rep("  txt('build 24',W-20,H-18,10,C.dimmer,'right','normal');","  txt('build 25',W-20,H-18,10,C.dimmer,'right','normal');")
# 1. fewer goods: the caravan timer stretches (tuned by the bot so items per day drop 20%)
rep("const crateEvery = d => Math.max(8.6, 14-0.6*(d-1));                  /* flat from day 10 */",
    "let CRATE_RATE=1.25;                                                    /* build 25: the road is 20% slower */\n"
    "const crateEvery = d => Math.max(8.6, 14-0.6*(d-1))*CRATE_RATE;       /* flat from day 10 */")
# 2. music
rep("  init(){ if(!this.ctx){ try{ this.ctx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} } },",
    "  init(){ if(!this.ctx){ try{ this.ctx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){} }\n"
    "    if(this.ctx&&this.ctx.state==='suspended'){ try{ this.ctx.resume(); }catch(e){} }\n"
    "    if(typeof Music!=='undefined') Music.apply(); },")
rep("const OPT={sound:true, vol:2, shake:true, tutorials:true};",
    r"""/* ================================================================
   MUSIC  -  one slow loop, made on the spot: a walking bass, a thin pad, a plucked
   lead in A minor with a little echo, and a dry kick and shaker. 84 bpm, 8 bars.
   ================================================================ */
const Music={
  on:false, ctx:null, master:null, lead:null, next:0, step:0, timer:null, chordOn:null,
  BPM:84, STEPS:128,
  ROOTS:[110,87.31,130.81,98],                                     /* Am  F  C  G, two bars each */
  CHORDS:[[220,261.63,329.63],[174.61,220,261.63],[261.63,329.63,392],[196,246.94,293.66]],
  MEL:(function(){ const A4=440,C5=523.25,D5=587.33,E5=659.25,G5=783.99,G4=392,_=0;
    return [A4,_,_,_,C5,_,_,_,D5,_,_,_,_,_,_,_, E5,_,_,_,_,_,D5,_,C5,_,_,_,A4,_,_,_,
            A4,_,_,_,_,_,_,_,C5,_,_,_,E5,_,_,_, D5,_,_,_,C5,_,_,_,A4,_,_,_,_,_,_,_,
            E5,_,_,_,_,_,_,_,G5,_,_,_,E5,_,_,_, D5,_,_,_,C5,_,_,_,_,_,_,_,_,_,_,_,
            D5,_,_,_,_,_,_,_,G4,_,_,_,A4,_,_,_, _,_,_,_,_,_,_,_,C5,_,_,_,_,_,_,_]; })(),
  vol(){ return 0.16*(Snd.vol||1); },
  apply(){
    const want=!!(OPT.music&&OPT.sound&&Snd.ctx);
    if(want&&!this.on) this.start();
    else if(!want&&this.on) this.stop();
    else if(this.on&&this.master) this.master.gain.setTargetAtTime(this.vol(),this.ctx.currentTime,0.1);
  },
  start(){
    const c=Snd.ctx; if(!c) return; this.ctx=c; this.on=true;
    this.master=c.createGain(); this.master.gain.setValueAtTime(0.0001,c.currentTime);
    this.master.gain.exponentialRampToValueAtTime(this.vol(),c.currentTime+2); this.master.connect(c.destination);
    const lf=c.createBiquadFilter(); lf.type='lowpass'; lf.frequency.value=1600; lf.connect(this.master);
    const dl=c.createDelay(1); dl.delayTime.value=60/this.BPM*0.75; const fb=c.createGain(); fb.gain.value=0.3;
    dl.connect(fb); fb.connect(dl); dl.connect(this.master); lf.connect(dl);
    this.lead=lf;
    this.next=c.currentTime+0.1; this.step=0; this.chordOn=null;
    this.timer=setInterval(()=>this.sched(),110);
  },
  stop(){
    this.on=false; clearInterval(this.timer); this.timer=null;
    if(this.master){ const m=this.master, c=this.ctx; m.gain.setTargetAtTime(0.0001,c.currentTime,0.25); setTimeout(()=>{ try{ m.disconnect(); }catch(e){} },1200); }
    if(this.chordOn){ this.chordOn.forEach(o=>{ try{ o.stop(this.ctx.currentTime+1); }catch(e){} }); this.chordOn=null; }
    this.master=null;
  },
  sched(){
    if(!this.on) return;
    const c=this.ctx, dt=60/this.BPM/4;
    while(this.next<c.currentTime+0.35){ this.play(this.step,this.next); this.step=(this.step+1)%this.STEPS; this.next+=dt; }
  },
  osc(type,f,t,dur,vol,dest,f2){
    const c=this.ctx, o=c.createOscillator(), g2=c.createGain();
    o.type=type; o.frequency.setValueAtTime(f,t); if(f2) o.frequency.exponentialRampToValueAtTime(f2,t+dur);
    g2.gain.setValueAtTime(0.0001,t); g2.gain.exponentialRampToValueAtTime(vol,t+0.015); g2.gain.exponentialRampToValueAtTime(0.0001,t+dur);
    o.connect(g2); g2.connect(dest||this.master); o.start(t); o.stop(t+dur+0.05); return o;
  },
  noise(t,dur,vol,hp){
    const c=this.ctx, n=Math.floor(c.sampleRate*dur), b=c.createBuffer(1,n,c.sampleRate), d=b.getChannelData(0);
    for(let i=0;i<n;i++) d[i]=(Math.random()*2-1)*(1-i/n);
    const s=c.createBufferSource(); s.buffer=b; const f=c.createBiquadFilter(); f.type=hp?'highpass':'bandpass'; f.frequency.value=hp||1800;
    const g2=c.createGain(); g2.gain.value=vol; s.connect(f); f.connect(g2); g2.connect(this.master); s.start(t);
  },
  play(step,t){
    const bar=Math.floor(step/16), b16=step%16, ch=Math.floor(bar/2)%4, dt=60/this.BPM/4;
    if(b16===0&&bar%2===0){                                                   /* the pad changes with the chord */
      if(this.chordOn) this.chordOn.forEach(o=>{ try{ o.stop(t+0.6); }catch(e){} });
      this.chordOn=this.CHORDS[ch].map((f,i)=>{
        const c=this.ctx, o=c.createOscillator(), g2=c.createGain(), lp=c.createBiquadFilter();
        o.type='sawtooth'; o.frequency.value=f; o.detune.value=(i-1)*6; lp.type='lowpass'; lp.frequency.value=520;
        g2.gain.setValueAtTime(0.0001,t); g2.gain.exponentialRampToValueAtTime(0.028,t+0.9); g2.gain.setTargetAtTime(0.0001,t+dt*30,0.5);
        o.connect(lp); lp.connect(g2); g2.connect(this.master); o.start(t); o.stop(t+dt*32+1); return o; });
    }
    const root=this.ROOTS[ch];
    if(b16===0||b16===8) this.osc('triangle',root,t,dt*6,0.30);            /* bass */
    if(b16===12&&bar%2===1) this.osc('triangle',root*1.5,t,dt*3,0.18);
    if(b16===0||b16===10) this.osc('sine',110,t,0.22,0.55,null,38);         /* kick */
    if(b16===8) this.noise(t,0.14,0.12);                                    /* snare-ish */
    if(b16%4===2) this.noise(t,0.05,0.05,7000);                             /* shaker */
    const m=this.MEL[step%64]; if(m) this.osc('square',m,t,dt*3.2,0.06,this.lead);
  }
};
const OPT={sound:true, vol:2, shake:true, tutorials:true, music:true};""")
rep("function optSave(){ try{ localStorage.setItem('rustrations.opts',JSON.stringify(OPT)); }catch(e){} Snd.on=OPT.sound; Snd.vol=[0,0.5,1,1.6][OPT.vol]; }",
    "function optSave(){ try{ localStorage.setItem('rustrations.opts',JSON.stringify(OPT)); }catch(e){} Snd.on=OPT.sound; Snd.vol=[0,0.5,1,1.6][OPT.vol]; Music.apply(); }")
rep("  const p=pageFrame('SETTINGS','sound, screen and game',7), r=i=>p.y+i*60;\n"
    "  toggleRow(p.x,r(0),p.w,'SOUND',OPT.sound?'ON':'OFF',()=>{ OPT.sound=!OPT.sound; optSave(); },'M also mutes');\n"
    "  toggleRow(p.x,r(1),p.w,'VOLUME',['MUTE','QUIET','NORMAL','LOUD'][OPT.vol],()=>{ OPT.vol=(OPT.vol%3)+1; optSave(); Snd.ui(); });\n"
    "  toggleRow(p.x,r(2),p.w,'FULL SCREEN',",
    "  const p=pageFrame('SETTINGS','sound, screen and game',8), r=i=>p.y+i*60;\n"
    "  toggleRow(p.x,r(0),p.w,'SOUND',OPT.sound?'ON':'OFF',()=>{ OPT.sound=!OPT.sound; optSave(); },'M also mutes');\n"
    "  toggleRow(p.x,r(1),p.w,'MUSIC',OPT.music?'ON':'OFF',()=>{ OPT.music=!OPT.music; optSave(); },'a slow loop under the day');\n"
    "  toggleRow(p.x,r(2),p.w,'VOLUME',['MUTE','QUIET','NORMAL','LOUD'][OPT.vol],()=>{ OPT.vol=(OPT.vol%3)+1; optSave(); Snd.ui(); });\n"
    "  toggleRow(p.x,r(3),p.w,'FULL SCREEN',")
rep("  toggleRow(p.x,r(3),p.w,'SCREEN SHAKE',","  toggleRow(p.x,r(4),p.w,'SCREEN SHAKE',")
rep("  toggleRow(p.x,r(4),p.w,'TUTORIALS',","  toggleRow(p.x,r(5),p.w,'TUTORIALS',")
rep("  toggleRow(p.x,r(5),p.w,'ERASE ALL SAVED GAMES',","  toggleRow(p.x,r(6),p.w,'ERASE ALL SAVED GAMES',")
rep("  toggleRow(p.x,r(6),p.w,'RESET ACHIEVEMENTS',","  toggleRow(p.x,r(7),p.w,'RESET ACHIEVEMENTS',")
open(P,'w').write(src); print('applied',n)
