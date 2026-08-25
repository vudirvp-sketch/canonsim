# ai-town · `REFERENCES.md` §5 + §9 · MIT · bg-4 (cost notes) / negative reference

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Catalog row (`REFERENCES.md` §5):
> `ai-town | MIT | negative reference: runtime LLM agents
> (\`ROADMAP §4\`)`. Code is in scope per §0.4; we lift the shape
> (Convex backend integration, agent loop structure, the "world
> state on the server" pattern) into our phase-1+ design notes,
> never the TypeScript / React syntax. Reference repo:
> `a16z/ai-town` (the original) — the `a16z-infra/ai-town`
> organisation is the same project under the org move. Corpus
> inspected: `convex/` (server functions: `engine.ts`,
> `agents.ts`, `index.ts`, `world.ts`, `tables.ts`), `src/`
> (React + pixi.js frontend), `prompts/` (LLM prompt templates
> as `.txt`), `package.json`. Catalog-row license match check
> (standing pre-flip per STATUS FAQ): index row ref-7-b lists
> MIT — matches catalog §5. No drift this iteration.

**What it is.** ai-town is a public multi-agent LLM sandbox
built by a16z in mid-2023 as a port of the Stanford Generative
Agents design (`generative_agents.md`) onto a different stack:
TypeScript instead of Python, Convex (a hosted reactive
database) instead of local SQLite, pixi.js for a tile-based
world view, and OpenAI / Anthropic / OpenRouter for the LLM
backend. The repo is small (~2500 lines TypeScript total) and
well-organised; it was the first widely-cited reference for
"LLM agents in a tile world with a reactive database" — and
the first widely-cited **negative** reference for the cost /
determinism problem. The catalogue marks it `negative reference:
runtime LLM agents` per `ROADMAP §4`; the canonsim relevance
is **phase 1+ brief layer design notes** and **bg-4 cost
benchmark only** — phase 0 explicitly rejects the entire
design.

**Concrete mechanics.**

- **Convex backend — server-side reactive database.** The
  entire world state lives in Convex tables (`world`, `players`,
  `agents`, `messages`, `conversations`, `archives`). Each
  table is a typed reactive collection; mutations are
  transactions. The pattern: **world state is a database; the
  simulation is a server-side mutation loop; the frontend is
  a reactive view**. This is the inverse of our INV-1 —
  Convex tables are mutable; the only log is the Convex
  internal history (which we cannot export deterministically).
  Our design rejects this shape: the JSONL log is the only
  truth, the SQLite index is rebuildable, the LLM never sees
  the database directly.
- **`engine.ts` — the simulation loop.** The engine runs as
  a single Convex transaction per tick. Each tick: (a) load
  all agents from the `agents` table; (b) for each agent in
  sorted order (insertion order, not sorted by ID — a
  determinism hazard we would fix); (c) call `agentStep`
  which runs the LLM and writes a new `messages` row; (d)
  if the agent moved, update the `players` table; (e) if
  the agent entered a conversation, write a `conversations`
  row. The tick rate is configurable (default 1 Hz); the
  engine runs as a Convex cron job. The pattern: **tick loop
  = load agents, per-agent LLM call, write back state**.
  For canonsim this is the negative reference for the
  "per-tick LLM call" anti-pattern (INV-4 + INV-2
  forbids); our phase-1+ design has the LLM call only in
  track B, behind the phase-0 gate, and the per-tick loop
  is deterministic.
- **`agentStep` — the per-tick LLM call.** The `agents.ts`
  file exports the `agentStep` mutation; it builds a prompt
  from: (a) the agent's identity description (`name`, `description`,
  `identity`); (b) the last 10 `messages` rows from any
  agent in the same conversation; (c) the agent's inventory
  (`Inventory` type with `stacks: Stack[]`); (d) the visible
  tiles around the agent (the `world` table's `currentView`
  field); (e) the agent's last action. The prompt is sent
  to the LLM; the LLM output is parsed into an `Action`:
  `MoveAction { direction }` or `SayAction { content }`
  or `WaitAction {}`. The pattern: **per-tick LLM call with
  recent-history context**. This is the canonical hot-loop
  LLM call; the cost-per-tick is N agents × 1 LLM call
  × ~500 tokens per call. Our `brief/` layer (phase 1+)
  inherits the prompt-template shape and the
  action-grammar shape; the per-tick LLM call is the
  INV-4 violation we explicitly reject.
