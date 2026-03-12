__version__ = "0.1.0"
__author__ = "mchauvin, equentin. 42Lyon"

from mazegen.generator import MazeGenerator
from mazegen.algorithms import Algorithm
from mazegen.utils import grid, point, Directions

__all__ = ["MazeGenerator", "grid", "point", "Algorithm", "Directions"]
