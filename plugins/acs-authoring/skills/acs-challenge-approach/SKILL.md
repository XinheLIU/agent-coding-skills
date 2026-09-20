---
name: acs-challenge-approach
description: Resolve user-owned decisions one at a time. Use when choices that cannot be discovered from the environment block an idea, plan, design, triage brief, or wayfinder ticket.
---

# Challenge Approach

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [decision.open_question]
  retrieves: [decision.existing_answers]
  produces: [decision.user_answer]
  updates: []
  invalidates: [context.answer_dependents]
  handoff_to: [domain_owners]
```

Shared semantics: [shared protocol](../../context/acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


1. Inspect the available context until every remaining blocker is a decision rather than a discoverable fact.
2. Walk prerequisite decisions before downstream choices. Ask one question at a time; lead with a recommendation and its trade-off.
3. Reflect each answer as a concrete decision and correct it immediately if the user disagrees.
4. Stop when every decision required by the caller's completion criterion is resolved. Return confirmed decisions and genuinely open questions to the caller, which owns persistence and implementation.
