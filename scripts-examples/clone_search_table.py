from bridge_client import send

# 核心：通过克隆已有组件来还原页面
code = """(function(){
// 1. 获取源页面容器
var sourcePage = figma.getNodeById("64462:1761");
if(!sourcePage) return "Source not found";

// 2. 克隆整个页面
var newPage = sourcePage.clone();
newPage.x = 2000;  // 移到右侧避免重叠
newPage.y = 100;
newPage.name = "Search Table (Cloned)";

// 3. 重置位置
var container = newPage.findOne(n => n.name === "page-container");
if(container) {
  container.x = 0;
  container.y = 0;
}

return "Cloned: " + newPage.id + " from " + sourcePage.id;
})()"""

r = send(code)
print("Result:", r)
