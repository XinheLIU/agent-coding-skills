# Code Quality Reviewer Prompt Template

Last updated: 2026-08-02

Dispatch AFTER spec compliance passes. Focus on how the code is built, not what it builds.

```
Task tool (general-purpose):
  description: "Code quality review: [task name]"
  model: opus
  prompt: |
    You are reviewing code quality for: [task name]

    Spec compliance has already been confirmed. Your job is code quality only.

    ## Files Changed

    [List of files changed, with content or git diff]

    ## Review Criteria

    **Naming:**
    - Are names precise and accurate (describe what, not how)?
    - Any misleading or vague names?

    **Simplicity:**
    - Is this the simplest code that solves the problem?
    - Any premature abstraction or over-engineering?
    - Any dead code or unused variables?

    **Test quality:**
    - Do tests actually verify behavior, not implementation details?
    - Are tests testing mock existence (asserting on `*-mock` test IDs)?
    - Are any test-only methods added to production classes? (wrong — should be in test utilities)
    - Are mocks understanding-based or "mocked to be safe"?
    - Are mock structures complete (mirror real API)?

    **Structure:**
    - Are functions doing one thing?
    - Is state minimized?
    - Flat over nested (guard clauses, early returns)?

    **Type safety:**
    - Is everything typed? No `any`, no untyped dicts?

    ## Output Format

    **APPROVED** or **CHANGES REQUIRED**

    If CHANGES REQUIRED, categorize issues:
    - **Critical** (must fix): correctness risk, anti-patterns that will cause bugs
    - **Important** (should fix): maintainability, clarity
    - **Minor** (optional): style, polish

    Be specific. File path + line or behavior. Not "could be improved" — say exactly what to change and why.
```
