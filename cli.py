from enum import Enum
import os, keyboard, sys
from simple_term_menu import TerminalMenu


class STATES(Enum):
    MAIN = 0
    GETNSPLIT = 1


class SCREENS:
    def __init__(self, menu_title, *args) -> None:
        self.options = [x for x in args]
        self.options.append("Quit")
        
        self.terminal_menu = TerminalMenu(
            self.options, menu_cursor_style=("fg_blue", "bold"), title=menu_title
        )
        self.menu_entry_idx = None
        self.draw()

    def draw(self) -> None:
        self.menu_entry_idx = self.terminal_menu.show()

        if self.menu_entry_idx == len(self.options) - 1:
            sys.exit()


class MAIN(SCREENS):
    def __init__(self) -> None:
        super().__init__("MAIN", "GetN'Split Audio", "Classifty Audio")


class GetNSplit(SCREENS):
    def __init__(self) -> None:
        super().__init__(
            "GetN'Split Audio", "Get audio from URL", "Split audio from file"
        )


class CLI:
    def __init__(self) -> None:
        self.current_state = STATES.MAIN


def main():
    test = MAIN()


if __name__ == "__main__":
    main()
