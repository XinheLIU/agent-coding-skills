---
name: acs-research
description: Resolve an external technical fact blocking an engineering decision, specification, diagnosis, or implementation, with cited primary evidence. Use for bounded engineering questions unavailable in the repository; learning-oriented synthesis and original research belong to the user's research workflow.
---

# Research

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [research.question]
  retrieves: [change.relevant_context]
  produces: [research.cited_evidence]
  updates: []
  invalidates: [context.evidence_dependents]
  handoff_to: [requesting_domain]
```

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../../protocols/presenter.md); source records retain authority.


1. State the question and the decision it blocks. Read `docs/agents/memory.md` and the active effort when configured. The question is bounded when a source could prove or disprove the answer.
2. Investigate official documentation, specifications, source code, or first-party APIs. Every material claim must trace to the source that owns it; record conflicts and uncertainty.
3. Synthesize the answer, evidence, implications, and unresolved uncertainty. The result is complete when the waiting decision can proceed or the missing evidence is named precisely.
4. Keep exploration and raw sources in the coordinator-resolved Working research directory. Before formal review or dependent handoff, save the focused conclusion and minimum cited evidence in the requesting change/decision's Persistent home, with its actual proposed/verified status and source revisions. Link that retained record from the waiting decision and configured run recovery entry. For a transient answer with no downstream reliance, return the same structure in the conversation.

Delegation is optional and runtime-neutral. The cited report, rather than private agent context, is the durable handoff.
