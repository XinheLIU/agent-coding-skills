# Debugging Workflow

Last updated: 2026-08-02

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
