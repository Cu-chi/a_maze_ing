from mazegen.algorithms import Algorithm, DFS, HAK
from mazegen.utils import grid, point, Directions, FG_COLORS, BG_COLORS
from typing import Optional
import random


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 entry: point, exit: point,
                 seed: Optional[int] = None) -> None:
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
            ValueError: if entry and exit point are the same
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

        if entry == exit:
            raise ValueError("entry and exit must be different.")

        self.__width: int = width
        self.__height: int = height
        self.__entry: point = entry
        self.__exit: point = exit

        if seed is None:
            seed = random.randint(1000000, 2700000000)
        self.__seed: int = seed
        self.__next_seed: int | None = None

        self.__grid: grid
        self.__path: list[point] = []
        self.__wall_color: str = "\033[97m"
        self.__42_color: str = "\033[107m"
        self.__path_color: str = "\033[106m"
        self.__algorithm: str = ""
        self.create_grid()

    def create_grid(self) -> None:
        self.__grid = [[0 for _ in range(self.__width)]
                       for _ in range(self.__height)]

    def draw_line(self, x: int, y: int, x2: int, y2: int) -> tuple[int, int]:
        for ny in range(y2 - y + 1):
            for nx in range(x2 - x + 1):
                self.__grid[y + ny][x + nx] = -1
        return x2, y2

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

    def get_seed(self) -> int:
        return self.__seed

    def get_algorithm(self) -> str:
        return self.__algorithm

    def generate(self, algorithm: Algorithm) -> grid:
        if self.__next_seed is not None:
            self.__seed = self.__next_seed
        self.__next_seed = random.randint(1000000, 2700000000)
        random.seed(self.__seed)
        match algorithm:
            case Algorithm.DFS:
                self.__grid = DFS(self.__grid).generate()
            case Algorithm.HAK:
                self.__grid = HAK(self.__grid).generate()
            case _:
                raise ValueError("Algorithm is not supported")
        self.__algorithm = algorithm.value
        return self.__grid

    def is_closed(self, x: int, y: int) -> tuple[bool, bool, bool]:
        E, S = 2, 4
        is_south_closed: bool = self.__grid[y][x] & S == 0
        is_east_closed: bool = self.__grid[y][x] & E == 0
        if self.__grid[y][x] == -1:
            is_south_closed = True
            is_east_closed = True
        return is_south_closed, is_east_closed, self.__grid[y][x] == -1

    def draw_entry_exit(self, current_point: point) -> str:
        if self.__entry == current_point:
            return "\033[46m"
        if self.__exit == current_point:
            return "\033[103m"
        return ""

    def solver_get_neighbours(self, x: int, y: int) -> list[point]:
        neighbours: list[point] = []

        # cell above
        if self.__grid[y][x] & Directions.N and y - 1 >= 0:
            neighbours.append((x, y - 1))

        # cell below
        if self.__grid[y][x] & Directions.S and y + 1 < self.__height:
            neighbours.append((x, y + 1))

        # cell on the left
        if self.__grid[y][x] & Directions.W and x - 1 >= 0:
            neighbours.append((x - 1, y))

        # cell on the right
        if self.__grid[y][x] & Directions.E and x + 1 < self.__width:
            neighbours.append((x + 1, y))
        return neighbours

    def solver_step(self, m: grid, step: int) -> grid:
        for y in range(self.__height):
            for x in range(self.__width):
                if m[y][x] == step:
                    neighbours = self.solver_get_neighbours(x, y)
                    # for each neighbour, we set the number of step needed
                    for neighbour in neighbours:
                        neighbour_x, neighbour_y = neighbour
                        # if cell hasn't already been visited
                        if m[neighbour_y][neighbour_x] == 0:
                            m[neighbour_y][neighbour_x] = step + 1
        return m

    def solver(self) -> None:
        # here we init a matrix with all cell at 0
        # entry cell is 1 because it's the first step
        m: grid = []
        for y in range(self.__height):
            m.append([])
            for _ in range(self.__width):
                m[y].append(0)
        exit_x, exit_y = self.__exit
        entry_x, entry_y = self.__entry
        m[entry_y][entry_x] = 1
        step: int = 1
        while m[exit_y][exit_x] == 0:
            m = self.solver_step(m, step)
            step += 1
        # here, we have a path to exit in m
        # so now we start from exit and we go in each cell
        # that is the number of step needed to get in exit
        # minus 1
        path: list[point] = [self.__exit]
        path_x, path_y = self.__exit
        while step > 1:
            neighbours = self.solver_get_neighbours(path_x, path_y)
            for neighbour in neighbours:
                neighbour_x, neighbour_y = neighbour
                # if cell is reachable by a number of step - 1
                if m[neighbour_y][neighbour_x] == step - 1:
                    path.append((neighbour_x, neighbour_y))
                    path_x, path_y = neighbour
                    break
            step -= 1
        self.__path = path[::-1]

    def solve_bfs(self) -> None:
        queue: list[point] = [self.__entry]
        visited: set[point] = {self.__entry}
        parents: dict[point, point | None] = {self.__entry: None}
        moves: list[tuple[int, int, int]] = [
            (0, -1, Directions.N), (1, 0, Directions.E),
            (0, 1, Directions.S), (-1, 0, Directions.W)
        ]
        current: point = self.__entry
        while queue:
            current = queue.pop(0)
            if current == self.__exit:
                break
            cx, cy = current
            for dx, dy, bit in moves:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.__width and 0 <= ny < self.__height:
                    if self.__grid[cy][cx] != -1 and (self.__grid[cy][cx]
                                                      & bit):
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            parents[(nx, ny)] = current
                            queue.append((nx, ny))
        path: list[point] = []
        if current != self.__exit:
            return
        new_current: point | None = self.__exit
        while new_current is not None:
            path.append(new_current)
            new_current = parents[new_current]
        self.__path = path[::-1]

    def is_cell_path(self, p: point) -> bool:
        return (p in self.__path
                and p != self.__entry
                and p != self.__exit)

    def rotate_color(self, type: str) -> None:
        current: str
        if type == "PATH":
            current = self.__path_color
            while self.__path_color == current:
                self.__path_color = BG_COLORS[
                    random.randrange(0, len(BG_COLORS))]
        elif type == "42":
            current = self.__42_color
            while self.__42_color == current:
                self.__42_color = BG_COLORS[
                    random.randrange(0, len(BG_COLORS))]
        elif type == "WALL":
            current = self.__wall_color
            while self.__wall_color == current:
                self.__wall_color = FG_COLORS[
                    random.randrange(0, len(FG_COLORS))]

    def visualize(self, display_path: bool) -> str:
        visualization: str = ""
        visualization += \
            self.__wall_color + "▄▄▄▄" * (self.__width) + "▄\033[0m"
        for y in range(self.__height):
            visualization += f"\n{self.__wall_color}█\033[0m"
            is_south_closed: bool
            is_east_closed: bool
            is_42: bool
            for is_top in [True, False]:
                if not is_top:
                    visualization += f"\n{self.__wall_color}█\033[0m"
                for x in range(self.__width):
                    visualization += self.draw_entry_exit((x, y))
                    is_south_closed, is_east_closed, is_42 = self.is_closed(x,
                                                                            y)
                    path: bool = self.is_cell_path((x, y)) and display_path
                    if path:
                        visualization += self.__path_color
                    if is_top:
                        if is_42:
                            visualization += self.__42_color
                        visualization += "   "
                    else:
                        visualization += self.__wall_color
                        if is_42:
                            visualization += self.__42_color
                        visualization += "▄▄▄" \
                            if is_south_closed else "   "
                    visualization += "\033[0m"
                    visualization += self.__wall_color
                    if path:
                        visualization += self.__path_color
                    visualization += "█" if is_east_closed \
                        else (" " if is_top else "▄")
                    visualization += "\033[0m"
        return visualization
