# Phase 3 — Match Report

**Target Spec**: [coding-spec-package.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/coding-spec/coding-spec-package.md)  
**Timestamp**: 2026-06-29T22:45:10+08:00

---

## 1. Matching Methodology
Requirements parsed during Phase 1 (`phases/phase_1.json`) were matched against the codebase evidence collected during Phase 2 (`phases/phase_2.md`). 

We looked for:
- Direct matches (matching filenames, folder structures, or README sections).
- Semantic matches (synonyms or descriptions of commands like `init`, `spec`, `plan`).
- Behavioral signals (unit tests or scripts asserting functionality).

---

## 2. Requirement Matching Summary

### A. README Pitch & positioning
- **Requirement**: The README should intro the toolkit as a "lightweight, opinionated toolkit for building software with specs before code" and include sections like "Why this exists", "What coding-spec does", and "Core workflow".
- **Codebase Match**: `coding-spec/README.md` exists, but its content describes the *agent skill for spec drift auditing* (how to copy the folder, run the parser, etc.) rather than the *coding-spec toolkit* (CLI, templates, prompts) described in the spec.
- **Verdict**: Mismatch / Stale alignment.

### B. Repo structure
- **Requirement**: Codebase should organize directories under `docs/`, `templates/`, `examples/`, `prompts/`, `src/`, and `tests/`.
- **Codebase Match**:
  - `docs/` folder: **Missing**.
  - `templates/` folder: **Missing**.
  - `prompts/` folder: **Missing**.
  - `src/` folder: **Missing**.
  - `tests/` folder: **Missing** (only the skill's parser tests exist under `coding-spec/scripts/`).
- **Verdict**: No matches (0% structurally aligned).

### C. First Three Commands to Ship (`init`, `spec`, `plan`)
- **Requirement**: CLI commands to initialize projects, generate specs, and convert specs to plans.
- **Codebase Match**: No python src/CLI codebase or executable exists in the repository. The only script is `coding-spec/scripts/spec-parse.py`, which is a utility for the skill, not the toolkit CLI.
- **Verdict**: No match.

### D. Roadmap Phases (Phases 1–4)
- **Requirement**: Add template files, CLI commands, review checklists, validation rules, snapshot tests, CI checks, benchmark examples.
- **Codebase Match**: No templates or validators exist.
- **Verdict**: No match.
