# Отчёт итерации iter-377 — hygiene-1 (три точечных фикса ревизии iter-376)

> Вызов владельца 2026-10-12: «даю добро на hygiene-1» — явное
> разрешение на строку бэклога, записанную iter-376 (D-198: запрос
> сессии = текущая задача). Класс R0: нуль строк кода поведения —
> комментарии, докстринги, доки. Все три находки закрыты за одну
> итерацию, как и обещала строка.

**Класс риска:** R0 (текст/комментарии/доки; нуль поведения;
райдеры STATUS/worklog/TASKS).

## A. F1 — четыре устаревших inference.py-пути → пакет

Модуль `workbench/application/inference.py` стал пакетом
`inference/` на iter-247 (ssi-4 шаг 1); четыре живых носителя всё
ещё указывали на несуществующий файл — класс KI#42/48/51/80 (doc
drift), функционально мёртвых ссылок не было, только текст.

| Сайт | Было | Стало |
|---|---|---|
| `settings.py:30` (докстринг модуля) | `` `workbench/application/inference.py` `` (profile store) | `` `workbench/application/inference/` `` |
| `settings.py:98` (SCHEMA-комментарий) | `` `workbench/application/inference.py`'s `migrate_launch_semantics` `` | `` `workbench/application/inference/migration.py`'s `` (функция живёт в `migration.py:49`; фасад `__init__` её реэкспортирует — оба пути валидны, выбран точный) |
| `settings.py:121` (докстринг LaunchSettings) | `` `workbench/application/inference.py`'s profile store `` | `` the `workbench/application/inference/` profile store `` |
| `test_inference.py:2` (докстринг модуля) | `` `workbench/application/inference.py` `` | `` `workbench/application/inference/` `` |

Проверено: других живых упоминаний старого пути нет (grep по репо
вне docs/iterations — истории; оставшиеся в SSI_TOPOLOGY/
SSI_OVERLAY/TASKS:359 — санкционированные исторические записи
«стал пакетом на iter-247», явная пометка прошлого состояния).

## B. F2 — голый внешний путь в TEST_PLAN §9.1

`docs/SCALE_TESTING_LAW.md` — путь ВНУТРИ внешнего хозяйского
research-компаньона (canonsim_unified_agent_pack v1.5), читался
как путь репо и не находился. Уточнение посажено в сам блок
цитирования (плюс одна строка, нуль потери смысла):

```text
> (`canonsim_unified_agent_pack` v1.5, `docs/SCALE_TESTING_LAW.md` +
> ULT §3/§17.2 — both paths inside that EXTERNAL pack, never this
> repo) — absorbed into the repo's verification owner because
```

Покрыты оба пути блока (SCALE_TESTING_LAW + ULT) — двусмысленность
снята одним маркером, форма «(внешний пак)» из строки бэклога
исполнена в языке дока (English).

## C. F3 — непиненая дословная копия ev_0007 → указатель (развилка решена)

**Развилка, оставленная iter-376 владельцу:** вариант A — пин копии
тестом; вариант B — изъять копию, оставить указатель. Владелец дал
добро на строку целиком, не выбрав вариант; выбор сделан по
собственным законам репо и стоящему приказу «логичнее и качественнее
на долгосрок» (2026-10-12):

- **D-024 (единый владелец факта):** дословный повтор — это второй
  источник истины; пин не устраняет дублирование, а вводит
  тест-механизм для его вечной синхронизации. Каждое будущее
  изменение схемы = правка двух доков или срабатывание синх-теста —
  постоянная плата за удобство, которое даёт один переход по ссылке.
- **§2.8 (admission):** минимальное вмешательство, нуль второй
  источника истины — вариант B и есть минимальная форма; вариант A —
  новая механика ради сохранения дубликата.
