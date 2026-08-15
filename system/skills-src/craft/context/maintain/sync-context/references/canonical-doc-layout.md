# Canonical Documentation Layout

Last updated: 2026-08-15

Reference for the canonical home of every fact in the three-layer memory model. Load this when:
- **Setting up** — init-context Phase 2a, to scaffold the right structure.
- **Checking drift** — sync-context Job A, to enforce canonical homes and required docs.

---

## Governing principle

One fact, one canonical home. The layer determines permanence; the path within the layer determines the category. When a fact appears in more than one place, the copy in the canonical home wins — the other is drift.

---

## Layer → canonical root

| Layer | Canonical root | Lifetime | Git |
|---|---|---|---|
| Core | `CONTEXT.md`, `docs/adr/` | Project | Tracked |
| Human | `docs/` + root context files | Project | Tracked |
| Wiki | configured in `docs/agents/memory.md` | Rebuildable | Either |
| Working | `.scratch/<effort>/` (or configured work root) | Effort | Ignored |

---

## Human layer — full canonical tree

```text
<repo-root>/
├── README.md                        ← project entrypoint: what + how to run
├── AGENTS.md                        ← agent routing index (under 200 lines)
│   (or CLAUDE.md for Claude-only repos)
├── CONTEXT.md                       ← vocabulary, bounded contexts (Core layer)
├── docs/
│   ├── agents/
│   │   └── memory.md                ← routing config: all four layer paths
│   ├── ARCHITECTURE.md              ← module responsibilities, data flows, dependency rules
│   ├── CONVENTIONS.md               ← coding patterns, naming, induced from code
│   ├── TECH_DECISIONS.md            ← framework/library choices and rationale
│   ├── QUALITY.md                   ← definition of done, test requirements, review checklist
│   ├── adr/                         ← architecture decision records (Core layer)
│   │   └── NNNN-<slug>.md
│   ├── architecture/                ← generated or detailed architecture docs
│   │   ├── entry-points.md
│   │   ├── module-deps.md
│   │   ├── external-deps.md
│   │   ├── data-model.md
│   │   └── *.puml / *.mmd           ← diagram sources
│   ├── product/                     ← product intent
│   │   └── <slug>/
│   │       └── prd.md
│   ├── runbooks/                    ← operational procedures
│   ├── data/                        ← shared data semantics
│   └── exec-plans/
│       ├── active/                  ← .gitkeep; plans live in working layer
│       ├── completed/               ← .gitkeep
│       ├── backlog.md
│       └── tech-debt-tracker.md
```

### Per-file purpose

| File | The one question it answers |
|---|---|
| `README.md` | What is this and how do I run it? |
| `AGENTS.md` | Where do I find X, and what must I know before I edit? |
| `docs/agents/memory.md` | Where is each memory layer, how is it configured? |
| `docs/ARCHITECTURE.md` | What are the modules, how do they depend, and why? |
| `docs/CONVENTIONS.md` | What patterns must I follow, with real examples? |
| `docs/TECH_DECISIONS.md` | What was chosen, what was rejected, and why? |
| `docs/QUALITY.md` | What does "done" mean and what does it take to merge? |
| `CONTEXT.md` | What are the bounded contexts, entities, and ubiquitous language? |
| `docs/adr/NNNN-<slug>.md` | What was decided, when, and why can't it be reversed? |
| `docs/exec-plans/backlog.md` | What is planned but not yet scheduled? |
| `docs/exec-plans/tech-debt-tracker.md` | What known debt exists and how risky is it? |

**`AGENTS.md` invariants (enforced by sync):**
- One-paragraph project description.
- Tech stack as a literal list: language, framework, database, infra.
- `Run:`, `Test:`, `Lint:` as literal runnable commands — no placeholders.
- A "How to find X" routing table; every entry must point to an existing file.
- A `## Startup sequence` section when working memory is enabled.
- Total length: under 200 lines.

---

## Core layer — canonical homes

| Artifact | Canonical path | Owner |
|---|---|---|
| Vocabulary, bounded contexts, ubiquitous language | `CONTEXT.md` | `domain-modeling` |
| Context map (multi-context repos) | `CONTEXT-MAP.md` | `domain-modeling` |
| Architecture decision records | `docs/adr/NNNN-<slug>.md` | `domain-modeling` |

---

## Wiki layer — canonical location

The wiki layer's path is set by `Wiki:` in `docs/agents/memory.md`. Default paths per tool:

| Tool | Default index path |
|---|---|
| codemap | `.codemap/` |
| codegraph | `.codegraph/codegraph.db` |
| graphify | `graphify-out/graph.json` |
| GitNexus | `.gitnexus/` |

