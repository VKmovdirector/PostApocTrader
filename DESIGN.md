# RUST & RATIONS — design notes (build 11)

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
