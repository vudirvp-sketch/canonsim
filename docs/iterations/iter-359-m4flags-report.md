# iter-359 · m4flags — починка флагов: --g/--ru/--det/--full-corpus теперь реальные no-op алиасы дефолта + --stages селектор + allow_abbrev=False (больше никакого «expected one argument» на --ru)

**Владелец:** «я не понимаю: [...] `station_m4_probe.bat --full-corpus` [...]
`station_m4_probe.bat --g --ru --det` [...]
`run` не является [...] `--full-corpus` unrecognized arguments [...]
`--run-dir: expected one argument` [...]
**настрой нормально скрипт! ало!**»

Это был мой косяк — iter-358 §K я писал «следующий станционный прогон
с `--g --ru --det` (или `--full-corpus`)». Флагов НЕТ в скрипте v4.1.
Владелец попробовал оба вызова, оба умерли в argparse:
1. `--full-corpus` → `unrecognized arguments: --full-corpus`;
2. `--g --ru --det` → `argument --run-dir: expected one argument`
   (это `--ru` совпал как ПРЕФИКС `--run-dir` через `allow_abbrev=True`
   дефолт argparse —/confusing вместо чёткой «unrecognized» ошибки).

**Класс риска:** R2 (локальная правка паковочного скрипта, вне репо
по Rule 9 / D-046 — нулевой код репо, INV-1..5 не тронуты). Базар
нулевого изменения поведения батареи: четыре новых флага — это
НО-ОП алиасы дефолта (все стадии и так запускаются), а реальный
переключатель остался один (`--no-g`); новый `--stages` —
добавочный селектор подмножества, дефолт «все стадии» сохранён.

**BASE_COMMIT:** `e275b6345170168cab275156faa7674211707668` (тот же,
что iter-358 — владелец ещё не закоммитил мои iter-358 райдеры,
iter-359 сидит на том же HEAD).

## A. Что вскрывалось в скрипте v4.1 (контекст фикса)

`station_m4_probe.py` v4.1 (93 289 байт) имеет фиксированный
STAGES = `("preflight", "reference", "r", "g", "ru", "det",
"package")` — все семь стадий запускаются по умолчанию, по
порядку, каждая ждёт что предыдущая «done». Единственный
toggle — `--no-g` (пропустить G-control). Никаких `--g`,
`--ru`, `--det`, `--full-corpus`, `--stages` НЕ было.

Проблема № 1 (МЕТРИКА): я назвал в iter-358 §K флаги, которых
нет → владелец попробовал → краш.

Проблема № 2 (КАЧЕСТВО ОШИБКИ): argparse с `allow_abbrev=True`
(дефолт) делает prefix-match — `--ru` совпало как префикс
`--run-dir` (единственный флаг на «ru-»). Поскольку
`--run-dir` требует аргумент, а следующий токен `--det` —
флаг, argparse сказал «argument --run-dir: expected one
argument» — ЧУЖДАЯ ошибка, маскирующая настоящую проблему
(опечатка/незнание флага).

## B. Что сделано — четыре no-op флага + --stages + allow_abbrev=False

1. **`--full-corpus`** (action="store_true") — no-op алиас
   дефолта: полный 10-юнитный корпус (антоним `--smoke`). Не
   меняет поведения — весь корпус и так дефолт. Документирует
   намерение в cmd-строке;
2. **`--g`** (action="store_true") — no-op: G-control идёт по
   дефолту (toggle остался `--no-g`);
3. **`--ru`** (action="store_true") — no-op: RU-полоса идёт по
   дефолту;
4. **`--det`** (action="store_true") — no-op: det-мини идёт по
   дефолту;
5. **`--stages a,b,c`** (default=None) — НОВЫЙ селектор
   подмножества STAGES. Чекает имена против каноничного списка;
   неизвестное имя → ГРОМКИЙ отказ (`error: --stages: unknown
   name(s) ['foo']; valid: ['preflight', 'reference', 'r',
   'g', 'ru', 'det', 'package']`). `package` всегда неявный в
   конце (закон always-a-zip — m4_*.zip едет всегда, даже на
   краше). Цикл диспетчеризации (`for stage in STAGES`) теперь
   фильтрует по `args._stages_set` (с пакетом-исключением);
