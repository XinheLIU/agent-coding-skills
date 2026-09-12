# Plan Workflow

Last updated: 2026-09-13
Turn an uncertain idea, opportunity, or maintenance alert into accepted product intent recorded in `docs/product/<product>/product.html`.

```
entry_artifact: User problem description, opportunity, or maintenance alert
exit_artifact:  docs/product/<product>/product.html (accepted intent records)
approval_gate:  User must accept demand verdict and scope before handoff to /design
```

## Overview

```
uncertain idea → brainstorm → validate-demand → shape-solution → write-prd → accepted intent
                                                ↓
                                        run-premortem (risk assessment)
                                        map-current-product (if existing product)
                                        ideate-product (if solution alternatives needed)
                                        define-outcomes / design-experiment (scope definition)
```

## Entry Criteria

- User has a problem description, opportunity, or feature idea (however vague).
- `docs/agents/memory.md` exists (if not, run `/init-context` first).

## Routing Decision

Check these in order:

1. **No memory exists** → run `/init-context` first, then return here.
2. **Problem is vague or unclear** → start with `/brainstorm`, then `/validate-demand`.
3. **Problem is clear but involves an existing product** → start with `/map-current-product`.
4. **Problem is clear and risky** → start with `/run-premortem` alongside discovery.
5. **Problem is clear, demand is validated** → go directly to `/shape-solution`.
6. **Scope is settled, need outcomes defined** → `/define-outcomes` or `/design-experiment`.
7. **Intent is ready to commit** → `/write-prd`.

## Skill Sequence

### Discovery (problem space)
- `/brainstorm` — turn vague idea into a JTBD brief through Socratic dialogue
- `/validate-demand` — assess whether the demand is real and worth solving
- `/map-current-product` — extract user stories and current state from an existing codebase
- `/run-premortem` — identify failure modes before committing

### Definition (solution space)
- `/ideate-product` — generate solution alternatives when multiple paths exist
- `/shape-solution` — define the target experience, connected journeys, and required capabilities
- `/define-outcomes` — establish measurable success criteria (replaces vague goals with verifiable outcomes)
- `/design-experiment` — scope a time-boxed experiment when demand remains uncertain
- `/write-prd` — consolidate accepted intent into the canonical product record

## Exit Criteria

- `docs/product/<product>/product.html` contains at least one accepted intent record.
- The record has: validated problem, scope boundary, success criteria, and open questions resolved or explicitly noted.
- User has reviewed and accepted the demand verdict.

## Handoff

Passes `product.html` (accepted intent) to `/design`. The design workflow reads the intent records and begins with requirements.

Shared context coordination: [context-coordination.md](context-coordination.md)
