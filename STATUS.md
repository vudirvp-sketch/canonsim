# STATUS — canonsim

Iteration: 0p (owner-requested: ref-7 batch — Stanford Generative Agents + ai-town + letta LLM-agent precedents, mostly negative) · Phase: 0 — simulator without LLM · Date: 2026-08-26

iter-0p is the **ref-7 3-batch iteration** — the
open-licensed LLM-agent precedent family (one repo + paper,
one MIT multi-agent sandbox, one ex-MemGPT memory architecture;
all open per `REFERENCES.md` §5 — pattern lifting permitted,
port the shape not the syntax per §0.7 / D-015), each in
its own per-ref file:
`docs/ref/generative_agents.md` (371 lines — Park et al.
2023 memory stream shape [list of `Memory` objects with
`description`/`creation_time`/`last_access_time` — one-to-one
with our per-NPC knowledge records in `MVP_SCOPE.md` §10],
the retrieval function `recency * w_r + importance * w_i +
relevance * w_rel` top-k [same shape lifted into
`brief/recall.py` — stdlib embedder instead of LLM
embedding, tick delta instead of wall-clock recency, event
`weight` field instead of LLM-scored importance], the
reflection pattern [periodic compaction LLM call every N new
memories, threshold=150, that emits higher-level entries
that are themselves log entries — INV-1-compatible compaction
by recurrence, not by truncation; lifted into
`brief/synthesise.py`], the planning pattern [hierarchical
decomposition with re-plan-on-violation; lifted into iter-4
director `seeded_hooks` re-plan-on-violation], the
`Persona`/`Scratchpad` JSON split [static profile + runtime
projection, both passed to the LLM; lifted into
`entities.json` + `state = fold(log)` + phase-1+
`brief/assembler.py`], the `agentStep` LLM hot loop [the
canonical LLM-agent architecture], the 25-agent Smallville
cost benchmark [~$70 OpenAI credit for 2-day simulation
at 2023 prices, per paper Table 2 §6.4 — the bg-4 benchmark;
the `"1,000 People" 2024 follow-up` extends to N=1000],
explicitly negative on LLM in hot loop [INV-4 forbids in
track A; the LLM moves to phase-1+ `brief/` layer behind
the phase-0 gate] + OpenAI network dependency [INV-4
stricter — local llama.cpp/Outlines in phase 1+] +
non-determinism [INV-2 byte-identical replay impossible
with the repo's design; `temperature=0.9` + partial `seed`
control only] + per-agent scratchpad files [INV-1 amnesia
— our JSONL log + per-actor projection is the inverse] +
flat memory stream without per-channel routing [no
`seen`/`told`/`inferred` distinction — KI#3
expectation_violation fix has no analogue here]);
`docs/ref/ai_town.md` (345 lines — Convex reactive database
[table-based world state: `world`/`players`/`agents`/
`messages`/`conversations`/`archives`; the only "log" is
Convex internal history, not byte-identical replayable],
the `engine.ts` simulation loop [single Convex transaction
per tick; per-agent LLM call in sorted insertion order —
determinism hazard we would fix with `sorted()` by ID],
the `agentStep` per-tick LLM call [prompt template +
retrieved top-k memories + action grammar + LLM call +
zod-parse to `MoveAction`/`SayAction`/`WaitAction`
discriminated-union — lifted into `templates.json`
`action_type` enum shape; the per-tick LLM call is the
INV-4 violation we explicitly reject], the conversation
handshake [`startConversation` creates a `conversations`
row with both agent IDs + unique conversation ID; each
turn per agent includes the recent `messages` from the
other; ends on `LeaveAction` — lifted into phase-1+
`talk` action brief shape; the LLM-as-participant model
does not], the `archives` table compaction [periodic
summary LLM call writes a single row with `description`/
`agentId`/`createdAt`; recent-messages context then pulls
from `archives` (compacted) + most recent `messages` (raw)
— same reflection shape as `generative_agents.md` but on
a database table, not a memory stream], the
`world.ts` tile grid [2D integer grid stored as a string
in the `world` table's `currentView` field, one char
per tile, `tileset.json` charset — the simplest possible
spatial model; phase-0 tavern inherits the grid-as-data
shape], the `prompts/` directory [LLM prompt templates as
plain `.txt` files with `{placeholder}` tokens, runtime
= string replace — same shape as our `templates.json`
(tracery grammar lifted in `tracery.md`)], the pixi.js
reactive frontend [subscribes to Convex tables, re-renders
on each mutation — the inverse of our phase-0 architecture
(no UI/server per `MVP_SCOPE.md` §2 non-goals)], the
GitHub OAuth Convex Auth multi-tenant [irrelevant for
phase-0 single-user CLI], the `memories` table schema
[`agentId`/`description`/`createdAt`/`importance` 1-10
— same field shape as our per-NPC knowledge records; the
per-agent table is the inverse of our global JSONL log +
per-actor projection], explicitly negative on Convex
reactive database substrate [INV-1 + INV-2 inverse —
mutable tables + non-deterministic mutation order; our
JSONL log + SQLite index is the right substrate] + LLM
in hot loop [INV-4] + OpenAI/Anthropic/OpenRouter network
[INV-4 stricter] + reactive frontend [`MVP_SCOPE.md` §2
non-goal — no UI in phase 0] + insertion-order iteration
[INV-2 fix = `sorted()` by ID, queue key
`(tick, sub_order, actor_id)`]; cost benchmark ~$50/day
for 25 agents at 1 Hz [bg-4 — overlaps
`generative_agents.md` Table 2]);
`docs/ref/letta.md` (353 lines — the block manager context
window partition [`system`/`persona`/`human`/`tools`/
`scratchpad`/`fifo_queue` blocks with per-block token
budget; the context window is a multi-block memory space,
not one prompt string; lifted into `brief/assembler.py`
block layout — brief as typed blocks with per-block
token budgets], the three-tier memory hierarchy
[`core_memory` (in-context block-level state, the "RAM")
+ `recall_memory` (vector store of all prior messages, the
"swap") + `archival_memory` (separate vector store for
long-term notes, the "disk") with explicit paging tools
between tiers — lifted into canon log (immutable stream
analogue of recall but append-only) + per-NPC projection
(working set, analogue of core but derived via `fold`,
not mutated via tools) + brief output cache (analogue of
archival for compaction entries)], the internal tools
[`core_memory_append`/`core_memory_replace`/
`archival_memory_insert`/`archival_memory_search`/
`conversation_search`/`conversation_search_date` — the
LLM self-manages its memory via tool calls; the negative
reference for canonsim: the LLM never mutates the canon,
only the simulator writes canon events, the LLM produces
Intent that the simulator validates], the
`conversation_search` retrieval [embed query + cosine
top-k — same shape as `generative_agents.md` but without
the three-signal weighting (recency+importance+relevance);
letta's is relevance-only, canonsim inherits the richer
three-signal shape], the `conversation_search_date`
[time-range filter on the log — the precedent for our
tick-range retrieval on the integer tick field], the
`core_memory_replace` string-replace on named blocks [the
anti-pattern; INV-5 forbids log edits, corrections are
new events], the `summarize_messages_in_place`
compaction-on-overflow [oldest N messages summarised into
one row via LLM call, originals dropped from queue but
retained in recall — INV-1 forbids truncation; the
canonsim shape is reflection-on-recurrence (from
`generative_agents.md`): compaction = new events on the
log, originals never dropped], the `AgentState` Pydantic
serialisation [state mutated in place by LLM tool calls;
INV-1 (state = fold(log)) is the inverse; our `state` is
a pure projection of the canon log, never a separate
mutable row], the pluggable `LLMClient` abstract base
with per-provider concrete classes [`OpenAILLMClient`/
`AnthropicLLMClient`/`GoogleLLMClient`/`OllamaLLMClient`/
`vLLMClient` — lifted into `brief/llm_client.py`; one
local implementation (llama.cpp/Outlines per
`TECH_NOTES.md` §1), same abstract shape; the OpenAI/
Anthropic/Google/vLLM network dependencies are not
lifted], the `Agent.step()` per-step LLM call with tool-use
loop [the canonical LLM-agent hot loop, same shape as
`ai-town.md` `agentStep` and `generative_agents.md`
`agent_step`; phase 0 forbids the LLM call entirely], the
REST + WebSocket agent-as-a-service [canonical
LLM-agent-as-a-service pattern (same as ai-town);
`MVP_SCOPE.md` §2 non-goals exclude the server /
multi-tenant layer for phase 0], the OS-memory-hierarchy
analogy from paper arXiv:2310.08560 [the design lesson
that shapes the phase-4 brief layer — the brief is a
managed context, not a stuffed prompt], explicitly
positive on block-manager shape + three-tier hierarchy +
pluggable-LLM-client interface + `conversation_search_date`
tick-range retrieval [phase-4 `brief/assembler.py` +
`brief/recall.py` + `brief/llm_client.py` inherit the
shapes] + OS-memory-hierarchy analogy [the design lesson
for the phase-4 brief layer]; explicitly negative on LLM
in hot loop [INV-4] + OpenAI/Anthropic/Google/vLLM
network dependencies [INV-4 stricter — local
llama.cpp/Outlines in phase 1+] + `core_memory_replace`
LLM-mutates-own-memory [INV-5 inverse — corrections are
new events] + `summarize_messages_in_place` drops-originals
[INV-1 inverse — reflection-on-recurrence from
`generative_agents.md` is the canonsim shape] + pgvector
dependency for `recall_memory` [D-012 stdlib-only — stdlib
SQLite + FTS5 per REFERENCES §6 instead] + agent-state
mutated by LLM [INV-1 inverse — state = fold(log), the
LLM never mutates state, the LLM produces Intent that the
simulator validates] + agent-as-a-service REST/WebSocket
[`MVP_SCOPE.md` §2 non-goal — no server in phase 0] +
flat `recall_memory` without per-channel routing [no
`seen`/`told`/`inferred` distinction — KI#3 has no
analogue here either]; cost benchmark ~$720/day at 1 Hz
for gpt-4-class models [bg-4 — overlaps
`generative_agents.md` Table 2 and `ai-town.md`]). All
three paraphrased from the open-source corpus + paper per
§0.4 / §0.7 (D-015). Licenses verified against
`REFERENCES.md` §5 on 2026-08-26: Stanford Generative
Agents = Apache-2.0 (the `joonspk-research/generative_agents`
repo — the paper is the academic companion, not the
license-bearing artefact; the index row previously said
"(paper)" which was misleading, fixed in the same edit
that flipped ref-7-a/b/c todo → done — KI#6-class drift
caught by the standing pre-flip check), ai-town = MIT (the
`a16z/ai-town` repo), letta = Apache-2.0 (the
`letta-ai/letta` repo, formerly `cpacker/MemGPT`, renamed
early 2024 — same license, expanded scope). No license
drift between catalog and index this iteration — KI#6-class
pitfall avoided. §2 of `docs/REFERENCES_DEEP.md` flips
ref-7-a/b/c from todo → done with rich one-line verdicts.
AGENT_NAVIGATION §1 adds the three new files to the
`docs/ref/` list. Per AGENTS §2.5 this is the
**fifteenth** docs iteration in a row (0, 0b, 0c, 0e, 0f,
0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n, 0o, 0p; iter-0d was
infra) — the doc-loop alarm has fired again; the owner
explicitly asked to continue reference work, so the
D-022 exception applies. iter-1 is still the next
functional step; no further docs iterations without a
fresh owner request. KI#3, KI#4, KI#5 unchanged.
AGENTS, ROADMAP, MVP_SCOPE, EVENT_SCHEMA, schemas,
TECH_NOTES, SPECS_BACKLOG, CORE_DESIGN_RESEARCH, VISION,
DECISIONS — untouched.

