# Organization Report

Last updated: 2026-09-17

## Chosen structure

Primary axis: **system component role**. Skills, shared memory, workflows, commands, agents, and human docs have distinct ownership and runtime behavior.

The user’s clarification determines the central invariant: skills do not operate as isolated prompt files. They share one configured memory system and use explicit protocols for reading, writing, ownership, handoff, and derived HTML views.

## Inventory

The [public catalog](../../catalog/skill-set.json) groups the canonical skill packages by lifecycle and cross-cutting capability. Run `python3 system/memory/validate_suite.py --inventory-only` for the current count and source/discovery/catalog agreement. Shared roles live in `agents/` and host commands in `commands/`.

All public skill IDs use `acs-`; the plugin remains `agent-coding-skills`. The [migration table](skill-name-migration.md) records the former names. `acs-manage-context` is an explicit-only compatibility router. The six lifecycle workflows are documents, not extra installed skills.

## Matt Pocock adaptation

| Upstream capability | System treatment |
| --- | --- |
| `ask-matt` | Adapted as workflow routing, retained in `acs-manage-context` |
| `setup-matt-pocock-skills` | Adapted as context skills and the setup command |
| `handoff`, `grilling`, `research`, `prototype`, `wayfinder` | Adapted as system skills with configured working-memory outputs |
| `domain-modeling`, `codebase-design`, `improve-codebase-architecture` | Adapted as shared terminology, decision, and design capabilities |
| `triage`, `diagnosing-bugs`, `resolving-merge-conflicts` | Adapted with runtime-neutral behavior and no automatic commits |
| `writing-great-skills` | Adapted with explicit memory ownership and provenance rules |
| `grill-with-docs` | Assigned for merge into `brainstorm-feature` |
| `to-spec` | Assigned for merge into `spec` |
| `to-tickets` | Assigned for merge into `tasks` |
| `implement` | Assigned for merge into the delivery/TDD executor |
| Matt `tdd` | Adapted into `acs-tdd` with criterion-linked evidence |
| Matt `code-review` | Merged into `acs-review-code-quality` (two-axis Standards/Spec) 2026-09-08 |
| `grill-me` | Omitted as a redundant wrapper around `grilling` |
| `teach` | Omitted as outside the coding-system boundary; its Markdown/HTML lesson pattern informed the memory design |

No files under `references/` were edited or promoted unchanged.

## Shared artifact model

The [shared protocol](../skills-src/craft/context/acs-init-context/references/PROTOCOL.md) defines the four lifecycles and [document layout](../skills-src/craft/context/acs-init-context/references/canonical-doc-layout.md) maps roles to homes. Product HTML remains semantic source; engineering roadmap HTML remains derived. Retained Change Context is separate from disposable Run Context. Each skill declares the same six context fields.

The [coordinator](../workflows/context-coordination.md) resolves identity, assembles relevant context, binds available runtimes, serializes writes/claims, propagates freshness, and cleans up reconciled scratch. Direct planning/execution contracts remove delivery's dependency on missing skills.

## Consolidation decisions

- Keep canonical skill packages grouped under `skills-src/<category>/`, including product-facing skills under `skills-src/plan/`; expose every package through a flat symlink in `skills/` for loader discovery.
- Centralize shared agents and commands.
- Remove the older duplicate `tdd-builder`; retain the feature-delivery version.
- Preserve detailed frontend, engineering-setup, Git, and review guides under `docs/`.
- Use one workflow document per requested path: ideas, feature shipping, testing, debugging.
- Preserve unresolved integration work in a prioritized TODO rather than claiming the move completed it.
