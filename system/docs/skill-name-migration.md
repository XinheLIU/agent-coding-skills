# ACS Skill Name Migration

Last updated: 2026-09-17

The plugin ID remains `agent-coding-skills`. Every suite skill now has one public `acs-` ID, shared by plugin discovery and planned standalone packages. The host supplies invocation syntax and any plugin qualification.

Update local callers and integrations using this table. Unprefixed names are not installed as aliases: they remain available to Matt Pocock, Feature Delivery, Knowledge & Learning, and other upstream skill collections. Source provenance and domain selectors are not renamed.

| Previous suite ID | Public ID |
| --- | --- |
| `analyze-test-gaps` | `acs-analyze-test-gaps` |
| `audit-architecture` | `acs-audit-architecture` |
| `brainstorm` | `acs-brainstorm` |
| `challenge-approach` | `acs-challenge-approach` |
| `define-outcomes` | `acs-define-outcomes` |
| `design-architecture` | `acs-design-architecture` |
| `design-context` | `acs-design-context` |
| `design-experiment` | `acs-design-experiment` |
| `design-foundation` | `acs-design-foundation` |
| `design-implement` | `acs-design-implement` |
| `design-interaction-flow` | `acs-design-interaction-flow` |
| `design-modules` | `acs-design-modules` |
| `design-system-create` | `acs-design-system-create` |
| `diagnose-incident` | `acs-diagnose-incident` |
| `draw-portfolio-dag` | `acs-draw-portfolio-dag` |
| `engineer-domain-model` | `acs-engineer-domain-model` |
| `explore-unknowns` | `acs-explore-unknowns` |
| `ideate-product` | `acs-ideate-product` |
| `implement` | `acs-implement` |
| `init-context` | `acs-init-context` |
| `manage-context` | `acs-manage-context` |
| `map-current-product` | `acs-map-current-product` |
| `plan-delivery` | `acs-plan-delivery` |
| `refactor-code` | `acs-refactor-code` |
| `research` | `acs-research` |
| `resolving-merge-conflicts` | `acs-resolving-merge-conflicts` |
| `review-agent-instructions` | `acs-review-agent-instructions` |
| `review-architecture` | `acs-review-architecture` |
| `review-code-quality` | `acs-review-code-quality` |
| `review-design-doc` | `acs-review-design-doc` |
| `review-implementation-gaps` | `acs-review-implementation-gaps` |
| `run-premortem` | `acs-run-premortem` |
| `settle-requirements` | `acs-settle-requirements` |
| `shape-solution` | `acs-shape-solution` |
| `sync-context` | `acs-sync-context` |
| `tdd` | `acs-tdd` |
| `translate-agent-context` | `acs-translate-agent-context` |
| `triage` | `acs-triage` |
| `validate-codebase` | `acs-validate-codebase` |
| `validate-demand` | `acs-validate-demand` |
| `validate-prototype` | `acs-validate-prototype` |
| `visual-design-variants` | `acs-visual-design-variants` |
| `write-prd` | `acs-write-prd` |
| `writing-great-skills` | `acs-writing-great-skills` |

`acs-manage-context` remains an explicit-only compatibility router for setup, synchronization, and translation; new callers should select the focused context skill. The name itself still needs migration.

## Source and distribution changes

The active TDD and test-gap sources remain in Build and Test. Their obsolete Quality copies and broken nested symlinks were removed. Source directories, frontmatter, discovery links, internal references, catalog entries, and the context subpackage now use the same namespace.

The six lifecycle names are workflow documents, not discoverable skills or installed commands. They remain available through [workflow navigation](../workflows/README.md). The catalog lists only existing skill sources.

Individual skill directories still depend on shared resources. Read the [standalone package contract](harness-architecture.md#standalone-package-contract) before treating a source directory or the context development package as independently distributable.

## Installation migration

This source migration does not uninstall, overwrite, or rename installed upstream skills. For user installation, update skills-manager source records first, then refresh agent-target symlinks. Preserve `/Users/xhl/.skills-manager/skills` as the source of truth and `/Users/xhl/.codex/skills` as a symlink target; do not recreate `.agents/skills`.

When moving an existing ACS installation, identify its ownership from source metadata rather than deleting an unprefixed name that may belong to an upstream skill. Plugin and individual installation of the same ACS skill are alternative delivery routes; avoid registering both copies in one host's discovery scope.

## Verification baseline

Run `python3 system/memory/validate_suite.py --inventory-only` for naming, source/loader/catalog agreement, plugin skill roots, and context subpackage consistency. Run the full command for context declarations and links as well.

Three unrelated full-suite findings existed before the migration and remain visible rather than being suppressed:

- `acs-settle-requirements`: invalid `handoff_to` selectors in its existing context declaration.
- `acs-settle-requirements`: missing `references/spec-template.md`.
- `memory/evals/verification.md`: historical link to the missing `skills-src/product/evals/shared-memory.json`.

The migration must introduce no additional full-suite findings. Upstream coexistence checks compare public frontmatter names, not just installation directory names (for example, `mattpocock-tdd` declares `name: tdd`).

The current Codex plugin validator also rejects `disable-model-invocation: true` on ten existing explicit-only skills (the product-lane skills and compatibility router). Running the validator on the pre-migration snapshot produces the same ten failures. Preserve invocation intent; a future Codex packaging adapter must translate this policy to its supported surface rather than enabling implicit invocation. The context subpackage passes that validator.

Migration verification uses the installed PyYAML-capable tool environment for plugin checks without adding a repository dependency. Namespace/inventory tests, the context builder's directory-symlink materialization test, existing DAG tests, and the visual report contract check pass. The actual shared frontend builder also resolves all ACS catalog entries in an isolated fixture without editing the frontend repository. All source skill context declarations are byte-identical to their pre-migration versions.
