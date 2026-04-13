# Select (下拉选择)

## 元信息

- 类型: 原子组件
- Figma Component ID: 待获取

## 用途

下拉选择控件，用于从预定义选项中选择。

## 尺寸规格

| 属性 | 值 |
|------|-----|
| 高度 | 32px |
| 宽度 | 484px |
| 圆角 | $radius-sm (4px) |

## 样式

| 属性 | 值 | Token |
|------|-----|-------|
| 背景色 | #ffffff | $color-bg-container |
| 边框色 | #e5e5e5 | $color-border-default |
| 边框宽度 | 1px | — |
| 圆角 | 4px | $radius-sm |

## 结构

```
Select (484×32)
├── placeholder (460×22)
│   └── text: "Please select"
├── Arrow icon (12×12)
└── dropdown (展开状态)
    └── Option × N
```

## 相关文档

- 容器: [FormItem](FormItem/spec.md)
- 页面: [BasicForm](../../pages/BasicForm/spec.md)
