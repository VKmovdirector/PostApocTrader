# RUST & RATIONS — design notes (build 20)

A trading-post game. You run the only stall in a dust-blown town. Caravans dump
mixed salvage on your counter, wanderers queue at the window, and rent is due
every night.

**Naming.** Nothing in the game borrows another franchise's vocabulary. The currency is
**chits** (shown as `c`), the everyday customer is a **Wanderer**, the glowing mutant is a
**Shiner**, and the goods are Mend Shot, Iodine Tabs, Ash Plum, Power Cell and Zip Gun.
Internal ids (`stimpak`, `radaway`, `mutfruit`, `cell`, `pipegun`, `glower`, `S.caps`) are
unchanged so saves and test scripts keep working — only what the player reads was renamed.

Single file: `index.html`. Canvas 2D, design resolution 1280×760, scaled and
letterboxed to the window. No dependencies. The only external request is the
Silkscreen webfont from Google Fonts — offline it falls back to a monospace stack
and everything still works.

Build 1 (vector placeholder art) is kept as `v1-build1.html`. Build 2 introduced the
pixel art; build 3 slows the rent curve, keeps the caravan timer visible during the
day-1 tutorial, and adds stall/merchant customisation; build 4 makes that customisation
try-before-you-buy, drip-feeds new options as the days pass, and adds the five-day ledger;
build 5 removes the town-mood meter; build 6 adds the hired hand and
raises Fixer prices 20 %; build 7 halves every sale, raises Fixer prices another 20 %,
guts the chicory upgrade, makes hires half again as dear and lets you stand one down;
build 8 brings in bulk orders, two scripted walkthroughs, and opens the tech shelf on day one;
build 9 keeps the top bar up at all times, turns the sorting drone into a robo-hand you can see,
gives every perk an icon, and adds the morning paper; build 10 splits the Fixer into passive
and active perks and puts both rails on the play screen; build 11 drops the Salvaged Shelf
upgrade and makes the walkthrough cards wait for a click.

---

## 1. The loop

One **day** lasts 90 seconds with three pressures running at once:

1. **Caravans deliver.** Every `crateEvery(day)` seconds a crate rolls in and pops
   3–6 items onto **the counter** (5–8 slots). Counter full → the goods **spill** and
   are gone: you lose whatever they would have sold for.
2. **You sort.** Drag each item onto the shelf whose sign matches its category.
   A correct file builds your **streak**; a wrong shelf breaks it and marks the
   item `MIS`.
3. **You sell.** Up to 3 customers queue at the window, each with a want and a
   burning patience bar. Drag them what they asked for. Let one run out and you lose
   the sale and your streak.

**Failing rent is the only way to lose.** Build 5 removed the town-mood meter: losing
standing because a customer wanted something the caravan never delivered was a penalty the
player could not prevent, which is exactly the randomness the meter was adding. What a
walk-out or a spill costs now is honest and immediate — the sale you did not make, the
goods you no longer have, and the streak you were building. Since rent is gentle (§8), a
run in practice ends when you stop rather than when the game stops you: the score is the
purse, the best day and the best streak.
**END DAY** in the HUD shuts the stall early and banks what you have — the queue
leaves without penalty. Between days you visit **the Fixer**.

## 2. Why shelving matters

Selling is allowed from anywhere, but the source sets the price:

| source | multiplier |
|---|---|
| correctly shelved stock | **×1.0** |
| straight off the counter | ×0.6 |
| misfiled stock | ×0.5 |

The counter is an emergency valve, not a shop. From day 3 there are **five
categories and only three shelves** (four or five if you buy them), so which
categories you stock is the strategic choice; everything else is sold cheap off
the counter, misfiled, or scrapped at the barrel for 25 % of value. Click an
**empty** shelf's sign to relabel it.

## 2b. Bulk orders (build 8, from day 3)

**15 %** of customers from day 3 arrive with a **BULK ORDER** — `3 × MEDS`, or `4 × Mend Shot`
for the exact-item variant (sizes 2–4, weighted to 3). Their card is edged in amber and they
carry 45 % more patience, because filling an order takes time.

**Shift-click** items on the shelves or the counter to select them; selected slots get a gold
border and a number, and the selection is locked to one category (`SAME KIND ONLY` otherwise).
Every bulk card then shows a live `2/3` counter, and the side panel shows what you are holding.
**Drag any selected item** onto the buyer and the whole stack goes at once. `Esc` drops it.

Price is the sum of the individual prices — each keeping its own shelved/counter/misfiled
multiplier — times `min(2.4, (1 + 0.18 × count) × 1.2)`: **×1.63** for two, **×1.85** for three,
**×2.06** for four. Every item adds a streak step. A stack dropped on a shelf row bulk-files it;
on the barrel it scraps the lot; short of the order it bounces with a patience nick.

Bulk orders exist because the stall's takings are capped by how many customers it can serve in a
day (see the hired-hand appendix), so the way to grow is to make one customer worth more. They
also reward stacking a category **deep**, where the rest of the game rewards spreading stock
**wide** — the tested rig showed ~+44 % on the day at this rate. See Appendix 2.

## 3. Haggling (hold to raise, let go before it snaps)

Hold a matching item over a customer instead of dropping it:

- The price climbs at `0.55/s` (×1.5 with Silver Tongue) to a ceiling of **+50 %**
  (+75 % / +100 % with Silver Tongue levels).
- Their patience burns **3× faster** while you hold — **4.5×** for raiders and
  bandits.
- Hold 0.9 s *after* hitting the ceiling and they snap: **price back to base,
  patience −35 %, streak broken.** The bar flashes `LET GO!`.

## 4. Streak

Every correct file and every sale adds +1; prices get **+5 % per step**, capped at
×1.5 (streak 10). Broken by a misfile, an angry customer, a spill, scrapping an
item, or a greed snap.

## 5. Price formula

```
price = round( 0.5            (build 7: every sale pays half)
             × value
             × source      (1.0 shelved | 0.6 counter | 0.5 misfiled)
             × want        (1.4 exact item | 1.0 category)
             × customer    (0.80 – 1.45)
             × sign        (1 + 0.15 × Painted Sign level)
             × streak      (1 + 0.05 × min(streak,10))
             × haggle      (1 + 0 … 1.0) )
```

## 6. Goods (15 items, 5 categories)

| ARMS | MEDS | CHOW | TECH | JUNK |
|---|---|---|---|---|
| Zip Gun 26 | Mend Shot 32 | Clean Water 21 | Old Terminal 36 | Duct Tape 10 |
| Trench Knife 19 | Iodine Tabs 27 | Canned Beans 11 | Power Cell 29 | Scrap Plate 7 |
| Shotshells 15 | Field Wrap 13 | Ash Plum 9 | Circuit Board 17 | Tin Cans 5 |

Categories unlock by day: **day 1 opens ARMS / MEDS / CHOW / TECH**, and JUNK joins on day 2.
The stall starts with **four shelf rows**, one per opening category, so day 1 is a clean fit and
the squeeze starts on day 2 when junk arrives with nowhere to go. Salvaged Shelf is now a single
upgrade (215 c) that takes you to five rows.

## 7. Customers — 21 archetypes in three tiers

Tier 1 walks in from day 1, tier 2 from day 3, tier 3 from day 5.

