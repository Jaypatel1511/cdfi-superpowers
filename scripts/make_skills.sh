#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$ROOT/skills"
DIST_DIR="$ROOT/dist"

mkdir -p "$DIST_DIR"

for skill_path in "$SKILLS_DIR"/*/; do
  name="$(basename "$skill_path")"
  if [ ! -f "$skill_path/SKILL.md" ]; then
    echo "SKIP $name (no SKILL.md at root)" >&2
    continue
  fi
  out="$DIST_DIR/$name.skill"
  rm -f "$out"
  ( cd "$skill_path" && zip -q -r -X "$out" . -x '.*' )
  echo "built $out"
done

echo "done: $(ls -1 "$DIST_DIR"/*.skill 2>/dev/null | wc -l | tr -d ' ') skill archive(s) in $DIST_DIR"
