"""Parse Chinese administrative addresses using the official division snapshot."""

from collections import defaultdict
from functools import lru_cache

from chinese_address_generator import get_data_metadata, load_divisions

__all__ = ["parse_address", "parse_address_excel"]

_FIELDS = ("province", "city", "district", "township")


@lru_cache(maxsize=1)
def _address_index():
    divisions = {division.code: division for division in load_divisions()}
    names = defaultdict(list)
    for division in divisions.values():
        path = []
        current = division
        while current is not None:
            path.append(current)
            current = divisions.get(current.parent_code)
        path = tuple(reversed(path))
        for start in range(len(path)):
            name = "".join(part.name for part in path[start:])
            names[name].append(path)
    return names, max(map(len, names)), get_data_metadata()["data_as_of"]


def parse_address(value: str) -> dict[str, object]:
    """Parse an administrative prefix and preserve the remaining address text.

    Accepts official names, starting at any level. A name shared by multiple
    divisions produces candidate codes unless the preceding names disambiguate it.
    """
    if not isinstance(value, str):
        raise TypeError("address must be a string")

    address = value.strip()
    names, longest, data_version = _address_index()
    result = dict.fromkeys((*_FIELDS, "adcode"))
    result.update(detail=address, status="unmatched", candidate_codes=(), data_version=data_version)

    for end in range(min(longest, len(address)), 0, -1):
        paths = names.get(address[:end])
        if paths is None:
            continue

        result["detail"] = address[end:].lstrip()
        for part in paths[0]:
            if all(part in path for path in paths):
                result[_FIELDS[part.level - 1]] = part.name
        if len(paths) == 1:
            result.update(adcode=paths[0][-1].code, status="matched")
        else:
            codes = tuple(sorted(path[-1].code for path in paths))
            result.update(status="ambiguous", candidate_codes=codes)
        break

    return result


def parse_address_excel(value: str) -> dict[str, object]:
    """Return scalar values suitable for an Excel row."""
    result = parse_address(value)
    result["candidate_codes"] = "、".join(result["candidate_codes"])
    return result
