---
name: scope-mvp
description: Triage a greenfield or new-product MVP into disciplined first-slice scope anchored to one falsifiable assumption. Use when the user asks to scope an MVP, prioritize features for a new product, decide what to build first, cut scope, or plan a validation sprint; for existing-product improvements, use scope-product-increment.
disable-model-invocation: true
---

# Scope MVP

Last updated: 2026-09-09

Transform a validated solution into a disciplined MVP scope. The output is a triage — what to
build, what to defer, what never to build — anchored to a single falsifiable assumption and
located at one explicit point in the scenario × form × data space.

Read `references/axes.md` before triaging features and `references/mvp-principles.md` for the
full triage framework.

## Boundary

Scope, not implementation. Do not review architecture, code quality, security, observability,
or deployment. Do not re-derive the demand type or the primary scenario; those are owned upstream.
For active-product improvements, route to `scope-product-increment` instead of forcing an MVP
shape onto existing behavior.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.

```text
Layer:       working
Contributes: scope decisions, capability priorities, validation assumptions, exclusions, metrics, questions
Writes:      <work-root>/<effort>/discovery.html — shared records, not an exclusive section
Promotes:    accepted scope, rationale, exclusions, success measures → product.html, via write-prd
```

Read demand assessments, scenarios, capabilities, constraints, risks, and accepted scope. Resolve scope axes and link selected capability IDs; do not rewrite their current behavior or demand grade.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and update `state.md` with record anchors. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

If demand evidence is assumption-only, disputed, Yellow, or Red, record the blocking claim and route to `validate-demand` before treating scope as a validated commitment. If the user already authorized an exploratory scope, keep it proposed and preserve the unresolved validation question. Absence of an earlier skill file alone is not a blocker.

## Workflow

### Step 1: Extract the core assumption

Identify the single riskiest bet. If the user hasn't stated it, derive it:

> "I assume that **[target user]** has a problem with **[pain point]**. They will use
> **[our solution]** to **[key action]** because it is **[specific advantage]** than their
> current way of doing things."

Reference the demand classification from demand assessment records — do not reclassify. If the
input is ambiguous, confirm the assumption with the user before continuing. A fuzzy assumption
produces a fuzzy MVP.

### Step 2: Resolve the three axes

Before any feature triage, locate the MVP in scope space. Read `references/axes.md` for the
selection tables and coherence checks.

1. **Scenario** — read the primary scenario and its five properties from
   proposed capability and journey records. Name the binding constraint (the property that rules out the most
   options). Reuse established scenario properties. If a necessary property is unknown, resolve that question from supplied context or with the user; route to `shape-solution` only when solution shaping is needed.
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

### Step 4: Build the Not-To-Do list

- **Not now (P1/P2)** — worth building if the assumption holds. Assign a trigger
  ("after 10 paying users").
- **Not ever (for this MVP)** — polish, scaling infra, secondary personas, and automation a
  manual process can stand in for.

Then present the full triage — P0 with rationale, Not-now with triggers, Not-ever — and ask
the user to challenge it before it is recorded: which cut would they reverse, which P0 would
they drop? A triage the user has not pushed on is unconfirmed, not agreed.

### Step 5: Review the ambition

Scope can be complete and still be the wrong bet. Challenge it before committing.

Map the trajectory:

```text
CURRENT USER EXPERIENCE → PROPOSED MVP → 12-MONTH IDEAL
```

Read an existing candidate or confirmed `vision` record in `overview` as the 12-month ideal
when one exists — reference it, do not reclassify or confirm it. When none exists, persist the
ideal this step constructs as a candidate `vision` record (inferred, linked to the claims and
scope that imply it) instead of leaving it as ephemeral prose; the Vision Synthesis rules in
`references/need-layers.md` govern what it may rest on.

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

## Output: enrich shared scope

Before persisting, run the close from `references/shared-understanding.md`: read back the
core assumption, the scenario × form × data point, and the P0 list, and ask the user to
confirm or correct the reading. Disagreements the conversation cannot settle become open
questions with revisit triggers, not silent concessions.

Write HTML records in `discovery.html`:

- Link the core validation assumption to the existing problem and demand assessment; do not copy or regrade demand.
- Record the scenario × form × data resolution and binding constraint as a scope decision linked to the primary scenario.
- Link P0/P1/P2 and Not-To-Do decisions to capability IDs, including rationale and revisit triggers. Keep current implementation status separate from priority and commitment.
- Record the ambition review and accepted/rejected/deferred alternatives with the user's decision basis. Proposed changes remain proposed until authorized.
- Persist the ambition review's 12-month ideal as a candidate `vision` record when no vision record exists (see Step 5); link it, never confirm it.
- Add validation-sprint actions and success metrics linked to the assumption they test, with thresholds when established.
- Enrich existing questions, assumptions, risks, and gaps rather than appending another "Open Questions / Risks" copy. Selecting a remedy does not close the original gap.

Preserve capability descriptions, unrelated scope, and accepted constraints. Update `state.md` with the records changed and unresolved blockers.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## Key Principles

- An MVP is not a cheap product. It is **the cheapest way to buy an answer**.
- Scope is a point in three-dimensional space, not a feature list. Resolve the axes first.
- A Wizard of Oz manual process beats an automated system for validating desire.
- A user who tolerates a buggy, ugly version to solve a real problem is stronger signal than
  1,000 sign-ups.
- "I'd use it if it had X, Y, Z" is polite rejection, not validation.
- A P0 that depends on data you cannot obtain is a wish, not a scope.

## What This Skill Does NOT Do

- **Does not validate demand** — it scopes a solution for demand already judged real
- **Does not design the solution** — it triages features against stories already written
- **Does not scope existing-product increments** — `scope-product-increment` owns behavior deltas against current product behavior
- **Does not write the PRD** — it produces the scope, not the consolidated spec
- **Does not stress-test the plan** — it defines the scope, not the failure modes

## Source adaptation

Triage framework and validation sprint adapted from the MVP-design material in the
skills-manager `Product & Strategy` setup. Ambition review adapted from gstack
`plan-ceo-review`, keeping its premise challenge, dream-state mapping, scope postures, and
explicit opt-in decisions while dropping its engineering mega-review and runtime dependencies.
The three-axis model is original to this system.
