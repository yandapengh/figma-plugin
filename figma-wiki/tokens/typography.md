# 字体阶梯

## 元信息
- 最后更新: 2026-04-13
- Figma Variable Collection ID: 待获取

## 字体家族

| Token | 值 | 说明 |
|-------|-----|------|
| $font-family-base | Inter | 全局主字体 |

## 字重

| Token | 值 | 用途 |
|-------|-----|------|
| $font-weight-regular | Regular (400) | 正文 |
| $font-weight-medium | Medium (500) | 强调文字 |
| $font-weight-bold | Bold (700) | 标题 |

## 字号阶梯

| Token | 字号 | 行高 | 用途 |
|-------|------|------|------|
| $font-size-xs | 12px | 20px | 辅助说明、Caption |
| $font-size-sm | 14px | 22px | 正文、表单标签 |
| $font-size-md | 16px | 24px | 小标题 |
| $font-size-lg | 20px | 28px | 区块标题 |
| $font-size-xl | 24px | 32px | 页面主标题 |

## 字体加载（Figma API）

```javascript
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });
```
