# Отчёт итерации iter-274 — moverelease: §6.5 закрыт, хранительница
# уходит с пепелища (цена iter-263 оплачена и перемерена)

> Порядок владельца 2026-09-27, строка 3: продолжить §6.5. Последняя
> незакрытая строка §6.5 — move-release, «будущая строка владельца по
> её iter-263 цене». Эта итерация открывает ряд: пик интента хука
> `market_mourns` переавторизован с ramble на DEPARTURE.

## A. Главный ответ (коротко)

**Марен уходит с пепелища — и рынок умирает вместе с ней.** Чистые
пак-данные, ноль ядра: блок intent хука теперь
`{"kind": "move", "target": "loc_keep"}`. Авторская причина: её нужда
была бумагой рынка — долг сына, покрытый лавками; огонь забрал
покрытие вместе с лавками, у весового луча нет хранительницы там,
где лавочный ряд — пепел. Дорога вдовы — пост стражи; шест счёта
едет с ней (контракт carried-item, форма iter-263 воспроизведена).

**Цена честно оплачена и перемерена на коммитнутой форме**
(composition-свидетель, seed 42):

| Поверхность | было | стало |
|---|---|---|
| разговоры (urgency_0004) | 287 | **2** (оба до выгорания) |
| слухи | 25 | **2** |
| автономные резолюции | 384 | **306** |
| всего событий | 2376 | **2269** (коллапс перевешивает кучу) |
| советы гильдии | 1 | **208** (1 живой + куча B2 из 207 за один тик) |
| макс. латентность | 518861 | **517055** |

Куча советов — известная форма (B2 catch-up через фракционную дверь,
семейство «86 проверок одним тиком» iter-261): страх Марен заморожен
холодной зоной LOD на 43 (над планкой гильдии 30), и годовое
пересечение выплёскивает накопленное одним тиком t=525335. Запись
честная: лог-куча, не сюжетный бит — цена, названная ещё в iter-263.

## B. След ухода на живой мир

- **Множества слушателей вигилии несут отпечаток ухода**: первая
  вигилия (t=3254, через два тика после ухода) минтуется БЕЗ Марен —
  она уже не «через стены рынка»; корпал на посту (окна ротации
  сдвинулись с каскадом), поздняя пара — сержант обратно.
- **Оброненный счёт всё равно материализуется** (ленивое рождение
  observe-семейства, скан сержанта) — минимум ramble забрал свой
  черпак, рождение потока осталось (INV-2: черпак — потоковый).
- **Закон негерметичности перемерен**: стоящий рынок никогда не
  скорбит (option gate), spurious-релизов нет.
- **Честная форма живости названа**: живой мир — не громкий. Мир
  читается тише, потому что его говорунья ушла. Это и есть
  liveness: накопленная история меняет то, что может произойти.

## C. Корпус

- **Дымовой корпус байт-в-байт** — релиз никогда не срабатывает в
  его окне (нулёвая цена корпуса, регенерация не нужна).
- Свидетель-двойник детерминирован (T1).

## D. Честные границы

- Куча из 207 советов — записанная форма сабстрата (B2), не
  сюжетный бит; её «укрощение» — вопрос будущего сабстрата, не этой
  строки (новая рантайм-механика — только по лимиту I0, по вашему
  закону).
- Рамбл-строка Марен осталась в словаре шаблонов (семейство
  wilmot_grief_ramble живо), но её площадка эмиссии ушла — строка
  more не мёртвая (ramble Уилмот её носитель).
- §6.5 ЗАКРЫТ полностью. Порядок: §6.2 (PRESENT/HATCH/NOTCH) → I0
  World Ignition Witness → W6.

## E. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2506 passed + 9 skipped
✓ ruff check . — clean
✓ python scripts/docguard.py — clean
✓ python scripts/topology.py --check — clean
✓ LOG не тронут; дымовой корпус байт-идентичен
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

Изменённые пути (9): content/province_pack/rules.json,
tests/test_marketlegs.py, tests/test_p1_composition.py,
docs/worldbuild/ANCHOR_REGION.md, docs/worldbuild/WORLD_TESTS.md,
docs/worldbuild/WORLD_WORKPLAN.md, docs/blueprint/phases.md,
docs/iterations/iter-274-moverelease-report.md (новый), STATUS.md,
worklog.md.

## F. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add content/province_pack/rules.json tests/test_marketlegs.py tests/test_p1_composition.py docs/worldbuild/ANCHOR_REGION.md docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/blueprint/phases.md docs/iterations/iter-274-moverelease-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-274-moverelease: the §6.5 row closed — the mourns intent pick re-authored to the departure (the keeper leaves the ashes), the iter-263 price honestly paid and re-measured (talks 287→2, the council pile 1→208)"
git push
```
