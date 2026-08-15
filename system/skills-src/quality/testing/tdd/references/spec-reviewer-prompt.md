# Spec Compliance Reviewer Prompt Template

Last updated: 2026-08-02

Dispatch AFTER implementer reports DONE. Verify spec completeness before code quality.

```
Task tool (general-purpose):
  description: "Spec review: [task name]"
  model: sonnet
  prompt: |
    You are reviewing spec compliance for: [task name]

    ## Original Task Spec

    [FULL TEXT of original task — paste verbatim]

    ## What Was Implemented

    [Implementer's summary of what was done]

    ## Files Changed

    [List of files the implementer changed, with git SHAs or descriptions]

    ## Your Job

    Read the changed files. Compare against the spec. Answer these questions:

    **Completeness (built everything required?):**
    - Is every requirement from the spec implemented?
    - Are all acceptance criteria met?
    - Are edge cases and error paths covered?

    **Scope (built only what was required?):**
    - Was anything added that wasn't in the spec? (YAGNI violations)
    - Are there extra methods, flags, or options not requested?

    **TDD compliance:**
    - Does a test exist for every behavior?
    - Do the tests test real behavior (not mock behavior or mock existence)?
    - Are there any test-only methods added to production classes?

    ## Output Format

    **PASS** or **FAIL**

    If FAIL, list specific issues:
    - Missing: [what requirement is missing]
    - Extra: [what was added beyond spec]
    - TDD: [what test is missing or tests wrong thing]

    Be precise. The implementer will fix based on your list.
    "Looks fine" is not acceptable — name specific lines or behaviors.
```
