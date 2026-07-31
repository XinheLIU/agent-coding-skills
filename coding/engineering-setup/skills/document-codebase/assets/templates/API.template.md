<!--
Template last updated: 2026-07-18

Fill-in skeleton for an API reference. The authoritative API-writing guidance
lives in `.claude/skills/document-codebase/references/doc-types-playbook.md`.

Rules while filling this in:
  1. Replace every [placeholder]. Do not ship with them.
  2. Group REST APIs by owning module/router, not by filesystem order.
  3. For every route, cite the handler or registration site with `path:line`.
  4. Record method, path, one-sentence description, request parameters, response
     structure, error shape, and orientation.
  5. Capture whether public interfaces hide implementation details or leak table
     names, queue names, framework types, or storage concerns.
-->

# API Reference

Last updated: [YYYY-MM-DD]

*Public interfaces exposed by [Project Name]. Pair this with [`../entry-points.md`](../entry-points.md): entry points show every trigger; this document describes API contracts and how they map to the model without exposing unnecessary implementation details.*

## Overview

- **Base URL:** `[https://host/prefix]`
- **Auth:** `[scheme | none]`
- **Versioning:** `[path/header/media type/none]`
- **Primary orientation:** `[resource-oriented | action-oriented | event-oriented | command-oriented | mixed]`
- **Public consumers:** `[users/services/tools/SDKs]`

## API shape analysis

| Question | Finding | Evidence |
|---|---|---|
| Are APIs resource-, action-, event-, or command-oriented? | `[finding]` | `[file:line]` |
| Are names consistent across routes, DTOs, tables, UI labels, and tests? | `[finding]` | `[file:line]` |
| Does the project prefer command objects, thin controllers, fat models, service layers, generated clients, or repository interfaces? | `[finding]` | `[file:line]` |
| Are errors shaped consistently? | `[finding]` | `[file:line]` |
| Do public interfaces hide implementation details? | `[finding]` | `[file:line]` |
| Do developer-facing commands encode good practice such as migrations, tests, scaffolding, or local setup? | `[finding]` | `[file:line]` |

## Shared contracts

### Authentication and authorization

| Concern | Contract | Source |
|---|---|---|
| Authentication | `[header/cookie/token/session]` | `[file:line]` |
| Authorization | `[role/scope/rule]` | `[file:line]` |

### Error shape

```json
{
  "error": {
    "code": "[ERROR_CODE]",
    "message": "[human-readable message]",
    "details": {}
  }
}
```

| Status | Code | Meaning | Source |
|---|---|---|---|
| `400` | `[CODE]` | [validation or semantic error] | `[file:line]` |
| `401` | `[CODE]` | [auth failure] | `[file:line]` |
| `500` | `[CODE]` | [unexpected failure shape] | `[file:line]` |

### Pagination, filtering, and sorting

| Mechanism | Parameters | Default / limit | Source |
|---|---|---|---|
| Pagination | `[limit, cursor/page]` | `[default/max]` | `[file:line]` |
| Filtering | `[field names]` | `[constraints]` | `[file:line]` |
| Sorting | `[field names]` | `[default]` | `[file:line]` |

## REST endpoints by module

### `[owning module or router]`

[One-sentence responsibility of this API group.]

| Method | Path | Orientation | Description | Main request parameters | Response structure | Handler source |
|---|---|---|---|---|---|---|
| `GET` | `/[resource]` | Resource | [one-sentence description] | query: `[limit]` (`int`) | `200 → {"items": [...]}` | `[file:line]` |
| `POST` | `/[resource]/[action]` | Action / command | [one-sentence description] | body: `[RequestModel]` | `202 → {"task_id": "..."}` | `[file:line]` |

#### `GET /[resource]`

[One-sentence description. State idempotency, auth scope, and rate-limit class if relevant.]

| Contract field | Value |
|---|---|
| Orientation | `[resource | action | event | command]` |
| Handler source | `[file:line]` |
| Owning module | `[path/to/module]` |
| Request model / DTO | `[ModelName]` (`[file:line]`) |
| Response model / DTO | `[ModelName]` (`[file:line]`) |
| Validation source | `[framework/model/manual validation]` (`[file:line]`) |
| Domain decision owner | `[domain/service module]` (`[file:line]`) |
| Persistence / side effects | `[db/queue/cache/filesystem/network/none]` |
| External calls | `[service/API/none]` |
| Idempotency | `[safe/idempotent/non-idempotent; key if any]` |

**Request**

| Location | Name | Type | Required | Notes |
|---|---|---|---|---|
| Query | `[name]` | `[type]` | `[yes/no]` | `[constraints/default]` |
| Path | `[id]` | `[type]` | yes | `[resource identity]` |
| Body | `[field]` | `[type]` | `[yes/no]` | `[constraints/default]` |

**Response**

```json
{
  "[field]": "[type/example]"
}
```

**Errors from code**

| Status | Code / exception | Condition | Source |
|---|---|---|---|
| `400` | `[code]` | [condition] | `[file:line]` |

**Example**

```bash
curl -X GET "[base-url]/[resource]" \
  -H "Authorization: Bearer [token]"
```

<!-- Repeat one detailed endpoint block per non-trivial endpoint. Keep trivial endpoints in the summary table only if detail adds no value. -->

## Events, webhooks, or streaming APIs

Delete this section if the project exposes none.

| Event / topic | Orientation | Producer | Consumer | Payload DTO | Delivery semantics | Source |
|---|---|---|---|---|---|---|
| `[event.name]` | Event | `[module]` | `[module/external]` | `[ModelName]` | `[at-most-once/at-least-once/order guarantees]` | `[file:line]` |

## SDK / public library calls

Delete this section if the project exposes none.

| Call | Orientation | Purpose | Parameters | Return type | Source |
|---|---|---|---|---|---|
| `[client.method()]` | Command / resource | [one-sentence description] | `[arg]` (`type`) | `[type]` | `[file:line]` |

## Mismatches and leaks

- [Route / DTO / table / test naming mismatch, with source links.]
- [Public API leaks internal table names, queue names, framework types, storage keys, or deployment details.]
- [Missing or inconsistent error shape.]
