# Organization Report

Last updated: 2026-09-09

## Chosen structure

Primary axis: **system component role**. Skills, shared memory, workflows, commands, agents, and human docs have distinct ownership and runtime behavior.

The user’s clarification determines the central invariant: skills do not operate as isolated prompt files. They share one configured memory system and use explicit protocols for reading, writing, ownership, handoff, and derived HTML views.

## Inventory

| Source category | Skills |
| --- | ---: |
| Product | 9 |
| Design | 11 |
| Engineering | 5 |
| Quality | 10 |
| Craft / context | 10 |
| Operations | 0 |
| **Total skills** | **45** |

The product also contains 26 canonical shared agents after removing one stale duplicate, plus five commands including setup.

## Matt Pocock adaptation

| Upstream capability | System treatment |
| --- | --- |
| `ask-matt` | Adapted as workflow routing, now folded into `manage-context` |
| `setup-matt-pocock-skills` | Adapted as `manage-context` (Phase A) and the setup command |
| `handoff`, `grilling`, `research`, `prototype`, `wayfinder` | Adapted as system skills with configured working-memory outputs |
| `domain-modeling`, `codebase-design`, `improve-codebase-architecture` | Adapted as shared terminology, decision, and design capabilities |
| `triage`, `diagnosing-bugs`, `resolving-merge-conflicts` | Adapted with runtime-neutral behavior and no automatic commits |
| `writing-great-skills` | Adapted with explicit memory ownership and provenance rules |
| `grill-with-docs` | Assigned for merge into `brainstorm-feature` |
| `to-spec` | Assigned for merge into `spec` |
| `to-tickets` | Assigned for merge into `tasks` |
| `implement` | Assigned for merge into the delivery/TDD executor |
| Matt `tdd` | Assigned for merge into existing `tdd` |
| Matt `code-review` | Merged into `review-code-quality` (two-axis Standards/Spec) 2026-09-08 |
| `grill-me` | Omitted as a redundant wrapper around `grilling` |
| `teach` | Omitted as outside the coding-system boundary; its Markdown/HTML lesson pattern informed the memory design |

No files under `references/` were edited or promoted unchanged.

## Shared artifact model

The [shared protocol](../skills-src/craft/context/init-context/references/PROTOCOL.md) defines the four lifecycles and [document layout](../skills-src/craft/context/init-context/references/canonical-doc-layout.md) maps roles to homes. Product HTML remains semantic source; engineering roadmap HTML remains derived. Retained Change Context is separate from disposable Run Context. Each of the 45 skills declares the same six fields.

The [coordinator](../workflows/context-coordination.md) resolves identity, assembles relevant context, binds available runtimes, serializes writes/claims, propagates freshness, and cleans up reconciled scratch. Direct planning/execution contracts remove delivery's dependency on missing skills.

## Consolidation decisions

- Keep canonical skill packages grouped under `skills-src/<category>/`, including product-facing skills under `skills-src/product/`; expose every package through a flat symlink in `skills/` for loader discovery.
- Centralize shared agents and commands.
- Remove the older duplicate `tdd-builder`; retain the feature-delivery version.
- Preserve detailed frontend, engineering-setup, Git, and review guides under `docs/`.
- Use one workflow document per requested path: ideas, feature shipping, testing, debugging.
- Preserve unresolved integration work in a prioritized TODO rather than claiming the move completed it.
