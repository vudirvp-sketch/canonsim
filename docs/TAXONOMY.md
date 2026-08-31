# TAXONOMY.md — DF Event Taxonomy (bg-2)

> The bg-2 deliverable (`docs/TASKS.md` Track B): 120 real Dwarf Fortress
> events across the 16 target types — birth, death, murder, theft, betrayal,
> artifact creation, site destruction, war, journey, captivity, escape,
> founding, item loss, madness, transformation, catastrophe — each carrying
> participants, place, cause, witness, long-term consequence, and the
> expressibility verdict against our event contract (`docs/EVENT_SCHEMA.md`).
> AC (≥100 entries): **MET — 120 entries**.

## 1. Method

- Source: the owner's large-world export `region2-00500-01-01` (2.38 GB,
  500y), imported into the SQLite sink **v2 with the plus companion**
  (`scripts/df_import.py`: 1,191,388 events · 197,051 collections · 98,001
  figures · 3,509,709 `event_plus_fields` rows). The other three exports
  (small/medium/small-dense) remain valid sources — `docs/TECH_NOTES.md` §3.1
  measured them; the taxonomy runs on the large world because it alone
  reaches the full 101-type event union.
- Tool: `scripts/df_taxonomy.py <db>` — 15 event-type plans + 1 measured gap
  (birth) + 2 collection plans (war, beast attack). Selection is a fixed
  quantile spread over the id-ascending candidate list — the report is a pure
  function of the DB content (no RNG, no wall-clock); re-running reproduces
  every row.
- Columns: participants/place resolve through the sink's name surfaces
  (figure names, site names, entity names, artifact names). **Cause is
  reconstructed**, never parsed — from role fields (slayer, snatcher,
  corruptor, changer) and `event_collections` grouping (`TECH_NOTES.md` §3).
  **Witness** = the nearest `hfs formed reputation relationship` event
  involving the entry's figures within ±10y — the closest DF analog of a
  knowledge record; "—" means none exists (the norm). **Consequence** = the
  next recorded log facts involving the entry's participants/artifact/site —
  what the export actually shows later, no narrative inference.
- The §2 verdict applies to every row of its section (expressibility is a
  property of the event type's field shape, not of the instance).
- Full-fidelity report: `output/df_taxonomy_<stem>.txt` (gitignored runtime
  artifact, reproducible via import → survey). This doc distills it; every id
  below is queryable in the DB.
- Honest limits: war casualty sums are lower bounds (identical repeated
  `attacking_squad_deaths` values collapse in the EAV dedup); escape has no
  dedicated DF type (ransoms are the recorded captivity exit); birth has no
  event type at all.

## 2. Type map — DF source → our ontology verdict

Verdict legend: **E** = expressible today (fields map onto
`docs/EVENT_SCHEMA.md` §2 + the `outcome` payload); **E+** = expressible,
needs the plus companion's fields (sink v2); **R** = reconstructed (no single
DF type carries the pattern — a family of events implies it); **GAP** = DF
records nothing; our schema is the richer side.

| target | DF source(s) | candidates (large) | verdict | mapping onto our contract |
|---|---|---|---|---|
| birth | none (figure `birth_year`) | 0 events · 98,001 figures | GAP | ours: `actor=world` event + `state_changes` birth; DF is derivable-only |
| death | `hf died` (old age/struck/shot) | 39,590 site-bearing of 87,613 | E | actor=slayer or world, target=victim, `outcome.cause`; `state_changes` death, `irreversible` |
| murder | `hf died` cause `murdered` | 5,786 (all carry slayer+site) | E | + our crime chain (knowledge→suspicion→arrest) has no DF donor: convictions exist, rumor propagation does not |
| theft | `item stolen` (+ `theft` collections) | 22,399 | E+ | thief/item/method live ONLY in the plus companion (`histfig`/`mat`/`theft_method`); DF theft is artifact-theft — the F7 macro/micro asymmetry |
| betrayal | `hfs formed intrigue relationship` (+ `assume identity`) | 5,209 / 9,977 | R | corruptor/target/method/action/successful → `outcome`; ours: phase-4 crafted lies (EVENT_SCHEMA §3 "a lie is a crafted record") |
| artifact creation | `artifact created` | 26,846 with creator+site | E | creator/artifact/site → `outcome`; custody chain = follow-ups (stored/given/lost) |
| site destruction | `destroyed site` (+ `hf destroyed site`, `razed structure`) | 250 / 275 / 870 | E | attacker/defender civs → entity slots; our fire layer + `spot_state` (D-057) is the micro analog |
| war | `war` collections → battles → events | 990 wars · 11,849 battles | E (grouping) | single-parent collection tree → our linear `cause` chain; multi-parent groupings defer to phase 3+ (EVENT_SCHEMA §11); casualties = cardinality events (GROUP_SPEC, phase 5) |
| journey | `hf travel` (+ `journey` collections) | 3,086 site-bearing of 6,218 | E | traveler/site/return-flag → `outcome`; collections group the legs |
| captivity | `hf abducted` (+ `hf enslaved`, `hf ransomed`) | 4,991 / 23 / 12 | E | snatcher/victim roles; abduction collections group the episode |
| escape | `hf ransomed` (+ `change hf state` reason `flight`) | 12 | near-GAP | no escape event type; ours: the flee action exists (phase 0); DF flight is a state-change reason |
| founding | `created site` (+ `entity created`, `created structure`) | 562 with builder / 3,960 / 4,118 | E | civ/builder → `outcome`; site's later fate = follow-ups |
| item loss | `artifact lost` (+ `artifact destroyed`, `artifact given`) | 2,774 / 682 / 3,354 | E | artifact/site → `outcome`; mostly terminal (measured §4.6) |
| madness | `change hf state` `mood` | 179 | E | mood enum (fey/secretive/possessed/insane/melancholy/macabre/berserk/fell) → `state_changes` on a status axis; `failed mood` reason is the counter-event |
| transformation | `changed creature type` | 1,356 | E | changee/changer/old→new race; `state_changes` race, `irreversible` (night-creature conversions) |
| catastrophe | `beast attack` collections (+ `creature devoured`) | 13,289 / 16,413 | E+ | eater/victim/race from the plus pass; the beast is an actor entity; attacks are macro collections (GROUP_SPEC cardinality) |

