# Path of Exile · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1 — the social-economy note)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-20, 4-batch + the
> Kenshi economy loop). Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. Source is
> proprietary — GGG's public postmortems, economy talks, and patch
> notes only. No code, no assets, no 1:1 rewrites (`REFERENCES.md`
> §0.5).

**What it is.** Grinding Gear Games' ARPG (2013) whose currency is
**functional**: there is no gold — the money IS the crafting material,
and spending it consumes it.

**Concrete mechanics.**

- **Currency orbs as consumable tools.** Each orb performs a
  modification: an Orb of Transmutation upgrades a normal item to
  magic; a Chaos Orb re-rolls a magic item's modifiers; an Exalted
  Orb adds one; a Divine Orb re-rolls numeric values of existing
  modifiers; a Mirror of Kalandra duplicates an item (the
  hyper-scarce reserve asset). **Every monetary unit is a verb.**
- **Value from use, not denomination.** Orbs are valued against each
  other through their *utility ratios* (how many Transmutations a
  Chaos is worth in practice), not by any declared face value. The
  "exchange rate" is a community-emergent convention restated each
  league, drifting with the meta (which crafting verbs the current
  builds want).
- **Consumption on use.** Using currency in crafting *removes it from
  the economy* — crafting is a sink. The league reset (fresh economy
  every ~3 months) exists precisely because wealth and perfect items
  accumulate otherwise; the reset is the meta-level answer to an
  open faucet.
- **Devaluation on publication.** When GGG patches a crafting
  outcome (a modifier pool changes, an exploit closes), the orbs
  tuned to it lose utility overnight — value follows the *function*,
  so a function change is a currency crisis. Economic shocks are
  patch notes.
- **Trade friction as design.** No auction house (deliberately):
  person-to-person trade with listing costs, item-by-item — the
  friction is the anti-flipping damper. Currency-item exchange
  sites emerged (player-run) and were later semi-formalized in-game.

**What we take.** The **leverage-as-currency analogy** (the catalog
row's own note): our secrets/leverage clusters behave like PoE orbs —
*spending is consuming* ("one secret buys one play", the coerce
card-play law, iter-45), value tracks function (a secret about the
guard's purse is worth what coerce can do with it), and **devaluation
on publication**: the spent/leaked cluster dies when the fact becomes
common knowledge (the fidelity/liveness window). res-1's sinks read
the same law materially: the consumed resource leaves (irreversible
item laws), it is never debited against a balance.

**What we adapt.** Emergent exchange rates are **refused** — the
knowledge economy has no market (the price marker is an observable
state token, PACK_SPEC §6, not a negotiated number). The league-reset
posture becomes the *campaign* shape: one log per world, a session
binding the checkpoint — value is bounded by the world's finite
history, not by a scheduler's reset (no wall-clock, INV-2). Crafting
verbs stay out of scope (items as claim/position records, not
modifier stacks — the take/drop/steal family).

**What inspires us.** Money as verbs: the economy IS the action
grammar — a currency nobody can spend is a score, not a resource.

**Strengths.** A decade of public design commentary on
currency-as-consumable: GGG openly discusses sink balance, league
resets, and trade-friction trade-offs (the most documented
functional-currency experiment anywhere). The system is fully
deterministic per craft (seeded rolls) while the *macro* economy is
social — the two-layer split we run (canon determinism, social
emergence). Utility-valued money needs zero price tables — value
self-organizes.

**Weaknesses.** The meta-drift makes the currency's meaning unstable
outside a competitive context (our leverage value is anchored to the
fold's live facts, not to a shifting build meta — steadier). Trade
friction at their scale breeds third-party tooling and RMT gray
markets — the anti-shape for pack design: our scarcity surfaces are
diegetic (merchants, rumors), never interface friction. The league
reset is a hard erase — INV-5's own anti-shape (corrections are new
events; the log never resets).

**Verdict.** The **social-economy note's donor**: spend-consumes,
value-follows-function, devaluation-on-publication — the secrets
family's economic vocabulary; for res-1 itself it contributes the
*sink's grammar* (a resource that leaves when used), not the market.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
