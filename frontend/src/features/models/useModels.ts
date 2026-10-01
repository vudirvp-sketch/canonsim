/**
 * useModels — the Models surface's state (Phase 3's sixth row), over
 * the EXISTING gateway ops only: `model.list` + `model.states` (the
 * two session-free context READs — §20's ladder truth, never a
 * discovery guess), `model.load`/`model.unload` (the §20 loading
 * half as RUNS — the admission walks the ladder fast, the
 * minutes-class port call rides the worker thread), and the run
 * family's three model work kinds over `run.start` (model.fetch /
 * model.import / model.digest — identity-then-poll with live
 * progress) observed through `run.get`/`run.cancel`. No new route is
 * invented (§3).
 *
 * EFFECTIVE-STATE CLOSURE (FRONTEND_WEB_LAW §8, the stages stay
 * distinct — they may coincide, they are never assumed equivalent):
 *
 * ```text
 * REQUESTED  the row's load/unload click, the fetch form's URL, the
 *            import form's path list, the digest affordance (each a
 *            REQUEST, never a state claim)
 * ACCEPTED   the admission's execution identity (STARTING)
 * EFFECTIVE  the run's frozen inputs + the ladder's own walk
 *            (SELECTED at load admission — observed on model.states)
 * OBSERVED   the run's terminal document + the terminal-triggered
 *            ONE context re-read (the landed file rides the NEXT
 *            discovery scan; the ladder rests at its own truth)
 * PRESENTED  the discovery rows (the §20 ladder chips) + the run lane
 * ```
 *
 * §20's own law, carried verbatim: file exists ≠ valid ≠ selected ≠
 * loading ≠ loaded ≠ active — the discovery entry proves nothing
 * beyond its cheap fingerprint; the ladder state comes from
 * model.states; the ACTIVE slot is the load-state owner's answer.
 *
 * G4 (the no-retry law): every explicit dispatch carries a FRESH
 * `client_request_id`; the hook auto-retries NOTHING — a poll that
 * hit TRANSPORT marks the lane STALE and the loop STOPS; the re-poll
 * is the user's explicit action.
 *
 * Boundedness (§6 rule 3): ONE poller for the ONE in-flight run (the
 * dispatch guard blocks a second while one is active), a fixed
 * interval, dead at terminal, dead on unmount, dead on the first
 * TRANSPORT. The context reads fire once on mount; every later read
 * is the user's explicit refresh — plus exactly ONE re-read at the
 * run's terminal (the closure's OBSERVED baseline, never polling).
 */
import { useCallback, useEffect, useRef, useState } from "react";

import type { DispatchResult, GatewayClient } from "../../api/gateway/client.ts";
import type {
  ExecutionState,
  ModelDigestResult,
  ModelFetchProgress,
  ModelFetchResult,
  ModelImportProgress,
  ModelImportResult,
  ModelLoadResult,
  ModelListResult,
  ModelStatesResult,
  ModelUnloadResult,
} from "../../api/gateway/contracts.ts";
import {
  modelDigestResultSchema,
  modelFetchProgressSchema,
  modelFetchResultSchema,
  modelImportProgressSchema,
  modelImportResultSchema,
  modelLoadResultSchema,
  modelUnloadResultSchema,
} from "../../api/gateway/validators.ts";

/** The run observation's fixed cadence (ms) — a declared constant,
 * never a tunable storm. */
const MODELS_POLL_INTERVAL_MS = 700;

/** One context read's honest lane (the same shape every surface
 * renders distinctly — defined HERE, never imported across features
 * (the guard's R5 row); a partial failure is a partial header). */
export type ContextLoad<T> =
  | { readonly kind: "NOT_LOADED" }
  | { readonly kind: "LOADING" }
  | { readonly kind: "LOADED"; readonly result: T; readonly at: number }
  | { readonly kind: "REJECTED"; readonly rejection: string; readonly reason: string | null; readonly at: number }
  | { readonly kind: "TRANSPORT"; readonly failure: string; readonly at: number }
  | { readonly kind: "MISMATCH"; readonly error: string; readonly at: number };

/** The live progress, narrowed per work kind at the consumer (the
 * run document's `progress` is loose; the fetch/import shapes are
 * the work's own closed reports — anything else is honestly
 * UNRECOGNIZED, never coerced). */
