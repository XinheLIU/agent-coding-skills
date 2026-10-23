# <Task ID>: <Independently deliverable outcome>

Last updated: 2026-09-17

Parent: <canonical change ID and ticket link>
Type: <implementation | design>
Status: <pending | in_progress | done | failed | superseded>
Readiness: <ready | needs-design | needs-criteria | needs-review>
depends_on: <comma-separated task IDs, change/task IDs, or none>
affects: <surfaces/modules/contracts>

## Scope
<One independently verifiable slice; explicit exclusions.>

## Inputs
- Requirements: <canonical spec and criterion IDs, consumed revision>
- Design: <accepted decision/contract references and revisions>

## Verification
<Implementation: criterion IDs → checks and observable pass/fail outcomes; relevant environment. Design: concrete question, responsible suite skill, and accepted decision/artifact that resolves it.>

## Blockers
<Unresolved criteria/design, external preconditions, stale premises, and affected tickets; use none when settled. Encode ticket prerequisites in depends_on. A non-ticket blocker keeps Readiness unready.>

## Coordination proposal
<Shared-write risks, safe boundaries, unresolved questions and blocking effects.>

## Evidence
<Implementation revision/diff and verification references when available.>

Set Last updated to the ticket creation/update date. For this local format, the filename is `<Task ID>.md` and the H1 ID matches it. The graph qualifies local IDs with their change directory; use `change/task` for cross-change edges. Readiness records settled inputs/preconditions; dependency completion is checked separately. Preserve historical done status when evidence becomes stale and set Readiness to needs-review.

Fine-grained steps and exclusive claims live in Run Context and reference this ticket. Preserve an existing tracker schema rather than translating it into this template.