## Invariants (one line each — full rules in AGENTS.md §4)

- INV-1 Event sourcing: state changes only via events; the JSONL log is the
  append-only truth; SQLite is a rebuildable index.
- INV-2 Determinism: single seeded RNG, no wall-clock, `sorted()` iteration,
  fixed `PYTHONHASHSEED`, queue key `(tick, sub_order, actor_id)`.
- INV-3 Content/code split: no domain words in code; all setting data in
  `content/tavern_pack/`.
- INV-4 LLM boundary: no LLM/network calls in track A before the phase-0 gate.
- INV-5 Log immutability: committed logs are never edited; corrections are new
  events.

## Active KIs

- KI#3 · `expectation_violation` primitive missing — NPC reacts only to presence in `knowledge`, not to absence (purse gone, guard missing). Fix: P2d in `CORE_DESIGN_RESEARCH.md` §6, slated for iter-3.
- KI#4 · balance harness (1000-sim distribution plots of `suspicion` / `fire_spread`) missing — MVP_SCOPE §15 promises an iter-6 baseline but no tool exists. Added as `balance-1` in `docs/TASKS.md` infra backlog.
- KI#5 · runtime state vs test fold not explicitly separated — risk of O(N²) at startup if `fold(log)` is misused as runtime path. D-023 records the rule: runtime = incremental projection; fold = T2 replay only.

