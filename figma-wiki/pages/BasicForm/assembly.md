# Basic Form 组件组装清单

## 布局结构

```
page-container (1232×813)
├── Page-Header (1232×131)
│   ├── Breadcrumb (186×22)
│   ├── Title: "Basic Form" (808×44)
│   └── 描述文字 (1184×17)
└── card body (1232×662)
    └── wrapper (1184×662, 居中)
        └── Form (548×614, 居中)
            └── Field Type (484×614)
                └── [Form-Item × 5 + Button-Group]
```

## 布局参数

| 容器 | 宽度 | 备注 |
|------|------|------|
| page-container | 1232px | 内容区 |
| wrapper | 1184px | 留白 24px |
| Form | 548px | 表单宽度 |
| Field Type | 484px | 表单项宽度 |

## 垂直间距

| 元素 | 间距 |
|------|------|
| Page-Header → card body | 0 (紧邻) |
| wrapper → Form | 24px |
| Form-Item 之间 | 56px |
| Form-Item → Button-Group | 32px |

## 组装顺序

1. 创建 page-container
2. 添加 Page-Header (Breadcrumb + Title + 描述)
3. 添加 card body / wrapper
4. 添加 Form / Field Type
5. 按顺序添加 Form-Item:
   - Input (Title)
   - Input (Goal)
   - Textarea
   - Select
   - DatePicker
6. 添加 Button-Group

## 相关文档

- [spec.md](spec.md) — 页面规格
- [structure.md](structure.md) — 节点 ID
