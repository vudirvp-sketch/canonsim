# Albion Online · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-20, 4-batch + the
> Kenshi economy loop). Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. Source is
> proprietary — Sandbox Interactive's dev posts and the published
> design notes only. No code, no assets, no 1:1 rewrites
> (`REFERENCES.md` §0.5).

**What it is.** Sandbox Interactive's MMO (2017) built on **regional
markets + full loot**: five royal cities + the black zone each run
separate order books, and dying drops everything you carried — risk
premiums are the entire economic gravity.

**Concrete mechanics.**

- **Regional order books.** Each city's market is local: buy/sell
  orders visible only there, fees and taxes local. The same item
  prices differently in Caerleon (PvP hub, black-zone gate) than in
  a safe royal city — the *spread* is the transport meta. Players
  become haulers by profession (the "fat looping" trade routes),
  and the order books' local depth is the spread's cause.
- **Full loot on death.** Equipment, inventory, mounts — all drops
  on kill. Every carried load through open PvP zones is a wager:
  expected haul value vs ambush probability. The map's economy is
  literally priced in blood.
- **Risk as price regulator.** When a zone's ganking spikes, its
  order books thin (haulers route around), spreads widen, local
  crafters pay more — the *fear moves the price* with no NPC
  anywhere. Conversely, safe corridors compress margins to
  near-zero. The loop the community names: fear → boycott →
  stagnation → scarcity.
- **Crafting interdependence + gear sinks.** Everything equipped is
  player-crafted from gathered/farmed tiers; death sinks the gear;
  the crafting food chain (raw → refined → artifact components)
  rebuilds demand. Fame (XP) is per-item-line — specialization is
  an investment the full-loot sink keeps pressing.
- **The black-zone frontier economy.** The highest resources spawn
  only in full-PvP land: reward tiers spatially gated by risk. The
  endgame economy's inputs require the endgame's danger.

**What we take.** **Risk as price regulator** — res-1's spread law's
social half: the price gap between the market town and the hill
forges is not distance (Stellaris' abstract weight) but *danger*
(the road's banditry state, the weather's seasonal rise). Our
version is read-side and fold-driven: the spread line derives from
the threat events already in the log (the world-state law — derived
read, never a stored object). The **fear → boycott → stagnation
loop** is a faction-dynamics row (depth-6's ratio grid): trade-guild
confidence is a live axis the player's failures depress; the garrison
patrol schedule is the counterweight the player can tip.

**What we adapt.** Order books and hauling professions are refused
(no negotiated markets — D-116's fence; no profession classes).
Regional markets become *regional read surfaces*: the merchant NPC's
rendered line ("iron dear since the road troubles") — price
differences as narrator-observable facts with knowledge records, not
trade interfaces. Full loot becomes the **carried-loss law**: a
robbed convoy loses its cargo claim (the irreversible item law's
transport case — st-5's containers + carrier closure already carry
the semantics); the loss event seeds the consequence hooks (the X4
cascade's local form).

**What inspires us.** Geography priced by danger alone: a map where
the *safe* road is cheap and the *short* road is a wager is a story
generator the player authors with every route choice.

**Strengths.** The purest published instance of risk premiums
organizing an economy — no NPC pricing anywhere, and the fear-loop
(boycott/stagnation) is the exact social feedback our asymmetric
trust data (D-030) formalizes. Regional spread + local order depth
is a legible two-variable story (which region, how thin) — maps
perfectly to one rendered line per market. Spatial reward-tier
gating (the risky land holds the valuable thing) is the province's
hill-iron shape verbatim.

**Weaknesses.** The economy's whole drama rides on PvP population
density — a thin server means no gankers means no spreads (our
threat state is simulated, not crowd-sourced: it holds at any
scale). Full loot's harshness drove continuous retention patching
(safe-ish pockets, gear insurance debates) — the tone dial's
(D-030) domain, pack-declared per setting, never a global rule.
Hauling-as-profession is pure interface labor — our travel prices
(st-6a) make the route *decision* the game, not the route *commute*.

**Verdict.** res-1's **risk-premium donor**: spread-from-threat,
the fear/stagnation social loop, and reward-gated-by-danger
geography — the river-artery province's economic weather, with EVE
supplying the sink law and X4 the cascade.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
