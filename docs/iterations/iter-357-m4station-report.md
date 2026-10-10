# iter-357 · m4station — THE M4 STATION PACK: скрипт «нормально проработан» — классификаторная эра станции собрана, валидирована живьём насквозь и передана владельцу в форме трёх двойных кликов

**Вызов владельца (2026-10-10, дословно, пять пунктов):**
«вот у тебя есть canonsim_m3_station_pack_v3.7z ==> тебе нужно
нормально проработать скрипт: 1) у меня rtx 3080ti! и 32gb ram!
нужно чтобы все запускалось адекватно и быстро работало, ало! 2)
сама станция у меня локально тут лежит …llama.cpp => можешь
скриптом нужную версию ставить последнюю для работы с cuda. 3)
модели лежат тут: …workbench\runtime\models 4) тебе важно понять
что тестируется с Kev-4B-Q8_0.gguf/Decision-2.0-Nox-4B-Q8_0.gguf/
decider-4b-v2.1-Q8_0.gguf ===> эти модели вообще не генерируют
текст! это jev подобные классификаторы… 5) тут у меня есть
llama.cpp но я не уверен что она та что нужна» + «продолжай
работы, открывай то что сейчас важнее всего сделать, логичнее и
качественнее на долгосрок. я разрешаю.»

Явный ввод сессии (D-198): m4-r строка ВЫЗВАНА (пункт 4 =
архитектура iter-356 §E дословно; пункты 1-2-3-5 = инфраструктура
станции). Пять пунктов ложатся на четыре инструмента пака
один-к-одному. BASE_COMMIT: `07cf7f3`.

**Класс риска:** R0/R1 (внутрирепо — только док-райдеры; нулевой код
репо, INV-1..5 не тронуты. Пак — внешний инструмент вне репо, Rule 9
/ D-046, форма iter-348..355; md5 пака
`4518ce2593bac53d8c0183963531f510`, 53 298 байт — для сверки).

## A. Что сделано — THE M4 STATION PACK (11 файлов, вне репо)

Двойной-клик форма; кладётся куда угодно рядом с canonsim (лестница
репо — то же подмножество m2 v2, плюс ПАК-ЛОКАЛЬНЫЙ движок теперь
ищется ПЕРВЫМ — пункт 5 владельца: репо-объект
workbench/runtime/llama.cpp оказался клоном canonsim-репо, пак не
может на него полагаться).

1. **station_m4_setup.bat/.py** (шаг 1): пинованный ОФИЦИАЛЬНЫЙ
   **b11541** `llama-b11541-bin-win-cuda-12.4-x64.zip` (265 224 711
   байт, sha256 `c5ccdd22…` — сверено живой загрузкой этой сессии;
   b11541 = НОВЕЙШИЙ nightly на 2026-10-10, несёт `/v1/systemone`
   живьём — строка найдена в бинаре ДО запуска, затем доказана
   живыми вызовами) + **НОВЫЙ ОФИЦИАЛЬНЫЙ cudart-КОМПАНЬОН**
   `cudart-llama-b11541-bin-win-cuda-12.4-x64.zip` (391 443 627
   байт, sha256 `8c79a9b2…`): ровно ТРИ DLL, которые кит iter-355
   развязывал руками по redist-архивам NVIDIA (cudart64_12 /
   cublas64_12 / cublasLt64_12) — теперь один официальный зип;
   лестница резолюции сохранена (видимы системе > компаньон >
   тулкит). Идемпотентен (sha256-skip), офлайн-путь (локальный
   архив рядом со скриптом, неверный хэш = громкий отказ),
   распаковка в `llama.cpp/` ПАКА, **побайтовая проверка
   `/v1/systemone` в бинаре до «done»** — неправильный билд не
   доезжает до батареи никогда. `--swap`/`--restore` — форма Б
   кита, теперь ВНУТРИ пака (см. §C);
