/**
 * The EventSource test double (tests only — the adapter's contract
 * rows run against this, never against a real socket): a minimal
 * implementation of the EventSource surface the adapter consumes
 * (constructor URL, addEventListener for the closed frame vocabulary,
 * close, readyState, the CONNECTING/OPEN/CLOSED constants). The frame
 * emission helpers drive the adapter from the tests exactly as the
 * browser would dispatch named SSE frames.
 *
 * `resetInstances()` between rows keeps the construction ledger
 * honest (one instance per dial — the "no second stream" law).
 */

export class FakeEventSource {
  static readonly CONNECTING = 0;
  static readonly OPEN = 1;
  static readonly CLOSED = 2;

  static instances: FakeEventSource[] = [];

  static resetInstances(): void {
    FakeEventSource.instances = [];
  }

  readonly url: string;
  readyState = FakeEventSource.CONNECTING;
  closed = false;

  private readonly listeners = new Map<string, Array<(event: unknown) => void>>();

  constructor(url: string) {
    this.url = url;
    FakeEventSource.instances.push(this);
  }

  addEventListener(type: string, listener: (event: unknown) => void): void {
    const list = this.listeners.get(type) ?? [];
    list.push(listener);
    this.listeners.set(type, list);
  }

  close(): void {
    this.closed = true;
    this.readyState = FakeEventSource.CLOSED;
    this.listeners.clear();
  }

  /** One named SSE frame, exactly as the browser dispatches it (the
   * data string + the implicit OPEN state of a delivering stream). */
  emit(type: string, data: string): void {
    this.readyState = FakeEventSource.OPEN;
    for (const listener of [...(this.listeners.get(type) ?? [])]) {
      listener({ data } as unknown as MessageEvent<string>);
    }
  }

  /** One error event, with the readyState AFTER the failure — the one
   * signal EventSource exposes (no status code, per the SSE spec). */
  emitError(readyStateAfter: number): void {
    this.readyState = readyStateAfter;
    for (const listener of [...(this.listeners.get("error") ?? [])]) {
      listener({} as unknown as Event);
    }
  }

  listenerCount(type: string): number {
    return this.listeners.get(type)?.length ?? 0;
  }
}

/** A document's wire form as a frame data string. */
export function frameData(document: unknown): string {
  return JSON.stringify(document);
}