6. **`allow_abbrev=False`** на `ArgumentParser` — больше
   никакого prefix-match: `--ru` больше НЕ ловится как
   `--run-dir`. Ошибка непонятного флага теперь ЧЁТКАЯ:
   `error: unrecognized arguments: --xyz`;
7. **`epilog`** в `--help` (с `RawDescriptionHelpFormatter`):
   читаемый список STAGES, объяснение дефолта, таблица
   EXAMPLES — `--g --ru --det` теперь видно как no-op алиас
   дефолта, а не как что-то загадочное.

PACK_VERSION bumped: `v4.2 (iter-359: the flag fix —
--g/--ru/--det/--full-corpus no-op aliases + --stages selector
+ allow_abbrev=False)`. Файл вырос с 93 289 до 98 582 байт
(+5 293 байт, ~5.7% — шесть новых `add_argument` блоков, epilog,
валидация `--stages`, фильтр в STAGES-цикле, комментарии).

README_RU.txt обновлен: заголовок → `iter-359, v4.2`; новый
раздел «ДОБАВЛЕНО В v4.2» с объяснением что владелец
попробовал, почему тогда не сработало, и что теперь
работает; раздел «ПОЧЕМУ ТВОЙ ПРЕДЫДУЩИЙ ПРОГОН ОБОРВАЛСЯ НА
s4» (R-рука не закрылась → G/RU/det не стартовали — НЕ баг
скрипта, а Ctrl-C/закрытое окно/`--time-budget`); рецепт
`--run-dir <папка> --stages ru,det` для докатки без перегона R.

## C. Почему no-op, а не реальные переключатели

Все семь стадий ВАЛЕНЫ по дефолту — это закон пака
(iter-357 §D: «G-control byte-comparable, RU band 12
hand-authored rows, det mini, gate sweep» — всё в каждом
прогоне). Делать `--g`/`--ru`/`--det` реальными включателями
значит: по дефолту G/RU/det OFF, и единственный прогон без
флагов НЕ делает всю батарею. Это сломало бы iter-358 §B
(где R самодостаточен, но G/RU/det ЕДУТ по дефолту, и.owner's
run ИМЕЛ ИХ В ИНТЕНЦИИ — он просто оборвался на s4).

Поэтому флаги — no-op алиасы дефолта: вызов `--g --ru --det`
читается как «включи все три», но они уже и так включены —
ничего не меняется. Реальные переключатели — `--no-g`
(пропустить G, как и в v4.1) и новый `--stages` (выбрать
подмножество). Так сохраняется батарейное поведение v4.1
и совместимость со всеми предыдущими вызовами, плюс мой
iter-358 §K гайд теперь работает дословно.

## D. Живая валидация в sandbox (python3 —syntax + 6 вызовов)

| # | Вызов | Результат |
|---|---|---|
| 1 | `python3 station_m4_probe.py --help` | epilog с STAGES + EXAMPLES виден |
| 2 | `--g --ru --det` | ПРИНЯТО → штатный выход «no decision model» (sandbox без моделей) |
| 3 | `--full-corpus` | ПРИНЯТО → тот же выход |
| 4 | `--g --ru --det --full-corpus` (все 4) | ПРИНЯТО → тот же выход |
| 5 | `--xyz` (опечатка) | `error: unrecognized arguments: --xyz` — ЧЁТКАЯ |
| 6 | `--stages r,foo` (опечатка стадии) | `error: --stages: unknown name(s) ['foo']; valid: [...]` |
| 7 | `--stages ru,det` (валидное подмножество) | ПРИНЯТО → штатный запуск |

Все семь проверок прошли. PACK_VERSION в stdout = `v4.2
(iter-359: ...)`. Сравните с v4.1: вызовы 2-4 падали с
argparse-ошибкой — теперь проходят.

## E. Пак v4.2 — что внутри

10 файлов в `canonsim_m4_station_pack/` (верхний уровень тот
же что у владельца):
- **station_m4_probe.py** (98 582 байт) — патченная v4.2;
- **README_RU.txt** (18 450 байт) — обновлённый заголовок +
  новый раздел «ДОБАВЛЕНО В v4.2» + раздел про обрыв s4 +
  рецепт --run-dir --stages для докатки;
