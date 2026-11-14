#!/usr/bin/env python3
"""Comprehensive test suite for tools/verify.py.

Tests all Acceptance Criteria (AC1-AC7), CLI options, edge cases,
and error handling using standard library unittest.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

# 导入待测 verify 模块
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import verify


class TestVerifyHelpers(unittest.TestCase):
    """测试解析与辅助函数"""

    def test_normalize_page_id(self):
        self.assertEqual(verify.normalize_page_id("customize/config"), "customize/config")
        self.assertEqual(verify.normalize_page_id("docs/customize/config.md"), "customize/config")
        self.assertEqual(verify.normalize_page_id("originals/customize/config.md"), "customize/config")
        self.assertEqual(verify.normalize_page_id("customize/config.md"), "customize/config")
        self.assertEqual(verify.normalize_page_id("  automate/cli.md  "), "automate/cli")

    def test_strip_code_blocks(self):
        text = "Hello\n```python\nprint(1)\n```\nWorld\n```sh\necho hi\n```\nEnd"
        clean, langs = verify.strip_code_blocks(text)
        self.assertNotIn("print(1)", clean)
        self.assertNotIn("echo hi", clean)
        self.assertIn("Hello", clean)
        self.assertIn("World", clean)
        self.assertIn("End", clean)
        self.assertEqual(langs, ["python", "sh"])

    def test_strip_code_blocks_indented(self):
        text = "List:\n 1. Item\n   ```sh\n   echo indented\n   ```\nEnd"
        clean, langs = verify.strip_code_blocks(text)
        self.assertNotIn("echo indented", clean)
        self.assertEqual(langs, ["sh"])

    def test_extract_headings(self):
        text = "---\ntitle: test\n---\n> 原文：...\n> 原文版本：...\n\n# Main Title\n\n## Sub 1\n\n### Sub Sub\n\n## Sub 2\n"
        clean, _ = verify.strip_code_blocks(text)
        headings = verify.extract_headings(clean)
        self.assertEqual(headings, [(1, "Main Title"), (2, "Sub 1"), (3, "Sub Sub"), (2, "Sub 2")])

    def test_count_tables(self):
        table_text = "| Col1 | Col2 |\n| --- | --- |\n| Val1 | Val2 |\n\n| A | B |\n|:--|--:|\n| 1 | 2 |\n"
        self.assertEqual(verify.count_tables(table_text), 2)


class TestAC1Existence(unittest.TestCase):
    """测试 AC1 文件存在性与非空校验"""

    def test_existing_non_empty(self):
        report = verify.Report()
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
            tf.write("content")
            tf_path = Path(tf.name)
        try:
            passed = verify.check_ac1_existence("test", tf_path, report)
            self.assertTrue(passed)
            self.assertTrue(report.passed)
        finally:
            tf_path.unlink()

    def test_missing_file(self):
        report = verify.Report()
        non_existent = Path("/non/existent/path.md")
        passed = verify.check_ac1_existence("test", non_existent, report)
        self.assertFalse(passed)
        self.assertFalse(report.passed)
        self.assertIn("不存在", report.results[0].message)

    def test_empty_file(self):
        report = verify.Report()
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
            tf_path = Path(tf.name)
        try:
            passed = verify.check_ac1_existence("test", tf_path, report)
            self.assertFalse(passed)
            self.assertFalse(report.passed)
            self.assertIn("为空", report.results[0].message)
        finally:
            tf_path.unlink()


class TestAC4Metadata(unittest.TestCase):
    """测试 AC4 文件头元数据检查"""

    def setUp(self):
        self.manifest = {"page/test": ("abc123def456", "2026-11-13")}

    def test_valid_header(self):
        report = verify.Report()
        lines = [
            "> 原文：https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：abc123def456（抓取于 2026-11-13）",
            "",
            "# 标题",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertTrue(report.passed)

    def test_reject_frontmatter(self):
        report = verify.Report()
        lines = [
            "---",
            "title: Foo",
            "---",
            "> 原文：https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：abc123def456（抓取于 2026-11-13）",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertFalse(report.passed)
        self.assertIn("frontmatter", report.results[0].message)

    def test_reject_frontmatter_post_header(self):
        report = verify.Report()
        lines = [
            "> 原文：https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：abc123def456（抓取于 2026-11-13）",
            "",
            "---",
            "title: Leaked Frontmatter",
            "---",
            "# 标题",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertFalse(report.passed)
        self.assertIn("frontmatter", report.results[0].message)

    def test_reject_half_width_colon(self):
        report = verify.Report()
        lines = [
            "> 原文: https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：abc123def456（抓取于 2026-11-13）",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertFalse(report.passed)
        self.assertIn("半角冒号", report.results[0].message)

    def test_reject_half_width_parentheses(self):
        report = verify.Report()
        lines = [
            "> 原文：https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：abc123def456(抓取于 2026-11-13)",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertFalse(report.passed)
        self.assertIn("半角括号", report.results[0].message)

    def test_reject_mismatched_sha(self):
        report = verify.Report()
        lines = [
            "> 原文：https://www.superlogical.com/rex/docs/page/test",
            "> 原文版本：wrong1234567（抓取于 2026-11-13）",
        ]
        verify.check_ac4_metadata("page/test", lines, self.manifest, report)
        self.assertFalse(report.passed)
        self.assertIn("不匹配", report.results[0].message)


class TestAC2Structure(unittest.TestCase):
    """测试 AC2 结构对齐检查"""

    def test_matching_structure(self):
        report = verify.Report()
        orig = "# Title\n\n## Section 1\n\n```sh\necho 1\n```\n\n| A | B |\n| - | - |\n| 1 | 2 |\n"
        doc = "# 标题\n\n## 第一节\n\n```sh\necho 1\n```\n\n| 甲 | 乙 |\n| - | - |\n| 1 | 2 |\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertTrue(report.passed)

    def test_matching_structure_with_indented_code_blocks(self):
        report = verify.Report()
        orig = "# Title\n\n1. Item\n   ```sh\n   echo 1\n   ```\n"
        doc = "# 标题\n\n1. 条目\n   ```sh\n   echo 1\n   ```\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertTrue(report.passed)

    def test_unclosed_code_block(self):
        report = verify.Report()
        orig = "# Title\n\n```sh\necho 1\n```\n"
        doc = "# 标题\n\n```sh\necho 1\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("未闭合", report.results[0].message)

    def test_mismatched_code_blocks_count(self):
        report = verify.Report()
        orig = "# Title\n\n```sh\necho 1\n```\n\n```sh\necho 2\n```\n"
        doc = "# 标题\n\n```sh\necho 1\n```\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("代码块数量不匹配", report.results[0].message)

    def test_mismatched_headings(self):
        report = verify.Report()
        orig = "# Title\n\n## Sub 1\n\n### Sub 2\n"
        doc = "# 标题\n\n## 第一节\n\n## 第二节\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("标题层级序列不匹配", report.results[0].message)

    def test_multiple_h1_headings(self):
        report = verify.Report()
        orig = "# Title\n\n## Sub 1\n"
        doc = "# 标题\n\n# 另一个大标题\n"
        verify.check_ac2_structure("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("多个 H1 标题", report.results[0].message)


class TestAC3Completeness(unittest.TestCase):
    """测试 AC3 翻译完整性检查"""

    def test_valid_chinese_prose(self):
        report = verify.Report()
        doc = "# 标题\n\n这是包含中文描述的正文段落，介绍了 Rex 的各种配置项。\n\n另一段也是中文。"
        verify.check_ac3_completeness("test", doc, report)
        self.assertTrue(report.passed)

    def test_untranslated_english_paragraph(self):
        report = verify.Report()
        doc = (
            "# 标题\n\n"
            "This is an untranslated English paragraph that explains the details of the service in full.\n\n"
            "这是中文。"
        )
        verify.check_ac3_completeness("test", doc, report)
        self.assertFalse(report.passed)
        self.assertIn("未翻译", report.results[0].message)

    def test_untranslated_heading(self):
        report = verify.Report()
        doc = "# 标题\n\n## This is the section for configuration\n\n这是配置的正文。"
        verify.check_ac3_completeness("test", doc, report)
        self.assertFalse(report.passed)
        self.assertIn("未翻译标题", report.results[0].message)

    def test_untranslated_heading_concise(self):
        report = verify.Report()
        doc = "# 标题\n\n## Overview\n\n这是中文正文。"
        verify.check_ac3_completeness("test", doc, report)
        self.assertFalse(report.passed)
        self.assertIn("未翻译标题", report.results[0].message)

    def test_allowed_proper_noun_heading(self):
        report = verify.Report()
        doc = "# CLI\n\n## PATH\n\n### Nix\n\n这是中文正文。"
        verify.check_ac3_completeness("test", doc, report)
        self.assertTrue(report.passed)

    def test_blockquote_translation(self):
        # 正常翻译的引用块应通过
        report = verify.Report()
        doc = "# 标题\n\n> 这是一个中文提示引用块。\n\n正文内容。"
        verify.check_ac3_completeness("test", doc, report)
        self.assertTrue(report.passed)

        # 未翻译的英文引用块应被拦截
        report_fail = verify.Report()
        doc_fail = "# 标题\n\n> Warning: This note is completely untranslated in English and explains configuration details.\n\n正文内容。"
        verify.check_ac3_completeness("test", doc_fail, report_fail)
        self.assertFalse(report_fail.passed)
        self.assertIn("未翻译", report_fail.results[0].message)


class TestAC5Cleanup(unittest.TestCase):
    """测试 AC5 模板残留与 <kbd> 标签保留"""

    def test_clean_template(self):
        report = verify.Report()
        orig = "# Title\n\nPress <kbd>Ctrl</kbd>+<kbd>C</kbd>."
        doc = "# 标题\n\n按下 <kbd>Ctrl</kbd>+<kbd>C</kbd>。"
        verify.check_ac5_cleanup("test", orig, doc, report)
        self.assertTrue(report.passed)

    def test_svelte_directive_residual(self):
        report = verify.Report()
        orig = "# Title\n\n{#if download}\nZip\n{/if}"
        doc = "# 标题\n\n{#if download}\n下载\n{/if}"
        verify.check_ac5_cleanup("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("Svelte", report.results[0].message)

    def test_component_residual(self):
        report = verify.Report()
        orig = "# Title\n\n<OsIcon name='mac' />"
        doc = "# 标题\n\n<OsIcon name='mac' />"
        verify.check_ac5_cleanup("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("导出组件标签", report.results[0].message)

    def test_html_heading_residual(self):
        report = verify.Report()
        orig = "# Title\n\n<h2 id='foo'>Foo</h2>"
        doc = "# 标题\n\n<h2 id='foo'>Foo</h2>"
        verify.check_ac5_cleanup("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("HTML 标题标签", report.results[0].message)

    def test_kbd_count_mismatch(self):
        report = verify.Report()
        orig = "# Title\n\nPress <kbd>Ctrl</kbd>+<kbd>C</kbd>."
        doc = "# 标题\n\n按下 Ctrl+C。"
        verify.check_ac5_cleanup("test", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("<kbd> 标签数量不一致", report.results[0].message)

    def test_windows_installation_fallback_missing(self):
        report = verify.Report()
        orig = "# Installing on Windows\n\n{#if download}\nZip\n{/if}"
        doc = "# 在 Windows 上安装\n\n没有后备文本的内容。"
        verify.check_ac5_cleanup("windows/installation", orig, doc, report)
        self.assertFalse(report.passed)
        self.assertIn("缺少必需的静态后备文本", report.results[0].message)

    def test_windows_installation_fallback_present(self):
        report = verify.Report()
        orig = "# Installing on Windows\n\n{#if download}\nZip\n{/if}"
        doc = "# 在 Windows 上安装\n\n拥有 Windows 角色的测试者可在此处获取下载。"
        verify.check_ac5_cleanup("windows/installation", orig, doc, report)
        self.assertTrue(report.passed)


class TestAC6Links(unittest.TestCase):
    """测试 AC6 内部相对链接检查"""

    def test_valid_relative_link(self):
        with tempfile.TemporaryDirectory() as td:
            base_dir = Path(td)
            target = base_dir / "target.md"
            target.write_text("# Target\n", encoding="utf-8")
            source = base_dir / "source.md"
            source.write_text("# Source\n\n[目标](target.md)\n", encoding="utf-8")

            report = verify.Report()
            verify.check_ac6_links("test", source, source.read_text(), report)
            self.assertTrue(report.passed)

    def test_broken_relative_link(self):
        with tempfile.TemporaryDirectory() as td:
            base_dir = Path(td)
            source = base_dir / "source.md"
            source.write_text("# Source\n\n[目标](non_existent.md)\n", encoding="utf-8")

            report = verify.Report()
            verify.check_ac6_links("test", source, source.read_text(), report)
            self.assertFalse(report.passed)
            self.assertIn("破坏", report.results[0].message)

    def test_official_link_to_existing_page_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base_dir = Path(td)
            # 模拟在 docs 目录下已有 customize/config.md
            docs_dir = base_dir / "docs" / "customize"
            docs_dir.mkdir(parents=True)
            config_md = docs_dir / "config.md"
            config_md.write_text("# Config\n", encoding="utf-8")
            source = docs_dir / "actions.md"
            source.write_text("# Actions\n\n[配置](https://www.superlogical.com/rex/docs/customize/config)\n", encoding="utf-8")

            report = verify.Report()
            old_docs = verify.DOCS_DIR
            verify.DOCS_DIR = base_dir / "docs"
            try:
                verify.check_ac6_links("customize/actions", source, source.read_text(), report)
                self.assertFalse(report.passed)
                self.assertIn("应转换为相对路径", report.results[0].message)
            finally:
                verify.DOCS_DIR = old_docs

    def test_official_link_to_untranslated_page_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            base_dir = Path(td)
            source = base_dir / "source.md"
            # 目标 future/untranslated 尚未翻译，保留官方链接应通过
            source.write_text("# Source\n\n[CLI](https://www.superlogical.com/rex/docs/future/untranslated)\n", encoding="utf-8")

            report = verify.Report()
            verify.check_ac6_links("test", source, source.read_text(), report)
            self.assertTrue(report.passed)

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base_dir = Path(td)
            source = base_dir / "source.md"
            source.write_text("# Source\n\n[越界](../../../../../../etc/passwd)\n", encoding="utf-8")

            report = verify.Report()
            verify.check_ac6_links("test", source, source.read_text(), report)
            self.assertFalse(report.passed)
            self.assertIn("越界", report.results[0].message)


class TestAC7Checklist(unittest.TestCase):
    """测试 AC7 任务清单检查"""

    def test_checklist_strict_on_current_state(self):
        manifest = verify.read_manifest()
        report = verify.Report()
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tf:
            tf.write("# Rex 文档中文翻译任务清单\n\n剩余 1 篇，进度 30 / 31\n\n")
            for page in list(manifest.keys())[:31]:
                if page == "reference/cli":
                    tf.write(f"- [ ] `{page}`\n")
                else:
                    tf.write(f"- [x] `{page}`\n")
            tf_path = Path(tf.name)
        try:
            verify.check_ac7_checklist(manifest, report, require_completed=True, tasks_path=tf_path)
            self.assertFalse(report.passed)
            self.assertIn("验收未完成", report.results[0].message)
        finally:
            tf_path.unlink()

    def test_checklist_allow_incomplete_on_current_state(self):
        manifest = verify.read_manifest()
        report = verify.Report()
        verify.check_ac7_checklist(manifest, report, require_completed=False)
        # allow_incomplete 模式下，当前清单头部计数与勾选状态完全同步，应判定为通过
        self.assertTrue(report.passed)


class TestCLIExecution(unittest.TestCase):
    """测试 tools/verify.py CLI 接口与不同调用方式"""

    def test_single_page_cli_success(self):
        cmd = [sys.executable, "tools/verify.py", "--page", "customize/config", "--json"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data["all_passed"])
        self.assertEqual(data["total_checks"], 6)

    def test_single_page_cli_failure(self):
        cmd = [sys.executable, "tools/verify.py", "--page", "nonexistent/page", "--json"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)
        data = json.loads(res.stdout)
        self.assertFalse(data["all_passed"])
        self.assertGreaterEqual(data["failed_checks"], 1)

    def test_checklist_cli_allow_incomplete(self):
        cmd = [sys.executable, "tools/verify.py", "--checklist", "--allow-incomplete"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

    def test_all_pages_cli_on_current_repo(self):
        cmd = [sys.executable, "tools/verify.py", "--all", "--json"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data["all_passed"])
        self.assertEqual(data["total_checks"], data["passed_checks"] + data["failed_checks"])
        self.assertEqual(data["total_checks"], 31 * 6 + 1)
        self.assertGreater(data["passed_checks"], 0)
        self.assertEqual(data["failed_checks"], 0)


if __name__ == "__main__":
    unittest.main()
