"""check.py — the named verification profiles of AGENTS.md §5.

One command per named profile, one verdict line each. The agent picks the
smallest profile that covers the touched surface (`full` before a commit) and
records a profile it could not run as SKIPPED, never as green.

    python scripts/check.py docs       # docguard + forward-doc reference scan
    python scripts/check.py fast [p]   # targeted pytest (paths, or the git diff)
    python scripts/check.py full       # pytest -q + ruff (the per-commit gate)
    python scripts/check.py frontend   # vitest + tsc
    python scripts/check.py model      # headless gateway start; asset roots resolve
    python scripts/check.py staged     # the pre-commit form: docs/fast by diff
    python scripts/check.py --install-hook

Exit codes: 0 green, 1 red, 2 SKIPPED (a required tool or surface is absent).
Stdlib only; D-046 (operator tooling lives in the repo when it is repo tooling).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_PY = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

GREEN, RED, SKIP = 0, 1, 2

#: A `fast` run has to stay fast: past this many owning tests the honest answer
#: is the `full` profile, not a suite-sized `fast`.
FAST_MAX_FILES = 20

#: The `content/` branch's owners: the pack admission lints. A per-pack test
#: (`test_<pack>_pack.py`) exists only for farstead, grim and pressure, so no
#: pack owner is guessed here — the label says "run `full`" instead.
PACK_LINT_TESTS = ["tests/test_packci.py", "tests/test_pack_tools.py"]

# Forward-looking documents: the ones a reader acts on. The state layer
# (STATUS/TASKS/GATES/AGENT_NAVIGATION + docs/iterations) is a local overlay and
# never reaches a published checkout, so README.md is its only public member.
FORWARD_DOCS = ["README.md"]
DEAD_VOCAB = re.compile(r"BASE_COMMIT|DELETED_PATHS|MANIFEST\.md5|tmpfiles\.org")
# The retired-vocabulary scan covers the published documents a reader ACTS on.
DEAD_VOCAB_DOCS = {"README.md"}
# A path-shaped reference inside a forward document must resolve.
REF = re.compile(
    r"\b((?:docs|scripts|core|tests|content|schemas|workbench|frontend|brief|cli)"
    r"/[A-Za-z0-9_./-]+\.(?:md|py|json|jsonl|ts|tsx|yml|yaml))"
)


def python_exe() -> str:
    """The repo interpreter: the pinned venv when present, else this one."""
    if VENV_PY.exists():
        return str(VENV_PY)
    return sys.executable


def run(
    cmd: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> tuple[int, str]:
    e = dict(os.environ)
    e["PYTHONIOENCODING"] = "utf-8"
    if env:
        e.update(env)
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=e,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except FileNotFoundError:
        return 127, f"not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {timeout}s: {' '.join(cmd)}"
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def verdict(profile: str, code: int, seconds: float, detail: str = "") -> int:
    state = {GREEN: "GREEN", RED: "RED", SKIP: "SKIPPED"}.get(code, "RED")
    line = f"check[{profile}]: {state} in {seconds:.1f}s"
    if detail:
        line += f" — {detail}"
    print(line)
    return code


def tail(text: str, lines: int = 25) -> str:
    rows = [r for r in text.strip().splitlines() if r.strip()]
    return "\n".join(rows[-lines:])


# ---------------------------------------------------------------- profiles


def profile_docs() -> int:
    started = time.time()
    code, out = run([python_exe(), "scripts/docguard.py"])
    if code != 0:
        print(tail(out, 40))
        return verdict("docs", RED, time.time() - started, "docguard")

    problems: list[str] = []
    for rel in FORWARD_DOCS:
        path = ROOT / rel
        if not path.exists():
            problems.append(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            if rel in DEAD_VOCAB_DOCS and DEAD_VOCAB.search(line):
                problems.append(
                    f"{rel}:{lineno}: retired handoff vocabulary: {line.strip()[:80]}"
                )
            for ref in REF.findall(line):
                if any(ch in ref for ch in "<>*{}"):
                    continue
                if not (ROOT / ref).exists():
                    problems.append(f"{rel}:{lineno}: dangling path reference: {ref}")
    if problems:
        print("\n".join(problems[:40]))
        return verdict("docs", RED, time.time() - started, f"{len(problems)} problem(s)")
    return verdict("docs", GREEN, time.time() - started, "docguard + references")


def _map_to_tests(paths: list[str]) -> list[str]:
    """Map changed paths to the tests that own them (the name convention).

    A test path is taken as-is; a source path is matched at a *name boundary* —
    `test_<stem>.py` / `test_<stem>_*.py` / `test_*_<stem>.py` — because a
    substring match is a lie (`scripts/check.py` would "own" the whole
    `test_checkpoint.py` family).
    """
    tests: list[str] = []
    for rel in paths:
        p = Path(rel)
        if rel.startswith("tests/") and p.suffix == ".py":
            tests.append(rel)
            continue
        if p.suffix != ".py" or not p.parts:
            continue
        if p.parts[0] in {"scripts", "core", "brief", "cli", "render", "sim", "workbench"}:
            found = []
            for pattern in (
                f"test_{p.stem}.py",
                f"test_{p.stem}_*.py",
                f"test_*_{p.stem}.py",
                f"test_*_{p.stem}_*.py",
            ):
                found.extend((ROOT / "tests").glob(pattern))
            if not found:
                # Name convention failed — fall back to the import reference:
                # the tests that actually name this module are its owners.
                dotted = ".".join(p.with_suffix("").parts)
                needle = dotted.replace("/", ".")
                for candidate in sorted((ROOT / "tests").glob("test_*.py")):
                    try:
                        body = candidate.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        continue
                    if needle in body:
                        found.append(candidate)
            tests.extend(str(c.relative_to(ROOT)) for c in sorted(set(found)))
    return sorted(set(tests))


def _changed_paths(staged: bool) -> list[str]:
    args = (
        ["git", "diff", "--cached", "--name-only"]
        if staged
        else ["git", "diff", "--name-only", "HEAD"]
    )
    code, out = run(args)
    return [r.strip() for r in out.splitlines() if r.strip()] if code == 0 else []


def profile_fast(targets: list[str], staged: bool = False) -> int:
    started = time.time()
    if not targets:
        targets = _changed_paths(staged)
        if not targets:
            return verdict("fast", SKIP, time.time() - started, "no changed paths")
    tests = _map_to_tests(targets)
    if not tests:
        return verdict(
            "fast",
            SKIP,
            time.time() - started,
            f"no owning test for {', '.join(targets[:3])}",
        )
    if len(tests) > FAST_MAX_FILES:
        # The module is imported widely: a "fast" run would be the whole suite.
        return verdict(
            "fast",
            SKIP,
            time.time() - started,
            f"{len(tests)} owning tests — run the full profile instead",
        )
    code, out = run(
        [python_exe(), "-m", "pytest", "-q", "--tb=short", *tests],
        env=pytest_env(),
    )
    if code != 0:
        print(tail(out, 40))
    return verdict(
        "fast",
        GREEN if code == 0 else RED,
        time.time() - started,
        f"{len(tests)} target(s)",
    )


def profile_full() -> int:
    started = time.time()
    code, out = run([python_exe(), "-m", "pytest", "-q"], env=pytest_env())
    counts = [r for r in out.strip().splitlines() if " passed" in r or " failed" in r]
    summary = counts[-1] if counts else "pytest"
    if code != 0:
        print(tail(out, 60))
        return verdict("full", RED, time.time() - started, summary)
    code, out = run([python_exe(), "-m", "ruff", "check", "."])
    if code != 0:
        print(tail(out, 40))
        return verdict("full", RED, time.time() - started, "ruff")
    return verdict("full", GREEN, time.time() - started, summary)


def runner_env() -> dict[str, str]:
    """The child environment for tools that need a writable temp dir.

    Measured on this host (2026-10-24): the *profile* temp root accepts a plain
    or nested `mkdir`, yet vitest's coverage provider still dies on
    `<TEMP>/<random>/web` with `EPERM`, while the same run against a repo-local
    root passes 256/256. The honest rule is therefore deterministic, not a
    probe: every child tool gets `.tmp-runner/<pid>` as TEMP/TMP (gitignored),
    and `CANONSIM_TEMP` overrides it when the operator knows better.
    """
    e = {"PYTHONIOENCODING": "utf-8"}
    root = Path(os.environ.get("CANONSIM_TEMP") or (ROOT / ".tmp-runner"))
    child = root / str(os.getpid())
    try:
        child.mkdir(parents=True, exist_ok=True)
    except OSError:
        child = Path(tempfile.gettempdir())
    e["TEMP"] = str(child)
    e["TMP"] = str(child)
    return e


def pytest_env() -> dict[str, str]:
    """pytest's child env: the runner temp root plus the determinism seed (INV-2)."""
    return {**runner_env(), "PYTHONHASHSEED": "0"}


