---
name: acs-design-test-strategy
description: Design or review the test strategy before code — critical paths, which layer tests what, seams and test doubles policy, contract tests, fixtures and data, characterization for brownfield changes, and CI gates — so every requirement, contract, and failure mode has a verification method. Use when a design needs a test plan or a plan's testing section is thin; writes the TST section of the shared technical-design.md.
---

# Design Test Strategy

Last updated: 2026-09-29

## Context contract

```yaml
context:
  requires: [verification.acceptance_criteria]
  retrieves: [design.module_contracts, design.contracts, design.failure_modes, system.current_state, verification.failure_history, operations.environment]
  produces: [verification.test_strategy, verification.expected_behavior]
  updates: [design.accepted_decisions]
  invalidates: [verification.criteria_coverage]
  handoff_to: [trace_requirements, delivery_planning, testing, implementation]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

Follow [the card contract](../../resources/skills-src/design/technical/references/card-contract.md): read MOD and CON, write only `## Test Strategy (TST)` and `FND-TST-*` rows. Views follow [the technical view template](../../resources/skills-src/design/technical/references/technical-view.md) and [the visual report contract](../acs-design-architecture/references/visual-report.md).

**Owns:** what is tested, at which layer, with which doubles and data, and what blocks a merge. **Does not own:** writing tests (`acs-tdd`, `acs-implement`), measuring coverage of existing tests (`acs-analyze-test-gaps`), reviewing test code in a diff (`acs-review-code-quality`).

## Current (brownfield)

Inventory only what the strategy depends on: test layers present and their runners, how slow each is, existing doubles and fixtures, flaky areas, and CI gates. When `docs/test-gaps.md` or `docs/critical-paths.md` from `acs-analyze-test-gaps` exist, consume them instead of re-deriving.

## Target

1. **Critical paths.** At most 8 business flows whose failure costs money, data, or trust, each tied to criterion IDs. These get the strongest verification; everything else is proportionate.
2. **Layer assignment.** For each thing to verify, pick the cheapest layer that can observe it:

   | Verify | Default layer |
   | --- | --- |
   | Pure logic, an invariant inside one module | unit |
   | Operation contract across a MOD boundary | contract / integration |
   | Adapter behavior (DB, queue, HTTP) | integration against a real or containerized dependency |
   | Critical path end to end | e2e, one happy path plus its worst failure mode |
   | Brownfield behavior about to be moved | characterization, written before the change |

3. **Verification map.** One `TST-n` row per criterion, `CON-n`, and failure-mode row:

```markdown
| ID | Verifies | Layer | Method | Doubles | Data | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| TST-4 | CON-2, failure "inventory timeout" | integration | fault-inject timeout, assert 503 and no stock change | fake clock | seeded sku | CI required |
```

4. **Seams and doubles policy.** Mock only at owned boundaries (MOD interfaces, adapters); never mock what you don't own; prefer fakes for stateful dependencies. Name each seam a test needs; a seam the design lacks goes to MOD as an open item.
5. **Fixtures and data.** How test data is built (builders, factories, seeded snapshots), isolated between tests, and kept free of production data.
6. **Gates.** What runs on every commit, what blocks merge, what runs nightly, and the time budget for each. LLM, prompt, or eval changes need an eval case.
7. **Regression.** Every changed behavior has a test that fails on the old behavior or a characterization test that pins the old behavior on purpose.

## Review mode

Flag as `FND-TST-n`: criteria or `CON` items with no `TST` row, critical paths verified only by unit tests, failure modes marked "tested" with no named test, mocks of third-party internals, e2e tests used where a contract test would do, brownfield moves with no characterization step, and no testing mentioned at all (`P1`).

## Done when

Every criterion, `CON` item, and failure-mode row has a `TST` row or an explicit accepted-risk decision. Hand the map to `acs-plan-delivery` so each ticket carries its checks, and to `acs-trace-requirements` for the test column.
