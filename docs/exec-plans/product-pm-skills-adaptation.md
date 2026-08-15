# Product PM-Skills Adaptation Plan

Last updated: 2026-08-10

Status: Planned. This document records the agreed direction; no implementation is included.

## Objective

Use `references/pm-skills/` as study material to strengthen the product system under
`system/skills-src/product/`, without copying the 68-skill library or introducing a second,
competing workflow taxonomy.

The current product pipeline remains canonical:

```text
brainstorm → validate-demand → design-solution → scope-mvp
  → run-premortem → write-prd → engineering/feature/spec
```

The adaptation should add the missing evidence-to-learning loop around that pipeline.

## Boundaries

- `references/pm-skills/` is read-only source material.
- Extract principles, output contracts, refusal protocols, handoffs, examples, and evaluation
  patterns; do not copy packages into `system/`.
- Preserve the current shared-memory contract: one canonical artifact owner, read-before-write,
  explicit `state.md` handoff, and no silent rewriting of upstream facts.
- Do not duplicate capabilities already owned by `write-prd`, `spec`, `domain-modeling`,
  `prototype`, or `run-premortem`.
- Preserve Apache-2.0 provenance when adapted PM-Skills material materially influences an
  implementation; update `system/THIRD_PARTY_NOTICES.md` as part of that work.

## Priority sequence

### P0 — Governance before library growth

Improve the reliability of the skill library before adding many product skills.

1. Adopt a minimal skill metadata contract for new or substantially revised skills:
   `name`, `description`, `version`, `updated`, `license`, and `category`.
2. Require an output contract for artifact-producing skills. Use a reference template and a
   completed example where the artifact has non-trivial structure.
3. Add trigger, no-trigger, and near-miss evaluation cases for routing-critical skills.
4. Add reciprocal `When NOT to Use` pointers for known collision pairs.
5. Add repository verification for frontmatter, unique names, links, catalog entries, artifact
   ownership, and Markdown update dates.
6. Consider a product-artifact adversarial reviewer covering demand, MVP scope, PRD, hypothesis,
   and experiment-result artifacts.

Reference patterns:

- `references/pm-skills/docs/templates/skill-template/SKILL.md`
- `references/pm-skills/scripts/check-trigger-fixtures.mjs`
- `references/pm-skills/scripts/check-output-eval-assets.mjs`
- `references/pm-skills/scripts/check-reciprocal-boundary-pointers.mjs`
- `references/pm-skills/skills/utility-pm-skill-validate/SKILL.md`

### P1 — Product evidence and learning loop

Add these as new, memory-aware skills with explicit artifact ownership and handoffs:

| Proposed capability | Reference | Proposed artifact | Handoff |
| --- | --- | --- | --- |
| Research synthesis | `discover-interview-synthesis` | `<effort>/research/synthesis.md` | `brainstorm` / `validate-demand` |
| Hypothesis definition | `define-hypothesis` | `<effort>/discovery/hypothesis.md` | experiment design / `scope-mvp` |
| Instrumentation contract | `measure-instrumentation-spec` | `<effort>/measurement/instrumentation.md` | engineering `spec` / `plan` |
| Experiment design | `measure-experiment-design` | `<effort>/measurement/experiment.md` | implementation / launch |
| Experiment results | `measure-experiment-results` | `<effort>/measurement/results.md` | pivot decision / lessons |
| Pivot or persevere | `iterate-pivot-decision` | `<effort>/iteration/pivot.md` | `ideate-product` or stop |
| Durable lessons | `iterate-lessons-log` | `<effort>/lessons/<slug>.md` | future efforts / domain memory when durable |

Minimum quality rules:

- Separate observed evidence, reported evidence, stated interest, and inference.
- Never fabricate quotes, metrics, sample sizes, owners, or experiment results.
- Every hypothesis names its falsifier, success metric, threshold, and cheapest test.
- Instrumentation names event, trigger, properties, identity, deduplication, and data-quality
  expectations.
- Results distinguish evidence from interpretation and include uncertainty and next action.

### P2 — Optional product strategy and communication capabilities

Only add these when real work demonstrates a recurring need:

- `define-opportunity-tree` — first use as an optional `scope-mvp` input; split into a skill only
  when multiple outcomes and opportunities need independent tracking.
- `discover-competitive-analysis` — useful for market entry, differentiation, or lost-deal
  analysis; unnecessary for routine internal features.
- `deliver-launch-checklist` — useful for cross-functional launches with support, legal, rollout,
  rollback, and analytics dependencies.
- `deliver-release-notes` — useful once the system owns a release communication workflow.
- `measure-dashboard-requirements` — add after instrumentation contracts exist and dashboards are
  an actual recurring request.

## Explicitly deferred

Do not port these as standalone product skills in the first pass:

- `deliver-prd`, `deliver-user-stories`, `deliver-acceptance-criteria`, and `deliver-edge-cases`:
  current `write-prd` and engineering `spec` already own these boundaries.
- `develop-adr`, `develop-spike-summary`, and `develop-design-rationale`: current technical
  design, ADR, prototype, and research capabilities cover the same decision space.
- `foundation-build-risk-review`: merge its single-dominant-assumption and no-code-test ideas
  into `scope-mvp` or `run-premortem` instead of adding a parallel gate.
- Full Foundation Sprint and Design Sprint families: workshop-heavy and disproportionate to the
  current system scope.
- Market sizing, OKR, meeting, and stakeholder families unless the product evolves into a
  broader PM operating system.

## Definition of done for future implementation

An adapted capability is not complete when its directory exists. It is complete only when:

- its role and artifact owner are registered;
- its upstream and downstream handoffs are documented;
- its runtime instructions use the current memory protocol and remain runtime-neutral;
- its output contract and refusal boundaries are explicit;
- representative trigger and output evaluations exist where risk justifies them;
- provenance and license notes are recorded;
- relevant catalog and documentation surfaces are updated;
- repository verification passes.

## First implementation slice when resumed

Implement only this smallest vertical slice:

```text
research synthesis → hypothesis → instrumentation spec
```

Verify that the resulting artifacts can be consumed by `validate-demand`, `scope-mvp`, and
engineering `spec` without re-asking or duplicating upstream decisions. Add experiment results,
pivot, and lessons only after this handoff is proven.

## Source references

- [`references/README.md`](../../references/README.md) — reference promotion policy
- [`references/pm-skills/README.md`](../../references/pm-skills/README.md) — PM-Skills catalog and
  lifecycle tooling
- [`system/skills-src/product/README.md`](../../system/skills-src/product/README.md) — current
  product pipeline and memory contract
- [`system/TODO.md`](../../system/TODO.md) — existing verification, provenance, and eval work
