---
name: spec
description: Start a new feature by creating a git worktree, feature branch, and spec.md (user stories, functional requirements, success criteria). Use when the user wants to kick off a new feature from a description. Folds a short clarify Q&A inline to resolve ambiguities.
---

Last updated: 2026-08-17

# /spec — Start a new feature

Turn a short feature description into a worktree + `specs/NNN-<short-name>/spec.md`. This is the first step of the spec-driven workflow (`/spec` → `/plan` → `/tasks`).

## When to use

Invoke this skill when the user:

- Says "add a new feature", "start a feature", "let's build X", or gives a feature pitch.
- Runs `/spec <description>`.

Do NOT use this skill for bug fixes, refactors, or edits to an existing feature.

## Inputs

- **Required**: a natural-language feature description (user message or `$ARGUMENTS`).
- **Optional**: the effort PRD — `docs/product/<slug>/prd.md`, found via `state.md` or named by the user. Read Part 1 (user story, requirement list, scope) and Part 3 (five-state specs, edge cases); derive user stories, FRs, and success criteria from them instead of re-deriving, and cite the PRD path in **Input**.
- **Optional**: design artifacts — resolved `map.md` decisions (`wayfinder`), `docs/design/system.md` and root `DESIGN.md` (the `design/ux` pipeline — see `workflows/design.md`), glossary and ADRs (`domain-modeling`), architecture docs. Treat them as constraints and terminology sources; implementation detail they contain still stays out of `spec.md` — it belongs to `plan.md`.
- **Implicit**: current working directory must be inside a git repository.

## Outputs

- A new worktree at `<repo-parent>/<repo-name>.worktrees/NNN-<short-name>/` on branch `NNN-<short-name>`.
- `specs/NNN-<short-name>/spec.md` inside the worktree, derived from `references/spec-template.md`.
- Session is switched into the worktree (via `EnterWorktree path=...`) so follow-on commands run there.

## Prerequisites check

Run at the start. If any fails, stop and tell the user.

