# Context Skills

Last updated: 2026-09-25

The [shared protocol](../../protocols/skill-declarations.md) defines **Working Memory** for a run and **Persistent Memory** across runs (Intent, Current, Changes). The [Presenter](../../protocols/presenter.md) produces derived human views; decisions and exact reviewed content remain Persistent. Product HTML and design prototypes keep their canonical roles. Retain required records before cleaning Working.

| Skill | Use it for |
| --- | --- |
| `acs-init-context` | Configure routing and canonical homes when absent |
| `acs-sync-context` | Detect drift, route domain reassessment, and verify retention |
| `acs-translate-agent-context` | Preserve behavior across runtime surfaces |
| `acs-engineer-domain-model` | Maintain shared terminology and consequential ADRs |
| `acs-manage-context` | Compatibility entry for older callers |

The [coordinator](../../protocols/context-coordination.md) resolves identities and paths, serializes shared writes, binds runtime capabilities, and applies proposed transitions. Domain skills own their judgments and evidence.
