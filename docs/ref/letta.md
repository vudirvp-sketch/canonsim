# letta (ex-MemGPT) · `REFERENCES.md` §5 + §14 · Apache-2.0 · bg-4 (cost notes) / phase 4 (memory patterns)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Catalog row (`REFERENCES.md` §5):
> `letta (ex-MemGPT) | Apache-2.0 | long-term-memory patterns (phase 4
> design notes)`. Code is in scope per §0.4; we lift patterns (block
> manager context window management, recall + archival memory
> hierarchy, the tool-calling protocol) into our `brief/` phase-1+
> design notes, never the Python syntax. Reference repo:
> `letta-ai/letta` (renamed from `cpacker/MemGPT` in early 2024 —
> same project, same Apache-2.0 license, expanded scope from research
> prototype to product). Paper: Packer et al., "MemGPT: Towards LLMs
> as Operating Systems", arXiv:2310.08560. Corpus inspected: the
> paper, `letta/` Python package (server + SDK), `letta/schemas/`
> (Pydantic data contracts), `letta/services/` (per-provider LLM
> clients, embedding, summarisation), `letta/agent.py` and
> `letta/memory.py` (the core loop and the block manager). Catalog-row
> license match check (standing pre-flip per STATUS FAQ): index row
> ref-7-c lists Apache-2.0 — matches catalog §5. No drift this
> iteration.

**What it is.** letta (the package and the company; the repo
was MemGPT until early 2024) is an open-source memory
architecture for LLM agents, framed as "LLMs as Operating
Systems". The central insight: a fixed-context-window LLM has
the same problem as a fixed-RAM computer — there is more
relevant data than fits in the working set, and the system
needs an OS-style memory hierarchy (working memory + secondary
storage + a paging mechanism) to swap pages in and out on
demand. The repo implements this hierarchy as: (1) a block
manager that partitions the context window into named blocks
(system / persona / human / tool / scratchpad / FIFO queue);
(2) a recall memory (a vector store of all prior messages);
(3) an archival memory (a vector store of long-term notes the
agent chose to save); (4) a set of internal tools the LLM can
call to page memory in / out (`core_memory_append`,
`core_memory_replace`, `archival_memory_insert`,
`conversation_search`, `conversation_search_date`,
`archival_memory_search`). The canonsim relevance is
**phase-4 brief memory patterns** and **bg-4 cost notes** —
the architecture is the most explicit public reference for
"context window as a managed resource" and the closest
existing system to our `brief/recall.py` + `brief/synthesise.py`
design.

**Concrete mechanics.**

- **Block manager — partition the context window into named
  blocks.** The agent's system prompt is not one string; it is
  a sequence of typed blocks: `system` (the OS-style instructions
  / tool descriptions), `persona` (the agent's identity — same
  shape as Generative Agents' `persona.json` lifted in
  `generative_agents.md`), `human` (the user's identity for
  this conversation), `tools` (the function-calling interface
  descriptions), `scratchpad` (a small writable block the
  LLM uses for transient notes), and a `fifo_queue` (a sliding
  window of the last N messages, with older messages evicted
  on overflow). Each block has a `limit` (maximum token count);
  the block manager enforces the limit by truncation. The
  pattern: **the context window is a multi-block memory space,
  each block has a role and a limit**. For canonsim phase-4
  this is the precedent for our `brief/assembler.py` block
  layout — the brief is not one prompt string but a sequence
  of typed blocks (canon facts + retrieved memories + active
  intents + template), each with a token budget.
- **Memory hierarchy — `core_memory` + `recall_memory` +
  `archival_memory`.** Three layers: (a) **`core_memory`** is
  the in-context-window block-level state — small, mutable
  via tool calls (`core_memory_append` / `core_memory_replace`),
  the "RAM" of the OS analogy; (b) **`recall_memory`** is a
  vector store (default: pgvector, but pluggable) of all prior
  messages — the "swap" of the OS analogy; (c) **`archival_memory`**
  is a separate vector store for long-term notes the agent
  chose to persist (`archival_memory_insert` tool call) — the
  "disk" of the OS analogy. The pattern: **three-tier memory
  hierarchy with explicit paging tools**. For canonsim phase-4
  this is the precedent for our three-tier brief architecture:
  canon log (the immutable stream — analogue of `recall_memory`
  but append-only) + per-NPC projection (the working set —
  analogue of `core_memory` but derived from the log via
  `fold`, not mutated via tool calls) + brief output cache
  (analogue of `archival_memory` for compaction entries).
