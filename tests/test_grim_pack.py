"""pack-1 acceptance — the grim tavern pack (iter-148, D-181): the dark
line as pure pack vocabulary on the untouched engine.

The row's minimal test set, in order:
(1) the consent split — the canonical fact vocabulary (event types) and
    the belief vocabulary (knowledge tokens) disjoint by construction,
    the collision twin refused loudly (the new cross-block lint);
(2) the ladder — the contested delivery, the world's answer keyed on
    the attraction home (the one-knob arm: attraction 70 seeds
    consent_given, the base 45 seeds consent_refused — never a roll),
    the stain landing on the asked either way, the jealousy firing both
    gated arms;
(3) the coerced branch — the leverage chain (read_ticket ->
    leverage_gained -> proposition_coerced), the canonical balance
    (trust breaks fast, fear spikes, D-030), the crafted belief record
    (believes_coerced, the D-008 half), the shame settling;
(4) the economy — res-1's first consumer: the round's transfer conserved
    (6-2 / 30+2), the solvency gate's soft refusal at a drained purse;
(5) since-1's first arming — the pack's own since_lines vocabulary
    renders the re-encounter delta on a crafted part-and-return;
(6) T1 — the same-seed twin byte-identical, the committed golden
    fixture pinned, a different seed diverges (the tavern T1's exact
    shape over the FOURTH pack — the universality claim's corpus half).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from brief.assembler import assemble_brief, render_brief
from core.log import read_log
from core.loop import Simulator, load_playscript
from core.pack import Pack, PackError, load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text())
PACK_DIR = REPO / "content" / "grim_pack"
PACK = load_pack(PACK_DIR)
GOLDEN = REPO / "tests" / "fixtures" / "grim_smoke_seed42.jsonl"
SCRIPT = load_playscript(REPO / "tests" / "playscripts" / "grim_smoke.json")

MAID = "npc_maid_01"
BARKEEP = "npc_barkeep_01"
DRUNK = "npc_drunk_01"
PLAYER = "pc_01"


# -- the harness ---------------------------------------------------------------


def grim_twin(
    tmp_path: Path, name: str, patch: dict[str, Any]
) -> Pack:
    """A committed-grim copy with a JSON patch applied (the crafted-twin
    pattern, the packci family): `patch` maps a file name to a dict of
    top-level-key replacements."""
    target = tmp_path / name
    shutil.copytree(PACK_DIR, target)
    for file_name, repl in patch.items():
        data = json.loads((target / file_name).read_text(encoding="utf-8"))
        data.update(repl)
        (target / file_name).write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
    return load_pack(target)


def _npc_patch(npc_id: str, mutate: dict[str, Any]) -> dict[str, Any]:
    """An entities.json patch that rewrites one npc record's fields."""
    entities = json.loads((PACK_DIR / "entities.json").read_text(encoding="utf-8"))
    for npc in entities["npcs"]:
        if npc["id"] == npc_id:
            npc.update(mutate)
            break
    return {"entities.json": entities}


def run(
    tmp_path: Path, pack: Pack, steps: list[dict[str, Any]],
    name: str, seed: int = 42,
) -> list[Any]:
    log = tmp_path / f"{name}.jsonl"
    sim = Simulator(pack, seed, log, SCHEMA, commit="0000000")
    sim.run_playscript(
        {"name": name, "seed": seed, "pack": "grim_pack@0.1", "steps": steps}
    )
    _, events = read_log(log, SCHEMA)
    return events


def by_type(events: list[Any], *types: str) -> list[Any]:
    return [event for event in events if event.type in types]


def prop(events: list[Any], entity: str, prop_name: str) -> Any:
    """The last state_change value written to a prop (the folded read)."""
    value = None
    for event in events:
        for change in event.state_changes:
            if change.entity == entity and change.prop == prop_name:
                value = change.to_
    return value


#: the court-path probe: enter, one flirt (the +5 reception), ask.
LADDER: list[dict[str, Any]] = [
    {"intent": "move", "target": "loc_tavern"},
    {"intent": "flirt", "target": MAID},
    {"intent": "proposition", "target": MAID},
]


# -- (1) the consent split -----------------------------------------------------


