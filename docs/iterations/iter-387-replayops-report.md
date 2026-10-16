# iter-387 · replayops — семейство execution.get/replay посажено живьём: приложная половина строки replay-UI (условие матрицы приёмки перевёрнуто)

**Класс риска:** R4 (публичный API — две новые операции гейтвея;
D-260 с компактной PCC-записью, AGENTS §2.9; DECISIONS 34/35 —
слот запаса цел).

**Вызов владельца:** стоящая директива «продолжай работы, открывай
то что сейчас важнее всего сделать, логичнее и качественнее на
долгосрок. я разрешаю» над порядком стоящих вызовов STATUS Next
(прецедент iter-384: общая делегация = ПЕРВЫЙ вызов). Порядок
называл: станционный прогон hroom (проверен НЕосуществимым в
песочнице: Gemma-4-E4B Q4_K_M — 5+ ГБ, 720 тензоров, против 3.6 ГБ
доступной RAM и без GPU; станционная форма остаётся станции
владельца, RTX 3080 Ti + 32 ГБ), затем эстетическая половина
H-базиса (исключительно вызов владельца), затем — ПЕРВОЙ среди
отвечаемых работой — строка replay-UI NOT-EXPOSED. Открыта её
приложная половина: условие матрицы приёмки iter-308 «when
application supports replay» — семейство `execution.get/replay`
закона приложения §8, статус `[CONTRACT]` с момента wb-4.

## A. Что сделано

### A.1 Реестр исполнений — линейно-осведомлённый допуск

`ExecutionRegistry.admit(..., replay_of=None)` (keyword-only
параметр): при установленной ссылке деривация identity расширяется
`replay_of` + `replay_sequence` (счёт уже допущенных повторов ЭТОГО
оригинала), оба — ПОД замком реестра, вместе с проверкой
существования оригинала, вставкой и dup-проверкой: два гонящихся
повтора одного оригинала выводят РАЗЛИЧНЫЕ identity (последователь
ности 0 и 1), никогда не сталкиваются на dup-raise. Исходная
(безповторная) деривация не тронута — байт-идентична каждому
существующему вызывающему (все прежние места допуска не менялись).
`_ExecutionRecord.replay_of` живёт с допуска (читается ДО
терминального артефакта); терминальное закрытие передаёт её в
`ExecutionArtifact.freeze` — поле `replay_of` жило в артефакте с
wb-3 (§10), теперь оно НАСЕЛЯЕТСЯ. Новое чтение `lineage(
execution_id, session_id)` — ссылка + сортированные прямые дети,
под законом владения сессией (собственная сессия — свой реестр).

### A.2 execution.get — чтение провенанса

Семейство исполнения отвечает СВОИМ документом: родословная
(`replay_of` + `replays` — прямые дети), замороженные входы,
request_digest, закрытый артефакт, состояние/терминальность.
НАМЕРЕННО не поле run.get: чтение жизненного цикла (состояние/
прогресс/дедлайн) и чтение провенанса (родословная/заморозка/
артефакт) — заботы РАЗНЫХ семейств (§8 развели их сам); строгая
схема run.get фронтенда (strictObject) не тронута — обратная
совместимость по построению. Родословная читается с допуска — до
существования артефакта (закон A.1).

### A.3 execution.replay — допуск повтора

Честные гейты по порядку: закрытый сет аргументов (`execution_id`);
несуществующий оригинал; владение сессией (гейт реестра);
ТОЛЬКО терминальный оригинал (полётный отвергается громко — его
исход ещё не истина); воспроизводимость ВИДА (карта адаптеров);
замороженный конверт обязан нести `deadline_seconds` (закон фриза
допуска) — бюджет переносится и переразрешается через ТОТ ЖЕ закон
потолка §12. Замороженный материал валиден ПОСТРОЕНИЕМ (§10-фриз
произошёл при допуске оригинала) — повтор ПЕРЕЗАПУСКАЕТ, никогда
не перевалидирует. Допуск: `operation_id="execution.replay"` (истина
того, КТО допустил), `work_kind` оригинала (истина того, ЧТО
запускается), `replay_of=оригинал`; запуск; один эффект
`RUN_REPLAYED` (execution_id/work/replay_of) в упорядоченный поток
сессии; ответ — новая identity + `replayed_from` + переносный
бюджет + состояние STARTING.

### A.4 Адаптеры повтора — анфриз у хозяина фриза

