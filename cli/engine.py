"""The runtime engine adapter (engine-1's landing, iter-177, D-193; the
model-facing serializer contract `docs/PRESENTATION_SPEC.md`, the doors'
own laws PARSER_SPEC §1 / BRIEF_SPEC §7.1 / VALIDATION_SPEC §7.1).

The ONE sanctioned network module in the repo — INV-4's executable form
(AGENTS §4): the LLM/network surface is exactly this file;
`tests/test_architecture.py` narrows the network ban to it. Everything
here is transport, serialization, backend-error mapping and provenance
(D-192's D1: the adapter owns transport/endpoint/serialization/errors;
orchestration and acceptance policy stay the application's — the
session, `cli/main.py`). The doors' gates run on the reply document,
unchanged: the runtime engine is "the operator" of the D-055 file
contract — it reads the emitted call document and writes the reply
document, exactly like the dev-time human operator. No engine client
ever enters `core/` or `brief/` (D-031/D-037).

The measured surface (TECH_NOTES §13/§13.1, llama-server b11064):

- GBNF rides `/v1/chat/completions` as a TOP-LEVEL `grammar` param
  (per-request, with seed/temperature/chat_template_kwargs);
  `response_format` is refused by the backend — never sent;
- thinking OFF via `chat_template_kwargs.enable_thinking=false` (the
  empty-content trap: reasoning_content consumes max_tokens, §13);
- the parse door runs temperature 0, the narrator 0.8 (the round-4
  recipe); the seed pins request identity (D-192's D3 seeded-local
  tier: same manifest → byte-identical replies);
- POST `/props` is a silent no-op at this build — per-request params
  are the only live settings surface; the adapter never writes them;
- `/health` and `/props` are the effective-state evidence (D7's
  observation boundary); engine metadata (finish_reason) is operator
  feedback, never canon (I6).

The model-management half (wb-6, the backend row — the owner's
«подключи llama.cpp» call, app §32 step 7): `POST /models/load` +
`POST /models/unload`, the upstream model-management surface. This is
BUILD-SENSITIVE research evidence (the app spec §20: "Build-specific
llama.cpp router/`/props`/`/slots`/model-replacement findings ... must
be re-verified"): the pinned b11064 station's model-management reality
is the ROUTER (autoload/eviction, model swap ≠ restart — TECH_NOTES
§13.1), and the dedicated endpoints are the newer upstream line. The
wire shapes are pinned by the stub contract tests (test_engine.py —
"adapter tests are not implementation snapshots", app §29); the live
re-verification rides the station rows (TEST_PLAN §8.5's gap family).
The management calls are SINGLE-TRY (unlike the chat ladder): §29's
matrix allows bounded retry for an unavailable backend — "if
allowed" — and the row's answer is no (a load/unload the caller may
re-issue deliberately; the adapter never loops a management call).

The failure→ladder mapping (CONTRACTS §4.1 D7): transport failures
retry on the tries ladder (5, bg-8's precedent — the local engine is
down-or-slow, never rate-limited; no sleeps: a refused connection is
instant), then surface as EngineError — the SESSION maps them onto the
EXISTING degradation ladders (the parse cycle stays open, the narrator
falls to the template rung; `cli/main.py` owns that mapping); an HTTP
error status is terminal for the request (the backend's own error
body, never retried blind); a malformed response fails loud ONCE (the
thinking trap is deterministic at a fixed recipe — retrying buys
nothing). The re-ask budget itself is the session's (1, the heartbeat
convention "raw → after one re-ask").

stdlib-only (D-012): `urllib` — no new runtime dependency.
"""

from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "DEFAULT_ENDPOINT",
    "EngineConfig",
    "EngineError",
    "LlamaServerClient",
    "build_request",
    "manifest_row",
    "model_sha256",
    "narrator_messages",
    "serialize_request",
    "write_manifest",
]

#: The pinned default endpoint (§13: the deployment default is 8080 and
#: moves upstream — the endpoint is pinned, never assumed; the session
#: flag overrides it).
DEFAULT_ENDPOINT = "http://127.0.0.1:8080"

#: One message of the chat request: a role + content pair.
Message = dict[str, str]


class EngineError(RuntimeError):
    """A backend failure, mapped (D-192's D1: the adapter owns backend
    errors). `cause`: "unavailable" (transport — after the tries
    ladder), "http" (the backend answered an error status), "malformed"
    (the response carries no usable completion — the empty-content
    trap's class). The session maps every EngineError onto the existing
    degradation ladders; nothing here is ever canon (I1/I6)."""

    def __init__(self, cause: str, detail: str) -> None:
        super().__init__(f"[{cause}] {detail}")
        self.cause = cause


