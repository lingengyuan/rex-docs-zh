#!/usr/bin/env python3
"""抓取 Rex 官方文档原文，对比本地快照，生成更新报告。

用法：
  tools/sync.py                 抓取并写入 originals/，更新 manifest
  tools/sync.py --dry-run       只检测，不写入
  tools/sync.py --report FILE   把更新报告写入 FILE；没有更新时不生成文件
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://www.superlogical.com/rex/docs"
ROOT = Path(__file__).resolve().parent.parent
PAGES_FILE = ROOT / "pages.txt"
ORIGINALS = ROOT / "originals"
MANIFEST = ORIGINALS / "manifest.tsv"
DOCS = ROOT / "docs"

PAGE_LINK = re.compile(r"https://www\.superlogical\.com/rex/docs/([A-Za-z0-9_./-]+)\.md")
VERSION = re.compile(r"原文版本：([0-9a-f]{7,64})")
HEADERS = {"User-Agent": "rex-docs-zh/1.0", "Accept": "text/markdown"}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def read_pages() -> list[str]:
    pages = []
    for line in PAGES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            pages.append(line)
    return pages


def read_manifest() -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    if not MANIFEST.exists():
        return entries
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        page, sha, fetched_at = line.split("\t")
        entries[page] = (sha, fetched_at)
    return entries


def translation_status(page: str, sha: str) -> str:
    path = DOCS / f"{page}.md"
    if not path.exists():
        return "未翻译"
    match = VERSION.search(path.read_text(encoding="utf-8"))
    if not match:
        return "缺少版本标记"
    return "最新" if sha.startswith(match.group(1)) else "落后"


def build_report(
    date: str,
    changed: list[tuple[str, str]],
    added: list[tuple[str, str]],
    new_pages: list[str],
    removed: list[str],
    errors: list[tuple[str, str]],
    llms_error: str | None,
) -> str:
    lines = [f"## 文档更新 {date}", ""]

    if changed or added:
        lines += ["### 原文变更（%d）" % (len(changed) + len(added)), ""]
        lines += ["| 页面 | 原文 | 译文 |", "| --- | --- | --- |"]
        for page, sha in changed + added:
            url = f"{BASE}/{page}"
            lines.append(f"| `{page}` | [打开]({url}) | {translation_status(page, sha)} |")
        lines.append("")

    if new_pages:
        lines += ["### 新增页面（%d）" % len(new_pages), ""]
        lines += ["以下页面出现在官方 `llms.txt`，但不在 `pages.txt` 中。确认后加入清单再翻译。", ""]
        for page in new_pages:
            lines.append(f"- `{page}` — [原文]({BASE}/{page})")
        lines.append("")

    if removed:
        lines += ["### 线上已删除（%d）" % len(removed), ""]
        lines += ["以下页面仍在 `pages.txt`，但官方 `llms.txt` 已不包含。确认后从清单移除。", ""]
        for page in removed:
            lines.append(f"- `{page}`")
        lines.append("")

    if errors or llms_error:
        lines += ["### 抓取失败", ""]
        if llms_error:
            lines.append(f"- `llms.txt` — {llms_error}")
        for page, message in errors:
            lines.append(f"- `{page}` — {message}")
        lines.append("")

    lines += [
        "### 处理",
        "",
        "1. 合并更新 PR 后，以 `originals/` 中的新原文为准修改 `docs/` 译文。",
        "2. 在译文开头更新 `原文版本：<sha>`。",
        "3. 完成后关闭本 Issue。",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取并对比 Rex 官方文档原文")
    parser.add_argument("--dry-run", action="store_true", help="只检测，不写入")
    parser.add_argument("--report", type=Path, help="更新报告的写入路径")
    args = parser.parse_args()

    pages = read_pages()
    old = read_manifest()
    now = datetime.now(timezone.utc)
    fetched_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    date = now.strftime("%Y-%m-%d")

    remote: set[str] = set()
    llms_error = None
    try:
        remote = set(PAGE_LINK.findall(fetch(f"{BASE}/llms.txt").decode("utf-8")))
    except Exception as exc:  # noqa: BLE001
        llms_error = str(exc)

    changed: list[tuple[str, str]] = []
    added: list[tuple[str, str]] = []
    errors: list[tuple[str, str]] = []
    entries: dict[str, tuple[str, str]] = {}
    fetched_ok = 0

    for page in pages:
        try:
            data = fetch(f"{BASE}/{page}.md")
        except Exception as exc:  # noqa: BLE001
            errors.append((page, str(exc)))
            if page in old:
                entries[page] = old[page]
            continue

        fetched_ok += 1
        sha = hashlib.sha256(data).hexdigest()
        # 仅用于测试分支：模拟 installation 原文变化。
        if page == "installation":
            data += b"\n<!-- workflow simulation -->\n"
            sha = hashlib.sha256(data).hexdigest()
        previous = old.get(page)
        if previous and previous[0] == sha:
            entries[page] = previous
            continue

        if previous:
            changed.append((page, sha))
        else:
            added.append((page, sha))
        entries[page] = (sha, fetched_at)

        if not args.dry_run:
            path = ORIGINALS / f"{page}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    if not args.dry_run:
        lines = ["# page\tsha256\tfetched_at"]
        for page in pages:
            if page in entries:
                sha, stamp = entries[page]
                lines.append(f"{page}\t{sha}\t{stamp}")
        MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")

    new_pages = sorted(remote - set(pages)) if remote else []
    removed = sorted(set(pages) - remote) if remote else []
    findings = bool(changed or added or new_pages or removed or errors or llms_error)

    if args.report:
        if findings:
            args.report.write_text(
                build_report(date, changed, added, new_pages, removed, errors, llms_error),
                encoding="utf-8",
            )
        elif args.report.exists():
            args.report.unlink()

    for page, _ in changed:
        print(f"CHANGED {page}")
    for page, _ in added:
        print(f"ADDED {page}")
    for page in new_pages:
        print(f"NEW {page}")
    for page in removed:
        print(f"REMOVED {page}")
    for page, message in errors:
        print(f"ERROR {page}: {message}", file=sys.stderr)
    if llms_error:
        print(f"ERROR llms.txt: {llms_error}", file=sys.stderr)
    print(
        f"changed: {len(changed)}, added: {len(added)}, new: {len(new_pages)}, "
        f"removed: {len(removed)}, errors: {len(errors)}"
    )

    if pages and fetched_ok == 0:
        print("error: 所有页面抓取失败", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
