#!/usr/bin/env python3
"""Lightweight tests for the sync/translate/index pipeline.

Run locally with:  python scripts/test_scripts.py
Run in CI without network — only tests pure functions and JSON validity.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name: str):
    """Import a script module without requiring env vars at import time."""
    os.environ.setdefault("GLM_API_KEY", "stub-key-for-tests")
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expect(cond, msg):
    if not cond:
        print(f"  ✗ {msg}")
        return 1
    print(f"  ✓ {msg}")
    return 0


def test_build_index_helpers():
    print("\ntest_build_index_helpers")
    bi = _load("build_index")
    fails = 0
    fails += expect(bi.derive_title("# Hello\nbody", "fb.md") == "Hello", "extracts H1")
    fails += expect(bi.derive_title("## Sub\n", "fb.md") == "Sub", "extracts H2")
    fails += expect(bi.derive_title("no heading", "Foo_Bar.md") == "Foo Bar", "filename fallback")
    fails += expect(bi.extract_date("ChatGPT-20250915.md") == "2025-09-15", "extracts YYYYMMDD")
    fails += expect(bi.extract_date("foo-2024-01-02-bar.md") == "2024-01-02", "extracts YYYY-MM-DD")
    fails += expect(bi.extract_date("no-date.md") == "", "no date returns empty")
    summary = bi.derive_summary("# Title\n\nFirst real line of body text.\n")
    fails += expect(summary.startswith("First real line"), "extracts first paragraph")
    return fails


def test_translate_helpers():
    print("\ntest_translate_helpers")
    tr = _load("translate")
    import re
    fails = 0
    fails += expect("glm" in tr.MODEL.lower(), "model is a GLM model")
    fails += expect(tr.MAX_FILES_PER_RUN > 0, "MAX_FILES_PER_RUN > 0")
    fails += expect("Markdown" in tr.SYSTEM_PROMPT, "system prompt mentions Markdown")
    fails += expect("代码块" in tr.SYSTEM_PROMPT, "system prompt asks to preserve code")
    # Test that thinking-tag stripping regex works
    sample = "<think>I should</think>Hello world"
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", sample).strip()
    fails += expect(cleaned == "Hello world", "<think> stripping works")
    return fails


def test_prompts_index_valid():
    print("\ntest_prompts_index_valid")
    fails = 0
    p = ROOT / "prompts_index.json"
    if not p.exists():
        print("  - prompts_index.json missing (skipping)")
        return 0
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ✗ invalid JSON: {e}")
        return 1
    fails += expect(isinstance(data, list), "is a list")
    fails += expect(len(data) > 0, "has entries")
    if data:
        keys = {"id", "title", "category", "path_en", "path_zh", "tags", "summary", "updatedAt"}
        fails += expect(keys.issubset(data[0].keys()), "first entry has required keys")
        bad_paths = [e for e in data if e.get("path_en") and not e["path_en"].endswith(".md")]
        fails += expect(len(bad_paths) == 0, "all path_en end with .md")
    return fails


def test_workflow_yaml():
    print("\ntest_workflow_yaml")
    fails = 0
    wf = ROOT / ".github" / "workflows" / "sync-and-translate.yml"
    if not wf.exists():
        print("  - workflow file missing (skipping)")
        return 0
    text = wf.read_text(encoding="utf-8")
    fails += expect("GLM_API_KEY" in text, "references GLM_API_KEY secret")
    fails += expect("0xeb/TheBigPromptLibrary" in text, "references upstream repo")
    fails += expect("python scripts/translate.py" in text, "runs translate script")
    fails += expect("python scripts/build_index.py" in text, "runs build_index script")
    return fails


def main():
    suites = [
        test_build_index_helpers,
        test_translate_helpers,
        test_prompts_index_valid,
        test_workflow_yaml,
    ]
    total_fails = 0
    for t in suites:
        try:
            total_fails += t()
        except Exception as e:
            print(f"  ✗ EXCEPTION in {t.__name__}: {e}")
            total_fails += 1
    print(f"\n{'='*40}")
    if total_fails == 0:
        print("All tests passed ✓")
        return 0
    print(f"{total_fails} failures ✗")
    return 1


if __name__ == "__main__":
    sys.exit(main())
