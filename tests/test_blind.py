"""iter-63 acceptance — the blind-NPC leak suite's phase-4 extension
(blind-1, phase 4; TASKS.md's row: "the blind-NPC leak suite extended to
the phase-4 surfaces — the exit criterion's instrument, the dir-2
precedent: mode B + retrieval outputs under T3's zero-leak law").
Contract owner: `docs/TEST_PLAN.md` §1.3 (T3's phase-4 extension);
architecture owner: `docs/blueprint/phases.md` §4; the exit criterion
itself: `docs/ROADMAP.md` §2 — "0 leaks on the blind-NPC suite", now
read over the phase-4 surfaces.

The instrument (the leak predicates — pure test-side folds over the
same (events, pack) inputs the engine reads, NEVER the engine's own
code paths: a checker that shares the checked code's implementation
cannot catch its bugs):

- `_perceived_lines` — every scene_delta line the knower may lawfully
  render: one line per event the knower perceived (the actor, or a
  record-holder born on the event — the T3 perception law), in the
  render's own byte format. The check is a MULTISET subset: a rendered
  line must be backed by a perceived event, count-for-count (two
  identical events perceived render two identical lines; one perceived
  backs exactly one).
- `_fact_leaks` / `_belief_leaks` — every recalled_facts line maps to
  the knower's own fold: a raw line to a record with the exact
  `(at, channel, fidelity, knows)` quadruple; a belief line to the
  knower's crystallized trait with the exact `(token, sources, cross)`
  triple (the provenance ids are addresses into the log, never prose).
- `_row_leaks` — every retrieval fact row maps to the knower's own
  record (`ref/source/channel/fidelity`); a lore row carries no
  knower. The `knower` query parameter IS known_by — the hard boundary
  made structural in `core/retrieval.py`; this suite measures it.

The four layers:

1. **The offline sweep** (mode B briefs): the 10-seed day1_full family
   (seeds 120..129, the corpus-price witness pattern) + the committed
   golden fixture, EVERY log prefix, EVERY declared actor + the player
   (mode A's own knower) — zero leaks. Every prefix, not every beat:
   the log is append-only, so any prefix is a legal assembly state;
   the strongest statement costs ~2s (measured, the 55-event day).
2. **The retrieval sweep**: the same windows — the REAL query (the
   fresh-window `recall_query`, the mediator's own derivation) and the
   ADVERSARIAL omniscient query (every token every knower holds on the
   WHOLE log — the query that knows everything, including the future):
   every fact row still maps to the named knower's own record; the
   `knower=None` probe never serves a fact. A leak here is the
   known_by boundary failing, not the query being clever. The assembler
   twin: the query is a RANKING signal, never a content source — the
   omniscient query re-ranks the knower's own memory and cannot render
   a foreign record.
3. **The live session wiring** (scene-2's drain): a multi-beat session
   over the cap-raised pack (every tavern NPC drains) — EVERY emitted
   call document is checked against its OWN anchor-addressed log
   prefix (`anchor: N` = the event count at emission; the log is
   append-only, so `events[:anchor]` of the final log IS the
   emission-time log — the document carries its own log address): the
   knowledge blocks re-derived byte-exact with the document's own
   knower + query (composition: the mediator fed the right subject),
   the query line == `recall_query` (the knower's own fresh tokens),
   the retrieval rows == the ladder's top-3 for (query, knower), and
   the leak law independently.
4. **The teeth**: a checker that cannot fail is decoration. Planted
   leaks — a foreign fact line, a foreign belief line, a foreign delta
   line, a foreign retrieval row — are each FLAGGED, and the same line
   passes for the knower who lawfully holds it; the pinned seed-125
   cross-knower divergence (the guard's belief vs the relief's fold)
   is flagged live.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pytest

from brief import assemble_brief, render_brief
from brief.scene import recall_query
from cli.mediator import Mediator
from core.knowledge import KnowledgeView
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import Simulator
from core.pack import Pack, load_pack
from core.retrieval import RetrievalIndex, Retrieved
from core.traits import crystallized_traits
from render.chronicle import display_name

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
GOLDEN = REPO / "tests" / "fixtures" / "plumbing_smoke_seed42.jsonl"
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())
PLAYER = PACK.player_id()
GUARD = "npc_guard_01"
RELIEF = "npc_guard_02"
MAID = "npc_maid_01"
#: The brief sweep's knowers: every declared actor + the player (mode A's
#: own knower — the narrator's brief is the PC's, T3's original subject).
KNOWERS: tuple[str, ...] = tuple(sorted(PACK.rules["brief"]["actors"])) + (PLAYER,)

_DELTA_LINE = re.compile(r"^\[t (\d+)\] (\w+): (.+?)(?: -> (.+))?$")
_FACT_LINE = re.compile(r"^- \[t (\d+), (\w+), (\w+)\] (\S+)$")
_BELIEF_LINE = re.compile(r"^- belief (\S+) \(t (\d+), sources: ([^)]+)\)$")
_DOC_ROW = re.compile(r"^fact (\S+) \((\w+)/(\w+), (\S+)\)$|^lore (\S+)$")


# -- the runs -------------------------------------------------------------------


def _run_day1(seed: int, tmp_path: Path) -> list[EventRecord]:
    """day1_full on a seed (the 10-seed family witness pattern)."""
    log = tmp_path / f"day1_blind_{seed}.jsonl"
    sim = Simulator(PACK, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(dict(DAY1, seed=seed))
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return list(events)


def _golden_events() -> list[EventRecord]:
    _header, events = read_log(GOLDEN, SCHEMA)
    return list(events)


def _blocks(text: str) -> dict[str, list[str]]:
    """Rendered document → block bodies (headers stripped)."""
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:]
            out[current] = []
        elif current is not None and line:
            out[current].append(line)
    return out


# -- the instrument (the leak predicates) ----------------------------------------


def _perceived_lines(
    events: list[EventRecord], pack: Pack, knower: str
) -> Counter[str]:
    """Every scene_delta line the knower may lawfully render — one line
    per event the knower perceived (the actor, or a record-holder born
    on the event), in the render's own byte format. The leak check is a
    multiset subset against this counter (count-for-count)."""
    out: Counter[str] = Counter()
    for event in events:
        perceived = event.actor == knower or any(
            record.who == knower for record in event.knowledge
        )
        if not perceived:
            continue
        line = f"[t {event.t}] {event.type}: {display_name(pack, event.actor)}"
        if event.target is not None:
            line += f" -> {display_name(pack, event.target)}"
        out[line] += 1
    return out


def _delta_leaks(
    events: list[EventRecord], pack: Pack, knower: str, lines: list[str]
) -> list[str]:
    """The scene_delta leak law: every rendered line is backed by a
    perceived event, count-for-count (a line the knower never perceived
    is a leak; a duplicate line beyond the perceived count is a leak)."""
    allowed = _perceived_lines(events, pack, knower)
    leaks: list[str] = []
    for line in lines:
        if line.startswith("[truncated:"):
            continue  # the fill law's marker — budget metadata, never content
        if _DELTA_LINE.match(line) is None:
            leaks.append(f"unparseable delta line: {line}")
        elif allowed[line] <= 0:
            leaks.append(f"delta line the knower never perceived: {line}")
        else:
            allowed[line] -= 1
    return leaks


def _fact_leaks(
    view: KnowledgeView, knower: str, lines: list[str]
) -> list[str]:
    """The recalled_facts raw-line law: every line maps to a record the
    knower holds with the exact (at, channel, fidelity, knows)
    quadruple — what you do not hold, you do not say."""
    held = {
        (record.at, record.channel, record.fidelity, record.knows)
        for record in view.records_of(knower)
    }
    leaks: list[str] = []
    for line in lines:
        if line.startswith("[truncated:"):
            continue
        match = _FACT_LINE.match(line)
        if match is None:
            leaks.append(f"unparseable fact line: {line}")
            continue
        if (int(match[1]), match[2], match[3], match[4]) not in held:
            leaks.append(f"fact the knower does not hold: {line}")
    return leaks


def _belief_leaks(
    events: list[EventRecord], pack: Pack, view: KnowledgeView,
    knower: str, lines: list[str],
) -> list[str]:
    """The belief-line law: every line maps to a belief the knower's own
    fold crystallized — the exact token, the exact provenance ids, the
    exact crossing tick (a belief line is an address into the log, never
    another knower's conclusion)."""
    tick_of = {event.id: event.t for event in events}
    held: set[tuple[str, int, tuple[str, ...]]] = set()
    for trait in crystallized_traits(pack, view, events[-1].t if events else 0):
        if trait.who != knower:
            continue
        cross = max((tick_of.get(sid, 0) for sid in trait.sources), default=0)
        held.add((trait.token, cross, trait.sources))
    leaks: list[str] = []
    for line in lines:
        match = _BELIEF_LINE.match(line)
        if match is None:
            leaks.append(f"unparseable belief line: {line}")
            continue
        parsed = (match[1], int(match[2]), tuple(match[3].split(", ")))
        if parsed not in held:
            leaks.append(f"belief the knower never crystallized: {line}")
    return leaks


def _brief_leaks(
    events: list[EventRecord], pack: Pack, knower: str, text: str
) -> list[str]:
    """The zero-leak law over a rendered brief's two knowledge blocks
    (scene_delta, recalled_facts — the L6 observables blocks are shared
    by law, BRIEF_SPEC §3.9; texture and cards are not knowledge)."""
    blocks = _blocks(text)
    facts = [
        line for line in blocks.get("recalled_facts", [])
        if not line.startswith("- belief ")
    ]
    beliefs = [
        line for line in blocks.get("recalled_facts", [])
        if line.startswith("- belief ")
    ]
    view = KnowledgeView.from_events(events)
    return (
        _delta_leaks(events, pack, knower, blocks.get("scene_delta", []))
        + _fact_leaks(view, knower, facts)
        + _belief_leaks(events, pack, view, knower, beliefs)
    )


def _row_leaks(
    view: KnowledgeView, knower: str, rows: tuple[Retrieved, ...]
) -> list[str]:
    """The retrieval leak law over structured rows: every fact row maps
    to a record the named knower holds (ref/source/at/channel/fidelity);
    a lore row carries no knower (static background, public by design)."""
    held = {
        (record.knows, record.source, record.at, record.channel, record.fidelity)
        for record in view.records_of(knower)
    }
    leaks: list[str] = []
    for row in rows:
        if row.kind != "fact":
            if row.knower is not None:
                leaks.append(f"lore row carries a knower: {row}")
            continue
        if row.knower != knower:
            leaks.append(f"fact row of another knower: {row}")
        elif (row.ref, row.source, row.at, row.channel, row.fidelity) not in held:
            leaks.append(f"fact row the knower does not hold: {row}")
    return leaks


def _doc_row_leaks(
    view: KnowledgeView, pack: Pack, knower: str, rows: list[str]
) -> list[str]:
    """The retrieval leak law over the call document's parsed rows (the
    document carries ref/channel/fidelity/source — no `at`; ref+source
    identify the record). Lore rows must name a declared lore entry."""
    held = {
        (record.knows, record.source, record.channel, record.fidelity)
        for record in view.records_of(knower)
    }
    lore_ids = {entry["id"] for entry in pack.rules["brief"]["lore"]}
    leaks: list[str] = []
    for row in rows:
        match = _DOC_ROW.match(row)
        if match is None:
            leaks.append(f"unparseable retrieval row: {row}")
        elif match[5] is not None:  # the lore arm
            if match[5] not in lore_ids:
                leaks.append(f"lore row names no declared entry: {row}")
        elif (match[1], match[4], match[2], match[3]) not in held:
            leaks.append(f"retrieval row the knower does not hold: {row}")
    return leaks


def _omniscient_query(events: list[EventRecord]) -> str:
    """The adversarial probe: every `knows` token every knower holds on
    the whole log, first-seen order, space-joined — the query that knows
    everything, including what the knower has not learned yet. The
    knower filter must still keep foreign facts out."""
    tokens: list[str] = []
    seen: set[str] = set()
    for event in events:
        for record in event.knowledge:
            if record.knows not in seen:
                seen.add(record.knows)
                tokens.append(record.knows)
    return " ".join(tokens)


# -- layer 1: the offline sweep (mode B briefs) ----------------------------------


@pytest.mark.parametrize("seed", [*range(120, 130), "golden"])
def test_mode_b_zero_leaks_every_prefix_every_knower(
    seed: int | str, tmp_path: Path
) -> None:
    """The exit criterion's instrument, offline form: over the 10-seed
    day1 family + the committed golden fixture, EVERY declared actor's
    brief AND the player's (mode A's own knower) is leak-free at EVERY
    log prefix — every scene_delta line is a perceived event's own line
    (count-for-count), every recalled_facts line (raw or belief) maps to
    the knower's own fold. The suite's core (test_scene.py's selected
    cuts) generalized to the exhaustive sweep: any prefix is a legal
    assembly state (the log is append-only)."""
    events = _golden_events() if seed == "golden" else _run_day1(seed, tmp_path)
    for cut in range(1, len(events) + 1):
        window = events[:cut]
        for knower in KNOWERS:
            brief = render_brief(assemble_brief(window, PACK, knower=knower))
            leaks = _brief_leaks(window, PACK, knower, brief)
            assert not leaks, f"seed {seed} cut {cut} knower {knower}: {leaks}"


def test_the_query_reranks_but_never_injects(tmp_path: Path) -> None:
    """The query is a ranking signal, never a content source (§3.5's
    law, adversarially probed): the omniscient query — every token on
    the whole log, including the future — re-ranks the knower's own
    memory and CANNOT render a foreign record; the recalled_facts block
    stays the knower's own fold, belief lines untouched by the query."""
    events = _run_day1(123, tmp_path)
    omniscient = _omniscient_query(events)
    assert omniscient  # the world holds something to know
    for cut in (13, 16, 20, 25, 30, len(events)):
        window = events[:cut]
        for knower in KNOWERS:
            brief = render_brief(
                assemble_brief(window, PACK, knower=knower, query=omniscient)
            )
            leaks = _brief_leaks(window, PACK, knower, brief)
            assert not leaks, f"cut {cut} knower {knower}: {leaks}"


# -- layer 2: the retrieval sweep -------------------------------------------------


@pytest.mark.parametrize("seed", [*range(120, 130), "golden"])
def test_retrieval_zero_leaks_the_adversarial_query(
    seed: int | str, tmp_path: Path
) -> None:
    """The known_by boundary, measured under maximal adversarial input:
    at every window, every knower the fold holds (not just the declared
    actors — any record-holder) is queried with (a) the REAL query (the
    fresh-window recall_query, the mediator's own derivation) and (b)
    the omniscient query (every token on the whole log) — every fact
    row must map to that knower's own record; lore rows carry no
    knower. The `knower=None` probe never serves a fact: no fact is
    reachable without naming the memory that holds it."""
    events = _golden_events() if seed == "golden" else _run_day1(seed, tmp_path)
    omniscient = _omniscient_query(events)
    for cut in range(1, len(events) + 1):
        window = events[:cut]
        view = KnowledgeView.from_events(window)
        index = RetrievalIndex.build(PACK, window)
        assert index is not None  # the committed pack declares the block
        try:
            for knower in view.knowers():
                for query in (recall_query(window, PACK, knower), omniscient):
                    rows = index.query(query, knower=knower)
                    leaks = _row_leaks(view, knower, rows)
                    assert not leaks, (
                        f"seed {seed} cut {cut} knower {knower} "
                        f"query {query[:40]!r}: {leaks}"
                    )
            assert all(row.kind == "lore" for row in index.query(omniscient))
        finally:
            index.close()


# -- layer 3: the live session wiring --------------------------------------------


def _session_pack() -> Pack:
    """The committed pack with the chorus cap raised to 9 — every tavern
    NPC drains (the full leak surface of the live session)."""
    data = json.loads(json.dumps(dict(PACK.data)))
    data["rules.json"]["brief"]["chorus"]["max_actor_calls"] = 9
    return Pack(data=data)


def _reply(tmp_path: Path, prose: str) -> Path:
    path = tmp_path / "reply.json"
    path.write_text(json.dumps({"prose": prose}), encoding="utf-8")
    return path


def _protocol(text: str) -> tuple[str, int, str | None, list[str]]:
    """The call document's protocol section → (knower, anchor, query,
    retrieval rows). Mode A (no actor line) → the player; the anchor is
    the emission-time event count — the document's own log address
    (append-only: events[:anchor] of the final log IS the log at
    emission)."""
    knower = PLAYER
    anchor = -1
    query: str | None = None
    rows: list[str] = []
    for line in _blocks(text).get("narrator_protocol", []):
        if line.startswith("actor: "):
            knower = line.removeprefix("actor: ")
        elif line.startswith("anchor: "):
            anchor = int(line.removeprefix("anchor: "))
        elif line.startswith("query: "):
            query = line.removeprefix("query: ")
        elif line.startswith("retrieval: "):
            rows.append(line.removeprefix("retrieval: "))
    return knower, anchor, query, rows


def _render_rows(rows: tuple[Retrieved, ...]) -> list[str]:
    """The retrieval rows as the document renders them, prefix stripped
    (`_protocol`'s parse shape; the instrument's own formatter — a
    format drift between the ladder and this pin fails loudly here:
    the pin IS the format)."""
    return [
        f"fact {row.ref} ({row.channel}/{row.fidelity}, {row.source})"
        if row.kind == "fact" else f"lore {row.ref}"
        for row in rows
    ]


def test_the_live_drain_emits_leak_free_calls(tmp_path: Path) -> None:
    """The session wiring under the zero-leak law: a multi-beat session
    over the cap-raised pack (the tavern's four declared actors drain
    per beat, the backyard beat drains none — the empty chorus is the
    honest answer). EVERY emitted call document is verified against its
    own anchor-addressed prefix: the knowledge blocks are byte-exact
    the knower's own assembly (composition — the mediator fed the right
    subject and query), the query line IS recall_query (the knower's
    own fresh tokens), the retrieval rows ARE the ladder's top-3 for
    (query, knower), and the leak law holds independently (the
    predicates, never the assembler's own paths)."""
    pack = _session_pack()
    log = tmp_path / "run.jsonl"
    sim = Simulator(pack, 42, log, SCHEMA, commit="0000000")
    sim.open()
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}])
    mediator = Mediator(sim, pack, SCHEMA, log, tmp_path / "mediator")
    calls: list[Path] = []

    def beat() -> None:
        """One beat: the player's exchange + the full chorus drain (the
        operator accepts every call with plain prose — the drain hands
        each queued NPC its call, the last accept closes the beat)."""
        calls.append(mediator.emit_call())
        result = mediator.apply_reply(_reply(tmp_path, "The room held its breath."))
        while result.call_path is not None:
            calls.append(result.call_path)
            result = mediator.apply_reply(_reply(tmp_path, "Ale and gossip."))
        assert not mediator.beat_open

    beat()  # the tavern: the player + guard, barkeep, drunk, maid
    sim.run_steps([{"intent": "move", "target": "loc_backyard"}])
    beat()  # the backyard: nobody — the player's call alone
    sim.run_steps([{"intent": "move", "target": "loc_tavern"}])
    beat()  # back at the tavern: the chorus again
    sim.close()

    _header, events = read_log(log, SCHEMA)
    assert len(calls) == 11  # 5 + 1 + 5: every drain, the empty chorus
    for path in calls:
        text = path.read_text(encoding="utf-8")
        knower, anchor, query, rows = _protocol(text)
        assert anchor > 0
        window = events[:anchor]
        is_actor = knower != PLAYER
        # composition: the knowledge blocks are the subject's own assembly
        expected = _blocks(render_brief(
            assemble_brief(window, pack, knower=knower, query=query)
        ))
        actual = _blocks(text)
        for block_id in ("scene_delta", "recalled_facts"):
            assert actual[block_id] == expected[block_id], (
                f"{path.name} {block_id}: the document is not the "
                f"knower's own assembly"
            )
        # the leak law, independently of the assembler's paths
        leaks = _brief_leaks(window, pack, knower, text)
        assert not leaks, f"{path.name} knower {knower}: {leaks}"
        # the query line: the knower's own fresh-window tokens
        assert query == (recall_query(window, pack, knower) or None if is_actor
                         else None), f"{path.name}: the query line"
        # the retrieval rows: the ladder's own top-3 for (query, knower)
        index = RetrievalIndex.build(pack, window)
        assert index is not None
        try:
            expected_rows = (
                _render_rows(index.query(query or "", knower=knower))[:3]
                if is_actor else []
            )
        finally:
            index.close()
        assert rows == expected_rows, f"{path.name}: the retrieval rows"
        view = KnowledgeView.from_events(window)
        assert not _doc_row_leaks(view, pack, knower, rows), path.name


