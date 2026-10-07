# iter-338 · occidx — ИНДЕКСНАЯ АТРИБУЦИЯ OCC-ОКНА: обход пишет только писателей читаемых пар (закон индекса); закон A/B-эквивалентности на КАЖДОМ вызове + побайтовая A/B; стена whole-руки 51.64 → 4.36 с на 100y (11.8×), **whole-килогод 3 818 → 43.5 с (87.7×), T1 HELD 45 000 433 × 2**; килогод = канон iter-335 побайтово; occ_refold 81.7% → 7.3% профиля

**Вызов владельца:** действующая директива «продолжай работы, открывай
то что сейчас важнее всего сделать, логичнее и качественнее на
долгосрок» — строка STATUS Next п.(1), названная первой в NEXT-линиях
iter-335/336/337: «фикс occ-окна whole-протокола (индексная
атрибуция, буква B7)» — квадратичный член стены, измеренный iter-335
(occ_refold 81.7% профилированной стены whole 100y) и оставленный
h9 как «остаток B7».
BASE_COMMIT: `2e54d39` (iter-337, чистое дерево — база 2616+1 green).
Задача ID: `iter-338-occidx`. **R3** (кросс-граничное: intent + loop +
инструмент; PCC-запись §G — DECISIONS на капе 30/30, прецедент
iter-332/337).

**llama.cpp не устанавливался** — строка LLM-free: индекс записи и
обход атрибуции, чистая инженерия read-side.

## A. Что сделано

### A.1 Закон индекса (механизм)

Вердикт атрибутивного преусловия — функция значений ПРОЕКЦИОННЫХ пар,
которые оно читает (плюс pack/world/intent — константы внутри одного
обхода: обе формы вычисляют через одни и те же живые объекты).
Событие, не пишущее НИ ОДНОЙ читаемой пары, не может перевернуть
вердикт — значит, первое ломающее событие обязано быть среди
писателей. Обход посещает ТОЛЬКО их.

Три части:

1. **Таблица read-pairs** (`core/intent.py::OCC_READ_PAIRS` +
   `STATIC_TESTS` + `precondition_read_pairs`) — ДВОЙНИК семейства
   тестов, рядом с ним, никогда вторая истина: 10 обработчиков
   объявляют пары (позиции same_location/adjacent_to/location_of,
   carrier у carried_by/uncarried/carries_flagged, carrier+позиции
   сканов flagged_accessible, relations.axis, account.kind с holder-
   формой, layer.spot по статичному списку пак); 6 тестов —
   pack-статичны (kind/flag/field_in/field_nonempty/has_field/
   texture_noun — их чтения едут по PACK-записям, не по проекции);
   windowed-семейство отсутствует по фильтру атрибуции.
   **Полнота — закон** (test_occidx): каждое имя PRECONDITION_TESTS —
   ровно одно из {таблица, статик, windowed}; новый тест объявляет
   пары или статичность, никогда ни то ни другое.
2. **Индекс записи** (`core/loop.py::_occ_index`) — `(entity, prop) →
   возрастающие индексы событий`, каждое писавшее ту пару; `_commit` —
   единственный писатель, resume-цикл — единственный перестройщик
   (pattern `_last_change` в полной истории, D-050/B7).
3. **Индексный обход** (`occ_breaking_cause(changes=…, stats=…)`) —
   кандидаты = писатели читаемых пар в окне [seq, end); состояние
   вне читаемого множества держит снапшотные значения ПО ЗАМЫСЛУ
   (тесты их не читают); from_-проверка сохранена НА читаемых парах —
   чистая сеть закона индекса (на полном индексе не может сработать
   никогда; срабатывание = индекс и лог расходятся). Один шорткат:
   вердикт уже падает на стартовом состоянии и первое событие окна —
   не писатель → полный обход отвечает events[seq].id; шорткат
   точен. Default (`changes=None`) — точный старый полный обход
   (внешние вызовы, resume-путь вызова, тесты).

Честные метки (`stats`-поверхность + `Simulator.occ_stats` +
`cost.occ` в labrunner, по прецеденту cost.skip): calls / window
(база стоимости полной формы) / inspected (реально применённые) /
attributed.

### A.2 Фальсификатор строки — закон A/B-эквивалентности

`tests/test_occidx.py`, закон 1: шпион на `core.loop.occ_breaking_
cause` — КАЖДЫЙ вызов индексного пути повторяется точным полным
обходом (без снапшот-шорткатов, без индекса) — ответы РАВНЫ; батарея
невакуумна (вызовы > 0, атрибуции > 0, на whole-руке inspected <
window — ускорение реально). Побайтовая A/B (закон 2): та же
(seed, шаги) с индексом и без — логи побайтово равны. Резюм-закон:
та же split-resume форма вооружённо/выключенно — побайтово равны,
индекс = независимый фолд истории записи лога.

