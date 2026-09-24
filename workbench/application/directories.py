"""The runtime/data-directory contract (wb-3, the app spec §16 —
the family's third row).

The law: **production paths are explicit and `.git`/CWD
independent.**

```text
application/runtime | user configuration | user data/history ;
models/assets       | cache | backups | logs/diagnostics
```

`DirectoryLayout` owns the mapping role → explicit path under ONE
absolute root. The root is supplied by the composition root (§6.1 —
an environment path, never a guess); a RELATIVE root is refused
loudly at construction (the CWD-independence law made executable:
no path this contract yields may silently depend on where the
process happens to stand). Paths are JOINED, never resolved against
CWD — `path_for` performs no filesystem access and no
`Path.resolve()`, so the same root yields the same paths under any
working directory and any symlink weather.

The startup/recovery outcome vocabulary (§16 — "define startup/
recovery outcomes for missing, read-only, permission-denied,
corrupt, partially migrated and externally removed paths"):

```text
OK | MISSING | READ_ONLY | PERMISSION_DENIED | CORRUPT |
PARTIALLY_MIGRATED | EXTERNALLY_REMOVED
```

`probe_directory` classifies mechanically what a filesystem probe
can see: MISSING, OK, READ_ONLY (errno EROFS — the medium itself is
read-only) and PERMISSION_DENIED (EACCES/EPERM — this process may
not write here). The remaining three are OWNER-REPORTED states —
CORRUPT and PARTIALLY_MIGRATED are verdicts of the migration/
recovery layer (§32 step 3), EXTERNALLY_REMOVED is observed by a
recovery path that held an earlier OK — the vocabulary is closed
now so those layers report into it, but no probe invents them (the
honest-skeleton law: no speculative detection machinery without its
consumer).
"""

from __future__ import annotations

import errno
from dataclasses import dataclass
from pathlib import Path

#: The path-role vocabulary (§16's line, one role per distinct
#: lifetime/owner — cache is never the sole copy of user data,
#: backups are never models, logs are never configuration).
PATH_ROLES: frozenset[str] = frozenset(
    {
        "RUNTIME",
        "USER_CONFIG",
        "USER_DATA",
        "MODELS_ASSETS",
        "CACHE",
        "BACKUPS",
        "LOGS",
    }
)

#: The startup/recovery outcome vocabulary (§16 — closed; the
#: probe-detectable subset is named in probe_directory's docstring).
DIRECTORY_STATES: frozenset[str] = frozenset(
    {
        "OK",
        "MISSING",
        "READ_ONLY",
        "PERMISSION_DENIED",
        "CORRUPT",
        "PARTIALLY_MIGRATED",
        "EXTERNALLY_REMOVED",
    }
)

#: Role → the standard subdirectory name under the root (the §16
#: line, spelled as path segments; deterministic and sorted-free —
#: a fixed mapping, one name per role).
_ROLE_DIRS: dict[str, str] = {
    "RUNTIME": "runtime",
    "USER_CONFIG": "config",
    "USER_DATA": "data",
    "MODELS_ASSETS": "models",
    "CACHE": "cache",
    "BACKUPS": "backups",
    "LOGS": "logs",
}

#: The write-probe filename (created and removed by probe_directory
#: under the probed directory; a fixed name keeps the probe
#: deterministic and visibly ours).
_PROBE_FILENAME = ".canonsim_dir_probe"


class DirectoryError(ValueError):
    """A directory-contract violation (construction-time, never
    silent)."""


@dataclass(frozen=True)
class DirectoryLayout:
    """One root's explicit path set: the seven §16 roles, each an
    absolute path under `root`.

    The root MUST be absolute (`.git`/CWD independence — a relative
    root is a loud error, never a silent CWD join). The layout is
    inert: constructing it touches no filesystem; `path_for` is a
    pure join (no resolve, no mkdir — creation policy belongs to the
    composition root / startup path, not the contract).
    """

    root: Path

    def __post_init__(self) -> None:
        if not isinstance(self.root, Path):
            raise DirectoryError(
                "layout: root must be a pathlib.Path "
                f"(got {type(self.root).__name__})"
            )
        if not self.root.is_absolute():
            raise DirectoryError(
                f"layout: root {str(self.root)!r} is relative — the "
                ".git/CWD-independence law (app §16) requires an "
                "explicit absolute root from the composition root"
            )

    def path_for(self, role: str) -> Path:
        """The explicit path of one role: root / the role's standard
        subdirectory. Pure — no filesystem access, no CWD read."""
        if role not in PATH_ROLES:
            raise DirectoryError(
                f"layout: unknown path role {role!r} "
                f"(closed enum: {sorted(PATH_ROLES)})"
            )
        return self.root / _ROLE_DIRS[role]

    def all_paths(self) -> dict[str, Path]:
        """Every role's path, roles sorted (deterministic
        enumeration for startup/recovery walks)."""
        return {role: self.path_for(role) for role in sorted(PATH_ROLES)}


def probe_directory(path: Path) -> str:
    """Classify one directory's startup state (§16).

    Mechanically probe-detectable here: MISSING (nothing exists at
    the path), OK (a directory this process can write), READ_ONLY
    (errno EROFS — the medium refuses writes), PERMISSION_DENIED
    (EACCES/EPERM — the process lacks leave), the shallow CORRUPT
    form (something EXISTS at the path but is not a directory — the
    directory slot itself is corrupt) and the raced EXTERNALLY_REMOVED
    (the path existed at entry and vanished before the write — an
    external removal observed in the act). The probe writes and
    removes one fixed-name file; errno is the classifier (the real
    attempt, not the racy `os.access` pre-check).

    Owner-reported, never probed: the deep CORRUPT verdict (content
    level — a truncated store, a half-written index) and
    PARTIALLY_MIGRATED (the migration layer's verdict, §32 step 3)
    — the closed vocabulary reserves them; detection lands with
    their consumer.
    """
    if not path.exists():
        return "MISSING"
    if not path.is_dir():
        return "CORRUPT"
    probe = path / _PROBE_FILENAME
    try:
        with probe.open("a", encoding="utf-8"):
            pass
    except OSError as exc:
        if exc.errno == errno.EROFS:
            return "READ_ONLY"
        if exc.errno in (errno.EACCES, errno.EPERM):
            return "PERMISSION_DENIED"
        if exc.errno == errno.ENOENT:
            return "EXTERNALLY_REMOVED"
        raise
    try:
        probe.unlink()
    except OSError as exc:
        if exc.errno == errno.EROFS:
            return "READ_ONLY"
        if exc.errno in (errno.EACCES, errno.EPERM):
            return "PERMISSION_DENIED"
        raise
    return "OK"