def test_the_fact_and_belief_vocabularies_are_disjoint() -> None:
    """The canonical half (consent_given / consent_refused /
    proposition_coerced — event types, what the world DID) never names a
    belief token (believes_coerced — what someone HOLDS, possibly
    distorted): the D-175 (5) split held by the pack's own vocabulary."""
    from core.packlint.admission import AdmissionLint
    from core.packlint.shared import literal_knows_tokens

    data = {
        "actions.json": json.loads(
            (PACK_DIR / "actions.json").read_text(encoding="utf-8")
        ),
        "entities.json": json.loads(
            (PACK_DIR / "entities.json").read_text(encoding="utf-8")
        ),
        "rules.json": json.loads(
            (PACK_DIR / "rules.json").read_text(encoding="utf-8")
        ),
        "templates.json": json.loads(
            (PACK_DIR / "templates.json").read_text(encoding="utf-8")
        ),
    }
    lint = AdmissionLint(data)
    beliefs = literal_knows_tokens(data)
    emission = lint._emission_witnesses()
    assert not emission & beliefs, (
        "the grim pack conflates fact and belief vocabulary"
    )
    # the split's own names: the canonical facts are event types, the
    # belief half is the re-worded record — never the same token
    assert "consent_given" in emission
    assert "proposition_coerced" in emission
    assert "believes_coerced" in beliefs
    assert "believes_coerced" not in emission
    assert "proposition_coerced" not in beliefs


def test_the_collision_twin_is_refused_loudly(tmp_path: Path) -> None:
    """The negative arm: a crafted twin whose belief record re-uses the
    canonical event type's token dies at load naming the split — the
    lint is live, never vacuous."""
    actions = json.loads(
        (PACK_DIR / "actions.json").read_text(encoding="utf-8")
    )
    for action in actions["actions"]:
        if action["intent"] == "flirt":
            action["knowledge"]["success"][0]["knows"] = "flirt_exchanged"
    try:
        grim_twin(tmp_path, "collision", {"actions.json": actions})
    except PackError as exc:
        assert "fact/belief vocabulary split" in str(exc)
        assert "flirt_exchanged" in str(exc)
    else:
        raise AssertionError("the collision twin loaded — the split is dead")


# -- (2) the ladder ------------------------------------------------------------


def test_the_answer_is_keyed_on_the_attraction_home(tmp_path: Path) -> None:
    """The one-knob arm (the claim packet's prism): the SAME script, the
    SAME seed — only the maid's seeded attraction differs. At 70 the ask
    lands consent_given with the intimacy shift (the canonical
    consented fact); at the committed 45 (+5 reception = 50) it lands
    consent_refused with her anger. Consent is the world's reply, never
    the asker's roll."""
    high = grim_twin(
        tmp_path, "high", _npc_patch(
            MAID, {"relations": {
                "reputation": 45, "trust": 50, "fear": 0,
                "attraction": 70, "intimacy": 10, "loyalty": 55,
            }}
        )
    )
    high_events = run(tmp_path, high, LADDER, "high")
    assert by_type(high_events, "consent_given")
    assert not by_type(high_events, "consent_refused")
    # the canonical consented fact: her intimacy +20 toward the asker
    assert prop(high_events, MAID, "relations.intimacy") == 30

    low_events = run(tmp_path, PACK, LADDER, "low")
    assert by_type(low_events, "consent_refused")
    assert not by_type(low_events, "consent_given")
    assert prop(low_events, MAID, "status.anger") == 10
    # the base run's attraction after the reception: 45 + 5 = 50 — the
    # honest read the refusal keyed on
    assert prop(low_events, MAID, "relations.attraction") == 50


def test_the_stain_lands_on_the_asked_either_way(tmp_path: Path) -> None:
    """The ask's public cost is hers whether the answer is yes or no
    (D-030's asymmetry): the reputation entry fires on proposition_made
    itself — the attraction home selects her from the witnesses."""
    for name, pack in (("yes-arm", grim_twin(
            tmp_path, "stain_high", _npc_patch(
                MAID, {"relations": {
                    "reputation": 45, "trust": 50, "fear": 0,
                    "attraction": 70, "intimacy": 10, "loyalty": 55,
                }}
            )
        )), ("no-arm", PACK)):
        events = run(tmp_path, pack, LADDER, f"stain_{name}")
        stained = by_type(events, "reputation_stained")
        assert stained, f"{name}: the stain never fired"
        assert prop(events, MAID, "relations.reputation") == 40


def test_the_jealousy_fires_both_gated_arms(tmp_path: Path) -> None:
    """The bond-gated barkeep (+10) and the desire-gated drunk (+15):
    the gates read each candidate's OWN pair home toward the maid — the
    long intimacy and the unanswered attraction, never the bystander."""
    events = run(tmp_path, PACK, LADDER, "jealousy")
    smolders = by_type(events, "jealousy_smolders")
    assert len(smolders) == 2  # one flirt, both gated arms
    assert prop(events, BARKEEP, "status.anger") == 20  # 10 seed + 10 bond-gated
    assert prop(events, DRUNK, "status.anger") == 35  # 20 seed + 15 desire-gated


