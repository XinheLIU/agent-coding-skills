---
name: scope-mvp
description: >
  Turn a validated solution into a scoped MVP. Resolves the three scope axes — scenario ×
  product form × data availability — then triages features into P0 (build now), P1/P2 (not
  yet), and Not-To-Do (never for this MVP), anchored to one falsifiable core assumption.
  Includes an ambition review: challenges whether the scope is the right bet, not just a
  complete one. Use when the user asks to scope an MVP, prioritize features, decide what to
  build first, choose a product form, plan a validation sprint, think bigger, cut scope, or
  review product strategy. Reads the demand classification and primary scenario from earlier
  discovery artifacts rather than re-deriving them.
---

# Scope MVP

Last updated: 2026-08-10

Transform a validated solution into a disciplined MVP scope. The output is a triage — what to
build, what to defer, what never to build — anchored to a single falsifiable assumption and
located at one explicit point in the scenario × form × data space.

Read `references/axes.md` before triaging features and `references/mvp-principles.md` for the
full triage framework.

## Boundary

Scope, not implementation. Do not review architecture, code quality, security, observability,
or deployment — those belong to the technical design and review skills. Do not re-derive the
demand type or the primary scenario; those are owned upstream.

## Shared Memory Contract

```text
Layer:    working — the triage and the reasoning behind it
Owns:     <work-root>/<effort>/discovery/mvp.md
Promotes: requirement list, scope boundaries, Not-To-Do list → PRD Part 1, via write-prd
```

Read `docs/agents/memory.md`, the active `state.md`, and the upstream artifacts —
`discovery/demand.md` for the demand classification and evidence grade, `discovery/solution.md`
for the primary scenario, user stories, and first-use moment. Read
`<product-docs>/<slug>/prd.md` when it exists, and triage against the stories recorded there.

Preserve the owned demand classification, persona, and journey. Write only axis resolution,
scope, validation assumptions, exclusions, ambition review, and success measures. Update
`state.md` with the artifact pointer and `run-premortem` as the default next transition, or
`prototype` when an unresolved design question blocks scoping.

The Not-To-Do list is the most durable thing this skill produces and the easiest to lose. It
answers a question that recurs for years — *why doesn't this product do X?* — and the answer is
worthless if it dies with the work root. Recommend `/write-prd` once scope is locked, so the
requirement list, the in/out-of-scope split, and the Not-To-Do list reach the tracked layer. The
axis reasoning and the ambition review can stay here; the commitments cannot.

If `discovery/demand.md` records evidence grade D (assumption only), stop and say so: scoping
an MVP for unvalidated demand produces a precise answer to the wrong question. Route back to
`/validate-demand`.

---

## Workflow

### Step 1: Extract the core assumption

Identify the single riskiest bet. If the user hasn't stated it, derive it:

> "I assume that **[target user]** has a problem with **[pain point]**. They will use
> **[our solution]** to **[key action]** because it is **[specific advantage]** than their
> current way of doing things."

Reference the demand classification from `discovery/demand.md` — do not reclassify. If the
input is ambiguous, confirm the assumption with the user before continuing. A fuzzy assumption
produces a fuzzy MVP.

### Step 2: Resolve the three axes

Before any feature triage, locate the MVP in scope space. Read `references/axes.md` for the
selection tables and coherence checks.

1. **Scenario** — read the primary scenario and its five properties from
   `discovery/solution.md`. Name the binding constraint (the property that rules out the most
   options). Do not re-derive the scenario; if `solution.md` lacks the properties, send it back.
2. **Product form** — choose the cheapest form that can produce the first-use moment. Apply the
   Wizard of Oz test: if a human could do this manually for the first 10 users, that is the form.
3. **Data** — list every element the core promise depends on and grade each A–D. Any grade C or
   D dependency in the P0 path must be removed from P0 or replaced with a manual substitute.

Write the resolution as one sentence, then run the coherence checks:

> "For **[primary scenario]**, delivered as a **[form]**, using **[data at grade X]**."

A failed coherence check means the combination is wrong — fix the axis, then triage.

### Step 3: Triage features with the Three Soul Questions

Run every capability through the filter (full decision table in
`references/mvp-principles.md`). Judge cost against the chosen form, not in the abstract.

1. **Required for the product to function at all?** → P0 candidate or cut
2. **Does it directly test the core assumption?** → keep or cut
3. **Does a user need it in the first 30 seconds?** → P0 confirmed or demote to P1

**Guard rail:** more than 5 P0 items means the core assumption is still too broad. Narrow it.

