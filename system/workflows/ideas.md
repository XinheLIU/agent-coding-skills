# Ideas Workflow

Last updated: 2026-08-10

Use this workflow when the problem or product shape is still uncertain. Each stage drafts in working memory; durable conclusions are promoted to the tracked product docs, and domain memory is updated only when vocabulary or a durable trade-off is resolved.

```text
WORKING LAYER — <work-root>/<effort>/, git-ignored, dies with the effort

discovery/ideas.md              (generate-product-ideas, optional entry)
  → discovery/brainstorm.md     (brainstorm — problem framing + JTBD)
  → discovery/demand.md         (validate-demand — evidence + demand type + go/no-go)
  → discovery/solution.md       (shape-solution — user stories as the unit of solution)
  → discovery/mvp.md            (scope-mvp — scenario x product form x data)
  → discovery/premortem.md      (run-premortem, optional)

        │ promote on Green verdict, then again as each stage closes
        ▼

HUMAN LAYER — <product-docs>/<slug>/, git-tracked, outlives the effort

prd.md                          (write-prd — Part 1 at the gate, extended later)
  → design gate                 (write-prd routes: spec directly, design/ux, design/technical, or brainstorm-feature)
```

`ideate-product` is the router over this chain. Invoke it when the entry point is unclear; it reads `state.md`, names the current stage, and delegates. Invoke a stage skill directly when you already know which one you need.

The three questions the chain answers, in order:

1. **Is the demand real?** — `brainstorm` frames the problem and the job; `validate-demand` grades the evidence and kills the idea if it fails.
2. **What is the solution?** — `shape-solution` expresses it as user stories, because a story names actor, job, and outcome in one testable unit.
3. **What is the smallest shippable slice?** — `scope-mvp` resolves scenario x product form x data before cutting scope, since each axis constrains the others.

Start with `generate-product-ideas` only when no candidate has been selected. Skip `run-premortem` for low-stakes efforts; run it when the MVP carries a reputational, migration, or data-integrity risk.

`domain-modeling`, `research`, and `prototype` support any stage. Use `wayfinder` instead of forcing a linear brief when the route is larger than one session; it remains outside the product-ideation category.

Each skill owns one artifact, reads upstream artifacts through `state.md`, and records its downstream transition there. The PRD is product intent, not the implementation spec. The feature-delivery workflow owns the technical handoff; the optional design phase between them is routed by the `write-prd` Design Gate.

## Why the PRD sits in a different layer

Every discovery artifact above is a draft: useful while the effort runs, disposable after it ends. The PRD is not. It answers what the product is for and why it exists — questions that stay open for as long as the code does — so it lives in the tracked product docs rather than the git-ignored work root.

Run `write-prd` twice rather than once. The first run happens the moment `validate-demand` returns Green: it writes Part 1 and marks the rest `Pending`, putting the validated core idea somewhere permanent while it is fresh. The second extends it once scope and risks are settled. An effort abandoned in between still leaves a record of what was considered and why it stopped, instead of a deleted directory.

The test for anything else you are tempted to persist: if the work root were deleted today, would the project have lost a fact it still needs? Yes means it belongs in the PRD or an ADR. No means it did its job in working memory.
