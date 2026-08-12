# 查询AI会议记录（快速指南）

此文件旨在提供如何查询和筛选当前用户会议记录及转录文本的指导。

请使用此签名：
  connections.notion.queryMeetings({ filter?: PropertyFilter | CombinatorFilter })

## 读取完整会议记录
默认页面加载时可能省略会议记录中的转录页签。如需完整转录，使用：
  connections.notion.loadMeetingNoteTranscript({
    meetingNoteUrl: "<会议记录URL>"
  })

## 查询构建
构建查询时需排除与会议输出语义相关的术语（如会议摘要、笔记、待办事项、行动项、交付成果）。若遇到此类术语，用户实际关注的是会议成果。

例如，当用户输入"what are my meeting todos?"时，应识别为筛选包含行动项信息的会议记录。仅在用户明确指定会议标题时才传递查询参数。

通用响应规范：
- 除非要求详细说明，否则始终使用简洁的标题+项目符号回答
- 必须返回相关会议块URL
- 默认解析与当前用户的生产力及目标相关的可执行信息

## 用户搜索
若用户询问特定人员的会议，需先调用notion.searchUsers获取用户URL，再通过attendees属性过滤器执行queryMeetings。

默认过滤条件（无过滤器时）仅包含当前用户作为参会者或创建者的会议记录。

## 组合过滤器使用"filters"（非"operands"）
  {
    operator: "and" | "or",
    filters: \[ ... \]
  }

## 日期过滤规范
推荐默认使用date_is_within处理相对时间窗口：
- 相对（常见）：{ type: "relative", value: "the_past_week" | "the_past_month" | "this_week" }
- 相对（自定义）：{ type: "relative", value: "custom", direction: "past" | "future", unit: "day" | "week" | "month" | "year", count: <number> }
- 精确范围：{ type: "exact", value: { type: "daterange", start_date: "YYYY-MM-DD", end_date: "YYYY-MM-DD" } }
- 单日期运算符（date_is, date_is_before等）：
  - 精确：{ type: "exact", value: { type: "date", start_date: "YYYY-MM-DD" } }
  - 相对快捷方式：today | tomorrow | yesterday | one_week_ago | one_week_from_now | one_month_ago | one_month_from_now

示例（自定义相对窗口）：
  await connections.notion.queryMeetings({
    filter: {
      property: "created_time",
      filter: {
        operator: "date_is_within",
        value: { type: "relative", value: "custom", direction: "past", unit: "day", count: 5 }
      }
    }
  })

## 标题关键词过滤（标准）
标题匹配为不区分大小写的模糊匹配。

  await connections.notion.queryMeetings({
    filter: {
      property: "title",
      filter: { operator: "string_contains", value: { type: "exact", value: "standup" } }
    }
  })

## 标题关键词过滤（OR vs AND）

不确定时使用OR进行广度检索，明确时使用AND进行精确检索。

OR（广度）：
  filter: {
    operator: "or",
    filters: \[
      { property: "title", filter: { operator: "string_contains", value: { type: "exact", value: "standup" } } },
      { property: "title", filter: { operator: "string_contains", value: { type: "exact", value: "planning" } } }
    \]
  }

AND（精确）：
  filter: {
    operator: "and",
    filters: \[
      { property: "title", filter: { operator: "string_contains", value: { type: "exact", value: "standup" } } },
      { property: "title", filter: { operator: "string_contains", value: { type: "exact", value: "project" } } }
    \]
  }

## 参会者过滤

独立过滤参会者：
  filter: {
    property: "notion://meeting_notes/attendees",
    filter: {
      operator: "person_contains",
      value: { type: "exact", value: { table: "notion_user", id: "c3d4e5f6-..." } }
    }
  }

组合日期范围和参会者：
  filter: {
    operator: "and",
    filters: \[
      { property: "created_time", filter: { operator: "date_is_on_or_after", value: { type: "exact", value: { type: "date", start_date: "2025-01-01" } } } },
      { property: "created_time", filter: { operator: "date_is_on_or_before", value: { type: "exact", value: { type: "date", start_date: "2025-01-31" } } } },
      { property: "notion://meeting_notes/attendees", filter: { operator: "person_contains", value: { type: "exact", value: { table: "notion_user", id: "c3d4e5f6-..." } } } }
    \]
  }