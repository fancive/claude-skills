---
name: tech-design
description: "Generate technical design through structured interview for iterative development. Use when user has a spec/requirement and needs to make technical decisions before coding. Keywords: tech design, 技术方案, technical plan, how to implement, 怎么实现, architecture decision"
---

# Tech Design Interview

Generate technical design for iterative development through structured interview. Focuses on **existing codebase changes**, not greenfield projects.

## When to Use

- User has a spec/requirement and asks "how to implement"
- Multiple valid technical approaches exist
- Changes affect existing codebase
- Need to make architecture/design decisions before coding

## When NOT to Use

- Simple bug fixes (just do it)
- User already knows exactly how to implement
- Greenfield project needing tech stack selection → use `/plan` directly

## Interview Flow

```
INPUT → FAMILIARITY → CODEBASE_SCAN → BEHAVIOR_CONFIRM → CONSTRAINTS → DECISIONS → TECH_PLAN
```

Target: **5-10 questions total**.

## Phase Rules

### Phase 0: INPUT

Confirm the requirement source:

```
我需要了解要实现的需求。请提供：
1. Spec 文件路径（如 docs/xxx-spec.md）
2. 或直接描述需求

[如果有 spec 文件，读取并总结关键点]
```

### Phase 1: FAMILIARITY (1 question)

Determine exploration strategy:

```yaml
question: "你对这块代码的熟悉程度？"
header: "代码熟悉度"
options:
  - label: "很熟，我知道改哪"
    description: "直接告诉我文件/函数名"
  - label: "大概知道模块"
    description: "我帮你定位具体位置"
  - label: "完全不熟"
    description: "我先探索代码库"
```

**Based on answer**:
- "很熟" → Ask user for entry points, skip to BEHAVIOR_CONFIRM
- "大概知道" → User gives module hint, AI locates specifics
- "完全不熟" → AI explores with Grep/Glob, confirms with user

### Phase 2: CODEBASE_SCAN

**AI actions** (not questions):

1. Search for relevant code using keywords from requirement
2. Trace call chains from entry points
3. Identify existing patterns that can be reused
4. Find similar implementations for reference

**Output format**:

```markdown
## 代码扫描结果

### 涉及文件
- path/to/file.go:123 - FunctionName() - 简述
- path/to/another.go - 相关逻辑

### 调用链
Entry → Service → DAO → External

### 可复用代码
- pkg/notify/sender.go - 现有通知发送逻辑
- pkg/queue/producer.go - MQ 生产者封装

### 现有模式
- 异步任务用 [X] 方式
- 错误处理用 [Y] 模式
```

Then ask:
> "以上是我找到的相关代码，有遗漏吗？"

### Phase 3: BEHAVIOR_CONFIRM (1-2 questions)

**Goal**: Prevent documentation vs reality mismatch.

```yaml
question: "现有行为是否符合你的理解？"
header: "行为确认"
options:
  - label: "符合"
    description: "继续"
  - label: "有出入"
    description: "告诉我实际情况"
  - label: "不确定"
    description: "需要一起验证"
```

If discrepancy found → clarify before proceeding.

Optional follow-up:
> "有哪些是历史遗留行为，这次绝对不能动的？"

### Phase 4: CONSTRAINTS (1-2 questions)

**Goal**: Lock the solution space.

```yaml
question: "这次改动有哪些硬约束？"
header: "硬约束"
multiSelect: true
options:
  - label: "不能改现有 API 签名"
    description: "有外部调用方"
  - label: "不能改表结构"
    description: "需要 DBA 审批/数据迁移"
  - label: "不能加新依赖"
    description: "需要安全审批"
  - label: "必须向后兼容"
    description: "老版本还在用"
  - label: "不能影响现有功能"
    description: "这块代码很脆弱"
  - label: "没有特殊约束"
```

### Phase 5: DECISIONS (2-4 questions)

**Goal**: Make key technical decisions. Questions are dynamic based on requirement.

#### Common Decision Points

**Implementation approach**:
```yaml
question: "实现方式倾向？"
header: "实现路径"
options:
  - label: "最小改动"
    description: "只改必要的"
  - label: "顺便重构"
    description: "借机改善代码"
  - label: "先重构再加功能"
    description: "现有代码不适合扩展"
  - label: "新写一套"
    description: "Strangler 模式逐步替换"
```

