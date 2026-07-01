# Phase 2 — Fingerprint Report

**Target Spec**: [coding-spec-package.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/coding-spec/coding-spec-package.md)  
**Timestamp**: 2026-06-29T22:45:00+08:00

---

## 1. Codebase Fingerprint Overview
A complete scan of the current repository was performed to identify files, directories, config files, and tests.

### Current Directory Structure
```text
/home/bryan04/gemini/agy/coding-projects/oss/coding-spec/
├── .git/
├── .gitignore
└── coding-spec/
    ├── Checklist.md
    ├── INSTALL.md
    ├── LICENSE
    ├── README.md
    ├── SKILL.md
    ├── coding-spec-package.md (Spec File)
    ├── references/
    │   ├── drift-heuristics.md
    │   └── sdd-patterns.md
    └── scripts/
        ├── fixtures/
        │   ├── acceptance_section.md
        │   ├── checklist_atomic.md
        │   ├── compound_narrative.md
        │   ├── false_positive_willow.md
        │   ├── nested_sections.md
        │   └── non_goal_section.md
        ├── spec-parse.py
        └── test_spec_parse.py
```

---

## 2. Key Observations
1. **Tool vs. Skill Split**: The current repository contains the code and configuration for the **agentic skill bundle** (under the `coding-spec/` subfolder). This skill bundle implements spec drift audits for LLM agents.
2. **Missing Implementation Files**: None of the folders or files specified for the `coding-spec` **CLI tool package** exist in the repository root. Specifically, the following expected components are missing:
   - `docs/` (`philosophy.md`, `workflow.md`, etc.)
   - `templates/` (`spec.template.md`, `plan.template.md`, etc.)
   - `examples/` (`feature-team-billing/`, `bugfix-checkout-tax/`)
   - `prompts/` (`feature.txt`, `refactor.txt`, etc.)
   - `src/` (`cli/`, `commands/`, `generators/`, etc.)
   - `tests/` (except the parser tests under the `coding-spec/scripts/` directory)
   - `.github/workflows/`

---

## 3. Evidence Categories Identified
- **Skill Configuration**: `coding-spec/SKILL.md` defines the agent execution contract.
- **Skill Documentation**: `coding-spec/README.md` and `coding-spec/INSTALL.md` provide installation instructions.
- **Python Parser**: `coding-spec/scripts/spec-parse.py` parses specs into JSON.
- **Parser Unit Tests**: `coding-spec/scripts/test_spec_parse.py` and its fixtures run successfully.
