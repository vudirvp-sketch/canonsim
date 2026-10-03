# iter-311 · worldsuite — ингестия CANONSIM_AGENT_WORLD_SUITE_v1_0

**Класс риска:** R0 (только документы и архив; ноль изменений кода, паков,
канона; INV-1..5 не тронуты; LOG не тронут).
**Вызов владельца (2026-10-03, чат):** «изучи и обработай
CANONSIM_AGENT_WORLD_SUITE_v1_0.zip, что перенимаем и реализуем а что нет,
что истинно а что нет. куда "паркуем" результаты и данные с пака и почему.
ВАЖНО: я не хочу всю дорогу скидывать тебе вручную этот архив. можешь
устанавливать llama.cpp для работы и прочее окружение.»

## A. Что это за артефакт

Третья внешняя pack-ингестия репозитория (семья D-242: worldcontext
iter-277 → frontendweb iter-288 → methoddoc iter-292 → **worldsuite
iter-311, D-251**). Suite = синхронизированный двухслойный агентский
handoff-пак:

- `CORE_WORLD` v1.3 — **новый для репозитория слой**: кросс-трековые
  вопросы (семантическая эквивалентность, execution/scale, граница
  LLM/наблюдения, роутинг исследований);
- `WORLD_TRACK` v4.6 — мировая половина, прямое обновление уже принятого
  в iter-277 пака v4.5.

Целостность: 92 572 байта, 25 файлов, md5 `6b43aeb9b41c59c03dcb777424242000`,
sha256 `e8c969666c3cac5bed5a543352b8ce21efd52954f265b844c12cf74c7ffbfbec`.
Ингестия против HEAD `8e788a4` (iter-310).

## B. Что истинно (сверено с живым репо)

Каждое проверяемое заявление CORE_WORLD сверено с HEAD:

1. **W-стадии** — W1–W4 закрыты, W5 gate met, W6/W7 complete, W8 текущая
   (аудит готовности приземлён) — совпадает с
   `WORLD_TRACK_AGENT_CONTEXT.md` §9 / `WORLD_WORKPLAN.md`. ✓
2. **Субстрат** — восемь семейств причинности, пять meso-юнитов,
   account/economy-рука поверх существующих примитивов, композиционный
   прогон 2371 событие + 16 оракулов, I0-свидетельство зажигания мира,
   четыре таймлайна (люди/материалы/знания/обязательства), knowledge
   asymmetry, жанровые/человеческие бэнды — всё подтверждается §5
   контекста и `WORLD_TESTS.md` §9. ✓
3. **Resolver kinds** — список (observe, inspect, movement, converse,
   wait, pickup, drop, use_item, stealth_take, divert, ignite, flee,
   recuperate, coerce, account) сверен grep'ом по `core/resolvers.py`:
   все присутствуют (плюс `settle`, которого в «such as»-списке пака
   нет — не противоречие, список открытый). ✓
4. **I0 inventory** — три кандидата (runtime route writer; two-sided
   band condition; response-repertoire floor) дословно совпадают с §7
   контекста. ✓
5. **Честная граница аудита W8** (тоньше смысловой слой, тоньше
   годичный бэнд persistence, influence-check не оракул, часть
   доказательств документарная) — совпадает с записью iter-287. ✓
6. **Заявления о границах** — модель проекта (SIMULATOR→CANON,
   LLM→INTERFACE…), byte-identical replay, promotion gate,
   separate-track law — всё действующий закон репо. ✓

## C. Что не истинно / дрейф (записано, не «починено»)

По §11 (никогда молча не сводить противоречия):

1. **STALE (сам дисклеймится):** `WORLD_TRACK/01_CURRENT_EVIDENCE.md`
   описывает W5 как «асимметричный, открытый» (humor/heartbreak,
   fail-then-pass/40-80, runner grudge, shave). Пак запинен на
   iter-272; в репо эти вопросы закрыты диспозициями iter-266
   (closed-as-residue), rs-9/rs-10 приземлены iter-267/268, W6/W7/W8
   завершены после. Пак сам предупреждает «Do not infer that an older
   measurement table is the latest implementation state» — но наивный
   читатель может споткнуться; в дистилляции §10 контекста стоит
   указатель на актуального владельца.
2. **Внутренняя рассинхронизация бандла:** read-order в
   `CORE_WORLD/00_README.md` ссылается на `08_CHANGE_GATE.md` и
   `INDEX.md` — **этих файлов в архиве нет**; `CHANGELOG.md` покрывает
   только v1.1→v1.2 (состояние v1.3 — только в `PACK_META.json`);
   половины несут разные пины репо (WORLD_TRACK — iter-272,
   CORE_WORLD — ~iter-287+): «synchronized» означает разделение сфер,
   а не равенство снапшотов.
3. **Внешняя ссылка без артефакта:** «Cross-Domain Mechanism
   Transplantation — Agent Instruction.md» назван authority метода
   исследований, но в suite не входит — зафиксирован как ссылка,
   никогда не вендорится (тот же закон, что у D-246).

## D. WORLD_TRACK v4.6: новой субстанции нет

Дифф пофайлово с архивным v4.5: 9 из 10 файлов отличаются только бампами
версий и кросс-пак синхро-заметками (`02_DORMANT_REGIMES.md` полностью
идентичен). Ни новых доказательств, ни новых проб, ни новых предложений.
Вывод: **повторная ингестия мировой половины не нужна** — реконсилиация
iter-277 покрывает её целиком (закон «never re-ingest» соблюдён буква
в букву).

