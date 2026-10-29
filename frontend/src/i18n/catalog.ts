/**
 * The DEFAULT-LOCALE catalog (i18n-1 band-1, FRONTEND_UIUX_LAW §17 —
 * the ONE translation boundary): every user-facing literal of the
 * migrated surfaces lives HERE as data, never inline in a component.
 * A second language adds an overlay catalog through `addCatalog`
 * (i18n.ts) — this map is the fallback base every locale resolves
 * against, so it stays the single source of the English strings.
 *
 * Key grammar: `<surface>.<place>[.<qualifier>` — the surface named
 * first (app/shell/settings/…), so a future band extends the map by
 * its own prefix and a reviewer can locate a string's owner from the
 * key alone. The map is `as const` — `MessageKey` is the literal union,
 * and a typo in a `tr()` call is a compile error, never a blank at
 * runtime.
 *
 * Verbatim contract tokens (op names, store field names, server
 * answers) are NOT catalogued: they name the backend's own closed
 * vocabulary and would be mistranslated, not localized. Prose around
 * them carries them as `{param}` placeholders.
 */
export const EN = {
  // — the composition root (app/composition/App.tsx) —
  "app.title": "CanonSim Workbench",
  "app.strip.session": "session",
  "app.strip.creating": "creating…",
  "app.strip.rev": "rev",
  "app.strip.seq": "seq",
  "app.strip.refresh": "refresh",
  "app.banner.createFailed":
    "session.create failed: {error} — the gateway may be down (start it: python scripts/workbench_app.py)",

  // the product routes' rail rows (labels + one-line hints)
  "app.route.chat.label": "Chat",
  "app.route.chat.hint": "Converse with the loaded model — every turn an honest run",
  "app.route.inference.label": "Inference",
  "app.route.inference.hint":
    "The generation-control workspace — chips, the sampler chain, the effective state",
  "app.route.models.label": "Models",
  "app.route.models.hint":
    "The model family — discovery, arrival (fetch/import), and the load ladder",
  "app.route.trajectory.label": "Trajectory",
  "app.route.trajectory.hint":
    "Live events of the current session — the volatile tail, never durable history",
  "app.route.observatory.label": "Observatory",
  "app.route.observatory.hint": "Committed run history — bounded windows over the archived logs",
  "app.route.settings.label": "Settings",
  "app.route.settings.hint": "Launch configuration — persisted, effective at the next spawn",

  // the diagnostic surfaces behind the Diagnostics entry
  "app.diag.session.label": "Session lifecycle",
  "app.diag.session.hint":
    "the lease lifecycle — attach under the CAS guard, detach under the lease guard, the honest closure",
  "app.diag.gateway.label": "Gateway",
  "app.diag.gateway.hint": "the app.status round-trip + the honest rejection probes",
  "app.diag.probe.label": "Load probe",
  "app.diag.probe.hint":
    "drives real session.attach ops (the CAS loop) — the S0-4 measurement instrument",

  // the S0-4 load probe surface
  "app.probe.region": "Load probe",
  "app.probe.title": "Load probe (S0-4)",
  "app.probe.noteA": "drives real ",
  "app.probe.noteB":
    " ops (CAS loop) — the Python-side load stand-in; with a model loaded, the LLM-side cost rides the chat runs (iter-302: 50 ops measured at ~108 ops/s alongside a live llama-server — the note, not a perf lab)",
  "app.probe.drive50": "drive 50 ops",
  "app.probe.drive300": "drive 300 ops (rolls the 256-event retention)",
  "app.probe.driving": "driving…",
  "app.probe.dt.ops": "ops",
  "app.probe.dt.wall": "wall",
  "app.probe.dt.observed": "observed",
  "app.probe.dt.at": "at",
  "app.probe.wallValue": "{seconds} s",
  "app.probe.observedValue": "{ops} ops/s (attach+get pairs)",
  "app.probe.notRun": "not run yet",

  // — the shell (features/shell/Shell.tsx) —
  "shell.region": "Workbench",
  "shell.nav": "Primary navigation",
  "shell.diagnostics": "Diagnostics",
  "shell.diagnosticsHint": "Engineering surfaces — gateway, session lifecycle, load probe",
  "shell.diagnosticsArea": "Diagnostics",
  "shell.diagNav": "Diagnostic surfaces",
  "shell.empty": "no product surfaces registered",

  // — the Settings surface (features/settings/Settings.tsx) —
  "settings.region": "Settings — launch configuration",
  "settings.title": "Settings",
  "settings.tag": "CONFIG · USER",
  "settings.note":
    "the managed spawn’s DEPLOYMENT knobs + the gateway identity — persisted by the store, effective at the NEXT spawn; the semantic generation controls live in the Inference surface (Settings ≠ Inference Control)",
  "settings.sectionsNav": "Settings sections",
  "settings.tab.deployment": "Deployment",
  "settings.tab.about": "About",
  "settings.tab.appearance": "Appearance",

  // the Deployment section
  "settings.deployment.region": "Settings — Deployment",
  "settings.deployment.title": "Deployment",
  "settings.deployment.tag": "LAUNCH · NEXT-SPAWN",
  "settings.deployment.note":
    "the managed llama-server spawn’s knobs — the executable preference, the web-UI surface, the raw extra_args hatch; the raw hatch belongs HERE (disclosure layers are not semantic classes — one document, one draft, one Save)",
  "settings.context.applies": "applies",
  "settings.context.managed": "managed",
  "settings.context.live": "LIVE",
  "settings.context.down": "down",
  "settings.context.draft": "DRAFT — unsaved changes",
  "settings.context.clean": "draft matches the observed document",
  "settings.context.noSession": "no session — save disabled",
  "settings.field.llamaServer.hint": "(the executable preference; empty = auto-discovery)",
  "settings.field.noWebui.hint": "(llama-server’s own web-UI surface on the spawned process)",
  "settings.field.extraArgs.hint":
    "(the RAW compatibility/debug escape hatch — duplicate flag ownership rejects loudly at the compile step)",
  "settings.controls.reread": "re-read settings",
  "settings.controls.reset": "reset draft",
  "settings.controls.save": "save changes",
  "settings.controls.note":
    "save sends ONLY the changed fields (absent fields unchanged) with a fresh idempotency key — one explicit attempt, never a blind retry",
  "settings.preview.title": "the next spawn’s compiled command (the composition root’s view)",
  "settings.preview.none": "(no preview — the composition did not inject one)",
  "settings.empty": "the settings document not read yet…",

  // the read's honest lanes
  "settings.read.transport":
    "settings read TRANSPORT · {failure} — the gateway may be down; the re-read is your explicit retry",
  "settings.read.mismatch": "settings read CONTRACT MISMATCH · {error} — reported, never coerced",
  "settings.read.rejected": "settings read REJECTED · {rejection}: {reason}",
  "settings.noReason": "(no reason)",

  // the save's honest lanes
  "settings.save.saving": "saving {fields}…",
  "settings.save.saved":
    "SAVED — requested [{fields}] accepted; EFFECTIVE at the NEXT managed spawn (applies: {applies})",
  "settings.save.savedLive": " — the LIVE server keeps its flags until unloaded",
  "settings.save.rejected":
    "save REJECTED · {rejection}: {reason} — the requested [{fields}] was NOT applied; the draft is preserved (your decision, never an auto-retry)",
  "settings.save.transport":
    "save TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry); re-read to reconcile, the draft is preserved",
  "settings.save.mismatch": "save CONTRACT MISMATCH · {error} — reported, never coerced",

  // — the About section (features/settings/SettingsAbout.tsx) —
  "settings.about.region": "Settings — About",
  "settings.about.title": "About",
  "settings.about.tag": "IDENTITY · READ-ONLY",
  "settings.about.noteA": "the gateway’s own identity document (",
  "settings.about.noteB":
    ") — the service, the contract it speaks, the exposure, and the full registered operation registry; nothing here is editable. The rejection-probe console lives in Diagnostics (identity here, proof there)",
  "settings.about.dt.service": "service",
  "settings.about.dt.contract": "contract",
  "settings.about.dt.exposure": "exposure",
  "settings.about.dt.auth": "auth",
  "settings.about.dt.operations": "operations",
  "settings.about.reread": "re-read identity",
  "settings.about.note":
    "one read per visit — the registry is construction-stable, it does not change under the reader",
  "settings.about.reading": "reading the gateway identity…",
  "settings.about.transport":
    "identity read TRANSPORT · {failure} — the gateway may be down; the re-read is your explicit retry",
  "settings.about.mismatch": "identity read CONTRACT MISMATCH · {error} — reported, never coerced",
  "settings.about.notOk":
    "the gateway answered, but not OK ({status}) — the honest fallback lane, never a friendly collapse",
  "settings.about.authRequired": "required",
  "settings.about.authNotRequired": "not required (loopback)",
  "settings.about.registered": "{count} registered",

  // — the Appearance section (features/settings/Settings.tsx) —
  // the ONE real appearance preference that exists: the interface
  // language. It is session-scoped by construction (the module-level
  // language in `i18n.ts` — no browser storage, the guard's R3 law),
  // so the section's note says so instead of implying persistence.
  "settings.appearance.region": "Settings — Appearance",
  "settings.appearance.title": "Appearance",
  "settings.appearance.tag": "SESSION · IN-MEMORY",
  "settings.appearance.note":
    "the interface language for THIS session — the choice lives in the translation boundary’s memory and returns to English on reload (browser storage is never truth, R3); the visual tokens are the design’s own law (VISUAL_SYSTEM_UI), not a preference",
  "settings.appearance.lang.label": "interface language",
  "settings.appearance.lang.hint":
    "(re-renders every mounted surface immediately; a partial catalog falls back to English per key, never blank)",
  "settings.appearance.lang.en": "English",
  "settings.appearance.lang.ru": "Русский",

  // — the Chat surface (features/chat/Chat.tsx) —
  "chat.region": "Chat — the conversation world",
  "chat.title": "Chat",
  "chat.note":
    "one conversation with the backend model — every turn an honest run: admitted, observed, terminal; the effective temperature the next send resolves from is shown in the strip",
  "chat.context.model": "model",
  "chat.context.noneActive": "none ACTIVE",
  "chat.context.discovered": "discovered",
  "chat.context.profile": "profile",
  "chat.context.temp": "temp",
  "chat.context.tempValue": "{value} ({state} · {source})",
  "chat.context.managed": "managed",
  "chat.context.live": "LIVE",
  "chat.context.down": "down",
  "chat.context.applies": "applies",
  "chat.context.compactNote":
    "the compact projection only — the full control depth lives in the Inference surface (a later row), never hidden here",
  "chat.context.laneRetry": "{failure} — the re-read is your explicit retry",
  "chat.context.laneMismatch": "{error} — reported, never coerced",
  "chat.context.laneRejected": "{rejection}: {reason}",
  "chat.context.laneJoin": "{title} {load} · {detail}",
  "chat.viewportLabel": "the conversation",
  "chat.empty":
    "no messages yet — the transcript lives with this surface (volatile by law: unmount drops it, the gateway documents are the truth)",
  "chat.runInFlight":
    "a run is in flight — the send stays disabled until it is terminal (one run at a time)",
  "chat.callLocalInvalid":
    "the call-local overrides are not a legal explicit value yet (temperature: a number in [0, 2]; max_tokens: an integer in [1, 4096]) — the send stays disabled",
  "chat.composer.message": "message",
  "chat.composer.messageHint": "(Enter sends · Shift+Enter breaks a line)",
  "chat.composer.noSessionPlaceholder": "no session — the run ops are session-scoped",
  "chat.composer.ellipsis": "…",
  "chat.composer.temperature": "temperature",
  "chat.composer.temperatureHint": "(empty = the profile’s BASE resolution)",
  "chat.composer.maxTokens": "max_tokens",
  "chat.composer.maxTokensHint": "(empty = the row’s own default)",
  "chat.composer.send": "send",
  "chat.composer.stop": "stop",
  "chat.composer.sendNote":
    "one explicit dispatch per send (a fresh idempotency key) — never a blind retry; the message list rides the wire as the conversation context",
  "chat.noSession": "no session — the send is disabled (chat.send is session-scoped)",

  // the transcript turn (replay echo, lanes, provenance)
  "chat.turn.replayOfLabel": "replay of",
  "chat.turn.replayEchoTail": " — the same frozen request re-run as a NEW execution",
  "chat.turn.roleYou": "you",
  "chat.turn.roleReplay": "you (replay echo)",
  "chat.turn.roleAssistant": "assistant",
  "chat.actions.replayTitle":
    "replay — re-run this execution's FROZEN material as a NEW execution (lineage via replay_of, never identity reuse); one explicit admission with a fresh idempotency key",
  "chat.actions.replay": "replay",
  "chat.actions.lineageTitle":
    "inspect lineage — the §10 provenance read: replay_of, the direct replays, the frozen inputs, the closed artifact",
  "chat.actions.inspectLineage": "inspect lineage",
  "chat.actions.hideLineage": "hide lineage",
  "chat.actions.note":
    "a replay is a NEW execution over the frozen material — observed below; the original stays untouched",
  "chat.replay.dispatching": "admitting the replay…",
  "chat.replay.admittedA": "replay admitted — new execution",
  "chat.replay.admittedB": "(a NEW identity; the lineage link is replay_of)",
  "chat.replay.rejected":
    "replay REJECTED · {rejection}: {reason} — nothing ran; a new attempt is your explicit new command (never an auto-retry)",
  "chat.replay.transport":
    "replay TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry)",
  "chat.replay.mismatch": "replay CONTRACT MISMATCH · {error} — reported, never coerced",

  // the lineage inspector (execution.get)
  "chat.lineage.region": "execution provenance for {id}",
  "chat.lineage.titleA": "lineage ·",
  "chat.lineage.refresh": "refresh lineage",
  "chat.lineage.refreshNote":
    "execution.get — the provenance read; the lifecycle read (run.get) stays separate",
  "chat.lineage.reading": "reading the provenance…",
  "chat.lineage.transport":
    "execution.get TRANSPORT · {failure} — the re-read is your explicit retry",
  "chat.lineage.mismatch":
    "execution.get CONTRACT MISMATCH · {error} — reported, never coerced",
  "chat.lineage.rejected": "execution.get REJECTED · {rejection}: {reason}",
  "chat.lineage.work": "work",
  "chat.lineage.workTerminal": "· terminal",
  "chat.lineage.workInFlight": "· in flight",
  "chat.lineage.state": "state",
  "chat.lineage.operation": "operation",
  "chat.lineage.lineage": "lineage",
  "chat.lineage.replayOf": "replay of",
  "chat.lineage.original": "— (original)",
  "chat.lineage.replays": "· replays",
  "chat.lineage.children": "· children",
  "chat.lineage.artifactSchemaJoin": "·",
  "chat.lineage.requestDigest": "request digest",
  "chat.lineage.artifact": "artifact",
  "chat.lineage.notClosed": "not closed yet (an in-flight original)",
  "chat.lineage.noStatus": "(no status)",
  "chat.lineage.frozenTitle": "frozen inputs (the §10 freeze — the replay re-runs these, never re-validates)",
  "chat.lineage.noPairs": "the freeze carries no pairs",
  "chat.lineage.key": "key",
  "chat.lineage.frozenValue": "frozen value",

  // the run's closure lanes
  "chat.lane.dispatching": "admitting the run…",
  "chat.lane.inFlightRun": "run {id} · {state}",
  "chat.lane.inFlightEllipsis": "…",
  "chat.lane.staleMarker": " · STALE (the observation itself failed)",
  "chat.lane.cancelOutcomeLabel": "stop requested — observed outcome:",
  "chat.lane.cancelTail":
    "(a request’s answer, never a completion; the run’s terminal state is the truth)",
  "chat.lane.cancelTransport": "TRANSPORT ({kind}) — the request’s outcome is UNKNOWN",
  "chat.lane.cancelMismatch": "CONTRACT MISMATCH: {error}",
  "chat.lane.cancelRejected": "{rejection}: {reason}",
  "chat.lane.repollNote":
    "run.get TRANSPORT · {failure} — the outcome is UNKNOWN; the re-poll is your explicit action (no blind retry)",
  "chat.lane.repoll": "re-poll",
  "chat.lane.runShort": "run {id}",
  "chat.lane.finish": "· finish {reason} ·",
  "chat.lane.tempRequested": "· temp requested",
  "chat.lane.tempAbsent": "(absent — the profile's BASE)",
  "chat.lane.effective": "→ effective {value} ·",
  "chat.lane.maxTokensTail": "max_tokens {value}",
  "chat.lane.replayOfShort": "· replay of",
  "chat.lane.completedMismatch":
    "the run COMPLETED but its result deviates from the chat contract · {error} — reported, never coerced",
  "chat.lane.failed": "run FAILED · {failureType} — {diagnostics}",
  "chat.lane.noFailureType": "(no failure type)",
  "chat.lane.noDiagnostics": "(no diagnostics)",
  "chat.lane.noReason": "(no reason)",
  "chat.lane.terminal": "run terminal · {state}",
  "chat.lane.sendRejected":
    "chat.send REJECTED · {rejection}: {reason} — the message was never sent; a new send is your explicit new command (never an auto-retry)",
  "chat.lane.sendTransport":
    "chat.send TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry); this turn stays out of the next send’s context",
  "chat.lane.pollRejected":
    "run.get REJECTED · {rejection}: {reason} — the observation itself was rejected; the run’s truth is unreachable from here",
  "chat.lane.pollMismatch": "run.get CONTRACT MISMATCH · {error} — reported, never coerced",

  // — the Models surface (features/models/Models.tsx) —
  "models.region": "Models — the model family",
  "models.title": "Models",
  "models.note":
    "the model family — discovery, arrival, and the load ladder; a file on disk proves nothing: discovered ≠ selected ≠ loading ≠ active, and the ladder state is the backend’s own answer, never a guess",
  "models.context.folder": "folder",
  "models.context.directory": "directory",
  "models.context.discovered": "discovered",
  "models.context.active": "active",
  "models.context.none": "none",
  "models.context.refresh": "refresh",
  "models.context.laneRetry": "{failure} — the re-read is your explicit retry",
  "models.context.laneMismatch": "{error} — reported, never coerced",
  "models.context.laneRejected": "{rejection}: {reason}",
  "models.context.noReason": "(no reason)",
  "models.context.laneJoin": "{title} {load} · {detail}",
  "models.arrival.fetchTitle": "fetch from anywhere",
  "models.arrival.urlLabel": "URL",
  "models.arrival.urlHint":
    "(a direct http(s) link, a huggingface.co page, or the hf:repo/file shorthand)",
  "models.arrival.urlPlaceholder": "https://huggingface.co/<org>/<repo>/resolve/main/<model>.gguf",
  "models.arrival.saveAs": "save as",
  "models.arrival.saveAsHint": "(empty = the URL’s own file name)",
  "models.arrival.saveAsPlaceholder": "model.gguf",
  "models.arrival.fetch": "fetch",
  "models.arrival.fetchNote":
    "a run with live progress — the file lands for the NEXT discovery scan (a name already discovered or a leftover .part rejects at admission, never mid-flight)",
  "models.arrival.importTitle": "import local files",
  "models.arrival.pathsLabel": "absolute paths",
  "models.arrival.pathsHint":
    "(one per line — the web form’s honest input; the native picker is the desktop row’s own concern)",
  "models.arrival.import": "import",
  "models.arrival.importNote":
    "a local copy on the gateway’s host (loopback — the same machine), no network; every admission gate (absolute, existing, plain name, unoccupied) rejects verbatim",
  "models.noSession":
    "no session — every dispatch is disabled (model.load/model.unload/run.start are session-scoped); the two reads above stay available",
  "models.list.notLanded": "the discovery scan has not landed yet",
  "models.list.missing":
    "the models folder does not exist yet — fetch or import lands it (the composition creates it at startup; the scan says so honestly, never an error)",
  "models.list.empty": "no model files discovered — fetch one from anywhere or import local files below",
  "models.row.identityComputed": "identity computed",
  "models.row.computeIdentity": "compute identity",
  "models.row.noIdentity": "strong identity not computed",
  "models.row.load": "load",
  "models.row.unload": "unload",
  "models.row.loadTitleFailed": "the ladder's FAILED is terminal (no re-selection path)",
  "models.row.loadTitle": "load — the admission walks the ladder to SELECTED; the load itself is a run",
  "models.row.unloadTitle": "unload — the graceful stop is a run; ACTIVE → EVICTED observed on its terminal",
  "models.row.digestTitle":
    "compute the §9 strong identity as a run — the honest long arm for a multi-GB file (cancellable, observable)",
  "models.run.idle":
    "no run yet — every load, unload, fetch, import, and identity computation is an honest run: admitted, observed, terminal",
  "models.run.admitting": "admitting the run ({work})…",
  "models.run.inFlight": "run {id} · {work} · {state}",
  "models.run.staleMarker": " · STALE (the observation itself failed)",
  "models.run.inFlightEllipsis": "…",
  "models.run.cancelOutcomeLabel": "stop requested — observed outcome:",
  "models.run.cancelTail":
    "(a request’s answer, never a completion; the run’s terminal state is the truth)",
  "models.run.cancelTransport": "TRANSPORT ({kind}) — the request’s outcome is UNKNOWN",
  "models.run.cancelMismatch": "CONTRACT MISMATCH: {error}",
  "models.run.cancelRejected": "{rejection}: {reason}",
  "models.run.noReason": "(no reason)",
  "models.run.repollNote":
    "run.get TRANSPORT · {failure} — the outcome is UNKNOWN; the re-poll is your explicit action (no blind retry)",
  "models.run.repoll": "re-poll",
  "models.run.stop": "stop",
  "models.run.completedMismatch":
    "the run COMPLETED but its result deviates from the {work} contract — reported, never coerced",
  "models.run.failed": "run FAILED ({work}) · {failureType} — {diagnostics}",
  "models.run.noFailureType": "(no failure type)",
  "models.run.noDiagnostics": "(no diagnostics)",
  "models.run.terminal": "run terminal · {work} · {state}",
  "models.run.dispatchRejected":
    "dispatch REJECTED · {rejection}: {reason} — nothing was sent; a new dispatch is your explicit new command (never an auto-retry)",
  "models.run.dispatchTransport":
    "dispatch TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry)",
  "models.run.dispatchMismatch": "dispatch CONTRACT MISMATCH · {error} — reported, never coerced",
  "models.run.pollRejected":
    "run.get REJECTED · {rejection}: {reason} — the observation itself was rejected; the run’s truth is unreachable from here",
  "models.run.pollMismatch": "run.get CONTRACT MISMATCH · {error} — reported, never coerced",
  "models.run.replayTitle":
    "replay — re-run this execution's FROZEN material as a NEW execution (lineage via replay_of, never identity reuse); one explicit admission with a fresh idempotency key",
  "models.run.replay": "replay",
  "models.run.replayNote": "a replay is a NEW execution over the frozen material — the original stays untouched",
  "models.run.notReplayableNote":
    "{work} owns its re-dispatch — a live-gate kind is not replayable (the backend’s own gate; re-select or re-load explicitly)",
  "models.run.replayLineageA": "replay lineage —",
  "models.run.replayLineageJoin": "→",
  "models.run.replayLineageB": "(a NEW execution over the original’s frozen material)",
  "models.replay.dispatching": "admitting the replay…",
  "models.replay.admittedA": "replay admitted — new execution",
  "models.replay.admittedB": "(a NEW identity; the lineage link is replay_of)",
  "models.replay.rejected":
    "replay REJECTED · {rejection}: {reason} — nothing ran; a new attempt is your explicit new command (never an auto-retry)",
  "models.replay.transport":
    "replay TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry)",
  "models.replay.mismatch": "replay CONTRACT MISMATCH · {error} — reported, never coerced",
  "models.progress.fetchTotalUnknown": "{name}: {downloaded} (total unknown — never a guess)",
  "models.progress.fetch": "{name}: {downloaded} of {total}",
  "models.progress.importRow":
    "file {index}/{count} ({name}): {copied} of {total}",
  "models.progress.unrecognized":
    "progress reported in a shape this surface does not recognize — shown as itself, never coerced",
  "models.outcome.loadSplitA": "load COMPLETED —",
  "models.outcome.loadSplitB": "is ACTIVE (the ladder’s own landing: SELECTED → LOADING → LOADED → ACTIVE)",
  "models.outcome.unloadSplitA": "unload COMPLETED —",
  "models.outcome.unloadSplitB": "is EVICTED (the graceful stop’s observed fold)",
  "models.outcome.fetchA": "fetch COMPLETED —",
  "models.outcome.fetchB": "landed ({size})",
  "models.outcome.fetchC": "from {url}; the NEXT discovery scan sees it",
  "models.outcome.importA": "import COMPLETED — {count} file(s) landed:",
  "models.outcome.identityA": "identity COMPLETED —",
  "models.outcome.identityJoin": ":",
  "models.outcome.identityB": "sha256 {digest} ({chunks} chunks, {size})",
  "models.row.activeMarker": "ACTIVE",

  // — the Inference surface (features/inference/Inference.tsx) —
  "inference.region": "Inference — the generation-control workspace",
  "inference.title": "Inference",
  "inference.tag": "CONTROL · SEMANTIC",
  "inference.note":
    "the semantic generation-control workspace — the chip library, the sampler chain, the effective-state presentation; the profile persists, effective at the NEXT spawn; the compiled command is a technical artifact, never the authoring language",
  "inference.context.profile": "profile",
  "inference.context.applies": "applies",
  "inference.context.managed": "managed",
  "inference.context.live": "LIVE",
  "inference.context.down": "down",
  "inference.context.chain": "chain",
  "inference.context.chainValue": "{count} members",
  "inference.context.deterministic": "deterministic",
  "inference.context.detYes": "yes (temp 0)",
  "inference.context.detNo": "no",
  "inference.context.draft": "DRAFT — unsaved changes",
  "inference.context.clean": "draft matches the observed document",
  "inference.context.noSession": "no session — updates disabled",
  "inference.preset.label": "preset — a transparent starting point",
  "inference.preset.none": "(no preset selected — inspect one, apply explicitly)",
  "inference.preset.apply": "apply preset",
  "inference.preset.applyNote":
    "a PLAIN update — the values land editable, never an opaque mode; the apply needs a CLEAN draft (a preset never silently modifies out-of-scope settings)",
  "inference.preset.noChanges":
    "every preset field already matches the observed profile — the apply would change nothing",
  "inference.search.label": "search controls (name, flag, category)",
  "inference.search.placeholder":
    "search — name, flag, or category; a match shows the advanced rows too",
  "inference.advanced": "advanced controls",
  "inference.category.rungNote":
    "all {count} of this family’s controls sit on the advanced rung — ask for them (the checkbox above) or search for one by name/flag",
  "inference.noMatch":
    "NO MATCH — no control’s name, flag, or category contains “{query}” (the library is the server’s own document, never a client list)",
  "inference.controls.reread": "re-read profile",
  "inference.controls.reset": "reset draft",
  "inference.controls.save": "save changes",
  "inference.controls.saveNote":
    "save sends ONLY the changed keys (absent fields unchanged) with a fresh idempotency key — one explicit attempt, never a blind retry; a pin/unpin is its own dispatch",
  "inference.invalid.one": "one editor holds a value that is not a legal explicit value yet",
  "inference.invalid.many": "{count} editors hold values that are not legal explicit values yet",
  "inference.invalidTail":
    "— the save stays disabled (the store validates loudly anyway; this is the honest client-side gate)",
  "inference.preview.toggleShow": "show the next spawn’s compiled command",
  "inference.preview.toggleHide": "hide the next spawn’s compiled command",
  "inference.preview.title": "the next spawn’s compiled command (the composition root’s view)",
  "inference.preview.none": "(no preview — the composition did not inject one)",
  "inference.empty":
    "the control document not read yet — the workspace builds ON the read (an offline surface stays honestly empty, never composed-before-read)",
  "inference.pinned.empty":
    "nothing pinned — pin a control’s chip for a quick-access reveal (an explicit personal pin, the workspace’s own section, never a profile value)",
  "inference.pinned.revealTitle": "reveal {name} ({flag}) in its category",
  "inference.pinned.orphanTitle":
    "a pinned id with no control in the current library (the server's own document)",
  "inference.pinned.unpin": "unpin {name}",
  "inference.chain.region": "the sampler chain",
  "inference.chain.title": "the sampler chain",
  "inference.chain.tag": "{count} members · the emitted --samplers order",
  "inference.chain.draft": "DRAFT — membership changes with the save",
  "inference.chain.note":
    "membership and value are separate concerns — disabling a member removes it from the emitted chain while its value family stays configured (INEFFECTIVE with its reason); the order is the runtime’s own reviewed order (reordering is a later row)",
  "inference.row.pin": "pin {name}",
  "inference.row.unpin": "unpin {name}",
  "inference.row.unpinTitle": "unpin — remove from the quick-access strip",
  "inference.row.pinTitle":
    "pin — add to the quick-access strip (the workspace's own section)",
  "inference.row.advanced": "advanced",
  "inference.row.scopeTitle": "the scope model — this control also rides the request layer",
  "inference.row.draft": "DRAFT",
  "inference.row.docJoin": "·",
  "inference.row.docBaseline": "baseline",
  "inference.row.docUpstream": "upstream",
  "inference.row.docSource": "source {source}",
  "inference.pinned.unpinMark": "×",
  "inference.category.count": "{visible}/{controls}",
  "inference.gpuLayers.placeholder": "layers",
  "inference.load.transport":
    "inference.read TRANSPORT · {failure} — the gateway may be down; the re-read is your explicit retry",
  "inference.load.mismatch": "inference.read CONTRACT MISMATCH · {error} — reported, never coerced",
  "inference.load.rejected": "inference.read REJECTED · {rejection}: {reason}",
  "inference.update.updating": "updating ({action}) {requested}…",
  "inference.update.updated":
    "UPDATED ({action}) — requested [{requested}] accepted; EFFECTIVE at the NEXT managed spawn (applies: {applies})",
  "inference.update.updatedLive": " — the LIVE server keeps its spawn flags until unloaded",
  "inference.update.rejected":
    "update ({action}) REJECTED · {rejection}: {reason} — the requested [{requested}] was NOT applied; the draft is preserved (your decision, never an auto-retry)",
  "inference.update.transport":
    "update ({action}) TRANSPORT · {failure} — if the request was sent, the outcome is UNKNOWN (no blind retry); re-read to reconcile, the draft is preserved",
  "inference.update.mismatch":
    "update ({action}) CONTRACT MISMATCH · {error} — reported, never coerced",

  // — the Observatory surface (features/observatory/Observatory.tsx) —
  "observatory.region": "Observatory — committed history",
  "observatory.title": "Observatory",
  "observatory.tag": "HISTORY · COMMITTED LOGS",
  "observatory.note":
    "durable, queryable, bounded windows over the canonical logs — never the live session tail (the Trajectory pane owns that world); no polling: every read is explicit",
  "observatory.controls.rescan": "rescan runs",
  "observatory.controls.openStem": "open stem",
  "observatory.controls.openStemPlaceholder": "open run by stem… (e.g. run_125_0)",
  "observatory.noRun": "no run open — scan the runs root or open a run by its stem",
  "observatory.scan.notScanned": "not scanned yet — the runs discovery is your explicit read",
  "observatory.scan.scanning": "scanning the runs root…",
  "observatory.scan.transport":
    "runs scan TRANSPORT · {failure} — the gateway may be down; the scan is your explicit retry",
  "observatory.scan.mismatch": "runs scan CONTRACT MISMATCH · {error} — reported, never coerced",
  "observatory.scan.blockLabel": "discovered runs",
  "observatory.scan.found": "runs {root} — {count} found",
  "observatory.scan.noDataA": "NO DATA — the runs root holds no committed runs (generate one: the CLI writes",
  "observatory.scan.noDataB": "logs/*.jsonl)",
  "observatory.scan.join": "·",
  "observatory.scan.open": "open",
  "observatory.scan.seed": "seed",
  "observatory.scan.schema": "schema",
  "observatory.scan.headerUnreadable":
    "header unreadable — {error} (the listing degrades honestly; the run stays openable, its read will name the cause)",
  "observatory.scan.unknownError": "unknown error",
  "observatory.read.reading": "reading run {run}…",
  "observatory.read.transport":
    "read TRANSPORT · {failure} — delivery failed, never a gateway rejection; the re-read is your explicit decision",
  "observatory.read.mismatch": "read CONTRACT MISMATCH · {error} — reported, never coerced",
  "observatory.read.rejectedA": "REJECTED · {rejection} — {reason}",
  "observatory.read.reread": "re-read from the head",
  "observatory.context.run": "run",
  "observatory.context.seed": "seed",
  "observatory.context.profile": "profile",
  "observatory.context.authority": "authority",
  "observatory.context.events": "events",
  "observatory.context.eventsValue": "{window}/{total}",
  "observatory.context.window": "window",
  "observatory.context.fromHead": "from head",
  "observatory.context.after": "after {id}",
  "observatory.context.limit": "limit",
  "observatory.context.durable": "DURABLE",
  "observatory.window.next": "next window ({after})",
  "observatory.window.end": "next window — end of run",
  "observatory.window.reread": "re-read from the head",
  "observatory.window.note":
    "{window} events in this window · {total} committed total {tail}",
  "observatory.window.moreRemain": "· more remain",
  "observatory.window.runEnd": "· this is the run's end",
  "observatory.header.tick": "tick",
  "observatory.header.type": "type",
  "observatory.header.kind": "kind",
  "observatory.header.actor": "actor",
  "observatory.header.imp": "imp",
  "observatory.header.eventId": "event id",
  "observatory.windowLabel": "event window",
  "observatory.inspector.region": "selected history event",
  "observatory.inspector.empty":
    "no selection — click a row (selection is by event id, the semantic identity)",

  // — the Trajectory surface (features/trajectory/Trajectory.tsx) —
  "trajectory.region": "Trajectory — live session tail",
  "trajectory.title": "Trajectory",
  "trajectory.tag": "LIVE SESSION TAIL",
  "trajectory.note":
    "volatile, retention-limited, resync-on-gap — not durable history (the Observatory read-side owns the durable world)",
  "trajectory.strip.session": "session",
  "trajectory.strip.seq": "seq",
  "trajectory.strip.rows": "rows",
  "trajectory.strip.stream": "stream {phase}",
  "trajectory.strip.poll": "poll {state}",
  "trajectory.strip.pollOn": "on",
  "trajectory.strip.pollOff": "off",
  "trajectory.strip.read": "read",
  "trajectory.strip.never": "never",
  "trajectory.resync":
    "RESYNC_REQUIRED — the cursor fell out of the retained tail (FIFO eviction, not canon loss); re-read from the server's retained window (from seq {from}).",
  "trajectory.synthetic":
    "{count} synthetic load-test rows appended — presentation-only, not gateway truth.",
  "trajectory.syntheticClear": "clear",
  "trajectory.trimmed":
    "{count} older rows trimmed from the presentation window (the buffer is bounded; durable evidence lives on the server).",
  "trajectory.disconnectedTail": " — presentation is last-known, not fresh",
  "trajectory.feed.label": "feed",
  "trajectory.feed.transport": "feed transport",
  "trajectory.feed.stream": "stream (SSE)",
  "trajectory.feed.poll1": "poll 1s",
  "trajectory.feed.poll2": "poll 2s",
  "trajectory.feed.poll5": "poll 5s",
  "trajectory.feed.off": "off",
  "trajectory.refreshTitle": "the POST read — always valid (S0's mandate is the stream's own fallback)",
  "trajectory.refreshNow": "refresh now",
  "trajectory.top": "top",
  "trajectory.latest": "latest",
  "trajectory.jumpPlaceholder": "jump to seq…",
  "trajectory.go": "go",
  "trajectory.plus1k": "+1k synthetic",
  "trajectory.plus10k": "+10k synthetic",
  "trajectory.emptyDisconnected": "DISCONNECTED — no successful read yet",
  "trajectory.emptyNoData": "NO DATA — the session has no events yet (every op emits one)",
  "trajectory.inspector.region": "selected event",
  "trajectory.inspector.empty":
    "no selection — click a row (selection is by event id, the semantic identity)",
  "trajectory.row.synthetic": "SYNTHETIC",

  // — the Session lifecycle surface (features/session-lifecycle/SessionLifecycle.tsx) —
  "session.region": "Session lifecycle",
  "session.title": "Session",
  "session.note":
    "the lease lifecycle — attach under the CAS revision guard, detach under the lease guard; REQUESTED → ACCEPTED/REJECTED → EFFECTIVE → OBSERVED, never collapsed",
  "session.observed.title": "observed document — the root’s re-read, never the optimistic echo",
  "session.observed.empty": "no OBSERVED document yet — reading…",
  "session.observed.session": "session",
  "session.observed.attached": "attached",
  "session.observed.revision": "revision",
  "session.observed.eventSequence": "event_sequence",
  "session.observed.createdObservedAt": "created_observed_at",
  "session.observed.true": "true",
  "session.observed.false": "false",
  "session.attach": "attach session",
  "session.detach": "detach session",
  "session.refresh": "refresh session.get",
  "session.new": "new session",
  "session.requested": "REQUESTED…",
  "session.lease.title": "held lease — tab memory only, never storage; the detach op’s material",
  "session.lease.empty":
    "no lease held (attach to take one; lease_seconds = 30 on this gateway)",
  "session.lease.token": "token",
  "session.lease.seconds": "lease_seconds",
  "session.lease.note":
    "the gateway’s lease expires (lease_seconds); a detach past the expiry answers LEASE_EXPIRED — the verdict lane renders it verbatim, the retry is your explicit decision",
  "session.verdict.empty": "no mutation attempted yet — the lane renders the NEXT verdict verbatim",
  "session.verdict.accepted":
    "{operation} · {at} — ACCEPTED → EFFECTIVE: {effect}{revision}{lease}; OBSERVED rides the re-read above",
  "session.verdict.revision": " (revision {revision})",
  "session.verdict.lease": ", lease {seconds}s",
  "session.verdict.rejected":
    "{operation} · {at} — REJECTED · {rejection}{reason}; the outcome law: NOT_SENT — a retry is your explicit decision (a fresh request identity)",
  "session.verdict.reason": ": {reason}",
  "session.verdict.transport":
    "{operation} · {at} — TRANSPORT · {failure}; never “rejected” — if the request was sent, its outcome is UNKNOWN (no blind retry)",
  "session.verdict.mismatch": "{operation} · {at} — CONTRACT MISMATCH · {error}",

  // — the Gateway status surface (features/gateway-status/GatewayStatus.tsx) —
  "gateway.region": "Gateway status",
  "gateway.title": "Gateway",
  "gateway.note": "POST /op — the one route; every payload runtime-validated at the client boundary",
  "gateway.status.reading": "reading app.status…",
  "gateway.status.refresh": "refresh app.status",
  "gateway.status.service": "service",
  "gateway.status.contract": "contract",
  "gateway.status.exposure": "exposure",
  "gateway.status.auth": "auth",
  "gateway.status.authRequired": "required",
  "gateway.status.authNotRequired": "not required (loopback)",
  "gateway.status.operations": "operations",
  "gateway.status.transport": "TRANSPORT — {kind}: {detail}",
  "gateway.status.mismatch": "CONTRACT MISMATCH — {error}",
  "gateway.status.notOk": "the gateway answered, but not OK — see the probe lane",
  "gateway.probe.title": "rejection probes — the honest paths, against the real gateway",
  "gateway.probe.bogus": "DOMAIN_REJECTED probe",
  "gateway.probe.stale": "STALE_REVISION probe",
  "gateway.probe.duplicate": "DUPLICATE_REQUEST probe",
  "gateway.probe.empty": "no probes run yet",
  "gateway.probe.note":
    "the client auto-retries nothing (G4): UNKNOWN and transport ambiguity stay honest, a retry is always an explicit user action",
  "gateway.probe.label.bogus": "session.get · bogus session id",
  "gateway.probe.label.stale": "session.attach · stale expected revision",
  "gateway.probe.label.duplicate": "session.create · same key, different material",
  "gateway.probe.label.first": "first material",
  "gateway.probe.label.staleProbe": "stale-revision probe",
  "gateway.probe.label.different": "DIFFERENT material",
  "gateway.probe.delivered": "DELIVERED · {status}{rejection}",
  "gateway.probe.deliveredRejection": " · {rejection}",
  "gateway.probe.transport": "TRANSPORT · {failure}",
  "gateway.probe.mismatch": "MISMATCH · {error}",
} as const;

export type MessageKey = keyof typeof EN;
