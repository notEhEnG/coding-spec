#!/usr/bin/env python3
"""coding-spec CLI — Phase 1: init, spec, and plan."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init
from src.commands.plan import run_plan
from src.commands.spec import run_spec


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

    args = parser.parse_args()

    if args.command == "init":
        return run_init(args.dir)
    if args.command == "spec":
        return run_spec(args.prompt, args.dir)
    if args.command == "plan":
        return run_plan(args.spec_file, args.dir)

    return 1


if __name__ == "__main__":
    sys.exit(main())