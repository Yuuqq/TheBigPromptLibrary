# ChatGPT工作虚拟机的完整系统清单

*由 **Elias Bachaalany** — [@0xeb](https://github.com/0xeb) 在GitHub · [Binary Wizards](https://www.youtube.com/@binary-wizards) 在YouTube · [@eliasbchlny](https://x.com/eliasbchlny) 在X*

ChatGPT工作模式为您提供**真实Linux虚拟机**——不是临时的画布，而是可长期运行的实体机器。您可以在其中编写代码、构建项目、浏览网页、运行实验、托管文件，并保持会话期间持久化的文件系统。

这种组合是其强大性的核心。指向仓库时，它能克隆、构建、运行输出并迭代实验。完成任务后，只需要求压缩结果，即可获得下载链接。这构成完整的开发-构建-运行-收集闭环，全程使用自然语言驱动。

显然的问题是：**这到底是什么机器？** 核心配置、内存容量、存储空间、资源限制、已安装工具链以及隐藏的边界在哪里？本文档完整展示CPU、内存、存储、资源限制、安装软件、Python/Node包列表等信息——这是沙盒刻意隐藏的主机部分。

本文档是前两篇沙盒清单（[Python包列表](./chatgpt-code-python-pkglist-08232024.md) 和 [Linux包列表](./chatgpt-code-pkglist-08232024.md)）的配套指南，但彼时沙盒环境受严格限制，而本环境突破包管理范畴。

*捕获时间：2026年8月6日 09:13:48（太平洋时间） (`2026-08-06T16:13:48.374439+00:00`)，基于全新工作区——会话前未克隆、安装或构建任何内容。所有图表均为实时抓取，非模型对自身环境的记忆。*

## 实际容量概览

若需评估运行负载，关键限制如下：

- **9逻辑CPU核心**
- **23.55GB总内存**，捕获时**22.11GB可用**
- **58.28GB工作区存储**
- **无交换分区**
- 强大的Python/Node.js/C/C++/文档/表格/PDF/图像/OCR及多媒体处理支持
- **未预装Docker/Podman/Go/Rust/.NET/CMake/Kubernetes或数据库客户端工具**

该环境适合中等规模的Python/Node项目及Make构建的C/C++项目，但受限于网络和文件系统沙盒。依赖CMake/Go/Rust工具链或容器运行时需自行携带。

以下为具体验证。

## 重要范围说明

这是受限制的KVM虚拟化执行环境。本文档数据仅反映工作区可见资源，非物理主机全貌。`/proc`、`/sys`、挂载表、Debian包数据库、PCI设备、GPU设备均被隐藏或截断。当常规工具无法读取这些接口时，清单改用操作系统系统调用和运行时API获取数据——因此您会看到类似`sysinfo`的数值而非`free`/`lscpu`输出。

## 操作系统

| 项目 | 值 |
|---|---|
| 发行版 | Ubuntu 24.04.3 LTS |
| 代号 | Noble Numbat |
| 内核 | Linux 6.18.35 |
| 内核编译 | `#1 SMP Mon Jul 27 18:07:50 UTC 2026` |
| 架构 | x86_64 / AMD64 |
| 字节序 | Little-endian |
| C库 | glibc 2.39 |
| 虚拟化 | KVM |
| 主机名 | `f20c423af0c2` |
| 工作区时区 | America/Los_Angeles |
| 页大小 | 4,096字节 |
| 捕获时系统运行时间 | 44,515秒（约12小时21分55秒） |
| 负载平均 | 0.000 / 0.000 / 0.000 |
| 进程计数器（`sysinfo`报告） | 213 |

注意容器化主机名及长期空闲状态下的12小时运行时间——该工作区在发出任何请求前已持续运行。

## CPU

| 项目 | 值 |
|---|---|
| 分配CPU | 9逻辑CPU核心 |
| CPU亲和 | IDs 0-8 |
| 暴露架构代数 | AMD Zen 4 |
| GCC原生目标 | `znver4` |
| CPUID品牌字符串 | AMD EPYC 9V74 80核处理器 |
| 虚拟化层 | KVM |
| L1指令缓存 | 32 KiB |
| L1数据缓存 | 32 KiB |
| 缓存行大小 | 64字节 |
| L2缓存 | 1 MiB |
| L3缓存 | 32 MiB |

处理器品牌标识**虚拟化主机CPU类**，而非物理分配。本工作区拥有**9 vCPUs**而非80物理核心。物理插槽、物理核心数、拓扑结构及频率均不暴露。

原生编译探测仍报告`znver4`目标。`AMD EPYC 9V74`字符串本身即泄露：`V`系列为Azure专用SKU，与当前运行环境一致。

暴露的指令集支持MMX/SSE4.2/AVX/AVX2/FMA/BMI1/2/AES/PCLMUL/VAES/VPCLMULQDQ/SHA/GFNI/RDRAND/RDSEED及多种AVX-512扩展（F/VL/BW/DQ/CD/VBMI/VBMI2/IFMA/VNNI/VPOPCNTDQ/BITALG/BF16）。

## 内存

| 项目 | 大小 |
|---|---:|
| 总内存 | 23.55 GB |
| 可用内存 | 22.11 GB |
| 共享内存 | 108 MB |
| 缓冲内存 | 78 MB |
| 总交换 | 0 |
| 交换可用 | 0 |

**无交换分区**。所有运行进程必须完全驻留内存。

## 工作区存储

这是挂载的工作区文件系统容量，非主机完整存储清单。

| 项目 | 大小 |
|---|---:|
| 文件系统容量 | 67.05 GB |
| 已用 | 5.32 GB |
| 工作区可用 | 58.28 GB |
| 原生空闲块 | 61.73 GB |

- 已用容量占比：约7.93%
- 文件系统块/片段大小：4 KiB
- 总节点数：4,194,304；空闲节点数：4,081,122
- 最大文件名长度：255字节

## 资源限制

| 限制 | 软限制 | 硬限制 |
|---|---:|---:|
| 打开文件数 | 16,384 | 16,384 |
| 进程数 | 7,851 | 7,851 |
| 栈大小 | 8 MiB | 无限制 |
| 核心转储 | 0（禁用） | 无上限 |

## 主要开发工具

| 软件 | 版本 | 可执行状态 |
|---|---|---|
| Git | 2.51.1 | `/usr/local/bin/git` |
| Git LFS | 3.4.1 | `/usr/bin/git-lfs` |
| GCC | 13.3.0 | `/usr/bin/gcc` |
| G++ | 13.3.0 | `/usr/bin/g++` |
| GNU Make | 4.3 | `/usr/bin/make` |
| Python | 3.12.13 | 嵌入主运行时 |
| pip | 26.0.1 | 嵌入主运行时 |
| uv | 0.11.33 | 嵌入主运行时 |
| Node.js | 24.14.0 LTS ("Krypton") | 嵌入主运行时 |
| npm | 11.9.0 | 嵌入主运行时 |
| pnpm | 11.7.0 | 嵌入主运行时 |
| Corepack | 0.34.6 | Node全局安装 |
| Perl | 5.38.2 | `/usr/bin/perl` |
| Bash | 5.2.21 | `/usr/bin/bash` |
| Zsh | 5.9 | `/usr/bin/zsh` |
| curl | 8.5.0 | `/usr/bin/curl` |
| wget | 1.21.4 | `/usr/bin/wget` |
| OpenSSH | 9.6p1 | `/usr/bin/ssh` |
| OpenSSL CLI | 3.0.13 | `/usr/bin/openssl` |
| apt | 2.8.3 | `/usr/bin/apt` |
| dpkg | 1.22.6 | `/usr/bin/dpkg` |
| jq | 1.7 | `/usr/bin/jq` |
| ripgrep | 15.2.0 | Codex路径 |
| nano | 可用 | `/usr/bin/nano` |
| rsync | 可用 | `/usr/bin/rsync` |

嵌入的Python/Node运行时基于OpenSSL 3.5.5。Python报告SQLite 3.50.4和zlib 1.3.1。Node报告SQLite 3.51.2、V8 13.6.233.17-node.41、ICU 78.2、Unicode 17.0、libuv 1.51.0、zlib 1.3.1和zstd 1.5.7。

## 文档/图像/媒体/OCR工具

| 软件 | 版本/状态 |
|---|---|
| FFmpeg | 6.1.1 |
| ImageMagick | 6.9.12-98 Q16 |
| Pandoc | 3.1.3 |
| Tesseract OCR | 5.3.4 |
| Poppler `pdftotext` | 24.02.0 |
| Ghostscript | 10.02.1 |
| LibreOfficeDev | 26.8.0.0.alpha0（通过捆绑启动器可检查版本） |
| Inkscape | 可执行文件存在，但失败——`libinkscape_base.so`缺失 |
| Java | 启动器存在，但失败——`libjli.so`缺失 |

## 已安装Python包

51个Python发行包：

```text
PyMuPDF==1.26.6
PyYAML==6.0.3
annotated-types==0.7.0
artifact_tool_v2==2.8.21
cffi==1.17.1
charset-normalizer==3.4.4
contourpy==1.3.3
cryptography==46.0.0
cycler==0.12.1
et_xmlfile==2.0.0
fonttools==4.61.1
joblib==1.5.3
kiwisolver==1.4.9
lxml==6.0.2
matplotlib==3.10.8
numpy==2.3.5
openpyxl==3.1.5
packaging==26.2
pandas==2.2.3
pdf2image==1.17.0
pdfminer.six==20251107
pdfplumber==0.11.8
pillow==12.2.0
pip==26.0.1
pycparser==2.23
pydantic==2.13.4
pydantic_core==2.46.4
pyhumps==3.8.0
pyparsing==3.3.2
pypdf==6.10.0
pypdfium2==5.3.0
python-dateutil==2.9.0.post0
python-docx==1.2.0
python-pptx==1.0.2
pytz==2026.2
reportlab==4.4.9
scikit-learn==1.8.0
scipy==1.17.0
seaborn==0.13.2
setuptools==82.0.1
six==1.17.0
threadpoolctl==3.6.0
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2026.2
uv==0.11.33
websockets==16.0
wheel==0.47.0
xlrd==2.0.1
xlsxwriter==3.2.9
zstandard==0.25.0
```

对比[2024代码解释器清单](./chatgpt-code-python-pkglist-08232024.md)：彼时沙盒预装数百个包包括完整科学/ML栈。本环境仅51个包——聚焦文档处理、绘图及核心scikit-learn/scipy支持。注意内部`artifact_tool_v2==2.8.21`非PyPI公开包。

## 捆绑的Node.js库

顶层运行时模块：

```text
@napi-rs
@oai
@viz-js
docx
jpeg-js
lucide
marked
pdf-lib
pdfjs-dist
pixelmatch
playwright
pngjs
pnpm
pptxgenjs
sharp
tesseract.js
```

依赖树包含117个`package.json`清单。全局Node包为`corepack@0.34.6`和`npm@11.9.0`。`@oai`作用域为内部工具，非公开包。

## 可用软件概览

`PATH`下可发现：

```text
apt, dpkg, git, git-lfs, curl, wget, rsync, ssh, scp,
gcc, g++, make, python3, pip, uv, node, npm, npx, pnpm,
perl, jq, rg, nano, ffmpeg, convert, pandoc, soffice,
tesseract, pdftotext, gs
```

无法找到以下命令行工具：

```text
rpm, apk, snap, flatpak, gh, svn, hg, gfortran, clang,
clang++, cmake, ninja, meson, autoconf, automake, yarn,
bun, deno, ruby, gem, javac, go, rustc, cargo, dotnet,
php, R, sqlite3, psql, mysql, redis-cli, docker, podman,
buildah, kubectl, helm, terraform, ansible, yq, fd, vim,
nvim, emacs, tmux, screen, magick, chromium,
chromium-browser, google-chrome, playwright CLI, qpdf,
nvidia-smi, rocminfo, lspci, lsusb
```

尽管包含`playwright` Node模块，但未在`PATH`下提供独立可执行文件。

## 清单统计

| 类别 | 数量 |
|---|---:|
| `PATH`下唯一可执行文件 | 1,023 |
| 可解析的shell命令 | 1,393 |
| 链接器缓存中的共享库 | 505 |
| Python发行包 | 51 |
| Node依赖树中的package.json | 117 |

## 不可见资源

本部分揭示沙盒的隐藏面：

- Debian包管理器工具存在，但未完整暴露包数据库。权威`apt`/`dpkg`包列表**无法生成**——这正是[2024代码解释器沙盒](./chatgpt-code-pkglist-08232024.md)的破解方式，而本环境已修复。
- `/proc`和`/sys`未挂载，因此`lscpu`、`free`、`df`等工具无法输出常规结果。清单改用系统调用/运行时API获取数据。
- GPU存在性无法确认。NVIDIA/AMD驱动未安装，且PCI(sysfs)探测不可用。解读为**GPU状态未知**而非明确"无GPU"。
- 物理磁盘设备、存储模型、RAID布局、CPU插槽、物理核心拓扑、散热状态及时钟频率均不暴露。
- 包含的执行文件**可能无法正常工作**。Java和Inkscape存在但依赖缺失（`libjli.so`/`libinkscape_base.so`）。