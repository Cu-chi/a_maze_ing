from mazegen.algorithms.base import BaseAlgorithm
from mazegen.utils import grid, Directions as Dir
import random


class DFS(BaseAlgorithm):
    def dfs(self, cx: int, cy: int) -> None:
        directions: list[int] = [Dir.N, Dir.S,
                                 Dir.E, Dir.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + Dir.DX[dir]
            ny: int = cy + Dir.DY[dir]

            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and self.grid[ny][nx] == 0:
                self.grid[cy][cx] = self.grid[cy][cx] | dir
                self.grid[ny][nx] = self.grid[ny][nx] | Dir.OPPOSITE[dir]
                self.dfs(nx, ny)

    def generate(self) -> grid:
        """Fill the grid using the DFS algorithm

        Returns:
            grid: the grid of the maze
        """
        self.dfs(0, 0)
        return self.grid
