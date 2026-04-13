# figma-plugin

Figma 设计系统知识库

---

## 项目简介

这是一个用于管理和沉淀 Figma 设计规范的实验性项目。通过结构化的文档和可执行的脚本，实现设计资产的版本化和复用。

## 目录结构

```
figma-plugin/
├── figma-wiki/              # 设计知识库
│   ├── tokens/             # 设计变量
│   │   ├── colors.md       # 全局色板：品牌色/中性色/语义色
│   │   ├── typography.md    # 字体阶梯：Inter, 12-24px
│   │   ├── spacing.md      # 间距系统：基于 4px 网格
│   │   └── radius.md       # 圆角规范：4/8/12px
│   ├── components/          # 组件规范
│   │   ├── FormItem/       # 表单容器（上下/左右布局）
│   │   ├── Input/          # 单行输入框
│   │   ├── Textarea/       # 多行文本框
│   │   ├── Select/         # 下拉选择
│   │   ├── DatePicker/    # 日期选择器
│   │   ├── Button/        # 按钮
│   │   ├── Card/          # 容器卡片
│   │   ├── Table/         # 数据表格
│   │   └── ...
│   ├── pages/             # 页面模板
│   │   ├── BasicForm/     # 基础表单页
│   │   └── SearchTable/   # 搜索表格页
│   └── tooling/           # 工具文档
│       ├── api-patterns.md # Figma API 命令模式
│       ├── variables.md    # Variables 变量绑定
│       └── common-errors.md # 已知错误和解决方案
├── scripts-examples/        # 可复用脚本
├── scripts-temp/           # 临时脚本（会话结束删除）
├── CLAUDE.md              # Agent 使用指南
└── bridge_client.py       # Python ↔ Figma 桥接工具
```

---

## 核心功能

- **组件规范文档化** - 记录组件的尺寸、样式、变体和 Auto Layout 属性
- **页面结构还原** - 通过节点 ID 快速克隆和还原页面
- **Auto Layout 最佳实践** - 记录布局模式（左右/上下）、间距、对齐规则
- **Variables 变量管理** - 绑定文本到变量实现批量修改
- **脚本驱动设计** - 通过 Python 脚本直接操作 Figma 画布

---

## 记忆库搭建思路

本项目的核心目标是将 Figma 设计资产转化为可复用、可执行的数字资产。

### 阶段一：基础设施

**1. 定义 Design Tokens**

Tokens 是设计系统的基础，确保全局一致性。

```
颜色 Token    → 品牌色、中性色、语义色
字体 Token    → 字号、字重、字体族
间距 Token    → 基于 4px 网格
圆角 Token    → 小/中/大 圆角
```

**2. 建立文档结构**

```
figma-wiki/
├── tokens/       # 先建，设计系统根基
├── components/    # 再建，沉淀可复用组件
├── pages/        # 最后建，整合组件形成页面
└── tooling/      # 同步建设，记录工具经验
```

### 阶段二：组件沉淀

**1. 从原子组件开始**

优先建设最底层、最通用的组件：

```
原子组件：Input → Textarea → Select → Button
         ↓
复合组件：FormItem → Form
```

**2. 组件规范内容**

每个组件文档包含：

| 内容 | 说明 |
|------|------|
| 元信息 | 组件名称、类型、Figma ID |
| 尺寸规格 | 高度、宽度、圆角 |
| 样式 | 背景色、边框色、间距 |
| 结构 | 完整的图层层级 |
| Auto Layout | 布局模式、对齐方式、间距 |
| 还原脚本 | 可执行的克隆代码 |

**3. Auto Layout 经验沉淀**

Auto Layout 是 Figma 设计系统的核心，需要记录：

```
左右布局：
├── layoutMode: HORIZONTAL
├── itemSpacing: 105        # label → Field 间距
├── counterAxisAlignItems: CENTER  # Input 垂直居中
└── counterAxisAlignItems: MIN    # Textarea 顶部对齐

上下布局：
├── layoutMode: VERTICAL
├── itemSpacing: 4         # label → Field 间距
└── counterAxisAlignItems: MIN
```

### 阶段三：页面提取

**1. 选择典型页面**

识别项目中重复出现的页面类型：

```
表单类型：BasicForm / AdvancedForm
列表类型：SearchTable / DataList
详情类型：DetailPage
```

**2. 完整结构记录**

每个页面文档包含：

```
页面规格 → 业务场景、布局参数
图层结构 → 完整节点 ID、层级关系
组装清单 → 组件拼接顺序、间距规则
还原脚本 → 一键克隆到画布
```

**3. 节点 ID 管理**

节点 ID 是 Figma 原生提供的唯一标识：

```javascript
// 通过 ID 克隆页面
var source = await figma.getNodeByIdAsync('28244:378');
var copy = source.clone();
```

### 阶段四：工具链建设

**1. Bridge 桥接系统**

```
Python (bridge_client.py) → Node.js (server.js) → Figma Plugin API
```

实现从本地脚本直接操作 Figma 画布：

```python
from bridge_client import send, read

send("figma code...")  # 执行代码
read()                  # 读取选中节点
```

**2. Variables 变量绑定**

将文本节点绑定到 Variables：

```javascript
// 创建变量
var variable = figma.variables.createVariable('Title', collection, 'STRING', modeId);

// 绑定到节点
node.setBoundVariable('characters', variable);
```

**3. 常见错误记录**

将踩过的坑文档化：

```
❌ detach + remove 破坏布局    → ✅ 使用 visible = false
❌ 直接修改 INSTANCE 内部     → ✅ 优先用 visible 属性
❌ 忘记加载字体               → ✅ 使用 loadFontAsync
```

### 阶段五：持续迭代

**1. 增量扩展**

```
新页面 → 提取结构 → 更新 wiki
         ↓
      新组件 → 补充规范 → 更新索引
```

**2. 经验沉淀**

每次操作遇到问题后：
1. 解决当前问题
2. 记录解决方案到 tooling
3. 更新 CLAUDE.md 供 Agent 参考

**3. 索引维护**

随着知识库扩大，保持索引清晰：

```
_index.md  → 总览，入口
spec.md    → 规格说明
structure.md → 结构定义
assembly.md  → 组装指南
```

---

## 声明

> ⚠️ **实验性项目**
>
> 本项目目前处于实验阶段，主要用于作者个人测试和 GitHub 项目管理。
>
> 暂未对外开放，不追求 Star 或社区贡献。
>
> 代码和文档可能随时重构，不保证向后兼容。

---

## 相关链接

- [CLAUDE.md](CLAUDE.md) - Agent 使用指南
- [figma-wiki/_index.md](figma-wiki/_index.md) - 知识库索引
- [tooling/api-patterns.md](figma-wiki/tooling/api-patterns.md) - API 命令模式

---

## License

[MIT](LICENSE)