- **Internal tools — `core_memory_append`, `core_memory_replace`,
  `archival_memory_insert`, `archival_memory_search`,
  `conversation_search`, `conversation_search_date`.** The LLM
  can call these tools to modify its own memory — append a
  fact, replace a fact, search the recall store, etc. The tool
  results are returned as messages; the LLM then produces the
  next message. The pattern: **the LLM self-manages its memory
  via tool calls**. For canonsim this is the **negative**
  reference for the brief layer — we do not let the LLM
  modify the canon log (INV-1 forbids — only the simulator
  writes canon events); the LLM produces Intent that the
  simulator validates and possibly rejects. The split: the
  LLM is a stateless caller over a deterministic memory; the
  memory is mutated only by the simulator.
- **`conversation_search` — vector retrieval over prior
  messages with `text` and optional `count` (top-k).** The
  tool takes a text query, embeds it with the agent's
  configured embedder (default OpenAI / Anthropic embeddings;
  pluggable), queries the recall store with cosine similarity,
  returns the top-k message rows. The pattern: **retrieval
  = embed query + cosine top-k**. This is the same shape as
  `generative_agents.md` retrieval, but without the
  three-signal weighting (recency + importance + relevance) —
  letta's `conversation_search` is relevance-only. For canonsim
  phase-4 `brief/recall.py` inherits the three-signal shape from
  `generative_agents.md` (richer); letta's `conversation_search`
  is the simpler shape, useful as the comparison.
- **`conversation_search_date` — date-range filter over
  prior messages.** The tool takes a `start_date` and optional
  `end_date` and returns all messages in the range (no
  embedding). The pattern: **temporal retrieval = date-range
  filter on the log**. For canonsim phase-4 this is the
  precedent for our tick-range retrieval — the canon log has
  a tick integer per event, so retrieval by tick range is the
  same shape, just on an integer field instead of a date.
- **`core_memory_replace` — string-replace within a block.**
  The LLM provides an `old_str` and `new_str`; the block
  manager finds `old_str` in the named block and replaces it.
  If `old_str` is not unique or not found, the tool returns an
  error. The pattern: **memory mutation = string-replace on
  named blocks**. For canonsim this is the **negative**
  reference — INV-5 forbids editing committed logs; corrections
  are new events. The `core_memory_replace` is the
  anti-pattern; the canonsim correction shape is `core_event_append`
  only.
- **`summarize_messages_in_place` — message compaction.** When
  the `fifo_queue` overflows, letta runs a `summarize_messages_in_place`
  step: the oldest N messages are summarised into one
  summarised message via an LLM call, the originals are dropped
  from the queue (still in `recall_memory`). The pattern:
  **compaction by summarisation on overflow**. For canonsim
  phase-4 this is the precedent for `brief/synthesise.py` — but
  INV-1 forbids dropping originals; the canonsim shape is
  reflection-on-recurrence (from `generative_agents.md`):
  compaction = new events on the log, originals never dropped.
- **State serialisation — `AgentState` Pydantic model with
  `state` dict containing `persona`, `human`, `system`,
  `tools`, `memory` blocks.** Each agent has an `AgentState`
  row in the SQLite metadata database; the state is
  serialised as JSON. The pattern: **agent state = Pydantic
  model + JSON serialised to a database row**. For canonsim
  this is the **negative** reference — the state is mutated
  in place by the LLM's tool calls; the only "log" is the
  message history (which is the per-agent recall store, not
  a global event log). INV-1 (state = fold(log)) is the
  inverse; our `state` is a pure projection of the canon
  log, never a separate mutable row.
- **LLM clients — `OpenAILLMClient` / `AnthropicLLMClient` /
  `GoogleLLMClient` / `OllamaLLMClient` / `vLLMClient`.** The
  `letta/services/llm/` directory has one Python class per
  provider; each implements the same `LLMClient` abstract
  base with `chat_completion` and `embedding` methods. The
  pattern: **pluggable LLM client with provider-agnostic
  interface**. For canonsim phase-1+ this is the precedent for
  our `brief/llm_client.py` — one abstract interface, one
  local implementation (llama.cpp / Outlines per
  `TECH_NOTES.md` §1). The provider set is smaller (we use
  local only; no OpenAI / Anthropic / Google / vLLM); the
  shape is the same.
- **`Agent` step loop — `step()` method that builds the
  prompt from the block manager, sends to the LLM, parses
  the response (text or tool call), executes the tool (memory
  mutation / retrieval), and returns.** The loop runs once
  per `step()` call (no internal tick); the caller (a CLI, a
  REST API, a cron) drives the cadence. The pattern: **per-step
  LLM call with tool-use loop**. For canonsim this is the same
  shape as `ai-town.md` `agentStep` and `generative_agents.md`
  `agent_step` — the canonical LLM-agent hot loop. Our
  phase-1+ brief step inherits the shape; phase 0 forbids
  the LLM call entirely.
