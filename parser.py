from io import TextIOWrapper


def parsed_info(file: TextIOWrapper) -> dict[str, str]:
    config: dict[str, str] = {}
    for line in file:
        data: list[str] = line.split("=")
        key: str = data[0].strip(" ")
        value: str = data[1].strip("\n").strip("\"")
        config.update({key: value})
    return config
