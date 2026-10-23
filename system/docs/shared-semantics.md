# Shared skill semantics

Last updated: 2026-10-23

Canonical paragraphs for source skills and portable packages. Source skills link to
the applicable section; `scripts/build-plugins.py` expands that link in packaged
`SKILL.md` files and relocates its contract links with the other dependencies.
Keep skill-specific rules when changing these variants.

This adapts generated preambles from [gstack](https://github.com/garrytan/gstack)
(`35dd014`, `scripts/gen-skill-docs.ts`) and source-derived drift checking from
[PM-Skills](https://github.com/product-on-purpose/pm-skills)
(`scripts/gen-derived-surfaces.mjs`); no upstream runtime code is included.

## Execution

Shared semantics: [shared protocol](../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../protocols/presenter.md); source records retain authority.

## Planning

Shared semantics: [shared protocol](../protocols/skill-declarations.md#skill-declarations); shared writes and claims: [Coordination](../protocols/context-coordination.md). Existing authorization persists. A planning request authorizes the plan, not implementation. Working Memory holds run recovery; Persistent Memory holds reusable domain records, including proposed review inputs. Save referenced conclusions before formal review or dependent handoff. For human-facing reports and review feedback, use [Presenter](../protocols/presenter.md); views carry source revisions and never own domain facts.

## Context

Shared semantics: [shared protocol](../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.

## README ownership

Shared semantics: [shared protocol](../protocols/skill-declarations.md#skill-declarations);
shared execution: [Coordination](../protocols/context-coordination.md).
Existing authorization persists. This skill owns human-facing README content;
`acs-review-agent-instructions` owns `AGENTS.md`/`CLAUDE.md`, and `acs-sync-context`
owns repository-wide document classification and reorganization.

## Technical design

Shared semantics: [memory and handoff protocol](../protocols/skill-declarations.md); shared execution: [Coordination](../protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../protocols/presenter.md); views carry source revisions and never own domain facts.
