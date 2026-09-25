# Shared Protocols

Last updated: 2026-09-26

`system/protocols/` is the canonical source of shared memory, ownership and handoff contracts. Skills own domain reasoning; the active coordinator resolves and reconciles records; Presenter organizes human reading. The [accepted design](../resources/docs/context-memory-presenter-proposal.md) explains the two-memory model and its trade-offs.

The contracts layer cleanly; each file stays in its layer:

```text
L0  Memory model      Working | Persistent{Intent, Current, Changes} | derived views,
                      plus identity, freshness and retention — skill-declarations.md
L1  Domain records    which records exist, ownership, status semantics — product/design/
                      engineering/operations-memory.md (format-free)
L2  Formats           how records serialize — html-records.md; run-state, CONTEXT and
                      ADR templates under acs-init-context/references/
L3  Presenter         derived human views and review reconciliation — presenter.md,
                      indexing the shared report templates
L4  Runtime           coordination, claims, orchestration, six-field declarations —
                      context-coordination.md, orchestration.md
```

A domain contract never teaches HTML; a format file never defines ownership; a Presenter view never owns facts.

| Contract | Layer | Read when |
| --- | --- | --- |
| [Shared Context](skill-declarations.md) | L0/L4 | Declaring inputs/outputs, classifying records, resolving identity, handing off or cleaning up |
| [Coordination](context-coordination.md) | L4 | Assembling context, serializing contributions, resuming a run or routing review |
| [Presenter](presenter.md) | L3 | Producing a human view, reconciling feedback or retaining reviewed content |
| [HTML records](html-records.md) | L2 | Writing or retrieving canonical HTML memory documents |
| [Product](product-memory.md) | L1 | Reading or changing product records, requirements or product decisions |
| [Design](design-memory.md) | L1 | Changing design authority, contracts, prototypes or design decisions |
| [Engineering](engineering-memory.md) | L1 | Planning, implementing, testing or retaining verification evidence |
| [Operations](operations-memory.md) | L1 | Recording runtime constraints, release evidence or operational decisions |
| [Orchestration](orchestration.md) | L4 | Dispatching and reconciling implementation work |

## Source references and distribution

Use real relative Markdown links to these canonical files, including section anchors when useful. `registry.json` assigns stable protocol identities and versions for validation; its `protocol:acs:*` IDs are metadata, not runtime-resolved links. No remote resolver or cache is required.

Legacy protocol files under context skills and workflows are compatibility symlinks. Edit the canonical target and use its actual relative path for new callers. When tooling reads an alias, resolve its target before interpreting links inside it.

The plugin builder embeds each plugin's transitive local dependency closure under `resources/<system-relative-path>`, dereferences source symlinks and rewrites local links to packaged destinations. Each plugin carries the contracts and referenced assets it needs; no separately installed protocol peer is required. Generated copies are distribution artifacts, never independently edited sources. A domain skill can complete with text output without a separate Presenter skill.

## Changing a contract

Change the owning file, its date and relevant registry version together. Preserve the six context fields and compatible record identities. A new shared contract needs a registry entry with a canonical file, title, version and status. Keep single-skill implementation details with that skill.

Verify actual local paths and anchors, declaration syntax, packaged dependency closure and relevant behavior scenarios. A valid registry alone does not prove working handoffs. Canonical reviewed content and persistent evidence must remain readable after Working cleanup; a derived view must be rebuildable without changing its sources.