- m4_analysis.py, m4_units.py, sandbox_report.txt,
  station_m4_doctor.{bat,py}, station_m4_probe.bat,
  station_m4_setup.{bat,py} — НЕ тронуты (те же, что v4.1).

Исключены против v4.1 пака владельца: `doctor.json`,
`m4_llama_main.log`, `m4_llama_router.log`, `__pycache__/` —
это runtime-артефакты прогона владельца, не инструменты
пака. Чистый пак = чистые инструменты.

## F. Что это значит для долгосрочного трека

iter-358 §B задал архитектурный вывод: R-форма работает на
станции живьём (0 изобретений/12 docs, output_tokens=[0], GPU
0.520 s). iter-359 закрывает ИНТЕРФЕЙС того же вопроса:
владелец теперь может запустить «полный прогон» ЧЕТЫРЬМЯ
равнозначными способами:

- `station_m4_probe.bat` (просто двойной клик, без аргументов);
- `station_m4_probe.bat --full-corpus` (явный «полный»);
- `station_m4_probe.bat --g --ru --det` (явный «все три
  дополнительные стадии»);
- `station_m4_probe.bat --g --ru --det --full-corpus`
  (комбинированный).

И новый `--stages` открывает ДОКАТКУ: если R+G уже
прогнаны, а RU+det не вышли, нет нужды перегонять R с нуля
— `--run-dir m4_<ts> --stages ru,det` докатает только
недостающее. Это был явный пробел iter-358 §F — теперь
закрыт инструментально.

## G. Верификация

- `python3 -c "import ast; ast.parse(open('station_m4_probe.py').read())"`
  — синтаксис OK;
- 7 живых smoke-вызовов в sandbox (таблица §D) — все прошли;
- PACK_VERSION в stdout — `v4.2 (iter-359: ...)`;
- `python scripts/docguard.py` — clean (AGENTS §6 caps);
- `python scripts/topology.py --check` — clean (owners +
  watchlist pins held; нулевой код репо);
- `python scripts/digest.py` — парсит (iter-359 заголовок
  обновлён в STATUS.md);
- INV-1..5 не тронуты (R2 riders-only вне репо; код пака
  отдельный от кода репо; zero repo code).

## H. Дальше

1. **Владелец распаковывает `canonsim_m4_station_pack_v4.2.7z`
   рядом с текущим паком** (или поверх — структура та же,
   `canonsim_m4_station_pack/` верхний уровень);
2. **Перезапуск прогона** — три двойных клика (setup уже
   сделан; doctor уже сделан; probe — теперь с любым из
   четырёх эквивалентных вызовов). Прогон идёт ~5-10 минут
   на GPU; m4_*.zip обратно;
3. **Альтернативный путь** — если владелец хочет ДОКАТАТЬ
   `m4_20261010_140351` (его оборванный прогон) без
   перегона R: `station_m4_probe.bat --run-dir
   m4_20261010_140351 --stages ru,det` (R будет «done
   (resumed)», скрипт пойдёт в RU+det);
4. Чтение вернувшегося m4_*.zip закрывает заголовочный
   вопрос RU-полосы на Kev (iter-358 §H OPEN-список);
   затем M2/M3 решения за гейтом runtime-promotion.

