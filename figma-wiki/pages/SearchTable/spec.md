# Search Table (搜索表格)

## 业务场景

用于展示结构化数据列表的搜索表格页面，常见于后台管理系统。

### 相关场景

- 用户管理
- 订单管理
- 数据报表

## 页面规格

- 尺寸: 1440×900
- 内容区宽度: 1184px
- 背景: $color-bg-page
- 布局: GlobalHeader + Sider + 大内容区

## 页面构成

- [GlobalHeader](../../components/GlobalHeader/spec.md) — 顶部导航
- [Sider](../../components/Sider/spec.md) — 左侧菜单 (208px)
- 大内容区
  - Page-Header: [Breadcrumb](../../components/Breadcrumb/spec.md) + [Title](../../components/Title/spec.md)
  - 内容区: [Card](../../components/Card/spec.md) (搜索表单变体) + [Table](../../components/Table/spec.md)

## 相关文档

- [structure.md](structure.md) — 完整图层结构和节点 ID
- [assembly.md](assembly.md) — 组件组装清单
- [full-structure.jsx](full-structure.jsx) — 完整 JSX 树

## 待补充

- 页面交互流程
- 响应式断点