# -- layer 4: the teeth -----------------------------------------------------------


def _crafted_events() -> list[EventRecord]:
    """Two knowers, one event: the guard's sighting (a family token) and
    the maid's murmur — plus three maid family tokens below her, so her
    fold crystallizes the belief and his does not (the teeth fixture:
    divergent knowers by construction, never by corpus luck)."""
    records = (
        LoggedKnowledgeRecord(
            who=GUARD, channel="saw", fidelity="partial",
            knows="figure_reaching_for_purse", at=9, source="ev_0002",
        ),
        LoggedKnowledgeRecord(
            who=MAID, channel="heard", fidelity="vague",
            knows="noise_by_the_bar", at=9, source="ev_0002",
        ),
        LoggedKnowledgeRecord(
            who=MAID, channel="told", fidelity="partial",
            knows="figure_reaching_for_purse", at=10, source="ev_0003",
        ),
        LoggedKnowledgeRecord(
            who=MAID, channel="told", fidelity="partial",
            knows="purse_missing", at=11, source="ev_0004",
        ),
    )
    return [
        EventRecord(
            id="ev_0002", t=9, type="take", actor=PLAYER, target=None,
            cause=None, outcome={}, knowledge=records[:2],
            state_changes=(), hooks=(), importance="high",
            provenance={"seed": 1},
        ),
        EventRecord(
            id="ev_0003", t=10, type="rumor_told", actor=MAID, target=GUARD,
            cause=None, outcome={}, knowledge=records[2:3],
            state_changes=(), hooks=(), importance="low",
            provenance={"seed": 1},
        ),
        EventRecord(
            id="ev_0004", t=11, type="rumor_told", actor=MAID, target=GUARD,
            cause=None, outcome={}, knowledge=records[3:4],
            state_changes=(), hooks=(), importance="low",
            provenance={"seed": 1},
        ),
    ]