## B. Измерено

| форма | ДО (BASE) | ПОСЛЕ | закон |
|---|---|---|---|
| whole 50y seed 7 | 13.66 с | **2.22 с** | 6.15×; A/B bytes IDENTICAL |
| whole 100y seed 7 | 51.64 с | **4.36 с** | 11.8×; **md5 `508807a0…` ОБЕ руки** (51.02 с stripped in-session) |
| whole 100y профиль | occ_refold 81.7% (iter-335) | **7.3%** | per-call ×2.0 → **×1.02**; knowledge 0.0%; canon-neutrality HELD |
| whole 100y метки | — | calls 4 911 / window 18 341 200 / inspected 82 174 | **срез поверхности 223×** |
| segmented 100y | 4.78 с (iter-337) | 4.59 с | окна и были короткие; window 120 205 → inspected 6 576 (18×) |
| **segmented 1000y** | 46.44 с (iter-337) | 46.15 с | **md5 `a1d8f05b…` = КАНОН iter-335/337**, T1-grade |
| **whole 1000y** | 3 818.15 с (станция, α=1.91) | **43.52 с** | **87.7×**; события 82 757 = станционное число; **байты 45 000 433 = ТОЧНОЕ исполнение предсказания iter-336** (CRLF-арифметика: «the whole-kiloyear log would be 45,000,433 bytes on a LF platform» — измерено на LF); **T1 HELD md5 `7cbfb68a…` × 2** — глубочайший детерминизм-прогон за историю репо (whole-килогод двойным прогоном); метки: calls 49 162 / window 1 825 244 517 / inspected 828 230 (**срез 2 203×**) |

- **Локальная экспонента whole-руки 50→100y: 1.89 → 0.997** —
  квадратичный член мёртв, рука линейна; whole-килогод теперь ДЕШЕВЛЕ
  сегментированного (43.5 против 46.4 с) — штраф отложенной
  реализации исчез целиком.
- **2627 passed + 1 skipped**, ruff clean, docguard clean,
  topology --check clean (Python 3.12.14, env pin; INV-1..5 не
  тронуты, ЛОГ не тронут; НИ ОДИН тест не удалён и не ослаблен —
  11 добавлено, 4 механических re-pin под 4-tuple run_world).

### B.1 Побочная находка — KI#114 (пре-существующая, НЕ этой строки)

Первая редакция резюм-закона пинила split-vs-uninterrupted
побайтово — и нашла расхождение: farthest-сплит ПОСЛЕ ожидания
входит следующий шаг на +16 тиков позже непрерывной формы
(ev_0210 t=1036802 vs 1036818): сегмент дренится до конца (follow-up
цепочка тянет часы за завершение ожидания), курсор пинит
пост-дрейн тик, следующий шаг входит там; непрерывная форма кормит
шаг НА тике завершения, до follow-up. **Воспроизведено с полностью
выключенным occ-1** (stripped-обезьянник) — пре-существующий дефект
на HEAD; tavern-корпус резюма его не ловит (его сплиты — не после
ожидания). KI#114 открыт в STATUS; фикс — отдельная строка
(семантика очереди/ленты, свой R3), никогда молча.

## C. Файлы