- **Action grammar — `MoveAction` / `SayAction` /
  `WaitAction` discriminated union.** The LLM output is
  parsed into one of these three actions; the parser is
  a small `zod` schema validation. The pattern: **LLM
  output → discriminated-union Intent**. Our Intent
  schema (`SPECS_BACKLOG.md` INTENT_SCHEMA sketch,
  `templates.json` `action_type` enum) inherits this
  shape — discriminated-union with type tag + per-type
  fields. Same shape, different schema language (JSON
  Schema spec, not zod; per REFERENCES §5).
- **Conversation handshake — `startConversation` +
  `walkAway` + `leaveConversation`.** When two agents
  collide on the tile grid, the `world.ts` mutation
  `startConversation` creates a `conversations` row with
  both agent IDs and a unique conversation ID. Each
  subsequent turn of each agent checks if it is in a
  conversation; if so, the prompt template includes the
  recent `messages` from the other agent. The conversation
  ends when an agent produces a `LeaveAction` (or moves
  away). The pattern: **conversation = shared mutable
  row + per-turn LLM call per agent**. This is the
  `generative_agents.md` conversation model with a
  database row instead of an in-memory scratchpad —
  structurally identical. Our phase-1+ `talk` action
  inherits the shared-row shape; the LLM-as-participant
  model does not.
- **`archives` table — periodic memory compaction.** Every
  N ticks per agent, the engine writes a summary of the
  last N `messages` rows to the `archives` table as a
  single row with `description` + `agentId` + `createdAt`.
  The recent-messages context for the prompt then pulls
  from `archives` (compacted) + the most recent `messages`
  (raw). The pattern: **compaction by summarisation, raw
  messages retained as fallback**. This is the Generative
  Agents reflection pattern (`generative_agents.md`) with
  a database table instead of a memory stream. Our
  phase-4 `brief/synthesise.py` inherits the shape —
  compaction = new events on the log (INV-1 compatible,
  not separate archive table).
- **`world.ts` — the tile grid.** The world is a 2D
  integer grid stored as a string in the `world` table's
  `currentView` field (one character per tile, the tile
  charset is a separate `tileset.json` asset). Mutations
  like `movePlayer` and `startConversation` operate on
  the grid by index. The pattern: **grid = string; tile =
  character**. This is the simplest possible spatial
  model — a tile grid as a string, same as the
  Generative Agents `maze` module. Our phase-0 tavern is
  the same shape (a single-tavern tile space) — we
  inherit the grid-as-data model; we do not inherit the
  Convex-side mutation pattern.
- **`prompts/` directory — LLM prompt templates as `.txt`
  files.** Each template is a plain text file with
  placeholder tokens like `{agentDescription}`, `{recentMessages}`,
  `{worldView}`. The `agentStep` mutation loads the
  template, replaces the placeholders, and sends the
  result to the LLM. The pattern: **prompts = static text
  files; runtime = string replace**. This is the same
  shape as our `templates.json` (tracery grammar lifted
  in `tracery.md`) — templates as data, runtime as a
  pure function (grammar, RNG state) → string. The
  placeholder-replace pattern is the simplest possible
  template engine; our `render/` layer inherits the shape
  (chronicle template as JSON, runtime as pure function
  from (template, state) → string).
- **Pixi.js frontend — reactive view of the Convex
  tables.** The React frontend subscribes to the Convex
  `world` and `players` tables; on each Convex
  mutation, the frontend re-renders the tile grid and
  the conversation log. The pattern: **frontend = reactive
  view; the simulation runs server-side**. For canonsim
  this is the inverse of our architecture — we have no
  frontend in phase 0 (`MVP_SCOPE.md` §2 non-goals: no
  UI); the chronicle is a CLI-rendered template
  (`MVP_SCOPE.md` §15). The "server-side sim, reactive
  frontend" split is the canonical LLM-agent-as-a-service
  pattern; we explicitly reject it for phase 0 (no UI,
  no server, no reactive frontend).
