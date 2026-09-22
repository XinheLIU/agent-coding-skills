# Testing Workflow

Last updated: 2026-09-17

```text
codebase-design identifies the public seam
  → acs-tdd runs one red/green behavior slice
  → project checks verify the integrated change
  → acs-review-code-quality checks standards and spec fidelity
  → acs-analyze-test-gaps audits critical behavior coverage
```

Tests observe behavior through agreed public seams and canonical acceptance criteria. Use [engineering context](../skills-src/craft/context/acs-init-context/references/engineering-memory.md): retain criterion → test/evidence → revision mappings, environment assumptions, failures, skips, omissions, and scoped readiness. Planning/raw output is Run Context; final evidence is Change Context. Canonical ticket status stays in its tracker.

The [coordinator](context-coordination.md) records evidence and propagates scoped freshness; Testing determines its meaning. Missing criteria block readiness claims while independent baseline analysis can continue. Changed code/contracts/environment require affected checks to be reassessed.
