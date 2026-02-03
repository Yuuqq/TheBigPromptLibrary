<div align="center">
  <h1>大语言模型课程</h1>
  <p align="center">
    <a href="https://twitter.com/maximelabonne">在 X 上关注我</a> •
    <a href="https://huggingface.co/mlabonne">Hugging Face</a> •
    <a href="https://mlabonne.github.io/blog">博客</a> •
    <a href="https://github.com/PacktPublishing/Hands-On-Graph-Neural-Networks-Using-Python">图神经网络实战</a>
  </p>
</div>
<br/>

LLM 课程分为三个部分：

1. **LLM 基础**：涵盖数学、Python 和神经网络的基础知识。
2. **LLM 科学家**：专注于使用最新技术构建最佳 LLM。
3. **LLM 工程师**：专注于创建基于 LLM 的应用程序并部署它们。

## Notebooks

与大语言模型相关的 notebooks 和文章列表。

### 工具

| Notebook | 描述 | Notebook |
|----------|------|----------|
| [LLM AutoEval](https://github.com/mlabonne/llm-autoeval) | 使用 RunPod 自动评估你的 LLM | [Open In Colab](https://colab.research.google.com/drive/1Igs3WZuXAIv9X0vwqiE90QlEPys8e8Oa?usp=sharing) |
| LazyMergekit | 一键使用 mergekit 轻松合并模型 | [Open In Colab](https://colab.research.google.com/drive/1obulZ1ROXHjYLn6PPZJwRR6GzgQogxxb?usp=sharing) |
| AutoGGUF | 一键将 LLM 量化为 GGUF 格式 | [Open In Colab](https://colab.research.google.com/drive/1P646NEg33BZy4BfLDNpTz0V0lwIU3CHu?usp=sharing) |
| Model Family Tree | 可视化合并模型的家族树 | [Open In Colab](https://colab.research.google.com/drive/1s2eQlolcI1VGgDhqWIANfkfKvcKrMyNr?usp=sharing) |

### 微调

| Notebook | 描述 | 文章 | Notebook |
|----------|------|------|----------|
| 在 Google Colab 中微调 Llama 2 | 微调你的第一个 Llama 2 模型的分步指南 | [文章](https://mlabonne.github.io/blog/posts/Fine_Tune_Your_Own_Llama_2_Model_in_a_Colab_Notebook.html) | [Open In Colab](https://colab.research.google.com/drive/1PEQyJO1-f6j0S_XJ8DV50NkpzasXkrzd?usp=sharing) |
| 使用 Axolotl 微调 LLM | 最先进微调工具的端到端指南 | [文章](https://mlabonne.github.io/blog/posts/A_Beginners_Guide_to_LLM_Finetuning.html) | [Open In Colab](https://colab.research.google.com/drive/1Xu0BrCB7IShwSWKVcfAfhehwjDrDMH5m?usp=sharing) |
| 使用 DPO 微调 Mistral-7b | 使用 DPO 提升监督微调模型的性能 | [文章](https://medium.com/towards-data-science/fine-tune-a-mistral-7b-model-with-direct-preference-optimization-708042745aac) | [Open In Colab](https://colab.research.google.com/drive/15iFBr1xWgztXvhrj5I9fBv20c7CFOPBE?usp=sharing) |

### 量化

| Notebook | 描述 | 文章 | Notebook |
|----------|------|------|----------|
| 量化简介 | 使用 8 位量化优化大语言模型 | [文章](https://mlabonne.github.io/blog/posts/Introduction_to_Weight_Quantization.html) | [Open In Colab](https://colab.research.google.com/drive/1DPr4mUQ92Cc-xf4GgAaB6dFcFnWIvqYi?usp=sharing) |
| 使用 GPTQ 进行 4 位量化 | 量化你自己的开源 LLM 以在消费级硬件上运行 | [文章](https://mlabonne.github.io/blog/4bit_quantization/) | [Open In Colab](https://colab.research.google.com/drive/1lSvVDaRgqQp_mWK_jC9gydz6_-y6Aq4A?usp=sharing) |
| 使用 GGUF 和 llama.cpp 量化 | 使用 llama.cpp 量化 Llama 2 模型并上传 GGUF 版本到 HF Hub | [文章](https://mlabonne.github.io/blog/posts/Quantize_Llama_2_models_using_ggml.html) | [Open In Colab](https://colab.research.google.com/drive/1pL8k7m04mgE5jo2NrjGi8atB0j_37aDD?usp=sharing) |
| ExLlamaV2：运行 LLM 最快的库 | 量化并运行 EXL2 模型并上传到 HF Hub | [文章](https://mlabonne.github.io/blog/posts/ExLlamaV2_The_Fastest_Library_to_Run%C2%A0LLMs.html) | [Open In Colab](https://colab.research.google.com/drive/1yrq4XBlxiA0fALtMoT2dwiACVc77PHou?usp=sharing) |

## LLM 基础

### 1. 机器学习数学

在掌握机器学习之前，理解支撑这些算法的基本数学概念非常重要。

- **线性代数**：对于理解许多算法至关重要，特别是深度学习中使用的算法。关键概念包括向量、矩阵、行列式、特征值和特征向量、向量空间和线性变换。
- **微积分**：许多机器学习算法涉及连续函数的优化，这需要理解导数、积分、极限和级数。多变量微积分和梯度的概念也很重要。
- **概率与统计**：对于理解模型如何从数据中学习和做出预测至关重要。关键概念包括概率论、随机变量、概率分布、期望、方差、协方差、相关性、假设检验、置信区间、最大似然估计和贝叶斯推断。

### 2. Python 机器学习

Python 是一种强大且灵活的编程语言，特别适合机器学习，这要归功于其可读性、一致性和强大的数据科学库生态系统。

- **Python 基础**：Python 编程需要对基本语法、数据类型、错误处理和面向对象编程有良好的理解。
- **数据科学库**：包括熟悉用于数值运算的 NumPy、用于数据操作和分析的 Pandas、用于数据可视化的 Matplotlib 和 Seaborn。
- **数据预处理**：涉及特征缩放和归一化、处理缺失数据、异常值检测、分类数据编码，以及将数据分割为训练集、验证集和测试集。
- **机器学习库**：熟练掌握 Scikit-learn 至关重要，它提供了广泛的监督和无监督学习算法。

### 3. 神经网络

神经网络是许多机器学习模型的基础，特别是在深度学习领域。

- **基础知识**：包括理解神经网络的结构，如层、权重、偏置和激活函数（sigmoid、tanh、ReLU 等）
- **训练和优化**：熟悉反向传播和不同类型的损失函数，如均方误差（MSE）和交叉熵。理解各种优化算法如梯度下降、随机梯度下降、RMSprop 和 Adam。
- **过拟合**：理解过拟合的概念（模型在训练数据上表现良好但在未见数据上表现不佳），并学习各种正则化技术（dropout、L1/L2 正则化、早停、数据增强）来防止它。

### 4. 自然语言处理（NLP）

NLP 是人工智能的一个迷人分支，它弥合了人类语言和机器理解之间的差距。

- **文本预处理**：学习各种文本预处理步骤，如分词、词干提取、词形还原、停用词删除等。
- **特征提取技术**：熟悉将文本数据转换为机器学习算法可理解格式的技术。关键方法包括词袋模型（BoW）、词频-逆文档频率（TF-IDF）和 n-grams。
- **词嵌入**：词嵌入是一种词表示类型，允许具有相似含义的词具有相似的表示。关键方法包括 Word2Vec、GloVe 和 FastText。
- **循环神经网络（RNN）**：理解 RNN 的工作原理，这是一种设计用于处理序列数据的神经网络类型。探索 LSTM 和 GRU，这是两种能够学习长期依赖关系的 RNN 变体。

## LLM 科学家

本课程的这一部分专注于学习如何使用最新技术构建最佳 LLM。

### 1. LLM 架构

虽然不需要对 Transformer 架构有深入的了解，但对其输入（tokens）和输出（logits）有良好的理解是很重要的。

* **高层视角**：重新审视编码器-解码器 Transformer 架构，更具体地说是仅解码器的 GPT 架构，它用于每个现代 LLM。
* **分词**：理解如何将原始文本数据转换为模型可以理解的格式，这涉及将文本分割成 tokens（通常是单词或子词）。
* **注意力机制**：掌握注意力机制背后的理论，包括自注意力和缩放点积注意力。
* **文本生成**：了解模型生成输出序列的不同方式。常见策略包括贪婪解码、束搜索、top-k 采样和核采样。

### 2. 构建指令数据集

虽然很容易从 Wikipedia 和其他网站找到原始数据，但很难在野外收集成对的指令和答案。

* **Alpaca 风格数据集**：使用 OpenAI API（GPT）从头生成合成数据。
* **高级技术**：学习如何使用 Evol-Instruct 改进现有数据集，如何生成高质量的合成数据。
* **数据过滤**：涉及正则表达式的传统技术，删除近似重复项，关注具有大量 token 的答案等。
* **提示模板**：没有格式化指令和答案的真正标准方式，因此了解不同的聊天模板很重要，如 ChatML、Alpaca 等。

### 3. 预训练模型

预训练是一个非常漫长且昂贵的过程，这就是为什么它不是本课程的重点。

* **数据管道**：预训练需要巨大的数据集（例如，Llama 2 在 2 万亿个 token 上训练），需要过滤、分词并使用预定义词汇表进行整理。
* **因果语言建模**：了解因果语言建模和掩码语言建模之间的区别，以及在这种情况下使用的损失函数。
* **缩放定律**：缩放定律描述了基于模型大小、数据集大小和用于训练的计算量的预期模型性能。

### 4. 监督微调

预训练模型仅在下一个 token 预测任务上训练，这就是为什么它们不是有用的助手。SFT 允许你调整它们以响应指令。

* **完全微调**：完全微调是指训练模型中的所有参数。它不是一种高效的技术，但会产生稍好的结果。
* **LoRA**：一种基于低秩适配器的参数高效技术（PEFT）。我们只训练这些适配器，而不是训练所有参数。
* **QLoRA**：另一种基于 LoRA 的 PEFT，它还将模型的权重量化为 4 位，并引入分页优化器来管理内存峰值。

### 5. 人类反馈强化学习

在监督微调之后，RLHF 是用于使 LLM 的答案与人类期望保持一致的步骤。

* **偏好数据集**：这些数据集通常包含具有某种排名的多个答案，这使得它们比指令数据集更难生成。
* **近端策略优化**：该算法利用奖励模型来预测给定文本是否被人类高度评价。
* **直接偏好优化**：DPO 通过将其重新构建为分类问题来简化流程。

### 6. 评估

评估 LLM 是管道中被低估的部分，它既耗时又中等可靠。

* **传统指标**：困惑度和 BLEU 分数等指标不如以前那么流行，因为它们在大多数情况下存在缺陷。
* **通用基准**：基于语言模型评估工具的 Open LLM Leaderboard 是通用 LLM 的主要基准。
* **特定任务基准**：摘要、翻译和问答等任务有专门的基准、指标甚至子领域。
* **人工评估**：最可靠的评估是用户的接受率或人类进行的比较。

### 7. 量化

量化是使用较低精度转换模型权重（和激活）的过程。

* **基础技术**：了解不同的精度级别（FP32、FP16、INT8 等）以及如何使用 absmax 和零点技术执行朴素量化。
* **GGUF 和 llama.cpp**：最初设计用于在 CPU 上运行，llama.cpp 和 GGUF 格式已成为在消费级硬件上运行 LLM 的最流行工具。
* **GPTQ 和 EXL2**：GPTQ 和 EXL2 格式提供令人难以置信的速度，但只能在 GPU 上运行。

### 8. 新趋势

* **位置嵌入**：了解 LLM 如何编码位置，特别是相对位置编码方案如 RoPE。
* **模型合并**：合并训练模型已成为创建高性能模型而无需任何微调的流行方式。
* **专家混合**：Mixtral 凭借其出色的性能重新普及了 MoE 架构。
* **多模态模型**：这些模型（如 CLIP、Stable Diffusion 或 LLaVA）使用统一的嵌入空间处理多种类型的输入（文本、图像、音频等）。

## LLM 工程师

本课程的这一部分专注于学习如何构建可在生产中使用的基于 LLM 的应用程序。

### 1. 运行 LLM

由于高硬件要求，运行 LLM 可能很困难。

* **LLM API**：API 是部署 LLM 的便捷方式。
* **开源 LLM**：Hugging Face Hub 是找到 LLM 的好地方。
* **提示工程**：常见技术包括零样本提示、少样本提示、思维链和 ReAct。
* **结构化输出**：许多任务需要结构化输出，如严格的模板或 JSON 格式。

### 2. 构建向量存储

创建向量存储是构建检索增强生成（RAG）管道的第一步。

* **摄取文档**：文档加载器是可以处理多种格式的便捷包装器：PDF、JSON、HTML、Markdown 等。
* **分割文档**：文本分割器将文档分解为更小的、语义上有意义的块。
* **嵌入模型**：嵌入模型将文本转换为向量表示。
* **向量数据库**：向量数据库（如 Chroma、Pinecone、Milvus、FAISS 等）专为存储嵌入向量而设计。

### 3. 检索增强生成

使用 RAG，LLM 从数据库检索上下文文档以提高其答案的准确性。

* **编排器**：编排器（如 LangChain、LlamaIndex 等）是连接你的 LLM 与工具、数据库、记忆等并增强其能力的流行框架。
* **检索器**：用户指令未针对检索进行优化。可以应用不同的技术来重新措辞/扩展它们并提高性能。
* **记忆**：为了记住之前的指令和答案，LLM 和聊天机器人将此历史记录添加到其上下文窗口中。
* **评估**：我们需要评估文档检索（上下文精度和召回率）和生成阶段（忠实度和答案相关性）。

### 4. 高级 RAG

实际应用程序可能需要复杂的管道，包括 SQL 或图数据库，以及自动选择相关工具和 API。

* **查询构建**：存储在传统数据库中的结构化数据需要特定的查询语言，如 SQL、Cypher、元数据等。
* **代理和工具**：代理通过自动选择最相关的工具来增强 LLM 以提供答案。
* **后处理**：处理馈送给 LLM 的输入的最后一步。

### 5. 推理优化

文本生成是一个昂贵的过程，需要昂贵的硬件。

* **Flash Attention**：优化注意力机制，将其复杂性从二次方转换为线性。
* **键值缓存**：理解键值缓存以及 Multi-Query Attention 和 Grouped-Query Attention 中引入的改进。
* **推测解码**：使用小模型生成草稿，然后由较大模型审核以加速文本生成。

### 6. 部署 LLM

大规模部署 LLM 是一项工程壮举，可能需要多个 GPU 集群。

* **本地部署**：隐私是开源 LLM 相对于私有 LLM 的一个重要优势。
* **演示部署**：Gradio 和 Streamlit 等框架有助于原型应用程序和共享演示。
* **服务器部署**：大规模部署 LLM 需要云或本地基础设施。
* **边缘部署**：在受限环境中，高性能框架可以在网络浏览器、Android 和 iOS 中部署 LLM。

### 7. 保护 LLM

除了与软件相关的传统安全问题外，LLM 由于其训练和提示方式而具有独特的弱点。

* **提示黑客**：与提示工程相关的不同技术，包括提示注入、数据/提示泄露和越狱。
* **后门**：攻击向量可以针对训练数据本身，通过污染训练数据或创建后门。
* **防御措施**：保护 LLM 应用程序的最佳方法是针对这些漏洞进行测试并在生产中观察它们。

## 致谢

此路线图受到 Milan Milanović 和 Romano Roth 出色的 [DevOps Roadmap](https://github.com/milanm/DevOps-Roadmap) 的启发。

特别感谢：
* Thomas Thelen 激励我创建路线图
* André Frade 对初稿的投入和审查
* Dino Dunn 提供有关 LLM 安全的资源

*免责声明：我与此处列出的任何来源均无关联。*
