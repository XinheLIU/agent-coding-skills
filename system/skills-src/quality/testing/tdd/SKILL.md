---
name: tdd
description: "Use when executing implementation tasks with TDD discipline. Triggered by: /tdd, or when user says 'execute with TDD', 'run tasks with TDD', 'implement with tests', or asks to execute a plan with testing. Follows red-green-refactor for every task. Parallelizes independent tasks via subagents when available — degrades gracefully to sequential when not. Blends into existing task lists."
---

Last updated: 2026-09-08

# TDD Execution

Execute implementation tasks with strict test-driven development. Independent tasks run in parallel waves when subagents are available; degrade to sequential when not. Progress is tracked in a living plan document.

**Core invariant:** Every behavior gets a test written before its implementation. No exceptions.

---

## Phase 0 — Discovery

### 0a. Find tasks

Check in order:
1. `TaskList()` — are there tasks in the current session?
2. Plan files in project (`docs/plans/*.md`, `.claude/plans/*.md`, user-specified)
3. If neither: ask the user what to execute

If tasks exist in the session, blend TDD into them — do not start over.

### 0b. Extract all task text upfront

Read every task's full description now. Subagents and sequential execution both need complete context — never make any executor read the plan file itself.

### 0c. Detect subagent capability

Ask yourself: am I in an environment that supports the `Agent` tool with subagent dispatch?

- **Yes (subagents available):** use parallel dispatch for independent tasks
- **No (agent-agnostic mode):** execute all tasks sequentially yourself, self-review with checklist

The rest of this skill uses "executor" to mean either a dispatched subagent or yourself in sequential mode.

### 0d. Analyze dependencies and build waves

Group tasks into **execution waves** — tasks within a wave have no dependencies on each other:

```
Wave 1: [A, B, C]   ← all independent
Wave 2: [D]         ← depends on A, B
Wave 3: [E, F]      ← both depend on D
```

**Parallelization signal:**
- Independent modules/directories → parallel
- Explicit `depends on` markers → sequential
- Same file touched → sequential within that file's scope
- Schema migrations → always serial, always before their dependents
- Uncertain → be conservative, make it sequential

---

## Phase 1 — Create the Execution Plan Document

Before executing anything, create (or update) this file in the project:

```
docs/plans/tdd-execution-plan.md
```

Use the format below. This document is the source of truth for progress.

```markdown
# TDD Execution Plan
Last updated: [date]

## Overview
- Total tasks: N  |  Done: 0 / N

## Wave 1 — Parallel (N tasks)
- [ ] Task A: [name] — [one-line summary]
- [ ] Task B: [name] — [one-line summary]

## Wave 2 — Sequential (depends on Wave 1)
- [ ] Task C: [name]

## Blockers & Notes
(updated during execution)
```

Status: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked

Update this file after every task completes (flip `[ ]` → `[x]`, update date and counts).

---

## Phase 2 — Execute Wave by Wave

For each wave:

### 2a. Dispatch executors

**Subagent mode (parallel within wave):**
Dispatch all tasks in the wave simultaneously (single message, multiple `Agent` tool calls). Each subagent receives:
- Full task text (pasted inline, not a file reference)
- Scene-setting context (what this fits into, dependencies, what to avoid touching)
- TDD requirements (see below)
- Working directory + files to leave untouched (to avoid conflicts)

**Sequential mode (no subagents):**
Execute tasks one at a time yourself. Apply the same TDD requirements.

### 2b. TDD requirements — given to every executor

```
## TDD Requirements (MANDATORY — Iron Law)

Follow red-green-refactor for every behavior:

1. RED: Write ONE failing test that names the behavior precisely.
2. Verify RED: Run it. Confirm it fails because the feature is missing, not a typo.
3. GREEN: Write the minimal code to pass. Nothing extra.
4. Verify GREEN: Run all tests. Target passes; nothing else broke.
5. REFACTOR: Clean structure only. Stay green.
6. Repeat for the next behavior.

Iron Law: no production code before a failing test.
Wrote code first? Delete it. Start over from the test.

Anti-patterns to reject:
- Test passes immediately (proves nothing — fix the test)
- Testing mock existence instead of real behavior
- Test-only methods in production classes (put them in test utilities)
- Mocking without understanding what the mock removes
- Incomplete mocks (mirror the full real structure)
```

