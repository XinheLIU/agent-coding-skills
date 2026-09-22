#!/bin/bash
# Phase Plugin Refactoring - Parallel Dispatch via herdr
# Orchestrator: Main pane
# Workers: 7 herdr agents (one per plugin)

set -euo pipefail

BASE_DIR="/Users/xhl/GitHub/learning-infra/agent-skill-projects/agent-coding-skills"
MIGRATION_DIR="$BASE_DIR/docs/migration"
PLUGINS_DIR="$BASE_DIR/plugins"

echo "=== Phase Plugin Refactoring Orchestrator ==="
echo "Starting parallel plugin creation via herdr..."

mkdir -p "$PLUGINS_DIR"

# Task 1: acs-context (P0 - foundation)
echo "[Task 1] Dispatching acs-context plugin creation..."
herdr agent spawn \
  --name "context-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-01-acs-context.md Execute this task. Work in $PLUGINS_DIR/acs-context. Extract skills from system/skills-src/context/, bundle protocols, create package.json and catalog. Report when complete with verification results." \
  --background

# Task 2: acs-plan (independent of others except context)
echo "[Task 2] Dispatching acs-plan plugin creation..."
herdr agent spawn \
  --name "plan-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-02-acs-plan.md Execute this task. Work in $PLUGINS_DIR/acs-plan. Extract 10 plan skills, bundle workflows. Depends on acs-context. Report when complete." \
  --background

# Task 3: acs-build (critical path)
echo "[Task 3] Dispatching acs-build plugin creation..."
herdr agent spawn \
  --name "build-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-03-acs-build.md Execute this task. Work in $PLUGINS_DIR/acs-build. Extract 7 build skills, bundle specialist agents and DAG scripts. Report when complete." \
  --background

# Task 4: acs-design
echo "[Task 4] Dispatching acs-design plugin creation..."
herdr agent spawn \
  --name "design-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-04-acs-design.md Execute this task. Work in $PLUGINS_DIR/acs-design. Extract 12 design skills, bundle architecture specialists. Report when complete." \
  --background

# Task 5: acs-test (largest by agent count)
echo "[Task 5] Dispatching acs-test plugin creation..."
herdr agent spawn \
  --name "test-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-05-acs-test.md Execute this task. Work in $PLUGINS_DIR/acs-test. Extract 9 test skills, bundle 20+ review specialists. Report when complete." \
  --background

# Task 6: acs-maintain
echo "[Task 6] Dispatching acs-maintain plugin creation..."
herdr agent spawn \
  --name "maintain-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-06-acs-maintain.md Execute this task. Work in $PLUGINS_DIR/acs-maintain. Extract maintain skills. Report when complete." \
  --background

# Task 7: acs-authoring (meta-tooling)
echo "[Task 7] Dispatching acs-authoring plugin creation..."
herdr agent spawn \
  --name "authoring-agent" \
  --model "claude-opus-5" \
  --prompt "@$MIGRATION_DIR/task-07-acs-authoring.md Execute this task. Work in $PLUGINS_DIR/acs-authoring. Extract 5 authoring skills. Report when complete." \
  --background

echo ""
echo "All 7 agents dispatched. Monitor with:"
echo "  herdr agent list"
echo ""
echo "Orchestrator will now monitor completion..."
