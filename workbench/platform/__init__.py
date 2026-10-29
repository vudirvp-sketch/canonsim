"""The platform envelope (§5's skeleton: `workbench/platform/` owns
OS/platform mechanics — process spawn/termination/observation over
injected seams; no engine imports, no semantics).

wb-9's one exception, owner-gated (D-208, the owner's 2026-09-25
«подтянуть модель откуда угодно» call): `model_fetch.py` is the THIRD
sanctioned network module (INV-4's outbound model-assets fetch — HTTP
GET downloads only). Every other platform row stays network-free."""
