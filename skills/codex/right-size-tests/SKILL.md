---
name: right-size-tests
description: Choose and maintain the smallest useful test coverage for a software change. Use when deciding test necessity, permanence, layer, scope, duplication, TDD suitability, or when to stop rerunning tests. Do not use for straightforward execution of an already-required check, to bypass repository policy, or to reduce coverage for high-risk behavior.
license: MIT
---

# Right-size tests

Protect behavior that matters without turning every edit into a test project. The goal is enough durable evidence for the actual risk, not the highest test count or coverage percentage.

## Start with the project contract

Read applicable `AGENTS.md`, contributor guidance, test configuration, and CI checks. Follow explicit project requirements. Do not remove or skip required checks because this skill prefers a smaller test set.

Inspect existing coverage before adding tests. Extend a nearby test when it can express the new contract clearly. Do not duplicate the same claim at several layers unless each layer proves a different failure boundary.

## Decide whether a permanent test earns its cost

Add or keep automated tests around:

- core domain invariants;
- nontrivial calculations, parsing, and transformations;
- persistence, migrations, transactions, and data integrity;
- important API, serialization, filesystem, queue, or service boundaries;
- authorization, validation, privacy, and security rules;
- regression bugs with a reproducible failure;
- critical workflows after their behavior has stabilized.

Usually defer permanent automation for:

- temporary visual or layout behavior in a prototype;
- scaffolding likely to be replaced soon;
- trivial getters, framework wiring, and behavior already owned by a dependency;
- implementation details with no independent behavioral contract;
- broad snapshots that change with harmless layout or formatting edits;
- a second test that proves no new risk beyond an existing test;
- speculative cases with no plausible failure or meaningful consequence.

Before writing a test, answer:

1. What specific regression could this catch?
2. Is the behavior stable enough to become a maintained contract?
3. What is the cheapest reliable seam that can observe the failure?
4. Does an existing test already provide that evidence?
5. Will the test survive a behavior-preserving refactor?

If those answers do not justify permanent automation, use a bounded manual, build, lint, type, or runtime check and say why no test was added.

Prototype status never excuses stable high-consequence rules. Protect authorization, privacy, data integrity, accessibility semantics, or another durable contract even when the surrounding interface is temporary.

## Choose the cheapest sufficient seam

Use the lowest-cost seam that can actually prove the behavior. "Lower" is not automatically better when the risk lives at a boundary.

- Use compiler, type, schema, lint, or build checks for constraints those tools directly enforce.
- Use unit tests for pure logic, state transitions, calculations, parsers, validation rules, and edge cases.
- Use narrow integration or contract tests for persistence, serialization, framework wiring, and one external boundary at a time.
- Use a small number of end-to-end tests for critical cross-boundary workflows that lower layers cannot prove.
- Use exploratory or manual checks for changing visual design, interaction feel, animation, and early prototypes. Add durable automation after the contract settles.

Mocks prove behavior against the mock. They do not prove a provider, database, device, browser, or deployed system works. Keep that boundary explicit in the result.

## Use TDD when the contract is already clear

Prefer test-first work when expected behavior can be stated precisely before implementation, including algorithms, domain rules, parsers, transformations, validation, and regression reproductions.

For a bug fix, make the regression test fail for the expected reason before changing production code when that reproduction is safe and practical. Preserve the behavior contract while fixing it.

Do not force TDD onto exploratory UI, uncertain product behavior, throwaway prototypes, or scaffolding. Build the smallest vertical slice, inspect the result, settle the behavior, then protect the stable boundary.

## Keep the test change proportional

State the intended test seam before substantial test work. A short note is enough for ordinary changes. Use a matrix only when several distinct risks or environments genuinely require one.

- Cover meaningful outcomes and boundaries, not every branch combination.
- Prefer one expressive test over many near-duplicates.
- Reuse the repository's test framework and helpers.
- Do not introduce a new runner, browser harness, fixture system, or service emulator for one low-risk change.
- Keep snapshots short and reviewable. Prefer direct assertions when only a few values matter.
- Do not rewrite unrelated tests or broaden the task into test-suite cleanup.
- Never weaken, delete, or update an assertion merely to make a run green. First decide whether the product contract or the implementation is wrong.

## Run tests without looping

Use staged verification:

1. Run the smallest relevant existing or new test after the behavior changes.
2. If it passes, run the nearest affected package or subsystem suite when cross-file regression risk warrants it.
3. Run the full suite once near completion only when repository policy requires it, the change crosses broad boundaries, or the full suite is cheap enough to be the normal project check.

Record the command, scope, and result. A passing deterministic local check remains evidence until relevant code, fixtures, configuration, dependencies, or environment state changes.

Do not rerun an unchanged passing command for reassurance. Bounded repetition is valid when repetition is the test, such as documented flake assessment, concurrency or race investigation, a drift-prone external system check, release certification, or explicit project policy. State the reason and limit before repeating it.

Do not run the full suite after every small edit. Do not ask several agents to run the same suite.

Rerun a failed test only after one of these occurs:

- code or test data relevant to the failure changed;
- a concrete environmental cause was corrected;
- evidence indicates nondeterminism and one bounded rerun will distinguish it.

If the same failure recurs twice without new evidence, stop blind retries. Continue only with bounded, hypothesis-driven diagnostics. Report the blocker when those diagnostics produce no new evidence. Do not keep increasing sleeps, retries, or timeouts without evidence that duration is the problem.

## Stop when the evidence is sufficient

Testing is complete when:

- each material changed behavior has at least one sufficient verification seam, with another seam only when it proves a distinct boundary or risk;
- the targeted checks pass;
- any project-required broader checks pass, or their blocker is reported accurately;
- no known failing test was weakened or hidden;
- remaining unverified boundaries are named.

Do not create more tests after these conditions are met unless they prove a distinct risk. A request for exhaustive testing, a regulated or safety-critical context, or direct project policy can justify more work. State that reason.

## Handle existing failures honestly

Distinguish failures caused by the current change from pre-existing failures. Confirm that distinction with the narrowest useful evidence. Do not repair unrelated failures unless the user asks.

If a runner hangs or the environment cannot support a test, preserve the exact failure. Use bounded diagnostics tied to specific hypotheses, then report the blocker if no new evidence emerges. Do not claim the product works merely because a mock, build, or different test layer passed.

## Review and report

When reviewing a test plan or suite, identify:

- important behavior with no reliable protection;
- duplicated coverage that adds runtime without new confidence;
- brittle assertions tied to implementation details;
- high-level tests that can move to a narrower seam;
- temporary tests that should not become permanent maintenance work.

Recommend changes before deleting or restructuring tests unless the user asked for implementation.

At completion, report tests added or deliberately omitted, commands run, results, and remaining boundaries. Keep the evidence proportional. Do not dump routine test narration into the final answer.

For the rationale and source notes behind these rules, read [research notes](references/research.md).
