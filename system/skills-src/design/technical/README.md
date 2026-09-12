# Design · Technical

Last updated: 2026-09-12

System architecture and structural decisions — the load-bearing design choices that constrain implementation. Feeds `build/` implementation. Upstream: the product document resolved through `docs/agents/memory.md` and `state.md`, and `specs/<spec>.md` from the requirements sub-phase. Entry criteria live in [`../README.md`](../README.md).

## The three-phase progression

Technical design follows a DDD-style sequence. Run these phases in order; skip earlier phases only when their artifacts already exist.

### Phase 1: Prototype validation (problem space)

**Question:** Is this worth building? Can the approach work at all?

| Skill | Owns |
| --- | --- |
| `explore-unknowns` | Spike technical unknowns; map dependency-ordered decision tickets before committing to full design |

Run `explore-unknowns` first when the approach is uncertain — API capability, performance cliff, license compatibility, integration risk. Exit with a go/no-go decision and validation notes. Spike code is disposable; the decision it bought is not.

### Phase 2: Engineering hardening (solution space)

**Question:** Can we maintain this long-term?

| Skill | Owns |
| --- | --- |
| `engineer-domain-model` | Entities, value objects, aggregates, bounded contexts; resolves overloaded terms; produces `CONTEXT.md` and ADRs |
| `harden-architecture` | Module boundaries, seams, deep modules, interface contracts, dependency rules; produces `DESIGN.md` |
| `challenge-approach` | Adversarial review of design decisions; stress-tests the plan before committing |

Run `engineer-domain-model` first to settle shared vocabulary, then `harden-architecture` to define the system structure, then `challenge-approach` to pressure-test it. The exit artifact is `DESIGN.md` with ADRs that the build phase implements against.

### Phase 3: Component extraction (composable space)

**Question:** Can we turn proven one-off work into reusable assets?

| Skill | Owns |
| --- | --- |
| `audit-architecture` | Assess existing architecture; identify structural debt and duplication; guides component extraction decisions |

Run `audit-architecture` after 2–3 features have stabilized patterns, not before. Extraction requires evidence of 3+ uses; earlier extraction creates premature abstractions.

## Agent/LLM projects (outside the standard SDLC loop)

These two skills apply only when building agent or LLM-powered systems. They do not belong in the main technical design loop for standard software.

| Skill | Owns |
| --- | --- |
| `design-agent-architecture` | LLM orchestration, tool calling, memory protocols, agent topology |
| `design-operational-ontology` | Operational concepts, taxonomy, and shared vocabulary for a domain |

Both skills offer an installed diagramming capability (a tool that renders a described structure into an exportable SVG, HTML, or image) and fall back to drawing inline. That offer is stateless: these skills hold no effort-scoped memory and write no capability record.

## Boundaries

Architecture decisions that need a record of their rationale belong in ADRs — scaffold them with `engineer-domain-model` or `harden-architecture`. Design review lives in `quality/review/review-architecture`. `audit-architecture` assesses the design; `quality/review/review-architecture` judges the implementation against it.
