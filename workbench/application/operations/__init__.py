"""The application-operations package (wb-5, the app spec §§6.1/8/10/
11/12/20 — the family's fifth row; the backend family wb-6, §32
step 7).

The modules: `lifecycles` (§11's four closed state machines — the
vocabulary owner), `execution` (§12's absolute deadline +
cooperative cancellation + the in-memory run registry over the §10
artifact freeze), `models` (§20's discovery half over the §16
MODELS_ASSETS role — the §9 identity closure, the strong identity
computed when needed, the one real work kind), `backend` (wb-6: the
typed llama.cpp port + the three backend operations — chat.send over
the run registry + model.load/unload over the Model ladder walked on
observed outcomes), `composition` (§6.1's single wiring owner — the
registered operations on the wb-4 gateway: the five from wb-5 + the
three backend operations when a port is injected).

The §27 dependency envelope (agreeing with pyproject): the runtime
dependencies of this package are EMPTY — stdlib + the wb-3 skeleton
(`workbench.application.*`) + the wb-4 gateway registration surface
(`workbench.api.gateway`/`contract`, imported by `composition` and
`backend`) and nothing else: no `core/` (the app side stays
CanonSim-free until the §24 seam row), no `cli/`, no engine, no
network (INV-4's two-surface form untouched — `cli/engine.py` and
`workbench/api/transport.py` remain the only sanctioned modules; the
backend port is INJECTED at the composition root, never imported —
the physical wiring is the application-entry rows' own).
"""

from __future__ import annotations

#: The §27 dependency envelope — the package's runtime dependencies
#: (empty: stdlib-only imports beyond the workbench packages, the
#: same discipline as the wb-3 `application/__init__.py`).
RUNTIME_DEPENDENCIES: tuple[str, ...] = ()
