<!--
Template last updated: 2026-08-02

Fill-in skeleton for the entry-point trace. The authoritative discovery
recipes and conventions live in
`.claude/skills/document-codebase/references/entry-points-playbook.md`.

Rules while filling this in:
  1. Replace every [placeholder]. Do not ship with them.
  2. Treat entry points as the coordinate origin; every important flow starts
     from an external trigger, not from directory order.
  3. Group entry points by surface; within a group, sort by trigger.
  4. Cite each entry point with `path:line` to the registration site
     (router decorator, CLI handler, etc.), not the helper it calls.
  5. Delete any surface section the project does not expose.
-->

# Entry Points

Last updated: [YYYY-MM-DD]

*External contract of the project. Everything below is a way for a user, another service, an operator, a developer, or a scheduler to trigger code in this repo. Use this as the coordinate origin: every main flow radiates from one of these triggers into the model and then into implementation details.*

## Surfaces

- [HTTP](#http)
- [MCP tools](#mcp-tools)
- [CLI commands](#cli-commands)
- [Scheduled jobs](#scheduled-jobs)
- [Queue consumers](#queue-consumers)

Delete sections that do not apply.

## HTTP

Base URL: `[https://host:port/prefix]`. Auth: `[scheme, e.g. Bearer token | none]`.

| Method + Path | Purpose | Key inputs | Response / side effect | Owning module | Source |
|---|---|---|---|---|---|
| `GET /[path]` | [one-sentence purpose] | `[param]` ([type]), `[param]` ([type]) | `200 → {[shape]}` | `[services/...]` | `[file:line]` |
| `POST /[path]` | [one-sentence purpose] | body: `[ModelName]` | `201 → {[shape]}` | `[services/...]` | `[file:line]` |

Full schemas: [`docs/codebase-documentation/api/reference.md`](./api/reference.md).

## MCP tools

Server: `[FastMCP instance name | module]`. Transport: `[stdio | http | sse]`.

| Tool name | Purpose | Key inputs | Returns | Owning module | Source |
|---|---|---|---|---|---|
| `[tool_name]` | [one-sentence purpose] | `[arg]` ([type]) | `[shape]` | `[services/...]` | `[file:line]` |

## CLI commands

| Command | Purpose | Key flags | Side effect | Owning module | Source |
|---|---|---|---|---|---|
| `[python -m pkg subcmd]` | [one-sentence purpose] | `--[flag]`, `--[flag]` | `[what changes]` | `[services/... | pipelines/...]` | `[file:line]` |

## Scheduled jobs

Runner: `[supercronic | APScheduler | k8s CronJob | …]`. Schedule source: `[deploy/.../crontab | settings | …]`.

| Schedule (cron) | Job | Purpose | Owning module | Source |
|---|---|---|---|---|
| `[*/15 * * * *]` | `[job-name]` | [one-sentence purpose] | `[pipelines/...]` | `[file:line]` |

## Queue consumers

Broker: `[Kafka | RabbitMQ | Redis Streams | …]`.

| Topic / queue | Consumer | Purpose | Owning module | Source |
|---|---|---|---|---|
| `[topic.name]` | `[consumer-name]` | [one-sentence purpose] | `[services/...]` | `[file:line]` |

## Origin traces

For each non-trivial entry point above, trace the flow from external language to domain language and then to implementation details. Skip trivial CRUD reads.

| Trigger | External input receiver | Validation / DTO | Domain language conversion | Business decision owner | Implementation details | Caller output | Source |
|---|---|---|---|---|---|---|---|
| `POST /[path]` | `[handler/controller]` | `[RequestModel]` | `[command/entity/value object]` | `[domain/service module]` | `[db/queue/filesystem/network/cache]` | `201 → {[shape]}` | `[file:line]` |
| `[cli command]` | `[parser/handler]` | `[args/schema]` | `[command object]` | `[domain/service module]` | `[db/job/external API]` | `[stdout/exit code/side effect]` | `[file:line]` |

## Downstream call traces (depth 1)

List the immediate modules each entry point touches. Use this to spot fan-out and shared dependencies. Promote critical flows that cross three or more modules into a dynamic diagram.

```
[POST /data/plans]   → app.repos.plans.insert
                     → app.events.emit("plan.created")
[mcp:list_plans]     → app.repos.plans.list_for_owner
[python -m rtb_data sync]
                     → pipelines.rtb_data.external.fetch
                     → pipelines.rtb_data.ods.upsert
                     → pipelines.rtb_data.dwd.refresh
```

## Notes

- [Anything operationally important: rate limits, idempotency keys, retry rules, ordering guarantees, dead-letter queues.]
- [Where to look when an entry point misbehaves: log location, metric name, dashboard URL.]
