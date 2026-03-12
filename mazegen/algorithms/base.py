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
        self.grid: grid = grid_

    @abstractmethod
    def generate(self) -> grid:
        pass
