"""The model-assets fetch mechanics (wb-9, the app spec §§16/20 + §2's
"asset mechanics | platform" row — the owner's 2026-09-25 «в идеале
вообще мог вызвать "менеджер" и подтянуть модель откуда угодно» call).

The law this module closes: a model may ARRIVE, not only be dropped by
hand — the workbench can pull a GGUF from anywhere the operator names.
Per the owner's call the network surface gains its THIRD sanctioned
module (D-208, INV-4's owner-gated extension — the same admission form
D-201 used for the inbound gateway):

```text
cli/engine.py                     OUTBOUND  the llama-server engine wire
workbench/api/transport.py        INBOUND   the loopback gateway binding
workbench/platform/model_fetch.py OUTBOUND  the model-assets fetch
                                            (HTTP GET downloads ONLY —
                                            no engine calls, no gateway
                                            semantics, no other verbs)
```

What this module owns (the platform row's own boundary): URL
normalization (the operator-facing shorthand forms → the direct fetch
URL), the streaming download to `<name>.part` + the atomic rename into
the MODELS_ASSETS root, the per-chunk progress observation, the
cooperative checkpoint (the caller's §12 carrier — the work context's
own check() — called once per chunk; it RAISES to abort, the
exception propagates through this module untouched), and the honest
failure vocabulary. What it does NOT own: discovery (models.py — the
file appears to it only after the rename), lifecycle states (a
fetching model holds NO Model-ladder state — it is not discovered
yet), the run registry (the work kind in models.py drives this module
cooperatively).

The accepted URL forms (the manager's input vocabulary):

```text
https://host/path/model.gguf            direct (any host, http/https)
https://huggingface.co/R/resolve/REV/F  direct HF resolve (any revision)
https://huggingface.co/R/blob/REV/F     rewritten blob → resolve
hf:R/F   or   hf://R/F                  shorthand → resolve/main/F
```

The derived logical_name is the URL's last path segment (the §9 law: a
file name, never a path — separators reject loudly). No percent-
decoding: a literal segment is the honest name (GGUF releases are
ASCII-named in practice; an encoded name arrives encoded, verbatim).

Failure vocabulary (the adapter's D1 family, reused by name):
"unavailable" (transport — unreachable host), "http" (the server
answered an error status), "malformed" (the body truncated against its
own Content-Length, or a URL that parses to no file name).

stdlib-only (D-012): urllib — no new runtime dependency.
"""

from __future__ import annotations

import http.client
import os
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

__all__ = [
    "CHUNK_BYTES",
    "FETCH_TIMEOUT_S",
    "HttpModelFetcher",
    "ModelFetchError",
]

#: The download chunk size — one progress observation + one abort
#: checkpoint per chunk (the §12 cooperative cadence: small enough to
#: bound the cancellation latency, large enough to keep the syscall
#: count sane on multi-GB files).
CHUNK_BYTES = 1024 * 1024

#: The per-read socket timeout (§12: transport policy, not a logical
#: deadline — the run's own absolute deadline rides the work context).
FETCH_TIMEOUT_S = 60.0

#: The honest User-Agent (the operator-facing identity on the wire —
#: some hosts refuse anonymous clients; never a spoofed browser).
_USER_AGENT = "canonsim-workbench/0.1 (model-assets fetch)"

_HF_HOSTS = frozenset({"huggingface.co", "www.huggingface.co"})


class ModelFetchError(RuntimeError):
    """A fetch failure with the D1-family cause ("unavailable" |
    "http" | "malformed") — the honest observed vocabulary, never
    'it did not work'."""

    def __init__(self, cause: str, detail: str) -> None:
        super().__init__(f"[{cause}] {detail}")
        self.cause = cause


