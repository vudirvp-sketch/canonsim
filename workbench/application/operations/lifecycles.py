"""The application/backend/model/execution lifecycles (wb-5, the app
spec §11 — the family's fifth row).

The law: **keep the state machines distinct** — four domains, each a
closed vocabulary with one owner, legal transitions, terminal
semantics and invalid-transition loudness. §11's own sentence: "These
are contract vocabularies, not one-class-per-state requirements" —
this module is the vocabulary owner (the `contract.py` pattern), not
a class-per-state hierarchy. The run registry (`execution.py`) is the
first consumer: an execution's state walks this table and nothing
else; the model registry (`models.py`) names DISCOVERED — the only
state its discovery half can honestly hold (§20: the loading states
arrive with the backend row, app §32 step 7).

The four ladders (§11 verbatim, the ↘ branches resolved):

```text
Application: STARTING → READY → DEGRADED → STOPPING → STOPPED
             (+ §25's FAILED_SHUTDOWN from STOPPING — the shutdown
             walk's own terminal: "STOPPED or FAILED_SHUTDOWN")
Backend:     ABSENT → STARTING → PROBING → READY → BUSY → STOPPING
             → STOPPED ; the failure branch FAILED ↔ RECOVERING with
             RECOVERING → READY (the recovered return)
Model:       DISCOVERED → VALIDATED → SELECTED → LOADING → LOADED →
             ACTIVE → UNLOADING → EVICTED ; ↘ FAILED ; EVICTED →
             SELECTED (the re-selection — the model stays validated)
Execution:   ADMITTED → STARTING → RUNNING → COMPLETING → COMPLETED ;
             ↘ FAILED ; ↘ CANCEL_REQUESTED → CANCELED |
             FAILED_TO_CANCEL | UNKNOWN
```

Terminal semantics = the empty successor set (`TERMINAL_STATES`): a
terminal state has no legal successor, and every attempted move away
from one is LOUD (`LifecycleError`) — never a silent reset, never a
quiet reuse. The Execution terminal set {COMPLETED, FAILED, CANCELED,
FAILED_TO_CANCEL, UNKNOWN} is the closure the wb-3 artifact's status
field pointed at ("§11 owns its closure when that step lands"): the
run registry closes every artifact with a member of it.

§12.3's cancellation truth rides the Execution table:
CANCEL_REQUESTED → FAILED_TO_CANCEL is the honest outcome when the
work finished despite the request (the late result — §12.3: late
results "cannot mutate newer state"; the result is recorded on the
FAILED_TO_CANCEL record, never applied as a completion); CANCELED is
the checkpoint-observed abort; UNKNOWN is the undeterminable race,
reachable in-process through the registry's `mark_unknown` (§25's
"backend loss during execution yields truthful terminal/unknown
state" — the process-loss rows own its producers, hence UNKNOWN in
STARTING's and RUNNING's successors too).
"""

from __future__ import annotations

#: The lifecycle domains (§11's four machines — one owner each).
LIFECYCLE_DOMAINS: frozenset[str] = frozenset(
    {"APPLICATION", "BACKEND", "MODEL", "EXECUTION"}
)

#: §11's Application ladder (+ §25's FAILED_SHUTDOWN terminal).
APPLICATION_STATES: frozenset[str] = frozenset(
    {
        "STARTING",
        "READY",
        "DEGRADED",
        "STOPPING",
        "STOPPED",
        "FAILED_SHUTDOWN",
    }
)

#: §11's Backend ladder (the ATTACHED/MANAGED ownership rows, §11.1,
#: walk it; wb-5 closes the vocabulary only — no process machinery).
BACKEND_STATES: frozenset[str] = frozenset(
    {
        "ABSENT",
        "STARTING",
        "PROBING",
        "READY",
        "BUSY",
        "STOPPING",
        "STOPPED",
        "FAILED",
        "RECOVERING",
    }
)

#: §11's Model ladder.
MODEL_STATES: frozenset[str] = frozenset(
    {
        "DISCOVERED",
        "VALIDATED",
        "SELECTED",
        "LOADING",
        "LOADED",
        "ACTIVE",
        "UNLOADING",
        "EVICTED",
        "FAILED",
    }
)

#: §11's Execution ladder — the run registry's own machine.
EXECUTION_STATES: frozenset[str] = frozenset(
    {
        "ADMITTED",
        "STARTING",
        "RUNNING",
        "COMPLETING",
        "COMPLETED",
        "FAILED",
        "CANCEL_REQUESTED",
        "CANCELED",
        "FAILED_TO_CANCEL",
        "UNKNOWN",
    }
)

