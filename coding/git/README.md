# Slash Commands

Custom commands for this project. Invoke with `/command-name [args]` in Claude Code.

---

## `/git:status`

**When:** Before committing, after a merge, or when you've lost track of what's staged.

```
/git:status
```

**Next steps it might suggest:**
- Stage specific files before committing
- Stash changes before switching context
- Notice untracked files that shouldn't be there

---

## `/git:log`

**When:** Catching up after time away, before writing a commit message, before creating a PR.

```
/git:log        # last 10 commits
/git:log 20     # last 20 commits
```

**Next steps it might suggest:**
- Spot where a bug was introduced
- Understand the current work theme before adding to it
- Decide whether to squash before PR

---

## `/commit`

**When:** You're done with a logical unit of work and want a clean commit without writing the message manually.

```
/commit                          # auto-generates message from diff
/commit feat: add weekly KPI view
```

Runs on `haiku` (fast). Stages everything unstaged if nothing is staged. Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.).

**Next steps after committing:**
- `/git:log` to verify the commit landed correctly
- `/pr-create` if the feature is ready for review
- Keep working and commit again

---

## `/pr-create`

**When:** Feature branch is ready — not for direct `main` commits.

```
/pr-create
/pr-create "Add weekly opportunity priority view"
/pr-create "Fix cashflow linkage" "Resolves null FK on opportunity_id when entry has no opportunity"
```

Auto-detects branch name, recent commits, and changed files. Generates a PR body if none is provided.

**Next steps after PR creation:**
- Share URL with reviewer
- `/git:status` to confirm working tree is clean
- Start next feature on a new branch

---

## Possible Future Commands

| Command | Purpose |
|---|---|
| `/db:migrate` | Run pending migrations and verify schema |
| `/db:check` | Validate `01_schema.sql` and `02_seed_data.sql` are in sync |
| `/agent:run` | Trigger orchestrator smoke test (`runner.py alerts`) |
| `/env:check` | Verify required env vars are set before starting services |
| `/review` | Review current branch diff against `main` |
