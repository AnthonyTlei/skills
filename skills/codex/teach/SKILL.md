---
name: teach
description: "Teach a codebase mechanism, change, or design through a concrete example and repository evidence. Use when the user wants to understand and reason about the system."
license: MIT
---

# Teach

Help the user reason about the system at the depth their question needs. This is a read-only teaching task, not permission to change code.

Start from their question and apparent familiarity. Explain the smallest complete idea first, then follow a representative input or action through the relevant components to its outcome. Connect unfamiliar concepts to that example before introducing more terminology.

Read the implementation needed to explain mechanics. Investigate history only when the reason for a design matters to the lesson. Use `how` or `why` if a deeper investigation benefits from their guidance and they are available; neither is a required dependency for a simple explanation. Reuse evidence already gathered in the conversation unless it may have drifted.

Keep documented intent separate from inferred rationale. Repository history and hosted PR discussion are the default history sources; do not silently expand to private external systems. State important unknowns without derailing the lesson.

Include boundaries, failure behavior, or a counterexample when they change the reader's understanding. Use a compact diagram or interactive example when it materially helps. Do not add a quiz, staged lesson plan, multiple explanations of the same concept, or mandatory analogy unless requested.

Answer the current question completely. File references should help the reader explore next, not substitute for an explanation. Use current runtime delegation rules without a separate orchestration workflow.
