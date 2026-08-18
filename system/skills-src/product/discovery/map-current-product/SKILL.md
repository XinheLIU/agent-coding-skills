---
name: map-current-product
description: Map what an existing codebase already does as a product baseline. Use when the user asks what an app/codebase/product does, wants user stories from existing code, inherits a repo, audits implemented versus planned product behavior, or needs a baseline before improving an existing product.
---

# Map Current Product

Last updated: 2026-08-18

Extract the current product from the code, docs, and tests before proposing anything new. The output is a source-backed baseline: who can do what today, what is partly built, what is only planned, and where the product surface has gaps.

## Shared Memory Contract

```text
Layer:    working — the source-backed current-product baseline
Owns:     <work-root>/<effort>/discovery/current-product.md
Promotes: implemented stories, product gaps, evidence pointers → PRD and scope-product-increment
```

Read `docs/agents/memory.md`, the active `state.md`, and `<product-docs>/<slug>/prd.md` when present. If memory routing is absent, work in conversation and recommend `manage-context` before persisting.

Write one artifact, update `state.md` with its path, and preserve existing PRD facts as the tracked source of product intent. Do not edit the codebase, PRD, or upstream discovery artifacts.

## Boundary

Map current behavior, not future scope. Do not validate demand, invent roadmap items, triage an MVP, or design an implementation. If the request is architecture-only with no user-visible outcome, route to `design/technical/codebase-design` or `design/technical/improve-codebase-architecture`.

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

### 4. Derive user stories

Write stories only for behavior with evidence. Use the product-facing form:

```text
As [specific persona or role], I can [observable action], so that [user outcome].
```

Keep stories implementation-neutral, but cite the implementation evidence beside each one. When a persona is inferred from auth, routes, copy, or model names, mark it as inferred and say from where.

### 5. Identify improvement candidates

List gaps and next-product questions without scoping them. Use this vocabulary so `scope-product-increment` can consume it directly:

- **Gap:** current behavior is missing, partial, contradictory, or invisible to users
- **Opportunity:** current behavior works but the user outcome is weaker than the product promise
- **Question:** evidence is insufficient to decide whether behavior exists or matters

If an improvement is already requested, hand off to `scope-product-increment` after the baseline exists.

## Output Format

Persist to `<work-root>/<effort>/discovery/current-product.md`:

```markdown
# Current Product Map: [Product Name]

Last updated: [YYYY-MM-DD]

## Product Snapshot
Purpose: [source-backed sentence]
Primary users: [roles/personas, with evidence]
Platforms/surfaces: [web/API/CLI/mobile/etc.]

## Evidence Index
| Area | Source |
| --- | --- |

## Implemented User Stories
| Story | Evidence | Notes |
| --- | --- | --- |

## In-Progress Behavior
| Behavior | Evidence | Missing link |
| --- | --- | --- |

## Planned Behavior
| Behavior | Evidence | Confidence |
| --- | --- | --- |

## Gaps and Opportunities
| Type | Finding | Evidence | Candidate next question |
| --- | --- | --- | --- |

## Product-Facing Flows
| Flow | Actor | Entry point | Outcome | Evidence |
| --- | --- | --- | --- | --- |

## Open Questions
- [Question that blocks product interpretation or increment scoping]
```

## Quality Bar

- Every implemented story names a persona, action, outcome, and evidence path.
- In-progress and planned work stay separate.
- UI/API/model gaps are visible instead of smoothed over.
- Source-backed facts are separated from inference.
- The artifact is a baseline another skill can consume without re-reading the whole codebase.

## Source Adaptation

Borrowed principles: PM-Skills `deliver-user-stories` for persona/action/benefit and INVEST-style testability; OpenSpec brownfield-first exploration for mapping only the slice at hand; existing `shape-solution` codebase exploration moved here as a standalone baseline.
