# Phase 4 — Classify Report

**Target Spec**: [coding-spec-package.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/coding-spec/coding-spec-package.md)  
**Timestamp**: 2026-06-29T22:45:20+08:00

---

## 1. Classification Summary
Following the portable `drift-heuristics.md` rules, we classify each requirement from the spec:

| Req ID | Title | Group | Status | Confidence | Reasoning |
|---|---|---|---|---|---|
| **CS-PKG-RD-01** | Stay lightweight and opinionated | `README pitch` | **Needs Review** | High | Subjective product direction guideline. |
| **CS-PKG-POS-01** | Simpler alternative to Spec Kit | `Positioning` | **Needs Review** | High | Positioning claim, not directly checkable in code. |
| **CS-PKG-RM-01** | One-paragraph README intro | `README pitch` | **Drifted** | High | A `README.md` exists, but describes the auditing skill rather than the toolkit CLI. |
| **CS-PKG-RM-02** | Suggested README sections | `README pitch` | **Drifted** | High | The sections in the current `README.md` do not match the spec sections. |
| **CS-PKG-DIR-01** | Root directories (`docs`, `src`, etc.) | `Repo structure` | **Not Started** | High | None of the expected folders exist in the repository root. |
| **CS-PKG-CMD-01** | `init` command | `First three commands` | **Not Started** | High | No CLI executable or commands exist in the source code. |
| **CS-PKG-CMD-02** | `spec` command | `First three commands` | **Not Started** | High | No CLI executable or commands exist in the source code. |
| **CS-PKG-CMD-03** | `plan` command | `First three commands` | **Not Started** | High | No CLI executable or commands exist in the source code. |
| **CS-PKG-RMP-01** | Phase 1: Make it real milestones | `Roadmap / Phase 1` | **Not Started** | High | Templates, CLI, and demo feature are completely missing. |
| **CS-PKG-RMP-02** | Phase 2: Add trust milestones | `Roadmap / Phase 2` | **Not Started** | High | Validation rules, review checklists, and snapshot tests are missing. |
| **CS-PKG-RMP-03** | Phase 3: Add integrations milestones | `Roadmap / Phase 3` | **Not Started** | High | Agent export modes and CI checks are missing. |
| **CS-PKG-RMP-04** | Phase 4: Differentiate milestones | `Roadmap / Phase 4` | **Not Started** | High | Scorecards and catalog are missing. |
| **CS-PKG-ADV-01** | Avoid universal operating system | `Blunt product advice` | **Needs Review** | High | Subjective product advice. |

---

## 2. Overall Spec-to-Code Alignment Score
- **Total Requirements**: 13
- **Aligned**: 0 (0%)
- **Partial**: 0 (0%)
- **Drifted**: 2 (15.4%)
- **Not Started**: 8 (61.5%)
- **Needs Review**: 3 (23.1%)

### ⚠️ Critical Gaps Detected (Drift Hotspots)
- **Codebase Role Discrepancy**: The repository contains the **verification tool (the skill)** rather than the **target product (the toolkit)**. 
- **Action Plan**: To kick off the actual `coding-spec` product, the codebase needs to be initialized (e.g. running `coding-spec init` or manually setting up `src/`, `templates/`, and `docs/` in the root).