- **REST API + WebSocket — `letta.server` exposes the agent
  as a service.** The agent runs server-side; clients send
  messages via REST or WebSocket; the agent replies. The
  pattern: **agent-as-a-service**. For canonsim this is the
  canonical LLM-agent-as-a-service pattern (same as ai-town);
  we explicitly reject this for phase 0 (no server; the
  simulator is a CLI tool).

**What we take.**

- **The block-manager context-window partition shape.**
  Phase-4 `brief/assembler.py` inherits this — the brief is
  not one prompt string but a sequence of typed blocks
  (canon facts + retrieved memories + active intents +
  template), each with a token budget. Same shape, different
  block names.
- **The memory-hierarchy three-tier shape — core / recall /
  archival.** Phase-4 inherits this — canon log (immutable
  stream, analogue of recall but append-only) + per-NPC
  projection (working set, analogue of core but derived via
  `fold`, not mutated via tools) + brief output cache (analogue
  of archival for compaction entries).
- **The pluggable-LLM-client abstract interface.** Phase-1+
  `brief/llm_client.py` inherits this; one local implementation
  (llama.cpp / Outlines), same `chat_completion` and `embedding`
  methods.
- **The `conversation_search_date` shape — temporal retrieval
  by date-range filter.** Phase-4 `brief/recall.py` inherits
  this shape on the tick integer field instead of a date.

**What we adapt.**

- **`core_memory_replace` (string-replace on blocks) → no
  log edits (INV-5).** letta allows the LLM to mutate its
  own memory in place; our design forbids this — corrections
  are new events, the log is append-only. The split: letta
  is a stateful agent with mutable memory; canonsim is a
  stateless caller over an immutable log.
- **`summarize_messages_in_place` (drop originals on
  overflow) → reflection on recurrence (INV-1).** letta drops
  the original messages from the queue; canonsim keeps the
  originals and adds a compaction entry as a new event.
  Reflection-on-recurrence (from `generative_agents.md`)
  is INV-1-compatible; summarise-in-place is not.
- **The LLM self-manages memory via tool calls → the LLM
  produces Intent that the simulator validates.** letta's
  LLM can call `core_memory_append` directly; canonsim's LLM
  produces an Intent that the simulator validates and possibly
  rejects. The LLM never mutates the canon; the simulator is
  the only writer.
- **The pgvector recall store → the JSONL log + SQLite index.**
  letta's `recall_memory` is a vector store of message rows;
  our canon log is the JSONL stream of events, with the SQLite
  index as the rebuildable projection. Same "the memory is
  the log" shape; different storage substrate (we use stdlib
  SQLite + FTS5 per REFERENCES §6; letta uses pgvector, an
  external dependency that violates our stdlib-only D-012).
- **The OpenAI / Anthropic / Google / vLLM network
  dependencies → local llama.cpp / Outlines only.** INV-4
  stricter — no network in track A; phase-1+ uses local
  inference only (REFERENCES §5).

**What inspires us.** The **"context window as a managed
resource, not an infinite buffer"** lesson. letta is the
most explicit public reference for the OS-memory-hierarchy
analogy applied to LLM context — block manager = RAM
partitioning, recall = swap, archival = disk, paging tools
= syscall interface. The lesson for canonsim: the brief
assembler is not "stuff everything into the prompt and hope
it fits" — it is a block-layout problem with per-block
budgets, where the LLM is the last consumer of a managed
context. The canon log + per-NPC projection + brief cache
is the canonsim version of the same hierarchy, with one
key difference: the canon log is immutable and append-only
(INV-1 + INV-5), so the LLM cannot mutate the underlying
state — only the simulator writes canon events, and the
LLM's Intent is a proposal that the simulator validates.

**Strengths.**

- Public Apache-2.0 — the entire Python codebase is readable;
  the repo is ~25k lines of Python and is the cleanest public
  reference for the OS-style memory hierarchy. Pattern-lifting
  is permitted per `REFERENCES.md` §0.4.
- The block-manager shape is the cleanest public reference
  for "the context window is a multi-block memory space" —
  our `brief/assembler.py` inherits the layout shape.
- The three-tier memory hierarchy (core / recall / archival)
  is the explicit OS-memory analogy; our canon log + projection
  + brief cache is the canonsim version.
- The pluggable-LLM-client abstract interface is small and
  explicit — the `LLMClient` abstract base + per-provider
  concrete classes is the right shape for `brief/llm_client.py`.
