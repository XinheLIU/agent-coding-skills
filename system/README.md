# Agent Coding System

Last updated: 2026-09-14

This directory is the plugin and product. Its skills share a repository memory system: setup declares the paths and protocols once, then all skills coordinate through those artifacts across the six lifecycle phases.

## System model

The [shared protocol](skills-src/craft/context/init-context/references/PROTOCOL.md) defines four lifecycles: North Star, Current State, Change Context, and Run Context. Product records retain their HTML format; engineering tickets and specs keep Markdown or established tracker homes. One canonical ticket/spec connects all contributions.

[Workflow coordination](workflows/context-coordination.md) resolves paths and identity, assembles relevant context, binds available runtime capabilities, serializes contributions, tracks freshness, and cleans up reconciled scratch. Skills retain domain reasoning and evidence interpretation.

## Structure

| Path | Contents |
| --- | --- |
| [`skills-src/`](skills-src/) | Skill source packages organized by lifecycle phase |
| [`skills/`](skills/) | Flat symlinks into `skills-src/` for one-level loader discovery |
| [`memory/`](memory/) | Layer definitions, read/write protocol, ownership registry |
| [`workflows/`](workflows/) | Six lifecycle workflows plus legacy sequences |
| [`commands/`](commands/) | Setup and Git commands |
| [`agents/`](agents/) | Shared explorer, reviewer, and delivery agents |
| [`docs/`](docs/) | Human guides and organization report |
| [`.claude-plugin/`](.claude-plugin/) | Claude Code plugin manifest |
| [`.codex-plugin/`](.codex-plugin/) | Codex plugin manifest |

## Workflow entry points

Six verbs cover the full lifecycle — use these as the primary entry points:

- [Plan](workflows/plan.md) — turn uncertain concepts into accepted product intent
- [Design](workflows/design.md) — settle requirements, UX, and technical architecture (three sub-phases: requirements → UX → technical)
- [Build](workflows/build.md) — implement features with plan approval, TDD, and handoff
- [Test](workflows/test.md) — audit coverage and add integration tests after build
- [Deploy](workflows/deploy.md) — release to staging and production with evidence
- [Maintain](workflows/maintain.md) — diagnose incidents and close the loop autonomously for in-band fixes

`init-context` sets up memory state and `sync-context` reconciles it. `handoff` carries pointers into a fresh session. `engineer-domain-model` owns the shared glossary and ADRs.

Legacy workflows are retained for backward compatibility: [ideas](workflows/ideas.md), [feature-delivery](workflows/feature-delivery.md), [testing](workflows/testing.md), [debugging](workflows/debugging.md).

## Context and retention

Lifecycle and artifact roles live in [shared memory](memory/README.md), with detailed domain contracts loaded only when relevant. Code indexes are derived views. Accepted requirements/designs, consequential decisions, compact verification, and release references survive completion; execution plans, claims, raw outputs, and handoffs are disposable after reconciliation.

Preserve existing tracker/document locations. New local-only changes use tracked `docs/changes/<change-id>/`; run scratch uses the configured work root, default `.scratch/<effort>/`. Current-state assertions carry evidence and relevant revision/environment; documentation dates alone do not prove freshness.

## Setup

Run the setup command once per target repository:

```text
/agent-coding-skills:setup
```

It inspects existing conventions, proposes the memory configuration, and writes `docs/agents/memory.md` after approval. It does not create empty memory artifacts.

External adaptations and revisions are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
