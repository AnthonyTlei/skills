---
name: why
description: "Investigate why code or architecture took its current shape using git history, hosted PR context when available, and rationale preserved in the repository. Use for design intent, regressions, tradeoffs, historical constraints, or unexplained thresholds. Use how for runtime behavior."
---

# Why

Investigate the motivation and constraints behind code. Separate documented intent from inference and unknown history.

This skill complements `how`. Use `how` to explain what the code does. Use `why` to explain what repository history says about the decisions that shaped it.

## Evidence boundary

Use repository evidence only:

- Commit messages, diffs, authorship, dates, branches, tags, and file history.
- Hosted pull request descriptions, reviews, and comments when `gh` or equivalent read-only access is available.
- Code comments, tests, ADRs, design notes, changelogs, release notes, and other files stored in the repository.
- Co-change history across files and symbols.

Do not search ticket trackers, document platforms, team chat, observability systems, error trackers, analytics warehouses, or other external evidence systems. If repository history points to one of them, record the reference as an unsearched lead and a gap.

Code proves mechanics, not intent. Read [the epistemics framework](references/epistemics.md) before synthesizing.

## Anchor the target

Interpret the target from the question and current conversation. If the referent is ambiguous, state a short best-guess interpretation and continue unless different interpretations would materially change scope or authorization.

Build a code anchor:

- Exact file paths, useful line ranges, and key symbols.
- Recent commits touching the target.
- Blame for the relevant lines when last-touch history matters.
- Full history through renames when the current commit does not explain the origin.
- PR numbers and external IDs found in commit messages.

Start with non-mutating commands such as:

```bash
git blame -L <start>,<end> <file>
git log --follow -p -- <file>
git log --oneline -20 -- <file>
git log -1 --format=%B <commit>
git log -S '<exact text>' -- <path>
git log -G '<regex>' -- <path>
```

Use `gh pr view` only when `gh` is installed and authenticated. Local git history and hosted PR discussion are separate evidence sets. Report unavailable hosted context as a gap.

Read [the code archaeology playbook](references/sources/code-archaeology.md) for search patterns and common traps.

## Choose effort and delegation

Match effort to the question:

- Simple. One symbol or a single well-documented commit. The lead agent investigates and answers directly.
- Moderate. Several commits, a rename, or one missing link between code and a PR. Use one investigator only if it reduces uncertainty or saves time.
- Complex. A subsystem with a long history, competing explanations, or changes spread across several files. Use up to two or three investigators when distinct angles justify the cost and capacity permits. Otherwise investigate the angles sequentially in the lead agent.

Useful angles for complex work include:

- Origin and evolution through commits, blame, renames, reverts, and follow-up fixes.
- Hosted PR rationale, review debate, and alternatives when read-only access exists.
- In-repository rationale in tests, comments, ADRs, changelogs, release notes, and co-change patterns.

Escalate from simple to moderate if the apparent rationale conflicts with the diff, the target cannot be linked to the cited commit, or the hosted PR says something materially different from local history.

## Codex sub-agent policy

Use Codex collaboration tools directly. Never invoke Cursor Task agents or non-GPT models.

Before every batch, use the concurrency budget supplied by the active Codex environment and call `list_agents` to count occupied slots. The lead occupies one slot. If the environment does not publish a limit, use one worker at a time. Never infer the limit from `list_agents` alone.

Start every investigator or synthesis worker with `spawn_agent`:

- Give it a unique lowercase `task_name` containing only letters, digits, and underscores.
- Use `fork_turns: "none"` whenever overriding the model or reasoning effort.
- Include the repository path, original question, code anchor, assigned angle, read-only boundary, and [investigator prompt](references/investigator-prompt.md).
- Keep assignments distinct. Do not pay several agents to run the same history search.

Choose the cheapest GPT model likely to finish accurately:

- Prefer `gpt-5.6-luna` at low or medium reasoning for narrow blame, log, and in-repo text searches.
- Prefer `gpt-5.6-terra` at medium or high reasoning for rename tracking, cross-file history, PR review, and ordinary synthesis.
- Prefer `gpt-5.6-sol` at high or xhigh reasoning for contradictory history, large subsystems, security-sensitive decisions, or difficult synthesis.
- Reserve max or ultra reasoning for unusually difficult or high-stakes investigations.
- If a named model is unavailable, use the nearest available GPT model with comparable cost and capability. Never use a non-GPT model.

Every worker stays read-only. It may inspect repository history and hosted PR material, but it must not edit files, create branches, post reviews, comment, merge, close, label, or change external state.

Use `wait_agent` with a long timeout instead of frequent polling. One wait may return after a single mailbox update, so track every worker, call `list_agents` after updates, and repeat bounded waits until each assigned worker has finished or needs attention. Verify important citations and contradictions against the repository.

The lead should synthesize by default. Spawn a separate synthesis worker only when reports are large, materially contradictory, or difficult enough to justify the cost. Give it all reports, the code anchor, [the epistemics framework](references/epistemics.md), and [the synthesizer prompt](references/synthesizer-prompt.md).

## Present the result

Keep documented intent separate from inference. Include:

- The question.
- The code in question.
- What we found. Direct or strongly supported claims with precise commit, PR, or file citations.
- What we can reasonably infer. Hedged claims with the inference chain shown.
- Competing hypotheses when more than one explanation fits.
- What we do not know. This section is mandatory. Name missing hosted context and external references that were deliberately not searched.
- Repository evidence consulted. List git commands, commits, PRs, and in-repo files checked, including searches that returned nothing.
- Confidence summary.

When the result will inform a code change, finish with a short Preserve, Change, Avoid, and Risk constraint set. Historical rationale is planning input, not a permanent requirement.

Do not weaken confidence language while editing the final response. An honest unknown is a valid result.

## References

- [Epistemics](references/epistemics.md) defines evidence tiers and phrasing.
- [Code archaeology](references/sources/code-archaeology.md) contains git and PR search patterns.
- [Investigator prompt](references/investigator-prompt.md) is the base task for Codex workers.
- [Synthesizer prompt](references/synthesizer-prompt.md) defines reconciliation and output checks.
