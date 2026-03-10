from pynput import keyboard
from typing import Any, Callable
import functools
import sys


class Menu:
    def __init__(self, menu: list[tuple[str, Callable[[], Any]]]) -> None:
        self.current_indexed: int = 0
        self.exiting: bool = False
        self.menu: list[tuple[str, Callable[[], Any]]] = menu
        self.need_refresh: bool = True
        self.listener: keyboard.Listener = keyboard.Listener(
            on_press=functools.partial(Menu.handle_keyboard_press, self),
            suppress=True
        )
        self.listener.start()

    @staticmethod
    def set_cursor_position(x: int, y: int) -> None:
        sys.stdout.write(f"\033[{x};{y}H")

    @staticmethod
    def show(output: str) -> None:
        Menu.set_cursor_position(0, 0)
        sys.stdout.write(output)
        sys.stdout.flush()

    def append_menu(self, output: str) -> str:
        output += "\n"
        for i, menu_data in enumerate(self.menu):
            if self.current_indexed == i:
                output += "\033[47m\033[30m"
            output += f"{i}: " + menu_data[0] + "\033[0m\n"
        return output

    def handle_keyboard_press(self,
                              key: keyboard.Key |
                              keyboard.KeyCode |
                              None) -> None:
        try:
            self.need_refresh = True
            if keyboard.Key.up == key:
                if self.current_indexed > 0:
                    self.current_indexed -= 1
            if keyboard.Key.down == key:
                if self.current_indexed < len(self.menu) - 1:
                    self.current_indexed += 1
            if keyboard.Key.enter == key:
                self.menu[self.current_indexed][1]()
        except Exception:
            pass
