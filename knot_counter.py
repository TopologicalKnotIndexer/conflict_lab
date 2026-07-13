"""Count prime-knot registry entries by minimal crossing number."""

from reader import get_prime_knot_set


def get_dict_by_crossing() -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    for knot_name in get_prime_knot_set():
        base_name = knot_name
        while base_name[0] in {"k", "K", "m", "M"}:
            base_name = base_name[1:]
        crossing_number = int(base_name.split("n")[0].split("a")[0])
        result.setdefault(crossing_number, []).append(knot_name)
    return result


if __name__ == "__main__":
    by_crossing = get_dict_by_crossing()
    for number in range(3, 12):
        print(
            "minimal crossing number: %2d => %3d knot(s)"
            % (number, len(by_crossing[number]))
        )
