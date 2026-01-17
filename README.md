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

## Plugins

*Coming soon*

## 目录结构

```
claude-skills/
├── skills/
│   └── reflect/
│       └── SKILL.md
├── agents/
│   └── code-reviewer/
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
