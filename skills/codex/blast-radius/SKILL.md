---
name: blast-radius
description: "Review indirect effects of a specified code change across consumers, stored data, lifecycle, and compatibility contracts. Use for a requested impact review or a risky diff with unclear downstream consequences."
license: MIT
---

# Blast radius

Find credible effects outside the edited lines. Default to a read-only review; this skill does not authorize fixes, dependency installation, temporary harnesses, or external changes.

## Establish the change

Resolve the repository, baseline, and exact diff or commit range. Keep staged, unstaged, and committed changes distinct unless the requested scope includes them together. Read complete changed functions and the surrounding contracts.

Trace relevant consumers and shared contracts: API and serialized data, stored state and migrations, configuration-driven dispatch, older clients, retries, cancellation, transactions, and partial failure. Follow only boundaries the change can plausibly affect. Read pinned dependency source when a library behavior is material. Search absence is evidence only for the searched scope.

Use current runtime delegation rules; this skill does not request a worker batch. `how` and `why` may help with difficult mechanics or history but are not required dependencies.

## Assess the evidence

Identify the facts the change's safety actually depends on. For each consequential claim, distinguish source-backed reasoning, executed checks, observed application behavior, and unresolved assumptions. Static evidence can be sufficient for a static claim; do not require executable proof by rule or imply runtime verification from source inspection.

Retain a risk only when a concrete consumer or invariant and a plausible failure path support it. Separate likelihood from impact. Do not invent hypothetical consumers or expand the review to unrelated hardening.

## Verify proportionately

Use existing checks only when their side effects fit the authorized scope. A strictly read-only review excludes commands that write caches, build products, snapshots, data, or external state. Do useful source analysis first and name any material execution gap.

If executable verification or disposable local writes are already authorized, choose the smallest check that resolves the uncertainty. Inspect setup and environment before executing application code. Do not add permanent tests during a review unless implementation was requested. No new harness is needed when current evidence answers the question.

Stop when credible affected boundaries have been assessed and remaining gaps are explicit. Do not run a full suite merely to produce a stronger-sounding verdict.

## Report

Lead with confirmed risks or the absence of findings within the reviewed scope. For each finding, provide the trigger, affected consumer, consequence, evidence, and smallest useful fix or verification. Include meaningful coverage limits and checks performed. Keep the report proportional; no fixed number of findings, invariants, or cleared risks is required.
