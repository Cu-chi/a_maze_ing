from io import TextIOWrapper
from mazegen.utils import point


def parsed_info(file: TextIOWrapper) -> dict[str, str]:
    config: dict[str, str] = {}
    for line in file:
        data: list[str] = line.split("=")
        key: str = data[0].strip(" ")
        value: str = data[1].strip("\n").strip("\"")
        config.update({key: value})
    return config


def get_int(data: dict[str, str], key: str) -> int:
    if key not in data:
        raise KeyError(f"missing key : {key}")
    try:
        return int(data[key])
    except ValueError:
        raise ValueError(f"{key.lower()} has to be an integers!")


def get_point(data: dict[str, str], key: str) -> point:
    if key not in data:
        raise KeyError(f"missing key : {key}")
    try:
        parts: list[str] = data[key].split(",")
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        raise ValueError(f"{key.lower()} has to be a tuple of two "
                         "integers (x,y).")
