# Universe Audit Protocol webapp (UAP) · `REFERENCES.md` §9 · README claims MIT; **no LICENSE file** (checked 2026-08-27 — pattern only until fixed) · track B (phase-1 harness) / phase 6 (pack CI)

> Per-reference deep dive. Format template: `REFERENCES_DEEP.md` §0. Iteration
> plan: `REFERENCES_DEEP.md` §1. Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line synthesis in
> `docs/CORE_DESIGN_RESEARCH.md` §2; concrete mechanics here. License filter
> and "patterns not content" rule: `REFERENCES.md` §0.7 (D-015).
> Source: `github.com/vudirvp-sketch/universe-audit-protocol-webapp` — the
> owner's own project; last commit 2026-05-12. Read in full:
> `README.md`, `src/lib/audit/prompts-v3.ts` (1346), `pipeline-v3.ts` (429),
> `scoring.ts` (204), `types-v3.ts` (222), `context-bridge.ts` (254),
> `protocol-data.ts` (checklist), `patch-tree.ts`, `error-handler.ts` (271),
> `llm-client.ts` (1140), `llm-streaming.ts`, vitest suites (~150 cases).

**What it is.** A no-backend web tool (Next.js 16 static SPA on Cloudflare
Pages + a CORS-proxy Worker → 14 LLM providers; Zustand + localStorage, no
server, no DB) that audits a user's fictional-world concept through a 5-block
sequential LLM pipeline implementing a Russian-language "Universe Audit
Protocol v10.0". Free-form markdown in, markdown out; a separate JSON-mode
call scores a 52-item checklist.

**Concrete mechanics.**

- **Block 1 Orientation** — audit mode (conflict / kishō / hybrid); author
  profile as a 7-question yes/no test (6-7 = gardener, 4-5 = hybrid, 0-3 =
  architect, with %-band); 8-element concept skeleton (Thematic Law, Root
  Trauma, Hamartia, 3 Pillars in an A→B→C→A cycle, Emotional Engine = dominant
  grief stage, Author Prohibition, Target Experience, Central Question);
  7-question yes/no screening (4+ NO = "stop, rebuild skeleton").