export type ModelsRunProgress =
  | { readonly kind: "FETCH"; readonly progress: ModelFetchProgress }
  | { readonly kind: "IMPORT"; readonly progress: ModelImportProgress }
  | { readonly kind: "UNRECOGNIZED" };

/** The run's OBSERVED terminal result, narrowed per work kind (the
 * five the surface starts — a foreign kind's completion is a
 * MISMATCH, never a coerced bubble). */
export type ModelsRunOutcome =
  | { readonly work: "model.load"; readonly result: ModelLoadResult }
  | { readonly work: "model.unload"; readonly result: ModelUnloadResult }
  | { readonly work: "model.fetch"; readonly result: ModelFetchResult }
  | { readonly work: "model.import"; readonly result: ModelImportResult }
  | { readonly work: "model.digest"; readonly result: ModelDigestResult };

/** The ONE run's honest closure lane — every stage rendered as
 * itself, none collapsed (the Chat row's own state matrix, carried to
 * the model family's run shapes). */
export type ModelsRunLane =
  | { readonly kind: "DISPATCHING"; readonly work: string }
  | {
      readonly kind: "IN_FLIGHT";
      readonly work: string;
      readonly executionId: string;
      readonly runState: ExecutionState;
      readonly progress: ModelsRunProgress | null;
      readonly stale: boolean;
      readonly failure: string | null;
    }
  | { readonly kind: "COMPLETED"; readonly outcome: ModelsRunOutcome }
  | { readonly kind: "COMPLETED_MISMATCH"; readonly error: string }
  | {
      readonly kind: "FAILED";
      readonly work: string;
      readonly failureType: string | null;
      readonly diagnostics: readonly string[];
    }
  | {
      readonly kind: "OTHER_TERMINAL";
      readonly work: string;
      readonly runState: ExecutionState;
      readonly diagnostics: readonly string[];
    }
  | { readonly kind: "DISPATCH_REJECTED"; readonly rejection: string; readonly reason: string | null }
  | { readonly kind: "DISPATCH_TRANSPORT"; readonly failure: string }
  | { readonly kind: "DISPATCH_MISMATCH"; readonly error: string }
  | { readonly kind: "POLL_REJECTED"; readonly rejection: string; readonly reason: string | null }
  | { readonly kind: "POLL_MISMATCH"; readonly error: string };

/** The active (non-terminal) lane's own shape — the poll loop's and
 * the guards' shared truth. */
type ActiveRunLane =
  | { readonly kind: "DISPATCHING"; readonly work: string }
  | {
      readonly kind: "IN_FLIGHT";
      readonly work: string;
      readonly executionId: string;
      readonly runState: ExecutionState;
      readonly progress: ModelsRunProgress | null;
      readonly stale: boolean;
      readonly failure: string | null;
    };

/** The fetch form's draft (a REQUEST, never a state claim). */
export interface FetchDraft {
  readonly url: string;
  readonly name: string;
}

export interface ModelsState {
  /** the two context READs (discovery + the ladder). */
  readonly models: ContextLoad<ModelListResult>;
  readonly modelStates: ContextLoad<ModelStatesResult>;
  readonly refreshContext: () => Promise<void>;
  /** the ONE run's closure lane (null before the first dispatch). */
  readonly run: ModelsRunLane | null;
  readonly cancelOutcome: string | null;
  /** the forms' drafts. */
  readonly fetchDraft: FetchDraft;
  readonly importDraft: string;
  readonly editFetchDraft: (field: keyof FetchDraft, value: string) => void;
  readonly editImportDraft: (value: string) => void;
  /** the dispatches — each ONE explicit attempt, a fresh key (G4).
   * (The fetch action is `fetchModel`, never a bare fetch verb — the
   * guard's own vocabulary reserves that call form for the one
   * transport adapter.) */
  readonly load: (logicalName: string) => Promise<void>;
  readonly unload: (logicalName: string) => Promise<void>;
  readonly fetchModel: () => Promise<void>;
  readonly importPaths: () => Promise<void>;
  readonly digest: (logicalName: string) => Promise<void>;
  readonly cancel: () => Promise<void>;
  readonly repoll: () => void;
  /** a dispatch (any) is in flight. */
  readonly busy: boolean;
  /** a run is admitted and not terminal — the dispatch guard's truth. */
  readonly runInFlight: boolean;
}

