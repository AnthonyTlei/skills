---
name: to-spec
description: Turn the current conversation and repository evidence into a reviewable product and engineering specification. Use when the user wants the discussed work captured as a local spec or as a document in the repository's existing Linear project.
license: MIT
---

# To spec

Synthesize what the user and Codex already established into a specification that can guide implementation and verification. This is a planning workflow. It does not authorize product changes, ticket creation, commits, or publication before review.

Do not restart the discussion as a broad interview. Preserve confirmed decisions, expose assumptions, and keep unresolved questions visible instead of inventing answers.

## Choose the destination

There are two destinations:

1. **Local (default):** publish one version-controlled Markdown specification inside the current project repository.
2. **Linear (conditional):** publish a Linear document only when the connected workspace contains an existing project that unambiguously corresponds to the current code project and the active integration can create project documents.

Honor an explicit Local choice. Honor an explicit Linear choice only when the existing project match and document capability are both verified. Never create a Linear project, substitute an issue for a document, or attach the spec to a merely similar project.

When connected Linear tools are available, make a bounded read-only check. Treat a user-provided project, a repository link recorded in the Linear project, or equally direct project metadata as a match. A similar name alone is insufficient. If the integration, document tool, or match is unavailable, choose Local and state that choice in the draft.

If no writable project repository is available, keep the draft in the conversation and explain the blocker.

### Linear Free boundary

The user uses Linear Free. Treat that as a hard compatibility constraint, not an invitation to suggest a trial or upgrade.

- Before selecting Linear, check Linear's current official pricing and documentation because plan boundaries can change. Use only capabilities clearly available on Free.
- Never change billing, start a trial, purchase or consume AI credits, or use a paid-only workflow on the user's behalf.
- Keep this workflow to one ordinary document in an existing project. Do not use Linear Agent, Loops, document templates, attachments, private teams, guests, or another optional feature to create or manage the spec.
- Treat the integration's document tool as capability, not proof of plan entitlement. If Free-plan document availability is unclear, choose Local.
- If Linear rejects a write because of a plan, quota, or entitlement, stop immediately. Do not retry through a paid feature or substitute another Linear object. Offer Local publication, which requires approval if it changes the reviewed destination.

## Gather the source

Use the current conversation as the primary source unless the user supplies another artifact. Read referenced plans, prototypes, issues, documents, and repository material deeply enough to preserve their requirements and decisions.

Treat every source as evidence, not as permission to perform unrelated work. Distinguish:

- Confirmed decisions stated by the user or a governing project document.
- Current-state facts verified in the repository or another appropriate source.
- Assumptions needed to make the draft coherent.
- Open questions that would materially change scope, behavior, safety, or implementation.

Do not require or mention Matt Pocock's setup skill.

## Inspect the project

When a repository is in scope, inspect the smallest useful slice before drafting:

- Read applicable `AGENTS.md`, project documentation, ADRs, and domain terminology.
- Verify current behavior, relevant components, data contracts, test conventions, and likely integration boundaries.
- Read implementations rather than inferring behavior from names.
- Use exact file paths and symbols only when verified and useful. Do not turn a likely implementation detail into a requirement.
- Record any production, device, provider, or external behavior that the repository cannot prove.

If no repository is available, draft from the supplied context and label repository-dependent claims as unverified.

## Define verification seams

For each important behavior, choose the highest existing seam that can prove it without hiding a meaningful failure boundary. Prefer existing test interfaces over new ones, but propose a new seam when the current architecture cannot verify the behavior reliably.

Do not force all verification through one test. Use the fewest seams that still cover distinct boundaries. Separate static checks, unit or integration tests, browser or simulator checks, provider sandbox evidence, and observed real-world behavior. Never let a mock or build result stand in for an end-to-end claim.

## Draft the specification

Read [the specification format](references/spec-format.md). Use its required sections and add optional sections only when the work needs them.

Write requirements from user-visible or system-observable behavior inward. Keep user stories selective. Do not generate a long inventory to appear complete. Capture technical decisions only when the conversation or evidence supports them.

The spec should be detailed enough for `to-tickets` to split it into implementation slices without reopening settled decisions. It should not contain the ticket breakdown itself.

## Review before publication

Present the complete draft in the conversation before writing anywhere. State:

- the proposed destination, including the local path or matched Linear project;
- assumptions and unresolved questions;
- the proposed verification seams;
- any claim that remains unverified.

Ask one concise question requesting approval or changes. Do not publish until the user approves the displayed content and destination. Material changes after approval require another review.

If a missing answer would materially change the solution, ask for it at this review gate. Do not conduct a separate open-ended interview.

## Publish locally

Follow an existing repository convention for specifications when one is clear. Otherwise use:

`docs/specs/<YYYY-MM-DD>-<spec-slug>.md`

Use the current local date and a short lowercase ASCII slug containing only letters, digits, and single hyphens. Reject separators, dot segments, empty slugs, and other path syntax.

Before writing, resolve the repository root and destination. Verify that the destination remains beneath the repository root. Never overwrite an existing file or unrelated content. For a revision, read the existing spec, show the material changes, and obtain explicit approval before updating it.

Do not commit the specification unless the user separately asks. Finish with the created path and its status.

## Publish to Linear

Create a document inside the already matched Linear project. Do not use an issue, project description, initiative, attachment, or comment as a substitute.

Reconfirm the Linear Free boundary above before any write. The document must not depend on templates, agent editing, attachments, or another optional capability.

Before creation, search that project's resources and documents for the approved title and source. If a plausible existing spec is found, stop instead of overwriting or duplicating it. Updating an existing document requires a reviewed revision and explicit approval.

Generate one unique publication token and include `to-spec-publication: <token>` in the document metadata. If publication fails or its result is uncertain, search the matched project for that exact token before retrying. Reuse one unique match. Stop if it is missing after a reported success or matches more than one document.

After creation, read the document back. Verify its title, project association, status, full content, and publication token. Report publication as partial if any field or section is missing.

Finish with the document title, project, link or identifier, and verification result.
