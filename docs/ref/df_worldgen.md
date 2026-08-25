# DF worldgen + history layer · `REFERENCES.md` §1 + §10 · proprietary (read exported data only; never code or assets) · bg-1..bg-4 (track B); LOD ladder for phase 5

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015).

**What it is.** Dwarf Fortress generates 200–1000+ years of world history
before the player arrives. This entry covers the **worldgen + history
layer** — the other half of DF Legends XML vs the export schema half
(see `df_legends_xml.md`). Where the export schema entry covers the
*format* of exported history, this entry covers *how DF generates it*:
history ticks, populations vs notables LOD, age/civ dynamics, artifact
anchors, reputation as event.

**Concrete mechanics.**

- **History ticks abstractly.** DF worldgen advances year-by-year, not
  turn-by-turn. Each year: populations get statistical updates
  (births, deaths, migrations as counts); notable figures
  (`historical_figures`) get full event records; sites grow or shrink;
  civilizations expand, contract, go to war, found new sites.
- **Populations vs notables LOD** (central abstraction):
  `entity_populations` = aggregate counts per race per site
  (`{civ_id, race, count, site_ids}` — no individual records);
  `historical_figures` = full per-individual records (name, race, caste,
  birth_year, death_year, affiliation history, kills, reputation).
  Boundary is membership-based: a figure becomes "historical" when it
  does something worth recording. DF keeps ~1000–10000 historical
  figures per 1000-year world; populations are 10–100× larger but
  never simulated individually. Civilizations have lifespans (founding
  → expansion → conflict → decline); wars reduce defender counts
  without simulating each death — the LOD abstraction strikes again.
- **Reputation as event** (cleanest precedent):
  `hf_reputation_change`: `{hfid, rep_hfid, identity_id, region_index,
  reputation_type, strength}`. `entity_reputation_change`: same shape
  for an entity. `reputation_type` enum: "rumors of theft",
  "terrorized", "respected", "feared"… `strength` is 1–100. Reputation
  is **not stored as a state field** — it is the *stream* of these
  events. "Current reputation" = fold over `hf_reputation_change`
  events for a given `hfid` × `rep_hfid` pair.

**What we take.**

- **Populations vs notables LOD ladder** — the boundary (count → record)
  is the same shape as our P3d: ambient → statistical → full simulation.
  Our `npc_market_crowd_01` ambient entity (`MVP_SCOPE.md` §4.2) is the
  seed; DF proves the seed grows. Reputation-as-event (already borrowed
  in `df_legends_xml.md`) — `hf_reputation_change` is the precedent
  for our `knowledge` records (MVP_SCOPE §10, EVENT_SCHEMA §3).

**What we adapt.**

- **Year-by-year tick → second-by-second tick.** DF worldgen advances
  years; our phase-0 tick is sub-minute (`MVP_SCOPE.md` §4.1: 1 tick =
  12 in-world minutes). Phase 5 will need a coarser macro-time tick
  layered over micro-time.
- **Macro-dense / micro-empty → micro-dense slice** (`df_legends_xml.md`,
  `TECH_NOTES.md` §3) + **worldgen monolith → runtime + history**
  (DF runs once and ends; we need both simultaneously — the tavern is
  "live history" the moment the PC walks in). Pre-PC worldgen seeds
  the "running world" the PC arrives into (`MVP_SCOPE.md` §11 director
  hooks). Causality reconstructed → recorded (P1a, INV-1, `df_legends_xml.md`)
  and no determinism contract across builds → INV-2 strict
  (`TECH_NOTES.md` §4) — cross-link, don't restate.

**What inspires us.**

- **"History without a player."** DF generates 1000 years before the
  player arrives; PC walks into a live world. Our phase-0 tavern is
  the analog: events have already been happening; the PC arrives at
  T=0 into a running world (seeded hooks in the director,
  `MVP_SCOPE.md` §11). DF is the proof-of-existence for the "running
  world" posture. Reputation is the *stream* of changes, not a
  number on an entity — aligns with INV-1 and D-007. The LOD
  discipline ("crowd is a count, guard is a record") is in
  "Concrete mechanics" above.

**Strengths.**

- The only existing implementation of "abstract history ticks at scale"
  (1000+ years) producing a usable canonical log.
- LOD discipline concretely demonstrated: populations vs notables is a
  working split with a 20-year track record.
- Reputation-as-event is the cleanest precedent for our `knowledge`
  records (cross-link `df_legends_xml.md`).

**Weaknesses.**

- **Macro-dense, micro-empty** (`df_legends_xml.md`, `TECH_NOTES.md`
  §3): wars and artifact-theft, not gossip and pickpocketing; bg track
  validates briefer *mechanics*, not micro-event interestingness.
- **Population LOD is "one tier"** (counts vs notables); our P3d proposes
  3 tiers (ambient → statistical → full). DF confirms the bottom 2;
  "ambient" tier is our addition (`MVP_SCOPE.md` §4.2).
- **DF worldgen has no "now"**: once play starts, worldgen ends; we need
  runtime + history simultaneously. DF is the negative precedent for
  "history runs only before play".
- **No determinism contract across builds** (`TECH_NOTES.md` §4) +
  **proprietary** (`REFERENCES.md` §10; DFHack is Zlib — pattern only).

**Verdict.** Phase-5 settlement cousin + phase-4 LEGEND_SPEC reference.
Confirms LOD ladder (P3d) and "history without a player"
(`MVP_SCOPE.md` §11). Schema shapes already borrowed in
`df_legends_xml.md`; worldgen mechanics proper wait for phase 5.
bg-1..bg-4 track parses the export; nothing here gates phase 0.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
