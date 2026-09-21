/* ================================================================
   ACHIEVEMENTS  -  50 of them, kept across runs in localStorage
   ================================================================ */
const AST={};                       /* lifetime numbers the tests read */
let ACH_GOT={}, TOASTS=[];
try{ const sv=JSON.parse(localStorage.getItem('rustrations.ach')||'null'); if(sv){ Object.assign(AST,sv.st||{}); ACH_GOT=sv.got||{}; } }catch(e){}
function achSave(){ try{ localStorage.setItem('rustrations.ach',JSON.stringify({st:AST,got:ACH_GOT})); }catch(e){} }
const n0=k=>AST[k]||0;
const ACH=[
 /* trade */
 {id:'sale1',   n:'FIRST CHIT',        d:'Make your first sale.',                     t:()=>n0('sold')>=1},
 {id:'sale50',  n:'REGULAR TRADE',     d:'Sell 50 goods.',                            t:()=>n0('sold')>=50},
 {id:'sale250', n:'KNOWN STALL',       d:'Sell 250 goods.',                           t:()=>n0('sold')>=250},
 {id:'sale1k',  n:'INSTITUTION',       d:'Sell 1,000 goods.',                         t:()=>n0('sold')>=1000},
 {id:'earn500', n:'POCKET CHANGE',     d:'Take 500c over your career.',               t:()=>n0('earned')>=500},
 {id:'earn5k',  n:'STRONGBOX',         d:'Take 5,000c over your career.',             t:()=>n0('earned')>=5000},
 {id:'earn50k', n:'IRON CHEST',        d:'Take 50,000c over your career.',            t:()=>n0('earned')>=50000},
 {id:'big50',   n:'GOOD PRICE',        d:'One sale of 50c or more.',                  t:()=>n0('maxSale')>=50},
 {id:'big250',  n:'BIG SPENDER',       d:'One sale of 250c or more.',                 t:()=>n0('maxSale')>=250},
 {id:'big1k',   n:'WHALE',             d:'One sale of 1,000c or more.',               t:()=>n0('maxSale')>=1000},
 /* haggling */
 {id:'hag1',    n:'HARD BARGAIN',      d:'Sell at the very top of the haggle bar.',   t:()=>n0('maxHag')>=1},
 {id:'hag25',   n:'SMOOTH TALKER',     d:'25 sales at the top of the haggle bar.',    t:()=>n0('maxHag')>=25},
 {id:'greedy',  n:'TOO GREEDY',        d:'Push a buyer until they snap.',             t:()=>n0('snaps')>=1},
 {id:'exact25', n:'JUST THE THING',    d:'25 exact-item sales.',                      t:()=>n0('exact')>=25},
 {id:'crate',   n:'OFF THE CRATE',     d:'Sell 20 goods straight off the counter.',   t:()=>n0('counterSales')>=20},
 /* streaks */
 {id:'st5',     n:'ON A ROLL',         d:'Reach a x5 streak.',                        t:()=>n0('bestStreak')>=5},
 {id:'st10',    n:'HOT HANDS',         d:'Reach a x10 streak.',                       t:()=>n0('bestStreak')>=10},
 {id:'st25',    n:'UNTOUCHABLE',       d:'Reach a x25 streak.',                       t:()=>n0('bestStreak')>=25},
 /* the counter */
 {id:'file100', n:'TIDY',              d:'File 100 goods on the right shelf.',        t:()=>n0('filed')>=100},
 {id:'file1k',  n:'QUARTERMASTER',     d:'File 1,000 goods on the right shelf.',      t:()=>n0('filed')>=1000},
 {id:'misfile', n:'WRONG SHELF',       d:'Misfile something. It happens.',            t:()=>n0('misfiled')>=1},
 {id:'spill10', n:'BUTTERFINGERS',     d:'Let 10 goods spill off a full counter.',    t:()=>n0('spilled')>=10},
 {id:'scrap50', n:'SCRAPPER',          d:'Scrap 50 goods.',                           t:()=>n0('scrapped')>=50},
 /* bulk */
 {id:'bulk1',   n:'WHOLESALE',         d:'Fill your first bulk order.',               t:()=>n0('bulk')>=1},
 {id:'bulk25',  n:'BY THE CRATE',      d:'Fill 25 bulk orders.',                      t:()=>n0('bulk')>=25},
 {id:'bulk4',   n:'FOUR OF A KIND',    d:'Fill a bulk order of four.',                t:()=>n0('bulk4')>=1},
 /* days */
 {id:'day5',    n:'STILL STANDING',    d:'Reach day 5.',                              t:()=>n0('bestDay')>=5},
 {id:'day10',   n:'PART OF THE TOWN',  d:'Reach day 10.',                             t:()=>n0('bestDay')>=10},
 {id:'day20',   n:'OLD HAND',          d:'Reach day 20.',                             t:()=>n0('bestDay')>=20},
 {id:'day30',   n:'FIXTURE',           d:'Reach day 30.',                             t:()=>n0('bestDay')>=30},
 {id:'nowalk',  n:'NOBODY WALKED',     d:'A day of 8+ sales and no walk-outs.',       t:()=>n0('noWalkDay')>=1},
 {id:'spotless',n:'SPOTLESS',          d:'A day of 10+ filings, no misfile, no spill.',t:()=>n0('spotlessDay')>=1},
 {id:'take300', n:'GOOD DAY',          d:'Take 300c in one day.',                     t:()=>n0('bestTake')>=300},
 {id:'take1k',  n:'GREAT DAY',         d:'Take 1,000c in one day.',                   t:()=>n0('bestTake')>=1000},
 {id:'take5k',  n:'BOOM TOWN',         d:'Take 5,000c in one day.',                   t:()=>n0('bestTake')>=5000},
 {id:'purse2k', n:'NEST EGG',          d:'Hold 2,000c after rent.',                   t:()=>n0('bestPurse')>=2000},
 {id:'purse10k',n:'DUST BARON',        d:'Hold 10,000c after rent.',                  t:()=>n0('bestPurse')>=10000},
 {id:'whisker', n:'BY A WHISKER',      d:'Pay rent with under 10c left.',             t:()=>n0('whisker')>=1},
 {id:'firesale',n:'FIRE SALE',         d:'Scrap the whole stall to make rent.',       t:()=>n0('fireSale')>=1},
 {id:'keep5',   n:'WASTE NOT',         d:'Keep leftover stock overnight 5 times.',    t:()=>n0('kept')>=5},
 /* the fixer */
 {id:'perk1',   n:'FIRST FIX',         d:'Buy anything from the Fixer.',              t:()=>n0('perks')>=1},
 {id:'passive', n:'FULLY FIXED',       d:'Max every passive perk in one run.',        t:()=>n0('allPassive')>=1},
 {id:'actives', n:'FIVE FINGERS',      d:'Own all five active perks in one run.',     t:()=>n0('allActive')>=1},
 {id:'hired',   n:'HELP WANTED',       d:'Hire KIT.',                                 t:()=>n0('hired')>=1},
 {id:'act50',   n:'BUTTON MASHER',     d:'Fire active perks 50 times.',               t:()=>n0('actUsed')>=50},
 {id:'look',    n:'NEW COAT',          d:'Buy something for your look or stall.',     t:()=>n0('looks')>=1},
 /* the bench */
 {id:'bench',   n:'MAKER',             d:'Unlock the workbench.',                     t:()=>n0('bench')>=1},
 {id:'craft25', n:'APPRENTICE',        d:'Craft 25 goods.',                           t:()=>n0('crafted')>=25},
 {id:'legend',  n:'LIVING LEGEND',     d:'Refine something to LEGENDARY.',            t:()=>n0('madeLeg')>=1},
 /* people */
 {id:'crowd',   n:'KNOW YOUR CROWD',   d:'Serve every kind of customer.',             t:()=>Object.keys(AST.types||{}).length>=TYPES.length}
];
function achCheck(){
  let any=false;
  ACH.forEach(a=>{ if(!ACH_GOT[a.id]&&a.t()){ ACH_GOT[a.id]=1; any=true; TOASTS.push({a:a,t:0}); } });
  if(any){ achSave(); Snd.good(); }
}
function achInc(k,by){ AST[k]=(AST[k]||0)+(by===undefined?1:by); achCheck(); }
function achMax(k,v){ if(v>(AST[k]||0)){ AST[k]=v; } achCheck(); }
function achCount(){ return ACH.filter(a=>ACH_GOT[a.id]).length; }
const TROPHY=spriteFrom(['kkkkkkkk','kaaaaaak','kabbbbak','.kabbak.','..kaak..','...kk...','..kaak..','.kkkkkk.'],{k:'#1a1410',a:'#e8b13c',b:'#fff0b0'});
const TROPHY_OFF=spriteFrom(['kkkkkkkk','kaaaaaak','kabbbbak','.kabbak.','..kaak..','...kk...','..kaak..','.kkkkkk.'],{k:'#14100c',a:'#3a3228',b:'#4a4034'});
function drawToasts(dt){
  if(!TOASTS.length) return;
  const o=TOASTS[0]; o.t+=dt;
  const k=o.t<0.3?o.t/0.3:(o.t>3.2?Math.max(0,1-(o.t-3.2)/0.4):1), w=380, x=W/2-w/2, y=66-(1-k)*70;
  plate(x,y,w,54,'#2a2012',C.gold);
  blit(TROPHY,x+12,y+11,4);
  txt('ACHIEVEMENT',x+56,y+16,9,C.gold);
  txt(o.a.n,x+56,y+34,14,C.ink);
  txt(achCount()+'/'+ACH.length,x+w-12,y+16,9,C.dim,'right');
  if(o.t>3.6) TOASTS.shift();
}
function openPage(scene){ S.backScene=S.scene; S.scene=scene; S.sceneT=0; }
function closePage(){ S.scene=S.backScene||'menu'; S.sceneT=0; }
function drawAchievements(){
  g.fillStyle='#0d0a08'; g.fillRect(0,0,W,H);
  txt('ACHIEVEMENTS',40,40,28,C.gold);
  txt(achCount()+' of '+ACH.length+' earned  ·  kept between runs',40,70,12,C.dim,'left','normal');
  bar(W-460,30,300,18,achCount()/ACH.length,C.gold);
  button(W-140,22,100,36,'BACK',()=>closePage(),C.gold,13);
  const cols=5, cw=236, ch=60, gx=8, gy=6, x0=(W-(cols*cw+(cols-1)*gx))/2, y0=92;
  ACH.forEach((a,i)=>{
    const x=x0+(i%cols)*(cw+gx), y=y0+Math.floor(i/cols)*(ch+gy), got=!!ACH_GOT[a.id];
    plate(x,y,cw,ch,got?'#2a2012':'#15110d',got?C.gold:'#3a3228');
    blit(got?TROPHY:TROPHY_OFF,x+8,y+14,4);
    txt(a.n,x+48,y+15,10,got?C.gold:C.dimmer);
    wrapText(a.d,x+48,y+32,cw-56,12,8,got?C.ink:C.dimmer);
  });
}

