---
description: Show recent git history with summary
argument-hint: "[n commits, default 10]"
allowed-tools: Bash(git:*)
model: haiku
---

Show recent commits. Count: $ARGUMENTS (default 10).

Last updated: 2026-08-02

## Steps

1. `git log --oneline -n [count]`
2. Group by theme if a pattern is obvious (e.g. "3 API changes, 2 frontend fixes")
3. Flag anything unusual: merge commits, fixups, large jumps in scope

## Output

```
[hash] [message]  ([time])
...

Pattern: [one line — what the recent work has been about]
```

No tables. No headers per commit. Just the log + one insight line.
