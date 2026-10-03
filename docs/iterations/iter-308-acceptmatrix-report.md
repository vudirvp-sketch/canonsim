# Отчёт итерации iter-308 — frontendweb: ACCEPTANCE MATRIX

(закрытие ПОЛНОЙ матрицы приёмки из пакета —
`docs/frontendweb/archive/…/docs/ACCEPTANCE_MATRIX.md`, ворота S0
давно зелёные, ряд был первым в стоящей очереди STATUS)

Вызов владельца: «продолжить работу по фронтенду: матрица приёмки
или CI-ряды; также можешь установить llama.cpp и закрыть "живые
полосы" и/или сыграть роль десятков/сотен тестеров и протестировать
интерфейс и все системы» — синтез по §2.7: матрица приёмки ЕСТЬ
масс-сессия тестеров (каждая строка матрицы = проверка с
доказательством), llama.cpp — окружение для живых полос внутри
матрицы. CI-ряды остались припаркованными рядами (честно отмечены
в таблице как OPEN — каждое своей итерацией, CI-файлы = §8
stop&confirm). Класс риска: **R0/R1** — итерация чистой верификации,
НИ ОДНОЙ правки кода; изменены только документы состояния (5
файлов, все — статусные). BASE_COMMIT `3e177b3`.

## A. Что исполнено (сессия «десятков тестеров»)

**Окружение** (вне диффа, gitignored): llama.cpp b11337 (v0.5.0-dev,
commit d775ebf36, ubuntu-x64 CPU — тот же билд, что iter-302) в
`workbench/runtime/llama.cpp/llama-b11337/`; гейтвей сам обнаружил
exe дискавери-сканом (баннер startup'а — закон разрешения проверён
живьём снова). Модели пришли ЧЕРЕЗ собственный `model.fetch`
гейтвея: `llama2.c-stories15M.Q4_K_M.gguf` (20 986 944 байта,
mradermacher) и `qwen2.5-0.5b-instruct-q4_k_m.gguf` (491 400 032
байта — байт-в-байт размер из iter-302, официальный репозиторий
Qwen). Настоящий canon-ран для HISTORY-мира сгенерирован CLI:
`run_125_0` (seed 125, day1_full, 56 событий, тик 1456).

**API-батареи** (реальные POST /op, свежие idempotency-ключи,
транскрипты в сессии):

- **fetch**: 10/10 — полоса arrival (COMPLETED, честный
  exists-refusal при повторе, DUPLICATE_REQUEST при конфликте
  материала, model.list с models_root);
- **liveband**: 24/24 — полный lifecycle: DISCOVERED → load → ACTIVE
  → chat COMPLETED (НАСТОЯЩИЙ ответ: stories — «Healed by the
  people who were very happy…», finish length; qwen — «The capital
  of France is Paris.», finish stop, effective temp 0.8 от BASE) →
  single-slot rejection дословно → unload → EVICTED → re-selection →
  EVICTED; backend identity `{model, build: b11337-d775ebf36}` в
  каждом ответе;
- **matrix-api**: 31/31 — все честные полосы отказов (unknown op /
  unknown argument / wrong type / missing field → DOMAIN_REJECTED
  дословно), G4 ОБЕ кромки (идентичный повтор → `duplicate=true`
  реплей ТОГО ЖЕ execution; тот же ключ + другой материал →
  DUPLICATE_REQUEST), CAS-гарда (STALE_REVISION на старой ревизии,
  честный takeover на текущей), LIVE-хвост (упорядоченный replay,
  RESYNC_REQUIRED после переполнения 256-event retention, одно-POST
  восстановление gapless, future-cursor → честное пустое окно),
  inference.read/update (плоское поле, partial OK, unknown control →
  отказ), backend.settings.read/update (закрытый трёх-полевой сет,
  applies: next-spawn), chat FAILED с наблюдённой причиной (backend
  down — никогда не сфабриковано), cancellation terminality, run.get
  foreign execution → отказ, app.status (21 ops, LOOPBACK), detach
  под CAS;
