# Repository instructions

This repository is the source of truth for the maintained skills listed in `skills.toml`.

- Keep installable packages under `skills/<harness>/<skill-name>/`.
- Do not assume instructions are portable across harnesses. Put a skill in `shared` only after verifying that its syntax, tools, paths, and invocation behavior work in every named harness.
- Edit repository files, not installed symlink paths.
- Preserve each skill's existing intent and authorization boundaries.
- Treat Linear Free as the compatibility target for every Linear-capable skill. Never require an upgrade, trial, paid add-on, AI credits, or a paid-only feature; use a local workflow when Free-plan availability is unclear or insufficient.
- For a skill change, update its semantic version in `skills.toml` and add an entry to `CHANGELOG.md`.
- Run `make validate` before declaring a change complete.
- Preserve `LICENSE`, `THIRD_PARTY_NOTICES.md`, package-level license files, and the source mapping in `docs/PROVENANCE.md`.
- Before a public release, validate the catalog and scan the tracked tree and Git history for credentials or unwanted personal data.
- Never overwrite unmanaged files or directories during installation.
