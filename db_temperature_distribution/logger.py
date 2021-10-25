import ctypes


def show_message(title: str, text: str) -> None:
    """Display native Windows information dialog."""
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)


class Logger:
    def __init__(self, show_dialogs: bool):
        self.show_dialogs = show_dialogs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.print_message(exc_type.__name__, exc_val)
        return True

    def print_message(self, title: str, message: str) -> None:
        if self.show_dialogs:
            show_message(title, message)
        else:
            print(f"{title}\n{'-' * len(title)}\n{message}")
