"""The golden-grammar regen for `tests/fixtures/parse_gbnf_seed125.gbnf`
(engine-1's GBNF mapping, iter-177). NOT a runtime tool: a one-off
committed-provenance helper — the fixture's regen protocol (TEST_PLAN
§1.1's discipline): re-run over the pinned state (the tavern pack, seed
125, fresh open, an empty ledger) and overwrite; any byte drift is a
grammar-contract change, never silent. Run from the repo root:

    python scripts/regen_parse_gbnf.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brief.gbnf import gbnf_grammar  # noqa: E402
from brief.ledger import SceneLedger  # noqa: E402
from brief.parser import grammar_snapshot  # noqa: E402
from core.log import read_log  # noqa: E402
from core.loop import Simulator  # noqa: E402
from core.pack import load_pack  # noqa: E402

OUT = REPO / "tests" / "fixtures" / "parse_gbnf_seed125.gbnf"


def main() -> int:
    pack = load_pack(REPO / "content" / "tavern_pack")
    schema = json.loads(
        (REPO / "schemas" / "event.schema.json").read_text(encoding="utf-8")
    )
    run = REPO / "output" / "regen_parse_gbnf"
    run.mkdir(parents=True, exist_ok=True)
    log = run / "run.jsonl"
    if log.exists():
        log.unlink()
    sim = Simulator(pack, 125, log, schema, commit="0000000")
    sim.open()
    _header, events = read_log(log, schema)
    grammar = gbnf_grammar(
        grammar_snapshot(events, pack, SceneLedger())
    )
    OUT.write_text(grammar, encoding="utf-8")
    print(f"[regen: {OUT} ({len(grammar.splitlines())} rules)]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
