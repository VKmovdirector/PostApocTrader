/* ================================================================
   FRONT END  -  title screen, save slots, options, settings, ESC menu
   ================================================================ */
const OPT={sound:true, vol:2, shake:true, tutorials:true};
try{ Object.assign(OPT,JSON.parse(localStorage.getItem('rustrations.opts')||'{}')); }catch(e){}
function optSave(){ try{ localStorage.setItem('rustrations.opts',JSON.stringify(OPT)); }catch(e){} Snd.on=OPT.sound; Snd.vol=[0,0.5,1,1.6][OPT.vol]; }
Snd.on=OPT.sound; Snd.vol=[0,0.5,1,1.6][OPT.vol];

/* ---------- saves: three slots, written every time you reach the town page ---------- */
const SLOTS=3;
const iref=it=>it?[it.base.id,it.r||0,it.crafted?1:0]:null;
const ideref=a=>a?rar(ITEMBY[a[0]],a[1],!!a[2]):null;
function slotKey(n){ return 'rustrations.slot'+n; }
function slotPeek(n){ try{ return JSON.parse(localStorage.getItem(slotKey(n))||'null'); }catch(e){ return null; } }
function slotErase(n){ try{ localStorage.removeItem(slotKey(n)); }catch(e){} }
function saveGame(){
  if(!S.slot) return;
  const d={v:1,t:Date.now(),day:S.day,caps:S.caps,up:S.up,hire:S.hire,actOwn:S.actOwn,wb:S.wb,wbDay:S.wbDay,unl:S.unl,mats:S.mats,
    rig:S.rig,history:S.history,cr:S.cr,maxCombo:S.maxCombo,cslots:S.cslots,rows:S.rows,tut:TUT.done,wt:WT.done,
    tray:S.tray.map(iref), anvil:iref(S.anvil),
    shelves:S.shelves.map(sh=>({cat:sh.cat,slots:sh.slots.map(e=>e?{i:iref(e.item),m:e.misfiled?1:0}:null)})),
    counter:(S.counter||[]).map(e=>e?iref(e.item):null)};
  try{ localStorage.setItem(slotKey(S.slot),JSON.stringify(d)); }catch(e){}
}
function loadGame(n){
  const d=slotPeek(n); if(!d) return false;
  startRun(); S.slot=n;
  ['day','caps','hire','actOwn','wb','wbDay','unl','mats','rig','history','cr','maxCombo','cslots','rows'].forEach(k=>{ if(d[k]!==undefined) S[k]=d[k]; });
  Object.assign(S.up,d.up||{}); while(S.actOwn.length<ACTIVES.length) S.actOwn.push(false);
  TUT.done=d.tut||{}; TUT.active=null; WT.done=!!d.wt; WT.on=false;
  S.tray=(d.tray||[]).map(ideref); while(S.tray.length<17) S.tray.push(null); S.anvil=ideref(d.anvil);
  S.shelves=(d.shelves||[]).map(sh=>({cat:sh.cat,slots:sh.slots.map(e=>e?{item:ideref(e.i),misfiled:!!e.m,arriving:0,anim:0}:null)}));
  S.counter=(d.counter||[]).map(a=>a?{item:ideref(a),arriving:0,anim:0,misfiled:false}:null);
  TRADER_KEY=''; S.fresh=false; S.paused=false; S.esc=false; S.scene='hub'; S.sceneT=0;
  return true;
}
function newGame(n){ slotErase(n); S.slotPick=n; S.scene='howto'; S.sceneT=0; }
function beginRun(){                                   /* OK on the how-to card: straight into day 1 and its lesson */
  startRun(); S.slot=S.slotPick||1; S.fresh=false; S.paused=false; S.esc=false;
  S.scene='play'; S.sceneT=0; say('Another day.');
}
function toTitle(){ S.paused=false; S.esc=false; S.drag=null; S.traderLineT=0; S.banner=null; S.scene='title'; S.sceneT=0; }

