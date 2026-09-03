---
name: teach
description: "Teach a codebase change, subsystem, or design in plain language by combining how it works with repository-backed reasons for its shape. Use when the user wants to understand, learn, or build a working mental model rather than change the code."
license: MIT
---

# Teach

Help the user understand a body of work well enough to reason about it. Explain what it is, how it works, and why it took its current shape. This is a read-only teaching workflow, not authorization to change code.

## Use the installed skills as dependencies

`teach` coordinates `how` and `why`. It does not copy their investigation rules.

Before investigating, use the current Available skills catalog to locate and read the complete `SKILL.md` for each dependency needed by the question. Newly installed skills may not appear in the catalog until a later turn. If one is absent, resolve it from `$CODEX_HOME/skills/<name>/SKILL.md`, or `~/.codex/skills/<name>/SKILL.md` when `CODEX_HOME` is unset. Treat a missing file as an unavailable dependency.

- Use `how` for runtime flow, components, ownership, placement, and architectural mechanics.
- Use `why` for design intent and historical constraints supported by git, hosted PR context, and in-repository evidence.
- Use both for a subsystem, change, or design the user wants to understand as a whole.
- Apply `unslop` during the final edit when it is installed.

Do not reproduce `how` or `why` instructions in this skill or create local copies of their references. Their files are the source of truth. If a dependency is unavailable, say which part could not use its normal workflow, then perform the smallest read-only fallback needed from repository evidence.

## Scope the lesson

Infer the useful depth from the user's question and the conversation. Do not quiz the user before starting.

Choose the few ideas they need to leave with. Someone about to edit the code needs boundaries and invariants. Someone debugging needs the execution path and failure points. Someone onboarding needs the component map and vocabulary.

Use only the dependency work the question needs:

- A narrow mechanism may need `how` only.
- A historical or tradeoff question may need `why` only.
- A broad "teach me this" request usually needs both.

## Coordinate the investigation

Build one shared target and code anchor so `how` and `why` do not rediscover the same scope.

Apply each selected skill faithfully, including its read-only boundary, evidence rules, complexity assessment, model choices, and delegation policy. Do not add another model matrix here.

The lead agent owns the shared Codex concurrency budget. Before any worker batch, use the environment's published limit and `list_agents` to count occupied slots. If no limit is published, use one worker at a time. Do not spawn wrapper agents merely to invoke `how` or `why`. Delegate only the concrete exploration or history tasks those skills call for. Tell each worker whether it may spawn children. Default to no child agents unless the lead reserved capacity and authorized a fixed count. When capacity is tight, batch or sequence the work.

For a small target, the lead may perform both investigations directly. For a complex target, mechanics and history can run in parallel when their assignments are distinct and capacity permits. Otherwise run them sequentially. Reopen the code only to resolve a contradiction, fill a material gap, or verify a citation.

## Teach the result

Start with the smallest complete explanation. Name the thing in plain terms, then tie it to the code in front of the user.

Build outward in this order when each layer helps:

1. What it is and what problem it solves.
2. What happens from trigger to result.
3. Which components and boundaries matter.
4. Why repository evidence says it was built this way.
5. Edge cases, sharp edges, and what remains uncertain.

Explain mechanisms in prose. File names and symbols support the explanation but should not become a changelog. Keep one name for each concept.

Preserve `why`'s evidence discipline. Keep its citations, hedges, competing explanations, and unknowns intact. You may weave them into the lesson, but do not turn "appears to" into "because" or hide an unsearched gap to make the account smoother.

Use a visualization only when it makes a relationship or sequence easier to understand than prose. Prefer the smallest useful diagram. A staged build-up can help with a dense multi-part flow, but do not create several diagrams by rule. Use an image only for a genuinely spatial idea that text or a compact diagram cannot explain well.

Keep the tone conversational without staging a performance. Do not quiz the user, ask them to repeat concepts, print pacing cues, or announce that a section is important or difficult. In an interactive exchange, answer the current question cleanly and leave room for the next one. In a one-shot request, provide the complete lesson at the requested depth.

Return the explanation itself. Do not lead with a report about the investigation or the skills used.
