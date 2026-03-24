grid = list[list[int]]
"type used to represent the grid"

point = tuple[int, int]
"type used to represent a point, a cell"

FG_COLORS: list[str] = [
    "\033[37m", "\033[31m", "\033[32m",
    "\033[33m", "\033[34m", "\033[35m",
    "\033[36m"
]
"Foreground colors used in the terminal"

BG_COLORS: list[str] = [
    "\033[41m", "\033[42m", "\033[43m",
    "\033[44m", "\033[45m", "\033[46m",
    "\033[47m", "\033[100m", "\033[101m",
    "\033[102m", "\033[103m", "\033[104m",
    "\033[105m", "\033[106m", "\033[107m",
]
"Background colors used in the terminal"


class Directions:
    """Useful class to use when working on the grid
    and on bits
    """
    N: int = 1
    "N is 1 because the N bit is stored in the first bit (LSB)"
    E: int = 2
    "E is 2 because the E bit is stored in the second bit (LSB)"
    S: int = 4
    "S is 4 because the S bit is stored in the third bit (LSB)"
    W: int = 8
    "W is 8 because the W bit is stored in the fourth bit (LSB)"

    DX: dict[int, int] = {N: 0, S: 0, E: 1, W: -1}
    """DX stores the moves possible to move on the X axis
    so N and S are useless
    E = 1 because we need to add 1 to move on the East side
    W = -1 because we need to remove 1 to move on the West side
    """
    DY: dict[int, int] = {N: -1, S: 1, E: 0, W: 0}
    """DY stores the moves possible to move on the Y axis
    so E and W are useless
    S = 1 because we need to add 1 to move on the South side
    N = -1 because we need to remove 1 to move on the North side
    """
    OPPOSITE: dict[int, int] = {N: S, S: N, E: W, W: E}
    """OPPOSITE stores the opposite of each direction
    """
