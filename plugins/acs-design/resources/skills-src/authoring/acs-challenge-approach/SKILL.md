---
name: acs-challenge-approach
description: Use when a user-owned decision blocks an idea, plan, design, triage brief, or decision ticket.
---

# Challenge Approach

Last updated: 2026-10-23

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

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../../protocols/presenter.md); source records retain authority.


1. Inspect the available context until every remaining blocker is a decision rather than a discoverable fact.
2. Follow the [questioning protocol](../../../protocols/questioning.md): classify candidates, ask only the settled-prerequisite frontier, and lead with a recommendation and its trade-off.
3. Reflect each answer as a concrete decision and correct it immediately if the user disagrees.
4. Stop when every decision required by the caller's completion criterion is resolved. Return confirmed decisions and genuinely open questions to the caller, which owns persistence and implementation.

## When NOT to use

- For production-readiness code review, use [acs-review-code-quality](../../test/review/acs-review-code-quality/SKILL.md) (reference procedure; capability not installed).
- For unsettled flows, wireframes, or interaction states, use [acs-design-interaction-flow](../../../../skills/acs-design-interaction-flow/SKILL.md).
- For product-demand evidence grading (explicit invocation only), use [acs-validate-demand](../../plan/acs-validate-demand/SKILL.md) (reference procedure; capability not installed).
