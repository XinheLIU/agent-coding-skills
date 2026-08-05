# Architecture

Last updated: {{YYYY-MM-DD}}

<!-- What the structure is and why it is split that way. Not implementation detail. -->

## Overall shape

{{Describe the layering in prose first, then a directory tree for support.}}

```text
{{Tree to the significant level only. Do not enumerate every file.}}
```

## Dependency direction

{{Which layer may reference which. An arrow diagram or a list.}}

Constraints:

- **{{Constraint}}** — {{why. A constraint without a reason gets ignored the first time it is inconvenient.}}
- **{{Constraint}}** — {{why}}

<!-- "Maintain clean layering" is not a constraint. Name the layers and the direction. -->

## Core data flows

{{The one or two most important paths, from entry point to persistence.}}

1. {{Step — the component that handles it}}
2. {{Step — the component that handles it}}

## Module responsibilities

| Module | Responsibility | Depends on |
| --- | --- | --- |
| `{{path}}` | {{single sentence}} | {{modules}} |

<!-- Every "depends on" claim must be backed by an actual import. Grep before writing it.
     No import found means no relationship, even inside the same directory. -->

## To be verified

- [ ] {{Relationship stated but not confirmed by an import — mark it rather than assert it.}}

## To be added

- [ ] {{What could not be determined from the code and needs a human.}}
