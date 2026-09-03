---
name: blast-radius
description: "Assess what a code change could break beyond its diff, identify the safety invariants it depends on, and verify the highest-value claims with real code when safe. Use before shipping a risky change or when reviewing a diff whose indirect effects are unclear."
license: MIT
---

# Blast radius

Find the effects a change may have outside the edited lines. The default workflow is read-only. It does not authorize fixing the code or creating verification artifacts.

A caller list is only the start. Look for contracts, timing, data shapes, stored state, configuration, pinned dependencies, and downstream readers that a symbol search can miss.

## Load related skills without copying them

Use the current Available skills catalog to locate and read the complete `SKILL.md` for dependencies needed by the review. Whenever a required skill is absent from the catalog, check `$CODEX_HOME/skills/<name>/SKILL.md` when `CODEX_HOME` is set. If that path is unavailable or missing, check `~/.codex/skills/<name>/SKILL.md`. Treat a missing file as an unavailable dependency.

- Load `how` to trace changed behavior, execution flow, ownership, and boundaries.
- Load `why` when historical intent or a repository constraint affects the safety judgment.
- Apply `unslop` during the final edit when installed.

Do not copy their references or model-selection rules into this skill. Their files remain the source of truth.

## Establish the change

Resolve the exact target before analysis. Identify the repository, baseline, diff or commit range, changed symbols, deleted behavior, and any generated or vendored files involved. Distinguish staged, unstaged, committed, and hosted PR changes instead of silently combining them.

Read the full changed functions and their surrounding invariants. Use `how` to trace the relevant runtime path. Use `why` only when history may explain a compatibility requirement, threshold, workaround, or intentional asymmetry.

## Map effects beyond the diff

Follow each relevant boundary:

- Direct and indirect callers, implementations, registrations, reflection, generated code, and configuration-driven dispatch.
- API payloads, wire formats, serialized files, database schemas, cache keys, environment variables, and feature flags.
- Other packages, services, processes, languages, clients, or older versions that read the same data or contract.
- Ordering, async tasks, retries, cancellation, teardown, transactions, concurrency, and partial failure.
- The exact pinned dependency version, local patches, and upstream source when behavior depends on a library.
- Tests, fixtures, snapshots, migration paths, release gates, and monitoring that encode expected behavior.

Use `rg --files`, `rg`, language-aware tooling, and repository history. Read implementations rather than inferring behavior from names. A search with no matches is evidence only for the scope and pattern searched.

## Identify load-bearing safety invariants

Find the smallest set of facts the change's safety depends on, usually one to three. Examples include idempotence, a value never being persisted, a callback always running after teardown, an old client ignoring an added field, or a library call affecting only expired entries.

For each invariant, record how far the evidence reached:

1. Assertion only. No supporting evidence.
2. Source-backed. Exact repository or dependency source citation.
3. Failure-path analysis. The bad case was traced and cannot reach the changed behavior under stated conditions.
4. Executed verification. An existing test or disposable harness called the real code and would fail if the invariant were false.
5. Observed application behavior. The scenario was reproduced in a representative running environment.

Do not present an invariant as settled below level 4 unless the user asked for static analysis only. Level 5 is useful when available, not a universal requirement.

## Verify safely

Prefer existing checks only when they are demonstrably non-mutating in the current environment. Inspect the command and its configuration first. Do not run it when it may write databases, snapshots, generated files, coverage output, build artifacts, caches, or external systems. If its behavior is uncertain, treat executable verification as unavailable.

Creating a focused harness is a constrained exception to the read-only workflow and requires explicit user authorization for temporary local writes. With that authorization, create it only in a disposable directory from `mktemp -d` or the task's designated scratch area. Inspect the entrypoint and environment first, use local fixtures, and import the same pinned code the application ships. Never place the harness in the repository unless the user separately asks for implementation.

Do not install dependencies, change configuration, write to production or shared services, send messages, or run a destructive scenario as part of a review. Do not execute application initialization unless its side effects are understood and confined to the authorized disposable environment. If safe verification is unavailable or temporary writes were not authorized, mark the invariant unproven and name the missing evidence.

Summarize the command and the relevant output. Do not paste large logs.

## Use Codex sub-agents when breadth warrants it

For a narrow change, work in the lead agent. For a wide or high-risk change, use read-only investigators with distinct angles, such as consumer contracts, lifecycle and concurrency, or persistence and compatibility. Use at most three workers total, including all authorized descendants, and fewer when the active environment has less capacity.

Use Codex collaboration tools only and GPT models only. Follow the loaded `how` skill's current model-selection policy rather than duplicating it here.

The lead owns the shared concurrency budget. Before each batch, use the environment's published limit and `list_agents` to count occupied slots. If no limit is published, use one worker at a time. Start workers with unique lowercase `task_name` values and `fork_turns: "none"` whenever overriding model or reasoning effort. Tell each worker whether it may spawn children. Default to no child agents unless the lead reserved capacity and authorized a fixed per-worker child count within the three-worker global limit.

Use `wait_agent` with a long timeout instead of frequent polling. One wait may return after a single mailbox update, so track every worker, call `list_agents` after updates, and repeat bounded waits until every assigned worker has finished or needs attention. The lead validates findings against the code and evidence. Independent opinions are leads, not proof.

## Report

Lead with the verdict and any confirmed high-impact risk. Then include:

- What changed, including non-obvious behavior.
- Safety invariants. State each invariant, its evidence level, and the proof or gap.
- Confirmed risks. Explain the failure path, likelihood, impact, affected code, and cheapest detection method.
- Cleared risks. Name what was checked and the evidence that ruled it out.
- Verification run. List focused commands or scenarios and the relevant results.
- Remaining gaps. Mark unproven claims and environmental limits plainly.
- Before merge. Give the smallest test, repro, or observation that would catch the most credible failure.

Cite exact files, lines, commits, dependency versions, and commands. Do not invent consumers, APIs, or runtime behavior. Keep likelihood and impact separate. A plausible story without executable or source evidence is not a finding.
