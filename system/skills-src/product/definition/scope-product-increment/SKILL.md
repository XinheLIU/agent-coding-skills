---
name: scope-product-increment
description: Scope a user-visible improvement to an existing product. Use when the user asks to improve, iterate, refine, modify, or extend an existing app/product/feature; convert current-product gaps into a next increment; or define ADDED/MODIFIED/REMOVED behavior, acceptance criteria, edge cases, instrumentation, and success metrics for active-product work.
---

# Scope Product Increment

Last updated: 2026-08-18

Turn an existing-product improvement into a behavior delta the team can build and measure. The output says what changes for users, what stays out of scope, how done will be tested, and what evidence will prove the increment worked.

## Shared Memory Contract

```text
Layer:    working — the behavior delta for this product increment
Owns:     <work-root>/<effort>/discovery/increment.md
Promotes: behavior delta, acceptance criteria, edge cases, instrumentation, metrics, out-of-scope → PRD via write-prd
```

Read `docs/agents/memory.md`, the active `state.md`, `<product-docs>/<slug>/prd.md` when present, and upstream artifacts in this order: `discovery/current-product.md`, `discovery/demand.md`, `discovery/solution.md`, then `discovery/mvp.md` if it exists.

If `current-product.md` is missing and the request references an existing codebase or app, run or route to `map-current-product` first. A delta without a baseline is guesswork.

## Boundary

Scope user-visible behavior. Do not review architecture, refactor internals, or write implementation tasks. If the request has no user outcome, route to `design/technical/codebase-design`, `design/technical/improve-codebase-architecture`, or `engineering/feature/spec` as appropriate.

`scope-mvp` owns greenfield first-slice scoping. This skill owns active-product increments.

## Workflow

### 1. Name the target outcome

State the existing behavior, the user pain or opportunity, and the target outcome in one sentence:

```text
For [user/role], improve [current behavior] so [target outcome], measured by [signal].
```

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

Each row must cite the baseline evidence from `current-product.md` or the PRD.

### 4. Triage P0/P1/out-of-scope

P0 is the smallest coherent set of behavior needed to deliver and test the target outcome. P1 is useful after the increment works. Out of scope is explicit so downstream specs do not smuggle it back in.

### 5. Define acceptance and edge coverage

For each P0 behavior, write Given/When/Then criteria that a tester can pass or fail. Cover the happy path first, then failure, recovery, permission, empty state, stale state, double action, dependency failure, and boundary inputs when relevant.

### 6. Define instrumentation and success metrics

Start from analytics questions, then define events. Include event name, trigger, properties, privacy/PII handling, and QA verification. Pick one or two success metrics that prove the target outcome, plus any guardrail metric that catches harm.

### 7. Record refinement notes

Capture decisions, open questions, blocked stories, and follow-up owners. If an answer changes scope, revise the delta before writing the artifact.

## Output Format

Persist to `<work-root>/<effort>/discovery/increment.md`:

```markdown
# Product Increment Scope: [Increment Name]

Last updated: [YYYY-MM-DD]

## Target Outcome
For [user/role], improve [current behavior] so [target outcome], measured by [signal].

Evidence: [support ticket / analytics / stakeholder / code / PRD references]
Assumptions: [explicit unsupported claims]

## Scope Posture
Posture: [Hold / Reduce / Selective expansion / Expand]
Decision: [what was accepted, rejected, or deferred]

## Behavior Delta
| Type | Behavior | Current evidence | New expected behavior |
| --- | --- | --- | --- |
| ADDED / MODIFIED / REMOVED | ... | ... | ... |

## P0
| Behavior | Why it is P0 | Acceptance coverage |
| --- | --- | --- |

## P1
| Behavior | Trigger to revisit |
| --- | --- |

## Out of Scope
- [Explicit exclusion and reason]

## Acceptance Criteria
### [P0 behavior]
- GIVEN [state], WHEN [action], THEN [observable result].

## Edge Cases and Recovery
| Scenario | Expected handling | Priority |
| --- | --- | --- |

## Instrumentation
Analytics questions:
- [Question this increment must answer]

| Event | Trigger | Properties | Privacy/PII | QA check |
| --- | --- | --- | --- | --- |

## Success Metrics
| Metric | Threshold | Proves | Guardrail? |
| --- | --- | --- | --- |

## Refinement Notes
### Decisions
- ...

### Open Questions
- ...

### Blockers
- ...
```

## Quality Bar

- The delta uses ADDED / MODIFIED / REMOVED against named current behavior.
- P0 is coherent and small enough to build as one increment.
- Acceptance criteria are observable Given/When/Then statements.
- Edge cases include recovery paths, not just failure labels.
- Instrumentation answers specific analytics questions and flags privacy handling.
- Out-of-scope items are explicit enough for `write-prd` and `spec` to preserve.

## Source Adaptation

Borrowed principles: PM-Skills `deliver-acceptance-criteria`, `deliver-edge-cases`, `measure-instrumentation-spec`, and `iterate-refinement-notes`; OpenSpec brownfield delta language; gstack `plan-ceo-review` scope postures and explicit opt-in for scope changes.
