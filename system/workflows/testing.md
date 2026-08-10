# Testing Workflow

Last updated: 2026-08-02

```text
codebase-design identifies the public seam
  → tdd runs one red/green behavior slice
  → project checks verify the integrated change
  → review-code-quality checks standards and spec fidelity
  → analyze-test-gaps audits critical behavior coverage
```

Tests observe behavior through agreed public seams. The active effort records testing decisions in `plan.md`; execution status belongs in issue files or `state.md`, not a second competing plan document.
