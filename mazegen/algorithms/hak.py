from mazegen.algorithms.base import BaseAlgorithm
from mazegen.utils import grid
from typing import Optional
import random


class HAK(BaseAlgorithm):
    def __init__(self, grid_: grid) -> None:
        super().__init__(grid_)
        self.h: int = len(self.grid)
        self.w: int = len(self.grid[0])
        self.visited: bool = [[False for _ in range(self.w)]
                              for _ in range(self.h)]

    def walk(self, cy: int, cx: int) -> tuple[int, int] | None:
        self.visited[cy][cx] = True
        directions: list[int] = [self.N, self.S, self.E, self.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + self.DX[dir]
            ny: int = cy + self.DY[dir]
            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and not self.visited[ny][nx] and self.grid[ny][nx] != -1:
                self.grid[cy][cx] |= dir
                self.grid[ny][nx] |= self.OPPOSITE[dir]
                return (ny, nx)
        return None

    def hunt(self) -> Optional[tuple[int, int]]:
        for cy in range(self.h):
            for cx in range(self.w):
                if not self.visited[cy][cx] and self.grid[cy][cx] != -1:
                    for direction in [self.N, self.S, self.E, self.W]:
                        nx: int = cx + self.DX[direction]
                        ny: int = cy + self.DY[direction]
                        if (0 <= ny < len(self.grid)) and \
                            (0 <= nx < len(self.grid[ny])) \
                                and self.visited[ny][nx]:
                            self.grid[cy][cx] |= direction
                            self.grid[ny][nx] |= self.OPPOSITE[direction]
                            self.visited[cy][cx] = True
                            return (cy, cx)
        return None

    def generate(self) -> grid:
        current: tuple = (0, 0)
        while current:
            while current:
                next: grid[list[int]] | None = self.walk(*current)
                if not next:
                    break
                current = next
            current = self.hunt()
        return self.grid
