from mazegen import MazeGenerator, Algorithm
from parser import parsed_info
from io import TextIOWrapper
import sys


def main() -> None:
    file: TextIOWrapper = open("config.txt")
    data: dict[str, str] = parsed_info(file)
    try:
        if "WIDTH" in data:
            width: int = int(data["WIDTH"])
    except ValueError:
        print("Error: width has to be a integer.")
        return
    try:
        if "HEIGHT" in data:
            height: int = int(data["HEIGHT"])
    except ValueError:
        print("Error: height has to be a integer.")
        return
    try:
        if "ENTRY" in data:
            entry_str: str = data["ENTRY"]
        if isinstance(entry_str, str):
            entries: list[str] = entry_str.split(",")
            first_entry = int(entries[0])
            second_entry = int(entries[1])
            entry: tuple[int, int] = (first_entry, second_entry)
    except ValueError:
        print("Error: entry has to be a tuple of integers.")
        return
    try:
        if "EXIT" in data:
            exit_str: str = data["EXIT"]
        if isinstance(exit_str, str):
            exits: list[str] = exit_str.split(",")
            first_exit = int(exits[0])
            second_exit = int(exits[1])
            exit: tuple[int, int] = (first_exit, second_exit)
    except ValueError:
        print("Error: exit has to be a tuple of integers.")
        return
    maze: MazeGenerator = MazeGenerator(width, height, entry, exit)
    sys.setrecursionlimit(1000000)
    maze.draw_42()
    print(maze.generate(Algorithm.HAK))
    maze.solve_bfs(entry, exit)
    print(maze.visualize(True))


if __name__ == "__main__":
    main()
