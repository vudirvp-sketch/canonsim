# Anchor Region — Sarrow Vale and the Human-Scale Integration Test

**Status:** active working surface; current engine-backed embodiment exists in
`content/province_pack`.

This document is intentionally narrower than the world kernel. It asks whether
the larger world theory can produce one region whose geography, economy,
institutions, culture, history, actors and knowledge actually interact.

## 1. World-level target

The source worldbuilding program calls for an anchor region at the intersection
of trade, inherited infrastructure, ordinary work and historical residue.

The intended shape is:

`PLACE → RESOURCE → TRADE → INSTITUTIONS → ACTORS → BEHAVIOR → EVENT → KNOWLEDGE → SOCIAL RESPONSE → RESIDUE`.

The region does not need to contain every civilization regime. It needs to make
the larger world legible at human scale.

## 2. Current embodiment: Sarrow Vale

The current repository's `province_pack` is the best concrete implementation
witness for this role.

Current repo evidence includes:

- a generated 324-site surface;
- the Sarrow river artery;
- six authored settlement/landmark locations spanning the weir stair, road,
  keep, Malby, the smelt crofts and Thornmill;
- derived travel pricing over the generated geometry;
- lowland and hill cultural profiles, custom vocabulary and prohibitions;
- the guild / old families / half-pay garrison faction triangle;
- a 150-year generated history surface with feud/quarrel/exodus collections;
- market, fair and seasonal calendar entries;
- seasonal weather with a storm-linked market murmur;
- condensation of road traffic into named travelers;
- NPC spine records and the current brief/read-side surface.

This is an **implementation witness**, not proof that every broader worldbuilding
claim has already been solved.

## 3. Region pillars

The region currently exposes a compact set of interacting pressures:

### River artery

Movement, trade, crossing, hearing, weather and route access are concentrated on
one geographic spine.

### Iron / bloom trade

The worldbuilding source uses hill-smelted iron as a focal scarcity tying the
crofts, market, guild and surrounding institutions together.

**Status:** WORKING worldbuilding pillar. The current province pack carries the
iron vocabulary and actors, but its full resource/economy cycle is not yet the
same as an economy-armed pack.

### Feud residue

The burned mill, the old families, wergeld memory and present grievance turn
history into an active social force.

### Institution triangle

The river guild, old families and half-pay garrison respond differently to the
same pressure. Their objectives and thresholds can create different world-side
responses to an ordinary event.

### Lowland / hill estrangement

Two cultural regimes share one artery but use different naming profiles,
vocabulary and prohibitions.

### Seasonal trade

Market days, fairs and the river's seasonal cycle make time part of ordinary
economic and social experience.

## 4. Current causal map

| Layer | Sarrow Vale surface | Open question / first answers |
|---|---|---|
| Geography | river, travel lattice, weir, keep, market, crofts, manor | open: how much of the wider region is economically connected? |
| Resource | bloom/iron vocabulary, charcoal, river trade | open: how does scarcity become a measured price/flow cycle? (the pack is not economy-armed) |
| Trade | road traffic, market, toll, waybill, guild | answered (§6.1): the crossing household carries the flood season's cost; the croft camp carries the shaved weights — the two named cost-carriers of a disrupted route |
| Institutions | guild, garrison, old families, watch rotation | answered for the crossing (§6.1): the ferry family under the guild-held flood debt — the first named meso mediator; the camp's meso half (the charcoal debt) named, not yet authored |
| Actors | Ketta, Maren, Osgar, Ferra, Garrick, Wilmot, travelers | answered (§6.1): both estranged halves pay the guild's paper — the crossing's flood debt, the camp's charcoal debt — each side believing the other the favored one |
| Culture | lowland/hill names, vocabulary, shelter law, wergeld memory | answered at the crossing (§6.1): the law held as the family's name, the debt as the table's silence, the pole-or-road question as the heir's inheritance; the camp's family life open |
| History | feud / burned mill / generated historical events | two events, two institutions named: the feud's fire → the vigil (Loop B); the flood year → the crossing's debt (§6.1); the rest of the 150-year chronicle open |
| Knowledge | witnessed events, rumors, watch suspicion, road knowledge | answered in the meaning slice (§7.1): the four-position asymmetry map over one toll |
| Weather/calendar | markets, fairs, seasons, storm chain | answered (§6.1): the high_water rise → the punt men's double toll — the custom as persistent social adaptation; the household's four-phase year |
| Read-side meaning | cards, chronicle, lore, named travelers, scene markers | answered (§6.1): the flood-debt lever set — whoever learns the flood story holds a different lever at the stair; the wergeld duty already live on the road |

