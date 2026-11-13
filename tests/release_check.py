"""Verify the installed parser against random and exhaustive official addresses."""

from argparse import ArgumentParser
from collections import Counter, defaultdict
from itertools import product
from random import Random

from regressions import check_issues

from address_dimensions import parse_address, parse_address_excel
from chinese_address_generator import Address, AddressGenerator, get_data_metadata, load_divisions

MIN_SAMPLES = 500_000
SEED = 20261113
REGION_SHORT_NAMES = dict(zip(
    ("内蒙古自治区", "广西壮族自治区", "西藏自治区", "新疆维吾尔自治区",
     "宁夏回族自治区", "香港特别行政区", "澳门特别行政区"),
    ("内蒙古", "广西", "西藏", "新疆", "宁夏", "香港", "澳门"),
))
EXPECTED_COUNTS = {1: 33, 2: 333, 3: 2845, 4: 38723}


def check(address, detail="", value=None):
    # Pass only names and the optional detail to the parser. Keep the code
    # and structured fields exclusively on the expected side.
    if value is None:
        value = address.full_name + detail
    expected = {
        "province": address.province,
        "city": address.prefecture,
        "district": address.county,
        "township": address.township,
        "adcode": address.code,
        "detail": detail,
        "status": "matched",
        "candidate_codes": (),
        "data_version": "2025-12-31",
    }
    actual = parse_address(value)
    if actual != expected:
        raise AssertionError(f"{value!r}\nexpected: {expected}\nactual: {actual}")


def main():
    cli = ArgumentParser()
    cli.add_argument("--samples", type=int, default=MIN_SAMPLES)
    args = cli.parse_args()
    if args.samples < MIN_SAMPLES:
        cli.error("at least 500,000 random cases are required")
    check_issues()

    divisions = load_divisions()
    counts = Counter(division.level for division in divisions)
    assert counts == EXPECTED_COUNTS, counts
    by_code = {division.code: division for division in divisions}
    assert len(by_code) == len(divisions)
    assert get_data_metadata()["data_as_of"] == "2025-12-31"

    names = set()
    omissions = defaultdict(set)
    for division in divisions:
        parts = [division]
        while parts[-1].parent_code:
            parent = by_code[parts[-1].parent_code]
            assert parent.level < parts[-1].level
            parts.append(parent)
        address = Address(tuple(reversed(parts)))
        assert address.full_name not in names, address.full_name
        names.add(address.full_name)
        check(address)
        check(address, "东华路88号3栋")
        choices = []
        for part in address.divisions:
            variants = [part.name]
            if part.name in REGION_SHORT_NAMES:
                variants.append(REGION_SHORT_NAMES[part.name])
            elif part.level in (1, 2) and part.name[-1] in "省市":
                variants.append(part.name[:-1])
            if part.code != address.code:
                variants.append("")
            choices.append(variants)
        for variant in product(*choices):
            omissions["".join(variant)].add(address.code)
    print(f"Exhaustive: {len(names):,} distinct addresses, each checked with and without detail")

    for value, expected in omissions.items():
        row = parse_address(value)
        actual = set(row["candidate_codes"] or (row["adcode"],))
        assert actual == expected and row["detail"] == "", (value, expected, row)
    print(f"Exhaustive omissions and aliases: {len(omissions):,} distinct spellings")

    generator = AddressGenerator(seed=SEED)
    rng = Random(SEED + 1)
    modes = Counter()
    for index in range(args.samples):
        level = (index % 4) + 1
        address = generator.generate(level=level)
        parts = address.divisions
        mode = rng.randrange(4)
        modes[mode] += 1
        if mode == 0:
            check(address)
        elif mode == 1:
            detail = f"东华路{rng.randrange(1, 100000)}号"
            value = rng.choice(("中国大陆", "中国", "")) + rng.choice((" ", "，", "")).join(
                part.name for part in parts
            )
            check(address, detail, value + detail)
        else:
            kept = [part.name for part in parts[:-1] if rng.getrandbits(1)]
            value = "".join((*kept, parts[-1].name))
            expected = omissions[value]
            row = parse_address(value)
            actual = set(row["candidate_codes"]) if row["status"] == "ambiguous" else {row["adcode"]}
            assert expected == actual and address.code in actual and row["detail"] == "", (
                value, expected, row
            )
            if len(actual) == 1:
                check(address, value=value)
        if (index + 1) % 500_000 == 0:
            print(f"Random cases passed: {index + 1:,}", flush=True)
    print(f"Random cases: {args.samples:,}; distribution by variant: {dict(modes)}")

    assert parse_address("朝阳区")["candidate_codes"] == ("110105", "220104")
    assert parse_address_excel("朝阳区")["candidate_codes"] == "110105、220104"
    assert parse_address("假县")["status"] == "unmatched"
    assert parse_address("合作共赢")["status"] == "unmatched"
    assert parse_address("广东省东莞市虎门镇")["district"] is None
    assert parse_address("北京市朝阳区")["city"] is None
    print("Release check: 100% exact field matches")


if __name__ == "__main__":
    main()