def test_the_instrument_has_teeth() -> None:
    """A checker that cannot fail is decoration: planted leaks are each
    FLAGGED, and the same line passes for the knower who lawfully holds
    it. The negative control runs on crafted records (hermetic — never
    corpus luck): the guard's sighting line flags for the maid (she
    holds the token told, not saw — the QUAD is the record, not the
    token), the delta line flags for the relief (no record, not the
    actor), the belief line flags for the guard (his fold never
    crystallized), the retrieval row flags for the maid."""
    events = _crafted_events()
    view = KnowledgeView.from_events(events)
    pack = PACK

    guard_line = "- [t 9, saw, partial] figure_reaching_for_purse"
    assert _fact_leaks(view, GUARD, [guard_line]) == []
    assert _fact_leaks(view, MAID, [guard_line]) != []

    delta_line = "[t 9] take: the player"
    assert _delta_leaks(events, pack, GUARD, [delta_line]) == []
    assert _delta_leaks(events, pack, GUARD, [delta_line, delta_line]) != []
    assert _delta_leaks(events, pack, RELIEF, [delta_line]) != []

    beliefs = crystallized_traits(pack, view, 11)
    assert [trait.who for trait in beliefs] == [MAID]  # her fold, not his
    maid_belief = "- belief paranoid_about_thieves (t 11, sources: ev_0002, ev_0003, ev_0004)"
    assert _belief_leaks(events, pack, view, MAID, [maid_belief]) == []
    assert _belief_leaks(events, pack, view, GUARD, [maid_belief]) != []

    guard_row = Retrieved(
        kind="fact", ref="figure_reaching_for_purse", text="x", score=1.0,
        knower=GUARD, source="ev_0002", at=9, channel="saw",
        fidelity="partial",
    )
    assert _row_leaks(view, GUARD, (guard_row,)) == []
    assert _row_leaks(view, MAID, (guard_row,)) != []


def test_the_instrument_flags_a_crossed_knower_live(tmp_path: Path) -> None:
    """The live-fire negative control (the pinned seed-125 divergence):
    the guard crystallizes `paranoid_about_thieves` with HIS sighting
    provenance (ev_0002, ev_0017 — the iter-55 canonical pin); the same
    belief line checked against the relief's fold is a leak (his hearsay
    mint carries one source) — the instrument sees the provenance, not
    just the token. The guard's own brief stays leak-free."""
    events = _run_day1(125, tmp_path)
    guard_brief = _blocks(render_brief(assemble_brief(events, PACK, knower=GUARD)))
    guard_line = guard_brief["recalled_facts"][0]
    assert guard_line == (
        "- belief paranoid_about_thieves (t 360, sources: ev_0002, ev_0017)"
    )
    view = KnowledgeView.from_events(events)
    assert _belief_leaks(events, PACK, view, RELIEF, [guard_line]) != []
    assert _belief_leaks(events, PACK, view, GUARD, [guard_line]) == []
    assert not _brief_leaks(events, PACK, GUARD, render_brief(
        assemble_brief(events, PACK, knower=GUARD)
    ))
