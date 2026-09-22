# acs-build

Build phase plugin for the Agent Coding Skills (ACS) system. Covers delivery planning, criterion-based TDD execution, and end-to-end feature implementation.

## Install

```bash
claude plugin install acs-build
```

Requires `acs-context` (peer: `acs-design` for implementation guidance).

## Build Workflow

```
acs-plan-delivery → acs-implement → acs-tdd
```

1. **acs-plan-delivery** — takes accepted product scope and produces a set of dependency-ordered tickets plus an HTML delivery plan with an embedded DAG.
2. **acs-implement** — accepts the ticket graph, executes ready implementation tickets in dependency order, and verifies the running system end-to-end.
3. **acs-tdd** — executes one ticket through criterion-based red-green-refactor loops; invoked per ticket by `acs-implement`, or standalone for focused TDD work.

## Skill Inventory

| Skill | Description |
|-------|-------------|
| `acs-plan-delivery` | Turn accepted scope or designs into delivery tickets and an openable HTML plan with an embedded DAG |
| `acs-implement` | Deliver a verifiable change end-to-end using dependency-ordered tickets, criterion-based execution, and running-system verification |
| `acs-tdd` | Execute one ticket through criterion-based red-green-refactor loops; returns criterion → test/evidence → revision mapping |

## Agents Bundled

| Agent | Role |
|-------|------|
| `shared/agents/tdd-builder.md` | Drives the TDD loop — prepares behavior slices, writes failing tests, implements, refactors, and returns evidence per criterion |

## Scripts Bundled

| Script | Purpose |
|--------|---------|
| `shared/scripts/commit.md` | Structured commit workflow |
| `shared/scripts/pr-create.md` | Pull request creation workflow |
| `shared/scripts/setup.md` | Repository/environment setup |
| `shared/scripts/git/` | Git operation helpers |

## Shared Workflows

- `shared/workflows/build.md` — overall build phase orchestration
- `shared/workflows/feature-delivery.md` — end-to-end feature delivery flow

## Usage Examples

```
# Break accepted scope into delivery tickets
/acs-plan-delivery --scope "add OAuth login"

# Execute the full delivery graph
/acs-implement

# Run TDD on a single ticket
/acs-tdd --ticket T001
```

For orchestration across phases, see the `acs-context` and `acs-design` plugins.
