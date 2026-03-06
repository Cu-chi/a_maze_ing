from mazegen.algorithms.base import Algorithm
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

    def generate(self, algorithm: Algorithm) -> None:
        match algorithm:
            case Algorithm.DFS:
                print("DFS")
            case Algorithm.HAK:
                print("HAK")
            case _:
                raise ValueError("Algorithm is not supported")
