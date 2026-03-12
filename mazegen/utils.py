grid = list[list[int]]
point = tuple[int, int]


class Directions:
    N: int = 1
    E: int = 2
    S: int = 4
    W: int = 8
    DX: dict[int, int] = {N: 0, S: 0, E: 1, W: -1}
    DY: dict[int, int] = {N: -1, S: 1, E: 0, W: 0}
    OPPOSITE: dict[int, int] = {N: S, S: N, E: W, W: E}
