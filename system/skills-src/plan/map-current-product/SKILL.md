---
name: map-current-product
description: Map what an existing codebase already does as a product baseline. Use when the user asks what an app/codebase/product does, wants user stories from existing code, inherits a repo, audits implemented versus planned product behavior, or needs a baseline before improving an existing product.
disable-model-invocation: true
---

# Map Current Product

Last updated: 2026-09-13

Read the standalone [visual report contract](references/visual-report.md) before creating or extending `discovery.html`. This local reference is bundled with the skill; do not depend on `/meta` or another installed skill.
## Context contract

```yaml
context:
  requires: [product.assessed_surface]
  retrieves: [product.relevant_context, system.affected_source]
  produces: [product.behavior_evidence, product.coverage]
  updates: [product.baseline_proposals]
  invalidates: [product.behavior_dependents]
  handoff_to: [product, design]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Extract the current product from the code, docs, and tests before proposing anything new. The output is a source-backed baseline: who can do what today, what is partly built, what is only planned, and where the product surface has gaps.

## Shared Memory Contract

Read [the product memory contract](references/product-memory.md) before persistence. It defines record identity, enrichment, authority, promotion, HTML structure, and legacy input handling.


Read product intent, relevant capabilities, gaps, and questions before inspecting code. Record the inspected product surface and revision where available. Enrich existing subjects with observed behavior; preserve proposed behavior and accepted intent as separate facts.

Follow read–match–enrich–verify: create only missing records, preserve other contributions, link related evidence and questions, and return record anchors to the coordinator. If invoked standalone, use supplied context and create useful partial memory; an absent prior artifact is not an absent answer. Missing substantive prerequisites remain explicit questions, not invented facts. Existing authorization governs decisions.

## Boundary

Map current behavior, not future scope. Do not validate demand, invent roadmap items, triage an MVP, or design an implementation. Synthesizing a candidate vision is inference about the intent already expressed by existing behavior and stated docs — it is a question for the user, not a roadmap item, and it authorizes no scope. If the request is architecture-only with no user-visible outcome, route to `design/technical/harden-architecture` or `design/technical/audit-architecture`.

## Workflow

### 1. Resolve the product surface

Prefer explicit user-provided paths. Otherwise inspect the current repository. Read product-facing docs before code: `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/`, `CHANGELOG.md`, `ROADMAP.md`, release notes, issue templates, and existing PRDs.

Record the stated product purpose, named users, platforms, and promised capabilities with file references.

### 2. Map entry points and flows

List the top-level tree, then identify the product-facing seams:

- UI routes, pages, screens, CLI commands, API routes, jobs, webhooks, or integrations
- auth roles, permissions, tenants, plans, or actor types
- data models and persisted entities users create, change, or consume
- tests, fixtures, demos, screenshots, examples, or docs proving behavior

Follow routes to handlers and views far enough to understand observable behavior. Prefer structured framework conventions over broad text search when the stack reveals them.

### 3. Classify product behavior

Classify each product-facing capability:

| Status | Meaning |
| --- | --- |
| Implemented | Wired end-to-end, tested, documented as shipped, or otherwise observable in code |
| In progress | UI without backend, API without UI, stubbed handler, partial data flow, feature flag with missing path |
| Planned | Roadmap, TODO, docs, issue, or placeholder names intent but no user-visible behavior yet |
| Gap | Contradiction between product promise and code, orphaned UI/API/model, missing permission path, or unclear actor |

Every row needs an evidence pointer: file path plus route/function/component/test name when available.

### 4. Derive user stories with layered needs and source evidence

Write stories only for behavior with evidence. Use the product-facing form:

```text
As [specific persona or role], I can [observable action], so that [user outcome].
```

For each story, identify the need at three layers (method and rules: `references/need-layers.md`):

- **Surface need**: the ask this behavior directly serves, evidenced by the code and docs
- **Deep need**: why the ask arises — inferred from docs, copy, data models, and story clusters; marked inferred with its source until confirmed
- **Fundamental need**: the instinct-level need (a noun — a fear, a loss, an identity), stated only when evidence or user context supports it; otherwise recorded as an open question, not invented

And the implementation:

- **Functional modules**: which code modules/components implement this behavior
- **Cross-cutting concerns**: authentication, logging, caching, etc.

Keep stories implementation-neutral, but cite the implementation evidence beside each one. When a persona is inferred from auth, routes, copy, or model names, mark it as inferred and say from where.

### 5. Synthesize candidate visions

Stories are not single points. Cluster them by shared deep need, then ask what larger intent makes the clusters coherent as one product — a project tool whose stories cover context capture and chat-based ticket claiming may imply an AI-native-organization vision.

Record at most one or two candidate `vision` records in `overview`, marked inferred, each linking the stories that imply it. A candidate vision needs at least two independent story clusters behind it; a single story is a need, not a vision. Method and rules: `references/need-layers.md`.

### 6. Confirm with the user

After synthesis — never before — send one consolidated message following the close in
`references/shared-understanding.md`: the candidate visions with their supporting clusters, the deep and fundamental entries currently marked inferred, and a direct ask to confirm, correct, or reject each. Apply the reply: confirmed items become user-confirmed with the date; corrections update the records.

Skip the message when the run is non-interactive or the user asked for a pure audit: visions and inferred layers stay inferred, and each unconfirmed vision gets a linked open question. Do not chain follow-up questions; residual uncertainty is recorded, not interrogated.

### 7. Assess observable constraints and unanswered design questions

Record user-visible performance, permissions, recovery, accessibility, and integration behavior only where observed or promised, with environment/revision and evidence. Code modules and API/data paths are evidence pointers, not mandatory architecture assessments.

If understanding a user outcome exposes a technical uncertainty, record the question and its blocking effect. Route cohesion/coupling, dependency cycles, API contracts, data-model design, or refactoring recommendations to `harden-architecture`, `audit-architecture`, or `review-architecture` when that analysis is requested. Do not infer demand or poor architecture from code inventory alone.

### 8. Identify improvement candidates

List gaps and next-product questions without scoping them. Use this vocabulary so `define-outcomes` can consume it directly:

- **Gap:** current behavior is missing, partial, contradictory, or invisible to users
- **Opportunity:** current behavior works but the user outcome is weaker than the product promise
- **Question:** evidence is insufficient to decide whether behavior exists or matters

A shortfall names the expected user outcome and observed behavior; insufficient evidence remains a question.

If an improvement is already requested, hand off to `define-outcomes` after the baseline exists.

## Output Format

Enrich `<work-root>/<effort>/discovery.html` using the shared record contract. Load [the HTML presentation patterns](references/html-report.md) and the standalone [visual report contract](references/visual-report.md) when creating or extending the baseline visuals. Reuse the document's style and navigation.

- Update overview coverage: product surface inspected, source revision when available, and exclusions.
- Create or enrich the effort's `research-coverage` record in the `research` section of `discovery.html`: aggregate assessed and not-assessed dimensions (platforms, roles, flows, data sources) across contributors, and state whether research is ready for roadmap decomposition — naming the blocking gaps or questions when it is not. This run's inspection updates the aggregate; it does not overwrite another contributor's recorded coverage.
- Enrich shared personas, capabilities, and journeys with current observed behavior and evidence. Keep implemented, partial, planned intent, and unassessed behavior distinct.
- Record candidate visions in `overview` with inferred/confirmed status and links to the implying stories; when the confirmation message was skipped, record the linked open question.
- Story records carry surface/deep/fundamental entries with per-layer status (inferred / user-confirmed / evidenced); unconfirmed need-fit hypotheses remain questions linked to observed capabilities.
- Attach user-flow maps and observable constraints to the capabilities they explain; cite code paths only as evidence.
- Match existing gaps, opportunities, and questions before adding findings. Cite the expected outcome and observed shortfall. Resolve an existing behavior question only when inspection answers it; do not close demand or scope questions from code alone.
- Preserve desired behavior and scope decisions contributed by other skills. If the baseline contradicts them, record the disagreement and mark affected conclusions for review.

Return the relevant anchors to the coordinator, open the resulting HTML for the user when requested or presenting a new report, and report the absolute path plus the records added or enriched. No companion Markdown baseline.

### Verify memory records

- Every record `<article>` has a document-unique id and a closed-list `data-kind` (see the contract's kind table).
- Records sit inside one of the shared sections listed in the contract's section table (including `research` in `discovery.html` and `roadmap` in `product.html`).
- Local `#anchor` links resolve; unrelated records and IDs are preserved.
- `Last updated` dates are current on changed records and the document.
- Run `python3 scripts/validate-product-memory.py <file>` when available; fix errors before reporting.

## Quality Bar

- Every implemented story names a persona, action, outcome, surface need, functional modules, and evidence path; deep and fundamental needs are stated or recorded as open questions, each marked with its status (inferred / user-confirmed / evidenced) and source.
- Candidate visions are supported by at least two story clusters, marked inferred until the user confirms, and never converted into roadmap items.
- User confirmation happens in one consolidated message, or is explicitly skipped with the open questions recorded.
- Observable constraints and coverage are evidenced; technical design questions are routed with their blocking effects.
- In-progress and planned work stay separate.
- UI/API/model gaps are visible instead of smoothed over, with user impact noted.
- Source-backed facts are separated from inference.
- The artifact is a baseline another skill can consume without re-reading the whole codebase.

## Source Adaptation

Borrowed principles: PM-Skills `deliver-user-stories` for persona/action/benefit and INVEST-style testability; OpenSpec brownfield-first exploration for mapping only the slice at hand; existing `shape-solution` codebase exploration moved here as a standalone baseline; matt-pocock `audit-architecture` for the original self-contained HTML report and diagram-first presentation. The adapted output now uses shared semantic records and inline styling; the earlier standalone Tailwind/Mermaid report scaffold is superseded.
