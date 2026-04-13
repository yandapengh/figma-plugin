# Figma Bridge 项目

## figma-wiki 使用规则

1. 开始任务前先读 `figma-wiki/_index.md` 了解可用知识
2. 根据任务需求按需读取相关组件/页面文档
3. 创建/修改组件时先读 `tokens/` 确保样式一致
4. 遇到 Figma API 问题时查 `tooling/common-errors.md`
5. 新建组件/页面后更新 `_index.md` 索引
6. 会话结束按需更新文档

## Bridge API

```python
from bridge_client import send, read
send("(function(){ /* IIFE代码 */ })()")  # 执行代码到 Figma
read()                                     # 读取选中节点
```

## 关键约束

- Figma 代码**必须** IIFE 包装：`(function(){ ... })()`
- 使用 `var` 而非 `let/const`
- 字体操作前必须 `figma.loadFontAsync()`
- 使用 `figma.getNodeByIdAsync()` 而非 `getNodeById()`
- AsyncFunction 被禁止，使用同步 Function + IIFE

## 脚本管理

- `scripts-examples/` — 可复用示例脚本
- `scripts-temp/` — 临时脚本（会话结束删除）
