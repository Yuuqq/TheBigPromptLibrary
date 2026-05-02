#!/usr/bin/env python3
"""Translate .md files to Chinese (_zh.md) using a chain of LLM providers.

Features:
- Multi-provider chain (GLM → Qwen → DeepSeek), auto-fallback on failure (#Q3.3).
- Diff-based translation: only translate paragraphs that changed since previous
  upstream version (#Q3.1). Falls back to full file translation when no prior
  version is available or paragraph alignment fails.
- Translation memory cache (#Q3.2): SHA-256 hashed paragraph → translation,
  shared across files. LRU-evicted at 5000 entries; persisted in
  stats/translation_memory.json.
- All previous behaviors preserved: oversized chunking, RETRANSLATE_OLDER_THAN,
  per-run stats, error log, oversized list.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import requests

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
TARGET_DIRS = ["SystemPrompts", "CustomInstructions", "Articles", "Jailbreak", "Security"]

MAX_FILES_PER_RUN = int(os.environ.get("MAX_FILES_PER_RUN", "40"))
MAX_FILE_CHARS = int(os.environ.get("MAX_FILE_CHARS", "30000"))
TRANSLATE_OVERSIZED = os.environ.get("TRANSLATE_OVERSIZED", "1") == "1"
MAX_OVERSIZED_PER_RUN = int(os.environ.get("MAX_OVERSIZED_PER_RUN", "5"))
CHUNK_TARGET_CHARS = int(os.environ.get("CHUNK_TARGET_CHARS", "12000"))
RETRANSLATE_OLDER_THAN = os.environ.get("RETRANSLATE_OLDER_THAN", "").strip()
MAX_RETRIES = 3
REQUEST_TIMEOUT = 300
SLEEP_BETWEEN = 1.0

# Diff-translate config
DIFF_TRANSLATE_ENABLED = os.environ.get("DIFF_TRANSLATE", "1") == "1"
DIFF_FALLBACK_RATIO = float(os.environ.get("DIFF_FALLBACK_RATIO", "0.5"))  # >50% changed → full

# Translation memory config
TM_ENABLED = os.environ.get("TM_ENABLED", "1") == "1"
TM_MAX_ENTRIES = int(os.environ.get("TM_MAX_ENTRIES", "5000"))
TM_MIN_PARA_CHARS = int(os.environ.get("TM_MIN_PARA_CHARS", "60"))
TM_MAX_PARA_CHARS = int(os.environ.get("TM_MAX_PARA_CHARS", "3000"))

STATS_DIR = Path("stats")
STATS_LOG = STATS_DIR / "translation-runs.jsonl"
ERROR_LOG = STATS_DIR / "translation-errors.log"
TM_FILE = STATS_DIR / "translation_memory.json"

SYSTEM_PROMPT = """你是专业的 AI / LLM 领域中英翻译专家。请把英文 Markdown 翻译成简体中文。

严格要求：
1. 保留所有 Markdown 格式（标题、列表、链接、粗体、斜体等）原样
2. 代码块（``` 包围的内容）原样不动，不要翻译代码
3. 行内代码（` 包围的内容）原样不动
4. 保留变量名、函数名、文件路径、URL、英文专有名词
5. 翻译符合中文表达习惯，技术术语使用业界通用译法
6. 提示词（system prompt）的指令性内容要准确翻译，保持原意
7. 直接输出翻译结果，不要任何解释、前后缀或思考过程

