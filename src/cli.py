#!/usr/bin/env python3
"""coding-spec CLI — init, spec, plan, validate, review, export, ci."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.ci import run_ci
from src.commands.export import FORMATS, run_export
from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.review import run_review
from src.commands.spec import run_spec
from src.commands.validate import run_validate, run_validate_all


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="coding-spec: lightweight spec-first workflow for AI-assisted development.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_init = subparsers.add_parser("init", help="Initialize folders and base templates.")
    parser_init.add_argument("--dir", help="Target directory (defaults to current directory).")

    parser_spec = subparsers.add_parser("spec", help="Create a feature spec from a short prompt.")
    parser_spec.add_argument("prompt", help="Title or short prompt for the feature.")
    parser_spec.add_argument("--dir", help="Target directory.")

    parser_plan = subparsers.add_parser("plan", help="Convert an approved spec into a technical plan.")
    parser_plan.add_argument("spec_file", help="Path to the approved spec file.")
    parser_plan.add_argument("--dir", help="Target directory.")

    parser_validate = subparsers.add_parser(
        "validate", help="Check a spec for completeness (acceptance criteria, tests, scope)."
    )
    parser_validate.add_argument("spec_file", nargs="?", help="Path to the spec file to validate.")
    parser_validate.add_argument(
        "--all", action="store_true", dest="all_specs",
        help="Validate every spec under docs/specs (repo-wide CI gate).",
    )
    parser_validate.add_argument("--dir", help="Target directory (used with --all).")

    parser_review = subparsers.add_parser(
        "review", help="Generate a review checklist comparing implementation to the spec."
    )
    parser_review.add_argument("spec_file", help="Path to the spec file.")
    parser_review.add_argument("--dir", help="Target directory.")

    parser_export = subparsers.add_parser(
        "export", help="Bundle a spec (+plan/tasks/review) into an agent-ready brief."
    )
    parser_export.add_argument("spec_file", help="Path to the spec file.")
    parser_export.add_argument(
        "--format", choices=FORMATS, default="markdown", help="Export format (default: markdown)."
    )
    parser_export.add_argument("--dir", help="Target directory.")

    parser_ci = subparsers.add_parser(
        "ci", help="Generate a GitHub Actions workflow that runs `validate --all`."
    )
    parser_ci.add_argument("--dir", help="Target directory.")

    args = parser.parse_args()

    if args.command == "init":
        return run_init(args.dir)
    if args.command == "spec":
        return run_spec(args.prompt, args.dir)
    if args.command == "plan":
        return run_plan(args.spec_file, args.dir)
    if args.command == "validate":
        if args.all_specs:
            return run_validate_all(args.dir)
        if not args.spec_file:
            parser_validate.error("provide a spec file, or use --all to validate every spec.")
        return run_validate(args.spec_file)
    if args.command == "review":
        return run_review(args.spec_file, args.dir)
    if args.command == "export":
        return run_export(args.spec_file, args.format, args.dir)
    if args.command == "ci":
        return run_ci(args.dir)

    return 1


if __name__ == "__main__":
    sys.exit(main())