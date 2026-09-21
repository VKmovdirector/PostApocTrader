/* ================================================================
   THE TOWN  -  the page every day starts from. Everything you can do
   off the stall hangs off here; the Fixer is one door among several.
   ================================================================ */
let CITY_IMG=null;
function buildCity(){
  const Wc=150,Hc=80, c=makeCanvas(Wc,Hc), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  ['#2a2238','#3d2c40','#5a3644','#7d4440','#a85c3a','#cf7c3a','#e39a48'].forEach((col,i)=>px(0,i*8,Wc,9,col));
  for(let dy=-13;dy<=13;dy++){ const w=Math.floor(Math.sqrt(169-dy*dy)); px(104-w,40+dy,w*2+1,1,dy<-4?'#f6d08a':'#f0b060'); }
  let sd=19; const rn=()=>{ sd=(sd*1103515245+12345)&0x7fffffff; return sd/0x7fffffff; };
  /* far ruins */
  let fx=0; while(fx<Wc){ const w=4+rn()*7, h=8+rn()*16; px(fx,58-h,w,h,'#6b3f40'); if(rn()<0.4) px(fx+1,58-h-3,2,3,'#6b3f40'); fx+=w+1; }
  /* broken towers */
  [[12,30,11],[30,22,9],[47,36,13],[70,18,8],[84,28,10],[118,34,12],[134,24,9]].forEach(t=>{
    const bx=t[0], h=t[1], w=t[2], top=60-h;
    px(bx,top,w,h,'#2e2230'); px(bx,top,2,h,'#3d2e3e');
    for(let k=0;k<w;k+=2) px(bx+k,top-(rn()*4|0),2,4,'#2e2230');                  /* ragged crown */
    for(let wy=top+4;wy<58;wy+=5) for(let wx=bx+2;wx<bx+w-2;wx+=3) if(rn()<0.16) px(wx,wy,1,2,'#f0c060');
  });
  /* water tower and windmill */
  px(58,30,10,7,'#241a26'); px(57,29,12,1,'#3d2e3e'); px(59,37,1,22,'#241a26'); px(66,37,1,22,'#241a26'); px(59,46,8,1,'#241a26');
  px(101,34,1,26,'#241a26'); [[-6,-1],[6,1],[-1,6],[1,-6]].forEach(v=>{ for(let k=1;k<7;k++) px(101+v[0]*k/6,34+v[1]*k/6,1,1,'#241a26'); });
  /* the wall, gate and lamps */
  px(0,60,Wc,8,'#1d1620'); for(let k=0;k<Wc;k+=6) px(k,58,3,2,'#1d1620');
  px(68,56,14,12,'#140f16'); px(70,58,10,10,'#2a1c18'); px(66,54,18,2,'#3d2e3e');
  [[64,57],[85,57]].forEach(l=>{ px(l[0],l[1],2,2,'#f6d874'); px(l[0]-1,l[1]-1,4,1,'#1d1620'); });
  /* dunes in front */
  px(0,68,Wc,12,'#3a2a22'); for(let k=0;k<16;k++){ const dx=rn()*Wc; px(dx,69+rn()*9,6+rn()*10,1,k%2?'#4a362a':'#2a1e18'); }
  px(20,66,18,2,'#3a2a22'); px(96,66,26,2,'#3a2a22');
  return c;
}
function hubOpenDay(){ if(S.fresh){ S.fresh=false; S.scene='dayintro'; S.sceneT=0; } else nextDay(); }
function toHub(){ S.scene='hub'; S.sceneT=0; }
function buyBench(){
  if(S.wb){ enterWorkshop(); return; }
  if(S.caps<CRAFT.price){ Snd.bad(); return; }
  S.caps-=CRAFT.price; S.wb=true; S.wbDay=S.day+1; achInc('bench'); Snd.coin(6); flash('#8fd0ee',0.25); enterWorkshop();
}
function drawHub(){
  dim(0.8);
  const x=70,y=78,w=W-140,h=H-98;
  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');
  txt('DUSTWELL',x+30,y+36,28,C.gold);
  txt(S.fresh?'before your first day':('the night after day '+S.day),x+30,y+64,12,C.dim,'left','normal');
  txt('purse '+S.caps+'c   ·   rent '+(S.fresh?'tonight ':'tomorrow ')+rentFor(S.fresh?S.day:S.day+1)+'c',x+w-30,y+36,14,C.ink,'right');
  /* the town, in the middle */
  if(!CITY_IMG) CITY_IMG=buildCity();
  const iw=600, ih=320, ix=W/2-iw/2, iy=y+96;
  plate(ix-6,iy-6,iw+12,ih+12,'#0d0a08','#5c4a37');
  g.imageSmoothingEnabled=false; g.drawImage(CITY_IMG,ix,iy,iw,ih);
  [[64,57],[85,57]].forEach((l,i)=>{ const p=0.5+Math.sin(S.t*3+i*2)*0.25; const gx=ix+l[0]*4+4, gy=iy+l[1]*4+4, gr=g.createRadialGradient(gx,gy,2,gx,gy,40);
    gr.addColorStop(0,'rgba(246,216,116,'+(0.5*p)+')'); gr.addColorStop(1,'rgba(246,216,116,0)'); g.fillStyle=gr; g.fillRect(gx-40,gy-40,80,80); });
  /* doors, left and right of it */
  const bw=216, bh=58, gp=12, lx=x+30, rx=x+w-30-bw, by=iy;
  const nl=newLooksOn(S.day).length, canWb=S.wb||S.caps>=CRAFT.price;
  button(lx,by,bw,bh,'THE FIXER',()=>{S.scene='shop';S.sceneT=0;},C.gold,15);
  button(lx,by+(bh+gp),bw,bh,S.wb?'THE WORKBENCH':('WORKBENCH · '+CRAFT.price+'c'),()=>buyBench(),canWb?'#8fd0ee':C.dimmer,S.wb?13:11);
  button(lx,by+(bh+gp)*2,bw,bh,'TRANSPORT '+rigCount()+'/'+RIG.length,()=>{S.scene='transport';S.sceneT=0;},rigDone()?C.gold:'#c8a070',13);
  button(lx,by+(bh+gp)*3,bw,bh,'STALL & LOOKS'+(nl?' *':''),()=>{S.scene='looks';},nl?C.purple:C.dim,13);
  button(rx,by,bw,bh,'THE LEDGER',()=>{S.scene='ledger';},S.history.length?C.green:C.dimmer,13);
  button(rx,by+(bh+gp),bw,bh,'THE MAP',()=>openPage('map'),'#8fd0ee',13);
  button(rx,by+(bh+gp)*2,bw,bh,'ACHIEVEMENTS '+achCount()+'/'+ACH.length,()=>openPage('ach'),C.gold,10);
  if(!S.wb&&inRect(MX,MY,{x:lx,y:by+(bh+gp),w:bw,h:bh})){
    plate(lx+bw+10,by+(bh+gp)-8,360,84,'#14100c','#8fd0ee');
    txt('THE WORKBENCH',lx+bw+24,by+(bh+gp)+10,12,'#8fd0ee');
    wrapText('Buy materials, craft your own goods and refine them up to LEGENDARY.',lx+bw+24,by+(bh+gp)+30,332,14,10,C.ink);
  }
  button(W/2-230,iy+ih+28,460,62,'OPEN THE STALL  ·  DAY '+(S.fresh?S.day:S.day+1),()=>hubOpenDay(),C.gold,18);
}
function buyActive(i){
  const a=ACTIVES[i];
  if(S.actOwn[i]||S.caps<a.cost) return;
  S.caps-=a.cost; S.actOwn[i]=true; Snd.coin(4); flash(a.col,0.2);
  AST.perks=n0('perks')+1; if(S.actOwn.every(Boolean)) AST.allActive=1; achCheck();
}
function drawShop(){
  dim(0.78);
  const w=940,h=600,x=W/2-w/2,y=74;
  plate(x,y,w,h,'#1a1410','#6b5540','#8a6f50');
  txt('THE FIXER',W/2,y+36,28,C.gold,'center');
  button(x+w-30-190,y+18,190,36,'BACK TO TOWN',()=>toHub(),C.gold,12);
  txt('spend it or save it for rent  ·  purse '+S.caps+'c',W/2,y+62,13,C.dim,'center','normal');
  const cw=211,ch=92,gap=12;
  txt('PASSIVE  ·  always on',x+30,y+88,12,C.gold);
  UPGRADES.forEach((u,i)=>{
    const cx=x+30+(i%4)*(cw+gap), cy=y+100+Math.floor(i/4)*(ch+gap);
    const lv=S.up[u.id], maxed=lv>=u.max, afford=!maxed&&S.caps>=u.cost[lv];
    shopCard(cx,cy,cw,ch,u.id,C.gold,u.n,u.d,lv,u.max,maxed?null:u.cost[lv],afford,()=>buyUpgrade(u),null);
  });
  txt('ACTIVE  ·  press its number key during the day',x+30,y+326,12,'#a173c8');
  ACTIVES.forEach((a,i)=>{
    const cx=x+30+(i%4)*(cw+gap), cy=y+338+Math.floor(i/4)*(ch+gap+16);
    if(a.id==='hire'){
      const h2=hired(), nx=nextHand(), afford=!!nx&&S.caps>=nx.fee;
      shopCard(cx,cy,cw,ch,'hire',a.col,h2?('HIRED HAND · LVL '+h2.lvl):'HIRE A HAND',
        nx?('KIT works the stall for '+nx.dur+'s'):('KIT works the stall for '+h2.dur+'s'),
        S.hire.lvl,HANDS.length, nx?nx.fee:null, afford,
        ()=>{ S.caps-=nx.fee; S.hire.lvl=nx.lvl; S.actOwn[i]=true; Snd.coin(4); flash(a.col,0.2); AST.perks=n0('perks')+1; AST.hired=1; if(S.actOwn.every(Boolean)) AST.allActive=1; achCheck(); }, ''+a.key);
    } else {
      const own=S.actOwn[i], afford=!own&&S.caps>=a.cost;
      shopCard(cx,cy,cw,ch,a.id,a.col,a.n,a.d,own?1:0,1,own?null:a.cost,afford,()=>buyActive(i),''+a.key);
    }
    txt(a.cd+'s rest',cx+44,cy+ch-12,9,C.dimmer,'left','normal');
    txt(fitText(a.why,cw-8,9,'normal'),cx+4,cy+ch+12,9,C.dimmer,'left','normal');
  });
}
