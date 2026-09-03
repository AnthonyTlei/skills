# Current Codex model guide

This guide was checked on 2026-09-03 against OpenAI's published model guidance and the collaboration tools available in Codex. Recheck both before an explicit model or effort override. Available names and supported reasoning levels may change.

## Two separate choices

Choose a model family for capability, latency, and cost. Choose reasoning effort for how hard that particular assignment is. A stronger family at low effort and a smaller family at high effort are not interchangeable.

| Assignment | Starting choice | Escalate when |
| --- | --- | --- |
| Exact inventory, formatting, rename, or repetitive edit | Luna low | The work requires judgment across several files or unclear evidence. |
| Bounded repeatable edit with an exact contract | Luna medium | The edit exposes integration or architecture decisions. |
| Ordinary repository exploration, synthesis, dependency inspection, logs, or review | Terra medium | Evidence conflicts or several boundaries must be reconciled. |
| Broad but bounded analysis or cross-file review | Terra high | The result becomes an architecture-sensitive implementation decision. |
| Clear implementation or integration work | Sol medium | The change has substantial cross-boundary risk or debugging depth. |
| Substantial implementation, debugging, architecture-sensitive change, or final integrative review | Sol high | Ordinary investigation has isolated a genuinely difficult reasoning problem. |
| Difficult coupled architecture or stubborn debugging | Sol xhigh | The problem remains an isolated quality-first blocker after a well-scoped attempt. |
| Exceptional concurrency, rendering, or cross-system blocker | Sol max | Do not escalate further automatically. Report the blocker or ask for direction. |

The table is a starting policy, not a benchmark result. Use the current tool's supported combinations. Preserve a user's explicit model choice.

## Effort test

- **Low:** the procedure and acceptance criteria are exact.
- **Medium:** ordinary multi-step reasoning with bounded ambiguity.
- **High:** important cross-file judgment, integration, or nontrivial debugging.
- **Xhigh:** several coupled decisions or a stubborn, evidence-backed problem.
- **Max:** the hardest isolated blocker where quality matters more than latency or cost.

Do not choose max because a task is long. Decompose independent work first. Do not repeat a failed attempt at a higher effort without stating what evidence makes the escalation useful.

Do not select Ultra unless the user explicitly requests it for the task. OpenAI describes Codex multi-agent behavior as similar to Ultra mode, so this repository treats Ultra as an orchestration choice rather than another default rung in the reasoning ladder.

## Sources and local behavior

OpenAI describes GPT-5.6 Sol as its flagship model for complex professional work, Terra as the balance of intelligence and cost, and Luna as the efficient option for high-volume or cost-sensitive workloads. Its reasoning guide recommends medium as a balanced starting point, lower effort for latency-sensitive work, and high through max only where evaluations show a material quality gain: [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model).

OpenAI also says multi-agent work is useful when a complex task divides cleanly into independent workstreams. That supports parallel read-heavy lanes, but it does not establish safe file ownership by itself. The one-writer and integration rules in this skill come from Codex's current shared-filesystem collaboration contract and repository workflow.

Git documents that linked worktrees share one repository while giving each working tree its own files, `HEAD`, and index. This makes them suitable for independent implementation branches, not for isolating external services or shared trackers: [git-worktree](https://git-scm.com/docs/git-worktree).
