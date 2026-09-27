# Отчёт итерации iter-275 — stepbench: §6.2 приземлён (PRESENT и NOTCH
# живым состоянием, HATCH остаётся прозой, двусторонняя полоса измерена)

> Порядок владельца 2026-09-27, строка 4: продолжить §6.2 — последний
> embodiment-ряд fill-list, поставленный последним самим владельцем
> (iter-266): «два риск-слоя — present-state persistence + verb gate;
> wattle = prose... наивысший шанс преждевременно удариться в
> substrate gap». Ряд приземлён через СУЩЕСТВУЮЩИЙ аккаунт-сабстрат
> (семейство iter-273), разрывы честно записаны, никогда не обойдены.

## A. Главный ответ (коротко)

**PRESENT приземлён.** Пятый вид счёта `step` — стоячий напор как живое
состояние, сток у хранительницы (три — рабочий напор, длина long_light
по умолчанию; настройка плоских ворот — в её руке). Дверь
`set_the_timbers`: вооружена ТОЛЬКО затяжка (consume), гейт
платёжеспособности step ≥ 3 — **закон пола в собственной арифметике
гейта**: затяжка только с рабочего напора; на низкой полосе гейт
отказывает мягко — первый уступ принадлежит засухе, не руке («never
set but by a drought the vale survives, and never unnotched»).
Ослабление остаётся авторизованным (восстановление цены — будущий
сезон, закон freightvol); четвёртый уступ — никогда не настройка
(это текст самого подъёма воды). Чтение у лестницы (read_stair,
iter-167) минтит ЗАКОН — сток несёт НАСТОЯЩЕЕ; две поверхности
встречаются у читателя.

**NOTCH приземлён честной половиной.** Шестой вид `notch` — сухие годы
в дереве, сток у руки весов (носительница счётного шеста, счёт
открывается в нулях). Дверь `cut_the_notch`: расчёт весового дня
(source, форма принятия по прецеденту reprice — актёр и цель одна
рука). **ЧЕСТНЫЙ РАЗРЫВ, ИЗМЕРЕН**: законное условие зарубки — стояние
сухой полосы — ДВУСТОРОННЕЕ условие, которое закрытый словарь гейтов
выразить не может (account_at_least читает полы, никогда потолки,
никогда точные значения). Свидетель прогоняет зарубку на РАБОЧЕМ
напоре — дверь срабатывает: закон полосы остаётся прозой. Это первое
отсутствующее причинное звено ряда §6.2 — названный кандидат в
инвентарь субстратных ограничений свидетеля I0.

**HATCH остаётся прозой — граница соблюдена.** Ватт (плетень в устье
лотка) имеет бросательно-открытую форму — «кто бросит, тот и право
пользователей у воды» — без единого держателя; ватт-сток потребовал бы
сток на каждом пользователе: сверх-авторинг, который граница verb-gate
отвергает (WORLD_AUTHORING §8, закон iter-266). Социальная половина
нарушения уже жива (претензия хода едет через толки весов —
коммитнутый канал слухов).

## B. Измеренное (seed 42, макро-480 твин)

- затяжка 3→2, свидетель — живая линия (вторая рука на лестнице
  узнаёт the_timbers_set exact); сказка несёт строку с глоссой вида:
  «Ketta is rid of 1 step at the weir stair — the standing head
  named by the stair's wet step, the timbers' setting in the keeper's
  hand (three the working head, two the low band's standing, one the
  drought floor the drought's own).»;
- пол: вторая затяжка отказана мягко (actor.account_at_least) — первый
  уступ недостижим рукой;
- зарубка 0→1, свидетели — толпа и сержант; строка: «Maren comes by
  1 notch on the tally staff — the dry years' sequence in wood, the
  beam's reckoning cut at the weighing day at the year's
  reckoning.»;
- разрыв: зарубка срабатывает на рабочем напоре (step всё ещё 3) —
  закон полосы проза, измерено;
- словарь видов теперь шесть (coin/bloom/paper/floodpaper/step/notch),
  пять цензусов пере-закреплены; потоки не трогают step и notch;
- корпус байт-в-байт (обе двери безоружны по доктрине), твины
  детерминированы.

## C. Честные границы

- Ослабление тимберсов — будущая строка (восстановление цены =
  авторский будущий сезон, закон freightvol).
- Двусторонняя полоса — первый кандидат в I0-инвентарь субстратных
  ограничений (никакого нового гейта до I0 — ваш закон).
- Ватт — проза по закону; если I0 вскроет повторную потребность в
  «бросателе-без-держателя», это будет тот самый повторный
  субстратный лимит.
- Fill-list ЗАКРЫТ полностью (§6.4 → §6.1 → §6.5 → §6.2 — все четыре
  ряда приземлены). Порядок: **I0 World Ignition Witness** → W6.

## D. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2513 passed + 9 skipped
✓ ruff check . — clean
✓ python scripts/docguard.py — clean
✓ python scripts/topology.py --check — clean
✓ LOG не тронут; золотой корпус байт-идентичен (нулевая цена)
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

Изменённые пути (14): content/province_pack/{entities.json, actions.json,
templates.json, rules.json}, tests/{test_stepbench.py (новый, 7 тестов),
test_campaccount.py, test_charcoalpaper.py, test_debt1.py,
test_floodpaper.py, test_freightvol.py (пять цензусных re-pin'ов)},
docs/{worldbuild/ANCHOR_REGION.md (§6.2), worldbuild/WORLD_TESTS.md (§9),
worldbuild/WORLD_WORKPLAN.md (§7 + cruft-pass D-024),
blueprint/phases.md (§6), TASKS.md, iterations/
iter-275-stepbench-report.md (новый)}, STATUS.md, worklog.md.

## E. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add content/province_pack/entities.json content/province_pack/actions.json content/province_pack/templates.json content/province_pack/rules.json tests/test_stepbench.py tests/test_campaccount.py tests/test_charcoalpaper.py tests/test_debt1.py tests/test_floodpaper.py tests/test_freightvol.py docs/worldbuild/ANCHOR_REGION.md docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/blueprint/phases.md docs/TASKS.md docs/iterations/iter-275-stepbench-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-275-stepbench: the §6.2 row landed — PRESENT (the step kind + the tightening door with the floor law in the gate) + NOTCH (the tally's count, the two-sided band gap measured) + HATCH held as prose (the verb-gate boundary)"
git push
```
