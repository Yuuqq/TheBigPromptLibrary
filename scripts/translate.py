#!/usr/bin/env python3
"""Translate .md files in target dirs to Chinese (_zh.md) using Zhipu GLM API.

- Skips files whose _zh.md is newer than source.
- Skips files larger than MAX_FILE_CHARS (cost control).
- Caps per-run translations at MAX_FILES_PER_RUN (cost control).
- Strips <think>...</think> blocks (GLM-Z1 reasoning output).
- Writes per-run stats to stats/translation-runs.jsonl.
"""
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import requests

GLM_API_KEY = os.environ.get("GLM_API_KEY")
if not GLM_API_KEY:
    print("ERROR: GLM_API_KEY not set", file=sys.stderr)
    sys.exit(1)

MODEL = os.environ.get("GLM_MODEL", "glm-z1-flash")
API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]

MAX_FILES_PER_RUN = int(os.environ.get("MAX_FILES_PER_RUN", "40"))
MAX_FILE_CHARS = int(os.environ.get("MAX_FILE_CHARS", "30000"))
MAX_RETRIES = 3
REQUEST_TIMEOUT = 300
SLEEP_BETWEEN = 1.0

STATS_DIR = Path("stats")
STATS_LOG = STATS_DIR / "translation-runs.jsonl"
ERROR_LOG = STATS_DIR / "translation-errors.log"

SYSTEM_PROMPT = """你是专业的中英文翻译专家。请把英文 Markdown 翻译成简体中文。

严格要求：
1. 保留所有 Markdown 格式（标题、列表、链接、粗体、斜体等）原样
2. 代码块（``` 包围的内容）原样不动，不要翻译代码
3. 行内代码（` 包围的内容）原样不动
4. 保留变量名、函数名、文件路径、URL、英文专有名词
5. 翻译符合中文表达习惯，技术术语使用业界通用译法
6. 提示词（system prompt）的指令性内容要准确翻译，保持原意
7. 直接输出翻译结果，不要任何解释、前后缀或思考过程"""


def call_glm(content: str) -> tuple[str, dict]:
    """Returns (translated_text, usage_dict)."""
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {GLM_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": content},
                    ],
                    "temperature": 0.3,
                },
                timeout=REQUEST_TIMEOUT,
            )
            if resp.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"  rate-limited, waiting {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            text = re.sub(r"<think>[\s\S]*?</think>", "", text).strip()
            text = re.sub(r"^```(?:markdown|md)?\n([\s\S]*?)\n```$", r"\1", text).strip()
            usage = data.get("usage", {}) or {}
            return text, usage
        except Exception as e:
            last_err = e
            print(f"  attempt {attempt + 1} failed: {e}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"All {MAX_RETRIES} retries failed: {last_err}")


def needs_translation(en_path: Path) -> bool:
    zh_path = en_path.with_name(en_path.name.replace(".md", "_zh.md"))
    if not zh_path.exists():
        return True
    return en_path.stat().st_mtime > zh_path.stat().st_mtime


def is_translatable_size(en_path: Path) -> tuple[bool, int]:
    """Return (is_translatable, char_count). Files outside [10, MAX_FILE_CHARS] are not."""
    try:
        size = len(en_path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return False, 0
    return (10 <= size <= MAX_FILE_CHARS), size


def log_error(file_path: Path, err: Exception) -> None:
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with ERROR_LOG.open("a", encoding="utf-8") as fp:
        fp.write(f"\n--- {datetime.now(timezone.utc).isoformat()} {file_path} ---\n")
        fp.write("".join(traceback.format_exception(type(err), err, err.__traceback__)))


def write_stats(stats: dict) -> None:
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with STATS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(stats, ensure_ascii=False) + "\n")


def main() -> int:
    candidates: list[Path] = []
    oversized: list[tuple[Path, int]] = []
    for d in TARGET_DIRS:
        base = Path(d)
        if not base.exists():
            continue
        for en in sorted(base.rglob("*.md")):
            name_low = en.name.lower()
            if en.name.endswith("_zh.md"):
                continue
            if name_low in ("readme.md", "license.md"):
                continue
            if not needs_translation(en):
                continue
            ok, size = is_translatable_size(en)
            if not ok:
                if size > MAX_FILE_CHARS:
                    oversized.append((en, size))
                continue
            candidates.append(en)

    print(
        f"Found {len(candidates)} translatable files needing translation; "
        f"{len(oversized)} oversized (>{MAX_FILE_CHARS} chars) deferred"
    )

    stats = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "candidates": len(candidates),
        "oversized_deferred": len(oversized),
        "translated": 0,
        "failed": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "duration_seconds": 0,
    }

    if not candidates:
        # Persist the oversized list so it's visible without re-scanning the tree
        if oversized:
            STATS_DIR.mkdir(parents=True, exist_ok=True)
            (STATS_DIR / "oversized.txt").write_text(
                "\n".join(f"{p}\t{s}" for p, s in oversized) + "\n", encoding="utf-8"
            )
        write_stats(stats)
        return 0

    batch = candidates[:MAX_FILES_PER_RUN]
    print(f"Will translate first {len(batch)} this run (cap={MAX_FILES_PER_RUN})")
    started_at = time.time()

    for i, en in enumerate(batch, 1):
        content = en.read_text(encoding="utf-8", errors="replace")
        size = len(content)

        print(f"[{i}/{len(batch)}] {en} ({size} chars)")
        try:
            translated, usage = call_glm(content)
            if not translated or len(translated) < 10:
                print("  empty translation, skipping")
                stats["failed"] += 1
                continue
            zh_path = en.with_name(en.name.replace(".md", "_zh.md"))
            zh_path.write_text(translated, encoding="utf-8")
            stats["translated"] += 1
            stats["tokens_in"] += int(usage.get("prompt_tokens", 0))
            stats["tokens_out"] += int(usage.get("completion_tokens", 0))
            time.sleep(SLEEP_BETWEEN)
        except Exception as e:
            print(f"  FAILED: {e}")
            stats["failed"] += 1
            log_error(en, e)

    stats["duration_seconds"] = round(time.time() - started_at, 1)
    stats["pending_after_run"] = max(0, len(candidates) - len(batch))

    if oversized:
        STATS_DIR.mkdir(parents=True, exist_ok=True)
        (STATS_DIR / "oversized.txt").write_text(
            "\n".join(f"{p}\t{s}" for p, s in oversized) + "\n", encoding="utf-8"
        )

    write_stats(stats)

    print(
        f"\nDone: {stats['translated']} translated, {stats['failed']} failed, "
        f"{stats['pending_after_run']} pending; "
        f"tokens in/out: {stats['tokens_in']}/{stats['tokens_out']}; "
        f"{stats['duration_seconds']}s"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
