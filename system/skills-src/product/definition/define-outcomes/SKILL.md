---
name: define-outcomes
description: Turn a chosen solution into verifiable product commitments — for new products, existing-product increments, and ambitious redesigns alike. Use when defining what success looks like, specifying observable acceptance criteria, capturing deferred intent, or producing the outcome contracts design and engineering build against.
disable-model-invocation: true
---

# Define Outcomes

Last updated: 2026-09-11

## Context contract

```yaml
context:
  requires: [product.solution_proposal]
  retrieves: [product.demand_assessment, product.current_behavior, product.constraints]
  produces: [product.outcome_contracts, product.verification_scenarios]
  updates: [product.discovery_records]
  invalidates: [design.scope_dependents, verification.criteria]
  handoff_to: [product, design]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Turn a chosen solution shape into the verifiable commitments the team can build and measure against. The output says what success looks like for each accepted user outcome, how to prove it end-to-end, which capabilities it depends on, and which capabilities are deferred with their rationale.

This skill works the same way for new products and existing-product work. For existing-product changes, outcomes are expressed as ADDED / MODIFIED / REMOVED behavior against the source-backed current baseline.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read current capabilities and their evidence, proposed solution capabilities and journeys, demand assessments, accepted constraints, and existing scope decisions. Enrich capability records with outcome IDs, verification scenarios, and acceptance criteria.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Boundary

Define intended behavior and what would prove it works. Do not review architecture, specify implementation, or write tasks. Do not silently schedule or cut scope — delivery sequencing belongs to downstream planning, with an explicit product return whenever a proposed cut would invalidate the core verification.

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

### 4. Identify capabilities and preserved behavior

For each outcome, list:

- The functions or changes it depends on
- For existing products: the current behavior that must be preserved

A capability appearing in multiple outcomes is a dependency that warrants explicit coordination.

### 5. State deferred intent

For each accepted but unscheduled capability, record:

- What the user would be able to do
- Why it matters (the linked need or journey)
- What decision would bring it forward

Do not collapse deferred capabilities into vague "P2, maybe later" entries. Intent, rationale, and link to the outcome must survive delivery sequencing.

For existing products, also state what the increment explicitly does not change, so downstream specs cannot silently expand scope.

### 6. For existing-product changes: write the behavior delta

Use change language against the source-backed current behavior:

| Type | Meaning |
| --- | --- |
| ADDED | New user-visible behavior that does not exist today |
| MODIFIED | Existing behavior whose outcome, rule, copy, permission, or flow changes |
| REMOVED | Existing behavior that will no longer happen |

Each row must cite the baseline evidence from current capability records. For REMOVED behavior, also define the transition: what happens to existing data, ongoing work, saved state, and prior expectations.

Present the delta and ask the user to confirm before writing acceptance criteria. A wrong MODIFIED row corrected here is cheap; corrected after acceptance criteria are written, it invalidates them.

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
- Functions and changes this outcome depends on
- Preserved behavior (for existing products)

**Future intent:**
Accepted but unscheduled capabilities, with rationale and links. Delivery can defer these without product approval as long as the core verification still passes.
```

Choose coverage based on the promise and risk: relevant cases include permissions, empty or stale states, repeated actions, dependency failures, boundary inputs, and cross-role handoffs. Do not require every possible case mechanically.

## Output: enrich the product model

Write HTML records in `discovery.html`.

- Outcome records: user story, success state, verification scenario, capability links, and future intent per outcome.
- For existing-product work: ADDED / MODIFIED / REMOVED delta with source evidence; transition behavior for REMOVED entries.
- Deferred intent: inline in the outcome record's future-intent section, not as separate tickets.
- Scope boundary: explicit out-of-scope items so downstream specs cannot silently expand.
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
- Deferred intent has rationale and a link to its outcome — not just a name.
- ADDED / MODIFIED / REMOVED rows (for existing products) cite source evidence.
- Out-of-scope items are explicit enough for `write-prd` and `spec` to preserve.

## What This Skill Does NOT Do

- **Does not validate demand** — it defines outcomes for a solution already judged worth building
- **Does not shape the solution** — `shape-solution` produces the target experience; this skill commits it
- **Does not define delivery sequencing** — build order and release proposals belong downstream
- **Does not write the PRD** — it produces outcome contracts; `write-prd` consolidates them
- **Does not run experiments** — use `design-experiment` to resolve specific uncertainties cheaply
