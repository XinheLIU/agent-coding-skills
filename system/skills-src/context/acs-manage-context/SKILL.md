---
name: acs-manage-context
description: Explicit-only compatibility router for context setup, synchronization, or cross-runtime translation. Prefer the focused ACS context skills for new integrations.
disable-model-invocation: true
---

# Manage Context

Last updated: 2026-09-25

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

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


This entry retains the former context router's behavior. Older callers must migrate the name to `acs-manage-context`; no unprefixed alias is installed:

1. Use `acs-init-context` when `docs/agents/memory.md` is absent.
2. Use `acs-sync-context` when the routing file exists.
3. Use `acs-translate-agent-context` for cross-runtime migration.

Routing is complete when exactly one canonical skill has taken over. Canonical contracts live under `system/protocols/`; compatibility aliases contain no independent rules.