2. **station_m4_doctor.bat/.py** (шаг 2): **доктор моделей** —
   каждый `*.gguf` в workbench/runtime/models читается ЛОКАЛЬНО
   (собственный GGUF-парсер: заголовок + метаданные, без спавна,
   без полной загрузки; закон полного потребления массивов выучен
   живьём на 50368-токенном токенизаторе Laya — частичное чтение
   рассинхронизирует все последующие ключи) и вердиктируется:
   `decision:<тип>` (один из пятёрки llama.cpp: laya/julia-1/lev/
   openjev/kev — годен для R-руки), `causal-lm` (генеративная),
   `broken` (заглушка/битая конверсия; отдельный оверлей для
   Kev-4B: файл без kev-метаданных = устаревшая конверсия →
   пинованная перекачка). Плюс вердикт движка (наличие сервера +
   `/v1/systemone` в бинаре + версия) и **диагноз папки
   runtime/llama.cpp** (клон репо = НЕ билд — случай владельца;
   source-checkout; пусто). Плюс пинованные фетчи:
   `--fetch-laya` (450 МБ, md5 + метаданные), `--fetch-kev`
   (4.5 ГБ, размер + 428 тензоров + kev-тип — датум iter-356 §D),
   `--fetch-qwen` (484 МБ, md5 — ультралайт для G-руки). Пишет
   doctor.json;
3. **station_m4_probe.bat/.py** (шаг 3) — **THE R BATTERY**
   (ядро, §D); 4. **m4_analysis.py** (отчёт, §E); 5.
   **m4_units.py** (юниты); 6. **README_RU.txt** (руки владельца);
   7-9. три .bat; 10. sandbox_report.txt (полный CPU-отчёт
   валидации — для сверки с GPU-прогоном владельца).

## B. Почему пин b11541, а не b11538 кита

Единственная причина пина b11538 в iter-355 — байт-сопоставимость
с CPU-прогоном станции (та же полоса, одна переменная: устройство).
У m4 НЕТ предыдущего прогона для сопоставления — батарея новая;
владелец явно попросил «последнюю для работы с cuda». b11541 =
новейший nightly на момент сессии, та же генерация, что несёт
`/v1/systemone` с окна b11538. Билды кита и пака СОСУЩЕСТВУЮТ
(пак ставится в свою папку; `--swap` в репо — только по вызову
владельца) — M3 GPU re-run остаётся самостоятельной формой.

## C. Сломанная папка владельца — диагноз и лечение (пункт 5)

Состояние станции (2026-10-10, из git-вывода владельца):
workbench/runtime/llama.cpp = **клон canonsim-репо** (origin =
vudirvp-sketch/canonsim, HEAD 07cf7f3) с ~20 exe-файлами в корне.
Лестница обнаружения m3 нашла бы exe в корне — но это не билд
llama.cpp (нет CMakeLists/README исходников llama.cpp). Формы:

- **диагноз доктора**: «NOT A LLAMA.CPP BUILD — a canonsim repo
  clone (git present, canonsim markers present)» + имена exe +
  имя фикса — ГРОМКО, в таблице и в doctor.json;
- **--swap**: текущая папка ЦЕЛИКОМ (включая .git) уезжает в
  sibling `llama.cpp.bak-<ts>` — ничего не удаляется — затем
  пинованный билд ставится плоско в корень (llama-server.exe в
  корне = первая позиция лестницы обнаружения); `--restore`
  возвращает 1:1;
- валидировано живьём на ВОСПРОИЗВЕДЁННОЙ сломанной папке
  (клон + три exe в корне): swap → диагноз + бэкап + установка;
  restore → возврат; повторный swap; git status репо чист на
  каждом шаге (runtime — gitignored).

## D. THE R BATTERY — рука R (пункт 4: семантика классификатора)

Каждый say-цикл корпуса (те же 51 цикл через НАСТОЯЩИЕ двери —
Simulator + Mediator + ParserDoor, общий леджер, форма m2/m3):

