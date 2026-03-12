from mazegen.algorithms.base import BaseAlgorithm
from mazegen.utils import grid, point, Directions as Dir
import random


class HAK(BaseAlgorithm):
    def __init__(self, grid_: grid) -> None:
        super().__init__(grid_)
        self.h: int = len(self.grid)
        self.w: int = len(self.grid[0])
        self.visited: list[list[bool]] = [[False for _ in range(self.w)]
                                          for _ in range(self.h)]

    def walk(self, cy: int, cx: int) -> point | None:
        self.visited[cy][cx] = True
        directions: list[int] = [Dir.N, Dir.S, Dir.E, Dir.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + Dir.DX[dir]
            ny: int = cy + Dir.DY[dir]
            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and not self.visited[ny][nx] and self.grid[ny][nx] != -1:
                self.grid[cy][cx] |= dir
                self.grid[ny][nx] |= Dir.OPPOSITE[dir]
                return (ny, nx)
        return None

    def hunt(self) -> point | None:
        for cy in range(self.h):
            for cx in range(self.w):
                if not self.visited[cy][cx] and self.grid[cy][cx] != -1:
                    for direction in [Dir.N, Dir.S, Dir.E, Dir.W]:
                        nx: int = cx + Dir.DX[direction]
                        ny: int = cy + Dir.DY[direction]
                        if (0 <= ny < len(self.grid)) and \
                            (0 <= nx < len(self.grid[ny])) \
                                and self.visited[ny][nx]:
                            self.grid[cy][cx] |= direction
                            self.grid[ny][nx] |= Dir.OPPOSITE[direction]
                            self.visited[cy][cx] = True
                            return (cy, cx)
        return None

    def generate(self) -> grid:
        """Fill the grid using the HAK algorithm

        Returns:
            grid: the grid of the maze
        """
        current: point | None = (0, 0)
        next: point | None = None
        while current:
            while current:
                next = self.walk(*current)
                if not next:
                    break
                current = next
            current = self.hunt()
        return self.grid
