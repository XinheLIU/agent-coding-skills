# B5-diagnosis-stops: Add stop rules and an edit boundary to incident diagnosis

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/maintain/acs-diagnose-incident/SKILL.md`; new `references/` recipes
Effort: S

## Scope

The skill asks for three to five falsifiable hypotheses (line 37) but never says when to stop or how far edits may go.

Add:
- after three falsified hypotheses, stop and present options instead of a fourth guess;
- once a hypothesis forms, restrict edits to the narrowest directory;
- ask before a fix touches more than five files;
- tag debug logs (`[DEBUG-xxxx]`) so they can be found and removed;
- put runtime-debugger recipes (node inspect, python debugpy) in `references/`.

## Inputs

- Analysis: §8.8 G6, §10 B5.
- Sources: gstack `investigate:116-142, 186-194`; Pocock `diagnosing-bugs`; skills-manager presets `node-inspect-debugger`, `python-debugpy`.

## Verification

- The skill states the three-strike stop, the directory boundary, the five-file ask and the log tag as numbered rules.
- A simulated transcript with three falsified hypotheses ends in options, not a fourth probe.
- `references/` holds at least one runtime-debugger recipe.

## Blockers

none

## Coordination proposal

Only this skill and its references.

## Evidence

Implemented 2026-10-23. B1/B2/B14/B19 integrated baseline preserved; the only pre-existing source changed is this ticket's diagnosis skill. Its short catalog description and context declaration are unchanged. No evidence bindings were edited.

### Criterion / command / result / source identity

All commands ran from the B5 worktree. `S1`–`S4` below identify the exact validated bytes; full logs are in `.scratch/B5-diagnosis-stops/`.

| Criterion | Command | Actual result | Source identity |
| --- | --- | --- | --- |
| Four numbered rules; three-strike options; runtime recipes | `python3 -m unittest discover -s system/evals/tests -p test_diagnose_incident.py -v` | PASS, 4 tests; includes fourth-probe and missing-choice/options negative fixtures, plus relocated standalone package closure | S1–S4 |
| Catalog description, declarations, local links | `python3 system/evals/validate_suite.py` | PASS, 43 source skills | S1–S2 on integrated baseline |
| Builder-generated packages | `python3 scripts/build-plugins.py --output .scratch/B5-diagnosis-stops/plugins` | PASS, 10 packages including optional protocols package | S1–S2 on integrated baseline |
| Protocol registry and generated package closure | `python3 scripts/validate-protocols.py --plugins .scratch/B5-diagnosis-stops/plugins` | PASS | S1–S2 and isolated builder output |
| Existing catalog, questioning, inventory and package checks | `python3 -m unittest discover -s system/evals/tests -p 'test_*.py' -v` | PASS, 36 tests | S1–S4 on integrated baseline |
| Whitespace; no staged files | `git diff --check`; `git diff --cached --name-only` | PASS; empty index | Final worktree |

### Validated source hashes (SHA-256)

- S1: `system/skills-src/maintain/acs-diagnose-incident/SKILL.md` — `dd8f9389e9a07fc54809d73db7c69316977d6505e830ea4d52f11ab337ff0fd9`
- S2: `system/skills-src/maintain/acs-diagnose-incident/references/runtime-debuggers.md` — `0e1c637c27da599a9b25dbf7e97c79024b67a903b404ac39896307580c489fcb`
- S3: `system/evals/fixtures/acs-diagnose-incident-stops.json` — `6d39efed912b4895b2af43b7c3911451b5e157a12c9c28e830a02c8f84e8456c`
- S4: `system/evals/tests/test_diagnose_incident.py` — `ca7566148fcdba2268f5528f43ba90f0e0b8b30ece45886eaa52d2c8dbe166ec`

### Baseline and exact contribution

Baseline HEAD: `fbc81fd046ea0c2093e4516cc8dbdd289d473395` (HEAD alone does not describe the integrated uncommitted baseline).

Before editing, captured `.scratch/B5-diagnosis-stops/baseline.diff` (SHA-256 `b621bea7ff34ed74c3aa12c5fc08841696960a8d1b789c5612761b11bcc4dcc3`), `baseline.status`, and `baseline-hashes.json` (1,071 file hashes; SHA-256 `330002cbf3bd02b73b95d230b33c3cdf930b6ad58584dfbc552c581ef9cb8480`). Original bytes for the skill and this ticket are in `baseline-files/`. A baseline-relative contribution patch and final hash audit are retained alongside them.

Exact repository contribution: this ticket, S1 (modified), and S2–S4 (added). Builder output lives only in `.scratch/B5-diagnosis-stops/plugins`; no generated repository file was edited. Parent regeneration remains separate. No commits, installs, pushes, publication, or staged files.

### Read-only provenance

Read the local reference map and actual sources under `/Users/xhl/GitHub/skills/agent-coding-skills/references`. Source identities:

- `gstack/source/investigate/SKILL.md.tmpl` — SHA-256 `10b2abd3dcb3b46d3d7fb9fb328bc45a5874102b763d244d81a0b693c7416bb4`
- `matt-pocock/skills/engineering/diagnosing-bugs/SKILL.md` — SHA-256 `849198df88cdb65fd0d97236604c1fca7ff2f22d2f705f9724a800d0266b118d`
- `skills-manager-presets/software-build-delivery/node-inspect-debugger/SKILL.md` — SHA-256 `f2f72c0c9e67143effc8cb9871a242309813af72c61b8d62548ae275c86f2d08`
- `skills-manager-presets/software-build-delivery/python-debugpy/SKILL.md` — SHA-256 `ce7e38367ea54fb86e32d41be2fb3682482b7e3d748316cb666b3d4e3ca51a40`

Gstack is mapped to `35dd014`, Pocock to `49dd158`; both debugger presets declare version 1.0.0. The skill and recipe retain their respective provenance without copying upstream runtime infrastructure.

### Limitations

The simulated transcript is explicitly authored. Tests validate its stop shape and reject a fourth probe; they do not establish model compliance. No agent behavioral run or live Node/debugpy session was performed. The source rules for directory and file-count boundaries are structurally checked, not exercised against a real incident. Review remains pending.

## Parent acceptance

2026-10-23: canonical build and affected suite passed; independent review found no remaining issues. See [bounded model exercises and source review](../evidence/bounded-model-exercises.md). B2/B3 evidence is one actual bounded model turn each, not a reliability benchmark. B4 has real scripted red/green evidence; B5 requires an explicitly simulated transcript.
