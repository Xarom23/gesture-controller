"""
Main Entry Point
-----------------
Application entry point that initializes and starts the gesture control system.
Creates the root Tkinter window and launches the Principal interface.
"""

import tkinter as tk
from principal import Principal


def start_up():
    """Initialize and start the main application"""
    root = tk.Tk()
    Principal(root)
    root.mainloop()


if __name__ == '__main__':
    start_up()
