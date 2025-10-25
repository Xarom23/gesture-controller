import tkinter as tk
from principal import Principal

def start_up():
    root = tk.Tk()
    Principal(root)
    root.mainloop()


if __name__ == '__main__':
    start_up()