| tier | type | patience | pays | wants |
|---|---|---|---|---|
| 1 | Wanderer | 26 s | ×1.00 | anything |
| 1 | Old Man | 32 s | ×0.85 | chow, meds |
| 1 | Child | 28 s | ×0.80 | chow, junk |
| 1 | Scavenger | 20 s | ×1.25 | tech, junk, arms |
| 1 | Trader | 24 s | ×1.15 | anything |
| 2 | Raider | 17 s | ×1.25 | arms, meds — **robs a shelf when he storms off** |
| 2 | Bandit | 18 s | ×1.20 | arms, junk — **robs** |
| 2 | Scout | 18 s | ×1.30 | chow, meds, tech |
| 2 | Mechanic | 22 s | ×1.20 | tech, junk |
| 2 | Medic | 24 s | ×1.20 | meds, chow |
| 2 | Engineer | 22 s | ×1.25 | tech, junk |
| 2 | Rat Mutant | 16 s | ×1.30 | chow, junk |
| 2 | Bloat | 26 s | ×1.10 | chow, meds |
| 3 | Soldier | 20 s | ×1.25 | arms, meds |
| 3 | Gunner | 17 s | ×1.35 | arms, tech |
| 3 | Sniper | 19 s | ×1.30 | arms, meds |
| 3 | Looter | 16 s | ×1.35 | arms, junk |
| 3 | Cultist | 22 s | ×1.30 | meds, tech, junk |
| 3 | Skinner | 15 s | ×1.45 | arms, meds |
| 3 | Rat King | 18 s | ×1.35 | chow, junk |
| 3 | Shiner | 20 s | ×1.40 | tech, meds |

35 % want a **specific item** (×1.4); the rest want any item from a category. A
wrong item costs them 10 % patience and bounces back — forgiving on purpose.

## 8. Day curve (rebalanced in build 2 — the old one was too steep)

```
length        90 s
rent          round(50 + 9 × (day−1)^1.15)        (build 3: growth cut 5×)
              d1 50 · d3 70 · d5 94 · d8 134 · d12 192 · d20 316
customer      day 1: 7.0 s, then max(2.7, 6.6 − 0.34×(d−1)) s
caravan       max(7.5, 14 − 0.6×(d−1)) s
crate size    3 + floor((d−1)/3), max 6
patience      ×max(0.68, 1 − 0.035×(d−1))
rush hour     at 50 % of the day: two crates + two extra customers
```

Bot-tested at two skill profiles over 14 days. Rent never threatens either: by day 14
it is 222 against 579 (slow player) to 2113 (fast player) earned. For reference, build 1
had rent at ~65 % of income and killed an average player by day 6; build 2 at ~45 %;
build 3 onward lands near 10 %.

**Consequence worth knowing:** chits now outrun their sinks. Every upgrade costs ~1,600
total and every cosmetic ~1,840, so a competent player owns everything by roughly day 9
and the purse just grows after that. If that starts to feel weightless, the fix is more
sinks (more cosmetics, a stall expansion, town projects) rather than steeper rent.

## 9. The Fixer (upgrades)

The Fixer is in two halves from build 10: **PASSIVE · always on** (the list below, plus the
hired hand) and **ACTIVE · press the key** (§9f). Builds 6 and 7 each raised every passive
price 20 %.

The stall has four shelf rows for the whole run — Salvaged Shelf was removed in build 11, so the
"five categories, four shelves" squeeze is permanent rather than something you buy your way out of.

| upgrade | effect | levels | cost |
|---|---|---|---|
| Wider Counter | +1 counter slot | 3 | 120 / 175 / 245 |
| Painted Sign | +15 % on every sale | 3 | 155 / 245 / 350 |
| Pot of Chicory | customer patience +2 % / +5 % / +8 % | 3 | 145 / 215 / 300 |
| Sorting Robo-Hand | a rusted arm that files for you every 9 s | 2 | 275 / 400 |
| Silver Tongue | haggle faster, higher ceiling | 2 | 215 / 320 |
| Hired Gun | raiders and bandits never rob you | 1 | 230 |

Chicory used to be +20 % patience a level (+60 % maxed); build 7 cut it to +2/5/8 %,
so it is now a nudge rather than a fix for a queue you cannot keep up with.

## 9b. The hired hand (build 6)

From **day 12** an eighth card appears at the Fixer: a hand for hire. She stands in the
stall beside you with her name over her head, and a second cursor in her colour works the
counter on its own — walking to a slot, pausing, picking an item up, carrying it, dropping
it, exactly as you do. Her priorities: serve the most impatient customer who can be served
from a shelf → serve one off the counter → file the counter → scrap what has no home once
the counter is nearly jammed. She haggles by holding over a customer and letting go at a
fraction of the ceiling set by her level.

**Hiring her opens a fourth customer window.** That is the point of her: the stall's
takings are capped by how many people it can serve at once, not by how fast one person
moves, so a second pair of hands raises the ceiling rather than competing for the same
sales. (The first integration had her competing, and she was a net loss for a quick player —
see the appendix.) Customer cards shrink to fit four.

You train her up between days, one level at a time, and each level unlocks three days after
the last:

| lvl | who | available | fee | wage | pace | files right | haggles to | perk |
|---|---|---|---|---|---|---|---|---|
| 1 | KIT · GREENHORN | day 12 | 450 c | 60 c/day | 180 px/s | 55 % | 40 % | — |
| 2 | MOSS · DRIFTER | day 15 | 675 c | 110 c/day | 330 | 70 % | 55 % | — |
| 3 | CASS · HAND | day 18 | 975 c | 170 c/day | 520 | 83 % | 70 % | — |
| 4 | VEK · RUNNER | day 21 | 1350 c | 230 c/day | 740 | 93 % | 85 % | +10 % on her sales |
| 5 | SOLA · ROADWISE | day 24 | 1800 c | 290 c/day | 960 | 99 % | 96 % | +25 % on her sales |

Build 7 made the ladder start much lower — a greenhorn now moves at 180 px/s (half build 6's
pace) and shelves barely half of it correctly — so that each level is a visible improvement
rather than a small one. Fees went up 50 %; the daily wages did not (see the warning below).

**Standing her down.** The day-intro card carries a toggle: `KIT WORKS TODAY · -60c` or
`KIT SITS OUT · NO WAGE`. Standing her down pays no wage, keeps her off the floor, and
closes the fourth customer window — `queueRows()` follows whether she is actually working,
not whether she is on the books.

The wage comes out of the purse at dusk alongside the rent, and the report shows what she
brought in against what she cost. She **shares your streak**: her good files build it and
her misfiles break it, which is what makes a greenhorn genuinely irritating and a reason to
train her.

**Warning, measured after build 7 (10 days each, day-16 pacing, mid-speed player bot):**

| hand | takings | sales | spilled | net after rent + wage |
|---|---|---|---|---|
| none | 406 c | 16 | 17 | +153 c |
| lvl 1 (60 c) | 524 c | 23 | 20 | **+211 c** |
| lvl 3 (170 c) | 536 c | 24 | 14 | +113 c |
| lvl 5 (290 c) | 573 c | 24 | 11 | +30 c |

Halving sales inverted the ladder: **training her up now makes you poorer.** Almost all of a
hand's value is the fourth window, which level 1 already opens; the extra takings between
level 1 and level 5 are only ~50 c against wage steps of 110–120 c. Two ways out, neither
applied yet: flatten the wages (roughly 60 / 80 / 100 / 125 / 150) so the steps cost less
than they add, or give the top levels a bigger gross edge — a fifth window at level 4, or
sale bonuses of +20 % / +45 % instead of +10 % / +25 %.

## 9f. Active perks (build 10)

Four perks you *press*, each answering one specific way the stall goes wrong — so the decision
is *which crisis am I in*, not which rotation I am on. Each is bound to a number key for the
life of the run.

| key | perk | what it does | cooldown | cost |
|---|---|---|---|---|
| 1 | **COUNTER SWEEP** | files every counter item that has a free matching shelf slot, instantly | 30 s | 240 c |
| 2 | **STEADY HANDS** | refills every waiting customer's patience and freezes it for 3 s | 45 s | 280 c |
| 3 | **HARD PATTER** | 10 s of +50 % prices; the haggle bar fills 3× faster and cannot snap | 50 s | 320 c |
| 4 | **THE BACK ROOM** | fills your emptiest shelf row with four items of its category | 60 s | 300 c |

