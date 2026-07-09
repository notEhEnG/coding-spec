"""export — bundle a spec and its related artifacts into an agent-ready brief.

Phase 3 (Automate). Produces a single self-contained context file in a
tool-specific format so a spec can be handed directly to a coding agent
(Claude Code, Cursor, an AGENTS.md-aware tool) instead of copy-pasting
fragments. The bundled content is identical across formats; only the wrapper
(preamble/frontmatter/extension) changes.
"""

import sys
from pathlib import Path

# format -> (file suffix, needs frontmatter). Keep keys in sync with the CLI
# choices in cli.py and the FORMATS list used by tests.
FORMATS = ("markdown", "claude", "cursor", "agents")

_SUFFIX = {
    "markdown": ".md",
    "claude": ".claude.md",
    "cursor": ".mdc",
    "agents": ".agents.md",
}


def _read_if_present(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _bundle(slug: str, title: str, artifacts: list[tuple[str, str]]) -> str:
    """Concatenate the discovered artifacts under labelled sections."""
    parts = []
    for label, body in artifacts:
        parts.append(f"## {label}\n\n{body.strip()}\n")
    return "\n".join(parts)


def _wrap(fmt: str, title: str, slug: str, body: str, present: list[str]) -> str:
    manifest = ", ".join(present)
    if fmt == "claude":
        return (
            f"# Agent brief: {title}\n\n"
            "You are implementing an approved, spec-first change. Treat the spec below as the "
            "source of truth: satisfy every acceptance criterion, respect the non-goals, and "
            "follow the technical plan where one is provided. Do not add out-of-scope work.\n\n"
            f"_Bundled artifacts: {manifest}._\n\n"
            "---\n\n"
            f"{body}"
        )
    if fmt == "cursor":
        # Cursor .mdc rule file: YAML frontmatter + body.
        return (
            "---\n"
            f"description: Spec-first context for {title}\n"
            'globs: ""\n'
            "alwaysApply: false\n"
            "---\n\n"
            f"# {title}\n\n"
            f"_Bundled artifacts: {manifest}._\n\n"
            f"{body}"
        )
    if fmt == "agents":
        return (
            f"# AGENTS.md — {title}\n\n"
            "Spec-driven context for this change. Agents working in this repository should keep the "
            "acceptance criteria below satisfied.\n\n"
            f"_Bundled artifacts: {manifest}._\n\n"
            f"{body}"
        )
    # markdown (default): plain, portable bundle.
    return (
        f"# {title} — spec bundle\n\n"
        f"_Bundled artifacts: {manifest}._\n\n"
        f"{body}"
    )


def run_export(spec_file_path: str, fmt: str | None, target_dir_path: str | None) -> int:
    fmt = (fmt or "markdown").lower()
    if fmt not in FORMATS:
        print(f"Error: unknown format '{fmt}'. Choose one of: {', '.join(FORMATS)}.", file=sys.stderr)
        return 1

    spec_path = Path(spec_file_path).resolve()
    if not spec_path.is_file():
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        return 1

    target_dir = Path(target_dir_path or ".").resolve()
    slug = spec_path.stem
    title = slug.replace("-", " ").title()

    plans_dir = target_dir / "docs" / "plans"
    candidates = [
        ("Specification", spec_path),
        ("Technical Plan", plans_dir / f"{slug}-plan.md"),
        ("Task List", plans_dir / f"{slug}-tasks.md"),
        ("Review Checklist", plans_dir / f"{slug}-review.md"),
    ]

    artifacts: list[tuple[str, str]] = []
    present: list[str] = []
    for label, path in candidates:
        body = _read_if_present(path)
        if body is not None:
            artifacts.append((label, body))
            present.append(label)

    body = _bundle(slug, title, artifacts)
    output = _wrap(fmt, title, slug, body, present)

    export_file = target_dir / "docs" / "exports" / f"{slug}{_SUFFIX[fmt]}"
    export_file.parent.mkdir(parents=True, exist_ok=True)
    export_file.write_text(output, encoding="utf-8")

    print(f"Exported {fmt} agent brief to: {export_file}")
    print(f"  Bundled: {', '.join(present)}.")
    return 0
