# FormItem (表单项)

## 元信息

- 类型: 表单容器组件
- Figma Component Set ID: `47211:209` (Field Type)
- 变体: Input, Textarea, Select, DatePicker, Button-Group

## 用途

表单项容器组件，包含标签和输入控件。支持**上下布局**和**左右布局**两种模式。

---

## 布局模式一：上下布局

```
Form-Item (VERTICAL)
├── label (HORIZONTAL)
│   └── [title, ":", InfoCircle]
└── Field (INSTANCE)
```

### Form-Item 属性

| 属性 | 值 | 说明 |
|------|-----|------|
| layoutMode | VERTICAL | 垂直布局 |
| itemSpacing | 4 | label → Field 间距 |
| counterAxisAlignItems | MIN | 左对齐 |
| primaryAxisSizingMode | AUTO | 高度自适应 |

### label 容器属性

| 属性 | 值 | 说明 |
|------|-----|------|
| layoutMode | HORIZONTAL | 文字水平排列 |
| itemSpacing | 4 | 文字间距 |
| counterAxisAlignItems | CENTER | 垂直居中 |

---

## 布局模式二：左右布局

```
Form-Item (HORIZONTAL)
├── label (HORIZONTAL, 固定宽度)
│   └── [title, ":", InfoCircle]
└── Field (INSTANCE)
```

### Form-Item 属性

| 属性 | 值 | 说明 |
|------|-----|------|
| layoutMode | HORIZONTAL | 左右布局 |
| itemSpacing | 105 | label 右边缘 → Field 左边缘间距 |
| counterAxisAlignItems | CENTER | Input 垂直居中对齐 |
| primaryAxisSizingMode | AUTO | 高度自适应 |

### label 容器属性

| 属性 | 值 | 说明 |
|------|-----|------|
| layoutMode | HORIZONTAL | 文字水平排列 |
| itemSpacing | 4 | 文字间距 |
| counterAxisAlignItems | CENTER | 垂直居中 |
| width | 固定值 | 最长文字宽度 + padding |

### 垂直对齐规则

| 控件类型 | counterAxisAlignItems | 说明 |
|---------|----------------------|------|
| Input | CENTER | 与 label 垂直居中对齐 |
| Textarea | MIN | 与 label 顶部对齐 |

---

## Field INSTANCE 说明

Field 是 INSTANCE 类型，其布局属性由组件定义：
- counterAxisSizingMode: AUTO (高度自适应)
- 如需修改 INSTANCE 布局，先 `detachInstance()`

---

## 尺寸规格

| 变体 | Form-Item 高度 | 说明 |
|------|---------------|------|
| Input | 32px | Field 高度 |
| Textarea | 76px | Field 高度 |
| Select | 32px | Field 高度 |
| DatePicker | 32px | Field 高度 |

---

## 标签样式

| 属性 | 值 | Token |
|------|-----|-------|
| 字号 | 14px | $font-size-sm |
| 颜色 | #000000 | $color-text-heading |

## 实现脚本（左右布局）

```javascript
var formItem = figma.createFrame();
formItem.name = 'Form-Item';
formItem.layoutMode = 'HORIZONTAL';
formItem.itemSpacing = 105;
formItem.counterAxisAlignItems = 'CENTER';
formItem.primaryAxisSizingMode = 'AUTO';
formItem.counterAxisSizingMode = 'FIXED';

var label = figma.createFrame();
label.name = 'label';
label.layoutMode = 'HORIZONTAL';
label.itemSpacing = 4;
label.counterAxisAlignItems = 'CENTER';
label.resize(158, 22);

formItem.appendChild(label);
```

## 子组件

| 组件 | 文档 |
|------|------|
| Input | [Input](Input/spec.md) |
| Textarea | [Textarea](Textarea/spec.md) |
| Select | [Select](Select/spec.md) |
| DatePicker | [DatePicker](DatePicker/spec.md) |
| Button | [Button](Button/spec.md) |

## 相关文档

- 页面: [BasicForm](../../pages/BasicForm/spec.md)
