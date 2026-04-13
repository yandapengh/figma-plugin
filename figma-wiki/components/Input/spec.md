# Input (输入框)

## 元信息

- 类型: 原子组件
- Figma Component ID: `44288:84051` (Field)
- 变体: default, with-prefix, with-suffix, with-addon

## 用途

单行文本输入控件，支持前缀/后缀图标和文本插件。

## Auto Layout 属性

| 属性 | 值 | 说明 |
|------|-----|------|
| layoutMode | HORIZONTAL | 水平排列 |
| itemSpacing | 0 | 无间距 |
| counterAxisAlignItems | CENTER | 垂直居中 |
| primaryAxisSizingMode | FIXED | 固定高度 |
| width | 父容器宽度 | 自适应 |

## 尺寸规格

| 属性 | 值 |
|------|-----|
| 高度 | 32px |
| 宽度 | 100% 父容器（使用 FIXED_WIDTH 配合外部拉伸） |
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
Field (FRAME - HORIZONTAL)
├── Input-Addon/Label (可选, 64×32)
│   └── text → "http://"
├── input (FRAME)
│   ├── input-prefix (可选, 14×14)
│   │   └── icon (User 等)
│   ├── wrapper (placeholder)
│   └── input-suffix (可选, 14×14)
│       └── icon (close-circle 等)
└── Input-Addon/Icon (可选, 38×32)
    └── icon (Setting 等)
```

## 自适应宽度实现

Field 放在 Form-Item 内，Form-Item 使用 `counterAxisSizingMode: 'FIXED'` + `width: 100%`，Field 自动填满宽度。

## 图标规格

| 图标 | 尺寸 | 颜色 |
|------|------|------|
| User | 14×14 | #000000 |
| Setting | 14×14 | #000000 |
| close-circle | 14×14 | #000000 |

## 占位符样式

| 属性 | 值 | Token |
|------|-----|-------|
| 字号 | 14px | $font-size-sm |
| 颜色 | #000000 | $color-text-primary |

## 实现脚本

```javascript
var field = figma.createFrame();
field.name = 'Field';
field.layoutMode = 'HORIZONTAL';
field.itemSpacing = 0;
field.counterAxisAlignItems = 'CENTER';
field.resize(484, 32);
field.fills = [{type: 'SOLID', color: {r:1, g:1, b:1}}];
field.strokes = [{type: 'SOLID', color: {r:0.898, g:0.898, b:0.898}}];
field.strokeWeight = 1;
field.cornerRadius = 4;
```

## 相关文档

- 容器: [FormItem](FormItem/spec.md)
- 页面: [BasicForm](../../pages/BasicForm/spec.md)
