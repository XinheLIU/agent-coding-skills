# Agent Coding System

Last updated: 2026-09-25

This directory is the plugin and product. Its skills coordinate through shared repository records across the six lifecycle phases. Setup configures paths when needed; explicit inputs and unambiguous existing homes also support standalone work.

## System model

The accepted [Context design](docs/context-memory-presenter-proposal.md) defines **Working Memory**, **Persistent Memory**, and a **Presenter**. The [shared protocol](protocols/skill-declarations.md) owns their artifact roles: Working holds run recovery and scratch; Persistent holds Intent, Current, and Changes. One canonical ticket/spec connects all contributions. Product records retain their HTML format; engineering records keep Markdown or established tracker homes.

The [Presenter](protocols/presenter.md) organizes versioned sources for human reading or review. Domain skills own conclusions; review decisions and exact reviewed content remain persistent. Accepted visual prototypes are persistent artifacts, while reports and DAGs are reconstructible views.

[Workflow coordination](workflows/context-coordination.md) resolves paths and identity, assembles relevant context, binds available runtime capabilities, serializes contributions, tracks freshness, and cleans up reconciled scratch. Skills retain domain reasoning and evidence interpretation.

## Structure

| Path | Contents |
| --- | --- |
| [`skills-src/`](skills-src/) | Skill source packages organized by lifecycle phase |
| [`skills/`](skills/) | Flat symlinks into `skills-src/` for one-level loader discovery |
| [`protocols/`](protocols/) | Memory, ownership, handoff, coordination, and Presenter contracts |
| [`workflows/`](workflows/) | Six lifecycle workflows plus legacy sequences |
| [`commands/`](commands/) | Setup and Git commands |
| [`agents/`](agents/) | Shared explorer, reviewer, and delivery agents |
| [`docs/`](docs/) | Human guides and organization report |
| [`.claude-plugin/`](.claude-plugin/) | Claude Code plugin manifest |
| [`.codex-plugin/`](.codex-plugin/) | Codex plugin manifest |

## Workflow navigation

Six workflow documents cover the lifecycle. They are navigation and sequencing guidance, not installed commands or router skills:

- [Plan](workflows/plan.md) — turn uncertain concepts into accepted product intent
- [Design](workflows/design.md) — settle requirements, UX, and technical architecture (three sub-phases: requirements → UX → technical)
- [Build](workflows/build.md) — plan delivery from Product or Design, then execute ready slices with TDD and verification
- [Test](workflows/test.md) — audit coverage and add integration tests after build
- [Deploy](workflows/deploy.md) — release to staging and production with evidence
- [Maintain](workflows/maintain.md) — diagnose incidents and close the loop autonomously for in-band fixes

`acs-init-context` sets up memory state and `acs-sync-context` reconciles it. The shared handoff envelope carries pointers into a fresh session. `acs-engineer-domain-model` owns the shared glossary and ADRs. `acs-manage-context` retains the explicit-only compatibility routing behavior under the new namespace.

The [harness architecture](docs/harness-architecture.md) separates domain skills, coordination, presentation and host adapters. Generated plugins retain public skill IDs and embed linked dependencies. Isolation tests cover resource closure and executable renderer behavior; copying individual source directories alone and host runtime parity remain outside that guarantee.

Legacy workflows are retained for backward compatibility: [ideas](workflows/ideas.md), [feature-delivery](workflows/feature-delivery.md), [testing](workflows/testing.md), [debugging](workflows/debugging.md).

## Context and retention

Memory and artifact roles live in the [shared protocol](protocols/skill-declarations.md), with domain contracts loaded only when relevant. Proposed records become persistent before formal review or downstream reliance; persistence does not imply acceptance. Code indexes are derived views. Requirements/designs, consequential decisions, compact verification, and release references survive completion; execution plans, claims, raw outputs, and handoffs are disposable only after the run ends and durable information is reconciled.

Preserve existing tracker/document locations. New local-only changes use tracked `docs/changes/<change-id>/`; run scratch uses the configured work root, default `.scratch/<effort>/`. Current-state assertions carry evidence and relevant revision/environment; documentation dates alone do not prove freshness.

## Setup

Run the setup command once per target repository:

```text
/agent-coding-skills:setup
```

It inspects existing conventions and configures `docs/agents/memory.md`, including one recovery entry per run. Existing authorization applies; ask only about unresolved choices or work beyond that scope. It does not create empty memory artifacts.

External adaptations and revisions are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