class HttpModelFetcher:
    """The fetch surface the composition root injects into the
    model.fetch work kind (models.py): `normalize` (pure — the
    admission-side URL/name resolution) and `fetch` (the streaming
    download). Injectable as one object so the application layer stays
    network-free (INV-4's injection form, the BackendPort pattern)."""

    def normalize(self, url: str) -> tuple[str, str]:
        """The operator-facing URL → (the direct fetch URL, the derived
        logical_name). Pure string law, loud on every form that parses
        to no file: the hf: shorthand, the HF blob→resolve rewrite, the
        direct URL's last path segment."""
        if not isinstance(url, str) or not url.strip():
            raise ModelFetchError("malformed", "the URL is empty")
        text = url.strip()
        if text.startswith(("hf:", "hf://")):
            rest = text[3:] if text.startswith("hf:") else text[5:]
            rest = rest.lstrip("/")
            parts = [p for p in rest.split("/") if p]
            if len(parts) < 3:
                raise ModelFetchError(
                    "malformed",
                    f"the hf: shorthand needs namespace/name/file "
                    f"(got {text!r})",
                )
            repo = "/".join(parts[:2])
            file_path = "/".join(parts[2:])
            fetch_url = (
                f"https://huggingface.co/{repo}/resolve/main/{file_path}"
            )
            return fetch_url, _safe_name(parts[-1], text)
        if not text.startswith(("http://", "https://")):
            raise ModelFetchError(
                "malformed",
                f"the URL must be http(s) or the hf: shorthand (got {text!r})",
            )
        after_scheme = text.split("://", 1)[1]
        host_part, separator, path_part = after_scheme.partition("/")
        host = host_part.split("@")[-1].split(":")[0]
        path = "/" + path_part if separator else ""
        if not path.startswith("/"):
            raise ModelFetchError(
                "malformed",
                f"the URL carries no file path (got {text!r})",
            )
        path = path.split("?", 1)[0].split("#", 1)[0]
        segments = [s for s in path[1:].split("/") if s]
        if not segments:
            raise ModelFetchError(
                "malformed",
                f"the URL carries no file path (got {text!r})",
            )
        file_name = segments[-1]
        if host.lower() in _HF_HOSTS and len(segments) >= 4:
            if segments[2] == "blob":
                segments[2] = "resolve"  # the browser URL → the fetch URL
                rebuilt = "/".join(segments)
                return (
                    f"https://huggingface.co/{rebuilt}",
                    _safe_name(file_name, text),
                )
        return text, _safe_name(file_name, text)

    def fetch(
        self,
        url: str,
        dest_dir: Path,
        logical_name: str,
        *,
        on_progress: Callable[[int, int | None], None],
        checkpoint: Callable[[], None],
    ) -> dict[str, object]:
        """The streaming download: GET → `<name>.part` → the atomic
        rename. The honest mechanics: a fresh truncating open (a
        leftover .part from a killed run restarts clean), one progress
        observation + one cooperative `checkpoint()` call per chunk
        (the §12 contract — the checkpoint RAISES to abort: the
        caller's own WorkCancelled/DeadlineExceeded carrier propagates
        through this module untouched, the registry maps it),
        Content-Length as the total when present (None — "total
        unknown" — never a guess), the truncated-body check against
        the observed length, and the best-effort .part cleanup on EVERY
        failure path (the finally guard — no residue, ever)."""
        if not isinstance(dest_dir, Path):
            raise ModelFetchError(
                "malformed", "dest_dir must be a pathlib.Path"
            )
        if not logical_name or os.sep in logical_name or (
            os.altsep and os.altsep in logical_name
        ):
            raise ModelFetchError(
                "malformed",
                f"logical_name {logical_name!r}: a plain file name",
            )
        dest_dir.mkdir(parents=True, exist_ok=True)
        final_path = dest_dir / logical_name
        part_path = dest_dir / (logical_name + ".part")
        request = urllib.request.Request(
            url, headers={"User-Agent": _USER_AGENT}, method="GET"
        )
        success = False
        downloaded = 0
        try:
            with urllib.request.urlopen(
                request, timeout=FETCH_TIMEOUT_S
            ) as response:
                if response.status != 200:
                    raise ModelFetchError(
                        "http", f"{url} answered {response.status}"
                    )
                length_header = response.headers.get("Content-Length")
                total: int | None = None
                if length_header is not None and length_header.isdigit():
                    total = int(length_header)
                with part_path.open("wb") as handle:
                    while True:
                        checkpoint()
                        chunk = response.read(CHUNK_BYTES)
                        if not chunk:
                            break
                        handle.write(chunk)
                        downloaded += len(chunk)
                        on_progress(downloaded, total)
                if total is not None and downloaded != total:
                    raise ModelFetchError(
                        "malformed",
                        f"the body is truncated: {downloaded} of "
                        f"{total} bytes (Content-Length's own claim)",
                    )
                os.replace(part_path, final_path)
                success = True
        except urllib.error.HTTPError as exc:
            raise ModelFetchError(
                "http", f"{url} answered {exc.code}: {exc.reason}"
            ) from exc
        except http.client.HTTPException as exc:
            # the body's own truncation family (IncompleteRead et al.) —
            # the malformed vocabulary's transport-side member
            raise ModelFetchError(
                "malformed", f"the body failed mid-stream: {exc}"
            ) from exc
        except (urllib.error.URLError, OSError) as exc:
            raise ModelFetchError(
                "unavailable", f"{url} unreachable: {exc}"
            ) from exc
        finally:
            if not success:
                _remove_quietly(part_path)
        return {
            "location": str(final_path),
            "logical_name": logical_name,
            "size_bytes": downloaded,
            "url": url,
        }


def _safe_name(file_name: str, source_url: str) -> str:
    """The §9 law at the fetch boundary: the logical_name is a plain
    file name (no separators, never '.'/'..') — loud otherwise."""
    if (
        not file_name
        or os.sep in file_name
        or (os.altsep and os.altsep in file_name)
        or file_name in (".", "..")
    ):
        raise ModelFetchError(
            "malformed",
            f"the URL's file name {file_name!r} (from {source_url!r}) is "
            "not a plain file name",
        )
    return file_name


def _remove_quietly(path: Path) -> None:
    """The honest cleanup's own half: a failed/aborted fetch leaves NO
    .part behind (best-effort — an unreadable directory surfaces at the
    next fetch's own open, never here)."""
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
