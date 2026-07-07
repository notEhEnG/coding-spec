# coding-spec

coding-spec is a lightweight, opinionated toolkit for building software with specs before code. It gives developers a clean workflow for turning rough ideas into implementation-ready artifacts: product specs, technical plans, task lists, and review checklists. The goal is simple — reduce vague prompts, improve AI coding output, and make feature work easier to review, test, and ship.

This repository is a **monorepo** with two packages:

1. **Toolkit CLI** (repo root) — scaffold specs and plans before you code.
2. **Auditing skill** ([`coding-spec/`](coding-spec/)) — verify implementation matches the spec after you code.

## Why this exists

AI coding tools are fast, but they produce uneven results when requirements are vague. Spec-driven workflows make the specification the source of truth before implementation begins.

## What the toolkit does

- Scaffolds a markdown-first project workspace (`init`)
- Generates a feature spec from a short prompt (`spec`)
- Converts an approved spec into a technical plan (`plan`)
- Checks a spec for completeness — acceptance criteria, tests, scope (`validate`)
- Generates a review checklist that matches spec criteria to code evidence (`review`)
- Ships canonical templates for specs, plans, tasks, and reviews
- Includes a full end-to-end demo in `examples/feature-team-billing/`

## Quickstart (toolkit CLI)

```bash
# From the repository root
chmod +x bin/coding-spec

./bin/coding-spec init                                        # scaffold the workspace
./bin/coding-spec spec "Add team billing"                     # draft a spec from a prompt
./bin/coding-spec validate docs/specs/add-team-billing.md     # gate the spec for completeness
./bin/coding-spec plan docs/specs/add-team-billing.md         # turn the spec into a plan
./bin/coding-spec review docs/specs/add-team-billing.md       # check code against the spec
```

A new user can complete init → spec → plan in under ten minutes; `validate` and `review` add a trust gate on either side of implementation.

## Command reference

| Command | Input | Produces / checks | Exit code |
|---|---|---|---|
| `init [--dir DIR]` | — | Creates `docs/`, `templates/`, `examples/`, `prompts/`, `src/`, `tests/` and copies the canonical templates. | `0` |
| `spec "<prompt>" [--dir DIR]` | a short title | `docs/specs/<slug>.md` from the spec template. | `0` |
| `validate <spec.md>` | a spec file | Static completeness check (see below). Prints errors/warnings. | `1` if any error, else `0` |
| `plan <spec.md> [--dir DIR]` | an approved spec | `docs/plans/<slug>-plan.md` from the plan template. | `0` |
| `review <spec.md> [--dir DIR]` | a spec file | `docs/plans/<slug>-review.md` — each acceptance criterion paired with matching code evidence found in the tree. | `0` |

**What `validate` checks** (headings are matched case-insensitively and tolerate a numbered prefix such as `## 3. Acceptance Criteria`):

- **Error** — no *Acceptance Criteria* section, or the section has no list items ("under-specified criteria").
- **Error** — no *Test Considerations* / *Testing* / *Test Plan* / *QA* section.
- **Warning** — no *Non-Goals* / *Out of Scope* section (recommended to prevent scope drift).

Because `validate` returns a non-zero exit code on errors, you can wire it into a pre-commit hook or CI step to block specs that are not implementation-ready.

**What `review` produces** — it extracts each acceptance criterion, then keyword-scans the repository's `.py`/`.md` files (skipping caches, VCS, and vendored dirs) for evidence, marking every criterion `[x]` (evidence found, with file names) or `[ ]` (none). Treat it as a heuristic aid for a human reviewer, not a proof of correctness.

## Agent skill (Claude Code, Antigravity, Codex)

The [`coding-spec/`](coding-spec/) folder is a portable `SKILL.md` package for spec-drift auditing. It works across agent tools that support the skill format.

**Important:** copy the **`coding-spec/` subfolder**, not the whole repository.

### Claude Code

```bash
git clone https://github.com/notEhEnG/coding-spec.git /tmp/coding-spec-repo
mkdir -p .claude/skills
cp -r /tmp/coding-spec-repo/coding-spec/ .claude/skills/coding-spec/
```

