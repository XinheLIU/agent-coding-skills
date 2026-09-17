---
name: acs-design-architecture
description: Map accepted features to business modules and shared technical capabilities, compare current, ideal, and feasible target architectures, and record the selected evolution for greenfield or brownfield systems.
---

# Design Architecture

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [system.current_state, system.affected_source, design.relevant_decisions]
  produces: [design.architecture_options, design.selected_architecture, design.capability_map]
  updates: [design.accepted_decisions, system.architecture_state]
  invalidates: [design.module_dependents, change.implementation_plan]
  handoff_to: [design_foundation, design_modules, validate_codebase]
```

Read the requirement criteria and inspect the relevant repository slice. For greenfield, establish the minimum structure that supports the accepted features. For brownfield, distinguish what exists from what is intended before proposing change.

For each structural option, make the current-versus-target change visible with a compact diagram; keep the detailed evidence in the Markdown design.

## Workflow

1. Map each feature to a capability, owner, entry point, data it changes, and evidence or requirement ID. Mark unknowns explicitly.
2. Identify shared capabilities by real consumers: communication, persistence, identity, errors, observability, scheduling, storage, UI primitives, or domain policies. Keep shared domain rules with their owning domain. Record only relevant non-functional constraints, with measurable targets, verification methods, and the trade-offs that determine architecture.
3. Describe current architecture where code exists. Describe an ideal architecture with freedom to reorganize. For brownfield, derive a feasible target that accounts for compatibility, migration cost, and operational constraints.
4. Compare two or three materially different options on locality, leverage, failure isolation, operability, migration cost, and complexity. Recommend one and record rejected alternatives only when the trade-off is consequential.
5. Produce `technical-design.md` (or the established design home) containing feature-to-module mapping, capability consumers, option comparison, selected architecture, gaps, and open decisions. Include a readable current/ideal/feasible comparison diagram and stable IDs for modules and capabilities. When an HTML companion is used, read [the local HTML report format](references/HTML-REPORT.md), apply the visual report contract with inline SVG first, and include a card for each materially different option.

The design is ready when every accepted requirement has an owner, every shared capability has an explicit consumer list, every selected boundary has a reason, and every gap has a next action or an explicit out-of-scope decision.

## Handoff

Send shared capability rows to `acs-design-foundation` and business/module rows to `acs-design-modules`. A greenfield foundation may be designed before all feature modules when it is needed to validate the first real path. A brownfield audit is required only when current structure or compatibility is unknown; use `acs-audit-architecture` for that evidence.
