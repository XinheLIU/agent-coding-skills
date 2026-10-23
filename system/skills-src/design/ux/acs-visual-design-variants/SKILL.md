---
name: acs-visual-design-variants
description: Use when locked wireframes and DESIGN.md exist but visual directions need comparison before style approval.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [design.locked_structure, design.applicable_rules]
  retrieves: [change.requirements, design.relevant_decisions]
  produces: [design.visual_decision]
  updates: [design.prototype_intent, design.accepted_decisions]
  invalidates: [implementation.visual_dependents, verification.visual_evidence]
  handoff_to: [implementation]
```

[Shared semantics](../../../../docs/shared-semantics.md#execution)

# Visual Design Variants

## Procedure

0. Use coordinator paths/change/criteria/revisions, never newest effort. Read DESIGN.md (legacy until migrated) and `docs/design/prototype.html`. Require locked wireframe and five `data-state` blocks. STOP if missing: structure → `acs-design-interaction-flow`; authority → `acs-design-context`/`acs-design-system-create`.
1. Save `data-surface` slugs/constraints/tokens in `<work-root>/<effort>/visual/constraints.md`; read optional journey/states. Header/nav/zones/positions/form order/footer/mobile/transitions/flows CANNOT change. Only type/color/within-scale spacing/weight/decoration/motion vary.
2. Ask visual/emotional intent through the coordinator using established context. Propose three distinct strategies, not color swaps; confirm directions before generation. If requested, show the locked prototype first.
3. Generate `visual/variants/variant-{a,b,c}.html`: exact structure, five states, working switcher, DESIGN.md tokens. Optional coordinator taste/production must obey structure/tokens/paths/states; native HTML fallback. [Example](references/output-examples.md#example-1).
4. Open all three variants for side-by-side review. Before formal review save the exact proposed revision and reviewed assets in Persistent Memory per [design memory](references/design-memory.md); bind feedback to that revision. Ask approval, iteration, hybrid or new directions through the coordinator.
5. Approval: merge winning CSS into the existing surface via shared `:root` tokens and section-scoped rules; preserve markup/markers/state blocks, keep structure locked, set `data-fidelity="styled"` and current `data-updated`. Iteration: change only visuals and present again, max 3 iterations; if not converging suggest returning to interaction design. Hybrid: combine visual elements without structural change and obtain approval before merge. None work: ask what's missing, define three new directions and regenerate.
6. Save `visual/decision.md` rationale/alternatives ([example](references/output-examples.md#example-2)). Return decision IDs/references, delta/surfaces, requirement/token/contract revisions, blockers/next action. Implementation → `acs-design-implement`; structure → `acs-design-interaction-flow`; authority → `acs-design-context`.

## Completion criteria and hard rules

- All three variants share the exact locked structure and differ meaningfully in strategy. All five states are styled in the approved merged section; empty/error states cannot be skipped. The switcher works, specified mobile behavior survives, interaction intent matches the journey, and WCAG AA contrast is checked with browser tools.
- Every visual value traces to DESIGN.md; no invented colors/fonts or local authority overrides. A missing/wrong token routes to `acs-design-context`. This skill selects among permitted directions; it does not create token authority.
- Only approved treatment merges; section stays locked with styled fidelity and current date. No navigation, button-position, layout or state-transition changes. A visual request never bypasses structure approval.
- Prototype and all variant HTML carry `generated` and `source-revision` matching visible date/revision; run the [HTML validator](../../../authoring/scripts/validate-report-html.py) with `--version-only` and fix errors.
- Retain exact review evidence, accepted rationale, consequential rejected alternatives and consumed revisions in Persistent Memory. Working variants remain exploration until reconciliation; preserve reviewed assets before cleanup. Keep decision rationale until folded into component documentation at shipping. Return capability outcomes and the approval transition to the coordinator; the styled canonical section is the implementation handoff.

<!-- compaction-core:end -->
