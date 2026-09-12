# Ideas Workflow

Last updated: 2026-09-13
Use this workflow when the problem, product shape, or next increment is uncertain. Product skills enrich shared records rather than passing separate reports down a fixed file chain. Read [the product memory contract](../skills-src/craft/context/init-context/references/product-memory.md) for identity, authority, enrichment, promotion, and legacy inputs.

```text
Greenfield: brainstorm → validate-demand → shape-solution → define-outcomes
Existing:  map-current-product → validate-demand (when value is disputed)
                              → define-outcomes
Either:    run-premortem (when useful) → write-prd → design gate → engineering

Every analysis enriches relevant records in:
  <work-root>/<effort>/discovery.html

Accepted conclusions promote early and incrementally to:
  <product-docs>/<product-slug>/product.html#prd
```

The arrows express reasoning dependencies, not mandatory prior skill executions. Any skill can start from supplied context and create partial memory or enrich existing records. A missing file does not establish a missing answer; evidence and decision quality determine readiness. `ideate-product` diagnoses the earliest unresolved question from the relevant records and routes there.

## Greenfield questions

1. **Is the problem real?** `brainstorm` frames the user, job, struggle, and desired outcome; `validate-demand` grades evidence and assesses the claim.
2. **What could solve it?** `shape-solution` enriches personas, proposed capabilities, journeys, and scenarios without replacing observed facts.
3. **What do we commit to?** `shape-solution` resolves scenario × form × data; `define-outcomes` sets a commitment level and depth for every capability, with exclusions and the basis each rests on.

## Existing-product questions

1. **What exists?** `map-current-product` enriches source-backed current capabilities, gaps, and questions, with inspected coverage and exclusions.
2. **Does the improvement matter?** `validate-demand` adds user evidence and a scoped assessment when value is uncertain.
3. **What changes?** `define-outcomes` links ADDED / MODIFIED / REMOVED behavior, acceptance, metrics, and commitment decisions to the affected capabilities and gaps.

Every stage can raise or answer relevant shared questions and enrich existing gaps with evidence. Match records by subject and context. Keep current behavior, proposed remedies, accepted commitments, and risk hypotheses distinct. An accepted remedy does not close a gap; verified behavior does. If a premise changes, mark materially dependent conclusions for review rather than silently recomputing them.

`run-premortem` enriches shared risks and mitigation proposals for either lane. It can stress-test a supplied plan standalone. Its Mission / Coherence dimension grills whether the committed wedge ever adds up to the product's mission, reading any vision record. It does not turn hypothetical failure into evidence or silently cut scope. `domain-modeling`, `research`, and `prototype` support any stage; link their evidence or decisions to the relevant product records. Use `wayfinder` when the unresolved route spans sessions.

## The vision thread

Demand verdicts are per-claim; the whole-product mission is tracked as a `vision` record in `overview`, inferred until the user confirms it. On the existing-product lane, `map-current-product` synthesizes candidates from implemented story clusters. On the greenfield lane, `validate-demand` may synthesize one from multiple validated claims or a user-stated mission. `run-premortem` stress-tests coherence against it; `write-prd` promotes only user-confirmed visions to `product.html`, linking the open confirmation question otherwise. A vision authorizes no scope and validates no demand.

## Durable intent and the PRD

Run `write-prd` as soon as Green demand establishes durable intent, then again as decisions settle. It reconciles accepted records into `product.html`, preserves essential evidence and rationale, and replaces working conclusions with links. The PRD is a human reading index over those records, not a second independently maintained document. Unresolved questions identify exactly what remains unready.

The [coordinator](context-coordination.md) resolves product/change identity, context, and paths and applies serialized transitions. Increments reuse product identity and canonical ticket/spec/criterion IDs; legacy documents remain canonical until an authorized migration. Skills return affected anchors, consumed revisions, blockers, and next action.

The design gate in `write-prd` routes to UX, technical design, feature brainstorming, or directly to `spec`. Downstream readers follow the configured product path and accepted capability/scope records, including any blocking questions. Execution plans stay in Run Context; accepted requirements/designs and consequential decisions remain Change Context. The same spec is consumed throughout delivery.

Before closing an effort, verify that durable intent remains understandable and its essential links resolve without the effort directory. Serialize shared-file writes and preserve unrelated records throughout.
