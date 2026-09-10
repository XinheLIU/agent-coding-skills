---
name: handoff
description: Preserve actionable context for a fresh session or domain consumer using canonical change identity, accessible revision-labelled references, and explicit next action. Use before a reset or transfer of active work.
---

# Handoff

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.active_identity]
  retrieves: [run.state, change.requirements, design.relevant_decisions, verification.latest_evidence]
  produces: [run.handoff]
  updates: []
  invalidates: []
  handoff_to: [receiving_agent, coordinator]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Use the [shared handoff envelope](../../../craft/context/init-context/references/PROTOCOL.md#handoff-envelope). The coordinator supplies the active change/task, relevant run pointers, canonical status, and consumed revisions. Read only the referenced sections needed to resume.

## Produce the envelope

Write a concise Run Context handoff at `<work-root>/<effort>/handoffs/<session>-<focus>.md`, or return it to the parent coordinator for transport. Include:

```markdown
# Handoff: <focus>

Last updated: YYYY-MM-DD

Change/task: <canonical IDs and links>
Scope: <bounded work and receiver>

## References and consumed revisions
<Canonical spec/criteria, accepted design/contracts, source revision or diff digest,
verification environment, active freshness findings, canonical ticket status link.>

## Delta and accepted decisions
<What changed; references to accepted decisions and retained rationale.>

## Unresolved questions
<Question → blocking effect; include conflicts and verification omissions.>

## Next action
<One executable action and its needed reference.>

## Claim transfer
<Current owner and explicit transfer state, or not applicable.>
```

Verify all references from the receiving environment, including worktree access. Transport a bounded source excerpt with its revision and revalidation condition only when needed; it remains temporary context. Retain accepted requirements, consequential decisions, and final evidence before handing off rather than leaving their only copy in this file.

Return the envelope and proposed next action to the coordinator, which updates run routing, appends progress, and transfers claims explicitly. Keep the handoff under roughly 60 lines; do not copy the conversation or maintain duplicate ticket status. No commit is implied.
