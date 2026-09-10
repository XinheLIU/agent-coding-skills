# Shared Context Protocol

Last updated: 2026-09-09

This is the suite's canonical lifecycle, identity, ownership, and handoff contract. Domain contracts specialize artifact meaning; workflows coordinate execution. It applies to standalone skills as well as composed workflows.

## Four lifecycles

| Lifecycle | Contains | Retention |
| --- | --- | --- |
| North Star | Mission, vision, principles, non-goals | Durable; revised through explicit decisions |
| Current State | Current product behavior, applicable design rules, system boundaries, operational constraints | Maintain present truth with evidence and relevant revision/environment |
| Change Context | Canonical ticket, requirements, accepted designs/contracts, consequential decisions, verification summary, release references | Retain a compact record after completion or abandonment |
| Run Context | Execution plan, claims, scratch analysis, temporary assumptions, raw outputs, session handoff | Remove only after durable information is reconciled |

Classify records, not file extensions or workflow stages. Several lifecycles may share a document: label the record's role explicitly when it would otherwise be ambiguous. Current-state records contain current assertions; change records and ADRs contain historical deltas and rationale. An accepted change does not establish shipped behavior.

Code indexes are derived views, not a lifecycle. Current-state summaries may explain structure; code, schemas, tests, and configuration establish executable facts. Record source revision and environment where they affect interpretation. Refresh a generated index with its owning tool, and confirm results against source before acting.

Keep established HTML and Markdown formats. Product HTML records are semantic sources with no Markdown twin; engineering HTML roadmaps remain derived from canonical tickets. `Last updated` is required documentation metadata, not proof of freshness.

## Repository configuration and resolution

`docs/agents/memory.md` records existing tracker locations, the work root, active-change selection, domain paths, product identity, and optional index commands. Defaults apply only when a home is not already established:

- Durable local changes: tracked `docs/changes/<change-id>/`.
- Run Context: `<work-root>/<effort>/`, default `.scratch/<effort>/`.
- Product: `docs/product/<product-slug>/product.html`.

The coordinator resolves explicit user references first, then memory configuration and active-state pointers, then an unambiguous branch mapping. A branch or directory name never replaces an existing ticket ID. Ask when multiple candidates remain. Without configuration, read-only work can use supplied sources; use unambiguous existing homes or these defaults for authorized persistence, and use `init-context` when routing remains ambiguous.

For a cold session: resolve change/task identity and canonical status; read Run Context's next action if present; load only the required and relevant optional records declared by the skill, including their evidence and active review findings. Absence of a prior skill's output does not require rerunning a pipeline when the substantive answer already exists. Missing substantive input blocks only dependent work.

## One change, multiple contributions

Use the same canonical ticket ID across Product, Design, Implementation, Testing, and Release. Requirements and acceptance criteria have one canonical spec, with stable requirement/criterion IDs. `spec` consumes an existing spec; only when none exists does it create requirements under [the Product contract](product-memory.md). Plans, tickets, designs, and tests reference criteria rather than copying normative text.

Technical contracts and accepted decisions remain separately addressable and link to the change. For independently deliverable slices, `tasks` creates child tickets with parent references and dependencies. Fine-grained execution steps are a Run Context checklist, not a second ticket system. Preserve established trackers and their field spellings.

Canonical ticket status lives once: in the existing tracker, or in the local ticket record. A product roadmap ticket may itself be that record. Roadmaps and session state link to canonical status; any rendered status is a derived view labelled with its source revision. Child ticket status is distinct from parent status and does not automatically complete the parent.

## Relationships and freshness

Store forward relationships with the artifact; derive reverse references when needed:

| Field | Meaning |
| --- | --- |
| `depends_on` | Prerequisite record/ticket/contract, with consumed revision where material |
| `affects` | Behavior, surface, criterion, module, or environment changed or assessed |
| `supersedes` | Earlier decision or record replaced for a stated scope; keep its history |
| `status` | Domain-specific progress or decision state, using that domain's vocabulary |

In HTML, express these names as visible labelled links inside the record; in Markdown use labelled fields or existing frontmatter. Do not add a second metadata store. Requirement revisions, code commits or diff digests, document hashes, artifact digests, and environment/configuration versions are suitable consumed revisions; dates alone are not.

Freshness is separate from status: `current`, `needs review`, or `disputed`, with a changed-premise reference and affected scope. A completed ticket or accepted decision may need review without losing its historical status.

When a premise changes:

1. Record the new revision and delta.
2. Inspect dependents that consumed the relevant premise, including cross-domain consumers.
3. Mark materially affected conclusions `needs review`, naming the premise; where write authority is absent, create a linked review finding and notify the coordinator.
4. Route reassessment to the domain owner. Preserve prior decisions, evidence, and disputes.
5. Follow affected conclusions onward only where the premise matters; revalidate that scope and leave unrelated records current.

## Skill declarations

Every suite `SKILL.md` contains one fenced YAML block with all six list fields:

```yaml
context:
  requires: [change.requirements, design.relevant_decisions]
  retrieves: [system.affected_modules, operations.checks]
  produces: [change.implementation_evidence]
  updates: [run.execution_plan]
  invalidates: [verification.for_changed_code]
  handoff_to: [testing, code_review]
```

