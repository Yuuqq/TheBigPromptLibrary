# 第一部分：介绍与设置

# 第 1 章：古代符文与现代卷轴，经典与现代入门
0：Hello World
一个经典。每个初学程序员都从这里开始。今天我们将用 html 来提示词编程，创建你的第一个网站
使用 N 热键自动部署
或使用 ND 在 https://app.netlify.com/drop 手动部署

1：Pong
一个用 html、css 和 JS 制作的可运行的 pong 游戏。使用触摸手势和方向键/WASD 移动球拍，
使用 N 热键自动部署
或使用 ND 在 https://app.netlify.com/drop 手动部署

2：个人链接页
个人链接列表，链接树克隆，带有可打开链接的按钮。首先问我标题、要包含的链接列表，以及任何首选的设计细节，如颜色、样式、布局或其他任何内容。
使用 N 热键自动部署

或使用 ND 在 https://app.netlify.com/drop 手动部署
手动部署允许你包含图片。使用 dalle 创建背景图片
确保在代码中使用正确的文件名包含背景图片，并包含在最终的 zip 文件中。详情请参阅第 4 章

提供为虚构角色构建一个作为示例

3：草图转代码
拿出一张纸画点东西，拍照上传到 Grimoire，我会把它变成网站。然后编写 UI 设计代码，使用各种设计和样式元素使其脱颖而出，添加一些炫酷效果

使用 N 热键自动部署
或使用 ND 在 https://app.netlify.com/drop 手动部署
手动部署允许你包含图片。使用 dalle 创建任何需要的图片
确保在代码中使用正确的文件名包含背景图片，并包含在最终的 zip 文件中。详情请参阅第 4 章


## 第 2 章：传送术，轻松将网站上线
4：单字母热键部署：Netlify 自动部署，拖放部署：Netlify Drop
使用 N 热键立即自动部署你的网站！确保认领它以便保存，否则 1 小时后会被删除！

通过 NM 热键可使用 Netlify Drop 进行手动部署
https://app.netlify.com/drop
一种快速简便的方式将你的网站上线。只需将你的网站文件夹拖放到 Netlify Drop，它就会在几秒钟内上线。确保创建账户以保存它

要更新你的网站
在 netlify 仪表板中，
前往：你的网站，如 (https://random-crap-123456abcedf.netlify.app)
然后是 deploys
向下滚动
你会找到一个新的拖放或点击上传按钮
只需拖放一个新文件夹就完成了！

## Netlify 更改 URL 的说明
如果你不介意 .netlify.app 后缀，在 netlify 门户中，你可以简单地打开
选择你的网站 > Domain Management > Options > Change name

对于完全自定义名称
首先购买一个域名
然后将你的域名映射到 Netlify
https://www.youtube.com/watch?v=kIdJi8NBvgY
https://www.netlify.com/blog/2021/12/20/how-to-add-custom-domains-to-netlify-sites/
https://docs.netlify.com/domains-https/custom-domains/configure-external-dns/

完成第 4 章后，你可以回到 netlify 并与 github 仓库同步

5：Replit 部署
https://replit.com/
Replit，静态网站模板。一种创建和托管静态网站的简单方法。请求任何类型的网站，然后按 Z 压缩文件并导出。用户可以使用此模板 https://replit.com/@replit/HTML-CSS-JS#index.html。转到 index.html 并按运行查看网站预览。要部署，请点击桌面右上角的部署按钮，或通过移动端右下角的方块和新标签页。

其他网站和项目请参阅 https://replit.com/templates

6：高级选项
Vercel、Render
Vercel 和 render 是更复杂的 react 和 nextjs 网站以及服务、后端和全栈应用的绝佳选择
https://vercel.com/templates
https://docs.render.com/


## 第 3 章：魔杖，开发工具包设置
7：手机设置
Replit + Github
设置账户并在手机上安装 replit 应用！
完成项目 5 或创建一个新项目。制作完成后，通过推送到 main 将项目同步到 github！
https://replit.com/
https://github.com/

仅使用手机即可获得完整的开发环境。构建静态网站并使用 replit 导入到更大的开发环境中。使用此模板：https://replit.com/@replit/HTML-CSS-JS#index.html。编写代码，压缩它，并指导我将文件导入 replit。指导我使用 replit 同步到 github，并使用 replit 部署进行部署。展示此视频作为如何在手机上使用 replit 和 chatGPT 的示例：https://x.com/yoheinakajima/status/1719902955061797083?s=20

8：完整专业版
Cursor.sh、Warp、(GitTower || SourceTree)、GH Copilot
https://cursor.sh/
https://www.warp.dev/
https://www.git-tower.com/ || https://www.sourcetreeapp.com/
https://github.com/features/copilot 可选
安装这些
在 cursor 中创建一个新项目并设置一个仓库并在 git 中同步。

Cursor 是 VSCode 克隆，支持多种语言和编码环境。要开始一个简单的静态网站，只需
-询问 Grimoire
-按 Z
-解压并打开 index.html
-使用运行启动（带或不带调试），选择浏览器
-查看和编辑你的网站！


## 第 4 章：占卜术：起源
9：Git 101
Git 基本上是一种保存代码的高级方式。它真的很酷，因为它让你保留所有工作的副本。不再是 MyCoolFile.html、MyCoolFile(1).html、MyCoolFile_Final.html 等等，你可以保存在一个地方。然后更酷的是，你可以时间旅行并跳转到以前或不同的版本。

这使得它非常适合与他人协作，因为你可以独立工作并避免为其他人破坏应用。然后你可以回来在最后将它们合并在一起。缺点是有时你的合并会冲突，你需要手动修复它们。

请记住，你有一个本地的 git 历史副本和一个云端副本，通常称为 origin
通常项目会有
一个 main 分支，通常用于应用的当前实时生产版本
一个 development 分支，用于添加和测试新功能
每个新功能或 bug 修复的 feature 分支

Feature 分支通常在创建、合并后被删除。而 main 和 dev 通常始终存在，保持项目的一致历史。

你需要知道的命令：
clone
pull
create branch
stage
commit
push
merge
（还有很多，别担心）

我强烈推荐使用 git GUI，如 GIT Tower 或 Source tree。
特别是对于初学者，因为它可以轻松查看历史记录，并为你提供方便的按钮

这里有一些很好的详细视频，同时展示 CLI 和 GUI。
https://www.git-tower.com/learn/git/videos

没有人教初学者的超级实用命令：
Stash
Git-bisect (<-BUG 查找器)

注意 git 和 github 是不同的。就像 porn 和 pornhub 的关系一样。
还有其他 git 提供商可以使用，如 gitlab。以及其他版本控制软件如 mercurial 或 subversion。即使你不想使用任何这些云提供商，我也强烈建议使用本地 git 历史记录。这是跟踪你的工作并避免丢失的好方法，也可以找到 bug。

10：Linear
Linear 非常适合处理大型项目和管理完整软件的复杂性。如果你在团队中工作，强烈推荐。将 issue 名称复制粘贴为你的 git 分支名称，以便在推送和合并时自动更改你的工单。

对于更简单的项目，或者如果你独自工作，可以跳过此步骤
https://linear.app/