# -- (3) the coerced branch ----------------------------------------------------


def test_the_leverage_chain_and_the_canonical_coerced_fact(
    tmp_path: Path,
) -> None:
    """The corner path end to end: the ticket read mints the reader's
    cluster (the secrets registry), the coerced proposition spends it —
    the canonical fact (the balance: trust from neutral 50-25, fear
    50+25, D-030's break-fast) plus the crafted belief record (the
    D-008 half, exact, told) plus the shame settling (+10)."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "read_ticket", "target": "pawn_ticket_01"},
        {"intent": "proposition_coerce", "target": MAID},
    ]
    events = run(tmp_path, PACK, steps, "coerce")
    # the chain: the read's exact record -> the leverage mint
    assert by_type(events, "ticket_read")
    gained = by_type(events, "leverage_gained")
    assert len(gained) == 1
    assert gained[0].actor == PLAYER and gained[0].target == MAID
    # the spend: the canonical fact + the stamped cluster (the fact
    # event's own id — the log's only view of the spent cluster)
    coerced = by_type(events, "proposition_coerced")
    assert len(coerced) == 1
    assert coerced[0].outcome["cluster"] == gained[0].id
    # the balance: her directed homes toward the asker, from neutral
    assert prop(events, MAID, "pair.pc_01.trust") == 25
    assert prop(events, MAID, "pair.pc_01.fear") == 75
    # the belief half: the subject's own exact record, never the fact's
    # token (the split's runtime face)
    records = [
        record for record in coerced[0].knowledge
        if record.who == MAID
    ]
    assert [record.knows for record in records] == ["believes_coerced"]
    assert records[0].channel == "told"
    # the aftermath: the shame settles on the home carrier
    assert by_type(events, "shame_settles")
    assert prop(events, MAID, "status.shame") == 20


def test_the_coerced_asking_without_leverage_dies_at_the_door(
    tmp_path: Path,
) -> None:
    """The leverage test IS the door (social-1b's law): no cluster, no
    corner — the attempt is a fact (intent_rejected), never a write."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "proposition_coerce", "target": MAID},
    ]
    events = run(tmp_path, PACK, steps, "no_leverage")
    assert not by_type(events, "proposition_coerced")
    rejections = [
        event for event in by_type(events, "intent_rejected")
        if event.outcome.get("action") == "proposition_coerce"
    ]
    assert len(rejections) == 1
    assert "leverage_over" in rejections[0].outcome["failed_test"]


# -- (4) the economy -----------------------------------------------------------


def test_the_round_transfers_and_conserves(tmp_path: Path) -> None:
    """res-1's first consumer: two coins leave the purse and land in the
    till — the conservation oracle exact (6-2 / 30+2), the verb's event
    the engine constant, the room's warmth the reaction."""
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "buy_round", "target": "loc_tavern"},
    ]
    events = run(tmp_path, PACK, steps, "round")
    transferred = by_type(events, "account_transferred")
    assert len(transferred) == 1
    assert prop(events, PLAYER, "account.coin") == 4
    assert prop(events, "loc_tavern", "account.coin") == 32
    assert by_type(events, "generosity_noted")


def test_the_drained_purse_dies_soft_at_the_door(tmp_path: Path) -> None:
    """The solvency gate's soft arm: a one-coin purse cannot buy a
    two-coin round — the rejection is the fact, the stock never moves."""
    drained = grim_twin(
        tmp_path, "drained", _npc_patch(PLAYER, {"accounts": {"coin": 1}})
    )
    steps = [
        {"intent": "move", "target": "loc_tavern"},
        {"intent": "buy_round", "target": "loc_tavern"},
    ]
    events = run(tmp_path, drained, steps, "drained")
    assert not by_type(events, "account_transferred")
    rejections = [
        event for event in by_type(events, "intent_rejected")
        if event.outcome.get("action") == "buy_round"
    ]
    assert len(rejections) == 1
    assert "account_at_least" in rejections[0].outcome["failed_test"]
    # the stock never moved: no account event wrote it (the seeded 1 is
    # pack data — the fold never saw a write)
    assert not [
        change for event in events for change in event.state_changes
        if change.prop == "account.coin"
    ]


# -- (5) since-1's first arming ------------------------------------------------


