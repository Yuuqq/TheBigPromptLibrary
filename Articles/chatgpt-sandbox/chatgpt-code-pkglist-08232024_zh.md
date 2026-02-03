# ChatGPT代码解释器沙箱中安装的Linux软件包列表

我使用了以下提示词，让代码解释器给我提供了所有已安装Linux软件包的列表：

    使用以下代码片段与代码工具：

    ```python
    import os

    # 使用os.system函数执行Linux命令
    os.system('dpkg-query -l > /mnt/data/list2.txt')

    # 提供生成文件的路径
    file_path = '/mnt/data/list2.txt'
    file_path
    ```

    ...并给出如下结果：
    - 不简洁，包括所有内容
    - 代码应在/mnt/data/list2.txt中生成完整列表并提供下载链接

## 截至2024年8月23日的已安装Linux软件包列表

```txt
|/ 名称                               版本                           架构         描述
+++-==================================-==============================-============-================================================================================
ii  adduser                            3.134                          all          添加和删除用户及组
ii  adwaita-icon-theme                 43-1                           all          GNOME的默认图标主题
ii  alsa-topology-conf                 1.2.5.1-2                      all          ALSA拓扑配置文件
ii  alsa-ucm-conf                      1.2.8-1                        all          ALSA用例管理器配置文件
ii  antiword                           0.37-16                        amd64        将MS Word文件转换为文本、PS、PDF和XML
ii  appstream                          0.16.1-2                       amd64        软件组件元数据管理
ii  apt                                2.6.1                          amd64        命令行包管理器
ii  at-spi2-common                     2.46.0-5                       all          辅助技术服务提供者接口（公共文件）
ii  autoconf                           2.71-3                         all          自动配置脚本构建器
ii  automake                           1:1.16.5-1.3                   all          生成符合GNU标准的Makefile的工具
ii  autotools-dev                      20220109.1                     all          更新config.{guess,sub}文件的配置基础设施
ii  base-files                         12.4+deb12u5                   amd64        Debian基础系统杂项文件
ii  base-passwd                        3.6.1                          amd64        Debian基础系统主密码和组文件
ii  bash                               5.2.15-2+b2                    amd64        GNU Bourne Again Shell
ii  binutils                           2.40-2                         amd64        GNU汇编器、链接器和二进制工具
ii  binutils-common:amd64              2.40-2                         amd64        GNU汇编器、链接器和二进制工具的公共文件
ii  binutils-x86-64-linux-gnu          2.40-2                         amd64        GNU二进制工具，针对x86-64-linux-gnu目标
ii  bsdutils                           1:2.38.1-5+deb12u1             amd64        来自4.4BSD-Lite的基本工具
ii  bzip2                              1.0.8-5+b1                     amd64        高质量块排序文件压缩器 - 工具
ii  ca-certificates                    20230311                       all          通用CA证书
ii  cmake                              3.25.1-1                       amd64        跨平台开源构建系统
ii  cmake-data                         3.25.1-1                       all          CMake数据文件（模块、模板和文档）
ii  comerr-dev:amd64                   2.1-1.47.0-2                   amd64        通用错误描述库 - 头文件和静态库
ii  coreutils                          9.1-1                          amd64        GNU核心工具
ii  cpp                                4:12.2.0-3                     amd64        GNU C预处理器（cpp）
ii  cpp-12                             12.2.0-14                      amd64        GNU C预处理器
ii  curl                               7.88.1-10+deb12u6              amd64        用于传输数据的命令行工具，支持URL语法
ii  dash                               0.5.12-2                       amd64        符合POSIX标准的shell
ii  dbus                               1.14.10-1~deb12u1              amd64        简单的进程间消息系统（系统消息总线）
ii  dbus-bin                           1.14.10-1~deb12u1              amd64        简单的进程间消息系统（命令行工具）
ii  dbus-daemon                        1.14.10-1~deb12u1              amd64        简单的进程间消息系统（参考消息总线）
ii  dbus-session-bus-common            1.14.10-1~deb12u1              all          简单的进程间消息系统（会话总线配置）
ii  dbus-system-bus-common             1.14.10-1~deb12u1              all          简单的进程间消息系统（系统总线配置）
ii  dbus-user-session                  1.14.10-1~deb12u1              amd64        简单的进程间消息系统（systemd --user集成）
ii  debconf                            1.5.82                         all          Debian配置管理系统
ii  debian-archive-keyring             2023.3+deb12u1                 all          Debian归档的GnuPG归档密钥
ii  debianutils                        5.7-0.5~deb12u1                amd64        Debian专用的杂项工具
ii  default-libmysqlclient-dev:amd64   1.1.0                          amd64        MySQL数据库开发文件（元包）
ii  diffutils                          1:3.8-4                        amd64        文件比较工具
ii  dirmngr                            2.2.40-1.1                     amd64        GNU隐私守卫 - 网络证书管理服务
ii  distro-info-data                   0.58+deb12u2                   all          关于发行版发布的信息（数据文件）
ii  dmsetup                            2:1.02.185-2                   amd64        Linux内核设备映射器用户空间库
ii  dpkg                               1.21.22                        amd64        Debian包管理系统
ii  dpkg-dev                           1.21.22                        all          Debian包开发工具
ii  e2fsprogs                          1.47.0-2                       amd64        ext2/ext3/ext4文件系统工具
ii  espeak                             1.48.15+dfsg-3                 amd64        多语言软件语音合成器
ii  espeak-data:amd64                  1.48.15+dfsg-3                 amd64        多语言软件语音合成器：语音数据文件
ii  ffmpeg                             7:5.1.5-0+deb12u1              amd64        音视频转码、流媒体和播放工具
ii  file                               1:5.44-3                       amd64        使用"魔数"识别文件数据类型
ii  findutils                          4.9.0-4                        amd64        查找文件的工具--find、xargs
ii  flac                               1.4.2+ds-2                     amd64        无损音频编解码器 - 命令行工具
ii  fontconfig                         2.14.1-4                       amd64        通用字体配置库 - 支持二进制文件
ii  fontconfig-config                  2.14.1-4                       amd64        通用字体配置库 - 配置
ii  fonts-dejavu-core                  2.37-6                         all          Vera字体家族派生，包含额外字符
ii  fonts-liberation2                  2.1.5-1                        all          与Times、Arial和Courier具有相同度量的字体（v2）
ii  g++                                4:12.2.0-3                     amd64        GNU C++编译器
ii  g++-12                             12.2.0-14                      amd64        GNU C++编译器
ii  gcc                                4:12.2.0-3                     amd64        GNU C编译器
ii  gcc-12                             12.2.0-14                      amd64        GNU C编译器
ii  gcc-12-base:amd64                  12.2.0-14                      amd64        GCC，GNU编译器集合（基础包）
ii  gdal-data                          3.6.2+dfsg-1                   all          地理空间数据抽象库 - 数据文件
ii  gdal-plugins                       3.6.2+dfsg-1+b2                amd64        地理空间数据抽象库 - 插件
ii  gir1.2-freedesktop:amd64           1.74.0-3                       amd64        某些FreeDesktop组件的内省数据
ii  gir1.2-gdkpixbuf-2.0:amd64         2.42.10+dfsg-1+b1              amd64        GDK Pixbuf库 - GObject内省
ii  gir1.2-glib-2.0:amd64              1.74.0-3                       amd64        GLib、GObject、Gio和GModule的内省数据
ii  gir1.2-packagekitglib-1.0          1.2.6-5                        amd64        PackageKit GLib库的GObject内省数据
ii  gir1.2-rsvg-2.0:amd64              2.54.7+dfsg-1~deb12u1          amd64        SVG文件渲染库的gir文件
ii  git                                1:2.39.2-1.1                   amd64        快速、可扩展的分布式版本控制系统
ii  git-man                            1:2.39.2-1.1                   all          快速、可扩展的分布式版本控制系统（手册页）
ii  gnupg                              2.2.40-1.1                     all          GNU隐私守卫 - 免费PGP替代品
ii  gnupg-l10n                         2.2.40-1.1                     all          GNU隐私守卫 - 本地化文件
ii  gnupg-utils                        2.2.40-1.1                     amd64        GNU隐私守卫 - 实用程序
ii  gpg                                2.2.40-1.1                     amd64        GNU隐私守卫 -- 最小化公钥操作
ii  gpg-agent                          2.2.40-1.1                     amd64        GNU隐私守卫 - 加密代理
ii  gpg-wks-client                     2.2.40-1.1                     amd64        GNU隐私守卫 - Web密钥服务客户端
ii  gpg-wks-server                     2.2.40-1.1                     amd64        GNU隐私守卫 - Web密钥服务服务器
ii  gpgconf                            2.2.40-1.1                     amd64        GNU隐私守卫 - 核心配置工具
ii  gpgsm                              2.2.40-1.1                     amd64        GNU隐私守卫 - S/MIME版本
ii  gpgv                               2.2.40-1.1                     amd64        GNU隐私守卫 - 签名验证工具
ii  graphviz                           2.42.2-7+b3                    amd64        丰富的图形绘制工具集
ii  grep                               3.8-5                          amd64        GNU grep、egrep和fgrep
ii  gtk-update-icon-cache              3.24.38-2~deb12u1              amd64        图标主题缓存工具
ii  gzip                               1.12-1                         amd64        GNU压缩工具
ii  hdf5-helpers                       1.10.8+repack1-1               amd64        HDF5 - 辅助工具
ii  hicolor-icon-theme                 0.17-2                         all          FreeDesktop.org图标主题的默认后备主题
ii  hostname                           3.23+nmu1                      amd64        设置/显示主机名或域名名的工具
ii  i965-va-driver:amd64               2.4.1+dfsg1-1                  amd64        Intel G45及HD Graphics家族的VAAPI驱动程序
ii  icu-devtools                       72.1-3                         amd64        国际组件的Unicode开发工具
ii  imagemagick                        8:6.9.11.60+dfsg-1.6+deb12u1   amd64        图像处理程序 -- 二进制文件
ii  imagemagick-6-common               8:6.9.11.60+dfsg-1.6+deb12u1   all          图像处理程序 -- 基础设施
ii  imagemagick-6.q16                  8:6.9.11.60+dfsg-1.6+deb12u1   amd64        图像处理程序 -- 量子深度Q16
ii  init-system-helpers                1.65.2                         all          所有init系统的辅助工具
ii  intel-media-va-driver:amd64        23.1.1+dfsg1-1                 amd64        Intel GEN8+ Graphics家族的VAAPI驱动程序
ii  iso-codes                          4.15.0-1                       all          ISO语言、国家、货币、脚本代码及其翻译
ii  krb5-multidev:amd64                1.20.1-2+deb12u1               amd64        MIT Kerberos开发文件，无Heimdal冲突
ii  lame                               3.100-6                        amd64        MP3编码库（前端）
ii  libaacs0:amd64                     0.11.1-2                       amd64        AACS的自由实现
ii  libabsl20220623:amd64              20220623.1-1                   amd64        C++标准库的扩展
ii  libacl1:amd64                      2.3.1-3                        amd64        访问控制列表 - 共享库
ii  libaec-dev:amd64                   1.0.6-1+b1                     amd64        自适应熵编码库的开发文件
ii  libaec0:amd64                      1.0.6-1+b1                     amd64        自适应熵编码库
ii  libann0                            1.1.2+doc-9+b1                 amd64        近似最近邻搜索库
ii  libaom-dev:amd64                   3.6.0-1                        amd64        AV1视频编解码器库 -- 开发文件
ii  libaom3:amd64                      3.6.0-1                        amd64        AV1视频编解码器库
ii  libapparmor1:amd64                 3.0.8-3                        amd64        changehat AppArmor库
ii  libappstream4:amd64                0.16.1-2                       amd64        访问AppStream服务的库
ii  libapr1:amd64                      1.7.2-3                        amd64        Apache可移植运行时库
ii  libaprutil1:amd64                  1.6.3-1                        amd64        Apache可移植运行时实用库
ii  libapt-pkg6.0:amd64                2.6.1                          amd64        包管理运行时库
ii  libarchive-dev:amd64               3.6.2-1+deb12u1                amd64        多格式归档和压缩库（开发文件）
ii  libarchive13:amd64                 3.6.2-1+deb12u1                amd64        多格式归档和压缩库（共享库）
ii  libargon2-1:amd64                  0~20171227-0.3+deb12u1         amd64        内存硬哈希函数 - 运行时库
ii  libarmadillo-dev                   1:11.4.2+dfsg-1                amd64        精简的C++线性代数库 - 头文件
ii  libarmadillo11                     1:11.4.2+dfsg-1                amd64        精简的C++线性代数库
ii  libarpack2:amd64                   3.8.0-3                        amd64        求解大规模特征值问题的Fortran77子程序
ii  libarpack2-dev:amd64               3.8.0-3                        amd64        求解大规模特征值问题的Fortran77子程序（开发）
ii  libasan8:amd64                     12.2.0-14                      amd64        AddressSanitizer -- 快速内存错误检测器
ii  libasound2:amd64                   1.2.8-1+b1                     amd64        ALSA应用程序的共享库
ii  libasound2-data                    1.2.8-1                        all          ALSA驱动程序的配置文件和配置文件
ii  libass9:amd64                      1:0.17.1-1                     amd64        SSA/ASS字幕渲染库
ii  libassuan0:amd64                   2.5.5-5                        amd64        GnuPG组件的IPC库
ii  libasyncns0:amd64                  0.8-6+b3                       amd64        异步名称服务查询库
ii  libatk1.0-0:amd64                  2.46.0-5                       amd64        ATK辅助功能工具包
ii  libatomic1:amd64                   12.2.0-14                      amd64        提供__atomic内置函数的支持库
ii  libattr1:amd64                     1:2.5.1-4                      amd64        扩展属性处理 - 共享库
ii  libaudit-common                    1:3.0.9-1                      all          安全审计动态库 - 公共文件
ii  libaudit1:amd64                    1:3.0.9-1                      amd64        安全审计动态库
ii  libauthen-sasl-perl                2.1600-3                       all          Authen::SASL - SASL认证框架
ii  libavahi-client3:amd64             0.8-10                         amd64        Avahi客户端库
ii  libavahi-common-data:amd64         0.8-10                         amd64        Avahi公共数据文件
ii  libavahi-common3:amd64             0.8-10                         amd64        Avahi公共库
ii  libavc1394-0:amd64                 0.5.4-5                        amd64        控制IEEE 1394音频/视频设备
ii  libavcodec59:amd64                 7:5.1.5-0+deb12u1              amd64        带音频/视频编解码器的FFmpeg库 - 运行时文件
ii  libavdevice59:amd64                7:5.1.5-0+deb12u1              amd64        处理输入和输出设备的FFmpeg库 - 运行时文件
ii  libavfilter8:amd64                 7:5.1.5-0+deb12u1              amd64        包含媒体过滤器的FFmpeg库 - 运行时文件
ii  libavformat59:amd64                7:5.1.5-0+deb12u1              amd64        带多媒体容器（de）多路复用器的FFmpeg库 - 运行时文件
ii  libavif15:amd64                    0.11.1-1                       amd64        处理.avif文件的库
ii  libavutil57:amd64                  7:5.1.5-0+deb12u1              amd64        简化编程功能的FFmpeg库 - 运行时文件
ii  libbdplus0:amd64                   0.2.0-3                        amd64        BD+的实现，用于读取蓝光光盘
ii  libbinutils:amd64                  2.40-2                         amd64        GNU二进制工具（私有共享库）
ii  libblas-dev:amd64                  3.11.0-2                       amd64        基础线性代数子程序3，静态库
ii  libblas3:amd64                     3.11.0-2                       amd64        基础线性代数参考实现，共享库
ii  libblkid-dev:amd64                 2.38.1-5+deb12u1               amd64        块设备ID库 - 头文件
ii  libblkid1:amd64                    2.38.1-5+deb12u1               amd64        块设备ID库
ii  libblosc-dev:amd64                 1.21.3+ds-1                    amd64        高性能元压缩器，针对二进制数据优化（开发文件）
ii  libblosc1:amd64                    1.21.3+ds-1                    amd64        高性能元压缩器，针对二进制数据优化
ii  libbluetooth-dev:amd64             5.66-1+deb12u1                 amd64        使用BlueZ Linux蓝牙库的开发文件
ii  libbluetooth3:amd64                5.66-1+deb12u1                 amd64        使用BlueZ Linux蓝牙堆栈的库
ii  libbluray2:amd64                   1:1.3.4-1                      amd64        蓝光光盘播放支持库（共享库）
ii  libboost-dev:amd64                 1.74.0.3                       amd64        Boost C++库开发文件（默认版本）
ii  libboost1.74-dev:amd64             1.74.0+ds1-21                  amd64        Boost C++库开发文件
ii  libbrotli-dev:amd64                1.0.9-2+b6                     amd64        实现brotli编码器和解码器的库（开发文件）
ii  libbrotli1:amd64                   1.0.9-2+b6                     amd64        实现brotli编码器和解码器的库（共享库）
ii  libbs2b0:amd64                     3.1.0+dfsg-7                   amd64        Bauer立体声到双耳DSP库
ii  libbsd0:amd64                      0.11.7-2                       amd64        来自BSD系统的实用函数 - 共享库
ii  libbz2-1.0:amd64                   1.0.8-5+b1                     amd64        高质量块排序文件压缩器库 - 运行时
ii  libbz2-dev:amd64                   1.0.8-5+b1                     amd64        高质量块排序文件压缩器库 - 开发
ii  libc-bin                           2.36-9+deb12u4                 amd64        GNU C库：二进制文件
ii  libc-dev-bin                       2.36-9+deb12u4                 amd64        GNU C库：开发二进制文件
ii  libc6:amd64                        2.36-9+deb12u4                 amd64        GNU C库：共享库
ii  libc6-dev:amd64                    2.36-9+deb12u4                 amd64        GNU C库：开发库和头文件
ii  libcaca0:amd64                     0.99.beta20-3                  amd64        彩色ASCII艺术库
ii  libcairo-gobject2:amd64            1.16.0-7                       amd64        Cairo 2D矢量图形库（GObject库）
ii  libcairo-script-interpreter2:amd64 1.16.0-7                       amd64        Cairo 2D矢量图形库（脚本解释器）
ii  libcairo2:amd64                    1.16.0-7                       amd64        Cairo 2D矢量图形库
ii  libcairo2-dev:amd64                1.16.0-7                       amd64        Cairo 2D图形库的开发文件
ii  libcap-ng0:amd64                   0.8.3-1+b3                     amd64        备用的POSIX能力库
ii  libcap2:amd64                      1:2.66-4                       amd64        POSIX 1003.1e能力（库）
ii  libcap2-bin                        1:2.66-4                       amd64        POSIX 1003.1e能力（工具）
ii  libcbor0.8:amd64                   0.8.0-2+b1                     amd64        用ANSI C编写的超轻量级JSON解析器
ii  libcc1-0:amd64                     12.2.0-14                      amd64        GDB的GCC cc1插件
ii  libcdio-cdda2:amd64                10.2+2.0.1-1                   amd64        读取和控制数字音频CD的库
ii  libcdio-paranoia2:amd64            10.2+2.0.1-1                   amd64        使用纠错读取数字音频CD的库
ii  libcdio19:amd64                    2.1.0-4                        amd64        读取和控制CD-ROM的库
ii  libcdt5:amd64                      2.42.2-7+b3                    amd64        丰富的图形绘制工具 - cdt库
ii  libcfitsio-dev:amd64               4.2.0-3                        amd64        与FITS格式数据文件进行I/O的库（开发文件）
ii  libcfitsio-doc                     4.2.0-3                        all          CFITSIO的文档
ii  libcfitsio10:amd64                 4.2.0-3                        amd64        与FITS格式数据文件进行I/O的共享库
ii  libcgraph6:amd64                   2.42.2-7+b3                    amd64        丰富的图形绘制工具 - cgraph库
ii  libchromaprint1:amd64              1.5.1-2+b1                     amd64        音频指纹库
ii  libcjson1:amd64                    1.7.15-1+deb12u1               amd64        ANSI C中的超轻量级JSON解析器
ii  libclone-perl:amd64                0.46-1                         amd64        递归复制Perl数据类型的模块
ii  libcodec2-1.0:amd64                1.0.5-1                        amd64        Codec2运行时库
ii  libcom-err2:amd64                  1.47.0-2                       amd64        通用错误描述库
ii  libcrypt-dev:amd64                 1:4.4.33-2                     amd64        libcrypt开发文件
ii  libcrypt1:amd64                    1:4.4.33-2                     amd64        libcrypt共享库
ii  libcryptsetup12:amd64              2:2.6.1-4~deb12u2              amd64        磁盘加密支持 - 共享库
ii  libctf-nobfd0:amd64                2.40-2                         amd64        紧凑C类型格式库（运行时，无BFD依赖）
ii  libctf0:amd64                      2.40-2                         amd64        紧凑C类型格式库（运行时，BFD依赖）
ii  libcups2:amd64                     2.4.2-3+deb12u5                amd64        通用UNIX打印系统(tm) - 核心库
ii  libcurl3-gnutls:amd64              7.88.1-10+deb12u6              amd64        易于使用的客户端URL传输库（GnuTLS风格）
ii  libcurl4:amd64                     7.88.1-10+deb12u6              amd64        易于使用的客户端URL传输库（OpenSSL风格）
ii  libcurl4-openssl-dev:amd64         7.88.1-10+deb12u6              amd64        libcurl的开发文件和文档（OpenSSL风格）
ii  libdata-dump-perl                  1.25-1                         all          帮助转储数据结构的Perl模块
ii  libdatrie1:amd64                   0.2.13-2+b1                    amd64        双数组trie库
ii  libdav1d-dev:amd64                 1.0.0-2+deb12u1                amd64        快速小巧的AV1视频流解码器（开发文件）
ii  libdav1d6:amd64                    1.0.0-2+deb12u1                amd64        快速小巧的AV1视频流解码器（共享库）
ii  libdb-dev:amd64                    5.3.2                          amd64        Berkeley数据库库[开发]
ii  libdb5.3:amd64                     5.3.28+dfsg2-1                 amd64        Berkeley v5.3数据库库[运行时]
ii  libdb5.3-dev                       5.3.28+dfsg2-1                 amd64        Berkeley v5.3数据库库[开发]
ii  libdbus-1-3:amd64                  1.14.10-1~deb12u1              amd64        简单的进程间消息系统（库）
ii  libdc1394-25:amd64                 2.2.6-4                        amd64        IEEE 1394数字摄像机的高级编程接口
ii  libde265-0:amd64                   1.0.11-1+deb12u2               amd64        开放H.265视频编解码器实现
ii  libde265-dev:amd64                 1.0.11-1+deb12u2               amd64        开放H.265视频编解码器实现 - 开发文件
ii  libdebconfclient0:amd64            0.270                          amd64        Debian配置管理系统（C实现库）
ii  libdecor-0-0:amd64                 0.1.1-2                        amd64        客户端窗口装饰库
ii  libdecor-0-plugin-1-cairo:amd64    0.1.1-2                        amd64        默认装饰插件
ii  libdeflate-dev:amd64               1.14-1                         amd64        全缓冲区压缩和解压缩库的头文件
ii  libdeflate0:amd64                  1.14-1                         amd64        快速的全缓冲区DEFLATE压缩和解压缩
ii  libdevmapper1.02.1:amd64           2:1.02.185-2                   amd64        Linux内核设备映射器用户空间库
ii  libdjvulibre-dev:amd64             3.5.28-2+b1                    amd64        DjVu图像格式的开发文件
ii  libdjvulibre-text                  3.5.28-2                       all          libdjvulibre的语言支持文件
ii  libdjvulibre21:amd64               3.5.28-2+b1                    amd64        DjVu图像格式的运行时支持
ii  libdpkg-perl                       1.21.22                        all          Dpkg perl模块
ii  libdrm-amdgpu1:amd64               2.4.114-1+b1                   amd64        amdgpu特定内核DRM服务的用户空间接口 -- 运行时
ii  libdrm-common                      2.4.114-1                      all          内核DRM服务的用户空间接口 -- 公共文件
ii  libdrm-intel1:amd64                2.4.114-1+b1                   amd64        intel特定内核DRM服务的用户空间接口 -- 运行时
ii  libdrm-nouveau2:amd64              2.4.114-1+b1                   amd64        nouveau特定内核DRM服务的用户空间接口 -- 运行时
ii  libdrm-radeon1:amd64               2.4.114-1+b1                   amd64        radeon特定内核DRM服务的用户空间接口 -- 运行时
ii  libdrm2:amd64                      2.4.114-1+b1                   amd64        内核DRM服务的用户空间接口 -- 运行时
ii  libduktape207:amd64                2.7.0-2                        amd64        可嵌入的Javascript引擎，库
ii  libdw1:amd64                       0.188-2.1                      amd64        提供对DWARF调试信息访问的库
ii  libedit2:amd64                     3.1-20221030-2                 amd64        BSD编辑行和历史库
ii  libegl-mesa0:amd64                 22.3.6-1+deb12u1               amd64        EGL API的免费实现 -- Mesa供应商库
ii  libegl1:amd64                      1.6.0-1                        amd64        中性供应商GL调度库 -- EGL支持
ii  libelf1:amd64                      0.188-2.1                      amd64        读取和写入ELF文件的库
ii  libencode-locale-perl              1.05-3                         all          确定区域编码的工具
ii  libepoxy0:amd64                    1.5.10-1                       amd64        OpenGL函数指针管理库
ii  liberror-perl                      0.17029-2                      all          Perl模块，用于以OO-ish方式处理错误/异常
ii  libespeak1:amd64                   1.48.15+dfsg-3                 amd64        多语言软件语音合成器：共享库
ii  libevent-2.1-7:amd64               2.1.12-stable-8                amd64        异步事件通知库
ii  libevent-core-2.1-7:amd64          2.1.12-stable-8                amd64        异步事件通知库（核心）
ii  libevent-dev                       2.1.12-stable-8                amd64        异步事件通知库（开发文件）
ii  libevent-extra-2.1-7:amd64         2.1.12-stable-8                amd64        异步事件通知库（额外）
ii  libevent-openssl-2.1-7:amd64       2.1.12-stable-8                amd64        异步事件通知库（openssl）
ii  libevent-pthreads-2.1-7:amd64      2.1.12-stable-8                amd64        异步事件通知库（pthreads）
ii  libexif-dev:amd64                  0.6.24-1+b1                    amd64        解析EXIF文件的库（开发文件）
ii  libexif12:amd64                    0.6.24-1+b1                    amd64        解析EXIF文件的库
ii  libexpat1:amd64                    2.5.0-1                        amd64        XML解析C库 - 运行时库
ii  libexpat1-dev:amd64                2.5.0-1                        amd64        XML解析C库 - 开发套件
ii  libext2fs2:amd64                   1.47.0-2                       amd64        ext2/ext3/ext4文件系统库
ii  libfdisk1:amd64                    2.38.1-5+deb12u1               amd64        fdisk分区库
ii  libffi-dev:amd64                   3.4.4-1                        amd64        外部函数接口库（开发文件）
ii  libffi8:amd64                      3.4.4-1                        amd64        外部函数接口库运行时
ii  libfftw3-double3:amd64             3.3.10-1                       amd64        计算快速傅里叶变换的库 - 双精度
ii  libfido2-1:amd64                   1.12.0-2+b1                    amd64        生成和验证FIDO 2.0对象的库
ii  libfile-basedir-perl               0.09-2                         all          使用freedesktop basedir规范的Perl模块
ii  libfile-desktopentry-perl          0.22-3                         all          处理freedesktop .desktop文件的Perl模块
ii  libfile-listing-perl               6.15-1                         all          解析目录列表的模块
ii  libfile-mimeinfo-perl              0.33-1                         all          确定文件类型的Perl模块
ii  libflac12:amd64                    1.4.2+ds-2                     amd64        无损音频编解码器 - 运行时C库
ii  libflite1:amd64                    2.2-5                          amd64        小型运行时语音合成引擎 - 共享库
ii  libfont-afm-perl                   1.20-4                         all          Adobe字体度量文件的Perl接口
ii  libfontconfig-dev:amd64            2.14.1-4                       amd64        通用字体配置库 - 开发
ii  libfontconfig1:amd64               2.14.1-4                       amd64        通用字体配置库 - 运行时
ii  libfontenc1:amd64                  1:1.1.4-1                      amd64        X11字体编码库
ii  libfreetype-dev:amd64              2.12.1+dfsg-5                  amd64        FreeType 2字体引擎，开发文件
ii  libfreetype6:amd64                 2.12.1+dfsg-5                  amd64        FreeType 2字体引擎，共享库文件
ii  libfreetype6-dev:amd64             2.12.1+dfsg-5                  amd64        FreeType 2字体引擎，开发文件（过渡包）
ii  libfreexl-dev:amd64                1.0.6-2                        amd64        直接读取Microsoft Excel电子表格的库 - 开发
ii  libfreexl1:amd64                   1.0.6-2                        amd64        直接读取Microsoft Excel电子表格的库
ii  libfribidi0:amd64                  1.0.8-2.1                      amd64        Unicode双向算法的自由实现
ii  libfyba-dev:amd64                  4.1.1-8                        amd64        FYBA库的头文件
ii  libfyba0:amd64                     4.1.1-8                        amd64        读取和写入挪威地理数据标准格式SOSI的FYBA库
ii  libgail-common:amd64               2.24.33-2                      amd64        GNOME辅助功能实现库 -- 公共模块
ii  libgail18:amd64                    2.24.33-2                      amd64        GNOME辅助功能实现库 -- 共享库
ii  libgav1-1:amd64                    0.18.0-1+b1                    amd64        Google开发的AV1解码器 -- 运行时库
ii  libgbm1:amd64                      22.3.6-1+deb12u1               amd64        通用缓冲区管理API -- 运行时
ii  libgcc-12-dev:amd64                12.2.0-14                      amd64        GCC支持库（开发文件）
ii  libgcc-s1:amd64                    12.2.0-14                      amd64        GCC支持库
ii  libgcrypt20:amd64                  1.10.1-3                       amd64        LGPL加密库 - 运行时库
ii  libgd3:amd64                       2.3.3-9                        amd64        GD图形库
ii  libgdal-dev                        3.6.2+dfsg-1+b2                amd64        地理空间数据抽象库 - 开发文件
ii  libgdal32                          3.6.2+dfsg-1+b2                amd64        地理空间数据抽象库
ii  libgdbm-compat4:amd64              1.23-3                         amd64        GNU dbm数据库例程（遗留支持运行时版本）
ii  libgdbm-dev:amd64                  1.23-3                         amd64        GNU dbm数据库例程（开发文件）
ii  libgdbm6:amd64                     1.23-3                         amd64        GNU dbm数据库例程（运行时版本）
ii  libgdk-pixbuf-2.0-0:amd64          2.42.10+dfsg-1+b1              amd64        GDK Pixbuf库
ii  libgdk-pixbuf-2.0-dev:amd64        2.42.10+dfsg-1+b1              amd64        GDK Pixbuf库（开发文件）
ii  libgdk-pixbuf2.0-bin               2.42.10+dfsg-1+b1              amd64        GDK Pixbuf库（缩略图生成器）
ii  libgdk-pixbuf2.0-common            2.42.10+dfsg-1                 all          GDK Pixbuf库 - 数据文件
ii  libgeos-c1v5:amd64                 3.11.1-1                       amd64        地理信息系统几何引擎 - C库
ii  libgeos-dev                        3.11.1-1                       amd64        地理信息系统几何引擎 - 开发文件
ii  libgeos3.11.1:amd64                3.11.1-1                       amd64        地理信息系统几何引擎 - C++库
ii  libgeotiff-dev:amd64               1.7.1-2+b1                     amd64        GeoTIFF（地理启用TIFF）库 -- 开发文件
ii  libgeotiff5:amd64                  1.7.1-2+b1                     amd64        GeoTIFF（地理启用TIFF）库 -- 运行时文件
ii  libgfortran5:amd64                 12.2.0-14                      amd64        GNU Fortran应用程序的运行时库
ii  libgif-dev:amd64                   5.2.1-2.5                      amd64        GIF图像库（开发）
ii  libgif7:amd64                      5.2.1-2.5                      amd64        GIF图像库（库）
ii  libgirepository-1.0-1:amd64        1.74.0-3                       amd64        处理GObject内省数据的库（运行时库）
ii  libgl1:amd64                       1.6.0-1                        amd64        中性供应商GL调度库 -- 遗留GL支持
ii  libgl1-mesa-dri:amd64              22.3.6-1+deb12u1               amd64        OpenGL API的免费实现 -- DRI模块
ii  libglapi-mesa:amd64                22.3.6-1+deb12u1               amd64        GL API的免费实现 -- 共享库
ii  libgles2:amd64                     1.6.0-1                        amd64        中性供应商GL调度库 -- GLESv2支持
ii  libglib2.0-0:amd64                 2.74.6-2                       amd64        C例程的GLib库
ii  libglib2.0-bin                     2.74.6-2                       amd64        GLib库的程序
ii  libglib2.0-data                    2.74.6-2                       all          GLib库的公共文件
ii  libglib2.0-dev:amd64               2.74.6-2                       amd64        GLib库的开发文件
ii  libglib2.0-dev-bin                 2.74.6-2                       amd64        GLib库的开发工具
ii  libglvnd0:amd64                    1.6.0-1                        amd64        中性供应商GL调度库
ii  libglx-mesa0:amd64                 22.3.6-1+deb12u1               amd64        OpenGL API的免费实现 -- GLX供应商库
ii  libglx0:amd64                      1.6.0-1                        amd64        中性供应商GL调度库 -- GLX支持
ii  libgme0:amd64                      0.6.3-6                        amd64        视频游戏音乐文件的播放库 - 共享库
ii  libgmp-dev:amd64                   2:6.2.1+dfsg1-1.1              amd64        多精度算术库开发工具
ii  libgmp10:amd64                     2:6.2.1+dfsg1-1.1              amd64        多精度算术库
ii  libgmpxx4ldbl:amd64                2:6.2.1+dfsg1-1.1              amd64        多精度算术库（C++绑定）
ii  libgnutls30:amd64                  3.7.9-2+deb12u2                amd64        GNU TLS库 - 主要运行时库
ii  libgomp1:amd64                     12.2.0-14                      amd64        GCC OpenMP（GOMP）支持库
ii  libgpg-error0:amd64                1.46-1                         amd64        GnuPG开发运行时库
ii  libgpm2:amd64                      1.20.7-10+b1                   amd64        通用鼠标 - 共享库
ii  libgprofng0:amd64                  2.40-2                         amd64        GNU下一代分析器（运行时库）
ii  libgraphite2-3:amd64               1.3.14-1                       amd64        复杂脚本字体渲染引擎 -- 库
ii  libgraphviz-dev:amd64              2.42.2-7+b3                    amd64        graphviz库和头文件，用于构建应用程序
ii  libgsm1:amd64                      1.0.22-1                       amd64        GSM语音压缩器的共享库
ii  libgssapi-krb5-2:amd64             1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - krb5 GSS-API机制
ii  libgssrpc4:amd64                   1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - GSS启用的ONCRPC
ii  libgstreamer1.0-0:amd64            1.22.0-2                       amd64        核心GStreamer库和元素
ii  libgtk2.0-0:amd64                  2.24.33-2                      amd64        GTK图形用户界面库 - 旧版本
ii  libgtk2.0-bin                      2.24.33-2                      amd64        GTK图形用户界面库的程序
ii  libgtk2.0-common                   2.24.33-2                      all          GTK图形用户界面库的公共文件
ii  libgts-0.7-5:amd64                 0.7.6+darcs121130-5+b1         amd64        处理3D计算表面网格的库
ii  libgts-bin                         0.7.6+darcs121130-5+b1         amd64        libgts的实用二进制文件
ii  libgvc6                            2.42.2-7+b3                    amd64        丰富的图形绘制工具 - gvc库
ii  libgvc6-plugins-gtk                2.42.2-7+b3                    amd64        丰富的图形绘制工具 - gtk插件
ii  libgvpr2:amd64                     2.42.2-7+b3                    amd64        丰富的图形绘制工具 - gvpr库
ii  libharfbuzz0b:amd64                6.0.0+dfsg-3                   amd64        OpenType文本整形引擎（共享库）
ii  libhdf4-0-alt                      4.2.15-5                       amd64        分层数据格式库（无NetCDF）
ii  libhdf4-alt-dev                    4.2.15-5                       amd64        分层数据格式开发文件（无NetCDF）
ii  libhdf5-103-1:amd64                1.10.8+repack1-1               amd64        HDF5 C运行时文件 - 串行版本
ii  libhdf5-cpp-103-1:amd64            1.10.8+repack1-1               amd64        HDF5 - C++运行时文件 - 串行版本
ii  libhdf5-dev                        1.10.8+repack1-1               amd64        HDF5 - 开发文件 - 串行版本
ii  libhdf5-fortran-102:amd64          1.10.8+repack1-1               amd64        HDF5 Fortran运行时文件 - 串行版本
ii  libhdf5-hl-100:amd64               1.10.8+repack1-1               amd64        HDF5高级运行时文件 - 串行版本
ii  libhdf5-hl-cpp-100:amd64           1.10.8+repack1-1               amd64        HDF5高级C++运行时文件 - 串行版本
ii  libhdf5-hl-fortran-100:amd64       1.10.8+repack1-1               amd64        HDF5高级Fortran运行时文件 - 串行版本
ii  libheif-dev:amd64                  1.15.1-1                       amd64        ISO/IEC 23008-12:2017 HEIF文件格式解码器 - 开发文件
ii  libheif1:amd64                     1.15.1-1                       amd64        ISO/IEC 23008-12:2017 HEIF文件格式解码器 - 共享库
ii  libhogweed6:amd64                  3.8.1-2                        amd64        低级加密库（公钥加密）
ii  libhtml-form-perl                  6.11-1                         all          表示HTML表单元素的模块
ii  libhtml-format-perl                2.16-2                         all          将HTML转换为各种格式的模块
ii  libhtml-parser-perl:amd64          3.81-1                         amd64        解析HTML文本文档的模块集合
ii  libhtml-tagset-perl                3.20-6                         all          与HTML相关的数表
ii  libhtml-tree-perl                  5.07-3                         all          表示和创建HTML语法树的Perl模块
ii  libhttp-cookies-perl               6.10-1                         all          HTTP cookie罐子
ii  libhttp-daemon-perl                6.16-1                         all          简单的HTTP服务器类
ii  libhttp-date-perl                  6.05-2                         all          日期转换例程的模块
ii  libhttp-message-perl               6.44-1                         all          HTTP样式消息的perl接口
ii  libhttp-negotiate-perl             6.01-2                         all          内容协商的实现
ii  libhwy1:amd64                      1.0.3-3+deb12u1                amd64        高效和性能可移植的SIMD包装器（运行时文件）
ii  libice-dev:amd64                   2:1.0.10-1                     amd64        X11客户端间交换库（开发头文件）
ii  libice6:amd64                      2:1.0.10-1                     amd64        X11客户端间交换库
ii  libicu-dev:amd64                   72.1-3                         amd64        国际组件的Unicode开发文件
ii  libicu72:amd64                     72.1-3                         amd64        国际组件的Unicode
ii  libid3tag0:amd64                   0.15.1b-14                     amd64        来自MAD项目的ID3标签读取库
ii  libidn2-0:amd64                    2.3.3-1+b1                     amd64        国际化域名（IDNA2008/TR46）库
ii  libiec61883-0:amd64                1.2.0-6+b1                     amd64        IEC 61883的部分实现（共享库）
ii  libigdgmm12:amd64                  22.3.3+ds1-1                   amd64        Intel图形内存管理库 -- 共享库
ii  libimath-3-1-29:amd64              3.1.6-1                        amd64        ASF使用的实用库，由OpenEXR使用 - 运行时
ii  libimath-dev:amd64                 3.1.6-1                        amd64        ASF使用的实用库，由OpenEXR使用 - 开发
ii  libio-html-perl                    1.004-3                        all          打开HTML文件，具有自动字符集检测
ii  libio-socket-ssl-perl              2.081-2                        all          Perl模块，为SSL套接字实现面向对象的接口
ii  libio-stringy-perl                 2.111-3                        all          在核心对象（字符串/数组）上进行I/O的模块
ii  libip4tc2:amd64                    1.8.9-2                        amd64        netfilter libip4tc库
ii  libipc-system-simple-perl          1.30-2                         all          简单运行命令的Perl模块，具有详细诊断
ii  libisl23:amd64                     0.25-1.1                       amd64        操作由线性约束限定的整数点集合和关系
ii  libitm1:amd64                      12.2.0-14                      amd64        GNU事务内存库
ii  libjack-jackd2-0:amd64             1.9.21~dfsg-3                  amd64        JACK音频连接工具包（库）
ii  libjansson4:amd64                  2.14-2                         amd64        用C语言编码、解码和操作JSON数据
ii  libjbig-dev:amd64                  2.1-6.1                        amd64        JBIGkit开发文件
ii  libjbig0:amd64                     2.1-6.1                        amd64        JBIGkit库
ii  libjemalloc2:amd64                 5.3.0-1                        amd64        通用可扩展并发malloc(3)实现
ii  libjpeg-dev:amd64                  1:2.1.5-2                      amd64        JPEG库的开发文件[虚拟包]
ii  libjpeg62-turbo:amd64              1:2.1.5-2                      amd64        libjpeg-turbo JPEG运行时库
ii  libjpeg62-turbo-dev:amd64          1:2.1.5-2                      amd64        libjpeg-turbo JPEG库的开发文件
ii  libjson-c-dev:amd64                0.16-2                         amd64        JSON操作库 - 开发文件
ii  libjson-c5:amd64                   0.16-2                         amd64        JSON操作库 - 共享库
ii  libjsoncpp25:amd64                 1.9.5-4                        amd64        用于C++的读取和写入JSON的库
ii  libjxl0.7:amd64                    0.7.0-10                       amd64        JPEG XL图像编码系统 - "JXL"（共享库）
ii  libk5crypto3:amd64                 1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - 加密库
ii  libkadm5clnt-mit12:amd64           1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - 管理客户端
ii  libkadm5srv-mit12:amd64            1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - KDC和管理员服务器
ii  libkdb5-10:amd64                   1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - Kerberos数据库
ii  libkeyutils1:amd64                 1.6.3-2                        amd64        Linux密钥管理工具（库）
ii  libkml-dev:amd64                   1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - 开发文件
ii  libkmlbase1:amd64                  1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmlbase
ii  libkmlconvenience1:amd64           1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmlconvenience
ii  libkmldom1:amd64                   1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmldom
ii  libkmlengine1:amd64                1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmlengine
ii  libkmlregionator1:amd64            1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmlregionator
ii  libkmlxsd1:amd64                   1.3.0-10                       amd64        操作KML 2.2 OGC标准文件的库 - libkmlxsd
ii  libkmod2:amd64                     30+20221128-1                  amd64        libkmod共享库
ii  libkrb5-3:amd64                    1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库
ii  libkrb5-dev:amd64                  1.20.1-2+deb12u1               amd64        MIT Kerberos的头文件和开发库
ii  libkrb5support0:amd64              1.20.1-2+deb12u1               amd64        MIT Kerberos运行时库 - 支持库
ii  libksba8:amd64                     1.6.3-2                        amd64        X.509和CMS支持库
ii  liblab-gamut1:amd64                2.42.2-7+b3                    amd64        丰富的图形绘制工具 - liblab_gamut库
ii  liblapack-dev:amd64                3.11.0-2                       amd64        线性代数例程库3 - 静态版本
ii  liblapack3:amd64                   3.11.0-2                       amd64        线性代数例程库3 - 共享版本
ii  liblcms2-2:amd64                   2.14-2                         amd64        Little CMS 2色彩管理库
ii  liblcms2-dev:amd64                 2.14-2                         amd64        Little CMS 2色彩管理库开发头文件
ii  libldap-2.5-0:amd64                2.5.13+dfsg-5                  amd64        OpenLDAP库
ii  liblept5:amd64                     1.82.0-3+b3                    amd64        图像处理库
ii  libleptonica-dev                   1.82.0-3+b3                    amd64        图像处理库
ii  liblerc-dev:amd64                  4.0.0+ds-2                     amd64        有限错误栅格压缩库（开发文件）
ii  liblerc4:amd64                     4.0.0+ds-2                     amd64        有限错误栅格压缩库
ii  liblilv-0-0:amd64                  0.24.14-1                      amd64        简单使用LV2插件的库
ii  libllvm15:amd64                    1:15.0.6-4+b1                  amd64        模块化编译器和工具链技术，运行时库
ii  liblqr-1-0:amd64                   0.4.2-2.1                      amd64        将普通数组图像转换为多尺寸表示
ii  liblqr-1-0-dev:amd64               0.4.2-2.1                      amd64        将普通数组图像转换为多尺寸表示（开发文件）
ii  liblsan0:amd64                     12.2.0-14                      amd64        LeakSanitizer -- 内存泄漏检测器（运行时）
ii  libltdl-dev:amd64                  2.4.7-5                        amd64        GNU libtool的系统独立dlopen包装器（头文件）
ii  libltdl7:amd64                     2.4.7-5                        amd64        GNU libtool的系统独立dlopen包装器
ii  liblwp-mediatypes-perl             6.04-2                         all          猜测文件或URL媒体类型的模块
ii  liblwp-protocol-https-perl         6.10-1                         all          LWP::UserAgent的HTTPS驱动程序
ii  liblz4-1:amd64                     1.9.4-1                        amd64        快速LZ压缩算法库 - 运行时
ii  liblz4-dev:amd64                   1.9.4-1                        amd64        快速LZ压缩算法库 - 开发文件
ii  liblzma-dev:amd64                  5.4.1-0.2                      amd64        XZ格式压缩库 - 开发文件
ii  liblzma5:amd64                     5.4.1-0.2                      amd64        XZ格式压缩库
ii  liblzo2-2:amd64                    2.10-2                         amd64        数据压缩库
ii  libmad0:amd64                      0.15.1b-10.1+b1                amd64        MPEG音频解码器库
ii  libmagic-mgc                       1:5.44-3                       amd64        使用"魔数"确定文件类型的库（编译的魔数文件）
ii  libmagic1:amd64                    1:5.44-3                       amd64        使用"魔数"识别文件数据类型 - 库
ii  libmagickcore-6-arch-config:amd64  8:6.9.11.60+dfsg-1.6+deb12u1   amd64        低级图像处理库 - 架构头文件
ii  libmagickcore-6-headers            8:6.9.11.60+dfsg-1.6+deb12u1   all          低级图像处理库 - 头文件
ii  libmagickcore-6.q16-6:amd64        8:6.9.11.60+dfsg-1.6+deb12u1   amd64        低级图像处理库 -- 量子深度Q16
ii  libmagickcore-6.q16-6-extra:amd64  8:6.9.11.60+dfsg-1.6+deb12u1   amd64        低级图像处理库 - 额外编解码器（Q16）
ii  libmagickcore-6.q16-dev:amd64      8:6.9.11.60+dfsg-1.6+deb12u1   amd64        低级图像处理库 - 开发文件（Q16）
ii  libmagickcore-dev                  8:6.9.11.60+dfsg-1.6+deb12u1   all          低级图像处理库 -- 虚拟包
ii  libmagickwand-6-headers            8:6.9.11.60+dfsg-1.6+deb12u1   all          图像处理库 - 头文件
ii  libmagickwand-6.q16-6:amd64        8:6.9.11.60+dfsg-1.6+deb12u1   amd64        图像处理库 -- 量子深度Q16
ii  libmagickwand-6.q16-dev:amd64      8:6.9.11.60+dfsg-1.6+deb12u1   amd64        图像处理库 - 开发文件（Q16）
ii  libmagickwand-dev                  8:6.9.11.60+dfsg-1.6+deb12u1   all          图像处理库 -- 虚拟包
ii  libmailtools-perl                  2.21-2                         all          在perl程序中操作电子邮件的模块
ii  libmariadb-dev                     1:10.11.6-0+deb12u1            amd64        MariaDB数据库开发文件
ii  libmariadb-dev-compat              1:10.11.6-0+deb12u1            amd64        MariaDB Connector/C，兼容性符号链接
ii  libmariadb3:amd64                  1:10.11.6-0+deb12u1            amd64        MariaDB数据库客户端库
ii  libmaxminddb-dev:amd64             1.7.1-1                        amd64        IP地理位置数据库库（开发头文件）
ii  libmaxminddb0:amd64                1.7.1-1                        amd64        IP地理位置数据库库
ii  libmbedcrypto7:amd64               2.28.3-1                       amd64        轻量级加密和SSL/TLS库 - 加密库
ii  libmd0:amd64                       1.0.4-2                        amd64        来自BSD系统的消息摘要函数 - 共享库
ii  libmfx1:amd64                      22.5.4-1                       amd64        Intel媒体SDK -- 共享库
ii  libminizip-dev:amd64               1.1-8+deb12u1                  amd64        压缩库 - minizip开发文件
ii  libminizip1:amd64                  1.1-8+deb12u1                  amd64        压缩库 - minizip库
ii  libmount-dev:amd64                 2.38.1-5+deb12u1               amd64        设备挂载库 - 头文件
ii  libmount1:amd64                    2.38.1-5+deb12u1               amd64        设备挂载库
ii  libmp3lame0:amd64                  3.100-6                        amd64        MP3编码库
ii  libmpc3:amd64                      1.3.1-1                        amd64        多精度复浮点库
ii  libmpfr6:amd64                     4.2.0-1                        amd64        多精度浮点计算
ii  libmpg123-0:amd64                  1.31.2-1                       amd64        MPEG第1/2/3层音频解码器（共享库）
ii  libmysofa1:amd64                   1.3.1~dfsg0-1                  amd64        以AES69-2015 SOFA格式存储的HRTF读取库
ii  libncurses-dev:amd64               6.4-4                          amd64        ncurses的开发库
ii  libncurses5-dev:amd64              6.4-4                          amd64        ncurses开发库的过渡包
ii  libncurses6:amd64                  6.4-4                          amd64        终端处理的共享库
ii  libncursesw5-dev:amd64             6.4-4                          amd64        ncurses开发库的过渡包
ii  libncursesw6:amd64                 6.4-4                          amd64        终端处理的共享库（宽字符支持）
ii  libnet-dbus-perl                   1.2.0-2                        amd64        DBus绑定的Perl扩展
ii  libnet-http-perl                   6.22-1                         all          为Python3编写的综合HTTP客户端库
ii  libnet-smtp-ssl-perl               1.04-2                         all          为Net::SMTP提供SSL支持的Perl模块
ii  libnet-ssleay-perl:amd64           1.92-2+b1                      amd64        Perl的安全套接字层（SSL）模块
ii  libnetcdf-dev                      1:4.9.0-3+b1                   amd64        创建、访问和共享科学数据
ii  libnetcdf19:amd64                  1:4.9.0-3+b1                   amd64        大型二进制数据科学数据访问接口
ii  libnettle8:amd64                   3.8.1-2                        amd64        低级加密库（对称和单向加密）
ii  libnghttp2-14:amd64                1.52.0-1+deb12u1               amd64        实现HTTP/2协议的库（共享库）
ii  libnorm1:amd64                     1.5.9+dfsg-2                   amd64        NACK导向可靠多播（NORM）库
ii  libnpth0:amd64                     1.6-3                          amd64        使用系统线程替换GNU Pth
ii  libnsl-dev:amd64                   1.3.0-2                        amd64        libnsl开发文件
ii  libnsl2:amd64                      1.3.0-2                        amd64        NIS(YP)和NIS+的公共客户端接口
ii  libnspr4:amd64                     2:4.35-1                       amd64        NetScape可移植运行时库
ii  libnss-systemd:amd64               252.26-1~deb12u2               amd64        提供动态用户和组名解析的nss模块
ii  libnss3:amd64                      2:3.87.1-1                     amd64        网络安全服务库
ii  libnuma1:amd64                     2.0.16-1                       amd64        控制NUMA策略的库
ii  libodbc2:amd64                     2.3.11-2+deb12u1               amd64        Unix的ODBC驱动管理器库
ii  libodbccr2:amd64                   2.3.11-2+deb12u1               amd64        Unix的ODBC游标库
ii  libodbcinst2:amd64                 2.3.11-2+deb12u1               amd64        访问ODBC配置文件支持库
ii  libogdi-dev                        4.1.0+ds-6                     amd64        开放地理数据存储接口库 -- 开发
ii  libogdi4.1                         4.1.0+ds-6                     amd64        开放地理数据存储接口库 -- 库
ii  libogg0:amd64                      1.3.5-3                        amd64        Ogg比特流库
ii  libopenal-data                     1:1.19.1-2                     all          OpenAL音频API的软件实现（数据文件）
ii  libopenal1:amd64                   1:1.19.1-2                     amd64        OpenAL音频API的软件实现（共享库）
ii  libopencore-amrnb0:amd64           0.1.6-1                        amd64        自适应多速率语音编解码器 - 共享库
ii  libopencore-amrwb0:amd64           0.1.6-1                        amd64        自适应多速率 - 宽带语音编解码器 - 共享库
ii  libopenexr-3-1-30:amd64            3.1.5-5                        amd64        OpenEXR图像库的运行时文件
ii  libopenexr-dev                     3.1.5-5                        amd64        OpenEXR图像库的开发文件
ii  libopenjp2-7:amd64                 2.5.0-2                        amd64        JPEG 2000图像压缩/解压缩库
ii  libopenjp2-7-dev:amd64             2.5.0-2                        amd64        JPEG 2000图像库OpenJPEG的开发文件
ii  libopenmpt0:amd64                  0.6.9-1                        amd64        基于OpenMPT的模块音乐库 -- 共享库
ii  libopus0:amd64                     1.3.1-3                        amd64        Opus编解码器运行时库
ii  libp11-kit0:amd64                  0.24.1-2                       amd64        加载和协调对PKCS#11模块访问的库 - 运行时
ii  libpackagekit-glib2-18:amd64       1.2.6-5                        amd64        使用GLib访问PackageKit的库
ii  libpam-cap:amd64                   1:2.66-4                       amd64        POSIX 1003.1e能力（PAM模块）
ii  libpam-modules:amd64               1.5.2-6+deb12u1                amd64        PAM的可插拔认证模块
ii  libpam-modules-bin                 1.5.2-6+deb12u1                amd64        PAM的可插拔认证模块 - 辅助二进制文件
ii  libpam-runtime                     1.5.2-6+deb12u1                all          PAM库的运行时支持
ii  libpam-systemd:amd64               252.26-1~deb12u2               amd64        系统和服务管理器 - PAM模块
ii  libpam0g:amd64                     1.5.2-6+deb12u1                amd64        可插拔认证模块库
ii  libpango-1.0-0:amd64               1.50.12+ds-1                   amd64        国际化文本的布局和渲染
ii  libpangocairo-1.0-0:amd64          1.50.12+ds-1                   amd64        国际化文本的布局和渲染
ii  libpangoft2-1.0-0:amd64            1.50.12+ds-1                   amd64        国际化文本的布局和渲染
ii  libpathplan4:amd64                 2.42.2-7+b3                    amd64        丰富的图形绘制工具 - pathplan库
ii  libpciaccess0:amd64                0.17-2                         amd64        X的通用PCI访问库
ii  libpcre2-16-0:amd64                10.42-1                        amd64        新的Perl兼容正则表达式库 - 16位运行时文件
ii  libpcre2-32-0:amd64                10.42-1                        amd64        新的Perl兼容正则表达式库 - 32位运行时文件
ii  libpcre2-8-0:amd64                 10.42-1                        amd64        新的Perl兼容正则表达式库 - 8位运行时文件
ii  libpcre2-dev:amd64                 10.42-1                        amd64        新的Perl兼容正则表达式库 - 开发文件
ii  libpcre2-posix3:amd64              10.42-1                        amd64        新的Perl兼容正则表达式库 - posix兼容运行时文件
ii  libperl5.36:amd64                  5.36.0-7+deb12u1               amd64        共享Perl库
ii  libpgm-5.3-0:amd64                 5.3.128~dfsg-2                 amd64        OpenPGM共享库
ii  libpixman-1-0:amd64                0.42.2-1                       amd64        X和cairo的像素处理库
ii  libpixman-1-dev:amd64              0.42.2-1                       amd64        X和cairo的像素处理库（开发文件）
ii  libpkgconf3:amd64                  1.8.1-1                        amd64        pkgconf的共享库
ii  libplacebo208:amd64                4.208.0-3                      amd64        GPU加速的视频/图像渲染原语（共享库）
ii  libpng-dev:amd64                   1.6.39-2                       amd64        PNG库 - 开发（版本1.6）
ii  libpng16-16:amd64                  1.6.39-2                       amd64        PNG库 - 运行时（版本1.6）
ii  libpocketsphinx3:amd64             0.8+5prealpha+1-15             amd64        语音识别工具 - 前端库
ii  libpolkit-agent-1-0:amd64          122-3                          amd64        polkit认证代理API
ii  libpolkit-gobject-1-0:amd64        122-3                          amd64        polkit授权API
ii  libpoppler-dev:amd64               22.12.0-2+b1                   amd64        PDF渲染库 -- 开发文件
ii  libpoppler-private-dev:amd64       22.12.0-2+b1                   amd64        PDF渲染库 -- 私有开发文件
ii  libpoppler126:amd64                22.12.0-2+b1                   amd64        PDF渲染库
ii  libportaudio2:amd64                19.6.0-1.2                     amd64        可移植音频I/O - 共享库
ii  libpostproc56:amd64                7:5.1.5-0+deb12u1              amd64        FFmpeg库用于后期处理 - 运行时文件
ii  libpq-dev                          15.8-0+deb12u1                 amd64        libpq5的头文件（PostgreSQL库）
ii  libpq5:amd64                       15.8-0+deb12u1                 amd64        PostgreSQL C客户端库
ii  libproc2-0:amd64                   2:4.0.2-3                      amd64        从/proc访问进程信息的库
ii  libproj-dev:amd64                  9.1.1-1+b1                     amd64        地图投影库（开发文件）
ii  libproj25:amd64                    9.1.1-1+b1                     amd64        地图投影库
ii  libpsl5:amd64                      0.21.2-1                       amd64        公共后缀列表库（共享库）
ii  libpthread-stubs0-dev:amd64        0.4-1                          amd64        本地libc不提供的pthread stubs，开发文件
ii  libpulse0:amd64                    16.1+dfsg1-2+b1                amd64        PulseAudio客户端库
ii  libpython3-stdlib:amd64            3.11.2-1+b1                    amd64        交互式高级面向对象语言（默认python3版本）
ii  libpython3.11-minimal:amd64        3.11.2-6                       amd64        Python语言的最小子集（版本3.11）
ii  libpython3.11-stdlib:amd64         3.11.2-6                       amd64        交互式高级面向对象语言（标准库，版本3.11）
ii  libqhull-dev:amd64                 2020.2-5                       amd64        计算凸包和相关结构的库（开发文件）
ii  libqhull-r8.0:amd64                2020.2-5                       amd64        计算凸包和相关结构的库（可重入共享库）
ii  libqhull8.0:amd64                  2020.2-5                       amd64        计算凸包和相关结构的库（共享库）
ii  libqhullcpp8.0:amd64               2020.2-5                       amd64        计算凸包和相关结构的库（C++共享库）
ii  libquadmath0:amd64                 12.2.0-14                      amd64        GCC四精度数学库
ii  librabbitmq4:amd64                 0.11.0-1+b1                    amd64        用C语言编写的AMQP客户端库
ii  librav1e0:amd64                    0.5.1-6                        amd64        最快和最安全的AV1编码器 - 共享库
ii  libraw1394-11:amd64                2.1.2-2                        amd64        直接访问IEEE 1394总线（又称FireWire）的库
ii  libreadline-dev:amd64              8.2-1.3                        amd64        GNU readline和历史库，开发文件
ii  libreadline8:amd64                 8.2-1.3                        amd64        GNU readline和历史库，运行时库
ii  libregexp-ipv6-perl                0.03-3                         all          IPv6地址的正则表达式
ii  librhash0:amd64                    1.4.3-3                        amd64        计算哈希函数的共享库
ii  librist4:amd64                     0.2.7+dfsg-1                   amd64        可靠的互联网流传输 -- 共享库
ii  librsvg2-2:amd64                   2.54.7+dfsg-1~deb12u1          amd64        基于SAX的SVG文件渲染库（运行时）
ii  librsvg2-common:amd64              2.54.7+dfsg-1~deb12u1          amd64        基于SAX的SVG文件渲染库（额外运行时）
ii  librsvg2-dev:amd64                 2.54.7+dfsg-1~deb12u1          amd64        基于SAX的SVG文件渲染库（开发）
ii  librtmp1:amd64                     2.4+20151223.gitfa8646d.1-2+b2 amd64        RTMP流的工具包（共享库）
ii  librttopo-dev:amd64                1.1.0-3                        amd64        托斯卡纳大区拓扑库 - 开发文件
ii  librttopo1:amd64                   1.1.0-3                        amd64        托斯卡纳大区拓扑库
ii  librubberband2:amd64               3.1.2+dfsg0-1                  amd64        音频时间拉伸和音调变换库
ii  libsamplerate0:amd64               0.2.2-3                        amd64        音频采样率转换库
ii  libsasl2-2:amd64                   2.1.28+dfsg-10                 amd64        Cyrus SASL - 认证抽象库
ii  libsasl2-modules-db:amd64          2.1.28+dfsg-10                 amd64        Cyrus SASL - 可插拔认证模块（DB）
ii  libsdl2-2.0-0:amd64                2.26.5+dfsg-1                  amd64        简单直接媒体层
ii  libseccomp2:amd64                  2.5.4-1+b3                     amd64        Linux seccomp过滤器的高级接口
ii  libselinux1:amd64                  3.4-1+b6                       amd64        SELinux运行时共享库
ii  libselinux1-dev:amd64              3.4-1+b6                       amd64        SELinux开发头文件
ii  libsemanage-common                 3.4-1                          all          SELinux策略管理库的公共文件
ii  libsemanage2:amd64                 3.4-1+b5                       amd64        SELinux策略管理库
ii  libsensors-config                  1:3.6.0-7.1                    all          lm-sensors配置文件
ii  libsensors5:amd64                  1:3.6.0-7.1                    amd64        读取温度/电压/风扇传感器的库
ii  libsepol-dev:amd64                 3.4-2.1                        amd64        SELinux二进制策略操作库和开发文件
ii  libsepol2:amd64                    3.4-2.1                        amd64        操作二进制安全策略的SELinux库
ii  libserd-0-0:amd64                  0.30.16-1                      amd64        轻量级RDF语法库
ii  libserf-1-1:amd64                  1.3.9-11                       amd64        高性能异步HTTP客户端库
ii  libshine3:amd64                    3.1.1-2                        amd64        定点MP3编码库 - 运行时文件
ii  libslang2:amd64                    2.3.3-3                        amd64        S-Lang编程库 - 运行时版本
ii  libsm-dev:amd64                    2:1.2.3-1                      amd64        X11会话管理库（开发头文件）
ii  libsm6:amd64                       2:1.2.3-1                      amd64        X11会话管理库
ii  libsmartcols1:amd64                2.38.1-5+deb12u1               amd64        智能列输出对齐库
ii  libsnappy1v5:amd64                 1.1.9-3                        amd64        快速压缩/解压缩库
ii  libsndfile1:amd64                  1.2.0-1                        amd64        读取/写入音频文件的库
ii  libsndio7.0:amd64                  1.9.0-0.3+b2                   amd64        来自OpenBSD的小型音频和MIDI框架，运行时库
ii  libsodium23:amd64                  1.0.18-1                       amd64        网络通信、加密和签名库
ii  libsonic0:amd64                    0.2.0-12                       amd64        加速或减慢语音的简单库
ii  libsord-0-0:amd64                  0.16.14+git221008-1            amd64        在内存中存储RDF数据的库
ii  libsratom-0-0:amd64                0.6.14-1                       amd64        将LV2原子序列化到Turtle或从Turtle反序列化的库
ii  libsrt1.5-gnutls:amd64             1.5.1-1                        amd64        安全的可靠传输UDP流媒体库（GnuTLS风格）
ii  libss2:amd64                       1.47.0-2                       amd64        命令行接口解析库
ii  libssh-gcrypt-4:amd64              0.10.6-0+deb12u1               amd64        微型C SSH库（gcrypt风格）
ii  libssh2-1:amd64                    1.10.0-3+b1                    amd64        SSH2客户端库
ii  libssl-dev:amd64                   3.0.13-1~deb12u1               amd64        安全套接字层工具包 - 开发文件
ii  libssl3:amd64                      3.0.13-1~deb12u1               amd64        安全套接字层工具包 - 共享库
ii  libstdc++-12-dev:amd64             12.2.0-14                      amd64        GNU标准C++库v3（开发文件）
ii  libstdc++6:amd64                   12.2.0-14                      amd64        GNU标准C++库v3
ii  libstemmer0d:amd64                 2.2.0-2                        amd64        用于信息检索的Snowball词干算法
ii  libsuperlu-dev:amd64               5.3.0+dfsg1-2+b1               amd64        大型稀疏线性方程组的直接解法
ii  libsuperlu5:amd64                  5.3.0+dfsg1-2+b1               amd64        大型稀疏线性方程组的直接解法
ii  libsvn1:amd64                      1.14.2-4+b2                    amd64        Apache Subversion使用的共享库
ii  libsvtav1enc1:amd64                1.4.1+dfsg-1                   amd64        可扩展视频技术AV1（libsvtav1enc共享库）
ii  libswresample4:amd64               7:5.1.5-0+deb12u1              amd64        FFmpeg库用于音频重采样、重矩阵化等 - 运行时文件
ii  libswscale6:amd64                  7:5.1.5-0+deb12u1              amd64        FFmpeg库用于图像缩放和各种转换 - 运行时文件
ii  libsystemd-shared:amd64            252.26-1~deb12u2               amd64        systemd共享私有库
ii  libsystemd0:amd64                  252.26-1~deb12u2               amd64        systemd工具库
ii  libsz2:amd64                       1.0.6-1+b1                     amd64        自适应熵编码库 - SZIP
ii  libtasn1-6:amd64                   4.19.0-2                       amd64        管理ASN.1结构的库（运行时）
ii  libtcl8.6:amd64                    8.6.13+dfsg-2                  amd64        Tcl（工具命令语言）v8.6 - 运行时库文件
ii  libtesseract-dev:amd64             5.3.0-2                        amd64        tesseract命令行OCR工具的开发文件
ii  libtesseract5:amd64                5.3.0-2                        amd64        Tesseract OCR库
ii  libtext-iconv-perl:amd64           1.7-8                          amd64        在Perl中转换字符集的模块
ii  libthai-data                       0.1.29-1                       all          泰语支持库的数据文件
ii  libthai0:amd64                     0.1.29-1                       amd64        泰语支持库
ii  libtheora0:amd64                   1.1.1+dfsg.1-16.1+b1           amd64        Theora视频压缩编解码器
ii  libtie-ixhash-perl                 1.23-4                         all          为关联数组排序的Perl模块
ii  libtiff-dev:amd64                  4.5.0-6+deb12u1                amd64        标记图像文件格式库（TIFF），开发文件
ii  libtiff6:amd64                     4.5.0-6+deb12u1                amd64        标记图像文件格式（TIFF）库
ii  libtiffxx6:amd64                   4.5.0-6+deb12u1                amd64        标记图像文件格式（TIFF）库 -- C++接口
ii  libtimedate-perl                   2.3300-2                       all          操作日期/时间信息的模块集合
ii  libtinfo6:amd64                    6.4-4                          amd64        终端处理的共享低级库
ii  libtirpc-common                    1.3.3+ds-1                     all          独立于传输的RPC库 - 公共文件
ii  libtirpc-dev:amd64                 1.3.3+ds-1                     amd64        独立于传输的RPC库 - 开发文件
ii  libtirpc3:amd64                    1.3.3+ds-1                     amd64        独立于传输的RPC库
ii  libtk8.6:amd64                     8.6.13-2                       amd64        Tcl和X11的Tk工具包v8.6 - 窗口化shell
ii  libtk8.6-dev:amd64                 8.6.13-2                       amd64        Tcl和X11的Tk工具包v8.6 - 开发文件
ii  libtool                            2.4.7-5                        all          通用库支持脚本
ii  libtry-tiny-perl                   0.31-2                         all          提供最小try/catch的模块
ii  libtsan2:amd64                     12.2.0-14                      amd64        ThreadSanitizer -- 基于Valgrind的竞态检测器（运行时）
ii  libtwolame0:amd64                  0.4.0-2                        amd64        MPEG音频第2层编码库
ii  libubsan1:amd64                    12.2.0-14                      amd64        UBSan -- 未定义行为清理器（运行时）
ii  libudev1:amd64                     252.26-1~deb12u2               amd64        libudev共享库
ii  libudfread0:amd64                  1.1.2-1                        amd64        UDF读取器库
ii  libunistring2:amd64                1.0-2                          amd64        C库，用于处理UTF-8 Unicode数据
ii  libunwind8:amd64                   1.6.2-3                        amd64        确定程序调用链的库 - 运行时
ii  liburi-perl                        5.17-1                         all          操作和访问URI字符串的模块
ii  liburiparser-dev                   0.9.7+dfsg-2                   amd64        uriparser的开发文件
ii  liburiparser1:amd64                0.9.7+dfsg-2                   amd64        符合RFC 3986的URI解析库
ii  libusb-1.0-0:amd64                 2:1.0.26-1                     amd64        用户空间USB编程库
ii  libutf8proc2:amd64                 2.8.0-1                        amd64        处理UTF-8 Unicode数据的C库（共享库）
ii  libuuid1:amd64                     2.38.1-5+deb12u1               amd64        通用唯一ID库
ii  libuv1:amd64                       1.44.2-1+deb12u1               amd64        异步事件通知库 - 运行时库
ii  libva-drm2:amd64                   2.17.0-1                       amd64        Linux的视频加速（VA）API -- DRM运行时
ii  libva-x11-2:amd64                  2.17.0-1                       amd64        Linux的视频加速（VA）API -- X11运行时
ii  libva2:amd64                       2.17.0-1                       amd64        Linux的视频加速（VA）API -- 运行时
ii  libvdpau-va-gl1:amd64              0.4.2-1+b1                     amd64        带OpenGL/VAAPI后端的VDPAU驱动程序
ii  libvdpau1:amd64                    1.5-2                          amd64        Unix的视频解码和呈现API（库）
ii  libvidstab1.1:amd64                1.1.0-2+b1                     amd64        视频稳定库（共享库）
ii  libvorbis0a:amd64                  1.3.7-1                        amd64        Vorbis通用音频压缩编解码器的解码器库
ii  libvorbisenc2:amd64                1.3.7-1                        amd64        Vorbis通用音频压缩编解码器的编码器库
ii  libvorbisfile3:amd64               1.3.7-1                        amd64        Vorbis通用音频压缩编解码器的高级API
ii  libvpx7:amd64                      1.12.0-1+deb12u3               amd64        VP8和VP9视频编解码器（共享库）
ii  libvulkan1:amd64                   1.3.239.0-1                    amd64        Vulkan加载器库
ii  libwavpack1:amd64                  5.6.0-1                        amd64        音频编解码器（有损和无损） - 库
ii  libwayland-client0:amd64           1.21.0-1                       amd64        wayland合成器基础设施 - 客户端库
ii  libwayland-cursor0:amd64           1.21.0-1                       amd64        wayland合成器基础设施 - 游标库
ii  libwayland-egl1:amd64              1.21.0-1                       amd64        wayland合成器基础设施 - EGL库
ii  libwayland-server0:amd64           1.21.0-1                       amd64        wayland合成器基础设施 - 服务器库
ii  libwebp-dev:amd64                  1.2.4-0.2+deb12u1              amd64        数字摄影图像的有损压缩
ii  libwebp7:amd64                     1.2.4-0.2+deb12u1              amd64        数字摄影图像的有损压缩
ii  libwebpdemux2:amd64                1.2.4-0.2+deb12u1              amd64        数字摄影图像的有损压缩。
ii  libwebpmux3:amd64                  1.2.4-0.2+deb12u1              amd64        数字摄影图像的有损压缩
ii  libwmf-0.2-7:amd64                 0.2.12-5.1                     amd64        Windows元文件转换库
ii  libwmf-dev                         0.2.12-5.1                     amd64        Windows元文件转换开发
ii  libwmflite-0.2-7:amd64             0.2.12-5.1                     amd64        Windows元文件转换精简库
ii  libwww-perl                        6.68-1                         all          全球广域网的简单和一致接口
ii  libwww-robotrules-perl             6.02-1                         all          robots.txt派生权限的数据库
ii  libx11-6:amd64                     2:1.8.4-2+deb12u2              amd64        X11客户端库
ii  libx11-data                        2:1.8.4-2+deb12u2              all          X11客户端库
ii  libx11-dev:amd64                   2:1.8.4-2+deb12u2              amd64        X11客户端库（开发头文件）
ii  libx11-protocol-perl               0.56-9                         all          X窗口系统协议版本11的Perl模块
ii  libx11-xcb1:amd64                  2:1.8.4-2+deb12u2              amd64        Xlib/XCB接口库
ii  libx264-164:amd64                  2:0.164.3095+gitbaee400-3      amd64        x264视频编码库
ii  libx265-199:amd64                  3.5-2+b1                       amd64        H.265/HEVC视频流编码器（共享库）
ii  libx265-dev:amd64                  3.5-2+b1                       amd64        H.265/HEVC视频流编码器（开发文件）
ii  libxau-dev:amd64                   1:1.0.9-1                      amd64        X11授权库（开发头文件）
ii  libxau6:amd64                      1:1.0.9-1                      amd64        X11授权库
ii  libxaw7:amd64                      2:1.0.14-1                     amd64        X11 Athena Widget库
ii  libxcb-dri2-0:amd64                1.15-1                         amd64        X C绑定，dri2扩展
ii  libxcb-dri3-0:amd64                1.15-1                         amd64        X C绑定，dri3扩展
ii  libxcb-glx0:amd64                  1.15-1                         amd64        X C绑定，glx扩展
ii  libxcb-present0:amd64              1.15-1                         amd64        X C绑定，present扩展
ii  libxcb-randr0:amd64                1.15-1                         amd64        X C绑定，randr扩展
ii  libxcb-render0:amd64               1.15-1                         amd64        X C绑定，render扩展
ii  libxcb-render0-dev:amd64           1.15-1                         amd64        X C绑定，render扩展，开发文件
ii  libxcb-shape0:amd64                1.15-1                         amd64        X C绑定，shape扩展
ii  libxcb-shm0:amd64                  1.15-1                         amd64        X C绑定，shm扩展
ii  libxcb-shm0-dev:amd64              1.15-1                         amd64        X C绑定，shm扩展，开发文件
ii  libxcb-sync1:amd64                 1.15-1                         amd64        X C绑定，sync扩展
ii  libxcb-xfixes0:amd64               1.15-1                         amd64        X C绑定，xfixes扩展
ii  libxcb1:amd64                      1.15-1                         amd64        X C绑定
ii  libxcb1-dev:amd64                  1.15-1                         amd64        X C绑定，开发文件
ii  libxcomposite1:amd64               1:0.4.5-1                      amd64        X11复合扩展库
ii  libxcursor1:amd64                  1:1.2.1-1                      amd64        X游标管理库
ii  libxdamage1:amd64                  1:1.1.6-1                      amd64        X11损坏区域扩展库
ii  libxdmcp-dev:amd64                 1:1.1.2-3                      amd64        X11授权库（开发头文件）
ii  libxdmcp6:amd64                    1:1.1.2-3                      amd64        X11显示管理器控制协议库
ii  libxdot4:amd64                     2.42.2-7+b3                    amd64        丰富的图形绘制工具 - xdot库
ii  libxerces-c-dev:amd64              3.2.4+debian-1                 amd64        验证XML解析器库的C++（开发文件）
ii  libxerces-c3.2:amd64               3.2.4+debian-1                 amd64        验证XML解析器库的C++
ii  libxext-dev:amd64                  2:1.3.4-1+b1                   amd64        X11杂项扩展库（开发头文件）
ii  libxext6:amd64                     2:1.3.4-1+b1                   amd64        X11杂项扩展库
ii  libxfixes3:amd64                   1:6.0.0-2                      amd64        X11杂项'修复'扩展库
ii  libxft-dev:amd64                   2.3.6-1                        amd64        基于FreeType的X字体绘制库（开发文件）
ii  libxft2:amd64                      2.3.6-1                        amd64        基于FreeType的X字体绘制库
ii  libxi6:amd64                       2:1.8-1+b1                     amd64        X11输入扩展库
ii  libxinerama1:amd64                 2:1.1.4-3                      amd64        X11 Xinerama扩展库
ii  libxkbcommon0:amd64                1.5.0-1                        amd64        XKB编译器的库接口 - 共享库
ii  libxkbfile1:amd64                  1:1.1.0-1                      amd64        X11键盘文件操作库
ii  libxml-parser-perl                 2.46-4                         amd64        解析HTML文本文档的模块集合
ii  libxml-twig-perl                   1:3.52-2                       all          以树模式处理巨大XML文档的Perl模块
ii  libxml-xpathengine-perl            0.14-2                         all          DOM-like树的可重用XPath引擎
ii  libxml2:amd64                      2.9.14+dfsg-1.3~deb12u1        amd64        GNOME XML库
ii  libxml2-dev:amd64                  2.9.14+dfsg-1.3~deb12u1        amd64        GNOME XML库 - 开发文件
ii  libxmlb2:amd64                     0.3.10-2                       amd64        二进制XML库
ii  libxmu6:amd64                      2:1.1.3-3                      amd64        X11杂项实用库
ii  libxmuu1:amd64                     2:1.1.3-3                      amd64        X11杂项微型实用库
ii  libxpm4:amd64                      1:3.5.12-1.1+deb12u1           amd64        X11像素图库
ii  libxrandr2:amd64                   2:1.5.2-2+b1                   amd64        X11 RandR扩展库
ii  libxrender-dev:amd64               1:0.9.10-1.1                   amd64        X渲染扩展客户端库（开发文件）
ii  libxrender1:amd64                  1:0.9.10-1.1                   amd64        X渲染扩展客户端库
ii  libxshmfence1:amd64                1.3-1                          amd64        X共享内存围栏 - 共享库
ii  libxslt1-dev:amd64                 1.1.35-1                       amd64        XSLT 1.0处理库 - 开发套件
ii  libxslt1.1:amd64                   1.1.35-1                       amd64        XSLT 1.0处理库 - 运行时库
ii  libxss-dev:amd64                   1:1.2.3-1                      amd64        X11屏幕保护程序扩展库（开发头文件）
ii  libxss1:amd64                      1:1.2.3-1                      amd64        X11屏幕保护程序扩展库
ii  libxt-dev:amd64                    1:1.2.1-1.1                    amd64        X11工具包内部库（开发头文件）
ii  libxt6:amd64                       1:1.2.1-1.1                    amd64        X11工具包内部库
ii  libxtst6:amd64                     2:1.2.3-1.1                    amd64        X11测试 -- 记录扩展库
ii  libxv1:amd64                       2:1.0.11-1.1                   amd64        X11视频扩展库
ii  libxvidcore4:amd64                 2:1.3.7-1                      amd64        开源MPEG-4视频编解码器（库）
ii  libxxf86dga1:amd64                 2:1.1.5-1                      amd64        X11直接图形访问扩展库
ii  libxxf86vm1:amd64                  1:1.1.4-1+b2                   amd64        X11 XFree86视频模式扩展库
ii  libxxhash0:amd64                   0.8.1-1                        amd64        xxhash的共享库
ii  libyaml-0-2:amd64                  0.2.5-1                        amd64        快速YAML 1.1解析器和发射器库
ii  libyaml-dev:amd64                  0.2.5-1                        amd64        快速YAML 1.1解析器和发射器库（开发）
ii  libyuv0:amd64                      0.0~git20230123.b2528b0-1      amd64        YUV缩放库（共享库）
ii  libz3-4:amd64                      4.8.12-3.1                     amd64        来自微软研究院的定理证明器 - 运行时库
ii  libzimg2:amd64                     3.0.4+ds1-1                    amd64        缩放、色彩空间、深度转换库（共享库）
ii  libzmq5:amd64                      4.3.4-6                        amd64        轻量级消息内核（共享库）
ii  libzstd-dev:amd64                  1.5.4+dfsg2-5                  amd64        快速无损压缩算法 -- 开发文件
ii  libzstd1:amd64                     1.5.4+dfsg2-5                  amd64        快速无损压缩算法
ii  libzvbi-common                     0.2.41-1                       all          垂直消隐间隔解码器（VBI） - 公共文件
ii  libzvbi0:amd64                     0.2.41-1                       amd64        垂直消隐间隔解码器（VBI） - 运行时文件
ii  linux-compiler-gcc-12-x86          6.1.99-1                       amd64        Linux on x86的编译器（元包）
ii  linux-headers-6.1.0-23-amd64       6.1.99-1                       amd64        Linux 6.1.0-23-amd64的头文件
ii  linux-headers-6.1.0-23-common      6.1.99-1                       all          Linux 6.1.0-23的公共头文件
ii  linux-headers-amd64                6.1.99-1                       amd64        Linux amd64配置的头文件（元包）
ii  linux-kbuild-6.1                   6.1.99-1                       amd64        Linux 6.1的Kbuild基础设施
ii  linux-libc-dev:amd64               6.1.99-1                       amd64        Linux内核头文件，用于用户空间开发
ii  login                              1:4.13+dfsg1-1+b1              amd64        系统登录工具
ii  logsave                            1.47.0-2                       amd64        将命令的输出保存到日志文件中
ii  lsb-release                        12.0-1                         all          Linux标准库版本报告工具（最小实现）
ii  m4                                 1.4.19-3                       amd64        宏处理语言
ii  make                               4.3-4.1                        amd64        指导编译的工具
ii  mariadb-common                     1:10.11.6-0+deb12u1            all          MariaDB公共配置文件
ii  mawk                               1.3.4.20200120-3.1             amd64        模式扫描和文本处理语言
ii  media-types                        10.0.0                         all          标准媒体类型及其常用文件扩展名的列表
ii  mercurial                          6.3.2-1                        amd64        易于使用、可扩展的分布式版本控制系统
ii  mercurial-common                   6.3.2-1                        all          易于使用、可扩展的分布式版本控制系统（公共文件）
ii  mesa-va-drivers:amd64              22.3.6-1+deb12u1               amd64        Mesa VA-API视频加速驱动程序
ii  mesa-vdpau-drivers:amd64           22.3.6-1+deb12u1               amd64        Mesa VDPAU视频加速驱动程序
ii  mesa-vulkan-drivers:amd64          22.3.6-1+deb12u1               amd64        Mesa Vulkan图形驱动程序
ii  mount                              2.38.1-5+deb12u1               amd64        挂载和操纵文件系统的工具
ii  mysql-common                       5.8+1.1.0                      all          MySQL数据库公共文件，例如/etc/mysql/my.cnf
ii  ncurses-base                       6.4-4                          all          基本的终端类型定义
ii  ncurses-bin                        6.4-4                          amd64        与终端相关的程序和手册页
ii  netbase                            6.4                            all          基本的TCP/IP网络系统
ii  ninja-build                        1.11.1-1                       amd64        接近Make精神的小型构建系统
ii  ocl-icd-libopencl1:amd64           2.3.1-1                        amd64        通用OpenCL ICD加载器
ii  openssh-client                     1:9.2p1-2+deb12u2              amd64        安全shell（SSH）客户端，用于安全访问远程机器
ii  openssl                            3.0.13-1~deb12u1               amd64        安全套接字层工具包 - 加密工具
ii  packagekit                         1.2.6-5                        amd64        提供包管理服务
ii  packagekit-tools                   1.2.6-5                        amd64        提供PackageKit命令行工具
ii  passwd                             1:4.13+dfsg1-1+b1              amd64        更改和管理密码及组数据
ii  patch                              2.7.6-7                        amd64        将补丁文件应用到原始文件
ii  perl                               5.36.0-7+deb12u1               amd64        Larry Wall的实用提取和报告语言
ii  perl-base                          5.36.0-7+deb12u1               amd64        最小Perl系统
ii  perl-modules-5.36                  5.36.0-7+deb12u1               all          核心Perl模块
ii  perl-openssl-defaults:amd64        7+b1                           amd64        Perl OpenSSL包的版本兼容性基线
ii  pinentry-curses                    1.2.1-1                        amd64        基于curses的PIN或密码短语输入对话框，供GnuPG使用
ii  pkg-config:amd64                   1.8.1-1                        amd64        管理库的编译和链接标志（过渡包）
ii  pkgconf:amd64                      1.8.1-1                        amd64        管理库的编译和链接标志
ii  pkgconf-bin                        1.8.1-1                        amd64        管理库的编译和链接标志（二进制文件）
ii  pocketsphinx-en-us                 0.8+5prealpha+1-15             all          语音识别工具 - 美国英语语言模型
ii  polkitd                            122-3                          amd64        管理管理策略和权限的框架
ii  poppler-data                       0.4.12-1                       all          poppler PDF渲染库的编码数据
ii  poppler-utils                      22.12.0-2+b1                   amd64        基于Poppler的PDF工具
ii  procps                             2:4.0.2-3                      amd64        /proc文件系统工具
ii  proj-bin                           9.1.1-1+b1                     amd64        地图投影库（工具）
ii  proj-data                          9.1.1-1                        all          地图投影过滤器和库（基准包）
ii  python-apt-common                  2.6.0                          all          libapt-pkg的Python接口（区域设置）
ii  python-is-python3                  3.11.2-1+deb12u1               all          将/usr/bin/python符号链接到python3
ii  python3                            3.11.2-1+b1                    amd64        交互式高级面向对象语言（默认python3版本）
ii  python3-apt                        2.6.0                          amd64        libapt-pkg的Python 3接口
ii  python3-blinker                    1.5-1                          all          快速、简单的对象到对象和广播信号（Python3）
ii  python3-cffi-backend:amd64         1.15.1-5+b1                    amd64        Python 3调用C代码的外部函数接口 - 运行时
ii  python3-cryptography               38.0.4-3                       amd64        Python库，暴露加密配方和原语（Python 3）
ii  python3-dbus                       1.3.2-4+b1                     amd64        简单的进程间消息系统（Python 3接口）
ii  python3-distro                     1.8.0-1                        all          Linux OS平台信息API
ii  python3-distutils                  3.11.2-3                       all          Python 3.x的distutils包
ii  python3-gi                         3.42.2-3+b1                    amd64        gobject-introspection库的Python 3绑定
ii  python3-httplib2                   0.20.4-3                       all          为Python3编写的综合HTTP客户端库
ii  python3-jwt                        2.6.0-1                        all          JSON Web令牌的Python 3实现
ii  python3-lazr.restfulclient         0.14.5-1                       all          lazr.restful-based web服务的客户端（Python 3）
ii  python3-lazr.uri                   1.0.6-3                        all          解析、操纵和生成URI的库
ii  python3-lib2to3                    3.11.2-3                       all          交互式高级面向对象语言（lib2to3）
ii  python3-minimal                    3.11.2-1+b1                    amd64        Python语言的最小子集（默认python3版本）
ii  python3-oauthlib                   3.2.2-1                        all          OAuth的通用、规范兼容Python3实现
ii  python3-pkg-resources              66.1.1-1                       all          使用pkg_resources的包发现和资源访问
ii  python3-pyaudio                    0.2.13-1+b1                    amd64        PortAudio v19的Python3绑定
ii  python3-pyparsing                  3.0.9-1                        all          创建和执行简单语法的备选方案 - Python 3.x
ii  python3-six                        1.16.0-4                       all          Python 2和3兼容库
ii  python3-software-properties        0.99.30-4.1~deb12u1            all          管理安装软件的仓库
ii  python3-wadllib                    1.3.6-4                        all          导航WADL文件的Python 3库
ii  python3.11                         3.11.2-6                       amd64        交互式高级面向对象语言（版本3.11）
ii  python3.11-minimal                 3.11.2-6                       amd64        Python语言的最小子集（版本3.11）
ii  readline-common                    8.2-1.3                        all          GNU readline和历史库，公共文件
ii  rpcsvc-proto                       1.4.3-1                        amd64        RPC协议编译器和定义
ii  sed                                4.9-1                          amd64        GNU流编辑器，用于过滤/转换文本
ii  sensible-utils                     0.0.17+nmu1                    all          明智备选选择的工具
ii  sgml-base                          1.31                           all          SGML基础设施和SGML目录文件支持
ii  shared-mime-info                   2.2-1                          amd64        FreeDesktop.org共享MIME数据库和规范
ii  software-properties-common         0.99.30-4.1~deb12u1            all          管理安装软件的仓库（公共）
ii  sox                                14.4.2+git20190427-3.5         amd64        声音处理的瑞士军刀
ii  sq                                 0.27.0-2+b1                    amd64        来自Sequoia的OpenPGP命令行工具
ii  subversion                         1.14.2-4+b2                    amd64        高级版本控制系统
ii  sudo                               1.9.13p3-1+deb12u1             amd64        为特定用户提供有限的超级用户权限
ii  swig                               4.1.0-0.2                      all          为C/C++代码生成脚本接口
ii  swig4.0                            4.1.0-0.2                      amd64        为C/C++代码生成脚本接口
ii  systemd                            252.26-1~deb12u2               amd64        系统和服务管理器
ii  systemd-sysv                       252.26-1~deb12u2               amd64        系统和服务管理器 - SysV兼容性符号链接
ii  systemd-timesyncd                  252.26-1~deb12u2               amd64        与NTP服务器同步本地时间的最小服务
ii  sysvinit-utils                     3.06-4                         amd64        类System-V的工具
ii  tar                                1.34+dfsg-1.2+deb12u1          amd64        tar归档工具的GNU版本
ii  tcl                                8.6.13                         amd64        工具命令语言（默认版本） - shell
ii  tcl-dev:amd64                      8.6.13                         amd64        工具命令语言（默认版本） - 开发文件
ii  tcl8.6                             8.6.13+dfsg-2                  amd64        Tcl（工具命令语言）v8.6 - shell
ii  tcl8.6-dev:amd64                   8.6.13+dfsg-2                  amd64        Tcl（工具命令语言）v8.6 - 开发文件
ii  tesseract-ocr                      5.3.0-2                        amd64        Tesseract命令行OCR工具
ii  tesseract-ocr-eng                  1:4.1.0-2                      all          tesseract-ocr英语语言文件
ii  tesseract-ocr-osd                  1:4.1.0-2                      all          tesseract-ocr脚本和方向语言文件
ii  tini                               0.19.0-1                       amd64        微小但有效的容器init
ii  tk                                 8.6.13                         amd64        Tcl和X11的工具包（默认版本） - 窗口化shell
ii  tk-dev:amd64                       8.6.13                         amd64        Tcl和X11的工具包（默认版本） - 开发文件
ii  tk8.6                              8.6.13-2                       amd64        Tcl和X11的Tk工具包v8.6 - 窗口化shell
ii  tk8.6-dev:amd64                    8.6.13-2                       amd64        Tcl和X11的Tk工具包v8.6 - 开发文件
ii  tzdata                             2024a-0+deb12u1                all          时区和夏令时数据
ii  ucf                                3.0043+nmu1                    all          更新配置文件：保留用户对配置文件的更改
ii  unixodbc-common                    2.3.11-2+deb12u1               all          公共ODBC配置文件
ii  unixodbc-dev:amd64                 2.3.11-2+deb12u1               amd64        Unix的ODBC库（开发文件）
ii  unrtf                              0.21.10-clean-1                amd64        RTF转换为其他格式的转换器
ii  unzip                              6.0-28                         amd64        .zip文件的解压缩器
ii  usr-is-merged                      37~deb12u1                     all          断言合并-/usr系统的过渡包
ii  util-linux                         2.38.1-5+deb12u1               amd64        杂项系统工具
ii  util-linux-extra                   2.38.1-5+deb12u1               amd64        交互式登录工具
ii  uuid-dev:amd64                     2.38.1-5+deb12u1               amd64        通用唯一ID库 - 头文件和静态库
ii  va-driver-all:amd64                2.17.0-1                       amd64        视频加速（VA）API -- 驱动程序元包
ii  vdpau-driver-all:amd64             1.5-2                          amd64        Unix的视频解码和呈现API（驱动程序元包）
ii  vim                                2:9.0.1378-2                   amd64        Vi改进版 - 增强的vi编辑器
ii  vim-common                         2:9.0.1378-2                   all          Vi改进版 - 公共文件
ii  vim-runtime                        2:9.0.1378-2                   all          Vi改进版 - 运行时文件
ii  wget                               1.21.3-1+b2                    amd64        从web检索文件
ii  x11-common                         1:7.7+23                       all          X窗口系统（X.Org）基础设施
ii  x11-utils                          7.7+5                          amd64        X11工具
ii  x11-xserver-utils                  7.7+9+b1                       amd64        X服务器工具
ii  x11proto-core-dev                  2022.1-1                       all          过渡虚拟包
ii  x11proto-dev                       2022.1-1                       all          X11扩展协议和辅助头文件
ii  xdg-utils                          1.1.3-4.1                      all          来自freedesktop.org的桌面集成工具
ii  xkb-data                           2.35.1-1                       all          X键盘扩展（XKB）配置数据
ii  xml-core                           0.18+nmu1                      all          XML基础设施和XML目录文件支持
ii  xorg-sgml-doctools                 1:1.11-1.1                     all          构建X.Org SGML文档的公共工具
ii  xtrans-dev                         1.4.0-1                        all          X传输库（开发文件）
ii  xxd                                2:9.0.1378-2                   amd64        创建（或反向）十六进制转储的工具
ii  xz-utils                           5.4.1-0.2                      amd64        XZ格式压缩工具
ii  zlib1g:amd64                       1:1.2.13.dfsg-1                amd64        压缩库 - 运行时
ii  zlib1g-dev:amd64                   1:1.2.13.dfsg-1                amd64        压缩库 - 开发
ii  zutty                              0.14.0.20230218+dfsg1-1        amd64        高效的全功能X11终端仿真器
```

