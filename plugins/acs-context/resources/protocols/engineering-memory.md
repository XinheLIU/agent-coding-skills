---
protocol: acs:engineering-memory
version: 1.1.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/engineering-memory.md
---

# Engineering and Verification Context

Last updated: 2026-09-25

Use the [protocol](skill-declarations.md) for lifecycle, identity, relationships, freshness, and coordination. This contract defines Implementation, Testing, and Refactoring artifact roles. Requirements, tickets, proposed/accepted contracts and concise evidence are Persistent Changes. Execution steps, claims, scheduler state and raw logs are Working; delivery reports and DAGs are derived [Presenter](presenter.md) views. Resolve all run paths and the one recovery entry through configuration.

## Implementation

`change.requirements` is the canonical spec and criterion IDs; `design.relevant_decisions` and `design.contracts` are accepted, separately addressable records with consumed revisions. `system.affected_modules` means relevant Persistent Current plus source/dependency evidence, not a repository-wide inventory.

`acs-plan-delivery` proposes independently deliverable child tickets with the same parent change, explicit `depends_on`, affected surfaces, criterion references, verification expectations, and shared-write risks. Use existing tickets when they already represent the slice. Small changes need no child tickets. Delivery tickets, dependencies, input revisions, and per-ticket readiness are retained Persistent Changes. Concrete design blockers reference their owning specialist and accepted answer; existing decision tickets are reused. `acs-implement` consumes this graph and returns scope/dependency changes to `acs-plan-delivery`. The execution plan and fine-grained checklist are Working Memory. Contracts/decisions required for formal review or downstream reliance leave the run plan before that use, with their actual proposed/accepted status. Retain exact reviewed content under Presenter rules.

`change.implementation_evidence` records change/task ID, source revision or dirty-diff digest, affected surfaces, accepted decision references, deviations, criterion references, and verification needs. It does not assert readiness without Testing evidence. Behavior changes outside accepted scope return to Product/Design.

## Testing and review

For a change, require its criteria and relevant contracts; for a standalone baseline audit, use explicitly accepted behavior/invariants and label missing expectations rather than inventing a change. Read relevant failure history and environment assumptions. `verification.criteria` identifies criterion → test/evidence → revision mappings; `verification.for_changed_code` selects only evidence affected by the delta.

Keep static coverage distinct from executed evidence. A compact retained verification record contains:

| Field | Required meaning |
| --- | --- |
| Identity/scope | Canonical change and task IDs, assessed criteria and regression surface |
| Consumed inputs | Requirement/design revisions and code revision or diff digest |
| Environment | Relevant runtime, configuration, services, data/migration assumptions |
| Mapping | Criterion ID → test/check → result and evidence reference |
| Results | Exact commands, failures, skips, not-run checks, omissions and their impact |
| Readiness | What is established, what remains blocked, and next action |

Raw output can remain in Working Memory only if the retained summary contains enough evidence to understand the verdict when raw logs disappear. Reconcile newer runs by scope and revision; preserve consequential prior failures. A code, contract, test, or environment change marks affected evidence for review. Standards review and Spec review remain separate axes; neither implies the other passed.

## Refactoring

`system.invariants` covers boundaries, dependency rules, external signatures, observable behavior, and consequential design rationale. Establish before/after baselines using the same checks and meaningful environment. Characterization tests preserve observed behavior; they do not override accepted criteria when current behavior is wrong.

`change.preservation_evidence` links invariant/criterion IDs to before/after results and structural delta. Update the configured System State (the architecture portion of Persistent Current) when module boundaries or dependency rules change. Record applicability/revision and source evidence. Amend or supersede applicable ADRs while preserving their rationale/history. If architecture did not change, record that assessment; do not create an empty ADR. External behavior changes return to Product/Design for scope resolution.

## Retained local records

Preserve existing homes. For new local-only changes, `docs/changes/<change-id>/` may contain `ticket.md`, `spec.md`, `decisions/`, `contracts/`, and `verification.md`; create only needed artifacts. The ticket/spec may already live in a product document or external tracker, in which case link there. The coordinator owns path resolution and shared writes, not domain verdicts.
