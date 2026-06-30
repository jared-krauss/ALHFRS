# Data Visualization Ideas — ALHFRS deployment data

Recommendations only. Nothing here is implemented. Each idea borrows a technique that
biologists, epidemiologists or criminologists use to read maps-over-time, then points it
at the ALHFRS deployment dataset (644 Met records + BTP + private, 2020–2026).

A note on framing first: these are *surveillance* deployments, not disease or wildlife. The
borrowed techniques are about reading **where-and-when** patterns — the maths is neutral, but
the story the project tells is about police behaviour and civil liberties, not "outbreaks."
A couple of ideas below flag where the disease metaphor could mislead, so it's used carefully.

---

## 1. Space-time cube ("stacked years" 3D view)
**Borrowed from:** epidemiology (the space-time cube is the standard way outbreak analysts show
*where* and *when* together without animation).

**Plain English:** Imagine the London map laid flat, then stack a transparent copy for each year
on top — 2020 at the bottom, 2026 at the top. Each deployment is a dot floating at its map
position and its year-height. Looking at the stack from the side, you instantly see which spots
have a tall column of dots running up through every year (persistent targets like Croydon and
Stratford) versus places that light up once and never again.

**Question it answers:** Which locations have been deployed at *repeatedly across years*, and which
were one-offs? Where did the Met start, and how did the geography spread or concentrate over time?

**Pros:** Shows the time dimension without making the user scrub a slider; the "tall columns"
read as the project's core argument (entrenchment at specific communities). Visually striking —
fits an art exhibition.
**Cons:** True 3D in a browser is fiddly and can be hard to read on a phone; needs a good default
camera angle. Could feel gimmicky if not designed cleanly. Best as a gallery/desktop centrepiece,
not the primary map.

---

## 2. Repeat-deployment intensity surface (kernel-density "heat" toggle)
**Borrowed from:** criminology hotspot mapping and ecology home-range estimation both use *kernel
density estimation* — a smooth "where is the activity concentrated" surface rather than countable dots.

**Plain English:** A toggle that swaps the dots for a soft glow showing where deployments cluster
most densely — bright where the Met returns again and again, fading to nothing in boroughs never
visited. This is the same maths ecologists use to draw an animal's "home range."

**Question it answers:** If you zoom out from individual days, what is the *overall geographic
footprint* of London facial recognition? Where is the centre of gravity?

**Pros:** Communicates concentration instantly to a non-expert; complements the precise dot map.
The dataset already clusters hard (Croydon, Westminster, Stratford) so the surface will be vivid.
**Cons:** Smoothing hides the underlying record count — viewers can mistake "smooth blob" for
"continuous surveillance everywhere in this area," which isn't true. Needs a caption clarifying it's
a density estimate, not coverage. The "home range" metaphor (police as a roaming animal) is
provocative — could be powerful or could read as glib; Jared's call.

---

## 3. Borough-frequency bar chart (ranked)
**Borrowed from:** plain descriptive epidemiology (case counts by district) — deliberately simple.

**Plain English:** A horizontal bar chart, one bar per London borough, sorted longest-first by
number of deployments. Croydon's bar runs off the end; many boroughs have none.

**Question it answers:** Which boroughs bear the overwhelming majority of deployments? How unequal
is the distribution across London?

**Pros:** The single clearest "this is not spread evenly" statement; trivial to build from existing
`borough` fields; accessible (works for screen readers and colour-blind users as plain text+length).
A natural companion panel to the map.
**Cons:** Loses all within-borough and time detail. Borough boundaries are an administrative
accident, not where people experience surveillance. Should be paired with a "per 100k residents"
option (using the census data already in the Garbett source) or it just tracks borough size.

---

## 4. Operator-type stacked area timeline
**Borrowed from:** social-science trend charts (stacked composition over time).

**Plain English:** A timeline along the bottom (2020 → 2026) where the height of the band is the
number of deployments per month, split into coloured layers: Met Police, British Transport Police,
private/Facewatch. You watch the total grow and see *who* is driving the growth at each point.

**Question it answers:** Is the expansion of facial recognition led by police, by private retail, or
both — and when did each accelerate? Did anything (a court ruling, a policy change) bend the curve?

**Pros:** Tells the "rapid expansion" story the news archive is full of; lets you annotate it with
the legal cases from `enforcement-actions.json` (e.g. mark the Bridges v South Wales judgment).
Time-series is honest about the post-2024 surge in the data.
**Cons:** Private/BTP counts are tiny next to Met, so their bands will be thin slivers — may need a
separate small-multiple or a log option. The 2020–2023 data is sparse, so early months look noisy.

---

## 5. Data-quality donut (the project's honesty meter)
**Borrowed from:** nothing exotic — a composition chart, but used as an *epistemics* device.

**Plain English:** A single ring split into three slices — `confirmed`, `approximate`, `unverified`
— showing what proportion of the dataset is primary-sourced versus inferred. Click a slice to filter
the map to just those records.

