---
name: why
description: "Investigate design intent and historical constraints using Git, hosted PR discussion, and repository documents. Use for why code took its current shape; keep mechanics separate from author intent."
license: MIT
---

# Why

Explain what the repository record says about a decision. This is a read-only investigation.

## Evidence boundary

Use local Git history, code, tests, comments, ADRs, and other repository documents. Hosted PR descriptions, reviews, and comments are allowed through available read-only access. Do not follow references into ticket trackers, chat, incident systems, or document platforms; record them as unsearched leads. A user explicitly expanding the source scope takes precedence.

Code proves mechanics, not motivation. Preserve the distinction between direct statements, supported interpretations, inference, and unknowns. Read [epistemics](references/epistemics.md) when the evidence is ambiguous or conflicting.

## Find the decision

Anchor the question to current files and symbols. Start with the relevant diff or recent history, then follow the origin only as far as needed:

```bash
git log --oneline -20 -- <file>
git blame -L <start>,<end> -- <file>
git log --follow -p -- <file>
git log -S '<exact text>' -- <path>
git log -G '<regex>' -- <path>
```

Blame identifies last touch, which may be a move or formatting change. Inspect the introducing diff, surrounding tests, reverts, and follow-up fixes before attributing a reason. Consult [code archaeology](references/sources/code-archaeology.md) for difficult history searches.

Stop when the decision is adequately supported or the useful evidence is exhausted. Do not exhaust repository history to fill a missing rationale. Follow current runtime delegation rules; this skill does not request workers or prescribe models.

## Answer

Lead with the supported reason, or say that the reason is unknown. Cite the commits, PRs, or documents that bear on it. Label inference and explain its basis. Include competing explanations only when they remain plausible and consequential.

State material missing evidence and unsearched leads, even in a short answer. A full command log, confidence score, and fixed report structure are unnecessary. If the answer informs a change, identify which historical constraints still apply and which need current verification. Historical intent is evidence, not an immutable product requirement.
