# Bridge 桥接系统

## 用途

Python Agent 与 Figma 之间的通信桥梁，通过 HTTP/WebSocket 双通道实现代码执行和节点读取。

## 架构

```
Python Agent → HTTP(8768) → Node Server → WS(8767) → Figma UI → code.js → Figma API
```

## 组成文件

| 文件 | 职责 |
|------|------|
| `server.js` | Node 中转服务器（8768 HTTP / 8767 WS） |
| `code.js` | Figma 插件核心代码 |
| `ui.html` | 插件 UI |
| `bridge_client.py` | Python 客户端 |

## 当前 API

```python
from bridge_client import send, read

send("(function(){ /* IIFE代码 */ })()")  # 执行代码到 Figma
read()                                     # 读取选中节点
```

## 关键功能

- 代码执行（send）— 发送 IIFE 包装的 JS 代码到 Figma 执行
- 节点读取（read）— 读取选中节点的属性和子节点（支持递归）
- Bridge 状态显示 — UI 面板显示连接状态

## 超时设置

- `/send` 路由: 30 秒超时
- `/read` 路由: 10 秒超时

## 相关

- [api-patterns.md](api-patterns.md) — Figma API 常用模式
- [common-errors.md](common-errors.md) — 已知错误和解决方案
