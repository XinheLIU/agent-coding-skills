<!--
Template last updated: 2026-08-02

Fill-in skeleton for the data-model / ER doc. The authoritative discovery
recipes and conventions live in
`.claude/skills/document-codebase/references/data-model-playbook.md`.

Rules while filling this in:
  1. Replace every [placeholder]. Do not ship with them.
  2. Derive the canonical models by comparing data models, DTOs, and database
     table creation SQL. DDL wins when they disagree; record mismatches.
  3. Use actual SQL types (BIGINT, TEXT, TIMESTAMPTZ, JSONB, …), not Python annotations.
  4. Show keys (PK / FK) only in the ER diagram body; full field tables go in
     the per-table sections below.
  5. Cite the DDL source for every table: `path:line` to the migration or
     `CREATE TABLE` statement.
  6. Name the schema owner for every table — the module allowed to write it.
-->

# Data Model

Last updated: [YYYY-MM-DD]

*Canonical entities the project stores. Pair this with [`entry-points.md`](./entry-points.md): one names what flows in, this names what gets stored. This document captures the model before implementation details: field names and types, keys, enums, relationships, and the modules allowed to write each entity.*

## Core model inventory

| Model | One-sentence description | Source kind | Backing table / storage | Input / output DTOs | Owner | Source |
|---|---|---|---|---|---|---|
| `[ModelName]` | [what concept it represents] | `[DDL | ORM | DTO | message]` | `[schema.table]` | `[RequestModel / ResponseModel]` | `[module]` | `[file:line]` |

## ER diagram

```mermaid
erDiagram
    [entity_a] ||--o{ [entity_b] : "[verb]"
    [entity_b] ||--o{ [entity_c] : "[verb]"

    [entity_a] {
        bigint   [a_id] PK
        text     [name]
        timestamptz created_at
    }

    [entity_b] {
        bigint   [b_id]  PK
        bigint   [a_id]  FK
        text     [name]
        [enum_type] status
        jsonb    payload
    }

    [entity_c] {
        bigint   [c_id]   PK
        bigint   [b_id]   FK
        date     stat_date
    }
```

### Relationship rationale

| Relationship | Cardinality | Why it exists | Enforced by | Source |
|---|---|---|---|---|
| `[entity_a] → [entity_b]` | `one-to-many` | [business meaning, not "has many"] | `[FK | unique constraint | application code]` | `[file:line]` |

## Schema ownership

| Schema | Owning module | Write API | Notes |
|---|---|---|---|
| `[ods]` | `[pipelines/...]` | `INSERT ... ON CONFLICT DO NOTHING` | [raw external sync] |
| `[dwd]` | `[pipelines/...]` | range `DELETE + INSERT` | [derived from ods] |
| `[app]` | `[services/...]` | mixed read/write | [serving layer] |

## Entities

### `[schema].[table_name]`

[One-sentence purpose.]

| Field | Type | Null | Default | Notes |
|---|---|---|---|---|
| `[id]` | `BIGINT` | no | — | PK |
| `[fk_id]` | `BIGINT` | no | — | FK → `[other_schema.other_table.id]` |
| `[name]` | `TEXT` | no | — | |
| `[status]` | `[enum_type]` | no | `'[default]'` | enum below |
| `created_at` | `TIMESTAMPTZ` | no | `now()` | |
| `payload` | `JSONB` | yes | `NULL` | [raw external response] |

- **Primary key:** `[id]`
- **Foreign keys:** `[fk_id]` → `[other_schema.other_table.id]`
- **Unique constraints:** `([col_a], [col_b])`
- **Natural / business keys:** `[external_id]`, `[tenant_id + name]`
- **Idempotency keys:** `[source_system + external_id]`
- **Enum `[enum_type]`:** `[value_1] | [value_2] | [value_3]`
- **Enum semantics:** `[value_1] = [meaning]; [value_2] = [meaning]`
- **Indexes:** `([col_a], [col_b] DESC)`
- **Schema owner:** `[module path]`
- **DDL source:** `[file:line]`

<!-- Repeat per canonical entity. Stay disciplined: 5–12 canonical entities, not 30. -->

## Lookups & enums

| Enum | Values | Declared at |
|---|---|---|
| `[enum_type]` | `[v1] | [v2] | [v3]` | `[file:line]` |

## Retention & lineage

- [Layered derivation rule, e.g. "DWD is refreshed by range DELETE+INSERT from ODS for the half-open window `[today − N days, today]`."]
- [Retention windows, archival policy, GDPR/PII concerns.]
- [Link to spec or ADR that established these rules.]

## Mismatches & gaps

[Anything DDL and ORM disagree on, tables documented elsewhere but missing here, or canonical entities that don't yet have a stable schema.]
