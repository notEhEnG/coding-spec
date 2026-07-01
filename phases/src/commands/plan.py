import sys
from pathlib import Path

def run_plan(spec_file_path: str, target_dir_path: str | None) -> int:
    spec_path = Path(spec_file_path)
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1
        
    target_dir = Path(target_dir_path or '.')
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
