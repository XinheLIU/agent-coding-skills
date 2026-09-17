# Plan Workflow

Last updated: 2026-09-17
Turn an uncertain idea, opportunity, or maintenance alert into accepted product intent recorded in `docs/product/<product>/product.html`.

```
entry_artifact: User problem description, opportunity, or maintenance alert
exit_artifact:  docs/product/<product>/product.html + delivery-plan.html for an accepted change
approval_gate:  User accepts demand verdict and scope; reuse that confirmation for delivery planning
```

## Overview

```
uncertain idea → acs-brainstorm → acs-validate-demand → acs-shape-solution → acs-write-prd → accepted intent
                                                ↓
                                        acs-run-premortem (risk assessment)
                                        acs-map-current-product (if existing product)
                                        acs-ideate-product (if solution alternatives needed)
                                        acs-define-outcomes / acs-design-experiment (scope definition)
```

## Entry Criteria

- User has a problem description, opportunity, or feature idea (however vague).
- `docs/agents/memory.md` exists (if not, run `/acs-init-context` first).

## Routing Decision

Check these in order:

1. **No memory exists** → run `/acs-init-context` first, then return here.
2. **Problem is vague or unclear** → start with `/acs-brainstorm`, then `/acs-validate-demand`.
3. **Problem is clear but involves an existing product** → start with `/acs-map-current-product`.
4. **Problem is clear and risky** → start with `/acs-run-premortem` alongside discovery.
5. **Problem is clear, demand is validated** → go directly to `/acs-shape-solution`.
6. **Scope is settled, need outcomes defined** → `/acs-define-outcomes` or `/acs-design-experiment`.
7. **Intent is ready to commit** → `/acs-write-prd`.

## Skill Sequence

### Discovery (problem space)
- `/acs-brainstorm` — turn vague idea into a JTBD brief through Socratic dialogue
- `/acs-validate-demand` — assess whether the demand is real and worth solving
- `/acs-map-current-product` — extract user stories and current state from an existing codebase
- `/acs-run-premortem` — identify failure modes before committing

### Definition (solution space)
- `/acs-ideate-product` — generate solution alternatives when multiple paths exist
- `/acs-shape-solution` — define the target experience, connected journeys, and required capabilities
- `/acs-define-outcomes` — establish measurable success criteria (replaces vague goals with verifiable outcomes)
- `/acs-design-experiment` — scope a time-boxed experiment when demand remains uncertain
- `/acs-write-prd` — consolidate accepted intent into the canonical product record

## Exit Criteria

- `docs/product/<product>/product.html` contains at least one accepted intent record.
- The record has: validated problem, scope boundary, success criteria, and open questions resolved or explicitly noted.
- User has reviewed and accepted the demand verdict.

## Handoff

When grilling confirms scope for a concrete change, persist its canonical Product records and invoke [acs-plan-delivery](../skills-src/build/acs-plan-delivery/SKILL.md). Supply the change ID, accepted scope/outcomes/priorities, spec/decision links and revisions, and remaining questions. It generates and opens `docs/changes/<change-id>/delivery-plan.html`: scope, outcomes, design blockers, ready tickets, next action, and an embedded DAG. Design resolves the blockers while independent slices can become ready. Scope still unsettled or a consolidation-only request ends with the Product report; accepted product intent alone does not authorize implementation.

Shared context coordination: [context-coordination.md](context-coordination.md)
