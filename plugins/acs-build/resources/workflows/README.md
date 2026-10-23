# Workflows

Last updated: 2026-10-23

Workflows compose skills around the [shared memory protocol](../protocols/skill-declarations.md). Skills provide focused behavior; workflows own sequencing, approval gates, and state transitions.

## Rigor tiers

Choose the route for the task, not every lifecycle phase for every change.

| Tier | Route | Retained outcome |
| --- | --- | --- |
| **Spike** | A question in, an answer out through [acs-validate-prototype](../skills-src/design/ux/acs-validate-prototype/SKILL.md) (reference procedure; capability not installed) or a small direct probe | Nothing kept as product code; retain the answer and reviewed evidence only when a later decision relies on them |
| **Bounded (default)** | Change an existing flow: one ticket → short in-chat design → approval → [acs-implement](../../skills/acs-implement/SKILL.md#bounded-entry) | The change record, criteria, compact revision-bound evidence, and any ADR-worthy decision; no separate spec or HTML delivery plan for a single ticket |
| **Architectural** | New projects or subsystems, changed shared interfaces, or restructuring: the full [plan](plan.md) → [design](design.md) → [build](build.md) route | The canonical records for those stages |

### Declare before the first skill

Before invoking the first skill in a new run, the coordinator says the tier and reason out loud so the user can override the selection, and records them in the single configured recovery entry (default `<work-root>/<run-id>/state.md`). Include the current stage, its approval reference or `pending`, and model class/sensor cadence. For example: “Rigor tier: Bounded — this changes one existing CLI flag; I’ll present the short design here.” This is a declaration, not an extra permission gate. Existing explicit approval for that design and implementation remains valid.

On resume, read this entry before dispatching a skill. If an older run has no tier, classify and record it before continuing. Use Bounded by default for a well-scoped existing flow; choose Spike for a throwaway question and Architectural for structural work. When uncertain between two tiers, take the higher one.

### One-way ratchet

The ratchet only goes up: Spike → Bounded → Architectural. Hidden complexity upgrades the tier; nothing downgrades mid-task. Stop dependent execution, announce the reason, record the prior and new tier, and complete the higher tier's missing design/approval stages before resuming. A user can correct the initial selection or request an upgrade; a lower-process preference after work starts does not bypass this ratchet. A successful Spike does not authorize keeping its code: classify and obtain approval for the follow-up change, reimplementing against its criteria.

### Staged approval

**A reply approves the stage actually presented.** Present the Spike question and probe before investigating; present the Bounded design (outcome, scope, approach, and checks) before implementation. For Architectural work, approval of intent permits the next planning/design stage; approve the concrete design and delivery scope before implementation. An idea approval cannot approve a design or execution plan that has not been presented. Reuse recorded approval for the same stage and scope; do not ask again. A material scope/design change needs its own approval. Silence or a skipped answer never supplies approval.

Use the canonical [Questioning protocol](../protocols/questioning.md) for classification, frontier rounds, and the Established/Assumption/Disputed close. Confirmation and execution approval may share a response when both are explicitly presented; confirmation of understanding alone is not execution authorization. Missing user decisions block dependent work, while read-only investigation and independent authorized work may continue.

### Model tier and sensors

With a **cost-optimized model**, run available sensors continuously during execution (at each relevant change). With a **frontier model**, run them as a final gate. Sensors are executable checks supplied by the target repository: tests, linters, contract validators, and evidence checks. Record the actual model/class when known, cadence, commands, results, and tested source identity in run/evidence records. If the class is unknown, state that and use continuous checks. Model choice never lowers the rigor tier, skips required TDD checks, or weakens the [revision-bound evidence contract](../protocols/orchestration.md#evidence-contract). A missing required sensor is a reported verification gap, not a pass.

## Six Lifecycle Phases

Use these documents to navigate the SDLC. Their phase names are not installed slash commands or discoverable router skills; invoke the named `acs-` skills within each workflow using the host's syntax.

- [Plan](plan.md) — turn uncertain ideas, opportunities, or alerts into accepted product intent
- [Design](design.md) — settle requirements, UX design, and technical architecture (three sequential sub-phases)
- [Build](build.md) — implement features with plan approval, TDD loop, and handoff
- [Test](test.md) — audit coverage, add integration tests, verify the full suite is green
- [Deploy](deploy.md) — release to staging and production with evidence and rollback plan
- [Maintain](maintain.md) — ingest alerts, diagnose, write change records, close the loop autonomously for in-band fixes

## Role Evolution

The six phases encode a progression in engineering scope:

- **Feature implementer** — plan + build: write code that satisfies requirements
- **System designer** — design: define domain models, module boundaries, interface contracts
- **Platform curator** — maintain + test: extract reusable components, close the autonomous loop

## Legacy Workflows (Retained — Deprecated)

These workflows are preserved for backward compatibility. Use the six lifecycle verbs above for new work.

- [Ideas](ideas.md) — *deprecated: use plan*
- [Feature delivery](feature-delivery.md) — *deprecated: use build*
- [Testing](testing.md) — *deprecated: use test*
- [Debugging](debugging.md) — *deprecated: use maintain*

Shared [context coordination](../protocols/context-coordination.md) owns resolution, runtime binding, scheduling, claims, shared writes, freshness, and retention.
