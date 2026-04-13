# Table (表格)

## 元信息
- 类型: 原子组件
- Figma Component ID: 待获取
- Figma Component Key: 待获取

## 用途

展示结构化数据列表。

## Tokens 引用

| 属性 | Token |
|------|-------|
| 背景色 | $color-bg-container |
| 表头文字 | $color-text-primary |
| 数据行文字 | $color-text-primary |
| 边框 | $color-border-default |
| 字体 | $font-family-base |
| 字号 | $font-size-sm |

## 结构

```
Table
├── Table-Toolbar（工具栏）
├── Table-Header (HORIZONTAL)
│   ├── Checkbox (32px)
│   ├── Column-1
│   ├── Column-2
│   └── ...
├── Table-Row × N (HORIZONTAL)
│   ├── Checkbox-Cell
│   ├── Data-Cell × N
│   └── Action-Cell
└── Pagination
```

## 列类型

| 列类型 | 说明 | 冻结位置 |
|--------|------|---------|
| Name | 名称（首行冻结） | 左侧 |
| Description | 描述文本 | — |
| Number | 数字 | — |
| Status | 状态标签 | — |
| Time | 时间戳 | — |
| Action | 操作按钮（末行冻结） | 右侧 |

### 列示例（Search Table）

| 列名 | 宽度 | 说明 |
|------|------|------|
| Checkbox | 32px | 行选择 |
| Application Name | 119px | 应用名称 |
| Description | 411px | 描述文本 |
| Service Calls | 115px | 数字 |
| Status | 97px | Online/Offline/Running/Error |
| Last Dispatch Time | 161px | 时间戳 |
| Action | 201px | 操作按钮 |

## Action 列规则

- 最多展示 3 个操作项
- 超出 3 个：显示 2 个 + "更多" Icon
- "更多" Icon 点击后展开 Dropdown

## 状态值

| 状态 | 颜色 Token |
|------|-----------|
| Online | $color-success |
| Offline | $color-text-secondary |
| Running | $color-primary |
| Error | $color-error |

## 相关

- 页面: [SearchTable](../../pages/SearchTable/spec.md)
