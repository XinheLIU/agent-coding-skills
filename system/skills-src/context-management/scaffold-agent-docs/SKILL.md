---
name: scaffold-agent-docs
description: Own the core Human documentation structure — create it from scratch for new repos, or audit and repair it for repos where docs exist but have drifted. Mode A (init) scaffolds AGENTS.md and docs/ from templates and fills them from the code. Mode B (update) inventories existing docs, verifies claims against live code, classifies each doc, and applies structural repairs. Content gaps that require deeper doc generation are flagged for manage-context to delegate. Run manage-context first if the repo has no memory routing.
---

# Scaffold Agent Docs

Last updated: 2026-08-05

Owner of the Human documentation layer's initial structure and ongoing structural health — the git-tracked, people-facing layer of the context-management collection.

**What the agent cannot see does not exist.** Architecture decisions, conventions, and technology choices only count once they live in a file. This skill writes them down, keeps `AGENTS.md` small enough to stay read, and keeps existing docs honest.

## Phase 0 — Mode detection

Run before anything else.

```
Does AGENTS.md (or CLAUDE.md) exist?
  No  →  Mode A (Init): scaffold structure, then fill from code
  Yes →  Mode B (Update): audit existing docs, repair structure
```

If routing is absent (`docs/agents/memory.md` missing), run or recommend `manage-context` (Phase A) before writing persistent state.

---

## Mode A — Init

For repos with no Human-layer docs. Two sub-phases: scaffold, then fill.

### Phase 1 — Scan, then scaffold

Read before writing: root structure two levels deep, the package manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), existing `*.md` and `docs/`, and the README. Reuse what exists — never duplicate a doc that is already correct.

Structure comes from [`references/templates/`](references/templates/README.md) shipped with this skill — one template per file. Read the template before writing its target, replace every `{{placeholder}}`, and strip the HTML guidance comments. Delete sections the project has not earned rather than leaving them empty.

Create only what the repo earns:

```text
AGENTS.md                    ← index file, under 200 lines
docs/
├── ARCHITECTURE.md          ← module boundaries, dependency direction
├── CONVENTIONS.md           ← naming rules, code style
├── TECH_DECISIONS.md        ← why each technology was chosen
├── QUALITY.md               ← acceptance criteria, definition of done
└── exec-plans/
    ├── active/.gitkeep      ← in-progress plans
    ├── completed/.gitkeep   ← finished plans
    ├── backlog.md           ← known but unscheduled work
    └── tech-debt-tracker.md ← known technical debt
```

Add `design-docs/`, `product-specs/`, or `references/` only when there is real material for them. For a repo large enough to need finer separation, see the canonical `/docs` layout in [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md).

`AGENTS.md` is an index, not an encyclopedia. It carries: what the project is in a few sentences; the tech stack, entry point, start command, and test command as literal commands; a table mapping "I want to know X" to the file that answers it; the working rules; and the genuine prohibitions. Everything else is a link.

### Phase 2 — Fill with what the code actually says

Before writing a word, be able to answer: which modules exist and what each is for, what the call chain looks like, which libraries matter, what the naming patterns are, and what makes a test fail.

**Verify every relationship claim with a grep.** Before writing "A uses B" or "page X includes component Y", confirm the import exists. Same directory is not evidence. No import found means no relationship — mark it `[VERIFY: no import found, confirm manually]` rather than asserting it.

What each file gets:

- **ARCHITECTURE.md** — module responsibilities, dependency direction rules, the one or two core data flows. Every constraint carries its reason; "keep clean layering" is not a constraint.
- **CONVENTIONS.md** — patterns induced from the code, each with an observed example. Where the codebase is inconsistent, say so and propose the target. Never invent a convention the code does not follow.
- **TECH_DECISIONS.md** — the main frameworks and libraries, what each is for, and why it was chosen. This is the hardest file because the reasons are rarely in the code. Infer what is inferable; mark the rest `待补充 / TO BE ADDED` rather than fabricating rationale.
- **QUALITY.md** — the definition of done, the review checklist, test requirements. Include the project-specific checks, not generic advice.
- **backlog.md** — known-but-unscheduled features. Ask the user; this is rarely derivable. Distinct from tech debt: backlog is *not yet built*, debt is *built badly*.
- **tech-debt-tracker.md** — duplicated logic, inconsistent naming, TODO/FIXME comments, oversized files, untested core modules. Write what you found honestly; an empty list with "to be discovered" beats invented debt.

