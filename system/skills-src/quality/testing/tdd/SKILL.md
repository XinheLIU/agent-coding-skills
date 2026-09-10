---
name: tdd
description: Execute scoped implementation work through criterion-based red-green-refactor loops. Use for test-first feature work or behavior fixes. Return evidence and proposed transitions to the coordinator; reuse canonical tickets and the existing run plan.
---

# TDD Execution

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.task, verification.acceptance_criteria]
  retrieves: [design.contracts, system.affected_source, verification.failure_history, operations.environment]
  produces: [change.implementation_evidence, verification.test_evidence]
  updates: [source.implementation, source.tests]
  invalidates: [verification.for_changed_code]
  handoff_to: [testing, code_review, coordinator]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Every changed behavior gets a meaningful failing test before its implementation. Use the canonical task, criteria, accepted contracts, relevant failure history, code baseline, and environment supplied under [delivery](../../../../workflows/feature-delivery.md) and [engineering context](../../../craft/context/init-context/references/engineering-memory.md).

## Prepare the behavior slice

Read only the relevant requirement/criterion and contract sections, including active review findings and consumed revisions. Reuse the existing ticket and run plan; do not create a second progress document. Map the next behavior to a criterion and public seam. If expected behavior is unknown, return the precise question and blocking effect; continue independent work when possible.

Propose dependencies and shared-write risks to the coordinator. It owns scheduling, claims, context transport, and available runtime bindings. Executors may read accessible canonical references; only use bounded revision-labelled excerpts when needed. Without authorized delegation and safe claim coordination, execute serially.

## Red → green → refactor

1. Write one test naming the observable behavior and criterion. Avoid tests that only assert mock calls or duplicate implementation logic.
2. Run it and confirm it fails for the expected missing behavior. A typo, missing service, or unrelated failure is not valid red evidence. If it already passes, inspect whether behavior is already implemented or the assertion is ineffective; never fabricate failure.
3. Implement the smallest scoped change that passes. Preserve external contracts and accepted requirements.
4. Run the targeted check and relevant regressions. Record exact command, revision/diff identity, environment, result, and any omissions. Never skip or weaken a valid test to claim green.
5. Refactor only when useful, preserving behavior and keeping checks green. Boundary changes follow `refactor-code`'s Current State/ADR contract.
6. Repeat for the next behavior in the authorized slice.

On an unexpected failure, distinguish implementation, test, and environment causes from evidence. On conflicting edits or changed premises, return to the coordinator for reconciliation. Do not discard unrelated work to restart a loop.

## Review and handoff

Self-check criterion coverage, scope, assertion quality, and regressions before reporting. Propose `review-implementation-gaps` when implementation completeness needs checking and `review-code-quality` for the Standards and Spec axes; the coordinator selects relevant reviews. A checked execution step is not acceptance evidence.

Return the common handoff envelope with criterion → test/evidence → revision mapping, affected surfaces, accepted decision references, deviations, failures, skipped/not-run checks, environment assumptions, and next action. The coordinator retains compact final verification in Change Context and reconciles canonical ticket status. Raw output and scratch remain Run Context. No commit or release is implied.
