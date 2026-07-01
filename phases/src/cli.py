#!/usr/bin/env python3
"""coding-spec CLI Tool Orchestrator.

Routes and dispatches execution to commands.
"""

import sys
from pathlib import Path

# Add src parent to sys.path to enable local imports when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.commands.init import run_init
from src.commands.spec import run_spec
from src.commands.plan import run_plan
from src.commands.validate import run_validate
from src.commands.review import run_review

def main():
    import argparse
    parser = argparse.ArgumentParser(description="coding-spec: CLI for spec-driven development.")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # init
    parser_init = subparsers.add_parser('init', help='Initialize folders and base templates.')
    parser_init.add_argument('--dir', help='Target directory (defaults to current directory).')
    
    # spec
    parser_spec = subparsers.add_parser('spec', help='Create a feature spec from a short prompt.')
    parser_spec.add_argument('prompt', help='Title or short prompt for the feature.')
    parser_spec.add_argument('--dir', help='Target directory.')
    
    # plan
    parser_plan = subparsers.add_parser('plan', help='Convert an approved spec into a technical plan.')
    parser_plan.add_argument('spec_file', help='Path to the approved spec file.')
    parser_plan.add_argument('--dir', help='Target directory.')

    # validate
    parser_validate = subparsers.add_parser('validate', help='Validate a spec for completeness (acceptance criteria, test strategies, scope).')
    parser_validate.add_argument('spec_file', help='Path to the spec file to validate.')

    # review
    parser_review = subparsers.add_parser('review', help='Generate review checklist comparing implementation against spec.')
    parser_review.add_argument('spec_file', help='Path to the spec file.')
    parser_review.add_argument('--dir', help='Target directory.')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        return run_init(args.dir)
    elif args.command == 'spec':
        return run_spec(args.prompt, args.dir)
    elif args.command == 'plan':
        return run_plan(args.spec_file, args.dir)
    elif args.command == 'validate':
        return run_validate(args.spec_file)
    elif args.command == 'review':
        return run_review(args.spec_file, args.dir)
        
if __name__ == '__main__':
    sys.exit(main())
