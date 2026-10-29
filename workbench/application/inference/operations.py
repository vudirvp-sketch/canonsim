"""The inference gateway family (ssi-4 step 3, iter-249 — extracted
verbatim).

The wiring the composition root calls (§6.1's single-owner law): the
READ (the resolved controls document + the injected compiled preview
+ the managed liveness) and the UPDATE (the closed partial document,
validated through the store, the honest next-spawn note) +
effective_temperature (the chat row's BASE-temperature provider,
§19.1's BASE layer — composition.py's injected callable). The preview
and liveness callables are INJECTED — this module never imports the
platform or the managed backend (settings.py's own seam).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from workbench.api.gateway import (
    Gateway,
    OperationRejected,
    OperationSpec,
)
from workbench.application.inference.library import InferenceError
from workbench.application.inference.resolver import resolve
from workbench.application.inference.store import InferenceStore

# ------------------------------------------------------------ operations


def _rejected(reason: str) -> OperationRejected:
    return OperationRejected("DOMAIN_REJECTED", reason)


def register_inference_operations(
    gateway: Gateway,
    store: InferenceStore,
    *,
    compiled_preview: Callable[[Mapping[str, object]], str] | None = None,
    managed_live: Callable[[], bool] | None = None,
) -> None:
    """The inference family's wiring (the composition root calls it —
    §6.1's single-owner law): the READ (the resolved controls
    document + the injected compiled preview + the managed liveness)
    and the UPDATE (the closed partial document, validated through
    the store, the honest next-spawn note). The preview and liveness
    callables are INJECTED — this module never imports the platform
    or the managed backend (settings.py's own seam)."""
    gateway.register(
        OperationSpec(
            name="inference.read",
            kind="READ",
            handler=_make_inference_read(store, compiled_preview, managed_live),
            description=(
                "the resolved inference-control document (§19.1's "
                "effective state per control) + the compiled preview — "
                "the Inference surface's own read"
            ),
        )
    )
    gateway.register(
        OperationSpec(
            name="inference.update",
            kind="MUTATION",
            handler=_make_inference_update(store, compiled_preview, managed_live),
            session_scoped=True,
            description=(
                "the closed partial update over the semantic profile "
                "(validated, persisted — effective at the NEXT managed "
                "spawn, §11.1's replacement path being a later row)"
            ),
        )
    )


def _inference_document(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
    *,
    request_temperature: float | None = None,
) -> dict[str, object]:
    """The read model: the RESOLVED document (the effective state per
    control — the law's §6/§8) + the workspace's pinned ids + the
    compiled-preview evidence + the honest next-spawn note (a LIVE
    server keeps its spawn flags until unloaded — settings.py's own
    law, verbatim)."""
    profile = store.current()
    resolved = resolve(profile, request_temperature=request_temperature)
    live_now = bool(live is not None and live())
    pinned = list(store.pinned())
    document: dict[str, object] = {
        **resolved,
        "profile": profile.as_document(),
        "pinned": pinned,
        "managed_live": live_now,
        "applies": "next-spawn",
    }
    if compiled_preview is not None:
        document["compiled_preview"] = compiled_preview(
            profile.as_document()
        )
    else:
        document["compiled_preview"] = None
    if live_now:
        document["note"] = (
            "a LIVE server keeps its spawn flags until unloaded — the "
            "saved values apply at the next model.load"
        )
    return document


def _make_inference_read(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        if context.arguments:
            raise _rejected(
                f"inference.read: takes no arguments "
                f"({sorted(context.arguments)})"
            )
        return _inference_document(store, compiled_preview, live)

    return handler


def _make_inference_update(
    store: InferenceStore,
    compiled_preview: Callable[[Mapping[str, object]], str] | None,
    live: Callable[[], bool] | None,
):
    def handler(context) -> Mapping[str, object]:
        arguments = dict(context.arguments)
        try:
            store.update(arguments)
        except InferenceError as exc:
            raise _rejected(f"inference.update: {exc}") from exc
        if context.effects is not None:
            context.effects.effect(
                {
                    "effect": "INFERENCE_UPDATED",
                    "fields": sorted(
                        key for key in arguments if key != "sampler_chain"
                    ),
                }
            )
        return _inference_document(store, compiled_preview, live)

    return handler


def effective_temperature(store: InferenceStore) -> float:
    """The chat row's BASE-temperature provider (§19.1's BASE layer —
    composition.py's injected callable): the resolved profile's
    effective temperature, the value a chat.send WITHOUT an explicit
    temperature resolves from (the explicit call-local value always
    wins, backend.py's own law)."""
    profile = store.current()
    resolved = resolve(profile)
    for control in resolved["controls"]:  # type: ignore[union-attr]
        if control["id"] == "sampling.temperature":  # type: ignore[index]
            value = control["value"]
            if isinstance(value, (int, float)) and not isinstance(
                value, bool
            ):
                return float(value)
    return float(profile.values.get("temperature", 0.8))  # type: ignore[arg-type]
