# Feature Specification: [FEATURE NAME]

Last updated: 2026-08-02

**Feature Branch**: `[NNN-feature-name]`
**Created**: [DATE]
**Status**: Draft
**Input**: User description: "[ORIGINAL DESCRIPTION]"

## User Scenarios & Testing *(mandatory)*

User stories are prioritized journeys (P1 = most critical). Each story must be independently testable: implementing only P1 must still ship a viable MVP.

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language.]

**Why this priority**: [Value and why it ranks this way.]

**Independent Test**: [How to verify this story works on its own, end-to-end.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey.]

**Why this priority**: [Value and why it ranks this way.]

**Independent Test**: [How to verify on its own.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey.]

**Why this priority**: [Value and why it ranks this way.]

**Independent Test**: [How to verify on its own.]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more stories as needed. Drop unused ones.]

### Edge Cases

- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST [specific capability].
- **FR-002**: System MUST [specific capability].
- **FR-003**: Users MUST be able to [key interaction].
- **FR-004**: System MUST [data requirement].
- **FR-005**: System MUST [behavior].

Mark unresolvable items inline: `[NEEDS CLARIFICATION: <question>]`. These get resolved in the clarify pass.

### Key Entities *(include only if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes — no implementation types.]
- **[Entity 2]**: [What it represents, relationships to other entities.]

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users complete task in under 2 minutes."]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation."]
- **SC-003**: [User satisfaction metric, e.g., "90% of users complete primary task on first attempt."]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%."]

Criteria must be technology-agnostic. No frameworks, endpoints, or file paths here.

## Assumptions

- [Assumption about users, scope, environment, or dependencies.]
- [Assumption about what is explicitly out of scope.]

## Clarifications

*Populated by the inline clarify pass. Omit this section if no clarifications were needed.*

### Session [YYYY-MM-DD]

- Q: [Question asked] → A: [Answer]
