# Canonical schema

Canonical feature and flow files are Markdown with a JSON object between opening and closing `---` lines. JSON is deliberate: the standard library parser gives exact line and column errors and avoids a runtime dependency.

## Configuration

`docs/feature-map/config.json`:

```json
{
  "schema_version": 1,
  "project": {
    "name": "Example",
    "summary": "What this product is for."
  },
  "scope": {
    "description": "The bounded product surface covered by this map.",
    "paths": ["src", "tests", "docs"],
    "coverage": "partial"
  },
  "domains": [
    {"id": "identity", "title": "Identity", "prefix": "AUTH"}
  ],
  "actors": [
    {"id": "customer", "title": "Customer", "type": "human"}
  ],
  "surfaces": ["web", "api", "worker"],
  "dependency_cycle_policy": "warning",
  "retired_ids": []
}
```

Domain IDs and actor IDs use lowercase letters, digits, and single hyphens. Domain prefixes use uppercase letters and digits, start with a letter, and remain unique. `retired_ids` is only for the exceptional case where a removed record cannot remain in the repository; a current feature may not reuse one.

Actor `type` is descriptive and extensible. Prefer `human`, `operator`, `api-client`, `external-system`, or `background`.

## Feature record

```markdown
---
{
  "schema_version": 1,
  "id": "AUTH-001",
  "title": "Sign in with a password",
  "domain": "identity",
  "capability": "Session access",
  "summary": "A registered customer can establish an authenticated session.",
  "actors": ["customer"],
  "surfaces": ["web", "api"],
  "lifecycle": "active",
  "implementation": "complete",
  "verification": "test-verified",
  "entry_points": ["/sign-in", "POST /api/sessions"],
  "depends_on": [],
  "code_refs": ["src/auth/session.ts#createSession"],
  "test_refs": ["tests/auth/session.test.ts#creates a session"],
  "spec_refs": ["docs/specs/authentication.md"],
  "decision_refs": ["docs/decisions/0003-session-cookies.md"],
  "last_verified": {
    "date": "2026-09-03",
    "methods": ["npm test -- session.test.ts"]
  }
}
---

## Behavior

Describe observable behavior, important boundaries, and failure behavior.

## Invariants

- State only constraints that the product or system must preserve.

## Notes

Record concise context that does not belong in metadata.
```

Feature IDs use `PREFIX-001` or a longer numeric suffix. The prefix must match the declared domain. IDs are stable, unique, and never recycled.

Required fields are `schema_version`, `id`, `title`, `domain`, `capability`, `summary`, `actors`, `surfaces`, `lifecycle`, `implementation`, `verification`, `entry_points`, `depends_on`, `code_refs`, `test_refs`, `spec_refs`, and `decision_refs`.

Allowed values:

- lifecycle: `proposed`, `active`, `deprecated`, `removed`
- implementation: `absent`, `partial`, `complete`, `unknown`
- verification: `unverified`, `code-traced`, `test-verified`, `runtime-verified`

Evidence requirements:

- `code-traced` requires at least one `code_ref`.
- `test-verified` requires at least one `test_ref`.
- Every verification level above `unverified` requires `last_verified.date` and at least one recorded method.
- `last_verified` must be absent when verification is `unverified`.

## Flow record

```markdown
---
{
  "schema_version": 1,
  "id": "FLOW-SIGN-IN",
  "title": "Customer signs in",
  "type": "user",
  "summary": "A returning customer establishes a session.",
  "primary_actor": "customer",
  "supporting_actors": [],
  "lifecycle": "active",
  "entry_points": ["/sign-in"],
  "steps": [
    {"feature": "AUTH-001", "outcome": "Credentials are accepted and a session begins."}
  ],
  "external_systems": []
}
---

## Narrative

Describe boundaries, alternate outcomes, and handoffs that the ordered list cannot express.
```

Flow IDs start with `FLOW-` and use stable uppercase words separated by hyphens. `type` is one of `user`, `operator`, or `system`. Required fields are `schema_version`, `id`, `title`, `type`, `summary`, `primary_actor`, `supporting_actors`, `lifecycle`, `entry_points`, `steps`, and `external_systems`.

Each step owns one canonical reference to a feature plus a concise observable outcome. Feature records do not store reverse flow membership.

## Reference rules

`code_refs`, `test_refs`, `spec_refs`, and `decision_refs` must be repository-relative files with optional `#symbol` fragments. Absolute paths, `..`, URLs, empty paths, and files outside the repository are invalid. The path before `#` must exist.

`entry_points` are labels rather than file references. They may contain routes, commands, API methods, job names, or integration events and are not checked for filesystem existence.
