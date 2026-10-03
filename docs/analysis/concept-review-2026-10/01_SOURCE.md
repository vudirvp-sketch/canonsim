# 01 — Source & Replacement Notice

## Provenance

- **Sources:** Canonsim Concept Analysis (Fully Consolidated) + Concept Review 2026-10 CONSOLIDATED + the reworked package already reviewed + live repository evidence noted below.
- **Evidence base:** live clone / ingested review material / direct code probes / `STATUS.md` / `docs/TASKS.md` / `docs/DECISIONS.md` / `docs/ROADMAP.md`.
- **HEAD:** `528de9c5324d37a46278da4614a028f59cf83d08` (`iter-311-worldsuite`).
- **Date:** 2026-10-03.
- **Update reason:** owner-requested consolidation of the review around D0 (Future-Reachability / Causal-Obligation Conservation) and the decision set D0–D11.

## Replacement rule

This directory is the operational form of the review.

- Agents do not need the original free-form review for implementation triage.
- Humans may keep originals for archival reading.
- Future amendments belong here and must preserve this package's agent-operable contracts.

## Standing architecture: preserved, not replaced

```text
resolver → EventDraft → sole writer → append-only JSONL → fold / derived indexes

Mediator / intent door = authority boundary
LLM = interpretation / candidate generation / narration
LLM ≠ canonical writer
```

Core invariants remain INV-1..5. No new truth authority is introduced by this review.

## Key live findings retained from the review

| Finding | Meaning |
|---|---|
| schema-valid `EventDraft(...)` can reach private `_commit()` with undeclared semantics | structural validity is not the full semantic/authority contract; production-path falsifier still required |
| `core/lod.py` derives zones from PC position and filters canonical activity | current LOD tests prove designed behaviour, not causal neutrality / future reachability |
| replay cursor binds seed, pack name/version, log prefix data, runtime cursors | semantic replay identity is incomplete without engine/schema/pack-content/config identity |
| several hot paths scan pack-wide collections then filter | locality is not yet a proven complexity contract |
| clean-boundary resume is strongly tested; writing uses `flush` | do not claim OS-durable commit from `flush` alone |
| injected / model-generated instruction-shaped content can reach the intent door | structural isolation is not semantic intent/authority separation |

## Design interpretation

The update does **not** call for a second architecture. It formalizes a stronger invariant over the existing architecture and derives the next contracts from it.
