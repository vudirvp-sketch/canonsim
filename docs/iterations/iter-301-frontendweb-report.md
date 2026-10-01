# Отчёт итерации iter-301 — frontendweb: SETTINGS SECONDARY NAV
(Phase 3, седьмой ряд: собственная вторичная навигация Settings —
Deployment | About, каждая секция над живым документом; внешний
IA-вердикт шаг 5, в реконсиляции с inf-1 по методу D-246)

Вызов владельца: «продолжай работу над фронтендом» — делегированный
вызов того же класса, что открыл iter-294..300 (D-198 intake). Ряд
выбран по собственному порядку следующих рядов STATUS («the next
frontend rows the owner's call: the Settings secondary nav, the
streaming admission…» — Settings secondary nav назван первым; отчёт
iter-297 назвал этот ряд вердикт-шагом 5, iter-298/299/300 повторяли
тот же порядок). Класс риска: R2 (frontend-local; ноль Python, ноль
canon, INV-1..5 не тронуты, LOG нетронут). BASE_COMMIT `075015f`.

## 0. Реконсиляция вердикта по методу D-246 (донор информирует,
закон решает)

Вердикт предлагал форму General / Deployment / Appearance / Advanced.
Наблюдение донора верно: Settings была единой плоской поверхностью
без группировки. Механизм донора переносим: вторичная навигация
группирует настройки по заботе, чтобы поверхность масштабировалась
без превращения в стену полей. Но состав секций решает закон:

| Секция вердикта | Реконсиляция | Обоснование |
|---|---|---|
| Deployment | KEEP | реальный документ: стор с тремя полями + скомпилированный предпросмотр + закон applies |
| General | RE-SCOPE → **About** | «General» подразумевал редактируемые общие настройки — их не существует (закрытый трёхпольный набор — закон стора, UI никогда не изобретает четвёртое поле); честное общее содержание, которое СУЩЕСТВУЕТ, — идентичность гейтвея (существующая session-free READ `app.status`), read-only |
| Appearance | BOUND (именованное ограничение) | нет персистентного стора внешнего вида; браузерное хранилище никогда не истина (R3-ряд стража); in-memory настройка умирает на remount (монтируется только активная поверхность); токен-система — закон дизайна (VISUAL_SYSTEM_UI), не пользовательская настройка. Никогда не сфабрикованная пустая секция |
| Advanced | DISSOLVE → Deployment | `extra_args` — сырой люк ТОГО ЖЕ документа; §19: уровни раскрытия — не семантические классы; один документ, один черновик, один Save с дельтой. Вынос одного поля в отдельную секцию — failure mode «feature directory» §2 |
| Inference/LLM | REJECT (inf-1) | отклонён ещё iter-297: generation-контроли — отдельная поверхность, никогда подраздел Settings; указатель рендерится в заголовке |

Ключевая честность: навигация из ОДНОЙ секции была бы feature
directory (собственный названный failure mode §2). About —
единственная честная вторая секция: существующая op, ноль новых
маршрутов, реальное содержание идентичности.

## A. Что высажено (6 кодовых/тестовых путей + 7 доковых — один
когерентный минимальный срез, в пределах мягкого лимита)

- **`frontend/src/features/settings/Settings.tsx`** — контейнер с
  вторичной навигацией:
  - нав-полоса «Settings sections» (прецедент Diagnostics:
    in-workspace табы, прецедент зеркалируется — `.section-tab`,
    активный таб с CONFIG-токеном, `aria-current="page"`,
    keyboard-native кнопки);
  - закрытый набор секций Deployment | About; активная секция —
    разрешённое локальное UI-состояние поверхности (§7), сброс на
    Deployment при remount (закон монтирования);
  - **владелец состояния — КОНТЕЙНЕР**: хук `useSettings` живёт
    здесь, секция Deployment — его проекция → черновик ПЕРЕЖИВАЕТ
    переключение секции (владелец черновика — ПОВЕРХНОСТЬ, не
    форм-секция); shell-переключение по-прежнему роняет всё
    (поверхность размонтируется — честная форма закона);
  - монтируется ТОЛЬКО активная секция; remounted About перечитывает
    свои доказательства; settings-чтение ОДНО на монтирование
    поверхности (переключения секций его никогда не повторяют);
  - заголовок несёт указатель inf-1 («Settings ≠ Inference Control»)
    с data-testid для пин-теста.
