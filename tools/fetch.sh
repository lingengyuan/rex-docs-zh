#!/usr/bin/env bash
# 抓取官方文档原文，保存到 originals/ 并更新 manifest。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="https://www.superlogical.com/rex/docs"
LIST="$ROOT/pages.txt"
OUT="$ROOT/originals"
MANIFEST="$OUT/manifest.tsv"

sha256() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

mkdir -p "$OUT"
printf '# page\tsha256\tfetched_at\n' > "$MANIFEST.new"

while IFS= read -r page; do
  case "$page" in ''|'#'*) continue ;; esac
  dest="$OUT/$page.md"
  mkdir -p "$(dirname "$dest")"
  curl -fsS "$BASE/$page.md" -o "$dest"
  sha="$(sha256 "$dest")"
  fetched_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s\t%s\t%s\n' "$page" "$sha" "$fetched_at" >> "$MANIFEST.new"
  echo "fetched $page"
done < "$LIST"

mv "$MANIFEST.new" "$MANIFEST"
echo "manifest: $MANIFEST"
