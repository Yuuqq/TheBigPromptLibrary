# Slack模块

- 当需要Slack搜索、消息读取或消息操作时使用。
- 当Slack消息包含文件URL（在`files`中）时，对每个需要处理的文件调用`connections.slack.viewFileUrl({ url })`。
  - 使用返回的`fileUrl`嵌入到Notion（例如`!\[image.png\](file://...)`）。
  - 不要直接嵌入原始Slack文件URL。
- 输入输出位于`index.ts`。
- 权限配置位于`integration.ts`。
- 触发器负载位于`triggers.ts`。