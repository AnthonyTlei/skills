# Explorer prompt template

Fill in the placeholders and send the resulting task to a Codex sub-agent.

---

You are mapping one slice of a codebase so another agent can explain how the whole subsystem works. Stay read-only. Do not edit files, install dependencies, or change external state.

## Repository

{REPOSITORY_PATH}

## Question

> {QUESTION}

## Assigned slice

{EXPLORATION_ANGLE}

## Investigation

Use `rg --files` and `rg` to find relevant code, then read the actual implementations. Do not infer behavior from file names.

Trace this slice from its entry point to its effect:

1. Find what triggers the behavior.
2. Follow callers, callees, and data transformations.
3. Read the central types, interfaces, services, and configuration.
4. Identify boundaries with other packages, persistence, queues, APIs, or platform services.
5. Record anything surprising or easy to misunderstand.

Stay on the assigned slice. Other agents may be tracing adjacent parts. Continue until you can explain the path without guessing. If a connection remains unclear, name the gap.

## Report

Return:

- Components found, with exact paths and one-line roles.
- Flow, step by step, with symbols and useful line numbers.
- Files read.
- Inputs, outputs, and subsystem boundaries.
- Non-obvious behavior.
- Open questions or unverified links.
