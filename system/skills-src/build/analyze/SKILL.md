---
name: analyze
description: Non-destructive cross-artifact consistency and quality audit across canonical requirements, plan, and tickets. Use after /tasks and before implementation to catch duplication, ambiguity, terminology drift, coverage gaps, and constitution violations. Read-only — produces a report, never edits files.
---

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [design.contracts, run.execution_plan, change.tickets, repository.instructions]
  produces: [change.consistency_findings]
  updates: []
  invalidates: [change.inconsistent_conclusions]
  handoff_to: [domain_owners, implementation]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


# Analyze — Cross-artifact consistency audit

Audit the canonical spec/criteria, accepted contracts, run plan, and tickets for the active change. This optional delivery stage is read-only: return findings and remediation proposals; never edit files or dispatch follow-up work.

## Inputs and scope

Use coordinator-resolved change/task identity and relevant input references/revisions. Canonical requirements are substantive input; a literal `spec.md`, `plan.md`, or combined `tasks.md` is not required. Read only requested scope and report missing substantive inputs with their blocking effects. Analyze independent available scope without inventing absent content.

Include applicable repository instructions, accepted product/design decisions, current-state constraints, canonical parent/child tickets, and execution approach when relevant. Preserve existing requirement/criterion IDs rather than imposing FR/SC numbering. Do not select the newest directory/report as identity.

## Build the trace map

- Requirements/criteria: stable IDs, expected behavior, scope, priorities, concrete pass/fail outcomes. Distinguish buildable criteria from post-release business metrics.
- Accepted design: contract/decision IDs, consumed requirements, entities, boundaries, alternatives, applicability and revision.
- Tickets: canonical parent/child IDs, explicit criterion references, `depends_on`, affected surfaces, verification expectations, unresolved questions.
- Run plan/checklist: proposed sequence, shared-write risks, and references to canonical tickets. It does not own ticket status or accepted contracts.

Explicit IDs establish coverage. A keyword or file-path match is only a candidate link for review. Missing prior skill output is not missing knowledge when the substantive answer already exists elsewhere.

## Detection passes

1. **Duplication**: competing normative requirements or decisions across Product/spec/design; duplicate tickets for the same deliverable. Preserve canonical IDs when proposing consolidation.
2. **Ambiguity**: subjective pass/fail, vague security/performance expectations, unresolved assumptions or placeholders affecting implementation.
3. **Underspecification**: behavior missing an actor/trigger/outcome, contract missing failure behavior, task missing a verifiable result. Missing a template heading alone is not a defect.
4. **Instruction alignment**: conflicts with applicable repository constraints and required checks. Cite the rule and conflicting artifact; propose correction to the change, not an unsolicited instruction rewrite.
5. **Coverage**: criteria without a task/check, child ticket without its parent or accepted scope, tasks/contracts with no requirement basis, and omissions whose impact is unstated. Post-release metrics need an observation plan rather than invented implementation tasks.
6. **Inconsistency**: terminology/contract drift, conflicting technical choices, dependency cycles or missing IDs, unsafe proposed parallel boundaries, duplicate status sources, and stale consumed revisions. Inspect affected dependents without rewriting another domain's decision.

## Prioritize findings

| Severity | Meaning |
| --- | --- |
| CRITICAL | Applicable MUST violation, absent core requirements, conflicting required contracts, or no coverage for the core accepted outcome |
| HIGH | Conflicting normative text, untestable acceptance criterion, material missing verification, or stale premise blocking implementation |
| MEDIUM | Non-blocking terminology/coverage/detail gap with concrete impact |
| LOW | Minor clarity or redundancy issue |

Do not turn absence of a particular filename or numbering scheme into a blocker. A malformed artifact blocks conclusions that depend on it, not unrelated analysis.

## Report and handoff

Return the shared envelope with canonical change/task identity, assessed scope and consumed revisions, findings, unresolved questions/blocking effects, and next action. Each finding has a stable ID, category, severity, exact source anchor, evidence, and proposed owner/action. Same inputs produce the same finding identities.

Include a compact coverage table:

| Criterion / contract | Canonical task | Check/evidence | Gap or omission |
| --- | --- | --- | --- |
| <existing ID> | <existing ID/reference> | <verification expectation> | <impact or none> |

Report assessed/unassessed scope and counts only when useful. Zero findings is valid; do not invent problems. Keep the report bounded (50 findings is a ceiling; summarize lower-severity overflow). Critical blockers must be resolved before dependent implementation. The coordinator applies authorized remediation outside this read-only audit and routes domain decisions to their owners.
