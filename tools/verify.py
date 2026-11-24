#!/usr/bin/env python3
"""Rex 文档中文翻译独立程序化验证脚本 (Rex Docs Translation Verification Tool)

严格对照 ORIGINAL_REQUEST.md、PROJECT.md 与 TEST_INFRA.md 中的 7 项验收标准（AC1 ~ AC7）进行自动化检查。
不依赖任何第三方 Python 包，仅使用 Python 3 标准库。
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import re
import sys
from typing import Any

# 项目基准路径
ROOT = Path(__file__).resolve().parent.parent
ORIGINALS_DIR = ROOT / "originals"
DOCS_DIR = ROOT / "docs"
MANIFEST_FILE = ORIGINALS_DIR / "manifest.tsv"
TASKS_FILE = ROOT / "TRANSLATION-TASKS.md"

# 英文常见语法停用词表（用于检测未翻译的整段英文）
EN_STOP_WORDS = {
    "the", "and", "is", "in", "to", "of", "that", "with", "for", "on",
    "it", "as", "by", "this", "are", "from", "at", "be", "or", "an",
    "will", "my", "your", "all", "have", "not", "but", "when", "they",
    "we", "you", "can", "if", "more", "also", "into", "has", "use",
}

# 允许作为纯英文标题出现的专有名词/缩写/系统平台名称
ALLOWED_HEADING_TERMS = {
    "cli", "path", "nix", "macos", "linux", "windows", "freebsd", "ios",
    "api", "lua", "ssh", "pam", "msi", "zip", "winget", "tailscale",
    "json", "rpc", "osc", "mcp", "rex",
}


@dataclass
class CheckResult:
    """单个验收检查项结果"""
    page: str
    criterion: str
    passed: bool
    message: str = ""


@dataclass
class Report:
    """验证总报告"""
    results: list[CheckResult] = field(default_factory=list)

    def add(self, page: str, criterion: str, passed: bool, message: str = "") -> None:
        self.results.append(CheckResult(page=page, criterion=criterion, passed=passed, message=message))

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def total_checks(self) -> int:
        return len(self.results)

    @property
    def passed_checks(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed_checks(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    def summary(self) -> dict[str, Any]:
        failures = [
            {"page": r.page, "ac": r.criterion, "error": r.message}
            for r in self.results if not r.passed
        ]
        return {
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "all_passed": self.passed,
            "failures": failures,
            "results": [asdict(r) for r in self.results],
        }


def read_manifest(manifest_path: Path = MANIFEST_FILE) -> dict[str, tuple[str, str]]:
    """读取 originals/manifest.tsv，返回 {page_id: (sha12, date10)}"""
    manifest: dict[str, tuple[str, str]] = {}
    if not manifest_path.exists():
        return manifest
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            page, sha, fetched_at = parts[0], parts[1], parts[2]
            manifest[page] = (sha[:12], fetched_at[:10])
    return manifest


def read_tasks(tasks_path: Path = TASKS_FILE) -> tuple[int, int, int, list[tuple[str, bool]]]:
    """解析 TRANSLATION-TASKS.md

    返回: (remaining, done, total, [(page_id, is_checked)])
    """
    if not tasks_path.exists():
        raise FileNotFoundError(f"任务清单文件不存在: {tasks_path}")
    text = tasks_path.read_text(encoding="utf-8")
    header_m = re.search(r"剩余\s*(\d+)\s*篇[，,]\s*进度\s*(\d+)\s*/\s*(\d+)", text)
    if not header_m:
        raise ValueError("无法解析 TRANSLATION-TASKS.md 顶部进度统计行（期望格式：剩余 X 篇，进度 Y / Z）")
    remaining = int(header_m.group(1))
    done = int(header_m.group(2))
    total = int(header_m.group(3))

    items = re.findall(r"^- \[([ xX])\] `([^`]+)`", text, re.M)
    task_list = [(page.strip(), flag.lower() == "x") for flag, page in items]
    return remaining, done, total, task_list


def strip_code_blocks(text: str) -> tuple[str, list[str]]:
    """移除围栏代码块并提取代码块语言标签

    返回: (剥离代码块后的文本, [语言标签列表])
    """
    langs = re.findall(r"^\s*```(\w*)", text, re.M)[::2]
    clean = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return clean, langs


def extract_headings(text_no_code: str) -> list[tuple[int, str]]:
    """提取纯 Markdown 标题 (层级, 标题内容)"""
    # 剥除 frontmatter
    clean = re.sub(r"^---\n.*?\n---\n?", "", text_no_code, flags=re.DOTALL)
    # 剥除文件头元数据引用块
    clean = re.sub(r"^> 原文.*?\n\n", "", clean, flags=re.DOTALL)
    matches = re.findall(r"^(#{1,6})\s+(.+)$", clean, re.M)
    return [(len(m[0]), m[1].strip()) for m in matches]


def count_tables(text_no_code: str) -> int:
    """统计 Markdown 表格分隔行数量"""
    return len(re.findall(r"^\s*\|?\s*:?-+:?\s*\|(?:\s*:?-+:?\s*\|)*\s*$", text_no_code, re.M))


def check_ac1_existence(page: str, doc_path: Path, report: Report) -> bool:
    """AC1: 检查译文文件是否存在且非空"""
    if not doc_path.exists():
        report.add(page, "AC1_Existence", False, f"译文文件不存在: {doc_path}")
        return False
    if not doc_path.is_file():
        report.add(page, "AC1_Existence", False, f"译文路径不是文件: {doc_path}")
        return False
    if doc_path.stat().st_size == 0:
        report.add(page, "AC1_Existence", False, f"译文文件为空 (0 字节): {doc_path}")
        return False
    report.add(page, "AC1_Existence", True, "文件存在且非空")
    return True


def check_ac4_metadata(
    page: str,
    doc_lines: list[str],
    manifest: dict[str, tuple[str, str]],
    report: Report,
) -> None:
    """AC4: 文件头与版本元数据规范检查"""
    if len(doc_lines) < 2:
        report.add(page, "AC4_Metadata", False, "文件行数不足，缺少标准文件头")
        return

    # 检查整个文档（代码块外部）是否残留 YAML frontmatter
    in_code = False
    for idx, line in enumerate(doc_lines):
        if re.match(r"^\s*```", line):
            in_code = not in_code
            continue
        if not in_code and line.strip() == "---":
            report.add(page, "AC4_Metadata", False, f"文件中发现残留的 YAML frontmatter 标记 ('---')，未按规范删除 (第 {idx + 1} 行)")
            return

    l1, l2 = doc_lines[0], doc_lines[1]

    # 标点符号规范性检查（防止半角冒号或括号）
    if l1.startswith("> 原文:"):
        report.add(page, "AC4_Metadata", False, "文件头第 1 行使用了半角冒号，应为全角中文冒号 '：'")
        return
    if l2.startswith("> 原文版本:"):
        report.add(page, "AC4_Metadata", False, "文件头第 2 行使用了半角冒号，应为全角中文冒号 '：'")
        return
    if "(" in l2 and "（" not in l2:
        report.add(page, "AC4_Metadata", False, "文件头第 2 行使用了半角括号，应为全角中文括号 '（抓取于 ...）'")
        return

    exp_url = f"> 原文：https://www.superlogical.com/rex/docs/{page}"
    if l1 != exp_url:
        report.add(page, "AC4_Metadata", False, f"文件头第 1 行不匹配: 期望 '{exp_url}'，实际为 '{l1}'")
        return

    if page not in manifest:
        report.add(page, "AC4_Metadata", False, f"manifest.tsv 中未找到页面 '{page}' 的版本记录")
        return

    exp_sha, exp_dt = manifest[page]
    exp_ver = f"> 原文版本：{exp_sha}（抓取于 {exp_dt}）"
    if l2 != exp_ver:
        report.add(
            page,
            "AC4_Metadata",
            False,
            f"文件头第 2 行版本元数据不匹配: 期望 '{exp_ver}'，实际为 '{l2}' (SHA 或日期不一致)",
        )
        return

    report.add(page, "AC4_Metadata", True, f"文件头与 manifest.tsv 一致 ({exp_sha}, {exp_dt})")


def check_ac2_structure(
    page: str,
    orig_text: str,
    doc_text: str,
    report: Report,
) -> None:
    """AC2: 结构对齐检查（标题层级序列、单个根 H1、代码块总数与闭合性、表格数量）"""
    # 剥离代码块
    orig_clean, orig_langs = strip_code_blocks(orig_text)
    doc_clean, doc_langs = strip_code_blocks(doc_text)

    # 1. 代码块闭合性与数量
    doc_code_markers = len(re.findall(r"^\s*```", doc_text, re.M))
    if doc_code_markers % 2 != 0:
        report.add(page, "AC2_Structure", False, f"代码块标记未闭合: 发现 {doc_code_markers} 个 '```'")
        return

    orig_code_cnt = len(orig_langs)
    doc_code_cnt = len(doc_langs)
    if orig_code_cnt != doc_code_cnt:
        report.add(
            page,
            "AC2_Structure",
            False,
            f"代码块数量不匹配: 原文 {orig_code_cnt} 个 vs 译文 {doc_code_cnt} 个",
        )
        return

    # 2. 标题层级序列
    orig_headings = extract_headings(orig_clean)
    doc_headings = extract_headings(doc_clean)
    orig_levels = [h[0] for h in orig_headings]
    doc_levels = [h[0] for h in doc_headings]

    if not doc_levels:
        report.add(page, "AC2_Structure", False, "译文中未检测到任何 Markdown 标题")
        return

    if doc_levels[0] != 1:
        report.add(page, "AC2_Structure", False, f"首个标题层级应为 H1 (实际为 H{doc_levels[0]})")
        return

    if doc_levels.count(1) != 1:
        report.add(page, "AC2_Structure", False, f"译文中存在多个 H1 标题 (总计 {doc_levels.count(1)} 个)")
        return

    if orig_levels != doc_levels:
        report.add(
            page,
            "AC2_Structure",
            False,
            f"标题层级序列不匹配: 原文 {orig_levels} vs 译文 {doc_levels}",
        )
        return

    # 3. 表格数量
    orig_tables = count_tables(orig_clean)
    doc_tables = count_tables(doc_clean)
    if orig_tables != doc_tables:
        report.add(
            page,
            "AC2_Structure",
            False,
            f"表格数量不匹配: 原文 {orig_tables} 个 vs 译文 {doc_tables} 个",
        )
        return

    report.add(
        page,
        "AC2_Structure",
        True,
        f"结构完全对齐: {len(doc_levels)} 个标题 (H1={doc_levels.count(1)}), {doc_code_cnt} 个代码块, {doc_tables} 个表格",
    )


def check_ac3_completeness(
    page: str,
    doc_text: str,
    report: Report,
) -> None:
    """AC3: 翻译完整性检查（检测未翻译的整段英文与未翻译标题）"""
    doc_clean, _ = strip_code_blocks(doc_text)

    # 剥离行内代码、完整 URL、Markdown 链接 URL、HTML 标签
    text_no_inline = re.sub(r"`[^`\n]+`", "", doc_clean)
    text_no_url = re.sub(r"https?://\S+", "", text_no_inline)
    # 保留链接文本用于语境检测: [text](url) -> text
    text_clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text_no_url)
    text_clean = re.sub(r"<[^>]+>", "", text_clean)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text_clean) if p.strip()]
    untranslated: list[str] = []

    for p in paragraphs:
        # 跳过文件头元数据引用块
        if p.startswith("> 原文") or p.startswith("> 原文版本"):
            continue

        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", p))
        words = re.findall(r"\b[A-Za-z]{2,}\b", p)
        stop_count = sum(1 for w in words if w.lower() in EN_STOP_WORDS)

        # 标题检测: 标题无任何中文且含有英文单词，非专有名词/平台缩写即判定为未翻译标题
        if p.startswith("#"):
            if cjk_count == 0 and len(words) >= 1:
                # 若标题单词全部属于允许的专有名词/平台缩写，则放行；否则判定为未翻译标题
                if any(w.lower() not in ALLOWED_HEADING_TERMS for w in words):
                    untranslated.append(f"未翻译标题: {p}")
            continue

        # 段落检测判定标准:
        # 1. 语法停用词 >= 4 且中文字符 < 2 (典型未翻译英文段落)
        # 2. 语法停用词 >= 3, 单词 >= 6 且完全无中文字符 (中短英文段落)
        if (stop_count >= 4 and cjk_count < 2) or (stop_count >= 3 and cjk_count == 0 and len(words) >= 6):
            snippet = p.replace("\n", " ")
            if len(snippet) > 60:
                snippet = snippet[:60] + "..."
            untranslated.append(snippet)

    if untranslated:
        preview = "; ".join(untranslated[:3])
        report.add(page, "AC3_Completeness", False, f"发现未翻译的英文内容 ({len(untranslated)} 处): {preview}")
    else:
        report.add(page, "AC3_Completeness", True, "正文无整段英文残留，汉字密度与术语符合规范")


def check_ac5_cleanup(
    page: str,
    orig_text: str,
    doc_text: str,
    report: Report,
) -> None:
    """AC5: 清理导出残留与 <kbd> 标签保留检查"""
    # 在非代码区域检查模板标签
    doc_clean, _ = strip_code_blocks(doc_text)
    # 剥离行内代码，防止帮助文档中的尖括号占位符（如 `rex help <command>`）误判
    doc_no_inline = re.sub(r"`[^`\n]+`", "", doc_clean)

    # 1. 检测 Svelte 指令残留
    svelte_match = re.search(r"\{[#/:][a-zA-Z0-9_]+|\{/(?:if|each|await)\}|\{:(?:else|then|catch)\}", doc_no_inline)
    if svelte_match:
        report.add(page, "AC5_TemplateCleanup", False, f"发现未清理的 Svelte 模板标记: '{svelte_match.group(0)}'")
        return

    # 2. 检测导出组件标签残留 (<OsIcon>, <Tag>)
    comp_match = re.search(r"</?(?:OsIcon|Tag)\b", doc_no_inline)
    if comp_match:
        report.add(page, "AC5_TemplateCleanup", False, f"发现未清理的导出组件标签: '{comp_match.group(0)}'")
        return

    # 3. 检测未转换为 Markdown 的 HTML 标题标签 (<h1-6>)
    h_match = re.search(r"</?h[1-6]\b", doc_no_inline)
    if h_match:
        report.add(page, "AC5_TemplateCleanup", False, f"发现未转换的 HTML 标题标签: '{h_match.group(0)}'")
        return

    # 4. 检测 <kbd> 标签保留数量
    orig_kbd_count = len(re.findall(r"<kbd>.*?</kbd>", orig_text))
    doc_kbd_count = len(re.findall(r"<kbd>.*?</kbd>", doc_text))
    if orig_kbd_count != doc_kbd_count:
        report.add(
            page,
            "AC5_TemplateCleanup",
            False,
            f"<kbd> 标签数量不一致: 原文 {orig_kbd_count} 个 vs 译文 {doc_kbd_count} 个",
        )
        return

    # 5. windows/installation.md 必须包含特定后备文本
    if page == "windows/installation":
        fallback_text = "使用 Discord 登录后，此处会显示下载链接。"
        if fallback_text not in doc_text:
            report.add(
                page,
                "AC5_TemplateCleanup",
                False,
                f"windows/installation.md 缺少必需的静态后备文本: '{fallback_text}'",
            )
            return

    report.add(
        page,
        "AC5_TemplateCleanup",
        True,
        f"模板标记清理干净，<kbd> 标签完全保留 ({doc_kbd_count} 个)",
    )


def check_ac6_links(
    page: str,
    doc_path: Path,
    doc_text: str,
    report: Report,
) -> None:
    """AC6: 内部链接有效性检查"""
    doc_clean, _ = strip_code_blocks(doc_text)
    # 排除文件头引用块
    clean = re.sub(r"^> 原文.*?\n\n", "", doc_clean, flags=re.DOTALL)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", clean)

    broken_links: list[str] = []
    rel_count = 0

    for title, target in links:
        target_path = target.split("#")[0]
        # 跳过空路径（纯页面内锚点 #...）、邮件链接
        if not target_path or target.startswith("mailto:"):
            continue

        # 检查是否为指向已翻译页面的官方文档 URL (https://www.superlogical.com/rex/docs/...)
        official_prefix = "https://www.superlogical.com/rex/docs/"
        official_prefix_http = "http://www.superlogical.com/rex/docs/"
        if target.startswith(official_prefix) or target.startswith(official_prefix_http):
            pfx = official_prefix if target.startswith("https://") else official_prefix_http
            raw_target = target_path[len(pfx):].rstrip("/")
            if raw_target.endswith(".md"):
                raw_target = raw_target[:-3]
            target_md = DOCS_DIR / f"{raw_target}.md"
            if target_md.exists() and target_md.is_file():
                broken_links.append(f"[{title}]({target}) -> 链接指向已翻译页面，应转换为相对路径: docs/{raw_target}.md")
            continue

        # 跳过其他外部 HTTP/HTTPS 链接
        if target.startswith("http://") or target.startswith("https://"):
            continue

        rel_count += 1
        # 解析相对路径目标文件
        try:
            resolved = (doc_path.parent / target_path).resolve()
        except Exception as exc:
            broken_links.append(f"[{title}]({target}) -> 路径解析错误: {exc}")
            continue

        # 路径遍历越界检查 (必须在项目根目录之内)
        boundary = ROOT if doc_path.resolve().is_relative_to(ROOT) else doc_path.parent.resolve()
        if not resolved.is_relative_to(boundary):
            broken_links.append(f"[{title}]({target}) -> 相对链接越界 (超出项目根目录): {target_path}")
            continue

        if not resolved.exists() or not resolved.is_file():
            broken_links.append(f"[{title}]({target}) -> 目标不存在: {target_path}")

    if broken_links:
        report.add(
            page,
            "AC6_InternalLinks",
            False,
            f"发现破坏或未转换的内部相对链接 ({len(broken_links)} 处): {'; '.join(broken_links)}",
        )
    else:
        report.add(
            page,
            "AC6_InternalLinks",
            True,
            f"所有相对链接有效 ({rel_count} 个相对链接已验证解析)",
        )


def check_document(page: str, manifest: dict[str, tuple[str, str]], report: Report) -> None:
    """对单篇文档执行 AC1 ~ AC6 完整检查"""
    doc_path = DOCS_DIR / f"{page}.md"
    orig_path = ORIGINALS_DIR / f"{page}.md"

    # AC1: Existence
    if not check_ac1_existence(page, doc_path, report):
        report.add(page, "AC4_Metadata", False, f"译文文件不存在: {doc_path}")
        report.add(page, "AC2_Structure", False, f"译文文件不存在: {doc_path}")
        report.add(page, "AC3_Completeness", False, f"译文文件不存在: {doc_path}")
        report.add(page, "AC5_TemplateCleanup", False, f"译文文件不存在: {doc_path}")
        report.add(page, "AC6_InternalLinks", False, f"译文文件不存在: {doc_path}")
        return

    doc_text = doc_path.read_text(encoding="utf-8")
    doc_lines = doc_text.splitlines()

    orig_text = orig_path.read_text(encoding="utf-8") if orig_path.exists() else ""

    # AC4: Metadata
    check_ac4_metadata(page, doc_lines, manifest, report)

    # AC2: Structure Parity
    check_ac2_structure(page, orig_text, doc_text, report)

    # AC3: Completeness
    check_ac3_completeness(page, doc_text, report)

    # AC5: Cleanup
    check_ac5_cleanup(page, orig_text, doc_text, report)

    # AC6: Links
    check_ac6_links(page, doc_path, doc_text, report)


def check_ac7_checklist(
    manifest: dict[str, tuple[str, str]],
    report: Report,
    require_completed: bool = True,
    tasks_path: Path = TASKS_FILE,
) -> None:
    """AC7: 任务清单与进度同步检查"""
    try:
        rem, done, total, task_list = read_tasks(tasks_path)
    except Exception as exc:
        report.add(tasks_path.name, "AC7_Checklist", False, f"读取任务清单失败: {exc}")
        return

    # 1. 任务清单总数必须严格为 31
    if total != 31:
        report.add(tasks_path.name, "AC7_Checklist", False, f"头部统计总篇数应为 31，实际为 {total}")
        return

    if len(task_list) != 31:
        report.add(tasks_path.name, "AC7_Checklist", False, f"清单中条目总数应为 31，实际为 {len(task_list)}")
        return

    # 2. 检查是否有重复任务条目
    pages = [page for page, _ in task_list]
    duplicates = [p for p in set(pages) if pages.count(p) > 1]
    if duplicates:
        report.add(tasks_path.name, "AC7_Checklist", False, f"清单中存在重复条目: {duplicates}")
        return

    # 3. 检查任务是否都在 manifest.tsv 中
    unknown_pages = [p for p in pages if p not in manifest]
    if unknown_pages:
        report.add(tasks_path.name, "AC7_Checklist", False, f"清单中包含未在 manifest.tsv 中的未知页面: {unknown_pages}")
        return

    # 4. 检查头部统计数字与条目勾选状态的内部一致性
    actual_checked = sum(1 for _, checked in task_list if checked)
    actual_unchecked = sum(1 for _, checked in task_list if not checked)

    if done != actual_checked or rem != actual_unchecked or (done + rem != total):
        report.add(
            tasks_path.name,
            "AC7_Checklist",
            False,
            f"头部统计与清单勾选状态不同步: 头部显示剩余 {rem} 篇 / 进度 {done} / 总计 {total}，"
            f"实际清单勾选为已完成 {actual_checked} 篇 / 剩余 {actual_unchecked} 篇",
        )
        return

    # 5. 最终验收要求（要求 100% 勾选，剩余 0 篇）
    unchecked_tasks = [page for page, checked in task_list if not checked]
    if require_completed:
        if rem != 0 or done != 31 or unchecked_tasks:
            report.add(
                tasks_path.name,
                "AC7_Checklist",
                False,
                f"验收未完成: 剩余任务数应为 0 (实际为 {rem})，完成进度应为 31 / 31 (实际为 {done} / {total})，"
                f"未完成任务 ({len(unchecked_tasks)} 项): {', '.join(unchecked_tasks[:5])}{'...' if len(unchecked_tasks) > 5 else ''}",
            )
            return

        report.add(
            tasks_path.name,
            "AC7_Checklist",
            True,
            "任务清单状态完全同步且全部完成 (剩余 0 篇，进度 31 / 31，所有 31 项均已勾选 [x])",
        )
    else:
        report.add(
            tasks_path.name,
            "AC7_Checklist",
            True,
            f"任务清单格式正确且与条目勾选状态同步 (进度 {done} / {total}，剩余 {rem} 篇)",
        )


def normalize_page_id(raw_page: str) -> str:
    """规范化页面 ID（去除前缀 docs/、originals/ 及后缀 .md）"""
    page = raw_page.strip()
    if page.startswith("docs/"):
        page = page[len("docs/"):]
    elif page.startswith("originals/"):
        page = page[len("originals/"):]
    if page.endswith(".md"):
        page = page[:-len(".md")]
    return page


def print_console_report(report: Report, verbose: bool = False) -> None:
    """终端友好的格式化报告输出"""
    sep = "=" * 70
    print(sep)
    print("Rex Documentation Verification Report")
    print(sep)

    if verbose:
        for r in report.results:
            tag = "[PASS]" if r.passed else "[FAIL]"
            msg = f" - {r.message}" if r.message else ""
            print(f"{tag:<7} {r.page} :: {r.criterion}{msg}")
        print("-" * 70)

    print(f"Total Checks : {report.total_checks}")
    print(f"Passed Checks: {report.passed_checks}")
    print(f"Failed Checks: {report.failed_checks}")

    if not report.passed:
        print("\nFailure Details:")
        for r in report.results:
            if not r.passed:
                print(f"  • [FAIL] {r.page} ({r.criterion}): {r.message}")
        print(f"\n{sep}")
        print("VERIFICATION FAILED")
        print(sep)
    else:
        print(f"\n{sep}")
        print("ALL CHECKS PASSED")
        print(sep)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rex 官方文档中文翻译程序化自动化验证工具 (AC1 ~ AC7)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--page",
        type=str,
        help="验证单篇文档（AC1-AC6），例如: --page customize/config 或 --page docs/automate/cli.md",
    )
    parser.add_argument(
        "--checklist",
        action="store_true",
        help="仅验证 TRANSLATION-TASKS.md 状态与条目同步 (AC7)",
    )
    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help="允许清单未完成，仅验证清单格式与条目同步一致性 (供阶段性检查使用)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="执行全量验证：对清单中所有 31 篇文档执行 AC1-AC6，并对清单执行 AC7 (默认模式)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以机器可读 JSON 格式输出验证结果",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="输出每个独立检查项的详细执行结果",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = read_manifest(MANIFEST_FILE)
    report = Report()

    # 确定执行范围
    run_all = args.all or (not args.page and not args.checklist)

    if args.page:
        page_id = normalize_page_id(args.page)
        check_document(page_id, manifest, report)

    if args.checklist:
        check_ac7_checklist(manifest, report, require_completed=not args.allow_incomplete)

    if run_all:
        try:
            _, _, _, tasks = read_tasks(TASKS_FILE)
            tracked_pages = [page for page, _ in tasks]
        except Exception:
            tracked_pages = [p for p in manifest.keys() if p != "installation"]

        for page_id in tracked_pages:
            check_document(page_id, manifest, report)

        check_ac7_checklist(manifest, report, require_completed=not args.allow_incomplete)

    if args.json:
        print(json.dumps(report.summary(), ensure_ascii=False, indent=2))
    else:
        print_console_report(report, verbose=args.verbose)

    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
