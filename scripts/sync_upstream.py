#!/usr/bin/env python3
"""Sync new/changed .md files from upstream repo (0xeb/TheBigPromptLibrary).

Strategy: pull-only overlay. We never overwrite our own files
(_zh.md translations, docs/index.html, .github/, scripts/, prompts_index.json),
only copy new or changed source .md from upstream.
"""
import os
import sys
import time
from pathlib import Path

import requests

UPSTREAM = os.environ.get("UPSTREAM_REPO", "0xeb/TheBigPromptLibrary")
TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]
REPO_API = f"https://api.github.com/repos/{UPSTREAM}"
RAW_BASE = f"https://raw.githubusercontent.com/{UPSTREAM}/main"

session = requests.Session()
gh_token = os.environ.get("GITHUB_TOKEN")
if gh_token:
    session.headers["Authorization"] = f"Bearer {gh_token}"
session.headers["Accept"] = "application/vnd.github.v3+json"


def fetch_tree() -> list:
    r = session.get(f"{REPO_API}/branches/main", timeout=60)
    r.raise_for_status()
    sha = r.json()["commit"]["sha"]
    r = session.get(f"{REPO_API}/git/trees/{sha}?recursive=1", timeout=60)
    r.raise_for_status()
    data = r.json()
    if data.get("truncated"):
        print("WARNING: upstream tree truncated; some files may be missed", file=sys.stderr)
    return data["tree"]


def fetch_file(path: str) -> bytes:
    for attempt in range(3):
        try:
            r = requests.get(f"{RAW_BASE}/{path}", timeout=60)
            r.raise_for_status()
            return r.content
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def main() -> int:
    tree = fetch_tree()
    new_count = 0
    update_count = 0
    skipped = 0

    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item["path"]
        if not path.endswith(".md"):
            continue
        if path.endswith("_zh.md"):
            continue
        if path.lower().endswith("/readme.md") or path.lower() == "readme.md":
            continue
        if not any(path.startswith(d + "/") for d in TARGET_DIRS):
            continue

        local = Path(path)
        try:
            new_content = fetch_file(path)
        except Exception as e:
            print(f"  fetch failed {path}: {e}", file=sys.stderr)
            continue

        if local.exists():
            if local.read_bytes() == new_content:
                skipped += 1
                continue
            local.write_bytes(new_content)
            update_count += 1
            print(f"  updated: {path}")
        else:
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(new_content)
            new_count += 1
            print(f"  new:     {path}")

    print(f"\nSummary: {new_count} new, {update_count} updated, {skipped} unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
