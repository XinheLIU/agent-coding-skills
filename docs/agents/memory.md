# Agent Memory Configuration

Last updated: 2026-09-26

Routing index for shared context in this repository, per [the shared protocol](../../system/protocols/skill-declarations.md). Pointers only — no normative facts live here.

## Memory homes

| Setting | Value |
| --- | --- |
| Work root | `.scratch/` (gitignored) |
| Recovery entry | `.scratch/<run-id>/state.md`, exactly one per run |
| Issue tracker | GitHub, `XinheLIU/agent-coding-skills` |
| Change records | `docs/changes/<change-id>/`, created lazily |
| Decision records | `docs/adr/NNNN-<slug>.md` |
| Changelog | [`CHANGELOG.md`](../../CHANGELOG.md), the promotion target for retained summaries |
| Retention window | 14 days, measured by the last commit touching the file |
| Domain memory | none; the product's own contracts under `system/protocols/` serve this role |
| Product memory | not configured — this repository's product intent lives in [`README.md`](../../README.md) |
| Code index | disabled |

## Not context

Exclusion rules for a document census. Each names its reason code; see [the layout guide](../../system/skills-src/context/acs-init-context/references/canonical-doc-layout.md).

| Rule | Reason | Note |
| --- | --- | --- |
| `plugins/**` | `generated` | Build output of `scripts/build-plugins.py`; byte-deterministic, never hand-edited |
| `system/**` | `product-source` | The artifact this repository builds; governed by its own domain skills, not by retention |
| `references/**` | `external` | Vendored upstream corpus, gitignored and read-only per [`AGENTS.md`](../../AGENTS.md) |
| `README.md`, `installation.md`, `THIRD_PARTY_NOTICES.md`, `MIGRATION.md` | `interface` | Repository front door and legal; repair only a broken routing pointer inside them |

Census boundary is `git ls-files '*.md' '*.html'`. Do not walk the filesystem: `references/` alone adds roughly 1,900 files that no disposition applies to.

## Startup sequence

1. Read [`AGENTS.md`](../../AGENTS.md) for repository boundaries.
2. Resolve the active effort from the current branch or an explicit user reference.
3. Read `.scratch/<run-id>/state.md` when an active run exists, and follow its pointers.
4. For contract questions, start at [the protocols index](../../system/protocols/README.md).

## Verification

```bash
python3 scripts/validate-protocols.py     # registry parity, links, package closure
python3 system/evals/validate_suite.py    # skill inventory, declarations, anchors
python3 scripts/build-plugins.py          # regenerate plugins/ after any system/ edit
```
