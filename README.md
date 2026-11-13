# address-dimensions

面向表格分析的中文地址结构化工具。首版支持省、地、县、乡四级正式名称，保留门牌等剩余详情。运行时离线，使用一个无第三方依赖的区划数据包，无需 pandas。

```python
from address_dimensions import parse_address, parse_address_excel

row = parse_address("广东省东莞市虎门镇东华路88号")
assert row["city"] == "东莞市"
assert row["district"] is None
assert row["township"] == "虎门镇"
assert row["adcode"] == "441900121"
assert row["detail"] == "东华路88号"

row = parse_address_excel("朝阳区")
assert row["status"] == "ambiguous"
assert row["candidate_codes"] == "110105、220104"
```

解析采用正式名称的最长连续区划前缀。支持省略任意上级、常见省市简称及地址开头重复的省市名。唯一命中时补齐上级，同名时返回候选。部分显式省市冲突会标记为 `conflict`。Excel 版把候选代码转为单个文本单元格。历史映射目前覆盖样本中的重庆江北区，全文多地址抽取仍待实现。

## 区划数据

固定使用 [chinese-address-generator 1.0.0](https://github.com/Ginkgoty/chinese-address-generator) 提供的快照，截止 2025-12-31，来源为[民政部国家地名信息库](https://dmfw.mca.gov.cn/XzqhVersionPublish.html)。数据和校验范围见[数据核查](docs/generator-data.md)。

## 发布验收

构建并安装待发布的 wheel 后运行 `python tests/release_check.py`。任何一条样本逐字段比对失败，都必须修复后再发布。GitHub Actions 在主分支、拉取请求和版本标签上运行同一检查。

- 默认随机校验 500,000 条地址。用 `python tests/release_check.py --samples 10000000` 运行大样本验收。固定种子，覆盖四级、上级省略、中国前缀、空白与逗号分隔及合成门牌。省略导致歧义时核对完整的候选代码集合。
- 额外全量遍历 41,934 条区划路径，分别验证纯区划名称和追加详情两种输入，同时遍历 659,228 种不同的省略和简称写法。
- 只把地址文本交给解析器。区划代码和各级名称来自生成器的结构化结果，用来逐字段核对。
- 另有 38 条上游 Issue 的回归样例，包括同名、路名误命中、父级冲突、直辖市及市直管镇。

## 真实地址回归

本次从本地 ByteDance 招聘数据提取 `address` 和 `city_name` 到 `tests/data/jobs-addresses.csv`，共 17,089 行、349 个不同地址。运行 `python tests/audit_jobs.py` 可生成逐行审查表 `tests/data/jobs-audit.csv`。两份数据文件都留在本地。

审查通过来源城市字段和地址中显式写出的区县核对 16,994 行（313 个不同地址）。另有 12 行为重庆历史地址、16 行只核对到城市或特别行政区、58 行缺少可直接判定的区划、9 行为海外地址。这里核对的是地址文本的行政区划归属，楼宇和门牌没有独立真值。

## 上游调研

- [项目对比、复测与方案](docs/research.md)
- [cpca 117 条 Issue 逐条审查](docs/issue-review.md)
