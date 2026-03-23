from io import TextIOWrapper
from mazegen.utils import point


class ConfigError(Exception):
    pass

def parsed_info(file: TextIOWrapper) -> dict[str, str]:
    config: dict[str, str] = {}
    for line in file:
        data: list[str] = line.split("=")
        if line == "\n":
            raise ConfigError("blank line in config.txt")
        if len(data) < 2:
            raise ConfigError("the line doesn't respect key=value")
        key: str = data[0].strip(" ")
        value: str = data[1].strip("\n").strip("\"")
        if len(value) < 1:
            raise ConfigError("the line doesn't respect key=value")
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


def get_bool(data: dict[str, str], key: str) -> bool:
    value: str | None = data.get(key)
    clean_value: str = value.strip().lower()
    if key not in data:
        raise KeyError(f"missing key : {key}")

    if clean_value == "true":
        return True
    if clean_value == "false":
        return False
    raise ValueError(f"{key.lower()} has to be a boolean (True or False).")