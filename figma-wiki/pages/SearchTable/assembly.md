# SearchTable - 组装清单

## 画布

- 尺寸: 1440×900
- 背景: $color-bg-page
- 内容区宽度: 1184px

## 组件实例化

| 序号 | 组件 | Component ID | 属性配置 | 父节点 |
|------|------|-------------|---------|--------|
| 1 | GlobalHeader | 待获取 | — | root |
| 2 | Sider | 待获取 | collapsed: false, width: 208 | LayoutFrame |
| 3 | Breadcrumb | 待获取 | items: ["Home", "List", "Search Table"] | PageHeader |
| 4 | Title | 待获取 | text: "Search Table" | PageHeader |
| 5 | Card (search-form) | 待获取 | fields: ["Rule Name", "Description"] | ContentArea |
| 6 | Table | 待获取 | columns: [Checkbox, RuleName, Description, ServiceCalls, Status, LastDispatchTime, Action], rows: 3 | ContentArea |
| 7 | Pagination | 待获取 | total: 100, pageSize: 20 | ContentArea |

## 布局关系

```
root (1440×900, VERTICAL, fill=$color-bg-page)
├── GlobalHeader (full-width)
└── LayoutFrame (HORIZONTAL, fill-container)
    ├── Sider (width=208)
    └── page-container (VERTICAL, flex=1)
        ├── PageHeader (VERTICAL, padding=$space-md)
        │   ├── Breadcrumb
        │   └── Title
        └── ContentArea (VERTICAL, padding=$space-md, gap=$space-sm)
            ├── Card:search-form (1184×84)
            │   └── LayoutBlocks (HORIZONTAL, gap=$space-sm)
            │       ├── Form-Item: Rule Name (400×32)
            │       └── Form-Item: Description (400×32)
            ├── TableFrame (1184×733)
            │   ├── Table-Toolbar
            │   ├── Table (columns × rows)
            │   └── Pagination
            └── (底部留白)
```

## Token 引用

| 元素 | 属性 | Token |
|------|------|-------|
| 页面背景 | fill | $color-bg-page |
| 容器/Card/Header | fill | $color-bg-container |
| 内容区 padding | padding | $space-md |
| 元素间距 | gap | $space-sm |
| Card 圆角 | cornerRadius | $radius-md |
| 正文字号 | fontSize | $font-size-sm |
| 标题字号 | fontSize | $font-size-xl |

## 克隆还原（快捷方式）

如 Figma 中已有原始设计稿，可直接克隆：

```javascript
(async function() {
  var source = await figma.getNodeByIdAsync('64462:1761');
  var copy = source.clone();
  copy.x = 2200;
  copy.name = 'Search Table - Clone';
})()
```
