# PARSER_SPEC.md — The mode-C Parser Contract v0 (Track A, phase 2)

> The trigger for this spec (`docs/SPECS_BACKLOG.md`: "phase-2 start") has
> fired; it is written from the iter-31 build, not ahead of it.
> Architecture owner: `docs/blueprint/phases.md` §2 (the parser is
> *classification with slots*, never free-form generation). This doc owns
> the boundary's document contracts and the pin/feed wiring; the intent
> record and the front door are `docs/INTENT_SCHEMA.md`'s; the exit
> criterion (≥90% valid intents) is `ROADMAP.md` §2's — §6 here owns only
> the measurement procedure. The narrator boundary's contracts stay with
> `BRIEF_SPEC.md` §7.1 / `VALIDATION_SPEC.md` §7.1.

## 1. The boundary (D-062 — D-055's pattern, applied to the player's text)

The parser is EXTERNAL at dev-time, exactly like the narrator: an
operator reads a parse call file and writes a parse reply file. Since
engine-1's landing (iter-177, D-193) the operator may be the RUNTIME
ENGINE — a llama-server behind the explicit adapter `cli/engine.py`,
answering the same files under a GBNF constraint derived from the
snapshot (§2.1): the doors and their gates are byte-identical either
way (the file contract — the runtime engine is "the operator";
INV-4's standing form: the network surface is exactly the adapter
module). Files are the contract, gitignored runtime artifacts under
`output/parser/`:

    parse_<NNNN>.md          the parser's input: the utterance + the grammar snapshot + the protocol
    parse_reply_<NNNN>.json  the parser's output: {intent} | {question} | {no_intent}

