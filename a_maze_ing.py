from mazegen import MazeGenerator, Algorithm, DrawError
from mazegen.utils import point
from menu import Menu
from parser import parsed_info, get_point, get_int, get_bool, ConfigError
from termios import tcflush, TCIFLUSH
from typing import Optional
import sys
import time


def main() -> None:
    ALLOWED_KEYS: set[str] = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "SEED", "PERFECT", "OUTPUT_FILE", "PATH_ANIM"
        }
    try:
        with open("config.txt", "r") as file:
            data: dict[str, str] = parsed_info(file)
        unknown_keys: set[str] = set(data.keys()) - ALLOWED_KEYS
        if unknown_keys:
            raise ValueError(f"Unknown key(s) in "
                             f"config: {', '.join(unknown_keys)}")
        width: int = get_int(data, "WIDTH")
        height: int = get_int(data, "HEIGHT")
        entry: point = get_point(data, "ENTRY")
        exits: point = get_point(data, "EXIT")
        seed: int | None = None
        seed = get_int(data, "SEED") if "SEED" in data else None
        perfect_flag: bool = get_bool(data, "PERFECT")
        output_file_name: str | None = data.get("OUTPUT_FILE")
        if output_file_name is None:
            raise KeyError("missing key : OUTPUT_FILE")
        elif not output_file_name.endswith(".txt"):
            raise ValueError("OUTPUT_FILE must end with .txt")
        path_anim: bool = get_bool(data, "PATH_ANIM") if "PATH_ANIM" in data \
            else True
        sys.setrecursionlimit(1000000)
        maze: MazeGenerator = MazeGenerator(width, height, entry, exits, seed)
    except ConfigError as e:
        print(f"Config error line {e.line_index}: {e}", file=sys.stderr)
        return
    except (FileNotFoundError, PermissionError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        return
    except (ValueError, KeyError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        return
    path_state: bool = False
    path_steps: int = 0
    menu: Menu = Menu()

    def handle_exit(error: Optional[str] = None) -> None:
        menu.exiting = True
        if error:
            print(f"Exiting due to error:\n{error}", file=sys.stderr)
        else:
            print("Exiting...")
        Menu.set_cursor_visibility(True)
        tcflush(sys.stdin, TCIFLUSH)  # removes all pending input in stdin

    def path_display() -> None:
        nonlocal path_state
        nonlocal path_steps
        path_state = not path_state
        maze.reset_path_steps()
        path_steps = maze.get_path_length()

    def new_maze() -> None:
        nonlocal path_steps
        maze.create_grid()
        maze.draw_42()
        if not perfect_flag:
            maze.generate(Algorithm.DFS_NOT_PERFECT, None)
        else:
            maze.generate(Algorithm.HAK, None)
        maze.solver()
        path_steps = maze.get_path_length()

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
        nonlocal path_steps
        current_seed: int = maze.get_seed()
        switch_algo = Algorithm.DFS \
            if maze.get_algorithm() == "HAK" else Algorithm.HAK
        maze.create_grid()
        maze.draw_42()
        maze.generate(switch_algo, seed=current_seed)
        maze.solver()
        path_steps = maze.get_path_length()

    def gen_new_maze() -> None:
        nonlocal path_steps
        if perfect_flag is True:
            gen_maze = Algorithm.DFS \
                if maze.get_algorithm() == "DFS" else Algorithm.HAK
        else:
            gen_maze = Algorithm.DFS_NOT_PERFECT
        maze.create_grid()
        maze.draw_42()
        maze.generate(gen_maze, None)
        maze.solver()
        path_steps = maze.get_path_length()

    try:
        new_maze()
        with menu.visualizator():
            while not menu.exiting:
                menu.menu_list = [
                    ("Generate a new maze", gen_new_maze),
                    ("Show/Hide shortest path from the entrance to the exit",
                        path_display),
                    ("Change maze wall colours", color_wall),
                    ("Change path colours", color_path),
                    ("Change 42 colours", color_42),
                    ("Random colours", color_random),
                    (f"Seed: {maze.get_seed()} "
                     f"(Algorithm: {maze.get_algorithm()})", lambda: None)
                ]
                if perfect_flag:
                    menu.menu_list.append(("Switch algorithm", change_algo))
                menu.menu_list.append(("Exit", handle_exit))
                if not path_state or not path_anim:
                    path_steps = 0
                else:
                    for _ in range(path_steps - 1):
                        menu.show(menu.append_menu(maze.visualize(path_state,
                                                                  path_anim)))
                        delay: float = 1 / maze.get_path_length()
                        if delay >= 0.001:
                            time.sleep(delay)
                    path_steps = 0
                menu.show(menu.append_menu(maze.visualize(path_state,
                                                          path_anim)))

                with open(output_file_name, "w") as file:
                    file.write(maze.output())
                tcflush(sys.stdin, TCIFLUSH)
                menu.handle_keyboard_input()
    except DrawError as e:
        handle_exit(f"Caught DrawError, we were unable to draw:\n{e}")
    except KeyboardInterrupt:
        handle_exit()
    except PermissionError as e:
        handle_exit(f"{e}")
    except Exception as e:
        handle_exit(f"{e}")


if __name__ == "__main__":
    main()
