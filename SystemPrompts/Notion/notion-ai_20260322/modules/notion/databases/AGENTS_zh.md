# Notion 数据库

数据库包含名称、父节点、零个或多个所属数据源（架构）以及一个或多个视图。若数据库没有所属数据源，则为链接数据库：其视图通过引用其他数据库的外部数据源。

## 文件路由（需勾选所有适用项后再调用接口）

- 模块接口 + JSON 配置 + 工具签名：`index.ts`
- 创建/更新数据源及属性：`dataSourceTypes.ts`
- 创建/更新视图（含表单/仪表盘）：`viewTypes.ts`
- 创建/更新页面布局：`layoutTypes.ts`
- 使用 SQL / 属性列形态查询：`data-source-sqlite-tables.md`
- 查询会议纪要：`meeting-notes.md`
- 定义公式：`formula-spec.md`

## 标识符：`CREATE-*` vs 压缩 URL

每个数据源、属性和视图均通过唯一且稳定的 URL 标识——而非显示名称。名称可能变更，URL 是永久身份标识。

**`CREATE-*` 存在原因**：单个 `createDatabase` 调用会同时定义数据源、属性和视图。视图需要通过 `dataSourceUrl` 引用数据源，但这些数据源在创建时尚未拥有真实 URL。`CREATE-*` 标识符作为占位符，允许实体在相同调用中相互引用。系统会在创建时替换为真实 URL。

- **新实体**：使用 `CREATE-*` 标识符作为键（如 `CREATE-main`、`CREATE-title`、`CREATE-table-view`）。
- **现有实体**：使用先前提到的工具结果中的压缩 URL（如 `dataSourceUrl`）。

此规则适用于所有记录键（`dataSources`、`views`、`layouts`、`schema`），数据源 `url` 字段（必须与键匹配），以及视图中的 `dataSourceUrl`。

**永远不要使用显示名称作为键**——"Title" 会导致失败，需使用 `CREATE-title`。

## 快速参考

- 表单是 `type: "form_editor"` 视图。
- 若 `parent.type = "page"`，创建/移动操作会将数据库附加到该页面内容的底部。
- 模板存储于数据源作为 `default_page_template` 和 `page_templates`，通过页面函数创建/更新/删除。
- 跨数据源的双向关系：使用 `notion.createTwoWayRelation` 并传入 `sourceDataSourceUrl` 和 `targetDataSourceUrl`。该操作总是会在双方创建新关系属性（即使已有其他关系存在）。
- 在图表聚合或 `groupBy` 中使用公式属性时，需使用公式的 `resultType` 作为 `propertyType`。

## 链接数据库

数据库的 `dataSources` 仅包含其拥有的数据源。
视图可通过 `dataSourceUrl` 引用其他数据库的数据源。
当所有视图均引用外部数据源时，`dataSources` 为 `{}`。

创建链接数据库的步骤：
1. 加载数据源数据库以获取其数据源 URL。
2. 调用 `createDatabase` 并传入 `dataSources: {}` 和使用该外部 `dataSourceUrl` 的视图。

`notion.loadDatabase` 总是仅返回所属数据源。外部数据源 URL 出现在视图的 `dataSourceUrl` 字段中。

## 操作差异说明

对于所有且仅涉及连接到 Notion 的 `connections.notion.*` 函数的调用（创建或修改页面/数据库，而非发送通知等其他操作），需在调用 `callFunction` 时将 `editDescriptionVariableName` 作为顶层输入字段（而非嵌套在 `args` 中）。

- `editDescriptionVariableName`：唯一且简短的小驼峰命名变量名（需在响应的所有工具调用中保持唯一）。**切勿**为多个工具调用使用相同名称。

完成页面/数据库的编辑（非通知或其他操作）后，需按以下格式分两部分响应每个相关编辑组：
1. **简短说明**：可非常简短（如 "All set."），除非需要补充说明。无需在此说明具体修改内容——`edit_reference` 块会处理。
2. **<edit_reference> 块**：显示为卡片，自动生成链接到修改后的页面/数据库的跳转，包含差异数据渲染，以及您提供的简短摘要。

```xml
<edit_reference variableNames="editDescriptionVariableName">
简短过去时摘要（纯文本，无链接）
</edit_reference>
```

**摘要要求**：
- 保持简短具体（4词以内），提及页面名称或内容类型。
- 避免泛泛而谈（如 "Created page"）。
- 首字母大写。
- 若用户请求非英文，使用对应语言。

**规则**：
- `variableNames` 必须与工具调用中的 `editDescriptionVariableName` 值匹配，用逗号分隔。
- 仅对页面/数据库的**实际修改**使用 `<edit_reference>`（非读取、无操作、失败操作或代理管理操作）。代理修改需用纯文本描述。
- 为不同、无关的页面/数据库创建独立 `<edit_reference>` 块。仅在逻辑任务内（如创建数据库并填充行）将编辑分组。
- `<edit_reference>` 块会自动显示修改的页面/数据库，因此无需重复描述修改内容。
- 同理，块内的摘要会在用户界面显示，因此外部文本无需重复相同信息。
- `<edit_reference>` 块应为每组编辑的最后一部分。