## 3. The 120 entries

Rows are the quantile spread (8 per target); `sNNN` = site id; `(id, RACE)`
= figure id and race from the sink; ev ids are `events.id`. "—" = nothing
recorded. The §2 verdict column applies row-wise.

### birth — measured gap

- measured: 98,001 figures carry birth_year (-275 .. 499) — derivable, never evented.

### death — DF 'hf died' · 39,590 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `4217` · 1 | linecavern (s422) | victim: rostfen questedwaves (3878, HUMAN); slayer: atafo brownred the brilliances of braving (3679, CYCLOPS); cause: struck | beast attack col 9 vs the council of tresses (1050) y1 | — | y1 'change hf state' (state settled) ev 1941; y1 'change hf job' ev 3696 |
| `204126` · 84 | deeresteem (s1746) | victim: quithe lineoranges (13934, ELF); slayer: goldenflickered the diamond (57, DRAGON); cause: struck | beast attack col 17135 vs the lauded tails (3526) y84 | — | y84 'hf attacked site' ev 204125; y84 'hf died' (cause struck) ev 204127 |
| `358609` · 122 | tradedblocked (s1121) | victim: sazir sandalcanyons (27285, DWARF); cause: struck | battle col 34117 'the savage onslaught' y122 | — | y122 'change hf job' ev 357454 |
| `534619` · 167 | relievedtin (s416) | victim: tolis creekpuzzled (20330, HUMAN); cause: struck | battle col 56174 'the assault of sabres' y167 | — | y167 'change hf state' (state settled) ev 534598; y167 'add hf entity link' ev 534600 |
| `741336` · 225 | goatsilks (s461) | victim: pis plankmeadow (48055, GOBLIN); cause: struck | battle col 85043 'the assaulted attack' y225 | — | y225 'hf revived' ev 741290 |
| `970879` · 302 | craftrhyme (s1457) | victim: uja stabtreasures (70047, HFEXP63454 E_HUM1); slayer: damso blamelessbows (70519, HUMAN); cause: struck | battle col 125340 'the outrageous assaults' y302 | — | y302 'changed creature type' (new_race HFEXP63454 E_HUM1) ev 970757; y302 'hf wounded' ev 970878 |
| `1220062` · 396 | watertowers (s526) | victim: tuma glazedpride (84062, HFEXP45103 E_HUM5); cause: struck | battle col 167498 'the onslaught of racks' y396 | — | y396 'change hf state' (state settled) ev 1219304; y396 'hf died' (cause struck) ev 1219330 |
| `1446094` · 499 | goldenrouts (s1739) | victim: kubuk lanceddrummed (74314, HUMAN); slayer: ukap strokedblocks (39063, HUMAN); cause: struck | battle col 196952 'the scraped assault' y499 | — | y499 'hf died' (cause struck) ev 1446087; y499 'attacked site' ev 1446093 |

### murder — DF 'hf died' · 5,786 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `6746` · 3 | doomedguard (s620) | victim: nguslu seduceclasp (1881, GOBLIN); slayer: estrur jackalspine (1882, GOBLIN); cause: murdered | orphan (roles only) | — | y5 'hf simple battle event' ev 9141; y5 'hf died' (cause struck) ev 9142 |
| `369752` · 125 | blushedshoot (s446) | victim: zon anguishlabored (8493, DWARF); slayer: kib womenchamber (32245, DWARF); cause: murdered | orphan (roles only) | — | y125 'change hf state' (mood fell) ev 369751; y129 'add hf entity link' ev 387539 |
| `552158` · 172 | riddlestole (s432) | victim: quogub glitterrumor (43935, HUMAN); slayer: mato monstrousstalked (16481, GOBLIN); cause: murdered | orphan (roles only) | — | y172 'add hf entity link' ev 553296; y175 'entity persecuted' ev 563277 |
| `731997` · 223 | scaledfiend (s421) | victim: ngokang profaneworks (53339, GOBLIN); slayer: stozu malignedsewer (54504, GOBLIN); cause: murdered | orphan (roles only) | — | y225 'hf died' (cause murdered) ev 738010; y254 'hf died' (cause murdered) ev 826899 |
| `898466` · 279 | dreadfulrasp (s426) | victim: bosa deviltreaties (68060, GOBLIN); slayer: iru motherworth the coastal wickedness (38328, ELF); cause: murdered | orphan (roles only) | — | y366 'hf died' (cause murdered) ev 1141581; y479 'hf died' (cause murdered) ev 1404304 |
| `1090416` · 345 | lionkindles (s1207) | victim: ngoso grossstole (75749, GOBLIN); slayer: snamoz menacedye (31213, GOBLIN); cause: murdered | orphan (roles only) | — | y366 'remove hf hf link' ev 1141184; y370 'add hf hf link' ev 1152680 |
| `1263796` · 415 | plaitcruelty (s1670) | victim: arstruk seducedclinch (87479, GOBLIN); slayer: dang demonmazes (87564, GOBLIN); cause: murdered | orphan (roles only) | — | y415 'add hf entity link' ev 1265300; y416 'hf preach' ev 1267898 |
| `1444831` · 499 | thiefslithered (s444) | victim: bosa crueldank (89933, GOBLIN); slayer: kutsmob ghoulspeeches (80515, GOBLIN); cause: murdered | orphan (roles only) | — | — |