**Sync vs Async** (if applicable):
```yaml
question: "这个操作应该同步还是异步？"
header: "执行方式"
options:
  - label: "同步"
    description: "简单，但阻塞主流程"
  - label: "异步 MQ"
    description: "解耦，需要处理最终一致"
  - label: "异步本地队列"
    description: "折中方案"
  - label: "看情况"
    description: "告诉我具体场景"
```

**Error handling** (if applicable):
```yaml
question: "失败时如何处理？"
header: "错误处理"
options:
  - label: "重试"
    description: "自动重试 N 次"
  - label: "忽略"
    description: "记日志，不影响主流程"
  - label: "回滚"
    description: "整个操作失败"
  - label: "人工介入"
    description: "告警 + 人工处理"
```

**Data storage** (if applicable):
```yaml
question: "数据存在哪里？"
header: "存储选择"
options:
  - label: "现有表加字段"
  - label: "新建表"
  - label: "用现有缓存"
  - label: "不需要持久化"
```

### Phase 6: TECH_PLAN

Generate technical design document.

## Convergence Rules

**Stop interviewing when**:

1. All decision points have clear answers
2. No conflicting choices
3. User says "够了" or "开始吧"
4. Question count reaches 10

**Convergence test**: Can you describe the implementation in one paragraph without "或者"/"可能"?

## Edge Cases

| Situation | Action |
|-----------|--------|
| Scan reveals spec issue | Pause, clarify with user, may need to revise spec |
| Multiple equally good approaches | Present tradeoffs, ask user preference |
| User says "你决定" | Give recommendation with rationale, ask to confirm |
| Constraint makes spec impossible | Stop, explain why, suggest alternatives |

## Output Format

```markdown
# [需求名称] 技术方案

## 需求概述
[1-2 句，来自 spec]

## 代码分析

### 涉及模块
- module1 - 作用
- module2 - 作用

### 可复用代码
- path/to/file.go - 描述

## 技术决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| 同步/异步 | 异步 MQ | 解耦，不阻塞下单 |
| 存储 | 现有表加字段 | 简单，无需迁移 |
| 错误处理 | 重试+告警 | 通知不能丢 |

## 改动计划

### 修改文件
| 文件 | 改动类型 | 说明 |
|------|---------|------|
| services/order.go | 修改 | 添加通知调用 |
| services/notify.go | 新增 | 通知服务 |

### 新增文件
- services/notify.go
- services/notify_test.go

## 影响评估
- 向后兼容：是/否
- 数据迁移：需要/不需要
- 测试覆盖：现有测试 + 新增测试

## 实现步骤
1. [ ] Step 1
2. [ ] Step 2
3. [ ] Step 3

## 风险
- [ ] Risk 1
- [ ] Risk 2

## 开放问题
- [ ] 待定事项（如有）
```

## Post-Interview Actions

1. Present tech plan for review
2. Ask: "需要调整哪里吗？"
3. After confirmation, save to `docs/{name}-tech-plan.md`
4. Ask: "要用 /plan 生成详细执行步骤吗？"

## Integration with Other Skills

```
/spec-interview → docs/xxx-spec.md
        ↓
/tech-design → docs/xxx-tech-plan.md
        ↓
/plan → 执行
```

## Example Interaction

**User**: /tech-design 实现用户下单后发邮件通知，spec 在 docs/order-notify-spec.md

**AI**: [读取 spec]

我已阅读需求，核心是：下单成功后给用户发邮件通知。

```yaml
question: "你对这块代码的熟悉程度？"
# ...
```

**User**: 大概知道，应该在 services/order 目录

**AI**: [扫描代码，输出结果]

我找到以下相关代码：
- services/order/create.go - CreateOrder 主流程
- pkg/notify/email.go - 现有邮件发送（可复用）
- pkg/mq/producer.go - MQ 生产者

有遗漏吗？

**User**: 没有

**AI**:
```yaml
question: "这次改动有哪些硬约束？"
# ...
```

**User**: 不能改现有 API 签名

**AI**:
```yaml
question: "通知应该同步还是异步？"
options:
  - label: "同步"
    description: "简单，下单变慢 ~200ms"
  - label: "异步 MQ"
    description: "用现有 Kafka，解耦"
  - label: "异步本地队列"
    description: "进程内队列，重启丢失"
```

**User**: 异步 MQ

**AI**:
```yaml
question: "发送失败如何处理？"
# ...
```

**User**: 重试 + 告警

**AI**: 基于我们的讨论，生成技术方案：

[输出完整技术方案]

需要调整吗？确认后保存到 `docs/order-notify-tech-plan.md`
