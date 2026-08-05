# Shared Memory Protocol

Last updated: 2026-08-05

## Repository configuration

`docs/agents/memory.md` is the routing document created by `manage-context` (Phase A). It records:

- the work root and issue tracker;
- single-context or multi-context domain memory;
- the human documentation root;
- whether the optional wiki is enabled;
- the Markdown sources and commands used to rebuild HTML views;
- the active-effort selection rule.

If the file is absent, a skill may perform read-only work using existing conventions. A skill must run or recommend setup before creating persistent shared state whose location is ambiguous.

## Skill contract

Every installed skill participates in this protocol in one of three modes:

- **Owner**: reads configured inputs, writes one canonical artifact, and records the transition.
- **Consumer**: reads canonical artifacts and may report findings, but does not rewrite their facts.
- **Transient**: performs an in-session operation and writes no persistent memory.

A skill must state its mode and artifact ownership before it writes persistent state. Setup, workflow, and handoff skills may coordinate state; they do not acquire ownership of the artifacts they route.

## Read protocol

Before acting, a memory-aware skill reads only the relevant surfaces:

1. Read `docs/agents/memory.md`.
2. Read the relevant `CONTEXT.md` and ADRs for terminology and constraints.
3. Resolve the active effort from the user, current branch, or configured rule.
4. Read its `state.md`, then follow pointers to the minimum required artifacts.
5. Treat generated HTML as a view; use the linked Markdown when reasoning about state.

## Write protocol

1. Write facts in one canonical artifact; link elsewhere instead of copying them.
2. Update only artifacts owned by the active skill or explicitly delegated to it.
3. Preserve user-authored sections and unrelated state.
4. Add or update `Last updated: YYYY-MM-DD` near the top of edited Markdown.
5. Update `state.md` with status, next action, blockers, and pointers after a workflow transition.
6. Regenerate affected HTML views after changing their Markdown sources.
7. Never record credentials, tokens, personal data, or large raw logs in shared memory.

## Artifact ownership

| Artifact | Owner | Other skills |
| --- | --- | --- |
| `docs/agents/memory.md` | `manage-context` | Read only |
| `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/` | `domain-modeling` | Consume; propose changes through the owner |
| Human docs | `scaffold-agent-docs` (structure + audit), `document-codebase` (content), `create-readme` (README) | Link to them; `manage-context` (Phase B) coordinates structural repairs |
| `AGENTS.md` + `docs/` initial structure | `scaffold-agent-docs` | Review skills own later structure |
| Wiki/code index | `index-codebase` | Consume; request refresh when stale |
| Cross-layer consistency | `manage-context` (Phase B) | Owns no layer; corrects facts and routes structural drift |
| Work-root initialization | `manage-context` (Phase A) | Workflows populate it afterward |
| `state.md` | Current workflow coordinator | Skills update only their transition fields |
| `discovery/ideas.md` | `generate-product-ideas` | `brainstorm` consumes the selected candidate |
| `discovery/brainstorm.md` | `brainstorm` | Product-discovery skills consume it |
| `discovery/jtbd.md` | `analyze-jtbd` | Product-discovery skills consume it |
| `discovery/opportunity.md` | `validate-product-opportunity` | `critique-idea` consumes its evidence and gaps |
| `discovery/critique.md` | `critique-idea` | Product-discovery skills consume its verdict and demand type |
| `discovery/user-story.md` | `write-user-story` | Product-discovery skills consume it |
| `discovery/mvp.md` | `design-mvp` | Product-discovery skills consume its scope |
| `discovery/strategy-review.md` | `review-product-strategy` | `design-mvp` consumes accepted scope changes; product-discovery skills consume the decision |
| `discovery/premortem.md` | `run-premortem` | Product-discovery skills consume its risks and mitigations |
| `prd.md` | `write-prd` | `spec` consumes product intent; it does not rewrite the PRD |
| `map.md`, decision tickets | `wayfinder` | Consume; do not duplicate decisions |
| `spec.md` | `spec` | Downstream skills read only |
| `plan.md` | `plan` *(system gap)* | Downstream skills read only |
| Issue files and dependency edges | `tasks` / `wayfinder` | Executors update claim/status only |
| `roadmap.md`, `roadmap.html` | `draw-portfolio-dag` | Views only |
| `diagnosis.md` | `diagnosing-bugs` | TDD consumes confirmed reproduction and cause |
| Handoffs | `handoff` (in feature-delivery) | New sessions consume and then follow source pointers |

## Working-memory shape

```text
<work-root>/<effort>/
├── state.md
├── brief.md
├── discovery/
│   ├── ideas.md
│   ├── brainstorm.md
│   ├── jtbd.md
│   ├── opportunity.md
│   ├── critique.md
│   ├── user-story.md
│   ├── mvp.md
│   ├── strategy-review.md
│   └── premortem.md
├── prd.md
├── map.md
├── spec.md
├── plan.md
├── issues/NN-*.md
├── research/
├── prototypes/
├── handoffs/
├── diagnosis.md
├── roadmap.md
└── roadmap.html
```

Create only artifacts earned by the workflow. Empty scaffolds are not memory.

## Concurrency

An executable issue must declare `Status`, `Blocked by`, and `Claimed by`. Claim before editing. A claim is exclusive until released or completed. Dependencies and completion are written to Markdown before regenerating the HTML roadmap.
