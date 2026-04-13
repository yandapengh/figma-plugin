# Textarea (多行文本框)

## 元信息

- 类型: 原子组件
- Figma Component ID: `55821:110439`

## 用途

多行文本输入控件，适用于较长的文本内容。

## 尺寸规格

| 属性 | 值 |
|------|-----|
| 高度 | 76px (默认) |
| 最小高度 | 64px |
| 宽度 | 484px |
| 圆角 | $radius-sm (4px) |

## 样式

| 属性 | 值 | Token |
|------|-----|-------|
| 背景色 | #ffffff | $color-bg-container |
| 边框色 | #e5e5e5 | $color-border-default |
| 边框宽度 | 1px | — |
| 圆角 | 4px | $radius-sm |
| 内边距 | 12px | $space-xs |

## 结构

```
Textarea (484×76)
├── placeholder (460×66)
│   └── text: "Please enter..."
└── bottom
    └── Resizer (8×8)
```

## 占位符样式

| 属性 | 值 | Token |
|------|-----|-------|
| 字号 | 14px | $font-size-sm |
| 颜色 | #000000 | $color-text-primary |

## 实现脚本

```javascript
var textarea = figma.createFrame();
textarea.name = 'Textarea';
textarea.resize(484, 76);
textarea.fills = [{type: 'SOLID', color: {r:1, g:1, b:1}}];
textarea.strokes = [{type: 'SOLID', color: {r:0.898, g:0.898, b:0.898}}];
textarea.strokeWeight = 1;
textarea.cornerRadius = 4;
```

## 相关文档

- 容器: [FormItem](FormItem/spec.md)
- 页面: [BasicForm](../../pages/BasicForm/spec.md)
