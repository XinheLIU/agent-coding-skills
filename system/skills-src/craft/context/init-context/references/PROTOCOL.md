# Shared Memory Protocol

Last updated: 2026-08-26

## Repository configuration

`docs/agents/memory.md` is the routing document written during setup. It records:

- the work root and issue tracker;
- single-context or multi-context domain memory;
- whether the optional code index is enabled;
- the active-effort selection rule.

If the file is absent, a skill may perform read-only work using existing conventions. A skill must run or recommend setup before creating persistent shared state whose location is ambiguous.

## Layer contract

Three layers, each defined by the question it answers:

| Layer | Answers | Lifetime | Git |
| --- | --- | --- | --- |
| Human | Why: decisions, constraints, terminology, product intent | Project | Tracked |
| Code Index | What/How: where code lives, what calls what | Rebuildable | Either |
| Working | Now: current effort state, next actions, drafts | Effort | Ignored |

**The separation principle.** Human layer documents only WHY — decisions code cannot show, constraints that bind the project, terminology that must stay consistent. Code Index (optional) documents WHAT and HOW — current structure agents can discover by reading code or querying an index. Working memory holds ephemeral state for the current effort.

**The durability test.** Before writing persistent state, ask: *if the work root were deleted today, would the project have lost a fact it still needs?* If yes, the fact belongs in the Human layer. If no, it belongs in working memory.

A skill choosing a path picks the layer from the question its output answers, never from the workflow stage that produced it. Product intent, scope boundaries, and settled trade-offs are WHY facts and belong in the Human layer even though a discovery or delivery effort is what surfaced them — they get passed around, outlive the effort, and cannot be recovered by reading code. Drafts, task state, and evidence trails answer NOW and stay in working memory.

**Promotion is one-way: Working → Human.** Promote a decision when it is settled, hard to reverse, and would surprise someone who did not watch it happen. The working artifact keeps a link to the promoted fact, never a second copy. Nothing is ever demoted from a persistent layer into working memory.

**Completion compacts; it does not archive by default.** Once an effort is verified as landed or abandoned, its plans, implemented specs, task state, scratch notes, handoffs, and evidence trails have finished their job. Extract only facts that still earn durable storage, point those records at the canonical evidence, then remove the completed working artifacts. Keep an archive only when an explicit audit, regulatory, or repository retention rule requires one.

Route the durable residue by purpose:

| What remains useful | Canonical record |
| --- | --- |
| Why a consequential choice was made, including meaningful rejected alternatives | ADR or the repository's decision-record home |
| A reader-relevant shipped, removed, deprecated, or migrated outcome | Existing changelog or release-history home |
| Product intent, scope, non-goals, or terminology that remains normative | Existing product or terminology home |
| Current behavior, structure, commands, and verification | Code, tests, manifests, and configuration; durable records point there instead of restating them |

A completed plan is never promoted wholesale. The implementation sequence, checked boxes, intermediate reasoning, and superseded drafts are not project memory.

## Skill contract

Every installed skill participates in this protocol in one of three modes:

- **Owner**: reads configured inputs, writes one canonical artifact, and records the transition.
- **Consumer**: reads canonical artifacts and may report findings, but does not rewrite their facts.
- **Transient**: performs an in-session operation and writes no persistent memory.

An owner declares three things before it writes:

```text
Layer:    working | human | code-index
Owns:     <the one path it writes>
Promotes: <the durable fact it contributes upward> → <owning artifact>
```

`Promotes: none` is a valid and common answer — most working artifacts are consumed by a downstream skill and then discarded with the effort. State it explicitly rather than leaving it open.

Setup, workflow, and handoff skills may coordinate state; they do not acquire ownership of the artifacts they route.

## Read protocol

Before acting, a memory-aware skill reads only the relevant surfaces:

1. Read `docs/agents/memory.md`.
2. Read the Human-layer documents that carry terminology, constraints, and decisions at the paths the memory config names.
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

### Human layer — WHY only

Tracked in git. Documents decisions, constraints, terminology, and product intent — things code cannot show.

| Content | Owned by | Other skills |
| --- | --- | --- |
| Memory configuration and routing | the setup skill that wrote it | Read; repair factual drift only |
| Terminology and bounded-context language | whichever skill authors terminology, else the user | Consume; propose changes through the owner |
| Decisions with rationale | whichever skill authors decisions, else the user | Consume; propose changes through the owner |
| Reader-relevant change history | whichever workflow owns the existing changelog or release history, else the user | Add a concise outcome and pointers; omit execution narrative |
| Product intent, problem framing, scope | whichever skill authors product docs, else the user | Consume; never rewrite the intent |

