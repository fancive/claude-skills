# CLI Agent UI 设计规范

> 完整版规范文档，供深入参考

## 目录

1. [设计原则](#设计原则)
2. [颜色系统](#颜色系统)
3. [排版规范](#排版规范)
4. [组件规范](#组件规范)
5. [交互模式](#交互模式)
6. [动画与反馈](#动画与反馈)
7. [键盘交互](#键盘交互)
8. [错误处理](#错误处理)
9. [终端兼容性](#终端兼容性)

---

## 设计原则

### 核心原则

| 原则 | 说明 |
|------|------|
| **键盘优先** | 所有操作必须可通过键盘完成 |
| **实时反馈** | 任何操作都应有即时视觉反馈 |
| **渐进披露** | 简单开始，高级功能可发现 |
| **上下文感知** | 根据当前状态调整 UI |
| **优雅降级** | 在简单终端也能正常工作 |
| **尊重用户** | 不打断、不惊吓、不丢失数据 |

### 与传统 CLI 的区别

```
传统 CLI              CLI Agent
─────────────────────────────────────
命令式                对话式
单次执行              持续会话
静态输出              动态更新
无状态                有状态
结果导向              过程导向
```

---

## 颜色系统

### 语义化颜色映射

```
颜色        ANSI Code    语义用途                 使用场景
────────────────────────────────────────────────────────────────
green       32           成功/生成/创建           操作成功、文件创建
red         31           错误/危险/删除           错误信息、危险操作
yellow      33           警告/需确认/验证         警告、需要用户确认
blue        34           信息/分析/进行中         一般信息、分析结果
cyan        36           审查/检查/次要信息       代码审查、次要提示
magenta     35           创意/转换/特殊           AI 生成、特殊操作
grey        90           中性/禁用/历史           历史记录、禁用选项
white       37           默认文本                 普通文本内容
```

### 状态指示

```
✓ Success message                    (green)
✗ Error message                      (red)
⚠ Warning message                    (yellow)
ℹ Info message                       (blue)
```

### 操作类型

```
[创建] Creating new file...          (green)
[修改] Editing file...               (yellow)
[删除] Removing file...              (red)
[读取] Reading file...               (blue)
[分析] Analyzing code...             (cyan)
```

### 对比度要求

- 前景/背景对比度至少 4.5:1
- 避免纯红/绿组合 (色盲友好)
- 重要信息不仅依赖颜色，配合符号

---

## 排版规范

### 间距规范

```
组件间距：
┌─────────────────────────────────────┐
│ [标题]                              │  ← 1 行空白后开始内容
│                                     │
│ 内容区域                            │
│                                     │  ← 段落间 1 行空白
│ 新段落                              │
│                                     │
│ [操作按钮]                          │  ← 1 行空白后显示操作
└─────────────────────────────────────┘
```

### 行宽限制

```yaml
line_width:
  max: 80          # 最大行宽 (推荐)
  preferred: 72    # 首选行宽
  code_block: 120  # 代码块最大宽度
```

### Unicode 字符

```
推荐符号：
├── • 列表项 (U+2022)
├── → 箭头指示 (U+2192)
├── ✓ 成功勾选 (U+2713)
├── ✗ 失败叉号 (U+2717)
├── ⚠ 警告符号 (U+26A0)
├── ℹ 信息符号 (U+2139)
└── ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏ Spinner (Braille)
```

---

## 组件规范

### Spinner (加载指示器)

```javascript
// Braille 字符集 (推荐，固定宽度)
const brailleSpinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];

// ASCII 兼容
const classicSpinner = ['/', '-', '\\', '|'];

// 配置
const spinnerConfig = {
  interval: 80,        // 毫秒/帧
  color: 'cyan',
};
```

**格式**: `[动画符号] [状态文本] [计数/进度]`

### 进度条

```
基础样式：
[████████████░░░░░░░░] 60%

带标签：
Installing dependencies [████████░░░░] 67% (4/6)
```

**规范**：
- 最小宽度：20 字符
- 显示百分比或 x/total

### 对话框

```
┌─ Title ──────────────────────────────┐
│                                      │
│  Dialog content goes here.           │
│                                      │
│  [Button 1]  [Button 2]  [Button 3]  │
└──────────────────────────────────────┘
```

**规范**：
- 最小宽度：40 字符
- 按钮排列：取消在左，确认在右
- 危险操作：确认按钮用红色

### 选择菜单

```
单选菜单：
  ○ haiku    - Fast, efficient
→ ● sonnet   - Balanced (recommended)
  ○ opus     - Most capable

多选菜单：
  [x] Read    - Read files
→ [x] Write   - Write files
  [ ] Bash    - Run commands
```

**规范**：
- 当前项用 → 或高亮标识
- 显示简短描述
- 推荐选项标记 (recommended)

### 状态行

```
布局：
model │ context │ tasks │ status

示例：
sonnet │ ████░░ 45% │ 2 tasks │ Ready
```

### 代码块

```
┌─ src/index.ts ───────────────────────┐
│ 1 │ function hello() {               │
│ 2 │   console.log("Hello");          │
│ 3 │ }                                │
└──────────────────────────────────────┘

Diff 显示：
│   │ function hello() {               │
│ - │   console.log("Hello");          │  (red)
│ + │   console.log("Hello, World!");  │  (green)
│   │ }                                │
```

---

## 交互模式

### 输入模式

```
基础输入：
> 用户输入内容

多行输入 (Shift+Enter)：
> 第一行内容
  第二行内容

带前缀输入：
[sonnet] > 输入内容
```

### 命令系统

```
斜杠命令格式：
/command [required-arg] [optional-arg]

命令补全：
> /mod[Tab]
→ /model
```

### 引用系统

```
文件引用：
> @src/index.ts 这个文件有问题

URL 引用：
> @https://example.com 参考这个
```

### 确认流程

```
简单确认：
Proceed? (y/n): y

危险操作确认：
⚠ This will delete 5 files permanently.
Type "DELETE" to confirm: DELETE
```

---

## 动画与反馈

### Spinner 动画

```javascript
const brailleSpinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
const interval = 80; // ms
```

### 状态转换

```
⠋ Starting...
⠙ Processing...
⠹ Finalizing...
✓ Complete (2.3s)

错误恢复：
⠋ Connecting...
✗ Failed, retrying (1/3)...
✓ Connected
```

---

## 键盘交互

### 全局快捷键

```
导航：
↑/↓          历史记录/菜单导航
Tab          补全/下一项
Enter        确认/提交
Escape       取消/返回

编辑：
Ctrl+A       全选/行首
Ctrl+E       行尾
Ctrl+K       删除到行尾
Ctrl+U       删除到行首
Ctrl+W       删除前一个词

控制：
Ctrl+C       中断当前操作
Ctrl+D       退出 (空行时)
Ctrl+L       清屏
```

---

## 错误处理

### 错误显示

```
内联错误：
✗ Error: File not found
  Path: /src/missing.ts
  Suggestion: Check if the file exists
```

### 错误层级

```yaml
fatal:     # 致命错误，必须退出
  color: red
  icon: ✗

error:     # 错误，可重试
  color: red
  icon: ✗

warning:   # 警告，可继续
  color: yellow
  icon: ⚠

info:      # 提示，仅通知
  color: blue
  icon: ℹ
```

### 错误信息规范

```
结构：
[错误标识] [简短描述]
[详细信息]
[建议操作]

好的示例：
✗ Failed to read file
  Path: /etc/passwd
  Reason: Permission denied
  Try: sudo claude or check file permissions
```

---

## 终端兼容性

### 终端能力检测

```yaml
capabilities:
  unicode:
    test: "echo '✓'"
    fallback: "[OK]"

  256_colors:
    test: "tput colors"
    minimum: 256
    fallback: 16_colors

  true_color:
    env: COLORTERM=truecolor
    fallback: 256_colors
```

### 降级策略

```
Unicode 降级：
✓ → [OK]
✗ → [FAIL]
⚠ → [WARN]
→ → ->
│ → |
┌┐└┘ → +-+

颜色降级：
TrueColor → 256色 → 16色 → 无颜色
```

### 环境变量

```bash
FORCE_COLOR=1              # 强制启用颜色
NO_COLOR=1                 # 禁用颜色
TERM=xterm-256color        # 256 色支持
COLORTERM=truecolor        # TrueColor 支持
```

---

## 推荐技术栈

| 功能 | 推荐库 | 备选 |
|------|--------|------|
| 终端 UI | Ink | Blessed, Textual |
| 颜色 | Chalk | Kleur, Picocolors |
| Spinner | Ora | CLI-spinners |
| 选择菜单 | Inquirer | Prompts, Enquirer |
| 进度条 | CLI-progress | Progress |
| Markdown | Marked-terminal | - |

---

## ANSI 转义码速查

```
文本样式：
\x1b[0m   重置
\x1b[1m   粗体
\x1b[4m   下划线

前景色 (30-37, 90-97)：
\x1b[31m  红色
\x1b[32m  绿色
\x1b[33m  黄色
\x1b[34m  蓝色
\x1b[35m  洋红
\x1b[36m  青色

256 色：
\x1b[38;5;{n}m  前景色
\x1b[48;5;{n}m  背景色

TrueColor：
\x1b[38;2;{r};{g};{b}m  前景色
\x1b[48;2;{r};{g};{b}m  背景色
```

---

> 本规范基于 Claude Code 设计模式总结
