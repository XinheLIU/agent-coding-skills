---
name: acs-design-implement
description: Use when an approved styled prototype and DESIGN.md are ready for production implementation.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.requirements, design.accepted_prototype, design.applicable_rules]
  retrieves: [system.affected_source, design.relevant_decisions, operations.checks]
  produces: [change.implementation_evidence]
  updates: [source.components, design.component_records]
  invalidates: [verification.for_changed_code]
  handoff_to: [testing, code_review]
```

[Shared semantics](../../../../docs/shared-semantics.md#execution)

# Design Implementation

## Procedure

0. Use coordinator paths/change, never newest effort. Require DESIGN.md (legacy system.md until migrated), criteria/contracts/revisions and prototype sections `data-fidelity="styled"`, `data-structure="locked"`, five states. STOP if missing: surface → `acs-design-interaction-flow`; visual approval → `acs-visual-design-variants`; authority → `acs-design-context`/`acs-design-system-create`.
1. Read target sections/tokens/capability links/durable rationale/contracts. Scratch may add unresolved context; accepted rationale survives cleanup. Preserve IDs/revisions and intent/behavior distinction.
2. Detect/report framework/versions/package manager/CSS from project config. Match React TypeScript functions/props, Vue script-setup SFCs, Svelte reactivity, HTML/BEM as applicable; never impose example stack.
3. Extract DESIGN.md tokens to stack CSS/Tailwind/CSS-in-JS; ask location if ambiguous. [Token examples](references/output-examples.md#example-1) / [typed tokens](references/output-examples.md#example-2) illustrate layout, never values.
4. Reuse/confirm names/directory/composition via coordinator. Implement semantic structure, LOADING/EMPTY/ERROR/SUCCESS/PARTIAL, token variables (no hardcoded colors/spacing), typed dynamic APIs/state variants/defaults; match conventions. Optional [examples](references/output-examples.md#example-3).
5. Optional polish: DESIGN.md values, locked structure, EVERY fix/reason in `## Implementation Notes`. Layout/nav/transitions → `acs-design-interaction-flow`; native gates always run.
6. Provide usage example; document API/props/states/rationale/revisions/notes in `docs/design/components/<name>.md` ([example](references/output-examples.md#example-5)). Before formal review persist exact proposal/revision/assets per [design memory](references/design-memory.md); bind feedback.
7. After implementation/checks mark prototype `data-fidelity="implemented"`, locked, with `data-component`, `data-component-doc`, current `data-updated`. Intent stays prototype; behavior is shipped code. Reconcile accepted better design or document drift. Reopen only accepted design changes; no second synchronized UI.
8. Return component/token/doc paths, surface anchors, decision IDs/references/rationale/alternatives, requirement/token/contract revisions, delta/blockers/next action; close design pipeline. Reusable conventions → `docs/conventions` via `acs-sync-context`. Preserve consequential review evidence/assets before reconciled cleanup.

## Completion criteria and hard rules

- All five approved states, locked structure and DESIGN.md tokens preserved; no off-system colors/fonts or unapproved layout/nav/transition changes.
- Validate WCAG AA contrast (4.5:1 normal text, 3:1 large text), semantic landmarks, sequential headings, icon-button ARIA labels, meaningful-image alt text, explicit associated form labels and keyboard access with visible 3px accent focus outline.
- Mobile-first flexible layouts; touch targets ≥44×44px; no small-screen horizontal scroll; test 375px, 768px and 1024px breakpoints.
- Component API/prop types and usage example documented; files/folders follow actual stack conventions. Code is canonical behavior, prototype canonical intent, component docs durable Current State.
- Prototype `generated`/`source-revision` match visible date/revision; run the [HTML validator](../../../authoring/scripts/validate-report-html.py) with `--version-only` and fix errors. Report later intent/behavior divergence and route reassessment to Design. Exploration is disposable only after review evidence is retained.

<!-- compaction-core:end -->
