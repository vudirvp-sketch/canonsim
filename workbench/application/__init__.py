"""The Workbench application-operations package (wb-3, the app spec
§32 step 1: identity + execution artifact + runtime/data directories
+ clock + dependency envelope; the owner's continuation call over the
v5.2 brief, the family's third row).

What this is: the Python-side skeleton of the Workbench APPLICATION
layer — the owner of application operations and policy (the app spec
§2's authority row: `workbench/application` owns application
operations/policy; widgets/CLI/gateway must not). Step 1 lands the
four contract vocabularies every later step composes on:

- `identity`      — the §9 identity closure (path is location, not
                    identity; strong content digests; composite
                    identity; INTEGRITY_UNKNOWN explicit);
- `artifact`      — the §10 immutable execution artifact + provenance
                    (the material run inputs frozen before side
                    effects; the reproducibility scopes and kinds);
- `directories`   — the §16 runtime/data-directory contract (explicit,
                    `.git`/CWD-independent paths; the startup/recovery
                    outcome vocabulary);
- `clock`         — the §17 clock contract (four separated domains;
                    no wall clock in CanonSim deterministic state,
                    canonical replay or request identity).

NOT here (each lands at its own §32 step, its own consumer): the
lifecycles and ATTACHED/MANAGED ownership (step 2), deadlines/retry/
cancellation (step 2), persistence CAS and recovery roles (step 3),
the inbound gateway (step 4, INV-4's owner-gated exception — zero
network surface in this package while it stands). No God Object: no
manager, no registry, no service locator (§2.1) — the composition
root (§6.1) arrives with a real running application, not before.

Periphery law (CONTRACTS §5 D3): this package is the render/cli/
scripts class (D-046) — it imports nothing from `core/` unless a
read-side API is actually consumed (wb-3 consumes none), writes no
canon, opens no socket (INV-4 untouched: `cli/engine.py` stays the
one network module).

Dependency envelope (§27 — admission: real consumer → demonstrated
problem/risk → smallest typed seam; no dependency for future-
proofing; no generic plugin/DI/workflow/persistence/RPC/event
framework without a concrete consumer). The envelope of step 1 is
the empty set — see RUNTIME_DEPENDENCIES below.
"""

from __future__ import annotations

#: The runtime dependency envelope, executable: the application
#: package may import ONLY the stdlib and local packages — the empty
#: set below is the declaration the envelope test reads (a future
#: third-party root must first pass §27's admission and update this
#: set in the same iteration, with the consumer named).
RUNTIME_DEPENDENCIES: frozenset[str] = frozenset()

#: The envelope's own version — bumps when (and only when) a dependency
#: is admitted or removed (§27's mechanical verification: the set and
#: the pyproject `dependencies` list must agree — both stay empty at
#: step 1, matching pyproject's `dependencies = []`).
DEPENDENCY_ENVELOPE_VERSION = "envelope@0.1"
