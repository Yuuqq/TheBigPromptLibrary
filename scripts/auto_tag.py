#!/usr/bin/env python3
"""Auto-tag prompts with semantic labels (Q4.2).

Modes:
  --mode heuristic  (default in CI; fast, no API; ~50ms for 1849 files)
  --mode llm        (monthly; refines via GLM-4-Air; slow + costs tokens)

Inputs:
  - All English prompt files under TARGET_DIRS (same as build_index.py)
  - scripts/tag_vocabulary.json — controlled vocabulary

Outputs:
  - stats/tags.json — { "<path_en>": {"tags": [...], "source": "heuristic"|"llm", "ts": "..."} }

Subsequent build_index.py merges this into prompts_index.json's `tags` field.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]
VOCAB_FILE = Path("scripts/tag_vocabulary.json")
TAGS_FILE = Path("stats/tags.json")
MAX_TAGS = 10
MIN_TAGS_TARGET = 5

# ----- Heuristic tagger -----

def _flatten_vocab(vocab: dict) -> list[tuple[str, list[str]]]:
    """Return [(tag, [keyword, ...]), ...] from the nested vocabulary."""
    out: list[tuple[str, list[str]]] = []
    for group_key, group in vocab.items():
        if group_key.startswith("_"):
            continue
        if not isinstance(group, dict):
            continue
        for tag, keywords in group.items():
            if not isinstance(keywords, list):
                continue
            out.append((tag, [k.lower() for k in keywords if isinstance(k, str)]))
    return out


def heuristic_tag(text: str, path: str, vocab_flat: list[tuple[str, list[str]]]) -> list[str]:
    """Match text + path against the controlled vocabulary."""
    haystack = (text + " " + path).lower()
    matched: list[tuple[str, int]] = []
    for tag, keywords in vocab_flat:
        # tag can also be a keyword itself
        all_kw = keywords or [tag.replace("-", " ")]
        hits = sum(haystack.count(k) for k in all_kw)
        if hits > 0:
            matched.append((tag, hits))
    matched.sort(key=lambda x: -x[1])

    # Always derive provider from path (more reliable than text)
    parts = [p.lower() for p in path.split("/")]
    provider_hint = parts[1] if len(parts) > 1 else ""
    provider_map = {
        "openai": "openai", "anthropic": "anthropic", "google": "google",
        "meta.ai": "meta", "mistral": "mistral", "deepseek": "deepseek",
        "qwen": "qwen", "xai": "xai", "perplexity.ai": "perplexity",
        "copilot": "copilot", "cursor.com": "cursor", "v0.dev": "v0",
    }
    forced: list[str] = []
    if provider_hint in provider_map:
        forced.append(provider_map[provider_hint])

    section = parts[0] if parts else ""
    section_map = {
        "systemprompts": "system-prompt",
        "custominstructions": "custom-instruction",
        "jailbreak": "jailbreak",
        "security": "guardrails",
    }
    if section in section_map:
        forced.append(section_map[section])

    seen: set[str] = set()
    out: list[str] = []
    for t in forced:
        if t not in seen:
            seen.add(t); out.append(t)
    for tag, _ in matched:
        if tag in seen:
            continue
        seen.add(tag); out.append(tag)
        if len(out) >= MAX_TAGS:
            break
    return out


# ----- LLM tagger (GLM-4-Air via OpenAI-compatible endpoint) -----

LLM_SYSTEM_PROMPT = """You are a prompt-library tagger. Given a prompt's title and excerpt,
output 5-10 tags STRICTLY chosen from the provided vocabulary list. Never invent new tags.
Return ONLY a JSON array of strings, no prose. Example: ["openai","jailbreak","persona"]
"""


def llm_tag(text: str, title: str, allowed_tags: list[str]) -> list[str] | None:
    """Call GLM-4-Air. Return None on any failure (caller falls back to heuristic)."""
    api_key = os.environ.get("GLM_API_KEY")
    if not api_key:
        return None
    try:
        import requests  # type: ignore
    except ImportError:
        return None

    user_msg = (
        f"VOCABULARY (pick 5-10 of these): {', '.join(allowed_tags)}\n\n"
        f"TITLE: {title}\n\nEXCERPT:\n{text[:1500]}"
    )
    try:
        r = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": os.environ.get("GLM_MODEL", "glm-4-air"),
                "messages": [
                    {"role": "system", "content": LLM_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                "temperature": 0.2,
                "max_tokens": 200,
            },
            timeout=30,
        )
        if r.status_code != 200:
            return None
        content = r.json()["choices"][0]["message"]["content"].strip()
        m = re.search(r"\[.*?\]", content, re.S)
        if not m:
            return None
        tags = json.loads(m.group(0))
        if not isinstance(tags, list):
            return None
        # Validate against vocabulary
        allowed_set = set(allowed_tags)
        return [t for t in tags if isinstance(t, str) and t in allowed_set][:MAX_TAGS]
    except Exception:
        return None


# ----- Main -----

def iter_prompt_files() -> list[Path]:
    files: list[Path] = []
    for d in TARGET_DIRS:
        base = Path(d)
        if not base.exists():
            continue
        for f in base.rglob("*.md"):
            name = f.name.lower()
            if name.endswith("_zh.md") or name in ("readme.md", "license.md"):
                continue
            files.append(f)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic")
    parser.add_argument("--max-files", type=int, default=int(os.environ.get("MAX_TAG_FILES", "0")),
                        help="0=no limit. Use to cap LLM cost.")
    parser.add_argument("--only-missing", action="store_true",
                        help="Only tag files not already in tags.json")
    args = parser.parse_args()

    if not VOCAB_FILE.exists():
        print(f"ERROR: vocabulary file {VOCAB_FILE} not found", file=sys.stderr)
        return 1
    vocab = json.loads(VOCAB_FILE.read_text(encoding="utf-8"))
    vocab_flat = _flatten_vocab(vocab)
    allowed_tags = [t for t, _ in vocab_flat]

    existing: dict[str, dict] = {}
    if TAGS_FILE.exists():
        try:
            existing = json.loads(TAGS_FILE.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    files = iter_prompt_files()
    if args.only_missing:
        files = [f for f in files if str(f).replace("\\", "/") not in existing]
    if args.max_files > 0:
        files = files[:args.max_files]

    print(f"Auto-tagging {len(files)} files in {args.mode} mode (vocab={len(allowed_tags)} tags)")
    out: dict[str, dict] = dict(existing)
    now = datetime.now(timezone.utc).isoformat()
    llm_count = heur_count = fallback_count = 0

    for i, f in enumerate(files, 1):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Title from first heading or filename
        title = f.stem
        for line in text.splitlines()[:20]:
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip(); break

        path_str = str(f).replace("\\", "/")

        tags: list[str] = []
        source = "heuristic"
        if args.mode == "llm":
            llm_tags = llm_tag(text, title, allowed_tags)
            if llm_tags and len(llm_tags) >= 3:
                tags = llm_tags
                source = "llm"
                llm_count += 1
            else:
                tags = heuristic_tag(text, path_str, vocab_flat)
                fallback_count += 1
        else:
            tags = heuristic_tag(text, path_str, vocab_flat)
            heur_count += 1

        if not tags:
            continue
        out[path_str] = {"tags": tags, "source": source, "ts": now}

        if args.mode == "llm" and i % 50 == 0:
            print(f"  [{i}/{len(files)}] {llm_count} LLM, {fallback_count} fallback")

    TAGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TAGS_FILE.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. {len(out)} files tagged total.")
    print(f"  this run: heuristic={heur_count}, llm={llm_count}, llm-fallback={fallback_count}")
    print(f"  written to {TAGS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