@dataclass(frozen=True, slots=True)
class EngineConfig:
    """Semantic config, never raw llama.cpp flags (D-192's D2): the
    pinned endpoint, the model stem (router sessions only — rides the
    request's `model` when set), the request identity (seed — the D3
    seeded-local tier), the per-door temperatures and completion
    budgets (the round-4 measured recipe: parse temp 0 / prose 0.8,
    parse prompts ~617 tok + <=160 completion), and the failure
    ladders' bounds (D7: 5 transport tries; the off-grammar re-ask
    budget is the session's acceptance policy, carried here as the
    semantic surface)."""

    endpoint: str = DEFAULT_ENDPOINT
    model: str | None = None
    seed: int = 42
    parse_temperature: float = 0.0
    prose_temperature: float = 0.8
    parse_max_tokens: int = 160
    prose_max_tokens: int = 512
    timeout_s: float = 120.0
    tries: int = 5
    re_asks: int = 1


# -- the request serialization (pure; PRESENTATION_SPEC's mapping) --------------


def build_request(
    messages: Sequence[Mapping[str, str]],
    *,
    grammar: str | None,
    temperature: float,
    max_tokens: int,
    seed: int,
    model: str | None,
) -> dict[str, Any]:
    """The chat-completions request body (pure, deterministic bytes via
    `serialize_request`): the measured surface — the `grammar` as a
    TOP-LEVEL param (omitted when None — the narrator side is
    unconstrained by design), thinking off, the seed pinning request
    identity (D3). The `model` rides only for router sessions."""
    body: dict[str, Any] = {
        "messages": [
            {"role": str(m["role"]), "content": str(m["content"])}
            for m in messages
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "seed": seed,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    if grammar is not None:
        body["grammar"] = grammar
    if model is not None:
        body["model"] = model
    return body


def serialize_request(body: Mapping[str, Any]) -> bytes:
    """The request's deterministic bytes: fixed separators, insertion
    order, ASCII-safe — same inputs → same bytes (the D3 request tier:
    the call-document bytes plus this serialization ARE the request
    identity)."""
    return json.dumps(body, ensure_ascii=True, separators=(", ", ": ")).encode(
        "utf-8"
    )


def narrator_messages(call_text: str) -> list[Message]:
    """The narrator call document as chat messages (PRESENTATION_SPEC's
    mapping table): the directives block seeds the SYSTEM role
    (BRIEF_SPEC §3.1's recorded intent — the pack's mode-role lines are
    the standing law, L2), the remainder rides the user message
    byte-verbatim (the D-049 purity: the serializer re-labels, never
    re-writes). The parse door runs DOCUMENT-ONLY (the measured request
    identity — §13.1's config answer: no parser-side system role)."""
    head, separator, tail = call_text.partition("\n\n")
    if not separator or not head.startswith("## directives"):
        # unreachable by construction (BRIEF_SPEC §7: the block pipeline
        # leads with directives) — the graceful fallback rides the whole
        # document, never a crash on the narrator path
        return [{"role": "user", "content": call_text}]
    system = "\n".join(head.splitlines()[1:])  # drop the block header
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": tail},
    ]


# -- the client (transport, errors) ---------------------------------------------


class LlamaServerClient:
    """The llama-server transport: health, props, chat completions.
    Holds nothing but the config — no connection state (a fresh request
    per call; the server is a long-lived process the operator owns,
    D-192's D1: the backend process is not application state)."""

    def __init__(self, config: EngineConfig) -> None:
        self._config = config

    @property
    def config(self) -> EngineConfig:
        return self._config

    def health(self) -> bool:
        """`/health` — the readiness probe (D7's observation boundary);
        False on any transport failure, never an exception."""
        try:
            with urllib.request.urlopen(
                self._config.endpoint + "/health",
                timeout=min(self._config.timeout_s, 5.0),
            ) as response:
                return response.status == 200
        except (urllib.error.URLError, OSError, ValueError):
            return False

    def props(self) -> dict[str, Any]:
        """`/props` — the effective-state evidence: model identity/path,
        build_info (the manifest row's backend half)."""
        return self._get_json(self._config.endpoint + "/props")

    def chat(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        grammar: str | None = None,
        temperature: float = 0.8,
        max_tokens: int = 512,
    ) -> tuple[str, str]:
        """One chat completion -> (content, finish_reason). Transport
        failures retry on the tries ladder; an HTTP error status is
        terminal (EngineError "http"); a response without a usable
        completion is EngineError "malformed" (the empty-content trap's
        class — the recipe's thinking-off makes it a backend/recipe
        mismatch, never something a blind retry fixes)."""
        body = build_request(
            messages,
            grammar=grammar,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=self._config.seed,
            model=self._config.model,
        )
        payload = serialize_request(body)
        url = self._config.endpoint.rstrip("/") + "/v1/chat/completions"
        request = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        last: Exception | None = None
        for _attempt in range(max(1, self._config.tries)):
            try:
                with urllib.request.urlopen(
                    request, timeout=self._config.timeout_s
                ) as response:
                    doc = json.loads(response.read().decode("utf-8"))
                return _extract_completion(doc)
            except urllib.error.HTTPError as exc:
                raise EngineError(
                    "http", f"{url} answered {exc.code}: {exc.reason}"
                ) from exc
            except json.JSONDecodeError as exc:
                raise EngineError(
                    "malformed", f"the response is not JSON: {exc}"
                ) from exc
            except (urllib.error.URLError, OSError) as exc:
                last = exc  # the tries ladder: down-or-slow, never sleep
                continue
        raise EngineError(
            "unavailable",
            f"{self._config.endpoint} unreachable after "
            f"{max(1, self._config.tries)} tries: {last}",
        )

    def load_model(
        self, model_path: str, alias: str | None = None
    ) -> dict[str, Any]:
        """POST `/models/load` — the model-management surface (wb-6,
        the backend row): the model's filesystem path + the optional
        alias (the workbench passes the logical_name). Build-sensitive
        research evidence — the wire shape pinned by the stub contract
        tests, the live re-verification a station row (see the module
        note). Single-try, no ladder: a management call the caller may
        re-issue, never a hidden loop."""
        body: dict[str, Any] = {"model": model_path}
        if alias is not None:
            body["alias"] = alias
        return self._post_json(
            self._config.endpoint.rstrip("/") + "/models/load", body
        )

    def unload_model(self, model_ref: str) -> dict[str, Any]:
        """POST `/models/unload` — the unload half (wb-6): the model
        reference (the alias the load named, or the path). The same
        single-try, build-sensitive contract as `load_model`."""
        return self._post_json(
            self._config.endpoint.rstrip("/") + "/models/unload",
            {"model": model_ref},
        )

    def _get_json(self, url: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(
                url, timeout=min(self._config.timeout_s, 10.0)
            ) as response:
                doc = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise EngineError(
                "http", f"{url} answered {exc.code}: {exc.reason}"
            ) from exc
        except (urllib.error.URLError, OSError) as exc:
            raise EngineError("unavailable", f"{url} unreachable: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise EngineError("malformed", f"{url} is not JSON: {exc}") from exc
        if not isinstance(doc, dict):
            raise EngineError("malformed", f"{url} is not an object")
        return doc

    def _post_json(
        self, url: str, body: Mapping[str, Any]
    ) -> dict[str, Any]:
        """One management POST -> the reply document. The error mapping
        is D1/D7's own: an HTTP error status is terminal ("http"), a
        dead endpoint is "unavailable" — single-try, the management
        no-ladder law (the module note)."""
        request = urllib.request.Request(
            url,
            data=serialize_request(dict(body)),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request, timeout=min(self._config.timeout_s, 10.0)
            ) as response:
                doc = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise EngineError(
                "http", f"{url} answered {exc.code}: {exc.reason}"
            ) from exc
        except (urllib.error.URLError, OSError) as exc:
            raise EngineError("unavailable", f"{url} unreachable: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise EngineError("malformed", f"{url} is not JSON: {exc}") from exc
        if not isinstance(doc, dict):
            raise EngineError("malformed", f"{url} is not an object")
        return doc


def _extract_completion(doc: Any) -> tuple[str, str]:
    """The (content, finish_reason) pair from a chat-completion response
    — loud on every shape the measured surface never promised."""
    try:
        choice = doc["choices"][0]
        content = choice["message"]["content"]
        finish = choice.get("finish_reason") or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise EngineError(
            "malformed", f"no usable completion in the response: {exc}"
        ) from exc
    if not isinstance(content, str) or not content.strip():
        raise EngineError(
            "malformed",
            "empty content — the thinking-consumed-budget trap "
            "(enable_thinking false is the recipe; check the model "
            "against the manifest)",
        )
    return content, str(finish)


# -- the provenance manifest (the D3 inference tier, §4.3's test 2) -------------


def model_sha256(path: str | Path) -> str | None:
    """The model file's sha256 (the manifest's model+hash half); None
    when unreadable (permissions, a router's remote path) — recorded as
    null, never guessed."""
    digest = hashlib.sha256()
    try:
        with open(path, "rb") as handle:  # noqa: PTH123 — a remote-local path
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def manifest_row(
    config: EngineConfig,
    props: Mapping[str, Any],
    *,
    parse_grammar_id: str | None = None,
) -> dict[str, Any]:
    """One session's provenance row (the §8.4/§13 pattern): model
    identity+hash (from /props), backend build, the request params, the
    seed, and the first parse call's grammar id (the constraint half of
    the request identity — the per-call grammas are derivable from the
    log, the manifest pins the mapping's fingerprint)."""
    model = props.get("model_path") or props.get("model")
    return {
        "endpoint": config.endpoint,
        "model": model,
        "model_sha256": model_sha256(str(model)) if model else None,
        "build": props.get("build_info"),
        "seed": config.seed,
        "params": {
            "parse_temperature": config.parse_temperature,
            "prose_temperature": config.prose_temperature,
            "parse_max_tokens": config.parse_max_tokens,
            "prose_max_tokens": config.prose_max_tokens,
            "thinking": False,
            "tries": config.tries,
            "re_asks": config.re_asks,
        },
        "parse_grammar_id": parse_grammar_id,
    }


def write_manifest(
    row: Mapping[str, Any], out_dir: Path, log_stem: str
) -> Path:
    """The manifest as a gitignored runtime artifact beside the session
    outputs (`output/engine/manifest_<log-stem>.json`) — provenance for
    the owner's station runs, never canon (INV-5's runtime-artifacts
    law)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"manifest_{log_stem}.json"
    path.write_text(
        json.dumps(row, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return path
