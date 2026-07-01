#!/usr/bin/env python3
"""Draft CLI implementation for the coding-spec toolkit.

Supports the first three commands planned for v0.1.0:
- init: sets up directories and copies base templates.
- spec: generates a feature spec from a prompt using the spec template.
- plan: generates a technical plan from an existing spec using the plan template.
"""

import sys
import argparse
import os
import shutil
from pathlib import Path

def slugify(text: str) -> str:
    import re
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def cmd_init(args):
    target_dir = Path(args.dir or '.')
    print(f"Initializing coding-spec repository layout under '{target_dir}'...")
    
    # Subdirectories to create
    subdirs = [
        'docs/specs',
        'docs/plans',
        'templates',
        'examples',
        'prompts',
        'src',
        'tests'
    ]
    for d in subdirs:
        (target_dir / d).mkdir(parents=True, exist_ok=True)
        print(f"  Created directory: {d}")
        
    # Copy templates from phases/templates relative to script
    script_dir = Path(__file__).resolve().parent
    source_templates_dir = script_dir / 'templates'
    
    templates = [
        'spec.template.md',
        'plan.template.md',
        'tasks.template.md',
        'review.template.md',
        'constitution.template.md'
    ]
    
    for t in templates:
        src_file = source_templates_dir / t
        dest_file = target_dir / 'templates' / t
        if src_file.is_file():
            shutil.copy2(src_file, dest_file)
            print(f"  Initialized template: templates/{t}")
        else:
            dest_file.write_text(f"# Template: {t}\n\n[Default stub content]\n")
            print(f"  Created stub template: templates/{t}")
            
    print("Initialization complete! Ready for spec-driven workflows.")
    return 0

def cmd_spec(args):
    prompt = args.prompt
    slug = slugify(prompt)
    target_dir = Path(args.dir or '.')
    spec_file = target_dir / 'docs' / 'specs' / f"{slug}.md"
    
    template_file = target_dir / 'templates' / 'spec.template.md'
    if not template_file.is_file():
        print(f"Error: spec template not found at '{template_file}'. Run 'init' command first.", file=sys.stderr)
        return 1
        
    content = template_file.read_text(encoding='utf-8')
    content = content.replace('[Feature Name]', prompt)
    
    spec_file.parent.mkdir(parents=True, exist_ok=True)
    spec_file.write_text(content, encoding='utf-8')
    print(f"Generated feature spec at: {spec_file}")
    return 0

def cmd_plan(args):
    spec_path = Path(args.spec_file)
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1
        
    target_dir = Path(args.dir or '.')
    slug = spec_path.stem
    plan_file = target_dir / 'docs' / 'plans' / f"{slug}-plan.md"
    
    template_file = target_dir / 'templates' / 'plan.template.md'
    if not template_file.is_file():
        print(f"Error: plan template not found at '{template_file}'. Run 'init' command first.", file=sys.stderr)
        return 1
        
    content = template_file.read_text(encoding='utf-8')
    content = content.replace('[Feature Name]', slug.replace('-', ' ').title())
    
    plan_file.parent.mkdir(parents=True, exist_ok=True)
    plan_file.write_text(content, encoding='utf-8')
    print(f"Generated technical plan at: {plan_file}")
    return 0

def main():
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
    
    args = parser.parse_args()
    
    if args.command == 'init':
        return cmd_init(args)
    elif args.command == 'spec':
        return cmd_spec(args)
    elif args.command == 'plan':
        return cmd_plan(args)
        
if __name__ == '__main__':
    sys.exit(main())