### theft — DF 'item stolen' · 22,399 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `4288` · 1 | claspedstakes (s427) | thief: nikuz mouthtaker the bejeweled apex (3805, GIANT); item: red spinach leaf; item kind: plant_growth; method: theft | beast attack col 25 vs the razor of curls (1060) y1 | — | y1 'change hf state' (state settled) ev 2067; y1 'add hf entity link' ev 4286 |
| `59129` · 43 | stokedblack (s569) | thief: drakrayrbin (2504, KOBOLD); item: brimstone; item kind: bracelet; method: theft | theft col 5266 by strasuger (1169) y43 | — | y102 'hf died' (cause old age) ev 272426 |
| `183485` · 79 | openedmuted (s731) | thief: trakafaplugus (5241, KOBOLD); item: turkey bone; item kind: bracelet; method: theft | theft col 15244 by shidikishrayngis (1109) y79 | — | y145 'remove hf hf link' ev 449569; y156 'hf died' (cause old age) ev 491063 |
| `351748` · 121 | hawkscarred (s1661) | thief: prukimbis (1599, KOBOLD); item: citron wood; item kind: bracelet; method: theft | theft col 33390 by jribiglimis (1035) y121 | — | y123 'remove hf hf link' ev 360635; y128 'add hf hf link' ev 380610 |
| `632639` · 194 | habitdrooped (s1175) | thief: jligigorber (29884, KOBOLD); item: donkey bone; item kind: ring; method: theft | theft col 69396 by sididilolmis (1273) y194 | — | y223 'hf died' (cause old age) ev 730868; y290 'hf revived' ev 935842 |
| `922731` · 286 | angelslaughter (s2014) | thief: stettad parchedheated the sweltering furnace (32, DRAGON); item: electrum; item kind: scepter; method: theft | beast attack col 113839 vs the first council (4056) y286 | — | y286 'add hf entity link' ev 922729; y344 'add hf entity link' ev 1088961 |
| `1196162` · 386 | gladthrifty (s1436) | thief: ruyava growthpulled (69863, ELF); item: iron; item kind: armor; method: theft | orphan (roles only) | — | y417 'hf revived' ev 1269935 |
| `1446420` · 499 | freshcrews (s984) | thief: pak assaultbuckle (90873, HUMAN); item: chert; item kind: goblet; method: looted | site conquered col 196992 by the empire of organizing (1305) y499 | — | — |

### betrayal — DF 'hfs formed intrigue relationship' · 5,209 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `13572` · 10 | trussedmosses (s502) | corruptor: ikim fondledplait (3442, HUMAN); target: shadu quietmonks (3441, HUMAN); method: intimidate; action: bring into network; outcome: yes | orphan (roles only) | — | y32 'hfs formed intrigue relationship' (action corrupt in place) ev 39319; y33 'entity overthrown' ev 40762 |
| `354862` · 121 | laborsnacks (s402) | corruptor: usbu poisonmirrors (28375, GOBLIN); target: ido foldlancer (22803, HUMAN); method: flatter; action: corrupt in place; outcome: yes | orphan (roles only) | rep-link y131 | y122 'hf preach' ev 358676; y126 'hf preach' ev 375248 |
| `587194` · 181 | riddlestole (s432) | corruptor: pethit tautdabblers (28505, HUMAN); target: nubpo taxtemple (33449, HUMAN); method: bribe; action: bring into network; outcome: yes | orphan (roles only) | rep-link y185 | y189 'hf died' (cause struck) ev 615812; y190 'hfs formed intrigue relationship' (action bring into network) ev 619428 |
| `780832` · 239 | squashbody (s1201) | corruptor: notlith runseeds the saffron of fields (61769, OLM_MAN); target: oba squaresocket (58830, OLM_MAN) | orphan (roles only) | — | y239 'hfs formed intrigue relationship' ev 780831; y239 'entity incorporated' ev 782988 |
| `962650` · 299 | razorancient (s2244) | corruptor: pena braidbridged (70692, HUMAN); target: uthra rapidpages (64589, HUMAN); method: intimidate; action: bring into network; outcome: yes | orphan (roles only) | — | y299 'failed intrigue corruption' (action induce to embezzle) ev 962651; y300 'add hf hf link' ev 963279 |
| `1105589` · 351 | moistnessbrides (s486) | corruptor: suque grapefruits (56657, HUMAN); target: bok fordedscorching (79174, HUMAN); method: flatter; action: corrupt in place; outcome: yes | orphan (roles only) | rep-link y360 | y357 'add hf entity link' ev 1120769; y358 'remove hf hf link' ev 1121518 |
| `1274257` · 419 | murkyouths (s2298) | corruptor: oled dwellingloves (76585, HUMAN); target: githa humiddrinks (80989, HUMAN); method: flatter; action: bring into network; outcome: yes | orphan (roles only) | rep-link y420 | — |
| `1446143` · 499 | growthbent (s1009) | corruptor: kisnast wispsound (94479, REPTILE_MAN); target: nethu drilljacks (94794, HUMAN); method: flatter; action: corrupt in place; outcome: yes | orphan (roles only) | — | y499 'add hf entity link' ev 1444765; y499 'failed intrigue corruption' (action induce to embezzle) ev 1444872 |

