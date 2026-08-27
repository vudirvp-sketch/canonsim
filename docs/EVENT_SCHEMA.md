# EVENT_SCHEMA.md — Event Contract v0

> Paired with `schemas/event.schema.json` (2-place sync, test-enforced: the
> example in §10 must validate). A breaking change = `schema_version` bump +
> owner approval (`AGENTS.md` §8).

## 1. Log format

- One JSONL file per run: `logs/run_<seed>_<n>.jsonl` (gitignored).
- Line 1 = header; then one event per line; append-only.
- The header carries **no wall-clock timestamp** (determinism, INV-2):

```json
{"header": true, "schema_version": "0.1", "seed": 42,
 "python": "3.11.9", "commit": "a1b2c3d", "pack": "tavern_pack@0.1"}
```

- SQLite is a derived, rebuildable index over the log — never the truth
  (INV-1). Dropping and re-folding the DB must always be possible.

## 2. Event record

| Field | Type | Req | Meaning |
|---|---|---|---|
| `id` | string, `^ev_[0-9]{4,}$` | yes | monotonic, gap-free per run |
| `t` | integer ≥ 0 | yes | tick when the event fires |
| `type` | string, snake_case | yes | pack-defined verb |
| `actor` | entity id | yes | who did it (`world` for world-events) |
| `target` | entity id | no | direct object |
| `cause` | event id or null | yes | causal predecessor; intents chain here |
| `outcome` | object | yes | type-specific payload, pack-defined |
| `knowledge` | array | yes (may be empty) | knowledge records born here (§3) |
| `state_changes` | array | yes (may be empty) | state deltas incl. irreversibility (§4) |
| `hooks` | array of strings | yes (may be empty) | deferred-consequence tags (§5) |
| `importance` | `low` \| `medium` \| `high` | yes | computed by the pack rule (§6) |
| `provenance` | object | yes | seed, cause_intent (§7) |

## 3. Knowledge record

| Field | Type | Meaning |
|---|---|---|
| `who` | entity id | the knower |
| `channel` | `saw` \| `heard` \| `told` \| `inferred` | how they learned |
| `fidelity` | `exact` \| `partial` \| `vague` | information quality |
| `knows` | string | what they know (structured token, pack vocabulary) |
| `at` | integer | tick of learning |
| `source` | event id | where the record came from |

Rules:

- `known_by` is **derived** from `knowledge` records — never stored on the
  event.
- **Rumor = knowledge-transfer event.** The teller emits new records for the
  listener with fidelity decayed one step (`exact → partial → vague`,
  `channel: told`). Distortion comes from source incompleteness; no separate
  rumor system.
- **A lie is a crafted record:** distorted `knows` or misrepresented fidelity —
  legal data, the foundation for `believes/lies` in phase 4.
- **Blind-NPC rule:** no record → cannot know, cannot say (T3).

Transfer example — the drunkard at the market:

```json
{ "id": "ev_0031", "t": 990, "type": "rumor_told",
  "actor": "npc_drunk_01", "target": "npc_market_crowd_01", "cause": "ev_0029",
  "outcome": { "accepted": true },
  "knowledge": [
    { "who": "npc_market_crowd_01", "channel": "told", "fidelity": "vague",
      "knows": "figure_at_back_door_last_night", "at": 990, "source": "ev_0031" } ],
  "state_changes": [], "hooks": ["market_gossip_spreading"],
  "importance": "low", "provenance": { "seed": 42 } }
```

## 4. `state_changes`

| Field | Type | Meaning |
|---|---|---|
| `entity` | entity id | whose state changed |
| `prop` | dotted path | which property |
| `from` / `to` | any | old and new value |
| `irreversible` | boolean (default false) | never reverts without an explicit counter-event |

Fire has no counter-event: a burned tavern stays burned (T4).

## 5. `hooks`

Tags seeded at event time and consumed by the director's buffer. Each hook
carries triggers (time / place / threshold) defined in pack rules. **Far
hooks** — usable 10–50 turns later — are first-class citizens, not an
afterthought.

## 6. `importance` rule

Computed from pack `rules.json`: a function of entities touched +
irreversibility + far hooks → mapped to `low` / `medium` / `high`. Never "by
feel" — the rule is data, and changing it is a pack change, not a code change.

## 7. `provenance`

`seed` (int, required) + `cause_intent` (intent id, when the event resolves a
player intent). Enough to re-derive *why* the event happened. Model/prompt
provenance joins the same field family when the LLM circuit arrives (phase 1+).

## 8. Versioning

- `schema_version` is a `"0.x"` string.
- **Additive** change (new optional field, new enum value for pack reasons) =
  minor bump.
- **Breaking** change (rename / remove / retype) = major bump + migration note
  + owner approval.
- Committed logs are never migrated in place (INV-5); replay code must
  understand every committed version.

## 9. Validation

- Every log line validates against `schemas/event.schema.json` (T0, from
  iter-1). The header line (§1) is validated as a separate shape.
- The example below is embedded in the test suite as a fixture — docs and
  schema cannot drift silently.

## 10. Example (canonical — `ev_0007`)

```json
{ "id": "ev_0007", "t": 412, "type": "pickpocket_failed",
  "actor": "pc_01", "target": "npc_guard_01", "cause": "ev_0006",
  "outcome": { "noticed": true },
  "knowledge": [
    { "who": "npc_guard_01", "channel": "saw", "fidelity": "partial",
      "knows": "figure_reaching_for_purse", "at": 412, "source": "ev_0007" },
    { "who": "npc_barkeep_01", "channel": "heard", "fidelity": "vague",
      "knows": "noise_by_the_bar", "at": 412, "source": "ev_0007" } ],
  "state_changes": [
    { "entity": "npc_guard_01", "prop": "suspicion_of.pc_01", "from": 0, "to": 25 },
    { "entity": "pc_01", "prop": "status", "from": "unknown", "to": "suspect" } ],
  "hooks": ["guard_suspicious_of_pc", "possible_document_check"],
  "importance": "medium",
  "provenance": { "seed": 42, "cause_intent": "intent_0006" } }
```

## 11. Extension policy

Adding an event `type` or an `outcome` payload: pack data, no bump. The
event `type` vocabulary and per-type `outcome` payload shapes are declared
by the pack and validated at load (closed per pack — the phase-0 minimum
lint in `docs/blueprint/phase0.md` §1); a type unknown to the pack fails
load loudly. Schema-level enums (`channel`, `fidelity`, `importance`) and
any field in §2–§4 are closed per `schema_version`: touching them = §8
applies. Type-specific payload fields (the DF Legends `hf_died` →
`victim_hfid`/`slayer_hfid` shape) live inside the validated `outcome`
object, never as ad-hoc top-level fields. Multi-parent event groupings (DF
`event_collections` many-to-many) are deferred to phase 3+, arriving with
arcs (P3c) — phase 0 keeps the single-parent `cause` chain.
