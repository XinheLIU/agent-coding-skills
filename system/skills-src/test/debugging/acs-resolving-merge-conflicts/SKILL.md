---
name: acs-resolving-merge-conflicts
description: Use when Git state or conflict markers show an active merge or rebase conflict.
---

# Resolving Merge Conflicts

Last updated: 2026-10-23

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

[Shared semantics](../../../../docs/shared-semantics.md#execution)


Inspect Git state, conflicting files, commits, source issues/specs, and relevant shared memory. For each hunk, state both intents and preserve both when compatible. When incompatible, choose the result that matches the operation’s stated goal and report the trade-off. Do not invent unrelated behavior.

Run the repository’s checks after resolving. Stage files only as required to mark conflicts resolved. Continue or commit only when the user’s request authorizes completing that Git operation; never create an unrelated commit automatically.

If the operation’s intent cannot be established, stop with the exact unresolved choice instead of guessing or aborting destructively.
