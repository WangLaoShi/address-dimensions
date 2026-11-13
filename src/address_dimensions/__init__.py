"""Parse Chinese administrative addresses using the official division snapshot."""

import re
from collections import defaultdict
from functools import lru_cache
from itertools import combinations, product

from chinese_address_generator import get_data_metadata, load_divisions

__all__ = ["parse_address", "parse_address_excel"]

_FIELDS = ("province", "city", "district", "township")
_SEPARATORS = " \t\r\n,，"
_COUNTRY_PREFIX = re.compile(r"^(?:[（(]do not use[）)]\s*)?中国(?:大陆)?[\s,，]*", re.I)
# The former Jiangbei District was incorporated into Liangjiang New Area.
# Keep the written district and its former code for historical addresses.
_HISTORICAL_DISTRICTS = {"重庆市": ("江北区", "500105")}

_PROVINCE_ALIASES = {
    "内蒙古自治区": "内蒙古",
    "广西壮族自治区": "广西",
    "西藏自治区": "西藏",
    "新疆维吾尔自治区": "新疆",
    "宁夏回族自治区": "宁夏",
    "香港特别行政区": "香港",
    "澳门特别行政区": "澳门",
}


def _alias(division):
    if division.level > 2:
        return None
    return _PROVINCE_ALIASES.get(division.name) or (
        division.name[:-1] if division.name.endswith(("省", "市")) else None
    )


@lru_cache(maxsize=1)
def _address_index():
    divisions = {division.code: division for division in load_divisions()}
    names = defaultdict(dict)
    official_upper = set()
    province_prefixes = []
    for division in divisions.values():
        alias = _alias(division)
        if division.level <= 2:
            official_upper.add(division.name)
        if division.level == 1 and alias:
            province_prefixes.append((alias, division.name))

        path = [division]
        while path[-1].parent_code:
            path.append(divisions[path[-1].parent_code])
        path = tuple(reversed(path))

        for size in range(len(path)):
            for parents in combinations(path[:-1], size):
                options = [(part.name, short) if (short := _alias(part)) else (part.name,)
                           for part in parents]
                for prefix in product(*options):
                    names["".join((*prefix, division.name))][division.code] = path
                    if alias:
                        names["".join((*prefix, alias))][division.code] = path

    return (names, max(map(len, names)), official_upper, tuple(province_prefixes),
            get_data_metadata()["data_as_of"])


def _without_repeated_levels(address, path):
    for start in range(len(path)):
        for end in range(len(path), start, -1):
            if end - start == 1 and end != len(path):
                continue
            repeated = "".join(part.name for part in path[start:end])
            if address.startswith(repeated):
                return address[len(repeated):].lstrip(_SEPARATORS)
    return address


def parse_address(value: str) -> dict[str, object]:
    """Parse formal and abbreviated administrative prefixes and retain details."""
    if not isinstance(value, str):
        raise TypeError("address must be a string")

    address = _COUNTRY_PREFIX.sub("", value.strip(), count=1)
    names, longest, upper, province_prefixes, data_version = _address_index()

    # Compact only the matching view and retain positions in the original text.
    positions = [index for index, char in enumerate(address) if char not in _SEPARATORS]
    compact = "".join(address[index] for index in positions)
    for alias, formal in province_prefixes:
        duplicate = next((prefix for prefix in (formal, alias)
                          if compact.startswith(prefix + formal)), None)
        if duplicate:
            compact = compact[len(duplicate):]
            positions = positions[len(duplicate):]
            break

    result = dict.fromkeys((*_FIELDS, "adcode"))
    result.update(detail=address, status="unmatched", candidate_codes=(), data_version=data_version)
    for end in range(min(longest, len(compact)), 0, -1):
        prefix = compact[:end]
        paths = names.get(prefix)
        if paths is None:
            continue

        # A trailing bare alias such as 广东 in 广东路 is weak evidence.
        candidates = tuple(path for path in paths.values()
                           if end == len(compact) or prefix.endswith(path[-1].name))
        if not candidates:
            continue
        result["detail"] = address[positions[end - 1] + 1:].lstrip(_SEPARATORS)
        if len(candidates) > 1:
            for part in candidates[0]:
                if all(part in path for path in candidates):
                    result[_FIELDS[part.level - 1]] = part.name
            result.update(status="ambiguous",
                          candidate_codes=tuple(sorted(path[-1].code for path in candidates)))
            break

        path = candidates[0]
        if path[-1].level <= 2 and any(compact.startswith(name, end) for name in upper
                                        if name not in {part.name for part in path}):
            result["status"] = "conflict"
            break
        for part in path:
            result[_FIELDS[part.level - 1]] = part.name
        detail = _without_repeated_levels(result["detail"], path)
        result.update(adcode=path[-1].code, status="matched", detail=detail)
        historical = _HISTORICAL_DISTRICTS.get(path[-1].name)
        if historical and detail.startswith(historical[0]):
            district, code = historical
            result.update(district=district, adcode=code, status="historical",
                          detail=detail[len(district):].lstrip(_SEPARATORS))
        break

    return result


def parse_address_excel(value: str) -> dict[str, object]:
    """Return scalar values suitable for an Excel row."""
    result = parse_address(value)
    result["candidate_codes"] = "、".join(result["candidate_codes"])
    return result
