# GeoNames · `REFERENCES.md` §1 + §14 · CC-BY 4.0 · phase 5 (worldgen donors)

> Per-reference deep dive. Format template: `docs/REFERENCES_DEEP.md`
> §0. Iteration plan: `docs/REFERENCES_DEEP.md` §1. Anti-drift
> (D-026): catalog/license/URL/phase gating in `docs/REFERENCES.md`;
> one-line synthesis in `docs/CORE_DESIGN_RESEARCH.md` §2; concrete
> mechanics here. License filter and "patterns not content" rule:
> `REFERENCES.md` §0.7 (D-015). Source is **CC-BY 4.0** —
> attribution required; keep a `CREDITS.md` sidecar in any pack
> that uses GeoNames data (per `REFERENCES.md` §0.3). Data is
> downloadable as tab-delimited UTF-8 text dumps
> (`download.geonames.org/export/dump/`). Catalog §1 row reads
> "GeoNames | CC-BY 4.0 (terms apply) | toponyms, settlement
> hierarchies | 5"; this per-ref file expands the dump format,
> feature-class/code enum, hierarchy scheme, and alternate-names
> table. Feature codes below are verified against
> `download.geonames.org/export/dump/featureCodes_en.txt` on
> 2026-08-26 (684 codes across 9 classes, not the 645 the readme
> claims — the readme is stale; the dump is the source of truth).

**What it is.** GeoNames is a geographical database covering all
countries, distributed as free downloadable dumps under CC-BY
4.0 (attribution required). The dump format is tab-delimited
UTF-8 text, refreshed daily (with `modifications-<date>.txt` +
`deletes-<date>.txt` daily deltas). The database contains over
25 million geographical names, over 12 million unique features
(of which 4.8 million populated places and 16 million alternate
names). All features are categorized into one of **9 feature
classes** and further sub-categorized into one of **684 feature
codes** (per the live `featureCodes_en.txt` dump on 2026-08-26;
the readme.txt still says 645, which is stale). WGS84 lat/long.
Wiki-editable; the dump is the canonical export. The precedent
for our phase-5 worldgen **real-world toponym source**: settlement
hierarchies, multilingual place names, admin divisions. CC-BY
4.0 = attribution sidecar required at intake.

**Concrete mechanics.**

- **The `geoname` table — the per-feature record.** Per the
  `download.geonames.org/export/dump/readme.txt` contract, the
  main table has these fields (in column order):
  `geonameid` (integer id, the primary key),
  `name` (UTF-8 name, varchar(200)),
  `asciiname` (ASCII transliteration, varchar(200)),
  `alternatenames` (comma-separated list of alternate names,
  a convenience field duplicated from the alternatenames
  table, varchar(10000)),
  `latitude` (decimal degrees, WGS84),
  `longitude` (decimal degrees, WGS84),
  `feature class` (single char, see below),
  `feature code` (varchar(10), see below),
  `country code` (ISO-3166 2-letter),
  `cc2` (alternate country codes, comma-separated ISO-3166
  2-letter),
  `admin1 code` (first-order administrative division code,
  varchar(20)),
  `admin2 code` (second-order administrative division,
  varchar(80)),
  `admin3 code` (third-level, varchar(20)),
  `admin4 code` (fourth-level, varchar(20)),
  `population` (bigint),
  `elevation` (meters, integer),
  `dem` (digital elevation model, SRTM3 or GTOPO30, average
  elevation of 90m or 900m cell),
  `timezone` (IANA timezone id, varchar(40)),
  `modification date` (yyyy-MM-dd, last modification).
  The pattern: **a flat per-feature record with primary key +
  display name + ASCII fallback + multilingual alternates +
  lat/long + typed feature + admin hierarchy + population +
  elevation + timezone**. Our `entities.json` records inherit
  the shape: per-entity record with primary key + display
  name + type + position + relations; the multilingual
  alternates are inherited via `templates.json` localized
  name sets (cf. `natural_earth.md`).
