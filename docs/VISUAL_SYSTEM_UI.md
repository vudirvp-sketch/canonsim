# VISUAL_SYSTEM_UI.md — The Workbench Visual System and UI Engineering Law

> The owner's 2026-09-26 admission call («нынешний ui - ужасен! поэтому
> всеми тремя руками и ногами - за!» — full approval of the external
> 24-section *CanonSim Workbench — Visual System and UI Engineering
> Agent Instruction* document, delivered with the wb-10 handback).
> This file is the repo-side LAW distilled from that document — the
> original text stays with the owner (the D-024/D-200 convenience-copy
> law: external briefs are never vendored); what lives here is the
> binding form every visual row obeys. Admission: iter-229, D-211.
>
> **Routing law:** every visual/UI question on the Workbench surface
> routes HERE first; every engine/API question routes through
> `docs/REDOT_ENGINE_INDEX.md` (D-207) — the two indexes are
> complementary, never overlapping. The v5.2 frontend spec stays
> outside the repo (D-024/D-200); where this law and an external copy
> disagree, THIS file + the app spec's own §18 evidence law win.

## 0. The delivery order (the standing resolution)

1. **Functional rows first, visual rows after** — a surface that lies
   is worse than a surface that is ugly; the owner's live blockers
   (the wb-11 transport chain) land before any palette does.
2. **One row per iteration** — the visual program is NOT a standing
   parallel track; it is a family of owner-gated rows (TASKS wb-12+),
   each one row, each with its own §5 report. The external document's
   "program" framing is resolved HERE: the doc is the LAW for each
   row, never a second schedule.
3. **The app spec's §18 evidence law wins over "quiet chrome"** — the
   effective state is NEVER hidden for visual calm (the badge, the
   status labels, the honest notes stay visible); quiet chrome
   applies to decoration, never to evidence.

## 1. The grammar: surface-driven, not card-driven

The Workbench UI is a small set of semantic SURFACES (Chat, Models,
Settings — later: Inference, Prompts, History, Diagnostics,
Simulation), not a grid of floating cards. The container hierarchy:

```text
CANVAS            the window's base plane (one per shell)
SURFACE           one primary work area (exactly one visible)
CONTAINER         a semantic region INSIDE a surface (list, composer,
                  toolbar, inspector) — named by its ROLE, never by
                  its appearance
CONTENT           the user's material (messages, model rows, values)
ACTION            a control that does something (button, field)
```

A container is a rectangle with a ROLE, not a "card" with a shadow.
No decorative elevation, no fake depth, no rounded-card grids. Depth
exists ONLY where the OS/platform idiom requires it (menus,
dialogs) — and the native picker/dialog is preferred over any
in-engine imitation (the wb-10 law continues).

## 2. The token taxonomy (one source of truth: the theme)

