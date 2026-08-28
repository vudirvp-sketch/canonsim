"""Brief assembly for the mediator: the deterministic block pipeline
(`docs/BRIEF_SPEC.md` owns the contract). Landed iter-8; the LLM side of
the pipeline is a later, owner-gated iteration (AGENTS §8)."""

from brief.assembler import (
    Block,
    Brief,
    assemble_brief,
    beats_crossed,
    brief_from_log,
    last_beat_tick,
    render_brief,
    token_count,
)

__all__ = [
    "Block",
    "Brief",
    "assemble_brief",
    "beats_crossed",
    "brief_from_log",
    "last_beat_tick",
    "render_brief",
    "token_count",
]
