# FS模块

对脚本文档沙盒虚拟文件系统的只读访问。定义于`index.ts`。

**`modules/`目录下的路径说明：**  
目录名是**模块类型**（如`notion`、`slack`、`mcpServer`），而非连接名称。对于MCP服务器，所有相关路径统一使用`modules/mcpServer/`（例如`modules/mcpServer/index.ts`、`modules/mcpServer/AGENTS.md`）；连接名称如`mcpServer_ramp`仅用于调用`connections.mcpServer_ramp.runTool`，而非路径。

### 浏览目录

`readDir({ dir })` 返回目标文件夹内所有条目的扁平化列表。

｀｀｀ts
const { entries } = connections.fs.readDir({ dir: "modules/notion" })
// entries => ["index.ts", "agents", "databases"]
｀｀｀

### 读取文件

`readFiles({ files })` 返回每个文件的原始内容（包括文件`path`）。

｀｀｀ts
const { files } = connections.fs.readFiles({
	files: ["modules/notion/index.ts"],
})
// files => [{ path: "modules/notion/index.ts", content: "..." }]
｀｀｀