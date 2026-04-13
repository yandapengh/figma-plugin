# GlobalHeader (顶部导航)

## 元信息
- 类型: 原子组件
- Figma Component ID: 待获取
- Figma Component Key: 待获取

## 用途

全局顶部导航栏，放置 LOGO 和工具栏。

## Tokens 引用

| 属性 | Token |
|------|-------|
| 背景色 | $color-bg-container |
| 文字色 | $color-text-primary |
| 图标色 | $color-text-secondary |

## 结构

```
GlobalHeader (HORIZONTAL, space-between)
├── LOGO（左侧）
└── Toolbar（右侧, HORIZONTAL）
    ├── 全局搜索
    ├── 帮助中心 Icon（问号）
    ├── 用户头像
    ├── 用户名称
    └── 多语言切换
```

## 布局

- LOGO 在左，Toolbar 在右
- 宽度: 100%（铺满页面宽度）

## 相关

- 页面: [SearchTable](../../pages/SearchTable/spec.md)
