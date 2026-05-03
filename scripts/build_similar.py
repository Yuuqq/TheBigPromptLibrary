#!/usr/bin/env python3
"""Compute top-K similar prompts for each entry (Q4.3).

Algorithm:
  base_score(A, B) = |tags(A) ∩ tags(B)| / |tags(A) ∪ tags(B)|       (Jaccard)
  same_top_category_bonus    = +0.05 if A.category[0] == B.category[0]
  same_provider_bonus        = +0.10 if A.category == B.category

Outputs:
  stats/similar.json — { "<id>": [{"id": ..., "title": ..., "score": 0.42}, ... up to K] }

Designed to run AFTER build_index.py (reads prompts_index.json) and AFTER auto_tag.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

INDEX = Path("prompts_index.json")
OUT = Path("stats/similar.json")
TOP_K = 5
MIN_SCORE = 0.05  # don't include barely-similar items
MIN_TAGS = 2      # entries with fewer tags get no recommendations

def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    if inter == 0:
        return 0.0
    return inter / len(a | b)


def main() -> int:
    if not INDEX.exists():
        print(f"ERROR: {INDEX} not found. Run build_index.py first.", file=sys.stderr)
        return 1

    entries = json.loads(INDEX.read_text(encoding="utf-8"))
    print(f"Computing similar prompts for {len(entries)} entries (K={TOP_K})")

    # Pre-extract
    tagged = [
        {
            "id": e["id"],
            "title": e.get("title", ""),
            "tags": set(e.get("tags") or []),
            "category": e.get("category", ""),
            "top_cat": (e.get("category") or "").split("/")[0],
            "path_zh": e.get("path_zh", ""),
            "path_en": e.get("path_en", ""),
        }
        for e in entries
    ]

    out: dict[str, list[dict]] = {}
    skipped_low_tags = 0

    for i, a in enumerate(tagged):
        if len(a["tags"]) < MIN_TAGS:
            skipped_low_tags += 1
            continue
        scored: list[tuple[float, dict]] = []
        for j, b in enumerate(tagged):
            if i == j or not b["tags"]:
                continue
            s = jaccard(a["tags"], b["tags"])
            if s == 0.0:
                continue
            if a["category"] == b["category"] and a["category"]:
                s += 0.10
            elif a["top_cat"] == b["top_cat"] and a["top_cat"]:
                s += 0.05
            if s >= MIN_SCORE:
                scored.append((s, b))
        scored.sort(key=lambda x: -x[0])
        top = scored[:TOP_K]
        if not top:
            continue
        # Compact format: only id + score. Frontend looks up title/category/paths
        # by id from prompts_index.json (already loaded).
        out[a["id"]] = [{"id": b["id"], "score": round(s, 3)} for s, b in top]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(out, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
        encoding="utf-8",
    )
    avg_neighbors = (sum(len(v) for v in out.values()) / len(out)) if out else 0
    print(f"  → {len(out)} entries got recommendations (avg {avg_neighbors:.1f} neighbors each)")
    print(f"  → {skipped_low_tags} entries skipped (fewer than {MIN_TAGS} tags)")
    print(f"  → written to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
