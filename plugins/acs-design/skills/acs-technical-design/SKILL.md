---
name: acs-technical-design
description: Run technical design or design review as a set of aspect cards — architecture, modules, contracts, test strategy, traceability — that write one shared technical-design.md and one HTML view. Use for "technical design", "architecture review", "review the design", "review this plan/RFC before coding", or a holistic design-quality read; it picks which cards to run and consolidates cross-card findings.
---

# Technical Design

Last updated: 2026-09-29

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [system.current_state, design.relevant_decisions, design.proposal, operations.constraints]
  produces: [design.technical_overview]
  updates: [design.accepted_decisions]
  invalidates: [change.implementation_plan]
  handoff_to: [design_architecture, design_modules, design_contracts, design_test_strategy, trace_requirements, delivery_planning]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

Read [the card contract](../../resources/skills-src/design/technical/references/card-contract.md) first. This skill owns no aspect lens. It decides which cards run, in which mode, and merges their findings. Every aspect judgment belongs to a card.

## 1. Locate and challenge scope

Resolve the requirement/criterion IDs, the record (`docs/design/technical-design.md` or the established home), and any user-supplied plan, RFC, or design doc. A supplied plan is the review subject; its content goes into the cards' `Target` blocks as `proposed`, and it is not kept as a second design file.

Before any card runs, answer:

1. **What already exists** that partly solves this? Search for related modules, services, and prior attempts. A rebuild of something that exists is the first finding.
2. **What is the minimum change** that meets the accepted criteria? Name work that can be deferred without blocking them.
3. **Complexity smell:** more than 8 files touched or more than 2 new services/classes. Challenge whether fewer moving parts reach the same goal.
4. **Completeness:** does the scope cover error paths, edge cases, and tests, or is it a happy-path shortcut? When completeness is cheap, recommend it.

If a check triggers, present a reduced scope as option A and stop until scope is agreed. Record the decision, `NOT in scope` items with one-line reasons, and `What already exists` in `## Overview`.

## 2. Pick cards and mode

| Situation | Cards |
| --- | --- |
| Greenfield, requirements accepted | ARC → MOD → CON → TST → TRC (design mode) |
| Brownfield change that fits current architecture | MOD → CON → TST → TRC; ARC only if a boundary moves |
| Brownfield, structure unclear or "this is tangled" | ARC and MOD in review mode against code first |
| Plan/RFC review before coding | all five in review mode against the plan |
| "What's left?" / resume a partial implementation | TRC post-build only |
| Holistic architecture review | ARC with deep mode, then CON; others on request |

Arguments like `arc,con` skip the prompt. Otherwise propose the set and mode, one line of reason each, and let the user trim it. Cards whose inputs are missing are listed as `not assessed` with the blocking input.

## 3. Run cards

Run cards in handoff order; each reads the sections accepted before it. A card may be run as a subagent when the coordinator allows delegation; each card still writes only its own section. Stop after each card with `P0` or `P1` findings of HIGH/MEDIUM confidence: present one question per finding, with 2–3 options, a recommendation, and "do nothing" when reasonable. Unanswered questions stay `open` and are listed as `UNRESOLVED`.

## 4. Consolidate

After the selected cards finish:

- Dedupe the ledger by anchor and add `Confirmed by` for cross-card overlaps. Cross-card findings rank first.
- Fill `## Overview`:

```markdown
## Overview
Scope: <accepted as-is | reduced — summary> · Cards run: ARC(review), CON(design) · Not assessed: TST (no criteria)

| Card | Status | P0 | P1 | P2 | Note |
| --- | --- | --- | --- | --- | --- |

Top risks: <≤3 FND links>
Cross-card themes: <2–4 patterns>
Verdict: READY TO BUILD | NEEDS REVISION | AT RISK — <one-line reason>
Next action: <one action, owning card or skill>
```

- Ask Presenter to rebuild `docs/design/technical-design.html` from [the technical view template](../../resources/skills-src/design/technical/references/technical-view.md) when a human will read the result. Complex multi-card views use the tabbed layout in [the visual report contract](../acs-design-architecture/references/visual-report.md).

`READY TO BUILD` requires: every accepted requirement has an ARC or MOD owner, every CON item names where it is enforced, every critical path has a TST layer, and no open `P0`.

## Handoff

Hand accepted target IDs and open items to `acs-plan-delivery`. Route code-level findings to `acs-review-code-quality`. Do not create per-card report files; the record and its view are the whole output.
