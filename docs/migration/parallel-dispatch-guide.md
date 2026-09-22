# Parallel Execution Guide for Remaining Plugins

## Summary

**acs-context plugin (Task 01) is complete.** Foundation ready for parallel execution of remaining 6 plugins.

Since herdr requires pre-existing tmux panes and you'll manage the tmux layout yourself, here's the corrected approach for parallel execution:

## Manual Parallel Dispatch

### Setup (run in your terminal)

```bash
cd /Users/xhl/GitHub/learning-infra/agent-skill-projects/agent-coding-skills

# Create tmux session with 6 panes for parallel agents
tmux new-session -s acs-refactor -d -n "plugins"
tmux split-window -h -t acs-refactor:plugins
tmux split-window -v -t acs-refactor:plugins.0
tmux split-window -v -t acs-refactor:plugins.1
tmux select-pane -t acs-refactor:plugins.2
tmux split-window -v -t acs-refactor:plugins.2
tmux select-pane -t acs-refactor:plugins.4
tmux split-window -v -t acs-refactor:plugins.4

# Attach to see layout
tmux attach -t acs-refactor
```

This creates 6 panes for the remaining plugins (plan, design, build, test, maintain, authoring).

### Dispatch via herdr (after pane setup)

Run these commands in the orchestrator pane (this session):

```bash
# Get pane IDs
tmux list-panes -t acs-refactor:plugins -F "#{pane_id}"

# Assuming pane IDs are %0, %1, %2, %3, %4, %5
# Start agents in each pane

# Pane 0: acs-plan
herdr agent start plan-agent --kind claude --pane %0 --timeout 3600000 -- \
  "Execute docs/migration/task-02-acs-plan.md. Create plugins/acs-plan/ with 10 skills from system/skills-src/plan/. Report completion."

# Pane 1: acs-design  
herdr agent start design-agent --kind claude --pane %1 --timeout 3600000 -- \
  "Execute docs/migration/task-04-acs-design.md. Create plugins/acs-design/ with 12 skills. Report completion."

# Pane 2: acs-build
herdr agent start build-agent --kind claude --pane %2 --timeout 3600000 -- \
  "Execute docs/migration/task-03-acs-build.md. Create plugins/acs-build/ with 7 skills and specialists. Report completion."

# Pane 3: acs-test
herdr agent start test-agent --kind claude --pane %3 --timeout 3600000 -- \
  "Execute docs/migration/task-05-acs-test.md. Create plugins/acs-test/ with 9 skills and 20+ reviewers. Report completion."

# Pane 4: acs-maintain
herdr agent start maintain-agent --kind claude --pane %4 --timeout 3600000 -- \
  "Execute docs/migration/task-06-acs-maintain.md. Create plugins/acs-maintain/. Report completion."

# Pane 5: acs-authoring
herdr agent start authoring-agent --kind claude --pane %5 --timeout 3600000 -- \
  "Execute docs/migration/task-07-acs-authoring.md. Create plugins/acs-authoring/ with 5 meta skills. Report completion."
```

### Monitor Progress

```bash
# List running agents
herdr agent list

# Check specific agent status
herdr agent explain plan-agent
herdr agent explain build-agent

# Read agent transcript
herdr agent read plan-agent --source recent --lines 50
```

### Alternative: Sequential Execution (if parallel too complex)

If tmux/herdr orchestration is too complex, run sequentially in this session:

```bash
# I (orchestrator) will execute each task in sequence
# Task 02 → Task 03 → Task 04 → Task 05 → Task 06 → Task 07
# Each takes 2-5 hours; total: ~20-25 hours
```

## Status

- ✅ Task 01 (acs-context): **Complete** — 5 skills, protocols bundled, verified
- ⏳ Task 02 (acs-plan): Ready for dispatch
- ⏳ Task 03 (acs-build): Ready for dispatch  
- ⏳ Task 04 (acs-design): Ready for dispatch
- ⏳ Task 05 (acs-test): Ready for dispatch
- ⏳ Task 06 (acs-maintain): Ready for dispatch
- ⏳ Task 07 (acs-authoring): Ready for dispatch

## Your Decision Point

**Option A**: Set up tmux panes manually, then I provide exact herdr dispatch commands with your actual pane IDs

**Option B**: I continue as orchestrator executing tasks sequentially (slower but simpler)

**Option C**: You manually start 6 Claude Code sessions in separate terminals, each reading one task spec

Which approach do you prefer?
