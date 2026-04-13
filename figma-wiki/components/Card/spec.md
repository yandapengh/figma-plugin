# Card (卡片)

## 元信息
- 类型: 原子组件
- Figma Component ID: 待获取
- Figma Component Key: 待获取
- 变体: default, search-form

## 用途

容器组件，用于包裹内容区块。

## Tokens 引用

| 属性 | Token |
|------|-------|
| 背景色 | $color-bg-container |
| 圆角 | $radius-md |
| 内边距 | $space-md |

## 结构

```
Card
├── header（可选）
│   └── title
└── body
    └── {children}
```

## 变体: 搜索表单 (Search Form)

用于搜索条件输入框的容器变体。

### 结构

```jsx
<Frame name="Card" width={1184} height={80} fill="$color-bg-container" radius="$radius-md">
  <Frame name="body" width={1184} height={80}>
    <Frame name="LayoutBlocks" width={1136} height={32} x={24} y={24}>
      <Frame name="Form-Item" width={400} height={32}>
        <Frame name="label" text="Rule Name:" fontSize="$font-size-sm" fill="$color-text-primary" />
        <Frame name="Field" width={400} height={32} fill="$color-bg-container">
          <Text name="placeholder" text="Please enter..." fill="$color-text-placeholder" />
        </Frame>
      </Frame>
      <Frame name="Form-Item-2" width={400} height={32}>
        <Frame name="label" text="Description:" fontSize="$font-size-sm" fill="$color-text-primary" />
        <Frame name="Field" width={400} height={32} fill="$color-bg-container" />
      </Frame>
    </Frame>
  </Frame>
</Frame>
```

### 样式属性

| 元素 | 属性 | Token |
|------|------|-------|
| Card 容器 | fill | $color-bg-container |
| Card 容器 | cornerRadius | $radius-md |
| label 文字 | fontSize | $font-size-sm |
| label 文字 | color | $color-text-primary |
| placeholder | color | $color-text-placeholder |
| Field 输入框 | fill | $color-bg-container |
| Field 输入框 | stroke | $color-border-default |

### 实现脚本

```javascript
var card = figma.createFrame();
card.name = 'Card';
card.resize(1184, 80);
card.fills = [{type: 'SOLID', color: {r:1, g:1, b:1}}]; // $color-bg-container
card.cornerRadius = 8; // $radius-md
```

### 扩展修改

- 展开/收起：通过 expanded 属性控制
- 查询项数量：通过循环添加 Form-Item

## JSX 格式说明

纯描述性 JSX，用于 LLM 理解结构，非直接执行。通过 figma-use 导出：

```bash
figma-use export jsx <node-id>
```

## 相关

- 页面: [SearchTable](../../pages/SearchTable/spec.md)
- 子组件: Form-Item（内嵌，暂无独立文档）
