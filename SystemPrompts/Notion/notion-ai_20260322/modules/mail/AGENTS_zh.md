# 邮件模块

- 当需要邮件工具时使用。
- 在 `index.ts` 中初始化工具输入/输出。直接调用模块上的函数（例如 `searchEmails`、`viewThreadContent`、`updateStatus`）。
- 权限配置位于 `integration.ts`。
- 触发载荷位于 `triggers.ts`。
- 请阅读 `skills/mail-guidelines.md`，以获取关于邮箱地址规则、草稿工具选择和邮件最佳实践的详细说明。