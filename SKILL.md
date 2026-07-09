---
name: coding-spec
description: Spec-first development toolkit and auditor. Scaffold a workspace, draft a feature spec, turn it into a technical plan, gate specs for completeness, export an agent brief, score spec-to-code health, and catalog every spec — then audit an implementation for drift against its spec. Use when the user wants to plan a feature before coding, generate/validate a spec, review or grade an implementation, or check whether a feature is actually done.
when_to_use: Trigger phrases include "start a spec", "scaffold a spec", "write a spec for X", "turn this spec into a plan", "validate my spec", "is this spec complete", "export this spec for an agent", "score this feature", "catalog our specs", "add a CI spec gate", plus the audit phrases "check spec drift", "are we on track", "validate my implementation against the spec", "is feature X done", and "generate a spec from the code".
argument-hint: "<command | spec-path | audit mode> [args]"
arguments: [target]
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(python *), Bash(python3 *), Bash(./bin/coding-spec *), Bash(bin/coding-spec *), Bash(git *), Bash(ls *), Bash(find *), Bash(cat *), Bash(sed *), Bash(head *), Bash(tail *), Bash(rg *)
---

# coding-spec

A spec-first workflow in one skill. It has **two halves**:

1. **Toolkit CLI** — scaffold and manage spec artifacts *before* you code.
2. **Auditor** — verify the implementation still matches the spec *after* you code.

`/coding-spec <arg>` dispatches to the right half based on the first token.

## Skill directory & CLI location

This skill is the whole repository. The toolkit CLI lives beside this file at
`src/cli.py` (launcher: `bin/coding-spec`), and the auditor's references/parser
live under `coding-spec/`. Resolve the skill root once, then reuse it:

```bash
# The directory containing this SKILL.md. Claude Code exposes $CLAUDE_SKILL_DIR;
# otherwise fall back to the folder this file is installed in.
SKILL_DIR="${CLAUDE_SKILL_DIR:-$(cd "$(dirname "$0")" && pwd)}"
CS="python3 $SKILL_DIR/src/cli.py"      # the toolkit CLI
```

The CLI self-locates its templates and always operates on the **current working
directory** (the user's project) unless a `--dir` is given, so run it from the
user's project root.

## Dispatch contract

Read the first whitespace-delimited token of `$target`:

### A. Toolkit commands → run the CLI

If the first token is one of `init`, `spec`, `plan`, `validate`, `review`,
`export`, `ci`, `score`, `catalog`, run the CLI and report its output:

```bash
$CS <token> <remaining-args>
```

| Invocation | What it does |
|---|---|
| `/coding-spec init` | Scaffold `docs/`, `templates/`, etc. into the project. |
| `/coding-spec spec "Add team billing"` | Draft `docs/specs/<slug>.md` from the template. |
| `/coding-spec validate docs/specs/<slug>.md` | Gate one spec for completeness (exit 1 on errors). |
| `/coding-spec validate --all` | Gate **every** spec under `docs/specs` (CI gate). |
| `/coding-spec plan docs/specs/<slug>.md` | Generate a technical plan. |
| `/coding-spec review docs/specs/<slug>.md` | Checklist matching criteria to code evidence. |
| `/coding-spec export docs/specs/<slug>.md --format claude` | Bundle an agent brief (`markdown`/`claude`/`cursor`/`agents`). |
| `/coding-spec score docs/specs/<slug>.md` | Grade spec-to-code health (A–F). |
| `/coding-spec catalog` | Index every spec with status + grade. |
| `/coding-spec ci` | Generate a GitHub Actions spec-gate workflow. |

After running, surface the CLI's printed output and the path(s) it wrote. If the
project has no `docs/` yet and the user asked for `spec`/`plan`/etc., run
`$CS init` first (ask if that side effect is unexpected).

### B. Auditing modes → follow the auditor workflow

If the first token is `audit`, `patch`, `reverse-spec`, `release-check`,
`phase-1`, or a path to an existing spec file (i.e. **not** a toolkit command),
this is an audit request. Follow the full auditor workflow documented in
[`coding-spec/SKILL.md`](coding-spec/SKILL.md): ingest → fingerprint → match →
classify → reconcile, producing `coding-spec-report.md`,
`coding-spec-checklist.json`, and `coding-spec-spec-patch.md`. Use
`$SKILL_DIR/coding-spec/references/*.md` for heuristics and
`python3 $SKILL_DIR/coding-spec/scripts/spec-parse.py <spec>` to parse the spec.

Summary of audit routing (see that file for the contract in full):
- `audit <spec>` / `<spec-path>` — classify each requirement Aligned / Partial / Drifted / Not Started / Needs Review.
- `patch <spec>` — same analysis, but only propose living-spec edits; never rewrite the source spec without explicit consent.
- `reverse-spec` — infer a draft spec from the code, tests, and docs.
- `release-check` — review packaging, prompts, install instructions, and triggerability.

### C. Ambiguous / empty

If `$target` is empty, ask whether the user wants to **scaffold** (toolkit) or
**audit** (auditor), and offer the most likely command. Never guess destructive
actions.

## Typical end-to-end flow

```text
/coding-spec init
/coding-spec spec "Add team billing"
/coding-spec validate docs/specs/add-team-billing.md
/coding-spec plan docs/specs/add-team-billing.md
# …implement…
/coding-spec review docs/specs/add-team-billing.md
/coding-spec score docs/specs/add-team-billing.md
/coding-spec audit docs/specs/add-team-billing.md
```

## Scope guard

The `validate`, `review`, `score`, and `catalog` outputs are heuristic aids for
human judgement, not proofs of correctness. The auditor never upgrades an item to
**Aligned** on a weak signal (a filename alone), and escalates ambiguous or
non-functional requirements to **Needs Review**.