术语表（必须严格遵守，括号内为指定中译，斜杠表示可保留英文）：
- LLM / Large Language Model → 大语言模型
- prompt → 提示词
- system prompt → 系统提示词
- user prompt → 用户提示词
- prompt engineering → 提示词工程
- agent / AI agent → 智能体
- multi-agent → 多智能体
- jailbreak → 越狱
- prompt injection → 提示词注入
- guardrails → 安全防护栏
- alignment → 对齐
- red team / red teaming → 红队 / 红队测试
- chain of thought / CoT → 思维链
- few-shot → 少样本
- zero-shot → 零样本
- one-shot → 单样本
- in-context learning → 上下文学习
- fine-tune / fine-tuning → 微调
- RLHF → 基于人类反馈的强化学习（RLHF）
- embedding → 嵌入向量
- vector database → 向量数据库
- RAG / Retrieval-Augmented Generation → 检索增强生成（RAG）
- token → token（保留英文）
- context window → 上下文窗口
- temperature → 温度参数
- top-p / top-k → top-p / top-k（保留）
- inference → 推理
- completion → 补全
- chat completion → 对话补全
- hallucination → 幻觉
- grounding → 信息基底 / 锚定
- assistant → 助手
- tool use / function calling → 工具调用 / 函数调用
- reasoning model → 推理模型
- thinking / chain-of-thought → 思考过程 / 思维链
- knowledge cutoff → 知识截止日期
- self-attention → 自注意力
- transformer → Transformer（保留）
- diffusion model → 扩散模型
- multimodal → 多模态
- vision-language → 视觉语言
- safety / safety policy → 安全 / 安全策略
- refusal → 拒绝回答
- persona → 人设
- role-play → 角色扮演
- character → 角色
- workflow → 工作流
- pipeline → 流水线
- 主流模型/产品名保留英文：ChatGPT, Claude, Gemini, GPT-4, GPT-4o, GPT-5, o1, o3, Llama, Mistral, Qwen, DeepSeek, Copilot, Grok, Cursor, Perplexity, V0, Cline 等"""


# --------------------------------------------------------------------------- #
# Provider chain (#Q3.3)
# --------------------------------------------------------------------------- #
ALL_PROVIDERS = {
    "glm": {
        "name": "glm",
        "env_key": "GLM_API_KEY",
        "model_env": "GLM_MODEL",
        "default_model": "glm-z1-flash",
        "url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "strip_think": True,
    },
    "qwen": {
        "name": "qwen",
        "env_key": "QWEN_API_KEY",  # DashScope OpenAI-compatible mode
        "model_env": "QWEN_MODEL",
        "default_model": "qwen-turbo",
        "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "strip_think": False,
    },
    "deepseek": {
        "name": "deepseek",
        "env_key": "DEEPSEEK_API_KEY",
        "model_env": "DEEPSEEK_MODEL",
        "default_model": "deepseek-chat",
        "url": "https://api.deepseek.com/chat/completions",
        "strip_think": False,
    },
}


def _build_provider_chain() -> list[dict]:
    """Build active provider chain from env: only providers with API keys are active."""
    chain_env = os.environ.get("LLM_PROVIDER_CHAIN", "glm,qwen,deepseek")
    requested = [p.strip() for p in chain_env.split(",") if p.strip()]
    chain: list[dict] = []
    for name in requested:
        spec = ALL_PROVIDERS.get(name)
        if not spec:
            print(f"  WARN: unknown provider '{name}' in LLM_PROVIDER_CHAIN, skipping")
            continue
        api_key = os.environ.get(spec["env_key"])
        if not api_key:
            print(f"  INFO: provider '{name}' skipped ({spec['env_key']} not set)")
            continue
        active = dict(spec)
        active["api_key"] = api_key
        active["model"] = os.environ.get(spec["model_env"], spec["default_model"])
        chain.append(active)
    return chain


PROVIDER_CHAIN = _build_provider_chain()
if not PROVIDER_CHAIN:
    print("ERROR: no LLM provider has its API key configured. Set GLM_API_KEY (or QWEN_API_KEY / DEEPSEEK_API_KEY).", file=sys.stderr)
    sys.exit(1)
print(f"Active provider chain: {[p['name'] + ':' + p['model'] for p in PROVIDER_CHAIN]}")

# Stats counters keyed by provider name
PROVIDER_STATS: dict[str, dict] = {p["name"]: {"calls": 0, "tokens_in": 0, "tokens_out": 0, "failures": 0} for p in PROVIDER_CHAIN}


def _post_one_provider(provider: dict, content: str) -> tuple[str, dict]:
    """Single provider call with internal MAX_RETRIES on transient errors. Raises on hard fail."""
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(
                provider["url"],
                headers={
                    "Authorization": f"Bearer {provider['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": provider["model"],
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
                print(f"    [{provider['name']}] rate-limited, waiting {wait}s")
                time.sleep(wait)
                continue
            if 500 <= resp.status_code < 600:
                wait = 5 * (attempt + 1)
                print(f"    [{provider['name']}] server error {resp.status_code}, waiting {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            if provider.get("strip_think"):
                text = re.sub(r"<think>[\s\S]*?</think>", "", text).strip()
            text = re.sub(r"^```(?:markdown|md)?\n([\s\S]*?)\n```$", r"\1", text).strip()
            usage = data.get("usage", {}) or {}
            return text, usage
        except Exception as e:
            last_err = e
            print(f"    [{provider['name']}] attempt {attempt + 1} failed: {e}")
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"provider {provider['name']} exhausted {MAX_RETRIES} retries: {last_err}")


def call_llm(content: str) -> tuple[str, dict, str]:
    """Try each provider in order; return (text, usage, provider_name) from the first that succeeds."""
    last_err: Exception | None = None
    for provider in PROVIDER_CHAIN:
        try:
            text, usage = _post_one_provider(provider, content)
            PROVIDER_STATS[provider["name"]]["calls"] += 1
            PROVIDER_STATS[provider["name"]]["tokens_in"] += int(usage.get("prompt_tokens", 0))
            PROVIDER_STATS[provider["name"]]["tokens_out"] += int(usage.get("completion_tokens", 0))
            return text, usage, provider["name"]
        except Exception as e:
            PROVIDER_STATS[provider["name"]]["failures"] += 1
            last_err = e
            print(f"  provider '{provider['name']}' failed: {e}; trying next provider")
    raise RuntimeError(f"all {len(PROVIDER_CHAIN)} providers failed; last error: {last_err}")


# --------------------------------------------------------------------------- #
# Translation memory (#Q3.2)
# --------------------------------------------------------------------------- #
TM: dict[str, dict] = {}  # hash -> {en, zh, hits, last}
TM_LOADED = False
TM_RUN_STATS = {"hits": 0, "misses": 0, "stores": 0}


def _normalize_para(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def _para_key(s: str) -> str:
    return hashlib.sha256(_normalize_para(s).encode("utf-8")).hexdigest()[:16]


def _para_eligible_for_tm(s: str) -> bool:
    if not s.strip():
        return False
    if not (TM_MIN_PARA_CHARS <= len(s) <= TM_MAX_PARA_CHARS):
        return False
    # Skip pure code blocks / tables / images — they're either not translated
    # or too structurally specific to reuse.
    stripped = s.strip()
    if stripped.startswith("```") or stripped.startswith("|") or stripped.startswith("!["):
        return False
    return True


def load_tm() -> None:
    global TM, TM_LOADED
    if not TM_ENABLED or TM_LOADED:
        return
    TM_LOADED = True
    if not TM_FILE.exists():
        print(f"TM: starting fresh (no {TM_FILE})")
        return
    try:
        raw = json.loads(TM_FILE.read_text(encoding="utf-8"))
        TM = raw.get("entries", {}) if isinstance(raw, dict) else {}
        print(f"TM: loaded {len(TM)} entries from {TM_FILE}")
    except Exception as e:
        print(f"TM: load failed ({e}); starting fresh")
        TM = {}


def tm_lookup(en_para: str) -> str | None:
    if not TM_ENABLED or not _para_eligible_for_tm(en_para):
        return None
    key = _para_key(en_para)
    entry = TM.get(key)
    if not entry:
        TM_RUN_STATS["misses"] += 1
        return None
    # Defense against hash collision: confirm normalized prefix matches
    if entry.get("en_norm_prefix") != _normalize_para(en_para)[:120]:
        TM_RUN_STATS["misses"] += 1
        return None
    entry["hits"] = entry.get("hits", 0) + 1
    entry["last"] = datetime.now(timezone.utc).isoformat()
    TM_RUN_STATS["hits"] += 1
    return entry["zh"]


def tm_store(en_para: str, zh_para: str) -> None:
    if not TM_ENABLED or not _para_eligible_for_tm(en_para):
        return
    if not zh_para or len(zh_para) < 5:
        return
    key = _para_key(en_para)
    TM[key] = {
        "en_norm_prefix": _normalize_para(en_para)[:120],
        "zh": zh_para,
        "hits": TM.get(key, {}).get("hits", 0) + 1,
        "last": datetime.now(timezone.utc).isoformat(),
    }
    TM_RUN_STATS["stores"] += 1


def save_tm() -> None:
    if not TM_ENABLED or not TM_LOADED:
        return
    # LRU-style eviction: if over cap, drop entries with lowest hits, then oldest last
    if len(TM) > TM_MAX_ENTRIES:
        keep = sorted(
            TM.items(),
            key=lambda kv: (kv[1].get("hits", 0), kv[1].get("last", "")),
            reverse=True,
        )[:TM_MAX_ENTRIES]
        new_tm = dict(keep)
        print(f"TM: evicted {len(TM) - len(new_tm)} low-value entries (cap={TM_MAX_ENTRIES})")
        TM.clear()
        TM.update(new_tm)
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "updated": datetime.now(timezone.utc).isoformat(),
        "size": len(TM),
        "entries": TM,
    }
    TM_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"TM: saved {len(TM)} entries to {TM_FILE}")


# --------------------------------------------------------------------------- #
# Diff-based translation (#Q3.1)
# --------------------------------------------------------------------------- #
def _git_show(rev: str, path: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "show", f"{rev}:{path}"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode("utf-8", errors="replace")
    except Exception:
        return None


def _git_prior_commit(path: str) -> str | None:
    """Return the hash of the second-most-recent commit touching `path`, or None."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-2", "--pretty=format:%H", "--", path],
            stderr=subprocess.DEVNULL, text=True,
        ).strip().splitlines()
        return out[1] if len(out) >= 2 else None
    except Exception:
        return None