- **`frontend/src/features/settings/SettingsAbout.tsx`** (новый) —
  секция About: идентичность гейтвея read-only над СУЩЕСТВУЮЩЕЙ
  session-free `app.status` (ноль новых маршрутов):
  - одно чтение на монтирование + явный re-read (кнопка), без
    поллинга (идентичность construction-stable — parity law);
  - честные лейны NOT READ ≠ READING ≠ TRANSPORT ≠ MISMATCH ≠
    answered-but-not-OK (защитный fallback по прецеденту
    GatewayStatus; DOMAIN-REJECTED структурно недостижим через
    типизированный шов — app.status не несёт аргументов, названо в
    докстринге, никогда не сфабриковано тестом);
  - рендер дословно: service / contract / exposure / auth + полный
    реестр операций чипами с честным счётом;
  - граница против диагностики названа в примечании: probe-консоль —
    в Diagnostics (идентичность здесь, доказательство там); тот же
    наблюдённый документ, тот же владелец-op — не второй источник
    истины (прецедент: хедер Chat рендерит model.list, который
    рендерит и Models).
- **`frontend/src/app/composition/styles.css`** — `.settings-sections`
  / `.section-tab` / `.section-tab-active` (зеркало diag-паттерна;
  активный таб — CONFIG-токен канала) + `.settings-section`; ноль
  сырых литералов вне :root — V1-скан стража зелёный.
- **`frontend/tests/fixtures/app_status_composition.json`** (новый,
  живой захват) + **`manifest.json`** — ПОЛНЫЙ реестр 21 операции
  живой композиции (in-process parity form: build_app с throwaway
  корнями, ноль транспорта, ноль спавна бэкенда); счёт «21
  registered» пинится интеграционным рядом.
- **`frontend/tests/integration/Settings.test.tsx`** — 7 новых рядов
  (см. D).

## B. Законы, которые несёт ряд

- **§2.1 (поправка, D-247-дерево)**: вторичная навигация Settings —
  собственное дело поверхности; новая binding line: «A Settings
  section exists only over a live document (real content, never a
  placeholder); the draft's owner is the SURFACE — a section switch
  never drops the user's unsaved REQUEST».
- **inf-1 стоит**: generation-контроли — поверхность Inference,
  никогда подраздел Settings; указатель рендерится; тест пинирует
  отсутствие «Inference»/«Appearance» в нав-наборе секций.
- **§7 (явное разрешение)**: черновик — presentation state,
  принадлежащий ПОВЕРХНОСТИ; секции — проекции. Ограниченность:
  один документ + один черновик + одно чтение идентичности.
- **Закон монтирования**: только активная секция монтируется;
  remounted секция перечитывает доказательства (About перечитывает
  на каждый вход — пин-тест), переключение никогда не кэширует.
- **§3/§5 (INV-4 клиентское зеркало)**: ноль новых маршрутов; About
  диспатчит СУЩЕСТВУЮЩУЮ app.status через типизированный клиент;
  fetch остаётся только в транспортном адаптере (R1 стража).
- **G4**: никакой авто-ретрай; re-read — явное действие
  пользователя (кнопка), TRANSPORT рендерится с честной заметкой.
- **V1 (визуальный пол)**: цвета — только токены; активный таб —
  CONFIG-токен (STATE-класс канала, не второй интерактивный
  акцент).

## C. §27 transfer records (метод D-246)

1. **Донор: внешний IA-вердикт, шаг 5** (General/Deployment/
   Appearance/Advanced). НАБЛЮДЕНИЕ: Settings плоская, без
   группировки. МЕХАНИЗМ: вторичная навигация группирует по заботе.
   ГРАНИЦА ПЕРЕНОСА: состав секций решает закон CanonSim, не донор;
   лейблы — MAY VARY (envelope). АДАПТАЦИЯ: Deployment | About (см.
   §0-таблицу); Appearance → BOUND; Advanced → DISSOLVE. ФАЛЬСИФИКАТОР:
   секция без живого документа = feature directory; тесты пинируют
   закрытый набор из двух секций. ДИСПОЗИЦИЯ: MODIFY (механизм
   перенесён, состав пересобран по закону).
