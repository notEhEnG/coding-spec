# Install and trigger `coding-spec` (auditor-only bundle)

This package uses the portable `SKILL.md` format so the same skill can be reused across agent tools that support it.

> **Want the full toolkit too?** This subfolder is the standalone **drift auditor**. To get `/coding-spec` driving the whole toolkit (`init`, `spec`, `plan`, `validate`, `review`, `export`, `ci`) *and* the auditor, install the **whole repository** as a skill instead — see the root [`README.md`](../README.md#use-it-as-an-agent-skill-coding-spec) or run `./install.sh`. Copy just this subfolder only if you want the auditor and nothing else.

## Before you install

This skill ships inside the [coding-spec monorepo](https://github.com/notEhEnG/coding-spec) as the `coding-spec/` **subfolder**. Copy that subfolder into your project's skill directory — do not copy the entire repository.

After install, the main file must be reachable as `<skill-dir>/coding-spec/SKILL.md`.

## Claude Code

Project install:

1. Clone or download the repository.
2. Copy the `coding-spec/` subfolder into `.claude/skills/`.
3. Final path: `.claude/skills/coding-spec/SKILL.md`.
4. Use `SKILL.md` as the canonical launcher and workflow reference.
5. Invoke with `/coding-spec path/to/spec.md` or `/coding-spec reverse-spec` when your Claude Code setup maps skills to slash commands.

```bash
mkdir -p .claude/skills
cp -r /path/to/coding-spec/coding-spec/ .claude/skills/coding-spec/
```

Why this works:

- Claude Code supports `SKILL.md` skills.
- A skill directory under `.claude/skills/<name>/SKILL.md` can be mapped to `/<name>`.
- Custom slash commands are support-dependent; `/coding-spec` works when your client exposes skill slash mapping.

## Antigravity IDE

Project install:

1. Copy the `coding-spec/` subfolder into `.antigravity/skills/`.
2. Final path: `.antigravity/skills/coding-spec/SKILL.md`.
3. Use `SKILL.md` as the canonical launcher and workflow reference.
4. Invoke with `/coding-spec path/to/spec.md` or assign the skill to a reviewer/architect agent in Manager View.

```bash
mkdir -p .antigravity/skills
cp -r /path/to/coding-spec/coding-spec/ .antigravity/skills/coding-spec/
```

Why this works:

- Antigravity supports `SKILL.md` skills.
- Project skills live in `.antigravity/skills/`.
- The same skill format is portable across compatible agent tools.

## Codex-compatible skill loaders

Recommended install:

1. Copy the `coding-spec/` subfolder into the skill directory your Codex environment watches.
2. Preserve the folder name `coding-spec` so the command identity remains stable.
3. Use `SKILL.md` as the canonical launcher and workflow reference.
4. Invoke with `/coding-spec path/to/spec.md` only when your Codex wrapper exposes slash-style skill commands.

Notes:

- Codex ecosystem support often follows the same open `SKILL.md` conventions rather than one single canonical path.
- If your wrapper uses namespaced or menu-based skills instead of literal slash commands, keep the directory name `coding-spec` and map it in your launcher config.

## Suggested trigger phrases

These help both automatic and explicit invocation:

- check spec drift
- validate my implementation
- are we on track
- sync the living doc
- update the spec
- is feature X done?
- generate a spec from the code

## Example invocations

See `SKILL.md` for the full invocation contract. Common examples:

- `/coding-spec phase-1`
- `/coding-spec docs/prd.md`
- `/coding-spec audit path/to/spec.md`
- `/coding-spec patch path/to/spec.md`
- `/coding-spec reverse-spec`
- `/coding-spec release-check`