export interface ModelsOptions {
  readonly client: GatewayClient;
  /** the run family's ops are session-scoped: null disables every
   * dispatch honestly (the two context READs stay available — they
   * are session-free). */
  readonly sessionId: string | null;
}

export function useModels(options: ModelsOptions): ModelsState {
  const { client, sessionId } = options;
  const [models, setModels] = useState<ContextLoad<ModelListResult>>({ kind: "NOT_LOADED" });
  const [modelStates, setModelStates] = useState<ContextLoad<ModelStatesResult>>({ kind: "NOT_LOADED" });
  const [run, setRun] = useState<ModelsRunLane | null>(null);
  const [cancelOutcome, setCancelOutcome] = useState<string | null>(null);
  const [fetchDraft, setFetchDraft] = useState<FetchDraft>({ url: "", name: "" });
  const [importDraft, setImportDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [pollEpoch, setPollEpoch] = useState(0);
  // The one-dispatch-at-a-time guards (refs — stable callback
  // identities, the mount reads fire exactly once, no busy-deps loop).
  const contextInFlight = useRef(false);
  const dispatchInFlight = useRef(false);
  const runRef = useRef<ModelsRunLane | null>(null);
  runRef.current = run;

  const active = activeRun(run);
  const runInFlight = active !== null;

  /** The two context READs — sequential, one at a time; every later
   * read is the user's explicit refresh (plus the run terminal's own
   * ONE closure re-read — see the poll loop). */
  const refreshContext = useCallback(async (): Promise<void> => {
    if (contextInFlight.current) return;
    contextInFlight.current = true;
    setBusy(true);
    setModels({ kind: "LOADING" });
    setModelStates({ kind: "LOADING" });
    try {
      await applyLane(await client.modelList(), setModels);
      await applyLane(await client.modelStates(), setModelStates);
    } finally {
      contextInFlight.current = false;
      setBusy(false);
    }
  }, [client]);

  // The mount reads — exactly one pass (the Settings/Chat precedent).
  useEffect(() => {
    void refreshContext();
  }, []);

  /** The shared dispatch body: guard → DISPATCHING lane → the
   * caller's dispatch → the four honest outcome lanes. ONE run at a
   * time (boundedness); a fresh idempotency key per attempt (G4 —
   * the caller mints it). Returns the lane it landed on (the
   * caller's own follow-up — e.g. consuming a form draft ONLY on
   * admission: a REJECTED/TRANSPORT attempt preserves the draft,
   * the user's explicit recovery is editing + re-dispatching). */
  const dispatchRun = useCallback(
    async (
      work: string,
      dispatch: () => Promise<DispatchResult<Admission>>,
    ): Promise<ModelsRunLane> => {
      if (dispatchInFlight.current || sessionId === null) {
        return { kind: "DISPATCH_MISMATCH", error: "the dispatch was guarded out" };
      }
      if (activeRun(runRef.current) !== null) {
        return { kind: "DISPATCH_MISMATCH", error: "the dispatch was guarded out" };
      }
      dispatchInFlight.current = true;
      setBusy(true);
      setCancelOutcome(null);
      setRun({ kind: "DISPATCHING", work });
      let lane: ModelsRunLane;
      try {
        const answer = await dispatch();
        if (answer.transport === "DELIVERED" && answer.status === "OK") {
          lane = {
            kind: "IN_FLIGHT",
            work,
            executionId: answer.result.executionId,
            runState: answer.result.runState,
            progress: null,
            stale: false,
            failure: null,
          };
        } else if (answer.transport === "TRANSPORT") {
          lane = {
            kind: "DISPATCH_TRANSPORT",
            failure: `${answer.failure.kind}: ${answer.failure.detail}`,
          };
        } else if (answer.transport === "MISMATCH") {
          lane = { kind: "DISPATCH_MISMATCH", error: answer.error };
        } else {
          lane = {
            kind: "DISPATCH_REJECTED",
            rejection: answer.response.rejection ?? "REJECTED",
            reason: reasonOf(answer.response.result),
          };
        }
      } finally {
        dispatchInFlight.current = false;
        setBusy(false);
      }
      setRun(lane);
      return lane;
    },
    [sessionId],
  );

  const load = useCallback(
    (logicalName: string): Promise<void> =>
      dispatchRun("model.load", async () => {
        const dispatch = await client.modelLoad({
          sessionId: sessionId as string,
          clientRequestId: `models-load-${crypto.randomUUID()}`,
          logicalName,
        });
        return projectAdmission(dispatch);
      }).then(() => undefined),
    [dispatchRun, client, sessionId],
  );

  const unload = useCallback(
    (logicalName: string): Promise<void> =>
      dispatchRun("model.unload", async () => {
        const dispatch = await client.modelUnload({
          sessionId: sessionId as string,
          clientRequestId: `models-unload-${crypto.randomUUID()}`,
          logicalName,
        });
        return projectAdmission(dispatch);
      }).then(() => undefined),
    [dispatchRun, client, sessionId],
  );

  const fetchModel = useCallback((): Promise<void> => {
    const url = fetchDraft.url.trim();
    if (url === "") return Promise.resolve();
    const name = fetchDraft.name.trim();
    return dispatchRun("model.fetch", async () => {
      const dispatch = await client.runStart({
        sessionId: sessionId as string,
        clientRequestId: `models-fetch-${crypto.randomUUID()}`,
        start:
          name === ""
            ? { work: "model.fetch", url }
            : { work: "model.fetch", url, logicalName: name },
      });
      return projectAdmission(dispatch);
    }).then((lane) => {
      // the REQUEST is consumed ONLY on admission (a REJECTED/
      // TRANSPORT attempt preserves the draft — the user's explicit
      // recovery is editing + re-dispatching, never a retyped URL).
      if (lane.kind === "IN_FLIGHT") {
        setFetchDraft({ url: "", name: "" });
      }
    });
  }, [dispatchRun, client, sessionId, fetchDraft]);

  const importPaths = useCallback((): Promise<void> => {
    const paths = importDraft
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line !== "");
    if (paths.length === 0) return Promise.resolve();
    return dispatchRun("model.import", async () => {
      const dispatch = await client.runStart({
        sessionId: sessionId as string,
        clientRequestId: `models-import-${crypto.randomUUID()}`,
        start: { work: "model.import", paths },
      });
      return projectAdmission(dispatch);
    }).then((lane) => {
      if (lane.kind === "IN_FLIGHT") {
        setImportDraft("");
      }
    });
  }, [dispatchRun, client, sessionId, importDraft]);

  const digest = useCallback(
    (logicalName: string): Promise<void> =>
      dispatchRun("model.digest", async () => {
        const dispatch = await client.runStart({
          sessionId: sessionId as string,
          clientRequestId: `models-digest-${crypto.randomUUID()}`,
          start: { work: "model.digest", logicalName },
        });
        return projectAdmission(dispatch);
      }).then(() => undefined),
    [dispatchRun, client, sessionId],
  );

  /** The truthful cancellation REQUEST (§12.3): a fresh key per
   * explicit attempt; the observed outcome renders verbatim; the poll
   * CONTINUES (the run's terminal state, not the cancel answer, is
   * the truth). */
  const cancel = useCallback(async (): Promise<void> => {
    const current = activeRun(runRef.current);
    if (sessionId === null || dispatchInFlight.current || current === null) return;
    if (current.kind !== "IN_FLIGHT") return; // no execution id yet
    dispatchInFlight.current = true;
    setBusy(true);
    try {
      const dispatch = await client.runCancel({
        sessionId,
        executionId: current.executionId,
        clientRequestId: `models-cancel-${crypto.randomUUID()}`,
      });
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        setCancelOutcome(dispatch.result.cancellation);
      } else if (dispatch.transport === "TRANSPORT") {
        setCancelOutcome(`TRANSPORT (${dispatch.failure.kind}) — the request's outcome is UNKNOWN`);
      } else if (dispatch.transport === "MISMATCH") {
        setCancelOutcome(`CONTRACT MISMATCH: ${dispatch.error}`);
      } else {
        setCancelOutcome(
          `${dispatch.response.rejection ?? "REJECTED"}: ${reasonOf(dispatch.response.result) ?? "(no reason)"}`,
        );
      }
    } finally {
      dispatchInFlight.current = false;
      setBusy(false);
    }
  }, [sessionId, client]);

  /** The explicit re-poll after a STALE lane — the user's action
   * (G4), never an automatic recovery. */
  const repoll = useCallback((): void => {
    setPollEpoch((epoch) => epoch + 1);
  }, []);

  // The bounded run observation: fires for the ONE admitted,
  // non-terminal run, stops at terminal / TRANSPORT / REJECTED /
  // MISMATCH / unmount. The key is the execution id — stable across
  // the lane's own patches, so the loop never restarts mid-run.
  const activeExecutionId =
    active !== null && active.kind === "IN_FLIGHT" ? active.executionId : null;
  useEffect(() => {
    if (activeExecutionId === null || sessionId === null) return;
    let stopped = false;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const step = async (): Promise<void> => {
      if (stopped) return;
      const dispatch = await client.runGet({
        sessionId,
        executionId: activeExecutionId,
      });
      if (stopped) return;
      if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
        const document = dispatch.result;
        if (document.terminal) {
          setRun((previous) =>
            previous !== null &&
            previous.kind === "IN_FLIGHT" &&
            previous.executionId === activeExecutionId
              ? terminalLane(document)
              : previous,
          );
          // The closure's OBSERVED baseline: exactly ONE context
          // re-read at the terminal (the landed file rides the NEXT
          // discovery scan; the ladder rests at its own truth) —
          // never polling.
          void refreshContext();
          return;
        }
        setRun((previous) =>
          previous !== null &&
          previous.kind === "IN_FLIGHT" &&
          previous.executionId === activeExecutionId
            ? {
                ...previous,
                runState: document.state,
                progress: progressOf(document.work, document.progress),
                stale: false,
                failure: null,
              }
            : previous,
        );
        timer = setTimeout(() => void step(), MODELS_POLL_INTERVAL_MS);
        return;
      }
      if (dispatch.transport === "TRANSPORT") {
        // G4: the loop STOPS — the re-poll is the user's explicit action.
        setRun((previous) =>
          previous !== null && previous.kind === "IN_FLIGHT"
            ? {
                ...previous,
                stale: true,
                failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
              }
            : previous,
        );
        return;
      }
      if (dispatch.transport === "MISMATCH") {
        setRun({ kind: "POLL_MISMATCH", error: dispatch.error });
        return;
      }
      setRun({
        kind: "POLL_REJECTED",
        rejection: dispatch.response.rejection ?? "REJECTED",
        reason: reasonOf(dispatch.response.result),
      });
    };
    void step();
    return () => {
      stopped = true;
      if (timer !== null) clearTimeout(timer);
    };
  }, [activeExecutionId, pollEpoch, sessionId, client, refreshContext]);

  const editFetchDraft = useCallback((field: keyof FetchDraft, value: string): void => {
    setFetchDraft((previous) => ({ ...previous, [field]: value }));
  }, []);

  const editImportDraft = useCallback((value: string): void => {
    setImportDraft(value);
  }, []);

  return {
    models,
    modelStates,
    refreshContext,
    run,
    cancelOutcome,
    fetchDraft,
    importDraft,
    editFetchDraft,
    editImportDraft,
    load,
    unload,
    fetchModel,
    importPaths,
    digest,
    cancel,
    repoll,
    busy,
    runInFlight,
  };
}