def fetch_prior_en(en_path: Path) -> str | None:
    """Fetch the previous version of an English file from git history."""
    p = str(en_path).replace("\\", "/")
    prior = _git_prior_commit(p)
    if not prior:
        return None
    return _git_show(prior, p)


def split_paragraphs(text: str) -> list[str]:
    """Split markdown by blank lines into paragraphs, preserving order.
    Empty (whitespace-only) entries are kept so indices map back faithfully.
    """
    return re.split(r"(?<=\n)\n+", text)


def diff_translate(en_path: Path, zh_path: Path, run_stats: dict) -> tuple[bool, str | None, dict]:
    """Try to translate only the changed paragraphs; reuse prior _zh for unchanged.

    Returns (success, full_zh_text, info). On any failure returns (False, None, info)
    and the caller falls back to full-file translation.
    """
    info = {"reason": "", "old_paras": 0, "new_paras": 0, "changed": 0, "reused": 0, "tm_hits": 0, "api_calls": 0}
    if not DIFF_TRANSLATE_ENABLED:
        info["reason"] = "diff_disabled"
        return False, None, info
    if not zh_path.exists():
        info["reason"] = "no_prior_zh"
        return False, None, info

    new_en = en_path.read_text(encoding="utf-8", errors="replace")
    old_en = fetch_prior_en(en_path)
    if old_en is None:
        info["reason"] = "no_git_history"
        return False, None, info
    try:
        old_zh = zh_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        info["reason"] = f"zh_read_failed:{e}"
        return False, None, info

    new_paras = split_paragraphs(new_en)
    old_en_paras = split_paragraphs(old_en)
    old_zh_paras = split_paragraphs(old_zh)

    info["old_paras"] = len(old_en_paras)
    info["new_paras"] = len(new_paras)

    # We require old_en and old_zh to have the same paragraph count for index-based mapping.
    # This holds for all files translated by this same script (paragraph-preserving).
    if len(old_en_paras) != len(old_zh_paras):
        info["reason"] = f"misaligned_old_{len(old_en_paras)}_vs_{len(old_zh_paras)}"
        return False, None, info

    # Build prior {normalized_en_para → zh_para}
    prior_map: dict[str, str] = {}
    for i, en_p in enumerate(old_en_paras):
        key = _normalize_para(en_p)
        if key:
            prior_map[key] = old_zh_paras[i]

    # Resolve every new paragraph: prior_map → TM → translate
    out_paras: list[str] = []
    for new_p in new_paras:
        if not new_p.strip():
            out_paras.append(new_p)
            continue
        norm = _normalize_para(new_p)
        if norm in prior_map:
            out_paras.append(prior_map[norm])
            info["reused"] += 1
            continue
        tm_hit = tm_lookup(new_p)
        if tm_hit is not None:
            out_paras.append(tm_hit)
            info["tm_hits"] += 1
            info["reused"] += 1
            continue
        info["changed"] += 1

    # If too much changed, fall back to full translate (better LLM context)
    eligible_for_change = sum(1 for p in new_paras if p.strip())
    if eligible_for_change and (info["changed"] / eligible_for_change) > DIFF_FALLBACK_RATIO:
        info["reason"] = f"too_many_changes_{info['changed']}/{eligible_for_change}"
        return False, None, info

    # Now actually translate the changed paragraphs (we re-walk so index aligns)
    out_paras = []
    for new_p in new_paras:
        if not new_p.strip():
            out_paras.append(new_p)
            continue
        norm = _normalize_para(new_p)
        if norm in prior_map:
            out_paras.append(prior_map[norm])
            continue
        tm_hit = tm_lookup(new_p)
        if tm_hit is not None:
            out_paras.append(tm_hit)
            continue
        # Translate this single paragraph
        try:
            translated, usage, provider = call_llm(new_p)
        except Exception as e:
            info["reason"] = f"llm_failed_on_para:{e}"
            return False, None, info
        if not translated or len(translated) < 3:
            info["reason"] = "empty_para_translation"
            return False, None, info
        out_paras.append(translated)
        tm_store(new_p, translated)
        info["api_calls"] += 1
        run_stats["tokens_in"] += int(usage.get("prompt_tokens", 0))
        run_stats["tokens_out"] += int(usage.get("completion_tokens", 0))
        time.sleep(SLEEP_BETWEEN)

    full_zh = "\n".join(out_paras) if not new_en.endswith("\n") else "\n".join(out_paras)
    # Preserve original join behavior: split_paragraphs splits on \n+, so rejoin with \n\n where needed.
    # Simpler & safer: join with \n\n for non-empty paras, preserve trailing newline.
    rebuilt: list[str] = []
    for p in out_paras:
        rebuilt.append(p if p.endswith("\n") else p + "\n")
    full_zh = "\n".join(rebuilt).rstrip() + "\n"
    info["reason"] = "ok"
    return True, full_zh, info


