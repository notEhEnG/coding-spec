# coding-spec Prompt Checklist

Use this file as the first-paste prompt sheet for `coding-spec` v0.1.0.

## Phase 1 Only

- [ ] Start with the package files in `coding-spec/` only:
  - `SKILL.md`
  - `README.md`
  - `INSTALL.md`
  - `references/sdd-patterns.md`
  - `references/drift-heuristics.md`
  - `scripts/spec-parse.py`
- [ ] Read and normalize the package purpose, audience, and trigger modes.
- [ ] Extract the invocation contract, output contract, and classification model.
- [ ] Build a requirement checklist with stable IDs from the package docs.
- [ ] Capture packaging gaps, ambiguities, and release risks for v0.1.0.
- [ ] Stop after Phase 1.

## Pasteable Prompt

```text
You are reviewing the `coding-spec/` package as a portable SKILL.md bundle.

Start Phase 1 only: ingest and normalize the package before doing any implementation or drift analysis.

Files to read first:
- `coding-spec/SKILL.md`
- `coding-spec/README.md`
- `coding-spec/INSTALL.md`
- `coding-spec/references/sdd-patterns.md`
- `coding-spec/references/drift-heuristics.md`
- `coding-spec/scripts/spec-parse.py`

Your job in Phase 1:
1. Identify the package purpose, intended users, and trigger modes.
2. Extract the invocation contract, output contract, and classification model.
3. Normalize the skill into a requirement checklist with stable IDs.
4. Capture any missing metadata, contradictions, or packaging gaps that would matter for a v0.1.0 release.
5. Summarize the package structure and whether it is internally consistent.

Do not:
- edit any files
- classify code/spec drift yet
- inspect a target repository yet
- proceed past Phase 1
- assume host-specific slash-command support unless the package explicitly states it as conditional

Deliverables:
- a concise Phase 1 summary
- a normalized requirement inventory
- a list of packaging issues or ambiguities
- a clear go/no-go note for v0.1.0 readiness
```

## Short Launcher Prompt

```text
/coding-spec phase-1
Inspect the package files in `coding-spec/`, normalize the skill requirements, and stop after ingest. Report packaging gaps and v0.1.0 readiness, but do not run drift analysis or edit files.
```

## Optional Host Variants

- Claude Code: use the pasteable prompt above, then invoke `/coding-spec phase-1` if your host maps the skill to slash commands.
- Codex: use the pasteable prompt above, then keep the skill directory name `coding-spec` unchanged in your launcher mapping.
- Antigravity: use the pasteable prompt above, then map the folder into `.antigravity/skills/coding-spec/` if your setup supports it.
