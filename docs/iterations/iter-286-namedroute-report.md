# Отчёт итерации iter-286 — namedroute: маршрут named-границы W7
# (институциональная причина отказа как строка рендеринга),
# две диспозиции владельца разрешены — батарея НЕТ, W8 ОТКРЫТА

> Ваш приказ: «продолжай работу над задачами класса мирового
> трека» — с тремя битами: (1) расширить disappearance-battery на
> остальные мажоры, «если это имеет смысл и глобально поможет
> проекту, а не будет просто допиливанием»; (2) «точечный и быстрый
> (read-side only)» — реализовать; (3) «если нет, то и w8 открыть».
> Эта итерация реализует (2), честно отвечает НЕТ на (1) и открывает
> W8 по вашему условному зову.

## A. Главный ответ (коротко)

**Маршрут named-границы посажен — read-side only, ноль канона,
ноль гейтов, ноль машин.** Граница (a) iter-284/285 —
институциональная причина отказа «за пределами читаемой
поверхности» — теперь читаема: в мире без слова запись бегуна
несёт «tries to coerce — impossible here — no minted word to lean
on», в мире со словом — чеканку и трату рычага. Механизмы «нет
рычага» и «запрет на coerce», неразличимые по материалу на обеих
полосах чтения W7, теперь различаются ПРОЗОЙ на поверхности
записей — граница Q5 закрыта на стороне чтения. **Расширение
батареи на остальные мажоры — НЕТ** (§C: честное обоснование,
измеренное вашим же критерием). **W8 открыта** по вашему условию.

## B. Что сделано (rs-13 — тринадцатый член семейства глосс-границ)

Форма — ровно прецеденты rs-2 (account_kinds, iter-196) и rs-4
(flow_glosses, iter-206), ни одного нового механизма:

1. **Пак-таблица** `templates.json::rejection_boundaries`:
   имя ГЕЙТА → проза, называющая отказывающий авторитет.
   Единственная строка: `leverage_over` → «no minted word to lean
   on» — реестр как власть рычага, в лексиконе самого семейства
   coerce («leans on … the hold is spent»). Слова — пак (ИНВ-3),
   механизм — рендер.
2. **Одна граница глосса** `render/chronicle.py::
   gloss_rejection_boundary`: из `failed_test` события берётся
   сегмент гейта (последняя точечная часть; префикс noun/holder —
   машинерия двери, не читателя), глоссится через таблицу.
   Неглоссированный гейт — ПУСТО (закон фолбэка flow-глоссов:
   сырой машинный токен никогда не доходит до читателя).
3. **Слот `boundary`** кладётся в контекст ДО генерического цикла
   outcome (прецедент rs-2/rs-4 — приоритет посадки), только для
   событий `intent_rejected`.
4. **Условный хвост** у строки отказа провинции:
   `{actor} tries to {action_label} — impossible here{boundary? —
   {boundary}}.` — форма rs-12 (знающий хвост счётной строки).
   Один шаблон — каждый потребитель: гейтированная строка сказки
   и негейтированная запись актёра (поверхность, которую читали
   читатели W7).
5. **Линт при загрузке** (`core/packlint/actions.py::_templates`):
   закон вакуативности у двери — глосс для гейта, который пак
   НИГДЕ не вооружает (`requires`), есть мёртвые данные, отказ.
   Словарь — объединение вооружённых гейтов пака.
6. **Константа блока** — единственный владелец `core/intent.py`
   (`REJECTION_BOUNDARY_BLOCK`, D-024): линт и рендер импортируют
   одну константу.

## C. Диспозиция 1: расширение батареи исчезновения — НЕТ

Ваш критерий: «глобально поможет проекту, а не будет просто
допиливанием». Измерение против него:

- **Мезо-юниты уже несут свой disable-тест.** Восемь петель
  якоря проходят его в `ANCHOR_REGION.md` §5 — «удали одного
  уникального драйвера, остальные выживают» — это и есть батарея
  исчезновения, применённая к мешу. Рука руки бы перемерила
  перенесённое.
- **Три плеча iter-283 отвечали на НОВЫЕ вопросы способностей**
  (грамматическая стена четвёртого глагола, цена скорби, реестр
  как власть). Непокрытой способности в мажорах больше нет:
  счётные руки мезо-юнитов едут через тот же резолвер, что и
  плечо settle; поверхности — через то же семейство rs.
- **Новый тип свидетельства не появляется.** Ещё четыре плеча
  дали бы ещё четыре CONFIRMED того же класса — определение
  допиливания.
- **Строка остаётся доступной** для ПЕРВОГО плеча следующего
  НОВОГО мажора (закон станции: батарея стреляет по новой
  способности, никогда по бэклогу).

## D. Диспозиция 2: W8 открыта — W7 закрыта

Станция W7 завершена четырьмя строками: батарея + компрессия
(iter-283), полоса чтения LLM-половина (iter-284), живая
половина (iter-285), маршрут named-границы (iter-286). W8
(интеграционная готовность) открыта вашим условным зовом — её
первая строка: аудит готовности по семи критериям
(`WORLD_WORKPLAN.md` §10), каждый критерий — цитатой своему
стоящему владельцу, зазор назван там, где доказательство тоньше
заявленного. Никакого перемера — аудит потребляет накопленное.

## E. Свидетель (`tests/test_namedroute.py`, 6 тестов)

