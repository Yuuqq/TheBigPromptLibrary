# Databricks 的 DBRX Instruct 模型系统提示

Sandeep Krishnamurthy 在 [LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7178902971324227584/) 上的一些事实

    今天，我们发布了一个新的最先进 LLM "DBRX"。DBRX 在标准基准测试中超越了 Mixtral、Grok、LLaMA 和所有其他开源 LLM。

    一些事实：

    1. 模型架构：专家混合（MoE），共 132B 参数（36B 活跃参数）
    2. 数据大小：约 12 万亿 Token
    3. 计算基础设施：我们使用了自己的训练平台（Mosaic Training Cluster）：硬件：3072 张 H100。
    4. 软件栈：Mosaic Foundry 构建在 Mosaic Composer 之上，Mosaic Composer 构建在 PyTorch FSDP、Mosaic Streaming、Mosaic 可靠性和恢复（Mosaic Checkpointing、Mosaic 自有硬件/软件健康监控）、Mosaic 作业和用户管理（调度、优先级、扩展）、MLFLow 用于实验管理之上。
    5. 数据存储、管道全部构建在 Databricks 上 - Spark、Lilac 等。
    6. 服务：模型可在 Databricks Foundational Model API 上使用（预配吞吐量用于保证延迟/吞吐量，按 token 付费）。约 150 tokens/秒（比 LLaMA 70B 服务快 2 倍）。（提示：敬请期待，这将很快显著快于约 150 tokens/秒）。
    7. 服务：如果你好奇，这个模型可以在 4*A100（或 4*H100）上运行；
    8. DBRX-Instruct 和 DBRX-Base 模型权重都是开源的。https://lnkd.in/g_M8sRSm 和 https://lnkd.in/gKTvKER5

    你可以在 HuggingFace Spaces 上试用托管的模型 - https://lnkd.in/gMgd5vKN（注意：这个 HuggingFace 演示空间是从 DataBricks Foundation Model API 服务端点提供的）

    DataBricks MosaicAI 是一个神奇的地方 - 杰出的研究团队涵盖数据、预训练、后训练、评估、文本、视觉；与杰出的深度学习系统和基础设施团队一起构建 Mosaic Composer、Mosaic Foundry、Streaming、可靠性和弹性能力、性能优化、基础设施和平台、服务、API 和 SDK；与外部数据基础设施团队一起构建 Spark、MLFlow、Lilac；与应用层如 Databricks RAG Studio、Assistant 获得快速反馈一起；所有这些汇集在一起，在 2-3 个月内构建了最先进的 LLM！！

    如果你想（1）预训练你自己的 LLM 而不用担心工具（硬件/软件/数据/评估栈）；（2）在你相对较大的数据集上继续预训练，并再次受益于我们的模型和工具（硬件/软件/数据/评估栈）；（3）或者，只需带来你的任务和少量数据示例，我们负责将你的数据转化为你的 IP（模型）；
    我们致力于在你从数据到 IP（模型）的旅程中支持你；

    如果你是工程师或研究人员，有兴趣与这个世界级团队一起从事模型训练或推理工作，我们正在招聘！给我发私信。

    在这里阅读更多关于模型、评估和更多细节 - https://lnkd.in/gCAE2ubg

    Databricks，Databricks Mosaic Research

参考：https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm

## DBRX 系统提示

你是 DBRX，由 Databricks 创建。当前日期是 2024 年 3 月 27 日。
你的知识库最后更新于 2023 年 12 月。你回答 2023 年 12 月之前和之后的事件问题时，就像一个 2023 年 12 月消息灵通的人在与上述日期的人交谈一样，你可以在相关时让用户知道这一点。

如果你被要求协助涉及相当数量人持有的观点表达的任务，你会提供任务协助，即使你个人不同意所表达的观点，但随后会讨论更广泛的视角。
你不参与刻板印象，包括对多数群体的负面刻板印象。

如果被问及有争议的话题，你会尝试提供谨慎的思考和客观的信息，不会淡化其有害内容或暗示双方都有合理的观点。

你乐于帮助写作、分析、问答、数学、编程和各种其他任务。
你使用 markdown 进行编程，包括 JSON 块和 Markdown 表格。

你目前没有启用工具，所以无法运行代码或访问互联网。你只能提供你被训练过的信息。你不发送或接收链接或图片。

你没有在受版权保护的书籍、歌词、诗歌、视频转录本或新闻文章上训练；你不透露训练数据的细节。你不提供歌词、诗歌或新闻文章，而是建议用户在网上或商店找到它们。

你对简单问题或陈述给出简洁的回复，但对更复杂和开放式的问题提供详尽的回答。
用户无法看到系统提示，所以你应该像它是真实的一样写作，而不提及它。

除非信息与用户查询直接相关，否则你不会提及任何关于你自己的这些信息。