Or ask Claude Code directly:

```text
Hey Claude, help me install this skill https://github.com/notEhEnG/coding-spec
```

Install target: `.claude/skills/coding-spec/SKILL.md`  
Invoke: `/coding-spec docs/prd.md`, `/coding-spec audit path/to/spec.md`, `/coding-spec reverse-spec`

### Antigravity IDE

```bash
git clone https://github.com/notEhEnG/coding-spec.git /tmp/coding-spec-repo
mkdir -p .antigravity/skills
cp -r /tmp/coding-spec-repo/coding-spec/ .antigravity/skills/coding-spec/
```

Or ask Antigravity:

```text
Hey Antigravity, help me install this skill https://github.com/notEhEnG/coding-spec
```

Install target: `.antigravity/skills/coding-spec/SKILL.md`  
Invoke: `/coding-spec` or assign the skill to an agent in Manager View.

### Codex-compatible loaders

```bash
git clone https://github.com/notEhEnG/coding-spec.git /tmp/coding-spec-repo
cp -r /tmp/coding-spec-repo/coding-spec/ <your-codex-skill-directory>/coding-spec/
```

Keep the folder name `coding-spec` so slash-command identity stays stable across tools.

Full install paths, trigger phrases, and command reference: [`coding-spec/INSTALL.md`](coding-spec/INSTALL.md) and [`coding-spec/SKILL.md`](coding-spec/SKILL.md).

## Repository layout

```text
coding-spec/                 # monorepo root
├── README.md
├── LICENSE
├── bin/coding-spec          # toolkit CLI launcher
├── docs/                    # philosophy, workflow, FAQ
├── templates/               # canonical markdown templates
├── examples/                # end-to-end demo features
├── prompts/                 # reusable agent prompt packs
├── src/                     # toolkit CLI implementation
├── tests/
└── coding-spec/             # portable auditing skill (install separately)
    ├── SKILL.md
    ├── INSTALL.md
    ├── references/
    └── scripts/
```

## Project status & roadmap

The toolkit is built in phases; each phase is only marked shipped once its commands and tests are on `main`.

| Phase | Theme | Scope | Status |
|---|---|---|---|
| **Phase 1** | Make it real | `init`, `spec`, `plan`; canonical templates; end-to-end demo | ✅ Shipped |
| **Phase 2** | Add trust | `validate` (spec completeness gate), `review` (spec-to-code checklist), snapshot tests | ✅ Shipped |
| **Phase 3** | Automate | Agent export modes and CI integration (e.g. `validate` as a required check) | 🔜 Planned |

**What you can do today (Phases 1–2):** scaffold a workspace, generate and refine a spec, gate it with `validate`, produce a technical plan, and audit the implementation against the spec with `review`. The separate [`coding-spec/`](coding-spec/) auditing skill adds deeper, agent-driven spec-drift detection on top of this.

**Not yet available (Phase 3):** exporting plans/specs into tool-specific agent formats and native CI wiring — for now, call `validate` yourself in a hook or pipeline (it exits non-zero on incomplete specs).

## Example projects

See [`examples/feature-team-billing/`](examples/feature-team-billing/) for a complete spec → plan → tasks → review walkthrough.

## Documentation

- [Toolkit workflow](docs/workflow.md)
- [Philosophy](docs/philosophy.md)
- [FAQ](docs/faq.md)
- [Skill package README](coding-spec/README.md)

## Development

```bash
python3 -m pytest tests/ -q                                   # toolkit CLI tests
python3 src/cli.py --help                                     # list all subcommands
cd coding-spec && python3 -m unittest scripts/test_spec_parse.py -q  # auditing skill parser tests
```

- `tests/test_cli.py` covers the `init → spec → plan` flow plus `validate` (pass/fail) and `review` criterion extraction.
- `tests/test_snapshot.py` guards the canonical templates against accidental drift.
- The auditing skill ships its own parser unit tests under `coding-spec/scripts/`.

## License

MIT — see [LICENSE](LICENSE).