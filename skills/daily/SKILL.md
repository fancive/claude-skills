---
name: daily
description: "访谈式日记记录到 Obsidian。参数：morning、evening、quick、deep、add。关键词：写日记、记日记、日记、/daily"
---

# 访谈式日记

通过对话引导用户记录日记到 Obsidian。

## 环境

- 环境变量：`$OBSIDIAN_DAILYS`（必须配置）
- 日记路径：`$OBSIDIAN_DAILYS/YYYY-MM-DD.md`
- 模板：[assets/template.md](assets/template.md)

## 命令

| 命令 | 说明 |
| ---- | ---- |
| `/daily` | 自动识别时段（6-12点=morning，18-2点=evening） |
| `/daily morning` | 早晨：睡眠、能量、计划 |
| `/daily evening` | 晚间：事件、反思、感恩 |
| `/daily quick` | 批量收集，最少问答 |
| `/daily deep` | 追问引导，深度反思 |
| `/daily add [内容]` | 随时追加内容 |

## 执行流程

1. **准备**：读取 `$OBSIDIAN_DAILYS`，获取/创建今日文件
2. **识别**：解析参数确定模式，检查已填字段
3. **访谈**：按模式逐字段对话收集
4. **保存**：更新 frontmatter 和正文

## 交互规范

- **评分 1-5**（困觉、精力、专注、今日评分）→ **文本对话**，数字 1-5
- **固定选项问题**（时间、是否、习惯打卡）→ 使用 AskUserQuestion 工具
- **开放式问题**（发生了什么、印象深刻、感恩、计划）→ 文本对话

详见：[references/askuserquestion.md](references/askuserquestion.md)

## 对话风格

- 友好简洁，像朋友聊天
- 智能解析用户一次说的多项信息
- "跳过" → 跳过当前字段
- "就这样" → 保存结束
- 结束时显示简短摘要

## 参考文档

- 模式详解：[references/modes.md](references/modes.md)
- AskUserQuestion 规范：[references/askuserquestion.md](references/askuserquestion.md)

## Add 模式速查

| 关键词 | 追加位置 |
| ------ | -------- |
| 发生了、做了 | 今日发生了 |
| 想到、感觉 | 印象深刻 |
| 学到、明白了 | 学到什么 |
| 感谢、感激 | 感恩列表 |
| 计划、打算 | 今日计划 |
| 完成了、打卡 | 习惯记录 |

快捷：`/daily add 学到：Go context 用法`
