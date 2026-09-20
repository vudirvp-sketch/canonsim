# canonsim

Deterministic canonical simulation core for an LLM-narrator architecture.
Phase 0 deliverable: **TavernSim v0** — one tavern, a theft, an arson, spreading
rumors — running as a pure Python simulation with an append-only event log.
No LLM anywhere near the canon yet.

> **Simulator produces facts. LLM produces prose. The log stores canon.
> The mediator holds the boundary.**

North star: a "living world" simulation mode inside
[Soul-of-Waifu](https://github.com/jofizcd/Soul-of-Waifu) (local-first desktop
AI companion app) — see `docs/VISION.md` §10. This repo stays frontend-agnostic;
the dumb-terminal frontend contract is the SoW horizon's (`docs/ROADMAP.md` §6).

## Status

**The roadmap's phase ladder is COMPLETE — phases 0..6 all CLOSED**
(`docs/ROADMAP.md` §2 owns the state; the per-phase evidence lives in
DECISIONS' gate-verdict family + `docs/TEST_PLAN.md` §4 + the worklog
gate entries — linked, never restated here):

- **Phase 0 (Sim without LLM) — gate PASS iter-6**: all six
  `MVP_SCOPE.md` §16 exit criteria met; the chronicle reads as a story;
  the world acts without the player (M5 p50 0.77 across 1000 seeds);
  losses are permanent. Deliverables: TEST_PLAN, `core/metrics.py`,
  the T1 fixture-regeneration guard, `tests/test_t8_ab.py`,
  `scripts/balance_harness.py`.
- **Phase 1 (Narrator) — gate PASS iter-26, D-058**: 0 canon violations
  over 109 live beats; the 105-case corpus through the real mediator
  cycle; the narrator agent-in-the-loop at dev-time over the call/reply
  file contract (D-055 — the repo stays LLM-free, INV-4); the polish
  menu closed iter-27–29.
- **Phase 2 (Parser) — gate PASS iter-35, D-064**: 35/35 boundary
  validity over 51 utterances, 0 honest misfires; the mode-C boundary
  mirrors D-055 on free text (`docs/PARSER_SPEC.md`).
- **Phase 3 (Director) — gate PASS iter-54, D-083**: the pacing clock,
  the Paradox event grammar, the arc release chains, the social stack —
  every declared layer live; max eventless stretch 1 (N reads 2).
- **Phase 4 (Knowledge & scene) — gate PASS iter-65, D-094**: 0 leaks
  on the blind-NPC suite (all four layers); the retrieval ladder, mode
  B + the scene manager, the texture identity tier, the mode-F
  chronicler live.
- **Phase 5 (Depth) — gate PASS iter-102, D-136**: the exit criterion
  "an emergent chain of 3+ events without the player" met in its
  worldgen-fed form (the armed committed pack); lazy worldgen, factions
  with goals, long history; ON seed 125 M1=0.52/M2=0.2, OFF T8 24
  chains, the 60-seed band 15–24, M5 p50 0.79.
- **Phase 6 (Packs & worldbuilder) — gate PASS iter-116, D-151**
  (opened iter-109, D-146): the exit criterion "a new T1 reskin
  without core edits, ≤1 day" MET BY MEASUREMENT — the road_pack
  reskin day (iter-112, D-149: the clock 14m24s, zero core edits,
  git-verified; the T1 twin + the first committed travel-price arming);
  the §5 re-run at the gate reproduced iter-102's numbers exactly.
  TWO packs live (tavern + road); the open build rows (roads-1, res-1,
  pack-ci, world-2 L2, since-1) stay owner-gated backlog rows.

**The standing work**: the owner-gated backlog (`docs/TASKS.md`) + the
Soul-of-Waifu horizon (`docs/ROADMAP.md` §6). Track B: bg-2/3/4/7/8
DONE, bg-6 owner-deferred; the {3–8B, GBNF} arm the standing gap row.

**The v0.2 refinement lance** (iter-66..72, closed): the post-gate
quality pass — the invented-entity prose floor (`brief/scan.py`), the
trait beliefwire gates, testproto, the rumor fidelity drift, the
per-target suspicion axes, the lowercase assertion surface. Contract
owners: the TASKS v0.2 rows + D-095..D-104/D-109.

## For AI agents (primary audience)

1. `AGENTS.md` — the law: invariants, iteration protocol, caps, git safety.
2. `docs/AGENT_NAVIGATION.md` — reading gradient + where things are.
3. `docs/TASKS.md` — what to do next, with acceptance criteria.

Humans: `docs/VISION.md` for the why; `docs/MVP_SCOPE.md` for the phase-0 tech
spec. Everything here is written for agents first — dense, tabular, no prose
padding.

## Repo map

