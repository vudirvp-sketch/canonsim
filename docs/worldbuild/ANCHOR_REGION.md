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
iron vocabulary and actors, and — since iter-162 (debt-1) — one armed economy
slice (the flood debt's accounts + flows); the full resource cycle (bloom,
iron, charcoal as measured scarcity) is not yet armed.

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
| Resource | bloom/iron vocabulary, charcoal, river trade | open: how does scarcity become a measured price/flow cycle? (the debt's slice armed iter-162 — accounts + flows, no prices yet; the water's ALLOCATION answered at the authored band, §6.2 — the step law, order before price) |
| Trade | road traffic, market, toll, waybill, guild | answered (§6.1): the crossing household carries the flood season's cost; the croft camp carries the shaved weights — the two named cost-carriers of a disrupted route |
| Institutions | guild, garrison, old families, watch rotation | answered three times: the crossing under the guild's paper (§6.1, the first named meso mediator), the water under the practitioners' step (§6.2 — the step bench, the second meso unit) and the care under the winter kin's recognition (§6.3 — the constructed kinship edge, the third W4 addition: no office, no court, the road's word the holder); the camp's meso half (the charcoal debt) named, not yet authored |
| Actors | Ketta, Maren, Osgar, Ferra, Garrick, Wilmot, travelers | answered (§6.1): both estranged halves pay the guild's paper — the crossing's flood debt, the camp's charcoal debt — each side believing the other the favored one |
| Culture | lowland/hill names, vocabulary, shelter law, wergeld memory | answered at the crossing (§6.1): the law held as the family's name, the debt as the table's silence, the pole-or-road question as the heir's inheritance; the law's own other half authored (§6.3): the care held as the notch, the mourning widened past blood; the camp's family life open |
| History | feud / burned mill / generated historical events | three events, four institutions named: the feud's fire → the vigil (Loop B); the flood year → the crossing's debt and the winter kin (§6.1, §6.3 — one catastrophe, two circuits); the quarrel's pact → the step law (§6.2); the rest of the 150-year chronicle open |
| Knowledge | witnessed events, rumors, watch suspicion, road knowledge | answered in the meaning slice (§7.1): the four-position asymmetry map over one toll |
| Weather/calendar | markets, fairs, seasons, storm chain | answered (§6.1): the high_water rise → the punt men's double toll — the custom as persistent social adaptation; the household's four-phase year |
| Read-side meaning | cards, chronicle, lore, named travelers, scene markers | answered (§6.1): the flood-debt lever set — whoever learns the flood story holds a different lever at the stair; the wergeld duty already live on the road |

## 5. The causal mesh (W3 — audited iter-156; the W4 additions F — iter-164, G — iter-165)

Seven loops, each a circuit that returns to its own driver changed. The audit's
two laws: the **disable test** — remove one loop's unique driver, and the other
six must still run — and the **shared-stage rule** — two circuits sharing
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
storm-armed rise), the mediation is authored (the debt's paper), and the
flow's arithmetic is armed (iter-162, debt-1: the accounts + the fold's two
flows on the macro year — the paper's fall still authored, the flow
vocabulary carrying no terminus). The C⇄E edge: the rise prices the toll —
the season modulates the debt's collection.

### Loop F — the step bench: the band → the step → the allocation (AUTHORED — §6.2's unit, iter-164)

`the recurring band (the late long_light's low water at the stair — the
seasons' flow consequence, an accumulated head state, never the calendar's
pulse itself) → the step rule (the practitioners' reading: the head named by
the stair's wet step) → the allocation (one use served, two priced — the
timbers, the hatch, the beam) → the users' own acts (the setting, the wattle,
the talk) → the head's state again — the acts change the very water the next
reading reads`.

