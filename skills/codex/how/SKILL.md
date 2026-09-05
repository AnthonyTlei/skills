---
name: how
description: "Explain how a codebase subsystem works by tracing its implementation. Use for runtime flow, component ownership, placement questions, or an explicitly requested architecture critique."
license: MIT
---

# How

Give the reader a useful mental model grounded in the current code. This is a read-only explanation; it does not authorize implementation or external changes.

## Trace the question

Infer the target from the conversation. For ambiguity that does not change the answer materially, state a brief assumption and proceed.

Locate the entry point and trace the relevant path from trigger through decisions, data movement, and boundaries to observable effect. Read implementations and important consumers, not just names or interfaces. Inspect error, cancellation, persistence, or configuration paths when they affect the explanation.

Stop when the question is answered and the consequential boundaries are understood. Do not map the entire subsystem for a narrow question. Use current runtime rules for delegation; this skill does not request workers or prescribe models, roles, or batches.

## Explain

Lead with what happens. Introduce only the concepts needed to follow it, then connect them to verified files and symbols. Use one representative example when it makes the flow concrete. Cite the important anchors without turning the answer into a file inventory.

Distinguish source-traced behavior from behavior observed in a running system. Name consequential gaps. Use a diagram only if it clarifies relationships better than a short explanation.

## Critique when requested

Explain the existing design before judging it. Read [the critique rubric](references/critique-rubric.md) when a broader architectural assessment is useful.

Retain only concerns with a concrete failure path, demonstrated maintenance cost, or a likely requirement supported by project context. For each, explain the evidence, impact, smallest useful improvement, and tradeoff. Distinguish problems worth fixing from acceptable compromises. Do not manufacture a finding quota or redesign a working subsystem to match a preferred pattern.
