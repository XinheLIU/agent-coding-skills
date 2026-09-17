---
name: acs-init-context
description: Initialize shared agent context when docs/agents/memory.md is absent or routing was lost. Configure canonical context paths, durable change records, run scratch, and an optional derived code index; use acs-sync-context for later drift.
---

# Init Context

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: []
  retrieves: [repository.instructions, context.existing_records]
  produces: [context.routing]
  updates: [context.configuration, run.state]
  invalidates: [context.broken_references]
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Set up routing under the lifecycle model in [the protocol](references/PROTOCOL.md). Do not define another layer scheme.

`AGENTS.md` and `docs/agents/memory.md` are routing indexes. They point at canonical sources instead of copying their contents.

## 1. Inspect

Read the repository's current agent instructions, memory config, manifests, CI config, work root, durable context documents, and code-index signals. Derive commands and paths from the environment.

Inspection is complete when each prospective output is classified as `keep`, `create`, or `repair`, and every proposed value has either repository evidence or a named user decision.

If routing and all configured outputs are healthy, report that setup is already complete and stop. Use `acs-sync-context` for content drift.

## 2. Resolve configuration

Reuse settled choices. Resolve only these missing values:

- **Work root:** preserve an established location; otherwise `.scratch/`.
- **Issue tracker:** preserve the repository's tracker; otherwise GitHub when the remote proves it, local Markdown when it does not.
- **Change records:** preserve the canonical ticket/spec home; new local changes use tracked `docs/changes/<change-id>/`. Keep canonical ticket ID distinct from branch/run identity.
- **Operations:** link relevant environment/build/deploy constraints and existing release-evidence homes; load the Operations contract only when needed.
- **Active effort:** explicit user selection, current branch mapping, or a documented repository rule.
- **Product memory:** preserve the existing canonical product path and identity; new products use `docs/product/<product-slug>/product.html`. Map increments to that same product. Read [the product contract](references/product-memory.md) when product work exists; do not migrate legacy docs as an incidental setup action.
- **Design memory:** the durable design triad is root `DESIGN.md` (how) and `docs/design/prototype.html` (what), linked to `product.html` (why). Read [the design contract](references/design-memory.md) when design work exists; a legacy `docs/design/system.md` stays canonical until `acs-design-context` migrates it — not an incidental setup action.
- **Domain memory:** one root `CONTEXT.md` by default; use a context map only when distinct bounded contexts already exist.
- **Code index:** disabled by default; offer it only when repository scale makes repeated source search materially expensive.

Configuration is complete when a cold session can resolve every enabled layer without guessing.

## 3. Propose one write plan

List exact files to create or update, existing content to preserve, verification commands, and any dependency installation. Apply already authorized setup changes; ask only for unresolved choices or actions outside authorization. A skipped item stays unchanged.

The plan may include:

- `docs/agents/memory.md`
- the work-root ignore rule
- `<work-root>/<effort>/state.md` for an active effort
- a short startup sequence and memory pointer in `AGENTS.md` or `CLAUDE.md`
- an optional environment check script when the repository lacks one and cold starts are otherwise ambiguous
- an optional code index and its routing pointer

Create `CONTEXT.md`, ADRs, and product documents only when the repository already has facts that belong there. Empty placeholders add no routing value.

## 4. Write routing and working memory

Load [`references/working-memory.md`](references/working-memory.md) for the active-effort shape. Write `docs/agents/memory.md` with the resolved work root, tracker, active-effort rule, domain-memory layout, product-doc path, and code-index status.

Use [`references/templates/AGENTS.template.md`](references/templates/AGENTS.template.md) only for missing routing sections. Preserve user-authored instructions. Every context pointer must name the condition that makes an agent open its target, and every target must resolve.

Create `state.md` only for a real active effort. It must identify the current status, one concrete next action, blockers, canonical change/task and status references, consumed revisions, and the minimum pointers needed to resume. Confirm the work root is ignored.

This step is complete when the memory config resolves all enabled layers and the active effort can resume from `state.md` without reconstructing prior conversation.

## 5. Route durable facts

Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md). Move or link existing durable facts to one canonical lifecycle-appropriate home:

- terminology and bounded-context language -> `CONTEXT.md` or `CONTEXT-MAP.md`
- settled, durable trade-offs -> `docs/adr/NNNN-<slug>.md`
- product intent -> the configured durable product document (new default `docs/product/<product-slug>/product.html`)

Use [`references/CONTEXT-FORMAT.md`](references/CONTEXT-FORMAT.md) and [`references/ADR-FORMAT.md`](references/ADR-FORMAT.md) only when that branch is earned. Preserve unique rationale and leave pointers where a fact moved.

This step is complete when each routed fact has one canonical home and routing files contain pointers rather than copies.

## 6. Build the optional code index

Skip this step when `Code index: disabled` is recorded. Otherwise load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md), recommend a tool from repository needs, and obtain approval before adding its dependency.

Build the index, query one known symbol, and confirm the result against source. Record its tool, path, query command, and refresh command in the routing indexes. Runtime-specific MCP wiring requires an explicit request.

This step is complete when the recorded query works from a cold shell and returns a source-verified result.

## 7. Verify cold start

Follow only the new startup sequence: run the recorded environment check when present, inspect recent history, resolve the active effort, read `state.md`, and follow its pointers. Verify every new local link and literal command.

Setup is complete when that sequence reaches one executable next action, all enabled layer paths resolve, and no repository fact was duplicated into a second canonical home. Report created, repaired, skipped, and deferred items. Leave commits to the user.

## Guardrails

- Use code, manifests, and configuration as executable evidence; maintain useful Current State summaries with evidence and revisions, and keep historical rationale in Change Context/ADRs.
- Preserve user-authored sections and unrelated state.
- Move unique rationale to its canonical home before removing a stale copy.
- Store credentials, personal data, and large raw logs outside shared memory.
- Add hooks, watchers, daemons, dependencies, and runtime configuration only with explicit approval.
