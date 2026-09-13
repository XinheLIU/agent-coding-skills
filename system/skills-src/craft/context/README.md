# Context Skills

Last updated: 2026-09-14

The [shared protocol](init-context/references/PROTOCOL.md) is the sole definition of North Star, Current State, Change Context, and Run Context. Indexes are derived views. Retain compact change records and reconcile present truth before deleting run scratch.

| Skill | Use it for |
| --- | --- |
| `init-context` | Configure routing and canonical homes when absent |
| `sync-context` | Detect drift, route domain reassessment, and verify retention |
| `translate-agent-context` | Preserve behavior across runtime surfaces |
| `engineer-domain-model` | Maintain shared terminology and consequential ADRs |
| `manage-context` | Compatibility entry for older callers |

The [coordinator](../../../workflows/context-coordination.md) resolves identities and paths, serializes shared writes, binds runtime capabilities, and applies proposed transitions. Domain skills own their judgments and evidence.
