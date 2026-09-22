# Installation Guide

Last updated: 2026-09-20

How to install ACS plugins in Claude Code, Codex, OpenCode, Cursor, and Pi.

The system ships as eight installable plugins plus one monolithic target:

```
Monolith:    agent-coding-skills   (all skills, one install)

Plugins:     acs-plan              product discovery and intent
             acs-design            UX and technical design
             acs-build             delivery, implementation, TDD
             acs-test              review, debugging, verification
             acs-context           agent context lifecycle
             acs-authoring         research, skill writing, decision tools
             acs-deploy            release and governance  (roadmap)
             acs-maintain          incident diagnosis
```

After installation, run a one-time repository setup to write `docs/agents/memory.md`, which is the shared memory file every skill reads and writes:

```
/acs-init-context
```


## Install from GitHub (any agent)

If your agent supports loading skills from a local directory, clone the repo once and point the agent at it. No npm registry or marketplace needed.

```bash
git clone https://github.com/XinheLIU/agent-coding-skills.git ~/skills/agent-coding-skills
```

Then install individual plugins:

```bash
npx skills install ~/skills/agent-coding-skills/plugins/acs-plan -g
npx skills install ~/skills/agent-coding-skills/plugins/acs-build -g
# etc.
```

Or install the full monolith:

```bash
npx skills install ~/skills/agent-coding-skills/system -g
```

To stay current, pull and reinstall:

```bash
cd ~/skills/agent-coding-skills && git pull
npx skills install ~/skills/agent-coding-skills/plugins/acs-build -g --force
```

To pin a specific release:

```bash
git clone --branch v0.3.0 https://github.com/XinheLIU/agent-coding-skills.git ~/skills/agent-coding-skills
```

---

## Test locally before installing

Verify a plugin is well-formed before installing it globally.

**Check structure:**

```bash
# Each skill must have a SKILL.md
find plugins/acs-build/skills -name "SKILL.md" | sort

# Each plugin must have a plugin.json
cat plugins/acs-build/.claude-plugin/plugin.json
```

**Dry-run install:**

```bash
npx skills install ./plugins/acs-build --dry-run
```

**Smoke-test a single skill** by loading it into a scratch project:

```bash
mkdir /tmp/acs-test && cd /tmp/acs-test
git init && echo "# test" > README.md

# Install the plugin locally (project scope only)
npx skills install /path/to/agent-coding-skills/plugins/acs-context

# Then in the agent: /acs-init-context
# Expected: creates docs/agents/memory.md
```

**Validate protocol references resolve:**

```bash
cd /path/to/agent-coding-skills
python3 scripts/validate-protocols.py
```

**Check no stale cross-plugin links:**

```bash
grep -r "acs-protocols\|acs-quality\|acs-craft" plugins/ --include="*.md" -l
# Expected: no output
```

---

---

## Claude Code

Claude Code reads skills from `~/.claude/skills/` (global) or `.claude/skills/` (project-local).

**Monolith — installs all skills at once:**

```bash
/plugin marketplace add XinheLIU/agent-coding-skills
/plugin install agent-coding-skills@agent-coding-skills
```

**Individual plugins:**

```bash
/plugin marketplace add XinheLIU/agent-coding-skills
/plugin install agent-coding-skills@acs-plan
/plugin install agent-coding-skills@acs-design
/plugin install agent-coding-skills@acs-build
/plugin install agent-coding-skills@acs-test
/plugin install agent-coding-skills@acs-context
/plugin install agent-coding-skills@acs-authoring
```

**From a local clone** (useful while developing skills):

```bash
npx skills install ./plugins/acs-build -g
```

Invoke skills with their public ID in the chat:

```
/acs-brainstorm
/acs-implement
/acs-review-code-quality
```

---

## Codex (OpenAI)

Codex discovers skills under `~/.codex/skills/`. Use `npx skills` or symlink from a shared directory.

**Global install from a local clone:**

```bash
npx skills install /path/to/agent-coding-skills/plugins/acs-build -g  --target codex
npx skills install /path/to/agent-coding-skills/plugins/acs-test  -g  --target codex
# repeat for each plugin
```

**Shared directory (keep Claude Code and Codex in sync):**

```bash
# Create a shared skills root once
mkdir -p ~/skills/coding

# Install into the shared root
npx skills install /path/to/agent-coding-skills/plugins/acs-build \
  --dir ~/skills/coding

# Symlink into Codex's discovery path
ln -sfn ~/skills/coding/acs-build ~/.codex/skills/acs-build
```

`~/.codex/skills/` is the discovery target; `~/skills/coding/` is the source of truth. Add an equivalent symlink under `~/.claude/skills/` to share across both agents.

Skills live in `AGENTS.md` for per-project overrides:

```markdown
<!-- in your project's AGENTS.md -->
Load skills: acs-implement, acs-review-code-quality
```

---

## OpenCode

OpenCode reads its global config from `~/.config/opencode/` and discovers skills placed in `~/.config/opencode/skills/`.

```bash
npx skills install /path/to/agent-coding-skills/plugins/acs-build \
  --dir ~/.config/opencode/skills

npx skills install /path/to/agent-coding-skills/plugins/acs-test \
  --dir ~/.config/opencode/skills
```

