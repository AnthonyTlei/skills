# Audit guide

Audit is report-first. Do not repair records or code unless the user separately asks.

## Mechanical pass

Run `check` to detect:

- malformed JSON frontmatter;
- schema or enum violations;
- duplicate or recycled IDs;
- undeclared domains, prefixes, actors, or surfaces;
- broken dependency and flow references;
- self-dependencies and dependency cycles;
- missing evidence files;
- active flows that use removed features;
- unsupported verification claims;
- missing or stale generated files.

## Semantic pass

Within the declared scope, compare the canonical map with current product docs, entry points, implementation, tests, flags, integrations, and relevant history. Look for:

- durable surfaces with no plausible mapped capability;
- mapped behavior whose entry point or implementation disappeared;
- deprecated or removed behavior that still appears active;
- implementation marked complete despite partial or conditional paths;
- verification stronger than the evidence supports;
- tests that no longer exercise the claimed boundary;
- specs or decisions that contradict current behavior;
- flow ordering or outcomes that no longer match the product;
- coverage claims unsupported by the inspected scope.

## Findings

For each finding, state:

1. severity and affected feature or flow IDs;
2. the map claim;
3. the contradictory or missing evidence;
4. whether intent is known;
5. the smallest safe reconciliation.

Do not treat code as automatically correct when it conflicts with a specification or decision. Record the conflict and ask which source represents intended behavior when the evidence cannot decide.

Likely unmapped behavior is an audit finding, not permission to create a canonical record. Propose the domain, capability, and evidence boundary before adding it.
