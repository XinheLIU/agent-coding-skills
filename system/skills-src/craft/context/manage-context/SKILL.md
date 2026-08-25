---
name: manage-context
description: Route legacy manage-context calls to the current context skill.
disable-model-invocation: true
---

# Manage Context

Last updated: 2026-08-25

This compatibility name preserves older integrations:

1. Use `init-context` when `docs/agents/memory.md` is absent.
2. Use `sync-context` when the routing file exists.
3. Use `translate-agent-context` for cross-runtime migration.

Routing is complete when exactly one canonical skill has taken over. The shared protocol remains at `../init-context/references/PROTOCOL.md`.