/** The admission answers' shared projection (every admission shape
 * carries the execution identity; the STARTING state is the
 * registry's own admission law — model.load/model.unload echo it,
 * run.start implies it). */
interface Admission {
  readonly executionId: string;
  readonly runState: ExecutionState;
}

function projectAdmission(
  dispatch: DispatchResult<{ readonly execution_id: string }>,
): DispatchResult<Admission> {
  if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
    return {
      ...dispatch,
      result: {
        executionId: dispatch.result.execution_id,
        runState: "STARTING",
      },
    };
  }
  return dispatch;
}

/** The last admitted, non-terminal run — at most one exists by the
 * dispatch guard (boundedness: ONE poller, ONE in-flight run). */
function activeRun(run: ModelsRunLane | null): ActiveRunLane | null {
  if (run === null) return null;
  if (run.kind === "DISPATCHING" || run.kind === "IN_FLIGHT") return run;
  return null;
}

/** The live progress, narrowed per work kind (anything else is
 * honestly UNRECOGNIZED — the run document's own truth, never a
 * coerced shape). */
function progressOf(
  work: string,
  progress: Readonly<Record<string, unknown>> | null,
): ModelsRunProgress | null {
  if (progress === null) return null;
  if (work === "model.fetch") {
    const parsed = modelFetchProgressSchema.safeParse(progress);
    return parsed.success ? { kind: "FETCH", progress: parsed.data } : { kind: "UNRECOGNIZED" };
  }
  if (work === "model.import") {
    const parsed = modelImportProgressSchema.safeParse(progress);
    return parsed.success ? { kind: "IMPORT", progress: parsed.data } : { kind: "UNRECOGNIZED" };
  }
  return { kind: "UNRECOGNIZED" };
}

