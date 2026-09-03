# Local ticket format

Use this format when publishing tickets inside a project repository.

## Choose the location

Follow an existing project convention when it clearly stores implementation tickets under version control. Otherwise create:

`docs/tickets/<YYYY-MM-DD>-<initiative-slug>/`

Use the current local date. Keep the initiative slug short and specific. A date-prefixed directory makes separate planning passes sortable and prevents unrelated batches from sharing identifiers.

The directory contains:

```text
README.md
T01-<ticket-slug>.md
T02-<ticket-slug>.md
```

Assign identifiers in dependency order. Use two digits until the set exceeds 99 tickets. Identifiers are stable within the ticket set and must not be renumbered after publication.

## Write the set index

Use `README.md` as the entry point:

```markdown
# <Initiative name>

Status: Approved
Created: <YYYY-MM-DD>
Source: <paths, URLs, issue identifiers, or "Conversation">

## Tickets

| ID | Title | Status | Blocked by |
| --- | --- | --- | --- |
| T01 | <Title> | Ready | None |
| T02 | <Title> | Blocked | T01 |

## Dependency order

1. T01 can start immediately.
2. T02 starts after T01.

## Open decisions

- None.
```

List only genuine blockers. Use `Ready` when a ticket can start and `Blocked` when its declared dependencies remain incomplete. Record unresolved product decisions instead of burying them inside a ticket.

## Write each ticket

Use one file per ticket:

```markdown
---
id: T01
title: <Ticket title>
status: ready
blocked_by: []
---

# T01: <Ticket title>

## Outcome

<The narrow result visible to a user, operator, or downstream system.>

## Context

<Why this ticket exists and the verified project anchors needed to start.>

## Scope

- <Included work>
- <Important boundary or explicit exclusion when needed>

## Acceptance criteria

- [ ] <Observable behavior or artifact>
- [ ] <Relevant failure or compatibility condition>

## Verification

- <Command, test, inspection, or evidence required to close the ticket>

## Notes

- <Assumption, decision, or useful implementation constraint, or "None.">
```

Allowed status values are `ready`, `blocked`, `in-progress`, `done`, and `cancelled`. Quote a YAML title when it contains punctuation that YAML could interpret.

Omit an optional section only when it has no useful content. Keep `Outcome`, `Acceptance criteria`, and `Verification` in every ticket.

## Keep the set consistent

Before finishing:

- confirm every index row has one ticket file;
- confirm every `blocked_by` identifier exists;
- confirm the dependency graph has no cycles;
- confirm filenames and frontmatter identifiers agree;
- confirm each acceptance criterion belongs to that ticket's outcome;
- confirm verification can produce evidence for the acceptance criteria.
