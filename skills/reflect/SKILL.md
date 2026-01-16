---
name: reflect
description: "Analyze conversation to extract reusable engineering rules. Use when user says 'reflect', 'remember this', 'learn from this', or after receiving corrections/feedback."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[--dry-run] [--scope frontend|backend|api|security] [--global|--project] [--review]"
---

# Reflect Skill

把对话中的纠正、确认、偏好提取为可复用的工程规则。

**核心理念**: Correct once, never again.

---

## 两阶段工作流

借鉴 build-insights-logger 的设计，采用低干扰的两阶段流程：

### Phase 1: 自动捕获 (Passive Logging)

在正常对话中，**自动检测**纠正信号并记录到暂存区：

```
用户: "这里不要用 var，用 const"
Claude: [完成代码修改]
       📝 检测到规则信号: prefer-const (已暂存)
```

**触发条件**（自动检测）：
- 用户使用纠正关键词：不要、别、必须、一定要、never、don't、always、must
- 用户明确表达偏好：用 X 不用 Y、统一用、建议用
- 同类请求出现 3+ 次

**暂存位置**：`.claude/pending-rules.md`

**通知格式**（低干扰）：
```
📝 检测到规则信号: {rule-id} (已暂存)
```

### Phase 2: 用户审查 (Review & Commit)

用户主动调用 `/reflect` 或 `/reflect --review` 时：

1. 读取暂存区 `.claude/pending-rules.md`
2. 合并同类规则
3. 逐条确认（使用 AskUserQuestion）
4. 写入正式规则文件
5. 清空暂存区

---

## 质量标准

规则必须满足（借鉴 build-insights-logger）：

| 标准 | 说明 | 示例 |
|------|------|------|
| **Non-trivial** | 有实际价值，非显而易见 | ✓ "API 错误码用枚举" ✗ "变量要命名" |
| **Actionable** | 可执行的具体指令 | ✓ "用 dayjs 不用 moment" ✗ "代码要好" |
| **Specific** | 针对具体决策 | ✓ "本项目用 Tailwind" ✗ "CSS 要写好" |
| **Contextual** | 有明确的适用场景 | ✓ "scope: frontend" ✗ "所有代码" |

**自动过滤**：
- 跳过：语法纠正、拼写错误、格式调整
- 跳过：一次性的临时决策
- 跳过：过于宽泛的建议

---

## Storage Scope (存储范围)

```
~/.claude/
├── learned-rules.md          # 全局规则（跨项目通用）
└── reflect-log.md            # 全局变更日志

./项目/.claude/
├── learned-rules.md          # 项目专属规则（优先级更高）
├── pending-rules.md          # 暂存区（待审查）
└── reflect-log.md            # 项目变更日志
```

### 存储建议

| 规则类型 | 建议存储 | 示例 |
|----------|----------|------|
| 安全规范 | 🌍 全局 | SQL 注入防护、密钥管理 |
| 代码风格通用 | 🌍 全局 | 命名规范、注释风格 |
| 框架/库偏好 | 📁 项目 | "本项目用 Redux 不用 MobX" |
| 业务逻辑约定 | 📁 项目 | "订单状态必须用枚举" |
| 团队特定流程 | 📁 项目 | "PR 必须关联 JIRA" |

---

## Signal Types (信号类型)

### 1. Corrections (纠正) - 最高价值
**关键词**: 不要、别、永远不要、必须、一定要、never、don't、always、must

```
"SQL 这里必须用参数化查询" → High confidence
"不要用 inline styles" → High confidence
```

### 2. Preferences (偏好) - 中等价值
**关键词**: 用 X 不用 Y、统一用、建议、prefer、should

```
"用 dayjs 不用 moment" → Medium confidence
"组件命名用 PascalCase" → Medium confidence
```

### 3. Patterns (模式) - 观察
**判断**: 同类请求出现 3+ 次

```
用户连续 3 次要求添加 loading 状态 → Low confidence
```

### 4. Approvals (确认) - 强化
**关键词**: 对的、很好、就这样、correct、perfect

用于：提升现有规则置信度

---

## Workflow

### 自动捕获流程

```
1. 检测到纠正信号
2. 评估质量标准 (Non-trivial? Actionable? Specific?)
3. 通过 → 写入 .claude/pending-rules.md
4. 输出: 📝 检测到规则信号: {rule-id} (已暂存)
5. 继续正常对话（不打断）
```

### 审查流程 (`/reflect` 或 `/reflect --review`)

```
1. 读取 ~/.claude/learned-rules.md（全局）
2. 读取 ./.claude/learned-rules.md（项目，如存在）
3. 读取 ./.claude/pending-rules.md（暂存区）
4. 合并同类规则，去重
5. 对每条规则调用 AskUserQuestion 确认
6. 根据用户选择写入对应文件
7. 清空暂存区
8. 写入 reflect-log.md
```

