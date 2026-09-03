# Provenance

This catalog contains Codex adaptations from two MIT-licensed upstream sources. Anthony reports that the initial ports were made from Cursor-oriented versions on 2026-09-02. The files were compared with the pinned public revisions below on 2026-09-03.

The adaptations do not imply endorsement by either upstream author.

## pstack

- Project: [pstack in `cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack)
- Author: [Lauren Tan, `poteto`](https://github.com/poteto)
- Compared revision: [`23a56e2dac2efd54788056db8eced26e371d7b5e`](https://github.com/cursor/plugins/commit/23a56e2dac2efd54788056db8eced26e371d7b5e)
- License: MIT, copyright 2026 Lauren Tan
- License notice: preserved in `THIRD_PARTY_NOTICES.md` and each derived package

| Local skill | Upstream file | Upstream `SKILL.md` SHA-256 |
| --- | --- | --- |
| `blast-radius` | [`pstack/skills/blast-radius/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/blast-radius/SKILL.md) | `b060df3ca85803eabbce9fab53f5cc024ca8d784bdde5513c1c1a784947523f8` |
| `bro` | [`pstack/skills/bro/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/bro/SKILL.md) | `aa329d0ceeeecb6822a7174ad76bb07a7826a3c52ceb6a588dec4138815084bb` |
| `how` | [`pstack/skills/how/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/how/SKILL.md) | `3a554ff564d66a4200a07e20164558e820ea7a9795beb98a4a06546146c98f5f` |
| `teach` | [`pstack/skills/teach/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/teach/SKILL.md) | `0a5987b0588dc56e14bfd84d0300e2ab405abc7c5c2aa81e0d3d7c6b243db7a7` |
| `technical-writing` | [`pstack/skills/technical-writing/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/technical-writing/SKILL.md) | `bd0cb21034f4fe6695cfdf8cd3561026eec943f0bb6e9300bc78a2b3340865a7` |
| `unslop` | [`pstack/skills/unslop/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/unslop/SKILL.md) | `2789ab80477b7e382292e4d7acca1057784df19713fffb74622ff0f83b2f3733` |
| `why` | [`pstack/skills/why/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/why/SKILL.md) | `a9423bb7bab7c3280d17478ebe97bb283ea6ed12d9dcae590fc2f81f41660990` |

These ports replace Cursor-specific agents, model names, setup dependencies, and evidence tools with Codex collaboration tools and GPT models. They also add explicit authorization boundaries and checks against the current repository.

## Matt Pocock's skills

- Project: [mattpocock/skills](https://github.com/mattpocock/skills)
- Author: [Matt Pocock](https://github.com/mattpocock)
- Port revision: [`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`](https://github.com/mattpocock/skills/commit/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76)
- License: MIT, copyright 2026 Matt Pocock
- License notice: preserved in `THIRD_PARTY_NOTICES.md` and each derived package

| Local skill | Upstream file | Upstream SHA-256 |
| --- | --- | --- |
| `to-spec` | [`skills/engineering/to-spec/SKILL.md`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/engineering/to-spec/SKILL.md) | `43ad9cf318e5e7d3d1fa360253a37021796dc87a0c2e595ad262661a10f85088` |
| `to-spec` metadata | [`skills/engineering/to-spec/agents/openai.yaml`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/engineering/to-spec/agents/openai.yaml) | `1c5b4d1e3d8e52287ef19cc2742fdbbfae1914ac75d33af3e4c8174f08cc55bb` |
| `to-tickets` | [`skills/engineering/to-tickets/SKILL.md`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/engineering/to-tickets/SKILL.md) | `5c9fba69845c2519b9b35b9af42ae5142c21f8ca15ac2123dc2722002c8058ae` |
| `to-tickets` metadata | [`skills/engineering/to-tickets/agents/openai.yaml`](https://github.com/mattpocock/skills/blob/6654f6b60cd9d5be8b54c6fafe44346dabeb3b76/skills/engineering/to-tickets/agents/openai.yaml) | `21bc6215fffcd7614e9f772bb1760e87cc5fc7dcc707e7d282bc9414267a6090` |

The Codex adaptations remove the upstream setup-skill dependency and make repository-local publication the default. Linear remains optional only for an existing matched project, with review, duplicate protection, read-back verification, and Linear Free compatibility.

## License boundary

Both upstream sources use the MIT License. The root MIT license covers Anthony's original repository work and adaptations. Upstream-derived portions keep their original copyright and license notices in `THIRD_PARTY_NOTICES.md` and their package-level `LICENSE.txt` files.

When adding another third-party skill, record its source, author, pinned revision, relevant file hashes, license, retained notices, and material adaptation before publishing the change.