/** The terminal lane from the run document — the observed truth,
 * narrowed per work kind at the consumer (the five closed shapes the
 * surface starts; a completion whose result deviates is the honest
 * COMPLETED_MISMATCH lane, never a coerced bubble). */
function terminalLane(run: {
  work: string;
  state: ExecutionState;
  result: Readonly<Record<string, unknown>> | null;
  failure_type: string | null;
  diagnostics: readonly string[];
}): ModelsRunLane {
  if (run.state === "COMPLETED" && run.result !== null) {
    const outcome = narrowOutcome(run.work, run.result);
    if (outcome !== null) {
      return { kind: "COMPLETED", outcome };
    }
    return {
      kind: "COMPLETED_MISMATCH",
      error: `the run COMPLETED but its result deviates from the ${run.work} contract`,
    };
  }
  if (run.state === "FAILED") {
    return {
      kind: "FAILED",
      work: run.work,
      failureType: run.failure_type,
      diagnostics: run.diagnostics,
    };
  }
  return {
    kind: "OTHER_TERMINAL",
    work: run.work,
    runState: run.state,
    diagnostics: run.diagnostics,
  };
}

/** The per-work result narrowing (the consumer's own closed depth). */
function narrowOutcome(
  work: string,
  result: Readonly<Record<string, unknown>>,
): ModelsRunOutcome | null {
  if (work === "model.load") {
    const parsed = modelLoadResultSchema.safeParse(result);
    return parsed.success ? { work, result: parsed.data } : null;
  }
  if (work === "model.unload") {
    const parsed = modelUnloadResultSchema.safeParse(result);
    return parsed.success ? { work, result: parsed.data } : null;
  }
  if (work === "model.fetch") {
    const parsed = modelFetchResultSchema.safeParse(result);
    return parsed.success ? { work, result: parsed.data } : null;
  }
  if (work === "model.import") {
    const parsed = modelImportResultSchema.safeParse(result);
    return parsed.success ? { work, result: parsed.data } : null;
  }
  if (work === "model.digest") {
    const parsed = modelDigestResultSchema.safeParse(result);
    return parsed.success ? { work, result: parsed.data } : null;
  }
  return null;
}

/** One context read's four-lane application — the shared honest form
 * (every READ state carries its own lane; none collapses). */
async function applyLane<T>(
  dispatch: DispatchResult<T>,
  set: (lane: ContextLoad<T>) => void,
): Promise<void> {
  if (dispatch.transport === "DELIVERED" && dispatch.status === "OK") {
    set({ kind: "LOADED", result: dispatch.result, at: Date.now() });
  } else if (dispatch.transport === "TRANSPORT") {
    set({
      kind: "TRANSPORT",
      failure: `${dispatch.failure.kind}: ${dispatch.failure.detail}`,
      at: Date.now(),
    });
  } else if (dispatch.transport === "MISMATCH") {
    set({ kind: "MISMATCH", error: dispatch.error, at: Date.now() });
  } else {
    set({
      kind: "REJECTED",
      rejection: dispatch.response.rejection ?? "REJECTED",
      reason: reasonOf(dispatch.response.result),
      at: Date.now(),
    });
  }
}

/** The gateway's reason, honestly typed (unknown on the wire). */
function reasonOf(result: Record<string, unknown> | undefined): string | null {
  const value = result?.["reason"];
  return typeof value === "string" ? value : null;
}
