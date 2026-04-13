# Basic Form 完整结构

## 节点 ID

| 节点 | ID | 类型 | 尺寸 |
|------|-----|------|------|
| Basic Form (根) | `28244:378` | FRAME | 1440×900 |
| page-container | `28244:6279` | FRAME | 1232×813 |
| Page-Header | `28244:6027` | INSTANCE | 1232×131 |
| Breadcrumb | `I28244:6027;56066:111076` | INSTANCE | 186×22 |
| Title | `I28244:6027;56061:53` | INSTANCE | 808×44 |
| 描述文字 | `I28244:6027;56061:106` | INSTANCE | 1184×17 |
| card body | `28244:6140` | FRAME | 1232×662 |
| wrapper | `58047:1` | FRAME | 1184×662 |
| Form | `28244:6141` | INSTANCE | 548×614 |
| Field Type | `I28244:6141;47211:209` | INSTANCE | 484×614 |

## 表单项节点

| 字段 | ID | 类型 | 尺寸 |
|------|-----|------|------|
| Form-Item/Input (Title) | `I28244:6141;47211:209;4473:14` | INSTANCE | 484×56 |
| Form-Item/Input (Goal) | `I28244:6141;47211:209;4473:15` | INSTANCE | 484×56 |
| Form-Item/Textarea | `I28244:6141;47211:209;4473:16` | INSTANCE | 484×100 |
| Form-Item/Select | `I28244:6141;47211:209;4473:17` | INSTANCE | 484×56 |
| Form-Item/DatePicker | `I28244:6141;47211:209;4473:18` | INSTANCE | 484×56 |
| Form-Item/Button-Group | `I28244:6141;47211:209;4473:19` | INSTANCE | 484×56 |

## 完整层级

```
Basic Form (1440×900, $color-bg-page)
├── page-container (1232×813)
│   ├── .Page-Header(Legacy) (1232×131)
│   │   ├── Breadcrumb (186×22)
│   │   │   ├── 1st-item → "Home"
│   │   │   ├── separator
│   │   │   ├── 2nd-item → "Form"
│   │   │   ├── separator
│   │   │   └── last-item → "Basic Form"
│   │   ├── heading-left → "Basic Form"
│   │   └── Text/Paragraph → 描述文字
│   └── card body (1232×662)
│       └── wrapper (1184×662, white)
│           └── Form (548×614, 居中)
│               └── Field Type (484×614)
│                   ├── Form-Item/Input (Title)
│                   │   ├── label → "Title:"
│                   │   └── Field
│                   │       ├── Input-Addon/Label → "http://"
│                   │       ├── input
│                   │       │   ├── input-prefix → User icon
│                   │       │   ├── placeholder → "Give the target a name"
│                   │       │   └── input-suffix → close-circle
│                   │       └── Input-Addon/Icon → Setting icon
│                   ├── Form-Item/Input (Goal)
│                   ├── Form-Item/Textarea
│                   │   ├── label → "Goal description:"
│                   │   └── Textarea → placeholder
│                   ├── Form-Item/Select
│                   ├── Form-Item/DatePicker
│                   └── Form-Item/Button-Group
│                       ├── Button (Primary) → "Submit"
│                       └── Button (Default) → "Reset"
```

## 还原方式

### 克隆页面

```javascript
var source = await figma.getNodeByIdAsync('28244:378');
var copy = source.clone();
copy.x = 2200;
copy.y = 100;
```

## 相关文档

- [spec.md](spec.md) — 页面规格
- [assembly.md](assembly.md) — 组装清单
- [FormItem](../../components/FormItem/spec.md)
- [Input](../../components/Input/spec.md)
