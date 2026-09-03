# Agent skills

A maintained collection of agent skills for software work. The repository currently ships Codex packages and keeps each harness separate so future Claude or Cursor ports can use their own metadata, tools, and invocation rules.

The catalog combines original packages with opinionated adaptations for Codex and GPT models. The adaptations are not official releases from the upstream authors.

## Current skills

| Skill | Purpose |
| --- | --- |
| `blast-radius` | Trace indirect change risks and verify the assumptions a change depends on. |
| `bro` | Restate the previous answer in shorter, plainer language. |
| `delegate-work` | Decide when to delegate, choose worker model and effort, and keep parallel work safe. |
| `feature-map` | Maintain a project-owned map of durable capabilities, flows, dependencies, and verification evidence. |
| `how` | Explain a codebase subsystem and critique its architecture when requested. |
| `right-size-tests` | Choose the smallest durable test coverage that proves the actual change risk. |
| `teach` | Build a guided technical explanation from current behavior and repository history. |
| `technical-writing` | Write and revise developer documentation in clear technical English. |
| `to-spec` | Turn discussion and repository evidence into a reviewed local or Linear specification. |
| `to-tickets` | Split a plan into dependency-aware local or Linear implementation tickets. |
| `unslop` | Remove common AI writing habits while preserving meaning and voice. |
| `why` | Investigate design intent using Git history and repository evidence. |

Local Markdown is the default for `to-spec` and `to-tickets`. Their optional Linear path targets the Free plan and only uses an existing project that matches the current codebase. See [the Linear Free policy](docs/LINEAR_FREE.md).

## Repository layout

```text
skills/
  codex/<skill>/       Installable Codex skill packages
scripts/skills.py      Validation, installation, and status checks
skills.toml            Skill catalog and per-skill versions
docs/                  Architecture, compatibility, and provenance notes
CHANGELOG.md            User-visible catalog changes
```

## Install for Codex

Clone the repository, validate it, and install the catalog as symbolic links:

```bash
git clone https://github.com/AnthonyTlei/skills.git
cd skills
make validate
make install
```

The installer refuses to replace a real file or directory. Set `CODEX_SKILLS_DIR`, set `CODEX_HOME`, or pass an explicit target when Codex uses a non-default skill directory:

```bash
python3 scripts/skills.py install codex --target /path/to/skills
```

Check the managed links at any time:

```bash
make status
```

Edits and Git pulls become visible through existing links without copying files. Run the installer again only after adding or renaming a skill. Restart Codex if it does not detect a change.

The default target follows `CODEX_SKILLS_DIR`, then `$CODEX_HOME/skills`. Without either variable, the installer preserves an existing managed installation under `~/.codex/skills`; otherwise it uses `~/.agents/skills`.

## Maintain the catalog

For every skill change:

1. Edit the package under `skills/<harness>/<skill>/`.
2. Update its semantic version in `skills.toml`.
3. Add the user-visible change to `CHANGELOG.md`.
4. Run `make validate`.
5. Commit the package, manifest, and changelog together.

Repository tags version the catalog as a whole. Individual versions in `skills.toml` track each package.

## Credits

Seven skills began as ports of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by [Lauren Tan](https://github.com/poteto): `blast-radius`, `bro`, `how`, `teach`, `technical-writing`, `unslop`, and `why`.

`to-spec` and `to-tickets` began as ports of [Matt Pocock's skills](https://github.com/mattpocock/skills).

`delegate-work`, `feature-map`, and `right-size-tests` are original repository work based on design briefs supplied by the maintainer.

The ported packages have since been adapted for Codex, GPT-only delegation, the tools available in Codex, and this repository's publication and safety rules. [Provenance](docs/PROVENANCE.md) records the upstream revisions and file hashes. [Third-party notices](THIRD_PARTY_NOTICES.md) preserve both MIT notices.

## License

Original repository work and adaptations are released under the [MIT License](LICENSE). Upstream-derived portions remain covered by their original MIT notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and each derived skill package.
