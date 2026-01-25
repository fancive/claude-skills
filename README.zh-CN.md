# Claude Extensions

Claude Code 自定义扩展集合：Skills、Agents、Plugins。

## 概念区分

| 类型 | 用途 | 上下文 | 触发方式 |
|------|------|--------|----------|
| **Skill** | 主窗口内执行的任务流程 | 占用主窗口上下文 | `/skill-name` |
| **Agent** | 后台子进程，独立上下文 | 不占用主窗口 | `Task(subagent_type)` 或关键词触发 |
| **Plugin** | 提供 MCP servers、hooks 等 | 取决于实现 | 自动加载 |

### 何时用 Skill vs Agent

- **Skill**: 需要用户交互、查看中间过程、`/skill-name` 触发
- **Agent**: 后台子进程执行，独立上下文，通过 `Task` 工具调用

### Agent YAML Frontmatter（必须）

Agent 文件必须包含 YAML frontmatter 才能被 `Task` 工具识别：

```yaml
---
name: my-agent          # Task(subagent_type: "my-agent")
description: "描述和关键词..."
model: inherit          # 或指定 sonnet/opus/haiku
---
```

## 安装

```bash
# 克隆仓库
git clone https://github.com/fancive/claude-skills.git
cd claude-skills

# 安装 skill（符号链接方式）
ln -sf $(pwd)/skills/reflect ~/.claude/skills/reflect

# 安装 agent（符号链接方式）
ln -sf $(pwd)/agents/code-reviewer/agent.md ~/.claude/agents/code-reviewer.md

# 安装 plugin（按 plugin 说明操作）
```

## Commands

Commands 是用户入口，调用对应的 agents。

| 命令 | Agent | 用途 |
|------|-------|------|
| `/plan` | planner | 实现规划 |
| `/architect` | architect | 系统设计、ADR |
| `/tdd` | tdd-guide | 测试驱动开发 |
| `/cr` | code-reviewer | Codex 代码审查 |
| `/investigate` | codebase-investigator | 代码库分析 |
| `/refactor-clean` | refactor-cleaner | 死代码清理 (Python/Go/JS/TS) |
| `/update-codemaps` | codemap-updater | 生成架构文档 |
| `/e2e` | e2e-browser | 通过 Claude in Chrome 进行浏览器 E2E 测试 |

### 安装

```bash
ln -sf $(pwd)/commands/plan.md ~/.claude/commands/plan.md
ln -sf $(pwd)/commands/architect.md ~/.claude/commands/architect.md
ln -sf $(pwd)/commands/tdd.md ~/.claude/commands/tdd.md
ln -sf $(pwd)/commands/cr.md ~/.claude/commands/cr.md
ln -sf $(pwd)/commands/investigate.md ~/.claude/commands/investigate.md
ln -sf $(pwd)/commands/refactor-clean.md ~/.claude/commands/refactor-clean.md
ln -sf $(pwd)/commands/update-codemaps.md ~/.claude/commands/update-codemaps.md
ln -sf $(pwd)/commands/e2e.md ~/.claude/commands/e2e.md
```

## Skills

### reflect

从对话中提取可复用的工程规则，实现 "Correct once, never again"。

```bash
/reflect                # 分析对话，提取规则
/reflect --dry-run      # 预览不修改
/reflect --global       # 存入全局规则
/reflect --project      # 存入项目规则
```

详见 [skills/reflect/SKILL.md](skills/reflect/SKILL.md)

## Agents

### code-reviewer

将代码改动发送给 OpenAI Codex 进行 review，返回精简的 P1/P2/P3 级别反馈。

**触发方式**：
- 关键词触发：`review my code`, `codex review`, `code review`
- 直接调用：`Task(subagent_type: "code-reviewer")`

**工作流程**（在独立子进程中执行）：
1. 收集 git diff
2. 格式化 review 请求写入临时文件
3. 调用 `codex exec` 发送给 Codex
4. 返回 P1/P2/P3 结构化反馈

**优势**：不占用主窗口上下文，中间过程在后台完成。

详见 [agents/code-reviewer/agent.md](agents/code-reviewer/agent.md)

### codebase-investigator

只读代码库分析：搜索文件、追踪依赖、理解架构、生成文档。

**触发方式**：
- 关键词触发：`investigate`, `analyze`, `trace`, `how does`, `where is`, `find code`
- 直接调用：`Task(subagent_type: "codebase-investigator")`

**输出**：在 `notes/` 目录生成结构化的分析报告（Markdown）。

详见 [agents/codebase-investigator/agent.md](agents/codebase-investigator/agent.md)

### planner

复杂功能和重构的实现规划专家。

**触发方式**：
- 关键词触发：`plan`, `implementation`, `feature planning`, `refactor planning`
- 直接调用：`Task(subagent_type: "planner")`

