---
name: acs-tdd
description: Use when one implementation ticket has acceptance criteria and prerequisite evidence ready for execution.
---

# TDD Execution

Last updated: 2026-10-23

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

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.


Every changed behavior gets a meaningful failing test before its implementation. The dispatching [`acs-implement`](../acs-implement/SKILL.md) run acts as coordinator: it supplies the canonical ticket, criteria, accepted contracts, relevant failure history, code baseline, prerequisite evidence, and environment, and it owns scheduling, claims, and merges. Invoked standalone, the active agent plays that role under [delivery](../../resources/workflows/feature-delivery.md) and [engineering context](../../resources/protocols/engineering-memory.md).

## Prepare the behavior slice

Read only the relevant requirement/criterion and contract sections, including active review findings and consumed revisions. Reuse the existing ticket and run plan; do not create a second progress document. Map the next behavior to a criterion and public seam: the interface where callers observe behavior without reaching into internals. Write a test only at a seam named in an accepted TST, or confirmed by the user when no TST exists. If a TST exists but does not accept the seam, return to the coordinator to reconcile the TST before writing the test. If expected behavior is unknown, return the precise question and blocking effect; continue independent work when possible.

Propose dependencies and shared-write risks to the coordinator. It owns scheduling, claims, context transport, and available runtime bindings. Executors may read accessible canonical references; only use bounded revision-labelled excerpts when needed. Without authorized delegation and safe claim coordination, execute serially.

## Test anti-patterns

- **Implementation-coupled**: tests private methods, internal collaborator calls, or a side channel instead of behavior at the agreed public seam; an internal refactor breaks the test without changing behavior.
- **Tautological**: repeats the implementation's calculation in the assertion or compares a value with itself. Expected values come from an independent source of truth: an accepted specification, a worked example, or a known-good literal.
- **Horizontal slicing**: writes all tests before any implementation. Work one seam and one behavior at a time: one test → one minimal implementation → green, then the next slice.

## Red → green

1. Write one test naming the observable behavior and criterion at the agreed seam.
2. Run it and confirm it fails for the expected missing behavior. A typo, missing service, or unrelated failure is not valid red evidence. If it already passes, inspect whether behavior is already implemented or the assertion is ineffective; never fabricate failure.
3. Implement the smallest scoped change that passes. Preserve external contracts and accepted requirements.
4. Run the targeted check and relevant regressions. Follow the [evidence template](../acs-implement/references/evidence-template.md): preserve dispatch BASE; bind each row to its exact command, tested source revision/tree fingerprint, actual completion timestamp with timezone, environment and result. Confirm the tested source stayed unchanged during the command; rerun if it changed. Record omissions and keep earlier red runs at their original identities outside current acceptance rows. Never skip or weaken a valid test to claim green.
5. End this loop at green. Repeat for the next behavior in the authorized slice.

On an unexpected failure, distinguish implementation, test, and environment causes from evidence. On conflicting edits or changed premises, return to the coordinator for reconciliation. Do not discard unrelated work to restart a loop.

## Review and handoff

Self-check criterion coverage, scope, assertion quality, and regressions before reporting. Refactoring belongs to review, outside the red → green loop: propose `acs-refactor-code` when useful, preserving behavior and keeping checks green. Boundary changes follow its Current State/ADR contract. Propose `acs-trace-requirements` (post-build) when implementation completeness needs checking and `acs-review-code-quality` for the Standards and Spec axes; the coordinator selects relevant reviews. A checked execution step is not acceptance evidence.

Return the common handoff envelope with criterion → test/evidence → revision mapping, affected surfaces, accepted decision references, deviations, failures, skipped/not-run checks, environment assumptions, and next action. The coordinator retains compact final verification in Change Context and reconciles canonical ticket status. Raw output and scratch remain Run Context. No commit or release is implied.