---

## 暂存区格式

`.claude/pending-rules.md`:

```markdown
# Pending Rules (待审查)

## 2024-01-16 14:30
- signal: "不要用 var，用 const"
- suggested-id: js-prefer-const
- scope: frontend
- confidence: high
- constraint: Use const/let instead of var

## 2024-01-16 15:45
- signal: "API 响应统一用 camelCase"
- suggested-id: api-response-camelcase
- scope: api
- confidence: medium
- constraint: Use camelCase for API response fields
```

---

## 交互式确认

**重要：先问后写，不要先展示 diff**

错误示范（看起来像已写入）：
```diff
+ ### some-rule
+ - scope: ...
```
然后问确认 ← 用户会以为已经写入了

正确流程：
1. 展示检测到的信号（纯文本描述）
2. 调用 AskUserQuestion 确认
3. **用户确认后**才展示写入结果

使用 `AskUserQuestion` 逐条确认：

```yaml
question: "规则: {rule-id}\n{constraint}\n\n来源: \"{original-signal}\"\n\n如何处理？"
header: "{rule-id}"
options:
  - label: "存入项目 (推荐)"
    description: "写入 ./.claude/learned-rules.md"
  - label: "存入全局"
    description: "写入 ~/.claude/learned-rules.md"
  - label: "跳过"
    description: "不保存，从暂存区移除"
```

**确认后的输出**：
- 选择存入 → `✓ 已写入 {path}`，然后展示 diff
- 选择跳过 → `⊘ 已跳过`，不展示 diff

---

## Rule Format

写入 `learned-rules.md` 的规则格式：

```markdown
### {rule-id}
- scope: {frontend|backend|api|security|testing|general}
- confidence: {high|medium|low}
- constraint: {给 Claude 的明确指令，祈使句}
- rationale: {为什么存在这条规则}
- added: {date}
- confirmations: {number}
```

---

## Usage Examples

### Example 1: 自动捕获 + 审查

```
User: "这里不要用 moment，用 dayjs，体积小"
Claude: [修改代码，替换为 dayjs]
        📝 检测到规则信号: use-dayjs-not-moment (已暂存)

... 继续其他工作 ...

User: /reflect

Claude:
检测到 1 条待审查规则:
  - use-dayjs-not-moment: 用 dayjs 替代 moment（体积更小）

→ 调用 AskUserQuestion（不展示 diff，只展示描述）:
  规则: use-dayjs-not-moment
  Use dayjs instead of moment for date handling (smaller bundle size)

  来源: "不要用 moment，用 dayjs，体积小"

  ○ 存入项目 (推荐)
  ○ 存入全局
  ○ 跳过

用户选择 "存入项目"

Claude:
✓ 已写入 ./.claude/learned-rules.md
```diff
+ ### use-dayjs-not-moment
+ - scope: frontend
+ - confidence: medium
+ - constraint: Use dayjs instead of moment for date handling
```
```

### Example 2: 批量审查

```
User: /reflect --review

Claude:
暂存区有 3 条待审查规则:

1/3: use-dayjs-not-moment
     → 用户选择: 存入项目

2/3: api-error-enum
     → 用户选择: 存入项目

3/3: css-no-important
     → 用户选择: 跳过

✓ 2 条规则已写入，1 条已跳过
```

### Example 3: 直接分析（无暂存）

```
User: /reflect

Claude:
暂存区为空，正在扫描当前对话...

检测到 1 条信号:
[CORRECTION] "必须用 TypeScript 的严格模式"

→ 调用 AskUserQuestion 确认...
```

### Example 4: Dry Run

```
/reflect --dry-run

输出所有检测到的信号，但不修改任何文件
```

---

## Safety Rules

1. **自动捕获只暂存，不直接写入** - 所有规则必须经过用户确认
2. **永不自动删除规则** - 只能人工 deprecate
3. **总是显示来源** - 让用户知道规则从哪句话提取
4. **变更必须可追溯** - 写入 reflect-log.md
5. **低干扰原则** - 自动捕获只输出一行提示，不打断工作流

---

## Files

**全局级 (跨项目)**
- `~/.claude/learned-rules.md` - 全局规则存储
- `~/.claude/reflect-log.md` - 全局变更日志

**项目级 (Git 跟踪)**
- `./.claude/learned-rules.md` - 项目规则存储
- `./.claude/pending-rules.md` - 暂存区（待审查）
- `./.claude/reflect-log.md` - 项目变更日志

---

## Notes

- 自动捕获是**被动的**，不会主动询问，只在检测到信号时暂存
- 暂存区的规则不会影响 Claude 行为，只有正式规则才会
- 全局规则存在 home 目录，不受 Git 管理
- 项目规则建议 `git commit` 后共享给团队
- 同 ID 规则冲突时，项目级优先
