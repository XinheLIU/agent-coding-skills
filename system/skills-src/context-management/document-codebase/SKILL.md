---
name: document-codebase
description: Generate or refresh codebase documentation — READMEs, ER diagrams, API references, C4 diagrams, module dependency charts, and entry-point traces. Use for initial engineer onboarding (full doc set) or targeted content refresh of a specific surface (invocable per surface by manage-context Phase B). Reuses existing SVGs and aligns with project conventions.
---

Last updated: 2026-08-02

# Codebase Onboarding

Onboard a new engineer to a codebase by generating documentation tailored to what's asked and what the codebase actually is. Write for a technical audience — the reader knows how to clone a repo and run a command.

The useful question is not "what files exist?". It is: **which directories represent the business model, which expose interfaces, and which are implementation mechanisms?**

## Rules

### Non-negotiable

1. **Audit before writing files.** Never generate a file until Phase 1 audit and Phase 2 approval are done.
2. **`Last updated: YYYY-MM-DD`** on every generated Markdown file, below the top-level heading.
3. **Professional tone.** Lead with invariants, constraints, and trade-offs. No "get running in 5 minutes!" phrasing, no decorative emoji, no "don't worry if you're new to X" caveats unless the project explicitly targets novices.
4. **Cite code with `path:line`.** Never paraphrase what a function does — point to it.
5. **Augment, don't duplicate.** If content exists elsewhere, link to it. If it's wrong, flag it in the proposal. Never create a shadow copy of an existing doc (e.g., a second `c4-context.md` under `docs/others/` when `docs/architecture/c4-context.md` already exists).
6. **Restructuring requires explicit approval.** Moving, splitting, or merging existing files is only allowed after the user says "yes" in Phase 2.
7. **Reuse existing rendered images.** If a project already has SVGs/PNGs (e.g. `docs/architecture.svg`), embed by relative path. Don't re-render. New diagrams default to Mermaid (text, renders inline).
8. **Structure before implementation.** Document the domain shape and interface surfaces before framework glue, storage details, deployment mechanics, or library choices.
9. **Architecture docs explain what, how, and why.** Every architecture artifact must state what concepts/components exist, how they interact, and why the important boundaries or technologies were chosen.
10. **Use the Model / Interface / Implementation spine.**
    - **Model** — the concepts this software is built around and the problem those concepts solve.
    - **Interface** — how the model exposes capabilities to users, callers, tools, and developers: REST resources, commands, events, public APIs, SDK calls, scheduled jobs.
    - **Implementation** — how model and interface are realized internally: databases, queues, caches, storage, framework glue, concurrency model, deployment shape, external services, and key technologies.
11. **Entry points are the coordinate origin.** Every main flow starts from an external trigger: HTTP route, command, event/message consumer, scheduled job, SDK call, or public library export.

### Defaults (override when the codebase or project conventions justify it)

These are starting positions, not laws. Each default lists when to deviate.

12. **Defer docstring rules to per-tree `AGENTS.md`** (e.g. `src/AGENTS.md`, `tests/AGENTS.md`) when present. *Override:* project has no such files and the user asks for inline-comment guidance — propose conventions inline, don't invent a docstring spec for them silently.
13. **C4 + Mermaid for architecture visuals.** *Override by shape:* libraries want module trees or call graphs, CLIs want command maps, pipelines want flow diagrams, notebook repos want an experiment index. C4 is for service / microservice / mixed-monorepo shapes. ASCII is fine for ≤5-box layered summaries; never for module graphs, ER, or anything that needs layout.
14. **Root README leads with pitch + badges + screenshot.** *Override:* internal services / agent runtimes / private monorepos can lead with "What this is", invariants, and a local-run section instead. Badges and screenshots are required for user-facing OSS/apps; optional otherwise. `references/readme-template.md` is the reference either way.
15. **Generated docs follow the two-level `docs/` convention (e.g. `docs/architecture/`, `docs/data/`).** *Override:* if the project already uses mdBook (`src/`), Docusaurus (`docs/` with sidebars), a wiki, or another established layout — align with it. Detect convention during Phase 1 and pick the target in Phase 2. The root `README.md` always stays at the repo root.
16. **Six-item coverage check on `AGENTS.md` / `AGENTS.md`.** *Override:* if neither file exists, check `CONTRIBUTING.md` / top-level `docs/` instead, or skip if the project has no agent-memory convention. When the files do exist, verify they cover:
    1. What the project does and why it exists.
    2. Architecture decisions and their rationale.
    3. Business rules, edge cases, constraints.
    4. Naming conventions, code style, design principles.
    5. Build, test, run instructions.
    6. Anti-patterns: things that look right in this codebase but aren't.

    Report gaps in the Phase 4 summary. Don't edit those files (defer to `review-Codex-md`).

