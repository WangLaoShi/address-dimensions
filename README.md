# address-dimensions

面向表格分析的中文地址结构化项目。本阶段完成了上游调研和首版设计。

- [项目对比、复测与方案](docs/research.md)
- [cpca 117 条 Issue 逐条审查](docs/issue-review.md)

建议首版提供纯 Python 的 `parse_address()`，返回省、市、区县、详情、区划代码和解析状态。明确区分同名歧义、层级冲突、部分匹配和无匹配。现阶段仓库包含研究文档，解析器尚未实现。
