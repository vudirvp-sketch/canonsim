# Отчёт итерации iter-306 — браузерный адаптер стрима
(FRONTEND_WEB_LAW §5, шаги 3+4 порядка допуска: EventSource за
типизированным клиентом + zod-валидаторы фреймов + политика
focused-tab)

Вызов владельца: «твоя задача сейчас продолжить работу по
фронтенду, например браузерный адаптер (шаг 3: EventSource за
типизированным клиентом + zod-валидаторы фреймов + политика
focused-tab)» — вызов открывает ровно те строки, которые STATUS
держал следующими в очереди фронтенда: «the browser stream adapter
(admission step 3) + the focused-tab budget policy (step 4, rides
3)». Класс риска: R2 (frontend-local, нулевой дифф Python; INV-4 не
тронут — браузер едет по САНКЦИОНИРОВАННОМУ iter-305 GET /events
биндингу, второго сетевого модуля не появилось). BASE_COMMIT
`7ce59ca`.

## A. Что было до (и почему ряд один, а не два)

Порядок допуска стриминга (FRONTEND_WEB_LAW §5) после iter-305:

```text
1. POST /op only (landed; S0)
2. explicit gateway contract + tests      ← iter-305 (бэкенд)
3. browser adapter behind the typed client ← ЭТОТ РЯД
4. focused-tab / budget policy in UI      ← едет с 3 (закон: rides 3)
```

Шаг 4 по закону едет СО шагом 3 — адаптер без политики бюджета
соединений нарушил бы сам смысл порядка допуска (N фоновых вкладок
× N стримов = исчерпание HTTP/1.1-бюджета — ровно то, от чего §5.3
защищает). Поэтому итерация = оба шага одной посадкой.

## B. Zod-валидаторы фреймов (validators.ts + contracts.ts)

Зеркало закрытого словаря провода: STREAM_CONTROL_FRAMES
(stream.open/rejected/overflow/close), STREAM_MODES
(REPLAY/RESYNC), STREAM_CLOSE_REASONS (SHUTDOWN) — контракты;
схемы — валидаторы, каждая СТРОГАЯ (неизвестный ключ/член =
CONTRACT_MISMATCH, никогда не пропуск):
- `streamOpenDocumentSchema` — дуальный ответ §13: union двух
  строгих рукавов (REPLAY {mode, session_id, last_sequence} |
  RESYNC + {resync, retained_from, snapshot} — снапшот той же
  sessionDocumentSchema, что и POST-ответ); рукава не
  валидируются друг другом (тест мутацией);
- `streamRejectedDocumentSchema` — вердикт по закрытому §8-словарю
  REJECTIONS + причина;
- `streamOverflowDocumentSchema` / `streamCloseDocumentSchema` —
  терминалы (close-причина по закрытому словарю).

Фреймы событий валидируются СУЩЕСТВУЮЩЕЙ eventEnvelopeSchema —
побайтовый паритет D4 означает: отдельной схемы быть не должно,
конверт один и тот же.

## C. Живые фикстуры провода (8 шт., сняты с настоящего гейтвея)

Захват скриптом вне репозитория (Правило 9 оператора) над НАСТОЯЩИМ
Gateway + LoopbackHttpTransport, чтение НАСТОЯЩИМ сокетом
(http.client, эфемерные порты): stream_open_replay,
stream_event_session_attached (паритет D4_ASSERTED ПРИ ЗАХВАТЕ —
байты фрейма == canonical_json реплея session.events),
stream_open_resync (retention_events=4), stream_overflow
(stream_buffer_events=1 + потребитель не читает сокет, пока 20 000
событий толкаются: буферы ОС заполняются, писатель блокируется,
очередь достигает потолка, наблюдаемый терминал следует за
дренированием — снят С ПРОВОДА), stream_close (живой стрим в
момент stop()), stream_rejected (неизвестная сессия — ОДИН фрейм
при HTTP 200), stream_bad_params (400), stream_auth_required (403
поверх конфига с креденциалом). Манифест дополнен провенансом.

## D. Адаптер (src/api/gateway/stream.ts — новый, ~370 строк)

