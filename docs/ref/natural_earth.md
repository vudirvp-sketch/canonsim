# Natural Earth · `REFERENCES.md` §1 + §14 · public domain · phase 5 (worldgen donors)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is **public domain** — the
> most permissive license possible; data is freely copyable,
> modifiable, redistributable, even commercially (per the project
> README "free for use in any type of project"). Reference repo:
> `nvkelso/natural-earth-vector` (vector data; raster data in
> `nvkelso/natural-earth-raster`). The catalog §1 row reads
> "Natural Earth | public domain | regions, rivers, coastlines |
> 5"; this per-ref file expands the data shape (themes, scales,
> properties, versioning) and the per-feature schema.

**What it is.** Natural Earth is a public-domain vector + raster
map dataset of the world, built through a collaboration of many
volunteers and supported by NACIS (North American Cartographic
Information Society). Available at three scales — **1:10m** (high
detail, ~22 MB for cultural vectors), **1:50m** (medium detail),
**1:110m** (low detail, ~500 KB for cultural vectors) — with
tightly integrated vector and raster data. The vector data is
GeoJSON (or Shapefile) at the `geojson/` and `ne_*.shp` paths; the
raster data is in the sibling `natural-earth-raster` repo. The
project uses **semantic versioning** (X.Y.Z; major = breaking
changes to file/column names; minor = additions; patch = bug
fixes). The dataset is the precedent for our phase-5 worldgen
**real-world reference layer**: regions, rivers, coastlines,
country borders, urban areas. Public-domain — no license friction
at intake.

**Concrete mechanics.**

- **Three scales — the LOD (level of detail) ladder.** Each theme
  is published at three scales: `ne_10m_<theme>.geojson`,
  `ne_50m_<theme>.geojson`, `ne_110m_<theme>.geojson`. The
  1:10m scale has the most features (~247 countries, thousands
  of rivers); the 1:110m scale has the fewest (~57 countries
  with simplified geometry). The pattern: **the same theme at
  three LODs** — the consumer picks the right scale for the
  zoom level. Our phase-5 LOD ladder (`MVP_SCOPE.md` §15, D-023
  runtime-vs-fold) inherits this shape: the canon log is the
  ground truth; per-NPC projections and brief cache are LOD
  layers above it.
- **Themes — the per-domain file split.** The `geojson/`
  directory groups files by theme + scale:
  **physical** (coastline, land, ocean, rivers_lake_centerlines,
  lakes, glaciated_areas, bathymetry, geographic_lines,
  graticules_1, wgs84_bounding_box, land_ocean_seams),
  **cultural** (admin_0_countries, admin_0_seams, admin_1_states_provinces,
  admin_1_seams, populated_places, urban_areas, roads,
  railroads, airports, ports, parks_and_protected_areas,
  10m_admin_0_scale_rank, 10m_lakes_europe, 10m_lakes_north_america),
  **raster** (in the sibling repo). The pattern: **per-theme
  file split** — each theme is a separate file with a clear
  scope. Our phase-3+ content packs (`content/packs/<pack>/`)
  inherit this shape (one file per category: `entities.json`,
  `actions.json`, `rules.json`, `templates.json`).
- **`featurecla` — the closed feature-class enum.** Every
  feature in a Natural Earth file carries a `featurecla`
  property that names its class. From
  `ne_110m_admin_0_countries.geojson` features[0]: `featurecla:
  'Admin-0 country'`. Other values: `Admin-0 country`,
  `Admin-0 sovereignty`, `Admin-1 state, province`,
  `Admin-1 region`, `Populated place`, `Urban area`, etc.
  The pattern: **a closed enum on each feature** — the dataset
  is self-describing; the consumer knows the type from the
  record, not from the filename. Our `EVENT_SCHEMA.md` §2
  `event_type` enum + `entities.json` `entity_type` enum
  inherit this shape — every record carries its type.
