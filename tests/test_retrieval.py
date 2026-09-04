"""iter-59 acceptance — the retrieval ladder (retr-1, phase 4, STORE-1;
TASKS.md's row: "SQLite FTS5 bm25() the zero-dep default, the
sqlite-vec probe + fallback chain (vec → pure-Python cosine →
FTS5-only, never an empty result), the deterministic re-ranker
α·recency + β·authority + γ·bm25 + δ·cosine (coefficients as pack
data); hard boundary: dynamic world state = SQL + known_by, never
vectors"). Architecture owner: `docs/blueprint/phases.md` §4 (the
retrieval paragraph); the two contract points `docs/LEGEND_SPEC.md`
§4/§5 fixes for the ladder.

The laws pinned here:

- **The DORMANT law**: the block is declarative-only — nothing in the
  runtime queries the ladder (the consumer is the mediator's keyword
  query, mode B, BRIEF_SPEC §9's deferral), so the corpus price is
  ZERO: the 10-seed day1_full A/B (committed pack vs a block-less
  copy) is 10/10 byte-identical.
- **The known_by boundary (the hard law, structural)**: facts enter
  the index only through the knowledge fold — the `knower` query
  parameter IS the filter. `knower=None` retrieves lore only; a
  knower id retrieves lore plus THAT knower's records, never another
  knower's (the blind-NPC law's retrieval twin, T3).
- **The ladder's rungs (L12 — a rung failure degrades, never breaks)**:
  FTS5 BM25 first (the unicode61 tokenizer splits underscored dry
  tokens into words — token equality, no stemming); the sqlite-vec
  probe (absence = normal operation, D-012 — the extension is probed
  environmental capability, never a dependency) with the pure-Python
  cosine scan as the rung's semantic definition; the keyword floor
  when the SQLite build lacks FTS5.
- **Never an empty result from a rung failure**: the candidate set is
  the union of FTS5 matches and the cosine top-k — with vectors live
  the nearest always ride (the RAG shape); without them a
  no-match query returns the honest empty, an answer, not a failure.
- **The re-ranker**: score = α·recency + β·authority + γ·bm25 +
  δ·cosine, coefficients pack data, ties by construction order
  (rowid: lore in pack declaration order, then facts in event order).
- **The stale law (LEGEND_SPEC §5)**: the build consults
  `stale_reflections` — a scavenged event universe (the log itself
  never drops originals, INV-1) excludes the stale reflection's
  minted record: it is never served.
- **The source-outranks law (LEGEND_SPEC §4, live-fire)**: the seed-123
  guard holds the reflection `sneak_at_work_here` (inferred/exact —
  the HIGHER score under β) and its two provenance-source sightings
  (`figure_reaching_for_purse`, saw/partial); a query retrieving both
  ("purse sneak") orders the SOURCES first — the derived view never
  shadows its own evidence.
- **The lint laws**: the closed key set, non-negative coefficients
  (at least one positive — an all-zero block is dead data), knn_k
  an integer >= 1, vectors keyed by existing lore ids, one dimension,
  finite values only (a NaN poisons the ranking).

Live-fire on the COMMITTED pack (the leg-1 precedent: the block ships
with the engine row) over the measured day1_full seed 123 — the
arming's own live reflections (iter-58) are what the ladder ranks."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

import core.retrieval as retrieval_module
from core.log import EventRecord, LoggedKnowledgeRecord, read_log
from core.loop import Simulator
from core.pack import PackError, load_pack
from core.reflection import stale_reflections
from core.retrieval import RetrievalIndex, cosine_sim

REPO = Path(__file__).resolve().parents[1]
PACK = load_pack(REPO / "content" / "tavern_pack")
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
DAY1 = json.loads((REPO / "tests" / "playscripts" / "day1_full.json").read_text())

GUARD = "npc_guard_01"
PC = "pc_01"
REFLECTION_EVENT = "conclusion_drawn"  # the committed pack's reflection type
INSIGHT = "sneak_at_work_here"


def crafted_pack(
    tmp_path: Path, mutate: Any = None, *, drop_retrieval: bool = False
) -> Any:
    """A committed-pack copy with the `retrieval` block editable (the
    hard_pack pattern); `mutate(rules)` edits the block before the
    load — the lint family's one door. `drop_retrieval` removes the
    block entirely (the DORMANT arm of the A/B)."""
    target = tmp_path / "pack_retrieval"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(REPO / "content" / "tavern_pack", target)
    rules = json.loads((target / "rules.json").read_text(encoding="utf-8"))
    if drop_retrieval:
        rules.pop("retrieval", None)
    elif mutate is not None:
        mutate(rules)
    (target / "rules.json").write_text(
        json.dumps(rules, indent=2), encoding="utf-8"
    )
    return load_pack(target)


def run_seed(pack: Any, seed: int, tmp_path: Path, tag: str) -> list[EventRecord]:
    """Run day1_full on `seed` with `pack` and return the log's events."""
    log = tmp_path / f"day1_{tag}_{seed}.jsonl"
    script = dict(DAY1)
    script["seed"] = seed
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(script)
    sim.close()
    _header, events = read_log(log, SCHEMA)
    return events


