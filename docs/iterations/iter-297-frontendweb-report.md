# Отчёт итерации iter-297 — frontendweb: IA REPAIR
(сплит реестров product/diagnostic, вертикальный рейл, контракт
навигации — D-247)

Вызов владельца: «вперед реализовывай и приступай к работе, делай
так как наиболее качественно и логично/обоснованно» — поверх
внешнего IA-вердикта (design-review delivery). Вердикт обработан по
методу D-246: наблюдения верифицированы по коду на HEAD `deda444`,
предписания приняты только там, где они мирятся с действующим
законом. Класс риска: R2 (frontend-local; ноль Python, ноль canon,
INV-1..5 не тронуты).

## 0. Верификация наблюдений вердикта (по коду, до реализации)

| Наблюдение вердикта | Проверка на HEAD `deda444` |
|---|---|
| Навигация строится из реестра panes | `Shell.tsx:47` — `props.panes.map(...)`; источник — массив в `App.tsx` |
| Диагностика — равноправные пункты меню | `Session`/`Gateway`/`Load probe` в одном ряду с `Observatory`/`Settings` |
| Инженерная проза в chrome | заголовок: «the browser is an untrusted presentation client…»; nav-заметка «only the active surface mounts…» |
| Навигация вертикальная | нет: `.shell-nav { flex-wrap: wrap }` — горизонтальные табы |
| Chat как primary surface | не существует (последний ряд Phase 3; ops уже живут в gateway) |

Диагноз вердикта верен — и главная опора не внешний аудит, а
СВОЙ закон: `FRONTEND_UIUX_LAW` §2 уже называет этот failure mode
(«a nav rail is a navigation instrument, never a feature
directory»). Ремонт возвращает фронтенд к действующему закону, а не
создаёт новый.

## A. Что высажено (7 кодовых/тестовых путей + 8 доковых — один
когерентный минимальный срез, сверх мягкого лимита 3–5, освоено в
worklog)

- **`frontend/src/features/shell/Shell.tsx`** — разделённые
  сущности `ProductRoute` (id/label/hint/pinned/element) и
  `DiagnosticSurface` (id/label/hint/element); вертикальный рейл
  («Primary navigation») только из product-маршрутов + ОДИН
  приглушённый пункт Diagnostics; workspace ровно один; при входе в
  диагностику — собственная вторичная навигация
  («Diagnostic surfaces») в workspace, не в рейле. Дисциплина
  монтинга не изменилась: монтируется ТОЛЬКО активная поверхность
  (переключение размонтирует предыдущую — boundedness).
- **`frontend/src/app/composition/App.tsx`** — composition root
  владеет сплитом: `routes` (Trajectory LIVE / Observatory HISTORY /
  Settings pinned) и `diagnostics` (Session lifecycle / Gateway /
  Load probe). Chrome очищен: h1 «CanonSim Workbench» (dev-тег
  «phase-3 slice» и архитектурные эссе убраны), identity-стриплайн
  остался (session/rev/seq/freshness + refresh — §9's context strip,
  STATE-labels по VISUAL_SYSTEM_UI §0.3 остаются, проза — нет);
  «new session» перенесён из chrome на поверхность Session (честный
  дом lifecycle-действия).
- **`frontend/src/app/composition/styles.css`** — layout
  приложения: header-строка + rail слева (216px) + скроллящийся
  workspace (контент с max-width 980px); приглушённый Diagnostics
  (muted, разделитель, без акцента); pinned Settings в конце рейла.
  **Токенизация**: 9 сырых hex-литералов итераций 289–296 названы
  токенами (`--row-divider`, `--row-hover`, `--row-selected-live`,
  `--row-selected-history`, `--text-mono`, `--border-strong`) —
  канальные выделения строк LIVE/HISTORY остались STATE-классом,
  dimmed-формы канальных оттенков, никогда не второй интерактивный
  акцент.
- **`frontend/src/features/session-lifecycle/SessionLifecycle.tsx`**
  — новый проп `recreateSession` + кнопка «new session» (FRESH
  таб-идентичность; старая сессия остаётся истечь серверно, никогда
  не «тихо detached»).
