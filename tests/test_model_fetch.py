"""wb-9's claim packet — the model-assets fetch (the D-208 surface
`workbench/platform/model_fetch.py` + the `model.fetch` work kind in
`workbench/application/operations/models.py`).

What this packet claims (TEST_PLAN §9's claim form — the EFFECT, not
the mechanics):

1. THE URL VOCABULARY: the operator-facing forms normalize honestly —
   the direct URL (query stripped from the derived name), the HF
   resolve pass-through, the blob→resolve rewrite, the hf: shorthand
   (namespace/name/file, subpaths preserved), and the loud rejections
   (no scheme, no file path, the too-short shorthand, the non-plain
   name).
2. THE ADMISSION GATES: run.start on model.fetch rejects BEFORE the
   run exists (NOT_SENT) — the occupied name, the .part residue, the
   non-plain logical_name, the malformed URL.
3. THE END-TO-END FETCH: run.start → the run.get poll → COMPLETED —
   against a REAL loopback HTTP file server, the bytes landing in the
   models root atomically, the live PROGRESS riding the run document
   between admission and the terminal, and model.list discovering the
   file afterwards.
4. THE HONEST FAILURES: the 404 answer closes FAILED with the
   observed cause in the diagnostics; the cancellation closes
   CANCELED with the .part cleaned (the checkpoint's own carrier).
5. THE RUN-REGISTRY WIRING: the kind's own default deadline
   (minutes-class, not the registry's generic 60s); the work raises
   through the registry's truthful closes.
"""

from __future__ import annotations

import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from workbench.api.contract import RequestEnvelope  # noqa: E402
from workbench.api.gateway import Gateway  # noqa: E402
from workbench.application.clock import AppClock  # noqa: E402
from workbench.application.operations.composition import (  # noqa: E402
    compose_workbench_operations,
)
from workbench.application.operations.execution import (  # noqa: E402
    WorkContext,
)
from workbench.application.operations.models import (  # noqa: E402
    FETCH_DEFAULT_DEADLINE_SECONDS,
)
from workbench.platform.model_fetch import (  # noqa: E402
    CHUNK_BYTES,
    HttpModelFetcher,
    ModelFetchError,
)

# --------------------------------------------------------- the URL forms


def test_the_url_vocabulary_normalizes_honestly() -> None:
    fetcher = HttpModelFetcher()
    # the direct URL: verbatim for the fetch, the query stripped from
    # the derived name
    assert fetcher.normalize(
        "https://example.com/models/qwen.gguf?download=true"
    ) == ("https://example.com/models/qwen.gguf?download=true", "qwen.gguf")
    # the HF resolve URL passes through
    url, name = fetcher.normalize(
        "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/"
        "main/gemma-2-2b-it.Q4_K_M.gguf"
    )
    assert url == (
        "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/"
        "main/gemma-2-2b-it.Q4_K_M.gguf"
    )
    assert name == "gemma-2-2b-it.Q4_K_M.gguf"
    # the browser blob URL rewrites to the fetch URL
    assert fetcher.normalize(
        "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/blob/"
        "main/gemma-2-2b-it.Q4_K_M.gguf"
    ) == fetcher.normalize(
        "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/"
        "main/gemma-2-2b-it.Q4_K_M.gguf"
    )
    # the hf: shorthand (both spellings) — namespace/name/file, the
    # subpath preserved, the LAST segment the name
    for shorthand in (
        "hf:bartowski/gemma-2-2b-it-GGUF/gemma-2-2b-it.Q4_K_M.gguf",
        "hf://bartowski/gemma-2-2b-it-GGUF/gemma-2-2b-it.Q4_K_M.gguf",
    ):
        assert fetcher.normalize(shorthand) == (
            "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/"
            "resolve/main/gemma-2-2b-it.Q4_K_M.gguf",
            "gemma-2-2b-it.Q4_K_M.gguf",
        )
    url, name = fetcher.normalize(
        "hf:unsloth/Models/Qwen/Qwen2.5-7B/Qwen2.5-7B-Q4_K_M.gguf"
    )
    assert url == (
        "https://huggingface.co/unsloth/Models/resolve/main/"
        "Qwen/Qwen2.5-7B/Qwen2.5-7B-Q4_K_M.gguf"
    )
    assert name == "Qwen2.5-7B-Q4_K_M.gguf"


