---
name: implement
description: "TDD implementation with per-feature Codex review. Use when you have a tech-plan and want to implement with tests-first methodology plus code review. Keywords: implement, 实现, tdd, develop, coding, 开发"
---

# Implement

TDD-driven implementation workflow with per-feature Codex code review. Combines test-first development with automated review feedback.

## When to Use

- Have a tech-plan ready (from `/tech-design` or manual)
- Want TDD methodology enforced
- Want code review feedback during development
- Implementing multiple related features

## When NOT to Use

- Quick one-line fixes
- Exploratory coding / prototyping
- No clear implementation plan yet → use `/tech-design` first

## Workflow

```
INPUT (tech-plan)
    ↓
TASK_BREAKDOWN
    ↓
┌─────────────────────────────────┐
│  FOR EACH TASK:                 │
│    ↓                            │
│  TDD_CYCLE                      │
│    ├── RED: Write failing test  │
│    ├── GREEN: Minimal impl      │
│    ├── REFACTOR: Clean up       │
│    └── VERIFY: Tests pass       │
│    ↓                            │
│  CODE_REVIEW (Codex)            │
│    ↓                            │
│  REVIEW_ACTION                  │
│    ├── Show P1/P2/P3 issues     │
│    ├── User picks what to fix   │
│    └── Fix selected items       │
│    ↓                            │
│  NEXT TASK                      │
└─────────────────────────────────┘
    ↓
FINAL_SUMMARY
    ↓
DONE
```

## Phase Details

### Phase 1: INPUT

Accept tech-plan from:
1. File path: `/implement --plan docs/xxx-tech-plan.md`
2. Direct input: `/implement [description]`
3. Previous conversation context

If no tech-plan provided:
> "请提供技术方案文件路径，或直接描述要实现的功能"

### Phase 2: TASK_BREAKDOWN

Extract implementation tasks from tech-plan:

```markdown
## 任务拆分

从技术方案中提取以下任务：

1. [ ] **Task 1**: [描述]
   - 文件: path/to/file.go
   - 类型: 新增/修改

2. [ ] **Task 2**: [描述]
   - 文件: path/to/another.go
   - 类型: 新增/修改

确认任务列表？可以调整顺序或拆分/合并。
```

Wait for user confirmation before proceeding.

### Phase 3: TDD_CYCLE (Per Task)

For each task, follow strict TDD:

#### Step 1: RED - Write Failing Test

```markdown
## Task N: [名称]

### Step 1: 写测试 (RED)

我要先写测试。测试文件: `path/to/file_test.go`

[写测试代码]

运行测试确认失败...
```

```bash
go test ./path/to/... -run TestXxx -v
# 或
npm test -- --testNamePattern="xxx"
```

**Must see test FAIL before proceeding.**

#### Step 2: GREEN - Minimal Implementation

```markdown
### Step 2: 实现 (GREEN)

写最小实现让测试通过：

[写实现代码]

运行测试确认通过...
```

```bash
go test ./path/to/... -run TestXxx -v
```

**Must see test PASS before proceeding.**

#### Step 3: REFACTOR - Clean Up

```markdown
### Step 3: 重构 (REFACTOR)

检查是否需要重构：
- [ ] 命名是否清晰
- [ ] 是否有重复代码
- [ ] 错误处理是否完善

[如有重构，展示改动]

再次运行测试确认仍然通过...
```

#### Step 4: VERIFY - All Tests Pass

```bash
# 运行相关测试
go test ./path/to/... -v

# 检查覆盖率（可选）
go test ./path/to/... -cover
```

### Phase 4: CODE_REVIEW (Per Task)

After each task's TDD cycle, invoke Codex review:

```markdown
## Code Review: Task N

正在发送到 Codex 进行 review...
```

**Review Request Format:**

```markdown
## Code Review Request

### Summary
实现 [功能描述]

### Changed Files
[git diff --stat for this task's changes]

### Key Changes
- [bullet points]

---

### Review Instructions
Focus on:
- Security: credentials, injection, auth bypass
- Correctness: logic errors, edge cases
- Performance: inefficient patterns
- Maintainability: complexity, readability

Output as P1 (must fix) / P2 (should fix) / P3 (consider).
```

**Send to Codex:**

```bash
cat > /tmp/codex-review.md << 'EOF'
[formatted request]
EOF
codex exec < /tmp/codex-review.md
```