Each has a cost elsewhere: Sweep spends your filing advantage, Steady buys time you then have to
use, Patter is loud but brief, and the Back Room hands you stock you did not choose.

**The rail.** A column down the left edge of the play screen, clear of the panels: owned passives
in a 3-wide grid on top, owned actives below, each showing its icon, its key in a badge, and
either `READY` or the seconds left — the box drains from the top as it recharges. Clicking an
icon fires it as well as the key. A lasting effect shows a countdown strip under the rail.
**Only what you own appears**; the rail packs up as you buy, so it grows with the run instead of
showing a wall of locked slots.

**Hovering any icon opens a description panel** beside it: what the perk does, and its state —
level owned and the next price for a passive, key, cooldown and seconds remaining for an active.

Measured in the rig at +29 % on the day with passives switched off, and a quarter fewer walk-outs.
See Appendix 3, including the open question about cooldown length against a 90-second day.

### How long the shop lasts

Bot-measured over full runs, buying cheapest-first every night:

| | all passives maxed | all four actives | **every perk** | hand at level 5 |
|---|---|---|---|---|
| fast player | day 11 | day 10 | **day 11** | day 24 |
| average player | day 11 | day 10 | **day 11** | day 24 |

Every perk costs **4,530 c** in total (3,390 c of passives, 1,140 c of actives) and both a fast and
an average player clear the lot by **day 11**. The hired hand is another 5,250 c but is gated by day, not by
money — levels open on days 12 / 15 / 18 / 21 / 24, so **day 24 is a hard floor** however well you
trade.

**The problem this exposes:** after day 11 the only sink left is cosmetics (~2,700 c, drip-fed to
day 20), and the purse runs away — 11,800 to 13,800 c by day 24 with nothing to spend it on. The
shop stops being a decision about a third of the way into a long run. Fixes worth considering, in
rough order of effort: stretch the perk prices so the last ranks cost multiples of the first;
gate perks by day the way the hand is gated; or add a recurring sink (restocking the caravan,
repairs, bribes) so chits drain as well as fill.

## 9c. The walkthroughs (build 8)

Two scripted lessons, each freezing the clock, the caravans, the queue and every patience bar
while it runs (`tutFrozen()`), with a SKIP in the banner. They run once per run and glow the
thing you are meant to touch.

**Day 1 — the stall.** One item on the counter, one on the meds shelf, nothing else.
*The caravan left you something* → *drag it onto the meds shelf* (counter slot and shelf row
pulse) → a settler walks up wanting meds, *now sell it* → a scavver follows, *hold it over him
to haggle* → *that is the job*. Each step waits for the player to actually do it; the haggle
step also releases after 16 s so nobody gets stuck.

**The cards wait for you.** A step that is only text — the opening card of either lesson, and the
closing one — holds until the player clicks, with a blinking *click anywhere to carry on*. Only the
steps that ask for an action advance on the action. The first version auto-advanced the opener after
1.2 s, which read as the tutorial skipping itself.

**The lesson takes its props back.** Everything a lesson puts on a shelf — the pre-placed stock and
anything `lessonStock()` tops up — is recorded in `TUT.gave`, and on `lessonFinish()` any of it still
sitting untouched is removed with a puff of dust. Identity is checked per item object, so nothing the
player filed or earned is ever taken. Without this the lesson left free stock on the shelf, which read
as a sale that had not gone through.

**Nobody walks out of a lesson.** Patience is frozen while one runs, the wrong-item and greed
penalties do not apply, and the haggle step has no timeout — it waits for the sale. The first
version of the freeze had a nasty bug worth remembering: gating the spawn block on `tutFrozen()`
sent its `else` branch — which accumulates `S.overtime` — running during the lesson, so after
30 s the game's closing-time rule force-marked every customer as leaving. A player who spent half
a minute reading the banner watched their buyer walk off. `S.overtime` now only accumulates when
the stall is actually closing.

**Both lessons are self-healing.** A tutorial that can dead-end is worse than none, so every
step that needs props checks for them each tick: if the lesson buyer is missing — walked off,
served early, lost to any edge case — another is sent in, and if the shelf it teaches from runs
dry it is topped up. The day-1 step also advances on the counter simply being *clear*, however
the player dealt with the item (filed, misfiled, or scrapped), rather than on a specific shelf
count that a misfile could make unreachable.

**Day 3 — bulk orders.** A medic arrives with a 3 × MEDS order and one shelf is pre-stocked with
four meds. *A bulk order* → *hold shift and click three meds* (matching slots pulse) → *now drag
one of them onto him* → the sale, with the multiplier named. Shift-select is not discoverable —
nothing else in the game uses shift — so it gets taught rather than hinted.

## 9d. The top bar and the morning paper (build 9)

**The bar never leaves.** `drawHUD()` is drawn last, over every screen except the title and the
game-over card, so the purse, the rent due and the day are readable in the Fixer, the dressing
room, the ledger and the paper. Pause and End Day only appear during play; elsewhere that corner
names the screen you are on.

**The morning paper.** Dusk now runs report → **THE DUST HERALD** → ledger (every fifth day) →
the Fixer. The paper is drawn as aged newsprint — masthead, rule, dateline, a pixel photograph of
the east road (`buildPaperImg()`, a 96×54 greyscale plate blown up ×3), the headline *MEDS PRICES
GO UP!* with two paragraphs of copy, and three filler columns. It is **flavour only** — no prices
move, nothing is scored. It exists to give the town a voice between days and as the hook for real
market events later.

## 9e. Perk icons (build 9)

Every Fixer card carries a square 8×8 pixel icon in a bordered badge — shelf rails, counter cells,
a signboard, a chicory pot, a claw, a speech bubble, a shield, and a figure for the hired hand.
They are drawn from `PERK_PX` through `perkBadge()`, and they grey out until the perk is owned or
affordable.

**The robo-hand is visible on the trader.** Buying Sorting Robo-Hand adds a `roboarm` prop to the
trader's sprite: a rusted mount behind his back and an arm arching up over his shoulder with a
two-finger claw above the hat. It is 70 pixels of sprite and reads clearly at the stall's scale —
the first upgrade in the game you can see on the character. `traderSprite()`'s cache key includes
it, and buying it invalidates the cache.

## 10. Customisation

After the day's takings are counted, **the Fixer → STALL & LOOKS** opens a dressing room
with two live previews: a crop of the real stall front (the actual scene canvas, so what
you see is exactly what the town sees) and the merchant himself.

**Try before you buy.** Clicking any unlocked option simply *wears* it — the stall and the
trader repaint at once and nothing is charged. Unowned pieces you are wearing are marked
`TRYING`, and a **BUY THE LOOK · Xc** button shows the total for everything on trial, so
you can assemble a whole outfit and pay once. Leaving the screen (Back, or Open Tomorrow)
drops anything unpaid back to what you own. Internally `S.look` is what is *displayed*,
`S.worn` is what is *paid for*; `tryList()` is the difference.

**Options unlock over time** — each carries an `un` (unlock day) and renders locked with
`DAY n` until then. Colours arrive often, textures occasionally, costumes rarely. The day
intro announces the day's arrivals ("NEW AT THE FIXER: 1 colour · 1 costume") and the
Fixer's button gets a `*` on those days.