**Question it answers:** How solid is the evidence base? How much of what we're mapping is rock-solid
FOI disclosure versus best-effort inference?

**Pros:** Uniquely on-brand — this project's whole ethic is "accuracy over polish," and a viewer
who can *see* the uncertainty trusts the rest more. Cheap to build (one existing field). Doubles as
a filter.
**Cons:** Risk of looking defensive ("look how much is unverified"). Needs framing as a strength
(transparency), not an apology. Low standalone interest — best as a small widget beside the map.

---

## 6. Near-repeat space-time scan (the "return pattern")
**Borrowed from:** criminology's *near-repeat victimization* analysis — after an event at a location,
is there an elevated chance of another event nearby within a short window?

**Plain English:** For each deployment, look at how soon the Met came back to the same spot (or one
within ~300m). Visualise it as a small chart: on the horizontal axis, "days until the next deployment
within 300m"; taller bars at the short end mean the Met tends to *return quickly* to the same places.

**Question it answers:** Does the Met treat certain streets as standing targets it revisits on a
regular cadence, rather than responding to discrete events? Is there a rhythm to redeployment?

**Pros:** Turns the (already-clustered) data into a behavioural finding — "they keep coming back to
the same corner every N weeks" is a strong, defensible claim. Uses the `location_cluster_id` tags
Workstream A just added. Genuinely novel angle versus a plain map.
**Cons:** Analytically the heaviest idea here; needs careful distance/time thresholds and a clear
caption or it's opaque. The crime-analysis framing is borrowed *in reverse* (here the police are the
recurring actor, not the offender) — interesting but needs explaining so it doesn't confuse.

---

## 7. Arrests-vs-faces-scanned scatter (the efficacy question)
**Borrowed from:** standard scientific scatter plots used to test a claimed relationship.

**Plain English:** One dot per deployment that has outcome data: horizontal = faces scanned (crowd
size), vertical = arrests made. If facial recognition were highly productive you'd expect a clear
upward trend; if most deployments scan thousands of faces for one or zero arrests, the cloud sits
flat along the bottom.

**Question it answers:** How many people are scanned per arrest? Does scanning more faces actually
produce more arrests — i.e. is this proportionate?

**Pros:** Speaks directly to the proportionality / civil-liberties argument with the project's own
numbers. The Garbett source carries faces-seen and arrest counts for many 2024 records.
**Cons:** Outcome data is **sparse and inconsistent** across the dataset (CLAUDE.md flags this) —
the chart would only cover the minority of records with both numbers, and must say so or it
misleads. Risk of implying "more arrests = good," which cuts against the project's stance; framing
matters.

---

## 8. Deployment-duration / dot-size encoding on the existing map
**Borrowed from:** ecology's graduated-symbol maps (symbol size = magnitude).

**Plain English:** Keep the current dot map, but let each dot's size encode something quantitative —
either the deployment's duration (hours the cameras ran) or watchlist size (how many people it was
scanning *against*). A big dot = a long deployment or a huge watchlist. (The map already sizes dots
by arrests; this would be an alternative size-mode toggle.)

**Question it answers:** Where were the *longest* or *largest-watchlist* operations? Do the biggest
operations cluster differently from the most frequent ones?

**Pros:** Reuses the existing map and the size-encoding machinery already in `map-embed.html`; low
build cost. Watchlist size is one of the more alarming numbers in the data (tens of thousands) and
deserves a visual home.
**Cons:** Adding more meanings to dot size risks overloading one channel — needs a clear toggle and
legend so "big dot" isn't ambiguous. Duration data is patchier than arrest data.

---

## Suggested priority (if Jared wants a steer)
- **Quick wins, high clarity:** #3 borough bar chart, #5 data-quality donut, #4 operator-type
  timeline. Cheap, accessible, directly support the argument.
- **Signature / exhibition piece:** #1 space-time cube — the most memorable, most "art-show."
- **Strongest new finding:** #6 near-repeat return pattern — turns the clustering into a claim.
- **Handle with care (framing-sensitive):** #2 density surface and #7 arrests scatter — powerful but
  easy to misread; each needs a caption that controls the interpretation.

## Sources consulted
- Space-time cube / STKDE in epidemiology — [PubMed: space-time cube COVID-19](https://pubmed.ncbi.nlm.nih.gov/32249952/),
  [EpiVECS, Nature Scientific Reports](https://www.nature.com/articles/s41598-023-48484-9)
- Crime hotspot KDE & near-repeat victimization — [STKDE predictive hotspot framework, arXiv](https://arxiv.org/pdf/2006.00272),
  [Crime mapping lab — what is a hot spot](https://bookdown.org/gmcirco42/crime_mapping_and_analysis/lab3.html)
- Ecology home-range / utilization distribution & flow maps — [Movement-based 3D space-use, PLOS One](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0101205),
  [Migration Mapper corridors](https://www.researchgate.net/publication/363276387)