| Path | What |
|---|---|
| `AGENTS.md` | operating conventions for AI agents (law) |
| `STATUS.md` | iteration state, KIs, pitfalls (read every task) |
| `worklog.md` | capped short-term memory (≤10 entries) |
| `.github/workflows/ci.yml` | CI runner: pytest + ruff on push to `main` (ci-1, iter-143 — Python 3.12.14 the env pin, `PYTHONHASHSEED=0`) |
| `docs/` | all specs & plans (see `docs/AGENT_NAVIGATION.md` §1) |
| `docs/worldbuild/` | the active worldbuilding surface: the authored-setting model (world kernel, Resonance, life/personhood, peoples, cultures, the Sarrow Vale anchor, authoring doctrine, world tests, the world track's plan — `README.md` the index; D-186) |
| `schemas/` | machine-readable contracts (`event.schema.json`) |
| `content/tavern_pack/` | setting as data (v0.1; loaded + linted by `core/pack.py` — the admission gate; the lint bodies in `core/packlint/`, the D-175 split) |
| `content/road_pack/` | the second pack: the travel-loop reskin (world-2 L1, iter-112 — `travel` armed, the derived prices; `CREDITS.md` the CC-BY sidecar) |
| `content/province_pack/` | the third pack: the original province (world-2 L2, slices 1-2, iter-118/119 — the 324-site generated surface, the settlements on the travel lattice, the spine records, the two name-1 phonotactic profiles + the condensation travelers + the cultures block; `tests/test_t1_province.py` the T1 twin, `tests/test_cultures.py` the block lint) |
| `core/`, `sim/systems/`, `render/`, `brief/`, `cli/` | code (core iter-1..4; the iter-3/4 systems live in `core/` per D-037 — `sim/systems/` stays reserved for periphery; render + cli landed iter-5; `core/metrics.py` landed iter-6; `core/worldgen.py` iter-81/87 (depth-5/chron-2 — the ordered passes,
the claim gate's first caller, the genesis + the DF legends history
bridge: participants/places, the pack-declared collection vocabulary,
the cause tree); `core/macro.py` iter-90 (maclock-1, D-124 — the L4
layered-clock primitive: the `time.macro` pack-declared cadence fired
at the loop's third crossing coarsest-first, the macro-year counter
bound to the worldgen chronicle horizon, `macro_turn_draft` the D-112
one-event-with-cardinality emission surface the depth-3/7 +
st-6a/weather-1 consumers call; the committed pack ARMED since
weather-1/iter-98 — the year-scale cadence 518400, the arming the
primitive's first consumer); `core/lod.py` iter-91 (depth-3, D-125 — the scene LOD: the
three zones' owner, `scene_zones` the pure partition, the cold census
`cold_npcs` on the macro turn, the one-gate law — armed clock or the
one-scene world); `core/factions.py` iter-92 (depth-6, D-126 —
factions with goals: the KeeperRL small formula over the members'
live per-entity axes, the group entity kind `entities.json::groups`
acting through the intent door, the `faction:<group>:<kind>` roll
stream — the D-079 family's fifth member, the anchor-scoped LOD; the
committed pack unarmed — the 68a pattern); `core/groups.py` iter-93
(depth-7, D-127 — the write-side LOD at group scale: the `member_of`
state door, the population tier's macro-tick aggregates, the
condensation on crossing the warm transition + the write-once
tombstone, the per-group opt-in `macro_event`/`condense_event`; the
committed pack unarmed — the 68a pattern); `core/names.py` iter-96
(name-1, D-131 — the name generator: `materialize_name` the lazy
per-npc materialization on the `name:<npc>` stream — the D-079
family's sixth member, per-declaration isolation, first-commit-wins,
the bounded collision walk against the entity namespace; the
profiles `rules.json::names.profiles` + the npc `generated_name`
declaration (the `_names` lint: mutual exclusion, reachability);
the consumer: depth-7's condensation births the names with the
memberships; the committed pack unarmed — the 68a pattern);
`core/travel.py` iter-97 (st-6a, D-132 — the travel price law: the
pack override wins per edge, else the derived integer function of
the WorldModel — lattice steps + height-band spread + river
endpoints, the min cross-pair, no division, draw-free; the accept
door schedules the completion at `t + price`, the crossings fire
mid-travel); `core/weather.py` iter-98 (weather-1, D-133 — the
ambient weather family: the chain roll at each macro crossing on
the isolated `weather:chain` stream (the D-079 family's seventh
member), the current weather a fold read, the SEEDED erosion
follow-ups (the fire follow-ups' shape — the rain reverts the
smoke), the storm's director hook; the committed pack ARMED — the
macro clock at the year-scale cadence + the weather block, the
corpus price the LOD's one-gate engagement alone); `brief/`: `assembler.py` iter-8 — the deterministic brief, `docs/BRIEF_SPEC.md` · `validator.py` iter-9 — the validation gate, `docs/VALIDATION_SPEC.md` · `ledger.py` iter-10 — the session scene ledger, `docs/BRIEF_SPEC.md` §3.3 · `mediator.py` iter-12 — the narrator boundary's document layer, D-055 · `parser.py` iter-31 — the phase-2 mode-C boundary, `docs/PARSER_SPEC.md`) |
| `scripts/` | operator tooling (CLI-class, D-046): `balance_harness.py` iter-6 (the 1000-sim distribution harness, KI#4 close) · `df_survey.py` iter-8e (DF Legends XML empirical survey — the bg-1 sanitize+stream core; measured numbers in `docs/TECH_NOTES.md` §3.1) · `df_import.py` bg-1 (the SQLite sink — typed cores + EAV + participant index + generic JSON records; bg-2: the plus pass, sink v2; `docs/TECH_NOTES.md` §3.2, D-051/D-063) · `df_taxonomy.py` bg-2 (the event-taxonomy survey over the sink DB; `docs/TAXONOMY.md`) · `df_briefer.py` bg-3 (the POV mini-briefer + reverse validation over the sink; `docs/TECH_NOTES.md` §3.3) · `profile_harness.py` iter-30 · `chronicle.py` iter-64 (the mode-F offline chronicler — read_ndjson_auto intake behind the count gate, the parquet pair + the sqlite summary via the stdlib ladder, the content-derived manifest; `[chronicler]` extra, D-093, `docs/TEST_PLAN.md` §7) · `checkpoint.py` iter-80 (depth-4 fold checkpoints — the derived snapshot + event-index offset over one committed log: the pack↔header identity gate, the born-verified re-fold pass, `checkpoint_<offset>.json` + `index.json` the sha256 anchor records under `output/checkpoints/`; `core/checkpoint.py` the mechanism, D-114, `docs/TEST_PLAN.md` §7.1) · `mechanics.py` iter-84 (mech-1, D-118 — the mechanics introspection CLI: matrix/trace/why/blast; the shadow-replay law, INV-2-equal to the runtime; `tests/test_mechanics.py`) · `worldgen_profile.py` iter-89 (geo-1, D-123 — the worldgen timing profile: the site ladder 36→10k over the committed pack's own block, clean + cProfile double-run with the fingerprints compared; the measured numbers in `docs/TECH_NOTES.md` §12) · `balance_harness.py` iter-107 (the payoff-latency + beat-tension blocks + the `--systems-minus` ablation arm, D-140/D-141) · `pack_scaffold.py` + `pack_doctor.py` iter-107 (the pack authoring loop's first rungs: a lint-clean scaffold from the committed pack + the lint's fix-hint surface; `tests/test_pack_tools.py`) · `digest.py` iter-108 (the derived one-pager over STATUS/TASKS/DECISIONS — the human-readable summary; a viewport, never a second source of truth; `tests/test_digest.py`) |
| `tests/`, `tests/playscripts/` | test suite + seed/intent fixtures |

## Running

```
pip install -e ".[dev]"
PYTHONHASHSEED=0 pytest -q
ruff check .
```

Play the slice (no LLM anywhere):

```
python -m cli play tests/playscripts/day1_theft_and_arson.json
python -m cli                      # interactive session ('help' lists commands)
python -m cli --resume logs/run_42_0.jsonl   # continue that session's run (D-139)
python -m cli chronicle logs/run_8_0.jsonl
python -m cli state purse_01 logs/run_8_0.jsonl
python -m cli replay logs/run_8_0.jsonl
```

A playscript plays end-to-end through the simulator; its log is
byte-identical across runs on the same environment (T1), and the
rendered chronicle is byte-identical, period (a pure function of the
log). Runtime logs land in `logs/` and rendered chronicles in
`output/` (both gitignored).

Fold checkpoints over a committed log (depth-4 — derived artifacts,
never truth; the session resume consumes them as its fast-path —
`--resume` restores the world as snapshot + tail replay, and the
continued run is byte-identical to an uninterrupted session):

```
python scripts/checkpoint.py logs/run_8_0.jsonl            # one end checkpoint
python scripts/checkpoint.py logs/run_8_0.jsonl --every 20 # cadence + the end
```

The one-page digest — the current state, derived (STATUS/TASKS/
DECISIONS are the sources; the digest is a viewport, never a second
truth):

```
python -m scripts.digest
```

## License

AGPL-3.0 — the GNU Affero General Public License v3.0; the full text
lives in `LICENSE` (SPDX: `AGPL-3.0-only`). Donor code/data policy and
licensing stance (what this repo takes in — a separate question from
what it publishes under): `docs/ROADMAP.md` §4. Full verified source
catalog: `docs/REFERENCES.md`.
