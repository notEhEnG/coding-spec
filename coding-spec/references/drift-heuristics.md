# Drift heuristics

Apply these heuristics conservatively. The goal is honest verification, not optimistic scoring.

## Status rules

### Aligned
Use when all of the following are true:
- There is concrete implementation evidence tied to the requirement.
- No strong contradictory evidence is present.
- Acceptance signals are mostly satisfied.
- At least one corroborating signal exists beyond a filename alone, ideally tests or docs.

### Partial
Use when:
- Core implementation exists, but an edge, permission rule, validation, error path, or acceptance criterion is missing.
- The feature is present but incomplete across surfaces such as UI without backend enforcement, or backend without tests.
- Evidence is mixed but trends toward progress rather than contradiction.

### Drifted
Use when:
- The spec says behavior A, but code clearly implements behavior B.
- The spec claims a feature exists but code removed or renamed it.
- An out-of-scope item was implemented anyway and changes user-visible behavior.
- Docs and code disagree in a way that would mislead maintainers.

### Not Started
Use when:
- No meaningful code, config, docs, or tests support the requirement.
- Only placeholders, TODOs, or issue references exist.

### Needs Review
Use when:
- The requirement is too subjective to verify automatically.
- Key evidence lives outside the repository.
- The wording is too ambiguous for fair classification.
- There is equal strong evidence on both sides and intent is unclear.

## Confidence rules
- **High**: direct implementation plus tests or multiple corroborating artifacts.
- **Medium**: direct implementation with limited corroboration, or partial but clear evidence.
- **Low**: weak or indirect evidence, ambiguity, or inference-heavy matching.

## Contradiction cues
Treat these as potential drift signals:
- Route or API name differs from the spec and behavior also changed.
- Required validation exists in UI only, not server side.
- Schema lacks a field the spec depends on.
- Tests are skipped or stale relative to current code paths.
- Feature flag disables the capability by default despite the spec claiming shipment.
- README or docs promise flows that the code no longer exposes.

## Recommended actions
- **Aligned** → keep spec, maybe add evidence links.
- **Partial** → implement missing edge cases, tests, docs, or enforcement.
- **Drifted** → choose whether code or spec is source of truth, then patch one.
- **Not Started** → create tasks from acceptance signals.
- **Needs Review** → ask owner to clarify measurable criteria.
