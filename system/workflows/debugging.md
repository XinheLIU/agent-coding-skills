# Debugging Workflow

Last updated: 2026-09-09

```text
reported symptom
  → diagnosing-bugs builds a red-capable command
  → minimize reproduction
  → rank and test hypotheses
  → add regression test at the correct seam
  → apply minimal fix
  → rerun original reproduction and project checks
  → improve-codebase-architecture when no stable seam exists
```

The active effort’s `diagnosis.md` stores the symptom, reproduction command, evidence, confirmed cause, and verification. Temporary instrumentation is removed before closeout.

Link the diagnosis and regression evidence to the canonical change/task and affected criterion or preservation invariant. Raw experiments remain Run Context; retain cause, fix revision/diff, environment, final check results, failures and omissions in Change Context before cleanup. The [coordinator](context-coordination.md) applies status and freshness transitions.
