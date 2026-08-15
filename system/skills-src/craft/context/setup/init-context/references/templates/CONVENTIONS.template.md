# Conventions

Last updated: {{YYYY-MM-DD}}

<!-- Patterns induced from the code as it is, each with an observed example.
     Never invent a convention the codebase does not follow. -->

## File naming

- {{Pattern}} — e.g. `{{RealExample.tsx}}`
- {{Pattern}} — e.g. `{{real-example.ts}}`

## Identifier naming

| Kind | Pattern | Example from this repo |
| --- | --- | --- |
| Variables, functions | {{pattern}} | `{{real example}}` |
| Classes, components | {{pattern}} | `{{real example}}` |
| Constants | {{pattern}} | `{{real example}}` |
| Test files | {{pattern}} | `{{real example}}` |

## Directory organization

{{What belongs in each significant directory.}}

## Comments and docstrings

{{The prevailing style. Where comments are expected and where they are noise.}}

## Commit messages

{{Induced from `git log`, or the recommended format if history is inconsistent.}}

```text
type(scope): what changed
```

Types: {{feat / fix / docs / refactor / test / chore}}

## Known inconsistencies

<!-- Where the codebase disagrees with itself, say so and name the target.
     Do not silently pick a winner and present it as settled. -->

- {{Concept}} is called {{A}} in `{{path}}` and {{B}} in `{{path}}`. Target: {{preferred}}.

## To be added

- [ ] {{Convention that cannot be induced from the code and needs a human.}}