- **9 feature classes — the top-level closed enum.** The
  `feature class` field is a single char with 9 values: `A`
  (country, state, region, ... administrative divisions),
  `H` (stream, lake, ... hydrographic),
  `L` (area, locality, ... locality type),
  `P` (populated place — city, town, village),
  `R` (road, railroad, ... transportation),
  `S` (spot — building, farm, mine, ...),
  `T` (mountain, hill, rock, ... terrain),
  `U` (undersea — seamount, trench, ...),
  `V` (forest, heath, ... vegetation).
  Each class has 40–200 feature codes for sub-types. The
  pattern: **a single-char top-level enum + sub-type codes**.
  Our `entities.json` `entity_type` enum inherits the shape:
  a small closed enum at the top, with per-type field
  refinements.
- **684 feature codes — the per-subtype enum.** Each feature
  class has sub-type codes formatted `<class>.<code>`. The
  live `featureCodes_en.txt` file is the authoritative list
  (one code per line, format `<code>\t<name>\t<description>`);
  the readme.txt's "645 codes" claim is stale (it lags the
  wiki-editable live dump). Sample of verified codes per
  class (verified 2026-08-26 against
  `download.geonames.org/export/dump/featureCodes_en.txt`):
  - `A.ADM1` (first-order administrative division), `A.ADM2`/
    `A.ADM3`/`A.ADM4`/`A.ADM5` (second/third/fourth/fifth-
    order), `A.ADM1H`/`A.ADM2H`/`A.ADM3H`/`A.ADM4H`/`A.ADM5H`
    (historical admin divisions, one per level), `A.ADMD`
    (administrative division, undifferentiated as to level),
    `A.ADMDH` (historical admin division, undifferentiated),
    `A.ADMS` (school district), `A.LTER` (leased area, usually
    military), `A.PCL` (political entity), `A.PCLD` (dependent
    political entity), `A.PCLF` (freely associated state),
    `A.PCLH` (historical political entity), `A.PCLI`
    (independent political entity), `A.PCLIX` (section of
    independent political entity), `A.PCLS` (semi-independent
    political entity), `A.PRSH` (parish), `A.TERR` (territory),
    `A.ZN` (zone), `A.ZNB` (buffer zone).
  - `H.BAY` (bay), `H.BAYS` (bays), `H.CNL` (canal), `H.CNLA`
    (aqueduct), `H.CNLB` (canal bend), `H.CNLD` (drainage
    canal), `H.CNLI` (irrigation canal), `H.CNFL` (confluence),
    `H.CHN` (channel), `H.CHNL` (lake channel), `H.CHNM`
    (marine channel), `H.CHNN` (navigation channel).
  - `L.AREA` (area, no homogeneous character), `L.CONT`
    (continent), `L.RGN` (region), `L.RGNE` (economic region),
    `L.RGNH` (historical region), `L.RGNL` (lake region),
    `L.MILB` (military base), `L.NVB` (naval base), `L.OAS`
    (oasis), `L.PRK` (park), `L.PRT` (port), `L.RES` (reserve),
    `L.RESA` (agricultural reserve), `L.RESF` (forest reserve),
    `L.RESH` (hunting reserve), `L.RESN` (nature reserve),
    `L.RESP` (palm tree reserve), `L.RESV` (reservation, for
    aboriginal/tribal/native populations), `L.RESW` (wildlife
    reserve), `L.SNOW` (snowfield), `L.TRB` (tribal area).
  - `P.PPL` (populated place — city, town, village), `P.PPLA`
    (seat of first-order admin division), `P.PPLA2`/`P.PPLA3`/
    `P.PPLA4`/`P.PPLA5` (seats of second/fourth/fifth-order),
    `P.PPLC` (capital of political entity), `P.PPLCD` (capital
    of dependency/special area), `P.PPLCH` (historical capital),
    `P.PPLF` (farm village), `P.PPLG` (seat of government),
    `P.PPLH` (historical populated place), `P.PPLL` (populated
    locality), `P.PPLQ` (abandoned populated place), `P.PPLR`
    (religious populated place), `P.PPLS` (populated places),
    `P.PPLW` (destroyed populated place), `P.PPLX` (section of
    populated place), `P.STLMT` (Israeli settlement).
  - `R.RD` (road), `R.RDA` (ancient road), `R.RDB` (road bend),
    `R.RDCUT` (road cut), `R.RDJCT` (road junction), `R.RJCT`
    (railroad junction), `R.RR` (railroad), `R.RRQ` (abandoned
    railroad), `R.RTE` (caravan route), `R.RYD` (railroad yard),
    `R.ST` (street), `R.STKR` (stock route), `R.TNL` (tunnel),
    `R.TNLN` (natural tunnel), `R.TNLRD` (road tunnel),
    `R.TNLRR` (railroad tunnel), `R.CSWY` (causeway), `R.OILP`
    (oil pipeline), `R.PRMN` (promenade), `R.PTGE` (portage).
  - `S.ADMF` (administrative facility), `S.AGRF` (agricultural
    facility), `S.AIRB` (airbase), `S.AIRF` (airfield), `S.AIRH`
    (heliport), `S.AIRP` (airport), `S.AIRQ` (abandoned airfield),
    `S.AIRT` (airport terminal), `S.ANS` (archaeological/
    prehistoric site), `S.BLDG` (building(s)), `S.CMP` (camp),
    `S.CMPL` (logging camp), `S.CMPLA` (labor camp), `S.CMPMN`
    (mining camp), `S.CMPO` (oil camp), `S.CMPQ` (abandoned camp),
    `S.CMPRF` (refugee camp), `S.CMTY` (cemetery), `S.COMC`
    (communication center), `S.CRRL` (corral), `S.CSNO` (casino),
    `S.CSTL` (castle), `S.CSTM` (customs house), `S.CTHSE`
    (courthouse).
  - `T.CAPE` (cape), `T.CLF` (cliff), `T.BCH` (beach), `T.BCHS`
    (beaches), `T.BDLD` (badlands), `T.BUTE` (butte), `T.ATOL`
    (atoll), `T.BAR` (bar — shallow ridge), `T.BLDR` (boulder
    field), `T.BLHL` (blowhole), `T.BLOW` (blowout), `T.BNCH`
    (bench), `T.ASPH` (asphalt lake), `T.CFT` (cleft), `T.CLDA`
    (caldera).
  
  The pattern: **a closed enum of `<class>.<code>` pairs covering
  the geographic taxonomy**. Our `entities.json` `entity_type`
  enum is the small subset (4 entity types in phase 0: NPC, item,
  place, concept); we don't need 684 codes.
