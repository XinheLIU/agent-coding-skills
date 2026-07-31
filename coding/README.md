# Feature Delivery

<div align="center">
  <a href="../README.md">Home</a> &bull;
  <a href="../product-planning/README.md">Product Planning</a> &bull;
  <a href="../architecture-design/README.md">Architecture Design</a> &bull;
  <strong>Feature Delivery</strong> &bull;
  <a href="../visualization/README.md">Visualization</a> &bull;
  <a href="../knowledge-management/README.md">Knowledge</a> &bull;
  <a href="../team-collaboration/README.md">Collaboration</a> &bull;
  <a href="../user-setup/README.md">User Setup</a> &bull;
  <a href="../learning-resources/README.md">Learning</a>
</div>
<br>

**Lifecycle stage 4.** Implementation and coding. This domain turns design into production code with a spec-first, test-first workflow designed for reliable agent execution. Testing & deployment (stage 5) — auto test generation, containerization/K8s, observability — is on the roadmap; see [`backlog.md`](../backlog.md).

## Capability Areas

| Area | Focus | Key Skills/Tools |
| :--- | :--- | :--- |
| **[Frontend](frontend/)** | Aesthetic intent & systems | `frontend-design`, `UI/UX Pro Max` |
| **[Backend](backend/code-quality-improvements/)** | Agentic code quality | Explorers, Reviewers, `simplify-code` |
| **[Working on a Feature](working-on-a-feature/)** | End-to-end feature delivery with TDD | `brainstorm`, `spec`, `plan`, `tasks`, `analyze`, `tdd`, `tdd-builder` |
| **[Git Workflow](git/)** | Agentic git commands | `/commit`, `/pr-create`, `/git:status` |

## TDD Workflow (Recommended)

Use this when shipping a new feature. The sequence is designed to prevent requirement drift, weak test plans, and late-stage rewrite churn.

```text
Feature idea
    |
    | (if vague)
    v
[brainstorm] -----------+
    |                    |
    | (if already clear) |
    +--------------------+
    |
    v
[spec] -> writes spec.md (FR/SC/user stories)
    |
    v
[plan] -> writes plan.md (architecture + test framework)
    |
    v
[tasks] -> writes tasks.md with tests required
    |
    v
[analyze] -> cross-artifact consistency audit
    |
    +--> CRITICAL findings? ---- yes ----> fix upstream artifacts, rerun analyze
    |                                  ^
    |                                  |
    +---------------- no ---------------+
    |
    v
[tdd-builder / tdd] -> optional execution loop
```

### Red-Green-Refactor Loop

```text
For each user story task:

Write test --> Run tests --> Fails for expected reason?
                              | no
                              v
                         fix test/setup
                              |
                              +----> re-run
                              |
                              v
                             yes
                              |
                              v
                    Write minimal implementation
                              |
                              v
                           Run tests
                              |
                    pass? ----+---- no --> fix code, re-run
                      |
                     yes
                      |
                      v
              Optional refactor (all tests green)
                      |
                      v
                Re-run full suite
```

## Workflow Rules

- **Tests first**: implementation tasks run only after corresponding tests are written and observed failing.
- **Story-first delivery**: complete one user story to green before starting the next.
- **Analyze gate**: run `analyze` before execution; treat CRITICAL findings as blocking.
- **Small diffs**: make minimal changes to turn targeted tests green, then refactor safely.
- **No fake green**: never skip tests or weaken assertions to pass.

## Workflow Context

Follows [Architecture Design](../architecture-design/). This domain executes architecture through disciplined planning and TDD, then feeds into review and release workflows.

## Add Your Own

Create `feature-delivery/<skill-name>/SKILL.md`. High-value additions include deployment automation, CI gating, release playbooks, and test infrastructure skills. See [CONTRIBUTING.md](../CONTRIBUTING.md).
