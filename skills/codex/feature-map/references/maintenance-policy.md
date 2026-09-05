# Maintenance policy

## When to update

Update the feature map when a change alters a durable capability, actor outcome, entry point, major flow, dependency, lifecycle state, implementation claim, verification claim, or evidence reference.

Do not update it for behavior-preserving refactors, formatting, dependency bumps, internal utility changes, or implementation churn that leaves every mapped claim true and every reference valid.

## Before implementation

Use the map to identify affected IDs, upstream dependencies, downstream dependents, flows, invariants, and verification gaps. This scoping step does not change canonical records unless the product plan itself changes.

## After implementation

Reconcile from the completed diff and real verification results:

1. read the affected canonical records;
2. inspect the final implementation and tests;
3. update only claims changed by the work;
4. preserve IDs;
5. set `last_verified` only for verification performed;
6. render and check;
7. report changed IDs and remaining uncertainty.

Do not promote `implementation` to `complete` because code was added. Do not promote `verification` because tests exist. Confirm the implemented paths and the actual verification result.

## Relationship ownership

- Feature records own `depends_on`.
- Flow records own ordered feature steps.
- Generated views own reverse dependency, actor, domain, maturity, and flow indexes.

Do not manually store reverse edges such as `depended_on_by` or `participates_in`.

## Removal and renaming

When a capability is removed, retain its record and set lifecycle to `removed`. Remove it from active flows. Do not reuse its ID.

If terminology changes but the durable capability remains the same, keep the ID and update its title, summary, and evidence. If one capability genuinely splits into several, retain the original as deprecated or removed and create new IDs with clear notes.

## AGENTS guidance

The asset `assets/AGENTS-feature-map-snippet.md` is optional. Add it only at the user's explicit request. Avoid duplicate `## Feature map` headings, preserve repository-specific instructions, and never overwrite an existing AGENTS file.

## Coverage and evidence drift

Update the README discovery ledger when scope, inspected surfaces, or known omissions change. Lower coverage to `partial` when newly added in-scope behavior has not been mapped. Keep old verification dates as historical evidence; if a changed contract invalidates that evidence, lower the claim and explain the gap in the record. Rendering and schema validation never refresh product verification.
