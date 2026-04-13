# 间距系统

## 元信息
- 最后更新: 2026-04-13
- 基础网格: 4px

## 间距阶梯

| Token | 值 | 典型用途 |
|-------|-----|---------|
| $space-xxs | 4px | 图标与文字间距 |
| $space-xs | 8px | 紧凑元素间距、小 padding |
| $space-sm | 16px | 标准 itemSpacing |
| $space-md | 24px | Card/区块 padding |
| $space-lg | 32px | 区块间距、大 gap |

## Figma Auto Layout 对应

```javascript
// 标准 Card padding
frame.paddingLeft = 24;   // $space-md
frame.paddingRight = 24;  // $space-md
frame.paddingTop = 24;    // $space-md
frame.paddingBottom = 24; // $space-md

// 标准内容间距
frame.itemSpacing = 16;   // $space-sm
```