def test_the_url_rejections_are_loud() -> None:
    fetcher = HttpModelFetcher()
    for bad in (
        "",
        "   ",
        "ftp://host/file.gguf",
        "just-a-name.gguf",
        "https://plainhost",
        "https://plainhost/",
        "hf:repo-only",
        "hf:one/two",
        "https://host/..",
        "https://host/.",
    ):
        with pytest.raises(ModelFetchError) as excinfo:
            fetcher.normalize(bad)
        assert excinfo.value.cause == "malformed"


def test_a_subpath_url_derives_the_last_segment() -> None:
    """A file served under a subpath is legitimate — the §9 name is
    the LAST path segment (never a path)."""
    fetcher = HttpModelFetcher()
    assert fetcher.normalize("https://host/sub/dir/model.gguf") == (
        "https://host/sub/dir/model.gguf",
        "model.gguf",
    )


# --------------------------------------------------- the admission gates


class _RecordingFetcher:
    """The injected-fetcher stand-in: the REAL normalizer (pure) over
    a fetch that records and never dials — the admission gates are
    testable without the network."""

    def __init__(self) -> None:
        self.inner = HttpModelFetcher()
        self.calls: list[tuple[str, str]] = []

    def normalize(self, url: str) -> tuple[str, str]:
        return self.inner.normalize(url)

    def fetch(self, url, dest_dir, logical_name, *, on_progress, checkpoint):
        self.calls.append((url, logical_name))
        return {
            "location": str(dest_dir / logical_name),
            "logical_name": logical_name,
            "size_bytes": 0,
            "url": url,
        }


def _compose_with(fetcher: object, models_root: Path):
    gateway = Gateway()
    operations = compose_workbench_operations(
        gateway, models_root, AppClock(), fetch=fetcher
    )
    return gateway, operations


def _direct_session(gateway: Gateway) -> str:
    response = gateway.dispatch(
        RequestEnvelope(
            operation="session.create",
            arguments={},
            client_request_id="wb9-fetch-session",
        )
    )
    assert response.status == "OK", response.to_mapping()
    return str(response.result["session_id"])


def test_the_admission_gates_reject_before_the_run_exists(
    tmp_path: Path,
) -> None:
    models = tmp_path / "models"
    models.mkdir()
    (models / "taken.gguf").write_bytes(b"here")
    (models / "inflight.gguf.part").write_bytes(b"partial")
    gateway, _operations = _compose_with(_RecordingFetcher(), models)
    session = _direct_session(gateway)
    cases = [
        ({"url": "https://host/taken.gguf"}, "already exists"),
        ({"url": "https://host/inflight.gguf"}, ".part exists"),
        ({"url": ""}, "non-empty str"),
        ({"url": "not-a-url"}, "http(s) or the hf: shorthand"),
        ({"url": "hf:repo/file"}, "namespace/name/file"),
        ({"url": "https://host/ok.gguf", "logical_name": "../evil"}, "plain"),
        ({"url": "https://host/ok.gguf", "logical_name": "a/b.gguf"}, "plain"),
        ({"url": "https://host/ok.gguf", "extra": 1}, "closed set"),
    ]
    for index, (arguments, fragment) in enumerate(cases):
        reply = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments={"work": "model.fetch", "arguments": arguments},
                session_id=session,
                client_request_id=f"wb9-gate-{index}",
            )
        )
        assert reply.status != "OK", (arguments, reply.to_mapping())
        assert reply.rejection == "DOMAIN_REJECTED", arguments
        reason = str(reply.result.get("reason"))
        assert fragment in reason, (fragment, reason)


