# Trigger fixture evaluation

Last updated: 2026-10-23

B17 tests selection from the current skill catalog. Each model-invocable source skill owns
`evals/trigger-fixtures.json` with at least eight automatic positive and eight automatic
negative queries. `near_miss_of` names the intended neighbor, outside the query text.
Collision cases reuse that neighbor's positive query. These are authored expectations,
not observed predictions. The explicit-only demand skill has additional explicit-request
fixtures; its invocation policy is unchanged.

## Checks and dry plan

```sh
python3 system/evals/trigger_evals.py --check
python3 -m unittest discover -s system/evals/tests -p 'test_trigger_evals.py' -v
python3 system/evals/trigger_evals.py
```

The check discovers canonical source skills, verifies both classes and near-misses, and
checks reciprocal `When NOT to use` links for trace/review and all pairs of the four
questioning callers. The unittest suite runs these checks in normal regression discovery
and exercises rejected fixtures, incorrect predictions, partial runs, and explicit policy.
The default command only prints the call plan: no adapter process, model calls, or metrics.
Use the dry-plan output for the current query count and required adapter calls; adding skills changes this budget. The integrated 584-query inventory requires 1,752 calls at three repetitions.

## Configure an adapter after model and budget approval

Copy [trigger-router.json](fixtures/trigger-router.json) to scratch. Set `model` to the
approved weak router's pinned provider/model revision, `adapter_command` to a JSON argv
array, and `max_calls` to the approved call ceiling. No shell expansion occurs. The model
and budget are deliberately unset in the shipped configuration. No provider dependency
or installation is required by this runner. The user still needs to select the model and
budget before a measured run; a call ceiling is not a currency estimate or a provider
spending limit. Adapter owners must account for model tokens, costs, and any internal
calls when obtaining that budget.

The runner sends one JSON request to the adapter's stdin for each repetition:

```json
{
  "schema": 1,
  "model": "approved-pinned-model",
  "query": "Review this PR for production readiness.",
  "catalog": [{"name": "acs-review-code-quality", "description": "Use when ...", "automatic": true}],
  "explicit_skill": null,
  "instruction": "Select relevant skills by their descriptions..."
}
```

The actual catalog includes all source descriptions and invocation flags. It contains no
skill bodies. The target skill, expected label, neighbor, and fixture ID are withheld.
Each process must make an isolated routing observation without invoking the selected
skills, return one JSON object on stdout, and exit zero:

```json
{"model": "approved-pinned-model", "selected": ["acs-review-code-quality"]}
```

An empty array means no skill selected. Use exact IDs, without duplicates. The adapter
must propagate the pinned model to the provider and report the model actually used;
this generic runner can check the echo, but cannot independently attest provider identity.
Automatic routing may select only `automatic: true` skills. An explicit case starts with
a slash invocation and supplies `explicit_skill`; a name mentioned casually grants no
permission. An unknown or unauthorized explicit-only selection voids the run rather than
being accepted as a valid observation. Do not execute skills or request external actions.

```sh
python3 system/evals/trigger_evals.py --config .scratch/trigger-router.json --execute --output .scratch/trigger-results.json
```

Use `evidence_kind: mock` for local test doubles. `measured` is an adapter operator's
provenance declaration, not proof of a model call; retain the adapter implementation and
provider execution evidence alongside any measured report. Tests use mock responses
only. No live weak-model success is claimed by the repository fixtures.

## Reports and failure semantics

Reports include date, pinned model, configuration and runner hashes, a fingerprint of
all source skill bodies plus fixtures and runner, raw selection arrays per repetition,
and completed/planned call counts. Retain reports in scratch. Regenerate them after
source changes; source changes detected during execution void the run. The fingerprint
covers dirty source bytes, not just Git HEAD.

At the default trigger threshold of 0.5, a skill must appear in at least two of three
responses to count as selected. Each skill has separate automatic and explicit metrics:
`tp`, `fp`, `tn`, `fn`, precision, and recall. A denominator of zero is `null`, never a
fabricated perfect score. A group with only negatives passes only if it has no false
positives; a positive group with no selections fails recall. Default minimum precision
and recall are 0.9, configurable before the run. Every near-miss must also select its
named neighbor and omit its target, so abstaining on every negative cannot pass the
collision gate. These fixtures cover scoped requests; they do not establish general
multi-skill routing quality.

Exit 0 means a valid dry plan/check, or a complete run meeting both thresholds and the
collision gate (inspect `status` and `evidence_kind`). Exit 1 means a fixture check or
measured/mock metric gate failed. Exit 2 means blocked configuration or a `void` run.
A timeout, adapter failure, invalid JSON, mismatched model, unauthorized selection, or
source drift stops immediately, retains partial selections, and emits no aggregate
metrics. There are no retries or fabricated completions.

## Provenance and limits

Adapted the balanced trigger/no-trigger cases, named near-misses, repetitions, and
weak-router intent from PM-Skills `deliver-prd/evals/trigger-fixtures.json` and
`run-trigger-evals.mjs` in the read-only reference corpus. ACS uses a stdlib Python JSON
adapter rather than depending on a particular host. The fixture schema is intentionally
small; no third-party schema validator is required. The model/budget decision, measured
precision and recall, and actual weak-model collision behavior remain unverified.
