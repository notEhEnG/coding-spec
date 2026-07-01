# Install and trigger `coding-spec`

This package uses the portable `SKILL.md` format so the same core skill can be reused across agent tools that support the format.

## Claude Code

Project install:
1. Copy `coding-spec/` into `.claude/skills/`.
2. Final path should be `.claude/skills/coding-spec/SKILL.md`.
3. Use `Checklist.md` as the launcher prompt sheet.
4. Invoke with `/coding-spec path/to/spec.md` or `/coding-spec reverse-spec` if your Claude Code setup maps skills to slash commands.

Why this works:
- Claude Code supports `SKILL.md` skills.
- A skill directory under `.claude/skills/<name>/SKILL.md` becomes `/<name>`.
- Custom slash commands have been merged into skills, so `coding-spec` is directly invocable as `/coding-spec`.

## Codex-compatible skill loaders

Recommended install:
1. Copy `coding-spec/` into the skill directory your Codex environment watches.
2. Preserve the folder name `coding-spec` so the slash command remains stable.
3. Use `Checklist.md` as the canonical prompt sheet.
4. Invoke it with `/coding-spec path/to/spec.md` only when your Codex wrapper exposes slash-style skill commands.

Notes:
- Codex ecosystem support is often implemented through the same open `SKILL.md` conventions rather than one single canonical path.
- If your wrapper exposes namespaced or menu-based skills instead of literal slash commands, keep the skill directory name unchanged and map it to `coding-spec`.

## Antigravity IDE

Project install:
1. Copy `coding-spec/` into `.antigravity/skills/`.
2. Final path should be `.antigravity/skills/coding-spec/SKILL.md`.
3. Use `Checklist.md` as the canonical prompt sheet.
4. Invoke with `/coding-spec path/to/spec.md` or assign the skill to a reviewer/architect agent in Manager View if your Antigravity setup exposes that mapping.

Why this works:
- Antigravity supports `SKILL.md` skills.
- Project skills live in `.antigravity/skills/`.
- The same skill format is intended to be portable across compatible agent tools.

## Suggested trigger phrases

These should help both automatic and explicit invocation:
- check spec drift
- validate my implementation
- are we on track
- sync the living doc
- update the spec
- is feature X done?
- generate a spec from the code

## Example invocations
- `/coding-spec docs/prd.md`
- `/coding-spec specs/export-flow.md`
- `/coding-spec reverse-spec`
