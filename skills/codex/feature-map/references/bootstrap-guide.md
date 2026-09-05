# Bootstrap guide

## Start with a boundary

State the declared product scope before discovering records. Use the whole product when the user asks for all project features; otherwise choose a coherent scope. Whole-product scope still needs explicit inclusions and exclusions. Record the paths used for discovery, but do not confuse filesystem paths with product scope.

Use `unknown` coverage when discovery has barely begun. Use `partial` when the main shape is known but omissions remain. Use `complete-for-declared-scope` only after systematic inspection of every relevant surface inside the declared boundary.

## Greenfield projects

Begin from approved plans, specifications, architecture decisions, and prototypes. Map durable intended capabilities and major flows. Keep implementation `absent` unless implementation evidence exists. Keep verification `unverified` unless verification actually occurred.

Do not turn every requirement sentence into a feature. Group details under the durable capability they define.

## Existing repositories

Inspect the applicable subset of:

- product docs, specifications, ADRs, and terminology;
- routes, screens, navigation, and public commands;
- API boundaries, auth and authorization paths;
- persistent data workflows and state transitions;
- workers, scheduled jobs, events, and webhooks;
- third-party integrations and feature flags;
- admin and operator paths;
- tests and runtime evidence;
- Git history when intent is otherwise unclear.

Trace behavior through real implementations. Names, stubs, comments, and file existence are leads, not proof.

## Build the taxonomy first

Define actors and domains before assigning IDs. A domain is a stable product area, not a source directory. A capability is a useful grouping inside a domain. A feature is the durable behavior itself.

Choose short prefixes that remain understandable as the project grows. Never derive IDs from current file ordering. Leave gaps when useful; do not renumber after deletion or reorganization.

Define major user, operator, and system flows after the taxonomy. Flows may cross domains. Avoid creating a flow for a one-step capability unless the process itself matters.

## Keep the first map small

The first useful map needs:

- an honest scope and coverage claim;
- the actors and domains needed by that scope;
- durable capabilities with evidence boundaries;
- major flows that reveal cross-domain behavior;
- visible omissions and uncertainty.

It does not need a record for every implementation detail. A small repository may need only a few features and one flow.

## Finish the bootstrap

Run `render` and `check`. Review the generated domain, actor, flow, maturity, dependency, and verification views for taxonomy mistakes. Report what was inspected, what remains outside scope, and why the coverage value is honest.

## Record the discovery basis

Maintain a short table in `docs/feature-map/README.md` with columns for surface or domain, inspected entry points, mapped IDs, and omissions or uncertainty. Record the Git revision or inspection date above it. Include relevant background and operator behavior, not only visible screens. An explicitly excluded surface belongs in the scope notes; an in-scope surface not yet inspected is an omission.

Before claiming `complete-for-declared-scope`, reconcile each relevant surface to mapped outcomes or an explained non-feature. Do not use passing validation or feature count as completeness evidence. This ledger is an inspection record, not an instruction to create a test for each row.