## 5. The causal mesh (W3 — audited iter-156)

Five loops, each a circuit that returns to its own driver changed. The audit's
two laws: the **disable test** — remove one loop's unique driver, and the other
four must still run — and the **shared-stage rule** — two circuits sharing
driver AND mediator are one mechanism counted once; sharing the response stage
alone is an interlock, never a collapse.

### Loop A — fire → institutional response (COMMITTED)

`fire_started over a location's fire_spots → alarm_raised (fear +40 direct,
panic_ripple +10 through the walls) → the triangle's fear arms — the guild
councils at 30, the garrison patrols at 40 (the FNV cascade: trade first,
crown second) → the changed world state (barred stalls, the watch on the
road) → the fear's own decay re-arms the bars`.

Closing edge: state-closing — the response changes the world the next fire
meets. Substrate: `transitions.fire`, the alarm's reactions, the guild and
garrison faction arms. Demonstrated: the market fire tips the guild, the keep
fire the garrison (`tests/test_triangle.py`). The anti-double-count ruling:
the theft → suspicion → document-check → arrest circuit is the SAME mechanism
family — an ordinary verb's axis ripple crossing the institutional door — one
mechanism, two armed verb families (fire/fear, theft/suspicion); counted once,
here, never a sixth loop.

### Loop B — feud residue → present politics (COMMITTED)

`the 150-year chronicle's feud collection (seeded once at worldgen) → the
houses' composition + the wergeld prohibition + the elders' seeded grievance
(35/30, under the vigil's 40-bar) → grief_wakes on a heard alarm (+20, the
numeric-home law: only the seeded holders wake) → both houses over the bar →
the wergeld vigil → the vigil itself a present political fact, rendered in
the tale`.

Closing edge: state-closing — the response is itself new residue. Substrate:
the chronicle collections, the old-families faction arm, the wergeld law, the
grief reaction. Demonstrated: each fire wakes exactly one elder — Thornmill
hears the market, the crofts hear the keep — and the vigil needs both
(`tests/test_triangle.py`). The honest interlock: the alarm is the only
committed grievance writer, so B's waking edge is fire-fed — A and B
interlock at the alarm; neither loop alone produces the vigil.

### Loop C — season → weather → social signal (COMMITTED)

`the seasons' cycle arithmetic (never a draw — the snowmelt comes when it
comes) → the weather ride's per-phase bias (the rise storm-heavy from any
state, the calm rebuilding slow) → storm → the murmur hook → Maren's ramble
— the market watching the rain eat the stalls`.

Closing edge: clock-closing — the year's return re-runs the bias; no state
feeds back. The honest grade: a pulse, the mesh's clock, not a feedback
circuit — and still cross-system (calendar → weather → director hook → market
NPC). Substrate: the calendar's seasons, the seasonal weather ride, the storm
hook. Demonstrated: the weather rides the seasons with the phase bias
(`tests/test_calendar.py`). The C→A edge: the rain washes the smoke away
(`smoke_washed_away`) — the sky erases the fire's sign.

### Loop D — route → condensation → culture (COMMITTED)

`the travel lattice + the artery's claims → the road traffic as ONE group
entity (road_counts, the cardinality aggregate while cold) → the reader's
warm zone → road_musters (the members' canon births, names drawn from the
cultures' profiles) → two lowland tongues and one hill tongue visible in the
tale`.

Closing edge: reader-closing — the condensation materializes who the road IS;
legibility, not state feedback. Substrate: the travel rules, the group's
macro/condense pair, the name profiles. Demonstrated: the traffic condenses
at the first beat, the born names render, the two tongues split their
postures (`tests/test_t1_province.py`). The B⇄D edge: the condensation
materializes the hill carrier — the wergeld word's walker is himself a born
stranger; the feud's memory rides the road's traffic.

### Loop E — the credit loop (AUTHORED — §6.1's unit)

`the flood year (one historical catastrophe, not the recurring phase) → the
guild-held flood debt → the high_water double toll under the shelter law →
the road's word ("the crossing answers the heaviest purse") → the debt
cleared by a strong honest season, or the bend hardened into custom`.

