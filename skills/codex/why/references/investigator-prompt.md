# Investigator prompt template

Fill in the placeholders and send the task to a Codex sub-agent.

---

Investigate one angle of the repository history behind a piece of code. The lead agent will combine your report with other evidence.

Stay read-only. Do not edit files, create branches, commit, push, post reviews or comments, merge, close, label, or change external state.

## Repository

{REPOSITORY_PATH}

## Question

> {QUESTION}

## Code anchor

Target files and lines: {FILES_WITH_LINE_RANGES}

Key symbols: {SYMBOLS}

Seed commits and PRs: {SEED_HISTORY}

## Assigned angle

{INVESTIGATION_ANGLE}

## Method

Use git, `rg`, and repository files. Use `gh` or an equivalent hosted-repository tool only when authenticated read-only access is available. Stay on the assigned angle.

Gather evidence instead of writing the final narrative:

1. Start broad enough to catch renames, reverts, follow-up fixes, and related files.
2. Read full commit messages and relevant diffs, not only one-line subjects.
3. When using hosted PR context, read the description, reviews, and relevant discussion.
4. Capture short exact excerpts when wording proves intent. Include commit hashes, PR numbers or URLs, file paths, symbols, and useful lines.
5. Record the searches that returned nothing.
6. Surface contradictions and missing links.
7. Do not follow external ticket, chat, document, incident, or analytics links. Return them as unsearched leads.

## Report

Return:

- Scope and angle investigated.
- Searches and commands run.
- Direct evidence with exact citations.
- Indirect evidence and what it may suggest.
- Contradictions.
- Unsearched external leads.
- Gaps and unresolved questions.
- Files, commits, and PRs inspected.

Do not claim intent from code mechanics alone.
