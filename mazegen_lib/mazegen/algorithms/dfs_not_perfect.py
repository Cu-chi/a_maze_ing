from mazegen.algorithms.base import BaseAlgorithm
from mazegen.utils import grid, Directions as Dir, point
import random


class DFS_NOT_PERFECT(BaseAlgorithm):
    def dfs(self, cx: int, cy: int) -> None:
        directions: list[int] = [Dir.N, Dir.S,
                                 Dir.E, Dir.W]
        random.shuffle(directions)
        for dir in directions:
            nx: int = cx + Dir.DX[dir]
            ny: int = cy + Dir.DY[dir]

            if (0 <= ny < len(self.grid)) and (0 <= nx < len(self.grid[ny])) \
               and self.grid[ny][nx] == 0xF:
                self.grid[cy][cx] ^= dir
                self.grid[ny][nx] ^= Dir.OPPOSITE[dir]
                self.dfs(nx, ny)

    @staticmethod
    def check_destruction(x: int, y: int, destroyed: list[point]) -> bool:
        return any(point_ in destroyed for point_ in [
            # next right, next left, up, down, self
            (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y),
            # down right, up left, down left, up right
            (x + 1, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1)
        ])

    def destroy_perfection(self) -> None:
        amount_to_destroy: int = len(self.grid)\
            if len(self.grid) > len(self.grid[0]) else len(self.grid[0])
        directions: list[int] = [Dir.N, Dir.S,
                                 Dir.E, Dir.W]
        destroyed_cells: list[point] = []
        for _ in range(amount_to_destroy):
            destroyed: bool = False
            while not destroyed:
                rx: int = random.randint(0, len(self.grid[0]) - 1)
                ry: int = random.randint(0, len(self.grid) - 1)
                random.shuffle(directions)
                if self.grid[ry][rx] != -1\
                   and not self.check_destruction(rx, ry, destroyed_cells):
                    for dir in directions:
                        nx: int = rx + Dir.DX[dir]
                        ny: int = ry + Dir.DY[dir]
                        if (0 <= ny < len(self.grid))\
                           and (0 <= nx < len(self.grid[ny]))\
                           and self.grid[ry][rx] & dir\
                           and self.grid[ny][nx] != -1:
                            self.grid[ry][rx] ^= dir
                            self.grid[ny][nx] ^= Dir.OPPOSITE[dir]
                            destroyed_cells.append((rx, ry))
                            destroyed = True
                            break

    def generate(self) -> grid:
        """Fill the grid using the DFS algorithm
        then it randomly breaks walls to make it not perfect

        Returns:
            grid: the grid of the maze
        """
        self.dfs(0, 0)
        self.destroy_perfection()
        return self.grid
