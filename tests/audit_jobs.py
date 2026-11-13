"""Compare local job addresses with the source city's independent field."""

import csv
import re
from collections import Counter
from pathlib import Path

from address_dimensions import parse_address
from chinese_address_generator import load_divisions

DATA = Path(__file__).parent / "data"
OVERSEAS = {"新加坡", "伦敦", "马德里"}
SHORT = {"香港特别行政区": "香港"}
PROVINCE_SHORT = {"内蒙古自治区": "内蒙古", "新疆维吾尔自治区": "新疆"}


def check_explicit_district(address, city, parsed, by_code, districts):
    # Independent check: find the written district in the leading text and
    # constrain its parent to the separately supplied source city.
    text = re.sub(r"^(?:（Do Not Use）)?中国(?:大陆)?", "", address.strip())
    candidates = set()
    for district in districts.get(city, ()):
        parent = by_code[district.parent_code]
        province = parent if parent.level == 1 else by_code[parent.parent_code]
        district_prefixes = (province.name + parent.name, province.name,
                             PROVINCE_SHORT.get(province.name, province.name.removesuffix("省")), city, "")
        for prefix in district_prefixes:
            location = text.removeprefix(prefix)
            location = re.sub(r"^(?:" + re.escape(city) + r"(?:市)?)+", "", location)
            if location.startswith(district.name):
                candidates.add(district.code)
    endpoint = by_code[parsed["adcode"]]
    code = endpoint.parent_code if endpoint.level == 4 else endpoint.code
    return candidates == {code}


def main():
    by_code = {division.code: division for division in load_divisions()}
    districts = {}
    for division in by_code.values():
        if division.level == 3:
            city = by_code[division.parent_code].name.removesuffix("市")
            districts.setdefault(city, []).append(division)

    counts = Counter()
    distinct = set()
    verified_addresses = set()
    with (DATA / "jobs-addresses.csv").open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    with (DATA / "jobs-audit.csv").open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(("row", "address", "source_city", "province", "city", "district",
                         "township", "adcode", "detail", "audit"))
        for index, row in enumerate(rows, 1):
            address, city = row["address"], row["city_name"]
            distinct.add(address)
            parsed = parse_address(address)
            inferred = parsed["city"] or parsed["province"] or ""
            short_city = SHORT.get(inferred, inferred.removesuffix("市"))
            if city in OVERSEAS:
                status = "overseas" if parsed["adcode"] is None else "unexpected_overseas_match"
            elif not parsed["adcode"]:
                status = "needs_review"
            elif city.removeprefix("中国") != short_city:
                status = "city_conflict"
            elif parsed["status"] == "historical":
                status = ("historical_city_confirmed" if
                          address.startswith("中国大陆重庆市江北区") and
                          parsed["district"] == "江北区" and parsed["adcode"] == "500105"
                          else "district_needs_review")
            elif not parsed["district"] and not parsed["township"]:
                status = "city_confirmed_only"
            else:
                status = ("explicit_district_verified" if
                          check_explicit_district(address, city, parsed, by_code, districts)
                          else "district_needs_review")
            counts[status] += 1
            if status == "explicit_district_verified":
                verified_addresses.add(address)
            writer.writerow((index, address, city, *(parsed[key] for key in
                            ("province", "city", "district", "township", "adcode", "detail")), status))
    print(f"{len(rows):,} rows, {len(distinct):,} distinct addresses: {dict(counts)}")
    print(f"Explicit district verified on {len(verified_addresses)} distinct addresses")
    if (len(rows) != 17_089 or counts["explicit_district_verified"] < 16_994
            or counts["district_needs_review"] or counts["city_conflict"] or counts["unexpected_overseas_match"]):
        raise AssertionError("See jobs-audit.csv for conflicting rows")


if __name__ == "__main__":
    main()