**Prototype loop:** when any step surfaces a design question conversation can't settle — how a
state transition should work, what a layout should look like — route to `/prototype`. It builds
throwaway variants, records the decision in `prototypes/<slug>/decision.md`, and returns
control here; resume at the step that raised the question. Loop as often as questions emerge.

### Step 4: Build the Not-To-Do list

- **Not now (P1/P2)** — worth building if the assumption holds. Assign a trigger
  ("after 10 paying users").
- **Not ever (for this MVP)** — polish, scaling infra, secondary personas, and automation a
  manual process can stand in for.

### Step 5: Review the ambition

Scope can be complete and still be the wrong bet. Challenge it before committing.

Map the trajectory:

```text
CURRENT USER EXPERIENCE → PROPOSED MVP → 12-MONTH IDEAL
```

State whether this MVP creates a path toward the ideal or a local optimum that will have to be
thrown away. Then select one posture from the evidence — ask the user only when their intent
doesn't already make it clear:

| Posture | Use when | Action |
| --- | --- | --- |
| **Hold** | Scope is right and focus is the advantage | Defend the boundary, remove distractions |
| **Reduce** | Scope exceeds what's needed to test the riskiest assumption | Cut to the smallest value-bearing experiment |
| **Selective expand** | Baseline is sound; a few adjacent bets may compound | Offer individually selectable additions |
| **Expand** | The wedge is proven but the plan misses a disproportionate opportunity | Describe the 10x experience and candidate additions |

When the posture is Expand or Reduce, produce two or three meaningfully different options —
including a focused baseline. For each: target outcome, wedge and differentiation, distribution
path, assumptions tested, effort class (S/M/L/XL), upside, failure mode, and what is explicitly
out of scope.

Recommend one and name the evidence that would change the recommendation. **No scope change is
accepted without explicit user approval.** If the user accepts a change, revise the P0 list and
re-run the Step 2 coherence checks — a scope change can invalidate the form or data choice.

### Step 6: Sketch the 4-week validation sprint

- **Week 1:** scoping, core assumption, and Not-To-Do list finalized
- **Week 2:** build the minimum carrier in the chosen form
- **Week 3:** test with 5–10 real target users (observe, don't sell)
- **Week 4:** decide — pivot, persevere, or stop

### Step 7: Define anti-vanity success metrics

Pick 1–2 metrics that prove the core assumption, not general engagement. Name the vanity
metrics to avoid explicitly.

---

## Output Format

Write to `<work-root>/<effort>/discovery/mvp.md`:

```markdown
# MVP Scope: [Product Name]

Last updated: [YYYY-MM-DD]

## Core Assumption
> [Filled template]

Demand type: [from discovery/demand.md] · Evidence grade: [A/B/C]

## Scope Axes
For **[primary scenario]**, delivered as a **[form]**, using **[data at grade X]**.

| Axis | Resolution | Why |
| --- | --- | --- |
| Scenario | ... | Binding constraint: ... |
| Form | ... | Cheapest form producing the first-use moment |
| Data | ... | Grades: ... · Substitutes: ... |

## What We're Building (P0)
| Feature | Why it's P0 |
| --- | --- |

## What We're NOT Building Yet (P1/P2)
| Feature | When to revisit |
| --- | --- |

## What We're NEVER Building for This MVP
- ...

## Ambition Review
Trajectory: [current] → [MVP] → [12-month ideal]
Posture: [Hold / Reduce / Selective expand / Expand]

| Proposal | Decision | Reason |
| --- | --- | --- |

Evidence that would change this: ...

## 4-Week Validation Sprint
- **Week 1–4:** ...

## Success Metrics (Not Vanity)
- Metric: [what it proves]
- ~~Vanity metric to avoid~~

## Open Questions / Risks
- ...
```

---

## Key Principles

- An MVP is not a cheap product. It is **the cheapest way to buy an answer**.
- Scope is a point in three-dimensional space, not a feature list. Resolve the axes first.
- A Wizard of Oz manual process beats an automated system for validating desire.
- A user who tolerates a buggy, ugly version to solve a real problem is stronger signal than
  1,000 sign-ups.
- "I'd use it if it had X, Y, Z" is polite rejection, not validation.
- A P0 that depends on data you cannot obtain is a wish, not a scope.

**Next step:** `/run-premortem` to stress-test the scope. Return here if the premortem surfaces
a scope change. Route to `/prototype` first when an unresolved design question would make the
P0 triage a guess.

## Source adaptation

Triage framework and validation sprint adapted from the MVP-design material in the
skills-manager `Product & Strategy` setup. Ambition review adapted from gstack
`plan-ceo-review`, keeping its premise challenge, dream-state mapping, scope postures, and
explicit opt-in decisions while dropping its engineering mega-review and runtime dependencies.
The three-axis model is original to this system.
