---
name: tasks
description: Break a feature spec.md + plan.md into an ordered, phase-organized tasks.md checklist. Use after /plan, when the user is ready to enumerate implementation tasks. Organizes tasks by user-story priority (P1/P2/P3) so each story stays an independently shippable MVP slice.
---

# /tasks — Break the plan into executable tasks

Turn `specs/NNN-<name>/spec.md` + `specs/NNN-<name>/plan.md` into `specs/NNN-<name>/tasks.md`. This is step 3 of the spec-driven workflow (`/spec` → `/plan` → `/tasks`).

## When to use

Invoke this skill when the user:

- Just finished `/plan` and wants to break it into tasks.
- Runs `/tasks` or says "generate tasks", "give me a task list", "break this down".

Do NOT use this skill before `plan.md` exists.

## Inputs

- **Required**: `spec.md` (user stories + priorities) and `plan.md` (tech stack + structure + data model / contracts subsections) for the current feature.
- **Context** (optional): `$ARGUMENTS` — e.g., `"include unit tests"`, `"skip phase 1"`, `"only P1"`.

## Outputs

- `<feature-dir>/tasks.md` — phase-organized checklist.

## Prerequisites check

Resolve `FEATURE_DIR` the same way `/plan` does:

1. `git rev-parse --show-toplevel` → repo root.
2. Try `<repo-root>/specs/<current-branch>/` first.
3. Fall back to scanning `<repo-root>/specs/*/` — if exactly one, use it; if multiple, ask.
4. Confirm both `spec.md` and `plan.md` exist in `FEATURE_DIR`. If `plan.md` is missing, stop and tell the user to run `/plan` first.

## Workflow

### Step 1 — Load context

- Read `spec.md` fully: extract user stories with their priorities (P1, P2, P3, …), functional requirements (FR-###), success criteria (SC-###), edge cases.
- Read `plan.md` fully: extract language, dependencies, project structure, any entities from the Data model subsection, any endpoints/commands/events from the Contracts subsection, any decisions from Research notes.
- Note `$ARGUMENTS`: in particular, is the user opting into tests?

### Step 2 — Decide on tests

Tests are **off by default**. Include test tasks only when **any** of these is true:

- The user's argument explicitly asks for them (e.g., `"with tests"`, `"include unit tests"`).
- `spec.md` says tests are a requirement (e.g., an SC like "95% line coverage" or an FR mandating contract tests).
- `plan.md` Technical Context names a testing framework AND the feature has non-trivial logic.

When tests are on, generate them **per user story**, to be written before the story's implementation.

### Step 3 — Build the task plan

Organize tasks into phases. Use this exact structure — drop phases that don't apply.

**Phase 1: Setup** — project scaffold, deps, tooling. Skip if the feature is a pure addition to an already-scaffolded repo.

**Phase 2: Foundational** — shared infrastructure that must exist before ANY user story can be built (e.g., base models, auth middleware, DB schema, routing). This phase blocks all user stories.

**Phase 3 … N: One phase per user story**, in priority order P1 → P2 → P3 → …
Inside each story phase, order tasks as:
1. Tests (only if tests are on), marked with `[P]` where parallelizable.
2. Models / data structures.
3. Services / business logic.
4. Endpoints, CLI commands, or UI screens.
5. Integration glue (DB wiring, middleware, logging, error handling).

End each story phase with a **Checkpoint** line stating what is now independently testable.

**Phase N+1: Polish & Cross-Cutting** — docs, perf, security hardening, extra unit tests, run the quickstart from `plan.md`.

### Step 4 — Write each task

Every task line **MUST** match this exact format:

```
- [ ] T### [P?] [USn?] <imperative action with exact file path>
```

Rules:

- **T###**: sequential, zero-padded to 3 digits, starting at T001 and continuing monotonically across all phases (don't restart per phase).
- **[P]**: include only when the task touches a different file from every other task in the same phase AND has no within-phase dependencies. If in doubt, omit `[P]`.
- **[USn]**: required inside user-story phases (e.g., `[US1]` for P1 story tasks). Omit in Setup / Foundational / Polish.
- **Description**: imperative verb + what to do + exact file path. Example: `Create User model in src/models/user.ts`.
- No vague tasks ("set things up", "implement feature"). Every task must name a file or a specific, verifiable action.

### Step 5 — Fill dependencies and execution order

At the end of `tasks.md`, add a **Dependencies & Execution Order** section:

- **Phase dependencies**: Setup → Foundational → (all user stories in parallel or in priority order) → Polish.
- **User story dependencies**: each story can start once Foundational is done; stories may optionally layer (e.g., US2 integrates with US1) but must remain independently testable.
- **Within-story order**: tests first (if on) → models → services → endpoints → integration.
- **Parallel opportunities**: list which tasks can run in parallel (same `[P]` marker, different files).
- **Suggested MVP scope**: usually "Complete Setup + Foundational + Phase 3 (US1), then stop and validate."

### Step 6 — Validate format

Before writing the file, check:

- Every task line matches the format exactly.
- Task IDs are unique and sequential.
- Every `[USn]` tag maps to a real user story in `spec.md`.
- No task appears in both Setup/Foundational and a user-story phase.
- Every user story from `spec.md` has at least one task (or is explicitly listed as out of scope with reason).

If any FR or user story is unmapped, either add tasks for it or call it out in a "Coverage gaps" note at the bottom of `tasks.md` so the user sees it.

### Step 7 — Write and report

Write the final content to `<feature-dir>/tasks.md` using `references/tasks-template.md` as the skeleton. Do not keep the template's HTML-style guidance comments.

Report to the user:

- `tasks.md` path
- Total task count
- Task count per user story
- Parallel opportunities (how many `[P]` tasks)
- Tests: on or off (and why)
- Suggested MVP scope
- Ready to implement — next step is to execute the task list (Claude Code will do this directly; no separate `/implement` skill needed).

## Non-goals

- Do NOT start writing source code. Task execution happens after this skill finishes.
- Do NOT commit or push.
- Do NOT modify `spec.md` or `plan.md`.
- Do NOT invent user stories that aren't in `spec.md`.

## Template

Structure is defined in `references/tasks-template.md` in this skill directory. Read it, fill it, write the result.
