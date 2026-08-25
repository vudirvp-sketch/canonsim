# Mesa · `REFERENCES.md` §2 · Apache-2.0 · phase 0 (architectural pattern)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift (D-026):
> catalog/license/URL/phase gating in `docs/REFERENCES.md`; one-line
> synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics
> here. License filter and "patterns not content" rule: `REFERENCES.md`
> §0.7 (D-015).

**What it is.** Python agent-based modelling framework
(`projectmesa/mesa`, Apache-2.0) — the reference implementation of the
Model / Scheduler / Agent / DataCollector pattern, and the closest
language match to our stdlib-only core.

**Concrete mechanics.**

- `Model` class — holds `self.schedule`, `self.random` (a single
  `random.Random(seed)` instance — same discipline as our INV-2),
  `self.running` flag, `self.current_id` counter for gap-free agent ids,
  and a `DataCollector`. Subclasses implement `step(self)`.
- `Agent` base — `unique_id`, `model` backreference, `pos` (optional,
  for spatial models), `step(self)` (the agent's per-tick action).
- `Scheduler` subclasses are pure **ordering policies**:
  - `SimpleActivation` — insertion order.
  - `RandomActivation` — shuffled by `model.random` each tick.
  - `SimultaneousActivation` — two-phase: all agents `step()` into a
    staging buffer, then all commits.
  - `StagedActivation` — per-tick stage list (`["talk", "move", "eat"]`),
    all agents run stage 1, then all stage 2.
- `DataCollector` — `agent_reporters` and `model_reporters` dicts of
  `name → callable(agent|model)`; `collect(model)` runs every step and
  stores per-step frames; `get_model_vars_dataframe()` / `get_agent_vars_dataframe()`
  return pandas frames.
- The tick loop, in pseudo-code (from `mesa/model.py` + `scheduler.py`):

  ```python
  while model.running:
      model.step()                # user code: schedule.step() + bookkeeping
      schedule.step()             # for agent in order: agent.step(model)
      datacollector.collect(model)
  ```

**What we take.**

- **Single-RNG-instance discipline.** Mesa holds one `random.Random(seed)`
  on the Model and passes it everywhere an agent needs entropy. This is
  exactly our INV-2; Mesa is the Python reference that the pattern works.
- **Model / Scheduler / Agent vocabulary.** Our `core/` ≈ Model
  (clock + rng + queue + writer); our `heapq` queue keyed
  `(tick, sub_order, actor_id)` ≈ Scheduler (with a stricter ordering
  policy); our `sim/systems/*` ≈ per-system Agent.step() pieces.
- **DataCollector precedent.** Mesa's `agent_reporters` /
  `model_reporters` is the same idea as our M1–M5 metrics
  (`CORE_DESIGN_RESEARCH.md` §6 P1b–d, D-019): computed from the run,
  not by feel. We compute M1–M5 by folding the JSONL log, not by
  collecting at runtime — but the *notion* of "named, callable,
  replay-derived" metrics is Mesa's.

**What we adapt.**

- **`agent.step(model)` → event emission** (INV-1). Mesa's agent decides
  and acts in one call, mutating state directly. Our agent produces an
  `Intent` (or none); the queue decides ordering; the writer flushes;
  the projection applies. The Intent is the unit of decision; the Event
  is the unit of state-change; they are not the same object (this is
  the Spec-Talk boundary — see `MVP_SCOPE.md` §7, `EVENT_SCHEMA.md` §1).
- **Scheduler → heapq** (INV-2). Mesa's `RandomActivation` reshuffles
  every tick; we key the queue by `(tick, sub_order, actor_id)` so
  ordering is deterministic without per-tick reshuffling. Mesa's
  `SimultaneousActivation` two-phase step is on file — a future phase may
  want simultaneous-intent resolution; not phase 0.
- **`DataCollector` → log-derived metrics** (D-023). Mesa collects at
  runtime into per-step frames; we fold the JSONL log to compute M1–M5.
  Same output shape, opposite path; the DataCollector pattern is reserved
  for the T2 test path (and `balance-1` 1000-sim harness, TASKS infra).

**What inspires us.** The **framework-not-engine** posture: Mesa is a
library, not an executable — agents and models are user code; Mesa
provides the tick loop, RNG, scheduler, and collectors. This matches
our stdlib-only posture (D-012) — we are not a game, we are a
simulation core. The "scheduler = the policy" insight
(`SimultaneousActivation` vs `RandomActivation` vs `StagedActivation`)
is the same lesson as our queue key: ordering is the design lever.

**Strengths.**

- Same language as our core (Python) — pattern transfer is one-to-one.
- Apache-2.0, mature, widely taught; many reference models in-repo.
- Single-RNG-instance discipline is literally our INV-2 — Mesa proves it.

**Weaknesses.**

- **Pure ABM = episodic amnesia** (Mesa / Sims problem,
  `CORE_DESIGN_RESEARCH.md` §2 row "Mesa"). `step()` mutates state; no
  event log; replay = re-run, not fold. Our JSONL log + `state_changes`
  is the amnesia fix — the lesson ported from The Sims via Mesa.
- No causal chain — `agent.step()` is opaque; the "why" lives in agent
  code, not the framework. Our `cause` (P1a) records this at the event.
- No content/code split (INV-3) — Mesa has no opinion on domain data;
  that's our addition via `content/tavern_pack/`.
- No determinism-by-construction — Mesa's `RandomActivation` is
  deterministic *given the seed*, but the contract is "replay the same
  run", not "byte-compare two runs from the same seed + same Python
  version". Our INV-2 + T1 byte-identical test is stricter.

**Verdict.** Phase-0 architectural pattern reference. The closest
language-level precedent for our tick loop. Half positive (RNG
discipline, scheduler-as-policy, framework-not-engine), half negative
(amnesia, no causal chain) — the negative half is exactly the spec for
our event log.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
