import os
import re
import sys
from pathlib import Path

# Kept in sync with validate.py: tolerate an optional numbered heading prefix so
# specs generated from the toolkit's own templates ("## 3. Acceptance Criteria")
# have their criteria extracted correctly.
ACCEPTANCE_RE = re.compile(
    r"(?i)^#+\s+(?:\d+\.\s+)?(?:acceptance\s+criteria|done\s+when|success\s+criteria|expected\s+behavior)"
)
HEADING_RE = re.compile(r"^#+\s+")
BULLET_RE = re.compile(r"^[-*]\s+(?:\[[ xX]\]\s+)?(.+)")
NUMBERED_RE = re.compile(r"^\d+\.\s+(.+)")

# Directories skipped when scanning for implementation evidence.
SKIP_DIRS = {"__pycache__", "node_modules", ".git", "venv", ".venv"}


def _extract_criteria(spec_text: str) -> list[str]:
    criteria = []
    in_acceptance = False
    for line in spec_text.splitlines():
        if ACCEPTANCE_RE.search(line):
            in_acceptance = True
            continue
        if HEADING_RE.match(line):
            in_acceptance = False
            continue
        if not in_acceptance:
            continue
        stripped = line.strip()
        bullet = BULLET_RE.match(stripped)
        if bullet:
            criteria.append(bullet.group(1).strip())
            continue
        numbered = NUMBERED_RE.match(stripped)
        if numbered:
            criteria.append(numbered.group(1).strip())
    return criteria


def _find_evidence(criterion: str, target_dir: Path, skip: set[Path]) -> list[str]:
    keywords = [w.lower() for w in re.findall(r"\b\w{4,}\b", criterion)[:3]]
    if not keywords or not target_dir.is_dir():
        return []

    matched = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            if not (name.endswith(".py") or name.endswith(".md")):
                continue
            path = Path(root) / name
            if path.resolve() in skip:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore").lower()
            except OSError:
                continue
            if all(keyword in content for keyword in keywords):
                matched.append(name)
    return matched


def run_review(spec_file_path: str, target_dir_path: str | None) -> int:
    spec_path = Path(spec_file_path).resolve()
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    target_dir = Path(target_dir_path or ".").resolve()
    slug = spec_path.stem
    review_file = target_dir / "docs" / "plans" / f"{slug}-review.md"
    skip = {spec_path, review_file.resolve()}

    criteria = _extract_criteria(spec_path.read_text(encoding="utf-8"))

    title = slug.replace("-", " ").title()
    lines = [
        f"# Implementation Review: {title}",
        "",
        "This checklist compares implementation evidence against the acceptance criteria in the spec.",
        "",
        "## Acceptance Criteria Compliance",
        "",
    ]

    if not criteria:
        lines.append("- [ ] No explicit acceptance criteria were found in the spec file.")
    else:
        for criterion in criteria:
            matched = _find_evidence(criterion, target_dir, skip)
            status = "[x]" if matched else "[ ]"
            evidence = (
                f" (evidence in: {', '.join(matched)})"
                if matched
                else " (no matching code evidence found)"
            )
            lines.append(f"- {status} {criterion}{evidence}")

    lines += [
        "",
        "## Verification Verdict",
        "- [ ] Passed manual review.",
        "- [ ] Verified in a testing sandbox.",
    ]

    review_file.parent.mkdir(parents=True, exist_ok=True)
    review_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated implementation review checklist at: {review_file}")
    return 0
