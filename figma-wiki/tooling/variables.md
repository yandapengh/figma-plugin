# Figma Variables 变量绑定

## 用途

将文本绑定到 Variables，方便统一管理和批量修改文本内容。

## API 限制

- `variable.valuesByMode[modeId] = value` 会覆盖为 "String value"
- **解决方案**：绑定前先创建变量，绑定后手动在 Figma 面板调整值

## 操作流程

### 1. 检查并清理重复 Collection

```javascript
return figma.variables.getLocalVariableCollectionsAsync().then(function(collections){
  for (var i = 0; i < collections.length; i++) {
    if (collections[i].name === 'FormLabels') {
      collections[i].remove();
    }
  }
  
  var newCollection = figma.variables.createVariableCollection('FormLabels');
  var modeId = newCollection.modes[0].modeId;
  
  // 继续创建变量...
});
```

### 2. 创建变量并绑定

```javascript
var variables = [
  {name: 'Title', nodeId: '179529:13254'},
  {name: 'GoalDescription', nodeId: '179529:13259'},
  {name: 'Metrics', nodeId: '179529:13269'}
];

var varMap = {};
variables.forEach(function(v) {
  var variable = figma.variables.createVariable(v.name, newCollection, 'STRING', modeId);
  variable.valuesByMode[modeId] = v.name; // 用 name 作为初始值
  varMap[v.name] = variable;
});

var promises = variables.map(function(v) {
  return figma.getNodeByIdAsync(v.nodeId).then(function(node) {
    var variable = varMap[v.name];
    if (node && variable) {
      node.setBoundVariable('characters', variable);
      return {name: v.name, bound: true};
    }
    return {name: v.name, success: false};
  });
});

return Promise.all(promises);
```

### 3. 手动调整变量值

在 Figma Variables 面板中，手动设置每个变量的实际值：
- Title → "Title"
- GoalDescription → "Goal description"
- Metrics → "Metrics"

## 关键代码片段

### 创建 Collection 和变量

```javascript
var collection = figma.variables.createVariableCollection('CollectionName');
var modeId = collection.modes[0].modeId;

var variable = figma.variables.createVariable('VariableName', collection, 'STRING', modeId);
variable.valuesByMode[modeId] = 'initial value';
```

### 绑定到文本节点

```javascript
figma.getNodeByIdAsync('nodeId').then(function(node) {
  node.setBoundVariable('characters', variable);
});
```

### 查找特定变量

```javascript
return figma.variables.getLocalVariablesAsync().then(function(variables){
  var formVars = variables.filter(function(v) {
    return v.collection && v.collection.name === 'FormLabels';
  });
  return formVars;
});
```

## 注意事项

1. **先检查后创建**：避免重复创建同名 Collection
2. **先值后绑定**：在绑定前设置初始值
3. **使用 async API**：`getLocalVariableCollectionsAsync`、`getLocalVariablesAsync`、`getNodeByIdAsync`
4. **绑定属性**：`setBoundVariable('characters', variable)` 用于文本节点

## 相关文档

- [api-patterns.md](api-patterns.md) — API 命令模式
- [common-errors.md](common-errors.md) — 已知错误
