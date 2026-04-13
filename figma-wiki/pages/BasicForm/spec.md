# Basic Form (基础表单页)

## 业务场景

用于收集或验证用户信息的表单页面，适用于数据项较少的场景。

### 典型用例

- 用户注册/登录
- 数据录入
- 设置/配置页面

## 页面规格

- 尺寸: 1440×900
- 内容区宽度: 1184px
- 背景: $color-bg-page
- 布局: GlobalHeader + Sider + 居中表单区

## 页面构成

| 区域 | 组件 | 说明 |
|------|------|------|
| 顶部导航 | [GlobalHeader](../../components/GlobalHeader/spec.md) | 固定导航栏 |
| 左侧菜单 | [Sider](../../components/Sider/spec.md) | 208px 菜单 |
| 页面头部 | [Breadcrumb](../../components/Breadcrumb/spec.md) + Title | 面包屑 + 标题 |
| 表单区域 | [FormItem](../../components/FormItem/spec.md) × N | 5个表单项 |
| 按钮区 | [Button](../../components/Button/spec.md) × 2 | 提交 + 重置 |

## 表单字段

| 字段 | 组件类型 | 必填 | 说明 |
|------|----------|------|------|
| Title | [Input](../../components/Input/spec.md) | ✓ | 带前缀 http:// |
| Goal description | [Input](../../components/Input/spec.md) | ✓ | 带清除图标 |
| Detailed goal | [Textarea](../../components/Textarea/spec.md) | ✗ | 多行文本 |
| Category | [Select](../../components/Select/spec.md) | ✓ | 下拉选择 |
| Due date | [DatePicker](../../components/DatePicker/spec.md) | ✗ | 日期选择 |

## 还原节点 ID

- 页面根节点: `28244:378`
- Form 实例: `28244:6141`
- Field Type: `47211:209`

## 相关文档

- [structure.md](structure.md) — 完整图层结构
- [assembly.md](assembly.md) — 组件组装清单
