---
id: "{{NNN}}"
title: "{{Imperative-phrase title}}"
spec: "{{spec-id}}"      # omit for standalone tasks not owned by a spec
type: agent              # agent | human
state: backlog           # backlog | ready | claimed | in-progress | blocked | review | done | abandoned
depends_on: []           # list of task ids that must be done first, e.g. ["001", "002"]
claimed_by: ~            # fill before starting work
verify: ""               # command that must exit 0 for review → done transition
---

## Context

{{What this task is and why it exists. One paragraph.}}

## Constraints

{{Hard constraints the implementer must not violate. Omit section if none.}}

## Acceptance detail

{{Specific, testable criteria beyond what the verify command checks. Omit if verify covers everything.}}
