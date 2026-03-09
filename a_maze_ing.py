from mazegen import MazeGenerator, Algorithm
import sys


def main() -> None:
    maze: MazeGenerator = MazeGenerator(10, 10, (0, 0), (0, 0))
    sys.setrecursionlimit(1000000)
    print(maze.generate(Algorithm.DFS))
    print(maze.visualize())


if __name__ == "__main__":
    main()
