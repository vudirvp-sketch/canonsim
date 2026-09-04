# MVP_SCOPE.md — TavernSim v0 (Phase-0 Tech Spec)

> Merged MVP scope + TavernSim design, per the unified plan. Single source of
> truth for phase 0. Event field details: `docs/EVENT_SCHEMA.md`. Phases and
> gates: `docs/ROADMAP.md`.

## 1. Purpose & victory condition

Phase 0 builds one dense vertical slice executing the concept's cross-cutting
examples: **pickpocketing a guard, burning down the Three Barrels tavern,
rumors spreading**. The prototype is an executable check of the document.

Victory is NOT "fun". The phase-0 verdict is about **expressiveness of the
mechanisms and combinatorial depth of the ontology**: the chronicle reads as a
story; characters know different things and act on what they know; old events
surface later; losses are permanent. "Fun" is a later property of game design,
not of architecture — a boring four-room scenario is not a verdict on the core.

## 2. Scope

**In scope:**

- 5 locations, 6 NPCs, 5 items, 9 systems, 16 actions — 12 phase-0
  plus the growth rows (rest tune-1/iter-27; document_check iter-43;
  the 9th system, secrets & leverage, iter-44; coerce, the leverage
  spend, iter-45; ramble, the ambient idle beat, iter-53; §4–§7).
- Deterministic core: seed, RngBank (INV-2, RNG-1), integer tick clock, single event
  queue, JSONL append-only log with header (§8, `docs/EVENT_SCHEMA.md` §1).
- Event schema v0 with knowledge records, `state_changes`, `hooks`.
- Content as data: one hand-assembled pack in `content/tavern_pack/` — no
  manifest, no pack CI, no generic loader; a fixed directory read at startup.
- Chronicle rendered by text templates (no LLM).
- CLI mapping 1:1 to the action set (buttons/commands; no free-text parsing).
- Playscript fixtures, test suite (§14), director-off A/B run (§11).

**Out of scope — do NOT build (phase-0 non-goals):**

Big world & worldgen; lazy depth; factions with goals (phase-5 territory — the
risks live in phases 0–1); any LLM in the product; free-text input; UI,
SillyTavern, Soul-of-Waifu integration; pack system & worldbuilder; magic,
economy, combat system; "a full game"; pulling external code (C:DDA fire →
phase 3, Azgaar worldgen → phase 5, Brogue levels → later); document factories
beyond what already exists.

## 3. Target walkthrough (what the slice must produce)

> Day 1, evening. The player enters the Three Barrels. Doren stands at the
> bar. A pickpocket attempt — Doren notices the movement and remembers the
> player (knowledge record: saw, partial). The barkeep notices the noise
> (heard, vague). At night the player drops a lamp by the back wall (action
> "drop/break" → fire source) — fire, alarm, and the guards hand the knowledge
> to each other at watch change (knowledge-transfer event). Next morning the
> drunkard tells the market about a figure at the back door (rumor = transfer
> with fidelity loss: position known, identity not).

