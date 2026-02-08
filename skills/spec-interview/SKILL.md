---
name: spec-interview
description: "Generate project spec through structured interview. Use when user has a vague idea and needs help clarifying requirements. Keywords: interview, spec, 需求, 规格, interview me, build a spec, 访谈, 生成需求"
---

# Spec Interview

Transform vague ideas into executable project specifications through structured interview.

## When to Use

- User says "interview me" or "help me clarify requirements"
- User has a rough idea but no clear spec
- Starting a personal project, tool, or prototype
- User wants to avoid over-engineering before knowing what they want

## Interview Flow

```
INIT → WHY (1-2) → WHO/WHEN (1-2) → SCOPE (2-3) → HOW (0-2) → SPEC → VALIDATE
```

Target: **5-8 questions total**, never exceed 12.

## Phase Rules

### Phase 1: INIT (1 question)

Determine project type to adjust subsequent questions:

```yaml
question: "这个项目最接近哪种类型？"
header: "项目类型"
options:
  - label: "个人工具"
    description: "自己用，解决具体痛点"
  - label: "技术验证"
    description: "验证某个技术方案是否可行"
  - label: "产品原型"
    description: "可能给别人用，需要考虑体验"
  - label: "开源项目"
    description: "公开发布，需要文档和可维护性"
```

### Phase 2: WHY (1-2 questions)

**Goal**: Establish existence reason.

First question (open-ended, no AskUserQuestion):
> "这个项目要解决什么具体问题？现在有什么痛点？"

If answer is vague, follow up:
```yaml
question: "做完后，什么情况说明它成功了？"
header: "成功标准"
options:
  - label: "自己用起来了"
  - label: "替代了现有工具"
  - label: "别人也愿意用"
  - label: "学到了想学的东西"
```

### Phase 3: WHO/WHEN (1-2 questions)

**Goal**: Establish usage context.

```yaml
question: "预计多久用一次？"
header: "使用频率"
options:
  - label: "每天多次"
    description: "需要极致效率"
  - label: "每天一次"
    description: "需要稳定可靠"
  - label: "每周几次"
    description: "可以有些手动步骤"
  - label: "偶尔用"
    description: "能用就行"
```

Skip if project_type == "技术验证".

### Phase 4: SCOPE (2-3 questions)

**Goal**: Prevent scope creep.

```yaml
question: "第一版必须包含的核心功能是？"
header: "核心功能"
# Generate options based on previous answers
```

```yaml
question: "以下哪些可以明确第一版不做？"
header: "明确不做"
multiSelect: true
# Generate options based on project type
```

### Phase 5: HOW (0-2 questions)

**Goal**: Engineering decisions. Only ask if not already clear.

```yaml
question: "主要在什么环境下用？"
header: "使用环境"
options:
  - label: "终端/命令行"
  - label: "IDE/编辑器"
  - label: "浏览器"
  - label: "移动端"
```

## Convergence Rules

**Stop interviewing when ANY of these are true:**

1. User says "够了" or "开始吧"
2. All phases complete with no ambiguity
3. Question count reaches 8
4. User chooses "其他" 3 times consecutively → switch to open-ended

**Convergence test**: Can you complete this sentence?
> "这是一个给 [谁] 用、在 [场景] 下、解决 [问题] 的 [形态] 工具，第一版只做 [X]"

If yes, stop interviewing.

## Edge Case Handling

| Situation | Action |
|-----------|--------|
| User mentions tech details in WHY phase | Record as `pending_decision`, revisit in HOW |
| User says "你决定" | Provide recommendation with rationale, ask to confirm |
| User wants to change previous answer | Allow with `revise:` prefix |
| User gives very detailed answer | Skip related questions, extract decisions |

## Spec Output Format

After interview, generate:

```markdown
# [项目名称] Spec

## 一句话描述
给 [谁] 在 [场景] 解决 [问题] 的 [形态] 工具

## 背景与动机
- 要解决的问题：
- 当前的痛点：
- 成功标准：

## 目标用户与场景
- 用户：
- 使用频率：
- 典型场景：

## 功能范围

### 第一版必须有
- [ ] ...

### 明确不做
- ...

## 技术决策
- 形态：
- 语言/框架：
- 关键依赖：

## 开放问题
- [ ] ...（如有未决定的事项）
```

## Post-Interview Actions

1. Present spec for user review
2. Ask: "需要调整哪里吗？"
3. After confirmation, ask where to save (default: `docs/{project-name}-spec.md`)
4. Ask: "要现在开始实现吗？" If yes, suggest `/plan` with spec reference

## Example Interaction

**User**: 我想做一个管理 dotfiles 的工具

**AI**: 好，让我通过几个问题帮你明确需求。

[AskUserQuestion: 项目类型]

**User**: 个人工具

**AI**: 你想解决什么具体问题？比如现在管理 dotfiles 有什么痛点？

**User**: 多台机器同步麻烦，每次换电脑都要手动搞

[AskUserQuestion: 成功标准 - 因为"同步麻烦"已经暗示了目标]

**User**: 自己用起来了

[AskUserQuestion: 使用频率]

**User**: 每周几次

[AskUserQuestion: 核心功能 - 动态生成选项]
```yaml
options:
  - label: "自动同步到新机器"
  - label: "版本管理/回滚"
  - label: "区分不同环境配置"
  - label: "一键安装依赖软件"
```

**User**: 自动同步到新机器

[AskUserQuestion: 明确不做]
```yaml
multiSelect: true
options:
  - label: "GUI 界面"
  - label: "多用户协作"
  - label: "加密敏感信息"
  - label: "支持 Windows"
```

**User**: [选择 GUI 界面, 多用户协作]

**AI**: 基于我们的讨论，这是生成的 Spec：

[输出 Spec]

需要我调整哪里吗？确认后我会保存到 `docs/dotfiles-manager-spec.md`
