"""Expected results for independently selected issue examples."""

from address_dimensions import parse_address

CASES = (
    (2, "内蒙古阿拉善盟阿拉善左旗巴彦浩特镇", "matched", "152921100", ""),
    (9, "新疆阿克苏地区阿克苏市实验林场二队", "matched", "652901", "实验林场二队"),
    (21, "云南省楚雄彝族自治州得3434343", "matched", "532300", "得3434343"),
    (26, "内蒙古鄂尔多斯市乌审旗", "matched", "150626", ""),
    (33, "兴安盟", "matched", "152200", ""),
    (36, "上海市浦东新区芳甸路", "matched", "310115", "芳甸路"),
    (59, "甘肃兰州", "matched", "620100", ""),
    (60, "南京市高淳区砖墙总部经济产业园", "matched", "320118", "砖墙总部经济产业园"),
    (64, "北京市密云区经济开发区西统路8号", "matched", "110118", "经济开发区西统路8号"),
    (68, "江西省南昌市新建区望城新区丰泽花园", "matched", "360112", "望城新区丰泽花园"),
    (69, "上海市虹口区四川北路东宝兴路", "matched", "310109", "四川北路东宝兴路"),
    (70, "黑龙江省安达市朝阳街168号", "matched", "231281", "朝阳街168号"),
    (77, "平度市", "matched", "370283", ""),
    (89, "吉林延吉市公园街", "matched", "222401", "公园街"),
    (112, "广东省中山市沙溪镇", "matched", "442000106", ""),
    (112, "陕西省榆林市神木市", "matched", "610881", ""),
    (3, "新疆", "matched", "650000", ""),
    (6, "吉林", "ambiguous", None, ""),
    (12, "福建省鼓楼区", "matched", "350102", ""),
    (23, "上海 上海市 徐汇区 陕西南路666弄", "matched", "310104", "陕西南路666弄"),
    (27, "万宁市万宁中学", "matched", "469006", "万宁中学"),
    (39, "启东市台湾风情街", "matched", "320681", "台湾风情街"),
    (41, "上海市徐汇区桂林路369号", "matched", "310104", "桂林路369号"),
    (42, "天津市", "matched", "120000", ""),
    (46, "合作共赢", "unmatched", None, "合作共赢"),
    (56, "广东省南昌市南山区粤海街道", "conflict", None, "南昌市南山区粤海街道"),
    (67, "上海市广东路689号", "matched", "310000", "广东路689号"),
    (78, "朝阳区汉庭酒店大山子店", "ambiguous", None, "汉庭酒店大山子店"),
    (86, "五大连池市", "matched", "231182", ""),
    (87, "漠河市", "matched", "232701", ""),
    (88, "江苏省鼓楼区琵琶街道办事处复兴北路", "matched", "320302008", "办事处复兴北路"),
    (89, "吉林通化市东昌区江南大街与江畅路交汇处", "matched", "220502", "江南大街与江畅路交汇处"),
    (95, "假县", "unmatched", None, "假县"),
    (98, "安徽省马鞍山市当涂县", "matched", "340521", ""),
    (113, "广东省深圳市龙华区", "matched", "440309", ""),
    (121, "安徽省池州市教育园区池州学院内", "matched", "341700", "教育园区池州学院内"),
    (125, "朝阳区", "ambiguous", None, ""),
    (126, "县科技局", "unmatched", None, "县科技局"),
    (131, "广东省东莞市虎门镇", "matched", "441900121", ""),
    ("jobs", "中国大陆重庆市江北区庆云路1号", "historical", "500105", "庆云路1号"),
    (132, "那曲市", "matched", "540600", ""),
)


def check_issues():
    # The same text can be a formal township or a city alias plus a township.
    assert parse_address("上海庙镇")["candidate_codes"] == ("150623106", "310151103")
    for issue, address, status, code, detail in CASES:
        row = parse_address(address)
        actual = row["status"], row["adcode"], row["detail"]
        assert actual == (status, code, detail), (issue, address, actual)


if __name__ == "__main__":
    check_issues()
