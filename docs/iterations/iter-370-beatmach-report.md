# Отчёт итерации iter-370 — beatmach (статичное разрешение beat-механики)

> На постоянной директиве владельца «продолжай работы, открывай то,
> что сейчас важнее всего сделать, логичнее и качественнее на
> долгосрок. я разрешаю» открыта голова рейтинга iter-364 — семейство
> beat-механики. Класс преобразований — iter-362 (парс-онс мемо +
> слитые примитивы, байт-идентичность + законы-оракулы).

**Класс риска:** R3 (ядро, кросс-модульно; компактная PCC-запись —
**D-253** в DECISIONS, 33/35).

## A. Что было измерено до кода (тот же протокол, что iter-362)

cProfile h32 (S=4/H=32, seed 7, сегментированные 10y, якорь
loc_s0_square, директоры off, скип on), первозданный HEAD сессии
(после iter-369) — стенa 18.58 с (непрофилированная), члены
профильной стены:

| Член | Доля | Внутри (cProfile, callee-декомпозиция) |
|---|---|---|
| skip_probes | 33.1% | `urgency_scan` 11.19 с: **`_build_intent` 2.51 с / 939K аллокаций проб** + `first_failing` 3.55 с / 939K + `urgency_rolls` 0.89 + имена f-строк 0.18; `next_decay_tick` 5.40 с: per-pair isinstance 1.44 + `_clamp` 0.65 + items 0.15 |
| beat_rolls | 16.2% | `urgency_intents` 8.13 с: **машинерия `with bank.assure(...)` 3.18 с** (contextlib enter/exit/helper на 939K пар) + `randint` 2.16 + имена 0.18 + список-копии |
| decay_walk | 15.4% | `decay_drafts` 7.73 с: **per-(NPC,ось) переразбор конфига**: isinstance 1.47 + `items()` 0.16 + f-строки имён пропов + **`pack.rules["relations"]["scale"]` ПОДЪЁМ ВНУТРИ ОСЕВОГО ЦИКЛА** + `_axis_deltas` 1.35 |

Вывод до кода: статичные издержки (аллокации, f-строки, переразбор
неизменяемых данных пакета, скоуп-машинерия) — мусор по определению;
канон-нейтральны по построению в форме iter-362.

## B. Изменение (7 файлов кода + 4 тест-файла)

1. **`core/rng.py` — `RngBank.family_randint(name, lo, hi)`**: слитый
   семейный дроу. Закон вложенности — инлайн-клауза `assure` (тот же
   текст, та же громкость на нарушение); счётчиковая арифметика —
   `randint`'а (то же слово с той же позиции, тот же инкремент);
   `_active`/`_assured` не тронуты — дроу маршрутизируется ИМЕНЕМ.
2. **`core/urgencies.py` + `core/factions.py` — мемо спеков**:
   `_UrgencySpec`/`_FactionSpec` несут предвычисленные `stream`
   (f-строка имени) и `probe` (IntentData с теми же id/kind/actor/
   target/fields/based_on_event_seq=0, что `_build_intent` вычислял
   на каждом вызове). Скан и волк читают их; мёртвые
   `_build_intent`-хелперы удалены. Замороженная проба ОБЩАЯ для
   скана и волка — луп штампует `based_on_event_seq` через
   `dataclasses.replace` (новый объект), пути мутации нет.
3. **`core/states.py` — `decay_axes(pack)`**: статичная таблица осей
   `(ось, имя-пропа, rate, знак, ceil(360/rate))`; обе прогулки
   (`decay_drafts`, `next_decay_tick`) читают её — параметр
   `axes=None` (прецедент `specs=None`), луп мемоизирует на
   инициализации (`self._decay_axes`). Мёртвый `_axis_deltas` удалён;
   `scale` поднят к голове вызова (был в осевом цикле).
4. **`core/loop.py`**: мемо `self._decay_axes` + прокидывание в три
   места вызова.
5. **`core/intent.py`**: аннотация `first_failing.preconditions`
   честно `Sequence` (кортежи едут на спеках; 939K `list()`-копий
   исчезли; тело только итерирует — поведение то же).

## C. Стена: до/после, один инструмент, один протокол

Labrunner (НЕпрофилированная стена; канон-нейтральность HELD в
обоих прогонах — профильные байты == непрофильным):

| | до (HEAD iter-369) | после (iter-370) | |
|---|---|---|---|
| стена h32 10y | **18.58 с** | **12.51 с** | **×1.48** |
| события | 25 859 | 25 859 | идентичны |
| md5 лога | `07e924cbe6a3f05e9991e083ed004610` | тот же | **байт-в-байт** |

Профильные члены (cProfile, та же пара прогонов):
`urgency_scan` 11.19 → 7.45 с; `urgency_intents` 8.13 → 3.97 с;
`decay_drafts` 7.73 → 3.26 с; `next_decay_tick` 5.40 → 2.65 с;
`first_d100_hit` 2.21 → 2.16 (без изменений — коллективный обход
iter-362 уже оптимален). **Beat-механика: 64.7% → 47.8% стены.**

