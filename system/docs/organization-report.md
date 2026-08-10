# Organization Report

Last updated: 2026-08-04

## Chosen structure

Primary axis: **system component role**. Skills, shared memory, workflows, commands, agents, and human docs have distinct ownership and runtime behavior.

The user’s clarification determines the central invariant: skills do not operate as isolated prompt files. They share one configured memory system and use explicit protocols for reading, writing, ownership, handoff, and derived HTML views.

## Inventory

| Source category | Skills |
| --- | ---: |
| Product ideation | 10 |
| Architecture design | 9 |
| Feature delivery | 6 |
| Code quality | 4 |
| Context management | 18 |
| Frontend | 3 |
| Debugging | 3 |
| Research and planning | 5 |
| **Total skills** | **58** |

The product also contains 26 canonical shared agents after removing one stale duplicate, plus five commands including setup.

## Matt Pocock adaptation

| Upstream capability | System treatment |
| --- | --- |
| `ask-matt` | Adapted as workflow routing, now folded into `manage-context` |
| `setup-matt-pocock-skills` | Adapted as `manage-context` (Phase A) and the setup command |
| `handoff`, `grilling`, `research`, `prototype`, `wayfinder` | Adapted as system skills with configured working-memory outputs |
| `domain-modeling`, `codebase-design`, `improve-codebase-architecture` | Adapted as shared core-memory and design capabilities |
| `triage`, `diagnosing-bugs`, `resolving-merge-conflicts` | Adapted with runtime-neutral behavior and no automatic commits |
| `writing-great-skills` | Adapted with explicit memory ownership and provenance rules |
| `grill-with-docs` | Assigned for merge into `brainstorm-feature` |
| `to-spec` | Assigned for merge into `spec` |
| `to-tickets` | Assigned for merge into `tasks` |
| `implement` | Assigned for merge into the delivery/TDD executor |
| Matt `tdd` | Assigned for merge into existing `tdd` |
| Matt `code-review` | Assigned for merge into `review-code-quality` |
| `grill-me` | Omitted as a redundant wrapper around `grilling` |
| `teach` | Omitted as outside the coding-system boundary; its Markdown/HTML lesson pattern informed the memory design |

No files under `references/` were edited or promoted unchanged.

## Shared artifact model

```text
docs/agents/memory.md             repository-specific routing
CONTEXT.md + docs/adr/            core domain memory
README.md + docs/                 human memory
docs/product/<slug>/prd.md        human memory — product intent, tracked
docs/wiki/                        optional code-map wiki
<work-root>/<effort>/             working memory, git-ignored
  state.md
  progress.md
  discovery/ideas.md -> brainstorm.md -> demand.md -> solution.md
  discovery/mvp.md -> premortem.md
  brief.md / map.md / spec.md / plan.md
  issues/NN-*.md
  research/ prototypes/ handoffs/
  diagnosis.md
  roadmap.md -> roadmap.html
```

Markdown owns meaning and status. HTML owns presentation and interaction only.

## Consolidation decisions

- Keep canonical skill packages grouped under `skills-src/<category>/`, including product-facing skills under `skills-src/product-ideation/`; expose every package through a flat symlink in `skills/` for loader discovery.
- Centralize shared agents and commands.
- Remove the older duplicate `tdd-builder`; retain the feature-delivery version.
- Preserve detailed frontend, engineering-setup, Git, and review guides under `docs/`.
- Use one workflow document per requested path: ideas, feature shipping, testing, debugging.
- Preserve unresolved integration work in a prioritized TODO rather than claiming the move completed it.