### Mode A verify

- `AGENTS.md` under 200 lines, with literal commands rather than "see docs".
- Every path in the index table resolves to a file that exists.
- No empty placeholder sections.
- Every unverifiable claim marked, not guessed.

### Mode A report

List what was created, what was inferred from the scan and needs human confirmation, and the collected `待补充 / TO BE ADDED` items as one checklist — that list is the most useful part of the output.

Then point onward — this skill owns the core `AGENTS.md` + `docs/` structure, not the whole Human layer:

| Still missing | Run |
| --- | --- |
| Root `README.md` | `create-readme` |
| Agent-behavior rules and coding conventions | `extract-rules` |
| Architecture, data-model, or API docs | `document-codebase` |
| A queryable code map | `index-codebase` |
| Layers have started to drift | `manage-context` (Phase B) |

Do not commit.

---

## Mode B — Update

For repos where docs exist but may have drifted. Audit first, repair after confirmation.

### Step 1 — Read routing and scope

Read `docs/agents/memory.md`. Resolve the Human, Wiki, and Working roots. Classify every candidate path by layer before inspecting it. Organize only tracked, people-facing Human documentation — never Wiki indexes, Working artifacts, or runtime skill/agent trees.

### Step 2 — Inventory

List all in-scope Human-layer docs: path, approximate line count, apparent role.

In scope: `README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/`, architecture notes, API docs, runbooks, specs, module READMEs.

Out of scope: skill/agent/prompt trees, vendored, generated, cache, and build-output directories.

### Step 3 — Verify claims against live code

For every doc that survives:

- **Paths and commands** — check they resolve and still work.
- **Relationships** — grep before asserting "A uses B". No import found → mark `[VERIFY]`, not a stated fact.
- **Tech stack** — cross-check against the package manifest.
- **Index table links** — every entry in `AGENTS.md` must point to a file that exists.

Verify against code, never against another doc. When code and a doc disagree, the code wins — unless the doc records an intended constraint the code violates. That is a defect, not drift; report it as one.

### Step 4 — Classify and report

Classify each doc as `KEEP`, `UPDATE`, `MOVE`, `MERGE`, or `DELETE`.

Present the audit report before touching anything:

```text
## Scaffold Agent Docs — Audit Report

### Inventory
| # | File | Lines | Role | Status |
| --- | ---- | ----- | ---- | ------ |

### Accuracy Issues
| # | File | Claim | Actual | Fix |
| --- | ---- | ----- | ------ | --- |

### Structural Issues
| # | Topic | Files | Problem | Action |
| --- | ----- | ----- | ------- | ------ |

### Content Gaps (flagged for manage-context)
| # | Surface | What's missing | Owning skill |
| --- | ------- | -------------- | ------------ |

### Proposed Actions (ordered)
1. UPDATE: <file> — <reason>
2. MOVE: <file> -> <target> — <reason>
```

Ask: **"Apply structural repairs? (yes / yes but skip #N,M / no)"**

### Step 5 — Apply repairs

After confirmation:

- Fix wrong paths, broken links, renamed commands.
- Apply `MOVE` and `MERGE` actions.
- Update `Last updated:` on every touched file.
- Repair cross-layer pointers in moved docs.
- Do NOT rewrite content owned by other skills (ADR decisions, wiki index, working memory).

Never edit `docs/agents/memory.md`. Never delete unique rationale silently — relocate or archive it.

### Step 6 — Flag content gaps, do not fill them

Content that requires deeper doc generation (stale architecture diagrams, missing API reference, outdated data model, README, agent-behavior rules) is out of scope for this skill. List those gaps in the report under "Content Gaps" with the owning skill (`document-codebase`, `create-readme`, `extract-rules`, `review-agent-instructions`). `manage-context` Phase B is the orchestrator that will invoke those skills — this skill only identifies the gaps and reports them.

### Mode B report

State what was fixed directly, what structural changes were made, and what content gaps were flagged. Point to `manage-context` (Phase B) for cross-layer reconciliation.

Do not commit.
