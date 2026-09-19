# Kenshi (economy loop) · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1 / world-2)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-20's riding fifth —
> the economy loop half of the Kenshi row; the emergent-chain half is
> already absorbed in the phase-5 records). Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. Source is proprietary — Chris Hunt's public dev interviews and
> the game itself (modding scene documents the data shapes). No code,
> no assets, no 1:1 rewrites (`REFERENCES.md` §0.5).

**What it is.** Lo-Fi Games' sandbox RPG (2018): a hostile
region-based world where **towns run on stockpiles that starve**,
and starving regions generate the raiders that starve them further —
the desperation economy as a self-running loop, with zero authored
plot.

**Concrete mechanics.**

- **Town stockpiles with a public state.** Each town's food and
  supplies accumulate from its biome's production and inbound trade;
  the town's *faction* reads its own stockpile: a fed town patrols,
  a starving town raids. The UI shows town states (allied, hostile,
  starving, dead) — the stockpile is the dial everything else
  reads.
- **Region-based world state.** The map is regions, each owning
  biome resources, faction control, and threat level. Rain (acid
  storms), fauna, and raiding pressure are per-region states —
  geography decides the economy's floor before any actor moves.
- **The desperation loop.** Supply failure → starvation → the
  faction's squads convert to raiding (their only income) → roads
  and farms degrade → deeper scarcity. Conversely, player actions
  (feeding a town, clearing raids, freeing slaves) restart
  production and the region heals. **No state machine authored this
  — three rules and a stockpile.**
- **Squads as the mobile unit.** Every group (caravans, patrols,
  raiders, slavers) is a squad with a destination and a purpose;
  the world's visible traffic is squads resolving their faction's
  needs. Arrivals trigger events (a raid arriving IS the event).
- **Escalating asymmetry.** Starving regions field progressively
  desperate forces (loot quality, numbers, morale) — the pressure
  curve is the scarcity curve.

**What we take.** **The desperation economy's exact shape** — the
phase-6 province's crime-pattern law: `convoy loss → price shock →
crime-pattern shift` (X4's cascade, Kenshi's social read-out). Our
form: a settlement's stock state (a fold over flow events) feeds
(a) the derived scarcity line res-1 renders, (b) faction dynamics'
live axes (the ratio grid reading hunger), (c) the director's
world-side predicates (a starving town seeds hooks, D-082's
pattern — pressure from scarcity + factions, never scripted
incidents: D-005's own donor). **Squads-arriving-as-events** is
depth-7's condensation consumer (the parked Kenshi arrival-side
dive, `phases.md` §6): road traffic as cold aggregates birthing a
named traveler band when the reader's zone warms — st-6a travel +
the group tier already carry the semantics.

**What we adapt.** Their factions read their own stockpiles
directly (a hidden C++ check); ours goes through the fold
explicitly: stock = a read-side aggregate over flow events, faction
behavior = declared dynamics over that read (the ratio/threshold
rows, depth-6) — same loop, INV-1-clean. Squad pathing (free
navigation) becomes travel's lattice edges (roads-1's derived
graph); the raid's *arrival* is the event, the road never simulates.
Player-as-healer is already our loop: the player tips ratios
(feeding the town = trade events + faction axis shifts), never
script gates.

**What inspires us.** A world that raids you *because it is
starving* — hostility as symptom, scarcity as disease: the
emergent-chain donor's economy half in one sentence.

**Strengths.** The proof that a THREE-rule economy loop
(stockpile → faction read → squad action) generates region-scale
narrative for hundreds of hours with no plot code — the cheapest
verified drama-per-rule ratio in our catalog. Region-state design
keeps the sim O(regions), not O(citizens) — the cold-tier LOD's
shape exactly. The self-healing inverse (players restart regions)
demonstrates the "many roads" claim the FNV row wants — multiple
player strategies all legitimate because the loop is a loop.

**Weaknesses.** The economy is a coarse dial (food, one axis; our
focal scarcity needs the closed cycle: source → flow → sink with
derived spreads — Kenshi gives the loop, not the ledger). Balance
collapses at the margins: a dead region stays dead (no re-seeding;
our counter-events + the director's buffer keep the world from
absorbing states it cannot answer). Squad-level AI costs real
performance late-game (hundreds of squads pathing) — our
condensation tiers make the cold half free. No epistemics: NPCs do
not know *why* they starve, and no rumor tells the player a
neighboring region is collapsing — the knowledge half the rumordrift
family adds.

**Verdict.** res-1's **loop donor + world-2's crime-pressure law**:
stockpile → faction read → action — the desperation economy binds
X4's cascade to a human-readable consequence (raids) and gives the
province its ambient threat curve; the arrival-side dive stays
parked with world-2's condensation rows.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