/* ---------- title ---------- */
function menuList(x,y,w,items){
  items.forEach((it,i)=>{
    const by=y+i*62, on=it.on!==false, hov=on&&inRect(MX,MY,{x:x,y:by,w:w,h:52});
    plate(x,by,w,52,hov?'#3e3125':'#1d1712',hov?C.gold:(on?'#6b5540':'#33291f'));
    if(hov){ g.fillStyle=C.gold; g.fillRect(x+16,by+22,10,8); }
    txt(it.n,x+w/2,by+26,18,on?(hov?C.ink:C.gold):C.dimmer,'center');
    if(it.sub) txt(it.sub,x+w/2,by+43,8,C.dimmer,'center','normal');
    if(on) BTNS.push({x:x,y:by,w:w,h:52,fn:it.fn});
  });
}
function anySave(){ for(let n=1;n<=SLOTS;n++) if(slotPeek(n)) return true; return false; }
function drawTitle(){
  g.fillStyle='rgba(8,5,4,0.55)'; g.fillRect(0,0,W,H);
  const gr=g.createLinearGradient(0,0,0,H); gr.addColorStop(0,'rgba(8,5,4,0.75)'); gr.addColorStop(0.45,'rgba(8,5,4,0)'); gr.addColorStop(1,'rgba(8,5,4,0.85)');
  g.fillStyle=gr; g.fillRect(0,0,W,H);
  for(let i=0;i<26;i++){ const px2=((i*173+S.t*(18+i%7*6))%(W+80))-40, py2=90+((i*97)%560)+Math.sin(S.t*0.7+i)*10;
    g.globalAlpha=0.10+((i*31)%10)/60; g.fillStyle='#e8c88a'; g.fillRect(Math.round(px2),Math.round(py2),(i%3)+2,2); } g.globalAlpha=1;
  const lx=W/2, ly=150, bob=Math.round(Math.sin(S.t*1.4)*2);
  txt('RUST & RATIONS',lx+4,ly+4+bob,64,'#120d0a','center'); txt('RUST & RATIONS',lx,ly+bob,64,C.gold,'center');
  g.fillStyle=C.gold; g.fillRect(lx-300,ly+50,600,3); g.fillStyle='#8a6a2a'; g.fillRect(lx-300,ly+53,600,2);
  txt('a trading post at the edge of the dust',lx,ly+78,15,'#d8c8a8','center','normal');
  const has=anySave();
  menuList(W/2-170,290,340,[
    {n:'NEW GAME', fn:()=>{ S.slotMode='new'; S.scene='slots'; S.backScene='title'; S.sceneT=0; }},
    {n:'CONTINUE', on:has, sub:has?null:'no saved game yet', fn:()=>{ S.slotMode='load'; S.scene='slots'; S.backScene='title'; S.sceneT=0; }},
    {n:'SETTINGS', fn:()=>openPage('settings')},
    {n:'EXIT',     fn:()=>{ S.scene='bye'; S.sceneT=0; try{ window.close(); }catch(e){} }}
  ]);
  txt('build 19',W-20,H-18,10,C.dimmer,'right','normal');
  txt('achievements '+achCount()+'/'+ACH.length+'  ·  best run: day '+S.best.day,20,H-18,10,C.dimmer,'left','normal');
}
function drawBye(){
  g.fillStyle='rgba(8,5,4,0.88)'; g.fillRect(0,0,W,H);
  txt('SHUTTERS DOWN',W/2,H/2-40,40,C.gold,'center');
  txt('Your game is saved. You can close this tab.',W/2,H/2+10,14,C.ink,'center','normal');
  button(W/2-140,H/2+60,280,48,'BACK TO THE MENU',()=>toTitle(),C.dim,14);
}
function drawSlots(){
  g.fillStyle='rgba(8,5,4,0.8)'; g.fillRect(0,0,W,H);
  const load=S.slotMode==='load';
  txt(load?'CONTINUE':'NEW GAME',W/2,110,36,C.gold,'center');
  txt(load?'pick a stall to go back to':'pick a slot for the new stall',W/2,150,13,C.dim,'center','normal');
  const cw=340, gap=30, x0=W/2-(cw*3+gap*2)/2;
  for(let n=1;n<=SLOTS;n++){
    const d=slotPeek(n), x=x0+(n-1)*(cw+gap), y=210, h=300, can=load?!!d:true, hov=can&&inRect(MX,MY,{x:x,y:y,w:cw,h:h});
    plate(x,y,cw,h,hov?'#33281c':'#1a1410',hov?C.gold:(can?'#6b5540':'#33291f'));
    txt('SLOT '+n,x+cw/2,y+34,20,can?C.gold:C.dimmer,'center');
    if(d){
      txt('DAY '+d.day,x+cw/2,y+92,34,C.ink,'center');
      txt(d.caps+' chits',x+cw/2,y+134,16,C.gold,'center');
      const perks=Object.values(d.up||{}).reduce((a,b)=>a+b,0)+(d.actOwn||[]).filter(Boolean).length;
      txt(perks+' perks'+(d.wb?'  ·  workbench':'')+'  ·  strider '+Object.values(d.rig||{}).filter(Boolean).length+'/4',x+cw/2,y+166,10,C.dim,'center','normal');
      txt('saved '+new Date(d.t).toLocaleDateString()+'  '+new Date(d.t).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}),x+cw/2,y+188,9,C.dimmer,'center','normal');
    } else txt('EMPTY',x+cw/2,y+110,22,C.dimmer,'center');
    const arm=S.slotArm===n;
    const label = load ? (d?'CONTINUE':'-') : (d?(arm?'SURE? THIS ERASES IT':'OVERWRITE'):'START HERE');
    plate(x+30,y+h-70,cw-60,44,'#241c16',can?(arm?C.red:C.gold):'#33291f');
    txt(label,x+cw/2,y+h-48,arm?11:14,can?(arm?C.red:C.gold):C.dimmer,'center');
    if(can) BTNS.push({x:x,y:y,w:cw,h:h,fn:()=>{
      if(load){ loadGame(n); return; }
      if(d&&!arm){ S.slotArm=n; return; }
      S.slotArm=0; newGame(n);
    }});
  }
  button(W/2-110,560,220,46,'BACK',()=>{ S.slotArm=0; S.scene=S.backScene||'title'; },C.dim,14);
  txt('the game saves by itself every time you reach the town page',W/2,640,10,C.dimmer,'center','normal');
}
function toggleRow(x,y,w,label,value,fn,note){
  plate(x,y,w,54,'#1d1712','#4a3b2c');
  txt(label,x+20,y+(note?21:27),14,C.ink);
  if(note) txt(note,x+20,y+40,9,C.dimmer,'left','normal');
  button(x+w-190,y+9,174,36,value,fn,C.gold,12);
}
function pageFrame(title,sub,rows){
  g.fillStyle='rgba(8,5,4,0.86)'; g.fillRect(0,0,W,H);
  const w=720,h=176+rows*60,x=W/2-w/2,y=Math.max(70,(H-h)/2);
  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');
  txt(title,W/2,y+42,30,C.gold,'center'); txt(sub,W/2,y+74,12,C.dim,'center','normal');
  button(W/2-100,y+h-60,200,44,'BACK',()=>{ S.eraseArm=false; S.achArm=false; closePage(); },C.gold,14);
  return {x:x+40,y:y+100,w:w-80};
}
function drawSettings(){
  const p=pageFrame('SETTINGS','sound, screen and game',7), r=i=>p.y+i*60;
  toggleRow(p.x,r(0),p.w,'SOUND',OPT.sound?'ON':'OFF',()=>{ OPT.sound=!OPT.sound; optSave(); },'M also mutes');
  toggleRow(p.x,r(1),p.w,'VOLUME',['MUTE','QUIET','NORMAL','LOUD'][OPT.vol],()=>{ OPT.vol=(OPT.vol%3)+1; optSave(); Snd.ui(); });
  toggleRow(p.x,r(2),p.w,'FULL SCREEN',document.fullscreenElement?'ON':'OFF',()=>{ try{ if(document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen(); }catch(e){} },'the browser may ask first');
  toggleRow(p.x,r(3),p.w,'SCREEN SHAKE',OPT.shake?'ON':'OFF',()=>{ OPT.shake=!OPT.shake; optSave(); });
  toggleRow(p.x,r(4),p.w,'TUTORIALS',OPT.tutorials?'ON':'OFF',()=>{ OPT.tutorials=!OPT.tutorials; optSave(); },'day 1, bulk orders and the workbench walkthrough');
  toggleRow(p.x,r(5),p.w,'ERASE ALL SAVED GAMES',S.eraseArm?'SURE?':'ERASE',()=>{ if(!S.eraseArm){ S.eraseArm=true; return; } for(let n=1;n<=SLOTS;n++) slotErase(n); S.eraseArm=false; Snd.bad(); },'three slots, gone for good');
  toggleRow(p.x,r(6),p.w,'RESET ACHIEVEMENTS',S.achArm?'SURE?':'RESET',()=>{ if(!S.achArm){ S.achArm=true; return; } for(const k in AST) delete AST[k]; ACH_GOT={}; achSave(); S.achArm=false; Snd.bad(); },achCount()+' of '+ACH.length+' earned');
}
/* ---------- ESC menu: during the day (pauses it) and on the town page ---------- */
function escOpen(){ return (S.scene==='play'&&S.paused)||(S.scene==='hub'&&S.esc); }
function drawEscMenu(){
  BTNS=[];                                             /* nothing underneath is clickable */
  g.fillStyle='rgba(6,4,3,0.72)'; g.fillRect(0,0,W,H);
  const w=420,h=440,x=W/2-w/2,y=H/2-h/2;
  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');
  txt(S.scene==='play'?'PAUSED':'MENU',W/2,y+40,28,C.gold,'center');
  const midDay=S.scene==='play';
  menuList(x+40,y+78,w-80,[
    {n:'CONTINUE',    fn:()=>{ S.paused=false; S.esc=false; }},
    {n:'NEW GAME',    fn:()=>{ S.slotMode='new'; S.backScene=S.scene; S.scene='slots'; S.sceneT=0; }},
    {n:'ACHIEVEMENTS',fn:()=>openPage('ach')},
    {n:'SETTINGS',    fn:()=>openPage('settings')},
    {n:'EXIT',        sub:midDay?'today is not saved - the game saves on the town page':'saved', fn:()=>{ if(!midDay) saveGame(); toTitle(); }}
  ]);
  txt('esc or space resumes',W/2,y+h-16,9,C.dimmer,'center','normal');
}