def seed123_events(tmp_path: Path) -> list[EventRecord]:
    """The measured recurrence's own event log (the arming's seed)."""
    return run_seed(PACK, 123, tmp_path, "armed")


def built(tmp_path: Path, pack: Any | None = None) -> RetrievalIndex:
    index = RetrievalIndex.build(pack or PACK, seed123_events(tmp_path))
    assert index is not None
    return index


# -- the DORMANT law: declarative-only, zero corpus price -------------------


def test_no_block_builds_none(tmp_path: Path) -> None:
    """The pack's own declaration is the gate (INV-3): a block-less
    pack builds no index — the ladder's DORMANT law, the reflection
    precedent."""
    index = RetrievalIndex.build(
        crafted_pack(tmp_path, drop_retrieval=True), []
    )
    assert index is None


def test_declarative_only_zero_corpus_price(tmp_path: Path) -> None:
    """The block is declarative-only: the 10-seed day1_full A/B
    (committed pack vs a block-less copy, seeds 120..129) — 10/10
    byte-identical logs. The runtime never queries the ladder, so the
    corpus price is zero by construction; the witness measures it,
    never assumes it (the measured-first law)."""
    bare = crafted_pack(tmp_path, drop_retrieval=True)
    for seed in range(120, 130):
        armed_log = tmp_path / f"price_armed_{seed}.jsonl"
        bare_log = tmp_path / f"price_bare_{seed}.jsonl"
        for pack, path in ((PACK, armed_log), (bare, bare_log)):
            script = dict(DAY1)
            script["seed"] = seed
            sim = Simulator(pack, seed, path, SCHEMA, commit="0000000")
            sim.run_playscript(script)
            sim.close()
        assert armed_log.read_bytes() == bare_log.read_bytes(), f"seed {seed}"


# -- the ladder's rungs ------------------------------------------------------


def test_fts5_rung_lore_only_knower_none(tmp_path: Path) -> None:
    """The zero-dep default: FTS5 BM25 over the corpus, token equality
    (no stemming — `toll` does not match `tollmaster`, the tokenizer's
    honest word shape). `knower=None` retrieves LORE only — the hard
    boundary made structural: no fact row is reachable without naming
    the knower whose memory holds it, even though the guard's records
    sit in the same index."""
    index = built(tmp_path)
    hits = index.query("bridge toll")
    assert [hit.ref for hit in hits] == ["salt_road"]
    assert all(hit.kind == "lore" and hit.knower is None for hit in hits)
    index.close()


def test_or_recall_semantics(tmp_path: Path) -> None:
    """Retrieval is recall first: OR-joined terms retrieve every row
    matching ANY term (an AND reading of "salt charter" would return
    nothing — no single row holds both words); the re-ranker sorts,
    bm25 sums what each row actually matched."""
    index = built(tmp_path)
    refs = {hit.ref for hit in index.query("salt charter")}
    assert refs == {"salt_road", "toll_charter"}
    index.close()


def test_knower_filter_the_known_by_boundary(tmp_path: Path) -> None:
    """The `knower` parameter IS known_by: the guard's sightings are
    invisible to the PC's query and vice versa — a knower retrieves
    only their own records plus the lore (the blind-NPC law's
    retrieval twin)."""
    index = built(tmp_path)
    guard_view = index.query("purse", knower=GUARD)
    assert {hit.ref for hit in guard_view} == {"figure_reaching_for_purse"}
    assert {hit.source for hit in guard_view} == {"ev_0002", "ev_0015"}
    pc_view = index.query("purse", knower=PC)
    assert {hit.ref for hit in pc_view} == {"purse_01_present"}
    assert all(hit.knower == PC for hit in pc_view)
    index.close()


def test_honest_empty_without_vectors(tmp_path: Path) -> None:
    """A no-match query on a vector-less corpus returns the honest
    empty — an answer, not a ladder failure (never-empty guards the
    RUNGS, never the truth)."""
    index = built(tmp_path)
    assert index.query("zzz", knower=GUARD) == ()
    assert index.query("zzz") == ()
    index.close()


