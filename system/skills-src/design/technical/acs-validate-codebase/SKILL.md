---
name: acs-validate-codebase
description: Validate technical design and implementation reachability across routes, menus, interfaces, exports, modules, dependencies, and agent instructions; apply scoped repairs and retain evidence.
---

# Validate Codebase

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [design.module_contracts]
  retrieves: [change.requirements, design.wiring_map, system.current_state, system.interface_rules, verification.latest_evidence]
  produces: [verification.design_reachability, verification.implementation_alignment]
  updates: [system.current_state, system.interface_rules, change.verification]
  invalidates: [design.gaps, verification.affected_evidence]
  handoff_to: [implementation, testing, sync_context]
```

Shared semantics: [memory and handoff protocol](../../../../protocols/skill-declarations.md); shared execution: [Coordination](../../../../protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../../../protocols/presenter.md); views carry source revisions and never own domain facts.

Check the selected design before build and the actual implementation after build. Trace each requirement through its entry point (route, menu, command, job, or public export), registration, interface, owning module, adapter, and test. Verify dependency direction, middleware order, error and permission paths, and dynamic registration where applicable.

Classify each row as `REACHABLE`, `PARTIAL`, `MISSING`, `DIVERGENT`, or `UNASSESSED`, with file/symbol evidence and the consumed design revision. Do not call code unused solely because static search misses dynamic or external consumers.

Apply only repairs within the requested scope when evidence is conclusive: broken registrations, stale links, missing exports, obsolete local guidance, and redundant documentation. Preserve unique rationale and user-authored rules. Route design changes back to the design owner; route broad cleanup to `acs-sync-context`.

Output `verification.md` (or the established verification home) with the trace matrix, failures, repairs, commands, environment, omissions, and one next action. Validation is complete when every in-scope criterion and module contract has a verdict and the remaining gaps are actionable.