- **§6.1 (substance/cruft):** копия уже несёт указатель «Full
  contract: docs/EVENT_SCHEMA.md» — самопризнание вторичности;
  владелец §10 закреплён T0-пином (D-010: блоки ```json
  EVENT_SCHEMA.md извлекаются и валидируются при каждом прогоне).

**Исполнено (вариант B):** 18 строк копии в MVP_SCOPE §9 заменены
пятью строками указателя на EVENT_SCHEMA §10 («Example (canonical —
`ev_0007`)») с пометкой механизма пина и провенансом изъятия;
MVP_SCOPE 404 → 391 строка (−13). Все внешние ссылки на «MVP_SCOPE
§9» (core/intent.py, packlint/systems.py, INTENT_SCHEMA.md, ref/)
проверены — они цитируют ПРАВИЛА §9 (importance-правило и др.),
не копию; §10 MVP_SCOPE ссылается на `ev_0007` как на канонический
id — остался осмысленным (пример живёт в EVENT_SCHEMA §10).
**Вариант A остаётся одной итерацией по вызову** — если владельцу
важна инлайн-удобность примера в MVP_SCOPE, обратная правка
точечная и дешёвая.

## D. Верификация (полный пакет обязательных проверок, ПОСЛЕ правок)

- `PYTHONHASHSEED=0 python -m pytest -q` — **2629 passed + 27 failed
  + 1 skipped**: счётчики установлены полной переписью исходов
  (2629 точек + 27 F по прогрессу + 1 collection-skip модуля
  test_chronicle — duckdb в песочнице отсутствует, проверен отдельным
  прогоном «1 skipped»); итоговая строка счётчиков полным -q-прогоном
  в этой песочнице не печатается (окружение, не дефект репо —
  подмножества печатают её; итог снят переписью) и совпадает со
  строкой базлайна iter-376 дословно; состав провалов 27/27 —
  золотые байтовые сверки (известный T1 log-header env-набор
  3.12.15), флейков ноль;
- `ruff check .` — clean; `python scripts/docguard.py` — clean
  (капы: TASKS 596/600 — строка hygiene-1 свёрнута 17→15 физических
  строк, леджер +iter-377/−iter-365; MVP_SCOPE 391/600; TEST_PLAN
  917 — allowlist без изменений; STATUS 229; worklog 10 записей —
  iter-365 вытеснен по «один вошёл, один вышел»);
- `python scripts/topology.py` — clean (структура не менялась);
  `python scripts/digest.py` — parses, читает ту же строку тестов.
- INV-1..5 не тронуты: нуль строк кода поведения (правки —
  комментарии/докстринги/доки).

## E. Объём (§2.3 — сверх soft-лимита, отмечено в worklog)

3 файла фиксов (settings.py, test_inference.py, TEST_PLAN.md,
MVP_SCOPE.md — 4) + 4 райдера протокола (STATUS.md, worklog.md,
docs/TASKS.md, этот отчёт) = 8 изменённых/созданных. Развилка F3
решена внутри вызова без молчаливого выбора: обоснование §C,
обратный путь назван.

## Стоп-пойнт

Done: все три находки iter-376 закрыты одной R0-итерацией по
добро-вызову владельца (4 пути → пакет; внешний путь помечен;
копия ev_0007 → указатель по D-024, вариант A задокументирован как
дешёвая обратная правка); полный верификационный прогон — числа и
множество провалов идентичны базлайну.
Not done: ничего из строки hygiene-1; пограничный блок G9–G11
(FRONTEND_UIUX_LAW ↔ WORLD_PRESENTATION_LAW) не тронут — iter-376
не передал его в hygiene-1 (цитированная форма матрицы, без
рекомендации).
Next: третья голова measured-wall — director_global_passes (5.06
проф. с; Standing Order владельца не меняется) — либо следующий
вызов владельца.
Active KIs: KI#113, KI#121 (закрыт), KI#122 (закрыт) — без изменений.

## Владельческий git-блок (§12.3)

> ВАЖНО: origin/main на момент итерации = 8373c14 — райдеры
> iter-376 ещё не закоммичены у владельца. Дельта-архив этой
> итерации КУМУЛЯТИВЕН (содержит и райдеры iter-376 поверх
> BASE_COMMIT, и фиксы iter-377 поверх них) — безопасен в обоих
> состояниях: поверх неприменённого iter-376 или поверх
> применённого (повторное перечисление уже закоммиченного пути
> стейджит только реальный дифф). Блок ниже перечисляет объединение
> путей обеих итераций.

```
cd /c/Users/fallo/OneDrive/Desktop/repo/canonsim
git status --short
git add workbench/application/settings.py tests/test_inference.py docs/TEST_PLAN.md docs/MVP_SCOPE.md STATUS.md worklog.md docs/TASKS.md docs/iterations/iter-376-revision-report.md docs/iterations/iter-377-hygiene1-report.md
git status --short
git commit -m "iter-377-hygiene1: THE THREE REVISION FIXES (the owner's 'даю добро на hygiene-1' call, R0 text, zero behavior) - (1) the four stale workbench/application/inference.py comment paths re-pointed to the package (settings.py:30/121 + test_inference.py:2 -> inference/; settings.py:98 -> inference/migration.py, migrate_launch_semantics' own carrier since the iter-247 split); (2) TEST_PLAN 9.1's bare docs/SCALE_TESTING_LAW.md + ULT marked 'both paths inside that EXTERNAL pack, never this repo'; (3) MVP_SCOPE 9's unpinned verbatim ev_0007 copy replaced by the EVENT_SCHEMA 10 pointer (the single owner, test-pinned by T0/D-010) - the fork resolved to option B per D-024 (a pinned copy is a second truth source kept alive by test machinery; option A stays one iteration away on the owner's call); rides on top of the un-applied iter-376 riders (origin/main 8373c14) - the archive is cumulative and the git block safe in both states; 2629+27 (the known T1 set, IDENTICAL to the iter-376 baseline AFTER the fixes)+1, ruff+docguard+topology+digest clean, INV-1..5 untouched"
git push
```