- **Admin hierarchy — the parent/child chain.** The `admin1`/
  `admin2`/`admin3`/`admin4` code fields form a 4-level
  hierarchy: country (by `country code`) → admin1 → admin2 →
  admin3 → admin4 → feature. The pattern: "the corresponding
  admin feature is found with the same countrycode and adminX
  codes and the respective feature code ADMx" — the hierarchy
  is implicit in the codes, not stored as a tree. The
  `hierarchy.zip` file (parentId, childId, type) is the
  explicit version: `type 'ADM'` for the admin hierarchy
  (derived from admin1-4 codes), `type 'related'` for
  user-entered relations, etc. The pattern: **implicit
  hierarchy via codes + explicit hierarchy via a separate
  parent/child file**. Our `relations.json` (P2a in
  `MVP_SCOPE.md` §4.2) inherits the shape: pair-keyed
  relation map with typed relations; the typed enum is closed.
- **`alternatenames` table — the multilingual name family.**
  Separate table, one row per (feature, name). Fields:
  `alternateNameId` (int),
  `geonameid` (foreign key to geoname),
  `isolanguage` (ISO 639 2- or 3-char language code,
  optionally with a hyphen and a country code for regional
  variants like `zh-CN` or a variant name like `zh-Hant`;
  4-char `post` for postal codes; `iata`, `icao`, `faac` for
  airport codes; `fr_1793` for French Revolution names; `abbr`
  for abbreviation; `link` for website link (mostly Wikipedia);
  `wkdt` for wikidata id),
  `alternate name` (UTF-8 string),
  `isPreferredName` (1/0 — official/preferred name),
  `isShortName` (1/0 — short form like "California" for "State of California"),
  `isColloquial` (1/0 — slang like "Big Apple" for New York),
  `isHistoric` (1/0 — former name like "Bombay" for Mumbai),
  `from` (period — when the name was used),
  `to` (period — when the name stopped being used).
  The pattern: **per-feature multilingual name records with
  type flags + period-of-use bounds**. Our `templates.json`
  localized name sets inherit the shape (one symbol per
  language per entity), with `isHistoric` + `from`/`to` as
  the precedent for naming-over-time events in our phase-3+
  chronicle (a state renamed → the new name is a new record
  with `from` = the rename tick).
