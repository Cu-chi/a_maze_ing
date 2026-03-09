from mazegen.algorithms import Algorithm, DFS
from mazegen.utils import grid, point


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 entry: point, exit: point) -> None:
        """Initialize a MazeGenerator

        This class takes all settings of the maze and validates them
        to create the base grid.

        Args:
            width (int): Width of the maze
            height (int): Height of the maze
            entry (tuple[int, int]): Coordinates of the entry point
            exit (tuple[int, int]): Coordinates of the exit point

        Raises:
            ValueError: if width is lower than 2
            ValueError: if height is lower than 2
            ValueError: if entry point is not in the maze
            ValueError: if exit point is not in the maze
        """
        if width < 10:
            raise ValueError("width attribute must be greater"
                             " or equal than 10")
        if height < 10:
            raise ValueError("height attribute must be greater"
                             " or equal than 10")

        if entry[0] < 0 or entry[0] >= width \
           or entry[1] < 0 or entry[1] >= height:
            raise ValueError("entry coordinates are not valid. Must be between"
                             f" (0, 0)-({width-1}, {height-1}), is {entry}")

        if exit[0] < 0 or exit[0] >= width \
           or exit[1] < 0 or exit[1] >= height:
            raise ValueError("exit coordinates are not valid. Must be between"
                             f" (0, 0)-({width-1}, {height-1}), is {exit}")

        self.__width: int = width
        self.__height: int = height
        self.__entry: point = entry
        self.__exit: point = exit
        self.__grid: grid = []

        for i in range(height):
            self.__grid.append([])
            for _ in range(width):
                self.__grid[i].append(0)

    def draw_line(self, x: int, y: int, x2: int, y2: int) -> tuple[int, int]:
        for ny in range(y2 - y + 1):
            for nx in range(x2 - x + 1):
                self.__grid[y + ny][x + nx] = -1
        return x2, y2

    def debug(self) -> None:
        for y in range(self.__height):
            for x in range(self.__width):
                self.__grid[y][x] = 15

    def draw_42(self) -> None:
        x_placement: int = int(self.__width / 2) - \
            (3 if self.__width % 2 else 4)
        y_placement: int = int(self.__height / 2) - \
            (2 if self.__height % 2 else 3)
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement, y_placement + 2)
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement + 2, y_placement)
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement, y_placement + 2)
        y_placement -= 4
        x_placement += 2
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement + 2, y_placement)
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement, y_placement + 2)
        x_placement -= 2
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement, y_placement + 2)
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement + 2, y_placement)
        x_placement -= 2
        y_placement -= 2
        x_placement, y_placement = self.draw_line(x_placement, y_placement,
                                                  x_placement + 2, y_placement)

    def generate(self, algorithm: Algorithm) -> grid:
        match algorithm:
            case Algorithm.DFS:
                self.__grid = DFS(self.__grid).generate()
            case Algorithm.HAK:
                return []
            case _:
                raise ValueError("Algorithm is not supported")
        return self.__grid

    def is_closed(self, x: int, y: int) -> tuple[bool, bool, bool]:
        E, S = 2, 4
        is_south_closed: bool = self.__grid[y][x] & S == 0
        is_east_closed: bool = self.__grid[y][x] & E == 0
        if self.__grid[y][x] == -1:
            is_south_closed = True
            is_east_closed = True
        return is_south_closed, is_east_closed, self.__grid[y][x] == -1

    def visualize(self) -> str:
        visualization: str = ""
        visualization += "▄▄▄▄" * (self.__width) + "▄"
        for y in range(self.__height):
            visualization += "\n█"
            is_south_closed: bool
            is_east_closed: bool
            is_42: bool
            for x in range(self.__width):
                is_south_closed, is_east_closed, is_42 = self.is_closed(x, y)
                visualization += "   " if not is_42 else "███"
                visualization += "█" if is_east_closed else " "
            visualization += "\n█"
            for x in range(self.__width):
                is_south_closed, is_east_closed, is_42 = self.is_closed(x, y)
                visualization += "▄▄▄" if is_south_closed and not is_42 else \
                    ("   " if not is_42 else "███")
                visualization += "█" if is_east_closed else "▄"
        return visualization