core/intent.py (OCC_READ_PAIRS + STATIC_TESTS + precondition_read_
pairs + индексный обход + stats-поверхность), core/loop.py
(_occ_index: init/_commit/resume + вызов с changes/stats +
occ_stats), scripts/labrunner.py (cost.occ + 4-tuple run_world),
tests/test_occidx.py (новый, 11 законов), tests/test_lab.py +
tests/test_h9.py (механические 4-tuple re-pins), docs/TASKS.md
(строка occ-1 + леджер, iter-328 evicted), STATUS.md (заголовок +
Next + KI#114), worklog.md (запись iter-338, iter-328 evicted),
этот отчёт — 10 changed/created (3 код + 3 тест + 4 райдера).
NO test deleted or weakened — 11 добавлено, 4 механических re-pin.

## D. Чего НЕ сделано (намеренно)

- **Фикс KI#114** (резюм-граница после ожидания) — своя строка:
  семантика feed-at-completion vs feed-at-resume-tick, чужой R3,
  никогда не в этой.
- **Проп-уровневое расширение entity-фильтра** — не нужно: парный
  уровень уже даёт срез 223×–2 203×; второй уровень гранулярности —
  при появлении измеренной потребности (AGENTS §2.8).
- **Индекс для внешних вызовов occ_breaking_cause** — внешние
  вызовы едут точным полным обходом (default); индекс — привилегия
  владельца цикла, никакого второго строителя.

## E. NEXT

1. Стоящие вызовы владельца в порядке: Lab E02/E31, M2, replay-UI,
   W8, фронтовые P1/P2/P3.
2. KI#114 — строка фикса резюм-границы (по вызову владельца).
3. Станционный кросс-чек whole-килогода под индексом (43.5 с —
   теперь и станционная форма дешёвая; по вызову владельца).

## F. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/intent.py core/loop.py scripts/labrunner.py tests/test_occidx.py tests/test_lab.py tests/test_h9.py docs/TASKS.md STATUS.md worklog.md docs/iterations/iter-338-occidx-report.md
git status --short
git commit -m "iter-338-occidx: THE INDEX-BASED OCC WINDOW ATTRIBUTION (B7) — the walk visits only the window's writers of the read pairs (the twin table in core/intent.py, the _occ_index in the loop); THE A/B ATTRIBUTION-EQUIVALENCE LAW held on every call + byte-identity both arms; the whole-arm wall 51.64->4.36s at 100y (11.8x, alpha 1.89->0.997), THE WHOLE KILOYEAR 3818->43.5s (87.7x, T1 HELD 45,000,433 x2, the iter-336 byte prediction landed EXACTLY); the segmented kiloyear md5 = the iter-335 canon; occ_refold 81.7%->7.3% of the profiled wall; +11 laws (test_occidx) + cost.occ labels; KI#114 opened (pre-existing resume-boundary drain divergence, found by the law, reproduced with occ-1 stripped)"
git push
```

## G. PCC (R3 — the compact record, AGENTS §2.9)

- **intent**: kill the whole-arm OCC quadratic member (B7's letter —
  every read surface index-based, never a log scan): the
  deferred-realize law made the attribution window [seq, end)
  horizon-long and the per-event re-check walk the measured wall
  (occ_refold 81.7% of the whole 100y profiled wall, per-call ×2.0,
  iter-335); the fix keeps the attribution's semantics EXACT while
  visiting only the window events that write a pair the intent's
  attributable tests can read.
- **invariants**: INV-1 (the walk is read-side only — no event, no
  log byte, no queue entry changes; the falsifier is byte-identity,
  held at 100y whole both arms and at the kiloyear both protocols);
  INV-2 (the index is derived bookkeeping over committed
  state_changes — zero entropy, rebuilt deterministically at resume;
  no draws, no clocks, no iteration-order surface: candidates are
  sorted); INV-3 (the twin table carries mechanic words only —
  position/carrier/relations/account/layer prefixes; the stoplist
  corpus green); INV-4 (untouched — no network surface); INV-5 (old
  logs never edited; the walk writes nothing).
- **delta**: core/intent.py (+OCC_READ_PAIRS, +STATIC_TESTS,
  +precondition_read_pairs, +the changes/stats params, +the indexed
  walk `_indexed_window_walk`), core/loop.py (+_occ_index maintained
  at _commit and rebuilt at resume, +occ_stats, the completion call
  passes changes+stats), scripts/labrunner.py (the 4-tuple +
  cost.occ), tests/test_occidx.py (+11 laws), tests/test_lab.py +
  tests/test_h9.py (mechanical 4-tuple re-pins).
- **verification**: the A/B attribution-equivalence law (every call:
  index answer == full-walk answer — 650 calls at 10y both
  protocols in-session, plus the test battery at 2y both protocols
  non-vacuous); the byte-identity A/B (2y whole in-test; 100y whole
  md5 `508807a0…` both arms measured in-session at 51.02 s stripped);
  the segmented KILOYEAR md5 `a1d8f05b…` = the iter-335/337 canon;
  the whole KILOYEAR T1 HELD (md5 `7cbfb68a…` × 2, 45,000,433 B —
  the iter-336 LF-platform byte prediction landed exactly); the
  twin-completeness table law; the twin-agreement property over all
  6 committed packs × every action × seeded non-read mutations; the
  resume rebuild law (index == independent fold of the log's write
  history; armed==stripped through the split); the unit grid
  (break / no-break / break-at-snapshot / repair-at-seq-then-rebreak
  / empty window / static-conds); the full corpus 2627+1 green,
  ruff/docguard/topology clean.
- **provenance**: the STATUS Next item (1) — the row named first by
  iter-335/336/337's NEXT lines; the owner's standing «продолжай
  работы, открывай важнейшее на долгосрок» directive; B7's letter
  (CONTRACTS §12) the cost law's own form.
- **runtime**: the index ride is unconditional in the loop (the
  defaults keep every external caller on the exact full walk); the
  index's memory is O(committed state_changes) — one int per change,
  ~2 MB at the kiloyear against the 45 MB log; resume rebuilds it
  from the log in the same pass as _last_change.
