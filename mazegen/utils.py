grid = list[list[int]]
point = tuple[int, int]
FG_COLORS: list[str] = [
    "\033[37m", "\033[31m", "\033[32m",
    "\033[33m", "\033[34m", "\033[35m",
    "\033[36m"
]
BG_COLORS: list[str] = [
    "\033[41m", "\033[42m", "\033[43m",
    "\033[44m", "\033[45m", "\033[46m",
    "\033[47m", "\033[100m", "\033[101m",
    "\033[102m", "\033[103m", "\033[104m",
    "\033[105m", "\033[106m", "\033[107m",
]


class Directions:
    N: int = 1
    E: int = 2
    S: int = 4
    W: int = 8
    DX: dict[int, int] = {N: 0, S: 0, E: 1, W: -1}
    DY: dict[int, int] = {N: -1, S: 1, E: 0, W: 0}
    OPPOSITE: dict[int, int] = {N: S, S: N, E: W, W: E}