### artifact creation — DF 'artifact created' · 26,846 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `5827` · 2 | cleanedshows (s522) | creator: uzu leafylover (1407, HUMAN); artifact: useful human (213) | orphan (roles only) | — | y22 'artifact stored' ev 24312 |
| `396547` · 131 | amuseyore (s2036) | creator: quazo anvilfang (14624, HUMAN); artifact: in pursuit of the monastery (4129) | orphan (roles only) | — | y131 'artifact stored' ev 396548 |
| `642171` · 196 | webtattoo (s2016) | creator: lor tooloak (24907, DWARF); artifact: a treatise on storage (7983) | orphan (roles only) | — | y198 'artifact stored' ev 649044 |
| `873979` · 271 | adorestyled (s466) | creator: iki danceglossed (66034, ELF); artifact: the hidden meaning of iki danceglossed (11829) | orphan (roles only) | — | — |
| `1077608` · 340 | hearthsister (s2793) | creator: uthral urgedust (59081, HUMAN); artifact: the great hearthsister (15688) | orphan (roles only) | — | y340 'artifact stored' ev 1077609 |
| `1234413` · 402 | rounddimples (s2552) | creator: eriya vipersiege (34605, ELF); artifact: hates fed (19546) | orphan (roles only) | — | y402 'artifact stored' ev 1234414 |
| `1352339` · 454 | straphug (s3055) | creator: hathur syrupwire (74654, HUMAN); artifact: errors in kingdomcounsels (23399) | orphan (roles only) | — | y454 'artifact stored' ev 1352340 |
| `1446575` · 499 | judgebeer (s2895) | creator: slenshi meadowbaldness (89694, HUMAN); artifact: do we understand the tower? (27249) | orphan (roles only) | — | y499 'artifact stored' ev 1446576 |

### site destruction — DF 'destroyed site' · 250 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `84344` · 52 | badlulled (s1247) | attacker: the lucid nations (1185); defender: the copper seductions (1847) | site conquered col 7296 by the lucid nations (1185) y52 | — | y77 'failed intrigue corruption' (action bring into network) ev 179799; y273 'hf revived' ev 879728 |
| `386409` · 129 | obeyedblossomed (s1570) | attacker: the wooden plague (1057); defender: the heroic hill (1153) | site conquered col 37291 by the wooden plague (1057) y129 | — | y215 'change hf state' (state settled) ev 707656 |
| `604462` · 186 | brimsdashed (s2138) | attacker: the wooden plague (1057); defender: the craters of delight (4647) | site conquered col 65568 by the wooden plague (1057) y186 | — | y187 'change hf state' (state settled) ev 608532; y187 'change hf state' (state settled) ev 608533 |
| `779394` · 238 | ardentfell (s2550) | attacker: the nation of worlds (1247); defender: the matched heathers (7912) | site conquered col 90235 by the nation of worlds (1247) y238 | — | y272 'change hf state' (state settled) ev 876086; y272 'change hf state' (state settled) ev 876087 |
| `900115` · 279 | washedsides (s2275) | attacker: the murky confederation (1271); defender: the mechanical healers (4595) | site conquered col 108661 by the murky confederation (1271) y279 | — | y290 'change hf state' (state settled) ev 935343; y319 'change hf state' (state settled) ev 1019872 |
| `1052879` · 331 | rackdwelled (s2805) | attacker: the confederation of couples (1251); defender: the fealties of garnishing (9162) | site conquered col 142134 by the confederation of couples (1251) y331 | — | y333 'change hf state' (state settled) ev 1059216; y452 'hf revived' ev 1349125 |
| `1162236` · 373 | embracehands (s2634) | attacker: the confederations of voice (1019); defender: the sensual spicy trench-partners (8239) | site conquered col 159144 by the confederations of voice (1019) y373 | — | y374 'change hf state' (state settled) ev 1164185; y385 'written content composed' ev 1193045 |
| `1443287` · 498 | kukubuklaylbus (s2460) | attacker: the soaked empires (1163); defender: shladalasteelus (1427) | site conquered col 196599 by the soaked empires (1163) y498 | — | — |

### journey — DF 'hf travel' · 3,086 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `4337` · 1 | narrowanvils (s408) | traveler: lor playarrow (1436, DWARF); return: yes | journey col 41 y1 | — | y1 'add hf entity link' ev 1347; y1 'hf travel' ev 4335 |
| `109196` · 60 | pristineringed (s546) | traveler: tira woodenblankets (1373, ELF); return: yes | journey col 9130 y60 | — | y60 'hf travel' ev 109194; y60 'hf new pet' ev 109195 |
| `366872` · 124 | botherplanned (s1429) | traveler: est gripsieged (26954, HUMAN); return: yes | journey col 35138 y124 | — | y124 'change hf state' (state settled) ev 365155; y124 'add hf entity link' ev 366522 |
| `601624` · 185 | seamseasons (s476) | traveler: gustem balancewades (38294, HUMAN); return: yes | journey col 65225 y185 | — | y185 'hf simple battle event' ev 599877; y185 'hf simple battle event' ev 599878 |
| `819348` · 251 | malignvaults (s1221) | traveler: pili clodpearl (41016, ELF); return: yes | journey col 95988 y251 | — | y251 'hf travel' ev 819346; y251 'hf new pet' ev 819347 |
| `1021287` · 319 | chastetimes (s490) | traveler: laspar beachedships (65172, HUMAN); return: yes | journey col 136619 y319 | — | y319 'attacked site' ev 1020626; y319 'attacked site' ev 1020688 |
| `1246938` · 407 | voicedshell (s531) | traveler: cacame seaferns (18113, ELF); return: yes | journey col 171051 y407 | — | y407 'field battle' ev 1246108; y407 'hf travel' ev 1246936 |
| `1445420` · 499 | valefiends (s409) | traveler: amxu dreadfulstarve (93893, GOBLIN); return: yes | journey col 196833 y499 | — | y499 'hf travel' ev 1445418; y499 'hf new pet' ev 1445419 |

