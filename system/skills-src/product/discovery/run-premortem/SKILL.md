---
name: run-premortem
description: Stress-test a plan by assuming it has already failed. Use when the user wants a pre-mortem, risk analysis, "what could go wrong" review, or devil's-advocate pass on any project or idea.
---

# Pre-Mortem Analysis

Last updated: 2026-08-17

Run a 5-phase "project autopsy" starting from an assumed total failure, then produce a
structured Markdown report.

## Shared Memory Contract

```text
Layer:    working — the risk analysis behind the plan
Owns:     <work-root>/<effort>/discovery/premortem.md
Promotes: edge cases, NFRs → PRD Part 3, via write-prd
```

Read `docs/agents/memory.md`, the active `state.md`, `discovery/mvp.md` (scope axes, P0 list,
Not-To-Do list), and `discovery/demand.md` (demand type and evidence grade) when present. Write
risks, evidence, scores, prevention actions, and monitoring signals without duplicating the
scope. Update `state.md` with the artifact pointer.

See `references/report-template.md` for the exact output format.

---

## Phase 1: Set the Gravestone Scene

Jump forward to **6 months from today**. The project has completely collapsed. Internalize all of these as facts before proceeding:

- **Data**: Daily active users (DAU) ≈ 0. The GitHub commit history has not been touched in 3 months.
- **Feedback**: The few users who tried it said *"I don't get how to use this"* or *"It's too slow."*
- **Personal state**: The developer has lost all motivation to even open the project folder. Talking about it feels like a chore.
- **Regression**: The developer is back to using Excel, sticky notes, or whatever manual tool the project was meant to replace. Six months of effort were effectively wasted.

Do not soften this. Do not say "might" or "could." Treat the failure as historical fact.

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

## Phase 5: Output the Report

Write the final report in Markdown following the template in `references/report-template.md`, with a refreshed `Last updated: YYYY-MM-DD` near the top.

Save to `<effort>/discovery/premortem.md`. Confirm the file path to the user when done.

## What This Skill Does NOT Do

- **Does not scope the MVP** — it stress-tests a plan, it does not create one
- **Does not validate demand** — it assumes failure, it does not grade evidence
- **Does not write the PRD** — it produces risks and mitigations, not the spec
- **Does not design the solution** — it finds what could go wrong, not what to build
