---
name: acs-shape-solution
description: Turn a validated demand or current-product baseline into a concrete solution with understood target experience, connected journeys, required capabilities, and a resolved product form and data basis. Use when defining what a product or feature should do from the user's side — including ambitious redesigns of existing products. For user stories from existing code without prior discovery, use acs-map-current-product first.
disable-model-invocation: true
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [product.problem_or_baseline]
  retrieves: [product.demand_assessment, north_star.relevant_goals]
  produces: [product.solution_proposal]
  updates: [product.discovery_records]
  invalidates: [product.solution_dependents]
  handoff_to: [product, design]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.

# Shape Solution

## Procedure

0. Reuse records; greenfield uses problem/demand context. Existing-product work needing a missing/stale baseline → `acs-map-current-product`; Yellow/Red/disputed/assumption-only demand → `acs-validate-demand`, unless authorized uncertain exploration. Settled → `acs-define-outcomes`.
1. Simple default; multi-role/flow/integration/architecture → Complex. Frame deep need/ambition/constraints vs assumptions, before/during/after/failure/other actors. Existing may need redesign.
2. Who (name/role/context), What (workaround/failure), Fear (consequence/audience). Ask gaps only: numbered recommendations via [questioning](../../resources/protocols/questioning.md). Label inferences; preserve facts.
3. Persona; acts: routine/trigger/action+time contrast/identity; journey: discovery+skepticism/one-action value/habit/identity; prompt. Scenarios: primary/included/deferred, frequency/duration/participants/connectivity/attention. Complex: rank personas/divergences, implemented/in-progress/planned capabilities/gaps. Never invent gaps/integrations/coverage. [Detail](references/framework.md).

## Phase C — Compare Meaningful Alternatives

### Scope postures

Reuse choice or recommend/reason/ask; analysis cannot approve scope.

- **Expansion**: explore a more ambitious experience.
- **Selective expansion**: baseline + optional additions, neutral recommendation/effort/risk.
- **Hold**: strengthen within accepted boundaries; no expansions or silent cuts.
- **Reduction**: minimum core; explain cuts, retain until approved.

Raise concerns once; no drift/re-arguing. Record changes. Every addition or removal requires explicit user opt-in. Reuse existing explicit approval; skipped or unanswered choice is pending. Distinct choices via questioning; batch independent ones.

`discovery.html` / `scope-decisions` `decision`: `Scope posture:`, basis/baseline/dispositions/approval. `NOT in scope:` exclusions/reasons (rejected/deferred additions, approved cuts), or `NOT in scope: none recorded`. Pending additions outside/cuts inside, never rejected. Return this record's anchor.

Compare outcome/coherence/assumptions/risk/complexity. [Expansion posture](#scope-postures): 2–3 distinct options incl. baseline; outcome/differentiation/tested assumptions/S/M/L/XL/upside/failure. Recommend + overturning evidence.

## Phase C2 — Resolve and confirm

4. [Axes](references/axes.md): binding scenario → cheapest first-value form (Wizard of Oz first ten users) → each core datum graded A–D. C/D forbid full depth. Scenario/form/data sentence; fix coherence failures before commitments.
5. Validate details/axes/C/D limits. Diagrams: primary journey only, added signal/real systems/status. Optional UI demo: primary scenario/realistic data/inline HTML+CSS+JS/no remote fonts/CDN/frameworks/Design Demo+date. [Examples](references/rich-output.md).
6. Confirm scenario/experience/first value before writes; correct records or note settling observation. Exit: outcomes/journeys/capabilities/relations/axes/alternatives/evidence vs assumptions/questions. Commitments → `acs-define-outcomes`; PRD/delivery downstream.

## Completion criteria and hard rules

Before writes read [product memory](../../resources/protocols/product-memory.md). Read–match–enrich–verify discovery.html; reuse IDs/facts/behavior, link evidence/questions, return anchors. Unknowns stay questions. Verify unique IDs/kinds/sections/anchors/dates, generated/source-revision = visible date/revision. Run [validator](../../resources/skills-src/authoring/scripts/validate-report-html.py) `--version-only`, available `scripts/validate-product-memory.py <file>`; fix errors. Demos own no facts.

<!-- compaction-core:end -->
