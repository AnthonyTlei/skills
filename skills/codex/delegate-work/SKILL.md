---
name: delegate-work
description: Decide when to use Codex subagents, divide work safely, choose GPT model and reasoning effort, prevent conflicting writes, and integrate worker evidence. Use when planning or running multi-agent work, selecting a worker model, or choosing between a shared checkout and Git worktrees. Do not use for a small sequential task that one agent can complete directly.
license: MIT
---

# Delegate work

Use subagents when independent work can finish sooner without making integration less reliable. Delegation is a coordination choice, not a reward for task size.

The primary agent owns the user's goal, authorization boundaries, project state, integration, and final verification. A worker owns only the bounded assignment in its prompt.

## Respect the current task

Follow explicit user, system, and repository instructions before this skill. Do not delegate when the user forbids it. Do not change the primary task's model or reasoning effort unless the user asks and the product supports that change.

Delegation does not expand permission. A worker may inspect or modify only what the primary agent could inspect or modify for the current request.

Before creating workers, inspect the collaboration tools and live capacity available in the current session. Model names, supported reasoning levels, concurrency, and worktree behavior can change. Never hardcode a worker limit from an earlier run.

## Make delegation earn its cost

Delegate a lane only when all of these are true:

- its objective is concrete and bounded;
- its result can be checked independently;
- it can run while the primary agent does other useful work;
- the context and handoff are cheaper than doing it directly;
- its reads and writes will not race with another lane.

Keep the work in the primary agent when it is small, sequential, tightly coupled to edits already in progress, dependent on rapidly changing context, or cheaper to finish than to explain and integrate.

Length alone is not a reason to delegate or increase reasoning effort. Split long work only at real seams. A short but stubborn concurrency bug may justify a stronger model; a long inventory may not.

## Prefer read-heavy parallel lanes

Favor parallel evidence gathering when lanes have distinct questions, such as:

- separate modules, services, or platforms;
- documentation, dependency, history, or configuration review;
- distinct logs, test failures, or provider boundaries;
- independent security, accessibility, or performance reviews.

Give each worker a question and scope. Do not launch several broad repository explorers and hope their results differ. The primary agent should keep progressing while workers run.

## Keep shared writes serialized

Assume subagents share the current filesystem unless the runtime explicitly provides an isolated worktree. Two workers must not edit the same file or overlapping generated state at the same time.

The primary agent is the sole integrator. Assign one writer at a time for shared sources of truth, including:

- Linear or another external tracker;
- feature maps and their generated views;
- specifications, plans, and decision records;
- `CHANGELOG` files, lockfiles, migrations, schemas, and shared configuration;
- generated indexes or outputs derived from multiple inputs.

Other workers may inspect that state and return findings or a proposed patch. The designated writer applies the final change. For external writes, use one owner, preserve any approval gate, use the system's idempotence mechanism where it exists, and read the result back. If a write outcome is uncertain and no idempotence mechanism makes a retry safe, stop and report rather than retrying.

If two workers begin to overlap, stop or redirect one, serialize the change, and reconcile in the primary agent. Do not let conflicting edits continue for the sake of parallelism.

## Use worktrees for independent implementation

Use a Git worktree only when the current subagent mechanism can create one for the delegated lane and the task authorizes that environment. If it cannot, keep workers read-only in the shared checkout or serialize writes through the primary agent.

When worktrees are available, use one when two implementation lanes need separate branches, have low file overlap, and have a clear integration seam. A worktree separates the branch, index, and working files. It does not isolate external services, databases, issue trackers, or other shared resources.

Before assigning work in a worktree:

1. Confirm the repository permits the branch and worktree operation.
2. Establish the exact base, branch, and worktree path.
3. Give the worker its absolute working directory and file ownership.
4. Require the worker to verify its working directory and branch before writing.
5. Define the expected commit, evidence, and handoff format.

