# Distant Worlds: Universe · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-18, 3-batch).
> Anti-drift (D-026): catalog/license/URL/phase gating in
> `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. Source is
> proprietary — public dev diaries (Elliott Gibbs, CodeForce) and
> player guides only. No code, no assets, no 1:1 rewrites
> (`REFERENCES.md` §0.5).

**What it is.** CodeForce's space 4X (2014) famous for one boundary:
a **private economy the player does not own** — the private sector
mines, hauls, builds, and trades on its own supply/demand, while the
state (the player) taxes it and buys from it. The boundary between
"the world runs itself" and "the player directs" is drawn through
*ownership*, not through scripting.

**Concrete mechanics.**

- **Two sectors.** State ships (built with state money) do war,
  exploration, and policy. Private ships (built by private
  corporations with their own money) mine resources, ferry cargo
  between colonies with price differences, and construct civilian
  stations. The player sees all of it and controls none of it
  directly.
- **Money flows are visible.** Private freighters pay the state for
  fuel; the state taxes colonies and freight; the private sector pays
  the state for mining licenses. The player's income is a *consequence
  of the private economy's health* — a trade war strangles the
  treasury indirectly, through the tax base.
- **Supply/demand freight.** A colony producing fuel sells cheap;
  a colony consuming it pays more; private freighters run the route
  because the margin exists. No scheduler assigns them — the margin
  IS the assignment. When demand is met, margins compress and the
  traffic thins by itself.
- **State constrains, never operates.** The policy levers: taxes,
  fuel-price controls, licensing, monopoly/embargo declarations,
  port capacity. If the state squeezes (high taxes + price caps),
  the private sector contracts — fewer ships built, routes thinning
  into scarcity spirals the player then has to police.
- **Agents at both layers.** Independent worlds, pirates, and the
  monsters are third parties feeding on the same flows — piracy
  suppresses the routes' margins, which suppresses the tax base:
  the security problem is paid for through the economy, not
  through a threat-meter.

**What we take.** **The boundary law — res-1's declaration shape**:
the simulator owns the rules (supply, demand, margins, decay), the
*behavior* is emergent; the player-acting-through-policy is the
province's whole posture (the ratio dynamics: the player tips, never
script gates). Our economy layer keeps the same split as pack data:
flows and margins declared; the convoys, the markets, and the crime
patterns emerge from them. The **tax-base coupling** maps to res-1's
faction funding: the garrison's supply line IS a flow node — when the
artery narrows, the institution weakens through the data, not through
a script.

**What we adapt.** Private-vs-state ownership becomes
**declared-vs-derived**: in our law, the pack authors the cycle
(source → flow → sink, the graph, D-116), the world *derives* the
prices and the consequences (read-side values, fold-over-events);
there is no second decision-making sector to own — NPCs with
urgencies and factions with goals are already the agents. Freight
assignment by margin is kept **as read, not as process**: a route
shows "margin exists" (a derived line the brief can carry); the
actual traffic is the cold aggregate condensing (depth-7), never
per-ship scheduling.

**What inspires us.** The treasury as a hose clamped by the world:
the player who wants money must keep the *world's* flows healthy —
economy design as incentive alignment, not as spreadsheet.

**Strengths.** The cleanest published example of an economy that is
simulator-run with the player as a constraint-setter (X4 runs agents
but also lets the player own the agents — DW refuses that). The
cascading statecraft is legible: squeeze policy → visible contraction
→ the player's own problem. Scales well (a DW galaxy is thousands of
simultaneous private ships on modest hardware, because the logic per
ship is a margin check).

**Weaknesses.** The private AI is opaque to the point of legend —
freighters idle with visible demand and the player cannot find out
why (no per-agent explanation surface; our answer: every flow line
names its cause chain, INV-1). The UI is counter-dense but causally
silent — same as X4, worse. Late-game performance and balance rely
on quiet caps the player never sees — the anti-shape for our lint =
CI posture (declared budgets, enforced at load).

**Verdict.** res-1's **boundary donor**: the declaration/emergence
split, the tax-base coupling, and the proof that constraint-based
economy play reads as statecraft — the Dune row's "ONE binding
scarcity that ties wealth, supply, and claim" gets its *mechanical*
architecture here.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
