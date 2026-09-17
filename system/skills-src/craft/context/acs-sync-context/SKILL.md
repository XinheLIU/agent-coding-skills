---
name: acs-sync-context
description: Detect and repair shared-context drift after setup. Use for broken routing, stale domain context, an outdated code index, or working memory that no longer matches repository state; use acs-init-context when routing is absent.
---

# Sync Context

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [context.configuration]
  retrieves: [context.changed_premises, run.state]
  produces: [context.drift_findings]
  updates: [context.routing, run.state]
  invalidates: [context.affected_dependents]
  handoff_to: [domain_owners, coordinator]
```

Shared semantics: [shared protocol](../acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Use the [protocol](references/PROTOCOL.md) and [document layout](references/canonical-doc-layout.md) for routing, freshness, ownership, and retention. When routing is absent, use `acs-init-context`; read-only inspection may proceed from explicit sources.

## Modes

- **Fast**: inspect routing and changed premises within the requested scope.
- **Full**: additionally reconcile affected domain context, active runs, optional indexes, and completion retention.

## Establish evidence

Use a requested revision/range, merge, release, or last successful sync as the baseline. A document date alone cannot establish freshness. Record relevant source revisions/environment and inspect changed paths, contracts, and dependencies. Follow only relevant domain records and reverse references derived from their forward relationships.

## Classify and route

Use the layout guide's `OK`, `UPDATE`, `STRUCTURAL`, `MISSING`, `MOVE`, `PROMOTE`, `COMPACT`, and `DELETE` dispositions. Every finding names evidence, owner, affected scope, and exact proposed action.

Current-state architecture, conventions, and runbooks may explain present truth with executable evidence; do not delete them just because code also describes structure. Historical decisions retain their prior verdict and rationale. Changing a premise marks only materially affected dependents `needs review`; route reassessment to their owner instead of silently rewriting another domain's judgment.

## Full-mode checks

- Active runs link canonical change/task status, useful next action, blockers, required references and revisions; do not maintain independent ticket status.
- Claims and shared writes follow serialized reconciliation. Repeated contributions with unchanged evidence create no duplicate records.
- Generated views can be rebuilt from declared sources. Query an enabled code index against source or refresh it using its recorded command.
- Product HTML is a semantic source under [the Product contract](references/product-memory.md), not a generated view; preserve record IDs, authority, and active review findings.
- Design acceptance preserved consequential rationale under [the Design contract](../acs-init-context/references/design-memory.md), independently of component documentation.
- Final verification identifies criteria, code/diff revision, environment, failures, omissions, and release references where applicable.

## Completion retention

Follow the protocol's retention gate. Retain the canonical ticket/spec, accepted designs/contracts, consequential decisions, compact verification and release references in Change Context. Reconcile applicable Current State. Verify all essential links and rationale with the run directory unavailable before removing execution plans, raw outputs, claims, temporary excerpts, or handoffs. A tracked spec does not become disposable on implementation.

## Apply and verify

The coordinator may repair factual routing, refresh derived indexes/views, and apply already authorized updates. Return domain findings to their owners; absent a specialized skill, the active agent can perform competent domain work under its contract. Ask only for unresolved decisions or actions outside existing authorization, naming the concrete proposed change.

Preserve unrelated/user-authored records, update Markdown dates, and verify changed references. Report applied, deferred, and still-blocked findings with scope and evidence. Synchronization is complete only when all applied actions are verified and retained change records survive cleanup. No commit is implied.
