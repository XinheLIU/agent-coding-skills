---
name: acs-design-modules
description: Turn a selected architecture into implementable code modules, interfaces, types, dependency rules, wiring, and brownfield migration steps for business and shared capabilities.
---

# Design Modules

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [design.selected_architecture]
  retrieves: [change.requirements, system.current_state, design.capability_map, system.conventions]
  produces: [design.module_contracts, design.wiring_map, design.migration_plan]
  updates: [design.accepted_decisions, system.interface_rules]
  invalidates: [change.implementation_plan, verification.contract_coverage]
  handoff_to: [validate_codebase, implementation]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

For each module define one responsibility, its public interface (including invariants and failures), owned types, dependencies, callers, registration/wiring location, and verification surface. Apply the deletion test and prefer a deep interface with local implementation complexity. Add seams for real variation; reuse a framework directly when it already provides the required contract. Show current ownership beside target ownership, seam placement, and dependency direction with a compact before/after diagram.

Cover routes, menus, commands, jobs, exports, adapters, middleware order, and dependency injection where they are part of the feature path. For brownfield work, use cohesion and change-coupling evidence to choose splits, break dependency cycles at caller-owned seams, preserve observable behavior with characterization evidence, and introduce facades or adapters where useful. Sequence one independently verifiable boundary change at a time, migrate callers incrementally, and name rollback points.

Name interfaces from the domain and consumer need. Record selection rules in the repository's applicable `AGENTS.md`/Claude Rules through context management rather than duplicating them in module docs. Use lightweight domain clarification; create a formal glossary or ADR only when the term or decision will be reused and is consequential.

## Output

Update `technical-design.md` with a module table, interface contracts, dependency direction, route/menu/export wiring, shared capability usage, tests, and migration steps. Include a current/target ownership and seam diagram for each structural change. When an HTML companion is used, read [the local HTML report format](references/HTML-REPORT.md). The result is implementation-ready when a builder can locate every symbol, registration point, and acceptance criterion without inventing ownership.