# --------------------------------------------------------------------------- #
# Existing helpers (preserved)
# --------------------------------------------------------------------------- #
_GIT_ZH_DATES: dict[str, str] | None = None


def _build_zh_git_dates() -> dict[str, str]:
    try:
        out = subprocess.check_output(
            ["git", "log", "--name-only", "--diff-filter=AM", "--pretty=format:%cs"],
            stderr=subprocess.DEVNULL, text=True,
        )
    except Exception:
        return {}
    dates: dict[str, str] = {}
    cur_date: str | None = None
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        if date_re.match(line):
            cur_date = line
        elif line.endswith("_zh.md") and cur_date and line not in dates:
            dates[line] = cur_date
    return dates


def _zh_git_date(zh_path: Path) -> str | None:
    global _GIT_ZH_DATES
    if _GIT_ZH_DATES is None:
        _GIT_ZH_DATES = _build_zh_git_dates()
    return _GIT_ZH_DATES.get(str(zh_path).replace("\\", "/"))


def needs_translation(en_path: Path) -> bool:
    zh_path = en_path.with_name(en_path.name.replace(".md", "_zh.md"))
    if not zh_path.exists():
        return True
    if en_path.stat().st_mtime > zh_path.stat().st_mtime:
        return True
    if RETRANSLATE_OLDER_THAN:
        d = _zh_git_date(zh_path)
        if d and d < RETRANSLATE_OLDER_THAN:
            return True
    return False


