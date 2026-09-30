---
name: acs-design-contracts
description: Design or review correctness contracts — invariants, pre/postconditions, error and failure semantics, idempotency and ordering, trust boundaries, and API/schema evolution — plus a failure-modes table for every new code path. Use when interfaces exist but what must stay true, what can fail, and how it fails are unstated; writes the CON section of the shared technical-design.md.
---

# Design Contracts

Last updated: 2026-09-30

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

Shared semantics: [memory and handoff protocol](../../../../protocols/skill-declarations.md); shared execution: [Coordination](../../../../protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../../../protocols/presenter.md); views carry source revisions and never own domain facts.

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

**Assumptions.** Every implicit assumption in the design or a supplied plan ("X is never null", "events arrive in order") becomes either a stated precondition or a finding.

## Review mode

Flag as `FND-CON-n`: invariants with no enforcement point, preconditions validated nowhere or twice, errors that leave undefined state, non-idempotent operations behind retries, breaking schema changes without migration, silent failure paths, and unstated assumptions.

## Done when

Every interface on the feature path has pre/post/error semantics, every invariant names where it is enforced, and every new path has a failure-mode row. Hand every `CON-n` to `acs-design-test-strategy`, which gives each one a verification method.
