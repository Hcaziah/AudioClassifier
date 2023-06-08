from simple_term_menu import TerminalMenu


def main():
    options = ["GetNSplit", "Classify", "Quit"]
    terminal = TerminalMenu(options, menu_cursor_style=("fg_blue", "bold"), title="Main")

    menu_entry_idx = terminal.show()
    print(f"you have selection {options[menu_entry_idx]}")


if __name__ == "__main__":
    main()
