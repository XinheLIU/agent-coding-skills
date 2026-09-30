---
name: acs-trace-requirements
description: Trace every requirement through entry point, registration, module, contract, and test — against the design before build and against the code after build — classifying each as REACHABLE, PARTIAL, MISSING, DIVERGENT, UNEXPECTED, or UNASSESSED, and applying scoped wiring repairs. Use for "what's left to do", "what did I miss from the design", resuming a partial implementation, or pre-PR drift checks; writes the TRC section of the shared technical-design.md.
---

# Trace Requirements

Last updated: 2026-09-30

## Context contract

```yaml
context:
  requires: [change.requirements, design.module_contracts]
  retrieves: [design.wiring_map, design.contracts, verification.test_strategy, system.current_state, system.interface_rules, verification.latest_evidence, source.review_scope]
  produces: [verification.trace_matrix]
  updates: [system.current_state, system.interface_rules, change.verification]
  invalidates: [design.gaps, verification.unsupported_readiness, verification.affected_evidence]
  handoff_to: [implementation, testing, code_review, sync_context]
```

Shared semantics: [memory and handoff protocol](../../../../protocols/skill-declarations.md); shared execution: [Coordination](../../../../protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../../../protocols/presenter.md); views carry source revisions and never own domain facts.

Follow [the card contract](../references/card-contract.md): read every accepted section, write only `## Traceability (TRC)` and `FND-TRC-*` rows. Views follow [the technical view template](../references/technical-view.md) and [the visual report contract](references/visual-report.md); run the contract's validator and fix every error before handover.

**Owns:** whether what was designed is connected, and whether what was built matches the design. **Does not own:** judging the design (other cards), code quality (`acs-review-code-quality`), running tests (`acs-analyze-test-gaps`).

## Modes

- **pre-build** — trace the design alone. Every criterion must reach an ARC/MOD owner, a wiring point, its CON items, and a TST row. Finds design holes before code exists.
- **post-build** — trace the code against the design. Scope with the coordinator-resolved range (`git diff --name-only <base>...HEAD`, a subtree, or the whole repo).

## Trace

For each criterion, one `TRC-n` row following the chain `requirement → entry (route/menu/command/job/export) → registration → MOD interface → owning module → adapter → CON items → TST test`:

```markdown
| ID | Requirement | Entry | Module | Contracts | Test | Status | Evidence | Conf |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRC-3 | AC-2.1 | POST /orders (routes.ts:12) | MOD-2 Orders | CON-1 | TST-4 (orders.int.test.ts:30) | PARTIAL | refund branch missing, orders.ts:88 | HIGH |
```

| Status | Meaning |
| --- | --- |
| `REACHABLE` | Every link found and matches intent. A static finding, not proof by execution |
| `PARTIAL` | Found but incomplete: missing branch, stub, TODO, unhandled error path, or no test |
| `MISSING` | No code (post-build) or no design owner (pre-build) |
| `DIVERGENT` | Exists but differs meaningfully from the design: other approach, data model, or API shape |
| `UNEXPECTED` | Code in scope that no requirement or target item explains |
| `UNASSESSED` | Could not be traced; name the reason (dynamic registration, external consumer, missing access) |

Also verify dependency direction against MOD, middleware order, and error and permission paths where the chain crosses them. Do not call code unused only because static search misses it; dynamic and external consumers stay `UNASSESSED`.

**Unexpected code.** For each changed file tied to no row, decide: legitimate infrastructure or pattern extension (note it) or scope creep (`FND-TRC` row, one sentence why).

**Build order.** From MOD dependencies, list non-`REACHABLE` rows in topological order, the ones that unblock the most first. Cycles are a MOD finding.

## Scoped repairs

Only in post-build mode, only within the requested scope, and only when the evidence is conclusive: fix broken registrations, stale links, missing exports, and obsolete local guidance. Preserve unique rationale and user-authored rules. Record each repair in the section. A `DIVERGENT` row is never "repaired" here: the design owner decides whether the code or the design changes.

## Output

The `TRC` section holds the summary counts, the matrix, unexpected code, build order, repairs, and the commands and environment used. Its `### Open` names which non-`REACHABLE` rows `acs-review-code-quality` should focus on.

## Done when

Every in-scope criterion has a status with evidence and every gap has one next action. Route `MISSING` and `PARTIAL` to `acs-implement`, `DIVERGENT` to the owning card, test gaps to `acs-analyze-test-gaps`, and broad doc drift to `acs-sync-context`.
