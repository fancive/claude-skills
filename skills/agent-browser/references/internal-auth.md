# Internal Sites Authentication (内网认证)

对于需要认证的内部网站（如 `*.baidu.com`, `*.baidu-int.com` 等），**必须**先复用已有登录状态。

## 方法 1：连接已打开的 Chrome（推荐）

```bash
# 检查 Chrome CDP 是否就绪
lsof -i :9222 | grep -q Chrome && echo "Chrome CDP ready" || echo "Need to start Chrome with CDP"

# 如果没有，提示用户启动：
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# 连接并访问
agent-browser connect 9222
agent-browser open <internal-url>
```

## 方法 2：加载保存的认证状态

```bash
# 如果有保存的状态文件
agent-browser state load ~/.agent-browser/baidu-auth.json
agent-browser open <internal-url>
```

## 工作流程

访问内部站点时，按以下顺序尝试：

1. 检测 URL 是否为内部站点（`*.baidu.com`, `*.baidu-int.com` 等）
2. 优先尝试 `agent-browser connect 9222`
3. 如果失败，检查是否有 `~/.agent-browser/baidu-auth.json`
4. 如果都没有，提示用户：
   - 启动带 CDP 的 Chrome：`/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`
   - 或手动登录后保存状态：`agent-browser state save ~/.agent-browser/baidu-auth.json`

## 保存认证状态

首次登录后保存状态供后续使用：

```bash
# 用 headed 模式打开，手动完成登录
agent-browser --headed open https://uuap.baidu.com

# 登录成功后保存状态
mkdir -p ~/.agent-browser
agent-browser state save ~/.agent-browser/baidu-auth.json
```
