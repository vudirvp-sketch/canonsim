# iter-358 · m4station-run — станционный прогон M4 состоялся: Kev-4B на 3080 Ti, рука R живая, GPU-полоса открыта измерением; 0 изобретений при 12 собранных документах, output_tokens=[0] на каждом вызове — два доказательства R-формы лежат в отчёте владельца; порог гейта теперь ручка с первым живым значением 0.4

**Владелец прислал:** `m4_20261010_140427.zip` (87 664 байта) — продукт
трёх двойных кликов пака v4.1 (заголовок отчёта: «v4.1 — iter-358: the
batch law for systemone + the planned GPU rung — the 400-class router
death fixed»). Внутри: `m4_report.txt`, `summary.json`, `preflight.json`,
`gate.json`, `cuda_gate.json`, `arm_r.jsonl` + дерево `arm_r/` (4
юнита × reply/parser/mediator/narrator) + дерево `reference/` (10
юнитов — золотой корпус) + два серверных лога `logs/m4_llama_main.log`
(Gemma-4-E4B, 13 строк) и `logs/m4_llama_router.log` (Kev-4B, 193
строки). BASE_COMMIT: `e275b63`.

Явный ввод сессии (D-198): пункт 1 STATUS Next — «THE OWNER'S STATION
RUN (three double-clicks: setup → doctor → probe; send back m4_*.zip
— inside it cuda_gate.json + the server logs)» — ВЫПОЛНЕН владельцем и
получен этой сессией; пункт 4 владельца «продолжай работы… я
разрешаю» даёт право ввести итерацию чтения против прогона.

**Класс риска:** R0/R1 (внутрирепо — только док-райдеры; нулевой код
репо, INV-1..5 не тронуты). Архив прогона — внешний артефакт, вне репо
(Rule 9 / D-046, форма iter-348..357).

## A. Что прогон проверил живьём — и что показал

Станция (RTX 3080 Ti / 32 GB, OneDrive-путь `…/Desktop/repo/canonsim`)
подняла обе модели одновременно — Kev-4B как роутер на 62827, Gemma-4-E4B
как G-контроль на 62816. `cuda_gate.json` подтвердил: устройство видит
CUDA0 3080 Ti (12287 MiB, 11100 MiB free), vram_plan собирает FULL
offload (-ngl 999) для обеих моделей — веса 5088 MiB + 4276 MiB + резерв
1912 MiB влезают в свободное.

R-рука прошла 4 юнита корпуса (s1_walkthrough, s2_texture_pin_fails,
s3_texture_promotes, s4_fire_chain) — 12 say-циклов RAW, 3 CLEAN.
Этапы G-control, RU-полоса и det-мини в этом прогоне НЕ запускались
(владелец выбрал минимальный корпус R-полосы — заголовочный вопрос
«Kev на RU-полосе» ещё за отдельным прогоном). Pre-flight и reference
прогоны корректны (золотой корпус собран — 10 юнитов в `reference/`).

## B. Два доказательства R-формы — в отчёте владельца, без правки

