# Shared Protocols

Last updated: 2026-09-25

`system/protocols/` is the canonical source of shared memory, ownership and handoff contracts. Skills own domain reasoning; the active coordinator resolves and reconciles records; Presenter organizes human reading. The [accepted design](../resources/docs/context-memory-presenter-proposal.md) explains the two-memory model and its trade-offs.

| Contract | Read when |
| --- | --- |
| [Shared Context](skill-declarations.md) | Declaring inputs/outputs, classifying records, resolving identity, handing off or cleaning up |
| [Coordination](context-coordination.md) | Assembling context, serializing contributions, resuming a run or routing review |
| [Presenter](presenter.md) | Producing a human view, reconciling feedback or retaining reviewed content |
| [Product](product-memory.md) | Reading or changing product records, requirements or product decisions |
| [Design](design-memory.md) | Changing design authority, contracts, prototypes or design decisions |
| [Engineering](engineering-memory.md) | Planning, implementing, testing or retaining verification evidence |
| [Operations](operations-memory.md) | Recording runtime constraints, release evidence or operational decisions |
| [Orchestration](orchestration.md) | Dispatching and reconciling implementation work |

## Source references and distribution

Use real relative Markdown links to these canonical files, including section anchors when useful. `registry.json` assigns stable protocol identities and versions for validation; its `protocol:acs:*` IDs are metadata, not runtime-resolved links. No remote resolver or cache is required.

Legacy protocol files under context skills and workflows are compatibility symlinks. Edit the canonical target and use its actual relative path for new callers. When tooling reads an alias, resolve its target before interpreting links inside it.

The plugin builder embeds each plugin's transitive local dependency closure under `resources/<system-relative-path>`, dereferences source symlinks and rewrites local links to packaged destinations. Each plugin carries the contracts and referenced assets it needs; no separately installed protocol peer is required. Generated copies are distribution artifacts, never independently edited sources. A domain skill can complete with text output without a separate Presenter skill.

## Changing a contract

Change the owning file, its date and relevant registry version together. Preserve the six context fields and compatible record identities. A new shared contract needs a registry entry with a canonical file, title, version and status. Keep single-skill implementation details with that skill.

Verify actual local paths and anchors, declaration syntax, packaged dependency closure and relevant behavior scenarios. A valid registry alone does not prove working handoffs. Canonical reviewed content and persistent evidence must remain readable after Working cleanup; a derived view must be rebuildable without changing its sources.