Ownership is a rule about *who edits*, not about filenames. Whatever path the repository already uses for a kind of content is that content's canonical home; a skill that consumes it proposes changes rather than editing in place.

**What does not belong here** — anything an agent can derive from code, manifests, configuration, or an index. Current structure, coding patterns, dependency lists, and descriptions of how something works all fail the source test, however well written.

### Code Index layer — WHAT/HOW (optional)

Rebuildable from source, so it is never the origin of a fact. It answers where code lives and what connects to what, letting an agent skip repeated search.

The index is owned by whatever tool built it. Consumers query it and request a refresh when it is stale; they do not hand-edit index output, and they confirm a query result against source before acting on it.

**When to enable:** only when the repository is large enough that repeated source search costs materially more than querying an index. Tool choice is the user's; a repository that already has an index keeps it.

### Working layer — NOW

Under the configured work root, git-ignored. Discarded with the effort. The `Promotes` column names the durable fact the artifact contributes upward; `none` means the artifact is consumed downstream and then dies with the effort.

| Kind of artifact | Owned by | Promotes |
| --- | --- | --- |
| The effort's routing hub — status, next action, blockers, pointers | whichever skill currently coordinates the effort | none; it routes rather than stores |
| Append-only session log | every participating skill appends | none; history is never rewritten |
| Discovery and exploration notes | the skill that produced them | the durable framing or constraint they settle |
| Prototype and experiment records | the skill that ran them | the decision the experiment settled |
| Implementation specs, plans, and task claims | the skill executing that stage | a lasting design choice, if the work produced one |
| Diagnosis and investigation notes | the skill that investigated | a rule worth enforcing beyond this fix |
| Generated views | the generator | none; regenerate rather than hand-edit |
| Handoffs | the skill that closed the session | none; successors follow the pointers to source |

Two rules make this table usable without knowing which skills a repository has installed. First, the owner of an artifact is whichever skill wrote it, and other participants update only the fields that carry their own transition. Second, an artifact appears in exactly one layer table: when its layer is unclear, apply the durability test rather than writing it to both.

Implementation specs deserve a note, because they split. A step-by-step plan for building something is working memory and dies with the effort. The design choice that plan encodes — the trade-off someone would otherwise re-litigate — is a WHY fact and promotes. A noteworthy shipped result may become one changelog entry. Both records point to canonical evidence; neither preserves the completed plan.

## Working-memory shape

```text
<work-root>/<effort>/
├── state.md           ← routing hub; routes, does not store
├── progress.md        ← append-only session log
├── specs/             ← earned on first multi-ticket initiative
│   └── NNN-slug.md    ← one file per design initiative
├── tasks/             ← one file per atomic work item
│   └── NNN-slug.md
├── discovery/
│   ├── brainstorm.md
│   ├── demand.md
│   ├── solution.md
│   ├── mvp.md
│   └── premortem.md
├── research/          ← optional: spikes
├── prototypes/
├── handoffs/
├── diagnosis.md
└── roadmap.html       ← generated by scripts/gen-roadmap.py; never edit directly
```

Create only artifacts earned by the workflow. `specs/` is not scaffolded — create it on the first multi-ticket initiative. Use the branch name as the `<effort>` slug when one exists.

Note what is *not* here: `prd.md`. Product intent is Human-layer and lives at `<product-docs>/<slug>/prd.md` — the discovery files above are the surface it is drafted on, not its home.

Engineering feature artifacts that an established workflow tracks elsewhere are referenced from `state.md`; working memory does not duplicate them. Tracking does not make them permanent: after implementation, apply completion compaction to tracked specs, plans, and task files too.

## Product-docs shape

```text
docs/product/          ← `<product-docs>`, default `docs/product/`
└── <slug>/
    └── prd.md
```

`<slug>` names the product for a greenfield effort and the feature for an incremental one. It matches the effort slug when one exists, so a reader can trace a PRD back to the discovery that produced it — and forward from `state.md` to the intent it serves.

## Concurrency

A task file (`tasks/NNN-slug.md`) must declare `state:` and `claimed_by:` before any agent touches its implementation. Write `claimed_by: <agent-id>` and advance `state` to `claimed` before modifying anything. A claim is exclusive until the task reaches `done` or `abandoned`. `depends_on:` lists the IDs of tasks that must be `done` before this task can reach `ready`. The only path to `done` is a passing `verify:` command — never advance state directly from `review` to `done` without it.
