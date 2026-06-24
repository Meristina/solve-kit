#!/usr/bin/env bash
# install-claude.sh — install the Solve-Kit command pack into ~/.claude.
# Commands become /solve.<name> ; the engine they invoke = the agents + skills mirror.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"

mkdir -p "$DEST/commands" "$DEST/agents" "$DEST/skills"

# 1) Commands → /solve.<name>  (spec-kit-style dotted namespace)
for f in "$ROOT"/.solve/commands/*.md; do
  name="$(basename "$f" .md)"
  cp "$f" "$DEST/commands/solve.${name}.md"
done

# 2) The engine the commands drive: the Claude mirror (agents + skills)
cp "$ROOT"/agents/*.md "$DEST/agents/"
cp -R "$ROOT"/skills/* "$DEST/skills/"

echo "Installed into $DEST :"
echo "  commands : $(ls "$ROOT"/.solve/commands/*.md | wc -l | tr -d ' ') → /solve.<name>"
echo "  agents   : $(ls "$ROOT"/agents/*.md | wc -l | tr -d ' ')"
echo "  skills   : $(ls -d "$ROOT"/skills/*/ | wc -l | tr -d ' ')"
echo "Try:  /solve.mission \"<your problem>\""
