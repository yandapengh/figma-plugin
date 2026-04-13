# Search Table PC 完整还原方案

## 节点 ID

- **Root**: `64462:1761` (Search Table)
- **page-container**: `64462:1762`
- **content**: 搜索表单 + 表格区域
- **sider**: 左侧菜单
- **global-header**: 顶部导航

## 结构层级

```
Search Table (1440×900, $color-bg-page)
├── page-container (1232×836)
│   ├── .Page-Header (1232×102)
│   │   ├── Breadcrumb (1184×22)
│   │   │   ├── 1st-item → "Home"
│   │   │   ├── 2nd-item → "List"
│   │   │   └── last-item → "Search Table"
│   │   └── heading-left → "Search Table" (Title)
│   └── content (1184×841)
│       ├── .card (搜索表单, 1184×84, 展开)
│       │   ├── Form-Item (Rule Name)
│       │   └── Form-Item (Description)
│       ├── Frame 151 (表格 1184×733)
│       │   ├── Table-Toolbar
│       │   ├── columns (6列)
│       │   │   ├── Checkbox (32)
│       │   │   ├── Rule Name (119)
│       │   │   ├── Description (411)
│       │   │   ├── Service Calls (115)
│       │   │   ├── Status (97)
│       │   │   ├── Last Dispatch Time (161)
│       │   │   └── Action (201)
│       │   └── pagination
│       └── sider (左侧菜单 208×852)
└── global-header (顶部导航)
```

## 还原方式

### 方式1：克隆原始页面（推荐高保真）

```javascript
(async function() {
  var source = await figma.getNodeByIdAsync('64462:1761');
  var copy = source.clone();
  copy.x = 2200;
  copy.y = 100;
  copy.name = 'Search Table - 副本';
})()
```

### 方式2：动态修改

```javascript
// 修改 Card 展开/收起
var content = page.findOne(n => n.name === 'content');
var card = content.findOne(n => n.name.includes('card'));
card.expanded = !card.expanded;

// 添加更多查询项
var body = card.findOne(n => n.name === 'body');
// 循环添加 Form-Item...
```

## 关键组件 ID（用于引用）

- Form-Item/Input (400×32) — 查询输入框
- Table/Column-Based — 表格组件
- Components/Table-Cell/Checkbox — 复选框
- Components/Table-Column/Status — 状态列
- Pagination — 分页

## Design System 组件

- `.Page-Header(Legacy)` — 页面头部
- `.card(legacy)` — 卡片组件
- `Breadcrumb` — 面包屑导航
- `Table/Column-Based` — 表格

## 完整 JSX 树

详见 [full-structure.jsx](full-structure.jsx)（完整节点树，约 700+ 行）。

## 相关文档

- [spec.md](spec.md) — 页面规格
- [assembly.md](assembly.md) — 组装清单
- [Card](../../components/Card/spec.md)
- [Table](../../components/Table/spec.md)
- [api-patterns](../../tooling/api-patterns.md)