- **Per-country dump + all-countries dump.** Dumps are
  per-country (XX.zip where XX = ISO-3166 2-letter country
  code; `no-country` for features not belonging to a country)
  and a combined `allCountries.zip`. City-only subsets:
  `cities500.zip` (population > 500 or PPLA4 seats),
  `cities1000.zip` (> 1000 or PPLA3), `cities5000.zip` (>
  5000 or PPLA), `cities15000.zip` (> 15000 or capitals). The
  pattern: **subsets by population threshold**. Our
  `content/packs/<pack>/entities.json` inherits the shape:
  the full dataset is the source of truth; subsets are
  convenience cuts (the simulation loads only what it needs).

**What we take.**

- The 9-class / 684-code feature-class enum is the precedent
  for our `entities.json` `entity_type` enum (closed enum at
  the top, per-type field refinements). The shape is direct;
  the scale is trimmed (4 types in phase 0 vs 9 classes +
  684 codes in GeoNames).
- The admin-hierarchy code chain (`admin1` → `admin2` →
  `admin3` → `admin4` + the `hierarchy.zip` explicit
  parent/child file) is the precedent for our `relations.json`
  pair-keyed relation map (P2a). The shape: implicit hierarchy
  via codes + explicit typed parent/child pairs.
- The `alternatenames` table (per-feature multilingual name
  records with `isPreferredName`/`isShortName`/`isColloquial`/
  `isHistoric`/`from`/`to` flags) is the precedent for our
  `templates.json` localized name sets + the chronicle event
  for renaming (a new name is a new record with `from` tick).
- The `modifications-<date>.txt` + `deletes-<date>.txt` daily
  delta files are the precedent for our `Intent` → `Event`
  validation front-door: changes are explicit records, not
  in-place edits (INV-5: corrections are new events).

**What we adapt.**

- The CC-BY 4.0 license requires attribution. Adaptation: a
  `CREDITS.md` sidecar in any content pack that uses GeoNames
  data (per `REFERENCES.md` §0.3) — the sidecar is mandatory
  at intake.
- The 684-code feature-class enum is too rich for our phase-0
  needs; we adapt by trimming to a small set of entity types
  (4 in phase 0: NPC, item, place, concept). The closed-enum
  shape is preserved; the scale is trimmed.
- The lat/long + admin1-4 hierarchy is for real-world
  geography; we adapt by lifting only the per-feature
  metadata into our entities and the typed-relation pattern
  into `relations.json`. The geography is not used in phase
  0 (the spatial layer is a phase-5+ concern).

**What inspires us.**