Карта адаптеров собирается композицией: каждый вид run.start
пары-нативен ПО ПОДПИСИ (`WorkKind.work(ctx, pairs)`) — адаптер
снимает два зарезервированных ключа конверта (`work`,
`deadline_seconds`) с гейтом целостности (ключ `work` обязан
равняться имени вида — теневое перекрытие ловится ГРОМКО);
`chat.completion` — `chat_replay_work(port, frozen)` в backend.py:
модуль, который ФРИЗИТ, хозяин и АНФРИЗА (никогда вторая истина
над форматом) — JSON сообщений, repr температуры (точный
round-trip питоновского float), строка max_tokens; температура
едет как ЯВНАЯ запрошенная — пара провенанса повтора схлопывается
в requested == effective (честная форма перезапуска: повтор
воспроизводит ЭФФЕКТИВНЫЙ материал; исходное различие
REQUESTED-vs-EFFECTIVE остаётся записанным на документе самого
оригинала). Живо-гейтовые вида (`model.load`/`model.unload`)
в карту НЕ входят: их лестница ходит живое состояние, которое
повтор не имеет права обойти — их перевыпуск есть явный вызов
пользователя (DOMAIN_REJECTED с причиной и списком воспроизводимых).

### A.5 Гейт словаря конверта — у самого владельца

`run.start` отвергает вид, чьи собственные пары аргументов
затирают зарезервированные ключи конверта (`work`,
`deadline_seconds`) — ГРОМКО, при допуске ОРИГИНАЛА (закон
словаря конверта; корректность съёма адаптера A.4 стоит на нём).
Латентный класс закрыт у владельца, не потребителем.

### A.6 Идемпотентность и события

`execution.replay` — мутация: повторный вызов с тем же
`client_request_id` отвечает ЗАПИСАННЫЙ исход (duplicate=True,
результат равен, работа НИКОГДА не перезапускается — §12.2);
конфликтующее переиспользование — DUPLICATE_REQUEST. Эффект
`RUN_REPLAYED` садится в упорядоченный поток ОДИН раз (одно
допущение — один эффект — одно событие; retry второго события не
добавляет). Нагрузка эффекта — открытая запись (фронтенд-валидатор
payload — z.record, новое имя эффекта совместимо по построению).

## B. Верификация (+8 законов, tests/test_execops.py — новый)

1. **Закон новой идентичности**: тот же замороженный материал
   (request_digest РАВЕН — одна идентичность запроса, много
   исполнений) допускается сколько угодно повторов, каждый — своя
   identity; второй повтор оригинала отличен (последовательность);
   повтор повтора цепочкой (внук ссылается на сына, не на деда).
2. **Закон родословной**: артефакт повтора несёт replay_of,
   оригинала — None; execution.get отвечает ссылку + сортированных
   прямых детей; run.get остаётся чтением жизненного цикла (поля
   родословной на нём НЕТ).
3. **Честные гейты**: закрытый сет; не-строка; несуществующий;
   чужая сессия; полётный оригинал («still in flight»);
   невоспроизводимый вид (реальный прогон model.load →
   «not replayable» с видом в причине).
4. **Закон работы (рука run.start)**: проба-счётчик растёт ровно
   на число повторов; детерминированная проба отвечает равный
   результат; переносный бюджет равен замороженному.
5. **Закон работы (чат-рука — ДАТУМ ВОСПРОИЗВОДИМОСТИ)**: порт
   вызван повторно с ТЕМ ЖЕ messages/temperature/max_tokens
   (свидетельство — записанные вызова дубля порта); ответ завершён;
   пара провенанса схлопнута (requested == effective); артефакт
   несёт replay_of и operation_id «execution.replay».
6. **Закон идемпотентности**: retry тем же ключом — записанный
   исход (duplicate=True, результат равен, счётчик пробы НЕ
   двинулся); конфликт ключа — DUPLICATE_REQUEST.
7. **Закон события**: ровно ОДИН RUN_REPLAYED в упорядоченном
   потоке (нагрузка: identity/вид/ссылка), последовательности
   возрастают; retry второго события не добавляет.
8. **Закон словаря конверта**: вид, замораживающий собственный
   ключ `work`, отвергается при допуске ОРИГИНАЛА (run.start) —
   «reserved envelope key(s) ['work']».

Полный прогон: **2684 passed + 27 failed + 1 skipped** (27 —
известный T1 env-набор: счёт и семейство идентичны задокументированному
базлайну iter-386 — изменение слоя workbench, нуль канон-байтов;
+8 законов зелёные). `ruff check .` чист; `docguard` чист (TASKS
после круфт-паса 599/600 — сжаты density-1/wb-2..wb-12/m4-r,
измеренные лестницы у своих отчётов); `topology --check` чист
(три строки манифеста синхронизированы); `digest` парсит.
Фронтенд (райдеры зеркала реестра, нуль строк исходника):
**256 vitest + tsc + build зелёные** (фикстура состава + пин
счётчика About 21→23). INV-1..5 не тронуты (INV-4: нулевая новая
сетевая поверхность — операции едут санкционированным
бес-сокетным гейтвеем; G2: реестр остаётся в-памяти, lineage живёт
с процессом — строки персистентности владеют долговечной половиной).

## C. Изменённые пути (15: 1 создан + 14 изменено)

