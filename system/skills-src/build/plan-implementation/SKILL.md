---
name: plan-implementation
description: Establish a feature's delivery boundary around its canonical ticket and requirements. Reuse an existing spec; create requirements only when none exist. Use to prepare an approved change for design, planning, and implementation.
---

# Plan Implementation

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.intent_or_existing_requirements]
  retrieves: [product.relevant_context, design.relevant_decisions]
  produces: [change.spec_readiness]
  updates: [change.requirements_when_absent]
  invalidates: [design.requirement_dependents, verification.criteria]
  handoff_to: [design, implementation]
```

Shared semantics: [shared protocol](../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Consume the canonical change and requirements selected by the coordinator. Keep ticket, requirement, and acceptance-criterion IDs across delivery; a new branch is not a new change identity.

## Inputs

- Existing ticket/spec and accepted product records, or explicit feature intent when no requirements exist.
- Relevant Product evidence, scope, criteria, open questions, and review findings.
- Accepted design/contract references and relevant Current State when available.

Use [the Product contract](../../craft/context/init-context/references/product-memory.md) for requirement authority and [delivery](../../../workflows/feature-delivery.md) for coordination and the planning/execution stages.

## Reuse before authoring

1. Follow the canonical ticket's spec link and relevant criterion anchors. An existing Markdown spec or canonical legacy PRD remains the requirement source. Do not create another `spec.md` from its contents.
2. Assess whether behavior, scope, priorities, acceptance, exclusions, and success measures are specific enough to implement. Read accepted design as constraints and linked decisions; do not recast it as new requirements.
3. Surface contradictions or missing implementation-critical answers with their exact blocking effect. Resolve from existing evidence first; ask only remaining substantive questions. Route proposed scope changes to Product and contract changes to Design.
4. Return the change ID, canonical spec path and consumed revision, criterion references, accepted decisions, unresolved questions, and next action. The coordinator updates run routing.

## When no canonical requirements exist

Create a single spec in the established product/tracker home; for a new local-only change default to tracked `docs/changes/<change-id>/spec.md`. Establish or reuse its canonical ticket. Use [the spec template](references/spec-template.md) only for this branch. Explicit user intent may supply authority; missing prior discovery artifacts do not force a research pipeline.

Requirements use stable IDs, independently testable behavior, and criterion IDs with Given/When/Then or another concrete pass/fail signal. Separate observed behavior from proposed or accepted scope. Record important edge/recovery cases and assumptions; do not invent dates, metrics, or scope to fill a template. Technical contracts and consequential decisions are separately linked Change Context.

For product-backed changes, return the new spec reference for `write-prd` to reconcile into the existing product reading index/roadmap. It tightens the same source instead of generating a competing spec. No product document is required solely for a small local change.

## Verify and hand off

- Exactly one canonical requirement source; existing IDs and unrelated requirements preserved.
- Requirements and acceptance criteria are testable, with authorization/decision basis and source references.
- Missing answers remain explicit blockers; proposed intent is not silently accepted.
- Accepted designs/contracts are accessible and revision-labelled.
- Next action is the relevant design stage or direct planning under the delivery workflow.

Worktree creation, path resolution, claims, and runtime bindings belong to the coordinator. This skill does not require a worktree or an unavailable planning skill. Do not commit or push.
