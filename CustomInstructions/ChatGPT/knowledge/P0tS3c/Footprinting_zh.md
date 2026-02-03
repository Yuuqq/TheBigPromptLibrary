#footprinting #dns #enumeration #hacking

#### assignment

我们受 `Inlanefreight Ltd` 公司委托，对其内部网络中的三台不同服务器进行测试。该公司使用多种不同的服务，IT 安全部门认为有必要进行渗透测试（penetration test，一种模拟攻击以评估安全性的测试方法），以全面了解其整体安全态势。

第一台服务器是需要调查的内部 DNS（Domain Name System，域名系统）服务器。具体而言，我们的客户想知道我们能从这些服务中获取哪些信息，以及这些信息如何被用于针对其基础设施的攻击。我们的目标是尽可能多地收集关于该服务器的信息，并找到利用这些信息针对该公司的方法。然而，我们的客户明确表示，禁止使用漏洞利用程序（exploits）对服务进行攻击性攻击，因为这些服务正在生产环境中运行。

此外，我们的队友发现了以下凭据"ceil:qwer1234"，他们指出该公司的一些员工曾在论坛上讨论过 SSH 密钥。

管理员在此服务器上存储了一个 `flag.txt` 文件，用于跟踪我们的进度并衡量成功与否。完全枚举目标并提交此文件的内容作为证明。

#### hack

PORT     STATE SERVICE VERSION
21/tcp   open  ftp     ProFTPD
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
	ssh-hostkey:
	3072 3f:4c:8f:10:f1:ae:be:cd:31:24:7c:a1:4e:ab:84:6d (RSA)
	256 7b:30:37:67:50:b9:ad:91:c0:8f:f7:02:78:3b:7c:02 (ECDSA)[[Lesson 18 - Windows Remote Management Protocols]]
	256 88:9e:0e:07:fe:ca:d0:5c:60:ab:cf:10:99:cd:6c:a7 (ED25519)
53/tcp   open  domain  ISC BIND 9.16.1 (Ubuntu Linux)
	dns-nsid:
	bind.version: 9.16.1-Ubuntu
2121/tcp open  ftp     ProFTPD
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

ftp.int.inlanefreight.htb

* 使用"ceil:qwer1234"凭据 ftp 连接到 <IP>
	* --> 端口 **2121** 而*不是* 21
* 找到 .ssh 目录并下载了 id_rsa
* 使用 id_rsa ssh 连接到 <IP>（不要忘记 chmod 400 id_rsa）
* cd /home/flag
* flag.txt
* HTB{7nrzise7hednrxihskjed7nzrgkweunj47zngrhdbkjhgdfbjkc7hgj}


#footprinting #enumeration #htb

第三台服务器是内部网络的 MX（Mail Exchange，邮件交换）和管理服务器。因此，该服务器具有域内内部账户备份服务器的功能。相应地，这里也创建了一个名为 `HTB` 的用户，我们需要获取其凭据才能访问。

### nmap general scan

![[footprintlabHard_nmap_general.html]]

### nmap aggressive scan
![[footprintlabHard_nmap_aggressive.html]]

### nmap mail ports
![[footprintlabHard_nmap_mailports.html]]

### nmap UDP scan![[footprintlabHard_nmap_udp.html]]



### found ports and other stuff

ports: 22,110,143,993, 995

NIXHARD

161/udp  open          snmp        udp-response ttl 63 net-snmp; net-snmp SNMPv3 server
| snmp-info:
|   enterprise: net-snmp
|   engineIDFormat: unknown
|   engineIDData: 5b99e75a10288b6100000000
|   snmpEngineBoots: 10
|_  snmpEngineTime: 1h02m55s


onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.202.20
Scanning 1 hosts, 3219 communities
10.129.202.20 [backup] Linux NIXHARD 5.4.0-90-generic #101-Ubuntu SMP Fri Oct 15 20:00:55 UTC 2021 x86_64

community string --> **backup**
* 我们使用 onesixtyone 暴力破解 SNMP（Simple Network Management Protocol，简单网络管理协议）community strings（社区字符串）
	* onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.202.20
	* --> 10.129.202.20 [backup] Linux NIXHARD 5.4.0-90-generic #101-Ubuntu SMP Fri Oct 15 20:00:55 UTC 2021 x86_64
* 我们找到了 SNMP community **"backup"**
* 我们执行 braa
	* braa backup@10.129.202.20:.1.3.6.*
		* 10.129.202.20:184ms:.80:**/opt/tom-recovery.sh**
		* 10.129.202.20:267ms:.80:** tom NMds732Js2761 **
		* 10.129.202.20:289ms:.0:Admin <tech@inlanefreight.htb>
		* 10.129.202.20:288ms:.0:NIXHARD
		* 10.129.202.20:288ms:.0:Inlanefreight
	* 我们可以以 **tom** 身份登录邮件服务器
		* openssl s_client -connect 10.129.202.20:pop3s
			* user tom
			* pass NMds732Js2761
			* 我们找到了一封包含 [[#private ssh key]] 的邮件（retr 1）
		* openssl s_client -connect 10.129.202.20:imaps
			* a0001 login tom NMds732Js2761
			* a0002 list "" *
			* a0003 select inbox
			* a0004 fetch 1 BODY[TEXT]
	* 我们可以使用私钥 ssh 连接到服务器（不要忘记 chmod 400）
		* ssh tom@10.129.202.20 -i id_rsa
	* mysql -u tom -p
		* show databases
		* use users
		* select * from users where username='HTB';
			* HTB / cr3n4o7rzse7rzhnckhssncif7ds


#### private ssh key

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEA9snuYvJaB/QOnkaAs92nyBKypu73HMxyU9XWTS+UBbY3lVFH0t+F
+yuX+57Wo48pORqVAuMINrqxjxEPA7XMPR9XIsa60APplOSiQQqYreqEj6pjTj8wguR0Sd
hfKDOZwIQ1ILHecgJAA0zY2NwWmX5zVDDeIckjibxjrTvx7PHFdND3urVhelyuQ89BtJqB
abmrB5zzmaltTK0VuAxR/SFcVaTJNXd5Utw9SUk4/l0imjP3/ong1nlguuJGc1s47tqKBP
HuJKqn5r6am5xgX5k4ct7VQOQbRJwaiQVA5iShrwZxX5wBnZISazgCz/D6IdVMXilAUFKQ
X1thi32f3jkylCb/DBzGRROCMgiD5Al+uccy9cm9aS6RLPt06OqMb9StNGOnkqY8rIHPga
H/RjqDTSJbNab3w+CShlb+H/p9cWGxhIrII+lBTcpCUAIBbPtbDFv9M3j0SjsMTr2Q0B0O
jKENcSKSq1E1m8FDHqgpSY5zzyRi7V/WZxCXbv8lCgk5GWTNmpNrS7qSjxO0N143zMRDZy
Ex74aYCx3aFIaIGFXT/EedRQ5l0cy7xVyM4wIIA+XlKR75kZpAVj6YYkMDtL86RN6o8u1x
3txZv15lMtfG4jzztGwnVQiGscG0CWuUA+E1pGlBwfaswlomVeoYK9OJJ3hJeJ7SpCt2GG
cAAAdIRrOunEazrpwAAAAHc3NoLXJzYQAAAgEA9snuYvJaB/QOnkaAs92nyBKypu73HMxy
U9XWTS+UBbY3lVFH0t+F+yuX+57Wo48pORqVAuMINrqxjxEPA7XMPR9XIsa60APplOSiQQ
qYreqEj6pjTj8wguR0SdhfKDOZwIQ1ILHecgJAA0zY2NwWmX5zVDDeIckjibxjrTvx7PHF
dND3urVhelyuQ89BtJqBabmrB5zzmaltTK0VuAxR/SFcVaTJNXd5Utw9SUk4/l0imjP3/o
ng1nlguuJGc1s47tqKBPHuJKqn5r6am5xgX5k4ct7VQOQbRJwaiQVA5iShrwZxX5wBnZIS
azgCz/D6IdVMXilAUFKQX1thi32f3jkylCb/DBzGRROCMgiD5Al+uccy9cm9aS6RLPt06O
qMb9StNGOnkqY8rIHPgaH/RjqDTSJbNab3w+CShlb+H/p9cWGxhIrII+lBTcpCUAIBbPtb
DFv9M3j0SjsMTr2Q0B0OjKENcSKSq1E1m8FDHqgpSY5zzyRi7V/WZxCXbv8lCgk5GWTNmp
NrS7qSjxO0N143zMRDZyEx74aYCx3aFIaIGFXT/EedRQ5l0cy7xVyM4wIIA+XlKR75kZpA
Vj6YYkMDtL86RN6o8u1x3txZv15lMtfG4jzztGwnVQiGscG0CWuUA+E1pGlBwfaswlomVe
oYK9OJJ3hJeJ7SpCt2GGcAAAADAQABAAACAQC0wxW0LfWZ676lWdi9ZjaVynRG57PiyTFY
jMFqSdYvFNfDrARixcx6O+UXrbFjneHA7OKGecqzY63Yr9MCka+meYU2eL+uy57Uq17ZKy
zH/oXYQSJ51rjutu0ihbS1Wo5cv7m2V/IqKdG/WRNgTFzVUxSgbybVMmGwamfMJKNAPZq2
xLUfcemTWb1e97kV0zHFQfSvH9wiCkJ/rivBYmzPbxcVuByU6Azaj2zoeBSh45ALyNL2Aw
HHtqIOYNzfc8rQ0QvVMWuQOdu/nI7cOf8xJqZ9JRCodiwu5fRdtpZhvCUdcSerszZPtwV8
uUr+CnD8RSKpuadc7gzHe8SICp0EFUDX5g4Fa5HqbaInLt3IUFuXW4SHsBPzHqrwhsem8z
tjtgYVDcJR1FEpLfXFOC0eVcu9WiJbDJEIgQJNq3aazd3Ykv8+yOcAcLgp8x7QP+s+Drs6
4/6iYCbWbsNA5ATTFz2K5GswRGsWxh0cKhhpl7z11VWBHrfIFv6z0KEXZ/AXkg9x2w9btc
dr3ASyox5AAJdYwkzPxTjtDQcN5tKVdjR1LRZXZX/IZSrK5+Or8oaBgpG47L7okiw32SSQ
5p8oskhY/He6uDNTS5cpLclcfL5SXH6TZyJxrwtr0FHTlQGAqpBn+Lc3vxrb6nbpx49MPt
DGiG8xK59HAA/c222dwQAAAQEA5vtA9vxS5n16PBE8rEAVgP+QEiPFcUGyawA6gIQGY1It
4SslwwVM8OJlpWdAmF8JqKSDg5tglvGtx4YYFwlKYm9CiaUyu7fqadmncSiQTEkTYvRQcy
tCVFGW0EqxfH7ycA5zC5KGA9pSyTxn4w9hexp6wqVVdlLoJvzlNxuqKnhbxa7ia8vYp/hp
6EWh72gWLtAzNyo6bk2YykiSUQIfHPlcL6oCAHZblZ06Usls2ZMObGh1H/7gvurlnFaJVn
CHcOWIsOeQiykVV/l5oKW1RlZdshBkBXE1KS0rfRLLkrOz+73i9nSPRvZT4xQ5tDIBBXSN
y4HXDjeoV2GJruL7qAAAAQEA/XiMw8fvw6MqfsFdExI6FCDLAMnuFZycMSQjmTWIMP3cNA
2qekJF44lL3ov+etmkGDiaWI5XjUbl1ZmMZB1G8/vk8Y9ysZeIN5DvOIv46c9t55pyIl5+
fWHo7g0DzOw0Z9ccM0lr60hRTm8Gr/Uv4TgpChU1cnZbo2TNld3SgVwUJFxxa//LkX8HGD
vf2Z8wDY4Y0QRCFnHtUUwSPiS9GVKfQFb6wM+IAcQv5c1MAJlufy0nS0pyDbxlPsc9HEe8
EXS1EDnXGjx1EQ5SJhmDmO1rL1Ien1fVnnibuiclAoqCJwcNnw/qRv3ksq0gF5lZsb3aFu
kHJpu34GKUVLy74QAAAQEA+UBQH/jO319NgMG5NKq53bXSc23suIIqDYajrJ7h9Gef7w0o
eogDuMKRjSdDMG9vGlm982/B/DWp/Lqpdt+59UsBceN7mH21+2CKn6NTeuwpL8lRjnGgCS
t4rWzFOWhw1IitEg29d8fPNTBuIVktJU/M/BaXfyNyZo0y5boTOELoU3aDfdGIQ7iEwth5
vOVZ1VyxSnhcsREMJNE2U6ETGJMY25MSQytrI9sH93tqWz1CIUEkBV3XsbcjjPSrPGShV/
H+alMnPR1boleRUIge8MtQwoC4pFLtMHRWw6yru3tkRbPBtNPDAZjkwF1zXqUBkC0x5c7y
XvSb8cNlUIWdRwAAAAt0b21ATklYSEFSRAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
#footprinting #enumeration #hacking #nfs #smtp #port111 #port2049 #port25 #smb #mssql #windows

#### assignment

第二台服务器是内部网络中每个人都可以访问的服务器。在与客户的讨论中，我们指出这些服务器通常是攻击者的主要目标之一，应该将此服务器添加到测试范围中。

我们的客户同意了这一点，并将此服务器添加到我们的测试范围内。在这里，目标仍然相同。我们需要尽可能多地了解这台服务器的信息，并找到利用这些信息针对服务器本身的方法。为了证明和保护客户数据，创建了一个名为 `HTB` 的用户。因此，我们需要获取该用户的凭据作为证明。

#### scans

##### general scan

![[mediumlab.html]]
_nmap -sS -sV -sC -A -oA mediumlab_basic_nmap.txt 10.129.202.41_

扫描了 994 个端口但未显示在下方的端口处于 **closed** 状态

- 994 个端口回复了：**reset**

|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
|Port|   |State (toggle closed [0] \| filtered [0])|Service|Reason|Product|Version|Extra info|
|111|tcp|open|rpcbind|syn-ack||2-4|RPC #100000|
||rpcinfo|program version    port/proto  service<br>  100000  2,3,4        111/tcp   rpcbind<br>  100000  2,3,4        111/tcp6  rpcbind<br>  100000  2,3,4        111/udp   rpcbind<br>  100000  2,3,4        111/udp6  rpcbind<br>  100003  2,3         2049/udp   nfs<br>  100003  2,3         2049/udp6  nfs<br>  100003  2,3,4       2049/tcp   nfs<br>  100003  2,3,4       2049/tcp6  nfs<br>  100005  1,2,3       2049/tcp   mountd<br>  100005  1,2,3       2049/tcp6  mountd<br>  100005  1,2,3       2049/udp   mountd<br>  100005  1,2,3       2049/udp6  mountd<br>  100021  1,2,3,4     2049/tcp   nlockmgr<br>  100021  1,2,3,4     2049/tcp6  nlockmgr<br>  100021  1,2,3,4     2049/udp   nlockmgr<br>  100021  1,2,3,4     2049/udp6  nlockmgr<br>  100024  1           2049/tcp   status<br>  100024  1           2049/tcp6  status<br>  100024  1           2049/udp   status<br>  100024  1           2049/udp6  status|   |   |   |   |   |
|135|tcp|open|msrpc|syn-ack|Microsoft Windows RPC|||
|139|tcp|open|netbios-ssn|syn-ack|Microsoft Windows netbios-ssn|||
|445|tcp|open|microsoft-ds|syn-ack||||
|2049|tcp|open|nlockmgr|syn-ack||1-4|RPC #100021|
|3389|tcp|open|ms-wbt-server|syn-ack|Microsoft Terminal Services|||
||rdp-ntlm-info|Target_Name: WINMEDIUM<br>  NetBIOS_Domain_Name: WINMEDIUM<br>  NetBIOS_Computer_Name: WINMEDIUM<br>  DNS_Domain_Name: WINMEDIUM<br>  DNS_Computer_Name: WINMEDIUM<br>  Product_Version: 10.0.17763<br>  System_Time: 2023-09-28T11:34:34+00:00|   |   |   |   |   |
||ssl-date|2023-09-28T11:34:44+00:00; -1s from scanner time.|   |   |   |   |   |
||ssl-cert|Subject: commonName=WINMEDIUM<br>Not valid before: 2023-09-27T11:21:27<br>Not valid after:  2024-03-28T11:21:27|   |   |   |   |   |

远程操作系统检测

- 使用的端口：**111/tcp**（**open**）
- 使用的端口：**1/tcp**（**closed**）
- 使用的端口：**32303/udp**（**closed**）
- 操作系统匹配：**Microsoft Windows Server 2019**（**96%**）
- 操作系统匹配：**Microsoft Windows 10 1709 - 1909**（**93%**）
- 操作系统匹配：**Microsoft Windows Server 2012**（**93%**）
- 操作系统匹配：**Microsoft Windows Vista SP1**（**92%**）
- 操作系统匹配：**Microsoft Windows Longhorn**（**92%**）
- 操作系统匹配：**Microsoft Windows 10 1709 - 1803**（**91%**）
- 操作系统匹配：**Microsoft Windows 10 1809 - 2004**（**91%**）
- 操作系统匹配：**Microsoft Windows Server 2012 R2**（**91%**）
- 操作系统匹配：**Microsoft Windows Server 2012 R2 Update 1**（**91%**）
- 操作系统匹配：**Microsoft Windows Server 2016 build 10586 - 14393**（**91%**）

- 已识别操作系统，但在扫描时请求了指纹。（点击展开）

主机脚本输出

|   |   |
|---|---|
|Script Name|Output|
|smb2-security-mode|3:1:1: <br>    Message signing enabled but not required|
|smb2-time|date: 2023-09-28T11:34:36<br>  start_date: N/A|

路由追踪信息（点击展开）

- 使用端口 22/tcp 生成的路由追踪数据

|   |   |   |   |
|---|---|---|---|
|Hop|Rtt|IP|Host|
|1|698.49|10.10.16.1||
|2|484.61|10.129.202.41||


其他指标（点击展开）

|   |   |
|---|---|
|Metric|Value|
|Ping Results|echo-reply|
|Network Distance|2 hops|
|TCP Sequence Prediction|Difficulty=263 (Good luck!)|
|IP ID Sequence Generation|Randomized|


##### NFS scan
![[mediumlab_nfs.html]]

找到 NFS（Network File System，网络文件系统）共享 /TechSupport


##### SMB scan
![[mediumlab_smb.html]]


### hack

使用以下命令将 /TechSupport 挂载为 NFS 共享

```
sudo mount -t nfs 10.129.202.41:/ ./nfs_share/ -o nolock
```

我可以以 sudo 身份访问挂载，找到**一个**工单"ticket4238791283782.txt"：

 2    host=smtp.web.dev.inlanefreight.htb 👈👈👈👈👈👈👈
 3    #port=25
 4    ssl=true
 5    user="alex"  👈👈👈👈👈👈👈
 6    password="lol123!mD" 👈👈👈👈👈👈👈
 7    from="alex.g@web.dev.inlanefreight.htb" 👈👈👈👈👈👈�
###### ticket4238791283782.txt

与 InlaneFreight Ltd 的对话
于 2021 年 11 月 10 日下午 01:27 伦敦时间 GMT（GMT+0200）开始
01:27 PM | Operator: Hello,.

So what brings you here today?
01:27 PM | alex: hello
01:27 PM | Operator: Hey alex!
01:27 PM | Operator: What do you need help with?
01:36 PM | alex: I run into an issue with the web config file on the system for the smtp server. do you mind to take a look at the config?
01:38 PM | Operator: Of course
01:42 PM | alex: here it is:

 1smtp {
 2    host=smtp.web.dev.inlanefreight.htb 👈👈👈👈👈👈👈
 3    #port=25
 4    ssl=true
 5    user="alex"  👈👈👈👈👈👈👈
 6    password="lol123!mD" 👈👈👈👈👈👈👈
 7    from="alex.g@web.dev.inlanefreight.htb" 👈👈👈👈👈👈👈
 8}
 9
10securesocial {
11
12    onLoginGoTo=/
13    onLogoutGoTo=/login
14    ssl=false
15
16    userpass {
17      withUserNameSupport=false
18      sendWelcomeEmail=true
19      enableGravatarSupport=true
20      signupSkipLogin=true
21      tokenDuration=60
22      tokenDeleteInterval=5
23      minimumPasswordLength=8
24      enableTokenJob=true
25      hasher=bcrypt
26      }
27
28     cookie {
29     #       name=id
30     #       path=/login
31     #       domain="10.129.2.59:9500"
32            httpOnly=true
33            makeTransient=false
34            absoluteTimeoutInMinutes=1440
35            idleTimeoutInMinutes=1440
36    }

##### SMB
看来我们需要继续使用 ~~smtp~~ SMB（Server Message Block，服务器消息块协议），使用上述凭据（alex/lol123!mD）

我使用以下命令列出共享

```
smbclient -U alex -L 10.129.202.41
```

-->
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        devshare        Disk
        IPC$            IPC       Remote IPC
        Users           Disk

devshare 看起来很有趣

```
smblient -U alex //10.129.202.41/devshare
```

我们找到了"important.txt"：

*sa:87N1ns@slls83*  这是什么？MSSQL！

Domain Name: INFREIGHT

我们可以使用以下命令 rdp 连接到该 IP

```
xfreerdp /u:alex /p:'lol123!mD' /v:10.129.202.41
```
Windows 主机上的 Administrator 与"sa"使用相同的密码，即 87N1ns@slls83

我以"Administrator"身份启动 MS SQL Studio，使用"Windows 身份验证"登录 MSSQL。

编辑数据库的最后 200 条记录，找到用户 HTB

![[Screenshot_2023-08-13_16_33_55 1.png]]



#enumeration #footprinting #hacking

--> [[notes about footprinting]]
# 枚举原则

---

枚举（Enumeration）是网络安全中广泛使用的术语。它代表使用主动（扫描）和被动（使用第三方提供商）方法收集信息。需要注意的是，OSINT（Open Source Intelligence，开源情报）是一个独立的过程，应该与枚举分开进行，因为 `OSINT 完全基于被动信息收集`，不涉及对给定目标的主动枚举。枚举是一个循环过程，我们根据已有或已发现的数据反复收集信息。

信息可以从域名、IP 地址、可访问的服务以及许多其他来源收集。

一旦我们在客户的基础设施中确定了目标，我们需要检查各个服务和协议。在大多数情况下，这些是实现客户、基础设施、管理人员和员工之间通信的服务。

如果我们设想自己被聘请来调查一家公司的 IT 安全，我们将开始对公司的功能建立一个总体理解。例如，我们需要了解公司的结构、使用哪些服务和第三方供应商、可能采取了哪些安全措施等等。这个阶段可能会被误解，因为大多数人只关注明显的东西，试图强行进入公司的系统，而不是理解基础设施是如何建立的，以及提供特定服务需要哪些技术方面和服务。

这种错误方法的一个例子是：在发现 SSH、RDP、WinRM 等身份验证服务后，我们尝试使用常见/弱密码和用户名进行暴力破解。不幸的是，暴力破解是一种嘈杂的方法，很容易导致被加入黑名单，使进一步测试变得不可能。这主要发生在我们不了解公司的防御安全措施及其基础设施的情况下。有些人可能会对这种方法微笑，但经验表明，太多的测试人员采取这种方法。

`我们的目标不是进入系统，而是找到所有进入的方法。`

我们可以把这比作一个寻宝者为探险做准备。他不会只是拿起铲子在某个随机的地方开始挖掘，而是会计划并准备装备，研究地图，了解他必须覆盖的地形以及宝藏可能在哪里，这样他就可以带上合适的工具。如果他到处挖洞，他会造成损害，浪费时间和精力，而且很可能永远无法实现目标。同样的道理也适用于理解公司的内部和外部基础设施，绘制其地图，并仔细制定我们的攻击计划。

枚举原则基于一些问题，这些问题将有助于我们在任何可能的情况下进行所有调查。在大多数情况下，许多渗透测试人员的主要关注点是他们能看到什么，而不是他们看不到什么。然而，即使是我们看不到的东西也与我们相关，可能非常重要。这里的区别在于，我们开始通过经验看到那些乍一看不可见的组件和方面。

- 我们能看到什么？
- 我们看到它的原因是什么？
- 我们所看到的为我们创造了什么画面？
- 我们从中获得什么？
- 我们如何利用它？
- 我们看不到什么？
- 我们看不到的原因可能是什么？
- 我们看不到的东西为我们呈现什么画面？

这里必须注意的一个重要方面是，规则总有例外。然而，原则不会改变。这些原则的另一个优势是，我们可以从实际任务中看到，当我们突然不知道如何继续时，我们缺乏的不是渗透测试能力，而是技术理解，因为我们的核心任务不是利用机器，而是找出如何利用它们。

|**`序号`**|**`原则`**|
|---|---|
|1.|眼见不一定为实。考虑所有观点。|
|2.|区分我们所见和我们所不见。|
|3.|总有方法获取更多信息。理解目标。|

为了熟悉这些原则，我们应该把这些问题和原则写在我们随时可以看到并轻松参考的地方。#enumeration #hacking #footprinting

source: https://academy.hackthebox.com/module/112/section/1185
--> [[notes about footprinting]]

# 枚举方法论

---

复杂的过程必须有标准化的方法论，帮助我们保持方向，避免因疏忽而遗漏任何方面。特别是考虑到目标系统可能提供的各种情况，我们的方法设计几乎是不可预测的。因此，大多数渗透测试人员遵循他们的习惯和他们感到最舒适和熟悉的步骤。然而，这不是标准化的方法论，而是基于经验的方法。

我们知道渗透测试，因此枚举，是一个动态过程。因此，我们为外部和内部渗透测试开发了一个静态枚举方法论，其中包含自由动态，允许对给定环境进行广泛的更改和调整。这个方法论嵌套在 6 个层次中，比喻地说，代表了我们试图通过枚举过程穿越的边界。整个枚举过程分为三个不同的级别：

|`基础设施枚举`|`主机枚举`|`操作系统枚举`|
|---|---|---|

![image](https://academy.hackthebox.com/storage/modules/112/enum-method3.png)

注意：每个层次显示的组件代表主要类别，而不是所有要搜索的组件的完整列表。此外，必须在此提及的是，第一层和第二层（互联网存在、网关）并不完全适用于内网，如 Active Directory 基础设施。内部基础设施的层次将在其他模块中介绍。

将这些线条想象成某种障碍物，比如一堵墙。我们在这里做的是四处查看，找出入口在哪里，或者我们可以穿过或翻越的缝隙，以便更接近我们的目标。理论上，也可以直接撞墙，但很多时候，我们花费大量努力和时间用力砸开的缝隙并没有给我们带来太多好处，因为在墙的这个位置没有通向下一堵墙的入口。

这些层次设计如下：

|**层次**|**描述**|**信息类别**|
|---|---|---|
|`1. 互联网存在`|识别互联网存在和外部可访问的基础设施。|域名、子域名、虚拟主机、ASN、网络块、IP 地址、云实例、安全措施|
|`2. 网关`|识别保护公司外部和内部基础设施的可能安全措施。|防火墙、DMZ、IPS/IDS、EDR、代理、NAC、网络分段、VPN、Cloudflare|
|`3. 可访问服务`|识别外部或内部托管的可访问接口和服务。|服务类型、功能、配置、端口、版本、接口|
|`4. 进程`|识别与服务相关的内部进程、源和目标。|PID、处理的数据、任务、源、目标|
|`5. 权限`|识别对可访问服务的内部权限和特权。|组、用户、权限、限制、环境|
|`6. 操作系统设置`|识别内部组件和系统设置。|操作系统类型、补丁级别、网络配置、操作系统环境、配置文件、敏感私有文件|

重要说明：为简单起见，人员方面和可通过 OSINT 从员工处获取的信息已从"互联网存在"层中移除。

我们最终可以把整个渗透测试想象成一个迷宫，我们必须识别缝隙并找到尽快有效地进入的方法。这种类型的迷宫可能看起来像这样：

![image](https://academy.hackthebox.com/storage/modules/112/pentest-labyrinth.png)

方块代表缝隙/漏洞。

正如我们可能已经注意到的，我们可以看到我们会遇到一个缝隙，很可能是多个。有趣且非常常见的事实是，并非我们发现的所有缝隙都能让我们进入。所有渗透测试在时间上都是有限的，但我们应该始终记住一个信念，那就是几乎总有一条进入的路。即使在四周的渗透测试之后，我们也不能 100% 说不存在更多漏洞。一个研究公司数月并分析它们的人，很可能比我们在评估期间的几周内获得的对应用程序和结构的理解要深得多。一个很好的最近例子是不久前发生的 [SolarWinds 网络攻击](https://www.rpc.senate.gov/policy-papers/the-solarwinds-cyberattack)。这是方法论必须排除此类情况的另一个极好的理由。

让我们假设我们被要求进行外部"黑盒"渗透测试。一旦所有必要的合同项目完全完成，我们的渗透测试将在指定时间开始。

---

## 第 1 层：互联网存在

我们必须通过的第一层是"互联网存在"层，在这里我们专注于寻找可以调查的目标。如果合同中的范围允许我们寻找其他主机，这一层甚至比只有固定目标更为关键。在这一层，我们使用不同的技术来查找域名、子域名、网络块以及代表公司及其基础设施在互联网上存在的许多其他组件和信息。

`这一层的目标是识别所有可能的目标系统和可测试的接口。`

---

## 第 2 层：网关

在这里，我们尝试理解可达目标的接口，它是如何受保护的，以及它在网络中的位置。由于多样性、不同的功能和一些特定的程序，我们将在其他模块中更详细地介绍这一层。

`目标是理解我们正在处理什么以及我们需要注意什么。`

---

## 第 3 层：可访问服务

对于可访问的服务，我们检查每个目标提供的所有服务。每个服务都有特定的目的，是管理员出于特定原因安装的。每个服务都有某些功能，因此也会产生特定的结果。要有效地使用它们，我们需要知道它们是如何工作的。否则，我们需要学习理解它们。

`这一层的目的是理解目标系统的原因和功能，并获得必要的知识以有效地与其通信并为我们的目的利用它。`

这是我们在本模块中主要处理的枚举部分。

---

## 第 4 层：进程

每次执行命令或函数时，无论是用户输入的还是系统生成的数据都会被处理。这会启动一个必须执行特定任务的进程，而这些任务至少有一个源和一个目标。

`这里的目标是理解这些因素并识别它们之间的依赖关系。`

---

## 第 5 层：权限

每个服务都通过特定用户在特定组中运行，该用户具有管理员或系统定义的权限和特权。这些特权通常为我们提供管理员忽视的功能。这在 Active Directory 基础设施和许多其他特定案例的管理环境和服务器中经常发生，其中用户负责多个管理区域。

`识别这些权限并理解这些权限能做什么和不能做什么是至关重要的。`

---

## 第 6 层：操作系统设置

在这里，我们使用内部访问收集有关实际操作系统及其设置的信息。这为我们提供了系统内部安全性的良好概述，并反映了公司管理团队的技能和能力。

`这里的目标是看管理员如何管理系统，以及我们可以从中收集哪些敏感的内部信息。`

---

## 枚举方法论实践

方法论总结了在给定目标范围内获取知识的所有系统化程序。重要的是要注意，方法论不是逐步指南，而是如定义所暗示的，是系统化程序的总结。在我们的案例中，枚举方法论是探索给定目标的系统化方法。

在这种方法论中如何识别各个组件和获取信息是一个动态和不断增长的方面，它在不断变化，因此可能有所不同。一个很好的例子是使用来自 Web 服务器的信息收集工具。这方面有无数不同的工具，每个工具都有特定的重点，因此提供的结果与其他应用程序不同。然而，目标是相同的。因此，工具和命令的集合不是实际方法论的一部分，而是一个备忘单，我们可以在给定情况下参考其中列出的命令和工具。#enumeration #footprinting #web #hacking
也可参阅 [Website checks for vulns](Website%20checks%20for%20vulns.md)
--> [[notes about footprinting]]

域名信息是任何渗透测试的核心组成部分，它不仅仅涉及子域名，还涉及整个互联网上的存在。因此，我们收集信息并尝试理解公司的功能以及成功高效地提供服务所需的技术和结构。

这类信息是被动收集的，无需直接和主动扫描。换句话说，我们保持隐蔽，以"客户"或"访客"的身份浏览，以避免与可能暴露我们身份的公司建立直接连接。OSINT（开源情报）相关部分只是 OSINT 深度研究的一小部分，仅描述了通过这种方式获取信息的众多方法中的几种。更多方法和策略可以在 [OSINT: Corporate Recon](https://academy.hackthebox.com/course/preview/osint-corporate-recon) 模块中找到。

然而，在`被动`收集信息时，我们可以使用第三方服务来更好地了解公司。但是，我们首先应该做的是仔细审查公司的`主网站`。然后，我们应该阅读文本内容，同时记住这些服务需要哪些技术和结构。

例如，许多IT公司根据其行业提供应用开发、物联网、托管、数据科学和IT安全服务。如果我们遇到以前很少接触的服务，有必要深入了解它，弄清楚它由哪些活动组成以及有哪些可用的机会。这些服务也让我们对公司的结构有了很好的了解。

例如，这部分是枚举`第一原则`和`第二原则`的结合。我们关注我们`看到的`和`看不到的`。我们看到了服务但看不到它们的功能。然而，服务与提供服务所必需的某些技术方面相关联。因此，我们采用开发者的视角，从他们的角度来看待整个事情。这种视角使我们能够获得关于功能的许多技术见解。

---

## 在线存在

一旦我们对公司及其服务有了基本了解，我们就可以对其在互联网上的存在有一个初步印象。假设一家中型公司雇用我们从黑盒（black-box）角度测试他们的整个基础设施。这意味着我们只收到了目标范围，必须自己获取所有进一步的信息。

注意：请记住，以下示例将与实际练习不同，不会给出相同的结果。然而，这些示例基于真实的渗透测试，说明了如何以及可以获取哪些信息。

互联网上的第一个存在点可能是我们可以检查的公司主网站的 `SSL 证书`。通常，这样的证书不仅包含一个子域名，这意味着该证书用于多个域名，而且这些域名很可能仍然是活跃的。

![](https://academy.hackthebox.com/storage/modules/112/DomInfo-1.png)

另一个查找更多子域名的来源是 [crt.sh](https://crt.sh/)。这个来源是[证书透明度](https://en.wikipedia.org/wiki/Certificate_Transparency)日志。证书透明度（Certificate Transparency）是一个旨在实现对加密互联网连接所颁发数字证书进行验证的过程。该标准 ([RFC 6962](https://tools.ietf.org/html/rfc6962)) 规定将证书颁发机构颁发的所有数字证书记录在可审计的日志中。这旨在能够检测域名的虚假或恶意颁发的证书。SSL 证书提供商如 [Let's Encrypt](https://letsencrypt.org/) 与 Web 界面 [crt.sh](https://crt.sh/) 共享此信息，后者将新条目存储在数据库中以供后续访问。

![](https://academy.hackthebox.com/storage/modules/112/DomInfo-2.png)

我们还可以以 JSON 格式输出结果。

#### 证书透明度

Certificate Transparency

```shell-session
tr01ax@htb[/htb]$ curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq .

[
  {
    "issuer_ca_id": 23451835427,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "matomo.inlanefreight.com",
    "name_value": "matomo.inlanefreight.com",
    "id": 50815783237226155,
    "entry_timestamp": "2021-08-21T06:00:17.173",
    "not_before": "2021-08-21T05:00:16",
    "not_after": "2021-11-19T05:00:15",
    "serial_number": "03abe9017d6de5eda90"
  },
  {
    "issuer_ca_id": 6864563267,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "matomo.inlanefreight.com",
    "name_value": "matomo.inlanefreight.com",
    "id": 5081529377,
    "entry_timestamp": "2021-08-21T06:00:16.932",
    "not_before": "2021-08-21T05:00:16",
    "not_after": "2021-11-19T05:00:15",
    "serial_number": "03abe90104e271c98a90"
  },
  {
    "issuer_ca_id": 113123452,
    "issuer_name": "C=US, O=Let's Encrypt, CN=R3",
    "common_name": "smartfactory.inlanefreight.com",
    "name_value": "smartfactory.inlanefreight.com",
    "id": 4941235512141012357,
    "entry_timestamp": "2021-07-27T00:32:48.071",
    "not_before": "2021-07-26T23:32:47",
    "not_after": "2021-10-24T23:32:45",
    "serial_number": "044bac5fcc4d59329ecbbe9043dd9d5d0878"
  },
  { ... SNIP ...
```

如果需要，我们还可以按唯一子域名进行过滤。

Certificate Transparency

```shell-session
tr01ax@htb[/htb]$ curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u

account.ttn.inlanefreight.com
blog.inlanefreight.com
bots.inlanefreight.com
console.ttn.inlanefreight.com
ct.inlanefreight.com
data.ttn.inlanefreight.com
*.inlanefreight.com
inlanefreight.com
integrations.ttn.inlanefreight.com
iot.inlanefreight.com
mails.inlanefreight.com
marina.inlanefreight.com
marina-live.inlanefreight.com
matomo.inlanefreight.com
next.inlanefreight.com
noc.ttn.inlanefreight.com
preview.inlanefreight.com
shop.inlanefreight.com
smartfactory.inlanefreight.com
ttn.inlanefreight.com
vx.inlanefreight.com
www.inlanefreight.com
```

接下来，我们可以识别可从互联网直接访问且不由第三方提供商托管的主机。这是因为如果没有第三方提供商的许可，我们不被允许测试其主机。

#### 公司托管的服务器

Company Hosted Servers

```shell-session
tr01ax@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done

blog.inlanefreight.com 10.129.24.93
inlanefreight.com 10.129.27.33
matomo.inlanefreight.com 10.129.127.22
www.inlanefreight.com 10.129.127.33
s3-website-us-west-2.amazonaws.com 10.129.95.250
```

一旦我们看到哪些主机可以进一步调查，我们就可以通过对 `cut` 命令进行少量调整来生成 IP 地址列表，并通过 `Shodan` 运行它们。

[Shodan](https://www.shodan.io/) 可用于查找永久连接到互联网的设备和系统，如`物联网`（`IoT`，Internet of Things）。它在互联网上搜索开放的 TCP/IP 端口，并根据特定术语和标准过滤系统。例如，搜索开放的 HTTP 或 HTTPS 端口以及其他服务器端口，如 `FTP`、`SSH`、`SNMP`、`Telnet`、`RTSP` 或 `SIP`。因此，我们可以找到设备和系统，如`监控摄像头`、`服务器`、`智能家居系统`、`工业控制器`、`交通灯`和`交通控制器`，以及各种网络组件。

#### Shodan - IP 列表

Shodan - IP List

```shell-session
tr01ax@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 >> ip-addresses.txt;done
tr01ax@htb[/htb]$ for i in $(cat ip-addresses.txt);do shodan host $i;done

10.129.24.93
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-09-01T09:02:11.370085
Number of open ports:    2

Ports:
     80/tcp nginx
    443/tcp nginx

10.129.27.33
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-08-30T22:25:31.572717
Number of open ports:    3

Ports:
     22/tcp OpenSSH (7.6p1 Ubuntu-4ubuntu0.3)
     80/tcp nginx
    443/tcp nginx
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, -TLSv1.3, TLSv1.2
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2

10.129.27.22
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-09-01T15:39:55.446281
Number of open ports:    8

Ports:
     25/tcp
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2, TLSv1.3
     53/tcp
     53/udp
     80/tcp Apache httpd
     81/tcp Apache httpd
    110/tcp
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2
    111/tcp
    443/tcp Apache httpd
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, TLSv1.2, TLSv1.3
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2
                Fingerprint:   RFC3526/Oakley Group 14
    444/tcp

10.129.27.33
City:                    Berlin
Country:                 Germany
Organization:            InlaneFreight
Updated:                 2021-08-30T22:25:31.572717
Number of open ports:    3

Ports:
     22/tcp OpenSSH (7.6p1 Ubuntu-4ubuntu0.3)
     80/tcp nginx
    443/tcp nginx
        |-- SSL Versions: -SSLv2, -SSLv3, -TLSv1, -TLSv1.1, -TLSv1.3, TLSv1.2
        |-- Diffie-Hellman Parameters:
                Bits:          2048
                Generator:     2
```

我们记住 IP `10.129.27.22`（`matomo.inlanefreight.com`）以便后续进行主动调查。现在，我们可以显示所有可用的 DNS 记录，在那里我们可能会找到更多主机。

#### DNS 记录

DNS Records

```shell-session
tr01ax@htb[/htb]$ dig any inlanefreight.com

; <<>> DiG 9.16.1-Ubuntu <<>> any inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52058
;; flags: qr rd ra; QUERY: 1, ANSWER: 17, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;inlanefreight.com.             IN      ANY

;; ANSWER SECTION:
inlanefreight.com.      300     IN      A       10.129.27.33
inlanefreight.com.      300     IN      A       10.129.95.250
inlanefreight.com.      3600    IN      MX      1 aspmx.l.google.com.
inlanefreight.com.      3600    IN      MX      10 aspmx2.googlemail.com.
inlanefreight.com.      3600    IN      MX      10 aspmx3.googlemail.com.
inlanefreight.com.      3600    IN      MX      5 alt1.aspmx.l.google.com.
inlanefreight.com.      3600    IN      MX      5 alt2.aspmx.l.google.com.
inlanefreight.com.      21600   IN      NS      ns.inwx.net.
inlanefreight.com.      21600   IN      NS      ns2.inwx.net.
inlanefreight.com.      21600   IN      NS      ns3.inwx.eu.
inlanefreight.com.      3600    IN      TXT     "MS=ms92346782372"
inlanefreight.com.      21600   IN      TXT     "atlassian-domain-verification=IJdXMt1rKCy68JFszSdCKVpwPN"
inlanefreight.com.      3600    IN      TXT     "google-site-verification=O7zV5-xFh_jn7JQ31"
inlanefreight.com.      300     IN      TXT     "google-site-verification=bow47-er9LdgoUeah"
inlanefreight.com.      3600    IN      TXT     "google-site-verification=gZsCG-BINLopf4hr2"
inlanefreight.com.      3600    IN      TXT     "logmein-verification-code=87123gff5a479e-61d4325gddkbvc1-b2bnfghfsed1-3c789427sdjirew63fc"
inlanefreight.com.      300     IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.24.8 ip4:10.129.27.2 ip4:10.72.82.106 ~all"
inlanefreight.com.      21600   IN      SOA     ns.inwx.net. hostmaster.inwx.net. 2021072600 10800 3600 604800 3600

;; Query time: 332 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mi Sep 01 18:27:22 CEST 2021
;; MSG SIZE  rcvd: 940
```

让我们看看我们在这里学到了什么，并回到我们的原则。我们看到一条 IP 记录、一些邮件服务器、一些 DNS 服务器、TXT 记录和一条 SOA（起始授权）记录。

- `A` 记录：我们通过 A 记录识别指向特定（子）域名的 IP 地址。这里我们只看到一个我们已经知道的。

- `MX` 记录：邮件服务器记录显示哪个邮件服务器负责管理公司的电子邮件。由于在我们的案例中这由 Google 处理，我们应该记下这一点并暂时跳过。

- `NS` 记录：这类记录显示使用哪些名称服务器将 FQDN（完全限定域名，Fully Qualified Domain Name）解析为 IP 地址。大多数托管提供商使用自己的名称服务器，这使得识别托管提供商更加容易。

- `TXT` 记录：这种类型的记录通常包含不同第三方提供商的验证密钥以及 DNS 的其他安全方面，如 [SPF](https://datatracker.ietf.org/doc/html/rfc7208)（发送方策略框架，Sender Policy Framework）、[DMARC](https://datatracker.ietf.org/doc/html/rfc7489)（基于域的消息认证报告和一致性）和 [DKIM](https://datatracker.ietf.org/doc/html/rfc6376)（域名密钥识别邮件），它们负责验证和确认发送的电子邮件的来源。如果我们仔细查看结果，已经可以看到一些有价值的信息。


DNS Records

```shell-session
...SNIP... TXT     "MS=ms92346782372"
...SNIP... TXT     "atlassian-domain-verification=IJdXMt1rKCy68JFszSdCKVpwPN"
...SNIP... TXT     "google-site-verification=O7zV5-xFh_jn7JQ31"
...SNIP... TXT     "google-site-verification=bow47-er9LdgoUeah"
...SNIP... TXT     "google-site-verification=gZsCG-BINLopf4hr2"
...SNIP... TXT     "logmein-verification-code=87123gff5a479e-61d4325gddkbvc1-b2bnfghfsed1-3c789427sdjirew63fc"
...SNIP... TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.24.8 ip4:10.129.27.2 ip4:10.72.82.106 ~all"
```

到目前为止，我们看到的是 DNS 服务器上的条目，乍一看并不是很有趣（除了额外的 IP 地址）。然而，我们无法一眼看出显示的条目背后的第三方提供商。我们现在能看到的核心信息是：

||||
|---|---|---|
|[Atlassian](https://www.atlassian.com/)|[Google Gmail](https://www.google.com/gmail/)|[LogMeIn](https://www.logmein.com/)|
|[Mailgun](https://www.mailgun.com/)|[Outlook](https://outlook.live.com/owa/)|[INWX](https://www.inwx.com/en) ID/用户名|
|10.129.24.8|10.129.27.2|10.72.82.106|

例如，[Atlassian](https://www.atlassian.com/) 表明该公司使用此解决方案进行软件开发和协作。如果我们不熟悉这个平台，可以免费试用以熟悉它。

[Google Gmail](https://www.google.com/gmail/) 表明 Google 被用于电子邮件管理。因此，这也可能表明我们可以通过链接访问开放的 GDrive 文件夹或文件。

[LogMeIn](https://www.logmein.com/) 是一个在许多不同级别上规范和管理远程访问的中心位置。然而，这种操作的集中化是一把双刃剑。如果以管理员身份访问此平台（例如，通过密码重用），也将完全访问所有系统和信息。

[Mailgun](https://www.mailgun.com/) 提供多个电子邮件 API、SMTP 中继和 Webhook，可以用来管理电子邮件。这告诉我们要留意 API 接口，然后我们可以测试各种漏洞，如 IDOR（不安全的直接对象引用，Insecure Direct Object Reference）、SSRF（服务器端请求伪造，Server-Side Request Forgery）、POST、PUT 请求以及许多其他攻击。

[Outlook](https://outlook.live.com/owa/) 是文档管理的另一个指标。公司经常使用 Office 365 与 OneDrive 以及 Azure blob 和文件存储等云资源。Azure 文件存储可能非常有趣，因为它使用 SMB 协议工作。

我们看到的最后一个是 [INWX](https://www.inwx.com/en)。这家公司似乎是一个可以购买和注册域名的托管提供商。带有"MS"值的 TXT 记录通常用于确认域名。在大多数情况下，它类似于用于登录管理平台的用户名或 ID。#cloud #enumeration #footprinting #hacking #web
[source](https://academy.hackthebox.com/module/112/section/1062)
--> [[notes about footprinting]]
# 云资源

---

云的使用，如 [AWS](https://aws.amazon.com/)、[GCP](https://cloud.google.com/)、[Azure](https://azure.microsoft.com/en-us/) 等，现在是许多公司的重要组成部分。毕竟，所有公司都希望能够在任何地方工作，因此他们需要一个用于所有管理的中心点。这就是为什么来自 `Amazon`（`AWS`）、`Google`（`GCP`）和 `Microsoft`（`Azure`）的服务非常适合此目的。

即使云提供商集中保护其基础设施，这并不意味着公司没有漏洞。管理员所做的配置仍然可能使公司的云资源易受攻击。这通常从 `S3 存储桶`（AWS）、`blobs`（Azure）、`云存储`（GCP）开始，如果配置不正确，可以在没有身份验证的情况下访问。

#### 公司托管的服务器

Company Hosted Servers

```shell-session
tr01ax@htb[/htb]$ for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done

blog.inlanefreight.com 10.129.24.93
inlanefreight.com 10.129.27.33
matomo.inlanefreight.com 10.129.127.22
www.inlanefreight.com 10.129.127.33
s3-website-us-west-2.amazonaws.com 10.129.95.250
```

当其他员工将云存储用于管理目的时，通常会将其添加到 DNS 列表中。这一步骤使员工更容易访问和管理它们。让我们继续这个案例，一家公司与我们签订了合同，在 IP 查找期间，我们已经看到一个 IP 地址属于 `s3-website-us-west-2.amazonaws.com` 服务器。

然而，有许多不同的方法可以找到这样的云存储。最简单和最常用的方法之一是结合 Google Dorks 进行 Google 搜索。例如，我们可以使用 Google Dorks `inurl:` 和 `intext:` 将搜索范围缩小到特定术语。在下面的示例中，我们看到红色审查区域包含公司名称。

#### Google 搜索 AWS

![](https://academy.hackthebox.com/storage/modules/112/gsearch1.png)

#### Google 搜索 Azure

![](https://academy.hackthebox.com/storage/modules/112/gsearch2.png)

在这里我们已经可以看到 Google 呈现的链接包含 PDF。当我们搜索一家我们可能已经知道或想要了解的公司时，我们还会遇到其他文件，如文本文档、演示文稿、代码等。

此类内容通常也包含在网页的源代码中，从中加载图像、JavaScript 代码或 CSS。此过程通常会减轻 Web 服务器的负担，并且不会存储不必要的内容。

#### 目标网站 - 源代码

![](https://academy.hackthebox.com/storage/modules/112/cloud3.png)

第三方提供商如 [domain.glass](https://domain.glass) 也可以告诉我们很多关于公司基础设施的信息。作为一个积极的副作用，我们还可以看到 Cloudflare 的安全评估状态已被归类为"安全"。这意味着我们已经发现了一个可以为第二层（网关）记录的安全措施。

#### Domain.Glass 结果

![](https://academy.hackthebox.com/storage/modules/112/cloud1.png)

另一个非常有用的提供商是 [GrayHatWarfare](https://buckets.grayhatwarfare.com)。我们可以进行许多不同的搜索，发现 AWS、Azure 和 GCP 云存储，甚至可以按文件格式排序和过滤。因此，一旦我们通过 Google 找到它们，我们也可以在 GrayHatWarefare 上搜索它们，并被动地发现给定云存储上存储了哪些文件。

#### GrayHatWarfare 结果

![](https://academy.hackthebox.com/storage/modules/112/cloud2.png)

许多公司还使用公司名称的缩写，然后在 IT 基础设施中相应使用。这些术语也是发现公司新云存储的绝佳方法的一部分。我们还可以同时搜索文件，以查看可以同时访问的文件。

#### 泄露的私有和公共 SSH 密钥

![](https://academy.hackthebox.com/storage/modules/112/ghw1.png)

有时当员工工作过度或压力过大时，错误可能对整个公司都是致命的。这些错误甚至可能导致 SSH 私钥被泄露，任何人都可以下载并登录到公司的一台或多台机器而无需使用密码。

#### SSH 私钥

![](https://academy.hackthebox.com/storage/modules/112/ghw2.png)#enumeration #footprinting #web #hacking
[source](https://academy.hackthebox.com/module/112/section/1065)
--> [[notes about footprinting]]
# 员工信息

---

在社交媒体平台上搜索和识别员工也可以揭示很多关于团队基础设施和组成的信息。这反过来可以让我们识别正在使用的技术、编程语言，甚至软件应用程序。在很大程度上，我们还可以根据他们的技能评估每个人的关注点。与他人分享的帖子和材料也是该人目前正在从事什么以及该人目前认为与他人分享什么很重要的重要指标。

员工可以在各种商业网络上被识别，如 [LinkedIn](https://www.linkedin.com) 或 [Xing](https://www.xing.de)。公司的招聘信息也可以告诉我们很多关于他们基础设施的信息，并为我们提供应该寻找什么的线索。

#### LinkedIn - 职位发布

Code: txt

```txt
Required Skills/Knowledge/Experience:

* 3-10+ years of experience on professional software development projects.

« An active US Government TS/SCI Security Clearance (current SSBI) or eligibility to obtain TS/SCI within nine months.
« Bachelor's degree in computer science/computer engineering with an engineering/math focus or another equivalent field of discipline.
« Experience with one or more object-oriented languages (e.g., Java, C#, C++).
« Experience with one or more scripting languages (e.g., Python, Ruby, PHP, Perl).
« Experience using SQL databases (e.g., PostgreSQL, MySQL, SQL Server, Oracle).
« Experience using ORM frameworks (e.g., SQLAIchemy, Hibernate, Entity Framework).
« Experience using Web frameworks (e.g., Flask, Django, Spring, ASP.NET MVC).
« Proficient with unit testing and test frameworks (e.g., pytest, JUnit, NUnit, xUnit).
« Service-Oriented Architecture (SOA)/microservices & RESTful API design/implementation.
« Familiar and comfortable with Agile Development Processes.
« Familiar and comfortable with Continuous Integration environments.
« Experience with version control systems (e.g., Git, SVN, Mercurial, Perforce).

Desired Skills/Knowledge/ Experience:

« CompTIA Security+ certification (or equivalent).
« Experience with Atlassian suite (Confluence, Jira, Bitbucket).
« Algorithm Development (e.g., Image Processing algorithms).
« Software security.
« Containerization and container orchestration (Docker, Kubernetes, etc.)
« Redis.
« NumPy.
```

从这样的职位发布中，我们可以看到，例如，首选哪些编程语言：`Java、C#、C++、Python、Ruby、PHP、Perl`。它还要求申请人熟悉不同的数据库，如：`PostgreSQL、MySQL 和 Oracle`。此外，我们知道用于 Web 应用程序开发的不同框架，如：`Flask、Django、ASP.NET、Spring`。

此外，我们使用 `REST API、Github、SVN 和 Perforce`。职位描述还表明该公司使用 Atlassian 套件，因此可能有我们可能访问的资源。我们可以从职业历史中看到一些技能和项目，这使我们对员工的知识有一个合理的估计。

#### LinkedIn - 员工 #1 简介

![](https://academy.hackthebox.com/storage/modules/112/linkedin-pers2.png)

我们尝试在社交媒体网站上建立业务联系，并向访问者证明我们带来了哪些技能，这不可避免地导致我们与公众分享我们所知道的以及我们迄今为止学到的东西。公司总是雇用他们可以使用并应用于业务的技能的员工。例如，我们知道 Flask 和 Django 是 Python 编程语言的 Web 框架。

如果我们搜索一下 Django 安全配置错误，最终会找到以下 [Github 仓库](https://github.com/boomcamp/django-security)，描述了 Django 的 OWASP Top10。我们可以使用它来理解 Django 的内部结构及其工作原理。最佳实践也经常告诉我们要寻找什么。因为许多人盲目相信它们，甚至按照说明中所示的方式命名许多文件。

#### Github

![](https://academy.hackthebox.com/storage/modules/112/github.png)

![](https://academy.hackthebox.com/storage/modules/112/github2.png)

展示我们的项目当然可以大大增加建立新业务联系甚至可能获得新工作的优势，但另一方面，它可能导致很难修复的错误。例如，在其中一个文件中，我们可以发现员工的个人电子邮件地址，经过深入调查，Web 应用程序中有一个硬编码的 [JWT token](https://jwt.io/)（JSON Web Token，JSON Web 令牌）。

#### LinkedIn - 员工 #2 职业生涯

![](https://academy.hackthebox.com/storage/modules/112/linkedin-pers1.png)

[LinkedIn](https://www.linkedin.com) 提供全面的搜索功能，按联系人、地点、公司、学校、行业、个人资料语言、服务、姓名、头衔等排序。可以理解的是，我们在那里提供的详细信息越多，得到的结果就越少。因此，我们应该仔细考虑执行搜索的目的。

假设我们试图找到公司最可能使用的基础设施和技术。我们应该寻找在开发和安全领域工作的技术员工。因为基于安全领域和在该领域工作的员工，我们也将能够确定公司采取了哪些安全措施来保护自己。

##### 目录

###### 简介

###### 基于基础设施的枚举

###### 基于主机的枚举

###### 远程管理协议

###### 技能评估

##### 我的工作站

OFFLINE

/ 1 spawns left#ftp #enumeration #footprinting #hacking  #port21
[source](https://academy.hackthebox.com/module/112/section/1066)
--> [[notes about footprinting]]

# FTP

---

`文件传输协议`（`FTP`，File Transfer Protocol）是互联网上最古老的协议之一。FTP 在 TCP/IP 协议栈的应用层内运行。因此，它与 `HTTP` 或 `POP` 在同一层。这些协议也与浏览器或电子邮件客户端一起工作来执行其服务。文件传输协议还有专门的 FTP 程序。

让我们想象一下，我们想使用 [FTP](https://datatracker.ietf.org/doc/html/rfc959) 协议将本地文件上传到服务器并下载其他文件。在 FTP 连接中，会打开两个通道。首先，客户端和服务器通过 `TCP 端口 21` 建立控制通道。客户端向服务器发送命令，服务器返回状态代码。然后两个通信参与者可以通过 `TCP 端口 20` 建立数据通道。此通道专门用于数据传输，协议在此过程中监视错误。如果传输过程中连接中断，在重新建立联系后可以恢复传输。

区分`主动`和`被动` FTP。在主动变体中，客户端如所述通过 TCP 端口 21 建立连接，从而通知服务器客户端侧的哪个端口服务器可以传输其响应。然而，如果防火墙保护客户端，服务器无法回复，因为所有外部连接都被阻止。为此，开发了`被动模式`。在这里，服务器宣布一个端口，客户端可以通过该端口建立数据通道。由于在此方法中是客户端发起连接，防火墙不会阻止传输。

FTP 有不同的[命令](https://www.smartfile.com/blog/the-ultimate-ftp-commands-list/)和状态代码。并非所有这些命令都在服务器上一致实现。例如，客户端指示服务器端上传或下载文件、组织目录或删除文件。服务器在每种情况下都用状态代码响应，指示命令是否成功执行。可能的状态代码列表可以在[这里](https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes)找到。

通常，我们需要凭据才能在服务器上使用 FTP。我们还需要知道 FTP 是一种`明文`协议，如果网络条件合适，有时可以被嗅探。然而，也有可能服务器提供`匿名 FTP`。服务器运营商然后允许任何用户通过 FTP 上传或下载文件而无需使用密码。由于此类公共 FTP 服务器存在安全风险，用户的选项通常受到限制。

---

## TFTP

`简单文件传输协议`（`TFTP`，Trivial File Transfer Protocol）比 FTP 更简单，在客户端和服务器进程之间执行文件传输。然而，它`不`提供用户身份验证和 FTP 支持的其他有价值的功能。此外，虽然 FTP 使用 TCP，但 TFTP 使用 `UDP`，使其成为不可靠的协议，导致它使用 UDP 辅助的应用层恢复。

这反映在这样一个事实上，即与 FTP 不同，TFTP 不需要用户身份验证。它不支持通过密码进行受保护的登录，并仅根据操作系统中文件的读写权限设置访问限制。实际上，这导致 TFTP 仅在与所有用户共享且可全局读写的目录和文件中运行。由于缺乏安全性，与 FTP 不同，TFTP 只能在本地和受保护的网络中使用。

让我们看看 `TFTP` 的一些命令：

|**命令**|**描述**|
|---|---|
|`connect`|设置远程主机，以及可选的端口，用于文件传输。|
|`get`|将文件或一组文件从远程主机传输到本地主机。|
|`put`|将文件或一组文件从本地主机传输到远程主机。|
|`quit`|退出 tftp。|
|`status`|显示 tftp 的当前状态，包括当前传输模式（ascii 或 binary）、连接状态、超时值等。|
|`verbose`|打开或关闭详细模式，该模式在文件传输期间显示附加信息。|

与 FTP 客户端不同，`TFTP` 没有目录列表功能。

---

## 默认配置

在基于 Linux 的发行版上最常用的 FTP 服务器之一是 [vsFTPd](https://security.appspot.com/vsftpd.html)。vsFTPd 的默认配置可以在 `/etc/vsftpd.conf` 中找到，一些设置已经默认预定义。强烈建议在虚拟机上安装 vsFTPd 服务器并仔细查看此配置。

#### 安装 vsFTPd

Install vsFTPd

```shell-session
tr01ax@htb[/htb]$ sudo apt install vsftpd
```

vsFTPd 服务器只是我们可用的少数 FTP 服务器之一。还有许多不同的替代方案，它们还带来了更多的功能和配置选项。我们将使用 vsFTPd 服务器，因为它是一种以简单易懂的方式展示 FTP 服务器配置可能性的绝佳方式，而无需深入了解手册页的细节。如果我们查看 vsFTPd 的配置文件，我们会看到许多被注释或取消注释的选项和设置。然而，配置文件不包含所有可以进行的设置。现有和缺失的设置可以在[手册页](http://vsftpd.beasts.org/vsftpd_conf.html)上找到。
#### vsFTPd 配置文件

vsFTPd 配置文件

```shell-session
tr01ax@htb[/htb]$ cat /etc/vsftpd.conf | grep -v "#"
```

|**设置**|**描述**|
|---|---|
|`listen=NO`|从 inetd 运行还是作为独立守护进程（daemon）运行？|
|`listen_ipv6=YES`|监听 IPv6？|
|`anonymous_enable=NO`|启用匿名访问？|
|`local_enable=YES`|允许本地用户登录？|
|`dirmessage_enable=YES`|当用户进入某些目录时显示活动目录消息？|
|`use_localtime=YES`|使用本地时间？|
|`xferlog_enable=YES`|激活上传/下载的日志记录？|
|`connect_from_port_20=YES`|从端口 20 连接？|
|`secure_chroot_dir=/var/run/vsftpd/empty`|空目录的名称|
|`pam_service_name=vsftpd`|此字符串是 vsftpd 将使用的 PAM（可插拔认证模块）服务的名称。|
|`rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem`|最后三个选项指定用于 SSL 加密连接的 RSA 证书的位置。|
|`rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key`||
|`ssl_enable=NO`||

此外，还有一个名为 `/etc/ftpusers` 的文件我们也需要注意，因为此文件用于拒绝某些用户访问 FTP 服务。在以下示例中，用户 `guest`、`john` 和 `kevin` 不允许登录 FTP 服务，即使他们存在于 Linux 系统上。

#### FTPUSERS

FTPUSERS

```shell-session
tr01ax@htb[/htb]$ cat /etc/ftpusers

guest
john
kevin
```

---

## 危险设置

我们可以在每个 FTP 服务器上进行许多不同的安全相关设置。这些设置可以有多种用途，例如通过防火墙测试连接、测试路由和认证机制。其中一种认证机制是 `anonymous`（匿名）用户。这通常用于允许内部网络中的每个人共享文件和数据，而无需访问彼此的计算机。使用 vsFTPd，可以添加到配置文件中用于匿名登录的[可选设置](http://vsftpd.beasts.org/vsftpd_conf.html)如下所示：

|**设置**|**描述**|
|---|---|
|`anonymous_enable=YES`|允许匿名登录？|
|`anon_upload_enable=YES`|允许匿名用户上传文件？|
|`anon_mkdir_write_enable=YES`|允许匿名用户创建新目录？|
|`no_anon_password=YES`|不要求匿名用户输入密码？|
|`anon_root=/home/username/ftp`|匿名用户的目录。|
|`write_enable=YES`|允许使用 FTP 命令：STOR、DELE、RNFR、RNTO、MKD、RMD、APPE 和 SITE？|

使用标准 FTP 客户端（`ftp`），如果使用了上述设置，我们可以相应地访问 FTP 服务器并使用匿名用户登录。匿名账户的使用可能出现在内部环境和基础设施中，其中所有参与者都是已知的。对这种类型服务的访问可以设置为临时的，或者通过设置来加速文件交换。

一旦我们连接到 vsFTPd 服务器，就会显示带有 FTP 服务器横幅的 `响应代码 220`。通常这个横幅包含 `服务` 的描述甚至是其 `版本`。它还告诉我们 FTP 服务器是什么类型的系统。FTP 服务器最常见的配置之一是允许 `anonymous`（匿名）访问，这不需要合法凭据但可以访问某些文件。即使我们无法下载它们，有时仅仅列出内容就足以产生进一步的想法并记下有助于我们采取另一种方法的信息。

#### 匿名登录

匿名登录

```shell-session
tr01ax@htb[/htb]$ ftp 10.129.14.136

Connected to 10.129.14.136.
220 "Welcome to the HTB Academy vsFTP service."
Name (10.129.14.136:cry0l1t3): anonymous

230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.


ftp> ls

200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
226 Directory send OK.

```

然而，要获得服务器设置的初步概览，我们可以使用以下命令：

#### vsFTPd 状态

vsFTPd 状态

```shell-session
ftp> status

Connected to 10.129.14.136.
No proxy connection.
Connecting using address family: any.
Mode: stream; Type: binary; Form: non-print; Structure: file
Verbose: on; Bell: off; Prompting: on; Globbing: on
Store unique: off; Receive unique: off
Case: off; CR stripping: on
Quote control characters: on
Ntrans: off
Nmap: off
Hash mark printing: off; Use of PORT cmds: on
Tick counter printing: off
```

有些命令应该偶尔使用，因为这些命令会使服务器向我们显示更多可用于我们目的的信息。这些命令包括 `debug` 和 `trace`。

#### vsFTPd 详细输出

vsFTPd 详细输出

```shell-session
ftp> debug

Debugging on (debug=1).


ftp> trace

Packet tracing on.


ftp> ls

---> PORT 10,10,14,4,188,195
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
226 Directory send OK.
```

|**设置**|**描述**|
|---|---|
|`dirmessage_enable=YES`|当用户首次进入新目录时显示消息？|
|`chown_uploads=YES`|更改匿名上传文件的所有权？|
|`chown_username=username`|被授予匿名上传文件所有权的用户。|
|`local_enable=YES`|启用本地用户登录？|
|`chroot_local_user=YES`|将本地用户放入其主目录？|
|`chroot_list_enable=YES`|使用将被放入其主目录的本地用户列表？|

|**设置**|**描述**|
|---|---|
|`hide_ids=YES`|目录列表中的所有用户和组信息将显示为 "ftp"。|
|`ls_recurse_enable=YES`|允许使用递归列表。|

在以下示例中，我们可以看到，如果存在 `hide_ids=YES` 设置，服务的 UID 和 GUID 表示将被覆盖，使我们更难识别这些文件是以什么权限写入和上传的。

#### 隐藏 ID - YES

隐藏 ID - YES

```shell-session
ftp> ls

---> TYPE A
200 Switching to ASCII mode.
ftp: setsockopt (ignored): Permission denied
---> PORT 10,10,14,4,223,101
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 ftp     ftp      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 ftp     ftp         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 ftp     ftp           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 ftp     ftp            0 Sep 15 14:57 testupload.txt
226 Directory send OK.
```

此设置是一项安全功能，用于防止泄露本地用户名。有了用户名，理论上我们可以使用暴力破解（brute-force）攻击来攻击 FTP 和 SSH 等服务以及许多其他服务。然而，在现实中，[fail2ban](https://en.wikipedia.org/wiki/Fail2ban) 解决方案现在是任何基础设施的标准实现，它会记录 IP 地址并在一定数量的登录失败尝试后阻止对基础设施的所有访问。

我们可以用于目的的另一个有用设置是 `ls_recurse_enable=YES`。这通常在 vsFTPd 服务器上设置，以便更好地了解 FTP 目录结构，因为它允许我们一次看到所有可见内容。

#### 递归列表

递归列表

```shell-session
ftp> ls -R

---> PORT 10,10,14,4,222,149
200 PORT command successful. Consider using PASV.
---> LIST -R
150 Here comes the directory listing.
.:
-rw-rw-r--    1 ftp      ftp      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 ftp      ftp         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 ftp      ftp           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 ftp      ftp            0 Sep 15 14:57 testupload.txt

./Clients:
drwx------    2 ftp      ftp          4096 Sep 16 18:04 HackTheBox
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:00 Inlanefreight

./Clients/HackTheBox:
-rw-r--r--    1 ftp      ftp         34872 Sep 16 18:04 appointments.xlsx
-rw-r--r--    1 ftp      ftp        498123 Sep 16 18:04 contract.docx
-rw-r--r--    1 ftp      ftp        478237 Sep 16 18:04 contract.pdf
-rw-r--r--    1 ftp      ftp           348 Sep 16 18:04 meetings.txt

./Clients/Inlanefreight:
-rw-r--r--    1 ftp      ftp         14211 Sep 16 18:00 appointments.xlsx
-rw-r--r--    1 ftp      ftp         37882 Sep 16 17:58 contract.docx
-rw-r--r--    1 ftp      ftp            89 Sep 16 17:58 meetings.txt
-rw-r--r--    1 ftp      ftp        483293 Sep 16 17:59 proposal.pptx

./Documents:
-rw-r--r--    1 ftp      ftp         23211 Sep 16 18:05 appointments-template.xlsx
-rw-r--r--    1 ftp      ftp         32521 Sep 16 18:05 contract-template.docx
-rw-r--r--    1 ftp      ftp        453312 Sep 16 18:05 contract-template.pdf

./Employees:
226 Directory send OK.

```

从这样的 FTP 服务器 `下载` 文件是主要功能之一，以及 `上传` 我们创建的文件。例如，这允许我们使用 LFI（本地文件包含）漏洞让主机执行系统命令。除了我们可以查看、下载和检查的文件之外，还可以使用 FTP 日志进行攻击，导致 `远程命令执行`（`RCE`）。这适用于 FTP 服务以及我们在枚举阶段可以检测到的所有服务。

#### 下载文件

下载文件

```shell-session
ftp> ls

200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxrwxrwx    1 ftp      ftp             0 Sep 16 17:24 Calendar.pptx
drwxrwxrwx    4 ftp      ftp          4096 Sep 16 17:57 Clients
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:05 Documents
drwxrwxrwx    2 ftp      ftp          4096 Sep 16 17:24 Employees
-rwxrwxrwx    1 ftp      ftp            41 Sep 18 15:58 Important Notes.txt
226 Directory send OK.


ftp> get Important\ Notes.txt

local: Important Notes.txt remote: Important Notes.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for Important Notes.txt (41 bytes).
226 Transfer complete.
41 bytes received in 0.00 secs (606.6525 kB/s)


ftp> exit

221 Goodbye.
```

下载文件

```shell-session
tr01ax@htb[/htb]$ ls | grep Notes.txt

'Important Notes.txt'
```

我们还可以一次下载我们有权访问的所有文件和文件夹。如果 FTP 服务器在较大的文件夹结构中有许多不同的文件，这尤其有用。然而，这可能会触发警报，因为公司中通常没有人想要一次下载所有文件和内容。

#### 下载所有可用文件

下载所有可用文件

```shell-session
tr01ax@htb[/htb]$ wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136

--2021-09-19 14:45:58--  ftp://anonymous:*password*@10.129.14.136/
           => '10.129.14.136/.listing'
Connecting to 10.129.14.136:21... connected.
Logging in as anonymous ... Logged in!
==> SYST ... done.    ==> PWD ... done.
==> TYPE I ... done.  ==> CWD not needed.
==> PORT ... done.    ==> LIST ... done.
12.12.1.136/.listing           [ <=>                                  ]     466  --.-KB/s    in 0s

2021-09-19 14:45:58 (65,8 MB/s) - '10.129.14.136/.listing' saved [466]
--2021-09-19 14:45:58--  ftp://anonymous:*password*@10.129.14.136/Calendar.pptx
           => '10.129.14.136/Calendar.pptx'
==> CWD not required.
==> SIZE Calendar.pptx ... done.
==> PORT ... done.    ==> RETR Calendar.pptx ... done.

...SNIP...

2021-09-19 14:45:58 (48,3 MB/s) - '10.129.14.136/Employees/.listing' saved [119]

FINISHED --2021-09-19 14:45:58--
Total wall clock time: 0,03s
Downloaded: 15 files, 1,7K in 0,001s (3,02 MB/s)
```

下载完所有文件后，`wget` 将创建一个以目标 IP 地址命名的目录。所有下载的文件都存储在那里，我们可以在本地检查它们。

下载所有可用文件

```shell-session
tr01ax@htb[/htb]$ tree .

.
└── 10.129.14.136
    ├── Calendar.pptx
    ├── Clients
    │   └── Inlanefreight
    │       ├── appointments.xlsx
    │       ├── contract.docx
    │       ├── meetings.txt
    │       └── proposal.pptx
    ├── Documents
    │   ├── appointments-template.xlsx
    │   ├── contract-template.docx
    │   └── contract-template.pdf
    ├── Employees
    └── Important Notes.txt

5 directories, 9 files
```

接下来，我们可以检查是否有权限将文件上传到 FTP 服务器。特别是对于 Web 服务器，文件通常是同步的，开发人员可以快速访问文件。FTP 通常用于此目的，而且大多数时候，在管理员认为无法被发现的服务器上会发现配置错误。认为内部网络组件无法从外部访问的态度意味着内部系统的加固往往被忽视，导致配置错误。

将文件上传到连接到 Web 服务器的 FTP 服务器的能力增加了直接访问 Web 服务器的可能性，甚至可能获得反向 shell（reverse shell），使我们能够执行内部系统命令，并可能提升我们的权限。

#### 上传文件

上传文件

```shell-session
tr01ax@htb[/htb]$ touch testupload.txt
```

使用 `PUT` 命令，我们可以将当前文件夹中的文件上传到 FTP 服务器。

上传文件

```shell-session
ftp> put testupload.txt

local: testupload.txt remote: testupload.txt
---> PORT 10,10,14,4,184,33
200 PORT command successful. Consider using PASV.
---> STOR testupload.txt
150 Ok to send data.
226 Transfer complete.


ftp> ls

---> TYPE A
200 Switching to ASCII mode.
---> PORT 10,10,14,4,223,101
200 PORT command successful. Consider using PASV.
---> LIST
150 Here comes the directory listing.
-rw-rw-r--    1 1002     1002      8138592 Sep 14 16:54 Calender.pptx
drwxrwxr-x    2 1002     1002         4096 Sep 14 17:03 Clients
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Documents
drwxrwxr-x    2 1002     1002         4096 Sep 14 16:50 Employees
-rw-rw-r--    1 1002     1002           41 Sep 14 16:45 Important Notes.txt
-rw-------    1 1002     133             0 Sep 15 14:57 testupload.txt
226 Directory send OK.

```

---

## 服务足迹分析

使用各种网络扫描器进行足迹分析也是一种方便且广泛使用的方法。这些工具使我们更容易识别不同的服务，即使它们不在标准端口上可访问。用于此目的的最广泛使用的工具之一是 Nmap。Nmap 还带有 [Nmap 脚本引擎](https://nmap.org/book/nse.html)（`NSE`），这是一组为特定服务编写的许多不同脚本。有关 Nmap 和 NSE 功能的更多信息可以在 [使用 Nmap 进行网络枚举](https://academy.hackthebox.com/course/preview/network-enumeration-with-nmap) 模块中找到。我们可以使用下面显示的命令更新这个 NSE 脚本数据库。

#### Nmap FTP 脚本

Nmap FTP 脚本

```shell-session
tr01ax@htb[/htb]$ sudo nmap --script-updatedb

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 13:49 CEST
NSE: Updating rule database.
NSE: Script Database updated successfully.
Nmap done: 0 IP addresses (0 hosts up) scanned in 0.28 seconds
```

所有 NSE 脚本都位于 Pwnbox 的 `/usr/share/nmap/scripts/` 中，但在我们的系统上，我们可以使用简单的命令在系统上找到它们。

Nmap FTP 脚本

```shell-session
tr01ax@htb[/htb]$ find / -type f -name ftp* 2>/dev/null | grep scripts

/usr/share/nmap/scripts/ftp-syst.nse
/usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse
/usr/share/nmap/scripts/ftp-proftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-bounce.nse
/usr/share/nmap/scripts/ftp-libopie.nse
/usr/share/nmap/scripts/ftp-anon.nse
/usr/share/nmap/scripts/ftp-brute.nse
```

正如我们已经知道的，FTP 服务器通常在标准 TCP 端口 21 上运行，我们可以使用 Nmap 进行扫描。我们还对目标 `10.129.14.136` 使用版本扫描（`-sV`）、激进扫描（`-A`）和默认脚本扫描（`-sC`）。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p21 -sC -A 10.129.14.136

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-16 18:12 CEST
Nmap scan report for 10.129.14.136
Host is up (0.00013s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rwxrwxrwx    1 ftp      ftp       8138592 Sep 16 17:24 Calendar.pptx [NSE: writeable]
| drwxrwxrwx    4 ftp      ftp          4096 Sep 16 17:57 Clients [NSE: writeable]
| drwxrwxrwx    2 ftp      ftp          4096 Sep 16 18:05 Documents [NSE: writeable]
| drwxrwxrwx    2 ftp      ftp          4096 Sep 16 17:24 Employees [NSE: writeable]
| -rwxrwxrwx    1 ftp      ftp            41 Sep 16 17:24 Important Notes.txt [NSE: writeable]
|_-rwxrwxrwx    1 ftp      ftp             0 Sep 15 14:57 testupload.txt [NSE: writeable]
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to 10.10.14.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```

默认脚本扫描基于服务的指纹、响应和标准端口。一旦 Nmap 检测到服务，它会依次执行标记的脚本，提供不同的信息。例如，[ftp-anon](https://nmap.org/nsedoc/scripts/ftp-anon.html) NSE 脚本检查 FTP 服务器是否允许匿名访问。如果允许，则为匿名用户呈现 FTP 根目录的内容。

例如，`ftp-syst` 执行 `STAT` 命令，该命令显示有关 FTP 服务器状态的信息。这包括配置以及 FTP 服务器的版本。Nmap 还提供了在网络级别跟踪 NSE 脚本进度的能力，如果我们在扫描中使用 `--script-trace` 选项。这让我们看到 Nmap 发送什么命令、使用什么端口以及从扫描的服务器收到什么响应。

#### Nmap 脚本跟踪

Nmap 脚本跟踪

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p21 -sC -A 10.129.14.136 --script-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 13:54 CEST
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 8 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 16 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 24 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 32 [10.129.14.136:21]
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #1 [10.129.14.136:21] (timeout: 7000ms) EID 42
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #2 [10.129.14.136:21] (timeout: 9000ms) EID 50
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #3 [10.129.14.136:21] (timeout: 7000ms) EID 58
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #4 [10.129.14.136:21] (timeout: 11000ms) EID 66
NSE: TCP 10.10.14.4:54226 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54228 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54230 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54232 > 10.129.14.136:21 | CONNECT
NSOCK INFO [11.4660s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 50 [10.129.14.136:21] (41 bytes): 220 Welcome to HTB-Academy FTP service...
NSOCK INFO [11.4660s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 58 [10.129.14.136:21] (41 bytes): 220 Welcome to HTB-Academy FTP service...
NSE: TCP 10.10.14.4:54228 < 10.129.14.136:21 | 220 Welcome to HTB-Academy FTP service.
```

扫描历史显示有四个不同的并行扫描正在针对该服务运行，具有不同的超时时间。对于 NSE 脚本，我们看到我们的本地机器使用其他输出端口（`54226`、`54228`、`54230`、`54232`），并首先使用 `CONNECT` 命令发起连接。从服务器的第一个响应中，我们可以看到我们从目标 FTP 服务器接收到发送到我们第二个 NSE 脚本（`54228`）的横幅。如有必要，我们当然可以使用其他应用程序如 `netcat` 或 `telnet` 与 FTP 服务器交互。

#### 服务交互

服务交互

```shell-session
tr01ax@htb[/htb]$ nc -nv 10.129.14.136 21
```

服务交互

```shell-session
tr01ax@htb[/htb]$ telnet 10.129.14.136 21
```

如果 FTP 服务器使用 TLS/SSL 加密运行，情况会略有不同。因为那时我们需要一个可以处理 TLS/SSL 的客户端。为此，我们可以使用客户端 `openssl` 与 FTP 服务器通信。使用 `openssl` 的好处是我们可以看到 SSL 证书，这也可能有所帮助。

服务交互

```shell-session
tr01ax@htb[/htb]$ openssl s_client -connect 10.129.14.136:21 -starttls ftp

CONNECTED(00000003)
```
Can't use SSL_get_servername
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
verify error:num=18:self signed certificate
verify return:1

depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
verify return:1
---
Certificate chain
 0 s:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb

 i:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Dev, CN = master.inlanefreight.htb, emailAddress = admin@inlanefreight.htb
---

Server certificate

-----BEGIN CERTIFICATE-----

MIIENTCCAx2gAwIBAgIUD+SlFZAWzX5yLs2q3ZcfdsRQqMYwDQYJKoZIhvcNAQEL
...SNIP...
```

这是因为 SSL 证书允许我们识别 `hostname`（主机名），例如，在大多数情况下还包括组织或公司的 `email address`（电子邮件地址）。此外，如果公司在全球有多个办公地点，也可以为特定地点创建证书，这些也可以通过 SSL 证书来识别。#footprinting #smb #hacking #windows #port139 #port445
[source](https://academy.hackthebox.com/module/112/section/1067)
--> [[notes about footprinting]]
## SMB

---

`Server Message Block`（`SMB`，服务器消息块）是一种客户端-服务器协议，用于管理对文件和整个目录以及其他网络资源（如打印机、路由器或为网络开放的接口）的访问。不同系统进程之间的信息交换也可以基于 SMB 协议来处理。[SMB](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb/f210069c-7086-4dc2-885e-861d837df688) 最初作为 OS/2 网络操作系统 LAN Manager 和 LAN Server 的一部分向更广泛的公众提供。从那时起，该协议的主要应用领域特别是 Windows 操作系统系列，其网络服务以向下兼容的方式支持 SMB——这意味着安装了较新版本的设备可以轻松地与安装了旧版 Microsoft 操作系统的设备进行通信。通过自由软件项目 Samba，还有一种解决方案可以在 Linux 和 Unix 发行版中使用 SMB，从而实现通过 SMB 进行跨平台通信。

SMB 协议使客户端能够与同一网络中的其他参与者通信，以访问网络上与其共享的文件或服务。另一个系统也必须实现该网络协议，并使用 SMB 服务器应用程序接收和处理客户端请求。然而，在此之前，双方必须建立连接，这就是为什么他们首先要交换相应的消息。

在 IP 网络中，SMB 为此目的使用 TCP 协议，该协议规定了客户端和服务器之间的三次握手，然后才能最终建立连接。TCP 协议的规范还管理后续的数据传输。我们可以在[这里](https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-SMB2/%5bMS-SMB2%5d.pdf#%5B%7B%22num%22%3A920%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C69%2C738%2C0%5D)查看一些示例。

SMB 服务器可以将其本地文件系统的任意部分作为共享提供。因此，客户端可见的层次结构部分独立于服务器上的结构。访问权限由 `Access Control Lists`（`ACL`，访问控制列表）定义。它们可以根据 `execute`（执行）、`read`（读取）和 `full access`（完全访问）等属性为单个用户或用户组进行细粒度控制。ACL 是基于共享定义的，因此不对应于服务器上本地分配的权限。

---

## Samba

如前所述，SMB 服务器有一个替代变体，称为 Samba，专为基于 Unix 的操作系统开发。Samba 实现了 `Common Internet File System`（`CIFS`，通用互联网文件系统）网络协议。[CIFS](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-cifs/934c2faa-54af-4526-ac74-6a24d126724e) 是 SMB 的一种"方言"。换句话说，CIFS 是 SMB 协议的一个非常具体的实现，而 SMB 协议又是由 Microsoft 创建的。这使得 Samba 能够与较新的 Windows 系统通信。因此，它通常被称为 `SMB / CIFS`。然而，CIFS 是 SMB 协议的扩展。所以当我们通过 Samba 向旧的 NetBIOS 服务传递 SMB 命令时，它通常通过 TCP 端口 `137`、`138`、`139` 连接到 Samba 服务器，但 CIFS 仅使用 TCP 端口 `445`。SMB 有多个版本，包括在特定基础设施中仍在使用的过时版本。

|**SMB 版本**|**支持的系统**|**特性**|
|---|---|---|
|CIFS|Windows NT 4.0|通过 NetBIOS 接口通信|
|SMB 1.0|Windows 2000|通过 TCP 直接连接|
|SMB 2.0|Windows Vista, Windows Server 2008|性能升级、改进的消息签名、缓存功能|
|SMB 2.1|Windows 7, Windows Server 2008 R2|锁定机制|
|SMB 3.0|Windows 8, Windows Server 2012|多通道连接、端到端加密、远程存储访问|
|SMB 3.0.2|Windows 8.1, Windows Server 2012 R2||
|SMB 3.1.1|Windows 10, Windows Server 2016|完整性检查、AES-128 加密|

从版本 3 开始，Samba 服务器获得了成为 Active Directory（活动目录）域完整成员的能力。从版本 4 开始，Samba 甚至提供了 Active Directory 域控制器。为此，它包含几个所谓的 daemons（守护进程）——即 Unix 后台程序。属于 Samba 的 SMB 服务器守护进程（`smbd`）提供前两个功能，而 NetBIOS 消息块守护进程（`nmbd`）实现后两个功能。SMB 服务控制这两个后台程序。

我们知道 Samba 适用于 Linux 和 Windows 系统。在网络中，每个主机都参与同一个 `workgroup`（工作组）。工作组是一个组名，用于标识 SMB 网络上计算机及其资源的任意集合。网络上可以同时存在多个工作组。IBM 开发了一种用于计算机联网的 `application programming interface`（`API`，应用程序编程接口），称为 `Network Basic Input/Output System`（`NetBIOS`，网络基本输入/输出系统）。NetBIOS API 提供了一个蓝图，用于应用程序连接并与其他计算机共享数据。在 NetBIOS 环境中，当一台机器上线时，它需要一个名称，这是通过所谓的 `name registration`（名称注册）过程完成的。每个主机在网络上保留其主机名，或者使用 [NetBIOS Name Server](https://networkencyclopedia.com/netbios-name-server-nbns/)（`NBNS`，NetBIOS 名称服务器）来实现此目的。它还被增强为 [Windows Internet Name Service](https://networkencyclopedia.com/windows-internet-name-service-wins/)（`WINS`，Windows Internet 名称服务）。

---

## 默认配置

正如我们可以想象的，Samba 提供了广泛的[设置](https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html)供我们配置。同样，我们通过文本文件定义设置，从中我们可以获得一些设置的概览。过滤后的这些设置如下所示：

#### 默认配置

默认配置

```shell-session
tr01ax@htb[/htb]$ cat /etc/samba/smb.conf | grep -v "#\|\;"

[global]
   workgroup = DEV.INFREIGHT.HTB
   server string = DEVSMB
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d

   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes

   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .

   pam password change = yes
   map to guest = bad user
   usershare allow guests = yes

[printers]
   comment = All Printers
   browseable = no
   path = /var/spool/samba
   printable = yes
   guest ok = no
   read only = yes
   create mask = 0700

[print$]
   comment = Printer Drivers
   path = /var/lib/samba/printers
   browseable = yes
   read only = yes
   guest ok = no
```

我们看到全局设置和两个用于打印机的共享。全局设置是可用 SMB 服务器的配置，用于所有共享。然而，在各个共享中，可以覆盖全局设置，这些设置很可能配置错误。让我们看看一些设置，以了解 Samba 中共享是如何配置的。

|**设置**|**描述**|
|---|---|
|`[sharename]`|网络共享的名称。|
|`workgroup = WORKGROUP/DOMAIN`|客户端查询时显示的工作组。|
|`path = /path/here/`|要授予用户访问权限的目录。|
|`server string = STRING`|发起连接时显示的字符串。|
|`unix password sync = yes`|将 UNIX 密码与 SMB 密码同步？|
|`usershare allow guests = yes`|允许未认证用户访问定义的共享？|
|`map to guest = bad user`|当用户登录请求不匹配有效的 UNIX 用户时该怎么办？|
|`browseable = yes`|此共享是否应显示在可用共享列表中？|
|`guest ok = yes`|允许不使用密码连接到服务？|
|`read only = yes`|仅允许用户读取文件？|
|`create mask = 0700`|需要为新创建的文件设置什么权限？|

---

## 危险设置

上述一些设置已经带来了一些敏感选项。然而，假设我们质疑下面列出的设置，并问自己员工和攻击者能从中获得什么。在这种情况下，我们将看到这些设置带来的优势和劣势。让我们以设置 `browseable = yes` 为例。如果我们作为管理员采用此设置，公司员工将能够方便地查看包含内容的各个文件夹。许多文件夹最终用于更好的组织和结构。如果员工可以浏览共享，攻击者在成功访问后也将能够这样做。

|**设置**|**描述**|
|---|---|
|`browseable = yes`|允许在当前共享中列出可用共享？|
|`read only = no`|禁止创建和修改文件？|
|`writable = yes`|允许用户创建和修改文件？|
|`guest ok = yes`|允许不使用密码连接到服务？|
|`enable privileges = yes`|遵守分配给特定 SID 的权限？|
|`create mask = 0777`|必须为新创建的文件分配什么权限？|
|`directory mask = 0777`|必须为新创建的目录分配什么权限？|
|`logon script = script.sh`|用户登录时需要执行什么脚本？|
|`magic script = script.sh`|脚本关闭时应执行哪个脚本？|
|`magic output = script.out`|magic 脚本的输出需要存储在哪里？|

让我们创建一个名为 `[notes]` 的共享和其他几个，看看这些设置如何影响我们的枚举过程。我们将使用上述所有设置并将它们应用于此共享。例如，这种设置经常被应用，即使只是出于测试目的。如果它是大部门中小团队的内部子网，这种设置经常被保留或忘记重置。这导致我们可以浏览所有共享，并且很可能甚至可以下载和检查它们。

#### 共享示例

共享示例

```shell-session
...SNIP...

[notes]
	comment = CheckIT
	path = /mnt/notes/

	browseable = yes
	read only = no
	writable = yes
	guest ok = yes

	enable privileges = yes
	create mask = 0777
	directory mask = 0777
```

强烈建议查看 Samba 的手册页并自己配置它并尝试这些设置。然后我们将发现对于渗透测试人员来说有趣的潜在方面。此外，我们越熟悉 Samba 服务器和 SMB，就越容易在环境中找到自己的方式并将其用于我们的目的。一旦我们根据需要调整了 `/etc/samba/smb.conf`，我们必须在服务器上重新启动服务。

#### 重启 Samba

重启 Samba

```shell-session
root@samba:~# sudo systemctl restart smbd
```

现在我们可以使用 `smbclient` 命令从我们的主机显示服务器共享的列表（`-L`）。我们使用所谓的 `null session`（空会话）（`-N`），这是 `anonymous`（匿名）访问，无需输入现有用户或有效密码。

#### SMBclient - 连接到共享

SMBclient - 连接到共享

```shell-session
tr01ax@htb[/htb]$ smbclient -N -L //10.129.14.128

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        home            Disk      INFREIGHT Samba
        dev             Disk      DEVenv
        notes           Disk      CheckIT
        IPC$            IPC       IPC Service (DEVSM)
SMB1 disabled -- no workgroup available
```

从结果中我们可以看到，Samba 服务器上现在有五个不同的共享。其中 `print$` 和 `IPC$` 已经包含在基本设置中，正如我们已经看到的。由于我们处理的是 `[notes]` 共享，让我们使用相同的客户端程序登录并检查它。如果我们不熟悉客户端程序，我们可以在成功登录后使用 `help` 命令，列出我们可以执行的所有可能命令。

SMBclient - 连接到共享

```shell-session
tr01ax@htb[/htb]$ smbclient //10.129.14.128/notes

Enter WORKGROUP\<username>'s password:
Anonymous login successful
Try "help" to get a list of possible commands.


smb: \> help

?              allinfo        altname        archive        backup
blocksize      cancel         case_sensitive cd             chmod
chown          close          del            deltree        dir
du             echo           exit           get            getfacl
geteas         hardlink       help           history        iosize
lcd            link           lock           lowercase      ls
l              mask           md             mget           mkdir
more           mput           newer          notify         open
posix          posix_encrypt  posix_open     posix_mkdir    posix_rmdir
posix_unlink   posix_whoami   print          prompt         put
pwd            q              queue          quit           readlink
rd             recurse        reget          rename         reput
rm             rmdir          showacls       setea          setmode
scopy          stat           symlink        tar            tarmode
timeout        translate      unlock         volume         vuid
wdel           logon          listconnect    showconnect    tcon
tdis           tid            utimes         logoff         ..
!


smb: \> ls

  .                                   D        0  Wed Sep 22 18:17:51 2021
  ..                                  D        0  Wed Sep 22 12:03:59 2021
  prep-prod.txt                       N       71  Sun Sep 19 15:45:21 2021

                30313412 blocks of size 1024. 16480084 blocks available
```

一旦我们发现了有趣的文件或文件夹，我们可以使用 `get` 命令下载它们。Smbclient 还允许我们通过在开头使用感叹号（`!<cmd>`）来执行本地系统命令，而不会中断连接。

#### 从 SMB 下载文件

从 SMB 下载文件

```shell-session
smb: \> get prep-prod.txt

getting file \prep-prod.txt of size 71 as prep-prod.txt (8,7 KiloBytes/sec)
(average 8,7 KiloBytes/sec)


smb: \> !ls

prep-prod.txt


smb: \> !cat prep-prod.txt

[] check your code with the templates
[] run code-assessment.py
[] …
```

从管理的角度来看，我们可以使用 `smbstatus` 检查这些连接。除了 Samba 版本，我们还可以看到谁从哪个主机连接到了哪个共享。这在我们进入子网（可能甚至是隔离的）时尤其重要，其他人仍然可以访问。

例如，使用域级安全性时，samba 服务器充当 Windows 域的成员。每个域至少有一个域控制器，通常是提供密码认证的 Windows NT 服务器。此域控制器为工作组提供权威的密码服务器。域控制器在自己的 `Security Authentication Module`（`SAM`，安全认证模块）中跟踪用户和密码，并在每个用户首次登录并希望访问另一台机器的共享时对其进行身份验证。

#### Samba 状态

Samba 状态

```shell-session
root@samba:~# smbstatus

Samba version 4.11.6-Ubuntu
PID     Username     Group        Machine                                   Protocol Version  Encryption           Signing
----------------------------------------------------------------------------------------------------------------------------------------
75691   sambauser    samba        10.10.14.4 (ipv4:10.10.14.4:45564)      SMB3_11           -                    -

Service      pid     Machine       Connected at                     Encryption   Signing
---------------------------------------------------------------------------------------------
notes        75691   10.10.14.4   Do Sep 23 00:12:06 2021 CEST     -            -

No locked files
```

---

## 服务足迹识别

让我们回到我们的枚举工具之一。Nmap 也有许多选项和 NSE 脚本，可以帮助我们更仔细地检查目标的 SMB 服务并获取更多信息。然而，缺点是这些扫描可能需要很长时间。因此，还建议手动查看服务，主要是因为我们可以找到比 Nmap 显示给我们的更多细节。不过，首先让我们看看 Nmap 能在我们的目标 Samba 服务器上发现什么，我们在那里创建了 `[notes]` 共享用于测试目的。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -sV -sC -p139,445

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 15:15 CEST
Nmap scan report for sharing.inlanefreight.htb (10.129.14.128)
Host is up (0.00024s latency).

PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
MAC Address: 00:00:00:00:00:00 (VMware)

Host script results:
|_nbstat: NetBIOS name: HTB, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-09-19T13:16:04
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.35 seconds
```

我们可以从结果中看到，Nmap 在这里为我们提供的信息并不多。因此，我们应该求助于其他工具，这些工具允许我们手动与 SMB 交互并发送特定请求以获取信息。其中一个方便的工具是 `rpcclient`。这是一个执行 MS-RPC 功能的工具。

[Remote Procedure Call](https://www.geeksforgeeks.org/remote-procedure-call-rpc-in-operating-system/)（`RPC`，远程过程调用）是一个概念，因此也是实现网络和客户端-服务器架构中操作和工作共享结构的核心工具。通过 RPC 的通信过程包括传递参数和返回函数值。

#### RPCclient

RPCclient

```shell-session
tr01ax@htb[/htb]$ rpcclient -U "" 10.129.14.128

Enter WORKGROUP\'s password:
rpcclient $>
```

`rpcclient` 为我们提供了许多不同的请求，我们可以使用这些请求在 SMB 服务器上执行特定功能以获取信息。所有这些功能的完整列表可以在 rpcclient 的[手册页](https://www.samba.org/samba/docs/current/man-html/rpcclient.1.html)上找到。

|**查询**|**描述**|
|---|---|
|`srvinfo`|服务器信息。|
|`enumdomains`|枚举网络中部署的所有域。|
|`querydominfo`|提供部署域的域、服务器和用户信息。|
|`netshareenumall`|枚举所有可用共享。|
|`netsharegetinfo <share>`|提供有关特定共享的信息。|
|`enumdomusers`|枚举所有域用户。|
|`queryuser <RID>`|提供有关特定用户的信息。|

#### RPCclient - 枚举

RPCclient - 枚举

```shell-session
rpcclient $> srvinfo

        DEVSMB         Wk Sv PrQ Unx NT SNT DEVSM
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03


rpcclient $> enumdomains

name:[DEVSMB] idx:[0x0]
name:[Builtin] idx:[0x1]


rpcclient $> querydominfo

Domain:         DEVOPS
Server:         DEVSMB
Comment:        DEVSM
Total Users:    2
Total Groups:   0
Total Aliases:  0
Sequence No:    1632361158
Force Logoff:   -1
Domain Server State:    0x1
Server Role:    ROLE_DOMAIN_PDC
Unknown 3:      0x1


rpcclient $> netshareenumall

netname: print$
        remark: Printer Drivers
        path:   C:\var\lib\samba\printers
        password:
netname: home
        remark: INFREIGHT Samba
        path:   C:\home\
        password:
netname: dev
        remark: DEVenv
        path:   C:\home\sambauser\dev\
        password:
netname: notes
        remark: CheckIT
        path:   C:\mnt\notes\
        password:
netname: IPC$
        remark: IPC Service (DEVSM)
        path:   C:\tmp
        password:


rpcclient $> netsharegetinfo notes

netname: notes
        remark: CheckIT
        path:   C:\mnt\notes\
        password:
        type:   0x0
        perms:  0
        max_uses:       -1
        num_uses:       1
revision: 1
type: 0x8004: SEC_DESC_DACL_PRESENT SEC_DESC_SELF_RELATIVE
DACL
        ACL     Num ACEs:       1       revision:       2
        ---
        ACE
                type: ACCESS ALLOWED (0) flags: 0x00
                Specific bits: 0x1ff
                Permissions: 0x101f01ff: Generic all access SYNCHRONIZE_ACCESS WRITE_OWNER_ACCESS WRITE_DAC_ACCESS READ_CONTROL_ACCESS DELETE_ACCESS
                SID: S-1-1-0
```

这些示例向我们展示了哪些信息可能会泄露给匿名用户。一旦 `anonymous`（匿名）用户访问了网络服务，只需要一个错误就可以给他们太多权限或太多可见性，从而使整个网络面临重大风险。

最重要的是，对此类服务的匿名访问也可能导致发现其他用户，在最激进的情况下可以对这些用户进行暴力破解攻击。人类比正确配置的计算机进程更容易出错，安全意识的缺乏和懒惰常常导致弱密码，这些密码很容易被破解。让我们看看如何使用 `rpcclient` 枚举用户。

#### Rpcclient - 用户枚举

Rpcclient - 用户枚举

```shell-session
rpcclient $> enumdomusers

user:[mrb3n] rid:[0x3e8]
user:[cry0l1t3] rid:[0x3e9]


rpcclient $> queryuser 0x3e9

        User Name   :   cry0l1t3
        Full Name   :   cry0l1t3
        Home Drive  :   \\devsmb\cry0l1t3
        Dir Drive   :
        Profile Path:   \\devsmb\cry0l1t3\profile
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Do, 01 Jan 1970 01:00:00 CET
        Logoff Time              :      Mi, 06 Feb 2036 16:06:39 CET
        Kickoff Time             :      Mi, 06 Feb 2036 16:06:39 CET
        Password last set Time   :      Mi, 22 Sep 2021 17:50:56 CEST
        Password can change Time :      Mi, 22 Sep 2021 17:50:56 CEST
        Password must change Time:      Do, 14 Sep 30828 04:48:05 CEST
        unknown_2[0..31]...
        user_rid :      0x3e9
        group_rid:      0x201
        acb_info :      0x00000014
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x00000000
        padding1[0..7]...
        logon_hrs[0..21]...


rpcclient $> queryuser 0x3e8

        User Name   :   mrb3n
        Full Name   :
        Home Drive  :   \\devsmb\mrb3n
        Dir Drive   :
        Profile Path:   \\devsmb\mrb3n\profile
        Logon Script:
        Description :
        Workstations:
        Comment     :
        Remote Dial :
        Logon Time               :      Do, 01 Jan 1970 01:00:00 CET
        Logoff Time              :      Mi, 06 Feb 2036 16:06:39 CET
        Kickoff Time             :      Mi, 06 Feb 2036 16:06:39 CET
        Password last set Time   :      Mi, 22 Sep 2021 17:47:59 CEST
        Password can change Time :      Mi, 22 Sep 2021 17:47:59 CEST
        Password must change Time:      Do, 14 Sep 30828 04:48:05 CEST
        unknown_2[0..31]...
        user_rid :      0x3e8
        group_rid:      0x201
        acb_info :      0x00000010
        fields_present: 0x00ffffff
        logon_divs:     168
        bad_password_count:     0x00000000
        logon_count:    0x00000000
        padding1[0..7]...
        logon_hrs[0..21]...
```

然后我们可以使用结果来识别组的RID（相对标识符），进而用它来检索整个组的信息。

#### Rpcclient - 组信息

Rpcclient - Group Information

```shell-session
rpcclient $> querygroup 0x201

        Group Name:     None
        Description:    Ordinary Users
        Group Attribute:7
        Num Members:2
```

然而，也可能出现并非所有命令都对我们可用的情况，我们会根据用户受到某些限制。不过，基于RID的 `queryuser <RID>` 查询通常是被允许的。因此我们可以使用rpcclient暴力破解RID来获取信息。因为我们可能不知道谁被分配了哪个RID，我们知道一旦查询到一个已分配的RID就会获得相关信息。有多种方式和工具可以用于此目的。为了继续使用该工具，我们可以使用 `Bash` 创建一个 `For循环`，通过rpcclient向服务发送命令并过滤结果。

#### 暴力破解用户RID

Brute Forcing User RIDs

```shell-session
tr01ax@htb[/htb]$ for i in $(seq 500 1100);do rpcclient -N -U "" 10.129.14.128 -c "queryuser 0x$(printf '%x\n' $i)" | grep "User Name\|user_rid\|group_rid" && echo "";done

        User Name   :   sambauser
        user_rid :      0x1f5
        group_rid:      0x201

        User Name   :   mrb3n
        user_rid :      0x3e8
        group_rid:      0x201

        User Name   :   cry0l1t3
        user_rid :      0x3e9
        group_rid:      0x201
```

另一种替代方案是来自 [Impacket](https://github.com/SecureAuthCorp/impacket) 的Python脚本 [samrdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/samrdump.py)。

#### Impacket - Samrdump.py

Impacket - Samrdump.py

```shell-session
tr01ax@htb[/htb]$ samrdump.py 10.129.14.128

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] Retrieving endpoint list from 10.129.14.128
Found domain(s):
 . DEVSMB
 . Builtin
[*] Looking up users in domain DEVSMB
Found user: mrb3n, uid = 1000
Found user: cry0l1t3, uid = 1001
mrb3n (1000)/FullName:
mrb3n (1000)/UserComment:
mrb3n (1000)/PrimaryGroupId: 513
mrb3n (1000)/BadPasswordCount: 0
mrb3n (1000)/LogonCount: 0
mrb3n (1000)/PasswordLastSet: 2021-09-22 17:47:59
mrb3n (1000)/PasswordDoesNotExpire: False
mrb3n (1000)/AccountIsDisabled: False
mrb3n (1000)/ScriptPath:
cry0l1t3 (1001)/FullName: cry0l1t3
cry0l1t3 (1001)/UserComment:
cry0l1t3 (1001)/PrimaryGroupId: 513
cry0l1t3 (1001)/BadPasswordCount: 0
cry0l1t3 (1001)/LogonCount: 0
cry0l1t3 (1001)/PasswordLastSet: 2021-09-22 17:50:56
cry0l1t3 (1001)/PasswordDoesNotExpire: False
cry0l1t3 (1001)/AccountIsDisabled: False
cry0l1t3 (1001)/ScriptPath:
[*] Received 2 entries.
```

我们已经通过 `rpcclient` 获得的信息也可以使用其他工具获取。例如，[SMBMap](https://github.com/ShawnDEvans/smbmap) 和 [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) 工具也被广泛使用，对SMB服务的枚举很有帮助。

#### SMBmap

SMBmap

```shell-session
tr01ax@htb[/htb]$ smbmap -H 10.129.14.128

[+] Finding open SMB ports....
[+] User SMB session established on 10.129.14.128...
[+] IP: 10.129.14.128:445       Name: 10.129.14.128
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        home                                                    NO ACCESS       INFREIGHT Samba
        dev                                                     NO ACCESS       DEVenv
        notes                                                   NO ACCESS       CheckIT
        IPC$                                                    NO ACCESS       IPC Service (DEVSM)
```

#### CrackMapExec

CrackMapExec

```shell-session
tr01ax@htb[/htb]$ crackmapexec smb 10.129.14.128 --shares -u '' -p ''

SMB         10.129.14.128   445    DEVSMB           [*] Windows 6.1 Build 0 (name:DEVSMB) (domain:) (signing:False) (SMBv1:False)
SMB         10.129.14.128   445    DEVSMB           [+] \:
SMB         10.129.14.128   445    DEVSMB           [+] Enumerated shares
SMB         10.129.14.128   445    DEVSMB           Share           Permissions     Remark
SMB         10.129.14.128   445    DEVSMB           -----           -----------     ------
SMB         10.129.14.128   445    DEVSMB           print$                          Printer Drivers
SMB         10.129.14.128   445    DEVSMB           home                            INFREIGHT Samba
SMB         10.129.14.128   445    DEVSMB           dev                             DEVenv
SMB         10.129.14.128   445    DEVSMB           notes           READ,WRITE      CheckIT
SMB         10.129.14.128   445    DEVSMB           IPC$                            IPC Service (DEVSM)
```

另一个值得一提的工具是 [enum4linux-ng](https://github.com/cddmp/enum4linux-ng)，它基于一个较老的工具enum4linux。这个工具自动化了许多查询（但不是全部），可以返回大量信息。

#### Enum4Linux-ng - 安装

Enum4Linux-ng - Installation

```shell-session
tr01ax@htb[/htb]$ git clone https://github.com/cddmp/enum4linux-ng.git
tr01ax@htb[/htb]$ cd enum4linux-ng
tr01ax@htb[/htb]$ pip3 install -r requirements.txt
```

#### Enum4Linux-ng - 枚举

Enum4Linux-ng - Enumeration

```shell-session
tr01ax@htb[/htb]$ ./enum4linux-ng.py 10.129.14.128 -A

ENUM4LINUX - next generation

 ==========================
|    Target Information    |
 ==========================
[*] Target ........... 10.129.14.128
[*] Username ......... ''
[*] Random Username .. 'juzgtcsu'
[*] Password ......... ''
[*] Timeout .......... 5 second(s)

 =====================================
|    Service Scan on 10.129.14.128    |
 =====================================
[*] Checking LDAP
[-] Could not connect to LDAP on 389/tcp: connection refused
[*] Checking LDAPS
[-] Could not connect to LDAPS on 636/tcp: connection refused
[*] Checking SMB
[+] SMB is accessible on 445/tcp
[*] Checking SMB over NetBIOS
[+] SMB over NetBIOS is accessible on 139/tcp

 =====================================================
|    NetBIOS Names and Workgroup for 10.129.14.128    |
 =====================================================
[+] Got domain/workgroup name: DEVOPS
[+] Full NetBIOS names information:
- DEVSMB          <00> -         H <ACTIVE>  Workstation Service
- DEVSMB          <03> -         H <ACTIVE>  Messenger Service
- DEVSMB          <20> -         H <ACTIVE>  File Server Service
- ..__MSBROWSE__. <01> - <GROUP> H <ACTIVE>  Master Browser
- DEVOPS          <00> - <GROUP> H <ACTIVE>  Domain/Workgroup Name
- DEVOPS          <1d> -         H <ACTIVE>  Master Browser
- DEVOPS          <1e> - <GROUP> H <ACTIVE>  Browser Service Elections
- MAC Address = 00-00-00-00-00-00

 ==========================================
|    SMB Dialect Check on 10.129.14.128    |
 ==========================================
[*] Trying on 445/tcp
[+] Supported dialects and settings:
SMB 1.0: false
SMB 2.02: true
SMB 2.1: true
SMB 3.0: true
SMB1 only: false
Preferred dialect: SMB 3.0
SMB signing required: false

 ==========================================
|    RPC Session Check on 10.129.14.128    |
 ==========================================
[*] Check for null session
[+] Server allows session using username '', password ''
[*] Check for random user session
[+] Server allows session using username 'juzgtcsu', password ''
[H] Rerunning enumeration with user 'juzgtcsu' might give more results

 ====================================================
|    Domain Information via RPC for 10.129.14.128    |
 ====================================================
[+] Domain: DEVOPS
[+] SID: NULL SID
[+] Host is part of a workgroup (not a domain)

 ============================================================
|    Domain Information via SMB session for 10.129.14.128    |
 ============================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found domain information via SMB
NetBIOS computer name: DEVSMB
NetBIOS domain name: ''
DNS domain: ''
FQDN: htb

 ================================================
|    OS Information via RPC for 10.129.14.128    |
 ================================================
[*] Enumerating via unauthenticated SMB session on 445/tcp
[+] Found OS information via SMB
[*] Enumerating via 'srvinfo'
[+] Found OS information via 'srvinfo'
[+] After merging OS information we have the following result:
OS: Windows 7, Windows Server 2008 R2
OS version: '6.1'
OS release: ''
OS build: '0'
Native OS: not supported
Native LAN manager: not supported
Platform id: '500'
Server type: '0x809a03'
Server type string: Wk Sv PrQ Unx NT SNT DEVSM

 ======================================
|    Users via RPC on 10.129.14.128    |
 ======================================
[*] Enumerating users via 'querydispinfo'
[+] Found 2 users via 'querydispinfo'
[*] Enumerating users via 'enumdomusers'
[+] Found 2 users via 'enumdomusers'
[+] After merging user results we have 2 users total:
'1000':
  username: mrb3n
  name: ''
  acb: '0x00000010'
  description: ''
'1001':
  username: cry0l1t3
  name: cry0l1t3
  acb: '0x00000014'
  description: ''

 =======================================
|    Groups via RPC on 10.129.14.128    |
 =======================================
[*] Enumerating local groups
[+] Found 0 group(s) via 'enumalsgroups domain'
[*] Enumerating builtin groups
[+] Found 0 group(s) via 'enumalsgroups builtin'
[*] Enumerating domain groups
[+] Found 0 group(s) via 'enumdomgroups'

 =======================================
|    Shares via RPC on 10.129.14.128    |
 =======================================
[*] Enumerating shares
[+] Found 5 share(s):
IPC$:
  comment: IPC Service (DEVSM)
  type: IPC
dev:
  comment: DEVenv
  type: Disk
home:
  comment: INFREIGHT Samba
  type: Disk
notes:
  comment: CheckIT
  type: Disk
print$:
  comment: Printer Drivers
  type: Disk
[*] Testing share IPC$
[-] Could not check share: STATUS_OBJECT_NAME_NOT_FOUND
[*] Testing share dev
[-] Share doesn't exist
[*] Testing share home
[+] Mapping: OK, Listing: OK
[*] Testing share notes
[+] Mapping: OK, Listing: OK
[*] Testing share print$
[+] Mapping: DENIED, Listing: N/A

 ==========================================
|    Policies via RPC for 10.129.14.128    |
 ==========================================
[*] Trying port 445/tcp
[+] Found policy:
domain_password_information:
  pw_history_length: None
  min_pw_length: 5
  min_pw_age: none
  max_pw_age: 49710 days 6 hours 21 minutes
  pw_properties:
  - DOMAIN_PASSWORD_COMPLEX: false
  - DOMAIN_PASSWORD_NO_ANON_CHANGE: false
  - DOMAIN_PASSWORD_NO_CLEAR_CHANGE: false
  - DOMAIN_PASSWORD_LOCKOUT_ADMINS: false
  - DOMAIN_PASSWORD_PASSWORD_STORE_CLEARTEXT: false
  - DOMAIN_PASSWORD_REFUSE_PASSWORD_CHANGE: false
domain_lockout_information:
  lockout_observation_window: 30 minutes
  lockout_duration: 30 minutes
  lockout_threshold: None
domain_logoff_information:
  force_logoff_time: 49710 days 6 hours 21 minutes

 ==========================================
|    Printers via RPC for 10.129.14.128    |
 ==========================================
[+] No printers returned (this is not an error)

Completed after 0.61 seconds
```

我们需要使用两个以上的工具进行枚举。因为由于工具的编程方式，我们可能会获得需要手动检查的不同信息。因此，我们永远不应该只依赖那些我们不清楚其编写方式的自动化工具。#nfs #footprinting #hacking #enumeration #port111 #port2049 [source](https://academy.hackthebox.com/module/112/section/1068) --> [[notes about footprinting]]
# NFS

---

`网络文件系统`（`NFS`，Network File System）是由Sun Microsystems开发的网络文件系统，与SMB具有相同的目的。它的目的是通过网络访问文件系统，就像它们是本地的一样。然而，它使用完全不同的协议。[NFS](https://en.wikipedia.org/wiki/Network_File_System) 用于Linux和Unix系统之间。这意味着NFS客户端无法直接与SMB服务器通信。NFS是一个互联网标准，管理分布式文件系统中的程序。虽然已使用多年的NFS协议版本3.0（`NFSv3`）对客户端计算机进行身份验证，但在 `NFSv4` 中这一点发生了变化。在这里，与Windows SMB协议一样，用户必须进行身份验证。

|**版本**|**特性**|
|---|---|
|`NFSv2`|较旧但被许多系统支持，最初完全通过UDP运行。|
|`NFSv3`|具有更多功能，包括可变文件大小和更好的错误报告，但与NFSv2客户端不完全兼容。|
|`NFSv4`|包含Kerberos（一种网络认证协议），可穿越防火墙和在互联网上工作，不再需要端口映射器（portmapper），支持ACL（访问控制列表），采用基于状态的操作，并提供性能改进和高安全性。它也是第一个具有有状态协议的版本。|

NFS版本4.1（[RFC 8881](https://datatracker.ietf.org/doc/html/rfc8881)）旨在提供协议支持以利用集群服务器部署，包括提供对分布在多个服务器上的文件的可扩展并行访问的能力（pNFS扩展）。此外，NFSv4.1包括会话中继机制，也称为NFS多路径。NFSv4相对于其前身的一个显著优势是，只使用一个UDP或TCP端口 `2049` 来运行服务，这简化了协议在防火墙中的使用。

NFS基于 [开放网络计算远程过程调用](https://en.wikipedia.org/wiki/Sun_RPC)（`ONC-RPC`/`SUN-RPC`）协议，暴露在 `TCP` 和 `UDP` 端口 `111` 上，该协议使用 [外部数据表示](https://en.wikipedia.org/wiki/External_Data_Representation)（`XDR`）进行与系统无关的数据交换。NFS协议`没有`用于`身份验证`或`授权`的机制。相反，身份验证完全转移到RPC协议的选项中。授权取自文件系统的可用信息，服务器负责将客户端提供的用户信息转换为文件系统的用户信息，并尽可能正确地将相应的授权信息转换为UNIX所需的语法。

最常见的身份验证是通过UNIX的 `UID`/`GID` 和`组成员资格`，这就是为什么这种语法最有可能应用于NFS协议。一个问题是客户端和服务器不一定具有相同的UID/GID到用户和组的映射，服务器不需要做任何进一步的操作。服务器端无法进行进一步的检查。这就是为什么NFS只应在受信任的网络中使用这种身份验证方法。

---

## 默认配置

NFS配置并不困难，因为它没有FTP或SMB那么多的选项。`/etc/exports` 文件包含NFS服务器上可供客户端访问的物理文件系统表。[NFS导出表](http://manpages.ubuntu.com/manpages/trusty/man5/exports.5.html) 显示了它接受的选项，从而指示我们可用的选项。

#### 导出文件

Exports File

```shell-session
tr01ax@htb[/htb]$ cat /etc/exports

# /etc/exports: the access control list for filesystems which may be exported
#               to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
```

默认的 `exports` 文件还包含一些配置NFS共享的示例。首先，指定文件夹并使其对其他人可用，然后将他们在此NFS共享上拥有的权限连接到主机或子网。最后，可以向主机或子网添加额外的选项。

|**选项**|**描述**|
|---|---|
|`rw`|读写权限。|
|`ro`|只读权限。|
|`sync`|同步数据传输。（稍慢）|
|`async`|异步数据传输。（稍快）|
|`secure`|不使用1024以上的端口。|
|`insecure`|将使用1024以上的端口。|
|`no_subtree_check`|此选项禁用子目录树检查。|
|`root_squash`|将root的UID/GID 0的所有文件权限分配给匿名用户的UID/GID，这可以防止 `root` 访问NFS挂载上的文件。|

让我们为测试目的创建这样一个条目并尝试这些设置。

#### ExportFS

ExportFS

```shell-session
root@nfs:~# echo '/mnt/nfs  10.129.14.0/24(sync,no_subtree_check)' >> /etc/exports
root@nfs:~# systemctl restart nfs-kernel-server
root@nfs:~# exportfs

/mnt/nfs      	10.129.14.0/24
```

我们已使用上述设置将文件夹 `/mnt/nfs` 共享给子网 `10.129.14.0/24`。这意味着网络上的所有主机都能够挂载此NFS共享并检查此文件夹的内容。

---

## 危险设置

然而，即使使用NFS，某些设置对公司及其基础设施也可能是危险的。以下列出了其中一些：

|**选项**|**描述**|
|---|---|
|`rw`|读写权限。|
|`insecure`|将使用1024以上的端口。|
|`nohide`|如果在导出目录下挂载了另一个文件系统，则该目录通过其自己的导出条目导出。|
|`no_root_squash`|root创建的所有文件都保持UID/GID为0。|

强烈建议创建一个本地虚拟机并试验这些设置。我们将发现一些方法来展示NFS服务器是如何配置的。为此，我们可以创建几个文件夹并为每个文件夹分配不同的选项。然后我们可以检查它们，看看哪些设置会对NFS共享及其权限以及枚举过程产生什么影响。

我们可以看一下 `insecure` 选项。这是危险的，因为用户可以使用1024以上的端口。前1024个端口只能由root使用。这防止了用户不能使用1024以上的端口套接字用于NFS服务并与其交互。

---

## 服务信息收集

在对NFS进行信息收集时，TCP端口 `111` 和 `2049` 是必不可少的。我们还可以通过RPC获取有关NFS服务和主机的信息，如下例所示。

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -p111,2049 -sV -sC

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 17:12 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00018s latency).

PORT    STATE SERVICE VERSION
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      41982/udp6  mountd
|   100005  1,2,3      45837/tcp   mountd
|   100005  1,2,3      47217/tcp6  mountd
|   100005  1,2,3      58830/udp   mountd
|   100021  1,3,4      39542/udp   nlockmgr
|   100021  1,3,4      44629/tcp   nlockmgr
|   100021  1,3,4      45273/tcp6  nlockmgr
|   100021  1,3,4      47524/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp open  nfs_acl 3 (RPC #100227)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.58 seconds
```

`rpcinfo` NSE脚本（Nmap脚本引擎脚本）检索当前运行的所有RPC服务的列表、它们的名称和描述以及它们使用的端口。这让我们可以检查目标共享是否在所有必需的端口上连接到网络。此外，对于NFS，Nmap有一些NSE脚本可用于扫描。这些脚本可以向我们展示共享的`内容`及其`统计信息`。

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap --script nfs* 10.129.14.128 -sV -p111,2049

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 17:37 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00021s latency).

PORT     STATE SERVICE VERSION
111/tcp  open  rpcbind 2-4 (RPC #100000)
| nfs-ls: Volume /mnt/nfs
|   access: Read Lookup NoModify NoExtend NoDelete NoExecute
| PERMISSION  UID    GID    SIZE  TIME                 FILENAME
| rwxrwxrwx   65534  65534  4096  2021-09-19T15:28:17  .
| ??????????  ?      ?      ?     ?                    ..
| rw-r--r--   0      0      1872  2021-09-19T15:27:42  id_rsa
| rw-r--r--   0      0      348   2021-09-19T15:28:17  id_rsa.pub
| rw-r--r--   0      0      0     2021-09-19T15:22:30  nfs.share
|_
| nfs-showmount:
|_  /mnt/nfs 10.129.14.0/24
| nfs-statfs:
|   Filesystem  1K-blocks   Used       Available   Use%  Maxfilesize  Maxlink
|_  /mnt/nfs    30313412.0  8074868.0  20675664.0  29%   16.0T        32000
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      41982/udp6  mountd
|   100005  1,2,3      45837/tcp   mountd
|   100005  1,2,3      47217/tcp6  mountd
|   100005  1,2,3      58830/udp   mountd
|   100021  1,3,4      39542/udp   nlockmgr
|   100021  1,3,4      44629/tcp   nlockmgr
```
   100021  1,3,4      45273/tcp6  nlockmgr
   100021  1,3,4      47524/udp6  nlockmgr
   100227  3           2049/tcp   nfs_acl
   100227  3           2049/tcp6  nfs_acl
   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
2049/tcp open  nfs_acl 3 (RPC #100227)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.45 seconds
```

一旦我们发现了这样的NFS服务，就可以将其挂载到本地机器上。为此，我们可以创建一个新的空文件夹，NFS共享将被挂载到该文件夹。挂载完成后，我们可以像浏览本地系统一样导航和查看其中的内容。

#### 显示可用的NFS共享

```shell-session
tr01ax@htb[/htb]$ showmount -e 10.129.14.128

Export list for 10.129.14.128:
/mnt/nfs 10.129.14.0/24
```

#### 挂载NFS共享

```shell-session
tr01ax@htb[/htb]$ mkdir target-NFS
tr01ax@htb[/htb]$ sudo mount -t nfs 10.129.14.128:/ ./target-NFS/ -o nolock
tr01ax@htb[/htb]$ cd target-NFS
tr01ax@htb[/htb]$ tree .

.
└── mnt
    └── nfs
        ├── id_rsa
        ├── id_rsa.pub
        └── nfs.share

2 directories, 3 files
```

在那里我们将有机会访问权限以及显示和可查看文件所属的用户名和组。因为一旦我们获得了用户名、组名、UID（用户标识符）和GUID（组标识符），我们就可以在自己的系统上创建它们，并将它们适配到NFS共享，以便查看和修改文件。

#### 列出带有用户名和组名的内容

```shell-session
tr01ax@htb[/htb]$ ls -l mnt/nfs/

total 16
-rw-r--r-- 1 cry0l1t3 cry0l1t3 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 cry0l1t3 cry0l1t3  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1 root     root     1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1 root     root      348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1 root     root        0 Sep 19 17:22 nfs.share
```

#### 列出带有UID和GUID的内容

```shell-session
tr01ax@htb[/htb]$ ls -n mnt/nfs/

total 16
-rw-r--r-- 1 1000 1000 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 1000 1000  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1    0 1000 1221 Sep 19 18:21 backup.sh
-rw-r--r-- 1    0    0 1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1    0    0  348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1    0    0    0 Sep 19 17:22 nfs.share
```

需要注意的是，如果设置了`root_squash`选项，即使以`root`身份也无法编辑`backup.sh`文件。

我们还可以利用NFS进行进一步的权限提升。例如，如果我们通过SSH访问系统，想要读取特定用户可以读取的另一个文件夹中的文件，我们需要上传一个具有该用户`SUID`（Set User ID，设置用户ID）的shell到NFS共享，然后通过SSH用户运行该shell。

完成所有必要步骤并获得所需信息后，我们可以卸载NFS共享。

#### 卸载

```shell-session
tr01ax@htb[/htb]$ cd ..
tr01ax@htb[/htb]$ sudo umount ./target-NFS
```#dns #footprinting #enumeration #hacking #port53
source: https://academy.hackthebox.com/module/112/section/1069
--> [[notes about footprinting]]
# DNS

---

`Domain Name System`（`DNS`，域名系统）是互联网的重要组成部分。例如，通过域名，如[academy.hackthebox.com](https://academy.hackthebox.com)或[www.hackthebox.com](https://www.hackthebox.eu)，我们可以访问托管服务商分配了一个或多个特定IP地址的Web服务器。DNS是一个将计算机名称解析为IP地址的系统，它没有中央数据库。简单来说，我们可以把它想象成一个拥有许多不同电话簿的图书馆。信息分布在数千台域名服务器上。全球分布的DNS服务器将域名转换为IP地址，从而控制用户可以通过特定域名访问哪台服务器。全球范围内使用几种不同类型的DNS服务器：

- DNS根服务器（DNS root server）
- 权威域名服务器（Authoritative name server）
- 非权威域名服务器（Non-authoritative name server）
- 缓存服务器（Caching server）
- 转发服务器（Forwarding server）
- 解析器（Resolver）

|**服务器类型**|**描述**|
|---|---|
|`DNS Root Server`|DNS的根服务器负责顶级域名（`TLD`，Top-Level Domain）。作为最后一级实例，只有当域名服务器没有响应时才会被请求。因此，根服务器是用户和互联网内容之间的核心接口，因为它连接域名和IP地址。[互联网名称与数字地址分配机构](https://www.icann.org/)（`ICANN`）协调根域名服务器的工作。全球共有`13`台这样的根服务器。|
|`Authoritative Nameserver`|权威域名服务器对特定区域拥有权限。它们只回答其责任区域内的查询，其信息具有约束力。如果权威域名服务器无法回答客户端的查询，根域名服务器将在此时接管。|
|`Non-authoritative Nameserver`|非权威域名服务器不负责特定的DNS区域。相反，它们自己收集特定DNS区域的信息，这是通过递归或迭代DNS查询完成的。|
|`Caching DNS Server`|缓存DNS服务器在指定时间段内缓存来自其他域名服务器的信息。权威域名服务器确定此存储的持续时间。|
|`Forwarding Server`|转发服务器只执行一个功能：将DNS查询转发到另一台DNS服务器。|
|`Resolver`|解析器不是权威DNS服务器，而是在计算机或路由器中本地执行名称解析。|

DNS主要是未加密的。因此，本地WLAN上的设备和互联网提供商可以入侵并监视DNS查询。由于这带来了隐私风险，现在有一些DNS加密解决方案。默认情况下，IT安全专业人员在此应用`DNS over TLS`（`DoT`）或`DNS over HTTPS`（`DoH`）。此外，网络协议`DNSCrypt`也可以加密计算机和域名服务器之间的流量。

然而，DNS不仅连接计算机名称和IP地址。它还存储和输出与域名相关的服务的附加信息。因此，DNS查询也可用于确定哪台计算机作为相关域的电子邮件服务器，或该域的域名服务器叫什么名称。

![](https://academy.hackthebox.com/storage/modules/27/tooldev-dns.png)

DNS查询使用不同的`DNS记录`，它们都有各种任务。此外，不同的功能有单独的条目，因为我们可以为一个域设置邮件服务器和其他服务器。

|**DNS记录**|**描述**|
|---|---|
|`A`|返回请求域的IPv4地址作为结果。|
|`AAAA`|返回请求域的IPv6地址。|
|`MX`|返回负责的邮件服务器作为结果。|
|`NS`|返回域的DNS服务器（域名服务器）。|
|`TXT`|此记录可以包含各种信息。这个多功能记录可用于验证Google Search Console或验证SSL证书。此外，还设置SPF和DMARC条目来验证邮件流量并保护其免受垃圾邮件。|
|`CNAME`|此记录用作别名。如果域名www.hackthebox.eu应该指向相同的IP，我们为一个创建A记录，为另一个创建CNAME记录。|
|`PTR`|PTR记录以相反的方式工作（反向查找）。它将IP地址转换为有效的域名。|
|`SOA`|提供有关相应DNS区域和管理联系人电子邮件地址的信息。|

`SOA`记录位于域的区域文件中，指定谁负责域的运营以及如何管理该域的DNS信息。

```shell-session
tr01ax@htb[/htb]$ dig soa www.inlanefreight.com

; <<>> DiG 9.16.27-Debian <<>> soa www.inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15876
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.inlanefreight.com.         IN      SOA

;; AUTHORITY SECTION:
inlanefreight.com.      900     IN      SOA     ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Jan 05 12:56:10 GMT 2023
;; MSG SIZE  rcvd: 128
```

在电子邮件地址中，点（.）被替换为@符号。在此示例中，管理员的电子邮件地址是`awsdns-hostmaster@amazon.com`。

---

## 默认配置

DNS有许多不同的配置类型。因此，我们只讨论最重要的配置，以便从管理的角度更好地说明功能原理。所有DNS服务器都使用三种不同类型的配置文件：

1. 本地DNS配置文件
2. 区域文件
3. 反向名称解析文件

DNS服务器[Bind9](https://www.isc.org/bind/)在基于Linux的发行版中非常常用。其本地配置文件（`named.conf`）大致分为两个部分，首先是用于通用设置的选项部分，其次是各个域的区域条目。本地配置文件通常是：

- `named.conf.local`
- `named.conf.options`
- `named.conf.log`

它包含相关的RFC，我们可以根据需求和不同域的各个区域来定制服务器和域结构。配置文件`named.conf`分为几个控制域名服务器行为的选项。区分`全局选项`和`区域选项`。

全局选项是通用的，影响所有区域。区域选项只影响其分配的区域。named.conf中未列出的选项具有默认值。如果一个选项既是全局的又是特定于区域的，则区域选项优先。

#### 本地DNS配置

本地DNS配置

```shell-session
root@bind9:~# cat /etc/bind/named.conf.local

//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";
zone "domain.com" {
    type master;
    file "/etc/bind/db.domain.com";
    allow-update { key rndc-key; };
};
```

在此文件中，我们可以定义不同的区域。这些区域被分成单独的文件，在大多数情况下主要用于一个域。例外情况是ISP和公共DNS服务器。此外，许多不同的选项可以扩展或减少功能。我们可以在Bind9的[文档](https://wiki.debian.org/Bind9)中查找这些选项。

`区域文件`是使用BIND文件格式描述DNS区域的文本文件。换句话说，它是DNS树中的委托点。BIND文件格式是行业首选的区域文件格式，现已在DNS服务器软件中得到良好确立。区域文件完整地描述一个区域。必须恰好有一条`SOA`记录和至少一条`NS`记录。SOA资源记录通常位于区域文件的开头。这些全局规则的主要目标是提高区域文件的可读性。语法错误通常会导致整个区域文件被视为不可用。域名服务器的行为就像这个区域不存在一样。它会用`SERVFAIL`错误消息响应DNS查询。

简而言之，这里根据BIND格式输入所有`正向记录`。这允许DNS服务器识别IP地址属于哪个域、主机名和角色。简单来说，这就是DNS服务器查找其搜索的域的地址的电话簿。

#### 区域文件

区域文件

```shell-session
root@bind9:~# cat /etc/bind/db.domain.com

;
; BIND reverse data file for local loopback interface
;
$ORIGIN domain.com
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

      IN     MX     10     mx.domain.com.
      IN     MX     20     mx2.domain.com.

             IN     A       10.129.14.5

server1      IN     A       10.129.14.5
server2      IN     A       10.129.14.7
ns1          IN     A       10.129.14.2
ns2          IN     A       10.129.14.3

ftp          IN     CNAME   server1
mx           IN     CNAME   server1
mx2          IN     CNAME   server2
www          IN     CNAME   server2
```

为了从`完全限定域名`（`FQDN`，Fully Qualified Domain Name）解析IP地址，DNS服务器必须有一个反向查找文件。在此文件中，计算机名称（FQDN）使用`PTR`记录分配给IP地址的最后一个八位字节，该八位字节对应于相应的主机。PTR记录负责将IP地址反向转换为名称，正如我们在上表中已经看到的那样。

#### 反向名称解析区域文件

反向名称解析区域文件

```shell-session
root@bind9:~# cat /etc/bind/db.10.129.14

;
; BIND reverse data file for local loopback interface
;
$ORIGIN 14.129.10.in-addr.arpa
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

5    IN     PTR    server1.domain.com.
7    IN     MX     mx.domain.com.
...SNIP...
```

---

## 危险设置

DNS服务器可以通过多种方式被攻击。例如，针对BIND9服务器的漏洞列表可以在[CVEdetails](https://www.cvedetails.com/product/144/ISC-Bind.html?vendor_id=64)上找到。此外，SecurityTrails提供了一个简短的[列表](https://securitytrails.com/blog/most-popular-types-dns-attacks)，介绍了针对DNS服务器最流行的攻击。

我们在下面可以看到的一些设置会导致这些漏洞等问题。因为DNS可能变得非常复杂，错误很容易潜入此服务，迫使管理员绕过问题，直到找到确切的解决方案。这通常导致某些元素被释放，以便基础设施的部分按计划和预期运行。在这种情况下，功能的优先级高于安全性，这导致错误配置和漏洞。

|**选项**|**描述**|
|---|---|
|`allow-query`|定义允许哪些主机向DNS服务器发送请求。|
|`allow-recursion`|定义允许哪些主机向DNS服务器发送递归请求。|
|`allow-transfer`|定义允许哪些主机从DNS服务器接收区域传送。|
|`zone-statistics`|收集区域的统计数据。|

---

## 服务信息收集

对DNS服务器的信息收集是作为我们发送的请求的结果完成的。因此，首先，可以查询DNS服务器以了解其他已知的域名服务器。我们使用NS记录和使用`@`字符指定我们要查询的DNS服务器来完成此操作。这是因为如果存在其他DNS服务器，我们也可以使用它们并查询记录。然而，其他DNS服务器可能配置不同，此外，可能永久用于其他区域。

#### DIG - NS查询

DIG - NS查询

```shell-session
tr01ax@htb[/htb]$ dig ns inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> ns inlanefreight.htb @10.129.14.128
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45010
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: ce4d8681b32abaea0100000061475f73842c401c391690c7 (good)
;; QUESTION SECTION:
;inlanefreight.htb.             IN      NS

;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136

;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:04:03 CEST 2021
;; MSG SIZE  rcvd: 107
```

有时也可以使用CHAOS类查询和TXT类型来查询DNS服务器的版本。但是，此条目必须存在于DNS服务器上。为此，我们可以使用以下命令：

#### DIG - 版本查询

DIG - 版本查询

```shell-session
tr01ax@htb[/htb]$ dig CH TXT version.bind 10.129.120.85

; <<>> DiG 9.10.6 <<>> CH TXT version.bind
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 47786
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; ANSWER SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1"

;; ADDITIONAL SECTION:
version.bind.       0       CH      TXT     "9.10.6-P1-Debian"

;; Query time: 2 msec
;; SERVER: 10.129.120.85#53(10.129.120.85)
;; WHEN: Wed Jan 05 20:23:14 UTC 2023
;; MSG SIZE  rcvd: 101
```

我们可以使用`ANY`选项来查看所有可用记录。这将导致服务器向我们显示它愿意公开的所有可用条目。需要注意的是，并非区域中的所有条目都会显示。

#### DIG - ANY查询

DIG - ANY查询

```shell-session
tr01ax@htb[/htb]$ dig any inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> any inlanefreight.htb @10.129.14.128
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7649
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 2

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 064b7e1f091b95120100000061476865a6026d01f87d10ca (good)
;; QUESTION SECTION:
;inlanefreight.htb.             IN      ANY

;; ANSWER SECTION:
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.

;; ADDITIONAL SECTION:
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136

;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:42:13 CEST 2021
;; MSG SIZE  rcvd: 437
```

`区域传送`（Zone transfer）是指在DNS中将区域传输到另一台服务器，这通常通过TCP端口53进行。此过程缩写为`异步完整区域传送`（`AXFR`，Asynchronous Full Transfer Zone）。由于DNS故障通常会对公司产生严重后果，区域文件几乎总是在多台域名服务器上保持相同。当进行更改时，必须确保所有服务器具有相同的数据。服务器之间的同步通过区域传送实现。使用我们在默认配置中最初看到的密钥`rndc-key`，服务器确保它们与自己的主服务器或从服务器通信。区域传送涉及文件或记录的传输以及检测相关服务器数据集中的差异。

区域的原始数据位于DNS服务器上，该服务器被称为该区域的`主`域名服务器。但是，为了提高可靠性、实现简单的负载分配或保护主服务器免受攻击，在实践中几乎所有情况下都会安装一台或多台额外的服务器，这些服务器被称为该区域的`辅助`域名服务器。对于某些`顶级域名`（`TLD`），强制要求`二级域名`的区域文件至少可在两台服务器上访问。

DNS条目通常只在主服务器上创建、修改或删除。这可以通过手动编辑相关区域文件或通过数据库的动态更新自动完成。作为区域文件同步直接来源的DNS服务器称为主控服务器（master）。从主控服务器获取区域数据的DNS服务器称为从属服务器（slave）。主服务器总是主控服务器，而辅助服务器可以同时是从属服务器和主控服务器。

从属服务器在一定间隔（所谓的刷新时间，通常为一小时）从主控服务器获取相关区域的`SOA`记录，并比较序列号。如果主控服务器的SOA记录的序列号大于从属服务器的序列号，则数据集不再匹配。

#### DIG - AXFR区域传送

DIG - AXFR区域传送

```shell-session
tr01ax@htb[/htb]$ dig axfr inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> axfr inlanefreight.htb @10.129.14.128
;; global options: +cmd
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
inlanefreight.htb.      604800  IN      TXT     "MS=ms97310371"
inlanefreight.htb.      604800  IN      TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
inlanefreight.htb.      604800  IN      TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
inlanefreight.htb.      604800  IN      NS      ns.inlanefreight.htb.
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
internal.inlanefreight.htb. 604800 IN   A       10.129.1.6
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
inlanefreight.htb.      604800  IN      SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 4 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:51:19 CEST 2021
;; XFR size: 9 records (messages 1, bytes 520)
```

如果管理员为了测试目的或作为变通解决方案在`allow-transfer`选项中使用了子网，或将其设置为`any`，则任何人都可以在DNS服务器上查询整个区域文件。此外，可以查询其他区域，这甚至可能显示内部IP地址和主机名。

#### DIG - AXFR区域传送 - 内部

DIG - AXFR区域传送 - 内部

```shell-session
tr01ax@htb[/htb]$ dig axfr internal.inlanefreight.htb @10.129.14.128

; <<>> DiG 9.16.1-Ubuntu <<>> axfr internal.inlanefreight.htb @10.129.14.128
;; global options: +cmd
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
internal.inlanefreight.htb. 604800 IN   TXT     "MS=ms97310371"
internal.inlanefreight.htb. 604800 IN   TXT     "atlassian-domain-verification=t1rKCy68JFszSdCKVpw64A1QksWdXuYFUeSXKU"
internal.inlanefreight.htb. 604800 IN   TXT     "v=spf1 include:mailgun.org include:_spf.google.com include:spf.protection.outlook.com include:_spf.atlassian.net ip4:10.129.124.8 ip4:10.129.127.2 ip4:10.129.42.106 ~all"
internal.inlanefreight.htb. 604800 IN   NS      ns.inlanefreight.htb.
dc1.internal.inlanefreight.htb. 604800 IN A     10.129.34.16
dc2.internal.inlanefreight.htb. 604800 IN A     10.129.34.11
mail1.internal.inlanefreight.htb. 604800 IN A   10.129.18.200
ns.internal.inlanefreight.htb. 604800 IN A      10.129.34.136
vpn.internal.inlanefreight.htb. 604800 IN A     10.129.1.6
ws1.internal.inlanefreight.htb. 604800 IN A     10.129.1.34
ws2.internal.inlanefreight.htb. 604800 IN A     10.129.1.35
wsus.internal.inlanefreight.htb. 604800 IN A    10.129.18.2
internal.inlanefreight.htb. 604800 IN   SOA     inlanefreight.htb. root.inlanefreight.htb. 2 604800 86400 2419200 604800
;; Query time: 0 msec
;; SERVER: 10.129.14.128#53(10.129.14.128)
;; WHEN: So Sep 19 18:53:11 CEST 2021
;; XFR size: 15 records (messages 1, bytes 664)
```

也可以借助暴力攻击找出各个带有主机名的`A`记录。为此，我们需要一个可能的主机名列表，用于按顺序发送请求。例如，[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/subdomains-top1million-5000.txt)提供了这样的列表。

一种选择是在Bash中执行`for循环`，列出这些条目并将相应的查询发送到所需的DNS服务器。

#### 子域名暴力破解

子域名暴力破解

```shell-session
tr01ax@htb[/htb]$ for sub in $(cat /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.14.128 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done

ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
```

许多不同的工具可用于此目的，它们大多以相同的方式工作。其中一个工具是[DNSenum](https://github.com/fwaeytens/dnsenum)。

子域名暴力破解

```shell-session
tr01ax@htb[/htb]$ dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb

dnsenum VERSION:1.2.6

-----   inlanefreight.htb   -----


Host's addresses:
__________________



Name Servers:
______________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136


Mail (MX) Servers:
___________________



Trying Zone Transfers and getting Bind Versions:
_________________________________________________

unresolvable name: ns.inlanefreight.htb at /usr/bin/dnsenum line 900 thread 1.

Trying Zone Transfer for inlanefreight.htb on ns.inlanefreight.htb ...
AXFR record query failed: no nameservers


Brute forcing with /home/cry0l1t3/Pentesting/SecLists/Discovery/DNS/subdomains-top1million-110000.txt:
```
_______________________________________________________________________________________________________

ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136
mail1.inlanefreight.htb.                 604800   IN    A        10.129.18.201
app.inlanefreight.htb.                   604800   IN    A        10.129.18.15
ns.inlanefreight.htb.                    604800   IN    A        10.129.34.136

...SNIP...
done.
```#footprinting #enumeration #smtp #hacking #port25 #port587
source: https://academy.hackthebox.com/module/112/section/1072
--> [[notes about footprinting]]
# SMTP（简单邮件传输协议）

---

`简单邮件传输协议`（`SMTP`，Simple Mail Transfer Protocol）是一种用于在 IP 网络中发送电子邮件的协议。它可以在电子邮件客户端和发送邮件服务器之间使用，也可以在两个 SMTP 服务器之间使用。SMTP 通常与 IMAP 或 POP3 协议结合使用，后者可以获取和发送电子邮件。原则上，它是一种基于客户端-服务器的协议，尽管 SMTP 可以在客户端和服务器之间以及两个 SMTP 服务器之间使用。在这种情况下，服务器实际上充当客户端的角色。

默认情况下，SMTP 服务器在端口 `25` 上接受连接请求。然而，较新的 SMTP 服务器也使用其他端口，如 TCP 端口 `587`。此端口用于接收来自经过身份验证的用户/服务器的邮件，通常使用 STARTTLS 命令将现有的明文连接切换为加密连接。身份验证数据受到保护，不再以明文形式在网络上可见。在连接开始时，当客户端使用用户名和密码确认其身份时进行身份验证。然后可以传输电子邮件。为此，客户端向服务器发送发件人和收件人地址、电子邮件内容以及其他信息和参数。电子邮件传输完成后，连接再次终止。然后电子邮件服务器开始将电子邮件发送到另一个 SMTP 服务器。

在没有进一步措施的情况下，SMTP 以未加密方式工作，并以明文形式传输所有命令、数据或身份验证信息。为了防止未经授权的数据读取，SMTP 与 SSL/TLS 加密一起使用。在某些情况下，服务器对加密连接使用标准 TCP 端口 `25` 以外的端口，例如 TCP 端口 `465`。

SMTP 服务器的一个重要功能是通过身份验证机制防止垃圾邮件，该机制仅允许授权用户发送电子邮件。为此，大多数现代 SMTP 服务器支持带有 SMTP-Auth 的协议扩展 ESMTP（扩展 SMTP）。在发送电子邮件后，SMTP 客户端（也称为 `邮件用户代理`（`MUA`，Mail User Agent））将其转换为邮件头和邮件正文，并将两者上传到 SMTP 服务器。服务器有一个所谓的 `邮件传输代理`（`MTA`，Mail Transfer Agent），这是发送和接收电子邮件的软件基础。MTA 检查电子邮件的大小和垃圾邮件，然后存储它。为了减轻 MTA 的负担，有时会在其前面放置一个 `邮件提交代理`（`MSA`，Mail Submission Agent），用于检查电子邮件的有效性，即来源。这个 `MSA` 也称为 `中继`（Relay）服务器。这些在后面非常重要，因为由于配置不正确，可以在许多 SMTP 服务器上进行所谓的 `开放中继攻击`（Open Relay Attack）。我们稍后将讨论这种攻击以及如何识别其弱点。然后 MTA 在 DNS 中搜索收件人邮件服务器的 IP 地址。

到达目标 SMTP 服务器后，数据包被重新组装成完整的电子邮件。从那里，`邮件投递代理`（`MDA`，Mail Delivery Agent）将其传输到收件人的邮箱。

|客户端（`MUA`）|`➞`|提交代理（`MSA`）|`➞`|开放中继（`MTA`）|`➞`|邮件投递代理（`MDA`）|`➞`|邮箱（`POP3`/`IMAP`）|
|---|---|---|---|---|---|---|---|---|

但 SMTP 有两个网络协议固有的缺点。

1. 第一个是使用 SMTP 发送电子邮件不会返回可用的投递确认。尽管协议规范提供了这种类型的通知，但默认情况下未指定其格式，因此通常只返回英文错误消息，包括未投递邮件的邮件头。

2. 当建立连接时，用户未经身份验证，因此电子邮件的发件人是不可靠的。因此，开放 SMTP 中继经常被滥用来大量发送垃圾邮件。发起者使用任意的虚假发件人地址以避免被追踪（邮件欺骗）。如今，使用许多不同的安全技术来防止 SMTP 服务器被滥用。例如，可疑电子邮件被拒绝或移至隔离区（垃圾邮件文件夹）。例如，负责此功能的有身份识别协议 [DomainKeys](http://dkim.org/)（`DKIM`）和[发件人策略框架](https://dmarcian.com/what-is-spf/)（`SPF`）。


为此，开发了一个名为 `扩展 SMTP`（`ESMTP`，Extended SMTP）的 SMTP 扩展。当人们一般谈论 SMTP 时，通常指的是 ESMTP。ESMTP 使用 TLS，这是在 `EHLO` 命令之后通过发送 `STARTTLS` 完成的。这将初始化 SSL 保护的 SMTP 连接，从这一刻起，整个连接都被加密，因此或多或少是安全的。现在 [AUTH PLAIN](https://www.samlogic.net/articles/smtp-commands-reference-auth.htm) 扩展也可以安全地用于身份验证。

---

## 默认配置

每个 SMTP 服务器都可以以多种方式配置，就像所有其他服务一样。然而，存在差异，因为 SMTP 服务器仅负责发送和转发电子邮件。

#### 默认配置

默认配置

```shell-session
tr01ax@htb[/htb]$ cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"

smtpd_banner = ESMTP Server
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 2
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
myhostname = mail1.inlanefreight.htb
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
smtp_generic_maps = hash:/etc/postfix/generic
mydestination = $myhostname, localhost
masquerade_domains = $myhostname
mynetworks = 127.0.0.0/8 10.129.0.0/16
mailbox_size_limit = 0
recipient_delimiter = +
smtp_bind_address = 0.0.0.0
inet_protocols = ipv4
smtpd_helo_restrictions = reject_invalid_hostname
home_mailbox = /home/postfix
```

发送和通信也通过特殊命令完成，这些命令使 SMTP 服务器执行用户所需的操作。

|**命令**|**描述**|
|---|---|
|`AUTH PLAIN`|AUTH 是用于验证客户端的服务扩展。|
|`HELO`|客户端使用其计算机名称登录，从而启动会话。|
|`MAIL FROM`|客户端指定电子邮件发件人。|
|`RCPT TO`|客户端指定电子邮件收件人。|
|`DATA`|客户端发起电子邮件的传输。|
|`RSET`|客户端中止已发起的传输，但保持客户端和服务器之间的连接。|
|`VRFY`|客户端检查邮箱是否可用于邮件传输。|
|`EXPN`|客户端也使用此命令检查邮箱是否可用于消息传递。|
|`NOOP`|客户端请求服务器响应以防止因超时而断开连接。|
|`QUIT`|客户端终止会话。|

要与 SMTP 服务器交互，我们可以使用 `telnet` 工具来初始化与 SMTP 服务器的 TCP 连接。会话的实际初始化是通过上面提到的命令 `HELO` 或 `EHLO` 完成的。

#### Telnet - HELO/EHLO

Telnet - HELO/EHLO

```shell-session
tr01ax@htb[/htb]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server


HELO mail1.inlanefreight.htb

250 mail1.inlanefreight.htb


EHLO mail1

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
```

命令 `VRFY` 可用于枚举系统上的现有用户。然而，这并不总是有效。根据 SMTP 服务器的配置方式，SMTP 服务器可能会发出 `code 252` 并确认系统上不存在的用户的存在。所有 SMTP 响应代码的列表可以在[这里](https://serversmtp.com/smtp-error/)找到。

#### Telnet - VRFY

Telnet - VRFY

```shell-session
tr01ax@htb[/htb]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server

VRFY root

252 2.0.0 root


VRFY cry0l1t3

252 2.0.0 cry0l1t3


VRFY testuser

252 2.0.0 testuser


VRFY aaaaaaaaaaaaaaaaaaaaaaaaaaaa

252 2.0.0 aaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

因此，永远不应该完全依赖自动化工具的结果。毕竟，它们执行预配置的命令，但没有任何功能明确说明管理员如何配置被测试的服务器。

有时我们可能必须通过 Web 代理工作。我们也可以让这个 Web 代理连接到 SMTP 服务器。我们发送的命令看起来像这样：`CONNECT 10.129.14.128:25 HTTP/1.0`

我们在命令行中输入的所有发送电子邮件的命令，我们从 Thunderbird、Gmail、Outlook 和许多其他电子邮件客户端程序中都知道。我们指定 `subject`（主题）、电子邮件应该发送给谁、CC（抄送）、BCC（密送）以及我们想要与他人分享的信息。当然，从命令行也可以执行同样的操作。

#### 发送电子邮件

发送电子邮件

```shell-session
tr01ax@htb[/htb]$ telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server


EHLO inlanefreight.htb

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING


MAIL FROM: <cry0l1t3@inlanefreight.htb>

250 2.1.0 Ok


RCPT TO: <mrb3n@inlanefreight.htb> NOTIFY=success,failure

250 2.1.5 Ok


DATA

354 End data with <CR><LF>.<CR><LF>

From: <cry0l1t3@inlanefreight.htb>
To: <mrb3n@inlanefreight.htb>
Subject: DB
Date: Tue, 28 Sept 2021 16:32:51 +0200
Hey man, I am trying to access our XY-DB but the creds don't work.
Did you make any changes there?
.

250 2.0.0 Ok: queued as 6E1CF1681AB


QUIT

221 2.0.0 Bye
Connection closed by foreign host.
```

邮件头是电子邮件中大量有趣信息的载体。除其他外，它提供了有关发件人和收件人、发送和到达时间、电子邮件在途中经过的站点、消息的内容和格式以及发件人和收件人的信息。

其中一些信息是强制性的，例如发件人信息和电子邮件创建时间。其他信息是可选的。但是，邮件头不包含技术投递所需的任何信息。它作为传输协议的一部分传输。发件人和收件人都可以访问电子邮件的邮件头，尽管它乍一看不可见。电子邮件头的结构由 [RFC5322](https://datatracker.ietf.org/doc/html/rfc5322) 定义。

---

## 危险设置

为了防止发送的电子邮件被垃圾邮件过滤器过滤并且无法到达收件人，发件人可以使用收件人信任的中继服务器。它是所有其他服务器都知道和验证的 SMTP 服务器。通常，发件人必须在使用中继服务器之前对自己进行身份验证。

通常，管理员对他们必须允许哪些 IP 范围没有概览。这导致 SMTP 服务器配置错误，我们在外部和内部渗透测试中仍然经常发现这种情况。因此，他们允许所有 IP 地址，以免在电子邮件流量中导致错误，从而不会干扰或无意中中断与潜在和现有客户的通信。

#### 开放中继配置

开放中继配置

```shell-session
mynetworks = 0.0.0.0/0
```

通过此设置，此 SMTP 服务器可以发送伪造的电子邮件，从而初始化多方之间的通信。另一种攻击可能是欺骗电子邮件并读取它。

---

## 服务信息收集

默认的 Nmap 脚本包括 `smtp-commands`，它使用 `EHLO` 命令列出可以在目标 SMTP 服务器上执行的所有可能命令。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -sC -sV -p25

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00025s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING,
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.09 seconds
```

然而，我们也可以使用 [smtp-open-relay](https://nmap.org/nsedoc/scripts/smtp-open-relay.html) NSE 脚本通过 16 种不同的测试来识别目标 SMTP 服务器是否为开放中继。如果我们还详细打印扫描输出，我们还将能够看到脚本正在运行哪些测试。

#### Nmap - 开放中继

Nmap - 开放中继

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-30 02:29 CEST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Initiating ARP Ping Scan at 02:29
Scanning 10.129.14.128 [1 port]
Completed ARP Ping Scan at 02:29, 0.06s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 02:29
Completed Parallel DNS resolution of 1 host. at 02:29, 0.03s elapsed
Initiating SYN Stealth Scan at 02:29
Scanning 10.129.14.128 [1 port]
Discovered open port 25/tcp on 10.129.14.128
Completed SYN Stealth Scan at 02:29, 0.06s elapsed (1 total ports)
NSE: Script scanning 10.129.14.128.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.07s elapsed
Nmap scan report for 10.129.14.128
Host is up (0.00020s latency).

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-open-relay: Server is an open relay (16/16 tests)
|  MAIL FROM:<> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@nmap.scanme.org> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@ESMTP> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest%nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org"@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@[10.129.14.128]:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@ESMTP:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@[10.129.14.128]>
|_ MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@ESMTP>
MAC Address: 00:00:00:00:00:00 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.48 seconds
           Raw packets sent: 2 (72B) | Rcvd: 2 (72B)
```#imap #port110 #port143 #port993 #port995 #pop3 #enumeration #footprinting #hacking [source](https://academy.hackthebox.com/module/112/section/1073) --> [[notes about footprinting]]

# IMAP / POP3

---

借助 `互联网消息访问协议`（`IMAP`，Internet Message Access Protocol），可以从邮件服务器访问电子邮件。与 `邮局协议`（`POP3`，Post Office Protocol）不同，IMAP 允许直接在服务器上在线管理电子邮件并支持文件夹结构。因此，它是一种用于在远程服务器上在线管理电子邮件的网络协议。该协议基于客户端-服务器模式，允许本地电子邮件客户端与服务器上的邮箱同步，为电子邮件提供一种网络文件系统，允许跨多个独立客户端进行无问题同步。另一方面，POP3 没有与 IMAP 相同的功能，它仅提供在电子邮件服务器上列出、检索和删除电子邮件的功能。因此，对于其他功能，如直接在邮件服务器上的分层邮箱、在会话期间访问多个邮箱以及电子邮件预选，必须使用 IMAP 等协议。

客户端在线访问这些结构并可以创建本地副本。即使跨多个客户端，这也会产生统一的数据库。电子邮件保留在服务器上直到被删除。IMAP 是基于文本的，具有扩展功能，例如直接在服务器上浏览电子邮件。多个用户也可以同时访问电子邮件服务器。如果没有与服务器的活动连接，则无法管理电子邮件。但是，一些客户端提供离线模式，带有邮箱的本地副本。当重新建立连接时，客户端会同步所有离线本地更改。

客户端通过端口 `143` 建立与服务器的连接。对于通信，它使用 `ASCII` 格式的基于文本的命令。可以连续发送多个命令，而无需等待服务器的确认。稍后来自服务器的确认可以使用与命令一起发送的标识符分配给各个命令。连接建立后，用户立即通过用户名和密码向服务器进行身份验证。只有在成功身份验证后才能访问所需的邮箱。

SMTP 通常用于发送电子邮件。通过将已发送的电子邮件复制到 IMAP 文件夹，所有客户端都可以访问所有已发送的邮件，无论它们是从哪台计算机发送的。互联网消息访问协议的另一个优点是可以在邮箱中创建个人文件夹和文件夹结构。此功能使邮箱更清晰、更易于管理。但是，电子邮件服务器上的存储空间需求会增加。

在没有进一步措施的情况下，IMAP 以未加密方式工作，并以明文形式传输命令、电子邮件或用户名和密码。许多电子邮件服务器要求建立加密的 IMAP 会话，以确保电子邮件流量中的更高安全性并防止未经授权访问邮箱。通常使用 SSL/TLS 来实现此目的。根据使用的方法和实现，加密连接使用标准端口 `143` 或替代端口，如 `993`。

---

## 默认配置

IMAP 和 POP3 都有大量的配置选项，这使得很难更详细地深入研究每个组件。如果您希望更深入地检查这些协议配置，我们建议在本地创建一个虚拟机，并使用 `apt` 安装 `dovecot-imapd` 和 `dovecot-pop3d` 两个软件包，然后摆弄配置并进行实验。

在 Dovecot 的文档中，我们可以找到可用于实验的各个[核心设置](https://doc.dovecot.org/settings/core/)和[服务配置](https://doc.dovecot.org/configuration_manual/service_configuration/)选项。但是，让我们看看命令列表，看看如何使用命令行直接与 IMAP 和 POP3 交互和通信。

#### IMAP 命令

|**命令**|**描述**|
|---|---|
|`1 LOGIN username password`|用户登录。|
|`1 LIST "" *`|列出所有目录。|
|`1 CREATE "INBOX"`|创建具有指定名称的邮箱。|
|`1 DELETE "INBOX"`|删除邮箱。|
|`1 RENAME "ToRead" "Important"`|重命名邮箱。|
|`1 LSUB "" *`|从用户已声明为 `active`（活动）或 `subscribed`（已订阅）的名称集中返回名称子集。|
|`1 SELECT INBOX`|选择邮箱以便可以访问邮箱中的消息。|
|`1 UNSELECT INBOX`|退出选定的邮箱。|
|`1 FETCH <ID> all`|检索与邮箱中消息关联的数据。|
|`1 CLOSE`|删除所有设置了 `Deleted`（已删除）标志的消息。|
|`1 LOGOUT`|关闭与 IMAP 服务器的连接。|

#### POP3 命令

|**命令**|**描述**|
|---|---|
|`USER username`|标识用户。|
|`PASS password`|使用密码对用户进行身份验证。|
|`STAT`|从服务器请求已保存电子邮件的数量。|
|`LIST`|从服务器请求所有电子邮件的数量和大小。|
|`RETR id`|请求服务器按 ID 传递请求的电子邮件。|
|`DELE id`|请求服务器按 ID 删除请求的电子邮件。|
|`CAPA`|请求服务器显示服务器功能。|
|`RSET`|请求服务器重置传输的信息。|
|`QUIT`|关闭与 POP3 服务器的连接。|

---

## 危险设置

尽管如此，配置不当的配置选项可能允许我们获取更多信息，例如调试服务上执行的命令或以匿名方式登录，类似于 FTP 服务。大多数公司使用第三方电子邮件提供商，如 Google、Microsoft 等。但是，出于许多不同的原因，一些公司仍然使用自己的邮件服务器。其中一个原因是保持他们想要掌握在自己手中的隐私。管理员可能会犯许多配置错误，在最坏的情况下，这将允许我们读取所有发送和接收的电子邮件，其中甚至可能包含机密或敏感信息。其中一些配置选项包括：

|**设置**|**描述**|
|---|---|
|`auth_debug`|启用所有身份验证调试日志记录。|
|`auth_debug_passwords`|此设置调整日志详细程度，提交的密码和方案会被记录。|
|`auth_verbose`|记录不成功的身份验证尝试及其原因。|
|`auth_verbose_passwords`|用于身份验证的密码会被记录，也可以被截断。|
|`auth_anonymous_username`|这指定使用 ANONYMOUS SASL 机制登录时要使用的用户名。|

---

## 服务信息收集

默认情况下，端口 `110`、`143`、`993` 和 `995` 用于 IMAP 和 POP3。两个较高的端口使用 `TLS/SSL` 加密客户端和服务器之间的通信。使用 Nmap，我们可以扫描服务器的这些端口。如果服务器使用嵌入式 SSL 证书，扫描将返回如下所示的相应信息。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -sV -p110,143,993,995 -sC

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-19 22:09 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00026s latency).

PORT    STATE SERVICE  VERSION
110/tcp open  pop3     Dovecot pop3d
|_pop3-capabilities: AUTH-RESP-CODE SASL STLS TOP UIDL RESP-CODES CAPA PIPELINING
| ssl-cert: Subject: commonName=mail1.inlanefreight.htb/organizationName=Inlanefreight/stateOrProvinceName=California/countryName=US
| Not valid before: 2021-09-19T19:44:58
|_Not valid after:  2295-07-04T19:44:58
143/tcp open  imap     Dovecot imapd
|_imap-capabilities: more have post-login STARTTLS Pre-login capabilities LITERAL+ LOGIN-REFERRALS OK LOGINDISABLEDA0001 SASL-IR ENABLE listed IDLE ID IMAP4rev1
| ssl-cert: Subject: commonName=mail1.inlanefreight.htb/organizationName=Inlanefreight/stateOrProvinceName=California/countryName=US
| Not valid before: 2021-09-19T19:44:58
|_Not valid after:  2295-07-04T19:44:58
993/tcp open  ssl/imap Dovecot imapd
|_imap-capabilities: more have post-login OK capabilities LITERAL+ LOGIN-REFERRALS Pre-login AUTH=PLAINA0001 SASL-IR ENABLE listed IDLE ID IMAP4rev1
| ssl-cert: Subject: commonName=mail1.inlanefreight.htb/organizationName=Inlanefreight/stateOrProvinceName=California/countryName=US
| Not valid before: 2021-09-19T19:44:58
|_Not valid after:  2295-07-04T19:44:58
995/tcp open  ssl/pop3 Dovecot pop3d
|_pop3-capabilities: AUTH-RESP-CODE USER SASL(PLAIN) TOP UIDL RESP-CODES CAPA PIPELINING
| ssl-cert: Subject: commonName=mail1.inlanefreight.htb/organizationName=Inlanefreight/stateOrProvinceName=California/countryName=US
| Not valid before: 2021-09-19T19:44:58
|_Not valid after:  2295-07-04T19:44:58
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.74 seconds
```

例如，从输出中，我们可以看到通用名称是 `mail1.inlanefreight.htb`，电子邮件服务器属于位于加利福尼亚州的 `Inlanefreight` 组织。显示的功能向我们展示了相应端口上服务器和服务可用的命令。

如果我们成功获取到某个员工的访问凭据，攻击者可以登录邮件服务器并读取甚至发送单独的消息。

#### cURL

cURL

```shell-session
tr01ax@htb[/htb]$ curl -k 'imaps://10.129.14.128' --user user:p4ssw0rd

* LIST (\HasNoChildren) "." Important
* LIST (\HasNoChildren) "." INBOX
```

如果我们还使用 `verbose`（详细）（`-v`）选项，我们将看到连接是如何建立的。从中，我们可以看到用于加密的 TLS 版本、SSL 证书的更多详细信息，甚至是通常包含邮件服务器版本的横幅。

cURL

```shell-session
tr01ax@htb[/htb]$ curl -k 'imaps://10.129.14.128' --user cry0l1t3:1234 -v

*   Trying 10.129.14.128:993...
* TCP_NODELAY set
* Connected to 10.129.14.128 (10.129.14.128) port 993 (#0)
* successfully set certificate verify locations:
*   CAfile: /etc/ssl/certs/ca-certificates.crt
  CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: C=US; ST=California; L=Sacramento; O=Inlanefreight; OU=Customer Support; CN=mail1.inlanefreight.htb; emailAddress=cry0l1t3@inlanefreight.htb
*  start date: Sep 19 19:44:58 2021 GMT
*  expire date: Jul  4 19:44:58 2295 GMT
*  issuer: C=US; ST=California; L=Sacramento; O=Inlanefreight; OU=Customer Support; CN=mail1.inlanefreight.htb; emailAddress=cry0l1t3@inlanefreight.htb
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
< * OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] HTB-Academy IMAP4 v.0.21.4
> A001 CAPABILITY
< * CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN
< A001 OK Pre-login capabilities listed, post-login capabilities have more.
> A002 AUTHENTICATE PLAIN AGNyeTBsMXQzADEyMzQ=
< * CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY MOVE SNIPPET=FUZZY PREVIEW=FUZZY LITERAL+ NOTIFY SPECIAL-USE
< A002 OK Logged in
> A003 LIST "" *
< * LIST (\HasNoChildren) "." Important
* LIST (\HasNoChildren) "." Important
< * LIST (\HasNoChildren) "." INBOX
* LIST (\HasNoChildren) "." INBOX
< A003 OK List completed (0.001 + 0.000 secs).
* Connection #0 to host 10.129.14.128 left intact
```

要通过 SSL 与 IMAP 或 POP3 服务器交互，我们可以使用 `openssl`，以及 `ncat`。用于此的命令如下所示：

#### OpenSSL - TLS 加密交互 POP3

OpenSSL - TLS 加密交互 POP3

```shell-session
tr01ax@htb[/htb]$ openssl s_client -connect 10.129.14.128:pop3s

CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb
verify error:num=18:self signed certificate
verify return:1
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb
verify return:1
---
Certificate chain
 0 s:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb

...SNIP...

---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 3CC39A7F2928B252EF2FFA5462140B1A0A74B29D4708AA8DE1515BB4033D92C2
    Session-ID-ctx:
    Resumption PSK: 68419D933B5FEBD878FF1BA399A926813BEA3652555E05F0EC75D65819A263AA25FA672F8974C37F6446446BB7EA83F9
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - d7 86 ac 7e f3 f4 95 35-88 40 a5 b5 d6 a6 41 e4   ...~...5.@....A.
    0010 - 96 6c e6 12 4f 50 ce 72-36 25 df e1 72 d9 23 94   .l..OP.r6%..r.#.
    0020 - cc 29 90 08 58 1b 57 ab-db a8 6b f7 8f 31 5b ad   .)..X.W...k..1[.
    0030 - 47 94 f4 67 58 1f 96 d9-ca ca 56 f9 7a 12 f6 6d   G..gX.....V.z..m
    0040 - 43 b9 b6 68 de db b2 47-4f 9f 48 14 40 45 8f 89   C..h...GO.H.@E..
    0050 - fa 19 35 9c 6d 3c a1 46-5c a2 65 ab 87 a4 fd 5e   ..5.m<.F\.e....^
    0060 - a2 95 25 d4 43 b8 71 70-40 6c fe 6f 0e d1 a0 38   ..%.C.qp@l.o...8
    0070 - 6e bd 73 91 ed 05 89 83-f5 3e d9 2a e0 2e 96 f8   n.s......>.*....
    0080 - 99 f0 50 15 e0 1b 66 db-7c 9f 10 80 4a a1 8b 24   ..P...f.|...J..$
    0090 - bb 00 03 d4 93 2b d9 95-64 44 5b c2 6b 2e 01 b5   .....+..dD[.k...
    00a0 - e8 1b f4 a4 98 a7 7a 7d-0a 80 cc 0a ad fe 6e b3   ......z}......n.
    00b0 - 0a d6 50 5d fd 9a b4 5c-28 a4 c9 36 e4 7d 2a 1e   ..P]...\(..6.}*.

    Start Time: 1632081313
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
+OK HTB-Academy POP3 Server
```

#### OpenSSL - TLS 加密交互 IMAP

OpenSSL - TLS 加密交互 IMAP

```shell-session
tr01ax@htb[/htb]$ openssl s_client -connect 10.129.14.128:imaps

CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb
verify error:num=18:self signed certificate
verify return:1
depth=0 C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb
verify return:1
---
Certificate chain
 0 s:C = US, ST = California, L = Sacramento, O = Inlanefreight, OU = Customer Support, CN = mail1.inlanefreight.htb, emailAddress = cry0l1t3@inlanefreight.htb

...SNIP...

---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 2B7148CD1B7B92BA123E06E22831FCD3B365A5EA06B2CDEF1A5F397177130699
    Session-ID-ctx:
    Resumption PSK: 4D9F082C6660646C39135F9996DDA2C199C4F7E75D65FA5303F4A0B274D78CC5BD3416C8AF50B31A34EC022B619CC633
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 68 3b b6 68 ff 85 95 7c-8a 8a 16 b2 97 1c 72 24   h;.h...|......r$
    0010 - 62 a7 84 ff c3 24 ab 99-de 45 60 26 e7 04 4a 7d   b....$...E`&..J}
    0020 - bc 6e 06 a0 ff f7 d7 41-b5 1b 49 9c 9f 36 40 8d   .n.....A..I..6@.
    0030 - 93 35 ed d9 eb 1f 14 d7-a5 f6 3f c8 52 fb 9f 29   .5........?.R..)
    0040 - 89 8d de e6 46 95 b3 32-48 80 19 bc 46 36 cb eb   ....F..2H...F6..
    0050 - 35 79 54 4c 57 f8 ee 55-06 e3 59 7f 5e 64 85 b0   5yTLW..U..Y.^d..
    0060 - f3 a4 8c a6 b6 47 e4 59-ee c9 ab 54 a4 ab 8c 01   .....G.Y...T....
    0070 - 56 bb b9 bb 3b f6 96 74-16 c9 66 e2 6c 28 c6 12   V...;..t..f.l(..
    0080 - 34 c7 63 6b ff 71 16 7f-91 69 dc 38 7a 47 46 ec   4.ck.q...i.8zGF.
    0090 - 67 b7 a2 90 8b 31 58 a0-4f 57 30 6a b6 2e 3a 21   g....1X.OW0j..:!
    00a0 - 54 c7 ba f0 a9 74 13 11-d5 d1 ec cc ea f9 54 7d   T....t........T}
    00b0 - 46 a6 33 ed 5d 24 ed b0-20 63 43 d8 8f 14 4d 62   F.3.]$.. cC...Mb

    Start Time: 1632081604
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] HTB-Academy IMAP4 v.0.21.4
```

一旦我们成功建立连接并登录到目标邮件服务器，就可以使用上述命令来操作和导航服务器。我们想指出的是，自己配置邮件服务器、进行相关研究以及与其他社区成员一起进行的实验，将为我们提供理解正在发生的通信以及哪些配置选项负责这些通信的专业知识。

在 SMTP 部分，我们发现了用户 `robin`。我们团队的另一位成员发现该用户也使用其用户名作为密码（`robin`:`robin`）。我们可以使用这些凭据尝试与 IMAP/POP3 服务进行交互。#snmp #footprinting #enumeration #hacking #port162 #port161 [source](https://academy.hackthebox.com/module/112/section/1075) --> [[notes about footprinting]]

# SNMP

---

`简单网络管理协议`（Simple Network Management Protocol，[SNMP](https://datatracker.ietf.org/doc/html/rfc1157)）是为监控网络设备而创建的。此外，该协议还可用于处理配置任务和远程更改设置。支持 SNMP 的硬件包括路由器、交换机、服务器、IoT（物联网）设备以及许多其他可以使用此标准协议查询和控制的设备。因此，它是一种用于监控和管理网络设备的协议。此外，还可以使用此标准远程处理配置任务和进行设置。当前版本是 `SNMPv3`，它特别提高了 SNMP 的安全性，但也增加了使用该协议的复杂性。

除了纯粹的信息交换外，SNMP 还通过代理在 UDP 端口 `161` 上传输控制命令。客户端可以使用这些命令在设备中设置特定值并更改选项和设置。在传统通信中，总是由客户端主动向服务器请求信息，而 SNMP 还支持通过 UDP 端口 `162` 使用所谓的 `trap`（陷阱）。这些是从 SNMP 服务器发送到客户端的数据包，无需客户端明确请求。如果设备配置得当，一旦服务器端发生特定事件，就会向客户端发送 SNMP trap。

为了使 SNMP 客户端和服务器能够交换各自的值，可用的 SNMP 对象必须具有双方都知道的唯一地址。这种寻址机制是成功传输数据和使用 SNMP 进行网络监控的绝对前提条件。

#### MIB

为确保 SNMP 访问能够跨制造商并在不同的客户端-服务器组合中工作，创建了 `管理信息库`（Management Information Base，`MIB`）。MIB 是一种独立的设备信息存储格式。MIB 是一个文本文件，其中以标准化的树形层次结构列出了设备的所有可查询 SNMP 对象。它至少包含一个 `对象标识符`（Object Identifier，`OID`），除了必要的唯一地址和名称外，还提供有关相应对象的类型、访问权限和描述的信息。MIB 文件以基于 `抽象语法标记一`（Abstract Syntax Notation One，`ASN.1`）的 ASCII 文本格式编写。MIB 不包含数据，但它们解释了在哪里可以找到哪些信息以及它们的格式、返回特定 OID 的值或使用的数据类型。

#### OID

OID 表示分层命名空间中的一个节点。一串数字唯一标识每个节点，从而可以确定节点在树中的位置。链越长，信息越具体。OID 树中的许多节点除了引用其下方的节点外，不包含任何内容。OID 由整数组成，通常通过点表示法连接。我们可以在 [Object Identifier Registry](https://www.alvestrand.no/objectid/) 中查找许多 MIB 的相关 OID。

#### SNMPv1

SNMP 版本 1（`SNMPv1`）用于网络管理和监控。SNMPv1 是该协议的第一个版本，仍在许多小型网络中使用。它支持从网络设备检索信息，允许配置设备，并提供 trap（事件通知）。然而，SNMPv1 `没有内置的身份验证`机制，这意味着任何访问网络的人都可以读取和修改网络数据。SNMPv1 的另一个主要缺陷是它`不支持加密`，这意味着所有数据都以明文形式发送，可以很容易地被拦截。

#### SNMPv2

SNMPv2 存在不同的版本。今天仍然存在的版本是 `v2c`，扩展名 `c` 表示基于社区的 SNMP。在安全性方面，SNMPv2 与 SNMPv1 处于同等水平，并且从不再使用的基于参与方的 SNMP 扩展了额外功能。然而，SNMP 协议初始执行的一个重要问题是，提供安全性的 `community string`（社区字符串）仅以明文形式传输，这意味着它没有内置加密。

#### SNMPv3

`SNMPv3` 通过安全功能大大提高了安全性，例如使用用户名和密码进行`身份验证`以及数据的传输`加密`（通过`预共享密钥`）。然而，复杂性也相应增加，配置选项比 `v2c` 多得多。

#### Community Strings（社区字符串）

Community strings 可以被视为用于确定是否可以查看所请求信息的密码。需要注意的是，许多组织仍在使用 `SNMPv2`，因为过渡到 `SNMPv3` 可能非常复杂，但服务仍需保持活动状态。这给许多管理员带来了很大的担忧，并产生了一些他们急于避免的问题。对于如何获取信息以及我们作为攻击者如何使用这些信息缺乏了解，使得管理员的做法看起来令人费解。同时，发送数据缺乏加密也是一个问题。因为每次通过网络发送 community strings 时，它们都可能被拦截和读取。

---

## 默认配置

SNMP 守护进程的默认配置定义了服务的基本设置，包括 IP 地址、端口、MIB、OID、身份验证和 community strings。

#### SNMP 守护进程配置

SNMP 守护进程配置

```shell-session
tr01ax@htb[/htb]$ cat /etc/snmp/snmpd.conf | grep -v "#" | sed -r '/^\s*$/d'

sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>
sysServices    72
master  agentx
agentaddress  127.0.0.1,[::1]
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
rocommunity  public default -V systemonly
rocommunity6 public default -V systemonly
rouser authPrivUser authpriv -V systemonly
```

此服务的配置也可以通过多种方式更改。因此，我们建议设置一个虚拟机来自己安装和配置 SNMP 服务器。可以对 SNMP 守护进程进行的所有设置都在 [manpage](http://www.net-snmp.org/docs/man/snmpd.conf.html) 中定义和描述。

---

## 危险设置

管理员可能对 SNMP 进行的一些危险设置包括：

|**设置**|**描述**|
|---|---|
|`rwuser noauth`|无需身份验证即可访问完整的 OID 树。|
|`rwcommunity <community string> <IPv4 address>`|无论请求从何处发送，都可以访问完整的 OID 树。|
|`rwcommunity6 <community string> <IPv6 address>`|与 `rwcommunity` 访问权限相同，区别在于使用 IPv6。|

---

## 服务信息收集

对于 SNMP 的信息收集，我们可以使用 `snmpwalk`、`onesixtyone` 和 `braa` 等工具。`Snmpwalk` 用于查询 OID 及其信息。`Onesixtyone` 可用于暴力破解 community strings 的名称，因为它们可以由管理员任意命名。由于这些 community strings 可以绑定到任何源，因此识别现有的 community strings 可能需要相当长的时间。

#### SNMPwalk

SNMPwalk

```shell-session
tr01ax@htb[/htb]$ snmpwalk -v2c -c public 10.129.14.128

iso.3.6.1.2.1.1.1.0 = STRING: "Linux htb 5.11.0-34-generic #36~20.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (5134) 0:00:51.34
iso.3.6.1.2.1.1.4.0 = STRING: "mrb3n@inlanefreight.htb"
iso.3.6.1.2.1.1.5.0 = STRING: "htb"
iso.3.6.1.2.1.1.6.0 = STRING: "Sitting on the Dock of the Bay"
iso.3.6.1.2.1.1.7.0 = INTEGER: 72
iso.3.6.1.2.1.1.8.0 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.13.3.1.3
iso.3.6.1.2.1.1.9.1.2.10 = OID: iso.3.6.1.2.1.92
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The management information definitions for the SNMP User-based Security Model."
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The MIB modules for managing SNMP Notification, plus filtering."
iso.3.6.1.2.1.1.9.1.3.10 = STRING: "The MIB module for logging SNMP Notifications."
iso.3.6.1.2.1.1.9.1.4.1 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.2 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.3 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.4 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.5 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.6 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.7 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.8 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.9 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.1.9.1.4.10 = Timeticks: (0) 0:00:00.00
iso.3.6.1.2.1.25.1.1.0 = Timeticks: (3676678) 10:12:46.78
iso.3.6.1.2.1.25.1.2.0 = Hex-STRING: 07 E5 09 14 0E 2B 2D 00 2B 02 00
iso.3.6.1.2.1.25.1.3.0 = INTEGER: 393216
iso.3.6.1.2.1.25.1.4.0 = STRING: "BOOT_IMAGE=/boot/vmlinuz-5.11.0-34-generic root=UUID=9a6a5c52-f92a-42ea-8ddf-940d7e0f4223 ro quiet splash"
iso.3.6.1.2.1.25.1.5.0 = Gauge32: 3
iso.3.6.1.2.1.25.1.6.0 = Gauge32: 411
iso.3.6.1.2.1.25.1.7.0 = INTEGER: 0
iso.3.6.1.2.1.25.1.7.0 = No more variables left in this MIB View (It is past the end of the MIB tree)

...SNIP...

iso.3.6.1.2.1.25.6.3.1.2.1232 = STRING: "printer-driver-sag-gdi_0.1-7_all"
iso.3.6.1.2.1.25.6.3.1.2.1233 = STRING: "printer-driver-splix_2.0.0+svn315-7fakesync1build1_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1234 = STRING: "procps_2:3.3.16-1ubuntu2.3_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1235 = STRING: "proftpd-basic_1.3.6c-2_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1236 = STRING: "proftpd-doc_1.3.6c-2_all"
iso.3.6.1.2.1.25.6.3.1.2.1237 = STRING: "psmisc_23.3-1_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1238 = STRING: "publicsuffix_20200303.0012-1_all"
iso.3.6.1.2.1.25.6.3.1.2.1239 = STRING: "pulseaudio_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1240 = STRING: "pulseaudio-module-bluetooth_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1241 = STRING: "pulseaudio-utils_1:13.99.1-1ubuntu3.12_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1242 = STRING: "python-apt-common_2.0.0ubuntu0.20.04.6_all"
iso.3.6.1.2.1.25.6.3.1.2.1243 = STRING: "python3_3.8.2-0ubuntu2_amd64"
iso.3.6.1.2.1.25.6.3.1.2.1244 = STRING: "python3-acme_1.1.0-1_all"
iso.3.6.1.2.1.25.6.3.1.2.1245 = STRING: "python3-apport_2.20.11-0ubuntu27.21_all"
iso.3.6.1.2.1.25.6.3.1.2.1246 = STRING: "python3-apt_2.0.0ubuntu0.20.04.6_amd64"

...SNIP...
```

在配置错误的情况下，我们从 `snmpwalk` 得到的结果与上面显示的大致相同。一旦我们知道 community string 并且 SNMP 服务不需要身份验证（版本 1、2c），我们就可以像前面的示例一样查询内部系统信息。

在这里我们识别到系统上安装了一些 Python 包。如果我们不知道 community string，可以使用 `onesixtyone` 和 `SecLists` 字典来识别这些 community strings。

#### OneSixtyOne

OneSixtyOne

```shell-session
tr01ax@htb[/htb]$ sudo apt install onesixtyone
tr01ax@htb[/htb]$ onesixtyone -c /opt/useful/SecLists/Discovery/SNMP/snmp.txt 10.129.14.128

Scanning 1 hosts, 3220 communities
10.129.14.128 [public] Linux htb 5.11.0-37-generic #41~20.04.2-Ubuntu SMP Fri Sep 24 09:06:38 UTC 2021 x86_64
```

通常，当某些 community strings 绑定到特定 IP 地址时，它们会以主机的主机名命名，有时甚至会在这些名称中添加符号以使它们更难被识别。然而，如果我们想象一个使用 SNMP 管理的拥有 100 多台不同服务器的大型网络，在这种情况下，标签将具有某种模式。因此，我们可以使用不同的规则来猜测它们。我们可以使用工具 [crunch](https://secf00tprint.github.io/blog/passwords/crunch/advanced/en) 来创建自定义字典。创建自定义字典不是本模块的重要部分，但可以在模块 [Cracking Passwords With Hashcat](https://academy.hackthebox.com/course/preview/cracking-passwords-with-hashcat) 中找到更多详细信息。

一旦我们知道了 community string，就可以使用 [braa](https://github.com/mteg/braa) 暴力破解各个 OID 并枚举它们背后的信息。

#### Braa

Braa

```shell-session
tr01ax@htb[/htb]$ sudo apt install braa
tr01ax@htb[/htb]$ braa <community string>@<IP>:.1.3.6.*   # Syntax
tr01ax@htb[/htb]$ braa public@10.129.14.128:.1.3.6.*

10.129.14.128:20ms:.1.3.6.1.2.1.1.1.0:Linux htb 5.11.0-34-generic #36~20.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64
10.129.14.128:20ms:.1.3.6.1.2.1.1.2.0:.1.3.6.1.4.1.8072.3.2.10
10.129.14.128:20ms:.1.3.6.1.2.1.1.3.0:548
10.129.14.128:20ms:.1.3.6.1.2.1.1.4.0:mrb3n@inlanefreight.htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.5.0:htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.6.0:US
10.129.14.128:20ms:.1.3.6.1.2.1.1.7.0:78
...SNIP...
```

我们再次想指出，独立配置 SNMP 服务将为我们带来各种不同的体验，这是任何教程都无法替代的。因此，我们强烈建议设置一个带有 SNMP 的虚拟机，进行实验并尝试不同的配置。SNMP 对于 IT 系统管理员来说可能是一个福音，但对于安全分析师和管理人员来说同样可能是一个诅咒。#mysql #footprinting #enumeration #hacking #port3306 [source](https://academy.hackthebox.com/module/112/section/1238) --> [[notes about footprinting]]

# MySQL

---

`MySQL` 是由 Oracle 开发和支持的开源 SQL 关系数据库管理系统。数据库只是为了便于使用和检索而组织的结构化数据集合。数据库系统可以高性能地快速处理大量数据。在数据库中，数据存储的方式是尽可能少地占用空间。数据库使用 [SQL 数据库语言](https://www.w3schools.com/sql/sql_intro.asp)进行控制。MySQL 按照`客户端-服务器原则`工作，由一个 MySQL 服务器和一个或多个 MySQL 客户端组成。MySQL 服务器是实际的数据库管理系统。它负责数据存储和分发。数据存储在具有不同列、行和数据类型的表中。这些数据库通常存储在扩展名为 `.sql` 的单个文件中，例如 `wordpress.sql`。

#### MySQL 客户端

MySQL 客户端可以使用结构化查询从数据库引擎检索和编辑数据。插入、删除、修改和检索数据都是使用 SQL 数据库语言完成的。因此，MySQL 适合管理许多不同的数据库，客户端可以同时向这些数据库发送多个查询。根据数据库的使用情况，可以通过内部网络或公共互联网进行访问。

数据库使用的最佳示例之一是 CMS（内容管理系统）WordPress。WordPress 将所有创建的帖子、用户名和密码存储在自己的数据库中，该数据库只能从 localhost 访问。然而，正如模块 [Introduction to Web Applications](https://academy.hackthebox.com/course/preview/introduction-to-web-applications) 中更详细解释的那样，有些数据库结构是分布在多个服务器上的。

#### MySQL 数据库

MySQL 非常适合`动态网站`等应用，其中高效的语法和快速的响应速度至关重要。它通常与 Linux 操作系统、PHP 和 Apache Web 服务器结合使用，这种组合也被称为 [LAMP](https://en.wikipedia.org/wiki/LAMP_(software_bundle))（Linux、Apache、MySQL、PHP），或者使用 Nginx 时称为 [LEMP](https://lemp.io/)。在使用 MySQL 数据库的虚拟主机中，它作为中央实例存储 PHP 脚本所需的内容。其中包括：

|||||
|---|---|---|---|
|Headers（头部）|Texts（文本）|Meta tags（元标签）|Forms（表单）|
|Customers（客户）|Usernames（用户名）|Administrators（管理员）|Moderators（版主）|
|Email addresses（电子邮件地址）|User information（用户信息）|Permissions（权限）|Passwords（密码）|
|External/Internal links（外部/内部链接）|Links to Files（文件链接）|Specific contents（特定内容）|Values（值）|

MySQL 可以以明文形式存储密码等敏感数据；但是，通常会事先由 PHP 脚本使用安全方法（如 [One-Way-Encryption](https://en.citizendium.org/wiki/One-way_encryption)，单向加密）进行加密。

#### MySQL 命令

MySQL 数据库在内部将命令转换为可执行代码并执行请求的操作。如果在处理过程中发生错误，Web 应用程序会通知用户，这可能由各种 `SQL 注入` 引发。这些错误描述通常包含重要信息，并确认 Web 应用程序与数据库的交互方式与开发人员预期的不同。

如果数据处理正确，Web 应用程序会将生成的信息发送回客户端。这些信息可以是从表中提取的数据，也可以是登录、搜索功能等后续处理所需的记录。SQL 命令可以显示、修改、添加或删除表中的行。此外，SQL 还可以更改表的结构、创建或删除关系和索引，以及管理用户。

`MariaDB` 通常与 MySQL 关联，是原始 MySQL 代码的分支。这是因为 MySQL 的首席开发人员在 `MySQL AB` 被 `Oracle` 收购后离开了公司，并基于 MySQL 的源代码开发了另一个开源 SQL 数据库管理系统，并将其命名为 MariaDB。

---

## 默认配置

SQL 数据库及其配置的管理是一个庞大的主题。它非常庞大，以至于整个职业（如`数据库管理员`）几乎只处理数据库。这些结构很快就会变得非常大，其规划可能变得复杂。数据库管理是`软件开发人员`以及`信息安全分析师`的核心能力之一。完整涵盖这一领域将超出本模块的范围。因此，我们建议设置一个 MySQL/MariaDB 实例，尝试各种配置，以更好地理解可用的功能和配置选项。让我们看一下 MySQL 的默认配置。

#### 默认配置

默认配置

```shell-session
tr01ax@htb[/htb]$ sudo apt install mysql-server -y
tr01ax@htb[/htb]$ cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep -v "#" | sed -r '/^\s*$/d'

[client]
port		= 3306
socket		= /var/run/mysqld/mysqld.sock

[mysqld_safe]
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
nice		= 0

[mysqld]
skip-host-cache
skip-name-resolve
user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
explicit_defaults_for_timestamp

symbolic-links=0

!includedir /etc/mysql/conf.d/
```

---

## 危险设置

MySQL 中有很多东西可能被错误配置。我们可以在 [MySQL reference](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html) 中更详细地查看服务器配置中可以进行哪些选项设置。与安全相关的主要选项包括：

|**设置**|**描述**|
|---|---|
|`user`|设置 MySQL 服务将以哪个用户身份运行。|
|`password`|设置 MySQL 用户的密码。|
|`admin_address`|在管理网络接口上监听 TCP/IP 连接的 IP 地址。|
|`debug`|此变量指示当前的调试设置。|
|`sql_warnings`|此变量控制单行 INSERT 语句在发生警告时是否产生信息字符串。|
|`secure_file_priv`|此变量用于限制数据导入和导出操作的影响。|

`user`、`password` 和 `admin_address` 设置与安全相关，因为这些条目是以明文形式输入的。通常，MySQL 服务器配置文件的权限分配不正确。如果我们通过其他方式读取文件甚至获得 shell，我们可以看到文件以及 MySQL 服务器的用户名和密码。假设没有其他安全措施来防止未经授权的访问。在这种情况下，可以查看甚至编辑整个数据库和所有现有客户的信息、电子邮件地址、密码和个人数据。

`debug` 和 `sql_warnings` 设置在发生错误时提供详细的信息输出，这对管理员来说至关重要，但不应该被其他人看到。这些信息通常包含敏感内容，可以通过试错法检测到以识别进一步的攻击可能性。这些错误消息通常直接显示在 Web 应用程序上。因此，SQL 注入甚至可以被操纵以使 MySQL 服务器执行系统命令。这在模块 [SQL Injection Fundamentals](https://academy.hackthebox.com/course/preview/sql-injection-fundamentals) 和 [SQLMap Essentials](https://academy.hackthebox.com/course/preview/sqlmap-essentials) 中进行了讨论和演示。

---

## 服务信息收集

MySQL 服务器可以从外部网络访问的原因有很多。然而，这远非最佳实践，我们总能找到可以访问的数据库。通常，这些设置只是暂时的，但被管理员遗忘了。这种服务器设置也可能因技术问题而被用作变通方案。通常，MySQL 服务器运行在 `TCP 端口 3306` 上，我们可以使用 `Nmap` 扫描此端口以获取更详细的信息。

#### 扫描 MySQL 服务器

扫描 MySQL 服务器

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-21 00:53 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00021s latency).

PORT     STATE SERVICE     VERSION
3306/tcp open  nagios-nsca Nagios NSCA
| mysql-brute:
|   Accounts:
|     root:<empty> - Valid credentials
|_  Statistics: Performed 45010 guesses in 5 seconds, average tps: 9002.0
|_mysql-databases: ERROR: Script execution failed (use -d to debug)
|_mysql-dump-hashes: ERROR: Script execution failed (use -d to debug)
| mysql-empty-password:
|_  root account has empty password
| mysql-enum:
|   Valid usernames:
|     root:<empty> - Valid credentials
|     netadmin:<empty> - Valid credentials
|     guest:<empty> - Valid credentials
|     user:<empty> - Valid credentials
|     web:<empty> - Valid credentials
|     sysadmin:<empty> - Valid credentials
|     administrator:<empty> - Valid credentials
|     webadmin:<empty> - Valid credentials
|     admin:<empty> - Valid credentials
|     test:<empty> - Valid credentials
|_  Statistics: Performed 10 guesses in 1 seconds, average tps: 10.0
| mysql-info:
|   Protocol: 10
|   Version: 8.0.26-0ubuntu0.20.04.1
|   Thread ID: 13
|   Capabilities flags: 65535
|   Some Capabilities: SupportsLoadDataLocal, SupportsTransactions, Speaks41ProtocolOld, LongPassword, DontAllowDatabaseTableColumn, Support41Auth, IgnoreSigpipes, SwitchToSSLAfterHandshake, FoundRows, InteractiveClient, Speaks41ProtocolNew, ConnectWithDatabase, IgnoreSpaceBeforeParenthesis, LongColumnFlag, SupportsCompression, ODBCClient, SupportsMultipleStatments, SupportsAuthPlugins, SupportsMultipleResults
|   Status: Autocommit
|   Salt: YTSgMfqvx\x0F\x7F\x16\&\x1EAeK>0
|_  Auth Plugin Name: caching_sha2_password
|_mysql-users: ERROR: Script execution failed (use -d to debug)
|_mysql-variables: ERROR: Script execution failed (use -d to debug)
|_mysql-vuln-cve2012-2122: ERROR: Script execution failed (use -d to debug)
MAC Address: 00:00:00:00:00:00 (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.21 seconds
```

与我们所有的扫描一样，我们必须谨慎对待结果并手动确认获得的信息，因为某些信息可能是误报。上面这个扫描就是一个很好的例子，因为我们事实上知道目标 MySQL 服务器的 `root` 用户没有使用空密码，而是使用了固定密码。我们可以使用以下命令进行测试：

#### 与 MySQL 服务器交互

与 MySQL 服务器交互

```shell-session
tr01ax@htb[/htb]$ mysql -u root -h 10.129.14.132

ERROR 1045 (28000): Access denied for user 'root'@'10.129.14.1' (using password: NO)
```

例如，如果我们使用我们猜测或通过研究发现的密码，我们将能够登录到 MySQL 服务器并执行一些命令。

与 MySQL 服务器交互

```shell-session
tr01ax@htb[/htb]$ mysql -u root -pP4SSw0rd -h 10.129.14.128

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MySQL connection id is 150165
Server version: 8.0.27-0ubuntu0.20.04.1 (Ubuntu)
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MySQL [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.006 sec)

```sql
MySQL [(none)]> select version();
+-------------------------+
| version()               |
+-------------------------+
| 8.0.27-0ubuntu0.20.04.1 |
+-------------------------+
1 row in set (0.001 sec)


MySQL [(none)]> use mysql;
MySQL [mysql]> show tables;
+------------------------------------------------------+
| Tables_in_mysql                                      |
+------------------------------------------------------+
| columns_priv                                         |
| component                                            |
| db                                                   |
| default_roles                                        |
| engine_cost                                          |
| func                                                 |
| general_log                                          |
| global_grants                                        |
| gtid_executed                                        |
| help_category                                        |
| help_keyword                                         |
| help_relation                                        |
| help_topic                                           |
| innodb_index_stats                                   |
| innodb_table_stats                                   |
| password_history                                     |
...SNIP...
| user                                                 |
+------------------------------------------------------+
37 rows in set (0.002 sec)
```

如果我们查看现有的数据库，会发现已经存在几个数据库。对于MySQL服务器来说，最重要的数据库是`系统架构`（`sys`）和`信息架构`（`information_schema`）。系统架构包含管理所需的表、信息和元数据。关于这个数据库的更多信息可以在MySQL的[参考手册](https://dev.mysql.com/doc/refman/8.0/en/system-schema.html#:~:text=The%20mysql%20schema%20is%20the,used%20for%20other%20operational%20purposes)中找到。

与MySQL服务器交互

```shell-session
mysql> use sys;
mysql> show tables;

+-----------------------------------------------+
| Tables_in_sys                                 |
+-----------------------------------------------+
| host_summary                                  |
| host_summary_by_file_io                       |
| host_summary_by_file_io_type                  |
| host_summary_by_stages                        |
| host_summary_by_statement_latency             |
| host_summary_by_statement_type                |
| innodb_buffer_stats_by_schema                 |
| innodb_buffer_stats_by_table                  |
| innodb_lock_waits                             |
| io_by_thread_by_latency                       |
...SNIP...
| x$waits_global_by_latency                     |
+-----------------------------------------------+


mysql> select host, unique_users from host_summary;

+-------------+--------------+
| host        | unique_users |
+-------------+--------------+
| 10.129.14.1 |            1 |
| localhost   |            2 |
+-------------+--------------+
2 rows in set (0,01 sec)
```

`信息架构`也是一个包含元数据的数据库。但是，这些元数据主要是从`系统架构`数据库中检索的。这两个数据库同时存在的原因是已建立的ANSI/ISO标准。`系统架构`是Microsoft SQL服务器的系统目录，包含比`信息架构`更多的信息。

下表描述了我们在使用MySQL数据库时应该记住并记录的一些命令。

|**命令**|**描述**|
|---|---|
|`mysql -u <user> -p<password> -h <IP address>`|连接到MySQL服务器。'-p'标志和密码之间**不应该**有空格。|
|`show databases;`|显示所有数据库。|
|`use <database>;`|选择一个现有的数据库。|
|`show tables;`|显示所选数据库中所有可用的表。|
|`show columns from <table>;`|显示所选数据库中的所有列。|
|`select * from <table>;`|显示所需表中的所有内容。|
|`select * from <table> where <column> = "<string>";`|在所需表中搜索需要的`字符串`。|

我们必须知道如何与不同的数据库进行交互。因此，我们建议在我们的虚拟机上安装和配置MySQL服务器进行实验。参考手册中还有一个广泛涵盖的[安全问题](https://dev.mysql.com/doc/refman/8.0/en/general-security-issues.html)部分，介绍了保护MySQL服务器的最佳实践。我们在设置MySQL服务器时应该使用它，以便更好地理解为什么某些配置可能无法正常工作。#mssql #footprinting #enumeration #hacking #port1433 [source](https://academy.hackthebox.com/module/112/section/1246) --> [[notes about footprinting]]

# MSSQL

---

[Microsoft SQL](https://www.microsoft.com/en-us/sql-server/sql-server-2019)（`MSSQL`）是微软基于SQL的关系数据库管理系统。与我们在上一节讨论的MySQL不同，MSSQL是闭源的，最初是为在Windows操作系统上运行而编写的。由于它对.NET的强大原生支持，在构建运行在微软.NET框架上的应用程序时，它在数据库管理员和开发人员中很受欢迎。虽然有可以在Linux和MacOS上运行的MSSQL版本，但我们更可能在运行Windows的目标上遇到MSSQL实例。

#### MSSQL客户端

[SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15)（`SSMS`）是一个可以与MSSQL安装包一起安装的功能，也可以单独下载和安装。它通常安装在服务器上，用于管理员进行初始配置和长期数据库管理。请记住，由于SSMS是一个客户端应用程序，它可以安装在管理员或开发人员计划用来管理数据库的任何系统上。它不仅存在于托管数据库的服务器上。这意味着我们可能会遇到一个安装了SSMS并保存了凭据的易受攻击系统，这些凭据允许我们连接到数据库。下图显示了SSMS的实际运行情况。

![SSMS](https://academy.hackthebox.com/storage/modules/112/ssms.png)

还有许多其他客户端可用于访问运行在MSSQL上的数据库。包括但不限于：

||||||
|---|---|---|---|---|
|[mssql-cli](https://docs.microsoft.com/en-us/sql/tools/mssql-cli?view=sql-server-ver15)|[SQL Server PowerShell](https://docs.microsoft.com/en-us/sql/powershell/sql-server-powershell?view=sql-server-ver15)|[HeidiSQL](https://www.heidisql.com)|[SQLPro](https://www.macsqlclient.com)|[Impacket's mssqlclient.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py)|

在上面列出的MSSQL客户端中，渗透测试人员可能会发现Impacket的mssqlclient.py最有用，因为SecureAuthCorp的Impacket项目在安装时就存在于许多渗透测试发行版中。要查找客户端是否以及在主机上的位置，我们可以使用以下命令：

MSSQL客户端

```shell-session
tr01ax@htb[/htb]$ locate mssqlclient

/usr/bin/impacket-mssqlclient
/usr/share/doc/python3-impacket/examples/mssqlclient.py
```

#### MSSQL数据库

MSSQL具有默认的系统数据库，可以帮助我们了解目标服务器上可能托管的所有数据库的结构。以下是默认数据库及其简要描述：

|默认系统数据库|描述|
|---|---|
|`master`|跟踪SQL服务器实例的所有系统信息|
|`model`|模板数据库，作为每个新创建数据库的结构。对model数据库所做的任何设置更改都会反映在更改model数据库后创建的任何新数据库中|
|`msdb`|SQL Server代理使用此数据库来调度作业和警报|
|`tempdb`|存储临时对象|
|`resource`|只读数据库，包含SQL服务器附带的系统对象|

表格来源：[系统数据库Microsoft文档](https://docs.microsoft.com/en-us/sql/relational-databases/databases/system-databases?view=sql-server-ver15)

---

## 默认配置

当管理员首次安装和配置MSSQL使其可通过网络访问时，SQL服务可能会以`NT SERVICE\MSSQLSERVER`身份运行。从客户端连接可以通过Windows身份验证进行，默认情况下，在尝试连接时不强制加密。

![SSMS](https://academy.hackthebox.com/storage/modules/112/auth.png)

身份验证设置为`Windows身份验证`意味着底层Windows操作系统将处理登录请求，并在允许连接到数据库管理系统之前使用本地SAM数据库或域控制器（托管Active Directory）进行验证。在Windows环境中使用Active Directory对于审计活动和控制访问是理想的，但如果账户被攻破，可能会导致权限提升和在Windows域环境中的横向移动。与任何操作系统、服务、服务器角色或应用程序一样，在虚拟机中从安装到配置进行设置可能是有益的，以了解所有默认配置和管理员可能犯的潜在错误。

---

## 危险设置

当我们在进行渗透测试时，将自己置于IT管理员的角度可能是有益的。这种思维方式可以帮助我们记住查找可能被管理员错误配置或以危险方式配置的各种设置。IT工作日可能相当繁忙，许多不同的项目同时进行，在许多组织中快速和准确地执行的压力是现实，错误很容易发生。只需要一个微小的错误配置就可能危及网络上的关键服务器或服务。这几乎适用于每个可以配置的网络服务和服务器角色，包括MSSQL。

这不是一个详尽的列表，因为管理员可以根据各自组织的需求以无数种方式配置MSSQL数据库。我们可能会从查看以下内容中受益：

- MSSQL客户端在连接到MSSQL服务器时不使用加密

- 使用加密时使用自签名证书。可以伪造自签名证书

- 使用[命名管道](https://docs.microsoft.com/en-us/sql/tools/configuration-manager/named-pipes-properties?view=sql-server-ver15)（named pipes，一种进程间通信机制）

- 弱密码和默认的`sa`凭据。管理员可能忘记禁用此账户


---

## 服务信息收集

有许多方法可以对MSSQL服务进行信息收集，我们的扫描越具体，就能收集到越有用的信息。NMAP有默认的mssql脚本，可用于针对MSSQL监听的默认tcp端口`1433`。

下面的脚本化NMAP扫描为我们提供了有用的信息。我们可以看到`主机名`、`数据库实例名`、`MSSQL软件版本`以及`启用了命名管道`。我们将从在笔记中添加这些发现中受益。

#### NMAP MSSQL脚本扫描

NMAP MSSQL脚本扫描

```shell-session
tr01ax@htb[/htb]$ sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248

Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-08 09:40 EST
Nmap scan report for 10.129.201.248
Host is up (0.15s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info:
|   Target_Name: SQL-01
|   NetBIOS_Domain_Name: SQL-01
|   NetBIOS_Computer_Name: SQL-01
|   DNS_Domain_Name: SQL-01
|   DNS_Computer_Name: SQL-01
|_  Product_Version: 10.0.17763

Host script results:
| ms-sql-dac:
|_  Instance: MSSQLSERVER; DAC port: 1434 (connection failed)
| ms-sql-info:
|   Windows server name: SQL-01
|   10.129.201.248\MSSQLSERVER:
|     Instance name: MSSQLSERVER
|     Version:
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|     TCP port: 1433
|     Named pipe: \\10.129.201.248\pipe\sql\query
|_    Clustered: false

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.52 seconds
```

我们还可以使用Metasploit运行一个名为`mssql_ping`的辅助扫描器，它将扫描MSSQL服务并在我们的信息收集过程中提供有用的信息。

#### Metasploit中的MSSQL Ping

Metasploit中的MSSQL Ping

```shell-session
msf6 auxiliary(scanner/mssql/mssql_ping) > set rhosts 10.129.201.248

rhosts => 10.129.201.248


msf6 auxiliary(scanner/mssql/mssql_ping) > run

[*] 10.129.201.248:       - SQL Server information for 10.129.201.248:
[+] 10.129.201.248:       -    ServerName      = SQL-01
[+] 10.129.201.248:       -    InstanceName    = MSSQLSERVER
[+] 10.129.201.248:       -    IsClustered     = No
[+] 10.129.201.248:       -    Version         = 15.0.2000.5
[+] 10.129.201.248:       -    tcp             = 1433
[+] 10.129.201.248:       -    np              = \\SQL-01\pipe\sql\query
[*] 10.129.201.248:       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

#### 使用Mssqlclient.py连接

如果我们能猜测或获取凭据，这允许我们远程连接到MSSQL服务器并开始使用T-SQL（`Transact-SQL`，微软对SQL的扩展实现）与数据库交互。通过MSSQL进行身份验证将使我们能够通过SQL数据库引擎直接与数据库交互。从Pwnbox或个人攻击主机，我们可以使用Impacket的mssqlclient.py进行连接，如下面的输出所示。一旦连接到服务器，最好先了解一下环境并列出系统上存在的数据库。

使用Mssqlclient.py连接

```shell-session
tr01ax@htb[/htb]$ python3 mssqlclient.py Administrator@10.129.201.248 -windows-auth

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(SQL-01): Line 1: Changed database context to 'master'.
[*] INFO(SQL-01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208)
[!] Press help for extra shell commands

SQL> select name from sys.databases

name

--------------------------------------------------------------------------------------

master

tempdb

model

msdb

Transactions
```#oracle #hacking #footprinting #enumeration #port1521 [source](https://academy.hackthebox.com/module/112/section/2117) --> [[notes about footprinting]]

# Oracle TNS

---

`Oracle透明网络底层`（`TNS`，Oracle Transparent Network Substrate）服务器是一种通信协议，促进Oracle数据库和应用程序之间通过网络进行通信。它最初作为[Oracle Net Services](https://docs.oracle.com/en/database/oracle/oracle-database/18/netag/introducing-oracle-net-services.html)软件套件的一部分引入，TNS支持Oracle数据库和客户端应用程序之间的各种网络协议，如`IPX/SPX`和`TCP/IP`协议栈。因此，它已成为医疗、金融和零售行业管理大型复杂数据库的首选解决方案。此外，其内置的加密机制确保了传输数据的安全性，使其成为数据安全至关重要的企业环境的理想解决方案。

随着时间的推移，TNS已更新以支持更新的技术，包括`IPv6`和`SSL/TLS`加密，这使其更适合以下用途：

||||
|---|---|---|---|
|名称解析|连接管理|负载均衡|安全性|

此外，它通过TCP/IP协议层之上的额外安全层在客户端和服务器通信之间启用加密。此功能有助于保护数据库架构免受未经授权的访问或试图破坏网络流量数据的攻击。除此之外，它为数据库管理员和开发人员提供了高级工具和功能，因为它提供全面的性能监控和分析工具、错误报告和日志记录功能、工作负载管理以及通过数据库服务实现的容错能力。

---

## 默认配置

Oracle TNS服务器的默认配置因安装的Oracle软件版本和版本而异。但是，Oracle TNS中通常默认配置一些常见设置。默认情况下，监听器在`TCP/1521`端口上监听传入连接。但是，此默认端口可以在安装期间或之后在配置文件中更改。TNS监听器被配置为支持各种网络协议，包括`TCP/IP`、`UDP`、`IPX/SPX`和`AppleTalk`。监听器还可以支持多个网络接口，并在特定IP地址或所有可用网络接口上进行监听。默认情况下，Oracle TNS可以在`Oracle 8i`/`9i`中远程管理，但在Oracle 10g/11g中不能。

TNS监听器的默认配置还包括一些基本的安全功能。例如，监听器只接受来自授权主机的连接，并使用主机名、IP地址以及用户名和密码的组合执行基本身份验证。此外，监听器将使用Oracle Net Services加密客户端和服务器之间的通信。Oracle TNS的配置文件称为`tnsnames.ora`和`listener.ora`，通常位于`ORACLE_HOME/network/admin`目录中。该纯文本文件包含Oracle数据库实例和其他使用TNS协议的网络服务的配置信息。

Oracle TNS通常与其他Oracle服务一起使用，如Oracle DBSNMP、Oracle数据库、Oracle应用服务器、Oracle企业管理器、Oracle Fusion中间件、Web服务器等。Oracle服务的默认安装已经进行了许多更改。例如，Oracle 9有一个默认密码`CHANGE_ON_INSTALL`，而Oracle 10没有设置默认密码。Oracle DBSNMP服务也使用默认密码`dbsnmp`，当我们遇到这个服务时应该记住。另一个例子是，许多组织仍然将`finger`服务与Oracle一起使用，当我们了解主目录时，这可能会使Oracle的服务面临风险并变得易受攻击。

每个数据库或服务在[tnsnames.ora](https://docs.oracle.com/cd/E11882_01/network.112/e10835/tnsnames.htm#NETRF007)文件中都有一个唯一的条目，包含客户端连接到服务所需的必要信息。该条目由服务名称、服务的网络位置以及客户端连接到服务时应使用的数据库或服务名称组成。例如，一个简单的`tnsnames.ora`文件可能如下所示：

#### Tnsnames.ora

Code: txt

```txt
ORCL =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.129.11.102)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
  )
```

这里我们可以看到一个名为`ORCL`的服务，它在IP地址`10.129.11.102`的`TCP/1521`端口上监听。客户端在连接到服务时应使用服务名`orcl`。但是，tnsnames.ora文件可以包含许多这样的不同数据库和服务的条目。这些条目还可以包含其他信息，如身份验证详细信息、连接池设置和负载均衡配置。

另一方面，`listener.ora`文件是一个服务器端配置文件，定义监听器进程的属性和参数，该进程负责接收传入的客户端请求并将它们转发到适当的Oracle数据库实例。

#### Listener.ora

Code: txt

```txt
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = PDB1)
      (ORACLE_HOME = C:\oracle\product\19.0.0\dbhome_1)
      (GLOBAL_DBNAME = PDB1)
      (SID_DIRECTORY_LIST =
        (SID_DIRECTORY =
          (DIRECTORY_TYPE = TNS_ADMIN)
          (DIRECTORY = C:\oracle\product\19.0.0\dbhome_1\network\admin)
        )
      )
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orcl.inlanefreight.htb)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

ADR_BASE_LISTENER = C:\oracle
```

简而言之，客户端Oracle Net Services软件使用`tnsnames.ora`文件将服务名称解析为网络地址，而监听器进程使用`listener.ora`文件来确定它应该监听的服务以及监听器的行为。

Oracle数据库可以通过使用所谓的PL/SQL排除列表（`PlsqlExclusionList`）来保护。它是一个用户创建的文本文件，需要放置在`$ORACLE_HOME/sqldeveloper`目录中，包含应该排除执行的PL/SQL包或类型的名称。一旦创建了PL/SQL排除列表文件，就可以将其加载到数据库实例中。它作为一个黑名单，无法通过Oracle应用服务器访问。

|**设置**|**描述**|
|---|---|
|`DESCRIPTION`|提供数据库名称及其连接类型的描述符。|
|`ADDRESS`|数据库的网络地址，包括主机名和端口号。|
|`PROTOCOL`|用于与服务器通信的网络协议|
|`PORT`|用于与服务器通信的端口号|
|`CONNECT_DATA`|指定连接的属性，如服务名称或SID、协议和数据库实例标识符。|
|`INSTANCE_NAME`|客户端要连接的数据库实例的名称。|
|`SERVICE_NAME`|客户端要连接的服务的名称。|
|`SERVER`|用于数据库连接的服务器类型，如专用或共享。|
|`USER`|用于与数据库服务器进行身份验证的用户名。|
|`PASSWORD`|用于与数据库服务器进行身份验证的密码。|
|`SECURITY`|连接的安全类型。|
|`VALIDATE_CERT`|是否使用SSL/TLS验证证书。|
|`SSL_VERSION`|用于连接的SSL/TLS版本。|
|`CONNECT_TIMEOUT`|客户端建立与数据库连接的时间限制（以秒为单位）。|
|`RECEIVE_TIMEOUT`|客户端从数据库接收响应的时间限制（以秒为单位）。|
|`SEND_TIMEOUT`|客户端向数据库发送请求的时间限制（以秒为单位）。|
|`SQLNET.EXPIRE_TIME`|客户端检测连接失败的时间限制（以秒为单位）。|
|`TRACE_LEVEL`|数据库连接的跟踪级别。|
|`TRACE_DIRECTORY`|存储跟踪文件的目录。|
|`TRACE_FILE_NAME`|跟踪文件的名称。|
|`LOG_FILE`|存储日志信息的文件。|

在我们枚举TNS监听器并与之交互之前，我们需要为我们的`Pwnbox`实例下载一些包和工具，以防它还没有这些。这是一个执行所有这些操作的Bash脚本：

#### Oracle-Tools-setup.sh

Code: bash

```bash
#!/bin/bash

sudo apt-get install libaio1 python3-dev alien python3-pip -y
git clone https://github.com/quentinhardy/odat.git
cd odat/
git submodule init
sudo submodule update
sudo apt install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus -y
pip3 install cx_Oracle
sudo apt-get install python3-scapy -y
sudo pip3 install colorlog termcolor pycryptodome passlib python-libnmap
sudo pip3 install argcomplete && sudo activate-global-python-argcomplete
```

之后，我们可以尝试运行以下命令来确定安装是否成功：

#### 测试ODAT

测试ODAT

```shell-session
tr01ax@htb[/htb]$ ./odat.py -h

usage: odat.py [-h] [--version]
               {all,tnscmd,tnspoison,sidguesser,snguesser,passwordguesser,utlhttp,httpuritype,utltcp,ctxsys,externaltable,dbmsxslprocessor,dbmsadvisor,utlfile,dbmsscheduler,java,passwordstealer,oradbg,dbmslob,stealremotepwds,userlikepwd,smb,privesc,cve,search,unwrapper,clean}
               ...

            _  __   _  ___
           / \|  \ / \|_ _|
          ( o ) o ) o || |
           \_/|__/|_n_||_|
-------------------------------------------
  _        __           _           ___
 / \      |  \         / \         |_ _|
( o )       o )         o |         | |
 \_/racle |__/atabase |_n_|ttacking |_|ool
-------------------------------------------

By Quentin Hardy (quentin.hardy@protonmail.com or quentin.hardy@bt.com)
...SNIP...
```

Oracle数据库攻击工具（`ODAT`）是一个用Python编写的开源渗透测试工具，旨在枚举和利用Oracle数据库中的漏洞。它可用于识别和利用Oracle数据库中的各种安全漏洞，包括SQL注入、远程代码执行和权限提升。

现在让我们使用`nmap`扫描默认的Oracle TNS监听器端口。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap -p1521 -sV 10.129.204.235 --open

Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-06 10:59 EST
Nmap scan report for 10.129.204.235
Host is up (0.0041s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.64 seconds
```

我们可以看到端口是开放的，服务正在运行。在Oracle RDBMS中，系统标识符（`SID`，System Identifier）是标识特定数据库实例的唯一名称。它可以有多个实例，每个实例都有自己的系统ID。实例是一组与管理数据库数据交互的进程和内存结构。当客户端连接到Oracle数据库时，它会在连接字符串中指定数据库的`SID`。客户端使用此SID来标识它要连接的数据库实例。假设客户端没有指定SID。那么将使用`tnsnames.ora`文件中定义的默认值。

SID是连接过程的重要组成部分，因为它标识客户端要连接的特定数据库实例。如果客户端指定了错误的SID，连接尝试将失败。数据库管理员可以使用SID来监控和管理数据库的各个实例。例如，他们可以启动、停止或重新启动实例，调整其内存分配或其他配置参数，并使用Oracle企业管理器等工具监控其性能。

有多种方法可以枚举，或者更准确地说是猜测SID。因此我们可以使用`nmap`、`hydra`、`odat`等工具。让我们先使用`nmap`。

#### Nmap - SID暴力破解

Nmap - SID暴力破解

```shell-session
tr01ax@htb[/htb]$ sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute

Starting Nmap 7.93 ( https://nmap.org ) at 2023-03-06 11:01 EST
Nmap scan report for 10.129.204.235
Host is up (0.0044s latency).

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)
| oracle-sid-brute:
|_  XE

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 55.40 seconds
```

我们可以使用`odat.py`工具执行各种扫描来枚举和收集有关Oracle数据库服务及其组件的信息。这些扫描可以检索数据库名称、版本、运行中的进程、用户账户、漏洞、错误配置等。让我们使用`all`选项并尝试`odat.py`工具的所有模块。

#### ODAT

ODAT

```shell-session
tr01ax@htb[/htb]$ ./odat.py all -s 10.129.204.235

[+] Checking if target 10.129.204.235:1521 is well configured for a connection...
[+] According to a test, the TNS listener 10.129.204.235:1521 is well configured. Continue...

...SNIP...

[!] Notice: 'mdsys' account is locked, so skipping this username for password           #####################| ETA:  00:01:16
[!] Notice: 'oracle_ocm' account is locked, so skipping this username for password       #####################| ETA:  00:01:05
[!] Notice: 'outln' account is locked, so skipping this username for password           #####################| ETA:  00:00:59
[+] Valid credentials found: scott/tiger. Continue...

...SNIP...
```

在这个例子中，我们找到了用户`scott`的有效凭据，密码是`tiger`。之后，我们可以使用`sqlplus`工具连接到Oracle数据库并与之交互。

#### SQLplus - 登录

SQLplus - 登录

```shell-session
tr01ax@htb[/htb]$ sqlplus scott/tiger@10.129.204.235/XE;

SQL*Plus: Release 21.0.0.0.0 - Production on Mon Mar 6 11:19:21 2023
Version 21.4.0.0.0

Copyright (c) 1982, 2021, Oracle. All rights reserved.

ERROR:
ORA-28002: the password will expire within 7 days



Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production

SQL>
```

如果遇到以下错误 `sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory`，请执行以下命令，参考自[这里](https://stackoverflow.com/questions/27717312/sqlplus-error-while-loading-shared-libraries-libsqlplus-so-cannot-open-shared)。

SQLplus - 登录

```shell-session
tr01ax@htb[/htb]$ sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig
```

有许多[SQLplus命令](https://docs.oracle.com/cd/E11882_01/server.112/e41085/sqlqraa001.htm#SQLQR985)可用于手动枚举数据库。例如，我们可以列出当前数据库中所有可用的表，或显示当前用户的权限，如下所示：

#### Oracle RDBMS - 交互操作

Oracle RDBMS - 交互操作

```shell-session
SQL> select table_name from all_tables;

TABLE_NAME
------------------------------
DUAL
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
STMT_AUDIT_OPTION_MAP
AUDIT_ACTIONS
WRR$_REPLAY_CALL_FILTER
HS_BULKLOAD_VIEW_OBJ
HS$_PARALLEL_METADATA
HS_PARTITION_COL_NAME
HS_PARTITION_COL_TYPE
HELP

...SNIP...


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SCOTT                          CONNECT                        NO  YES NO
SCOTT                          RESOURCE                       NO  YES NO
```

这里，用户 `scott` 没有管理权限。但是，我们可以尝试使用此账户以系统数据库管理员（System Database Admin，`sysdba`）身份登录，从而获得更高的权限。当用户 `scott` 拥有适当的权限时，这种操作是可行的——这些权限通常由数据库管理员授予，或者管理员本人使用该账户。

#### Oracle RDBMS - 数据库枚举

Oracle RDBMS - 数据库枚举

```shell-session
tr01ax@htb[/htb]$ sqlplus scott/tiger@10.129.204.235/XE as sysdba

SQL*Plus: Release 21.0.0.0.0 - Production on Mon Mar 6 11:32:58 2023
Version 21.4.0.0.0

Copyright (c) 1982, 2021, Oracle. All rights reserved.


Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            ADM_PARALLEL_EXECUTE_TASK      YES YES NO
SYS                            APEX_ADMINISTRATOR_ROLE        YES YES NO
SYS                            AQ_ADMINISTRATOR_ROLE          YES YES NO
SYS                            AQ_USER_ROLE                   YES YES NO
SYS                            AUTHENTICATEDUSER              YES YES NO
SYS                            CONNECT                        YES YES NO
SYS                            CTXAPP                         YES YES NO
SYS                            DATAPUMP_EXP_FULL_DATABASE     YES YES NO
SYS                            DATAPUMP_IMP_FULL_DATABASE     YES YES NO
SYS                            DBA                            YES YES NO
SYS                            DBFS_ROLE                      YES YES NO

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            DELETE_CATALOG_ROLE            YES YES NO
SYS                            EXECUTE_CATALOG_ROLE           YES YES NO
...SNIP...
```

一旦获得Oracle数据库的访问权限，我们可以采取多种方法。这在很大程度上取决于我们拥有的信息和整体配置。但是，我们可能无法添加新用户或进行任何修改。从这一点开始，我们可以从 `sys.user$` 中检索密码哈希值，并尝试离线破解它们。查询语句如下所示：

#### Oracle RDBMS - 提取密码哈希

Oracle RDBMS - 提取密码哈希

```shell-session
SQL> select name, password from sys.user$;

NAME                           PASSWORD
------------------------------ ------------------------------
SYS                            FBA343E7D6C8BC9D
PUBLIC
CONNECT
RESOURCE
DBA
SYSTEM                         B5073FE1DE351687
SELECT_CATALOG_ROLE
EXECUTE_CATALOG_ROLE
DELETE_CATALOG_ROLE
OUTLN                          4A3BA55E08595C81
EXP_FULL_DATABASE

NAME                           PASSWORD
------------------------------ ------------------------------
IMP_FULL_DATABASE
LOGSTDBY_ADMINISTRATOR
...SNIP...
```

另一种选择是向目标上传Web Shell（网页后门）。但是，这需要服务器运行Web服务器，并且我们需要知道Web服务器根目录的确切位置。尽管如此，如果我们知道正在处理的系统类型，可以尝试默认路径，它们是：

|**操作系统**|**路径**|
|---|---|
|Linux|`/var/www/html`|
|Windows|`C:\inetpub\wwwroot`|

首先，重要的是尝试使用不会被杀毒软件或入侵检测/防御系统视为危险的文件来进行漏洞利用尝试。因此，我们创建一个包含字符串的文本文件，并将其上传到目标系统。

#### Oracle RDBMS - 文件上传

Oracle RDBMS - 文件上传

```shell-session
tr01ax@htb[/htb]$ echo "Oracle File Upload Test" > testing.txt
tr01ax@htb[/htb]$ ./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt

[1] (10.129.204.235:1521): Put the ./testing.txt local file in the C:\inetpub\wwwroot folder like testing.txt on the 10.129.204.235 server
[+] The ./testing.txt file was created on the C:\inetpub\wwwroot directory on the 10.129.204.235 server like the testing.txt file
```

最后，我们可以使用 `curl` 测试文件上传方法是否有效。因此，我们将使用 `GET http://<IP>` 请求，或者可以通过浏览器访问。

Oracle RDBMS - 文件上传

```shell-session
tr01ax@htb[/htb]$ curl -X GET http://10.129.204.235/testing.txt

Oracle File Upload Test
```#ipmi #footprinting #enumeration #hacking #port623 [source](https://academy.hackthebox.com/module/112/section/1245) [[notes about footprinting]]


---

[智能平台管理接口](https://www.thomas-krenn.com/en/wiki/IPMI_Basics)（Intelligent Platform Management Interface，`IPMI`）是一组用于基于硬件的主机管理系统的标准化规范，用于系统管理和监控。它作为一个自主子系统运行，独立于主机的BIOS、CPU、固件和底层操作系统工作。IPMI使系统管理员能够管理和监控系统，即使系统已关机或处于无响应状态。它通过直接网络连接到系统硬件来运行，不需要通过登录Shell访问操作系统。IPMI还可以用于远程升级系统，无需物理访问目标主机。IPMI通常以三种方式使用：

- 在操作系统启动前修改BIOS设置
- 当主机完全断电时
- 系统故障后访问主机

当不用于这些任务时，IPMI可以监控多种不同的内容，如系统温度、电压、风扇状态和电源供应。它还可以用于查询库存信息、查看硬件日志以及使用SNMP发送警报。主机系统可以关机，但IPMI模块需要电源和LAN连接才能正常工作。

IPMI协议最初由Intel于1998年发布，现在已被超过200家系统供应商支持，包括Cisco、Dell、HP、Supermicro、Intel等。使用IPMI 2.0版本的系统可以通过串口over LAN（Serial over LAN）进行管理，使系统管理员能够在带内查看串行控制台输出。要运行，IPMI需要以下组件：

- 基板管理控制器（Baseboard Management Controller，BMC）- 微控制器，是IPMI的核心组件
- 智能机箱管理总线（Intelligent Chassis Management Bus，ICMB）- 允许从一个机箱到另一个机箱通信的接口
- 智能平台管理总线（Intelligent Platform Management Bus，IPMB）- 扩展BMC
- IPMI内存 - 存储系统事件日志、仓库存储数据等内容
- 通信接口 - 本地系统接口、串行和LAN接口、ICMB和PCI管理总线

---

## 服务足迹侦察

IPMI通过623端口UDP进行通信。使用IPMI协议的系统称为基板管理控制器（BMC）。BMC通常作为运行Linux的嵌入式ARM系统实现，直接连接到主机主板。BMC内置于许多主板中，但也可以作为PCI卡添加到系统中。大多数服务器要么自带BMC，要么支持添加BMC。我们在内部渗透测试中经常看到的最常见的BMC是HP iLO、Dell DRAC和Supermicro IPMI。如果我们在评估期间能够访问BMC，我们将获得对主机主板的完全访问权限，并能够监控、重启、关机，甚至重新安装主机操作系统。获得BMC的访问权限几乎等同于对系统的物理访问。许多BMC（包括HP iLO、Dell DRAC和Supermicro IPMI）暴露了基于Web的管理控制台、某种命令行远程访问协议（如Telnet或SSH），以及623 UDP端口——同样用于IPMI网络协议。下面是使用Nmap [ipmi-version](https://nmap.org/nsedoc/scripts/ipmi-version.html) NSE脚本对服务进行足迹侦察的示例扫描。

#### Nmap

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-04 21:48 GMT
Nmap scan report for ilo.inlanfreight.local (172.16.2.2)
Host is up (0.00064s latency).

PORT    STATE SERVICE
623/udp open  asf-rmcp
| ipmi-version:
|   Version:
|     IPMI-2.0
|   UserAuth:
|   PassAuth: auth_user, non_null_user
|_  Level: 2.0
MAC Address: 14:03:DC:674:18:6A (Hewlett Packard Enterprise)

Nmap done: 1 IP address (1 host up) scanned in 0.46 seconds
```

在这里，我们可以看到IPMI协议确实在623端口上监听，Nmap已识别出协议版本为2.0。我们还可以使用Metasploit扫描模块 [IPMI Information Discovery (auxiliary/scanner/ipmi/ipmi_version)](https://www.rapid7.com/db/modules/auxiliary/scanner/ipmi/ipmi_version/)。

#### Metasploit版本扫描

Metasploit版本扫描

```shell-session
msf6 > use auxiliary/scanner/ipmi/ipmi_version
msf6 auxiliary(scanner/ipmi/ipmi_version) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_version) > show options

Module options (auxiliary/scanner/ipmi/ipmi_version):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   BATCHSIZE  256              yes       The number of hosts to probe in each set
   RHOSTS     10.129.42.195    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      623              yes       The target port (UDP)
   THREADS    10               yes       The number of concurrent threads


msf6 auxiliary(scanner/ipmi/ipmi_version) > run

[*] Sending IPMI requests to 10.129.42.195->10.129.42.195 (1 hosts)
[+] 10.129.42.195:623 - IPMI - IPMI-2.0 UserAuth(auth_msg, auth_user, non_null_user) PassAuth(password, md5, md2, null) Level(1.5, 2.0)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

在内部渗透测试期间，我们经常发现管理员没有更改默认密码的BMC。一些应该保存在备忘录中的独特默认密码包括：

|产品|用户名|密码|
|---|---|---|
|Dell iDRAC|root|calvin|
|HP iLO|Administrator|由数字和大写字母组成的随机8字符字符串|
|Supermicro IPMI|ADMIN|ADMIN|

对于我们发现的任何服务，尝试已知的默认密码也很重要，因为这些密码通常未被更改，可能会带来快速突破。在处理BMC时，这些默认密码可能使我们获得Web控制台的访问权限，甚至通过SSH或Telnet获得命令行访问权限。

---

## 危险配置

如果默认凭据无法访问BMC，我们可以利用IPMI 2.0中RAKP协议的一个[缺陷](http://fish2.com/ipmi/remote-pw-cracking.html)。在认证过程中，服务器在认证发生之前将用户密码的加盐SHA1或MD5哈希发送给客户端。这可以被利用来获取BMC上任何有效用户账户的密码哈希。然后可以使用 `Hashcat` 模式 `7300` 通过字典攻击离线破解这些密码哈希。如果HP iLO使用出厂默认密码，我们可以使用这个Hashcat掩码攻击命令 `hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u`，它会尝试大写字母和数字的所有8字符密码组合。

这个问题没有直接的"修复方法"，因为该缺陷是IPMI规范的关键组成部分。客户端可以选择使用非常长且难以破解的密码，或实施网络分段规则来限制对BMC的直接访问。在内部渗透测试中不要忽视IPMI很重要（我们在大多数评估中都会看到它），因为我们不仅通常可以获得BMC Web控制台的访问权限（这是一个高风险发现），而且我们曾见过设置了独特（但可破解）密码的环境，该密码后来在其他系统中被重复使用。在一次这样的渗透测试中，我们获得了IPMI哈希，使用Hashcat离线破解，并能够以root用户身份通过SSH登录到环境中的许多关键服务器，并获得各种网络监控工具的Web管理控制台访问权限。

要检索IPMI哈希，我们可以使用Metasploit [IPMI 2.0 RAKP Remote SHA1 Password Hash Retrieval](https://www.rapid7.com/db/modules/auxiliary/scanner/ipmi/ipmi_dumphashes/) 模块。

#### Metasploit哈希转储

Metasploit哈希转储

```shell-session
msf6 > use auxiliary/scanner/ipmi/ipmi_dumphashes
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > show options

Module options (auxiliary/scanner/ipmi/ipmi_dumphashes):

   Name                 Current Setting                                                    Required  Description
   ----                 ---------------                                                    --------  -----------
   CRACK_COMMON         true                                                               yes       Automatically crack common passwords as they are obtained
   OUTPUT_HASHCAT_FILE                                                                     no        Save captured password hashes in hashcat format
   OUTPUT_JOHN_FILE                                                                        no        Save captured password hashes in john the ripper format
   PASS_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_passwords.txt  yes       File containing common passwords for offline cracking, one per line
   RHOSTS               10.129.42.195                                                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT                623                                                                yes       The target port
   THREADS              1                                                                  yes       The number of concurrent threads (max one per host)
   USER_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_users.txt      yes       File containing usernames, one per line



msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > run

[+] 10.129.42.195:623 - IPMI - Hash found: ADMIN:8e160d4802040000205ee9253b6b8dac3052c837e23faa631260719fce740d45c3139a7dd4317b9ea123456789abcdefa123456789abcdef140541444d494e:a3e82878a09daa8ae3e6c22f9080f8337fe0ed7e
[+] 10.129.42.195:623 - IPMI - Hash for user 'ADMIN' matches password 'ADMIN'
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

在这里我们可以看到，我们成功获取了用户 `ADMIN` 的密码哈希，工具能够快速破解它，揭示了看起来是默认密码 `ADMIN`。从这里，我们可以尝试登录BMC，或者如果密码是更独特的内容，检查其他系统上是否存在密码重用。IPMI在网络环境中非常常见，因为系统管理员需要能够在停机事件中远程访问服务器，或执行某些传统上需要亲自在服务器前才能完成的维护任务。这种管理便利性伴随着将密码哈希暴露给网络上任何人的风险，可能导致未经授权的访问、系统中断，甚至远程代码执行。检查IPMI应该成为我们在任何评估环境中进行内部渗透测试的标准流程的一部分。#linux #footprinting #enumeration #ssh #hacking #port873[source](https://academy.hackthebox.com/module/112/section/1240)
[[notes about footprinting]]

# Linux远程管理协议

---

在Linux发行版的世界中，有许多方法可以远程管理服务器。例如，假设我们在众多地点之一，我们的一位员工刚刚去了另一个城市的客户那里，因为遇到了他无法解决的错误而需要我们的帮助。在大多数情况下，通过电话进行有效的故障排除会很困难，因此如果我们知道如何登录远程系统来管理它会很有帮助。

这些应用程序和服务几乎可以在公共网络上的每台服务器上找到。这节省了时间，因为我们不必亲自到服务器现场，而且工作环境看起来仍然相同。这些用于远程系统管理的协议和应用程序出于这些原因成为了有趣的目标。如果配置不正确，作为渗透测试人员，我们甚至可以快速获得对远程系统的访问权限。因此，我们应该熟悉为此目的最重要的协议、服务器和应用程序。

---

## SSH

[安全外壳协议](https://en.wikipedia.org/wiki/Secure_Shell)（Secure Shell，`SSH`）使两台计算机能够在可能不安全的网络上通过标准端口 `TCP 22` 建立加密的直接连接。这对于防止第三方拦截数据流从而截获敏感数据是必要的。SSH服务器还可以配置为仅允许来自特定客户端的连接。SSH的一个优势是该协议可在所有常见操作系统上运行。由于它最初是Unix应用程序，因此在所有Linux发行版和MacOS上都是原生实现的。SSH也可以在Windows上使用，前提是我们安装了适当的程序。Linux发行版上著名的[OpenBSD SSH](https://www.openssh.com/)（`OpenSSH`）服务器是SSH Communication Security原始商业 `SSH` 服务器的开源分支。因此，有两个竞争的协议：`SSH-1` 和 `SSH-2`。

`SSH-2`，也称为SSH版本2，在加密、速度、稳定性和安全性方面比SSH版本1更先进。例如，`SSH-1` 容易受到 `MITM`（中间人攻击）的影响，而SSH-2则不会。

我们可以想象我们想要管理一个远程主机。这可以通过命令行或GUI完成。此外，我们还可以使用SSH协议向所需系统发送命令、传输文件或进行端口转发。因此，我们需要使用SSH协议连接到它并对其进行身份验证。总的来说，OpenSSH有六种不同的身份验证方法：

1. 密码认证
2. 公钥认证
3. 基于主机的认证
4. 键盘认证
5. 挑战-响应认证
6. GSSAPI认证

我们将更仔细地研究和讨论最常用的身份验证方法之一。此外，我们可以在[这里](https://www.golinuxcloud.com/openssh-authentication-methods-sshd-config/)等地方了解更多关于其他身份验证方法的信息。

#### 公钥认证

第一步，SSH服务器和客户端相互进行身份验证。服务器向客户端发送证书以验证它是正确的服务器。只有在首次建立联系时，才存在第三方介入两个参与者之间从而拦截连接的风险。由于证书本身也是加密的，因此无法被模仿。一旦客户端知道了正确的证书，其他人就无法假装通过相应的服务器进行联系。

服务器认证后，客户端也必须向服务器证明它有访问授权。然而，SSH服务器已经拥有为所需用户设置的密码的加密哈希值。因此，用户每次在同一会话期间登录到另一台服务器时都必须输入密码。出于这个原因，客户端身份验证的另一种选择是使用公钥和私钥对。

私钥是为用户自己的计算机单独创建的，并使用应该比典型密码更长的口令进行保护。私钥仅存储在我们自己的计算机上，并始终保持秘密。如果我们想要建立SSH连接，我们首先输入口令，从而打开对私钥的访问。

公钥也存储在服务器上。服务器使用客户端的公钥创建一个密码学问题并将其发送给客户端。客户端反过来使用自己的私钥解密该问题，发回解决方案，从而通知服务器它可以建立合法的连接。在会话期间，用户只需输入一次口令即可连接到任意数量的服务器。在会话结束时，用户从本地机器注销，确保没有获得本地机器物理访问权限的第三方可以连接到服务器。

---

## 默认配置

负责OpenSSH服务器的[sshd_config](https://www.ssh.com/academy/ssh/sshd_config)文件默认只配置了少数设置。然而，默认配置包括X11转发，这在2016年的OpenSSH 7.2p1版本中包含一个命令注入漏洞。尽管如此，我们不需要GUI来管理我们的服务器。

#### 默认配置

默认配置

```shell-session
tr01ax@htb[/htb]$ cat /etc/ssh/sshd_config  | grep -v "#" | sed -r '/^\s*$/d'

Include /etc/ssh/sshd_config.d/*.conf
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
```

此配置文件中的大多数设置都被注释掉了，需要手动配置。

---

## 危险配置

尽管SSH协议是当今可用的最安全协议之一，但一些错误配置仍然可能使SSH服务器容易受到易于执行的攻击。让我们看看以下设置：

|**设置**|**描述**|
|---|---|
|`PasswordAuthentication yes`|允许基于密码的身份验证。|
|`PermitEmptyPasswords yes`|允许使用空密码。|
|`PermitRootLogin yes`|允许以root用户身份登录。|
|`Protocol 1`|使用过时的加密版本。|
|`X11Forwarding yes`|允许GUI应用程序的X11转发。|
|`AllowTcpForwarding yes`|允许TCP端口转发。|
|`PermitTunnel`|允许隧道。|
|`DebianBanner yes`|登录时显示特定横幅。|

允许`密码认证`使我们能够对已知用户名进行暴力破解以获取可能的密码。可以使用许多不同的方法来猜测用户的密码。为此，通常使用特定的`模式`来变异最常用的密码，并且令人恐惧的是，这些变异通常是正确的。这是因为我们人类是懒惰的，不想记住复杂和繁琐的密码。因此，我们创建易于记忆的密码，这导致例如数字或字符仅添加在密码末尾。相信密码是安全的，上述模式被用来猜测这些密码的这种"调整"。然而，有一些说明和[加固指南](https://www.ssh-audit.com/hardening_guides.html)可以用来加固我们的SSH服务器。

---

## 服务足迹侦察

我们可以用来对SSH服务器进行指纹识别的工具之一是[ssh-audit](https://github.com/jtesta/ssh-audit)。它检查客户端和服务器端的配置，并显示一些一般信息以及客户端和服务器仍在使用的加密算法。当然，这可以在稍后的密码层面用于攻击服务器或客户端。

#### SSH-Audit

SSH-Audit

```shell-session
tr01ax@htb[/htb]$ git clone https://github.com/jtesta/ssh-audit.git && cd ssh-audit
tr01ax@htb[/htb]$ ./ssh-audit.py 10.129.14.132

# general
(gen) banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3
(gen) software: OpenSSH 8.2p1
(gen) compatibility: OpenSSH 7.4+, Dropbear SSH 2018.76+
(gen) compression: enabled (zlib@openssh.com)

# key exchange algorithms
(kex) curve25519-sha256                     -- [info] available since OpenSSH 7.4, Dropbear SSH 2018.76
(kex) curve25519-sha256@libssh.org          -- [info] available since OpenSSH 6.5, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp256                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp384                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) ecdh-sha2-nistp521                    -- [fail] using weak elliptic curves
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(kex) diffie-hellman-group-exchange-sha256 (2048-bit) -- [info] available since OpenSSH 4.4
(kex) diffie-hellman-group16-sha512         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73
(kex) diffie-hellman-group18-sha512         -- [info] available since OpenSSH 7.3
(kex) diffie-hellman-group14-sha256         -- [info] available since OpenSSH 7.3, Dropbear SSH 2016.73

# host-key algorithms
(key) rsa-sha2-512 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) rsa-sha2-256 (3072-bit)               -- [info] available since OpenSSH 7.2
(key) ssh-rsa (3072-bit)                    -- [fail] using weak hashing algorithm
                                            `- [info] available since OpenSSH 2.5.0, Dropbear SSH 0.28
                                            `- [info] a future deprecation notice has been issued in OpenSSH 8.2: https://www.openssh.com/txt/release-8.2
(key) ecdsa-sha2-nistp256                   -- [fail] using weak elliptic curves
                                            `- [warn] using weak random number generator could reveal the key
                                            `- [info] available since OpenSSH 5.7, Dropbear SSH 2013.62
(key) ssh-ed25519                           -- [info] available since OpenSSH 6.5
...SNIP...
```

在输出的前几行中，我们首先看到的是显示OpenSSH服务器版本的横幅。之前的版本存在一些漏洞，例如[CVE-2020-14145](https://www.cvedetails.com/cve/CVE-2020-14145/)，它允许攻击者进行中间人攻击并攻击初始连接尝试。与OpenSSH服务器建立连接的详细输出通常也可以提供重要信息，例如服务器可以使用哪些身份验证方法。

#### 更改身份验证方法

更改身份验证方法

```shell-session
tr01ax@htb[/htb]$ ssh -v cry0l1t3@10.129.14.132

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
```

对于潜在的暴力破解攻击，我们可以使用SSH客户端选项 `PreferredAuthentications` 指定身份验证方法。

更改身份验证方法

```shell-session
tr01ax@htb[/htb]$ ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: password

cry0l1t3@10.129.14.132's password:
```

即使对于这种明显且安全的服务，我们也建议在我们的虚拟机上设置自己的OpenSSH服务器，进行实验，并熟悉不同的设置和选项。

在渗透测试期间，我们可能会遇到SSH服务器的各种横幅。默认情况下，横幅以可应用的协议版本开头，然后是服务器本身的版本。例如，使用 `SSH-1.99-OpenSSH_3.9p1`，我们知道可以使用SSH-1和SSH-2两种协议版本，并且我们正在处理OpenSSH服务器版本3.9p1。另一方面，对于横幅 `SSH-2.0-OpenSSH_8.2p1`，我们正在处理只接受SSH-2协议版本的OpenSSH版本8.2p1。

---

## Rsync

[Rsync](https://linux.die.net/man/1/rsync)是一个用于本地和远程复制文件的快速高效工具。它可用于在给定机器上本地复制文件，以及从远程主机复制文件或复制到远程主机。它非常灵活，以其增量传输算法（delta-transfer algorithm）而闻名。当目标主机上已存在文件的某个版本时，此算法减少了通过网络传输的数据量。它通过仅发送源文件与驻留在目标服务器上的旧版本文件之间的差异来实现这一点。它通常用于备份和镜像。它通过查看大小或最后修改时间发生变化的文件来查找需要传输的文件。默认情况下，它使用端口 `873`，可以配置为通过利用已建立的SSH服务器连接使用SSH进行安全文件传输。

这个[指南](https://book.hacktricks.xyz/network-services-pentesting/873-pentesting-rsync)涵盖了Rsync可能被滥用的一些方式，最值得注意的是列出目标服务器上共享文件夹的内容和检索文件。这有时可以在没有身份验证的情况下完成。其他时候我们需要凭据。如果在渗透测试期间找到凭据并在内部（或外部）主机上遇到Rsync，总是值得检查密码重用，因为你可能能够下载一些敏感文件，这些文件可用于获得对目标的远程访问。

让我们做一些快速的足迹侦察。我们可以看到Rsync正在使用协议31。

#### 扫描Rsync

扫描Rsync

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p 873 127.0.0.1

Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-19 09:31 EDT
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0058s latency).

PORT    STATE SERVICE VERSION
873/tcp open  rsync   (protocol version 31)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.13 seconds
```

#### 探测可访问的共享

我们接下来可以稍微探测一下服务，看看我们能获得什么访问权限。

探测可访问的共享

```shell-session
tr01ax@htb[/htb]$ nc -nv 127.0.0.1 873

(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
#list
dev            	Dev Tools
@RSYNCD: EXIT
```

#### 枚举开放共享

在这里我们可以看到一个名为 `dev` 的共享，我们可以进一步枚举它。

枚举开放共享

```shell-session
tr01ax@htb[/htb]$ rsync -av --list-only rsync://127.0.0.1/dev

receiving incremental file list
drwxr-xr-x             48 2022/09/19 09:43:10 .
-rw-r--r--              0 2022/09/19 09:34:50 build.sh
-rw-r--r--              0 2022/09/19 09:36:02 secrets.yaml
drwx------             54 2022/09/19 09:43:10 .ssh

sent 25 bytes  received 221 bytes  492.00 bytes/sec
total size is 0  speedup is 0.00
```

从上面的输出中，我们可以看到一些可能值得下载进行进一步调查的有趣文件。我们还可以看到一个可能包含 SSH 密钥的目录是可访问的。从这里，我们可以使用命令 `rsync -av rsync://127.0.0.1/dev` 将所有文件同步到我们的攻击主机。如果 Rsync 配置为使用 SSH 传输文件，我们可以修改命令包含 `-e ssh` 标志，如果 SSH 使用非标准端口，则使用 `-e "ssh -p2222"`。这个[指南](https://phoenixnap.com/kb/how-to-rsync-over-ssh)对于理解通过 SSH 使用 Rsync 的语法很有帮助。

---

## R-Services（R 服务）

R-Services 是一套托管服务，用于通过 TCP/IP 在 Unix 主机之间实现远程访问或发出命令。最初由加州大学伯克利分校的计算机系统研究组（`CSRG`）开发，`r-services` 是 Unix 操作系统之间远程访问的事实标准，直到由于其固有的安全缺陷而被安全外壳（`SSH`）协议和命令所取代。与 `telnet` 一样，r-services 通过网络以未加密格式在客户端和服务器之间传输信息，这使得攻击者可以通过执行中间人（`MITM`）攻击来截获网络流量（密码、登录信息等）。

`R-services` 跨越端口 `512`、`513` 和 `514`，只能通过一套称为 `r-commands` 的程序访问。它们最常被商业操作系统使用，如 Solaris、HP-UX 和 AIX。虽然现在不太常见，但我们在内部渗透测试中偶尔会遇到它们，因此值得了解如何处理它们。

[R-commands](https://en.wikipedia.org/wiki/Berkeley_r-commands) 套件由以下程序组成：

- rcp（`remote copy`，远程复制）
- rexec（`remote execution`，远程执行）
- rlogin（`remote login`，远程登录）
- rsh（`remote shell`，远程 shell）
- rstat
- ruptime
- rwho（`remote who`，远程用户查询）

每个命令都有其预期功能；但是，我们只会介绍最常被滥用的 `r-commands`。下表将提供最常被滥用命令的快速概述，包括它们与之交互的服务守护进程、可以访问的端口和传输方法，以及每个命令的简要描述。

|**命令**|**服务守护进程**|**端口**|**传输协议**|**描述**|
|---|---|---|---|---|
|`rcp`|`rshd`|514|TCP|从本地系统双向复制文件或目录到远程系统（或反之），或从一个远程系统到另一个远程系统。它的工作方式类似于 Linux 上的 `cp` 命令，但`不会警告用户覆盖系统上的现有文件`。|
|`rsh`|`rshd`|514|TCP|在远程机器上打开一个 shell，无需登录过程。依赖 `/etc/hosts.equiv` 和 `.rhosts` 文件中的信任条目进行验证。|
|`rexec`|`rexecd`|512|TCP|使用户能够在远程机器上运行 shell 命令。需要通过未加密的网络套接字使用`用户名`和`密码`进行身份验证。身份验证可被 `/etc/hosts.equiv` 和 `.rhosts` 文件中的信任条目覆盖。|
|`rlogin`|`rlogind`|513|TCP|使用户能够通过网络登录到远程主机。它的工作方式类似于 `telnet`，但只能连接到类 Unix 主机。身份验证可被 `/etc/hosts.equiv` 和 `.rhosts` 文件中的信任条目覆盖。|

/etc/hosts.equiv 文件包含受信任主机列表，用于授予网络上其他系统的访问权限。当这些主机上的用户尝试访问系统时，他们会自动获得访问权限，无需进一步身份验证。

#### /etc/hosts.equiv

/etc/hosts.equiv

```shell-session
tr01ax@htb[/htb]$ cat /etc/hosts.equiv

# <hostname> <local username>
pwnbox cry0l1t3
```

现在我们对 `r-commands` 有了基本了解，让我们使用 `Nmap` 进行快速信息收集，以确定所有必要的端口是否都已开放。

#### 扫描 R-Services

扫描 R-Services

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p 512,513,514 10.0.17.2

Starting Nmap 7.80 ( https://nmap.org ) at 2022-12-02 15:02 EST
Nmap scan report for 10.0.17.2
Host is up (0.11s latency).

PORT    STATE SERVICE    VERSION
512/tcp open  exec?
513/tcp open  login?
514/tcp open  tcpwrapped

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 145.54 seconds
```

#### 访问控制与信任关系

`r-services` 的主要问题，也是引入 `SSH` 来替代它的主要原因之一，是这些协议在访问控制方面存在固有问题。R-services 依赖于从远程客户端发送到它们尝试进行身份验证的主机机器的信任信息。默认情况下，这些服务使用[可插拔认证模块（PAM）](https://debathena.mit.edu/trac/wiki/PAM)对远程系统上的用户进行身份验证；但是，它们也可以通过系统上的 `/etc/hosts.equiv` 和 `.rhosts` 文件绕过此身份验证。`hosts.equiv` 和 `.rhosts` 文件包含当使用 `r-commands` 进行连接尝试时，本地主机`信任`的主机（`IP` 或 `主机名`）和用户列表。这两个文件中的条目可能如下所示：

**注意：** `hosts.equiv` 文件被视为系统上所有用户的全局配置，而 `.rhosts` 提供每用户配置。

#### 示例 .rhosts 文件

示例 .rhosts 文件

```shell-session
tr01ax@htb[/htb]$ cat .rhosts

htb-student     10.0.17.5
+               10.0.17.10
+               +
```

从这个例子中我们可以看到，这两个文件都遵循 `<用户名> <IP 地址>` 或 `<用户名> <主机名>` 对的特定语法。此外，`+` 修饰符可以在这些文件中用作通配符来指定任何内容。在这个例子中，`+` 修饰符允许任何外部用户通过 IP 地址为 `10.0.17.10` 的主机从 `htb-student` 用户账户访问 r-commands。

这两个文件中的任何配置错误都可能允许攻击者在没有凭据的情况下以另一个用户身份进行身份验证，有可能获得代码执行权限。现在我们了解了如何潜在地滥用这些文件中的配置错误，让我们尝试使用 `rlogin` 登录到目标主机。

#### 使用 Rlogin 登录

使用 Rlogin 登录

```shell-session
tr01ax@htb[/htb]$ rlogin 10.0.17.2 -l htb-student

Last login: Fri Dec  2 16:11:21 from localhost

[htb-student@localhost ~]$
```

由于 `.rhosts` 文件中的配置错误，我们已成功以远程主机上的 `htb-student` 账户登录。成功登录后，我们还可以滥用 `rwho` 命令通过向 UDP 端口 513 发送请求来列出本地网络上的所有交互式会话。

#### 使用 Rwho 列出已认证用户

使用 Rwho 列出已认证用户

```shell-session
tr01ax@htb[/htb]$ rwho

root     web01:pts/0 Dec  2 21:34
htb-student     workstn01:tty1  Dec  2 19:57  2:25
```

从这些信息中，我们可以看到 `htb-student` 用户当前已认证到 `workstn01` 主机，而 `root` 用户已认证到 `web01` 主机。当我们在网络上的主机上进行进一步攻击时，我们可以利用这些信息来确定潜在的用户名。但是，`rwho` 守护进程会定期广播已登录用户的信息，因此监视网络流量可能会有益处。

#### 使用 Rusers 列出已认证用户

为了与 `rwho` 配合提供更多信息，我们可以发出 `rusers` 命令。这将为我们提供网络上所有已登录用户的更详细账户信息，包括用户名、访问机器的主机名、用户登录的 TTY、用户登录的日期和时间、用户自上次敲击键盘以来的时间，以及他们登录的远程主机（如果适用）。

使用 Rusers 列出已认证用户

```shell-session
tr01ax@htb[/htb]$ rusers -al 10.0.17.5

htb-student     10.0.17.5:console          Dec 2 19:57     2:25
```

正如我们所见，由于 R-services 固有的安全缺陷以及 SSH 等更安全协议的可用性，现在它们的使用频率较低。作为一名全面的信息安全专业人员，我们必须对许多系统、应用程序、协议等有广泛而深入的了解。所以，将关于 R-services 的知识记录下来，因为你永远不知道什么时候会遇到它们。

---

## 最后的思考

远程管理服务可以为我们提供大量数据，并且通常可以通过弱/默认凭据或密码重用来滥用进行未授权访问。我们应该始终尽可能多地从这些服务中探测信息，不放过任何可能的线索，特别是当我们从目标网络的其他地方编译了一份凭据列表时。#windows #footprinting #enumeration #hacking #rdp #port5985 #port5986 #port135 #port3389
[source](https://academy.hackthebox.com/module/112/section/1242)
[[notes about footprinting]]


---

Windows 服务器可以使用服务器管理器在远程服务器上进行本地管理任务。从 Windows Server 2016 开始，默认启用远程管理。远程管理是 Windows 硬件管理功能的一个组件，用于本地和远程管理服务器硬件。这些功能包括实现 WS-Management 协议的服务、通过基板管理控制器进行硬件诊断和控制，以及使我们能够编写通过 WS-Management 协议远程通信的应用程序的 COM API 和脚本对象。

用于 Windows 和 Windows 服务器远程管理的主要组件如下：

- 远程桌面协议（`RDP`）

- Windows 远程管理（`WinRM`）

- Windows 管理规范（`WMI`）


---

## RDP

[远程桌面协议](https://docs.microsoft.com/en-us/troubleshoot/windows-server/remote/understanding-remote-desktop-protocol)（`RDP`）是微软开发的用于远程访问运行 Windows 操作系统的计算机的协议。该协议允许通过 GUI（图形用户界面）加密显示和控制命令通过 IP 网络传输。RDP 工作在 TCP/IP 参考模型的应用层，通常使用 TCP 端口 3389 作为传输协议。但是，无连接的 UDP 协议也可以使用端口 3389 进行远程管理。

为了建立 RDP 会话，网络防火墙和服务器上的防火墙都必须允许来自外部的连接。如果在客户端和服务器之间的路由上使用[网络地址转换](https://en.wikipedia.org/wiki/Network_address_translation)（`NAT`），就像互联网连接中常见的那样，远程计算机需要公共 IP 地址才能到达服务器。此外，必须在 NAT 路由器上设置端口转发指向服务器。

自 Windows Vista 以来，RDP 已处理[传输层安全性](https://en.wikipedia.org/wiki/Transport_Layer_Security)（`TLS/SSL`），这意味着所有数据，特别是登录过程，通过其良好的加密在网络中受到保护。然而，许多 Windows 系统并不坚持这一点，仍然接受通过 [RDP 安全性](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/8e8b2cca-c1fa-456c-8ecb-a82fc60b2322)的不充分加密。尽管如此，即使有这个，攻击者仍然远没有被锁在外面，因为提供身份的证书默认只是自签名的。这意味着客户端无法区分真正的证书和伪造的证书，并为用户生成证书警告。

`远程桌面`服务默认安装在 Windows 服务器上，不需要额外的外部应用程序。可以使用`服务器管理器`激活此服务，默认设置是只允许具有[网络级别身份验证](https://en.wikipedia.org/wiki/Network_Level_Authentication)（`NLA`）的主机连接到该服务。

---

## 服务信息收集

扫描 RDP 服务可以快速为我们提供大量关于主机的信息。例如，我们可以确定服务器上是否启用了 `NLA`、产品版本和主机名。

Nmap

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --script rdp*

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 15:45 CET
Nmap scan report for 10.129.201.248
Host is up (0.036s latency).

PORT     STATE SERVICE       VERSION
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-enum-encryption:
|   Security layer
|     CredSSP (NLA): SUCCESS
|     CredSSP with Early User Auth: SUCCESS
|_    RDSTLS: SUCCESS
| rdp-ntlm-info:
|   Target_Name: ILF-SQL-01
|   NetBIOS_Domain_Name: ILF-SQL-01
|   NetBIOS_Computer_Name: ILF-SQL-01
|   DNS_Domain_Name: ILF-SQL-01
|   DNS_Computer_Name: ILF-SQL-01
|   Product_Version: 10.0.17763
|_  System_Time: 2021-11-06T13:46:00+00:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.26 seconds
```

此外，我们可以使用 `--packet-trace` 来跟踪各个数据包并手动检查其内容。我们可以看到 Nmap 用于与 RDP 服务器交互的 `RDP cookies`（`mstshash=nmap`）可以被`威胁猎人`和各种安全服务（如[端点检测和响应](https://en.wikipedia.org/wiki/Endpoint_detection_and_response)（`EDR`））识别，并可能在加固网络上将我们作为渗透测试人员锁定在外。

Nmap

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 16:23 CET
SENT (0.2506s) ICMP [10.10.14.20 > 10.129.201.248 Echo request (type=8/code=0) id=8338 seq=0] IP [ttl=53 id=5122 iplen=28 ]
SENT (0.2507s) TCP 10.10.14.20:55516 > 10.129.201.248:443 S ttl=42 id=24195 iplen=44  seq=1926233369 win=1024 <mss 1460>
SENT (0.2507s) TCP 10.10.14.20:55516 > 10.129.201.248:80 A ttl=55 id=50395 iplen=40  seq=0 win=1024
SENT (0.2517s) ICMP [10.10.14.20 > 10.129.201.248 Timestamp request (type=13/code=0) id=8247 seq=0 orig=0 recv=0 trans=0] IP [ttl=38 id=62695 iplen=40 ]
RCVD (0.2814s) ICMP [10.129.201.248 > 10.10.14.20 Echo reply (type=0/code=0) id=8338 seq=0] IP [ttl=127 id=38158 iplen=28 ]
SENT (0.3264s) TCP 10.10.14.20:55772 > 10.129.201.248:3389 S ttl=56 id=274 iplen=44  seq=2635590698 win=1024 <mss 1460>
RCVD (0.3565s) TCP 10.129.201.248:3389 > 10.10.14.20:55772 SA ttl=127 id=38162 iplen=44  seq=3526777417 win=64000 <mss 1357>
NSOCK INFO [0.4500s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.4500s] nsock_connect_tcp(): TCP connection requested to 10.129.201.248:3389 (IOD #1) EID 8
NSOCK INFO [0.4820s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 8 [10.129.201.248:3389]
Service scan sending probe NULL to 10.129.201.248:3389 (tcp)
NSOCK INFO [0.4830s] nsock_read(): Read request from IOD #1 [10.129.201.248:3389] (timeout: 6000ms) EID 18
NSOCK INFO [6.4880s] nsock_trace_handler_callback(): Callback: READ TIMEOUT for EID 18 [10.129.201.248:3389]
Service scan sending probe TerminalServerCookie to 10.129.201.248:3389 (tcp)
NSOCK INFO [6.4880s] nsock_write(): Write request for 42 bytes to IOD #1 EID 27 [10.129.201.248:3389]
NSOCK INFO [6.4880s] nsock_read(): Read request from IOD #1 [10.129.201.248:3389] (timeout: 5000ms) EID 34
NSOCK INFO [6.4880s] nsock_trace_handler_callback(): Callback: WRITE SUCCESS for EID 27 [10.129.201.248:3389]
NSOCK INFO [6.5240s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 34 [10.129.201.248:3389] (19 bytes): .........4.........
Service scan match (Probe TerminalServerCookie matched with TerminalServerCookie line 13640): 10.129.201.248:3389 is ms-wbt-server.  Version: |Microsoft Terminal Services|||

...SNIP...

NSOCK INFO [6.5610s] nsock_write(): Write request for 54 bytes to IOD #1 EID 27 [10.129.201.248:3389]
NSE: TCP 10.10.14.20:36630 > 10.129.201.248:3389 | 00000000: 03 00 00 2a 25 e0 00 00 00 00 00 43 6f 6f 6b 69    *%      Cooki
00000010: 65 3a 20 6d 73 74 73 68 61 73 68 3d 6e 6d 61 70 e: mstshash=nmap
00000020: 0d 0a 01 00 08 00 0b 00 00 00

...SNIP...

NSOCK INFO [6.6820s] nsock_write(): Write request for 57 bytes to IOD #2 EID 67 [10.129.201.248:3389]
NSOCK INFO [6.6820s] nsock_trace_handler_callback(): Callback: WRITE SUCCESS for EID 67 [10.129.201.248:3389]
NSE: TCP 10.10.14.20:36630 > 10.129.201.248:3389 | SEND
NSOCK INFO [6.6820s] nsock_read(): Read request from IOD #2 [10.129.201.248:3389] (timeout: 5000ms) EID 74
NSOCK INFO [6.7180s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 74 [10.129.201.248:3389] (211 bytes)
NSE: TCP 10.10.14.20:36630 < 10.129.201.248:3389 |
00000000: 30 81 d0 a0 03 02 01 06 a1 81 c8 30 81 c5 30 81 0          0  0
00000010: c2 a0 81 bf 04 81 bc 4e 54 4c 4d 53 53 50 00 02        NTLMSSP
00000020: 00 00 00 14 00 14 00 38 00 00 00 35 82 8a e2 b9        8   5
00000030: 73 b0 b3 91 9f 1b 0d 00 00 00 00 00 00 00 00 70 s              p
00000040: 00 70 00 4c 00 00 00 0a 00 63 45 00 00 00 0f 49  p L     cE    I
00000050: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
00000060: 00 31 00 02 00 14 00 49 00 4c 00 46 00 2d 00 53  1     I L F - S
00000070: 00 51 00 4c 00 2d 00 30 00 31 00 01 00 14 00 49  Q L - 0 1     I
00000080: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
00000090: 00 31 00 04 00 14 00 49 00 4c 00 46 00 2d 00 53  1     I L F - S
000000a0: 00 51 00 4c 00 2d 00 30 00 31 00 03 00 14 00 49  Q L - 0 1     I
000000b0: 00 4c 00 46 00 2d 00 53 00 51 00 4c 00 2d 00 30  L F - S Q L - 0
000000c0: 00 31 00 07 00 08 00 1d b3 e8 f2 19 d3 d7 01 00  1
000000d0: 00 00 00

...SNIP...
```

[Cisco CX Security Labs](https://github.com/CiscoCXSecurity) 还开发了一个名为 [rdp-sec-check.pl](https://github.com/CiscoCXSecurity/rdp-sec-check) 的 Perl 脚本，可以基于握手在未认证的情况下识别 RDP 服务器的安全设置。

RDP 安全检查 - 安装

```shell-session
tr01ax@htb[/htb]$ sudo cpan

Loading internal logger. Log::Log4perl recommended for better logging

CPAN.pm requires configuration, but most of it can be done automatically.
If you answer 'no' below, you will enter an interactive dialog for each
configuration option instead.

Would you like to configure as much as possible automatically? [yes] yes


Autoconfiguration complete.

commit: wrote '/root/.cpan/CPAN/MyConfig.pm'

You can re-run configuration any time with 'o conf init' in the CPAN shell

cpan shell -- CPAN exploration and modules installation (v2.27)
Enter 'h' for help.


cpan[1]> install Encoding::BER

Fetching with LWP:
http://www.cpan.org/authors/01mailrc.txt.gz
Reading '/root/.cpan/sources/authors/01mailrc.txt.gz'
............................................................................DONE
...SNIP...
```

RDP 安全检查

```shell-session
tr01ax@htb[/htb]$ git clone https://github.com/CiscoCXSecurity/rdp-sec-check.git && cd rdp-sec-check
tr01ax@htb[/htb]$ ./rdp-sec-check.pl 10.129.201.248

Starting rdp-sec-check v0.9-beta ( http://labs.portcullis.co.uk/application/rdp-sec-check/ ) at Sun Nov  7 16:50:32 2021

[+] Scanning 1 hosts

Target:    10.129.201.248
IP:        10.129.201.248
Port:      3389

[+] Checking supported protocols

[-] Checking if RDP Security (PROTOCOL_RDP) is supported...Not supported - HYBRID_REQUIRED_BY_SERVER
[-] Checking if TLS Security (PROTOCOL_SSL) is supported...Not supported - HYBRID_REQUIRED_BY_SERVER
[-] Checking if CredSSP Security (PROTOCOL_HYBRID) is supported [uses NLA]...Supported

[+] Checking RDP Security Layer

[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_NONE...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_40BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_128BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_56BIT...Not supported
[-] Checking RDP Security Layer with encryption ENCRYPTION_METHOD_FIPS...Not supported

[+] Summary of protocol support

[-] 10.129.201.248:3389 supports PROTOCOL_SSL   : FALSE
[-] 10.129.201.248:3389 supports PROTOCOL_HYBRID: TRUE
[-] 10.129.201.248:3389 supports PROTOCOL_RDP   : FALSE

[+] Summary of RDP encryption support

[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_NONE   : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_40BIT  : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_128BIT : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_56BIT  : FALSE
[-] 10.129.201.248:3389 supports ENCRYPTION_METHOD_FIPS   : FALSE

[+] Summary of security issues


rdp-sec-check v0.9-beta completed at Sun Nov  7 16:50:33 2021
```

可以通过多种方式对此类 RDP 服务器进行身份验证和连接。例如，我们可以使用 `xfreerdp`、`rdesktop` 或 `Remmina` 在 Linux 上连接到 RDP 服务器，并相应地与服务器的 GUI 进行交互。

#### 启动 RDP 会话

启动 RDP 会话

```shell-session
tr01ax@htb[/htb]$ xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248

[16:37:47:135] [95319:95320] [INFO][com.freerdp.core] - freerdp_connect:freerdp_set_last_error_ex resetting error state
[16:37:47:135] [95319:95320] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpdr
[16:37:47:135] [95319:95320] [INFO][com.freerdp.client.common.cmdline] - loading channelEx rdpsnd
[16:37:47:135] [95319:95320] [INFO][com.freerdp.client.common.cmdline] - loading channelEx cliprdr
[16:37:47:447] [95319:95320] [INFO][com.freerdp.primitives] - primitives autodetect, using optimized
[16:37:47:453] [95319:95320] [INFO][com.freerdp.core] - freerdp_tcp_is_hostname_resolvable:freerdp_set_last_error_ex resetting error state
[16:37:47:453] [95319:95320] [INFO][com.freerdp.core] - freerdp_tcp_connect:freerdp_set_last_error_ex resetting error state
[16:37:47:523] [95319:95320] [INFO][com.freerdp.crypto] - creating directory /home/cry0l1t3/.config/freerdp
[16:37:47:523] [95319:95320] [INFO][com.freerdp.crypto] - creating directory [/home/cry0l1t3/.config/freerdp/certs]
[16:37:47:523] [95319:95320] [INFO][com.freerdp.crypto] - created directory [/home/cry0l1t3/.config/freerdp/server]
[16:37:47:599] [95319:95320] [WARN][com.freerdp.crypto] - Certificate verification failure 'self signed certificate (18)' at stack position 0
[16:37:47:599] [95319:95320] [WARN][com.freerdp.crypto] - CN = ILF-SQL-01
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - @           WARNING: CERTIFICATE NAME MISMATCH!           @
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - The hostname used for this connection (10.129.201.248:3389)
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - does not match the name given in the certificate:
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - Common Name (CN):
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] -      ILF-SQL-01
[16:37:47:600] [95319:95320] [ERROR][com.freerdp.crypto] - A valid certificate for the wrong name should NOT be trusted!
Certificate details for 10.129.201.248:3389 (RDP-Server):
        Common Name: ILF-SQL-01
        Subject:     CN = ILF-SQL-01
        Issuer:      CN = ILF-SQL-01
        Thumbprint:  b7:5f:00:ca:91:00:0a:29:0c:b5:14:21:f3:b0:ca:9e:af:8c:62:d6:dc:f9:50:ec:ac:06:38:1f:c5:d6:a9:39
The above X.509 certificate could not be verified, possibly because you do not have
the CA certificate in your certificate store, or the certificate has expired.
Please look at the OpenSSL documentation on how to add a private CA to the store.


Do you trust the above certificate? (Y/T/N) y

[16:37:48:801] [95319:95320] [INFO][com.winpr.sspi.NTLM] - VERSION ={
[16:37:48:801] [95319:95320] [INFO][com.winpr.sspi.NTLM] -      ProductMajorVersion: 6
[16:37:48:801] [95319:95320] [INFO][com.winpr.sspi.NTLM] -      ProductMinorVersion: 1
[16:37:48:801] [95319:95320] [INFO][com.winpr.sspi.NTLM] -      ProductBuild: 7601
[16:37:48:801] [95319:95320] [INFO][com.winpr.sspi.NTLM] -      Reserved: 0x000000
```

成功认证后，将出现一个新窗口，可以访问我们连接的服务器的桌面。

---

## WinRM

Windows 远程管理（`WinRM`）是一个简单的基于命令行的 Windows 集成远程管理协议。WinRM 使用简单对象访问协议（`SOAP`）来建立与远程主机及其应用程序的连接。因此，从 Windows 10 开始，必须显式启用和配置 WinRM。WinRM 依赖于 `TCP` 端口 `5985` 和 `5986` 进行通信，其中后者端口 `5986 使用 HTTPS`，因为之前端口 80 和 443 曾用于此任务。但是，由于端口 80 主要因安全原因被阻止，因此现在使用较新的端口 5985 和 5986。

另一个适合 WinRM 进行管理的组件是 Windows 远程 Shell（`WinRS`），它让我们可以在远程系统上执行任意命令。该程序甚至默认包含在 Windows 7 中。因此，使用 WinRM，可以在另一台服务器上执行远程命令。

PowerShell 远程会话和事件日志合并等服务需要 WinRM。从 `Windows Server 2012` 版本开始默认启用，但对于旧版服务器和客户端，必须首先进行配置，并创建必要的防火墙例外。

---

## 服务信息收集

正如我们已经知道的，WinRM 默认使用 TCP 端口 `5985`（`HTTP`）和 `5986`（`HTTPS`），我们可以使用 Nmap 进行扫描。但是，我们经常会看到只使用 HTTP（`TCP 5985`）而不是 HTTPS（`TCP 5986`）。

Nmap WinRM

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p5985,5986 --disable-arp-ping -n

Starting Nmap 7.92 ( https://nmap.org ) at 2021-11-06 16:31 CET
Nmap scan report for 10.129.201.248
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.34 seconds
```

如果我们想确定一台或多台远程服务器是否可以通过 WinRM 访问，我们可以使用 PowerShell 轻松做到这一点。[Test-WsMan](https://docs.microsoft.com/en-us/powershell/module/microsoft.wsman.management/test-wsman?view=powershell-7.2) cmdlet 负责此操作，并将要查询的主机名传递给它。在基于 Linux 的环境中，我们可以使用名为 [evil-winrm](https://github.com/Hackplayers/evil-winrm) 的工具，这是另一个专门设计用于与 WinRM 交互的渗透测试工具。

Nmap WinRM

```shell-session
tr01ax@htb[/htb]$ evil-winrm -i 10.129.201.248 -u Cry0l1t3 -p P455w0rD!

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Cry0l1t3\Documents>
```

---

## WMI

Windows 管理规范（`WMI`）是微软对通用信息模型（`CIM`）的实现和扩展，是 Windows 平台上标准化基于 Web 的企业管理（`WBEM`）的核心功能。WMI 允许对 Windows 系统上几乎所有设置进行读写访问。可以理解的是，这使它成为 Windows 环境中用于管理和远程维护 Windows 计算机（无论是 PC 还是服务器）的最关键接口。WMI 通常通过 PowerShell、VBScript 或 Windows 管理规范控制台（`WMIC`）访问。WMI 不是单个程序，而是由多个程序和各种数据库（也称为存储库）组成。

---

## 服务信息收集

WMI 通信的初始化始终在 `TCP` 端口 `135` 上进行，成功建立连接后，通信将移至随机端口。例如，可以使用 Impacket 工具包中的程序 [wmiexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py) 来完成此操作。

WMIexec.py

```shell-session
tr01ax@htb[/htb]$ /usr/share/doc/python3-impacket/examples/wmiexec.py Cry0l1t3:"P455w0rD!"@10.129.201.248 "hostname"

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] SMBv3.0 dialect used
ILF-SQL-01
```

再次需要提到的是，通过在我们自己的 Windows Server 虚拟机上安装这些服务并尝试配置来获得经验，以及从功能原理和管理员角度来发展理解，这是阅读手册无法替代的。因此，我们强烈建议设置自己的 Windows Server，试验这些设置，并反复扫描这些服务以查看结果中的差异。#footprinting #hacking #services #enumeration #smb #ftp #dns #nfs #nmap

source: https://academy.hackthebox.com/module/112/section/1060

一个错误方法的例子可能是，在找到 SSH、RDP、WinRM 等身份验证服务后，**我们尝试使用常见/弱密码和用户名进行暴力破解。不幸的是，暴力破解是一种嘈杂的方法，很容易导致被列入黑名单，使进一步测试变得不可能。** 主要是，如果我们不了解公司的防御安全措施及其基础设施，就可能发生这种情况。有些人可能会对这种方法一笑置之，但经验表明，太多测试人员采用了这种类型的方法。

[Lesson 01 - Enumeration](hacking/HackTheBox/modules/Footprinting/Lesson%2001%20-%20Enumeration.md)

👉👉 **我们的目标不是入侵系统，而是找到所有可能的入侵途径。**

### 枚举原则：

[Lesson 01 - Enumeration](hacking/HackTheBox/modules/Footprinting/Lesson%2001%20-%20Enumeration.md)

- 我们能看到什么？
- 我们看到它的原因可能是什么？
- 我们看到的内容为我们构建了什么样的图景？
- 我们能从中获得什么？
- 我们如何利用它？
- 我们看不到什么？
- 我们看不到的原因可能是什么？
- 我们看不到的内容为我们构建了什么样的图景？

|   |   |
|---|---|
|1.|**眼见不一定为实。考虑所有的视角。**|
|2.|**区分我们能看到的和看不到的。**|
|3.|**总有方法获取更多信息。理解目标。**|

### 枚举方法论

[Lesson 02 - Enumeration methodology](Lesson%2002%20-%20Enumeration%20methodology.md)
#### 枚举作为一个过程分为三个层级：

* 基于基础设施的枚举（Infrastructure-based enumeration）
* 基于主机的枚举（Host-based enumeration）
* 基于操作系统的枚举（OS-based enumeration）

#### 上述三个层级被划分为六个层次：

|**层次**|**描述**|**信息类别**|
|---|---|---|
|`1. 互联网存在`|识别互联网存在和外部可访问的基础设施。`此层次的目标是识别所有可能的目标系统和可测试的接口。`|域名、子域名、虚拟主机（vHosts）、ASN（自治系统号）、网段、IP地址、云实例、安全措施|
|`2. 网关`|识别保护公司外部和内部基础设施的可能安全措施。`目标是了解我们面对的是什么以及需要注意什么。`|防火墙、DMZ（隔离区）、IPS/IDS（入侵防御/检测系统）、EDR（端点检测与响应）、代理、NAC（网络访问控制）、网络分段、VPN、Cloudflare|
|`3. 可访问服务`|识别外部或内部托管的可访问接口和服务。`此层次旨在理解目标系统的原因和功能，并获取必要的知识以有效地与其通信和利用。`|服务类型、功能、配置、端口、版本、接口|
|`4. 进程`|识别与服务相关的内部进程、来源和目标。`此处的目标是理解这些因素并识别它们之间的依赖关系。`|PID（进程ID）、处理的数据、任务、来源、目标|
|`5. 权限`|识别对可访问服务的内部权限和特权。`识别这些并理解这些权限能做什么和不能做什么至关重要。`|组、用户、权限、限制、环境|
|`6. 操作系统配置`|识别内部组件和系统配置。`此处的目标是了解管理员如何管理系统以及我们可以从中获取什么敏感内部信息。`|操作系统类型、补丁级别、网络配置、操作系统环境、配置文件、敏感私有文件|


#### 显示层级和层次的图像：

[image](obsidian://open?vault=stff&file=files%2FPasted%20image%2020230915134646.png)
![[Pasted image 20230915134646.png]]


### 域名信息：
[Lesson 03 - Domain information](Lesson%2003%20-%20Domain%20information.md)

👉 我们首先应该做的是仔细审查公司的**主网站**。然后，我们应该阅读文本内容，同时注意这些服务需要什么技术和结构。

#### 在线存在

互联网上的第一个存在点可能是我们可以检查的公司主网站的`SSL证书`。通常，这样的证书包含的不仅仅是一个子域名，这意味着该证书用于多个域名，而这些域名很可能仍然是活跃的。
另一个查找更多子域名的来源是 [crt.sh](https://crt.sh/)。这个来源是[证书透明度](https://en.wikipedia.org/wiki/Certificate_Transparency)（Certificate Transparency）日志。证书透明度是一个旨在验证加密互联网连接所颁发的数字证书的过程。

我们也可以以JSON格式输出结果：
* ```curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq .```

我们可以过滤出唯一的子域名：
* ```curl -s https://crt.sh/\?q\=inlanefreight.com\&output\=json | jq . | grep name | cut -d":" -f2 | grep -v "CN=" | cut -d'"' -f2 | awk '{gsub(/\\n/,"\n");}1;' | sort -u```

公司托管的服务器（使用上一步创建的子域名）：
* ```for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done```

Shodan IP列表
* ```for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f4 >> ip-addresses.txt;done```
* ```for i in $(cat ip-addresses.txt);do shodan host $i;done```

#### DNS记录

```dig any inlanefreight.com```

- `A`记录：我们通过A记录识别指向特定（子）域名的IP地址。这里我们只看到一个我们已经知道的。
- `MX`记录：邮件服务器记录向我们展示哪个邮件服务器负责管理公司的电子邮件。由于在我们的案例中这是由Google处理的，我们应该记录下来并暂时跳过。
- `NS`记录：这类记录显示使用哪些名称服务器将FQDN（完全限定域名）解析为IP地址。大多数托管提供商使用自己的名称服务器，这使得识别托管提供商更加容易。
- `TXT`记录：这种类型的记录通常包含不同第三方提供商的验证密钥以及DNS的其他安全方面，如[SPF](https://datatracker.ietf.org/doc/html/rfc7208)（发件人策略框架）、[DMARC](https://datatracker.ietf.org/doc/html/rfc7489)（基于域的邮件认证报告和一致性）和[DKIM](https://datatracker.ietf.org/doc/html/rfc6376)（域名密钥识别邮件），它们负责验证和确认发送邮件的来源。如果我们仔细查看结果，这里已经可以看到一些有价值的信息。

### 云资源
[Lesson 04 - Cloud resources](Lesson%2004%20-%20Cloud%20resources.md)

#### 如何查找云存储：
* 最简单和最常用的方法之一是Google搜索结合Google Dorks。例如，我们可以使用Google Dorks `inurl:` 和 `intext:` 将搜索范围缩小到特定术语。
* [domain.glass](https://domain.glass) 等提供商也可以告诉我们很多关于公司基础设施的信息
* 另一个非常有用的提供商是 [GrayHatWarfare](https://buckets.grayhatwarfare.com)。我们可以进行许多不同的搜索，发现AWS、Azure和GCP云存储，甚至可以按文件格式排序和过滤。因此，一旦我们通过Google找到它们，我们也可以在GrayHatWarefare上搜索它们，并被动地发现给定云存储中存储了哪些文件。

### 员工

在社交媒体平台上搜索和识别员工也可以揭示很多关于团队基础设施和组成的信息。这反过来可以让我们识别正在使用的技术、编程语言甚至软件应用程序。在很大程度上，我们还可以根据每个人的技能评估其关注重点。与他人分享的帖子和材料也是很好的指标，表明此人目前正在从事什么工作以及此人目前认为与他人分享什么是重要的。

公司总是雇用技能可以应用于业务的员工。例如，我们知道Flask和Django是Python编程语言的Web框架。
如果我们稍微搜索一下Django安全配置错误，我们最终会找到以下描述Django OWASP Top10的[Github仓库](https://github.com/boomcamp/django-security)。

### FTP

[[Lesson 06 - FTP]]

### SMB

[[Lesson 07 - SMB]]

`服务器消息块`（`SMB`，Server Message Block）是一种客户端-服务器协议，用于管理对文件、整个目录以及其他网络资源（如打印机、路由器或为网络发布的接口）的访问。不同系统进程之间的信息交换也可以基于SMB协议处理。[SMB](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-smb/f210069c-7086-4dc2-885e-861d837df688) 首次向更广泛的公众开放，例如作为OS/2网络操作系统LAN Manager和LAN Server的一部分。从那时起，该协议的主要应用领域特别是Windows操作系统系列，其网络服务以向下兼容的方式支持SMB——这意味着安装了较新版本的设备可以轻松地与安装了较旧Microsoft操作系统的设备通信。通过自由软件项目Samba，还有一个解决方案可以在Linux和Unix发行版中使用SMB，从而实现通过SMB的跨平台通信。

SMB协议使客户端能够与同一网络中的其他参与者通信，以访问网络上与其共享的文件或服务。另一个系统也必须实现网络协议并使用SMB服务器应用程序接收和处理客户端请求。然而，在此之前，双方必须建立连接，这就是为什么它们首先要交换相应的消息。

在IP网络中，SMB使用TCP协议，该协议规定在最终建立连接之前客户端和服务器之间进行三次握手。TCP协议的规范还管理后续的数据传输。我们可以在[这里](https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-SMB2/%5bMS-SMB2%5d.pdf#%5B%7B%22num%22%3A920%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C69%2C738%2C0%5D)查看一些示例。

SMB服务器可以将其本地文件系统的任意部分作为共享提供。因此，客户端可见的层次结构部分独立于服务器上的结构。访问权限由`访问控制列表`（`ACL`，Access Control Lists）定义。它们可以基于`执行`、`读取`和`完全访问`等属性对单个用户或用户组进行细粒度控制。ACL是基于共享定义的，因此与服务器上本地分配的权限不对应。

[...] 当我们通过Samba向较旧的NetBIOS服务传递SMB命令时，它通常通过TCP端口`137`、`138`、`139`连接到Samba服务器，但CIFS仅使用TCP端口`445`

#### 列出smb/samba共享

```shell-session
smbclient -N -L //10.129.14.128
```

连接：
```
smbclient //10.129.14.128/notes
```

一旦我们发现有趣的文件或文件夹，我们可以使用`get`命令下载它们。Smbclient还允许我们通过在开头使用感叹号（`!<cmd>`）来执行本地系统命令，而不中断连接。

Nmap也有许多选项和NSE脚本，可以帮助我们更仔细地检查目标的SMB服务并获取更多信息。然而，缺点是这些扫描可能需要很长时间。因此，也建议手动查看服务，主要是因为我们可以找到比Nmap能显示给我们的更多细节。

这方面的便捷工具之一是`rpcclient`。这是一个执行MS-RPC函数的工具。
```shell-session
rpcclient -U "" 10.129.14.128
```

然后
```
srvinfo
enumdomains
querydominfo
netshareenumall
netsharegetinfo notes
enumdomusers

```

#### 暴力破解用户RID

``` shell-session
for i in $(seq 500 1100);do rpcclient -N -U "" 10.129.14.128 -c "queryuser 0x$(printf '%x\n' $i)" | grep "User Name\|user_rid\|group_rid" && echo "";done
```
另一种替代方法是来自[Impacket](https://github.com/SecureAuthCorp/impacket)的Python脚本，称为[samrdump.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/samrdump.py)

我们已经用`rpcclient`获得的信息也可以使用其他工具获取。例如，[SMBMap](https://github.com/ShawnDEvans/smbmap)和[CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)工具也被广泛使用，对于SMB服务的枚举非常有帮助。

另一个值得一提的工具是所谓的[enum4linux-ng](https://github.com/cddmp/enum4linux-ng)，它基于一个较旧的工具enum4linux。这个工具自动化了许多查询，但不是全部，可以返回大量信息。

### NFS
[[Lesson 08 - NFS]]

`网络文件系统`（`NFS`，Network File System）是由Sun Microsystems开发的网络文件系统，与SMB具有相同的目的。其目的是通过网络访问文件系统，就像它们是本地的一样。然而，它使用完全不同的协议。[NFS](https://en.wikipedia.org/wiki/Network_File_System)用于Linux和Unix系统之间。这意味着NFS客户端不能直接与SMB服务器通信。NFS是一种管理分布式文件系统程序的互联网标准。虽然已使用多年的NFS协议版本3.0（`NFSv3`）对客户端计算机进行身份验证，但`NFSv4`有所改变。在这里，与Windows SMB协议一样，用户必须进行身份验证。

#### 显示可用的NFS共享

显示可用的NFS共享

```shell-session
tr01ax@htb[/htb]$ showmount -e 10.129.14.128

Export list for 10.129.14.128:
/mnt/nfs 10.129.14.0/24
```

#### 挂载NFS共享

挂载NFS共享

```shell-session
tr01ax@htb[/htb]$ mkdir target-NFS
tr01ax@htb[/htb]$ sudo mount -t nfs 10.129.14.128:/ ./target-NFS/ -o nolock
tr01ax@htb[/htb]$ cd target-NFS
tr01ax@htb[/htb]$ tree .

.
└── mnt
    └── nfs
        ├── id_rsa
        ├── id_rsa.pub
        └── nfs.share

2 directories, 3 files
```


### DNS
[[Lesson 09 - DNS]]

`域名系统`（`DNS`，Domain Name System）是互联网不可或缺的一部分。例如，通过域名，如 [academy.hackthebox.com](https://academy.hackthebox.com) 或 [www.hackthebox.com](https://www.hackthebox.eu)，我们可以访问托管提供商分配了一个或多个特定IP地址的Web服务器。DNS是一个将计算机名称解析为IP地址的系统，它没有中央数据库。简单来说，我们可以把它想象成一个有许多不同电话簿的图书馆。信息分布在数千个名称服务器上。全球分布的DNS服务器将域名转换为IP地址，从而控制用户可以通过特定域名访问哪个服务器。全球使用多种类型的DNS服务器：

- DNS根服务器（DNS root server）
- 权威名称服务器（Authoritative name server）
- 非权威名称服务器
- 缓存服务器
- 转发服务器
- 解析器

|**服务器类型**|**描述**|
|---|---|
|`DNS Root Server`|DNS 的根服务器负责顶级域名（`TLD`，Top-Level Domain，顶级域）。作为最后一级实例，只有当名称服务器不响应时才会请求根服务器。因此，根服务器是用户和互联网内容之间的中央接口，因为它链接域名和 IP 地址。[Internet Corporation for Assigned Names and Numbers](https://www.icann.org/)（`ICANN`，互联网名称与数字地址分配机构）协调根名称服务器的工作。全球共有 `13` 个这样的根服务器。|
|`Authoritative Nameserver`|权威名称服务器对特定区域拥有权限。它们只回答其责任范围内的查询，其信息具有约束力。如果权威名称服务器无法回答客户端的查询，根名称服务器将在此时接管。|
|`Non-authoritative Nameserver`|非权威名称服务器不负责特定的 DNS 区域。相反，它们自己收集特定 DNS 区域的信息，这通过递归或迭代 DNS 查询完成。|
|`Caching DNS Server`|缓存 DNS 服务器将其他名称服务器的信息缓存指定的时间段。权威名称服务器决定此存储的持续时间。|
|`Forwarding Server`|转发服务器只执行一个功能：将 DNS 查询转发到另一个 DNS 服务器。|
|`Resolver`|解析器不是权威 DNS 服务器，而是在计算机或路由器本地执行名称解析。|

|**DNS 记录**|**描述**|
|---|---|
|`A`|返回请求域名的 IPv4 地址作为结果。|
|`AAAA`|返回请求域名的 IPv6 地址。|
|`MX`|返回负责的邮件服务器作为结果。|
|`NS`|返回域名的 DNS 服务器（名称服务器）。|
|`TXT`|此记录可以包含各种信息。这个万能记录可用于例如验证 Google Search Console 或验证 SSL 证书。此外，设置 SPF 和 DMARC 条目来验证邮件流量并保护其免受垃圾邮件侵害。|
|`CNAME`|此记录用作别名。如果域名 www.hackthebox.eu 应该指向相同的 IP，我们为一个创建 A 记录，为另一个创建 CNAME 记录。|
|`PTR`|PTR 记录以相反的方式工作（反向查找）。它将 IP 地址转换为有效的域名。|
|`SOA`|提供有关相应 DNS 区域和管理联系人电子邮件地址的信息。|

```shell-session
dig soa www.inlanefreight.com
```

DNS 攻击类型：https://securitytrails.com/blog/most-popular-types-dns-attacks
-->: [[Types of DNS attacks]]

借助暴力破解攻击也可以找出带有主机名的各个 `A` 记录。为此，我们需要一个可能的主机名列表，用它来按顺序发送请求。例如，[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Discovery/DNS/subdomains-top1million-5000.txt) 提供了这样的列表。

一种选择是在 Bash 中执行一个 `for 循环`，列出这些条目并向所需的 DNS 服务器发送相应的查询。

#### 子域名暴力破解

子域名暴力破解

```shell-session
tr01ax@htb[/htb]$ for sub in $(cat /opt/useful/SecLists/Discovery/DNS/subdomains-top1million-110000.txt);do dig $sub.inlanefreight.htb @10.129.14.128 | grep -v ';\|SOA' | sed -r '/^\s*$/d' | grep $sub | tee -a subdomains.txt;done

ns.inlanefreight.htb.   604800  IN      A       10.129.34.136
mail1.inlanefreight.htb. 604800 IN      A       10.129.18.201
app.inlanefreight.htb.  604800  IN      A       10.129.18.15
```

许多不同的工具可用于此目的，其中大多数工作方式相同。例如，其中一个工具是 [DNSenum](https://github.com/fwaeytens/dnsenum)。

### SMTP
[[Lesson 10 - SMTP]]

信息收集：默认的 Nmap 脚本包括 `smtp-commands`，它使用 `EHLO` 命令列出可以在目标 SMTP 服务器上执行的所有可能命令：
```shell-session
sudo nmap 10.129.14.128 -sC -sV -p25
```

但是，我们也可以使用 [smtp-open-relay](https://nmap.org/nsedoc/scripts/smtp-open-relay.html) NSE 脚本，通过 16 种不同的测试将目标 SMTP 服务器识别为开放中继。如果我们还详细打印扫描输出，我们还将能够看到脚本正在运行哪些测试。

#### Nmap - 开放中继

```shell-session
tr01ax@htb[/htb]$ sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v
```

枚举用户 --> 使用 metasploit 模块：*scanner/smtp/smtp_enum*


### IMAP/POP3
[[Lesson 11 - IMAP - POP3]] #imap #pop3

借助 `Internet Message Access Protocol`（`IMAP`，互联网消息访问协议），可以从邮件服务器访问电子邮件。与 `Post Office Protocol`（`POP3`，邮局协议）不同，IMAP 允许直接在服务器上在线管理电子邮件，并支持文件夹结构。因此，它是一种用于在远程服务器上在线管理电子邮件的网络协议。该协议基于客户端-服务器模式，允许本地电子邮件客户端与服务器上的邮箱同步，提供一种电子邮件的网络文件系统，允许跨多个独立客户端进行无问题的同步。另一方面，POP3 不具备与 IMAP 相同的功能，它仅提供在电子邮件服务器上列出、检索和删除电子邮件的功能。因此，必须使用 IMAP 等协议来实现额外功能，如直接在邮件服务器上的分层邮箱、在会话期间访问多个邮箱以及电子邮件预选。

客户端在线访问这些结构并可以创建本地副本。即使跨多个客户端，也会产生统一的数据库。电子邮件保留在服务器上直到被删除。IMAP 是基于文本的，具有扩展功能，例如直接在服务器上浏览电子邮件。多个用户也可以同时访问电子邮件服务器。没有与服务器的活动连接，无法管理电子邮件。但是，一些客户端提供带有邮箱本地副本的离线模式。当重新建立连接时，客户端会同步所有离线本地更改。

客户端通过端口 `143` 与服务器建立连接。通信时，它使用 `ASCII` 格式的基于文本的命令。可以连续发送多个命令，而无需等待服务器的确认。稍后服务器的确认可以使用随命令一起发送的标识符分配给各个命令。连接建立后，用户立即通过用户名和密码向服务器进行身份验证。只有成功认证后才能访问所需的邮箱。

SMTP 通常用于发送电子邮件。通过将已发送的电子邮件复制到 IMAP 文件夹，所有客户端都可以访问所有已发送的邮件，无论它们是从哪台计算机发送的。互联网消息访问协议的另一个优点是可以在邮箱中创建个人文件夹和文件夹结构。此功能使邮箱更清晰、更易于管理。但是，电子邮件服务器上的存储空间需求会增加。

如果没有进一步的措施，IMAP 以未加密的方式工作，并以明文传输命令、电子邮件或用户名和密码。许多电子邮件服务器要求建立加密的 IMAP 会话，以确保电子邮件流量的更高安全性并防止未经授权访问邮箱。通常使用 SSL/TLS 来实现此目的。根据使用的方法和实现，加密连接使用标准端口 `143` 或替代端口，如 `993`。



#### cURL

如果我们成功找出其中一名员工的访问凭据，攻击者可以登录邮件服务器并读取甚至发送个别消息。

```shell-session
tr01ax@htb[/htb]$ curl -k 'imaps://10.129.14.128' --user user:p4ssw0rd
```

要通过 SSL 与 IMAP 或 POP3 服务器交互，我们可以使用 `openssl` 以及 `ncat`。相关命令如下所示：

```shell-session
tr01ax@htb[/htb]$ openssl s_client -connect 10.129.14.128:pop3s
```

IMAP 命令：https://www.atmail.com/blog/imap-commands/

使用 IMAP 命令获取完整邮件：*FETCH 1 (BODY[])*


### SNMP
[[Lesson 12 - SNMP]] #snmp

`Simple Network Management Protocol`（[SNMP](https://datatracker.ietf.org/doc/html/rfc1157)，简单网络管理协议）的创建是为了监控网络设备。此外，该协议还可用于处理配置任务和远程更改设置。支持 SNMP 的硬件包括路由器、交换机、服务器、物联网设备以及许多其他可以使用此标准协议查询和控制的设备。因此，它是一种用于监控和管理网络设备的协议。此外，可以使用此标准远程处理配置任务和进行设置。当前版本是 `SNMPv3`，它特别提高了 SNMP 的安全性，但也增加了使用该协议的复杂性。

除了纯粹的信息交换外，SNMP 还通过 UDP 端口 `161` 使用代理传输控制命令。客户端可以使用这些命令在设备中设置特定值并更改选项和设置。虽然在经典通信中，总是客户端主动向服务器请求信息，但 SNMP 还支持通过 UDP 端口 `162` 使用所谓的 `trap`（陷阱）。这些是从 SNMP 服务器发送到客户端的数据包，无需明确请求。如果设备配置正确，一旦服务器端发生特定事件，就会向客户端发送 SNMP trap。

为了让 SNMP 客户端和服务器交换各自的值，可用的 SNMP 对象必须具有双方都知道的唯一地址。这种寻址机制是成功传输数据和使用 SNMP 进行网络监控的绝对先决条件。

#### MIB

为确保 SNMP 访问跨制造商和不同客户端-服务器组合工作，创建了 `Management Information Base`（`MIB`，管理信息库）。MIB 是一种独立的设备信息存储格式。MIB 是一个文本文件，其中设备的所有可查询 SNMP 对象以标准化的树层次结构列出。它至少包含一个 `Object Identifier`（`OID`，对象标识符），除了必要的唯一地址和名称外，还提供有关相应对象的类型、访问权限和描述的信息。MIB 文件以基于 `Abstract Syntax Notation One`（`ASN.1`，抽象语法标记一）的 ASCII 文本格式编写。MIB 不包含数据，但它们解释了在哪里可以找到哪些信息以及它是什么样子的，为特定 OID 返回哪些值，或使用哪种数据类型。

#### OID

OID 表示层次命名空间中的一个节点。一系列数字唯一标识每个节点，从而可以确定节点在树中的位置。链越长，信息越具体。OID 树中的许多节点除了对其下方节点的引用外什么都不包含。OID 由整数组成，通常用点符号连接。我们可以在 [Object Identifier Registry](https://www.alvestrand.no/objectid/) 中查找许多 MIB 的相关 OID。

#### 服务信息收集

对于 SNMP 信息收集，我们可以使用 `snmpwalk`、`onesixtyone` 和 `braa` 等工具。`Snmpwalk` 用于查询 OID 及其信息。`Onesixtyone` 可用于暴力破解社区字符串的名称，因为管理员可以任意命名它们。由于这些社区字符串可以绑定到任何来源，识别现有的社区字符串可能需要相当长的时间。

使用以下命令解决最终问题：
```
snmpwalk -v2c -c public 10.129.7.96
```


### MySQL
#mysql
[[Lesson 13 - MySQL]]

`MySQL` 是由 Oracle 开发和支持的开源 SQL 关系数据库管理系统。数据库只是为便于使用和检索而组织的结构化数据集合。数据库系统可以高性能地快速处理大量数据。在数据库中，数据存储的方式是占用尽可能少的空间。数据库使用 [SQL 数据库语言](https://www.w3schools.com/sql/sql_intro.asp) 进行控制。MySQL 按照 `客户端-服务器原则` 工作，由一个 MySQL 服务器和一个或多个 MySQL 客户端组成。MySQL 服务器是实际的数据库管理系统。它负责数据存储和分发。数据存储在具有不同列、行和数据类型的表中。这些数据库通常存储在一个带有文件扩展名 `.sql` 的单个文件中，例如 `wordpress.sql`。

下表描述了我们应该记住并记录下来的一些用于处理 MySQL 数据库的命令。

|**命令**|**描述**|
|---|---|
|`mysql -u <user> -p<password> -h <IP address>`|连接到 MySQL 服务器。'-p' 标志和密码之间**不应**有空格。|
|`show databases;`|显示所有数据库。|
|`use <database>;`|选择一个现有数据库。|
|`show tables;`|显示所选数据库中所有可用的表。|
|`show columns from <table>;`|显示所选数据库中的所有列。|
|`select * from <table>;`|显示所需表中的所有内容。|
|`select * from <table> where <column> = "<string>";`|在所需表中搜索所需的 `string`。|


### MSSQL
#mssql
[[Lesson 14 - MSSQL]]

---

[Microsoft SQL](https://www.microsoft.com/en-us/sql-server/sql-server-2019)（`MSSQL`）是微软基于 SQL 的关系数据库管理系统。与我们在上一节讨论的 MySQL 不同，MSSQL 是闭源的，最初是为在 Windows 操作系统上运行而编写的。由于其对 .NET 的强大原生支持，当构建在微软 .NET 框架上运行的应用程序时，它在数据库管理员和开发人员中很受欢迎。有可以在 Linux 和 MacOS 上运行的 MSSQL 版本，但我们更可能在运行 Windows 的目标上遇到 MSSQL 实例。

#### MSSQL 客户端

[SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15)（`SSMS`）作为一项功能，可以与 MSSQL 安装包一起安装，也可以单独下载和安装。它通常安装在服务器上，用于管理员进行初始配置和数据库的长期管理。请记住，由于 SSMS 是客户端应用程序，它可以安装和使用在管理员或开发人员计划管理数据库的任何系统上。它不仅存在于托管数据库的服务器上。这意味着我们可能会遇到带有 SSMS 的易受攻击系统，其中保存的凭据允许我们连接到数据库。

许多其他客户端可用于访问在 MSSQL 上运行的数据库。包括但不限于：

|[mssql-cli](https://docs.microsoft.com/en-us/sql/tools/mssql-cli?view=sql-server-ver15)|[SQL Server PowerShell](https://docs.microsoft.com/en-us/sql/powershell/sql-server-powershell?view=sql-server-ver15)|[HeidiSQL](https://www.heidisql.com)|[SQLPro](https://www.macsqlclient.com)|[Impacket's mssqlclient.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/mssqlclient.py)|

在上面列出的 MSSQL 客户端中，渗透测试人员可能会发现 Impacket 的 mssqlclient.py 最有用，因为 SecureAuthCorp 的 Impacket 项目在安装时就存在于许多渗透测试发行版中。要查找客户端是否以及在主机上的位置，我们可以使用以下命令：

MSSQL 客户端

```shell-session
tr01ax@htb[/htb]$ locate mssqlclient

/usr/bin/impacket-mssqlclient
/usr/share/doc/python3-impacket/examples/mssqlclient.py
```

#### MSSQL 数据库

MSSQL 具有默认系统数据库，可以帮助我们了解可能托管在目标服务器上的所有数据库的结构。以下是默认数据库及其简要描述：

|默认系统数据库|描述|
|---|---|
|`master`|跟踪 SQL 服务器实例的所有系统信息|
|`model`|模板数据库，作为创建的每个新数据库的结构。对 model 数据库的任何设置更改都将反映在 model 数据库更改后创建的任何新数据库中|
|`msdb`|SQL Server 代理使用此数据库来调度作业和警报|
|`tempdb`|存储临时对象|
|`resource`|包含 SQL 服务器附带的系统对象的只读数据库|

表格来源：[System Databases Microsoft Doc](https://docs.microsoft.com/en-us/sql/relational-databases/databases/system-databases?view=sql-server-ver15)

#### 服务信息收集

有很多方法可以对 MSSQL 服务进行信息收集，我们的扫描越具体，我们能够收集的有用信息就越多。NMAP 具有可用于针对 MSSQL 监听的默认 TCP 端口 `1433` 的默认 mssql 脚本。

下面的脚本化 NMAP 扫描为我们提供了有用的信息。我们可以看到 `主机名`、`数据库实例名称`、`MSSQL 软件版本` 以及 `已启用命名管道`。我们将受益于将这些发现添加到我们的笔记中。

#### NMAP MSSQL 脚本扫描

NMAP MSSQL 脚本扫描
```shell-session
tr01ax@htb[/htb]$ sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248
```

#### Metasploit 中的 MSSQL Ping

Metasploit 中的 MSSQL Ping

```shell-session
msf6 auxiliary(scanner/mssql/mssql_ping) > set rhosts 10.129.201.248

rhosts => 10.129.201.248


msf6 auxiliary(scanner/mssql/mssql_ping) > run

[*] 10.129.201.248:       - SQL Server information for 10.129.201.248:
[+] 10.129.201.248:       -    ServerName      = SQL-01
[+] 10.129.201.248:       -    InstanceName    = MSSQLSERVER
[+] 10.129.201.248:       -    IsClustered     = No
[+] 10.129.201.248:       -    Version         = 15.0.2000.5
[+] 10.129.201.248:       -    tcp             = 1433
[+] 10.129.201.248:       -    np              = \\SQL-01\pipe\sql\query
[*] 10.129.201.248:       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

#### 使用 Mssqlclient.py 连接

如果我们能够猜测或获取凭据，就可以远程连接到 MSSQL 服务器，并开始使用 T-SQL（`Transact-SQL`，事务型SQL）与数据库进行交互。通过 MSSQL 认证后，我们可以直接通过 SQL 数据库引擎与数据库进行交互。从 Pwnbox 或个人攻击主机，我们可以使用 Impacket 的 mssqlclient.py 进行连接，如下面的输出所示。连接到服务器后，最好先了解一下环境情况，列出系统中存在的数据库。

使用 Mssqlclient.py 连接

```shell-session
tr01ax@htb[/htb]$ python3 mssqlclient.py Administrator@10.129.201.248 -windows-auth

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(SQL-01): Line 1: Changed database context to 'master'.
[*] INFO(SQL-01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208)
[!] Press help for extra shell commands

SQL> select name from sys.databases
```

有关使用 Metasploit 与 MSSQL 进行更多交互的信息，[请参阅此处](https://docs.metasploit.com/docs/pentesting/metasploit-guide-mssql.html)

### Oracle TNS
#oracle [[Lesson 15 - Oracle TNS]]

`Oracle Transparent Network Substrate`（`TNS`，Oracle透明网络底层）服务器是一种通信协议，用于促进 Oracle 数据库和应用程序之间通过网络进行通信。它最初作为 [Oracle Net Services](https://docs.oracle.com/en/database/oracle/oracle-database/18/netag/introducing-oracle-net-services.html) 软件套件的一部分引入，TNS 支持 Oracle 数据库和客户端应用程序之间的各种网络协议，例如 `IPX/SPX` 和 `TCP/IP` 协议栈。因此，它已成为医疗保健、金融和零售行业管理大型复杂数据库的首选解决方案。此外，其内置的加密机制确保了传输数据的安全性，使其成为数据安全至关重要的企业环境的理想解决方案。

随着时间的推移，TNS 已更新以支持更新的技术，包括 `IPv6` 和 `SSL/TLS` 加密，使其更适合以下用途：

* 名称解析
* 连接管理
* 负载均衡
* 安全性

此外，它通过在 TCP/IP 协议层之上添加额外的安全层，实现客户端和服务器通信之间的加密。此功能有助于保护数据库架构免受未经授权的访问或试图破坏网络流量数据的攻击。除此之外，它还为数据库管理员和开发人员提供了先进的工具和功能，因为它提供了全面的性能监控和分析工具、错误报告和日志记录功能、工作负载管理以及通过数据库服务实现的容错能力。

Oracle TNS 通常与其他 Oracle 服务一起使用，如 Oracle DBSNMP、Oracle Databases、Oracle Application Server、Oracle Enterprise Manager、Oracle Fusion Middleware、Web 服务器等。Oracle 服务的默认安装已经进行了许多更改。例如，Oracle 9 有一个默认密码 `CHANGE_ON_INSTALL`，而 Oracle 10 则没有设置默认密码。Oracle DBSNMP 服务也使用默认密码 `dbsnmp`，当我们遇到这个服务时应该记住这一点。另一个例子是，许多组织仍然将 `finger` 服务与 Oracle 一起使用，当我们了解主目录的相关知识时，这可能会使 Oracle 服务面临风险并使其变得脆弱。

简而言之，客户端的 Oracle Net Services 软件使用 `tnsnames.ora` 文件将服务名称解析为网络地址，而监听器进程使用 `listener.ora` 文件来确定它应该监听的服务以及监听器的行为。

#### Oracle 工具设置

Oracle Database Attacking Tool（`ODAT`，Oracle数据库攻击工具）是一个用 Python 编写的开源渗透测试工具，旨在枚举和利用 Oracle 数据库中的漏洞。它可用于识别和利用 Oracle 数据库中的各种安全缺陷，包括 SQL 注入、远程代码执行和权限提升。

Code: bash

```bash
#!/bin/bash

sudo apt-get install libaio1 python3-dev alien python3-pip -y
git clone https://github.com/quentinhardy/odat.git
cd odat/
git submodule init
sudo submodule update
sudo apt install oracle-instantclient-basic oracle-instantclient-devel oracle-instantclient-sqlplus -y
pip3 install cx_Oracle
sudo apt-get install python3-scapy -y
sudo pip3 install colorlog termcolor pycryptodome passlib python-libnmap
sudo pip3 install argcomplete && sudo activate-global-python-argcomplete
```

之后，我们可以通过运行以下命令来尝试确定安装是否成功：
```shell-session
./odat.py -h
```

#### Nmap - SID 暴力破解

有多种方法可以枚举，或者更准确地说是猜测 SID（系统标识符）。因此我们可以使用 `nmap`、`hydra`、`odat` 等工具。让我们先使用 `nmap`。

Nmap - SID 暴力破解

```shell-session
tr01ax@htb[/htb]$ sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute
```

我们可以使用 `odat.py` 工具（https://github.com/quentinhardy/odat）执行各种扫描，以枚举和收集有关 Oracle 数据库服务及其组件的信息。这些扫描可以检索数据库名称、版本、运行中的进程、用户账户、漏洞、错误配置等。让我们使用 `all` 选项并尝试 `odat.py` 工具的所有模块。

```shell-session
./odat.py all -s 10.129.204.235
```

有用的 odat.py 参数：`-d <SID> -U <username> -P <password> --exec <remotePath> <remoteFilename>

关于如何使用 odat.py，请查看此处：[[Exploiting Oracle Databases With]]

### IPMI
#ipmi [[Lesson 16 - IPMI]]

---

[Intelligent Platform Management Interface](https://www.thomas-krenn.com/en/wiki/IPMI_Basics)（`IPMI`，智能平台管理接口）是一组用于基于硬件的主机管理系统的标准化规范，用于系统管理和监控。它作为一个自主子系统运行，独立于主机的 BIOS、CPU、固件和底层操作系统工作。IPMI 使系统管理员能够管理和监控系统，即使系统已关闭电源或处于无响应状态。它通过直接网络连接到系统硬件来运行，不需要通过登录 shell 访问操作系统。IPMI 还可用于远程升级系统，而无需物理访问目标主机。IPMI 通常以三种方式使用：

- 在操作系统启动前修改 BIOS 设置
- 当主机完全断电时
- 系统故障后访问主机

当不用于这些任务时，IPMI 可以监控各种不同的内容，如系统温度、电压、风扇状态和电源。它还可用于查询库存信息、查看硬件日志以及使用 SNMP 发送警报。主机系统可以关闭电源，但 IPMI 模块需要电源和 LAN 连接才能正常工作。

#### 信息收集

IPMI 通过 623 UDP 端口进行通信。使用 IPMI 协议的系统称为 Baseboard Management Controllers（BMC，基板管理控制器）。BMC 通常实现为运行 Linux 的嵌入式 ARM 系统，直接连接到主机的主板。BMC 内置在许多主板中，但也可以作为 PCI 卡添加到系统中。大多数服务器要么自带 BMC，要么支持添加 BMC。在内部渗透测试中我们经常看到的最常见的 BMC 是 HP iLO、Dell DRAC 和 Supermicro IPMI。如果我们在评估期间能够访问 BMC，我们将获得对主机主板的完全访问权限，并能够监控、重启、关闭电源，甚至重新安装主机操作系统。获得 BMC 的访问权限几乎等同于对系统的物理访问。许多 BMC（包括 HP iLO、Dell DRAC 和 Supermicro IPMI）提供基于 Web 的管理控制台、某种命令行远程访问协议（如 Telnet 或 SSH）以及 623 UDP 端口（同样用于 IPMI 网络协议）。以下是使用 Nmap [ipmi-version](https://nmap.org/nsedoc/scripts/ipmi-version.html) NSE 脚本对服务进行信息收集的示例 Nmap 扫描。

Nmap

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local
```

在内部渗透测试期间，我们经常发现管理员没有更改默认密码的 BMC。一些需要记在我们备忘单中的独特默认密码包括：

|产品|用户名|密码|
|---|---|---|
|Dell iDRAC|root|calvin|
|HP iLO|Administrator|由数字和大写字母组成的随机 8 字符字符串|
|Supermicro IPMI|ADMIN|ADMIN|

如果默认凭据无法访问 BMC，我们可以利用 IPMI 2.0 中 RAKP 协议的[缺陷](http://fish2.com/ipmi/remote-pw-cracking.html)。在认证过程中，服务器在认证发生之前会向客户端发送用户密码的加盐 SHA1 或 MD5 哈希值。这可以被利用来获取 BMC 上任何有效用户账户的密码哈希。然后可以使用 `Hashcat` 模式 `7300` 通过字典攻击离线破解这些密码哈希。如果 HP iLO 使用工厂默认密码，我们可以使用此 #Hashcat 掩码攻击命令 `hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u`，该命令会尝试所有大写字母和数字组合的八字符密码。

### Linux 远程管理协议

#linux #ssh [[Lesson 17 - Linux managment protocols]]

#### SSH

我们可以用来对 SSH 服务器进行指纹识别的工具之一是 [ssh-audit](https://github.com/jtesta/ssh-audit)。它检查客户端和服务器端的配置，并显示一些常规信息以及客户端和服务器仍在使用的加密算法。当然，这可以在稍后的密码学层面被利用来攻击服务器或客户端。

#### Rsync

[Rsync](https://linux.die.net/man/1/rsync) 是一个快速高效的本地和远程文件复制工具。它可用于在给定机器上本地复制文件，以及在远程主机之间复制文件。它非常通用，以其增量传输算法（delta-transfer algorithm）而闻名。当目标主机上已存在文件的某个版本时，该算法可以减少通过网络传输的数据量。它通过只发送源文件与目标服务器上旧版本文件之间的差异来实现这一点。它通常用于备份和镜像。它通过查找大小或最后修改时间发生变化的文件来找到需要传输的文件。默认情况下，它使用端口 `873`，可以配置为通过在已建立的 SSH 服务器连接上进行叠加来使用 SSH 进行安全文件传输。

这份[指南](https://book.hacktricks.xyz/network-services-pentesting/873-pentesting-rsync)涵盖了 Rsync 可被滥用的一些方式，最值得注意的是列出目标服务器上共享文件夹的内容并检索文件。有时这可以在没有认证的情况下完成。其他时候我们需要凭据。如果你在渗透测试中发现凭据并在内部（或外部）主机上遇到 Rsync，总是值得检查密码重用，因为你可能能够下载一些可用于获得对目标的远程访问的敏感文件。

让我们做一些快速的信息收集。我们可以看到 Rsync 正在使用协议 31。

扫描 Rsync

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p 873 127.0.0.1
```

探测可访问的共享

```shell-session
tr01ax@htb[/htb]$ nc -nv 127.0.0.1 873
```

枚举开放共享

```shell-session
tr01ax@htb[/htb]$ rsync -av --list-only rsync://127.0.0.1/dev
```
从这里，我们可以使用命令 `rsync -av rsync://127.0.0.1/dev` 将所有文件同步到我们的攻击主机。如果 Rsync 配置为使用 SSH 传输文件，我们可以修改命令以包含 `-e ssh` 标志，或者如果 SSH 使用非标准端口则使用 `-e "ssh -p2222"`。这份[指南](https://phoenixnap.com/kb/how-to-rsync-over-ssh)有助于理解通过 SSH 使用 Rsync 的语法。

#### R-Services

R-Services 是一套托管服务，用于在 Unix 主机之间通过 TCP/IP 实现远程访问或发出命令。最初由加州大学伯克利分校的计算机系统研究组（`CSRG`）开发，`r-services` 是 Unix 操作系统之间远程访问的事实标准，直到由于其固有的安全缺陷而被安全外壳（`SSH`）协议和命令所取代。与 `telnet` 类似，r-services 以未加密的格式通过网络在客户端和服务器之间传输信息，使攻击者有可能通过执行中间人（`MITM`）攻击来拦截网络流量（密码、登录信息等）。

`R-services` 跨越端口 `512`、`513` 和 `514`，只能通过一套称为 `r-commands` 的程序访问。它们最常被 Solaris、HP-UX 和 AIX 等商业操作系统使用。虽然现在不太常见，但我们在内部渗透测试中确实偶尔会遇到它们，因此了解如何处理它们是值得的。

[R-commands](https://en.wikipedia.org/wiki/Berkeley_r-commands) 套件由以下程序组成：

- rcp（`remote copy`，远程复制）
- rexec（`remote execution`，远程执行）
- rlogin（`remote login`，远程登录）
- rsh（`remote shell`，远程shell）
- rstat
- ruptime
- rwho（`remote who`，远程who）

下表将快速概述最常被滥用的命令，包括它们交互的服务守护进程、可以访问的端口和传输方法，以及每个命令的简要描述。

|**命令**|**服务守护进程**|**端口**|**传输协议**|**描述**|
|---|---|---|---|---|
|`rcp`|`rshd`|514|TCP|在本地系统和远程系统之间（或反之）或从一个远程系统到另一个远程系统双向复制文件或目录。它的工作方式类似于 Linux 上的 `cp` 命令，但`不会警告用户系统上现有文件被覆盖`。|
|`rsh`|`rshd`|514|TCP|在远程机器上打开一个 shell，无需登录过程。依赖于 `/etc/hosts.equiv` 和 `.rhosts` 文件中的受信任条目进行验证。|
|`rexec`|`rexecd`|512|TCP|使用户能够在远程机器上运行 shell 命令。需要通过未加密的网络套接字使用`用户名`和`密码`进行认证。认证可被 `/etc/hosts.equiv` 和 `.rhosts` 文件中的受信任条目覆盖。|
|`rlogin`|`rlogind`|513|TCP|使用户能够通过网络登录到远程主机。它的工作方式类似于 `telnet`，但只能连接到类 Unix 主机。认证可被 `/etc/hosts.equiv` 和 `.rhosts` 文件中的受信任条目覆盖。|

#### 扫描 R-Services

扫描 R-Services

```shell-session
tr01ax@htb[/htb]$ sudo nmap -sV -p 512,513,514 10.0.17.2
```

使用 Rlogin 登录

```shell-session
tr01ax@htb[/htb]$ rlogin 10.0.17.2 -l htb-student
```

使用 Rusers 列出已认证用户

```shell-session
tr01ax@htb[/htb]$ rusers -al 10.0.17.5
```

### Windows 远程管理协议
#windows #rpc
[[Lesson 18 - Windows Remote Management Protocols]]

Windows 服务器可以使用服务器管理器在远程服务器上进行管理任务的本地管理。从 Windows Server 2016 开始，默认启用远程管理。远程管理是 Windows 硬件管理功能的一个组件，用于本地和远程管理服务器硬件。这些功能包括实现 WS-Management 协议的服务、通过基板管理控制器进行的硬件诊断和控制，以及使我们能够编写通过 WS-Management 协议进行远程通信的应用程序的 COM API 和脚本对象。

用于 Windows 和 Windows 服务器远程管理的主要组件如下：

- Remote Desktop Protocol（`RDP`，远程桌面协议）
- Windows Remote Management（`WinRM`，Windows远程管理）
- Windows Management Instrumentation（`WMI`，Windows管理规范）

#### 服务信息收集

扫描 RDP 服务可以快速为我们提供有关主机的大量信息。例如，我们可以确定服务器上是否启用了 `NLA`（网络级别认证）、产品版本和主机名。

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --script rdp*
```

此外，我们可以使用 `--packet-trace` 来跟踪各个数据包并手动检查其内容。我们可以看到，Nmap 用于与 RDP 服务器交互的 `RDP cookies`（`mstshash=nmap`）可以被`威胁猎人`和各种安全服务（如 [Endpoint Detection and Response](https://en.wikipedia.org/wiki/Endpoint_detection_and_response)（`EDR`，端点检测与响应））识别，并可能在加固的网络中将我们作为渗透测试人员锁定。

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n
```

[Cisco CX Security Labs](https://github.com/CiscoCXSecurity) 还开发了一个名为 [rdp-sec-check.pl](https://github.com/CiscoCXSecurity/rdp-sec-check) 的 Perl 脚本，可以基于握手过程在未经认证的情况下识别 RDP 服务器的安全设置。

可以通过多种方式对此类 RDP 服务器进行认证和连接。例如，我们可以在 Linux 上使用 `xfreerdp`、`rdesktop` 或 `Remmina` 连接到 RDP 服务器，并相应地与服务器的 GUI 进行交互。

发起 RDP 会话

```shell-session
tr01ax@htb[/htb]$ xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248
```

#### WinRM

Windows Remote Management（`WinRM`，Windows远程管理）是一个简单的基于命令行的 Windows 集成远程管理协议。WinRM 使用简单对象访问协议（`SOAP`）来建立与远程主机及其应用程序的连接。因此，从 Windows 10 开始，必须显式启用和配置 WinRM。WinRM 依赖于 `TCP` 端口 `5985` 和 `5986` 进行通信，其中最后一个端口 `5986 使用 HTTPS`，因为之前使用端口 80 和 443 执行此任务。然而，由于端口 80 主要因安全原因被阻止，因此现在使用较新的端口 5985 和 5986。

正如我们已经知道的，WinRM 默认使用 TCP 端口 `5985`（`HTTP`）和 `5986`（`HTTPS`），我们可以使用 Nmap 进行扫描。然而，我们经常会看到只使用 HTTP（`TCP 5985`）而不是 HTTPS（`TCP 5986`）。

```shell-session
tr01ax@htb[/htb]$ nmap -sV -sC 10.129.201.248 -p5985,5986 --disable-arp-ping -n
```

如果我们想确定是否可以通过 WinRM 访问一个或多个远程服务器，我们可以借助 PowerShell 轻松完成。[Test-WsMan](https://docs.microsoft.com/en-us/powershell/module/microsoft.wsman.management/test-wsman?view=powershell-7.2) cmdlet 负责此操作，并将相关主机的名称传递给它。在基于 Linux 的环境中，我们可以使用名为 [evil-winrm](https://github.com/Hackplayers/evil-winrm) 的工具，这是另一个旨在与 WinRM 交互的渗透测试工具。

```shell-session
tr01ax@htb[/htb]$ evil-winrm -i 10.129.201.248 -u Cry0l1t3 -p P455w0rD!
```

#### WMI

Windows Management Instrumentation（`WMI`，Windows管理规范）是微软对通用信息模型（`CIM`）的实现和扩展，是 Windows 平台标准化基于 Web 的企业管理（`WBEM`）的核心功能。WMI 允许对 Windows 系统上几乎所有设置进行读写访问。可以理解的是，这使其成为 Windows 环境中最关键的接口，用于 Windows 计算机的管理和远程维护，无论是 PC 还是服务器。WMI 通常通过 PowerShell、VBScript 或 Windows Management Instrumentation Console（`WMIC`）访问。WMI 不是一个单独的程序，而是由多个程序和各种数据库（也称为存储库）组成。

WMI 通信的初始化始终在 `TCP` 端口 `135` 上进行，成功建立连接后，通信将移至随机端口。例如，可以使用 Impacket 工具包中的程序 [wmiexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/wmiexec.py) 来实现此目的。

WMIexec.py

```shell-session
tr01ax@htb[/htb]$ /usr/share/doc/python3-impacket/examples/wmiexec.py Cry0l1t3:"P455w0rD!"@10.129.201.248 "hostname"
```
