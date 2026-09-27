# Отчёт итерации iter-272 — floodpaper: ряд §6.1 приземлён целиком
# (бумага переправы → держатель → наследование → расчёт + покупка баркаса)

> Fill-list (порядок владельца, iter-266): §6.4 → **§6.1** → §6.5 →
> §6.2 → W6. Ваша формулировка ряда: «усилить carrier: paper
> representation → holder → inherited obligation → later settlement;
> НЕ новый debt-примитив». Ряд закрыт полностью — все четыре части,
> ноль ядра.

## A. Главный ответ (коротко)

**Долг наводнения переправы стал живой арифметикой — полный
жизненный цикл, как у угольной бумаги лагеря.** Четвёртый вид счёта
`floodpaper`, сток на Кетте (20), приёмный сток на Деллане (0),
четыре двери: settle_paper (падение), render_toll (сбор), pass_paper
(наследование), buy_punt (покупка баркаса). НОВОГО примитива нет —
те же три глагола account-резолвера, то же семейство прецедентов
charcoalpaper. «Одна монета — два требования» стала ЗАКОНОМ ДВЕРЕЙ:
покупка баркаса съедает фонд — расчёт мягко отказывает, пока
пошлина не дорастёт.

## B. Четыре части ряда

| Часть ряда | Посадка | Механика |
|---|---|---|
| PAPER DEBT (представление) | ЧЕТВЁРТЫЙ вид `floodpaper`, сток 20 на Кетте | глосса вида несёт СВОЮ датированную цепь: «paper owed to the guild's chest at Malby since the winter after the flood — the borrowed punt and the stranded season's stores, the shelter law's cost» — зима ПОСЛЕ наводнения, никогда не голодная зима лагеря: две бумаги, один сундук, две зимы — собственная пара отчуждения |
| HOLDER (держатель) | сток на toll-taker — держательская сторона места | «долг утонувшего поколения — долг живой руки»: unlapseable-чтение на стороне переправы |
| DEBT INHERITANCE (наследование) | дверь `pass_paper` + приёмный сток на Деллане | открытый вопрос trace iter-160 (rung TRANSFER: «the drowned generation's open question») ОТВЕЧЕН: бумага уходит живой линии, шест и бумага — одно наследство; ответ переправы на анти-фриз — ЛИНИЯ (у лагеря — ремесленное место; сознательно не повторено) |
| LATER SETTLEMENT (расчёт) | `settle_paper` (падение под покрытый фонд) + `render_toll` (сбор в сундук) | форма reckon_paper / render_fund: две доли, один порядок сцены, обратный порядок оставляет over-payment — законный, не сценарный |

**PUNT BUYOUT** — четвёртая дверь, `buy_punt`: двенадцать монет
фондa баркаса уходят в Малби (бухгалтерия лодочной верфи — сток
локации рынка, честная форма без сущности; отдельная сущность верфи
— будущая строка). Это закрывает residue «нет терминуса у
словаря потоков» из debt-1: покупка — дискретное событие, теперь
дверь.

## C. Одна монета — два требования (движок §6.1 — теперь в масштабе игрока)

Слабый профицит (2 + 2/год) кормит ОБА требования: расчёт (20) и
баркас (12). Измерено в т вире (seed 42): фонд дорос до 14 →
покупка баркаса проходит (12 уходят, свидетели слышат
the_punt_bought) → немедленный расчёт ОТКАЗАН мягко (2 < 20).
Требование Деллана накормлено первым — требование Кетты ждёт
 следующего цикла. Это и есть смысл §6.1 — внутренняя напряжённость
домохозяйства одной монетой, теперь проверяемая дверями, а не
только авторским текстом.

## D. Измеренное

- Твин (макро 480, seed 42): бумага стоит 20 сквозь пересечения,
  пока фонд растёт (закон не-амортизации — живое состояние);
- падение: отказ в раннем мире (фонд 2), посадка под покрытый фонд
  (свидетели — the_floodpaper_fell; сказка несёт обе строки
  расчёта с собственной глоссой вида);
- связка: punt в 14 → отказ расчёта в 2;
- наследование: бумага уходит Деллану (0→20), цель без стока —
  мягкий отказ; шест уже на той же руке;
- золотой корпус байт-в-байт (стоки сеются молча, двери не
  вооружены доктриной — нулевая цена корпуса);
- твин детерминирован;
- четыре перепина (campaccount / charcoalpaper / debt1 /
  freightvol — осознанный акт по закону пинов: словарь видов
  расширен, заявки каждого ряда не тронуты).

## E. Честные границы

- **Рождение предмета-баркаса** — припаркованная дверь (семейство
  st-5: entity-birth без механизма): канонический факт покупки —
  ход монет + слово свидетелей; сам корпус лодки появится, когда
  строка откроет дверь рождения. residue записан.
- **Сущность верфи** не заводилась (бухгалтерия — сток локации
  Малби) — будущая строка по вашему зову.
- §6.4 остаётся в состоянии iter-271: продажа — ваша развилка
  (грамматическая стена актёр-стороны), признание тега — будущая
  строка.
- D-строка в DECISIONS не заведена (кап 30/30): запись живёт в
  WORLD_TESTS §9, WORKPLAN §7, ANCHOR_REGION §6.1, phases.md §6.

## F. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — 2493 passed + 9 skipped
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

Изменённые пути (14): content/province_pack/entities.json,
content/province_pack/rules.json,
content/province_pack/actions.json,
content/province_pack/templates.json,
tests/test_floodpaper.py (новый), tests/test_campaccount.py,
tests/test_charcoalpaper.py, tests/test_debt1.py,
tests/test_freightvol.py, docs/worldbuild/WORLD_TESTS.md,
docs/worldbuild/WORLD_WORKPLAN.md,
docs/worldbuild/ANCHOR_REGION.md, docs/blueprint/phases.md,
docs/TASKS.md, docs/iterations/iter-272-floodpaper-report.md
(новый), STATUS.md, worklog.md.

## G. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add content/province_pack/entities.json content/province_pack/rules.json content/province_pack/actions.json content/province_pack/templates.json tests/test_floodpaper.py tests/test_campaccount.py tests/test_charcoalpaper.py tests/test_debt1.py tests/test_freightvol.py docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/worldbuild/ANCHOR_REGION.md docs/blueprint/phases.md docs/TASKS.md docs/iterations/iter-272-floodpaper-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-272-floodpaper: the §6.1 fill row landed whole — the crossing's flood debt at full lifecycle (the fourth kind, the four doors, ONE COIN TWO CLAIMS as door law, the punt fund's terminus)"
git push
```
