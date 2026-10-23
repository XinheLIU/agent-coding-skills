---
name: acs-design-contracts
description: Use when interfaces lack invariants, failure semantics, trust boundaries, ordering guarantees, or evolution rules.
---

# Design Contracts

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [design.module_contracts]
  retrieves: [change.requirements, design.selected_architecture, system.terminology, system.current_state, verification.failure_history]
  produces: [design.contracts, design.failure_modes, system.invariants]
  updates: [design.accepted_decisions]
  invalidates: [verification.contract_coverage, design.unsupported_assumptions]
  handoff_to: [design_test_strategy, trace_requirements, implementation, refactoring]
```

[Shared semantics](../../../../docs/shared-semantics.md#technical-design)

Follow [the card contract](../references/card-contract.md): read ARC and MOD, write only `## Contracts & Correctness (CON)` and `FND-CON-*` rows. Views follow [the technical view template](../references/technical-view.md) and [the visual report contract](references/visual-report.md); run the contract's validator and fix every error before handover.

**Owns:** what must always be true, what each interface promises and requires, and what happens when something fails. **Does not own:** interface shape (MOD), how contracts are tested (TST), code-level violations (`acs-review-code-quality`).

## Current (brownfield)

Recover contracts the code already enforces, or silently relies on, before designing new ones: validation at entry points, database constraints, assertions, type guards, lock and transaction scopes, retry wrappers, error mappings. An invariant the code relies on but never checks is a finding. Domain invariants already recorded in `CONTEXT.md` by `acs-engineer-domain-model` are consumed, not redefined.

## Target

**Invariants.** `CON-n` rows of kind `invariant`: a statement that holds between operations, the module that owns it, where it is enforced (type, constraint, check, or transaction), and what breaks if violated.

```markdown
| ID | Kind | Statement | Owner | Enforced at | Violation effect |
| --- | --- | --- | --- | --- | --- |
| CON-1 | invariant | An order's total equals the sum of its line items | MOD-2 | db trigger + Order.recalc() | overcharge |
| CON-2 | operation | reserve(sku, qty): pre qty>0 ∧ sku exists; post stock' = stock−qty; err OutOfStock (no change) | MOD-3 | InventoryService | — |
```

**Operation contracts.** For each public MOD interface on the feature path: preconditions, postconditions, errors (which, when, and the state left behind), idempotency, and ordering or concurrency assumptions. Name who validates each precondition: the caller or the callee, never both, never neither.

**Error semantics.** One error model per boundary: which errors are domain outcomes returned to callers, which are faults that propagate, how they map across layers (domain → HTTP/CLI/UI), and what is retried. Partial writes must be impossible, compensated, or explicitly visible.

**Trust boundaries.** Where input stops being trusted, where authorization is decided, and which data crosses which boundary. Take the boundaries from ARC; this card makes them checkable.

**Evolution.** For public APIs, events, and schemas: compatibility rule (additive only, versioned, or breaking with migration), deprecation path, and who is affected.

**Failure modes.** For every new or changed code path, name one realistic production failure: timeout, null/missing, race, stale cache, partial write, duplicate delivery.

```markdown
| Path | Failure | Handled? | Tested? | Visible? |
| --- | --- | --- | --- | --- |
| checkout → reserve | inventory timeout | retry ×2 then 503 | planned TST-4 | alert |
```

A row that is unhandled, untested, and silent is a `P0` finding.

### Observability

Before naming signals or instrumenting a new or changed production path, write **2–4 on-call questions** in CON: what users experience, where failure occurs, and why. Then map every proposed signal to a question ID and a concrete query; cover every question. Choose structured logs, metrics, or traces for the answer needed, not a mandatory inventory of all three. Tie the map to the path's failure-mode row. Use correlation IDs across boundaries, allowlisted fields without secrets or personal data, and bounded metric labels.

For **every alert**, record its user-visible symptom, threshold and duration with rationale, destination, and a linked **three-line runbook**: `Means:` (impact), `First query:` (executable telemetry query), `Escalate to:` (owner). Require one test-fire per alert with evidence of receipt at the declared test destination and successful runbook resolution. A configured rule alone is not evidence.

Hand these CON IDs to `acs-design-test-strategy` to define verification, then implementation to execute it: declare the command and local mock/scratch environment before running; unset commands or environments block execution. Induce one named failure and retain telemetry, the queries used, and the diagnosis. The diagnostic pass must locate the affected path and cause **from telemetry alone**, without source, injection controls, or an answer key. Missing or ambiguous telemetry fails the exercise. Bind results to the tested source revision and configuration; relevant changes invalidate them. Preserve existing authorization; any external notification or environment needs authorization covering that action.

Keep planned checks distinct from executed evidence. Missing test-fire or failure-exercise evidence remains an open CON item routed to TST/implementation; do not claim operational readiness from a design or a mock. A local exercise establishes only its stated environment.

**Assumptions.** Every implicit assumption in the design or a supplied plan ("X is never null", "events arrive in order") becomes either a stated precondition or a finding.

## Review mode

Flag as `FND-CON-n`: invariants with no enforcement point, preconditions validated nowhere or twice, errors that leave undefined state, non-idempotent operations behind retries, breaking schema changes without migration, silent failure paths, unmapped signals or uncovered on-call questions, alerts without runbooks or test-fire evidence, undiagnosable induced failures, and unstated assumptions.

## Done when

Every interface on the feature path has pre/post/error semantics, every invariant names where it is enforced, and every new path has a failure-mode row. The observability design includes 2–4 questions before signals, a complete signal map, and a three-line runbook per alert; unexecuted checks remain explicit open items. Hand every `CON-n` to `acs-design-test-strategy`, which gives each one a verification method.