#: The legal-transition tables: domain → state → successors. The
#: closure of each ladder's arrows (the ↘ failure branches resolved
#: per the docstring's note). A state with an EMPTY successor set is
#: terminal — that is the whole terminal semantics.
_TRANSITIONS: dict[str, dict[str, frozenset[str]]] = {
    "APPLICATION": {
        "STARTING": frozenset({"READY", "STOPPING"}),
        "READY": frozenset({"DEGRADED", "STOPPING"}),
        "DEGRADED": frozenset({"READY", "STOPPING"}),
        "STOPPING": frozenset({"STOPPED", "FAILED_SHUTDOWN"}),
        "STOPPED": frozenset(),
        "FAILED_SHUTDOWN": frozenset(),
    },
    "BACKEND": {
        "ABSENT": frozenset({"STARTING"}),
        "STARTING": frozenset({"PROBING", "FAILED", "STOPPING"}),
        "PROBING": frozenset({"READY", "FAILED", "STOPPING"}),
        "READY": frozenset({"BUSY", "FAILED", "STOPPING"}),
        "BUSY": frozenset({"READY", "FAILED", "STOPPING"}),
        "FAILED": frozenset({"RECOVERING", "STOPPING"}),
        "RECOVERING": frozenset({"READY", "FAILED", "STOPPING"}),
        "STOPPING": frozenset({"STOPPED"}),
        "STOPPED": frozenset(),
    },
    "MODEL": {
        "DISCOVERED": frozenset({"VALIDATED"}),
        "VALIDATED": frozenset({"SELECTED", "FAILED"}),
        "SELECTED": frozenset({"LOADING"}),
        "LOADING": frozenset({"LOADED", "FAILED"}),
        "LOADED": frozenset({"ACTIVE"}),
        "ACTIVE": frozenset({"UNLOADING"}),
        "UNLOADING": frozenset({"EVICTED"}),
        "EVICTED": frozenset({"SELECTED"}),
        "FAILED": frozenset(),
    },
    "EXECUTION": {
        "ADMITTED": frozenset({"STARTING", "CANCEL_REQUESTED"}),
        "STARTING": frozenset(
            {"RUNNING", "FAILED", "CANCEL_REQUESTED", "UNKNOWN"}
        ),
        "RUNNING": frozenset(
            {"COMPLETING", "FAILED", "CANCEL_REQUESTED", "UNKNOWN"}
        ),
        "COMPLETING": frozenset({"COMPLETED", "FAILED"}),
        "CANCEL_REQUESTED": frozenset(
            {"CANCELED", "FAILED_TO_CANCEL", "UNKNOWN", "FAILED"}
        ),
        "COMPLETED": frozenset(),
        "FAILED": frozenset(),
        "CANCELED": frozenset(),
        "FAILED_TO_CANCEL": frozenset(),
        "UNKNOWN": frozenset(),
    },
}

#: The domain → state-set map (the vocabulary closures themselves).
LIFECYCLE_STATES: dict[str, frozenset[str]] = {
    "APPLICATION": APPLICATION_STATES,
    "BACKEND": BACKEND_STATES,
    "MODEL": MODEL_STATES,
    "EXECUTION": EXECUTION_STATES,
}

#: Each ladder's head — the state a fresh instance enters.
INITIAL_STATES: dict[str, str] = {
    "APPLICATION": "STARTING",
    "BACKEND": "ABSENT",
    "MODEL": "DISCOVERED",
    "EXECUTION": "ADMITTED",
}

#: The terminal states per domain (empty successor set — derived,
#: never hand-maintained).
TERMINAL_STATES: dict[str, frozenset[str]] = {
    domain: frozenset(
        state for state, successors in table.items() if not successors
    )
    for domain, table in _TRANSITIONS.items()
}


class LifecycleError(ValueError):
    """A lifecycle-contract violation (an unknown domain/state or an
    illegal transition — LOUD, never a silent fallback)."""


def states(domain: str) -> frozenset[str]:
    """One domain's closed state set."""
    _require_domain(domain)
    return LIFECYCLE_STATES[domain]


def legal_transitions(domain: str, state: str) -> frozenset[str]:
    """The legal successors of one state (empty = terminal)."""
    _require_domain(domain)
    table = _TRANSITIONS[domain]
    if state not in table:
        raise LifecycleError(
            f"{domain}: unknown state {state!r} (closed set: {sorted(table)})"
        )
    return table[state]


def is_terminal(domain: str, state: str) -> bool:
    """True when the state has no legal successor (the terminal
    semantics — §11: terminal states never quietly reopen)."""
    return not legal_transitions(domain, state)


def transition(domain: str, current: str, target: str) -> str:
    """Validate one lifecycle move and return the target — or raise
    `LifecycleError` naming the legal set (invalid-transition
    loudness, §11's own test requirement). A same-state call is NOT a
    transition: it raises (the tables carry no self-loops — a state
    either moves or it does not)."""
    successors = legal_transitions(domain, current)
    if target not in successors:
        raise LifecycleError(
            f"{domain}: illegal transition {current!r} → {target!r} "
            f"(legal: {sorted(successors)})"
        )
    return target


def _require_domain(domain: str) -> None:
    if domain not in LIFECYCLE_DOMAINS:
        raise LifecycleError(
            f"unknown lifecycle domain {domain!r} "
            f"(closed set: {sorted(LIFECYCLE_DOMAINS)})"
        )