## FAQ / Pitfalls

- **Zip upload loses dotfiles and empty dirs.** "Add files via upload" on GitHub
  dropped `.gitignore` (and every dir without tracked files). After any future
  upload: verify `.gitignore` exists and `git status --short` shows no runtime
  artifacts (KI#1).
- **Workspace files ≠ tracked files.** `git status --short` shows changes
  *vs HEAD*, not what is *in HEAD* — a file present in your working directory
  may not be committed at all. After any structural change, run
  `git ls-files <path>` (or `git ls-files | head -50`) to confirm what is
  actually tracked. This is the diagnostic for KI#1-class losses and for
  "the file exists but tests can't find it" surprises.
- **Doc-loop alarm vs owner-requested research.** Fifteen docs iterations in
  a row would normally force a stop (AGENTS §2.5). Owner-requested research
  passes are the explicit exception (D-022). The rule still bites: this is
  the last allowed research-only iteration before iter-1, no further
  exceptions without a fresh owner request. iter-0p is the fifteenth docs
  iteration in a row (0, 0b, 0c, 0e, 0f, 0g, 0h, 0i, 0j, 0k, 0l, 0m, 0n,
  0o, 0p; iter-0d was infra).
- **Substance over line count (D-025) + per-ref split (D-026).** The
  400-line cap was a crutch — iter-0i trimmed real depth (XML element
  lists, event-type enumerations, Mesa pseudo-code, DataCollector
  details) to fit. AGENTS §6 cap is 600, but §6.1 is the real law — filler /
  restatements / linker chains / decorative prose are cut always; named
  systems, real field lists, type enumerations, pseudo-code, per-source
  verdicts are never cut to fit the cap. Over cap after a real cruft pass:
  keep, document in worklog. At iter-0j the single-file
  `docs/REFERENCES_DEEP.md` was 737 lines — 4 deep dives with concrete
  field names and type enumerations justified the breach. At iter-0k the
  same content was split into 5 per-ref files in `docs/ref/` (D-026);
  each is 101–244 lines — under the cap by construction. At iter-0l
  `paradox_scripting.md` is 605 lines — 5 over the cap, justified per
  §6.1 (three games × trigger/MTTH/weight/effect/scope/on_action
  subsystems with real field names and ~150+ on_action IDs). At
  iter-0m three proprietary §10 source files (`rimworld.md` 253,
  `l4d_director.md` 245, `alien_isolation.md` 296) — all under
  cap by construction (the closed-source constraint forces
  field-shape-from-public-talks only, not full enumeration). At
  iter-0n four open-licensed event/narrative grammar family files
  (`wesnoth_wml.md` 244, `endless_sky_dsl.md` 228, `ink.md` 212,
  `tracery.md` 217) — all under cap by construction (the pattern-
  not-content rule §0.7 + the JSON/grammar shape lift keeps each
  file to the mechanics layer only). At iter-0o three open-
  licensed roguelike emergence + micro-sim files
  (`brogue.md` 326, `dcss.md` 360, `keeperrl.md` 444) — all
  under cap by construction (the pattern-not-content rule §0.7
  + the shape-lift keeps each file to the mechanics layer
  only; the larger line counts vs iter-0n reflect the deeper
  RNG/scheduler/queue mechanics these three sources carry —
  the §6.1 substance filter protects the depth). At iter-0p
  three open-licensed LLM-agent precedent files
  (`generative_agents.md` 371, `ai_town.md` 345,
  `letta.md` 353) — all under cap by construction (the
  pattern-not-content rule §0.7 + the shape-lift keeps each
  file to the mechanics layer only; the larger line counts
  vs iter-0n reflect the deeper memory hierarchy + retrieval
  + context-window block manager mechanics these three
  sources carry — the §6.1 substance filter protects the depth).
- **License drift between catalog and index (KI#6, closed iter-0n; pitfall
  persists).** The `REFERENCES_DEEP.md` §2 index table is **not** the source
  of truth for licenses — `REFERENCES.md` (the catalog) is. The index
  restates the license as a one-line convenience column; if the two
  disagree, the catalog wins. iter-0n found two drifts in §2 (ref-5-b
  "CC-BY-SA" vs catalog "GPL-3.0 code; mixed assets"; ref-5-d "CC0"
  vs catalog "Apache-2.0"); both fixed in the same edit. iter-0o
  verified the three new ref-6 rows (AGPL/GPL/GPL shorthand) against
  catalog §2 (AGPL-3.0 (CE) / GPL-2.0+ / GPL-2.0) — no drift this
  iteration. iter-0p caught one drift on ref-7-a (index said
  "(paper)", misleading — the catalog §5 says Apache-2.0 for the
  `joonspk-research/generative_agents` repo; the paper is the academic
  companion, not the license-bearing artefact); fixed in the same §2
  edit that flipped ref-7-a/b/c todo→done with the corrected
  "Apache-2.0 (repo) + paper" annotation. The diagnostic: before
  flipping any ref-N row todo→done, grep the source row in
  `REFERENCES.md` and verify the license column matches the index
  entry. Same pattern as the catalog ↔ synthesis ↔ deep-dive
  anti-drift rule (D-024/D-026): a fact restated in two places
  drifts; the catalog is the owner. Standing pre-flip check added
  to the iter-0o workflow, exercised again in iter-0p.
- **Catalog vs deep dives vs synthesis — three places, three jobs.**
  `docs/REFERENCES.md` is the **catalog** (license, URL, phase gating,
  intake rules). `docs/CORE_DESIGN_RESEARCH.md` §2 is the **synthesis**
  (one-line depth primitive + failure mode per source). Per-source
  **deep dives** live in `docs/ref/<source>.md` (one file per source,
  indexed by `docs/REFERENCES_DEEP.md` §2 — D-026; the single-file
  arrangement from D-024 did not scale). Drift rule (AGENTS §3): never
  restate across these three — link only. A future reference detail
  belongs in a per-ref file under `docs/ref/`, not in the catalog or the
  synthesis table.

## Next step

iter-1 · core plumbing is the next functional step: seed, RNG instance, clock,
event queue, JSONL log with header, playscript runner, pack loader for the
drafted `content/tavern_pack/` v0.1. Acceptance criteria in `docs/TASKS.md`.
Owner's blocking answers to Q1–Q3 are absorbed as D-019..D-021 and flip
P2a/P2b and M3/M4/M5 from proposals to accepted iter-3/iter-4/iter-6 scope.
The ref-6 deep dives (Brogue two-stream RNG, DCSS multi-stream RNG +
energy-based scheduler, KeeperRL continuous-time queue + Collective tick
order) are the direct precedents for iter-1 core plumbing. The ref-7 deep
dives (Generative Agents memory stream + retrieval function + reflection
pattern, ai-town reactive-database anti-pattern, letta block-manager +
three-tier memory hierarchy) are the precedents for the phase-1+ brief
layer (track B only, behind the phase-0 gate).
