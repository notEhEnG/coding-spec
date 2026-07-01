import os
import shutil
from pathlib import Path

def run_init(target_dir_path: str | None) -> int:
    target_dir = Path(target_dir_path or '.')
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
    script_dir = Path(__file__).resolve().parent.parent.parent
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
