# Claude Skills Collection

我的 Claude Code 自定义技能集合。

## 安装

```bash
# 安装单个 skill
cp -r skills/{skill-name} ~/.claude/skills/

# 或创建符号链接（便于同步更新）
ln -sf $(pwd)/skills/{skill-name} ~/.claude/skills/{skill-name}
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

## 目录结构

```
claude-skills/
├── skills/
│   └── reflect/
│       └── SKILL.md
├── templates/
│   ├── learned-rules.md    # 规则文件模板
│   └── reflect-log.md      # 日志文件模板
└── README.md
```

## 添加新 Skill

1. 创建目录 `skills/{name}/`
2. 添加 `SKILL.md`（参考现有格式）
3. 更新本 README

## License

MIT
