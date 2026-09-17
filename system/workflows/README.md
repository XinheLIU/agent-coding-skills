# Workflows

Last updated: 2026-09-17

Workflows compose skills around the [shared memory protocol](../skills-src/craft/context/acs-init-context/references/PROTOCOL.md). Skills provide focused behavior; workflows own sequencing, approval gates, and state transitions.

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

Shared [context coordination](context-coordination.md) owns resolution, runtime binding, scheduling, claims, shared writes, freshness, and retention.
