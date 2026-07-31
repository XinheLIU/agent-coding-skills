# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[NNN-feature-name]/`
**Prerequisites**: `spec.md` (user stories + priorities), `plan.md` (tech stack, structure, data model, contracts).

**Tests**: [on | off — and why. E.g., "off — user did not request tests" or "on — user asked for unit tests".]

**Organization**: Tasks are grouped by user story so each story stays independently implementable, testable, and shippable.

## Format

```
- [ ] T### [P?] [USn?] <imperative action with exact file path>
```

- **T###**: sequential across all phases.
- **[P]**: parallelizable — different file, no within-phase dependency.
- **[USn]**: required inside user-story phases; omitted elsewhere.
- Description: imperative verb + exact file path.

## Phase 1: Setup

*Skip if the repo is already scaffolded.*

- [ ] T001 [P] …
- [ ] T002 …

## Phase 2: Foundational

*Blocks all user stories.*

- [ ] T00X …
- [ ] T00X [P] …

**Checkpoint**: Foundation ready — user-story phases can begin.

---

## Phase 3: User Story 1 — [Title] (Priority: P1) — MVP

**Goal**: [What this story delivers.]
**Independent Test**: [How to verify this story on its own.]

### Tests for User Story 1 *(include only if tests are on)*

- [ ] T0XX [P] [US1] …

### Implementation for User Story 1

- [ ] T0XX [P] [US1] …
- [ ] T0XX [US1] …

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 — [Title] (Priority: P2)

**Goal**: [What this story delivers.]
**Independent Test**: [How to verify this story on its own.]

### Tests for User Story 2 *(include only if tests are on)*

- [ ] T0XX [P] [US2] …

### Implementation for User Story 2

- [ ] T0XX [US2] …

**Checkpoint**: User Stories 1 and 2 both work independently.

---

[Add one phase per remaining user story, in priority order.]

---

## Phase N: Polish & Cross-Cutting

- [ ] T0XX [P] Update docs in …
- [ ] T0XX Run quickstart from plan.md end-to-end.

---

## Dependencies & Execution Order

### Phase dependencies

- Setup → Foundational → (user stories, parallelizable) → Polish.
- Foundational blocks all user stories.

### User story dependencies

- US1 (P1): depends only on Foundational.
- US2 (P2): depends on Foundational; may integrate with US1 but must stay independently testable.
- US3 (P3): depends on Foundational; may integrate with prior stories but must stay independently testable.

### Within each story

- Tests (if on) before implementation.
- Models → services → endpoints/UI → integration.

### Parallel opportunities

- [List the `[P]` tasks that can run together, grouped by phase.]

---

## Suggested MVP scope

Complete Setup + Foundational + Phase 3 (US1). Stop and validate against Independent Test for US1. Ship or iterate.

## Coverage gaps *(only include if any)*

- [FR-### or SC-### or user story that has no mapped task, and why.]