- **`frontend/tests/integration/Shell.test.tsx`** (новый, 12 тестов)
  — два банда: (1) механизм Shell на синтетических маршрутах
  (рейл = только product + Diagnostics; диагностические лейблы
  никогда в рейле; ровно один active-workspace; только активная
  поверхность монтируется; вход/выход из диагностики; initialRouteId;
  honest empty); (2) IA-acceptance на настоящем `App` с
  fixture-gateway (routing-мок по operation): рейл = ровно
  `[Trajectory, Observatory, Settings, Diagnostics]`; proof-лейблы
  только во вторичной навигации; chrome несёт identity-стриплайн и
  НЕ несёт инженерной прозы (эссе об «untrusted presentation
  client», «only the active surface mounts» — отсутствуют);
  Gateway-диагностика диспатчит `app.status`; Settings монтируется
  поверх CONFIG-стора.
- **`frontend/tests/integration/SessionLifecycle.test.tsx`** —
  прокинут `recreateSession` в mount-хелпер.
- **`frontend/tests/architecture/guard.test.ts`** — новый ряд V1
  (visual floor): в `styles.css` сырые цвета (`#hex`, `rgb(`)
  допустимы ТОЛЬКО в `:root` — цвет есть токен, литерал есть
  нарушение (VISUAL_SYSTEM_UI §2/§3). Ряд ПОЙМАЛ стоящее нарушение
  (9 литералов) и закрыл его токенизацией — guard отработал как
  положено в первый же день.
- **Доки**: `FRONTEND_UIUX_LAW.md` §2.1 (контракт навигации +
  канонический IA-дерево + acceptance floor), `DECISIONS.md` D-247,
  `FRONTEND_WEB_AGENT_CONTEXT.md` (stage map), `TASKS.md` (ledger,
  iter-288 выселен), `STATUS.md`, `worklog.md` (iter-287 выселен),
  `frontend/README.md`, этот отчёт.

## B. Законы, которые несёт ремонт

- **FRONTEND_UIUX_LAW §2.1 (новый, D-247)**: PRIMARY NAVIGATION
  expose only approved user-facing product intents;
  first-class surface ≠ navigation item; diagnostic/proof/
  instrumentation surfaces никогда в primary navigation;
  feature registry ≠ navigation registry; Settings закреплён в
  конце рейла, вторичная навигация — его собственное дело
  (inf-1 «Settings ≠ Inference Control» стоит: inference-контроли —
  отдельная поверхность, не подраздел Settings).
- **Реконсиляция вердикта с законом (по методу D-246: донор
  информирует, закон решает)**: (1) Settings-структура вердикта
  (Inference/LLM подразделы) отклонена — inf-1; (2) Trajectory
  ОСТАЁТСЯ product-маршрутом (LIVE-половина dual-read пары,
  FRONTEND_WEB_LAW §4 — IA вердикта её терял); (3) каналы
  LIVE/HISTORY/CONFIG — STATE-класс токенов, не «вторые акценты»
  (закон об одном акценте не тронут, уточнён формулировкой
  «one INTERACTIVE accent»); (4) «Status/…» вердикта уже существует
  как identity-стриплайн §9 — проб-консоль GatewayStatus уехала в
  диагностику, а не стала product-секцией.
- VISUAL_SYSTEM_UI §0.3: доказательство состояния никогда не
  прячется ради визуального спокойствия — из chrome ушла ПРОЗА,
  STATE-метки (freshness, rev/seq, LIVE/DRAFT) остались.
- Boundedness и honesty-механики предыдущих итераций не тронуты:
  G4 no-retry, dual-read метки, закрытые контракты, RESYNC — всё
  прежнее (INV-ами и тестами 289–296).