**输出**：结构化实现计划，包含阶段、步骤、风险和成功标准。

详见 [agents/planner/agent.md](agents/planner/agent.md)

### architect

系统设计和技术决策的软件架构专家。

**触发方式**：
- 关键词触发：`architecture`, `system design`, `scalability`, `technical decision`
- 直接调用：`Task(subagent_type: "architect")`

**输出**：架构决策记录（ADR）、设计提案、权衡分析。

详见 [agents/architect/agent.md](agents/architect/agent.md)

### tdd-guide

强制测试先行的 TDD 专家。

**触发方式**：
- 关键词触发：`TDD`, `test first`, `write tests`, `test coverage`
- 直接调用：`Task(subagent_type: "tdd-guide")`

**能力**：可以编写代码（有 Write, Edit, Bash 工具）。强制 Red-Green-Refactor 循环，确保 80%+ 覆盖率。

详见 [agents/tdd-guide/agent.md](agents/tdd-guide/agent.md)

### refactor-cleaner

多语言死代码检测和清理。

**支持语言**：
- Python: vulture, dead, autoflake
- Go: deadcode, staticcheck, go mod tidy
- JS/TS: knip, depcheck, ts-prune

**触发方式**：
- 关键词触发：`refactor`, `clean`, `dead code`, `unused`
- 直接调用：`Task(subagent_type: "refactor-cleaner")`

**安全性**：每次删除前后运行测试，失败自动回滚。

详见 [agents/refactor-cleaner/agent.md](agents/refactor-cleaner/agent.md)

### codemap-updater

从代码库分析生成高效的架构文档。

**输出**：
```
codemaps/
├── architecture.md   # 整体结构
├── backend.md        # API 路由、服务
├── frontend.md       # 页面、组件
└── data.md           # 数据模型
```

**触发方式**：
- 关键词触发：`codemap`, `architecture`, `documentation`
- 直接调用：`Task(subagent_type: "codemap-updater")`

**特性**：多语言支持 (Go, Python, JS/TS, Rust)，差异检测，时间戳。

详见 [agents/codemap-updater/agent.md](agents/codemap-updater/agent.md)

### e2e-browser

使用 Claude in Chrome 进行真实浏览器 E2E 测试。

**前置条件**：
- 安装并连接 Claude in Chrome MCP 扩展

**触发方式**：
- 关键词触发：`e2e`, `test`, `browser`, `chrome`, `visual`
- 直接调用：`Task(subagent_type: "e2e-browser")`

**能力**：
- 导航到 URL、点击元素、填写表单
- 每步截图
- 录制测试流程为 GIF
- 验证页面内容和元素状态
- 生成测试报告

**用法**：
```bash
/e2e test login flow on https://example.com
/e2e verify search works on current page
/e2e record checkout flow with GIF
```

详见 [agents/e2e-browser/agent.md](agents/e2e-browser/agent.md)

## Plugins

*Coming soon*

## 目录结构

```
claude-skills/
├── commands/
│   ├── plan.md
│   ├── architect.md
│   ├── tdd.md
│   ├── cr.md
│   ├── investigate.md
│   ├── refactor-clean.md
│   ├── update-codemaps.md
│   └── e2e.md
├── skills/
│   └── reflect/
│       └── SKILL.md
├── agents/
│   ├── architect/
│   │   └── agent.md
│   ├── code-reviewer/
│   │   └── agent.md
│   ├── codebase-investigator/
│   │   └── agent.md
│   ├── planner/
│   │   └── agent.md
│   ├── tdd-guide/
│   │   └── agent.md
│   ├── refactor-cleaner/
│   │   └── agent.md
│   ├── codemap-updater/
│   │   └── agent.md
│   └── e2e-browser/
│       └── agent.md
├── plugins/
│   └── (future)
├── templates/
│   ├── learned-rules.md
│   └── reflect-log.md
└── README.md
```

## 添加新扩展

### 添加 Skill

1. 创建目录 `skills/{name}/`
2. 添加 `SKILL.md`（参考 reflect 格式）
3. 创建符号链接：`ln -sf $(pwd)/skills/{name} ~/.claude/skills/{name}`
4. 更新本 README

### 添加 Agent

1. 创建目录 `agents/{name}/`
2. 添加 `agent.md`，**必须包含 YAML frontmatter**：
   ```yaml
   ---
   name: {name}
   description: "描述... Keywords: 关键词1, 关键词2"
   model: inherit
   ---
   ```
3. 创建符号链接：`ln -sf $(pwd)/agents/{name}/agent.md ~/.claude/agents/{name}.md`
4. 更新本 README

### 添加 Plugin

*文档待补充*

## License

MIT
