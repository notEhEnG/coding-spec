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

./bin/coding-spec init
./bin/coding-spec spec "Add team billing"
./bin/coding-spec plan docs/specs/add-team-billing.md
```

A new user can complete init → spec → plan in under ten minutes.

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

## Example projects

See [`examples/feature-team-billing/`](examples/feature-team-billing/) for a complete spec → plan → tasks → review walkthrough.

## Documentation

- [Toolkit workflow](docs/workflow.md)
- [Philosophy](docs/philosophy.md)
- [FAQ](docs/faq.md)
- [Skill package README](coding-spec/README.md)

## Development

```bash
python3 -m pytest tests/ -q
python3 src/cli.py --help
cd coding-spec && python3 -m unittest scripts/test_spec_parse.py -q
```

## License

MIT — see [LICENSE](LICENSE).