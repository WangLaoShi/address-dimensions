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

### 最终测试结果

**合成样本和 Issue 回归全部通过。真实招聘地址有 16,994 / 17,089 行（99.44%）通过来源城市和显式区县双重核对。**

| 验收项目 | 结果 |
| --- | --- |
| 随机生成地址 | 10,000,000 / 10,000,000 通过 |
| 完整区划路径，分别带和不带详情 | 83,868 / 83,868 次检查通过 |
| 不同的省略和简称写法 | 659,228 / 659,228 通过 |
| 上游 Issue 回归 | 覆盖 38 条 Issue，所有用例通过 |

合成用例使用固定随机种子 `20261113` 和 `chinese-address-generator==1.0.0`，在 macOS / Python 3.12 上验证。歧义用例通过的条件是返回完整的预期候选。真实样本的 99.44% 是城市和区县双重核对通过率，按 CSV 行计算，包含重复地址。

### 从项目根目录复现

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install .
python tests/regressions.py
python tests/release_check.py                     # 50 万随机样本 + 全量检查
python tests/release_check.py --samples 10000000  # 1,000 万随机样本 + 全量检查
```

## 真实地址回归

本次从本地 ByteDance 招聘数据提取 `address` 和 `city_name` 到 `tests/data/jobs-addresses.csv`，共 17,089 行、349 个不同地址。运行 `python tests/audit_jobs.py` 可生成逐行审查表 `tests/data/jobs-audit.csv`。两份数据文件都留在本地。

审查通过来源城市字段和地址中显式写出的区县核对 16,994 行（313 个不同地址）。另有 12 行为重庆历史地址、16 行只核对到城市或特别行政区、58 行缺少可直接判定的区划、9 行为海外地址。这里核对的是地址文本的行政区划归属，楼宇和门牌没有独立真值。

### 从原始招聘 CSV 复现

在项目根目录运行以下命令。原始文件路径可以替换为本机路径。

```bash
python - ../ByteDance/Chapter1/data/jobs.csv <<'PYTHON'
import csv
import sys
from pathlib import Path

target = Path("tests/data/jobs-addresses.csv")
target.parent.mkdir(parents=True, exist_ok=True)
fields = ("address", "city_name")
with open(sys.argv[1], encoding="utf-8-sig", newline="") as source, \
        target.open("w", encoding="utf-8", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for row in csv.DictReader(source):
        writer.writerow({field: row[field] for field in fields})
PYTHON
python tests/audit_jobs.py
```

真实地址审查需要同一份原始 CSV。测试脚本纳入 Git，招聘样本及逐行审查表由上述命令在本地生成。

## 上游调研

- [项目对比、复测与方案](docs/research.md)
- [cpca 117 条 Issue 逐条审查](docs/issue-review.md)
