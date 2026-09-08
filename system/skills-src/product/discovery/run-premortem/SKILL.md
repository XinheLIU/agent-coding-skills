---
name: run-premortem
description: Stress-test a plan by assuming it has already failed. Use when the user wants a pre-mortem, risk analysis, "what could go wrong" review, or devil's-advocate pass on any project or idea.
disable-model-invocation: true
---

# Pre-Mortem Analysis

Last updated: 2026-09-08

Run a 5-phase "project autopsy" starting from an assumed total failure, then produce a
risk analysis that enriches shared HTML product memory.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.

```text
Layer:       working
Contributes: risks, mitigations, constraints, monitoring metrics, linked gaps, assumptions, questions
Writes:      <work-root>/<effort>/discovery.html — shared records, not an exclusive section
Promotes:    accepted mitigations, edge cases, NFRs and monitoring decisions → product.html, via write-prd
```

Read the supplied plan or existing scope, relevant demand evidence, capabilities, gaps, and risks. Enrich existing failure scenarios before adding new ones. Hypothetical failures and quotes are exercises, never observed evidence.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and update `state.md` with record anchors. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Phase 1: Set the Gravestone Scene

Jump forward to **6 months from today**. The project has completely collapsed. Use the following as hypothetical prompts for the exercise, adapting them to the actual plan:

- **Data**: Daily active users (DAU) ≈ 0. The GitHub commit history has not been touched in 3 months.
- **Feedback**: The few users who tried it said *"I don't get how to use this"* or *"It's too slow."*
- **Personal state**: The developer has lost all motivation to even open the project folder. Talking about it feels like a chore.
- **Regression**: The developer is back to using Excel, sticky notes, or whatever manual tool the project was meant to replace. Six months of effort were effectively wasted.

Write the narrative vividly in the past tense, but label the entire scene and invented quotes as hypothetical. Never attach them as observed evidence or use them to downgrade demand evidence.

---

## Phase 2: Multi-Dimensional Autopsy — The Death List

Channel your inner "hater." Generate **10–15 distinct causes of death** spread across multiple failure dimensions. Each cause must:
- Name the **Dimension** (Demand, Tech, UX, Habit, Market, Personal, Scenario, Distribution, Monetization, etc.)
- Answer the **Inversion Question** for that dimension (e.g., "What makes a user close it instantly?")
- State the specific, ruthless **Cause of Death**

Cover at least 7 of these dimensions:

| Dimension | Inversion Question |
|---|---|
| Demand | What makes a user close it instantly? |
| Tech | What makes the code unmaintainable? |
| UX | What makes the first 60 seconds of use confusing? |
| Habit | Why would they quit after two uses? |
| Scenario | In what situation would users NEVER use this? |
| Market | Who already does this better? |
| Personal | When does the builder lose motivation? |
| Distribution | How does nobody ever find this? |
| Monetization | Why does this never make money? |
| Scope | How does feature creep kill it? |
| Mission / Coherence | How does the product ship its P0 wedge yet fail its mission — features that never cohere into one product, wedge success that never extends? |

For the Mission / Coherence dimension, read any candidate or confirmed `vision` record in
`overview` (and the claims it links) as input. If none exists, record its absence as a
finding — do not invent a vision to stress-test. A coherence failure scenario is still
hypothetical: it never confirms or rejects the vision, and never downgrades demand evidence.

Be specific, not generic. "The value prop is unclear" is weak. "Users open it once, can't figure out how to import their existing notes, and never return" is strong.

---

## Phase 3: Risk Rating — Prioritize the Fears

Score each cause of death:

> **Risk Score = Probability (1–5) × Severity (1–5)**

Assign a priority tier:
- **Critical (15–25 pts)** — Must be addressed in the first week of development
- **High (9–14 pts)** — Requires specific monitoring checkpoints in the dev plan
- **Medium (4–8 pts)** — Watch list; revisit monthly

Sort the list from highest score to lowest.

---

## Phase 4: The Vaccine Plan

For every **Critical** and **High** risk, write one concrete prevention action.

**Rule**: Never write *"I should be careful about X."* Always write *"To prevent X, I will do Y by [date/milestone]."*

Examples of the required format:
- *"To prevent feature creep killing momentum, I will freeze the feature list at 1 core function for v1.0 and move all other ideas to a 'Not Doing' list."*
- *"To prevent users bouncing on first use, I will run a 5-minute usability test with 3 real people before any public launch."*
- *"To prevent tech debt making the codebase unmaintainable, every AI-generated function must include a manually written unit test before I move to the next feature."*

---

## Phase 5: Enrich shared risks

Read [the report mapping](references/report-template.md). Update risk, metric, constraint, assumption, and question records in `discovery.html`. Match existing failure scenarios by affected capability, trigger, and consequence before adding one. Attach risk scores and mitigation proposals; link shared scope and gaps instead of copying them.

A proposed pivot or scope cut stays a proposal. Record user-authorized changes with their basis and route to the appropriate scope skill to reconcile the delta; do not silently rewrite scope or close a gap. Update `state.md` with changed anchors and report the HTML path.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections (`overview`, `users-problems`, `capabilities-journeys`, `gaps-opportunities`, `questions-assumptions`, `evidence`, `scope-decisions`, `risks-measures`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## What This Skill Does NOT Do

- **Does not scope the MVP** — it stress-tests a plan, it does not create one
- **Does not validate demand** — it assumes failure, it does not grade evidence
- **Does not write the PRD** — it produces risks and mitigations, not the spec
- **Does not design the solution** — it finds what could go wrong, not what to build