| row | options (unlock day) |
|---|---|
| Merchant · hat | brim 1 · bare 2 · cap 3 · hood 5 · cowl 8 · helm 11 · mohawk 15 · crown 19 |
| Merchant · coat | dust 1 · olive 2 · storm 4 · rust 6 · plum 9 · soot 12 · bone 16 · teal 20 |
| Merchant · face | bandana 1 · bare 2 · goggles 4 · gasmask 9 · skull 17 |
| Stall · awning | red 1 · green 2 · blue 3 · ochre 5 · violet 7 · grey 10 · wine 14 · jade 18 |
| Stall · cloth | plain 1 · solid 6 · banded 11 · patched 16 |
| Stall · wall | planks 1 · tin 7 · brick 13 · painted 18 |
| Stall · lanterns | warm 1 · green 4 · cold 8 · ember 12 · violet 17 |
| Stall · flag | red 1 · green 3 · yellow 5 · black 9 · white 14 |
| Stall · sign | free text, up to 10 characters, free |

Costs run 50–200 c. Cloth patterns and wall textures are drawn procedurally inside
`buildScene()`; changing any stall option calls `invalidateLook()`, which nulls the cached
scene canvas so it rebuilds on the next frame. Everything owned and worn persists across
runs in `localStorage` (`rustrations.look` = `{look, owned}`).

## 11. The ledger (every 5 days)

On every fifth dusk the report's button becomes **READ THE LEDGER**, and the Fixer keeps a
`THE LEDGER` button so it can be reopened any time. It is a green-phosphor CRT — bezel,
scanlines, a slow flicker — showing the last 10 days:

- **TAKINGS PER DAY** — a bar per day with the night's rent drawn across it as a gold
  notch, so profit vs rent reads at a glance.
- **SERVED / WALKED OUT** — paired bars per day, green against red.
- **TAKINGS BY SHELF** — horizontal bars per category, which is the only place the game
  tells you what the town actually buys.
- **THE BOOKS** — takings, rent paid, net, sales, average sale, best day, best streak,
  walked out / spilled — closed by a summary line with the window's takings trend and the
  best-selling shelf.

`S.history` collects one record per day at `endDay()` (`{day, earned, rent, sold, angry,
spilled, combo, cat:{…}}`); per-category takings accumulate in `S.catEarn` inside
`sellTo()` and reset each morning.

## 12. Art (build 2)

Everything is drawn in code — no image files.

- **Sprite engine.** `spriteFrom(rows, palette)` turns arrays of strings into an
  offscreen canvas, one character per pixel; `blit()` draws it with
  `imageSmoothingEnabled = false` at an integer scale.
- **Items** are hand-authored 16×16 grids in `ITEM_PX`, drawn at ×3 (×2 in a
  crowded shelf). Category badges are 8×8.
- **Characters** are procedural: `drawChar(cfg)` paints a 22×32 sprite from a
  config — build (`norm/big/small/hunch/robe`), skin, coat, face
  (`eyes/goggles/mask/skull/dark/snout/bandana`), headgear
  (`brim/cap/helmet/hood/cowl/mohawk/spikes/hair`) and props (rifle, backpack,
  cane, staff, wrench, toolbox, case, ammo, glow, tentacle, rats). One config per
  archetype, cached on first use.
- **The stall** is one 320×190 canvas built once (`buildScene`) and blitted at ×4:
  sunset bands, a pixel sun, two ruin skylines, pylons, a wrecked car, the timber
  stall with awning, sign, lanterns and counter. Fire, lantern glow, the flag and
  the trader's idle bob are drawn per frame on top.
- **UI** uses hard-edged chamfered `plate()` panels and `bar()` meters, no
  antialiasing, with the Silkscreen pixel font.

## 13. Controls

Drag with the mouse — that is the whole verb. `Space`/`Esc` pauses, `M` mutes.
Audio is a small WebAudio synth (grab, drop, file, coin, angry, caravan horn).

## 14. Known gaps / next passes

- No bulk orders, no regulars, no reputation rewards beyond price.
- Characters are procedural silhouettes, not hand-pixelled portraits; the
  archetype configs are the place to add detail.
- Single stall, single town — you take what the caravan brings.
- Endless: no win state, only a best-day record in `localStorage`
  (`rustrations.best`).
- Chits still outrun their sinks late, though the drip-fed cosmetics (~2,700 c spread
  over 20 days) now soak up a lot more of the surplus than build 3 did.
- The early game is very tight after the 50 % sale cut: a mid-speed player nets ~16 c on
  day 3 and ~37 c on day 8 against upgrades that start at 120 c, so the first purchase is
  now many days away.
- The hand's attributed takings swing wildly (25–220 c a day) because whoever reaches the
  customer first books the sale; the honest measure of her worth is the day's total, not her
  column.
- With town mood gone and rent gentle, there is no real fail state. If tension is wanted
  back, it should come from something the player controls — a visible morning quota, or a
  counter that jams harder — not from a meter that random customer wants can drain.

## 15. Testing hooks

`window.tick(dt)` drives the simulation directly (the browser pane throttles rAF
when hidden), `window.S` is the whole state, `window.__errors` counts uncaught
errors, and `window.__api` exposes `startRun`, `spawnCrate`, `spawnCustomer`,
`place`, `sell`, `freeShelfSlot`, `wantsMatch`, `salePrice`, `rentFor`,
`charSprite` and the slot-rect helpers — enough to write a bot player, which is
how the economy above was tuned.

---

# Appendix — the hired-trader test v2 (`hired-trader-demo.html`)

A **separate** fork of build 5, not part of the game. It answers one question: what is a
hired hand worth, and how much should each level of one cost?

**What it is.** A second cursor works the counter on its own. She walks to a slot, pauses,
picks the item up, carries it, and drops it — the same drag the player makes, at human
speed. Priorities in order: serve the most impatient customer who can be served from a
shelf → serve one straight off the counter → file a counter item → scrap something with no
home once the counter is nearly jammed. She haggles by holding over the customer and
letting go at a fraction of the ceiling set by her level.

Both cursors are live: the player can work alongside her, and either can take the item the
other was walking toward (both re-plan). `YOU HELP / HANDS OFF` locks the player out so a
day can be watched clean.

## The five hands

| lvl | who | pace | reaction | files right | haggles to | perk | wage |
|---|---|---|---|---|---|---|---|
| 1 | KIT · GREENHORN | 360 px/s | 0.62 s | 68 % | 45 % of ceiling | — | 100 c |
| 2 | MOSS · DRIFTER | 480 | 0.48 | 80 % | 62 % | — | 160 c |
| 3 | CASS · HAND | 620 | 0.37 | 89 % | 78 % | — | 220 c |
| 4 | VEK · RUNNER | 790 | 0.27 | 95 % | 88 % | +10 % on her sales | 280 c |
| 5 | SOLA · ROADWISE | 960 | 0.19 | 99 % | 96 % | +25 % on her sales | 340 c |

Each level gets its own cursor colour and name tag. `COMPARE ALL` in the test bar runs
every level headlessly over two day loads and prints the table below — five levels × two
loads × 12 days in about a third of a second.

## Measured (20-day averages, hands off)

| lvl | quiet take (d5) | busy take (d12) | sales q/b | misfiles | spilled q/b |
|---|---|---|---|---|---|
| 1 | 235 c | 248 c | 10.2 / 11.5 | 2.8 | 18 / 63 |
| 2 | 323 | 360 | 11.6 / 14.3 | 2.3 | 16 / 59 |
| 3 | 426 | 426 | 12.7 / 14.9 | 1.8 | 14 / 56 |
| 4 | 409 | 564 | 12.1 / 17.4 | 0.9 | 11 / 51 |
| 5 | 511 | 666 | 13.5 / 18.9 | 0.2 | 10 / 48 |

**Three things the numbers say.**

