#!/usr/bin/env python3
"""Term consistency audit for Chinese translations.

Walks every *_zh.md under TARGET_DIRS and checks whether the project's
canonical glossary (mirrors translate.py SYSTEM_PROMPT) was applied.
Two violation kinds are detected:

  1. WRONG_TRANSLATION: a known incorrect Chinese rendering is present
     (e.g. "代理" used for "agent" instead of "智能体").
  2. UNTRANSLATED: an English source term still appears in body text
     (excluded inside code blocks, inline code, links, and headings)
     when the glossary expects translation.

Outputs:
  stats/term_audit.json   — full structured report
  stats/term_audit.md     — human-readable summary (top 50 worst files)
  stats/term_audit_worst.txt — file paths only, one per line, for #Q3.4
                                (monthly retranslate worst-N workflow)

Run standalone: ``python scripts/term_audit.py``
Exit code is always 0 — this is a reporter, not a gate.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]
STATS_DIR = Path("stats")
WORST_LIMIT = 50

# --------------------------------------------------------------------------- #
# Glossary (mirrors SYSTEM_PROMPT in scripts/translate.py)
# --------------------------------------------------------------------------- #
# Each rule:
#   en_terms         : list of English source forms (case-insensitive match)
#   expected_zh      : the canonical Chinese rendering
#   wrong_zh         : alternative Chinese renderings that we treat as errors
#   allow_english    : if True, leaving the English term in zh body is fine
#                      (term may be kept in English per glossary)
TERM_RULES: list[dict] = [
    {"en_terms": ["large language model", "LLM"],
     "expected_zh": "大语言模型",
     "wrong_zh": ["大型语言模型", "巨型语言模型"],
     "allow_english": True},
    {"en_terms": ["prompt engineering"],
     "expected_zh": "提示词工程",
     "wrong_zh": ["提示工程", "Prompt 工程", "提示语工程"],
     "allow_english": False},
    {"en_terms": ["system prompt"],
     "expected_zh": "系统提示词",
     "wrong_zh": ["系统提示", "系统 prompt", "系统prompt"],
     "allow_english": False},
    {"en_terms": ["user prompt"],
     "expected_zh": "用户提示词",
     "wrong_zh": ["用户提示", "用户 prompt"],
     "allow_english": False},
    {"en_terms": ["AI agent", "agent"],
     "expected_zh": "智能体",
     "wrong_zh": ["代理", "代理人", "智能代理", "Agent"],
     "allow_english": False},
    {"en_terms": ["multi-agent"],
     "expected_zh": "多智能体",
     "wrong_zh": ["多代理", "多智能代理"],
     "allow_english": False},
    {"en_terms": ["jailbreak", "jailbreaking"],
     "expected_zh": "越狱",
     "wrong_zh": ["破解", "破狱"],
     "allow_english": False},
    {"en_terms": ["prompt injection"],
     "expected_zh": "提示词注入",
     "wrong_zh": ["提示注入", "Prompt 注入", "提示语注入"],
     "allow_english": False},
    {"en_terms": ["guardrails", "guardrail"],
     "expected_zh": "安全防护栏",
     "wrong_zh": ["护栏", "栅栏", "防护栏"],
     "allow_english": False},
    {"en_terms": ["red team", "red teaming"],
     "expected_zh": "红队",
     "wrong_zh": ["红色团队", "红军团"],
     "allow_english": True},
    {"en_terms": ["chain of thought", "chain-of-thought", "CoT"],
     "expected_zh": "思维链",
     "wrong_zh": ["思考链", "思考链条", "想法链"],
     "allow_english": True},
    {"en_terms": ["few-shot", "few shot"],
     "expected_zh": "少样本",
     "wrong_zh": ["小样本", "少量样本", "少镜头"],
     "allow_english": True},
    {"en_terms": ["zero-shot", "zero shot"],
     "expected_zh": "零样本",
     "wrong_zh": ["零镜头", "零样例"],
     "allow_english": True},
    {"en_terms": ["one-shot", "one shot"],
     "expected_zh": "单样本",
     "wrong_zh": ["一次样本", "一镜头"],
     "allow_english": True},
    {"en_terms": ["in-context learning", "in context learning"],
     "expected_zh": "上下文学习",
     "wrong_zh": ["语境学习", "上下文中学习"],
     "allow_english": True},
    {"en_terms": ["fine-tuning", "fine tuning", "fine-tune", "finetune"],
     "expected_zh": "微调",
     "wrong_zh": ["精调", "精细调整", "细调"],
     "allow_english": True},
    {"en_terms": ["RLHF"],
     "expected_zh": "基于人类反馈的强化学习",
     "wrong_zh": ["人类反馈强化学习", "强化学习人类反馈"],
     "allow_english": True},
    {"en_terms": ["embedding", "embeddings"],
     "expected_zh": "嵌入向量",
     "wrong_zh": ["嵌入"],  # Bare "嵌入" without "向量" is too vague
     "allow_english": True},
    {"en_terms": ["vector database"],
     "expected_zh": "向量数据库",
     "wrong_zh": ["矢量数据库", "Vector DB"],
     "allow_english": True},
    {"en_terms": ["RAG", "retrieval-augmented generation", "retrieval augmented generation"],
     "expected_zh": "检索增强生成",
     "wrong_zh": ["检索增强型生成", "增强检索生成"],
     "allow_english": True},
    {"en_terms": ["context window"],
     "expected_zh": "上下文窗口",
     "wrong_zh": ["语境窗口", "上下文长度"],
     "allow_english": True},
    {"en_terms": ["temperature"],
     "expected_zh": "温度参数",
     "wrong_zh": ["温度值"],  # Bare "温度" is OK in physics context
     "allow_english": True},
    {"en_terms": ["inference"],
     "expected_zh": "推理",
     "wrong_zh": ["推断", "推论"],
     "allow_english": True},
    {"en_terms": ["completion", "completions"],
     "expected_zh": "补全",
     "wrong_zh": ["完成", "完结"],
     "allow_english": True},
    {"en_terms": ["hallucination", "hallucinations"],
     "expected_zh": "幻觉",
     "wrong_zh": ["臆造", "虚构"],
     "allow_english": True},
    {"en_terms": ["assistant"],
     "expected_zh": "助手",
     "wrong_zh": ["辅助", "助理"],  # 助理 is close but inconsistent
     "allow_english": True},
    {"en_terms": ["tool use", "tool calling", "function calling", "function call"],
     "expected_zh": "工具调用",
     "wrong_zh": ["工具使用", "函数使用"],
     "allow_english": True},
    {"en_terms": ["reasoning model"],
     "expected_zh": "推理模型",
     "wrong_zh": ["推断模型", "思考模型"],
     "allow_english": True},
    {"en_terms": ["knowledge cutoff"],
     "expected_zh": "知识截止日期",
     "wrong_zh": ["知识截至", "知识截止时间"],
     "allow_english": True},
    {"en_terms": ["self-attention"],
     "expected_zh": "自注意力",
     "wrong_zh": ["自我注意", "自注意机制"],
     "allow_english": True},
    {"en_terms": ["diffusion model"],
     "expected_zh": "扩散模型",
     "wrong_zh": ["传播模型"],
     "allow_english": True},
    {"en_terms": ["multimodal"],
     "expected_zh": "多模态",
     "wrong_zh": ["跨模态", "多模式"],
     "allow_english": True},
    {"en_terms": ["refusal", "refuse"],
     "expected_zh": "拒绝",
     "wrong_zh": ["拒否", "回绝"],
     "allow_english": False},
    {"en_terms": ["persona"],
     "expected_zh": "人设",
     "wrong_zh": ["人格", "角色身份"],
     "allow_english": True},
    {"en_terms": ["role-play", "roleplay", "role play"],
     "expected_zh": "角色扮演",
     "wrong_zh": ["扮演", "角色游戏"],
     "allow_english": True},
    {"en_terms": ["workflow"],
     "expected_zh": "工作流",
     "wrong_zh": ["工作流程", "工作流水"],
     "allow_english": True},
    {"en_terms": ["pipeline"],
     "expected_zh": "流水线",
     "wrong_zh": ["管道", "管线"],
     "allow_english": True},
]


# --------------------------------------------------------------------------- #
# Body extraction: strip code/inline-code/links/headings
# --------------------------------------------------------------------------- #
_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]+\)")
_URL_RE = re.compile(r"https?://\S+")
_HEADING_RE = re.compile(r"^#+\s.*$", re.MULTILINE)


def extract_body(zh_text: str) -> str:
    """Return zh_text with code, links, URLs, and headings stripped.
    Headings often legitimately contain English (preserved per style guide),
    so they're excluded from "untranslated English term" detection.
    """
    t = _CODE_BLOCK_RE.sub(" ", zh_text)
    t = _INLINE_CODE_RE.sub(" ", t)
    t = _LINK_RE.sub(r"\1", t)  # keep link text, drop URL
    t = _URL_RE.sub(" ", t)
    t = _HEADING_RE.sub(" ", t)
    return t


# --------------------------------------------------------------------------- #
# Audit logic
# --------------------------------------------------------------------------- #
def _word_pattern(term: str) -> re.Pattern:
    """Build a case-insensitive whole-word regex for an English term.
    Multi-word terms allow any whitespace between words.
    """
    parts = [re.escape(p) for p in term.split()]
    body = r"\s+".join(parts)
    # Boundary: start/end on non-word chars (works for ASCII; Chinese is non-word)
    return re.compile(rf"(?<![A-Za-z0-9_-]){body}(?![A-Za-z0-9_-])", re.IGNORECASE)


# Pre-compile all patterns once
_RULE_RUNTIME: list[dict] = []
for rule in TERM_RULES:
    _RULE_RUNTIME.append({
        "en_patterns": [_word_pattern(t) for t in rule["en_terms"]],
        "en_terms": rule["en_terms"],
        "expected_zh": rule["expected_zh"],
        "wrong_zh": rule["wrong_zh"],
        "allow_english": rule["allow_english"],
    })


def audit_file(path: Path) -> list[dict]:
    """Return a list of issue dicts found in this _zh.md file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if len(text.strip()) < 10:
        return []
    body = extract_body(text)
    issues: list[dict] = []

    for rule in _RULE_RUNTIME:
        # 1) WRONG_TRANSLATION: any wrong_zh present in body
        for wrong in rule["wrong_zh"]:
            count = body.count(wrong)
            if count > 0:
                # If the expected_zh is ALSO present, lower the severity
                # (might be deliberate — e.g. defining the wrong term then giving the right one)
                expected_present = rule["expected_zh"] in body
                issues.append({
                    "kind": "wrong_translation",
                    "term": rule["en_terms"][0],
                    "wrong_zh": wrong,
                    "expected_zh": rule["expected_zh"],
                    "count": count,
                    "severity": "low" if expected_present else "high",
                })

        # 2) UNTRANSLATED: english term appears in body and policy says translate
        if not rule["allow_english"]:
            for pat, term in zip(rule["en_patterns"], rule["en_terms"]):
                matches = pat.findall(body)
                if matches:
                    issues.append({
                        "kind": "untranslated",
                        "term": term,
                        "expected_zh": rule["expected_zh"],
                        "count": len(matches),
                        "severity": "medium",
                    })
    return issues


