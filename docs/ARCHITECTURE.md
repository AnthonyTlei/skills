# Repository architecture

## Decision

Organize installable skills by harness:

```text
skills/<harness>/<skill-name>/
```

This keeps each package directly installable while allowing different harnesses to use different metadata, tools, paths, and instructions.

Use `skills/shared/<skill-name>/` only for a package verified unchanged across every harness that consumes it. Similar names or common ancestry do not make two skills portable.

## Source and installation

Repository directories are canonical. Harness skill directories contain per-skill symbolic links back to this checkout. The installer manages only skills declared in `skills.toml` and refuses to replace non-link paths.

This arrangement gives existing edits and Git pulls immediate effect. A newly added or renamed skill needs one installer run so the harness receives its link.

## Versions

Each skill has its own semantic version in `skills.toml`. A version changes when that package changes.

Git tags version the repository catalog. A catalog release may contain unchanged skills with older individual versions.

Do not add unsupported version fields to `SKILL.md` frontmatter. Harness validators own that schema.

## Adding another harness

Before adding Claude, Cursor, or another harness:

1. Verify its current skill specification and discovery directories.
2. Add its installable packages under `skills/<harness>/`.
3. Add manifest entries and target resolution to `scripts/skills.py`.
4. Add harness-native validation when available.
5. Test discovery and one realistic invocation in that harness.

Keep ports separate until identical behavior has been observed. Share references or scripts only when the package remains self-contained after installation or distribution.

## Retired packages

`archive/codex/` preserves retired package sources and license notices outside the installable catalog. It is not a skill discovery directory. Removal from `skills.toml` does not prune an existing installation: inspect each retired link and unlink it only if it resolves to that repository package. Never remove a same-named unmanaged file, directory, or unrelated symlink.

## Instruction scope

Active skills describe task-specific outcomes, evidence boundaries, and stopping conditions. They do not duplicate runtime model catalogs, worker counts, or generic writing rules. Explanation and review skills preserve their existing explicit invocation settings; `feature-map` and `right-size-tests` remain available for automatic selection.
