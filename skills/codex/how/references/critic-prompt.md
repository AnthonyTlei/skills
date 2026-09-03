# Critic prompt template

Fill in the placeholders and send the resulting task to an independent Codex sub-agent.

---

Review the architecture of this codebase subsystem. Stay read-only. Do not edit files, install dependencies, or change external state.

The explanation below is an orientation aid, not evidence. Read the relevant code and form your own judgment.

## Repository

{REPOSITORY_PATH}

## Architectural explanation

{EXPLANATION}

## Relevant files

{FILE_PATHS}

## Critique rubric

{CRITIQUE_RUBRIC_CONTENTS}

## Task

Find architectural problems, not line-level bugs or style preferences. Ask whether the subsystem fits its current needs and likely evolution. An empty critique is valid when the architecture is sound.

For each finding, report:

1. Severity: `structural`, `concern`, or `observation`.
2. Finding: the specific boundary, model, dependency, or coupling at issue.
3. Evidence: exact paths, symbols, and code behavior that demonstrate it.
4. Impact: the concrete cost to testing, change safety, reliability, performance, or operations.

Do not propose a rewrite without first proving a problem. Do not ask for more abstraction unless you can name the repeated change or dependency it would isolate. Treat intentional tradeoffs fairly.
