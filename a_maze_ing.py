from mazegen import MazeGenerator, Algorithm, DrawError
from mazegen.utils import point
from menu import Menu
from parser import parsed_info, get_point, get_int
import sys
from termios import tcflush, TCIFLUSH


def main() -> None:
    try:
        with open("config.txt", "r") as file:
            data: dict[str, str] = parsed_info(file)
    except FileNotFoundError:
        print("Error opening the configuration file.")
    try:
        width: int = get_int(data, "WIDTH")
        height: int = get_int(data, "HEIGHT")
        entry: point = get_point(data, "ENTRY")
        exits: point = get_point(data, "EXIT")
        seed: int | None = None
        seed = get_int(data, "SEED") if "SEED" in data else None
        sys.setrecursionlimit(1000000)
        maze: MazeGenerator = MazeGenerator(width, height, entry, exits, seed)
    except (ValueError, KeyError) as e:
        print(f"Config error: {e}")
        return
    path_state: bool = False
    menu: Menu = Menu()

    def handle_exit() -> None:
        menu.exiting = True
        print("Exiting...")
        Menu.set_cursor_visibility(True)
        tcflush(sys.stdin, TCIFLUSH)  # removes all pending input in stdin

    def path_display() -> None:
        nonlocal path_state
        path_state = not path_state

    def new_maze() -> None:
        maze.create_grid()
        maze.draw_42()
        maze.generate(Algorithm.DFS, None)
        maze.solver()

    def color_path() -> None:
        maze.rotate_color("PATH")

    def color_42() -> None:
        maze.rotate_color("42")

    def color_wall() -> None:
        maze.rotate_color("WALL")

    def color_random() -> None:
        color_path()
        color_42()
        color_wall()

    def change_algo() -> None:
        current_seed: int = maze.get_seed()
        switch_algo = Algorithm.DFS \
            if maze.get_algorithm() == "HAK" else Algorithm.HAK
        maze.create_grid()
        maze.draw_42()
        maze.generate(switch_algo, seed=current_seed)
        maze.solver()

    try:
        new_maze()
        with menu.visualizator():
            while not menu.exiting:
                menu.menu_list = [
                    ("Generate a new maze", new_maze),
                    ("Show/Hide shortest path from the entrance to the exit",
                        path_display),
                    ("Change maze wall colours", color_wall),
                    ("Change path colours", color_path),
                    ("Change 42 colours", color_42),
                    ("Random colours", color_random),
                    ("Switch algorithm", change_algo),
                    (f"Seed: {maze.get_seed()} "
                     f"(Algorithm: {maze.get_algorithm()})", lambda: None),
                    ("Exit", handle_exit)
                ]
                menu.show(menu.append_menu(maze.visualize(path_state)))
                with open("maze.txt", "w") as file:
                    file.write(maze.output())
                menu.handle_keyboard_input()
    except DrawError as e:
        print("Caught DrawError, we were unable to draw:\n"
              f"{e}")
        handle_exit()
    except KeyboardInterrupt:
        handle_exit()


if __name__ == "__main__":
    main()
