# Sider (左侧菜单)

## 元信息
- 类型: 原子组件
- Figma Component ID: 待获取
- Figma Component Key: 待获取

## 用途

页面左侧导航菜单，支持两级展开/收起。

## Tokens 引用

| 属性 | Token |
|------|-------|
| 背景色 | $color-bg-container |
| 菜单文字 | $color-text-primary |
| 选中项 | $color-primary |
| 分隔线 | $color-border-default |

## 规格

- 宽度: 208px
- 菜单层级: 两级

## 结构

```
Sider (VERTICAL, width=208)
├── Menu-Group-1
│   ├── Menu-Item (一级)
│   ├── Sub-Menu-Item (二级)
│   └── Sub-Menu-Item (二级)
├── Menu-Group-2 (收起)
│   └── Menu-Item (一级)
└── ...
```

## 状态

| 状态 | 变化 |
|------|------|
| Default | 正常显示 |
| Menu-Item Hover | 背景高亮 |
| Menu-Item Active | 文字色 $color-primary，左侧指示条 |
| Collapsed | 宽度收缩，仅显示图标 |

## 默认状态

- 默认展开一个菜单组
- 其余菜单组收起

## 相关

- 页面: [SearchTable](../../pages/SearchTable/spec.md)
