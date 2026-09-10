---
name: manage-context
description: Route legacy manage-context calls to the current context skill.
disable-model-invocation: true
---

# Manage Context

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: []
  retrieves: [context.configuration]
  produces: [context.route]
  updates: []
  invalidates: []
  handoff_to: [context_management]
```

Shared semantics: [shared protocol](../init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


This compatibility name preserves older integrations:

1. Use `init-context` when `docs/agents/memory.md` is absent.
2. Use `sync-context` when the routing file exists.
3. Use `translate-agent-context` for cross-runtime migration.

Routing is complete when exactly one canonical skill has taken over. The shared protocol remains at `../init-context/references/PROTOCOL.md`.
