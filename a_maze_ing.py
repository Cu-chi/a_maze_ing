from mazegen import MazeGenerator, Algorithm
import sys


def main() -> None:
    maze: MazeGenerator = MazeGenerator(11, 11, (0, 0), (0, 0))
    sys.setrecursionlimit(1000000)
    maze.draw_42()
    print(maze.generate(Algorithm.DFS))
    print(maze.visualize())


if __name__ == "__main__":
    main()
