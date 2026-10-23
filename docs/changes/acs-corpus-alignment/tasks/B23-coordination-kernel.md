# B23-coordination-kernel: Move the mechanical half of the coordinator into one executable kernel

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B14-status-json, B19-evidence-binding, B1-catalog-budget
affects: a new script under `scripts/` or `system/skills-src/authoring/.../scripts/`; `system/protocols/context-coordination.md`
Effort: L

## Scope

The coordinator — claims, serialized writes, freshness — is "a written Harness contract, not a new executable service" (`context-coordination.md:12`).

Build one CLI any host can call:
- resolve identity and paths;
- report status and the frontier;
- scan consumed revisions and list `needs review` candidates;
- verify evidence revisions;
- run the catalog and derived-surface checks.

The prose keeps the judgment: what must be serialized and why. The kernel is read-only except for explicitly authorized writes.

## Inputs

- Analysis: §8.5 U8, §10 B23.
- Sources: gstack "The harness is in the repo now"; OpenSpec status CLI; the SDLC playbook's hooks and evals.

## Verification

- Commands run on this repository and reproduce the current status, frontier and freshness findings.
- A stale evidence row is rejected; a fresh one passes.
- Unit tests cover path resolution, cycle detection and budget checks.
- The protocol links to the kernel instead of restating mechanics.

## Blockers

Location/language settled by parent: stdlib Python CLI under `scripts/`, read-only by default, reusing the B14 scanner and B19 evidence checker. Independent acceptance review remains pending.

## Coordination proposal

Consumes B14, B19, B1. B24 binds the kernel to host primitives; land B23 first.

## Execution rulings

Recorded before implementation on 2026-10-23. Parent approved `scripts/` and stdlib Python, a read-only default, and reuse of B14 status/scanning and B19 evidence validation. This contribution supplies no write operation, claim service, host dispatch, or new runtime dependency. Canonical status, write serialization, judgment of material freshness, and authorization stay with the coordinator.

The other settled parent rulings remain boundaries, not B23 deliverables: B11 observability belongs to `acs-design-contracts`; B10 consumers must declare verification commands and environments, with unset values blocking execution and checks limited to local mock/scratch/dry-run operations; B7 review fix rounds are distinct from B8 operational retries and must preserve authorization and source freshness. B17 trigger fixtures/configurable runner and B16/B17 model/budget selection are separate work; the pending user decision cannot support a live metric claim. No external PR, merge, deploy, installation, publication, or subagent action is authorized here.

Mechanical ruling: use an explicit local Markdown adapter and fail on ambiguous identities rather than infer tracker configuration from prose. Hosts resolve configured/external tracker references first and supply the local paths. Store optional consumed file revisions inside their owning Markdown record in a named JSON fence; never create a second status store. Missing bindings remain unassessed, changed/missing/unverifiable sources become review candidates, and the kernel never changes readiness automatically. Derived checks call the existing builder's `--check` and may use temporary output internally; selected source/generated trees remain read-only.

## Evidence

Baseline captured before edits: 1,144 tracked/nonignored untracked paths, including integrated dirty source and ticket records; SHA-256 `810b726c0da14d402319e054338696fb5fb1dacacd4d6172f65712e478c39dce` over sorted JSON baseline manifest. Byte copies, symlink targets, initial status, HEAD and binary diff are retained under `.scratch/B23-coordination-kernel/`. Validation completed below; independent review pending.

## Consumed source revisions

Kernel dependency bindings (exact file bytes; domain materiality remains review-owned):

```acs-consumed-revisions
[
  {
    "source": "../../../../system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py",
    "revision": "sha256:50ddbf4c18d6c33c96a1e701338dae38b766e5254722f2403c265f316eaa1598",
    "scope": "canonical identity, status, frontier and cycle checks"
  },
  {
    "source": "../../../../system/skills-src/build/acs-implement/scripts/check-evidence.py",
    "revision": "sha256:72a51e456625be6146812bebcdc0eefdda268331112607f6bfc034752f01c2db",
    "scope": "recorded evidence revision validation"
  },
  {
    "source": "../../../../system/evals/validate_suite.py",
    "revision": "sha256:8a087edf92c989d002c8e356b2a21cb04775c8aa1b543b2d48ee6d47e93ee916",
    "scope": "catalog budget and source validation"
  },
  {
    "source": "../../../../scripts/build-plugins.py",
    "revision": "sha256:c7bbb18a40273370b4efe11c439a5f7e6c7d01dad461bea37bdc6e0041b6ca4a",
    "scope": "read-only derived output comparison"
  }
]
```

## Validation results

