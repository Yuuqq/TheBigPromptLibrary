# 代码库地图 / Codebase Map

> 由 [GSD](https://github.com/gsd-build/get-shit-done) 风格生成的项目结构概览。
> 适用于 AI 编码助手（Claude Code / OpenCode / Cursor / Codex / Copilot 等）快速建立上下文。
>
> Last updated: 2026-05-03 · Commit: `abb42e7c`

---

## 1. 项目定位 (STACK)

**类型**: 静态内容仓库 + GitHub Pages 站点
**用途**: [0xeb/TheBigPromptLibrary](https://github.com/0xeb/TheBigPromptLibrary) 的中文翻译镜像
**部署**: GitHub Pages → 自定义域名 `thebigpromptlibrary.aisbest.eu.cc`
**语言栈**:
- Python 3.11 (脚本与 CI 工作流)
- Vanilla JS / HTML / CSS (前端，零框架)
- Markdown (内容主体)

**关键依赖**:
- `openai` Python SDK — 调用翻译模型（自动翻译流水线）
- 无前端构建工具 — `docs/index.html` 为单文件应用，IIFE 内联 JS

---

## 2. 架构 (ARCHITECTURE)

```
┌─────────────────────────────────────────────────────────────┐
│  上游 0xeb/TheBigPromptLibrary  (英文原版)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ scripts/sync_upstream.py (rsync 风格)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  本仓库 Yuuqq/TheBigPromptLibrary                            │
│                                                              │
│  ┌──────────────┐  scripts/translate.py   ┌──────────────┐  │
│  │ 英文 .md 内容 │ ─────────────────────► │ 中文 .md 内容 │  │
│  └──────────────┘   (TM cache + LLM)      └──────────────┘  │
│                                                  │           │
│           ┌──────────────────────────────────────┘           │
│           ▼                                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ scripts/build_*.py — 索引构建器                      │   │
│  │   build_index.py        → docs/index.json            │   │
│  │   build_search_index.py → docs/search-index.json     │   │
│  │   build_similar.py      → docs/similar.json          │   │
│  │   auto_tag.py           → stats/tags.json            │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           ▼                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ docs/ — GitHub Pages 站点                            │   │
│  │   index.html  — 单页应用 (header/list/viewer/search) │   │
│  │   compare.html — 中英对照视图                        │   │
│  │   sw.js       — Service Worker (network-first)       │   │
│  │   manifest.json — PWA manifest                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
                 GitHub Pages CDN
                 (custom domain via CNAME)
```

**触发流**:
- **每日自动**: `.github/workflows/sync-and-translate.yml` (定时 cron) → 拉上游 → 翻译变化 → 重建索引 → 提交
- **手动**: workflow_dispatch + 直接 commit
- **数据刷新**（Q4 增量计划）: `q4-refresh-data.yml` 在 sync 后跑增量重建（待手动复制到 `.github/workflows/`）

---

## 3. 目录结构 (STRUCTURE)

```
TheBigPromptLibrary/
├── README.md                # 中文项目首页（本仓库定制）
├── README_zh.md             # 上游 README 的中文翻译（保留兼容）
│
├── CustomInstructions/      # 3,388 .md  GPT 自定义指令
│   ├── ChatGPT/             # 主体（大量 .md）
│   ├── Gemini/
│   └── Gab.ai/
│
├── SystemPrompts/           #   238 .md  各厂商系统提示词
│   ├── OpenAI/  Anthropic/  Google/  Meta.ai/  Copilot/
│   ├── Perplexity.ai/  xAI/  Mistral/  ...
│
├── Jailbreak/               #    14 .md  教育性越狱样例
├── Security/                #   104 .md  GPT 防护机制
├── Articles/                #    10 .md  研究文章
├── Tools/                   #     4 .md  工具与脚本说明
│
├── scripts/                 # 自动化 Python 脚本
│   ├── sync_upstream.py     # 拉取上游变更
│   ├── translate.py         # LLM 翻译（含 TM 缓存 + 失败链路 fast-fail）
│   ├── retranslate_worst.py # 重译质量最差的 N 个
│   ├── auto_tag.py          # 自动打标 → stats/tags.json
│   ├── term_audit.py        # 术语一致性审计
│   ├── build_index.py       # 主索引（卡片列表）
│   ├── build_search_index.py # 全文搜索倒排索引
│   ├── build_similar.py     # "相似条目"推荐
│   └── test_scripts.py      # 脚本自测
│
├── docs/                    # GitHub Pages 站点根目录
│   ├── index.html           # 单页应用（~131KB）
│   ├── compare.html         # 中英对照视图
│   ├── sw.js                # Service Worker (v2: same-origin network-first)
│   ├── manifest.json        # PWA manifest
│   ├── ROADMAP.md
│   ├── index.json           # 卡片列表数据 (build_index.py 产物)
│   ├── search-index.json    # 全文检索数据
│   └── similar.json         # 相似度数据
│
├── stats/
│   └── tags.json            # 自动标签数据 (~566KB, 懒加载)
│
├── .github/
│   └── workflows/
│       └── sync-and-translate.yml  # 主流水线
│
└── .planning/               # GSD 元数据（本目录）
    └── codebase/
        └── INDEX.md         # 本文件
```

---

## 4. 前端约定 (CONVENTIONS)

### 单文件设计
- `docs/index.html` 包含全部 CSS + JS（IIFE 内联）
- 主要 JS 块用 `<script id="...">` 标记，便于脚本化重注入：
  - `<script id="q4-features">` — Q4 增强模块（搜索/标签/对比/差异/PWA 等）
  - 源文件托管在 `/tmp/q4/q4-features.js`（开发态），通过正则替换回 HTML

### 主题
- `data-theme="light"` 触发 light mode（默认 dark）
- 关键变量: `--bg-primary`, `--bg-secondary`, `--text-primary`, `--accent-blue`
- header 在 dark 时硬编码深色，light 时通过 `[data-theme="light"] header` 覆盖

### Service Worker 缓存策略
- **同源资源**: `network-first` + cache fallback（避免站点更新后旧版长期卡住）
- **第三方 CDN**: `cache-first`
- **GitHub API**: `network-only`
- 升级版本号: 改 `CACHE_VERSION` 字符串

### 数据加载
- `index.json` / `search-index.json`: 启动时 fetch（核心）
- `tags.json` (566KB): **懒加载**，首次 `enhanceCards()` 时触发，到达后回填已渲染卡片
- `similar.json`: 进入 viewer 后按需加载

---

## 5. 翻译流水线 (INTEGRATIONS)

**模型**: OpenAI 兼容 API（`scripts/translate.py` 中通过 env 变量配置）
**TM 缓存**: 段落级哈希，复用历史翻译降低成本
**故障处理**:
- 429 / 5xx → fast-fail 整条链路（不重试同段落）
- 单 pass 计算 diff，避免 TM 命中率重复计数
- `retranslate_worst.py` 周期性把质量最差的 N 个段落重新翻译

**所需 secrets** (GitHub repo settings):
- `OPENAI_API_KEY` — 翻译模型
- `OPENAI_BASE_URL` — 自定义端点（如代理）
- `OPENAI_MODEL` — 模型 ID

---

## 6. 测试与质量 (TESTING)

**自动化**:
- `scripts/test_scripts.py` — Python 脚本自测
- `scripts/term_audit.py` — 跨文件术语一致性检查（运行后人工审阅 diff）
- `scripts/retranslate_worst.py --plan` — 输出待重译清单（不立即写）

**人工回归** (前端变更必做):
- viewer 中英切换 → Q4 增强（对比按钮、标签芯片）应保留
- 搜索框输入 A → 修改为 B → 下拉应正确刷新（不卡在旧结果）
- light / dark 主题切换 → 顶栏、卡片、链接配色一致
- 离线访问（kill 网络后 reload）→ Service Worker 应回退到缓存

---

## 7. 已知关注点 (CONCERNS)

| 等级 | 项 | 备注 |
|---|---|---|
| 中 | RAW SWR 首次访问可能短暂显示陈旧 viewer 内容 | 第二次访问即时新鲜 |
| 中 | `q4-refresh-data.yml` 仍未复制到 `.github/workflows/` | GitHub App 无 `workflows:write` 权限，需仓库主手动复制 |
| 低 | `tags.json` 持续膨胀 | 当前 566KB，已懒加载缓解；超过 ~2MB 时考虑分片 |
| 低 | 单文件 `docs/index.html` ~131KB | 维护成本高但部署极简，暂不拆分 |
| 信息 | LLM 翻译可能存在术语漂移 | 用 `term_audit.py` 周期检查 |

---

## 8. 维护命令速查

```bash
# 拉取上游
python scripts/sync_upstream.py

# 翻译新增/变更内容
python scripts/translate.py

# 重建所有索引
python scripts/build_index.py
python scripts/build_search_index.py
python scripts/build_similar.py
python scripts/auto_tag.py

# 重译质量最差的 50 段
python scripts/retranslate_worst.py --top 50

# 术语审计
python scripts/term_audit.py
```

---

## 9. 何时刷新本文件

- 新增/移除 top-level 目录
- 新增 scripts 或前端模块
- 改变部署方式或域名
- Service Worker 缓存策略调整
- 主流水线 (`.github/workflows/`) 结构变化

> 用 [GSD](https://github.com/gsd-build/get-shit-done) 的 `/gsd:map-codebase --query refresh` 可重新生成。
