#!/usr/bin/env python3
"""Rebuild prompts_index.json by scanning the file system.

Output format matches what docs/index.html consumes:
  { id, title, category, path_en, path_zh, tags, summary, updatedAt }

Also writes:
  - stats/coverage.json (latest snapshot, simple to consume)
  - stats/coverage.jsonl (append-only history)
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]
OUTPUT = Path("prompts_index.json")
STATS_DIR = Path("stats")
DATE_RE = re.compile(r"(\d{8}|\d{4}-\d{2}-\d{2})")


def extract_date(name: str) -> str:
    m = DATE_RE.search(name)
    if not m:
        return ""
    raw = m.group(1).replace("-", "")
    if len(raw) == 8 and raw.startswith("20"):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return ""


def git_last_modified(path: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        return out
    except Exception:
        return ""


def derive_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
        if line.startswith("## "):
            return line[3:].strip()
    return fallback.replace(".md", "").replace("_", " ")


def derive_summary(content: str, max_len: int = 160) -> str:
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("```") or line.startswith("---"):
            continue
        if line.startswith(("|", "- ", "* ", ">")):
            continue
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        text = re.sub(r"[*_`]", "", text)
        if len(text) > max_len:
            text = text[: max_len - 1] + "…"
        return text
    return ""


def write_coverage(entries: list[dict]) -> None:
    total = len(entries)
    with_zh = sum(1 for e in entries if e.get("path_zh"))
    by_cat: dict[str, dict] = {}
    for e in entries:
        top = e["category"].split("/")[0] if e.get("category") else "_root"
        bucket = by_cat.setdefault(top, {"total": 0, "with_zh": 0})
        bucket["total"] += 1
        if e.get("path_zh"):
            bucket["with_zh"] += 1

    snap = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": total,
        "with_zh": with_zh,
        "coverage_pct": round(with_zh / total * 100, 1) if total else 0.0,
        "by_category": by_cat,
    }

    STATS_DIR.mkdir(parents=True, exist_ok=True)
    (STATS_DIR / "coverage.json").write_text(
        json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (STATS_DIR / "coverage.jsonl").open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(snap, ensure_ascii=False) + "\n")


def main() -> int:
    entries: list[dict] = []
    for d in TARGET_DIRS:
        base = Path(d)
        if not base.exists():
            continue
        for en_path in sorted(base.rglob("*.md")):
            name_low = en_path.name.lower()
            if en_path.name.endswith("_zh.md"):
                continue
            if name_low in ("readme.md", "license.md"):
                continue

            zh_path = en_path.with_name(en_path.name.replace(".md", "_zh.md"))
            has_zh = zh_path.exists()

            try:
                content_en = en_path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            id_ = str(en_path.with_suffix("")).replace("\\", "/")
            category = "/".join(en_path.parts[:-1])
            file_date = extract_date(en_path.name)
            git_date = git_last_modified(en_path)

            entries.append({
                "id": id_,
                "title": derive_title(content_en, en_path.name),
                "category": category,
                "path_en": str(en_path).replace("\\", "/"),
                "path_zh": str(zh_path).replace("\\", "/") if has_zh else "",
                "tags": [],
                "summary": derive_summary(content_en),
                "updatedAt": file_date or git_date,
            })

    OUTPUT.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_coverage(entries)

    zh_count = sum(1 for e in entries if e["path_zh"])
    pct = (zh_count / len(entries) * 100) if entries else 0
    print(
        f"Wrote {len(entries)} entries to {OUTPUT}; "
        f"{zh_count} have Chinese ({pct:.1f}% coverage); "
        f"snapshot saved to {STATS_DIR}/coverage.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
