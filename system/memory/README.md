# Shared Context

Last updated: 2026-09-09

The [canonical protocol](../skills-src/craft/context/init-context/references/PROTOCOL.md) defines North Star, Current State, Change Context, and Run Context. Code indexes and generated roadmaps are derived views. Classify records by lifecycle even when they share one HTML or Markdown document.

Setup records repository paths in `docs/agents/memory.md`. The [coordinator](../workflows/context-coordination.md) resolves identity and relevant context once, applies serialized contributions, tracks freshness, and performs cleanup. Skills own domain reasoning and evidence interpretation.

- [Product](../skills-src/craft/context/init-context/references/product-memory.md): addressable HTML records, one canonical change spec, evidence versus commitment.
- [Design](../skills-src/craft/context/init-context/references/design-memory.md): token authority, accepted prototype intent, consequential decisions retained at acceptance.
- [Engineering and verification](../skills-src/craft/context/init-context/references/engineering-memory.md): child tickets, criterion evidence, refactoring preservation and architecture updates.
- [Operations](../skills-src/craft/context/init-context/references/operations-memory.md): environment constraints and release evidence.
- [Run shape](../skills-src/craft/context/init-context/references/working-memory.md) and [document layout](../skills-src/craft/context/init-context/references/canonical-doc-layout.md): paths, routing, and retention checks.

A completed change retains its ticket/spec, accepted decisions, compact verification, and release references. Only reconciled execution scratch is disposable. Preserve established trackers; new local changes use tracked `docs/changes/<change-id>/`.

[Verification evidence and commands](evals/verification.md) cover structural checks, cleanup fixtures, existing DAG/Product checks, and an independent cross-domain handoff scenario.