1. `git rev-parse --git-dir` succeeds (we are in a git repo).
2. The feature description is non-empty. If empty, ask the user for it.
3. Working tree state is clean enough that creating a new worktree is safe. (Worktrees don't touch the current tree, so uncommitted changes are fine — just note them in the report.)

## Workflow

### Step 1 — Derive the short name

From the description, pick **2–4 kebab-case words** that capture the feature. Examples:
- "Add a pomodoro timer CLI with session history" → `pomodoro-timer`
- "Let users reset their password via email" → `password-reset-email`

Keep it short and content-bearing. Avoid articles ("the", "a") and generic words ("feature", "system").

### Step 2 — Pick the feature number

- Resolve repo root: `git rev-parse --show-toplevel`.
- If `<repo-root>/specs/` does not exist, pick `001`.
- Otherwise scan for existing `NNN-*` subdirectories, find the max `NNN`, and use `max + 1`, zero-padded to 3 digits.

The resulting identifier is `NNN-<short-name>` (e.g., `003-pomodoro-timer`). This is used for BOTH the branch name and the spec directory.

### Step 3 — Create the worktree and branch

- Worktree path: `<repo-parent>/<repo-name>.worktrees/NNN-<short-name>/`
  - `<repo-name>` = basename of repo root.
  - `<repo-parent>` = parent of repo root.
- Run: `git worktree add -b NNN-<short-name> <worktree-path>`
- Switch the session into the worktree using the `EnterWorktree` tool with `path=<worktree-path>`. (EnterWorktree accepts `path` for an existing worktree that already appears in `git worktree list`.)

All subsequent file operations use absolute paths inside the worktree.

**Initialize working memory for this effort.** Immediately after switching into the worktree:

- Confirm `.scratch/` is in `.gitignore`. If not, add the rule.
- Create `.scratch/NNN-<short-name>/state.md`:

```markdown
# NNN-<short-name> — State

Last updated: YYYY-MM-DD

## Status
Spec in progress.

## Next action
Finish and approve spec.md, then run /plan.

## Blockers
none

## Pointers
- Spec: `specs/NNN-<short-name>/spec.md`
- Plan: (pending /plan)
- Tasks: (pending /tasks)
- Progress: `.scratch/NNN-<short-name>/progress.md`
```

This is the working memory anchor for the effort. Every subsequent skill (`/plan`, `/tasks`, `handoff`) updates this file in place rather than creating a new one.

### Step 4 — Create the feature directory

`mkdir -p <worktree>/specs/NNN-<short-name>/`

### Step 5 — Draft `spec.md`

Read `references/spec-template.md` (in this skill directory) and fill in every placeholder. Write the result to `<worktree>/specs/NNN-<short-name>/spec.md`.

Content rules:

- **User Stories**: prioritized P1 → P2 → P3. Each MUST be independently testable (implementing only P1 must still ship a viable MVP). Give each story a title, a "Why this priority" line, an "Independent Test" line, and at least one Given/When/Then acceptance scenario.
- **Functional Requirements** (`FR-001`, `FR-002`, …): each MUST be testable and unambiguous. Use MUST/SHOULD language. If something genuinely cannot be determined from the description, mark it `[NEEDS CLARIFICATION: <question>]` — these become questions in Step 6.
- **Key Entities**: include only if the feature is data-bearing. List entity name, what it represents, key attributes (no implementation types).
- **Success Criteria** (`SC-001`, …): measurable, technology-agnostic, user- or business-outcome-oriented ("complete signup in under 2 minutes", "reduce support tickets by 50%"). No implementation language.
- **Edge Cases**: boundary conditions, error scenarios.
- **Assumptions**: anything you inferred because the description did not say.

Never put implementation choices (framework, database, API shape) in `spec.md`. Those belong in `plan.md`.

Set:
- `**Feature Branch**: NNN-<short-name>`
- `**Created**: YYYY-MM-DD` (today's date)
- `**Status**: Draft`
- `**Input**: User description: "<original description>"`

### Step 6 — Inline clarify pass

Scan the draft for `[NEEDS CLARIFICATION: …]` markers and for any remaining genuine ambiguities across these axes:

- Functional scope, domain/data model, UX flow, NFRs, integrations, edge cases, terminology.

Pick **up to 3** of the highest-impact questions. If there are fewer real ambiguities, ask fewer. **Do not invent questions** just to hit the cap. A question the PRD or a design artifact already answers is not an ambiguity; apply the answer and do not re-ask.

Ask them in a single `AskUserQuestion` call (multi-question), with the recommended option listed first and labeled `(Recommended)` where you have a strong default. For open-ended answers, offer 2–3 concrete options and allow "Other".

After the user answers:

1. Add a `## Clarifications` section at the end of the spec (if not already present) with a `### Session YYYY-MM-DD` subsection.
2. Append one bullet per Q/A: `- Q: <question> → A: <answer>`
3. Apply each answer to the relevant spec sections (FRs, user stories, success criteria, edge cases, assumptions) — update in place, do not duplicate.
4. Remove the corresponding `[NEEDS CLARIFICATION: …]` marker.

### Step 7 — Validate

Before finishing, check:

- No remaining `[NEEDS CLARIFICATION: …]` markers.
- Every mandatory section is present and filled (User Scenarios, Requirements, Success Criteria).
- No implementation details (language, framework, DB, HTTP verbs, file paths) appear in requirements or success criteria.
- Every FR is independently testable.
- Every SC is measurable (has a number or a clear pass/fail signal).
- Every user story has at least one Given/When/Then acceptance scenario.

If any check fails, fix the spec and re-validate. At most 2 fix iterations — if still failing, report what could not be resolved and stop.

### Step 8 — Report

Output a concise summary to the user:

- Branch created: `NNN-<short-name>`
- Worktree path
- Spec path
- Working memory: `.scratch/NNN-<short-name>/state.md` created
- User story count by priority
- FR count, SC count
- Any assumptions the user should confirm
- Suggested next command: `/plan`

## Non-goals

- Do NOT generate `plan.md`, `tasks.md`, research notes, data models, contracts, or checklists. Those belong to later skills.
- Do NOT modify the original (pre-worktree) working tree.
- Do NOT commit or push.

## Template

The spec structure is defined in `references/spec-template.md` in this skill directory. Read it, fill it, write the result. Do not keep the HTML comments from the template in the final `spec.md`.