`GatewayStream` — EventSource за швом типизированного клиента (R4:
импортирует только api-модули; R2 стража сужен: EventSource ТОЛЬКО
здесь — ровно как fetch в client.ts).

**Собственная реконнект-дисциплина — НЕ вкусовое решение, а закон
провода.** Документировано в модуле: браузерный auto-reconnect
ошибается ДВАЖДЫ против контракта iter-305: (а) он перезапрашивает
ТОТ ЖЕ URL — явный параметр since_sequence ПОБЕЖДАЕТ
Last-Event-ID («the explicit parameter wins»), и окно реплея
доставится ПОВТОРНО — дубликаты в хвосте; (б) семантический отказ
(stream.rejected + закрытие сервером) реконнектится в тот же
вердикт ВЕЧНО. Поэтому адаптер закрывает EventSource на КАЖДОМ
терминале/ошибе и пере-диалит сам: явный курсор в URL,
ограниченная лестница отката (500мс → удвоение → потолок 5с,
сброс на OPEN), одна связь, один таймер.

**Честный словарь фаз** (никогда не схлопнутый, §5.2): IDLE /
CONNECTING / OPEN / PAUSED / RESYNC / REJECTED / FAILED. Классы
не смешиваются: HTTP-уровневый отказ диала (readyState CLOSED —
EventSource статус-код не вскрывает, честная заметка с отсылкой к
devtools) = FAILED без ретрая; сетевая ошибка = собственный
bounded-ретрай; семантический вердикт = стоп, вердикт дословно,
явный рестарт — только решение вызывающего (дух G4); контрактное
несоответствие фрейма = FAILED с деталью.

**RESYNC-ответ**: адаптер эмитит документ и ЗАКРЫВАЕТСЯ —
потребитель владеет восстановлением (хук делает ТЕ ЖЕ один
POST-read из окна удержания, что и лейн поллинга, затем
пере-начинает стрим с выверенным курсором). Живой хвост
resync-стрима начинается с last_sequence+1 — продолжать его
означало бы дыру в буфере; закрытие — честный ход.

**Курсор**: sequence конверта (D4-паритет; проводной `id` —
бухгалтерия браузера, не наша). Курсор-вперёд-сервера
(REPLAY-open с last_sequence < курсора) сверяется в пользу
сервера — заметкой.

## E. Интеграция (useLiveTail — дуальный транспорт; Trajectory)

`useLiveTail` получил `transport: "stream" | "poll"` (по умолчанию
stream): ОБА лейна разделяют одну дисциплину курсора/буфера
(семантическая последовательность, bounded-буфер 50k, RESYNC-нотис,
freshness LIVE/STALE/DISCONNECTED). Политика focused-tab (шаг 4) в
стрим-лейне: связь держит ТОЛЬКО видимая+сфокусированная вкладка
(visibilitychange + focus/blur); фоновая вкладка НЕ ДЕРЖИТ НИЧЕГО
(STALE, last-known); одна связь на вкладку; переключение транспорта
сохраняет буфер (один мир доказательств, два транспорта). POST-лестница
поллинга — вечно-валидный фолбэк (селектор фида: stream / poll 1s/2s/5s
/ off); строка фазы стрима в стрипе поверхности; заметки транспорта
дословно.

## F. Тестовый пакет (+29 строк: 23 контрактных + 6 интеграционных)

- Слой 1 — валидаторы по живым фикстурам: валидации всех форм,
  мутации (чужой член/имя/причина = mismatch), непересечение рукавов
  дуала, закрытость словарей guard-ов.
- Слой 2 — законы адаптера (FakeEventSource — двойник в
  tests/helpers/, фейковые таймеры): диал правильного URL с явным
  курсором; ровно закрытый словарь слушателей; overflow → фрейм +
  закрытие + реконнект от ПОСЛЕДНЕГО полученного id через 500мс;
  close(SHUTDOWN) → реконнект с отходом; сетевая ошибка → источник
  закрыт НЕМЕДЛЕННО (анти-auto-reconnect) + собственный ретрай;
  лестница отката 500/1000/2000/4000/5000 + сброс на OPEN;
  HTTP-отказ → FAILED без ретрая; rejected → стоп навсегда, явный
  рестарт разрешён; mismatch → FAILED; RESYNC → фрейм + закрытие +
  фаза, собственного ретрая нет; setActive(false/true) → пауза без
  связи/таймера → пере-диал от курсора; терминалы под гейтом
  остаются; отсутствие EventSource в рантайме → честный FAILED.
