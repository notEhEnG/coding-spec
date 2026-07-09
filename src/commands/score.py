"""score — produce a spec-to-code health scorecard.

Phase 4 (Differentiate). Combines the existing signals into a single graded
scorecard so a feature's readiness can be seen at a glance:

  * Completeness (40 pts) — reuses the `validate` rules (errors/warnings).
  * Coverage     (40 pts) — share of acceptance criteria with code evidence,
                            reusing the `review` scanner.
  * Artifacts    (20 pts) — whether a plan and a review checklist exist.

The scoring is intentionally simple and transparent; treat the grade as a
prompt for human judgement, not a proof of correctness.
"""

import sys
from pathlib import Path

from src.commands.review import _collect_sources, _extract_criteria, _find_evidence
from src.commands.validate import check_spec

COMPLETENESS_MAX = 40
COVERAGE_MAX = 40
ARTIFACTS_MAX = 20


def _grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def compute_score(spec_path: Path, target_dir: Path) -> dict:
    """Return the full scorecard breakdown for one spec (pure; no file writes)."""
    errors, warnings = check_spec(spec_path)
    completeness = max(0, COMPLETENESS_MAX - 20 * len(errors) - 5 * len(warnings))

    criteria = _extract_criteria(spec_path.read_text(encoding="utf-8"))
    slug = spec_path.stem
    plans_dir = target_dir / "docs" / "plans"
    plan_file = plans_dir / f"{slug}-plan.md"
    review_file = plans_dir / f"{slug}-review.md"

    covered = 0
    per_criterion: list[tuple[str, list[str]]] = []
    if criteria:
        skip = {spec_path.resolve(), review_file.resolve()}
        sources = _collect_sources(target_dir, skip)
        for c in criteria:
            matched = _find_evidence(c, sources)
            if matched:
                covered += 1
            per_criterion.append((c, matched))
        coverage = round(COVERAGE_MAX * covered / len(criteria))
    else:
        coverage = 0

    has_plan = plan_file.is_file()
    has_review = review_file.is_file()
    artifacts = (10 if has_plan else 0) + (10 if has_review else 0)

    total = completeness + coverage + artifacts
    return {
        "slug": slug,
        "errors": errors,
        "warnings": warnings,
        "completeness": completeness,
        "criteria_total": len(criteria),
        "criteria_covered": covered,
        "coverage": coverage,
        "has_plan": has_plan,
        "has_review": has_review,
        "artifacts": artifacts,
        "total": total,
        "grade": _grade(total),
        "per_criterion": per_criterion,
    }


def _render(card: dict, title: str) -> str:
    lines = [
        f"# Scorecard: {title}",
        "",
        f"**Grade: {card['grade']}  ({card['total']}/100)**",
        "",
        "| Dimension | Score | Detail |",
        "|---|---|---|",
        f"| Completeness | {card['completeness']}/{COMPLETENESS_MAX} | {len(card['errors'])} error(s), {len(card['warnings'])} warning(s) |",
        f"| Coverage | {card['coverage']}/{COVERAGE_MAX} | {card['criteria_covered']}/{card['criteria_total']} acceptance criteria have code evidence |",
        f"| Artifacts | {card['artifacts']}/{ARTIFACTS_MAX} | plan: {'yes' if card['has_plan'] else 'no'}, review: {'yes' if card['has_review'] else 'no'} |",
        "",
    ]
    if card["errors"]:
        lines.append("## Completeness errors")
        lines += [f"- {e}" for e in card["errors"]]
        lines.append("")
    if card["per_criterion"]:
        lines.append("## Criteria coverage")
        for c, matched in card["per_criterion"]:
            mark = "[x]" if matched else "[ ]"
            evidence = f" (evidence in: {', '.join(matched)})" if matched else " (no matching code evidence)"
            lines.append(f"- {mark} {c}{evidence}")
        lines.append("")
    lines.append("_Heuristic scorecard — a prompt for human judgement, not a proof of correctness._")
    return "\n".join(lines) + "\n"


def run_score(spec_file_path: str, target_dir_path: str | None) -> int:
    spec_path = Path(spec_file_path).resolve()
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    target_dir = Path(target_dir_path or ".").resolve()
    card = compute_score(spec_path, target_dir)
    title = card["slug"].replace("-", " ").title()

    scorecard_file = target_dir / "docs" / "plans" / f"{card['slug']}-scorecard.md"
    scorecard_file.parent.mkdir(parents=True, exist_ok=True)
    scorecard_file.write_text(_render(card, title), encoding="utf-8")

    print(f"Scorecard for {card['slug']}: grade {card['grade']} ({card['total']}/100)")
    print(
        f"  Completeness {card['completeness']}/{COMPLETENESS_MAX}, "
        f"Coverage {card['coverage']}/{COVERAGE_MAX} "
        f"({card['criteria_covered']}/{card['criteria_total']} criteria), "
        f"Artifacts {card['artifacts']}/{ARTIFACTS_MAX}."
    )
    print(f"  Wrote {scorecard_file}")
    return 0