1. **Sales count is capped by customer supply, not by her speed** — every level sells
   10–13 on a quiet day. Almost all of a better hand's extra income is *price per sale*
   (streak kept alive, better haggling), which is why levels 4 and 5 needed an explicit
   per-sale bonus to be worth their wage at all.
2. **A cheap hand drowns as the road gets busier.** Level 1 earns *less* on a busy day than
   a quiet one in some runs, and spills 63 items against level 5's 48. The gap between top
   and bottom widens from 2.2× on a quiet road to 2.7× on a busy one.
3. **The shared streak is the real cost of a cheap hire.** Hands-off numbers hide it: beside
   a player who is building a multiplier, three misfiles a day is expensive in a way the
   hire's own takings never show.

**Design read.** Wages priced at ~40 % of takings leave every level profitable, which means
the best hand you can afford is always correct and the level choice collapses. If levels are
meant to be a progression, the lever should be **availability** — a given level shows up at
the Fixer on a given day — with price as a secondary gate. Left open: whether a hire should
have her own streak instead of sharing yours, and whether the player should be able to
assign her a lane (file only, never sell).

---

# Appendix 2 — bulk orders test (`bundles-demo.html`)

A **separate** fork of build 7, not part of the game. It tests one idea against the
bottleneck the hired-hand tests found: the stall's takings are capped by how many customers
it can serve in a day, so the way to grow is to make each customer worth more.

**Encores are parked.** The first pass also tested an "anything else?" second want after each
sale; it worked (+67 % on its own) but was set aside. The code is still in the file behind
`DEMO.encore`, switched off.

## The mechanic

**15 %** of customers arrive with a **BULK ORDER** — `3 × MEDS`, or `4 × Mend Shot` for the
exact-item variant (sizes 2–4, weighted to 3). Their card is edged in amber and they carry
45 % more patience, because filling an order takes time.

**Shift-click** items on the shelves or the counter to select them; selected slots get a gold
border and a number. The selection is locked to one category — a second category is refused
with `SAME KIND ONLY`. While a selection exists, every bulk order shows a live `2/3` counter
and the side panel shows what you are holding. Then **drag any selected item** onto the buyer
and the whole stack goes at once. `Esc` drops the selection.

Price is the sum of the individual prices (each keeping its own shelved/counter/misfiled
multiplier) times a bulk bonus of `min(2.4, (1 + 0.18 × count) × 1.2)` — **×1.63** for two,
**×1.85** for three, **×2.06** for four. Every item in the bundle adds a streak step.

A stack dropped on a shelf row bulk-files it, and one dropped on the barrel scraps the lot.
Dropping a short stack on a bulk buyer costs a little patience and is counted as an order
dropped short.

## The walkthrough

The test day opens with a scripted lesson, because the verb is not discoverable — nothing
else in the game uses shift. The clock, the caravans and the queue are all frozen while it
runs. A MEDIC walks up with a 3 × MEDS order, one shelf is pre-stocked with four meds, and
three prompts step through it: *a bulk order* → *hold shift and click three meds* (the
matching slots pulse) → *now drag one of them onto him* (the card pulses) → the sale, with
the multiplier named. Each step advances on the player actually doing it, and a SKIP button
sits in the banner. It runs once; the `LESSON` toggle on the test bar replays it.

## Measured (14 days each, same bot, 0.85 s reaction, day-8 pacing)

| bulk buyers | takings | served | **per customer** | orders filled | from bulk | walked out |
|---|---|---|---|---|---|---|
| off | 357 c | 14.2 | 24.9 c | – | – | 5.9 |
| 10 % | 428 c | 10.9 | 38.9 c | 1.4 | 192 c | 7.5 |
| **15 %** | **515 c** | 13.1 | 38.5 c | 2.1 | 248 c | 6.1 |
| 25 % | 510 c | 12.1 | 43.9 c | 2.5 | 277 c | 6.1 |

At 15 % the day earns **44 % more** than with the mechanic off, and **roughly half the day's
takings come from two of thirteen customers**. Per-customer value is up 55 %.

The +20 % price rise did the work it was meant to: at the old 30 % rate and old multiplier a
bulk order was worth ~91 c; at 15 % with the new one it is worth ~118 c. Fewer of them,
each worth substantially more — which is the shape that makes them feel like an event rather
than a chore.

Pushing to 25 % does not earn more in total (510 c) despite filling more orders, because bulk
buyers occupy queue slots you may not be able to fill. **15 % looks like the right rate.**

**What the mechanic actually changes:** bulk orders reward stacking a category **deep**, where
the game has so far rewarded spreading stock **wide**. That is a genuinely new decision on the
shelf wall, and it is the reason to keep them.

## Test rig controls

The bar toggles bulk orders, sets the rate (10/15/25 %), shows the current bulk multipliers,
and replays the lesson. The dusk panel reports takings split by source, orders dropped short,
per-customer takings, and a comparison against the previous run.

---

# Appendix 3 — active perks test (`perks-demo.html`)

A **separate** fork of build 9, not part of the game. Every perk in the game so far is passive:
you buy it and forget it. This rig splits the Fixer in two and asks whether perks you *press*
add anything.

## The Fixer in two halves

**PASSIVE · always on** — the seven existing upgrades plus the hired hand, unchanged.

**ACTIVE · press the key** — four new perks, each bound to a number key for the life of the
run. Each answers one specific way the stall goes wrong, so the decision is *which crisis am I
in* rather than *which rotation am I on*.

| key | perk | what it does | cooldown | cost | the moment |
|---|---|---|---|---|---|
| 1 | **COUNTER SWEEP** | files every counter item that has a free matching shelf slot, instantly | 30 s | 240 c | the counter is jammed |
| 2 | **STEADY HANDS** | refills every waiting customer's patience and freezes it for 3 s | 45 s | 280 c | three people are about to walk |
| 3 | **HARD PATTER** | 10 s of +50 % prices; the haggle bar fills 3× faster and cannot snap | 50 s | 320 c | you need chits now |
| 4 | **THE BACK ROOM** | fills your emptiest shelf row with four items of its category | 60 s | 300 c | the shelves are bare |

Each one is a single keystroke with a visible cost elsewhere: Sweep spends your filing advantage,
Steady buys time you then have to use, Patter is loud but brief, and the Back Room gives you
stock you did not sort (so no misfiles, but no choice about what arrives either).

## Both rails live on the left

A column down the left edge of the play screen, clear of the panels. Owned passives sit in a
small 3-wide grid at the top; the four active slots sit below it, each showing its icon, its key
in a badge, and either `READY` or the seconds remaining — the box drains from the top as it
recharges. Clicking an icon fires it too, for anyone who would rather not use the keyboard.
An active effect that lasts (Patter, Steady) shows a countdown strip under the rail.

## Measured (12 days each, passives switched off so the actives are measured alone)

| | takings | sales | walked out | spilled | uses per day |
|---|---|---|---|---|---|
| actives off | 399 c | 11.9 | 6.8 | 3.1 | – |
| actives on | **516 c** (+29 %) | 12.3 | **5.2** | 3.3 | 1.7 / 1.1 / 2.0 / 1.0 |

Worth about **+29 % on the day**, and the walk-out count drops by a quarter — Steady Hands
earning its place. Note the bot fires each perk only one or two times in a 90-second day; a
player watching the rail would use them more.

**The open question is cooldown length.** Against a 90-second day, a 60-second cooldown means The
Back Room is a once-a-day lifeline and Patter is twice at best. That reads as "emergency button"
rather than "rotation", which is the intent — but if they should feel like part of the minute-to-
minute rhythm rather than a panic move, every cooldown wants roughly halving.

## Test rig controls

`GIVE ME EVERYTHING` in the bar hands you every passive at max and all four actives, so the perks
can be felt without a shopping trip first. The bar also tracks how many times each was used, and
the dusk panel reports uses against the theoretical maximum the cooldown allows.


