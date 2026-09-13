# Orchestration protocol

Last updated: 2026-09-13

How `implement` dispatches ticket execution to parallel sub-agents. The skill logic speaks only the four abstract operations; each orchestrator supplies a binding. Swapping orchestrators means writing a new binding section — the loop never changes.

## The four operations

| Operation | Contract |
| --- | --- |
| `dispatch(ticket) → agent_ref` | Start an isolated sub-agent executing the `tdd` skill against one ticket. The prompt carries the ticket file path, criterion references, prerequisite evidence paths, and the evidence file it must write. |
| `await(agent_refs) → completions` | Block until at least one dispatched agent reaches a terminal state (done, blocked, failed). |
| `collect(agent_ref) → evidence` | Read the agent's evidence file and terminal output; validate the criterion → test/evidence → revision mapping is present. |
| `reclaim(agent_ref)` | Release the agent's resources — merge or discard its worktree, close its pane. |

## Evidence contract

Every dispatched agent writes `docs/changes/<change-id>/run/evidence/<ticket-id>.md` in its own workspace before finishing: criteria addressed, tests with exact commands and results, revision/diff identity, deviations, environment assumptions. Terminal output supplements the file; it never replaces it. `collect` fails a ticket whose evidence file is missing or claims green without commands.

## Primary binding: herdr

herdr is a terminal agent multiplexer with an agent-native CLI (`~/.local/bin/herdr`). Its sidebar gives the user live per-agent state; any pane can be attached mid-run.

```bash
# dispatch
herdr worktree create <change-id>-<ticket-id>          # isolated git worktree
herdr pane split --cwd <worktree-path>                  # pane in that worktree
herdr agent start claude                                # Claude Code in the pane
herdr agent prompt <agent> "Load the tdd skill. Execute ticket <path>. \
  Criteria: <refs>. Prerequisite evidence: <paths>. \
  Write evidence to docs/changes/<change-id>/run/evidence/<ticket-id>.md, then stop."

# await
herdr agent wait <agent> --state done,blocked,idle

# collect
herdr agent read <agent>                                # terminal output
# evidence file read from the worktree path

# reclaim
git -C <main-checkout> merge <ticket-branch>            # dependency order only
herdr worktree remove <worktree-path>
herdr pane close <pane>
```

Consult `herdr <subcommand> --help` for exact flags — the CLI is the source of truth; the lines above name the primitives, not frozen invocations.

## Fallback binding: in-process Agent tool

When herdr is absent or no session is active: dispatch through the harness's Agent tool (sub-agent per ticket, shared working tree). Without worktree isolation, any two tickets with shared-write risk run serially — parallel dispatch only for tickets that touch disjoint files *and* pass the semantic safety rules.

## State lifecycle

`docs/changes/<change-id>/run/state.json` ([schema](state-schema.json)) is the orchestrator's single working record: every ticket's status, agent ref, timestamps, and evidence pointer, plus the computed frontier. Update it on every transition, then re-render the DAG so the user's view stays current.

Ticket statuses: `ready` → `in_progress` → `done` | `failed`; `blocked` until dependencies are done. Canonical ticket status lives in the ticket files/tracker; `state.json` is Run Context — remove it after reconciliation, retain the tickets and evidence.

## Failure policy

A failed or blocked-and-stuck agent fails its ticket: record the evidence trail, keep its dependents blocked, continue every independent ticket. Never discard another ticket's work to restart a loop. The final envelope lists failed tickets with blocking effects; the user retries specific tickets, which re-enter the loop as `ready`.

## Handoff envelope

The run's return value is the [shared handoff envelope](../../../craft/context/init-context/references/PROTOCOL.md#handoff-envelope) — the retired standalone `handoff` skill's format, now produced by every `implement` run: canonical change identity, criterion → ticket → evidence → revision mapping, end-to-end verification result, unresolved questions with blocking effects, and one executable next action.