def test_the_fetch_kind_deadline_is_minutes_class() -> None:
    """The kind's own §12 material input: the registry's generic 60s
    default would fail a multi-GB download before the first percent —
    the kind resolves 3600s (the ceiling), asserted end-to-end in the
    landing test below."""
    assert FETCH_DEFAULT_DEADLINE_SECONDS == 3600.0


# --------------------------------------------- the end-to-end fetch


class _FileServer:
    """A REAL loopback HTTP file server: serves the given bytes at the
    given path with an honest Content-Length; a path registered as
    None answers 404; a path registered as ('truncate', n) sends fewer
    bytes than it claims."""

    def __init__(self) -> None:
        self.files: dict[str, bytes | None | tuple[str, int]] = {}
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802 — http.server's name
                entry = outer.files.get(self.path)
                if entry is None:
                    self.send_error(404)
                    return
                if isinstance(entry, tuple) and entry[0] == "truncate":
                    claimed, sent = entry[1], entry[1] // 2
                    body = b"x" * sent
                    self.send_response(200)
                    self.send_header(
                        "Content-Length", str(claimed)
                    )
                    self.end_headers()
                    self.wfile.write(body)
                    self.wfile.flush()
                    self.close_connection = True
                    return
                if entry is None:  # pragma: no cover — the 404 arm
                    self.send_error(404)
                    return
                body = bytes(entry)
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args: object) -> None:
                pass

        self._server = ThreadingHTTPServer(
            ("127.0.0.1", 0), Handler
        )
        self.thread = threading.Thread(
            target=self._server.serve_forever, daemon=True
        )

    @property
    def url(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()


def _await_run(gateway: Gateway, session: str, execution: str) -> dict:
    for _ in range(300):
        reply = gateway.dispatch(
            RequestEnvelope(
                operation="run.get",
                arguments={"execution_id": execution},
                session_id=session,
            )
        )
        assert reply.status == "OK", reply.to_mapping()
        result = reply.result
        if result["terminal"]:
            return dict(result)
        time.sleep(0.02)
    raise AssertionError("the fetch run never reached terminal")


def test_the_end_to_end_fetch_lands_the_file(tmp_path: Path) -> None:
    """THE wb-9 fetch claim: run.start model.fetch → the run.get poll
    → COMPLETED — the REAL HttpModelFetcher against the REAL loopback
    HTTP server, the bytes landing atomically, the live progress riding
    the run document, and discovery seeing the file afterwards."""
    models = tmp_path / "models"
    models.mkdir()
    payload = b"THE-MODEL-BYTES" * (CHUNK_BYTES // 16 + 7)
    server = _FileServer()
    server.files["/good.gguf"] = payload
    server.start()
    try:
        gateway, operations = _compose_with(HttpModelFetcher(), models)
        session = _direct_session(gateway)
        started = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments={
                    "work": "model.fetch",
                    "arguments": {"url": server.url + "/good.gguf"},
                },
                session_id=session,
                client_request_id="wb9-fetch-1",
            )
        )
        assert started.status == "OK", started.to_mapping()
        execution = started.result["execution_id"]
        assert started.result["deadline_seconds"] == (
            FETCH_DEFAULT_DEADLINE_SECONDS
        ), "the kind's own minutes-class default, not the registry's 60s"
        terminal = _await_run(gateway, session, execution)
        assert terminal["state"] == "COMPLETED", terminal
        run_result = terminal["result"]
        assert run_result["logical_name"] == "good.gguf"
        assert run_result["size_bytes"] == len(payload)
        landed = models / "good.gguf"
        assert landed.read_bytes() == payload
        assert not (models / "good.gguf.part").exists()
        # discovery sees the arrival — §20's own law
        listing = gateway.dispatch(
            RequestEnvelope(operation="model.list", arguments={})
        )
        names = [
            entry["logical_name"] for entry in listing.result["models"]
        ]
        assert "good.gguf" in names
        # the frozen inputs carry the normalized URL + the derived name
        frozen = dict(terminal["frozen_inputs"])
        assert frozen["logical_name"] == "good.gguf"
        assert frozen["url"] == server.url + "/good.gguf"
    finally:
        server.stop()


