# Stanford Generative Agents · `REFERENCES.md` §5 + §14 · Apache-2.0 (repo) + paper (arXiv:2304.03442) · bg-4 (cost notes) / phase 4 (memory patterns)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Catalog row (`REFERENCES.md` §5)
> names the repo `generative_agents (joonspk-research)` with license
> Apache-2.0 — the codebase is in scope per §0.4; we lift patterns
> (memory stream shape, retrieval function, reflection trigger)
> into our `brief/` phase-1+ design notes, never the Python syntax.
> Paper: Park et al., "Generative Agents: Interactive Simulacra
> of Human Behavior", arXiv:2304.03442, UIST 2023. Reference repo:
> `joonspk-research/generative_agents`. Corpus inspected: the
> paper (44 pages), the repo `reverie` backend (Python) and
> `frontend_server` (Flask) — the small Smallville scenario with
> 25 NPCs is the entire study corpus. Catalog-row license match
> check (standing pre-flip per STATUS FAQ): index row ref-7-a
> previously listed "(paper)" — that is misleading; the catalog
> says Apache-2.0 (the repo) and the paper is the academic
> companion, not the license-bearing artifact. Drift fixed in
> the same edit that flips this row todo → done (KI#6-class
> pre-flip caught; the FAQ rule holds).

**What it is.** Generative Agents is a small simulation of 25
LLM-driven NPCs in a 2D tile town (Smallville) where each agent
maintains a memory stream of observations, periodically reflects
on memories to form higher-level conclusions, and plans each
day's schedule through a chain of LLM calls. The paper is the
most-cited LLM-agent reference in the design space; the repo is
the working artefact that produced the paper's results. The
architecture is the **canonical LLM-agent architecture** —
memory + reflection + planning + action — and almost every
later framework (ai-town, letta, the "1,000 People" follow-up)
is either a port or a critique of this design. For canonsim
the relevance is **phase-4 only** (brief / memory layer) and
**almost entirely as a negative reference for phase 0**: the
entire design depends on a stateful LLM in the hot loop, which
our INV-4 forbids in track A.

**Concrete mechanics.**

- **Memory stream — list of `Memory` objects with `description`,
  `creation_time`, `last_access_time`.** Every perception or
  thought an agent has is appended as a `Memory` (one row per
  observation, one per generated thought, one per conversation
  turn). The stream is append-only — there is no deletion, only
  retrieval. The data structure is the simplest possible event
  log per agent: `[Memory(description="..."), creation_time,
  last_access_time]`. This is structurally identical to our
  per-NPC knowledge records in `MVP_SCOPE.md` §10 — same
  append-only shape, same "knowledge = fold(per-NPC event log)"
  fold. The agent's memory stream IS an event log, scoped to
  that agent. The key design decision: **memory is data, not
  behaviour** — the LLM only consumes the retrieved top-k.
  Our `brief/` layer inherits this shape (retrieve → render →
  LLM → parse → emit Intent); the difference is that our memory
  is the canon log (one global stream, filtered by actor /
  knowledge channel), not 25 per-agent streams.
- **Retrieval function — `recency * weight_recency +
  importance * weight_importance + relevance *
  weight_relevance` scalar score.** To answer a query "what
  does the agent remember about X", the retrieval function
  scores every memory in the stream: (a) **recency** =
  exponential decay since `last_access_time` (decay factor
  0.99 per hour of simulation time); (b) **importance** = a
  1-10 integer the LLM assigns at memory creation time
  ("eating breakfast" → 2, "winning an election" → 9); (c)
  **relevance** = cosine similarity between the LLM embedding
  of the query and the LLM embedding of the memory description.
  The top-k memories by scalar score are returned. The pattern:
  **retrieval = weighted sum of three signals, weights are
  hyperparameters**. The repository uses default weights
  `{recency: 1, importance: 1, relevance: 1}` — the paper
  reports these as tunable. The shape is the precedent for
  our `brief/recall.py` (phase 4) — recency = tick delta,
  importance = the event's `weight` field (`EVENT_SCHEMA.md`),
  relevance = embedding cosine over the brief query. Same
  shape, different scoring inputs (we have a tick integer
  clock, not a wall-clock; we have a weight on the event,
  not an LLM-scored importance).
