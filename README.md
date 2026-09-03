# Anthony's agent skills

This repository is the source of truth for Anthony's maintained agent skills. Skills stay separated by harness because instructions, tools, metadata, and invocation rules differ between Codex, Claude, and Cursor.

The current catalog contains Codex skills only. Add `skills/claude/`, `skills/cursor/`, or `skills/shared/` when real skills need those locations. Do not add empty placeholder trees.

## Repository layout

```text
skills/
  codex/<skill>/       Installable Codex skill packages
scripts/skills.py      Validation, installation, and status checks
skills.toml            Skill catalog and per-skill versions
docs/                  Architecture and provenance notes
CHANGELOG.md            User-visible changes
```

Each installable directory contains `SKILL.md` and any references, scripts, assets, or harness metadata that belong to that skill.

## Use the skills with Codex

Validate the repository:

```bash
make validate
```

Install the Codex catalog as per-skill symbolic links:

```bash
make install
```

The installer never overwrites a real file or directory. It only creates missing links or updates existing links. Set `CODEX_SKILLS_DIR` or pass `--target` when Codex uses a non-default location:

```bash
python3 scripts/skills.py install codex --target /path/to/skills
```

Check whether every managed skill points to this checkout:

```bash
make status
```

Once linked, edits and Git pulls are visible to Codex without copying files. Restart Codex only when it does not detect a change.

The default target follows `CODEX_SKILLS_DIR`, then `$CODEX_HOME/skills`. Without either variable, it preserves an existing managed installation under `~/.codex/skills`; otherwise it uses `~/.agents/skills`.

## Maintain the catalog

For every skill change:

1. Edit the package under `skills/<harness>/<skill>/`.
2. Update its version in `skills.toml` using semantic versioning.
3. Add a concise entry under `Unreleased` in `CHANGELOG.md`.
4. Run `make validate`.
5. Commit the skill, manifest, and changelog together.

Use patch versions for compatible instruction fixes, minor versions for new behavior, and major versions when invocation or workflow behavior changes incompatibly.

Repository tags version the catalog as a whole. Skill versions in `skills.toml` record the version of each package.

Linear-capable skills target the Free plan and must fall back to local artifacts rather than requiring a trial, upgrade, paid add-on, or AI credits. See [the Linear Free policy](docs/LINEAR_FREE.md).

## Distribution boundary

This repository currently has no top-level license because not every upstream influence has been traced. Individual skill packages may carry their own license. Treat the rest as private and do not publish or redistribute it until the remaining sources and licenses have been recorded. See [the provenance notes](docs/PROVENANCE.md).
