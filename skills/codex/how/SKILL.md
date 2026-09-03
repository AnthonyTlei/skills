---
name: how
description: "Explain how a codebase subsystem works, trace runtime flow, answer placement or ownership questions, and critique architecture when requested. Use for code walkthroughs and architectural mental models."
license: MIT
---

# How

Explore the codebase and explain how a subsystem works at the level of a senior engineer joining the project. Build a useful mental model instead of annotating every line.

Use two modes:

1. Explain, the default. Trace the implementation and describe the architecture and runtime flow.
2. Critique. Explain first, then assess architectural problems and tradeoffs.

## Scope the question

Interpret the user's question and state a brief best-guess scope if it is ambiguous. Continue without stopping for clarification unless different interpretations would materially change the work or require different authorization.

Classify the investigation:

- Simple: one function, utility, or module with a short call chain. Explore directly in the lead agent.
- Moderate: several related files or one unfamiliar boundary. Use one explorer only if it will save time or reduce uncertainty.
- Complex: a subsystem spanning packages, services, persistence, or multiple runtime boundaries. Use two or three parallel explorers with distinct assignments.

Lean simple. Delegation has a cost and should buy independent coverage, not duplicate reading.

## Codex sub-agent policy

Use Codex collaboration tools only. Never invoke Cursor Task agents or non-GPT models.

When delegation is useful:

1. Before every worker batch, read the concurrency budget supplied by the active Codex environment and call `list_agents` to count occupied slots. The lead agent occupies one slot. Never start more workers than the remaining capacity allows. Reduce the batch, handle a slice in the lead agent, or run workers in a later batch when capacity is tight.
2. Start every explorer, critic, or synthesis worker with `spawn_agent`. Give it a unique lowercase `task_name` containing only letters, digits, and underscores. Use `fork_turns: "none"` whenever overriding the model or reasoning effort. Put the question, assigned role or slice, repository path, read-only boundary, and relevant prompt template in the task message.
3. Tell every explorer to stay read-only. It may inspect files and run non-mutating diagnostics, but it must not edit files, install dependencies, or change external state.
4. Give each explorer a distinct slice such as request path, data model, configuration, persistence, or observability.
5. Track every worker started for the batch. Use `wait_agent` with a long timeout instead of frequent polling. Since one wait may return after only one mailbox update, use `list_agents` after each update and repeat bounded waits until every assigned worker has finished or needs attention. Review each final report and verify important contradictions against the code.

Choose among GPT models available in the current Codex environment:

- Prefer `gpt-5.6-luna` at low or medium reasoning for narrow file mapping and straightforward call-chain tracing.
- Prefer `gpt-5.6-terra` at medium or high reasoning for cross-file investigation, synthesis, and ordinary architecture review.
- Prefer `gpt-5.6-sol` at high or xhigh reasoning for ambiguous boundaries, large systems, security-sensitive flows, or hard architectural judgment.
- Reserve max or ultra reasoning for unusually difficult or high-stakes work.
- If one of these models is unavailable, use the nearest available GPT model with a comparable cost and capability. Do not use a non-GPT model.

Use the cheapest model likely to finish its assigned slice accurately. Increase model capability or reasoning when the first pass exposes ambiguity, contradictions, or important risk. Do not spawn extra agents merely to use different models.

The current agent should synthesize findings by default. Spawn a separate synthesis agent only when the reports are large, materially contradictory, or the subsystem is difficult enough to justify the extra cost. If used, give it the original question, all explorer reports, relevant file paths, and [the explainer prompt](references/explainer-prompt.md).

## Explain mode

For direct exploration and explorer tasks:

- Start with `rg --files` and `rg` to locate directories, symbols, types, and entry points.
- Read implementations rather than inferring behavior from names.
- Trace the path from trigger to effect, including callers, callees, data transformations, persistence, and external boundaries.
- Stop when the path can be explained without hand-waving. Name any gap that remains unverified.
- Record exact file paths, symbols, and useful line numbers.
- Note behavior a newcomer would likely misunderstand.

For complex questions, build each explorer task from [the explorer prompt](references/explorer-prompt.md) and add one specific exploration angle.

Reconcile the reports against the code, then present one explanation. Use this structure only where it helps:

- Overview. What the subsystem is, what it does, and why it exists.
- Key concepts. The few types, services, or abstractions needed to follow the flow.
- How it works. The trigger, execution path, data movement, and decision points.
- Where things live. A short map of the files and directories needed to start work.
- Gotchas. Non-obvious behavior, sharp edges, or verified historical constraints.

Reference specific files and functions. Avoid large code dumps. Add a small diagram only when it makes a multi-component flow easier to understand than prose.

## Critique mode

Use critique mode when the user asks for architectural problems, risks, or improvements.

First complete the explain flow. Architecture criticism without a traced implementation is guesswork.

Then choose the smallest useful critic set:

- Bounded, ordinary subsystem: one `gpt-5.6-terra` critic at high reasoning.
- Broad, risky, or disputed subsystem: two independent critics, normally `gpt-5.6-terra` at high and `gpt-5.6-sol` at xhigh.
- Add a third critic only when the risk or breadth warrants the cost and a free agent slot exists.

Build each task from [the critic prompt](references/critic-prompt.md). Give critics the explanation, relevant paths, and [the critique rubric](references/critique-rubric.md). Critics must read the actual code and stay read-only.

The lead agent judges the results rather than counting votes. Classify each finding:

- Act on: a demonstrated problem worth fixing now.
- Consider: a real concern whose cost or priority remains unclear.
- Noted: a valid, low-priority tradeoff.
- Dismissed: unsupported, incorrect, missing context, or merely stylistic.

Present the standalone explanation first, followed by the critique. Cite code evidence for every retained finding and say what remains unverified.
