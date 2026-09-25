# Portable ACS Harness

Last updated: 2026-09-25

ACS has one set of domain skills and shared context contracts. Generated plugins materialize their transitive resource closure with the same public skill IDs. Context coordination and Presenter are written procedures executed by the active agent; this change adds no scheduler or host SDK integration.

## Identity and ownership

`system/skills-src/` owns skill content. A package directory and its frontmatter `name` use the same `acs-<name>` ID; `system/skills/` exposes exactly one symlink per source package. The catalog describes that inventory and is checked against it. The plugin ID remains `agent-coding-skills`.

The host adds its own invocation syntax or plugin qualification around the ID. Neither `/`, `$`, nor a host/plugin namespace becomes part of `name`. The migration table is documentation, not an alias registry. External skill names and protocol selectors such as `research.question` remain unchanged.

| Component | Owns | Uses |
| --- | --- | --- |
| Domain skill | Domain reasoning, scoped work, acceptance criteria, evidence interpretation | Canonical inputs and available capabilities |
| Harness coordinator | Context assembly, workflow selection, claims, scheduling, freshness, reconciliation, handoff | Existing context and task contracts; selected host binding |
| Presenter | Reading order, comparisons and review views over versioned records | Domain judgments and the shared Presenter contract |
| Host adapter | Discovery, invocation syntax, tool calls, questions, delegation, workspace isolation, lifecycle events | Host APIs and the neutral procedure/role prompts |

The [shared protocol](../protocols/skill-declarations.md) remains authoritative for context and state ownership. The [coordinator](../workflows/context-coordination.md) remains authoritative for execution coordination. This document defines packaging and adapter boundaries, not a second protocol or task database.

## Host capability boundary

Discover capabilities from the actual session and host documentation, using the existing [capability profile](../skills-src/context/acs-translate-agent-context/references/agent-surface.md#capability-profile). Record verified availability and restrictions for skill loading, file/tool access, questions, delegation, workspace isolation, lifecycle events, persistence, and enforcement. Unknown capability support needs verification; a host or model name alone is not evidence.

Domain procedures request capabilities rather than naming `AskUserQuestion`, `Task`, a preferred model, or a host executable. Adapters resolve those requests to available tools. Shared role prompts stay outside host-specific control flow. Ordinary host permission rules and the user's existing authorization continue to apply.

Delivery retains the existing [dispatch, await, collect, reclaim contract](../skills-src/build/acs-implement/references/orchestration-protocol.md). When authorized delegation and safe coordination are available, bind those operations to the host. Otherwise the active agent executes ready work serially, writes the same evidence, and reconciles the same canonical tickets. A missing required tool produces a named blocker; missing optional delegation does not.

Canonical status stays in the configured tracker. Persistent Memory retains cross-run Intent, Current and Changes, including version-scoped review decisions. Working Memory holds one configured recovery entry per run and disposable execution handles. The [Presenter](../protocols/presenter.md) reads versioned records and provides derived views; domain skills own judgment and the coordinator reconciles feedback. A later restart must reread current tickets, claims, revisions, and evidence before resuming; it cannot replay a stale write or restore authorization from an adapter's private state.

## Current host support

These statuses describe checked-in surfaces, not proven runtime parity.

| Target | Existing surface | Remaining work |
| --- | --- | --- |
| Codex | Main and context-subpackage plugin manifests; shared skill discovery | Translate existing explicit-only frontmatter for Codex ingestion; host binding and behavioral parity verification |
| Claude Code | Main and context-subpackage manifests; setup/Git commands; role prompts | Host capability binding and behavioral parity verification |
| Pi | Context-subpackage `package.json` with `pi.skills` | Full-suite packaging, extension lifecycle binding, verification |
| OpenCode | Neutral skill and context source only | Verify current package/plugin API, implement adapter, test parity |
| DeepSeek harness | Neutral skill and context source only | Identify actual host/version and APIs, implement adapter, test parity |

A DeepSeek model provider is not itself a host adapter. Host discovery and lifecycle behavior must be checked against the actual harness. The [herdr/Claude example](runtime-bindings/herdr.md) is an optional documented binding whose CLI syntax requires verification; it is not the portable default.

The current Codex validator rejects ten existing `disable-model-invocation: true` declarations in the main suite, both before and after the namespace migration. This is a known packaging compatibility gap, not permission to change their invocation policy. The context subpackage passes manifest/skill validation; neither result establishes runtime parity. See the verification baseline.

## Standalone package contract

The unit is one independently usable capability, not a single giant harness skill. Plugin and standalone outputs must be generated from the same canonical sources and retain the same public ID and behavior.

- Declare and include the required protocol excerpts/files, role prompts, templates, scripts, and their transitive runtime resources. Follow resource symlinks when building; installed references must resolve within the package.
- Rewrite local resource paths in generated output only. Shared resources have one maintained source; generated copies are not edited independently.
- Discover optional companion skills by their exact ACS ID. Without them, the active agent performs the applicable procedure directly when competent; necessary supporting procedures/resources must travel in the package. A required capability that cannot be supplied yields a precise blocker.
- Resolve scripts from the installed skill/package root, not the user's working directory or a sibling repository.
- Installing a focused capability does not require full-suite setup. Reuse configured project memory when present; use explicit task inputs and the shared defaults when absent.
- Keep provenance and required license notices in generated artifacts; copied upstream study material under repository-root `references/` is excluded.

Source skill directories can link outside themselves. The plugin and context builders resolve symlinks and rewrite linked resources into a self-contained output. Referenced companion procedures travel as nondiscoverable supporting documents, not fictitiously installed capabilities. Package tests check all copied Markdown links, remove a fixture source checkout, relocate outputs, compare deterministic rebuilds and execute the packaged DAG tests. Install the entire generated directory, including resources; these checks do not establish host parity or arbitrary single-directory copying.

Further behavioral acceptance requires representative tasks in each supported host. Start with `acs-research`, `acs-tdd`, `acs-review-code-quality`, and `acs-implement`; then cover every public skill. Check authorized serial operation, optional-skill absence, unavailable required tools, and equivalent evidence in plugin and standalone modes. Resource isolation alone does not prove those behaviors.

## Delivery sequence

1. Namespace and inventory integrity: source/loader/catalog agreement, upstream coexistence, preserved contracts, and explicit portability limits.
2. Standalone distribution: dependency declarations, deterministic materialization, isolated resource and behavior tests.
3. Host adapters: verify each target's current APIs and implement the same capability contract; record native, partial, or unavailable support explicitly.
4. Runtime enhancements: add scheduling, resume, and lifecycle automation only where actual use requires executable enforcement.

Local user-skill installation remains managed by skills-manager: update its source records first, then refresh agent-target symlinks. The repository migration does not overwrite upstream installations or recreate the retired `.agents/skills` discovery directory.
