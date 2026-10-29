/**
 * The i18n boundary's public surface (i18n-1 band-1): the catalog
 * data (catalog.ts) and the runtime (i18n.ts) behind one import —
 * `tr`, the language plumbing, and the locale-aware formatters.
 * FRONTEND_UIUX_LAW §17 names this the ONE translation boundary;
 * the architecture guard's T1 scan enforces that a migrated surface
 * renders no raw literal around it.
 */
export { EN } from "./catalog.ts";
export type { Catalog, MessageKey, TrParams } from "./i18n.ts";
export {
  addCatalog,
  currentLanguage,
  formatClock,
  formatNumber,
  setLang,
  subscribeLanguage,
  tr,
} from "./i18n.ts";
export { useLanguage } from "./useLanguage.ts";
