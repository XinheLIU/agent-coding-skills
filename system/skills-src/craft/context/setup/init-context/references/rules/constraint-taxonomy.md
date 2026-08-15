# Constraint Taxonomy

Last updated: 2026-08-02

Loaded by extract-rules when a finding's classification is ambiguous. Three constraint types — static, dynamic, implicit — are mutually exclusive. Pick exactly one per finding.

## Static constraints

**Definition:** Permanent rules that apply across all tasks and all files (or all files in a path-scoped subtree). The agent should follow them without being reminded each task.

**Home:** `.claude/rules/*.md` (Claude auto-loaded). Cross-runtime rules also surface in `AGENTS.md`.

**Examples:**

1. *Naming.* "Use `snake_case` for variables and functions. `PascalCase` for classes. `UPPER_SNAKE_CASE` for module-level constants."
2. *API stability.* "Class method signatures must remain backward-compatible. New parameters must be optional with defaults."
3. *SQL safety.* "All queries use parameterized statements. Never concatenate user input into SQL strings."
4. *Test conventions.* "Test files live next to source as `<name>_test.py`. Test functions start with `test_`."
5. *Frontend.* "All API calls go through `src/api/client.ts`. No direct `fetch()` calls in components."
6. *Security.* "All authenticated endpoints use `@require_auth` decorator. No bypass for any reason."
7. *Logging.* "Log all external API calls at INFO level with the request ID."

## Dynamic constraints

**Definition:** Per-task ad-hoc guardrails. The user re-states them each invocation. The agent cannot reliably remember them between tasks.

**Home:** describe the *meta-pattern* in `docs/spec.md` §Workflow Norms. Do **not** encode as a static rule — that would force the constraint when the user didn't ask for it.

**Examples:**

1. *Edit scope.* "Only modify these three files." (Re-stated per task.)
2. *Plan-first.* "Show me the plan before writing any code." (Re-stated per task.)
3. *Pause-and-ask.* "If anything is unclear, stop and ask — don't guess." (Re-stated per task.)
4. *Output format.* "Reply in bullet points only." (Re-stated per task.)
5. *No-delete.* "Don't delete any files in this run." (Re-stated per task.)

**Meta-pattern documentation example (`docs/spec.md`):**

> ### Workflow Norms
>
> - This team typically narrows edit scope per task. If a task doesn't name specific files, ask before broadening.
> - Plan confirmation is the default for changes spanning more than ~3 files. Surface a plan and wait for approval.
> - Prefer pause-and-ask over best-guess when requirements are ambiguous.

## Implicit conventions

**Definition:** Norms that exist beyond the code's structure — embedded in HTML comments, sidebar notes, or non-obvious markers. Often invisible to a fresh agent reading the code.

**Home:** leave the marker at the source. **Index** it in `docs/spec.md` §Implicit Conventions so the agent can discover it. If the convention generalizes, promote to an explicit rule in `.claude/rules/`.

**Examples:**

1. HTML comment in a doc:
   ```html
   <!-- Do not delete this section. It is referenced by the onboarding flow. -->
   ```
2. Sidebar note on an interface file:
   ```python
   # NOTE: This interface is consumed by Partner A. Do not change the signature.
   def get_user_profile(user_id: str) -> Profile: ...
   ```
3. File-level marker:
   ```python
   # DO NOT MOVE — referenced by external CI job at runtime by absolute path.
   ```
4. Section header in a config file:
   ```yaml
   # ----- LEGAL: do not modify without legal review -----
   ```
5. Test file decoration:
   ```python
   @pytest.mark.canary  # Runs in production smoke tests; keep stable.
   def test_health(): ...
   ```

**Index format in `docs/spec.md`:**

```markdown
### Implicit Conventions

| Location | Marker | Convention |
|---|---|---|
| `docs/onboarding.md:42` | `<!-- Do not delete -->` | Section is referenced by onboarding flow |
| `src/api/partner.py:12` | `# NOTE: Consumed by Partner A` | Signature must remain stable |
| `scripts/cron.py:1` | `# DO NOT MOVE` | Path is hardcoded in external CI |
```

## Decision rules for ambiguous classification

### "Is it static or dynamic?"

- Does it apply to *all* tasks unless the user opts out? → **Static**.
- Does the user have to re-state it each task to make it apply? → **Dynamic**.
- Borderline case: a rule that *should* be permanent but isn't enforced. → **Static**, with a note that it's not yet codified.

### "Is it static or implicit?"

- Is the rule explicit somewhere (a doc, a config, a CI check)? → **Static**.
- Does it only live as a comment marker or sidebar note? → **Implicit**.
- A static rule generalizing from many implicit markers (e.g., "all interfaces with `# NOTE: Consumed by` comments are stable") → both: index the markers as implicit, promote the generalization to static.

### "Is it dynamic or implicit?"

- Is it stated in a per-task prompt? → **Dynamic**.
- Is it embedded in the code itself? → **Implicit**.
- These rarely confuse — the location of the marker is the clue.

### When in doubt

Default to **static** if the rule applies repo-wide. Default to **implicit** if the rule is local to one file or asset and only appears as a comment. Use **dynamic** only when you're sure the user re-states it per task.
