"""Module to manage logging events."""

import ctypes


def show_message(title: str, text: str) -> None:
    """Display native Windows information dialog."""
    ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0)


class Logger:
    """
    Handle error reporting.

    Parameters
    ----------
    show_dialogs : bool
        A flag to control error output stream, set True for native dialog,
        False for console.

    """

    def __init__(self, show_dialogs: bool):
        self.show_dialogs = show_dialogs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.print_message(exc_type.__name__, exc_val)
        return True

    def print_message(self, title: str, message: str) -> None:
        """Report message to native dialog or console."""
        if self.show_dialogs:
            show_message(title, message)
        else:
            print(f"{title}\n{'-' * len(title)}\n{message}")
