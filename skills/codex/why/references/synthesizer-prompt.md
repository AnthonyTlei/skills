# Synthesizer prompt template

Use this only when a separate Codex synthesis worker is justified.

---

Answer a "why" question about code using repository history only. Stay read-only. Investigator reports are leads, not ground truth. Spot-check important citations in git, repository files, and hosted PR context when read-only access exists.

## Repository

{REPOSITORY_PATH}

## Question

> {QUESTION}

## Code anchor

{CODE_ANCHOR}

## Investigator reports

{INVESTIGATOR_REPORTS}

## Instructions

Follow the confidence tiers in `references/epistemics.md`.

- Merge duplicate evidence.
- Reconcile contradictions without hiding either source.
- Distinguish local git evidence from hosted PR evidence.
- Treat external ticket, document, chat, incident, observability, and analytics references as unsearched leads.
- Do not infer intent from code mechanics.
- Do not edit files or change hosted repository state.

## Output

Include:

1. The question.
2. The code in question.
3. What we found, with Direct or Supported labels and precise citations.
4. What we can reasonably infer, with hedged language and visible reasoning.
5. Competing hypotheses when needed.
6. What we do not know. Always include this, even when the remaining gaps are small.
7. Repository evidence consulted, including commands, commits, PRs, files, null searches, and unavailable hosted context.
8. Confidence summary.

Before returning, confirm that each causal claim has evidence appropriate to its tier and that no external source was silently treated as searched.
