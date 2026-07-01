# coding-spec (auditing skill)

Portable `SKILL.md` workflow for spec drift detection, implementation verification, and living spec updates in spec-driven development.

Claude Code, Antigravity IDE, and Codex-compatible loaders can all use this package when they support the `SKILL.md` skill format.

## Relationship to the toolkit

This repository is a monorepo:

| Package | Location | Purpose |
|---|---|---|
| **Toolkit CLI** | repo root (`bin/coding-spec`) | Scaffold specs and plans *before* coding |
| **Auditing skill** | this folder (`coding-spec/`) | Verify code matches specs *after* coding |

For toolkit quickstart, see the [root README](../README.md).

## Why this skill exists

Most spec-driven workflows stop at plan and implement. Teams still need a practical way to check whether the code actually matches the spec after changes land. This skill reads a spec, inspects the codebase, classifies each requirement, and proposes controlled updates to keep documentation current.

## What it does

- Parses Markdown specs into a structured checklist with stable IDs.
- Scans a repository for evidence across code, tests, schemas, configs, and docs.
- Classifies each requirement as `Aligned`, `Partial`, `Drifted`, `Not Started`, or `Needs Review`.
- Produces a report, machine-readable checklist, and proposed spec patch.
- Supports slash-style invocation such as `/coding-spec docs/prd.md` in compatible agent tools.

## Package contents

```text
coding-spec/
├── SKILL.md              # canonical launcher and workflow
├── README.md
├── INSTALL.md
├── LICENSE
├── references/
│   ├── sdd-patterns.md
│   └── drift-heuristics.md
└── scripts/
    ├── spec-parse.py
    ├── test_spec_parse.py
    └── fixtures/
        ├── acceptance_section.md
        ├── checklist_atomic.md
        ├── compound_narrative.md
        ├── false_positive_willow.md
        └── non_goal_section.md
```

## Install

Copy this **`coding-spec/` subfolder** into your agent's skill directory. See [INSTALL.md](INSTALL.md) for host-specific paths.

### Claude Code

```text
Hey Claude, help me install this skill https://github.com/notEhEnG/coding-spec
```

Manual target: `.claude/skills/coding-spec/SKILL.md`

### Antigravity IDE

```text
Hey Antigravity, help me install this skill https://github.com/notEhEnG/coding-spec
```

Manual target: `.antigravity/skills/coding-spec/SKILL.md`

### Codex-compatible loaders

```text
Hey Codex, help me install this skill https://github.com/notEhEnG/coding-spec
```

Manual target: `<your-skill-dir>/coding-spec/SKILL.md` — preserve the folder name `coding-spec`.

## Usage

`SKILL.md` is the single source of truth for commands and workflow. Common invocations:

- `/coding-spec phase-1` — ingest and normalize only
- `/coding-spec path/to/spec.md` — full audit against a spec file
- `/coding-spec audit path/to/spec.md` — explicit audit mode
- `/coding-spec patch path/to/spec.md` — propose spec updates without rewriting the source
- `/coding-spec reverse-spec` — infer requirements from implementation
- `/coding-spec release-check` — validate packaging and install instructions

When slash commands are unavailable, ask your agent to follow the five-phase workflow in `SKILL.md`.

### Good trigger phrases

- check spec drift
- validate my implementation
- are we on track
- update the spec
- sync the living doc
- is feature X done?
- generate a spec from the code

## Workflow

1. **Ingest** — read the primary spec and normalize requirements.
2. **Fingerprint** — inspect repo structure, code, tests, configs, and docs.
3. **Match** — connect requirements to implementation evidence.
4. **Classify** — score each requirement conservatively.
5. **Reconcile** — generate a report and proposed spec updates.

## Output artifacts

By default, the skill produces:

- `coding-spec-report.md`
- `coding-spec-checklist.json`
- `coding-spec-spec-patch.md`

## Classification model

| Status | Meaning |
|---|---|
| `Aligned` | Implementation and supporting evidence materially satisfy the requirement. |
| `Partial` | Some implementation exists, but important behavior, validation, tests, or coverage is incomplete. |
| `Drifted` | Code and spec materially disagree, or the documented behavior is no longer true. |
| `Not Started` | No meaningful implementation evidence was found. |
| `Needs Review` | The requirement is too ambiguous or external to verify reliably. |

## Reverse-spec mode

`/coding-spec reverse-spec` infers a draft living spec from the current codebase when the original planning document is missing, stale, or incomplete.

## Limitations

This is a verification aid, not a formal proof system. It works best when the repository includes clear specs, tests, and implementation artifacts, and falls back to `Needs Review` when requirements are subjective or depend on systems outside the visible repository.