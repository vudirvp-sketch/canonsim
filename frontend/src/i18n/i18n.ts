/**
 * The translation-boundary runtime (i18n-1 band-1, FRONTEND_UIUX_LAW
 * §17): `tr(key, params?)` resolves a catalogued message for the
 * CURRENT language, falling back to the default-locale base (catalog
 * .ts) for every key an overlay does not carry — a partially
 * translated surface stays honest, never blank. Locale-aware number
 * and clock formatting are owned by this same module (Intl over the
 * current language), so a surface never hand-joins a locale format.
 *
 * ZERO dependency: the module is stdlib-shaped (the platform's Intl
 * plus the catalog data) — a localization package would need the
 * AGENTS §8 dependency gate, and nothing here needs one.
 *
 * Language state is module-level (a plain mutable current language +
 * overlay registry): the boundary is a projection of the app's
 * language choice, never React state — rendered strings re-resolve
 * on the next render, and no surface re-mounts to translate. The
 * default resolves the default locale, so every existing suite that
 * never calls `setLang` observes the EN strings byte-for-byte.
 */
import { EN } from "./catalog.ts";
import type { MessageKey } from "./catalog.ts";

export type { MessageKey } from "./catalog.ts";

/** An overlay catalog: any subset of keys over the default base. */
export type Catalog = Readonly<Partial<Record<MessageKey, string>>>;

/** Interpolation params — `{name}` placeholders, string or number. */
export type TrParams = Readonly<Record<string, string | number>>;

const DEFAULT_LANG = "en";

let currentLang: string = DEFAULT_LANG;
const overlays = new Map<string, Catalog>();

/** The change listeners (the framework-free subscription half): a
 * surface that renders translated strings subscribes and re-renders
 * when the language changes — the module stays React-agnostic, the
 * hook (`useLanguage.ts`) is the only React-aware file. */
type LanguageListener = () => void;
const listeners = new Set<LanguageListener>();

/** The active language tag ("en" until a caller chooses another). */
export function currentLanguage(): string {
  return currentLang;
}

/** Choose the active language; missing keys keep falling back to EN.
 * Idempotent: re-selecting the active language notifies nobody. */
export function setLang(lang: string): void {
  if (lang === currentLang) return;
  currentLang = lang;
  for (const listener of listeners) listener();
}

/** Subscribe to language changes; returns the unsubscribe function. */
export function subscribeLanguage(listener: LanguageListener): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

/** Register (or merge into) an overlay catalog for a language. */
export function addCatalog(lang: string, catalog: Catalog): void {
  const previous = overlays.get(lang) ?? {};
  overlays.set(lang, { ...previous, ...catalog });
}

/** Resolve one catalogued message, interpolating `{name}` params. */
export function tr(key: MessageKey, params?: TrParams): string {
  const template = overlays.get(currentLang)?.[key] ?? EN[key];
  if (params === undefined) return template;
  return template.replace(/\{([a-zA-Z][a-zA-Z0-9_]*)\}/g, (placeholder, name: string) =>
    Object.hasOwn(params, name) ? String(params[name]) : placeholder,
  );
}

/** The current language as an Intl-usable tag (EN on a malformed tag). */
function localeTag(): string {
  try {
    void new Intl.Locale(currentLang);
    return currentLang;
  } catch {
    return DEFAULT_LANG;
  }
}

/** Locale-aware number formatting — the module owns the format, the
 * caller never hand-joins a locale's separators. */
export function formatNumber(value: number, options?: Intl.NumberFormatOptions): string {
  return new Intl.NumberFormat(localeTag(), options).format(value);
}

/** Locale-aware clock time for an ISO instant (HH:MM:SS, 24-hour).
 * UTC by construction: the app's clock strings are slices of UTC
 * instants (the log vocabulary), so the formatter owns the FORMAT
 * (digits, separators) while the zone stays machine-independent. */
export function formatClock(iso: string): string {
  return new Intl.DateTimeFormat(localeTag(), {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
    timeZone: "UTC",
  }).format(new Date(iso));
}