## Workflow

### Phase 0 — Mode select

Pick one before doing anything else. Restate the chosen mode to the user in one sentence so they can redirect.

| Mode                | Trigger phrasing                                                                                      | What it produces                                                                       | Audit depth                               |
| ------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------- |
| **targeted-doc**    | "write the README", "generate an ER diagram", "document the API", "draw the module deps"              | One or two specific docs. Skip the gap table; only audit what the requested doc needs. | Narrow — only the surface the doc covers. |
| **full-onboarding** | "onboard me to this codebase end-to-end", "document the whole repo", "produce the onboarding doc set" | Full doc set per the shape × tier rubric below.                                        | Full — Phase 1 gap table required.        |

If the request is ambiguous ("onboard me to this codebase"), ask: *Do you want a specific doc, or the full doc set?* Don't assume.

### Phase 1 — Audit

Scope the audit to the mode chosen in Phase 0. **targeted-doc** audits only the surface the requested doc covers (e.g. "write the README" → check whether a README exists and whether install/run is current; skip the rest). **full-onboarding** runs the full table below.

Also detect, in any mode:

- **Codebase shape** — service / library / CLI / pipeline / ML-repo / mixed. Used by Phase 2 to pick deliverables (see [Shape × tier rubric](#shape--tier-rubric)).
- **Existing docs convention** — `docs/`, `documentation/`, mdBook (`book.toml` + `src/`), Docusaurus (`docusaurus.config.*`), wiki, or none. Used to align output location with project convention (default rule 15 override).
- **Model / Interface / Implementation split** — identify the domain concepts, the surfaces that expose them, and the replaceable implementation mechanisms.
- **Module roles** — classify meaningful directories/modules before describing internals:

| Module type         | Question to ask                                                            | Why it matters                                                      |
| ------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Core domain         | Would the product still be the same without this?                          | This is where model understanding matters most.                     |
| Interface adapter   | Does this expose the system through HTTP, CLI, RPC, jobs, or messages?     | These are entry points into the model.                              |
| Infrastructure      | Is this database, queue, cache, auth, logging, config, or deployment code? | These are implementation choices and should usually be replaceable. |
| Shared utility      | Is this used everywhere but owns no domain concept?                        | These create broad blast radius.                                    |
| Legacy or migration | Does this preserve an old contract or transition path?                     | These often explain strange constraints.                            |

For full-onboarding on Complex projects, and only when the runtime supports it and the user explicitly asks for or allows subagents, run independent read-only explorer subagents for bounded surfaces such as entry points, data model, API surface, module dependency graph, or external dependencies. Give each explorer a specific question and do not duplicate their work locally unless their output conflicts with cited code.

Enumerate what exists before proposing anything. Produce a gap table.

```
├── Root README.md?              present / missing / stale
├── docs/                        present / missing
│   ├── architecture/            present / missing
│   │   ├── overview.md          narrative + layer summary
│   │   ├── entry-points.md      external contract (HTTP / MCP / CLI / cron)
│   │   ├── c4-context.md        present → link from index, do NOT recreate
│   │   ├── c4-containers.md     present → link from index, do NOT recreate
│   │   ├── module-deps.md       internal modules, cycles flagged
│   │   ├── external-deps.md     language deps / middleware / external APIs
│   │   └── *.svg                enumerate (will be embedded if relevant)
│   ├── data/
│   │   └── data-model.md        ER diagram + per-table breakdown
│   ├── conventions/
│   │   └── configuration.md     present / missing
│   │   ├── api-reference.md     grouped by owning module
│   ├── runbooks/
│   │   └── env-checklist.md     present / missing
│   ├── tech-decisions/          present / missing
│   └── others/                  catch-all for uncategorized existing docs
├── AGENTS.md / AGENTS.md chain  enumerate all
└── Inline docstrings            sample coverage: high / low / mixed
```

Report format:

| Doc type              | Exists? | Location                 | Health                                 |
| --------------------- | ------- | ------------------------ | -------------------------------------- |
| README                | yes     | `./README.md`            | stale — no install steps               |
| Arch (Context)        | no      | —                        | —                                      |
| Arch (Containers)     | no      | —                        | —                                      |
| Module-deps diagram   | no      | —                        | —                                      |
| External-deps diagram | partial | `docs/external-deps.svg` | rendered SVG only, no doc page         |
| Entry-point trace     | no      | —                        | —                                      |
| Data model / ER       | no      | —                        | —                                      |
| API reference         | partial | `docs/API.md`            | covers 3/7 endpoints                   |
| ADRs                  | no      | —                        | —                                      |
| Context-file coverage | partial | `AGENTS.md`, `AGENTS.md` | missing: anti-patterns, business rules |

Also run a **complexity triage** (see [Shape × tier rubric](#shape--tier-rubric) below) to tier the project.

The audit notes must preserve this order:

1. **Model** — core concepts, business nouns, states, lifecycle, and the problem they solve.
2. **Interface** — external ways to use those concepts: HTTP resources, CLI commands, MCP/RPC tools, events/messages, public APIs/SDKs, scheduled jobs.
3. **Implementation** — internal modules, key technologies, storage, queues, caches, framework glue, concurrency model, deployment shape, and external services.

### Phase 2 — Propose

Present a concrete diff plan. Block until the user approves.

```
Proposed changes:
  CREATE  docs/README.md                                                (index)
  CREATE  docs/architecture/entry-points.md
  CREATE  docs/architecture/overview.md                                 (embeds docs/architecture.svg)
  CREATE  docs/architecture/c4-context.md
  CREATE  docs/architecture/c4-containers.md
  CREATE  docs/architecture/module-deps.md                              (embeds docs/module-deps.svg; cycle list)
  CREATE  docs/architecture/external-deps.md                            (embeds docs/external-deps.svg)
  CREATE  docs/architecture/api-reference.md                            (grouped by module; currently scattered)
  CREATE  docs/data/data-model.md
  UPDATE  README.md    (add "Invariants & constraints" section; refresh install)

  NO CHANGE: docs/conventions/configuration.md  (current content is accurate)
  NO CHANGE: docs/tech-decisions/               (ADRs are the user's responsibility)
  NO CHANGE: AGENTS.md, AGENTS.md   (gaps listed in Context-file gaps section; defer edits to review-Codex-md)

Restructuring (requires explicit yes):
  NONE

Context-file gaps (flagged, not edited):
  AGENTS.md  missing: anti-patterns section
  AGENTS.md  missing: business rules / edge cases

Rationale:
  Complexity tier: Complex (see [signals]).
  Gaps: missing entry-point trace; module/external-dep docs only exist as SVGs without prose; API doc covers 3/7 endpoints; no ER diagram.
```

For restructuring proposals, list every source → target with a one-line reason. Never move or delete without an explicit "yes".

### Phase 3 — Generate

Write per the deliverables chosen in Phase 2. Use `assets/templates/` as starting points; load `references/*.md` on demand.

Per file:
1. Fill the template with project-specific content.
2. Replace placeholders with real examples from the code (cite `path:line`).
3. For architecture docs, force the narrative through **what / how / why**:
   - **What**: the model concepts and modules.
   - **How**: the interface surfaces and internal realization.
   - **Why**: the constraints, trade-offs, and technology choices.
4. For entry-point docs, trace each non-trivial flow:
   - What object or function receives external input?
   - Where does input validation happen?
   - Where does external language become domain language?
   - Which module owns the actual business decision?
   - Where do implementation details enter: database, queue, filesystem, network, cache?
   - What does the caller receive back?
5. For data-model docs, inspect data models, DTOs, and table-creation SQL. For each canonical model, list field names, types, one-sentence purpose, primary keys, foreign keys, enumeration values, and relationships. Include a Mermaid ER diagram.
6. For API docs, classify each surface as resource-oriented, action-oriented, event-oriented, or command-oriented. Group REST APIs by owning module and list method, path, one-sentence description, main request parameters, and response structure.
7. Before saving any C4 Mermaid block, run the layout-quality checklist:
   - Count elements: ≤15?
   - Count edges: ≤ elements × 1.5?
   - Every relationship label ≤40 chars?
   - `UpdateLayoutConfig` present for diagrams with ≥5 elements?
   - No `BiRel`?
   - All aliases defined before first use?
   If any check fails, fix before proceeding — don't leave layout problems for the viewer to discover.
8. Add `Last updated:` at today's date.
9. Cross-link related docs.
10. **Environment Checklist Task:** If the user asks for an environment checklist or full-onboarding, execute this exact task (via subagent or directly):
    ```text
    You are my environment engineer for this project.

    Task:
    Analyze this codebase and produce a complete list of all external dependencies required to RUN the project locally.

    Scope of analysis:
    - docs/external-deps.svg
    - application*.yml
    - pom.xml
    - README (and any other obvious docs in docs/)

    Deliverable: a file docs/runbooks/env-checklist.md containing a dependency checklist.

    For EACH dependency, list:
    - Name
    - Version requirement (at least major version, e.g. 8.x, 2.x)
    - Default ports
    - Connection information (host, port, credentials pattern or env vars)
    - Initialization requirements, for example:

    Output format:
    - Markdown file docs/runbooks/env-checklist.md
    - Organized by category (e.g. Databases, Config/Registry, Messaging, Monitoring, External APIs)
    - Use bullet points or small tables so teammates can read and act on it quickly.
    ```
11. **Critical Paths Task:** If the user asks for critical test paths or core testing links, execute this exact task (via subagent or directly):
    ```text
    Based on docs/architecture/api-reference.md, docs/data/data-model.md, and AGENTS.md, list the core critical paths most worth testing in this project. Requirements:
    - No more than 8 paths in total, fewer is better.
    - Must be paths that are "prone to breaking during modifications", not all paths.
    - For each path, include: Path Name, Origin (which interface), Key Nodes (which service / DB operations), and End Point (what state counts as success).
    Summarize the output in a table. Save to docs/architecture/critical-paths.md.
    ```

### Phase 4 — Verify

Check **only the items that apply to docs you generated.** Skip the rest.

Universal (always check when files were written):
- [ ] `Last updated:` present on every new or edited `.md`.
- [ ] All `path:line` citations point to real locations.
- [ ] All internal links resolve.
- [ ] No duplication with existing docs.
- [ ] Embedded SVG paths resolve (relative to the generated doc).

Conditional (check only if the corresponding deliverable was produced):
- [ ] Mermaid blocks parse (no unmatched braces, all aliases defined before use).
- [ ] C4 diagrams pass the Phase 3 layout-quality checklist.
- [ ] Module-deps doc lists any detected cycles; cycle edges highlighted in Mermaid.
- [ ] External-deps doc groups deps into language / middleware / external-API buckets, color-coded.
- [ ] Entry-point doc cites `file:line` for each route, MCP tool, CLI command, or scheduled job.
- [ ] Entry-point doc traces external input → validation → domain language → business decision → implementation detail → caller output for each non-trivial flow.
- [ ] Data-model doc includes an ER diagram + per-table sections (fields, PK/FK, enums, schema owner).
- [ ] API doc groups REST routes by module and records method, path, request parameters, response structure, error shape, and orientation (resource/action/event/command).
- [ ] Architecture overview has explicit Model, Interface, Implementation, module-role taxonomy, and key technology sections.
- [ ] Review checklist in `references/doc-types-playbook.md` passes for prose-heavy docs.
- [ ] Environment checklist includes versions, ports, and connection information for every external dependency.
- [ ] Critical paths list contains ≤8 entries in a table format with specific origin, nodes, and success states.

For full-onboarding mode only:
- [ ] Context-file coverage check (rule 16) run; gaps reported.

Report back with a short summary: what was created, what was updated, anything deferred to the user, and — when in full-onboarding mode — a **Context-file gaps** section listing any of the six items missing from `AGENTS.md` / `AGENTS.md`.

## Shape × tier rubric

Two axes pick the deliverables: **shape** (what kind of codebase is this?) and **tier** (how complex?). Tier signals are OR'd — one strong signal promotes. Shape signals are detected from the project's entry points and top-level structure.

### Tier signals

| Tier        | Signals                                                                               |
| ----------- | ------------------------------------------------------------------------------------- |
| **Simple**  | <2k LOC AND single module AND no external services                                    |
| **Medium**  | 2k–20k LOC OR 3–10 modules OR 1–2 external integrations                               |
| **Complex** | >20k LOC OR microservices OR async workflows OR multi-team OR multi-region deployment |

### Shape detection

| Shape        | Tells                                                                                                   | Onboarding priority                                                           |
| ------------ | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **service**  | HTTP/gRPC/MCP server, `main.py` / `app.py` / `cmd/`, Dockerfile + Compose                               | Entry points, API ref, container architecture                                 |
| **library**  | `pyproject.toml` / `setup.py` with packages and no server entry, public-API `__init__.py`, examples dir | Public API surface, module tree, key abstractions, usage examples             |
| **CLI**      | `console_scripts` / `bin/`, argparse / click / typer entry, no server                                   | Command map, subcommand reference, config/env vars                            |
| **pipeline** | Cron / Airflow / Prefect DAGs, ETL scripts, scheduler entry, batch jobs                                 | Job inventory, data-flow diagram, schedule + lineage, schema ownership        |
| **ML-repo**  | `notebooks/`, MLflow / W&B, experiment configs, model registry calls                                    | Experiment index, dataset/feature lineage, training run reference             |
| **mixed**    | Monorepo combining ≥2 of the above (this project: services + pipelines + ML examples)                   | Per-component shape applied to that sub-tree; one top-level reading-order doc |

### Deliverables by shape × tier

Use this as a starting position. Override when a deliverable would not help a real reader.

| Shape        | Simple                                 | Medium                                                                                                         | Complex                                                                                                                      |
| ------------ | -------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **service**  | README + entry-points (if any surface) | + C4 context + C4 containers + external-deps + API reference                                                   | + module-deps + data-model (ER) + per-container component diagrams + dynamic diagrams for critical flows + deployment + ADRs |
| **library**  | README (usage front-and-center)        | + public-API reference + module tree (Mermaid)                                                                 | + module-deps with cycle detection + key-abstractions doc + ADRs for non-obvious API choices                                 |
| **CLI**      | README with command examples           | + command reference (one section per subcommand) + config/env-var table                                        | + module-deps if internals are non-trivial + ADRs                                                                            |
| **pipeline** | README + job list                      | + data-flow diagram + per-job spec (inputs/outputs/schedule) + external-deps                                   | + lineage / schema-ownership doc + ER for produced tables + retry/idempotency notes                                          |
| **ML-repo**  | README + experiment list               | + experiment index + dataset card per dataset                                                                  | + feature lineage + model registry reference + reproducibility runbook                                                       |
| **mixed**    | README + reading-order                 | + one C4 container diagram across components + per-component Medium deliverables for sub-trees that warrant it | Full Complex deliverables, scoped per sub-tree; one top-level index doc that maps reader → entry point                       |

### Diagram-vs-no-diagram check

Tier and shape are starting points, not mandates. Before producing any diagram, ask: *would a new engineer learn something non-obvious from this?* If the architecture is conceptually straightforward — a single app talking to one database, a CLI with no service boundary, a script pipeline whose flow is the file list — skip the diagram. A prose description with `path:line` citations beats a diagram that maps 1-to-1 with code.

When in doubt, ask. Four diagrams nobody reads is worse than two diagrams everyone reads.

## Doc-type menu

The skill picks from this set first. It's a menu, not a fixed list — if a specific codebase needs something outside it (e.g. a plugin-architecture map, a protocol-buffer reference), produce that instead and note the deviation in Phase 2. Confirm with the user before introducing types far outside this set.

File paths below assume the standard two-level `docs/` convention; align with the project's existing docs convention when one is in use (rule 15).

### Always-useful onboarding artifacts

| Doc type            | File                                                 | When                                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project README      | `./README.md`                                        | Always. Follow `references/readme-template.md`; sub-package READMEs may skip badges and screenshots.                                                                                         |
| Reading-order guide | `docs/architecture/reading-order.md` or top of index | When a new reader has more than one valid starting point (mixed-shape monorepos, libraries with both API and CLI). 5–10 file pointers in the order to read them, each with a one-line "why". |
| Glossary            | `docs/architecture/glossary.md`                      | When the codebase uses domain terms that aren't obvious from code (RTB, ODS/DWD, TaskPlan, etc.).                                                                                            |
| Codebase-doc index  | `docs/README.md`                                     | When ≥3 onboarding docs are generated. One-page map of everything below.                                                                                                                     |

### Entry / surface

| Doc type          | File                                   | When                                                                                                                         |
| ----------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Entry-point trace | `docs/architecture/entry-points.md`    | Any HTTP / MCP / CLI / scheduled surface. Cite `file:line` per route/command/job. See `references/entry-points-playbook.md`. |
| Command reference | `docs/architecture/commands.md` (CLIs) | CLI shape — one section per subcommand, including flags, env vars, exit codes.                                               |
| API reference     | `docs/architecture/api-reference.md`   | Public HTTP / MCP / SDK surface. Group by owning module.                                                                     |

### Architecture

| Doc type               | File                                           | When                                                                                                              |
| ---------------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Architecture overview  | `docs/architecture/overview.md`                | Service/mixed Medium+ when containers need cross-referencing; embeds existing `docs/architecture.svg` if present. |
| System Context (C4 L1) | `docs/architecture/c4-context.md`              | Service/mixed Medium+. Skip and link if `docs/architecture/c4-context.md` exists.                                 |
| Container (C4 L2)      | `docs/architecture/c4-containers.md`           | Service/mixed Medium+. Skip and link if exists.                                                                   |
| Component (C4 L3)      | `docs/architecture/c4-components-{feature}.md` | Service/mixed Complex, per non-trivial container.                                                                 |
| Dynamic (C4 sequence)  | `docs/architecture/c4-dynamic-{flow}.md`       | Complex, per critical cross-container flow (auth, payments, sagas).                                               |
| Deployment (C4 L4)     | `docs/architecture/c4-deployment.md`           | Complex production systems.                                                                                       |
| Module dependency      | `docs/architecture/module-deps.md`             | Library/mixed Complex, or any tier where cycles are suspected. Cycles in red.                                     |
| External dependency    | `docs/architecture/external-deps.md`           | Medium+ with non-trivial integrations. 3 color buckets: language / middleware / external APIs.                    |
| Module tree (library)  | `docs/architecture/module-tree.md`             | Library shape — hierarchy of public packages and their responsibilities.                                          |
| Data-flow diagram      | `docs/architecture/data-flow.md`               | Pipeline shape. Source → transform → sink with schedule and retry/idempotency notes.                              |

### Data

| Doc type        | File                      | When                                                                                     |
| --------------- | ------------------------- | ---------------------------------------------------------------------------------------- |
| Data model / ER | `docs/data/data-model.md` | Service/pipeline Complex. ER + per-table fields/PK/FK/enums/schema-owner.                |
| Dataset card    | `docs/data/{dataset}.md`  | ML-repo or pipeline shape — one per first-class dataset; schema, source, refresh, owner. |
| Feature lineage | `docs/data/lineage.md`    | ML-repo Complex. Upstream tables → features → models.                                    |

### Ops / runtime

| Doc type                | File                                                        | When                                                                                                                             |
| ----------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Configuration reference | `docs/conventions/configuration.md`                         | Non-trivial config surface. Kept at canonical path if already there.                                                             |
| Runbook / operations    | `docs/runbooks/OPERATIONS.md` or `docs/runbooks/runbook.md` | Anything deployed (service/pipeline). Health checks, common failures, recovery. Link to existing playbook instead of recreating. |
| Experiment index        | `docs/data/experiments.md`                                  | ML-repo shape. One row per experiment with hypothesis, status, link to MLflow/W&B run.                                           |
| Environment checklist   | `docs/runbooks/env-checklist.md`                            | When requested or as part of full-onboarding. Lists external dependencies and initialization requirements.                       |
| Critical test paths     | `docs/architecture/critical-paths.md`                       | When requested for QA/testing focus. Lists ≤8 most fragile end-to-end flows.                                                     |

### Governance

| Doc type                | File                                 | When                                                                                                       |
| ----------------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| ADRs                    | `docs/tech-decisions/00X-{title}.md` | Complex, or when a decision is load-bearing. Keep at canonical `docs/tech-decisions/`.                     |
| Inline docstrings       | In source files                      | Always; deferred to project's own rules (rule 8).                                                          |
| Context-file gap report | Phase 4 summary, no file             | Always for full-onboarding mode. Flags missing items per rule 16. Does not edit `AGENTS.md` / `AGENTS.md`. |

## C4 essentials (compressed)

Full reference: `references/c4-syntax.md`. Anti-patterns: `references/c4-anti-patterns.md`. Advanced patterns (microservices, event-driven, deployment, CQRS, multi-region): `references/c4-advanced-patterns.md`.

### Hard rules

1. **Every element has**: name, type, technology (where applicable), one-line description.
2. **Unidirectional arrows only.** `BiRel` is banned — split into two `Rel` statements that name each direction.
3. **Label every arrow with an action verb + technology/protocol.** `Rel(web, api, "Fetches expenses", "JSON/HTTPS")` — not `"uses"`.
4. **≤15 elements per diagram** (Mermaid's Dagre layout degrades past 15 even though the C4 model allows 20). Split by bounded context when over.
5. **Always include a title.** `title System Context — Personal Accountant`.
6. **Typed aliases**: `Container` (deployable), `ContainerDb` (database), `ContainerQueue` (topic/queue), `Component` (non-deployable, inside a container). Containers and components are different kinds of thing — never mix.
7. **Start at Level 1.** Context + Container together are sufficient for most teams. Only add Component / Deployment / Dynamic when they earn their keep.
8. **Relationship label length: ≤40 characters.** Verb + protocol/technology only — no parenthetical detail. Move extra context into the element's own description field, not the arrow label. Long labels collide on crossing edges in Mermaid.
9. **`UpdateLayoutConfig` is mandatory for any C4Container or C4Context with ≥5 elements.** Start with `UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")` and tune upward if elements cluster naturally in rows. See `references/c4-syntax.md` for tuning guidance.
10. **Edge-density limit: edges must not exceed elements × 1.5.** Count before generating: if `|edges| > |elements| × 1.5`, split into focused sub-diagrams (one container + its direct dependencies) rather than producing one dense diagram.

### Output locations

Default tree (following the standard two-level docs/ convention):

```text
docs/
├── README.md                       # index + map to all generated docs
├── architecture/
│   ├── overview.md                 # narrative + ≤5-box ASCII layer summary; embeds docs/architecture.svg if present
│   ├── entry-points.md             # external contract: HTTP / MCP / CLI / cron
│   ├── api-reference.md            # grouped by owning module
│   ├── c4-context.md               # Level 1 — required for Medium+
│   ├── c4-containers.md            # Level 2 — required for Medium+
│   ├── c4-components-{X}.md        # Level 3 — one per non-trivial container
│   ├── c4-dynamic-{flow}.md        # One per critical flow
│   ├── c4-deployment.md            # Level 4 — for production systems
│   ├── module-deps.md              # internal modules; cycles in red
│   └── external-deps.md            # 3 colored groups
├── data/
│   └── data-model.md               # ER diagram + per-table breakdown
├── runbooks/
│   └── env-checklist.md            # initialization requirements
└── tech-decisions/                 # ADRs
```

Existing rendered SVGs at the repo root or under `docs/` (e.g. `docs/architecture.svg`, `docs/module-deps.svg`, `docs/external-deps.svg`) are **embedded by relative path** from the corresponding generated `.md`, never regenerated.

### When to split a diagram

- More than 15 elements.
- Edge density exceeds elements × 1.5 (e.g., 12 nodes with 19+ edges) — crossing arrows will collide regardless of node count.
- Mixed ownership (multiple teams) at Container level — promote to Systems instead and give each team its own Container diagram.
- Mixed logical/physical concerns — split logical into Container, physical into Deployment.

## Existing-doc-aware behavior (project-specific)

Before proposing anything in a project, the audit MUST read:

- Root `AGENTS.md` (if present) — Global Rules, Workflows, Context-Files routing.
- Root `AGENTS.md` and `.Codex/rules/*.md` — rule entry points and path-scoped rules.
- Any `docs/AGENTS.md` — docs-local rules.
- Any `docs/spec.md` — project conventions and tech specs.
- Any pre-existing architecture / API / configuration docs under `docs/`.
- Any rendered diagrams under `docs/` (`*.svg`, `*.png`) — these are reused, not regenerated (rule 7).
- Per-tree `AGENTS.md` (e.g. `src/AGENTS.md`, `tests/AGENTS.md`) — if present, they own docstring rules for those trees.

Default stance: **augment with cross-links**, not rewrite. New docs go under the detected docs convention (or the standard two-level `docs/` convention as fallback) and link out to authoritative content that already exists (playbooks, ADRs, spec). Plug gaps (entry-point trace, module/external dep diagrams, ER, missing API coverage); never re-explain what's already written.

## Reference Triggers (Progressive Disclosure)

Load files from `references/` and `assets/templates/` **on demand only**, based on what you are generating:

- `readme-template.md` & `README.template.md` — Required before authoring or editing any root `README.md`.
- `doc-types-playbook.md` — Default companion for other prose-heavy docs.
- `c4-*` references — Default companions when writing any architecture diagram.
- `entry-points-playbook.md` & `ENTRY_POINTS.template.md` — Load when generating entry-point docs.
- `module-deps-playbook.md` — Load when generating module dependency diagrams.
- `external-deps-playbook.md` — Load when generating external dependency diagrams.
- `data-model-playbook.md` & `DATA_MODEL.template.md` & `CODE_COMMENTS.template.md` — Load when generating data models or code comments.
- `API.template.md` — Load when generating API references.
- `ARCHITECTURE.template.md` — Load when generating the architecture overview.

## Non-overlap with sibling skills

| If the user asks for...                                                                           | Use skill...                   |
| ------------------------------------------------------------------------------------------------- | ------------------------------ |
| Write / create / generate docs (any kind)                                                         | **document-codebase** (this) |
| Review code for quality/security                                                                  | `review-code-quality`          |
| Review the existing architecture's soundness                                                      | `review-architecture`          |
| Extract, classify, or document agent-behavior rules and conventions (static / dynamic / implicit) | `extract-rules`                |
| Review AGENTS.md and referenced docs for leanness                                                 | `review-Codex-md`              |

Words to watch: "document the architecture" → this skill. "review the architecture" → `review-architecture`. When ambiguous, ask.
