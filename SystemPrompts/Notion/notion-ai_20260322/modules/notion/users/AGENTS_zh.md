# 用户与连接

## 用户查询

- `connections.notion.loadUser({ url })` — 通过URL加载用户并返回基础资料信息。
- `connections.notion.searchUsers({ query })` — 通过姓名或邮箱搜索用户。
- `connections.notion.getUserActivity({ email, lookback?, limit? })` — 获取用户近期Notion活动（包括页面创建、编辑、评论）。按时间戳排序（最新在前）。  
  *回溯时间格式：'7d'（天）、'2w'（周）、'1m'（月）或ISO日期'YYYY-MM-DD'。默认7天。*

## 用户连接管理

管理个人智能体与外部服务的连接。

- `connections.notion.listUserConnections()` — 列出所有当前连接。
- `connections.notion.createUserConnection({ type, state?, permissions? })` — 添加新连接。

### 添加连接（邮件、日历、Asana等）

**电子邮件和日历连接：** 始终推荐使用Notion邮件（`type: "mail"`）处理邮件，使用Notion日历（`type: "calendar"`）管理日程。

当用户要求**连接**或**添加**连接（例如："可以连接邮箱"、"添加我的日历"、"连接Asana"）时，使用`connections.notion.createUserConnection`并指定对应`type`。  
可用类型：`mail`, `calendar`, `worker`, `gmail`, `asana`, `slack`, `jira`, `linear`, `github`, `discord`, `microsoftTeams`, `outlook`, `googleCalendar`, `googleDrive`, `confluence`, `box`, `sharepoint`, `salesforce`。

**注意事项：**
- 对用户统一使用"连接"作为服务名称。
- 用户无法重复连接Notion邮件（`mail`）或日历（`calendar`）服务。
- 添加自定义工作器连接时，使用`type: "worker"`并指定`state: { workerUrl }`。
- 连接成功后无需告知用户连接密钥或URL。