Every visual decision routes through the semantic token set —
`workbench/presentation/redot/themes/workbench_theme.tres` stays the
single source (§10's existing law). The token names follow the role
taxonomy:

```text
CANVAS            background_base
SURFACE_*         surface planes (panel, bar, sunken rows)
CONTENT_*         text tiers (primary, secondary, disabled)
ACTION_*          control surfaces (rest, hover, pressed, disabled)
BORDER_*          separators and outlines (subtle by default)
STATE_*           status colors (success, warning, danger, busy)
AUTHORITY_*       CANONICAL | OBSERVED | DERIVED | UNKNOWN — the
                  provenance axis (scene_ir's status laws)
```

Adding a color outside a token is forbidden — a new need names a NEW
token with a role, lands in the theme, and is consumed by name.

## 3. Color law: neutral-first, ONE accent

- A neutral ramp carries the whole UI (surfaces, text, borders).
- Exactly ONE accent color exists; it marks interactive affordances
  and the live/primary state. It never decorates.
- Status colors (success/warning/danger/busy) are semantic STATE_*,
  never a second accent.
- Color is never the ONLY carrier of state (§4's not-color-only law).

## 4. Not-color-only state (the accessibility invariant)

Every state a user must ACT on is carried by at least TWO of:
{text label, icon/glyph, position/layout, motion, color}. A state
carried by color alone is a bug (the §18 matrix below names the
text/label half for every visual state — the label is mandatory).

## 5. The visual state matrix (every surface's honest states)

Each surface enumerates its states UP FRONT; a state outside the
matrix is a bug; a matrix state without a visible rendering is a bug.
The mandatory minimum set (the wb-11 rows already render these
honestly):

```text
Chat:     EMPTY | ACTIVE | GENERATING
Models:   EMPTY | DISCOVERED | ACTIVE | LOADING | FAILED
Settings: DEFAULT | EDITING | DISABLED | ERROR
```

- EMPTY is a REAL state with guidance (what to do next), never a
  blank void — and never a fabricated sample (nothing fake, §18).
- LOADING shows live progress where a run exists (the run poll's own
  note), and the surface stays USABLE while it loads (wb-11's law:
  no long call ever wedges the UI).
- FAILED shows the observed CAUSE (§21's diagnostics on the wire),
  never a bare "error".

## 6. The transplantation protocol (mechanisms, not looks)

Borrowing from any external UI source is a documented transplant:

```text
SOURCE        the exact project + file/surface
TECHNIQUE     what they did, mechanically
MECHANISM     the underlying rule that makes it work
INVARIANT     the constraint that must survive the port
ADAPTATION    what changes for the Workbench's tokens/surfaces
CONSEQUENCE   what the user gains; what it costs
```

Looks are never transplanted — a mechanism is. "They use a nice
blue" is not a mechanism; "the primary action is the only filled
button in the toolbar" is.

## 7. The reference pack (admission per AGENTS §2.8)

Research donors for the visual rows — MECHANISMS ONLY, no assets, no
vendored code; licenses checked BEFORE any port:

```text
Godot Modern/Minimal themes   token structure, theme organization
ThemeGen                      a THEME TOOL — generates candidates,
                              never a dependency, never the decision
                              source (the law: tools don't decide)
LobeHub / Jan / LM Studio /   chat surface mechanics: composer
Open WebUI                    behavior, list virtualization, state
                              notes, settings disclosure
dot-ui / Iso-Themes           neutral ramp + single-accent systems
Godot Theme Explorer          token audit/debug mechanics
editor-icons (Godot)          the icon vocabulary's shape language
SillyTavern                   LICENSE-SENSITIVE — mechanisms only,
                              never code, never assets, never look
```

## 8. The per-row UI report (every visual row closes with one)

```text
TARGET PROBLEM       the user-facing problem this row solves
CURRENT PRIMITIVE    what exists today (the honest baseline)
TRANSFERRED MECHANISM the transplant, per §6's protocol (or "none —
                     first-party" when no donor)
INVARIANT            what must NOT change (behavior, wire, tests)
FILES AFFECTED       the explicit path list
EXPECTED CONSEQUENCE the user-visible outcome
REJECT CONDITIONS    what would make the owner reject this row
VERIFICATION STATE   the proof run (tests + the REDOT_EXE-gated
                     screenshot packets where applicable)
```

## 9. Anti-patterns (rejected on sight)

- Card grids where a surface/list belongs; floating shadows on flat
  tools.
- A second accent color; gradient decoration; colored text that is
  not a link or a state.
- State by color alone; icon-only actions without tooltips/labels.
- A fake empty state (samples/fabricated content); a spinner where a
  truthful progress note exists (the run poll's own words).
- An in-engine imitation of a native dialog (the picker law).
- Any UI state that hides the effective truth (§18 wins, §0.3).

## 10. The standing row queue (owner-gated, one row at a time)

The visual rows open ONLY on the owner's call (the wb family's own
law). Candidates in dependency order — each is ONE row with a §8
report:

```text
wb-12  the token audit      — the theme reconciled to §2's taxonomy
                               (rename/retire, the neutral ramp, the
                               single accent pinned)
wb-13  the Models surface   — §5's matrix rendered over the wb-11
                               run circuits (the LOADING live note,
                               the FAILED cause, the EMPTY guidance)
wb-14  the Chat surface     — the message list's semantic containers
                               + the composer states
wb-15  the Settings surface — the DEFAULT/EDITING/DISABLED/ERROR
                               matrix + the disclosure layers
wb-16+ the later surfaces   — Inference, Prompts, History,
                               Diagnostics, Simulation (each opens
                               with its functional row first)
```

The order is dependency logic, not a schedule — the owner reorders
freely; a row opens when named. The FRONTEND_UIUX_LAW §25 order
(iter-233, D-214) re-points the queue's position in the whole-frontend
plan: the P0 minimums row (ux-1) and the Observatory slice (obs-1)
run BEFORE indefinite peripheral polish — the visual rows wb-13+
are the P2 continuation, each still its own owner-gated row here.

## 11. Mandatory companion requirements (the spec-integrity repair)

This file is the VISUAL law owner — one layer of the frontend law,
never the whole of it. The following requirements are BINDING on
every visual row and live in their owning law
(`docs/FRONTEND_UIUX_LAW.md`, admitted iter-233/D-214 over the
owner's Ultimate Frontend/UI/UX/Visual Architecture pack; the
D-024/D-200 no-vendoring law). This routing block is the §1 repair
of the drift the pack diagnosed: the short law was an accidental
lossy compression of the approved requirements (accessibility,
keyboard/focus, reduced motion, responsive/DPI, localization were
materially missing) — an INDEX, never permission to forget:

```text
Accessibility (WCAG 2.2 + ISO 9241-171:2025 baseline) — LAW §15
Focus/keyboard contract (order, entry, restoration, Escape)  — LAW §15
Reduced-motion policy (the static-equivalent law)            — LAW §15
Responsive/DPI/multi-monitor (viewport classes + min-size)  — LAW §16
Localization (the _tr boundary + Cyrillic-safe layout)        — LAW §17
Observatory interaction grammar (selection/context/evidence) — LAW §3..§9
Verification (static ≠ runtime ≠ task proof + the A–I gates)   — LAW §22
```

A visual row that satisfies THIS file while violating a companion
requirement is NOT compliant — the §8 report checks the companion
set too.
