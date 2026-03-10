from mazegen import MazeGenerator, Algorithm
from parser import parsed_info
import sys


def main() -> None:
    file: sys.TextIOWrapper = open("config.txt")
    data: dict = parsed_info(file)
    try:
        if "WIDTH" in data.keys():
            width: int = int(data.get("WIDTH"))
    except ValueError:
        print("Error: width has to be a integer.")
        return
    try:
        if "HEIGHT" in data.keys():
            height: int = int(data.get("HEIGHT"))
    except ValueError:
        print("Error: height has to be a integer.")
        return
    try:
        if "ENTRY" in data.keys():
            entries: tuple = data.get("ENTRY").split(",")
            first_entry = int(entries[0])
            second_entry = int(entries[1])
            entry: tuple[int, int] = (first_entry, second_entry)
    except ValueError:
        print("Error: entry has to be a tuple of integers.")
        return
    try:
        if "EXIT" in data.keys():
            exits: tuple = data.get("EXIT").split(",")
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
    print(maze.visualize())


if __name__ == "__main__":
    main()
