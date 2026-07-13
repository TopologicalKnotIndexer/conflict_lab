"""Reproduce collision statistics for the three committed invariant registries."""

from functools import cache
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_DIR = ROOT / "json"
EXPECTED_RECORDS = 1783
EPS = 1e-4


def load_database(filepath: str | Path, name_on_left: bool) -> dict[str, str]:
    """Load `[left|right]` records and return a knot-name keyed mapping."""

    path = Path(filepath)
    if not path.is_absolute():
        path = ROOT / path
    info: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line:
            continue
        if not line.startswith("[") or not line.endswith("]") or "|" not in line:
            raise ValueError(f"malformed record at {path}:{line_number}")
        left, right = line[1:-1].split("|", 1)
        name, value = (left, right) if name_on_left else (right, left)
        if not name or name in info:
            raise ValueError(f"missing or duplicate knot name at {path}:{line_number}")
        info[name] = value
    return info


@cache
def get_combined_data() -> dict[str, dict[str, str]]:
    """Join registries after proving that their knot-name sets are identical."""

    hom = load_database("HOMFLY-PT-reg.txt", False)
    kho = load_database("khovanov-reg.txt", False)
    vol = load_database("volume_info_list-reg.txt", True)
    if set(hom) != set(kho) or set(hom) != set(vol):
        raise ValueError("invariant registries contain different knot-name sets")
    if len(hom) != EXPECTED_RECORDS:
        raise ValueError(f"expected {EXPECTED_RECORDS} knots, found {len(hom)}")
    return {
        knot_name: {"hom": hom[knot_name], "kho": kho[knot_name], "vol": vol[knot_name]}
        for knot_name in hom
    }


def get_cnt_stat(
    raw_value_to_names: dict[str, list[str]], dump_file_name: str
) -> dict[int, int]:
    """Write collision groups and return a class-size histogram."""

    groups: list[list[str]] = []
    count_by_size: dict[int, int] = {}
    for names in raw_value_to_names.values():
        size = len(names)
        count_by_size[size] = count_by_size.get(size, 0) + 1
        groups.append(names)
    groups.sort(key=len)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    with (JSON_DIR / dump_file_name).open("w", encoding="utf-8") as stream:
        json.dump(groups, stream, indent=4)
    return count_by_size