def test_the_live_progress_rides_the_run_document(tmp_path: Path) -> None:
    models = tmp_path / "models"
    models.mkdir()
    payload = b"y" * (CHUNK_BYTES * 2 + 11)  # 3 chunks: 3 observations
    server = _FileServer()
    server.files["/big.gguf"] = payload
    server.start()
    try:
        gateway, _operations = _compose_with(HttpModelFetcher(), models)
        session = _direct_session(gateway)
        started = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments={
                    "work": "model.fetch",
                    "arguments": {"url": server.url + "/big.gguf"},
                },
                session_id=session,
                client_request_id="wb9-progress",
            )
        )
        execution = started.result["execution_id"]
        seen_progress = False
        for _ in range(300):
            reply = gateway.dispatch(
                RequestEnvelope(
                    operation="run.get",
                    arguments={"execution_id": execution},
                    session_id=session,
                )
            )
            result = reply.result
            if result["progress"] is not None:
                progress = result["progress"]
                assert progress["logical_name"] == "big.gguf"
                assert progress["total_bytes"] == len(payload)
                assert 0 < progress["downloaded_bytes"] <= len(payload)
                seen_progress = True
            if result["terminal"]:
                break
            time.sleep(0.01)
        assert seen_progress, "the live progress never rode the document"
        terminal = _await_run(gateway, session, execution)
        assert terminal["state"] == "COMPLETED", terminal
        assert (models / "big.gguf").read_bytes() == payload
    finally:
        server.stop()


def test_the_404_answer_closes_failed_with_the_cause(
    tmp_path: Path,
) -> None:
    models = tmp_path / "models"
    models.mkdir()
    server = _FileServer()
    server.files["/missing.gguf"] = None
    server.start()
    try:
        gateway, _operations = _compose_with(HttpModelFetcher(), models)
        session = _direct_session(gateway)
        started = gateway.dispatch(
            RequestEnvelope(
                operation="run.start",
                arguments={
                    "work": "model.fetch",
                    "arguments": {"url": server.url + "/missing.gguf"},
                },
                session_id=session,
                client_request_id="wb9-404",
            )
        )
        terminal = _await_run(
            gateway, session, started.result["execution_id"]
        )
        assert terminal["state"] == "FAILED", terminal
        assert terminal["failure_type"] == "ModelFetchError"
        assert "404" in terminal["diagnostics"][0]
        assert not list(models.iterdir()), "no residue on the failure"
    finally:
        server.stop()


