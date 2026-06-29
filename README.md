# coding-spec

Portable `SKILL.md` workflow for spec drift detection, implementation verification, and living spec updates in spec-driven development. Claude Code supports extensible skills via `SKILL.md`, and Antigravity IDE uses the same skill format in `.antigravity/skills/`, which makes this package suitable for cross-tool agent workflows.[cite:27][cite:20]

## Why it exists

Most spec-driven workflows stop at plan and implement, but teams still need a practical way to check whether the code actually matches the spec after changes land. `coding-spec` adds that missing verification layer by reading a spec, inspecting the codebase, classifying each requirement, and proposing controlled updates to keep documentation current.[cite:27][cite:20]

## What it does

- Parses Markdown-style specs into a structured checklist with stable IDs.
- Scans a repository for evidence across code, tests, schemas, configs, and docs.
- Classifies each requirement as `Aligned`, `Partial`, `Drifted`, `Not Started`, or `Needs Review`.
- Produces a report, machine-readable checklist, and proposed spec patch.
- Supports explicit slash-style invocation such as `/coding-spec docs/prd.md` in compatible skill-driven agent tools.[cite:27][cite:20][cite:60]

## Package contents

```text
coding-spec/
├── SKILL.md
├── README.md
├── INSTALL.md
├── references/
│   ├── sdd-patterns.md
│   └── drift-heuristics.md
└── scripts/
    └── spec-parse.py
```

Each skill is typically organized as a folder containing `SKILL.md` plus optional `scripts/` and `references/`, which matches common Claude Code skill packaging patterns.[cite:27][cite:65]

## Install

### Claude Code

**Easiest install:** open Claude Code in your project and paste the repo link. Claude can clone or copy the skill for you:

```text
Hey Claude, help me install this skill https://github.com/notEhEnG/coding-spec
```

Claude should place the package at `.claude/skills/coding-spec/SKILL.md` so you can invoke it as `/coding-spec`.

**Manual install:** copy the folder into `.claude/skills/coding-spec/` so the main file ends up at `.claude/skills/coding-spec/SKILL.md`. Claude Code documents skills as reusable extensions defined by `SKILL.md`, and community guides describe them as directly invocable slash commands using the skill name.[cite:27][cite:50]

### Antigravity IDE

**Easiest install:** open Antigravity in your project and paste the repo link. The agent can clone or copy the skill for you:

```text
Hey Antigravity, help me install this skill https://github.com/notEhEnG/coding-spec
```

Antigravity should place the package at `.antigravity/skills/coding-spec/SKILL.md` so you can invoke it as `/coding-spec` or assign it to an agent in Manager View.

**Manual install:** copy the folder into `.antigravity/skills/coding-spec/`. Antigravity guides describe `.antigravity/skills/` as the project-level location for portable `SKILL.md` skills, with the same format reused across compatible agent tools.[cite:20]

### Codex-compatible loaders

**Easiest install:** open your Codex-compatible agent in the project and paste the repo link. The agent can clone or copy the skill for you:

```text
Hey Codex, help me install this skill https://github.com/notEhEnG/coding-spec
```

Codex should place the folder in the skill directory your environment watches, keeping the directory name `coding-spec` unchanged so `/coding-spec` remains stable across tools.

**Manual install:** place the same folder into the skill directory used by your Codex-compatible wrapper or launcher, keeping the directory name `coding-spec` unchanged so the command identity remains stable across tools.[cite:22]

## Usage

### Explicit commands

```bash
/coding-spec phase-1
/coding-spec docs/prd.md
/coding-spec specs/export-flow.md
/coding-spec audit docs/prd.md
/coding-spec patch docs/prd.md
/coding-spec reverse-spec
/coding-spec release-check
```

Claude Code skill docs describe `name` and `description` as core skill metadata, and cross-tool explainers note that the skill name is used as the direct invocation identifier in slash-style workflows.[cite:27][cite:60]

### Without slash commands

When slash commands are unavailable, ask your agent to follow the five-phase workflow in `SKILL.md`. See `INSTALL.md` for host-specific install paths and trigger phrases.

### Good trigger phrases

- check spec drift
- validate my implementation
- are we on track
- update the spec
- sync the living doc
- is feature X done?
- generate a spec from the code

## Workflow

`coding-spec` follows a five-phase workflow:

1. **Ingest** — read the primary spec and normalize requirements.
2. **Fingerprint** — inspect repo structure, code, tests, configs, and docs.
3. **Match** — connect requirements to implementation evidence.
4. **Classify** — score each requirement conservatively.
5. **Reconcile** — generate a report and proposed spec updates.

This structure is implemented in the shipped `SKILL.md`, `references/`, and parser script so the agent has both instructions and reusable heuristics in one portable package.[cite:27][cite:65]

## Output artifacts

By default, the skill is designed to produce:

- `coding-spec-report.md`
- `coding-spec-checklist.json`
- `coding-spec-spec-patch.md`

These outputs separate the human-readable audit, the structured machine-readable checklist, and the proposed documentation changes into distinct artifacts for review.[cite:27]

## Classification model

Each requirement is assigned one of five states:

| Status | Meaning |
|---|---|
| `Aligned` | Implementation and supporting evidence materially satisfy the requirement. |
| `Partial` | Some implementation exists, but important behavior, validation, tests, or coverage is incomplete. |
| `Drifted` | Code and spec materially disagree, or the documented behavior is no longer true. |
| `Not Started` | No meaningful implementation evidence was found. |
| `Needs Review` | The requirement is too ambiguous or external to verify reliably. |

The skill uses conservative scoring so weak signals such as filenames alone do not justify a strong alignment claim.[cite:27]

## Reverse-spec mode

`/coding-spec reverse-spec` infers a draft living spec from the current codebase, tests, routes, schemas, and docs instead of starting from an existing spec file. This is useful when code exists but the original planning document is missing, stale, or incomplete.[cite:27]

## Limitations

`coding-spec` is a verification aid, not a formal proof system. It works best when the repository includes reasonably clear specs, tests, and implementation artifacts, and it should fall back to `Needs Review` when requirements are subjective, underspecified, or depend on systems outside the visible repository.[cite:27][cite:20]

## Roadmap ideas

- Add a repo scanner that automatically writes the output artifacts.
- Add adapters for PRD templates, ADRs, and issue-based specs.
- Add test-fixture repos for regression checks.
- Add stricter evidence scoring for security and performance requirements.