---

## Appendix — build 12: brush-art reskin (REJECTED, reverted — kept as `v12-build12.html`)

> The user did not like this look; `index.html` is back on build 11 (pixel art). Notes kept for reference only.

Rules, numbers and layout are untouched; only the drawing layer changed. The last pixel
build is kept as `v11-build11-pixel.html`. Source paintings and the cutting scripts live
in `art-src/`.

| Piece | Where it comes from |
|---|---|
| Backdrop | `art-src/background.png`, cover-cropped to 1280×760, embedded as JPEG |
| Stall (posts, awning, sign board) | cut out of `art-src/ui-elements.png`, background keyed to alpha |
| Customers (21 types) | cut out of `art-src/characters.png` — flood-fill key + hole fill so dark clothing survives |
| Hired hand, levels 1–5 | spare sheet figures: woman scavenger, hunter, sniper woman, engineer woman, medic |
| Panels, cells, buttons, frames | procedural brush strokes (`stroke()` — bundles of loose dabs), cached per size. Timber colours collapse onto one beam brown; signal colours (gold/green/red) get a finer line |
| Items, category + perk icons, cursor | the old 16×16 / 8×8 sprites run through `paint()`: upscale ×6, blur, noisy alpha threshold, streaky grain |
| Newspaper photo | the backdrop painting through a sepia newsprint wash |
| Trade ledger | deliberately still a green CRT — it is a machine in the world |

**Customisation in paint.** Hats are now *costumes*: each hat is a painted figure from the
sheet, the face option picks a variant of it (`COSTUME` table), and the coat colour is dyed
into the paint (DUST leaves it as painted). Awning colour and cloth pattern are dyed into
the stall cutout, the flag into the backdrop; wall and lantern are painted procedurally.
The Sorting Robo-Hand is a brush-stroke arm drawn behind whichever figure is worn.

Dev hook: `window.__zoom={x,y,k}` magnifies a region of the canvas for inspection.


---

## Appendix — crafting test (`crafting-demo.html`, separate rig)

Route C of the "scale to 3-4 hours" options. The main game is untouched. 7-day run, caravans
**off** by default (menu toggle turns them back on).

**Loop:** day intro → **workshop** (untimed) → trading day → dusk → next day. Fixer, looks,
ledger and paper are skipped so the loop repeats fast.

**Workshop.** Left: material market, fixed prices — Scrap 1, Cloth 1, Grain 1, Timber 2,
Herbs 2, Glass 2, Chem 3, Wire 4; Fine Parts 9 (day 3) and Relic Core 24 (day 5) are
refine-only. Centre: recipe book by category (every good = two materials, click to craft
into an 18-slot tray), the **anvil** (drag an object on, pay the bill, it goes up a tier —
deterministic), the tray. Right: the four shelves; what you shelve is what you open with,
and unsold stock stays overnight. Anything left in the tray rides along as **back stock**:
it feeds onto the counter one piece every 1.6 s while there is room, so the file-it-fast
loop survives without caravans. Unsold back stock returns to the tray next morning.