The repo-side half (this spec's subject) is pure: `brief/parser.py`
(document assembly and inspection as functions of (log, pack, ledger) —
same inputs → same call bytes, the D-049 quarantine family) and
`cli/parser.py` (the session door: files, the Simulator handle, cycle
state — periphery, D-046); `brief/gbnf.py` (the snapshot's engine-facing
serialization, §2.1) and `cli/engine.py` (the adapter) join as the
engine-side periphery, never touching the gate.

Player input is data, not instruction (`VISION.md` §5): the parser
produces intents; the simulator decides outcomes. The only cure for
sycophancy is that the world answers.

## 2. The grammar snapshot (the closed target grammar)

`grammar_snapshot(events, pack, ledger)` — the grammar the parser
classifies into, as data:

- **Verbs** — the pack's action intents in declaration order, each with
  its display label (word matching), the `target_required` flag (derived
  from `requires` exactly as the door's own shape gate derives it,
  `core/intent.py::validate_shape`), and the declared fields with their
  pack-derivable constraints:
  - `ticks` → positive integer, when the action declares the drawn-`N`
    duration form (`action["ticks"] == "N"`);
  - `method` → the rules' modifier-table keys (`rules.checks.methods`)
    — the same enum the door's check machinery validates against;
  - `near` → the action's ignition layer's spot list on the actor's
    current location (folded from the log — the same list the completion
    resolver validates against, so grammar and door agree by
    construction);
  - `texture` → a live texture-entry reference, only on texture-capable
    verbs (the pack's `texture` block, INTENT_SCHEMA §3);
  - anything else → an open string the door validates downstream.
  Derivation is pack-data-only (INV-3): a second pack requires zero
  engine changes.
- **Nouns** — the addressable vocabulary: every canon entity (id,
  category, display name) plus every live texture entry (the
  copy-verbatim reference `{entry, scope, slot, value}` and the entry's
  surface prose). **Ghost interactivity is structurally impossible**
  (blueprint §2): any noun the narrator established is parseable by
  construction; a noun that is neither canon nor live texture cannot
  appear in a reply — the parser must take the disambiguation path.

Free-text player mentions never pin at the mediator (zero-LLM capture,
blueprint §1); the parser turns mentions into intents, which then pin
(§5).

### 2.1 The GBNF serialization (engine-1's landing, iter-177/D-193)

`brief/gbnf.py::gbnf_grammar(snapshot)` — the snapshot as GBNF text
(one INV-3-clean pure function over it, CONTRACTS §4.1 D6/I3): the
LLM-facing constraint the adapter rides on the parse requests
(top-level `grammar` param, PRESENTATION_SPEC's mapping). The grammar
is NARROWER than the §4 gate, never wider — grammar-valid output is
gate-valid by construction — and it encodes the door's own shape laws
at the source (the s2c1 lesson): the canon path and the texture path
as SEPARATE per-verb alternatives (one path, never both — the one-path
law), the target enum canon-nouns-only (texture ids are never targets),
the drawn-`N` `ticks` field REQUIRED (the door's accept-time law,
mirrored on the snapshot's `FieldConstraint.required`), empty-enum
fields never offered, non-empty free-text strings (the f1b degenerate
form structurally impossible). The honest guess-within-grammar class
stays untouched (D-192's D5: the grammar fixes validity, never
honesty). `grammar_fingerprint(grammar)` is the D3 manifest's grammar
id (sha256, 16 hex). The dialect laws (measured at b11064, TECH_NOTES
§13.1): rule names carry no underscores (identifiers sanitized),
`"` escapes inside literals (json.gbnf's own forms — control
characters refuse loud), the string/number rules adopt json.gbnf's
proven shapes. The golden fixture `tests/fixtures/parse_gbnf_seed125.gbnf`
(regen: `scripts/regen_parse_gbnf.py`) pins the byte contract; the
station compile check rides the owner's first live run.

## 3. The call document

`parse_call(text, events, pack, ledger)` — the utterance verbatim, the
snapshot, and the protocol; block geometry (one blank line between
sections, BRIEF_SPEC §7.1's family):

    ## player_input
    <the utterance, verbatim>

    ## grammar
    verbs:
      steal "steal" [target required] method=one of: distraction
      take "take" [target required] texture=<a live texture entry>
      wait "wait" ticks=<positive integer>
      drop_break "drop / break" [target required] near=one of: bar, tables, back_wall
    nouns:
      npc_guard_01 (npc) "Doren"
      ...
    texture entries:                # present only when live entries exist
      tex_0000 scene:loc_tavern candles=lit "A few candles ..."

    ## parse_protocol
    reply: ONE JSON object with exactly one alternative —
      {"intent": {"kind": "<verb>", "target": "<noun id>", "fields": {...}}}
      {"question": "<ask the player — never guess>"}
      {"no_intent": "<the utterance carries no world-touching intent>"}
    ... (the closed-grammar clauses, verbatim in the emitted document)

A verb with an empty value enum renders `near=<none available>` — the
field is unusable at that position. Same (log, ledger, pack, text) →
same bytes.

## 4. The reply document (closed; gated at the boundary)

`parse_reply_from_mapping(doc, snapshot)` — exactly ONE alternative:

| Field | Type | Meaning |
|---|---|---|
| `intent` | object | the parsed intent: `kind` (required), `target`?, `fields`? |
| `question` | non-empty string | a disambiguation question — uncertainty is surfaced, never guessed |
| `no_intent` | non-empty string | the utterance carries no world-touching intent |

The gate (loud `ParseError`, caught by the session before anything
feeds — the world never moves on a malformed parse):

- the document is an object, closed, with exactly one alternative key;
- `kind` ∈ the snapshot's verbs; `target` (when given) ∈ the snapshot's
  nouns — an off-grammar target's error message points at the
  disambiguation path;
- `fields` ⊆ the verb's declared fields, with value checks per §2's
  constraints (enum membership, positive integer, the texture
  reference);
- the `texture` field must carry a live entry's `{entry, scope, slot,
  value}` **verbatim** — a fabricated or stale reference is off-grammar.

Every off-grammar family's refusal payload carries the
**nearest-valid menu** (iter-107, the risk-synthesis §4 rider): up to
three grammar tokens ranked by Levenshtein distance (case-folded,
ties by declaration order — deterministic), over both spellings for
kinds (token + display label) and the closed candidate lists for
targets, field names and field values. The menu ranks the grammar, it
never widens it — the re-ask ladder itself stays §7's deferral; the
menu is the fuel both the dev-time operator and the future runtime
ladder patch toward (`brief/parser.py` owns the law;
`tests/test_parser.py` the pins).

The gate deliberately does NOT duplicate door-owned checks — one owner
per law (`core/intent.py::validate_shape`): target-required, the
one-path law (texture XOR target), preconditions, world legality. A
reply that passes the gate but violates those raises the door's loud
`RunnerError`; the session prints it, nothing is corrupted.

## 5. The pin law and the feed

`cli/parser.py::ParserDoor` closes one cycle per utterance:

1. **emit** (`say <text>`) — ledger hygiene first (the contradiction
   window + the scene sync, the same idempotent folds the narrator door
   runs), then the call document. One call awaits one reply.
2. **apply** (`say apply <reply.json>`) — the gate runs against the
   CURRENT snapshot (recomputed; texture that died mid-cycle is
   off-grammar), then:
   - `question` / `no_intent` — surfaced to the player; nothing feeds;
   - `intent` — the parsed intent converts to the step grammar
     (INTENT_SCHEMA §9 — the same conversion the narrator path
     performs), the door re-anchors it at feed time, and **the reference
     IS the pin** (`SceneLedger.pin`, blueprint §1(a) — wired by this
     path's first consumer): the entry pins before the feed, a
     door-rejected attempt still pins, and a failed attempt promotes
     nothing (the entry stays live+pinned — un-pinning does not exist).
     Committed promotions flip their entries exactly like the narrator
     path (`promotions_in` → `mark_promoted`); a take-success IS the
     promotion (D-054).
3. **Off-grammar replies** leave the cycle open — the operator may fix
   the reply file and re-apply (dev-time semantics). The RUNTIME re-ask
   ladder (landed with the engine, iter-177/D-193): the session's
   engine cycle re-asks ONCE with the refusal note as the repair turn
   (the ParseError's own message — the nearest-valid menu riding it,
   iter-107 — is the fuel the engine patches toward; user/assistant/
   user, still grammar-constrained); exhaustion leaves the cycle OPEN
   exactly like dev-time (hand-write the reply — engine down ==
   operator absent). The door's own `RunnerError` (a gate-valid reply
   violating a door-owned law — the s2c1 class) is TERMINAL: the cycle
   was consumed, the world answered with a loud refusal, nothing
   re-asks. A second apply after a consumed call is a loud error, never
   a crash.

Attempts are facts: a well-formed world-impossible intent commits an
`intent_rejected` no-op event — parse validity and world legality are
different axes.

## 6. The exit criterion's measurement (≥90% valid intents)

Per player utterance fed through the door in live sessions: an
utterance counts **valid** when its reply is a boundary-accepted
`intent` alternative (well-formed and on-grammar — it reached the
door). Door outcomes (`intent_rejected`, failed checks) are world
answers, not parse failures. Questions and no-intent verdicts are
honest outcomes, not violations — but a parser that never commits
fails the criterion's spirit; live-session tallies record the
alternative mix (the corpus carries per-session provenance, the
narrator-beats fixture's family). Kill criterion ("else redo the
grammar", ROADMAP §2): the grammar is the pack's verb/field
declarations + the snapshot derivation — redoing it is pack data work,
never engine work (INV-3).

## 7. Deferred (just-in-time — writing these early = scope creep)

| Deferred | Arrives with | Owner |
|---|---|---|
| ~~The runtime inference engine + the C-parser wiring~~ — **LANDED iter-177 (engine-1/D-193)**: the GBNF mapping repo-side (§2.1) + the adapter `cli/engine.py` + the door wiring (`--engine`, the file contract preserved) + the failure→ladder mapping (§5's re-ask; D7's degradation rungs); the runtime re-ask ladder — **LANDED with it** (§5) | — | AGENTS §4 (INV-4's standing form); CONTRACTS §4 the collapsed contract |
| Disambiguation **buttons** (the grammar enumerates the alternatives; today the question is free text) | a frontend consumer (mode C live play) | ROADMAP §2 |
| Multi-intent utterances (one reply carries N intents — today one classification per document) | live-session evidence it is needed | this spec §4 |
| More session volume (the corpus landed iter-32/parse-1 — six live sessions distilled into `tests/fixtures/parse_replies.json` — and grew iter-33/parse-1 batch 2, the owner's corpus-growth call: ten sessions total, 51 combined utterances; **the gate review landed iter-35, D-064 — verdict PASS** (35/35 boundary validity, 0 honest misfires, the §5 protocol re-run reproducing the iter-26 numbers); phase 2 CLOSED, ROADMAP §2; **the engine-1 local corpus landed iter-174** — the deviation families F1–F6 re-distilled at both local models, `tests/fixtures/engine1_deviation_corpus.json` + the Layer-1 suite) | the owner's next call | ROADMAP §5 |

## 8. Versioning

This contract is code-owned (`brief/parser.py`, `cli/parser.py`,
`brief/gbnf.py` (§2.1's serialization), `cli/engine.py` (the adapter);
the snapshot derives from `actions.json`/`rules.json`/the ledger). A
change that renames or removes a field of §3–§5 is an owner-approval
event per `AGENTS.md` §8. Additive constraint kinds, alternative
refinements, or new derived enums = growth, no bump. A change to the
golden grammar's byte contract (§2.1) regenerates the fixture in the
same commit, never silently.
