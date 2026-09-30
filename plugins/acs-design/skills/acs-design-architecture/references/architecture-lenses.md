# Architecture Lenses

Last updated: 2026-09-30

Deep mode applies these six lenses to the whole system or a subtree. For each lens, first **map** (read the listed sources and record facts with `file:line` anchors), then **judge** (apply the checks). Mapping stays in structure: do not read handler logic or query bodies.

A lens can run inline or as a delegated task. A delegated task gets this file's section for its lens as its whole instruction, plus the scope file list, and it returns anchored findings. It never writes to the record.

**Confidence.** `HIGH` = both the claim and at least one consumer or enforcement point have been read. `MEDIUM` = the map plus one side has been read. `LOW` = inferred from the map alone. Never promote a `LOW` finding to `P0`.

**Out of scope for every lens.** Code-level defects are `routed` to `acs-review-code-quality`, which applies them through its domain lenses.

## business

**Map:** the intent docs (spec, README, `AGENTS.md`/`CLAUDE.md`, design archives), then trace each documented capability to its entry point (CLI command, route, scheduled job).

**Checks:**
- A capability is documented but not implemented, or implemented but not documented.
- A persona has no working entry point, or an entry point serves no persona.
- A documented end-to-end flow cannot be executed, or a flow in code has no owner or success criterion.
- Scope creep beyond the stated mission, or a gap in the mission with no plan to close it.
- A KPI the system cannot measure, or a metric that no KPI uses.

## application

**Map:** each module's root, entry point and public surface; label files as Entry / Domain / Integration / Persistence / Config; list inter-module contracts (function, SQL, JSON, file), the runtime topology and the extension points. Compare against the architecture docs and diagrams.

**Checks:**
- A god module, a capability split with no clear seam, or a library/service split that contradicts the stated runtime.
- A layering inversion (persistence imports domain), a file that mixes concerns, or a missing domain layer.
- Callers reaching into internals, a contract duplicated across modules, or a public surface that leaks implementation detail.
- Sync where async is required (or the reverse), or hidden coupling through a shared process, file or row.
- A registry with no enforced schema, or an undocumented plugin slot.
- Docs and code that disagree.

## data

**Map:** schemas and migrations, the owner module of each schema (who creates it, who writes it), and producer → consumer lineage for each non-raw dataset.

**Checks:**
- A dataset in the wrong layer, a missing layer, or a consumer bypassing the layer contract.
- A module writing a schema it does not own, or two writers to one table.
- A producer–consumer pair with no stated schema, or a consumer that reads internal tables instead of a published view.
- Broken lineage, orphan tables, or a cycle through shared tables.
- Two stores claiming authority over one entity, or an entity with no owner.
- A reload model (append vs replace) that does not fit the use case, or inconsistent idempotency within a layer.

## technology

**Map:** the runtimes and key library versions, storage clients and where their connections are opened, the scheduler/async model per service, observability (logs, metrics, traces), and lockfile posture.

**Checks:**
- A database, scheduler or web server that does not fit the workload's read/write, batch or concurrency shape.
- A scaling cliff at 10× (single-process scheduler, one DB role, a stateful single replica), especially where scaling would force a rewrite.
- A system that cannot answer "is it healthy, what is it doing" without a code change.
- A missing lockfile, loose version ranges, a critical library with a stale upstream, or an end-of-life runtime.
- Incompatible runtimes across services that share libraries, or mixed package managers with no stated reason.
- A technology choice with no recorded rationale.

## deploy

**Map:** the deploy files (compose/k8s manifests, Dockerfiles, proxy config, `.env.example`, init SQL); for each service record its ports, networks, volumes, env, healthcheck and dependencies; the prod vs dev overrides; and which services are exposed.

**Checks:**
- An internal service bound to a host port, merged trust zones, or a proxy scope that does not match the trust model.
- No stated exposure model, stub healthchecks, or a restart policy that hides outages.
- A required env var missing from `.env.example`, working secrets shipped as defaults, secrets mixed with config, or the same value declared twice.
- A stateful volume with no backup story, or two writers to one volume.
- Dev-only defaults in prod, or dev and prod silently sharing migrations or data.
- A deploy-time migration or bootstrap with no order, owner or idempotency.
- "The internal network" used as the authentication boundary without being stated.

## adr

**Map:** the ADR folders, decision lines in `AGENTS.md`/`CLAUDE.md`/README, and implicit decisions (patterns that recur in every module). For each decision record where it is stated, where it is enforced and where it is violated.

**Checks:** give each decision one status. These fill `## Decisions` in the record:
- `Sound`: stated, enforced and still fits.
- `Reconsider`: enforced, but its assumption (scale, persona, regulation) has changed.
- `Missing-but-needed`: implicit, with 2 or more enforcement points and material consequences.
- `Drifted`: stated but violated at least once.
- `Stale`: written, but nothing relies on it.

Also flag decisions that conflict at a boundary, cross-cutting concerns with no decision, and rules that no test or lint enforces.

Anchor each decision to its ADR path when one exists. The coordinator turns non-`Sound` statuses into ADR edits under `## ADR upkeep` in the skill; a delegated lens only reports them.
