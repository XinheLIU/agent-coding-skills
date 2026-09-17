# Run Context

Last updated: 2026-09-17

Use the lifecycle and retention rules in [PROTOCOL.md](PROTOCOL.md). This reference defines the disposable run shape; accepted change records live separately in established tracker/document homes, defaulting to tracked `docs/changes/<change-id>/` for new local-only changes.

## Shape

Create only artifacts needed by the run:

```text
<work-root>/<effort>/
├── state.md
├── progress.md
├── plan.md             # execution steps; links accepted contracts/decisions
├── checklist.md        # fine-grained steps, not canonical tickets
├── claims/             # task IDs, owners, base revisions; serialized coordinator
├── discovery.html      # product analysis awaiting reconciliation
├── research/
├── prototypes/         # experiments, not the accepted design prototype
├── handoffs/
└── raw-output/
```

Keep established paths. A canonical ticket or spec already under a legacy work root must be retained or moved with stable identity and repaired links before deleting that root. Location does not turn Change Context into scratch.

## State template

```markdown
# <Effort>: State

Last updated: YYYY-MM-DD

Change: <canonical ID and accessible ticket reference>
Task: <canonical child ID/reference, when applicable>
Canonical status: <ticket reference; do not maintain a second status>

## Run posture
<What this session established; consumed revisions.>

## Next action
<One concrete action a cold session can begin.>

## Blockers
<Questions and their blocking effects, or none.>

## Pointers
- <Canonical spec and needed criterion anchors>
- <Accepted decisions/contracts and revisions>
- <Relevant evidence, active review findings, and claim>
```

The coordinator updates routing after a meaningful transition and appends one dated progress entry. Correct prior progress with a newer entry rather than rewriting it. Handoffs use the protocol's envelope; no transcript copy is required.

## Decision work and execution work

Open consequential decisions are addressable Change Context tickets or records with a question, domain status, dependencies, decision/evidence, and owner. An answered decision remains retained. Claims reference those identities in Run Context and follow the protocol's serialized acquisition/transfer rules. Canonical ticket progress is not inferred from an unchecked run checklist.

## Cleanup gate

Follow the protocol's retention sequence. Verify ticket/spec, consequential rationale, final verification, release references, and applicable Current State without the run directory. Only then remove reconciled run artifacts. Preserve accepted design decisions at acceptance, not at cleanup or component-documentation time. Repeating reconciliation without new evidence changes nothing.
