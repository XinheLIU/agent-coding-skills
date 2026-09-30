---
name: acs-design-architecture
description: Design or review the system shape — feature-to-capability map, current/ideal/feasible architecture, shared foundations, data/technology/deploy fit, and the decision ledger. Use for greenfield architecture, brownfield audits ("this is tangled", "tech debt", "audit architecture"), or architecture review; writes the ARC section of the shared technical-design.md.
---

# Design Architecture

Last updated: 2026-09-30

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [system.current_state, system.affected_source, design.relevant_decisions, operations.constraints, verification.failure_history]
  produces: [design.selected_architecture, design.capability_map, design.architecture_findings]
  updates: [design.accepted_decisions, system.architecture_state]
  invalidates: [design.module_dependents, change.implementation_plan, design.disproved_assumptions]
  handoff_to: [design_modules, design_contracts, code_review]
```

Shared semantics: [memory and handoff protocol](../../resources/protocols/skill-declarations.md); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Save domain records, including proposed review inputs, in Persistent Memory before formal review or dependent handoff. Run recovery belongs to Working Memory. For human-facing reports and review feedback, use [Presenter](../../resources/protocols/presenter.md); views carry source revisions and never own domain facts.

Follow [the card contract](../../resources/skills-src/design/technical/references/card-contract.md): read the record, write only `## Architecture (ARC)` and `FND-ARC-*` ledger rows. Views follow [the technical view template](../../resources/skills-src/design/technical/references/technical-view.md) and [the visual report contract](references/visual-report.md); run the contract's validator and fix every error before handover.

**Owns:** what the parts of the system are, who owns each capability, what is shared and in what form, and whether the stack and topology fit the workload. **Does not own:** module interfaces (MOD), invariants and failure semantics (CON), code-level defects (`acs-review-code-quality`).

## Current (brownfield)

Reconstruct only what cannot be read cheaply from the record. Scope the survey to the request plus hot spots from change frequency (`git log --format= --name-only | sort | uniq -c | sort -rn`).

Map what imports, routes, registrations, and runtime paths actually do. Then assess:

| Lens | Look for |
| --- | --- |
| Boundaries | Circular dependencies, hidden coupling through shared mutable state, leaky abstractions, seams that don't match concerns |
| Cohesion | God modules, feature envy, scattered concerns, inappropriate intimacy — record the problem here; the split design belongs to MOD |
| Change cost | Change amplification (simple features touch 10+ files), navigation friction, cognitive load |
| Decisions | Explicit and implicit architectural decisions, each `Sound`, `Reconsider`, `Missing-but-needed`, `Drifted`, or `Stale` |

Rank each problem by `impact × change frequency / fix difficulty`. Violations on hot paths rank high; violations in stable code and aesthetic issues rank low.

## Target

1. **Capability map.** Give each accepted requirement a capability, owner, entry point, and the data it changes. Mark unknowns.
2. **Shared foundations.** Name a shared capability (communication, persistence, identity, errors, observability, scheduling, storage, UI primitives) only when it has named consumers. Choose the smallest form: local module, package/library, component, middleware, or service. Keep shared domain rules with their domain; do not create a `common` dumping ground. The foundation's contract is designed in MOD.
3. **Three views.** Describe *current* (brownfield), *ideal* (free to reorganize), and *feasible target* (accounting for compatibility, migration cost, and operations).
4. **Options.** Compare two or three materially different options on locality, leverage, failure isolation, operability, migration cost, and complexity. Recommend one. Keep rejected options only when the trade-off is consequential.
5. **Fit.** Record only non-functional constraints that shape the architecture, each with a measurable target and a verification method. Check:
   - **Data:** schema ownership, one writer per dataset, layering, lineage.
   - **Technology:** runtime, database, scheduler, and observability against the workload; name scaling cliffs.
   - **Deploy:** deploy units, network exposure, environment contract, prod/dev variant model.
   - **Trust boundaries:** where authentication happens, where authorization is decided, which component sees which data.
6. **Decisions.** Give each consequential choice an ADR or a `## Decisions` row. Reversibility matters most: a one-way door needs a flag, canary, or rollback path.

Target items: `ARC-n` rows naming capability, owner, form, consumers, and requirement IDs. Include one current/target diagram (ideal and feasible when brownfield).

## Review mode

Check the target (or a supplied plan) with the lenses above plus:

- **Blast radius:** the worst case of this decision, and how many systems and users it affects.
- **Boring by default:** is an innovation token being spent on something already proven?
- **Essential vs accidental complexity:** does the design solve a real problem or one it created?

Every problem is a `FND-ARC-n` ledger row with severity, confidence, and anchor.

## Deep mode

For a whole-system review, apply the six lenses in [architecture-lenses.md](references/architecture-lenses.md). Each lens maps first, then judges. Default: all six; args like `business,data` select a subset.

| Lens | Question |
| --- | --- |
| business | Do modules and entry points deliver the documented capabilities and end-to-end flows? |
| application | Is decomposition coherent; do layering, boundaries, cohesion, and runtime ownership match decisions? |
| data | Are schema ownership, data layering, dataset contracts, and lineage explicit and respected? |
| technology | Do runtime, DB, scheduler, and observability choices fit the workload; where are the scaling cliffs? |
| deploy | Are topology, network exposure, env contract, and prod/dev variants sound? |
| adr | Which decisions does the system rest on, and what is each one's ledger status? |

Scope is whole codebase or a subtree by default; architecture findings need surrounding context that a narrow diff hides. For scoped runs, capture the file list first and use it for every lens. An empty scope stops here.

When the coordinator allows delegation, a lens may run as a delegated task whose instruction is that lens's section of the reference; otherwise run it inline. Lens findings become `FND-ARC` rows with their confidence and anchors quoted verbatim, never paraphrased. The `adr` lens fills the Decisions ledger. A lens that was not run is recorded as `not assessed` in `### Open`. Code-level defects a lens surfaces (handler validation, SQL, concrete auth/reliability/security/perf bugs, test quality) are `routed` to `acs-review-code-quality`, not kept as ARC findings.

## Done when

Every accepted requirement has an owner, every shared capability has consumers and a chosen form, every boundary has a reason, and every gap has a next action or an out-of-scope decision. Hand boundaries and foundations to `acs-design-modules`, and trust-boundary and data-ownership items to `acs-design-contracts`.