- **Reflection — periodic summary LLM call.** Every N ticks
  (N is the number of new memories since the last reflection;
  the repo uses `threshold = 150` — when the stream has grown
  by 150 since the last reflection, fire one), the agent runs
  a "what 3 high-level questions can I answer from my recent
  memories?" LLM call, then for each question a "answer the
  question, citing specific memories" LLM call, then writes
  the answer as a new `Memory` of type "thought". The new
  thought is appended to the stream — it now competes in
  retrieval alongside raw observations. The pattern: **a
  periodic compaction pass over the log that produces
  higher-level entries that are themselves log entries**.
  This is the precedent for our future `brief/synthesise.py`
  — compaction by recurrence, not by truncation. INV-1
  forbids truncation (the log is append-only); reflection
  is the pattern that compacts without losing data — the
  higher-level entry is a new event, not a replacement.
- **Planning — daily schedule chain through LLM calls.** At
  6 AM agent-time, the agent runs "what's my plan for today,
  given my recent memories and my identity?" — produces a
  high-level plan (an hour-by-hour schedule). Then for each
  hour, recursively expands the hour into 5-minute slots,
  then for each 5 minutes into minute-level actions. The
  recursion bottoms out when the slot is one action long.
  The plan is stored in `Memory` of type "plan" — it
  competes in retrieval just like observations and thoughts.
  If the agent encounters a new observation that
  contradicts the plan, the plan is re-generated from the
  point of contradiction forward. The pattern: **planning =
  hierarchical decomposition with re-plan-on-violation**.
  For canonsim phase-3 director (D-005 consequence planner),
  we lift the **re-plan-on-violation** shape — the director
  generates a seeded-hook chain, and on a violation
  (e.g., the fire was put out before spreading) the chain
  re-plans from that point forward. We explicitly do NOT
  lift the LLM call — the director's planner is a
  deterministic rules-driven planner (`rules.json`
  `effect` family, the Brogue `promoteTile` pattern
  lifted in `brogue.md`). Same shape, different engine.
- **Action — `generate_plural` and `generate_one` LLM call
  with a templated prompt.** When an agent has to choose
  an action (say a line in a conversation, pick a movement
  direction, react to an event), the repo builds a prompt
  template with the retrieved top-k memories, the current
  situation description, and the action grammar, then calls
  the LLM. The output is parsed into a structured action
  (e.g., `{"action": "say", "content": "..."}` or
  `{"action": "move", "direction": "north"}`). The pattern:
  **action = retrieved-context prompt + structured-grammar
  output**. This is the canonical LLM-agent hot loop, and
  it is exactly what our INV-4 forbids in track A. Our
  `brief/` layer (phase 1+, `SPECS_BACKLOG.md` BRIEF_SPEC
  sketch) inherits the prompt template shape, the retrieval
  top-k shape, and the structured-grammar output shape —
  but the LLM call is in track B only, behind the phase-0
  gate. The Intent → Event pipeline is the LLM-output side;
  the brief assembler is the prompt-construction side.
- **`Persona` and `Scratchpad` JSON files.** Each agent has
  a `persona_{name}_{birthday}.json` file with: `first_name`,
  `last_name`, `age`, `innate` (3 Big-Five traits as string
  list), `learned` (3 traits as string list), `currently`
  (3 strings), `lifestyle` (daily schedule template as
  string), `living_area` (place ID). The agent also has a
  `scratchpad` JSON file at runtime with the current plan,
  the current action queue, the current conversation state.
  The pattern: **persona = static data + scratchpad =
  runtime state**; the LLM is stateless between calls, all
  state is in the JSON scratchpad that gets passed to the
  prompt template. For canonsim this is the inverse — our
  agents have a `entities.json` static profile (the
  persona analogue) and a `state = fold(log)` runtime
  projection (the scratchpad analogue); the LLM in track B
  consumes both as part of the brief. The split is clean
  and inherited: static profile JSON + dynamic projection
  JSON, both passed to the brief assembler.
- **Tile-based movement — `maze` module with `tiles` and
  collision check.** Smallville is a 2D tile grid; agents
  move one tile per ~5 simulated minutes. The collision
  check (`is_walkable(tile)`) prevents stacking. The pattern
  is the simplest possible spatial model — a grid with
  walkable / blocked tiles. For canonsim phase-0 the tavern
  is exactly this shape (a single tavern = a tile space with
  walkable / blocked / interactable tiles). The `maze` module
  is not lifted (we do not need a tile maze engine for a
  single tavern), but the "agent occupies one tile, moves
  one tile per tick" model is our `MVP_SCOPE.md` §5 spatial
  system.
- **Conversation — turn-based dialogue via `generate_dialogue`
  with a `conversation_initiator` / `conversation_responder`
  handshake.** When two agents collide, the initiator runs a
  "decide whether to talk" LLM call; if yes, the
  `generate_dialogue` chain starts: each turn is one LLM call
  per agent, with the conversation history as context. The
  conversation ends when an LLM call returns "exit". The
  pattern: **conversation = LLM-terminated state machine
  over shared history**. For canonsim this is the precedent
  for the `talk` action in `actions.json` — but the LLM is
  the text producer, not the participant decider. The Intent
  pipeline (one-shot LLM call per turn) inherits the
  shape; the LLM-as-participant model does not.
