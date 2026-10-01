# Отчёт итерации iter-299 — frontendweb: INFERENCE ENTRY
(Phase 3, пятый ряд: воркспейс семантического управления генерацией
над существующими inference.read/inference.update; Inference в рейле
сразу за Chat)

Вызов владельца: «продолжай работу над фронтендом» — делегированный
вызов того же класса, что открыл iter-294..298 (D-198 intake). Ряд
выбран по собственному порядку следующих рядов STATUS («the next
frontend rows the owner's call: the Inference surface (the control
workspace — inf-2's regions), the Models surface…» — Inference
назван первым). Класс риска: R2 (frontend-local; ноль Python, ноль
canon, INV-1..5 не тронуты, LOG нетронут). BASE_COMMIT `bbd92de`.

## A. Что высажено (21 кодовый/тестовый путь + 6 доковых — один
когерентный минимальный срез, сверх мягкого лимита 3–5, освоено в
worklog)

- **Контракт-зеркало** (`frontend/src/api/gateway/
  {contracts,validators,client}.ts`) — ДВЕ существующие операции,
  ни одного нового маршрута (§3), глубина на один уровень глубже
  компактного среза Chat:
  - закрытые словари, зеркалящие СВОИХ владельцев на Python:
    INFERENCE_STATES (10 состояний резолвера —
    `resolver.py`'s STATES), INFERENCE_KINDS (5 видов — закон §3),
    INFERENCE_VALUE_TYPES (6 типов — `library.py`), INFERENCE_SCOPES
    (3 скоупа — закон §5);
  - документ котрола — 19 полей СТРОГО по собственному полю набору
    резолвера (`resolve()`'s control_document): идентичность
    (id/name/category/kind/scope/flag/field), метаданные редакторов
    (value_doc/value_type/forms/minimum/maximum/step/advanced),
    состояние (state/reasons/source), лестница §4 (baseline/
    upstream_default), заметки; `value`/`baseline`/
    `upstream_default` остаются `z.unknown()` — формы значений
    есть ДАННЫЕ бэкенда (закон data-driven §21.2: «UI никогда не
    перекодирует словарь»);
  - документ цепи (9 членов: id/name/enabled/order/value/state/
    reasons), пресета (id/name/description/values — values loose:
    словарь полей бэкенда), категории (id + честный счёт);
  - документ воркспейса — loose на НЕпотребляемой глубине
    (сырой `profile`-словарь значений, `request_layer`), закрытый
    на потребляемой; проекция `projectInferenceDocument` на шве
    снимает члены поимённо — index-сигнатура не попадает в
    поверхности;
  - `inferenceUpdate` — закрытый частичный документ стора
    (`name`/`sampler_chain`/`pinned`/поля значений; отсутствующие
    поля неизменны): на провод едут ТОЛЬКО изменённые ключи,
    свежий `client_request_id` на каждую явную попытку (G4).
- **Хук** (`frontend/src/features/inference/useInference.ts`
  (новый)) — состояние воркспейса:
  - чтение на монтирование + явный re-read (без поллинга — профиль
    не меняется под читателем, честный закон next-spawn);
  - черновик = REQUEST (имя + значения-дельта + ЦЕЛАЯ 9-членная
    цепь): маркер dirty, никогда не утверждение эффективного
    состояния; Set invalidFields — редактор с нелегальным явным
    значением дизейблит Save (честно, без клампа);
  - Save: дельта (изменённые ключи значений + имя + ЦЕЛАЯ цепь при
    изменении членства); на ACCEPTED возвращённый документ — новая
    OBSERVED-база, черновик примиряется к ответу СЕРВЕРА (запрет
    `input.value === EFFECTIVE` фальсифицирован: ответ несёт top_k
    20, который клиент не редактировал — ответ сервера побеждает
    локальную проекцию);
  - applyPreset: ПРОСТОЙ update со значениями пресета ДОСЛОВНО
    (§14: никогда не непрозрачный режим), сторожed на ЧИСТОМ
    черновике (§21.2: пресет никогда молча не модифицирует
    внеобластные настройки);
  - togglePinned: СВОЯ диспетчеризация списка pinned целиком
    (порядок сохранён) — секция workspace, никогда правка профиля:
    reconcileDraft=false, черновик профиля не тронут;
  - четыре честных лейна на каждую диспетчеризацию (UPDATED/
    REJECTED/TRANSPORT/MISMATCH), G4: никакого авто-ретрая,
    черновик сохранён при любом отказе.
- **Поверхность** (`frontend/src/features/inference/Inference.tsx`
  (новый)) — регионы §21.2 (каждый строится НА прочитанном
  документе: офлайн-поверхность честно пуста):
  - **пресет-ряд** — ПРОЗРАЧНЫЙ diff-превью ДО применения (каждое
    поле, которое применённый пресет изменил бы, старое → новое;
    сравнение по controls-значениям — валидируемая глубина), сам
    apply — простое обновление со сторожем чистого черновика;
  - **поиск** по имени/флагу/категории (§32 match families):
    совпадение — ЯВНЫЙ запрос, оно показывает и advanced-ряды;
    очищенный поиск восстанавливает Disclosure-состояния; NO MATCH —
    свой честный стейт (никогда пустота);
  - **закреплённая полоса** — чипы-REVEALS (открыть категорию +
    подсветить ряд), никогда вторые редакторы; pin/unpin — своя
    диспетчеризация;
  - **сворачиваемые категории** с честными счётами (N/M — видимые/
    всего): шесть general-chat семейств открыты по умолчанию
    (model/device/memory/moe/sampling/chat — §15); семейство, где
    ВСЕ контролы на advanced-рунге (cpu), открывается с честной
    заметкой — никогда беззвучный пробел;
  - **advanced-рунг** — чекбокс эксперта;
  - **цепь сэмплеров** — упорядоченный first-class объект: 9 членов
    в порядке рантайма, членство — DRAFT-правка (Save несёт ЦЕЛЫЙ
    документ), OBSERVED-состояние каждого члена + причины резолвера
    дословно; порядок — прочитанный порядок рантайма (переупорядо-
    чивание — будущий ряд, сказано в примечании);
  - **компилированный превью** — технический артефакт, только-
    чтение, за собственной disclosure (никогда не язык авторинга);
  - **редакторы DATA-DRIVEN** по собственным метаданным документа
    (value_type/forms/limits): int/float → number (min/max/step),
    bool → checkbox, enum → select по формам контроля, text → text,
    gpu_layers → композит auto/all/explicit+счётчик ('explicit' —
    UI-локальный режим, коммит — форма рантайма); новый контроль
    приземляется документом сервера один (словарь не перекодирован);
  - **ряд котрола**: имя (первичное) + флаг (сырой маппинг) +
    state-чип (закрытый словарь резолвера как STATE-class токены —
    ЭФФЕКТ→accent, AUTO→config, INACTIVE→muted, INEFFECTIVE→warn,
    CONFLICT→error; ноль сырых литералов вне :root) + маркер DRAFT +
    pin-аффорданс; строка value_doc + лестница §4 (baseline ·
    upstream бок о бок); причины резолвера ДОСЛОВНО под рядом
    (§7: сконфигурированный-но-неэффективный ВИДИМ — Mirostat
    INACTIVE с собственной причиной закреплён тестом);
  - стрип: имя профиля (редактируемый черновик) · applies
    next-spawn · managed · цепь · deterministic · маркер dirty ·
    no-session.
- **Маршрут**: Inference в рейле сразу за Chat (AI-семейство
  смежно: converse → управлять генерацией) — §2.1 каноничное
  IA-дерево ПОПРАВЛЕНО (закон-владелец синхронизирован; Settings ≠
  Inference — раскол inf-1 держится: воркспейс — свой ряд, никогда
  подсекция Settings).

## B. Законы, которые несёт ряд

- **§21.2 (UIUX) + LLAMA_CPP_INFERENCE_CONTROL_LAW целиком**:
  Inference — воркспейс семантического управления генерацией;
  Chat несёт только компактную проекцию + ссылку; полная глубина
  контрола живёт ЗДЕСЬ. Регионы inf-2: пресеты (прозрачный diff,
  никогда непрозрачный режим), поиск (имя/флаг/категория),
  закреплённая полоса (reveal'ы), сворачиваемые категории
  (прогрессивное раскрытие — никогда плоская стена из 85 котроло-
  в), advanced-рунг; редакторы data-driven НА прочитанном
  документе.
- **§4 лестница дефолтов**: upstream default ≠ project baseline ≠
  профиль-значение ≠ эффективное ≠ наблюдаемое — оба (baseline ·
  upstream) едут рядом в каждом ряду, никогда молча не сверяются.
- **§7 словарь эффективных состояний**: EFFECTIVE/AUTO/INACTIVE/
  INEFFECTIVE/… — состояние и причина от резолвера, дословно;
  сконфигурированный-но-неэффективный контроль ОСТАЁТСЯ видимым.
- **§8 замыкание**: REQUESTED (черновик) → ACCEPTED (проверка
  стора) → EFFECTIVE (следующий managed-spawn, applies:
  next-spawn дословно; LIVE-сервер держит свои флаги — заметка
  дословно) → OBSERVED (возвращённый документ + скомпилированный
  превью) → PRESENTED (этой поверхностью). Запрещённые коллапсы
  названы и фальсифицированы тестами.
- **§11 цепь**: упорядоченный first-class объект; членство и
  значение — РАЗНЫЕ заботы; правка — ЦЕЛЫЙ документ (частичная
  правка отклоняется store'ом громко — захвачено фикстурой и
  закреплено контрактом).
- **§14 пресеты/пины**: пресет — прозрачная стартовая точка,
  применение — простое обновление; закрепления — секция workspace
  профиля (один файл, две именованные секции — никогда второй
  стор).
- **G4**: никакого авто-ретрая; свежий ключ идемпотентности на
  каждую явную попытку; TRANSPORT после отправки = UNKNOWN, черновик
  сохранён, примирение — явный re-read пользователя.
- **INV-4 не тронут**: браузер — клиент гейтвея над существующим
  loopback-биндингом; никаких новых сетевых поверхностей, ноль
  Python.

## C. §27 transfer records (метод D-246 — донор информирует, закон
CanonSim решает)

1. **Донор: удалённый Redot-воркспейс inf-2** (`git show
   4a1eb8c:workbench/presentation/redot/scripts/inference.gd`,
   история — D-245):
   - НАБЛЮДЕНИЕ: DEFAULT_OPEN_CATEGORIES = [model, device, memory,
     moe, sampling, chat] — «шесть категорий, с которыми новый
     воркспейс открывается; каждое другое семейство — в одном
     disclosure-клике (никогда плоская стена из 85 котролов)»;
     поиск — подстрока без учёта регистра по имени/флагу/категории;
     пресет-diff — «каждое поле, которое пресет изменил бы, старое
     → новое, превью ДО применения»; закреплённые чипы —
     «one-click REVEAL своего контроля, никогда второй редактор»;
     apply пресета — «PLAIN update payload».
   - МЕХАНИЗМ: прогрессивное раскрытие по явным спискам + фильтры,
     производные от прочитанного документа; перенесено всё
     выше-названное.
   - ГРАНИЦА ПЕРЕНОСА: движок/сцены Godot, тема, `_tr`-локализация,
     SpinBox/OptionButton-виджеты — НЕ переносятся; фокус веб-ряда —
     те же законы в DOM.
   - ИНВАРИАНТ: INV-4 (браузер — никогда четвёртая сетевая
     поверхность), data-driven (§21.2).
   - ФАЛЬСИФИКАТОР: шесть дефолтно-открытых семейств рендерятся, а
     закрытые нет, до клика — закреплён integration-тестом.
   - ДИСПОЗИЦИЯ: KEEP.
2. **Донор: собственный Settings-ряд iter-296** (прецедент веб-
   дерева): Send-ONLY-changed-keys, свежий ключ на попытку,
   примирение черновика к ответу сервера, applies: next-spawn
   дословно, заметка LIVE, без поллинга — один mount-READ.
   Перенесено как форма §8-замыкания над персистентным стором.
   ДИСПОЗИЦИЯ: KEEP (внутренний прецедент, не внешний донор —
   запись для полноты метода).

## D. Проверка

```
PYTHONHASHSEED=0 python -m pytest -q      → 2529 passed + 1 skipped (92.3s)
ruff check .                              → clean
python scripts/docguard.py                → clean (caps + state-layer)
python scripts/topology.py --check        → clean
frontend: npx tsc --noEmit                → clean
frontend: npx vitest run                  → 174 passed / 11 files (139 + 35)
frontend: npm run build                   → dist 13.66kB css / 411.99kB js
```

**Живой смок против ОБСЛУЖИВАЕМОЙ композиции** (реальные HTTP POST
по 127.0.0.1, `build_app` + `transport.start()`, throwaway-корни +
один фиктивный .gguf) — **11/11**:
- app.status OK;
- inference.read: полный документ — 85 котроло / 9 цепь / 4 пресета
  / 15 категорий;
- session.create OK;
- inference.update {temperature 0.55, top_p 0.9} → OK,
  возвращённый документ — новая база (temperature → 0.55);
- значение ПЕРСИСТИРОВАНО через повторное чтение (реальный
  round-trip стора);
- неизвестное поле → DOMAIN_REJECTED дословно («unknown field(s)
  ['not_a_field'] (closed set: …)»);
- частичная цепь (1 член) → DOMAIN_REJECTED дословно («is missing
  member(s) ['dry', 'min_p', 'penalties, …]» — закон целого
  документа);
- pinned [temperature, top_k] → OK (секция workspace);
- закрепления ПЕРСИСТИРОВАНЫ, значения профиля НЕ тронуты
  закреплением (0.55 жив);
- идемпотентный дубль (тот же client_request_id) → duplicate:
  true;
- персистентный профиль: schema canonsim.workbench.inference/1 +
  temperature 0.55 + top_p 0.9 + workspace.pinned — свидетельство
  файла.

**Фикстуры** (4 новые, parity-law byte form, захвачены с реальной
композиции in-process): inference_update_ok (частичное temperature
0.65 + top_k 20 приземлилось дословно), unknown_field, bad_type
(«temperature 'hot' must be a number in [0, 2]»), bad_chain.
manifest.json синхронизирован.

**Контрактные ряды** (20 новых): полный документ на потребляемой
глубине; метаданные котроло закрыты (gpu_layers: forms auto/all,
max 999); цепь 9 членов без дублей (penalties первый, temperature
последний); пресеты; закрытые словари (10/5/6/3); три лейна
отклонения дословно; фальсификаторы закрытого документа: чужой
kind/state/value_type, неизвестный член, нестроковая причина,
отрицательный порядок, пропажа цепи/deterministic, values-список,
нулевая категория, не-финитный step — все MISMATCH.

**Интеграционные ряды** (14 новых + 1 Shell): ровно ОДНО чтение на
монтирование без аргументов и сессии, никогда поллинг; шесть
дефолтно-открытых семейств рендерятся, закрытые — нет до клика;
полностью-advanced семейство открывается с честной заметкой;
состояние OBSERVED в каждом ряду (Mirostat INACTIVE с причиной
дословно); data-driven редакторы (number с min/max/step, select по
формам, gpu-комозит, текст, цепь 9); advanced-рунг + поиск (флаг
top-k матчится, semantic-id — нет: три §32-семейства, не четвёртое);
NO MATCH отличен; §8-замыкание (маркер DRAFT → Save ТОЛЬКО дельта
{temperature: 0.65} со свежим ключом → баннер замыкания → примирение
к ответу сервера: top_k становится 20 без правки клиента); нелегаль-
ный ввод дизейблит Save и восстанавливается; цепь — WHOLE-документ
на проводе (min_p: false среди 9); пресет — прозрачный diff до
применения + значения дословно ({temperature: 0}) + примирение;
пресет сторожен на чистом черновике; пин — своя диспетчеризация
{pinned: […]}, чип-релью-markер; REJECTED дословно с сохранённым
черновиком, ноль авто-ретрая; без сессии все мутации честно
дизейблены при работающем чтении; TRANSPORT с UNKNOWN-заметкой.

## E. Границы / следующий шаг

- **Владелец-сайд для полного живого бенда**: скомпилированный
  превью отражает реальную композицию уже сейчас; «managed LIVE +
  заметка» требует загруженной модели (ряд поверхности Models).
  Доступный в этой среде бенд закрыт ПОЛНОСТЬЮ: персистентный стор
  round-trip'ает без llama-server (в отличие от Chat, у которого
  COMPLETED-бенд владельца).
- Следующие ряды фронтенда — вызов владельца: поверхность
  **Models** (load/unload/import — оставшееся зеркало семейства;
  открывает managed-LIVE бенд для Settings/Inference/Chat),
  вторичная навигация Settings, streaming admission (SSE — сначала
  контракт gateway), acceptance matrix, коллапс DECISIONS.
- Отложено этим рядом (названо, не молча): переупорядочивание цепи
  в UI (порядок рантайма читается; правка — будущий ряд), модель-
  driven контекстная осведомлённость §15 (нужны факты загруженной
  модели — ряд Models), недавние/частые ранжирования, custom-preset
  персистентность — уже строки TASKS.

## F. Риски

- Черновик умирает с поверхностью (переключение вкладки рейла
  теряет несохранённые правки) — волатильность presentation-state
  по закону §7, как у каждой поверхности; стор — истина, повторное
  чтение явно.
- Два источника правок профиля (вкладка A и вкладка B): каждая
  вкладка — независимый клиент; «последняя принятая правка
  побеждает» в сторе, черновики расходятся с observed в `dirty` —
  расхождение это факт представления, примирение явное (re-read),
  никогда молчаливое.
- 85 котролов рендерятся без виртуализации: ~60 рядов видимо в
  дефолтных шести семействах (порог закона — 10³+, порядок
  ниже; virtualization — если семейства когда-нибудь превысят).
- Loose-глубина документа (profile/request_layer) не валидируется
  — гибкость по закону data-driven; потребляемая глубина закрыта и
  покрыта (пропажа члена — MISMATCH, тесты).
- Compiles-preview длинный: за disclosure по умолчанию (§13 —
  технический артефакт, не язык авторинга).

## G. Owner-side Git Bash (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/api/gateway/contracts.ts frontend/src/api/gateway/validators.ts frontend/src/api/gateway/client.ts frontend/src/features/inference/useInference.ts frontend/src/features/inference/Inference.tsx frontend/src/app/composition/App.tsx frontend/src/app/composition/styles.css frontend/tests/fixtures/inference_update_ok.json frontend/tests/fixtures/inference_update_unknown_field.json frontend/tests/fixtures/inference_update_bad_type.json frontend/tests/fixtures/inference_update_bad_chain.json frontend/tests/fixtures/manifest.json frontend/tests/contract/validators.test.ts frontend/tests/integration/Inference.test.tsx frontend/tests/integration/Shell.test.tsx frontend/README.md docs/FRONTEND_UIUX_LAW.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-299-frontendweb-report.md
git status --short
git commit -m "iter-299-inference: Phase 3 row 5 — the Inference entry over the profile store (the §21.2 workspace, the data-driven editors, Inference behind Chat)"
git push
```

Delta-архив: `canonsim_iter-299-inference_2026-10-01.zip`
(BASE_COMMIT `bbd92de…`, изменённые/созданные пути — ровно 22
(14 изменённых + 8 созданных), удалений нет), приложен к сессии +
прямая ссылка и md5 в чате.