Closing edge: state-closing at the authored band — the allocation changes the
head, the head changes the next allocation. Band honesty: the gauge is
committed (the stone stair), the phases are committed (the calendar), and the
rise's own line is committed (the drowned fords + the double toll — the fourth
step's text); the allocation order, the reading at the turn and the enforcement
doors are authored (§6.2). Substrate: the weir, the race's timbers, the bank
market + the beam's talk (the committed rumor channel), the seasons. The
distinction from C (the mesh's own E-precedent class): the calendar feeds both,
but C's mediator is the weather bias + the hook and F's is the step rule + the
reading — the sky and the water are different stages, as the one-off flood (E)
is distinct from the recurring phase. The distinction from Loop A's family:
the enforcement has no axis, no threshold, no institutional door — the users'
physical act at the water is the council mechanism's negative image.

### Loop G — the winter kin: the notch → the recognition → the obligations (AUTHORED — §6.3's edge, iter-165)

`the minted notch (the stranded season's mark, seeded once — the winter
after the flood year's rise) → the recognition (the road's word: who
wintered where, who answered whom) → the obligations performed (the
protection, the barred purse, the mourning kept) → the recognition changed
— the standing deepened or starved, the betrayal inverted → the next
claim's standing`.

Closing edge: state-closing at the authored band — the recognition is the
circuit's own living state; each performance re-prices the next claim's
reading. Band honesty: the gauge surfaces are committed (the haft's tallies,
the road's word, the shelter law), the mint's terms and the obligations are
authored (§6.3). The distinction from E (the one-winter kinship): one
catastrophe, two circuits — the paper carries the winter's coin (money,
deferred, collectable), the notch the winter's care (obligation, bilateral,
durable); different mediators, different responses (the double toll vs the
obligations), different residues (standing vs recognition) — the disable
test passes both ways (remove the paper, the notch's duties stand; remove
the notch, the debt still collects). The distinction from B (the
seeded-residue driver class): B's driver is the grievance, G's the
recognition — the feud's negative pole and the care's positive pole of the
same seeded-history family; different mediators (the wergeld law's numeric
home vs the road's word), different responses (the vigil, faction-level, vs
the obligations, household-bilateral). The B⇄G edge: the betrayal inversion
— a winter kin turned enemy is the feud's next material, and the exclusion
rung is the door they meet at.

### The verdict

| Loop | Driver | Mediator | Response | Residue | Closure | Band |
|---|---|---|---|---|---|---|
| A | live fire event | fear axis + thresholds | council / patrol | changed world | state | committed |
| B | generated feud history | grievance + prohibition | the vigil | new memory | state | committed |
| C | the calendar clock | weather bias + hook | the murmur | market texture | clock | committed |
| D | the travel graph | condensation + names | born strangers | visible culture | reader | committed |
| E | the flood year | the debt's paper | the double toll | reputation + standing | state | committed beats, authored paper; the flow armed iter-162 |
| F | the recurring band | the step rule + the reading | the allocation's acts | legitimacy / resentment + the tally's record | state | authored (§6.2) |
| G | the minted notch | the road's word + the notch's proof | the obligations performed | the living recognition (or the inverted grievance) | state | authored (§6.3) |