The primary agent reviews the commit or diff, integrates it, resolves conflicts, and runs final validation on the combined state. Do not create a worktree when the integration cost is likely to exceed the parallel gain. Never remove a worktree containing unmerged or uncommitted work without explicit authority.

## Choose the smallest credible model

Choose the model family from the assignment's ambiguity and consequence. Choose reasoning effort from the depth of thought required. Start at the lowest combination that can reliably do the job, then escalate a blocked lane for a concrete reason.

- Use **Luna low** for exact inventories, renames, formatting, and other narrow mechanical work.
- Use **Luna medium** for bounded, repeatable edits with precise acceptance criteria.
- Use **Terra medium** as the ordinary worker for repository exploration, documentation synthesis, dependency or log analysis, read-heavy review, and modest bounded changes.
- Use **Terra high** when a bounded analysis must reconcile broader or ambiguous evidence.
- Use **Sol medium or high** for implementation, integration, substantial debugging, architecture-sensitive changes, and integrative review. Prefer high when mistakes would propagate across important boundaries.
- Use **Sol xhigh** for difficult coupled decisions, unresolved architecture, or stubborn debugging that resists an ordinary pass.
- Use **Sol max** only for an isolated, quality-first blocker whose difficulty cannot be removed by clearer decomposition. State why xhigh is insufficient.
- Do not select **Ultra** unless the user explicitly requests Ultra for that task. Treat it as aggressive orchestration behavior, not the next routine reasoning step.

Do not use a premium model to compensate for a vague prompt. Tighten the scope first. Do not escalate the entire goal because one lane is hard; escalate that lane if possible.

Read [the current model guide](references/model-guide.md) before making an explicit model or effort override. If the current runtime disagrees with the guide, the runtime wins.

## Write a complete worker contract

Every worker prompt should state:

- the exact objective and why it matters;
- the files, subsystem, or evidence source in scope;
- whether the worker is read-only, may edit named files, or owns a worktree;
- decisions already made and repository instructions that apply;
- the required output, evidence, and validation;
- what must not be changed;
- stop conditions and when to report a blocker;
- a requirement to stop before an unauthorized external, destructive, or costly action, a conflict with another worker or an unisolated shared resource, or an outcome that cannot be independently verified.

Use a unique lowercase task name. Avoid personal data and secrets in prompts.

When overriding a worker's model or effort, use the context-fork option required by the current collaboration tool. If an override forbids a full-history fork, pass only the recent turns needed or no turns, then restate all required context in the prompt. Use full-history inheritance only when the worker genuinely needs it and no override is required.

Workers should not spawn their own workers unless the primary agent explicitly authorizes that structure for an independently decomposable subproblem. Recursive delegation is not a default.

## Run and converge

1. Decompose the goal into a small task map with ownership and dependencies.
2. Check live agents and capacity before spawning a batch.
3. Start only independent lanes that provide real wall-clock benefit.
4. Continue useful primary-agent work instead of waiting immediately.
5. Send follow-up context to an existing worker instead of spawning a duplicate.
6. Wait with a meaningful timeout and avoid busy polling or narrating unchanged status.
7. Account for every assigned worker. Interrupt obsolete or conflicting work.
8. Inspect worker evidence and diffs; do not accept a completion claim on trust.
9. Integrate in the primary agent and run the required validation once on the combined state.

Do not create open-ended review, repair, and rereview chains. One independent final reviewer is normally enough. Add another only for a distinct high-risk discipline or an explicit user request. Do not ask multiple agents to run the same expensive test suite.

The delegated task is complete when every worker is accounted for, authorized changes are integrated, shared state has one coherent owner, the combined result is validated, and remaining uncertainty is reported. A worker cannot declare the user's whole goal complete.

## Report the result

Summarize:

- which lanes were delegated and why;
- any deliberate model or effort override;
- what each worker contributed;
- how conflicts and shared writes were controlled;
- what the primary agent integrated and verified;
- any incomplete lane or unverified boundary.

Keep routine orchestration details out of the final answer unless they affect confidence, cost, or what the user should do next.