- The dump readme's "this work is licensed under a Creative
  Commons Attribution 4.0 License" + the daily
  modifications/deletes delta files: the lesson that **a
  dataset can be a live append-only log**, not just a
  snapshot. GeoNames publishes deltas; consumers sync by
  applying the deltas in order. Our INV-1 + INV-5
  (event sourcing + log immutability) is the same principle,
  applied to the canon log: the log is append-only, every
  change is a new event, no edits ever.

**Strengths.**

- CC-BY 4.0 — the most permissive license that still requires
  attribution; data is freely copyable, modifiable,
  redistributable. The attribution sidecar is a small price.
- 25M+ names, 12M+ features, 684 feature codes — the
  richest public-domain/CC-BY toponym source available.
- The admin-hierarchy code chain (admin1-4 + the explicit
  `hierarchy.zip` file) is the cleanest precedent for typed
  parent/child relations; the shape is direct.
- The `alternatenames` table's `isHistoric` + `from`/`to`
  flags are the cleanest precedent for naming-over-time
  events; the shape is direct.
- Daily delta files (`modifications-<date>.txt` +
  `deletes-<date>.txt`) are the cleanest precedent for
  append-only log discipline; INV-1 + INV-5 inherit the shape.
- 50+ localized-name variants per feature (via the
  alternatenames table's `isolanguage` field) — the most
  multilingual public-domain/CC-BY toponym source available
  at this scale.

**Weaknesses.**

- The dump is **tab-delimited text**, not structured — the
  consumer must parse the columns by position. INV-3 (no
  domain words in code) forbids us from hard-coding the
  column order; we lift the schema into `entities.json` and
  use a loader that reads the schema from a sidecar.
- The lat/long fields are **floating-point** — INV-2 forbids
  floating-point in the canonical path. We lift only the
  per-feature metadata in phase 0, defer the geometry to
  phase 5+ when we can decide the spatial representation.
- The 684-code feature-class enum is **over-specified** for
  fantasy-world use — many codes (e.g., `S.AIRB` for airbase,
  `R.RR` for railroad) don't apply to a pre-industrial fantasy
  setting. We adapt by trimming to a small set of entity
  types.
- The readme.txt's "645 codes" claim is **stale** — the live
  dump has 684. This is a documentation lag, not a content
  bug; the dump is the source of truth. (Logged here as a
  doc↔repo drift catch in the same class as the catalog
  row "chronology generator" vs the actual Azgaar repo
  — cf. `azgaar_fmg.md` §"catalog row drift".)
- The CC-BY 4.0 license requires attribution; the sidecar
  must be maintained at every intake. This is a small price
  but a real obligation (cf. `natural_earth.md` public
  domain, which has no such obligation).
- The dump is **real-world** — it's not the right source for
  fantasy-world toponyms. It is the precedent for shape
  (typed relations, multilingual names, append-only deltas),
  not for content. For content, `azgaar_fmg.md` and a future
  fantasy toponym source are better fitted.

**Verdict.** Phase-5 worldgen donor reference, mostly positive
on shape (the 9-class / 684-code feature-class enum, the
admin-hierarchy code chain + explicit typed parent/child file,
the alternatenames table with `isHistoric`/`from`/`to` flags,
the daily delta files are all direct inheritances), explicitly
negative on tab-delimited format (INV-3 fix: schema in sidecar,
not in code) + floating-point lat/long (INV-2 fix: lift
metadata only in phase 0) + 684-code enum scale (trim to 4
types in phase 0) + real-world-only content (the right shape
for our `entities.json` + `relations.json` + chronicle rename
events, but not the right content for a fantasy world). CC-BY
4.0 attribution sidecar is a small price for the richest
public toponym source. The "dataset as append-only log" lesson
(daily modifications/deletes deltas) is the design principle
that shapes INV-1 + INV-5 (event sourcing + log immutability).
The readme.txt's stale "645 codes" claim is a documentation
lag — the live dump is the source of truth (684 codes as of
2026-08-26); this per-ref file uses the verified count.

---

← Back to [`docs/REFERENCES_DEEP.md`](../REFERENCES_DEEP.md) index.
