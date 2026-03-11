from mazegen import MazeGenerator, Algorithm
from menu import Menu
from parser import parsed_info
from io import TextIOWrapper
import sys
from termios import tcflush, TCIFLUSH


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
    seed: int | None = None
    try:
        if "SEED" in data:
            seed = int(data["SEED"])
    except ValueError:
        print("Error: seed has to be a int.")
        return

    sys.setrecursionlimit(1000000)
    maze: MazeGenerator = MazeGenerator(width, height, entry, exit, seed)
    path_state: bool = False
    menu: Menu = Menu()

    def handle_exit() -> None:
        menu.exiting = True
        print("Exiting...")
        sys.stdout.write("\033[?25h")  # show cursor
        tcflush(sys.stdin, TCIFLUSH)  # removes all pending input in stdin

    def path_display() -> None:
        nonlocal path_state
        path_state = not path_state

    def new_maze() -> None:
        maze.create_grid()
        maze.draw_42()
        maze.generate(Algorithm.HAK)
        maze.solve_bfs()
        menu.need_refresh = True

    new_maze()
    try:
        while not menu.exiting:
            if menu.need_refresh:
                menu.menu_list = [
                    ("Generate a new maze", new_maze),
                    ("Show/Hide shortest path from the entrance to the exit",
                        path_display),
                    ("Change maze wall colours", lambda: None),
                    ("Edit colours of the 42 pattern", lambda: None),
                    (f"Seed: {maze.get_seed()}", lambda: None),
                    ("Exit", handle_exit)
                ]
                menu.need_refresh = False
                sys.stdout.write("\033c\033[?25l")  # clear and hide cursor
                menu.show(menu.append_menu(maze.visualize(path_state)))
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    main()
