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

解析采用正式名称的最长连续区划前缀。接受从中间层级起写的连续路径，唯一命中时补齐上级，同名时返回候选。Excel 版把候选代码转为单个文本单元格。简称、历史地名、行政层级冲突检测和全文多地址抽取仍待实现。

## 区划数据

固定使用 [chinese-address-generator 1.0.0](https://github.com/Ginkgoty/chinese-address-generator) 提供的快照，截止 2025-12-31，来源为[民政部国家地名信息库](https://dmfw.mca.gov.cn/XzqhVersionPublish.html)。数据和校验范围见[数据核查](docs/generator-data.md)。

## 发布验收

构建并安装待发布的 wheel 后运行 `python tests/release_check.py`。任何一条样本逐字段比对失败，都必须修复后再发布。GitHub Actions 在主分支、拉取请求和版本标签上运行同一检查。

- 随机生成 50,000 条地址，按四个行政级别分层采样，可复现。
- 额外全量遍历 41,934 条区划路径，分别验证纯区划名称和追加详情两种输入。
- 只把地址文本交给解析器。区划代码和各级名称来自生成器的结构化结果，用来逐字段核对。
- 另有同名、普通词误命中、直辖市及市直管镇回归样例。

## 上游调研

- [项目对比、复测与方案](docs/research.md)
- [cpca 117 条 Issue 逐条审查](docs/issue-review.md)
