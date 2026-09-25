---
name: acs-settle-requirements
description: Define WHAT capabilities the product provides through functional requirements and testable acceptance criteria. Use when starting the design phase from accepted product intent, or when requirements are missing or ambiguous before technical design begins.
---

# Settle Requirements

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [product.accepted_intent]
  retrieves: [product.relevant_context, design.prior_decisions, change.existing_requirements]
  produces: [design.functional_requirements, verification.acceptance_criteria]
  updates: [change.spec_readiness]
  invalidates: [design.ux_dependents, verification.criteria]
  handoff_to: [design.ux, design.technical]
```

Shared semantics: [shared protocol](../../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../../protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../../../protocols/presenter.md); source records retain authority.

## Purpose

Requirements define WHAT capabilities the product provides, not how they are delivered (that is UX's job) or how they are engineered (that is technical design's job). Keep this boundary sharp: a requirement states observable behavior and an acceptance criterion states the concrete pass/fail signal. Neither specifies screens, components, or implementation.

## Inputs

- Accepted product intent from `docs/product/<product>/product.html` (the canonical source — do not invent scope).
- Existing canonical spec or requirement documents; reuse before authoring.
- Open questions from product intent that block testable behavior definition.

## Process

1. Read accepted intent records from `product.html`. Extract the capabilities that were validated, scoped, and accepted — these are the boundary.
2. For each capability, define one or more functional requirements using stable requirement IDs (e.g., `REQ-001`). A requirement names an observable behavior independent of implementation: who can do what, under which conditions, with what outcome.
3. For each requirement, write acceptance criteria with `Given / When / Then` or equivalent pass/fail structure. Criteria must be independently testable. Avoid criteria that assert only that "the UI shows X" — specify the behavior, not the rendering.
4. Surface contradictions, missing information, or scope gaps as explicit blockers with their blocking effect. Resolve from existing evidence first; ask only for remaining substantive questions.
5. Write output to `docs/changes/<change-id>/spec.md` or the established product spec home. Use [spec template](references/spec-template.md) when creating from scratch.

## Output

`specs/<spec>.md` containing:

- Requirement IDs with stable identifiers
- Observable behavior statements (actor, condition, outcome)
- Acceptance criteria (Given/When/Then, independently testable)
- Scope boundary: explicit list of what is out of scope
- Open questions blocking testable behavior (if any)

## Verify and hand off

- Every capability from accepted intent has at least one requirement.
- Every requirement has at least one acceptance criterion with a concrete pass/fail signal.
- No requirement describes a screen, component, or algorithm — only observable behavior.
- Scope boundary is explicit.
- No dates, metrics, or implementation assumptions invented to fill gaps.

Hand off to `design` (UX sub-phase) once requirements are complete. Technical design may begin in parallel once the capability boundary is settled. Do not commit or push.
