---
name: scope-product-increment
description: Scope a user-visible improvement to an existing product. Use when the user asks to improve, iterate, refine, modify, or extend an existing app/product/feature; convert current-product gaps into a next increment; or define ADDED/MODIFIED/REMOVED behavior, acceptance criteria, edge cases, instrumentation, and success metrics for active-product work.
disable-model-invocation: true
---

> **Deprecated — use `define-outcomes` instead.** This skill is replaced by `define-outcomes`, which handles both new and existing-product work with a common outcome-contract model. Old invocations route here for one release; then this file is removed.

# Scope Product Increment

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [product.current_behavior, product.change_request]
  retrieves: [product.relevant_context, design.feasibility]
  produces: [product.behavior_delta, product.criteria_proposal]
  updates: [product.discovery_records]
  invalidates: [design.scope_dependents, verification.criteria]
  handoff_to: [product, design]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Turn an existing-product improvement into a behavior delta the team can build and measure. The output says what changes for users, what stays out of scope, how done will be tested, and what evidence will prove the increment worked.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read current capabilities and their evidence/coverage, accepted product intent, demand assessments, proposed solutions, and existing scope. Enrich the affected records with an explicit delta and linked scope decisions.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Boundary

Scope user-visible behavior. Do not review architecture, refactor internals, or write implementation tasks. If the request has no user outcome, route to `design/technical/codebase-design`, `design/technical/improve-codebase-architecture`, or `engineering/feature/spec` as appropriate.

`scope-mvp` owns greenfield first-slice scoping. This skill owns active-product increments.

Before defining a delta, require evidence of the affected current behavior. Reuse supplied or shared baseline evidence; if it is missing, route the relevant inspection to `map-current-product`. When improvement value is disputed, preserve that question and route to `validate-demand` before claiming the change is validated. Baseline module need-fit verdicts and vision-resilience notes from `map-current-product` are direct input: an under-serving module is a candidate for MODIFIED behavior; a serves-no-real-need module is a candidate for REMOVED.

## Workflow

### 1. Name the target outcome

State the existing behavior, the user pain or opportunity, and the target outcome in one sentence:

```text
For [user/role], improve [current behavior] so [target outcome], measured by [signal].
```

Check the target outcome against the problem's deep need and any vision record, not only the surface ask — an increment that serves the ask but not the motivation is precise and wrong. Layers: `references/need-layers.md`.

Use active-product evidence when available: support tickets, analytics, usage funnels, churn/lost-deal notes, stakeholder reports, sales/support transcripts, customer interviews, or observed sessions. Mark unsupported assumptions explicitly.

### 2. Choose the scope posture

Default to **Selective expansion** for existing-product work: hold the requested improvement as baseline, then surface optional adjacent improvements for explicit user approval.

| Posture | Use when | Output |
| --- | --- | --- |
| Hold | The requested improvement is already the right boundary | Harden acceptance, edges, and measurement |
| Reduce | The request is too broad for one coherent increment | Propose the smallest user-value slice |
| Selective expansion | A few nearby improvements may compound value | List candidates; include only approved ones |
| Expand | The stated request misses the larger product opportunity | Present the ambitious version, then ask before adding scope |

Never silently add or remove scope. Put rejected or deferred candidates in Out of Scope.

### 3. Write the behavior delta

Use OpenSpec-style change language against current behavior:

| Type | Meaning |
| --- | --- |
| ADDED | New user-visible behavior that does not exist today |
| MODIFIED | Existing behavior whose outcome, rule, copy, permission, or flow changes |
| REMOVED | Existing user-visible behavior that will no longer happen |

Each row must cite the baseline evidence from current capability records or the PRD.

Then present the delta table with its baseline evidence and ask the user to confirm or
correct each row before writing acceptance criteria
(`references/shared-understanding.md`). A wrong MODIFIED row corrected here is cheap;
corrected after acceptance criteria and instrumentation are written, it invalidates both.

### 4. Triage P0/P1/out-of-scope

P0 is the smallest coherent set of behavior needed to deliver and test the target outcome. P1 is useful after the increment works. Out of scope is explicit so downstream specs do not smuggle it back in.

### 5. Define acceptance and edge coverage

For each P0 behavior, write Given/When/Then criteria that a tester can pass or fail. Cover the happy path first, then failure, recovery, permission, empty state, stale state, double action, dependency failure, and boundary inputs when relevant.

### 6. Define instrumentation and success metrics

Start from analytics questions, then define events. Include event name, trigger, properties, privacy/PII handling, and QA verification. Pick one or two success metrics that prove the target outcome, plus any guardrail metric that catches harm.

### 7. Record refinement notes

Capture decisions, open questions, blocked stories, and follow-up owners. If an answer changes scope, revise the delta before writing the artifact.

## Output: enrich the existing product

Write HTML records in `discovery.html`; link to durable records where the subject already has a canonical home.

- Target outcome: actor, affected current behavior, desired outcome, the need layer the outcome serves, evidence, assumptions, and success signal.
- Scope decision: posture and authorized accepted/rejected/deferred alternatives; P0/P1/out-of-scope links with rationale and revisit conditions.
- Behavior delta: ADDED / MODIFIED / REMOVED against named capability IDs and source evidence, with proposed new behavior separate from current observation.
- Acceptance: Given/When/Then criteria for each P0 behavior, including relevant failure, recovery, permission, empty/stale state, repeated action, dependency, and boundary cases.
- Measurement: analytics questions, event trigger/properties/privacy/QA, success thresholds, and guardrails linked to the outcomes they test.
- Refinement: enrich shared decisions, questions, assumptions, risks, and blockers. Link a remedy to its gap; leave the gap open until implementation is evidenced.

Do not create a second capability inventory or overwrite unrelated decisions. Preserve unanswered questions with their blocking effect and next resolver. Return routing updates to the coordinator with changed anchors.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## Quality Bar

- The delta uses ADDED / MODIFIED / REMOVED against named current behavior.
- P0 is coherent and small enough to build as one increment.
- Acceptance criteria are observable Given/When/Then statements.
- Edge cases include recovery paths, not just failure labels.
- Instrumentation answers specific analytics questions and flags privacy handling.
- Out-of-scope items are explicit enough for `write-prd` and `spec` to preserve.

## Source Adaptation

Borrowed principles: PM-Skills `deliver-acceptance-criteria`, `deliver-edge-cases`, `measure-instrumentation-spec`, and `iterate-refinement-notes`; OpenSpec brownfield delta language; gstack `plan-ceo-review` scope postures and explicit opt-in for scope changes.