- Слой 3 — интеграция Trajectory: стрим = дефолтный фид (URL
  since_sequence=0, фреймы рендерят строки, «stream OPEN»); blur →
  PAUSED/STALE + закрытие, focus → пере-диал от полученного
  курсора; rejected дословно без ретрая; overflow-нота + собственный
  реконнект; RESYNC → POST-восстановление заполняет окно
  удержания (since = retained_from-1) + пере-начало от
  last_sequence ответа; переключение stream→poll останавливает
  стрим и передаёт эстафету POST-лейну. 7 бывших poll-строк
  переприколоты к явному выбору poll-фида (смысл сохранён).

## G. Живая проверка (настоящий гейтвей + dev-сервер + настоящий браузер)

`python scripts/workbench_app.py --no-backend` (реестр 13 ops)
+ `GATEWAY_TARGET=… npm run dev` + headless Chromium:

1. **Стрим открыт через прокси Vite**: фаза «stream OPEN»,
   фрейм SESSION_CREATED в хвосте, ноль ошибок консоли.
2. **Живой push**: load probe «drive 50 ops» (127.2 ops/s) → 51
   событие ПРИШЛО СТРИМОМ без единого refresh — seq 51, rows 51,
   LIVE.
3. **Политика focused-tab**: уход на вторую вкладку и возврат —
   счёт диалов 1→2 (связь закрыта на фоне, пере-диал при возврате),
   rows 51 — ДУБЛИКАТОВ НЕТ (дисциплина явного курсора на живом
   проводе).
4. **Две вкладки = две независимые сессии** (6c3de3… и 6c6420…) —
   каждая со своим хвостом; сфокусированная держит связь.
5. **RESYNC end-to-end**: вкладка t1 поставлена на паузу (фон),
   300 attach-ops прокатаны ПРЯМЫМ POST мимо браузера (удержание
   256 прокатано за курсором 51) → возврат на t1: пере-диал
   попадает в out-of-retention → баннер RESYNC_REQUIRED → один
   POST-read заполняет окно → стрим пере-начат от seq 351:
   «seq 351 rows 307 (=51+256) LIVE stream OPEN».
6. **Переключение транспорта вживую**: stream→poll («poll on»,
   буфер цел) → stream обратно («stream OPEN»).
7. Ноль ошибок консоли/страницы на всём протяжении. Скриншоты:
   resync-recovery.png, live-stream-open.png,
   second-tab-independent.png, final-stream-open.png (доставка —
   архив сессии).

## H. Полный проверочный пакет

| Проверка | Результат |
|---|---|
| `pytest` (PYTHONHASHSEED=0) | **2555 passed + 1 skipped** (ноль диффов Python — неизменно) |
| `ruff check .` | clean |
| `python scripts/docguard.py` | clean (caps: worklog 10/10, TASKS-леджер 10/10) |
| `python scripts/topology.py --check` | clean (Python-карта не тронута) |
| `npm test` (vitest) | **251 passed** (было 222; +29, ничего не удалено/не ослаблено) |
| `npm run typecheck` | clean |
| `npm run build` | 1.59s |
| живое закрытие | §G (стрим/фокус/мультивкладка/RESYNC — всё над реальным гейтвеем) |

llama.cpp НЕ требовался ряду: стрим живёт на событиях операций
(attach-циклы load probe), LLM-бэнд закрыт живым ещё iter-302.

## I. Чего здесь НЕТ (границы ряда)

- **SharedWorker-транспорта** (§5.4: упаковочный общий транспорт
  требует СВОЕГО контракта гейтвея и тестов — никогда агентская
  импровизация).
- **WebSocket** (только под конкретную двунаправленную
  потребность), **HTTP/2/фан-аут** (только по измеренной
  потребности).
