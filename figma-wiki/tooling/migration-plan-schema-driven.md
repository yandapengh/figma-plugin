# Grab 迁移计划（Legacy -> Schema-Driven）

## 目标

- 去除硬编码 grab。
- schema 变化可自动适配（通过 schema registry + extractor mapping）。
- 保证非破坏迁移。

## 阶段

1. 样本冻结：对现有典型页面保留 legacy 抽取结果。
2. 双轨输出：新抽取器并行输出 schema 结果，仅做 diff。
3. 校验门控：接入五层验证，未通过不允许进入写入流程。
4. 人工确认：similar/new page 走不同决策动作。
5. 切换与回滚：默认 schema，保留 legacy adapter 回滚。

## 兼容策略

- 包装层保持 `read()` 输出 envelope 稳定。
- 增加 `schemaVersion` 字段。
- legacy 使用 adapter 映射到新结构，避免调用端一次性改造。