- **`admin_0_countries` properties — the per-record schema.**
  The 1:110m admin-0 file (the smallest, smallest schema)
  has 155 properties per feature including: `featurecla`,
  `scalerank` (int), `LABELRANK` (int), `SOVEREIGNT` (string),
  `SOV_A3` (3-letter code), `ADM0_DIF` (int), `LEVEL` (int),
  `TYPE` (string — "Sovereign country", "Country", etc.),
  `ADMIN` (display name), `ADM0_A3` (3-letter code), `GEOUNIT`,
  `GU_A3`, `SUBUNIT`, `SU_A3`, `BRK_DIFF`, `NAME`, `NAME_LONG`,
  `BRK_A3`, `BRK_NAME`, `BRK_GROUP`, `ABBREV`, `POSTAL`,
  `FORMAL_EN`, `FORMAL_FR`, `NAME_CIAWF`, `NOTE_ADM0`,
  `NOTE_BRK`, `NAME_SORT`, `NAME_ALT`, `MAPCOLOR7`/`8`/`9`/`13`
  (int 1..N — the suggested map color), `POP_EST` (int),
  `POP_RANK` (int 1..N), `POP_YEAR` (int year), `GDP_MD` (int
  million USD), `GDP_YEAR`, `ECONOMY` (string — "1. Developed
  region: G7"), `INCOME_GRP` (string — "1. High income: OECD"),
  `FIPS_10`, `ISO_A2`/`A2_EH`, `ISO_A3`/`A3_EH`, `ISO_N3`/
  `N3_EH`, `UN_A3`, `WB_A2`, `WB_A3`, `WOE_ID`, `CONTINENT`,
  `REGION_UN`, `SUBREGION`, `REGION_WB`, `NAME_LEN`,
  `LONG_LEN`, `ABBREV_LEN`, `TINY` (int 0/1), `HOMEPART`,
  `MIN_ZOOM`, `MIN_LABEL`, `MAX_LABEL`, `LABEL_X`, `LABEL_Y`,
  `NE_ID`, `WIKIDATAID`, and ~50 localized name fields
  (`NAME_AR`, `NAME_BN`, `NAME_DE`, `NAME_EN`, `NAME_ES`,
  ... `NAME_ZH`, `NAME_ZHT`) and ~30 `FCLASS_<country>` fields
  (the feature class in the named country's classification
  system). The pattern: **a rich per-record schema with
  multiple foreign-key systems (ISO, FIPS, UN, WB, WOE,
  WIKIDATA) + localized names + economic/population data**.
  Our `entities.json` `entity_type` enum + per-type fields
  inherit the shape (closed enum + per-type fields), not the
  scale (we don't need 155 properties per entity in phase 0).
- **`MAPCOLOR7`/`8`/`9`/`13` — precomputed display color.**
  Each country has 4 integer color suggestions (one per map
  palette size — 7-color, 8-color, 9-color, 13-color). The
  pattern: **precomputed presentation hints on the data record**
  — the renderer picks the palette size, the data carries the
  color. Our `render/` templates inherit the shape: the data
  carries display hints, the renderer picks the format.
- **Localized names — the multilingual toponym field family.**
  The 50 `NAME_<lang>` fields on each admin-0 record provide
  the country's name in 25 languages (`NAME_AR` for Arabic,
  `NAME_BN` for Bengali, `NAME_DE` for German, `NAME_EN` for
  English, `NAME_ES` for Spanish, `NAME_FA` for Persian,
  `NAME_FR` for French, `NAME_EL` for Greek, `NAME_HE` for
  Hebrew, `NAME_HI` for Hindi, `NAME_HU` for Hungarian,
  `NAME_ID` for Indonesian, `NAME_IT` for Italian, `NAME_JA`
  for Japanese, `NAME_KO` for Korean, `NAME_NL` for Dutch,
  `NAME_PL` for Polish, `NAME_PT` for Portuguese, `NAME_RU`
  for Russian, `NAME_SV` for Swedish, `NAME_TR` for Turkish,
  `NAME_UK` for Ukrainian, `NAME_UR` for Urdu, `NAME_VI` for
  Vietnamese, `NAME_ZH` for Chinese, `NAME_ZHT` for Chinese
  Traditional). The pattern: **one field per language** —
  the schema is the multilingual table. Our `templates.json`
  localized name sets inherit the shape (one symbol per
  language; the renderer picks by locale).
- **Semantic versioning — the data-layout contract.** The
  README documents the versioning scheme explicitly:
  **major** = breaking changes to file names / column names /
  `FeatureCla` enum values / admin-0 additions or deletions /
  significant new themes; **minor** = additions, deletions,
  any shape or attribute changes in admin-1 / any theme /
  major shape changes / `FeatureCla` value additions; **patch**
  = minor shape changes / bug fixes. The pattern: **the data
  layout is the API** — consumers can pin to a major version
  and trust stability. Our `schemas/event.schema.json`
  `schema_version` field (per `EVENT_SCHEMA.md` §3) inherits
  the shape: a breaking change requires a major bump + a
  migration note.

**What we take.**

- The three-scale LOD ladder (1:10m / 1:50m / 1:110m) is the
  precedent for our phase-5 LOD system (canon log = ground
  truth; per-NPC projection = mid LOD; brief cache = top
  LOD). The shape is direct.
- The `featurecla` closed-enum-on-each-record pattern is the
  precedent for `entities.json` `entity_type` enum and
  `EVENT_SCHEMA.md` §2 `event_type` enum — every record
  carries its type.
- The semantic-versioning scheme (X.Y.Z with documented major
  / minor / patch boundaries) is the precedent for
  `schemas/event.schema.json` `schema_version` field and the
  §3 migration rule.
- The per-theme file split (one file per domain: physical,
  cultural, populated_places, urban_areas, ...) is the
  precedent for `content/packs/<pack>/` per-category file
  split (`entities.json`, `actions.json`, `rules.json`,
  `templates.json`).
- The localized-name field family (`NAME_<lang>`) is the
  precedent for `templates.json` localized name sets — one
  symbol per language; the renderer picks by locale.

**What we adapt.**

- The 155-property per-record schema is too rich for our
  phase-0 needs; we adapt by trimming to a small set of
  named fields per entity type (the closed enum is preserved,
  the field set is trimmed to what the simulation uses).
- The vector geometry (polygons for countries, lines for
  rivers) is not used in phase 0 (no spatial layer yet); we
  adapt by lifting only the per-record metadata (the
  properties) into our content packs. The geometry is a
  phase-5+ concern (when the spatial layer is added).
- The `MAPCOLOR*` fields are display hints for the renderer;
  our `render/` templates inherit the shape but use template
  tokens (`#color.state1#`, `#color.state2#`) instead of
  numeric color ids.

**What inspires us.**

- The README's "Neatness Counts" section: "the carefully
  generalized linework maintains consistent, recognizable
  geographic shapes at 1:10m, 1:50m, and 1:110m scales. Natural
  Earth was built from the ground up so you will find that all
  data layers align precisely with one another. For example,
  where rivers and country borders are one and the same, the
  lines are coincident." The lesson: **multiple LODs of the
  same data should be coherent** — the high-detail version
  is not a different dataset, it is a richer projection of
  the same ground truth. Our phase-5 LOD ladder inherits
  this discipline: the canon log is the ground truth; per-NPC
  projections and brief cache are LODs of the same data.

**Strengths.**

- Public domain — the most permissive license; no license
  friction at intake; data is freely copyable, modifiable,
  redistributable, even commercially.
- Three-scale LOD ladder is a clean, documented abstraction
  for "the same data at multiple zoom levels".
- `featurecla` closed-enum-on-each-record is a clean
  self-describing record pattern; the consumer doesn't need
  to know the file's theme to know the record's type.
- Semantic versioning with documented major / minor / patch
  boundaries is a clean data-layout contract; consumers can
  pin to a major version.
- 50 localized-name fields per admin-0 record — the most
  multilingual public-domain toponym source available at
  this scale (GeoNames is richer in toponym count but
  sparser in per-record multilingual coverage).

**Weaknesses.**

- The 155-property per-record schema is **heavy** — most
  consumers use only 5–10 fields; the rest is overhead for
  our use case. We adapt by trimming.
- The vector geometry (polygons, lines) is **floating-point**,
  which is not byte-identical-replayable across GIS libraries
  (GDAL, GEOS, Shapely each have float drift). INV-2 forbids
  floating-point in the canonical path; we lift only the
  metadata in phase 0, defer geometry to phase 5+.
- The dataset is **not** the right source for fantasy-world
  toponyms — it's a real-world dataset. It is the precedent
  for shape (LOD ladder, per-theme split, closed enum), not
  for content. For content, `GeoNames` (`geonames.md`) is
  the richer toponym source.
- The dataset is **big** — the 1:10m admin-0 file is ~21 MB
  of GeoJSON; the full dataset is several gigabytes. Our
  phase-0 needs ~10 records; we lift the shape, not the
  scale.

**Verdict.** Phase-5 worldgen donor reference, mostly positive
on shape (the three-scale LOD ladder, the `featurecla` closed
enum, the semantic-versioning scheme, the per-theme file
split, the localized-name field family are all direct
inheritances), explicitly negative on per-record schema
heaviness (155 properties; trim to what the simulation uses)
+ floating-point geometry (INV-2 fix: lift metadata only in
phase 0, defer geometry to phase 5+) + dataset scale (several
GB; lift the shape, not the data). Public domain is the most
permissive license possible; no license friction at intake.
The "multiple LODs of the same data should be coherent"
lesson is the design principle for our phase-5 LOD ladder
(canon log = ground truth; per-NPC projection = mid LOD;
brief cache = top LOD).

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
