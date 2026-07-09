import re
import sys
from pathlib import Path

# Section headings the validator looks for. Each pattern tolerates an optional
# numbered prefix (e.g. "## 3. Acceptance Criteria") so specs generated from the
# toolkit's own templates validate cleanly.
ACCEPTANCE_RE = re.compile(
    r"(?i)^#+\s+(?:\d+\.\s+)?(?:acceptance\s+criteria|done\s+when|success\s+criteria|expected\s+behavior)"
)
NON_GOALS_RE = re.compile(
    r"(?i)^#+\s+(?:\d+\.\s+)?(?:non-?goals?|out\s+of\s+scope|exclusions?)"
)
TEST_RE = re.compile(
    r"(?i)^#+\s+(?:\d+\.\s+)?(?:test\s+considerations?|testing|test\s+(?:strateg(?:y|ies)|plan)|qa)"
)
HEADING_RE = re.compile(r"^#+\s+")
LIST_ITEM_RE = re.compile(r"^(?:[-*]|\d+\.)\s+")


def check_spec(spec_path: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a single spec file. Shared by the single-file
    and --all validation paths so both apply exactly the same rules."""
    has_acceptance = False
    acceptance_items = 0
    has_non_goals = False
    has_test_considerations = False
    in_acceptance = False

    for line in spec_path.read_text(encoding="utf-8").splitlines():
        if ACCEPTANCE_RE.search(line):
            has_acceptance = True
            in_acceptance = True
            continue
        if NON_GOALS_RE.search(line):
            has_non_goals = True
            in_acceptance = False
            continue
        if TEST_RE.search(line):
            has_test_considerations = True
            in_acceptance = False
            continue
        if HEADING_RE.match(line):
            in_acceptance = False
            continue

        if in_acceptance and LIST_ITEM_RE.match(line.strip()):
            acceptance_items += 1

    errors = []
    warnings = []

    if not has_acceptance:
        errors.append("Missing required 'Acceptance Criteria' section.")
    elif acceptance_items == 0:
        errors.append("'Acceptance Criteria' section exists but lists no criteria.")

    if not has_test_considerations:
        errors.append("Missing 'Test Considerations' section; specs should plan a test strategy.")

    if not has_non_goals:
        warnings.append("Missing 'Non-Goals / Out of Scope' section; defining scope prevents drift.")

    return errors, warnings


def run_validate(spec_file_path: str) -> int:
    spec_path = Path(spec_file_path).resolve()
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    errors, warnings = check_spec(spec_path)

    print(f"Validating spec file: {spec_path}")
    print(f"  Found {len(errors)} error(s), {len(warnings)} warning(s).")
    for message in errors:
        print(f"  [ERROR] {message}")
    for message in warnings:
        print(f"  [WARNING] {message}")

    if errors:
        print("Validation FAILED.")
        return 1

    print("Validation PASSED.")
    return 0


def run_validate_all(target_dir_path: str | None) -> int:
    """Validate every spec under docs/specs. Returns non-zero if any spec has
    errors, so it can serve as a single required CI check for a whole repo."""
    target_dir = Path(target_dir_path or ".").resolve()
    specs_dir = target_dir / "docs" / "specs"
    if not specs_dir.is_dir():
        print(f"Error: no specs directory found at '{specs_dir}'. Run `coding-spec init` first.", file=sys.stderr)
        return 1

    spec_files = sorted(specs_dir.glob("*.md"))
    if not spec_files:
        print(f"No specs found under '{specs_dir}'. Nothing to validate.")
        return 0

    failed = 0
    total_warnings = 0
    print(f"Validating {len(spec_files)} spec(s) under '{specs_dir}':")
    for spec_path in spec_files:
        errors, warnings = check_spec(spec_path)
        total_warnings += len(warnings)
        status = "FAIL" if errors else "PASS"
        if errors:
            failed += 1
        print(f"  [{status}] {spec_path.name} — {len(errors)} error(s), {len(warnings)} warning(s)")
        for message in errors:
            print(f"      [ERROR] {message}")

    print(f"Summary: {len(spec_files) - failed}/{len(spec_files)} passed, {total_warnings} warning(s).")
    if failed:
        print("Validation FAILED.")
        return 1
    print("Validation PASSED.")
    return 0
