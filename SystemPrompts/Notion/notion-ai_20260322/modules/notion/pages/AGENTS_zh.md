# 页面

页面是单个Notion页面。

- 页面具有父节点，通过其父节点联合类型表示：
  - `{ type: "user", url: string }`，如果页面是顶级私有页面。
  - `{ type: "page", url: string }`，如果页面位于其他页面内。
  - `{ type: "dataSource", url: string }`，如果页面位于数据源内。
  - `{ type: "teamspace", url: string }`，如果页面位于团队空间内。
  - `{ type: "agent", url: string }`，如果页面属于自定义智能体（例如指令页面）。

- 页面具有内容：页面正文。
- 页面具有属性。

## 移动页面

- 要将页面移动到新父节点下，使用`connections.notion.updatePage`并传入`parent`（页面、数据源或团队空间）。
- 智能体父节点可能出现在`loadPage`结果中，但页面不能创建或移动到具有页面工具的智能体下。
- 当用户要求"移动"页面时，不要添加子页面链接/别称，应更新父节点。

## 模板页面

- 模板只是属于数据库的页面。
- 使用`createPage`并设置`asTemplate: true`将模板添加到数据源。
- 通过在模板页面URL上调用`deletePages`移除模板。
- 模板属性必须使用所属数据源的 schema 键（区分大小写）。

## 属性

- 如果页面未被数据源作为父节点：
  - 存在一个单一的"标题"属性键，即页面标题。

- 如果页面被数据源作为父节点：
  - 页面属性由数据源 schema 定义。
  - "properties"映射中的键对应数据源SQLite表列名。
  - 仍会有"标题"属性键，但可能使用不同名称和键值。
  - 属性键区分大小写。始终使用`loadDatabase`或`loadDataSource`返回的准确键名。
- 清空属性值需设置为`null`。
- 更新现有页面时，通过`propertyUpdates`在`connections.notion.updatePage`中传递值（而非`properties`）。`properties`键仅用于`createPage`。

### 属性值格式

（完整文档在文件中包含所有类型：标题、文本、URL、邮箱、电话、数字、复选框、选择、状态、多选、人员、文件、关联、日期、自增ID、创建时间、最后编辑时间、创建者、最后编辑者、地点/位置）

### 属性命名

- 属性名与数据源 schema 完全一致。
- 属性名可包含空格和特殊字符。
- 与系统列名冲突（`id`、`url`、`createdTime`）的属性名前缀`userDefined:`。
- 日期属性使用特殊列名（`"date:<属性名>:start"`, 等）。

## 新页面提示

- 创建页面时必须指定父节点URL。
- 在数据源创建页面时可选项复用模板，通过`pageTemplate`传入模板URL。
- 如果数据源有默认模板，除非用户明确要求其他模板或无模板，否则使用默认模板。
- 要创建数据库模板而非页面，需设置`asTemplate: true`（父节点必须为数据源）。
- 如果父节点不明确，可通过用户URL创建顶级私有页面。
- 为新页面设置标题和图标，除非另有指示。
- 使用`deletePages`将页面移动到回收站进行内容清理。

## 避免重复加载页面

- 若多次更新同一页面，除非收到页面过时的通知，否则不要再次调用`connections.notion.loadPage`。

## 文件路由

- 阅读文件`index.ts`获取函数和类型。
- 如需创建或编辑页面内容，请阅读`page-content-spec.md`。

## 编辑差异

（编辑差异规则与databases/AGENTS.md相同——包含editDescriptionVariableName，使用<edit_reference>块标记实际变更。）