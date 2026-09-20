# EVE Online · `REFERENCES.md` §10 · proprietary (design notes only) · phase 6 / track A (res-1)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md` §0.
> Iteration plan: `docs/REFERENCES_DEEP.md` §1 (ref-20, 4-batch + the
> Kenshi economy loop). Anti-drift (D-026): catalog/license/URL/phase
> gating in `docs/REFERENCES.md`; one-line
> the cross-reference synthesis in `docs/BLUEPRINT.md`; concrete mechanics
> here. Source is
> proprietary — the famous CSM/FFDC economic talks (CCP Dr.EyjoG's
> "EVE economy" presentations), the monthly economic reports, and the
> published dev notes only. No code, no assets, no 1:1 rewrites
> (`REFERENCES.md` §0.5).

**What it is.** CCP's single-shard MMO (2003) with the only
player-driven economy at MMO scale that has been *publicly analyzed
by its own economists* — a closed-loop production economy where
~everything of value is built by players from mined materials, and
destruction is permanent.

**Concrete mechanics.**

- **Absolute sinks.** A destroyed ship is gone — the hull, the
  fittings, the cargo (some loot drops, the rest is removed). Insurance
  pays ISK, not matter. Every combat outcome is therefore a *demand
  event*: the loser re-enters the market as a buyer, the region's
  industrial chain re-spins up. **Destruction is the pump.**
- **The production interdependence chain.** Ore → minerals →
  components → modules/hulls; moons yield advanced materials; blueprints
  (originals, copies, invention) gate the tech tiers. No player makes
  a battleship alone — the vertical chain forces the horizontal
  trade. The devs' own talks: the ISK faucet/sink ledger and the
  monthly mineral-volume index tracked against fleet-loss spikes.
- **Geographic friction as price spreads.** Jita (the trade hub)
  prices versus nullsec front-line prices differ by the *haul risk*:
  a freighter run through hostile space carries ambush probability,
  so regional buy orders price the risk premium in. The spread is
  the game's real "map" — distance is measured in ISK/m3.
- **Information asymmetry.** Local market prices are visible only
  where you stand; intel on distant prices is player-run (scouts,
  price-relay channels, third-party market APIs). Insider knowledge
  of an upcoming fleet move is arbitrage. Rumors move markets before
  fleets move.
- **Scarcity wars.** When CCP throttled a key input (the r64
  moon-goo era, later the null-sec anomalies), the political map
  re-formed around the remaining sources: alliance-level wars whose
  casus belli was a resource ledger, not a narrative.

**What we take.** **Sinks via the irreversible item laws** — res-1's
sink half: EVE is the proof that a sink is not a balance patch but
the *engine of demand and drama* (our arson family's "losses
irreversible" is the same law at tavern scale; the theft family's
"the axe leaves the room" — position as canon). **Price spreads as
derived read-side values over distance+risk**: the river artery's
town-vs-hill iron spread is the Jita/front-line spread, a *read* the
pack derives, never a negotiated market. **Information asymmetry =
rumordrift's economic half**: news rides the road with fidelity
decay — the merchant who knows the convoy was lost *before* the
market does is our insider, a knowledge record with a price marker
(PACK_SPEC §6).

**What we adapt.** Player-driven *production* is refused — our
sources are declared (mines, forges as pack data), the labor is
invisible (aggregate flows on the maclock cadence). The blueprints/
tech-tiers ladder collapses into ONE focal scarcity (the Dune law:
hill-smelted iron binds wealth/supply/claim — no r64 table of
seventeen tiers). Warfare-as-sink becomes the crime-pattern shift
(theft/arson families over the landed mechanics), never a combat
system (outside every planned phase).

**What inspires us.** The economic reports themselves: CCP published
faucet/sink ledgers and price indices because the *story of the
world is legible in its ledgers* — the chronicler's posture, economy
edition.

**Strengths.** Two decades of public, quantified evidence that
closed-loop scarcity generates political narrative without authored
plots — the strongest single confirmation of VISION §6. The
spread-as-risk-premium is a fully deterministic function of
geography + threat state: cheap to compute, rich to read. Player
arbitrage around *information* (not just price) proves the knowledge
layer is the economy's other half — our exact architecture
(epistemics beside physics).

**Weaknesses.** The economy's legibility required CCP's economists
publishing monthly; the in-game tools never answered "why is this
expensive" (same opacity minus as X4/DW — our read surface answers
in one line). Vertical chain depth (17+ tiers) creates cold-war
stagnation between production blocs — mono-resource focus is the
cure, deliberately ours. Player-run markets are also *gameable*
manipulation theaters (pump-and-dump on region buys) — no NPC
economy can be so manipulated because ours never negotiates; the
spread is derived, not traded.

**Verdict.** res-1's **sink + friction + asymmetry donor**: the
closed-loop law (absolute sinks pump demand), the spread-as-derived
read, and the rumor-moves-markets confirmation — the theft family's
and rumordrift's economic backbone, phase-6 form.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
