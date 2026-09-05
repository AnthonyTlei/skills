---
name: feature-map
description: Map durable product capabilities, actors, flows, dependencies, implementation, and verification to repository evidence. Use when bootstrapping or maintaining a project feature map, explaining what a product does, scoping feature impact, reconciling a completed change, or auditing product-documentation drift. Do not use for source dependency graphs, exhaustive UI inventories, or behavior-preserving internal changes.
license: MIT
---

# Feature map

Maintain a project-owned map of durable product behavior and the evidence that supports it. Keep canonical records in the project repository. Treat generated views as disposable indexes, never as sources of truth.

Use the bundled CLI for parsing, validation, and rendering. Use repository inspection and engineering judgment for taxonomy, intent, scope, and drift findings.

## Guardrails

- Map capabilities users, operators, API clients, external systems, or background actors can meaningfully rely on.
- Do not inventory every button, component, endpoint, utility, internal event, infrastructure item, refactor, dependency update, or formatting change.
- Do not add feature IDs throughout source code or require one test per feature.
- Do not create a map update merely because a pull request exists.
- Never infer implementation, verification, runtime behavior, or product intent from file presence alone.
- Keep lifecycle, implementation, and verification as separate claims.
- Preserve stable IDs. Never renumber or recycle one. Retain removed features with `lifecycle: removed`.
- Keep uncertainty visible. Use `unknown`, `partial`, warnings, and audit findings instead of inventing completeness.
- Treat an explicit request to map the whole project as authorization for repository-wide discovery and map creation. State the scope and inspect it systematically; do not shrink that request to an arbitrary subsystem. For unspecified scope, start with the smallest coherent scope that answers the question.

Read [architecture](references/architecture.md) before initializing or changing the taxonomy of a map. Read [the schema](references/schema.md) whenever creating or changing canonical records.

## Choose the mode

Infer the smallest applicable mode from the request:

1. **Bootstrap:** create a new map from plans or a declared slice of an existing repository.
2. **Query:** answer a product, capability, flow, or impact question from an existing map and targeted evidence. This is read-only.
3. **Pre-implementation scope:** identify affected feature and flow IDs, dependencies, invariants, evidence gaps, and likely map updates before coding. This is read-only unless the user also asks to update the map.
4. **Reconcile:** inspect a completed change, update only affected canonical records, render, and validate.
5. **Audit:** report drift, contradictions, unsupported claims, or likely omissions before proposing edits. This is read-only unless the user also asks for repairs.
6. **Validate or render:** run deterministic tooling without changing canonical records.

If the request could mean either scoped discovery or a durable bootstrap, do scoped discovery and say that no canonical map was created. Creating a repository-wide map is a deliberate write operation.

## Locate the project map

Resolve the repository root first. The conventional layout is:

```text
FEATURE_MAP.md                     generated overview
docs/feature-map/
  README.md                        local scope and maintenance notes
  config.json                      declared scope, domains, actors, surfaces
  glossary.md                      optional project terms
  features/<domain>/<ID-slug>.md   canonical feature records
  flows/<FLOW-ID>.md               canonical flow records
  generated/                       derived views
```

If an existing repository has an equivalent documented convention, follow it only when the bundled CLI can address it safely. Otherwise use the conventional layout.

## Bootstrap

Read [the bootstrap guide](references/bootstrap-guide.md), then:

1. Establish the declared scope and honest coverage: `unknown`, `partial`, or `complete-for-declared-scope`.
2. Record discovery coverage in the map README using the bootstrap guide. Inspect governing docs and the smallest systematic set of product surfaces needed for that scope: routes or screens, APIs, auth boundaries, data workflows, jobs, webhooks, integrations, flags, tests, operator paths, and relevant history.
3. Define actors, domains with stable prefixes, capabilities, and major flows before enumerating features. Split records by independently meaningful outcomes or lifecycle, not by screens, files, or test cases.
4. Run `init` once. It refuses to overwrite an existing map.
5. Create only durable feature and flow records supported by plans or repository evidence.
6. Run `render`, then `check`.

For greenfield work, map agreed plans and specs while keeping implementation `absent` unless implementation evidence exists. For an existing codebase, do not claim complete coverage until the declared scope was systematically inspected.

Do not add the AGENTS guidance automatically. Use `--integrate-agents` only when the user explicitly asks for repository-agent integration.

## Query and scope

Load `config.json`, then only the canonical records and generated index needed for the question. Confirm important claims against live repository evidence when they may have drifted.

For change scoping, report:

- affected feature and flow IDs;
- upstream dependencies and downstream dependents;
- invariants or product decisions at risk;
- current implementation and verification evidence;
- records likely to need reconciliation after implementation.

Skip map work for behavior-preserving internal changes unless they invalidate a recorded reference or claim.

## Reconcile

Read [the maintenance policy](references/maintenance-policy.md). Inspect the completed diff and current behavior, then update only the affected records.

- Preserve IDs and taxonomy unless the product model itself changed.
- Remove stale evidence references; add new ones only after checking them.
- Raise implementation or verification status only to the strongest level actually demonstrated.
- Set `last_verified` only when verification really occurred.
- Update the canonical owner of each relationship: feature records own dependencies; flow records own ordered membership.
- Render and check after canonical edits.

Report changed feature and flow IDs plus any unresolved drift.

## Audit

Read [the audit guide](references/audit-guide.md). Run the mechanical validator first, then compare the declared map with current docs, entry points, implementation, tests, and history inside the declared scope.

Report findings before editing. Distinguish invalid structure from semantic drift. If code and documentation disagree, do not silently choose which one represents intent.

## CLI

Resolve the skill directory from the available-skills catalog or the path of this `SKILL.md`; do not assume a particular installation root. Use its bundled script:

```bash
FEATURE_MAP_SKILL="/absolute/path/to/feature-map"
python3 "$FEATURE_MAP_SKILL/scripts/feature_map.py" init --repo /absolute/project/path --project-name "Project" --scope "Declared product surface"
python3 "$FEATURE_MAP_SKILL/scripts/feature_map.py" validate --repo /absolute/project/path
python3 "$FEATURE_MAP_SKILL/scripts/feature_map.py" render --repo /absolute/project/path
python3 "$FEATURE_MAP_SKILL/scripts/feature_map.py" check --repo /absolute/project/path
```

The CLI uses only the Python standard library. It never imports or executes project code.

- `init` creates an empty scaffold and generated views. It refuses existing map paths.
- `validate` reads canonical records and reports errors and warnings without writing.
- `render` validates, then atomically replaces only `FEATURE_MAP.md` and `docs/feature-map/generated/*.md`.
- `check` validates and compares expected generated content without writing.

Warnings preserve honest incompleteness and normally exit successfully. Errors and stale generated output exit nonzero.

## Explicit invocations

```text
$feature-map bootstrap a partial map for the authentication and account-recovery surfaces.
$feature-map explain which capabilities depend on AUTH-003 and show the evidence.
$feature-map scope this checkout change before implementation.
$feature-map reconcile the completed diff with the project map.
$feature-map audit the declared payments scope for drift; report only.
```

## Completion contract

State:

- the mode and declared scope used;
- canonical feature and flow IDs created or changed;
- generated files updated;
- validation and freshness results;
- warnings, unverified claims, and coverage limits;
- whether AGENTS guidance was changed.

Never describe a partial map as a complete inventory. Validation checks structure and generated freshness; it does not establish semantic completeness, current runtime behavior, or successful product verification.
