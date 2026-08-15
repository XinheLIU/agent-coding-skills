# `.claude/rules/*.md` File Format

Last updated: 2026-08-02

Loaded by extract-rules Step 4 only when authoring a new rules file. If a rules file already exists, **append or merge** — don't overwrite.

## Frontmatter spec

```yaml
---
paths:
  - "src/api/**/*.py"
  - "src/api/**/*.pyi"
---
```

- **`paths:`** — list of globs matching files this rule applies to. Omit the entire `paths:` block for **global** rules (apply to all files).
- Globs use standard glob syntax: `*` matches a path segment, `**` matches any depth.
- Be specific. Prefer `src/api/**/*.py` over `**/*.py`.

## Cross-runtime discoverability

`.claude/rules/*.md` is **Claude-specific** — Codex, OpenCode, Cursor do not auto-load it.

- For Claude-only enforcement: stop here. Document this limitation when relevant.
- For cross-runtime parity: also surface the rule in `AGENTS.md`. The symlink pattern (`.codex/rules → ../.claude/rules`) is `translate-agent-context`'s territory — recommend invoking that skill if cross-runtime support is needed.

## File body

Lead with one-sentence purpose, then numbered rules. Each rule is one line.

```markdown
---
paths:
  - "src/api/**/*.py"
---

# API Conventions

Rules for HTTP endpoint handlers in `src/api/`.

1. Path format: `/api/v1/<resource>`. Plural resource names.
2. Use `snake_case` for query parameters. Translate to camelCase only at the response layer.
3. Response envelope: `{"data": ..., "error": null}` on success. `{"data": null, "error": {"code": "...", "message": "..."}}` on failure.
4. All authenticated endpoints use `@require_auth` decorator from `src/auth/decorators.py`.
5. Validation: use Pydantic models in `src/api/schemas/`. Never validate manually in handlers.
```

## Tier 1 vs Tier 2 placement

Rules belong in `.claude/rules/` (Tier 1, auto-loaded) only if they actively shape every coding task. Lower-value content stays in `docs/spec.md` (Tier 2, reference only).

**Tier 1 — `.claude/rules/<topic>.md`:**

- Naming, formatting, code style.
- API design patterns (path-scoped to `api/`).
- DB conventions (path-scoped to models/migrations).
- Security practices.
- Test conventions (path-scoped to test files).
- Logging standards.

**Tier 2 — `docs/spec.md`:**

- Background rationale or decision history.
- Setup and configuration narrative.
- Git/commit/branch conventions (low active-coding value).
- Deferred or rarely-applicable rules.
- Workflow Norms (dynamic per-task patterns).
- Implicit Conventions index.

## Reference from `docs/spec.md`

In the spec file, the relevant section body is replaced with a one-line reference:

```markdown
## 2. API Endpoint Conventions

→ See [`.claude/rules/api.md`](../.claude/rules/api.md)
```

Do not duplicate rule bodies between `docs/spec.md` and `.claude/rules/`.

## Append vs overwrite

If `.claude/rules/<topic>.md` exists:

1. Read it.
2. Diff incoming rules against the existing list.
3. **Append** new rules. **Update** rules whose meaning changed (preserve numbering by appending). **Never overwrite** the file.
4. If the existing file has a different structure, surface the conflict to the user and ask before merging.

## Full example: `.claude/rules/database.md`

```markdown
---
paths:
  - "src/models/**/*.py"
  - "migrations/**/*.sql"
  - "migrations/**/*.py"
---

# Database Conventions

Rules for ORM models and migrations.

1. Table names: plural, `snake_case`. Example: `users`, `audit_logs`.
2. Column names: `snake_case`. Boolean columns prefixed with `is_` or `has_`.
3. Primary key: always named `id`, type `BIGINT` auto-increment.
4. Foreign keys: `<other_table_singular>_id`. Example: `user_id` references `users.id`.
5. Timestamps: every table has `created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()` and `updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()`.
6. Soft delete: use `deleted_at TIMESTAMPTZ NULL`. Never hard-delete from tables with foreign-key relationships.
7. Index naming: `idx_<table>_<column>` for single-column, `idx_<table>_<col1>_<col2>` for composite.
8. Migrations are forward-only. No `down` migrations — write a new forward migration to revert.
```
