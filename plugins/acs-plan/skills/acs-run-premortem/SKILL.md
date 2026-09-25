---
name: acs-run-premortem
description: Stress-test a plan by assuming it has already failed. Use when the user wants a pre-mortem, risk analysis, "what could go wrong" review, or devil's-advocate pass on any project or idea.
disable-model-invocation: true
---

# Pre-Mortem Analysis

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [change.proposal]
  retrieves: [product.relevant_context, design.contracts, operations.constraints]
  produces: [product.risk_assessment]
  updates: [product.risk_records]
  invalidates: [change.risk_dependents]
  handoff_to: [product, design, operations]
```

Shared semantics: [shared protocol](../../resources/skills-src/context/acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.


Run a 6-phase "project autopsy" starting from an assumed total failure, then produce a
risk analysis that enriches shared HTML product memory. The autopsy is a dialogue: the
user holds context the records do not, and the output is a reading of the risks that the
user has confirmed or explicitly disputed — not a list the model believes is true.
Questioning and confirmation follow [the shared-understanding protocol](../acs-brainstorm/references/shared-understanding.md).

## Shared Memory Contract

Read [the product memory contract](../acs-brainstorm/references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read the supplied plan or existing scope, relevant demand evidence, capabilities, gaps, and risks. Enrich existing failure scenarios before adding new ones. Hypothetical failures and quotes are exercises, never observed evidence.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Phase 1: Set the Gravestone Scene

Jump forward to **6 months from today**. The project has completely collapsed. Use the following as hypothetical prompts for the exercise, adapting them to the actual plan:

- **Data**: Daily active users (DAU) ≈ 0. The GitHub commit history has not been touched in 3 months.
- **Feedback**: The few users who tried it said *"I don't get how to use this"* or *"It's too slow."*
- **Personal state**: The developer has lost all motivation to even open the project folder. Talking about it feels like a chore.
- **Regression**: The developer is back to using Excel, sticky notes, or whatever manual tool the project was meant to replace. Six months of effort were effectively wasted.

Write the narrative vividly in the past tense, but label the entire scene and invented quotes as hypothetical. Never attach them as observed evidence or use them to downgrade demand evidence.

---

## Phase 2: Stress the Product Thread

Before enumerating causes, grill the plan's product reasoning — vision, demand, MVP, and
the discovery that produced them. This is where most products actually die, and the user
must hold these questions, not just receive a list.

Read from shared memory first: any candidate or confirmed `vision` record in `overview`
(and the claims it links), the demand assessment with its zones and evidence levels, and
the MVP scope with its core validation assumption. A missing record is itself a finding —
record its absence as an open question; do not invent a vision or a verdict to stress-test.

Then put **one question block** to the user, each question with a recommended answer drawn
from the records just read:

1. **Vision** — if the vision is wrong, what would have shown it by now, and why hasn't it?
2. **Demand** — which zone of the demand verdict would you least want to defend, and what
   observation would downgrade it?
3. **Commitment fit** — does the committed set actually test the core assumption, and what result
   could be misread as validation? Which `reduced` depth is doing more damage than its record admits?
4. **Discovery link** — which discovery finding, if it turned out to be an artifact of how
   we asked, invalidates the most downstream work?

The answers seed Phase 3 causes and are recorded as assumptions or questions on the records
they challenge. A stress question never confirms or rejects the vision and never downgrades
demand evidence — it exposes what would.

---

## Phase 3: Multi-Dimensional Autopsy — The Death List

Channel your inner "hater." Generate **10–15 distinct causes of death** spread across multiple failure dimensions, seeded by the Phase 2 answers. Each cause must:
- Name the **Dimension** (Demand, Mission / Coherence, Scenario, Habit, Market, Distribution, UX, Monetization, Scope, Personal, Tech, etc.)
- Answer the **Inversion Question** for that dimension (e.g., "What makes a user close it instantly?")
- State the specific, ruthless **Cause of Death**

Cover at least 7 of these dimensions. Product-thread dimensions lead the table because they
lead the autopsy: at this stage a product dies through demand, coherence, and adoption
before it dies through code. Implementation-level causes (Tech, performance, stack) stay a
minority of the list unless the plan itself is engineering-heavy.

| Dimension | Inversion Question |
|---|---|
| Demand | What makes a user close it instantly? |
| Mission / Coherence | How does the product ship its committed wedge yet fail its mission — features that never cohere into one product, wedge success that never extends? |
| Scenario | In what situation would users NEVER use this? |
| Habit | Why would they quit after two uses? |
| Market | Who already does this better? |
| Distribution | How does nobody ever find this? |
| UX | What makes the first 60 seconds of use confusing? |
| Monetization | Why does this never make money? |
| Scope | How does feature creep kill it? |
| Personal | When does the builder lose motivation? |
| Tech | What makes the code unmaintainable? |

The Mission / Coherence dimension consumes the vision record and stress answers already
gathered in Phase 2. A coherence failure scenario is still hypothetical: it never confirms
or rejects the vision, and never downgrades demand evidence.

Be specific, not generic. "The value prop is unclear" is weak. "Users open it once, can't figure out how to import their existing notes, and never return" is strong.

---

## Phase 4: Risk Rating — Prioritize the Fears

Score each cause of death:

> **Risk Score = Probability (1–5) × Severity (1–5)**

Assign a priority tier:
- **Critical (15–25 pts)** — Must be addressed in the first week of development
- **High (9–14 pts)** — Requires specific monitoring checkpoints in the dev plan
- **Medium (4–8 pts)** — Watch list; revisit monthly

Sort the list from highest score to lowest. Then present the Critical and High risks and
ask the user, in one block: which would you rank differently, which do you dispute
outright, and what is missing from the list entirely? A disputed score records both
readings and the observation that would settle it; the user's ranking does not overwrite
yours — the disagreement is the finding.

---

## Phase 5: The Vaccine Plan

For every **Critical** and **High** risk, write one concrete prevention action.

**Rule**: Never write *"I should be careful about X."* Always write *"To prevent X, I will do Y by [date/milestone]."*

Examples of the required format:
- *"To prevent feature creep killing momentum, I will freeze the feature list at 1 core function for v1.0 and move all other ideas to a 'Not Doing' list."*
- *"To prevent users bouncing on first use, I will run a 5-minute usability test with 3 real people before any public launch."*
- *"To prevent tech debt making the codebase unmaintainable, every AI-generated function must include a manually written unit test before I move to the next feature."*

---

## Phase 6: Enrich shared risks

Before persisting, run the close from `references/shared-understanding.md`: state what the
autopsy established, what remains assumption, and where the user disputed a score or a
cause — and apply their corrections. Confirmed and disputed readings are recorded
distinctly; a disputed risk carries both readings.

Read [the report mapping](references/report-template.md). Update risk, metric, constraint, assumption, and question records in `discovery.html`. Match existing failure scenarios by affected capability, trigger, and consequence before adding one. Attach risk scores and mitigation proposals; link shared scope and gaps instead of copying them.

A proposed pivot or scope cut stays a proposal. Record user-authorized changes with their basis and route to the appropriate scope skill to reconcile the delta; do not silently rewrite scope or close a gap. Return routing updates to the coordinator with changed anchors and report the HTML path.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## What This Skill Does NOT Do

- **Does not scope the MVP** — it stress-tests a plan, it does not create one
- **Does not validate demand** — it assumes failure, it does not grade evidence
- **Does not write the PRD** — it produces risks and mitigations, not the spec
- **Does not design the solution** — it finds what could go wrong, not what to build
