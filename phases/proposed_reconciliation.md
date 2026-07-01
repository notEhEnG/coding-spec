# Proposed Reconciliation & Action Plan

**Target Spec**: [coding-spec-package.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/coding-spec/coding-spec-package.md)  
**Timestamp**: 2026-06-29T22:46:40+08:00

---

## 1. Relocation of the Auditing Skill
To keep the root of the repository clean for the actual `coding-spec` CLI tool (as defined in the spec), the current auditing skill files should be relocated:

- Move `coding-spec/` (containing `SKILL.md`, `Checklist.md`, `INSTALL.md`, `references/`, `scripts/`) to `.antigravity/skills/coding-spec/` or `.claude/skills/coding-spec/`.
- This ensures that when a developer clones the repository, the root contains the package implementation and documentation, and the agent skill remains an extension under the standard skill directory.

---

## 2. CLI Draft Demonstration
We have implemented a fully functional draft of the CLI tool inside [cli_draft.py](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/cli_draft.py) that satisfies the Phase 1 Roadmap commands:

1. **`init`**: Scaffolds the expected directories and copies base templates from the templates directory:
   ```bash
   python3 phases/cli_draft.py init --dir my-new-project
   ```
2. **`spec`**: Generates a custom feature spec draft based on user input:
   ```bash
   python3 phases/cli_draft.py spec "Add team billing" --dir my-new-project
   ```
3. **`plan`**: Transforms a written spec into a technical plan skeleton:
   ```bash
   python3 phases/cli_draft.py plan my-new-project/docs/specs/add-team-billing.md --dir my-new-project
   ```

---

## 3. Template Scaffolding
The base templates described in the spec have been drafted in [phases/templates/](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/):
- [spec.template.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/spec.template.md)
- [plan.template.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/plan.template.md)
- [tasks.template.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/tasks.template.md)
- [review.template.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/review.template.md)
- [constitution.template.md](file:///home/bryan04/gemini/agy/coding-projects/oss/coding-spec/phases/templates/constitution.template.md)
