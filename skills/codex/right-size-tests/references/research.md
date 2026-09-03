# Research notes

These notes explain the choices in `right-size-tests`. They are not a mandatory reading list for ordinary test work.

Research checked on 2026-09-03.

## Findings

The practical cost comes from duplicated evidence, slow feedback, brittleness, and repeated execution. Raw test count is a poor target.

- Google's testing guidance explains why broad end-to-end suites are slow, harder to diagnose, and more exposed to unrelated failures. It recommends smaller integration tests when they can catch the same defect, with only a small set of end-to-end checks for whole-system confidence: [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html).
- Ham Vocke's practical test-pyramid guide treats the pyramid as a heuristic rather than a fixed ratio. It recommends observable behavior over implementation detail, narrow tests for integration boundaries, few high-level tests, and removing duplicated coverage that provides no additional confidence: [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html).
- Playwright recommends testing user-visible behavior, using resilient user-facing locators, isolating tests, and avoiding third-party systems outside the team's control: [Playwright best practices](https://playwright.dev/docs/best-practices).
- Testing Library ties maintainability to tests that resemble real use and warns that tests coupled to component internals slow behavior-preserving refactors: [Testing Library introduction](https://testing-library.com/docs/).
- Jest recommends short, focused, deterministic snapshots and explicitly warns against regenerating snapshots merely to clear failures: [Snapshot testing](https://jestjs.io/docs/snapshot-testing).
- Google's brittleness guidance defines a useful test as one that fails when an important property breaks, not when irrelevant ordering or formatting changes. It recommends expressive assertions and narrower golden comparisons: [How I Learned To Stop Writing Brittle Tests and Love Expressive APIs](https://testing.googleblog.com/2024/04/how-i-learned-to-stop-writing-brittle.html).

## Codex-specific evidence

OpenAI documents that repositories can use `AGENTS.md` to tell Codex which test commands and project practices to follow. It also says Codex should expose test failures and uncertainty rather than hide them: [Introducing Codex](https://openai.com/index/introducing-codex/).

Direct user reports in the public Codex repository show the failure pattern this skill aims to constrain:

- One report documented at least 18 full-suite runs, one five-test selection run 13 times, and repeated review and repair cycles in a single task: [openai/codex issue 38989](https://github.com/openai/codex/issues/38989).
- Another report describes Codex rerunning earlier validations with different commands and expanding beyond the request: [openai/codex issue 5970](https://github.com/openai/codex/issues/5970).
- A timeout report includes repeated retries of long-running test commands despite unchanged conditions: [openai/codex issue 3557](https://github.com/openai/codex/issues/3557).
- A regression report describes tests being weakened after repeated failures so the suite would pass, while the intended behavior remained broken: [openai/codex issue 24922](https://github.com/openai/codex/issues/24922).

These reports are first-person examples, not prevalence data. They support bounded reruns, explicit stop conditions, preservation of assertions, and accurate blocker reporting. They do not justify skipping tests that a project or risk profile requires.

## Resulting policy

The skill therefore uses four rules:

1. Every permanent test must protect a plausible, durable behavior or boundary.
2. Each distinct risk should be proven at the cheapest reliable seam, without repeating all lower-level cases at higher levels.
3. Passing evidence is not rerun until a relevant input changes. Repeated identical failures trigger diagnosis, not another blind retry.
4. Project requirements and high-consequence risks override the preference for less test work.
