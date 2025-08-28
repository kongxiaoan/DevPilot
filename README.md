# DevPilot 🚀
面向 AI 时代的“本地项目架构生成与工程启动” MCP Server

> Your Copilot for App Architecture.  
> From Scaffold to Decisions — DevPilot guides your code.  
> 一键生成，智能决策，让架构更轻松。

DevPilot 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 的本地服务，让支持 MCP 的 AI（GitHub Copilot / ChatGPT MCP / 未来的 VS Code / Android Studio Gemini 等）可以通过自然语言直接在你的磁盘上生成工程架构骨架（Android / iOS / React Native / Flutter 等），并逐步扩展到知识记忆、模板化与智能演进。

> 目标：把 “我想要一个采用 xxx 架构的多端应用骨架” 这种自然语言请求，转换成具体目录结构 + 基础文件 + 后续持续增强的自动化能力。

---

## ✨ 特性（当前 & 近期）
| 类别 | 状态 | 说明 |
|------|------|------|
| 架构骨架生成 | ✅ 初始版本 | 生成多层领域/数据/模块目录 |
| 多端支持(Android/iOS/React Native/Flutter) | ⚙️ 进行中 | 逐步补充模板 |
| 可选架构模式 (UseCase / Repository / Domain / Data) | ✅ | 通过参数控制 |
| MCP 工具暴露 | ✅ | 以工具列表形式被 AI 调用 |
| 自然语言触发 | ✅ | “使用 DevPilot 生成一个 Android 项目” |
| Python 核心逻辑 + npm 分发 | ✅ | 后端 Python，前端 npx 一键启动 |
| 健康输出 / 日志结构化 | ⏳ | 准备添加 |
| 更多工具（记忆 / 学习 / 资源索引） | 🧪 规划中 |
| 增量生成 / 二次进化 | 🧪 规划中 |
| 自定义模板仓库 | 🧪 规划中 |
| 多 AI 平台集成 (Claude / Cursor / 等) | 🧪 规划中 |

---

## 🧠 设计理念
1. 把“架构生成”抽象为稳定的工具接口，UI / IDE / AI 只是前端。
2. 后端逻辑优先使用 Python（生态丰富：AST、LLM、向量、分析）。
3. 通过 npm 包 + `uv` 解决“前端环境全是 Node，但我逻辑在 Python”的鸿沟。
4. 所有行为透明：最终产物直接写入本地目录；不锁死在云端。
5. 渐进扩展：从单一工具 → 多工具（architecture / memory / learn / recall / tool）。

---

## 📦 快速开始

