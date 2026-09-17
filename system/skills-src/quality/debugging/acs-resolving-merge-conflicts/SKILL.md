---
name: acs-resolving-merge-conflicts
description: Resolve an in-progress Git merge or rebase from both sides' documented intent. Use only when conflict markers or Git state show an active conflict operation.
---

# Resolving Merge Conflicts

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [source.conflict_state]
  retrieves: [change.requirements, design.relevant_decisions, source.both_intents]
  produces: [change.conflict_resolution_evidence]
  updates: [source.conflicted_files]
  invalidates: [verification.for_changed_code, context.affected_dependents]
  handoff_to: [testing, coordinator]
```

Shared semantics: [shared protocol](../../../craft/context/acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Inspect Git state, conflicting files, commits, source issues/specs, and relevant shared memory. For each hunk, state both intents and preserve both when compatible. When incompatible, choose the result that matches the operation’s stated goal and report the trade-off. Do not invent unrelated behavior.

Run the repository’s checks after resolving. Stage files only as required to mark conflicts resolved. Continue or commit only when the user’s request authorizes completing that Git operation; never create an unrelated commit automatically.

If the operation’s intent cannot be established, stop with the exact unresolved choice instead of guessing or aborting destructively.