Seven loops pass the disable test — no two share a driver, and the one shared
stage (the triangle's threshold dynamics feeding the intent door) carries two
different axes (fear, grievance) without making the loops one mechanism. The
band split is honest: A–D committed, E committed at its beats with the paper
authored and the flow armed (iter-162), F authored over committed gauges
(iter-164), G authored over the committed notch habit and the road's word
(iter-165). Ten named interlock edges: the alarm wakes both fear and grief
(A⇄B), the rain erases the smoke (C→A), the condensation materializes the
feud's carrier (B⇄D), the rise prices the toll (C⇄E), the season forces the
step (C⇄F — the rise turns the fourth, the dry band presses the second), the
paper prices the pool (E⇄F — the take rides the toll the step protects; the
keeper's timbers double-bound), and the feud residue prices the race's claim
(B⇄F — the protection read as theft; the timber law died in the feud's fire,
the water law lives in stone); one winter, two prices (E⇄G — the stranded
season's stores priced in coin by the paper and in duty by the notch; the
return lands in the stores-counting month, the debt's own reckoning season);
the feud's arithmetic meets the notch at the door (B⇄G — the exclusion rung
against the wergeld word; the betrayal the inversion path); and the road
materializes the return (D⇄G — the winter kin's claimant a named stranger,
the condensation's committed surface the carrier). Independent loops,
interlocked edges — not one engine wearing seven masks.

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

**The debt's lifecycle (the residue lifecycle trace, run iter-160 — the W4
experiment, `WORLD_WORKPLAN.md` §6):**

| Rung | The flood debt's lifecycle |
|---|---|
| EVENT | the flood year — committed as both spines' cause field |
| RESIDUE | the debt standing; the bend's reputation; the pole inherited |
| CARRIER | the guild's paper (authored); the pole (committed, carried); the weighing day's beam (committed — the guild already reads the trade) |
| HOLDER | the guild's factor; Ketta the debtor; Dellan the pole |
| TRANSFORMATION | partial repayment (a fat season's toll surplus); the bend hardening into custom |
| TRANSFER | the pole to the second hand (committed, iter-157); the debt's inheritance — the drowned generation's open question |
| CLEARANCE | a strong honest season outruns the paper |
| NEW OPTIONS | the debt clearable or the bend custom; the lever at the stair |

The trace's explanatory gain at the authored band: the household's internal
tension is one coin's two claims — Ketta's need (the debt cleared) and
Dellan's need (the punt bought back) draw on the same thin toll surplus; the
lifecycle makes the competition legible without any account state. The pole's
runtime gates (the verb-gate boundary, `WORLD_AUTHORING.md` §8): carried ⇒
untakeable, unstealable unless flagged (the `steal_target` flag committed
iter-161), breakable only by its carrier. Both embodiment options LANDED
(iter-161, pure pack data, zero core — the KI#87 precedent class): the
flood-story recognition token (the `read_pole` hinge minting
`the_flood_story`, registered in the secrets table over the toll-taker —
whoever learns the story holds a live lever at the stair, the coerce door
open; the story steps down to partial read by dark on the unlit stair) and
the player-facing ablation (the pole liftable unseen from the second hand; a
successful lift flips the carrier binding and the road-leg beat then walks
the second hand pole-less — test-pinned, `tests/test_poleseed.py`). The
debt's economy flow LANDED (iter-162, the `debt-1` row's build — pure
pack data over the res-1 substrate: the toll-taker's thin surplus + the
guild's chest at the weighbeam, the net-surplus flow + the collection flow
folded per the co-due limit, the reckoning a story beat; the paper's fall
and the clearance still authored — the flow vocabulary has no terminus).

**Embodiment (committed vs authored).** Committed: the spine (want/need/flaw/
cause), the coerce urgency entry (the purse-read double-toll beat), the shelter
law (the lowland prohibition set), the high_water lines (the drowned fords, the
punt men's double), the boathouse fire spot, the auditor's errand — and, since
iter-157, the second hand himself (Dellan: the kin/runner pair axes, the
road-leg urgency beat, the paired escort legs) and the punt pole (the item
committed; KI#87 closed iter-157); since iter-161 the pole's social half
(the flood-story recognition read `read_pole` + the secrets registration over
the toll-taker — the lever at the stair) and its theft gate (the
`steal_target` flag, the player-facing ablation; the lift and the pole-less
hop test-pinned, `tests/test_poleseed.py`). Authored here (WORKING): the debt's
guild-holder, the credit winter, the household's year, the debt's lifecycle
(the iter-160 trace above), and the debt's own standing arithmetic (the
paper twenty, the punt twelve — the arming's notes their mirror); the
flow's movement armed iter-162 (debt-1: the accounts + the two folded
flows, `tests/test_debt1.py`).

### 6.2 The step bench (WORKING — the second authored meso unit, iter-164)

The weir stair's water bench: the vale's three hands over one head, authored
over the committed substrate (the stair, the race's timbers, the bank market,
the seasons, the tally) — no new entity classes, no new institution beyond the
practitioners' own custom: the irrigation-tribunal MECHANISM, never the
institution (`WORLD_AUTHORING.md` §19 — a practice at the water, not a court
with officers; the bench is literal stone steps, the reading a habit, not an
office).

**Composition.** Three hands over one head of water, each a committed role
read at its own door: the weir keeper — the pool's hand (Ketta, committed: the
timbers hers to set daily; the toll's substrate is the pool she holds); the
steward of the burned name — the draw's hand (Wilmot, committed: Thornmill's
race, the `mill_race_timbers` fire spot; the grief-ramble the claim's own
voice walking); the market mistress — the run's hand (Maren, committed: the
weighbeam and the tally staff; the bank market rides the navigable Sarrow the
weir spills). The gateless present: the guild's factor (the paper prices the
pool's produce — the weighing day reads the trade the step rations; the guild
holds no water writ) and the watch (the writ runs on the road's fear, never
the river). The assembly probe's answer: the bench is not a committee — the
three hands meet only at the reading, and each leaves by a different door with
a different consequence (the timbers, the hatch, the beam's talk); the unit
cannot be honestly played as one homogeneous actor.

**The steps** (the law's own text — stone, four rungs):

| Step | The head it names | The standing allocation |
|---|---|---|
| first | the drought floor | the pool at the punt's grounding band — the crossing wades, the race shut, the run at the weir's drip; never set but by a drought the vale survives, and never unnotched |
| second | the low band's standing | the pool held for the crossing, the race at its trickle (the claim's wet proof, no more), the run light — the barges lighten or wait for the weighing day |
| third | the working head | the pool full, the race running whole, the run deep — the long_light default, the fat season's law |
| fourth | the rise | all claims flooded together: the race shut against the flood, the fords drowned, the crossing at double toll — the committed high_water line IS the fourth step's own text |

**The chain (the doctrine's ladder, walked once):**

| Rung | The step bench |
|---|---|
| CAUSE | the water quarrel — three claims on one head, settled once by the stair pact (the chronicle's quarrel collection: `pact_signed`, three members — the committed slot themed; the terms authored) |
| POSSIBILITY | the stair itself: the Sarrow leaves the hills at one step — the head nameable in stone, settable by one hand, shared by three uses |
| PRESSURE | the recurring band: the rise floods all claims at once (no scarcity), the late long_light starves all three together — every season's turn forces the re-reading |
| ACTORS | the keeper, the steward, the beam; the factor and the watch present but gateless |
| INSTITUTION | the step law: the head named by the stair's wet step, held by the practitioners' reading at the season's turn, enforced at the water by the users themselves — the pact's descendant, older than the guild's ledgers (the shelter law's own age class) |
| KNOWLEDGE | the keeper knows the water's present (the steps, the rise arithmetic) and the debt's size; the steward knows the pact's terms and the mill's name; the beam knows the trade's weight and the dry years' cost; the road knows only the rate — each map bounded and legitimate (the stranger reads a stingy ferryman, never the order: the books show the toll, not the step) |
| CONSEQUENCE | the timbers set: one use served, two priced; the dry band's second-step argument is the vale's standing quarrel made arithmetic |
| RESIDUE | the tally's notches (the dry years' sequence in wood); the race kept wet (a dry race rots — the claim's living proof); the resentment (the protection read as theft: all the manor got was a wet channel); the beam's memory (the grounding year weighs light) |
| NEW OPTION | the mill rebuilt (the claim made whole — the option the step law holds open); the guild's capture (the paper reaching for the steps — the failure mode); the navigation deepened (the bank's engineering, constrained by the standing step) |

**The bench's year** (the step over the committed phases — the allocation as
lived): thaw — the melt runs loud, the head high, no scarcity: the setting
loose, the spill takes the melt (the bench idle, the road soft, the toll
thin); high_water — the fourth step: the race shut, the fords drowned, the
crossing doubled (the committed beat — the rise's own law); long_light — the
third step falling: the fat season's working head, the dry weeks pressing
toward the second — the bench's standing argument (the race's trickle against
the pool's hold against the run's lightness); first_frost — the second step:
the still water, the stores counted, the steward's hatch watched through the
thin months.

**The enforcement (the mechanism's own door — the anti-council core).** A
breach of the standing step answers at the water, by the users, immediately —
no axis, no threshold, no institutional door (Loop A's family negative
image): the race's breach (the hatch opened against the step) finds the hatch
wattled — a hurdle thrown in the race's mouth, the physical act, reversible
and proportionate: the breach stilled, the next setting re-argues; the pool's
breach (the timbers set to the household's own book — the keeper's two
masters meeting in her one hand, the purse-read bend's water-side twin) is
read at the next weighing day against the tally's notch — the vale can count,
and the keeper knows it can; the run's claim rides the beam's talk (the
committed rumor channel — hearsay lives at Malby): the breaker's barges
weighed last, gossiped first. The function the immediacy performs: keeping the
guild out — a law unenforced at the water becomes the council's business at
the next dry band (the capture path, the perturbation test's own edge).

**The step law's residue lifecycle (the §8 trace, run iter-164):**

| Rung | The step law's lifecycle |
|---|---|
| EVENT | the water quarrel settled by the stair pact (the chronicle's quarrel collection — three members, three claims) |
| RESIDUE | the step custom; the tally's notches; the resentment; the beam's dry-year memory |
| CARRIER | the stair's stone (the law's own text, unburnable — the feud's material lesson: the timber law died in the mill's fire, the water law lives in stone); the tally staff (committed, Maren's — the market's keep-peace stick that also keeps the count); the race's wet timbers; the pole's haft tallies (committed — the family's payment count: one vale, one notch-keeping habit, a people that signs with a blade, not a pen) |
| HOLDER | the three hands jointly — deliberately not one holder (the assembly's own form) |
| TRANSFORMATION | each season's re-setting; each dry band's re-argument; the flood year's re-cut (the fourth step added after the flood — the law amended by catastrophe, the rise's committed line re-named) |
| TRANSFER | the arithmetic passes hand to hand — the drowned generation's steps now the toll-taker's, the second hand learning the reading (Dellan's own inheritance) |
| CLEARANCE / INHERITANCE | the pact's terms lapse only by a new pact; the custom inherits down the practitioners' lines |
| NEW OPTIONS | the mill rebuilt; the guild's capture; the navigation deepened |

The trace's explanatory gain at the authored band: the bench makes the vale's
water legible as ONE arithmetic shared by three doors — the steward's grief,
the keeper's double bind and the market's dry-year talk were three separate
committed textures; the step law is the one order they all price. The
perturbation test passes per transition: the rule's removal gives the vale the
strongest hand's water (the claim lapses, the mill-rebuilt option dies); the
enforcement's removal opens the capture path (the council enters the water
question at the next dry band); the memory's removal drifts the setting (the
grievance out-argues the arithmetic, the feud re-opens). Each removal changes
reachable futures, not prose.

**The crisis probe (the biography form, WORLD_TESTS §3).** The dry long_light
pressing the second step, the race found running whole at dawn — the hatch
open against the standing step — with the weighing day a week out and the
guild's take landing on a thin season. The chain walks on committed surfaces
(the seasons' phases, the toll's custom, the beam's weighing day, the rumor
channel): the required decisions are the keeper's timbers (tighten past the
second step and punish the whole run for the race's breach, or hold and wattle
the hatch), the wattle question (who throws it — the users' own law executed
at the water), and the beam's reckoning (the dry year's notch cut at the
weighing day). The consequences diverge per door: the hatch wattled deepens
the resentment (even the claim's own hand may not draw); the timbers tightened
grounds the fair's barges and buys the beam's grudge; the setting held pinches
the paper's payment through the toll's thin season. The residue: the notch,
the road's word, the steward's grief read as the feud's second theft. The
probe's missing links — three first-exposure substrate gaps, recorded, not
routed (the separate-track law): the water level (no runtime flow state — the
phases carry no head; the setting verb's landed read mints the LAW, never
the PRESENT — `read_stair`, iter-167), the setting verb (the reading at the
stair COMMITTED iter-167 — the `read_stair` hinge minting `the_step_law`,
the `read_pole` precedent's third instance; the wet step's current standing
stays authored), and the hatch gate (the wattle is prose — the verb-gate
boundary's honest answer, `WORLD_AUTHORING.md` §8).

**The humor probe (the generator form, WORLD_TESTS §3).** The cheapest safe
joke, market day at the beam in a dry band: "Four steps on the stair, and the
vale falls out over the middle two" — the stair the fool, no hand named, every
hearer owning the argument. The same words at Thornmill's gate read as the
vale's mockery of the claim (the middle two ARE the manor's trickle — the
steward hears his channel measured). Never joked: the pact's terms aloud (the
feud's wound) and the flood year's dead (the shelter law's other edge). The
joke's position-dependence is the shared-categories proof — the step is a
category the whole vale owns, and the beam's laughter re-prices the dry band's
grumbling into shared standing while the manor's gate holds its silence.

**Embodiment (committed vs authored).** Committed: the stair (the steps as
gauge — the stone), the race (`mill_race_timbers`, the fire spot), the bank
market (the navigable Sarrow, the weighbeam, the tally staff, the rumor
channel), the seasons (the four phases; the rise's drowned fords + double
toll — the fourth step's own line), the toll's custom, the grief-ramble (the
claim's voice), the chronicle's quarrel collection (the pact, three members),
the pole's haft tallies, the step's close read (iter-167, stepread: the
`read_stair` hinge — the pole's `read_pole` precedent's third instance, the
hinge family's first location-kind target — minting the literal token
`the_step_law` to the reader, plain knowledge never a secret: the step law
is the vale's own category, no lever; the brief's recalled facts the read
surface — §7.1's stranger row, the road's misread, correctable in play;
the unlit weir steps the night read down to partial; `tests/test_stepread.py`
the claim packet). Authored here (WORKING): the step law's PRESENT (the
four-rung allocation's current standing — the phases carry no head), the
stair pact's theming (the water quarrel), the enforcement doors (the hatch's
wattle, the beam's grudge, the keeper's book-setting breach), the tally's
notch record. The unit's remaining embodiment options — the notch record's
arming, the hatch — stay the owner's call class (the pole's iter-161
precedent); the live-session question stands (a real dry band, a real reader:
the meaning distribution's own unfinished band, §7.1's form).

### 6.3 The winter kin (WORKING — the constructed kinship edge, the third W4 addition, iter-165)

The constructed kinship edge: care performed under the shelter law through one
full stranded season mints a socially recognized kin edge — the milk-kinship
MECHANISM, never the practice (`WORLD_AUTHORING.md` §19's transfer law; the
documented donor: the Hindu Kush foster-relations research — `docs/ref/kurvitz.md`
ref-21's named pair with the irrigation tribunal). An edge, not a unit: the
mechanism binds the existing units, it adds no standing body. Authored over
committed substrate only — the shelter law (the lowland prohibition set), the
flood year (both spines' cause), the notch-keeping habit (the pole's haft
tallies — a people that signs with a blade, not a pen), the road's word (the
committed rumor channel), the condensation's named-stranger surface.

**The mint (the mechanism's own terms, three rungs).** RECOGNITION: the
winter's board through one full stranded season mints the edge — never the
night's board (the rarity gate: the stranded season is flood-year class, once
a generation; the ordinary meal prices nothing — the shelter law's gift stays
unpriced, a law, never a trade). OBLIGATION: the edge binds both ways — the
guest's line owes the host's house its standing duties (protection on the
road, the memory of the house's dead, the open door), the host's house owes
the barred purse (the purse-read bend's own boundary: kin-at-the-table are
never read for coin) — the exclusion rung. INHERITANCE: the edge passes down
both lines — the drowned generation's notch now the toll-taker's holding, the
guests' children carrying the same duties; the notch is never unnotched (the
first step's own vocabulary), but the recognition is living memory — the
road's word carries who answered whom (an unperformed duty starves the
standing; a betrayed edge inverts into the feud's next grievance — Loop B's
own material).

**The chain (the doctrine's ladder, walked once):**

| Rung | The winter kin |
|---|---|
| CAUSE | the stranded season — the winter after the flood year's rise, the fords drowned a full season, strangers under the crossing's roof (committed: the flood year, both spines' cause; authored: the winter — §6.1's credit winter, the borrowed punt twelve + the stranded season's stores eight = the paper twenty) |
| POSSIBILITY | the shelter law compels the care; the vale's notch habit gives the mint its form — the winter's guests cut into the host's own count, the same blade, the same staff |
| PRESSURE | the care's cost is real and by the law's own design one-sided: the stores eaten (eight coin of the eventual paper), the winter's care flowing to the debt — the law gives, the paper prices (§7.1's own shame) |
| ACTORS | the host household; the stranded guests (road strangers — the condensation's class); the road as witness; the guild absent by vocabulary (the paper has no row for a notch) |
| INSTITUTION | the recognition itself: held by the road's word and the haft's notch, never an office, never a court (the step bench's own gateless class — a practice at the table, not a tribunal) |
| KNOWLEDGE | the host knows the notch's names; the guest knows the door; the road knows the word (who wintered where, who answered whom); the guild knows nothing — each map bounded and legitimate |
| CONSEQUENCE | the edge performed: the protection rendered, the mourning kept, the purse barred — the flaw's income forgone at its own boundary; the edge starved: the standing thins; the edge betrayed: the grievance inverted |
| RESIDUE | the notch on the haft (permanent, never unnotched); the road's word (the living standing); the mourning line widened — the flood year's dead kept by name outside the bloodline |
| NEW OPTION | the winter kin's return (a named stranger at the stair claiming the notch — the option no other mechanism expresses); the drowned generation's mourning answered; the feud's arithmetic met at the crossing's own door |

**The edge's lifecycle (the §8 trace, run iter-165):**

| Rung | The winter kin's lifecycle |
|---|---|
| EVENT | the stranded season (the winter after the flood year's rise — the shelter law held at real cost) |
| RESIDUE | the winter kin edge — a recognized obligation, bilateral, inheritable |
| CARRIER | the host's own notch surface (the pole's haft — the payment tallies' own staff, the winter's guests cut into the family's count) + the road's word (the witness carrier) |
| HOLDER | both lines jointly — deliberately bilateral (the assembly probe's own form: the two sides hold different duties, the care flowed one way and the duties flow back, and neither side may honestly play the whole edge) |
| TRANSFORMATION | the standing rides performance and memory: the notch unchanged, the recognition living (the road's word carries who answered whom) |
| TRANSFER | down both lines (the drowned generation's notch now the toll-taker's; the guests' children inherit the duties) |
| CLEARANCE / INHERITANCE | the notch never unnotched — the edge outlives its minters; clearance only by mutual reckoning (a new pact's own class) or the holders' dying-out; the betrayal path inverts the edge into grievance (Loop B's next material) |
| NEW OPTIONS | the return; the widened mourning line; the feud's collision at the door |

The trace's explanatory gain at the authored band: the flood year's cost is
TWO carriers' work — the paper carries the winter's coin (Loop E: the debt,
the double toll, the standing), the notch carries the winter's care (the
obligations, the recognition). Without the edge the vale has one answer to
the stranded season's cost: the debt, and after it the bend — the one who ate
the winter's stores owing nothing, the next stranger paying for them (the
committed symptom: the spine's own flaw, "the crossing answers the heaviest
purse"). The perturbation test passes per transition: the mint's removal
returns the vale to the bend's single path; the carrier's reduction (the
notch unread) leaves the edge hearsay — contestable at the stair, the proof
gone; the exclusion rung's removal turns the edge into a discount — kin read
for coin after all, the inflation path the candidate's own warning made a
test; the transfer's removal kills the edge at the drowned generation — the
notch a dead mark (the read hinge's vague-unread failure surface's own
family). Each removal changes reachable futures, not prose.

**The crisis probe (the biography form, WORLD_TESTS §3).** The return: a
named hill-side stranger at the stair in the thin months (first_frost — the
stores-counting season), claiming the notch — the flood-year guest's son, the
crofts' tongue (feud-adjacent: the smelt line's own half of the vale). The
required decisions, all on committed surfaces: the purse question (Ketta's
flaw meeting the notch — the committed purse-read beat's own boundary case:
the exclusion rung bars the read against kin, the flaw's income forgone);
the protection question (the feud's word riding the guest — the wergeld
word is the hills' own prohibition walking the road, and the crossing's
roof is not a feud location: the vigil's arithmetic meets the notch at the
door, the B⇄G collision); the mourning question (the guest keeps the
drowned generation's names — his father's winter's debt: the flood year's
dead mourned at the crossing's table by the man whose father ate there).
The consequences diverge per door: the purse barred — the road re-reads the
crossing (the flaw's fork: the reputation's own event, an exception named
where the word had none); the protection rendered — the feud's word defied
at the door (the road carrying both words now, the elders' grudge the
price); the mourning kept — the grief given its second holder (the names
said aloud by a stranger, the tale's own surface). The debt stays untouched
— the honest boundary: the notch prices care, never coin (the paper's fall
and the punt's purchase stay the debt row's own future calls). The probe's
missing links — three first-exposure substrate gaps, recorded, not routed
(the separate-track law): the relation form (no committed non-blood kin
edge in the pair vocabulary — blood kin is a trust axis value; a recognized
standing would need its own form), the proof's read (the notch has no
committed action — the `read_pole` hinge reads the flood story, not the
guest count; the return's claim would need its own hinge family), and the
mourning surface (no non-blood grief registration — the grief_wakes
numeric-home law; the constructed kin's mourning would need a seeded entry,
the `the_flood_story` precedent's family).

**The humor probe (the generator form, WORLD_TESTS §3).** The cheapest safe
joke, market day at the beam: "Ask the crossing how many kin she keeps —
she'll count her pole" — the notch habit made comedy (a family that counts
its kin on its tool), no name named, every hearer owning the habit. The same
words at the guild's weighing day read as evasion — the collector hears a
toll dodge dressed as kinship (the paper has no row for a notch; kin a toll
category the guild cannot price). Never joked: the dead mark (a notch whose
names are gone — the drowned generation's unreadable count) and the betrayed
edge (kin turned enemy — the feud's next wound). The joke's
position-dependence is the shared-categories proof — the notch is a category
the whole vale owns, and the beam's laughter prices the habit into shared
standing while the guild's table holds its ledger silence.

**Embodiment (committed vs authored).** Committed: the shelter law (the
lowland prohibition set), the flood year (both spines' cause; the debt's own
authored arithmetic carrying the stranded season's stores eight), the
notch-keeping habit (the pole's haft tallies, the `read_pole` hinge's own
vocabulary), the road's word (the rumor channel), the seasons (first_frost's
stores-counting month), the condensation's named-stranger surface (the
return's carrier class), the grief's numeric-home law (the boundary the
mourning rung meets). Authored here (WORKING): the winter kin itself (the
mint's three rungs), the kin notch's meaning (the haft's payment tallies
re-read as the guest count — the same staff, a new mark's class), the
obligations (the protection, the barred purse, the mourning), the return
claim, the exclusion rung. The unit's embodiment options — the relation
form, the notch's read hinge, the mourning registration — stay the owner's
call class (the pole's iter-161 precedent); the live-session question stands
(a real return, a real reader: the meaning distribution's own unfinished
band, §7.1's form).

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
three times: the pole at the crossing, the wergeld word on the road, and the
winter kin's notch (the care inherited as duty down both lines, the flood's
dead kept by name outside blood, §6.3). The Thornmill family obligation,
open since this slice, is ANSWERED iter-164 (§6.2): the
manor's own household carries the mill fire's debt as the race's keeping — the
claim held wet at the price of its own tending (the vigil stays faction-level;
the obligation is the steward's household's own).

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
surfaces), a second time over the water's band (§6.2's step bench,
iter-164: the dry band walked the same chain — place/resource → the step law →
the setting → the breach → the bounded maps → the wattle and the beam's talk →
the notch and the resentment → the changed options) and a third time over the
care's band (§6.3's winter kin, iter-165: the stranded season walked the same
chain — the winter after the flood → the shelter law held → the notch minted → the
bounded maps → the road's word → the living recognition → the return's
standing option). The implementation witness carries the chain at the
single-NPC + companion band (iter-157: the second
hand, the pole — KI#87 closed; iter-161:
the pole's social half — the recognition read, the lever chain, the theft
gate, all test-pinned in `tests/test_poleseed.py`); the debt's economy flow
landed iter-162 (the `debt-1` row's build: the accounts + the fold's two
flows, the reckoning a story beat — `tests/test_debt1.py`; the paper's fall
and the punt's purchase stay authored, the flow vocabulary carrying no
terminus).
