from mazegen import MazeGenerator, Algorithm
from menu import Menu
from parser import parsed_info
from typing import Callable
import sys


def main() -> None:
    file: sys.TextIOWrapper = open("config.txt")
    data: dict = parsed_info(file)
    if "WIDTH" in data.keys():
        width: int = int(data.get("WIDTH"))
    if "HEIGHT" in data.keys():
        height: int = int(data.get("HEIGHT"))
    if "ENTRY" in data.keys():
        entries: tuple = data.get("ENTRY").split(",")
        first_entry = int(entries[0])
        second_entry = int(entries[1])
        entry: tuple[int, int] = (first_entry, second_entry)
    if "EXIT" in data.keys():
        exits: tuple = data.get("EXIT").split(",")
        first_exit = int(exits[0])
        second_exit = int(exits[1])
        exit: tuple[int, int] = (first_exit, second_exit)
    maze: MazeGenerator = MazeGenerator(width, height, entry, exit)
    sys.setrecursionlimit(1000000)
    maze.draw_42()
    maze.generate(Algorithm.HAK)

    def new_maze() -> None:
        maze.create_grid()
        maze.draw_42()
        maze.generate(Algorithm.HAK)

    menu_list: list[tuple[str, Callable[[], None]]] = [
            ("Generate a new maze", new_maze),
            ("Show/Hide shortest path from the entrance to the exit",
             lambda: None),
            ("Change maze wall colours", lambda: None),
            ("Edit colours of the 42 pattern", lambda: None)
        ]
    menu: Menu = Menu(menu_list)

    def handle_exit() -> None:
        menu.exiting = True
        print("Exiting...")
        sys.stdout.write("\033[?25h")  # restore cursor visibility
    menu.menu.append(("Exit", handle_exit))
    try:
        while not menu.exiting:
            sys.stdout.write("\033c")
            menu.show(menu.append_menu(maze.visualize()))
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    main()