- **Reverie — the simulation loop.** `reverie.py` is the
  main loop; it calls `maze.step()` once per simulated
  minute, advancing each agent's plan by one step. The
  loop terminates when the user ends the scenario or after
  a max-tick count. The pattern: **fixed tick rate, agent
  per tick**. This is the same shape as our
  `MVP_SCOPE.md` §5 per-tick update order (KeeperRL
  `Model::tick` lifted in `keeperrl.md`).

**What we take.**

- **The memory stream shape — append-only list of `Memory`
  rows with description + creation_time + last_access_time.**
  Exactly our per-NPC knowledge records in `MVP_SCOPE.md` §10.
  Same fold structure (per-actor projection of the global log).
- **The retrieval function shape — `recency * w_r + importance
  * w_i + relevance * w_rel` top-k.** Phase-4 `brief/recall.py`
  inherits this. We replace the LLM embedding with a
  stdlib-embedder cosine (REFERENCES §14 row, phase 4), the
  LLM-scored importance with the event `weight` field
  (`EVENT_SCHEMA.md`), and the wall-clock recency with the
  integer tick delta. Same shape, deterministic inputs.
- **The reflection pattern — periodic compaction that emits
  higher-level entries that are themselves log entries.**
  Phase-4 `brief/synthesise.py` inherits this. INV-1
  compatible (compaction = new events, not edits).
- **The persona / scratchpad split — static data JSON +
  runtime projection JSON passed to the LLM.** Phase-1+
  `brief/assembler.py` inherits this shape; the LLM
  consumes both as part of the brief, the Intent is the
  LLM's output.

**What we adapt.**

- **The LLM in the hot loop → the LLM in track B only, behind
  the phase-0 gate (INV-4).** Every place where the repo calls
  the LLM, our design defers to the `brief/` layer in phase 1+.
  Phase 0 has zero LLM — the simulator produces facts, the
  chronicle is template-rendered, the LLM does not appear
  anywhere in the canon path. Same retrieval shape, same
  memory stream shape; the LLM call is the part we explicitly
  forbid in track A.
- **The wall-clock time → the integer tick.** The repo uses
  Python `datetime` with a start time and an hour-per-tick
  rate; we use a plain integer tick with the speed of time
  in `rules.json` (one tick = N minutes in fiction, but the
  clock is integer). INV-2 deterministic; the LLM is the
  only non-determinism in the repo (and ours eliminates that
  too in track A).
- **The OpenAI API call → local llama.cpp / Outlines
  constrained decoding (`TECH_NOTES.md` §1).** Phase 1+ uses
  local inference; no network in the canon path (INV-4
  stricter — the repo's OpenAI dependency is the
  track-B-only escape we explicitly reject for track A).
- **The per-agent stream → one global stream + per-actor
  projection.** Generative Agents has 25 memory streams
  (one per NPC); canonsim has one global log + a per-actor
  projection (the `fold` is filtered by actor + knowledge
  channel). Same information density, single source of truth
  (INV-1). The retrieval operates on the projection, not on
  a separate per-agent log.

**What inspires us.** The **"memory is data, retrieval is a
function, the LLM is a stateless caller over the result"**
separation. The repo never lets the LLM hold state between
calls — every call is a fresh prompt with the retrieved
top-k. This is the inverse of the chatbot "conversation
history grows linearly" model; it is the OS-style memory
hierarchy (working set vs archive) that `letta.md` takes to
its extreme. The lesson: a per-call stateless LLM with
explicit retrieval can produce coherent long-horizon agent
behaviour, IF the retrieval is good. For canonsim this
means: the canon log is the memory stream, the brief is
the retrieval result, the LLM is the stateless caller. The
quality of phase-1+ narration is the quality of the
retrieval function — which is why `MVP_SCOPE.md` §10
knowledge records carry a `weight` field for the
importance signal.

**Strengths.**

- Public Apache-2.0 — the entire Python backend is
  readable; `reverie.py` is ~900 lines and is the
  clearest public reference for the canonical LLM-agent
  architecture. Pattern-lifting is permitted per
  `REFERENCES.md` §0.4.
- The memory stream shape is structurally identical to
  our per-NPC knowledge records — same append-only
  list, same per-row creation_time, same retrieval
  pattern. The mapping is one-to-one.
- The retrieval function is small and explicit — three
  signals, scalar weights, top-k. The shape is the
  entire algorithm; the LLM embedding is the only
  component we replace with a stdlib alternative.
