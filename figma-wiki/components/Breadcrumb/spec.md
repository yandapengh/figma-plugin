# Breadcrumb (面包屑)

## 元信息
- 类型: 原子组件
- Figma Component ID: 待获取
- Figma Component Key: 待获取

## 用途

页面导航路径指示。

## Tokens 引用

| 属性 | Token |
|------|-------|
| 文字色 | $color-text-heading |
| 链接色 | $color-primary |
| 分隔符色 | $color-text-secondary |
| 字号 | $font-size-sm |

## 结构

```
Breadcrumb (HORIZONTAL, gap=$space-xxs)
├── Item: "Home"（链接）
├── Separator: "/"
├── Item: "List"（链接）
├── Separator: "/"
└── Item: "Search Table"（当前页，无链接）
```

## 规则

- 最少 3 个层级
- 最后一项为当前页面，无链接样式
- 分隔符: "/"

## 相关

- 页面: [SearchTable](../../pages/SearchTable/spec.md)