### captivity — DF 'hf abducted' · 4,991 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `4291` · 1 | coupleburied (s458) | victim: pevo catstricken (2324, NIGHT_CREATURE_17); snatcher: oreme fateddied the ashen (1292, NIGHT_CREATURE_17) | beast attack col 26 vs the imperial skirts (1142) y1 | — | y1 'change hf state' (state wandering) ev 1292; y1 'add hf entity link' ev 1657 |
| `172062` · 76 | boulderspines (s1162) | victim: minkot razorlovely (21446, DWARF); snatcher: usbu blowfiend (10714, GOBLIN) | abduction col 14163 by the wooden plague (1057) y76 | — | y76 'add hf entity link' ev 172063; y76 'change hf state' (state settled) ev 172064 |
| `326951` · 115 | boulderspines (s1162) | victim: rimtar wintercloistered (30219, DWARF); snatcher: xuspgas packhates (33876, GOBLIN) | abduction col 30481 by the wooden plague (1057) y115 | — | y115 'add hf entity link' ev 326952; y115 'change hf state' (state settled) ev 326953 |
| `463603` · 149 | tallpassions (s1875) | victim: xah nightbuckle (43312, HUMAN); snatcher: azstrog helldepress (31180, GOBLIN) | abduction col 47109 by the untoward sins (1015) y149 | — | y149 'add hf entity link' ev 463604; y149 'change hf state' (state settled) ev 463605 |
| `613480` · 189 | primgroove (s419) | victim: duli searingchanted (51324, HUMAN); snatcher: song mosthells (52002, GOBLIN) | abduction col 66839 by the frightful hate (1005) y189 | — | y189 'add hf entity link' ev 613481; y189 'change hf state' (state settled) ev 613482 |
| `820619` · 252 | oilpot (s480) | victim: tholtig lancercomets (61214, HUMAN); snatcher: nguslu craftedfiends (63912, GOBLIN) | abduction col 96202 by the dread of uttering (1111) y252 | rep-link y250 | y252 'add hf entity link' ev 820620; y252 'change hf state' (state settled) ev 820621 |
| `1114635` · 355 | praisechaoses (s484) | victim: edri shakenashes (79989, HUMAN); snatcher: stozu fiendsilences (77803, GOBLIN) | abduction col 151773 by the folded seduction (1045) y355 | — | y355 'add hf entity link' ev 1114638; y355 'change hf state' (state settled) ev 1114639 |
| `1444581` · 499 | rhythmpetals (s2010) | victim: gisu veilcrimson (96123, HUMAN); snatcher: amxu borednightmares (94101, GOBLIN) | abduction col 196729 by the evil of trumpets (1119) y499 | — | y499 'add hf entity link' ev 1444582; y499 'change hf state' (state settled) ev 1444583 |

### escape — DF 'hf ransomed' · 12 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `179207` · 77 | no place recorded | captive: lelgo waxparched (15540, HUMAN); ransomer: gicast halepresent (9789, HUMAN); payer: talde fatalbolted (10090, HUMAN); moved to: beeradores [site 1553] | orphan (roles only) | rep-link y68 | y77 'hf abducted' ev 179206; y79 'hfs formed intrigue relationship' (action corrupt in place) ev 187018 |
| `561794` · 174 | no place recorded | captive: lomoth strawspooned (39779, HUMAN); ransomer: isi lordreigned (37614, HUMAN); payer entity: the mythical coalition (6551); moved to: anvilhoney [site 477] | orphan (roles only) | rep-link y172 | y174 'entity created' ev 561714; y174 'add hf entity link' ev 561716 |
| `627325` · 192 | no place recorded | captive: esme gameplanned (51425, HUMAN); ransomer: thora telltiles (26593, HUMAN); payer entity: the bold coalition (6990); moved to: roperansacked [site 1689] | orphan (roles only) | — | y192 'hf abducted' ev 626836; y192 'entity created' ev 627057 |
| `694408` · 211 | no place recorded | captive: rulak petsuns (40671, HUMAN); ransomer: iwo urgedrink (22230, HUMAN); payer: kajeth meadacts (50601, HUMAN); moved to: unitedrevered [site 2489] | orphan (roles only) | — | y211 'add hf hf link' ev 691623; y211 'hf abducted' ev 694407 |
| `852907` · 263 | no place recorded | captive: busla diereins (51242, HUMAN); ransomer: ona smileobeyed (54926, HUMAN); payer entity: the company of festivals (5770); moved to: botherplanned [site 1429] | orphan (roles only) | rep-link y264 | y263 'failed intrigue corruption' (action bring into network) ev 852904; y263 'hf abducted' ev 852906 |
| `1121246` · 357 | no place recorded | captive: nique practicedtell (71410, HUMAN); ransomer: song hateweather (76377, GOBLIN); payer: nelti ectochews (59672, HUMAN); moved to: toldsearch [site 2621] | orphan (roles only) | rep-link y352 | y357 'hf abducted' ev 1121244; y357 'hf wounded' ev 1121245 |
| `1154079` · 370 | no place recorded | captive: nique practicedtell (71410, HUMAN); ransomer: aquov swallowbranded (77695, HUMAN); payer: nelti ectochews (59672, HUMAN); moved to: toldsearch [site 2621] | orphan (roles only) | — | y370 'entity persecuted' ev 1153269; y370 'hf abducted' ev 1154078 |
| `1437215` · 495 | no place recorded | captive: lum trickfight (92339, HUMAN); ransomer: xaki bounddove (91151, REPTILE_MAN); payer: dirlu bottleamused (92338, HUMAN); moved to: hatematches [site 450] | orphan (roles only) | — | y495 'change hf job' ev 1437424; y495 'add hf entity link' ev 1437425 |

