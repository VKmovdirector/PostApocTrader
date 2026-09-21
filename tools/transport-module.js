/* ================================================================
   TRANSPORT  -  the yard behind the Fixer. Four parts build THE STRIDER,
   a six-legged walker, and the Strider is how you leave Dustwell.
   (Leaving is not built yet: the other towns are still only on the map.)
   ================================================================ */
const RIG=[
 {id:'engine',n:'TURBINE ENGINE', cost:3000, d:'Pulled from a grounded flyer. Drinks anything that burns.'},
 {id:'legs',  n:'HYDRAULIC LEGS', cost:4000, d:'Six of them, all from different machines. It sits on blocks until they go on.'},
 {id:'gun',   n:'ROOF GUN',       cost:2500, d:'Nobody crosses Cinder Gap unarmed. Nobody who arrives, anyway.'},
 {id:'hold',  n:'CARGO HOLD',     cost:2000, d:'An armoured bay on its back. No point walking nine days to arrive empty.'}
];
function rigCount(){ return RIG.filter(p=>S.rig&&S.rig[p.id]).length; }
function rigDone(){ return rigCount()===RIG.length; }
function buyRig(p){
  if(S.rig[p.id]||S.caps<p.cost){ Snd.bad(); return; }
  S.caps-=p.cost; S.rig[p.id]=true; Snd.coin(6); flash('#8fd0ee',0.22); shake(5);
  if(rigDone()){ S.banner=null; flash(C.gold,0.35); Snd.good(); }
}
const RIG_CACHE={};
function striderCanvas(){
  const key=RIG.map(p=>S.rig[p.id]?1:0).join('');
  if(RIG_CACHE[key]) return RIG_CACHE[key];
  const Wc=176,Hc=100, c=makeCanvas(Wc,Hc), X=c.getContext('2d');
  const layer=(have,fn)=>{            /* a part you own is solid; one you do not is a faint blueprint */
    const t=makeCanvas(Wc,Hc), x=t.getContext('2d');
    const px=(a,b,w,h,col)=>{ x.fillStyle=have?col:'#8fd0ee'; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
    const ln=(x0,y0,x1,y1,th,col)=>{ const n=Math.max(Math.abs(x1-x0),Math.abs(y1-y0)); for(let i=0;i<=n;i++) px(lerp(x0,x1,i/n)-th/2,lerp(y0,y1,i/n)-th/2,th,th,col); };
    fn(px,ln); X.globalAlpha=have?1:0.2; X.drawImage(t,0,0); X.globalAlpha=1;
  };
  const R='#7a5438', RH='#9a7048', RD='#54382a', M='#5a5a58', MH='#8a8a84', MD='#3a3a3a', K='#1a1410';
  /* far legs first, so the hull sits in front of them */
  layer(S.rig.legs,(px,ln)=>{ [[70,56,88],[92,96,98],[114,134,146]].forEach(l=>{ ln(l[0],64,l[1],52,3,MD); ln(l[1],52,l[2],88,3,MD); px(l[2]-3,88,7,2,K); }); });
  /* yard blocks while it cannot stand */
  if(!S.rig.legs) layer(true,(px)=>{ [[58,78],[108,78]].forEach(b=>{ px(b[0],b[1],16,5,'#6b4a2a'); px(b[0]+2,b[1]+5,12,5,'#5a3f28'); px(b[0],b[1]+10,16,4,'#6b4a2a'); px(b[0],b[1],16,1,'#8a6438'); }); });
  /* hull + cockpit: always there, this is the wreck the Fixer dragged in */
  layer(true,(px)=>{
    px(52,50,68,4,RH); px(48,54,76,18,R); px(52,72,68,4,RD); px(56,76,60,2,K);
    for(let i=0;i<7;i++) px(54+i*10,56,1,14,RD);
    for(let i=0;i<8;i++) px(51+i*9,53,2,2,MH);
    px(118,44,20,6,RH); px(116,50,26,20,R); px(120,70,20,4,RD);
    px(124,52,14,10,K); px(125,53,12,8,rigDone()?'#f0c060':'#2a3a44'); px(125,53,12,2,rigDone()?'#fff0b0':'#3f5664');
    px(140,60,4,6,M); px(144,62,3,2,MH);                       /* headlamp */
    px(64,60,10,7,K); px(65,61,8,5,'#3a2a1c');                  /* hatch */
  });
  layer(S.rig.hold,(px)=>{ px(54,34,46,16,'#5a4a3a'); px(54,34,46,2,'#7a6650'); px(54,48,46,2,'#3a2e24');
    [62,76,90].forEach(sx=>px(sx,34,2,16,'#2a2018')); px(58,28,12,6,'#8a6a3a'); px(72,26,14,8,'#6b5a3a'); px(88,29,9,5,'#8a6a3a'); px(72,26,14,1,'#a8865a'); });
  layer(S.rig.engine,(px)=>{ px(30,52,20,20,M); px(30,52,20,2,MH); px(30,70,20,2,MD); px(26,58,4,10,MD);
    for(let i=0;i<4;i++) px(33+i*4,56,2,12,MD);
    px(34,28,5,24,MD); px(42,32,5,20,MD); px(33,26,7,3,MH); px(41,30,7,3,MH); px(35,30,1,20,MH); px(43,34,1,16,MH); px(46,60,6,4,RD); });
  layer(S.rig.gun,(px)=>{ px(100,40,16,10,M); px(102,36,12,4,MH); px(100,48,16,2,MD); px(116,41,26,3,MD); px(116,41,26,1,MH); px(140,40,4,5,K); px(106,42,4,4,K); });
  /* near legs last */
  layer(S.rig.legs,(px,ln)=>{ [[62,44,30],[84,84,84],[106,126,142]].forEach((l,i)=>{ ln(l[0],66,l[1],46,4,M); ln(l[1],46,l[2],90,4,M); ln(l[0],65,l[1],45,1,MH);
      px(l[1]-3,43,6,6,MH); px(l[1]-2,44,4,4,K); px(l[0]-3,63,6,6,RD); px(l[2]-5,90,10,3,K); px(l[2]-5,90,10,1,MH); }); });
  return (RIG_CACHE[key]=c);
}
function drawTransport(){
  dim(0.86);
  const px0=40, py0=76, pw=W-80, ph=H-100;
  plate(px0,py0,pw,ph,'#1a1410','#6b5540','#8a6f50');
  txt('TRANSPORT',px0+28,py0+34,26,C.gold);
  txt('the yard behind the Fixer  ·  purse '+S.caps+'c',px0+28,py0+62,12,C.dim,'left','normal');
  button(px0+pw-150,py0+18,120,38,'BACK',()=>{S.scene='shop';S.sceneT=0;},C.gold,13);
  /* the machine */
  const vx=px0+24, vy=py0+92, vw=704, vh=440;
  g.fillStyle='#120e0b'; g.fillRect(vx,vy,vw,vh);
  g.fillStyle='#2a2119'; g.fillRect(vx,vy+vh-84,vw,84); g.fillStyle='#3a2e22'; g.fillRect(vx,vy+vh-84,vw,3);
  for(let i=0;i<12;i++){ g.fillStyle='#1d1711'; g.fillRect(vx+20+i*58,vy+vh-60+((i*7)%3)*14,30,3); }
  const done=rigDone(), bob=done?Math.round(Math.sin(S.t*2.2)*3):0, cvs=striderCanvas();
  g.fillStyle='rgba(0,0,0,0.4)'; g.fillRect(vx+110,vy+vh-74,vw-220,10);
  g.imageSmoothingEnabled=false;
  g.drawImage(cvs,vx,vy+22+bob,cvs.width*4,cvs.height*4);
  if(S.rig.engine){ for(let i=0;i<6;i++){ const k=((S.t*(done?0.9:0.35)+i/6)%1), sx=vx+(i%2?176:144)+Math.sin(k*9+i)*10, sy=vy+22+bob+100-k*110;
      g.globalAlpha=(1-k)*0.5; g.fillStyle='#8a8378'; const r=6+k*16; g.fillRect(Math.round(sx-r/2),Math.round(sy-r/2),Math.round(r),Math.round(r)); } g.globalAlpha=1; }
  txt('THE STRIDER',vx+16,vy+20,16,done?C.gold:C.ink);
  txt(done?'she walks':(rigCount()+' of '+RIG.length+' parts fitted  ·  pale parts are still missing'),vx+vw-16,vy+20,10,done?C.green:C.dim,'right','normal');
  /* parts */
  const cx=vx+vw+20, cw=px0+pw-24-cx;
  RIG.forEach((p,i)=>{
    const cy=vy+i*98, own=!!S.rig[p.id], can=!own&&S.caps>=p.cost, hov=can&&inRect(MX,MY,{x:cx,y:cy,w:cw,h:90});
    plate(cx,cy,cw,90,hov?'#33281c':'#211a14',own?'#3a3228':(can?'#8fd0ee':'#5a3a30'));
    txt(p.n,cx+14,cy+20,13,own?C.dimmer:C.ink);
    wrapText(p.d,cx+14,cy+40,cw-28,13,9,own?C.dimmer:C.dim);
    if(own) txt('FITTED',cx+cw-12,cy+76,11,C.green,'right');
    else { txt(p.cost+'c',cx+cw-12,cy+76,14,can?'#8fd0ee':C.red,'right'); if(can) BTNS.push({x:cx,y:cy,w:cw,h:90,fn:()=>buyRig(p)}); }
  });
  const fy=vy+4*98+4;
  if(done){
    plate(cx,fy,cw,44,'#2a2012',C.gold);
    BTNS.push({x:cx,y:fy,w:cw,h:44,fn:()=>openPage('map')});
    txt('SEE THE ROAD',cx+cw/2,fy+22,14,C.gold,'center');
  } else wrapText('Fit all four and the Strider can carry the stall out of Dustwell. The road itself opens in a later build.',cx+4,fy+10,cw-8,13,9,C.dimmer);
}
