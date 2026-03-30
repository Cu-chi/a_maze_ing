# MazeGenerator
Initialize a MazeGenerator

This class takes all settings of the maze and validates them
to create the base grid.
At instantiation it create a grid, but if you want to
use the same instance to re-generate a maze, you should
use the `create_grid()` method to clear the old grid

Example:
```
from mazegen import MazeGenerator, Algorithm

# instantiate the maze generator
maze = MazeGenerator(10, 10, (0, 0), (9, 9))

# this will set a special flag in the grid
# for the 42 cells at the middle
maze.draw_42()

# generate the maze using an algorithm of mazegen.algorithms
# it will fill the grid
maze.generate(Algorithm.DFS)

# it returns the path in order from the entry to the exit cell
# mandatory if you want to print the path in the visualization
maze.solver()

# visualize the maze (boolean for the visibility of the path)
print(maze.visualize(True))

# create output file to see the result of the generation  
with open("maze_output.txt", "w") as file:
    file.write(maze.output())
```

Args:
    width (int): Width of the maze
    height (int): Height of the maze
    entry (tuple[int, int]): Coordinates of the entry point
    exit (tuple[int, int]): Coordinates of the exit point
    seed (Optional[int]): seed to use for the generation

Raises:
    ValueError: if width is lower than 2
    ValueError: if height is lower than 2
    ValueError: if entry point is not in the maze
    ValueError: if exit point is not in the maze
    ValueError: if entry and exit point are the same