Разреженный конверт (farstead 100y, seed 7, сегментированные):
0.37 → 0.33 с, md5 `4adcd95b…` идентичен — **регрессии нет** (None-форма
обхода не дороже прежней). Пара h3 (S=4/H=3): md5 идентичен.

**Экспоненты плотностной оси** (h3→h32, per-call cum, оба прогона
этой сессии): decay_drafts ×11.85 → **×8.1**; urgency_intents ×8.94 →
**×7.1**; urgency_scan ×6.22 → **×4.8**; next_decay_tick ×10.7 →
**×7.8**. Честный остаток: прогулки остаются популяционно-линейными
на вызов (чтения словарей + арифметика) — пол дисперсии экспонент;
индекс/куча лендингов decay — отдельная будущая строка.

## D. Законы (+4; все существующие — фальсификаторы, не тронуты)

- **`test_core.py`** — `test_family_randint_is_the_assure_form`:
  оракул эквивалентности (те же слова в том же порядке, те же
  счётчики, отпечаток substantive нетронут; закон вложенности equally
  loud — семейное имя внутри чужого скоупа отказывает, неизвестное
  имя громко).
- **`test_states.py`** — `test_decay_axes_match_the_per_pair_resolution`:
  линейный оракул по ВСЕМ шести коммитнутым пакам (та же форма, что
  закон индекса kind_of из iter-362): те же оси в том же порядке, те
  же rate/знак/ceil(360/rate).
- **`test_urgencies.py` / `test_factions.py`** —
  `test_the_parse_memos_match_the_derived_forms`: каждая спека's
  stream == имя-строитель, probe == выведенная форма (id
  `urgency_<seq>`/`faction_<seq>`, actor, target, fields,
  based_on_event_seq=0), requires == кортеж записи.
- Существующие законы — главные фальсификаторы: T1-батарея (байт
  против золотых фикстур — известный env-сет 3.12.15), h9-законы
  (A/B скипа, scan-vs-walk, коллективный обход, grid-арифметика),
  покс-пакеты — все зелёные на новом коде.

## E. Верификация

- `PYTHONHASHSEED=0 pytest -q` → **2626 passed + 27 failed + 1
  skipped**; множество падений продиффено против pristine-базлайна
  сессии (взят ДО изменения) — **ИДЕНТИЧНО** (известный T1 env-сет);
  +4 новых закона. Одна флейк-вспышка `test_the_wall_growth_and_
  labels_law` на первом пост-инсталл прогоне полной батареи (класс
  KI#113): в изоляции зелёный, 3 полных повтора test_lab зелёные,
  второй полный прогон зелёный — записи KI#113 дополнена, новый KI
  не открыт (класс уже стоит).
- `ruff check .` clean; `python scripts/docguard.py` clean;
  `python scripts/topology.py --check` clean; digest парсится.
- md5: h32 `07e924cb…` / farstead `4adcd95b…` / h3-пара — все
  идентичны до/после; канон-нейтральность прибором HELD.

## F. Риски и честные границы

1. **Общая замороженная проба** (скан и волк делят объект IntentData):
   закон — «IntentData frozen+slots, пути мутации нет; луп штампует
   replace()'ом». Закреплено мемо-законом (поля равны выведенной
   форме) + всей байт-батареей.
2. **`family_randint`** семантически ≡ assure+randint для каждого
   имени, где assure легален (включая substantive) — закон-оракул
   пинит эквивалентность, а не только семейный случай; поверхность
   названа по назначению (семейные волки), не по ограничению.
3. **Экспоненты остаются ≥ ×7**: статичное разрешение срезало
   популяционно-пропорциональную константу, но прогулки честно
   линейны по населению на вызов. Следующая голова названа:
   **чтения гейтов `first_failing` внутри `urgency_scan` (7.45 с)** —
   кандидат-форма: мемо ответа гейта по замороженному состоянию
   (закон инвалидации назвать до кода); затем
   commit_knowledge_fold (4.41 с, ×6.7) и director_global_passes
   (4.99 с, ×2.5); индекс лендингов decay (куча) — большой R3 позади
   них.

## G. Дальше

M6-станционный прогон (сторона владельца); форма фикса KI#120 (зов
владельца); следующая measured-wall строка — гейт-мемо скана.

## Владельческий git-блок (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/rng.py core/urgencies.py core/factions.py core/states.py core/loop.py core/intent.py tests/test_core.py tests/test_states.py tests/test_urgencies.py tests/test_factions.py docs/DECISIONS.md STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-369-deccap-report.md docs/iterations/iter-370-beatmach-report.md scripts/docguard.py tests/test_docguard.py AGENTS.md docs/AGENT_NAVIGATION.md
git status --short
git commit -m "iter-369+iter-370: THE DECISIONS CAP RAISED 30->35 ON RESEARCH (D-252 - the citation scan found all 31 rows live-cited, zero removable; docguard+AGENTS+NAV synced; the guard red cleared) + THE BEAT-MACHINERY STATIC-RESOLUTION FAMILY (D-253, R3, the iter-362 class: family_randint the fused family draw + the spec stream/probe memos + the decay static axis table - zero canon bytes, the h32 md5 identical; the wall 18.58->12.51 s x1.48, the members cut 33-58%, +4 oracle laws)"
git push
```