- **observatory**: 12/12 — HISTORY-мир над настоящим committed-раном
  (identity-строка: authority CANONICAL, profile CANON_VIEW, header
  {seed 125, pack tavern_pack@0.1, schema 0.3, commit 3e177b3,
  python 3.12.14}, total_events 56), bounded window 50, forward
  pagination ЗАМЕНЯЕТ окно (курсор = event id, без повторов),
  unknown run → NO MATCH дословно (форма фикстуры).

**Браузерная сессия** (Vite dev server + proxy + headless Chromium
через agent-browser; 15 скриншотов; **ноль ошибок консоли** на всём
драйве):

- **Trajectory**: +10k synthetic → rows 10001, спейсер 280 028px,
  DOM 201 узел (виртуализация S0-2 живьём), честный банер
  presentation-only, jump-to-seq 5000 → scrollTop 139 972 (окно
  4994–4998), stream OPEN;
- **Chat**: honest FAILED дословно («run FAILED · EngineError — …
  unreachable after 5 tries: Connection refused»), затем COMPLETED
  через живую модель с полной строкой происхождения («run 189e4ad1…
  · finish length · …stories15M… · temp requested (absent — the
  profile's BASE) → effective 0.7 · max_tokens 512» — пара
  REQUESTED/EFFECTIVE отрендерена);
- **Models**: чипы дискавери, load ЧЕРЕЗ СОБСТВЕННУЮ кнопку → ACTIVE,
  второй load при ACTIVE → DOMAIN_REJECTED дословно («…is ACTIVE —
  unload first (the slot is single this row…) — nothing was sent; a
  new dispatch is your explicit new command (never an auto-retry)»),
  unload → EVICTED;
- **Inference**: поиск temperature, правка в draft, Save → «draft
  matches the observed document» (замыкание §8 живьём), документ
  гейтвея подтверждает observed 0.55 EFFECTIVE source=profile;
- **Observatory**: rescan → 1 found, open → identity-строка + окно
  50/56 DURABLE, next window → последние 6 («this is the run's
  end»);
- **Settings**: Deployment draft → save changes → reconciliation;
  About (identity: service, contract, LOOPBACK, 21 ops); черновик
  ПЕРЕЖИЛ переключение секций Deployment → About → Deployment
  (закон iter-301 воспроизведён);
- **Diagnostics**: session lifecycle (attach → «ACCEPTED → EFFECTIVE:
  ATTACHED (revision 1), lease 30s; OBSERVED rides the re-read»),
  gateway probes ×3 (DOMAIN_REJECTED / STALE_REVISION /
  DUPLICATE_REQUEST — все DELIVERED · REJECTED дословно), **S0-4 с
  живым llama-server: 50 ops, 0.4s, 124.9 ops/s** (attach+get пары;
  iter-302 мерил ≈108–110);
- **Два таба**: ДВЕ независимые сессии (526563… vs 034428… — нет
  общего стора, S0-3), focused-tab политика через собственный
  механизм (visibilityState=hidden → фаза **STALE**, коннект закрыт;
  visible+focus → повторное подключение, stream OPEN снова), live
  push (события через API → строки 58→62 БЕЗ рефреша), transport
  switch (stream → poll 1s: буфер выжил, 62→64 через poll; обратно
  → stream).

## B. МАТРИЦА ПРИЁМКИ — таблица вердиктов

Форма: строка пакета → вердикт (VERIFIED = живое доказательство
этой сессии и/или исполняемый тест; OPEN = честно открытый
припаркованный ряд) → доказательство. Владелец закона каждой строки
не переиздаётся здесь (D-024): FRONTEND_WEB_LAW.md и его семья.

### Foundation

| Строка | Вердикт | Доказательство |
|---|---|---|
| сборка воспроизводима из lockfile | VERIFIED | package-lock.json закоммичен; ДВЕ сборки подряд — байт-идентичные хэши (index-CU_4p9EM.css / index-MLwP2iY7.js) |
| один видимый composition root | VERIFIED | guard.test.ts (one composition root); src/app/composition/ единственный |
| нет feature-private-state обходов | VERIFIED | guard R1 (никакого browser storage как истины) + интеграционные ряды |
| runtime-валидация на границе клиента | VERIFIED | validators.ts (99 рядов) + fixtures-манифест; каждый wire-документ через zod |
| surface-модули по SURFACE_MODULE_CONTRACT | VERIFIED | features/* с собственными state-matrix; guard (нет cross-feature импортов, `import type`-only стейт) |

### Routing / snapshot truth

| Строка | Вердикт | Доказательство |
|---|---|---|
| активный закон прежде исторического | VERIFIED | FRONTEND_WEB_LAW §1 (прецеденция); архив md5-пinned, никогда не live |
| snapshot provenance записывает HEAD/base/dirty | VERIFIED | пакета (cd84069, верифицирован iter-288) + BASE_COMMIT-дисциплина каждой итерации (§12.1) |
| исторический Redot-материал не перекрывает активных владельцев | VERIFIED | D-245: дерево удалено; вопросы → архив, никогда repo-файл |

### Application truth

| Строка | Вердикт | Доказательство |
|---|---|---|
| operation/execution identity сохранена | VERIFIED | execution_id во всех run-семьях (обе батареи + UI-строки происхождения) |
| UNKNOWN остаётся UNKNOWN | VERIFIED (тест-уровень) | тест-классы: test_gateway.py 36, client.test.ts 15 (SENT_OUTCOME_UNKNOWN вокабуляр); живьём не форсируется (нужен kill mid-dispatch) |
| cancellation terminality честна | VERIFIED | run.cancel живьём (батарея); UI-заметка «a request is never a completion» |
| stale/reconnect/resync честны | VERIFIED | RESYNC_REQUIRED живьём (retention overflow), STALE живьём (hidden tab), повторное подключение живьём |
| credentials вне URLs/logs/bundle | VERIFIED | contract.py §21 (auth никогда в digest); test_sse_stream.py 24 (auth никогда в stream URLs) |
| фронтенд не пере-реализует retry/deadline/idempotency | VERIFIED | G4 живьём: duplicate=true реплей, DUPLICATE_REQUEST конфликт, авто-ретраев нет (UI-текст + поведение) |
| requested/accepted/effective/observed различимы | VERIFIED | Chat-строка происхождения (temp requested → effective 0.7); Settings/Inference §8-замыкания живьём; attach ACCEPTED→EFFECTIVE→OBSERVED |
| model lifecycle из evidence приложения | VERIFIED | лестница-чипы = model.states' собственный ответ; DISCOVERED≠ACTIVE≠EVICTED живьём через кнопки UI |
| replay identity / material input identity где открыты | VERIFIED (backend) / NOT-EXPOSED (UI) | артефакты несут replay_of (backend-тесты); UI-кнопки replay нет — честно не открыто |
| material adapters: contract-тесты (capabilities/defaults/errors/cancel/stream/UNKNOWN) | VERIFIED | validators 99 + client 15 + stream 37 контракных рядов; run.cancel в батареях |

### Harness / Traceability

| Строка | Вердикт | Доказательство |
|---|---|---|
| Trajectory: упорядоченная evidence с семантическим курсором | VERIFIED | живьём: sequence-курсор, jump-to-seq, виртуализация 10k+ |
| replay UI запрашивает НОВУЮ execution identity | NOT-EXPOSED | строка условная («when application supports replay»); CLI поддерживает, UI-ряд будущий |
| failure presentation: что сломалось/причина/что цело/известно ли/действие/id | VERIFIED | FAILED-полоса Chat дословно с причиной + run id; G4-заметка о явном повторе |
| нет клиентского trajectory-лога, расходящегося с session.events | VERIFIED | кадры = ТЕ ЖЕ байты (D4-паритет, iter-305/306); synthetic строки помечены presentation-only на строке |
| нет браузерного agent/tool loop вне gateway-медиации | VERIFIED | по построению; guard (нет вторых транспортов) |

### Dual-read / stream budget

| Строка | Вердикт | Доказательство |
|---|---|---|
| LIVE ≠ HISTORY различимы в UI | VERIFIED | живьём оба мира: LIVE-лейбл + volatile-заметка (Trajectory) vs DURABLE + committed (Observatory) |
| live tail не выдаётся за полную историю | VERIFIED | заметка «never durable history» на поверхности; 50k-bound буфера |
| нет SSE/WebSocket без контракта + admission | VERIFIED | порядок допуска исполнен: контракт (iter-305) → адаптер (iter-306) → focused-tab |
| connection budget exhaustion ≠ gateway-down | VERIFIED (тест-уровень) | §5.2 первый класс; test_sse_stream.py; живьём не форсируется (нужно 6+ стримов) |
| focused-tab политика при стримах | VERIFIED | живьём: hidden → STALE (коннект закрыт), visible → повторное подключение; один стрим на таб |

### Browser runtime

| Строка | Вердикт | Доказательство |
|---|---|---|
| два таба — независимые клиенты | VERIFIED | живьём: две сессии; guard (нет общих мутабельных сторов) |
| cross-tab messaging — только non-authoritative UX | N/A (отсутствует) | никаких cross-tab каналов нет — соблюдено отсутствием |
| большие списки — virtualization/жёсткий bound | VERIFIED | живьём 10 001 строка / 201 DOM-узел; virtualization.test.ts 7 |
| gateway client изолирует транспорт | VERIFIED | guard: fetch ТОЛЬКО в client.ts, EventSource ТОЛЬКО в stream.ts |
| disconnect/stale/resync различимы | VERIFIED | живьём все три (FAILED/STALE/RESYNC lanes) |
| PWA/offline помечает stale | N/A (не поставляется) | PWA — припаркованный ряд |
| DOM vs Canvas/WebGL split | VERIFIED | canvas в клиенте нет вовсе — тривиально соблюдено; scene=off по умолчанию (S0-4) |
| никаких неограниченных live React-деревьев | VERIFIED | 10k+ строк → 201 узел; bound 50k буфера |

### Analytical UX

| Строка | Вердикт | Доказательство |
|---|---|---|
| context strip / identity recovery | VERIFIED | Observatory identity-строка (seed/pack/CANON_VIEW/CANONICAL); header-сессия |
| semantic shared selection | VERIFIED | event-id выборка в Observatory/Trajectory над тем же документом |
| query lifecycle | VERIFIED | явные reads (scan → open → window → next), никакого polling в HISTORY |
| empty/no-result различие | VERIFIED | «not scanned yet» ≠ «no run open» ≠ NO MATCH — все три отрендерены живьём |
| evidence/provenance reachability | VERIFIED | строка происхождения Chat; identity-строка Observatory; run.get артефакты |
| bounded compare/timeline/graph где допущено | VERIFIED (допущенное) | trajectory/virtualized + observatory/bounded; compare/graph — НЕ допущены (P3-ряды, законно) |
| reopenable analytical context | VERIFIED | повторное открытие ранов; re-attach сессий |

### Visual

| Строка | Вердикт | Доказательство |
|---|---|---|
| у каждой material-поверхности честная state matrix | VERIFIED | все 9 поверхностей прогнаны живьём; EMPTY/LOADING/ACTIVE/STALE/FAILED линии рендерятся |
| функциональная корректность прежде визуального рефайнмента | VERIFIED | порядок фаз исполнен (S0 → Phase 3 → visual floors V1/V2/V3 после) |
| Scene IR contract tests | VERIFIED (backend) | tests/test_scene_ir.py; web-рендерер — Phase 4 ряд |
| visual regression | PARTIAL | visual floors V1/V2/V3 — guard-сканы токенов (исполняемы); pixel-diff сюита НЕ поставлена (ряд) |
| bounded rendering | VERIFIED | виртуализация живьём; bound-буферы |
| compatibility identity check | VERIFIED | pack@0.1 + schema 0.3 + commit в identity-строке Observatory |
| missing/stale/incompatible asset degradation | VERIFIED (доступное) | backend loss → честный FAILED + UI жив; assets — Phase 4 |
| semantic-vs-presentation camera separation | N/A (Phase 4) | сцена не поставляется |

### Proof

| Строка | Вердикт | Доказательство |
|---|---|---|
| static/runtime/task/visual классы различимы | VERIFIED | TEST_PLAN §9 claim-packet; отчёты итераций различают формы |
| runtime-unavailable ≠ runtime-pass | VERIFIED | honest FAILED живьём; полосы никогда не сфабрикованы (форма, не текст) |
| evidence artifact переподключает результат к run/revision/source | VERIFIED | run id + модель + effective inputs в каждой строке происхождения |

### Current repository truth (снимок пакета)

Верифицировано как СТАРЕЮЩИЙ-ПО-КОНСТРУКЦИИ раздел: утверждения
пакета («React frontend does not yet exist», «SSE not landed»)
были истиной на момент снимка и превзойдены живым состоянием —
прецеденция §1 (активный закон > снимок) исполнена; сам раздел
пакета остаётся историческим свидетельством, никогда не
переиздаётся.

### Tooling floor

| Строка | Вердикт | Доказательство |
|---|---|---|
| deterministic typecheck + unit/contract | VERIFIED | tsc --noEmit чист; 252 vitest |
| dependency boundary check | VERIFIED (своя форма) | guard.test.ts 23 ряда — репо-форма вместо dependency-cruiser (D-244 дисциплина: существующий механизм прежде нового) |
| runtime validators по Python-фикстурам | VERIFIED | fixtures из живого гейтвея + manifest.json провенанс |
| virtualization proof | VERIFIED | живьём 10k+; unit-ряды |
| Playwright-класс multi-tab smoke | **OPEN (припаркован)** | сегодняшняя браузерная сессия — тот же класс evidence, но НЕ закоммиченный сюит; ряд остаётся рядом |
| frontend CI additive | **OPEN (припаркован)** | ci.yml = Python-only (pytest+ruff); ряд CI wiring — своя итерация, §8 stop&confirm |

### Optional P1 — N/A (не блокирует; layout manifest / capabilities screen — припаркованные ряды)

**Итог: 39 VERIFIED (включая 3 тест-уровня и 4 условно-N/A), 2
OPEN (Playwright smoke, frontend CI), 1 PARTIAL (visual regression:
токен-сканы есть, pixel-diff нет), 2 NOT-EXPOSED (replay UI,
честно). Ноль дефектов продукта за всю сессию.**

## C. Наблюдение (не KI, кандидат в ряд — вызов владельца)

Свежезагруженная страница показывает в шапке **DISCONNECTED** при
успешно созданной сессии — по букве собственного словаря честно
(«no successful read yet»: create — мутация, freshness считается по
session.get-чтению, первое чтение происходит на Session-lifecycle
поверхности или по кнопке refresh). Юзер может прочитать
«DISCONNECTED» как «гейтвей мёртв» при работающих операциях.
Кандидат: один OBSERVED-sync (session.get) сразу после create в
буте. Не правка этой итерации (R0-верификация; §2.4 scope-закон) —
ряд на вызов владельца.

## D. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2555 passed + 1 skipped
ruff check .                              → clean
python scripts/docguard.py                → clean
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 252 passed / 13 files
frontend: npm run build (×2)              → 18.89 kB css / 445.83 kB js
                                            (байт-идентичные хэши)
```

Живые батареи: см. §A (77 API-проверок: 10+24+31+12; браузерный
драйв: 15 скриншотов, 9 персона-тестеров, ноль ошибок консоли).
Транскрипты: `/tmp/iter308_{fetch,liveband,matrix_api,observatory}
_report.json` + скриншоты `/tmp/iter308_sh*.png` — приложены к
сессии.

## E. Границы / следующий шаг

- Матрица закрыта на ТЕКУЩУЮ глубину клиента; новые классы
  возможностей открывают свои строки (закон §7 — «update the
  acceptance docs only if a NEW capability class is introduced»).
- Открытые ряды (каждое своей итерацией, вызов владельца):
  Playwright multi-tab smoke (сегодняшний драйв — образец формы),
  CI wiring (frontend additive), visual regression pixel-diff,
  replay UI, DECISIONS-коллапс (36→30), B1/C4 law diffs из iter-303.
- Наблюдение §C — кандидат в ряд.
- Standing boundaries без изменений: SharedWorker, Tauri, PWA,
  Settings Appearance.

## F. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/iterations/iter-308-acceptmatrix-report.md
git status --short
git commit -m "iter-308-acceptmatrix: the full acceptance matrix closed over a mass live verification session (77 API checks + 9 browser tester personas + llama.cpp live bands; zero product defects; the honest OPEN rows named)"
git push
```

Delta-архив: `canonsim_iter-308-acceptmatrix_2026-10-03.zip`
(BASE_COMMIT `3e177b3…`, изменённые пути — ровно 5, создан
`docs/iterations/iter-308-acceptmatrix-report.md`, удалений нет),
приложен к сессии + прямая ссылка и md5 в чате.