def test_keyword_floor_engages_without_fts5(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The L12 floor: a SQLite build lacking FTS5 degrades to any-term
    token containment (the same word view — underscores split), γ
    contributes nothing, the ladder never breaks."""
    monkeypatch.setattr(retrieval_module, "_fts5_available", lambda db: False)
    index = built(tmp_path)
    hits = index.query("bridge")
    assert [hit.ref for hit in hits] == ["salt_road"]
    assert hits[0].score == 1.0  # β·1.0 authority, γ·0 — the degradation
    assert index.query("bridge", knower=GUARD) == hits  # lore either way
    index.close()


def test_cosine_scan_rung_and_rag_shape(tmp_path: Path) -> None:
    """The vec rung over craft vectors (the committed pack ships none —
    the embedder is offline pack-authoring, D-012): the pure-Python
    scan computes the top-k, the candidates ride WITHOUT any keyword
    match (the RAG shape — with vectors live a query is never
    empty-handed), δ·cosine lifts the near vector, and the candidates
    are LORE rows only — vectors never touch facts (the hard
    boundary)."""
    near_charter = [1.0, 0.0, 0.0, 0.0]
    query_vector = [0.9, 0.1, 0.0, 0.0]

    def add_vectors(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {
            "salt_road": [0.0, 1.0, 0.0, 0.0],
            "toll_charter": near_charter,
        }

    pack = crafted_pack(tmp_path, add_vectors)
    index = RetrievalIndex.build(pack, [])
    assert index is not None
    assert index.vec_loaded is False  # this environment: the scan answers
    hits = index.query("zzz", vector=query_vector)
    assert [hit.ref for hit in hits] == ["toll_charter", "salt_road"]
    assert hits[0].score == pytest.approx(
        1.0 + cosine_sim(near_charter, query_vector)  # β·1.0 + δ·cos
    )
    assert all(hit.kind == "lore" for hit in hits)
    index.close()


def test_vec_probe_degrades_never_breaks(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A lying probe (an environment that claims the extension but
    cannot create the vec0 table) degrades to the scan — the rung
    failure answer, never a crash."""
    monkeypatch.setattr(retrieval_module, "_probe_vec", lambda db: True)

    def add_vectors(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {
            "salt_road": [1.0, 0.0],
            "toll_charter": [0.0, 1.0],
        }

    pack = crafted_pack(tmp_path, add_vectors)
    index = RetrievalIndex.build(pack, [])
    assert index is not None
    assert index.vec_loaded is False  # the CREATE failed — the scan answers
    refs = [hit.ref for hit in index.query("x", vector=[1.0, 0.0])]
    assert refs == ["salt_road", "toll_charter"]  # the top-k rides whole
    index.close()


def test_query_vector_inert_without_corpus_vectors(tmp_path: Path) -> None:
    """A query vector against a vector-less corpus is INERT (the rung
    is off — the keyword rung answers; the loud errors are for corrupt
    inputs: a dimension mismatch, non-finite values)."""
    index = built(tmp_path)
    assert index.query("bridge", vector=[1.0, 0.0]) == index.query("bridge")
    index.close()


def test_query_vector_dim_and_nan(tmp_path: Path) -> None:
    """The dimension and finiteness guards on a vectorized corpus."""
    def add_vectors(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {"salt_road": [1.0, 0.0], "toll_charter": [0.0, 1.0]}

    pack = crafted_pack(tmp_path, add_vectors)
    index = RetrievalIndex.build(pack, [])
    assert index is not None
    with pytest.raises(ValueError, match="2-d"):
        index.query("x", vector=[1.0])
    with pytest.raises(ValueError, match="non-finite"):
        index.query("x", vector=[float("nan"), 1.0])
    index.close()


# -- the re-ranker -----------------------------------------------------------


def test_recency_the_newer_record_first(tmp_path: Path) -> None:
    """α·recency: the same token held twice (the guard's two sightings,
    t=9 and t=12) — the newer record ranks first (age at the build
    snapshot)."""
    index = built(tmp_path)
    hits = index.query("purse", knower=GUARD)
    assert [hit.source for hit in hits] == ["ev_0015", "ev_0002"]
    assert hits[0].at == 12 and hits[1].at == 9
    index.close()


def test_authority_fidelity_ranks_exact_over_vague(tmp_path: Path) -> None:
    """β·authority: evidential quality — a record's fidelity rank in
    the pack's chain. Crafted: the same tick, three fidelities."""
    def rec(who: str, knows: str, fidelity: str) -> LoggedKnowledgeRecord:
        return LoggedKnowledgeRecord(
            who=who, channel="heard", fidelity=fidelity, knows=knows,
            at=10, source="ev_0009",
        )

    event = EventRecord(
        id="ev_0009", t=10, type="wait", actor=PC, target=None, cause=None,
        outcome={}, knowledge=(rec(GUARD, "alpha_signal", "vague"),
                               rec(GUARD, "beta_signal", "partial"),
                               rec(GUARD, "gamma_signal", "exact")),
        state_changes=(), hooks=(), importance="low", provenance={"seed": 1},
    )
    index = RetrievalIndex.build(PACK, [event])
    assert index is not None
    hits = index.query("signal", knower=GUARD)
    assert [hit.fidelity for hit in hits] == ["exact", "partial", "vague"]
    index.close()


def test_coefficients_are_pack_data(tmp_path: Path) -> None:
    """The balance is pack data (INV-3): α=0 flattens recency — the
    two sightings tie and the construction order wins (the earlier
    event first); α=10 sharpens it (the newer first)."""
    events = seed123_events(tmp_path)

    def zero_alpha(rules: dict[str, Any]) -> None:
        rules["retrieval"]["alpha"] = 0.0

    flat = RetrievalIndex.build(crafted_pack(tmp_path, zero_alpha), events)
    assert flat is not None
    assert [hit.source for hit in flat.query("purse", knower=GUARD)] == [
        "ev_0002",
        "ev_0015",
    ]
    flat.close()
    sharp = built(tmp_path)
    assert [hit.source for hit in sharp.query("purse", knower=GUARD)] == [
        "ev_0015",
        "ev_0002",
    ]
    sharp.close()


def test_tie_break_construction_order(tmp_path: Path) -> None:
    """An exact score tie resolves by rowid — construction order
    (INV-2): lore in pack declaration order, then facts in event
    order."""
    def rec(knows: str, source: str) -> LoggedKnowledgeRecord:
        return LoggedKnowledgeRecord(
            who=GUARD, channel="saw", fidelity="partial", knows=knows,
            at=10, source=source,
        )

    first = EventRecord(
        id="ev_0001", t=10, type="wait", actor=PC, target=None, cause=None,
        outcome={}, knowledge=(rec("tie_token", "ev_0001"),),
        state_changes=(), hooks=(), importance="low", provenance={"seed": 1},
    )
    second = EventRecord(
        id="ev_0002", t=10, type="wait", actor=PC, target=None, cause=None,
        outcome={}, knowledge=(rec("tie_token", "ev_0002"),),
        state_changes=(), hooks=(), importance="low", provenance={"seed": 1},
    )
    index = RetrievalIndex.build(PACK, [first, second])
    assert index is not None
    hits = index.query("tie", knower=GUARD)
    assert [hit.source for hit in hits] == ["ev_0001", "ev_0002"]
    index.close()


def test_determinism_double_build_identical(tmp_path: Path) -> None:
    """Same (pack, events, query) → the same ranked tuple, twice over
    (the read-side purity law; the floats are same-environment
    deterministic, TECH_NOTES §4)."""
    events = seed123_events(tmp_path)
    one = RetrievalIndex.build(PACK, events)
    two = RetrievalIndex.build(PACK, events)
    assert one is not None and two is not None
    assert one.query("purse sneak", knower=GUARD) == two.query(
        "purse sneak", knower=GUARD
    )
    one.close()
    two.close()


# -- LEGEND_SPEC §5: the stale law ------------------------------------------


def test_stale_fold_empty_on_whole_logs(tmp_path: Path) -> None:
    """INV-1: the runtime log never drops originals, so the stale fold
    is empty and every minted reflection serves (the whole-log
    guarantee the scavenged case below breaks on purpose)."""
    events = seed123_events(tmp_path)
    assert stale_reflections(PACK, events) == frozenset()
    index = built(tmp_path)
    assert [hit.ref for hit in index.query("sneak", knower=GUARD)] == [INSIGHT]
    index.close()


def test_stale_law_scavenged_store(tmp_path: Path) -> None:
    """LEGEND_SPEC §5: a derived store after scavenge (the event
    universe minus a provenance event — the log itself is never
    edited, INV-5) must not serve the reflection whose provenance no
    longer resolves. The stale record is excluded at build; the
    surviving source stays retrievable (the honest remainder)."""
    events = seed123_events(tmp_path)
    scavenged = [e for e in events if e.id != "ev_0002"]
    index = RetrievalIndex.build(PACK, scavenged)
    assert index is not None
    assert index.query("sneak", knower=GUARD) == ()  # stale — never served
    purse = index.query("purse", knower=GUARD)
    assert [hit.source for hit in purse] == ["ev_0015"]  # the survivor
    index.close()


# -- LEGEND_SPEC §4: the source-outranks law (live-fire) ---------------------


def test_source_precedence_law_live(tmp_path: Path) -> None:
    """The contract's live-fire: the reflection (inferred/exact — the
    HIGHER score under β·authority) is demoted below BOTH its
    provenance sources when a query retrieves them together. The
    spec's contradiction case, formalized as the precedence that makes
    contradiction harmless: the derived view never shadows its own
    evidence."""
    index = built(tmp_path)
    hits = index.query("purse sneak", knower=GUARD)
    reflection = [hit for hit in hits if hit.ref == INSIGHT]
    sources = [hit for hit in hits if hit.source in ("ev_0002", "ev_0015")]
    assert len(reflection) == 1 and len(sources) == 2
    # the score alone would put the reflection FIRST (authority 1.0
    # over 0.5) — the law, not the score, orders the evidence first
    assert reflection[0].score > sources[0].score
    assert hits.index(reflection[0]) > hits.index(sources[0])
    assert hits.index(reflection[0]) > hits.index(sources[1])
    assert [hit.source for hit in hits] == ["ev_0015", "ev_0002", "ev_0016"]
    index.close()


def test_reflection_alone_ranks_by_score(tmp_path: Path) -> None:
    """The law fires only when the query retrieves BOTH sides: a query
    hitting the reflection alone leaves it ranked by score (the
    retrieval-time law, never a blanket demotion)."""
    index = built(tmp_path)
    hits = index.query("sneak", knower=GUARD)
    assert [hit.ref for hit in hits] == [INSIGHT]
    assert hits[0].source == "ev_0016"
    index.close()


# -- the lint family ---------------------------------------------------------


def test_lint_closed_key_set(tmp_path: Path) -> None:
    def bad(rules: dict[str, Any]) -> None:
        rules["retrieval"]["epsilon"] = 1.0

    with pytest.raises(PackError, match="unknown keys \\['epsilon'\\]"):
        crafted_pack(tmp_path, bad)


def test_lint_coefficients(tmp_path: Path) -> None:
    def negative(rules: dict[str, Any]) -> None:
        rules["retrieval"]["alpha"] = -0.5

    with pytest.raises(PackError, match="alpha must be a non-negative"):
        crafted_pack(tmp_path, negative)

    def all_zero(rules: dict[str, Any]) -> None:
        for key in ("alpha", "beta", "gamma", "delta"):
            rules["retrieval"][key] = 0.0

    with pytest.raises(PackError, match="at least one coefficient"):
        crafted_pack(tmp_path, all_zero)

    def bad_k(rules: dict[str, Any]) -> None:
        rules["retrieval"]["knn_k"] = 0

    with pytest.raises(PackError, match="knn_k"):
        crafted_pack(tmp_path, bad_k)


def test_lint_vectors(tmp_path: Path) -> None:
    def unknown_id(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {"no_such_lore": [1.0]}

    with pytest.raises(PackError, match="no brief.lore entry"):
        crafted_pack(tmp_path, unknown_id)

    def dim_mismatch(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {"salt_road": [1.0, 0.0], "toll_charter": [1.0]}

    with pytest.raises(PackError, match="dimension 1 differs"):
        crafted_pack(tmp_path, dim_mismatch)

    def non_finite(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {"salt_road": [float("nan")]}

    with pytest.raises(PackError, match="finite"):
        crafted_pack(tmp_path, non_finite)

    def empty_table(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {}

    with pytest.raises(PackError, match="non-empty object"):
        crafted_pack(tmp_path, empty_table)

    def empty_vector(rules: dict[str, Any]) -> None:
        rules["retrieval"]["vectors"] = {"salt_road": []}

    with pytest.raises(PackError, match="non-empty list"):
        crafted_pack(tmp_path, empty_vector)


def test_committed_block_pins() -> None:
    """The committed pack's own block: the neutral v0.1 balance (all
    signals equal), the family's cap scale for kNN, no vectors."""
    block = PACK.rules["retrieval"]
    assert block["alpha"] == 1.0
    assert block["beta"] == 1.0
    assert block["gamma"] == 1.0
    assert block["delta"] == 1.0
    assert block["knn_k"] == 8
    assert "vectors" not in block


# -- lifecycle ---------------------------------------------------------------


def test_close_guard(tmp_path: Path) -> None:
    """The derived store dies whole: `close` releases the handle and
    every later call refuses loudly (the resource discipline — the
    Simulator's own close law)."""
    index = built(tmp_path)
    index.close()
    with pytest.raises(RuntimeError, match="closed"):
        index.query("purse")
