---
name: acs-design-modules
description: Design or review code structure — module responsibilities, deep interfaces, owned types, dependency direction, wiring, shared-capability forms (library, component, middleware, adapter), splits and migration. Use when an architecture must become implementable code or when modules are shallow, tangled, or need splitting; writes the MOD section of the shared technical-design.md.
---

# Design Modules

Last updated: 2026-09-29

## Context contract

```yaml
context:
  requires: [design.selected_architecture]
  retrieves: [change.requirements, system.current_state, design.capability_map, system.conventions]
  produces: [design.module_contracts, design.wiring_map, design.migration_plan, design.foundation_contracts]
  updates: [design.accepted_decisions, system.interface_rules, system.shared_capabilities]
  invalidates: [change.implementation_plan, verification.contract_coverage]
  handoff_to: [design_contracts, design_test_strategy, trace_requirements, implementation]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

Follow [the card contract](../../resources/skills-src/design/technical/references/card-contract.md): read ARC, write only `## Modules & Interfaces (MOD)` and `FND-MOD-*` rows. Views follow [the technical view template](../../resources/skills-src/design/technical/references/technical-view.md) and [the visual report contract](../acs-design-architecture/references/visual-report.md).

**Owns:** where code lives, what each module exposes, which way dependencies point, and how the pieces are wired. **Does not own:** what the parts are (ARC), what must stay true across calls (CON), how it is tested (TST).

## Current (brownfield)

For the modules the change touches:

- **Shallow modules.** Interface complexity (method count, parameter count, concepts to learn) against the complexity hidden. Apply the deletion test: if the abstraction were removed, how much simpler would callers be, and how much would they absorb?
- **Cohesion and change coupling.** Files that change together (`git log` co-change), responsibilities that are mixed, concerns scattered across modules.
- **Wiring.** Routes, menus, commands, jobs, exports, dependency injection, middleware order, and dynamic registration on the feature path.

## Target

For each module, one `MOD-n` row:

| Field | Content |
| --- | --- |
| Responsibility | One sentence; if it needs "and", split it |
| Interface | Public functions/types, named from the domain and the consumer's need |
| Owned types | Types no other module constructs |
| Depends on / callers | Direction must match ARC layering |
| Wiring | Registration point, route, export, or DI binding, with file path |
| Requirements | Criterion IDs it serves |

Prefer a deep interface: small surface, significant hidden implementation. Add a seam only for real variation; use the framework directly when it already provides the contract. Show current and target ownership, seam placement, and dependency direction in one compact before/after diagram per structural change.

**Shared capabilities from ARC** get a contract shaped by their form:

| Form | Settle |
| --- | --- |
| Library / SDK | Import surface, examples, errors, configuration, compatibility; versioning only if published independently |
| Component | State ownership, composition, accessibility, extension points |
| Middleware | Registration, execution order, context propagation, short-circuit and failure behavior |
| Infrastructure adapter | Resource lifecycle, timeout/transaction/message semantics, health, observability |

**Greenfield bootstrap.** Specify only what the first real end-to-end scenario needs. Optional slices: minimal scaffold, encapsulated infrastructure, declared module positions, one real full-link path, one-command startup. Empty placeholders are not required; a 501 proves registration only.

**Brownfield migration.** Change one independently verifiable boundary at a time. Break cycles at caller-owned seams. Preserve behavior with characterization evidence (planned in TST), introduce facades or adapters where useful, migrate callers incrementally, and name rollback points. Prefer adopting an existing library over extracting a new one; extraction needs named consumers and measurable benefit.

Record interface naming and selection rules in the applicable `AGENTS.md` or Claude Rules through `acs-sync-context`, not in module docs.

## Review mode

Flag as `FND-MOD-n`: modules with more than one responsibility, shallow wrappers that fail the deletion test, dependencies pointing against the ARC layering, missing registration points, interfaces named after implementation rather than the domain, and migrations without a rollback point.

## Done when

A builder can locate every symbol, registration point, and criterion without inventing ownership. Hand interfaces to `acs-design-contracts` for their invariants and failure behavior.
