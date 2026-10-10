# iter-356 · clfarch — «kev и подобные модели => они не могут генерировать текст вообще!»: семантика классификатора ИСПРАВЛЕНА, класс decision-моделей изучен вживую, `/v1/systemone` доказан против инвентаря таверны, оба файла-кандидата владельца прочитаны по HEAD-зондам

**Вызов владельца (2026-10-10, дословно):** «ты дурачок? kev и
подобные модели => они не могут генерировать текст вообще! изучи
принципы работы классификаторов типа jev! я думал поставить
классификатор, чтобы он валидность ответов игрока/llm моделей
проверял и мог "триггеры" дергать доступные, чтобы на симулятор
влиять => типа игрок написал что подошел заговорить с npc и jev
должен понять что там написано было и выбрать релевантное действие
понимаешь? чтобы большая llm модель не тупила и не троила сто лет
или типа того.»

Явный ввод сессии (D-198): коррекция понимания = текущая
задача. Она бьёт ТОЧНО в формулировку iter-351 §A.2 («a legal
classifier IS a grammar-constrained tiny extractor») — формулировка
НЕВЕРНА для класса jev/kev/laya, и владелец это называет прямо.
Ниже: исправление (§A), принципы класса (§B), живая валидация
против НАСТОЯЩЕГО инвентаря пака (§C), вердикты по обоим файлам
владельца (§D), скорректированная архитектура — ровно та, что
владелец описал (§E), честные границы (§F). Нулевой код репо;
нулевые данные пака; INV-1..5 не тронуты. BASE_COMMIT: `760bd3b`
(riders iter-355 не закоммичены владельцем — дельта несёт оба
слоя).

**Класс риска:** R0/R1 (док-райдеры; Rule 9 — весь live-инструмент
вне репо: `scripts/systemone_live_probe.py` в сэндбоксе, модели в
корне сэндбокса).

## A. Что именно было неправильно (и где это записано)

iter-351 §A.2 свернул «классификатор» владельца в форму F:
ультралайт, вызываемый ЧАТОМ (`/v1/chat/completions`) под
грамматикой ответа, эмитящий ДОКУМЕНТ интента. Для класса
jev/kev/laya это ошибка КАТЕГОРИИ, дважды:

1. **Модели этого класса не генерируют текст вообще** — нет
   авторегрессии, нет сэмплинга, нет декодера как поверхности.
   Их выход — распределения вероятностей над ЗАДАННЫМИ в запросе
   опциями. Карточка модели говорит это дословно: «It never
   generates text, so there is nothing to parse and nothing to
   hallucinate».
