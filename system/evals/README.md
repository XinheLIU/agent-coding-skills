# Shared Context

Last updated: 2026-09-25

The [canonical protocol](../protocols/skill-declarations.md) defines Working Memory for run recovery and Persistent Memory for Intent, Current, and Changes. The [Presenter](../protocols/presenter.md) derives human review views without owning domain facts; review decisions and exact reviewed artifacts remain persistent. Classify records by ownership and retention, never by file format.

Setup records repository paths in `docs/agents/memory.md`. The [coordinator](../workflows/context-coordination.md) resolves identity and relevant context once, applies serialized contributions, tracks freshness, and performs cleanup. Skills own domain reasoning and evidence interpretation.

- [Product](../skills-src/context/acs-init-context/references/product-memory.md): addressable HTML records, one canonical change spec, evidence versus commitment.
- [Design](../skills-src/context/acs-init-context/references/design-memory.md): token authority, accepted prototype intent, consequential decisions retained at acceptance.
- [Engineering and verification](../skills-src/context/acs-init-context/references/engineering-memory.md): child tickets, criterion evidence, refactoring preservation and architecture updates.
- [Operations](../skills-src/context/acs-init-context/references/operations-memory.md): environment constraints and release evidence.
- [Run shape](../skills-src/context/acs-init-context/references/working-memory.md) and [document layout](../skills-src/context/acs-init-context/references/canonical-doc-layout.md): paths, routing, and retention checks.

A completed change retains its ticket/spec, accepted decisions, compact verification, and release references. Only reconciled execution scratch is disposable. Preserve established trackers; new local changes use tracked `docs/changes/<change-id>/`.

[Current implementation verification](evals/context-memory-presenter-verification.md) records Working/Persistent/Presenter checks and the independent review/cleanup exercise. The earlier [verification record](evals/verification.md) is a historical snapshot.

## Repeatable verification

```sh
python3 system/evals/validate_suite.py
python3 -m unittest discover -s system/evals/tests -p 'test_*.py' -v
python3 -m unittest discover -s system/evals/evals -p 'test_*.py' -v
python3 scripts/build-plugins.py --output /tmp/acs-packages-check
python3 scripts/validate-protocols.py --plugins /tmp/acs-packages-check
```

Package fixtures remove the source tree, relocate one package, verify every copied Markdown link and symlink, run the packaged DAG renderer tests, and compare repeat builds. These exercise artifact behavior, not host dispatch or agent judgment. Review revision binding, feedback deduplication, and cold-start choices are isolated-agent scenarios in [context-lifecycle.json](evals/context-lifecycle.json); structural success alone does not establish those outcomes.
