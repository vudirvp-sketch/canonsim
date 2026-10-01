/**
 * The Inference surface (Phase 3's fifth row) — the semantic
 * generation-control WORKSPACE over the two EXISTING gateway ops:
 * `inference.read` (the full resolved control document) +
 * `inference.update` (the closed partial MUTATION over the profile
 * store). The DEPLOYMENT knobs live in Settings — the inf-1 split
 * (LLAMA_CPP_INFERENCE_CONTROL_LAW §1); the full control depth lives
 * HERE, never in Chat (§17/§21.2: Chat carries only the compact
 * projection + the link).
 *
 * THE WORKSPACE'S OWN REGIONS (§21.2, inf-2's named shape — every
 * region builds ON the read: an offline surface stays honestly
 * empty, never composed-before-read):
 * - the PRESET ROW — a TRANSPARENT diff preview (every field the
 *   apply would change, old → new), never an opaque mode; the apply
 *   is a plain update, guarded on a CLEAN draft (a preset never
 *   silently modifies out-of-scope settings);
 * - the SEARCH field (name/flag/category — the §32 match families);
 *   a search match is an EXPLICIT ASK: it shows the advanced rows
 *   too; the cleared search restores the rung and the disclosures;
 * - the PINNED quick-access strip — REVEALS (open the category +
 *   highlight the row), never second editors; a pin/unpin is its
 *   own explicit dispatch over the workspace section;
 * - the COLLAPSIBLE categories with honest counts (the six
 *   general-chat categories open by default — every other family one
 *   disclosure click away, never a flat 85-control wall);
 * - the ADVANCED rung — the expert controls hidden until asked;
 * - the SAMPLER CHAIN — the ordered 9-member first-class object
 *   (membership is a DRAFT edit; the value families stay configured);
 * - the COMPILED PREVIEW — the technical artifact, read-only,
 *   collapsed behind its own disclosure (never the authoring
 *   language).
 *
 * The control editors are DATA-DRIVEN over the read document's own
 * metadata (kind/value_type/forms/limits — the UI never re-encodes
 * the vocabulary; a new control lands by the server's document
 * alone). Every row renders the OBSERVED state + the resolver's own
 * reasons verbatim (§7: configured-but-ineffective controls stay
 * VISIBLE, never hidden) and the §4 defaults ladder side by side
 * (baseline · upstream — never silently reconciled).
 *
 * EFFECTIVE-STATE CLOSURE (§8): the draft is a REQUEST (the DRAFT
 * marker per row + the strip); the Save is ONE explicit dispatch
 * sending ONLY the changed keys; on ACCEPTED the returned document
 * is the new OBSERVED baseline and the draft reconciles to the
 * SERVER's answer; `applies: next-spawn` verbatim (a LIVE server
 * keeps its spawn flags until unloaded — the note rides verbatim).
 * No polling: the profile does not change under the reader; every
 * read and every update is the user's explicit action.
 */
import { useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";

import type { GatewayClient } from "../../api/gateway/client.ts";
import type {
  InferenceControlDocument,
  InferenceDocument,
  InferencePreset,
} from "../../api/gateway/contracts.ts";
import type { InferenceLoad, InferenceUpdateLane } from "./useInference.ts";
import { useInference } from "./useInference.ts";

export interface InferenceProps {
  readonly client: GatewayClient;
  /** the UPDATE is session-scoped: null disables every mutation
   * honestly (the READ stays available — it is session-free). */
  readonly sessionId: string | null;
  readonly className?: string;
}

/** The six general-chat categories a new workspace opens with (the
 * law §15's own list, the Redot-era mechanism carried verbatim);
 * every other family stays one disclosure click away. */
const DEFAULT_OPEN_CATEGORIES: readonly string[] = [
  "model",
  "device",
  "memory",
  "moe",
  "sampling",
  "chat",
];

export function Inference(props: InferenceProps): ReactNode {
  const inference = useInference({ client: props.client, sessionId: props.sessionId });
  const { load, draft } = inference;

  // The component's own PRESENTATION state (§7's allowance: UI
  // open/closed/scroll — per-surface, volatile, never a truth claim).
  const [search, setSearch] = useState("");
  const [advancedRung, setAdvancedRung] = useState(false);
  const [openCategories, setOpenCategories] = useState<ReadonlySet<string>>(
    () => new Set<string>(DEFAULT_OPEN_CATEGORIES),
  );
  const [selectedPresetId, setSelectedPresetId] = useState<string | null>(null);
  const [revealId, setRevealId] = useState<string | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const searchRef = useRef<HTMLInputElement>(null);

  // Task-aware focus entry (§15): the workspace → the search field.
  useEffect(() => {
    searchRef.current?.focus();
  }, []);

  const query = search.trim().toLowerCase();
  const searching = query !== "";

  const toggleCategory = (category: string): void => {
    setOpenCategories((previous) => {
      const next = new Set(previous);
      if (next.has(category)) {
        next.delete(category);
      } else {
        next.add(category);
      }
      return next;
    });
  };

  /** The pinned chip's REVEAL: open the category + mark the row (a
   * quick-access reveal, never a second editor); the scroll is
   * best-effort (jsdom never implements it — the marker is the
   * testable artifact). */
  const revealControl = (controlId: string, category: string): void => {
    setOpenCategories((previous) => new Set(previous).add(category));
    setRevealId(controlId);
    const row = document.querySelector<HTMLElement>(
      `[data-testid="control-${controlId}"]`,
    );
    try {
      row?.scrollIntoView?.({ block: "nearest" });
    } catch {
      // jsdom: not implemented — the reveal marker is the artifact
    }
  };

  const document_ = load.kind === "LOADED" ? load.result : null;
  const selectedPreset =
    document_ !== null && selectedPresetId !== null
      ? (document_.presets.find((preset) => preset.id === selectedPresetId) ?? null)
      : null;

  const mutationsDisabled = props.sessionId === null;

  return (
    <section
      className={props.className ?? "surface"}
      aria-label="Inference — the generation-control workspace"
    >
      <header className="surface-header">
        <h2>
          Inference <span className="tag tag-config">CONTROL · SEMANTIC</span>
        </h2>
        <p className="surface-note">
          the semantic generation-control workspace — the chip library, the sampler chain, the
          effective-state presentation; the profile persists, effective at the NEXT spawn; the
          compiled command is a technical artifact, never the authoring language
        </p>
      </header>

      <LoadLane load={load} />

      {document_ !== null && draft !== null ? (
        <>
          <div className="strip" data-testid="inference-context">
            <span>
              profile{" "}
              <label className="strip-edit">
                <input
                  data-testid="inference-profile-name"
                  value={draft.name}
                  disabled={inference.busy}
                  onChange={(event) => inference.editName(event.target.value)}
                />
              </label>
            </span>
            <span>
              applies <code>{document_.applies}</code>
            </span>
            <span>
              managed{" "}
              <code>{document_.managed_live ? "LIVE" : "down"}</code>
            </span>
            <span>
              chain <code>{document_.chain_order.length} members</code>
            </span>
            <span>
              deterministic <code>{document_.deterministic ? "yes (temp 0)" : "no"}</code>
            </span>
            {inference.dirty ? (
              <span className="tag tag-config" data-testid="inference-dirty">
                DRAFT — unsaved changes
              </span>
            ) : (
              <span className="tag">draft matches the observed document</span>
            )}
            {mutationsDisabled ? (
              <span className="freshness freshness-stale">no session — updates disabled</span>
            ) : null}
          </div>

          {document_.managed_live && document_.note !== undefined ? (
            <div className="banner banner-stale" role="note">
              {document_.note}
            </div>
          ) : null}

          {/* THE PRESET ROW — a transparent diff preview, never an opaque mode. */}
          <div className="workspace-row" data-testid="inference-presets">
            <select
              aria-label="preset — a transparent starting point"
              value={selectedPresetId ?? ""}
              onChange={(event) =>
                setSelectedPresetId(event.target.value === "" ? null : event.target.value)
              }
            >
              <option value="">(no preset selected — inspect one, apply explicitly)</option>
              {document_.presets.map((preset) => (
                <option key={preset.id} value={preset.id}>
                  {preset.name}
                </option>
              ))}
            </select>
            {selectedPreset !== null ? (
              <PresetPreview
                preset={selectedPreset}
                document={document_}
                applyDisabled={
                  inference.busy ||
                  inference.dirty ||
                  mutationsDisabled
                }
                onApply={() => void inference.applyPreset(selectedPreset.id)}
              />
            ) : null}
          </div>

          {/* THE SEARCH + ADVANCED RUNG row. */}
          <div className="workspace-row">
            <input
              ref={searchRef}
              type="search"
              aria-label="search controls (name, flag, category)"
              placeholder="search — name, flag, or category; a match shows the advanced rows too"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              data-testid="inference-search"
            />
            <label className="strip-check">
              <input
                type="checkbox"
                checked={advancedRung}
                onChange={(event) => setAdvancedRung(event.target.checked)}
              />{" "}
              advanced controls
            </label>
          </div>

          {/* THE PINNED STRIP — quick-access reveals, never second editors. */}
          <PinnedStrip
            document={document_}
            onReveal={revealControl}
            onUnpin={(controlId) => void inference.togglePinned(controlId)}
            unpinDisabled={inference.busy || mutationsDisabled}
          />

          {/* THE SAMPLER CHAIN — the ordered first-class object. */}
          <ChainRegion
            document={document_}
            draftChain={draft.chain}
            disabled={inference.busy}
            onToggleMember={inference.toggleChainMember}
          />

          {/* THE CATEGORIES — collapsible, honest counts, the advanced
              rung, the search filter; builds ON the read. */}
          <div className="inference-categories">
            {document_.categories.map((category) => {
              const members = document_.controls.filter(
                (control) => control.category === category.id,
              );
              const visible = members.filter((control) =>
                controlVisible(control, query, searching, advancedRung),
              );
              if (!searching && visible.length === 0 && members.length === 0) return null;
              if (searching && visible.length === 0) return null;
              const open = searching || openCategories.has(category.id);
              const hiddenByRung = members.length - visible.length;
              return (
                <section
                  key={category.id}
                  className="category-section"
                  data-testid={`category-${category.id}`}
                >
                  <button
                    type="button"
                    className="category-toggle"
                    aria-expanded={open}
                    onClick={() => toggleCategory(category.id)}
                  >
                    <span aria-hidden="true">{open ? "▾" : "▸"}</span>{" "}
                    <span className="category-title">{category.id}</span>{" "}
                    <span className="category-count">
                      {visible.length}/{category.controls}
                    </span>
                  </button>
                  {open
                    ? visible.map((control) => (
                        <ControlRow
                          key={control.id}
                          control={control}
                          draftValue={draft.values[control.field]}
                          draftDirty={draft.values[control.field] !== control.value}
                          pinned={document_.pinned.includes(control.id)}
                          revealed={revealId === control.id}
                          disabled={inference.busy}
                          onEdit={inference.editValue}
                          onValidity={inference.markFieldValidity}
                          onTogglePin={(controlId) => void inference.togglePinned(controlId)}
                          pinDisabled={inference.busy || mutationsDisabled}
                        />
                      ))
                    : null}
                  {open && visible.length === 0 && members.length > 0 ? (
                    <p className="empty-inspector">
                      all {String(hiddenByRung)} of this family&rsquo;s controls sit on the
                      advanced rung — ask for them (the checkbox above) or search for one by
                      name/flag
                    </p>
                  ) : null}
                </section>
              );
            })}
            {searching &&
            document_.categories.every((category) =>
              document_.controls
                .filter((control) => control.category === category.id)
                .every((control) => !controlVisible(control, query, true, advancedRung)),
            ) ? (
              <p className="empty" data-testid="inference-no-match">
                NO MATCH — no control&rsquo;s name, flag, or category contains &ldquo;{search.trim()}
                &rdquo; (the library is the server&rsquo;s own document, never a client list)
              </p>
            ) : null}
          </div>

          {/* THE SAVE CONTROLS — one explicit dispatch, only the changed keys. */}
          <div className="controls">
            <button onClick={() => void inference.refresh()} disabled={inference.busy}>
              re-read profile
            </button>
            <button
              onClick={inference.resetDraft}
              disabled={inference.busy || !inference.dirty}
            >
              reset draft
            </button>
            <button
              onClick={() => void inference.saveChanges()}
              disabled={
                inference.busy ||
                !inference.dirty ||
                mutationsDisabled ||
                inference.invalidFields.size > 0
              }
              data-testid="inference-save"
            >
              save changes
            </button>
            <span className="controls-note">
              save sends ONLY the changed keys (absent fields unchanged) with a fresh idempotency
              key — one explicit attempt, never a blind retry; a pin/unpin is its own dispatch
            </span>
          </div>
          {inference.invalidFields.size > 0 ? (
            <div className="banner banner-stale" role="note">
              {[...inference.invalidFields].length === 1
                ? "one editor holds a value that is not a legal explicit value yet"
                : `${String(inference.invalidFields.size)} editors hold values that are not legal explicit values yet`}{" "}
              — the save stays disabled (the store validates loudly anyway; this is the honest
              client-side gate)
            </div>
          ) : null}

          <UpdateLane update={inference.update} />

          {/* THE COMPILED PREVIEW — the technical artifact, read-only. */}
          <div className="workspace-row">
            <button type="button" onClick={() => setShowPreview((value) => !value)}>
              {showPreview ? "hide" : "show"} the next spawn&rsquo;s compiled command
            </button>
          </div>
          {showPreview ? (
            <div className="preview-block">
              <h3>the next spawn&rsquo;s compiled command (the composition root&rsquo;s view)</h3>
              <pre className="command-preview" data-testid="inference-preview">
                {document_.compiled_preview ??
                  "(no preview — the composition did not inject one)"}
              </pre>
            </div>
          ) : null}
        </>
      ) : load.kind === "NOT_LOADED" || load.kind === "LOADING" ? (
        <p className="empty" data-testid="inference-empty">
          the control document not read yet — the workspace builds ON the read (an offline
          surface stays honestly empty, never composed-before-read)
        </p>
      ) : null}
    </section>
  );
}

// ------------------------------------------------------------ the regions

/** One control's visibility: the search filter (a match is an
 * explicit ask — it shows the advanced rows too) over the advanced
 * rung (the expert controls hidden until asked). */
function controlVisible(
  control: InferenceControlDocument,
  query: string,
  searching: boolean,
  advancedRung: boolean,
): boolean {
  if (control.advanced && !advancedRung && !searching) return false;
  if (!searching) return true;
  const haystack = `${control.name} ${control.flag} ${control.category}`.toLowerCase();
  return haystack.includes(query);
}

/** The preset's TRANSPARENT diff — every field the apply would
 * change, old → new (unchanged fields ride nothing; the preview is
 * the REQUEST, the apply the user's explicit action). */
function presetDiffLines(
  document: InferenceDocument,
  preset: InferencePreset,
): string[] {
  const byField = new Map(document.controls.map((control) => [control.field, control]));
  const lines: string[] = [];
  for (const [field, incoming] of Object.entries(preset.values)) {
    const control = byField.get(field);
    const current = control?.value;
    if (current === incoming) continue;
    const name = control?.name ?? field;
    lines.push(`${name}: ${valueText(current)} → ${valueText(incoming)}`);
  }
  return lines;
}

function PresetPreview(props: {
  readonly preset: InferencePreset;
  readonly document: InferenceDocument;
  readonly applyDisabled: boolean;
  readonly onApply: () => void;
}): ReactNode {
  const lines = presetDiffLines(props.document, props.preset);
  return (
    <div className="preset-preview" data-testid="inference-preset-preview">
      <p className="preset-description">{props.preset.description}</p>
      {lines.length > 0 ? (
        <ul className="preset-diff" data-testid="inference-preset-diff">
          {lines.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      ) : (
        <p className="empty-inspector">
          every preset field already matches the observed profile — the apply would change
          nothing
        </p>
      )}
      <div className="controls">
        <button
          type="button"
          onClick={props.onApply}
          disabled={props.applyDisabled}
          data-testid="inference-preset-apply"
        >
          apply preset
        </button>
        <span className="controls-note">
          a PLAIN update — the values land editable, never an opaque mode; the apply needs a
          CLEAN draft (a preset never silently modifies out-of-scope settings)
        </span>
      </div>
    </div>
  );
}

/** The pinned quick-access strip — reveals, never second editors. */
function PinnedStrip(props: {
  readonly document: InferenceDocument;
  readonly onReveal: (controlId: string, category: string) => void;
  readonly onUnpin: (controlId: string) => void;
  readonly unpinDisabled: boolean;
}): ReactNode {
  const byId = new Map(props.document.controls.map((control) => [control.id, control]));
  if (props.document.pinned.length === 0) {
    return (
      <p className="empty-inspector" data-testid="inference-pinned-empty">
        nothing pinned — pin a control&rsquo;s chip for a quick-access reveal (an explicit
        personal pin, the workspace&rsquo;s own section, never a profile value)
      </p>
    );
  }
  return (
    <div className="pinned-strip" data-testid="inference-pinned">
      {props.document.pinned.map((controlId) => {
        const control = byId.get(controlId);
        return (
          <span key={controlId} className="pinned-chip">
            <button
              type="button"
              className="pinned-reveal"
              onClick={() =>
                control !== undefined
                  ? props.onReveal(control.id, control.category)
                  : undefined
              }
              title={
                control !== undefined
                  ? `reveal ${control.name} (${control.flag}) in its category`
                  : "a pinned id with no control in the current library (the server's own document)"
              }
            >
              {control?.name ?? controlId}
            </button>
            <button
              type="button"
              className="pinned-unpin"
              onClick={() => props.onUnpin(controlId)}
              disabled={props.unpinDisabled}
              aria-label={`unpin ${control?.name ?? controlId}`}
            >
              ×
            </button>
          </span>
        );
      })}
    </div>
  );
}

/** The sampler chain — the ordered 9-member first-class object: the
 * membership is a DRAFT edit (the whole 9-member document rides the
 * Save), the OBSERVED state/reasons the resolver's own answer. */
function ChainRegion(props: {
  readonly document: InferenceDocument;
  readonly draftChain: readonly { readonly id: string; readonly enabled: boolean }[];
  readonly disabled: boolean;
  readonly onToggleMember: (chainId: string) => void;
}): ReactNode {
  return (
    <section className="chain-region" aria-label="the sampler chain">
      <h3>
        the sampler chain{" "}
        <span className="tag">
          {props.document.chain_order.length} members · the emitted --samplers order
        </span>
      </h3>
      <ol className="chain-list" data-testid="inference-chain">
        {props.document.sampler_chain.map((member) => {
          const draftMember = props.draftChain.find((item) => item.id === member.id);
          const membershipDraft =
            draftMember !== undefined && draftMember.enabled !== member.enabled;
          return (
            <li
              key={member.id}
              className={`chain-member ${membershipDraft ? "chain-member-draft" : ""}`}
              data-testid={`chain-${member.id}`}
            >
              <label className="strip-check">
                <input
                  type="checkbox"
                  checked={draftMember?.enabled ?? member.enabled}
                  disabled={props.disabled}
                  onChange={() => props.onToggleMember(member.id)}
                />{" "}
                <span className="chain-order" aria-hidden="true">
                  {String(member.order + 1)}.
                </span>{" "}
                <span className="chain-name">{member.name}</span>
              </label>
              <span className={`control-state state-${member.state.toLowerCase()}`}>
                {member.state}
              </span>
              {membershipDraft ? (
                <span className="tag tag-config">DRAFT — membership changes with the save</span>
              ) : null}
              {member.reasons.length > 0 ? (
                <ul className="control-reasons">
                  {member.reasons.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>
              ) : null}
            </li>
          );
        })}
      </ol>
      <p className="controls-note">
        membership and value are separate concerns — disabling a member removes it from the
        emitted chain while its value family stays configured (INEFFECTIVE with its reason);
        the order is the runtime&rsquo;s own reviewed order (reordering is a later row)
      </p>
    </section>
  );
}

// -------------------------------------------------------------- the rows

/** One control's row: the name (primary), the flag (the raw mapping),
 * the data-driven editor, the OBSERVED state + the resolver's own
 * reasons verbatim, the §4 defaults ladder side by side, and the
 * pin affordance. */
function ControlRow(props: {
  readonly control: InferenceControlDocument;
  readonly draftValue: unknown;
  readonly draftDirty: boolean;
  readonly pinned: boolean;
  readonly revealed: boolean;
  readonly disabled: boolean;
  readonly onEdit: (field: string, value: unknown) => void;
  readonly onValidity: (field: string, valid: boolean) => void;
  readonly onTogglePin: (controlId: string) => void;
  readonly pinDisabled: boolean;
}): ReactNode {
  const { control } = props;
  const notesTitle =
    control.notes.length > 0 ? control.notes.join(" | ") : undefined;
  return (
    <article
      className={[
        "control-row",
        props.revealed ? "control-row-revealed" : "",
        props.draftDirty ? "control-row-draft" : "",
      ]
        .filter(Boolean)
        .join(" ")}
      data-testid={`control-${control.id}`}
      data-reveal={props.revealed ? "true" : undefined}
    >
      <div className="control-head">
        <button
          type="button"
          className="pin-button"
          onClick={() => props.onTogglePin(control.id)}
          disabled={props.pinDisabled}
          aria-pressed={props.pinned}
          aria-label={`${props.pinned ? "unpin" : "pin"} ${control.name}`}
          title={
            props.pinned
              ? "unpin — remove from the quick-access strip"
              : "pin — add to the quick-access strip (the workspace's own section)"
          }
        >
          {props.pinned ? "★" : "☆"}
        </button>
        <span className="control-name" title={notesTitle}>
          {control.name}
        </span>
        <code className="control-flag" title={control.value_doc}>
          {control.flag}
        </code>
        <span
          className={`control-state state-${control.state.toLowerCase()}`}
          data-testid={`state-${control.id}`}
        >
          {control.state}
        </span>
        {control.advanced ? <span className="tag">advanced</span> : null}
        {control.scope !== "spawn" ? (
          <span className="tag" title="the scope model — this control also rides the request layer">
            {control.scope}
          </span>
        ) : null}
        {props.draftDirty ? (
          <span className="tag tag-config" data-testid={`draft-${control.id}`}>
            DRAFT
          </span>
        ) : null}
      </div>
      <p className="control-doc">
        {control.value_doc} · baseline <code>{valueText(control.baseline)}</code> · upstream{" "}
        <code>{valueText(control.upstream_default)}</code>
        {control.source !== "profile" ? ` · source ${control.source}` : ""}
      </p>
      <div className="control-editor">
        <ControlEditor
          control={control}
          value={props.draftValue}
          disabled={props.disabled}
          onCommit={(value) => props.onEdit(control.field, value)}
          onValidity={(valid) => props.onValidity(control.field, valid)}
        />
      </div>
      {control.reasons.length > 0 ? (
        <ul className="control-reasons" data-testid={`reasons-${control.id}`}>
          {control.reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      ) : null}
    </article>
  );
}

/** The DATA-DRIVEN editor factory — the read document's own
 * value_type/forms/limits metadata builds the editor; the UI never
 * re-encodes the vocabulary (a new control lands by the server's
 * document alone). */
function ControlEditor(props: {
  readonly control: InferenceControlDocument;
  readonly value: unknown;
  readonly disabled: boolean;
  readonly onCommit: (value: unknown) => void;
  readonly onValidity: (valid: boolean) => void;
}): ReactNode {
  const { control } = props;
  const testId = `editor-${control.id}`;
  if (control.value_type === "int" || control.value_type === "float") {
    return (
      <NumberEditor
        testId={testId}
        control={control}
        value={props.value}
        disabled={props.disabled}
        onCommit={props.onCommit}
        onValidity={props.onValidity}
      />
    );
  }
  if (control.value_type === "bool") {
    return (
      <input
        type="checkbox"
        data-testid={testId}
        checked={props.value === true}
        disabled={props.disabled}
        onChange={(event) => props.onCommit(event.target.checked)}
      />
    );
  }
  if (control.value_type === "enum") {
    const current = valueText(props.value);
    const options = control.forms.includes(current)
      ? control.forms
      : [current, ...control.forms];
    return (
      <select
        data-testid={testId}
        value={current}
        disabled={props.disabled}
        onChange={(event) => props.onCommit(event.target.value)}
      >
        {options.map((form) => (
          <option key={form} value={form}>
            {form}
          </option>
        ))}
      </select>
    );
  }
  if (control.value_type === "gpu_layers") {
    return (
      <GpuLayersEditor
        testId={testId}
        control={control}
        value={props.value}
        disabled={props.disabled}
        onCommit={props.onCommit}
        onValidity={props.onValidity}
      />
    );
  }
  return (
    <input
      type="text"
      data-testid={testId}
      value={typeof props.value === "string" ? props.value : valueText(props.value)}
      disabled={props.disabled}
      onChange={(event) => props.onCommit(event.target.value)}
    />
  );
}

/** The numeric editor — the local text holds the in-flight edit (an
 * invalid entry stays VISIBLE with the invalid marker; the commit
 * lands only legal parsed values; the save stays disabled while any
 * invalid rides — the Chat row's own honest form). */
function NumberEditor(props: {
  readonly testId: string;
  readonly control: InferenceControlDocument;
  readonly value: unknown;
  readonly disabled: boolean;
  readonly onCommit: (value: number) => void;
  readonly onValidity: (valid: boolean) => void;
}): ReactNode {
  const [text, setText] = useState<string>(() => numericText(props.value));
  useEffect(() => {
    setText(numericText(props.value));
  }, [props.value]);
  const onChange = (raw: string): void => {
    setText(raw);
    const parsed = parseNumeric(raw, props.control);
    if (parsed.valid) {
      props.onCommit(parsed.value);
      props.onValidity(true);
    } else {
      props.onValidity(false);
    }
  };
  return (
    <input
      type="number"
      data-testid={props.testId}
      value={text}
      disabled={props.disabled}
      min={props.control.minimum ?? undefined}
      max={props.control.maximum ?? undefined}
      step={props.control.step}
      onChange={(event) => onChange(event.target.value)}
    />
  );
}

/** The GPU-layers composite — the runtime's own literal forms
 * ('auto' | 'all') + the explicit count editor ('explicit' is the
 * UI-local mode; the commit is the runtime's own value form). */
function GpuLayersEditor(props: {
  readonly testId: string;
  readonly control: InferenceControlDocument;
  readonly value: unknown;
  readonly disabled: boolean;
  readonly onCommit: (value: unknown) => void;
  readonly onValidity: (valid: boolean) => void;
}): ReactNode {
  const [form, setForm] = useState<string>(() =>
    typeof props.value === "string" ? props.value : "explicit",
  );
  const [countText, setCountText] = useState<string>(() =>
    typeof props.value === "number" ? String(props.value) : "",
  );
  useEffect(() => {
    if (typeof props.value === "string") {
      setForm(props.value);
    } else if (typeof props.value === "number") {
      setForm("explicit");
      setCountText(String(props.value));
    }
  }, [props.value]);
  const commitCount = (raw: string): void => {
    setCountText(raw);
    const parsed = parseNumeric(raw, props.control);
    if (parsed.valid) {
      props.onCommit(parsed.value);
      props.onValidity(true);
    } else {
      props.onValidity(false);
    }
  };
  return (
    <span className="gpu-layers-editor">
      <select
        data-testid={`${props.testId}-form`}
        value={form}
        disabled={props.disabled}
        onChange={(event) => {
          const next = event.target.value;
          setForm(next);
          if (next === "auto" || next === "all") {
            props.onCommit(next);
            props.onValidity(true);
          } else if (countText !== "") {
            const parsed = parseNumeric(countText, props.control);
            if (parsed.valid) {
              props.onCommit(parsed.value);
              props.onValidity(true);
            } else {
              props.onValidity(false);
            }
          }
        }}
      >
        {["auto", "all", "explicit"].map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      {form === "explicit" ? (
        <input
          type="number"
          data-testid={props.testId}
          value={countText}
          disabled={props.disabled}
          max={props.control.maximum ?? undefined}
          placeholder="layers"
          onChange={(event) => commitCount(event.target.value)}
        />
      ) : null}
    </span>
  );
}

// -------------------------------------------------------------- the lanes

/** The read's honest lanes — never collapsed into one spinner. */
function LoadLane(props: { readonly load: InferenceLoad }): ReactNode {
  const { load } = props;
  if (load.kind === "NOT_LOADED" || load.kind === "LOADING") return null;
  if (load.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        inference.read TRANSPORT · {load.failure} — the gateway may be down; the re-read is
        your explicit retry
      </div>
    );
  }
  if (load.kind === "MISMATCH") {
    return (
      <div className="banner banner-error" role="alert">
        inference.read CONTRACT MISMATCH · {load.error} — reported, never coerced
      </div>
    );
  }
  if (load.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        inference.read REJECTED · {load.rejection}: {load.reason ?? "(no reason)"}
      </div>
    );
  }
  return null;
}

/** The last explicit update's closure — the stages rendered as
 * stages (§8), for every action (save / preset / pin). */
function UpdateLane(props: { readonly update: InferenceUpdateLane }): ReactNode {
  const { update } = props;
  if (update.kind === "IDLE") return null;
  if (update.kind === "UPDATING") {
    return (
      <p className="empty">
        updating ({update.action}) {update.requested.join(", ")}…
      </p>
    );
  }
  if (update.kind === "UPDATED") {
    return (
      <div className="banner banner-accepted" data-testid="inference-update-closure">
        UPDATED ({update.action}) — requested [{update.requested.join(", ")}] accepted;
        EFFECTIVE at the NEXT managed spawn (applies: {update.result.applies})
        {update.result.managed_live
          ? " — the LIVE server keeps its spawn flags until unloaded"
          : ""}
      </div>
    );
  }
  if (update.kind === "REJECTED") {
    return (
      <div className="banner banner-error" role="alert">
        update ({update.action}) REJECTED · {update.rejection}: {update.reason ?? "(no reason)"}{" "}
        — the requested [{update.requested.join(", ")}] was NOT applied; the draft is
        preserved (your decision, never an auto-retry)
      </div>
    );
  }
  if (update.kind === "TRANSPORT") {
    return (
      <div className="banner banner-error" role="alert">
        update ({update.action}) TRANSPORT · {update.failure} — if the request was sent, the
        outcome is UNKNOWN (no blind retry); re-read to reconcile, the draft is preserved
      </div>
    );
  }
  return (
    <div className="banner banner-error" role="alert">
      update ({update.action}) CONTRACT MISMATCH · {update.error} — reported, never coerced
    </div>
  );
}

// ------------------------------------------------------------- formatting

/** A JSON scalar's honest display form (never a silent blank). */
function valueText(value: unknown): string {
  if (value === null) return "(none)";
  if (value === undefined) return "(absent)";
  if (typeof value === "string") return value === "" ? "(empty)" : value;
  return String(value);
}

function numericText(value: unknown): string {
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  if (typeof value === "string") return value;
  return "";
}

/** The numeric parse — the control's own metadata (int/float, the
 * limits) is the law; an entry that is not a legal explicit value
 * yet stays INVALID (never clamped, never coerced — the store's own
 * loud validation is the authority, this is the honest client gate). */
function parseNumeric(
  raw: string,
  control: InferenceControlDocument,
): { readonly valid: true; readonly value: number } | { readonly valid: false } {
  if (raw.trim() === "") return { valid: false };
  const parsed = Number(raw);
  if (!Number.isFinite(parsed)) return { valid: false };
  if (control.value_type === "int" && !Number.isInteger(parsed)) return { valid: false };
  if (control.minimum !== null && parsed < control.minimum) return { valid: false };
  if (control.maximum !== null && parsed > control.maximum) return { valid: false };
  return { valid: true, value: parsed };
}
