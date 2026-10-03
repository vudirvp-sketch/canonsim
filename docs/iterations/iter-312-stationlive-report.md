# iter-312 · stationlive — живой station-ряд в песочнице

**Класс риска:** R0/R1 (verification-итерация: Substance — живая
сессия и её доказательства; дифф репо — документы + один
comment-only рефреш заметки адаптера; INV-1..5 не тронуты; LOG не
тронут; поведение движка не изменено ни на байт).

**Вызов владельца (2026-10-03, чат):** «дорабатывай прошлую итерацию
и делай что должно, разрешаю. мне нужно качество и отсутствие
костылей» + повторенный энаблер «можешь устанавливать llama.cpp для
работы и прочее окружение». По D-198 явный запрос владельца есть
текущая задача; энаблер — тот же, что в вызове iter-311, где он остался
неиспользованным («llama.cpp не устанавливался — R0 doc-only,
inference-ряд не открывался»). Эта итерация открывает отложенный ряд.

## A. Что сделано (окружение — документированным потоком)

- **llama.cpp b11337** (новейшая доступная ubuntu-x64 сборка; та же,
  что дропы iter-302/308) — в документированной drop-раскладке
  `workbench/runtime/llama.cpp/llama-b11337/` (gitignored, как требует
  закон). Проверено: `llama-server --version` → `0.5.0-dev (build
  11337, commit d775ebf36)`.
- **Обе модели — через СОБСТВЕННЫЙ `model.fetch` гейтвея** (доказанный
  поток): Qwen2.5-0.5B-Instruct-Q4_K_M (468.6 МБ) и
  Qwen3-1.7B-Q4_K_M (1056.1 МБ); live-прогресс наблюдаем в документе
  run.get, обе COMPLETED, discovery видит файлы, `.part` не остаётся.
- Гейтвей поднимался `scripts/workbench_app.py --no-backend`
  (loopback 127.0.0.1:8765), драйвер сессии — вне репо (Rule 9).

## B. Закрытый ряд 1: сплит brief/parse + первый полный heartbeat-ряд

Инструмент (Rule 9, вне репо): 51-высказывание корпуса
(`tests/fixtures/parse_replies.json`) через НАСТОЯЩИЙ mode-C стек
(Simulator + Mediator + ParserDoor над одним ledger; повествовательная
половина — PINNED документы, детерминированный субстрат), оператор —
живой llama-server; цикл приземлённой сессии отражён дословно
(`cli/main.py::_say_via_engine`): emit → grammar → GBNF-chat (temp 0 /
160 токенов / seed 42) → apply; ParseError → один re-ask с заметкой
сессии; RunnerError → door_error.

**Разложение часов (без пробелов, без двойного счёта):** brief =
emit_call; parse = grammar_snapshot + gbnf_grammar + apply_reply МИНУС
tick; tick = run_steps (делегирующий прокси); generate = chat
адаптера; fold = отдельная проба n=10 на кейс.

**Ряд engine1-q1p7b (TEST_PLAN §8.5 — первый ряд со всеми пятью
колонками):**

| Метрика | Значение |
|---|---|
| Validity raw → 1 re-ask | **51/51 → 51/51 (100% → 100%, ноль re-ask потрачено)** |
| Mix i/q/n | **51/0/0** (самый агрессивный измеренный mapper: каждое высказывание — интент; 16 догадок look_around; вопросы дизамбигуации не срабатывают вовсе) |
| Agreement | 4 full / 15 kind / 32 mismatch |
| Мир отказывает | 4 intent_rejected + 2 take_failed (попытки — факты); 4 take сработало; 0 door errors (v2-грамматика делает one-path класс структурно неэмитируемым) |
| tick | 0.3/0.5 мс (n=51) |
| fold | 0.8/0.9 мс (n=100) |
| brief | 0.9/1.1 мс (n=51) |
| parse | 2.7/3.4 мс (n=51) |
| generate | 11598/12512 мс (CPU: ~617-ток промпт на ~92 ток/с; ~26-ток ответ на ~7.9 ток/с) |

Репо-стороны колонки ложатся в масштаб слитой колонки станций
(brief+parse 1.0–1.1 мс там; половина emit от модели не зависит);
generate доминирует CPU — честная цена этой среды.

**Детерминизм-мини (три рычага):** greedy ×3, seeded ×3, cacheless ×3
(форма §13.1: `cache_prompt false` сырым запросом вне пиннованной
идентичности адаптера) — побайтово идентичны в каждом. Одна
межпраймовая вариация честно записана: один и тот же запрос на
по-разному прогретом слоте однажды ответил `loc_tavern` против
`loc_backyard` — класс prompt-cache, ровно причина, по которой §13.1
пинил кэш выключенным; внутри прогона идентичность не ломалась ни разу.