def profile_frontend() -> int:
    started = time.time()
    npm = "npm.cmd" if os.name == "nt" else "npm"
    if shutil.which(npm) is None:
        return verdict("frontend", SKIP, time.time() - started, "npm not on PATH")
    fe = ROOT / "frontend"
    if not (fe / "node_modules").exists():
        return verdict("frontend", SKIP, time.time() - started, "node_modules absent — npm ci")
    env = runner_env()
    code, out = run([npm, "test", "--", "--reporter=dot"], cwd=fe, env=env)
    if code != 0:
        print(tail(out, 40))
        return verdict("frontend", RED, time.time() - started, "vitest")
    code, out = run([npm, "run", "typecheck"], cwd=fe, env=env)
    if code != 0:
        print(tail(out, 40))
        return verdict("frontend", RED, time.time() - started, "tsc")
    return verdict("frontend", GREEN, time.time() - started, "vitest + tsc")


def profile_model(seconds: int = 20) -> int:
    """Start the gateway headless and prove it resolves its asset roots."""
    started = time.time()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    # The gateway's readiness lines are the evidence; without this they stay
    # in the pipe buffer and a terminated child reports nothing at all.
    env["PYTHONUNBUFFERED"] = "1"
    try:
        p = subprocess.Popen(
            [python_exe(), "scripts/workbench_app.py"],
            cwd=str(ROOT),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError as exc:
        return verdict("model", SKIP, time.time() - started, f"cannot start: {exc}")
    try:
        out = p.communicate(timeout=seconds)[0] or ""
    except subprocess.TimeoutExpired:
        p.terminate()  # the readiness window elapsed — the honest stop
        try:
            out = p.communicate(timeout=10)[0] or ""
        except subprocess.TimeoutExpired:  # pragma: no cover
            p.kill()
            out = ""
    if "Traceback" in out:
        print(tail(out, 30))
        return verdict("model", RED, time.time() - started, "gateway raised")
    roots = [
        line.strip()
        for line in out.splitlines()
        if re.search(r"(models?|llama|runtime|loopback gateway)", line, re.IGNORECASE)
    ]
    if not roots:
        return verdict("model", SKIP, time.time() - started, "no asset-root line observed")
    for line in roots[:4]:
        print(line[:180])
    return verdict("model", GREEN, time.time() - started, "gateway started, roots resolved")


def profile_staged() -> int:
    """The pre-commit form: docs over docs, content over the pack lints, fast over code.

    A SKIPPED fast run does not block the commit — the hook's job is to catch a
    red shape or a red targeted test, and an unmapped source path is reported as
    a skip for the commit body (never silently upgraded to "green").
    """
    started = time.time()
    changed = _changed_paths(staged=True)
    if not changed:
        return verdict("staged", GREEN, 0.0, "nothing staged")
    docs = [c for c in changed if c.endswith(".md") or c.startswith("docs/")]
    if docs:
        code = profile_docs()
        if code != GREEN:
            return code
    content = [c for c in changed if c.startswith("content/")]
    if content:
        code, out = run(
            [python_exe(), "-m", "pytest", "-q", "--tb=short", *PACK_LINT_TESTS],
            env=pytest_env(),
        )
        if code != 0:
            print(tail(out, 40))
            return verdict("staged", RED, time.time() - started, "content pack lints")
    code_paths = [
        c for c in changed if c.endswith((".py", ".toml")) and not c.startswith("docs/")
    ]
    if code_paths:
        code = profile_fast(code_paths, staged=True)
        if code == SKIP:
            return verdict("staged", GREEN, 0.0, "code changed, no owning test (recorded)")
        return code
    if content:
        return verdict(
            "staged",
            GREEN,
            time.time() - started,
            "content changed: pack lints; run `full` for the pack's own laws",
        )
    return verdict("staged", GREEN, 0.0, f"{len(changed)} doc-only path(s)")


# ------------------------------------------------------------------- hooks

HOOK = """#!/bin/sh
# Installed by `python scripts/check.py --install-hook` (AGENTS.md §5).
# Bypass with `git commit --no-verify` only when another profile's evidence exists.
exec python scripts/check.py staged
"""


def install_hook() -> int:
    hooks = ROOT / ".git" / "hooks"
    if not hooks.is_dir():
        return verdict("install-hook", SKIP, 0.0, "no .git/hooks directory")
    target = hooks / "pre-commit"
    # Git for Windows runs hooks through its bundled sh, which reads LF: a CRLF
    # hook ends every command with a stray \r and fails on the first line.
    target.write_text(HOOK, encoding="utf-8", newline="\n")
    print(f"installed {target.relative_to(ROOT)}")
    return verdict("install-hook", GREEN, 0.0, "pre-commit -> check.py staged")


# -------------------------------------------------------------------- main

PROFILES = {
    "docs": lambda a: profile_docs(),
    "fast": lambda a: profile_fast(a.targets),
    "full": lambda a: profile_full(),
    "frontend": lambda a: profile_frontend(),
    "model": lambda a: profile_model(a.seconds),
    "staged": lambda a: profile_staged(),
}


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Named verification profiles (AGENTS.md §5).")
    parser.add_argument("profile", nargs="?", choices=sorted(PROFILES), help="profile to run")
    parser.add_argument("targets", nargs="*", help="for `fast`: test or source paths")
    parser.add_argument("--install-hook", action="store_true", help="install the pre-commit hook")
    parser.add_argument("--seconds", type=int, default=20, help="for `model`: startup window")
    args = parser.parse_args(argv)
    if args.install_hook:
        return install_hook()
    if not args.profile:
        parser.print_help()
        return RED
    return PROFILES[args.profile](args)


if __name__ == "__main__":
    raise SystemExit(main())
