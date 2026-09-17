# Context Skills

Last updated: 2026-09-17

The [shared protocol](acs-init-context/references/PROTOCOL.md) is the sole definition of North Star, Current State, Change Context, and Run Context. Indexes are derived views. Retain compact change records and reconcile present truth before deleting run scratch.

| Skill | Use it for |
| --- | --- |
| `acs-init-context` | Configure routing and canonical homes when absent |
| `acs-sync-context` | Detect drift, route domain reassessment, and verify retention |
| `acs-translate-agent-context` | Preserve behavior across runtime surfaces |
| `acs-engineer-domain-model` | Maintain shared terminology and consequential ADRs |
| `acs-manage-context` | Compatibility entry for older callers |

The [coordinator](../../../workflows/context-coordination.md) resolves identities and paths, serializes shared writes, binds runtime capabilities, and applies proposed transitions. Domain skills own their judgments and evidence.
