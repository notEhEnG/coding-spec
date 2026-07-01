# coding-spec

> **Build with specs, plan with confidence, code with trust.**

`coding-spec` is a lightweight, opinionated toolkit for spec-driven software development. It helps solo developers and small teams bridge the gap between initial requirements and execution by enforcing a clear, markdown-first workflow before writing code.

---

## 1. Why this exists

AI coding assistants are extremely fast, but their output quality degrades rapidly when requirements are vague or incomplete. `coding-spec` solves this by:
1. Making **specifications** the source of truth before code generation.
2. Converting approved specs into actionable **technical plans**.
3. Deconstructing plans into concrete **tasks** and **review checklists**.
4. Enforcing **validation rules** to catch missing test strategies or ambiguous scope early.

---

## 2. What it generates

Running `coding-spec` scaffolds a clean, markdown-first workspace:
- **`templates/`**: Base markdown configurations for specs, plans, tasks, and reviews.
- **`docs/specs/`**: Feature specifications capturing intent and acceptance criteria.
- **`docs/plans/`**: System design docs detailing databases, APIs, and step-by-step tasks.
- **`constitution.template.md`**: Alignment rules for AI coding assistants.

---

## 3. Why use this instead of prompting AI directly?

- **Zero Prompt Drift**: AI models perform significantly better when handed structured Markdown context rather than conversational, unstructured instructions.
- **Strict Verification**: The built-in validator flags missing acceptance criteria, test considerations, and out-of-scope creep before you commit to coding.
- **Repeatable Discipline**: Provides a simple process that solo builders can complete in minutes.

---

## 4. Quickstart

```bash
# Initialize project workspace and templates
python3 phases/src/cli.py init

# Scaffolder a new feature spec from a prompt
python3 phases/src/cli.py spec "User Invitations"

# Validate spec for completeness (acceptance criteria, test strategies, scope)
python3 phases/src/cli.py validate docs/specs/user-invitations.md

# Convert spec into a technical plan
python3 phases/src/cli.py plan docs/specs/user-invitations.md
```
