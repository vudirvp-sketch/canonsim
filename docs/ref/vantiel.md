# Vantiel RPG rules corpus · REFERENCES.md §10 · license unverified (pattern only — no license statement in the supplied archive) · presentation-1/engine-1 consult, owner-gated (D-190)

> Per-reference deep dive. Format template: this file §0. Iteration
> plan: this file §1. Anti-drift (D-026): catalog/license/phase gating
> in `docs/REFERENCES.md`; the cross-reference synthesis in
> `docs/BLUEPRINT.md`; concrete mechanics here. License filter and
> "patterns not content" rule: `REFERENCES.md` §0.7 (D-015). Scope
> fence: this file is the SOURCE record for the intake-32 routing
> (iter-159, D-190) — the consult residue it feeds is parked behind the
> owner gate at `presentation-1` (TASKS' standing row), never a runtime
> contract, never pack content, never a worldbuild layer. The source is
> the owner-supplied `Vantiel_RPG_Rules_Clean.zip` (37 Markdown files,
> ~408 KB) as consolidated by the uploaded prior-session research
> handoff; the handoff's substrate map was re-verified claim-by-claim
> against HEAD `44151f1` before routing (the convenience-copy law). The
> original archive, the full handoff, and the prior-session one-pass
> record live outside the repo.

**What it is.** An LLM-centric tabletop-style RPG/AI-GM ruleset whose
architectural value for this repo is a set of SEPARATIONS — distinctions
that keep evidence, interpretation, emotion, accessibility, relationship
state, recovery, context, and presentation from collapsing into one
mutable abstraction — never a set of transferable subsystems.

**Concrete mechanics.** The ten separations, each with its Vantiel
mechanism, its already-owned `canonsim` form (verified at HEAD), and its
disposition:

1. **Truth retention != recall salience** (emotional impact and
   reinforcement modulate how long memory stays accessible). Owned:
   INV-1/INV-5 log truth + `core/retrieval.py` recall ranking +
   `core/echo.py` residue. PARTIALLY CONFIRMED — the split is the
   substrate's own shape; magnitude-dependent persistence is already
   emergent (residue = valence x linear decay, so a larger |valence|
   outlasts any fixed threshold — Vantiel's "reinforcement" needs no new
   decay law).
2. **Fact != interpretation** (belief/conclusion never becomes objective
   state). Owned: `core/knowledge.py` records + `core/traits.py`
   crystallization + `core/reflection.py` provenance-carrying events.
   CONFIRMED AS ALREADY EXPRESSED.
3. **Emotion != factual memory** (emotional residue can outlive practical
   recall). Owned: `core/echo.py` as an independent read-side fold.
   PARTIALLY CONFIRMED.
4. **Relationship magnitude != relationship history** (a scalar is not an
   explanation; companion affinity follows shared experience). Owned:
   `entities.json::pair_relations` (directional: A->B never implies
   B->A) + event provenance + knowledge + echo; companion-1 (D-188) is
   the observed consumer. PARTIALLY CONFIRMED — the falsifier (a social
   consumer inexpressible with pair axes + events + read models) has one
   negative instance on record.
5. **Failure != punishment** (repeated failure escalates; failure
   transforms the future answer-space). Owned: `intent_rejected` +
   state changes + predicates (attempts are facts). PARTIALLY
   CONFIRMED — the composition ladder (first failure -> observable
   consequence -> stronger consequence -> a door closes and/or a
   different one opens) is pack authoring, never a failure-count
   subsystem.
6. **Recovery != undo** (recovery is a new causal path). Owned: the
   append-only log (INV-5). CONFIRMED AS ALREADY EXPRESSED.
7. **Knowledge != accessibility** (censorship, secrecy, expertise,
   locality constrain access). Owned: `known_by` + telling/fidelity +
   trust + drift + travel. CONFIRMED AS ALREADY EXPRESSED — access is a
   path/eligibility problem, never a rewrite of the fact.
8. **Context bundle != memory truth** (threads compact under context
   pressure). Owned: `brief/` assembly + budgets/eviction + since-1.
   PARTIALLY CONFIRMED — the fresh residue is the re-expansion law (see
   "What we take").
9. **Journal != canon** (human-facing recall). Owned:
   `render/chronicle.py` pure functions of the log. CONFIRMED.
10. **World intervention != narrative override** (tiered Architect edits
    with scope/consistency/ripple checks). Owned: the
    Intent->validation->OCC->Resolution->Event door. PARTIALLY
    CONFIRMED — the ripple-audit question is a parked candidate, not a
    lint (falsifier: a recurring authored-change failure an explicit
    impact set would have prevented).

Also refused as runtime: the learning watchdogs/self-repair family
(hidden mutable state, nondeterministic self-modification — INV-1/INV-2
conflicts); its diagnostics principle is already expressed
(stale-reflection detection, pack lint, replay tests).

**What we take.** (1) The separations checklist as design-review
questions for the model-facing boundary — each cites its owner above,
nothing restated. (2) The presentation-1 consult material, two items:
the **re-expansion law** — a bounded model-facing context bundle may be
disposable only if its compact claims retain stable event/entity
handles and re-expand deterministically from canonical evidence (never
a second truth, never a mutation of knowledge); and the
**staged-interpretation sketch** — input -> interpretation/intent
proposal -> bounded context -> model decision proposal -> repository
validation -> prose, each stage separately inspectable, the exact
contract derived from the real engine-1 consumer (D-022/D-055), never
guessed from Vantiel.

**What we adapt.** Nothing now. The two pack-authoring compositions
(shared event -> directed relation consequence; the failure ladder
above) are already-expressed law whose authoring form is owned by
PACK_SPEC's authoring loop and the packs themselves; both carry their
falsifiers and wait for a pack that needs them.

**What inspires us.** The strongest cross-domain note: Vantiel's
relationship inertia (enter <= A, leave only >= B) is the weaker form
of a law this repo already owns — the D-105 deadband family prevents
state chatter BY CONSTRUCTION (no state flips, so no hysteresis is
owed; `core/factions.py`), one less knob to tune. The transplant test
ran both directions and the existing own-form won.

**Strengths.** A coherent separation discipline unusual for LLM-GM
rulesets: the epistemic surface (direct knowledge, secondary
transmission, expertise, regional awareness, censorship) is decomposed
almost exactly along the axes `core/knowledge.py` later chose
independently — a strong cross-domain confirmation of the substrate's
shape. The staged cognitive pipeline names the right seams
(interpretation / recall / decision / realization) even though its
runtime form is LLM-private.

**Weaknesses.** License/provenance unverified — pattern/reference only,
no prose, names, setting content, tables, prompts, code, or 1:1
formulations. Subsystem-first thinking: affinity meters, personality/
trauma flag catalogs, universal intelligence/wisdom multipliers, and
fixed difficulty percentages that are not causally grounded in world
state. The Architect's free-form edit path bypasses any proposal/
validation door. Setting content (Three Walls, factions, magic,
bestiary) is not portable knowledge.

**Verdict.** PARTIALLY CONFIRMED (intake-32, D-190): a SEPARATIONS
donor for the model-facing boundary — the consult material parked at
presentation-1 (owner-gated, the intake-30 visual-card precedent); zero
build-grade items; the queue untouched. The reject list is binding:
generic difficulty percentages; mutable memory threads as truth; generic
affinity meters; large flag catalogs; universal cognition multipliers;
free-form Architect world edits; journal as mutable state;
classes/combat/inventory as subsystem donors; setting content. The
falsifiers that would reopen any candidate: the context bundle vs the
current brief/retrieval stack on a real consumer (context cost,
traceability, re-expansion correctness); two independent propagation
consumers requiring shared edge-selection semantics beyond
known_by+trust+locality+drift; a measured oscillation problem the
deadbands do not already prevent; a recurring authored-change
contradiction for the ripple question.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
