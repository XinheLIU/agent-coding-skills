# Ticket evidence template

Last updated: 2026-10-23

Use the [orchestration evidence contract](../../../resources/protocols/orchestration.md#evidence-contract). Write a Markdown evidence file at the coordinator-resolved path with ticket/criterion references, immutable dispatch `BASE`, completion source identity and its reproducible fingerprint method/path scope, environment, deviations, omissions, raw-output references, and the next action. Keep each check's exact command (including working directory and relevant environment), result, tested revision, and completion timestamp together. Retain earlier red runs with their own revisions as history; only current acceptance rows go in the JSON sidecar checked by `collect`.

Write the adjacent `<ticket-id>.json` sidecar with `base` and a nonempty `rows` array. Each row has string fields `criterion`, `command`, `revision`, `timestamp`, and `result`. Use `passed`, `failed`, or `not-run` for results; only `passed` can establish acceptance. Timestamp is the actual command completion time in RFC 3339 with timezone. Record failed/not-run checks honestly; they block green collection. Preserve command output separately. Do not replace missing checks with sample rows.

This is a **synthetic fixture**, not a claim that a command ran. The labels stand in for full source identities; real records must use the independently reproducible identity specified by the coordinator. Every acceptance row carries its own revision even when all rows tested the same tree.

```json
{
  "base": "git:dispatch-base",
  "rows": [
    {
      "criterion": "AC-1",
      "command": "python3 -m unittest",
      "revision": "sha256:completion-tree",
      "timestamp": "2026-10-23T07:00:00Z",
      "result": "passed"
    }
  ]
}
```

Run the [stdlib checker](../scripts/check-evidence.py) from the installed skill directory, substituting coordinator-resolved paths and independently measured identities:

```sh
python3 scripts/check-evidence.py <evidence-json> --base <dispatch-BASE> --revision <current-completion-identity>
```

Exit 0 means the recorded rows have current bindings and passed results; it does not prove execution or criterion coverage. Exit 1 names `STALE-REVISION`, `BASE-MISMATCH`, `INVALID-EVIDENCE`, `INVALID-FIELD`, `INVALID-TIMESTAMP`, or `CHECK-NOT-PASSED`. The coordinator still checks commands/output, criterion coverage, fingerprint scope, and environment. Rerun stale checks on the current tree and replace current acceptance rows, preserving history; never relabel old evidence with a new revision.
