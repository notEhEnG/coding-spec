#!/usr/bin/env bash
#
# Install coding-spec as an agent skill so it can be triggered with /coding-spec.
#
# Usage:
#   ./install.sh [claude|antigravity|codex|all] [--dir TARGET_PROJECT]
#
# Run it from inside a clone of the repo, or pipe it straight from GitHub:
#   curl -fsSL https://raw.githubusercontent.com/notEhEnG/coding-spec/main/install.sh | bash -s -- claude
#
# It copies the whole repository (SKILL.md + toolkit CLI + auditor) into the
# tool's skill directory under the target project, so /coding-spec can drive
# both the toolkit and the auditor.

set -euo pipefail

REPO_URL="https://github.com/notEhEnG/coding-spec.git"
TOOL="claude"
TARGET_DIR="$PWD"

# --- parse args ---
while [ $# -gt 0 ]; do
  case "$1" in
    claude|antigravity|codex|all) TOOL="$1"; shift ;;
    --dir) TARGET_DIR="${2:?--dir needs a path}"; shift 2 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# --- locate the source (this repo, or clone it) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" >/dev/null 2>&1 && pwd || true)"
CLEANUP=""
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ] && [ -f "$SCRIPT_DIR/src/cli.py" ]; then
  SRC="$SCRIPT_DIR"
else
  echo "Cloning $REPO_URL ..."
  SRC="$(mktemp -d)"
  CLEANUP="$SRC"
  git clone --depth 1 "$REPO_URL" "$SRC" >/dev/null 2>&1
fi

copy_into() {
  local dest="$1"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a \
      --exclude '.git' --exclude '.claude' --exclude '.antigravity' --exclude '.codex' \
      --exclude '__pycache__' --exclude '*.pyc' --exclude '.pytest_cache' \
      --exclude 'phases' --exclude 'dist' --exclude 'node_modules' --exclude '.venv' \
      "$SRC"/ "$dest"/
  else
    # Fallback without rsync: copy then prune the noise.
    cp -R "$SRC"/. "$dest"/
    rm -rf "$dest/.git" "$dest/.claude" "$dest/.antigravity" "$dest/.codex" \
           "$dest/phases" "$dest/dist" "$dest/node_modules" "$dest/.venv" "$dest/.pytest_cache"
    find "$dest" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
    find "$dest" -name '*.pyc' -delete 2>/dev/null || true
  fi
  echo "  Installed skill at: $dest/SKILL.md"
}

install_tool() {
  case "$1" in
    claude)      copy_into "$TARGET_DIR/.claude/skills/coding-spec" ;;
    antigravity) copy_into "$TARGET_DIR/.antigravity/skills/coding-spec" ;;
    codex)       copy_into "${CODEX_SKILLS_DIR:-$TARGET_DIR/.codex/skills}/coding-spec" ;;
    *) echo "Unknown tool: $1" >&2; exit 2 ;;
  esac
}

echo "Installing coding-spec skill (tool: $TOOL) into: $TARGET_DIR"
if [ "$TOOL" = "all" ]; then
  install_tool claude
  install_tool antigravity
  install_tool codex
else
  install_tool "$TOOL"
fi

[ -n "$CLEANUP" ] && rm -rf "$CLEANUP"

cat <<'EOF'

Done. Trigger it with:
  /coding-spec init
  /coding-spec spec "Your Feature"
  /coding-spec audit docs/specs/your-feature.md

Or just ask your agent: "install this skill https://github.com/notEhEnG/coding-spec"
EOF
