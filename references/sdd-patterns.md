# SDD patterns reference

Use this file to normalize common spec formats into the same requirement checklist.

## Common source documents
- PRD or product requirement doc.
- Feature spec in Markdown.
- ADR with acceptance criteria.
- Task plan with checklists.
- Issue or epic description.
- Reverse-engineered notes from a shipped feature.

## Parsing rules

### 1. Headings become requirement groups
Treat H1/H2/H3 headings as grouping structure, not automatically as requirements.
A heading becomes a requirement only when it states an expected capability or constraint.

### 2. Checklist items are usually requirements or subrequirements
Examples:
- `- [ ] User can export a CSV`
- `- [ ] Block duplicate invitations`

Assign stable IDs by section path plus ordinal.

### 3. Acceptance criteria lines are strong requirement signals
Look for phrases such as:
- Acceptance Criteria
- Done when
- Success criteria
- Expected behavior
- Must / should / shall

Split compound bullets into separate atomic requirements when possible.

### 4. Narrative paragraphs can contain hidden requirements
Extract statements that describe:
- User-visible behaviors
- Data constraints
- Permissions and roles
- Validation rules
- Error handling
- Performance thresholds
- Integration behavior

### 5. Decisions and exclusions matter
Capture explicit non-goals and out-of-scope statements because code that implements excluded behavior may indicate drift.

## Stable schema
Each parsed item should fit this shape:

```json
{
  "id": "auth-03",
  "title": "Block duplicate invitations",
  "group": "Authentication / Invitations",
  "source_excerpt": "The system must prevent sending duplicate invitations to the same email while one is pending.",
  "acceptance_signals": [
    "duplicate pending invitation rejected",
    "error surfaced to caller",
    "test covers duplicate case"
  ],
  "priority": "unknown",
  "type": "functional"
}
```

## Heuristic cues
- Strong verbs: must, shall, should, prevents, allows, rejects, records, displays.
- Data cues: schema, field, column, enum, payload, validation, migration.
- UX cues: button, screen, modal, page, prompt, toast, empty state.
- Operational cues: cron, queue, retry, audit log, alert, timeout.

## Ambiguity handling
If a line is aspirational but not testable, keep it as a requirement with `type: ambiguous` and expect later classification to fall back to `Needs Review` unless stronger measurable criteria are found.