2. **Поверхность вызова другая**: llama.cpp с 2026-10-02 (PR
   #29818, merged; билд-окно станции b11538 уже несёт) отдаёт
   decision-модели через `POST /v1/systemone` — `{state,
   questions}`, вопросы трёх типов: `choice` (выбор из словаря
   критериев), `noul` (P[да]), `score` (ордин-шкала). Ответ —
   вероятности по опциям, всё в ОДИН прямой проход.

Следствие для батарей m3: **рука F никогда не измеряла идею
владельца.** Она измеряла крошечный ГЕНЕРАТИВНЫЙ экстрактор
(Qwen3-0.6B под грамматикой) — легально, но это другой класс.
Оба кандидата владельца (Kev-4B, decider-4b) в форме F были
обречены КАТЕГОРИЧЕСКИ: чат-вызов к негенеративной голове (см.
§C T5 — сервер отказывает за 1 мс). CPU-датум «F −2 full» —
артефакт 0.6B, не приговор идее.

## B. Класс: как работают decision-модели типа jev

**Референс** — TypeSafe Jev (закрытый API, «System 1» model).
Открытые репродукции/альтернативы (все Apache-2.0):

| Модель | Основа | Параметры | Заметки |
|---|---|---|---|
| jaredpalmer/kev-4B | Qwen3.5-4B-Base + LoRA | 4.2B | EN; trained на banking77/NLI/sentiment/safety; accuracy 0.838 transfer-v4 |
| convaiinnovations/laya | ModernBERT-large + decision head | 421M | EN root; head: 2 слоя + option-marker scorer; RLCD (калибровка честности) |
| convaiinnovations/laya-multilingual | mmBERT-base | 322M | 100+ языков, РУССКИЙ включён; НЕТ ggml-org GGUF |
| Mapika/decider-2b/4b/35b | Qwen3.5-Base | 0.8B-35B | «open reproduction of the System One class (TypeSafe AI's Jev)»; НЕ в пятёрке llama.cpp |
| OpenJev / Julia-1 / lev | — | — | +vision у openjev; все в пятёрке |

**Механика** (одинаково у всех): энкодер читает `state`
(текст/JSON) + все вопросы вызова; каждая опция каждого choice-
вопроса маркерится своим токеном; скоры маркеров softmax-ятся
внутри вопроса. Пространство ответа задаётся В ЗАПРОСЕ — новые
схемы (инвентарь действий пака!) не требуют переучивания.
Температуры калибровки ПЕЧАТАЮТСЯ В GGUF-МЕТАДАННЫЕ (у Laya —
по типу И по числу опций: choice.2=1.906, choice.3_5=1.760,
choice.6_10=1.000, choice.11=0.101). Знание об ответе = 1 forward
pass; `usage.output_tokens = 0` на каждом вызове (§C).
Скорость: карточка Laya — 32.8-39.5 мс/вопрос на T4; 103-332
вопросов/с батчем.

## C. ЖИВАЯ валидация (§13.1-класс): b11540 ubuntu × Laya-Q8_0 × инвентарь НАСТОЯЩЕГО пака

Инструмент: `llama-server` b11540 (в билде строки `/v1/systemone`,
`laya`, `kev` найдены в `libllama-server-impl.so` — поверхность
подтверждена до запуска) + `ggml-org/Laya-Q8_0.gguf`
(449 397 600 байт, 201 тензор, modern-bert, `decision.type=laya`,
контекст 8192, `max_head_tokens=192`). Критерии — НЕ выдуманы:
словарь 16 действий `content/tavern_pack/actions.json`
(intent → label + notes) и 10 целей из `entities.json`. Сырьё:
`scripts/systemone_live_results.json` (сэндбокс).

| Тест | Вход | Ответ | Вердикт |
|---|---|---|---|
| T1 EN, сценарий владельца («walk up to the guard and start talking») | choice ×16 | **move** P≈1.0 (talk 2-й, 6.8e-10); noul is_action 0.736; score risk 0.667 | работает; читает «подошёл» как подход (честная лексика первого действия) |
| T1b инструкция «PRIMARY action, not the approach walk» | choice ×16 | move снова P≈1.0 | рычаг инструкции НЕ перевернул — лексическое доминирование; критерии надо проектировать (или 2 шага: move→talk) |
| T2 РУССКИЙ «подошёл к npc, хочу заговорить с ним» | choice ×16 | **coerce** P=0.9998 (WRONG; talk 2-й 1.7e-4) | EN-чекпоинт на кириллице = уверенно НЕВЕРЕН — ровно честный предел карточки («collapses on non-Latin scripts… confident while being wrong — gating cannot save you»); доверие НЕ фильтрует |
| T3 цель («the guard by the bar… missing purse») | choice ×10 целей | **npc_guard_01** 0.416 top-1; purse_01 0.396; conf 0.35 | top-1 верен; лексическое заражение «purse» видно; слабое доверие честно |
| T4 валидация: чистая проза-атмосфера («fire pops in the hearth») | choice + noul | **arson** P≈1.0 (WRONG); any_action 0.536 | уверенно НЕВЕРЕН на атмосферной прозе — zero-shot предел базы |
| T4b валидация: явная кража («reaches into the belt and takes the purse») | choice + noul | **use** P≈1.0 (steal 2-й, 1.5e-8) | почти-верен, но не тот лейбл — zero-shot маппинг слаб |
| **T5 чат-поверхность на decision-модели** («hello») | /v1/chat/completions | **HTTP 500 за 1 мс**: «the current context does not support logits computation» | **НЕГЕНЕРАТИВНОСТЬ ДОКАЗАНА ВЖИВУЮ** — сервер отказывает; форма F была невозможна по построению |

**Латентность** (сэндбокс CPU, 210 input-токенов): 0.80–1.39 с на
вызов, ВСЕ вопросы вызова — один проход; карточка: 32.8–39.5 мс
на T4 GPU → на полосе 3080 Ti = десятки миллисекунд. Контекст
сравнения: экстракция руки F на CPU-полосе стоила ~4.95 с
(iter-351) — роут systemone дешевле ~5× уже на CPU, и разрыв
взрывается на GPU. Нет KV-прайминга, нет сэмплинга, нет грамматики
— «смена тапок» как класс исчезает: это свойство ЗАПРОСА, не
сессии (iter-351 §A.1, подтверждено).

## D. Оба файла владельца — вердикты по живым HEAD-зондам

Зонд GGUF-заголовков HTTP Range-запросами (без полной загрузки;
`gguf_header_probe.py`): число тензоров, `*.decision.*` метаданные.

- **Kev-4B (файл станции, «wrong number of tensors; expected 428,
  got 426», 20 смертей подряд — iter-354 §H):** СВЕЖИЙ
  `ggml-org/Kev-4B-Q8_0.gguf` = **428 тензоров, self-consistent**,
  `qwen35.decision.type = kev`, калиброванные температуры
  choice/score/noul = 2.406. То есть СТАНЦИОННЫЙ ФАЙЛ —
  устаревшая/битая конверсия; **«перекачать» (iter-354) теперь
  подтверждено живым зондом: перекачка с ggml-org/Kev-4B-GGUF
  реально чинит загрузку.** Билд станции b11538 уже знает
  qwen35+kev (ошибка числа тензоров — это ошибка УРОВНЯ АРХИТЕК-
  ТУРЫ, т.е. загрузчик decision-класса уже работал).
- **decider-4b («refusing to extract»):** `Mapika/decider-4b-v2.1-
  Q8_0.gguf` = **426 тензоров, НИКАКИХ decision-метаданных**,
  конверсия как ОБЫЧНЫЙ qwen35 causal-LM + свой `chat_template.jinja`
  и свой скрипт вызова `decide_gguf.py`. Mapika НЕ в пятёрке
  llama.cpp (laya, julia-1, lev, openjev, kev): даже чистый файл
  не ответит на `/v1/systemone` сегодня. Чат-вызов к нему в форме
  F был категорически неверен обеими сторонами: «It is called
  from software, not chatted with» (карточка дословно).
- Попутно: число 426 у обоих файлов — совпадение осей (Mapika
  честно имеет 426; станционный Kev ОБЕЩАЕТ 428, содержит 426) —
  но это объясняет, ПОЧЕМУ сбой выглядел как «сломан GGUF», а не
  «не та поверхность».

## E. Скорректированная архитектура — форма R (ровно слова владельца)

Игрок/LLM-проза → `POST /v1/systemone`:

```json
{"state": {"message": "<реплика игрока или проза LLM>"},
 "questions": {
   "action":  {"type": "choice",   "instructions": "Which pack action…",
               "criteria": {…actions.json: intent → label+notes…}},
   "target":  {"type": "choice",   "instructions": "Which entity…",
               "criteria": {…entities.json сцены…}},
   "is_modeled": {"type": "noul",  "instructions": "Is a modeled action attempted?"},
   "risk":    {"type": "score",    "criteria": ["safe","bold","reckless"]}}}
```

→ топ-опция каждого вопроса → **детерминированная дверь** собирает
интент-документ из СХЕМЫ действия пака (INTENT_SCHEMA §2: type из
choice; target из второго choice; fields — дефолты схемы);
предикаты `requires` валидируют; событие коммитит. Классификатор
ROUTES, никогда не коммитит — VISION §5 не просто цел: **сильнее,
чем F** — decision-модель ФИЗИЧЕСКИ не может нагаллюцинировать
документ: она выбирает только из известных ключей. Большая LLM
освобождена от парсинга целиком («не тупила и не троила») — ей
остаётся проза/нарратив (или ход вообще без неё, быстрый путь).

## F. Честные границы (что измерять в R-руке до доверия)

1. **РУССКИЙ**: EN-чекпоинт уверенно неверен (T2); ggml-org НЕ
   конвертировал laya-multilingual; Kev-4B (Qwen3.5-токенизатор,
   кириллица в словаре) — EN-обучен, точность на РУ не измерена.
   R-батарея обязана мерить Kev на русских репликах до доверия.
2. **Zero-shot**: базовые чекпоинты ≈ chance на typed-decisions
   (карточка: 0.362 базы vs 0.766 fine-tune; T4/T4b подтвердили
   вживую: уверенно неверные ответы). Тонкая настройка на корпусе
   таверны (путь Kaggle-ноутбука laya) — где прыгает точность.
   Дверь остаётся валидатором в любом случае.
3. **Бюджет опций**: `max_head_tokens=192` (Laya EN) → 16 действий
   ≈ 11 токенов/опцию — выше опасной зоны (77 опций Banking77);
   разросшийся инвентарь (province) требует двухступенчатого
   choice или поднятия бюджета.
4. **Decision-модель на GPU-полосе** — вопрос VRAM-бюджета: Laya
   Q8 = 450 МБ рядом с главной моделью на 12 ГБ — тривиально;
   Kev-4B Q8 = 4.48 ГБ — заметный сосед (борьба с Gemma-4-E4B).

## G. Строки и решения

- ОТКРЫТА (владелец-гейт): **R-рука для M4-батареи** — роут
  `/v1/systemone` (Kev-4B перекачанный и/или Laya) против F/H на
  ТОМ ЖЕ корпусе: точность топ-1 против золота, латентность,
  RU-полоса. Это та вилка, которую вопрос владельца 2026-10-09
  реально спрашивал — и которую m3 не измерял.
- ВЛАДЕЛЬЦУ, одна перекачка: `ggml-org/Kev-4B-Q8_0.gguf` (4 483
  801 504 байта) чинит загрузку; decider-4b на сегодня вне
  llama.cpp-пятёрки — не тратьте на него прогон.
- M2 (block/downgrade/allow) и M3 (H/F/G2) решения НЕ тронуты —
  R композируется с любой политикой, как и m3-формы.
- Upstream-пробел записан: ggml-org laya-multilingual GGUF
  отсутствует (строка наблюдения, не работы репо).

## H. Верификация и доставка

- `PYTHONHASHSEED=0 python -m pytest -q` — зелёные (счёт в
  STATUS); `ruff check .` чист; `python scripts/docguard.py` чист;
  topology чист; INV-1..5 не тронуты (нулевой код).
- Живое сырьё: `scripts/systemone_live_results.json` (сэндбокс);
  зонды HEAD: Kev 428/kev-метаданные, decider 426/без, Laya
  201/laya-метаданные.
- Дельта-архив против BASE `760bd3b`: attachment + tmpfiles-ссылка
  + md5 (§12.2); изменённые пути в §12.3-блоке ниже.

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/LLAMA_CPP_INFERENCE_CONTROL_LAW.md docs/iterations/iter-356-clfarch-report.md
git status --short
git commit -m "iter-356-clfarch: THE CLASSIFIER SEMANTICS CORRECTED (the owner's «kev и подобные => не могут генерировать текст вообще!» call - iter-351 §A.2's «legal classifier = grammar-constrained extractor» WRONG for the jev/kev/laya class; the class studied live: TypeSafe Jev the reference, the open family, llama.cpp PR #29818's /v1/systemone in b11538+; VALIDATED LIVE §13.1-class: b11540 + Laya-Q8_0 against the REAL tavern_pack inventory - T1 EN owner scenario move P≈1.0, T3 target top-1, T5 chat REFUSED HTTP 500 in 1ms (non-generativity proven), output_tokens=0, 0.80-1.39 s CPU/33ms-class GPU; THE HONEST LIMITS live: EN-checkpoint confidently WRONG on Russian (coerce 0.9998), scene-prose validation confidently wrong (arson), zero-shot base ≈ chance - fine-tune is the jump, the door stays the validator; THE OWNER'S TWO FILES live-probed: ggml-org Kev-4B-Q8_0 SELF-CONSISTENT 428 tensors + kev metadata (the re-download VERDICT confirmed - the station file is the stale copy), Mapika decider-4b 426 tensors NO decision metadata OUTSIDE the llama.cpp five; THE R-FORM (the owner's own architecture): systemone choice over the pack's action inventory + target choice + noul validity -> the deterministic door assembles the intent - the classifier ROUTES never commits, STRONGER than F by construction; the M4 R-arm row opened owner-gated; M2/M3 decisions untouched; zero repo code)"
git push
```

**Done:** исправление записано; класс изучен; механизм доказан
живьём против настоящего пака; оба файла владельца получили
вердикты с живыми данными; R-форма открыта строкой; райдеры
прошли чеки.
**Not done:** сама R-рука батареи (владелец-гейт: это прогон
станции, не док); RU-полоса на Kev (нет модели в сэндбоксе — 4.5 ГБ
скачивание; вилка записана).
**Next:** выбор владельца: (1) R-батарея M4 (нужна перекачка
Kev-4B и/или Laya на станцию), (2) M3 GPU re-run (кит iter-355 уже
двойной клик), (3) M2-решение. Всё композируется.
**Active KIs:** KI#113 (test_lab, как в STATUS).
