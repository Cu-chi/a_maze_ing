from typing import Any, Callable, Generator
import sys
import termios
import contextlib


class Menu:
    def __init__(self) -> None:
        self.current_indexed: int = 0
        self.exiting: bool = False
        self.menu_list: list[tuple[str, Callable[[], Any]]] = []

    @staticmethod
    def set_cursor_position(x: int, y: int) -> None:
        sys.stdout.write(f"\033[{x};{y}H")

    @staticmethod
    @contextlib.contextmanager
    def visualizator() -> Generator[None, None, None]:
        fd: int = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = termios.tcgetattr(fd)
        # this will edit local config of stdin
        # we disable echo (to avoid key pressed from being
        # printed)
        # we disable ICANON, so input is available immediately (without the
        # user having to type a line-delimiter character
        # man termios:
        # https://man7.org/linux/man-pages/man3/termios.3.html
        new_settings[3] &= ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
            yield  # execute code inside with statement
        finally:
            # on exit or error, we put back the original config
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @staticmethod
    def show(output: str) -> None:
        Menu.set_cursor_position(0, 0)
        sys.stdout.write(output)
        sys.stdout.flush()

    def append_menu(self, output: str) -> str:
        output += "\n"
        for i, menu_data in enumerate(self.menu_list):
            if self.current_indexed == i:
                output += "\033[47m\033[30m"
            output += f"{i}: " + menu_data[0] + "\033[0m\n"
        return output

    @staticmethod
    def get_key() -> str:
        char: str = sys.stdin.read(1)
        if char == "\033":
            char_special = sys.stdin.read(2)
            char += char_special
            if char == "\033[A":
                return "UP"
            elif char == "\033[B":
                return "DOWN"
        return char

    def handle_keyboard_input(self) -> None:
        key: str = self.get_key()
        if key == "UP":
            if self.current_indexed > 0:
                self.current_indexed -= 1
        if key == "DOWN":
            if self.current_indexed < len(self.menu_list) - 1:
                self.current_indexed += 1
        if key == '\n':
            self.menu_list[self.current_indexed][1]()