- **Authentication — GitHub OAuth via Convex Auth.** The
  repo uses Convex Auth (GitHub OAuth provider) for user
  authentication; each user can "become" an agent in the
  world. The pattern: **multi-tenant LLM-agent sandbox**.
  For canonsim this is irrelevant — single-user CLI in
  phase 0; multi-tenant is a phase-7+ concern if ever.
- **Memory schema — `memories` table with `agentId`,
  `description`, `createdAt`, `importance` (1-10).** The
  repo's `tables.ts` declares `memories` as a Convex table;
  the engine writes a new `memories` row every time an
  agent perceives something or generates a thought. The
  retrieval function (used in the prompt template) is
  `q.recencyScore + q.importanceScore + q.relevanceScore`
  — same three-signal shape as `generative_agents.md`,
  just expressed as a Convex query. The pattern: **per-agent
  memory table + three-signal retrieval**. This is the
  `generative_agents.md` memory stream, ported to a
  reactive database. Our per-NPC knowledge records
  inherit the shape; the per-agent database table does
  not.

**What we take.**

- **The action-grammar shape — discriminated-union Intent
  with `type` tag + per-type fields.** Phase-1+ Intent
  schema inherits this; `templates.json` `action_type`
  enum lifts the same closed list.
- **The prompt-template shape — static text files with
  placeholder tokens, runtime = string replace.**
  Phase-5 `render/` inherits this shape; our `templates.json`
  is the JSON analogue (tracery grammar lifted in
  `tracery.md`).
- **The conversation-as-shared-row shape — a per-conversation
  row with both agent IDs and a list of message rows.**
  Phase-1+ `talk` action brief inherits the shape; the
  LLM-as-participant model does not.
- **The `memories` table schema with `agentId` + `description`
  + `createdAt` + `importance`.** Phase-4 `brief/recall.py`
  inherits the field shape; we use the global JSONL log as
  the source of truth, not a per-agent table.

**What we adapt.**

- **Convex backend → JSONL log + SQLite index.** The
  Convex reactive database is replaced by the INV-1
  JSONL log + SQLite index. Same "world state lives
  somewhere queryable" pattern, different storage
  shape (append-only log + rebuildable index vs reactive
  mutable tables).
- **Per-tick LLM call → no LLM in phase 0, optional LLM
  in phase-1+ track B.** The INV-4 boundary is the inverse
  of ai-town's design — the LLM is in the `brief/` layer
  only, behind the phase-0 gate, and only in track B.
- **`agentStep` server-side mutation → per-tick
  deterministic simulator step.** The agent-step LLM call
  is replaced by the deterministic `MVP_SCOPE.md` §5
  per-tick update order (creatures → levels → collectives
  → territory → external, lifted from `keeperrl.md`).
- **The `agentStep`'s insertion-order iteration → our
  `sorted()` iteration (INV-2).** ai-town iterates agents
  in insertion order — a determinism hazard (the order
  depends on the Convex table's internal row order, which
  is mutable). Our INV-2 fixes this: iteration only via
  `sorted()` by ID, queue key `(tick, sub_order, actor_id)`.

**What inspires us.** The **"reactive database is the wrong
substrate for a deterministic simulation"** lesson. ai-town is
the cleanest public reference for what an LLM-agent sandbox
looks like when the database is reactive and the LLM is in the
hot loop — and it is the cleanest public reference for why
this design is structurally incompatible with determinism
(the Convex mutation order is non-deterministic across
agents; the LLM output is non-deterministic across runs).
The lesson for canonsim: the JSONL log + SQLite index is
the right substrate for a deterministic simulation, the
reactive database is the wrong substrate; the LLM in the
hot loop is the wrong place for the LLM, the LLM in the
brief layer is the right place. The cost benchmark (ai-town
~$50 OpenAI credit per day for ~25 agents at the repo's
default tick rate) overlaps bg-4 (`docs/TASKS.md`) with
`generative_agents.md` Table 2.

**Strengths.**

- Public MIT — the entire TypeScript codebase is readable;
  the repo is small enough to read in one evening and
  structured cleanly (`convex/` for server, `src/` for
  frontend, `prompts/` for templates). Pattern-lifting is
  permitted per `REFERENCES.md` §0.4.
- The prompt-template-as-text-file pattern is the
  cleanest public reference for "prompts as data" —
  our `templates.json` is the JSON analogue; the
  per-template `.txt` file pattern is the precedent.
