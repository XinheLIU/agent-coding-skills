# Gap Consultation Format

Last updated: 2026-07-18

Loaded by extract-rules Step 3. Use this format to present gaps to the user. Wait for the user's decision before proceeding.

## Format

For each gap, present:

1. **Gap heading** — name the category and subtopic.
2. **Current state** — one line describing what the code does (or doesn't do) today.
3. **Options** — 2–3 concrete choices with one-line trade-offs.
4. **Decision prompt** — clear ask: `(A/B/C/other)`.

## Worked example

```markdown
### Gap: Commit Message Format

Current state: free-form, no consistent pattern. Sample of last 20 commits shows
mixed styles ("update X", "fix bug", "[backend] refactor Y", "feat: add Z").

Options:
A) Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`)
   — widely adopted, enables automated changelogs, weak against drift without a hook.
B) Prefixed free-form (`[feature]`, `[bugfix]`, `[backend]`)
   — lighter, matches the team's existing tendency, no tooling needed.
C) Keep free-form
   — least friction, but harder to parse history and impossible to automate.

Recommended: A (Conventional Commits) if the project has any release automation
ambitions; B otherwise.

Which do you prefer? (A/B/C/other)
```

## Batching

When multiple gaps exist, batch them in one message and number them. The user can reply with `1A 2B 3-skip 4-defer` to address several at once.

```markdown
Gaps requiring decisions:

1. **Commit Message Format** — current state: free-form.
   A) Conventional Commits  B) Prefixed  C) Keep free-form
2. **API Path Versioning** — current state: mixed `/api/v1/` and `/v1/api/`.
   A) `/api/v1/<resource>` (recommended)  B) `/v1/<resource>`  C) No version prefix
3. **Test File Layout** — current state: mostly co-located, some in `tests/`.
   A) Co-locate everywhere (`<name>_test.py`)  B) Centralize in `tests/`

Reply with picks (e.g. "1A 2A 3-defer") or any clarifying questions.
```

## Trade-off conventions

Each option's trade-off line follows: `<benefit> — <cost>`. Keep both halves to one line.

Good:
- `widely adopted, enables automated changelogs — weak against drift without a hook`
- `lighter, no tooling needed — harder to parse history`

Bad (no cost):
- `industry standard, used by most teams` ← reads like marketing

Bad (no benefit):
- `requires a pre-commit hook` ← reads like a warning

## Recommendation conventions

If one option is clearly stronger for this project's stack and goals, lead with `Recommended: <letter>` followed by a one-line reason. Otherwise omit the recommendation line.

Do **not** recommend by default — only when there's a meaningful tilt. False neutrality is fine; false confidence is not.

## Handling deferrals

If the user says `defer` or `skip` for a gap, mark it `Deferred` in the eventual `docs/spec.md` and add a `<!-- TODO: decide on <topic> -->` HTML comment so the gap is easy to find later.

```markdown
## 8. Version Control Conventions [Deferred]

<!-- TODO: decide on commit message format — see extract-rules run 2026-05-08 -->

Current state: free-form commits. No team decision yet.
```

## Handling "other"

If the user picks `other` and provides a custom answer, treat it as a fourth option. Confirm understanding by restating before applying:

> Got it — you want commit messages to follow `[<area>] <verb> <object>` (e.g.
> `[api] fix pagination off-by-one`). I'll write that into `docs/spec.md` §Version
> Control. Confirm? (y/n)

## When to skip consultation

If a gap has an obviously correct answer for this stack (e.g., a Python project with no JS code asking about JS formatter), skip consultation and apply the obvious choice. Note the auto-decision in the Step 4 output so the user can object.