/* ================================================================
   THE MAP  -  five towns in the barrens. Only Dustwell is open yet;
   the others are where the road goes next.
   ================================================================ */
const TOWNS=[
 {id:'dustwell',n:'DUSTWELL',    x:66, y:124, home:true, road:'your stall',
  d:'A well, a wall and a council that wants its rent. Everyone passes through; nobody is rich.', wants:'a bit of everything'},
 {id:'saltpan', n:'SALTPAN',     x:146,y:58,  road:'3 days north-east',
  d:'Salt miners on the bed of a dead lake. Cracked hands, cracked lips, steady pay.', wants:'clean water and meds'},
 {id:'cinder',  n:'CINDER GAP',  x:236,y:98,  road:'5 days east',
  d:'A mountain pass held by raiders who found that tolls pay better than raids. Short tempers.', wants:'arms, and quickly'},
 {id:'meridian',n:'OLD MERIDIAN',x:180,y:152, road:'4 days south-east',
  d:'The drowned city. Scavengers haul machines out of towers that lean a little further every year.', wants:'tech, and sells it cheap'},
 {id:'lastpump',n:'LAST PUMP',   x:286,y:40,  road:'9 days, the end of the road',
  d:'The only deep pump left working. Rich, thirsty, and a long way from anywhere.', wants:'the finest goods you can make'}
];
const ROUTES=[[0,1],[0,3],[1,2],[3,2],[2,4]];
let MAP_IMG=null;
function buildMap(){
  const c=makeCanvas(320,190), x=c.getContext('2d');
  const px=(a,b,w,h,col)=>{ x.fillStyle=col; x.fillRect(Math.round(a),Math.round(b),Math.round(w),Math.round(h)); };
  let sd=7; const rnd2=()=>{ sd=(sd*1103515245+12345)&0x7fffffff; return sd/0x7fffffff; };
  const sand=['#c9a469','#c19b60','#b89258','#ae8950'];
  for(let yy=0;yy<190;yy+=2) for(let xx=0;xx<320;xx+=2){
    const n=Math.sin(xx*0.045+yy*0.02)+Math.sin(yy*0.09-xx*0.015)*0.7+rnd2()*0.9;
    px(xx,yy,2,2,sand[clamp(Math.floor((n+2.2)/1.15),0,3)]);
  }
  /* dunes: short crescents of light over shadow */
  for(let i=0;i<70;i++){ const dx=rnd2()*320, dy=rnd2()*190, w=6+rnd2()*12;
    px(dx,dy,w,1,'#dcb87c'); px(dx+2,dy+1,w-2,1,'#9a7846'); }
  /* the dead lake */
  for(let yy=-16;yy<=16;yy++){ const w=Math.floor(Math.sqrt(1-yy*yy/256)*34); px(150-w,52+yy,w*2,1,yy<-8?'#e6e0d0':'#d8d1bf'); }
  for(let i=0;i<40;i++) px(122+rnd2()*56,40+rnd2()*26,1+rnd2()*5,1,'#b9b19c');
  /* mountains in the east */
  for(let i=0;i<9;i++){ const mx=216+i*9+rnd2()*5, mh=16+rnd2()*18, my=112-i*3;
    for(let k=0;k<mh;k++){ px(mx-k*0.6,my-mh+k,k*1.2+1,1,k<mh*0.3?'#8a7560':'#6b5a48'); px(mx,my-mh+k,k*0.6+1,1,'#54463a'); } }
  /* dry river */
  let rx=0, ry=172; for(let i=0;i<130;i++){ px(rx,ry,3,2,'#8f7a58'); px(rx,ry,2,1,'#7a6648'); rx+=2.5; ry+=Math.sin(i*0.22)*1.3-0.5; }
  /* the drowned city */
  for(let i=0;i<16;i++){ const bx=166+rnd2()*34, bh=5+rnd2()*12; px(bx,160-bh,3+rnd2()*3,bh,'#5a5148'); px(bx,160-bh,1,bh,'#7a7064'); }
  px(160,158,50,4,'#6f8a8a'); px(164,161,40,2,'#57706f');
  /* crater and bones */
  for(let yy=-7;yy<=7;yy++){ const w=Math.floor(Math.sqrt(49-yy*yy)*1.6); px(96-w,44+yy,w*2,1,yy<0?'#8a6f48':'#a5864f'); }
  /* caravan routes */
  ROUTES.forEach(r=>{ const a=TOWNS[r[0]], b=TOWNS[r[1]], n=Math.hypot(b.x-a.x,b.y-a.y)/4;
    for(let i=1;i<n;i++){ const t=i/n, bow=Math.sin(t*Math.PI)*6;
      px(lerp(a.x,b.x,t)-bow*0.3,lerp(a.y,b.y,t)+bow,2,2,(i%2)?'#4a3a28':'#6b5438'); } });
  /* towns */
  TOWNS.forEach(tn=>{ const tx=tn.x, ty=tn.y;
    px(tx-7,ty+3,15,2,'rgba(0,0,0,0.25)');
    px(tx-6,ty-2,5,5,'#6b4a2a'); px(tx-6,ty-3,5,1,'#a8562a'); px(tx,ty-4,6,7,'#5a3f28'); px(tx,ty-5,6,1,'#c8703a');
    px(tx-1,ty+1,2,2,'#f0c060');
    if(tn.home){ px(tx+7,ty-10,1,11,'#2a1f14'); px(tx+8,ty-10,5,3,'#a8382a'); }
    if(tn.id==='lastpump'){ px(tx-10,ty-8,1,10,'#3a3129'); px(tx-13,ty-9,7,1,'#3a3129'); }
  });
  /* frame and compass */
  px(0,0,320,2,'#2a1f14'); px(0,188,320,2,'#2a1f14'); px(0,0,2,190,'#2a1f14'); px(318,0,2,190,'#2a1f14');
  px(24,18,1,15,'#2a1f14'); px(17,25,15,1,'#2a1f14'); px(23,16,3,3,'#a8382a');
  return c;
}
function drawMap(){
  if(!MAP_IMG) MAP_IMG=buildMap();
  g.imageSmoothingEnabled=false;
  g.drawImage(MAP_IMG,0,0,W,H);
  g.fillStyle='rgba(20,14,8,0.18)'; g.fillRect(0,0,W,H);
  plate(W/2-210,14,420,54,'#1a1410','#6b5540');
  txt('THE BARRENS',W/2,34,22,C.gold,'center');
  txt('five towns, one road  ·  only Dustwell is open to you so far',W/2,56,10,C.dim,'center','normal');
  txt('N',100,52,12,'#2a1f14','center');
  button(W-150,20,110,40,'BACK',()=>closePage(),C.gold,14);
  let hov=null;
  TOWNS.forEach(tn=>{
    const sx=tn.x*4, sy=tn.y*4, h=Math.hypot(MX-sx,MY-sy)<46;
    if(h) hov=tn;
    const w=txtw(tn.n,12)+16;
    plate(sx-w/2,sy+22,w,22,tn.home?'#2a2012':'#1a1410',h?C.gold:(tn.home?C.gold:'#5c4a37'));
    txt(tn.n,sx,sy+33,12,tn.home?C.gold:(h?C.ink:'#c9b48f'),'center');
    if(tn.home&&Math.sin(S.t*4)>-0.2){ g.strokeStyle=C.gold; g.lineWidth=3; g.strokeRect(sx-36,sy-30,72,50); }
  });
  const tn=hov||TOWNS[0], bw=460, bx=24, by=H-150;
  plate(bx,by,bw,126,'#1a1410',hov?C.gold:'#6b5540');
  txt(tn.n,bx+16,by+22,16,C.gold);
  txt(tn.home?'YOU ARE HERE':'THE ROAD IS NOT OPEN YET',bx+bw-16,by+22,10,tn.home?C.green:C.dimmer,'right');
  txt(tn.road,bx+16,by+42,10,C.dim,'left','normal');
  wrapText(tn.d,bx+16,by+64,bw-32,15,11,C.ink);
  txt('buys: '+tn.wants,bx+16,by+110,10,'#8fd0ee','left','normal');
  if(!hov) txt('point at a town',bx+bw-16,by+110,9,C.dimmer,'right','normal');
}
