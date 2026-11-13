# cpca Issue 逐条审查

截至 2026-11-13，GitHub API 返回 117 条 Issue（70 条开放、47 条关闭），已排除 PR。查阅每条公开正文及 API 返回的 213 条对应评论。#83 标示有 1 条评论，直接请求评论接口仍返回空列表。截图帖以可读取的文字、标题和评论为依据。上游报告修复的条目与本地复测结果分开标注。

「可修」指已有明确的实现方向；「需数据」指要补来源或历史记录；「已处理」指上游已有对应修复或替代接口；「部分处理」指不同子问题需要不同方案。状态为上游 Issue 状态，分类为本次研究结论。项目尚未实现这些修复。


分类计数：范围外 14、已处理 30、可修 26、需数据 24、需外部服务 4、信息不足 4、部分处理 15。

| Issue | 上游状态 | 可见评论 | 判断 | 处理方式与证据 |
| --- | --- | ---: | --- | --- |
| [#1 图床](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/1) | 开放 | 0 | 范围外 | 文档图片托管，无解析缺陷。 |
| [#2 对少数民族地区的地名映射存在问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/2) | 关闭 | 5 | 已处理 | 自治区别名与盟保留原名；勿再拼接市后缀。 |
| [#3 新疆、西藏、宁夏、广西 识别不了](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/3) | 关闭 | 3 | 已处理 | 新版内置五个自治区的简称。 |
| [#6 吉林省与吉林市的识别问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/6) | 关闭 | 2 | 可修 | 吉林省和吉林市均保留候选；用后续地名或显式后缀消歧。 **复测：**两者均直接选吉林省，未暴露候选。 |
| [#7 transform返回dataframe的index缺失](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/7) | 关闭 | 2 | 已处理 | 上游已有 index 参数；新库批量接口按输入顺序保留记录。 |
| [#8 Python2兼容性](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/8) | 关闭 | 8 | 范围外 | Python 2 兼容诉求；新项目按 Python 3 设计。 |
| [#9 新疆自动补全问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/9) | 关闭 | 3 | 已处理 | 自治区简称与阿克苏地区、县级市应走同一父链；上游曾确认修复。 |
| [#10 类似 新疆生产建设兵团第八师一四七团 怎么匹配到 新疆生产建设兵团](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/10) | 关闭 | 1 | 需数据 | 兵团师团有独立组织关系，需专项表；不能按普通区县自动补齐。 |
| [#11 广东省东莞市莞城区东莞大道解析错误的问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/11) | 关闭 | 6 | 需数据 | 莞城区与莞城街道需按年代和层级建模；东莞大道保留在详情。 **复测：**cpca 详情只剩大道海雅百货；fork 给出城区。 |
| [#12 “福建省鼓楼区”的bug](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/12) | 关闭 | 2 | 已处理 | 福建省约束可排除其他鼓楼区，复测见附录。 **复测：**两者均补福州市。 |
| [#13 地址的数据权重如何在热力图中反映](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/13) | 关闭 | 2 | 范围外 | 把权重按区划代码汇总后交给绘图层。 |
| [#14 中文国外地址的经纬度如何用python批量获取？谢谢](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/14) | 开放 | 0 | 需外部服务 | 海外地址批量地理编码要接覆盖目标国家的服务。 |
| [#15 新疆地区在地图上不显示](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/15) | 关闭 | 1 | 范围外 | 旧版绘图渲染问题，上游称 0.3.5 已修复。 |
| [#16 请问如何添加地址](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/16) | 开放 | 4 | 需数据 | 允许注入标准化区划树；港澳台与海外按各自层级及版本加载。 |
| [#17 获取数据异常](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/17) | 开放 | 10 | 信息不足 | PHP 调用得到空解析；需同一解释器、参数编码和最小复现，建议 JSON 输入输出。 |
| [#18 没有地址的情况，还是会有分词](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/18) | 关闭 | 11 | 可修 | 区分无匹配与地址残余；地址栏解析和全文抽取分别提供接口。 |
| [#19 菏泽市没有识别出来](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/19) | 关闭 | 3 | 已处理 | 上游已更新为菏泽市；校验数据并把常见错字作为可配置别名。 |
| [#20 输入地址前的无效内容去除](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/20) | 关闭 | 5 | 可修 | 返回命中区间及前缀，允许调用方选择是否去掉前缀。 |
| [#21 地址解析bug](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/21) | 关闭 | 1 | 已处理 | 旧版可用全文模式绕过分词；新版应直接匹配楚雄彝族自治州全称。 |
| [#22 某些单独的地级市无法被识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/22) | 关闭 | 3 | 已处理 | 讨论定位到 Python 2 环境；秦皇岛等短名继续做回归。 |
| [#23 当传入地址含有省份命名的街道时，会被错误解析](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/23) | 关闭 | 4 | 部分处理 | 上游称新版修复；仍应以父链和街路边界约束陕西南路、澳门路。 **复测：**cpca 保留陕西南路；fork 误判陕西省。 |
| [#24 环境如何搭建](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/24) | 关闭 | 1 | 可修 | 旧 pandas.compat 接口问题；核心使用字典，无 pandas。 |
| [#25 地址套叠](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/25) | 关闭 | 1 | 部分处理 | 保留北京东城区与燕郊的冲突证据；燕郊开发区的归属需要专项地名表。 |
| [#26 鄂尔多斯市  不显示](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/26) | 关闭 | 3 | 已处理 | 上游确认内蒙古、鄂尔多斯、乌审旗可连成父链。 |
| [#27 县级市是不是没法解析？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/27) | 关闭 | 1 | 已处理 | 新版能补出海南；分析输出可将虚拟地级分组留空。 **复测：**cpca 补海南及虚拟地级分组；fork 仅识别万宁市。 |
| [#28 大学校区跨省，解析出的省和市有矛盾](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/28) | 开放 | 0 | 需外部服务 | 大学名称与校区实际位置是 POI 关系；需校区库或地理编码。 |
| [#29 echart版本？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/29) | 开放 | 2 | 范围外 | 旧版 pyecharts API 兼容，绘图独立于解析。 |
| [#30 如何关闭umap warning提示](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/30) | 关闭 | 2 | 已处理 | 旧版曾加 open_warning，新版移除相关日志；新库用结构化状态。 |
| [#31 非行政区向行政区（高新区）匹配](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/31) | 开放 | 0 | 需数据 | 开发区需要独立类型和地理归属，临江高新区不能按临江市补齐。 |
| [#32 地址不带“省、市、区”的也匹配不到](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/32) | 关闭 | 4 | 部分处理 | 杭州短名可入别名；雅山东路靠地址边界和父链避免误识别山东。 |
| [#33 内蒙古部分市级解析不到内蒙古](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/33) | 关闭 | 2 | 已处理 | 上游复测三个盟均可补内蒙古；保留回归用例。 |
| [#34 国家级新区无法识别，比如贵州的贵安新区](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/34) | 开放 | 0 | 需数据 | 贵安新区是功能区，可能涉及多个行政区；单独字段与候选。 |
| [#35 省市区只有省和区存在的地级市，比如湖北仙桃，海南万宁，能匹配出区，但不能根据区匹配省。](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/35) | 开放 | 5 | 可修 | 仙桃、万宁直接连接省；屯县等简称需经核验后收录。 |
| [#36 省略区字无法映射，上海市浦东新区无法识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/36) | 开放 | 4 | 部分处理 | 浦东新区全称可匹配；罗湖短名只有在深圳等上下文足够时接受。 |
| [#37 下城区、上城区被压缩为“城区”](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/37) | 关闭 | 0 | 需数据 | 上城区全称优先；已撤销的下城区用有时效的历史映射。 |
| [#38 该模块是否可以通过向pca.csv添加乡村两级的数据，拆解为五级行政区+地址，大致需要修改哪些代码](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/38) | 关闭 | 0 | 需数据 | 五级须换显式父子结构，并补乡级、村级字典。 |
| [#39 对于类似“启东市台湾风情街”的一种改进策略](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/39) | 开放 | 3 | 可修 | 接受启东父链后保留台湾风情街；不跨地址边界拼接父级。 **复测：**cpca 正确保留详情，fork 误选台湾。 |
| [#40 无法查询已撤销的区](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/40) | 开放 | 1 | 需数据 | 大厂区曾撤销；需历史代码、生效时间及后继映射，可能一对多。 |
| [#41 上海市徐汇区桂林路369号错误识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/41) | 开放 | 1 | 已处理 | 上游称已修复；保留桂林路尾部，不提取桂林市。 |
| [#42 “天津市”在全文匹配模式下，会被拆分成“天津市”、“津市市”](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/42) | 关闭 | 2 | 已处理 | 上游确认天津用例修复；通用规则保留全称并处理重叠。 |
| [#43 对于地名中带有省类别的地址识别错误](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/43) | 关闭 | 2 | 已处理 | 上游有道路误判修复；山西路与老山东里都应进回归。 |
| [#44 对于pyinstaller打包后报错的问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/44) | 开放 | 5 | 可修 | 改用 importlib.resources 并验证 PyInstaller 数据资源收集。 |
| [#45 国外的国家和城市支持？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/45) | 开放 | 1 | 范围外 | 国际地理分级需独立数据和可变层级，建议独立扩展。 |
| [#46 字符串中包含“合作”的识别问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/46) | 开放 | 1 | 可修 | 抑制普通词中的合作简称；合作市全称或明确上级仍可识别。 **复测：**两者均误识别合作市。 |
| [#47 能不能把umap warning提示关闭啊？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/47) | 关闭 | 2 | 已处理 | 旧版已有关闭警告选项，新版日志机制变化。 |
| [#48 加入乡镇功能的复杂度如何？如何实现？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/48) | 开放 | 1 | 需数据 | 乡镇扩展需要独立乡级数据与父级关系。 |
| [#49 建议添加日志等级设置功能](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/49) | 关闭 | 1 | 可修 | 重名返回 ambiguous，可选严格异常；避免依赖日志等级。 |
| [#50 运行setup.py后，应该输入什么呢？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/50) | 开放 | 2 | 可修 | README 给 pip 安装和导入示例。 |
| [#51 当通过命令行运行程序时，程序无法导入capca](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/51) | 关闭 | 0 | 信息不足 | 命令行与 IDE 解释器可能不同；核对 python -m pip 与模块名。 |
| [#52 广州南沙在地址库且唯一但是提示无法映射？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/52) | 关闭 | 2 | 已处理 | 旧版全文模式可识别南沙区；当前用词典全称匹配。 |
| [#53 大量转换时显示省略号](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/53) | 关闭 | 1 | 范围外 | DataFrame 显示截断；通过导出或原生字典迭代读取。 |
| [#54 log 打印过多导致提取速度过慢](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/54) | 关闭 | 0 | 可修 | 高频未匹配用状态返回，避免逐行记录日志。 |
| [#55 能提供爬取自中华人民共和国民政局全国行政区 爬取省 市 区 等的爬虫吗？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/55) | 关闭 | 4 | 需数据 | 从官方快照建立可复现更新流程；讨论中还有黑龙江中路误判，纳入街路回归。 |
| [#56 〔建议功能〕 请增加信息校验功能，比如输入的地址中有错误的校验](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/56) | 开放 | 3 | 可修 | 广东与南昌父链不一致时返回 conflict，可列修正候选但不自动改。 **复测：**cpca 静默推成深圳，fork 保留矛盾父链。 |
| [#57 自己项目引入cpca后如何用pyinstaller -F打包项目到一个exe包含所有依赖,解决错误No module named 'cpca.resources'](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/57) | 开放 | 1 | 可修 | 同 #44，需另外验证单文件打包。 |
| [#58 地名变动](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/58) | 开放 | 1 | 需数据 | 曾用地名要维护有效区间和后继关系。 |
| [#59 甘肃兰州无法识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/59) | 关闭 | 2 | 已处理 | 上游 0.5.1 确认可解析甘肃兰州；历史电白县另建映射。 |
| [#60 南京市高淳区砖墙总部经济产业园，该地址识别问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/60) | 关闭 | 2 | 已处理 | 上游 0.5.1 已能提取高淳区，避免旧分词切断全称。 |
| [#61 关于作者的CPCA模块基于jieba实现分词造成很多分词错误的修改建议！](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/61) | 开放 | 5 | 已处理 | cpca 已替换 jieba；AC 仅负责找词，仍需独立消歧。 |
| [#62 区识别错误](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/62) | 关闭 | 1 | 已处理 | 上游称观山湖区用例已修，匹配区县后不继续在详情找龙泉市。 |
| [#63 请问我想把这个方法打包上传到hadoop集群使用，应该怎么操作？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/63) | 开放 | 0 | 范围外 | 集群部署须在执行节点提供兼容环境和资源；纯 Python 可减少平台依赖。 |
| [#64 地址过长时无法正确识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/64) | 关闭 | 1 | 部分处理 | 长度不应影响已识别前缀；梅列区现行归属还需历史版本。 |
| [#65 发现有的地址已经过期](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/65) | 开放 | 1 | 需数据 | 已有手工更新说明；仍需数据版本、来源和持续更新。 |
| [#66 请问画热力图怎么画到市一级](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/66) | 开放 | 0 | 范围外 | 绘图按市级代码聚合；市中心点和实际地址坐标须区分。 |
| [#67 以省市命名的街道被识别为省了](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/67) | 关闭 | 1 | 已处理 | 上游称修复广东路覆盖上海的问题，复测见附录。 **复测：**两者均保留广东路。 |
| [#68 '江西省南昌市新建区望城新区丰泽花园'无法解析出'新建区'](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/68) | 关闭 | 1 | 已处理 | 上游 0.5.1 确认可解析新建区；不再依赖分词开关。 |
| [#69 采用全词匹配 识别 “上海市虹口区四川北路东宝兴路嘉杰办公楼B2保洁部” 分词到了四川省](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/69) | 关闭 | 1 | 已处理 | 上游确认新版保留四川北路详情。 |
| [#70 关于道路地址中含省市名导致识别错误问题的简单解决方法](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/70) | 开放 | 3 | 已处理 | 上游新版修复朝阳街示例；无需沿用旧 jieba 条件补丁。 |
| [#71 识别报错:  在识别:  浙江省 织里镇 吴兴区织里镇织纺路731号中通快递2栋4号楼中间. 时报错了: AttributeError: 'bool' object has no attribute 'get'](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/71) | 关闭 | 1 | 已处理 | 旧接口把 bool 当成 umap；新接口用关键字参数和类型校验。 |
| [#72 一些云南的自治州简写不能map到](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/72) | 开放 | 1 | 需数据 | 自治州简称可人工审核后入表，并保留同名候选。 |
| [#74 结巴分词精细度默认值设置为可调怎样？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/74) | 关闭 | 3 | 已处理 | 新版已移除 jieba 的 cut_all 诉求；武汉东湖开发区另按功能区。 |
| [#75 数据更新比较慢](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/75) | 开放 | 0 | 需数据 | 宁乡、京山、邵东、坪山的变动靠版本化区划更新和历史别名。 |
| [#76 adcode数据不更新的问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/76) | 开放 | 3 | 需数据 | 第三方快照可做交叉校验；官方快照作为现行区划主来源。 |
| [#77 县级市怎么处理的](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/77) | 关闭 | 0 | 已处理 | 平度市是县级市，应落县级字段，层级独立于名称后缀。 |
| [#78 如何有效识别“朝阳区”](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/78) | 关闭 | 3 | 可修 | 新版支持 umap；默认应返回朝阳区候选，酒店定位需 POI 或业务提示。 **复测：**cpca 默认长春，fork 默认北京。 |
| [#79 找不到"PCA.CSV"文件](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/79) | 开放 | 2 | 已处理 | pca.csv 已换成 adcodes.csv，文档应标明版本。 |
| [#81 直辖市 可以映射出 省市区，但是地址中还包含“省市区”](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/81) | 开放 | 8 | 部分处理 | 新版可切出详情；直辖市展示可用市名，底层保留真实层级；另有旧 Mac 安装问题。 |
| [#82 台湾省的不太完善啊](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/82) | 开放 | 0 | 需数据 | 台中县是历史名称；需台中市和平区等历史关系与独立数据覆盖。 |
| [#83 大数据热力图](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/83) | 开放 | 0 | 范围外 | 按代码预聚合再渲染；缺少可见评论，正文要求热力比例控制。 |
| [#84 广东东莞市只有镇，没有区这种有解决办法没](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/84) | 开放 | 0 | 需数据 | 东莞可市直连乡镇，不能虚构县级；需乡级快照。 |
| [#85 匹配出了错误的结果](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/85) | 开放 | 1 | 部分处理 | 拒绝裸县、核验前郭县别名；公司名称模式下应降低推断力度。 **复测：**cpca 误选重庆，fork 未匹配。 |
| [#86 五大连池市 与 元江县 目前无法匹配正确的省份与城市](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/86) | 开放 | 6 | 部分处理 | 五大连池市要优先于内嵌大连；元江县需要有来源的简称。 **复测：**cpca 误选大连，fork 识别五大连池。 |
| [#87 漠河目前无法识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/87) | 开放 | 3 | 需数据 | 漠河是县级市；更新现行名称和代码，并保留漠河县历史记录。 **复测：**cpca 无匹配，fork 识别漠河市。 |
| [#88 重名(区级名称相同)，匹配结果有误](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/88) | 开放 | 0 | 可修 | 江苏约束下仍有南京与徐州鼓楼区；琵琶街道可消歧，但需乡级数据。 **复测：**cpca 选南京，fork 留空地级。 |
| [#89 简称“吉林”，导致的匹配错误](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/89) | 开放 | 2 | 可修 | 吉林的省市同名必须保存多候选，按通化、延吉、长春的层级与父链消歧。 |
| [#90 尝试：基于044版，增加“建筑物”的概念](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/90) | 开放 | 3 | 需外部服务 | 建筑物映射区县须使用受范围约束的 POI 数据；行政区核心保留详情。 |
| [#91 运行cpca.transform()报错，没有找到 keyword argument 'cut'](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/91) | 开放 | 2 | 已处理 | 0.5.5 已移除 cut，属于旧示例与接口版本不符。 |
| [#92 一些识别错误地址，希望对算法改进有帮助](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/92) | 开放 | 1 | 部分处理 | 保护上海城、朝阳路、山西北路等详情；功能区、旧称、缺上级分别处理。 |
| [#93 有GO版本的吗？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/93) | 开放 | 1 | 范围外 | Go 版本是另一个实现目标。 |
| [#94 支持python2环境吗？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/94) | 开放 | 1 | 范围外 | Python 2 不进入新项目兼容范围；历史讨论提到 fork。 |
| [#95 未匹配的县，结果输出重庆市](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/95) | 开放 | 4 | 可修 | 将重庆的县等虚拟节点排除出词索引，避免假县误判。 **复测：**cpca 误选重庆，fork 未匹配。 |
| [#96 乡镇级别是否可实现？难度如何？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/96) | 开放 | 1 | 需数据 | 乡镇识别依赖覆盖与父链，同 #48。 |
| [#97 深圳的区域龙华坪山无法区分](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/97) | 开放 | 1 | 需数据 | 深圳龙华与坪山需核对数据覆盖；龙华同名用深圳父链约束。 |
| [#98 安徽省马鞍山市当涂县无法解析](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/98) | 开放 | 1 | 部分处理 | 标题给出可测样例；复测及数据需分开判断。 **复测：**两者均识别当涂县。 |
| [#101 一些归属地识别问题](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/101) | 开放 | 1 | 部分处理 | 怀仁等现名、达县等旧名、康巴什新区、崇阳镇和民族县简称应分别入不同表。 |
| [#102 安装失败，2014年的Mac不能正常安装？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/102) | 开放 | 1 | 部分处理 | 评论归因于架构但缺少独立复现；纯 Python 避免依赖 C 扩展，Mac 测试仍需矩阵。 |
| [#105 应新增30个自治州、3个盟等地级行政区划的简称](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/105) | 开放 | 0 | 需数据 | 自治州与盟的简称清单可作为候选，逐项核验后入表。 |
| [#107 使用cpca过程中，报错缺少某些库，如下](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/107) | 开放 | 1 | 可修 | 缺少 ahocorasick 依赖；纯 Python 默认实现，扩展可选。 |
| [#108 希望新增匹配到相似区的异常抛出](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/108) | 开放 | 0 | 可修 | 同名无法区分返回候选，可选抛异常。 |
| [#110 不支持python3.6版本](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/110) | 开放 | 0 | 范围外 | Python 3.6 兼容属于版本策略，需明确支持版本。 |
| [#112 有些地址的区/县/镇无法识别，列表如下](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/112) | 开放 | 5 | 部分处理 | 龙华、坪山、南岔、神木查区划快照；市直管镇需乡级；开发区与历史地名独立。 |
| [#113 adcodes.csv内有龙华区而无法识别](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/113) | 开放 | 0 | 可修 | 龙华区同名与匹配顺序、父级约束应回归，详见复测。 **复测：**cpca 缺深圳龙华，fork 可识别。 |
| [#114 两个省份相连只能识别第一个!](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/114) | 开放 | 0 | 可修 | 多个省份是全文提取任务，逐项给命中区间；吉林仍可能歧义。 **复测：**全文 API 可抽取多个省，但吉林默认选一个。 |
| [#115 如何返回行政区划的经纬度信息？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/115) | 开放 | 0 | 需数据 | 可按代码返回来源明确的行政区代表点，并标注坐标系；地址坐标需地理编码。 |
| [#117 transform_text_with_addrs  输入不含省市区的文本会报错](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/117) | 开放 | 0 | 可修 | 无命中返回空列表；DataFrame 适配器显式给列。 **复测：**cpca 全文 API 无地址时触发 KeyError。 |
| [#119 无法使用csv文件吗](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/119) | 开放 | 0 | 可修 | 用标准库 csv.DictReader 读地址列并保留行号；截图中的具体错误未复现。 |
| [#121 安徽省池州市教育园区池州学院内 地址识别结果是](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/121) | 开放 | 0 | 部分处理 | 池州学院里的池州不应再次消费，详情保留教育园区池州学院内。 **复测：**cpca 详情只剩学院内；fork 保留完整详情。 |
| [#122 import capa的时候能自定义使用自己本地的adcodes.csv么](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/122) | 开放 | 0 | 可修 | 加载器支持显式数据路径和 schema 校验；避免修改安装目录。 |
| [#123 使用echarts进行绘图的时候，会报错 ImportError: cannot import name 'Markup' from 'jinja2' (C:\Python\work\venv\lib\site-packages\jinja2\__init__.py)](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/123) | 开放 | 0 | 范围外 | 旧 pyecharts 与 Jinja2 Markup 接口不兼容；绘图从核心拆出。 |
| [#125 能否新增参数，当只根据区信息无法区分时，给出可能的全部解析让用户选择](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/125) | 开放 | 0 | 可修 | 朝阳区默认返回北京和长春两个候选，用业务上下文消歧。 |
| [#126 县科技局识别错误](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/126) | 开放 | 4 | 可修 | 县不可独立命中；合作部与合作局应用普通词边界及低证据拒识。 **复测：**cpca 误选重庆，fork 未匹配。 |
| [#127 Potential Vulnerability in urllib3==1.25.11](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/127) | 开放 | 0 | 部分处理 | 源码 requirements.txt 锁定旧 urllib3，发布包核心依赖另列；更新锁定并重新扫描。 |
| [#128 详细地址中包含数字的话会报错invalid decimal literal](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/128) | 关闭 | 0 | 信息不足 | invalid decimal literal 可能是 Python 输入未加引号，截图未复现；字符串中数字应直接测试。 |
| [#129 热力图渲染出来是空白也](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/129) | 开放 | 0 | 信息不足 | 绘图空白可能涉及地图资源、网络和版本，需要最小 HTML 样例。 |
| [#130 单位名称也能识别出来吗？逻辑是怎么样的？](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/130) | 开放 | 0 | 需外部服务 | 单位名称是 POI，可命中其中的显式行政区，单位归属需独立数据。 |
| [#131 无法识别广东省东莞市、广东省中山市、海南省儋州市、甘肃省嘉峪关市的行政区](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/131) | 开放 | 0 | 需数据 | 东莞、中山、儋州、嘉峪关支持市直管乡级，区县允许为空。 **复测：**两者识别东莞；虎门镇留在详情。 |
| [#132 无法识别到那曲市](https://github.com/DQinYuan/chinese_province_city_area_mapper/issues/132) | 开放 | 0 | 需数据 | 核对那曲市及色尼区的现行代码，保留那曲地区与那曲县历史映射。 **复测：**cpca 无匹配，fork 识别那曲市。 |
