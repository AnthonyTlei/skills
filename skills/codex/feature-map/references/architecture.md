# Architecture

## Ownership

Each product repository owns its feature map. This skill supplies a protocol, templates, and deterministic tooling; it is not a central database. A repository checkout must remain understandable without a service, plugin, graph database, or network connection.

Canonical truth lives only in:

- `docs/feature-map/config.json`
- `docs/feature-map/features/**/*.md`
- `docs/feature-map/flows/**/*.md`
- optional explanatory prose in `docs/feature-map/README.md` and `glossary.md`

`FEATURE_MAP.md` and `docs/feature-map/generated/*.md` are derived. Never edit them to record a product decision.

## Model

The hierarchy is:

```text
domain -> capability -> feature
                         |
                         +-> dependencies
                         +-> evidence references

flow -> ordered feature steps
```

A feature is a durable capability with an actor-observable or system-observable outcome. A flow is an ordered user, operator, or system process. Features own dependency edges. Flows own ordered feature membership. Reverse relationships are generated.

Actors include humans, administrators, operators, API clients, external systems, and background actors. Surfaces identify where a capability is entered or delivered, such as web, mobile, desktop, API, CLI, admin, webhook, worker, scheduled job, or integration.

## Status dimensions

Never collapse these into one status:

- lifecycle: whether the product still intends the capability;
- implementation: how much implementation evidence exists;
- verification: what kind of verification actually occurred.

A feature may be active, completely implemented, and still unverified. A proposed feature may have no code. A removed feature remains in the map so its ID cannot be recycled.

## Scope and coverage

The configuration declares a bounded scope and one coverage value:

- `unknown`: discovery has not established how much of the declared scope is mapped;
- `partial`: known omissions remain;
- `complete-for-declared-scope`: the declared scope was systematically inspected and no known durable capabilities remain unmapped.

Coverage never applies beyond the declared scope. A complete map of one subsystem is not a complete product map.

## Evidence

Evidence references use repository-relative paths with an optional `#symbol` fragment. They do not use line numbers, which decay too quickly. The validator checks the path portion only; the agent must inspect whether the symbol and claimed behavior are still accurate.

Project history may explain intent, but the map should link durable decisions or specifications rather than ephemeral investigation notes when possible.

## Determinism and portability

The bundled CLI uses only Python's standard library, sorts every discovery and rendering operation, includes no timestamps, writes atomically, and never imports project code. Repeated rendering over unchanged canonical inputs must produce byte-identical output.

## Record boundaries and context cost

Use one record for a durable outcome with a coherent actor, contract, and lifecycle. Keep variations, UI states, and failure cases in that record unless they are independently meaningful capabilities. Several entry points may implement one feature. A shared infrastructure dependency is not itself a product feature unless an actor can rely on its outcome.

Keep schema version 1 and the existing canonical files. A domain is a taxonomy entry, a capability is a grouping, and a feature owns the outcome and dependency edges. Do not introduce parallel registries, copied reverse edges, per-file feature annotations, or a service to query the map.

The map README holds a compact discovery ledger: product surface or domain, inspected entry points, mapped IDs, known omissions, and the inspection revision or date. This records the basis for coverage without duplicating feature records. It is human-reviewed evidence, not a new validator-enforced schema.

## Queries and freshness

Start with the generated overview and relevant index, then read the canonical records needed for the question. Follow dependency edges only as far as the question requires. Expand discovery for uncovered surfaces instead of reading every record by default.

Coverage is a claim about the inspected revision and declared scope, not a permanent property of the product. If changes introduce an uninspected surface, lower coverage to `partial` until reconciliation. Preserve historical verification dates; do not refresh them merely because a path exists or rendering succeeds. Record changed assumptions or environments in the affected record's prose and lower the verification claim when the old evidence no longer supports it.
