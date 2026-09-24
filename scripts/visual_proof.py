"""The wb seam proof's operator runner (CONTRACTS.md §5 D1/D6, wb-1).

What this does: builds the Visual Scene IR from a committed fixture
(workbench/scene_build), then drives the pinned external Redot 26.2
LTS binary over the repository project (workbench/presentation/redot)
to compose the placeholder scene and capture the screenshot + metadata
artifacts. Everything lands under an output directory (gitignored —
runtime artifacts, INV-5's family); the proof is re-run and byte-diffed
by the pytest packet, never committed.

Engine resolution law (the brief's integration §7): ONE configurable
path — the REDOT_EXE environment variable. No hardcoded engine paths,
no second resolution site. Display law: an existing DISPLAY is reused;
otherwise a private Xvfb display is spawned for the run (POSIX only —
Windows renders windowed natively).

Usage:
    REDOT_EXE=/path/to/redot python scripts/visual_proof.py \\
        --log tests/fixtures/plumbing_smoke_seed42.jsonl \\
        --pack content/tavern_pack --location loc_tavern \\
        [--out output/visual_proof]
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPO / "workbench" / "presentation" / "redot"
RUN_TIMEOUT_S = 180
XVFB_WAIT_S = 2.0

if str(REPO) not in sys.path:  # the scripts/ pattern (mechanics.py et al.)
    sys.path.insert(0, str(REPO))


class ProofError(RuntimeError):
    """The proof's loud failure (never a silent skip at this layer)."""


def resolve_engine() -> Path:
    """REDOT_EXE — the single toolchain path (CONTRACTS §5 D1)."""
    value = os.environ.get("REDOT_EXE", "").strip()
    if not value:
        raise ProofError(
            "REDOT_EXE is not set — the engine binary is an external "
            "toolchain (CONTRACTS §5 D1); pass REDOT_EXE=<path to the "
            "Redot 26.2 LTS executable>"
        )
    engine = Path(value).expanduser()
    if not engine.is_file():
        raise ProofError(f"REDOT_EXE={value}: not a file")
    return engine


def _free_display() -> int:
    for candidate in range(90, 110):
        sock = Path(f"/tmp/.X11-unix/X{candidate}")
        if not sock.exists():
            return candidate
    raise ProofError("no free Xvfb display in 90..109")


class _Xvfb:
    """A private virtual display for the run (POSIX, no DISPLAY set)."""

    def __init__(self) -> None:
        self._proc: subprocess.Popen[bytes] | None = None
        self._display = ""

    def __enter__(self) -> dict[str, str]:
        if os.name != "posix":
            return dict(os.environ)
        current = os.environ.get("DISPLAY", "")
        if current and Path(f"/tmp/.X11-unix/X{current.lstrip(':').split('.')[0]}").exists():
            return dict(os.environ)  # an alive display is reused, never duplicated
        if shutil.which("Xvfb") is None:
            raise ProofError(
                "no DISPLAY and no Xvfb available — rendering needs one of them"
            )
        number = _free_display()
        self._display = f":{number}"
        self._proc = subprocess.Popen(
            ["Xvfb", self._display, "-screen", "0", "1280x720x24"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + XVFB_WAIT_S
        sock = Path(f"/tmp/.X11-unix/X{number}")
        while time.monotonic() < deadline:
            if sock.exists():
                break
            time.sleep(0.05)
        else:
            self.__exit__(None, None, None)
            raise ProofError("Xvfb did not come up")
        env = dict(os.environ)
        env["DISPLAY"] = self._display
        return env

    def __exit__(self, *_: object) -> None:
        if self._proc is not None:
            self._proc.send_signal(signal.SIGTERM)
            try:
                self._proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._proc.kill()
            self._proc = None


def run_proof(
    engine: Path,
    ir_path: Path,
    png_path: Path,
    meta_path: Path,
) -> int:
    """Drive the Redot project over one IR document; returns the exit code."""
    cmd = [
        str(engine),
        "--path",
        str(PROJECT_DIR),
        "--rendering-method",
        "gl_compatibility",
        "--rendering-driver",
        "opengl3",
        "--",
        "--ir",
        str(ir_path),
        "--png",
        str(png_path),
        "--meta",
        str(meta_path),
    ]
    with _Xvfb() as env:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=RUN_TIMEOUT_S,
            env=env,
            check=False,
        )
    if result.stdout.strip():
        print(result.stdout.strip())
    tail = "\n".join(result.stderr.strip().splitlines()[-4:])
    if tail:
        print(tail, file=sys.stderr)
    return int(result.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--log", required=True, type=Path, help="the committed fixture log")
    parser.add_argument("--pack", required=True, type=Path, help="the pack directory")
    parser.add_argument(
        "--location", default=None, help="the scene location (default: the player's)"
    )
    parser.add_argument("--out", type=Path, default=REPO / "output" / "visual_proof")
    args = parser.parse_args(argv)

    from workbench.scene_build import build_scene  # local: keeps --help fast

    engine = resolve_engine()
    out_dir = args.out.expanduser().resolve()  # absolute: the child's CWD is not ours
    out_dir.mkdir(parents=True, exist_ok=True)

    scene = build_scene(args.log, args.pack, args.location)
    ir_path = out_dir / "ir.json"
    ir_path.write_text(scene.to_json(), encoding="utf-8")
    png_path = out_dir / "proof.png"
    meta_path = out_dir / "meta.json"
    for stale in (png_path, meta_path):
        stale.unlink(missing_ok=True)

    code = run_proof(engine, ir_path, png_path, meta_path)
    if code != 0:
        raise ProofError(f"the Redot proof exited {code} (see stderr above)")
    if not png_path.is_file() or not meta_path.is_file():
        raise ProofError("the proof exited 0 but an artifact is missing")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    print(f"scene_identity {meta['scene_identity']}")
    print(f"artifacts: {png_path} + {meta_path} + {ir_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ProofError as exc:
        print(f"visual_proof: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
