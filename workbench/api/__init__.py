"""The Workbench inbound gateway package (wb-4, the app spec §§4.1/8 —
the family's fourth row, INV-4's owner-gated exception, D-201).

The law this package lands: **two network boundaries, not one** (the
app spec §4.1):

```text
OUTBOUND LLM transport: Workbench -> backend; cli/engine.py (D-193)
INBOUND Workbench gateway: client -> application operations; api/
```

Module shape (the G1/G7 pins, CONTRACTS §5's wb-4 contract):

- `contract.py` — the typed envelope + closed-vocabulary layer (the
  §8 request/response/event documents, the rejection vocabulary, the
  exposure/dispatch-outcome vocabularies). Pure stdlib +
  `workbench.application`; SOCKET-FREE.
- `gateway.py` — the transport-independent dispatch core (auth ->
  idempotency -> revision/lease -> operation -> outcome; the ordered
  per-session events + the RESYNC law; the session-translation seed).
  Pure stdlib + `workbench.application`; SOCKET-FREE — protocol/
  schema/auth/session translation ONLY (§4.1): it never invokes the
  backend transport (`cli/engine.py`), persistence internals, or
  CanonSim internals (§6.2's forbidden edges).
- `transport.py` — the ONE inbound network module (INV-4's second
  sanctioned surface, the architecture-test exception riding D-201):
  the loopback HTTP binding over the dispatch core. Binds loopback
  hosts only; the non-loopback-no-auth refusal is executable at
  construction (§30/§33, G3).

The semantic API is application operations (§8: "HTTP/SSE/WebSocket
are delivery mechanisms"); GUI/CLI/API share the same dispatch core —
the parity law (§30's row) is the packet's byte-diff proof. No God
Object (§2.1): the gateway owns translation, not the operations; the
composition root (§6.1) wires registered operations through
`OperationSpec` — wb-5+ grows the real families on that seam.

Dependency envelope (§27): stdlib only — `http.server`, `json`,
`threading`, `hmac` — zero third-party roots, agreeing with the
application package's empty envelope.
"""