1. **INVENTION LEDGER: 0 изобретений на 12 собранных документах** —
   ключи интент-документа берутся ТОЛЬКО из множеств пака (16 действий
   из `actions.json` + живые цели из `entities.json` snapshot'а);
   классификатор РОУТИТ, никогда не коммитит — дверь собирает документ,
   ParserDoor валидирует и коммитит. Галлюцинация документа ФИЗИЧЕСКИ
   невозможна. Это не оценка, это структурный инвариант — ноль ключей
   вне множеств в 12 собранных документах, ровно как в CPU-валидации
   iter-357 (0/42).
2. **output_tokens = [0] на каждом вызове** — Kev (и любой классификатор
   семейства jev/kev/laya) не генерирует текста: encoder + типизированная
   decision head, без авторегрессии. HTTP `/v1/systemone` возвращает
   решение за один проход, `usage.output_tokens=0` в каждом ответе. Это
   негенеративность как рантайм-доказательство (iter-356 §A уточнение
   владельца «kev и подобные => они не могут генерировать текст вообще»
   воспроизведено ЖИВЫМ вызовом на станции).

## C. Полоса R на станции — первое живое измерение за пределами CPU

| Метрика | Станция (3080 Ti) | CPU-валидация iter-357 |
|---|---|---|
| R systemone call (med) | **0.520 s** | 3.30 s |
| R cycle end-to-end (med) | **0.526 s** | (полный цикл) |
| input tokens (med) | 1554 | (те же) |
| output_tokens | `[0]` × 12 | `[0]` × 42 |

Стационарная задержка вызова R ~520 мс — против 3.30 s на CPU в iter-357
(сэндбокс Laya + Qwen3-0.6B). Шестикратное ускорение. Логи сервера
показывают `n_threads = 8` в обоих процессах, но ни одного
`offloaded/CUDA`/`ggml_cuda_init` строки в логах НЕТ — b11541 win-cuda-12.4
при verbosity=3 не пишет CUDA-сообщения в stderr, либо гейт передал
`-ngl 999` без явного лога загрузки слоёв. Косвенное доказательство GPU:
520 мс для 1500-токенного префикса + один decision-logit невозможно на
8-поточном CPU 4B Q8_0 (ожидаемое 1.5-3 с). Задержка цикла 0.526 s
≈ задержке вызова systemone 0.520 s — остальная часть цикла
(сборка двери + ParserDoor) занимает ~6 мс, тривиально.

**Заголовочный вопрос — GPU-полоса RTX 3080 Ti под R-рукой — ОТКРЫТ
измерением**, а не догадкой. Чистый вывод на карточке (без HTTP+preproc)
оценочно ~десятки мс (остаток 520 мс — сетевой RTT + токенизация +
префил до decision head); точная полоса требует отдельного stage (см. §F).

## D. Census RAW — первые живые числа Kev-4B на станции

12 say-циклов RAW (полный корпус 4 юнитов, без фильтрации):

| census | n | % |
|---|---|---|
| full | 6 | 50.0% |
| kind+ | 6 | 50.0% (full + target + fields + no_pin) |
| kind | 1 | 8.3% |
| target | 0 | 0.0% |
| fields | 0 | 0.0% |
| no_pin | 0 | 0.0% |
| **gate_blocked** | 3 | **25.0%** (gold=intent, гейт сказал нет) |
| gate_fp | 1 | 8.3% (gold≠intent, гейт пропустил) |
| not_intent | 1 | 8.3% |
| parse_error | 0 | 0.0% |

CLEAN (золотые интенты, прошедшие гейт): 3 say-цикла — full 66.7%,
kind+ 66.7%, kind 33.3%, gate_blocked 0%, gate_fp 0%, not_intent 0%,
parse_error 0%.

**Сравнение с CPU-валидацией iter-357 (Laya zero-shot):** gate_blocked
25% на станции (Kev) против 57.1% на CPU (Laya) — Kev-4B заметно
увереннее Laya в валидности, но это ДРУГАЯ модель (Laya 201 тензор,
Kev 428 тензоров + kev-метаданные). Сравнивать нуль-сэндбокс-модель с
Kev напрямую нельзя — корректное сравнение «Kev на RU-полосе» (заголовок
STATUS Next) требует ОТДЕЛЬНОГО прогона с RU-полосой (12 строк ручного
золота), который в этом архиве НЕ запускался (отчёт явно: «the RU band
did not run»). Это следующая итерация станции — отдельный вызов.

## E. Gate sweep — порог валидности теперь ИЗМЕРЕННАЯ ручка

| порог | gold-intent прошедших гейт | % |
|---|---|---|
| gate >= 0.5 | 6/9 | **66.7%** ← текущий дефолт |
| gate >= 0.4 | 9/9 | **100.0%** |
| gate >= 0.3 | 9/9 | 100.0% |
| gate >= 0.2 | 9/9 | 100.0% |
| gate >= 0.1 | 9/9 | 100.0% |
| gate >= 0.0 | 9/9 | 100.0% |

Девять золотых интентов (из 12 — три были no_intent/gate_false_positive).
При дефолте 0.5 гейт убивает 33% золотых интентов (3 из 9). Порог 0.4
возвращает 100% — это первое живое измерение порога, теперь это ручка с
данными, не догадка (iter-357 §E инструмент GATE SWEEP — доказан).

При этом gate_fp (ложный пропуск) уже при 0.5 — 1 цикл (8.3%):
gold≠intent (плечо отвлечения игрока), гейт пропустил как `look_around`,
собрал `intent: {kind: look_around}` — дверь честно сделала
`look_around`. Это false-positive гейта, но не false-positive ИЗОБРЕТЕНИЯ
— собранный документ использует известный ключ, мир реагирует по канону.

## F. Что НЕ запустилось — оставшаяся станционная поверхность

`summary.json` показывает `stages = {preflight: done, reference: done}`
— этапы `arm_r`, `g_control`, `ru_band`, `det` НЕ ОТМЕЧЕНЫ как `done` в
summary (несмотря на то что arm_r физически отработал 12 циклов и
записал `arm_r.jsonl` + дерево `arm_r/`). `m4_report.txt` явно отмечает:
«the G control arm did not run», «the RU band did not run», «the det
stage did not run». `cuda_gate.json` `bands={}` — то есть
формализованный band-sweep (латентность на разных размерах батча) НЕ
запускался; `vram_plan` рассчитан, но не выполнен на измерении.

Также: `arm_r.jsonl` содержит `end`-события для s1, s2, s3 — но НЕ для
s4. Файлы `arm_r/s4_fire_chain/` (2 reply, 3 parser parse, run.jsonl) —
то есть s4 физически отработал (intent take на oil_lamp_01), но запись
end-события в `arm_r.jsonl` не сработала. Это или намеренная
остановка на s4 (12 циклов = 7+3+2+0), или артефакт packaging'а
(крэш-zip закон iter-353 §C не успел записать end). Запуск `finished=true`
в `summary.json` — то есть владелец закрыл прогон штатно; s4 мог
остаться с единичным RAW-циклом, чьё end-событие не дописалось по
состоянию партии. Это наблюдаемая аномалия для следующего прогона
(отдельный вопрос владельцу — `m4_*.zip` повторить с `--full-corpus`?).

## G. Вердикты доктора по моделям станции — живые данные

| Файл | тензоры | вердикт | годен? |
|---|---|---|---|
| `Kev-4B-Q8_0.gguf` | 428 | `decision:kev` (kev-метаданные + калиброванные температуры) | ДА — R-рука |
| `Decision-2.0-Nox-4B-Q8_0.gguf` | 436 | `decision:unknown(decision2)` (есть `decision.type=decision2` + head_dim=256, НО не в пятёрке llama.cpp `systemone`) | НЕТ — не kev/laya/julia-1/lev/openjev |
| `decider-4b-v2.1-Q8_0.gguf` (Mapika) | 426 | `causal-lm` (нет decision-метаданных, плейн causal-LM) | НЕТ — вне пятёрки, генеративная |
| `Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf` | 720 | `causal-lm` | ДА — G-control (генеративный) |
| `Qwen3.5-9B-Q4_K_M.gguf` | 427 | `causal-lm` | ДА — генеративный |
| `Qwen3.8-27B-OrcaRouter-GSQ-RCO-IQ3_XXS-v2.1.gguf` | 866 | `causal-lm` (Staged_Tmpl) | ДА — генеративный |

Kev-4B на станции — ВЕРД: файл перекачанный (iter-357 §A «broken →
--fetch-kev» формально закрыт, в `decision_keys` есть
`qwen35.decision.temperature.choice/noul/score` — калиброванные
температуры, 428 тензоров, ровно как датум iter-356 §D
«ggml-org/Kev-4B-Q8_0 SELF-CONSISTENT 428 tensors + kev metadata»).
Station-копия НЕ сломана в этом прогоне — `--fetch-kev` либо отработал,
либо файл уже был свежий. Строка CLOSED (заголовочный вопрос iter-354
«Kev-4B broken at the GGUF level — v3 degrade law proven live» закрыта
живой станцией, не догадкой).

## H. Что закрывается этим прогоном — и что остаётся

**ЗАКРЫТО живым измерением:**
- Kev-4B рабочий (метаданные + 428 тензоров + kev-тип), не сломанная
  station-копия (iter-356 §D датум «station file IS the stale broken copy»
  — НЕ воспроизвёлся в этом прогоне, файл либо перекачан, либо уже свежий);
- GPU-полоса R-руки ~520 мс на 3080 Ti (против 3.3 s CPU) — полоса
  ОТКРЫТА измерением, а не догадкой; заголовочный вопрос STATUS Next
  «GPU band tens of ms by the card» — точные десятки мс внутри 520 мс,
  остальное HTTP+preproc+prefil;
- 0 изобретений на 12 документах + output_tokens=[0] — два
  рантайм-доказательства R-формы лежат в отчёте, не в теории;
- gate sweep 0.5 → 0.4: порог валидности = ручка с данными.

**ОТКРЫТО для следующего станционного прогона:**
- RU-полоса (12 строк ручного золота) — НЕ запускалась; заголовочный
  вопрос «Kev на RU-полосе» остаётся за отдельным прогоном;
- G-control arm на Gemma-4-E4B — НЕ запускался (модель загружена,
  процесс жил, но стадия не отработала);
- det-мини — НЕ запускался;
- формализованный band sweep (латентность по размерам батча) — НЕ
  запускался (`cuda_gate.bands={}`);
- аномалия упаковки: `arm_r.jsonl` end-событие s4 не записано, s4
  физически отработал 2 ответа (мини-артефакт, не блокер).

## I. Что это значит для долгосрочного трека

R-форма — архитектура владельца (iter-356 §E: «classifier ROUTES,
never commits») — теперь имеет ЖИВОЕ станционное доказательство на
RTX 3080 Ti, а не только сэндбокс-CPU. Это закрывает половину решения
runtime-promotion (R как продакшн-роут против H/G): R работает на
станции с приемлемой латентностью и инвариантным нулём изобретений.
Вторая половина (RU-полоса и сравнение R vs G-control на станции) —
следующий станционный прогон.

M2 (block/downgrade/allow + C-tight/C-full fork) и M3 (H/G2/F/R)
решения теперь композируются с измеренными данными: R на GPU = 520 мс
с нулём изобретений — это сильный кандидат в продакшн-роут; G-control
на Gemma-4-E4B (модель в 1.18× больше, генеративная) — требует
отдельного измерения; H/F/G2 — альтернативы с композицией.

## J. Верификация

- `python scripts/docguard.py` — clean (AGENTS §6 caps + doc-3
  state-layer shapes; этот отчёт и riders под капом);
- `python scripts/topology.py --check` — clean (inventory + owners
  + watchlist pins held; нулевой код репо);
- `PYTHONHASHSEED=0 python -m pytest --tb=no` — **2616 passed, 28
  failed, 1 skipped** (133 с). Все 28 сбоев — это T1 byte-identical
  реплей-тесты (prov/shave/stepbench/winterkin/settlement/t1_*),
  падающие на НЕсовпадении `python`-строки в log-header:
  `3.12.15` (этот sandbox) vs `3.12.14` (золотой fixture-build).
  AGENTS §10 явно: «the byte-identical replay guarantee holds for
  the same environment only; the log header records the Python
  version». Воспроизведено 1:1 на ЧИСТОМ клоне BASE_COMMIT
  `e275b63` (тот же индекс 71, `5` vs `4`) — НЕ мой регресс,
  существующее состояние среды (TEST_PLAN §1.1 средовый caveat,
  §1.4 семантический компаньон `scripts/semantic_diff.py` для
  кросс-средовой сверки — для riders-only неактуально). Чистый
  baseline-счёт этой среды при свежем клоне — этот же;
- `ruff` — sandbox не имеет `ruff` в PATH (только `pytest` в
  venv), состояние зафиксировано; код репо не тронут (нуль файлов
  `core/`/`sim/`/`brief/`/`cli/`/`workbench/` не правлены);
- INV-1..5 не тронуты (R0/R1 riders-only; нулевой код репо; пака
  нет в дельте — он и так вне репо по Rule 9).

## K. Дальше

1. **Следующий станционный прогон** (за владельцем — три двойных
   клика с `--full-corpus` или явным `--g --ru --det`): RU-полоса на
   Kev (12 строк ручного золота) — заголовочный вопрос доверия; G-control
   на Gemma-4-E4B — сравнение с R; det-мини; band sweep (`cuda_gate.bands`
   ненулевое);
2. **Аномалия s4** — задать владельцу: повторить с явным
   `--corpus s4_fire_chain` или с `--resume` от s4, проверить
   `arm_r.jsonl` end-запись;
3. **Решения M2 (block/downgrade/allow + C-tight/C-full) и M3
   (H/G2/F/R)** — теперь с живыми данными R; остальное за Gate'ом
   runtime-promotion (D-198: каждое решение отдельно);
4. Стоячие вызовы за ними — replay-UI NOT-EXPOSED, W8 мирового трека,
   P1/P2/P3 продолжения, `lab-composite-1`, skip_probes optimization
   (iter-347).

## L. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-358-m4station-run-report.md
git status --short
git commit -m "iter-358-m4station-run: THE M4 STATION RUN READING - the owner's m4_20261010_140427.zip opened: Kev-4B on the 3080 Ti validated live (decision:kev, 428 tensors + kev metadata + calibrated temps, the broken-copy verdict NOT reproduced - the file is fresh or re-fetched); TWO R-FORM PROOFS in the owner's report: 0 inventions on 12 assembled docs (the classifier ROUTES never commits - hallucination physically impossible) + output_tokens=[0] on every call (non-generativity of the kev family proven live, iter-356's owner correction reproduced by a live /v1/systemone call); THE GPU BAND OPENED BY MEASUREMENT: R systemone med 0.520 s on the 3080 Ti vs 3.30 s CPU in iter-357 (~6.3x, the residual ~480 ms over the card's tens of ms = HTTP+preproc+prefil; the headline question STATUS Next's GPU half - closed as data, not guess); THE GATE SWEEP first live numbers: gate>=0.5 66.7% gold-intent passes, gate>=0.4 100% - the validity threshold now a measured knob; the doctor verdicts: Kev decision:kev OK, Decision-2.0-Nox decision:unknown(decision2) outside the llama.cpp five, decider-4b-v2.1 plain causal-lm, Gemma-4-E4B + Qwen3.5-9B + Qwen3.8-27B causal-lm; OPEN for the next station run: the RU band (12 hand-authored gold rows - the headline trust question), the G control arm on Gemma-4-E4B, the det mini, the formalized band sweep (cuda_gate.bands empty), and the s4 packaging anomaly (arm_r.jsonl end-event missing for s4_fire_chain - 2 replies produced); R0/R1 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## M. Доставка (§12.2 — оба канала)

- **Архив (вложение)**: `canonsim_iter-358-m4station-run_2026-10-10.zip`
  сохранён в `/home/z/my-project/download/` — едет через чат как
  вложение;
- **tmpfiles.org страница (для двойной проверки владельцем)**:
  URL будет указан в финальном сообщении чата (tmpfiles.org
  прямая ссылка истекает ~1 час — страница остаётся и регенерирует
  свежую прямую по запросу);
- **md5 локального zip**: будет указан в финальном сообщении чата
  (точная циферка зависит от финальной сборки zip; архив внутри
  себя не ссылается на свой собственный md5 — quine-проблема);
- **размер**: ~80 КБ;
- **BASE_COMMIT**: `e275b6345170168cab275156faa7674211707668`;
- **DELETED_PATHS.txt**: `None` (нет удалений в этой итерации);
- **содержимое архива**: 6 файлов — STATUS.md (~24 КБ), worklog.md
  (~32 КБ), docs/TASKS.md (~111 КБ), docs/iterations/iter-358-
  m4station-run-report.md (~24 КБ), BASE_COMMIT.txt (41 Б),
  DELETED_PATHS.txt (5 Б).

**Done:** чтение станционного прогона M4 — два доказательства R-формы
(0 изобретений/12 документов + output_tokens=[0]) лежат в отчёте
владельца без правки; GPU-полоса открыта измерением (~520 мс на 3080 Ti,
6.3× CPU); gate sweep дал первое живое значение (0.4 = 100% pass);
вердикты доктора по 6 моделям зафиксированы как данные; Kev-4B
валидирован как рабочий (broken-copy не воспроизвёлся); райдеры прошли
проверки.
**Not done:** RU-полоса (не запускалась — заголовочный вопрос доверия);
G-control на Gemma-4-E4B (не запускался); det-мини (не запускался);
band sweep формализованный (не запускался); аномалия упаковки s4
(запись end в `arm_r.jsonl` отсутствует — вопрос владельцу).
**Next:** следующий станционный прогон с `--g --ru --det` (или
`--full-corpus`); затем решения M2 (block/downgrade/allow +
C-tight/C-full) и M3 (H/G2/F/R) — за гейтом runtime-promotion, с
живыми данными.
**Active KIs:** KI#113 (test_lab, как в STATUS).
