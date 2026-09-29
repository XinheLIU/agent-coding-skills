# Quality · Review

Last updated: 2026-09-29

Reviewing and improving code at the change level. It covers the judgment pass (review) and the corrective action (refactor). Design-level review lives in the technical design cards (`design/technical/`): architecture, modules, contracts, test strategy, and requirement traceability each review their own aspect and write one shared record.

| Skill | Owns |
| --- | --- |
| `acs-review-code-quality` | Review a change for production readiness on two axes, Standards (repo conventions, quality bar) and Spec (does it do what was asked), and give a merge verdict. Drills into open `FND-ARC` findings and reuses `TRC` statuses |
| `acs-refactor-code` | Improve code without changing behavior: quick polish (no gate) or structural refactor (metrics plus approval gate). Preserves `CON` invariants |

Review flows down: `acs-technical-design` cards → `acs-trace-requirements` post-build → `acs-review-code-quality`. `acs-refactor-code` acts on the findings.
