#!/usr/bin/env python3
"""Queue the worst-quality translations for re-translation by deleting their _zh.md files.

Inputs (read from `stats/`):
  - quality.json            — produced by build_index.py; contains a
                              "worst" list of {file, qs} where qs<70.
  - term_audit_worst.txt    — produced by term_audit.py; one file path
                              per line, ranked by term-consistency severity.

Behavior:
  1. Read both inputs (either may be missing).
  2. Compute the union, capped at MAX_RETRANSLATE files (default 50).
  3. Print the planned list.
  4. With --apply: delete the corresponding _zh.md files.
     Without --apply: print only (dry-run, default).

After --apply, run translate.py — it will see the missing _zh.md files
and re-translate them. Use a stronger model env in the workflow
(GLM_MODEL=glm-4-air) for higher quality on retries.

Exit code 0 always; this is a planner, not a gate.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

STATS_DIR = Path("stats")
QUALITY_FILE = STATS_DIR / "quality.json"
TERM_AUDIT_WORST = STATS_DIR / "term_audit_worst.txt"

DEFAULT_MAX = int(os.environ.get("MAX_RETRANSLATE", "50"))
QUALITY_THRESHOLD = int(os.environ.get("QUALITY_THRESHOLD", "70"))


def load_quality_worst(threshold: int) -> list[tuple[str, int]]:
    """Return [(file, qs)] for files below threshold, ranked worst-first."""
    if not QUALITY_FILE.exists():
        print(f"  (no {QUALITY_FILE} — skipping quality-based selection)")
        return []
    try:
        data = json.loads(QUALITY_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  WARN: failed to parse {QUALITY_FILE}: {e}")
        return []
    worst = data.get("worst") or data.get("worst_files") or []
    out: list[tuple[str, int]] = []
    for entry in worst:
        if isinstance(entry, dict):
            f = entry.get("file") or entry.get("path")
            qs = entry.get("qs") or entry.get("score")
            if f and isinstance(qs, (int, float)) and qs < threshold:
                out.append((f, int(qs)))
    out.sort(key=lambda x: x[1])  # ascending qs (worst first)
    return out


def load_term_audit_worst() -> list[str]:
    if not TERM_AUDIT_WORST.exists():
        print(f"  (no {TERM_AUDIT_WORST} — skipping term-audit selection)")
        return []
    try:
        lines = [
            ln.strip() for ln in TERM_AUDIT_WORST.read_text(encoding="utf-8").splitlines()
            if ln.strip()
        ]
        return lines
    except Exception as e:
        print(f"  WARN: failed to read {TERM_AUDIT_WORST}: {e}")
        return []


def _en_path_for_zh(zh_path_str: str) -> Path | None:
    """Map an _zh.md path to its EN counterpart. Returns None if mapping doesn't apply."""
    if zh_path_str.endswith("_zh.md"):
        return Path(zh_path_str[:-len("_zh.md")] + ".md")
    # quality.json may already store EN paths
    if zh_path_str.endswith(".md"):
        return Path(zh_path_str)
    return None


def _zh_path_for_any(path_str: str) -> Path | None:
    """Given either an EN or ZH path string, return the ZH file path."""
    if path_str.endswith("_zh.md"):
        return Path(path_str)
    if path_str.endswith(".md"):
        return Path(path_str[:-len(".md")] + "_zh.md")
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply", action="store_true",
        help="Actually delete the _zh.md files. Without this flag, runs in dry-run mode.",
    )
    parser.add_argument(
        "--max", type=int, default=DEFAULT_MAX,
        help=f"Maximum files to queue for retranslation (default {DEFAULT_MAX}).",
    )
    parser.add_argument(
        "--quality-threshold", type=int, default=QUALITY_THRESHOLD,
        help=f"Files with qs < this are queued (default {QUALITY_THRESHOLD}).",
    )
    args = parser.parse_args()

    print(f"Worst-N retranslate planner (max={args.max}, qs threshold<{args.quality_threshold})")
    print(f"Mode: {'APPLY (will delete files)' if args.apply else 'DRY-RUN'}\n")

    print("Source 1: quality.json (low qs)")
    quality_worst = load_quality_worst(args.quality_threshold)
    print(f"  → {len(quality_worst)} files below threshold")

    print("\nSource 2: term_audit_worst.txt")
    audit_worst = load_term_audit_worst()
    print(f"  → {len(audit_worst)} files flagged by term audit")

    # Build the union, preserving rank: interleave so both sources contribute.
    seen: set[str] = set()
    queue: list[tuple[str, str]] = []  # (zh_path_str, reason)
    # Take top N/2 from each source first, then fill from remainders
    half = max(1, args.max // 2)

    for f, qs in quality_worst[:half]:
        zp = _zh_path_for_any(f)
        if not zp:
            continue
        s = str(zp).replace("\\", "/")
        if s in seen:
            continue
        seen.add(s)
        queue.append((s, f"quality qs={qs}"))

    for f in audit_worst[:half]:
        zp = _zh_path_for_any(f)
        if not zp:
            continue
        s = str(zp).replace("\\", "/")
        if s in seen:
            continue
        seen.add(s)
        queue.append((s, "term-audit"))

    # Fill any remaining slots from the longer source
    for f, qs in quality_worst[half:]:
        if len(queue) >= args.max:
            break
        zp = _zh_path_for_any(f)
        if not zp:
            continue
        s = str(zp).replace("\\", "/")
        if s in seen:
            continue
        seen.add(s)
        queue.append((s, f"quality qs={qs}"))
    for f in audit_worst[half:]:
        if len(queue) >= args.max:
            break
        zp = _zh_path_for_any(f)
        if not zp:
            continue
        s = str(zp).replace("\\", "/")
        if s in seen:
            continue
        seen.add(s)
        queue.append((s, "term-audit"))

    print(f"\nQueued {len(queue)} files for retranslation:")
    for i, (zp, reason) in enumerate(queue, 1):
        exists = "✓" if Path(zp).exists() else "✗ (already missing)"
        print(f"  {i:3}. [{reason:>16}] {zp}  {exists}")

    if not args.apply:
        print("\n(dry-run: no files deleted. Re-run with --apply to delete.)")
        return 0

    # APPLY
    deleted = 0
    skipped = 0
    for zp, _ in queue:
        p = Path(zp)
        if not p.exists():
            skipped += 1
            continue
        try:
            p.unlink()
            deleted += 1
        except Exception as e:
            print(f"  WARN: failed to delete {p}: {e}")
            skipped += 1
    print(f"\nDeleted {deleted} _zh.md files ({skipped} skipped). "
          f"Run translate.py next to recreate them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
