# canonsim

Deterministic canonical simulation core for an LLM-narrator architecture.
Phase 0 deliverable: **TavernSim v0** — one tavern, a theft, an arson, spreading
rumors — running as a pure Python simulation with an append-only event log.
No LLM anywhere near the canon yet.

> **Simulator produces facts. LLM produces prose. The log stores canon.
> The mediator holds the boundary.**

North star: a "living world" simulation mode inside
[Soul-of-Waifu](https://github.com/jofizcd/Soul-of-Waifu) (local-first desktop
AI companion app) — see `docs/VISION.md` §10. This repo stays frontend-agnostic
until the phase-1 gate.

## Status

**Phase 0 gate: PASS** (iter-6, 2026-08-28). All `MVP_SCOPE.md` §16
exit criteria met; no kill-criteria hit. The simulator produces
facts; the chronicle reads them from the log; the world acts without
the player (M5 p50=0.77 across 1000 seeds); old events surface later
via the reaction cascade + watch rotation; losses are permanent (the
backyard stays destroyed — T4). The gate deliverables: `docs/TEST_PLAN.md`
(T0–T8 + M1–M5 + gate protocol + UAP crosswalk), `core/metrics.py`
(M1–M5 + emergent-chain count as pure functions of the log — Mesa
`DataCollector` inverted), the T1 fixture-regeneration guard
(schema-version pin + fresh-regen byte diff), `tests/test_t8_ab.py`
(single-factor A/B: ≥3 emergent chains OFF, director_0000 fires ON,
seed 125 gate playscript), `scripts/balance_harness.py` (KI#4 close —
the 1000-sim distribution harness; full table in `output/`). Phase 1
(narrator over the log) opened with the iter-7 intake and landed its
first deliverable at iter-8: `docs/BRIEF_SPEC.md` + `brief/assembler.py`
— the deterministic eight-block brief (budgets, eviction, voice
isolation) as pure functions of (log, ledger), zero RNG, byte-identical
on the golden fixture. Its second deliverable landed at iter-9:
`docs/VALIDATION_SPEC.md` + `brief/validator.py` — the mediator's
deterministic validation gate (the closed proposal document — prompt
injection neutralized structurally; honest verdicts
supported/contradicted/insufficient_data under closed-world semantics;
ExpectedVersion OCC; the fact-transaction pass-through; the ≤2-regens
protocol; a committed golden set pinning verdict semantics). Its third
landed at iter-10: `brief/ledger.py` + the `scene_texture` 7th brief
block — the session scene ledger (the texture stream: entry lifecycle,
scenes as PC-location intervals, the one validation gateway, canon
outranks texture, tombstones; the BRIEF_SPEC §9 atomic flip — the
purity pair is now (log, ledger), D-053). Its fourth landed at iter-11:
the texture promotion door — the narrator boundary's LLM-free half
(`core/intent.py` texture path: a texture-capable action's pack
`texture` block replaces the canon preconditions for intents carrying
the mediator-resolved reference — core stays ledger-blind — and a
take-success IS the promotion, the slot's canon birth; D-054; the
laundering + unique_slot golden pins complete the 8-reason refusal
vocabulary). The iter-11a audit hardened the door: conditional take
templates render the promoted slot noun (the texture-path chronicle
line), unique-slot claims survive promotion, canon-slot overlap
includes pack-modeled fields (KI#39..41). **Phase 1 gate: PASS**
(iter-26, D-058 — the owner's quality-first close): 109 live beats
over 10 narrate sessions with **0 canon violations**, the phase-1
regression corpus at 105 distilled cases replayed through the real
mediator cycle, T1 byte-identity + the T8 single-factor A/B re-run;
the narrator landed agent-in-the-loop at iter-12 (D-055 — the
dev-time engine is the owner's assistant over a call/reply file
contract; the repo stays LLM-free, INV-4 unchanged) and the polish
menu closed iter-27–29 (tune-1/tune-2/pack-2, D-059–D-061).
**Phase 2 (parser, mode C) gate: PASS** (iter-31 opened it, D-062 —
the owner's call; closed iter-35, D-064 — the owner's "continue per
the plans" session call): the mode-C boundary's LLM-free half — the
grammar snapshot (pack verbs ∪ addressable nouns; ghost interactivity
structurally impossible), the parse call/reply file contract with the
closed reply {intent | question | no_intent} gated at the boundary,
the pin law, the `say`/`say apply` session door; contract owner
`docs/PARSER_SPEC.md`. parse-1 validation beats landed iter-32 (six
live say-door sessions, 30 utterances, 0 honest misfires) and grew
iter-33, batch 2 (the owner's corpus-growth call: four more sessions —
seeds 111/65/30/32; 51 combined utterances, 35/35 boundary validity —
the ≥90% criterion MET on the combined volume per PARSER_SPEC §6; the
parse-reply regression corpus 10 cases); the gate's §5 protocol re-run
reproduced the iter-26 numbers exactly (day1_full ON M1=0.417 /
M2=0.500; T8 OFF 26 chains). Track B: **bg-2 DONE** (the owner supplied the four
world exports; `docs/TAXONOMY.md` — 120 DF events across the 16 bg-2
target types with ontology verdicts + the sink v2 plus pass, D-063);
**bg-3 DONE** (iter bg-3 — the owner re-supplied large/medium/
small-dense; `scripts/df_briefer.py`: the POV mini-briefer + the
closed-vocabulary reverse validation over the sink + the ≤2-regen
ladder + the retrieval stress — 4 live cases, 0 honest misfires,
brief p50 ≈ 2.9 KB on GB-scale exports; numbers owner
`docs/TECH_NOTES.md` §3.3). 697 tests green, ruff clean,
golden fixtures byte-identical. **Phase 3 (Director) OPEN** — iter-36,
the owner's "continue per the plan" call (the iter-31 precedent): the
pacing clock landed first (DIR-1, D-065 — the L4D peak/rest donor:
the per-run RAMP/PEAK/REST/STAGNATION machine over narrative entropy,
`director.pacing` pack data + lint, REST = the post-climax breathing
room, explicit triggers ungated; contract owner `docs/DIRECTOR_SPEC.md`
§5); the exit-criterion instrument landed iter-37 (DIR-2, D-066 —
`core.metrics.eventless_beat_stretches` + the harness `--pacing
on|off` A/B; measured 1000 seeds: both arms byte-identical — every
day1_full run ends in PEAK, the clock inert on this pack+script; max
stretch 1; contract owner `docs/TEST_PLAN.md` §6); the climax layer
landed iter-38 (DIR-3, D-067 — the L4D2 three-intensity rule:
`director.pacing.climax_floor` 75 = 3× the peak floor, the climax
release path at the END of a peak, the one-beat `PEAK_CLIMAX` boss
state; the pack declares the layer, no hook carries the flag — it
lands with the `document_check` action, the owner's content call);
the multi-channel quiet split landed iter-39 (DIR-4, D-068 — the L4D
three-director family: `director.channels` threat/social/ambient with
per-channel quiet floors + input bindings, `SeededHook.channel`, the
per-hook `permit_quiet` gate; clock/budget/climax/explicit triggers
stay global on purpose; the v0.1 global floor survives for channelless
hooks — the per-hook opt-in, the climax-flag pattern); the event
grammar's predicate + weight layer landed iter-40 (drama-1, D-069 —
the Paradox trigger block adapted: `core/predicates.py` the JSON
predicate grammar (the three v0.1 leaves byte-identical + compound
`all`/`any`/`not` + the `prop` leaf), the `weight_multiplier` object
(the entropy sensor reads the effective weight per beat),
`first_time_only` the burn policy); the grammar's option layer landed
iter-41 (drama-2, D-070 — per-option availability gates +
`ai_chance`-style weights (a pure deterministic pick: heaviest wins,
ties by declaration order, zero never picked, all-closed defers) +
whole-key payload overrides); the grammar's on_action dispatch landed
iter-42 (drama-3, D-071 — `core/onaction.py` + the `on_action` pack
table: event X commits → content reacts, appended after the hardcoded
system reactions (the donor's append-not-overwrite composition); the
`witnesses` scope + the per-entity quantified gate (the explicit ctx
argument — "every NPC who witnessed X") + the alarm-shaped state
change; the one-hop law terminates the cascade; the pack's entry is
dormant on `document_check` until the action lands, the owner's
content call — the grammar's three layers are COMPLETE). 836 tests
green, ruff clean, zero fixture regen (the 10-seed A/B per landing:
10/10 byte-identical each time; TEST_PLAN §6). Contract owner
`docs/DIRECTOR_SPEC.md` §3/§3a/§3b/§3c.
Next: the phase-3 social-depth run (`social-1/2`, `arc-1`;
`docs/TASKS.md`) + the owner-gated set (parse-2, engine-1, the
document_check content decision — with it the climax flag and the
crowd-witness reaction, ambient-channel content).

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
| `docs/` | all specs & plans (see `docs/AGENT_NAVIGATION.md` §1) |
| `schemas/` | machine-readable contracts (`event.schema.json`) |
| `content/tavern_pack/` | setting as data (v0.1; loaded + linted by `core/pack.py`) |
| `core/`, `sim/systems/`, `render/`, `brief/`, `cli/` | code (core iter-1..4; the iter-3/4 systems live in `core/` per D-037 — `sim/systems/` stays reserved for periphery; render + cli landed iter-5; `core/metrics.py` landed iter-6; `brief/`: `assembler.py` iter-8 — the deterministic brief, `docs/BRIEF_SPEC.md` · `validator.py` iter-9 — the validation gate, `docs/VALIDATION_SPEC.md` · `ledger.py` iter-10 — the session scene ledger, `docs/BRIEF_SPEC.md` §3.3 · `mediator.py` iter-12 — the narrator boundary's document layer, D-055 · `parser.py` iter-31 — the phase-2 mode-C boundary, `docs/PARSER_SPEC.md`) |
| `scripts/` | operator tooling (CLI-class, D-046): `balance_harness.py` iter-6 (the 1000-sim distribution harness, KI#4 close) · `df_survey.py` iter-8e (DF Legends XML empirical survey — the bg-1 sanitize+stream core; measured numbers in `docs/TECH_NOTES.md` §3.1) · `df_import.py` bg-1 (the SQLite sink — typed cores + EAV + participant index + generic JSON records; bg-2: the plus pass, sink v2; `docs/TECH_NOTES.md` §3.2, D-051/D-063) · `df_taxonomy.py` bg-2 (the event-taxonomy survey over the sink DB; `docs/TAXONOMY.md`) · `df_briefer.py` bg-3 (the POV mini-briefer + reverse validation over the sink; `docs/TECH_NOTES.md` §3.3) · `profile_harness.py` iter-30 |
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
python -m cli chronicle logs/run_8_0.jsonl
python -m cli state purse_01 logs/run_8_0.jsonl
python -m cli replay logs/run_8_0.jsonl
```

A playscript plays end-to-end through the simulator; its log is
byte-identical across runs on the same environment (T1), and the
rendered chronicle is byte-identical, period (a pure function of the
log). Runtime logs land in `logs/` and rendered chronicles in
`output/` (both gitignored).

## License

TBD — no monetization planned. Donor code/data policy and licensing stance:
`docs/ROADMAP.md` §4. Full verified source catalog: `docs/REFERENCES.md`.
