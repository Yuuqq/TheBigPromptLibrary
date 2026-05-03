#!/usr/bin/env python3
"""Build full-text search index for the site (Q4.1).

Extracts a 500-char body excerpt (markdown stripped) from each prompt and emits
a single JSON file the frontend can lazy-load on first search-box focus.

Output: stats/search_index.json
  [
    {"id": "...", "ex": "first 500 chars stripped of markdown ..."},
    ...
  ]

Total size for ~1849 files ≈ 1MB uncompressed, ~300KB gzipped.

Frontend strategy: lazy-load on input focus, cached by browser, search via
substring match — same fuzzy logic as performSearch() in index.html, just
extended to a new `body` field. Avoids needing lunr.js (~30KB lib + complex
tokenization) for an MVP that already lifts find-rate dramatically.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

INDEX = Path("prompts_index.json")
OUT = Path("stats/search_index.json")
EXCERPT_LEN = 500

CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```")
INLINE_CODE_RE = re.compile(r"`[^`]+`")
LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
HEADING_RE = re.compile(r"^#+\s+", re.M)
EMPHASIS_RE = re.compile(r"[*_]{1,3}([^*_]+)[*_]{1,3}")
HTML_TAG_RE = re.compile(r"<[^>]+>")
MULTI_WS_RE = re.compile(r"\s+")


def strip_markdown(text: str) -> str:
    text = IMAGE_RE.sub("", text)
    text = CODE_BLOCK_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = LINK_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub(" ", text)
    text = HEADING_RE.sub("", text)
    text = EMPHASIS_RE.sub(r"\1", text)
    text = MULTI_WS_RE.sub(" ", text)
    return text.strip()


def main() -> int:
    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found", file=sys.stderr)
        return 1

    entries = json.loads(INDEX.read_text(encoding="utf-8"))
    print(f"Building search index from {len(entries)} entries")

    out: list[dict] = []
    skipped = 0
    for e in entries:
        path_en = e.get("path_en")
        if not path_en:
            continue
        p = Path(path_en)
        if not p.exists():
            skipped += 1
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            skipped += 1
            continue
        excerpt = strip_markdown(content)[:EXCERPT_LEN]
        if not excerpt:
            continue
        out.append({"id": e.get("id") or e.get("path_en", "").rsplit(".md", 1)[0], "ex": excerpt})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(out, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    size_kb = OUT.stat().st_size / 1024
    print(f"  → {len(out)} excerpts ({skipped} skipped)")
    print(f"  → written to {OUT} ({size_kb:.0f}KB uncompressed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
