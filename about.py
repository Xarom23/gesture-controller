import tkinter as tk
from tkinter.constants import *
from config import _bgcolor, _fgcolor


class AboutPage:
    def __init__(self, top=None):
        top.geometry("482x341+519+262")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Acerca de")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        ########### start #######################
        ########### end #######################

        self.Label1 = tk.Label(self.top)
        self.Label1.place(x=30, y=10, height=41, width=124)
        self.Label1.configure(activebackground="#d9d9d9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(anchor='w')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Segoe UI} -size 18 -weight bold -slant italic")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="#000000")
        self.Label1.configure(text='''Acerca de''')

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(x=30, y=70, height=235, width=425)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#ffffff")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="#000000")

        self.Message1 = tk.Message(self.Frame1)
        self.Message1.place(x=0, y=0, height=235, width=425)
        self.Message1.configure(anchor='nw')
        self.Message1.configure(aspect="300")
        self.Message1.configure(background="#ffffff")
        self.Message1.configure(foreground="#000000")
        self.Message1.configure(highlightbackground="#d9d9d9")
        self.Message1.configure(highlightcolor="#000000")
        self.Message1.configure(padx="1")
        self.Message1.configure(pady="1")
        self.Message1.configure(text='''Control de gestos humanos
V1.0
Desarrollado por Omar Luna Hernández
Este sistema fue desarrollado con el objetivo de explorar el uso de la inteligencia artificial y la visión por computadora para el control de interfaces mediante gestos humanos. Busca ofrecer una forma más natural e intuitiva de interacción entre el usuario y el equipo, facilitando el acceso y mejorando la experiencia de uso.

Software libre''')
        self.Message1.configure(width=425)
