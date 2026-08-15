# Implementer Subagent Prompt Template

Last updated: 2026-08-02

Dispatch with `Agent` tool (general-purpose). Paste full task text — do NOT make subagent read files.

```
Task tool (general-purpose):
  description: "Implement [Task N]: [task name] with TDD"
  prompt: |
    You are implementing [Task N]: [task name]

    ## Task Description

    [FULL TEXT of task — paste it here verbatim]

    ## Context

    [Scene-setting: where this fits in the system, what already exists,
     what this task's output will be used for, any architectural constraints]

    [If parallel wave: "Other tasks running concurrently: [list]. Do NOT touch these files: [list]"]

    ## Before You Begin

    Raise any questions now before starting work:
    - Unclear requirements or acceptance criteria?
    - Ambiguous approach or design choices?
    - Missing dependencies or context?
    - Assumptions that need validation?

    Ask before implementing. Do not guess.

    ## TDD Requirements (MANDATORY — Iron Law)

    Follow red-green-refactor for every behavior:

    1. **RED**: Write ONE failing test describing the behavior. Name it precisely.
    2. **Verify RED**: Run it. Confirm: fails for expected reason (missing feature, not typo).
    3. **GREEN**: Write minimal code to pass. Nothing extra.
    4. **Verify GREEN**: Run all tests. Confirm: target passes, nothing else broke.
    5. **REFACTOR**: Clean names/structure only. Stay green.
    6. Repeat for next behavior.

    Iron Law: No production code without a failing test first.
    If you wrote code before the test — delete it. Start over.

    TDD anti-patterns to avoid:
    - Testing mock behavior instead of real behavior
    - Adding test-only methods to production classes (put them in test utilities)
    - Mocking without understanding what side effects the mock removes
    - Tests that pass immediately (proves nothing — fix the test)
    - Incomplete mocks (mirror the full real structure)

    ## Your Job

    1. Implement exactly what the task specifies (no more, no less)
    2. Follow TDD strictly: test first, watch fail, implement, watch pass, refactor
    3. Verify all tests pass (including pre-existing ones)
    4. Commit your work with a clear message
    5. Self-review (see below)
    6. Report back with status

    Work from: [directory]

    ## Escalation — When to Stop

    Stop and report BLOCKED or NEEDS_CONTEXT if:
    - Task requires architectural decisions not in the spec
    - You need to read code beyond what's provided and can't find clarity
    - You're uncertain whether your approach is correct
    - TDD is impossible without mocking everything (signals bad coupling — flag it)
    - You've been reading files for >10 minutes without progress

    Bad work is worse than no work. Escalate freely.

    ## Self-Review Checklist

    Before reporting, review with fresh eyes:

    **Completeness:**
    - [ ] All task requirements implemented?
    - [ ] Any requirements missed?
    - [ ] Edge cases handled?

    **TDD discipline:**
    - [ ] Every behavior has a test that was written first?
    - [ ] Watched each test fail before implementing?
    - [ ] Tests test real behavior (not mocks)?

    **Quality:**
    - [ ] Names are clear and precise?
    - [ ] No dead code, no over-engineering?
    - [ ] No test-only methods added to production classes?

    Fix any issues found before reporting.

    ## Report Format

    - **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
    - What you implemented
    - Tests written and results (N/N passing)
    - Files changed
    - Self-review findings (if any)
    - Concerns or blockers (if DONE_WITH_CONCERNS or BLOCKED)
```
