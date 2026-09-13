---
name: explore-unknowns
description: Map a multi-session effort into dependency-ordered decision tickets. Use when the destination is known but the route is unclear, or independent decisions can proceed concurrently.
---

# Explore Unknowns

Last updated: 2026-09-14

## Context contract

```yaml
context:
  requires: [change.objective]
  retrieves: [change.requirements, design.relevant_decisions]
  produces: [change.decision_tickets]
  updates: [run.decision_map]
  invalidates: [run.dependent_plans]
  handoff_to: [design, implementation]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Wayfinding resolves the route; the delivery workflow executes it.

## Chart

1. Read shared memory and relevant domain context, including the effort PRD when present. Extract the destination, fixed scope, and explicit exclusions.
2. Use `challenge-approach` until destination and scope are concrete enough to distinguish an in-scope decision from an unrelated question.
3. Write `<effort>/map.md` with Destination, Decisions so far, Open decisions, and Out of scope.
4. Propose one addressable decision ticket per consequential open question, reusing canonical identity and parent change. Preserve existing tracker homes; new local tickets live in tracked Change Context. Each records domain status, `depends_on`, scope, question, and accepted answer/evidence. Claims remain Run Context through the coordinator.
5. Use `draw-portfolio-dag` to regenerate `roadmap.md` and `roadmap.html`. Charting is complete when every open decision is represented once and every dependency is either an edge or an explicit external blocker.

## Resolve

Work one frontier ticket per session unless the user authorizes independent tickets to run concurrently. Have the coordinator acquire the exclusive claim before work; retain the accepted answer, rationale and revisions in the decision ticket, and keep only a linked summary in `map.md`. Turn newly exposed uncertainty into tickets, then regenerate both roadmap views.

The map is complete when no in-scope open decision remains. Hand canonical decision/requirement references and consumed revisions to `build/implement`; implementation requires a separate request or an explicit scope change.
