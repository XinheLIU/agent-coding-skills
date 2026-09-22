# acs-plan

Planning phase plugin for [agent-coding-skills](https://github.com/XinheLIU/agent-coding-skills). Bundles the 10 skills that cover product discovery, demand validation, solution shaping, and PRD generation — the full upstream half of the ACS pipeline.

Install this plugin when you need discovery and PRD work without the design or build phases.

## Workflow chain

The primary path through the planning phase:

```
acs-brainstorm → acs-validate-demand → acs-shape-solution → acs-write-prd
```

Supporting skills slot in around that spine as needed:

- Use **acs-ideate-product** when it is not yet clear which planning question is still open.
- Use **acs-map-current-product** before shaping a solution when the starting point is an existing codebase.
- Use **acs-explore-unknowns** to decompose a complex effort into ordered decision tickets.
- Use **acs-design-experiment** to resolve a specific falsifiable uncertainty before committing.
- Use **acs-define-outcomes** after a solution is chosen to produce verifiable acceptance criteria.
- Use **acs-run-premortem** to stress-test a plan before moving to design.

## Skill inventory

| Skill | One-line description |
|---|---|
| acs-brainstorm | Turn an ambiguous idea into a Jobs-to-be-Done brief through Socratic dialogue |
| acs-validate-demand | Grade the evidence behind a product claim and issue a go/no-go verdict |
| acs-shape-solution | Turn validated demand into a concrete solution with journeys, capabilities, and product form |
| acs-write-prd | Consolidate shared product knowledge into a durable HTML PRD document |
| acs-ideate-product | Route a product effort to the right next planning step |
| acs-map-current-product | Map what an existing codebase already does as a product baseline |
| acs-explore-unknowns | Map a multi-session effort into dependency-ordered decision tickets |
| acs-design-experiment | Design a bounded experiment to resolve a named, falsifiable uncertainty cheaply |
| acs-define-outcomes | Turn a chosen solution into verifiable product commitments and acceptance criteria |
| acs-run-premortem | Stress-test a plan by assuming it has already failed |

## Installation

Copy the `skills/` directory into your agent's skill path:

```bash
cp -rP plugins/acs-plan/skills/. ~/.claude/skills/
```

Or reference individual skills directly from this plugin directory by pointing your agent config at `plugins/acs-plan/skills/<skill-name>/SKILL.md`.

## Bundled workflows

`shared/workflows/plan.md` — step-by-step planning phase workflow  
`shared/workflows/ideas.md` — idea triage and routing reference

## Dependencies

Requires `acs-context ^0.4.0` for shared product memory. Install that plugin first so `acs-init-context` is available before running any planning skill.