2. **Донор: собственный Diagnostics-паттерн iter-297** (внутренний
   прецедент): in-workspace вторичная навигация под приглушённым
   входом. МЕХАНИЗМ: таб-полоса + aria-current + монтирование
   только активного. ПЕРЕНОС: зеркалирован для Settings (тот же
   паттерн, свои токены класса). ГРАНИЦА: Diagnostics-реестр —
   композиционный root-сплит; Settings-секции — внутреннее дело
   самой поверхности (§2.1), не реестр root'а. ДИСПОЗИЦИЯ: KEEP.
3. **Донор: отсутствующий — Appearance-стор** (внешняя рамка
   «настройки внешнего вида»). НАБЛЮДЕНИЕ: стора нет; R3-ряд стража
   банит браузерное хранилище как истину; in-memory умирает на
   remount. МЕХАНИЗМ не переносим в чистом вебе без четвёртой
   сетевой поверхности или нового backend-ряда. ГРАНИЦА: именованное
   ограничение (как нативный проводник импорта — Tauri-ряд);
   открытие Appearance-стора — будущий backend-ряд по вызову
   владельца, никогда молчаливая клиентская фабрикация.
   ДИСПОЗИЦИЯ: BOUND (задокументировано в §2.1-дереве + stage map).

## D. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped (92.5s)
ruff check .                              → clean
python scripts/docguard.py                → clean (caps + state-layer)
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 221 passed / 12 files (=214+7)
frontend: npm run build                   → dist 15.69kB css / 437.25kB js
```

**Живой смок против ОБСЛУЖИВАЕМОЙ композиции** (реальные HTTP POST
по 127.0.0.1:8765, `build_app` + `transport.start()`, throwaway-корни
+ один фиктивный .gguf, managed-бэкенд пробует свободный порт, спавна
нет — app.status/backend.settings бэкенд-порт не трогают) — **38/38**:

- app.status: OK + идентичность (service/contract/exposure LOOPBACK/
  auth false) + ПОЛНЫЙ реестр 21 операции, все ключевые имена
  проверены (chat.send, inference.*, model.*, observatory.*, run.*,
  session.*, backend.settings*);
- backend.settings: OK, defaults + applies next-spawn +
  command_preview + managed_live false;
- session.create OK; частичный update принят (no_webui false +
  extra_args "--verbose"), возвращённый документ — новая OBSERVED-база;
  PERSISTED settings.json на диске: schema canonsim.workbench.settings/2,
  значения дословно;
- unknown field → DOMAIN_REJECTED дословно («unknown field(s)
  ['llama_threads']»); bad type → DOMAIN_REJECTED дословно («must be
  a bool»);
- идемпотентный дубль (тот же client_request_id + материал) →
  duplicate: true; свежее чтение несёт принятые значения.

**Живой браузерный closure** (Vite dev server + proxy + headless
браузер; снимки приложены к сессии:
`iter-301-settings-deployment.png`, `iter-301-settings-about.png`,
`iter-301-settings-draft-survived.png`):

- Settings в рейле (pinned); вторичная навигация рендерится:
  [Deployment | About], Deployment активен по умолчанию;
- About: идентичность живой композиции (service, contract,
  LOOPBACK, «21 registered» + чипы операций) — проверено и снапшотом
  DOM, и VLM-описанием скриншота;
- **черновик переживает переключение секции**: правка no_webui →
  «DRAFT — unsaved changes» → About → Deployment → маркер ЧЕРНОВИКА
  НА МЕСТЕ (живой фальсификатор запрещённого коллапса);
- консоль: ноль ошибок.

**Интеграционные ряды** (7 новых): закрытый набор секций ровно
[Deployment, About] + Deployment по умолчанию + About отсутствует до
запроса + монтирование — только settings-чтение; переключение на
About — ОДНО чтение идентичности (без аргументов, без session) +
settings-документ НЕ перечитывается + идентичность дословно (21
registered, чипы) + форма Deployment размонтирована + без поллинга;
DRAFT ПЕРЕЖИВАЕТ переключение (маркер + чекбокс + вооружённый save +
ровно по одному чтению на op); remounted About перечитывает (2
чтения на 2 монтирования, счёт стабилен); TRANSPORT-лейн с честной
заметкой re-read, без авто-ретрая; MISMATCH-лейн (сфабрикованный
документ без service) — reported never coerced, идентичность не
отрендерена; inf-1 указатель рендерится + «Inference»/«Appearance»
никогда в нав-наборе.

**Мутационная проверка**: живой DRAFT-survival драйв (браузер) —
тот же запрет, что пинит тест: до правки контейнера переключение
секции роняло бы черновик (секция владела бы состоянием) — правка
контейнера это закрывает, тест + браузер фальсифицируют коллапс.

## E. Границы / следующий шаг

- **§5-чистка**: KI#109 УДАЛЁН (закрыт iter-294 — семь итераций
  спустя правила двух итераций; сущность проверена разрешённой на
  текущем HEAD зеркала: все 16 D-245-удалений на месте, архитектурный
  набор зелёный). Активных KI нет.
- **Appearance-стор не существует** — именованное ограничение
  (никогда не сфабрикованная секция); открытие — будущий backend-ряд
  по вызову владельца (нужен persisted-стор + op-семейство), никогда
  клиентская фабрикация.
- **DOMAIN-REJECTED для app.status структурно недостижим** через
  типизированный шов (op не принимает аргументов) — лейн есть как
  защитный fallback (прецедент GatewayStatus), тестом не
  сфабрикован — честная граница, названная в докстринге.
- Идентичность About — presentation того же наблюдённого документа,
  что рендерит и Gateway-диагностика: владелец факта — op бэкенда;
  дублирование презентации — прецедент (Chat-хедер vs Models).
- Следующие ряды фронтенда — вызов владельца: streaming admission
  (SSE — сначала контракт gateway), acceptance matrix, коллапс
  DECISIONS; каждый — своя итерация.
- Отложено этим рядом (названо, не молча): переиспользование
  таб-паттерна в общий `.secondary-nav`-класс (третий потребитель —
  ряд унификации, если появится; сейчас два параллельных
  паттерна-зеркала дешевле, чем трогать рабочую Diagnostics-поверхность).

## F. Риски

- Секция сбрасывается на Deployment при shell-переключении (remount
  поверхности) — закон монтирования, честная форма; если владельцу
  понадобится восстановление активной секции — отдельная строка
  (restoration — §2-требование к расширению навигации, сейчас
  состав фиксирован двумя секциями и сброс тривиален).
- About перечитывает идентичность на каждый вход в секцию — один
  POST, дешёво и честно (fresh evidence per mount); при появлении
  тяжёлой третьей секции паттерн пересмотреть.
- Две вкладки — два независимых клиента: черновик локален для
  вкладки (как и всё presentation state); расхождение черновиков —
  факт представления, reconciliation — Save/re-read пользователя.
- VLM-описание About-скриншота прочитало «canon.workbench_gateway»
  и «not requested» (оптическая интерпретация мелкого шрифта);
  DOM-снапшот и тесты пинируют точные строки —
  `canon_workbench_gateway@0.1`, «not required (loopback)».

## G. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/features/settings/Settings.tsx frontend/src/features/settings/SettingsAbout.tsx frontend/src/app/composition/styles.css frontend/tests/fixtures/app_status_composition.json frontend/tests/fixtures/manifest.json frontend/tests/integration/Settings.test.tsx frontend/README.md docs/FRONTEND_UIUX_LAW.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-301-frontendweb-report.md
git status --short
git commit -m "iter-301-settings-nav: Phase 3 row 7 — the Settings secondary nav (Deployment | About over live documents, the D-246 reconciliation, the draft owned by the surface)"
git push
```

Delta-архив: `canonsim_iter-301-settings-nav_2026-10-02.zip`
(BASE_COMMIT `075015f…`, изменённые/созданные пути — ровно 13
(10 изменённых + 3 созданных), удалений нет), приложен к сессии +
прямая ссылка и md5 в чате.
