#!/usr/bin/env bash
# new-mission.sh — allocate the next mission folder and seed its dossier.
# Usage: .solve/scripts/sh/new-mission.sh "<one-line problem>"
# Prints the created mission directory path (so a command can chain on it).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PROBLEM="${1:-}"
if [ -z "$PROBLEM" ]; then
  echo "usage: new-mission.sh \"<one-line problem>\"" >&2
  exit 1
fi

MISSIONS="$ROOT/missions"
mkdir -p "$MISSIONS"

# next zero-padded NNN
LAST=$(ls -1 "$MISSIONS" 2>/dev/null | grep -E '^[0-9]{3}-' | sed -E 's/^([0-9]{3}).*/\1/' | sort -n | tail -1 || true)
NEXT=$(printf "%03d" $(( 10#${LAST:-000} + 1 )))

# slug from the problem (lowercase, alnum -> dashes, trimmed, max 6 words)
SLUG=$(printf '%s' "$PROBLEM" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs 'a-z0-9' '-' \
  | sed -E 's/^-+//; s/-+$//' \
  | cut -d'-' -f1-6)
SLUG="${SLUG:-mission}"

DIR="$MISSIONS/${NEXT}-${SLUG}"
mkdir -p "$DIR"

# seed dossier.md from the template, filling the obvious placeholders
TPL="$ROOT/.solve/templates/dossier-template.md"
sed -e "s/{{MISSION_ID}}/${NEXT}-${SLUG}/g" \
    -e "s|{{ONE_LINE_PROBLEM}}|${PROBLEM}|g" \
    "$TPL" > "$DIR/dossier.md"

echo "$DIR"
