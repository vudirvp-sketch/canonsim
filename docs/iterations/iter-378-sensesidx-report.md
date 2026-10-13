# iter-378 · sensesidx — ТРЕТЬЯ ГОЛОВА СТОЯЩЕГО ПРИКАЗА ЗАКРЫТА: ИНДЕКС ЧУВСТВ ДИРЕКТОРА (класс iter-362, нуль канон-байт) — стена h32 10y 11.37 → 9.57 с (×1.19), член director_global_passes 5.07 → 0.02 проф. с (16.1% → 0.1%), per-call entropy теперь НЕЗАВИСИМ ОТ ПОПУЛЯЦИИ

**Вызов владельца (стоящая директива, дословно):** «продолжай
работы, открывай то что сейчас важнее всего сделать, логичнее и
качественнее на долгосрок. я разрешаю.» — строка STATUS Next называла
третью голову в точности: `director_global_passes` (5.06 профильных
с; кандидат-форма: индекс подозрения/угроз НА ПУТИ КОММИТА, класс
iter-362 «O(1) id→kind»; закон KI#16 ограничением дизайна).

**BASE_COMMIT:** `e5b095af16ed2c54670d3304a06049c37560e0af`
(HEAD iter-377, снят до любой правки).

**Класс риска: R3** (ядро: два модуля поведения + тесты + инструмент;
нулевые канон-байты по закону md5; PCC-строка D-255 — 35/35, НА КАПЕ
D-252).

## A. Измерение ПЕРЕД кодом (тот же протокол, что iter-364/375)

cProfile h32 (S=4, H=32, seed 7, сегментированные 10y, якорь
loc_s0_square, директоры off), первозданный HEAD:

- непрофилированная стена **11.37 с** (25 859 событий; записи
  iter-375: 11.14/11.26 — джиттер машины, форма та же);
- профильная стена 31.82 с; **`director_global_passes` 5.07 с
  (16.1%)** — `entropy` 7 634 вызова (= каждый ленд-бит), внутри:
  **`_global_suspicion` cum 4.11 с** (310 мкс/вызов) +
  **`_visible_physical_threats` cum 0.91 с** (91 мкс/вызов) +
  пересборка frozenset `_threat_states(rules)` НА КАЖДЫЙ вызов;
- `releases` cum 5.10 с — обёртка почти целиком из entropy;
- profiled-протокол: labrunner `--profile-depths 10`,
  canon_check byte_identical=True (снят ДО правок).

## B. Изменение (5 файлов кода/док + 1 новый тест)

1. **`core/director.py` — `SensesIndex`**: складка двух
   мировых чувств (сумма подозрения в ОБОИХ домах + счёт видимых
   угроз) с `apply_change(prop, from_, to_)` и рождением
   `from_projection(projection, states)` (делегирует двум сканам —
   они остаются семантическими владельцами, D-024). Указатель
   `_is_suspicion_home` — единственный владелец формы оси (скан,
   складка и закон-двойник читают его, никогда повторённые копии).
2. **`Director`**: `__post_init__` рождает складку из
   `initial_projection(pack.entities)`; **`seed` складывает
   state_changes КАЖДОГО события** (двойник `apply_event`: `from_`
   есть до-значение, валидированное дверью коммита; реакции
   вложены между коммитом и его `seed` — порядок складки = порядок
   apply); **`bind(projection)`** пересканирует + штампует живой
   объект (честная промывка — локально корректна везде, где база
   складки финальна); **`releases` читает индекс ТОЛЬКО для
   штампованного объекта** (`projection is self._bound`), любая
   чужая проекция держит сканы; `entropy`/`channel_entropies` —
   keyword-only `senses=None` (None = сканы, все прежние вызывающие
   не тронуты).
3. **`core/loop.py`**: bind при construction + после
   resume-восстановления (пасс реплея уже складывает через `seed` —
   перескан промывки заменяет теми же числами). Индекс НЕ входит в
   `export_run_state` (перестраиваем по логу — закон буфера;
   старые курсоры валидны).
4. **`scripts/labrunner.py`**: комментарий члена
   `director_global_passes` + 1 note `_PROFILE_NOTES` (iter-378).
5. **`docs/DIRECTOR_SPEC.md` §4**: runtime-примечание (формула
   неизменна; O(1)-чтение для связанной проекции; сканы — закон
   фолбэка и семантический владелец).
6. **`tests/test_senses.py`** — НОВЫЙ, 7 законов-оракулов (§D).

## C. Почему это законно (законы, ограничивающие дизайн)

- **KI#16 (целая проекция, никогда события-селеры):** складка
  рождена из initial-проекции пакета (каждое посевное значение
  чувствуется как событийная запись — закон «скан целой проекции»
  удовлетворён теми же входами) и обновляется на КАЖДОМ событии,
  несущем hooks или нет — она отслеживает историю ПРОЕКЦИИ, никогда
  события, засеявшие хуки. Двойник `apply_event` — тот же фолд того
  же лога (закон INV-1 сам по себе: живая проекция ЕСТЬ этот фолд).
- **L6/EPIST-1:** entropy читает только наблюдаемое состояние —
  складка агрегирует те же пропсы, никогда knowledge-записи.
- **Обратная совместимость:** `senses` keyword-only со значением
  по умолчанию None; тесты/инструменты/чужие проекции держат сканы
  побайтово (закон-гейт §D — фальсификатор живьём).
- **D-024 (один владелец):** `_is_suspicion_home` единственный
  владелец формы; рождение из сканов; законы-двойники держат
  равенство.

## D. Законы (+7; tests/test_senses.py — все зелёные)

1. `test_birth_scan_equals_the_scans_on_every_committed_pack` —
   рождение == сканам на всех шести паков (tavern/province/
   farstead/grim/pressure/road).
2. `test_birth_scan_counts_seeded_values_not_zero` — зубы закона
   рождения: посевная подозрительность/горящая точка читаются
   НЕ-нулём через индекс (складка из нуля была бы слепа к
   декларациям пака).
3. `test_the_fold_twin_agrees_after_every_event` — ГЛАВНЫЙ закон:
   краевой сценарий из 13 изменений, после КАЖДОГО —
   складка == свежим сканам на сложенной проекции. Края: int в
   обоих домах; **bool** в доме подозрения (никогда не считается,
   обе стороны дельты); **str** в доме; вход/выход dotted-пропа
   из threat-states; **безточечный** проп со значением-угрозой
   (никогда не угроза); **рождение с from_=None**; очистка до None;
   повторные изменения одного пропа в одном событии.
4. `test_repeated_same_prop_changes_inside_one_event` —
   прогрессивная семантика (change N от состояния change N-1).
5. `test_the_identity_gate_bound_reads_the_fold_foreign_reads_the_scan`
   — гейт идентичности, наблюдаемый СНАРУЖИ через quiet-gate:
   связанная проекция при подозрении 10 держит ворота закрытыми
   (складка ответила); та же director на чужой копии без подъёма
   ОТДАЁТ релиз (скан ответил чужому виду — закон фолбэка).
6. `test_the_real_log_twin_law` — реальный лог (кража → каскад
   подозрения → биты → ротация): складка == сканам mid-run и в
   конце (производственный путь, для которого индекс существует).
7. `test_the_resume_law` — курсор-резюм: складка возобновлённой
   сессии == сканам восстановленной проекции; `_bound is
   sim2.projection` (O(1)-путь вооружён через границу процесса).

## E. Стена: до/после (один инструмент, один протокол)

| | до (HEAD e5b095a) | после (iter-378) | |
|---|---|---|---|
| стена h32 10y (непроф.) | **11.37 с** | **9.57 / 9.49 с** | **×1.19** |
| профильная стена | 31.82 с | 27.06 с | ×1.18 |
| director_global_passes | **5.07 с (16.1%)** | **0.02 с (0.1%)** | **×253** |
| `_global_suspicion` cum | 4.11 с / 7 634 вызова | отсутствует в профиле | честный ноль |
| `_visible_physical_threats` cum | 0.91 с / 7 634 | отсутствует в профиле | честный ноль |
| entropy per-call (cum) | 663 мкс | 3.1 мкс | **×213** |
| события | 25 859 | 25 859 | идентичны |
| md5 лога h32 | `07e924cb…` | тот же | **байт-в-байт** |

Пары конверта: h3 md5 `796afbe1…` идентичен (стена 0.36→0.30 с);
farstead 100y md5 `4e4f4cf2…` идентичен (13 915 событий, 2.62 с).
canon_check labrunner HELD в обоих профильных прогонах.

**Экспонента списана:** iter-364 записывал entropy ×2.50 (сублинейно
на душу — мягчайший из популяционных проходов); теперь per-call
**НЕ ЗАВИСИТ ОТ ПОПУЛЯЦИИ ВООБЩЕ** (h3→h32 ratio 1.2 — чтение O(1)
+ весовой фолд буфера). Цена: складка на пути коммита — O(changes)
на событие внутри `seed` (ездит в `_react` → `seed`, цена в
остатке пути коммита, стеной измерена).

**Остаточная стена (переранжировка, ×1.19 от ×3.37 iter-362):**
skip_probes 35.6% (сборка ключей 939K + роллинг-фильтр) >
beat_rolls 15.3% > commit_validate 14.7% (population-flat — никогда
не стена) > decay_walk 12.3% (×8.1 — сильнейшая остаточная
экспонента, индекс приземления decay — следующая строка приказа).

## F. Верификация (claim-пакет, TEST_PLAN §9)

- **Claim:** складка на пути коммита отвечает РОВНО тому, что
  отвечают сканы целой проекции, для связанного живого объекта.
- **Lens/Prism:** равенство значений (twin-agreement) /
  identity-gate A/B на одном директоре.
- **Oracle:** сканы (семантические владельцы) на реальных
  логах/паках; законы §D — фальсификаторы.
- **Observed:** 7/7 зелёные; канон-нейтральность: три md5
  байт-в-байт (h32/h3/farstead); canon_check HELD ×2; полный
  battery **2636 passed + 27 failed** (сбор 2663 = 2656 HEAD + 7
  новых; 27 = известный T1 log-header env-набор, список имён сверен
  поимённо с документированным множеством — ноль новых; одиночный
  char-дифф на индексе 71 подтверждён живьём — python-поле
  заголовка, оговорка 3.12.15; золотой 3.12.14 зелёный по
  iter-363);
- `ruff check .` clean; `python scripts/docguard.py` clean;
  `python scripts/topology.py --check` clean;
  `python scripts/digest.py` парсит (tests: 2636 passed + 27 failed);
- INV-1..5 не тронуты (INV-2: чистая складка, ноль новых потоков,
  ноль дроу — решения релиза байт-идентичны по закону md5).

## G. Гит-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add core/director.py core/loop.py scripts/labrunner.py docs/DIRECTOR_SPEC.md tests/test_senses.py STATUS.md worklog.md docs/TASKS.md docs/DECISIONS.md docs/iterations/iter-378-sensesidx-report.md
git status --short
git commit -m "iter-378-sensesidx: THE STANDING ORDER'S THIRD HEAD LANDED - the director's SensesIndex (D-255, R3, the iter-362 class, ZERO canon bytes) - the global-suspicion sum + the visible-threat count as a COMMIT-PATH FOLD: born from the pack-seeded initial projection (KI#16's whole-projection law by construction), updated per committed event inside Director.seed (the apply_event twin - from_ IS the door-validated pre-change value; reactions nested between a commit and its seed arrive in exactly apply order), read O(1) per beat for the BOUND projection only (the ScanGateMemo identity-gate form: bind rescans + stamps the live object; every foreign projection keeps the whole-projection scans - entropy/channel_entropies keyword-only senses=None, every existing caller untouched) + the _is_suspicion_home predicate the single owner of the axis's two-home shape + loop.py binds at construction and after the resume restore + the index never enters export_run_state (rebuildable by seed over the log - the buffer's own law, old cursors valid) + 7 oracle laws (tests/test_senses.py: birth on all six packs + the seeded-values teeth; the fold twin after EVERY event over a 13-step edge script - bool/str suspicion both delta directions, the pair home, dotted props entering/leaving the threat states, undotted never-a-threat, None births/clears, repeated same-prop changes inside one event; the identity gate observable through the quiet gate - bound closed at suspicion 10, the same director RELEASES on the foreign copy; the real-log twin mid-run and at drain; the resume law) + labrunner member comment/note + DIRECTOR_SPEC 4 runtime note; MEASURED: the wall h32 10y 11.37 -> 9.57/9.49 s (x1.19), the member director_global_passes 5.07 -> 0.02 profiled s (16.1% -> 0.1%, x253), entropy per-call cum 663 -> 3.1 us - POPULATION-INDEPENDENT now (the iter-364 x2.50 datum retired), both scans the honest absence in the profile, the profiled wall 31.82 -> 27.06 s; ZERO canon bytes: h32 07e924cb../h3 796afbe1../farstead 4e4f4cf2.. identical before/after (canon_check HELD); 2636 passed + 27 failed (the known T1 log-header env set, the failure list diffed name-by-name - zero new; the +7 the new laws, all green), ruff+docguard+topology+digest clean; DECISIONS at 35/35 - AT the D-252 cap, the next entry the owner's collapse call; INV-1..5 untouched"
git push
```

## H. Доставка (§12.2 — оба канала)

Дельта-архив `canonsim_iter-378-sensesidx_2026-10-13.zip` против
BASE_COMMIT `e5b095af…` — файлы §G + BASE_COMMIT.txt +
DELETED_PATHS.txt (`None`); self-check по `git status --porcelain
-uall`; md5 + байты + tmpfiles-ссылка — в финальном сообщении
сессии (само-ссылка: хэш архива не может лежать в отчёте, который
архив содержит).

**Done:** третья голова стоящего приказа закрыта (индекс чувств,
класс iter-362, нуль канон-байт; ×1.19 стены, ×253 члена, per-call
не зависит от популяции); 7 законов-оракулов; D-255 записан;
инструмент синхронизирован; специфик-примечание посажено.
**Not done:** индекс приземления decay (×8.1 — сильнейшая
остаточная экспонента, своя строка допуска по приказу); роллинг-
фильтр memo (urgency_rolls 1.70 с); сборка ключей скана (939K
pair_values); коллапс DECISIONS — вызов владельца (35/35).
**Next:** стоящий приказ продолжается — decay landing index
первой строкой (переранжировка §E), затем роллинг-фильтр и сборка
ключей; параллельные вызовы владельца прежние (runtime-promotion
D-250, replay-UI, W8, P1/P2/P3, lab-composite-1).
**Active KIs:** KI#113 (test_lab, как в STATUS — класс
growth/labels flake, на трёх полных прогонах этой сессии ноль
флейков); KI#121/KI#122 УДАЛЕНЫ этой итерацией по §5 (закрыты
iter-372/373 — более двух итераций назад; живые доказательства
обоих фиксов записаны в репо отчётом iter-374 §0 + worklog —
обязательная чистка, той же приоритетности, что новые строки;
стоящее нарушение закрыто).
