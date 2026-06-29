#!/usr/bin/env python3
"""Parse Markdown-style specs into a structured requirement checklist."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
CHECKLIST_RE = re.compile(r"^-\s+\[[ xX]\]\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^[-*]\s+(.+?)\s*$")
NUMBERED_RE = re.compile(r"^\d+\.\s+(.+?)\s*$")
FENCED_CODE_RE = re.compile(r"^```")

ACCEPTANCE_SECTION_RE = re.compile(
    r"(?i)\b(acceptance criteria|done when|success criteria|expected behavior)\b"
)
NON_GOAL_SECTION_RE = re.compile(
    r"(?i)\b(non-?goals?|out of scope|not in scope|exclusions?)\b"
)

REQUIREMENT_VERBS = (
    "must",
    "shall",
    "should",
    "will",
    "need to",
    "needs to",
    "required to",
    "prevents",
    "prevent",
    "allows",
    "allow",
    "rejects",
    "reject",
    "records",
    "record",
    "displays",
    "display",
    "supports",
    "support",
    "enables",
    "enable",
    "ensures",
    "ensure",
    "validates",
    "validate",
    "blocks",
    "block",
)

CAPABILITY_HEADING_RE = re.compile(
    r"(?i)\b("
    r"can|must|shall|should|will|"
    r"support|enable|allow|prevent|block|reject|validate|display|record|ensure"
    r")\b"
)
IMPERATIVE_HEADING_RE = re.compile(
    r"^(?:Support|Enable|Allow|Prevent|Block|Reject|Validate|Display|Record|Ensure|Handle|Provide|Implement|Add|Remove|Create|Update|Delete|Export|Import|Sync|Notify)\b"
)

PRIORITY_RE = re.compile(r"(?i)\b(P0|P1|P2|P3|high|medium|low|critical)\b")
COMPOUND_AND_RE = re.compile(r"\s+and\s+", re.IGNORECASE)

SIGNAL_CUES = (
    ("duplicate", "duplicate case handled"),
    ("error", "error surfaced to caller"),
    ("validation", "validation enforced"),
    ("permission", "permission rule enforced"),
    ("role", "role-based access enforced"),
    ("test", "test covers requirement"),
    ("export", "export path implemented"),
    ("import", "import path implemented"),
    ("timeout", "timeout behavior implemented"),
    ("retry", "retry behavior implemented"),
    ("audit", "audit log recorded"),
    ("schema", "schema field present"),
    ("migration", "migration applied"),
)


@dataclass
class Requirement:
    id: str
    title: str
    group: str
    source_excerpt: str
    acceptance_signals: list[str] = field(default_factory=list)
    priority: str = "unknown"
    type: str = "functional"


@dataclass
class ParseResult:
    source: str
    parsed_at: str
    groups: list[str]
    requirements: list[Requirement]


def slugify(text: str, max_length: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        slug = "requirement"
    return slug[:max_length].rstrip("-")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_compound(text: str) -> list[str]:
    text = normalize_whitespace(text)
    if ";" in text:
        return [normalize_whitespace(part) for part in text.split(";") if normalize_whitespace(part)]

    and_parts = [normalize_whitespace(part) for part in COMPOUND_AND_RE.split(text)]
    if len(and_parts) > 1:
        splittable = [
            part
            for part in and_parts
            if looks_like_requirement_sentence(part) or len(part.split()) >= 4
        ]
        if len(splittable) >= 2:
            return splittable

    return [text]


def detect_priority(text: str) -> str:
    match = PRIORITY_RE.search(text)
    if not match:
        return "unknown"
    value = match.group(1).lower()
    if value in {"p0", "critical", "high"}:
        return "high"
    if value in {"p1", "medium"}:
        return "medium"
    if value in {"p2", "p3", "low"}:
        return "low"
    return value


def looks_like_requirement_sentence(text: str) -> bool:
    lowered = text.lower()
    if any(verb in lowered for verb in REQUIREMENT_VERBS):
        return True
    if re.search(r"(?i)\b(user|system|api|service)\b", text) and re.search(
        r"(?i)\b(can|cannot|can't|able to)\b", text
    ):
        return True
    return False


def heading_is_requirement(text: str) -> bool:
    if CAPABILITY_HEADING_RE.search(text):
        return True
    return bool(IMPERATIVE_HEADING_RE.match(text))


def infer_requirement_type(text: str, *, in_non_goal_section: bool) -> str:
    if in_non_goal_section:
        return "non_goal"
    lowered = text.lower()
    aspirational = (
        "nice to have" in lowered
        or "ideally" in lowered
        or "consider" in lowered
        or "may " in lowered
    )
    measurable = any(
        cue in lowered
        for cue in (
            "must",
            "shall",
            "should",
            "reject",
            "prevent",
            "validate",
            "within",
            "less than",
            "at least",
            "no more than",
        )
    )
    if aspirational and not measurable:
        return "ambiguous"
    return "functional"


def derive_acceptance_signals(text: str) -> list[str]:
    lowered = text.lower()
    signals: list[str] = []
    for cue, signal in SIGNAL_CUES:
        if cue in lowered and signal not in signals:
            signals.append(signal)
    if looks_like_requirement_sentence(text):
        excerpt = normalize_whitespace(text)
        if len(excerpt) <= 120:
            summary = excerpt
        else:
            summary = excerpt[:117].rstrip() + "..."
        if summary not in signals:
            signals.append(summary)
    return signals[:5]


def make_title(text: str) -> str:
    text = normalize_whitespace(text)
    text = re.sub(r"^The system\s+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^Users?\s+", "User ", text, flags=re.IGNORECASE)
    if len(text) <= 120:
        return text
    return text[:117].rstrip() + "..."


def current_group(heading_stack: list[tuple[int, str]]) -> str:
    if not heading_stack:
        return "General"
    return " / ".join(title for _, title in heading_stack)


def allocate_id(group_path: str, counters: dict[str, int]) -> str:
    base = slugify(group_path) or "general"
    counters[base] = counters.get(base, 0) + 1
    return f"{base}-{counters[base]:02d}"


def add_requirement(
    requirements: list[Requirement],
    counters: dict[str, int],
    *,
    group: str,
    text: str,
    in_non_goal_section: bool,
    force: bool = False,
) -> None:
    clauses = (
        [normalize_whitespace(text)]
        if force
        else split_compound(text)
    )
    for clause in clauses:
        if not force and not looks_like_requirement_sentence(clause):
            if not heading_is_requirement(clause):
                continue
        req_id = allocate_id(group, counters)
        requirements.append(
            Requirement(
                id=req_id,
                title=make_title(clause),
                group=group,
                source_excerpt=clause,
                acceptance_signals=derive_acceptance_signals(clause),
                priority=detect_priority(clause),
                type=infer_requirement_type(clause, in_non_goal_section=in_non_goal_section),
            )
        )


def parse_markdown(text: str, source: str) -> ParseResult:
    heading_stack: list[tuple[int, str]] = []
    groups: list[str] = []
    requirements: list[Requirement] = []
    counters: dict[str, int] = {}
    in_code_fence = False
    in_acceptance_section = False
    in_non_goal_section = False
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if not paragraph_lines:
            return
        paragraph = normalize_whitespace(" ".join(paragraph_lines))
        paragraph_lines = []
        if looks_like_requirement_sentence(paragraph):
            add_requirement(
                requirements,
                counters,
                group=current_group(heading_stack),
                text=paragraph,
                in_non_goal_section=in_non_goal_section,
            )

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        if FENCED_CODE_RE.match(line):
            flush_paragraph()
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            title = normalize_whitespace(heading_match.group(2))
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            group = current_group(heading_stack)
            if group not in groups:
                groups.append(group)

            in_acceptance_section = bool(ACCEPTANCE_SECTION_RE.search(title))
            in_non_goal_section = bool(NON_GOAL_SECTION_RE.search(title))

            if heading_is_requirement(title):
                add_requirement(
                    requirements,
                    counters,
                    group=group,
                    text=title,
                    in_non_goal_section=in_non_goal_section,
                    force=True,
                )
            continue

        if not line.strip():
            flush_paragraph()
            continue

        checklist_match = CHECKLIST_RE.match(line)
        if checklist_match:
            flush_paragraph()
            add_requirement(
                requirements,
                counters,
                group=current_group(heading_stack),
                text=checklist_match.group(1),
                in_non_goal_section=in_non_goal_section,
                force=True,
            )
            continue

        bullet_match = BULLET_RE.match(line) or NUMBERED_RE.match(line)
        if bullet_match:
            flush_paragraph()
            bullet_text = bullet_match.group(1)
            add_requirement(
                requirements,
                counters,
                group=current_group(heading_stack),
                text=bullet_text,
                in_non_goal_section=in_non_goal_section or in_acceptance_section,
                force=in_acceptance_section or in_non_goal_section,
            )
            continue

        paragraph_lines.append(line.strip())

    flush_paragraph()

    return ParseResult(
        source=source,
        parsed_at=datetime.now(timezone.utc).isoformat(),
        groups=groups,
        requirements=requirements,
    )


def parse_spec(path: Path) -> ParseResult:
    text = path.read_text(encoding="utf-8")
    return parse_markdown(text, str(path))


def to_json(result: ParseResult) -> str:
    payload = {
        "source": result.source,
        "parsed_at": result.parsed_at,
        "groups": result.groups,
        "requirements": [asdict(req) for req in result.requirements],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse a Markdown spec into a structured requirement checklist."
    )
    parser.add_argument(
        "target",
        help="Path to the primary spec file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Optional output JSON path. Defaults to stdout.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    target = Path(args.target)
    if not target.is_file():
        print(f"error: spec file not found: {target}", file=sys.stderr)
        return 1

    try:
        result = parse_spec(target)
    except OSError as exc:
        print(f"error: failed to read spec: {exc}", file=sys.stderr)
        return 1

    output = to_json(result)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())