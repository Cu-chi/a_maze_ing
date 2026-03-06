from mazegen import MazeGenerator, Algorithm


def main() -> None:
    maze: MazeGenerator = MazeGenerator(10, 10, (0, 0), (9, 9))
    maze.generate(Algorithm.HAK)
    maze.generate(Algorithm.DFS)


if __name__ == "__main__":
    main()
