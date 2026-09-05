---
name: right-size-tests
description: "Decide whether a change needs new tests and choose the smallest sufficient verification. Use when planning test scope or stopping criteria, especially to avoid redundant tests and repeated suites."
license: MIT
---

# Right-size tests

Choose evidence for the actual change risk. Adding no tests is a valid outcome. This skill is a decision aid, not an extra mandatory test phase for every edit.

## Decide before adding

Follow applicable repository checks and explicit user requirements. Inspect nearby coverage. Before writing a test, identify the meaningful regression it would catch, whether existing evidence already catches it, and whether the behavior is stable enough to maintain as a contract.

Usually add no permanent test for prose, formatting, static content, trivial wiring enforced by types, temporary layouts, behavior-preserving refactors already covered, or assertions that merely repeat the implementation. Use inspection, a targeted build, or a manual check only when that adds useful evidence. Do not invent a check just to fill a report.

Add or extend a test when it protects a meaningful uncovered risk: nontrivial logic, a reproduced bug, authorization, privacy, data integrity, persistence, compatibility, or a critical boundary. High-consequence stable behavior still matters in a prototype. Feature count and changed line count are not test quotas.

## Choose one sufficient seam

Prefer an existing test that can express the contract. Choose the cheapest reliable boundary that would actually reveal the failure:

- Types, schemas, lint, or compilation for constraints they enforce.
- A focused unit test for logic or a state transition.
- A narrow integration test when the failure lives between components.
- A representative runtime or end-to-end check only when lower layers cannot prove the required claim.
- Manual inspection for unsettled visual design or interaction feel.

Add a second seam only when it covers a distinct material failure. Do not mirror the same assertions across unit, integration, and browser suites. Mocks prove behavior against the mock, not the provider or deployed system.

Use test-first work when a stable contract or reproducible regression makes it useful. Do not force TDD onto exploratory UI or scaffolding. Avoid new runners, elaborate fixtures, broad snapshots, combinatorial edge-case inventories, and test-only production abstractions for a bounded change.

## Run and stop

Run the smallest affected check. Broaden only for a concrete cross-component risk, an established normal project check, or an explicit requirement. A passing targeted check does not automatically trigger package and full-suite runs.

Once sufficient targeted evidence and required checks pass, stop. Do not rerun unchanged passing checks for reassurance, after documentation-only follow-ups, or through multiple workers. Repeat only when relevant inputs changed or a bounded repeat is itself the experiment, such as investigating a race.

For a failure, inspect it before rerunning. Retry only after a relevant change or for a stated hypothesis about nondeterminism. Two identical failures without new evidence end blind retries; pursue a specific diagnostic or report the blocker. Do not increase timeouts by habit.

Never weaken assertions to get green results. Do not delete existing tests merely because this skill favors restraint; suite cleanup must be in scope and the lost protection understood.

## Report only what matters

Briefly state checks performed, results, and material unverified boundaries. Mention why no test was added when that decision is useful to the user. Do not create a test plan artifact, coverage target, or lengthy matrix for routine work.

[Research notes](references/research.md) retain the background for this policy; read them only when the rationale is needed.
