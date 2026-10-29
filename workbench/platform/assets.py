"""assets.py — where the runtime assets live (the 2026-10-24 relocation).

The 18.6 GB GGUF pool, the 188 MB llama.cpp build and the station-pack archive
no longer sit inside the working tree: they moved to the workspace asset area
`<workspace>/runtime/assets/…`. The repo is a nested checkout at
`<workspace>/projects/applications/canonsim`, so the workspace root is found by
walking the checkout's parents — no absolute path is written down here.

One owner for the resolution, three steps, in order:

1. an explicit env override — ``CANONSIM_MODELS_ASSETS`` /
   ``CANONSIM_LLAMA_ROOT`` (the operator's escape hatch);
2. the workspace asset area when it exists —
   ``<workspace>/runtime/assets/models/models`` (the shared pool) and
   ``<workspace>/runtime/assets/canonsim/llama.cpp``;
3. the in-tree drop folder ``workbench/runtime/<role>`` — the pre-relocation
   layout, kept as the fallback so a fresh clone, CI, or another machine still
   starts the Workbench without any configuration (§16's startup/recovery
   vocabulary: a missing folder is created, a custom path that does not exist
   stays the loud argument error).

`scripts/workbench_app.py` and `scripts/workbench_launch.py` both resolve their
defaults through `runtime_asset_dir()` — never a second copy of this order.
"""

from __future__ import annotations

import os
from pathlib import Path

#: The env override per role (the operator's explicit choice wins).
ENV_OVERRIDE: dict[str, str] = {
    "models": "CANONSIM_MODELS_ASSETS",
    "llama.cpp": "CANONSIM_LLAMA_ROOT",
}

#: The workspace-area location per role, relative to the workspace root.
WORKSPACE_ASSET: dict[str, tuple[str, ...]] = {
    "models": ("runtime", "assets", "models", "models"),
    "llama.cpp": ("runtime", "assets", "canonsim", "llama.cpp"),
}


def workspace_root(repo: Path) -> Path | None:
    """The enclosing workspace, when this checkout lives inside one.

    The workspace is the nearest ancestor that carries a `runtime/assets`
    directory — the asset area's own marker, not a project list (a checkout
    outside a workspace honestly returns ``None`` and falls back in-tree).
    """
    for base in (repo, *repo.parents):
        if (base / "runtime" / "assets").is_dir():
            return base
    return None


def runtime_asset_dir(role: str, repo: Path | None = None) -> Path:
    """Resolve one runtime asset role: env override → workspace → in-tree.

    `role` is `"models"` or `"llama.cpp"`; an unknown role is a programming
    error, not a silently empty folder.
    """
    if role not in WORKSPACE_ASSET:
        raise ValueError(f"unknown runtime asset role: {role!r}")
    if repo is None:
        repo = Path(__file__).resolve().parents[2]
    override = os.environ.get(ENV_OVERRIDE[role])
    if override:
        return Path(override).expanduser()
    root = workspace_root(repo)
    if root is not None:
        candidate = root.joinpath(*WORKSPACE_ASSET[role])
        if candidate.is_dir():
            return candidate
    return repo / "workbench" / "runtime" / role
