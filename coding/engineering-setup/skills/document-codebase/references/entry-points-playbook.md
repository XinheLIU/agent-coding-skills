# Entry-Points Playbook

Last updated: 2026-05-16

The **entry-point trace** is the project's external contract. Every place a user, another service, a developer, a scheduler, or an operator can *trigger* code execution belongs here. It is the single doc a new engineer reads to learn "what can this thing actually be told to do?".

Output file: `docs/codebase-documentation/entry-points.md`. Template: `assets/templates/ENTRY_POINTS.template.md`.

Treat entry points as the **coordinate origin** of onboarding. Do not start from directory order. Every important module should be reachable from at least one trigger or classified explicitly as core domain, infrastructure, shared utility, test support, legacy/migration, or unused/dead code.

## Surfaces to enumerate

Group entry points by surface. Skip any group the project does not expose.

| Surface | Typical signature |
|---|---|
| **HTTP** | FastAPI/Flask/Django routers, Express, Gin, Spring controllers |
| **MCP** | `@mcp.tool`, `@server.tool`, `FastMCP.tool()` |
| **CLI** | `argparse`, `click`, `typer`, `cobra`, `__main__.py`, `bin/*` scripts |
| **Scheduled** | cron, supercronic, APScheduler, Celery beat, Airflow DAGs |
| **Queue consumers** | Kafka/RabbitMQ/SQS consumers, Celery workers, Dramatiq actors |
| **Library exports** | `__all__`, public re-exports in `__init__.py`, package entry points in `pyproject.toml` |

## Discovery recipes

Run from repo root. Adjust source paths to the project's layout.

### HTTP (FastAPI / Starlette)

```bash
grep -rn -E '@(app|router)\.(get|post|put|patch|delete)\(' services/ pipelines/
grep -rn 'APIRouter\(' services/
grep -rn 'include_router(' services/
```

### MCP tools

```bash
grep -rn -E '@(mcp|server|app)\.tool\b|FastMCP\(|add_tool\(' services/
```

### CLI (Python)

```bash
grep -rn -E '(argparse|click|typer)\b' services/ pipelines/
grep -rln '^if __name__ == .__main__.' services/ pipelines/
# pyproject entry points
grep -nE '^\[project\.scripts\]|^\[tool\.poetry\.scripts\]' pyproject.toml services/*/pyproject.toml pipelines/*/pyproject.toml
```

### Scheduled

```bash
# supercronic / cron
find deploy/ -name 'crontab*' -o -name '*.cron'
grep -rn 'supercronic\|@cron\|APScheduler\|CronTrigger' services/
```

### Queue consumers

```bash
grep -rn -E 'consume\(|@consumer|Celery\(|task_queue|kafka.Consumer' services/
```

## What to capture per entry point

A row, not a paragraph. One sentence each.

| Field | Example |
|---|---|
| **Surface** | HTTP / MCP / CLI / Scheduled / Consumer |
| **Trigger** | `GET /data/plans`, `mcp:list_plans`, `python -m pipelines.rtb_data sync`, `cron 15 * * * *` |
| **One-line purpose** | "Return TaskPlan queue for a given owner" |
| **Key inputs** | `owner` (str), `status` (enum), `limit` (int ≤ 200) |
| **Response / side effect** | `200 → {plans: [...]}`; or "inserts into `ods.rtb_creative`" |
| **Owning module** | `services/data_service/app/routes/plans.py` |
| **Source** | `services/data_service/app/routes/plans.py:42` |
| **Downstream calls** | `app.db.read_only_cursor`, `app.repos.plans.list_for_owner` |

Group rows by surface, sort by trigger inside each group.

## Origin trace for non-trivial flows

For non-trivial entry points, trace beyond the registration row:

1. **External input receiver** — the route handler, command callback, message listener, SDK function, or scheduled job function.
2. **Validation / DTO** — where shape, type, authorization, and semantic validation happen.
3. **Domain language conversion** — where route params, JSON, CLI args, or events become command objects, entities, value objects, or domain terms.
4. **Business decision owner** — the module that decides what should happen, not the controller or repository that only forwards data.
5. **Implementation details** — where database, queue, filesystem, network, cache, storage, framework glue, concurrency, or deployment-specific behavior enters.
6. **Caller output** — response body, event ack, stdout/exit code, scheduled side effect, or public return value.

This trace is usually one table row per entry point. Use a sequence/dynamic diagram only when ordering or retries matter.

## Tracing downstream calls

For each entry point, list the immediate downstream modules it touches (depth 1 is usually enough). Use the import graph, not the call graph — the call graph is too noisy at this level. If a flow is genuinely critical (auth, billing, plan creation) and crosses ≥3 modules, promote it to a `c4-dynamic-{flow}.md` sequence diagram and link from the entry-point row.

## Cross-links

- Link each row's owning-module path to its `README.md` (if it exists) or to the package directory.
- Link the doc itself from `docs/codebase-documentation/README.md` and from `CLAUDE.md` Context Files (per hard rule 16).
- If the project already has a partial API doc (e.g. `docs/API.md`), link it from the HTTP section and avoid duplicating endpoint detail — the entry-point trace is the **index**, the API reference is the **schema**.

## Anti-patterns

- Dumping all routes from `app.routes` without grouping → unreadable. Group by router / module.
- Pasting request/response JSON schemas inline → that's `api/reference.md`'s job.
- Including private helper functions → only user-triggerable entry points.
- "TBD" rows → either find it or omit it; the doc must reflect reality.