def _group_by(fields: tuple[str, ...]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for knot_name, record in get_combined_data().items():
        key = "[" + "@".join(record[field] for field in fields) + "]"
        grouped.setdefault(key, []).append(knot_name)
    return grouped


def get_kho_stat():
    grouped = _group_by(("kho",))
    stats = get_cnt_stat(grouped, "get_kho_stat.json")
    print("get_kho_stat", len(grouped), stats)
    return len(grouped), stats


def get_hom_stat():
    grouped = _group_by(("hom",))
    stats = get_cnt_stat(grouped, "get_hom_stat.json")
    print("get_hom_stat", len(grouped), stats)
    return len(grouped), stats


def get_kho_hom_stat():
    grouped = _group_by(("hom", "kho"))
    stats = get_cnt_stat(grouped, "get_kho_hom_stat.json")
    print("get_kho_hom_stat", len(grouped), stats)
    return len(grouped), stats


def _group_with_rounded_volume(knot_names: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    data = get_combined_data()
    for knot_name in knot_names:
        record = data[knot_name]
        key = f"[{record['hom']}|{record['kho']}|{float(record['vol']):.3f}]"
        grouped.setdefault(key, []).append(knot_name)
    return grouped


def get_deprecated_kho_hom_vol_stat():
    grouped = _group_with_rounded_volume(list(get_combined_data()))
    stats = get_cnt_stat(grouped, "get_deprecated_kho_hom_vol_stat.json")
    print("get_deprecated_kho_hom_vol_stat", len(grouped), stats)
    return len(grouped), stats


def get_prime_knot_set() -> list[str]:
    """Return 801 prime-knot names after identifying mirror pairs."""

    return sorted(
        knot_name
        for knot_name in get_combined_data()
        if "," not in knot_name and not knot_name.startswith("m") and knot_name != "K0a1"
    )


def get_non_prime_knot_set() -> list[str]:
    return [name for name in get_combined_data() if "," in name]


def get_vol_stat1():
    primes = get_prime_knot_set()
    data = get_combined_data()
    total_count = 0
    collision_count = 0
    for index, first in enumerate(primes):
        first_volume = float(data[first]["vol"])
        for second in primes[:index]:
            if abs(first_volume - float(data[second]["vol"])) < EPS:
                collision_count += 1
            total_count += 1
    print(
        "get_vol_stat1",
        "total_cnt:",
        total_count,
        " wrong_cnt:",
        collision_count,
    )
    return total_count, collision_count


def get_col_stat2():
    grouped: dict[str, list[str]] = {}
    data = get_combined_data()
    for knot_name in get_prime_knot_set():
        volume = float(data[knot_name]["vol"])
        if volume < 0:
            raise ValueError(f"negative volume for {knot_name}")
        grouped.setdefault(f"{volume:.3f}", []).append(knot_name)
    stats = get_cnt_stat(grouped, "get_col_stat2.json")
    print("get_col_stat2", len(grouped), stats)
    return len(grouped), stats


def get_chiral_prime() -> list[str]:
    data = get_combined_data()
    return [prime for prime in get_prime_knot_set() if "m" + prime in data]


def get_prime_stat():
    primes = get_prime_knot_set()
    chiral_count = len(get_chiral_prime())
    amphichiral_count = len(primes) - chiral_count
    print("get_prime_stat", "chiral:", chiral_count, "amchiral:", amphichiral_count)
    return chiral_count, amphichiral_count


def _get_chiral_collision_stat(field: str):
    data = get_combined_data()
    collisions = [
        prime
        for prime in get_chiral_prime()
        if data[prime][field] == data["m" + prime][field]
    ]
    return len(get_chiral_prime()), collisions


def get_chiral_kho_stat():
    total, collisions = _get_chiral_collision_stat("kho")
    print(
        "get_chiral_kho_stat",
        "total:",
        total,
        "wrong:",
        len(collisions),
        collisions,
    )
    return total, collisions


def get_chiral_hom_stat():
    total, collisions = _get_chiral_collision_stat("hom")
    print(
        "get_chiral_hom_stat",
        "total:",
        total,
        "wrong:",
        len(collisions),
        collisions,
    )
    return total, collisions


def get_chiral_vol_stat():
    data = get_combined_data()
    chiral = get_chiral_prime()
    collisions = sum(
        abs(float(data[prime]["vol"]) - float(data["m" + prime]["vol"])) < EPS
        for prime in chiral
    )
    print("get_chiral_vol_stat", "total:", len(chiral), "wrong:", collisions)
    return len(chiral), collisions


def get_kho_hom_non_prime_stat():
    names = get_non_prime_knot_set()
    data = get_combined_data()
    grouped: dict[str, list[str]] = {}
    for knot_name in names:
        record = data[knot_name]
        key = f"[{record['hom']}|{record['kho']}]"
        grouped.setdefault(key, []).append(knot_name)
    stats = get_cnt_stat(grouped, "get_kho_hom_non_prime_stat.json")
    print("get_kho_hom_non_prime_stat", len(grouped), stats)
    return len(grouped), stats


def get_deprecated_kho_hom_vol_non_prime_stat():
    grouped = _group_with_rounded_volume(get_non_prime_knot_set())
    stats = get_cnt_stat(grouped, "get_deprecated_kho_hom_vol_non_prime_stat.json")
    print("get_deprecated_kho_hom_vol_non_prime_stat", len(grouped), stats)
    return len(grouped), stats


def main() -> int:
    get_kho_stat()
    get_hom_stat()
    get_kho_hom_stat()
    get_deprecated_kho_hom_vol_stat()
    get_vol_stat1()
    get_col_stat2()
    get_prime_stat()
    get_chiral_kho_stat()
    get_chiral_hom_stat()
    get_chiral_vol_stat()
    get_kho_hom_non_prime_stat()
    get_deprecated_kho_hom_vol_non_prime_stat()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
