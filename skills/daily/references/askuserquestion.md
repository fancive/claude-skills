# AskUserQuestion 使用规范

对于**有固定选项的问题**使用 AskUserQuestion 工具，开放式问题和评分问题保持文本对话。

## 适用场景

| 问题类型 | 使用工具 | 示例 |
| -------- | -------- | ---- |
| 评分 1-5 | **文本对话** | 状态评分、能量、专注、起床困难度 |
| 时间选择 | AskUserQuestion | 入睡时间、起床时间 |
| 是/否 | AskUserQuestion | 陪宝宝了吗 |
| 习惯打卡 | AskUserQuestion（多选） | 完成了哪些习惯 |
| 开放式 | 文本对话 | 今天发生了什么、印象深刻、感恩 |

## 评分类问题（1-5 文本对话）

由于工具限制最多 4 个选项，1-5 评分**直接文本对话**，不使用 AskUserQuestion：

```text
Claude: 起床困觉？(1-5，1=轻松，5=很困)
用户: 3
Claude: 能量水平？(1-5)
用户: 4
```

**所有评分字段统一使用数字**：
- 起床困觉：1-5（1=很轻松，5=很困难）
- 能量水平：1-5（1=很疲惫，5=精力充沛）
- 专注水平：1-5（1=无法集中，5=高度专注）
- 今日状态评分：1-5（1=很差，5=很棒）

## 入睡时间（23点-2点，每小时）

```json
{
  "questions": [{
    "question": "昨晚几点睡的？",
    "header": "入睡时间",
    "options": [
      {"label": "23:00", "description": "11点"},
      {"label": "00:00", "description": "12点"},
      {"label": "01:00", "description": "1点"},
      {"label": "02:00", "description": "2点"}
    ],
    "multiSelect": false
  }]
}
```

## 起床时间（7点-9点，每半小时）

```json
{
  "questions": [{
    "question": "今早几点起？",
    "header": "起床时间",
    "options": [
      {"label": "07:00", "description": "7点"},
      {"label": "07:30", "description": "7点半"},
      {"label": "08:00", "description": "8点"},
      {"label": "08:30", "description": "8点半"}
    ],
    "multiSelect": false
  }]
}
```

注：9点可通过 "Other" 输入。

## 是否类问题

```json
{
  "questions": [{
    "question": "今天陪宝宝了吗？",
    "header": "陪伴记录",
    "options": [
      {"label": "是", "description": "有高质量陪伴时间"},
      {"label": "否", "description": "今天没有陪伴"}
    ],
    "multiSelect": false
  }]
}
```

## 习惯打卡（多选）

```json
{
  "questions": [{
    "question": "今天完成了哪些习惯？",
    "header": "习惯打卡",
    "options": [
      {"label": "自习", "description": "进行了学习"},
      {"label": "运动", "description": "锻炼身体"},
      {"label": "阅读", "description": "读书时间"},
      {"label": "冥想", "description": "静心冥想"}
    ],
    "multiSelect": true
  }]
}
```

## Quick 模式批量收集

Morning 快速（睡眠+评分），分两部分：

**时间（AskUserQuestion）**

```json
{
  "questions": [
    {
      "question": "昨晚几点睡？",
      "header": "入睡",
      "options": [
        {"label": "23:00", "description": "11点"},
        {"label": "00:00", "description": "12点"},
        {"label": "01:00", "description": "1点"},
        {"label": "02:00", "description": "2点"}
      ],
      "multiSelect": false
    },
    {
      "question": "今早几点起？",
      "header": "起床",
      "options": [
        {"label": "07:00", "description": "7点"},
        {"label": "07:30", "description": "7点半"},
        {"label": "08:00", "description": "8点"},
        {"label": "08:30", "description": "8点半"}
      ],
      "multiSelect": false
    }
  ]
}
```

**评分（文本对话）**

```text
Claude: 困觉、精力、专注各几分？(1-5)
用户: 3 4 4
Claude: ✅ 困觉3 精力4 专注4
```

## 注意事项

- 每次最多 4 个问题，每个问题最多 4 个选项
- 超出范围的值通过 "Other" 输入
- 开放式问题（发生了什么、印象深刻、感恩、计划）直接文本对话