def test_the_cancellation_closes_canceled_and_cleans_the_part(
    tmp_path: Path,
) -> None:
    """The checkpoint's own carrier: a fetch whose checkpoint observes
    the cancellation raises WorkCancelled mid-download — the registry
    closes CANCELED and the .part never survives.

    KI#95 (iter-232): the fetch's single checkpoint() call RACED the
    main thread's run.cancel dispatch — on a fast runner the worker
    reached the checkpoint BEFORE the cancel landed, the checkpoint
    passed, and the "unreachable" AssertionError closed the run FAILED
    (the honest registry truth for an unrequested abort — the CI-red
    form). The fetch now POLLS the checkpoint (the work contract's own
    observation surface) until the cancellation arrives, bounded — the
    test is deterministic under any thread scheduling, and a cancel
    that never lands fails loudly with its own honest cause."""
    models = tmp_path / "models"
    models.mkdir()

    class _SlowFetcher:
        def normalize(self, url: str) -> tuple[str, str]:
            return url, "slow.gguf"

        def fetch(self, url, dest_dir, logical_name, *, on_progress, checkpoint):
            part = dest_dir / (logical_name + ".part")
            part.write_bytes(b"partial-download")
            try:
                on_progress(16, 1024)
                # the mid-download boundary, made deterministic: poll
                # the cooperative checkpoint until the cancellation
                # lands (the checkpoint reads the token without the
                # registry lock, so run.cancel is never starved); a
                # bounded wait — an absent cancel fails LOUDLY below.
                deadline = time.monotonic() + 20.0
                while time.monotonic() < deadline:
                    checkpoint()
                    time.sleep(0.005)
                raise AssertionError(
                    "the cancellation never arrived at the checkpoint "
                    "(run.cancel was not dispatched within 20s)"
                )
            finally:
                part.unlink(missing_ok=True)  # the real fetcher's own law

    gateway, _operations = _compose_with(_SlowFetcher(), models)
    session = _direct_session(gateway)
    started = gateway.dispatch(
        RequestEnvelope(
            operation="run.start",
            arguments={
                "work": "model.fetch",
                "arguments": {"url": "https://host/slow.gguf"},
            },
            session_id=session,
            client_request_id="wb9-cancel",
        )
    )
    execution = started.result["execution_id"]
    cancelled = gateway.dispatch(
        RequestEnvelope(
            operation="run.cancel",
            arguments={"execution_id": execution},
            session_id=session,
            client_request_id="wb9-cancel-req",
        )
    )
    assert cancelled.status == "OK", cancelled.to_mapping()
    terminal = _await_run(gateway, session, execution)
    assert terminal["state"] == "CANCELED", terminal
    assert not list(models.iterdir()), "the .part cleaned on the abort"


def test_the_work_context_progress_is_json_safe_gated(
    tmp_path: Path,
) -> None:
    """The reporter's own law: a non-JSON-safe payload is the work
    contract's loud violation (the registry's gate raises, never
    swallows) — driven through the registry's own reporter surface."""
    from workbench.application.operations.execution import (
        ExecutionRegistry,
        RegistryError,
    )

    registry = ExecutionRegistry(AppClock())
    execution_id = registry.admit(
        operation_id="probe-op",
        session_id="probe-session",
        work_kind="probe",
        frozen_inputs={"work": "probe"},
        deadline_seconds=10.0,
    )
    with pytest.raises(RegistryError, match="not JSON-safe"):
        registry.report_progress(execution_id, {"bad": object()})
    # the JSON-safe form records and the document serves it
    registry.report_progress(
        execution_id, {"downloaded_bytes": 5, "total_bytes": None}
    )
    document = registry.document(execution_id, "probe-session")
    assert document["progress"] == {
        "downloaded_bytes": 5,
        "total_bytes": None,
    }


def test_the_real_fetcher_cleans_the_part_on_abort(tmp_path: Path) -> None:
    """The platform row's own cleanup law: the checkpoint's carrier
    propagates through HttpModelFetcher.fetch untouched AND the .part
    never survives it (the finally guard — no residue, ever)."""
    from workbench.application.operations.execution import (
        CancellationToken,
        OperationDeadline,
    )

    models = tmp_path / "models"
    models.mkdir()
    started = AppClock().now_monotonic()
    context = WorkContext(
        execution_id="probe",
        deadline=OperationDeadline(
            operation_id="probe",
            started_monotonic=started,
            deadline_monotonic=started + 10.0,
        ),
        clock=AppClock(),
        cancellation=CancellationToken(),
    )
    context.cancellation.request()  # the abort observed at the boundary
    fetcher = HttpModelFetcher()
    from workbench.application.operations.execution import WorkCancelled

    server = _FileServer()
    server.files["/stall.gguf"] = b"payload-bytes"
    server.start()
    try:
        # the connection opens (the server is LIVE) and the FIRST
        # chunk-boundary checkpoint observes the cancellation — the
        # carrier propagates untouched through the platform module
        with pytest.raises(WorkCancelled):
            fetcher.fetch(
                server.url + "/stall.gguf",
                models,
                "stall.gguf",
                on_progress=lambda _done, _total: None,
                checkpoint=context.check,
            )
    finally:
        server.stop()
    assert not list(models.iterdir()), "no residue on the abort"
