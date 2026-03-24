__version__ = "0.1.0"
__author__ = "mchauvin, equentin. 42Lyon"

from mazegen.generator import MazeGenerator, DrawError
from mazegen.algorithms import Algorithm
from mazegen.utils import grid, point, Directions, FG_COLORS, BG_COLORS

__all__ = ["MazeGenerator", "DrawError", "grid", "point", "Algorithm",
           "Directions", "FG_COLORS", "BG_COLORS"]
