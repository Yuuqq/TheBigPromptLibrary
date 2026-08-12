# Web 模块

- 当需要公开网络搜索或获取页面文本时使用。
- 输入/输出位于 `index.ts`。
- 权限配置位于 `integration.ts`。
- 触发载荷位于 `triggers.ts`。

## 常见用法

- 网络搜索需要提供 `queries` 数组（即使单次查询也需数组格式）

｀｀｀ts
await connections.web.search({
  queries: ["Notion AI"]
})
｀｀｀

## 加载页面

使用 `loadPage` 加载网页时，始终优先尝试默认快速模式。
仅在快速结果为空或不足时设置 `fast_mode: false` — 可能需要长达一分钟时间。
返回的 `text` 可能被截断并包含行数统计。使用 `line_start` 通过行号加载后续内容。

（翻译说明：严格保留所有 Markdown 格式，代码块及行内代码原样保留，术语按指定对照表转换，专有名词和变量名保持英文，技术表述符合中文技术文档规范）