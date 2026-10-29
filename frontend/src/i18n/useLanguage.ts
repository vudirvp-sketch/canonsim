/**
 * The one React-aware file of the translation boundary (i18n-1, the
 * `lang` plumbing): a surface renders translated strings and calls
 * this hook, so a language change re-renders it through the ordinary
 * React scheduler instead of a custom event bus. `useSyncExternalStore`
 * is the platform primitive — the store is the module-level language
 * (`i18n.ts`), the snapshot is `currentLanguage()`.
 *
 * The hook is the PLUMBING, never a second source of truth: it neither
 * caches nor owns the language. A surface that does not call it still
 * resolves the right strings on its next render (the boundary's own
 * law); the hook only guarantees that render happens immediately.
 */
import { useSyncExternalStore } from "react";

import { currentLanguage, subscribeLanguage } from "./i18n.ts";

/** The active language, reactive — re-renders the caller on change. */
export function useLanguage(): string {
  return useSyncExternalStore(subscribeLanguage, currentLanguage, currentLanguage);
}
