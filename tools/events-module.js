/* ================================================================
   EVENTS TEST  -  the Herald prints one event; it moves the price of
   ONE kind of goods for ONE day: the very next trading day.
   ================================================================ */
const EVDEMO={everyNight:true};
const EVENTS=[
 /* weather */
 {id:'dust',   type:'weather', cat:'meds', m:1.40, h:['DUST STORM','ROLLS IN'],      b:'A wall of grit is due off the flats by dawn. Lungs will rattle for days and the clinic has already hung out its lamp.', q:'"Wet rag over the mouth and pray," the ferryman advises.'},
 {id:'heat',   type:'weather', cat:'food', m:1.50, h:['HEAT WAVE','BAKES TOWN'],     b:'The well rope came up dry twice yesterday. Anything that can be drunk or eaten cold will be fought over tomorrow.',          q:'"I would trade my boots for a clean bottle," said a drover.'},
 {id:'cold',   type:'weather', cat:'food', m:1.35, h:['COLD SNAP','TONIGHT'],        b:'Frost on the pump handle for the first time this year. Folk eat more when they shiver, and they pay for it.',                q:'"Beans. Hot. Now." - overheard at the gate.'},
 {id:'acid',   type:'weather', cat:'tech', m:1.40, h:['ACID RAIN','FORECAST'],       b:'Yellow cloud to the west. Every exposed wire and board in Dustwell will be pitted by noon; spares will be dear.',              q:'"Cover your terminals," warns the council engineer.'},
 {id:'fair',   type:'weather', cat:'food', m:0.75, h:['FAIR SKIES','ALL WEEK'],      b:'Growers are bringing everything in at once while the weather holds. The strip will be knee-deep in produce.',                 q:'"You cannot give plums away," one grower complained.'},
 /* military */
 {id:'gangs',  type:'military',cat:'meds', m:1.50, h:['GANGS CLASH','AT THE RIDGE'], b:'Two bands met over the ridge road last night and neither backed down. The wounded are being carted toward town.',            q:'"Bring bandages, not questions," said a gate guard.'},
 {id:'raiders',type:'military',cat:'guns', m:1.60, h:['RAIDERS MASS','UP NORTH'],    b:'Scouts count forty fires past the north wash. Every household is arming whoever can hold a gun the right way round.',          q:'"I will take anything that goes bang," said a farmer.'},
 {id:'militia',type:'military',cat:'guns', m:1.40, h:['THE MILITIA','IS HIRING'],    b:'The council is paying a day-rate for wall duty, and recruits are told to bring their own iron.',                              q:'"No gun, no pay," the sergeant confirmed.'},
 {id:'truce',  type:'military',cat:'guns', m:0.70, h:['CEASEFIRE','IS SIGNED'],      b:'The ridge bands shook on it at noon. Nobody expects it to last, but nobody is buying rifles while it does.',                  q:'"First quiet night in a month," said the gate guard.'},
 {id:'convoy', type:'military',cat:'tech', m:1.35, h:['TECH CONVOY','AMBUSHED'],     b:'The monthly haul from Old Meridian never arrived. What is already on the shelves in town is all there is.',                  q:'"They took the lot, even the cables," a survivor said.'},
 /* the town */
 {id:'fever',  type:'town',    cat:'meds', m:1.60, h:['FEVER IN THE','SOUTH QUARTER'],b:'Eleven down in two days. The clinic is out of nearly everything and is sending runners to every stall on the strip.',       q:'"Pay what they ask," the doctor told her runners.'},
 {id:'harvest',type:'town',    cat:'food', m:0.70, h:['THE HARVEST','COMES IN'],     b:'Carts are queued past the gate. Good news for bellies and bad news for anyone sitting on a shelf of tins.',                   q:'"Cheapest week of the year," said a cook.'},
 {id:'tower',  type:'town',    cat:'food', m:1.45, h:['WATER TOWER','CRACKS'],       b:'A seam opened overnight and half the tank is in the street. Clean water is suddenly worth queueing for.',                     q:'"Patch it again," voted the council, again.'},
 {id:'bunker', type:'town',    cat:'tech', m:0.70, h:['OLD BUNKER','CRACKED OPEN'],  b:'Scavengers broke into a sealed store under the rail yard. Crates of old machines are flooding the strip.',                    q:'"More boards than buyers," a scavenger shrugged.'},
 {id:'power',  type:'town',    cat:'tech', m:1.50, h:['POWER OUT','AT THE WORKS'],   b:'The generator hall went dark at dusk. The foreman wants cells and boards by morning and is not counting chits.',               q:'"Whatever it costs," the foreman said.'},
 {id:'quack',  type:'town',    cat:'meds', m:0.75, h:['QUACK DOCTOR','RUN OUT'],     b:'His whole stock was seized and is being handed out free at the gate. Honest medicine will be a hard sell for a day.',          q:'"Most of it is sugar," admitted a guard.'}
];
const EV_FILL=[['WELL ROPE REPLACED','Third one this season.'],['STRAY MULE FOUND','Answers to nothing.'],['COUNCIL MEETS AGAIN','No decision reached.'],
 ['WALL PATROL DOUBLED','Volunteers wanted.'],['FERRY FARE GOES UP','Ferryman blames the mud.'],['LOST: ONE LEFT BOOT','Reward: the right one.'],
 ['RAT KING SIGHTED','East drain, after dark.'],['NEW LAMP AT THE GATE','Burns till midnight.'],['STRIDER SEEN WALKING','Children delighted.']];
const EV_ICON={
 weather: ['..kkk...','.kkkkk..','kkkkkkk.','kkkkkkkk','.kkkkkk.','...kk...','..kk....','.kk.....'],
 military:['k......k','.k....k.','..k..k..','...kk...','...kk...','..k..k..','.kk..kk.','kk....kk'],
 town:    ['...kk...','..kkkk..','.kkkkkk.','.kkkkkk.','.kkkkkk.','kkkkkkkk','...kk...','...kk...']
};
const EV_SPR={}; Object.keys(EV_ICON).forEach(k=>EV_SPR[k]=spriteFrom(EV_ICON[k],{k:'#2a241c'}));
function evPct(e){ const p=Math.round((e.m-1)*100); return (p>0?'+':'')+p+'%'; }
function evToday(){ return (S.event&&S.event.day===S.day)?S.event:null; }
function evTomorrow(){ return (S.event&&S.event.day===S.day+1)?S.event:null; }
function evMult(cat){ const e=evToday(); return (e&&e.cat===cat)?e.m:1; }
/* called when the Herald is about to be shown: tomorrow's event is fixed then, never rerolled */
function rollEvent(){
  const last=S.event, pool=EVENTS.filter(e=>!last||(e.id!==last.id&&e.cat!==last.cat));
  const e=pick(pool);
  const fill=EV_FILL.slice().sort(()=>Math.random()-0.5).slice(0,3);
  S.event=Object.assign({},e,{day:S.day+1,fill:fill});
  S.evLog=S.evLog||[];
}