workbench/application/operations/execution.py; workbench/application/
operations/backend.py; workbench/application/operations/composition.py;
tests/test_execops.py (новый); tests/test_operations.py;
tests/test_backend_row.py; frontend/tests/fixtures/app_status_
composition.json; frontend/tests/integration/Settings.test.tsx;
docs/WORKBENCH_APP_LAW.md; docs/SSI_TOPOLOGY.md; docs/DECISIONS.md
(D-260, 34/35); STATUS.md; worklog.md (iter-377 вытеснен);
docs/TASKS.md (строка replayui-1 + леджер, iter-377 вытеснен +
круфт-пас); docs/iterations/iter-387-replayops-report.md (новый).
Превышение soft-капа §2.3 (3–5): код + законы + обязательные
синхронные райдеры (пины реестра, зеркало фронтенда, четыре
законодательных документа, три документа состояния) — объём
отмечен.

## D. Риски

- **UI-экспозиция — остаток строки**: матрица приёмки несёт
  NOT-EXPOSED до посадки аффорданса повтора на поверхности
  (терминальный ход чата / ран Models) + зеркала
  contracts/validators/client. Приложная половина самодостаточна
  (CLI/гейтвей-потребитель), но строка закрывается только
  экспозицией — честно записано в STATUS Next.
- **Пары-нативные виды — форматное знание**: адаптер чата
  знает формат фриза (три ключа); знание живёт У ХОЗЯИНА фриза
  (backend.py), но добавление поля в фриз chat.send потребует
  синхронного анфриза — закон одного владельца соблюдён, риск
  дрейфа закрыт колокацией.
- **G2 (в-памяти реестр)**: родословная умирает с процессом —
  столько же, сколько и сам реестр (wb-5 честная форма); долговечная
  родословная — строка персистентности, не этой итерации.
- **Расширение identity-деривации**: повторы выводят отличные
  identity от оригинала ПО ПОСТРОЕНИЮ (operation_id «execution.
  replay» + линейные поля) — столкновение с исходной деривацией
  невозможно; вторая деривация того же повтора того же оригинала
  невозможна без удаления первой (в-памяти — не бывает).

## E. Дальше

Первая отвечаемая позиция — UI-экспозиция строки replay-UI
(аффорданс на терминальном ходе + зеркало клиента; каждый ряд —
вызов владельца по FRONTEND_UIUX_LAW §25, стоящая директива
покрывает). Затем порядок владельца: станционный прогон hroom
(Gemma-4-E4B — станция владельца), W8, P1/P2/P3, lab-composite-1
(головы ждут потребителей). Новая строка производительности —
только по свежему непрофилированному A/B-датуму.

## F. Git-блок владельца

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add workbench/application/operations/execution.py workbench/application/operations/backend.py workbench/application/operations/composition.py tests/test_execops.py tests/test_operations.py tests/test_backend_row.py frontend/tests/fixtures/app_status_composition.json frontend/tests/integration/Settings.test.tsx docs/WORKBENCH_APP_LAW.md docs/SSI_TOPOLOGY.md docs/DECISIONS.md STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-387-replayops-report.md
git status --short
git commit -m "iter-387-replayops: THE EXECUTION FAMILY LANDED (the replay-UI row's app half, R4, D-260 PCC) - the app law §8's execution.get/replay [CONTRACT]->[LANDED]: the registry's lineage-aware admission (replay_of on the record from admission, the per-original sequence in the identity derivation UNDER the lock - racing replays derive distinct identities, the original derivation untouched), the lineage read, the artifact link at the terminal close; execution.get the PROVENANCE read (lineage + the direct children + the frozen inputs + the closed artifact, readable from admission - never a run.get field, the lifecycle/provenance family split keeping the frontend's strict run.get schema untouched); execution.replay §10's admission with the honest gates (closed set, session ownership, TERMINAL-only, kind replayability, the carried deadline re-resolved through the same ceiling law; the frozen material post-validation by construction - the replay RE-RUNS, never re-validates); the replay adapters (run.start kinds pairs-native; chat.completion over the freeze owner's own unfreeze - backend.py, never a second truth over the format; the live-gate kinds model.load/unload own their re-dispatch) + run.start's reserved-envelope-keys gate at the owner + the RUN_REPLAYED stream effect; +8 laws (tests/test_execops.py) - the chat arm carrying the inference-reproducibility datum: the port re-called with the SAME frozen messages/temperature/max_tokens, the provenance pair collapsing to requested == effective; the acceptance matrix's condition 'when application supports replay' FLIPPED SATISFIED - the UI exposure the row's explicit remainder; the registry pins + the frontend mirror synced (21->23 registered, zero frontend source); the topology manifest's three rows; 2684 passed + 27 failed (the known T1 env set identical to the documented baseline, zero canon bytes), ruff+docguard+topology+digest clean, the frontend 256 vitest + tsc + build green; INV-1..5 untouched"
git push
```