def is_translatable_size(en_path: Path) -> tuple[bool, int]:
    try:
        size = len(en_path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return False, 0
    return (10 <= size <= MAX_FILE_CHARS), size


def chunk_markdown(text: str, target: int) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(("# ", "## ")) and current:
            parts.append("".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        parts.append("".join(current))

    refined: list[str] = []
    cap = int(target * 1.5)
    for p in parts:
        if len(p) <= cap:
            refined.append(p)
            continue
        buf: list[str] = []
        size = 0
        for para in p.split("\n\n"):
            chunk_piece = para + "\n\n"
            if size + len(chunk_piece) > target and buf:
                refined.append("".join(buf))
                buf, size = [], 0
            buf.append(chunk_piece)
            size += len(chunk_piece)
        if buf:
            refined.append("".join(buf))
    return [c for c in refined if c.strip()]


def translate_oversized(en_path: Path, stats: dict) -> bool:
    content = en_path.read_text(encoding="utf-8", errors="replace")
    chunks = chunk_markdown(content, CHUNK_TARGET_CHARS)
    print(f"  chunked into {len(chunks)} pieces (avg {len(content)//max(1,len(chunks))} chars)")
    translated_chunks: list[str] = []
    for j, chunk in enumerate(chunks, 1):
        print(f"    chunk {j}/{len(chunks)} ({len(chunk)} chars)")
        # TM check on the whole chunk (rare hit for big chunks but possible for boilerplate)
        cached = tm_lookup(chunk)
        if cached is not None:
            translated_chunks.append(cached)
            continue
        try:
            t, usage, provider = call_llm(chunk)
        except Exception as e:
            print(f"    chunk failed: {e}")
            return False
        if not t or len(t) < 5:
            print("    empty chunk translation, aborting file")
            return False
        translated_chunks.append(t)
        tm_store(chunk, t)
        stats["tokens_in"] += int(usage.get("prompt_tokens", 0))
        stats["tokens_out"] += int(usage.get("completion_tokens", 0))
        time.sleep(SLEEP_BETWEEN)
    full = "\n\n".join(translated_chunks)
    zh_path = en_path.with_name(en_path.name.replace(".md", "_zh.md"))
    zh_path.write_text(full, encoding="utf-8")
    return True


def log_error(file_path: Path, err: Exception) -> None:
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with ERROR_LOG.open("a", encoding="utf-8") as fp:
        fp.write(f"\n--- {datetime.now(timezone.utc).isoformat()} {file_path} ---\n")
        fp.write("".join(traceback.format_exception(type(err), err, err.__traceback__)))


def write_stats(stats: dict) -> None:
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with STATS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(stats, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    load_tm()

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
        "providers_active": [p["name"] for p in PROVIDER_CHAIN],
        "primary_model": PROVIDER_CHAIN[0]["model"],
        "candidates": len(candidates),
        "oversized_deferred": len(oversized),
        "translated": 0,
        "translated_via_diff": 0,
        "translated_via_full": 0,
        "failed": 0,
        "tokens_in": 0,
        "tokens_out": 0,
        "duration_seconds": 0,
        "tm_enabled": TM_ENABLED,
        "diff_enabled": DIFF_TRANSLATE_ENABLED,
    }

    if not candidates:
        if oversized:
            STATS_DIR.mkdir(parents=True, exist_ok=True)
            (STATS_DIR / "oversized.txt").write_text(
                "\n".join(f"{p}\t{s}" for p, s in oversized) + "\n", encoding="utf-8"
            )
        # Still flush TM stats (diff-translate may have been considered)
        stats["tm_run"] = dict(TM_RUN_STATS)
        stats["tm_size"] = len(TM)
        stats["provider_breakdown"] = {k: v for k, v in PROVIDER_STATS.items() if v["calls"] or v["failures"]}
        write_stats(stats)
        save_tm()
        return 0

    batch = candidates[:MAX_FILES_PER_RUN]
    print(f"Will translate first {len(batch)} this run (cap={MAX_FILES_PER_RUN})")
    started_at = time.time()

    for i, en in enumerate(batch, 1):
        content = en.read_text(encoding="utf-8", errors="replace")
        size = len(content)
        zh_path = en.with_name(en.name.replace(".md", "_zh.md"))
        print(f"[{i}/{len(batch)}] {en} ({size} chars)")

        # Try diff-based translation first
        if DIFF_TRANSLATE_ENABLED and zh_path.exists():
            try:
                ok, text, info = diff_translate(en, zh_path, stats)
            except Exception as e:
                ok, text, info = False, None, {"reason": f"exception:{e}"}
            if ok and text:
                zh_path.write_text(text, encoding="utf-8")
                stats["translated"] += 1
                stats["translated_via_diff"] += 1
                print(
                    f"  ✓ DIFF-translated: {info['reused']} reused / "
                    f"{info['api_calls']} API calls / {info['tm_hits']} TM hits "
                    f"(of {info['new_paras']} paragraphs)"
                )
                time.sleep(SLEEP_BETWEEN)
                continue
            else:
                print(f"  diff-translate skipped ({info.get('reason', 'unknown')}); falling back to full")

        # Full file translation (default path)
        try:
            translated, usage, provider = call_llm(content)
            if not translated or len(translated) < 10:
                print("  empty translation, skipping")
                stats["failed"] += 1
                continue
            zh_path.write_text(translated, encoding="utf-8")
            stats["translated"] += 1
            stats["translated_via_full"] += 1
            stats["tokens_in"] += int(usage.get("prompt_tokens", 0))
            stats["tokens_out"] += int(usage.get("completion_tokens", 0))
            # Cache the file as a whole-document TM entry (rare hit but cheap to try)
            tm_store(content, translated)
            print(f"  ✓ FULL-translated via {provider}")
            time.sleep(SLEEP_BETWEEN)
        except Exception as e:
            print(f"  FAILED: {e}")
            stats["failed"] += 1
            log_error(en, e)

    stats["duration_seconds_normal"] = round(time.time() - started_at, 1)
    stats["pending_after_run"] = max(0, len(candidates) - len(batch))

    # ----- Oversized -----
    stats["oversized_translated"] = 0
    stats["oversized_failed"] = 0
    if TRANSLATE_OVERSIZED and oversized:
        oversized_batch = oversized[:MAX_OVERSIZED_PER_RUN]
        print(
            f"\nOversized batch: translating {len(oversized_batch)} of "
            f"{len(oversized)} oversized files (cap={MAX_OVERSIZED_PER_RUN})"
        )
        for k, (en, size) in enumerate(oversized_batch, 1):
            print(f"[oversized {k}/{len(oversized_batch)}] {en} ({size} chars)")
            try:
                ok = translate_oversized(en, stats)
                if ok:
                    stats["oversized_translated"] += 1
                else:
                    stats["oversized_failed"] += 1
            except Exception as e:
                print(f"  FAILED: {e}")
                stats["oversized_failed"] += 1
                log_error(en, e)

    if oversized:
        STATS_DIR.mkdir(parents=True, exist_ok=True)
        (STATS_DIR / "oversized.txt").write_text(
            "\n".join(f"{p}\t{s}" for p, s in oversized) + "\n", encoding="utf-8"
        )

    stats["duration_seconds"] = round(time.time() - started_at, 1)
    stats["tm_run"] = dict(TM_RUN_STATS)
    stats["tm_size"] = len(TM)
    stats["provider_breakdown"] = {k: v for k, v in PROVIDER_STATS.items() if v["calls"] or v["failures"]}
    write_stats(stats)
    save_tm()

    print(
        f"\nDone: {stats['translated']} translated "
        f"({stats['translated_via_diff']} via diff / {stats['translated_via_full']} full), "
        f"{stats['failed']} failed, {stats['pending_after_run']} pending; "
        f"oversized: {stats['oversized_translated']} ok / {stats['oversized_failed']} failed; "
        f"tokens in/out: {stats['tokens_in']}/{stats['tokens_out']}; "
        f"TM: {TM_RUN_STATS['hits']} hits / {TM_RUN_STATS['misses']} misses / size={len(TM)}; "
        f"providers: {stats['provider_breakdown']}; "
        f"{stats['duration_seconds']}s"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
