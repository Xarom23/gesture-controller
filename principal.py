#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Clase Principal - Ventana principal del sistema de control por gestos

import tkinter as tk
from tkinter.constants import *
from config import _bgcolor, _fgcolor
from about import AboutPage
from settings import Settings
from camera_handler import CameraHandler


class Principal:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x351+410+253")  # Start with expanded view
        top.minsize(120, 1)
        top.maxsize(1540, 825)
        top.resizable(0, 0)
        top.title("Control por gestos")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top
        self.checkViewVideo = tk.StringVar(value='1')  # Activado por defecto
        self.checkViewLandmarks = tk.StringVar()
        self.acerca_de_window = None  # Referencia a la ventana "Acerca de"
        self.configuracion_window = None  # Referencia a la ventana "Configuración"

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        ########### start #######################
        self.sub_menu0 = tk.Menu(self.menubar, activebackground='#d9d9d9',
                                 activeborderwidth=1, activeforeground='black',
                                 background='#d9d9d9', borderwidth=1, disabledforeground='#a3a3a3',
                                 font="-family {Segoe UI} -size 9", foreground='#000000',
                                 tearoff=0)
        self.menubar.add_cascade(compound='left', font="TkDefaultFont",
                                 label='Ver', menu=self.sub_menu0, )
        self.sub_menu0.add_checkbutton(variable=self.checkViewVideo,
                                       compound='left', font="TkMenuFont", label='Ver video',
                                       command=self.toggle_canvas)
        self.sub_menu0.add_checkbutton(variable=self.checkViewLandmarks,
                                       compound='left', font="TkMenuFont",
                                       label='Ver puntos de referecia',
                                       command=self.toggle_landmarks)
        self.sub_menu1 = tk.Menu(self.menubar, activebackground='#d9d9d9',
                                 activeborderwidth=1, activeforeground='black',
                                 background='#d9d9d9', borderwidth=1, disabledforeground='#a3a3a3',
                                 font="-family {Segoe UI} -size 9", foreground='#000000',
                                 tearoff=0)
        self.menubar.add_cascade(compound='left', font="TkDefaultFont",
                                 label='Opciones', menu=self.sub_menu1, )
        self.sub_menu1.add_command(compound='left', font="TkMenuFont",
                                   label='Configuración', command=self.open_settings)
        self.sub_menu1.add_separator()
        # Obtener el estado inicial del control gestual
        from config import gesture_control_enabled
        initial_label = 'Desactivar control gestual' if gesture_control_enabled else 'Activar control gestual'
        self.sub_menu1.add_command(compound='left', font="TkMenuFont",
                                   label=initial_label,
                                   command=self.toggle_gesture_control)
        self.sub_menu2 = tk.Menu(self.menubar, activebackground='#d9d9d9',
                                 activeborderwidth=1, activeforeground='black',
                                 background='#d9d9d9', borderwidth=1, disabledforeground='#a3a3a3',
                                 font="-family {Segoe UI} -size 9", foreground='#000000',
                                 tearoff=0)
        self.menubar.add_cascade(compound='left', font="TkDefaultFont",
                                 label='Ayuda', menu=self.sub_menu2, )
        self.sub_menu2.add_command(compound='left', font="TkMenuFont",
                                   label='Acerca de', command=self.open_about)
        ########### end #######################

        self.Canvas1 = tk.Canvas(self.top)
        self.Canvas1.place(x=0, y=0, height=351, width=600)  # Visible por defecto
        self.Canvas1.configure(background="#d9d9d9")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="#000000")
        self.Canvas1.configure(insertbackground="#000000")
        self.Canvas1.configure(relief="ridge")
        self.Canvas1.configure(selectbackground="#d9d9d9")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.configure(state='normal')  # Enabled por defecto

        # Inicializar el manejador de cámara
        self.camera = CameraHandler(self.Canvas1, camera_index=0, width=600, height=351)
        # Iniciar la cámara automáticamente si el canvas está visible
        if self.checkViewVideo.get() == '1':
            self.camera.start()

    def toggle_canvas(self):
        '''Toggle canvas visibility and resize window'''
        if self.checkViewVideo.get() == '1':
            # Show canvas
            self.Canvas1.place(x=0, y=0, height=351, width=600)
            self.Canvas1.configure(state='normal')
            self.top.geometry("600x351+410+253")
            # Activar la visualización del video
            self.camera.set_show_video(True)
        else:
            # Hide canvas
            self.Canvas1.place_forget()
            self.Canvas1.configure(state='disabled')
            self.top.geometry("600x1+410+253")
            # Desactivar la visualización del video (la cámara sigue activa)
            self.camera.set_show_video(False)

    def toggle_landmarks(self):
        '''Toggle landmarks visibility'''
        if self.checkViewLandmarks.get() == '1':
            # Mostrar landmarks
            self.camera.set_show_landmarks(True)
        else:
            # Ocultar landmarks
            self.camera.set_show_landmarks(False)

    def open_window(self, window_ref_attr, window_class):
        '''Common function to open modal windows and keep them persistent on top of the main window

        Args:
            window_ref_attr: name of the attribute that holds the window reference (str)
            window_class: class of the window to instantiate
        '''
        # Get the reference to the existing window
        existing_window = getattr(self, window_ref_attr, None)

        # If the window already exists and is open, just focus it
        if existing_window is not None and existing_window.winfo_exists():
            existing_window.lift()  # Bring the window to the front
            existing_window.focus()
        else:
            # Create a new Toplevel window
            new_window = tk.Toplevel(self.top)
            # Make the window modal and keep it on top of the main window
            new_window.transient(self.top)  # Associated with the main window
            new_window.grab_set()  # Modal - blocks interaction with the main window
            # Save the reference to the new window
            setattr(self, window_ref_attr, new_window)
            # Create the instance of the corresponding class
            window_class(new_window)

    def open_about(self):
        '''Opens the "About" window'''
        self.open_window('acerca_de_window', AboutPage)

    def open_settings(self):
        '''Opens the "Settings" window'''
        self.open_window('configuracion_window', Settings)

    def toggle_gesture_control(self):
        '''Toggle gesture control and update menu label'''
        import config
        config.gesture_control_enabled = not config.gesture_control_enabled
        # Update menu label
        new_label = 'Activar control gestual' if not config.gesture_control_enabled else 'Desactivar control gestual'
        # Find the current label to update it
        current_label = 'Activar control gestual' if config.gesture_control_enabled else 'Desactivar control gestual'
        self.sub_menu1.entryconfigure(current_label, label=new_label)
