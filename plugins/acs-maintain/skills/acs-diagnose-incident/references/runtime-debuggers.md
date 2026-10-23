# Runtime debugger recipes

Last updated: 2026-10-23

Use a debugger to test one prediction from the diagnosis loop. Record the command, breakpoint location, observed value or stack, and whether it falsifies the hypothesis in `diagnosis.md`. These recipes do not bypass the three-strike stop, directory boundary, or five-file ask. Replace example paths and line numbers with the minimized reproduction.

## Node.js: inspect without source edits

Start the reproduction in an interactive terminal:

```bash
node inspect path/to/repro.js
```

At the `debug>` prompt, set a breakpoint before the suspected operation, continue, and inspect only the state needed for the prediction:

```text
sb('path/to/affected.js', 42)
cont
bt
exec suspectedValue
```

Confirm the breakpoint hit the expected file and frame before treating a value as evidence. For compiled TypeScript, use the emitted JavaScript path and line; the CLI does not map source breakpoints automatically. Keep the inspector on its default loopback interface. End the reproduction process you started with `kill`, then leave the debugger with `.exit`; do not leave a paused target behind. Rerun the ordinary reproduction command after disconnecting to check whether debugger timing affected the symptom.

## Python: debugpy with an existing client

Use the project's isolated Python environment with `debugpy` already available and an existing DAP-capable debugger client. If unavailable, record the limitation and use `python -m pdb path/to/repro.py` for interactive inspection; this recipe does not require installing a dependency.

Launch the minimized reproduction without editing source:

```bash
python -m debugpy --listen 127.0.0.1:5678 --wait-for-client path/to/repro.py
```

Attach the existing client to `127.0.0.1:5678`, set a breakpoint at the suspected operation, then continue. `--wait-for-client` deliberately holds startup until attachment; a listening port alone is not evidence that the breakpoint hit. Check the source path and stack frame, inspect the local value that distinguishes the prediction, and record the observation. If port 5678 is occupied, select another free loopback port and use it in both launch and client settings.

Disconnect the client and stop only the reproduction process you launched. Remove any temporary breakpoints or instrumentation added during the investigation and rerun the ordinary reproduction command. Prefer this launch method over injecting into an unrelated running process.

## Provenance

These short recipes adapt evidence-gathering methods from the read-only skills-manager `software-build-delivery` presets `node-inspect-debugger` and `python-debugpy`, each declaring version 1.0.0, author Hermes Agent, and MIT licensing. They omit preset-specific paths, installation steps, and process-injection scripts. The B5 ticket records the exact study-copy hashes; no preset package is a runtime dependency.
