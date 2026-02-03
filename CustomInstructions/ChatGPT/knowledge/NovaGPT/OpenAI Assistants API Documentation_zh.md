# Assistants API

[**Assistants API Beta**](https://platform.openai.com/docs/assistants/overview/agents)

Assistants API 允许您在自己的应用程序中构建 AI 助手。Assistant 具有指令，可以利用模型、工具和知识来响应用户查询。Assistants API 目前支持三种类型的[工具](https://platform.openai.com/docs/assistants/tools)：Code Interpreter、Retrieval 和 Function calling。未来，我们计划发布更多 OpenAI 构建的工具，并允许您在我们的平台上提供自己的工具。

通过 [Assistants playground](https://platform.openai.com/playground?mode=assistant) 探索 Assistants API 的功能，或按照本指南中概述的步骤构建分步集成。Assistants API 的典型集成包括：

1. **创建 Assistant：** 为您的 [Assistant](https://platform.openai.com/docs/api-reference/assistants/createAssistant) 定义自定义指令并选择模型。启用 Code Interpreter、Retrieval 和 Function calling 等工具。
2. **创建 Thread：** 当用户开始对话时，启动一个 [Thread](https://platform.openai.com/docs/api-reference/threads)。
3. **添加 Messages：** 当用户提问时，在 Thread 中添加 [Messages](https://platform.openai.com/docs/api-reference/messages)。
4. **运行 Assistant：** 通过在 Thread 上[运行](https://platform.openai.com/docs/api-reference/runs) Assistant 来触发响应，自动调用相关工具。

Assistants API 处于 **beta** 阶段。我们欢迎您在我们的 [Developer Forum](https://community.openai.com/) 中提供反馈！

本入门指南详细介绍了使用 [Code Interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter) 创建和运行 Assistant 的关键步骤。

### 步骤 1：创建 Assistant

[**创建 Assistant**](https://platform.openai.com/docs/assistants/overview/step-1-create-an-assistant)

使用以下参数配置 Assistant 以响应 Messages：

- **Instructions：** 定义 Assistant 和模型应如何行为或响应。
- **Model：** 从 GPT-3.5 或 GPT-4 模型中选择，包括微调模型。Retrieval 工具需要 `gpt-3.5-turbo-1106` 和 `gpt-4-1106-preview` 模型。
- **Tools：** API 支持 OpenAI 构建和托管的工具，如 Code Interpreter 和 Retrieval。
- **Functions：** 定义自定义函数签名，类似于 [function calling](https://platform.openai.com/docs/guides/function-calling) 功能。

示例：创建一个启用 Code Interpreter 的个人数学辅导 Assistant：

API 调用的 Beta HTTP 头：

```
OpenAI-Beta: assistants=v1
```

Python 示例：

```python
assistant = client.beta.assistants.create(     name="Math Tutor",     instructions="You are a personal math tutor. Write and run code to answer math questions.",     tools=[{"type": "code_interpreter"}],     model="gpt-4-1106-preview" )
```

### 步骤 2：创建 Thread

[**创建 Thread**](https://platform.openai.com/docs/assistants/overview/step-2-create-a-thread)

在对话开始时为每个用户创建一个 Thread。通过 Messages 包含用户特定的上下文和文件。

Python 示例：

```python
thread = client.beta.threads.create()
```

Thread 支持无限的 Messages。API 使用截断等技术优化请求以适应最大上下文窗口。

### 步骤 3：向 Thread 添加 Message

[**向 Thread 添加 Message**](https://platform.openai.com/docs/assistants/overview/step-3-add-a-message-to-a-thread)

Messages 包含用户的文本和可选的[文件](https://platform.openai.com/docs/assistants/tools/supported-files)。图像文件支持计划在未来更新中提供。

Python 示例：

```python
message = client.beta.threads.messages.create(     thread_id=thread.id,     role="user",     content="I need to solve the equation `3x + 11 = 14`. Can you help me?" )
```

使用 [list Messages in Thread](https://platform.openai.com/docs/api-reference/messages/listMessages) 查看已添加的 Messages。

### 步骤 4：运行 Assistant

[**运行 Assistant**](https://platform.openai.com/docs/assistants/overview/step-4-run-the-assistant)

创建一个 [Run](https://platform.openai.com/docs/api-reference/runs/createRun) 让 Assistant 处理 Thread 并响应用户查询。Assistant 会添加角色为 `assistant` 的 Messages。

可选：在创建 Run 时传递额外的指令。

Python 示例：

```python
run = client.beta.threads.runs.create(   thread_id=thread.id,   assistant_id=assistant.id,   instructions="Please address the user as Jane Doe. The user has a premium account." )
```

### 步骤 5：显示 Assistant 的响应

检索 Run 的[状态](https://platform.openai.com/docs/assistants/how-it-works/run-lifecycle)以检查其进度，从 `queued` 到 `completed`。

Python 示例：

```python
run = client.beta.threads.runs.retrieve(   thread_id=thread.id,   run_id=run.id )
```

检索并显示 Assistant 添加的 Messages。

Python 示例：

```python
messages = client.beta.threads.messages.list(   thread_id=thread.id )
```

在此 Run 期间，Assistant 向 Thread 添加了两条新 Messages：

|角色|内容|
|---|---|
|`user`|I need to solve the equation `3x + 11 = 14`. Can you help me?|
|`assistant`|Certainly, Jane Doe. To solve the equation `(3x + 11 = 14)` for `(x)`, you'll want to isolate `(x)` on one side of the equation. Here's how you can do that:<br><br>1. Subtract 11 from both sides to get `(3x = 3)`.<br>2. Divide both sides by 3 to solve for `(x)`. Let me calculate the value of `(x)` for you.|
|`assistant`|The solution to the equation `(3x + 11 = 14)` is `(x = 1)`.|

---

探索此 Run 的 [Run Steps](https://platform.openai.com/docs/api-reference/runs/listRunSteps) 以了解 Assistant 的处理过程和工具。

- - -

# Assistants 工作原理 (Beta)

Assistants API 旨在帮助开发者构建能够执行各种任务的强大 AI 助手。

## 概述

- **Beta 状态**：Assistants API 处于 beta 阶段，我们正在积极添加更多功能。请在我们的 Developer Forum 中分享您的反馈！
- **功能**：
1. Assistant 可以使用特定指令调用 OpenAI 的**[模型](https://platform.openai.com/docs/models)**来调整其个性和功能。
2. Assistant 可以**并行访问多个工具**。这些可以是 OpenAI 托管的工具——如 [Code interpreter](https://platform.openai.com/docs/assistants/tools/code-interpreter) 和 [Knowledge retrieval](https://platform.openai.com/docs/assistants/tools/knowledge-retrieval)——或您构建/托管的工具（通过 [Function calling](https://platform.openai.com/docs/assistants/tools/function-calling)）。
3. Assistant 可以访问**持久化 Threads**。Threads 通过存储消息历史记录并在对话对模型上下文长度过长时截断它来简化 AI 应用程序开发。您只需创建一次 Thread，然后在用户回复时简单地向其追加 Messages。
4. Assistant 可以**访问多种格式的[文件](https://platform.openai.com/docs/assistants/tools/supported-files)**——作为创建的一部分或作为 Assistant 和用户之间 Threads 的一部分。使用工具时，Assistant 还可以创建文件（例如图像、电子表格等）并在其创建的 Messages 中引用文件。

## 对象

![[Pasted image 20231113112640.png]]

### Assistants 对象架构图

|对象|表示什么|
|---|---|
|Assistant|使用 OpenAI 模型并调用工具的专用 AI|
|Thread|Assistant 和用户之间的对话会话|
|Message|由 Assistant 或用户创建的消息|
|Run|在 Thread 上调用 Assistant|
|Run Step|Assistant 在 Run 过程中采取的详细步骤|

## 创建 Assistants

我们建议在 Assistants API 中使用 OpenAI 的[最新模型](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo)以获得最佳结果和与工具的最大兼容性。

要开始，创建 Assistant 只需指定要使用的 `model`。但您可以进一步自定义 Assistant 的行为：

1. 使用 `instructions` 参数指导 Assistant 的个性并定义其目标。Instructions 类似于 Chat Completions API 中的系统消息。
2. 使用 `tools` 参数让 Assistant 访问最多 128 个工具。您可以让它访问 OpenAI 托管的工具，如 `code_interpreter` 和 `retrieval`，或通过 `function` 调用调用第三方工具。
3. 使用 `file_ids` 参数让 `code_interpreter` 和 `retrieval` 等工具访问文件。文件使用 `File` [上传端点](https://platform.openai.com/docs/api-reference/files/create)上传，必须将 `purpose` 设置为 `assistants` 才能与此 API 一起使用。

### 示例：创建数据可视化 Assistant

首先，使用 Python SDK 上传文件：

```python
file = client.files.create(
  file=open("speech.py", "rb"),
  purpose='assistants'
)
```

然后，使用上传的文件创建 Assistant：

```python
assistant = client.beta.assistants.create(
  name="Data visualizer",
  description="You are great at creating beautiful data visualizations. You analyze data present in .csv files, understand trends, and come up with data visualizations relevant to those trends. You also share a brief text summary of the trends observed.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)
```

- **注意**：每个 Assistant 最多 20 个文件，每个文件最大 512 MB。总文件存储不超过 100GB。可以通过帮助中心请求增加存储限制。

## 管理 Threads 和 Messages

Threads 和 Messages 促进 Assistant 和用户之间的对话会话。

### 创建带有 Messages 的 Thread

```python
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Create 3 data visualizations based on the trends in this file.",
      "file_ids": [file.id]
    }
  ]
)
```

- **Message 内容**：可以包含文本、图像或文件。目前，用户创建的消息不能包含图像，但未来将支持此功能。

### Message 注释

- **类型**：
    - `file_citation`：引用 Assistant 使用的文件中的引文。
    - `file_path`：引用 Assistant 生成的文件。

### 示例：用注释替换模型生成的子字符串

```python
# 检索消息对象
message = client.beta.threads.messages.retrieve(
  thread_id="...",
  message_id="..."
)

# 提取消息内容
message_content = message.content[0].text
annotations = message_content.annotations
citations = []

# 遍历注释并添加脚注
for index, annotation in enumerate(annotations):
    # 用脚注替换文本
    message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

    # 根据注释属性收集引用
    if (file_citation := getattr(annotation, 'file_citation', None)):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
    elif (file_path := getattr(annotation, 'file_path', None)):
        cited_file = client.files.retrieve(file_path.file_id)
        citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
        # 注意：为简洁起见，上面未实现文件下载功能

# 在向用户显示之前将脚注添加到消息末尾
message_content.value += '\n' + '\n'.join(citations)
```

## Runs 和 Run Steps

### 创建 Run

```python
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)
```

默认情况下，Run 将使用 Assistant 对象中指定的 `model` 和 `tools` 配置，但您可以在创建 Run 时覆盖其中大部分以增加灵活性：

```python
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  model="gpt-4-1106-preview",
  instructions="additional instructions",
  tools=[{"type": "code_interpreter"}, {"type": "retrieval"}]
)
```

注意：与 Assistant 关联的 `file_ids` 在 Run 创建期间无法覆盖。您必须使用 [modify Assistant](https://platform.openai.com/docs/api-reference/assistants/modifyAssistant) 端点来执行此操作。

**Run 生命周期**：包括 queued、in_progress、completed、requires_action、expired、cancelling、cancelled 和 failed 等状态。
![[Pasted image 20231113112420.png]]


|状态|定义|
|---|---|
|`queued`|当 Runs 首次创建或您完成 `required_action` 时，它们会进入 queued 状态。它们应该几乎立即转移到 `in_progress`。|
|`in_progress`|在 in_progress 期间，Assistant 使用模型和工具执行步骤。您可以通过检查 [Run Steps](https://platform.openai.com/docs/api-reference/runs/step-object) 来查看 Run 的进度。|
|`completed`|Run 成功完成！您现在可以查看 Assistant 添加到 Thread 的所有 Messages，以及 Run 采取的所有步骤。您还可以通过向 Thread 添加更多用户 Messages 并创建另一个 Run 来继续对话。|
|`requires_action`|使用 [Function calling](https://platform.openai.com/docs/assistants/tools/function-calling) 工具时，一旦模型确定要调用的函数的名称和参数，Run 将进入 `required_action` 状态。然后您必须运行这些函数并[提交输出](https://platform.openai.com/docs/api-reference/runs/submitToolOutputs)，然后 run 才能继续。如果在 `expires_at` 时间戳之前（大约在创建后 10 分钟）未提供输出，run 将进入 expired 状态。|
|`expired`|当函数调用输出未在 `expires_at` 之前提交且 run 过期时会发生这种情况。此外，如果 runs 执行时间过长并超过 `expires_at` 中规定的时间，我们的系统将使 run 过期。|
|`cancelling`|您可以使用 [Cancel Run](https://platform.openai.com/docs/api-reference/runs/cancelRun) 端点尝试取消 `in_progress` 的 run。取消尝试成功后，Run 的状态会变为 `cancelled`。尝试取消但不保证成功。|
|`cancelled`|Run 已成功取消。|
|`failed`|您可以通过查看 Run 中的 `last_error` 对象来查看失败原因。失败的时间戳将记录在 `failed_at` 下。|

**轮询更新**

为了保持 run 状态的最新，您需要定期[检索 Run](https://platform.openai.com/docs/api-reference/runs/getRun) 对象。您可以在每次检索对象时检查 run 的状态，以确定您的应用程序接下来应该做什么。我们计划在不久的将来添加对流式传输的支持以使这更简单。

**Thread 锁定**

当 Run 处于 `in_progress` 状态且不在终端状态时，Thread 会被锁定。这意味着：

- 无法向 Thread 添加新 Messages。
- 无法在 Thread 上创建新 Runs。

### Run Steps

![[Pasted image 20231113112312.png]]

- **详细信息**：
    - `message_creation`：创建 Messages 的步骤。
    - `tool_calls`：调用工具的步骤。

## 数据访问指南

目前，通过 API 创建的 assistants、threads、messages 和 files 的范围是整个组织。因此，任何拥有组织 API 密钥访问权限的人都可以读取或写入组织中的 assistants、threads、messages 和 files。

我们强烈建议以下数据访问控制：

- _实施授权。_ 在对 assistants、threads、messages 和 files 执行读取或写入操作之前，确保最终用户有权这样做。例如，在您的数据库中存储最终用户有权访问的对象 ID，并在使用 API 获取对象 ID 之前检查它。
- _限制 API 密钥访问。_ 仔细考虑组织中谁应该拥有 API 密钥，并定期审核此列表。API 密钥可以执行各种操作，包括读取和修改敏感信息，如 messages 和 files。
- _创建单独的账户。_ 考虑为不同的应用程序创建单独的账户/组织，以便跨多个应用程序隔离数据。

## 限制

在此 beta 期间，有几个已知的限制我们希望在未来几周和几个月内解决。当我们添加对其他功能的支持时，我们将在此页面上发布更改日志。

- 支持流式输出（包括 Messages 和 Run Steps）。
- 支持通知以共享对象状态更新，无需轮询。
- 支持 DALL·E 作为工具。
- 支持用户消息创建时包含图像。


# 工具 (Beta)

让 Assistants 访问 OpenAI 托管的工具，如 Code Interpreter 和 Knowledge Retrieval，或使用 Function calling 构建您自己的工具。使用 OpenAI 托管的工具需要额外付费。访问我们的帮助中心文章了解这些工具的定价方式。

Assistants API 处于 beta 阶段，我们正在积极添加更多功能。请在我们的 Developer Forum 中分享您的反馈！

## Code Interpreter

Code Interpreter 允许 Assistants API 在沙盒执行环境中编写和运行 Python 代码。此工具可以处理具有多种数据和格式的文件，并生成包含数据和图形图像的文件。Code Interpreter 允许您的 Assistant 迭代运行代码以解决具有挑战性的代码和数学问题。当您的 Assistant 编写的代码运行失败时，它可以通过尝试运行不同的代码来迭代此代码，直到代码执行成功。

### 启用 Code Interpreter

要启用 Code Interpreter，请在 Assistant 对象的 tools 参数中传递 `code_interpreter`：

```python
assistant = client.beta.assistants.create(
  instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}]
)
```

### 向 Code Interpreter 传递文件

Code Interpreter 可以在 Assistant 和 Thread 级别解析文件中的数据：

- **Assistant 级别**：
```python
# 上传带有 "assistants" 目的的文件
file = client.files.create(
  file=open("speech.py", "rb"),
  purpose='assistants'
)

# 使用文件 ID 创建 assistant
assistant = client.beta.assistants.create(
  instructions="You are a personal math tutor. When asked a math question, write and run code to answer the question.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)
```

- **Thread 级别**：

```python
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?",
      "file_ids": [file.id]
    }
  ]
)
```

### 读取 Code Interpreter 生成的图像和文件

- Code Interpreter 输出图像和数据文件。

```python
{
    "id": "msg_OHGpsFRGFYmz69MM1u8KYCwf",
    "object": "thread.message",
    "created_at": 1698964262,
    "thread_id": "thread_uqorHcTs46BZhYMyPn6Mg5gW",
    "role": "assistant",
    "content": [
    {
      "type": "image_file",
      "image_file": {
        "file_id": "file-WsgZPYWAauPuW4uvcgNUGcb"
      }
    }
  ]
  # ...
}
```

- 使用 Files API 检索生成的文件内容：

```python
content = client.files.retrieve_content(file.id)
```

当 Code Interpreter 引用文件路径（例如"Download this csv file"）时，文件路径列为注释。您可以将这些注释转换为下载文件的链接：

```json
{
  "id": "msg_3jyIh3DgunZSNMCOORflDyih",
  "object": "thread.message",
  "created_at": 1699073585,
  "thread_id": "thread_ZRvNTPOoYVGssUZr3G8cRRzE",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": {
        "value": "The rows of the CSV file have been shuffled and saved to a new CSV file. You can download the shuffled CSV file from the following link:\n\n[Download Shuffled CSV File](sandbox:/mnt/data/shuffled_file.csv)",
        "annotations": [
          {
            "type": "file_path",
            "text": "sandbox:/mnt/data/shuffled_file.csv",
            "start_index": 167,
            "end_index": 202,
            "file_path": {
              "file_id": "file-oSgJAzAnnQkVB3u7yCoE9CBe"
            }
          }
          ...
```

### Code Interpreter 的输入和输出日志

通过列出 Run 的步骤来检查代码输入和输出日志：

```python
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)
```

```python
{
  "object": "list",
  "data": [
    {
      "id": "step_DQfPq3JPu8hRKW0ctAraWC9s",
      "object": "thread.run.step",
      "type": "tool_calls",
      "run_id": "run_kme4a442kme4a442",
      "thread_id": "thread_34p0sfdas0823smfv",
      "status": "completed",
      "step_details": {
        "type": "tool_calls",
        "tool_calls": [
          {
            "type": "code",
            "code": {
              "input": "# Calculating 2 + 2\nresult = 2 + 2\nresult",
              "outputs": [
                {
                  "type": "logs",
                  "logs": "4"
                }
                        ...
 }
```

## Knowledge Retrieval

Retrieval 使用外部知识增强 Assistant，例如专有产品信息或用户提供的文档。

### 启用 Retrieval

通过在 tools 参数中传递 `retrieval` 来启用 Retrieval：

```python
assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}]
)
```

### 为 Retrieval 上传文件

文件可以在 Assistant 和 Thread 级别上传和传递：

```python
# 上传带有 "assistants" 目的的文件
file = client.files.create(
  file=open("knowledge.pdf", "rb"),
  purpose='assistants'
)

# 将文件添加到 assistant
assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "retrieval"}],
  file_ids=[file.id]
)

# Thread 级别
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I can't find in the PDF manual how to turn off this device.",
  file_ids=[file.id]
)
```

### 删除文件

从 assistant 分离文件以将其从检索索引中删除：

```python
file_deletion_status = client.beta.assistants.files.delete(
  assistant_id=assistant.id,
  file_id=file.id
)
```

### 文件引用

使用 annotations 字段将 Message 中的文件路径转换为相应的文件下载。

```python
{
    "id": "msg_3jyIh3DgunZSNMCOORflDyih",
    "object": "thread.message",
    "created_at": 1699073585,
    "thread_id": "thread_ZRvNTPOoYVGssUZr3G8cRRzE",
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": {
          "value": "The rows of the CSV file have been shuffled and saved to a new CSV file. You can download the shuffled CSV file from the following link:\n\n[Download Shuffled CSV File](sandbox:/mnt/data/shuffled_file.csv)",
          "annotations": [
            {
              "type": "file_path",
              "text": "sandbox:/mnt/data/shuffled_file.csv",
              "start_index": 167,
              "end_index": 202,
              "file_path": {
                "file_id": "file-oSgJAzAnnQkVB3u7yCoE9CBe"
              }
            }
          ]
        }
      }
    ],
    "file_ids": [
      "file-oSgJAzAnnQkVB3u7yCoE9CBe"
    ],
        ...
  },
```

## Function Calling

与 Chat Completions API 类似，Assistants API 支持 function calling。

### 定义 Functions

在创建 Assistant 时定义 functions：

```python
assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4-1106-preview",
  tools=[{
      "type": "function",
    "function": {
      "name": "getCurrentWeather",
      "description": "Get the weather in location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
          "unit": {"type": "string", "enum": ["c", "f"]}
        },
        "required": ["location"]
      }
    }
  }, {
    "type": "function",
    "function": {
      "name": "getNickname",
      "description": "Get the nickname of a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        },
        "required": ["location"]
      }
    }
  }]
)
```

### 读取 Assistant 调用的 Functions

检查 Run 的状态以识别所需的操作：

```python
{
  "id": "run_3HV7rrQsagiqZmYynKwEdcxS",
  "object": "thread.run",
  "assistant_id": "asst_rEEOF3OGMan2ChvEALwTQakP",
  "thread_id": "thread_dXgWKGf8Cb7md8p0wKiMDGKc",
  "status": "requires_action",
  "required_action": {
    "type": "submit_tool_outputs",
    "submit_tool_outputs": {
      "tool_calls": [
        {
          "id": "call_Vt5AqcWr8QsRTNGv4cDIpsmA",
          "type": "function",
          "function": {
            "name": "getCurrentWeather",
            "arguments": "{\"location\":\"San Francisco\"}"
          }
        },
        {
          "id": "call_45y0df8230430n34f8saa",
          "type": "function",
          "function": {
            "name": "getNickname",
            "arguments": "{\"location\":\"Los Angeles\"}"
          }
        }
      ]
    }
  },
...
```

### 提交 Functions 输出

提交工具输出以完成 Run：

```python
run = client.beta.threads.runs.submit_tool_outputs(
  thread_id=thread.id,
  run_id=run.id,
  tool_outputs=[
      {
        "tool_call_id": call_ids[0],
        "output": "22C",
      },
      {
        "tool_call_id": call_ids[1],
        "output": "LA",
      },
    ]
)
```

## 支持的文件

|文件格式|MIME 类型|Code Interpreter|Retrieval|
|---|---|---|---|
|`.c`|text/x-c|||
|`.cpp`|text/x-c++|||
|`.csv`|application/csv||✓|
|`.docx`|application/vnd.openxmlformats-officedocument.wordprocessingml.document||✓|
|...|...|...|...|