These are semantic selectors, not literal paths or mandatory skill names. Domain contracts resolve their artifact roles. `requires` names substantive inputs for the requested mode; `retrieves` names optional relevant context; `produces` names domain results; `updates` names owned records or proposed coordinated updates; `invalidates` identifies conclusions to assess, never permission to rewrite another domain's decisions; `handoff_to` names consumers, never automatic dispatch. Empty lists are valid. Apply only selectors relevant to the requested task; report missing input and its blocking effect.

Skills may be owners, record-level contributors, consumers, or transient operations. Ownership concerns facts and contribution authority, not exclusive ownership of an entire shared file. Keep domain reasoning, evidence interpretation, validation, and operational constraints inside the skill. Keep path/identity resolution, context assembly, runtime bindings, scheduling, claims, coordinated writes, freshness propagation, and cleanup in the coordinator. See [workflow coordination](../../../../../workflows/context-coordination.md).

## Domain ownership

| Domain | Owns / produces | Reads | Downstream evidence | Invalidated by |
| --- | --- | --- | --- | --- |
| Product | Problem, intent, priority, scope, requirements, criteria, product decisions | North Star, current capabilities, user evidence, constraints, feasibility | Change/spec IDs, criteria, boundaries, questions | Changed evidence, goals, behavior, feasibility |
| Design | UX/UI decisions, data/API/system/module contracts, alternatives, prototypes, warranted ADRs | Requirements, affected current state, patterns, constraints | Accepted decision/contract references, prototype sections, constraints | Requirements, shared contracts/tokens, architecture, disproved assumptions |
| Implementation | Decomposition, dependency/parallelization proposals, execution plan, code, implementation evidence | Change, accepted design, source/dependencies, criteria, checks | Revision/diff, surfaces, deviations, criterion references, verification needs | Requirements/design/dependencies, conflicting edits, failed verification |
| Testing | Expected-behavior coverage, tests, regressions, edge cases, failure history | Criteria, contracts, code, regression surface, environment | Criterion → test/evidence → revision mapping, failures, omissions, readiness | Relevant requirements, contracts, code, tests, environment |
| Refactoring | Preservation constraints, structural assessment, debt decisions, before/after evidence | Invariants, dependencies, accepted behavior, tests, rationale | Structural delta, preservation evidence, state/ADR amendments | Broken invariants, behavior/dependency changes, invalid baseline |
| DevOps / CI-CD | Environment, build/deploy config, constraints, migration/release/rollback decisions and evidence | Change, verified artifact/revision, CI, topology, contracts | Artifact, environment, gates, migration, observability, rollback references | Artifact/config/runtime/topology/migration/production-condition changes |

Load [Product](product-memory.md), [Design](design-memory.md), [engineering and verification](engineering-memory.md), or [Operations](operations-memory.md) detail only for the affected domain.

## Handoff envelope

Every cross-session or domain handoff contains:

```text
change/task identity + scope
references and consumed revisions
delta + accepted decision references
unresolved questions and blocking effects
next action
```

References must be accessible to the receiver, including across worktrees. If a reference cannot be shared directly, transport a bounded, revision-labelled excerpt as temporary Run Context, identifying its canonical source and expiry/revalidation condition. Do not turn the excerpt into a second requirements source. Persist consequential accepted decisions before handing off; private conversation is insufficient.

## Coordinated writes and claims

The coordinator serializes writes to each shared file/tracker record. Before applying a contribution it rereads the target and consumed premises, matches stable IDs, and reconciles against the current revision. Preserve unrelated edits and conflicting assessments; never use a stale whole-document replacement. Repeated reconciliation with unchanged inputs must create no duplicate records, tickets, or evidence.

Claims are exclusive Run Context records referencing canonical task identity and base revision. Acquire a claim only after rechecking dependencies and existing claims. Use an available atomic tracker operation or a single serialized writer; a Markdown field edit alone is not a lock. Without safe coordination, execute serially. A handoff transfers the claim explicitly; a context reset or expired session does not silently steal it. Release on verified completion, explicit abandonment, or coordinated transfer. Implementation proposes safe work boundaries; the coordinator schedules them.

## Retention and completion

Before removing Run Context:

1. Establish landed or abandoned outcome from repository/tracker evidence.
2. Retain the canonical ticket/spec, accepted designs/contracts and consequential rationale, compact verification summary (criteria, revision, environment, failures and omissions), and release references in Change Context. Abandoned changes retain the reason and unverified scope.
3. Reconcile current behavior, architecture, design rules, and operational state with evidence; preserve history in change records/ADRs. Do not present planned behavior as current.
4. Verify all essential references without the run directory, including accepted design rationale. Move unique required evidence before removing raw outputs; references to unavailable logs are insufficient.
5. Remove only reconciled execution plans, scratch, claims, temporary excerpts, raw outputs, and session handoffs, and repair routing.

Completion compacts Change Context; it does not delete requirements, accepted decisions, or final evidence by default. An archive is optional under repository retention rules. Do not promote an execution transcript wholesale. Preserve user-authored content, update Markdown dates and HTML record dates, and never store secrets or unnecessary personal data in shared context.
