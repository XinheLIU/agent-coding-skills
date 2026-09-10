---
name: codebase-design
description: Apply shared deep-module vocabulary to interfaces and test seams. Use when designing or improving a module, deciding where behavior belongs, or making code more testable and agent-navigable.
---

# Codebase Design

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [design.question, system.affected_source]
  retrieves: [change.requirements, system.invariants]
  produces: [design.module_contracts]
  updates: [design.accepted_decisions]
  invalidates: [implementation.affected_plan, verification.contract_coverage]
  handoff_to: [implementation, testing]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Use these terms consistently:

- **Module**: anything with an interface and implementation.
- **Interface**: every fact a caller must know, including invariants and failures.
- **Seam**: a place where behavior can vary without editing the caller.
- **Adapter**: a concrete implementation at a seam.
- **Depth**: behavior exposed per unit of interface.
- **Leverage**: capability gained by callers.
- **Locality**: change and verification concentrated in one place.

Prefer a small interface hiding substantial behavior. Apply the deletion test: deleting a useful module redistributes complexity across callers; deleting a pass-through removes complexity. Treat the interface as the public test surface. Introduce a seam when real variation exists, not for hypothetical flexibility.

This skill owns module-design reasoning. Retain accepted contracts and consequential decisions as separately addressable Change Context linked to the canonical change/spec/criteria and consumed revisions; the run plan links them. Record warranted ADRs and update applicable System State when boundaries change. `tasks` and `tdd` consume these references; do not keep accepted design only in the disposable plan.
