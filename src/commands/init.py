import shutil
from pathlib import Path

from src.paths import package_root

TEMPLATE_NAMES = (
    "spec.template.md",
    "plan.template.md",
    "tasks.template.md",
    "review.template.md",
    "constitution.template.md",
)


def run_init(target_dir_path: str | None) -> int:
    target_dir = Path(target_dir_path or ".").resolve()
    print(f"Initializing coding-spec workspace under '{target_dir}'...")

    subdirs = (
        "docs/specs",
        "docs/plans",
        "templates",
        "examples",
        "prompts",
        "src",
        "tests",
    )
    for subdir in subdirs:
        (target_dir / subdir).mkdir(parents=True, exist_ok=True)
        print(f"  Created directory: {subdir}")

    source_templates_dir = package_root() / "templates"
    for name in TEMPLATE_NAMES:
        src_file = source_templates_dir / name
        dest_file = target_dir / "templates" / name
        if src_file.is_file():
            shutil.copy2(src_file, dest_file)
            print(f"  Initialized template: templates/{name}")
        else:
            dest_file.write_text(f"# Template: {name}\n\n[Default stub content]\n", encoding="utf-8")
            print(f"  Created stub template: templates/{name}")

    print('Initialization complete. Run `./bin/coding-spec spec "Your Feature"` next.')
    return 0