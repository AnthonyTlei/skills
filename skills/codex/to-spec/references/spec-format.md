# Specification format

Use this format for local Markdown files and Linear project documents. Keep the section names stable so people and later skills can navigate the document.

## Required structure

```markdown
# <Specification title>

Status: <Draft or Approved>
Created: <YYYY-MM-DD>
Source: <conversation, paths, URLs, or identifiers>
Owner: <name if established, otherwise Unassigned>

## Summary

<The change, who it helps, and the intended result in one short paragraph.>

## Problem

<The observed problem and its effect. Separate evidence from interpretation.>

## Goals

- <Outcome this work must achieve>

## Non-goals

- <Nearby work this specification does not authorize>

## Current state

<Verified behavior, relevant project anchors, and evidence limits.>

## Proposed behavior

<The experience or system behavior after implementation. Cover the normal flow and meaningful failure behavior.>

## Requirements

1. **R1:** <Observable requirement>
2. **R2:** <Observable requirement>

## Technical decisions

### <Decision name>

- Decision: <What was decided>
- Rationale: <Why, using confirmed context or evidence>
- Consequences: <Important tradeoff, compatibility effect, or constraint>

## Verification plan

| Requirement | Seam | Evidence required |
| --- | --- | --- |
| R1 | <Existing test or runtime boundary> | <What must be observed> |

## Acceptance criteria

- [ ] <Observable completion condition tied to a requirement>

## Risks and open questions

- <Risk, assumption, unresolved decision, or "None.">

## References

- <Source path, ADR, issue, document, or URL>
```

For Linear publication, add this metadata line below `Owner`:

`Publication ID: to-spec-publication: <token>`

## Optional sections

Add a section only when it changes implementation or review:

- **Users and scenarios:** include a short numbered list when distinct actors or jobs matter.
- **UX states:** cover loading, empty, error, permission, offline, and accessibility behavior when applicable.
- **Data and contracts:** describe schema, API, file format, cache, event, or migration changes.
- **Security and privacy:** record trust boundaries, sensitive data, permissions, abuse cases, and retention.
- **Compatibility and migration:** define older clients, stored data, rollout order, and rollback behavior.
- **Operations:** define observability, support, recovery, and manual procedures.

Place optional sections after `Requirements` and before `Technical decisions` unless another position reads more naturally.

## Writing rules

- Give each requirement a stable identifier.
- State behavior and constraints, not speculative code structure.
- Include verified paths or symbols only when they help the implementer find current code.
- Keep decisions separate from assumptions and open questions.
- Do not claim production, provider, device, or end-to-end behavior from repository evidence alone.
- Do not duplicate the same fact across sections. Link to its authoritative section.
- Use `Draft` when blocking decisions remain. Use `Approved` only after the user approves the full draft.
- Preserve concise source excerpts only when exact wording is part of the requirement.
