# coding-spec

coding-spec is a lightweight, opinionated toolkit for building software with specs before code. It gives developers a clean workflow for turning rough ideas into implementation-ready artifacts: product specs, technical plans, task lists, and review checklists. The goal is simple — reduce vague prompts, improve AI coding output, and make feature work easier to review, test, and ship.

## Why this exists

AI coding tools are fast, but they produce uneven results when requirements are vague. Spec-driven workflows make the specification the source of truth before implementation begins.

## What coding-spec does

- Scaffolds a markdown-first project workspace (`init`)
- Generates a feature spec from a short prompt (`spec`)
- Converts an approved spec into a technical plan (`plan`)
- Ships canonical templates for specs, plans, tasks, and reviews
- Includes a full end-to-end demo in `examples/feature-team-billing/`

## Who it is for

- Solo developers using AI editors
- Small product teams that need consistent feature planning
- Engineers who want more structure than vibe coding, with less process than enterprise frameworks

## Core workflow

1. Capture the feature intent.
2. Write or refine the spec.
3. Produce a technical plan.
4. Hand the plan to your coding agent.

Phase 1 ships the first three steps. Validation, review automation, and CI integration arrive in later phases.

## Quickstart

```bash
# From the repository root
chmod +x bin/coding-spec

# Initialize a project workspace (current directory by default)
./bin/coding-spec init

# Generate a spec from a prompt
./bin/coding-spec spec "Add team billing"

# Convert the spec into a technical plan
./bin/coding-spec plan docs/specs/add-team-billing.md
```

A new user can complete init → spec → plan in under ten minutes.

## Repository layout

```text
coding-spec/
├── README.md
├── LICENSE
├── bin/coding-spec          # CLI launcher
├── docs/                    # Philosophy, workflow, FAQ, examples guide
├── templates/               # Canonical markdown templates
├── examples/                # End-to-end demo features
├── prompts/                 # Reusable agent prompt packs
├── src/                     # CLI implementation
├── tests/                   # CLI and template snapshot tests
└── coding-spec/             # Portable spec-drift auditing skill (separate package)
```

## Example projects

See [`examples/feature-team-billing/`](examples/feature-team-billing/) for a complete spec → plan → tasks → review walkthrough, and [`docs/examples.md`](docs/examples.md) for a guided tour.

## Documentation

- [Philosophy](docs/philosophy.md)
- [Workflow guide](docs/workflow.md)
- [FAQ](docs/faq.md)

## Development

```bash
python3 -m pytest tests/ -q
python3 src/cli.py --help
```

## License

MIT — see [LICENSE](LICENSE).