- **Block 2 Mechanism (L1)** — MDA+OT 5-level vitality model (mechanics /
  dynamics / aesthetics / ontology / corporeality + cross-level consistency:
  "mechanics 'killing pays' + ontology 'killing is tragedy' = fix or declare
  irony"); 17 vitality criteria, thresholds 13/17 alive, 10-12 rework, <10
  redesign; N×N connectedness matrix — a **verb of action in every cell**,
  every element ≥2 bidirectional links; 5×5 faction matrix with 6
  faction-liveness criteria (internal conflict, distinct economy,
  join-closes-opens, NPCs argue, unacknowledged dark side, ideological
  trauma) — <3 met = decoration; Tarkovsky space-with-memory ("a trace of an
  event we never saw"); ripple effect ≥2; three-handshakes rule (any two
  elements ≤3 steps apart); economic arrow — 6 mandatory questions (origin /
  control / exchange / who suffers / what people eat / superstitions);
  "A chtoby chto?" ("what for?") 7-iteration why-chain, break at step ≤4 =
  critical.
- **Block 3 Body + Psyche (L2+L3)** — 5-layer character model (motivation /
  hamartia / flaw / arc / belief-as-perception-filter); competence rule (show
  mastery *before* the fall); price of greatness hits identity, not HP; Mary
  Sue test 8 items, ≤3 fails allowed; character cult potential 7 items;
  psychological authenticity 5 items; 3 character anti-patterns (stagnation,
  intellect degradation, physical solution to a psychological problem);
  Sanderson magic test (5 questions incl. "what happened at the first
  abuse?"); **7 logical hole types** — motivation / competence / scale /
  resources / memory / ideology / time — each with a quick fix (e.g.
  motivation hole → "he didn't know / was awaiting a condition"; memory hole
  → "suppression mechanism"); Grief Architecture: 5 stages × 4 materialization
  levels (character + location + mechanics + act) — a stage hanging on one
  level = structural hole; generative template Thematic Law → dominant stage
  ("deprives of illusions → denial as dominant"); ensemble rule: no two key
  characters in the same grief stage.
- **Block 4 Meta (L4)** — three reality layers each tested by *removal*
  (personal desire / plot causality / meta-authorial question "and you
  yourself…?"); Cornelian dilemma generation from the Thematic Law with 4
  criteria (value vs value, irreversibility, identity, victory = betraying one
  truth — a "third way" existing = fake dilemma); authorship ethics 4
  questions; agent mirror; misdirection 4 parameters (false exposition, visual
  anomalies, emotional hook before lore, layered onion); narrative debt 4
  types (informational / emotional / mechanical / thematic) each with a
  non-payment consequence; diegetic integrity table + "can one character
  explain this to another without the fourth wall?" test.
- **Block 5 Synthesis** — prioritized fix list (diagnosis / concrete action /
  approach via patch decision tree / effort in hours-days-weeks); verdict;
  X/52 checklist score; 3 priority actions; optional exemplar comparison
  (Disco Elysium, Expedition 33, Pathologic 2, Attack on Titan) with
  per-criterion deltas.
- **Engineering** — chunked sub-requests (Block 2 → 4 chunks, Blocks 3-5 → 2
  each) against free-plan timeouts; RPM-aware inter-chunk delay
  `max(1000, 60000 / rpm)`; single retry with 5 s backoff on 429/502/503;
  partial-text recovery (accumulated stream text is returned if the request
  dies mid-stream); per-block temperatures 0.2 / 0.45 / 0.45 / 0.45 / 0.6
  (extraction → analysis → synthesis); `DESIRED_MAX_TOKENS` 8192 (block 1)
  and 16384 (blocks 2-5) capped by a per-model capabilities table (e.g.
  `zai: contextWindow 128_000, maxOutputTokens 8192`); SSE delta extraction
  per provider family; `classifyLLMError` → typed `AuditError` with
  retryable/transient split and Russian user messages.
- **Context bridge** (`context-bridge.ts`) — regex extraction of orientation
  context (3 pattern shapes per skeleton element: "Key: …", table row,
  bullet); weaknesses summary via the literal marker
  `"РЕЗЮМЕ СЛАБЫХ МЕСТ:"` aggregated across chunks, then a keyword fallback
  (слаб/дыр/проблем/…), then "last 500 chars"; every extraction failure falls
  back to raw markdown — the bridge never breaks the UI.
- **Scoring** (`scoring.ts`) — separate low-temperature (0.1) JSON-mode call
  over the concatenated audit markdown; per-item verdicts
  **PASS / FAIL / INSUFFICIENT_DATA** + an evidence quote; items the LLM
  omitted are auto-filled as INSUFFICIENT_DATA (never fabricated); the
  52-item `MASTER_CHECKLIST` lives in `protocol-data.ts` with a per-media
  applicability filter (`applicableMedia`); aggregates X/52 + per-level L1-L4
  percentages; failure is non-blocking (the audit completes regardless).

**What we take.**

- **The countable-criteria discipline as independent validation of our
  metric law.** UAP's section 0.6 rule — "count-based screening: code
  decides, not the LLM" — is the narratology-side twin of our "metrics
  computed from the log, not by feel" (`MVP_SCOPE.md` §15). Two projects
  unknown to each other converging on "quality gates must be countable over
  evidence" is the strongest available external validation of the M1-M5
  approach.
- **The "A chtoby chto?" why-chain is our `cause` chain.** UAP audits prose
  for it after the fact (break at ≤4 = critical); we have it by construction
  (`EVENT_SCHEMA.md` §2 `cause` on every event; M3 mean depth ≥ 2). Cited as
  validation of M3, not as a new mechanism.
- **The 7 logical hole types as a test-taxonomy crosswalk** (the single most
  load-bearing transfer): motivation hole → T3 blind-NPC suite ("no NPC
  action without a preceding knowledge record", `MVP_SCOPE.md` §10); memory
  hole → T2 replay fold == state (INV-1 makes the hole *structurally
  impossible* — the log is the fix UAP patches over with "suppression
  mechanisms"); competence hole → rules-driven behavior (no author-needs
  actors exist to degrade); scale hole → D-005 buffer discipline
  (complications are seeded, never disproportionate inventions); resources /
  ideology / time holes → tick queue + queue key (INV-2) + phase-5 faction
  goals. Recorded in the `TEST_PLAN.md` sketch (`SPECS_BACKLOG.md`).
- **Prompt-engineering shapes for the phase-1 harness (track B):** role in
  the system prompt (a senior-auditor persona whose explicit job is
  non-flattering diagnosis — "you do not praise for the sake of praising");
  full criteria + thresholds + worked examples embedded in prompts, never
  abstract labels ("the LLM sees criteria, not tags"); staged context
  injection — each later block receives the *distilled weaknesses* of earlier
  blocks, not their full text (our brief-as-delta principle, `BRIEF_SPEC.md`
  sketch, arriving from the other direction); per-stage temperature policy
  (0.2 extraction / 0.45 analysis / 0.6 synthesis) mapping onto mode A/B/C
  roles (`TECH_NOTES.md` §1); exemplar-anchored comparison (the Disco
  Elysium / Expedition 33 block) = golden-set comparison for the chronicler —
  computed against committed chronicles, never LLM-judged.
- **Free-tier resilience patterns**, proven in production on 14 providers:
  chunked sub-requests, RPM-aware pacing, single retry with fixed backoff,
  partial-text recovery, non-blocking auxiliary calls. Cheap, MIT-claimed,
  directly portable to the mode-A harness.
- **The three-state verdict with an honest default.** PASS / FAIL /
  INSUFFICIENT_DATA where omitted items *default to* INSUFFICIENT_DATA and
  missing evidence is never fabricated — the correct shape for
  `VALIDATION_SPEC.md` fact-transaction reports.

**What we adapt.**

- **Pack-admission lint (phase 6, `PACK_SPEC.md` sketch).** UAP's teleology
  gate ("every event type must produce a state delta or a hook — dead
  content otherwise") becomes a deterministic pack-CI check: dead action
  types, orphan entities, empty intersection-matrix cells
  (`MVP_SCOPE.md` §6), declared-but-unused templates. Thematic Law, pillars
  and Author Prohibitions enter as **pack metadata** (INV-3: content, not
  code), enforced as log asserts at gate review (e.g. "no event without
  `cause`" — already INV-1/D-005 by construction; "every kill seeds ≥1
  consequence hook" — already M2 discipline). UAP's Grief Architecture
  likewise becomes pack metadata for packs that want it, never a core system.
- **The 17 vitality criteria: only the countable subset may become metrics.**
  Interdependence ≈ M3 + M1; world-memory ≈ M2 + M3; no-free-lunch ≈ the
  causal-density checklist (`MVP_SCOPE.md` §15) — the honest form here is a
  gate-report annotation, **not** a new M-id and **not** UAP's invented
  thresholds (0.6 / 0.9 / 0.2 in the integration draft contradict our law:
  thresholds come from the iter-6 measured baseline, `MVP_SCOPE.md` §15).
  The literary criteria (tragedy-without-villain, unexplained-detail
  atmosphere, cult potential) stay out of core — future chronicler-critique
  material for track B, never simulator law.
- **The language contract** (prompts/prose Russian, JSON keys and enums
  English, code comments English) matches D-001/D-009 exactly; for phase 1
  it lands as template/pack data, zero code.

**What inspires us.** A quality gate for worlds is the same species of
machinery whether the world is written or simulated: UAP audits authored
canon with rubrics; we audit emergent canon with fold(log). The rubric
approach, validated from the narratology side, raises our confidence that
gate reviews (`ROADMAP.md` §5) are the right instrument, not bureaucratic
overhead.

**Strengths.** Every criterion is operationalized — a number, a threshold, or
a test question, never a vibe; honest defaults (INSUFFICIENT_DATA) instead of
forced binary verdicts on soft criteria; the resilience layer is proven on
free-tier providers (the same constraint class as our local-LLM scenario,
`TECH_NOTES.md` §2); identical language contract (D-001 shape); the owner's
own code — zero negotiation cost, and a one-file LICENSE fix unlocks lifting
outright.

**Weaknesses.** (1) **LLM-as-judge scoring**: the X/52 checklist is the
opinion of the same model family that wrote the audit — no seed, no inter-run
stability, unusable as a metric under INV-2; their own section 0.6 rule
("code decides") is applied to screening but not to scoring. (2) **Regex over
markdown** as the inter-block contract — three fallback layers plus keyword
heuristics; exactly the "post-hoc text sanitization" crutch D-018 rejects;
our grammar-constrained Intent JSON and prose-never-parsed law is the fix.
(3) **Free-form markdown output** — no machine-checkable contract on any
block. (4) **No LICENSE file** despite README claiming MIT (checked
2026-08-27): by our own catalog convention this reads "none = all rights
reserved, reference only" — patterns are free, code lifting is not, until the
owner drops a LICENSE in. (5) Forced PASS/FAIL on literary criteria produces
false precision; asserted thresholds (13/17) with no outcome validation. (6)
Wall-clock everywhere (`Date.now()`, `elapsedMs`) — fine for a webapp, the
inverse of INV-2. (7) The full concept text is re-sent in all ~11
sub-requests — acceptable for a one-shot tool, wrong for a runtime loop (our
brief is O(relevance), never O(history)). (8) localStorage state: no
immutability, no versioning, no replay — an audit is stateless opinion, the
opposite of a canon.

**Verdict.** The rubric-and-resilience donor: countable-criteria discipline
as external validation of M1-M5 and the gate-review instrument; hole-type
taxonomy → test crosswalk; prompt shapes + free-tier resilience for the
phase-1 harness; pack-lint vocabulary for phase 6. Structurally negative on
LLM-judged scores, regex bridges and free-form canon — all three are the
inversions our invariants exist to prevent. Same owner: fixing the LICENSE
file upgrades "pattern reference" to "code donor" at zero cost.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
