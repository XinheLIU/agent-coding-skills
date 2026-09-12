---
name: define-outcomes
description: Turn a chosen solution into verifiable product commitments — for new products, existing-product increments, and ambitious redesigns alike. Use when defining what success looks like, specifying observable acceptance criteria, deciding which capabilities are committed, reduced, deferred, or excluded, prioritizing or cutting scope, or producing the outcome contracts design and engineering build against.
disable-model-invocation: true
---

# Define Outcomes

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [product.solution_proposal]
  retrieves: [product.demand_assessment, product.current_behavior, product.constraints]
  produces: [product.outcome_contracts, product.verification_scenarios, product.scope_decisions]
  updates: [product.discovery_records]
  invalidates: [design.scope_dependents, verification.criteria]
  handoff_to: [product, design]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Turn a chosen solution shape into the verifiable commitments the team can build and measure against. The output says what success looks like for each accepted user outcome, how to prove it end-to-end, which capabilities it depends on, and which capabilities are deferred with their rationale.

This skill works the same way for new products and existing-product work. For existing-product changes, outcomes are expressed as ADDED / MODIFIED / REMOVED behavior against the source-backed current baseline.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read current capabilities and their evidence, proposed solution capabilities and journeys, demand assessments, accepted constraints, and existing scope decisions. Enrich capability records with outcome IDs, verification scenarios, and acceptance criteria.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Boundary

Define intended behavior, how deep each capability goes, and what would prove it works. Do not review architecture, specify implementation, or write tasks.

Scope holds two decisions and this skill owns one of them. *Whether and how deep* a capability is committed changes what the user can do — that is a product commitment, decided here. *When* committed capabilities ship is delivery sequencing, decided downstream. Downstream planning may reorder and split committed work freely; it returns to product whenever a proposed change would drop a committed capability, lower a recorded depth, or invalidate an end-to-end verification.

For existing products, require source-backed evidence of the affected current behavior before defining a delta. Reuse supplied or shared baseline evidence; route missing behavior inspection to `map-current-product`.

When improvement value is disputed, preserve the unresolved question and route to `validate-demand` before treating the change as validated.

## Workflow

### 1. Name each user outcome

For each outcome in the chosen solution, write:

```
[actor] can [action] so that [benefit]
```

Check each outcome against the deep need and any vision record — an outcome that serves the surface ask but not the underlying motivation is precise and wrong.

For existing-product work, state which current behavior the outcome extends, replaces, or removes. A removed behavior that existing users depend on needs a defined transition.

### 2. Define observable success states

For each outcome, state:

- The observable result the user gets
- The system state that must exist
- The quality bar: performance threshold, error rate, or accessibility level where relevant

Success is a state the user or a tester can observe. "The notification is displayed" is not a success state. "The user knows whether their export succeeded or failed without re-running it" is.

### 3. Write end-to-end verification scenarios

Verification works at two levels:

```
User outcome
    +-- End-to-end verification story
            +-- Capability A acceptance
            +-- Capability B acceptance
```

Capability acceptance establishes local behavior. The end-to-end story establishes that the user can complete the job. Capability tests passing does not guarantee the end-to-end story passes.

For each outcome, write the end-to-end story: the full journey from trigger to verified result, including what the user does with the result, how they recover from failure, and what state persists across sessions.

### 4. Set commitment and depth for each capability

For each outcome, list the capabilities it depends on, and for existing products the current behavior that must be preserved. A capability appearing in multiple outcomes is a dependency that warrants explicit coordination.

Then decide two independent things per capability: whether it is part of this commitment, and how deep it goes. A single priority ladder (P0/P1/P2) collapses the two and cannot express the most common real answer — *ship it, but narrower*.

**Commitment** — is this capability part of what we are promising?

| Level | Meaning | Must record |
| --- | --- | --- |
| `committed` | An outcome's verification fails without it | The verification scenario that needs it |
| `reduced` | Committed, at a named lower depth | What the user cannot do at that depth, and the trigger to reach `full` |
| `deferred` | Accepted intent, not in this commitment | Why it matters, and the decision that brings it forward |
| `excluded` | Decided against for this product | The constraint or evidenced non-need behind it |
| `open` | Unresolved and blocking | A linked question record and the observation that would settle it |

**Depth** — for `committed` and `reduced` only:

| Depth | Meaning |
| --- | --- |
| `full` | The capability as shaped in the target experience |
| `narrowed` | Full behavior over a restricted set of inputs, cases, or actors |
| `fixed` | Behavior whose tunable policy is frozen to one choice |
| `manual` | The user-visible outcome produced by a human behind the interface |

To place a capability, run it through three questions in order:

1. **Does the product still deliver the outcome without it?** No → `committed`. Yes → continue.
2. **Does any verification scenario exercise it?** No → `deferred` or `excluded`. Yes → continue.
3. **Does the outcome need it at full depth, or does a narrower version still pass verification?** Narrower → `reduced`, and name the depth.

**Excluded is not a schedule.** An `excluded` capability must cite a constraint or an evidenced non-need. If the honest reason is capacity — no time, no people, not this quarter — it is `deferred`, not `excluded`. Recording a deferral as an exclusion loses the intent permanently.

| Capability | Commitment | Depth | Basis |
| --- | --- | --- | --- |
| Private document retrieval | `reduced` | `narrowed` `fixed` | TXT only, fixed-size chunking; cannot ingest PDF or tune chunk size. Trigger for `full`: a team blocked by TXT-only |
| Role-based permissions | `excluded` | — | Constraint: one internal team, access managed offline |