Tested source identity: `sha256:9f6d59e19294edef9e4c4f79134be3e70a203a4c5bd12fef60088c77b9c5fb7b`. Exact manifest: `.scratch/B23-coordination-kernel/validation-source-manifest.json`; SHA-256 of UTF-8 `json.dumps(path_to_sha256, sort_keys=True)` over all file bytes beneath `scripts/`, `system/`, and `catalog/`, excluding `__pycache__` and `.pyc`, dereferencing file symlinks. The validation runner checked identical source manifests before and after every command. Ticket/evidence bookkeeping and generated output are excluded. Environment: Python 3.14.6, macOS-26.6.2-arm64-arm-64bit-Mach-O, `PYTHONDONTWRITEBYTECODE=1`; compaction tokenizer configuration was supplied through the three user-provided environment variables and remains outside tracked source.

| Exact command | Result |
| --- | --- |
| `python3 -m unittest discover -s system/evals/tests -p test_coordination_kernel.py -v` | PASS (exit 0) |
| `python3 -m unittest discover -s system/skills-src/authoring/acs-draw-portfolio-dag/tests -v` | PASS (exit 0) |
| `python3 -m unittest discover -s system/evals/evals -p test_*.py -v` | PASS (exit 0) |
| `python3 scripts/acs-coordination.py resolve docs/changes/acs-corpus-alignment --ticket B23-coordination-kernel` | PASS (exit 0) |
| `python3 scripts/acs-coordination.py status docs/changes/acs-corpus-alignment` | PASS (exit 0) |
| `python3 scripts/acs-coordination.py freshness docs/changes/acs-corpus-alignment` | PASS (exit 0) |
| `python3 scripts/build-plugins.py --output .scratch/B23-coordination-kernel/plugins` | PASS (exit 0) |
| `python3 scripts/build-plugins.py --check --output .scratch/B23-coordination-kernel/plugins` | PASS (exit 0) |
| `python3 scripts/validate-protocols.py --plugins .scratch/B23-coordination-kernel/plugins` | PASS (exit 0) |
| `python3 system/evals/validate_suite.py` | PASS (exit 0) |
| `python3 scripts/acs-coordination.py checks --plugins .scratch/B23-coordination-kernel/plugins` | PASS (exit 0) |
| `python3 -m unittest discover -s system/evals/tests -p test_*.py -v` | FAIL (exit 1): 121/122 pass; one independently reproduced baseline failure |
| `git diff --check` | PASS (exit 0) |
| `git diff --cached --name-only` | PASS (exit 0) |

Focused tests: 12 pass, covering foreign-CWD/symlink path resolution, ambiguous and absent IDs, B14 parity, missing dependencies, cycles, fresh/changed/missing/unsupported premises, malformed bindings, current/stale evidence and BASE mismatch, no source rewrites, real catalog subprocess acceptance at 260 bytes/rejection at 300 bytes, and real builder comparison rejecting drift without repairing it. B14 regression suite: 16 pass. Evidence/contract regression suite: 19 pass. All configured compaction checks ran without skips, and shared semantics/catalog/package regressions passed.

The broad suite's sole failure is `test_scope_postures.ScopePostureTests.test_phase_c_defines_postures_and_record_contract`: untouched integrated source says `Raise concerns once`, while the preexisting test expects `Raise concerns about it once`. Running that exact test against the preserved baseline reproduces one failure and zero errors (`baseline-scope-postures.log`). This is not fixed by B23 and is not counted as green evidence. Initial focused testing also found three macOS fixture path expectations that failed to normalize `/var` to `/private/var`; those fixtures were corrected and all focused checks passed again.

Repository smoke results: 25 tickets; frontier is `acs-corpus-alignment/B17-trigger-fixtures`, `acs-corpus-alignment/B7-review-seat`; next is `implement` for B17. These are B14 recorded-state results, not authorization or proof that model-selection gates are settled. Freshness after adding this ticket's four in-record dependency bindings: four current bindings, zero review candidates/errors, and 28 unassessed records. This explicitly does not certify all repository premises current. Scratch-only negative fixtures establish changed/missing premise detection.

`python3 scripts/acs-coordination.py verify .scratch/B23-coordination-kernel/evidence.json --base <baseline fingerprint above> --revision <tested source identity above>` passes for the 13 successful command rows; the broad failure is excluded and disclosed here. Exact expanded arguments and outputs are reproducible from the named identities; command records and raw logs are in `.scratch/B23-coordination-kernel/checks.json` and `check-*.log`. Final smoke outputs are `final-status.json` and `final-freshness.json` there.

Unverified behavioral criteria: no live model reliability, weak-model gate, host claim/dispatch enforcement, remote tracker integration, command-execution attestation, or semantic freshness propagation was measured. The local Markdown/file-hash adapter deliberately reports unsupported identities and unbound records instead of inventing currentness. Canonical repository generated output remains untouched; successful scratch packaging and relocation fixtures verify this contribution's closure. Independent acceptance remains required; ticket stays `in_progress` / `needs-review`.

## Parent acceptance

2026-10-23: integrated source accepted after 152 suite tests, build/check, both validators and [independent review](../evidence/fifth-batch-review.md). Acceptance is the source contract and explicitly described local scripted exercises. It does not certify live agent/host enforcement, real PR/release actions, or production telemetry. No external operation was performed.