## E. Что перенимаем — и куда паркуем

| Материал | Диспозиция | Где живёт |
|---|---|---|
| Сам zip | ПАРКУЕТСЯ дословно (durable preservation) | `docs/worldbuild/archive/CANONSIM_AGENT_WORLD_SUITE_v1_0.zip` (md5/sha256-пин в `archive/README.md`) |
| Провенанс, уникальные сохранения (C1–C5/POC-контракты, capability index, sync matrix, караванный досье, пробы, карточки режимов) | Список «открывать только для этого» | `archive/README.md` |
| Кросс-пак граница (CORE ↔ WORLD_TRACK) | ПРИНИМАЕМ как ROUTING, не как власть | `WORLD_TRACK_AGENT_CONTEXT.md` §10 + `docs/worldbuild/README.md` (fence) |
| C1–C5 таксономия кросс-трековых гэпов | ПАРКУЕМ как owner-gated исследовательский ряд | `docs/TASKS.md`, ряд `core-1` |
| Дистилляция ингестии | Запись семьи D-242 | `docs/DECISIONS.md` (D-251) + `docs/blueprint/phases.md` §6 |
| Статус v4.6 как новейшая форма бандла | Бумп строки bootstrap | `WORLD_TRACK_AGENT_CONTEXT.md` (шапка) |

**Почему так:** ответ на «не хочу всю дорогу скидывать вручную» — сам
репозиторий. После применения владельцем delta-архива zip живёт в репо:
каждая будущая сессия/клон его несёт, а дистилляция (§10 + TASKS + fence)
гарантирует, что пак никогда не нужно повторно инжестить. Сессийный
upload-каталог эфемерен; архив репо — нет. Это третий экземпляр
требования D-242 («репозиторий один несёт достаточно контекста, чтобы
зип не перезагружали»).

## F. Что НЕ перенимаем

1. **Любую заявку на власть/вторую истину** — сам suite с этим согласен
   («Repository owner documents… remain authoritative»); закон D-242
   продолжает действовать.
2. **Runtime-механизмы C2/C3/C5** (компилированный/индексированный
   execution, history/replay scale machinery, батчинг) — гейт продвижения
   не удовлетворён (нет потребителя, нет измеренного нативного лимита, нет
   фальсификатора); сам пак помечает их «RESEARCH / POC ONLY». Tри
   кандидата I0 остаются непродвинутыми ровно как §7 контекста записывает.
3. **Переоткрытие W5/W6** из устаревших таблиц доказательств.
4. **Новый CORE-навигационный файл верхнего уровня** — стоянка «no
   second project memory» (AGENTS §2.8): роутинг несут AGENT_NAVIGATION,
   TASKS и README архива.
5. **Отсутствующие файлы (08/INDEX)** — дрейф записан, не сфабрикован.

## G. Окружение (llama.cpp)

Владельцем разрешена установка llama.cpp — **в этой итерации не
устанавливался**: iter-311 — R0 doc-only, inference-ряд не открывался.
Документированное место при живой надобности (iter-302/308 —
доказанный поток): drop-папка `workbench/runtime/llama.cpp/`,
обнаружение лаунчером, модели через `model.import`/`model.fetch`.
Базлайн верификации репо поднят с нуля: Python 3.12.14 (env pin),
`pip install -e ".[dev]"`, полный пакет зелёный ДО и ПОСЛЕ правок.

## H. Верификация

- `PYTHONHASHSEED=0 python -m pytest -q` — **2556 passed + 1 skipped**
  (идентично до и после: ноль изменений кода);
- `ruff check .` — clean;
- `python scripts/docguard.py` — clean (капы соблюдены: TASKS 593 строк,
  worklog 10 записей, DECISIONS 30 рядов — D-251 в компаунд-строке
  D-242/D-243/D-246/D-251);
- `python scripts/topology.py --check` — clean.
- Самопроверка дельты: список путей == `git status --porcelain -uall`
  против BASE `8e788a4` (см. блок Git ниже).

## I. Блок Git (owner-side)

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add docs/worldbuild/archive/CANONSIM_AGENT_WORLD_SUITE_v1_0.zip docs/worldbuild/archive/README.md docs/worldbuild/WORLD_TRACK_AGENT_CONTEXT.md docs/worldbuild/README.md docs/TASKS.md docs/DECISIONS.md docs/blueprint/phases.md STATUS.md worklog.md docs/iterations/iter-311-worldsuite-report.md
git status --short
git commit -m "iter-311-worldsuite: the CANONSIM_AGENT_WORLD_SUITE_v1_0 ingestion (D-251) — the suite archived verbatim, the C1-C5 taxonomy parked as core-1, the cross-pack boundary as routing"
git push
```

## J. Риски и следующее

- Риск: наследие двух паков в одном архиве (v4.5 + suite) — закрыто
  README архива (какой что уникально сохраняет); мировая половина
  suite НЕ удалена, хотя и эквивалентна v4.5: дословное сохранение
  важнее экономии 92 КБ.
- Следующее — вызов владельца: (1) мир-трек: оставшиеся ряды W8;
  (2) исследовательская семья `core-1` открывается только по
  nameable-consumer вызову; (3) живой inference-ряд (llama.cpp в
  runtime-раскладке) — по запросу.
