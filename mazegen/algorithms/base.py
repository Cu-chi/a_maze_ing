from abc import ABC, abstractmethod
from enum import Enum
from mazegen.utils import grid


class Algorithm(Enum):
    """All supported algorithms
    """

    DFS = 0
    """Depth-First-Search algorithm"""

    HAK = 1
    """Hunt-And-Kill algorithm"""


class BaseAlgorithm(ABC):
    def __init__(self, grid_: grid) -> None:
        self.N, self.E, self.S, self.W = 1, 2, 4, 8

        self.DX: dict[int, int] = {self.N: 0, self.S: 0,
                                   self.E: 1, self.W: -1}
        self.DY: dict[int, int] = {self.N: -1, self.S: 1,
                                   self.E: 0, self.W: 0}

        self.OPPOSITE: dict[int, int] = {self.N: self.S, self.S: self.N,
                                         self.E: self.W, self.W: self.E}
        self.grid: grid = grid_

    @abstractmethod
    def generate(self) -> grid:
        pass