- **Ограничения, задокументированные честно**: EventSource не
  вскрывает HTTP-стatus/тело 4xx (заметка адаптера отсылает к
  devtools — на loopback-мире параметры конструируются, 403 —
  будущий authenticated-ряд); фрейм с именем ВНЕ закрытого словаря
  диспетчеризируется браузером в никуда (нет wildcard-слушателя) —
  закрытость словаря пришпилена контрактными тестами ОБЕИХ сторон.
- **Playwright-класс мульти-таб дым** — стоячий ряд тулинг-полa
  (адаптерная focused-tab-закон теперь исполняема там); CI-вiring
  — тот же стоячий ряд.

## J. Изменённые файлы

```text
frontend/src/api/gateway/contracts.ts     — фрейм-типы + закрытые словари
frontend/src/api/gateway/validators.ts    — zod-валидаторы фреймов
frontend/src/api/gateway/stream.ts        — NEW: адаптер (~370 строк)
frontend/src/features/trajectory/useLiveTail.ts — дуальный транспорт
frontend/src/features/trajectory/Trajectory.tsx  — фид-селектор + строка фазы
frontend/src/app/composition/styles.css   — одно токен-правило (.stream-phase)
frontend/tests/helpers/fakeEventSource.ts — NEW: тестовый двойник
frontend/tests/contract/stream.test.ts    — NEW, 23 строки
frontend/tests/integration/Trajectory.test.tsx — +6 строк стрим-лейна
frontend/tests/fixtures/stream_*.json ×8 + manifest.json — живой захват
frontend/tests/architecture/guard.test.ts — R2 сужен к санкционированному модулю
frontend/README.md                        — заметки стрима
docs/FRONTEND_WEB_LAW.md                  — §3-строка + §5 шаги 3+4 LANDED
docs/AGENT_NAVIGATION.md                  — §1 строка frontend/
docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md — stage map + границы §5
docs/TASKS.md                             — леджер (iter-296 выселен)
STATUS.md                                 — шапка + Next step
worklog.md                                — запись iter-306 (iter-296 выселен)
docs/iterations/iter-306-browserstream-report.md — этот отчёт
```

## K. Риски и откат

Риски: (а) новое поведение живого хвоста — смягчено дуальностью
транспорта (POST-лестница — вечно-валидный фолбэк, один клик
селектора) и 29 тест-строками; (б) собственная реконнект-логика —
документирована ЗАКОНОМ провода (две ошибки браузерного
auto-reconnect), лестница ограничена, терминалы без слепых ретраев;
(в) политику фокуса можно ужесточить/ослабить — она в ОДНОЙ точке
хука (derive), не размазана. Откат: git revert одного коммита
(нулевые миграции; фикстуры/тесты удаляются вместе с рядом).

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add frontend/src/api/gateway/contracts.ts frontend/src/api/gateway/validators.ts frontend/src/api/gateway/stream.ts frontend/src/features/trajectory/useLiveTail.ts frontend/src/features/trajectory/Trajectory.tsx frontend/src/app/composition/styles.css frontend/tests/helpers/fakeEventSource.ts frontend/tests/contract/stream.test.ts frontend/tests/integration/Trajectory.test.tsx frontend/tests/fixtures/stream_open_replay.json frontend/tests/fixtures/stream_open_resync.json frontend/tests/fixtures/stream_event_session_attached.json frontend/tests/fixtures/stream_overflow.json frontend/tests/fixtures/stream_close.json frontend/tests/fixtures/stream_rejected.json frontend/tests/fixtures/stream_bad_params.json frontend/tests/fixtures/stream_auth_required.json frontend/tests/fixtures/manifest.json frontend/tests/architecture/guard.test.ts frontend/README.md docs/FRONTEND_WEB_LAW.md docs/AGENT_NAVIGATION.md docs/frontendweb/FRONTEND_WEB_AGENT_CONTEXT.md docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-306-browserstream-report.md
git status --short
git commit -m "iter-306-browserstream: the browser stream adapter landed (admission steps 3+4 - the EventSource adapter behind the typed client, the zod frame validators, the focused-tab policy)"
git push
```
