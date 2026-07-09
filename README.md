# coding-spec

coding-spec is a lightweight, opinionated toolkit for building software with specs before code. It gives developers a clean workflow for turning rough ideas into implementation-ready artifacts: product specs, technical plans, task lists, and review checklists. The goal is simple — reduce vague prompts, improve AI coding output, and make feature work easier to review, test, and ship.

This repository is a **monorepo** with two packages:

1. **Toolkit CLI** (repo root) — scaffold specs and plans before you code.
2. **Auditing skill** ([`coding-spec/`](coding-spec/)) — verify implementation matches the spec after you code.

**Use it as a skill:** install the repo into Claude Code, Antigravity, or a
Codex-compatible tool and the whole workflow becomes `/coding-spec` — see
[Use it as an agent skill](#use-it-as-an-agent-skill-coding-spec).

## Why this exists

AI coding tools are fast, but they produce uneven results when requirements are vague. Spec-driven workflows make the specification the source of truth before implementation begins.

## What the toolkit does

- Scaffolds a markdown-first project workspace (`init`)
- Generates a feature spec from a short prompt (`spec`)
- Converts an approved spec into a technical plan (`plan`)
- Checks a spec for completeness — acceptance criteria, tests, scope (`validate`, or `validate --all` for a whole repo)
- Generates a review checklist that matches spec criteria to code evidence (`review`)
- Bundles a spec and its plan/review into an agent-ready brief for Claude, Cursor, or AGENTS.md tools (`export`)
- Generates a GitHub Actions workflow that runs the spec gate as a required check (`ci`)
- Grades a feature's spec-to-code health as a single scorecard (`score`)
- Indexes every spec with its status and grade in one portfolio view (`catalog`)
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
./bin/coding-spec export docs/specs/add-team-billing.md --format claude  # bundle an agent brief
./bin/coding-spec score docs/specs/add-team-billing.md        # grade spec-to-code health
./bin/coding-spec catalog                                     # index every spec's status
./bin/coding-spec ci                                          # generate a CI spec gate
```

A new user can complete init → spec → plan in under ten minutes; `validate` and `review` add a trust gate on either side of implementation.

## Command reference

| Command | Input | Produces / checks | Exit code |
|---|---|---|---|
| `init [--dir DIR]` | — | Creates `docs/`, `templates/`, `examples/`, `prompts/`, `src/`, `tests/` and copies the canonical templates. | `0` |
| `spec "<prompt>" [--dir DIR]` | a short title | `docs/specs/<slug>.md` from the spec template. | `0` |
| `validate <spec.md>` | a spec file | Static completeness check (see below). Prints errors/warnings. | `1` if any error, else `0` |
| `validate --all [--dir DIR]` | — | Runs the completeness check on every spec under `docs/specs`. A single repo-wide gate for CI. | `1` if any spec has errors, else `0` |
| `plan <spec.md> [--dir DIR]` | an approved spec | `docs/plans/<slug>-plan.md` from the plan template. | `0` |
| `review <spec.md> [--dir DIR]` | a spec file | `docs/plans/<slug>-review.md` — each acceptance criterion paired with matching code evidence found in the tree. | `0` |
| `export <spec.md> [--format F] [--dir DIR]` | a spec file | `docs/exports/<slug>.*` — the spec plus any plan/tasks/review bundled into one agent brief. `F` ∈ `markdown` (default), `claude`, `cursor`, `agents`. | `0` |
| `ci [--dir DIR]` | — | `.github/workflows/coding-spec.yml` — a workflow running `validate --all` on push/PR. | `0` (or `1` if it already exists) |
| `score <spec.md> [--dir DIR]` | a spec file | `docs/plans/<slug>-scorecard.md` — a graded scorecard (completeness + criteria coverage + artifacts). | `0` |
| `catalog [--dir DIR]` | — | `docs/catalog.md` — a table of every spec with validation status, plan/review presence, coverage, and grade. | `0` |

**What `validate` checks** (headings are matched case-insensitively and tolerate a numbered prefix such as `## 3. Acceptance Criteria`):

- **Error** — no *Acceptance Criteria* section, or the section has no list items ("under-specified criteria").
- **Error** — no *Test Considerations* / *Testing* / *Test Plan* / *QA* section.
- **Warning** — no *Non-Goals* / *Out of Scope* section (recommended to prevent scope drift).

Because `validate` returns a non-zero exit code on errors, you can wire it into a pre-commit hook or CI step to block specs that are not implementation-ready.

**What `review` produces** — it extracts each acceptance criterion, then keyword-scans the repository's `.py`/`.md` files (skipping caches, VCS, and vendored dirs) for evidence, marking every criterion `[x]` (evidence found, with file names) or `[ ]` (none). Treat it as a heuristic aid for a human reviewer, not a proof of correctness.

## Use it as an agent skill (`/coding-spec`)

Install the repository as a skill and the whole workflow becomes a slash command:
`/coding-spec` drives **both** the toolkit (`init`, `spec`, `plan`, `validate`,
`review`, `export`, `ci`, `score`, `catalog`) and the drift **auditor** (`audit`,
`reverse-spec`, `patch`, `release-check`). The root [`SKILL.md`](SKILL.md) routes
each call to the right half based on the first token.

### Easiest: ask your agent

Tell your coding agent to install it, then trigger `/coding-spec`:

```text
Hey Claude, install this skill https://github.com/notEhEnG/coding-spec
Hey Antigravity, install this skill https://github.com/notEhEnG/coding-spec
Hey Codex, install this skill https://github.com/notEhEnG/coding-spec
```

The agent clones the repo into your skill directory (`.claude/skills/`,
`.antigravity/skills/`, or your Codex skill dir) and you invoke `/coding-spec`.

### One-command install

```bash
# from anywhere in your project — clones and installs in one step
curl -fsSL https://raw.githubusercontent.com/notEhEnG/coding-spec/main/install.sh | bash -s -- claude
# or: ... | bash -s -- antigravity     (or codex, or all)
```

Or, from a local clone:

```bash
git clone https://github.com/notEhEnG/coding-spec.git
./coding-spec/install.sh claude --dir /path/to/your/project
```

### Manual install

Copy the **whole repository** into the tool's skill directory as `coding-spec/`
(the toolkit CLI must sit next to `SKILL.md` so `/coding-spec spec …` can run):

| Tool | Install path | Invoke |
|---|---|---|
| Claude Code | `.claude/skills/coding-spec/SKILL.md` | `/coding-spec spec "Add billing"`, `/coding-spec audit docs/specs/x.md` |
| Antigravity IDE | `.antigravity/skills/coding-spec/SKILL.md` | `/coding-spec …` or assign the skill to an agent in Manager View |
| Codex-compatible | `<codex-skill-dir>/coding-spec/SKILL.md` | `/coding-spec …` when your wrapper maps skills to slash commands |

```bash
git clone https://github.com/notEhEnG/coding-spec.git /tmp/coding-spec-repo
mkdir -p .claude/skills
cp -r /tmp/coding-spec-repo .claude/skills/coding-spec
```

Keep the folder name `coding-spec` so the slash-command identity stays stable.

### Auditor-only bundle

If you want *only* the drift auditor (no toolkit CLI), the self-contained
[`coding-spec/`](coding-spec/) subfolder is still a standalone `SKILL.md`
package — copy just that subfolder. See [`coding-spec/INSTALL.md`](coding-spec/INSTALL.md).

## Repository layout

```text
coding-spec/                 # monorepo root (also installs as the /coding-spec skill)
├── README.md
├── SKILL.md                 # unified skill entry point (toolkit + auditor routing)
├── install.sh               # install as an agent skill (claude/antigravity/codex)
├── LICENSE
├── bin/coding-spec          # toolkit CLI launcher
├── docs/                    # philosophy, workflow, FAQ
├── templates/               # canonical markdown templates
├── examples/                # end-to-end demo features
├── prompts/                 # reusable agent prompt packs
├── src/                     # toolkit CLI implementation
├── tests/
└── coding-spec/             # portable auditor-only skill (install separately)
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
| **Phase 3** | Automate | `export` (agent brief modes), `validate --all` + `ci` (GitHub Actions spec gate) | ✅ Shipped |
| **Phase 4** | Differentiate | `score` (spec-to-code scorecard) and `catalog` (portfolio index of all specs) | ✅ Shipped |

**What you can do today (Phases 1–4):** scaffold a workspace, generate and refine a spec, gate it with `validate` (single file or `--all`), produce a technical plan, audit the implementation with `review`, export the spec as an agent brief for Claude/Cursor/AGENTS.md tools, wire a CI spec gate with `ci`, grade a feature with `score`, and see every feature at a glance with `catalog`. The separate [`coding-spec/`](coding-spec/) auditing skill adds deeper, agent-driven spec-drift detection on top of this.

The `export`, `score`, and `catalog` outputs are heuristic aids for human judgement, not proofs of correctness.

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
- `tests/test_phase3.py` covers `export` (all formats), `validate --all`, and `ci`.
- `tests/test_phase4.py` covers `score` (scorecard + artifact rewards) and `catalog` (portfolio index).
- `tests/test_snapshot.py` guards the canonical templates against accidental drift.
- The auditing skill ships its own parser unit tests under `coding-spec/scripts/`.
- CI (`.github/workflows/ci.yml`) runs the toolkit tests, the skill parser tests, and the spec gate on every push and PR.

## License

MIT — see [LICENSE](LICENSE).