### founding — DF 'created site' · 562 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `1749` · 1 | blanketitches (s506) | builder: soshosh lowstenches the poisoned (1359, DEMON_19) | orphan (roles only) | — | — |
| `203237` · 84 | garnishedmetal (s2047) | builder: ulum paddednarrow (9975, HUMAN) | orphan (roles only) | — | y105 'change hf state' (state visiting) ev 287606; y105 'hf prayed inside structure' ev 287607 |
| `319804` · 113 | scoopedbristle (s2184) | builder: izem crushedperfect (11594, HUMAN) | orphan (roles only) | — | y128 'change hf state' (state visiting) ev 381386; y128 'change hf job' ev 381388 |
| `483830` · 154 | partnerchant (s2339) | builder: uja burytuft (29039, HUMAN) | orphan (roles only) | — | y155 'change hf state' (state visiting) ev 490835; y155 'hf prayed inside structure' ev 490836 |
| `617988` · 190 | enjoyedglistens (s2464) | builder: seto fernancient the connected gifts of winter (24558, HUMAN) | orphan (roles only) | — | y211 'change hf state' (state settled) ev 693476; y267 'attacked site' ev 864524 |
| `824166` · 253 | figureyearlings (s2592) | builder: ngilsho ownthimble (44975, HUMAN) | orphan (roles only) | — | y269 'change hf state' (state settled) ev 868848; y352 'change hf state' (state settled) ev 1107454 |
| `1060090` · 334 | twinehides (s2818) | builder: adre planknighted (68064, HUMAN) | orphan (roles only) | — | y390 'change hf state' (state settled) ev 1206166; y403 'change hf state' (state settled) ev 1235960 |
| `1440569` · 497 | swallowedgulfs (s3104) | builder: sas latheredtile (92531, HUMAN) | orphan (roles only) | — | — |

### item loss — DF 'artifact lost' · 2,774 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `25671` · 23 | taxhowl (s784) | artifact: targets and the diminished elevation (223) | battle col 2339 'the dangerous assault' y23 | — | — |
| `351577` · 121 | sableguilds (s1285) | artifact: anatomy for students (2206) | orphan (roles only) | — | — |
| `484660` · 154 | stockaderinged (s1274) | artifact: darkate (502) | battle col 49657 'the attack of spikes' y154 | — | y154 'artifact claim formed' ev 484690; y212 'artifact lost' ev 694663 |
| `642604` · 196 | cobaltclearings (s938) | artifact: elements of waxing and waning (7475) | battle col 70920 'the outrageous assault' y196 | — | — |
| `775630` · 237 | curledvalleys (s425) | artifact: principles of the moon's path (9626) | battle col 89748 'the assault of wars' y237 | — | — |
| `971712` · 303 | conflictflax (s579) | artifact: the forest retreat: the truth (11964) | orphan (roles only) | — | — |
| `1190550` · 384 | taxhill (s411) | artifact: mysteries of surveying (7719) | battle col 163464 'the furious attack of cyclones' y384 | — | — |
| `1445930` · 499 | toppearls (s1130) | artifact: deathsnot (351) | battle col 196932 'the onslaught of ferocity' y499 | — | y499 'artifact claim formed' ev 1445853 |

### madness — DF 'change hf state' · 179 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `12451` · 9 | dikesquash (s541) | figure: tobul lettersmoothness (4718, DWARF); mood: macabre | orphan (roles only) | — | y10 'add hf entity link' ev 12853; y10 'change hf state' (state settled) ev 12854 |
| `42121` · 34 | emeralddye (s431) | figure: iden sinktower (7322, DWARF); mood: possessed | orphan (roles only) | — | y34 'change hf job' ev 42119; y34 'add hf entity link' ev 42120 |
| `55118` · 41 | hazesilver (s424) | figure: tun pageprincess (1728, DWARF); mood: fey | orphan (roles only) | — | y41 'change hf job' ev 55117; y44 'add hf entity link' ev 62930 |
| `105446` · 59 | galleybrands (s401) | figure: kadol showeredbridged (13295, DWARF); mood: secretive | orphan (roles only) | — | y70 'add hf entity link' ev 147868; y70 'change hf state' (state settled) ev 147869 |
| `177941` · 77 | baldcopper (s1827) | figure: zon vesselflashed (5430, DWARF); mood: possessed | orphan (roles only) | — | y79 'remove hf hf link' ev 184130; y80 'add hf hf link' ev 187567 |
| `369751` · 125 | blushedshoot (s446) | figure: kib womenchamber (32245, DWARF); mood: fell | orphan (roles only) | — | y125 'hf died' (cause murdered) ev 369752; y129 'add hf entity link' ev 387539 |
| `592406` · 183 | portalorange (s406) | figure: monom gorgefenced (42488, DWARF); mood: macabre | orphan (roles only) | — | y187 'knowledge discovered' ev 608106; y189 'knowledge discovered' ev 614730 |
| `1423967` · 489 | boulderspines (s1162) | figure: song flyleaps (96027, DWARF); mood: fey | orphan (roles only) | — | y489 'change hf job' ev 1423965; y489 'add hf entity link' ev 1423966 |