- The `conversation_search_date` shape is the precedent
  for tick-range retrieval on the canon log.
- The paper (arXiv:2310.08560) is the only public reference
  for the OS-memory-hierarchy analogy applied to LLM context,
  with evaluation results in §6 — useful as the bg-4 cost /
  quality benchmark for the brief layer.

**Weaknesses.**

- The LLM is in the hot loop — every agent step is one or
  more LLM API calls (the tool-use loop can produce several
  tool calls per step). This is the canonical INV-4 violation;
  phase 0 forbids the entire design.
- The OpenAI / Anthropic / Google / vLLM network dependencies
  are pluggable but default to OpenAI — the repo will not
  run without an API key by default. INV-4 stricter — no
  network in track A; phase-1+ uses local llama.cpp / Outlines.
- The `core_memory_replace` tool allows the LLM to mutate its
  own memory in place — INV-5 forbids log edits; the canonsim
  correction shape is `core_event_append` only.
- The `summarize_messages_in_place` tool drops original
  messages from the queue on overflow — INV-1 forbids
  truncation; the canonsim shape is reflection-on-recurrence
  (compaction = new events, originals never dropped).
- The pgvector dependency for `recall_memory` is an
  external Postgres extension — violates D-012 (stdlib-only);
  we use stdlib SQLite + FTS5 per REFERENCES §6 instead.
- The state is mutated by the LLM via tool calls — INV-1 is
  the inverse (state = fold(log); the LLM never mutates state;
  the LLM produces Intent that the simulator validates).
- No knowledge records with per-channel routing — the
  `recall_memory` is a flat vector store of messages with
  no `seen` / `told` / `inferred` distinction. Same
  weakness as `generative_agents.md` and `ai-town.md`; the
  KI#3 expectation_violation fix has no analogue here.
- The agent-as-a-service REST + WebSocket shape is the
  canonical LLM-agent-as-a-service pattern (same as
  ai-town) — `MVP_SCOPE.md` §2 non-goals explicitly exclude
  the server / multi-tenant layer for phase 0.
- The cost-per-step is 1 LLM call × ~2k tokens × N tool-use
  iterations per step — at $0.01 / 1k tokens (gpt-4 class
  models) this is ~$0.02 per step, ~$720/day at 1 Hz. This
  is the bg-4 cost benchmark; canonsim's design goal is to
  push the LLM out of the hot loop (only on brief / chronicle
  events) and reduce the cost by orders of magnitude.

**Verdict.** Phase-4 memory-pattern reference, mostly
positive on the **block-manager context-window partition shape**
(lifted into `brief/assembler.py` — brief as typed blocks with
per-block token budgets, not one prompt string), the **three-tier
memory hierarchy** (lifted into canon log + per-NPC projection
+ brief cache — same hierarchy shape, different storage substrate),
the **pluggable-LLM-client abstract interface** (lifted into
`brief/llm_client.py` — local llama.cpp / Outlines only, same
abstract shape), and the **`conversation_search_date` shape**
(lifted into `brief/recall.py` tick-range retrieval on the
integer tick field). Explicitly negative on the **LLM in the
hot loop** (INV-4 forbids in track A; the LLM moves to the
phase-1+ `brief/` layer behind the phase-0 gate), the
**OpenAI / Anthropic / Google / vLLM network dependencies**
(INV-4 stricter — no network in track A; local llama.cpp /
Outlines in phase 1+), the **`core_memory_replace` LLM-mutates-
its-own-memory pattern** (INV-5 forbids log edits; corrections
are new events), the **`summarize_messages_in_place` drops-
originals-on-overflow pattern** (INV-1 forbids truncation;
reflection-on-recurrence is the canonsim shape), the
**pgvector dependency** (D-012 stdlib-only — we use stdlib
SQLite + FTS5), the **agent-as-a-service REST + WebSocket
shape** (`MVP_SCOPE.md` §2 non-goals exclude server /
multi-tenant for phase 0), and the **flat `recall_memory`
without per-channel routing** (our `knowledge` records
carry `seen` / `told` / `inferred` — KI#3 expectation_violation
fix has no analogue here). The OS-memory-hierarchy analogy
from the paper (arXiv:2310.08560 §1) is the design lesson
that shapes the phase-4 brief layer — the brief is a managed
context, not a stuffed prompt. The cost benchmark
(~$720/day at 1 Hz for gpt-4-class models) overlaps bg-4 with
`generative_agents.md` Table 2 and `ai-town.md`; canonsim's
design goal is to push the LLM out of the hot loop and reduce
the cost by orders of magnitude.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
