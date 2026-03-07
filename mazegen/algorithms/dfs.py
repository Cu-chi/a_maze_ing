from mazegen.algorithms.base import BaseAlgorithm
from mazegen.utils import grid
import random


class DFS(BaseAlgorithm):
    def dfs(self, cx: int, cy: int) -> None:
        directions: list[int] = [self.N, self.S, self.E, self.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + self.DX[dir]
            ny: int = cy + self.DY[dir]

            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and self.grid[ny][nx] == 0:
                self.grid[cy][cx] = self.grid[cy][cx] | dir
                self.grid[ny][nx] = self.grid[ny][nx] | self.OPPOSITE[dir]
                self.dfs(nx, ny)

    def generate(self) -> grid:
        self.dfs(0, 0)
        return self.grid
