# Optional herdr Delivery Binding

Last updated: 2026-09-17

This preserves the earlier herdr/Claude delivery example as a host-specific binding of the [four orchestration operations](../../skills-src/build/acs-implement/references/orchestration-protocol.md). It is not the default host, an installed runtime integration, or verified CLI syntax.

Use only when the session has herdr, the selected worker executable, authorized delegation, and suitable isolated workspaces. Consult the installed `herdr <subcommand> --help` before mapping operations; discover the executable rather than assuming a user-home path. The example selects Claude Code; another supported worker is an adapter choice.

```bash
# dispatch: illustrative primitives; verify flags against the installed CLI
herdr worktree create <change-id>-<ticket-id>
herdr pane split --cwd <worktree-path>
herdr agent start claude
herdr agent prompt <agent> "Load acs-tdd. Execute ticket <path>. \
  Criteria: <refs>. Prerequisite evidence: <paths>. \
  Write evidence to docs/changes/<change-id>/run/evidence/<ticket-id>.md, then stop."

# await
herdr agent wait <agent> --state done,blocked,idle

# collect: also read the required evidence file in the worker workspace
herdr agent read <agent>
```

For `reclaim`, collect and reconcile evidence first, preserve unmerged work, and merge only within existing Git authorization. A worker being finished or idle does not authorize discarding its workspace or creating a commit. Close panes and remove only verified disposable resources after reconciliation.

If this binding is unavailable, use another verified host binding or execute serially as the active agent. Parallel work in a shared tree still requires the coordinator's semantic conflict checks and exclusive claims; disjoint filenames alone are insufficient.
