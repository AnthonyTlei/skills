---
name: technical-writing
description: "Write or revise developer documentation, RFCs, READMEs, PR descriptions, and commit messages for clarity, accuracy, and global readability. Uses Diátaxis for document purpose and plain technical English for sentences."
---

# Technical writing

Write for a tired engineer who needs to understand the text on the first read. Preserve technical accuracy, uncertainty, citations, and required detail while removing friction.

This skill covers prose. It does not authorize code changes, commits, PR updates, or publishing unless the user asks for those actions.

## Load the editing dependency

When available, apply the installed `unslop` skill during the final edit. Locate it in the current Available skills catalog. If it is absent, check `$CODEX_HOME/skills/unslop/SKILL.md` when `CODEX_HOME` is set, then `~/.codex/skills/unslop/SKILL.md`. Read the complete file before applying it. If it is unavailable, continue with this skill rather than blocking the writing task.

Do not copy or modify `unslop` from this skill. It owns the shared catalog of filler, AI phrasing, and formatting habits.

Technical accuracy, source terminology, user intent, artifact conventions, and calibrated uncertainty take priority over `unslop`. Use `unslop` as a style scan only. It must not add opinions or informality, replace a legitimate technical term, remove a necessary hedge, alter a citation, or change established project language.

Do not stylistically rewrite verbatim quotations, code blocks, commands, program output, error messages, structured metadata, generated content, or text whose exact form is under discussion. Preserve the repository's punctuation and formatting conventions when they are intentional requirements.

## Preserve truth before improving style

Establish the audience, task, source material, and requested output format. Keep the user's terminology when it names a real product concept. Use the codebase's exact symbols, files, flags, commands, error strings, and configuration names.

Do not invent behavior, smooth over uncertainty, or turn a plan into an implemented fact. Verify source-code facts such as paths, symbols, commands, defaults, and generated trees against the current repository when one is provided. A repository does not prove current production state, observed test results, release status, or an external API's behavior. Support those claims with current user-provided or authoritative evidence, or keep them qualified.

Preserve unrelated wording in a focused edit. Do not rewrite the whole document merely to impose a preferred voice.

## Pick the document's primary mode

Use Diátaxis to decide what the reader needs. Choose one primary mode for a page or clearly bounded section. Split and link when different reader needs would fight each other.

- Tutorial. Help a learner build something through a safe sequence. State the outcome, give early visible results, and tell the reader what they should observe.
- How-to. Help a competent reader complete a real task. Start from the goal, keep background brief, and include conditional branches where judgment matters.
- Reference. Provide facts for lookup. Mirror the structure of the interface or system. State options, defaults, limits, errors, and compatibility precisely.
- Explanation. Help the reader understand a bounded concept, decision, or tradeoff. Context and reasoned judgment belong here.

Do not force every artifact into Diátaxis. PR descriptions, commit messages, short release notes, and decision records have their own established structures.

## Organize for the reader

Lead with the information needed to decide or act. Put the common path before exceptions. Put a condition or warning before the instruction it controls.

Use headings that carry meaning. Use sentence case. Use a verb phrase for a task heading and a noun phrase for a concept heading. Keep one level-one heading and do not skip heading levels.

Use numbered lists for sequences and bullets for unordered sets. Introduce each list with a complete sentence. Keep list items grammatically parallel.

Use links whose text names the destination. Add enough local context that the reader can decide whether to follow the link.

## Write plain technical sentences

- Address the reader as "you" when appropriate. Use present tense for current behavior.
- Name the actor and action. Prefer "the compiler validates the schema" to "the schema is validated."
- Write procedures as commands. Prefer "Run `make verify`" to "You should run `make verify`."
- Give one instruction per sentence. Keep one main thought per sentence.
- Split sentences that require the reader to backtrack. Treat 20 words for instructions and 25 words for other prose as review signals, not hard limits.
- Use the short everyday word when it is equally precise.
- Give each concept one name and keep it. Do not rotate synonyms for variety.
- Put modifiers such as "only" and "not" next to the word they change.
- Make pronouns point to one obvious noun. Repeat the noun when ambiguity remains.
- Break up long noun strings. Write "the script that checks the import budget" instead of "the import budget check script."
- Keep articles, conjunctions, and verbs when they prevent two readings.
- Avoid slashes, semicolons, unexplained idioms, and culture-specific metaphors.
- Use active voice by default. Use passive voice when the actor is unknown or irrelevant.
- Do not call a task easy, simple, quick, or obvious.

These rules borrow practical ideas from Google developer style, ASD Simplified Technical English, and Global English. They improve clarity but do not claim formal compliance with those standards.

## Match the artifact

Tutorials should produce visible progress. Keep conceptual detours short and link to explanation or reference material.

How-to guides should solve the reader's goal. Do not add teaching steps or exhaustive reference material unless the task requires them.

Reference pages should be complete for their declared scope. Preserve necessary uncertainty and version boundaries instead of sounding certain when the source is not.

Explanations may compare alternatives and state a reasoned view. Separate documented facts from interpretation.

For RFCs and decision records, distinguish context, goals, non-goals, options, decision, consequences, risks, and unresolved questions. Do not present a proposal as approved.

For PR descriptions, state the problem, the change, meaningful risks, and verification. Keep claims bounded to the diff and observed results.

For commit messages, write a concise imperative subject and use the body for motivation or non-obvious constraints. Do not repeat the diff line by line.

For code examples, preserve the repository's formatter and indentation style. Use real commands and safe placeholders. Show expected output when it helps the reader confirm success.

Product UI text is outside this skill unless the user explicitly asks to apply documentation style to it.

## Review the result

Check the final text:

1. Does the structure match the reader's job?
2. Is every technical claim supported by the right evidence type: repository source for code facts, observed results for execution claims, and current authoritative evidence for external or operational facts?
3. Does each instruction name one action and put its condition first?
4. Can any sentence be read in two ways?
5. Does each concept keep one name?
6. Can any word, heading, list, or paragraph be removed without losing meaning?
7. Are commands, symbols, paths, defaults, counts, and expected results exact?
8. Did the edit preserve uncertainty, authorization boundaries, and content outside the requested scope?

Return the finished or revised prose. When reviewing without a requested rewrite, return concrete findings and suggested corrections instead of silently replacing the document.