- The action-grammar discriminated-union is small and
  explicit (3 actions: Move, Say, Wait); our
  `templates.json` `action_type` enum inherits the
  closed-list shape, expanded to ~12 actions
  (`MVP_SCOPE.md` §7).
- The `memories` table schema with `agentId` +
  `description` + `createdAt` + `importance` is the
  explicit public version of the Generative Agents
  memory stream — same shape, just on a reactive
  database. Our per-NPC knowledge records inherit the
  field shape.
- The repo is the canonical reference for "what an
  LLM-agent sandbox looks like" — useful as the
  negative pole in the design space; we explicitly
  reject the substrate (Convex) and the LLM-in-hot-loop
  pattern, but the architecture pattern (memory + retrieval
  + LLM + parse + action) is the same canonical shape
  every LLM-agent framework inherits.

**Weaknesses.**

- The Convex reactive database is the wrong substrate for
  a deterministic simulation — table mutation order is
  non-deterministic, the LLM output is non-deterministic,
  and the only "log" is the Convex internal history
  (which is not byte-identical replayable). INV-1 + INV-2
  both forbid this shape.
- The LLM is in the hot loop — every agent, every tick,
  is one or more LLM API calls. This is the canonical
  INV-4 violation; phase 0 forbids the entire design.
- The OpenAI / Anthropic / OpenRouter network dependency
  is hardcoded — the repo will not run without an API
  key. INV-4 stricter: no network in track A; phase-1+
  uses local llama.cpp / Outlines (no network).
- The frontend is reactive and depends on Convex
  reactivity; the backend is a server-side transaction
  loop. For canonsim phase 0, the non-goals (`MVP_SCOPE.md`
  §2) explicitly exclude UI/frontend integration —
  the entire frontend layer of ai-town is the wrong
  shape for our phase 0.
- The cost-per-tick is N agents × 1 LLM call × ~500
  tokens — at $0.002 / 1k tokens (gpt-3.5-turbo at 2023
  prices) this is ~$0.001 per agent per tick, ~$1 per
  tick for 25 agents, ~$50/day at 1 Hz. This is the
  bg-4 cost benchmark; canonsim's design goal is to
  push the LLM out of the hot loop (only on brief /
  chronicle events) and reduce the cost by orders of
  magnitude.
- The repo's iteration order over agents is insertion
  order (Convex `q.order("desc")` on `createdAt`), not
  sorted by ID. This is a determinism hazard; the
  canonical fix is `sorted()` by ID (INV-2).
- No knowledge records with per-channel routing — the
  `memories` table is a flat list with no `seen` / `told`
  / `inferred` distinction. Same weakness as
  `generative_agents.md`; the KI#3 expectation_violation
  fix has no analogue here.

**Verdict.** Negative reference for phase 0, design-notes
source for phase 1+. Almost entirely negative on the
**Convex reactive database** (INV-1 + INV-2 forbid; the
JSONL log + SQLite index is the inverse substrate), the
**LLM in the hot loop** (INV-4 forbids in track A; the LLM
moves to the phase-1+ `brief/` layer behind the phase-0
gate), the **OpenAI / Anthropic / OpenRouter network
dependency** (INV-4 stricter — no network in track A;
local llama.cpp / Outlines in phase 1+), and the
**reactive frontend** (the `MVP_SCOPE.md` §2 non-goals
explicitly exclude UI/frontend integration for phase 0).
Positive on the **action-grammar discriminated-union**
(lifted into `templates.json` `action_type` enum), the
**prompt-template-as-text-file pattern** (lifted into
`templates.json` shape), the **conversation-as-shared-row
shape** (phase-1+ `talk` action brief inherits), and the
**`memories` table schema** (lifted into our per-NPC
knowledge records field shape, but on a JSONL log not a
reactive database). Cost benchmark (~$50/day for 25 agents
at 1 Hz) overlaps bg-4 with `generative_agents.md` Table 2.
ai-town is the canonical proof that "LLM agents in a tile
world with a reactive database" is architecturally simple
and operationally expensive — the canonsim split (deterministic
simulator produces canon, LLM produces prose behind the
phase-0 gate) is the cost-engineering response; the JSONL
log + SQLite index substrate is the determinism-engineering
response.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
