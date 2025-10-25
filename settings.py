#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Clase Toplevel2 (Configuración) - Ventana de configuración del sistema

import tkinter as tk
from tkinter.constants import *
from config import _bgcolor, _fgcolor


class Settings:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x360+512+341")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(0, 0)
        top.title("Configuración")
        top.configure(borderwidth="2")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top

        # Configurar el grid principal para que se expanda
        top.grid_columnconfigure(0, weight=1)

        # Frame para botones de acción
        self.button_frame = tk.Frame(self.top)
        self.button_frame.grid(row=3, column=0, pady=20)
        self.button_frame.configure(background="#d9d9d9")

        # Botones de acción
        self.Button1 = tk.Button(self.button_frame)
        self.Button1.grid(row=0, column=0, padx=10)
        self.Button1.configure(background="#d9d9d9", text='Guardar')

        self.Button2 = tk.Button(self.button_frame)
        self.Button2.grid(row=0, column=1, padx=10)
        self.Button2.configure(background="#d9d9d9", text='Restablecer')

        # Frame para gestos faciales
        self.Labelframe2 = tk.LabelFrame(self.top)
        self.Labelframe2.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        self.Labelframe2.configure(relief='groove', text='Gestos faciales', background="#d9d9d9")
        self.Labelframe2.grid_columnconfigure(0, weight=1)
        self.Labelframe2.grid_columnconfigure(2, weight=1)

        # Contenido del frame de gestos faciales
        self.Label3 = tk.Label(self.Labelframe2)
        self.Label3.grid(row=0, column=0, padx=5, pady=5)
        self.Label3.configure(background="#d9d9d9", text='Parpadeo izquierdo')

        self.Message2 = tk.Message(self.Labelframe2)
        self.Message2.grid(row=1, column=0, padx=5, pady=5)
        self.Message2.configure(background="#ffffff", text='Click izquierdo', width=90)

        self.Button4 = tk.Button(self.Labelframe2)
        self.Button4.grid(row=0, column=1, rowspan=2, padx=20)
        self.Button4.configure(background="#d9d9d9", text='Intercambiar')

        self.Label4 = tk.Label(self.Labelframe2)
        self.Label4.grid(row=0, column=2, padx=5, pady=5)
        self.Label4.configure(background="#d9d9d9", text='Parpadeo derecho')

        self.Message3 = tk.Message(self.Labelframe2)
        self.Message3.grid(row=1, column=2, padx=5, pady=5)
        self.Message3.configure(background="#ffffff", text='Click derecho', width=100)

        # Frame para gestos de las manos
        self.Labelframe1 = tk.LabelFrame(self.top)
        self.Labelframe1.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.Labelframe1.configure(relief='groove', text='Gestos de las manos', background="#d9d9d9")
        self.Labelframe1.grid_columnconfigure(0, weight=1)
        self.Labelframe1.grid_columnconfigure(2, weight=1)

        # Contenido del frame de gestos de manos
        self.Label5 = tk.Label(self.Labelframe1)
        self.Label5.grid(row=0, column=0, padx=5, pady=5)
        self.Label5.configure(background="#d9d9d9", text='Mano izquierda')

        self.Message4 = tk.Message(self.Labelframe1)
        self.Message4.grid(row=1, column=0, padx=5, pady=5)
        self.Message4.configure(background="#ffffff", text='Flechas del teclado', width=140)

        self.Button3 = tk.Button(self.Labelframe1)
        self.Button3.grid(row=0, column=1, rowspan=2, padx=20)
        self.Button3.configure(background="#d9d9d9", text='Intercambiar')

        self.Label6 = tk.Label(self.Labelframe1)
        self.Label6.grid(row=0, column=2, padx=5, pady=5)
        self.Label6.configure(background="#d9d9d9", text='Mano derecha')

        self.Message5 = tk.Message(self.Labelframe1)
        self.Message5.grid(row=1, column=2, padx=5, pady=5)
        self.Message5.configure(background="#ffffff", text='Cursor del ratón', width=90)

        # Frame superior con título
        self.Frame2 = tk.Frame(self.top)
        self.Frame2.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.Frame2.configure(relief='groove', borderwidth="2", background="#d9d9d9")
        
        # Título
        self.Label2 = tk.Label(self.Frame2)
        self.Label2.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.Label2.configure(
            background="#d9d9d9",
            font="-family {Segoe UI} -size 20 -weight bold -slant italic",
            text='Configuración'
        )

    def popup0(self, event, *args, **kwargs):
        self.Popupmenu1.post(event.x_root, event.y_root)
