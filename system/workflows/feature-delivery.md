# Feature Delivery Workflow

Last updated: 2026-08-10

Use this workflow once intent is approved. The active effort is the shared unit of memory.

```text
<product-docs>/<slug>/prd.md (write-prd), brief.md (brainstorm-feature), or completed map.md (wayfinder)
  → spec.md
  → plan.md                 (missing integrated skill)
  → issues/NN-*.md
  → analyze
  → implement with tdd
  → review-code-quality
  → done
```

When the PRD leaves experience or structure open, the optional `design/` phase runs before `spec` — routing criteria live in the `write-prd` Design Gate and `design/README.md`.

Ticket dependencies are canonical in the issue files. `draw-portfolio-dag` renders them to `roadmap.md` and `roadmap.html`; HTML does not own status.

Each executable issue should be a vertical, independently verifiable slice that fits one fresh session. Work the unblocked frontier. Update `state.md` after every transition and use `handoff` before crossing context windows.
