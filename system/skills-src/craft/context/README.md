# Context Skills

Last updated: 2026-08-26

Shared context has three layers:

| Layer | Answers | Canonical contents |
| --- | --- | --- |
| Human | Why must the project behave this way? | Product intent, terminology, constraints, ADRs |
| Code index | Where is the current implementation and how is it connected? | Optional rebuildable index |
| Working | What is happening now and what happens next? | Active effort state, drafts, issues, and handoffs |

`AGENTS.md` and `docs/agents/memory.md` route agents to these sources; they are indexes, not additional knowledge stores. Each fact has one canonical home. While work is active, promoted conclusions replace working copies with pointers. When work finishes, its plans and scratch artifacts are compacted into decision records or reader-relevant changelog entries, then removed unless a retention rule requires them.

| Skill | Use it for |
| --- | --- |
| `init-context` | Configure the three layers when routing is absent |
| `sync-context` | Detect and repair drift after setup |
| `translate-agent-context` | Preserve behavior while moving agent surfaces across runtimes |
| `manage-context` | Compatibility entry point for older callers |

The full layer and ownership contract lives with `init-context` in [`references/PROTOCOL.md`](init-context/references/PROTOCOL.md).
