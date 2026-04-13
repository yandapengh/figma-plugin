# Figma API 命令模式

## 基础命令

```python
from bridge_client import send, read

read()           # 读取选中节点
send("JS代码")   # 执行代码（必须 IIFE 包装）
```

## 核心技巧

### 1. 字体加载（必须）

任何文字操作前必须加载字体：

```javascript
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });
```

### 2. IIFE 包装（必须）

Figma 插件环境要求所有代码使用 IIFE：

```javascript
(function(){
  var f = figma.createFrame();
  f.name = "Test";
  return f.id;
})()
```

### 3. Auto Layout

```javascript
frame.layoutMode = "VERTICAL";     // 垂直布局
frame.layoutMode = "HORIZONTAL";   // 水平布局

frame.itemSpacing = 16;            // $space-sm
frame.paddingLeft = 24;            // $space-md
frame.paddingRight = 24;
frame.paddingTop = 24;
frame.paddingBottom = 24;
frame.counterAxisAlignItems = "CENTER";
```

### 4. 创建 Frame

```javascript
var f = figma.createFrame();
f.name = "Name";
f.resize(width, height);
f.layoutMode = "VERTICAL";
f.fills = [{type: "SOLID", color: {r: 0.94, g: 0.95, b: 0.96}}]; // $color-bg-page
parent.appendChild(f);
```

### 5. 创建 Text

```javascript
var t = figma.createText();
t.characters = "文字";
t.fontSize = 14;  // $font-size-sm
t.fills = [{type: "SOLID", color: {r: 0.2, g: 0.2, b: 0.2}}]; // $color-text-primary
parent.appendChild(t);
```

## 常用操作模式

### 查找并修改子节点

```javascript
var page = await figma.getNodeByIdAsync('页面ID');
var target = page.findOne(n => n.name === '组件名');
target.属性 = 新值;
```

### 动态添加子节点

```javascript
for(var i = 0; i < 数量; i++) {
  var item = figma.createFrame();
  item.name = '名称' + i;
  item.resize(宽, 高);
  parent.appendChild(item);
}
```

### 替换组件

```javascript
var old = parent.findOne(n => n.name === '旧组件');
var newOne = figma.createFrame();
newOne.name = '新组件';
parent.appendChild(newOne);
```

### 操作列特殊处理

```javascript
columns.forEach((col, index) => {
  if (col.name === "Actions") {
    var viewText = figma.createText();
    viewText.characters = "View";
    cell.appendChild(viewText);
  }
});
```

## 快速模板

### 标准页面框架

```javascript
(async function(){
  var page = figma.createFrame();
  page.name = '页面名';
  page.resize(1440, 900);
  page.layoutMode = 'VERTICAL';
  page.itemSpacing = 24;  // $space-md
  page.fills = [{type: 'SOLID', color: {r:0.94, g:0.95, b:0.96}}]; // $color-bg-page

  var header = figma.createFrame();
  header.name = 'Header';
  header.resize(1192, 100);
  header.layoutMode = 'VERTICAL';
  header.fills = [{type: 'SOLID', color: {r:1, g:1, b:1}}]; // $color-bg-container
  page.appendChild(header);

  var content = figma.createFrame();
  content.name = 'content';
  content.resize(1192, 700);
  content.layoutMode = 'VERTICAL';
  page.appendChild(content);

  return page.id;
})()
```

### 嵌套结构参考

```
Page (VERTICAL)
├── Search_Bar (HORIZONTAL)
│   ├── Input
│   └── Button
└── Table (VERTICAL)
    ├── Header_Row (HORIZONTAL)
    │   ├── Cell_ID
    │   ├── Cell_Name
    │   └── Cell_Actions
    └── Data_Row (HORIZONTAL)
        ├── Cell_Data
        └── Cell_Actions
```

## INSTANCE 操作最佳实践

### 隐藏 vs 删除

在 INSTANCE 中隐藏元素时，**优先使用 `visible = false`**，而不是 `detachInstance()` + `remove()`。

| 方式 | 代码 | 效果 |
|------|------|------|
| ❌ 删除 | `node.detachInstance(); node.remove();` | 破坏 Auto Layout 联动 |
| ✅ 隐藏 | `node.visible = false;` | 保持布局完整 |

```javascript
figma.getNodeByIdAsync('179528:11492').then(function(form){
  var fieldType = form.findOne(function(n){ return n.name === 'Field Type'; });
  var radio = fieldType.findOne(function(n){ return n.name === 'Form-Item/Radio'; });
  radio.visible = false;  // 隐藏而不是删除
});
```

### 何时用 detachInstance()

只有当需要**修改 INSTANCE 内部的具体内容**（如文字、样式）时才用 detach：

```javascript
var instance = parent.findOne(function(n){ return n.name === 'Form-Item'; });
var detached = instance.detachInstance();
detached.name = 'Modified Form-Item';
```

### 总结

| 需求 | 操作 |
|------|------|
| 隐藏/排除某元素 | `node.visible = false` |
| 修改 INSTANCE 内的文字 | 先 `detachInstance()` 再修改 |
| 在 INSTANCE 内插入元素 | 不支持，必须 detach 或替换 |

## 相关

- [bridge.md](bridge.md) — 桥接系统架构
- [common-errors.md](common-errors.md) — 已知错误
