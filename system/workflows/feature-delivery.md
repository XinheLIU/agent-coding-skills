# Feature Delivery Workflow

Last updated: 2026-09-09

Use approved intent and the [shared coordinator](context-coordination.md). Keep one canonical change/ticket ID throughout Product, Design, Implementation, Verification, and Release.

```text
canonical ticket + canonical requirements/criteria (write-prd or existing spec)
  → spec: establish delivery readiness, reuse requirements
  → accepted design/contracts when needed
  → planning by the active agent
  → tasks: independently deliverable child tickets when useful
  → analyze: read-only consistency audit
  → execution by the active agent, with tdd where appropriate
  → testing + review-code-quality
  → release evidence when authorized → retained change + run cleanup
```

There are no integrated `plan` or `implement` skills in this suite. Planning and execution are stages performed directly by the active agent under the contracts below. Never invoke missing entries. Existing substantive answers let work enter at the relevant stage without regenerating prior artifacts.

## Planning contract

Read the canonical spec/criteria, accepted decisions/contracts, affected Current State/source dependencies, operational constraints, and applicable checks. Record consumed revisions. Propose implementation boundaries, dependencies, affected surfaces, risks, criterion-to-check mapping, and a bounded execution sequence in `<work-root>/<effort>/plan.md` (or its established home).

The plan is Run Context. Accepted API/data/system contracts and consequential decisions are separately addressable Change Context linked from it; preserve them as soon as accepted. Do not copy normative requirement text into the plan. Unknown behavior returns to Product; unresolved design choices go to the relevant design skill. Reuse authorization and decisions already present.

Planning is ready when an implementer can identify the next change, its criterion references and verification, and unresolved questions have explicit blocking effects. The existence of `plan.md` alone proves nothing.

## Task decomposition and scheduling

`tasks` proposes child tickets only for independently deliverable, verifiable slices. Each keeps its parent change ID, criterion references, `depends_on`, affected surfaces, verification needs, and shared-write risks. Fine-grained steps stay in the run checklist. Reuse existing tickets and established tracker locations; local defaults are tracked `docs/changes/<change-id>/tasks/<task-id>.md`.

Canonical ticket status remains in that tracker. Roadmaps, including `draw-portfolio-dag`, render or reference it. The coordinator validates dependencies, claims, and concurrent-write risks and schedules the unblocked frontier. Do not create shadow claim tickets or infer parent completion from all child checkboxes.

## Execution contract

Before editing, recheck the active task's requirements/design revisions, dependencies, affected code, and exclusive claim. Implement the scoped slice using existing project conventions. Use criterion-based red → green loops when testing behavior; run appropriate checks for other changes. Report failed verification and scope/design deviations rather than silently revising accepted requirements.

Return code revision/diff identity, affected surfaces, decision and criterion references, checks run, failures/omissions, and next verification needs. The coordinator reconciles evidence and proposed transitions. Uncommitted work needs a reproducible diff identity; HEAD alone cannot identify it. A worktree is optional isolation selected by the coordinator, not a requirement imposed by `spec`; all handed-off references must resolve in the receiver's environment.

## Verification contract

Use [Testing](testing.md) and the [engineering evidence contract](../skills-src/craft/context/init-context/references/engineering-memory.md). Review both Standards and Spec axes. Retain criterion → test/evidence → revision mappings, environment assumptions, failures, omissions, and scoped readiness. Static implementation presence is not passing acceptance evidence. Changes to relevant requirements, contracts, code, tests, or environment trigger scoped reassessment.

## Release and close

Use the [Operations contract](../skills-src/craft/context/init-context/references/operations-memory.md) with existing project tooling and task authorization. Release evidence links the same change to the verified revision/artifact digest, target environment/configuration, gates, migration results, observability, and rollback references. If no release was requested or performed, record that without implying one occurred.

Reconcile applicable Product/System/Design/Operations Current State with observed evidence. Apply the protocol's retention gate: retain compact Change Context; verify it remains understandable without the run directory; then remove only reconciled scratch. Use `handoff` whenever another session must continue, with explicit claim transfer when applicable.
