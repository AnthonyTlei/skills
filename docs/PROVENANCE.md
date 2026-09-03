# Provenance

The initial Codex catalog was imported on 2026-09-03 from Anthony's local Codex installation. Anthony reports that the skills were ported from Cursor versions on 2026-09-02 and were influenced by pstack skills and work by Matt Pocock.

The exact upstream repositories, files, revisions, and licenses have not yet been recorded. This note does not claim that every skill contains copied upstream text.

## `to-spec`

- Upstream: `https://github.com/mattpocock/skills/tree/main/skills/engineering/to-spec`
- Retrieved: 2026-09-03
- Upstream revision: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- Upstream `SKILL.md` SHA-256: `43ad9cf318e5e7d3d1fa360253a37021796dc87a0c2e595ad262661a10f85088`
- Upstream `agents/openai.yaml` SHA-256: `1c5b4d1e3d8e52287ef19cc2742fdbbfae1914ac75d33af3e4c8174f08cc55bb`
- License: MIT, preserved in `skills/codex/to-spec/LICENSE.txt`

The Codex adaptation removes the unsupported frontmatter field and setup-skill dependency. It adds repository-first publishing, optional Linear project documents, explicit approval, evidence boundaries, duplicate protection, and read-back verification.

Before public distribution:

1. Identify the upstream source for each affected skill.
2. Record the source URL and revision.
3. Compare the retained text and supporting files.
4. Preserve required notices and choose a compatible repository license.
