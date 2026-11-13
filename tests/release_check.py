"""Verify the installed parser against random and exhaustive official addresses."""

from collections import Counter

from address_dimensions import parse_address, parse_address_excel
from chinese_address_generator import Address, AddressGenerator, get_data_metadata, load_divisions

SAMPLES_PER_LEVEL = (1_000, 4_000, 10_000, 35_000)
SEED = 20261113
EXPECTED_COUNTS = {1: 33, 2: 333, 3: 2845, 4: 38723}


def check(address, detail=""):
    # Pass only names and the optional detail to the parser. Keep the code
    # and structured fields exclusively on the expected side.
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
    generator = AddressGenerator(seed=SEED)
    for level, count in enumerate(SAMPLES_PER_LEVEL, 1):
        for _ in range(count):
            check(generator.generate(level=level))
        print(f"Random L{level}: {count:,}/{count:,} passed", flush=True)

    divisions = load_divisions()
    counts = Counter(division.level for division in divisions)
    assert counts == EXPECTED_COUNTS, counts
    by_code = {division.code: division for division in divisions}
    assert len(by_code) == len(divisions)
    assert get_data_metadata()["data_as_of"] == "2025-12-31"

    names = set()
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
    print(f"Exhaustive: {len(names):,} distinct addresses, each checked with and without detail")

    assert parse_address("朝阳区")["candidate_codes"] == ("110105", "220104")
    assert parse_address_excel("朝阳区")["candidate_codes"] == "110105、220104"
    assert parse_address("假县")["status"] == "unmatched"
    assert parse_address("合作共赢")["status"] == "unmatched"
    assert parse_address("广东省东莞市虎门镇")["district"] is None
    assert parse_address("北京市朝阳区")["city"] is None
    print("Release check: 100% exact field matches")


if __name__ == "__main__":
    main()