## I. Git-блок владельца (§12.3)

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-358-m4station-run-report.md docs/iterations/iter-359-m4flags-report.md
git status --short
git commit -m "iter-358 + iter-359: THE M4 STATION RUN READING + THE FLAG FIX - iter-358 read the owner's m4_20261010_140427.zip (TWO R-FORM PROOFS: 0 inventions/12 docs + output_tokens=[0] on every call; GPU band opened by measurement 0.520 s on 3080 Ti vs 3.30 s CPU iter-357 x6.3; gate sweep first live numbers gate>=0.5 66.7% / gate>=0.4 100%; doctor verdicts on six models; Kev-4B decision:kev validated — broken-copy NOT reproduced, CLOSED LIVE); iter-359 fixed the flag interface I broke in iter-358 §K: the four no-op aliases (--g --ru --det --full-corpus) now exist as documentation of the default (all stages run by default), plus the --stages selector for subset runs (e.g. --stages ru,det for the docatka after R+G finished), plus allow_abbrev=False so --ru no longer collides with --run-dir prefix-match (the confusing expected one argument error). PACK_VERSION v4.2 (iter-359). Zero battery behavior change — the four flags are documentation, the real toggles stay --no-g and --stages. Pack v4.2 (10 files, 49 079 bytes, md5 be974f8c32771922766ffbb21051ae4c) outside the repo per Rule 9. R0/R1+R2 riders-only, zero repo code, INV-1..5 untouched"
git push
```

## J. Доставка (§12.2 — оба канала)

- **Пак v4.2** (вложение): `canonsim_m4_station_pack_v4.2.7z`
  сохранён в `/home/z/my-project/download/` — едет через чат
  как вложение;
- **tmpfiles.org страница**: https://tmpfiles.org/wsAs6rgYxgrO/canonsim_m4_station_pack_v4.2.7z
  (открывает страницу с кнопкой «Download»);
- **tmpfiles.org прямая ссылка**: https://tmpfiles.org/dl/1791644285.e3a2d79b6f016ed8/wsAs6rgYxgrO/canonsim_m4_station_pack_v4.2.7z
  (срок ~1 час; страница регенерирует свежую по запросу);
- **md5**: `be974f8c32771922766ffbb21051ae4c` (локальный и
  скачанный сверены);
- **размер**: 49 079 байт;
- **содержимое**: 10 файлов под `canonsim_m4_station_pack/`
  — station_m4_probe.py v4.2 (98 582 байт, патченный),
  README_RU.txt v4.2 (18 450 байт, обновлённый), и 8
  нетронутых файлов пака v4.1.

**Репо-дельта** (5 файлов, same BASE_COMMIT `e275b63`): STATUS.md
(header + Next), worklog.md (iter-359 entry + iter-358 entry, iter-348
evicted), docs/TASKS.md (m4-r row updated + iter-359 ledger line,
iter-348 evicted), docs/iterations/iter-358-m4station-run-report.md
(the prior iter in this session), docs/iterations/iter-359-m4flags-
report.md (this) — 5 changed/created, all riders. И архива:

- **Дельта-архив** (вложение): `canonsim_iter-358-plus-359_2026-10-10.zip`
  сохранён в `/home/z/my-project/download/` — едет через чат;
- **tmpfiles.org страница и прямая ссылка**: будут указаны в
  финальном сообщении чата (tmpfiles.org прямая ссылка
  истекает ~1 час — страница остаётся и регенерирует свежую
  прямую по запросу);
- **md5**: будет указан в финальном сообщении чата (точная
  циферка зависит от финальной сборки zip; архив внутри себя
  не ссылается на свой собственный md5 — quine-проблема);
- **размер**: ~88 КБ;
- **содержимое**: 7 файлов — STATUS.md (~24 КБ), worklog.md
  (~33 КБ), docs/TASKS.md (~113 КБ), docs/iterations/iter-358-
  m4station-run-report.md (~24 КБ), docs/iterations/iter-359-
  m4flags-report.md (~18 КБ), BASE_COMMIT.txt (41 Б),
  DELETED_PATHS.txt (5 Б = None).

**Done:** флаги `--g`/`--ru`/`--det`/`--full-corpus` теперь
реальные no-op алиасы дефолта; `--stages` — селектор
подмножества; `allow_abbrev=False` убирает путающий
prefix-match; PACK_VERSION v4.2; smoke-тесты 7/7 прошли; пак
собран и загружен; райдеры прошли docguard + topology + digest.
**Not done:** станционный прогон с v4.2 (за владельцем —
распаковать пак, перезапустить probe, прислать m4_*.zip).
**Next:** чтение вернувшегося m4_*.zip (закрывает RU-полосу +
G-control + det-mini на станции); затем решения M2/M3 за
гейтом runtime-promotion.
**Active KIs:** KI#113 (test_lab, как в STATUS).
