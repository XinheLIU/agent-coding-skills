---
name: acs-design-foundation
description: Design reusable technical foundations—libraries, SDKs, components, middleware, and infrastructure adapters—for project-local or independently published use, and specify the smallest verifiable bootstrap or adoption change.
---

# Design Foundation

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [design.capability_map]
  retrieves: [change.requirements, design.selected_architecture, system.current_state, system.conventions]
  produces: [design.foundation_contracts, change.foundation_spec]
  updates: [design.accepted_decisions, system.shared_capabilities]
  invalidates: [design.module_dependents, verification.foundation_coverage]
  handoff_to: [design_modules, implementation, validate_codebase]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

Design a foundation capability only when it has a named consumer and a clear reason to centralize it. A capability may remain a local module, become a package/library, or run as middleware or a service. Choose the smallest form that gives consumers locality and leverage. Do not move shared domain policy into a technical `common` layer merely because it is used twice.

For each capability record consumers, scenarios, public types, configuration, lifecycle, errors, ordering, observability, private internals, supported variation, and a real consumer verification path. Translate relevant usability, performance, scalability, resilience, and testability constraints into measurable acceptance targets. Add compatibility, versioning, and distribution only for independently published artifacts.

| Form | Design focus |
| --- | --- |
| Library / SDK | imports, examples, errors, configuration, compatibility |
| Component | state ownership, composition, accessibility, extension points |
| Middleware | registration, order, context propagation, short-circuit and failure behavior |
| Infrastructure adapter | lifecycle, timeout/transaction/message semantics, health and observability |

For greenfield, specify only the foundation needed by the first real end-to-end scenario. A bootstrap may use minimal scaffold, encapsulated infrastructure, declared module positions, one real full-link path, and one-command startup; empty placeholders are optional. For brownfield, use audit evidence when wiring is unclear, prefer adoption or a compatibility adapter before extraction, and document migration, preservation checks, and rollback when replacing a foundation.

Output `technical-design.md` sections for capability contracts and, when a bootstrap is needed, a tracked foundation spec with criterion IDs and binary gates. The design is ready when each capability has consumers, an owner, a contract, and a real verification path.