1. **ОДИН вызов** `POST /v1/systemone`: state = {message, scene:
   location + present} (компактный живой фолд) + questions:
   **action** (choice по 16 интентам пака, критерии = label+notes
   из actions.json), **target** (choice по ЖИВЫМ существам
   snapshot'а — тот же закрытый набор, что даёт грамматика G),
   **is_modeled** (noul — гейт валидности), **risk** (score:
   safe/bold/reckless);
2. **детерминированная дверь** собирает интент-документ ТОЛЬКО из
   известных ключей: top-action; kind-aware выбор цели (лучшая по
   вероятности сущность, чей kind соответствует requires действия;
   **двойственная форма take**: item-цель ИЛИ текстура — текстура
   едет в FIELD, не в target, ровно форма корпуса); поля —
   фиксированная политика по умолчанию (wait.ticks=30,
   steal.method=distraction — единственный легальный ключ methods);
3. **НАСТОЯЩАЯ ParserDoor** валидирует и коммитит (или честно
   отвергает — `intent_rejected` это датум, не сбой).

Классификатор РОУТИТ, никогда не коммитит. Два исполняемых
доказательства едут в каждом прогоне: **INVENTION LEDGER** (0
ключей вне множеств пака — галлюцинация документа ФИЗИЧЕСКИ
невозможна) и `output_tokens = 0` на каждом вызове
(негенеративность). G-рука-контроль (форма m3 байт-в-байт,
опционально `--no-g`), RU-полоса (12 строк с ручным золотом),
det-мини, crash-zip, возобновляемые стадии, device-class гейт
ВНУТРИ пака (строка v4 из iter-355 §D закрыта: пре-чек
--list-devices, громкий отказ без CUDA, cuda_gate.json).

## E. Отчёт (m4_analysis) — что читает владелец

CENSUS (классы m3 дословно + `gate_blocked`/`gate_false_positive`
— работа гейта) · INVENTION LEDGER · LATENCY LEDGER (стена вызова
vs G-parse; input_tokens; output_tokens) · **GATE SWEEP** — новый
инструмент: сырой `gate_p` пишется в каждую запись, отчёт
показывает долю прошедших гейт золотых интентов при порогах
0.5/0.4/0.3/0.2/0.1/0.0 БЕЗ перезапуска — порог валидности как
измеряемая ручка, не закон · RU BAND · DET · таблица по циклам.

## F. Живая валидация (§13.1-класс, насквозь)

Сэндбокс: b11541 ubuntu-x64 (та же генерация, что win-билд;
`/v1/systemone` в бинаре + живые вызовы) × Laya-Q8_0 (449 397 600
байт, md5 `fb91a5f2…`, метаданные сверены: 201 тензор,
decision.type=laya, калиброванные температуры) × Qwen3-0.6B-Q4_K_M
(484 219 808 байт, md5 `541151b1…` — байт-в-байт пин iter-355):

- **юниты**: census (дословно m3), вопросы+сборка+kind-aware цель,
  изобретения (включая негативный тест: подсунутый «teleport/
  atlantis/magic» пойман по всем трём осям), двойственная форма
  take-texture (текстура через живой narrator-бит медиатора), форма
  RU-полосы — ALL GREEN;
- **доктор**: вердикты по трём классам живьём (decision:laya /
  causal-lm / broken-Kev-стаб + FIX-строка) + диагноз движка +
  диагноз сломанной папки (§C);
- **swap/restore** 1:1 на воспроизведённой сломанной папке;
- **ПОЛНАЯ БАТАРЕЯ насквозь** (smoke + полный прогон, все стадии
  зелёные; heal-лестница сработала живьём — мёртвое соединение
  посреди G-руки, рестарт, прогон продолжился);
- **живые дефекты, найденные и закрытые валидацией** (закон
  iter-349 §C): (1) контракт emit-call — R-рука умирала на
  «no parse call awaits a reply», пока вызов emit не встал перед
  systemone-роутом; (2) форма take-texture — target у двойственной
  формы делает класс full недостижимым (census требует
  бестаргетную форму).

## G. Честные числа полного CPU-прогона (база для сверки с GPU)

42 say-цикла (полный корпус): **0 изобретений** на 42 собранных
документах; **output_tokens = [0]** везде; det идентичен обеим
рукам; R-вызов med 3.30 с против G-parse 4.57 с (CPU; полоса
3080 Ti = десятки мс по карточке Laya). R-ценз (Laya zero-shot
EN): full 14.3% RAW, kind 11.9%, **gate_blocked 57.1%**,
gate_fp 7.1%; развёртка гейта 22.6%@0.5 → 74.2%@0.1 → 100%@0.0 —
zero-shot база ≈ шанс, ровно карточный датум (0.362 → 0.766 после
файнтюна: прыжок за корпусом таверны, дверь остаётся валидатором).
Исходы двери честные: intent_rejected 6 (мир отверг неверные
маршруты), одна location_burned_out — **T4-класс zero-shot валидации
измерен живьём** (уверенно-неверный arson на атмосферной прозе
РЕАЛЬНО коммитится; гейт+файнтюн — адрес). RU-полоса: уверенно-
неверное семейство («подошёл заговорить» → coerce — датум T2
iter-356 воспроизведён; «выйду во двор» → steal — лексическое
заражение) — RU-полоса на Kev = главный вопрос станционного
прогона.

## H. Вердикты по моделям владельца (пункт 4, инструментально)

- **Kev-4B-Q8_0.gguf** (копия станции): broken (нет kev-метаданных,
  426≠428) → `--fetch-kev` перекачивает пинованно и проверяет
  метаданные после загрузки;
- **Decision-2.0-Nox-4B-Q8_0.gguf**: доктор скажет по факту
  (нет `*.decision.*` в метаданных → causal-lm: НЕ классификатор
  для systemone, только генеративное использование);
- **decider-4b-v2.1-Q8_0.gguf** (Mapika): вне пятёрки llama.cpp,
  systemone-поверхности нет сегодня (iter-356 §D) — доктор
  вердиктирует честно по метаданным.

## I. Верификация и доставка

- `PYTHONHASHSEED=0 python -m pytest -q` — 2644 passed, 1 skipped
  (та же строка, что iter-356; чистый клон — три красных на
  загрязнённом мной workbench/runtime при первом прогоне были
  МОИМИ валидационными деревьями под сканом тестов, после чистки
  чисто); `ruff check .` clean; `python scripts/docguard.py` clean;
  `python scripts/topology.py --check` clean; INV-1..5 не тронуты
  (нулевой код репо);
- Дельта-архив против BASE `07cf7f3`: attachment +
  tmpfiles-ссылка + md5 (§12.2); пак — отдельный зип (Rule 9).

## J. Дальше

1. **Станционный прогон владельца** (три двойных клика; m4_*.zip
   обратно): GPU-полоса R vs G + **Kev на RU-полосе** — главный
   вопрос доверия (3080 Ti: ожидай десятки мс на вызов);
2. Чтение → решение runtime-promotion (R как продакшн-роут против
   H/G) + M2-решение + M3-решение — всё композируется;
3. Стоячие вызовы: replay-UI, W8, P1/P2/P3, lab-composite-1.

## K. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-357-m4station-report.md
git status --short
git commit -m "iter-357-m4station: THE M4 STATION PACK (11 files outside the repo per Rule 9) - the owner's five points («нормально проработай скрипт»: the 3080 Ti band, the script-installed LATEST CUDA llama.cpp, the models folder, the Kev/Decision/decider CLASSIFIER semantics, the broken local runtime/llama.cpp) mapped onto the pack's four tools: (A) the PINNED INSTALLER b11541 win-cuda-12.4 + the NEW official cudart companion (the three DLLs the iter-355 kit hand-resolved, now one zip) + the /v1/systemone byte-check; (B) the SWAP form --swap/--restore - the owner's broken runtime folder (a canonsim repo CLONE with stray exes) diagnosed loud + healed whole-folder, nothing deleted; (C) the MODEL DOCTOR - every *.gguf verdicted locally (decision:<five>/causal-lm/broken; the pinned fetches incl. the Kev re-download); (D) THE R BATTERY - ONE /v1/systemone call per cycle (the 16 actions + the LIVE scene nouns + the noul gate + the risk) -> the deterministic door (kind-aware target, take's dual item|texture form) -> the REAL ParserDoor - the classifier ROUTES never commits; the G control + the RU band + det + the crash zip + the resumable stages + the DEVICE-CLASS GATE INSIDE the pack (iter-355's v4 row closed); (E) the report - the R census + THE INVENTION LEDGER + THE GATE SWEEP; VALIDATED LIVE end-to-end (b11541 ubuntu x Laya x Qwen3-0.6B through the real doors; the heal ladder fired live; swap+restore 1:1 on the reproduced broken folder; honest zero-shot numbers as data: 0 inventions/42 docs, output_tokens=[0], gate_blocked 57% with the sweep 22.6%@0.5->74%@0.1, the RU band confidently-wrong (iter-356 T2 reproduced), R 3.3s vs G 4.5s CPU); two live defects found and closed by the validation (the emit-call contract, the take-texture targetless form); zero repo code)"
git push
```

**Done:** пак собран и валидирован живьём насквозь; пять пунктов
владельца закрыты инструментально; райдеры прошли чеки.
**Not done:** станционный GPU-прогон (за владельцем — три двойных
клика, ~650 МБ пинованных загрузок, затем 5-10 минут); RU-полоса
на Kev (нет модели в сэндбоксе — строка вилки).
**Next:** чтение вернувшегося m4_*.zip; затем решения (R/H/G,
M2, M3) за гейтом runtime-promotion.
**Active KIs:** KI#113 (test_lab, как в STATUS).