Later a narrator is layered onto this canon ("The flame eagerly licked the dry
beams...") — but the fact of the fire belongs to the simulator, not the model.

## 4. World model

### 4.1 Locations (5)

| ID | Name | Role in the slice |
|---|---|---|
| `loc_tavern` | Three Barrels tavern | main scene: bar, tables, back door |
| `loc_street` | street in front of the tavern | escape route, patrol path |
| `loc_backyard` | backyard | fire source spot; origin of the "figure at the back door" rumor |
| `loc_guardroom` | guard room | watch change → knowledge transfer between guards |
| `loc_market` | market square | the rumor scene (mandatory: this is where hearsay lives) |

### 4.2 NPCs (6)

| ID | Name | Role | Simple goal |
|---|---|---|---|
| `pc_01` | the player | thief down on his luck | get money, stay free |
| `npc_guard_01` | Doren | on-duty guard | keep order |
| `npc_guard_02` | second guard | Doren's relief | keep order |
| `npc_barkeep_01` | barkeep | tavern owner | protect the property |
| `npc_drunk_01` | drunkard | witness by accident | get ale |
| `npc_maid_01` | serving maid | moves around, sees much | finish the shift |

NPC record: `id`, `name`, `role`, `position`, status flags (fatigue /
intoxication / fear / injury), relations map to the PC (reputation, suspicion,
trust, fear), **plus a sparse pair-keyed NPC↔NPC relations map (iter-3, P2a,
D-020 — rumor trust weights have a data home)**, knowledge set, mood trend,
simple goal.

Ambient group entity: `npc_market_crowd_01` (the market crowd) — a passive
knowledge-holder used by the §3 walkthrough and the rumor example in
`docs/EVENT_SCHEMA.md` §3. Not one of the 6 individual NPCs: no goals, no
relations, no movement — it only receives knowledge records (rumor listener).

### 4.3 Items (5)

| ID | Item | Notes |
|---|---|---|
| `oil_lamp_01` | oil lamp | fire source; breakable |
| `purse_01` | purse | owned by Doren; steal target |
| `ale_mug_01` | mug of ale | intoxication vector |
| `club_01` | club | barkeep's, under the bar |
| `rope_01` | rope | utility, in the backyard |

## 5. Systems (9)

| # | System | Owns | Notes |
|---|---|---|---|
| 1 | time | tick counter, day phase (morning/afternoon/evening/night), ticks-per-action | integer ticks only |
| 2 | position & visibility | who is where; line of sight, hearing radius | perception-check input |
| 3 | relations | per (npc, pc): reputation, suspicion, trust, fear; plus the sparse npc↔npc pair map (iter-3, P2a/D-020) | numeric 0–100 |
| 4 | knowledge | knowledge records; rumor transfer with fidelity loss | `docs/EVENT_SCHEMA.md` §3; the psychological echo (social-2/iter-46, P3e) reads these records — `core/echo.py`, the residue as a behavior gate (INTENT_SCHEMA §3 `echo_at_least`) |
| 5 | states | fatigue, intoxication, fear, injury | modifiers on perception & behavior |
| 6 | fire | source, flammability, spread, smoke, alarm | irreversible state changes |
| 7 | crime & watch | suspicion thresholds, document check, arrest attempt, watch change | no group reputation — knowledge spread models it (§10) |
| 8 | director | deferred-consequence buffer, triggers, stagnation detector; the release-chain layer (arc-1/iter-47, P3c — `director.arcs` pack chains: the order law + the min-gap pacing + the entropy mirror, DIRECTOR_SPEC §3d) | §11 |
| 9 | secrets & leverage (iter-44, P3a) | the fact-cluster registry (`rules.json::secrets`) + the leverage birth reaction and spend door; a novel knower of a declared secret token mints a `leverage_gained` fact event (holder, subject, type, expiry); liveness is a read-side fold | `core/leverage.py`; the CK3 `add_hook` precedent — the fact is immutable, the spend a new event naming the cluster's id (iter-45: the `coerce` action, `leverage_over` the door) |

## 6. Intersection matrix (first-class design artifact)

| Chain | What it produces |
|---|---|
| fire → smoke → visibility → perception → knowledge | witnesses know less through smoke |
| knowledge → suspicion → guard behavior | partial sightings escalate |
| intoxication → perception → witness quality | the drunkard's testimony is vague by construction |
| time → fatigue → NPC goals | guards rotate, the maid goes home |
| hooks → buffer → director release | delayed consequences fire causally |
| hooks → arc → ordered release | the chain's beats march in pack-declared order, spaced by the gap law — tension shaped as a sequence, not a pile (arc-1/iter-47, P3c; DIRECTOR_SPEC §3d) |
| position → visibility → crime success | where you stand decides what you can steal |
| relations → talk → rumor acceptance | trusted tellers spread rumors faster |
| knowledge → secrets → leverage → coerce | a witnessed secret becomes a social fact: novel knowers mint immutable leverage clusters (told secrets included — the briefing mints the relief's); the spend (iter-45) plays the card — the cluster dies in the fold, the subject's directed pair axes shift (the balance) |
| knowledge → echo → behavior | the emotional residue of what an NPC knows — per-NPC valence decaying with ticks since learned, scaled by fidelity — gates autonomous behavior (`echo_at_least`, the P2b read; iter-46, P3e: the watcher who saw the fire is jittery next morning, and the residue fades so "events that happened but no longer matter" stop driving behavior) — a read model, never canon, never an entropy input (L6) |
| leverage → relations | what a spent cluster buys is pack data: trust breaks fast, fear spikes — the directed pair map, never a group reputation |

Eight systems taken separately are trivial — emergence lives at the
intersections. The log metrics (§15) measure exactly this. (The ninth
— secrets & leverage, iter-44 — is a knowledge-family reaction: its
intersections are the two rows above that already pass through
knowledge.)

## 7. Actions

Phase 0 landed 12; tune-1 (iter-27, D-059) added `rest` as pack data over
the `recuperate` resolver — the registry grows only with a new mechanic;
iter-43 (D-072) added `document_check` as pack data over the `inspect`
resolver — the crime ladder's public rung (the deferred consequence
became a real action: the watcher's scrutiny vs the stranger's composure,
the verdict token escalating through the standing crime reactions);
iter-45 (D-074) added `coerce` as pack data over the `coerce` resolver —
the leverage spend (social-1b): the fact cluster's first runtime consumer,
the door reading the live-leverage fold, the balance (what the cluster
buys) pack-declared pair-axis shifts.

| Action | Intent type | Ticks | Check | On failure | Knowledge produced |
|---|---|---|---|---|---|
| look around | `look_around` | 1 | — | — | self: scene snapshot |
| examine | `examine` | 2 | perception | vague info | self: details |
| approach | `move` | 2–4 | — | — | observers see movement |
| talk | `talk` | 4–8 | relations | cold shoulder | both: conversation topic |
| wait | `wait` | N | — | — | — |
| take | `take` | 2 | stealth if owner near | noticed | owner/observers: saw/heard |
| drop / break | `drop_break` | 1–2 | — | — | noise (heard); lamp → fire source |
| use | `use` | 2–6 | context | no effect | observers |
| steal | `steal` | 3 | stealth vs perception | partial/total failure | rich records: saw(partial), heard(vague) |
| distract | `distract` | 3 | social | ignored | target attention state |
| set fire | `arson` | 4 | fire source + flammable target required | abort | alarm, smoke, visibility drop |
| flee | `flee` | 2+ | pursuit | caught | guards: chase knowledge |
| rest | `rest` | 60 | — | — | — (tune-1: fatigue −30, pack `status_effects`) |
| demand papers | `document_check` | 2 | scrutiny (perception) vs composure (social) | talked down | actor: the verdict; room: the public challenge (iter-43) |
| lean on | `coerce` | 3 | live leverage required (the door reads the fold) | door rejection | — : the quiet corner; the subject's pair axes shift (iter-45) |

Free-text input arrives when the C-parser can decompose it into these same
intents (phase 2). Buttons/commands are shortcuts to identical intents.

## 8. Time, tick loop, event queue

- Integer tick `t` from 0. Day phases map to tick ranges; a full day ≈ 1440
  ticks (tunable in pack rules). Typical action = 2–8 ticks.
- Single event queue: `heapq` with key `(tick, sub_order, actor_id)`;
  `sub_order` fixes system ordering within a tick.
- Actions with duration: at commit, a completion entry is enqueued at
  `t + duration`. No mid-action cancellation in v0 (a cancelled action is a
  new event).
- Player intent = an event in the same queue (sub_order before NPC reactions).
- Determinism rules: INV-2 (`AGENTS.md` §4). No wall-clock anywhere,
  **including the log header**.

```text
while queue not empty:
    (t, sub_order, actor_id) = heappop(queue)
    execute entry: system updates, checks, RngBank draws (INV-2)
    emit events (append-only; every state change is an event)
    enqueue completions/hooks with their trigger ticks
```

## 9. Events

Full contract: `docs/EVENT_SCHEMA.md`. Canonical example (`ev_0007`):

```json
{ "id": "ev_0007", "t": 412, "type": "pickpocket_failed",
  "actor": "pc_01", "target": "npc_guard_01", "cause": "ev_0006",
  "outcome": { "noticed": true },
  "knowledge": [
    { "who": "npc_guard_01", "channel": "saw", "fidelity": "partial",
      "knows": "figure_reaching_for_purse", "at": 412, "source": "ev_0007" },
    { "who": "npc_barkeep_01", "channel": "heard", "fidelity": "vague",
      "knows": "noise_by_the_bar", "at": 412, "source": "ev_0007" } ],
  "state_changes": [
    { "entity": "npc_guard_01", "prop": "suspicion_of.pc_01", "from": 0, "to": 25 },
    { "entity": "pc_01", "prop": "status", "from": "unknown", "to": "suspect" } ],
  "hooks": ["guard_suspicious_of_pc", "possible_document_check"],
  "importance": "medium",
  "provenance": { "seed": 42, "cause_intent": "intent_0006" } }
```

Schema rules (short form; full form in EVENT_SCHEMA.md):

- `known_by` is a derived index over `knowledge` — never a primary field.
- A rumor is a knowledge-transfer event with fidelity loss. The drunkard
  telling the market about "a figure at the back door" is a machine fact:
  position known, identity not. Distortion comes from source incompleteness —
  no separate rumor system.
- Lies are expressible: an intentional record with lowered fidelity or a
  distorted `knows` (foundation for `believes/lies`, phase 4).
- `state_changes` with `irreversible: true` carry irreversibility — the
  "burned tavern" test finally has a handle.
- No group reputations in v0: "reputation among the watch" = knowledge spread
  between guards (transfer event at watch change).
- `importance` is computed by the pack rule (entities touched +
  irreversibility + far hooks + the story-critical hook — tune-1/D-059:
  pack-listed event types score a bonus, the signal/noise split the tale
  gate reads), never by feel.
- `visibility` is perception-check input; `knowledge` is its result — not
  duplicate fields.

## 10. Knowledge model

- Channels: `saw`, `heard`, `told`, `inferred`. Fidelity: `exact`, `partial`,
  `vague`.
- Transfer: when NPC A tells NPC B, B receives a record with fidelity decayed
  one step (exact → partial → vague) and `channel: told`.
- Blind-NPC rule: no record → the NPC cannot know it and cannot say it (T3).
- A lie is a crafted record (distorted `knows`, or fidelity misrepresenting
  the source) — legal data, not a special mechanism.
- **Expectation violation (iter-3, P2d, KI#3):** a behaviour rule in
  `rules.json` generates per-NPC expectations from schedule + position
  (e.g., "guard expects `purse_01` on the bar at watch start"); perception
  compares expected vs observed; on mismatch, an `inferred`-channel
  knowledge record is emitted (e.g., `knows: "purse_missing_from_bar"`,
  cause-chained to the theft event). No new schema field — expectations
  are behaviour functions, not state; the record uses the existing
  `inferred` channel. This is the only legitimate trigger for
  suspicion-from-absence: a guard cannot arrest on "purse not seen", but
  can on `inferred: purse_missing_from_bar` cause-chained to `ev_0007`.

## 11. Director = consequence planner, not improviser

- "Document check in two hours" is not a director decision at moment X. It is
  a consequence seeded **into the buffer at event time**, with triggers
  (time / place / suspicion threshold).
- The stagnation detector only decides **when to release already-seeded
  material**.
- Therefore the director is causal by construction; a complication "out of
  nowhere" is a bug. Named anti-pattern: the RimWorld storyteller materializes
  threats from nothing — exactly what we do not do.
- **Director-off control run is mandatory**: A/B on identical seed +
  playscript. If all emergent chains are director injections, the core is dead
  — phase 0 must see it. Conversely: boredom of a four-room scenario is not a
  verdict on the core; the verdict is about expressiveness and combinatorial
  depth (§1).

## 12. Chronicle & CLI

- Chronicle = dry, templated rendering of the log: day headers, event lines
  from pack templates. No LLM, no embellishment — the readability test (T7)
  runs on exactly this output.
- CLI commands: `play <playscript>`, `look`, `wait N`, `chronicle`,
  `state <entity>`, `replay <log>`, `directors on|off`, `seed <n>`.

## 13. Playscripts

```json
{
  "name": "day1_theft_and_arson",
  "seed": 42,
  "pack": "tavern_pack@0.1",
  "steps": [
    { "intent": "move", "target": "loc_tavern" },
    { "intent": "steal", "target": "npc_guard_01", "method": "distraction" },
    { "intent": "wait", "ticks": 120 },
    { "intent": "move", "target": "loc_backyard" },
    { "intent": "drop_break", "target": "oil_lamp_01", "near": "back_wall" }
  ]
}
```

One artifact, four roles: test fixture, demo, future LLM-circuit benchmark,
regression anchor. The runner and the first fixture land in iter-1; the
suite grows through iter-2.

## 14. Tests (from day one)

| ID | Test |
|---|---|
| T1 | **Determinism:** seed + playscript = identical log; two runs byte-identical (fixed environment and header). |
| T2 | **Replay:** fold(log) restores state — event-sourcing invariant. |
| T3 | **Blind NPC:** no record in `knowledge` → does not know, cannot say. |
| T4 | **Irreversibility:** an `irreversible` state change never reverts without an explicit counter-event (fire has none). |
| T5 | **Impossible stays impossible:** teleport, arson without a fire source, taking an absent item, knowing the unseen. |
| T6 | **Smoke:** 1000 ticks without exceptions or hangs. |
| T7 | **Readability:** a human reads the chronicle and retells the story in their own words (manual gate). |
| T8 | **Director-off:** ≥3 emergent chains without the director; its contribution measured A/B. |

Plus T0 (from iter-1): every log line validates against
`schemas/event.schema.json`; the example in EVENT_SCHEMA.md is a test fixture.

## 15. Metrics (computed from the log, not by feel)

- **M1 cross-system share:** events touching ≥2 systems / all events.
- **M2 deferred hooks fired:** hooks released by trigger / hooks seeded.
- **M3 causal chain length** (D-019, iter-6): mean/median depth of the
  `cause` chain per event, from the log alone. Depth-equation Causality
  factor, measured.
- **M4 novelty/repetition** (D-019, iter-6): rate of repeated (type, actor)
  bigrams; share of distinct `knows` tokens. RimWorld's repetitive-tale
  problem, measured instead of felt.
- **M5 non-PC event share** (D-019, iter-6): events with actor ≠ player /
  all events. "World not player-centered" (Kenshi/RimWorld lesson) made
  measurable at the director-off gate (T8).
- **Causal-density checklist** — every event answers: what changed in the
  world · who learned what, at what fidelity · who can be wrong · who can lie
  · what became irreversible · what future conflict did it seed · can it be
  used 10–50 turns later.
  - Bad event: "tried to steal — failed" (the world did not change, nothing
    to grab).
  - Good event: "tried to steal → guard noticed the movement (partial
    knowledge) → suspects the player → barkeep heard the noise → two hours
    later — a document check" (the deferred consequence fired).

Thresholds are set at the iter-6 gate review from the measured baseline — not
invented now. Direction: M1 non-trivial and rising across the slice; M2
non-zero; M3 mean ≥ 2 (one event, then another = failure); M4 novelty share
rising; M5 non-zero at director-off.

Signs of a living prototype: the player says "I'm in trouble *because* I did
that"; the world remembers; old things resurface; characters know different
things; there are unrecoverable losses; the chronicle reads without
ornaments. "One thing happened, then another" = failure; a causal chain =
norm.

## 16. Exit & kill criteria

**Exit criteria (all must hold):**

1. 1000 ticks without exceptions or hangs (T6).
2. Determinism: byte-identical replays (T1); replay fold == state (T2).
3. ≥3 emergent chains with director off (T8).
4. Chronicle readable and retold by a human (T7).
5. 0 knowledge leaks on the blind-NPC suite (T3).
6. Impossible stays impossible (T5).

**Kill criteria (any → stop, rethink the ontology):**

- Events without consequences.
- Knowledge does not affect behavior.
- The director produces noise instead of causal complications.

## 17. Build sequence (iteration-counted — calendar dropped, D-029)

> The original two-week day-numbered sprint map was dropped: the
> owner-directed reference-research phase (iter-0..0v) consumed the calendar.
> Sequencing is by iteration count only; per-iteration donor designs live in
> `docs/blueprint/phase0.md`, the build index in `docs/BLUEPRINT.md` §3.

| Iteration | Deliverable |
|---|---|
| iter-0..0v (done) | docs & tooling bootstrap; reference research: 33 deep dives (`docs/ref/`) distilled into the blueprint (D-027/D-028); concept realignment (D-029) |
| iter-1 | seed, RngBank, clock, queue, JSONL log with header, playscript format, pack skeleton: world creates from seed, an event writes, a playscript plays |
| iter-2 | actions, checks, outcomes, event emission: steal / arson / talk = fact |
| iter-3 | knowledge records, transfer-rumors, suspicion, relations, NPC memory: characters know different things and react differently |
| iter-4 | director planner: consequence seeding, triggers, stagnation detector |
| iter-5 | chronicle templates, scene card, CLI: playable and readable without LLM |
| iter-6 | tests T1–T8, director-off A/B, manual playtest → phase-0 verdict |

Background: `bg-1..bg-4` run in parallel on foreign canon (`docs/TASKS.md`).

## 18. Code layout & conventions

- Python (iterations, schemas, CLI). Rust/TypeScript = separate decision after
  the core is confirmed.
- `core/` (clock, rng, queue, log writer, fold/replay, ids, intent
  front-door + checks + OCC, action resolvers + registry, transitions,
  scheduler) · `sim/systems/` (the 8 — declared as pack data from iter-2,
  first system code in iter-3) · `content/tavern_pack/` (JSON: entities,
  actions, rules, templates) · `render/` (chronicle) · `brief/`
  (reserved, phase 1) · `cli/` · `tests/` + `tests/playscripts/`.
- stdlib-only runtime deps; pytest + ruff as dev deps. Type hints on public
  functions. No `print` in committed code (CLI-class tools excepted — `cli/`
  and the operator scripts in `scripts/`, D-046) — log instead.
- Core code never mentions domain words (INV-3); a grep stoplist test
  enforces it from iter-2.
