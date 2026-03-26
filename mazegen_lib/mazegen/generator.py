from mazegen.algorithms import Algorithm, DFS, HAK, DFS_NOT_PERFECT
from mazegen.utils import grid, point, Directions, FG_COLORS, BG_COLORS
from typing import Optional, Literal
import random


class DrawError(Exception):
    """Error drawing
    """
    pass


class MazeGenerator():
    def __init__(self, width: int, height: int,
                 entry: point, exit: point,
                 seed: Optional[int] = None) -> None:
        """Initialize a MazeGenerator

        This class takes all settings of the maze and validates them
        to create the base grid.
        At instantiation it create a grid, but if you want to
        use the same instance to re-generate a maze, you should
        use the `create_grid()` method to clear the old grid

        Example:
        ```
        from mazegen import MazeGenerator, Algorithm

        # instantiate the maze generator
        maze = MazeGenerator(10, 10, (0, 0), (9, 9))

        # this will set a special flag in the grid
        # for the 42 cells at the middle
        maze.draw_42()

        # generate the maze using an algorithm of mazegen.algorithms
        # it will fill the grid
        maze.generate(Algorithm.DFS)

        # it returns the path in order from the entry to the exit cell
        # mandatory if you want to print the path in the visualization
        maze.solver()

        # visualize the maze (boolean for the visibility of the path)
        print(maze.visualize(True))
        ```

        Args:
            width (int): Width of the maze
            height (int): Height of the maze
            entry (tuple[int, int]): Coordinates of the entry point
            exit (tuple[int, int]): Coordinates of the exit point
            seed (Optional[int]): seed to use for the generation

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
        self.__path_step: int = 0
        self.create_grid()

    def create_grid(self) -> None:
        """Initialize the grid with walls everywhere
        must be used before re-generating a maze to prevent
        undefined behavior of algorithms
        """
        self.__grid = [[0xF for _ in range(self.__width)]
                       for _ in range(self.__height)]

    def __draw_line(self, x: int, y: int, x2: int, y2: int) -> tuple[int, int]:
        for ny in range(y2 - y + 1):
            for nx in range(x2 - x + 1):
                if x + nx == self.__entry[0] and y + ny == self.__entry[1]\
                   or x + nx == self.__exit[0] and y + ny == self.__exit[1]:
                    raise DrawError(f"can't draw on ({x + nx}, {y + ny}),"
                                    " it's an entry/exit point")
                self.__grid[y + ny][x + nx] = -1
        return x2, y2

    def draw_42(self) -> None:
        """Draw 42 at the center of the grid
        it puts -1 flag in the 42 cells.
        Inner use of draw_line may raise a DrawError
        """
        x_pos: int = int(self.__width / 2) - \
            (3 if self.__width % 2 else 4)
        y_pos: int = int(self.__height / 2) - \
            (2 if self.__height % 2 else 3)
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos, y_pos + 2)
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos + 2, y_pos)
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos, y_pos + 2)
        y_pos -= 4
        x_pos += 2
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos + 2, y_pos)
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos, y_pos + 2)
        x_pos -= 2
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos, y_pos + 2)
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos + 2, y_pos)
        x_pos -= 2
        y_pos -= 2
        x_pos, y_pos = self.__draw_line(x_pos, y_pos, x_pos + 2, y_pos)

    def get_seed(self) -> int:
        """Get the seed of the last generation

        Returns:
            int: the seed
        """
        return self.__seed

    def get_algorithm(self) -> str:
        """Get the algorithm used for the last generation

        Returns:
            str: algorithm key
        """
        return self.__algorithm

    def generate(self, algorithm: Algorithm, seed: Optional[int]
                 = None) -> grid:
        """Generate the grid with the given algorithm
        and the seed of the instance.

        Args:
            algorithm (Algorithm): The algorithm chosen

        Raises:
            ValueError: if algorithm key is not supported

        Returns:
            grid: the grid filled with flags for the walls
        """
        if seed is not None:
            self.__seed = seed
        else:
            if self.__next_seed is not None:
                self.__seed = self.__next_seed
            self.__next_seed = random.randint(1000000, 2700000000)
        random.seed(self.__seed)
        self.__path_step = 0
        match algorithm:
            case Algorithm.DFS:
                self.__grid = DFS(self.__grid).generate()
            case Algorithm.HAK:
                self.__grid = HAK(self.__grid).generate()
            case Algorithm.DFS_NOT_PERFECT:
                self.__grid = DFS_NOT_PERFECT(self.__grid).generate()
            case _:
                raise ValueError("Algorithm is not supported")
        self.__algorithm = algorithm.value
        return self.__grid

    def __is_closed(self, x: int, y: int) -> tuple[bool, bool, bool]:
        is_south_closed: bool = self.__grid[y][x] & Directions.S != 0
        is_east_closed: bool = self.__grid[y][x] & Directions.E != 0
        if self.__grid[y][x] == -1:
            is_south_closed = True
            is_east_closed = True
        return is_south_closed, is_east_closed, self.__grid[y][x] == -1

    def __draw_entry_exit(self, current_point: point) -> str:
        if self.__entry == current_point:
            return "\033[46m"
        if self.__exit == current_point:
            return "\033[103m"
        return ""

    def __solver_get_neighbours(self, x: int, y: int) -> list[point]:
        neighbours: list[point] = []

        # cell above
        if not self.__grid[y][x] & Directions.N and y - 1 >= 0:
            neighbours.append((x, y - 1))

        # cell below
        if not self.__grid[y][x] & Directions.S and y + 1 < self.__height:
            neighbours.append((x, y + 1))

        # cell on the left
        if not self.__grid[y][x] & Directions.W and x - 1 >= 0:
            neighbours.append((x - 1, y))

        # cell on the right
        if not self.__grid[y][x] & Directions.E and x + 1 < self.__width:
            neighbours.append((x + 1, y))
        return neighbours

    def __solver_step(self, m: grid, step: int) -> grid:
        for y in range(self.__height):
            for x in range(self.__width):
                if m[y][x] == step:
                    neighbours = self.__solver_get_neighbours(x, y)
                    # for each neighbour, we set the number of step needed
                    for neighbour in neighbours:
                        neighbour_x, neighbour_y = neighbour
                        # if cell hasn't already been visited
                        if m[neighbour_y][neighbour_x] == 0:
                            m[neighbour_y][neighbour_x] = step + 1
        return m

    def solver(self) -> None:
        """This method will fill the path attribute of the instance
        with the list in order from the entry to the exit of the
        shortest path (in number of cell)
        """
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
            m = self.__solver_step(m, step)
            step += 1
        # here, we have a path to exit in m
        # so now we start from exit and we go in each cell
        # that is the number of step needed to get in exit
        # minus 1
        path: list[point] = [self.__exit]
        path_x, path_y = self.__exit
        while step > 1:
            neighbours = self.__solver_get_neighbours(path_x, path_y)
            for neighbour in neighbours:
                neighbour_x, neighbour_y = neighbour
                # if cell is reachable by a number of step - 1
                if m[neighbour_y][neighbour_x] == step - 1:
                    path.append((neighbour_x, neighbour_y))
                    path_x, path_y = neighbour
                    break
            step -= 1
        self.__path = path[::-1]

    def __is_cell_path(self, p: point) -> bool:
        return (p in self.__path
                and p != self.__entry
                and p != self.__exit)

    def rotate_color(self, type: Literal["PATH", "42", "WALL"]) -> None:
        """Rotate color attribute used in the visualization

        Args:
            type (Literal["PATH", "42", "WALL"]): the type of color to change

        Raises:
            ValueError: if type is not "PATH", "42" or "WALL"
        """
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
        else:
            raise ValueError(f"type '{type}' for rotatation of colors"
                             " is not supported")

    def __conv_path_to_dir(self) -> str:
        path_str: str = ""
        for i, cell in enumerate(self.__path):
            if i == 0:
                continue
            previous: point = self.__path[i - 1]
            direction: point = (cell[0] - previous[0], cell[1] - previous[1])
            if direction == (1, 0):
                path_str += "E"
            if direction == (-1, 0):
                path_str += "W"
            if direction == (0, -1):
                path_str += "N"
            if direction == (0, 1):
                path_str += "S"
        return path_str

    def output(self) -> str:
        """Generate the output string:
        each character represents a cell
        0 means full opened and F wall on each side
        each row represents a row of the maze
        atfer the blank line, you have
        the entry point, then
        the exit point and then
        the path with direction to follow to join the exit

        Returns:
            str: the output string
        """
        output: str = ""
        for row in self.__grid:
            for cell in row:
                if cell == -1:
                    output += "F"
                else:
                    output += f"{cell:X}"
            output += "\n"
        output += "\n{0},{1}".format(*self.__entry)
        output += "\n{0},{1}\n".format(*self.__exit)
        output += f"{self.__conv_path_to_dir()}\n"
        return output

    def get_path_length(self) -> int:
        return len(self.__path)

    def reset_path_steps(self) -> None:
        self.__path_step = 0

    def visualize(self, display_path: bool,
                  animate: Optional[bool] = False) -> str:
        """Generate the string of the visualization of the maze
        it also display the path from entry to exit if the argument is True

        Args:
            display_path (bool): display the shortest path
            animate(Optional[bool]): display with animation or not

        Returns:
            str: the visualization
        """
        if display_path and self.__path_step == 0:
            self.__path_step = 1
        elif display_path:
            self.__path_step += 1
        visualization: str = ""
        visualization += \
            self.__wall_color + "▄▄▄▄" * (self.__width) + "▄\033[0m"
        limited_path: list[point] = self.__path[:self.__path_step]
        for y in range(self.__height):
            visualization += f"\n{self.__wall_color}█\033[0m"
            is_south_closed: bool
            is_east_closed: bool
            is_42: bool
            for is_top in [True, False]:
                if not is_top:
                    visualization += f"\n{self.__wall_color}█\033[0m"
                for x in range(self.__width):
                    visualization += self.__draw_entry_exit((x, y))
                    is_south_closed, is_east_closed, is_42 = \
                        self.__is_closed(x, y)
                    path: bool = self.__is_cell_path((x, y)) and display_path
                    if path and ((x, y) in limited_path or not animate):
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
                    if path and ((x, y) in limited_path or not animate):
                        visualization += self.__path_color
                    visualization += "█" if is_east_closed \
                        else (" " if is_top else "▄")
                    visualization += "\033[0m"
        return visualization