### transformation — DF 'changed creature type' · 1,356 candidates

| ev · year | place | participants | cause (reconstructed) | witness | consequence |
|---|---|---|---|---|---|
| `4497` · 1 | no place recorded | changee: pevo catstricken (2324, NIGHT_CREATURE_17); changer: oreme fateddied the ashen (1292, NIGHT_CREATURE_17); from: ELF; to: NIGHT_CREATURE_17 | orphan (roles only) | — | y1 'change hf state' (state wandering) ev 1292; y1 'add hf entity link' ev 1657 |
| `484829` · 154 | no place recorded | changee: tosid lustrouslances (43250, HFEXP29548 E_HUM1); changer: bikda nightcobalt (29548, HUMAN); from: DWARF; to: HFEXP29548 E_HUM1 | site conquered col 49674 by the craters of delight (4647) y154 | — | y154 'hf performed horrible experiments' ev 484762; y154 'changed creature type' (new_race HFEXP29548 E_HUM1) ev 484763 |
| `702414` · 214 | no place recorded | changee: ote peaksquid (43492, HFEXP11521 E_HUM1); changer: nique nurtureddye (11521, HUMAN); from: HUMAN; to: HFEXP11521 E_HUM1 | site conquered col 79494 by the veiled bowls (2744) y214 | — | y214 'hf performed horrible experiments' ev 702412; y214 'changed creature type' (new_race HFEXP11521 E_HUM1) ev 702413 |
| `741072` · 225 | no place recorded | changee: cango fireshark the umbral calluses (49868, HFEXP11521 E_HUMG6); changer: nique nurtureddye (11521, HUMAN); from: HUMAN; to: HFEXP11521 E_HUMG6 | site conquered col 85005 by the veiled bowls (2744) y225 | — | y225 'remove hf hf link' ev 737085; y225 'hf performed horrible experiments' ev 740772 |
| `977041` · 304 | no place recorded | changee: ero fathercraft (69312, HFEXP69575 E_HUM2); changer: nasnok applesdrums (69575, HUMAN); from: HUMAN; to: HFEXP69575 E_HUM2 | site conquered col 126707 by the ambiguity of closets (5825) y304 | — | y304 'hf performed horrible experiments' ev 977038; y304 'changed creature type' (new_race HFEXP69575 E_FS1) ev 977039 |
| `1208471` · 391 | no place recorded | changee: kogan hailedroofs (83090, NIGHT_CREATURE_9); changer: rufithi dustash the shady umbra (64375, NIGHT_CREATURE_9); from: DWARF; to: NIGHT_CREATURE_9 | orphan (roles only) | — | y400 'add hf entity link' ev 1229697; y400 'add hf entity link' ev 1229698 |
| `1301210` · 430 | no place recorded | changee: ettad ruledinsight (87546, HFEXP76787 E_HUM1); changer: telsta beestick (76787, HUMAN); from: HUMAN; to: HFEXP76787 E_HUM1 | site conquered col 178264 by the tressed carnages (10346) y430 | — | y430 'hf performed horrible experiments' ev 1301115; y430 'changed creature type' (new_race HFEXP76787 E_HUM1) ev 1301116 |
| `1446060` · 499 | no place recorded | changee: ume bravecandles (96865, HFEXP89712 E_HUM1); changer: shosa wiseriddled (89712, HUMAN); from: HUMAN; to: HFEXP89712 E_HUM1 | site conquered col 196945 by the heavy confederation (1209) y499 | — | y499 'add hf entity link' ev 1445826; y499 'change hf state' (state settled) ev 1445827 |

### war — collection 'war' · 990 candidates

| war · span | name | scale |
|---|---|---|
| `20` · 1-2 | the scorching conflict' · aggressor the disloyal tick [entity 1001] vs defender the earthen queen [entity 1083] | 11 nested battles · 2 direct member events · casualty sum >= 66 |
| `10794` · 65-136 | the dented conflict' · aggressor the stormy racks [entity 3101] vs defender the empire of nurturing [entity 1081] | 2 nested battles · 0 direct member events · casualty sum >= 7 |
| `37122` · 128-129 | the brutal conflict' · aggressor the lucid vice [entity 1089] vs defender the knowing hooves [entity 1105] | 25 nested battles · 1 direct member events · casualty sum >= 657 |
| `74487` · 203 | the war of hatchets' · aggressor the bulbous sieges [entity 5516] vs defender the willful trusses [entity 6975] | 2 nested battles · 0 direct member events · casualty sum >= 0 |
| `111709` · 283 | the roasted war' · aggressor the wads of heat [entity 3889] vs defender the confederations of voice [entity 1019] | 14 nested battles · 0 direct member events · casualty sum >= 933 |
| `158001` · 370 | the furious conflict' · aggressor the gulf of bucks [entity 1091] vs defender the oily nations [entity 1297] | 1 nested battles · 1 direct member events · casualty sum >= 131 |
| `178256` · 430-ongoing | the ignited war' · aggressor the tressed carnages [entity 10346] vs defender the competitive confederation [entity 1283] | 2 nested battles · 0 direct member events · casualty sum >= 0 |
| `196947` · 499-ongoing | the conflict of hatchets' · aggressor the vipers of planning [entity 10256] vs defender the green hares [entity 9906] | 6 nested battles · 0 direct member events · casualty sum >= 14 |

