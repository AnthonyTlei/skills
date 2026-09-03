# Epistemics

Repository history is incomplete. Commits can be squashed, rewritten, or poorly described. PR discussion may be inaccessible. Comments can explain a current invariant without preserving the original motivation.

Every claim about intent belongs to one evidence tier.

## Direct

A repository source explicitly states the reason.

Examples include a PR description naming the failure being fixed, a review comment explaining why an alternative was rejected, a commit message naming a constraint, or a code comment explaining why a specific value exists.

State the claim plainly and cite the exact commit, PR, review comment, or file line.

## Supported

Several repository signals converge, but no single source states the full reason. For example, a performance-focused PR, matching benchmark changes, and a follow-up regression test may jointly support the same rationale.

Name each supporting item. Do not turn correlation into a direct author statement.

## Inferred

The history supports a reasonable reading, but the record never states it. Use phrases such as "appears to," "likely," "suggests," or "is consistent with." Show the inference chain.

Code shape alone belongs here at best. A null check proves that the code handles null, not why the author added it.

## Speculative

The explanation is plausible but weakly supported, or several explanations fit equally well. Label it as a possibility and state what evidence is missing.

## Unknown

The repository record does not answer the question. Say what was searched and what did not surface. If commits or PRs point to an external ticket, document, chat thread, incident, or dashboard, name it as an unsearched lead rather than following it.

## Rules

- Treat a reason suggested by the user as a hypothesis, not a conclusion.
- Do not cite code behavior as proof of author intent.
- Surface contradictions between commit messages, diffs, PR descriptions, and review comments.
- Distinguish local git history from hosted PR evidence.
- Treat missing history as a gap, not evidence that no rationale existed.
- Prefer an explicit unknown to a polished guess.

Before returning, check every causal claim. If it lacks a direct citation, move it to Supported, Inferred, Speculative, or Unknown and adjust the wording.