### Phase 5: REVIEW_ACTION

Present review results and let user decide:

```markdown
## Codex Review 结果

### P1 - 必须修复
- [ ] Issue 1: [描述] (file:line)
- [ ] Issue 2: [描述] (file:line)

### P2 - 建议修复
- [ ] Issue 3: [描述]
- [ ] Issue 4: [描述]

### P3 - 可选优化
- [ ] Issue 5: [描述]

---

请选择要修复的项（输入编号，如 "1,2,3" 或 "all P1" 或 "skip"）：
```

**User options:**
- `1,2,3` - Fix specific items
- `all P1` / `all P2` - Fix all items of priority
- `all` - Fix everything
- `skip` - Continue to next task
- `stop` - Stop implementation

**After fixing:**
- Re-run tests to ensure fixes don't break anything
- If user fixed items, do NOT re-review (avoid infinite loop)

### Phase 6: NEXT_TASK

```markdown
---

✅ Task N 完成

进度: [N/Total]
- [x] Task 1
- [x] Task 2
- [ ] Task 3 ← 下一个

继续下一个任务？(y/n/调整)
```

### Phase 7: FINAL_SUMMARY

After all tasks complete:

```markdown
## 实现完成

### 完成的任务
- [x] Task 1: [描述]
- [x] Task 2: [描述]
- [x] Task 3: [描述]

### 新增/修改文件
| 文件 | 改动类型 | 测试覆盖 |
|------|---------|---------|
| services/xxx.go | 新增 | ✅ |
| services/xxx_test.go | 新增 | - |

### Review 修复统计
- P1 修复: 3
- P2 修复: 5
- P3 跳过: 2

### 下一步
- [ ] 运行完整测试: `go test ./...`
- [ ] 检查覆盖率: `go test ./... -cover`
- [ ] 提交代码: `git add . && git commit`
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Test won't pass after 3 attempts | Stop, ask user for help |
| Codex review times out | Skip review, warn user |
| User wants to modify task order | Allow reordering |
| User wants to add new task mid-way | Allow, update task list |
| User wants to skip a task | Mark as skipped, continue |

## TDD Best Practices Enforced

1. **Test First**: Never write implementation before test
2. **One Thing at a Time**: Each test tests one behavior
3. **Minimal Implementation**: Only code needed to pass test
4. **Refactor with Safety Net**: Tests must pass before and after
5. **No Skipping Tests**: Every public function needs tests

## Test Quality Checklist (Per Task)

Before marking task complete:
- [ ] Test describes expected behavior
- [ ] Test covers happy path
- [ ] Test covers error cases
- [ ] Test is independent (no shared state)
- [ ] Implementation is minimal

## Integration with Other Skills

```
/spec-interview → docs/xxx-spec.md
        ↓
/tech-design → docs/xxx-tech-plan.md
        ↓
/implement → code + tests + review
        ↓
git commit
```

## Example Interaction

**User**: /implement --plan docs/order-notify-tech-plan.md

**AI**:
```
读取技术方案...

## 任务拆分

1. [ ] NotifyService 基础结构
   - 新增: services/notify/service.go

2. [ ] MQ Producer 集成
   - 修改: services/order/create.go

3. [ ] 错误处理和重试
   - 修改: services/notify/service.go

确认开始？
```

**User**: 确认

**AI**:
```
## Task 1: NotifyService 基础结构

### Step 1: 写测试 (RED)

创建测试文件 services/notify/service_test.go:
```

[写测试]

```
运行测试...
FAIL - NotifyService not found (符合预期)

### Step 2: 实现 (GREEN)

创建 services/notify/service.go:
```

[写实现]

```
运行测试...
PASS

### Step 3: 重构

检查代码... 暂无需重构。

---

正在发送到 Codex review...

## Codex Review 结果

### P1 - 必须修复
- [ ] 1. 缺少 context 参数 (service.go:15)

### P2 - 建议修复
- [ ] 2. 建议添加 metrics (service.go:20)

### P3 - 可选
- [ ] 3. 可以用 sync.Pool 优化

请选择要修复的项：
```

**User**: 1

**AI**:
```
修复 P1 #1: 添加 context 参数...

[修改代码]

运行测试确认通过... PASS

---

✅ Task 1 完成

进度: [1/3]

继续 Task 2？
```
