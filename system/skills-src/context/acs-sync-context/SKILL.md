---
name: acs-sync-context
description: Inventory and classify every repository document into its memory class, then repair shared-context drift. Use for a whole-repository documentation audit, stale or abandoned plan documents, broken routing, stale domain context, an outdated code index, or working memory that no longer matches repository state. Presents a classification table and confirms the edit plan before moving, promoting, or removing anything; if routing is absent, inspect explicit sources read-only or use acs-init-context when setup is needed.
---

# Sync Context

Last updated: 2026-09-26

## Context contract

```yaml
context:
  requires: [repository.documents]
  retrieves: [context.configuration, context.changed_premises, run.state, change.completion_evidence]
  produces: [context.document_classification, context.drift_findings]
  updates: [context.routing, run.state, change.decision_records]
  invalidates: [context.affected_dependents, run.expired_working_memory]
  handoff_to: [domain_owners, coordinator]
```

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Use the [protocol](../../../protocols/skill-declarations.md) and [document layout](../acs-init-context/references/canonical-doc-layout.md) for routing, freshness, ownership, and retention, and [the census procedure](references/document-census.md) for inventory, effort verdicts, and why-extraction. Configuration is relevant context, not a precondition: absent routing, inspect explicit sources read-only and use `acs-init-context` when a repair needs routing.

## Modes

- **Fast**: narrow the census boundary to changed paths, report scoped findings, claim no completeness. Stops after step 3.
- **Full**: account for every document in the boundary, then reconcile affected domain context, active runs, optional indexes, and completion retention.

Steps 1 through 4 are read-only in both modes. An inventory-only request is Full mode declined at step 5.

## 1. Scope and baseline

State the mode, the baseline, and the census boundary in one sentence.

Use a requested revision/range, merge, release, or last successful sync as the baseline. A document date cannot establish freshness. Record relevant source revisions and environment.

## 2. Census

Account for every tracked `.md` and `.html` file in the boundary. Each lands in exactly one classification row, or inside one named exclusion rule carrying its file count. Read the configured `## Not context` rules before deriving any.

Complete when classified rows plus excluded counts equal the scan count, stated explicitly, with no row implied by "etc."

## 3. Classify

Give each row a memory class, a disposition, its evidence, and its owner, using the two axes in the layout guide. Every `NOT-CONTEXT` row names its reason code.

Class follows role, not location. A tracked, committed execution plan under `docs/` or the repository root is Working Memory that was misfiled, and retention applies to it.

Current-state architecture, conventions, and runbooks may explain present truth with executable evidence; do not delete them just because code also describes structure. Historical decisions retain their prior verdict and rationale. Changing a premise marks only materially affected dependents `needs review`; route reassessment to their owner instead of silently rewriting another domain's judgment.

Fast mode reports here and stops.

## 4. Decide effort state

Give each Working-class row `COMPLETE`, `PARTIAL`, `ONGOING`, or `ABANDONED` from the evidence ladder in the census procedure. A document's own checklist is not evidence of its state. `PARTIAL` and `ONGOING` rows keep their documents; name what remains and route it to its owner.

## 5. Confirm the plan

Persist the census, then present scope, exclusions, rows grouped by disposition with the destructive groups last and expanded, the close, and one question per disposition group.

Before this gate, apply nothing but in-place repair of broken links and stale paths within this skill's ownership, and list each one as applied — [ordinary factual updates need no approval](../../../protocols/presenter.md#review-reconciliation). `MOVE`, `PROMOTE`, `COMPACT`, `DELETE`, and `EXPIRE` require confirmation here, per group, naming exact paths. Existing explicit authorization for a named action persists and is not re-requested.

Complete when the user has confirmed, amended, or declined each group. Declining ends the run with the census as the deliverable. A non-interactive run stops here, records the unconfirmed plan as an open question, and applies nothing destructive.

## 6. Extract the why

For every confirmed `PROMOTE` or `EXPIRE` row, separate rationale from procedure, write one ADR per decision and one changelog line linked to the release reference, then verify a reader can answer why the repository is shaped this way with the source unavailable. Incomplete extraction leaves the row unexpired.

## 7. Full-mode checks

- Each active run has one configured recovery entry with canonical change/task references, one useful next action, blockers and required revisions. An internal scheduler file is linked detail, not a second next-action or ticket-status source.
- Claims and shared writes follow serialized reconciliation. Repeated contributions with unchanged evidence create no duplicate records.
- Proposed records required for review or downstream work already live in Persistent Memory; persistence does not imply acceptance.
- Review decisions bind actual feedback to subject, revision and scope; exact reviewed content/assets remain retrievable and duplicate feedback is a no-op under [Presenter](../../../protocols/presenter.md).
- Generated views can be rebuilt from declared sources. Query an enabled code index against source or refresh it using its recorded command.
- Product HTML is a semantic source under [the Product contract](../../../protocols/product-memory.md), not a generated view; preserve record IDs, authority, and active review findings.
- Design acceptance preserved consequential rationale under [the Design contract](../../../protocols/design-memory.md), independently of component documentation.
- Final verification identifies criteria, code/diff revision, environment, failures, omissions, and release references where applicable.

## Completion retention

Follow the protocol's retention gate. Retain the canonical ticket/spec, required proposals, accepted designs/contracts, exact reviewed content, consequential and review decisions, compact verification and release references in Persistent Changes. Reconcile applicable Persistent Current. Verify all essential links and rationale with the run directory unavailable before removing execution plans, raw outputs, claims, temporary excerpts, or handoffs. A tracked spec does not become disposable on implementation.

Working Memory past the configured retention window is presumed abandoned and may be expired once its unique durable facts are promoted and the user confirms. Age authorizes that decision; it does not waive promotion.

## 8. Apply, verify, report

Apply confirmed actions. Return domain findings to their owners; absent a specialized skill, the active agent can perform competent domain work under its contract. Ask only for actions outside existing authorization, naming the concrete proposed change.

Preserve unrelated and user-authored records, update Markdown dates, and verify changed references. Record the retention outcome as a Persistent Changes entry naming what was removed and on what basis. Report applied, deferred, and still-blocked findings with scope and evidence. Synchronization is complete only when all applied actions are verified and retained change records survive cleanup with removed sources unavailable. No commit is implied.
