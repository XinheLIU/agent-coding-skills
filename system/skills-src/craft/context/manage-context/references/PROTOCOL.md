# Shared Memory Protocol

Last updated: 2026-08-10

## Repository configuration

`docs/agents/memory.md` is the routing document created by `manage-context` (Phase A). It records:

- the work root and issue tracker;
- single-context or multi-context domain memory;
- the human documentation root and the product-docs home inside it;
- whether the optional wiki is enabled;
- the Markdown sources and commands used to rebuild HTML views;
- the active-effort selection rule.

If the file is absent, a skill may perform read-only work using existing conventions. A skill must run or recommend setup before creating persistent shared state whose location is ambiguous.

## Layer contract

Four layers, each defined by the question it answers and how long the answer stays true. See [`memory/README.md`](../../../../../memory/README.md) for the full table.

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Core | What words and constraints bind this project | Project | Tracked |
| Human | What we are building, why, and how it works | Project | Tracked |
| Wiki | Where the code for X lives | Rebuildable | Either |
| Working | How the current effort is going and what happens next | Effort | Ignored |

**The durability test.** Before writing persistent state, ask: *if the work root were deleted today, would the project have lost a fact it still needs?* If yes, the fact belongs in the Human or Core layer. If no, it belongs in working memory.

Working memory holds the *how* and *now* — drafts, plans, task state, evidence trails. The Human and Core layers hold the *what* and *why* — product intent, architecture, settled trade-offs, conventions. A skill choosing a path picks the layer from the question its output answers, not from the stage of the workflow that produced it.

**Promotion is one-way: Working → Human or Core.** Promote a decision when it is settled, hard to reverse, and would surprise someone who did not watch it happen. The working artifact keeps a link to the promoted fact, never a second copy. Nothing is ever demoted from a persistent layer into working memory.

## Skill contract

Every installed skill participates in this protocol in one of three modes:

- **Owner**: reads configured inputs, writes one canonical artifact, and records the transition.
- **Consumer**: reads canonical artifacts and may report findings, but does not rewrite their facts.
- **Transient**: performs an in-session operation and writes no persistent memory.

An owner declares three things before it writes:

```text
Layer:    working | human | core
Owns:     <the one path it writes>
Promotes: <the durable fact it contributes upward> → <owning artifact>
```

`Promotes: none` is a valid and common answer — most working artifacts are consumed by a downstream skill and then discarded with the effort. State it explicitly rather than leaving it open.

Setup, workflow, and handoff skills may coordinate state; they do not acquire ownership of the artifacts they route.

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

### Persistent layers — the *what* and *why*

Tracked in git. Survives the effort that produced it.

| Artifact | Layer | Owner | Other skills |
| --- | --- | --- | --- |
| `docs/agents/memory.md` | Config | `manage-context` (Phase A) | Read only |
| `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/` | Core | `domain-modeling` | Consume; propose changes through the owner |
| `<product-docs>/<slug>/prd.md` | Human | `write-prd` | `spec` consumes product intent; it does not rewrite the PRD |
| Human docs — `docs/architecture/`, `docs/conventions/`, `docs/quality/`, runbooks | Human | `scaffold-agent-docs` (structure + audit), `document-codebase` (content), `create-readme` (README) | Link to them; `manage-context` (Phase B) coordinates structural repairs |
| `AGENTS.md` + `docs/` initial structure | Human | `scaffold-agent-docs` | Review skills own later structure |
| Wiki/code index | Wiki | `index-codebase` | Consume; request refresh when stale |
| Cross-layer consistency | — | `manage-context` (Phase B) | Owns no layer; corrects facts and routes structural drift |

### Working layer — the *how* and *now*

Under the configured work root, git-ignored. Discarded with the effort. The `Promotes` column names the durable fact the artifact contributes upward; `none` means the artifact is consumed downstream and then dies with the effort.

| Artifact | Owner | Promotes | Other skills |
| --- | --- | --- | --- |
| Work-root initialization | `manage-context` (Phase A) | none | Workflows populate it afterward |
| `state.md` | Current workflow coordinator | none | Skills update only their transition fields |
| `progress.md` | Append-only session log | none | Every skill appends; never rewrite history |
| `discovery/ideas.md` | `generate-product-ideas` *(system gap)* | none — only the selected candidate travels | `brainstorm` consumes the selected candidate |
| `discovery/brainstorm.md` | `brainstorm` | Persona, job, struggle → PRD Part 1 | Product skills consume it |
| `discovery/demand.md` | `validate-demand` | Demand type, evidence grade, verdict → PRD Part 1 | `shape-solution` consumes the type and grade |
| `discovery/solution.md` | `shape-solution` | User stories, first-use moment → PRD Parts 1 and 3 | `scope-mvp` consumes the stories and moment |
| `discovery/mvp.md` | `scope-mvp` | Requirement list, scope boundaries, Not-To-Do → PRD Part 1 | Product skills consume its axes and P0 list |
| `discovery/premortem.md` | `run-premortem` | Edge cases, NFRs, monitoring signals → PRD Part 3 | Product skills consume its risks and mitigations |
| `prototypes/<slug>/decision.md` | `prototype` | Interaction decisions → PRD Part 3; architectural decisions → ADR | The stage that raised the question resumes from it |
| `map.md`, decision tickets | `wayfinder` | Settled cross-session decisions → ADR | Consume; do not duplicate decisions |
| `spec.md` | `spec` | none — the shipped code is the durable answer | Downstream skills read only |
| `plan.md` | `plan` *(system gap)* | none | Downstream skills read only |
| Issue files and dependency edges | `tasks` / `wayfinder` | none | Executors update claim/status only |
| `roadmap.md`, `roadmap.html` | `draw-portfolio-dag` | none | Views only |
| `diagnosis.md` | `diagnosing-bugs` | A regression rule worth enforcing → `CONVENTIONS.md` or a rule file | TDD consumes confirmed reproduction and cause |
| Handoffs | `handoff` (in feature-delivery) | none | New sessions consume and then follow source pointers |

An artifact appears in exactly one of these tables. If a skill is unsure which, it applies the durability test rather than writing to both.

## Working-memory shape

```text
<work-root>/<effort>/
├── state.md
├── progress.md
├── brief.md
├── discovery/
│   ├── ideas.md
│   ├── brainstorm.md
│   ├── demand.md
│   ├── solution.md
│   ├── mvp.md
│   └── premortem.md
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

Note what is *not* here: `prd.md`. Product intent is Human-layer and lives at `<product-docs>/<slug>/prd.md` — the discovery files above are the surface it is drafted on, not its home.

## Product-docs shape

```text
<human-docs>/product/          ← `<product-docs>`, default `docs/product/`
└── <slug>/
    └── prd.md
```

`<slug>` names the product for a greenfield effort and the feature for an incremental one. It matches the effort slug when one exists, so a reader can trace a PRD back to the discovery that produced it — and forward from `state.md` to the intent it serves.

## Concurrency

An executable issue must declare `Status`, `Blocked by`, and `Claimed by`. Claim before editing. A claim is exclusive until released or completed. Dependencies and completion are written to Markdown before regenerating the HTML roadmap.
