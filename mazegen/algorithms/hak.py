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

    def walk(self, cx: int, cy: int) -> grid[int] | None:
        self.visited[cx][cy] = True
        directions: list[int] = [self.N, self.S, self.E, self.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + self.DX[dir]
            ny: int = cy + self.DY[dir]
            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and not self.visited[nx][ny]:
                self.grid[cx][cy] |= dir
                self.grid[nx][ny] |= self.OPPOSITE[dir]
                return [nx, ny]

    def hunt(self) -> Optional[tuple[int, int]]:
        for cy in range(self.h):
            for cx in range(self.w):
                if not self.visited[cy][cx]:
                    for direction in [self.N, self.S, self.E, self.W]:
                        nx: int = cx + self.DX[direction]
                        ny: int = cy + self.DY[direction]
                        if (0 <= ny < len(self.grid)) and \
                            (0 <= nx < len(self.grid[ny])) \
                                and self.visited[nx][ny]:
                            self.grid[cx][cy] |= dir
                            self.grid[nx][ny] |= self.OPPOSITE[dir]
                            self.visited[cx][cy] = True
                            return (cx, cy)
            return None

    def generate(self) -> grid:
        current_cords = (0, 0)
        while current_cords:
            cx, cy = current_cords
            self.walk(cx, cy)
            current_cords = self.hunt()
        return (self.grid)
