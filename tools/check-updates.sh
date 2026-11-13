#!/usr/bin/env bash
# 对比线上原文与 originals/ 快照，列出发生变化的页面。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="https://www.superlogical.com/rex/docs"
MANIFEST="$ROOT/originals/manifest.tsv"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

sha256() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

if [ ! -f "$MANIFEST" ]; then
  echo "缺少 $MANIFEST，先运行 tools/fetch.sh" >&2
  exit 1
fi

changed=0
missing=0

while IFS=$'\t' read -r page sha fetched_at; do
  case "$page" in ''|'#'*) continue ;; esac
  file="$TMP/page.md"
  if ! curl -fsS "$BASE/$page.md" -o "$file"; then
    echo "MISSING $page"
    missing=$((missing + 1))
    continue
  fi
  now="$(sha256 "$file")"
  if [ "$now" != "$sha" ]; then
    echo "CHANGED $page (snapshot $fetched_at)"
    changed=$((changed + 1))
  fi
done < "$MANIFEST"

echo "---"
echo "changed: $changed, missing: $missing"
[ "$changed" -eq 0 ] && [ "$missing" -eq 0 ]
