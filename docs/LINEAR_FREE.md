# Linear Free compatibility

Linear Free is the compatibility target for this repository. A skill may use Linear only when its workflow fits the user's current Free workspace. It must never require or initiate a trial, upgrade, paid add-on, or AI-credit purchase.

## Current verified boundary

Checked against Linear's official pricing and documentation on 2026-09-03:

- Free includes up to 250 issues and 2 teams.
- The pricing page lists issues and projects among core capabilities.
- Linear documents can belong to projects, and projects can contain optional documents. The public pricing table does not separately identify document availability by plan, so an exposed document tool is not enough to prove Free entitlement.
- Optional AI features can require purchased AI credits.
- Business and Enterprise features are outside this repository's compatibility target.

Plan limits can change. Treat this list as a maintenance snapshot, not a permanent entitlement map.

## Skill rules

Every Linear-capable skill must:

1. Keep a complete local workflow as the default or safe fallback.
2. Recheck current official plan documentation before relying on Linear when plan availability could have changed.
3. Resolve the target workspace, team, project, and capability with read-only calls before writing.
4. Use only the minimum core Linear objects needed by the workflow.
5. Disclose relevant limits or unresolved capacity before the publication approval gate.
6. Stop on plan, quota, entitlement, or permission errors. Never work around them with a paid feature.
7. Obtain renewed approval before switching an approved publication from Linear to Local or vice versa.

For ticket publication, the approved batch counts against the Free issue limit. If remaining capacity is exposed through read-only tooling, verify that the whole batch fits. Otherwise disclose the uncertainty and stop cleanly if Linear rejects a write.

For specification publication, use only an ordinary document in an existing matched project. If document creation is unavailable or Free eligibility is unclear, publish locally after the normal review gate.

## Features outside the boundary

Do not build skill behavior around paid-plan or separately metered capabilities, including private teams, guest accounts, Triage Intelligence, Loops, Code Intelligence, Insights, Asks, issue SLAs, enterprise administration, or AI-credit-dependent workflows.

Avoid optional extras that the workflow does not need, even when they happen to be available. In particular, these skills do not create workspace configuration, upload attachments, invoke Linear Agent, or create Linear projects.

## Sources

- [Linear pricing](https://linear.app/pricing)
- [Billing and plans](https://linear.app/docs/billing-and-plans)
- [Documents](https://linear.app/docs/documents)
- [Projects](https://linear.app/docs/projects)
- [Issue relations](https://linear.app/docs/issue-relations)