### catastrophe — collection 'beast attack' · 13,289 candidates

| col · span | place | beast | members | beast's fate |
|---|---|---|---|---|
| `3` · 1 | clashedshot (s561) | eve flamesilver the sweltering gold of pearls (28, DRAGON) | 2 'add hf entity link', 2 'creature devoured' | y55 'hf died' (cause struck) ev 93257 |
| `17170` · 84 | doomwhispered (s1260) | scribepalms the momentous (25066, CRETACEOUS_TYRANNOSAURUS_MAN) | 10 'creature devoured', 6 'hf died', 12 'hf simple battle event', 1 'hf wounded' | y84 'hf died' (cause struck) ev 204361 |
| `52132` · 159 | cactusbeach (s1624) | ? | 2 'add hf entity link', 1 'item stolen' | — |
| `86370` · 229 | datefarms (s1341) | rodem heavenglades the willful (124, BIRD_ROC) | 9 'creature devoured', 3 'hf died', 5 'hf simple battle event', 3 'item stolen' | y229 'hf died' (cause struck) ev 751428 |
| `121563` · 297 | distancevised (s838) | ? | 1 'add hf entity link', 2 'hf died', 2 'hf simple battle event' | — |
| `154970` · 363 | lulltouches (s1848) | ? | 3 'add hf entity link', 2 'hf simple battle event' | — |
| `178633` · 432 | handlecuddle (s467) | ? | 2 'hf simple battle event', 2 'hf wounded' | — |
| `196880` · 499 | huggedflutes (s891) | ? | 1 'add hf entity link', 10 'hf simple battle event' | — |

## 4. Findings (measured on the 120-entry corpus)

1. **The witness column is empty by design — DF has no epistemology
   events.** 9 of the 88 figure-bearing entries show a nearby reputation
   link; the other 79 record "none". DF never stores who saw what: our
   knowledge records (channel `saw/heard/told`, fidelity, `known_by`) have
   no donor in the export. The epistemology layer is our design burden —
   `docs/ref/df_legends_xml.md` maps `hf_reputation_change` ↔ knowledge
   records as the nearest analog, and that is all there is.
2. **The sink's participant index misses `hfid1`/`hfid2`.** Reputation
   events key their two figures as `hfid1`/`hfid2` — tags that do not end in
   `hfid` — so `event_participant` lifts zero rows for all 25,079 of them.
   This survey queries the EAV directly for the witness column; bg-3's
   "figure Y's own records" prefix scan inherits the same blind spot
   (reputation context is invisible to it). The fix — extending the bg-1
   lift rule — is a measured-law change, deliberately out of bg-2 scope.
3. **Theft and beast detail are plus-companion-only.** 22,399/22,399
   `item stolen` events resolve a thief via the companion (`histfig`) — 100%
   coverage; the main file carries only a circumstance pointer. Beast
   attacks are the same story (`eater`/`victim`/`race`). The sink v2 plus
   pass (bg-2, D-063) exists exactly because of this — D-051's recorded
   deferral fired.
4. **Causality reconstruction is mostly role-fields-only.** All 8 murder
   entries read "orphan (roles only)" — no collection; the orphan mass is
   the known 20–23% orphan share plus the ~70–80% ungrouped events
   (`TECH_NOTES.md` §3.1 F8). Where grouping exists it is a strict
   single-parent tree — liftable into our linear `cause` chain; the §11
   multi-parent deferral (arcs, P3c) is unaffected by anything measured
   here.
5. **Murders always carry slayer AND site** (5,786/5,786); the ambiguous
   deaths are the other causes — old age/struck carry no slayer on 52.8% of
   deaths. The archaeology work concentrates where the cause enum is quiet.
6. **Consequence columns read as terminal-or-sparse.** Item-loss follow-ups:
   6/8 "—" (lost artifacts mostly never re-appear in the log); murder
   consequences jump decades (y279 → y366 → y479). Our `hooks`
   (deferred-consequence tags, EVENT_SCHEMA §5) are the design answer to
   exactly this gap: DF records an outcome only when the world happens to
   touch the subject again — we declare the consequence at event time.
7. **Place is always a payload, never a position.** DF events carry
   `site_id`/`subregion_id`/`feature_layer_id` as data; our place is the
   projection (st-1 presence reads) plus `outcome` payload. No schema field
   is needed (§2 has none) — the brief resolves "where" from the fold,
   exactly as phase 1 already does.
8. **The two-slot actor/target law holds across all 15 event types.**
   Multi-role events (field battle: 2 civs + 2 generals; `created site`:
   civ + builder + resident civ) fit actor + target + `outcome` payload —
   the §11 law (type-specific DF-shaped fields live inside the validated
   outcome object) confirmed by construction.

## 5. What bg-3 inherits

- The query home stays the sink: participant prefix scans (4 ms measured,
  D-051) + `event_plus_fields` for theft/beast detail + the `hfid1`/`hfid2`
  caveat (finding 2) for reputation context.
- The 120 entries are ready-made brief-validation cases: known participants,
  known place, known follow-ups — the invented-facts count can score a
  briefer against these rows directly.
- The F7 distribution warning stands (`TECH_NOTES.md` §3): DF canon is
  macro-dense and micro-empty — the spike validates briefer mechanics, not
  micro-event interestingness; measure that on our own dry chronicle.
