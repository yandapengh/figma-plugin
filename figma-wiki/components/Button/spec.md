# Button (按钮)

## 元信息

- 类型: 原子组件
- 变体: Primary, Default, Dashed, Text

## 尺寸规格

| 属性 | 值 |
|------|-----|
| 高度 | 32px |
| 最小宽度 | 72px |
| 圆角 | $radius-sm (4px) |
| 内边距 | 16px 水平 |

## 变体样式

### Primary (主要按钮)

| 属性 | 值 | Token |
|------|-----|-------|
| 背景色 | #1890ff | $color-primary |
| 文字色 | #ffffff | — |
| 悬停色 | #40a9ff | $color-primary-hover |

### Default (默认按钮)

| 属性 | 值 | Token |
|------|-----|-------|
| 背景色 | #ffffff | $color-bg-container |
| 边框色 | #e5e5e5 | $color-border-default |
| 文字色 | #000000 | $color-text-heading |

### Dashed (虚线按钮)

| 属性 | 值 | Token |
|------|-----|-------|
| 背景色 | transparent | — |
| 边框样式 | dashed | — |
| 边框色 | #e5e5e5 | $color-border-default |
| 文字色 | #000000 | $color-text-heading |

### Text (文本按钮)

| 属性 | 值 |
|------|-----|
| 背景色 | transparent |
| 文字色 | #1890ff | $color-primary |

## 文字样式

| 属性 | 值 | Token |
|------|-----|-------|
| 字号 | 14px | $font-size-sm |
| 字重 | Medium (500) | $font-weight-medium |

## 典型用例

| 按钮 | 变体 | 场景 |
|------|------|------|
| Submit | Primary | 提交表单 |
| Reset | Default | 重置表单 |

## 实现脚本

```javascript
var btn = figma.createFrame();
btn.name = 'Button';
btn.resize(80, 32);
btn.fills = [{type: 'SOLID', color: {r:0.098, g:0.565, b:1}}]; // #1890ff
btn.cornerRadius = 4;
```

## 相关文档

- 页面: [BasicForm](../../pages/BasicForm/spec.md)