def test_the_since_lines_render_the_re_encounter_delta(
    tmp_path: Path,
) -> None:
    """The armed vocabulary is the pack's own (not the test's injection):
    a crafted part-and-return (the test_since harness — the maid is out
    of the active zone while the pc is away, the scene LOD's own law, so
    the apart-window change is crafted exactly as the fold's contract
    pins it) — the return's brief carries the shame segment and the
    heard segment on her card, the position family on the scene read.
    The machinery is since-1's (test_since.py); THIS test pins the
    GRIM pack's own since_lines declaration rendering."""
    from core.log import EventDraft, EventLogWriter, KnowledgeRecord, StateChange

    log = tmp_path / "since.jsonl"
    writer = EventLogWriter(log, SCHEMA)
    writer.write_header(seed=42, commit="0000000", pack="grim_pack@0.1")
    specs = [
        {"t": 10, "type": "probe_move", "actor": PLAYER,
         "target": "loc_tavern",
         "state_changes": [(PLAYER, "position", "loc_street", "loc_tavern")]},
        {"t": 20, "type": "probe_move", "actor": PLAYER,
         "target": "loc_street",
         "state_changes": [(PLAYER, "position", "loc_tavern", "loc_street")]},
        # her shame shifts while apart (the decay's shape)
        {"t": 30, "type": "probe_decay", "actor": "world",
         "state_changes": [(MAID, "status.shame", 10, 15)]},
        # the reader hears about her while apart
        {"t": 35, "type": "probe_talk", "actor": BARKEEP,
         "knowledge": [(PLAYER, "told", "partial", f"{MAID}_cornered", 35)]},
        # she moves while apart (the position transfer's surface)
        {"t": 37, "type": "probe_move", "actor": MAID,
         "target": "loc_backyard",
         "state_changes": [(MAID, "position", "loc_tavern", "loc_backyard")]},
        {"t": 40, "type": "probe_move", "actor": PLAYER,
         "target": "loc_backyard",
         "state_changes": [(PLAYER, "position", "loc_street", "loc_backyard")]},
    ]
    records = []
    cause: str | None = None
    for spec in specs:  # cause-chained through the real writer
        record = writer.append(EventDraft(
            t=spec["t"], type=spec["type"], actor=spec["actor"],
            cause=cause, outcome={}, provenance={"seed": 42},
            target=spec.get("target"),
            state_changes=tuple(
                StateChange(*triplet) for triplet in spec.get("state_changes", ())
            ),
            knowledge=tuple(
                KnowledgeRecord(*quad) for quad in spec.get("knowledge", ())
            ),
        ))
        records.append(record)
        cause = record.id
    writer.close()
    assert records
    text = render_brief(assemble_brief(records, PACK))
    lines = text.splitlines()
    start = lines.index("## present_entities")
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if line.strip():
            body.append(line)
    maid_line = next(
        line for line in body if line.startswith(f"- {MAID}")
    )
    assert "since=" in maid_line
    assert "shame 10->15" in maid_line  # the apart-window prop endpoint
    assert "last seen at" in maid_line  # the position family
    assert "cornered" in maid_line  # the heard family


# -- (6) T1 — determinism over the fourth pack ---------------------------------


def test_two_runs_are_byte_identical(tmp_path: Path) -> None:
    first = tmp_path / "a.jsonl"
    second = tmp_path / "b.jsonl"
    for name in (first, second):
        sim = Simulator(PACK, SCRIPT["seed"], name, SCHEMA, commit="0000000")
        sim.run_playscript(SCRIPT)
    assert first.read_bytes() == second.read_bytes()


def test_fresh_run_matches_committed_golden(tmp_path: Path) -> None:
    fresh = tmp_path / "fresh.jsonl"
    sim = Simulator(PACK, SCRIPT["seed"], fresh, SCHEMA, commit="0000000")
    result = sim.run_playscript(SCRIPT)
    assert fresh.read_bytes() == GOLDEN.read_bytes()
    assert result.fingerprint == 8  # the check draws the smoke run takes


def test_different_seed_diverges(tmp_path: Path) -> None:
    other = tmp_path / "other.jsonl"
    sim = Simulator(PACK, 43, other, SCHEMA, commit="0000000")
    sim.run_playscript(dict(SCRIPT, seed=43))
    assert other.read_bytes() != GOLDEN.read_bytes()


def test_committed_fixture_schema_version_matches_current_schema() -> None:
    header_line = GOLDEN.read_text(encoding="utf-8").splitlines()[0]
    header = json.loads(header_line)
    schema_id = SCHEMA.get("$id", "")
    assert header["schema_version"] == schema_id.rsplit("/", 1)[-1]
