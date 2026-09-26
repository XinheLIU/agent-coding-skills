# Ship independent plugins that materialize their own resource closure

Last updated: 2026-09-26

Change: phase plugin refactoring
Status: accepted
Basis: plugins created in `17c3eb2` (tagged `v0.4.0`); closure model corrected in `eb84af4`
affects: `plugins/**`, `scripts/build-plugins.py`, install topology, `catalog/skill-set.json`

The suite shipped as one monolithic plugin, so installing any skill installed all 44. Skills are now grouped into independently installable phase plugins, each built by `scripts/build-plugins.py` with every shared protocol, reference, and workflow it transitively needs copied into its own tree.

## Considered options

The refactoring plan specified a dependency model in which every phase plugin **required** `acs-context`, which would own the shared protocols. That shipped first and was reversed in `eb84af4`: it was not a real dependency. A plan or design plugin does not call into context skills at runtime — it reads contracts, which are documents. Modelling a document read as a package dependency meant a user installing one plan skill had to install the context suite too, and it made the install graph a lie about what actually happens at runtime.

Materializing the closure instead means each plugin carries dereferenced copies of the contracts it cites. The cost is real and accepted: the same protocol file exists in up to eleven copies across `plugins/`, and 714 tracked documents hold only 325 distinct contents. That redundancy buys plugins that install and work with every other plugin absent, which is the property the facade pattern in this workspace depends on.

## Consequences

`plugins/` is generated build output. Never hand-edit it; run `scripts/build-plugins.py`, which is byte-deterministic, and `scripts/validate-protocols.py` checks that no package retains a symlink or a reference escaping its boundary.

Two plugins may materialize the same skill — `acs-craft` and `acs-context` both carry the context skills — because plugin membership is a packaging choice, not an ownership claim. `system/skills-src/` remains the single source of truth for skill content.