- The reflection pattern is INV-1-compatible by
  construction — higher-level entries are new log
  entries, not edits. Compaction by recurrence, not by
  truncation.
- The `Persona` JSON shape is structurally identical
  to our `entities.json` — same static-profile +
  runtime-state split.
- The paper includes the only public cost-per-tick
  numbers for a 25-agent LLM simulation — bg-4
  (`docs/TASKS.md`) inherits this benchmark. Per
  the paper's Table 2 and §6.4, a 2-day simulation
  of 25 agents costs roughly $70 in OpenAI API
  credit (gpt-3.5-turbo at 2023 prices) — the
  cost scales with N agents × M ticks × L calls-per-tick.

**Weaknesses.**

- The LLM is in the hot loop — every agent action, every
  reflection, every conversation turn is one or more
  OpenAI API calls. This is the canonical INV-4
  violation; phase 0 forbids this entire design.
- The LLM is non-deterministic — same prompt, same
  temperature, different outputs across runs. The repo
  uses `temperature=0.9` and a `seed` parameter that
  only partially controls gpt-3.5-turbo. INV-2 (byte-
  identical replay) is impossible with the repo's design;
  our design keeps the deterministic simulator and
  pushes the LLM to the optional narration layer.
- The OpenAI network dependency is hardcoded — the repo
  will not run without an API key. INV-4 stricter: no
  network in track A, ever; the `brief/` layer in phase
  1+ uses local llama.cpp / Outlines (no network).
- No event sourcing — the agent state lives in the
  `scratchpad` JSON files that get rewritten between
  runs; the only "log" is the printed transcript. INV-1
  (state = fold(log)) is the inverse; we keep the
  global JSONL log as the single source of truth and
  the scratchpad as a derived projection.
- No knowledge records with per-channel routing — the
  memory stream is a flat list; there is no distinction
  between "what I saw", "what I was told", "what I
  inferred from absence". Our `knowledge` records
  carry a `channel` field (`seen` / `told` / `inferred`)
  that this repo lacks. The KI#3 expectation_violation
  fix (per-NPC absence detection) requires the
  `inferred` channel — the Generative Agents repo has
  no analogue; absences are not in the stream.
- The conversation model is LLM-terminated (an LLM call
  decides when to stop) — this is the canonical
  indeterminate-loop anti-pattern (INV-2 fix: every
  loop has a deterministic bound).
- The 25-agent simulation takes wall-clock days to
  complete a few simulated days; the cost-per-tick
  is the dominant scaling constraint. Our phase-4
  retrieval + brief budget inherits the cost ceiling
  as a design parameter (`TECH_NOTES.md` §6
  latency/repeat metrics).

**Verdict.** Phase-4 memory-pattern reference, almost
entirely positive on the **memory stream shape** (one-to-one
mapping to our per-NPC knowledge records in `MVP_SCOPE.md`
§10), the **retrieval function shape** (`recency + importance
+ relevance` top-k, lifted into `brief/recall.py`), the
**reflection pattern** (INV-1-compatible compaction by
recurrence), and the **persona / scratchpad split** (static
profile JSON + runtime projection JSON, lifted into
`entities.json` + `state = fold(log)`). Explicitly negative
on the **LLM in the hot loop** (INV-4 forbids this in track
A; the LLM moves to the phase-1+ `brief/` layer behind the
phase-0 gate), the **OpenAI network dependency** (we use
local llama.cpp / Outlines in phase 1+, no network), the
**non-determinism** (INV-2 byte-identical replay is
impossible with the repo's design; we keep the deterministic
simulator + LLM only in the narration layer), the **no event
sourcing** (INV-1 the JSONL log is the inverse — global log
+ per-actor projection, not per-agent scratchpad files),
and the **flat memory stream without per-channel routing**
(our `knowledge` records carry a `channel` field for
`seen` / `told` / `inferred` — the KI#3 expectation_violation
fix requires the `inferred` channel; this repo has no
analogue). Cost benchmark (Table 2, §6.4: ~$70 OpenAI credit
for a 2-day 25-agent simulation at 2023 prices) is the bg-4
benchmark (`docs/TASKS.md` track B); the
`"1,000 People" 2024 follow-up` extends this to N=1000 —
bg-4 inherits both. The repo is the canonical proof that
LLM-agent simulation is architecturally simple (memory +
retrieval + LLM-call + parse) and operationally expensive
(cost ∝ N agents × M ticks × L LLM-calls-per-tick); the
lesson for us is that the canonsim split — deterministic
simulator produces canon, LLM produces prose — is the
cost-engineering response.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
