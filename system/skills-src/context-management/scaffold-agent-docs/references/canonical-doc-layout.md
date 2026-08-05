# Canonical Documentation Layout

Read this reference when classifying documents or proposing their canonical homes.

## Ownership model

Prefer a MECE layout: each doc has one primary job and one canonical home. Two levels is usually sufficient; optimize for discoverability rather than perfect taxonomy.

- Root `README.md`: shortest possible entrypoint to the repository.
- Root context files such as `AGENTS.md` and `CLAUDE.md`: contributor or runtime instructions that must remain at repository root.
- `docs/architecture/`: how the system works — architecture, C4 diagrams, domain/data models, core workflows, entry points, external dependencies, service contracts, critical paths, and scalability/security considerations.
- `docs/product/`: what is being built and why — vision, capability map, boundaries, personas, journeys, user stories, PRDs, and acceptance criteria.
- `docs/conventions/`: how software is written — coding, naming, API, testing, logging, configuration, Git, and deployment conventions.
- `docs/quality/`: what good looks like — Definition of Done, quality gates, test strategy, performance, reliability, security, and release checklists.
- `docs/tech-decisions/`: why choices were made — tradeoffs, alternatives, and decisions with outcomes.
- `docs/runbooks/`: how the system is operated — deployment, monitoring, incident response, recovery, and troubleshooting.
- `docs/data/`: shared data meaning — metrics, semantic layer, entities, data contracts, quality rules, feature definitions, and lineage.
- `docs/agents/`: agent-specific architecture and behavior — skills, tools, memory, planning, evaluation, guardrails, and prompting.
- `docs/exec-plans/`: execution and project management — active and completed plans, backlog, roadmap, technical debt, proposals, and postmortems.
- `docs/others/`: human documentation that needs further classification.

A new engineer should find relevant information within two clicks from `docs/`. Avoid finer categorization unless the repository has earned it.

## Execution-plan layout

```text
exec-plans/
├── active/              ← currently ongoing plans (empty directory, keep .gitkeep)
├── completed/           ← completed plans (empty directory, keep .gitkeep)
├── backlog.md           ← pending, unscheduled requirements
└── tech-debt-tracker.md ← known technical debt
```

## README rule

Keep a module README only when it is the right local entrypoint for its directory. Move large durable reference material, detailed architecture, long workflows, and historical context into the canonical `docs/` structure. Leave behind a short local README with setup or discovery information and a direct link to the canonical document.

## Classification tests

For each in-scope document, choose one of:

- `KEEP IN PLACE`
- `MOVE to /docs/...`
- `SPLIT` — retain a short local entrypoint and move durable material to `docs/`.
- `MERGE into <target>`
- `DELETE (obsolete)`
- `NEEDS UPDATE`

Apply these tests:

1. Is this file an entrypoint or a reference? Entry points stay beside what they introduce; reference docs belong under `docs/`.
2. Does it overlap another doc's ownership? Choose one canonical home and trim or merge the rest.
3. Would a new contributor know where to look? If not, reorganize.
4. Is the location forcing duplication? Move durable content when local placement repeats architecture or workflows.
