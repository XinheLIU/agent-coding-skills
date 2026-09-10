# Agent Coding System

Last updated: 2026-09-09

This directory is the plugin and product. Its skills share a repository memory system: setup declares the paths and protocols once, then idea, delivery, testing, debugging, review, and documentation skills coordinate through those artifacts.

## System model

The [shared protocol](skills-src/craft/context/init-context/references/PROTOCOL.md) defines four lifecycles: North Star, Current State, Change Context, and Run Context. Product records retain their HTML format; engineering tickets and specs keep Markdown or established tracker homes. One canonical ticket/spec connects all contributions.

[Workflow coordination](workflows/context-coordination.md) resolves paths and identity, assembles relevant context, binds available runtime capabilities, serializes contributions, tracks freshness, and cleans up reconciled scratch. Skills retain domain reasoning and evidence interpretation.

## Structure

| Path | Contents |
| --- | --- |
| [`skills-src/`](skills-src/) | Skill source packages grouped into browsable categories |
| [`skills/`](skills/) | Flat symlinks into `skills-src/` for one-level loader discovery |
| [`memory/`](memory/) | Layer definitions, read/write protocol, ownership registry |
| [`workflows/`](workflows/) | Ideas, feature delivery, testing, debugging |
| [`commands/`](commands/) | Setup and Git commands |
| [`agents/`](agents/) | Shared explorer, reviewer, and delivery agents |
| [`docs/`](docs/) | Human guides and organization report |
| [`.claude-plugin/`](.claude-plugin/) | Claude Code plugin manifest |
| [`.codex-plugin/`](.codex-plugin/) | Codex plugin manifest |

## Context and retention

Lifecycle and artifact roles live in [shared memory](memory/README.md), with detailed domain contracts loaded only when relevant. Code indexes are derived views. Accepted requirements/designs, consequential decisions, compact verification, and release references survive completion; execution plans, claims, raw outputs, and handoffs are disposable after reconciliation.

Preserve existing tracker/document locations. New local-only changes use tracked `docs/changes/<change-id>/`; run scratch uses the configured work root, default `.scratch/<effort>/`. Current-state assertions carry evidence and relevant revision/environment; documentation dates alone do not prove freshness.

## Workflow entry points

- [Ideas](workflows/ideas.md): greenfield product discovery plus existing-product baselines and increments, with research/prototype/wayfinder detours.
- [Design](workflows/design.md): design context (DESIGN.md / system.md) → interaction design → visual variants → production implementation, orchestrating external design skills.
- [Feature delivery](workflows/feature-delivery.md): specification → plan → dependency tickets → implementation → review.
- [Testing](workflows/testing.md): public seams → TDD → checks → test-gap audit.
- [Debugging](workflows/debugging.md): red-capable reproduction → evidence → regression test → fix.

`init-context` sets up memory state and `sync-context` reconciles it. `handoff` carries pointers into a fresh session. `domain-modeling` owns the shared glossary and ADRs.

## Setup

Run the setup command once per target repository:

```text
/agent-coding-skills:setup
```

It inspects existing conventions, proposes the memory configuration, and writes `docs/agents/memory.md` after approval. It does not create empty memory artifacts.

## Current limitations

Planning and execution are active-agent stages defined in the delivery workflow; dedicated `plan` and `implement` skills and an executable Harness are not part of this iteration. Operations defines a context/release boundary using existing project tooling. Remaining adaptations are tracked in [`TODO.md`](TODO.md).

External adaptations and revisions are recorded in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