Or copy the full plugins tree:

```bash
cp -r /path/to/agent-coding-skills/plugins/* ~/.config/opencode/skills/
```

Project-level overrides go in your project's `AGENTS.md` (same format as Codex).

---

## Cursor

Cursor loads agent instructions from `.cursorrules` (project-root) or `AGENTS.md`. It does not have a native skill-install command, so the pattern is to paste the skill content into your rules file or include it from a shared path.

**Option 1 — inline in `.cursorrules`:**

Copy the relevant SKILL.md content into `.cursorrules`:

```bash
cat /path/to/agent-coding-skills/plugins/acs-build/skills/acs-implement/SKILL.md \
  >> .cursorrules
```

**Option 2 — reference via `AGENTS.md`:**

```markdown
# AGENTS.md

@include ~/.cursor/skills/acs-implement/SKILL.md
@include ~/.cursor/skills/acs-review-code-quality/SKILL.md
```

Then copy or symlink the skill directories:

```bash
mkdir -p ~/.cursor/skills
ln -sfn /path/to/agent-coding-skills/plugins/acs-build/skills/acs-implement \
  ~/.cursor/skills/acs-implement
```

**Recommended subset for Cursor** — use skills that match Cursor's edit-focused workflow:

```
acs-implement      implementation planning and delivery
acs-tdd            test-driven development
acs-review-code-quality    inline code review
acs-refactor-code  targeted refactoring
```

---

## Pi

Pi discovers skills from a `package.json` with a `pi.skills` field. The ACS source tree is not yet packaged as a Pi-native extension; the current path is to use the context subpackage directly.

**From a local clone:**

Add to your project's `package.json`:

```json
{
  "pi": {
    "skills": [
      "./path/to/agent-coding-skills/plugins/acs-build",
      "./path/to/agent-coding-skills/plugins/acs-test",
      "./path/to/agent-coding-skills/plugins/acs-context"
    ]
  }
}
```

Or point at the monolith:

```json
{
  "pi": {
    "skills": [
      "./path/to/agent-coding-skills/system"
    ]
  }
}
```

Pi extension packaging (`pi.skills` with a published npm path) is a planned milestone tracked in [`system/docs/harness-architecture.md`](system/docs/harness-architecture.md#standalone-package-contract).

---

## DeepSeek harness

DeepSeek is a model provider, not a host agent. To use ACS skills with a DeepSeek-backed session, install into whatever harness or runner is wrapping the model — the skills work the same regardless of the underlying model.

**Via OpenCode with a DeepSeek backend:**

OpenCode supports model routing. Set up OpenCode pointing at DeepSeek, then install skills as normal:

```bash
# ~/.config/opencode/config.json — set your model to deepseek
cp -r /path/to/agent-coding-skills/plugins/acs-build ~/.config/opencode/skills/
cp -r /path/to/agent-coding-skills/plugins/acs-test  ~/.config/opencode/skills/
```

**Via a custom runner (herdr or similar):**

If you use a dispatch harness that spawns an agent subprocess with a chosen model, point that runner at the skills directory and pass the skill name as a prompt prefix. Example with herdr:

```bash
# Start an agent with DeepSeek as the worker
herdr agent start deepseek-coder

# Prompt it with a skill
herdr agent prompt <agent> "Load acs-review-code-quality. Review the diff in the current branch."
```

The ACS harness contract is model-neutral: skills declare context requirements in YAML, not model-specific syntax. Any host that can load a SKILL.md and follow its instructions will work.

**Note:** ACS uses protocol references like `protocol:acs:skill-declarations` that assume a skill-aware host can resolve them. A generic chat interface that just reads raw Markdown will see those as unresolved links. Use a harness that understands the plugin format, not a bare chat window.

---

## Shared skills directory (multi-agent setup)

If you use more than one agent, keep one install and symlink into each agent's discovery path:

```bash
# Source of truth
mkdir -p ~/skills/acs
npx skills install /path/to/agent-coding-skills/plugins/acs-build --dir ~/skills/acs
npx skills install /path/to/agent-coding-skills/plugins/acs-test  --dir ~/skills/acs
# ... repeat for each plugin

# Agent discovery paths
ln -sfn ~/skills/acs/acs-build ~/.claude/skills/acs-build
ln -sfn ~/skills/acs/acs-build ~/.codex/skills/acs-build
ln -sfn ~/skills/acs/acs-build ~/.config/opencode/skills/acs-build
# ... one symlink per plugin per agent
```

`~/.skills-manager/skills/` serves the same role if you already use skills-manager as your source of truth; in that case symlink from there rather than creating a separate `~/skills/acs/` directory.

---

## Verifying the install

After installing, run a quick check from the agent prompt:

```
/acs-research What is the current project?
```

If the skill loads, it will ask for a bounded engineering question. If you see "skill not found", confirm the skills directory is on the agent's discovery path.

---

## Updating

Pull the latest from the repo and reinstall:

```bash
cd /path/to/agent-coding-skills
git pull
npx skills install ./plugins/acs-build -g --force
# repeat for each installed plugin
```

