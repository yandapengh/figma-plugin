# 已知错误和解决方案

## 错误速查表

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| Cannot write to unloaded font | 未加载字体 | 先执行 `await figma.loadFontAsync({ family: "Inter", style: "Regular" })` |
| Unexpected token 'var' | Figma 不支持裸 `var` 声明 | 用 IIFE 包装：`(function(){ var x; return x; })()` |
| Not available | AsyncFunction 被禁止 | 改用同步 Function + IIFE 包装 |
| INSTANCE 内部无法修改 | 组件实例的子节点不可直接修改 | 优先使用 `visible = false` 隐藏；如需修改内容再 `detachInstance()` |
| detach + remove 破坏布局 | Auto Layout 联动被破坏 | 使用 `node.visible = false` 代替删除 |
| getNodeById 报错 | 旧 API 已废弃 | 改用 `figma.getNodeByIdAsync('id')` |
| 克隆后属性丢失 | 引用 vs 值的问题 | 保留原始组件 ID，用克隆方式还原 |

## 关键约束

1. **IIFE 包装是必须的** — Figma 插件沙箱不支持裸声明
2. **字体必须提前加载** — 任何文字操作前都要 `loadFontAsync`
3. **使用异步节点查找** — `getNodeByIdAsync` 替代 `getNodeById`
4. **组件实例只读** — 修改实例内部需先 detach 或克隆
5. **var 而非 let/const** — IIFE 内部使用 `var`

## 相关

- [bridge.md](bridge.md) — 桥接系统架构
- [api-patterns.md](api-patterns.md) — API 命令模式
