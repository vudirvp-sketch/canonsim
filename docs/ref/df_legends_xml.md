# DF Legends XML · `REFERENCES.md` §1 + §10 · proprietary (export from own install) · bg-1..bg-4 (track B); schema shapes borrow for phase 0

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015).

**What it is.** Dwarf Fortress (proprietary) exports a world's history
as XML via the DFHack `exportlegends info` command. The XML contains
populations, sites, regions, figures, entities, artistic forms, structured
events, and nested `event_collections`. It is the **only irreplaceable
external resource** (`ROADMAP.md` §4): a ready canonical event log from a
real world generator. This entry covers the **export schema** half;
`df_worldgen.md` covers the worldgen + history layer half.

**Concrete mechanics.** Field names and structures below verified
against the owner's real exports (iter-8e survey — measured numbers in
`docs/TECH_NOTES.md` §3). Note the naming duality: type strings are
display-style in the main file (`change hf state`, `hf died`) and
snake_case in the plus companion (`change_hf_state`) — normalize on
import (KI#33).

- Top-level XML elements (verified against DFHack docs, current DF
  Classic): `regions`, `underground_regions`, `sites`, `landmasses`,
  `mountain_peaks`, `rivers`, `creature_collections`, `historical_figures`,
  `entities`, `entity_populations`, `art_forms`, `dance_forms`,
  `musical_forms`, `poetic_forms`, `written_contents`, `historical_events`,
  `historical_event_collections`.
- **`historical_events`** — flat list of typed events, each with `id`
  (gap-free integer), `year`, `seconds72` (sub-year tick; `-1` = no
  sub-year time), and type-specific fields. Common types (normalized
  names; the main file spells them display-style):
  - `hf_died` (figure died) — `hfid` (victim), `slayer_hfid`,
    `slayer_race`, `slayer_caste`, `cause` (enum: murdered, old age,
    struck, shot, `exec …`, `suicide …`), `site_id`. Measured: slayer
    recorded on 42–61% of deaths; struck ~51%, old age 22–27%,
    murdered 18–24%.
  - `hf_attacked_site` — `attacker_civ_id`, `site_id`, `defender_civ_id`.
  - `artifact_created` — `artifact_id`, `creator_hfid`, `site_id`.
  - `created_site` / `destroyed_site` — `site_id`, `civ_id`, `builder_hfid`.
  - `hf_reputation_change` — `hfid`, `rep_hfid` (the figure whose
    reputation changed), `identity_id`, `region_index`, `reputation_type`
    (enum: rumors of theft, terrorized, …), `strength` (1–100).
  - `entity_reputation_change` — like the above but for an entity.
- **`historical_event_collections`** — nested groupings; each has `id`,
  `type`, `start_year`, `end_year`, repeated `<event>` child elements
  (member event ids) and repeated `<eventcol>` child elements
  (subcollection ids), plus role fields (attacker, defender, winner,
  loser, killer, abductor). `parent_eventcol` exists as an up-edge but
  is almost never set (measured: 199 of 29,663 and 710 of 110,519) —
  reconstruct nesting from the parents' `<eventcol>` lists. Measured
  types (16): `war`, `battle`, `duel`, `abduction`, `theft`, `beast
  attack`, `site conquered`, `persecution`, `journey`, `occasion`,
  `ceremony`, `performance`, `procession`, `competition`, `purge`,
  `entity overthrown`.
- **`historical_figures`** — entry per notable: `name` (with translated
  variant layers), `race`, `caste`, `birth_year`, `death_year`,
  `entity_id`, `site_link`, `ent_pop_id`, `reputation` (nested list of
  reputation entries), `honor`, `kills` list (figure ids), `affiliation`
  history (entity_id + role + start_year + end_year).
- **Causality is NOT a first-class field.** Events have participants,
  place, year; the "why" is reconstructed from role fields (killer,
  abductor, attacker) and from `event_collections` grouping (a `war`
  collection groups `battle` collections, which group `hf_died` events).
  This is the **TECH_NOTES.md §3** finding: "Causality is reconstructed,
  not parsed — budget inference work, not parsing work."

**Coverage matrix — survey vs SQLite sink.** `scripts/df_survey.py`
extracts F7/F8 detail from three record tags (the HANDLED set); every
other record tag is counted + structurally fingerprinted (every unique
child-tag set per record tag) by `--audit` (iter-8g). The SQLite sink
landed (bg-1, `scripts/df_import.py`): typed core + EAV field tables
for the HANDLED three, one generic JSON `records` table for every
non-noise UNHANDLED tag — including any future UNDOCUMENTED tag, so a
drift record still imports instead of breaking the sink. The matrix is
the single owner of "which sections exist in an export"; any record
tag outside it renders as UNDOCUMENTED by the audit — a drift signal
(a future DF version grew the schema; KI#36 — the marker was documented
here but never implemented until the large world's audit caught two
real matrix gaps: `artifact`, present in every export, and
`historical_era`). Section presence is export-dependent: the large
world's main file carries 14 sections; its landmasses, mountain_peaks
and rivers live only in the plus companion.

| Section (plural, depth=2) | Record tag (singular, depth=3) | Survey status |
|---|---|---|
| `historical_events` | `historical_event` | HANDLED — F7 type/year/role, F8 collection refs |
| `historical_event_collections` | `historical_event_collection` | HANDLED — F8 type/parent/child links |
| `historical_figures` | `historical_figure` | HANDLED — race/birth/death |
| `sites` | `site` | UNHANDLED — count + child-tag fingerprint only |
| `entities` | `entity` | UNHANDLED — count + fingerprint |
| `entity_populations` | `entity_population` | UNHANDLED — count + fingerprint |
| `regions` | `region` | UNHANDLED — count + fingerprint |
| `underground_regions` | `underground_region` | UNHANDLED — count + fingerprint |
| `landmasses` | `landmass` | UNHANDLED — count + fingerprint (plus-companion-only in the large world) |
| `mountain_peaks` | `mountain_peak` | UNHANDLED — count + fingerprint (plus-companion-only in the large world) |
| `rivers` | `river` | UNHANDLED — count + fingerprint (plus-companion-only in the large world) |
| `creature_collections` | `creature_collection` (+ nested) | UNHANDLED — count + fingerprint |
| `artifacts` | `artifact` | UNHANDLED — count + fingerprint (KI#36 matrix-gap fix; item names serve bg-2/bg-3) |
| `art_forms` | `art_form` | UNHANDLED — count + fingerprint (design noise, skip on sink) |
| `dance_forms` | `dance_form` | UNHANDLED — count + fingerprint (design noise) |
| `musical_forms` | `musical_form` | UNHANDLED — count + fingerprint (design noise) |
| `poetic_forms` | `poetic_form` | UNHANDLED — count + fingerprint (design noise) |
| `written_contents` | `written_content` | UNHANDLED — count + fingerprint (bg-4 interest) |
| `historical_eras` | `historical_era` | UNHANDLED — count + fingerprint (KI#36; 1 record: name + start_year; large world) |

The "design noise" rows (art/dance/musical/poetic forms) are bg-1
selective-import skips per `df_design.md` "What we adapt" — briefer
noise (the sink counts and skips them). `written_content` IS imported
by the sink as generic records (bg-4's cost notes read them from
SQLite when that spike lands).

**What we take.**

- **Event-with-id-and-tick schema shape.** Every DF event has `id`
  (gap-free integer), `year`, `seconds72`. Our event schema
  (`EVENT_SCHEMA.md` §1) follows: gap-free `event_id`, `tick`,
  `sub_order` — same idea, deterministic naming, sub-tick precision.
- **`event_collections` as the precedent for grouping.** Our `cause`
  chain (`EVENT_SCHEMA.md` §2) does similar work in a stricter way:
  an event points at its parent via `cause` (single-parent linear
  chain). Measured (iter-8e): the export's grouping is itself a strict
  single-parent TREE — direct event→collection references are unique
  (0 multi-parent events), and no subcollection has 2+ parents; only
  19–24% of events sit in any collection at all (numbers:
  `TECH_NOTES.md` §3). Multi-parent arc grouping (a battle under both a
  war and a journey) remains a hypothetical future extension (P3c,
  `CORE_DESIGN_RESEARCH.md` §6) — now recorded as our own design
  idea, not a DF-export property.
- **Figure-with-affiliation-history pattern.** Our `entity` records
  (knowledge records, `known_by`, etc.) will need the same "track who
  was where when" structure for any non-trivial timeline. DF's
  `affiliation` history (entity_id + role + start + end) is the model
  for `LEGEND_SPEC` (phase 4).
- **Population vs notables LOD.** DF keeps `entity_populations` as
  aggregate counts and `historical_figures` as full records — exactly
  the LOD ladder (`CORE_DESIGN_RESEARCH.md` §2 row "DF worldgen", §6
  P3d). Our `npc_market_crowd_01` ambient entity (`MVP_SCOPE.md` §4.2)
  is the seed of this same ladder.

**What we adapt.**

- **Causality from reconstructed → recorded** (P1a, INV-1). DF's
  causality is inferred from `event_collections` + role fields; our
  `cause` is first-class, recorded at event time. bg-2 will measure
  how much DF causality we can lift into our `cause` chain.
- **Macro-dense/micro-empty → micro-dense slice.** DF events are macro
  (wars, artifacts, births, deaths, abductions); our phase-0 events
  are micro (theft, arson, gossip, watch change). `TECH_NOTES.md` §3:
  the bg track validates briefer mechanics, NOT micro-event
  interestingness — that stays on our own dry chronicle.
- **XML → JSONL** (D-002). DF speaks XML; we speak JSONL. The bg-1
  pipeline parses XML → SQLite; from there we read rows. Our event
  log is never XML.

**What inspires us.**

- **"History ticks abstractly."** DF worldgen advances the clock year by
  year; populations get statistics, notables get events — the LOD
  principle (`CORE_DESIGN_RESEARCH.md` §2 row "DF worldgen") confirmed
  at the source; our `entity LOD ladder` (P3d, phase 5) follows.
- **"History without a player."** DF generates 1000 years before the
  player arrives; the player walks into a live world. Our phase-0
  tavern is the analog: events have already been happening; the PC
  arrives at T=0 into a running world (seeded hooks in the director —
  `MVP_SCOPE.md` §11).
- **Epistemology schema.** DF's `hf_reputation_change` /
  `entity_reputation_change` are the closest precedent for our
  `knowledge records` (MVP_SCOPE §10, EVENT_SCHEMA §3). DF tracks
  who-reputed-what-where; we track who-knows-what-with-what-fidelity.
  Mapping: `rep_hfid` ↔ `known_by`, `reputation_type` ↔ `knows`
  token, `strength` ↔ `fidelity`.

**Strengths.**

- The only irreplaceable external resource (`ROADMAP.md` §4) — a ready
  canonical event log, exportable from a free install.
- Real-world precedent for every primitive we care about: events,
  figures, entities, sites, collections, reputations, affiliations.
- Structured XML — parseable, not a binary blob; schema documented in
  DFHack source.

**Weaknesses.**

- **Causality is reconstructed, not parsed** (`TECH_NOTES.md` §3) —
  bg-2 budgets inference work, not parsing work. We lift the shape,
  not the chains.
- **Macro-dense, micro-empty** (`TECH_NOTES.md` §3) — DF has wars and
  artifact theft, not gossip and pickpocketing. DF's theft events
  are artifact-theft (a hammer stolen from a museum), not street theft.
  This is why the bg track validates mechanics, not interestingness.
- **HEX errors after fortress play** (`TECH_NOTES.md` §3) — must export
  from a clean legends-mode save; the bug is on DFHack's side. And the
  export is not well-formed XML: raw CP437 control bytes (item-quality
  symbols) sit inside artifact names — byte-level sanitize before parse
  (measured: 12–24 bytes per world; the recipe lives in `TECH_NOTES.md`
  §3 / `scripts/df_survey.py`).
- **The exporter can die mid-write (KI#34, iter-8f)** — one world arrived
  truncated at 2.91 GB (cut inside a battle collection, no `</df_world>`;
  the complete re-export is 4.95 GB and reproduces the recovered prefix
  counts exactly). Tail-check + best-effort closing-tag synthesis,
  loudly PARTIAL: `TECH_NOTES.md` §3.
- **Scale is brutal and the format is bigger than the docs assumed** —
  measured 315 MB / 1.99 GB / 4.95 GB per world (0.45M / 1.22M / 0.93M
  events), 10–20× the old ballpark; the parser must stream with clearing
  (a non-clearing parse OOMs 4 GB on the medium world) —
  `TECH_NOTES.md` §3. Plus companion repeats `historical_events` with
  complementary fields — import selectively.
- **Proprietary.** We read exported data, never DF's code or assets
  (`REFERENCES.md` §10). DFHack is Zlib — pattern only; its parser is
  a reference, not a donor.

**Verdict.** bg-1..bg-4 track. Phase-0 borrows schema shapes (event
id + tick, role fields, population vs notables). Phase-4 (LEGEND_SPEC)
borrows its epistemology. Phase-5 (depth/worldgen) borrows its LOD
ladder. Nothing here gates phase 0.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
