---
name: research
description: Resolve an external technical fact with cited primary evidence. Use when an idea, decision, specification, diagnosis, or implementation depends on information unavailable in the repository.
---

# Research

Last updated: 2026-08-25

1. State the question and the decision it blocks. Read `docs/agents/memory.md` and the active effort when configured. The question is bounded when a source could prove or disprove the answer.
2. Investigate official documentation, specifications, source code, or first-party APIs. Every material claim must trace to the source that owns it; record conflicts and uncertainty.
3. Synthesize the answer, evidence, implications, and unresolved uncertainty. The result is complete when the waiting decision can proceed or the missing evidence is named precisely.
4. For persistent work, write one focused report under `<effort>/research/` and add its pointer to `state.md` or the waiting decision ticket. For transient work, return the same structure in the conversation.

Delegation is optional and runtime-neutral. The cited report, rather than private agent context, is the durable handoff.
