#!/usr/bin/env python3
"""Rebuild prompts_index.json by scanning the file system.

Output format matches what docs/index.html consumes:
  { id, title, category, path_en, path_zh, tags, summary, updatedAt,
    last_modified, last_modified_zh, qs }

Also writes:
  - stats/coverage.json (latest snapshot, simple to consume)
  - stats/coverage.jsonl (append-only history)
  - stats/quality.json  (qs distribution + worst-50 list)
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
TAGS_FILE = STATS_DIR / "tags.json"
DATE_RE = re.compile(r"(\d{8}|\d{4}-\d{2}-\d{2})")

# ----- Quality scoring -----
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")
CODE_FENCE_RE = re.compile(r"```")
HEADING_RE = re.compile(r"^#{1,6}\s", re.M)
LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")
SUSPICIOUS_TAIL_RE = re.compile(
    r"(<think>|</think>|here is the translation|translated as follows|"
    r"翻译如下|以下是翻译)",
    re.I,
)


def score_translation(en_text: str, zh_text: str) -> tuple[int, list[str]]:
    """Score 0..100 with issue tags. Heuristic-only, no LLM call."""
    score = 100
    issues: list[str] = []

    en_len = max(1, len(en_text))
    zh_len = len(zh_text)

    if zh_len < 20:
        return 0, ["empty_or_truncated"]

    ratio = zh_len / en_len
    if ratio < 0.18 or ratio > 1.8:
        score -= 30
        issues.append("length_anomaly")
    elif ratio < 0.28 or ratio > 1.35:
        score -= 12
        issues.append("length_warning")

    chinese_count = len(CHINESE_RE.findall(zh_text))
    chinese_ratio = chinese_count / zh_len
    if chinese_ratio < 0.12:
        score -= 40
        issues.append("mostly_english")
    elif chinese_ratio < 0.28:
        score -= 18
        issues.append("partial_translation")

    en_fences = len(CODE_FENCE_RE.findall(en_text))
    zh_fences = len(CODE_FENCE_RE.findall(zh_text))
    if abs(en_fences - zh_fences) > 1:
        score -= 15
        issues.append("code_block_mismatch")

    en_headings = len(HEADING_RE.findall(en_text))
    zh_headings = len(HEADING_RE.findall(zh_text))
    if en_headings > 3 and abs(en_headings - zh_headings) / en_headings > 0.3:
        score -= 12
        issues.append("heading_mismatch")

    en_links = len(LINK_RE.findall(en_text))
    zh_links = len(LINK_RE.findall(zh_text))
    if en_links > 3 and abs(en_links - zh_links) / en_links > 0.4:
        score -= 10
        issues.append("link_mismatch")

    if SUSPICIOUS_TAIL_RE.search(zh_text):
        score -= 25
        issues.append("translation_artifact")

    return max(0, score), issues


def extract_date(name: str) -> str:
    m = DATE_RE.search(name)
    if not m:
        return ""
    raw = m.group(1).replace("-", "")
    if len(raw) == 8 and raw.startswith("20"):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
    return ""


def _bulk_git_dates() -> dict[str, str]:
    """One git call → ISO date for every tracked file. Avoids per-file fork overhead."""
    cache: dict[str, str] = {}
    try:
        # %x00 NUL between fields, NUL after each commit. --name-only lists files per commit.
        # We only need the *latest* commit per file, so walk in chronological order overwriting.
        out = subprocess.check_output(
            ["git", "log", "--reverse", "--name-only", "--format=%x00%cs", "--diff-filter=AM"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8", errors="replace")
    except Exception:
        return cache
    current_date = ""
    for line in out.splitlines():
        if not line:
            continue
        if line.startswith("\x00"):
            current_date = line[1:].strip()
        else:
            cache[line] = current_date
    return cache


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


def write_quality(qs_map: dict[str, dict]) -> None:
    if not qs_map:
        return
    scores = [v["score"] for v in qs_map.values()]
    avg = round(sum(scores) / len(scores), 1)
    dist = {
        "excellent_90_plus": sum(1 for s in scores if s >= 90),
        "good_70_89":        sum(1 for s in scores if 70 <= s < 90),
        "poor_50_69":        sum(1 for s in scores if 50 <= s < 70),
        "bad_below_50":      sum(1 for s in scores if s < 50),
    }
    low = sorted(
        [{"path": p, **v} for p, v in qs_map.items() if v["score"] < 70],
        key=lambda x: x["score"],
    )[:50]
    snap = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_scored": len(qs_map),
        "average_score": avg,
        "distribution": dist,
        "worst_50": low,
        # Q3.4 / Q4.4 alias used by build_search_index + retranslate_worst
        "worst": low,
    }
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    (STATS_DIR / "quality.json").write_text(
        json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_tags() -> dict[str, list[str]]:
    """Load Q4.2 tags.json → {path_en: [tag, ...]}. Returns empty dict if missing."""
    if not TAGS_FILE.exists():
        return {}
    try:
        raw = json.loads(TAGS_FILE.read_text(encoding="utf-8"))
        return {p: (v.get("tags") or []) for p, v in raw.items() if isinstance(v, dict)}
    except Exception:
        return {}


def main() -> int:
    print("Indexing prompts...")
    git_dates = _bulk_git_dates()
    print(f"  loaded git dates for {len(git_dates)} tracked files")
    tags_map = load_tags()
    if tags_map:
        print(f"  loaded tags for {len(tags_map)} files (from {TAGS_FILE})")

    entries: list[dict] = []
    qs_map: dict[str, dict] = {}
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
            en_path_str = str(en_path).replace("\\", "/")
            zh_path_str = str(zh_path).replace("\\", "/") if has_zh else ""
            git_date_en = git_dates.get(en_path_str, "")
            git_date_zh = git_dates.get(zh_path_str, "") if has_zh else ""

            entry = {
                "id": id_,
                "title": derive_title(content_en, en_path.name),
                "category": category,
                "path_en": en_path_str,
                "path_zh": zh_path_str,
                "tags": tags_map.get(en_path_str, []),
                "summary": derive_summary(content_en),
                "updatedAt": file_date or git_date_en,
                # Q4.4: separate fields for "新/更新" badge logic in frontend
                "last_modified": git_date_en,
                "last_modified_zh": git_date_zh,
            }

            if has_zh:
                try:
                    content_zh = zh_path.read_text(encoding="utf-8", errors="replace")
                    score, issues = score_translation(content_en, content_zh)
                    entry["qs"] = score
                    qs_map[entry["path_zh"]] = {"score": score, "issues": issues}
                except Exception:
                    pass

            entries.append(entry)

    OUTPUT.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_coverage(entries)
    write_quality(qs_map)

    zh_count = sum(1 for e in entries if e["path_zh"])
    pct = (zh_count / len(entries) * 100) if entries else 0
    avg_qs = (sum(v["score"] for v in qs_map.values()) / len(qs_map)) if qs_map else 0
    tagged_count = sum(1 for e in entries if e["tags"])
    print(
        f"Wrote {len(entries)} entries to {OUTPUT}; "
        f"{zh_count} have Chinese ({pct:.1f}% coverage); "
        f"avg translation quality: {avg_qs:.1f}/100 over {len(qs_map)} pairs; "
        f"{tagged_count} entries tagged; "
        f"snapshots saved to {STATS_DIR}/coverage.json + quality.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
