"""agenda-1 P2 (iter-420) — the AGENDA VIEW: the dominant drive, the want
it serves, and the door's own status, on the brief's entity cards.

Claim packet (`docs/TEST_PLAN.md` §9):

- Claim: the persona line is a READ of the world the engine already
  holds — the strongest current drive, the authored want, and a status
  that is the door's own evaluator — and it reaches the narrator on every
  beat the person is present (the model has no transcript across beats:
  PRESENTATION_SPEC §4), while a pack with no profile and no spine keeps
  every byte.
- Problem: before this row a brief said WHO is here and what their body
  and voice look like (iter-419), but never what they WANT or whether
  they can act — the narrator could only invent motive (the exact
  invention the file's prose floor refuses).
- Lens: "the read is the engine's own numbers, not a second mechanism" →
  the door's evaluator, the ticker's bar, the pack's authored prose.
- Prism: BASE (the committed pack: the born travellers + the authored
  spines) vs NO-PERSONA (every archetype `want` and every `spine` record
  removed — no want segment anywhere; the drives stay armed, so the
  `drive=` half must survive the ablation).
- Scenario + corpus: the province smoke play (seed 42), the prefix the
  runner holds on the artery (the travellers born at t=360).
- Oracle: `AgendaView` fields (drive/status/want/failing/bar) on the
  committed projection; the brief's card segments; the block's token
  count against its own hard budget.
- Observed (seed 42): drover `scan_the_road:OPEN` bar 40, peddler bar 20,
  carrier bar 10 — all from `look_around` (its `requires` is empty, so
  OPEN is the door's truth); want `the road's own sign read` (the
  archetype's). Ketta — no profile, so no drive, but the authored
  `spine.want` renders (`the crossing kept honest`); Dellan's longer
  authored want renders too. The player renders neither (no want, no
  drive). The card block: 93 of 120 tokens (iter-446's `need` segment added
  three per offered card; iter-420 measured 78 before the board existed).
- Falsifier: a status that disagrees with the door (OPEN while a static
  precondition fails, or BLOCKED while it passes); a want from the wrong
  origin (the record's spine must outrank the archetype's); the card
  line surviving a removed want (the segment would be invented).
- Epistemic class: the read is FACT about the engine's own numbers; the
  NARRATOR's use of it is the same reading measurement iter-419 named.
- Disposition: CONFIRMED at the measured band (seed 42).
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import pytest

from brief.assembler import assemble_brief, render_brief, token_count
from core.agenda import (
    BLOCKED,
    OPEN,
    SATISFIED,
    WANT_MAX_WORDS,
    AgendaView,
    agenda_view,
    agenda_views,
)
from core.fold import initial_projection
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import PackError, load_pack
from core.psyche import materialize_psyche
from core.rng import RngBank
from core.traits import Trait

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)
PACK_DIR = REPO / "content" / "province_pack"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "province_smoke.json")
TRAVELLERS = ("npc_drover_01", "npc_peddler_01", "npc_carrier_01")


def _born_pack() -> tuple[Any, dict[str, dict[str, Any]]]:
    """The committed pack with the three travellers' profiles BORN into a
    fresh projection (the state the brief assembles in after the
    condensation), seed 42."""
    pack = load_pack(PACK_DIR)
    projection = initial_projection(pack.entities)
    for npc in TRAVELLERS:
        birth = materialize_psyche(RngBank(42), pack, projection, npc)
        projection[npc]["psyche"] = birth.to_
    return pack, projection


def _twin(tmp_path: Path, name: str, mutate: Any, templates: Any = None) -> Path:
    """The committed pack copied into tmp and mutated (`rules`, `entities`,
    `actions`) — never a committed edit (PACK_SPEC §8). `templates` (an
    optional callable) exists for the ablations whose vocabulary goes with
    a removed block (iter-429: a turn's emission line)."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    files = {
        key: json.loads((target / f"{key}.json").read_text(encoding="utf-8"))
        for key in ("rules", "entities", "actions")
    }
    mutate(files["rules"], files["entities"], files["actions"])
    for key, data in files.items():
        (target / f"{key}.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    if templates is not None:
        data = json.loads(
            (target / "templates.json").read_text(encoding="utf-8")
        )
        templates(data)
        (target / "templates.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return target


def _run(pack_dir: Path, tmp_path: Path, name: str) -> list[Any]:
    pack = load_pack(pack_dir)
    log = tmp_path / name
    sim = Simulator(pack, SCRIPT["seed"], log, SCHEMA, commit="0000000")
    sim.run_playscript(SCRIPT)
    sim.close()
    _, events = read_log(log, SCHEMA)
    return events


def _walk_start(events: list[Any]) -> list[Any]:
    cut = next(
        index
        for index, event in enumerate(events)
        if event.type == "move"
        and event.actor == "pc_01"
        and event.target == "loc_keep"
    )
    return events[:cut]


# -- the read's laws --------------------------------------------------------


def test_the_status_is_the_doors_own_read() -> None:
    """The three statuses are the door's own answers, never a second
    evaluator: OPEN while the verb's static preconditions pass (the
    travellers' `look_around` has none), SATISFIED once the measure is
    fully met (the flag on the record — the continuity law), BLOCKED with
    the FIRST failing condition named while a static precondition fails
    (a drive whose verb wants the crofts' wood, the traveller on the
    road)."""
    pack, projection = _born_pack()
    for npc in TRAVELLERS:
        view = agenda_view(pack, projection, npc)
        assert view is not None
        assert (view.drive, view.status) == ("scan_the_road", OPEN)
        assert view.failing is None
        assert view.want == "the road's own sign read"  # the archetype's
    bars = [agenda_view(pack, projection, npc).bar for npc in TRAVELLERS]
    assert bars == [40, 20, 10]  # the drawn weights, the ticker's own


def test_a_met_measure_reads_satisfied() -> None:
    """`SATISFIED` is the ticker's continuity law read from the other side.
    The measure reads the EVENT-DRIVEN fold (`trait_held`, iter-439): the
    caller passes the fold read it took, and a held belief collapses the
    bar to 0 and the status to SATISFIED while a traveller without it stays
    OPEN (one measure, one owner)."""
    pack, projection = _born_pack()
    held = (
        Trait(who=TRAVELLERS[0], token="the_road_known", sources=("ev_0001",)),
    )
    view = agenda_view(pack, projection, TRAVELLERS[0], traits=held)
    assert view is not None
    assert (view.status, view.bar, view.failing) == (SATISFIED, 0, None)
    others = agenda_view(pack, projection, TRAVELLERS[1], traits=held)
    assert others is not None
    assert others.status == OPEN  # the belief is the drover's alone
    assert agenda_view(pack, projection, TRAVELLERS[1]).status == OPEN


def test_a_failing_precondition_reads_blocked(tmp_path: Path) -> None:
    """`BLOCKED` names the FIRST failing static condition — the same
    `<noun>.<test>` string the door's rejection event carries. The drive
    is armed on the road wanderer with the smelter's verb (the crofts'
    stacks, the traveller on the river road): `target.same_location`
    fails, and the read says so."""
    def armed_drive(rules: Any, _entities: Any, _a: Any) -> None:
        rules["psyche"]["drives"].append(
            {
                "id": "fire_the_roadside",
                "archetypes": ["the_road_wanderer"],
                "base": 60,
                "max_per_beat": 100,
                "verb": "burn_the_stacks",
                "target": "loc_crofts",
                "measure": [],
            }
        )

    pack = load_pack(_twin(tmp_path, "blocked", armed_drive))
    projection = initial_projection(pack.entities)
    for npc in TRAVELLERS:
        projection[npc]["psyche"] = materialize_psyche(
            RngBank(42), pack, projection, npc
        ).to_
    view = agenda_view(pack, projection, TRAVELLERS[0])
    assert view.drive == "fire_the_roadside"  # bar 60 beats scan's 40
    assert view.status == BLOCKED
    assert view.failing == "target.same_location"


def test_the_dominant_is_the_strongest_bar_and_a_tie_keeps_the_order(
    tmp_path: Path,
) -> None:
    """The dominant drive is the strongest CURRENT bar (`weight x unmet
    deficit`), and a tie keeps the pack's DECLARATION order (INV-2 — never
    a set, never a sort key). Two no-measure appetites on one archetype:
    the declared-first wins the tie, the heavier base wins otherwise (the
    carrier's `scan_the_road` bar is 10 — openness at the low band halves
    the weight)."""
    def appetites(rules: Any, _entities: Any, _a: Any) -> None:
        rules["psyche"]["drives"].append(
            {
                "id": "wander_aimless",
                "archetypes": ["the_road_wanderer"],
                "base": 10,
                "max_per_beat": 100,
                "verb": "look_around",
                "measure": [],
            }
        )

    pack = load_pack(_twin(tmp_path, "tie", appetites))
    projection = initial_projection(pack.entities)
    for npc in TRAVELLERS:
        projection[npc]["psyche"] = materialize_psyche(
            RngBank(42), pack, projection, npc
        ).to_
    tie = agenda_view(pack, projection, TRAVELLERS[2])
    assert (tie.drive, tie.bar) == ("scan_the_road", 10)

    def heavier(rules: Any, entities: Any, _a: Any) -> None:
        appetites(rules, entities, _a)
        rules["psyche"]["drives"][-1]["base"] = 15

    pack = load_pack(_twin(tmp_path, "heavier", heavier))
    projection = initial_projection(pack.entities)
    for npc in TRAVELLERS:
        projection[npc]["psyche"] = materialize_psyche(
            RngBank(42), pack, projection, npc
        ).to_
    heavier_view = agenda_view(pack, projection, TRAVELLERS[2])
    assert (heavier_view.drive, heavier_view.bar) == ("wander_aimless", 15)


def test_the_authored_spine_outranks_the_archetype_want(tmp_path: Path) -> None:
    """The want's precedence is `profile_of`'s own law one slot over: the
    RECORD's authored `spine.want` first (the author's override, AP-9's
    field — its first runtime reader), the drawn archetype's own `want`
    second. An NPC with both renders the author's."""
    pack, projection = _born_pack()
    assert agenda_view(pack, projection, TRAVELLERS[0]).want == (
        "the road's own sign read"
    )

    def authored_spine(rules: Any, entities: Any, _a: Any) -> None:
        for record in entities["npcs"]:
            if record["id"] == TRAVELLERS[0]:
                record["spine"] = {
                    "want": "the bank market reached before the stalls",
                    "need": "the herd sold at a fair weight",
                    "flaw": "the road always pays the debt first",
                    "cause": "a winter that took the herd",
                }
        # AP-8: an authored spine's flaw must be CONSUMED by an urgency
        # entry of the same npc (GHOST without anchors is dead data) —
        # the quietest legal entry. iter-430 (D-282): NOT the drive's own
        # verb — `look_around` for a born road_wanderer is a second
        # autonomous source for the scan, and `psyche._single_carrier`
        # refuses it at load; the entry rides `wait` instead.
        rules["urgencies"]["entries"].append(
            {
                "npc": TRAVELLERS[0],
                "probability_per_beat": 1,
                "intent": {"kind": "wait", "fields": {"ticks": 1}},
                "requires": [],
                "flaw": "the road always pays the debt first",
            }
        )

    own = load_pack(_twin(tmp_path, "spine", authored_spine))
    projection = initial_projection(own.entities)
    for npc in TRAVELLERS:
        projection[npc]["psyche"] = materialize_psyche(
            RngBank(42), own, projection, npc
        ).to_
    view = agenda_view(own, projection, TRAVELLERS[0])
    assert view.want == "the bank market reached before the stalls"
    assert view.drive == "scan_the_road"  # the pursuit is unaffected


def test_a_want_without_a_drive_is_a_line_and_no_more() -> None:
    """An AUTHORED-spine-only person (no profile) has a want and no
    pursuit: the card renders `want=` and no `drive=` (Dellan — Ketta
    left this arm in iter-443, when the content arming gave her
    `the_weir_keeper` and its drive). Neither a want nor a drive renders
    nothing at all (the player)."""
    pack, projection = _born_pack()
    dellan = agenda_view(pack, projection, "npc_secondhand_01")
    assert dellan == AgendaView(
        npc="npc_secondhand_01",
        want="the crossing worked — one on the water, one on the rope",
        drive=None,
        status=None,
        failing=None,
        bar=0,
    )
    assert agenda_view(pack, projection, "pc_01") is None
    views = agenda_views(pack, projection, ("pc_01", "npc_secondhand_01"))
    assert set(views) == {"npc_secondhand_01"}  # the player never renders


# -- the brief's read surface (the witness) ---------------------------------


def test_the_card_renders_the_persona_line(tmp_path: Path) -> None:
    """The consumer law: every present profiled NPC's card carries
    `drive=<id>:<STATUS>` and `want=<phrase>`; an authored-spine NPC
    carries the want alone; the player carries neither; and the whole
    card block stays inside its own hard budget."""
    events = _run(PACK_DIR, tmp_path, "base.jsonl")
    pack = load_pack(PACK_DIR)
    text = render_brief(assemble_brief(_walk_start(events), pack))
    block = (
        text.split("## present_entities", 1)[1]
        .split("## ", 1)[0]
        .strip()
        .splitlines()
    )
    by_entity = {}
    for line in block:
        match = re.match(r"- (npc_\w+|pc_01) ", line)
        if match:
            by_entity[match.group(1)] = line
    assert "drive=scan_the_road:OPEN" in by_entity["npc_drover_01"]
    assert "want=the road's own sign read" in by_entity["npc_drover_01"]
    assert "drive=" not in by_entity["npc_secondhand_01"]
    assert "want=the crossing worked" in by_entity["npc_secondhand_01"]
    assert "drive=" not in by_entity["pc_01"]
    assert "want=" not in by_entity["pc_01"]
    hard = pack.rules["brief"]["blocks"]["present_entities"]["hard"]
    assert sum(token_count(line) for line in block) <= hard


def test_the_ablation_strips_only_the_derived_want(tmp_path: Path) -> None:
    """The derived want is the switch for the BORN half: with every
    archetype `want` removed the born travellers lose `want=` while the
    authored spines keep theirs (the records cannot be dropped — the
    `spine` is all-or-nothing, AP-9, and the cultures' prohibition law
    reads it), and the `drive=` half survives untouched (the pursuit is
    still armed). Stripping the three derived segments from the base
    brief gives the ablated bytes exactly: no other byte moved."""
    base_events = _run(PACK_DIR, tmp_path, "base.jsonl")
    base = render_brief(
        assemble_brief(_walk_start(base_events), load_pack(PACK_DIR))
    )

    def no_derived_want(rules: Any, _entities: Any, _a: Any) -> None:
        for row in rules["psyche"]["archetypes"]:
            row.pop("want", None)
        # iter-429 (D-281): a turn into a wantless role is dead data (the
        # card-coherence lint), so the ablation drops the turn rows with the
        # wants it strips — the born travellers' wants are what this arm
        # measures, and the turn's emission line goes with its rows.
        rules["psyche"].pop("turnings", None)
        rules["psyche"].pop("turning_event", None)

    ablated = render_brief(
        assemble_brief(
            _walk_start(base_events),
            load_pack(
                _twin(
                    tmp_path,
                    "plain",
                    no_derived_want,
                    lambda templates: templates["events"].pop(
                        "role_turned", None
                    ),
                )
            ),
        )
    )
    derived = " want=the road's own sign read"
    assert base.count(derived) == len(TRAVELLERS)
    assert derived not in ablated
    assert "want=the crossing worked" in ablated  # the authored half stays
    assert "drive=scan_the_road:OPEN" in ablated  # the pursuit survives
    assert base.replace(derived, "") == ablated


# -- the lint's refusals ----------------------------------------------------


def test_the_lint_refuses_the_malformed_wants(tmp_path: Path) -> None:
    """Three dead shapes, each refused at LOAD: a non-string want, an
    empty want, and a want longer than the card-budget bound (the want
    rides EVERY present beat's card — its length is a budget law)."""

    def non_string(rules: Any, _e: Any, _a: Any) -> None:
        rules["psyche"]["archetypes"][1]["want"] = 42

    def empty(rules: Any, _e: Any, _a: Any) -> None:
        rules["psyche"]["archetypes"][1]["want"] = "   "

    def too_long(rules: Any, _e: Any, _a: Any) -> None:
        rules["psyche"]["archetypes"][1]["want"] = "word " * (WANT_MAX_WORDS + 1)

    for name, mutate in (
        ("non-string", non_string),
        ("empty", empty),
        ("long", too_long),
    ):
        with pytest.raises(PackError):
            load_pack(_twin(tmp_path, name, mutate))
