# The Three Axes: Scenario × Product Form × Data

Last updated: 2026-09-17

Scope is not a feature list — it is a point in a three-dimensional space. The same validated job
produces a completely different solution depending on where it lands.

Resolve the axes **in `acs-shape-solution`, before `acs-define-outcomes` sets commitment and depth.** A
commitment table written before the product form is chosen is a table for an imaginary product:
"export to CSV" is trivial in a CLI, a week of work in a mobile app, and meaningless in a chat
agent. The axes decide what a capability *costs*; commitment and depth decide whether that cost
is worth paying.

## Table of Contents

- [Why Three Axes](#why-three-axes)
- [Axis 1: Scenario](#axis-1-scenario)
- [Axis 2: Product Form](#axis-2-product-form)
- [Axis 3: Data](#axis-3-data)
- [Resolving the Combination](#resolving-the-combination)
- [Failure Modes](#failure-modes)

---

## Why Three Axes

Each axis independently determines what "minimum" means:

- **Scenario** determines *when and where* the product is used, which constrains form.
- **Form** determines the cost of every feature and the shape of the first-use moment.
- **Data** determines whether the core promise is even possible to deliver.

The axes are ordered. Scenario constrains form; form and scenario together determine what data
must be available and when. Resolving them out of order produces scope that has to be redone.

---

## Axis 1: Scenario

Read from the shared primary scenario and journey records, which mark a primary scenario and
state five properties. Never re-derive these here — a missing property is a gap to resolve with
the user, not to guess at.

| Property | Values | What it constrains |
| --- | --- | --- |
| Frequency | Per-day / per-week / per-month / episodic | Whether habit formation or discoverability matters more |
| Session length | Seconds / minutes / a working session | Tolerable startup cost and interface density |
| Participants | Single user / collaborative / handed off | Whether accounts, sharing, and permissions can be committed at all |
| Connectivity | Always online / intermittent / offline required | Local-first vs. server-side architecture |
| Attention | Attended (user waits) / unattended (background) | Whether latency is a feature or irrelevant |

**The binding constraint.** One property usually dominates. A per-day, seconds-long, single-user,
attended scenario rules out anything with a login screen — the login costs more than the job. Name
the binding constraint explicitly before moving to form.

---

## Axis 2: Product Form

The delivery vehicle. Choose one; hybrids are a stage-3 concern, not an MVP.

| Form | Fits when | Minimum viable version | Hidden cost |
| --- | --- | --- | --- |
| **Script / CLI** | Technical user, unattended or fast attended, single participant | One command, one flag, stdout | Zero discoverability; nontechnical users cannot adopt it |
| **Chat / agent** | Input is natural language, task is open-ended, low frequency | One prompt + one tool call | Unpredictable output shape; hard to demo consistently |
| **Web app** | Collaborative, session-length work, needs to be linkable | One page, one action, no auth | Auth, hosting, and state are all latent commitment creep |
| **Mobile app** | On-the-go trigger, camera or location or notifications essential | One screen, one gesture | Store review cycles; a web app usually tests the assumption faster |
| **Embedded / plugin** | The job happens inside an existing tool the user already lives in | One command inside the host | Host API limits define the ceiling |
| **Internal tool / dashboard** | Sponsor-driven, workflow adoption is the signal | One view over real data | No price signal; commitment must be measured differently |
| **Wizard of Oz** | The automation is the expensive part and desire is unproven | A human doing it manually behind a simple interface | Does not scale — and must not, until desire is proven |

### Selection rule

Choose the **cheapest form that can produce the first-use moment** described in the shared
primary scenario and journey records. If a script can produce it, a web app is premature. The form
is a hypothesis about delivery, not a commitment to a platform.

### The Wizard of Oz test

Before choosing an automated form, ask: *could a human do this manually for the first 10 users?*
If yes, that is the form — and the capabilities behind it are committed at `manual` depth.
Automation is the second experiment, not the first.

---

## Axis 3: Data

The axis most often skipped, and the one that most often kills an MVP after the scope is approved.

For each data element the core promise depends on:

| Question | Why it decides scope |
| --- | --- |
| **Does it exist?** | If not, the MVP is a data-collection product, not the product you scoped |
| **Can you access it?** | API, export, scrape, manual entry, user-supplied — each has a different cost |
| **What does access cost?** | Money, rate limits, legal review, a partnership, a login you don't control |
| **Is it fresh enough?** | A daily-triggered scenario cannot run on monthly data |
| **Is it clean enough?** | Cleaning cost often exceeds the feature it enables |
| **Cold start?** | If value requires accumulated history, what does user #1 see? |
| **Legal and privacy?** | PII, regulated data, ToS restrictions, consent — these are gates, not tasks |

### Availability grades

| Grade | Meaning | Scope implication |
| --- | --- | --- |
| **A — In hand** | You have it now, legally, fresh enough | Build on it |
| **B — Reachable** | A known API or export, within budget, days of work | Committable if the promise depends on it |
| **C — Contingent** | Needs a partnership, a scrape of uncertain legality, or paid access at scale | Not committable as shaped. Prove desire without it |
| **D — Nonexistent** | Must be created by users or by you | The product is now about seeding this data. Say so explicitly |

**The rule:** a capability resting on grade C or D data cannot be `committed` at `full` depth. It
is `reduced` — usually to `narrowed` or `manual` — or it is `deferred` until the data is reachable.
A commitment that depends on data you cannot obtain is not a scope; it is a wish.

### Cold-start substitutes

| Problem | Substitute |
| --- | --- |
| Needs user history | Seed with the user's own imported data, or hand-curate for the first 10 |
| Needs a corpus | Hand-build a corpus of 50 items covering the primary scenario |
| Needs a network | Serve single-player value first; the network is experiment two |
| Needs a trained model | Prompt an existing model; train only after desire is proven |

---

## Resolving the Combination

Write the resolution as one sentence before handing the shape to `acs-define-outcomes`:

> "For **[primary scenario]**, delivered as a **[form]**, using **[data at grade X]**."

Then check the combination for coherence:

| Check | Fails when |
| --- | --- |
| Form serves the binding constraint | A per-day seconds-long job behind a login |
| Data freshness matches frequency | A daily scenario on a monthly export |
| Form matches participants | A collaborative job in a local-only CLI |
| Connectivity matches form | Offline-required job in a server-side web app |
| No grade C/D data behind a full-depth capability | Core promise depends on a partnership not yet signed |

A failed check means the combination is wrong, not that the feature list needs tuning. Fix the
axis, then hand the shape forward. A commitment table built on a failed coherence check has to be
rebuilt, not adjusted.

---

## Failure Modes

| Failure | Symptom | Fix |
| --- | --- | --- |
| **Form by default** | Building a web app because that's what products are | Ask what the cheapest form producing the first-use moment is |
| **Form by fashion** | It's an agent because agents are current | Check whether the input is genuinely natural language |
| **Data assumed** | "We'll get the data" appears nowhere in scope | Grade every element; C and D cannot be committed at full depth |
| **Cold start ignored** | The demo works with seeded data; user #1 sees an empty screen | Commit the empty state as a capability, or seed manually |
| **Scenario averaged** | Scope serves three scenarios adequately and none well | Pick the primary; the others are deferred |
| **Platform commitment** | Choosing mobile-native before desire is proven | Web first unless camera, location, or notifications are essential |
