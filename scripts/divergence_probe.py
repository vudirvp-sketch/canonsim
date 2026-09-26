"""The future-divergence minimal-pair probe (div-1, iter-259, D-235 —
intake-40's P0-6, the owner's «и прочими» call opening the parked row).

Answers the §9 first-prism question the metric-level arms cannot: not
"are the outcome DISTRIBUTIONS different" (the balance harness's paired
Δ) but "WHERE did this pair of futures diverge, WHY (the causal
ancestry at the divergence point), and does the divergence persist".
One same-seed minimal pair over the existing balance-harness arm family:

    BASE      the committed pack, directors on
    PERTURBED --directors-off (the T8 landed instance, the default)
              | --pacing-off | --systems-minus <name>   (the tavern arm
              family; the materializers are balance_harness's own —
              imported, never duplicated: the flag family's single owner)

The comparison rides ssi-7's oracle (`scripts/semantic_diff.py`,
deterministic, zero shared code with the engine): the verdict + the
verdict's own report lines come from `compare()` — the §1.4 form with
BOTH arms' run-side RngBank fingerprints supplied — and the probe's own
bounded walk over `parse_log` produces the records the oracle's capped
report deliberately does not carry:

    first divergence   the first stream position where the futures
                       disagree (anchors named; a one-side event named
                       for the side that has it)
    causal path        the divergent event's `cause` ancestry walked
                       back through ITS OWN log, bounded 8 links — why
                       this event exists at this tick
    persistence        over the positions after the divergence: how many
                       stay divergent, whether the streams re-converge,
                       whether the divergence persists to the horizon,
                       the divergent event families, the final
                       projection delta (the state-level persistence)

The walk's equality semantics is the oracle's own `_json_equal`
(imported, never re-implemented — the kind-strict numeric/bool/key-order
law single-owned by the checker). Pure stdlib + core's public Simulator
for the arms; periphery (scripts/, D-046); read-only over the pack; the
arm logs land under the gitignored output/ dir.

Exit codes: 0 = the pair is semantically equal (the null control); 1 =
divergence found (the records on stdout); 2 = input error — loud, never
a silent skip (SSI-N006).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import balance_harness  # noqa: E402  (the arm materializer's owner)
from semantic_diff import (  # noqa: E402
    ANCHOR_FIELDS,
    SemanticDiff,
    _json_equal,
    compare,
    format_report,
    parse_log,
)

from core.fold import fold, initial_projection  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator, load_playscript  # noqa: E402
from core.pack import Pack, load_pack  # noqa: E402

__all__ = [
    "DEFAULT_SCRIPT",
    "MAX_CAUSAL_LINKS",
    "DivergenceRecords",
    "ProbeInputError",
    "probe",
    "render_report",
    "main",
]

#: The T8 gate script — the landed minimal-pair instance's own scenario
#: (TEST_PLAN §1.2; the director's document_check release is the pinned
#: first divergence).
DEFAULT_SCRIPT: Final[Path] = REPO / "tests" / "playscripts" / "day1_full.json"
#: The causal-path walk bound (the records stay readable; the full
#: ancestry stays computable from the arm logs).
MAX_CAUSAL_LINKS: Final[int] = 8
#: Report caps: the divergent-family and projection-delta lines shown.
MAX_FAMILY_LINES: Final[int] = 12
MAX_PROJECTION_LINES: Final[int] = 12

SCHEMA = json.loads(
    (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
)


class ProbeInputError(RuntimeError):
    """A bad probe invocation (exit 2): an unknown systems-minus block,
    a pacing/systems-minus arm on a non-tavern script, an unreadable
    script."""


@dataclass(frozen=True)
class DivergenceRecords:
    """The bounded records of one minimal pair's semantic future
    comparison — the probe's own output; the oracle's verdict rides
    separately."""

    base_log: Path
    pert_log: Path
    base_events: int
    pert_events: int
    base_fingerprint: int
    pert_fingerprint: int
    base_last_tick: int
    pert_last_tick: int
    #: (index, tick, side, id, type) — side "base"/"pert" for a
    #: one-side event, "both" when the positions disagree in content
    first_index: int | None = None
    first_tick: int | None = None
    first_side: str | None = None
    first_id: str | None = None
    first_type: str | None = None
    first_anchors: tuple[str, ...] = ()
    #: the divergent event's cause ancestry, oldest last: (id, t, type)
    causal_path: tuple[tuple[str, int, str], ...] = ()
    #: persistence: positions after the divergence, how many divergent,
    #: the last divergent index, whether it persists to the horizon,
    #: whether the streams re-converged (a fully-equal suffix)
    positions_after: int = 0
    divergent_positions: int = 0
    last_divergent_index: int | None = None
    persists_to_horizon: bool = False
    re_converged: bool = False
    #: the event-family counter delta (pert - base) + the final
    #: projection delta lines
    family_delta: tuple[str, ...] = ()
    projection_delta: tuple[str, ...] = ()
    projection_delta_count: int = 0


def _run_arm(
    script: dict[str, Any],
    seed: int,
    pack: Pack,
    directors: bool,
    out_dir: Path,
    tag: str,
) -> tuple[Path, int, int]:
    """One arm's fresh run (same seed, same script, the pack/director
    flag the arm names): the log path, the RngBank fingerprint, the last
    tick. Deterministic by construction (INV-2)."""
    log = out_dir / f"div_{script['name']}_{tag}.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(
        pack, seed, log, SCHEMA, commit="0000000",
        director_enabled=directors,
    )
    result = sim.run_playscript(dict(script, seed=seed))
    sim.close()
    return log, result.fingerprint, result.last_tick


def _first_divergence(
    base_events: list[dict[str, Any]], pert_events: list[dict[str, Any]]
) -> tuple[int, dict[str, Any], dict[str, Any] | None] | None:
    """The first position where the streams disagree (deep, kind-strict
    equality — the oracle's own semantics). Returns the index, the
    side-that-has-it event (base preferred on one-side rows), and the
    other side's event when both exist."""
    for index in range(max(len(base_events), len(pert_events))):
        if index >= len(pert_events):
            return index, base_events[index], None
        if index >= len(base_events):
            return index, pert_events[index], None
        if not _json_equal(base_events[index], pert_events[index]):
            return index, base_events[index], pert_events[index]
    return None


def _causal_path(
    events: list[dict[str, Any]], start: dict[str, Any]
) -> tuple[tuple[str, int, str], ...]:
    """Walk one event's `cause` ancestry back through its own log,
    bounded by MAX_CAUSAL_LINKS — the divergence point's why-chain."""
    by_id = {str(event.get("id")): event for event in events}
    chain: list[tuple[str, int, str]] = [
        (str(start.get("id")), int(start.get("t", 0)), str(start.get("type")))
    ]
    current = start
    for _ in range(MAX_CAUSAL_LINKS):
        cause = current.get("cause")
        if not isinstance(cause, str):
            break
        parent = by_id.get(cause)
        if parent is None:
            break
        chain.append(
            (str(parent.get("id")), int(parent.get("t", 0)),
             str(parent.get("type")))
        )
        current = parent
    return tuple(chain)


def _projection_delta(
    pack: Pack, base_log: Path, pert_log: Path
) -> tuple[tuple[str, ...], int]:
    """The final state-level persistence: the projection props that
    differ between the arms (the engine's own fold — the probe compares
    futures through the public API, never a private re-derivation)."""
    _, base_events = read_log(base_log, SCHEMA)
    _, pert_events = read_log(pert_log, SCHEMA)
    base = fold(base_events, initial_projection(pack.entities))
    pert = fold(pert_events, initial_projection(pack.entities))
    lines: list[str] = []
    for entity in sorted(set(base) | set(pert)):
        props_a = dict(base.get(entity, {}))
        props_b = dict(pert.get(entity, {}))
        for prop in sorted(set(props_a) | set(props_b)):
            if not _json_equal(props_a.get(prop), props_b.get(prop)):
                lines.append(
                    f"{entity}.{prop}: {props_a.get(prop)!r} != "
                    f"{props_b.get(prop)!r}"
                )
    return tuple(lines), len(lines)


def probe(
    script: dict[str, Any],
    base_pack: Pack,
    pert_pack: Pack,
    *,
    base_directors: bool,
    pert_directors: bool,
    seed: int | None = None,
    out_dir: Path | None = None,
) -> tuple[DivergenceRecords, SemanticDiff]:
    """Run one minimal pair and derive the bounded divergence records +
    the oracle's own §1.4 verdict (fingerprints supplied — the
    latent-divergence axis rides the pair)."""
    if seed is None:
        seed = int(script["seed"])
    if out_dir is None:
        out_dir = REPO / "output" / "div"
    out_dir.mkdir(parents=True, exist_ok=True)
    base_log, base_fp, base_tick = _run_arm(
        script, seed, base_pack, base_directors, out_dir, "base"
    )
    pert_log, pert_fp, pert_tick = _run_arm(
        script, seed, pert_pack, pert_directors, out_dir, "pert"
    )
    _header, base_events = parse_log(base_log)
    _header, pert_events = parse_log(pert_log)

    diff = compare(
        base_log, pert_log,
        fingerprint_left=base_fp, fingerprint_right=pert_fp,
    )
    records = _derive_records(
        base_log, pert_log, base_events, pert_events,
        base_fp, pert_fp, base_tick, pert_tick, base_pack,
    )
    return records, diff


def _derive_records(
    base_log: Path,
    pert_log: Path,
    base_events: list[dict[str, Any]],
    pert_events: list[dict[str, Any]],
    base_fp: int,
    pert_fp: int,
    base_tick: int,
    pert_tick: int,
    pack: Pack,
) -> DivergenceRecords:
    """The bounded walk: first divergence, causal path, persistence,
    family deltas, projection delta (deterministic — sorted() iteration
    only, INV-2's periphery discipline)."""
    records = DivergenceRecords(
        base_log=base_log, pert_log=pert_log,
        base_events=len(base_events), pert_events=len(pert_events),
        base_fingerprint=base_fp, pert_fingerprint=pert_fp,
        base_last_tick=base_tick, pert_last_tick=pert_tick,
    )
    first = _first_divergence(base_events, pert_events)
    if first is None:
        return records
    index, event, other = first
    if other is None:
        # a one-side row: the side that holds the event at this index
        side = "base" if index < len(base_events) else "pert"
    else:
        side = "both"
    anchors: tuple[str, ...] = ()
    if other is not None:
        anchors = tuple(
            f"{name}: {event.get(name)!r} != {other.get(name)!r}"
            for name in ANCHOR_FIELDS
            if not _json_equal(event.get(name), other.get(name))
        )
    # the causal ancestry walks the side that HAS the event; on a
    # both-differ row the perturbed side is the perturbation's own
    # consequence chain
    if side == "pert":
        path = _causal_path(pert_events, event)
    else:
        path = _causal_path(base_events, event)
    after = max(len(base_events), len(pert_events)) - index - 1
    divergent = 0
    divergent_after = 0
    last_div: int | None = None
    for position in range(index, max(len(base_events), len(pert_events))):
        in_base = position < len(base_events)
        in_pert = position < len(pert_events)
        if in_base and in_pert:
            equal = _json_equal(base_events[position], pert_events[position])
        else:
            equal = False
        if not equal:
            divergent += 1
            if position > index:
                divergent_after += 1
            last_div = position
    persists = (
        last_div is not None
        and last_div == max(len(base_events), len(pert_events)) - 1
    )
    types_base = Counter(str(event.get("type")) for event in base_events)
    types_pert = Counter(str(event.get("type")) for event in pert_events)
    family: list[str] = []
    for name in sorted(set(types_base) | set(types_pert)):
        delta = types_pert.get(name, 0) - types_base.get(name, 0)
        if delta:
            family.append(f"{'+' if delta > 0 else ''}{delta} {name}")
    proj_lines, proj_count = _projection_delta(pack, base_log, pert_log)
    return DivergenceRecords(
        base_log=base_log, pert_log=pert_log,
        base_events=len(base_events), pert_events=len(pert_events),
        base_fingerprint=base_fp, pert_fingerprint=pert_fp,
        base_last_tick=base_tick, pert_last_tick=pert_tick,
        first_index=index,
        first_tick=int(event.get("t", 0)) if event.get("t") is not None else None,
        first_side=side,
        first_id=str(event.get("id")),
        first_type=str(event.get("type")),
        first_anchors=anchors,
        causal_path=path,
        positions_after=after,
        divergent_positions=divergent,
        last_divergent_index=last_div,
        persists_to_horizon=persists,
        re_converged=bool(after) and divergent_after == 0,
        family_delta=tuple(family[:MAX_FAMILY_LINES]),
        projection_delta=proj_lines[:MAX_PROJECTION_LINES],
        projection_delta_count=proj_count,
    )


def render_report(
    records: DivergenceRecords, diff: SemanticDiff, perturbation: str,
    name: str,
) -> str:
    """The human-readable report (stdout; the verdict line is the
    oracle's own, quoted verbatim)."""
    lines = [
        f"== DIVERGENCE PROBE: {name} · perturbation: {perturbation} ==",
        f"arm BASE  : {records.base_events} events · ticks 0.."
        f"{records.base_last_tick} · fingerprint 0x"
        f"{records.base_fingerprint:016x}",
        f"arm PERT  : {records.pert_events} events · ticks 0.."
        f"{records.pert_last_tick} · fingerprint 0x"
        f"{records.pert_fingerprint:016x}",
        f"arm logs  : {records.base_log} · {records.pert_log}",
    ]
    if records.first_index is None:
        lines.append("first divergence: NONE — the futures are equal "
                     "(the null control; exit 0)")
    else:
        where = f"event[{records.first_index}]"
        if records.first_tick is not None:
            where += f" t={records.first_tick}"
        if records.first_side == "both":
            lines.append(
                f"first divergence: {where} — both sides differ "
                f"({records.first_id} {records.first_type})"
            )
            lines.extend(f"  anchor {anchor}" for anchor in records.first_anchors)
        else:
            lines.append(
                f"first divergence: {where} — {records.first_side}-only: "
                f"{records.first_id} {records.first_type}"
            )
        lines.append(
            "causal path (the divergent event's own-log ancestry, "
            f"bounded {MAX_CAUSAL_LINKS}):"
        )
        chain = " <- ".join(
            f"{eid} {etype} (t={tick})" for eid, tick, etype in records.causal_path
        )
        lines.append(f"  {chain}")
        lines.append(
            f"persistence: {records.positions_after} positions after the "
            f"divergence · {records.divergent_positions} divergent · "
            f"last divergent "
            + (
                f"event[{records.last_divergent_index}]"
                if records.last_divergent_index is not None else "none"
            )
            + f" · persists to the horizon: "
            f"{'yes' if records.persists_to_horizon else 'no'} · "
            f"re-converged: {'yes' if records.re_converged else 'no'}"
        )
        if records.family_delta:
            lines.append(
                "divergent families (pert - base): "
                + "; ".join(records.family_delta)
            )
        lines.append(
            f"projection delta: {records.projection_delta_count} prop(s)"
            + (
                ": " + "; ".join(records.projection_delta)
                if records.projection_delta else ""
            )
        )
    lines.append("-- the oracle verdict (semantic_diff, TEST_PLAN §1.4) --")
    for line in format_report(diff).splitlines():
        if line.startswith(("VERDICT:", "fingerprints:", "events:")):
            lines.append(line)
    return "\n".join(lines) + "\n"


def _perturbation_pack(
    perturbation: str, systems_minus: str | None, out_dir: Path, pack_dir: Path
) -> tuple[Pack, bool, str]:
    """Resolve the perturbation into (pack, directors, label). The
    pacing/systems-minus arms are the TAVERN balance family (the
    materializers' own pack) — a non-tavern script refuses loudly, the
    T8 directors arm is the pack-agnostic one."""
    if perturbation == "directors":
        return load_pack(pack_dir), False, "directors off (the T8 minimal pair)"
    if pack_dir.name != balance_harness.PACK_DIR.name:
        raise ProbeInputError(
            f"the {perturbation} arms are the tavern balance family "
            f"(balance_harness's own materializers); the script's pack "
            f"{pack_dir.name!r} is out of family — use --directors-off"
        )
    if perturbation == "pacing":
        return (
            balance_harness._nopacing_pack(out_dir),
            True,
            "pacing off (director.pacing dropped)",
        )
    assert systems_minus is not None
    if systems_minus not in balance_harness.ABLATABLE:
        raise ProbeInputError(
            f"unknown systems-minus block {systems_minus!r} — the measured "
            f"removable set is {list(balance_harness.ABLATABLE)} (the "
            f"systems-table rows are interlocked, TEST_PLAN §6)"
        )
    return (
        balance_harness._systems_minus_pack(out_dir, systems_minus,
                                            drop_pacing=False),
        True,
        f"systems minus {systems_minus} (the arming block dropped)",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "The future-divergence minimal-pair probe (div-1): one "
            "same-seed BASE/PERTURBED pair over the balance-harness arm "
            "family, the semantic oracle's verdict + first-divergence / "
            "causal-path / persistence records."
        ),
    )
    parser.add_argument(
        "--script", type=Path, default=DEFAULT_SCRIPT,
        help="the playscript both arms run (default: the T8 gate script)",
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="both arms' shared seed (default: the script's own)",
    )
    pert = parser.add_mutually_exclusive_group()
    pert.add_argument(
        "--directors-off", action="store_true",
        help="the T8 minimal pair: BASE directors on, PERTURBED off "
        "(the default)",
    )
    pert.add_argument(
        "--pacing-off", action="store_true",
        help="PERTURBED = the pack minus director.pacing (tavern family)",
    )
    pert.add_argument(
        "--systems-minus",
        help="PERTURBED = the pack minus one arming block (tavern family)",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=REPO / "output" / "div",
        help="the arm logs' gitignored output dir",
    )
    args = parser.parse_args(argv)
    try:
        script = load_playscript(args.script)
    except (OSError, ValueError) as exc:
        print(f"divergence probe: INPUT ERROR — {exc}")
        return 2
    pack_dir = REPO / "content" / str(script["pack"]).partition("@")[0]
    try:
        if args.pacing_off:
            perturbation = "pacing"
        elif args.systems_minus is not None:
            perturbation = "systems-minus"
        else:
            perturbation = "directors"
        pert_pack, pert_directors, label = _perturbation_pack(
            perturbation, args.systems_minus, args.out_dir, pack_dir
        )
        base_pack = load_pack(pack_dir)
        records, diff = probe(
            script, base_pack, pert_pack,
            base_directors=True, pert_directors=pert_directors,
            seed=args.seed, out_dir=args.out_dir,
        )
    except ProbeInputError as exc:
        print(f"divergence probe: INPUT ERROR — {exc}")
        return 2
    print(render_report(records, diff, label, str(script["name"])), end="")
    return 0 if diff.equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