Then apply the guard rails:

- Every `committed` and `reduced` capability is exercised by at least one end-to-end verification scenario. One that no scenario touches is not committed — it is `deferred`.
- Every `reduced` capability names the lost user capability. An unnamed reduction is a silent quality cut that resurfaces later as a bug report.
- The commitment set fits one sentence: *"[actor] can [core action] using [committed capabilities at their depths]."* If the sentence needs an "and also," the set is too broad — recheck which capabilities the outcome genuinely fails without.

Present the commitment table and ask the user to challenge it before recording: which exclusion would they reverse, which `committed` capability would they reduce? A triage the user has not pushed on is unconfirmed, not agreed.

For existing products, also state what the increment explicitly does not change, so downstream specs cannot silently expand scope.

### 5. For existing-product changes: write the behavior delta

Use change language against the source-backed current behavior:

| Type | Meaning |
| --- | --- |
| ADDED | New user-visible behavior that does not exist today |
| MODIFIED | Existing behavior whose outcome, rule, copy, permission, or flow changes |
| REMOVED | Existing behavior that will no longer happen |

Each row must cite the baseline evidence from current capability records. For REMOVED behavior, also define the transition: what happens to existing data, ongoing work, saved state, and prior expectations.

Present the delta and ask the user to confirm before writing acceptance criteria. A wrong MODIFIED row corrected here is cheap; corrected after acceptance criteria are written, it invalidates them.

### 6. Name the metric that would prove each outcome

Pick one or two metrics per outcome that move only if the outcome actually landed, and name the vanity signal each one replaces so the substitution is deliberate.

| Vanity signal | Why it lies | Use instead |
| --- | --- | --- |
| Sign-ups, installs | Measures interest, not the outcome | Users who complete the outcome's key action |
| Page views, sessions | No intent signal | Repeat completions of the same action |
| "I'd use this if…" | Polite rejection | Repeat use of an incomplete version |

A metric that still rises when the outcome fails is not a metric for this outcome. Persist these as `metric` records linked to the outcome.

## Outcome contract format

Write each outcome as a five-section record:

```markdown
## [Outcome ID] Title

**User story:** [actor] can [action] so that [benefit]

**Success state:**
- Observable result the user gets
- System state that must exist
- Quality bar (performance, error rate, accessibility level)

**Verification:**
The end-to-end scenario that exercises the full journey and would fail if something is missing.

**Capabilities:**

| Capability | Commitment | Depth | Basis |
| --- | --- | --- | --- |
| Name | committed / reduced / deferred / excluded / open | full / narrowed / fixed / manual | Verification link, lost capability, constraint, or re-entry trigger |

Preserved behavior (for existing products) listed alongside. Delivery may reorder and split `committed` rows without product approval; changing a commitment level or a depth requires returning here.

**Metric:** the signal that moves only if this outcome landed, and the vanity signal it replaces.
```

Choose coverage based on the promise and risk: relevant cases include permissions, empty or stale states, repeated actions, dependency failures, boundary inputs, and cross-role handoffs. Do not require every possible case mechanically.

## Output: enrich the product model

Write HTML records in `discovery.html`.

- Outcome records: user story, success state, verification scenario, capability links, and metric per outcome.
- Capability records carry `data-commitment` and `data-depth` alongside `data-kind="capability"`, the way roadmap tickets carry `data-ticket-type`. The basis — verification link, lost capability, constraint, or re-entry trigger — goes in the record body, never in the attribute.
- For existing-product work: ADDED / MODIFIED / REMOVED delta with source evidence; transition behavior for REMOVED entries.
- Deferred and excluded capabilities stay capability records at their commitment level, not separate tickets. A `deferred` record keeps its rationale and re-entry trigger; an `excluded` record keeps the constraint it rests on.
- Scope boundary: the `excluded` set read as one list, explicit enough that downstream specs cannot silently expand.
- Enrich existing question, assumption, risk, and gap records rather than appending new "Open Questions" sections. A selected outcome does not close the original demand gap.

Do not create a second capability inventory or overwrite unrelated decisions. Preserve unanswered questions with their blocking effect and next resolver. Return routing updates to the coordinator with changed anchors.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## Quality bar

- Each outcome has an observable success state, not just a feature description.
- The end-to-end verification story would fail if any capability were missing.
- Every capability carries a commitment level; every `committed` and `reduced` one is exercised by a verification scenario.
- Every `reduced` capability names what the user cannot do at that depth and the trigger to reach `full`.
- Every `excluded` capability cites a constraint or evidenced non-need — never capacity, which is a `deferred`.
- The commitment set passes the one-sentence test without an "and also".
- ADDED / MODIFIED / REMOVED rows (for existing products) cite source evidence.
- Excluded and deferred items are explicit enough for `write-prd` and `spec` to preserve.

## What This Skill Does NOT Do

- **Does not validate demand** — it defines outcomes for a solution already judged worth building
- **Does not shape the solution** — `shape-solution` produces the target experience; this skill commits it
- **Does not locate the solution in scope space** — `shape-solution` resolves scenario, product form, and data availability before capabilities can be judged
- **Does not define delivery sequencing** — build order and release proposals belong downstream; this skill fixes what is committed and how deep, not when it ships
- **Does not write the PRD** — it produces outcome contracts; `write-prd` consolidates them
- **Does not run experiments** — use `design-experiment` to resolve specific uncertainties cheaply