### 方式一：直接使用（面向使用者）
（确保已安装 [uv](https://github.com/astral-sh/uv)，或后续提供 pip fallback）

```bash
# 测试服务器是否能启动
npx -y devpilot-mcp@latest
```

若看到启动日志且无 `ModuleNotFoundError`，说明环境 OK。

### 方式二：克隆仓库本地开发（面向贡献者）
```bash
git clone https://github.com/kongxiaoan/DevPilot.git
cd DevPilot

# 创建虚拟环境 & 安装依赖（方案 B：pyproject + uv）
uv venv
source .venv/bin/activate
uv sync

# 运行 Python 版本（直接调试）
uv run src/mcp_architecture_generate.py
```

---

## ⚙️ 安装 / 分发结构说明

| 层 | 内容 | 说明 |
|----|------|------|
| npm 包 (devpilot-mcp) | bin/mcp-server.js | 入口；调用 `uv run ...` |
| Python 源码 | `src/` | 架构生成逻辑、工具注册 |
| 依赖声明 | `pyproject.toml` + （可选）`uv.lock` | 让 uv 可重现安装 |
| 用户启动 | `npx -y devpilot-mcp` | 自动下载 + 启动 MCP 服务器 |
| AI 客户端 | `mcp.json` / IDE UI | 连接并列出工具 |

---

## 🔌 MCP 集成

在支持 MCP 的客户端增加配置（示例：Android Studio Gemini / OpenAI MCP 客户端）：

`mcp.json` 示例：
```json
{
  "servers": {
    "devpilot": {
      "command": "npx",
      "args": ["-y", "devpilot-mcp@latest"]
    }
  }
}
```

放置位置（示例）：
- macOS Android Studio: `~/Library/Application Support/Google/AndroidStudio*/mcp.json`
- Linux: `~/.config/Google/AndroidStudio*/mcp.json`
- OpenAI (实验 MCP 客户端): `~/.config/openai/mcp.json`

重启客户端后应看到 `devpilot` 工具组。

---

## 🛠️ 当前暴露的工具 (示例约定)

| 工具名 | 输入参数 | 说明 | 返回 |
|--------|----------|------|------|
| `architecture_generate` | `platform` (android/ios/react_native/flutter)<br>`project_name`<br>`include_layers` (数组，如 ["domain","data","usecase"])<br>`output_dir` | 生成指定平台项目目录骨架 | JSON：写入路径、创建的文件数、跳过项 |
| （预留）`memory_store` | … | 将经验/知识记入本地存储 | 待实现 |
| （预留）`memory_recall` | … | 检索历史生成上下文 | 待实现 |

> 真实名称以代码中注册的工具为准（后续 README 会同步自动生成）。

---

## 💬 交互示例

### 中文
```
使用 DevPilot 生成一个 Android 项目，项目名：SmartNotes，
包含 domain 层、data 层和 usecase，输出到当前目录的 generated 目录。
```

### English
```
Use DevPilot to generate an Android project named SmartNotes with domain, data and usecase layers, output under ./generated.
```

AI ↔ DevPilot 典型响应：
```json
{
  "status": "ok",
  "root": "/absolute/path/generated/SmartNotes",
  "created_files": 18,
  "skipped": []
}
```

---

## 📂 生成目录（示例）

```
generated/SmartNotes
├── domain
│   ├── models
│   └── usecases
├── data
│   ├── repository
│   └── datasource
├── app
│   └── modules
└── README.md
```

---

## 🧪 开发 / 调试

### 1. 本地直接运行
```bash
uv run src/mcp_architecture_generate.py --debug
```

### 2. 使用 MCP Inspector
```bash
npx @modelcontextprotocol/inspector npx -y devpilot-mcp@latest
```

### 3. 查看工具握手日志
Inspector 中应显示：
```
-> server capabilities ...
<- tools: [architecture_generate, ...]
```

### 4. 常见调试命令
```bash
# 检查依赖是否正确可导入
uv run python -c "import mcp; print(mcp.__file__)"
```

---

## ❗ 常见问题 (FAQ / Troubleshooting)

| 症状 | 原因 | 解决 |
|------|------|------|
| ModuleNotFoundError: No module named 'mcp' | 未携带 pyproject / bin 未加 --with mcp | 确认使用 >= 0.1.3 版本（含 pyproject）或临时在 bin 加 `--with mcp` |
| MCP error -32000: Connection closed | 进程启动即崩溃 | 查看 npx 输出 stderr；先本地 `uv run ...` |
| 没有列出工具 | FastMCP 未成功 register | 检查工具注册代码；启动加 debug 输出 |
| 权限错误 (macOS) | bin 没有执行权限 | `chmod +x bin/mcp-server.js` |
| 冷启动慢 | 首次安装依赖 | 复用 uv 缓存；后续会加依赖瘦身/预构建 |

---

## 🧭 路线图 (Roadmap)

- 核心
  - [ ] 结构化日志（JSON line）
  - [ ] 健康检查 `--health` / `--version`
  - [ ] 错误分级与 AI 可读提示
- 架构生成
  - [ ] 添加 iOS 模板
  - [ ] 添加 Flutter 模板
  - [ ] 添加 React Native 模板
  - [ ] 自定义模板插件（用户仓库引用）
- AI 协作
  - [ ] 记忆：生成历史 → 召回
  - [ ] 学习：输入设计文档 → 提取结构建议
  - [ ] 多工具组合执行
- 生态
  - [ ] VS Code MCP 文档示例
  - [ ] GitHub Action 自动发布 + 兼容测试
  - [ ] 版本变更日志自动生成
- 性能 / 可靠性
  - [ ] 并发请求队列
  - [ ] 任务进度回传（流式）
  - [ ] 生成后验证（lint / compile probe）

> 欢迎通过 Issue / PR 添加建议。后续会维护一个 `CHANGELOG.md`。

---

## 📐 版本与发布

遵循 SemVer：
- 0.x：快速迭代期（可能有破坏性更新）
- 1.0 起：稳定工具接口（向后兼容）

发布流程（维护者）：
```bash
# 确保 pyproject / package.json 同步
npm version patch        # 或 minor / major
npm publish
git tag v$(node -p "require('./package.json').version")
git push origin --tags
```

---

## 🤝 贡献指南（简要）

1. Fork & 新建分支：`feat/<topic>` / `fix/<topic>`
2. 添加/更新相关工具注册 & 文档
3. 若新增依赖：只改 `pyproject.toml`（不要硬写 bin）
4. 本地跑：`uv run src/mcp_architecture_generate.py`
5. 提交 PR：附使用示例 / 截图 / 工具描述更新建议

> 后续会补充 `CONTRIBUTING.md` & `CODE_OF_CONDUCT.md`。

---

## 🧾 许可证

MIT（暂定，如有调整会在此注明）

---

## 🛰️ 未来愿景

DevPilot 会向“AI 可编排的本地开发助手层”演进：  
不仅生成骨架，还能：
- 分析现有仓库 → 推导模块划分
- 生成/更新依赖图与架构文档
- 维护项目知识记忆（变更意图 / 设计决策）
- 引导 AI 在一个“可控范围”内安全修改工程

---

## 🔍 状态标记输出（建议）
启动成功后建议在 stdout 输出一行：
```
READY service=devpilot version=0.1.3 tools=architecture_generate
```
方便上游检测是否握手前崩溃。

---

## 🧪 示例 Prompt 集（可复制）

```
使用 DevPilot 生成一个 Flutter 项目，项目名 DemoApp，包含 domain + data 层。
```

```
Generate an Android clean architecture project named CleanShop with domain, data, and usecase layers.
```

```
使用 DevPilot 重构刚才生成的目录：再添加一个 analytics 模块目录。
```

---

## 🗂️ 相关文件（建议应当存在）
| 文件 | 作用 |
|------|------|
| `pyproject.toml` | Python 依赖声明 |
| `uv.lock` | 可重现锁定（可选） |
| `bin/mcp-server.js` | npm 启动入口 |
| `src/mcp_architecture_generate.py` | 工具实现 |
| `README.md` | 文档 |
| `LICENSE` | 许可 |
| （未来）`CHANGELOG.md` | 版本追踪 |
| （未来）`CONTRIBUTING.md` | 贡献说明 |

---

> 如果你第一次使用 MCP，可先用官方 Inspector 测试：  
> `npx @modelcontextprotocol/inspector npx -y devpilot-mcp@latest`

---

如你有：  
1. 新的架构模式想法  
2. 更复杂的生成参数需求（如 module variants / platform adapters）  
3. 融合 AI 模型（解释生成决策） 的需求  
欢迎反馈 Issue！

—— Happy Building with DevPilot 🚀