| Tier | Value | Refine bill (A, B = the recipe's two materials) | Opens |
|---|---|---|---|
| Common | x1 | recipe: 1 A + 1 B | day 1 |
| Rare | x2.2 | 2 A + 1 B | day 1 |
| Epic | x5 | 3 A + 3 B + 1 Fine Parts | day 3 |
| Legendary | x12 | 4 A + 4 B + 2 Fine Parts + 1 Relic Core | day 5 |

**Purse.** Customer tier = richest rarity they pay full price for (tier 1 → Rare, 2 → Epic,
3 → Legendary), shown as pips by the name. Above it they pay their cap and the price plate
says `PAYS AS RARE` before you drop. No randomness anywhere in crafting.

**Recipes by day:** 1 Zip Gun, Field Wrap, Canned Beans, Circuit Board · 2 Tin Cans,
Shotshells · 3 Mend Shot, Clean Water · 4 Power Cell, Duct Tape · 5 Trench Knife, Ash Plum ·
6 Iodine Tabs, Old Terminal, Scrap Plate. Exact-item wants only ask for opened recipes.

**Bot results (instant-reaction seller, start purse 80c, same rent curve):**
commons only → takings fall to ~50-75c/day and the run dies on day 6; refine to Rare →
~180-410c/day, purse 688c on day 7; refine everything → slower start, 823c on day 7, purse
763c. So refining is mandatory, Rare is the safe line, Epic/Legendary pay off only from
day 4-5 when rich buyers arrive. First finding fixed during the build: without caravans the
16 shelf slots capped a whole day's sales — hence back stock. Still open: the bot leaves
5-9 walk-outs a day because four shelves cannot cover five categories plus exact-item asks.


---

## Appendix — build 12: the workbench joins the main game

The crafting rig and the main game now share one crafting module (generated into both files
from the same source; `CRAFT.demo` switches behaviour).

**Changes made to crafting first (both files):**
- **Scrap bin** in the workbench (last tray cell). Drop any object on it: half of every
  material that went into it comes back, at least one of its first material. The bin shows
  what you will get before you let go.
- **Materials cost double:** Scrap 2, Cloth 2, Grain 2, Timber 4, Herbs 4, Glass 4, Chem 6,
  Wire 8, Fine Parts 18, Relic Core 48. A flat doubling would have made a third of the
  recipes loss-making (goods sell at about half their value), so the cheap goods now come
  out **two per craft**: Field Wrap, Canned Beans, Circuit Board, Tin Cans, Shotshells,
  Duct Tape, Ash Plum, Scrap Plate. Every recipe costs roughly 25-55 % of what it sells for.
- **Workbench walkthrough**, first visit only: starter kit (6 Scrap, 4 Timber, 2 Cloth) →
  click the Zip Gun recipe → drag it to the anvil → press REFINE → put it on a shelf →
  closing card on the market, the scrap bin and purse pips. Text cards wait for a click,
  action steps advance on the action, SKIP is always there. One lesson, one kit per run.

**In the main game:**
- The Fixer's bottom row is now STALL & LOOKS · THE LEDGER · **WORKBENCH · 1000c** ·
  TOMORROW. Hovering the locked button explains it; buying it opens the bench at once.
- The bench is a night screen: you craft for **tomorrow**. Recipe and tier calendar counts
  from the day you bought it (4 recipes and Rare at once, +2 recipes a day, Epic on bench
  day 3, Legendary on bench day 5, everything by bench day 6).
- Caravans stay on. There is no back stock here — the tray simply keeps goods until you
  shelve them. **Once you own the bench, shelf stock keeps overnight** (before that the
  shelves are cleared every morning as in build 11).
- Rarity frames, `PAYS AS RARE` warning and purse pips appear on the trading screen (pips
  only once the bench is owned). Rarity is a variant item object with the same id, so
  the hired hand, robo-hand, bulk orders and active perks handle refined goods unchanged.
- Dusk report lists materials bought the night before (already paid, for information).

**Verified:** unlock refused when poor, 1000c deducted when rich, walkthrough end to end,
scrap yields, paired crafts, stock surviving the night, 20-24 day bot runs through every
screen with zero errors. **Not reliably measured:** how much the bench is worth. My selling
bot barely uses it, and because stock now keeps overnight and caravans keep delivering,
shelves are rarely empty at night — making room (selling out, scrapping leftovers) is the
real cost of crafting in the main game.


---

## Appendix — build 13 (supersedes the numbers above where they differ)

| # | Change |
|---|---|
| 1-3 | Active perk prices: Counter Sweep **600c**, Hard Patter **1000c**, The Back Room **1200c** (Steady Hands stays 280c). |
| 4 | **Stock always keeps overnight** (shelves and counter). The dusk report, when anything is left, offers `SCRAP THEM +Nc` (25 % of value each, the barrel rate) or `KEEP THEM`. If rent broke you but the leftovers would cover it, the report offers `SCRAP IT ALL TO MAKE RENT` instead of ending the run. |
| 5 | **The hired hand is an active perk, key 5.** KIT works the stall for **5 / 8 / 12 s** at level 1 / 2 / 3 (**2000 / 2500 / 3000c**), then rests 40 s (cooldown starts when she clocks off). No day gate, no wage, no morning toggle, no fourth customer window (the queue is always three). One stat line for all levels: 740 px/s, 93 % correct filing, haggles to 85 % of the ceiling, +10 % on her sales. Anything in her hand when time runs out goes back to the counter. |
| 6, 10, 11 | **Materials x8:** Scrap / Cloth / Grain 16, Timber / Herbs / Glass 32, Chem 48, Wire 64. **Fine Parts 1000c**, opens 5 days after the bench; **Relic Core 2000c**, opens after 10. Epic and Legendary work open on the same days. |
| 7 | **CONTROL-click (or right-click) scraps an item** on the counter or a shelf, same 25 % as the barrel; at the bench it returns half the materials. Day-1 lesson gained a step after the haggle sale: tin cans land on the counter, scrap them (either way), then the closing card. |
| 8, 9 | Caravan goods after **day 10: 5 % Rare**; after **day 15: also 1 % Epic**. Purse pips show from day 11 even without the bench. The Back Room still conjures Commons. |
| 12 | No JUNK tab at the bench. |
| 13 | The Dust Herald prints on **day 5, 9, 13, 17…** only; other nights go straight to the ledger/Fixer. |

### (Superseded by build 14) Warning: at these material prices the bench cannot pay for itself
Goods sell for about half their value, so:

| Object | Costs to make | Sells for about |
|---|---|---|
| Zip Gun, Common | 48c | 13c |
| Zip Gun, Rare | 112c | 29c |
| Old Terminal, Common | 96c | 18c |
| Old Terminal, Legendary | 5,928c | 216c |

Even with every price perk, a streak and a perfect haggle (roughly x4) a Common Terminal
reaches ~70c against 96c of materials. As it stands the bench is a pure chit sink. If it is
meant to earn, crafted goods need a value multiplier of their own (about x6 at these prices),
or the x8 should apply to refine bills only.


---

## Appendix — build 14: making the bench pay

- **Hand-made goods are worth x8** (`CRAFT.mult`) a caravan piece of the same tier. Crafted is a
  variant flag like rarity (`rar(item,r,crafted)`), marked by a tan frame and a maker's notch,
  `HAND-MADE` in the drag label. Caravan Rares/Epics and Back Room stock do **not** get it.
- **Tier values:** Common x1, Rare x2.2, **Epic x6** (was 5), **Legendary x16** (was 12).
- **Fine Parts / Relic Core are one-time unlocks** — 1000c (bench day 5) and 2000c (bench day
  10) — then ordinary materials at 144c / 384c. The anvil says so when a refine is blocked.
- **Scrap value ignores the x8** (barrel, CONTROL-click, dusk scrap, the hand's strand), or a
  fresh Zip Gun (48c of materials) would scrap for 52c.
- Circuit Board is now Cloth + Wire (was Wire + Cloth) so its Rare refine costs 96c, not 144c.

Cost to make > plain sale (half of value, no bonuses):

| | Common | Rare | Epic | Legendary |
|---|---|---|---|---|
| Zip Gun | 48 > 104 | 112 > 229 | 400 > 624 | 1264 > 1664 |
| Mend Shot | 80 > 128 | 192 > 282 | 576 > 768 | 1568 > 2048 |
| Old Terminal | 96 > 144 | 256 > 317 | 688 > 864 | 1744 > 2304 |
| Circuit Board (x2) | 40 > 68 | 136 > 150 | 520 > 408 | 1512 > 1088 |
| Ash Plum (x2) | 16 > 36 | 64 > 79 | 304 > 216 | 1104 > 576 |

Cheap goods lose above Rare on purpose: what you refine is a decision.

### Measured, and it matters: x8 runs away in real play
The table above is the *plain* price. Real late-game sales carry sign, streak, haggle, exact
match and buyer generosity — roughly x2.3 on top — and every one of those multiplies the
hand-made value too. A bot that fills the shelves with crafted Rares each night, 20 days:

| `CRAFT.mult` | purse on day 20 | takings/day, last 8 days |
|---|---|---|
| no bench | ~2,200c | ~300c |
| x2.5 / x3 | ~580c (bench loses money) | 1,000-1,500c |
| x4 | ~2,000c (break-even with no bench) | ~2,300c |
| x5 | 10,700-15,700c | ~3,300c |
| x6 | ~25,000-26,500c | ~5,200c |
| **x8 (shipped)** | **~42,000c** | **4,000-9,500c** |

Profit compounds because takings are reinvested in more stock. The knee is between x4 and x5.


---

## Appendix — build 15

- **Hired hand: two levels.** KIT works **10 s** (2500c) then **15 s** (3200c). 40 s rest, key 5, unchanged otherwise.
- **Bulk-lesson fix (day 3).** The lesson topped its stock and its buyer back up *before* checking
  whether the order had been filled, so the sale was answered with a fresh buyer and fresh meds.
  The step is now decided first. A bulk order also counts **every piece** in `Sales` (3 sold, not 1).
- **Shift-held drag** lifts a marked stack (build 14c) — a drag with shift down used to unmark the item.
- **The map** (`THE MAP` on the title screen and the pause screen, Esc closes). A pixel map of
  THE BARRENS with five towns on one caravan road: **Dustwell** (your stall — a bit of everything),
  **Saltpan** (dead-lake salt miners — water and meds), **Cinder Gap** (toll-keeping raiders —
  arms, short tempers), **Old Meridian** (the drowned city — tech), **Last Pump** (end of the
  road — the finest goods). Pointing at a town shows its card. Only Dustwell is open; the rest
  are marked `THE ROAD IS NOT OPEN YET`. It is the scaffold for route A (towns as chapters) —
  no gameplay hangs on it yet.
- **Achievements** (`ACHIEVEMENTS n/50` on the title screen and the pause screen). 50, kept
  between runs in `localStorage` (`rustrations.ach`), with a toast when one lands. Groups: trade
  (sales, career takings, single-sale size), haggling, streaks, the counter (filing, misfiles,
  spills, scrap), bulk orders, days survived, day records (no walk-outs, spotless, takings,
  purse, rent by a whisker, fire sale, keeping stock), the Fixer (perks, actives, KIT, looks),
  the bench (unlock, 25 crafts, a Legendary), and serving every customer type. Lifetime numbers
  live in `AST`; tests are one-liners in the `ACH` table, so adding one is a single row.

**Build 15b.** THE MAP and ACHIEVEMENTS also sit in the Fixer's header (either side of the
title), so they are reachable every night; both return to the Fixer. Lesson stock now counts
what the player is *holding*: lifting the last lesson item off the shelf used to make a
replacement appear behind it (day 1, second sale) — and on day 3, carrying the marked stack of
three made two more pop up. Lesson goods now run out like any other stock.


---

## Appendix — build 16

**Difficulty is flat from day 10.** Caravan gap bottoms out at **8.6 s** (was 7.5 s from day 12),
customer gap at **3.54 s** (~28 a day; was 2.7 s, ~35). Patience already bottomed out at day 10.
Rent keeps climbing. **Crates roll their size:** each carries a random 3 up to the day's ceiling
(3 on days 1-3, +1 every three days, 6 from day 10), so late crates average 4.5 instead of a
flat 6. Goods arriving per day from day 10: about 55 (was ~84) against ~28 buyers.

**Painted Sign:** +5 % per level (max +15 %), 150 / 400 / 800c (was +15 % per level, 155/245/350).

**SIGNAL FIRE — sixth active, key 6, 800c, 60 s rest.** Caravans hurry in 10 % faster for 20 s
(`SIGNAL_BOOST`, `SIGNAL_TIME`). Sold from its own card in the Fixer grid next to HIRE A HAND.
Honest size of it: 20 s at +10 % moves the caravan clock by 2 s — under a quarter of one crate
per use, roughly +2 goods a day if fired on cooldown. The "own every active" achievement is now
EVERY TRICK.

**TRANSPORT** (fifth button in the Fixer's bottom row, `TRANSPORT n/4`; screen titled THE YARD).
THE STRIDER is a six-legged walker; the hull is there from the start, and four parts bolt on
visibly (missing ones show as pale blueprints): **Turbine Engine 3000c** (block + twin stacks,
smokes once fitted), **Hydraulic Legs 4000c** (it sits on yard blocks until then), **Roof Gun
2500c**, **Cargo Hold 2000c** — 11,500c in all, per run. Complete, she idles, the cockpit lights,
and SEE THE ROAD opens the map with the Dustwell→Saltpan leg lit and Saltpan marked reachable.
Travelling itself is not built — the other towns exist only on the map — and the screen says so.


---

## Appendix — build 17: the town page

**Every day now starts from DUSTWELL**, a hub page (`scene 'hub'`): a small dusk skyline of the
town in the middle (`buildCity`, gate lamps flicker), doors either side, and the big
`OPEN THE STALL · DAY n` button underneath. Left: **THE FIXER**, **THE WORKBENCH** (or
`WORKBENCH · 1000c` with its tooltip), **TRANSPORT n/4**, **STALL & LOOKS**. Right: **THE LEDGER**,
**THE MAP**, **ACHIEVEMENTS n/50**. A new run opens here too (`S.fresh`), before day 1.

Flow: dusk report → (Herald on its days) → (ledger every fifth day) → **town** → day intro → day.
Every sub-screen's back button, and Esc, returns to town; the Fixer lost its bottom row and its
map/achievement buttons and gained `BACK TO TOWN`.

**The Fixer** is now two clean blocks: six passives, then **all six actives together** — Counter
Sweep 1, Steady Hands 2, Hard Patter 3, The Back Room 4, Hire a Hand 5, Signal Fire 6.

**Key caps.** Each active shows its number in a large key cap: on its Fixer card (left, under the
icon, labelled KEY; level pips moved to the top-right) and on the in-game rail (left of the icon).

**Build 17b — shelf labels.** Clicking an empty shelf's sign used to cycle through *every* kind,
so one stray click could turn TECH into a second ARMS shelf and leave tech with nowhere to go.
A shelf can now only be relabelled to a kind that has **no shelf yet** (`freeLabel`). With four
kinds and four shelves (day 1) there is nothing to swap to and the hint disappears; from day 2
the click swaps in the one missing kind (usually JUNK) and back. An empty duplicate that already
exists is repaired on sight (`fixDupShelves`), on the stall and at the workbench.

**Build 17c — no JUNK.** The shop has four kinds for the whole game: ARMS, MEDS, CHOW, TECH
(`SHOPCATS`). Caravans never bring junk, nobody asks for it, the day-2 "junk crates" notice and
the ledger's JUNK row are gone. Scrap Plate, Duct Tape and Tin Cans no longer appear; the cans
survive only as the worthless prop the day-1 lesson has you scrap. With four kinds and four
shelves there is never anything to relabel to, so the "click to relabel" hint no longer shows.
(Earlier sections of this document that mention a fifth category from day 2 are out of date.)


---

## Appendix — build 18

**Key caps.** The number on every active skill is drawn as a keyboard key (`keycap()`): cream
top face raised off a darker side wall, highlight on the top-left edge, dark legend, and a thin
stripe in the perk's colour. Ready = cream, resting = greyed, not yet owned (Fixer) = dark.
On the rail the key visibly goes down for a moment when the perk fires (`S.keyFx`).

**Caravans come one at a time.** A caravan only rolls in when the yard is empty. If the timer
(or Signal Fire) comes due while one is unloading, the next is held at the gate (`S.crateDue`)
and sent as soon as the yard clears — nothing is lost, it just never stacks. The half-time rush is
now **one BIG CARAVAN**: a larger gold-banded crate with a double roll (6 on days 1-3, 6-12 late)
plus the same two extra customers. Every crate shows how many goods are still aboard (`x5`), and
the NEXT CARAVAN panel reads `unloading...` / `at the gate` / `in 7s`.
Measured: never more than one crate on screen over full days at day 2, 6 and 15 and a 10-day bot
run; goods per day unchanged (about 27 / 38 / 58).


---

## Appendix — build 19: front end

**Title screen** (`scene 'title'`, the game boots here): the stall at dusk behind a dark wash,
drifting dust, the logo, and five buttons — **NEW GAME, CONTINUE, OPTIONS, SETTINGS, EXIT**.
CONTINUE is greyed until a save exists. EXIT shows a "shutters down" card (a browser tab cannot
close itself unless a script opened it).

**Save slots.** NEW GAME opens three slot cards; an occupied slot asks twice before it is
overwritten. CONTINUE shows the same cards in load mode with day, chits, perks, workbench,
Strider progress and the time saved. **The game saves itself every time you arrive on the town
page** (`toHub` → `saveGame`), into `localStorage` `rustrations.slotN`: day, purse, perks, hand,
actives, workbench (materials, unlocks, tray, anvil), shelves and counter (goods stored as
id + rarity + hand-made), Strider parts, ledger history, lesson flags. A day in progress is not
saved — leaving mid-day returns you to that morning. Losing the stall erases the slot.
Looks and achievements stay shared across slots, as before.

**New game flow:** slot → the how-to card (the old title card, now with a single **OK**) → day 1
and its tutorial directly. The town page appears from the first night on.

**ESC menu** (Esc or Space during the day, which pauses it; Esc on the town page):
**CONTINUE, NEW GAME, ACHIEVEMENTS, SETTINGS, EXIT**. EXIT returns to the title screen (saving
first when on the town page; mid-day it warns that today is not saved).

**SETTINGS:** sound on/off (M still mutes), volume quiet/normal/loud, full screen, screen shake.
**OPTIONS:** tutorials on/off (day 1, bulk orders, workbench), erase all saved games, reset
achievements — both destructive ones ask twice. Stored in `rustrations.opts`.

**Build 19b.** OPTIONS is gone from the title screen (NEW GAME · CONTINUE · SETTINGS · EXIT);
its three rows moved into **SETTINGS**, which now lists sound, volume, full screen, screen
shake, tutorials, erase all saved games, reset achievements. Same page from the ESC menu.


---

## Appendix — build 20: demand is spread across the shelves

`spawnCustomer()` used to pick a customer type and then a category blindly, so three buyers in
a row could all ask for MEDS (one queue in sixteen by chance, worse for the popular kinds) while
three shelves sat idle. Now an arrival:
1. never asks for a kind someone already in the queue wants (3 windows, 4 kinds — one is always free);
2. is never the same type as someone already waiting (no twin WANDERERs);
3. does not ask for what the previous arrival asked for.
Exact-item (≈30-35 %) and bulk (≈15 %) odds, prices, patience and tiers are unchanged; lesson
customers are scripted and unaffected. Measured over 20,000 arrivals each on days 2, 6 and 15:
0 repeated kinds in the queue, 0 twins, 0 back-to-back repeats, and each kind gets 24-27 % of
requests.
