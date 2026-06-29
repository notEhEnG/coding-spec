---
name: coding-spec
description: Verify spec-to-code alignment, detect drift after implementation, propose living spec updates, and audit the skill package itself. Use when the user asks to check spec drift, validate an implementation against a spec, sync a living document, generate a spec from code, review packaging and triggerability, or ask whether a feature is actually done.
when_to_use: Trigger phrases include "check spec drift", "are we on track", "validate my implementation", "update the spec", "is feature X done?", "sync the living doc", "generate a spec from the code", and "release check". Best for repositories that use spec-driven development, task plans, PRDs, ADRs, acceptance-criteria documents, and portable skill bundles.
argument-hint: [spec-path-or-mode]
arguments: [target]
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash(python *), Bash(git *), Bash(ls *), Bash(find *), Bash(cat *), Bash(sed *), Bash(head *), Bash(tail *), Bash(rg *)
---

# coding-spec

Close the spec-driven development loop by verifying whether the implementation still matches the plan, then propose controlled updates to the living spec.

## Invocation contract

Interpret `$target` using these rules:
- If it is `phase-1`, inspect the package files only and stop after ingest.
- If it is `release-check`, review packaging, prompts, install instructions, and host triggerability.
- If it is a readable file path, treat it as the primary spec.
- If it is `reverse-spec`, infer a spec from the current codebase and docs.
- If it starts with `audit `, treat the remainder as the primary spec path.
- If it starts with `patch `, treat the remainder as the primary spec path and propose spec updates without rewriting the source file.
- If it is empty, search for the best candidate spec in `spec/`, `docs/`, `planning/`, `.claude/`, and repository root.
- If multiple candidate specs exist, present the top candidates and ask for confirmation before final classification.
- If none of the above match, treat the value as a prompt label for a documented launcher flow and report the closest supported mode.

## Output contract

Always produce all three artifacts in the working tree unless the user explicitly asks for a dry run:
- `coding-spec-report.md` — human-readable alignment report.
- `coding-spec-checklist.json` — machine-readable structured checklist.
- `coding-spec-spec-patch.md` — suggested edits to turn the current spec into a living spec.

If the repository is read-only or the user asks not to write files, return the same content inline.

## Classification labels

Classify each requirement into exactly one state:
- **Aligned** — implementation exists and acceptance signals are materially satisfied.
- **Partial** — some implementation exists, but one or more important elements, edges, or validations are missing.
- **Drifted** — the implementation materially differs from the current spec, or the spec claims behavior the code no longer matches.
- **Not Started** — no meaningful implementation evidence was found.
- **Needs Review** — requirement is too ambiguous or non-functional to score reliably without human judgment.

Never upgrade an item to **Aligned** on a single weak signal such as a filename alone.

## Five-phase workflow

### Phase 1 — Ingest
1. Read the primary spec and related planning artifacts.
2. Load `${CLAUDE_SKILL_DIR}/references/sdd-patterns.md` for common SDD document structures.
3. Run `python ${CLAUDE_SKILL_DIR}/scripts/spec-parse.py "$target"` when a concrete spec path is available. If no path is available, identify candidate spec files first.
4. Normalize the spec into a requirement checklist with stable IDs, titles, source excerpts, and acceptance signals.

`spec-parse.py` emits Phase 1 ingest JSON with this envelope:

```json
{
  "source": "path/to/spec.md",
  "parsed_at": "2026-06-29T14:21:53.527889+00:00",
  "groups": ["Authentication / Invitations"],
  "requirements": [
    {
      "id": "authentication-invitations-01",
      "title": "Block duplicate invitations",
      "group": "Authentication / Invitations",
      "source_excerpt": "The system must prevent sending duplicate invitations...",
      "acceptance_signals": ["duplicate case handled"],
      "priority": "unknown",
      "type": "functional"
    }
  ]
}
```

Each object in `requirements` follows the ingest schema in `references/sdd-patterns.md`.
Phase 4 reconciliation produces a separate classified checklist artifact with `status`, `confidence`, and evidence fields.

### Phase 2 — Fingerprint
Build a fast codebase fingerprint before judging requirements.
Collect evidence from:
- Source files, routes, controllers, handlers, services, schemas, migrations, configs.
- Tests, fixtures, snapshots, mocks, and CI workflows.
- README, docs, changelog, ADRs, task lists, TODOs.
- Git metadata when useful, especially recently changed files tied to the feature.

For each requirement, gather evidence with file paths and short excerpts, not vague summaries.

### Phase 3 — Match
Map each requirement to implementation evidence using layered signals:
- Direct names: feature names, route names, function names, config keys, schema fields.
- Semantic matches: synonyms and adjacent terms from the spec.
- Behavioral signals: tests, validation logic, permissions, error handling, telemetry, docs.
- Negative signals: TODOs, skipped tests, dead stubs, mismatched docs, feature flags left off.

Load `${CLAUDE_SKILL_DIR}/references/drift-heuristics.md` before final scoring.

### Phase 4 — Classify
For each requirement, emit:
- `id`
- `title`
- `status`
- `confidence` as `high`, `medium`, or `low`
- `evidence_for`
- `evidence_against`
- `reasoning`
- `recommended_action`

Use conservative judgment.
Prefer **Partial** or **Needs Review** over false certainty.
Mark **Drifted** when the code and spec disagree in a meaningful way, even if the feature is “working”.

### Phase 5 — Reconcile
Create:
1. `coding-spec-report.md` with an executive summary, requirement table, drift hotspots, and next actions.
2. `coding-spec-checklist.json` with the structured results.
3. `coding-spec-spec-patch.md` with concrete edit suggestions, including added decisions, changed behaviors, and stale claims to remove.

If the user asked to update the living spec, propose the patch first. Do not silently rewrite the source spec unless the user explicitly authorizes changes.

## Scope guard

Do not claim exhaustive semantic equivalence.
This skill is a verification aid, not a formal proof system.
Escalate to **Needs Review** when:
- The spec is ambiguous.
- The requirement is mainly UX quality, performance, or security posture without measurable criteria.
- The implementation is spread across generated code or external systems not visible in the repo.
- The repo lacks the tests or artifacts needed to verify behavior.

## Evidence hierarchy

Rank evidence strength roughly in this order:
1. Tests that directly assert the requirement.
2. Concrete implementation plus corroborating docs or config.
3. Concrete implementation alone.
4. Docs or comments alone.
5. Filenames or TODO references alone.

A weak signal alone cannot justify **Aligned**.

## Reverse-spec mode

If invoked as `/coding-spec reverse-spec` or with `$target = reverse-spec`:
- Infer a draft spec from code, tests, routes, schemas, and docs.
- Produce the same three artifacts, but mark all inferred requirements as derived from implementation.
- Call out places where behavior appears intentional but undocumented.

## Suggested slash usage

These explicit invocations should work in tools that map skill directories to slash commands:
- `/coding-spec phase-1`
- `/coding-spec path/to/spec.md`
- `/coding-spec audit path/to/spec.md`
- `/coding-spec patch path/to/spec.md`
- `/coding-spec reverse-spec`
- `/coding-spec release-check`
- `/coding-spec docs/prd.md`

## Supporting files

Use these references when needed:
- `references/sdd-patterns.md` — common spec shapes and how to parse them.
- `references/drift-heuristics.md` — concrete scoring rules for alignment and drift.
- `scripts/spec-parse.py` — parser that converts a spec into Phase 1 ingest JSON (`source`, `parsed_at`, `groups`, `requirements[]`).