### 2c. Handle executor status

| Status | Action |
|--------|--------|
| Done | Proceed to review |
| Done with concerns | Read concerns first. Correctness doubts → resolve before review. Observations → note and proceed. |
| Needs context | Provide the missing context. Re-dispatch or continue yourself. |
| Blocked | Provide context and retry; if still stuck, upgrade to more capable model or break the task smaller; escalate to user if plan itself is wrong. |

### 2d. Review

**Per-task executor self-check** (every executor, before reporting):
- Every spec requirement implemented; nothing extra built (no YAGNI violations)?
- Tests written first and test real behavior, not mock behavior?
- Names precise, no dead code, everything typed?
- Full suite green?

**Full reviews are owned by the review skills, not embedded here.** After a wave that changed risky or cross-cutting code — and always at plan completion (Phase 3) — run `review-implementation-gaps` against the plan doc (spec compliance: COMPLETE / PARTIAL / MISSING / DIVERGENT per task), then `review-code-quality` Mode A on the accumulated diff (code quality on the Standards + Spec axes, with a merge verdict). Fix Criticals before starting the next wave.

### 2e. Mark progress

After the self-check passes (and any routed-review Criticals are fixed):
- Update `tdd-execution-plan.md`: flip `[~]` → `[x]`, update counts, update date
- If using `TaskUpdate`: mark the session task complete
- Add any notable notes to Blockers & Notes

### 2f. Next wave

Only start Wave N+1 after Wave N is 100% `[x]`.

---

## Phase 3 — Final Review

After all waves complete, run the review chain — this is the mandatory invocation point:

1. All tasks `[x]` in the plan doc?
2. Run `review-implementation-gaps` against the plan doc — every task COMPLETE?
3. Run `review-code-quality` Mode A on the accumulated diff — verdict READY or READY-WITH-FIXES?
4. Full test suite passing? Any open concerns from executors?

Fix Criticals, then update plan doc: `Status: Complete`. Report to user.

---

## Subagent Prompt Templates

Key rules for executor prompts:
- Paste full task text inline — subagents must never read the plan file
- Include scene-setting context (where this fits, what not to touch)
- Include the TDD requirements block above verbatim
- Ask them to raise questions before starting work
- Escalation triggers: stop and report BLOCKED or NEEDS_CONTEXT if the task needs architectural decisions not in the spec, or after >10 minutes of reading without progress — bad work is worse than no work
- Required report shape: Status (DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT), tests written and results (N/N passing), files changed, concerns if any

---

## Model Selection (Subagent Mode)

| Role | Model |
|------|-------|
| Isolated task, 1-2 files, complete spec | haiku |
| Multi-file, integration concerns | sonnet |
| Architecture, review, debugging | opus |

---

## Red Flags — Stop and Reassess

- Executor wrote code before tests → require restart with TDD from scratch
- Test passes immediately without implementation → test is wrong, fix before proceeding
- Parallel tasks both modified the same file → merge carefully, check for conflicts
- Routed review reports the same issue twice → escalate to user; something is systematically wrong
- More than 3 fix-and-re-review loops on one task's routed-review findings → escalate to user

---

## Integration with Existing Task Lists

If the session already has a `TaskCreate`/`TaskUpdate` task list:
- Read it with `TaskList`, do NOT create a new one
- Map existing tasks to waves based on dependency analysis
- Mark progress with `TaskUpdate` as tasks complete
- Also create `tdd-execution-plan.md` — it persists across sessions; `TaskUpdate` is session-only

---

## Limitations

- Stop and ask if the plan has no clear task boundaries
- Stop and ask if dependency analysis is ambiguous
- Escalate if an executor is stuck after 2 retries
- This skill does not set up git worktrees — do that separately if needed