def severity_score(issue: dict) -> int:
    base = {"high": 5, "medium": 3, "low": 1}[issue["severity"]]
    return base * issue["count"]


def main() -> int:
    STATS_DIR.mkdir(parents=True, exist_ok=True)

    files: list[Path] = []
    for d in TARGET_DIRS:
        base = Path(d)
        if base.exists():
            files.extend(sorted(base.rglob("*_zh.md")))

    print(f"Auditing {len(files)} _zh.md files against {len(TERM_RULES)} term rules...")

    per_file: list[dict] = []
    term_aggregate: dict[str, dict] = defaultdict(
        lambda: {"wrong_translations": Counter(), "untranslated_count": 0, "files": set()}
    )
    issue_kind_count = Counter()

    for f in files:
        issues = audit_file(f)
        if not issues:
            continue
        score = sum(severity_score(i) for i in issues)
        per_file.append({
            "file": str(f).replace("\\", "/"),
            "score": score,
            "issue_count": len(issues),
            "issues": issues,
        })
        for issue in issues:
            issue_kind_count[issue["kind"]] += issue["count"]
            agg = term_aggregate[issue["term"]]
            agg["files"].add(str(f).replace("\\", "/"))
            if issue["kind"] == "wrong_translation":
                agg["wrong_translations"][issue["wrong_zh"]] += issue["count"]
            else:
                agg["untranslated_count"] += issue["count"]

    per_file.sort(key=lambda r: r["score"], reverse=True)
    worst = per_file[:WORST_LIMIT]

    # Build the JSON report
    term_report: dict[str, dict] = {}
    for term, agg in term_aggregate.items():
        # Find the canonical rule for this term to surface expected_zh
        expected = next(
            (r["expected_zh"] for r in TERM_RULES if term in r["en_terms"]),
            "?",
        )
        term_report[term] = {
            "expected_zh": expected,
            "wrong_translations": dict(agg["wrong_translations"]),
            "untranslated_count": agg["untranslated_count"],
            "file_count": len(agg["files"]),
        }

    report = {
        "version": 1,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "total_files_scanned": len(files),
        "files_with_issues": len(per_file),
        "issue_kind_totals": dict(issue_kind_count),
        "term_breakdown": term_report,
        "worst_files": worst,
    }

    json_path = STATS_DIR / "term_audit.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  → {json_path} ({len(per_file)} files with issues)")

    # Markdown summary
    md_lines: list[str] = []
    md_lines.append(f"# 术语一致性审计报告\n")
    md_lines.append(f"- 审计时间：{report['audited_at']}")
    md_lines.append(f"- 扫描文件：{len(files)}")
    md_lines.append(f"- 有问题的文件：{len(per_file)}")
    md_lines.append(f"- 错误总计：{dict(issue_kind_count)}")
    md_lines.append("\n## 高频问题术语 Top 15\n")
    md_lines.append("| 英文术语 | 标准译法 | 涉及文件数 | 错误译法分布 | 未翻译次数 |")
    md_lines.append("|---|---|---|---|---|")
    sorted_terms = sorted(
        term_report.items(),
        key=lambda kv: kv[1]["file_count"],
        reverse=True,
    )[:15]
    for term, info in sorted_terms:
        wrong_str = ", ".join(f"`{k}`×{v}" for k, v in sorted(info["wrong_translations"].items(), key=lambda x: -x[1])[:3]) or "—"
        md_lines.append(
            f"| {term} | {info['expected_zh']} | {info['file_count']} | {wrong_str} | {info['untranslated_count']} |"
        )
    md_lines.append(f"\n## 待重译 worst-{WORST_LIMIT} 文件\n")
    md_lines.append("| 排名 | 文件 | 严重度评分 | 问题数 |")
    md_lines.append("|---|---|---|---|")
    for i, row in enumerate(worst, 1):
        md_lines.append(f"| {i} | `{row['file']}` | {row['score']} | {row['issue_count']} |")
    md_lines.append("")

    md_path = STATS_DIR / "term_audit.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  → {md_path}")

    # Worst-N path list (for #Q3.4 retranslate workflow to consume)
    txt_path = STATS_DIR / "term_audit_worst.txt"
    txt_path.write_text("\n".join(r["file"] for r in worst) + "\n", encoding="utf-8")
    print(f"  → {txt_path}")

    print(
        f"\nDone. {len(per_file)}/{len(files)} files have issues "
        f"({issue_kind_count.get('wrong_translation', 0)} wrong, "
        f"{issue_kind_count.get('untranslated', 0)} untranslated). "
        f"See stats/term_audit.md for the summary."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
