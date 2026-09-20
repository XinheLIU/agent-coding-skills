---
name: acs-diagnose-incident
description: Diagnose hard bugs and performance regressions through a red-capable feedback loop, evidence log, and regression test. Use when behavior is broken, intermittent, slow, or resistant to an obvious fix.
---

# Diagnose Incident

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [change.symptom]
  retrieves: [change.requirements, system.affected_source, verification.failure_history, operations.environment]
  produces: [change.diagnosis, change.regression_evidence]
  updates: [run.investigation]
  invalidates: [verification.for_changed_code, system.disproved_assumptions]
  handoff_to: [implementation, testing]
```

Shared semantics: [shared protocol](../../craft/context/acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Read shared memory, relevant domain context, and ADRs. Create or update the active effort’s `diagnosis.md`.

## 1. Build the loop

Produce one agent-runnable command that has already gone red on the user’s exact symptom. Prefer a failing test, then a request/CLI/browser replay, captured trace, throwaway harness, property loop, bisection, or differential check. Tighten it until deterministic and fast. If no red-capable loop is possible, record attempts and request the missing artifact or access.

## 2. Reproduce and minimize

Confirm the right symptom, then remove inputs and steps one at a time until every remaining element is load-bearing.

## 3. Test hypotheses

Write three to five ranked, falsifiable hypotheses and the prediction for each. Change one variable per probe. Record evidence, not narrative guesses. For performance, measure and profile before changing code.

## 4. Fix

Turn the minimized reproduction into a failing regression test at the correct public seam. Apply the smallest fix, rerun the regression, original loop, and project checks.

## 5. Close

Remove temporary instrumentation, record the confirmed cause and verification, return routing updates to the coordinator, and route architectural seam failures to `acs-audit-architecture`. Do not commit unless asked.
