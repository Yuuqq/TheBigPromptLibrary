# 数据源 SQLite 表（Notion 脚本）

当需要通过 `connections.notion.querySql` 查询 Notion 数据源（数据库）的结构化数据，或通过 `connections.notion.updatePage` 更新数据源内页面属性时，使用本文档。

## 1) 单数据源 = 单 SQLite 表

- 每个 Notion 数据源 URL `dataSourceUrl` 对应一个同名的 SQLite 表（精确匹配）。
- SQL 表名必须用双引号包裹：
  ```sql
  SELECT * FROM "dataSourceUrl" LIMIT 10
  ```

## 2) 系统列（始终存在）

所有数据源表包含以下系统列：

- `url` (`TEXT`, unique)：页面 URL（主键标识符）
- `createdTime` (`TEXT`): ISO-8601 时间字符串（页面创建时间）

## 3) 属性列（Notion 属性 → SQL 列映射）

### 列名规则

- 列名按数据源 schema 中的属性名生成（区分大小写）
- SQLite 列名可包含空格/特殊字符，但必须用双引号包裹（除非是简单标识符）
  - 示例：`"Task Name"`, `"Status"`
- 与系统列名冲突的属性名会前缀 `userDefined:`
  - 示例：`"userDefined:url"`

### 哪些属性会转为列？

仅以下类型的属性会被映射为列，其他类型需通过 `connections.notion.queryView` 获取：

| Notion 类型       | SQL 类型 | 值语义                     |
|-------------------|----------|----------------------------|
| **Title / Text**  | `TEXT`   | 平文本（可为空或 `NULL`）  |
| **Number**        | `FLOAT`  | 数值（可为空）             |
| **Checkbox**      | `TEXT`   | `"__YES__"` = true，`"__NO__"` = false |
| **Select**        | `TEXT`   | 配置选项名称（可为空）     |
| **Status**        | `TEXT`   | 配置状态名称（可为空）     |
| **Multi-select**  | `TEXT`   | `Array<string>` 的 JSON 字符串<br>使用 `json_each` 过滤/连接：<br>`... WHERE EXISTS (SELECT 1 FROM json_each(t."Tags") WHERE value = 'Important')` |
| **Person**        | `TEXT`   | 单值：用户 ID 字符串<br>多值：用户 ID 数组<br>用户 ID 格式：`"URL"` |
| **Files**         | `TEXT`   | 文件 ID 数组的 JSON 字符串 |
| **Relation**      | `TEXT`   | 关联页面 URL 数组的 JSON 字符串<br>单值：单个 URL<br>多值：URL 数组<br>推荐使用 `json_each` 连接（优于直接关联列） |
| **Created time**  | `TEXT`   | ISO-8601 时间字符串（非空） |
| **Date**          | 3 列扩展：<br>`"date:<属性名>:start"`（日期时间字符串）<br>`"date:<属性名>:end"`（日期时间字符串，单日期时为 `NULL`）<br>`"date:<属性名>:is_datetime"`（整型：1=时间，0=日期，默认 0） |
| **Auto-increment ID** | `INTEGER` | 数值（可为空）             |
| **Created by**    | `TEXT`   | 用户 URL 字符串（只读）     |
| **Place / Location** | 5 列扩展：<br>`"place:<属性名>:address"`（地址）<br>`"place:<属性名>:name"`（可选名称）<br>`"place:<属性名>:latitude"`（纬度）<br>`"place:<属性名>:longitude"`（经度）<br>`"place:<属性名>:google_place_id"`（可选 Google Place ID） |

## 4) 查询数据源

### SQL 查询 (`connections.notion.querySql`)

- 可跨表查询/关联
- 必须包含 `url` 列（优先）
- 所有含空格/特殊字符的列名和表名必须用双引号包裹

示例 1：基础过滤
```typescript
const result = await connections.notion.querySql({
  dataSourceUrls: ["dataSourceUrl"],
  query: `
    SELECT url, "Status", "Owner"
    FROM "dataSourceUrl"
    WHERE "Status" = ?
  `,
  params: ["In progress"],
});
```

示例 2：通过关联列关联表（关联列存储 URL 数组）
```typescript
const result = await connections.notion.querySql({
  dataSourceUrls: ["okrs", "teams"],
  query: `
    SELECT o.url, o."Objective", t."Team Name"
    FROM "okrs" o
    JOIN "teams" t
      ON t.url IN (SELECT value FROM json_each(o."Team"))
  `,
});
```

### 视图查询 (`connections.notion.queryView`)
用于获取视图显示的原始数据（无需自定义 SQL）
```typescript
const result = await connections.notion.queryView({ viewUrl: "dataSourceUrl" });
```

## 5) 更新数据源页面属性

使用 `connections.notion.updatePage` 通过 `propertyUpdates` 对象更新属性

规则：
- 必须使用数据源 schema 中的属性名
- 清空值设为 `null`
- 禁止修改只读字段（如 `url` / `createdTime`）或计算属性

示例 1：常规更新
```typescript
await connections.notion.updatePage({
  url: "dataSourceUrl",
  propertyUpdates: {
    Title: "New title",
    Status: "In progress",
    "Is due": true,
    Points: 5,
    Tags: ["Important", "Customer"],
  },
});
```

示例 2：日期属性更新
```typescript
await connections.notion.updatePage({
  url: "okrs",
  propertyUpdates: {
    "date:Due Date:start": "2025-01-15",
    "date:Due Date:end": null,
    "date:Due Date:is_datetime": 0,
  },
});
```