Closing edge: state-closing at the authored band — the residue (reputation,
debt standing) changes the next season's options. Band honesty: the beats are
committed (the spine, the coerce double-toll, the shelter law, the
storm-armed rise), the mediation is authored (the debt's paper), and the flow
is not economy-armed. The C⇄E edge: the rise prices the toll — the season
modulates the debt's collection.

### The verdict

| Loop | Driver | Mediator | Response | Residue | Closure | Band |
|---|---|---|---|---|---|---|
| A | live fire event | fear axis + thresholds | council / patrol | changed world | state | committed |
| B | generated feud history | grievance + prohibition | the vigil | new memory | state | committed |
| C | the calendar clock | weather bias + hook | the murmur | market texture | clock | committed |
| D | the travel graph | condensation + names | born strangers | visible culture | reader | committed |
| E | the flood year | the debt's paper | the double toll | reputation + standing | state | authored |

Five loops pass the disable test — no two share a driver, and the one shared
stage (the triangle's threshold dynamics feeding the intent door) carries two
different axes (fear, grievance) without making the loops one mechanism. Four
named interlock edges: the alarm wakes both fear and grief (A⇄B), the rain
erases the smoke (C→A), the condensation materializes the feud's carrier
(B⇄D), the rise prices the toll (C⇄E). Independent loops, interlocked edges —
not one engine wearing five masks.

## 6. Meso frontier

The largest current gap is not another town. It is the layer between factions and
individuals:

- household;
- workshop;
- small merchant house;
- ferryman family;
- smithing crew;
- inn/boarding economy;
- apprentice relationship;
- local legal/customary office.

The next question is:

> **When the river trade or iron scarcity changes, what does one ordinary household do?**

The answer should affect money, labor, relationships, status, knowledge or
obligation and should be capable of producing at least one durable consequence.

The first unit is authored: the crossing household (§6.1).

### 6.1 The crossing household (WORKING — the first authored meso unit)

The weir stair's ferry family, authored over the committed substrate (the spine,
the shelter law, the high_water custom, the boathouse) — no new entity classes, no
new institutions beyond the guild's existing paper.

**Composition.** The toll-taker (the committed spine's holder), one grown second
hand — the pole is two-handed work: one on the water, one on the rope — and the
drowned generation's memory. Assets: the boathouse (the bank's one burnable
thing), the punt pole (the family's last tool), the crossing's custom itself.
Losses: the punt and the savings, drowned the flood year.

**The chain (the doctrine's ladder, walked once):**

| Rung | The crossing household |
|---|---|
| CAUSE | the flood year — the rise drowned the family punt and the savings with it |
| POSSIBILITY | the crossing is the artery's gate: the river runs quicker than the road, the fords drown in high_water and the stair does not |
| PRESSURE | the flood debt — guild-held since the winter after: the borrowed punt, the stores eaten keeping the shelter law through the stranded season |
| ACTORS | the toll-taker, the second hand, the guild's factor (the paper), the road's strangers |
| INSTITUTION | the crossing's custom: the high_water double toll (the season's risk priced) under the shelter law — a paying stranger is never turned from the crossing's shelter, the trade's own law, older than the guild's ledgers |
| KNOWLEDGE | the toll-taker knows the debt's size and the season; the road knows only the rate; the guild knows the paper — each map bounded and legitimate (the four-position table: §7.1) |
| CONSEQUENCE | the purse-read bend past custom on the rich-seeming stranger — the flaw, live as the committed double-toll beat; the law's edge holds it: coin may bend, shelter never |
| RESIDUE | the road's word ("the crossing answers the heaviest purse" — the flaw's reputation is itself residue); the debt standing; the pole inherited |
| NEW OPTION | the debt is clearable (a strong honest season) or the bend hardens into custom (the next crossing answers purses by default); on the read side, whoever learns the flood story holds a different lever at the stair |

**The household's year** (the seasonal cycle as lived, not as weather): thaw —
the weir runs loud, the road soft, the toll thin; high_water — the fords drown,
the custom doubles, the poler's risk is real (the family paid it once in punt and
savings); long_light — the road dry and fast, the fat season, the payment season;
first_frost — the trade slows, the stores counted against the debt.

**The guild's hold.** The debt ties the household into the institution triangle's
trade arm without inventing a new institution: the guild lent against the toll,
the guild's weighing day prices the trade the toll feeds, the guild's council
watches the trade's fear. The collision already staged in the committed
substrate: the first stranger through the rise with a waybill book is a
debt-auditor by his own errand — a debtor's toll squeeze meeting a creditor's
reader, no new mechanics required (the small-alphabet law, authoring doctrine
§10).

