---
name: audit-architecture
description: Survey architectural friction and propose deepening opportunities as linked Markdown and HTML reports. Use when modules are hard to understand, change, test, or navigate with agents.
---

# Audit Architecture

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [system.affected_source]
  retrieves: [system.invariants, design.relevant_decisions, verification.failure_history]
  produces: [design.structural_assessment]
  updates: []
  invalidates: [design.disproved_assumptions]
  handoff_to: [refactoring, design]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Read memory routing, domain context, ADRs, and `harden-architecture`. Scope the survey to the user’s target or recent hot spots.

Identify shallow modules, scattered knowledge, leaky seams, and tests coupled to internals. Apply the deletion test before recommending a new interface.

Write a canonical Markdown report under `docs/architecture/reviews/` with files, problem, proposed deepening, leverage/locality benefit, test impact, ADR conflicts, and recommendation strength. Generate a same-named self-contained HTML view with before/after diagrams. The HTML must cite its Markdown source and generation time.

Ask which candidate to explore. Route the selected candidate into `challenge-approach`; do not refactor during the survey.
