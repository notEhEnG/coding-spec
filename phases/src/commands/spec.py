import sys
from pathlib import Path

def slugify(text: str) -> str:
    import re
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def run_spec(prompt: str, target_dir_path: str | None) -> int:
    slug = slugify(prompt)
    target_dir = Path(target_dir_path or '.')
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
