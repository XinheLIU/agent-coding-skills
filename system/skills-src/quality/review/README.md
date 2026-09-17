# Quality · Review

Last updated: 2026-09-17

Reviewing and improving artefacts at every level — architecture decisions, design docs, implementation gaps, and code quality. Covers both the judgment pass (review) and the corrective action (refactor).

| Skill | Owns |
| --- | --- |
| `acs-review-architecture` | Review system or module architecture against design goals and constraints |
| `acs-review-design-doc` | Review a design document for completeness, clarity, and internal consistency |
| `acs-review-implementation-gaps` | Identify gaps between what the design specifies and what the implementation delivers |
| `acs-review-code-quality` | Review a change for production readiness on two axes — Standards (repo conventions, quality bar) and Spec (does it do what was asked) — with a merge verdict |
| `acs-refactor-code` | Improve code without changing behavior — quick polish (no gate) or structural refactor (metrics + approval gate) |

Review flows down: architecture → design doc → implementation gaps → code quality. `acs-refactor-code` acts on the findings.
