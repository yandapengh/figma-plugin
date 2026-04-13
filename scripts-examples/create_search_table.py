import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bridge_client import send

# 根据 L4-JSX 生成的完整代码
code = """(function(){
// 1. 主页面 Frame
var page = figma.createFrame();
page.name = "Search Table";
page.x = 100;
page.y = 100;
page.resize(1440, 900);
page.layoutMode = "VERTICAL";
page.paddingLeft = 208;
page.paddingRight = 40;
page.paddingTop = 48;
page.paddingBottom = 26;
page.itemSpacing = 24;
page.fills = [{type: "SOLID", color: {r: 0.941, g: 0.949, b: 0.961}}];

// 2. Page-Header
var header = figma.createFrame();
header.name = "Page-Header";
header.resize(1192, 102);
header.layoutMode = "VERTICAL";
header.fills = [{type: "SOLID", color: {r: 1, g: 1, b: 1}}];
page.appendChild(header);

// 2.1 Breadcrumb 容器
var breadcrumb = figma.createFrame();
breadcrumb.name = "Breadcrumb";
breadcrumb.resize(1192, 22);
breadcrumb.layoutMode = "HORIZONTAL";
breadcrumb.counterAxisAlignItems = "CENTER";
header.appendChild(breadcrumb);

// 2.2 Title
var title = figma.createFrame();
title.name = "heading-left";
title.resize(1192, 40);
title.layoutMode = "HORIZONTAL";
title.paddingTop = 6;
header.appendChild(title);

// 3. Content 区域
var content = figma.createFrame();
content.name = "content";
content.resize(1192, 712);
content.layoutMode = "VERTICAL";
content.itemSpacing = 16;
page.appendChild(content);

// 3.1 Card - 搜索表单
var card = figma.createFrame();
card.name = "Card";
card.resize(1192, 80);
card.layoutMode = "HORIZONTAL";
card.itemSpacing = 158;
card.fills = [{type: "SOLID", color: {r: 1, g: 1, b: 1}}];
content.appendChild(card);

// Form-Item 1: Rule Name
var form1 = figma.createFrame();
form1.name = "Form-Item";
form1.resize(400, 32);
form1.layoutMode = "HORIZONTAL";
card.appendChild(form1);

// Form-Item 2: Description
var form2 = figma.createFrame();
form2.name = "Form-Item";
form2.resize(400, 32);
form2.layoutMode = "HORIZONTAL";
card.appendChild(form2);

// 3.2 Buttons
var buttons = figma.createFrame();
buttons.name = "Buttons";
buttons.resize(200, 36);
buttons.layoutMode = "HORIZONTAL";
buttons.itemSpacing = 16;
buttons.fills = [{type: "SOLID", color: {r: 0.09, g: 0.44, b: 1}}];
content.appendChild(buttons);

// 3.3 Table
var table = figma.createFrame();
table.name = "Table";
table.resize(1192, 500);
table.layoutMode = "VERTICAL";
table.fills = [{type: "SOLID", color: {r: 1, g: 1, b: 1}}];
content.appendChild(table);

// Table-Header
var thead = figma.createFrame();
thead.name = "Table-Header";
thead.resize(1192, 52);
thead.layoutMode = "HORIZONTAL";
thead.paddingLeft = 24;
thead.paddingRight = 24;
thead.counterAxisAlignItems = "CENTER";
table.appendChild(thead);

// Table-Row (示例3行)
for(var i = 0; i < 3; i++) {
  var row = figma.createFrame();
  row.name = "Table-Row";
  row.resize(1192, 52);
  row.layoutMode = "HORIZONTAL";
  row.paddingLeft = 24;
  row.paddingRight = 24;
  row.counterAxisSizingMode = "FIXED";
  table.appendChild(row);
}

// 3.4 Pagination
var paging = figma.createFrame();
paging.name = "Pagination";
paging.resize(1192, 44);
paging.layoutMode = "HORIZONTAL";
paging.counterAxisAlignItems = "CENTER";
content.appendChild(paging);

return "Created: " + page.id + " (" + page.width + "x" + page.height + ")";
})()"""

r = send(code)
print("Result:", r)
