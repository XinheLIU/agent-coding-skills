---
name: acs-design-interaction-flow
description: Use when feature behavior, user flows, wireframes, navigation, or interaction states are unsettled.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [product.relevant_context, design.applicable_rules, design.relevant_decisions]
  produces: [design.interaction_contract]
  updates: [design.prototype_intent, design.accepted_decisions]
  invalidates: [design.visual_dependents, verification.interaction_evidence]
  handoff_to: [visual_design, product, implementation]
```

[Shared semantics](../../../../docs/shared-semantics.md#execution)

# Design Interaction Flow

## Procedure

0. Coordinator paths/change identity, never newest effort. Read PRD Parts 1+3, IDs/revisions, prototype markers, optional DESIGN.md/context. Existing design: ask iterate/archive+restart/cancel via coordinator. Explicitly reopen touched locked surfaces with user; no silent structure changes.
1. Reuse persona/tasks/platform/flows/edge cases; ask only gaps. Save `interaction/context.md` in resolved effort. Optional UX knowledge is evidence, never required.
2. Save hierarchy/nav in `architecture.md`: primary/secondary/tertiary, entry/exit, three indispensable elements. Confirm via coordinator; show grayscale draft first if requested.
3. In `state-table.md` define EVERY feature: LOADING/EMPTY/ERROR/SUCCESS/PARTIAL. Reuse PRD states; [questioning](../../../../protocols/questioning.md) classifies user-owned frontier decisions; present proposals at gate. Empty needs warmth, errors recovery. Authorized PRD reconciliation → `acs-write-prd` with accepted states/capability IDs; no second normative copy.
4. Validate 2–3 journeys via coordinator; `journey-map.md`: action/screen/feeling/support, emotional arc, failure/recovery.
5. Draft surface HTML in `interaction/wireframes/`: critical screens and differing mobile layouts. Only #f5f5f5/#e0e0e0/#333 grays, system font, labeled boxes/gray buttons; no decoration/shadows/gradients. Stable `data-surface`, real `data-capability`, `data-fidelity="wireframe"`, `data-structure="open"`, `data-updated`, five `data-state` blocks required. Missing capability → raise, never invent scope. Show drafts; structure approval/lock precedes visuals.
6. `decisions.md`: rationale. `responsive-a11y.md`: intentional desktop 1024+/tablet 768–1023/mobile <768; tab order/focus, Escape overlays, applicable arrow keys, landmarks/icon labels, live regions for dynamic state updates and error announcements, 44×44px targets/spacing, contrast 4.5:1 text / 3:1 large text+controls, reduced motion/nonanimated loading.
7. `unresolved.md`: decisions/recommendations/blockers, explicit deferrals; [questioning](../../../../protocols/questioning.md) for user-owned frontier.
8. Before formal review save exact proposal/revision/assets in Persistent Memory per [design memory](references/design-memory.md); bind feedback. On approval merge ONLY approved/reopened surfaces into `docs/design/prototype.html`, preserve slugs/unrelated sections, lock structure. Reopened styled/implemented → wireframe; report stale visuals. New prototype: self-contained/no build, keyboard state switcher, grayscale `:root`.
9. Return surfaces, accepted decision IDs/references/rationale/alternatives, requirement/token/contract revisions, delta/blockers/next action. Styling → `acs-visual-design-variants`; states → `acs-design-implement`; authorized PRD sync → `acs-write-prd`. Retain consequential rejections/review evidence; reconcile before cleanup.

## Completion criteria and hard rules

Verify all five states/capability links, ≥2 journeys, approved structure, recorded architecture/rationale/mobile/a11y/deferrals. No styling or unrelated surface edits. Authorized state promotion replaces working definitions with links. Prototype/drafts: `generated`/`source-revision` match visible date/revision; run [validator](../../../authoring/scripts/validate-report-html.py) `--version-only`, fix errors. Accepted rationale survives scratch; drafts are not authority.

[Layouts](references/output-examples.md) as needed.


## When NOT to use

[Choices](../../../authoring/acs-challenge-approach/SKILL.md); [code review](../../../test/review/acs-review-code-quality/SKILL.md); [demand evidence](../../../plan/acs-validate-demand/SKILL.md) (explicit only).

<!-- compaction-core:end -->
