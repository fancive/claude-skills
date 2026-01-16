---
name: reflect
description: "Analyze conversation to extract reusable engineering rules. Use when user says 'reflect', 'remember this', 'learn from this', or after receiving corrections/feedback."
allowed-tools: Read, Write, Edit, Glob, Grep
argument-hint: "[--dry-run] [--scope frontend|backend|api|security] [--global|--project]"
---

# Reflect Skill

把对话中的纠正、确认、偏好提取为可复用的工程规则。

**核心理念**: Correct once, never again.

## Storage Scope (存储范围)

支持混合模式：全局规则 + 项目规则

```
~/.claude/
└── learned-rules.md             # 全局规则（跨项目通用）

./项目/.claude/
└── learned-rules.md             # 项目专属规则（优先级更高）
```

### 加载顺序
1. 读取全局规则 `~/.claude/learned-rules.md`
2. 读取项目规则 `./.claude/learned-rules.md`（如存在）
3. 合并：相同 rule-id 时，项目规则覆盖全局规则

### 写入规则
提取规则后，询问用户存储位置：
- `--global`: 强制写入全局
- `--project`: 强制写入项目
- 无参数: 交互式询问

### 判断建议
| 规则类型 | 建议存储 | 示例 |
|----------|----------|------|
| 安全规范 | 全局 | SQL 注入防护、密钥管理 |
| 代码风格通用 | 全局 | 命名规范、注释风格 |
| 框架/库偏好 | 项目 | "本项目用 Redux 不用 MobX" |
| 业务逻辑约定 | 项目 | "订单状态必须用枚举" |
| 团队特定流程 | 项目 | "PR 必须关联 JIRA" |

## Signal Types (信号类型)

按优先级识别以下信号：

### 1. Corrections (纠正) - 最高价值
**关键词**: 不要、别、永远不要、必须、一定要、never、don't、always、must

示例：
- "SQL 这里必须用参数化查询" → High confidence
- "不要用 inline styles" → High confidence
- "组件命名用 PascalCase" → Medium confidence

### 2. Approvals (确认) - 强化
**关键词**: 对的、很好、就这样、correct、perfect、right

用于：提升现有规则置信度

### 3. Patterns (模式) - 观察
**判断**: 同类请求出现 3+ 次

用于：创建 Low confidence 观察规则

## Workflow

1. **Load existing rules** (merge global + project):
   ```bash
   # 读取顺序
   global_rules = read ~/.claude/learned-rules.md
   project_rules = read ./.claude/learned-rules.md  # if exists
   merged_rules = merge(global_rules, project_rules)  # project wins on conflict
   ```

2. **Scan conversation** for correction/approval/pattern signals

3. **Extract and classify** each signal:
   ```yaml
   signal:
     type: correction | approval | pattern
     quote: "原始用户话语"
     scope: frontend | backend | api | security | testing | general
     confidence: high | medium | low
     storage: global | project | ask  # 建议的存储位置
   ```

4. **Map confidence by keywords**:
   | Keywords | Confidence |
   |----------|------------|
   | 永远、必须、never、always、一定 | high |
   | 尽量、最好、prefer、should、建议 | medium |
   | 可以、考虑、observe、might | low |

5. **Suggest storage location**:
   | 规则特征 | 建议 |
   |----------|------|
   | 安全相关、通用编码规范 | global |
   | 提到"本项目"、框架选型、业务逻辑 | project |
   | 不确定 | ask |

6. **Check existing rules**:
   - If similar rule exists in either location: Consider upgrading confidence
   - If new: Propose new rule with storage location

7. **Format proposed changes** as diff:
   ```diff
   + ### {rule-id}
   + - scope: {scope}
   + - confidence: {confidence}
   + - constraint: {clear instruction}
   + - rationale: {why}
   + - storage: {global|project}  ← 新增
   ```

8. **Apply based on mode**:
   - `--dry-run`: Show only, no changes
   - `--global`: Force all to ~/.claude/learned-rules.md
   - `--project`: Force all to ./.claude/learned-rules.md
   - High confidence: **Always ask for approval + storage location**
   - Medium/Low: Auto-apply to suggested location, notify user

9. **Log changes** to corresponding reflect-log.md

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

## Output Format

```markdown
## Reflect 分析结果

### 当前规则统计
- 全局规则 (~/.claude/): 5 条 (3 high, 2 medium)
- 项目规则 (./.claude/): 3 条 (1 high, 2 low)

### 检测到的信号
1. [CORRECTION] "{原话}" (约第 N 行)
   → scope: backend, confidence: high
   → 建议存储: 🌍 全局 (安全相关)

2. [CORRECTION] "{原话}" (约第 N 行)
   → scope: frontend, confidence: medium
   → 建议存储: 📁 项目 (提到"本项目")

3. [APPROVAL] "{原话}" (约第 N 行)
   → 强化规则: api-error-codes (项目级)

### 建议的规则变更

#### 新增规则

**→ 全局 (~/.claude/learned-rules.md)**
```diff
+ ### security-sql-parameterized
+ - scope: security
+ - confidence: high
+ - constraint: Always use parameterized queries. Never concatenate user input.
+ - rationale: 用户明确指出 SQL 注入风险
```

**→ 项目 (./.claude/learned-rules.md)**
```diff
+ ### frontend-use-antd
+ - scope: frontend
+ - confidence: medium
+ - constraint: Use Ant Design components. Don't introduce other UI libraries.
+ - rationale: 用户说"本项目统一用 antd"
```

#### 置信度提升 (项目级)
```diff
  ### api-error-codes
- - confidence: low
+ - confidence: medium
  - confirmations: 3 → 4
```

---
⚠️ 检测到 1 条 high confidence 规则，需要确认。

security-sql-parameterized:
  [G] 确认存入全局 (推荐)
  [P] 改存项目
  [E] 编辑规则
  [S] 跳过

选择: _
```

## Safety Rules

1. **High confidence 规则必须人工确认** - 防止过度学习单次情绪
2. **永不自动删除规则** - 只能人工 deprecate
3. **总是显示 diff** - 不做静默覆盖
4. **变更必须可追溯** - 写入 reflect-log.md

## Usage Examples

### Example 1: 安全纠正
```
User: "这个 SQL 有注入风险，必须参数化"

/reflect

输出:
检测到: [CORRECTION] "必须参数化"
建议:
  - id: security-sql-parameterized
  - confidence: high (关键词: 必须)

⚠️ High confidence 规则需要确认。应用？ [y/n]
```

### Example 2: 代码风格
```
User: "组件命名用 PascalCase 比较好"

/reflect

输出:
检测到: [APPROVAL] 组件命名偏好
建议:
  - id: frontend-component-naming
  - confidence: medium (关键词: 比较好)

✓ Medium confidence 规则已自动应用
```

### Example 3: Dry Run
```
/reflect --dry-run

输出所有建议但不修改任何文件
```

### Example 4: 指定范围
```
/reflect --scope api

只提取 API 相关的规则
```

## Files

**全局级 (跨项目)**
- `~/.claude/learned-rules.md` - 全局规则存储
- `~/.claude/reflect-log.md` - 全局变更日志

**项目级 (Git 跟踪)**
- `./.claude/learned-rules.md` - 项目规则存储
- `./.claude/reflect-log.md` - 项目变更日志

## Notes

- 全局规则存在 home 目录，不受 Git 管理
- 项目规则存在项目目录，建议 `git commit` 后共享给团队
- 可通过 Stop Hook 实现自动 reflect（谨慎使用）
- 同 ID 规则冲突时，项目级优先