**Манифест** — через собственный `manifest_row` репо: model_sha256
заполнен, build `b11337-d775ebf36`, `parse_grammar_id
9fa7e9f4359a9201` — **побайтово равен id манифеста round-5 станции**
(кросс-средовая детерминизм чистой функции грамматики).

**Урок среды (честный конфиг 4 ГБ):** AUTO-слоты при `-c 4096`
(4-слотовый unified pool) словили OOM-kill посреди корпуса (anon-rss
3.5 ГБ); пиннутая форма `-np 1` (закон предсказуемого слота §13.1) +
`-c 2048` + q8_0 KV (квант round-6) держит с ~0.6 ГБ запаса.

## C. Закрытый ряд 2: wb-6 live-реверификация

Адаптерская половина управления моделями (POST /models/load + POST
/models/unload, стаб-пины с wb-6) проверена живьём через СОБСТВЕННЫЙ
клиент репо на реальном llama-server b11337:

1. **Эндпоинты только в router-режиме**: одиночная (single-model)
   форма 404 оба (роуты скомпилированы, не зарегистрированы).
2. **Unload совпадает со стаб-пином ровно**: запрос `{"model":
   <stem>}`, ответ `{"success": true}`.
3. **Load работает, но `model` = REGISTRY ID роутера (STEM файла),
   не путь**: `{"model": "Qwen3-1.7B-Q4_K_M"}` → 200 `{"success":
   true}`; форма с путём → 404. Воркбенч в ATTACHED-режиме передаёт
   путь (корректно против path-принимающей сборки; эта сборка
   отказывает) — MANAGED-дефолт эндпоинтов не касается вовсе (spawn
   с `-m`).
4. **Ошибки — OpenAI-конверты**: дубль-загрузка → 400 «model is
   already running»; выгрузка незагруженного → 400 «model is not
   found»; терминальное HTTP-отображение адаптера (без слепого
   ретрая) проверено правильно против обеих.
5. **Законы роутера §13.1 все подтвердились на b11337**: role /
   models_autoload / max_instances в /props; stem-адресация ленивым
   автозагрузом (0.95 с первое касание); переключение моделей при
   `--models-max 1` за 2.62 с (evict + autoload, не рестарт); GET
   /models с per-model status/argv/preset/meta.
6. **Новая поверхность**: GET `/models/sse` — живой стрим статуса
   загрузки по стадиям. Естественный потребитель для live-прогресса
   загрузки в воркбенче; запаркован как ряд-кандидат (вызов
   владельца), здесь не строился.
7. **Дрифт-данное /props**: в single-model форме нет ключа `role`
   (стабовый `"role": "server"` — предположение фикстуры; адаптер
   читает только model_path/build_info, код не трогается).

## D. Что осталось (честная граница)

- **27B GBNF parse arm + one-model-constrained A/B (§4.3 arm a)** —
  остаются рядами станции владельца: 27B Q4_K_M не размещается в
  4.1 ГБ RAM песочницы. Инструмент сплита готов к переиспользованию
  на GPU-станции.
- **Narrator-convention call** — без изменений (форма round-6: ещё
  живые биты на Q9B либо 27B как one-model кандидат).
- GET /models/sse — ряд-кандидат при живом потребителе.

## E. Верификация

- `PYTHONHASHSEED=0 python -m pytest` — **2556 passed + 1 skipped**
  (до и после: поведение не менялось);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (TASKS 593, worklog 10,
  DECISIONS 30);
- `python scripts/topology.py --check` — clean;
- `python scripts/digest.py` — parses iter-312 clean;
- Самопроверка дельты: список путей == `git status --porcelain -uall`
  против BASE `528de9c` (блок Git ниже).

## F. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/TEST_PLAN.md docs/TECH_NOTES.md cli/engine.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-312-stationlive-report.md
git status --short
git commit -m "iter-312-stationlive: the live station row at the sandbox band — the brief/parse split + the first full-column heartbeat row (engine1-q1p7b) + the wb-6 live re-verification (router-mode-only, stem-not-path)"
git push
```

## G. Риски и следующее

- Риск: числа ряда — банды песочницы (CPU/2 ядра, q8_0 KV, 2048
  контекст), не станции; записано в самом ряду и в §13 — тренд-чтение
  обязано это учитывать.
- Риск: одна межпраймовая вариация prompt-cache — записана как
  данное, внутриигровая идентичность не ломалась; станция
  перепроверит на реальных моделях.
- Следующее — вызовы владельца: (1) 27B-рычаги на станции (инструмент
  готов); (2) GET /models/sse как ряд при живом потребителе; (3)
  прочие ряды постоянной очереди (replay-UI NOT-EXPOSED, мир-трек
  W8, inf-3+/obs-3+/wb-13+).
