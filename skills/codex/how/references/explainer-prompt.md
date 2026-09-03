# Explainer prompt template

Use this only when a separate Codex synthesis agent is justified. Fill in the placeholders.

---

Write one architectural explanation for a senior engineer who is new to this subsystem. Stay read-only. Explorer reports are leads, not ground truth. Check important details in the code and resolve contradictions before writing.

## Repository

{REPOSITORY_PATH}

## Original question

> {QUESTION}

## Explorer reports

{EXPLORER_FINDINGS_ALL}

## Relevant files

{FILE_PATHS}

## Instructions

Explain the architecture well enough that the reader can begin working in it. Use concrete names such as `UserService` calls `AuthClient.refresh()` instead of vague phrases such as "the service delegates to the client."

Use only the sections that help:

- Overview.
- Key concepts.
- How it works.
- Where things live.
- Gotchas.

Reference exact files and functions. Keep code excerpts small. Use a diagram only if it makes a multi-component flow materially clearer. State any remaining gaps instead of filling them with assumptions.
