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
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


This entry retains the former context router's behavior. Older callers must migrate the name to `acs-manage-context`; no unprefixed alias is installed. Route by the requested outcome, then inspect the existing configuration:

1. Use `acs-translate-agent-context` for cross-runtime migration.
2. Use `acs-init-context` when setup is requested, or missing/lost routing blocks a required persistent write after checking explicit sources, established homes, and protocol defaults. Preserve any other established routing found during inspection.
3. Use `acs-sync-context` to inspect or reconcile drift in existing context. If routing is absent, a read-only inspection can still use explicit sources; hand off to `acs-init-context` only when the requested repair needs routing.

Missing `docs/agents/memory.md` alone does not require setup. Routing is complete when the focused skill has taken over, or a read-only request has been answered from explicit sources. Canonical contracts live under `system/protocols/`; compatibility aliases contain no independent rules.
