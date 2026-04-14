# figma-wiki 索引

设计知识库入口。按需读取相关文档，不需要全量加载。

## Tokens（设计变量）

- [colors](tokens/colors.md) — 全局色板：品牌色/中性色/语义色
- [typography](tokens/typography.md) — 字体阶梯：Inter, 12-24px
- [spacing](tokens/spacing.md) — 间距系统：基于 4px 网格
- [radius](tokens/radius.md) — 圆角规范：4/8/12px

## Components（组件）

- [FormItem](components/FormItem/spec.md) — 表单项容器，含标签和输入控件
- [Input](components/Input/spec.md) — 单行文本输入框，支持前缀/后缀
- [Textarea](components/Textarea/spec.md) — 多行文本输入框
- [Select](components/Select/spec.md) — 下拉选择框
- [DatePicker](components/DatePicker/spec.md) — 日期选择器
- [Button](components/Button/spec.md) — 按钮，Primary/Default/Dashed/Text 变体
- [Table](components/Table/spec.md) — 数据表格，支持排序/分页/状态列/Action列
- [Card](components/Card/spec.md) — 容器卡片，含搜索表单变体
- [GlobalHeader](components/GlobalHeader/spec.md) — 顶部导航栏，Logo + Toolbar
- [Sider](components/Sider/spec.md) — 左侧导航菜单，208px，两级
- [Breadcrumb](components/Breadcrumb/spec.md) — 面包屑导航
- [Title](components/Title/spec.md) — 页面主标题

## Pages（页面）

- [BasicForm/spec](pages/BasicForm/spec.md) — 基础表单页，5个表单项 + 提交/重置
- [SearchTable/spec](pages/SearchTable/spec.md) — 搜索表格页，业务场景 + 页面规格
- [SearchTable/structure](pages/SearchTable/structure.md) — 图层结构 + 节点 ID + 还原脚本
- [SearchTable/assembly](pages/SearchTable/assembly.md) — 组件组装清单
- [SearchTable/full-structure.jsx](pages/SearchTable/full-structure.jsx) — 完整 JSX 树（700+ 行）

## Tooling（工具）

- [bridge](tooling/bridge.md) — Python↔Node↔Figma 桥接架构
- [api-patterns](tooling/api-patterns.md) — Figma API 命令模式和模板
- [common-errors](tooling/common-errors.md) — 已知错误和解决方案
- [variables](tooling/variables.md) — Variables 变量绑定方法
- [migration-plan-schema-driven](tooling/migration-plan-schema-driven.md) — Grab 从 legacy 到 schema-driven 迁移方案
