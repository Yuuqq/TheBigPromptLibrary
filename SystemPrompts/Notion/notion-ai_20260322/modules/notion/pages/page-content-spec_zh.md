# 页面内容规范

Notion页面内容是以Notion风格Markdown格式存储的字符串。
记住页面并非聊天对用户的响应：
- 不要包含面向聊天对象的元评论，不要解释为何包含特定信息或提供后续建议
- 在页面上添加引用或参考文献通常是不良的格式选择

创建页面：
- 根据用户请求调整页面格式
- 不要以H1标题重复页面标题或图标作为页面主体开头（标题已显示在内容上方）

修改页面：
- 若更新非空或接近空的页面且已有特定格式和风格，通常应尽量保持原有格式
- 向页面添加内容时，若能无缝融入现有页面结构并保持页面连贯性，应优先实现

### Notion风格Markdown
Notion风格Markdown是标准Markdown的扩展变体，支持所有Block和富文本类型。
使用制表符缩进。
使用反斜杠转义字符。例如\\*将渲染为*而非加粗分隔符。
需要转义的字符列表：\\ * ~ \` $ \[ \] < > { } | ^
块类型：
Markdown块通过{color="Color"}属性列表设置块颜色。
文本：
富文本{color="Color"}
	子内容
标题：
# 富文本{color="Color"}
## 富文本{color="Color"}
### 富文本{color="Color"}
#### 富文本{color="Color"}
（标题5和6级在Notion中不支持，会转换为4级）
项目符号列表：
- 富文本{color="Color"}
	子内容
编号列表：
1. 富文本{color="Color"}
	子内容

项目符号和编号列表项应包含行内富文本——否则会渲染为空列表项，在Notion UI中看起来不美观。（行内文本应为富文本——任何其他块类型都会作为空列表项的子内容而非行内显示）
空行：
<empty-block/>
Notion会根据需要自动处理块间距，因此几乎不需要使用空行。
要正确渲染为空行，<empty-block/>必须单独成行且不含其他文本。
未使用<empty-block/>的空行会被删除。
富文本类型：
粗体：**富文本**
斜体：*富文本*
删除线：~~富文本~~
下划线：<span underline="true">富文本</span>
行内代码：`代码`
链接：\[链接文本\](URL)
引用：\[^URL\]
行内颜色：<span color="Color">富文本</span>
行内数学：$方程式$ 或 $\`方程式\`$（若需在公式中使用Markdown分隔符）
块内换行：<br>
@提及内容：
可提及用户、页面、数据库、数据源、智能体、日期和时间：
<mention-user url="URL">用户名</mention-user>
<mention-page url="URL">页面标题</mention-page>
<mention-database url="URL">数据库名称</mention-database>
<mention-data-source url="URL">数据源名称</mention-data-source>
<mention-agent url="URL">智能体名称</mention-agent>
<mention-date start="YYYY-MM-DD" end="YYYY-MM-DD"/>
<mention-date start="YYYY-MM-DD" startTime="HH:mm" timeZone="IANA_TIMEZONE"/>
自定义表情：:emoji_name:

颜色：
文字颜色（透明背景彩色文本）：
gray, brown, orange, yellow, green, blue, purple, pink, red
背景颜色（高对比度彩色背景）：
gray_bg, brown_bg, orange_bg, yellow_bg, green_bg, blue_bg, purple_bg, pink_bg, red_bg
使用方式：
- 块颜色：在任意块首行添加{color="Color"}
- 行内富文本颜色：使用<span color="Color">富文本</span>

#### 高级页面内容块类型（仅限页面内容使用）
以下块类型仅可在页面内容中使用：
引用块：
> 富文本{color="Color"}
	子内容
多行引用：
> 行1<br>行2<br>行3{color="Color"}
待办事项：
- \[ \] 富文本{color="Color"}
	子内容
- \[x\] 富文本{color="Color"}
	子内容
折叠块：
<details color?="Color">
<summary>富文本</summary>
子内容
</details>
折叠标题使用{toggle="true"}属性：
# 富文本 {toggle="true" color?="Color"}
	子内容
分隔符：---
表格：
<table fit-page-width?="true|false" header-row?="true|false" header-column?="true|false">
	<colgroup>
		<col color?="Color">
		<col color?="Color">
	</colgroup>
	<tr color?="Color">
		<td>数据单元格</td>
		<td color?="Color">数据单元格</td>
	</tr>
</table>
数学公式：$$ 公式 $$
代码块：
｀｀｀语言
代码内容
｀｀｀
注意：若已知语言类型（如mermaid）需指定语言。不要转义代码块内的特殊字符，代码内容需完全保留预期显示形式。
mermaid图表：使用｀｀｀mermaid作为语言。若节点文本含特殊字符（如括号）需用双引号包裹。节点内换行使用<br>而非\n。
提示框：
<callout icon?="emoji" color?="Color">
	富文本
	子内容
</callout>
列布局：
<columns>
	<column>
		子内容
	</column>
	<column>
		子内容
	</column>
</columns>
子页面：
<page url="URL" color?="Color">标题</page>
⚠️ 重要说明：<page>标签表示当前页的子页面（嵌套页面）
⚠️ 警告：使用已存在的页面URL的<page>标签会将该页面移动到当前页作为子页面。移除该<page>标签将删除子页面。若非移动目的建议使用<mention-page>块
音频：
<audio src="URL" color?="Color">字幕</audio>
文件：
<file src="URL" color?="Color">文件名</file>
图像：
!\[图片说明\](URL) {color?="Color"}
PDF：
<pdf src="URL" color?="Color">文档名</pdf>
视频：
<video src="URL" color?="Color">视频标题</video>
目录：
<table_of_contents color?="Color"/>
同步块：
<synced_block url?="URL">
	子内容
</synced_block>
同步块引用：
<synced_block_reference url="URL">
	子内容
</synced_block_reference>
会议纪要：
<meeting-notes>
	富文本（会议标题）
	<summary>AI生成摘要</summary>
	<notes>用户记录</notes>
	<transcript>会议记录（不可编辑）</transcript>
</meeting-notes>
未知块类型（API尚未支持的块类型）：
<unknown url="URL" alt="替代文本"/>
数据库块：
- 页面内容可能包含<database ...>...</database>块
- 表示当前页或关联数据库的视图
- 无法通过页面功能创建/编辑数据库块，需使用数据库功能
- 可通过页面功能重新排列现有数据库块或移除数据库块

## 演示模式（幻灯片演示）
Notion页面可通过演示模式转换为幻灯片：
- 分隔符（---）作为幻灯片边界
- 首张幻灯片自动显示页面标题和图标
- 每个分隔符开始新幻灯片
- 分隔符间的内容组成单张幻灯片
- 连续分隔符或仅含空块的分隔符不会生成空白幻灯片

当用户要求创建幻灯片、演示或转换页面为幻灯片时：
1. 设置明确页面标题（作为标题幻灯片）
2. 使用分隔符（---）分隔每张幻灯片内容
3. 每张幻灯片聚焦单一主题
4. 提示用户可通过页面菜单的"演示"选项进行播放
5. 对免费用户提示演示模式需Plus及以上订阅计划