| # | Тест | Вердикт |
|---|---|---|
| 1 | named-граница рендерится на поверхности записей | **MET** — двойник без слова: «tries to coerce — impossible here — no minted word to lean on»; сырой токен `actor.leverage_over` не протекает |
| 2 | мёртвые двери различаются прозой | **MET** — C: leverage_gained + coerce, запись несёт «now holds something over Garrick …» и «leans on Garrick — the hold is spent»; D: ноль того, ноль другого, отказ с причиной — дискриминация Q5 стала фактом ПРОЗЫ |
| 3 | неглоссированные гейты — стоячая строка | **MET** — золотой корпус: отказ хода (`target.adjacent_to`, t 1440) рендерится «tries to move — impossible here.» байт-в-байт; фолбэки функции пусты |
| 4 | гейт сказки не тронут | **MET** — отказ (low) не входит в сказку (gate medium, без изменения), граница едет на ЗАПИСЯХ; тот же шаблон служит обеим поверхностям |
| 5 | линт отказывает мёртвым данным | **MET** — негде не вооружённый гейт (trait_held), неизвестный гейт, пустой и нестроковый глосс — все PackError; невооружённый двойник грузится и рендерит стоячую строку |
| 6 | золотой корпус байт-в-байт | **MET** — нулевая цена корпуса: шаблоны не входят в лог |

## F. Честные границы (классифицированы, не «починены»)

| # | Граница | Класс |
|---|---|---|
| a | Перемер полосы чтения над поверхнутой границей не проводился | честная граница этой строки: маршрута, не перемера; ваш будущий зов (форма iter-284/285 — слепые чтения над регенерированным китом) |
| b | Глоссирован один гейт (`leverage_over`) | точечность — ваш собственный заказ; остальные гейты читаемы из состояния мира (география/запас), читатели их границей не называли |
| c | Хвост виден только в записях актёров | закон гейта сказки (T7, low-importance канон отказа) — не поднимался и не будет без вашего зова |
| d | Песочница: один прогон тестов дал единичный таймаут лаунчер-теста под нагрузкой; одиночный и повторный прогоны чисты | окружение, не код; отмечено в STATUS |

## G. Верификация

```text
✓ PYTHONHASHSEED=0 python -m pytest -q — зелёный, 2556 passed + 8
  skipped в этой песочнице (стоящее 2550+9: вариация одного скипа
  окружения; +6 — свидетель namedroute)
✓ ruff check . — clean
✓ python scripts/docguard.py — clean (workplan 598/600, реестр 10,
  worklog 10×3–5 строк, один скользящий DONE-блок, KI-секция пуста)
✓ python scripts/topology.py --check — clean
✓ committed pack тронут ровно одним блоком (rejection_boundaries) и
  одной строкой (хвост intent_rejected); LOG не тронут; ноль
  изменений канона; золотой T1-корпус байт-в-байт; ноль цены корпуса
```

## Воспроизведение

```bash
PYTHONHASHSEED=0 python -m pytest tests/test_namedroute.py -q
PYTHONHASHSEED=0 python -m pytest -q
ruff check .
python scripts/docguard.py
python scripts/topology.py --check
```

## H. Порядок дальше

W8 открыта; её первая строка — ваш зов: аудит
интеграционной готовности по семи критериям
(`WORLD_WORKPLAN.md` §10): якорь с авторским субстратом, мезо-юнит,
представимость контента примитивами пака (или названный зазор),
обычное событие с персистентным человеческим следствием, явная
асимметрия знания, мир-специфика вне ядра онтологии, тесты
различают доказанное и гипотетическое. Альтернативно — перемер
полосы чтения над поверхнутой границей (F(a)), если хотите
закрыть её на обеих полосах до аудита.

## I. Изменённые пути (13)

render/chronicle.py, core/intent.py, core/packlint/actions.py,
content/province_pack/templates.json, tests/test_namedroute.py
(новый — свидетель), docs/worldbuild/WORLD_TESTS.md (§9 — четвёртая
строка + обе диспозиции), docs/worldbuild/WORLD_WORKPLAN.md (§9
четвёртая строка; §10 W8 OPENED; кап 598/600),
docs/worldbuild/WORLD_TRACK_AGENT_CONTEXT.md (§9 + блок W-стадий),
docs/blueprint/phases.md (§6 — запись iter-286), docs/TASKS.md
(реестр, iter-276 вытеснен), docs/iterations/
iter-286-namedroute-report.md (новый — этот отчёт), STATUS.md
(заголовок iter-286 + Next + KI#107 удалён по §5), worklog.md
(iter-276 вытеснен).

## J. Владельческий git-блок

```bash
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add render/chronicle.py core/intent.py core/packlint/actions.py content/province_pack/templates.json tests/test_namedroute.py docs/worldbuild/WORLD_TESTS.md docs/worldbuild/WORLD_WORKPLAN.md docs/worldbuild/WORLD_TRACK_AGENT_CONTEXT.md docs/blueprint/phases.md docs/TASKS.md docs/iterations/iter-286-namedroute-report.md STATUS.md worklog.md
git status --short
git commit -m "iter-286-namedroute: the W7 station's fourth row — the named-boundary rendering route landed read-side (rs-13, the gloss-boundary family: the pack table rejection_boundaries with leverage_over -> «no minted word to lean on», the one gloss boundary over the failed_test's gate segment, the boundary slot before the outcome loop, the intent_rejected line's rs-12-form conditional tail, the armed-gate vacuity lint) — the Q5 boundary closed at the readable surface: the no-word twin's record carries the refusal's institutional cause while the committed package's carries the hold minted and spent, the discrimination now a prose fact; the owner's two dispositions resolved: the disappearance-battery extension to the remaining majors NO (the meso units' drivers already pass the anchor's disable test — no uncovered capability remains, the row stays for a NEW major's own arm), W8 OPENED on the conditional call — the W7 station COMPLETE (iter-283/284/285/286); KI#107 deleted at the §5 cleanup"
git push
```