## C. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped (93.9s)
ruff check .                              → clean
python scripts/docguard.py                → clean (caps + state-layer)
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 108 passed / 9 files (96 + 12)
frontend: npm run build                   → dist 8.61kB css / 366.98kB js
```

**Живой смок против реального gateway** (запущен
`python scripts/workbench_app.py`, bind 127.0.0.1:8765):
- `app.status` → OK, полный словарь ops (включая `chat.send`,
  `model.*`, `inference.*` — следующий ряд не backend-blocked);
- `session.create` (client_request_id top-level) → OK, session_id
  выдан;
- `backend.settings` → OK, applies: next-spawn + command_preview;
- `chat.send` на несуществующей сессии → честный DOMAIN_REJECTED
  («no such session») — op существует, лейн отказов верифицирован.

**Живой браузерный closure** (Vite dev server + proxy + headless
браузер, снимки приложены к сессии:
`iter-297-rail-trajectory.png`, `iter-297-diagnostics.png`):
- рейл = ровно 4 approved-записи (Trajectory/Observatory/Settings/
  Diagnostics), identity-стриплайн с minted session id;
- клик Diagnostics → вторичная навигация «Diagnostic surfaces»
  (Session lifecycle / Gateway / Load probe) внутри workspace,
  поверхности монтируются; «new session» на поверхности Session;
- возврат на Trajectory — product-workspace восстановлен;
- консоль: ноль ошибок (только vite-connect debug и React DevTools
  info).

**Мутационная проверка V1** (по канону iter-293): guard поймал
реальное стоящее нарушение в момент посадки (9 hex-литералов) —
красный → токенизация → зелёный; falsifier работает, это не
декоративный тест.

## D. Границы / следующий шаг

- Чат-строка §2.1 («Chat lands as its own surface row at the rail's
  head») — СЛЕДУЮЩИЙ ряд (iter-298): контракт-зеркало
  `model.*`/`inference.*`/`chat.send` по образцу Settings +
  поверхность (header/viewport/composer/status) с §27 transfer
  record по донорам §7 (LM Studio/Jan-класс механик composer'а).
  Живой proof-band для chat.send с загруженной моделью —
  owner-side; в этой среде честно закрыты только лейны
  DOMAIN_REJECTED/UNKNOWN.
- Settings-вторичная навигация (General/Deployment/Appearance/
  Advanced) — отдельный ряд после Chat (вердикт-шаг 5, в
  реконсиляции с inf-1).
- Визуальная полировка (wb-12 токен-аудит по полной таксономии,
  типографический контракт §2.2) — ПОСЛЕ композиции, как
  требует вердикт и §0 delivery order.
- Стоящие границы без изменений: SSE/WebSocket, Tauri, PWA — каждое
  своё admission.

## E. Риски

- Смена layout (full-viewport rail) — surfaces рассчитаны на
  max-width 980px внутри workspace; на узких окнах (<860px) колонки
  поверхностей складываются (существующий media-query). Полный
  responsive/DPI-проход — LAW §16, вне этого ряда.
- Диагностика «на один клик глубже» — приемлемо по вердикту
  («Advanced/Developer band»); если владельцу понадобится
  developer-mode флаг — отдельная строка, не расширение этого ряда.
- Рейл-лейблы/порядок — MAY VARY по target envelope; фиксируется
  только состав (approved set), что и пинят тесты.

## F. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/features/shell/Shell.tsx frontend/src/app/composition/App.tsx frontend/src/app/composition/styles.css frontend/src/features/session-lifecycle/SessionLifecycle.tsx frontend/tests/integration/Shell.test.tsx frontend/tests/integration/SessionLifecycle.test.tsx frontend/tests/architecture/guard.test.ts docs/FRONTEND_UIUX_LAW.md docs/DECISIONS.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-297-frontendweb-report.md frontend/README.md
git status --short
git commit -m "iter-297-ia: Phase 3 IA repair — the product/diagnostic registry split, the vertical rail, the navigation contract (D-247)"
git push
```

Delta-архив: `canonsim_iter-297-ia_2026-10-01.zip` (BASE_COMMIT
`deda444...`, изменённые/созданные пути — ровно 15, удалений нет),
приложен к сессии + прямая ссылка и md5 в чате.
