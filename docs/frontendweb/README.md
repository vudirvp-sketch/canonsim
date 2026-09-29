# Canonsim Frontend-Web Track — Active Knowledge Surface

> The web-frontend track surface: the durable agent context + the
> preserved pack archive. Created iter-288 (D-243) by ingesting the
> owner's external `CANONSIM_FRONTEND_WEB_AGENT_PACK_FINAL_v1_3.zip`.

## Purpose

This directory is the **web-frontend track surface**: what an agent
resuming the web-frontend work needs. It is not a runtime contract
by itself — the binding distilled law lives at
`docs/FRONTEND_WEB_LAW.md`; the repository owner documents remain
authoritative everywhere (the pack's own routing law).

## Read order

0. `FRONTEND_WEB_AGENT_CONTEXT.md` — the durable compact agent
   context (identity, the reconciliation verdicts, the owner-gated
   boundary, the stage map, navigation, anti-patterns) — the entry
   surface for an agent resuming the web track; it navigates, it
   never replaces the owners.
1. `docs/FRONTEND_WEB_LAW.md` — the binding web-frontend
   implementation law (the pack's distillation: the S0 gate, the
   gateway seam, dual-read, the connection budget, browser runtime
   bounds, surface modules, effective-state closure, the tooling
   floor).
2. The pack's own read order inside the archive
   (`archive/…/docs/AGENT_READ_ORDER.md`) — only when the compact
   law names a seam whose full contract is needed.

Do **not** load the archive by default; its provenance fence is
`archive/README.md`.

## Information ownership

| Surface | Owns | Does not own |
|---|---|---|
| `FRONTEND_WEB_AGENT_CONTEXT.md` | the web-track agent context: identity, the reconciliation verdicts, the owner-gated boundary list, the stage map, navigation, anti-patterns | owner content — it navigates and reconciles, never restates; history (the archive record stays in `archive/README.md`) |
| `archive/` | the preserved pack: verbatim evidence, provenance, the unique retains | anything current — never re-ingested, never a second source |

## Current stage

**S0 LANDED (iter-289, D-244) — awaiting the owner's green review.**
The Redot tree DELETED at iter-290/D-245 (the owner's «удаляй redot»
call — the launcher re-pointed to the web dev server). The standing
boundary list (the later gates):
`FRONTEND_WEB_AGENT_CONTEXT.md` §5.
