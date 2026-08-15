---
description: Show git status with helpful context
allowed-tools: Bash(git:*)
model: haiku
---

Run `git status` and report what's going on.

Last updated: 2026-08-02

## Steps

1. Run `git status`
2. Run `git diff --stat` if there are unstaged changes
3. Report clearly

## Output

```
Branch: [name]

Staged:
- [files]

Unstaged:
- [files]

Untracked:
- [files]

Next: [one concrete suggestion — commit, stage, or clean]
```

If clean: `✓ Clean on [branch]`

Be terse. No padding.
