---
name: design-experiment
description: Design a bounded experiment to resolve a named, falsifiable uncertainty cheaply. Invoked explicitly — not as a default scoping step — when a specific assumption can be tested before committing to the full solution. The experiment scope never becomes the product scope.
disable-model-invocation: true
---

# Design Experiment

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [product.named_uncertainty]
  retrieves: [product.solution_proposal, product.demand_assessment]
  produces: [product.experiment_design, product.validation_evidence]
  updates: [product.discovery_records]
  invalidates: []
  handoff_to: [product]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Design the cheapest credible way to resolve a specific product uncertainty. The output is an experiment design — not a product definition. After the experiment runs, its evidence returns to `shape-solution` if it changes the target experience, or to `define-outcomes` if the solution holds but a commitment needs adjustment.

## Invocation contract

This skill requires explicit invocation with two inputs:

1. **The uncertainty**: a single falsifiable assumption — what specifically might be wrong, and what observation would settle it.
2. **Why resolving it cheaply matters**: what risk it removes before full commitment.

Without both, surface the gap and stop. Vague uncertainty does not produce a useful experiment.

## Boundary

Design one experiment to answer one question. Do not define the product, scope multiple assumptions at once, or minimize the product as a side effect. The product's target experience lives in `shape-solution`; commitments live in `define-outcomes`.

A disposable experiment is acceptable. The experiment's scope never automatically becomes the product's scope.

## Workflow

### 1. Clarify the uncertainty

Restate the assumption in falsifiable form:

```
I believe [target user] experiences [specific pain] strongly enough to [specific behavior].
This would be false if [observable counter-evidence].
```

If the counter-evidence cannot be stated, the assumption is not falsifiable — the experiment will not settle it. Name that gap before designing the test.

### 2. Design the cheapest credible test

The experiment must be:

- **Targeted**: answers only the stated uncertainty, nothing else
- **Credible**: the result would actually change the decision
- **Bounded**: has a stated scope, participant pool, and duration

Options to consider: a landing page with a sign-up, a manual walkthrough with five real users, a paper prototype, a concierge service, a Wizard of Oz backend. Match the test to what the assumption is actually about.

For each candidate, state: what it resolves, what it leaves open, and what makes it credible for this assumption.

### 3. Define the decision rule

State before running:

- **Success threshold**: the minimum signal that would support the assumption
- **Failure threshold**: the observation that would contradict it
- **Decision**: what happens if it passes, what happens if it fails

An experiment without a predetermined decision rule produces results the team will rationalize. Define the rule before the experiment runs.

### 4. Choose whether to use manual substitutes

Manual substitutes are valid when:

- A human performing the function manually can plausibly simulate the automated behavior for the users in this test
- The user's reaction genuinely informs the automated version
- The limitations of the manual version are explicit to the experimenter

Do not recommend manual substitutes merely because they are cheaper. The substitution must be credible for the specific uncertainty being tested.

### 5. Fix the rhythm

An experiment without an end date stops being an experiment and becomes the product. Bound it
before it starts. Four weeks is the default; shorter is better, longer needs a reason.

| Week | Focus | Output |
| --- | --- | --- |
| 1 | Scope | Assumption, decision rule, and what is deliberately not built |
| 2 | Build | The minimum carrier: landing page, prototype, script, or a human behind an interface |
| 3 | Observe | 5-10 real target users. Watch behavior; do not sell |
| 4 | Decide | Apply the decision rule from step 3 |

At the end, the rule resolves to exactly one of:

| Outcome | Condition | Next |
| --- | --- | --- |
| **Persevere** | The assumption held and users demonstrated the behavior | Return to `define-outcomes`; the evidence may raise a `deferred` capability or lift a `reduced` depth |
| **Pivot** | The assumption was wrong but the test surfaced a new one | Rewrite the assumption and re-enter at step 1 |
| **Stop** | No signal and no new assumption | Stop. The information was still worth buying |

Whichever it is, the experiment's own scope does not become the product's scope. A persevere returns
evidence, not a commitment table.

## Output: experiment design record

Produce:

- The falsifiable assumption
- The chosen test: scope, participants, duration, and what will be observed
- The decision rule: success threshold, failure threshold, and what each implies for next steps
- The end date, and which of persevere / pivot / stop the result produced
- Manual substitutes, if any, with their limitations stated

After the experiment runs, return to:

- `shape-solution` if the evidence changes the target experience
- `define-outcomes` if the solution holds but a commitment level or depth needs adjustment

Record the design and outcome in `discovery.html` as an experiment record linked to the uncertainty it addressed. A failed assumption with clear evidence is valuable product knowledge; preserve it regardless of direction.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table.
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## What This Skill Does NOT Do

- **Does not define the product** — the solution shape stays in `shape-solution`
- **Does not commit scope** — commitments belong in `define-outcomes`
- **Does not replace demand validation** — for general demand uncertainty, use `validate-demand`
- **Does not minimize the product to experiment size** — the target product and the experiment are separate