**Embodiment (committed vs authored).** Committed: the spine (want/need/flaw/
cause), the coerce urgency entry (the purse-read double-toll beat), the shelter
law (the lowland prohibition set), the high_water lines (the drowned fords, the
punt men's double), the boathouse fire spot, the auditor's errand — and, since
iter-157, the second hand himself (Dellan: the kin/runner pair axes, the
road-leg urgency beat, the paired escort legs) and the punt pole (the item
committed; KI#87 closed iter-157). Authored here (WORKING): the debt's
guild-holder, the credit winter, the household's year, and the debt's flow
(not economy-armed — the open engineering-side question).

## 7. Meaning frontier

The current region is already strong at mechanical composition. The next depth
question is whether those mechanics change the meaning of ordinary life.

Useful concrete probes:

- What does a ferryman call a "fair" toll after a flood?
- Which family obligation exists because of the old mill fire?
- What does a hill household consider an insulting price?
- What is a lowland trader ashamed to admit about the guild's shelter law?
- Which memory is inherited as a duty rather than a story?

These are authoring probes, not current canon answers.

### 7.1 The first meaning slice (run 2026-09-20, iter-155): the high-water double toll

The event: a rich-seeming stranger crosses at the stair in the rise; the toll is
doubled — the committed purse-read beat riding the season's custom. The same
mechanical event, four maps (WORKING — authored over the committed substrate):

| Position | The same toll means | The bounded map |
|---|---|---|
| the toll-taker | the debt's next payment; the custom's justice — the risk priced, the poler's risk real, the family paid it once | knows the debt's size and the season; does not know the stranger audits debts for a living |
| the hill carrier | the artery's skim on his labor: priced on who crosses, not what crosses — the insult is the reading, not the sum | knows the custom and the camp's charcoal debt; does not know the crossing's paper |
| the stranger (the auditor) | the road's friction — a greedy ferryman | knows the convoy books; does not know the flood story — the books show the toll, not the debt |
| the guild | the debt's interest: the toll kept up while the paper stands | knows the paper; does not weigh what either bank of the river carries for it |

**The distribution finding:** the meaning lands on four positions — household
survival, labor skimmed, the road's misread, the institution's interest — not on
one dramatic faction vertex. PARTIALLY CONFIRMED at the authored band
(`WORLD_TESTS.md` §9).

**The probes after the slice** (WORKING answers, this section): the ferryman's
fair toll — two justices, the risk-priced against the load-priced; the insulting
price — the purse-read itself, not the sum; the lowland trader's shelter-law
shame — "we shelter by law and charge by ledger": the law is older than the
guild's paper, and the paper now prices what the law gives; the inherited duty —
twice, the pole at the crossing and the wergeld word on the road. Still open:
the Thornmill family obligation — the vigil is faction-level; which household
carries the mill fire's debt is unanswered.

## 8. Current limitations

### NOT YET PROVEN

- full household economics;
- durable workshop/market meso institutions;
- a complete iron scarcity cycle in the current province pack;
- all-year consumer use of every calendar surface;
- a complete world-to-region mapping for the Ancient Network;
- cross-region trade consequences beyond the anchor.

### IMPORTANT

The current repository's world-2 L2 verdict already treats Sarrow Vale as a
successful deep second-world slice at the measured band. This document is asking
a different question: whether it can serve as the **worldbuilding anchor** for the
broader setting.

## 9. Anchor exit criterion

The anchor is ready to serve as the base for broader expansion when one ordinary
local disruption can be followed through:

`place/resource → meso institution → actor choice → event → knowledge asymmetry → social response → historical/cultural residue → changed future option`.

The chain must be understandable without adding a new worldbuilding document for
each link.

**Status (2026-09-20):** the criterion's own test — one disruption (the flood
year, the high_water rise) followed through the whole chain without a new
document per link — is MET once at the authored band (§6.1's ladder; the social
response rides the road's word and the market's rumor channel, both committed
surfaces). The implementation witness carries the chain at the single-NPC +
companion band (iter-157: the second hand, the pole — KI#87 closed); the debt's
economy flow remains the engineering-side question the world track does not
open by itself — the pack is not economy-armed.
