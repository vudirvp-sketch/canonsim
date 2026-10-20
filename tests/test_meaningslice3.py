"""meaning3 — the THIRD meaning slice: the return's claim, the meaning
distribution's substrate measured at the deterministic band (iter-396, the
world track's W8-era content row — the owner's standing delegation «сначала
системы запилить/контентом наполнить, потом за 1 раз всё протестировать»:
the meaning slices the adjacent systems, the live reading band the single
test pass — the corpus filled to its THIRD REGISTER before the band runs;
the register the first two slices never touched: the NON-ECONOMIC claim —
the recognition claimed under the care's own law, the option no other
mechanism expresses (iter-203's winter kin embodiment, the F02 criterion's
mechanical form; the family's own return walk, the lived half W5's
heartbreak station).

The slice's authored half lives in `ANCHOR_REGION.md` §7.3 — the same
mechanical event (the flood-year guest's son at the crossing his father
wintered at, the proof shown where the road can hear), FIVE bounded
position-maps: the claimant (the father's winter answered, his own side
staying forty), the host (the purse barred at her own table, the
acknowledgment's arithmetic), the road's near half (the crossing re-read,
the word the claim's living carrier), the guild's chest (the paper's
silence — no row for a notch), the far road (wordless until the word
rides). This witness owns the DISTRIBUTION'S SUBSTRATE — the half the
deterministic band can measure (both prior slices' own honest remainder;
the live reading band stays open, the §7.1/§7.2 form's own class):

- the PROOF'S SELECTIVE DISCLOSURE: the failed read mints only the vague
  unread marks to the reader (the marks stay marks — wear seen, meaning
  missed); the passed read mints the token to the reader ALONE — the
  leverage gate's own key, the only holder through the read;
- the MINT'S BOUNDARY: the claim's knowledge records land on EXACTLY the
  stair's co-present — the keeper, the heir, the claimant (the actor
  INCLUDED: the counter-record spent aloud, the claimant hears his own
  claim — the told channel's public form, the sale's authorship-exempt
  actor the deliberate contrast);
- the ABSENT MAPS: the whole-log KnowledgeView holding the token on
  exactly the witness set (no ambient spread — the rumor channel its own
  door, never a leak); the mourning token nowhere in the band (the claim
  opens the option, the names stay owed — the duty's performance its own
  beat, never the claim's side effect);
- the PAPERS' SILENCE (the accounts' divergence, the care register's own
  shape): the claim's own event writes NOTHING (the converse beat — the
  knowledge IS the point); the echo writes exactly ONE relation leg (the
  host's side 40→80); ZERO account writes through the band's remainder;
  the crossing's floodpaper TWENTY and the camp's paper SIXTEEN both stand
  — the notch prices care, never coin, held executable at the claim's own
  moment; the claimant's own side stays 40 (the honest state — his own
  winter not spent, no new winter);
- INV-2: the twin's double-run byte-identical (the family's own form).

The claim packet (TEST_PLAN §9):

- Claim: the third meaning slice's distribution rides the canonical
  knowledge boundary and the relation ledger — after the claim, the five
  positions hold materially different states (the proof alone / the
  public record / neither), each bounded exactly as the §7.3 maps claim,
  zero leakage across the boundary, zero account movement, zero pack
  change, zero core.
- Lens(es): the meaning-distribution lens (the same event, five maps, the
  positions' states diverging in KIND — the distribution's substrate
  measured, n=3 for the frontier's claim, the register now non-economic);
  the boundary lens (the token's holders exactly the witnesses; the
  selective disclosure before, the absent maps after); the relation lens
  (the care register's material footprint — ONE kin leg, ZERO accounts —
  against the sale's four account legs, the substrate differing in KIND
  per register).
- Prism: the committed pack itself, seed 80 — the winterkin family's own
  measured instance (the honest fail-then-pass read surface, rng-1's
  recorded corpus price; no twin patching: the family's walk needs no
  macro crossings).
- Oracle: the read and claim events' knowledge records, the whole-log
  KnowledgeView, the echo's state changes, the whole-log account writes,
  the projection's kin and paper reads.
- Falsifier: a second holder minted by the read (the disclosure broken);
  a fourth knower minted by the claim, or the token reaching the camp,
  the manor, the market or the watch in the band (a leak); an account
  written by the claim or the echo (the meaning inverted — the notch
  pricing coin); the floodpaper or the paper moving (the claim taxing the
  institutions); the claimant's side climbing (a new winter minted); the
  twin's bytes diverging (INV-2).
- Expected evidence: the read's holders == {the claimant} through the
  read; the claim's knowers == {the keeper, the heir, the claimant}; the
  whole-log holders == the claim's knowers; the echo == exactly the one
  kin leg 40→80; no account writes at/after the claim; floodpaper 20,
  paper 16, both standing; the T1 self-compare green.
- Observed evidence: CONFIRMED at the measured band (seed 80, the
  winterkin family's own form — the mechanics cited, never re-pinned: the
  claim's door and echo the winterkin witness's own rows).
- Epistemic class: measured, deterministic per seed.
- Disposition: the deterministic half CONFIRMED; the authored band
  PARTIALLY CONFIRMED (the §7.1/§7.2 form's own class — the live reading
  band the slice's open half, the single pass over all three slices the
  owner's future row).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from core.knowledge import KnowledgeView
from core.log import read_log
from core.loop import Simulator
from core.pack import load_pack

REPO = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8"))
PACK_DIR = REPO / "content" / "province_pack"

TORK = "npc_winterkin_01"        # the claimant — the guest's son, the proof's holder
KETTA = "npc_weirkeeper_01"      # the host — the toll-taker, the claim's target
DELLAN = "npc_secondhand_01"     # the road's near half — the heir at the stair
MASTER = "npc_smelter_01"        # the camp's seat — the far road's first wordless
STEWARD = "npc_steward_01"       # Thornmill — the manor's grief, never the stair's
MARKET = "npc_marketmistress_01" # the beam — the market's mistress at Malby
CROWD = "npc_malby_crowd_01"     # the Malby crowd — the far market's wordless
SERGEANT = "npc_sergeant_01"     # the watch — the duty post at Malby
CORPORAL = "npc_corporal_01"     # the garrison — the keep's wordless
PC = "pc_01"                     # the stranger — on the road, never at the stair
POLE = "punt_pole_01"
STAIR = "loc_weirstair"
TOKEN = "the_winter_kin"
VAGUE = "unread_guest_marks_on_the_haft"
MOURNING = "the_drowned_generation_named"
CLAIM_EVENT = "kinmark_claimed"
ECHO_EVENT = "the_edge_answers"

#: the stair's witness set — the claim's co-present knowers at the family's
#: own arithmetic (the keeper at her post, the heir at the stair, the
#: claimant himself — the told channel's public form, the actor included).
WITNESSES = {KETTA, DELLAN, TORK}

#: every position the slice's maps bound — the absent set measured against.
ABSENT = {MASTER, STEWARD, MARKET, CROWD, SERGEANT, CORPORAL, PC}


#: the slice's event: the return's walk (the crofts' man down-country to the
#: crossing his father wintered at), the proof's read (the honest fail-then-
#: pass at the family's own seed), the claim fired once at the stair, a
#: short wait draining the beat — the mourning deliberately NOT performed
#: (the duty stays owed: the claim's moment measured on its own).
CLAIM_STEPS: list[dict[str, Any]] = [
    {"intent": "move", "actor": TORK, "target": "loc_keep"},
    {"intent": "move", "actor": TORK, "target": "loc_riverroad"},
    {"intent": "move", "actor": TORK, "target": STAIR},
    {"intent": "read_kinmark", "actor": TORK, "target": POLE},
    {"intent": "read_kinmark", "actor": TORK, "target": POLE},
    {"intent": "claim_kinmark", "actor": TORK, "target": KETTA},
    {"intent": "wait", "ticks": 10},
]


def _run(tmp_path: Path, log_name: str) -> tuple[list, Simulator]:
    """The committed pack at the winterkin family's own seed — the return
    walk's measured instance (the honest fail-then-pass read surface), the
    family's `_run` form (`tests/test_winterkin.py`'s own helper, repeated
    here because the family's tests stay self-contained — one claim packet,
    one file)."""
    pack = load_pack(PACK_DIR)
    log = tmp_path / log_name
    sim = Simulator(pack, 80, log, SCHEMA, commit="0000000")
    sim.run_playscript({
        "name": log_name, "seed": 80, "pack": "province_pack@0.1",
        "steps": CLAIM_STEPS,
    })
    _, events = read_log(log, SCHEMA)
    return events, sim


# -- the proof's selective disclosure ------------------------------------------------


def test_the_proofs_selective_disclosure(tmp_path: Path) -> None:
    """The distribution's first leg: the proof is the READER'S alone — the
    failed read mints only the vague unread marks (the marks stay marks:
    wear seen, meaning missed — the honest failure surface, the poleseed
    precedent's own law), the passed read mints the token to the claimant
    ALONE (the selective disclosure, the leverage gate's own key). Through
    the read the whole log holds the token on exactly one soul — the
    claimant's; the proof is not yet the road's, not yet the host's."""
    events, sim = _run(tmp_path, "disclosure.jsonl")
    sim.close()
    reads = [e for e in events if e.type.startswith("kinmark_read")]
    assert [e.type for e in reads] == ["kinmark_read_failed", "kinmark_read"]
    failed, proof = reads
    # the marks stay marks: the vague surface only, the reader only
    assert [(k.who, k.knows, k.fidelity) for k in failed.knowledge] == [
        (TORK, VAGUE, "vague"),
    ]
    # the proof: the literal token, the reader ALONE
    assert [(k.who, k.knows, k.fidelity) for k in proof.knowledge] == [
        (TORK, TOKEN, "exact"),
    ]
    # through the read the token has exactly one holder — the claimant
    claim_index = next(
        i for i, e in enumerate(events) if e.type == CLAIM_EVENT
    )
    before = KnowledgeView.from_events(events[:claim_index])
    holders = {w for w in before.knowers() if before.holds(w, TOKEN)}
    assert holders == {TORK}


def test_the_mints_boundary_is_the_stair(tmp_path: Path) -> None:
    """The distribution's second leg: the claim's knowledge records land on
    EXACTLY the stair's co-present — the keeper (the claim's target, the
    proof's subject), the heir (the road's near half at the stair), and the
    claimant himself (the actor INCLUDED — the counter-record spent aloud,
    the claimant hears his own claim; the sale's authorship-exempt actor
    the deliberate contrast, §7.2's own convention). The told channel, the
    exact fidelity — no fourth knower, no vaguer spread."""
    events, sim = _run(tmp_path, "mint.jsonl")
    claims = [e for e in events if e.type == CLAIM_EVENT]
    assert len(claims) == 1  # the slice's one event
    claim = claims[0]
    knowers = {r.who for r in claim.knowledge}
    assert knowers == WITNESSES  # EXACTLY the stair's three — no fourth mint
    assert all(r.knows == TOKEN for r in claim.knowledge)
    assert all(r.channel == "told" for r in claim.knowledge)
    assert all(r.fidelity == "exact" for r in claim.knowledge)
    # the absent maps: no record rides past the stair
    assert not (knowers & ABSENT)
    # the claimant is INCLUDED — the public record's own form
    assert TORK in knowers
    assert sim.projection[TORK]["position"] == STAIR
    assert sim.projection[KETTA]["position"] == STAIR
    assert sim.projection[DELLAN]["position"] == STAIR
    sim.close()


def test_the_absent_maps_stay_wordless(tmp_path: Path) -> None:
    """The distribution's third leg: the whole-log KnowledgeView holds the
    token on EXACTLY the witness set — the boundary holds through the band,
    no ambient spread (the rumor channel its own door, never a leak). The
    camp's seat, the manor's steward, the beam's mistress, the Malby crowd,
    the duty watch, the garrison, the stranger on the road — all wordless
    in this band: the claim's fact stays the stair's until the word rides.
    The mourning token NOWHERE — the claim opens the option, the names
    stay owed (the duty's performance its own beat, never the claim's side
    effect)."""
    events, _sim = _run(tmp_path, "absent.jsonl")
    view = KnowledgeView.from_events(events)
    holders = {w for w in view.knowers() if view.holds(w, TOKEN)}
    assert holders == WITNESSES  # the boundary law: no fourth holder ever
    for absent in ABSENT:
        assert not view.holds(absent, TOKEN)
    # the witnesses hold it — the stair's own three
    for witness in WITNESSES:
        assert view.holds(witness, TOKEN)
    # the mourning not yet performed: the names stay owed in this band
    assert not any(
        view.holds(w, MOURNING) for w in view.knowers()
    )
    assert not any(e.type == "the_names_kept" for e in events)


# -- the papers' silence (the care register's material footprint) ---------------------


def test_the_papers_silence(tmp_path: Path) -> None:
    """The distribution's fourth leg: the claim's material footprint is ONE
    relation leg and ZERO accounts — the care register's own shape, against
    the sale's four account legs (§7.2): the claim's own event writes
    NOTHING (the converse beat — the knowledge IS the point), the echo
    writes exactly the host's kin 40→80 (the acknowledgment's arithmetic,
    the rarity gate intact: the claim answers the generation-old notch, no
    new winter — the claimant's own side stays 40, the honest state). NO
    account prop is written at or after the claim's tick: the crossing's
    floodpaper TWENTY and the camp's paper SIXTEEN both stand — the notch
    prices care, never coin, held executable at the claim's own moment
    (the claim never the chest's business; the debt's fall its own door)."""
    events, sim = _run(tmp_path, "papers.jsonl")
    claims = [e for e in events if e.type == CLAIM_EVENT]
    assert len(claims) == 1
    claim = claims[0]
    # the converse beat: the claim's own event writes nothing
    assert list(claim.state_changes) == []
    # the echo: exactly one relation leg — the host's side completing
    echoes = [e for e in events if e.type == ECHO_EVENT]
    assert len(echoes) == 1
    assert [(c.entity, c.prop, c.from_, c.to_)
            for c in echoes[0].state_changes] == [
        (KETTA, f"pair.{TORK}.kin", 40, 80),
    ]
    # no account written at/after the claim's tick — the papers' silence
    assert not [
        (e.type, c.entity, c.prop)
        for e in events if e.t >= claim.t
        for c in e.state_changes if c.prop.startswith("account.")
    ]
    # the papers stand: the crossing's twenty, the camp's sixteen
    assert sim.projection[KETTA]["account.floodpaper"] == 20
    assert sim.projection[MASTER]["account.paper"] == 16
    # the honest state: the claimant's own side stays forty
    assert sim.projection[TORK][f"pair.{KETTA}.kin"] == 40
    assert sim.projection[KETTA][f"pair.{TORK}.kin"] == 80
    sim.close()


# -- INV-2 (the family's own closing arm) ---------------------------------------------


def test_the_walk_is_deterministic(tmp_path: Path) -> None:
    """The twin's T1 self-compare: the same script twice, byte-identical —
    the distribution's substrate is canon, not chance (the boundary's law
    holds at every replay of the same seed)."""
    _events, sim_a = _run(tmp_path, "det_a.jsonl")
    sim_a.close()
    _events, sim_b = _run(tmp_path, "det_b.jsonl")
    sim_b.close()
    assert (tmp_path / "det_a.jsonl").read_bytes() == (
        tmp_path / "det_b.jsonl").read_bytes()