**`AGENTS.md` entry invariant:** when wiki is enabled, `AGENTS.md` must contain a `## Code index` section naming the tool, path, query command, and refresh command. Without this entry the index is invisible to agents.

---

## Working layer — canonical structure

Work root: `.scratch/` by default; the `Work root:` value in `docs/agents/memory.md` wins.

```text
.scratch/<effort>/
├── state.md            ← routing hub: Status, Next action, Blockers, Pointers
├── progress.md         ← append-only session log, newest first
├── brief.md            ← optional: effort summary in 1–2 paragraphs
├── discovery/          ← product discovery drafts
│   ├── brainstorm.md
│   ├── demand.md
│   ├── solution.md
│   ├── mvp.md
│   └── premortem.md
├── map.md
├── spec.md
├── plan.md
├── issues/NN-<slug>.md
├── research/
├── prototypes/
├── handoffs/
├── diagnosis.md
├── roadmap.md
└── roadmap.html        ← generated view; do not edit directly
```

**Gitignore invariant:** the work root must appear in `.gitignore` or `.git/info/exclude`. Verify with `git status` — no `.scratch/` files should appear as untracked.

---

## Classification protocol

Used in init-context Phase 2a (scaffold) and sync-context Job A (drift check). Assign one status per in-scope document:

| Status | Meaning | Action |
|---|---|---|
| `OK` | In canonical home, content is current | None |
| `MISSING` | Required doc does not exist at canonical path | Create via owning skill |
| `MOVE` | In wrong location | Move to canonical target path |
| `SPLIT` | Carries both entrypoint + durable content | Retain short local entrypoint; move durable content |
| `MERGE` | Overlaps another doc's ownership | Consolidate into canonical owner |
| `UPDATE` | Canonical home correct; content is stale or wrong | Correct inline (sync-context applies directly) |
| `STRUCTURAL` | Canonical home correct; structure requires owning skill | Flag + dispatch to owning skill |
| `DELETE` | Obsolete, no unique content | Delete after confirming no unique rationale |

Precedence: `MISSING` > `MOVE` > `STRUCTURAL` > `UPDATE` > `OK`.

**Classification tests:**
1. **Layer test** — does this document's content belong to the layer its file is in? Working-memory facts in tracked files are misplaced; tracked decisions in `.scratch/` need promotion.
2. **Ownership test** — does this overlap another doc's single question? Merge into the canonical owner.
3. **Entrypoint test** — is this a short local entrypoint, or durable reference material? Entrypoints stay local; references move under `docs/`.
4. **Size test** — does a module README carry architecture detail that belongs in `docs/ARCHITECTURE.md`? SPLIT.

---

## Structural invariants

Required conditions across all three layers. sync-context enforces them on every full run; init-context enforces them before writing anything.

**Human layer:**
1. `AGENTS.md` (or `CLAUDE.md`) exists at repo root with routing content.
2. `docs/agents/memory.md` exists and specifies work root, issue tracker, wiki status, and human docs root.
3. `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, `docs/TECH_DECISIONS.md`, `docs/QUALITY.md` all exist.
4. `docs/exec-plans/` exists with `backlog.md` and `tech-debt-tracker.md`.
5. `AGENTS.md` is under 200 lines; every path in its routing table resolves to an existing file.

**Wiki layer:**
6. If wiki is enabled: index exists at the configured path; `AGENTS.md` has a `## Code index` section.
7. If wiki is disabled: `docs/agents/memory.md` explicitly states `Wiki: disabled`.

**Working layer:**
8. Work root is gitignored (`.gitignore` or `.git/info/exclude`).
9. Active efforts have a `state.md` whose `## Next action` is specific enough to start work without re-deriving context.

Flag violations as `STRUCTURAL`. sync-context corrects trivial violations directly (fix broken paths, update `Last updated:`); it must invoke `init-context` Phase 2 or 4 for structural creation.

---

## Common misplacement patterns

| Found at | Canonical home | Classification |
|---|---|---|
| Architecture detail in a module README | `docs/ARCHITECTURE.md` | SPLIT |
| ADR embedded in `docs/TECH_DECISIONS.md` | `docs/adr/NNNN-<slug>.md` | MOVE |
| Working-memory facts in tracked docs | Human/Core after promotion | MOVE + promote via owning skill |
| Conventions only in code comments | `docs/CONVENTIONS.md` | MOVE (extract) |
| Multiple files covering the same topic | Single canonical home | MERGE |
| Product intent stuck in `.scratch/` | `docs/product/<slug>/prd.md` | PROMOTE via `write-prd` |
| Runbook sections inside ARCHITECTURE.md | `docs/runbooks/` | SPLIT |
| Missing `## Code index` when wiki is enabled | `AGENTS.md` | STRUCTURAL |
